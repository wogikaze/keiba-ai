"""仮説探索の実験を 1 つ走らせる（ADR 0005）。実験ディレクトリの config.yaml の search を読み、results.json を書く。

uv run --extra ml python scripts/run_search.py experiments/<dir>
    --smoke   1/20 のレース・seed 1 つ・反復を減らして走らせ、/tmp に書く（動作確認用）
予測は data/processed/jra-van/derived/preds_<dir>.parquet に保存する（後の実験の init に使える）。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import polars as pl
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from keiba_ai import features as F  # noqa: E402
from keiba_ai import search as S  # noqa: E402


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exp")
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    exp = (ROOT / a.exp).resolve()
    cfg = yaml.safe_load((exp / "config.yaml").read_text(encoding="utf-8"))
    sc = cfg["search"]
    n_boot = cfg.get("eval", {}).get("n_boot", 2000)
    t0 = time.time()
    git_hash = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain", "--", "src", "scripts/run_search.py", str(exp.relative_to(ROOT)))
    extra = []
    for path in sc.get("extra_preds", []):  # 前の実験の予測を列として足す（init に使うなど）
        e = pl.read_parquet(ROOT / path["path"], columns=["race_key", "umaban", path["col"]])
        extra.append(e.rename({path["col"]: path["as"]}))
    pdf = S.load_frame(extra)
    if a.smoke:
        keys = pdf["race_key"].unique()
        keep = set(keys[np.random.default_rng(0).random(len(keys)) < 0.05])
        pdf = pdf[pdf["race_key"].isin(keep)].reset_index(drop=True)
        sc = {**sc, "seeds": sc.get("seeds", [42])[:1], "num_boost_round": 50}
        n_boot = 100
    p, infos = S.predict(pdf, sc)
    pdf["p_new"] = p
    r = S.evaluate(pdf, "p_new", n_boot=n_boot, seed=cfg.get("seed", 42))
    head = {f"search_{k}": v for k, v in S.headline(r).items()}
    res = {"experiment": exp.name, "status": "done", "git_hash": git_hash, "git_dirty_tracked_paths": dirty or None,
           "data_version": F.data_version(F.DATA_DIR, F.FeatureConfig.from_dict(S.FEATURE_CONFIG)) + "+market_v1",
           "seed": cfg.get("seed", 42), "split": "2004-2018/2019-2021/2022-2025",
           "metrics": head, "eval": r, "train": infos, "n_races": pdf.groupby("split")["race_key"].nunique().to_dict(),
           "runtime_s": round(time.time() - t0, 1),
           "note": "test は探索中の参考値（ADR 0005: 採否は valid だけで決める）"}
    out = Path("/tmp") / f"{exp.name}-smoke.json" if a.smoke else exp / "results.json"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    if not a.smoke:
        pl.from_pandas(pdf[["race_key", "umaban", "date", "split", "p_mkt", "p_new", "y"]]).write_parquet(
            F.DATA_DIR / "derived" / f"preds_{exp.name}.parquet")
    print(json.dumps(head, indent=1, default=float))


if __name__ == "__main__":
    main()

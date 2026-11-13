"""市場オフセット LightGBM の予測を作り直して保存する（この実験の入力）。

experiments/2026-11-14_market-combination/run.py の load_frame と offset_lgbm を、その実験の config.yaml のまま呼ぶ。
あの実験は予測を保存していなかった。test の race logloss が 1.9317（あの実験の値）に戻ることを確かめる。

uv run --extra ml python experiments/2026-11-14_betting-policies/make_preds.py
出力: data/processed/jra-van/derived/preds_offset_lgbm.parquet と .json（git_hash・logloss）
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("mc", ROOT / "experiments/2026-11-14_market-combination/run.py")
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)


def main():
    git_hash = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    pdf, universe, fcfg, k = mc.load_frame()
    pdf["p_mkt"] = mc.mo.market_probs(pdf[["race_key", "odds_10"]], "power_fit", k=k, odds="odds_10")["p_market"].to_numpy()
    p, info = mc.offset_lgbm(pdf)
    pdf["p_offset"] = p
    ll = {}
    for s in ("train", "valid", "test"):
        d = pdf[pdf["split"] == s]
        w = d[d["y"] == 1]
        # 同着は等分（evaluate.race_scores と同じ）
        t = w.groupby("race_key")["p_offset"].apply(lambda v: -np.mean(np.log(v))).mean()
        ll[s] = float(t)
    out = mc.F.DATA_DIR / "derived" / "preds_offset_lgbm.parquet"
    pl.from_pandas(pdf[["race_key", "umaban", "date", "split", "p_mkt", "p_offset", "y"]]).write_parquet(out)
    meta = {"git_hash": git_hash, "power_fit_k": k, "race_logloss": ll, "offset_info": info, "universe": universe}
    out.with_suffix(".json").write_text(json.dumps(meta, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(json.dumps(ll), flush=True)


if __name__ == "__main__":
    main()

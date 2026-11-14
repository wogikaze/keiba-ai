"""2 つの探索の予測を同じレースで比べる（ADR 0005 の採否: 対になった差の開催日ブートストラップ）。

uv run --extra ml python scripts/compare_preds.py <新しい実験> <基準の実験> [--split valid]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from keiba_ai import evaluate as ev  # noqa: E402
from keiba_ai.features import DATA_DIR  # noqa: E402


def load(name: str) -> pl.DataFrame:
    return pl.read_parquet(DATA_DIR / "derived" / f"preds_{name}.parquet")


def compare(new: str, ref: str, split: str = "valid", n_boot: int = 2000) -> dict:
    a = load(new).filter(pl.col("split") == split)
    b = load(ref).filter(pl.col("split") == split).select("race_key", "umaban", p_ref="p_new")
    d = a.join(b, on=["race_key", "umaban"], how="inner").to_pandas()
    d["date"] = pd.to_datetime(d["date"])
    d["race_id"] = d["race_key"]
    r = ev.delta_logloss(d, "p_new", "p_ref", cluster="date", n_boot=n_boot, seed=0)
    return {"new": new, "ref": ref, "split": split, **{k: r[k] for k in ("delta", "ci", "se", "n_races")},
            "adopt": bool(r["delta"] < -r["se"])}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("ref")
    ap.add_argument("--split", default="valid")
    a = ap.parse_args()
    print(json.dumps(compare(a.new, a.ref, a.split), ensure_ascii=False, default=float))

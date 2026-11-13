"""JRA-VAN の生データから data/processed/jra-van/ の parquet を作る。

    uv run --extra ml python scripts/build_dataset.py                       # 全テーブル
    uv run --extra ml python scripts/build_dataset.py --tables races entries --years 2024
    uv run --extra ml python scripts/build_dataset.py --validate            # 検証の集計を表示

差分更新: 生ファイルの大きさと更新時刻が前回と同じなら読み直さない。--force で全部読み直す。
--years は読み直す生ファイル（RACE/<年>.txt、SLOP/<年>.txt、0B41/<年>/）を絞る。
仕上げのテーブルは、それまでに取り込んだ全ファイルから作る。
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from keiba_ai.jvdata.build import TABLES, Paths, run  # noqa: E402

DEFAULT_RAW = Path(os.environ.get("KEIBA_JRAVAN_RAW", "/mnt/e/keiba-ai/jra-van/raw"))


def parse_years(s: str | None) -> set[int] | None:
    if not s:
        return None
    out: set[int] = set()
    for part in s.split(","):
        a, _, b = part.partition("-")
        out |= set(range(int(a), int(b or a) + 1))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tables", nargs="+", default=["all"], choices=["all", *TABLES])
    ap.add_argument("--years", help="例: 2024 / 2020-2024 / 2019,2024")
    ap.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    ap.add_argument("--out", type=Path, default=ROOT / "data/processed/jra-van")
    ap.add_argument("--spec", type=Path, default=ROOT / "data/raw/jra-van/specs/text/JV-Data仕様書__フォーマット.csv")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--force", action="store_true", help="変更がなくても読み直す")
    ap.add_argument("--validate", action="store_true", help="作ったテーブルを検証して結果を表示する")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")

    paths = Paths(raw=args.raw, out=args.out, spec=args.spec)
    if args.validate:
        from keiba_ai.jvdata.validate import report

        print(report(paths))
        return
    tables = list(TABLES) if "all" in args.tables else args.tables
    run(paths, tables, parse_years(args.years), args.jobs, args.force)


if __name__ == "__main__":
    main()

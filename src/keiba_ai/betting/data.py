"""賭けのシミュレーションに使うテーブルの読み込み（docs/data/processed.md のテーブルから）。

- place_snapshot(N): 発走 N 分前の中間オッズの複勝（odds_ts_win から。market_odds.pre_deadline_odds と同じ決め方）
- quinella_snapshot(N): 0B42 の馬連の N 分前のスナップショット（odds_ts_quinella_snap）
- final_exotic(bet_type): 確定オッズ（odds_final_<券種>）。組番はコード（combos.combo_code と同じ）に直す
- payouts_by_type(bet_type): 払戻（不成立・特払・返還の券種は除く）
- pools(): 単勝・複勝の総票数（odds_final、円）と複勝の払戻着数
"""

from __future__ import annotations

from pathlib import Path

import polars as pl

from keiba_ai.baselines.market_odds import DATA_DIR, INTERMEDIATE

TAKEOUT = {"win": 0.20, "place": 0.20, "quinella": 0.225, "wide": 0.225, "exacta": 0.25, "trio": 0.25,
           "trifecta": 0.275}


def _derived(data_dir: Path) -> Path:
    d = data_dir / "derived"
    d.mkdir(parents=True, exist_ok=True)
    return d


def place_snapshot(minutes_before: int, *, data_dir: Path | None = None, refresh: bool = False) -> pl.DataFrame:
    """列: race_key, umaban, place_odds_min, place_odds_max, place_status, announced_at。"""
    data_dir = Path(data_dir or DATA_DIR)
    out = _derived(data_dir) / f"place_odds_{int(minutes_before)}.parquet"
    ts_dir = data_dir / "odds_ts_win"
    srcs = [data_dir / "races.parquet", *ts_dir.glob("year=*/*.parquet")]
    if not refresh and out.exists() and out.stat().st_mtime >= max(p.stat().st_mtime for p in srcs):
        return pl.read_parquet(out)
    post = pl.scan_parquet(data_dir / "races.parquet").select("race_key", "post_at")
    parts = []
    for ydir in sorted(ts_dir.glob("year=*")):
        lf = (pl.scan_parquet(ydir / "*.parquet")
              .filter(pl.col("data_kubun") == INTERMEDIATE)
              .select("race_key", "umaban", "place_odds_min", "place_odds_max", "place_status", "announced_at")
              .join(post, on="race_key", how="inner")
              .filter(pl.col("announced_at") <= pl.col("post_at") - pl.duration(minutes=int(minutes_before)))
              .filter(pl.col("announced_at") == pl.col("announced_at").max().over("race_key"))
              .drop("post_at"))
        parts.append(lf.collect())
    df = pl.concat(parts)
    df = df.filter(pl.col("announced_at") == pl.col("announced_at").max().over("race_key")).sort("race_key", "umaban")
    df.write_parquet(out)
    return df


def _code(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(code=pl.col("combination").cast(pl.Int64, strict=False))


def quinella_snapshot(snap: str, *, data_dir: Path | None = None, race_keys=None) -> pl.DataFrame:
    data_dir = Path(data_dir or DATA_DIR)
    lf = pl.scan_parquet(data_dir / "odds_ts_quinella_snap" / "**" / "*.parquet", hive_partitioning=True)
    lf = lf.filter(pl.col("snap") == snap)
    if race_keys is not None:
        lf = lf.filter(pl.col("race_key").is_in(list(race_keys)))
    return _code(lf.select("race_key", "combination", "odds", "status", "vote_total").collect())


def final_exotic(bet_type: str, *, data_dir: Path | None = None, race_keys=None) -> pl.DataFrame:
    """列: race_key, code, odds（ワイドは odds_min を odds として返し、odds_max も付ける）, status, vote_total。"""
    data_dir = Path(data_dir or DATA_DIR)
    p = data_dir / f"odds_final_{bet_type}"
    lf = (pl.scan_parquet(p / "**" / "*.parquet", hive_partitioning=True) if p.is_dir()
          else pl.scan_parquet(p.with_suffix(".parquet")))
    if race_keys is not None:
        lf = lf.filter(pl.col("race_key").is_in(list(race_keys)))
    cols = lf.collect_schema().names()
    sel = ["race_key", "combination", "status", "vote_total"]
    if "odds_min" in cols:
        lf = lf.with_columns(odds=pl.col("odds_min"))
        sel += ["odds", "odds_max"]
    else:
        sel += ["odds"]
    return _code(lf.select(sel).collect())


def payouts_by_type(bet_type: str, *, data_dir: Path | None = None) -> pl.DataFrame:
    """列: race_key, code, payout（100 円あたり）。不成立・特払・返還のあるレースのその券種は落とす。"""
    data_dir = Path(data_dir or DATA_DIR)
    df = pl.read_parquet(data_dir / "payouts.parquet").filter(pl.col("bet_type") == bet_type)
    bad = df.filter((pl.col("not_established") == 1) | (pl.col("special_payout") == 1)
                    | (pl.col("refund") == 1))["race_key"].unique()
    return _code(df.filter(~pl.col("race_key").is_in(bad.implode()))).select("race_key", "code", "payout")


def pools(*, data_dir: Path | None = None) -> pl.DataFrame:
    """レースごと: win_pool, place_pool（円、確定時）, place_pay_key（2 か 3）。"""
    data_dir = Path(data_dir or DATA_DIR)
    return (pl.read_parquet(data_dir / "odds_final.parquet",
                            columns=["race_key", "win_vote_total", "place_vote_total", "place_pay_key"])
            .group_by("race_key").agg(win_pool=pl.col("win_vote_total").max(),
                                      place_pool=pl.col("place_vote_total").max(),
                                      place_pay_key=pl.col("place_pay_key").max()))

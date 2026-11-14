"""決定時刻（発走 N 分前）までに見えている市場の特徴量 market_v1（ADR 0005）。1 行 = 1 レースの 1 馬番。

すべて中間オッズ（データ区分 1）のうち ``announced_at <= post_at − 10 分`` の発表だけから作る。
確定オッズ・10 分前より後の発表・当日の結果は使わない。

    snapshots(data_dir) -> 10・15・20・30・60 分前と最初の中間オッズの単勝・複勝・票数（横持ち）
    quinella_marginal(data_dir) -> 10 分前の馬連オッズから作った各馬の周辺確率
    build(df_snap, df_q) -> 特徴量（列は FEATURES）
    load_market_features(data_dir) -> キャッシュつきで build まで
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import polars as pl

from keiba_ai.baselines.market_odds import DATA_DIR, INTERMEDIATE

VERSION = "market_v1"
DECISION_MIN = 10
SNAPS = (10, 15, 20, 30, 60)
COLS = ("win_odds", "place_odds_min", "place_odds_max", "win_vote_total", "place_vote_total")

FEATURES: dict[str, str] = {
    "mk_logodds": "10 分前の単勝オッズの対数",
    "mk_rank": "10 分前の単勝オッズのレース内順位（1 が最低オッズ）",
    "mk_rank_frac": "順位 / 頭数",
    "mk_d15": "log(15 分前のオッズ / 10 分前のオッズ)",
    "mk_d20": "log(20 分前 / 10 分前)",
    "mk_d30": "log(30 分前 / 10 分前)",
    "mk_d60": "log(60 分前 / 10 分前)",
    "mk_dfirst": "log(その馬の最初の中間オッズ / 10 分前)",
    "mk_dprob30": "log(30 分前の比例正規化確率 / 10 分前の比例正規化確率)（全体の動きを除いた相対的な動き）",
    "mk_dprob_first": "log(最初の比例正規化確率 / 10 分前)",
    "mk_logpool": "10 分前の単勝票数合計の対数（レース単位）",
    "mk_pool_growth": "log(10 分前の単勝票数 / 30 分前)（レース単位）",
    "mk_place_win_pool": "log(複勝票数 / 単勝票数)（10 分前、レース単位）",
    "mk_mins": "10 分前のスナップショットの、発走までの分（情報の新しさ）",
    "mk_pl_min_rel": "log(複勝下限オッズ) − log(単勝オッズ)（10 分前）",
    "mk_pl_max_rel": "log(複勝上限オッズ) − log(単勝オッズ)",
    "mk_pl_vs_win": "log(複勝から作った確率 / 単勝の比例正規化確率)",
    "mk_q_vs_win": "log(馬連から作った周辺確率 / 単勝の比例正規化確率)（10 分前）",
    "mk_overround": "10 分前の単勝の Σ1/odds（レース単位）",
}


def _derived(data_dir: Path) -> Path:
    d = data_dir / "derived"
    d.mkdir(parents=True, exist_ok=True)
    return d


def snapshots(data_dir: Path = DATA_DIR) -> pl.DataFrame:
    """列: race_key, umaban, <col>_<tag>（tag は 10・15・20・30・60・first）, mins_10。"""
    post = pl.scan_parquet(data_dir / "races.parquet").select("race_key", "post_at")
    parts = []
    for ydir in sorted((data_dir / "odds_ts_win").glob("year=*")):
        lf = (pl.scan_parquet(ydir / "*.parquet")
              .filter(pl.col("data_kubun") == INTERMEDIATE)
              .select("race_key", "umaban", "announced_at", "win_status", *COLS)
              .join(post, on="race_key", how="inner")
              # 決定時刻より後の発表はここで捨てる（以後はこれより前だけを見る）
              .filter(pl.col("announced_at") <= pl.col("post_at") - pl.duration(minutes=DECISION_MIN)))
        x = lf.collect()
        times = x.group_by("race_key").agg(
            pl.col("post_at").first(),
            **{f"t_{n}": pl.col("announced_at").filter(
                pl.col("announced_at") <= pl.col("post_at") - pl.duration(minutes=n)).max() for n in SNAPS})
        base = None
        for tag in map(str, SNAPS):
            s = (x.join(times.select("race_key", t=pl.col(f"t_{tag}")), on="race_key")
                 .filter(pl.col("announced_at") == pl.col("t"))
                 .select("race_key", "umaban",
                         *[pl.when(pl.col("win_status") == "ok").then(pl.col(c)).otherwise(None).alias(f"{c}_{tag}")
                           if c == "win_odds" else pl.col(c).alias(f"{c}_{tag}") for c in COLS],
                         *([((pl.col("post_at") - pl.col("announced_at")).dt.total_seconds() / 60).alias("mins_10")]
                           if tag == "10" else [])))
            base = s if base is None else base.join(s, on=["race_key", "umaban"], how="left")
        # 最初のオッズは馬ごと（発売直後は無投票の馬が多いので、その馬に初めてオッズが付いた発表）
        first = (x.filter(pl.col("win_status") == "ok").sort("announced_at")
                 .group_by("race_key", "umaban").agg(win_odds_first=pl.col("win_odds").first()))
        parts.append(base.join(first, on=["race_key", "umaban"], how="left"))
    df = pl.concat(parts, how="diagonal_relaxed")
    # 年をまたぐ前日発売で同じレースが 2 年に出ることがある: 10 分前の時刻が後のものを残す
    return df.unique(subset=["race_key", "umaban"], keep="last").sort("race_key", "umaban")


def quinella_marginal(data_dir: Path = DATA_DIR) -> pl.DataFrame:
    """10 分前の馬連オッズ: q_ij ∝ 1/o_ij をレースで正規化し、各馬の周辺 Σ_j q_ij / 2（合計 1）。"""
    q = (pl.scan_parquet(data_dir / "odds_ts_quinella_snap" / "**" / "*.parquet", hive_partitioning=True)
         .filter((pl.col("snap") == str(DECISION_MIN)) & (pl.col("status") == "ok") & (pl.col("odds") > 0))
         .select("race_key", "a", "b", w=1.0 / pl.col("odds")).collect())
    long = pl.concat([q.select("race_key", umaban=pl.col("a").cast(pl.Int16), w="w"),
                      q.select("race_key", umaban=pl.col("b").cast(pl.Int16), w="w")])
    m = long.group_by("race_key", "umaban").agg(pl.col("w").sum())
    return m.with_columns(p_q=pl.col("w") / pl.col("w").sum().over("race_key")).select("race_key", "umaban", "p_q")


def build(snap: pl.DataFrame, qm: pl.DataFrame) -> pl.DataFrame:
    lo = lambda c: pl.col(c).log()  # noqa: E731
    d = snap.join(qm, on=["race_key", "umaban"], how="left")
    inv = lambda tag: 1.0 / pl.col(f"win_odds_{tag}")  # noqa: E731
    d = d.with_columns(
        **{f"_pp_{t}": inv(t) / inv(t).sum().over("race_key") for t in ("10", "30", "first")},
        _pl_mid=1.0 / ((pl.col("place_odds_min_10") + pl.col("place_odds_max_10")) / 2),
    )
    d = d.with_columns(_pl_p=pl.col("_pl_mid") / pl.col("_pl_mid").sum().over("race_key"))
    n = pl.len().over("race_key")
    out = d.select(
        "race_key", "umaban",
        mk_logodds=lo("win_odds_10"),
        mk_rank=pl.col("win_odds_10").rank("min").over("race_key").cast(pl.Float64),
        mk_rank_frac=pl.col("win_odds_10").rank("min").over("race_key").cast(pl.Float64) / n,
        **{f"mk_d{t}": lo(f"win_odds_{t}") - lo("win_odds_10") for t in ("15", "20", "30", "60")},
        mk_dfirst=lo("win_odds_first") - lo("win_odds_10"),
        mk_dprob30=lo("_pp_30") - lo("_pp_10"),
        mk_dprob_first=lo("_pp_first") - lo("_pp_10"),
        mk_logpool=lo("win_vote_total_10"),
        mk_pool_growth=lo("win_vote_total_10") - lo("win_vote_total_30"),
        mk_place_win_pool=lo("place_vote_total_10") - lo("win_vote_total_10"),
        mk_mins=pl.col("mins_10"),
        mk_pl_min_rel=lo("place_odds_min_10") - lo("win_odds_10"),
        mk_pl_max_rel=lo("place_odds_max_10") - lo("win_odds_10"),
        mk_pl_vs_win=lo("_pl_p") - lo("_pp_10"),
        mk_q_vs_win=lo("p_q") - lo("_pp_10"),
        mk_overround=inv("10").sum().over("race_key"),
    )
    return out.with_columns([pl.when(pl.col(c).is_finite()).then(pl.col(c)).otherwise(None).alias(c)
                             for c in FEATURES])


def load_market_features(data_dir: Path = DATA_DIR, refresh: bool = False) -> pl.DataFrame:
    data_dir = Path(data_dir)
    out = _derived(data_dir) / f"{VERSION}.parquet"
    srcs = [data_dir / "races.parquet", *(data_dir / "odds_ts_win").glob("year=*/*.parquet"),
            *(data_dir / "odds_ts_quinella_snap").glob("year=*/*.parquet")]
    if not refresh and out.exists() and out.stat().st_mtime >= max(p.stat().st_mtime for p in srcs):
        return pl.read_parquet(out)
    df = build(snapshots(data_dir), quinella_marginal(data_dir))
    df.write_parquet(out)
    return df


def _check_finite(df: pl.DataFrame) -> dict:
    return {c: float(np.mean(df[c].is_null().to_numpy())) for c in FEATURES}

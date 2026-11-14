"""過去のレースでの「市場の外れ方」の特徴量 history_v2（ADR 0005 の探索）。1 行 = 1 レースの 1 出走馬。

市場オフセットのモデルは「10 分前の市場がどれだけ外れるか」を学ぶので、過去に同じ種類の外れ方をしたかを直接入れる。
過去のレースの確定オッズ・着順は、そのレースの後には公開情報なので、**レース日より厳密に前の日**の分だけ使う。

- 馬: 前走・直近 3 走の確定単勝オッズの対数と人気、「人気から見た着順のよさ」（(人気−1)/(n−1) − (着順−1)/(n−1)）。
- 騎手・調教師・父・馬: 前日までの「勝ち − 確定オッズの比例正規化確率」の累積（全期間と直近 365 日）を、
  出走数で縮小した値（Σ残差 / (n + k)）。正なら市場がその騎手などを過小評価してきた。
"""

from __future__ import annotations

import json
from pathlib import Path

import polars as pl

from keiba_ai.features import DATA_DIR

VERSION = "history_v2"
SHRINK = 50.0
WINDOW_DAYS = 365
NOT_STARTED = (1, 2, 3)

ENTITIES = {"jk": "jockey_code", "tr": "trainer_code", "sire": "sire_id", "hh": "horse_id"}
FEATURES: dict[str, str] = {
    "h2_prev_logodds_1": "前走の確定単勝オッズの対数",
    "h2_prev_pop_1": "前走の単勝人気 / 頭数",
    "h2_prev_logodds_mean3": "直近 3 走の確定単勝オッズの対数の平均",
    "h2_beat_pop_1": "前走の（人気の位置 − 着順の位置）。正なら人気より上の着順",
    "h2_beat_pop_mean3": "直近 3 走の平均",
    "h2_beat_pop_mean10": "直近 10 走の平均",
    **{f"{p}_mresid": f"{lab}: 前日までの（勝ち − 市場確率）の累積 / (n + {SHRINK:g})"
       for p, lab in (("jk", "騎手"), ("tr", "調教師"), ("sire", "父"), ("hh", "馬"))},
    **{f"{p}_mresid_1y": f"{lab}: 直近 {WINDOW_DAYS} 日の同じ値"
       for p, lab in (("jk", "騎手"), ("tr", "調教師"), ("sire", "父"))},
    "jk_mresid_pop": "騎手: 前日までの（人気の位置 − 着順の位置）の累積 / (n + k)",
}


def base(data_dir: Path = DATA_DIR) -> pl.DataFrame:
    races = pl.read_parquet(data_dir / "races.parquet", columns=["race_key", "date", "is_cancelled"]).filter(
        ~pl.col("is_cancelled")).drop("is_cancelled")
    ent = pl.read_parquet(data_dir / "entries.parquet",
                          columns=["race_key", "umaban", "horse_id", "jockey_code", "trainer_code", "abnormal_code",
                                   "finish_pos", "win_odds", "win_pop"])
    horses = pl.read_parquet(data_dir / "horses.parquet", columns=["horse_id", "sire_id"])
    d = (ent.filter(~pl.col("abnormal_code").is_in(NOT_STARTED) & pl.col("umaban").is_not_null())
         .join(races, on="race_key", how="inner").join(horses, on="horse_id", how="left"))
    n = pl.len().over("race_key").cast(pl.Float64)
    inv = pl.when(pl.col("win_odds") > 0).then(1.0 / pl.col("win_odds"))
    d = d.with_columns(
        n=n,
        y=(pl.col("finish_pos") == 1).fill_null(False).cast(pl.Float64),
        p_fin=inv / inv.sum().over("race_key"),
        pos_n=pl.when(n > 1).then(((pl.col("finish_pos").fill_null(n) - 1) / (n - 1)).clip(0, 1)),
        pop_n=pl.when(n > 1).then(((pl.col("win_pop") - 1) / (n - 1)).clip(0, 1)),
    )
    return d.with_columns(resid=pl.col("y") - pl.col("p_fin"), beat_pop=pl.col("pop_n") - pl.col("pos_n"))


def _horse_lags(d: pl.DataFrame) -> pl.DataFrame:
    """馬ごとに日付順に並べ、前走以前（shift(1) 以降）だけから作る。"""
    h = d.sort("horse_id", "date").with_columns(
        _lo=pl.col("win_odds").log(),
    )
    g = pl.col("horse_id")
    return h.select(
        "race_key", "umaban",
        h2_prev_logodds_1=pl.col("_lo").shift(1).over(g),
        h2_prev_pop_1=pl.col("pop_n").shift(1).over(g),
        h2_prev_logodds_mean3=pl.col("_lo").shift(1).rolling_mean(3, min_samples=1).over(g),
        h2_beat_pop_1=pl.col("beat_pop").shift(1).over(g),
        h2_beat_pop_mean3=pl.col("beat_pop").shift(1).rolling_mean(3, min_samples=1).over(g),
        h2_beat_pop_mean10=pl.col("beat_pop").shift(1).rolling_mean(10, min_samples=1).over(g),
    )


def _entity_prior(d: pl.DataFrame, key: str, prefix: str, value: str = "resid", out: str | None = None,
                  window: int | None = None) -> pl.DataFrame:
    """(key, date) ごとに前日までの Σvalue と件数（全期間、または直近 window 日）。同じ日の分は含めない。"""
    out = out or f"{prefix}_mresid" + ("_1y" if window else "")
    daily = (d.drop_nulls([key, value]).group_by(key, "date").agg(s=pl.col(value).sum(), c=pl.len())
             .sort(key, "date")
             .with_columns(cs=pl.col("s").cum_sum().over(key), cc=pl.col("c").cum_sum().over(key)))
    # 前日までの累積 = 当日までの累積 − 当日分
    daily = daily.with_columns(ps=pl.col("cs") - pl.col("s"), pc=pl.col("cc") - pl.col("c"))
    if window:
        lag = daily.select(key, date=pl.col("date") + pl.duration(days=window), ls="cs", lc="cc").sort(key, "date")
        # date − window 日「以前」の最後の累積（その日を含む）を引く → (date − window, date) の開区間 … 前日まで
        daily = daily.sort("date").join_asof(lag.sort("date"), on="date", by=key, strategy="backward", check_sortedness=False)
        daily = daily.with_columns(ps=pl.col("ps") - pl.col("ls").fill_null(0), pc=pl.col("pc") - pl.col("lc").fill_null(0))
    daily = daily.with_columns((pl.col("ps") / (pl.col("pc") + SHRINK)).alias(out))
    return d.select("race_key", "umaban", key, "date").join(daily.select(key, "date", out), on=[key, "date"],
                                                            how="left").select("race_key", "umaban", out)


def build(d: pl.DataFrame) -> pl.DataFrame:
    out = _horse_lags(d)
    for p, key in ENTITIES.items():
        out = out.join(_entity_prior(d, key, p), on=["race_key", "umaban"], how="left")
        if p != "hh":
            out = out.join(_entity_prior(d, key, p, window=WINDOW_DAYS), on=["race_key", "umaban"], how="left")
    out = out.join(_entity_prior(d, "jockey_code", "jk", value="beat_pop", out="jk_mresid_pop"),
                   on=["race_key", "umaban"], how="left")
    return out.select("race_key", "umaban", *FEATURES)


def load_hist2(data_dir: Path = DATA_DIR, refresh: bool = False) -> pl.DataFrame:
    path = data_dir / "derived" / f"{VERSION}.parquet"
    srcs = [data_dir / f"{t}.parquet" for t in ("races", "entries", "horses")]
    if not refresh and path.exists() and path.stat().st_mtime >= max(p.stat().st_mtime for p in srcs):
        return pl.read_parquet(path)
    df = build(base(data_dir))
    df.write_parquet(path)
    path.with_suffix(".json").write_text(json.dumps({"features": FEATURES}, ensure_ascii=False, indent=1))
    return df

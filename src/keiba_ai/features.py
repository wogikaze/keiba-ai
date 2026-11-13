"""オッズを使わない特徴量（features_v1）。1 行 = 1 レースの 1 出走馬（race_key, umaban）。

入力は ``data/processed/jra-van/`` の races・entries・horses・training_slope・training_wood。
**オッズ・人気は一切使わない**（市場の情報は後の段で別に足す）。

## 情報の使える時点（各特徴量の ``availability``）

- ``race_card``: 出馬表の確定時（レース前日まで）に分かる。競走条件・距離・枠番・馬番・負担重量・騎手など。
- ``race_day``: レース当日の発走前に発表される。馬場状態・天候・馬体重と増減・出走頭数（取消・除外の反映後）。
- ``history``: **レース日より厳密に前の日**のレース結果・調教だけから作る。同じ日の他のレースの結果も使わない。

## リークを避ける仕組み

- 過去成績は「馬 × 日付」で一意（同じ日に 2 回走る馬はいない、を確かめる）なので、
  馬ごとに日付順に並べて ``shift(1)`` 以降だけを使う。
- 騎手・調教師・種牡馬の率、スピード指数の基準（コース × 距離 × 馬場の平均・標準偏差）は、
  日ごとに集計してから累積し、**その日の分を引いた**値（前日までの累積）を使う。直近 N 日の率は
  ``closed="left"`` の窓（その日を含まない）。
- 調教は ``train_date <= レース日 − 1`` の最新の 1 本と、その前 ``training_window_days`` 日の本数。
- 結果の列（着順・タイム・上がり・着差・通過順・賞金・異常区分 4〜7）は過去の行の値としてだけ読む。
- ``tests/test_features.py`` が、ある日 D 以降のデータを消し・D 当日の結果を壊しても、D 以前の行の
  特徴量が変わらないことを合成データで確かめる。

対象（universe）: JRA、中止でないレース、``min_year`` 以降、出走した馬（異常区分 1 出走取消・
2 発走除外・3 競走除外を除く。4 競走中止〜7 降着は出走扱い）。
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path

import polars as pl

FEATURES_VERSION = "features_v1"

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "processed" / "jra-van"
CACHE_PATH = DATA_DIR / "derived" / f"{FEATURES_VERSION}.parquet"


@dataclass(frozen=True)
class FeatureConfig:
    min_year: int = 1986                 # これより前のレースは出走馬が欠けている（docs/data/processed.md）
    not_started_codes: tuple = (1, 2, 3)  # 出走取消・発走除外・競走除外
    n_last: int = 5                      # 直近何走の着順を並べるか
    n_recent_mean: int = 3               # スピード指数などの直近平均の走数
    rate_prior_strength: float = 20.0    # 騎手・調教師・種牡馬の率の縮小（仮想的な出走数）
    recent_days: int = 365               # 直近の率の窓（日）
    speed_min_n: int = 30                # スピード指数の基準に要る過去の完走頭数
    behind_clip: tuple = (-2.0, 10.0)    # 着差（秒 / 1000m）の切り詰め
    fig_clip: tuple = (-10.0, 10.0)      # スピード指数・上がり指数の切り詰め（SD 単位）
    training_window_days: int = 14       # 調教を見る日数（レース前日から遡る）

    @classmethod
    def from_dict(cls, d: dict | None) -> "FeatureConfig":
        d = dict(d or {})
        names = {f.name for f in fields(cls)}
        unknown = set(d) - names
        if unknown:
            raise ValueError(f"unknown feature config keys: {sorted(unknown)}")
        for k in ("not_started_codes", "behind_clip", "fig_clip"):
            if k in d:
                d[k] = tuple(d[k])
        return cls(**d)


# 特徴量の一覧: 名前 -> (availability, 説明)
FEATURES: dict[str, tuple[str, str]] = {
    # レース条件
    "venue_code": ("race_card", "競馬場"),
    "surface": ("race_card", "芝・ダート・障害"),
    "track_code": ("race_card", "トラックコード（内外・回り）"),
    "distance": ("race_card", "距離 m"),
    "grade_code": ("race_card", "グレード"),
    "class_level": ("race_card", "最若年条件の賞金条件（万円、新馬・未勝利 0、オープン 9999）"),
    "race_type_code": ("race_card", "競走種別（年齢条件）"),
    "race_symbol_code": ("race_card", "競走記号（性・混合などの条件）"),
    "weight_type_code": ("race_card", "重量種別（ハンデ・定量など）"),
    "prize_1st_log": ("race_card", "1 着本賞金の log1p"),
    "month": ("race_card", "開催月"),
    "going_code": ("race_day", "馬場状態"),
    "weather_code": ("race_day", "天候"),
    "n_runners": ("race_day", "出走頭数（取消・除外の後）"),
    # 馬（当日まで）
    "age": ("race_card", "馬齢"),
    "sex_code": ("race_card", "性別"),
    "belong_code": ("race_card", "東西所属"),
    "weight_carried": ("race_card", "負担重量"),
    "weight_carried_rel": ("race_card", "負担重量 − レース平均"),
    "umaban": ("race_card", "馬番"),
    "wakuban": ("race_card", "枠番"),
    "umaban_rel": ("race_day", "馬番 / 出走頭数"),
    "blinker": ("race_card", "ブリンカー"),
    "apprentice_code": ("race_card", "騎手見習コード（減量）"),
    "horse_weight": ("race_day", "馬体重"),
    "weight_diff": ("race_day", "馬体重の増減"),
    # 馬の過去成績
    "h_n_runs": ("history", "過去の出走数"),
    "h_days_since": ("history", "前走からの日数"),
    **{f"h_pos_{k}": ("history", f"{k} 走前の着順（(着順−1)/(頭数−1)、中止・失格は 1）") for k in range(1, 6)},
    "h_pos_mean5": ("history", "直近 5 走の正規化着順の平均"),
    "h_win_rate": ("history", "過去の勝率"),
    "h_top3_rate": ("history", "過去の 3 着内率"),
    "h_fig_1": ("history", "前走のスピード指数（(基準平均−タイム)/基準 SD）"),
    "h_fig_mean3": ("history", "直近 3 走のスピード指数の平均"),
    "h_fig_max5": ("history", "直近 5 走のスピード指数の最大"),
    "h_l3f_1": ("history", "前走の上がり 3F 指数"),
    "h_l3f_mean3": ("history", "直近 3 走の上がり 3F 指数の平均"),
    "h_behind_1": ("history", "前走の着差（秒 / 1000m）"),
    "h_behind_mean3": ("history", "直近 3 走の着差の平均"),
    "h_corner4_mean3": ("history", "直近 3 走の 4 角位置（順位 / 頭数）の平均"),
    "h_prize_log": ("history", "過去の獲得本賞金合計の log1p"),
    "h_dist_change": ("history", "距離 − 前走距離"),
    "h_surface_change": ("history", "前走と馬場（芝・ダ・障）が違う"),
    "h_same_surface_runs": ("history", "同じ馬場での過去の出走数"),
    "h_same_surface_top3_rate": ("history", "同じ馬場での 3 着内率"),
    "h_class_change": ("history", "log(1 着賞金) − 前走の log(1 着賞金)"),
    "h_wc_change": ("history", "負担重量 − 前走の負担重量"),
    "h_jockey_change": ("history", "前走と騎手が違う"),
    # 騎手・調教師・種牡馬（前日までの累積）
    **{f"{p}_{s}": ("history", f"{lab}の{desc}")
       for p, lab in (("jk", "騎手"), ("tr", "調教師"), ("sire", "父"))
       for s, desc in (("n_log", "過去の騎乗・出走数の log1p"), ("win_rate", "勝率（縮小）"),
                       ("top3_rate", "3 着内率（縮小）"), ("win_rate_1y", "直近 1 年の勝率（縮小）"),
                       ("top3_rate_1y", "直近 1 年の 3 着内率（縮小）"))},
    # 調教
    "ts_last_4f": ("history", "直近の坂路 4F 合計（14 日以内）"),
    "ts_last_1f": ("history", "直近の坂路のラスト 1F"),
    "ts_days_before": ("history", "直近の坂路が何日前か"),
    "ts_n": ("history", "14 日以内の坂路の本数"),
    "tw_last_3f": ("history", "直近のウッド 3F 合計（14 日以内）"),
    "tw_last_1f": ("history", "直近のウッドのラスト 1F"),
    "tw_days_before": ("history", "直近のウッドが何日前か"),
    "tw_n": ("history", "14 日以内のウッドの本数"),
    # レース内の相対値（同じレースの出走馬の、上の特徴量だけから作る）
    **{f"{c}_z": ("history", f"{c} のレース内 z 値")
       for c in ("h_fig_mean3", "h_fig_max5", "h_pos_mean5", "h_l3f_mean3", "jk_win_rate", "h_prize_log")},
}

CATEGORICAL = ["venue_code", "surface", "track_code", "grade_code", "race_type_code", "race_symbol_code",
               "weight_type_code", "going_code", "weather_code", "sex_code", "belong_code",
               "apprentice_code"]

KEY_COLS = ["race_key", "umaban", "date", "horse_id"]
LABEL_COLS = ["finish_pos", "y_win", "y_top3"]


# --- 部品 ------------------------------------------------------------------

def _class_level(code: pl.Expr) -> pl.Expr:
    """競走条件コード（コード表 2007）を賞金条件の数値に。701〜703（新馬・未出走・未勝利）は 0、
    999（オープン）は 9999、001〜100 は賞金条件（百万円単位の数字のまま）。"""
    v = code.cast(pl.Int32, strict=False)
    return (pl.when(v.is_between(701, 799)).then(0)
            .when(v == 999).then(9999)
            .when(v.is_between(1, 698)).then(v)
            .otherwise(None)).cast(pl.Float64)


def base_frame(races: pl.DataFrame, entries: pl.DataFrame, cfg: FeatureConfig) -> pl.DataFrame:
    """対象の出走馬（全期間）。過去成績の母集団もこれ。"""
    r = races.filter(~pl.col("is_cancelled") & (pl.col("date").dt.year() >= cfg.min_year)).select(
        "race_key", "date", "venue_code", "surface", "track_code", "distance", "grade_code",
        "race_type_code", "race_symbol_code", "weight_type_code", "going_code", "weather_code",
        "prize_1st", "cond_youngest")
    e = entries.select(
        "race_key", "umaban", "wakuban", "horse_id", "sex_code", "age", "belong_code", "trainer_code",
        "weight_carried", "blinker", "jockey_code", "apprentice_code", "horse_weight", "weight_diff",
        "abnormal_code", "finish_pos", "time_sec", "last_3f", "time_diff", "corner4", "prize")
    x = (e.join(r, on="race_key", how="inner")
         .filter(~pl.col("abnormal_code").is_in(list(cfg.not_started_codes)))
         .filter(pl.col("umaban").is_not_null()))
    x = x.with_columns(
        n_runners=pl.len().over("race_key").cast(pl.Int32),
        y_win=(pl.col("finish_pos") == 1).fill_null(False).cast(pl.Int8),
        y_top3=(pl.col("finish_pos") <= 3).fill_null(False).cast(pl.Int8),
        class_level=_class_level(pl.col("cond_youngest")),
        prize_1st_log=pl.col("prize_1st").cast(pl.Float64).log1p(),
        month=pl.col("date").dt.month().cast(pl.Int8),
    )
    dup = x.group_by("horse_id", "date").len().filter(pl.col("len") > 1).height
    if dup:
        raise ValueError(f"同じ日に 2 回以上出走した馬がある（{dup} 件）。shift(1) の前提が崩れる")
    return x


def _prior_daily(df: pl.DataFrame, key: list[str], aggs: dict[str, pl.Expr]) -> pl.DataFrame:
    """key × date で集計し、前日までの累積（その日の分を除く）を付ける。列名は prior_<名>。"""
    daily = df.group_by([*key, "date"]).agg(**aggs).sort([*key, "date"])
    over = key if key else None
    exprs = []
    for name in aggs:
        cum = pl.col(name).cum_sum()
        cum = cum.over(over) if over else cum
        exprs.append((cum - pl.col(name)).alias(f"prior_{name}"))
    return daily.with_columns(exprs)


def _speed_reference(x: pl.DataFrame, value: str, cfg: FeatureConfig) -> pl.DataFrame:
    """コース × 距離 × 馬場状態ごとの、前日までの value の平均と SD。"""
    key = ["venue_code", "surface", "distance", "going_code"]
    ok = x.filter((pl.col("abnormal_code") == 0) & pl.col(value).is_not_null())
    d = _prior_daily(ok, key, {"n": pl.len().cast(pl.Float64), "s": pl.col(value).sum(),
                               "s2": (pl.col(value) ** 2).sum()})
    mean = pl.col("prior_s") / pl.col("prior_n")
    var = pl.col("prior_s2") / pl.col("prior_n") - mean ** 2
    return d.select(*key, "date",
                    pl.when(pl.col("prior_n") >= cfg.speed_min_n).then(mean).alias(f"ref_{value}_mean"),
                    pl.when(pl.col("prior_n") >= cfg.speed_min_n).then(var.clip(1e-6).sqrt())
                    .alias(f"ref_{value}_sd"))


def _entity_rates(x: pl.DataFrame, key: str, prefix: str, cfg: FeatureConfig) -> pl.DataFrame:
    """騎手・調教師・父の、前日までの勝率・3 着内率（全体の前日までの率に向けて縮小）。"""
    g = _prior_daily(x, [], {"n": pl.len().cast(pl.Float64), "w": pl.col("y_win").cast(pl.Float64).sum(),
                             "t": pl.col("y_top3").cast(pl.Float64).sum()})
    g = g.select("date", p0w=pl.col("prior_w") / pl.col("prior_n"), p0t=pl.col("prior_t") / pl.col("prior_n"))
    sub = x.filter(pl.col(key).is_not_null())
    aggs = {"n": pl.len().cast(pl.Float64), "w": pl.col("y_win").cast(pl.Float64).sum(),
            "t": pl.col("y_top3").cast(pl.Float64).sum()}
    d = _prior_daily(sub, [key], aggs)
    roll = (d.select(key, "date", "n", "w", "t")
            .rolling(index_column="date", period=f"{cfg.recent_days}d", closed="left", group_by=key)
            .agg(rn=pl.col("n").sum(), rw=pl.col("w").sum(), rt=pl.col("t").sum()))
    d = d.join(roll, on=[key, "date"], how="left").join(g, on="date", how="left")
    k = cfg.rate_prior_strength

    def shrink(num, den, p0):
        return (pl.col(num).fill_null(0) + k * pl.col(p0)) / (pl.col(den).fill_null(0) + k)

    return d.select(
        key, "date",
        pl.col("prior_n").log1p().alias(f"{prefix}_n_log"),
        shrink("prior_w", "prior_n", "p0w").alias(f"{prefix}_win_rate"),
        shrink("prior_t", "prior_n", "p0t").alias(f"{prefix}_top3_rate"),
        shrink("rw", "rn", "p0w").alias(f"{prefix}_win_rate_1y"),
        shrink("rt", "rn", "p0t").alias(f"{prefix}_top3_rate_1y"),
    )


def _training(targets: pl.DataFrame, tr: pl.DataFrame, cols: dict[str, str], prefix: str,
              cfg: FeatureConfig) -> pl.DataFrame:
    """レース前日までの最新の調教 1 本（window 日以内）と、window 日の本数。

    cols: 出力名の接尾辞 -> 調教テーブルの列名。
    """
    w = cfg.training_window_days
    t = (tr.filter(pl.col("horse_id").is_not_null() & pl.col("train_date").is_not_null())
         .select("horse_id", "train_date", "train_time", *cols.values())
         .sort("horse_id", "train_date", "train_time", maintain_order=True)
         .with_columns(_cnt=pl.int_range(1, pl.len() + 1).over("horse_id"))
         # 同じ日の複数本は最後（時刻の遅い方）の 1 本に。_cnt はその日までの累計本数になる
         .unique(subset=["horse_id", "train_date"], keep="last", maintain_order=True)
         .sort("train_date"))
    q = (targets.select("horse_id", "date").unique()
         .with_columns(_hi=pl.col("date") - pl.duration(days=1), _lo=pl.col("date") - pl.duration(days=w + 1))
         .sort("_hi"))
    hi = q.join_asof(t, left_on="_hi", right_on="train_date", by="horse_id", strategy="backward",
                     check_sortedness=False)
    lo = (q.sort("_lo").join_asof(t.select("horse_id", "train_date", pl.col("_cnt").alias("_cnt_lo")),
                                  left_on="_lo", right_on="train_date", by="horse_id", strategy="backward",
                     check_sortedness=False)
          .select("horse_id", "date", "_cnt_lo"))
    out = hi.join(lo, on=["horse_id", "date"], how="left")
    days = (pl.col("date") - pl.col("train_date")).dt.total_days()
    recent = days <= w
    return out.select(
        "horse_id", "date",
        *[pl.when(recent).then(pl.col(src)).alias(f"{prefix}_{name}") for name, src in cols.items()],
        pl.when(recent).then(days).cast(pl.Float64).alias(f"{prefix}_days_before"),
        (pl.col("_cnt").fill_null(0) - pl.col("_cnt_lo").fill_null(0)).cast(pl.Float64).alias(f"{prefix}_n"),
    )


# --- 本体 ------------------------------------------------------------------

def build_features(races: pl.DataFrame, entries: pl.DataFrame, horses: pl.DataFrame | None = None,
                   training_slope: pl.DataFrame | None = None, training_wood: pl.DataFrame | None = None,
                   cfg: FeatureConfig = FeatureConfig()) -> pl.DataFrame:
    """特徴量の表を作る。返り値は KEY_COLS + LABEL_COLS + FEATURES の列。"""
    x = base_frame(races, entries, cfg)

    # 過去の 1 走ごとの値（結果を使う。過去の行としてだけ読む）
    for v in ("time_sec", "last_3f"):
        ref = _speed_reference(x, v, cfg)
        x = x.join(ref, on=["venue_code", "surface", "distance", "going_code", "date"], how="left")
    lo, hi = cfg.behind_clip
    flo, fhi = cfg.fig_clip
    x = x.with_columns(
        _pos=pl.when(pl.col("finish_pos").is_null()).then(1.0)
        .when(pl.col("n_runners") > 1).then((pl.col("finish_pos") - 1) / (pl.col("n_runners") - 1))
        .otherwise(0.0),
        _fig=((pl.col("ref_time_sec_mean") - pl.col("time_sec")) / pl.col("ref_time_sec_sd")).clip(flo, fhi),
        _l3f=((pl.col("ref_last_3f_mean") - pl.col("last_3f")) / pl.col("ref_last_3f_sd")).clip(flo, fhi),
        _behind=pl.when(pl.col("finish_pos").is_not_null())
        .then((pl.col("time_diff") / pl.col("distance") * 1000).clip(lo, hi)),
        _c4=pl.col("corner4") / pl.col("n_runners"),
        _prize=pl.col("prize").fill_null(0).cast(pl.Float64),
    )

    # 馬ごとの過去成績（日付順に並べて shift(1) 以降）
    x = x.sort("horse_id", "date")
    H = "horse_id"

    def lag(c, k=1):
        return pl.col(c).shift(k).over(H)

    nl, nm = cfg.n_last, cfg.n_recent_mean
    surf_cnt = pl.int_range(pl.len()).over([H, "surface"])  # 同じ馬場での過去の出走数
    x = x.with_columns(
        h_n_runs=pl.int_range(pl.len()).over(H).cast(pl.Float64),
        h_days_since=(pl.col("date") - lag("date")).dt.total_days().cast(pl.Float64),
        **{f"h_pos_{k}": lag("_pos", k) for k in range(1, nl + 1)},
        h_pos_mean5=pl.mean_horizontal([lag("_pos", k) for k in range(1, nl + 1)]),
        _cw=(pl.col("y_win").cast(pl.Float64).cum_sum() - pl.col("y_win")).over(H),
        _ct=(pl.col("y_top3").cast(pl.Float64).cum_sum() - pl.col("y_top3")).over(H),
        h_fig_1=lag("_fig"),
        h_fig_mean3=pl.mean_horizontal([lag("_fig", k) for k in range(1, nm + 1)]),
        h_fig_max5=pl.max_horizontal([lag("_fig", k) for k in range(1, nl + 1)]),
        h_l3f_1=lag("_l3f"),
        h_l3f_mean3=pl.mean_horizontal([lag("_l3f", k) for k in range(1, nm + 1)]),
        h_behind_1=lag("_behind"),
        h_behind_mean3=pl.mean_horizontal([lag("_behind", k) for k in range(1, nm + 1)]),
        h_corner4_mean3=pl.mean_horizontal([lag("_c4", k) for k in range(1, nm + 1)]),
        h_prize_log=(pl.col("_prize").cum_sum() - pl.col("_prize")).over(H).log1p(),
        h_dist_change=(pl.col("distance") - lag("distance")).cast(pl.Float64),
        h_surface_change=pl.when(lag("surface").is_not_null())
        .then((pl.col("surface") != lag("surface")).cast(pl.Float64)),
        h_same_surface_runs=surf_cnt.cast(pl.Float64),
        _cst=(pl.col("y_top3").cast(pl.Float64).cum_sum() - pl.col("y_top3")).over([H, "surface"]),
        h_class_change=pl.col("prize_1st_log") - lag("prize_1st_log"),
        h_wc_change=pl.col("weight_carried") - lag("weight_carried"),
        h_jockey_change=pl.when(lag("jockey_code").is_not_null())
        .then((pl.col("jockey_code") != lag("jockey_code")).cast(pl.Float64)),
    )
    x = x.with_columns(
        h_win_rate=pl.when(pl.col("h_n_runs") > 0).then(pl.col("_cw") / pl.col("h_n_runs")),
        h_top3_rate=pl.when(pl.col("h_n_runs") > 0).then(pl.col("_ct") / pl.col("h_n_runs")),
        h_same_surface_top3_rate=pl.when(pl.col("h_same_surface_runs") > 0)
        .then(pl.col("_cst") / pl.col("h_same_surface_runs")),
    )

    # 騎手・調教師・父
    x = x.join(_entity_rates(x, "jockey_code", "jk", cfg), on=["jockey_code", "date"], how="left")
    x = x.join(_entity_rates(x, "trainer_code", "tr", cfg), on=["trainer_code", "date"], how="left")
    if horses is not None:
        x = x.join(horses.select("horse_id", "sire_id").unique("horse_id"), on="horse_id", how="left")
    else:
        x = x.with_columns(sire_id=pl.lit(None, pl.String))
    x = x.join(_entity_rates(x, "sire_id", "sire", cfg), on=["sire_id", "date"], how="left")

    # 調教
    tcols = {"ts": {"last_4f": "total_4f", "last_1f": "lap_200_0"},
             "tw": {"last_3f": "total_3f", "last_1f": "lap_200_0"}}
    for prefix, tr in (("ts", training_slope), ("tw", training_wood)):
        if tr is not None and tr.height:
            x = x.join(_training(x, tr, tcols[prefix], prefix, cfg), on=["horse_id", "date"], how="left")
        else:
            x = x.with_columns(*[pl.lit(None, pl.Float64).alias(f"{prefix}_{n}")
                                 for n in (*tcols[prefix], "days_before", "n")])

    # レース内の相対値
    x = x.with_columns(
        weight_carried_rel=pl.col("weight_carried") - pl.col("weight_carried").mean().over("race_key"),
        umaban_rel=pl.col("umaban") / pl.col("n_runners"),
        **{f"{c}_z": ((pl.col(c) - pl.col(c).mean().over("race_key"))
                      / pl.col(c).std().over("race_key").clip(1e-6))
           for c in ("h_fig_mean3", "h_fig_max5", "h_pos_mean5", "h_l3f_mean3", "jk_win_rate", "h_prize_log")},
    )

    feats = list(FEATURES)
    out = x.select(*KEY_COLS, *LABEL_COLS, *[c for c in feats if c not in KEY_COLS]).sort(
        "date", "race_key", "umaban")
    num = [c for c in feats if c not in CATEGORICAL]
    return out.with_columns(pl.col(num).cast(pl.Float64), pl.col(CATEGORICAL).cast(pl.String))


# --- キャッシュ ------------------------------------------------------------

def _source_fingerprint(data_dir: Path) -> str:
    info = data_dir / "_build_info.json"
    raw = info.read_bytes() if info.exists() else b""
    return hashlib.sha256(raw).hexdigest()[:8]


def data_version(data_dir: Path = DATA_DIR, cfg: FeatureConfig = FeatureConfig()) -> str:
    cfg_hash = hashlib.sha256(json.dumps(asdict(cfg), sort_keys=True).encode()).hexdigest()[:6]
    return f"jra-van@{_source_fingerprint(data_dir)}/{FEATURES_VERSION}-{cfg_hash}"


def load_features(cfg: FeatureConfig = FeatureConfig(), data_dir: Path = DATA_DIR,
                  rebuild: bool = False) -> pl.DataFrame:
    """キャッシュがあり版が同じなら読む。なければ作って保存する。"""
    path = data_dir / "derived" / f"{FEATURES_VERSION}.parquet"
    meta = path.with_suffix(".json")
    ver = data_version(data_dir, cfg)
    if not rebuild and path.exists() and meta.exists() and json.loads(meta.read_text())["version"] == ver:
        return pl.read_parquet(path)
    rd = lambda t: pl.read_parquet(data_dir / f"{t}.parquet")  # noqa: E731
    df = build_features(rd("races"), rd("entries"), rd("horses"), rd("training_slope"), rd("training_wood"),
                        cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)
    meta.write_text(json.dumps({"version": ver, "config": asdict(cfg), "rows": df.height,
                                "features": FEATURES}, ensure_ascii=False, indent=1))
    return df

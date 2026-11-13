"""市場ベースライン: 決定時刻に見えていた単勝オッズと、そこから作る市場確率。

他の実験はこのモジュールを import して市場の参照確率を作る。API は変えない（変えるときは足すだけ）。

    pre_deadline_odds(minutes_before: int | None) -> pl.DataFrame   # 締切前（中間オッズ）
    final_odds() -> pl.DataFrame                                     # 確定オッズ（odds_final, O1）
    race_universe() -> pl.DataFrame                                  # 評価対象の出走馬と目的変数
    market_probs(df, method, k=None) -> 同じ型の df + 列 p_market    # オッズ → 勝率
    fit_power_k(df, y="y") -> float                                  # 全体で 1 つのべき乗 k を最尤で当てはめ

オッズの表の列（1 行 = 1 レース × 1 馬番。キーは ``race_key`` + ``umaban``）:

- ``win_odds``: 単勝オッズ（倍）。``win_status`` が ``ok`` 以外（無投票・取消）は null。
- ``win_status``, ``win_pop``, ``win_vote_total``（その発表時点の単勝票数合計、円）。
- pre_deadline_odds だけ: ``announced_at``（採った発表の時刻）、``minutes_to_post``
  （予定発走時刻 − 発表時刻、分。発走が遅れたレースでは負になりうる）。

決定時刻の定義（docs/data/processed.md の odds_ts_win）:

- ``minutes_before=N``: データ区分 1（中間）の発表のうち ``announced_at <= post_at − N 分`` の
  最後の 1 回（その発表の全馬の行）。``post_at`` は予定の発走時刻で、遅延は入っていない。
  遅延したレースでは実際より早い時点を取るので、リークの側にはずれない。
- ``minutes_before=None``: 発走時刻に関係なく、最後の中間オッズ。2021 年までは発走約 6 分前、
  2023 年以降は約 1 分前、2022 年は混在。発走が遅れたレース（491 レース）では予定時刻より後の
  発表を含む（実際の締切前ではある）。
- 時刻を満たす中間オッズがないレースは行がない（2003-10 より前のレースも行がない）。

結果は ``data/processed/jra-van/derived/market_odds_<N|last|final>.parquet`` にキャッシュする。
元のテーブル（odds_ts_win / races / odds_final）がキャッシュより新しければ作り直す。
odds_ts_win（約 1.5 億行）は年のパーティションごとに遅延評価で読むので、全部をメモリに載せない。

評価対象（race_universe）:

- JRA のレース（processed テーブルはもともと JRA だけ）で、中止（``is_cancelled``）でないもの。
- 出走取消（異常区分 1）・発走除外（2）・競走除外（3）の馬は除く。どれも単勝は返還になり、
  発走していない。残った馬で確率を正規化し直す（オッズを universe に結合してから market_probs を呼ぶ）。
- 競走中止（4）・失格（5）・落馬再騎乗（6）・降着（7）は残す（発走しており、単勝は返還されない）。
  ``y`` = 確定着順が 1（失格は着順なしなので 0、降着は降着後の着順）。同着は y=1 が 2 頭以上になり、
  evaluate.py が的中を等分する。
- 注意: 出走馬だけで正規化し直した確率は「出走馬が決まった条件での勝率」で、確率の評価に使う。
  **購入判断（p·odds）には使わない。** 決定時刻のあとで競走除外になった馬の分だけ Σ1/odds が下がり、
  知り得ない情報で p·odds > 1 の馬ができる。判断には、決定時刻の発表に載っている全馬で
  market_probs を呼んだ確率を使う。
- ``win_payout_odds`` = HR の単勝払戻金 / 100（払い戻された馬だけ、他は null）。賭けのシミュレーションで
  払戻しに使う。払戻確定後の失格で SE の 1 着と HR が違うレース（2 件）は、払戻を正とする。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import polars as pl

if TYPE_CHECKING:
    import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = Path(os.environ.get("KEIBA_PROCESSED_JRAVAN", ROOT / "data/processed/jra-van"))

INTERMEDIATE = "1"          # odds_ts_win の data_kubun: 中間オッズ
SCRATCHED_CODES = (1, 2, 3)  # 出走取消・発走除外・競走除外（単勝は返還）
METHODS = ("proportional", "power", "shin", "goto", "power_fit")
ODDS_COLS = ["race_key", "umaban", "win_odds", "win_status", "win_pop", "win_vote_total"]


# --- キャッシュ ---------------------------------------------------------------

def _derived(data_dir: Path) -> Path:
    d = data_dir / "derived"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _newest_mtime(paths) -> float:
    return max((p.stat().st_mtime for p in paths), default=0.0)


def _cached(path: Path, sources: list[Path], refresh: bool) -> bool:
    return (not refresh) and path.exists() and path.stat().st_mtime >= _newest_mtime(sources)


def _tag(minutes_before: int | None) -> str:
    return "last" if minutes_before is None else str(int(minutes_before))


# --- オッズ -------------------------------------------------------------------

def pre_deadline_odds(minutes_before: int | None, *, data_dir: Path | None = None,
                      refresh: bool = False) -> pl.DataFrame:
    """発走 N 分前（None なら最後）の中間オッズの発表 1 回分を、レース × 馬番で返す。

    列: race_key, umaban, win_odds, win_status, win_pop, win_vote_total, announced_at, minutes_to_post。
    """
    if minutes_before is not None and minutes_before < 0:
        raise ValueError("minutes_before は 0 以上か None")
    data_dir = Path(data_dir or DATA_DIR)
    ts_dir = data_dir / "odds_ts_win"
    races_path = data_dir / "races.parquet"
    out = _derived(data_dir) / f"market_odds_{_tag(minutes_before)}.parquet"
    sources = [races_path, *ts_dir.glob("year=*/*.parquet")]
    if _cached(out, sources, refresh):
        return pl.read_parquet(out)

    post = pl.scan_parquet(races_path).select("race_key", "post_at")
    parts = []
    for ydir in sorted(ts_dir.glob("year=*")):
        lf = (pl.scan_parquet(ydir / "*.parquet")
              .filter(pl.col("data_kubun") == INTERMEDIATE)
              .select([*ODDS_COLS, "announced_at"])
              .join(post, on="race_key", how="inner"))
        if minutes_before is not None:
            lf = lf.filter(pl.col("announced_at")
                           <= pl.col("post_at") - pl.duration(minutes=int(minutes_before)))
        lf = (lf.filter(pl.col("announced_at") == pl.col("announced_at").max().over("race_key"))
              .with_columns(minutes_to_post=((pl.col("post_at") - pl.col("announced_at"))
                                             .dt.total_seconds() / 60.0))
              .drop("post_at"))
        parts.append(lf.collect())
    df = pl.concat(parts).sort("race_key", "umaban")
    # 年をまたぐパーティション（前年末の前日発売）で同じレースが 2 年に分かれていたら、後の発表を残す
    df = df.filter(pl.col("announced_at") == pl.col("announced_at").max().over("race_key"))
    df.write_parquet(out)
    return df


def final_odds(*, data_dir: Path | None = None, refresh: bool = False) -> pl.DataFrame:
    """確定オッズ（odds_final、RACE の O1）。列: race_key, umaban, win_odds, win_status, win_pop, win_vote_total。"""
    data_dir = Path(data_dir or DATA_DIR)
    src = data_dir / "odds_final.parquet"
    out = _derived(data_dir) / "market_odds_final.parquet"
    if _cached(out, [src], refresh):
        return pl.read_parquet(out)
    df = pl.read_parquet(src, columns=ODDS_COLS).sort("race_key", "umaban")
    df.write_parquet(out)
    return df


# --- 評価対象 -----------------------------------------------------------------

def race_universe(*, data_dir: Path | None = None) -> pl.DataFrame:
    """評価対象の出走馬（モジュールの docstring の「評価対象」）。

    列: race_key, date, year, post_at, umaban, horse_id, abnormal_code, finish_pos, y, win_payout_odds。
    """
    data_dir = Path(data_dir or DATA_DIR)
    races = (pl.scan_parquet(data_dir / "races.parquet")
             .filter(~pl.col("is_cancelled"))
             .select("race_key", "date", "year", "post_at"))
    ent = (pl.scan_parquet(data_dir / "entries.parquet")
           .filter(~pl.col("abnormal_code").is_in(SCRATCHED_CODES) & pl.col("umaban").is_not_null())
           .select("race_key", "umaban", "horse_id", "abnormal_code", "finish_pos")
           .with_columns(y=(pl.col("finish_pos") == 1).fill_null(False).cast(pl.Int8)))
    pay = (pl.scan_parquet(data_dir / "payouts.parquet")
           .filter(pl.col("bet_type") == "win")
           .select("race_key", umaban=pl.col("combination").cast(pl.Int16, strict=False),
                   win_payout_odds=pl.col("payout") / 100.0)
           .drop_nulls("umaban"))
    return (races.join(ent, on="race_key", how="inner")
            .join(pay, on=["race_key", "umaban"], how="left")
            .sort("race_key", "umaban").collect())


# --- 確率 ---------------------------------------------------------------------

def market_probs(df, method: str = "proportional", *, k: float | None = None,
                 odds: str = "win_odds", race: str = "race_key", out: str = "p_market"):
    """オッズからレース内の勝率を作り、列 ``out`` を足して返す（polars でも pandas でも同じ型で返す）。

    method: market.implied_probs の 4 種（proportional, power, shin, goto）か ``power_fit``
    （p ∝ (1/odds)^k、k は全レース共通。``fit_power_k`` で学習期間から求めて渡す）。
    正規化は df に入っている馬の中で行う。取消馬を除いてから呼ぶこと。オッズが null の馬は NaN。
    """
    from keiba_ai import market

    if method not in METHODS:
        raise ValueError(f"method は {METHODS} のいずれか: {method!r}")
    is_pl = isinstance(df, pl.DataFrame)
    pdf = df.select(race, odds).to_pandas() if is_pl else df[[race, odds]].reset_index(drop=True)
    if method == "power_fit":
        if k is None:
            raise ValueError("power_fit には k が要る（fit_power_k で求める）")
        o = pdf[odds].astype(float)
        q = (1.0 / o.where(o > 0)) ** k
        p = (q / q.groupby(pdf[race]).transform("sum")).to_numpy()
    else:
        p = market.implied_probs(pdf, method, race=race, odds=odds).to_numpy()
    if is_pl:
        return df.with_columns(pl.Series(out, p, dtype=pl.Float64))
    res = df.copy()
    res[out] = p
    return res


def fit_power_k(df, *, odds: str = "win_odds", y: str = "y", race: str = "race_key") -> float:
    """p ∝ (1/odds)^k の k（全レース共通）をレース単位の条件付き最尤で求める。

    df は学習期間の出走馬（取消を除き、オッズが全馬にあるレース）。evaluate.fit_benter で
    log(比例正規化の確率) の係数を推定する（レース内の定数は消えるので log(1/odds) と同じ）。
    """
    from keiba_ai import evaluate

    d = market_probs(df, "proportional", odds=odds, race=race, out="_p_prop")
    pdf = d.select(race, y, "_p_prop").to_pandas() if isinstance(d, pl.DataFrame) else d
    fit = evaluate.fit_benter(pdf, ["_p_prop"], y=y, race=race)
    return float(fit["coef"]["_p_prop"])

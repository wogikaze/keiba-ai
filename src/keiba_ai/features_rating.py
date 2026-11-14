"""相手の強さを考えた馬のレーティング rating_v1（多頭の Elo）。1 行 = 1 レースの 1 出走馬。

日付順に進め、**その日のレースの前に**全レースのレーティングを読み取り、その日の結果で更新する（同じ日の結果は使わない）。
更新: 各馬の実際の得点 S = (n − 着順) / (n − 1)（中止・失格は 0）、期待得点 E = 他の馬との Elo の勝率の平均、
R ← R + K·(S − E)。K は出走数が少ないほど大きい（K0 / (1 + runs / K_HALF)^0.5）。新馬は初期値 R0。
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import polars as pl

from keiba_ai.features import DATA_DIR

VERSION = "rating_v1"
R0, K0, K_HALF, SCALE = 1500.0, 64.0, 5.0, 400.0
NOT_STARTED = (1, 2, 3)

FEATURES = {
    "rt_elo": "前日までの Elo レーティング",
    "rt_elo_runs": "レーティングに使った出走数",
    "rt_elo_rel": "Elo − レース内の平均",
    "rt_elo_gap_top": "Elo − 他の馬の最大",
    "rt_elo_exp": "Elo から見たレース内の期待得点（他の馬に勝つ確率の平均）",
    "rt_elo_delta3": "直近 3 走のレーティング変化の合計",
}


def build(data_dir: Path = DATA_DIR) -> pl.DataFrame:
    races = pl.read_parquet(data_dir / "races.parquet", columns=["race_key", "date", "is_cancelled"]).filter(
        ~pl.col("is_cancelled"))
    ent = (pl.read_parquet(data_dir / "entries.parquet",
                           columns=["race_key", "umaban", "horse_id", "abnormal_code", "finish_pos"])
           .filter(~pl.col("abnormal_code").is_in(NOT_STARTED) & pl.col("umaban").is_not_null())
           .join(races.select("race_key", "date"), on="race_key", how="inner")
           .sort("date", "race_key", "umaban"))
    hid, hidx = np.unique(ent["horse_id"].to_numpy(), return_inverse=True)
    R = np.full(len(hid), R0)
    runs = np.zeros(len(hid))
    hist = [[] for _ in range(len(hid))]  # 各馬のレーティング変化
    rk = ent["race_key"].to_numpy()
    dates = ent["date"].to_numpy()
    fp = ent["finish_pos"].to_numpy().astype(float)
    n_rows = len(ent)
    out = np.full((n_rows, len(FEATURES)), np.nan)
    starts = np.r_[0, np.nonzero(rk[1:] != rk[:-1])[0] + 1, n_rows]
    # 日ごとにまとめる
    race_dates = dates[starts[:-1]]
    day_starts = np.r_[0, np.nonzero(race_dates[1:] != race_dates[:-1])[0] + 1, len(race_dates)]
    for da, db in zip(day_starts[:-1], day_starts[1:]):
        updates = []
        for r in range(da, db):
            a, b = starts[r], starts[r + 1]
            idx = hidx[a:b]
            Ri = R[idx]
            n = b - a
            diff = (Ri[None, :] - Ri[:, None]) / SCALE        # [i, j] = (R_j − R_i)/400
            pw = 1.0 / (1.0 + 10.0 ** diff)                  # i が j に勝つ確率
            np.fill_diagonal(pw, np.nan)
            E = np.nanmean(pw, axis=1) if n > 1 else np.full(n, 0.5)
            others_max = np.array([np.max(np.delete(Ri, i)) if n > 1 else np.nan for i in range(n)])
            d3 = np.array([np.sum(hist[h][-3:]) if hist[h] else np.nan for h in idx])
            out[a:b] = np.column_stack([Ri, runs[idx], Ri - Ri.mean(), Ri - others_max, E, d3])
            if n > 1:
                pos = fp[a:b]
                S = np.where(np.isnan(pos), 0.0, (n - pos) / (n - 1))
                K = K0 / np.sqrt(1.0 + runs[idx] / K_HALF)
                updates.append((idx, K * (S - E)))
        for idx, dR in updates:  # その日の全レースを読み取ってから更新する
            R[idx] += dR
            runs[idx] += 1
            for h, v in zip(idx, dR):
                hist[h].append(v)
    df = ent.select("race_key", "umaban")
    return df.with_columns([pl.Series(name, out[:, i]) for i, name in enumerate(FEATURES)])


def load_rating(data_dir: Path = DATA_DIR, refresh: bool = False) -> pl.DataFrame:
    path = data_dir / "derived" / f"{VERSION}.parquet"
    srcs = [data_dir / f"{t}.parquet" for t in ("races", "entries")]
    if not refresh and path.exists() and path.stat().st_mtime >= max(p.stat().st_mtime for p in srcs):
        return pl.read_parquet(path)
    df = build(data_dir)
    df.write_parquet(path)
    path.with_suffix(".json").write_text(json.dumps({"features": FEATURES, "R0": R0, "K0": K0, "K_HALF": K_HALF},
                                                    ensure_ascii=False, indent=1))
    return df

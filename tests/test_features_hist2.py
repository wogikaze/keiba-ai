import datetime as dt

import numpy as np
import polars as pl
from polars.testing import assert_frame_equal

from keiba_ai import features_hist2 as H


def _data(seed=0, n_days=30):
    rng = np.random.default_rng(seed)
    races, ents = [], []
    horses = [f"H{i:03d}" for i in range(60)]
    for d in range(n_days):
        date = dt.date(2020, 1, 1) + dt.timedelta(days=d * 3)
        for r in range(3):
            rk = f"{date:%Y%m%d}0101{r + 1:02d}{r + 1:02d}"
            races.append({"race_key": rk, "date": date, "is_cancelled": False})
            hs = rng.choice(horses, 8, replace=False)  # 同じ日に 2 回走る馬がいないよう 1 日 1 レースに分ける
            if r > 0:
                continue
            odds = rng.uniform(1.5, 80, 8)
            order = rng.permutation(8) + 1
            pop = np.argsort(np.argsort(odds)) + 1
            for i, h in enumerate(hs):
                ents.append({"race_key": rk, "umaban": i + 1, "horse_id": h, "jockey_code": f"J{rng.integers(5)}",
                             "trainer_code": f"T{rng.integers(5)}", "abnormal_code": 0,
                             "finish_pos": int(order[i]), "win_odds": float(odds[i]), "win_pop": int(pop[i])})
    return (pl.DataFrame(races), pl.DataFrame(ents).with_columns(pl.col("umaban").cast(pl.Int16)),
            pl.DataFrame({"horse_id": horses, "sire_id": [f"S{i % 7}" for i in range(60)]}))


def _write(p, races, ents, horses):
    p.mkdir()
    (p / "derived").mkdir()
    races.write_parquet(p / "races.parquet")
    ents.write_parquet(p / "entries.parquet")
    horses.write_parquet(p / "horses.parquet")


def test_hist2_uses_only_previous_days(tmp_path):
    races, ents, horses = _data()
    last = races["date"].max()
    rk_last = races.filter(pl.col("date") == last)["race_key"]
    # 最終日の結果とオッズを壊しても、どの行の特徴量も変わらない（当日の分は使わない）
    ents2 = ents.with_columns(
        finish_pos=pl.when(pl.col("race_key").is_in(rk_last.implode())).then(9 - pl.col("finish_pos"))
        .otherwise("finish_pos"),
        win_odds=pl.when(pl.col("race_key").is_in(rk_last.implode())).then(pl.col("win_odds") * 5)
        .otherwise("win_odds"))
    _write(tmp_path / "a", races, ents, horses)
    _write(tmp_path / "b", races, ents2, horses)
    fa = H.load_hist2(tmp_path / "a").sort("race_key", "umaban")
    fb = H.load_hist2(tmp_path / "b").sort("race_key", "umaban")
    assert_frame_equal(fa, fb)
    # 途中の日の結果を壊すと、その日より後の行だけが変わる
    mid = sorted(races["date"].unique())[15]
    rk_mid = races.filter(pl.col("date") == mid)["race_key"]
    ents3 = ents.with_columns(finish_pos=pl.when(pl.col("race_key").is_in(rk_mid.implode()))
                              .then(9 - pl.col("finish_pos")).otherwise("finish_pos"))
    _write(tmp_path / "c", races, ents3, horses)
    fc = H.load_hist2(tmp_path / "c").sort("race_key", "umaban")
    dates = fa.join(races.select("race_key", "date"), on="race_key")["date"]
    upto = (dates <= mid).to_numpy()
    assert_frame_equal(fa.filter(upto), fc.filter(upto))
    assert not fa.filter(~upto).equals(fc.filter(~upto))

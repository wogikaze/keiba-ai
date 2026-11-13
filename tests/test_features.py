"""features.py のリーク検査（合成データ）。

ある日 D について、(1) D より後のデータを消し、(2) D 当日の結果の列を壊し、(3) D 当日以降の
調教を消しても、D 以前のすべての行の特徴量が変わらないことを確かめる。
"""

from datetime import date, timedelta

import numpy as np
import polars as pl
import pytest

from keiba_ai import features as F

RESULT_COLS = ["finish_pos", "time_sec", "last_3f", "time_diff", "corner4", "prize"]


def make_synthetic(n_days=120, races_per_day=6, n_horses=400, n_jockeys=25, n_trainers=30, seed=0):
    rng = np.random.default_rng(seed)
    start = date(2010, 1, 2)
    ability = rng.normal(0, 1, n_horses)
    last_run = np.full(n_horses, -999)
    races, entries = [], []
    for d in range(0, n_days * 3, 3):  # 3 日おきに開催
        day = start + timedelta(days=d)
        for r in range(races_per_day):
            key = f"{day:%Y%m%d}05{1:02d}{1:02d}{r + 1:02d}"
            venue = ["05", "06"][r % 2]
            surface = ["turf", "dirt"][(r // 2) % 2]
            dist = [1200, 1600, 2000][r % 3]
            races.append(dict(race_key=key, date=day, is_cancelled=bool(rng.random() < 0.02),
                              venue_code=venue, surface=surface, track_code="10", distance=dist,
                              grade_code=None if r < 5 else "E", race_type_code="13",
                              race_symbol_code="000", weight_type_code="3",
                              going_code=str(rng.integers(1, 5)), weather_code="1",
                              prize_1st=int(rng.choice([5_000_000, 10_000_000])),
                              cond_youngest=["703", "005", "010", "999"][r % 4]))
            free = np.where(d - last_run >= 14)[0]
            n = min(int(rng.integers(6, 15)), len(free))
            hs = rng.choice(free, n, replace=False)
            last_run[hs] = d
            perf = ability[hs] + rng.normal(0, 1, n)
            order = np.argsort(-perf)
            pos = np.empty(n, int)
            pos[order] = np.arange(1, n + 1)
            ab = rng.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 4], n)
            for i, h in enumerate(hs):
                fin = None if ab[i] in (1, 2, 3, 4) else int(pos[i])
                t = None if fin is None else float(dist / 16.5 - perf[i] + rng.normal(0, 0.3))
                entries.append(dict(
                    race_key=key, umaban=i + 1, wakuban=i // 2 + 1, horse_id=f"H{h:05d}",
                    sex_code=str(1 + h % 3), age=3 + h % 4, belong_code=str(1 + h % 2),
                    trainer_code=f"T{h % n_trainers:03d}", weight_carried=54.0 + rng.integers(0, 4),
                    blinker=int(rng.random() < 0.1), jockey_code=f"J{rng.integers(n_jockeys):03d}",
                    apprentice_code="0", horse_weight=int(rng.integers(420, 520)),
                    weight_diff=int(rng.integers(-10, 11)), abnormal_code=int(ab[i]), finish_pos=fin,
                    time_sec=t, last_3f=None if t is None else 35 + rng.normal(0, 1),
                    time_diff=None if fin is None else float(rng.exponential(1)),
                    corner4=None if fin is None else int(rng.integers(1, n + 1)),
                    prize=int(rng.choice([0, 1_000_000])),
                ))
    races = pl.DataFrame(races)
    entries = pl.DataFrame(entries)
    horses = pl.DataFrame({"horse_id": [f"H{h:05d}" for h in range(n_horses)],
                           "sire_id": [f"S{h % 15:03d}" for h in range(n_horses)]})
    tdays = [start + timedelta(days=int(x)) for x in rng.integers(-30, n_days * 3, 40_000)]
    th = [f"H{h:05d}" for h in rng.integers(0, n_horses, 40_000)]
    slope = pl.DataFrame({"horse_id": th, "train_date": tdays,
                          "train_time": [f"{int(x):04d}" for x in rng.integers(600, 1100, 40_000)],
                          "total_4f": rng.normal(53, 2, 40_000), "lap_200_0": rng.normal(12.5, 0.5, 40_000)})
    slope = slope.unique(subset=["horse_id", "train_date", "train_time"], keep="first", maintain_order=True)
    wood = slope.rename({"total_4f": "total_3f"}).sample(fraction=0.3, seed=seed)
    return races, entries, horses, slope, wood


@pytest.fixture(scope="module")
def synth():
    return make_synthetic()


def _build(races, entries, horses, slope, wood):
    return F.build_features(races, entries, horses, slope, wood, F.FeatureConfig(speed_min_n=5))


def _truncate(races, entries, slope, wood, cut, seed=1):
    """cut より後を消し、cut 当日の結果を壊し、cut 当日以降の調教を消す。"""
    rng = np.random.default_rng(seed)
    r = races.filter(pl.col("date") <= cut)
    e = entries.join(r.select("race_key", "date"), on="race_key")
    today = e["date"] == cut
    m = today.to_numpy()
    scr = {}
    for c in RESULT_COLS[1:]:
        v = e[c].cast(pl.Float64).to_numpy().copy()
        v[m] = rng.permutation(np.nan_to_num(v[m], nan=1.0)) * rng.uniform(0.5, 2.0)
        scr[c] = pl.Series(c, v, nan_to_null=True).cast(e[c].dtype, strict=False)
    e2 = e.with_columns(**scr)
    # 当日の着順も壊す（1 着の付け替え）
    fp = np.where(m, rng.integers(1, 15, len(e)), e["finish_pos"].fill_null(-1).to_numpy())
    e2 = e2.with_columns(finish_pos=pl.Series(fp).cast(pl.Int64).replace(-1, None))
    s = slope.filter(pl.col("train_date") < cut)
    w = wood.filter(pl.col("train_date") < cut)
    return r, e2.drop("date"), s, w


FEATURE_NAMES = list(F.FEATURES)


@pytest.mark.parametrize("cut_idx", [10, 60, 110])
def test_no_same_day_or_future_information(synth, cut_idx):
    races, entries, horses, slope, wood = synth
    days = sorted(races["date"].unique().to_list())
    cut = days[cut_idx]
    full = _build(races, entries, horses, slope, wood)
    r, e, s, w = _truncate(races, entries, slope, wood, cut)
    trunc = _build(r, e, horses, s, w)

    a = full.filter(pl.col("date") <= cut).sort("race_key", "umaban")
    b = trunc.sort("race_key", "umaban")
    assert a.height == b.height > 0
    assert (a["race_key"] == b["race_key"]).all() and (a["umaban"] == b["umaban"]).all()
    for c in FEATURE_NAMES:
        x, y = a[c], b[c]
        if x.dtype == pl.String:
            assert x.equals(y, null_equal=True), c
        else:
            xa, ya = x.to_numpy().astype(float), y.to_numpy().astype(float)
            np.testing.assert_allclose(xa, ya, rtol=1e-9, atol=1e-9, equal_nan=True, err_msg=c)
    # 壊した当日のラベルは実際に変わっている（検査が空振りしていない）
    la = a.filter(pl.col("date") == cut)["y_win"].to_numpy()
    lb = b.filter(pl.col("date") == cut)["y_win"].to_numpy()
    assert (la != lb).any()


def test_history_values_by_hand():
    races = pl.DataFrame({
        "race_key": ["2010010205010101", "2010010205010102", "2010011005010101"],
        "date": [date(2010, 1, 2), date(2010, 1, 2), date(2010, 1, 10)],
        "is_cancelled": [False] * 3, "venue_code": ["05"] * 3, "surface": ["turf", "dirt", "turf"],
        "track_code": ["10"] * 3, "distance": [1600, 1200, 1800], "grade_code": [None] * 3,
        "race_type_code": ["13"] * 3, "race_symbol_code": ["000"] * 3, "weight_type_code": ["3"] * 3,
        "going_code": ["1"] * 3, "weather_code": ["1"] * 3, "prize_1st": [5_000_000] * 3,
        "cond_youngest": ["703"] * 3})
    rows = []
    # 1 レース目: A 1 着, B 2 着, C 3 着。2 レース目: D 1 着, E 2 着（同じ日）。3 レース目: A, B, D
    for key, hs, pos in [("2010010205010101", "ABC", [1, 2, 3]), ("2010010205010102", "DE", [1, 2]),
                         ("2010011005010101", "ABD", [3, 1, 2])]:
        for i, (h, p) in enumerate(zip(hs, pos)):
            rows.append(dict(race_key=key, umaban=i + 1, wakuban=i + 1, horse_id=h, sex_code="1", age=3,
                             belong_code="1", trainer_code="T1", weight_carried=55.0, blinker=0,
                             jockey_code="J1" if h in "AD" else "J2", apprentice_code="0",
                             horse_weight=480, weight_diff=0, abnormal_code=0, finish_pos=p,
                             time_sec=100.0 + p, last_3f=35.0, time_diff=0.1 * (p - 1), corner4=p,
                             prize=1_000_000 if p == 1 else 0))
    f = F.build_features(races, pl.DataFrame(rows), cfg=F.FeatureConfig(rate_prior_strength=0.0))
    f = f.sort("race_key", "umaban")
    first = f.filter(pl.col("date") == date(2010, 1, 2))
    # 初日はすべての履歴が空、騎手の率は「前日までの全体の率」もないので null
    assert (first["h_n_runs"] == 0).all() and first["h_pos_1"].is_null().all()
    assert first["jk_win_rate"].fill_nan(None).is_null().all()
    last = f.filter(pl.col("date") == date(2010, 1, 10))
    a, b, d = last.row(0, named=True), last.row(1, named=True), last.row(2, named=True)
    assert a["h_n_runs"] == 1 and a["h_pos_1"] == 0.0 and a["h_win_rate"] == 1.0
    assert b["h_pos_1"] == 0.5 and b["h_days_since"] == 8
    assert d["h_surface_change"] == 1.0 and d["h_same_surface_runs"] == 0
    # 騎手 J1 は前日までに 2 戦 2 勝（A, D）、縮小なし
    assert a["jk_win_rate"] == 1.0 and b["jk_win_rate"] == 0.0
    assert a["h_dist_change"] == 200 and d["h_dist_change"] == 600


def test_same_day_duplicate_horse_rejected(synth):
    races, entries, *_ = synth
    r0 = races.row(0, named=True)["race_key"]
    r1 = races.filter(pl.col("date") == races["date"][0]).row(1, named=True)["race_key"]
    dup = entries.filter(pl.col("race_key") == r0).head(1).with_columns(race_key=pl.lit(r1), umaban=pl.lit(99, entries["umaban"].dtype))
    with pytest.raises(ValueError):
        F.base_frame(races.with_columns(is_cancelled=pl.lit(False)), pl.concat([entries, dup]),
                     F.FeatureConfig())

import datetime as dt

import numpy as np
import polars as pl

from keiba_ai import features_market as fm


def _write(tmp, ts: pl.DataFrame, q: pl.DataFrame):
    races = pl.DataFrame({"race_key": ["2024010101010101", "2024010101010102"],
                          "post_at": [dt.datetime(2024, 1, 1, 12, 0), dt.datetime(2024, 1, 1, 12, 30)]})
    races.write_parquet(tmp / "races.parquet")
    (tmp / "odds_ts_win" / "year=2024").mkdir(parents=True)
    ts.write_parquet(tmp / "odds_ts_win" / "year=2024" / "part-000.parquet")
    (tmp / "odds_ts_quinella_snap" / "year=2024").mkdir(parents=True)
    q.write_parquet(tmp / "odds_ts_quinella_snap" / "year=2024" / "part-000.parquet")


def _data(seed=0):
    rng = np.random.default_rng(seed)
    rows, qrows = [], []
    for rk, post in (("2024010101010101", dt.datetime(2024, 1, 1, 12, 0)),
                     ("2024010101010102", dt.datetime(2024, 1, 1, 12, 30))):
        for m in range(-120, 5, 3):  # 発走 120 分前〜発走 4 分後まで 3 分おき
            t = post + dt.timedelta(minutes=m)
            for u in range(1, 7):
                rows.append({"race_key": rk, "announced_at": t, "data_kubun": "1", "umaban": u,
                             "win_odds": float(rng.uniform(1.5, 50)), "win_status": "ok",
                             "place_odds_min": float(rng.uniform(1.1, 5)), "place_odds_max": float(rng.uniform(5, 9)),
                             "win_vote_total": int(1e6 + 1e4 * (m + 120)), "place_vote_total": int(2e6)})
            for a in range(1, 7):
                for b in range(a + 1, 7):
                    for snap in ("10", "1"):
                        qrows.append({"race_key": rk, "snap": snap, "a": a, "b": b,
                                      "odds": float(rng.uniform(3, 200)), "status": "ok"})
    ts = pl.DataFrame(rows).with_columns(pl.col("umaban").cast(pl.Int16),
                                         pl.col("win_status").cast(pl.Enum(["ok", "no_vote", "cancel_pre", "cancel_post"])))
    q = pl.DataFrame(qrows).with_columns(pl.col("a").cast(pl.Int8), pl.col("b").cast(pl.Int8),
                                         pl.col("status").cast(pl.Enum(["ok", "no_vote", "cancel_pre", "cancel_post"])))
    return ts, q


def test_market_features_ignore_announcements_after_decision(tmp_path):
    ts, q = _data()
    a_dir, b_dir = tmp_path / "a", tmp_path / "b"
    a_dir.mkdir(), b_dir.mkdir()
    _write(a_dir, ts, q)
    post = pl.DataFrame({"race_key": ["2024010101010101", "2024010101010102"],
                         "post_at": [dt.datetime(2024, 1, 1, 12, 0), dt.datetime(2024, 1, 1, 12, 30)]})
    late = ts.join(post, on="race_key").with_columns(
        late=pl.col("announced_at") > pl.col("post_at") - pl.duration(minutes=10))
    # 決定時刻より後の発表と、10 分前より後の馬連スナップショットを壊す
    ts2 = late.with_columns(
        win_odds=pl.when("late").then(pl.col("win_odds") * 7).otherwise("win_odds"),
        win_vote_total=pl.when("late").then(pl.col("win_vote_total") * 3).otherwise("win_vote_total"),
    ).drop("post_at", "late")
    q2 = q.with_columns(odds=pl.when(pl.col("snap") == "1").then(pl.col("odds") * 9).otherwise("odds"))
    _write(b_dir, ts2, q2)
    fa = fm.load_market_features(a_dir).sort("race_key", "umaban")
    fb = fm.load_market_features(b_dir).sort("race_key", "umaban")
    from polars.testing import assert_frame_equal

    assert_frame_equal(fa, fb, rel_tol=1e-12)  # 和の順序による 1e-16 程度の差は許す
    assert fa.height == 12
    # 10 分前のスナップショットは発走 12 分前の発表（3 分おきの −12）
    assert fa["mk_mins"].unique().to_list() == [12.0]
    assert fa["mk_dfirst"].null_count() == 0

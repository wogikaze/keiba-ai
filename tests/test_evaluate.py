import numpy as np
import pandas as pd
import pytest

from keiba_ai import evaluate as ev


def test_logloss_dead_heat_and_top1():
    df = pd.DataFrame({"race_id": [1, 1, 1, 2, 2], "p": [0.5, 0.3, 0.2, 0.6, 0.4],
                       "y": [1, 1, 0, 0, 1]})
    s = ev.race_scores(df, "p")
    # 同着は −(log 0.5 + log 0.3)/2
    np.testing.assert_allclose(s.loc[1, "logloss"], -(np.log(0.5) + np.log(0.3)) / 2)
    np.testing.assert_allclose(s.loc[2, "logloss"], -np.log(0.4))
    np.testing.assert_allclose(s.loc[1, "brier"], 0.0**2 + 0.2**2 + 0.2**2)
    assert s["top1"].tolist() == [1.0, 0.0]


def test_nan_winner_raises_and_renormalize():
    df = pd.DataFrame({"race_id": [1, 1, 1], "p": [2.0, 1.0, np.nan], "y": [0, 1, 0]})
    np.testing.assert_allclose(ev.renormalize(df, "p")[:2], [2 / 3, 1 / 3])
    with pytest.raises(ValueError):
        ev.race_scores(df.assign(y=[0, 0, 1]), "p")


def test_market_is_truth_delta_covers_zero(races):
    # 市場が真の生成過程。情報のないモデルを Benter で足しても市場と区別できない
    df = races(4000, seed=2)
    split = ev.time_split(df["date"], "2021-01-01")
    r = ev.benter_two_stage(df[split == "train"], df[split == "test"], "p_model", "p_market",
                            cluster="date", n_boot=500)
    assert abs(r["alpha"]) < 2.5 * r["alpha_se"] + 0.02
    lo, hi = r["test"]["ci"]
    assert lo <= 0 <= hi and abs(r["test"]["delta"]) < 0.01
    # 真の確率そのものを比べれば Δ=0 ちょうど
    assert ev.delta_logloss(df, "p_true", "p_market")["delta"] == pytest.approx(0)


def test_extra_signal_gives_positive_alpha(races):
    df = races(4000, seed=3, b_scale=0.7)
    split = ev.time_split(df["date"], "2021-01-01")
    r = ev.benter_two_stage(df[split == "train"], df[split == "test"], "p_model", "p_market",
                            n_boot=500)
    assert r["alpha"] > 3 * r["alpha_se"] > 0
    assert r["test"]["ci"][1] < 0  # 結合は市場より良い
    assert 0.8 < r["beta"] < 1.2


def test_shuffled_placebo_is_worse(races):
    df = races(3000, seed=4, b_scale=0.7)
    real = ev.delta_logloss(df, "p_model", "p_market")["delta"]
    pl = ev.placebo(df, lambda d, rng: ev.shuffle_within_race(d, "p_model", rng), "p_market", n_rep=5)
    assert (pl["delta"] > real).all()
    # 並べ替えてもレース内の和は 1 のまま、値の集合も同じ
    sh = ev.shuffle_within_race(df, "p_model", np.random.default_rng(0))
    np.testing.assert_allclose(sh.groupby(df["race_id"]).sum(), 1.0)
    assert sorted(sh[df.race_id == 0]) == sorted(df.loc[df.race_id == 0, "p_model"])


def test_summary_and_calibration(races):
    df = races(3000, seed=5)
    s = ev.summary(df, "p_true")
    assert s["ece"] < 0.01 and s["n_races"] == 3000
    c = ev.calibration_table(df, "p_true", bins=5)
    assert c["n"].sum() == len(df)
    np.testing.assert_allclose(c["p_mean"], c["win_rate"], atol=0.02)


def test_betting_uses_decision_and_payout_columns():
    df = pd.DataFrame({
        "race_id": [1, 1, 2, 2, 3, 3], "date": pd.to_datetime(["2024-01-01"] * 4 + ["2024-01-02"] * 2),
        "p": [0.6, 0.4, 0.5, 0.5, 0.7, 0.3], "y": [1, 0, 0, 1, 0, 1],
        "o_pre": [2.0, 2.0, 1.5, 3.0, 2.0, 2.0], "o_final": [1.5, 4.0, 1.5, 2.5, 1.2, np.nan],
    })
    r = ev.simulate_bets(df, "p", decision_odds="o_pre", payout_odds="o_final", n_boot=200)
    # 判断は o_pre: 1-1 (1.2), 2-2 (1.5), 3-1 (1.4) を買う。3-2 は p·o=0.6 で買わない
    assert r["n_bets"] == 3 and r["n_hits"] == 2 and r["n_void"] == 0
    assert r["return"] == pytest.approx(1.5 + 2.5)
    assert r["roi"] == pytest.approx(4.0 / 3 - 1)
    assert r["max_drawdown"] == pytest.approx(1.0)  # +0.5, +2.0, +1.0
    with pytest.warns(UserWarning):
        ev.simulate_bets(df, "p", decision_odds="o_pre", payout_odds="o_pre", n_boot=10)


def test_betting_on_fair_market_loses_takeout(races):
    df = races(3000, seed=6)
    df["odds_pay"] = df["odds"]
    r = ev.simulate_bets(df, "p_market", decision_odds="odds", payout_odds="odds_pay",
                         threshold=0.0, cluster="date", n_boot=300)
    lo, hi = r["roi_ci"]
    assert lo < -0.2 < hi  # 全頭買いの期待 ROI は −控除率


def test_time_split():
    d = pd.Series(pd.to_datetime(["2019-12-31", "2020-01-01", "2020-06-30", "2020-07-01", "2021-01-01"]))
    s = ev.time_split(d, "2020-01-01", "2020-07-01", "2021-01-01")
    assert s.tolist()[:4] == ["train", "valid", "valid", "test"] and pd.isna(s.iloc[4])

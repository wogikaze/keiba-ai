import numpy as np
import pandas as pd
import pytest

from keiba_ai.market import METHODS, implied_probs, overround


def _race(p, odds):
    return pd.DataFrame({"race_id": [1] * len(odds), "odds": odds, "p": p})


P = np.array([0.4, 0.3, 0.2, 0.1])


@pytest.mark.parametrize("method", METHODS)
def test_fair_odds_recover_probs(method):
    out = implied_probs(_race(P, 1 / P), method)
    np.testing.assert_allclose(out, P, atol=1e-9)


@pytest.mark.parametrize("method", METHODS)
def test_sums_to_one_and_excludes_scratched(method, races):
    df = races(200, seed=1)
    df.loc[df.index[::7], "odds"] = np.nan  # 取消
    df.loc[df.index[3], "odds"] = 0.0
    out = implied_probs(df, method)
    assert out[df["odds"].isna() | (df["odds"] <= 0)].isna().all()
    np.testing.assert_allclose(out.groupby(df["race_id"]).sum(), 1.0, atol=1e-9)
    assert (out.dropna() > 0).all()


def test_proportional_removes_takeout():
    out = implied_probs(_race(P, 0.8 / P), "proportional")
    np.testing.assert_allclose(out, P, atol=1e-12)


def test_power_round_trip():
    k = 1.15
    q = P ** (1 / k)  # p = q^k
    np.testing.assert_allclose(implied_probs(_race(P, 1 / q), "power"), P, atol=1e-8)


def test_shin_round_trip():
    z = 0.05
    s = np.sqrt(z * P + (1 - z) * P**2)
    q = s * s.sum()  # Shin モデルが生む implied probability
    np.testing.assert_allclose(implied_probs(_race(P, 1 / q), "shin"), P, atol=1e-8)


def test_goto_matches_reference_formula():
    q = np.array([0.5, 0.35, 0.25, 0.15])  # Σ=1.25
    se = np.sqrt(q * (1 - q) / q)
    ref = q - se * (q.sum() - 1) / se.sum()
    np.testing.assert_allclose(implied_probs(_race(q, 1 / q), "goto"), ref / ref.sum(), atol=1e-12)


def test_longshot_correction_direction():
    # 控除を本命・大穴で比例以外に配る方法は、大穴の確率を比例より小さくする
    q = np.array([0.45, 0.3, 0.2, 0.1, 0.05])  # goto は Σq が大きいと負になり比例に戻るので控えめな控除
    df = _race(q, 1 / q)
    prop = implied_probs(df, "proportional")
    for m in ("power", "shin", "goto"):
        assert implied_probs(df, m).iloc[-1] < prop.iloc[-1]


def test_single_runner_and_overround():
    df = pd.DataFrame({"race_id": [1, 2, 2], "odds": [1.5, 2.0, np.nan]})
    for m in METHODS:
        np.testing.assert_allclose(implied_probs(df, m)[:2], [1.0, 1.0])
    np.testing.assert_allclose(overround(df), [1 / 1.5, 0.5])

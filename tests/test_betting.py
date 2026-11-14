import itertools

import numpy as np
import pandas as pd

from keiba_ai.betting import combos, kelly, policy, pricing


def _brute(p, g2, g3):
    """割引つき Harville の 3連単を定義どおりに計算する。"""
    n = len(p)
    s2 = p ** g2 / np.sum(p ** g2)
    s3 = p ** g3 / np.sum(p ** g3)
    T = {}
    for i, j, k in itertools.permutations(range(n), 3):
        T[(i, j, k)] = p[i] * s2[j] / (1 - s2[i]) * s3[k] / (1 - s3[i] - s3[j])
    return T


def test_race_probs_match_definition_and_sum():
    rng = np.random.default_rng(0)
    p = rng.dirichlet(np.ones(7))
    u = np.array([3, 1, 7, 2, 9, 5, 4])
    g2, g3 = 0.85, 0.75
    r = combos.race_probs(u, p, g2, g3)
    T = _brute(p, g2, g3)
    tri = dict(zip(*r["trifecta"]))
    for (i, j, k), v in T.items():
        np.testing.assert_allclose(tri[u[i] * 10000 + u[j] * 100 + u[k]], v)
    # 排反な券種は合計 1（γ が 1 でないと 3連単の合計は厳密には 1 にならないので緩く）
    for t in ("win", "exacta", "quinella"):
        np.testing.assert_allclose(r[t][1].sum(), 1.0, atol=1e-9)
    np.testing.assert_allclose(r["trio"][1].sum(), r["trifecta"][1].sum())
    # 複勝（3 着まで）の合計 = 3 着までに入る頭数の期待値（3 着の確率の合計が 1 のとき 3）
    np.testing.assert_allclose(r["place"][1].sum(), 2 + r["trifecta"][1].sum(), atol=1e-9)
    # ワイドの合計 = 3 頭から 2 頭を選ぶ 3 組 × 3連複の合計
    np.testing.assert_allclose(r["wide"][1].sum(), 3 * r["trio"][1].sum())
    # 組番は小さい順（馬連・ワイド・3連複）
    q = r["quinella"][0]
    assert np.all(q // 100 < q % 100)
    tr = r["trio"][0]
    assert np.all((tr // 10000 < tr // 100 % 100) & (tr // 100 % 100 < tr % 100))


def test_fit_gammas_recovers_parameters():
    rng = np.random.default_rng(1)
    g2, g3 = 0.8, 0.7
    ps, f, s, t = [], [], [], []
    for _ in range(4000):
        n = rng.integers(8, 17)
        p = rng.dirichlet(np.full(n, 0.8))
        E, T = combos.tensors(p, g2, g3)
        flat = T.ravel() / T.sum()
        i, j, k = np.unravel_index(rng.choice(len(flat), p=flat), T.shape)
        ps.append(p), f.append(i), s.append(j), t.append(k)
    fit = combos.fit_gammas(ps, f, s, t)
    assert abs(fit["g2"] - g2) < 0.05 and abs(fit["g3"] - g3) < 0.07
    assert fit["nll2"] <= fit["nll2_harville"]


def test_kelly_exclusive_known_case_and_no_edge():
    # 2 頭、p = 0.6/0.4、オッズ 2.0/2.5: 両方に張るのが最適（Σ1/o = 0.9 < 1）
    f = kelly.exclusive(np.array([0.6, 0.4]), np.array([2.0, 2.5]))
    R = (1 - 1.0) / (1 - 0.9)  # 両方選ぶと R = 0
    np.testing.assert_allclose(f, [0.6 - R / 2.0, 0.4 - R / 2.5])
    # 1 頭だけ期待値 > 1
    f = kelly.exclusive(np.array([0.5, 0.3, 0.2]), np.array([2.4, 2.5, 4.0]))
    np.testing.assert_allclose(f, [0.5 - 0.5 / (1 - 1 / 2.4) / 2.4, 0, 0])
    # 期待値 > 1 がなければ賭けない（控除のある市場で p = 市場の確率）
    q = np.array([0.5, 0.3, 0.2])
    assert kelly.exclusive(q, 0.8 / q).sum() == 0
    np.testing.assert_allclose(kelly.independent(np.array([0.5, 0.1]), np.array([3.0, 5.0])), [0.25, 0.0])


def test_kelly_exclusive_maximizes_log_growth():
    rng = np.random.default_rng(3)
    p = rng.dirichlet(np.ones(6))
    o = 0.85 / rng.dirichlet(np.ones(6))
    f = kelly.exclusive(p, o)

    def growth(f):
        return np.sum(p * np.log(1 - f.sum() + f * o))

    g = growth(f)
    for _ in range(2000):
        h = np.clip(f + rng.normal(0, 0.01, 6), 0, None)
        if h.sum() < 1:
            assert growth(h) <= g + 1e-12


def test_effective_pay_no_stake_and_dilution():
    pay = np.array([5.0, 0.0])
    np.testing.assert_allclose(policy.effective_pay(pay, [0, 100], 100, [1e6, 1e6], 1, 0.2), [5.0, 0.0])
    # 的中組番の票数 W = 1e6·0.8/5 = 160,000。そこに 160,000 円を足すと払戻はほぼ半分
    e = policy.effective_pay(np.array([5.0]), [160_000], 160_000, [1e6], 1, 0.2)
    np.testing.assert_allclose(e, (1e6 + 160_000) * 0.8 / 320_000)


def _cands(n_races=400, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    dates = pd.date_range("2022-01-01", periods=n_races // 10, freq="D")
    for r in range(n_races):
        p = rng.dirichlet(np.ones(8))
        o = 0.8 / p * np.exp(rng.normal(0, 0.2, 8))
        w = rng.choice(8, p=p)
        pay = np.where(np.arange(8) == w, o, 0.0)
        f = kelly.exclusive(p, o)
        for i in range(8):
            rows.append((r, dates[r // 10], 2022, p[i], o[i], f[i], pay[i], np.nan, 1, 0.2))
    return pd.DataFrame(rows, columns=["race_idx", "date", "year", "p", "o", "f_full", "pay", "pool", "k_win",
                                       "takeout"])


def test_flat_and_kelly_and_metrics_run():
    c = _cands()
    b = policy.flat(c, 1.1, (1, np.inf), 100)
    assert (b["p"] * b["o"] >= 1.1).all() and (b["stake"] == 100).all()
    m = policy.bet_metrics(b, c["date"], n_boot=200)
    assert m["roi_ci"][0] <= m["roi"] <= m["roi_ci"][1]
    kb, path = policy.kelly(c, 0.25, 0.05, 1e6)
    assert len(path) >= 2 and (kb["stake"] % 100 == 0).all()
    # どのレースも賭け金の合計は資金の 5% 以下
    assert (kb.groupby("race_idx")["stake"].sum().to_numpy() <= 0.05 * path.max() + 1e-6).all()


def test_placebo_pool_unbiased_when_market_fair():
    # 確率どおりに払う市場（控除なし）では、無作為な賭けの回収率の平均は 0 付近
    rng = np.random.default_rng(5)
    pool = policy.PlaceboPool()
    o_all, pay_all = [], []
    for _ in range(3000):
        p = rng.dirichlet(np.ones(10))
        o = 1 / p
        w = rng.choice(10, p=p)
        pay = np.where(np.arange(10) == w, o, 0.0)
        pool.add(o, pay)
        o_all.append(o), pay_all.append(pay)
    o_all = np.concatenate(o_all)
    bets = pd.DataFrame({"o": o_all[:3000], "stake": 100.0})
    d = pool.roi_distribution(bets, 300, 0)
    assert abs(np.mean(d)) < 0.1


def test_holm():
    adj = policy.holm({"a": 0.01, "b": 0.04, "c": 0.03})
    assert adj == {"a": 0.03, "b": 0.06, "c": 0.06}


def test_pricing_recovers_linear_model():
    rng = np.random.default_rng(2)
    q = rng.uniform(1e-4, 0.3, 5000)
    n = rng.integers(6, 19, 5000)
    o = np.exp(-0.3 - 0.95 * np.log(q) + 0.01 * np.log(q) ** 2 + 0.05 * np.log(n) + rng.normal(0, 0.1, 5000))
    m = pricing.fit_price(q, n, o)
    np.testing.assert_allclose(m["beta"], [-0.3, -0.95, 0.01, 0.05], atol=0.05)
    assert (pricing.predict_price(m, q, n) >= 1).all()

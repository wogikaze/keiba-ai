import numpy as np
import pytest

from keiba_ai import market_offset as mo


def _synthetic(n_races=40, seed=0):
    rng = np.random.default_rng(seed)
    sizes = rng.integers(5, 12, n_races)
    race = np.repeat(np.arange(n_races), sizes)
    score = rng.normal(0, 1, len(race))
    y = np.zeros(len(race))
    starts = np.r_[0, np.cumsum(sizes)[:-1]]
    y[starts + rng.integers(0, sizes)] = 1
    y[starts[0] + 1] = 1 if sizes[0] > 1 else 0  # 同着を 1 レース
    gid, n = mo.group_ids(race)
    return score, mo.targets(y, gid, n), gid, n


def test_gradient_matches_finite_difference():
    score, t, gid, n = _synthetic()
    g, h = mo.race_softmax_grad_hess(score, t, gid, n)
    total = lambda s: mo.race_nll(s, t, gid, n) * n  # noqa: E731  総和の損失
    eps = 1e-5
    for i in np.random.default_rng(1).choice(len(score), 25, replace=False):
        e = np.zeros_like(score)
        e[i] = eps
        fd_g = (total(score + e) - total(score - e)) / (2 * eps)
        # 対角ヘッセ行列 = 勾配の差分
        gp, _ = mo.race_softmax_grad_hess(score + e, t, gid, n)
        gm, _ = mo.race_softmax_grad_hess(score - e, t, gid, n)
        fd_h = (gp[i] - gm[i]) / (2 * eps)
        assert g[i] == pytest.approx(fd_g, abs=1e-6)
        assert h[i] == pytest.approx(fd_h, rel=1e-5, abs=1e-8)


def test_gradient_sums_to_zero_and_shift_invariant():
    score, t, gid, n = _synthetic(seed=2)
    g, _ = mo.race_softmax_grad_hess(score, t, gid, n)
    np.testing.assert_allclose(np.bincount(gid, weights=g, minlength=n), 0, atol=1e-12)
    shift = np.random.default_rng(3).normal(0, 5, n)[gid]  # レース内の定数は損失を変えない
    assert mo.race_nll(score + shift, t, gid, n) == pytest.approx(mo.race_nll(score, t, gid, n))


def test_lightgbm_offset_learns_residual():
    lgb = pytest.importorskip("lightgbm")
    rng = np.random.default_rng(4)
    n_races, size = 1500, 10
    race = np.repeat(np.arange(n_races), size)
    a = rng.normal(0, 1, len(race))          # 市場が知る強さ
    x = rng.normal(0, 1, len(race))          # 市場が知らない特徴
    gid, n = mo.group_ids(race)
    p_true = mo.softmax_by_group(a + 0.8 * x, gid, n)
    u = rng.random(n_races)[gid]
    c = np.zeros(len(race))
    for r in range(n_races):
        sl = slice(r * size, (r + 1) * size)
        c[sl] = np.cumsum(p_true[sl])
    y = ((c - p_true <= u) & (u < c)).astype(float)
    obj = mo.RaceSoftmax(race, y)
    ds = lgb.Dataset(x[:, None], label=y, init_score=a)
    b = lgb.train({"objective": obj.objective, "metric": "None", "verbose": -1, "learning_rate": 0.1,
                   "num_leaves": 4, "min_data_in_leaf": 50}, ds, num_boost_round=100)
    f = b.predict(x[:, None], raw_score=True)
    assert obj.metric(a + f) < obj.metric(a) - 0.05
    # 学習した f は x と単調（傾き ≈ 0.8）
    assert np.corrcoef(f, x)[0, 1] > 0.9


def test_clogit_recovers_coefficients():
    rng = np.random.default_rng(5)
    n_races, size = 3000, 10
    race = np.repeat(np.arange(n_races), size)
    X = rng.normal(0, 1, (len(race), 2))
    gid, n = mo.group_ids(race)
    p = mo.softmax_by_group(X @ np.array([1.0, -0.5]), gid, n)
    y = np.zeros(len(race))
    for r in range(n_races):
        sl = slice(r * size, (r + 1) * size)
        y[r * size + rng.choice(size, p=p[sl])] = 1
    fit = mo.fit_clogit(X, mo.targets(y, gid, n), gid, n)
    np.testing.assert_allclose(fit["coef"], [1.0, -0.5], atol=4 * fit["se"].max())

"""単勝確率モデルの評価。データソースに依存しない。

入力は 1 行 1 頭の long DataFrame。列名は引数で変えられる（既定: ``race_id``, ``date``, ``y``）。
``y`` は 1 = 1 着、0 = それ以外。同着（1 レースに y=1 が複数）は的中を等分した目標
t_i = y_i / Σy を使う（対数損失・Brier・較正）。賭けの払戻しだけは y をそのまま使う。
確率列はレース内で和 1 を仮定する（``renormalize`` で揃える）。確率が NaN の行は除く。

主な API:

    renormalize(df, p, race="race_id") -> Series
    race_scores(df, p, y="y", race="race_id") -> DataFrame       # レースごとの logloss, brier, top1
    summary(df, p, ...) -> dict                                   # logloss（主指標）, brier, top1, ece, n_races
    calibration_table(df, p, bins=10, strategy="quantile") -> DataFrame
    delta_logloss(df, p_model, p_ref, cluster="race_id", n_boot=2000, seed=0) -> dict
    fit_benter(df, cols, ...) -> dict ; benter_predict(df, coef, cols) -> Series
    benter_two_stage(train, test, model, market, ...) -> dict     # α, β と結合 vs 市場の ΔlogLoss
    shuffle_within_race(df, p, rng) -> Series ; placebo(df, make_p, p_ref, n_rep) -> DataFrame
    simulate_bets(df, p, decision_odds=..., payout_odds=..., threshold=1.0) -> dict
    time_split(dates, train_end, valid_end=None, test_end=None) -> Series

ΔlogLoss は「モデル − 参照」。負ならモデルが良い。CI はクラスタ（既定はレース、
同日のレースの相関を見るなら ``cluster="date"``）のブートストラップのパーセンタイル区間。
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
import pandas as pd
from scipy import optimize, stats

EPS = 1e-15  # log(0) を避ける下限


# --- 共通 -----------------------------------------------------------------

def renormalize(df: pd.DataFrame, p: str, race: str = "race_id") -> pd.Series:
    """レース内で和 1 に正規化する（NaN は除いて正規化、NaN のまま残す）。"""
    return df[p] / df.groupby(race)[p].transform("sum")


def _clean(df, cols, y, race):
    """確率が NaN の行を除く。勝ち馬の確率が NaN なら評価できないので例外。"""
    d = df.dropna(subset=list(cols))
    lost = df.index.difference(d.index)
    if len(lost) and (df.loc[lost, y] > 0).any():
        raise ValueError("勝ち馬の確率が NaN の行がある")
    tot = d.groupby(race)[y].transform("sum")
    d = d[tot > 0]  # 勝ち馬のいないレース（不成立など）は除く
    return d.assign(_t=d[y] / tot[tot > 0])


def cluster_bootstrap(num, den, n_boot: int = 2000, seed: int = 0, chunk: int = 200) -> np.ndarray:
    """クラスタ単位の比推定量 Σnum/Σden のブートストラップ分布。"""
    num, den = np.asarray(num, float), np.asarray(den, float)
    rng = np.random.default_rng(seed)
    out = []
    for start in range(0, n_boot, chunk):
        idx = rng.integers(0, len(num), size=(min(chunk, n_boot - start), len(num)))
        out.append(num[idx].sum(1) / den[idx].sum(1))
    return np.concatenate(out)


def _ci(boot, level):
    a = (1 - level) / 2
    return float(np.quantile(boot, a)), float(np.quantile(boot, 1 - a))


# --- 指標 -----------------------------------------------------------------

def race_scores(df: pd.DataFrame, p: str, y: str = "y", race: str = "race_id") -> pd.DataFrame:
    """レースごとの条件付き対数損失 −Σt·log p、多クラス Brier Σ(p−t)²、top1 的中。"""
    d = _clean(df, [p], y, race)
    pv, t = d[p].to_numpy(float), d["_t"].to_numpy()
    g = d.assign(_ll=-t * np.log(np.clip(pv, EPS, None)), _br=(pv - t) ** 2).groupby(race)
    top = d.loc[g[p].idxmax()]
    return pd.DataFrame({
        "logloss": g["_ll"].sum(),
        "brier": g["_br"].sum(),
        "top1": (top.set_index(race)[y] > 0).astype(float),
        "n_horses": g.size(),
    })


def calibration_table(df: pd.DataFrame, p: str, y: str = "y", race: str = "race_id",
                      bins: int = 10, strategy: str = "quantile") -> pd.DataFrame:
    """馬単位の較正表。strategy="quantile"（等頻度）か "uniform"（等幅）。"""
    d = _clean(df, [p], y, race)
    if strategy == "quantile":
        b = pd.qcut(d[p].rank(method="first"), bins, labels=False)
    else:
        b = pd.cut(d[p], np.linspace(0, 1, bins + 1), labels=False, include_lowest=True)
    g = d.groupby(b)
    return pd.DataFrame({"n": g.size(), "p_lo": g[p].min(), "p_hi": g[p].max(),
                         "p_mean": g[p].mean(), "win_rate": g["_t"].mean()}).rename_axis("bin")


def ece(df: pd.DataFrame, p: str, **kw) -> float:
    """Expected Calibration Error = Σ (n_b/N)·|平均p − 勝率|。"""
    c = calibration_table(df, p, **kw)
    return float((c["n"] * (c["p_mean"] - c["win_rate"]).abs()).sum() / c["n"].sum())


def summary(df: pd.DataFrame, p: str, y: str = "y", race: str = "race_id", bins: int = 10) -> dict:
    s = race_scores(df, p, y, race)
    return {"logloss": float(s["logloss"].mean()), "brier": float(s["brier"].mean()),
            "top1": float(s["top1"].mean()), "ece": ece(df, p, y=y, race=race, bins=bins),
            "n_races": len(s)}


def delta_logloss(df: pd.DataFrame, p_model: str, p_ref: str, y: str = "y", race: str = "race_id",
                  cluster: str | None = None, n_boot: int = 2000, seed: int = 0,
                  level: float = 0.95) -> dict:
    """同じレースでの ΔlogLoss = logloss(model) − logloss(ref)。負ならモデルが良い。

    cluster: ブートストラップの単位の列（None ならレース）。p_value はブートストラップ SE による
    正規近似の両側検定（H0: Δ=0）。
    """
    d = _clean(df, [p_model, p_ref], y, race)
    a, b = race_scores(d, p_model, y, race), race_scores(d, p_ref, y, race)
    diff = (a["logloss"] - b["logloss"]).rename("d").to_frame()
    if cluster and cluster != race:
        diff["c"] = d.groupby(race)[cluster].first()
    else:
        diff["c"] = diff.index
    g = diff.groupby("c")["d"]
    boot = cluster_bootstrap(g.sum(), g.size(), n_boot, seed)
    delta, se = float(diff["d"].mean()), float(boot.std(ddof=1))
    return {"delta": delta, "ci": _ci(boot, level), "se": se,
            "p_value": float(2 * stats.norm.sf(abs(delta) / se)) if se > 0 else float("nan"),
            "logloss_model": float(a["logloss"].mean()), "logloss_ref": float(b["logloss"].mean()),
            "n_races": len(diff), "n_clusters": g.ngroups}


# --- Benter の 2 段階（条件付きロジット） ---------------------------------

def _clogit_parts(d, cols, race):
    X = np.log(np.clip(d[list(cols)].to_numpy(float), EPS, None))
    gid, _ = pd.factorize(d[race])
    return X, d["_t"].to_numpy(), gid, int(gid.max()) + 1


def _clogit_probs(X, beta, gid, n):
    eta = X @ beta
    m = np.full(n, -np.inf)
    np.maximum.at(m, gid, eta)
    e = np.exp(eta - m[gid])
    return e / np.bincount(gid, weights=e, minlength=n)[gid]


def fit_benter(df: pd.DataFrame, cols: Sequence[str], y: str = "y", race: str = "race_id") -> dict:
    """p_i ∝ exp(Σ_j β_j·log p_ij) をレース単位の最尤で当てはめる。

    返り値: coef（cols 順）、se（解析的ヘッセ行列の逆から、レース独立を仮定）、train_logloss。
    """
    d = _clean(df, cols, y, race)
    X, t, gid, n = _clogit_parts(d, cols, race)

    def nll(beta):
        q = _clogit_probs(X, beta, gid, n)
        grad = ((q - t)[:, None] * X).sum(0) / n
        return -(t * np.log(np.clip(q, EPS, None))).sum() / n, grad

    res = optimize.minimize(nll, np.ones(len(cols)) / len(cols), jac=True, method="L-BFGS-B")
    q = _clogit_probs(X, res.x, gid, n)
    # ヘッセ行列 = Σ_r Cov_q(x)
    mean = np.stack([np.bincount(gid, weights=q * X[:, j], minlength=n) for j in range(X.shape[1])], 1)
    Xc = X - mean[gid]
    H = (q[:, None, None] * Xc[:, :, None] * Xc[:, None, :]).sum(0)
    se = np.sqrt(np.diag(np.linalg.pinv(H)))
    return {"coef": dict(zip(cols, res.x.tolist())), "se": dict(zip(cols, se.tolist())),
            "train_logloss": float(res.fun), "n_races": n, "converged": bool(res.success)}


def benter_predict(df: pd.DataFrame, coef: dict, race: str = "race_id") -> pd.Series:
    """fit_benter の coef で結合確率を出す（確率が NaN の行は NaN）。"""
    cols = list(coef)
    d = df.dropna(subset=cols)
    X = np.log(np.clip(d[cols].to_numpy(float), EPS, None))
    gid, _ = pd.factorize(d[race])
    q = _clogit_probs(X, np.array(list(coef.values())), gid, int(gid.max()) + 1)
    return pd.Series(q, index=d.index, name="p_benter").reindex(df.index)


def benter_two_stage(train: pd.DataFrame, test: pd.DataFrame, model: str, market: str,
                     y: str = "y", race: str = "race_id", **delta_kw) -> dict:
    """train で α（model）, β（market）を当てはめ、test で結合 vs 市場の ΔlogLoss を測る。

    α≈0（CI が 0 を含む）なら、モデルは市場に情報を足していない。
    """
    fit = fit_benter(train, [model, market], y, race)
    t = test.assign(_p_comb=benter_predict(test, fit["coef"], race))
    return {"alpha": fit["coef"][model], "beta": fit["coef"][market],
            "alpha_se": fit["se"][model], "beta_se": fit["se"][market], "fit": fit,
            "test": delta_logloss(t, "_p_comb", market, y, race, **delta_kw),
            "p_test": t["_p_comb"]}


# --- プラセボ ---------------------------------------------------------------

def shuffle_within_race(df: pd.DataFrame, p: str, rng: np.random.Generator,
                        race: str = "race_id") -> pd.Series:
    """レース内で確率を並べ替える（馬との対応だけ壊す。和は 1 のまま）。"""
    key = pd.Series(rng.random(len(df)), index=df.index)
    order = df.assign(_k=key).sort_values([race, "_k"]).index
    srt = df.sort_values([race, p]).index  # 同じレース順で並ぶ
    out = pd.Series(df.loc[srt, p].to_numpy(), index=order)
    return out.reindex(df.index)


def placebo(df: pd.DataFrame, make_p: Callable[[pd.DataFrame, np.random.Generator], pd.Series],
            p_ref: str, n_rep: int = 20, seed: int = 0, y: str = "y", race: str = "race_id",
            n_boot: int = 200, **delta_kw) -> pd.DataFrame:
    """make_p(df, rng) が返す偽の確率で ΔlogLoss を n_rep 回測る。

    例: ``lambda d, r: shuffle_within_race(d, "p_model", r)``。時間をずらしたラベルで学習した
    モデルなど、学習を含む偽モデルも同じ形の callable にして渡す。
    """
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_rep):
        d = df.assign(_p_placebo=make_p(df, rng))
        r = delta_logloss(d, "_p_placebo", p_ref, y, race, n_boot=n_boot, seed=seed + i, **delta_kw)
        rows.append({"rep": i, "delta": r["delta"], "ci_lo": r["ci"][0], "ci_hi": r["ci"][1]})
    return pd.DataFrame(rows)


# --- 賭けのシミュレーション -------------------------------------------------

def simulate_bets(df: pd.DataFrame, p: str, *, decision_odds: str, payout_odds: str,
                  threshold: float = 1.0, stake: float = 1.0, y: str = "y", race: str = "race_id",
                  order: Sequence[str] = ("date",), cluster: str | None = None,
                  n_boot: int = 2000, seed: int = 0, level: float = 0.95) -> dict:
    """単勝の均等賭け。p·decision_odds > threshold の馬を買い、payout_odds で払い戻す。

    - decision_odds: 購入判断に使うオッズ（締切前の時点で知り得るもの）。
    - payout_odds: 払戻しに使うオッズ（確定オッズ、同着なら公式の払戻金/100 を渡す）。
      同着の勝ち馬はそれぞれ y=1 として payout_odds で払い戻す。
    - 判断時に買ったが payout_odds が NaN（発走取消など）の馬は返還扱いで除き、n_void に数える。
    ROI = 払戻計/賭け金計 − 1（控除率込み）。CI はクラスタ（既定はレース）ブートストラップ。
    max_drawdown は order 順の累積損益の山から谷の最大幅（賭け金単位）。
    """
    if decision_odds == payout_odds:
        import warnings
        warnings.warn("decision_odds と payout_odds が同じ列。確定オッズで判断するとリークになる")
    bet = df[(df[p] * df[decision_odds] > threshold)]
    n_void = int(bet[payout_odds].isna().sum())
    bet = bet.dropna(subset=[payout_odds])
    keys = [c for c in (*order, race) if c in bet.columns]
    bet = bet.sort_values(keys).assign(
        _stake=stake, _ret=lambda b: stake * b[payout_odds] * (b[y] > 0))
    if bet.empty:
        return {"n_bets": 0, "n_void": n_void}
    profit = (bet["_ret"] - bet["_stake"]).cumsum()
    dd = float((np.maximum.accumulate(np.r_[0.0, profit.to_numpy()])[1:] - profit).max())
    g = bet.groupby(cluster or race)
    boot = cluster_bootstrap(g["_ret"].sum(), g["_stake"].sum(), n_boot, seed) - 1
    roi = float(bet["_ret"].sum() / bet["_stake"].sum() - 1)
    return {"n_bets": len(bet), "n_void": n_void, "n_hits": int((bet[y] > 0).sum()),
            "hit_rate": float((bet[y] > 0).mean()), "stake": float(bet["_stake"].sum()),
            "return": float(bet["_ret"].sum()), "roi": roi, "roi_ci": _ci(boot, level),
            "max_drawdown": dd, "bets": bet.drop(columns=["_stake", "_ret"])}


# --- 時系列分割 -------------------------------------------------------------

def time_split(dates: pd.Series, train_end, valid_end=None, test_end=None) -> pd.Series:
    """日付の境界で "train" / "valid" / "test" を返す（ランダム分割はしない）。

    train: date < train_end、valid: train_end ≤ date < valid_end、
    test: valid_end（valid_end が None なら train_end）≤ date < test_end。範囲外は NaN。
    """
    d = pd.to_datetime(dates)
    te, ve = pd.Timestamp(train_end), pd.Timestamp(valid_end) if valid_end is not None else None
    out = pd.Series(np.nan, index=dates.index, dtype=object)
    out[d < te] = "train"
    test_start = te
    if ve is not None:
        out[(d >= te) & (d < ve)] = "valid"
        test_start = ve
    end = pd.Timestamp(test_end) if test_end is not None else pd.Timestamp.max
    out[(d >= test_start) & (d < end)] = "test"
    return out

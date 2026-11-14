"""市場をオフセットにした学習の部品（レース内 softmax = 条件付きロジット）。

- ``RaceSoftmax``: LightGBM の自作目的関数と評価関数。スコア s_i（init_score = log p_market を含む）を
  レース内で softmax し、損失 L = Σ_races −Σ_i t_i log p_i（t = y/Σy、同着は等分）。
  勾配 g_i = p_i − t_i、ヘッセ行列は対角 h_i = p_i(1 − p_i)（Newton の近似。真の行列は p_i δ_ij − p_i p_j）。
  LightGBM 4.x では fobj / feval に渡る preds は init_score を含む。predict() は init_score を含まないので、
  予測は ``log p_market + booster.predict(raw_score=True)`` を softmax する。
- ``fit_clogit``: 線形の条件付きロジット（Bolton–Chapman、Benter の第 1 段）を L2 つきで当てはめる。
- ``design_matrix``: 標準化・欠損の補完と欠損指示変数（平均・SD・中央値は学習期間だけから）。

勝ち馬のいないレース（Σy = 0）は渡す前に除くこと（t が定義できない）。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import optimize

EPS = 1e-15


def group_ids(race: pd.Series | np.ndarray) -> tuple[np.ndarray, int]:
    gid, uniq = pd.factorize(np.asarray(race))
    return gid.astype(np.int64), len(uniq)


def softmax_by_group(score: np.ndarray, gid: np.ndarray, n: int) -> np.ndarray:
    m = np.full(n, -np.inf)
    np.maximum.at(m, gid, score)
    e = np.exp(score - m[gid])
    return e / np.bincount(gid, weights=e, minlength=n)[gid]


def targets(y: np.ndarray, gid: np.ndarray, n: int) -> np.ndarray:
    y = np.asarray(y, float)
    tot = np.bincount(gid, weights=y, minlength=n)
    if (tot <= 0).any():
        raise ValueError("勝ち馬のいないレースがある（先に除く）")
    return y / tot[gid]


def race_nll(score: np.ndarray, t: np.ndarray, gid: np.ndarray, n: int) -> float:
    """レース平均の条件付き対数損失。"""
    p = softmax_by_group(np.asarray(score, float), gid, n)
    return float(-(t * np.log(np.clip(p, EPS, None))).sum() / n)


def race_softmax_grad_hess(score: np.ndarray, t: np.ndarray, gid: np.ndarray, n: int):
    """L = Σ_races −Σ t log softmax(score) の勾配と対角ヘッセ行列（レースで割らない総和の損失）。"""
    p = softmax_by_group(np.asarray(score, float), gid, n)
    return p - t, np.maximum(p * (1.0 - p), 1e-12)


@dataclass
class RaceSoftmax:
    """1 つの lgb.Dataset 用の目的関数・評価関数。行の並びは Dataset と同じであること。"""

    race: np.ndarray
    y: np.ndarray
    weight: np.ndarray | None = None  # 行ごとの重み（同じレースの行は同じ値にする）。勾配・ヘッセ行列に掛ける

    def __post_init__(self):
        self.gid, self.n = group_ids(self.race)
        self.t = targets(self.y, self.gid, self.n)

    def objective(self, preds, _dataset):
        g, h = race_softmax_grad_hess(preds, self.t, self.gid, self.n)
        if self.weight is not None:
            g, h = g * self.weight, h * self.weight
        return g, h

    def metric(self, preds):
        return race_nll(preds, self.t, self.gid, self.n)


def make_feval(evaluators: dict[int, RaceSoftmax]):
    """id(Dataset) → RaceSoftmax の辞書から feval を作る（valid ごとに別のレース構造を持つため）。"""

    def feval(preds, dataset):
        return "race_logloss", evaluators[id(dataset)].metric(preds), False

    return feval


# --- 線形の条件付きロジット ---------------------------------------------------

def fit_clogit(X: np.ndarray, t: np.ndarray, gid: np.ndarray, n: int, l2: float = 0.0,
               maxiter: int = 1000) -> dict:
    """p ∝ exp(Xβ) をレース平均の損失 + (l2/2)·||β||² 最小で当てはめる。切片はない（レース内で消える）。

    se はペナルティなしのヘッセ行列（Σ_r Cov_p(x)）の逆から（レース独立を仮定、参考値）。
    """
    X = np.asarray(X, float)

    def f(beta):
        eta = X @ beta
        p = softmax_by_group(eta, gid, n)
        loss = -(t * np.log(np.clip(p, EPS, None))).sum() / n + 0.5 * l2 * beta @ beta
        grad = X.T @ (p - t) / n + l2 * beta
        return loss, grad

    res = optimize.minimize(f, np.zeros(X.shape[1]), jac=True, method="L-BFGS-B",
                            options={"maxiter": maxiter})
    p = softmax_by_group(X @ res.x, gid, n)
    mean = np.stack([np.bincount(gid, weights=p * X[:, j], minlength=n) for j in range(X.shape[1])], 1)
    Xc = X - mean[gid]
    H = (Xc * p[:, None]).T @ Xc
    se = np.sqrt(np.clip(np.diag(np.linalg.pinv(H)), 0, None))
    return {"coef": res.x, "se": se, "loss": float(res.fun), "converged": bool(res.success),
            "n_iter": int(res.nit)}


@dataclass
class Standardizer:
    """学習期間の統計で標準化する。欠損は中央値で埋め、欠損のあった列には指示変数を足す。"""

    cols: list[str]
    log1p: tuple[str, ...] = ()
    clip: float = 5.0

    def fit(self, df: pd.DataFrame) -> "Standardizer":
        x = self._raw(df)
        self.median_ = x.median()
        self.na_cols_ = [c for c in self.cols if x[c].isna().any()]
        xf = x.fillna(self.median_)
        self.mean_, self.sd_ = xf.mean(), xf.std(ddof=0).replace(0, 1.0)
        return self

    def _raw(self, df):
        x = df[self.cols].astype(float).copy()
        for c in self.log1p:
            x[c] = np.log1p(x[c].clip(lower=0))
        return x

    def transform(self, df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
        x = self._raw(df)
        na = x[self.na_cols_].isna().astype(float).to_numpy()
        z = ((x.fillna(self.median_) - self.mean_) / self.sd_).clip(-self.clip, self.clip).to_numpy()
        return np.hstack([z, na]), [*self.cols, *[f"{c}_isna" for c in self.na_cols_]]


# --- 上位 3 着の Plackett-Luce（探索 08） ----------------------------------------------

@dataclass
class RacePL:
    """1 着は RaceSoftmax と同じ（同着は等分）。2・3 着は、残った馬の中で exp(γ_k·score) に比例して選ばれる。

    L = Σ_races [ −Σ t log softmax(score) + Σ_{k=2,3} w_k ( −γ_k s_{c_k} + log Σ_{j∈R_k} exp(γ_k s_j) ) ]
    R_k は 1〜k−1 着の馬を除いた出走馬（着順のない馬 = 中止・失格も残る）。k 着の馬がちょうど 1 頭のレースだけ
    （それより前の着順も 1 頭ずつ）その段を足す。勾配は w_k γ_k (p^k − 1[c_k])、対角ヘッセ行列は w_k γ_k² p^k (1 − p^k)。
    """

    race: np.ndarray
    y: np.ndarray
    finish_pos: np.ndarray
    gammas: tuple = (1.0, 1.0, 1.0)
    weights: tuple = (1.0, 1.0, 1.0)

    def __post_init__(self):
        self.gid, self.n = group_ids(self.race)
        self.t = targets(self.y, self.gid, self.n)
        fp = np.nan_to_num(np.asarray(self.finish_pos, float), nan=99.0)
        self.stages = []
        ok = np.ones(self.n, bool)
        for k in (1, 2, 3):
            cnt = np.bincount(self.gid, weights=(fp == k).astype(float), minlength=self.n)
            ok &= cnt == 1
            if k == 1:
                continue
            races_ok = ok[self.gid]
            rem = races_ok & (fp >= k)              # 残った馬
            chosen = races_ok & (fp == k)
            self.stages.append((k, rem, chosen))

    def _stage_p(self, score, rem, g):
        s = np.where(rem, g * score, -np.inf)
        m = np.full(self.n, -np.inf)
        np.maximum.at(m, self.gid, s)
        m = np.where(np.isfinite(m), m, 0.0)
        e = np.where(rem, np.exp(s - m[self.gid]), 0.0)
        den = np.bincount(self.gid, weights=e, minlength=self.n)
        return np.where(rem, e / np.where(den > 0, den, 1.0)[self.gid], 0.0)

    def objective(self, preds, _dataset):
        g, h = race_softmax_grad_hess(preds, self.t, self.gid, self.n)
        for (k, rem, chosen) in self.stages:
            gk, wk = self.gammas[k - 1], self.weights[k - 1]
            p = self._stage_p(preds, rem, gk)
            g = g + wk * gk * (p - chosen)
            h = h + wk * gk * gk * p * (1 - p)
        return g, np.maximum(h, 1e-12)

    def metric(self, preds):
        return race_nll(preds, self.t, self.gid, self.n)

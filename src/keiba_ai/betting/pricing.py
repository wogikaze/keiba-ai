"""判断に使うオッズの予測。

- 価格モデル（price）: 過去分の 10 分前オッズがない券種（ワイド・馬単・3連複・3連単）で、
  10 分前の単勝オッズから作った市場の組合せ確率 q（combos.race_probs、γ は市場で当てはめる）から確定オッズを予測する。
  log o = a + b·log q + c·(log q)^2 + d·log n（n は頭数）。
- オッズ変化のモデル（drift）: 10 分前のオッズから確定オッズを予測する（P3）。
  log(o_final / o_10) = 線形（log o_10、(log o_10)^2、log(o_10 / o_30)、log n）。
どちらも train で最小二乗で当てはめる。決定時刻より後の情報は入力にしない（確定オッズは目的変数だけ）。
"""

from __future__ import annotations

import numpy as np


def _price_X(logq, n):
    logq = np.asarray(logq, float)
    return np.column_stack([np.ones_like(logq), logq, logq ** 2, np.log(np.broadcast_to(np.asarray(n, float), np.shape(logq)))])


def _drift_X(log_o, log_o30, n):
    log_o = np.asarray(log_o, float)
    mom = log_o - np.asarray(log_o30, float)
    mom = np.where(np.isfinite(mom), mom, 0.0)
    return np.column_stack([np.ones_like(log_o), log_o, log_o ** 2, mom, np.log(np.broadcast_to(np.asarray(n, float), np.shape(log_o)))])


def _ols(X, y):
    ok = np.all(np.isfinite(X), axis=1) & np.isfinite(y)
    beta, *_ = np.linalg.lstsq(X[ok], y[ok], rcond=None)
    resid = y[ok] - X[ok] @ beta
    return beta, {"n": int(ok.sum()), "rmse": float(np.sqrt(np.mean(resid ** 2))),
                  "r2": float(1 - resid.var() / y[ok].var()), "mae": float(np.mean(np.abs(resid)))}


def fit_price(q, n, odds_final) -> dict:
    beta, st = _ols(_price_X(np.log(np.clip(q, 1e-12, None)), n), np.log(np.asarray(odds_final, float)))
    return {"beta": beta.tolist(), **st}


def predict_price(model: dict, q, n) -> np.ndarray:
    X = _price_X(np.log(np.clip(q, 1e-12, None)), n)
    return np.maximum(np.exp(X @ np.asarray(model["beta"])), 1.0)


def fit_drift(o10, o30, n, o_final) -> dict:
    lo = np.log(np.asarray(o10, float))
    beta, st = _ols(_drift_X(lo, np.log(np.asarray(o30, float)), n), np.log(np.asarray(o_final, float)) - lo)
    return {"beta": beta.tolist(), **st}


def predict_drift(model: dict, o10, o30, n) -> np.ndarray:
    lo = np.log(np.asarray(o10, float))
    X = _drift_X(lo, np.log(np.asarray(o30, float)), n)
    return np.maximum(np.exp(lo + X @ np.asarray(model["beta"])), 1.0)

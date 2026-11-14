"""単勝の勝率から、連勝式（馬連・ワイド・馬単・3連複・3連単）と複勝の確率を作る。

割引つき Harville（Benter 1994、Lo & Bacon-Shone 2008 の簡略版）:

    P(i 1 着)                = p_i
    P(j 2 着 | i 1 着)       = s2_j / (1 − s2_i)          s2 = p^γ2 を正規化
    P(k 3 着 | i, j)         = s3_k / (1 − s3_i − s3_j)   s3 = p^γ3 を正規化

γ = 1 が素の Harville。γ < 1 は 2・3 着で人気薄が来やすいことを表す。
γ は実際の 1〜3 着の並びの尤度で当てはめる（fit_gammas）。

組番のコード（int）は払戻（payouts.combination）の文字列と同じ並び:
2 頭は a*100+b、3 頭は a*10000+b*100+c。馬連・ワイド・3連複は馬番の小さい順、馬単・3連単は着順。
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

BET_TYPES = ("win", "place", "quinella", "wide", "exacta", "trio", "trifecta")
EXCLUSIVE = {"win": True, "place": False, "quinella": True, "wide": False, "exacta": True, "trio": True,
             "trifecta": True}
N_LEGS = {"win": 1, "place": 1, "quinella": 2, "wide": 2, "exacta": 2, "trio": 3, "trifecta": 3}
EPS = 1e-12


def combo_code(*legs) -> np.ndarray:
    """馬番の配列（1 着、2 着、…の順）から組番のコード。"""
    out = np.zeros_like(np.asarray(legs[0]), dtype=np.int64)
    for a in legs:
        out = out * 100 + np.asarray(a, dtype=np.int64)
    return out


def code_from_str(s: str) -> int:
    return int(s)


def _strength(p: np.ndarray, g: float) -> np.ndarray:
    s = np.power(np.clip(p, EPS, None), g)
    return s / s.sum()


def tensors(p: np.ndarray, g2: float = 1.0, g3: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """馬単の確率 E[i, j] と 3連単の確率 T[i, j, k]（同じ馬を含む要素は 0）。"""
    p = np.asarray(p, dtype=float)
    p = p / p.sum()
    n = len(p)
    s2, s3 = _strength(p, g2), _strength(p, g3)
    eye = np.eye(n, dtype=bool)
    E = p[:, None] * s2[None, :] / np.clip(1.0 - s2[:, None], EPS, None)
    E[eye] = 0.0
    den = np.clip(1.0 - s3[:, None] - s3[None, :], EPS, None)  # [i, j]
    T = E[:, :, None] * s3[None, None, :] / den[:, :, None]
    idx = np.arange(n)
    T[idx, :, idx] = 0.0
    T[:, idx, idx] = 0.0
    T[eye] = 0.0
    return E, T


def race_probs(umaban: np.ndarray, p: np.ndarray, g2: float = 1.0, g3: float = 1.0,
               place_k: int = 3, types=BET_TYPES) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """1 レースの券種ごとの (組番コード, 確率)。place_k は複勝の払戻が何着までか（2 か 3）。"""
    u = np.asarray(umaban, dtype=np.int64)
    n = len(u)
    E, T = tensors(p, g2, g3)
    pw = np.asarray(p, dtype=float) / np.sum(p)
    out: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    i2, j2 = np.triu_indices(n, 1)
    if "win" in types:
        out["win"] = (u.copy(), pw)
    if "place" in types:
        top2 = pw + E.sum(axis=0)
        top3 = top2 + T.sum(axis=(0, 1))
        out["place"] = (u.copy(), top2 if place_k == 2 else top3)
    if "exacta" in types:
        ii, jj = np.nonzero(~np.eye(n, dtype=bool))
        out["exacta"] = (combo_code(u[ii], u[jj]), E[ii, jj])
    if "quinella" in types:
        a, b = _sorted_pair(u, i2, j2)
        out["quinella"] = (combo_code(a, b), E[i2, j2] + E[j2, i2])
    if "wide" in types or "trio" in types:
        # 3 頭が上位 3 着に入る確率（順不同）
        S = T + T.transpose(0, 2, 1) + T.transpose(1, 0, 2) + T.transpose(1, 2, 0) + T.transpose(2, 0, 1) + \
            T.transpose(2, 1, 0)
        if "trio" in types:
            ii, jj, kk = _triples(n)
            uu = np.sort(np.stack([u[ii], u[jj], u[kk]], 1), axis=1)
            out["trio"] = (combo_code(uu[:, 0], uu[:, 1], uu[:, 2]), S[ii, jj, kk])
        if "wide" in types:
            # i と j がともに 3 着以内: Σ_k S[i, j, k]（S は i, j, k が全部違うときだけ非 0）
            W = S.sum(axis=2)
            a, b = _sorted_pair(u, i2, j2)
            out["wide"] = (combo_code(a, b), W[i2, j2])
    if "trifecta" in types:
        ii, jj, kk = np.nonzero(T > 0) if n >= 3 else (np.array([], int),) * 3
        mask = (ii != jj) & (jj != kk) & (ii != kk)
        ii, jj, kk = ii[mask], jj[mask], kk[mask]
        out["trifecta"] = (combo_code(u[ii], u[jj], u[kk]), T[ii, jj, kk])
    return out


def _sorted_pair(u, i, j):
    a, b = u[i], u[j]
    return np.minimum(a, b), np.maximum(a, b)


def _triples(n: int):
    if n < 3:
        z = np.array([], dtype=int)
        return z, z, z
    idx = np.array([(i, j, k) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n)])
    return idx[:, 0], idx[:, 1], idx[:, 2]


# --- γ の当てはめ ---------------------------------------------------------------

def _pad(groups: list[np.ndarray], n_max: int) -> np.ndarray:
    m = np.zeros((len(groups), n_max))
    for r, g in enumerate(groups):
        m[r, : len(g)] = g
    return m


def fit_gammas(ps: list[np.ndarray], first: list[int], second: list[int], third: list[int],
               bounds=(0.2, 2.0)) -> dict:
    """各レースの勝率 ps[r]（馬の並び）と、1〜3 着の馬の位置（ps[r] の添字）から γ2・γ3 を最尤で当てはめる。

    2 着の尤度 s2_{2着} / (1 − s2_{1着}) は γ2 だけ、3 着の尤度は γ3 だけに依存するので、別々に 1 次元で解く。
    """
    n_max = max(len(p) for p in ps)
    P = np.clip(_pad([np.asarray(p) / np.sum(p) for p in ps], n_max), 0.0, None)
    mask = _pad([np.ones(len(p)) for p in ps], n_max) > 0
    r = np.arange(len(ps))
    f, s, t = np.asarray(first), np.asarray(second), np.asarray(third)
    logP = np.log(np.where(mask, np.clip(P, EPS, None), 1.0))

    def strength(g):
        S = np.where(mask, np.exp(g * logP), 0.0)
        return S / S.sum(axis=1, keepdims=True)

    def nll2(g):
        S = strength(g)
        return -np.mean(np.log(S[r, s] + EPS) - np.log(np.clip(1 - S[r, f], EPS, None)))

    def nll3(g):
        S = strength(g)
        return -np.mean(np.log(S[r, t] + EPS) - np.log(np.clip(1 - S[r, f] - S[r, s], EPS, None)))

    o2 = minimize_scalar(nll2, bounds=bounds, method="bounded")
    o3 = minimize_scalar(nll3, bounds=bounds, method="bounded")
    return {"g2": float(o2.x), "g3": float(o3.x), "nll2": float(o2.fun), "nll3": float(o3.fun),
            "nll2_harville": float(nll2(1.0)), "nll3_harville": float(nll3(1.0)), "n_races": len(ps)}

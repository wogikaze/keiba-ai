"""ケリー基準の賭け比率。

- 排反な馬券（1 レースで当たりが 1 つだけ: 単勝・馬連・馬単・3連複・3連単）は、全部を同時に最適化する
  Smoczynski & Tomkins (2010) の方法。p_i は当たる確率、o_i は 1 円あたりの払戻（元本込み）。
- 排反でない馬券（複勝・ワイド）は 1 点ずつのケリー f = (p·o − 1) / (o − 1)。
返す比率は資金に対する割合（full Kelly）。分数ケリー λ や上限は呼ぶ側で掛ける。
"""

from __future__ import annotations

import numpy as np


def exclusive(p: np.ndarray, o: np.ndarray) -> np.ndarray:
    p, o = np.asarray(p, float), np.asarray(o, float)
    f = np.zeros_like(p)
    ok = (o > 1.0) & (p > 0)
    if not ok.any():
        return f
    idx = np.nonzero(ok)[0]
    e = p[idx] * o[idx]
    order = idx[np.argsort(-e, kind="stable")]
    sp = sinv = 0.0
    R = 1.0
    chosen = []
    for i in order:
        if p[i] * o[i] <= R:
            break
        sp += p[i]
        sinv += 1.0 / o[i]
        if sinv >= 1.0:  # 全部に張ると必ず勝つ（裁定）。ここで止める
            sp -= p[i]
            sinv -= 1.0 / o[i]
            break
        chosen.append(i)
        R = (1.0 - sp) / (1.0 - sinv)
    if chosen:
        c = np.array(chosen)
        f[c] = np.clip(p[c] - R / o[c], 0.0, None)
    return f


def independent(p: np.ndarray, o: np.ndarray) -> np.ndarray:
    p, o = np.asarray(p, float), np.asarray(o, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        f = (p * o - 1.0) / (o - 1.0)
    return np.where((o > 1.0) & np.isfinite(f), np.clip(f, 0.0, None), 0.0)

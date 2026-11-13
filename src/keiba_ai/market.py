"""オッズ → レース内の勝率（市場確率）。データソースに依存しない。

入力は 1 行 1 頭の long DataFrame（``race_id``, ``odds`` など。列名は引数で変えられる）。
オッズが欠損・0 以下の馬（取消・除外）は確率 NaN にし、残りで 1 に正規化する。

    implied_probs(df, method="proportional" | "power" | "shin" | "goto",
                  race="race_id", odds="odds") -> pd.Series   # df と同じ index
    overround(df, race="race_id", odds="odds") -> pd.Series   # レースごとの Σ1/odds

方法（q_i = 1/o_i、S = Σq_i）:

- proportional: p_i = q_i / S。
- power: p_i = q_i^k、Σp=1 となる k をレースごとに二分法で解く。
- shin: Shin (1992/1993) のインサイダーモデル。
  p_i = (sqrt(z² + 4(1−z) q_i²/S) − z) / (2(1−z))、Σp=1 となる z ∈ [0,1) を解く。
  PyPI の ``shin`` は Python 3.14 でビルドできなかったので自前実装。
- goto: goto_conversion (Goto 2024, MIT) の式を移植。
  se_i = sqrt(q_i(1−q_i)/q_i) = sqrt(1−q_i)、p_i = q_i − se_i·(S−1)/Σse。
  負の確率が出る・S≤1 のレースは proportional にフォールバック
  （PyPI 版 ``multiplicativeIfImprudentOdds=True`` と同じ）。
  PyPI の ``goto-conversion`` 4.x は無関係な画像・文章変換コード（PIL/torch の任意 import）を
  同梱しているため依存に入れず、式だけ移植した。

いずれも固定オッズ向けの補正で、パリミュチュエルの JRA で効くかは時系列分割で確かめてから使う。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

METHODS = ("proportional", "power", "shin", "goto")
_BISECT_ITERS = 100  # 二分法の反復回数（区間幅は 2^-100 倍になる）


def _groups(df: pd.DataFrame, race: str, odds: str):
    """有効な行のマスク、グループ番号、q=1/odds、グループ和の関数を返す。"""
    o = pd.to_numeric(df[odds], errors="coerce").to_numpy(dtype=float)
    valid = np.isfinite(o) & (o > 0)
    g, _ = pd.factorize(df[race].to_numpy()[valid])
    q = 1.0 / o[valid]
    n_groups = int(g.max()) + 1 if len(g) else 0

    def gsum(x):
        return np.bincount(g, weights=x, minlength=n_groups)

    return valid, g, q, gsum


def _bisect(f, lo, hi):
    """f(x) はグループごとの配列を返す単調減少関数。f(x)=0 をグループごとに解く。"""
    for _ in range(_BISECT_ITERS):
        mid = (lo + hi) / 2
        pos = f(mid) > 0
        lo = np.where(pos, mid, lo)
        hi = np.where(pos, hi, mid)
    return (lo + hi) / 2


def _power(q, g, gsum):
    # Σ q^k は k について単調減少（q<1）。q≥1（元返し 1.0 倍以下）があっても上限で止まる。
    n = len(gsum(np.zeros_like(q)))
    k = _bisect(lambda k: gsum(q ** k[g]) - 1.0, np.full(n, 1e-6), np.full(n, 100.0))
    return q ** k[g]


def _shin(q, g, gsum):
    S = gsum(q)

    def p_of(z):
        zg = z[g]
        return (np.sqrt(zg**2 + 4 * (1 - zg) * q**2 / S[g]) - zg) / (2 * (1 - zg))

    z = _bisect(lambda z: gsum(p_of(z)) - 1.0, np.zeros(len(S)), np.full(len(S), 1 - 1e-12))
    z = np.where(S > 1, z, 0.0)  # 控除がないレースは z=0（後段の正規化で proportional と同じ）
    return p_of(z)


def _goto(q, g, gsum):
    S = gsum(q)
    se = np.sqrt(np.clip(1 - q, 0, None))
    p = q - se * ((S - 1) / gsum(se))[g]
    bad = (gsum((p <= 0).astype(float)) > 0) | (S <= 1)
    return np.where(bad[g], q, p)  # bad なレースは q のまま → 正規化で proportional


def implied_probs(
    df: pd.DataFrame, method: str = "proportional", race: str = "race_id", odds: str = "odds"
) -> pd.Series:
    """オッズからレース内の勝率を返す。無効なオッズの行は NaN。"""
    if method not in METHODS:
        raise ValueError(f"method は {METHODS} のいずれか: {method!r}")
    valid, g, q, gsum = _groups(df, race, odds)
    p = {"proportional": lambda: q, "power": lambda: _power(q, g, gsum),
         "shin": lambda: _shin(q, g, gsum), "goto": lambda: _goto(q, g, gsum)}[method]()
    p = p / gsum(p)[g]  # 数値誤差と 1 頭立て・フォールバックをまとめて正規化
    out = np.full(len(df), np.nan)
    out[valid] = p
    return pd.Series(out, index=df.index, name=f"p_{method}")


def overround(df: pd.DataFrame, race: str = "race_id", odds: str = "odds") -> pd.Series:
    """レースごとの Σ1/odds（JRA 単勝なら控除率 20% で約 1.25）。"""
    o = pd.to_numeric(df[odds], errors="coerce")
    q = (1.0 / o.where(o > 0)).rename("overround")
    return q.groupby(df[race]).sum(min_count=1)

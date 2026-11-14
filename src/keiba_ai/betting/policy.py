"""賭けの方針（ADR 0004 の P1〜P3）、資金のシミュレーション、賭けの成績、賭け方のプラセボ。

入力は「候補」の表（pandas、1 行 = 1 レースの 1 組番）。列:

- ``race_idx``: 発走順に並べたレースの番号（資金のシミュレーションはこの順に進む）
- ``date``（開催日、ブートストラップの単位）、``year``
- ``p``: モデルの当たる確率、``o``: 判断に使うオッズ（1 円あたりの払戻、元本込み）
- ``f_full``: full Kelly の比率（レース内で同時に計算済み。候補を作る側で kelly.exclusive / independent）
- ``pay``: 実際の払戻（1 円あたり、HR の払戻金 / 100）。外れは 0
- ``pool``: その券種のレースの総票数（円、確定時）。不明なら NaN（払戻の補正をしない）
- ``k_win``: その券種で払い戻される組番の数（排反な券種 1、複勝 2 か 3、ワイド 3）
- ``takeout``: 控除率

自分の賭け金による払戻の低下（パリミュチュエル）: 的中組番の票数を W = pool(1−t) / (k·pay) と推定し、
払戻を (pool + S)(1 − t) / (k (W + s)) に直す（s その組番への自分の賭け金、S その券種へのレース内の自分の賭け金の合計）。
"""

from __future__ import annotations

import numpy as np
import pandas as pd

ODDS_BINS = np.array([1.0, 1.5, 2, 3, 5, 7, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 500, 1000, 2000, 5000,
                      1e4, 1e5, np.inf])


def effective_pay(pay, s, S, pool, k, t):
    """自分の賭け金を入れた後の払戻（1 円あたり）。pay = 0（外れ）はそのまま 0。"""
    pay = np.asarray(pay, float)
    s = np.asarray(s, float)
    pool = np.asarray(pool, float)
    out = pay.copy()
    hit = (pay > 0) & np.isfinite(pool) & (pool > 0) & (s > 0)
    if hit.any():
        kk = np.broadcast_to(np.asarray(k, float), pay.shape)[hit]
        tt = np.broadcast_to(np.asarray(t, float), pay.shape)[hit]
        SS = np.broadcast_to(np.asarray(S, float), pay.shape)[hit]
        W = pool[hit] * (1 - tt) / (kk * pay[hit])
        out[hit] = (pool[hit] + SS) * (1 - tt) / (kk * (W + s[hit]))
    return out


# --- 方針 ----------------------------------------------------------------------

def flat(c: pd.DataFrame, tau: float, band: tuple[float, float], unit: float) -> pd.DataFrame:
    """P1: 期待値 p·o ≥ τ かつ判断オッズが band = [lo, hi) の組番に unit 円ずつ。"""
    sel = c[(c["p"] * c["o"] >= tau) & (c["o"] >= band[0]) & (c["o"] < band[1])].copy()
    sel["stake"] = float(unit)
    S = sel.groupby("race_idx")["stake"].transform("sum").to_numpy()
    sel["ret"] = sel["stake"] * effective_pay(sel["pay"], sel["stake"], S, sel["pool"], sel["k_win"],
                                              sel["takeout"])
    sel["ret_noimpact"] = sel["stake"] * sel["pay"]
    return sel


def kelly(c: pd.DataFrame, lam: float, cap: float, bankroll0: float, min_stake: float = 100.0
          ) -> tuple[pd.DataFrame, np.ndarray]:
    """P2・P3: 分数ケリー。発走順にレースを進め、賭け金 = λ·f_full·資金（1 レースの合計は cap·資金まで）、
    min_stake 円単位に切り捨てる。返り値は (賭けた行, レースごとの資金の推移)。

    注意: 同じ時刻に発走する別の場のレースも、前のレースの結果が分かってから賭けたことにしている。
    """
    c = c[c["f_full"] > 0].sort_values(["race_idx"], kind="stable")
    if c.empty:
        return c.assign(stake=[], ret=[], ret_noimpact=[]), np.array([bankroll0])
    races = c["race_idx"].to_numpy()
    starts = np.r_[0, np.nonzero(np.diff(races))[0] + 1, len(races)]
    f = c["f_full"].to_numpy() * lam
    pay = c["pay"].to_numpy()
    pool = c["pool"].to_numpy()
    kw = c["k_win"].to_numpy()
    tk = c["takeout"].to_numpy()
    stake = np.zeros(len(c))
    ret = np.zeros(len(c))
    B = bankroll0
    path = [B]
    for a, b in zip(starts[:-1], starts[1:]):
        fr = f[a:b]
        tot = fr.sum()
        if tot > cap:
            fr = fr * (cap / tot)
        s = np.floor(fr * B / min_stake) * min_stake
        if s.sum() <= 0:
            path.append(B)
            continue
        r = s * effective_pay(pay[a:b], s, s.sum(), pool[a:b], kw[a:b], tk[a:b])
        stake[a:b], ret[a:b] = s, r
        B = B - s.sum() + r.sum()
        path.append(B)
        if B < min_stake:
            break
    out = c.assign(stake=stake, ret=ret, ret_noimpact=stake * pay)
    return out[out["stake"] > 0], np.array(path)


# --- 成績 ----------------------------------------------------------------------

def _date_boot(stake_d: np.ndarray, ret_d: np.ndarray, n_boot: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = len(stake_d)
    w = rng.multinomial(n, np.full(n, 1.0 / n), size=n_boot).astype(float)
    st = w @ stake_d
    return np.where(st > 0, (w @ ret_d) / np.where(st > 0, st, 1.0) - 1.0, np.nan)


def bet_metrics(bets: pd.DataFrame, all_dates, *, n_boot: int = 2000, seed: int = 0, level: float = 0.95,
                path: np.ndarray | None = None, bankroll0: float | None = None, n_races: int | None = None,
                ret_col: str = "ret") -> dict:
    """賭けた行から回収率など。all_dates はその期間の全開催日（賭けなかった日も 0 として再標本化する）。"""
    dates = pd.Index(pd.unique(pd.Series(all_dates)))
    out = {"n_bets": int(len(bets)), "n_races_bet": int(bets["race_idx"].nunique()) if len(bets) else 0}
    if bets.empty:
        return {**out, "roi": None}
    g = bets.groupby("date")[["stake", ret_col]].sum().reindex(dates, fill_value=0.0)
    stake, ret = float(g["stake"].sum()), float(g[ret_col].sum())
    roi = ret / stake - 1.0
    boot = _date_boot(g["stake"].to_numpy(), g[ret_col].to_numpy(), n_boot, seed)
    a = (1 - level) / 2
    out.update(
        stake=stake, ret=ret, roi=roi,
        roi_ci=[float(np.nanquantile(boot, a)), float(np.nanquantile(boot, 1 - a))],
        # 片側 p 値（回収率 ≤ 0 の帰無仮説）: ブートストラップ分布を 0 の周りに移した近似
        p_roi_gt0=float((1 + np.sum(boot - roi >= roi)) / (1 + np.sum(np.isfinite(boot)))),
        hit_rate=float((bets["pay"] > 0).mean()),
        mean_odds=float(bets["o"].mean()),
        roi_by_year={int(y): float(v[ret_col].sum() / v["stake"].sum() - 1) for y, v in bets.groupby("year")},
        roi_by_band=_by_band(bets, ret_col),
    )
    cum = np.cumsum(g[ret_col].to_numpy() - g["stake"].to_numpy())
    out["max_drawdown_yen"] = float(np.max(np.maximum.accumulate(np.r_[0, cum]) - np.r_[0, cum]))
    if path is not None and bankroll0:
        out["bankroll_final"] = float(path[-1])
        out["log_growth_total"] = float(np.log(max(path[-1], 1e-9) / bankroll0))
        if n_races:
            out["log_growth_per_race"] = out["log_growth_total"] / n_races
        peak = np.maximum.accumulate(path)
        out["max_drawdown_frac"] = float(np.max(1 - path / peak))
    return out


def _by_band(bets: pd.DataFrame, ret_col: str) -> dict:
    edges = [1, 5, 20, 100, 1000, np.inf]
    lab = pd.cut(bets["o"], edges, right=False)
    r = {}
    for k, v in bets.groupby(lab, observed=True):
        r[f"[{k.left:g},{k.right:g})"] = {"n": int(len(v)), "roi": float(v[ret_col].sum() / v["stake"].sum() - 1)}
    return r


# --- 賭け方のプラセボ --------------------------------------------------------------

def bin_index(o) -> np.ndarray:
    return np.clip(np.searchsorted(ODDS_BINS, np.asarray(o, float), side="right") - 1, 0, len(ODDS_BINS) - 2)


class PlaceboPool:
    """ある券種・期間の全候補について、判断オッズの帯ごとの候補数と当たりの払戻を持つ。"""

    def __init__(self):
        self.n = np.zeros(len(ODDS_BINS) - 1, dtype=np.int64)
        self.wins: list[list[float]] = [[] for _ in range(len(ODDS_BINS) - 1)]

    def add(self, o: np.ndarray, pay: np.ndarray) -> None:
        b = bin_index(o)
        self.n += np.bincount(b, minlength=len(self.n))
        for bi, pv in zip(b[pay > 0], pay[pay > 0]):
            self.wins[bi].append(float(pv))

    def roi_distribution(self, bets: pd.DataFrame, n_rep: int, seed: int) -> np.ndarray:
        """bets と同じ帯・同じ回数・同じ賭け金で無作為に選んだときの回収率（払戻の補正なし）。"""
        rng = np.random.default_rng(seed)
        b = bin_index(bets["o"])
        stakes = bets["stake"].to_numpy(float)
        total = stakes.sum()
        rets = np.zeros(n_rep)
        for bi in np.unique(b):
            st = stakes[b == bi]
            m = len(st)
            wins = np.asarray(self.wins[bi])
            N = int(self.n[bi])
            if N == 0 or len(wins) == 0:
                continue
            m_eff = min(m, N)
            h = rng.hypergeometric(len(wins), N - len(wins), m_eff, size=n_rep)
            for r in range(n_rep):
                if h[r]:
                    rets[r] += np.sum(rng.choice(st, h[r], replace=False) * rng.choice(wins, h[r], replace=False))
        return rets / total - 1.0


def holm(pvals: dict[str, float]) -> dict[str, float]:
    keys = [k for k, v in pvals.items() if v is not None]
    ps = np.array([pvals[k] for k in keys])
    order = np.argsort(ps)
    m = len(ps)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * ps[i])
        adj[i] = min(run, 1.0)
    return {k: float(a) for k, a in zip(keys, adj)}

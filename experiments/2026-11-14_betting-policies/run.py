"""賭け方の評価（ADR 0004）。config.yaml を読み、results.json を書く。

先に make_preds.py で市場オフセット LightGBM の予測を作っておく。
uv run --extra ml python experiments/2026-11-14_betting-policies/run.py
KEIBA_SMOKE=1 で 1/20 のレース・少ない反復で走らせ、結果は /tmp に書く。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from keiba_ai import features as F  # noqa: E402
from keiba_ai.baselines import market_odds as mo  # noqa: E402
from keiba_ai.betting import combos, kelly, policy, pricing  # noqa: E402
from keiba_ai.betting import data as bd  # noqa: E402

cfg = yaml.safe_load((HERE / "config.yaml").read_text(encoding="utf-8"))
SEED = cfg["seed"]
SMOKE = os.environ.get("KEIBA_SMOKE") == "1"
BOOT = cfg["eval"]["bootstrap"]
if SMOKE:
    BOOT = {**BOOT, "n_boot": 200}
    cfg["placebo"]["n_rep"] = 50
    cfg["pricing"]["n_races_sample"] = 300
    cfg["grid"]["P1"]["min_bets_valid"] = 30
TYPES = cfg["bet_types"]
SPLITS = ("valid", "test")
t0 = time.time()


def log(*a):
    print(f"[{time.time() - t0:7.1f}s]", *a, flush=True)


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


# --- 読み込み ----------------------------------------------------------------------

def load_horses():
    """予測のあるレースの出走馬 + 10 分前・30 分前の単勝・複勝オッズ + 確定オッズ + 着順。"""
    D = cfg["decision"]
    preds = pl.read_parquet(ROOT / cfg["model"]["preds"])
    races = pl.read_parquet(mo.DATA_DIR / "races.parquet", columns=["race_key", "post_at", "n_starters"])
    df = preds.join(races, on="race_key", how="left")
    df = df.with_columns(pl.col("umaban").cast(pl.Int16))
    N, M = D["minutes_before"], D["momentum_minutes"]
    w10 = mo.pre_deadline_odds(N).select("race_key", pl.col("umaban").cast(pl.Int16),
                                         o10=pl.when(pl.col("win_status") == "ok").then(pl.col("win_odds")))
    w30 = mo.pre_deadline_odds(M).select("race_key", pl.col("umaban").cast(pl.Int16),
                                         o30=pl.when(pl.col("win_status") == "ok").then(pl.col("win_odds")))
    wf = mo.final_odds().select("race_key", pl.col("umaban").cast(pl.Int16), of=pl.col("win_odds"))
    pl10 = bd.place_snapshot(N).select("race_key", pl.col("umaban").cast(pl.Int16),
                                       pl10=pl.when(pl.col("place_status") == "ok").then(pl.col("place_odds_min")))
    pl30 = bd.place_snapshot(M).select("race_key", pl.col("umaban").cast(pl.Int16),
                                       pl30=pl.when(pl.col("place_status") == "ok").then(pl.col("place_odds_min")))
    plf = pl.read_parquet(mo.DATA_DIR / "odds_final.parquet", columns=["race_key", "umaban", "place_odds_min"]
                          ).select("race_key", pl.col("umaban").cast(pl.Int16), plf=pl.col("place_odds_min"))
    ent = pl.read_parquet(mo.DATA_DIR / "entries.parquet", columns=["race_key", "umaban", "finish_pos"]
                          ).select("race_key", pl.col("umaban").cast(pl.Int16), "finish_pos")
    for t in (w10, w30, wf, pl10, pl30, plf):
        df = df.join(t, on=["race_key", "umaban"], how="left")
    df = df.join(ent, on=["race_key", "umaban"], how="left")
    # 決定時刻の発表に載っていて、予測のない馬（あとで取消・除外）がいるレース
    snap_n = w10.filter(pl.col("o10").is_not_null()).group_by("race_key").agg(n_snap=pl.len())
    df = df.join(snap_n, on="race_key", how="left").with_columns(n=pl.len().over("race_key"))
    info = {"n_races_preds": df["race_key"].n_unique()}
    bad = df.filter((pl.col("n_snap") != pl.col("n")) | pl.col("o10").is_null())["race_key"].unique()
    df = df.filter(~pl.col("race_key").is_in(bad.implode()))
    info["n_races_dropped_snapshot_mismatch"] = int(len(bad))
    assert pd.Timestamp(df["date"].max()) < pd.Timestamp(cfg["split"]["holdout_never_evaluate_from"])
    if SMOKE:
        df = df.filter(pl.col("race_key").hash(seed=0) % 20 == 0)
    df = df.sort("post_at", "race_key", "umaban")
    info["n_races_by_split"] = {s: int(v) for s, v in df.group_by("split").agg(pl.col("race_key").n_unique()).rows()}
    return df, info


def place_k(n: int) -> int:
    r = cfg["decision"]["place_k_rule"]
    return 3 if n >= r["min_3"] else (2 if n >= r["min_2"] else 0)


def top3(g: pd.DataFrame):
    fp = g["finish_pos"].to_numpy()
    idx = [np.nonzero(fp == k)[0] for k in (1, 2, 3)]
    if all(len(i) == 1 for i in idx):
        return [int(i[0]) for i in idx]
    return None


def race_groups(pdf: pd.DataFrame):
    keys = pdf["race_key"].to_numpy()
    starts = np.r_[0, np.nonzero(keys[1:] != keys[:-1])[0] + 1, len(keys)]
    for a, b in zip(starts[:-1], starts[1:]):
        yield keys[a], pdf.iloc[a:b]


def fit_gamma(pdf: pd.DataFrame, col: str) -> dict:
    ps, f, s, t = [], [], [], []
    for _, g in race_groups(pdf):
        o = top3(g)
        if o is None:
            continue
        ps.append(g[col].to_numpy()), f.append(o[0]), s.append(o[1]), t.append(o[2])
    return combos.fit_gammas(ps, f, s, t, bounds=tuple(cfg["gamma"]["bounds"]))


def by_race(df: pl.DataFrame, val: str, keys=None) -> dict:
    """race_key → (code の昇順の配列, 値の配列)。"""
    if keys is not None:
        df = df.filter(pl.col("race_key").is_in(list(keys)))
    df = df.sort("race_key", "code")
    out = {}
    rk = df["race_key"].to_numpy()
    code = df["code"].to_numpy()
    v = df[val].to_numpy().astype(float)
    starts = np.r_[0, np.nonzero(rk[1:] != rk[:-1])[0] + 1, len(rk)] if len(rk) else [0]
    for a, b in zip(starts[:-1], starts[1:]):
        out[rk[a]] = (code[a:b], v[a:b])
    return out


def lookup(table: dict, rk: str, codes: np.ndarray) -> np.ndarray:
    if rk not in table:
        return np.full(len(codes), np.nan)
    c, v = table[rk]
    i = np.clip(np.searchsorted(c, codes), 0, len(c) - 1)
    return np.where(c[i] == codes, v[i], np.nan)


# --- 価格モデルとオッズ変化のモデル ----------------------------------------------------

def fit_price_models(train: pd.DataFrame, g_mkt: dict, valid: pd.DataFrame) -> tuple[dict, dict]:
    rng = np.random.default_rng(SEED)
    P = cfg["pricing"]
    models, diag = {}, {}
    sets = {}
    for name, d in (("train", train), ("valid", valid)):
        rks = d["race_key"].unique()
        sets[name] = set(rng.choice(rks, min(P["n_races_sample"], len(rks)), replace=False).tolist())
    ptypes = sorted({t for t in TYPES if "price" in cfg["odds_sources"][t]})
    for name in ("train", "valid"):
        rows = defaultdict(list)
        d = (train if name == "train" else valid)
        d = d[d["race_key"].isin(sets[name])]
        for rk, g in race_groups(d):
            r = combos.race_probs(g["umaban"].to_numpy(), g["p_mkt"].to_numpy(), g_mkt["g2"], g_mkt["g3"],
                                  types=ptypes)
            for t in ptypes:
                code, q = r[t]
                rows[t].append(pd.DataFrame({"race_key": rk, "code": code, "q": q, "n": len(g)}))
        for t in ptypes:
            q = pd.concat(rows[t])
            fo = bd.final_exotic(t, race_keys=sets[name]).filter(pl.col("status") == "ok").select(
                "race_key", "code", "odds").to_pandas()
            m = q.merge(fo, on=["race_key", "code"], how="inner")
            if name == "train":
                models[t] = pricing.fit_price(m["q"], m["n"], m["odds"])
                log("price", t, {k: v for k, v in models[t].items() if k != "beta"})
            else:
                pred = pricing.predict_price(models[t], m["q"], m["n"])
                e = np.log(pred) - np.log(m["odds"])
                diag[t] = {"valid_n": int(len(m)), "valid_rmse_log": float(np.sqrt(np.mean(e ** 2))),
                           "valid_mae_log": float(np.mean(np.abs(e))), "valid_bias_log": float(np.mean(e))}
                if t == "quinella":  # 実際の 10 分前オッズとの比較（検算）
                    s10 = bd.quinella_snapshot(str(cfg["decision"]["minutes_before"]), race_keys=sets[name]
                                               ).filter(pl.col("status") == "ok").select(
                        "race_key", "code", o10=pl.col("odds")).to_pandas()
                    mm = m.assign(pred=pred).merge(s10, on=["race_key", "code"], how="inner")
                    diag[t]["valid_rmse_log_pred_vs_n10"] = float(np.sqrt(np.mean(np.log(mm["pred"] / mm["o10"]) ** 2)))
                    diag[t]["valid_rmse_log_n10_vs_final"] = float(np.sqrt(np.mean(np.log(mm["o10"] / mm["odds"]) ** 2)))
                log("price diag", t, diag[t])
    return models, diag


def fit_drift_models(train: pd.DataFrame) -> dict:
    out = {}
    out["win"] = pricing.fit_drift(train["o10"], train["o30"], train["n"], train["of"])
    out["place"] = pricing.fit_drift(train["pl10"], train["pl30"], train["n"], train["plf"])
    rng = np.random.default_rng(SEED + 1)
    rks = train["race_key"].unique()
    rks = set(rng.choice(rks, min(10 * cfg["pricing"]["n_races_sample"], len(rks)), replace=False).tolist())
    s = str(cfg["decision"]["minutes_before"]), str(cfg["decision"]["momentum_minutes"])
    a = bd.quinella_snapshot(s[0], race_keys=rks).filter(pl.col("status") == "ok").select("race_key", "code", o10="odds")
    b = bd.quinella_snapshot(s[1], race_keys=rks).filter(pl.col("status") == "ok").select("race_key", "code", o30="odds")
    f = bd.final_exotic("quinella", race_keys=rks).filter(pl.col("status") == "ok").select("race_key", "code", of="odds")
    n = pl.from_pandas(train[["race_key", "n"]].drop_duplicates())
    m = a.join(b, on=["race_key", "code"], how="left").join(f, on=["race_key", "code"], how="inner").join(
        n, on="race_key").to_pandas()
    out["quinella"] = pricing.fit_drift(m["o10"], m["o30"], m["n"], m["of"])
    for k, v in out.items():
        log("drift", k, {kk: vv for kk, vv in v.items() if kk != "beta"})
    return out


# --- 候補 --------------------------------------------------------------------------

class Cands:
    def __init__(self):
        self.cols = defaultdict(list)
        self.placebo = policy.PlaceboPool()
        self.n_all = 0

    def add(self, **kw):
        for k, v in kw.items():
            self.cols[k].append(v)

    def frame(self) -> pd.DataFrame:
        if not self.cols:
            return pd.DataFrame(columns=["race_idx", "date", "year", "p", "o", "f_full", "pay", "pool", "k_win",
                                         "takeout"])
        d = {k: np.concatenate(v) for k, v in self.cols.items()}
        return pd.DataFrame(d)


def build_candidates(d: pd.DataFrame, g_model: dict, g_mkt: dict, price_m: dict, drift_m: dict,
                     tables: dict) -> tuple[dict, dict]:
    """(券種, 判断オッズ) ごとの候補。期待値 ≥ 1 か full Kelly > 0 の行だけ残す（プラセボの母集団は全行）。"""
    C: dict[tuple[str, str], Cands] = defaultdict(Cands)
    stats = defaultdict(int)
    for ri, (rk, g) in enumerate(race_groups(d)):
        u = g["umaban"].to_numpy().astype(np.int64)
        n = len(u)
        date = g["date"].iloc[0]
        year = date.year
        pk = place_k(n)
        types = [t for t in TYPES if not (t == "place" and pk == 0) and not (combos.N_LEGS[t] > n - 1)]
        pm = combos.race_probs(u, g["p_offset"].to_numpy(), g_model["g2"], g_model["g3"], place_k=max(pk, 2),
                               types=types)
        qm = combos.race_probs(u, g["p_mkt"].to_numpy(), g_mkt["g2"], g_mkt["g3"], types=types)
        for t in types:
            if rk not in tables["pay"][t]:
                stats[f"no_payout_{t}"] += 1
                continue
            code, p = pm[t]
            pay = np.nan_to_num(lookup(tables["pay"][t], rk, code)) / 100.0
            k_win = max(int((pay > 0).sum()), 1)
            pool = tables["pool"][t].get(rk, np.nan)
            for src in cfg["odds_sources"][t]:
                if t in ("win", "place"):
                    a, b = ("o10", "o30") if t == "win" else ("pl10", "pl30")
                    o10 = g[a].to_numpy(float)
                    o = o10 if src == "n10" else pricing.predict_drift(drift_m[t], o10, g[b].to_numpy(float), n)
                elif src in ("n10", "drift"):  # quinella
                    o10 = lookup(tables["q10"], rk, code)
                    o = o10 if src == "n10" else pricing.predict_drift(drift_m[t], o10, lookup(tables["q30"], rk, code), n)
                else:  # price
                    qc, q = qm[t]
                    assert np.array_equal(qc, code)
                    o = pricing.predict_price(price_m[t], q, n)
                ok = np.isfinite(o) & (o > 0)
                if not ok.all():
                    stats[f"missing_odds_{t}_{src}"] += int((~ok).sum())
                if not ok.any():
                    continue
                pp, oo, pa, cc = p[ok], o[ok], pay[ok], code[ok]
                f = kelly.exclusive(pp, oo) if combos.EXCLUSIVE[t] else kelly.independent(pp, oo)
                c = C[(t, src)]
                c.placebo.add(oo, pa)
                c.n_all += len(oo)
                keep = (pp * oo >= 1.0) | (f > 0)
                if keep.any():
                    m = int(keep.sum())
                    c.add(race_idx=np.full(m, ri, np.int32), date=np.full(m, np.datetime64(date, "D")),
                          year=np.full(m, year, np.int16), code=cc[keep], p=pp[keep].astype(np.float32),
                          o=oo[keep].astype(np.float32), f_full=f[keep].astype(np.float32), pay=pa[keep],
                          pool=np.full(m, pool), k_win=np.full(m, k_win, np.int8),
                          takeout=np.full(m, bd.TAKEOUT[t], np.float32))
        if ri % 2000 == 0:
            log("candidates", ri)
    return C, dict(stats)


# --- 方針の評価 ------------------------------------------------------------------------

def compact(m: dict) -> dict:
    return {k: m.get(k) for k in ("n_bets", "roi", "roi_ci", "p_roi_gt0", "log_growth_per_race", "stake",
                                  "max_drawdown_frac", "hit_rate")}


def run_policy(pol: str, c: pd.DataFrame, t: str, params: dict, dates, n_races: int, full: bool):
    G = cfg["grid"]
    kw = dict(n_boot=BOOT["n_boot"] if full else 200, seed=SEED, level=BOOT["level"])
    if pol == "P1":
        b = policy.flat(c, params["tau"], tuple(params["band"]), G["P1"]["unit_yen"])
        return b, policy.bet_metrics(b, dates, **kw)
    K = G[pol]
    b, path = policy.kelly(c, params["lambda"], params["cap"], K["bankroll0_yen"], K["min_stake_yen"])
    m = policy.bet_metrics(b, dates, path=path, bankroll0=K["bankroll0_yen"], n_races=n_races, **kw)
    if m.get("roi") is not None:
        m["roi_noimpact"] = float(b["ret_noimpact"].sum() / b["stake"].sum() - 1)
    return b, m


def grid(pol: str, t: str):
    G = cfg["grid"]
    if pol == "P1":
        return [{"tau": float(tau), "band": [float(x) for x in band]} for tau in G["P1"]["tau"] for band in G["P1"]["bands"][t]]
    return [{"lambda": lam, "cap": cap} for lam in G[pol]["lambda"] for cap in G[pol]["cap"]]


def select(pol: str, rows: list[dict]):
    if pol == "P1":
        ok = [r for r in rows if r["metrics"]["n_bets"] >= cfg["grid"]["P1"]["min_bets_valid"]
              and r["metrics"].get("roi") is not None]
        return max(ok, key=lambda r: r["metrics"]["roi_ci"][0]) if ok else None
    ok = [r for r in rows if r["metrics"].get("log_growth_per_race") is not None]
    return max(ok, key=lambda r: r["metrics"]["log_growth_per_race"]) if ok else None


# --- 本体 ----------------------------------------------------------------------------

def main():
    git_hash = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain", "--", *cfg["git_tracked_paths"])
    meta = json.loads((ROOT / cfg["model"]["preds"]).with_suffix(".json").read_text(encoding="utf-8"))
    if abs(meta["race_logloss"]["test"] - cfg["model"]["expected_test_logloss"]) > 5e-4:
        raise SystemExit(f"予測の作り直しが一致しない: {meta['race_logloss']}")
    df, universe = load_horses()
    log("universe", universe)
    pdf = df.to_pandas()
    pdf["date"] = pd.to_datetime(pdf["date"])
    parts = {s: pdf[pdf["split"] == s].reset_index(drop=True) for s in ("train", "valid", "test")}

    g_mkt = fit_gamma(parts["train"], "p_mkt")
    g_model = fit_gamma(parts["valid"], "p_offset")
    log("gamma market", g_mkt, "model", g_model)
    price_m, price_diag = fit_price_models(parts["train"], g_mkt, parts["valid"])
    drift_m = fit_drift_models(parts["train"])

    rk_eval = set(parts["valid"]["race_key"]) | set(parts["test"]["race_key"])
    tables = {"pay": {}, "pool": {}}
    for t in TYPES:
        tables["pay"][t] = by_race(bd.payouts_by_type(t), "payout", rk_eval)
    pools = bd.pools().filter(pl.col("race_key").is_in(list(rk_eval)))
    tables["pool"]["win"] = dict(zip(pools["race_key"], pools["win_pool"].cast(pl.Float64)))
    tables["pool"]["place"] = dict(zip(pools["race_key"], pools["place_pool"].cast(pl.Float64)))
    for t in TYPES:
        if t in ("win", "place"):
            continue
        v = (bd.final_exotic(t, race_keys=rk_eval).group_by("race_key").agg(pl.col("vote_total").max()))
        tables["pool"][t] = dict(zip(v["race_key"], v["vote_total"].cast(pl.Float64)))
    N, M = str(cfg["decision"]["minutes_before"]), str(cfg["decision"]["momentum_minutes"])
    tables["q10"] = by_race(bd.quinella_snapshot(N, race_keys=rk_eval).filter(pl.col("status") == "ok"), "odds")
    tables["q30"] = by_race(bd.quinella_snapshot(M, race_keys=rk_eval).filter(pl.col("status") == "ok"), "odds")
    log("tables loaded")

    cands, cstats, dates, n_races = {}, {}, {}, {}
    for s in SPLITS:
        C, st = build_candidates(parts[s], g_model, g_mkt, price_m, drift_m, tables)
        cands[s] = C
        cstats[s] = {**st, **{f"{t}/{src}": {"n_all": c.n_all} for (t, src), c in C.items()}}
        dates[s] = parts[s]["date"].unique()
        n_races[s] = parts[s]["race_key"].nunique()
        log("candidates done", s, {k: v.n_all for k, v in C.items()})

    results, pvals = {}, {}
    for t in TYPES:
        for src in cfg["odds_sources"][t]:
            for pol in ("P1", "P2", "P3"):
                if src not in cfg["policies"][pol]["odds_sources"]:
                    continue
                key = f"{t}/{src}/{pol}"
                cv = cands["valid"][(t, src)].frame()
                rows = []
                for prm in grid(pol, t):
                    _, m = run_policy(pol, cv, t, prm, dates["valid"], n_races["valid"], full=False)
                    rows.append({"params": prm, "metrics": compact(m)})
                best = select(pol, rows)
                entry = {"valid_grid": rows, "selected": best and best["params"]}
                if best is not None:
                    ct = cands["test"][(t, src)].frame()
                    bt, mt = run_policy(pol, ct, t, best["params"], dates["test"], n_races["test"], full=True)
                    _, mv = run_policy(pol, cv, t, best["params"], dates["valid"], n_races["valid"], full=True)
                    entry["valid"] = mv
                    entry["test"] = mt
                    if mt.get("roi") is not None and len(bt):
                        dist = cands["test"][(t, src)].placebo.roi_distribution(bt, cfg["placebo"]["n_rep"], SEED)
                        roi0 = float(bt["ret_noimpact"].sum() / bt["stake"].sum() - 1)
                        entry["placebo"] = {"roi_noimpact": roi0, "mean": float(np.mean(dist)),
                                            "p95": float(np.percentile(dist, cfg["placebo"]["pass_percentile"])),
                                            "percentile_of_actual": float(np.mean(dist < roi0) * 100)}
                        if key not in cfg["holm_exclude"]:
                            pvals[key] = mt["p_roi_gt0"]
                results[key] = entry
                log(key, best and best["params"], "valid", best and best["metrics"].get("roi"),
                    "test", entry.get("test", {}).get("roi"), entry.get("placebo", {}).get("percentile_of_actual"))

    adj = policy.holm(pvals)
    alpha = cfg["eval"]["alpha"]
    summary = {}
    for key, e in results.items():
        if "test" not in e:
            summary[key] = {"selected": None}
            continue
        mt = e["test"]
        pb = e.get("placebo", {})
        summary[key] = {
            "selected": e["selected"], "valid_roi": e["valid"].get("roi"), "test_roi": mt.get("roi"),
            "test_roi_ci": mt.get("roi_ci"), "test_n_bets": mt.get("n_bets"),
            "test_log_growth_per_race": mt.get("log_growth_per_race"),
            "p_holm": adj.get(key),
            "pass_test_holm": bool(adj.get(key) is not None and adj[key] < alpha),
            "pass_placebo": bool(pb and pb["roi_noimpact"] > pb["p95"]),
        }
    passed = [k for k, v in summary.items() if v.get("pass_test_holm") and v.get("pass_placebo")]
    head = {"n_policies_in_family": len(pvals), "n_pass_test_and_placebo": len(passed), "passed": passed,
            **{f"test_roi/{k}": v["test_roi"] for k, v in summary.items() if v.get("test_roi") is not None}}
    res = {
        "experiment": HERE.name, "status": "done", "git_hash": git_hash, "git_dirty_tracked_paths": dirty or None,
        "data_version": F.data_version(F.DATA_DIR, F.FeatureConfig.from_dict(
            yaml.safe_load((ROOT / "experiments/2026-11-14_market-combination/config.yaml").read_text())
            ["offset_lgbm"]["feature_config"])),
        "seed": SEED, "split": "2004-2018/2019-2021/2022-2025", "metrics": head, "summary": summary,
        "preds_meta": {k: meta[k] for k in ("git_hash", "race_logloss", "power_fit_k")},
        "universe": universe, "gamma": {"market_train": g_mkt, "model_valid": g_model},
        "price_models": price_m, "price_diag": price_diag, "drift_models": drift_m, "candidates": cstats,
        "results": results, "runtime_s": round(time.time() - t0, 1),
    }
    out = Path("/tmp/betting-policies-smoke.json") if SMOKE else HERE / "results.json"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    log("written", out, "passed:", passed)


if __name__ == "__main__":
    main()

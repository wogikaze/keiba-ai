"""市場（10 分前 × power_fit）とオッズなしモデルの結合。config.yaml を読み、results.json を書く。

uv run --extra ml python experiments/2026-11-14_market-combination/run.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
import warnings
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import polars as pl
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from keiba_ai import evaluate as ev  # noqa: E402
from keiba_ai import features as F  # noqa: E402
from keiba_ai import market_offset as mof  # noqa: E402
from keiba_ai.baselines import market_odds as mo  # noqa: E402

cfg = yaml.safe_load((HERE / "config.yaml").read_text(encoding="utf-8"))
SEED = cfg["seed"]
BOOT = cfg["eval"]["bootstrap"]
BINS = cfg["eval"]["ece_bins"]
RACE = "race_id"
# 動作確認用: KEIBA_SMOKE=1 で 1/20 のレース、少ない反復で走らせ、結果は /tmp に書く（本番の結果には使わない）
import os  # noqa: E402

SMOKE = os.environ.get("KEIBA_SMOKE") == "1"
if SMOKE:
    BOOT = {**BOOT, "n_boot": 100}
    cfg["offset_lgbm"]["num_boost_round"] = 30
    cfg["placebo"]["shuffle_n_rep"] = 2


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def tag(m):
    return "last" if m is None else str(m)


def dl(d, p, ref, cluster=None, n_boot=None):
    r = ev.delta_logloss(d, p, ref, race=RACE, cluster=cluster, n_boot=n_boot or BOOT["n_boot"], seed=SEED,
                         level=BOOT["level"])
    return {k: r[k] for k in ("delta", "ci", "se", "p_value", "logloss_model", "logloss_ref", "n_races",
                              "n_clusters")}


def deltas(d, p, ref):
    return {c: dl(d, p, ref, cluster=None if c == "race" else "date") for c in BOOT["clusters"]}


# --- データ ------------------------------------------------------------------

def load_frame():
    sp = cfg["split"]
    lo, hi = pd.Timestamp(sp["train"][0]).date(), pd.Timestamp(sp["test"][1]).date()
    uni = mo.race_universe().filter(pl.col("date").is_between(lo, hi))
    df = uni
    for s in cfg["universe"]["common_odds_sources"]:
        o = mo.final_odds() if s == "final" else mo.pre_deadline_odds(None if s == "last" else int(s))
        df = df.join(o.select("race_key", "umaban", pl.col("win_odds").alias(f"odds_{s}")),
                     on=["race_key", "umaban"], how="left")
    ocols = [f"odds_{s}" for s in cfg["universe"]["common_odds_sources"]]
    info = {"n_races_universe": df["race_key"].n_unique()}
    bad = df.filter(pl.any_horizontal([pl.col(c).is_null() | (pl.col(c) <= 0) for c in ocols]))["race_key"].unique()
    df = df.filter(~pl.col("race_key").is_in(bad.implode()))
    info["n_races_after_common_odds"] = df["race_key"].n_unique()
    # k は market-baseline と同じ集合（共通オッズのレースの train）で当てはめる（モデルの有無で絞る前）
    sp_tr = [pd.Timestamp(v).date() for v in sp["train"]]
    k = mo.fit_power_k(df.filter(pl.col("date").is_between(*sp_tr)).select("race_key", "odds_10", "y").to_pandas(),
                       odds="odds_10")

    for name, path in cfg["models"]["lgbm_preds"].items():
        p = (pl.read_parquet(ROOT / path, columns=["race_key", "umaban", "p_win"])
             .with_columns(pl.col("umaban").cast(df["umaban"].dtype)).rename({"p_win": f"p_{name}"}))
        df = df.join(p, on=["race_key", "umaban"], how="left")
    fcfg = F.FeatureConfig.from_dict(cfg["offset_lgbm"]["feature_config"])
    feats = F.load_features(fcfg).select("race_key", *F.FEATURES)
    feats = feats.with_columns(pl.col("umaban").cast(df["umaban"].dtype), _has_feat=pl.lit(True))
    df = df.join(feats, on=["race_key", "umaban"], how="left")
    need = [f"p_{m}" for m in cfg["universe"]["require_models"]]
    miss = df.filter(pl.any_horizontal([pl.col(c).is_null() for c in need]) | pl.col("_has_feat").is_null())
    df = df.filter(~pl.col("race_key").is_in(miss["race_key"].unique().implode()))
    info["n_races_dropped_missing_model"] = int(miss["race_key"].n_unique())
    nowin = df.group_by("race_key").agg(pl.col("y").sum()).filter(pl.col("y") == 0)["race_key"]
    df = df.filter(~pl.col("race_key").is_in(nowin.implode())).drop("_has_feat")
    info["n_races_dropped_no_winner"] = int(len(nowin))

    if SMOKE:
        df = df.filter(pl.col("race_key").hash(seed=0) % 20 == 0)
    pdf = df.to_pandas()
    pdf["date"] = pd.to_datetime(pdf["date"])
    pdf[RACE] = pdf["race_key"]
    pdf["split"] = ev.time_split(pdf["date"], pd.Timestamp(sp["valid"][0]), pd.Timestamp(sp["test"][0]),
                                 pd.Timestamp(sp["test"][1]) + pd.Timedelta(days=1))
    assert pdf["date"].max() < pd.Timestamp(sp["holdout_never_evaluate"][0])
    for c in F.CATEGORICAL:
        pdf[c] = pdf[c].astype("category")
    pdf = pdf.sort_values(["date", "race_key", "umaban"]).reset_index(drop=True)
    info["n_races_by_split"] = pdf.groupby("split")[RACE].nunique().to_dict()
    info["n_horses_by_split"] = pdf.groupby("split").size().to_dict()
    info["n_dead_heat_races"] = int((pdf.groupby(RACE)["y"].sum() > 1).sum())
    return pdf, info, fcfg, k


# --- モデル ------------------------------------------------------------------

def clogit(pdf):
    C = cfg["clogit"]
    st = mof.Standardizer(C["features"], tuple(C["log1p"]), C["clip_z"]).fit(pdf[pdf["split"] == "train"])
    X, names = st.transform(pdf)
    gid_all, n_all = mof.group_ids(pdf[RACE])
    parts = {}
    for s in ("train", "valid"):
        m = (pdf["split"] == s).to_numpy()
        gid, n = mof.group_ids(pdf.loc[m, RACE])
        parts[s] = (X[m], mof.targets(pdf.loc[m, "y"].to_numpy(), gid, n), gid, n)
    grid = []
    best = None
    for l2 in C["l2_grid"]:
        fit = mof.fit_clogit(*parts["train"], l2=l2)
        Xv, tv, gv, nv = parts["valid"]
        vl = mof.race_nll(Xv @ fit["coef"], tv, gv, nv)
        grid.append({"l2": l2, "train_loss": fit["loss"], "valid_logloss": vl, "converged": fit["converged"]})
        print(f"clogit l2={l2}: valid {vl:.5f}", flush=True)
        if best is None or vl < best[0]:
            best = (vl, l2, fit)
    _, l2, fit = best
    p = mof.softmax_by_group(X @ fit["coef"], gid_all, n_all)
    coef = {n: {"coef": float(c), "se": float(s)} for n, c, s in zip(names, fit["coef"], fit["se"])}
    return p, {"l2_grid": grid, "l2": l2, "coef": coef, "n_params": len(names)}


def offset_lgbm(pdf):
    O = cfg["offset_lgbm"]
    feats = list(F.FEATURES)
    d = {s: pdf[pdf["split"] == s] for s in ("train", "valid", "test")}
    init = {s: np.log(np.clip(v["p_mkt"].to_numpy(float), ev.EPS, None)) for s, v in d.items()}
    cats = [c for c in F.CATEGORICAL if c in feats]
    obj = mof.RaceSoftmax(d["train"][RACE].to_numpy(), d["train"]["y"].to_numpy())
    ev_va = mof.RaceSoftmax(d["valid"][RACE].to_numpy(), d["valid"]["y"].to_numpy())
    dtr = lgb.Dataset(d["train"][feats], label=d["train"]["y"].to_numpy(float), init_score=init["train"],
                      categorical_feature=cats, free_raw_data=False)
    dva = lgb.Dataset(d["valid"][feats], label=d["valid"]["y"].to_numpy(float), init_score=init["valid"],
                      categorical_feature=cats, reference=dtr, free_raw_data=False)
    params = {**O["params"], "objective": obj.objective, "metric": "None", "seed": SEED}
    log = {}
    t0 = time.time()
    b = lgb.train(params, dtr, num_boost_round=O["num_boost_round"], valid_sets=[dva], valid_names=["valid"],
                  feval=mof.make_feval({id(dva): ev_va}),
                  callbacks=[lgb.early_stopping(O["early_stopping_rounds"], verbose=False),
                             lgb.log_evaluation(O["log_every"]), lgb.record_evaluation(log)])
    curve = log["valid"]["race_logloss"]
    info = {"best_iteration": b.best_iteration, "train_seconds": round(time.time() - t0, 1),
            "valid_logloss_iter0": ev_va.metric(init["valid"]),
            "valid_logloss_best": float(curve[b.best_iteration - 1]),
            "valid_curve_every_100": [float(curve[i]) for i in range(0, len(curve), 100)]}
    out = np.empty(len(pdf))
    for s, v in d.items():
        f = b.predict(v[feats], num_iteration=b.best_iteration, raw_score=True)
        gid, n = mof.group_ids(v[RACE])
        out[v.index.to_numpy()] = mof.softmax_by_group(init[s] + f, gid, n)
        info[f"{s}_f_sd"] = float(np.std(f))
    gain = pd.Series(b.feature_importance("gain"), index=b.feature_name())
    info["importance_gain_share"] = {k: round(float(v), 4) for k, v in
                                     (gain / gain.sum()).sort_values(ascending=False).head(20).items()}
    return out, info


# --- 本体 --------------------------------------------------------------------

def main():
    git_hash = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain", "--", *cfg["git_tracked_paths"])
    pdf, universe, fcfg, k = load_frame()
    print(json.dumps(universe, indent=1, default=str), flush=True)
    tr, va, te = (pdf["split"] == s for s in ("train", "valid", "test"))

    # 市場
    M = cfg["market"]
    if not SMOKE and abs(k - M["expected_k"]) > 1e-6:
        warnings.warn(f"power_fit k = {k} が market-baseline の {M['expected_k']} と違う")
    pdf["p_mkt"] = mo.market_probs(pdf[["race_key", "odds_10"]], "power_fit", k=k, odds="odds_10")["p_market"].to_numpy()
    pdf["p_final"] = mo.market_probs(pdf[["race_key", "odds_final"]], "proportional", odds="odds_final")["p_market"].to_numpy()
    pdf["p_unif"] = 1.0 / pdf.groupby(RACE)["umaban"].transform("size")
    print("k =", k, flush=True)

    # 条件付きロジット
    pdf["p_clogit"], clogit_info = clogit(pdf)
    # 市場オフセットの LightGBM
    pdf["p_offset"], offset_info = offset_lgbm(pdf)
    print("offset:", {k_: v for k_, v in offset_info.items() if k_ != "importance_gain_share"}, flush=True)

    V, T = pdf[va], pdf[te]
    # Benter の 2 段階（valid で当てはめ、test で評価）
    models = ["A_top3", "B_rank", "C_win", "clogit"]
    benter = {}
    for m in models:
        fit = ev.fit_benter(V, [f"p_{m}", "p_mkt"], race=RACE)
        coef = fit["coef"]
        pdf[f"p_benter_{m}"] = ev.benter_predict(pdf, coef, race=RACE)
        Tm = pdf[te]
        benter[m] = {"alpha": coef[f"p_{m}"], "alpha_se": fit["se"][f"p_{m}"], "beta": coef["p_mkt"],
                     "beta_se": fit["se"]["p_mkt"], "valid_fit_logloss": fit["train_logloss"],
                     "converged": fit["converged"], "test": deltas(Tm, f"p_benter_{m}", "p_mkt")}
        print("benter", m, {k_: benter[m][k_] for k_ in ("alpha", "alpha_se", "beta")},
              benter[m]["test"]["race"]["delta"], flush=True)
    V, T = pdf[va], pdf[te]

    # プラセボ
    P = cfg["placebo"]
    rng = np.random.default_rng(SEED)
    placebo = {}
    for m in models:
        rows = []
        for i in range(P["shuffle_n_rep"]):
            Vs = V.assign(_p=ev.shuffle_within_race(V, f"p_{m}", rng, race=RACE))
            Ts = T.assign(_p=ev.shuffle_within_race(T, f"p_{m}", rng, race=RACE))
            r = ev.benter_two_stage(Vs, Ts, "_p", "p_mkt", race=RACE, n_boot=200, seed=SEED + i)
            rows.append({"alpha": r["alpha"], "alpha_se": r["alpha_se"], "beta": r["beta"],
                         "test_delta": r["test"]["delta"], "test_ci": list(r["test"]["ci"])})
        a = np.array([r["alpha"] for r in rows])
        placebo[f"shuffle_{m}"] = {"alpha_mean": float(a.mean()), "alpha_max_abs": float(np.abs(a).max()),
                                   "alpha_se_mean": float(np.mean([r["alpha_se"] for r in rows])),
                                   "test_delta_mean": float(np.mean([r["test_delta"] for r in rows])),
                                   "reps": rows}
        print("placebo", m, placebo[f"shuffle_{m}"]["alpha_mean"], placebo[f"shuffle_{m}"]["test_delta_mean"],
              flush=True)
    r = ev.benter_two_stage(V, T, "p_final", "p_mkt", race=RACE, n_boot=BOOT["n_boot"], seed=SEED)
    placebo["leaky_final_odds_DEMO"] = {"note": "確定オッズを「モデル」に入れたリークのデモ（使ってはいけない）",
                                        "alpha": r["alpha"], "alpha_se": r["alpha_se"], "beta": r["beta"],
                                        "beta_se": r["beta_se"], "test_delta": r["test"]["delta"],
                                        "test_ci": list(r["test"]["ci"])}
    print("leaky", placebo["leaky_final_odds_DEMO"], flush=True)

    # 比較表（全モデル、同じレース）
    cols = {"uniform": "p_unif", "lgbm_A_top3": "p_A_top3", "lgbm_B_rank": "p_B_rank", "lgbm_C_win": "p_C_win",
            "clogit": "p_clogit", "market_final_prop": "p_final", "market_n10_power_fit": "p_mkt",
            **{f"benter_{m}": f"p_benter_{m}" for m in models}, "offset_lgbm": "p_offset"}
    table = {}
    for name, c in cols.items():
        row = {s: ev.summary(pdf[pdf["split"] == s], c, race=RACE, bins=BINS) for s in ("valid", "test")}
        if c != "p_mkt":
            row["test_vs_mkt"] = deltas(T, c, "p_mkt")
        table[name] = row
        print(name, round(row["test"]["logloss"], 5), flush=True)
    # 年ごとの Δ（test）
    per_year = {}
    base = ev.race_scores(T, "p_mkt", race=RACE)["logloss"]
    yr = T.groupby(RACE)["date"].first().dt.year
    for name in [f"benter_{m}" for m in models] + ["offset_lgbm", "market_final_prop"]:
        dlt = ev.race_scores(T, cols[name], race=RACE)["logloss"] - base
        per_year[name] = {int(y): {"delta": float(v.mean()), "n_races": int(len(v))}
                          for y, v in dlt.groupby(yr.reindex(dlt.index))}

    # 賭けの健全性（戦略ではない）
    Bt = cfg["bets"]
    cands = [f"benter_{m}" for m in models] + ["offset_lgbm"]
    best = min(cands, key=lambda n: table[n]["valid"]["logloss"])
    snap = mo.pre_deadline_odds(int(Bt["decision_odds"]))
    snap = snap.filter(pl.col("win_odds").is_not_null() & (pl.col("win_odds") > 0))
    n_snap = snap.group_by("race_key").len().to_pandas().set_index("race_key")["len"]
    n_start = pdf.groupby(RACE).size()
    extra = n_snap.reindex(n_start.index).fillna(0) - n_start
    assert (extra >= 0).all(), "出走馬が決定時刻の発表にない"
    scratched_after = set(extra.index[extra > 0])
    pdf["pay_odds"] = pdf["win_payout_odds"].fillna(0.0)
    pdf["y_pay"] = pdf["win_payout_odds"].notna().astype(int)
    pdf["year"] = pdf["date"].dt.year
    bets = {"best_by_valid_logloss": best, "n_races_dropped_scratched_after_decision":
            {s: len(set(pdf.loc[pdf["split"] == s, RACE].unique()) & scratched_after) for s in Bt["splits"]},
            "runs": {}}
    # 残ったレースでは決定時刻の発表の全馬 = 出走馬なので、出走馬で正規化した確率 = 判断の確率
    for name in [best, "offset_lgbm", "market_n10_power_fit"]:
        c = cols[name]
        out = {}
        for s in Bt["splits"]:
            d = pdf[(pdf["split"] == s) & ~pdf[RACE].isin(scratched_after)]
            for th in Bt["thresholds"]:
                key = f"{s}_th{th}"
                r = ev.simulate_bets(d, c, decision_odds="odds_10", payout_odds="pay_odds", threshold=th,
                                     y="y_pay", race=RACE, n_boot=BOOT["n_boot"], seed=SEED, level=BOOT["level"])
                bt = r.pop("bets", None)
                if r["n_bets"]:
                    rd = ev.simulate_bets(d, c, decision_odds="odds_10", payout_odds="pay_odds", threshold=th,
                                          y="y_pay", race=RACE, cluster="date", n_boot=BOOT["n_boot"], seed=SEED,
                                          level=BOOT["level"])
                    r["roi_ci_date"] = rd["roi_ci"]
                    if Bt["by_year"]:
                        g = bt.groupby("year")
                        r["by_year"] = {int(y): {"n_bets": int(len(v)),
                                                 "roi": float(v["pay_odds"].mul(v["y_pay"]).sum() / len(v) - 1)}
                                        for y, v in g}
                out[key] = r
                print("bets", name, key, r.get("n_bets"), round(r.get("roi", float("nan")), 4), flush=True)
        bets["runs"][name] = out

    tv = lambda n: table[n]["test"]["logloss"]  # noqa: E731
    head = {"test_logloss_market_n10": tv("market_n10_power_fit"), "test_logloss_offset_lgbm": tv("offset_lgbm"),
            **{f"test_dlogloss_benter_{m}": benter[m]["test"]["race"]["delta"] for m in models},
            **{f"alpha_{m}": benter[m]["alpha"] for m in models},
            "test_dlogloss_offset_lgbm": table["offset_lgbm"]["test_vs_mkt"]["race"]["delta"]}
    res = {
        "experiment": HERE.name, "status": "done", "git_hash": git_hash, "git_dirty_tracked_paths": dirty or None,
        "data_version": F.data_version(F.DATA_DIR, fcfg), "seed": SEED,
        "split": "/".join(f"{a[:4]}-{b[:4]}" for a, b in (cfg["split"][s] for s in ("train", "valid", "test")))
                 + " (provisional)",
        "metrics": head, "reference": "market_n10_power_fit", "power_fit_k": k, "universe": universe,
        "benter": benter, "clogit": clogit_info, "offset_lgbm": offset_info, "placebo": placebo,
        "table": table, "per_year_test_delta": per_year, "bets": bets,
    }
    out_path = Path("/tmp/market-combination-smoke.json") if SMOKE else HERE / "results.json"
    out_path.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float) + "\n",
                                       encoding="utf-8")
    print("written; dirty =", dirty or None)


if __name__ == "__main__":
    main()

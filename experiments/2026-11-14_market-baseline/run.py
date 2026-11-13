"""市場（単勝オッズだけ）のベースライン。config.yaml を読み、results.json を書く。

uv run --extra ml python experiments/2026-11-14_market-baseline/run.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from keiba_ai import evaluate as ev  # noqa: E402
from keiba_ai.baselines import market_odds as mo  # noqa: E402

cfg = yaml.safe_load((HERE / "config.yaml").read_text(encoding="utf-8"))
P = cfg["model"]["params"]


def git_info():
    h = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "src/keiba_ai", str(HERE)],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return h, dirty == ""


def tag(m):
    return "last" if m is None else str(m)


def main():
    git_hash, clean = git_info()
    sp = cfg["split"]
    first, last = pd.Timestamp(sp["train"][0]), pd.Timestamp(sp["test"][1])

    # --- 評価対象と各時点のオッズ ---
    uni = mo.race_universe().filter(pl.col("date").is_between(first.date(), last.date()))
    sources = {tag(m): mo.pre_deadline_odds(m) for m in P["decision_minutes"]}
    if P["include_final"]:
        sources["final"] = mo.final_odds()
    df = uni
    for s, o in sources.items():
        cols = [pl.col("win_odds").alias(f"odds_{s}")]
        if "minutes_to_post" in o.columns:
            cols.append(pl.col("minutes_to_post").alias(f"mtp_{s}"))
        df = df.join(o.select("race_key", "umaban", *cols), on=["race_key", "umaban"], how="left")
    ocols = [f"odds_{s}" for s in sources]
    n_races_all = df["race_key"].n_unique()
    bad = df.filter(pl.any_horizontal([pl.col(c).is_null() | (pl.col(c) <= 0) for c in ocols]))["race_key"].unique()
    drop_by_src = {s: int(df.filter(pl.col(f"odds_{s}").is_null())["race_key"].n_unique()) for s in sources}
    if cfg["universe"]["common_races"]:
        df = df.filter(~pl.col("race_key").is_in(bad.implode()))
    pdf = df.to_pandas()
    pdf["date"] = pd.to_datetime(pdf["date"])
    pdf["split"] = ev.time_split(pdf["date"], pd.Timestamp(sp["valid"][0]), pd.Timestamp(sp["test"][0]),
                                 pd.Timestamp(sp["test"][1]) + pd.Timedelta(days=1))
    assert pdf["date"].max() < pd.Timestamp(sp["holdout_never_evaluate"][0])
    universe_info = {"n_races_before_common": n_races_all, "n_races_dropped_missing_odds": int(len(bad)),
                     "races_missing_odds_by_source": drop_by_src,
                     "n_races_by_split": pdf.groupby("split")["race_key"].nunique().to_dict(),
                     "n_dead_heat_races": int((pdf.groupby("race_key")["y"].sum() > 1).sum()),
                     "n_horses": len(pdf)}
    mtp = {s: pdf.groupby("split")[f"mtp_{s}"].describe(percentiles=[.1, .5, .9])[["mean", "10%", "50%", "90%"]]
           .round(2).to_dict("index") for s in sources if f"mtp_{s}" in pdf}
    print(json.dumps(universe_info, indent=1, default=str))

    # --- 確率 ---
    tr = pdf["split"] == "train"
    power_k = {}
    pcols = []
    for s in sources:
        for m in P["methods"]:
            col = f"p_{s}_{m}"
            k = None
            if m == "power_fit":
                k = mo.fit_power_k(pdf.loc[tr, ["race_key", f"odds_{s}", "y"]], odds=f"odds_{s}")
                power_k[s] = k
            pdf[col] = mo.market_probs(pdf[["race_key", f"odds_{s}"]], m, k=k, odds=f"odds_{s}", out=col)[col].to_numpy()
            pcols.append(col)
    print("power_fit k:", power_k)

    # --- 指標 ---
    E = cfg["eval"]
    B = E["bootstrap"]
    ref = f"p_{E['reference']['odds']}_{E['reference']['method']}"
    metrics = {}
    for split in ("train", "valid", "test"):
        d = pdf[pdf["split"] == split].rename(columns={"race_key": "race_id"})
        out = {}
        for c in pcols:
            r = ev.summary(d, c, bins=E["ece_bins"])
            if c != ref:
                dl = ev.delta_logloss(d, c, ref, n_boot=B["n_boot"], seed=cfg["seed"], level=B["level"])
                r.update(dlogloss_vs_ref=dl["delta"], dlogloss_ci=list(dl["ci"]), dlogloss_p=dl["p_value"])
            out[c.removeprefix("p_")] = r
        metrics[split] = out
        print(split, {k: round(v["logloss"], 5) for k, v in out.items()})

    py = E["per_year"]
    per_year = {}
    for s in py["odds"]:
        c = f"p_{s}_{py['method']}"
        sc = ev.race_scores(pdf.rename(columns={"race_key": "race_id"}), c).join(
            pdf.groupby("race_key")["date"].first().rename_axis("race_id"))
        g = sc.groupby(sc["date"].dt.year)
        per_year[f"{s}_{py['method']}"] = {int(y): {"logloss": float(v["logloss"].mean()), "n_races": len(v)}
                                           for y, v in g}
    # 年ごとの「最後の中間 − 確定」と「10 分前 − 確定」の差
    print("per-year logloss:", {k: {y: round(v["logloss"], 4) for y, v in d.items()} for k, d in per_year.items()})

    # --- 賭けのシミュレーション（健全性の確認） ---
    Bt = cfg["bets"]
    pdf["pay_odds"] = pdf["win_payout_odds"].fillna(0.0)
    pdf["y_pay"] = pdf["win_payout_odds"].notna().astype(int)
    dec = f"odds_{Bt['decision_odds']}"
    bets = {}
    for split in Bt["splits"]:
        d = pdf[pdf["split"] == split].rename(columns={"race_key": "race_id"})
        out = {}
        runs = [(m, f"p_{Bt['decision_odds']}_{m}", Bt["threshold"]) for m in Bt["methods"]]
        if Bt["all_horses_check"]:
            runs.append(("all_horses", f"p_{Bt['decision_odds']}_proportional", -1.0))
        for name, c, th in runs:
            r = ev.simulate_bets(d, c, decision_odds=dec, payout_odds="pay_odds", threshold=th, y="y_pay",
                                 n_boot=B["n_boot"], seed=cfg["seed"], level=B["level"])
            r.pop("bets", None)
            if r["n_bets"]:
                r["return_ratio"] = r["return"] / r["stake"]
            out[name] = r
        bets[split] = out
        print("bets", split, {k: (v["n_bets"], round(v.get("return_ratio", float("nan")), 4)) for k, v in out.items()})

    # 締切前オッズで見た控除（Σ1/odds）
    ovr = {s: float(pdf.assign(q=1 / pdf[f"odds_{s}"]).groupby("race_key")["q"].sum().median()) for s in sources}

    T = metrics["test"]
    V = metrics["valid"]
    head = {
        "test_logloss_final_prop": T["final_proportional"]["logloss"],
        "test_logloss_n10_prop": T["10_proportional"]["logloss"],
        "test_logloss_n10_powerfit": T["10_power_fit"]["logloss"],
        "test_logloss_last_prop": T["last_proportional"]["logloss"],
        "valid_logloss_n10_prop": V["10_proportional"]["logloss"],
        "valid_logloss_n10_powerfit": V["10_power_fit"]["logloss"],
        "test_dlogloss_n10_prop_vs_final": T["10_proportional"]["dlogloss_vs_ref"],
    }
    res = {
        "experiment": HERE.name, "status": "done", "git_hash": git_hash, "git_clean": clean,
        "data_version": cfg["data"]["version"], "seed": cfg["seed"],
        "split": f"{sp['train'][0][:4]}-{sp['train'][1][:4]}/{sp['valid'][0][:4]}-{sp['valid'][1][:4]}/"
                 f"{sp['test'][0][:4]}-{sp['test'][1][:4]} (provisional)",
        "metrics": head,
        "reference": ref.removeprefix("p_"),
        "universe": universe_info, "minutes_to_post": mtp, "power_fit_k": power_k,
        "median_overround": ovr,
        "by_split": metrics, "per_year": per_year, "bets": bets,
    }
    (HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float) + "\n",
                                       encoding="utf-8")
    print("written; git_clean =", clean)


if __name__ == "__main__":
    main()

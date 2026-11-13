"""オッズを使わない LightGBM の 3 本（JvLinkToImporter ML スターター風、自前の実装）。

- A: 3 着内の二値分類（binary）
- B: レース内の順位学習（lambdarank、関連度は着順から）
- C: 1 着の二値分類（binary）

どれもレース内で和 1 の単勝確率 p_win を出す。
C は予測確率をレース内で割って正規化する。A・B はスコア（A は log-odds、B は順位スコア）を
p ∝ exp(s·score) とし、温度 s を valid のレース単位 logloss 最小で 1 つ決める。
early stopping も valid だけで行う（test は最後に 1 回だけ評価する）。

使い方:
    uv run --extra ml python -m keiba_ai.lgbm_nomarket experiments/2026-11-14_lgbm-nomarket/config.yaml
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import yaml
from scipy import optimize

from keiba_ai import evaluate as ev
from keiba_ai import features as F

ROOT = Path(__file__).resolve().parents[2]
RACE = "race_key"


# --- 確率への変換 ------------------------------------------------------------

def _race_parts(df: pd.DataFrame, y: str):
    gid, _ = pd.factorize(df[RACE])
    n = int(gid.max()) + 1
    yv = df[y].to_numpy(float)
    tot = np.bincount(gid, weights=yv, minlength=n)
    return gid, n, yv / np.where(tot[gid] > 0, tot[gid], 1.0), tot > 0


def softmax_by_race(score: np.ndarray, gid: np.ndarray, n: int) -> np.ndarray:
    m = np.full(n, -np.inf)
    np.maximum.at(m, gid, score)
    e = np.exp(score - m[gid])
    return e / np.bincount(gid, weights=e, minlength=n)[gid]


def fit_temperature(df: pd.DataFrame, score: str, y: str, bounds) -> float:
    """p ∝ exp(s·score) の s を、レース単位の条件付き logloss 最小で決める。"""
    gid, n, t, has_win = _race_parts(df, y)
    sc = df[score].to_numpy(float)

    def nll(s):
        p = softmax_by_race(s * sc, gid, n)
        ll = np.bincount(gid, weights=-t * np.log(np.clip(p, ev.EPS, None)), minlength=n)
        return ll[has_win].mean()

    res = optimize.minimize_scalar(nll, bounds=tuple(bounds), method="bounded")
    return float(res.x)


# --- 学習 --------------------------------------------------------------------

def _split(df: pd.DataFrame, split_cfg: dict) -> pd.Series:
    out = pd.Series(pd.NA, index=df.index, dtype=object)
    for name in ("train", "valid", "test"):
        lo, hi = (pd.Timestamp(v) for v in split_cfg[name])
        out[(df["date"] >= lo) & (df["date"] <= hi)] = name
    return out


def _label(df: pd.DataFrame, mcfg: dict) -> np.ndarray:
    if mcfg["label"] == "relevance":
        k = mcfg["relevance_top"]
        pos = df["finish_pos"].to_numpy(float)
        return np.where(np.isnan(pos), 0, np.clip(k + 1 - pos, 0, None)).astype(int)
    return df[mcfg["label"]].to_numpy(int)


def _dataset(df, feats, mcfg, ref=None):
    kw = {}
    if mcfg["objective"] == "lambdarank":
        kw["group"] = df.groupby(RACE, sort=False).size().to_numpy()
    return lgb.Dataset(df[feats], label=_label(df, mcfg), categorical_feature=[c for c in F.CATEGORICAL if c in feats],
                       reference=ref, free_raw_data=False, **kw)


def train_one(name: str, mcfg: dict, cfg: dict, data: dict[str, pd.DataFrame], feats: list[str]):
    params = {**cfg["lgbm"]["params"], **mcfg.get("params", {}), "objective": mcfg["objective"],
              "seed": cfg["seed"]}
    dtr = _dataset(data["train"], feats, mcfg)
    dva = _dataset(data["valid"], feats, mcfg, ref=dtr)
    log = {}
    t0 = time.time()
    booster = lgb.train(
        params, dtr, num_boost_round=cfg["lgbm"]["num_boost_round"], valid_sets=[dva], valid_names=["valid"],
        callbacks=[lgb.early_stopping(cfg["lgbm"]["early_stopping_rounds"], first_metric_only=True,
                                      verbose=False),
                   lgb.log_evaluation(cfg["lgbm"]["log_every"]), lgb.record_evaluation(log)])
    info = {"best_iteration": booster.best_iteration, "train_seconds": round(time.time() - t0, 1),
            "best_valid": {k: float(v[booster.best_iteration - 1]) for k, v in log["valid"].items()}}
    return booster, info


def to_win_prob(name: str, mcfg: dict, booster, data: dict[str, pd.DataFrame], feats, cfg) -> dict:
    """スコアと p_win を各分割に付ける。温度は valid で決める。"""
    for d in data.values():
        d["score"] = booster.predict(d[feats], num_iteration=booster.best_iteration, raw_score=True)
    info = {"method": mcfg["prob"]}
    if mcfg["prob"] == "renormalize":
        for d in data.values():
            d["p_win"] = ev.renormalize(d.assign(_p=1 / (1 + np.exp(-d["score"]))), "_p", race=RACE)
    elif mcfg["prob"] == "softmax_temperature":
        s = fit_temperature(data["valid"], "score", "y_win", cfg["temperature"]["bounds"])
        info["temperature_s"] = s
        for d in data.values():
            gid, n = pd.factorize(d[RACE])[0], d[RACE].nunique()
            d["p_win"] = softmax_by_race(s * d["score"].to_numpy(float), gid, n)
    else:
        raise ValueError(mcfg["prob"])
    return info


def _git(*args) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def run(config_path: Path) -> dict:
    config_path = Path(config_path).resolve()
    exp_dir = config_path.parent
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    fcfg = F.FeatureConfig.from_dict(cfg["features"]["config"])
    if cfg["features"]["version"] != F.FEATURES_VERSION:
        raise ValueError(f"features version mismatch: {cfg['features']['version']} != {F.FEATURES_VERSION}")
    dirty = _git("status", "--porcelain", "--", *cfg["git_tracked_paths"])
    git_hash = _git("rev-parse", "HEAD")

    feats_pl = F.load_features(fcfg)
    df = feats_pl.to_pandas()
    df["date"] = pd.to_datetime(df["date"])
    for c in F.CATEGORICAL:
        df[c] = df[c].astype("category")
    feats = [c for c in F.FEATURES if c not in set(cfg["features"].get("exclude", []))]
    df["split"] = _split(df, cfg["split"])
    df = df[df["split"].notna()].reset_index(drop=True)
    data = {s: df[df["split"] == s].sort_values(["date", RACE, "umaban"]).reset_index(drop=True)
            for s in ("train", "valid", "test")}

    out_dir = ROOT / cfg["output"]["preds_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    ece_bins = cfg["eval"]["ece_bins"]
    results = {"models": {}, "uniform": {}}
    for s in ("valid", "test"):
        d = data[s].assign(p_unif=1.0 / data[s].groupby(RACE)["umaban"].transform("size"))
        results["uniform"][s] = ev.summary(d, "p_unif", y="y_win", race=RACE, bins=ece_bins)

    for name, mcfg in cfg["models"].items():
        print(f"== model {name}: {mcfg['objective']} label={mcfg['label']}", flush=True)
        booster, tinfo = train_one(name, mcfg, cfg, data, feats)
        pinfo = to_win_prob(name, mcfg, booster, data, feats, cfg)
        m = {s: ev.summary(data[s], "p_win", y="y_win", race=RACE, bins=ece_bins) for s in ("valid", "test")}
        gain = pd.Series(booster.feature_importance("gain"), index=booster.feature_name())
        top = (gain / gain.sum()).sort_values(ascending=False).head(cfg["eval"]["importance_top"])
        results["models"][name] = {**mcfg, "train": tinfo, "prob": pinfo, "metrics": m,
                                   "importance_gain_share": {k: round(float(v), 4) for k, v in top.items()}}
        print(json.dumps(results["models"][name]["metrics"], indent=1), flush=True)
        preds = pd.concat([d[["race_key", "umaban", "date", "split", "score", "p_win", "y_win", "finish_pos",
                              "horse_id"]] for d in data.values()], ignore_index=True)
        preds.to_parquet(out_dir / f"preds_{cfg['output']['model_prefix']}{name}.parquet", index=False)
        booster.save_model(str(out_dir / f"model_{cfg['output']['model_prefix']}{name}.txt"),
                           num_iteration=booster.best_iteration)

    flat = {}
    for name, r in results["models"].items():
        for s in ("valid", "test"):
            flat[f"{s}_logloss_{name}"] = r["metrics"][s]["logloss"]
    res = {
        "experiment": exp_dir.name, "status": "done", "git_hash": git_hash,
        "git_dirty_tracked_paths": dirty or None, "data_version": F.data_version(F.DATA_DIR, fcfg),
        "seed": cfg["seed"],
        "split": "/".join(f"{a[:4]}-{b[:4]}" for a, b in (cfg["split"][s] for s in ("train", "valid", "test"))),
        "metrics": flat,
        "n_rows": {s: len(d) for s, d in data.items()},
        "n_races": {s: int(d[RACE].nunique()) for s, d in data.items()},
        "n_features": len(feats), "features": feats,
        **results,
        "preds": {name: str((out_dir / f"preds_{cfg['output']['model_prefix']}{name}.parquet").relative_to(ROOT))
                  for name in cfg["models"]},
    }
    (exp_dir / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str) + "\n",
                                          encoding="utf-8")
    return res


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("config", type=Path)
    run(p.parse_args().config)


if __name__ == "__main__":
    main()

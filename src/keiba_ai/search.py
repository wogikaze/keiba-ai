"""仮説探索の共通の土台（ADR 0005）。市場オフセット LightGBM を設定で変えて学習し、ADR 0004 の指標で評価する。

母集団は ``derived/preds_offset_lgbm.parquet``（market-combination と同じレース・出走馬、p_mkt は 10 分前 × power_fit）。
設定（実験の config.yaml の ``search``）:

    features: [v1, market_v1]       # 特徴量のブロック。v1 = features.FEATURES、market_v1 = features_market.FEATURES
    drop: [...]                     # 除く列
    params: {...}                   # LightGBM
    seeds: [42]                     # 複数なら生のスコア（オフセットの補正 f）を平均する
    train_from: "2004-01-01"        # 学習に使う最初の日
    weight_halflife_years: null     # 学習の重みを新しいほど大きく（半減期・年）
    num_boost_round, early_stopping_rounds
    init: p_mkt                     # オフセット（log p）。p_mkt のほか、p_offset（前段の予測）も可

返り値の指標: valid・test の ΔlogLoss（vs p_mkt、レース単位・開催日単位）、年ごとの Δ、Benter の α（valid で当てはめ、
test で評価）、プラセボ（レース内で予測を並べ替えたときの α と Δ）、特徴量の gain。
"""

from __future__ import annotations

import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import polars as pl

from keiba_ai import evaluate as ev
from keiba_ai import features as F
from keiba_ai import features_market as FM
from keiba_ai import market_offset as mof

ROOT = Path(__file__).resolve().parents[2]
RACE = "race_id"
BASE = F.DATA_DIR / "derived" / "preds_offset_lgbm.parquet"
FEATURE_CONFIG = dict(min_year=1986, not_started_codes=[1, 2, 3], n_last=5, n_recent_mean=3,
                      rate_prior_strength=20.0, recent_days=365, speed_min_n=30, behind_clip=[-2.0, 10.0],
                      fig_clip=[-10.0, 10.0], training_window_days=14)


def blocks() -> dict[str, list[str]]:
    return {"v1": list(F.FEATURES), "market_v1": list(FM.FEATURES)}


def load_frame(extra: list[pl.DataFrame] | None = None) -> pd.DataFrame:
    base = pl.read_parquet(BASE)
    base = base.with_columns(pl.col("umaban").cast(pl.Int16))
    fv1 = F.load_features(F.FeatureConfig.from_dict(FEATURE_CONFIG)).select("race_key", *F.FEATURES)
    fv1 = fv1.with_columns(pl.col("umaban").cast(pl.Int16))
    fm = FM.load_market_features().with_columns(pl.col("umaban").cast(pl.Int16))
    df = base.join(fv1, on=["race_key", "umaban"], how="left").join(fm, on=["race_key", "umaban"], how="left")
    for e in extra or []:
        df = df.join(e.with_columns(pl.col("umaban").cast(pl.Int16)), on=["race_key", "umaban"], how="left")
    pdf = df.to_pandas()
    pdf["date"] = pd.to_datetime(pdf["date"])
    pdf[RACE] = pdf["race_key"]
    for c in F.CATEGORICAL:
        if c in pdf:
            pdf[c] = pdf[c].astype("category")
    return pdf.sort_values(["date", "race_key", "umaban"]).reset_index(drop=True)


def feature_list(cfg: dict, pdf: pd.DataFrame) -> list[str]:
    b = blocks()
    cols = []
    for name in cfg["features"]:
        cols += b[name] if name in b else [name]
    drop = set(cfg.get("drop") or [])
    return [c for c in dict.fromkeys(cols) if c not in drop and c in pdf.columns]


def train(pdf: pd.DataFrame, cfg: dict, seed: int) -> tuple[np.ndarray, dict]:
    """1 つの seed で学習し、全行の補正 f（生のスコア）を返す。"""
    feats = feature_list(cfg, pdf)
    cats = [c for c in F.CATEGORICAL if c in feats]
    init = np.log(np.clip(pdf[cfg.get("init", "p_mkt")].to_numpy(float), ev.EPS, None))
    tr = (pdf["split"] == "train") & (pdf["date"] >= pd.Timestamp(cfg.get("train_from", "2004-01-01")))
    va = pdf["split"] == "valid"
    w = None
    if cfg.get("weight_halflife_years"):
        age = (pd.Timestamp("2019-01-01") - pdf.loc[tr, "date"]).dt.days / 365.25
        w = np.power(0.5, age / cfg["weight_halflife_years"]).to_numpy()
    obj = mof.RaceSoftmax(pdf.loc[tr, RACE].to_numpy(), pdf.loc[tr, "y"].to_numpy(), weight=w)
    ev_va = mof.RaceSoftmax(pdf.loc[va, RACE].to_numpy(), pdf.loc[va, "y"].to_numpy())
    dtr = lgb.Dataset(pdf.loc[tr, feats], label=pdf.loc[tr, "y"].to_numpy(float), init_score=init[tr.to_numpy()],
                      categorical_feature=cats, free_raw_data=False)
    dva = lgb.Dataset(pdf.loc[va, feats], label=pdf.loc[va, "y"].to_numpy(float), init_score=init[va.to_numpy()],
                      categorical_feature=cats, reference=dtr, free_raw_data=False)
    params = {**cfg["params"], "objective": obj.objective, "metric": "None", "seed": seed, "verbose": -1}
    log = {}
    t0 = time.time()
    b = lgb.train(params, dtr, num_boost_round=cfg.get("num_boost_round", 5000), valid_sets=[dva],
                  valid_names=["valid"], feval=mof.make_feval({id(dva): ev_va}),
                  callbacks=[lgb.early_stopping(cfg.get("early_stopping_rounds", 200), verbose=False),
                             lgb.record_evaluation(log)])
    f = b.predict(pdf[feats], num_iteration=b.best_iteration, raw_score=True)
    gain = pd.Series(b.feature_importance("gain"), index=b.feature_name())
    info = {"seed": seed, "best_iteration": b.best_iteration, "train_seconds": round(time.time() - t0, 1),
            "valid_logloss_best": float(log["valid"]["race_logloss"][b.best_iteration - 1]),
            "n_features": len(feats), "n_train_rows": int(tr.sum()),
            "gain_share_top25": {k: round(float(v), 4) for k, v in
                                 (gain / gain.sum()).sort_values(ascending=False).head(25).items()}}
    return f, info


def predict(pdf: pd.DataFrame, cfg: dict) -> tuple[np.ndarray, list[dict]]:
    fs, infos = [], []
    for s in cfg.get("seeds", [42]):
        f, info = train(pdf, cfg, s)
        fs.append(f)
        infos.append(info)
        print("trained", info["seed"], info["best_iteration"], info["valid_logloss_best"], flush=True)
    init = np.log(np.clip(pdf[cfg.get("init", "p_mkt")].to_numpy(float), ev.EPS, None))
    gid, n = mof.group_ids(pdf[RACE])
    return mof.softmax_by_group(init + np.mean(fs, axis=0), gid, n), infos


def evaluate(pdf: pd.DataFrame, p: str, ref: str = "p_mkt", n_boot: int = 2000, seed: int = 42,
             placebo_rep: int = 5) -> dict:
    out = {}
    for s in ("valid", "test"):
        d = pdf[pdf["split"] == s]
        out[s] = {c: {k: v for k, v in ev.delta_logloss(d, p, ref, race=RACE, cluster=cl, n_boot=n_boot,
                                                       seed=seed).items()
                      if k in ("delta", "ci", "se", "logloss_model", "logloss_ref", "n_races", "n_clusters")}
                  for c, cl in (("race", None), ("date", "date"))}
    te = pdf[pdf["split"] == "test"]
    out["test_by_year"] = {int(y): float(ev.delta_logloss(g, p, ref, race=RACE, n_boot=10)["delta"])
                           for y, g in te.groupby(te["date"].dt.year)}
    # Benter: valid で α・β、test で評価
    va = pdf[pdf["split"] == "valid"]
    fit = ev.fit_benter(va, [p, ref], race=RACE)
    out["benter_valid_fit"] = {"alpha": fit["coef"][p], "beta": fit["coef"][ref],
                               "alpha_se": fit["se"][p], "beta_se": fit["se"][ref]}
    # プラセボ: レース内で並べ替えた予測は α ≈ 0、Δ ≈ 0（並べ替えた予測そのものの Δ は大きく正）
    rng = np.random.default_rng(seed)
    pl_alpha = []
    for _ in range(placebo_rep):
        d = va.copy()
        d["_shuf"] = ev.shuffle_within_race(d, p, rng, race=RACE).to_numpy()
        f2 = ev.fit_benter(d, ["_shuf", ref], race=RACE)
        pl_alpha.append((f2["coef"]["_shuf"], f2["se"]["_shuf"]))
    out["placebo_shuffle_alpha"] = [{"alpha": a, "se": s} for a, s in pl_alpha]
    return out


def headline(r: dict) -> dict:
    return {"valid_delta": r["valid"]["race"]["delta"], "valid_delta_se_date": r["valid"]["date"]["se"],
            "test_delta": r["test"]["race"]["delta"], "test_delta_ci_date": r["test"]["date"]["ci"],
            "test_logloss": r["test"]["race"]["logloss_model"], "valid_logloss": r["valid"]["race"]["logloss_model"],
            "test_all_years_negative": all(v < 0 for v in r["test_by_year"].values())}

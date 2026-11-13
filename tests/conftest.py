"""合成データ: 真の強さ s = a + b。市場は a だけ、モデルは b（とノイズ）を知る。"""

import numpy as np
import pandas as pd
import pytest


def softmax_by_race(x, race):
    e = np.exp(x - x.groupby(race).transform("max"))
    return e / e.groupby(race).transform("sum")


def make_races(n_races=3000, seed=0, b_scale=0.0, noise=0.5, takeout=0.2):
    rng = np.random.default_rng(seed)
    sizes = rng.integers(8, 17, n_races)
    race = np.repeat(np.arange(n_races), sizes)
    date = pd.Timestamp("2020-01-04") + pd.to_timedelta(np.repeat(np.arange(n_races) // 24, sizes) * 7, "D")
    df = pd.DataFrame({"race_id": race, "date": date, "horse": np.arange(len(race))})
    a, b = rng.normal(0, 1.0, len(df)), rng.normal(0, b_scale, len(df))
    r = df["race_id"]
    df["p_true"] = softmax_by_race(pd.Series(a + b), r)
    df["p_market"] = softmax_by_race(pd.Series(a), r)
    df["p_model"] = softmax_by_race(pd.Series(b + rng.normal(0, noise, len(df))), r)
    # 勝ち馬を真の確率で引く
    u = rng.random(n_races)[race]
    cum = df.groupby("race_id")["p_true"].cumsum()
    df["y"] = ((cum - df["p_true"] <= u) & (u < cum)).astype(int)
    df["odds"] = (1 - takeout) / df["p_market"]
    return df


@pytest.fixture(scope="session")
def races():
    return make_races

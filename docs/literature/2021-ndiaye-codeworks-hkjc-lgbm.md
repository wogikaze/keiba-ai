---
title: Use Case #3: Horse Racing Prediction: A Machine Learning Approach (Part 1, Part 2)
authors: Idrissa Ndiaye, Koffi Cornelis (CodeWorks Paris)
year: 2021
venue: Medium（CodeWorks Paris）＋ GitHub codeworks-data/mvp-horse-racing-prediction
url: https://medium.com/codeworksparis/horse-racing-prediction-a-machine-learning-approach-part-2-e9f5eb9a92e9
topic: practitioner
tags: grey-literature, hong-kong, kaggle-hkracing, lightgbm, neural-network, ensemble, hyperopt, monthly-retraining, baseline-strategies, final-odds-leak
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# Kaggle 香港データ（1997–2005）で LightGBM＋NN を月次再学習し、素朴な賭け方と収支を比べた 2 部作

> 一言で: Kaggle の香港競馬データで、まず「ランダム・1 番人気・内枠」の素朴な賭け方がすべて赤字になることを確かめた（Part 1）。次に LightGBM と 1 層 NN を月ごとに学習し直して 2005 年 1〜8 月の 470 レースで賭けた（Part 2）。単勝は 470 ドル投じて 8.7 ドルの損、複勝は +336.7 ドルだったが、黒字は 1 か月分の大穴に依存していた。著者ら自身が「運が良かった」と書いている。

原本は Part 2（主）。Part 1 と GitHub の README を添付している。

## データ

- Kaggle の `gdaley/hkracing`（香港 1997–2005、6,348 レース、のべ 4,405 頭。README では 6,349 レース）。元の列は 104 個（Part 2「Describe the initial data」）。
- 2005 年 1 月より前の 5,878 レースを開発用、2005 年以降の 470 レースをテスト用にした（Part 1「Dataset」）。
- 複勝オッズ（place_odds）が欠けたレースは複勝の評価から除いた。そのため複勝は 249 レース・746 点で、最後の 2 か月は評価できない。

## 特徴量

- 体重の変化、前走からの間隔、騎手の乗り替わり、過去の着順など。`extract_features.py` で日付を使って大量に作り、1,618 特徴になった（Part 2「Feature engineering」）。
- LightGBM の重要度（分割回数）で上位に来たのは `win_odds` と `declared_weight` 関連（Part 2「LGBM feature importance」）。

## モデルと目的変数

- 単勝: レースごとに 1 着を当てる分類。LightGBM（Hyperopt の TPE で調整）と Keras の NN（96 ユニット 1 層、40 エポック、バッチ 100）。
- アンサンブルは確率の加重平均で、LightGBM 0.7・NN 0.3。
- 複勝: LightGBM は単勝用のモデルをそのまま使い、NN は 2〜3 クラスを当てるよう学習し直した。頭数 7 頭以下なら 2 頭、それ以上なら 3 頭を選ぶ。

## 評価

- **月次の拡張窓**: Set 1 は 2005 年より前で学習して 1 月を予測、Set 2 はそれに 1 月を足して 2 月を予測、…と 8 月まで続ける（4 月は開催なしで Set 4 は欠番）。時系列のウォークフォワードになっている。
- **賭け方**: 1 レース 1 ドルの定額。単勝はモデルの 1 位に、複勝は上位 2〜3 頭に賭ける。期待値による選別はしていない。
- **払戻**: データセットの `win_odds` / `place_odds` を掛ける。どの時点のオッズかは書かれていないが、Kaggle データの値は確定オッズと考えられる。
- **指標**: 的中率と収支。著者らは「的中率は良い指標ではない。多く当てても低オッズなら負ける」と書き、収支を主にしている（Part 2「And what about metrics?」）。

## 結果

- **素朴な賭け方（Part 1、470 レース・各 1 ドル）**:
  - 単勝: ランダムは 17 的中・払戻 266.4 ドル・収支 −203.6 ドル。1 番人気は約 3 回に 1 回当たるが −61.7 ドル。2 番枠固定も赤字。
  - 複勝（746 点）: ランダム −152.7 ドル、人気順は的中率ほぼ 50% でも −151.5 ドル、内枠 −174.6 ドル。
  - 探索的な観察: 1〜3 番枠は 10 番枠以降より勝率が 3 ポイント高い。3〜4 歳がよく勝つ。
- **LightGBM 単独（Set 1 = 2005 年 1 月）**: 20 戦目で約 +20 ドル、70 戦目で約 −13 ドル（Part 2「The LGBM approach」）。Hyperopt で選んだパラメータは Set 1 で +27.4 ドルの収支を出したもの。
- **NN（Set 1）**: 平均オッズが 1 番人気の約 2 倍の馬を選んでいた。
- **単勝アンサンブル（全 7 か月）**: 470 ドル投資、−8.7 ドル（Part 2「Consolidated results … for winner」）。アンサンブルの収支は単独モデルより良いが、的中率は LightGBM 単独より低い。
- **複勝アンサンブル**: 平均的中率は NN 30%・LightGBM 42%・統合 41.3%。黒字は Set 2（2005 年 2 月）だけで、NN がこの月に平均オッズ 10.48 の穴馬を当てた。最終まとめでは複勝 +336.7 ドル。

## 落とし穴と教訓（著者の記述から）

- 1 番人気に賭けると的中率は高いが、控除率で負ける。モデルの勝ち方は「人気でない馬が当たったときに大きい」ことにある。
- 複勝の黒字は 1 か月の大穴次第で、著者らは「運が最も重要な特徴量だった」と書いている。

## 批判的に読む

- **テスト期間でハイパーパラメータを選んでいる**。Hyperopt の目的関数は Set 1（2005 年 1 月、つまりテスト月）の収支で、そのパラメータを全月に使った。Set 1 の成績はリークを含む。
- **確定オッズが特徴量に入っている**。`win_odds` が重要度上位で、データセットの値は確定オッズと考えられる。投票時点では分からない情報である。払戻も同じ確定オッズで計算している。
- 470 レース・7 か月で、単勝 −1.9%（−8.7/470）は「控除率約 17.5% の市場でほぼ損益なし」にあたり、市場を 15 ポイント程度上回っている。確定オッズのリークがあれば説明がつく水準で、そのまま優位とは読めない。
- 複勝はオッズ欠損で月が抜けていて、+336.7 ドルは 1 か月の外れ値で決まっている。
- 期待値による選別をしていない（常にモデル 1 位に賭ける）。確率モデルの良し悪しと賭け方の良し悪しを分けて評価していない。

## keiba-ai での使い方

- **素朴な基準戦略を必ず並べる**: ランダム・1 番人気・内枠（JRA なら枠順）の回収率を同じテスト期間で出し、モデルの回収率と並べる。Part 1 の構成は、そのまま実験テンプレートの「ベースライン」節に使える。
- **月次の拡張窓**: 月ごとに学習し直すウォークフォワードは、keiba-ai の時系列分割の具体的な形として採れる。ただしハイパーパラメータは最初のテスト月より前の検証期間で決める。
- **反面教師**: 確定オッズを特徴にしたモデルと、オッズを除いたモデルを必ず両方報告する。

## 関連ノート

- [Leung & Leung 2023](./2023-leung-annotated-benter-paper.md) — 同じ香港市場で、大衆の確率がどれだけ正確か。
- [Dhital ほか 2018](./2018-dhital-nycdsa-hkjc-neural-net.md)、[Sankari ほか 2019](./2019-sankari-nycdsa-hkjc-kelly.md) — 香港データでの他の受講生・実践者の記録。
- [Ke ほか 2017](./2017-ke-lightgbm.md) — LightGBM。
- [Hubáček ほか 2019](./2019-hubacek-exploiting-betting-market-ml.md) — 市場オッズを特徴に入れることの問題（モデルが市場に寄る）。
- [Bergmeir ほか 2018](./2018-bergmeir-cv-time-series.md) — 時系列での検証。

## 検索語

香港競馬 Kaggle hkracing, LightGBM ニューラルネット アンサンブル 競馬, 月次再学習, 1番人気 回収率, 内枠有利, 複勝 収支, Hong Kong horse racing Kaggle gdaley, baseline betting strategies favourite draw, monthly expanding window, Hyperopt profit objective

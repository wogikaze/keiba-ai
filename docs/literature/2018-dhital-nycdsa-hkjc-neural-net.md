---
title: Data Analyzing Horse Racing
authors: Basant Dhital, SangYeon Choi, Jiwon Cha, Tristan Dresbach, Karim El Zaatari
year: 2018
venue: NYC Data Science Academy ブログ（受講生の卒業制作、RaceQuant との共同）
url: https://nycdatascience.com/blog/student-works/data-analyzing-horse-racing/
topic: practitioner
tags: grey-literature, hong-kong, hkjc, neural-network, kelly, fractional-kelly, smoczynski-tomkins, bootcamp-capstone, random-split
verified: fulltext
importance: low
source: downloaded
source_version: web
---

# 香港競馬の勝率 NN と多頭 Kelly（NYCDSA 卒業制作、2018）

> 一言で: 香港の 2015〜2018 年前半 2,384 レースで NN の勝率モデルを作り、Smoczynski–Tomkins 型の多頭同時 Kelly で配分した。ランダムに選んだ 541 レースで「賭け金に対する ROI 19.76%、元手 10 万ドルが 105 万ドル」と報告した。ただし分割はランダムで、手法の詳細は NDA で伏せられている。

## データ

- 予測会社 RaceQuant が提供した HKJC の全レース。2015〜2017 年と 2018 年第 1・2 四半期。特徴量は 81 個（「Objective」の節）。
- 2,384 レース、のべ 24,863 頭（「Feature Cleaning and Engineering」の節）。
- 学習 1,843 レース（77.31%）、テスト 541 レース（「Data Outcome」の表）。目的の節では「データから無作為に選んだ 540 レース」でバックテストすると書いている。

## 特徴量

- 欠損補完: 初騎乗の騎手・初出走厩舎の勝率は 10% と置いた。香港に来る騎手・調教師は海外で実績があるから、という理由。
- 馬体重: 「勝ったときの体重からの乖離率」と「平均体重からの乖離率」を作った。
- RaceQuant 提供の 81 特徴の中身（スピード指数など）は NDA で非公開。

## モデルと目的変数

- 目的変数は 1 着かどうか。多くの特徴と勝率の関係が線形でなかったため、複数のモデルを試して NN を採用した。「勝ち馬を選べる確率を最大化するよう」調整したとある。構造やレース内での正規化の有無は書かれていない。

## 賭け方

- まず Kelly 基準を試したが、賭け比率が大きすぎて早期に破産した。さらに、1 レース 14 頭への賭けは互いに排他的なのに、Kelly は独立な賭けを前提にしている。
- 対策 1: Kelly 比率に 0.2 を掛ける（分数 Kelly）。
- 対策 2: 「Peter Tompkin の論文」による多頭同時最適化に切り替えた。手順は、払戻オッズから市場確率を出す → 控除率込みの期待収益率を計算して降順に並べる → 集合 S に順に加え、条件を満たさなくなったら止める → 最適比率を計算。この比率にも 0.03 を掛けた。題名から見て、これは Smoczynski & Tomkins (2010) の明示解である。

## 結果（「Data Outcome」の表）

- 賭けた回数 1,953（1 レース平均 3.61 点、可能な賭けの 29.78%）。的中 143。
- 予測 1 位の馬が 1 着だった割合 26.38%。
- 最大の賭け 28,774.20 ドル、最小 1.30 ドル。平均ネット勝ちオッズ 5.38。
- 元手 10 万ドル → 最低 91,912.05 ドル → 最高 1,418,354.18 ドル → 最終 1,054,003.96 ドル。
- 総賭け金 5,333,083.60 ドル、**賭け金に対する ROI 19.76%**、総 ROI 1054%。

## 批判的に読む

- **ランダム分割**。テストの 541 レースは期間全体から無作為に選ばれている。同じ馬の後の走りが学習側に入るので、馬・騎手の集計特徴を通じて未来の情報が漏れうる。時系列の外挿としての成績ではない。
- **オッズの時点が不明**。賭け金の計算と払戻に確定オッズを使ったとみられる。実際にはその時点で賭けられない。2.8 万ドルの賭けがオッズに与える影響（プール規模の制約）も考慮されていない。
- **複利の総 ROI は誤解を招く**。1054% は資金を再投資した結果で、優位の大きさは賭け金 ROI 19.76% のほうで見るべきである。香港の控除率約 17.5% を考えると、19.76% の黒字は非常に大きい。Benter が報告した水準（総売上の 0.25〜0.5%）と比べても異常で、リークか過学習を疑うべき値である。
- 541 レース・的中 143 回では信頼区間が広い。分数 Kelly の係数 0.2 と 0.03 も同じテストデータで選ばれた可能性がある。
- NDA で手法が伏せられているため、再現はできない。

## 落とし穴と教訓（著者の記述から）

- 素の Kelly は過大で破産する。排他的な多頭賭けには独立前提の Kelly ではなく同時最適化が必要。これは実務上の教訓として正しい。

## keiba-ai での使い方

- **反面教師**: ランダム分割・確定オッズ・テストで調整した配分係数が重なると、ROI がどれほど膨らむかの実例。keiba-ai のバックテスト規約（時系列分割のみ、投票時点オッズ）の根拠として ADR に引ける。
- **多頭同時 Kelly の実装**: 単勝で 1 レースに複数頭へ賭けるなら Smoczynski–Tomkins の明示解を使う。その場合も分数係数は検証期間で決め、テストでは固定する。

## 関連ノート

- [Sankari ほか 2019（NYCDSA の翌年度チーム）](./2019-sankari-nycdsa-hkjc-kelly.md) — 同じ RaceQuant との共同で、ランダム 80/20 分割を 500 回繰り返した。
- [Smoczynski & Tomkins 2010](./2010-smoczynski-explicit-kelly-horse-races.md) — 本稿が使った多頭 Kelly の明示解。
- [Benter 1994](./2019-benter-model.md) — 現実的な利益水準の目安。
- [Leung & Leung 2023](./2023-leung-annotated-benter-paper.md) — 香港の大衆確率の精度。
- [Bergmeir ほか 2018](./2018-bergmeir-cv-time-series.md)、[Bailey ほか 2017](./2017-bailey-probability-backtest-overfitting.md) — 分割とバックテストの過学習。

## 検索語

香港競馬 ニューラルネット 勝率, NYC Data Science Academy 競馬, RaceQuant, 多頭 Kelly 明示解, 分数ケリー, ランダム分割 リーク, Hong Kong horse racing neural network capstone, explicit Kelly multiple horses, betting ROI 19.76%

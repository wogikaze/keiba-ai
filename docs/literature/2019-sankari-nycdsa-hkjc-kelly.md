---
title: Horse Races: Can Machine Learning Make A Winning Proposition?
authors: Michael Sankari, Matthew Rautionmaa, Eric Adlard, David Levy, Marc Hasson, David Felsen
year: 2019
venue: NYC Data Science Academy ブログ（受講生の卒業制作、RaceQuant との共同）
url: https://nycdatascience.com/blog/student-works/can-machine-learning-make-horse-races-a-winning-proposition/
topic: practitioner
tags: grey-literature, hong-kong, hkjc, xgboost, logistic-regression, kelly, monte-carlo, feature-selection, random-split, bootcamp-capstone
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 香港 2 シーズンでロジスティック回帰〜XGBoost と分数 Kelly を比較（NYCDSA 卒業制作、2019）

> 一言で: 香港の 2016–17・2017–18 シーズン（1,600 レース超）で勝率モデル 5 種を作り、5% 配分の改変 Kelly で賭けた。ランダム 80/20 分割を 500 回繰り返すと、XGBoost が賭け金 ROI 平均 14.5%・中央値 13.5% で最良だった。特徴を減らしたモデルほど良く、1 シーズンだけの成績はシミュレーション全体より楽観的だった、という観察が有用。

## データ

- RaceQuant が提供した HKJC の 1,600 レース超（2016–17 と 2017–18 の 2 シーズン）。
- 単勝プールの控除率 17.5% を越えることが黒字の条件、と明記している。

## 特徴量

- 「勝ったときの平均体重に近い」ことを示す二値フラグ。
- RaceQuant のアナリストが計算したスピード指数を、そのクラスの典型的な勝ち馬と比べた値。
- 体重変化、前走からの日数、香港初出走か、前走勝利か。直近の勝利を重く見た加重勝率。
- 過去レーティング、過去の距離・コース、調教、バリアトライアル、騎手と前騎手の勝率・勝数・騎乗数などの欠損を項目ごとに補完した。
- 相関行列・ランダムフォレストの重要度・正規化した係数で特徴を評価し、1 つずつ足して比べた。

## モデル

- 走破時計の線形回帰→時計分布→レースのシミュレーション、という当初案は、Q-Q プロットや Box-Cox 変換で残差を調べた結果、線形の前提に無理があると判断して捨てた。
- 代わりにロジスティック回帰と分類モデル（ランダムフォレスト、XGBoost、LightGBM、CatBoost）で勝率を出した。レース内で確率を正規化したかどうかは書かれていない。

## 賭け方

- Kelly 基準で、1 レースに資金の 5% を配分する分数方式に落ち着いた。
- 通常の Kelly 式を「ごくわずかに」改変すると、どの確率モデルでも成績が大きく良くなった。改変は低オッズの「コンセンサス馬」への賭けを増やす方向だという。式は公開されていない。

## 結果

- **縮小ロジスティックモデル 4 種**（1 シーズンでの検証。表）: 賭け数 700〜762、1 レース 4.3〜4.7 点。賭け金 ROI は 18.9% / 23.5% / 22.5% / 18.3%、最終資金 24.6〜29.5 万ドル、勝ち馬的中率 29.8〜32.3%。一方で最低資金は 67,849〜72,924 ドルまで落ち、著者らは下振れを懸念した。100 以上の変数を持つフルモデルより、どの縮小版も良かった。
- **500 シーズンのモンテカルロ**（ランダム 80/20 分割の繰り返し）: 最終資金は平均 151,637 ドル、中央値 138,713、最小 71,062、最大 388,576。
- **XGBoost（最良）**: 1 レース 7.5 点、賭け数約 1,205、賭け金総額 約 31.5 万ドル（平均）。**賭け金 ROI 平均 14.5%・中央値 13.5%**、資金 ROI 51.6% / 38.7%。最大の賭け 3,842 ドル、最低資金 91,273 ドル（平均）。

## 落とし穴と教訓（著者の記述から）

- 特徴を盛りすぎると確率が悪くなる。縮小モデルのほうが一貫して良かった。
- 1 シーズンの検証で良く見えたモデルは、多数のシミュレーションで成績が下がった。著者らはシーズン間でモデルや特徴の当たり外れが変わる可能性（過学習・偏り）を自分たちで議論している。

## 批判的に読む

- **ランダム分割**。「モンテカルロ」はレース単位のランダム 80/20 の繰り返しで、時系列ではない。同一馬の未来の走りが学習に入るので、馬・騎手の集計特徴がリークしうる。500 回の平均は分散を減らすだけで、リークの偏りは消えない。
- **オッズの時点と市場影響**が書かれていない。確定オッズで賭け金と払戻を計算したとみられる。
- 改変 Kelly の中身が非公開で、検証の自由度がどれだけあったか分からない。
- 2 シーズン・1,600 レースは小さい。控除率 17.5% の市場で 14% 台の黒字は、Benter の報告水準と比べて大きすぎる。前年度の NYCDSA チーム（[Dhital ほか 2018](./2018-dhital-nycdsa-hkjc-neural-net.md)）の 19.76% と同じく、上振れとみるべきである。
- 価値があるのは定性的な観察のほう。「縮小モデルのほうが良い」「1 期間の成績はシミュレーション分布の上側に出やすい」。

## keiba-ai での使い方

- **期間の分布で評価する**: 単一のテスト期間ではなく、時系列のウォークフォワードを複数の窓で回し、ROI の分布（中央値・下側分位・最低資金）を報告する。この記事の発想を、ランダム分割ではなく時系列でやり直す形で取り入れる。
- **特徴の縮小を試す**: 全部入りのモデルと、重要度上位だけの縮小モデルを、logloss と ROI の両方で比べる実験を一つ立てる価値がある。
- **最低資金（ドローダウン）を記録する**: results.json に ROI だけでなく最大ドローダウンを入れる。

## 関連ノート

- [Dhital ほか 2018](./2018-dhital-nycdsa-hkjc-neural-net.md) — 前年度の NYCDSA × RaceQuant チーム。
- [Kelly 1956](./1956-kelly-information-rate.md)、[MacLean ほか 2010](./2010-maclean-kelly-good-bad-properties.md)、[Baker & McHale 2013](./2013-baker-kelly-parameter-uncertainty.md) — 分数 Kelly とその理由。
- [Benter 1994](./2019-benter-model.md)、[Leung & Leung 2023](./2023-leung-annotated-benter-paper.md) — 同じ香港市場の基準。
- [Bergmeir ほか 2018](./2018-bergmeir-cv-time-series.md)、[Cerqueira ほか 2020](./2020-cerqueira-time-series-performance-estimation.md) — 時系列での性能推定。

## 検索語

香港競馬 XGBoost 回収率, 分数ケリー 5%, モンテカルロ 80/20 分割, 特徴量削減, NYC Data Science Academy, RaceQuant, Hong Kong horse racing XGBoost Kelly, reduced logistic model, simulated seasons bankroll

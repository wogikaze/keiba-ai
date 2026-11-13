---
title: Hong Kong Horse Racing Prediction
authors: anton-schwarberg
year: 2025
venue: GitHub
url: https://github.com/anton-schwarberg/Hongkong-Horse-Racing-Prediction
topic: practitioner
tags: grey-literature, hong-kong, hkjc, lightgbm, lambdarank, xgboost-ranker, calibration, target-encoding, top3, no-odds
verified: fulltext
importance: low
source: downloaded
source_version: web
---

# 香港競馬16季の3着内予測: ランカーは較正で負けたので分類器を選んだ

> 一言で: HKJC の2009〜2025年の16季をスクレイピングし、ロジスティック回帰、LightGBM 分類器、LightGBM ランカー、XGBoost ランカーで3着内を予測した個人のパイプライン。最新季をテストにして AUC 0.726、1番手の3着内率 52.9%。ランカーは Brier と log loss では良く見えたが、レース内 softmax の確率が 0.05〜0.55 に押し込められて較正が悪く、分類器を採用した。オッズは使わず、回収率の評価はない。

## データ

- HKJC 公式サイトの結果ページ、2009〜2025年の16季（「What this project does」）。年ごとの CSV をスクレイパーで作る。
- 各馬の公式レーティング（`Rtg.`）は取れておらず、レースのレーティング帯（例「60-40」）だけ。著者は、これを入れれば AUC が 0.78 を超えるだろうと書いている。

## 特徴量

- 直近成績の rolling 統計、馬体重の推移、レース内のパーセンタイル順位、馬・騎手・調教師の**拡張窓（expanding）ターゲットエンコーディング**。87特徴量。
- 欠損補完の統計量、ターゲットエンコーディング、検証分割をすべて先読みが起きない形で計算する、と書いている。
- 単勝オッズは意図的に使わない。

## モデルと評価

- 時系列分割: 季 1〜14 を学習、15 を検証、16 をテスト。
- 4モデルを Brier、log loss、較正曲線、Top-1 / Top-3 の3着内率で比較。SHAP、頭数別の性能も出す（`05_Modelling.ipynb`）。

## 結果

「Results」節（テスト季）: 採用モデル LightGBM 分類器。

| 指標 | 値 |
|---|---|
| ROC-AUC | 0.726 |
| PR-AUC | 0.450 |
| 1番手が3着内に入った率 | 52.9%（12頭立ての無作為は約25%） |
| 上位3頭のうち少なくとも1頭が3着内 | 87.1% |

- 「Why LightGBM Classifier and not a Ranker?」: ランカー2つは Brier と log loss で勝って見えたが、レース内 softmax による確率は 0.05〜0.55 程度に圧縮され、高確信の領域に届かない。Kelly で賭け金を決めるなら「65%」が本当に65%であることが重要なので、分類器を選んだ。

## 落とし穴と教訓

- 実運用には、レース当日の出馬表から同じ87特徴量を作る関数、出馬表のスクレイパー、学習済みモデルと補完値の保存が足りない、と「How could you actually use this?」で整理している。

## 批判的に読む

- 回収率の評価がなく、市場（オッズ）との比較もない。AUC 0.726 が市場の情報にどれだけ足すかは分からない。
- 1番手の3着内率 52.9% は、1番人気の3着内率（一般に60%前後）より低い可能性が高い。
- ランカーの softmax 確率が圧縮されたのは、softmax の温度（スコアのスケール）を学習していないためと考えられる。ランカーの出力に温度スケーリングや条件付きロジットの係数を当てれば解消できる余地があり、「ランカーは較正が悪い」は一般論ではない。
- 3着内の目的に対してレース内 softmax（合計1）を当てるのは、合計3になるべき確率を1に押し込めることになる。圧縮の一因はこれかもしれない。

## keiba-ai での使い方

- lambdarank の出力を確率に変換するときは、softmax の温度を検証期間で推定し、3着内確率には Harville などの順位モデルを使う。ランカーと分類器の比較は、変換を揃えてから行う。
- 拡張窓のターゲットエンコーディング（馬・騎手・調教師）は、時点整合の実装例として使える。
- 公式レーティングのような「その時点の値」が取れない項目の扱いを、データ取得の時点で決めておく。

## 関連ノート

- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): LambdaRank / LambdaMART。
- [Guo 2017](./2017-guo-calibration-modern-nn.md): 温度スケーリング。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 単勝確率から3着内確率。
- [Chung 2024](./2024-chung-learning-to-rank-seoul.md)、[So 2025](./2025-so-learning-to-rank-kra-web-service.md): 韓国競馬の learning-to-rank。
- [jerrydaphantom 2026](./2026-jerrydaphantom-hkjc-ml-research.md): 同じ HKJC で市場ありなしを比較した研究。

## 検索語

香港競馬, 3着内予測, ランキング学習, ランカーの較正, ソフトマックス, ターゲットエンコーディング, 時系列分割, Hong Kong Jockey Club, top-3 prediction, LGBMRanker, XGBRanker, lambdarank calibration, softmax compression, expanding target encoding, SHAP, official rating

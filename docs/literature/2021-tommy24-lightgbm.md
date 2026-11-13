---
title: 機械学習における競馬予測 〜LightGBM編〜
authors: tommy24
year: 2021
venue: Qiita
url: https://qiita.com/tommy24/items/acf5dc4152b4a534c058
topic: practitioner
tags: grey-literature, netkeiba-scraping, lightgbm, binary-classification, top3, random-split-leak, final-odds-leak, auc, optuna, beginner
verified: fulltext
importance: low
source: downloaded
source_version: web
---

# ランダム分割・確定オッズ込みで3着内 AUC 0.817 という初学者の記録

> 一言で: netkeiba からスクレイピングした約50万行×20列のデータで、3着以内か否かを LightGBM で二値分類し、AUC 0.816736 を得た初学者の記事。回収率は計算していない。分割はランダム（`train_test_split`, test_size=0.33）で、確定オッズと人気を特徴量に入れている。この AUC は購入時点で使えるモデルの性能ではなく、リークを含む数字の参照例として残す。

## データ

- netkeiba.com のスクレイピング（手順は別の Qiita 記事を参照）。約50万行×20列（「2 前処理」の節）。期間は書かれていない。
- 列: 年齢、前走からの体重差、コース、日付、馬場、性別、頭数、馬名、斤量、騎手、オッズ、人気、レース、レース名、着順、調教師（2列）、馬体重、年。
- 中止・失格の行（約2,000）は削除。オッズ・人気・レース名の欠損行も削除。

## 特徴量

- 上記の列をそのまま。カテゴリ列（馬名、騎手、調教師、レース名、コースなど）はラベルエンコーディング。
- 追加特徴量は2つ: オッズ×人気（`odds_popu`）と前走の馬体重（馬体重−体重差）（「2-4」の節）。
- 過去走の集計（前走着順、平均着順など）はない。当日のレースの情報だけで学習している。

## モデルと目的変数

- 目的変数: 3着以内なら1（「2-5」の節）。
- LightGBM の二値分類。ハイパーパラメータは Optuna の LightGBM 統合（`optuna.integration.lightgbm`）で決め、`num_boost_round=100`、early stopping 10 で再学習。

## 評価

- **ランダム分割**: `train_test_split(test_size=0.33, random_state=0)`。同じレースの馬が学習とテストに分かれ、同じ日・同じ馬の情報が両側に入る。
- テストデータを Optuna の検証と early stopping の両方に使っている。
- 指標は AUC のみ。回収率は「そこまでの技術はない」として計算していない（「行ったこと」の節）。

## 結果

- AUC 0.816736（「おわりに」の節）。
- 特徴量重要度ではオッズが最も高く、騎手も高い。人気と調教師A の重要度は低く、調教師B は高い（「3 学習、予測」の節）。

## 批判的に読む

- **確定オッズ**: 特徴量のオッズは結果ページの確定単勝オッズ。3着内の判別では、オッズだけでかなりの AUC が出る。この記事の AUC の大半はオッズ由来と考えられ、購入時点で同じ精度は出ない。
- **ランダム分割**: レース単位でも時系列でもない分割。馬名をラベルエンコードして入れているので、同じ馬の別のレースが学習側にあれば、その馬の強さを覚えられる。
- **テストデータでのチューニング**: Optuna と early stopping にテストデータを使っているので、AUC はやや楽観的。
- 人気の重要度が低いのは、オッズ×人気とオッズがほぼ同じ情報を持つため（LightGBM の分割回数ベースの重要度は相関した特徴量の間で分散する）。
- 著者は「当たるけど、戻ってくるお金は少ない」と回収率の問題を認識しているが、検証していない。

## keiba-ai での使い方

- 3着内二値分類の AUC 0.82 前後は、確定オッズを入れたモデルなら初学者の設定でも出る、という目安として使う。自分のモデルの AUC を比べるときは、オッズを入れたか、分割は時系列か、を揃える。
- 市場（単勝オッズの逆数だけ）の AUC をベースラインとして必ず並べる。オッズ込みのモデルがそれをどれだけ上回るかで評価する。
- 分割はレース日付による時系列分割。ハイパーパラメータ探索・early stopping には、テストと別の検証期間を使う。

## 関連ノート

- [gara-gara 2020](./2020-gara-gara-lightgbm-leak.md): LightGBM の競馬モデルでリークに気づいた記録。
- [kazuktym 2020](./2020-kazuktym-beginner-keiba-model.md): 初学者による別の競馬モデル。
- [mshimia 2020](./2020-mshimia-recovery-over-100.md): この記事が参考にした Qiita 記事。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): 予測時点で使える変数の棚卸しと時系列評価。この記事の確定オッズとランダム分割の問題を体系的に扱う。
- [Cerqueira 2020](./2020-cerqueira-time-series-performance-estimation.md): 時系列データでのランダム分割の問題。
- [Ke 2017](./2017-ke-lightgbm.md): LightGBM。

## 検索語

LightGBM 競馬、3着以内 二値分類、AUC 0.81、netkeiba スクレイピング、ランダム分割、train_test_split リーク、確定オッズ 特徴量、Optuna LightGBM、ラベルエンコーディング 馬名、特徴量重要度 オッズ、初心者 競馬予測

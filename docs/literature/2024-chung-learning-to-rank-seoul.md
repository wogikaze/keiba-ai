---
title: Horse race rank prediction using learning-to-rank approaches
authors: Chung Junhyoung, Shin Donguk, Hwang Seyong, Park Gunwoong
year: 2024
venue: The Korean Journal of Applied Statistics 37(2) 239-253
url: https://koreascience.kr/article/JAKO202414143309228.page
doi: 10.5351/KJAS.2024.37.2.239
topic: machine-learning
tags: learning-to-rank, pointwise, pairwise, korea, seoul, kra, catboost, lambdamart, shap
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# ソウル競馬の着順予測: point-wise 回帰より LambdaMART、特に CatBoost Ranker が良い

> 一言で: 韓国馬事会（KRA）の公開データでソウルの 2013年1月〜2023年7月・7,894レースを使い、線形回帰・RF（point-wise）と RankNet・XGBoost/LightGBM/CatBoost の LambdaMART（pair-wise）を比べた。全指標で CatBoost Ranker が最良で、単勝的中率は 30.5%（RF は 26.0%）。ただし分割は時系列ではなく、通算成績の変数の時点も明記されておらず、市場との比較も無い。

本文は韓国語（要旨・表は英語）。ページは PDF のページ番号（library の `=== page N ===`）で書く。雑誌の印刷ページは PDF ページ + 238。

## データ

| 項目 | 内容 | 出典 |
|---|---|---|
| 取得元 | 韓国馬事会（www.kra.co.kr）の公開データ10種 | p.6, Table 1 |
| 内容 | 競走成績・馬場・天候、騎手の通算成績、馬の通算成績・詳細情報・診療記録・発走調教、調教師の通算成績・詳細情報 | p.4, p.6 |
| 期間 | 2013年1月〜2023年7月（ソウル） | p.6 |
| 規模 | 82,681頭・回、7,894レース | p.6 |
| 除外 | 欠測・失格などの異常な記録、前走記録の無い新馬 | p.6 |
| 説明変数 | 33個（カテゴリ5、数値28） | p.6, Table 2 |

距離別のレース数は 1,200m が 2,040 と最多、2,300m は 12 しかない（p.6, Table 3）。先行研究の Choe ら（2015）は距離ごとに別のモデルを作ったが、それではデータの少ない距離で学習できない。そこで本研究は、走破タイムを**距離ごとに標準化**し、1つのモデルで全距離を扱う（p.7）。

$$y_{qj} = \frac{\tilde y_{qj} - \bar{\tilde y}_d}{s_d}$$

ここで $\tilde y_{qj}$ はレース $q$ の馬 $j$ の走破タイム、$\bar{\tilde y}_d,\ s_d$ は距離 $d$ の全レースでの平均と標準偏差。目的変数はこの標準化タイムである（p.8）。

主な特徴量（p.5, Table 2）:

- 前走の標準化タイム（`str_rcTimeLag1`）
- 馬・騎手・調教師の「成績」: 通算の1〜5着回数に 5,4,3,2,1 の重みを付けた和を、15 × 出走数で割ったもの。$\text{performance} = \sum_{n=1}^{5}(6-n)\,\text{ord}_n / (15 \times \text{rcCnt})$
- 発走調教の回数（通算と、前走からの回数）
- 診療（疾病診断）回数
- 斤量、馬体重とその増減、馬番、頭数、年齢、性、産地、クラス、天候、馬場、含水率

発走調教・診療記録・前走の標準化タイムは、先行研究で使われていなかった変数だと著者は言う（p.7, p.11）。

## モデル

| 系統 | モデル | 実装 |
|---|---|---|
| point-wise | 線形回帰、ランダムフォレスト（Choe ら 2015 の方法） | |
| pair-wise | RankNet | |
| pair-wise（LambdaMART） | XGBoost Ranker、LightGBM Ranker、CatBoost Ranker | Python の xgboost / lightgbm / catboost |

LambdaRank の損失は、RankNet のペア損失に「2頭の順位を入れ替えたときの NDCG の変化量」$|\Delta Z_{ij}|$ を掛けたもの（p.5–6）。

$$\hat f = \arg\min_f \sum_q \sum_{i<j} |\Delta Z_{ij}| \log\bigl(1+\exp(-\sigma (f(x_i^q) - f(x_j^q)))\bigr)$$

カテゴリ変数は、CatBoost では内蔵の処理（ordered target statistics など）、それ以外は one-hot にした（p.8）。ハイパーパラメータの調整方法は書かれていない。

## 評価方法

- レース単位でまとめて学習 6,315 レース・評価 1,579 レースに分け、この無作為分割を100回繰り返して平均した（p.8）。**時系列での分割ではない。**
- 指標（p.8–10）:
  - k-winrate: 実際の上位 k 頭が、すべて予測の上位 k 頭に入ったレースの割合。$k=1$ が単勝、$k=2$ が複勝式（馬連に相当）、$k=3$ が三複勝式（3連複に相当）
  - レースごとの Spearman 相関と Kendall の τ の平均
  - NDCG（ゲインは標準化タイムから $2^{-y}-1$）

## 結果（p.9, Table 4。括弧内は100回の標準誤差）

| 指標 | 線形回帰 | RF | RankNet | XGBoost Ranker | LightGBM Ranker | CatBoost Ranker |
|---|---|---|---|---|---|---|
| 単勝 | 0.2744 | 0.2598 | 0.2600 | 0.2733 | 0.2803 | **0.3049** (0.0107) |
| 馬連 | 0.1155 | 0.1070 | 0.1087 | 0.1142 | 0.1225 | **0.1345** |
| 3連複 | 0.0643 | 0.0579 | 0.0585 | 0.0625 | 0.0701 | **0.0771** |
| Spearman | 0.4080 | 0.3859 | 0.3844 | 0.4037 | 0.4284 | **0.4474** |
| Kendall τ | 0.3129 | 0.2951 | 0.2935 | 0.3083 | 0.2935 | **0.3439** |
| NDCG | 0.7025 | 0.7001 | 0.6901 | 0.7002 | 0.6901 | **0.7149** |

- CatBoost Ranker が全指標で最良。著者はその理由を、pair-wise であることと、カテゴリ変数の扱いの良さに求める（p.10）。
- RankNet は point-wise にも負けた。著者は、このデータの関係が NN に向かないためと解釈する（p.11）。
- 単純な線形回帰が RF より全指標で良く、XGBoost Ranker とほぼ同じ。
- LightGBM Ranker の Kendall τ と NDCG は、RankNet と小数第4位まで同じ値（0.2935、0.6901）。転記の誤りの可能性がある（推測）。

### SHAP による変数重要度（p.10–12, Figure 3–4）

- RF では前走の標準化タイムが飛び抜けて重要。含水率・距離・頭数のように、レース内で全馬共通の変数も上位10に入った。
- CatBoost Ranker では馬の「成績」が1位。年齢・診療回数・斤量・馬体重増減・馬番・通算出走数のように、レース内で馬ごとに違う変数が上位に来た。著者は、順位の予測では馬どうしの相対的な能力を表す変数が効くと解釈する（p.11）。
- 方向: 年齢と通算出走数が大きいほど低評価（老化）。馬番が大きい（外枠）ほど低評価。斤量が重いほど高評価（能力の高い馬に重い斤量が課されるためと解釈）（p.12）。
- 診療回数が多いほど高評価。著者は「管理が行き届いている指標」と読むが、省かれた要因の影響がありうるので解釈に注意するよう書いている（p.8, p.12）。

## 批判的に読む

- **通算成績の時点がわからない。** KRA の「通算記録」データは、普通は取得した時点の累計である。各レースの時点の累計に直したという記述は見当たらない。もし取得時点の値なら、馬の「成績」（1位の変数）・通算出走数・診療回数のどれにも未来の成績が入っている。診療回数が多いほど高評価という直感に反する結果も、長く活躍した馬ほど通算の診療回数が多い、と考えればこのリークで説明がつく（推測）。
- **時系列で分けていない。** レースをまとめたうえでの無作為分割なので、同じ馬の前後のレースが学習と評価に分かれる。
- **市場と比べていない。** 単勝的中率 30.5% が、ソウルの1番人気の勝率と比べてどうかは示されていない。1番人気の勝率が同程度なら、モデルは市場以上の情報を持っていない。回収率も計算していない。
- **ハイパーパラメータの調整が書かれていない。** 手法間の差が調整の差なのか、手法の差なのかを分けられない。
- **目的変数が走破タイム。** 着順ではなく、距離で標準化したタイムを学習している。馬場状態やペースによるレース全体のタイムのぶれは、レース内の順位には関係ないが、point-wise 回帰には雑音になる。pair-wise が有利になる一因と思われる（推測）。
- 良い点: 同じレースの馬を学習と評価に分けない「レース単位のグループ分割」をしている（p.8）。100回の反復で標準誤差を出している。

## keiba-ai での使い方

- **LambdaMART の実装を比べる。** keiba-ai で LightGBM の `lambdarank` を使うなら、CatBoost の `YetiRank` / `PairLogit` 系も、同じ特徴量・同じ時系列分割で比べる価値がある。カテゴリ変数（騎手・調教師・種牡馬）が多い JRA データでは、CatBoost の ordered target statistics が効く、という仮説。評価は1着の log loss（スコアを softmax で確率にしてから）と、市場確率と混ぜたときの改善で行う。
- **距離で標準化したタイムを目的変数・特徴量にする。** 前走タイムを距離ごと（さらに競馬場・芝ダート・馬場状態ごと）に標準化した「前走の標準化タイム」は、タイム指数の簡易版として使える。
- **累計特徴量は時点を切って作る。** 「通算成績」「通算出走数」「診療回数」に当たるものは、すべてレース日より前の記録だけで作る。JRA-VAN や netkeiba の現在値を使わない。
- **発走調教・診療記録に当たるデータ。** JRA には直接対応する公開データは少ないが、調教の本数（坂路・ウッドの本数）、出走間隔、放牧明けといった情報で近いものは作れる。

## 関連ノート

- [So 2025](./2025-so-learning-to-rank-kra-web-service.md): 同じ KRA データで LTR を使い、Web サービスまで作った後続の韓国の研究。
- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): RankNet・LambdaRank・LambdaMART の原典。本研究の手法の出どころ。
- [Ke 2017](./2017-ke-lightgbm.md): LightGBM の原典。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md): 競馬の予測を NDCG で評価した先行例。
- [Fujisawa 2024](./2024-fujisawa-ranknet-condition-datasets.md): RankNet を日本の競馬に使った研究。本研究では RankNet が最下位だった点と比べられる。
- [Pudaruth 2015](./2015-pudaruth-ann-champs-de-mars.md): 本研究が使う「1〜5着の重み付き成績」変数の発案者のグループ（2013年の論文）。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): リークを意識した評価。本研究の通算成績・無作為分割の問題を点検する観点。

## 検索語

順位学習, ランキング学習, learning to rank, LTR, point-wise, pair-wise, list-wise, RankNet, LambdaRank, LambdaMART, XGBoost Ranker, LightGBM Ranker, CatBoost Ranker, CatBoost, NDCG, Kendall tau, Spearman, SHAP, シャープレイ値, 韓国, ソウル, 韓国馬事会, KRA, Korea Racing Authority, 標準化タイム, 距離別標準化, 発走調教, 診療記録, 通算成績, リーク, 単勝的中率, 馬連, 3連複

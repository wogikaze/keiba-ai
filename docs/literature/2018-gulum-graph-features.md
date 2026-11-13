---
title: Horse racing prediction using graph-based features.
authors: Gulum Mehmet Akif
year: 2018
venue: Master's Thesis, University of Louisville (Electronic Theses and Dissertations, Paper 2953)
url: https://ir.library.louisville.edu/etd/2953/
doi: 10.18297/etd/2953
topic: machine-learning
tags: graph-features, neural-network, logistic-regression, equibase, pairwise, kentucky-derby
verified: abstract
importance: medium
source: unavailable
source_version:
---

# 馬どうしの対戦関係を有向グラフにして、特徴量として足す（修士論文）

> 原本未取得。全文 PDF は Louisville 大学の機関リポジトリで公開されている（OA）。ただ、ボット対策で自動取得が 403 になり、library に保存できなかった。ブラウザで手動取得すれば読める。以下はリポジトリの要旨と、他文献での引用に基づく。

> 一言で: 2015〜2017年の米国の競走データで、同じレースを走った馬どうしの先着関係から大きな有向グラフを作り、そこから取った特徴量を基本特徴量に足した。すると、ニューラルネットとロジスティック回帰の「2頭のどちらが先着するか」の正解率が上がった、という修士論文。

## 何をしたか（要旨の4段階）

要旨は、論文を次の4段階で説明している（リポジトリの要旨）。

1. 競馬サイトから 2015〜2017年のレースデータを集める。データ源は Equibase とされる（二次情報。原本で未確認）。
2. 基本特徴量だけで予測モデル（ANN とロジスティック回帰）を学習し、予測する。
3. 全馬を節点とする大域的な有向グラフを作り、グラフ特徴量を抽出する（著者が「中核」と呼ぶ部分）。
4. グラフ特徴量を足して同じモデルを学習し直し、精度が上がるかを見る。

評価は、同じレースを走った2頭を無作為に選び、どちらが先着するかを当てる形式。さらに 2016年と 2017年のケンタッキーダービーにも当てはめた。2016年は上位4頭を当て、2017年は上位3頭を当てられなかった（要旨）。

## グラフの作り方（推測を含む）

要旨には定義が無い。題名と「global directed graph of horses」から考えると、次のような構成と思われる（推測）。

- 節点: 馬
- 辺: 同じレースで馬 A が馬 B に先着したら、B→A（または A→B）の有向辺。複数回対戦すれば重みを足す。
- 特徴量: 節点の入次数・出次数（何頭に勝ち、何頭に負けたか）、勝敗差、PageRank のような伝播型の強さのスコア

こうした特徴量の強みは推移性を使える点にある。「A は B に勝ち、B は C に勝った」なら、A と C が一度も対戦していなくても比べられる。Elo や Bradley–Terry の強さパラメータと似た役割を、グラフ上の計算で得ていることになる。

## 報告された数値（二次情報）

ペンシルベニア大学の学部卒論（Won）の引用では、2頭比較の正解率が「オッズ基準 66%、ML 77%、グラフ特徴量込み 93%」とされる。本論文の原本では確認していない。

## 批判的に読む

- **グラフをどの期間で作ったか。** 要旨は「大域的な」グラフと言う。2015〜2017年の全レースで1つのグラフを作り、その特徴量を同じ期間の2頭比較に使ったのなら、テスト対象のレースの勝敗そのものが辺としてグラフに入っている。正解率 93% という高さは、このリークでよく説明できる。グラフを「予測するレースより前の結果だけ」で作り直したかどうかが、この論文を評価する決め手になる（未確認）。
- **2頭比較は易しい課題。** 無作為に選んだ2頭には、能力差が大きい組が多く含まれる。オッズ基準で 66% という数字もそれを反映している。勝率の推定や回収率とは別物である。
- **ダービー2回は事例にすぎない。** 2回の結果では何も言えない。
- **回収率の評価は無い（と思われる）。**

## keiba-ai での使い方

- **対戦グラフの特徴量は試す価値がある。** JRA では、クラスや条件の違いで直接対戦していない馬どうしを比べる場面が多い。「同じレースで先着した相手の強さ」を伝播させるスコア（PageRank、Elo、Bradley–Terry の強さ）を特徴量に入れると、初対戦の組み合わせの比較に効く、という仮説。
- **必ず時点を切って作る。** 特徴量はレース日 $t$ より前の結果だけで作ったグラフから計算する。実装は、日付順に辺を足しながら各時点のスコアを記録する形にする。全期間のグラフから一度に計算すると、本論文で疑われるのと同じリークが起きる。
- **評価。** 2頭比較の正解率ではなく、レース内の勝率の log loss と、市場確率と混ぜたときの改善で評価する。

## 関連ノート

- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 対戦結果から強さを推定する Bradley–Terry の MM アルゴリズム。グラフ特徴量の統計モデル版。
- [Cotton 2021](./2021-cotton-relative-ability-winning-probability.md): 相対的な能力から勝率を出す考え方。
- [Guiver 2009](./2009-guiver-bayesian-plackett-luce.md): 順位データから強さを推定するベイズ Plackett–Luce。
- [Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md): 能力を階層ベイズで推定し、同じく初対戦の比較を可能にする。
- [Davoodi 2010](./2010-davoodi-ann-horse-racing.md): 同じく ANN で競馬を予測した先行研究。

## 検索語

グラフ特徴量, 対戦グラフ, 有向グラフ, 直接対決, head-to-head, graph-based features, directed graph, PageRank, ネットワーク分析, network features, ペアワイズ比較, pairwise comparison, 先着予測, Bradley-Terry, Elo, ニューラルネット, ANN, ロジスティック回帰, logistic regression, Equibase, ケンタッキーダービー, Kentucky Derby, 推移性, transitivity, リーク

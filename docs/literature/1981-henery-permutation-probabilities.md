---
title: Permutation Probabilities as Models for Horse Races
authors: Henery R. J.
year: 1981
venue: Journal of the Royal Statistical Society Series B (Methodological) 43(1) 86-91
url: https://academic.oup.com/jrsssb/article/43/1/86/7028103
doi: 10.1111/j.2517-6161.1981.tb01153.x
topic: probability-models
tags: henery-model, thurstone, normal-order-statistics, ordering-probability
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 着順の確率を「正規分布の順序統計量」で作る Henery モデルの原典

> 一言で: 着順確率モデルが満たすべき性質として「順列の確率的順序（stochastic ordering）」を定義し、走破時間を独立な確率変数とみる順序統計量モデルがそれを満たす条件（単調密度比）を示した。そのうえで、正規分布版（後に「Henery モデル」と呼ばれる）の着順確率を、勝率だけから計算できる1次近似を与えた。実際の競馬データでの検証はこの論文には無い。

## 位置づけ

Plackett (1975) が提示した解（Harville 公式と同じ $p_i\cdot p_j/(1-p_i)\cdot p_k/(1-p_i-p_j)$）には、確率が頭数に依存しないという「おそらく非現実的な」性質がある、と著者は指摘する (p.86)。一方 Upton & Brook (1974) の正規モデル（選挙の投票順位の分析に使われた）は頭数に依存するが、多変量正規積分が必要で扱いにくい。本論文は両者を順序統計量モデルの特殊例として統一的に論じ、正規モデルを実用化する近似を提案する。

6ページの短い理論論文で、データ分析は投票の数値例1つだけ。既存ノートの旧版にあった「香港データで Harville より良い」は後続研究（Lo & Bacon-Shone 1994 など）の結果であり、本論文の主張ではない。

## 確率的順序（第2節）

勝率の順に $R_1, R_2, \dots, R_n$（$p_1>p_2>\dots>p_n$）と並べたとき、自然に期待される性質を次のように定式化する (p.86–87)。

- 2頭の位置だけを入れ替えた2つの着順 D, E のうち、2頭が勝率の順に並ぶ方 D の確率が高い（D > E）。
- これを推移的に広げた半順序を「確率的順序」と呼ぶ。3頭なら 123 が最も起こりやすく 321 が最も起こりにくい。132 と 213 のように転倒数が同じ順列は比べられない (p.87, Fig.1)。

この順序から導かれる帰結 (p.88):

1. $p_j(1)$（馬 $j$ が1着の確率）は $j$ について減少
2. $p_j(n)$（最下位の確率）は $j$ について増加。「最も勝ちそうな馬が最も最下位になりにくい」
3. $p_1(k)$ は $k$ について減少
4. $p_n(k)$ は $k$ について増加

ただし (1)〜(4) が成り立っても確率的順序が成り立つとは限らない（$n>2$）。

## 順序統計量モデル（第3節）

走破時間 $X_1,\dots,X_n$ を独立な連続確率変数（分布 $F(x;\theta_i)$）とし、$X_1<X_2<\dots<X_n$ の確率を着順 $\lbrace 1,2,\dots,n\rbrace $ の確率とする (p.88)。独立性から「一部の馬どうしの相対順位は残りの馬の相対順位と独立」という性質が自動的に従う。

**主結果**: 密度の比 $f(x;\theta_r)/f(x;\theta_s)$ が $x$ について単調（単調尤度比に類似）なら、順列は確率的順序を満たす (p.88–89)。満たす分布族の例:

| 分布 | 対応するモデル |
|---|---|
| 正規 $N(\theta,\sigma^2)$、$\sigma$ 固定 | Upton & Brook / Henery の正規モデル |
| 指数（平均 $\theta$） | Plackett (1975)、$p_i=1/\theta_i$ とすれば Harville 公式 |
| ガンマ（形状固定） | 後の Stern (1990) のガンマ順位モデル |

このうち $\theta$ の変化が単純な平行移動になるのは正規だけ (p.89)。平行移動型（位置族）なら単峰でなくても性質 (1)(2) は成り立つが、二峰の例では確率的順序が崩れることを反例で示す (p.89)。

著者は、非ハンデ戦なら馬を能力で格付けできるとしつつ、要因は多く「これらのモデルは当面は定性的に受け取るべき」と控えめに述べる (p.89)。

## 正規モデルの近似（第4節）

$X_i\sim N(\theta_i,1)$ のとき、着順確率を $\theta=0$ の周りで1次の Taylor 展開する (p.90)。$\mu_{i;n}$ を標準正規 $n$ 標本の第 $i$ 順序統計量の期待値とすると、

- 着順 $\pi$ の確率: $P\lbrace \pi\rbrace \approx 1/n! + \sum_i\theta_i\mu_{i;n}/n!$
- 馬 $j$ が $k$ 着の確率: $P\approx 1/n + \theta_j\mu_{k;n}/(n-1)$

実用的な手順として、勝率 $\pi_j$ を与えて平均を逆算する (p.91):

1. $z_j=\Phi^{-1}(\pi_j)$、$z_0=\Phi^{-1}(1/n)$
2. $\theta_j\approx(n-1)\phi(z_0)(z_j-z_0)/\mu_{1;n}$
3. 馬 $j$ が $k$ 着の確率 $\approx\Phi\lbrace z_0+(z_j-z_0)\mu_{k;n}/\mu_{1;n}\rbrace $
4. $\mu_{i;n}$ は Blom の近似 $\Phi^{-1}((i-3/8)/(n+1/4))$ で計算できる

この $\theta_j$ の式は、Ali (1998) が数値解法の初期値として使っている（[Ali 1998](./1998-ali-probability-models-outcomes.md) の式6）。

**数値例** (p.91): Brook & Upton の3候補（勝率 0.3771, 0.3631, 0.2598）で、近似の平均は −0.1034, −0.0704, +0.1738。123 と 321 の確率は近似で 0.2058 と 0.1276、厳密値は 0.2096 と 0.1283。Plackett（Harville）モデルは一般に Pr{123} を過大、Pr{321} を過小に見積もると付記している (p.91)。

> Plackett's model gives reasonable approximations to Pr{123} and Pr{321} in this and other cases, but the former probability is generally overestimated while the latter is underestimated. (p.91)

## 批判的に読む

- **実データの検証がない**: 主張は性質の整理と近似式の提案まで。競馬で Harville より良いかは、後の Lo & Bacon-Shone (1994)、Ali (1998) の実証に頼る必要がある。
- **近似の精度**: 1次展開なので $\theta$ が小さい（勝率が $1/n$ に近い）ときに良い。本命が抜けたレースでは誤差が大きくなりうる。著者も $\theta$ が1に近いときは正規分布を使う複雑な方の近似を勧める (p.91)。どの程度まで使えるかの系統的評価はない。
- **分散を1に固定**: 全馬で走破時間のばらつきが同じという仮定。馬ごとに不確実性が違う（新馬、休み明け）場合は扱えない。
- 原文 PDF はスキャンからのテキスト化で、数式の一部（$\mu_{i;n}$ の添字など）は読み取りが崩れている。式は文脈から復元した。

## keiba-ai での使い方

- **馬単・3連単の確率を単勝確率から作る代替公式**: Harville は人気馬の上位独占を過大に見る（本論文の数値例でも 123 を過大評価）。Henery 近似は $\Phi^{-1}$ と Blom の近似だけで計算でき、数値積分なしに「馬 $j$ が $k$ 着」の確率を出せる。複勝・ワイドの確率推定に直接使える。
- **実験案（仮説）**: 単勝確率（市場またはモデル）を入力に、Harville と Henery 近似の両方で各馬の着順分布を作り、JRA の複勝的中（3着以内）の対数損失と較正を比べる。仮説は「頭数が多い（16〜18頭）レースほど Henery の方が良い」。Harville は頭数に依存しないという本論文の指摘が根拠。
- **シミュレーション版**: 正規モデルはモンテカルロ（各馬の $\theta_j$ に標準正規ノイズを足して並べ替え）で厳密に近い値が出せる。近似式は高速なベースライン、モンテカルロを正解として誤差を測る。
- **能力モデルとの接続**: 走破タイム（スピード指数）を直接回帰するモデルなら、その予測平均と残差分散をそのまま $\theta_j$ と分散に使うのが自然で、Henery の枠組みと一致する。

## 関連ノート

- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 本論文が批判的に参照する1次モデル（指数分布に対応）。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): Plackett の解と同じ公式を競馬に適用した先行研究。
- [Stern 1990](./1990-stern-gamma-permutations.md): ガンマ分布版。指数と正規の間をつなぐ。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Henery と Harville を実データで比較し Henery が優位。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 正規順位モデルが最良だが2・3着の偏りは残ると報告。本論文の近似式を初期値に使用。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): Henery/Stern を簡単に近似する割引 Harville 型の公式。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 指数（Plackett-Luce）側の推定アルゴリズム。

## 検索語

Henery モデル, Henery model, 正規順位モデル, normal ranking model, 正規順序統計量, normal order statistics, Thurstone-Mosteller, Upton-Brook, 順列確率, permutation probability, 着順確率, ordering probability, 確率的順序, stochastic ordering, 単調尤度比, monotone likelihood ratio, Plackett モデル, Harville 公式, 2着確率, 3着確率, place probability, Blom 近似, Taylor 展開, 走破時間の分布, running time distribution

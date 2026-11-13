---
title: Models for Distributions on Permutations
authors: Stern Hal S.
year: 1990
venue: Journal of the American Statistical Association 85(410) 558-564
url: https://www.tandfonline.com/doi/abs/10.1080/01621459.1990.10476235
doi: 10.1080/01621459.1990.10476235
topic: probability-models
tags: gamma-model, ordering-probability, permutation, harville-formula
verified: abstract
importance: medium
source: unavailable
---

# ガンマ分布の走破時間で着順確率を作る Stern モデル

> **原本未取得。** JASA の有料論文で、合法な無料版が見つからなかった。本ノートは要旨と、本論文を引用する後続論文（Ali 1998、Glickman & Hennessy 2015、Henery 1981。いずれも library に原本あり）に基づく。

> 一言で: $k$ 頭の着順の確率を、形状 $r$ が共通で尺度が馬ごとに違う独立なガンマ確率変数の大小順の確率として定義した。$r=1$ が Harville（Luce-Plackett）、$r\to\infty$ で正規（Thurstone）に近づく族で、勝率しか分からない競馬の着順推定に当てはめると $r>1$ の方が良かった。

## モデル

- 動機: $k$ 人が独立な Poisson 過程で得点し、$r$ 点に早く達した順に順位が決まる競争。到達時間は形状 $r$、尺度（強さ）$a_i$ のガンマ分布に従う（要旨）。
- 定義: 着順 $\pi$ の確率 $=\Pr(X_{\pi_1}<X_{\pi_2}<\dots<X_{\pi_k})$、$X_i\sim\text{Gamma}(r,a_i)$ 独立。
- 密度は $f(x;a_i,r)=a_i^r x^{r-1}e^{-a_i x}/\Gamma(r)$（[Ali 1998](./1998-ali-probability-models-outcomes.md), p.223 の記法）。
- 特殊例: $r=1$ で指数分布＝Luce-Plackett＝Harville。$r$ を大きくすると Thurstone-Mosteller-Daniels（正規）型に近づく。Glickman & Hennessy (2015) も、正規と極値分布の順位モデルはガンマモデルの特殊例（極限）であり、一般のパラメータでは順列確率の数値計算が難しいと書く（[Glickman & Hennessy 2015](./2015-glickman-stochastic-rank-ordered-logit.md), PDF p.3）。
- ガンマ分布が単調密度比を持つことから、Henery (1981) の意味での「確率的順序」を満たす（[Henery 1981](./1981-henery-permutation-probabilities.md), p.89）。

## 推定（勝率だけが分かる場合）

1レースで観測できる着順は1つしかなく、レースごとにパラメータが違う。そこで市場の単勝オッズから勝率 $p_n(i)$ を推定し、モデルの単勝確率をそれに一致させる。Stern はこれが最尤方程式 $p(i)=p_n(i)$ になることを示した（Ali p.223–224 による）。そのうえで $r$ を固定して $a_i$ を解き、2・3着の確率を数値積分で計算する。

## 結果（要旨と孫引き）

- 要旨: 競馬に当てはめると、形状が1より大きいモデルが、最もよく使われる $r=1$ より良い。
- Ali (1998) によれば、Stern は 47 レースで $r=1, 2$ を分析し、Harville の偏り（人気馬の2・3着の過大評価）を裏づけた (Ali p.222, p.226)。
- 要旨によれば、分布の計算が難しいため例は小さい $k$ に限られ、広く使うには近似が必要だと著者自身が認めている。
- 具体的な尤度の値、データの競馬場は**未確認**。

## 大規模データでの追試

Ali (1998) は NY ハーネス 15,402 レースで $r=0.5$〜$20$ を比べた。1番人気の2着確率（実際 0.192）に対し、$r=1$: 0.256、$r=2$: 0.242、$r=5$: 0.230、$r=20$: 0.220 と、$r$ が大きいほど偏りは小さくなるが消えず、正規モデル（0.210）が最良だった (Ali p.227, Table 2)。

## 批判的に読む

- **計算コスト**: 着順確率ごとに多重積分が必要。18頭立ての3連単（4,896通り）を全部計算するのは重い。モンテカルロなら簡単だが、精度とのトレードオフがある。
- **標本の小ささ**: 原論文の競馬データは 47 レース（孫引き）で、$r$ の推定精度は低いはず。
- **$r$ の解釈**: $r$ が大きいほど、走破時間の変動係数が小さい（＝能力どおりに決まる）競争になる。競馬場・距離・頭数で $r$ が違う可能性があり、単一の $r$ を全レースに使うのは粗い。Lo (1994) は日本のデータで $r$ を推定している（[Lo 1994](./1994-lo-running-time-japan.md) を参照）。

## keiba-ai での使い方

- **1パラメータで Harville からのずれを測る**: JRA データで $r$ を最尤推定する（単勝確率を固定し、2・3着の実際の結果で $r$ の尤度を計算）。芝/ダート、距離、頭数で層別して $r$ が変わるかを見る。
- **仮説**: 「ダート短距離は $r$ が大きい（能力どおり）、芝長距離やハンデ戦は $r$ が小さい（荒れやすい）」。
- **実装**: ガンマ分布の着順確率はモンテカルロで計算し、Lo & Bacon-Shone の割引 Harville 近似と比べて、近似で十分かを確かめる。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): $r=1$ の特殊例。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規版と、順序統計量モデルの一般的性質。
- [Plackett 1975](./1975-plackett-analysis-of-permutations.md), [Luce 1959](./1959-luce-individual-choice-behavior.md): $r=1$ の理論的出典。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 15,000 レースで $r$ を変えて比較。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較。
- [Lo 1994](./1994-lo-running-time-japan.md): 日本のデータへの走破時間分布モデルの適用。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 順位確率モデルの賭けへの応用。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): Henery/Stern の簡単な近似。
- [Glickman & Hennessy 2015](./2015-glickman-stochastic-rank-ordered-logit.md): ガンマモデルを一般形として位置づける。

## 検索語

Stern モデル, ガンマ順位モデル, gamma ranking model, ガンマ分布, gamma distribution, 形状パラメータ, shape parameter, 順列の分布, distribution on permutations, 着順確率, ordering probability, Poisson 過程, Thurstone, Luce-Plackett, Harville, 走破時間分布, running time distribution, 2着確率, 3着確率

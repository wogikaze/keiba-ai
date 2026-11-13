---
title: New order-statistics-based ranking models and faster computation of outcome probabilities
authors: Baker Rose D.
year: 2020
venue: IMA Journal of Management Mathematics 31(1) 33-48
url: https://academic.oup.com/imaman/article-abstract/31/1/33/5308454
doi: 10.1093/imaman/dpz001
topic: probability-models
tags: order-statistics, ranking-model, gamma-model, thurstone, plackett-luce, computation, numerical-integration, pareto
verified: abstract
importance: medium
source: unavailable
source_version: accepted-manuscript
---

# 順序統計量に基づく新しい順位モデル（指数化指数分布・Pareto）と着順確率の高速計算

**原本未取得。** OUP 版は購読制。著者最終稿は Salford 大学のリポジトリ（eprint 49762）にあるが、Cloudflare のボット検査で取得できなかった。arXiv 版はなく、ResearchGate にも全文はない。本ノートは要旨・キーワード・書誌情報（OpenAlex、検索結果）に基づく。数値・式の詳細は未確認。

> 一言で: 「各競技者のパフォーマンスがある分布に従い、その順序統計量で着順が決まる」という Thurstone 型の順位モデルに、指数化指数分布と Pareto 分布に基づく2つの新しいモデル族を加え、多人数の着順確率を速く正確に数値計算する方法を示した（要旨より）。2019年2月にオンライン公開、2020年の巻号に収録。

## 位置づけ

着順の確率モデルは大きく2系統ある。

| 系統 | 例 | 着順確率の計算 |
|---|---|---|
| 逐次選択（Luce 型） | Plackett–Luce、Harville | 閉じた式（積） |
| 順序統計量（Thurstone 型） | Henery（正規）、Stern（gamma）、Thurstone–Mosteller V 型 | 1次元・多次元の数値積分 |

Plackett–Luce はパフォーマンスが Gumbel（極値）分布のときの順序統計量モデルと一致する（Yellott の結果、[Guiver 2009](./2009-guiver-bayesian-plackett-luce.md) 参照）。それ以外の分布では、$n$ 人の着順確率は $n-1$ 重の積分になり、多人数では計算が重い。要旨によれば、Henery の gamma モデルや Thurstone–Mosteller V 型のような順序統計量モデルは、競技者の強さの推定に有用だが、計算が遅いことが実用の障害になっており、高速化が強く求められている。

## 本論文の貢献（要旨・キーワードから分かる範囲）

1. **新しい分布族**: 指数化指数分布（exponentiated exponential、Gupta–Kundu 型。$F(x)=(1-e^{-\lambda x})^\alpha$）と Pareto 分布から、2つの順位モデル族を導く。形状パラメータで分布の裾や歪みを変えられるので、Luce 型より柔軟なモデルになると考えられる（推測）。
2. **高速計算**: 順序統計量モデルの着順確率を精度を保って速く計算する数値積分法を与える（キーワード: numerical integration）。
3. **実証**: 検索結果によれば、Baker and McHale (2015) のゴルフデータと Baker and McHale (2017) の女子テニスデータで複数のモデルを比較している。競馬データへの適用があるかは未確認。

どのモデルが当てはまりで勝ったか、計算速度がどれだけ改善したかは未確認。

## 批判的に読む（原本未取得のため限定的）

- 新しい分布族が Plackett–Luce より予測で優れるかは、データ（ゴルフ・テニス）と評価指標しだい。競馬の着順に当てはまるかは自分で確かめる必要がある。
- 数値積分の高速化は、頭数が多い競馬（JRA は最大18頭）でこそ効くが、3連単の全組み合わせ（18頭で 4,896 通り）を毎レース計算する速度が実用的かは未確認。

## keiba-ai での使い方

- **走破時間モデルの候補を広げる**: 着順確率を Plackett–Luce（Gumbel）以外の分布で作る選択肢として、Henery（正規）・Stern（gamma）に加えて本論文の族を検討できる。仮説: 下位着順ほどランダムになる競馬の性質（[Benter 2019](./2019-benter-model.md) の $\gamma,\delta<1$）は、裾の重い分布を使う順序統計量モデルの方が自然に表せる。
- **実装の優先度**: まずは閉じた式の Plackett–Luce と discount 補正で十分かを確かめ、残差（3着の校正のずれなど）が大きい場合にだけ数値積分系モデルを試す。比較指標は3連単の的中組の負の対数尤度と計算時間。
- 原本が取れたら、計算法の手順と比較表を追記する。

## 関連ノート

- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規分布の順序統計量モデル。
- [Stern 1990](./1990-stern-gamma-permutations.md): gamma 分布の順序統計量モデル。本論文が高速化の対象に挙げる。
- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): Gumbel に対応する Luce 型モデル。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 勝率だけから作る Luce 型の着順確率。
- [Lo 2008](./2008-lo-ordering-probabilities-approximation.md): Henery・Stern を閉じた式で近似する別の道。
- [Glickman 2015](./2015-glickman-stochastic-rank-ordered-logit.md): 順位ロジットの動的拡張。
- [Guiver 2009](./2009-guiver-bayesian-plackett-luce.md): Gumbel と P-L の対応（Yellott）。

## 検索語

順序統計量, 順位モデル, 着順確率, Thurstone モデル, Thurstone–Mosteller, Henery モデル, gamma モデル, 指数化指数分布, 一般化指数分布, Pareto 分布, 数値積分, 高速計算, Plackett-Luce, ゴルフ, テニス, order statistics, ranking model, outcome probabilities, exponentiated exponential distribution, generalized exponential, Pareto distribution, numerical integration, Thurstone-Mosteller type V, Henery gamma model, Baker McHale

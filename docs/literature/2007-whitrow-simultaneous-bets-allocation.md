---
title: Algorithms for optimal allocation of bets on many simultaneous events
authors: Whitrow Chris
year: 2007
venue: Journal of the Royal Statistical Society: Series C (Applied Statistics) 56(5) 607-623
url: https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9876.2007.00594.x
doi: 10.1111/j.1467-9876.2007.00594.x
topic: betting-strategy
tags: kelly, simultaneous-bets, portfolio, stochastic-gradient, simplex, football
verified: abstract
importance: medium
source: unavailable
source_version:
---

# 多数の同時事象への賭けの配分：同時 Kelly を確率的勾配法で解く

> 原本未取得。Wiley は購読制で、OpenAlex・Semantic Scholar に OA 版が無く（status CLOSED）、著者の Academia.edu はログインが必要だった。本ノートは要旨と、原本取得済みの二次資料（Uhrín ほか 2021）、Flowerdew の博士論文（Lancaster 大学リポジトリで公開）に基づく。数値結果は未確認。

> 一言で: 同じ時刻に結果が出る多数の事象（たとえば土曜15時キックオフの多数のサッカーの試合）に同時に賭けるとき、対数効用を最大化する賭け金の組を、確率的勾配に基づくアルゴリズムで数値的に求めた。シンプレックス法と比べ、解は Kelly の賭けを多数の同時の賭けへ一般化したものとみなせる。

## なぜ難しいか

同時に $n$ 個の独立な事象に賭けると、資産の結果は全事象の結果の組み合わせで決まる。各試合に3通りの結果があれば組み合わせは $3^n$ 通りで、期待対数効用 $E\log(\cdot)$ を正確に計算するだけで指数的な手間がかかる。逐次の賭けなら1事象ずつ Kelly を計算すればよいが、同時だとそれができない。Flowerdew (2015) は、英国サッカーの土曜15時に多数の試合のオッズが並ぶ状況を例に、核となる Kelly 研究が扱っていなかった問題として紹介している（同博士論文 第3章）。

## 要旨から分かること

- 主に対数効用で、多数の同時の賭けを最適化する問題を考える。
- 確率的勾配に基づくアルゴリズムを開発し、シンプレックス法と比較する。
- 解は「Kelly staking」を多数の同時の賭けへ一般化したものとみなせる。
- スポーツブックメーカーの実際のオッズを使った2つの例で調べる。
- アルゴリズムは、妥当な効用関数を持つ一般のポートフォリオ最適化にも広げられる。

## 二次資料での扱い

- Flowerdew (2015) は、Whitrow が初めてこの問題に取り組み、高速な確率近似の手法で同時の事象への賭けの割合を数値的に求めた、と書く（第3章）。続けて、このような戦略が最適な成長率にほぼ到達するのは、事象のすべての部分集合への賭け（アキュムレーター、連勝式に相当）が許される場合に限る（Edelman 2000）と述べ、Grant ほか (2008) がアキュムレーターを許すと成長率が上がり、解析的な結果も得られることを示した、と紹介している。
- Uhrín ほか (2021) は、同時に行われる複数の試合への賭けに関する一連の研究（Whitrow 2007、Grant ほか 2008、Buchen and Grant 2012）が、多数の賭けをまとめる際の近似を提案したと位置づける (p.7)。
- 検索で見つかった要約（Academia.edu の抜粋、および二次的なリポジトリ）には、最適化された賭け金が単独の Kelly の賭け金に非常に近いという記述がある。本文での位置と条件は未確認。

## 批判的に読む

- 原本未読のため、アルゴリズムの具体形（学習率、サンプリングの方法、制約の扱い）や計算時間の比較は未確認。
- 「単独 Kelly にほぼ等しい」が成り立つのは、各事象の優位が小さく独立な場合だと考えられる。Thorp の2事象の式（$f_1^*=m_1(1-m_2^2)/(1-m_1^2m_2^2)$）でも、優位 $m$ が数%なら縮小はごくわずかである。優位が大きい、または相関がある場合は外れる（推測）。
- 確率的勾配法は大規模化しやすい一方、ロバスト最適化の立場からは計算が重く、非常に多数の事象には適用しにくいという批判もある（検索で見つかった二次資料の記述。本ノートでは原本未確認）。

## keiba-ai での使い方

- **同時刻のレース**: JRA では同じ時間帯に複数場のレースが締め切られる。互いに独立とみなせるので、まず「レースごとの Kelly をそのまま使う」近似を基準とし、同時最適化と比べる。仮説: 1レースあたりの賭け比率が小さい（数%以下）限り、差は無視できる。
- **同じレース内**: 同じレースの複数の馬・複数の券種は独立ではない（排反、包含）。こちらは本論文の「独立な同時事象」の枠外で、着順の同時分布から直接 $E\log$ を最大化する必要がある。組み合わせが多い（三連単など）場合は、着順をサンプリングして確率的勾配で解く本論文の発想が使える。
- **実装**: 着順の確率モデル（Plackett–Luce など）から着順をサンプリングし、各サンプルでの資産の対数の勾配を平均して賭け比率を更新する。賭け比率の非負と合計の上限を射影で守る。凸なので、既製の凸最適化ソルバーで解いた結果と照合できる。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 単独の事象での Kelly。
- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): 重なりのある賭けの集合への一般化（部分集合の定式化）。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): 2つの同時の賭けの解析解と相関の効果。
- [Uhrín ほか 2021](./2021-uhrin-optimal-sports-betting-review.md): スポーツ賭けでの Kelly 系戦略の実証比較。本論文を同時の賭けの研究として紹介。
- [Hubáček ほか 2020](./2020-hubacek-beating-market-bad-model.md): 本論文を引用するスポーツ賭けの研究。
- [Jacot, Mochkovitch 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): 排反でない賭けへの Kelly。
- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 排反な複数の結果への賭け。
- [Busseti, Ryu, Boyd 2016](./2016-busseti-risk-constrained-kelly.md): 凸最適化としての Kelly（同時の賭けを含む一般形）。

## 検索語

同時の賭け, 同時事象, 複数試合, 資金配分, ポートフォリオ, Kelly, 対数効用, 確率的勾配法, 確率近似, シンプレックス法, アキュムレーター, サッカー, simultaneous bets, many simultaneous events, bet allocation, Kelly staking, log utility, stochastic gradient, stochastic approximation, simplex method, portfolio optimization, accumulator, football betting, Whitrow

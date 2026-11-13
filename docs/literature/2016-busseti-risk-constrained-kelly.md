---
title: Risk-Constrained Kelly Gambling
authors: Busseti Enzo, Ryu Ernest K., Boyd Stephen
year: 2016
venue: Journal of Investing 25(3) 118-134
url: https://arxiv.org/abs/1603.06183
doi: 10.3905/joi.2016.25.3.118
topic: betting-strategy
tags: kelly, drawdown, convex-optimization, fractional-kelly, risk-management
verified: fulltext
importance: high
source: downloaded
source_version: preprint
---

# ドローダウン確率の上界を凸制約にした「リスク制約付き Kelly」（RCK）

> 一言で: 「資産が初期値の α 倍を一度でも下回る確率 < β」という扱いにくい制約を、$\mathbb{E}(r^\top b)^{-\lambda} \le 1$（$\lambda = \log\beta/\log\alpha$）という凸制約で置き換え、Kelly 問題を CVXPY で解ける形にした。有限結果のシミュレーションでは、同じドローダウン確率で fractional Kelly より成長率が高い。

原本は arXiv v1（2016年3月）。掲載誌版（Journal of Investing）は未確認で、ページは arXiv 版のもの。

## 要旨

Kelly 賭けは長期の成長率を最大にするが、途中で資産が大きく減る（ドローダウン）。実務では fractional Kelly（Kelly 解を一律 $f$ 倍に縮める）が使われるが、これはアドホックである (p.1)。
著者らはドローダウン確率を直接制約に入れた問題を立て、その制約を保守的な凸制約で置き換える（restriction）。得られた解は元の制約を必ず満たす (p.2, p.7-8)。

## モデル

### Kelly 問題（一般形）

- $b \in \mathbb{R}^n$: 資産の配分。$b \ge 0$, $\mathbf{1}^\top b = 1$。最後の成分 $b_n$ は現金（賭けない分）で $r_n = 1$ (p.2)。
- $r \in \mathbb{R}^n_+$: 各賭けの払戻倍率（確率変数）。1回の賭けで資産は $r^\top b$ 倍になる。
- 目的: $\max_b \mathbb{E}\log(r^\top b)$ (p.3, 式1)。

特殊ケースとして、2結果、**相互排他な結果（単勝）**、**一般の有限結果（複勝・馬連・馬単などを含む）**、連続分布を挙げている (p.2-3)。
有限結果なら $\sum_i \pi_i \log(r_i^\top b)$ の最大化で、CVXPY + ECOS（指数錐）でそのまま解ける (p.4)。
期待払戻 $\mathbb{E} r_i \le 1$ がすべての賭けで成り立つとき、そしてそのときに限り「賭けない」が最適 (p.4, Lemma 1)。

### ドローダウンと RCK

- $W^{\min} = \inf_t w_t$、ドローダウンリスクは $\mathrm{Prob}(W^{\min} < \alpha)$ (p.6)。
- 中心の結果 (p.7, 式6): 任意の $\lambda > 0$ について
  $\mathbb{E}(r^\top b)^{-\lambda} \le 1 \Rightarrow \mathrm{Prob}(W^{\min} < \alpha) < \alpha^{\lambda}$。
  停止時刻とマルチンゲール的な不等式から導く。
- RCK 問題 (p.7, 式7): $\max \mathbb{E}\log(r^\top b)$ s.t. $\mathbf{1}^\top b = 1$, $b \ge 0$, $\mathbb{E}(r^\top b)^{-\lambda} \le 1$。
- 有限結果では制約を $\log\sum_i \exp(\log\pi_i - \lambda\log(r_i^\top b)) \le 0$ と書くと log-sum-exp の合成で DCP に乗る (p.10, 式11)。

$\lambda$ はリスク回避パラメータとして読める。$\alpha = 0.7, \beta = 0.1$ なら $\lambda = 6.46$ で、このとき「資産が半分になる確率 ≤ $0.5^{6.46} = 0.011$」も同時に保証される (p.8)。つまり1本の制約が $W^{\min}$ の CDF 全体を $\alpha^\lambda$ で上から抑える。

$\lambda \to 0$ の極限では制約が $\frac{\lambda}{2}\mathrm{var}\log(r^\top b) \le \mathbb{E}\log(r^\top b)$ になる (p.9)。成長率に対する分散の比を抑える制約、という直感的な形である。$\lambda \to \infty$ では無リスクの賭けしか許さない (p.9)。

### 2結果の場合

制約なし Kelly 解 $(\pi P - 1)/(P - 1)$ が制約を満たせばそれが解。満たさなければ二分法で縮める。このとき RCK は fractional Kelly と一致する (p.9-10)。**単一の賭けでは RCK と fractional Kelly は同じもの**で、差が出るのは複数の賭けを組み合わせるときである。

### 二次近似（QRCK）と Markowitz

$r^\top b \approx 1$ でテイラー展開すると凸 QP になり (p.12, 式14)、無裁定の仮定のもとでその解は Markowitz の平均分散ポートフォリオになる (p.12-13)。連続分布では QRCK 解を確率的勾配法（primal-dual）の初期値に使う (p.10-12)。

## 数値実験

20 個の賭け（うち 19 がリスクあり）、100 結果の人工データ。リターンは [0.7, 1.3] 一様で、一部を 0.2 や 2 の極端値にする (p.13)。各賭け方で 10,000 本 × 100 期のモンテカルロ。$\alpha = 0.7$。

| 賭け方 | 成長率 $\mathbb{E}\log(r^\top b)$ | 上界 $\alpha^\lambda$ | MC ドローダウン確率 |
|---|---|---|---|
| Kelly | 0.062 | - | 0.397 |
| RCK $\lambda=6.456$ | 0.043 | 0.100 | 0.073 |
| RCK $\lambda=5.500$ | 0.047 | 0.141 | 0.099 |
| QRCK $\lambda=2.800$ | 0.044 | 0.368 | 0.100 |

（p.14 Table 1, p.15 Table 2）

- 上界は実際のリスクより 30% 程度高い程度で、「緩すぎない」(p.14)。
- ドローダウン確率 0.1 で比べると、fractional Kelly の成長率は約 0.035、RCK は 0.047 (p.17, Figure 4)。
- Kelly は 1 つの賭け（outcome 4）に集中し、RCK はそれを残しつつ他にも分散する (p.14, Figure 3)。
- 対数正規混合の連続分布では Kelly のドローダウン確率 0.569、RCK($\lambda=6.456$) 0.080 (p.18, Table 3)。**ただしこの例では fractional Kelly は RCK と「本質的に同じ」性能** (p.18)。RCK の優位は分布の形に依存する。

## 批判的に読む

- **確率が既知という前提**。$\pi$ と $r$ は真の値として与えられ、推定誤差は扱わない。推定誤差を入れると Kelly は過大に賭ける。これを扱うのは [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md) や [Sun 2018](./2018-sun-distributional-robust-kelly.md)。
- **IID の繰り返し**。同じ分布の賭けを無限回繰り返す設定で、レースごとに出走馬もオッズも変わる競馬とは違う。上界の導出（マルチンゲール）はレースごとに分布が変わっても各回で制約を満たせば成り立ちそうだが、論文は扱っていない（推測）。
- **パリミュチュエルの自己影響なし**。払戻 $r$ は賭け額に依存しない。自分の賭けでオッズが下がる効果は入っていない。
- **実データの検証なし**。実験は人工データのみ。「fractional Kelly より良い」は Figure 4 の有限結果例で、連続分布例では差がない。
- 比較の fractional Kelly は全賭けを一律に縮めるもので、[MacLean 1992](./1992-maclean-growth-versus-security.md) 流の他の手法との比較はない。

## keiba-ai での使い方

- **1レース内の複数券種の配分**: 有限結果（着順の組み合わせ）ごとに各券種の払戻ベクトル $r_i$ を作れば、単勝・複勝・馬連などを混ぜた配分を式11 の CVXPY でそのまま解ける。結果の数は着順の組み合わせ数なので、上位3頭の順列（18頭なら 4,896）程度までなら現実的。確率は Plackett–Luce などの着順モデルから作る。
- **fractional Kelly の代替候補として比較する実験**: 仮説「同じ最大ドローダウン確率（例: 資金が 70% を割る確率 10%）で、RCK は fractional Kelly より成長率が高い」。過去レースの予測確率と確定オッズでバックテストし、資金推移の $W^{\min}$ の分布と対数成長率を両方で比べる。単勝だけなら両者はほぼ同じになるはずなので、券種を混ぜたときに差が出るかを見る。
- **評価指標**: 回収率だけでなく、$\mathbb{E}\log(r^\top b)$（1レースあたりの対数成長率）と $\mathrm{Prob}(W^{\min} < \alpha)$ をバックテストの標準出力にする。
- **注意**: 確率推定の誤差を考えない RCK は過大に賭けうる。確率の較正（キャリブレーション）を先に済ませ、Baker 型の縮小と組み合わせる。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 元の Kelly 基準。本論文はそれに制約を足したもの。
- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): Kelly 解の漸近最適性。RCK の前提。
- [MacLean 1992](./1992-maclean-growth-versus-security.md): 成長と安全性のトレードオフ。fractional Kelly の理論的背景で、本論文の比較対象。
- [MacLean 2010](./2010-maclean-kelly-good-bad-properties.md): Kelly のドローダウンなどの欠点の整理。
- [Whitrow 2007](./2007-whitrow-simultaneous-bets-allocation.md): 同時に多数の賭けをするときの配分アルゴリズム。
- [Deza 2015](./2015-deza-chance-constrained-parimutuel.md): 損失の確率を機会制約で扱う、競馬の実データ版。本論文と同じ問題意識。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md), [Sun 2018](./2018-sun-distributional-robust-kelly.md): 確率の不確実性を入れた Kelly。本論文の「確率既知」を緩める方向。
- [Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md): RCK を含む戦略を実データで比較したレビュー。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): 相互排他でない賭け（複数券種）の Kelly と fractional Kelly。

## 検索語

リスク制約付きKelly, ドローダウン制約, 最大ドローダウン確率, 凸最適化, CVXPY, 分数ケリー, フラクショナルケリー, 資金配分, 平均分散, マーコウィッツ, risk-constrained Kelly, RCK, QRCK, drawdown risk, fractional Kelly, growth-optimal portfolio, log-sum-exp, disciplined convex programming, stochastic gradient, Markowitz, Boyd

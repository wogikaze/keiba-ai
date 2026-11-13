---
title: Chance constrained optimization for parimutuel horse race betting
authors: Deza Antoine, Huang Kai, Metel Michael R.
year: 2015
venue: arXiv:1503.06535v1（改題版 Managing losses in exotic horse race wagering は Journal of the Operational Research Society 69 319-325）
url: https://arxiv.org/abs/1503.06535v1
doi: 10.48550/arXiv.1503.06535
topic: betting-strategy
tags: chance-constrained, parimutuel, exotic-bets, superfecta, minlp, risk-management
verified: fulltext
importance: medium
source: downloaded
source_version: preprint
---

# 4連単（superfecta）の Kelly 賭けに「期間内に一度は当たる」機会制約を付ける

> 一言で: 4連単は当たるまでの平均待ちレース数の中央値が 13,600 レース。Kelly 最大化に「τ レース以内に少なくとも1回払い戻される確率 ≥ 1−α」という機会制約を付け、自分の賭けによる払戻の低下も入れた混合整数非線形計画として解いた。カナダの繋駕速歩 350 レースで、制約あり 28.8%、制約なし 17.8% の利益だった。

原本は arXiv v1（7ページの短い論文）。arXiv の v2 は "Managing losses in exotic horse race wagering" に改題され、Journal of the Operational Research Society 69: 319-325 に掲載された（[Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md) の引用による）。掲載版の中身は未確認。

## 動機：4連単はほとんど当たらない

Flamboro Downs（カナダ・オンタリオ州の繋駕速歩競走場）の1レースについて、全 4 着順列の推定確率から「その順列が当たるまでの平均待ちレース数 $1/\pi_s$」を集計すると (p.2, Table 1):

| 統計量 | レース数 |
|---|---|
| 最小 | 141 |
| 中央値 | 13,600 |
| 平均 | 38,192 |
| 最大 | 566,225 |

1シーズン約 1,200 レースなので、中央値で 11 シーズン以上待つ (p.2)。Kelly は漸近的に最適でも、毎シーズン何らかの収入が欲しい人には合わない。

## モデル

- 期間 τ レースで払戻回数 $B \sim \mathrm{Binomial}(\tau, \pi_{\hat x})$ とし、$P(B \ge 1) \ge 1-\alpha$ を要求する。これは1レースの的中確率 $\pi_{\hat x} \ge 1 - \alpha^{1/\tau}$ と同値（レース間の独立を仮定）(p.2-3)。
- 目的は Kelly（期待対数資金の最大化）。機会制約は「賭ける価値のある買い目があるとき」だけ課す（期待効用を $\log w$ 未満に下げてまで当てにいかない）(p.3)。
- 払戻はパリミュチュエルで自分の賭けを含めて計算する: $P_s(x) = x_s (Q + \sum_u x_u)(1-t) / (Q_s + x_s)$ (p.4)。$Q$ はプール総額、$Q_s$ は順列 $s$ への票、$t$ は控除率 24.7%。
- 最低 0.2 ドル単位の制約を 0-1 変数 $z_s$ で表す。Kallberg–Ziemba の変数変換 $y_s = \log(x_s + Q_s)$ で、線形緩和が凸の MINLP にして IPOPT と Bonmin で大域最適解を得る (p.4-5)。

## 確率と票数の推定

- 勝率: 条件付きロジット（[Bolton 1986](./1986-bolton-conditional-logit.md)）。説明変数は単勝オッズから出した市場の勝率の対数と、CompuBet（市販の予想データ）の2因子の対数の計3つ。R の mlogit (p.3)。
- 着順確率: Lo–Bacon-Shone の割引モデル $\pi_{ijkl} = \pi_i \cdot \pi_j^{\lambda_1}/\sum \pi^{\lambda_1} \cdots$。$\lambda$ もロジットで推定 (p.3-4)。
- **4連単の各順列への票数 $Q_s$**: 公開されるのはプール総額 $Q$ だけ。そこで市場の単勝確率を割引モデル（指数 $\theta$）で 4 着順列に広げたものを「大衆の確率」$\pi^p_s$ とし、的中順列の票数が二項分布に従うとして $\theta$ を最尤推定する。的中順列の払戻から $Q_s = Q(1-t)/P_s$ が逆算できるので、それを観測値に使う (p.4)。Kanto–Rosenqvist の馬連（quinella）の方法の応用。
- 負の対数尤度は凸関数の差。Harville 型の初期値（$\theta=1$）と一様ランダムの初期値（$\theta=0$）から同じ解に収束した (p.4)。

## データと結果

- 2013-2014 シーズンの Flamboro Downs 1,168 レース。前半 70% で確率・票数モデルを推定し、後半 30%（350 レース）で検証 (p.3, p.5)。
- 初期資金 1,000 ドル、τ = 350、α = 0.01 (p.5)。
- 実現払戻は公表払戻を自分の賭けと端数切り捨て（breakage）を考慮して補正して計算 (p.5)。
- 結果: 制約あり（Opt+）28.8%、制約なし（Opt）17.8% の利益 (p.6)。Opt+ は制約を満たすために余分な買い目を足すので途中まで資金が低いが、約 280 レース目にその余分な買い目が当たって逆転した (p.5-6, Figure 1)。

## 批判的に読む

- **1本の資金推移だけ**。350 レースの1経路で、差は 280 レース目の1回の的中で生じている。「10% 以上の改善」はほぼ1回の当たりに依存し、統計的な有意性は示されていない。
- **制約の目的は収益ではなく的中の頻度**。制約を付ければ期待対数成長は下がるはずで（制約付きの最大化だから）、今回の逆転は運とみるのが自然（推測）。
- 検証期間が短い。τ = 350 と検証期間が同じ長さで、制約の効果を見るには複数期間の反復が必要。
- 説明変数に市場の単勝確率を含めているので、モデルは「市場 + 補正」の形。[Benter 1994](./2019-benter-model.md) と同じ発想。
- 自分の賭けによるオッズ低下を入れている点は、多くの Kelly 論文より現実的。ただし締切直前の他の票の流入は考えない（$Q_s$ は期待値で固定）。
- 対象は繋駕速歩（standardbred）で、控除率 24.7%。

## keiba-ai での使い方

- **3連単・3連複での払戻推定**: JRA は 3 連単の全組み合わせのオッズを公開しているので、票数推定の部分は不要。ただし地方競馬や過去データで票数が欠ける場合、「単勝オッズを割引モデルで広げて的中払戻に合わせる」方法は代替になる。
- **自分の賭けによるオッズ低下の式** $x_s(Q + \sum x)(1-t)/(Q_s + x_s)$ は、3連単や WIN5 のような票の薄い券種で賭け額の上限を決めるときに必須。バックテストで確定オッズをそのまま使うと回収率を過大評価する。
- **実験案**: 仮説「3連単の Kelly に『シーズン内に的中が少なくとも1回ある確率 99%』の制約を付けても、期待対数成長の低下は小さい」。制約の有無で、バックテストの対数成長率・的中率・最長不的中レース数を比較する。1経路でなくブートストラップ（レース順のシャッフル）で分布を見る。
- 低確率の券種で「当たるまでの待ち時間」を指標として出すのは、運用上の資金計画に役立つ。

## 関連ノート

- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 同じ著者による、確率推定の不確実性を機会制約で扱う単勝版。
- [Busseti 2016](./2016-busseti-risk-constrained-kelly.md): ドローダウン確率を凸制約にする別の Kelly のリスク管理。本論文を同系統として引用している。
- [Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 単勝 Kelly の明示解。本論文の出発点の一つ。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 自分の賭けによるオッズ変化を入れた最適単勝賭け。
- [Hausch 1981](./1981-hausch-racetrack-market-efficiency.md): Kelly で複勝・3着内の非効率を突いた古典。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 勝率推定の条件付きロジット。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md), [Lo 2008](./2008-lo-ordering-probabilities-approximation.md): 着順確率のモデル。本論文は Lo–Bacon-Shone の割引モデルを使う。
- [Hausch 1994](./1994-hausch-pricing-exotic-wagers.md): エキゾチック券種の価格付け。

## 検索語

機会制約, 確率制約計画, 4連単, スーパーフェクタ, 3連単, エキゾチック券種, パリミュチュエル, 自分の賭けによるオッズ低下, 票数推定, 割引モデル, 混合整数非線形計画, 期間制約, 不的中の連続, 繋駕速歩, chance constrained programming, superfecta, exotic bets, parimutuel, MINLP, Bonmin, IPOPT, discount model, Lo Bacon-Shone, Harville, Kelly criterion, time horizon, harness racing, Flamboro Downs

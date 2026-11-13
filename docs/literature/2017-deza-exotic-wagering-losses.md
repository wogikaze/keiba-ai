---
title: Managing losses in exotic horse race wagering
authors: Deza Antoine, Huang Kai, Metel Michael R.
year: 2017
venue: Journal of the Operational Research Society 69(3) 319-325
url: https://arxiv.org/abs/1503.06535
doi: 10.1057/s41274-017-0213-8
topic: probability-models
tags: betting-strategy, chance-constrained, exotic-bets, superfecta, discount-model, harville-formula, risk-management, kelly, harness-racing
verified: fulltext
importance: medium
source: downloaded
source_version: preprint
---

# 連敗の長さを制約に入れた Kelly 賭け：4連単（superfecta）での機会制約最適化

> 一言で: 「τ レース以内に少なくとも1回は v ドル以上勝つ」確率を $1-\alpha$ 以上にする機会制約を Kelly 最大化に加え、混合整数非線形計画として解く。カナダの繋駕速歩 350 レースで、連敗の最長を 52 → 19 レースまで抑えられたが、総リターンは 7.8% → 1.0% に下がった (p.10, Table 1)。

原本は arXiv v2（2017年8月、15ページ）。JORS 掲載版との差は未確認。

## 問題設定

4連単のように的中頻度が低い賭けは、ディープ・アウト・オブ・ザ・マネーのオプションに似て「小さな損が続き、まれに大きく勝つ」(p.3)。香港のシンジケートでも3か月当たりが出ないのは普通、という実務家の証言を引き、長い連敗は資金より先に運用者の判断を壊すと論じる (p.3)。

分散で危険を測る平均分散法は上振れも罰するので、正の歪度が大きい4連単には合わない。VaR は本来テール損失の指標だが、ここでは損失の上限が賭け金なので、$v\le 0$ 側で使うと「連敗の制御」に転用できる、というのが着想 (pp.3-4)。

## モデル

賭け $x=\lbrace x_s\rbrace $（$s$ は上位4頭の並び）、払戻を $P(x)$ とする。

- 1レースで $v$ 以上の利益が出る確率を $\tilde\pi_x$ とし、τ レースで1回以上起きる確率を $1-\alpha$ 以上にしたい。独立なら $\tilde\pi_x \ge 1-\alpha^{1/\tau}$ が条件になる (p.4)。
- 最適化問題 (p.5):

$$\max_x\ E\log\Big(P(x)+w-\sum_s x_s\Big)\quad \text{s.t.}\ \sum_s x_s\le w,\ \ \Pr\Big(P(x)-\sum_s x_s\ge v\Big)\ge 1-\alpha^{1/\tau},\ x_s\ge0$$

- パリミュチュエルの払戻は自分の賭けで下がるので $P_s(x)=x_s\,(Q+\sum_u x_u)(1-t)/(Q_s+x_s)$ とする。$Q$ はプール総額、$Q_s$ は他人の $s$ への投票額、$t$ は控除率。端数切り捨て（breakage）は無視 (p.6)。
- 機会制約は「この並びが来たら $v$ 以上勝つ」を表す二値変数 $z_s$ で書き、$\sum_s \pi_s z_s\ge 1-\alpha^{1/\tau}$ とする (pp.7-8)。これで MINLP になり、IPOPT と Bonmin で解く。計算量を抑えるため、期待利益の上位 50% の並びだけを候補にする（それでも推定確率の中央値で 84% を覆い、勝ち並びは常に含まれた）(p.8)。
- 実際の賭け金は Kelly 解に分数 $f=0.5$ を掛け、最小単位 $b$ に丸める (p.7, p.9)。

## 確率と他人の投票額の推定

### 勝率

Bolton–Chapman 型の多項ロジットで、変数は最終単勝オッズの暗黙確率の対数、CompuBet 社の指標 Pre（データの質）と Class の対数。有意でない変数を後退的に落とした (p.14, Table 3)。

| 変数 | 係数 |
|---|---|
| $\log \pi^m$（最終オッズ） | 1.083 |
| $\log$ Pre | 0.421 |
| $\log$ Class | 0.728 |

テスト期間の McFadden $R^2$ はモデル 0.2181、市場 0.2145 で、差は 0.0036 と小さい (p.14)。

### 4連単の着順確率（Lo–Bacon-Shone の discount 近似）

Harville は本命寄りに偏るとして、Lo and Bacon-Shone (2008) の近似を使う (p.6):

$$\pi_{ijkl}=\pi_i\cdot\frac{\pi_j^{\lambda_1}}{\sum_{s\ne i}\pi_s^{\lambda_1}}\cdot\frac{\pi_k^{\lambda_2}}{\sum_{s\ne i,j}\pi_s^{\lambda_2}}\cdot\frac{\pi_l^{\lambda_3}}{\sum_{s\ne i,j,k}\pi_s^{\lambda_3}}$$

対数尤度が段ごとに分離できるので、$\lambda$ は段ごとに多項ロジットで個別に推定できる。推定値は $\lambda_1=0.601,\ \lambda_2=0.385,\ \lambda_3=0.262$ (p.15, Table 4)。
下の着順ほど $\lambda$ が小さい、つまり勝率の差が効かなくなり、ランダムに近づく。$\lambda=1$ の Harville からかなり離れている。

### 他人の投票額 $Q_s$

公表払戻 $P_s$ から $Q_s=Q(1-t)/P_s$ を逆算し、大衆の4連単確率も同じ discount 型（指数 $\theta_1..\theta_4$）で単勝暗黙確率から作ると仮定して、投票数を二項分布で最尤推定する (p.6)。

| | $\theta_1$ | $\theta_2$ | $\theta_3$ | $\theta_4$ |
|---|---|---|---|---|
| 大衆 | 1.206 | 0.822 | 0.531 | 0.415 (p.15, Table 5) |

$\theta_1>1$ は、大衆が4連単の1着を単勝オッズ以上に本命へ寄せて買っていることを意味する（解釈は本ノート）。
推定の不確実性に備え、$\theta\sim N(\hat\theta,\Sigma)$ から 9,999 回サンプルし、$\pi^p_s$ の 99 パーセンタイル（＝自分に不利な側）を使う (pp.6-7)。

## データと結果

- カナダ・オンタリオ州 Flamboro Downs の 2013-2014 シーズン、1,168 レース。**繋駕速歩（スタンダードブレッド）**であり平地競走ではない (p.5)。前半 70% で推定、後半 30%（350 レース）で検証 (p.5, p.9)。
- 控除率 $t=24.7\%$、最小単位 $b=\$0.2$、初期資金 \$5,000、$f=0.5$、$\alpha=0.05$、$v=\$20.24$ (p.9)。
- 払戻は公表払戻を自分の賭けと breakage で補正して計算 (p.9)。

| τ | 最長連敗 | 総リターン (%) | 賭けたレース | 1レース平均賭け金 (\$) |
|---|---|---|---|---|
| ∞（制約なし） | 52 | 7.8 | 224 | 10.8 |
| 40 | 40 | 4.5 | 163 | 14.4 |
| 30 | 27 | 4.0 | 123 | 20.5 |
| 20 | 19 | 1.0 | 61 | 37.9 |

(p.10, Table 1)。連敗の長さは指定どおり τ 以下に収まった。制約を強めると賭けるレースが減り、1レースあたりの賭け金は増える（多くの並びで利益が出るよう広く買う必要があるため）(p.10)。

## 批判的に読む

- **検証は 350 レース・1シーズン・1場**。総リターン 7.8% や 1.0% に信頼区間はなく、τ の違いによる差がノイズか判断できない。τ の候補（40, 30, 20）と $v$ はテスト期間の τ=∞ の結果（最長連敗 52、最小利益 \$20.24）を見て決めているので、制約の設定にテスト期間の情報が漏れている (p.9)。
- 勝率モデルの優位は McFadden $R^2$ で 0.0036 とわずかで、利益の源泉が勝率の改善なのか、discount 近似と大衆の $\theta$ の差（4連単プールの歪み）なのかは分解されていない。
- 他人の投票額は最終オッズからの事後推定で、締切前に分かる量ではない。最終オッズで賭けられる前提のシミュレーションである。
- 独立性の仮定のもとで連敗確率を計算しており、モデルの誤指定（確率が過大）があると実際の連敗は長くなる。著者も点推定の使用を限界に挙げる (p.10)。
- コードとデータは公開されていない。CompuBet 指標は商用。

## keiba-ai での使い方

- **3連単・3連複の確率生成**: 勝率モデルの出力から discount 近似で着順確率を作る。$\lambda$ は段ごとに独立な多項ロジットで推定できるので実装が軽い。仮説: JRA でも $\lambda_1<1,\ \lambda_2<\lambda_1$ となり、Harville（$\lambda=1$）より3連単の対数尤度が改善する。比較指標は3連単の的中組の負の対数尤度。
- **大衆の着順確率の推定**: 3連単オッズ（JRA は全組み合わせのオッズが公開）から大衆の $\theta$ を推定すれば、単勝オッズと3連単オッズの間の歪み（大衆が2・3着をどう見ているか）を測れる。JRA では $Q_s$ を推定する必要がなく、オッズから直接得られるのが利点。
- **資金管理の評価指標**: 回収率と最大ドローダウンに加えて「最長連敗（レース数）」を実験ログに記録する。3連単戦略では、回収率の差より連敗長の差の方が実運用上の判断に効く可能性がある。
- **自分の賭けによる払戻低下**: $P_s(x)$ の式はそのまま JRA のパリミュチュエルに使える。賭け金が大きいシミュレーションでは払戻を補正する。

## 関連ノート

- [Lo 2008](./2008-lo-ordering-probabilities-approximation.md): discount 近似の原典（原本未取得）。本論文の式と推定値が近似の具体例になる。
- [Lo 2008](./2008-lo-probability-statistical-models-racing.md): Harville の偏りと Henery/Stern をまとめたレビュー。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): $\lambda=1$ の特殊ケース。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 勝率の多項ロジット。
- [Deza 2015](./2015-deza-chance-constrained-parimutuel.md): 同じ著者らの機会制約パリミュチュエル賭け。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 同じ著者による確率推定の不確実性を考えた Kelly。
- [MacLean 1992](./1992-maclean-growth-versus-security.md): 成長と安全性のトレードオフ（分数 Kelly）。
- [Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 単勝の Kelly 最適解。

## 検索語

4連単, スーパーフェクタ, 3連単, エキゾチック馬券, 連敗, 損失管理, 機会制約, 確率制約計画, VaR, バリュー・アット・リスク, 分数 Kelly, ハーフ Kelly, 混合整数非線形計画, discount モデル, 着順確率, Harville 補正, 大衆の着順確率, 繋駕速歩, superfecta, exotic wager, losing streak, chance-constrained optimization, MINLP, Bonmin, IPOPT, fractional Kelly, discount model, Lo Bacon-Shone approximation, harness racing, Flamboro Downs, parimutuel payout

---
title: Kelly betting on horse races with uncertainty in probability estimates
authors: Metel Michael R.
year: 2017
venue: arXiv
url: https://arxiv.org/abs/1701.02814
doi: 10.48550/arXiv.1701.02814
topic: betting-strategy
tags: kelly, estimation-error, multinomial-logit, stochastic-optimization, fractional-kelly
verified: fulltext
importance: high
source: downloaded
source_version: preprint
---

# 条件付きロジットの推定誤差を織り込んだ単勝 Kelly：期待確率・下界・機会制約

> 一言で: 条件付きロジット（多項ロジット）で推定した勝率には係数の推定誤差がある。係数を $\beta \sim N(\hat\beta, \Sigma)$ とみなし、勝率の期待値（モンテカルロ）や機会制約で Kelly を解くと、点推定の Kelly より期待対数成長が少し上がった。半分 Kelly はこの人工実験ではむしろ大きく劣った。

原本は arXiv v2（2017年8月）。査読者への謝辞があるが、掲載誌は未確認。

## 問題意識

推定確率をそのまま Kelly に入れると、過大評価された馬に系統的に多く賭けてしまう（誤差が平均で打ち消し合わない）(p.2)。実務の対処は fractional Kelly（Benter や Thorp が使った）で、2結果なら [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md) が縮小係数を導いた。本論文は**多結果（単勝の n 頭）**で、勝率がロジットで推定される場合を扱う (p.2)。

## モデル

### 基本問題 (P)

$\max_x \sum_h \pi_h \log(x_h O_h + w - \sum_i x_i)$ s.t. $\sum_h x_h \le w$, $x \ge 0$ (p.3)。
$x_h$ は馬 $h$ への賭け額、$O_h$ は小数オッズ（固定と仮定）、$w$ は現在資金。厳密解は [Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md) のアルゴリズムで求まる。

### 勝率の推定と不確実性

- 勝率は条件付きロジット $\pi_h = e^{\beta' v_h} / \sum_i e^{\beta' v_i}$（[Bolton 1986](./1986-bolton-conditional-logit.md) の方式）(p.3)。
- 最尤推定 $\hat\beta$ の共分散は、モデルの誤特定を考えてサンドイッチ推定 $\Sigma = I^{-1} V I^{-1}$ を使う (p.4)。競馬の着順を決める要因は多すぎて真のモデルとは考えられない、というのが理由。
- $\beta \sim N(\hat\beta, \Sigma)$ とすると勝率はロジスティック正規分布に従う (p.5)。

### 比較する定式化

| 記号 | 中身 | ページ |
|---|---|---|
| (S) | 点推定 $\pi(\hat\beta)$ をそのまま使う標準 Kelly | p.4 |
| (F) | (S) の 50% fractional Kelly | p.11 |
| (Emc) | $\mathbb{E}[\pi_h]$ をモンテカルロで求めて (P) に入れる | p.5 |
| (Elb) | 正規 MGF と Jensen で $\mathbb{E}[\pi_h]$ の下界を作る。確率の和が1に足りない分は「全額没収」の仮想結果にする | p.5-6 |
| (CC) | 「目的値 $\ge t$ が確率 $1-\alpha$ 以上で成立」の機会制約で $t$ を最大化 | p.6 |
| (CC2) | 2結果のときの (CC) の厳密な決定論的等価 | p.7, 付録 |
| (CCN) | n 結果用。$\pi$ を S 個サンプルし、最大 $S\alpha$ 個の違反を許す混合整数問題。ヒューリスティックで違反集合を決めて凸問題に落とす | p.8 |
| (ECC) | (Emc) の目的 + 「真の期待対数資金が $\log w$ を下回らない確率 $\ge 1-\alpha$」 | p.9 |

(Elb) の下界は $\mathbb{E}(\pi_h) \ge e^{\hat\beta' v_h} / \sum_i e^{\hat\beta' v_i + \frac12 (v_i - v_h)'\Sigma(v_i - v_h)}$ (p.5)。他馬との特徴量の差が不確かな係数方向に大きいほど、その馬の勝率は割り引かれる。

## 実験設定（人工データ）

- 係数 $\hat\beta$ は 10 次元の標準正規。各係数の標準偏差は p 値が 0.05 以下になる範囲で乱数 (p.9)。
- 真の係数 $\beta^t$ を $N(\hat\beta, \Sigma)$ から1つ引き、特徴量は一様乱数で真の勝率を作る (p.9)。
- 評価は実現資金ではなく、**真の確率のもとでの期待対数成長**を合計する（分散を減らすため）(p.10)。オッズも全馬同一の固定値。
- 4実験 × 2,500 試行: (E1) 2頭 O=1.1, (E2) 2頭 O=1.2, (E3) 10頭 O=2, (E4) 30頭 O=4 (p.10, Table 1)。

## 結果

期待対数成長の合計 (p.11, Table 2, 抜粋):

| モデル | E1 | E2 | E3 | E4 | 合計 |
|---|---|---|---|---|---|
| (T) 真の確率 | 3.051 | 16.861 | 4.385 | 3.166 | 27.463 |
| (S) 標準 Kelly | 1.583 | 12.214 | 2.383 | 1.954 | 18.134 |
| (F) 半分 Kelly | 1.210 | 8.754 | 1.788 | 1.515 | 13.268 |
| (Elb) | 1.852 | 12.179 | 2.353 | 1.823 | 18.206 |
| (Emc) | 1.820 | 12.297 | 2.390 | 1.964 | 18.471 |
| (CCx) α=0.10 | 1.080 | 9.027 | 1.206 | 0.846 | 12.158 |
| (ECCx) α=0.40 | 1.825 | 12.288 | 2.390 | 1.980 | 18.484 |

- 推定誤差による損失が大きい: 真の確率なら 27.5、点推定なら 18.1 (p.11-12)。
- (Emc) と (ECCx, α=0.4) は全実験で (S) を上回る。改善幅は合計で 2% 程度 (p.11)。
- 機会制約を厳しくする（α を小さくする）と成長が大きく落ちる。著者も「小さい α ではリスク対策として攻めすぎ（過剰に保守的）」と認める (p.11)。
- 半分 Kelly (F) は (S) より明確に悪い。この実験設定では過大賭けより過小賭けの損が大きかった。

## 批判的に読む

- **オッズが市場と無関係**。全馬同一の固定オッズで、エッジの大きさは人工的。実際の単勝ではオッズが他の参加者の確率評価を反映するので、推定誤差とエッジの相関（過大評価した馬ほど「割安」に見える）がもっと強く出るはず。Table 2 の「半分 Kelly が劣る」は設定依存とみるべき（推測）。
- **評価は期待値で、実現資金ではない**。ドローダウンや破産の頻度は見ていない。リスク面の比較は別途必要。
- **不確実性は係数の推定誤差だけ**。特徴量の欠落やモデル構造の誤り（バイアス）は $\Sigma$ のサンドイッチ推定で一部しか拾えない。
- 試行数 2,500、Matlab fmincon。コードの公開は未確認。

## keiba-ai での使い方

- **推定誤差の取り込み方の雛形**: 条件付きロジットや Plackett–Luce 系のモデルなら、係数の共分散（サンドイッチ推定、またはブートストラップ）から勝率をサンプリングし、平均勝率 $\mathbb{E}[\pi_h]$ を Kelly に入れる (Emc) は実装が軽い。勾配ブースティングならブートストラップ・アンサンブルの平均で近似できる（推測）。
- **実験案**: 仮説「勝率をアンサンブル平均（Emc 相当）にすると、点推定 Kelly より期待対数成長が上がり、半分 Kelly との差は市場オッズ込みのバックテストでは縮む（または逆転する）」。評価は確定オッズでのバックテストの対数成長率と最大ドローダウン。
- (Elb) の下界は「不確実な特徴量に頼る馬ほど割り引く」効果を持つ。新馬・転入馬などデータが少ない馬の過大賭けを抑える手段として試す価値がある。
- 全体の教訓として、真の確率との成長率の差（27.5 対 18.1）は大きい。賭け方の工夫より確率推定の改善のほうが効くことを示唆する。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 基礎となる基準。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 本論文が前提とする条件付きロジットの勝率推定。
- [Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 問題 (P) の厳密解アルゴリズム。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md): 2結果での縮小係数。本論文はその多結果版を目指す。
- [MacLean 1992](./1992-maclean-growth-versus-security.md): 推定値を使うと過大賭けになるという指摘と fractional Kelly。
- [Deza 2015](./2015-deza-chance-constrained-parimutuel.md): 同じ著者グループの機会制約モデル（損失の連続を制約）。
- [Sun 2018](./2018-sun-distributional-robust-kelly.md): 確率の不確実性を分布ロバスト最適化で扱う別アプローチ。
- [Busseti 2016](./2016-busseti-risk-constrained-kelly.md): 確率既知でのドローダウン制約。
- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 相互排他な多結果での最適賭けの解析。

## 検索語

推定誤差, パラメータ不確実性, 確率の不確実性, 条件付きロジット, 多項ロジット, サンドイッチ推定, 機会制約, 確率制約計画, 単勝, ケリー基準, 半分ケリー, Kelly criterion, estimation error, parameter uncertainty, multinomial logit, conditional logit, logistic-normal, sandwich estimator, chance constraint, chance-constrained programming, stochastic optimization, fractional Kelly, overbetting

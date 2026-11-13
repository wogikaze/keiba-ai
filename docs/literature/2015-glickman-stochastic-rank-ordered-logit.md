---
title: A stochastic rank ordered logit model for rating multi-competitor games and sports
authors: Glickman Mark E., Hennessy Jonathan
year: 2015
venue: Journal of Quantitative Analysis in Sports 11(3) 131-144
url: https://www.degruyterbrill.com/document/doi/10.1515/jqas-2015-0012/html?lang=en
doi: 10.1515/jqas-2015-0012
topic: probability-models
tags: rank-ordered-logit, plackett-luce, state-space, dynamic-rating, bayesian, mcmc, ties, rating-system
verified: fulltext
importance: medium
source: downloaded
source_version: accepted-manuscript
---

# 能力が時間とともに動く順位ロジット：状態空間モデルと近似ベイズフィルタによるレーティング

> 一言で: 着順を順位ロジット（ROL = Plackett–Luce）で、各競技者の能力の時間変化をガウスのランダムウォークでモデル化し、MCMC による完全ベイズ推定と、毎期の事後分布を正規近似して更新する軽いフィルタ（Glicko の多者版）を作った。女子アルペン滑降 103 大会で、フィルタは完全ベイズとほぼ同じ予測精度で、計算は2日から1分未満になった (p.25, Table 3; p.27)。

原本は著者サイトの 2015年1月29日付の原稿（33ページ）。ページは原稿のもの。

## モデル

### 順位の尤度

期 $t$ の競技者 $i$ の能力を $\theta_{it}$、レースでの潜在パフォーマンスを $Y_i\mid\theta_{it}\sim\mathrm{Gumbel}(\theta_{it})$（独立）とすると、着順 $1,2,\dots,m$ の確率は (pp.4-5, 式2-4)

$$L=\prod_{j=1}^{m-1}\frac{\exp(\theta_j)}{\sum_{l=j}^{m}\exp(\theta_l)}$$

で、1着が全員に勝つ確率 × 2着が残りに勝つ確率 × … という多項ロジットの積になる。Plackett–Luce、exploded logit、rank-ordered logit は同じモデルの別名 (p.3)。能力は定数を足しても尤度が変わらないので、$\sum_i\theta_{it}=0$ などの制約を置く。

### 能力の時間変化

$\theta_{t+1}=\theta_t+\omega_t$、$\omega_t\sim N(0,\Upsilon)$。$\Upsilon=\tau^2(I-\tfrac1n\mathbf{1}\mathbf{1}^\top)$ とすると、イノベーションの平均がゼロになり、順位データからは分からない「全員一斉の能力変化」を排除できる (p.6, 式6-7)。自己回帰 $\theta_{t+1}=\nu\theta_t+\omega_t$ への拡張も示す (p.6)。初期能力は $\theta_{i1}\sim N(0,\sigma_1^2)$。

### 同着と完走できなかった者

同着は (1) 潜在パフォーマンスが近いときに同着になるモデル、(2) 同着者のあらゆる並べ方の混合尤度、の2通りがありうる。本論文は (2) を採り、MCMC の各反復で同着者の順序を無作為に並べ替えて条件付けることで、混合尤度を計算せずに済ませる (pp.8-9)。完走できなかった者は最下位の同着として扱える (p.8)。

## 近似ベイズフィルタ（レーティング更新）

全期間の MCMC は重いので、期ごとに次を繰り返す (pp.10-16)。

1. 期 $t$ の開始時、各競技者の能力を独立な正規分布 $N(\mu_{it},\sigma_{it}^2)$ とみなす（事前）。
2. その期の全レースの ROL 尤度と事前分布の積（対数事後）のモードを Newton–Raphson で求め、モードでの2階微分の逆行列の符号反転を事後分散とする。
3. 次期の事前分布は $N(\mu^*_{it},\sigma^{2*}_{it}+\tau^2)$（ランダムウォークの分散を足す）(式15-16)。
4. 同着は、同着者それぞれを「同順位以下の全員に勝つ」因子にする近似で扱う（Baker and McHale の方法）。
5. $\tau,\sigma_1$ は、検証期間の予測順位と実際の順位の Spearman 相関（重み付き平均）を Nelder–Mead で最大化して決める (p.16)。

共分散は各期の後でゼロに戻るので、同じレースに何度も一緒に出た2人の相対能力の精度は失われる、と著者は限界を述べる (p.26)。

## 適用例：女子アルペン滑降

- 2002年2月〜2013年12月の FIS の 103 大会、268 人。年平均 1.58 大会の出場で、51 人は1大会のみ (p.17)。
- 実際のタイムは提供されず、FIS のポイントによる順位のみ。ポイント同点の同着が 4.4%、上位 30 位に入れずポイントなしの「最下位同着」が 8.7%、計 13.1% が同着 (pp.17-18)。
- 6か月を1期として 24 期。MCMC は JAGS で2チェーン、バーンイン 10,000、本サンプル 20,000 (p.18)。

| パラメータ | 完全ベイズ 事後平均 (95% 区間) | 近似フィルタ 最適化値 |
|---|---|---|
| $\tau$（期あたりの能力変化の標準偏差） | 0.352 (0.310, 0.399) | 0.295 |
| $\sigma_1$（初期能力の標準偏差） | 0.451 (0.083, 0.668) | 0.313 |

(p.19, Table 1)。$\tau$ は能力の散らばりに比べて大きく、半年で能力が大きく動きうる。

2013年後半の上位 20 人の事後平均は、近似フィルタの方が一様に 0.5 程度低いが、順位はほぼ一致する。ROL は能力の定数差に不変なので確率には影響しない (pp.20-21, Table 2)。Vonn が Mancuso に勝つ確率の推移は、両方法で 0.05 以内（1期だけ 0.076）の差 (p.22, Fig.2)。

### 予測精度

学習に使っていない7大会（2013年12月〜2014年3月）で、事後平均の順位と実際の着順の Spearman 相関を重み付き平均した (pp.23-25)。

| 方法 | 3か月 | 6か月 | 12か月 |
|---|---|---|---|
| 完全ベイズ | 0.580 | 0.586 | 0.614 |
| 近似フィルタ | 0.601 | 0.587 | 0.596 |

(p.25, Table 3)。標準誤差は約 0.06 で、どの方法も他を明確には上回らない (p.25)。

計算時間は完全ベイズが2日、近似フィルタは最適化込みで1分未満 (p.27)。

## 批判的に読む

- **予測評価は7大会のみ**で、標準誤差 0.06 に対し方法間の差は 0.03 程度。期の長さや方法の優劣について結論は出せない。著者もそう述べている。
- 評価指標は Spearman 相関で、確率予測としての良さ（対数尤度、校正）は評価していない。賭けや勝率予測に使うには、ROL の確率そのものの評価が必要。
- 予測時の能力は「最後の期の事後平均」で、評価期間中に更新していない。
- 共変量（コース、天候、用具）はない。能力の変化はすべてランダムウォークが吸収する。
- 近似フィルタの $\tau,\sigma_1$ は最後の3期で予測相関を最大化して決めており、その3期は MCMC 側の学習にも含まれる。テスト7大会とは分離されている。
- 再現性: データは米国オリンピック委員会提供で非公開。

## keiba-ai での使い方

- **馬・騎手の動的レーティング特徴量**: 各馬の能力を ROL の状態空間で追跡し、レース前時点の $\mu_{it}$（平均）と $\sigma_{it}$（不確実性）を特徴量にする。Elo や TrueSkill より、多頭数の着順をそのまま使える点で競馬向き。仮説 H1: 近似フィルタの $\mu$ と $\sigma$ を GBDT に加えると、前走着順・スピード指数だけのモデルより単勝 log loss が下がり、特に出走数の少ない馬で効く。
- **期の取り方**: 競馬では1期 = 1レース（馬ごとに出走のたびに更新）とし、前走からの日数に比例して $\tau^2$ を足す形（$\tau^2\Delta t$）が自然。休養明けの不確実性が自動的に大きくなる。
- **競走中止・同着**: 中止馬を最下位同着として扱う方法は、そのまま JRA の中止・失格に使える。
- **リーク防止**: フィルタは時系列順に1回通すだけなので、特徴量は自然に「そのレース以前の情報のみ」になる。完全ベイズ（スムーザ）の値を特徴量にすると未来の情報が入るので使わない。
- **$\tau$ の決め方**: 本論文は順位相関で最適化したが、keiba-ai では検証期間の ROL 対数尤度で最適化する。

## 関連ノート

- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): ROL の原典。
- [Luce 1959](./1959-luce-individual-choice-behavior.md): 多項ロジットの選択公理。
- [Guiver 2009](./2009-guiver-bayesian-plackett-luce.md): 静的な P-L のベイズ推論（EP）。本論文は時間変化を加える。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): P-L の最尤推定（MM）。
- [Henery 1981](./1981-henery-permutation-probabilities.md), [Stern 1990](./1990-stern-gamma-permutations.md): Gumbel 以外のパフォーマンス分布。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 競馬の exploded logit。
- [Baker 2020](./2020-baker-order-statistics-ranking.md): 順序統計量に基づく順位モデル。
- [Wilkens 2026](./2026-wilkens-plackett-luce-uk-racing.md): 英国競馬への P-L 適用。

## 検索語

順位ロジット, ランクロジット, 爆発ロジット, Plackett-Luce, 状態空間モデル, 動的レーティング, 能力の時間変化, ガウスランダムウォーク, ベイズフィルタ, 近似ベイズ, Glicko, Elo, TrueSkill, MCMC, JAGS, 同着, 競走中止, 最下位同着, Spearman 相関, アルペンスキー, rank ordered logit, ROL, exploded logit, state-space model, dynamic rating, random walk, Bayesian filter, Newton-Raphson, ties, Gumbel, extreme value distribution, multi-competitor games, Glickman

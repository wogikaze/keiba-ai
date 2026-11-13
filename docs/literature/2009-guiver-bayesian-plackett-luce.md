---
title: Bayesian inference for Plackett-Luce ranking models
authors: Guiver John, Snelson Edward
year: 2009
venue: Proceedings of the 26th International Conference on Machine Learning (ICML 2009) 377-384
url: https://icml.cc/Conferences/2009/papers/347.pdf
doi: 10.1145/1553374.1553423
topic: probability-models
tags: plackett-luce, bayesian, expectation-propagation, partial-ranking, motor-racing, gamma-prior, sparse-data
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# Plackett–Luce のベイズ推論を Power EP で解く：出走数の少ない選手を過大評価しない

> 一言で: Plackett–Luce（P-L）の強さパラメータに gamma 事前分布を置き、Power EP（$\alpha=-1$）のメッセージ伝播で事後分布を近似する方法。NASCAR 2002 年シーズンで、最尤推定（MM 法）が1戦しか走っていない選手を1位・2位にしてしまう過学習を、事後平均では起こさないことを示した (p.6, Table 1)。

## 背景：最尤推定の2つの問題

P-L の最尤推定には Hunter (2004) の MM アルゴリズムがあるが、著者は2つの欠点を挙げる (pp.1, 3)。

1. **疎なデータで過学習する**。観測が少なく項目が多い、あるいは各観測が一部の項目しか順位付けしない場合。
2. **解が存在しないことがある**。MM の収束には「項目をどう2分割しても、後者の誰かが前者の誰かに少なくとも1回勝っている」という仮定が必要で、全出走で最下位の選手がいると破れる。NASCAR データでは4人がこれに当たり、Hunter はこの4人を除外していた (p.5)。

ベイズ推論なら適切な事前分布でどちらも回避でき、パラメータの不確実性も得られる。

## モデル

順序 $\omega=(\omega_1,\dots,\omega_K)$（$\omega_k$ は $k$ 位の項目）の確率は (p.2, 式1-2)

$$PL(\omega\mid v)=\prod_{k=1}^{K}\frac{v_{\omega_k}}{v_{\omega_k}+\dots+v_{\omega_K}}$$

- $v_i\ge0$ は項目 $i$ の強さ。1位から順に、残った項目の中から $v$ に比例して選ぶ（「壺」モデル）。
- **Thurston 解釈**: 各項目が独立な得点を持ち、分布が平均だけ異なるとき、順位分布が P-L になるのは得点が Gumbel 分布のとき、かつそのときに限る（Yellott 1977）(p.2)。Gumbel の自然パラメータ $v=e^{\mu/\beta}$ の共役事前分布が gamma であることが、$v$ に gamma 事前を置く理由になる (pp.2-3)。
- 競馬の言葉で言えば、走破時間（の符号を反転したもの）が Gumbel なら着順は P-L、つまり Harville の公式と同じ構造になる。
- 正規分布の得点（TrueSkill）は Luce の選択公理を満たさないので P-L にはならない (p.3)。

## アルゴリズム

事後分布 $p(v\mid\Omega)\propto\prod_n\prod_k f^{(n)}_k(v)$ を、各 $v_i$ の gamma 分布の積 $q(v)=\prod_i \mathrm{Gam}(v_i\mid\alpha_i,\beta_i)$ で近似する (p.3, 式5-9)。

1. 事前メッセージを広い $\mathrm{Gam}(3.0, 2.0)$、他のメッセージを一様に初期化する (p.5)。
2. 収束するまで繰り返す。
   1. 因子 $a=(n,k)$（観測 $n$ の $k$ 位の選択）を1つ選ぶ。
   2. その因子に入るメッセージ（他の因子からのメッセージの積）を計算する。
   3. 因子を掛けた分布を gamma に射影する。P-L の因子は分数で扱いにくいので、$\alpha$-ダイバージェンスを $\alpha=-1$ にとると因子が逆数 $\sum_{l\ge k} v_{\omega_l}/v_{\omega_k}$ になり、和の期待値として1次・2次モーメントが閉じた形で計算できる (p.4)。
   4. モーメント一致で出力メッセージを更新する。
3. 周辺分布は全メッセージの積で得る。$v$ には定数倍の自由度があるので、平均の和を1などに正規化する (p.5)。

モデルエビデンスも計算できるので、P-L の混合モデルの成分数をベイズ因子で選べる、と著者は述べる (p.5)。

**不完全な順位**: P-L は内部整合的で、一部の項目だけの順位の確率は、残りの項目の位置を周辺化したものと一致する。したがって各観測では、そのレースに出た項目の因子だけを掛ければよい。上位 S 位だけ観測される場合も、$k>S$ の因子を落とすだけで扱える (p.5)。

## 実験

### 既知パラメータの復元

$v=(1,2,\dots,10)$ から生成した 5, 50, 5,000 観測で推定し、観測が増えると事後分布が真値の周りに縮むことを確認 (p.5, Fig.1)。大きい $v$ ほど不確実性が大きい。$v_{10}/v_9$ は $v_2/v_1$ より比が小さく、上位の選択ほど決着がはっきりしないため (p.5)。

### NASCAR 2002

36 レース、延べ 87 人、1レース 43 人。MLE と比べるため Hunter と同じ 83 人に絞った (p.5)。

| 選手 | 出走 | 平均着順 | MLE 順位 | EP 順位 | EP 平均 $v$ | EP 標準偏差 |
|---|---|---|---|---|---|---|
| PJ Jones | 1 | 4.00 | 1 | 18 | 0.0159 | 0.0079 |
| Scott Pruett | 1 | 6.00 | 2 | 19 | 0.0156 | 0.0078 |
| Mark Martin | 36 | 12.17 | 4 | 1 | 0.0278 | 0.0047 |
| Rusty Wallace | 36 | 13.17 | 5 | 2 | 0.0275 | 0.0046 |
| Mike Bliss | 1 | 14.00 | 3 | 23 | 0.0146 | 0.0073 |
| Morgan Shepherd | 5 | 41.20 | 78 | 83 | 0.0041 | 0.0016 |

(p.7, Table 1 から抜粋)。1戦だけの好走者は EP では中位に下がり、標準偏差が大きい。逆に5戦すべて下位の Morgan Shepherd は、1〜2戦の下位選手より確信をもって最下位に置かれる。
平均着順が同じでも P-L の順位は違う。誰と走ったかを考慮し、強い相手のレースで勝つ方が価値が高いため (p.6)。

### MovieLens

943 ユーザーの評価をジャンルの順位に変換して推定（部分順位）。全体では War が1位、25-29 歳では Film-Noir が1位。55-59 歳は 32 人しかいないため標準偏差が大きい (p.7, Table 2)。

## 批判的に読む

- 評価は MLE との順位の比較と定性的な議論が中心で、**予測性能（未来のレースの対数尤度など）での比較はない**。事後平均が「もっともらしい」順位を与えることは示したが、予測が良くなるかは示していない。
- 事前分布 $\mathrm{Gam}(3,2)$ の選び方の感度分析はない。少数出走の選手の位置は事前分布でほぼ決まるので、結果はこの選択に依存する。
- 強さ $v$ はシーズンを通じて一定で、時間変化や共変量（コース、天候）はない。競馬の予測にはそのままでは使えない。
- 近似の精度（MCMC との比較）は示されていない。

## keiba-ai での使い方

- **出走数の少ない馬・騎手の強さの推定**: 新馬や出走の少ない馬、乗鞍の少ない騎手の強さを P-L で推定すると、MLE は少数の好走を過大評価する。gamma 事前（あるいは L2 正則化、階層ベイズ）で縮小する。仮説: 騎手・調教師の P-L 強さを特徴量にするとき、事前で縮小した版は MLE 版より、出走数の少ない層で log loss が良い。
- **部分順位の扱い**: JRA の着順は全頭の順位が得られるが、競走中止や降着がある。P-L の内部整合性により、中止馬を「順位不明」として因子から外すだけで整合的に扱える。
- **Thurston–Gumbel の対応**: 勝率モデル（softmax）を着順確率に拡張すると P-L になる、という理論的根拠。正規誤差（Henery、TrueSkill）を選ぶと P-L ではなくなる点に注意。
- **モデル選択**: P-L の混合（例: 先行型・差し型のような潜在クラス）をエビデンスで比べる方向は未検証の拡張として残る。

## 関連ノート

- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): P-L 分布の原典（競馬の着順への応用を含む）。
- [Luce 1959](./1959-luce-individual-choice-behavior.md): 選択公理。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 比較対象の MM 法と NASCAR データの出典。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 勝率から作る着順確率。P-L と同じ構造。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規得点の Thurston モデル。P-L にならない側。
- [Glickman 2015](./2015-glickman-stochastic-rank-ordered-logit.md): 順位ロジットの拡張（スケールの確率化）。
- [Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md): 競馬での階層ベイズ。縮小の考え方が共通。
- [Baker 2020](./2020-baker-order-statistics-ranking.md): 順序統計量に基づく別の順位モデル。

## 検索語

Plackett-Luce, プラケット・ルース, ベイズ推論, 期待値伝播, Power EP, メッセージ伝播, 因子グラフ, gamma 事前分布, 共役事前分布, Gumbel 分布, Thurstone モデル, 選択公理, 部分順位, 不完全な順位, 上位 S 位, 過学習, 縮小推定, 順位集約, NASCAR, MovieLens, ranking model, expectation propagation, alpha-divergence, Bayesian ranking, rank aggregation, partial ranking, top-k ranking, MM algorithm, Hunter 2004, Yellott, Luce choice axiom

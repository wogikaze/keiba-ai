---
title: A Comparison Between Two Models for Predicting Ordering Probabilities in Multiple-Entry Competitions
authors: Lo Victor S. Y., Bacon-Shone John
year: 1994
venue: Journal of the Royal Statistical Society Series D (The Statistician) 43(2) 317-327
url: http://hdl.handle.net/10722/60981
doi: 10.2307/2348347
topic: probability-models
tags: harville-formula, henery-model, ordering-probability, model-comparison, hong-kong
verified: fulltext
importance: medium
source: downloaded
source_version: working-paper
---

# Harville と Henery の着順確率モデルを香港の600レースで比べる

> **原本について。** 取得できたのは JRSS D 掲載版ではなく、その元になった香港大学統計学科の Research Report No.17（1992年6月、本文17ページ。HKU Scholars Hub 10722/60981 の PDF を Internet Archive 経由で取得）。スキャン PDF を機械 OCR した。掲載版（1994）と表の数値や節構成が違う可能性がある。以下のページ番号は報告書に印刷された番号で、PDF のページは印刷番号＋2。

> 一言で: 単勝の票数比から2着以下の条件付き確率を作る Harville（指数分布）と Henery（正規分布）を、「モデル確率の logit に係数を掛ける」条件付きロジットで評価した。Harville の係数は着順が下がるほど 0.86 → 0.24 と単調に縮み、系統的な偏りがある。Henery の係数はほぼ 1 で偏りが小さい。ただし係数を推定した Harville は、尤度で Henery を上回っていた。

## 2つのモデル

- **Harville (1973)**: $\pi_{ij}=\pi_i\pi_j/(1-\pi_i)$。走破時間が独立な指数分布なら厳密にこの式になる (p.2–3)。Luce & Suppes (1965) の順位モデル、Plackett (1975) と同じ。Hausch, Ziemba & Rubinstein (1981) が「Silky Sullivan 問題（勝つか着外かの馬）で2・3着確率を過大評価する」と指摘したことに触れる (p.3)。
- **Henery (1981)**: $T_i\sim N(\theta_i,1)$ を独立に仮定。着順確率は多重積分で閉じた形がない。Henery の近似式 $P[T_i\text{ が最小}]\approx\Phi\{z+\theta_i\mu_{1:n}/((n-1)\phi(z))\}$, $z=\Phi^{-1}(1/n)$ を使い、単勝確率から $\theta_i$ を逆算する (p.4, 式(2))。$\mu_{i:n}$ は標準正規の順序統計量の期待値。和が1になるよう事後にスケーリングする。
- 両者は Stern (1990) のガンマ走破時間モデル（形状パラメータ固定）の両端とみなせる (p.4)。

## 評価の方法

前作 Bacon-Shone, Lo & Busche (1992a) の「定数 β モデル」$\ln(\pi_i/\pi_k)=\beta\ln(P_i/P_k)$（$P$ は単勝の票数比）を条件付き確率に広げる (p.5)。

$$\mathrm{logit}\,\pi_{j|i}=\mu\,\mathrm{logit}\,P_{j|i},\quad \mathrm{logit}\,\pi_{k|ij}=\omega\,\mathrm{logit}\,P_{k|ij},\ \ldots$$

右辺の $P$ に Harville または Henery が出す条件付き確率を入れ、係数を最尤推定する（logit は多項）。モデルが正しければ係数は 1 になる。$q$ 着目の条件付き確率（上位 $q-1$ 頭が決まったときに残りの中で最先着する確率）を $q=2,\dots,7$ で別々に推定する。Henery の条件付き確率は Henery の近似を拡張した式 (4) で計算 (p.6)。

## データ

香港（Royal Hong Kong Jockey Club, 1981–89）の **8頭立て 600 レース** (p.6)。入力は単勝の票数比。券種は単勝のみで、連勝式の配当は使っていない。

## 結果

係数と対数尤度（$l(1)$: 係数を1に固定、$l(\text{est})$: 係数を推定）。p.6 Table 1、p.7 Table 2 から。

| q | Harville 係数 | Harville $l(1)$ | Harville $l(\text{est})$ | Henery 係数 | Henery $l(1)$ | Henery $l(\text{est})$ |
|---|---|---|---|---|---|---|
| 2 | 0.8551 | −1055.22 | −1052.60 | 1.1358 | −1061.47 | −1060.11 |
| 3 | 0.6675 | −1015.53 | −1000.77 | 1.1002 | −1007.18 | −1006.65 |
| 4 | 0.5271 | −949.34 | −917.85 | 1.0372 | −921.83 | −921.78 |
| 5 | 0.4480 | −827.77 | −791.94 | 1.1747 | −793.04 | −792.21 |
| 6 | 0.3616 | −689.49 | −639.83 | 0.9681 | −641.77 | −641.75 |
| 7 | 0.2369 | −463.94 | −409.33 | 0.7134 | −411.29 | −410.45 |

読み取れること:

1. Harville の係数は $q$ とともに滑らかに下がる。下の着順ほど Harville の確率の差が大きすぎ、縮める必要がある (p.7)。
2. Henery の係数は $q=7$ を除き 1 に近い (p.9)。
3. 係数を 1 に固定した尤度では、$q\ge3$ で Henery が大きく勝つ（差は $q=7$ で約 53。Figure 1）。**$q=2$（2着）だけは Harville の方が良い**（−1055.22 対 −1061.47）。
4. **係数を推定すると、すべての $q$ で Harville の方が尤度が高い。** 著者も「Harville に推定した係数を付けたものよりは良くない」と書く (p.9)。非入れ子モデルの尤度の直接比較は素朴だと認め、Cox 検定は Bacon-Shone ら (1992b) に譲る。

## 理論的な結果

Henery モデルが真のとき、Harville の条件付き確率 $\pi_j/(1-\pi_i)$ と真の $\pi_{j|i}$ の差を調べる (p.9–12)。Gutmann & Maymin (1987) の不等式を補題に使い、次を示した（Theorem 1）。

- 残りの中で最も強い馬 $a$ について、Harville は2着の条件付き確率を**過大評価**する。
- 最も弱い馬 $b$ について**過小評価**する。
- 中間の馬は $\theta$ の組合せ次第で符号が変わる（$n>3$ では端の馬についてしか示せていない）。

これは Silky Sullivan 効果の説明になりうると著者は述べる (p.12)。

> the Harville model will overestimate the conditional probability of the most favourite horse finishing second and underestimate the conditional probability of the longshot finishing second (p.12)

## 二次資料による旧ノートとの違い

- 旧ノートは「Henery の当てはまりが明らかに良い」と要約していた。原本（報告書版）では、それが成り立つのは係数を 1 に固定したときだけである。係数を推定すれば Harville が尤度で上回り、$q=2$ は固定でも Harville が上だった。結論の「Henery の方が信頼できる」は、係数が 1 に近い（偏りがない）ことに基づく。
- 旧ノートで未確認としていたデータは「香港の8頭立て600レース（1981–89）」と確認できた。
- 掲載版（1994）でデータや表が増えたかは未確認。

## 批判的に読む

- **8頭立てだけ**: 頭数を揃えて $\mu_{i:n}$ を固定するための選択だろうが、JRA の 16〜18 頭立てに外挿できるかは分からない。Harville の偏りは頭数が多いほど大きくなる可能性がある（推測）。
- **入力は市場の票数比そのもの**: 単勝の人気-大穴バイアスを補正しないまま条件付き確率を作っている。$q=2$ の Henery の係数 1.14 などには、単勝段階の偏りが混ざっている可能性がある。
- **評価は尤度と係数だけ**: 回収率、較正表はない。[Ali 1998](./1998-ali-probability-models-outcomes.md) は、このやり方では人気馬の偏りが見落とされると反論した。
- **$q$ ごとに別の係数**: 実務で使うときは段ごとに係数を持つことになる。これは後の割引 Harville（$\pi^{\lambda}$）と同じ発想である。

## keiba-ai での使い方

- **段ごとの温度パラメータ**: 本論文の表は「Harville の $q$ 段目の確率を $\mathrm{softmax}(\mu_q\log P)$ に置き換え、$\mu_q$ を段ごとに推定する」ことの実証である。keiba-ai の Plackett-Luce 系出力で、2着・3着段の温度を別に学習する実験の根拠になる。
- **仮説**: JRA データでも $\mu_2>\mu_3>\cdots$ と単調に下がり、温度付き Harville が尤度で Henery 近似を上回る。比べる指標は (1) 着順の対数尤度、(2) 人気順別の較正表、(3) ワイド・馬連・3連複の回収率。
- **頭数依存**: JRA は頭数の幅が広いので、$\mu_q$ を頭数で条件付けるか、$q/n$ の関数にするかを比べる。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md), [Henery 1981](./1981-henery-permutation-probabilities.md): 比較した2モデル。
- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): Harville と同じ順位モデル。
- [Stern 1990](./1990-stern-gamma-permutations.md): 両者を両端に含むガンマモデル。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 尤度だけでは偏りを見落とすと反論。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 同じ著者による賭けへの応用。
- [Lo 1994](./1994-lo-running-time-japan.md): 日本のデータへの適用。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): 割引近似。本論文の「係数付き Harville」の延長。
- [Lo & Bacon-Shone 2008 (JQAS)](./2008-lo-probability-statistical-models-racing.md): 本論文を含むサーベイ。
- [Benter 1994/2019](./2019-benter-model.md): 段ごとの割引係数を実務で使った例。
- [Deza ら 2017](./2017-deza-exotic-wagering-losses.md): 割引近似を4連単に使用。

## 検索語

Harville モデル, Henery モデル, 着順確率, ordering probability, 順位確率, ranking probability, 条件付き確率, conditional logit, 多項ロジット, モデル比較, model comparison, 正規順位モデル, 指数分布, 走破時間分布, running time distribution, 尤度比較, Cox 検定, 香港競馬, Hong Kong, 8頭立て, Silky Sullivan, 割引モデル, discount model, 温度パラメータ, 2着確率, 3着確率, 人気馬の偏り, favourite bias, Lo Bacon-Shone, research report

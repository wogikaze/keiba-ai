---
title: Assigning Probabilities to the Outcomes of Multi-Entry Competitions
authors: Harville David A.
year: 1973
venue: Journal of the American Statistical Association 68(342) 312-316
url: https://www.tandfonline.com/doi/abs/10.1080/01621459.1973.10482425
doi: 10.1080/01621459.1973.10482425
topic: probability-models
tags: harville-formula, ordering-probability, exotic-bets, conditional-independence
verified: abstract
importance: high
source: unavailable
---

# 単勝確率だけから全着順の確率を作る Harville 公式

> **原本未取得。** JASA の有料論文で、合法な無料版が見つからなかった。本ノートは要旨と、本論文を詳しく扱う後続論文（Henery 1981、Ali 1998、Benter 1994、Snowberg & Wolfers 2010、Hunter 2004。いずれも library に原本あり）に基づく。

> 一言で: 「1着が決まった後、残りの馬の中で2着になる確率は、残りの馬の勝率を比例配分したものに等しい」という仮定で、勝率 $p_i$ だけから任意の着順の確率を計算する式を与えた。馬単・3連単・複勝の確率計算の標準ベンチマークになったが、後続研究はこの式が人気馬の2・3着確率を過大評価することを繰り返し示している。

## 公式

勝率 $p_1,\dots,p_n$（$\sum p_i=1$）が与えられたとき、馬 $i, j, k$ がこの順で1〜3着になる確率は

$P(i,j,k)=p_i\cdot\dfrac{p_j}{1-p_i}\cdot\dfrac{p_k}{1-p_i-p_j}$

2着条件付き確率は $p_{j|i}=p_j/(1-p_i)$。馬 $i$ が2着になる確率は $\sum_{h\ne i}p_h\,p_i/(1-p_h)$。

- 走破時間が独立な指数分布（あるいは Gumbel 分布）に従うと仮定したときの順序統計量モデルと一致する（[Henery 1981](./1981-henery-permutation-probabilities.md), p.89; [Ali 1998](./1998-ali-probability-models-outcomes.md), p.223）。
- Luce の選択公理に基づく Plackett-Luce モデルを、勝率をそのまま強さ $\gamma_i=p_i$ として使ったものと同じ（[Hunter 2004](./2004-hunter-mm-bradley-terry.md), p.396–397）。
- 同じ公式は Plackett (1975) も独立に提示し、ポーカーでは Independent Chip Model（Malmuth–Harville）として知られる。

Henery (1981) は、この解は確率が頭数に依存しないという「おそらく非現実的な」性質を持つと指摘した (Henery p.86)。

## 原論文の実証（孫引き）

Ali (1998) によれば、Harville 自身が 335 レース（サラブレッド）を分析し、2・3着になる確率が高い馬ではこの式が過大評価、それ以外では過小評価になる傾向を報告した (Ali p.221–222)。データの競馬場・期間、要旨に書かれた具体的な応用（複勝・3着内馬券の評価など）は**未確認**。

## 後続研究が示した偏り

| 研究 | データ | 結果 |
|---|---|---|
| Ali (1998) | NY ハーネス 15,402 レース（8頭立て） | 1番人気の2着確率: Harville 0.256 vs 実際 0.192（20.2 SE）。3着: 0.178 vs 0.129 (p.227–228) |
| Benter (1994) | 香港 3,198 レース | 2・3着で低確率馬は予測より多く、高確率馬は少なく2・3着に入る。3着の方が偏りが大きい（PDF p.10–11） |
| Snowberg & Wolfers (2010) | 米国の大規模データ | Harville は2着予測として非常に有用だが、1着馬と2着馬のオッズの非線形効果を入れると明確に改善する（PDF p.17） |

**Benter の補正**（Lo, Bacon-Shone & Busche 型の割引）: 2着の計算では勝率を $p_i^{\gamma}$、3着では $p_i^{\delta}$ に置き換えて正規化してから Harville 式を使う。香港データの最尤推定値は $\gamma=0.81$、$\delta=0.65$ で、これで偏りがほぼ消えた（Benter PDF p.11–12, Tables 11–12）。Benter はこの値は普遍的な定数ではなく、競馬場ごとに違うと注意している。

## 批判的に読む

- **条件付き独立の仮定**: 1着馬が決まると、残りの馬の相対的な強さはそのまま、という仮定。実際には2・3着争いは1着争いよりランダム性が大きい（Benter の説明）。勝率の差が2・3着では縮む。
- **入力の勝率の質に依存**: 市場の単勝オッズを勝率に使う場合、単勝自体の人気-大穴バイアスと、Harville 式の偏りが重なる。どちらの偏りかを分けて評価する必要がある。
- **原論文の標本は小さい**: 335 レースでの偏りの報告（孫引き）は、その後の大規模検証で確認された。

## keiba-ai での使い方

- **必ず実装するベースライン**: 馬連・馬単・ワイド・3連複・3連単の確率を単勝確率から作るときの最初の式。実装は軽く、Plackett-Luce のサンプリングでも同じ分布になる。
- **補正の実験（仮説）**: 「JRA でも Harville は人気馬の2・3着を過大評価し、Benter 型の指数補正 $(\gamma,\delta)$ で対数損失が下がる」。学習期間で $\gamma,\delta$ を最尤推定し、評価期間でワイド・3連複の確率の対数損失と人気順別の較正表を比べる。比較対象は Henery 近似、Stern（ガンマ $r=2$）、Lo & Bacon-Shone の割引モデル。
- **期待値計算の誤差**: 3連単は Harville の偏りが積で効くため、人気薄を含む組み合わせの期待値を過小評価しやすい。回収率のシミュレーションでは、補正の有無で買い目がどう変わるかを記録する。

## 関連ノート

- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 同じ公式を順列データの一般モデルとして提示。
- [Luce 1959](./1959-luce-individual-choice-behavior.md): 理論的な基礎（選択公理）。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規分布版の代替モデル。
- [Stern 1990](./1990-stern-gamma-permutations.md): ガンマ分布で一般化（$r=1$ が Harville）。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 大規模データで偏りを確認。
- [Hausch, Ziemba & Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): Harville で複勝・3着内の割安を探した戦略。
- [Hausch, Lo & Ziemba 1994](./1994-hausch-pricing-exotic-wagers.md): 連勝式の価格付けでの比較。
- [Benter 1994](./2019-benter-model.md): 指数補正を提案。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): 条件付き独立の検定。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): 割引 Harville 型の近似。

## 検索語

Harville 公式, Harville formula, ハービル, 着順確率, ordering probability, 条件付き独立, conditional independence, 馬単, 馬連, 3連単, 3連複, ワイド, exacta, quinella, trifecta, 複勝, place, show, Plackett-Luce, 指数分布, exponential, Gumbel, Independent Chip Model, ICM, Malmuth-Harville, 割引モデル, discount model, Benter 補正

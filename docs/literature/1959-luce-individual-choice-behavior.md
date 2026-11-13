---
title: Individual Choice Behavior: A Theoretical Analysis
authors: Luce R. Duncan
year: 1959
venue: Wiley (book)
url: https://search.worldcat.org/title/190041
doi:
topic: probability-models
tags: luce-choice-axiom, plackett-luce, choice-model
verified: metadata
importance: medium
source: unavailable
---

# Luce の選択公理：Plackett-Luce と多項ロジットの理論的な出発点

> **原本未取得。** 書籍（New York: Wiley / London: Chapman & Hall, 1959, xii+153 p.、Dover 再版あり）で、合法な無料の全文が見つからなかった。本ノートは書誌情報と、公理を正確に引用する後続論文（Hunter 2004、Guiver & Snelson 2009、Ali 1998。いずれも library に原本あり）に基づく。本書固有の章立て・議論は未確認。

> 一言で: 「選択肢の集合 $B$ から $i$ が選ばれる確率は、部分集合 $A$ を経由して選んだ場合の確率の積に分解できる」という選択公理を置くと、各選択肢に正の重み $\gamma_i$ が存在して選択確率が $\gamma_i/\sum_{j\in B}\gamma_j$ になることを示した。これを「1着を選び、残りから2着を選ぶ…」と繰り返したものが Plackett-Luce モデルであり、競馬の Harville 公式と条件付きロジット（softmax）の共通の土台になる。

## 選択公理

Hunter (2004) の記法で書くと、選択肢のどの2つの組でも互いに勝つ確率が正であるとき、任意の $i\in A\subset B$ について

$P_B(i\text{ が選ばれる})=P_A(i\text{ が選ばれる})\cdot P_B(A\text{ のどれかが選ばれる})$

これは次と同値である（[Hunter 2004](./2004-hunter-mm-bradley-terry.md), p.397, 式28–29）。

$P_B(i\text{ が選ばれる})=\gamma_i/\sum_{j\in B}\gamma_j$

帰結として、2つの選択肢の確率の比 $\gamma_i/\gamma_j$ は、他にどんな選択肢があっても変わらない。計量経済学でいう IIA（無関係な選択肢からの独立性）である。

## 競馬モデルとのつながり

| つながり | 内容 | 出典 |
|---|---|---|
| Plackett-Luce | 選択公理に従う選択を「勝者を選ぶ→残りから次を選ぶ」と繰り返すと、着順の分布 $\prod_k \gamma_{\pi(k)}/\sum_{l\ge k}\gamma_{\pi(l)}$ になる。逆も成り立つ | Hunter p.397 |
| 順序統計量 | 独立な Gumbel 分布の得点（指数分布の走破時間）の並び順と一致。位置だけが違う独立な分布でこれが成り立つのは Gumbel のときだけ（Yellott 1977） | Guiver PDF p.2 |
| 走破時間モデル | Luce モデルは確率変数が Gumbel 分布の順位モデル。Plackett (1975) のロジスティック体系の1次モデルでもある | [Ali 1998](./1998-ali-probability-models-outcomes.md), p.222 |
| 条件付きロジット | $\gamma_i=\exp(\beta^\top x_i)$ とおけば McFadden の条件付きロジット＝レース内 softmax | 一般的な対応 |

## 批判的に読む（競馬への含意）

- **IIA は2・3着争いで崩れる**: 1着馬を除いて勝率を比例配分する Harville 公式は、IIA をそのまま着順に適用したもの。実データでは人気馬の2・3着確率が過大になる（Ali 1998、Benter 1994）。原因の一つは、上位争いと下位争いでランダム性（ノイズの大きさ）が違うことで、単一の $\gamma$ では表せない。
- **似た選択肢の問題**: IIA は、似た選択肢（同じ脚質の馬、同厩舎の馬）が同時にいると不自然な予測をする（古典的な「赤バス・青バス」問題）。展開（ペース）の影響が大きいレースでは、馬どうしの相関を入れたモデル（多変量正規＝Thurstone 型、ネステッドロジット）の方が自然かもしれない。これは推測で、本書での議論は未確認。
- 本書は心理学的な選択理論の書籍で、競馬の実証は含まないと思われる（未確認）。

## keiba-ai での使い方

- **モデル設計の前提を明示する**: レース内 softmax で勝率を出し、Harville で連勝式の確率を作るパイプラインは、Luce の公理を2回使っている。どちらで崩れているかを分けて検証する。
- **実験案（仮説）**: 「同じ softmax のスコアでも、2着・3着を選ぶ段階では温度を上げる（$\gamma_i^{\alpha}$, $\alpha<1$）方が着順の対数尤度が高い」。段階ごとの温度 $\alpha_2,\alpha_3$ を推定し、1 から有意に離れるかを見る。
- **相関のある馬**: 同厩舎・同馬主の複数出走、同じ脚質の馬が多いレースで Harville の誤差が大きいかを層別に調べる。

## 関連ノート

- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 公理を着順に広げた Plackett-Luce の出典。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 公理を競馬の着順確率に適用した式。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 公理と Plackett-Luce の同値性の証明と推定法。
- [Guiver & Snelson 2009](./2009-guiver-bayesian-plackett-luce.md): Plackett-Luce のベイズ推定と解釈。
- [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md): 公理に基づく多項ロジットを競馬に使った。
- [Henery 1981](./1981-henery-permutation-probabilities.md): IIA を持たない正規分布版の代替。
- [Cotton 2021](./2021-cotton-relative-ability-winning-probability.md): 能力と勝率の関係のモデル。Luce の公理を Harville の言い換えとして扱う。

## 検索語

Luce の選択公理, Luce's choice axiom, 選択公理, choice axiom, IIA, 無関係な選択肢からの独立性, independence of irrelevant alternatives, Bradley-Terry-Luce, BTL, Plackett-Luce, 多項ロジット, multinomial logit, 条件付きロジット, softmax, 離散選択, discrete choice, Gumbel, 心理物理学, 効用, Individual Choice Behavior

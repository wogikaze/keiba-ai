---
title: A Comparison Between Two Models for Predicting Ordering Probabilities in Multiple-Entry Competitions
authors: Lo Victor S. Y., Bacon-Shone John
year: 1994
venue: Journal of the Royal Statistical Society Series D (The Statistician) 43(2) 317-327
url: https://www.researchgate.net/publication/277036201_An_approximation_to_ordering_probabilities_of_multi-entry_competitions
doi: 10.2307/2348347
topic: probability-models
tags: harville-formula, henery-model, ordering-probability, model-comparison
verified: abstract
importance: medium
source: unavailable
---

# Harville と Henery の着順確率モデルを実データで比べる

> **原本未取得。** JRSS D の有料論文。HKU の機関リポジトリ（hdl 10722/60981, 86405）に記録はあるが取得できず、合法な無料版が見つからなかった。本ノートは要旨の断片と、本論文を引用する後続論文（Ali 1998、Deza ら 2017。いずれも library に原本あり）に基づく。

> 一言で: 単勝確率から2着・3着の確率を作る2つのモデル、簡便な Harville（指数分布）と Henery（正規分布）を、各モデルの確率を説明変数にしたロジスティックモデルの当てはまりで比較した。Harville には人気馬に偏った系統的な誤差があり、Henery の方が明らかに当てはまりが良いと報告した。

## 何を比べたか

- Harville (1973): 走破時間を独立な指数分布とみなす。単勝確率 $\pi_i$ から $\pi_{ij}=\pi_i\pi_j/(1-\pi_i)$ のように閉じた式で計算できる。
- Henery (1981): 走破時間を独立な正規分布 $N(\theta_i,1)$ とみなす。閉じた式がなく数値積分か近似が必要。
- 比較の方法: 各モデルが出す着順確率を説明変数とするロジスティック（多項ロジット）モデルを当てはめ、尤度で比べた（[Ali 1998](./1998-ali-probability-models-outcomes.md), p.222 の要約）。前段の Bacon-Shone, Lo & Busche (1992, 香港大学の研究報告) は、香港と米国 Meadowlands のデータで Harville、Henery、複数の Stern モデルを同じ方法で比べ、Henery が最良だった (Ali p.222)。

## 結果（孫引き）

- Harville は着順確率の推定に系統的な偏りがあり、人気馬に寄る（[Deza ら 2017](./2017-deza-exotic-wagering-losses.md), PDF p.6 は、Harville 型の式は人気馬に偏ることが Lo (2008) と本論文で見つかったと書く）。
- Henery の当てはまりが明らかに良い（Lo & Bacon-Shone 2008 による要約、検索結果経由）。
- データの範囲（香港のみか、他の競馬場を含むか）、レース数、尤度の値は**未確認**。

## 反論と限界

Ali (1998) は、15,402 レースで「平均の予測確率」と「実際の頻度」を人気順に比べ、最良の正規モデルでも1番人気の2・3着確率を 5.7〜6.8 SE 過大評価することを示した。そして、尤度比較だけで Henery を十分と結論した Bacon-Shone ら (1992) と本論文に対し、偏りは残ると反論した (Ali p.226–227)。尤度が高いことと、確率が較正されていることは別の問題である。

## 後の展開

Henery は計算が重いため、同じ著者は後に、Harville 式の各段で単勝確率を $\pi^{\lambda}$ に割り引く簡単な近似（discount モデル）を提案した。Deza ら (2017) はこれを
$\pi_{ijkl}=\pi_i\cdot\pi_j^{\lambda_1}/\sum_{s\ne i}\pi_s^{\lambda_1}\cdot\pi_k^{\lambda_2}/\sum_{s\ne i,j}\pi_s^{\lambda_2}\cdots$
の形で使い、$\lambda$ を過去のレースから多項ロジットで推定している (Deza PDF p.6)。Benter (1994) の補正 $(\gamma,\delta)=(0.81,0.65)$ も同じ形。

## 批判的に読む

- **評価は尤度のみ（とされる）**: 較正（人気順ごとの予測と実際）や、馬券の回収率への影響は本論文の範囲外だった可能性が高い（未確認）。
- **入力の単勝確率**: 市場オッズをそのまま勝率に使うと、単勝自体の人気-大穴バイアスが2・3着の比較に混ざる。どう補正したかは未確認。

## keiba-ai での使い方

- **再現実験**: JRA の単勝確率（市場とモデルの両方）から、Harville / Henery 近似 / 割引 Harville（$\lambda$ を推定）で各馬の2着・3着確率を作り、(1) 着順の対数尤度、(2) 人気順別の較正表（Ali 型）、(3) ワイド・3連複の回収率シミュレーション、の3つで比べる。本論文と Ali の対立は (1) と (2) の違いなので、両方を見る。
- **仮説**: 「尤度では Henery ≒ 割引 Harville > Harville になるが、較正では割引 Harville の方が人気馬の偏りを消せる（段ごとに $\lambda$ を変えられるため）」。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md), [Henery 1981](./1981-henery-permutation-probabilities.md): 比較した2モデル。
- [Stern 1990](./1990-stern-gamma-permutations.md): 両者をつなぐガンマモデル。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 正規モデルでも偏りが残ると反論。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 同じ著者による賭けへの応用。
- [Lo 1994](./1994-lo-running-time-japan.md): 日本のデータへの適用。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): 割引近似。
- [Lo & Bacon-Shone 2008 (JQAS)](./2008-lo-probability-statistical-models-racing.md): 本論文を含むサーベイ。
- [Deza ら 2017](./2017-deza-exotic-wagering-losses.md): 割引近似を4連単に使用。

## 検索語

Harville モデル, Henery モデル, 着順確率, ordering probability, 順位確率, ranking probability, モデル比較, model comparison, 正規順位モデル, 指数分布, ロジスティック回帰, 尤度比較, 香港競馬, Hong Kong, 割引モデル, discount model, 2着確率, 3着確率, 人気馬の偏り, favourite bias, Lo Bacon-Shone

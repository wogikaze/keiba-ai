---
title: Approximating the Ordering Probabilities of Multi-Entry Competitions by a Simple Method
authors: Lo Victor S. Y., Bacon-Shone John
year: 2008
venue: Handbook of Sports and Lottery Markets (Hausch, Ziemba eds.), Elsevier, pp. 51-65
url: https://doi.org/10.1016/B978-044450744-0.50007-X
doi: 10.1016/B978-044450744-0.50007-X
topic: probability-models
tags: discount-model, harville-formula, henery-model, stern-model, ordering-probability, exotic-bets
verified: metadata
importance: high
source: unavailable
source_version: published
---

# 着順確率の簡易近似（discount モデル）：勝率のべき乗を再正規化する

**原本未取得。** Elsevier の書籍章で OA 版がなく、HKU Scholars Hub の登録（10722/64961）にはファイルが無い。1992 年の HKU 統計学科 Research Report 版は ResearchGate にしかなく取得できなかった。本ノートは要旨（HKU Hub の書誌）と、この近似を使った論文の原本（[Deza 2017](./2017-deza-exotic-wagering-losses.md)、[Deza 2015](./2015-deza-chance-constrained-parimutuel.md)）に基づく。ページ番号はそれらの原本のもの。

> 一言で: Harville の公式が「独立な指数分布（極値分布）の走破時間」から導かれることを手がかりに、Henery（正規）や Stern（gamma）の着順確率を「段ごとに勝率を $\lambda$ 乗して再正規化する」だけで近似する方法を示した章（要旨より）。

## 位置づけ

勝率 $\pi_i$ だけから馬単・3連単の確率を作る方法は、次の系譜にある。

1. Harville (1973): 2着は「1着馬を除いたレースの勝者」と見なし $\pi_j/(1-\pi_i)$。計算は簡単だが、本命の2・3着確率を過大に、穴馬を過小に見積もる偏りが知られる（Lo と Bacon-Shone の 1994 年の比較、[Lo 1994](./1994-lo-comparison-harville-henery.md)）。
2. Henery (1981) は走破時間を正規、Stern (1990) は gamma と仮定する。当てはまりは良いが、着順確率の計算に数値積分が要り、実用には重い。
3. 本章の discount モデルは 2 の当てはまりを 1 の計算量で得ようとする。

要旨（HKU Hub の書誌に載る文）によれば、Harville のモデルは走破時間が独立な指数分布あるいは極値分布であることに対応し、この理論結果が Henery・Stern モデルの近似の動機になった。

## 式

Deza らの引用形（4着まで）(Deza 2017, p.6; Deza 2015, p.4):

$$\pi_{ijkl}=\pi_i\cdot\frac{\pi_j^{\lambda_1}}{\sum_{s\ne i}\pi_s^{\lambda_1}}\cdot\frac{\pi_k^{\lambda_2}}{\sum_{s\ne i,j}\pi_s^{\lambda_2}}\cdot\frac{\pi_l^{\lambda_3}}{\sum_{s\ne i,j,k}\pi_s^{\lambda_3}}$$

- $\pi_i$: 勝率（オッズから作った市場確率でもモデル確率でもよい）。
- $\lambda_m$: $m+1$ 着を決める段の「割引」指数。$\lambda=1$ で Harville に一致する。$\lambda<1$ なら勝率の差が縮み、下位の着順ほどランダムに近づく。
- 各段は $\log\pi$ を唯一の説明変数とする条件付きロジットと同じ形なので、対数尤度は段ごとに分離でき、$\lambda$ は段ごとに個別に推定できる (Deza 2017, p.6)。

レビュー論文 [Lo 2008](./2008-lo-probability-statistical-models-racing.md) では3着までの形で $\lambda$ と $\tau$ の2パラメータとして書かれている（検索結果での引用。原本未確認）。

## 推定値の例（他論文）

本章自身の推定値・データは未確認。旧報告書版は香港・米国・日本のデータを使ったとされるが、これも未確認。
本章の近似を使った Deza ら（カナダ繋駕速歩、約 800 レース）の推定値は次のとおり (Deza 2017, p.15, Table 4)。

| $\lambda_1$ | $\lambda_2$ | $\lambda_3$ |
|---|---|---|
| 0.601 | 0.385 | 0.262 |

着順が下がるほど $\lambda$ が小さく、Harville から大きく離れる。Benter (1994) が勝率確率の指数で2着・3着を補正したのも同じ形である（[Benter 2019](./2019-benter-model.md)）。

## 批判的に読む（原本未取得のため限定的）

- 近似の精度（Henery・Stern の厳密計算との差）を何で測ったか、どのデータで検証したかは未確認。
- $\lambda$ がレースの頭数や勝率の分布に依存するかは、この式の形からは扱えない。頭数別に推定し直す必要があるかは実データで確かめる。
- 段ごとの独立推定は簡単だが、2着の予測に1着の情報（どの馬が勝ったか）以外を使わない、という制約は残る。

## keiba-ai での使い方

- **3連単・馬単の確率の第一候補**: 勝率モデルの出力 $\pi$ に対して、$\lambda_1,\lambda_2$ を学習期間で推定するだけでよい。実装は `log(pi)` を1変数とする段ごとの条件付きロジット。
- **仮説 H1**: JRA の3連単で、$\lambda$ を推定した discount モデルは Harville より的中組の対数尤度が高く、改善の大部分は $\lambda_2$（3着）から来る。
- **仮説 H2**: $\lambda$ は芝・ダート、頭数、クラスで異なる。条件別に推定して対数尤度が改善するか確かめる。
- 比較対象は Harville、Henery（正規、数値積分）、Plackett–Luce を直接学習したモデル。評価指標は3連単・馬単の負の対数尤度と、組み合わせ確率の校正。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): $\lambda=1$ の特殊ケース。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規走破時間モデル。近似の対象。
- [Stern 1990](./1990-stern-gamma-permutations.md): gamma 走破時間モデル。近似の対象。
- [Lo 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較。本章の前段。
- [Lo 1995](./1995-lo-ranking-probability-betting.md): 着順確率モデルを賭けに使った実証。
- [Lo 2008](./2008-lo-probability-statistical-models-racing.md): 同じ著者のレビュー。本章の近似を要約。
- [Deza 2017](./2017-deza-exotic-wagering-losses.md): 本近似で4連単確率を作り $\lambda$ を推定した応用。
- [Benter 2019](./2019-benter-model.md): 2・3着の確率を指数で補正した実務版。

## 検索語

着順確率, 順序確率, 3連単確率, 馬単確率, discount モデル, 割引モデル, べき乗補正, Harville 公式, Harville 補正, Henery モデル, Stern モデル, 走破時間分布, 指数分布, 極値分布, gamma 分布, ordering probability, discount model, power-law adjustment, Harville formula, Henery model, Stern model, exacta, trifecta, superfecta, multi-entry competition, Lo Bacon-Shone

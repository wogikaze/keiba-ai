---
title: Approximating the Ordering Probabilities of Multi-Entry Competitions by a Simple Method
authors: Lo Victor S. Y., Bacon-Shone John
year: 2008
venue: Handbook of Sports and Lottery Markets (Hausch, Ziemba eds.), Elsevier, pp. 51-65
url: https://doi.org/10.1016/B978-044450744-0.50007-X
doi: 10.1016/B978-044450744-0.50007-X
topic: probability-models
tags: discount-model, harville-formula, henery-model, stern-model, ordering-probability, exotic-bets, japan
verified: fulltext
importance: high
source: downloaded
source_version: working-paper
---

# 着順確率の簡易近似（discount モデル）：勝率のべき乗を再正規化する

> **原本について。** 取得できたのは 2008 年の書籍章ではなく、その元になった香港大学統計学科 Research Report No.16「An approximation to ordering probabilities of multi-entry competitions」（1992年6月、本文16ページ。HKU Scholars Hub 10722/60982 の PDF を Internet Archive 経由で取得）。書籍章（2008）で数値や節が改訂された可能性がある。ページ番号は報告書に印刷された番号（PDF のページは印刷番号＋1）。

> 一言で: Henery（正規）モデルの着順確率は「勝率を 0.76 乗して再正規化（2着）、0.62 乗して再正規化（3着）」でほぼ再現できることを、香港・米国 Meadowlands・日本のデータで示した。日本のデータでは Henery より形状 $r=4$ の Stern（ガンマ）モデルの方が尤度が高く、それも同じ「べき乗＋再正規化」で近似できる。

## 背景

Harville (1973) の式 $\pi_{ij}=\pi_i\pi_j/(1-\pi_i)$ は、走破時間を独立な指数分布とみなすことに等しい (p.2, Dansie 1983)。Henery (1981, 正規) と Stern (1990, 形状 $r$ 固定のガンマ) は、勝率から $\theta$ を逆算するのに非線形方程式を解き、着順確率に数値積分が要る。前作 Bacon-Shone, Lo & Busche (1992b) は、単勝の票数比だけを使ったとき、Meadowlands の馬単、Meadowlands と香港の3連単、香港の馬連で Henery が最良と報告していた (p.2)。

## 着想：対数比がほぼ一定

Henery モデルで計算した確率について
$$\lambda^{Hen}_{ij|l}=\frac{\ln(\hat\pi_{ij}/\hat\pi_{il})}{\ln(\hat\pi_j/\hat\pi_l)}$$
を求めると、馬の組やレースが変わってもほぼ一定になる (p.2–3, 式(2))。一定なら $\pi_{ij}\propto\pi_i\pi_j^{\lambda}$ と書けるので、
$$\pi_{ijk}=\pi_i\cdot\frac{\pi_j^{\lambda}}{\sum_{s\ne i}\pi_s^{\lambda}}\cdot\frac{\pi_k^{\tau}}{\sum_{t\ne i,j}\pi_t^{\tau}}$$
で近似できる（式(6)、「discount model」）。$\pi$ は単勝の票数比。$\lambda=\tau=1$ が Harville。

## 推定された $\lambda$ と $\tau$

上位3頭の組で計算した平均（p.4, Table 1・2）。

| 競馬場 | $\lambda^{Hen}$ 平均 (s.d.) | $\tau^{Hen}$ 平均 (s.d.) |
|---|---|---|
| 香港 (89) | 0.767 (0.024) | 0.652 (0.034) |
| Meadowlands | 0.756 (0.022) | 0.639 (0.043) |
| 日本 | 0.779 (0.034) | 0.661 (0.038) |

- $\lambda$ は最尤推定量の比（Harville 係数 / Henery 係数）でも 0.76 になった (p.3–4)。$\tau$ は同じ方法で 0.62。
- $\tau$ を 0.62 と 0.65 で比べても対数尤度はほぼ同じ（香港 −699.68 対 −700.20、Meadowlands −10667.80 対 −10667.47; p.5, Table 3）。報告書は以後 $\lambda=0.76$, $\tau=0.62$ に固定する。
- **頭数依存**: 頭数が増えると $\lambda,\tau$ はゆっくり上がる (p.5–6, Table 4)。日本のデータでは 5頭立て $\lambda=0.718,\tau=0.560$ から 16頭立て $\lambda=0.797,\tau=0.687$。
- **シミュレーション**: $\theta_i\sim N(\mu_0,\sigma_0^2)$ で10頭立てを生成すると、$\sigma_0$（能力のばらつき）が 0.2〜1.5 のどれでも平均 $\lambda$ は 0.73〜0.77。ばらつきが大きいほど s.d. が増え、近似は粗くなる (p.7, Table 5–7)。

## Henery との比較

尤度（p.9, Table 8）:

| 券種・データ | Harville | Henery | discount |
|---|---|---|---|
| 馬単 Meadowlands 510 R | −1875.77 | −1859.63 | −1859.25 |
| 馬連 香港 4153 R | −13619.28 | −13589.55 | −13586.95 |
| 3連単 Meadowlands 120 R | −711.50 | −699.83 | −699.68 |
| 3連単 香港 1809 R | −10747.98 | −10667.25 | −10667.80 |

厳密な Henery（数値積分）の馬単確率との KL 情報量（Meadowlands 510 R, p.9–10, Table 9）では、discount（$\lambda$ 固定）が 0.000339 と最小。Henery 自身の1次テイラー近似（0.013）や Harville（0.020）よりはるかに近い。計算時間が小さい点も強調される (p.11)。

## Stern モデルと日本のデータ

Stern のガンマモデル（$r=1$ で Harville、$r\to\infty$ で Henery）を、上位3頭の対数尤度で比べた (p.12–13)。

| $r$ | 日本 | 香港 (89) | Meadowlands |
|---|---|---|---|
| 1 (Harville) | −8977.57 | −2523.37 | −2845.93 |
| 2 | −8954.57 | | |
| 3 | −8950.60 | | |
| 4 | **−8950.35** | | |
| 8 | −8953.44 | | |
| 10 / 20 / 30 / 40 | | −2504.55 / −2503.58 / −2503.44 / −2503.72 | −2800.87 / −2798.02 / −2796.90 / −2795.78 |
| ∞ (Henery) | −8986.88 | **−2502.74** | **−2792.94** |

**日本では $r=4$ が最良で、Henery は Harville より悪い。** 香港と Meadowlands では Henery が最良 (p.12–13, Table 10–12)。日本のデータの出所（年、競馬場）は報告書の本文からは読み取れなかった（未確認）。Table 13 によると 1583 レース。

Stern にも同じ近似を使う（式(8)）。日本の 1583 レースで平均した値は $r=4$ で $\lambda_4=0.884$, $\tau_4=0.814$ (p.14, Table 13)。$r$ が大きいほど $\lambda,\tau$ は小さくなり、$r\to\infty$ で 0.76 と 0.62 に近づく。数値積分との KL は Harville の 1/10 以下 (p.15, Table 14)。尤度もほぼ一致する（$r=4$ で −8950.35 対 −8952.00; p.16, Table 15）。

> We have proposed to use the discount model in (8) with different values of $(\lambda_r,\tau_r)$ for different $r$. (p.16)

## 二次資料による旧ノートとの違い

- 旧ノートは Deza ら (2017) の4段の形と推定値（0.601, 0.385, 0.262）から書いていた。原本の報告書版は3着までで、$\lambda,\tau$ は「Henery（または Stern）モデルの確率の対数比の平均」として求める。尤度で直接推定するのは Deza らのやり方で、報告書では補助的（最尤推定量の比）だった。
- 旧ノートで未確認だったデータは、香港・Meadowlands・日本と確認できた。日本では Henery より Stern ($r=4$) が良いことは旧ノートになかった。
- 書籍章（2008）の内容が報告書と同じかは未確認。

## 批判的に読む

- **近似の目標は Henery / Stern の再現**: KL は「Henery が真」という仮定での近さで、実際の着順への当てはまりは Table 8・10・15 の尤度だけ。回収率、較正表はない。
- **入力は票数比**: 単勝の人気-大穴バイアスを補正しないまま使う。$\lambda$ の値は、入力の勝率がどれだけ較正されているかにも依存するはず（推測）。モデル確率を入れる keiba-ai では推定し直す必要がある。
- **尤度は同じデータで評価**: $\lambda=0.76$ は同じデータの平均から決めた。パラメータは2つなので過学習の余地は小さいが、時系列での検証はない。
- **日本のデータの詳細不明**: 年、開催、頭数の分布（Table 4(c) からは 5〜18頭立て）以外は確認できなかった。

## keiba-ai での使い方

- **3連単・馬単の確率の第一候補**: 勝率 $\pi$ に対し、2着段は $\pi^{\lambda}$、3着段は $\pi^{\tau}$ で再正規化する。初期値は日本の $r=4$ に合わせた $(0.88, 0.81)$ か Henery 相当の $(0.76, 0.62)$。学習期間で $\log\pi$ を1変数とする条件付きロジットとして推定し直す。
- **仮説 H1**: JRA の近年データでも、Henery 相当 (0.76, 0.62) より緩い割引（$r=4$ 相当）の方が上位3頭の対数尤度が高い。報告書の日本データ（1990年前後と推測）の結果が今も成り立つかを確かめる。
- **仮説 H2**: $\lambda,\tau$ を頭数の関数にすると尤度が改善する（Table 4 の単調増加）。
- 比較対象は Harville、Henery（数値積分）、Plackett–Luce を直接学習したモデル。指標は3連単・馬単の負の対数尤度、組合せ確率の較正、回収率。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): $\lambda=\tau=1$ の特殊ケース。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規走破時間モデル。近似の対象。
- [Stern 1990](./1990-stern-gamma-permutations.md): ガンマ走破時間モデル。日本で $r=4$ が最良。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): 同時期の報告書。条件付きロジットで Harville の偏りを示した前段。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 着順確率モデルを賭けに使った実証。
- [Lo 1994](./1994-lo-running-time-japan.md): 日本のデータへの適用。
- [Lo & Bacon-Shone 2008 (JQAS)](./2008-lo-probability-statistical-models-racing.md): 同じ著者のレビュー。
- [Deza ら 2017](./2017-deza-exotic-wagering-losses.md): 本近似で4連単確率を作り、段ごとの指数を尤度で推定した応用。
- [Deza ら 2015](./2015-deza-chance-constrained-parimutuel.md): 同じ近似を使う。
- [Benter 2019](./2019-benter-model.md): 2・3着の確率を指数で補正した実務版。

## 検索語

着順確率, 順序確率, 3連単確率, 馬単確率, 馬連確率, discount モデル, 割引モデル, べき乗補正, 再正規化, Harville 公式, Harville 補正, Henery モデル, Stern モデル, ガンマ分布, 形状パラメータ, 走破時間分布, 指数分布, KL 情報量, Kullback-Leibler, ordering probability, discount model, power-law adjustment, Harville formula, Henery model, Stern model, exacta, trifecta, quinella, multi-entry competition, 日本競馬, Japan, 香港, Meadowlands, 頭数, race size, Lo Bacon-Shone, research report

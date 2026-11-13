---
title: Probability and Statistical Models for Racing
authors: Lo Victor S. Y., Bacon-Shone John
year: 2008
venue: Journal of Quantitative Analysis in Sports 4(2) Article 11
url: https://www.degruyter.com/document/doi/10.2202/1559-0410.1103/pdf
doi: 10.2202/1559-0410.1103
topic: probability-models
tags: favourite-longshot-bias, ordering-probability, running-time-distribution, henery-model, correlated-running-times, discount-model
verified: fulltext
importance: high
source: downloaded
source_version: accepted-manuscript
---

# 競馬の確率・統計モデル：各国の本命大穴バイアスと、相関を入れた Henery モデル

> 一言で: 勝率の「べき補正」モデル $\pi_i\propto P_i^\beta$ を米国・日本・香港・上海の9競馬場に当てはめ、本命大穴バイアス（FLB）は米国と日本では有意だが香港・上海では見られないと示した。後半は Henery（正規走破時間）モデルに馬どうしの相関と馬ごとの分散を入れて拡張し、香港 400 レースで「わずかに改善」（6% 水準）を報告する短い論文。

原本は bepress の投稿版（"An Article Submitted to Journal of Quantitative Analysis in Sports, Manuscript 1103"）で、著者が ResearchGate に置いた PDF を Internet Archive（web.archive.org、2025-06-18 のスナップショット）から取得した。本文 14 ページ。以下のページは原本の印刷ページ番号（PDF の 3〜16 枚目が p.1〜14）。出版版との差は未確認。

## 原本で覆った点（旧ノートとの違い）

旧ノートは要旨と断片から「レビュー論文」と推測していたが、原本を読むと次のとおり。

- **レビューではなく、短い実証＋モデル拡張の論文**。FLB の国際比較（Table 1）と、Henery モデルの拡張（Table 2）という2つの新しい結果がある。既存の着順モデルの紹介は第3.1節の2ページだけ (pp.5-7)。
- FLB の分析は「対数線形回帰」ではなく、条件付きロジットと同じ形の **べき補正モデル** (1) で β を推定する (p.3)。
- **日本のデータが含まれる**: 1990 年の 1,607 レースで β=1.07（p=0.01）、有意に FLB あり (p.4, Table 1)。旧ノートで「日本でバイアスが弱いという報告を含むかは未確認」としていた点は、この論文では「日本でも米国と同じ向きのバイアスがある」が答え。
- 走破時間モデルの比較で、Lo (1994b) の日本データでは **Stern の gamma モデル（形状母数 4）が Henery・Harville より良かった** と紹介している (p.7)。香港（Lo and Bacon-Shone 1994）とメドウランズ（Bacon-Shone, Lo and Busche 1992b）では Henery が勝った。
- discount 近似の式 (7) は本文にあるが、λ, τ の値は「Lo and Bacon-Shone (2007) の値」として示されず、この論文では推定していない (p.7)。

## 1. 本命大穴バイアスの国際比較

### モデル

$P_i$ を馬 $i$ の単勝票数シェア（市場の勝率）、$O_i$ を単勝オッズ、$t$ を控除率とすると $P_i=(1-t)/(1+O_i)$。真の勝率 $\pi_i$ を

$$\pi_i=\frac{P_i^{\beta}}{\sum_{j=1}^{n}P_j^{\beta}}\qquad(1)$$

とおき、β を最尤推定する (p.3)。出典は Lo (1994a) と Bacon-Shone, Lo and Busche (1992a)。β>1 なら本命が過小・穴が過大に買われている（FLB）。著者は β>1 を「リスク愛好」、β<1 を「リスク回避」と対応させる。

### 推定結果 (p.4, Table 1)

| 競馬場 | 期間 | レース数 | β | p 値（β≠1） | 平均単勝プール |
| --- | --- | --- | --- | --- | --- |
| Atlantic City（米） | 1983-84 | 712 | 1.10 | 0.08 | 不明 |
| Meadowlands（米） | 1983-84 | 705 | 1.12 | 0.02 | $52K |
| Saratoga（米） | 1970-74 | 9,072 | 1.16 | ~0 | $25K |
| Roosevelt（米） | 1970-74 | 5,806 | 1.13 | ~0 | $218K |
| Yonkers（米） | 1970-74 | 5,369 | 1.13 | ~0 | $228K |
| 日本 | 1990 | 1,607 | 1.07 | 0.01 | $168K |
| Happy Valley（香港） | 1981-89 | 2,212 | 1.04 | 0.25 | $1.1M |
| Shatin（香港） | 1981-89 | 1,943 | 0.94 | 0.04 | $1.1M |
| 上海 | 1923-35 | 730 | 1.03 | 0.38 | 不明 |

米国と日本は β>1 で有意、香港と上海は有意でない（Shatin は 0.94 で逆向きに有意）。著者の仮説は **プールの大きさ**: 香港は単勝プールが桁違いに大きく、期待利益が大きいため Benter (1994) のような本格的な研究者が参加し、オッズが正確になる (p.4)。これは仮説で、検定はしていない。

### 効用による解釈 (p.5)

Ali (1977) と同じく「代表的賭け手はどの馬に賭けても期待効用が等しい」と仮定すると、$U(1+O_i)\propto(1+O_i)^\beta$ というべき関数の効用になり、Arrow–Pratt の絶対リスク回避度は $-(\beta-1)/x$。β>1 なら負で、富が減るほどリスクを取る「リスク愛好」と解釈する (式 2)。

## 2. 走破時間分布による着順確率

### 既存モデルの手順 (pp.5-7)

1. 勝率 $\pi_i$ を票数シェア $P_i$ で推定する。
2. 走破時間の分布 $F(\cdot\mid\theta_i)$ を仮定し、「馬 $i$ が最速になる確率 = $\pi_i$」を満たすように位置母数 $\theta_i$ を解く。
3. その $\theta$ で $\pi_{ij}$、$\pi_{ijk}$ を積分で計算する。

Harville (1973) は指数分布（極値分布）に当たり、$\pi_{ij}=\pi_i\pi_j/(1-\pi_i)$ と閉じた式になる。Henery (1981) の正規分布と Stern (1990) の gamma 分布は数値積分の連立方程式が要り、実用的でない。そこで Lo and Bacon-Shone の近似

$$\pi_{ijk}=\pi_i\,\frac{\pi_j^{\lambda}}{\sum_{s\ne i}\pi_s^{\lambda}}\,\frac{\pi_k^{\tau}}{\sum_{t\ne i,j}\pi_t^{\tau}}\qquad(7)$$

を挙げる。λ=τ=1 で Harville に戻る (p.7)。なお原本では Harville の式番号が (3)(4) と手順の式番号 (3)(4) で重複しており、(7) の説明は「(5) と (6) に戻る」と書かれている。投稿版の誤植と思われる。

### Henery モデルの拡張 (pp.7-9)

全馬に同じ相関 ρ を入れても独立な Henery と同値になるので、次の構造を入れる。

- **非一定の相関**: $\rho_{ij}=\psi_i\psi_j$、$\log\frac{\psi_i}{1-\psi_i}=-\delta-\gamma(\theta_i-\bar\theta)$。γ>0 なら強い馬（$\theta$ が小さい）どうしほど相関が高い (式 8, 9)。
- **非一定の分散**: $\sigma_i=\exp[\kappa(\theta_i-\bar\theta)]$。κ>0 なら弱い馬ほど走破時間のばらつきが大きい (式 10)。
- 実装は共通因子 $U_0$ を使った表現 $(T_i-\theta_i)/\sigma_i=\psi_iU_0+\sqrt{1-\psi_i^2}\,U_i$ (Appendix A, p.11) と、Henery と同じ1次のテイラー近似で $\theta_i$ と上位5頭の順列確率を閉じた式 (11)(12) にする。
- 尤度は **上位5頭の着順** で作る（高次の着順ほど相関・分散の構造が効くと考えるため）(p.7)。

### 結果 (p.9, Table 2)

香港の 8 頭立て 400 レースで、Henery に対する尤度比検定:

| 拡張 | 推定値 | p 値 |
| --- | --- | --- |
| 非一定相関（γ のみ） | γ=0.58 | 0.06 |
| 非一定相関（γ と δ） | γ=0.60, δ=0.05 | 0.18 |
| 非一定分散 | κ=0.08 | 0.06 |

著者は「有望」とするが 5% 水準では有意でない。付録の末尾で、δ=0 のとき近似の上では (9) と (10) が同値になり γ と κ のどちらか一方で足りると述べている (p.12)。賭けの成績での検証は「今後の課題」(p.9)。

## 批判的に読む

- **FLB の推定に時系列の分割や検証がない**: β は全期間をまとめた当てはめで、予測性能や回収率では評価していない。期間もばらばら（上海は 1923-35 年）で、プールの大きさ以外の違い（控除率、券種構成、時代）が交絡している。プール仮説は9点の観察からの推測にすぎない。
- **日本のデータの出所が書かれていない**: 「Japan (90)」1,607 レースとあるだけで、JRA か地方か、どの競馬場かは本文に記載がない（Lo 1994b の日本データと同じかも未確認）。
- **市場確率の算出**: $P_i=(1-t)/(1+O_i)$ は控除率を一律とした計算で、ブレイケージ（端数切り捨て）を無視している。
- **拡張 Henery の検証は小さい**: 400 レース・8頭立てのみ、ホールドアウトなし、p=0.06。回収率での評価なし。
- 投稿版なので、出版版で数値や式番号が直っている可能性がある（未確認）。

## keiba-ai での使い方

- **市場確率のべき補正をベースラインに**: JRA の単勝オッズから $P_i$ を作り、(1) の β を時系列分割の学習期間で推定して検証期間の log loss・キャリブレーションを比べる。仮説: 「JRA の近年データでも β>1（FLB あり）だが、1990 年の 1.07 より 1 に近い」。β は年ごとに推定して推移を見る。
- **着順モデルの比較実験**: Harville（λ=τ=1）、discount 近似 (7) で λ, τ を推定、Stern gamma（日本で形状母数 4 が良かったという Lo 1994b の結果の追試）を、3連単・馬単の対数尤度で比べる。
- **相関のある走破時間**: 強い馬どうしの相関（γ）は、展開（ペース）で上位人気がまとめて崩れる現象のモデル化に当たる。Plackett–Luce に共通因子（レースごとのランダム効果）を入れる実験の動機になる。ただし原本の証拠は弱い（p=0.06）。
- **評価の注意**: 本論文の FLB 推定は当てはめのみ。keiba-ai では必ず時系列分割で β を固定してから検証期間で評価し、控除率込みの回収率も出す。

## 関連ノート

- [Lo 2008（近似の章）](./2008-lo-ordering-probabilities-approximation.md): 式 (7) の discount 近似の本体。λ, τ の推定はこちら。
- [Lo 1994（Harville と Henery の比較）](./1994-lo-comparison-harville-henery.md): 香港データで Henery が優れるという本論文の根拠。
- [Lo 1994（日本の走破時間モデル）](./1994-lo-running-time-japan.md): 日本で Stern（形状母数 4）が最良とした結果の出典。
- [Lo 1995](./1995-lo-ranking-probability-betting.md): Henery・Stern モデルの賭けでの優位（Kelly 型の最適化）。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md), [Henery 1981](./1981-henery-permutation-probabilities.md), [Stern 1990](./1990-stern-gamma-permutations.md): 比較・拡張の対象モデル。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): 効用による FLB 解釈の元。Saratoga 等の米国データ（Table 1）の出典。
- [Asch 1982](./1982-asch-racetrack-informed-behavior.md): Atlantic City のデータ（Quandt らのデータ）の系統。
- [Busche 1988](./1988-busche-exception-risk-preference.md): 香港で FLB がないという先行結果。本論文の Table 1 と整合。
- [Benter 2019](./2019-benter-model.md): 香港の本格的なシンジケート。プール仮説の根拠として引用されている（原典は Benter 1994）。
- [Hausch 1994](./1994-hausch-pricing-exotic-wagers.md): Harville が Henery よりわずかに良いとした反対の結果。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 条件付きロジット。式 (1) と同じ形の多項ロジット。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 着順確率モデルの比較（gamma・正規・Harville）。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 日本の FLB のサーベイ。
- [Snowberg 2010](./2010-snowberg-flb-risk-love-misperceptions.md): FLB をリスク愛好と確率の誤認で比べる。本論文の効用解釈への対案。
- [Deza 2017](./2017-deza-exotic-wagering-losses.md): discount 近似の応用。

## 検索語

競馬の確率モデル, 統計モデル, 本命大穴バイアス, 穴馬バイアス, 国際比較, 日本, 香港, 上海, べき補正, 票数シェア, 着順確率, 順序確率, 走破時間分布, Henery モデル拡張, 相関のある走破時間, 非一定分散, 共通因子, 上位5頭の尤度, 3連単, 馬単, discount モデル, Harville, Henery, Stern, gamma, 効用理論, Arrow-Pratt, リスク愛好, プールの大きさ, favorite-longshot bias, FLB, ordering probability, running time distribution, correlated running times, non-constant variance, exacta, trifecta, pool size, Lo Bacon-Shone

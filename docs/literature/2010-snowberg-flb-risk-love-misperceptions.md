---
title: Explaining the Favorite-Long Shot Bias: Is it Risk-Love or Misperceptions?
authors: Snowberg Erik, Wolfers Justin
year: 2010
venue: Journal of Political Economy 118(4) 723-746
url: http://users.nber.org/~jwolfers/papers/Favorite_Longshot_Bias.pdf
doi: 10.1086/655844
topic: market-efficiency
tags: favourite-longshot-bias, prospect-theory, probability-weighting, exotic-bets, us
verified: fulltext
importance: high
source: downloaded
source_version: working-paper
---

# FLB はリスク愛好か確率の誤認か：連勝系馬券の価格で両説を識別する

> 一言で: 単勝データだけではリスク愛好説と確率誤認説は区別できない。単勝で推定した各モデルで馬単・馬連・三連単の価格を予測させると、確率誤認（確率加重関数）モデルの方が一貫して当たる。

原本は NBER Working Paper 15923（2010年4月, 29ページ）。JPE 掲載版との差は未確認。ページ番号は WP の PDF ページ。

## 要旨

米国の全出走 6,403,712（1992–2001年）を使い、FLB の二つの説明を比較する (p.6)。新古典派は「合理的期待だがリスク愛好の代表的賭け手」、行動経済学は「リスク中立だが確率を歪めて知覚する代表的賭け手」と定式化する。どちらも単勝データにはちょうど識別（just-identified）で当てはまるので、単勝だけでは観察上同値である (p.4, p.10)。そこで、単勝で推定した効用関数・確率加重関数を使って**連勝系（exacta, quinella, trifecta）の価格を外挿予測**し、どちらが実際の価格に近いかで識別する。

## データと事実の整理（2節）

- 米国の公式データ（Axcis/ジョッキークラブ）、1992–2001年の全 6,403,712 出走。単勝分析は 5,610,580 出走 (p.3 Figure 1, p.6)。
- 連勝系の払戻が記録された 206,808 レース（1,485,112 出走）でも同じ FLB の形 (p.6)。
- 比較用に豪州 2,725,000 出走、英国 380,000 出走。米国はパリミュチュエル、英国はブックメーカー、豪州は両者併存だが FLB は同様に見られる (p.6, Figure 2)。1949年の Griffith 以来ほぼ不変 (p.6–7)。

単勝回収率の主要な数字 (p.3, Figure 1):

| 買い方 | 回収率（1ドルあたり損益） |
|---|---|
| オッズ 100/1 以上の馬 | 約 −61% |
| 無作為に買う | −23% |
| 毎レース1番人気 | −5.5% |
| オッズ 4/1〜9/1 の馬 | ほぼ一定の −18% |

- Thaler and Ziemba (1988) が報告した「大本命はプラス回収」は、どのデータでも再現しない (p.7)。
- 「その日の最終レースで中穴が過剰に買われる（損失回避）」も、点推定は少し違うが統計的に有意でない (p.7)。古い小標本の結果が再現しない例として重要。
- 脚注1で FLB の例外として香港（Busche and Hall 1988, 2,653 レース）と日本（Busche 1994, 1,738 レース）を挙げる (p.4)。

## 二つのモデル（3節）

単勝オッズ $O$、勝率 $p$ とする。

- **リスク愛好クラス**（期待は不偏、効用が非線形）: 均衡では全ての馬で期待効用が等しく $p\,U(O) = 1$ と正規化でき、$U(O) = 1/p$ として効用関数をデータから逆算する。CARA でよく当てはまり、Arrow–Pratt 係数は −0.017（リスク愛好） (p.9, Figure 3 左)。
- **誤認クラス**（リスク中立、確率を $\pi(p)$ と知覚）: $\pi(p_A)(O_A+1) = \pi(p_B)(O_B+1) = 1$ (p.10, 式(2))。推定された $\pi(p)$ は Prelec (1998) の1パラメータ型 $\ln \pi = -(-\ln p)^{a}$ に近い (p.11, Figure 3 右)。
- 控除率の分だけ馬は単勝オッズほど勝たないので、オッズ由来の確率はレースごとの $(1-\text{控除率})$ で補正して平均的に不偏にしている (p.11 脚注7)。

### 連勝系への外挿（3.3節）

馬単 AB のオッズ $E_{AB}$ について (p.12):

| | リスク愛好 | 誤認 |
|---|---|---|
| 均衡条件 | $p_A p_{B|A} U(E_{AB}) = 1$ | $\pi(p_A)\pi(p_{B|A})(E_{AB}+1) = 1$ |
| 予測式 | $E_{AB} = U^{-1}(U(O_A) U(O_{B|A}))$ | $E_{AB} = (O_A+1)(O_{B|A}+1) - 1$ |

条件付き確率 $p_{B|A}$ は Harville 式で単勝から作る。誤認クラスは「まず1着、次に2着」と段階的に確率を評価し、複合くじを単純くじに還元しない、という仮定を含む (p.13)。還元するなら誤認クラスはリスク愛好クラスと同じ価格付けになる、という指摘が重要で、リスク愛好クラスの棄却は Ali (1977)、Shin、裁定の限界など「単純くじの価格に偏りを置く」理論群をまとめて退けることになる (p.13–14)。

## 推定結果

$1 の条件付き請求権の価格で予測誤差を比べる (p.16, Table 1):

| 券種 (n) | 平均絶対誤差 リスク愛好 / 誤認 | 絶対%誤差 リスク愛好 / 誤認 | 誤認の方が近い割合 |
|---|---|---|---|
| Exacta (197,551) | 0.0139 / 0.0125 | 34.3% / 28.0% | 57.9% |
| Quinella (70,169) | 0.0274 / 0.0258 | 39.0% / 36.3% | 54.0% |
| Trifecta (137,756) | 0.00796 / 0.00532 | 100% / 57.4% | 71.1% |

- Exacta で誤認クラスは 6.3 ポイント近く、相対改善 18.4%。両馬とも 10/1 未満（データの70%）では 16.8% 改善 (p.14–16)。
- 長いオッズ側ではどちらのクラスでも説明できないパターンが残る (p.16)。
- **Harville 式の検証 (p.17–18, Table 2)**: 2着予測で Harville 式の係数は 0.793（固定効果を足すと 0.908）。有用だが、1着馬と当該馬のオッズのダミー（各100水準）やその交互作用（10,000ダミー）が有意に追加説明力を持つ（F=32.3, 43.5）。つまり Harville の条件付き独立は破れている。経験的な条件付き確率に置き換えても結論は同じ (p.19, Table 3)。
- **馬単と馬連の同時価格付け（5節, p.19–23）**: 上位2頭が決まったとき、どちらが1着かを予測させると、誤認クラスの予測は正の相関（係数 0.63, SE 0.014, n=60,288）、リスク愛好クラスは**負**の相関（−0.59）。例: 4/1 と 9/1 の馬で平均馬単オッズ 39/1 と 44/1、馬連 20/1 は誤認クラスとほぼ一致 (p.21)。オッズ・馬連オッズの百分位固定効果とその交互作用を入れても頑健 (p.22–23, Figure 5)。

> This bias likely persists in equilibrium because misperceptions are not large enough to generate profit opportunities for unbiased bettors. (p.24)

## 批判的に読む

- 「代表的賭け手」の二択に押し込めている。異質な賭け手の混合（[Gandhi and Serrano-Padial 2015](./2015-gandhi-belief-heterogeneity-longshot.md)）や私的情報（[Ottaviani and Sørensen 2010](./2010-ottaviani-noise-information-flb.md)）は、どちらのクラスに入るかを著者が整理してはいるが、直接は検定していない。
- 予測精度は平均絶対誤差と「どちらが近いか」の割合で、尤度ベースの比較ではない。差は統計的に有意だが、Quinella の改善は小さい（2.7ポイント）。
- 200/1 を超えるオッズは効用関数を推定できず価格付けできない (p.12 脚注9)。三連単の長いオッズ部分が抜けている。
- 回収率は実オッズ（米国の確定配当）で計算されており、控除率込みの数字。ただし確率の補正では控除率で正規化している。
- データは有料の公式データで、再現には同等のデータ購入が必要。

## keiba-ai での使い方

- **単勝の確率加重関数を推定して連勝系に流用する**: JRA 単勝オッズで $\pi(p)$（Prelec 型でよい）を推定し、誤認クラスの式 $E_{AB}=(O_A+1)(O_{B|A}+1)-1$ で馬単・三連単の市場オッズを再現できるかを見る。仮説: 本論文と同じく誤認型の方が JRA の連勝系オッズをよく再現する。再現できるなら、連勝系の「市場の見積もり」を単勝から作れ、期待値計算で実オッズが無い時点の推定に使える。
- **Harville の破れの補正**: 本論文の Table 2 は「1着馬のオッズ × 当該馬のオッズ」の非パラメトリック補正が2着予測を改善することを示す。keiba-ai で Plackett–Luce/Harville 系の順位モデルを使うとき、2着・3着確率の校正を（1着馬人気 × 当該馬人気）の層別で評価する実験を入れる。
- **評価の作法**: 「最終レースの損失回避」のような古い小標本の効果が大標本で消える例として、特徴量の採否を十分な標本で検定する根拠になる。
- 1番人気でも −5.5% という数字は、オッズだけを使う戦略で控除率を超えることの難しさの基準線になる。

## 関連ノート

- [Griffith 1949](./1949-griffith-odds-adjustments.md): FLB の最初の報告。Figure 2 で歴史的推定として重ねている。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 連勝系の条件付き確率に使う公式。本論文が破れを検証。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): リスク愛好の効用逆算の先行例。
- [Thaler and Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 大本命プラス回収・最終レース効果を報告。本論文で再現せず。
- [Busche and Hall 1988](./1988-busche-exception-risk-preference.md): 香港で FLB が無いという例外。
- [Jullien and Salanié 2000](./2000-jullien-estimating-preferences-racetrack.md): 単勝だけで選好と知覚を識別しようとした先行研究。
- [Ottaviani and Sørensen 2010](./2010-ottaviani-noise-information-flb.md): 情報ベースの説明。期待収益曲線の形を再現しようとした理論。
- [Gandhi and Serrano-Padial 2015](./2015-gandhi-belief-heterogeneity-longshot.md): 信念の異質性で FLB を構造推定。代替説明。
- [Obata and Dazai 2014](./2014-obata-horse-racing-prospect-theory.md): JRA データで確率加重を検証。日本版の対応研究。
- [Okamoto and Fukushige 2022](./2022-okamoto-flb-without-cross-arbitrage.md): 券種間で FLB の出方が違うかを日本で検証。
- [Meyer and Hundtofte 2023](./2023-meyer-longshot-bias-context-effect.md): FLB を文脈効果として説明。誤認説の発展。
- [Lo and Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較。条件付き独立の破れの別の扱い。

## 検索語

本命穴馬バイアス, ロングショットバイアス, favorite-longshot bias, FLB, リスク愛好, risk-love, risk-loving, 確率の誤認, misperceptions, 確率加重関数, probability weighting, Prelec, プロスペクト理論, prospect theory, 複合くじ, compound lottery, 還元公理, 連勝系, exotic bets, 馬単, exacta, 馬連, quinella, 三連単, trifecta, Harville 公式, 条件付き独立, conditional independence, 代表的賭け手, representative agent, CARA, Equibase, 米国競馬, 最終レース効果, 損失回避

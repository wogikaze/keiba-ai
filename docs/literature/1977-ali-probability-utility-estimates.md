---
title: Probability and Utility Estimates for Racetrack Bettors
authors: Ali Mukhtar M.
year: 1977
venue: Journal of Political Economy 85(4) 803-815
url: https://ideas.repec.org/a/ucp/jpolec/v85y1977i4p803-15.html
doi: 10.1086/260600
topic: market-efficiency
tags: favourite-longshot-bias, parimutuel, risk-preference, heterogeneous-beliefs, classic, harness-racing, representative-agent, last-race-effect
verified: metadata
importance: high
source: unavailable
source_version:
---

# 競馬の賭け手の確率と効用の推定：NY ハーネス 2 万レースの本命-大穴バイアスと、信念の異質性による説明

> **原本未取得**。JPE（シカゴ大学出版局, JSTOR）で有料、無料版は見つからなかった。本ノートは他の文献での引用に基づく。主な出典は Sauer (1998) の要約と Table 4 の再掲、同じ著者の Ali (1998)（同じデータを再分析した論文で、データ表がある）、Ottaviani & Sørensen (2010) と芦谷 (2010) の理論の紹介。数値の出典ページは引用元のもの。

> 一言で: ニューヨークの3つのハーネス（繋駕速歩）競馬場の 20,247 レースで、1番人気は大きく過小に、4〜8番人気は過大に賭けられていた。これを代表的賭け手の局所的リスク愛好として効用関数を推定すると、売上の小さい競馬場や最終レースでリスク愛好が強く出る。同時に、賭け手の信念がばらつくだけで（リスク中立でも）本命-大穴バイアスが生じることを理論的に示した。

## データ

Ali (1998, Table 1, p.225) によると、同じデータの内訳は次のとおり（すべてニューヨーク州のハーネス競馬）。

| 競馬場 | 年 | レース数（年あたり） | 1レースあたりの売上（全券種, US$） |
|---|---|---|---|
| Saratoga | 1970–74 | 約 1,700–1,900 | 約 2.4–2.6 万 |
| Roosevelt | 1970/71–74 | 約 1,350–1,700 | 約 21–23 万 |
| Yonkers | 1971–74 | 約 1,270–1,410 | 約 22–23 万 |

合計 20,247 レース（Sauer 1998, p.2037 Table 4 の注; Ali 1998, p.225）。8頭立てが 15,402 レースを占める（Ali 1998, p.225）。Saratoga は売上がほかの2場の約10分の1の「小さな市場」である。

## 結果

### 人気順位別の主観確率と客観確率（Sauer 1998, p.2037, Table 4 による再掲）

馬をレース内の単勝人気順位でまとめ、推定勝率 $\hat p_k$（その順位の馬が勝った割合）と票数シェア $w_k$ を比べる。

| 人気順位 | $\hat p_k$ | $w_k - \hat p_k$ |
|---|---|---|
| 1 | 0.358 | −0.035 |
| 2 | 0.205 | +0.003 |
| 3 | 0.153 | −0.001 |
| 4 | 0.105 | +0.007 |
| 5 | 0.076 | +0.006 |
| 6 | 0.055 | +0.005 |
| 7 | 0.034 | +0.008 |
| 8 | 0.021 | +0.007 |

$w_k = \hat p_k$ の検定の t 値は、1番人気で −10.3、2・3番人気は有意でなく、4〜8番人気で 3.0 を超える（Sauer 1998, 脚注27, p.2037）。主観確率と客観確率が等しいという帰無仮説は強く棄却された。同じ方法の Hoerl & Fallin (1974) のサラブレッド 1,825 レースでは棄却されなかったのと対照的である（Sauer 1998, p.2036）。

### 代表的賭け手の効用（局所的リスク愛好）

Weitzman (1965) と同様に、オッズと勝率の観測された関係から、代表的賭け手の効用関数の局所的な形を復元した（Sauer 1998, p.2030）。Snowberg & Wolfers (2010) は、この効用関数が凸（リスク愛好）であるとまとめている。

リスク愛好の程度は2つの方向で変わった（Sauer 1998, p.2038）。

1. **市場の規模**。リスク愛好を表すパラメータは、小規模市場の競馬場で .17、大規模市場の競馬場で .06（脚注31）。上の表から、小規模市場は Saratoga と考えられる（推測）。
2. **最終レース**。その日の最終レースではリスク愛好が強まる。負けている賭け手が大穴で取り返そうとする、という解釈である。Thaler & Ziemba (1988) はこれを心の会計（mental accounting）として解釈した。

### 連勝（daily double）の価格

2レースの勝ち馬を当てる daily double について、単勝プールが効率的な確率を与え2レースが独立なら、効率的な配当は2つの勝率の積の逆数から1を引いたものになる。Ali のデータはこの予測に合っていた（Sauer 1998, p.2046）。

### 信念の異質性によるバイアスの導出（Theorem 2）

2頭立てで、リスク中立の賭け手がそれぞれ同額をどちらかの馬に賭ける。各人の信念は、真の勝率を中央値とする分布から引かれる。このとき市場の本命の確率は中央値の賭け手の信念より低くなり、中央値の信念が正しければ本命-大穴バイアスが生じる（Ottaviani & Sørensen 2010, p.25; 芦谷 2010, p.8）。Blough (1994) が $n$ 頭に拡張した。

この結果は、同じ論文の前半で示した「リスク愛好による説明」と競合する説明を著者自身が与えている点で重要である。

## 批判的に読む

- **ハーネス競馬である**。サラブレッドの平地競走ではなく繋駕速歩競走。出走頭数や展開の性質が違う。
- **集計の単位**。人気順位でまとめて $\hat p_k$ を出す方法は、似た人気の馬の勝率が均質だと仮定する。Busche & Hall (1988) は、この方法自体が客観確率の測定に誤差を入れうると指摘している（小幡・太宰 2014 の紹介）。
- **代表的個人の解釈**。リスク愛好の推定値は「全員が同じ効用を持つ」仮定の下での値で、Theorem 2 が示すように、信念のばらつきでも同じパターンが生じる。どちらが真の原因かは単勝データだけでは識別できない（Snowberg & Wolfers 2010 の観測的同値性）。
- **最終レース効果は再現されていない**。Snowberg & Wolfers (2010, PDF p.7) は 1992–2001 年の米国 640 万出走で、最終レースの差は統計的に有意でないと報告している。小標本の古い結果として扱う。
- **規模との相関は因果ではない**。小規模市場ほどリスク愛好が強いという結果は、情報を持つ賭け手の参入（Sauer 1998 の解釈）でも、客層の違いでも説明できる。
- 原本未読のため、効用関数の関数形、推定方法、オッズ帯別の回収率は未確認。

## keiba-ai での使い方

- **人気順位別の較正表を最初に作る**。本論文の表の形（人気順位 × $\hat p_k$ × $w_k-\hat p_k$ × t 値）は、JRA データでオッズ由来確率の偏りを見る最小限の診断になる。仮説: JRA 単勝でも1番人気は過小に賭けられているが、その差は Ali の −.035 より小さい（売上が大きいため）。
- **売上規模による層別**。Saratoga と Roosevelt・Yonkers の対比は、同じ主催者内で売上規模の差がバイアスの差になる例である。仮説: JRA の売上の小さいレース（平場の未勝利戦など）や地方競馬では、大レースより偏りが大きい。層別した較正誤差（ECE）や log loss の改善幅を比べる。
- **最終レース・開催日内の位置を特徴量にする**。効果は再現されていないので、まず検定してから使う。JRA のその日の最終レースで、人気順位別の $w_k - \hat p_k$ が他のレースと違うかを調べる。
- **信念の異質性**。票数シェアが「平均的な信念」ではなく「信念の分布の結果」だという見方は、オッズ由来確率を補正する理由になる。補正なしの $w_i$ を勝率として使うと、本命の勝率を系統的に過小評価する。

## 関連ノート

- [Griffith 1949](./1949-griffith-odds-adjustments.md): オッズ帯別にバイアスを最初に示した研究。本論文は人気順位別の方法で追試した。
- [Snyder 1978](./1978-snyder-efficient-markets-horse-racing.md): 同時期の北米の集計研究。
- [Asch ら 1982](./1982-asch-racetrack-informed-behavior.md): 同じ人気順位別の方法で Atlantic City を分析。最終レース効果も報告。
- [Busche & Hall 1988](./1988-busche-exception-risk-preference.md): 同じ方法で香港を分析し、バイアスがないと報告。
- [Thaler & Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 最終レース効果を心の会計で解釈。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): 本論文の数値を Table 4 に再掲し、規模の効果を情報を持つ賭け手の数で説明。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 同じ著者が同じデータで Harville 型の順位確率モデルを比較した論文。
- [Jullien & Salanié 2000](./2000-jullien-estimating-preferences-racetrack.md): 代表的個人の効用推定を、オッズ帯の集計なしで行う方法に改良。
- [Ottaviani & Sørensen 2010](./2010-ottaviani-noise-information-flb.md): 私的情報によるバイアスの説明。Ali の Theorem 2（信念の異質性）と区別する。
- [Gandhi & Serrano-Padial 2015](./2015-gandhi-belief-heterogeneity-longshot.md): 信念の異質性による説明を実証的に発展。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): 最終レース効果が再現されないことを示した。

## 検索語

本命-大穴バイアス, favourite-longshot bias, favorite-longshot bias, FLB, ハーネス競馬, 繋駕速歩, harness racing, trotting, ニューヨーク, Saratoga, Roosevelt, Yonkers, 主観確率, subjective probability, 客観確率, objective probability, 人気順位, favorite rank, 効用関数の推定, utility estimation, 代表的賭け手, representative bettor, リスク愛好, risk loving, local risk preference, 局所的リスク愛好, 信念の異質性, heterogeneous beliefs, 中央値の賭け手, median bettor, 最終レース効果, last race effect, 心の会計, mental accounting, 市場規模, daily double, 連勝, Ali 1977, Journal of Political Economy

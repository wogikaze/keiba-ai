---
title: Racetrack betting and informed behavior
authors: Asch Peter, Malkiel Burton G., Quandt Richard E.
year: 1982
venue: Journal of Financial Economics 10(2) 187-194
url: https://ideas.repec.org/a/eee/jfinec/v10y1982i2p187-194.html
doi: 10.1016/0304-405X(82)90012-5
topic: market-efficiency
tags: late-money, informed-bettors, odds-dynamics, parimutuel, classic, morning-line, favourite-longshot-bias, last-race-effect
verified: metadata
importance: high
source: unavailable
source_version:
---

# 競馬の賭けと情報を持つ行動：締切直前の資金は勝ち馬を知っている

> **原本未取得**。Journal of Financial Economics（ScienceDirect）で有料、著者稿やワーキングペーパー版は見つからなかった。本ノートは Sauer (1998) の Table 4・Table 6A に再掲された数値と、他の文献での引用に基づく。ページは引用元のもの。

> 一言で: Atlantic City 競馬場の 1978 年のデータで、勝ち馬は朝の予想オッズより最終オッズが下がる（買われる）一方、負けた馬は上がる。締切前の最後の時間帯の資金だけで作ったオッズでは、この差がさらに大きい。情報を持つ賭け手は締切直前に賭ける、という競馬場の通説を初めてデータで示した。

## データ

- Atlantic City Race Course（ニュージャージー州）の 1978 年シーズン。レース数は Sauer の表注では 729、本文では 765（Sauer 1998, p.2037 Table 4 注, p.2043 Table 6A 見出しと本文）。どちらが正しいかは未確認。
- 朝のオッズ $O_{ML}$（競馬場の予想家が出す morning line）、最終オッズ $O_{FINAL}$、締切前の最後の時間帯の資金だけから計算した限界オッズ $O_{LATE}$ を使う。$O_{LATE}$ の時間帯は、Sauer の本文では「最後の8分間」、表注では「賭け期間の最後の3分の1」と書かれている（Sauer 1998, p.2043）。

## 結果

### 1. 勝ち馬は締切に向けて買われる（Sauer 1998, p.2043, Table 6A による）

着順ごとの平均オッズの比。1より小さければ朝の予想よりオッズが下がった（買われた）。

| 着順 | $O_{FINAL}/O_{ML}$ | $O_{LATE}/O_{ML}$ |
|---|---|---|
| 1着 | 0.96 | 0.82 |
| 2着 | 1.16 | 1.06 |
| 3着 | 1.22 | 1.17 |
| 着外 | 1.59 | 1.63 |

勝ち馬だけが朝の予想より買われ、2・3着馬を含む他の馬は予想より売れない。締切前の資金だけで見ると勝ち馬の比は 0.82 まで下がり、着外馬では逆に上がる。締切直前の資金の方が勝ち馬をよく知っている、ということである。

**Thaler & Ziemba (1988) の原本による補足**（[同ノート](./1988-thaler-parimutuel-anomalies.md)、原本 p.166）: Thaler らは本論文を「Atlantic City Race Course の **729 レース**」の研究として紹介し、勝ち馬の最終オッズは朝のオッズの 96%、**最後の8分間**の資金だけの限界オッズでは 82%、**最後の5分間**では 79% まで下がると書く。負け馬の最終オッズは朝のオッズの約 1.5 倍。上の「729 か 765 か」「最後の8分か3分の1か」の食い違いについて、Sauer とは独立の二次資料が 729 レース・8分を支持する。5分間の 79% という数値は Sauer の表にはない。いずれも本論文の原本では未確認。

> "winning horses are especially preferred by the late bettors." (Sauer 1998, p.2043 の引用)

### 2. なぜ情報を持つ賭け手は遅く賭けるか（Sauer 1998, pp.2042–2043 の整理）

- **払戻は最終オッズで決まる**。賭け期間の初めはプールが小さく、少額でオッズが大きく動く（7-1 が 3-1 になる）。遅く賭ければ期待払戻の推定の分散が小さい。
- **戦略的な理由**。大口の賭けはオッズを動かし、オッズを見ている他の賭け手に「何かある」と知らせる。遅く賭ければ便乗（bandwagon）を避けられる。

### 3. 本命-大穴バイアスと最終レース

- 人気順位別の票数シェアと推定勝率の差 $w_k - \hat p_k$ は、1番人気で −0.036（$\hat p_1 = 0.361$）、9番人気で +0.012。Ali (1977) と同じパターンである。1番人気の差の有意性について、Sauer の脚注28は「Ali では標準誤差の約10倍、Asch らでは2倍の大きさ」と書いており、t 値が約20なのか差が2倍なのかは文面から確定できない（Sauer 1998, p.2037, Table 4 と脚注28）。
- 最終2レースでは本命-大穴バイアスが強まる（芦谷 2010, p.4）。ただし Snowberg & Wolfers (2010, PDF p.7) は 1992–2001 年の米国全データでこの効果を再現できなかった。

## 後続：締切直前の資金に乗って儲かるか

Asch ら (1984, *Journal of Business*) は「締切直前にオッズが下がった馬に賭ける」ルールで正の利益を報告したが、これは複勝・3着内オッズを払戻に変換するプログラムの誤りによるものだった。訂正版（1986）では新しいデータでも検証し、控除率よりは損失が小さいが黒字にはならないと結論した（Sauer 1998, p.2046, 脚注43）。芦谷 (2010, p.4) は、締切間際にオッズが下がった1番人気の複勝で期待利益が正になる、という結果を Asch ら (1984, 1986) と Asch & Quandt (1986) のものとして紹介している。

## 批判的に読む

- **小標本**。1競馬場・1シーズン、700 レース余り。着順別の比の標準誤差は Sauer の表にはない。
- **比の平均の取り方**。「平均オッズの比」（Sauer の注）なので、大穴の大きなオッズが平均を支配する。中央値や対数の差で見た方が頑健だが、原本の処理は未確認。
- **Sauer の引用ページの誤り**。Sauer は引用文を "(1982, p.306)" としているが、論文は pp.187–194 なので、ページは誤り（別の論文のページの可能性）。Table 6A の注の出典は p.193。
- **実時間で使えるか**。$O_{LATE}$ は締切後に計算できる量で、締切前に知ることはできない。勝ち馬が締切直前に買われることは、締切直前のオッズの変化で賭けて儲かることを意味しない（後続の 1984/1986 論文の結果がそれを示す）。
- 原本未読のため、統計検定、オッズの時刻の正確な定義、最終レースの分析の詳細は未確認。

## keiba-ai での使い方

- **オッズの時系列は強い特徴量の候補**。仮説: JRA でも、前日オッズ・朝のオッズから最終オッズへの変化（対数比）は、最終オッズを条件にしても勝率を予測する。特に締切前10分の変化が効く（JRA では単勝の約半数が締切10分前以降に買われる, 芦谷 2010, p.4 が引く Mori & Hisakado 2009）。
- **リークに厳重に注意**。最終オッズは締切後にしか確定しない。予測に使えるのは「実際に馬券を買う時刻」に観測できるオッズだけである。評価では、買う時刻のオッズで特徴量を作り、払戻は確定オッズで計算する。最終オッズを特徴量にしたモデルの回収率は、実際には達成できない。
- **予想印（新聞の予想・JRA の予想オッズ）との比較**。$O_{FINAL}/O_{ML}$ に当たる「予想オッズに対する実際の人気」を特徴量にする。予想家が見落とした情報を市場が持っているかの代理になる。

## 関連ノート

- [Ali 1977](./1977-ali-probability-utility-estimates.md): 同じ人気順位別の方法による北米の本命-大穴バイアス。最終レース効果も報告。
- [Snyder 1978](./1978-snyder-efficient-markets-horse-racing.md): 朝のオッズのバイアスに最初に注目した。
- [Crafts 1985](./1985-crafts-insider-knowledge-britain.md): 英国ブックメーカー市場で、予想オッズから大きく買われた馬に情報があることを示した。本論文の英国版。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Table 4 と Table 6A に本論文の数値を再掲。"Late money is smart money" とまとめる。
- [Shin 1991](./1991-shin-optimal-betting-odds-insiders.md): 本論文と Crafts の情報を持つ賭け手の証拠を受けて作られたインサイダーのモデル。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): 最終レース効果を大規模データで否定。
- [Mori & Hisakado 2010](./2010-mori-independent-herding-betters.md): JRA の投票の時間的な流れ（独立な賭け手と追随する賭け手）。
- [Hanyu ら 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 締切直前のオッズの動きと情報の集約。本論文の現代版。
- [芦谷 2010](./2010-ashiya-longshot-bias-survey.md): 締切間際のオッズ低下を使う戦略を紹介。

## 検索語

締切直前, 締切間際, late money, smart money, 情報を持つ賭け手, informed bettors, informed behavior, オッズの変化, odds movement, odds dynamics, 朝のオッズ, morning line, 予想オッズ, 最終オッズ, final odds, 限界オッズ, marginal odds, 便乗, bandwagon, 本命-大穴バイアス, favourite-longshot bias, FLB, 最終レース効果, last race effect, Atlantic City, パリミュチュエル, parimutuel, Asch Malkiel Quandt 1982, Journal of Financial Economics

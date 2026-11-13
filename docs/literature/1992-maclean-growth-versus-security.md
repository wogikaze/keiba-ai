---
title: Growth Versus Security in Dynamic Investment Analysis
authors: MacLean L. C., Ziemba W. T., Blazenko G.
year: 1992
venue: Management Science 38(11) 1562-1585
url: https://dl.acm.org/doi/10.5555/3217126.3217130
doi: 10.1287/mnsc.38.11.1562
topic: betting-strategy
tags: fractional-kelly, kelly, risk-management, growth-security-tradeoff, blackjack, horseracing, lotto
verified: abstract
importance: high
source: unavailable
source_version:
---

# 成長と安全性のトレードオフ：分数 Kelly で「どれだけ控えるか」を測る

> 原本未取得。INFORMS は購読制で、OpenAlex・Semantic Scholar に OA 版が無く、Dalhousie 大学のワーキングペーパー版（1988）の公開版も見つからなかった。本ノートは要旨と、原本取得済みの二次資料（MacLean, Thorp, Ziemba 2010、Ziemba 2023、Sauer 1998）および Ziemba と MacLean による解説章（Edinburgh 大学の講義ページで公開）に基づく。

> 一言で: Kelly（最大成長）とは逆の極として「最大安全」を置き、さまざまな成長と安全の指標を計算する式を導いた。分数 Kelly（Kelly 比率の一定割合だけ賭け、残りは現金）を動かすことで、成長と安全のトレードオフ曲線を完全に描ける。Kelly より多く賭けると成長も安全も下がる（支配される）ので、合理的な選択は Kelly 以下に限られる。

## 要旨から分かること

- 成長の最大化だけでなく、安全性の最大化に基づく戦略も作れる。いくつかの成長と安全の指標について計算式を導く。
- 分数 Kelly 戦略で、成長と安全の完全なトレードオフを描ける。
- キーワード（EconPapers の書誌による）: capital accumulation, fractional Kelly strategies, effective growth-security tradeoff, blackjack, horseracing, lotto games, turn of the year effect。適用例としてブラックジャック、競馬、ロト、年末年始効果（1月効果）の先物を扱ったとみられる。

## 二次資料から分かる中身

### ブラックジャックの図

勝率 0.51（優位 2%）のコイン投げ近似で、賭ける割合に対して「半減する前に2倍になる確率」「半減する前に4倍になる確率」「相対成長率」を重ねた図が本論文の出典として再掲されている（Ziemba and MacLean の解説章, Fig. 1.1）。成長率も安全性も $f>f^*=0.02$ で下がるので、Kelly を超えて賭けるのは決して勧められない、と解説している。

MacLean, Thorp, Ziemba (2010) は同じ設定の数値表を MacLean and Ziemba (1999) から引いている (p.4, Table 3)。読み取り値は、Kelly の 0.5 倍で2倍到達確率 0.89・相対成長率 0.75、1.0 倍で 0.67・1.00、2.0 倍で 0.50・0.00。本論文自体の表の数値は未確認。

### 大きな賭け比率の例

MacLean, Thorp, Ziemba (2010) は、Kelly の賭けが資産の大きな割合になる例として、本論文の「1月効果の先物への 74% の賭け」を挙げている (p.7)。

### 半分 Kelly の目安

Ziemba (2023) は、半分 Kelly は成長率の 75% を保ちつつ、損益分岐以上になる確率をフル Kelly の 87% から 95.4% に上げる、と書く (p.646)。この数値が本論文由来かは明記されていない。

### 分数 Kelly と効用関数

対数正規の資産では、負のべき効用 $u(w)=\delta w^\delta$（$\delta<0$）の最適解は「Kelly 比率 $\alpha=1/(1-\delta)$ と現金の混合」と一致する。半分 Kelly は $\delta=-1$、4分の1 Kelly は $\delta=-3$ (MacLean, Thorp, Ziemba 2010, p.4)。分数 Kelly を効用関数の選択として解釈する根拠になる。ただし離散の賭けでは厳密には一致しない（同 p.4 のコイン投げの式）。

### 情報優位者の問題への拡張

Sauer (1998) は Isaacs (1953) の期待利益最大化の問題に対し、リスク回避を入れた分析として本論文を挙げている (p.6, 注10)。

## 批判的に読む

- 原本を読んでいないため、どの安全指標（目標到達前に一定水準を割る確率、一定期間後に水準を上回る確率など）を、どの近似で計算したかは未確認。
- ブラックジャックの例は独立同分布の二値の賭けで、競馬の多値で毎回違う賭けにそのまま当てはまるかは別途確認が要る。
- 「Kelly 超は支配される」は確率が既知の場合の結論である。推定誤差があると、名目上の Kelly 比率が実際には Kelly 超になっている可能性がある（MacLean, Thorp, Ziemba 2010 の平均の誤差の議論）。

## keiba-ai での使い方

- **分数 Kelly の係数を指標で決める**: 係数 $c$ を 0.1〜1.0 で変えたバックテストで、(a) レースあたりの平均対数成長率、(b) 半減前に2倍になる確率（ブートストラップ）、(c) 最大ドローダウン、を並べた成長–安全の曲線を描く。その上で許容するリスクの水準から $c$ を選ぶ。
- **支配される領域の確認**: 曲線上で $c$ を上げても成長率が増えなくなる点（モデル誤差込みの実効 Kelly 点）を探す。仮説: 校正の悪いモデルほどこの点が $c<1$ に来る。
- **報告の形式**: 回収率だけではなく、成長と安全の2軸で戦略を比べる。単一の数字（回収率、シャープレシオ）での比較は、安全性の違いを隠す。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 最大成長の極。
- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): Kelly の漸近最適性の証明。
- [MacLean, Thorp, Ziemba 2010](./2010-maclean-kelly-good-bad-properties.md): 本論文を含む成長と安全の研究の要約。ブラックジャックの表や 74% の例。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): 連続近似での分数 Kelly の成長率比 $c(2-c)$ とリスク比 $c$。
- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 競馬への Kelly 型システムの適用。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): リスク中立の情報優位者の問題（本論文がリスク回避を入れたとされる）。
- [Busseti, Ryu, Boyd 2016](./2016-busseti-risk-constrained-kelly.md): ドローダウン確率の制約を凸最適化で入れた Kelly（安全性の別の定式化）。
- [Deza ほか 2015](./2015-deza-chance-constrained-parimutuel.md): 確率制約付きのパリミュチュエル賭け。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 確率推定の不確実性を入れた競馬の Kelly。
- [Ziemba 2023](./2023-ziemba-parimutuel-revisited.md): 半分 Kelly の目安とケンタッキーダービーでの資産推移。

## 検索語

成長と安全, 成長–安全トレードオフ, 分数 Kelly, ハーフ Kelly, 部分 Kelly, 資金管理, ドローダウン, 半減前に2倍, 負のべき効用, ブラックジャック, 競馬, ロト, 1月効果, growth versus security, growth-security tradeoff, fractional Kelly, half Kelly, capital accumulation, probability of doubling before halving, negative power utility, dynamic investment analysis, blackjack, horseracing, lotto, turn of the year effect, MacLean Ziemba Blazenko

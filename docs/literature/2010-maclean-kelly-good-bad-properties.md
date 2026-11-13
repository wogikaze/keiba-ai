---
title: Long-Term Capital Growth: The Good and Bad Properties of the Kelly and Fractional Kelly Capital Growth Criteria
authors: MacLean L. C., Thorp E. O., Ziemba W. T.
year: 2010
venue: Quantitative Finance 10(7) 681-687
url: https://escholarship.org/uc/item/5mr5k8qj
doi: 10.1080/14697688.2010.506108
topic: betting-strategy
tags: kelly, fractional-kelly, risk-management, drawdown, estimation-error, overbetting
verified: fulltext
importance: high
source: downloaded
source_version: preprint
---

# Kelly 基準の良い性質と悪い性質：一覧表と「2倍 Kelly で成長率ゼロ」

> 一言で: Kelly（$E\log$ 最大化）の長所と短所を箇条書きで整理した短い総説。長所は漸近的な成長率最大と破産しないこと、短所は賭け額が大きすぎて短期の損失が深いこと。平均の推定誤差が分散の誤差より桁違いに効くので、推定に自信がなければ分数 Kelly に下げよ、が実務上の結論。

## 原本について

取得したのは著者による草稿 "Good and bad properties of the Kelly criterion"（2010年1月1日付、11ページ、UC Berkeley の Aldous の講義ページに掲載）。本文中で "this volume" と書いており、World Scientific の論文集 *The Kelly Capital Growth Investment Criterion*（2011）向けの原稿である。Quantitative Finance 10(7) の出版版との文言の違いは未確認。ページは草稿の頁番号。

## 平均の誤差が最も効く

冒頭で Chopra and Ziemba (1993) を引き、資産配分で入力の誤差が最終資産の確実性等価に与える損失は、平均・分散・共分散でおよそ 20 : 2 : 1 だと紹介する (p.1, Table 1)。リスク許容度が高い（リスク回避度が低い）ほど平均の誤差の影響が大きい。

| リスク許容度 | 平均 vs 共分散 | 平均 vs 分散 | 分散 vs 共分散 |
|---|---|---|---|
| 25 | 5.38 | 3.22 | 1.67 |
| 50 | 22.50 | 10.98 | 2.05 |
| 75 | 56.84 | 21.42 | 2.68 |

出典は p.2, Table 1。対数効用の Arrow–Pratt 絶対リスク回避度は $1/w$ で小さいため、Kelly は最もこの誤差に弱い側にいる (p.2)。

## 成長と安全性のトレードオフ（ブラックジャックの例）

勝率 $p=0.51$（優位 2%）のブラックジャックで、Kelly の何倍を賭けるかと「半減する前に2倍になる確率」「相対成長率」を比べた表 (p.4, Table 3; 出典 MacLean and Ziemba 1999)。草稿の PDF は表の組版が崩れており、下は読み取った値。

| Kelly に対する割合 | 半減前に2倍になる確率 | 相対成長率 |
|---|---|---|
| 0.1 | 0.999 | 0.19 |
| 0.3 | 0.98 | 0.51 |
| 0.5 | 0.89 | 0.75 |
| 0.7 | 0.78 | 0.91 |
| 1.0 | 0.67 | 1.00 |
| 1.5 | 0.56 | 0.75 |
| 2.0 | 0.50 | 0.00 |

半分 Kelly で成長率の 75% を保ちつつ、2倍到達の確率が 0.67 から 0.89 に上がる。Kelly を超えて賭けるとリスクが増え、しかも成長率が下がる。連続時間の近似では「ちょうど2倍の Kelly で成長率が安全利子率まで落ちる」(p.3; 証明は付録 p.8–9)。

> Hence it never pays to bet more than the Kelly strategy because then risk increases (lower security) and growth decreases (p.3)

### 分数 Kelly と負のべき効用

効用 $u(w)=\delta w^\delta$（$\delta<0$）は $\delta\to0$ で対数効用になる。定常な対数正規過程では、Kelly 比率 $\alpha=1/(1-\delta)$ と現金の混合が同じポートフォリオを与える。半分 Kelly は $\delta=-1$、4分の1 Kelly は $\delta=-3$ (p.4)。ただしコイン投げでは成り立たず、最適比率は

$$f_\delta^*=\frac{p^\alpha-q^\alpha}{p^\alpha+q^\alpha},\quad \alpha=\frac{1}{1-\delta}$$

で、$\alpha f^*$（$f^*=p-q$）にはならない (p.4)。分数 Kelly を「Kelly 比率の定数倍」と実装するのは、離散の賭けでは近似にすぎない。

## 良い性質（p.5–6）

1. $E\log X$ 最大化は漸近的に資産成長率を最大化する（Breiman 1961 ほか）。
2. 目標額への期待到達時間が、目標額を大きくすると漸近的に最小（Breiman 1961）。
3. 一般的な条件で、中央値の $\log X$ も漸近的に最大化する（Ethier）。
4. 破産の危険を冒さない（Hakansson and Miller 1975）。
5. 賭ける絶対額は資産に対して単調増加。
6. 近視眼的（myopic）政策が最適。前後の投資機会を考えなくてよい。過去は条件付き期待対数として取り込める (p.5)。実務上「決定的に重要」と著者は書く。
7. シミュレーションでは、「本質的に異なる」戦略より妥当なサンプル数で先行する。ただし成長率の差が小さいと分離は遅い。
8. 安全性を重視するなら負のべき効用か分数 Kelly で成長を安全性と交換できる。
9. 競争的最適性: 任意の戦略の資産 $X$ について $E(X/X^*)\le1$。Markov の不等式から $P[X>tX^*]\le1/t$ (p.6, Bell and Cover)。
10. 超セントペテルスブルク型の賭けでも Kelly 比率が定義できる (p.6)。

## 悪い性質（p.7）

1. 有利で損失リスクが小さい賭けでは、資産の大きな割合を賭けさせる。1984年 Breeders' Cup Classic で、単勝オッズを勝率とみなした Dr Z システム（複勝・3着内）の最適賭け額が資産の 64% になった例を挙げる (p.7)。
2. 固定比率の戦略は、勝ち数と負け数が等しいと必ず損している: $W_{2n}=W_0(1-f^2)^n$ (p.7)。
3. 重み付けしない平均リターン率は算術リターン率の半分に収束する。期待より少なく勝つように感じる (p.7)。

## 観察（p.7–8）

- 14% の優位を持つ賭けを700回（最も低い勝率 19%）しても、フル Kelly で $1000 が $18 になりうる。一方で 16.6% の確率で $100,000 以上になる。半分 Kelly でも最悪は $145 で、$100,000 超えは 0.1% しかない (p.7)。
- 「ほぼ確実に良い結果になるなら、十分大きい $N$ で期待効用も上回る」は誤り（Samuelson 1971 の反例）(p.8)。
- 支配には長い時間がかかる。優位 1.0% と 1.1% のコイン投げで、前者が後者を 84% の確率で上回るのに200万回かかる (p.8)。
- 結論: 確率分布が正確に分かっていれば Kelly は素直だが、実際の投資では通常そうではない。$E\log$ の計算は平均の推定誤差に極めて敏感なので、賭け額は減らすべきだとする (p.8)。

## 批判的に読む

- 総説であり新しい実証は無い。数値の多くは他の文献（MacLean and Ziemba 1999、Ziemba and Hausch 1986 など）からの再掲で、元の計算条件は本稿だけでは確認できない。
- 表 3 は PDF の組版が崩れていて、読み取り値に誤りがある可能性がある（特に 0.2, 0.4, 0.6, 0.8, 0.9 の行は省略した）。
- 「平均の誤差が 20 倍効く」は株式の資産配分での結果で、競馬の勝率推定にそのまま当てはまる保証は無い。ただし賭けの文脈では「平均」が勝率×オッズの期待値に当たり、同じ方向の示唆になると考えられる（推測）。

## keiba-ai での使い方

- **分数 Kelly を既定にする根拠**: 勝率モデルの誤差（特に期待値1付近の馬での過大評価）は、ここで言う「平均の誤差」に当たる。実験仮説: 単勝の Kelly 配分で、比率 $c\in\lbrace 0.1,0.25,0.5,1.0\rbrace $ を変えてバックテストすると、フル Kelly は対数成長率でも分数 Kelly に負ける（推定誤差があるため）。評価はレース時系列で分割したテスト期間の $\sum\log V$ と最大ドローダウン。
- **2倍 Kelly の目安**: 推定の過信で実効的に Kelly の2倍を賭けていると成長率がほぼゼロになる。モデルの確率が市場より自信過剰（校正の傾きが1より大きい）かを、資金管理の前に確認する。
- **バックテスト報告**: 回収率だけでなく「半減前に2倍になる確率」型の指標（ブートストラップで推定）を併記する。良い性質3（中央値）に合わせ、最終資産の平均ではなく中央値を報告する。
- **Dr Z の 64% の例**: 単勝オッズを確率とみなした複勝の賭けは、本命で極端に大きい比率を出しうる。複勝の資金配分には上限を設ける。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 原典。
- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): 良い性質1・2の出典。
- [MacLean, Ziemba, Blazenko 1992](./1992-maclean-growth-versus-security.md): 成長と安全性のトレードオフの定式化。本稿の性質一覧の元になった論文。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): 2倍 Kelly で成長率ゼロの一般的な証明や、支配に要する試行回数の出典。
- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 悪い性質1の Dr Z システム（複勝・3着内）の原典。
- [Baker, McHale 2013](./2013-baker-kelly-parameter-uncertainty.md): 推定誤差下での Kelly の縮小を定量化（本稿の結論の理論的な裏付け）。
- [Busseti, Ryu, Boyd 2016](./2016-busseti-risk-constrained-kelly.md): ドローダウン制約付き Kelly。
- [Sun, Boyd 2018](./2018-sun-distributional-robust-kelly.md): 確率の不確実性に頑健な Kelly。

## 検索語

Kelly 基準, ケリー基準, 分数 Kelly, ハーフ Kelly, フラクショナル・ケリー, 過剰ベット, 2倍 Kelly, 成長と安全性, ドローダウン, 破産, 推定誤差, 平均の誤差, 競争的最適性, 近視眼的政策, 負のべき効用, Kelly criterion, fractional Kelly, half Kelly, overbetting, double Kelly, growth versus security, drawdown, estimation error, Chopra Ziemba, competitive optimality, myopic policy, negative power utility, Dr Z system, Breeders Cup

---
title: Growth Versus Security in Dynamic Investment Analysis
authors: MacLean L. C., Ziemba W. T., Blazenko G.
year: 1992
venue: Management Science 38(11) 1562-1585
url: https://dl.acm.org/doi/10.5555/3217126.3217130
doi: 10.1287/mnsc.38.11.1562
topic: betting-strategy
tags: fractional-kelly, kelly, risk-management, growth-security-tradeoff, blackjack, horseracing, lotto
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 成長と安全性のトレードオフ：分数 Kelly で「どれだけ控えるか」を測る

原本は、本論文を第24章として再録した書籍 *The Kelly Capital Growth Investment Criterion: Theory and Practice*（MacLean, Thorp, Ziemba 編, World Scientific 2011）の全体 PDF（Internet Archive の item `kelly_202408`、883ページ）。再録は Management Science 誌面の写真版で、誌面のページ（1562-1585）がそのまま残る。書籍では pp.331-354、PDF では pp.360-383。以下のページは**誌面のページ**で書く（PDF のページ = 誌面 − 1202）。OCR のテキストなので数式は崩れており、式は誌面の画像の意味をとって書き直した。

> 一言で: Kelly（成長最大）と現金（安全最大）の2つの極を結ぶ「分数 Kelly」$p(\lambda)=\lambda p^*+(1-\lambda)p_0$ に沿えば、成長の指標は単調に増え安全の指標は単調に減る（Tradeoff Theorem）。だから $\lambda$ 1つで成長と安全の交換を連続的に選べる。ブラックジャック・競馬・ロト・年末効果の4例で、その曲線を計算した (p.1562-1563)。

## 原本で確認・訂正した点

旧ノートは要旨と二次資料（MacLean, Thorp, Ziemba 2010 など）に基づいていた。

- 二次資料経由で書いていた「1月効果の先物で Kelly 比率 74%」は原本どおり (p.1583)。著者は推定の不確実性と証拠金の要件から「はるかに小さい賭け」を勧め、実際の顧客口座では 25% 弱の分数 Kelly で運用した (p.1583-1584)。
- ブラックジャックの数値: 半分 Kelly（$p=0.02\to0.01$）で成長率は 25% 下がり、半減前に2倍になる確率は 67%→89% に上がる (p.1576)。旧ノートが MacLean, Thorp, Ziemba (2010) から引いた値（0.89・0.75）と一致する。
- **競馬の例は実データの検証ではない**。Hausch and Ziemba (1990) の「5場同時の5レース、各1頭、期待払戻 1.14」という仮想例で Kelly と固定比率を比べただけ (p.1577-1578)。
- 「Kelly 超は成長も安全も下がる」は、Kelly の性質の表（Table 1）で「データが不確かだと過大に賭ける」が悪い性質として挙げられ、本論文の動機だと明記されている (p.1566)。

## モデル

資産 $Y_t$、各期の投資比率ベクトル $p=(p_0,\dots,p_n)$（$p_0$ は現金）、総リターン $R_i(\omega)$ として $Y_t=Y_{t-1}\sum_i R_i(\omega_t)p_i$ (p.1563, 式1)。$Z_t=\ln Y_t$ は跳躍 $J(p,\omega)=\ln\sum_i R_i(\omega)p_i$ のランダムウォークになり、各指標はこれで計算できる (p.1567)。

| 種類 | 記号 | 意味 |
|---|---|---|
| 成長 G1 | $\mu_t=EY_t$ | $t$ 期後の平均資産 |
| 成長 G2 | $\phi=E\ln(Y_t^{1/t})$ | 平均指数成長率（Kelly はこれの最大化） |
| 成長 G3 | $\eta=E\,T(Y\ge U)$ | 目標 $U$ に届くまでの平均時間 |
| 安全 S1 | $\gamma_t=\Pr[Y_t\ge b_t]$ | $t$ 期後に目標以上の確率 |
| 安全 S2 | $\alpha=\Pr[Y_t\ge b_t,\ \forall t]$ | 全期間で下限経路を割らない確率 |
| 安全 S3 | $\beta=\Pr[T(U)<T(L)]$ | 下限 $L$ に落ちる前に $U$ に届く確率（例: 半減前に2倍）|

(p.1563-1564)。計算式は Table 2 (p.1569) にまとまる。S1 は $Z_t$ の正規近似、S3 と G3 は $E\theta^{J}=1$ の根 $\theta$ を使う Feller 型の境界問題の解で、上下の界を与える（ジャンプが初期資産に比べて小さければ界は狭い）(p.1568-1570)。

Tradeoff Theorem（p.1574）: 分数 Kelly の経路上では、どの組（$\mu_t,\gamma_t$）（$\phi,\alpha$）（$\eta^{-1},\beta$）でも、$\lambda$ を上げると成長は増え安全は減る。この経路は効率的フロンティアそのものではないが「effective」（一方の損失を他方の利得で埋める）で、2極を結ぶ直線より上にある (p.1566)。

## 適用例

### ブラックジャック（勝率 0.51、優位 2%）(p.1575-1577)

| $\lambda$ | 半減前に2倍の確率 | 相対成長率 |
|---|---|---|
| 0.3 | 0.98 | 0.51 |
| 0.4 | 0.94 | 0.64 |
| 0.6 | 0.83 | 0.84 |
| 0.7 | 0.78 | 0.91 |
| 1.0（Kelly） | 0.67 | 1.00 |
| 2.0 | 0.50 | 0.00 |

(p.1576, Table 3)。プロのチームは $\lambda=0.2$〜0.8 を使うという (p.1577)。

### 競馬（仮想例）(p.1577-1578)

単勝・複勝（place）・3着内（show）の1レースの払戻関数を書いたうえで、例は「5場で同時に行われる5レースに各1頭だけ賭ける」単純化。各馬の勝率 0.570〜0.190・オッズ 1-1〜5-1 で、期待払戻はどれも 1.14 (p.1577)。$t=700$ 回、初期資産 1000 での比較 (p.1578, Table 4):

| 目標 $b_t$ | Kelly | 半分 Kelly | 1% | 5% | 10% |
|---|---|---|---|---|---|
| 1,000 を超える確率 | 0.892 | 0.961 | 0.980 | 0.856 | 0.517 |
| 10,000 を超える確率 | 0.603 | 0.445 | 0.003 | 0.512 | 0.304 |
| 100,000 を超える確率 | 0.231 | 0.028 | 0.000 | 0.148 | 0.141 |
| 資産の中央値 | 17,497 | 8,670 | 2,394 | 10,464 | 1,176 |

固定比率（1%・5%・10%）は各馬に (0.1, 0.3, 0.3, 0.2, 0.1) で配分したもので分数 Kelly ではない。結論は「Kelly 比率を超える 10% は成長も安全も劣る」「**総賭け比率のほうが馬への配分より効く**」(p.1578)。

注意: 本文は Kelly の賭け比率を「6%」と書くが、同じページの Kelly ベクトル $(0.8529, 0.0140, 0.0210, 0.0141, 0.0700, 0.0280)$ は現金 0.8529、合計の賭けが約 14.7% になる (p.1577-1578)。ページ画像でも数字は同じで、OCR の誤りではなく原本の中の不整合である。どちらが正しいかは未確認。

### ロト・年末効果 (p.1578-1584)

人気のない数字のロト 6/49 では Kelly の賭けが資産の $10^{-7}$ 程度と極小で、1000万ドルの資金でも1回11枚・65枚 (p.1579-1580)。目標達成まで数百万年かかる (p.1581-1582)。年末効果の先物スプレッドでは Kelly が 74% になる (p.1583)。賭け比率が「資産の半分以上から100万分の1未満まで」大きく変わる例として並べられている (p.1563)。

## 批判的に読む

- 確率・リターン分布は既知で時間的に一定という前提（固定比率戦略）。著者も入力は動的に更新すべきと書く (p.1575)。
- 競馬の例は仮想の数値で、パリミュチュエルで自分の賭けがオッズを動かす効果も入らない（例は少額の単勝のみ）。実際の回収率の検証ではない。
- S1 は正規近似、S3・G3 は上下界の中点で、精度はジャンプの大きさしだい (p.1570)。
- 分数 Kelly の経路は効率的フロンティアと一致しない (p.1565-1566)。最適な動的戦略は別問題として残る。

## keiba-ai での使い方

- **分数 Kelly の係数を成長–安全の曲線で決める**: 係数 $c$ を 0.1〜1.0 で変えたバックテスト（時系列分割のテスト期間、確定オッズ・控除率込み）で、レースあたり平均対数成長率（G2）と「半減前に2倍になる確率」（S3、ブートストラップで推定）を並べ、Table 3 と同じ形の表を作る。
- **総賭け比率を先に決める**: Table 4 の結論（総額 > 配分）に従い、同時に多数のレースへ賭ける場合も、まず1日の総賭け比率の上限を決め、その中で配分する。仮説: 1日の総額を Kelly 合計の 0.25〜0.5 倍に抑えると、対数成長率の損失は小さくドローダウンは大きく減る。
- **モデル誤差の扱い**: 推定した勝率が過信気味なら名目の Kelly は実際には Kelly 超になり、支配される領域に入る。校正の悪いモデルほど最適な $c$ が小さくなるかを確かめる。
- 報告は回収率だけでなく、成長と安全の2軸で並べる。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 成長最大の極。
- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): Kelly の漸近最適性（Table 1 の出典）。
- [MacLean, Thorp, Ziemba 2010](./2010-maclean-kelly-good-bad-properties.md): 本論文を含む研究の要約。同じブラックジャックの表と 74% の例を再掲。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): 連続近似での分数 Kelly の成長率比 $c(2-c)$。
- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 本論文が競馬の優位の出典に挙げる複勝・3着内の非効率 (p.1578)。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): リスク中立の情報優位者の問題。
- [Busseti, Ryu, Boyd 2016](./2016-busseti-risk-constrained-kelly.md): ドローダウン確率を制約にした Kelly（安全性の別の定式化）。
- [Deza ほか 2015](./2015-deza-chance-constrained-parimutuel.md): 確率制約付きのパリミュチュエル賭け。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 確率推定の不確実性を入れた競馬の Kelly。
- [Ziemba 2023](./2023-ziemba-parimutuel-revisited.md): 半分 Kelly の目安とケンタッキーダービーでの資産推移。

## 検索語

成長と安全, 成長–安全トレードオフ, 分数 Kelly, ハーフ Kelly, 部分 Kelly, 資金管理, ドローダウン, 半減前に2倍, 初到達時間, 破産確率, 効率的フロンティア, ブラックジャック, 競馬, 複勝, 3着内, ロト, 人気のない数字, 年末効果, 1月効果, growth versus security, growth-security tradeoff, fractional Kelly, half Kelly, capital accumulation, probability of doubling before halving, first passage time, tradeoff theorem, dynamic investment analysis, blackjack, horseracing, place and show, lotto 6/49, turn of the year effect, MacLean Ziemba Blazenko, Kelly Capital Growth Investment Criterion

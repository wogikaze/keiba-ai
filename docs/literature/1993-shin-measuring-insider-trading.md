---
title: Measuring the Incidence of Insider Trading in a Market for State-Contingent Claims
authors: Shin Hyun Song
year: 1993
venue: The Economic Journal 103(420) 1141-1153
url: https://academic.oup.com/ej/article-abstract/103/420/1141/5157258
doi: 10.2307/2234240
topic: market-efficiency
tags: insider-trading, shin-model, bookmaker, implied-probability, favourite-longshot-bias, overround, shin-z, uk
verified: abstract
importance: medium
source: unavailable
source_version:
---

# 状態条件付き請求権の市場でインサイダー取引の割合を測る：Shin の z

> **原本未取得**。Economic Journal（OUP/JSTOR）で有料、ワーキングペーパー版は見つからなかった。本ノートは Sauer (1998)、Smith, Paton & Vaughan Williams (2006)、Whelan (2024, "On Estimates of Insider Trading in Sports Betting", 著者サイトで公開) の記述に基づく。ページは引用元のもの。

> 一言で: ブックメーカーのオッズの合計が1を超える分（オーバーラウンド）を出走頭数に回帰すると、その係数がインサイダーの資金の割合 $z$ を測る、という方法を提案し、英国の競馬で $z \approx 2$〜2.5% と推定した。この「Shin の z」はその後、オッズから勝率を出す方法（Shin 法）としても広く使われたが、近年は $z$ をインサイダーの量と読む解釈が強く批判されている。

## 背景

Shin (1991, 1992) は、結果を知るインサイダーが割合 $z$ でいるとき、ブックメーカーが付ける価格は本命-大穴バイアスを持ち、価格の合計が1を超えることを示した。本論文はそのモデルの検証可能な含意を取り出し、データから $z$ を推定する（Sauer 1998, p.2040）。

## モデルと推定式

Shin (1992) のモデルでは、真の勝率 $p_i$ の馬 $i$ の価格（1を受け取る権利の値段, オッズの逆数）は

$$\pi_i = \frac{\sqrt{z p_i + (1-z) p_i^2}}{\sum_j \sqrt{z p_j + (1-z) p_j^2}}\cdot \beta, \qquad \beta = \Big(\sum_j \sqrt{z p_j + (1-z)p_j^2}\Big)^2$$

の形になる（Whelan 2024, p.6, 式9–10 の表記を価格に直したもの）。価格の合計から1を引いた $D = \sum_i \pi_i - 1$ が市場のスプレッド（オーバーラウンド）である（Sauer 1998, p.2040）。

Shin (1993) はこの式をテイラー展開で近似し、$D$ を出走頭数 $n$ と勝率の散らばりで説明する回帰式を導いた（Whelan 2024, p.6）。

$$D_r = z\,(n_r - 1) + \sum_k a_k\, n_r^k\, \mathrm{Var}(p)_r + \sum_k b_k\, n_r^k\, [\mathrm{Var}(p)_r]^2$$

（Smith ら 2006, p.12, 式1。Shin 1993, p.1148 による）。$(n-1)$ の係数が $z$ で、正で小さければモデルが支持される（Sauer 1998, p.2041）。勝率の分散は観測できないので、まずレース内の価格の分散で代用して $z$ を推定し、それを使って分散を推定し直す反復最小二乗法を使う（Smith ら 2006, p.12）。

この方法の利点は、レースの結果（勝ち馬）を使わず、オッズだけで推定できることである。そのため少ないレース数でも適用できる（Smith ら 2006, p.12）。

## 推定結果

| 出典 | レース数 | 時期 | $z$ |
|---|---|---|---|
| Sauer (1998, p.2041) による要約 | 136 | 1991 年7月第1週, 英国 | 約 .02（有意） |
| Smith ら (2006, p.12) による要約 | 178 | 1990 年代初め | .025（賭け金の 2.5% がインサイダー由来） |

二次資料の間でレース数と推定値が食い違っている。原本で確認できていない（論文中に2つの標本がある可能性もある）。

## 後続の利用

- **Vaughan Williams & Paton (1997)**: 同じ回帰を使い、私的情報があまり重要でない上級のレースでは $D$ と $n$ に関係がないこと、オッズが大きく動くレースほどスプレッドが大きいことを示した。どちらもインサイダーの存在と整合的とされた（Sauer 1998, p.2041）。
- **Cain, Law & Peel (1997, 2001)**: ゼロ利益を仮定すると、レースごとにオッズだけから $z$ と各馬の $p_i$ を解けることを示した（Whelan 2024, pp.2, 6–7）。これが「Shin 法」として、ブックメーカーのオッズから勝率を出す標準的な方法の一つになった。
- **Law & Peel (2002)**: Shin の方法でインサイダーの可能性が高い馬券を取り出すと期待利益が正になる、と報告した（芦谷 2010, p.5）。
- **Smith ら (2006)**: ブックメーカーと賭け取引所（Betfair）で $z$ を比べ、取引所の方が本命-大穴バイアスが小さいことを示した。
- **Jullien & Salanié (1994)** は本論文へのコメント（*Economic Journal* 104, pp.1418–1419）を書いている。内容は未確認。

## 批判的に読む

- **$z$ はインサイダーの量か**。Whelan (2024) は、この推定方法が正確なのは非常に非現実的な条件の下だけで、インサイダーがいない現実的な設定でも $z$ は正に推定されやすいと示した。$z$ のばらつきは、インサイダー情報の量よりも、ブックメーカーの費用や競争の程度の違いを反映している可能性が高いと論じる（Whelan 2024, p.2 の要旨）。
- **オーバーラウンドの他の源**。ブックメーカーの利幅は、運営費・競争・リスク回避でも変わる。$D$ と $n$ の関係はそれらでも生じうる。
- **小標本**。1週間分・百数十レースでの推定である。
- **モデルの仮定**。インサイダーは結果を確実に知り、非インサイダーは確率に比例して1単位ずつ賭けるなど、極端な仮定の上に立つ（Sauer 1998, p.2040）。
- 原本未読のため、標準誤差、反復推定の収束の扱い、標本の詳細は未確認。

## keiba-ai での使い方

- **Shin 法を「オッズ→確率」の候補の一つとして比較する**。JRA の単勝はパリミュチュエルなので、Shin のモデルの前提（ブックメーカーがインサイダーに備える）は成り立たない。それでも Shin 法は「本命-大穴バイアスを1パラメータで補正する写像」として使える。比較対象: (a) 票数シェア $w_i$、(b) 単純正規化、(c) 累乗補正 $w_i^\alpha$、(d) Shin 法、(e) 等温回帰。評価は時系列で分割した検証データの log loss と較正誤差。仮説: JRA 単勝では (c)(d)(e) の差は小さく、(a) より良い。
- **$z$ をレースの特徴量にする**。レースごとの $z$（または補正の強さ）を、そのレースの「情報の非対称の大きさ」や「オッズの歪み」の代理として、モデルに入れる案がある。ただし Whelan の批判のとおり、意味はインサイダーではなく単なるオッズ分布の形の要約と考えるべきである。
- **海外競馬・固定オッズを扱う場合**。英国や豪州のブックメーカーのオッズを特徴量に使うなら、Shin 法での確率化を既定にしてよい（固定オッズでの標準的な処理）。

## 関連ノート

- [Shin 1991](./1991-shin-optimal-betting-odds-insiders.md): インサイダーに対する最適オッズの2頭モデル。本論文の理論の出発点。
- [Crafts 1985](./1985-crafts-insider-knowledge-britain.md): Shin が着想を得た英国のインサイダーの証拠。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Shin のモデルと本論文の推定を紹介。
- [Smith ら 2006](./2006-smith-person-to-person-betting.md): Shin の z をブックメーカーと賭け取引所の比較に使用。推定手順を詳しく説明。
- [Franck ら 2010](./2010-franck-bookmakers-vs-betting-exchange.md): ブックメーカーと賭け取引所の価格の比較。
- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 同じ著者の多結果の賭けの研究。
- [芦谷 2010](./2010-ashiya-longshot-bias-survey.md): Law & Peel による Shin の方法の応用を紹介。

## 検索語

Shin の z, Shin's z, Shin 法, Shin method, Shin モデル, インサイダー取引, insider trading, インサイダーの割合, incidence of insider trading, 状態条件付き請求権, state-contingent claims, ブックメーカー, bookmaker, オーバーラウンド, overround, 市場スプレッド, market spread, 控除, 出走頭数, number of runners, 反復最小二乗法, iterative OLS, オッズから確率, implied probability, 本命-大穴バイアス, favourite-longshot bias, FLB, 英国競馬, Cain Law Peel, Vaughan Williams Paton, Shin 1993, Economic Journal

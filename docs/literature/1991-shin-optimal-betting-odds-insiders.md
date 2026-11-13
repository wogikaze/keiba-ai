---
title: Optimal Betting Odds Against Insider Traders
authors: Shin Hyun Song
year: 1991
venue: The Economic Journal 101(408) 1179-1185
url: https://academic.oup.com/ej/article-abstract/101/408/1179/5190137
doi: 10.2307/2234434
topic: market-efficiency
tags: insider-trading, shin-model, bookmaker, favourite-longshot-bias, adverse-selection, monopoly-bookmaker, two-outcome
verified: abstract
importance: medium
source: unavailable
source_version:
---

# インサイダーがいるときのブックメーカーの最適オッズ：2頭立てのモデル

> **原本未取得**。Economic Journal（OUP/JSTOR）で有料、ワーキングペーパー版は見つからなかった。本ノートは要旨（EconPapers）と、モデルを一般化して再導出した Whelan (2023, "How does inside information affect sports betting odds?", UCD WP23/16, econstor で公開) の記述、Sauer (1998) の要約に基づく。式の番号とページは Whelan の WP のもの（「Whelan WP p.N」）。

> 一言で: 結果を知るインサイダーが一定割合いるとき、独占ブックメーカーが期待利益を最大にするオッズは真の確率から系統的にずれ、本命の勝つ見込みを過小に、大穴を過大に表す。ブックメーカー市場の本命-大穴バイアスを「インサイダーへの防衛」として説明する理論の出発点。ただし後の再検討では、この2頭立ての特殊ケースではインサイダーの割合はオッズの比に影響せず、バイアスを生んでいるのは非インサイダーの信念のばらつきだと指摘されている。

## 要旨（EconPapers）

一部が自分より優れた情報を持つ賭け手の集団に向かって、ブックメーカーが最適な価格を決める問題を調べる。中心的な結果は、正規化したオッズが真の勝率から系統的に乖離することである。その帰結として、オッズは本命の勝つ見込みを過小に、大穴の勝つ見込みを過大に表す。

## モデル（Whelan WP pp.8–10 による再構成）

- 2頭（2チーム）の競走。本命の真の勝率を $p \ge 0.5$ とし、ブックメーカーは $p$ を知っている。
- ブックメーカーは独占で、本命と大穴の配当倍率（小数オッズ）$O_F$, $O_L$ を決めて期待利益を最大化する。
- 賭けに回る資金を1に正規化し、割合 $z$ は結果を知るインサイダー（必ず勝ち馬に賭ける）が持つ。
- 残りは非インサイダーの連続体で、各人は1単位を賭けるか賭けないかを選ぶ。主観確率 $\tilde p$ は区間 $[A,B]$ 上の一様分布から独立に引かれ、期待収益が非負のときだけ賭ける。**Shin (1991) は $A=0, B=1$ と置いた**（Whelan WP p.9）。つまり非インサイダーの信念は真の確率と無関係である。

このとき最適オッズの比は、$A+B=1$ の場合

$$\frac{O_F}{O_L} = \sqrt{\frac{1-p}{p}}$$

になる（Whelan WP p.10, 式14）。Whelan によれば、これが Shin (1991) の示した本命-大穴バイアスの式である。期待収益が等しいならオッズの比は $(1-p)/p$ のはずだが、平方根が付くので本命のオッズが相対的に良くなる。例えば $p = 0.7$ なら、期待収益が等しい比は 0.43 だが、この式では 0.65 になる（Whelan WP p.11）。

## 何がバイアスを生んでいるか（後の再検討）

Whelan (2023) は、上の式に $z$ が含まれないことに注目する（Whelan WP p.10）。

> "the specific case it examined implied the fraction of wealth won by insiders had no impact on the relative odds." (Whelan WP p.10)

インサイダーは両方のオッズを同じ割合で下げる（オッズに関係なく賭けるので、需要の弾力性が下がり、ブックメーカーの上乗せが増える）。しかし比は変えない。バイアスを生むのは、非インサイダーの信念がばらつくことで、本命と大穴への需要の価格弾力性が違うことである（大穴への需要はオッズに鈍感）。さらに、非インサイダーの信念が真の確率の周りに集まる現実的な設定では、インサイダーの割合が増えたときのオッズの比の変化はごく小さく、$z$ が比較的小さい値を超えると、ブックメーカーの利益が負になって市場が成立しなくなる（Whelan WP pp.4–5）。

この再検討は、Shin のモデルを「インサイダーがバイアスを生む」証拠として引用する多くの文献（Ottaviani & Sørensen 2008、Snowberg & Wolfers 2008 のサーベイなど）への重要な注意である（Whelan WP p.4）。

## n 頭への拡張（Shin 1992）との関係

Shin (1992, *Economic Journal* 102, pp.426–435）は $n$ 頭の競走に拡張した。市場構造について、Sauer (1998, p.2039) は「競争均衡」、Whelan (2024, "On Estimates of Insider Trading in Sports Betting", p.2) は「独占ブックメーカー」と書いており、原本で確認できていない。Sauer (1998, p.2040) の簡略版では、ブックメーカーが確率 $z$ でインサイダーと取引するとき、価格（勝ったら1を払う権利の値段）は

$$\pi_i^* = A_i \sum_s A_s, \quad A_i = \sqrt{z p_i + (1-z) p_i^2}$$

となる。$z>0$ なら価格の合計は1を超え（オーバーラウンド）、正規化した価格は大穴を過大に、本命を過小に評価する。例えば $p = (.25, .75)$, $z = .05$ なら正規化価格は (.2617, .7384)（Sauer 1998, p.2040）。$z$ が大きすぎると、どの価格でもブックメーカーの利益が負になり市場が成立しない（Sauer 1998, 脚注36）。Whelan は 1992 年版のモデルも、インサイダーによるバイアスの説明としては説得力に欠けると論じている（Whelan WP p.20 以降）。

## 背景

Asch, Malkiel & Quandt (1982) と Crafts (1985) が情報を持つ賭け手の証拠を出したのを受けて、Shin は一連の論文（1991, 1992, 1993）で、ブックメーカー市場ではインサイダーの存在が本命-大穴バイアスを生むことを示した（Jullien & Salanié 2005 の IDEI 草稿, p.6 の整理）。パリミュチュエルにはこの経路がない（Sauer 1998, p.2042）。

## 批判的に読む

- **信念の仮定が強い**。非インサイダーの主観確率が [0,1] 上の一様分布で真の確率と無関係という仮定は、賭け手に大きな損失を生み、現実的でない（Whelan WP p.4）。
- **独占ブックメーカー**。1991 年版は独占を仮定する。競争的な市場（1992 年版）とは別のモデルである。
- **2頭立て**。競馬の多頭立てへの含意は 1992 年版に頼る。
- 原本未読のため、インサイダーの富や情報の価値についての命題、証明の細部は未確認。

## keiba-ai での使い方

- **JRA には直接当てはまらない**。JRA はパリミュチュエルで、ブックメーカーがインサイダーに備えてオッズを決める経路はない。本命-大穴バイアスの説明としては、パリミュチュエル向けの説明（信念の異質性、知覚の歪み、控除率による裁定の限界）を優先する。
- **オッズから確率への写像として使う**。ブックメーカーのオッズ（海外競馬や賭け取引所との比較を将来扱う場合）から勝率を出すとき、単純な正規化 $1/O_i / \sum_j 1/O_j$ ではなく、Shin の式を逆に解いた確率（いわゆる Shin 法）を使う選択肢がある。仮説: 英国 SP のような固定オッズでは、Shin 法の確率の方が単純正規化より log loss が小さい。
- **教訓**。バイアスの式が「誰の行動」から生じたかは、モデルの仮定次第で入れ替わる。オッズ補正の関数形を選ぶときは、理論的な由来より、時系列で分割した検証データでの較正で決める。

## 関連ノート

- [Shin 1993](./1993-shin-measuring-insider-trading.md): このモデルの検証可能な含意から、インサイダーの割合 $z$ を推定した続編。
- [Crafts 1985](./1985-crafts-insider-knowledge-britain.md): 英国ブックメーカー市場のインサイダーの証拠。Shin のモデルの着想源。
- [Asch ら 1982](./1982-asch-racetrack-informed-behavior.md): 情報を持つ賭け手の米国での証拠。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): 信念の異質性によるバイアスの導出。Whelan はバイアスの真の源がこちらの仕組みだと論じる。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Shin (1992) のモデルを式3–4で紹介。
- [Smith ら 2006](./2006-smith-person-to-person-betting.md): Shin の $z$ をブックメーカーと賭け取引所の比較に使用。
- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 同じ著者による多結果の賭けの価格付けの研究。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): Shin を情報の非対称による説明の代表として挙げる。

## 検索語

Shin モデル, Shin model, Shin 法, Shin's method, インサイダー, insider trading, insider traders, 情報の非対称, asymmetric information, 逆選択, adverse selection, ブックメーカー, bookmaker, 固定オッズ, fixed odds, 独占ブックメーカー, monopoly bookmaker, 最適オッズ, optimal odds, オーバーラウンド, overround, 本命-大穴バイアス, favourite-longshot bias, FLB, 需要の価格弾力性, 信念の異質性, 2頭立て, two-horse race, 正規化オッズ, implied probability, Shin 1991, Economic Journal, Whelan

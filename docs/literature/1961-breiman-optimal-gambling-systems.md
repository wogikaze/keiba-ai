---
title: Optimal Gambling Systems for Favorable Games
authors: Breiman Leo
year: 1961
venue: Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability Vol. 1 pp. 65-78
url: https://projecteuclid.org/euclid.bsmsp/1200512159
doi:
topic: betting-strategy
tags: kelly, log-optimal, asymptotic-optimality, martingale, wald-identity
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# 有利なゲームでの最適な賭け方：$E\log S_n$ 最大化戦略の漸近最適性

> 一言で: 有利なゲームを繰り返すとき、毎回 $E\log$ を最大化する固定比率の戦略 $\Lambda^*$ は、「目標額に到達するまでの期待回数」でも「$n$ 回後の資産の大きさ」でも漸近的に最良である。Kelly (1956) が「固定比率の戦略同士」に限って示した優越を、過去に依存する任意の戦略に広げた。

原本は UC Berkeley 図書館デジタルコレクションの PDF（14ページ、プロシーディングスの頁番号 65–78）。シンポジウム自体は1960年6–7月開催。以下のページは頁番号 65–78 で書く。

## 設定

結果 $X\in\lbrace 1,\dots,s\rbrace $、$P\lbrace X=i\rbrace =p_i$。賭けの対象は部分集合 $A_1,\dots,A_r$ で、$A_j$ に賭けた1単位は $X\in A_j$ のとき $o_j$ 返ってくる (p.65)。部分集合で書くので、単勝（互いに排反）だけでなく、複勝のように重なる賭けも同じ枠で扱える。手元に残す資金は「$A_1=I$, $o_1=1$」という賭けとして表現できるので、常に全額を配分すると仮定してよい (p.65)。

ゲームが**有利（favorable）**とは、ある戦略で $S_n\to\infty$（概収束）となること (p.65)。

戦略 $\Lambda$ は、各回の配分比率 $\lambda^{(n+1)}$（合計1）を過去の結果 $R_n$ に依存してよい (p.67)。1回の資産倍率を $V_n$、$W_n=\log V_n$ とすると $\log S_n=W_1+\dots+W_n$ (p.67, (2.3))。

$$W(\lambda)=\sum_i p_i\log\Big(\sum_{j:\,i\in A_j}\lambda_j o_j\Big), \quad W=\max_\lambda W(\lambda)$$

最大点 $\lambda^*$ を毎回使う戦略が $\Lambda^*$ である (p.67–68, (2.4))。

## 主要な結果

| 結果 | 内容 | ページ |
|---|---|---|
| 命題1 | $W(\lambda)$ の最大点が複数あっても、各結果での払戻 $\sum_{i\in A_j}\lambda_j o_j$ は一意。$\Lambda^*$ の $W_k$ は i.i.d. | p.67–68 |
| 命題2 | $A_j$ が互いに排反なら、オッズに関係なく $\lambda_j^*=P\lbrace X\in A_j\rbrace $ | p.68 |
| 命題3 | ゲームが有利 $\iff W>0$ | p.68 |
| 定理1 | 目標額 $x\to\infty$ で、任意の戦略の期待到達回数 $ET(x)$ と $ET^*(x)$ の差は非負の量に収束し、$\Lambda^*$ と同値な戦略でのみ0。逆向きの差 $ET^*(x)-ET(x)$ は $x$ と戦略によらない定数で抑えられる | p.68 |
| 定理2 | 任意の戦略で $\lim S_n/S_n^*$ が概収束し、その期待値は1以下 | p.72 |
| 定理3 | $\Lambda^*$ から漸近的に離れ続ける戦略は $S_n/S_n^*\to 0$（無限に劣る） | p.73 |
| 定理4 | コイン投げで「$n$ 回後に目標額を超える確率」を最大化する最適戦略の確率と、$\Lambda^*$ の確率の差は $n\to\infty$ で一様に0に近づく | p.77 |

命題2は Kelly (1956) の「掲示オッズを無視して自分の確率どおりに賭ける」結果の一般化である（控除なしで、保留を賭けとして表現できる場合）。

Breiman は $\Lambda^*$ の性格を次のようにまとめている (p.66)。

> It is a conservative policy which consists in betting fixed fractions of the available fortune on the various A_i.

同じ段落で、最大期待値の1点に賭けるのではなく、多くの $A_j$ に分散する戦略だとも述べている (p.66)。コイン投げなら「毎回資産の $p-q$ を表に賭ける」(p.66, p.77)。

## 証明の道具

- 定理1は Wald の恒等式の「超過量（excess）」の漸近評価が中心で、再生定理と Blackwell の手法を使う (p.69)。$W_k$ が非格子（nonlattice）であることを仮定する。有理数のオッズと確率でも $\log V$ は通常非格子になる、と注記している (p.68)。
- 定理2・3はマルチンゲール収束定理による (p.73)。
- 定理2・3は有利なゲームでなくても成り立つ (p.72)。

## 未解決として残したこと

- 有限の目標額 $x$ で期待到達回数を最小化する戦略は解けていない。予想として「資産がある閾値 $\xi_0$ 未満なら $\Lambda^*$、以上なら勝てばちょうど目標に届く額を賭ける」を挙げている (p.78)。
- Dubins and Savage の未刊原稿（後の *How to Gamble If You Must*）に優先権があることを認め、一部の命題（命題3）がほぼ重複すると明記している (p.66–67)。きっかけは Kelly (1956) だったと書いている (p.67)。

## 批判的に読む

- 確率 $p_i$ とオッズ $o_j$ は既知で、各回の試行は独立同分布と仮定している。競馬では毎レース確率もオッズも変わる。ただし定理2・3は各回のゲームが異なる場合への拡張が自然で、実務ではこの拡張された形で引用されることが多い（本論文での明示的な扱いは未確認）。
- 「漸近的に最良」は無限回の試行での主張である。有限回では、定理4の意味で近いという保証しかなく、短期の破産確率やドローダウンは別問題として残る。この点が後の分数 Kelly 研究の出発点になる。
- 推定誤差の扱いは無い。$p_i$ を推定値で置き換えた場合の最適性は保証されない。

## keiba-ai での使い方

- **重なる券種への Kelly の一般化の根拠**: $A_j$ を部分集合で書く定式化により、単勝・複勝・ワイドなど同時に当たりうる券種を1つの最適化問題として扱える。$W(\lambda)$ は凹関数なので、凸最適化ソルバーで解ける。資金配分モジュールの目的関数をこの形で実装するのが素直である。
- **「有利かどうか」の判定**: 命題3より、推定確率とオッズで $W>0$ となるレースだけが賭ける対象になる。仮説: レースごとに $W$ を計算し、$W$ の大きさでレースを選別すると、一律に賭けるより対数成長率が改善する。
- **評価指標**: 定理2・3は「対数資産の差」で戦略を比べることを正当化する。バックテストでは回収率に加えて $\sum\log V_n$ を主要指標に置く。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 出発点。Kelly が未証明とした時間依存戦略に対する優越を本論文が証明。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): Breiman の結果を実務向けに解説し、ブラックジャックやスポーツに適用。
- [MacLean, Thorp, Ziemba 2010](./2010-maclean-kelly-good-bad-properties.md): 漸近最適性（良い性質）と短期リスク（悪い性質）の整理。
- [MacLean, Ziemba, Blazenko 1992](./1992-maclean-growth-versus-security.md): 有限期間での成長と安全性のトレードオフ。
- [Whitrow 2007](./2007-whitrow-simultaneous-bets-allocation.md): 多数の同時の賭けへの $E\log$ 最大化の数値解法。
- [Jacot, Mochkovitch 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): 排反でない賭けでの Kelly（本論文の部分集合の定式化に対応）。

## 検索語

Breiman, 有利なゲーム, 最適賭け戦略, 対数最適, 漸近最適性, 目標到達時間, 期待到達回数, Wald の恒等式, マルチンゲール, 固定比率戦略, 分散投資, favorable game, optimal gambling system, log-optimal strategy, growth optimal, Kelly criterion, asymptotic optimality, minimal expected time, magnitude problem, Dubins Savage, fractionalizing strategy

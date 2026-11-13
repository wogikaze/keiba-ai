---
title: Optimal Horse Race Bets
authors: Isaacs Rufus
year: 1953
venue: American Mathematical Monthly 60(5) 310-315
url: https://www.semanticscholar.org/paper/Optimal-Horse-Race-Bets-Isaacs/799c11ef15de20c5b9f67979da8e7cf2dd133b7b
doi: 10.1080/00029890.1953.11988295
topic: betting-strategy
tags: parimutuel, market-impact, expected-profit, win-bet, informed-bettor, monopoly
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# パリミュチュエル単勝の最適賭け金：自分の賭けで配当が下がる場合の期待利益最大化

> 原本は書籍『Efficiency of Racetrack Betting Markets』2008 年版への再録（書籍 pp.93-98）を、pdfcoffee.com 上の抽出テキストで読んだ。ページは書籍のもので、元の American Mathematical Monthly のページ（310-315）とは異なる。抽出テキストは OCR 由来で、数式の大半が崩れている。p.98（第4節「Some ramifications」の後半）は抽出テキストに含まれていない。以下の式は、崩れた本文と論文の数値例から再構成し、数値例で検算したものである。

> 一言で: 真の勝率を知る1人の賭け手が、他人の単勝票を所与として、自分の賭けが配当を下げることを考慮して期待利益を最大化する問題を、閉形式で解いた。賭けるのは「勝率 ÷ 他人の票」の比が大きい馬の上位集合で、全馬に賭けることは決してない。

## 既存ノート（二次資料版）から原本で直した点

- 二次資料版は Sauer (1998) の3頭立て・控除なしの例だけで式を説明していた。原本は $n$ 頭立て・控除率込みの一般の問題を解き、**どの馬に賭けるかの判定手順と各馬の賭け金の閉形式**を与えている (p.94-97)。
- 二次資料版の「最後の1円の期待利益をゼロにする手前で止める」は Ottaviani & Sørensen と Ashiya の解釈である。原本の最適条件は「賭け金を全体として増やしても期待利益が増えない点」で、各馬への賭け金はその一次条件から決まる（下のモデル節）。解釈として矛盾はないが、原本にその言い回しはない。
- 原本の数値例（5頭立て、控除 10%）では、勝率が最も高い馬（勝率 .4）には賭けない (p.93, p.97)。「本命に賭ける」話ではなく、**勝率と他人の票の比**で選ぶ話である。
- 著者が RAND Corporation 所属であることは原本で確認した (p.93)。

## 問題（p.93-94）

記号:

- $p_j$: 馬 $j$ の真の勝率（自分は知っている）
- $s_j$: 自分以外が馬 $j$ に賭けた額（$s_j>0$）
- $x_j$: 自分の賭け金
- $Q$: 払戻率（$0<Q<1$、1 − 控除率）

賭け金の総額 $S+X$（$S=\sum s_j$、$X=\sum x_j$）に $Q$ を掛けた額が、勝ち馬に賭けた人に賭け額に比例して配られる。自分の期待利益は

$$F(x)=Q(S+X)\sum_j \frac{p_j x_j}{s_j+x_j}-X$$

で、これを $x_j\ge 0$ の範囲で最大化する (p.93-94)。

著者は導入で、方針自体は競馬で言う「オーバーレイ」（群衆が勝率を見誤った馬を買う）で新しくなく、新しいのは厳密解だと書いている (p.93)。

> What we believe is new is the exact solution. (p.93)

## 解（p.94-97）

1. **賭ける価値があるか**（Lemma 1）。ある馬で $Q p_j S/s_j>1$、つまり控除後の払戻を他人の票だけで計算した期待値が1を超えるなら、期待利益の正の最大値がある (p.94)。
2. **全馬には賭けない**（Lemma 2）。全馬に正の額を賭ける点を一次条件に入れると、期待利益の傾きが $Q-1<0$ になり、最大にならない (p.95)。
3. **馬の順位づけ**。比 $\rho_j=p_j/s_j$（勝率 ÷ 他人の票）で馬を並べる。最適解で賭けるのは、ある順位 $t$ 以上の馬すべてで、それより下の馬には賭けない（Lemma 3）(p.95)。
4. **賭け金の閉形式**。賭ける馬の間では一次条件から $p_i s_i/(s_i+x_i)^2$ が等しくなる (p.94)。これを解くと、賭ける馬の集合を $T$ として

$$x_i=\lambda\sqrt{p_i s_i}-s_i,\qquad \lambda^2=\frac{Q\,S_{\bar T}}{1-Q\,P_T}$$

になる。$S_{\bar T}$ は賭けない馬への他人の票の合計、$P_T$ は賭ける馬の勝率の合計（この $\lambda$ の形は崩れた式 (10) から再構成し、下の数値例で検算した）。
5. **$t$ の決め方**（Lemma 4・5）。$\rho$ の大きい順に馬を1頭ずつ加え、加えた馬で $x_i>0$（すなわち $\rho_i>1/\lambda^2$）が成り立つかを順に確かめる。最初に成り立つところで $t$ と $\lambda$ が決まる (p.96-97)。

補足として、他人の票が 0 の馬があると最適解が存在しないことがある（上限には近づけるが達しない）(p.97)。

## 数値例（p.93, p.97）

| 馬 | 勝率 | 他人の票 | $\rho=p/s$ | 最適な賭け金（$Q=0.9$） |
|---|---|---|---|---|
| A | .4 | 1,000 | .00040 | 0 |
| B | .2 | 350 | .00057 | 28.40 |
| C | .2 | 300 | .00067 | 50.33 |
| D | .1 | 250 | .00040 | 0 |
| E | .1 | 100 | .00100 | 43.02 |

合計 2,000 ドル。抽出テキストでは B の票が「330」と読めるが、論文の賭け金（28.40、50.33、43.02）を上の式で再現できるのは 350 のときなので 350 とした。$T=\{B,C,E\}$ では $P_T=.5$、$S_{\bar T}=1{,}250$、$\lambda^2=0.9\times1250/(1-0.45)\approx 2045$ で、3つの賭け金が論文の値と一致する。

控除を無視すれば E が最良の投資（勝率 .1 で配当 20 倍）だが、E に多く賭けると自分の票で配当が下がり、他の馬の方が有利になる (p.93)。だから最適解は複数の馬への分散になる。

## 位置づけ

- 著者は、この問題が当時の非線形計画法に近く、アルゴリズムと閉形式で解けるのは珍しいと書く (p.93)。第4節では Thrall による変形と、商品の価格付け（merchandising economics）への応用に触れる (p.97)。続きの p.98 は未確認。
- 書籍の編者序文は、本論文を規範的（normative）分析の出発点と位置づけ、後続研究は (1) 対数効用（Kelly）への拡張、(2) 勝率の推定、(3) 複勝・連勝への拡張の3方向だとまとめる (書籍 p.87)。
- 同書の Kallberg & Ziemba の章は、勝率が票数シェアでよく推定される（Snyder 1978）以上、Isaacs の「賭ける価値がある」条件が満たされることはまれだと指摘する (書籍 p.102)。

## 批判的に読む

- **自分が最後に賭ける前提**。他人の票を確定値として扱うので、締切直前に自分だけが賭ける状況を想定している。実際は締切後もオッズが動く。著者も導入で、実用には大口の資金と優れた予想屋と締切直前の素早い計算が要ると皮肉っている (p.93)。
- **リスク中立**。期待利益の最大化で、資金に対する比率や破産は考えない。対数効用への拡張は Kelly・Breiman の系譜（MacLean ら）。
- **真の勝率を既知とする**。勝率の推定誤差があると、$\rho$ の順位と $\lambda$ が両方ずれる。
- **単勝のみ**。複勝・連勝への拡張は Hausch, Ziemba, Rubinstein (1981)。

## keiba-ai での使い方

- **自分の賭けを含めた期待値**。JRA もパリミュチュエルなので、賭け金が売上に比べて無視できないレース（地方、少頭数、新馬戦）では、上の $F(x)$ で期待利益を計算する。
- **賭ける馬の選び方の基準**。モデルの勝率 $p$ と単勝票 $s$ から $\rho=p/s$ を作ると、それは「モデル勝率 ÷ 票数シェア」に比例し、期待値の比と同じ順位になる。Isaacs の手順は、期待値の高い順に馬を加え、自分の票の影響を考えた賭け金が正である限り続ける、という形で実装できる。
- **賭け金の上限**。$x_i=\lambda\sqrt{p_i s_i}-s_i$ は、期待利益を最大にする賭け金の上限として使える。仮説: 通常の資金規模ではこの上限は効かないが、売上の小さいレースや低オッズの馬では Kelly の賭け金より小さくなることがある。バックテストでは確定オッズに自分の賭けを足して配当を再計算し、上限を超えた分を除いた回収率も出す。
- **確定オッズでのバックテストの楽観度**。Isaacs の前提（自分が最後）を崩す締切後のオッズ変動を、締切前オッズと確定オッズの差で測る。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 対数成長率の最大化。自分の賭けがオッズを動かさない前提。
- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): Kelly 基準の漸近的な最適性。編者序文が挙げる拡張の1つ目。
- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 自分の賭けによる配当低下を入れた最適化を複勝・3着内に拡張。
- [MacLean, Ziemba, Blazenko 1992](./1992-maclean-growth-versus-security.md): 成長と安全性のトレードオフ。リスク回避を入れた分析。
- [Snyder 1978](./1978-snyder-efficient-markets-horse-racing.md): 単勝市場がほぼ効率的なので Isaacs の条件はまれにしか満たされない、という指摘の根拠。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): 3頭立ての数値例で本論文を解説した総説。
- [Ottaviani, Sørensen 2010](./2010-ottaviani-noise-information-flb.md): FLB の代替説明（独占的な情報優位者が賭けを控える）として位置づけ。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 「大口投資家の独占力」として紹介。
- [Deza ほか 2015](./2015-deza-chance-constrained-parimutuel.md)、[Deza ほか 2017](./2017-deza-exotic-wagering-losses.md): 競馬の最適化研究の起点として引用。
- [Smoczynski, Tomkins 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 単勝の Kelly の明示解（期待利益ではなく対数効用）。

## 検索語

Isaacs, Rufus Isaacs, RAND, 最適賭け金, パリミュチュエル, 単勝, 期待利益最大化, 閉形式解, マーケットインパクト, 自己影響, 配当低下, オーバーレイ, overlay, 情報優位者, 独占, 非線形計画法, 勝率と票の比, 賭ける馬の選択, optimal horse race bets, parimutuel, win pool, expected profit maximization, market impact, price impact, informed bettor, monopolist bettor, favorite-longshot bias, Efficiency of Racetrack Betting Markets, American Mathematical Monthly

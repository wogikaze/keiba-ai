---
title: Optimal Horse Race Bets
authors: Isaacs Rufus
year: 1953
venue: American Mathematical Monthly 60(5) 310-315
url: https://www.semanticscholar.org/paper/Optimal-Horse-Race-Bets-Isaacs/799c11ef15de20c5b9f67979da8e7cf2dd133b7b
doi: 10.1080/00029890.1953.11988295
topic: betting-strategy
tags: parimutuel, market-impact, expected-profit, win-bet, informed-bettor, monopoly
verified: metadata
importance: high
source: unavailable
source_version:
---

# パリミュチュエル単勝の最適賭け金：自分の賭けで配当が下がる場合の期待利益最大化

> 原本未取得。American Mathematical Monthly（Taylor & Francis / JSTOR）は購読制で、OpenAlex・Semantic Scholar にも OA 版が無かった。本ノートは、この論文を引用している原本取得済みの文献（Sauer 1998、Ottaviani and Sørensen 2010、Deza ほか 2015・2017、Ashiya 2010）の記述だけに基づく。式の具体形は未確認。

> 一言で: 真の勝率を知る1人の賭け手が、他の賭け手の投票を所与として単勝プールに賭けるとき、自分の賭けが配当を下げることを考慮した期待利益最大化の賭け金を閉形式で与えた。最適解では、最後の1円の期待利益をゼロにする手前で止める。

## 何を解いたか（二次資料から）

- 競馬の最適化研究の出発点で、期待利益を最大化する単勝の最適賭け金の閉形式解を導いた (Deza ほか 2015, p.1; Deza ほか 2017, p.2)。
- 設定は「正しい確率と他の賭け手の投票を知る、1人の情報優位な賭け手」で、目的は期待利益の最大化 (Sauer 1998, p.6)。
- Sauer の要約では、一般の賭け手の投票シェアを $s_i$、払戻率を $Q$（1 − 控除率）、真の勝率を $p_i$ とすると、$Qp_i/s_i>1$ の馬には常に正の額を賭けるのが最適になる (Sauer 1998, p.6)。
- 独占的な情報優位者は、限界の賭けの期待収益をゼロにしない。それをすると、それまでに賭けた分（inframarginal bets）の収益まで壊すからである (Ottaviani and Sørensen 2010, p.25)。Ashiya はこれを独占企業になぞらえ、本命馬でも「追加的な 1 円」の期待利益率がゼロになる手前で買うのをやめる必要があるとまとめている (Ashiya 2010, p.8)。

## 数値例（Sauer 1998 による例示）

Sauer は Isaacs の問題を次の例で説明している (Sauer 1998, p.6)。3頭立て、控除なし、色の好みで $N$ 人が1ドルずつ均等に賭ける（各馬 $N/3$）。実はある馬 $k$ の勝率が $2/3$ だと知る賭け手が $x$ を賭けると、期待利益は

$$E\Pi = p\frac{N+x}{N/3+x}x - x$$

で、最適は $x^*=N/3$。このとき馬 $k$ への1ドルの期待払戻は $4/3$ になり、市場は非効率に見える。情報優位者が自分の配当低下を考慮して賭けを控えるため、価格に情報が完全には織り込まれない、という例である。

## FLB の説明としての位置づけ

Ottaviani and Sørensen (2010) は FLB の代替説明の一つとして Isaacs を挙げる (p.25)。独占的な情報優位者が賭けを控えるので、本命（真の勝率が高い馬）が過小に賭けられたまま残り、本命の期待収益が高くなる。Griffith (1949) の確率の誤認、Weitzman (1965) のリスク愛好、Ali (1977) の信念の異質性と並ぶ説明である。

## 批判的に読む

- **自分が最後に賭けるという仮定**: 他の賭け手の投票を所与とするので、締切直前に自分だけが賭けることを想定している。実際は締切後もオッズが動く（自分の後に他人が賭ける）ので、最適性は保証されない。
- **リスク中立**: 期待利益の最大化で、資金に対する比率や破産は考えない。資金の制約やリスク回避を入れた分析は MacLean, Ziemba, Blazenko (1992) にあると Sauer は注記する (Sauer 1998, p.6, 注10)。
- **単勝のみ**: 連勝式や複勝は扱わない（二次資料の範囲では）。
- 二次資料によれば RAND 在籍中の仕事とされるが、本ノートでは未確認。

## keiba-ai での使い方

- **マーケットインパクトの考慮**: JRA の単勝もパリミュチュエルなので、賭け金を増やすと自分の配当が下がる。1レースあたりの賭け金が売上に比べて無視できない場合（新馬戦、地方、少頭数など）、Kelly 配分の前に「自分の賭けを加えた後のオッズ」で期待値を再計算する。
- **賭け金の上限の目安**: 期待利益の最大化でも賭け金には内点解がある。Sauer の例の形（$E\Pi=pQ\frac{W+x}{W_i+x}x-x$、$W$ は総額、$W_i$ はその馬への総額）を各馬で解けば、レースごとの「これ以上賭けると期待利益が減る額」が出る。仮説: この上限は単勝売上の数% 程度で、通常の資金規模では問題にならないが、オッズの低い本命では早く効く。
- **締切後のオッズ変動**: Isaacs の仮定（自分が最後）を崩す要因として、締切前オッズと確定オッズの差を測る。差の分布はバックテストで「確定オッズで回収率を計算する」ことの楽観度を示す。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 同時期の対数成長率最大化。自分の賭けがオッズを動かさない前提。
- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 自分の賭けによる配当低下を入れた Kelly 型最適化（複勝・3着内）。
- [MacLean, Ziemba, Blazenko 1992](./1992-maclean-growth-versus-security.md): リスク回避を入れた分析（Sauer の注による）。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Isaacs の問題を数値例で解説した総説。
- [Ottaviani, Sørensen 2010](./2010-ottaviani-noise-information-flb.md): FLB の代替説明として Isaacs を位置づけ。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 「大口投資家の独占力」として紹介。
- [Deza ほか 2015](./2015-deza-chance-constrained-parimutuel.md)、[Deza ほか 2017](./2017-deza-exotic-wagering-losses.md): 競馬の最適化研究の起点として引用。
- [Griffith 1949](./1949-griffith-odds-adjustments.md): FLB の別の説明（確率の誤認）。
- [Smoczynski, Tomkins 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 単勝の Kelly の明示解（期待利益ではなく対数効用）。

## 検索語

Isaacs, 最適賭け金, パリミュチュエル, 単勝, 期待利益最大化, マーケットインパクト, 自己影響, 配当低下, 情報優位者, 独占, 限界賭け, 本命・大穴バイアス, optimal horse race bets, parimutuel, win pool, expected profit maximization, market impact, price impact, informed bettor, monopolist bettor, inframarginal bets, favorite-longshot bias, RAND

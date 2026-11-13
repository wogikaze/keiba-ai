---
title: Kelly criterion and fractional Kelly strategy for non-mutually exclusive bets
authors: Jacot Benjamin P., Mochkovitch Paul V.
year: 2023
venue: Journal of Quantitative Analysis in Sports 19(1) 37-42
url: https://www.degruyter.com/document/doi/10.1515/jqas-2020-0122/html?lang=en
doi: 10.1515/jqas-2020-0122
topic: betting-strategy
tags: kelly, fractional-kelly, multiple-bet-types, horse-racing, constrained-programming
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 複数券種を同時に買う Kelly：払戻行列で書き直し、fractional Kelly を「成長率の何割を残すか」で定義し直す

> 一言で: 単勝・複勝・馬連などを1レースで同時に買うと、1つの着順結果で複数の賭けが当たる（相互排他でない）。結果ごとの払戻ベクトル $r_i$ を使えば Kelly の目的は $\sum_i p_i\log(1 + r_i^\top a)$ と簡潔に書け、信頼領域法で解ける。さらに fractional Kelly を「成長率の k 割を保つ最小の賭け総額」と定義し直した。6ページの短い理論ノートで、実データの検証はない。

原本は出版社版（ドイツ国立図書館 d-nb.info に置かれた PDF）。

## 背景

競馬の Kelly 研究は単勝（[Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md)）や4連単（[Deza 2015](./2015-deza-chance-constrained-parimutuel.md)）のように1つの券種に限られ、複数の券種を1レースで組み合わせる包括的な扱いがなかった (p.37)。

## モデル

### 単一の賭けと fractional Kelly の効率

勝率 $p$、勝ったときのリターン $r^+$、負ければ −100% の賭けで、最適な賭け割合は $a^* = p - q/r^+$ (p.38, 式5)。
成長率の比 $k = G_\infty(a_f)/G_\infty(a^*)$ を定義すると、$a_f/a^* = 0.5$ で $k \approx 0.75$、$a_f/a^* = 0.33$ で $k \approx 0.55$ (p.38, 式6)。半分 Kelly でも最大成長率の 75% が残る。成長率が凹関数だから、縮めた割合ほどには成長率が落ちない。

### 相互排他な賭け（単勝）

$G_\infty(a) = \sum_i p_i\log(b + a_i(1 + r_i^+))$、$b = 1 - \mathbf{1}^\top a$ は賭けない分 (p.38, 式7-8)。KKT 条件から閉形式の解が出る（Kempton 2011）(p.39)。

### 相互排他でない賭け（複数券種）

- $n$ 個の結果（1〜3着の順列）と $m$ 個の賭け（券種×買い目）。$m > n$ になりうる (p.39)。
- 結果 $i$ のときの各賭けのリターンを並べたベクトル $r_i = (r_{i,j})_{1\le j\le m}$。当たった賭けは正、外れは −100% (p.39, 式10)。
- 目的関数は $G_\infty(a) = \sum_i p_i\log(1 + r_i^\top a)$ (p.39, 式12)。
- 勾配 $\nabla G = \sum_i p_i r_i/(1 + r_i^\top a)$、ヘッセ行列 $-\sum_i p_i r_i r_i^\top/(1 + r_i^\top a)^2$ (p.39, 式13-14)。
- 制約は $1 + r_i^\top a > 0$、$a \ge 0$、$\mathbf{1}^\top a \le 1$ (p.39, 式15)。凹関数の最大化なので KKT 条件が成り立つが、閉形式は面倒なので数値解法（SciPy の信頼領域法）を使う (p.39-41)。

### fractional Kelly の再定義

複数の賭けがあると、各賭けを何倍に縮めればよいかが自明でない。そこで

$\min_a \mathbf{1}^\top a$ s.t. $G_\infty(a)/G_\infty(a^*) \ge k$, $a \ge 0$

と定義する (p.39, 式9)。成長率を k 割以上保ちつつ、賭け総額を最小にする。

## 例

2つの賭け、2つの結果（コイン投げ）(p.40-41, Table 2):

| ケース | p | 賭け1 $(r^+, r^-)$ | 賭け2 | $a^*$ | $a_f$ (k=0.75) |
|---|---|---|---|---|---|
| (a) | 50% | (100%, −100%) | (100%, −100%) | (0, 0) | (0, 0) |
| (b) | 60% | (100%, −100%) | (100%, −100%) | $a_1+a_2 = 20\%$ | 合計 10.1% |
| (c) | 50% | (100%, −80%) | (120%, −100%) | (12.5%, 0) | (6.2%, 0) |

2つの賭けのリターンが比例する（$r_1^+ r_2^- = r_2^+ r_1^-$）ときは最適解が一意でない。比例しなければ解は境界にあり、有利なほうの賭けだけが残る (p.40)。

2つの賭け、3つの結果（Table 3, p.41）: 結果1（確率60%）で両方当たり（リターン 200% と 100%）、結果2（20%）で両方外れ、結果3（20%）で賭け2だけ当たる（100%）。Kelly 解は $a^* = (20\%, 40\%)$、k = 0.75 の fractional 解は $(16.3\%, 14.5\%)$。**最も多く賭ける対象が Kelly と fractional で入れ替わる** (p.41)。つまり一律に縮める従来の fractional Kelly とは違う配分になる。

## 批判的に読む

- **実データの検証も、他手法との比較もない**。例は2つの賭けの小さな数値例だけ。
- 「成長率の k 割を保つ」fractional Kelly が、一律縮小よりドローダウンや推定誤差に対して良いかは示されていない。賭け総額を最小にするという目的は直感的だが、リスクを直接測っていない。
- 確率 $p_i$ と各券種の払戻の推定が難しいこと、他の参加者の賭けでオッズが変わること、同じ戦略の参加者が締切直前に集まるノイズを、著者自身が限界として挙げる (p.41)。
- 定式化自体は [Busseti 2016](./2016-busseti-risk-constrained-kelly.md) の「一般の有限結果」の場合と同じで、新しいのは fractional Kelly の再定義の部分。

## keiba-ai での使い方

- **1レースの複数券種の配分の実装の基本形**: 着順モデル（Plackett–Luce など）から上位3頭の順列の確率 $p_i$ を作り、単勝・複勝・馬連・ワイド・馬単・3連複・3連単の各買い目について払戻行列 $R$（結果×賭け）を組み立てる。目的 $\sum_i p_i\log(1 + r_i^\top a)$ は CVXPY でも書ける。買い目が多いと $m$ が大きくなるので、期待値が正の買い目だけに絞ってから解く。
- **fractional Kelly の2つの定義を比べる実験**: 仮説「複数券種を混ぜるとき、『成長率の 75% を保つ最小賭け額』（本論文の式9）は、『Kelly 解を一律 0.5 倍』より、同じ対数成長率でバックテストの最大ドローダウンが小さい」。評価は確定オッズでの対数成長率と最大ドローダウン。
- 本論文の例のとおり、最適解は少数の買い目に集中しやすい。著者が提案する Lasso 的な罰則（ゼロの多い配分）は、実際の購入点数を減らす目的で試す価値がある (p.41)。
- 複勝・ワイドは払戻が幅を持つ（同着や他の当たり馬で変わる）ので、$r_i$ を結果ごとに正確に計算する必要がある。JRA の複勝の払戻計算規則を実装しておく。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 元の Kelly 基準。
- [Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 単勝（相互排他）の Kelly 解。本論文はその拡張を目指す。
- [Deza 2015](./2015-deza-chance-constrained-parimutuel.md): 4連単の Kelly と機会制約。
- [Busseti 2016](./2016-busseti-risk-constrained-kelly.md): 一般の有限結果（複数券種）の Kelly と、ドローダウン制約。同じ定式化。
- [MacLean 1992](./1992-maclean-growth-versus-security.md): fractional Kelly の成長と安全性のトレードオフ。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md): 確率の不確実性を考えた Kelly の縮小。本論文が今後の課題として挙げる。
- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 相互排他な多結果での最適賭け。
- [Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md): fractional Kelly を含む戦略の実データ比較（相互排他な場合のみ）。
- [Hausch 1981](./1981-hausch-racetrack-market-efficiency.md): 複勝・3着内を Kelly で買う古典。

## 検索語

複数券種, 非相互排他, 券種の組み合わせ, 払戻行列, 分数ケリー, フラクショナルケリー, 成長率の比, 信頼領域法, 単勝, 複勝, 馬連, 馬単, 3連単, ケリー基準, non-mutually exclusive bets, multiple bet types, Kelly criterion, fractional Kelly, expected log-growth, trust region, exotic bets, win place show, exacta, quinella, trifecta, constrained programming

---
title: An Explicit Solution to the Problem of Optimizing the Allocations of a Bettor's Wealth When Wagering on Horse Races
authors: Smoczynski Peter B., Tomkins Dave
year: 2010
venue: The Mathematical Scientist 35(1) 10-17
url: https://www.researchgate.net/publication/268615950_An_explicit_solution_to_the_problem_of_optimizing_the_allocations_of_a_bettor's_wealth_when_wagering_on_horse_races
doi:
topic: betting-strategy
tags: kelly, win-bet, kkt, closed-form, takeout
verified: abstract
importance: high
source: unavailable
---

# 単勝の複数頭買いの Kelly 解：賭ける馬の集合を決めれば配分は閉形式

**原本未取得**。The Mathematical Scientist（Applied Probability Trust）は有料で、ResearchGate に全文はなく、著者ページやリポジトリの版も見つからなかった。本ノートは、本論文を引用・再現した論文（[Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md) の改訂稿、[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md)、[Deza 2015](./2015-deza-chance-constrained-parimutuel.md)、[Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md)）の記述に基づく。式の正確な形と記号は原本で確認していない。

> 一言で: 控除率のある単勝で、複数の馬に同時に賭けるときの期待対数資金の最大化（Kelly）を KKT 条件で解いた。賭ける馬の集合 $S$ が決まれば各馬への賭け額は閉形式で書け、$S$ は「勝率/価格」の大きい順に馬を加えていく反復で決まる。1頭だけなら通常の Kelly に一致する。

## 問題

$n$ 頭のレース。馬 $h$ の勝率 $\pi_h$、小数オッズ $O_h$（固定と仮定）、資金 $w$、賭け額 $x_h \ge 0$、$\sum x_h \le w$ のもとで

$\max_x \sum_h \pi_h \log\big(x_h O_h + w - \sum_i x_i\big)$

を解く（[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md) p.3 の問題 (P) の記述。Metel は「厳密な最適解は Smoczynski と Tomkins のアルゴリズムで求まる」とする）。
[Deza 2015](./2015-deza-chance-constrained-parimutuel.md) は本論文を「KKT 条件を使って最適な単勝の賭けを求める簡単な手順を導いた」と紹介する (Deza p.1)。

## 解の形（Whelan 2025 による再記述）

価格 $p_i = 1/O_i$ として、賭ける馬の集合を $S$ とすると、各馬への賭け（1ドル払戻の賭けの数）は

$x_i = w\Big(\dfrac{\pi_i}{p_i} - \dfrac{1 - \sum_{k\in S}\pi_k}{1 - \sum_{k\in S}p_k}\Big)$

の形になる（Whelan p.10, 式19。抽出テキストが崩れていたため、1頭のとき Kelly に一致することから再構成した）。右辺の第2項は「$S$ 以外の馬が勝つ確率」と「$S$ 以外の馬の価格の和」の比で、Kelly の「留保率（reserve rate）」に当たる。

- 馬 $i$ に正の額を賭けるための条件は $\pi_i/p_i$ が一定の閾値を超えること（Whelan p.10, 式20）。
- 集合 $S$ を決める手順: $\pi_i/p_i$（期待払戻率）が最大の馬から始め、条件を満たす限り次の馬を加え、満たさない最初の馬で止める（Whelan p.10）。
- 式自体は $S$ を決めないので、この反復が必要（Whelan p.10）。
- 期待対数成長の最大値の式も与える（ResearchGate の要旨による）。
- 論文には2つの数値例があり、Whelan の Matlab コード（fmincon の内点法）で同じ答えが再現された（Whelan p.11）。

控除率があると全馬の価格の和が1を超えるので、全馬に賭けることはなく、少なくとも1頭は賭けない集合の外に残る。これは Whelan が一般の凹効用で示した一意性の条件と同じ構造である（Whelan p.9-10）。

## 位置づけ

- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md) が期待利益最大化で単勝の最適な組み合わせを閉形式で与えたのに対し、本論文は対数効用（Kelly）で同じことをした。
- 複数頭への同時の賭けを、各馬独立の Kelly ではなく一体で最適化する点が要。Whelan は、独立に扱う2択ルールより同時最適のほうが賭け額が大きくなり、期待値がわずかに負の馬も買うことを示した。
- 後続研究はこの解を出発点にしている: 確率の推定誤差（[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md)）、機会制約と4連単（[Deza 2015](./2015-deza-chance-constrained-parimutuel.md)）、相互排他でない複数券種（[Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md)）、CRRA 効用（[Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md)）。

## 批判的に読む（原本未読のため限定的）

- オッズを固定とみなす。パリミュチュエルでは自分の賭けでオッズが下がるが、その効果は入らない（Metel の問題設定からの推測）。
- 勝率 $\pi$ を既知とする。推定誤差を入れると過大賭けになる（Metel が指摘し、本論文の解を出発点に改良した）。
- 実データでの検証があるかは未確認。

## keiba-ai での使い方

- **単勝 Kelly の基準実装**: 汎用ソルバを使わず、$\pi_i/p_i$ の降順ソートと累積和だけで解ける。1レース数マイクロ秒で、全レースのバックテストや、確率を何千回もサンプリングする実験（[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md) の Emc 型）の内側ループに使える。CVXPY で解いた結果と一致するかを単体テストにする。
- **単勝オッズと確率の入れ方**: $p_i$ は確定オッズの逆数（控除率込みなので $\sum p_i > 1$）、$\pi_i$ はモデルの勝率。fractional Kelly にするなら得られた $x$ を一律に縮めるか、[Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md) の定義を使う。
- **実験案**: 仮説「同じレースの複数馬を同時最適化した単勝 Kelly は、各馬独立の Kelly より1レースあたりの賭け総額が大きく、モデルのずれが誤差主体なら評価期間の対数成長率は低い」（[Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md) の予測の検証）。
- 原本が手に入ったら、式の記号と2つの数値例をここに追記し、実装のテストケースにする。

## 関連ノート

- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 本論文の解を再現し、CRRA 効用へ拡張。本ノートの主な情報源。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 本論文の問題に確率の推定誤差を入れた。
- [Deza 2015](./2015-deza-chance-constrained-parimutuel.md): 本論文を引用し、4連単と機会制約に進む。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): 相互排他でない複数券種への拡張。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 期待利益最大化での最適な単勝の組み合わせ。
- [Kelly 1956](./1956-kelly-information-rate.md): 1頭の場合に一致する元の基準。
- [Hausch 1981](./1981-hausch-racetrack-market-efficiency.md): 複勝・3着内での Kelly の古典的な実証。

## 検索語

単勝, 複数頭買い, 同時最適化, ケリー基準, KKT条件, 閉形式解, 明示解, 能動集合, 留保率, 期待払戻率, 控除率, 資金配分, win bet, Kelly criterion, explicit solution, closed form, Karush-Kuhn-Tucker, active set, reserve rate, takeout, multiple horses, optimal allocation, log utility, Mathematical Scientist

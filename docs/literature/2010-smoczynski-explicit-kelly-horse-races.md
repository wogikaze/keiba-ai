---
title: An Explicit Solution to the Problem of Optimizing the Allocations of a Bettor's Wealth When Wagering on Horse Races
authors: Smoczynski Peter B., Tomkins Dave
year: 2010
venue: The Mathematical Scientist 35(1) 10-17
url: https://www.researchgate.net/publication/268615950_An_explicit_solution_to_the_problem_of_optimizing_the_allocations_of_a_bettor's_wealth_when_wagering_on_horse_races
doi:
topic: betting-strategy
tags: kelly, win-bet, kkt, closed-form, takeout
verified: fulltext
importance: high
source: downloaded
source_version: accepted-manuscript
---

# 単勝の複数頭買いの Kelly 解：賭ける馬の集合を決めれば配分は閉形式

原本は著者が ResearchGate に上げた原稿（2019年1月アップロード、12ページ + RG の表紙）を Internet Archive の保存版から取得した。誌面（pp.10-17）ではなく著者の組版なので、版は accepted-manuscript とした（誌面との異同は未確認）。ページは PDF のページ（p.1 は RG の表紙、本文は p.2-13）。

> 一言で: 控除率のある単勝で、複数の馬に同時に賭けるときの期待対数資金の最大化（Kelly）を KKT 条件で解いた。賭ける馬の集合 $S$ が決まれば配分は $f_i=\pi_i-\beta_i R(S)/D$ と閉形式で書け、$S$ は「期待払戻率」の大きい順に、それが留保率 $R$ を超える限り馬を加えるだけで決まる (p.9-10)。

## 原本で確認・訂正した点

旧ノートは [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md) などの再記述に頼り、式の形を「1頭のとき Kelly に一致する」ことから再構成していた。原本の式 (6.5)・(6.8) と照合し、再構成した形は（記号の違いを除き）**正しかった**。

- 旧ノートの $p_i=1/O_i$ と原本の $\beta_i$ の関係は $\beta_i=D\,p_i$（$\beta_i$ は単勝票数のシェア、$D=1-$控除率）(p.4, 式2.1-2.2)。
- 旧ノートは「1ドル払戻の賭けの数」で書いていたが、原本は資金に対する**賭け額の割合** $f_i$ で書く。
- 実データでの検証はない。数値例2つだけ (p.11-12)。
- 一意性や「全額を賭ける解は劣る」ことの証明は省略されている (p.8, 10)。

## モデル

$n$ 頭のレースが同じ条件で無限に繰り返される。馬 $k$ の真の勝率 $\pi_k$、単勝票数のシェア $\beta_k=b_k/\sum_m b_m$、配当率 $D=1-tt$（$tt$ は控除率。北米で 0.80〜0.85）(p.3-4)。

- 払戻率: $r_k=D/\beta_k=Q_k+1$（$Q_k$ はオッズ）(p.4, 式2.2)
- 期待払戻率: $er_k=D\pi_k/\beta_k=\pi_k(Q_k+1)$ (p.4, 式2.3)
- 目的関数: $L(f)=\sum_k \pi_k\ln\big(1-\sum_m f_m+D f_k/\beta_k\big)$ (p.5, 式3.1)
- 制約: $f_m\ge0$（レイなし）、$\sum f_m\le1$（借入なし）(p.6, 式3.2)

自分の賭けが $\beta$ を変えない（少額）ことを仮定する (p.4)。

## 解

KKT 条件 (p.8, 式5.1-5.5) を解くと、賭ける集合 $S$ について

$$f_i^{opt}=\pi_i-\beta_i\frac{\sum_{k\notin S}\pi_k}{D-\sum_{k\in S}\beta_k}\quad(i\in S),\qquad f_j^{opt}=0\quad(j\notin S)$$

(p.9, 式6.5)。賭けずに残す割合（留保率）は

$$R(S)=1-\sum_{m\in S}f_m=\frac{D\sum_{k\notin S}\pi_k}{D-\sum_{k\in S}\beta_k},\quad R(\emptyset)=1$$

(p.9, 式6.8)。$f_i=\pi_i-\beta_i R(S)/D$ と書ける。最大対数成長率は

$$L(f^{opt})=\sum_{k\in S}\pi_k\ln\frac{D\pi_k}{\beta_k}+\Big(\sum_{k\notin S}\pi_k\Big)\ln R(S)$$

(p.10, 式6.9)。$S$ の条件は「$S$ の中の馬は $er_i>R(S)$、外の馬は $er_j\le R(S)$」(p.9, 式6.7)。

## アルゴリズム（p.10）

1. 各馬の $er_i$ を計算する。
2. $er_i$ の降順に並べ替える。
3. $S=\emptyset$、$R=1$ とする。
4. 次の馬が $er_i>R$ なら $S$ に加えて $R$ を式 (6.8) で再計算する。そうでなければ止める。

止まったときの $S$ が唯一の最適集合（空なら賭けない）。

## 数値例

| 例 | $D$ | 頭数 | 賭ける馬 | 配分 $f$ | $L(f^{opt})$ |
|---|---|---|---|---|---|
| 1 (p.11) | 0.80 | 7 | 7, 5 | 0.4870, 0.0974 | 0.2964 |
| 2 (p.12, Enns & Tomkins 1993 の例) | 0.85 | 5 | 3, 2, 4, 1 | 0.1477, 0.06591, 0.07955, 0.1955 | 0.08736 |

例1では馬6の $er_6=0.4156$ が $R(\{7,5\})=0.4156$ と等しく、集合に入らない (p.11)。例2では **$er=1.0$（期待利益ゼロ）の馬4にも資金の約2割を賭けている** (p.12)。期待値がプラスでなくても、他の馬が負けたときの保険として入る。これが「各馬独立の Kelly」との違いの核心である。

## 批判的に読む

- 確率 $\pi$ を既知として扱う。推定誤差を入れると過大な賭けになる（[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md) が後に扱う）。
- 少額の仮定で、自分の賭けによるオッズの変化を無視する (p.4)。パリミュチュエルで大口になると成り立たない。
- 確定オッズを使う前提。実際は締切前のオッズで賭けるので、$\beta$ の不確実性が残る。
- 証明の一部（一意性、$\sum f=1$ の解が劣ること）が省略されている (p.8, 10)。結論は凸最適化の一般論と Whelan の再現で裏づけられているが、原本だけでは完結しない。
- 実データによる検証・回収率の計算はない。

## keiba-ai での使い方

- **単勝 Kelly の基準実装**: 降順ソートと累積和だけで解ける。$\beta_k$ は単勝オッズから $\beta_k=D/(Q_k+1)$ で戻せる（JRA の単勝は $D=0.80$）。数値例2つ（p.11-12）をそのまま単体テストにし、CVXPY の解とも突き合わせる。
- **確率をサンプリングする実験の内側ループ**: 1レースあたりの計算が軽いので、[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md) 型の不確実性込みの評価に使える。
- **実験案（仮説）**: 「同時最適化した単勝 Kelly は、各馬独立の Kelly より1レースの賭け総額が大きく、$er\le1$ の馬も含む。モデルの勝率が過信気味なら、評価期間の対数成長率は独立 Kelly や fractional Kelly より低い」。時系列分割のテスト期間で、実際の確定オッズ・控除率込みで比べる。

## 関連ノート

- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 本論文の解を再現し、CRRA 効用へ拡張。旧ノートの情報源で、再記述は原本と一致した。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 本論文の問題に確率の推定誤差を入れた。
- [Deza 2015](./2015-deza-chance-constrained-parimutuel.md): 本論文を引用し、4連単と機会制約に進む。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): 相互排他でない複数券種への拡張。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 期待利益最大化での最適な単勝の組み合わせ。本論文は対数効用版。
- [Kelly 1956](./1956-kelly-information-rate.md): 本論文が「不完全な解」とした元の問題 (p.2)。
- [Hausch 1981](./1981-hausch-racetrack-market-efficiency.md): 複勝・3着内での Kelly の古典的な実証。

## 検索語

単勝, 複数頭買い, 同時最適化, ケリー基準, KKT条件, 閉形式解, 明示解, 能動集合, 留保率, 期待払戻率, 控除率, 配当率, 資金配分, 保険的な賭け, win bet, Kelly criterion, explicit solution, closed form, Karush-Kuhn-Tucker, active set, reserve rate, expected revenue rate, dividend rate, takeout, track take, multiple horses, optimal allocation, log utility, Mathematical Scientist, Enns Tomkins

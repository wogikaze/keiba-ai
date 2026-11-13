---
title: Optimal Betting Under Parameter Uncertainty: Improving the Kelly Criterion
authors: Baker Rose D., McHale Ian G.
year: 2013
venue: Decision Analysis 10(3) 189-199
url: https://pubsonline.informs.org/doi/10.1287/deca.2013.0271
doi: 10.1287/deca.2013.0271
topic: betting-strategy
tags: kelly, estimation-error, shrinkage, fractional-kelly, tennis
verified: abstract
importance: high
source: unavailable
---

# 勝率が推定値なら Kelly の賭け額を縮める：縮小係数 k の導出（2択の賭け）

**原本未取得**。INFORMS の掲載版は有料で、Salford 大学のリポジトリ（USIR 36876）は全文非公開、移行先の worktribe は自動取得を拒否（403）、ResearchGate の著者アップロード版も取得できなかった。本ノートは要旨と、本論文を引用する論文（Chu, Wu & Swartz 2018 の著者版 PDF、[Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md)、[Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md)、[Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md)）の記述に基づく。数値やページは原本で確認していない。

> 一言で: Kelly 基準は勝率の推定値 $\hat p$ をそのまま使い、推定の不確実性を無視する。賭け割合を $k\,s^*(\hat p)$（$s^*$ は Kelly 割合、$0<k<1$）の形に限定して、標本外の期待効用を最大にする縮小係数 $k$ を求めると、不確実性があるときは $k<1$ が最適になる。シミュレーションとテニスの賭けデータで、縮小 Kelly が素の Kelly を上回った（要旨による）。

## 要旨から分かること

- 問題: Kelly は推定勝率を真の値として使う。推定誤差を考えると、標本外の成績を上げるには賭け額を縮めるべき。
- 方法: 縮小係数の推定値をいくつか比較する。ブートストラップを使う（キーワードによる）。
- 評価: シミュレーションと、テニスの賭けデータ。
- 結論: 縮小 Kelly は「生の」Kelly より良い。近似的な縮小係数の1つは、賭ける人が「封筒の裏」で計算できる簡易な補正になる。
- 一般の危険回避的な効用関数での縮小（shrinkage）と膨張（swelling）、決定理論への含意も論じる（Salford リポジトリの要旨による）。
- キーワード: Kelly criterion, parameter risk, expected utility, bootstrap, tennis betting, shrinkage。

## 引用論文から分かる設定

- Chu, Wu & Swartz（"Modified Kelly criteria", JQAS 2018 の著者版 PDF、第1節）によれば、本論文は賭け割合を $k\,s^*(q)$ と仮定する。$s^*(p)$ は Kelly 割合、$q$ は $p$ の推定量、$0<k<1$ が縮小係数。その上で、効用が $k$、推定量 $q$、その標本分布にどう依存するかを、特定の $p$ の値ごとに分析する。代替の効用関数も扱う。Chu らはベイズ推定量を使い、賭け割合の形を仮定しない点で本論文と対比する。
- 同じ著者らの続編（Baker & McHale 2016, International Journal of Statistics and Probability 5: 80-90）は、頻度論的リスクの最小化が事後期待損失の最小化より好ましい条件を論じる（Chu らによる）。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md) は本論文を「2結果の賭けで、最適な Kelly の割合を与える縮小係数を導いた」と紹介し、多結果（単勝の n 頭）への拡張を自らの課題とした (Metel p.2)。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md) と [Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md) は、確率の不確実性を考える Kelly の代表例として引用する。

## 考え方の整理（一般論、原本未確認）

推定勝率が真の勝率より高い賭けほど「有利に見える」ので、Kelly はその賭けに多く賭ける。誤差が平均ゼロでも、賭け額が推定値の増加関数であるため、過大評価の側で大きく賭けることになり、標本外の成長率は下がる（Metel p.2 も同じ説明）。対数効用の成長率は賭け割合について凹で、最適点の近くでは平らなので、少し縮めても失う成長率は小さく、過大賭けの損失は大きい。これが縮小が有利になる理由である。$k$ の最適値は推定の分散が大きいほど小さくなると考えられるが、本論文の具体式は未確認。

## 批判的に読む（原本未読のため限定的）

- 対象は2択の賭け（テニスの勝敗）。単勝のような多結果では、縮小を全馬一律の $k$ にするのか馬ごとにするのかで話が変わる。
- 賭け割合を $k\,s^*(q)$ の形に限るのは制約で、Chu らはこの仮定を外したベイズ的な最適化を示している。
- テニスのデータの規模、期間、オッズの出所、回収率の計算方法は未確認。

## keiba-ai での使い方

- **fractional Kelly の係数を経験則でなく推定誤差から決める**: 単勝確率モデルのブートストラップ（またはアンサンブル）で各馬の勝率の分散を出し、分散が大きい馬ほど Kelly 割合を縮める。最初は全馬共通の $k$ を検証期間の対数成長率最大で選び、次に分散に応じた馬ごとの $k$ と比べる。
- **実験案**: 仮説「ブートストラップの分散で馬ごとに縮める Kelly は、全馬一律の $k$ の fractional Kelly より、評価期間の対数成長率が高い」。新馬・休み明けなどデータの少ない馬で差が出るはず。
- 多頭立てへの拡張は [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md)（係数の推定誤差から勝率をサンプリングする方法）を参照する。
- 原本が手に入ったら、縮小係数の近似式（「封筒の裏」の補正）を確認して、ここに追記する。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md): 縮小の対象となる元の基準。
- [MacLean 1992](./1992-maclean-growth-versus-security.md): 推定値の使用による過大賭けと fractional Kelly。本論文の背景。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): 本論文の考えを単勝の多結果に拡張。
- [Sun 2018](./2018-sun-distributional-robust-kelly.md): 確率の不確実性を最悪ケース（分布ロバスト）で扱う別の方法。
- [Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md): fractional Kelly の係数を検証データで選ぶ実証比較。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): fractional Kelly の別の定義（成長率の k 割を保つ）。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): 実務での Kelly と半分 Kelly。

## 検索語

パラメータ不確実性, 推定誤差, 縮小係数, 縮小ケリー, 分数ケリー, 半分ケリー, 過大賭け, ブートストラップ, 期待効用, テニス, parameter uncertainty, parameter risk, estimation error, shrinkage factor, shrunken Kelly, fractional Kelly, overbetting, bootstrap, expected utility, tennis betting, Decision Analysis, Baker McHale

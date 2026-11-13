---
title: 競馬予想アプリの「勝率」を数式で解剖したら、確率になっていなかった話
authors: tatsuya_m07（TatsuyaM2667）
year: 2026
venue: Zenn
url: https://zenn.dev/tatsuya_m07/articles/0a5d4654b6bc8b
topic: practitioner
tags: grey-literature, monte-carlo, thurstone, harville, softmax, expected-value, calibration
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 競馬予想アプリの「勝率」を数式で解剖したら、確率になっていなかった話（tatsuya_m07 2026）

> 一言で: 自作の予想アプリ Keiba Vision のロジックを数式で書き下したところ、画面の「勝率」は合計 375% で確率になっておらず、その勝率にオッズを掛けた期待値ではオッズが打ち消し合って消えていた。正規分布の揺らぎを持つ Thurstone 型のモンテカルロで馬連確率を直接数えると、Harville の公式は約 28% 過大だった。

実データでの評価はない。記録の価値は、個人開発で起きやすい「確率でないものを確率として扱う」誤りと、Harville の公式の偏りを具体例で示した点にある。

## データ

- アプリ内蔵のサンプル出馬表（有馬記念、16頭）。過去のレース結果での推定や検証は行っていない。
- アプリ: https://keiba-vision.pages.dev 、ドキュメント（18ページ）: https://keiba-vision-docs.pages.dev 、リポジトリ: https://github.com/TatsuyaM2667/keiba-predictor

## 特徴量

- スピード指数、脚質（逃げ〜追込）とペースの相性、スタミナ。脚質の相性はペース π の1次関数で、逃げは `1.04 - 0.30(π - 1)`、追込は `0.98 + 0.30(π - 1)`。2本の直線は π = 1.1 で交わる。

## モデルと目的変数

3つの別の仕組みが画面に出ていた（「『予想』は 3 種類あった」）。

1. 予想エンジン（Kotlin）: 経験則の加重平均。印・買い目・「勝率」を出す。
2. モンテカルロ（Zig → WebAssembly）: 馬 i の出来 = 平均 μ_i + 揺らぎ。出来の大きい順に着順を決める（Thurstone モデル）。揺らぎは一様乱数4個の和（Irwin–Hall、係数 0.11 で標準偏差 0.064）。10万回走らせて勝率・3着内率を数える。
3. 3D シミュレーション: 結果（ゴール時刻）から走行過程を作る演出。

## 評価

- 実レースでの評価はない。検算として、2頭の場合の厳密解 Φ(Δμ/(√2σ)) とシミュレーションを比べ、0.6096 対 0.6083 で一致を確認した。
- モンテカルロの標準誤差: N = 10^5 で 0.15 ポイント。

## 結果

- **発見1**: 予想エンジンの勝率は、総合スコア S とオッズ O から作られており、16頭の合計は 375.1%。上限 68% で切っていた。
- **発見2**: 妙味指数（期待値）は `75 × (p̂/100) × O` で、p̂ がオッズの逆数を含むためオッズが消え、`2.1 S` になる。スコア 47.1 以上は全頭が上限 99。「勝率をオッズから作り、その勝率にオッズを掛ける」循環だった。
- **発見3**: ドウデュースとレガレイラの馬連確率は、Harville の公式で 0.2199、直接シミュレーションで 0.1713。公式は約 28% 過大。著者は、Harville は揺らぎが Gumbel 分布のとき（Luce モデル、softmax）に厳密で、裾の軽い正規分布では「強い馬が1着のとき2着も強い馬」の確率を高く見積もりすぎると説明する。
- 揺らぎの係数で1番人気の勝率は 62.0%（0.05）、36.3%（0.11）、22.1%（0.20）と大きく変わる。0.11 は「1番人気の勝率は3割前後」に合わせて手で決めた。
- 改善案: 勝率をモンテカルロの確率に置き換える、期待値は `p^MC × O` で計算しケリー基準の一部で配分する、馬単・3連単は直接シミュレーションで数える、揺らぎの係数を過去の結果の対数損失最小化で推定する。

## 落とし穴と教訓

- 画面に「勝率」と書いてあっても、合計が 100% にならないなら確率ではない。期待値計算に使う前に、レース内の合計を確かめる。
- オッズを入力に使って作った確率にオッズを掛けると、期待値が循環してオッズの情報が消える（あるいは自己参照になる）。
- 揺らぎの分布の形（正規か Gumbel か）で、2着以下の確率が大きく変わる。

## 批判的に読む

- 実データでの検証がない。Harville が 28% ずれるというのは、「真の着順過程が Thurstone（正規）である」と仮定したモデル内での比較で、実際の競馬でどちらが当たるかは別の問題。実データでは [Lo 1994](./1994-lo-comparison-harville-henery.md) が Harville と Henery（正規）を比べ、Harville が2着・3着の確率で偏ることを示している。方向は本記事と一致する。
- 揺らぎの係数を1番人気の勝率だけに合わせており、全馬への較正ではない。
- 能力値（スピード指数など）の出どころと時点が書かれていない。

## keiba-ai での使い方

- 勝率モデルの出力に、**レース内の確率の合計 = 1 の検査**と、オッズを入力に使ったかどうかのフラグを付ける。期待値の計算に使う確率がオッズから作られていないことを、コードで保証する。
- 馬連・3連系の確率は、Harville だけでなく、Henery／Stern の補正やシミュレーションと比べる。比べる基準は実データの対数損失。
- Thurstone（正規）と Plackett–Luce（Gumbel）の違いを、着順モデルの選択として ADR に書く材料にする。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md) — 本記事が検証した公式。
- [Henery 1981](./1981-henery-permutation-probabilities.md) — 正規分布（Thurstone）の着順確率。
- [Lo 1994](./1994-lo-comparison-harville-henery.md) — Harville と Henery の実データ比較。
- [Stern 1990](./1990-stern-gamma-permutations.md) — ガンマ分布で両者をつなぐ。
- [Luce 1959](./1959-luce-individual-choice-behavior.md) — Gumbel → softmax の Luce モデル。
- [Lo 2008](./2008-lo-ordering-probabilities-approximation.md) — 着順確率の近似。

## 検索語

勝率, 確率の合計, 期待値の循環, circular expected value, モンテカルロ, Monte Carlo simulation, Thurstone モデル, Harville 公式, Harville formula, Henery, Plackett-Luce, Gumbel, softmax, 馬連確率, exacta probability, quinella, Irwin-Hall, ケリー基準

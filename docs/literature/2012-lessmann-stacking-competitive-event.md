---
title: A new methodology for generating and combining statistical forecasting models to enhance competitive event prediction
authors: Lessmann Stefan, Sung Ming-Chien, Johnson Johnnie E.V., Ma Tiejun
year: 2012
venue: European Journal of Operational Research 218(1) 163-174
url: https://ideas.repec.org/a/eee/ejores/v218y2012i1p163-174.html
doi: 10.1016/j.ejor.2011.10.032
topic: machine-learning
tags: ensemble, stacking, conditional-logit, forecast-combination, diversity
verified: abstract
importance: high
source: unavailable
source_version: none
---

# 多様なベースモデルを大量に作り、条件付きロジットのスタッキングで結合する（EJOR 2012）

> 一言で: 着順の「代替指標」をいろいろな目的変数にして多数のベースモデルを作り、条件付きロジット回帰と対数尤度比による予測選択を組み合わせたスタッキングで結合した。単純平均は競争的イベントでは不適切なことがあり、ベースモデルの強さと多様性の両方が重要だと結論する。

**原本未取得。** Elsevier は有料。Southampton ePrints（201409）の PDF は職員限定、academia.edu の著者アップロードはログインが必要で、他の無料版は見つからなかった。著者らの2013年の関連講演スライド（UNLV リポジトリ）も取得時 403 だった。以下は IDEAS/RePEc の要旨と検索結果の要約に基づく。数値は未確認。

## 要旨から分かること

- 予測の結合（forecast combination）は他分野で効果が大きいが、競争的イベント（スポーツ、選挙）ではほとんど使われてこなかった。
- 障害は2つ。参加者間の競争の強さと、個々のモデルの精度と多様性のトレードオフ。
- 方法: レース結果の代替指標（surrogate measures of event outcomes）を使って多様なベース予測を作り、条件付きロジット回帰と対数尤度比に基づく予測選択を組み合わせたスタッキングで統合する。
- 結果: (1) 結合ではベースモデルの強さと多様性の両方が重要、(2) 他分野でよく使う単純平均はこの設定では不適切なことがある、(3) 提案手法は統計的にも経済的にも、より正確な予測を出す。
- 著者は、賭け市場の規制当局や市場効率性の評価にも意味があるとする。
- キーワード: Forecasting, Forecast combination, Competitive event prediction。

検索結果に表示された academia.edu の要約断片では、回帰・分類の各種手法から571個の多様なベースモデルのライブラリを作り、平均ベースの結合はベースモデルの多様性不足で失敗すると述べている（原本で未確認）。

## 批判的に読む（未確認点）

- データ（市場・期間・レース数）、評価の分割、回収率の算出方法、統計的検定は未確認。
- 571個ものベースモデルから選択・結合するとき、選択に使う期間と評価期間が分かれていないと過学習しやすい。対数尤度比による選択がどのデータで行われたかは原本で確認が必要。

## keiba-ai での使い方

- **結合層は条件付きロジット（レース内 softmax）にする**: GBDT 勝率、タイム回帰、ランキングモデル、市場確率など複数の予測を単純平均せず、レース内 softmax のロジスティック層で重み付けして結合する。第2段に市場確率 $\ln q$ を入れれば Benter 型二段階モデルの一般化になる。
- **目的変数を変えて多様性を作る**: 勝ち2値、3着以内、着差（秒）、正規化着順、上がりタイムなどを目的にしたモデルを作り、それぞれの出力を結合層の入力にする。仮説: 同じ特徴量でも目的変数を変えた複数モデルの結合は、単一モデルより第2段後の対数損失が下がる。
- **選択と評価の期間分離**: 結合層の学習・モデル選択・最終評価を時系列で3期間に分ける（[Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md) の考え方）。

## 関連ノート

- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md), [Lessmann 2009](./2009-lessmann-svm-classification-horserace.md), [Lessmann 2010](./2010-lessmann-random-forest-horserace.md): 同じグループの前作。第1段の学習器と目的変数を変えてきた流れの延長。
- [Sung 2007](./2007-sung-two-step-conditional-logit.md): 条件付きロジットの二段階モデル。
- [Benter 2019](./2019-benter-model.md): ファンダメンタルモデルと市場確率の結合。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 条件付きロジット。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): モデル選択と評価の分離。

## 検索語

予測の結合, フォーキャスト・コンビネーション, スタッキング, アンサンブル, ベースモデルの多様性, 代替指標, 目的変数の多様化, 条件付きロジット, 対数尤度比, 予測選択, 単純平均, 競争的イベント, forecast combination, stacking, ensemble selection, surrogate measures, diversity, conditional logit, competitive event prediction, EJOR

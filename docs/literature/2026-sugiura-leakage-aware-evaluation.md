---
title: Leakage-aware pre-event machine learning evaluation for horse-race prediction under temporal validation
authors: Sugiura Shuichi
year: 2026
venue: Frontiers in Artificial Intelligence 9:1896192 (Brief Research Report)
url: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1896192/full
doi: 10.3389/frai.2026.1896192
topic: japan
tags: jra, jra-van, leakage, temporal-validation, ablation, gradient-boosting, calibration, place-bet, bootstrap
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 出走確定後・結果前の情報だけで JRA を予測し、特徴ブロックをアブレーションする評価手順

> 一言で: JRA-VAN の平地競走で「出走確定後・結果判明前」に使える変数だけを棚卸しし、時系列分割とレース単位ブートストラップで評価したところ、騎手・種牡馬の集計特徴やドメイン理論由来の特徴ブロックを足した 110 特徴のモデルは、素朴な 25 特徴のモデルより単勝・複勝の両方で悪かった。オッズは使っておらず、回収率の評価もない。

関西大学大学院心理学研究科の単著。2026年5月31日受付、9月24日公開 (p.1)。本文7ページの Brief Research Report。

## 要旨

予測時点を「出走確定後、結果が分かる前」と定め、データベース内の変数を「予測時点で使える」「結果後の情報」「市場情報」「予測時点での入手が不安定」「識別子」「ラベル定義専用」に分類する特徴量棚卸しとリーク監査を行う (p.3, Table 1)。
そのうえで、同じ勾配ブースティング（scikit-learn の HistGradientBoostingClassifier）を使い、特徴セットだけを変えた3モデルを独立の時系列テスト期間で比べる (p.3)。
主張の中心は「ドメイン知識が無益」ではなく、「実装した理論スコアのブロックは増分の予測力を持たなかったので、特徴ブロックは導入前に増分評価すべき」という手順論である (p.6–7)。

## データと分割

| 項目 | 内容 |
|---|---|
| データ | JRA 平地競走。JRA-VAN Data Lab から TARGET frontier JV で CSV 出力 (p.3) |
| 期間 | 2015年1月〜2026年5月10日 |
| 訓練 | 2015〜2022 |
| 検証 | 2023〜2024（中間評価とハイパーパラメータの確認） |
| テスト | 2025年1月5日〜2026年5月10日、4,556 レース・63,910 頭 (p.3, p.5) |
| ラベル | y_win（1着）、y_place_jra（JRA の複勝規則: 8頭以上は3着内、5〜7頭は2着内、4頭以下は除外）(p.4) |

複勝ラベルの評価対象は 63,481 頭、うち陽性 13,567。単純な「3着内」と食い違ったのは 116 頭だった (p.5)。
頭数（field_size）は TARGET の加工済み変数で、取消・除外後の最終頭数を反映している可能性があり、実際の発売時の条件を完全には再現しないと著者自身が断っている (p.4)。

## 使った特徴・除外した特徴

除外したもの (p.3, Table 1):

- 結果後の情報: 着順、払戻、上がり3F、同レースの結果から作った情報
- 市場情報: 最終オッズ、最終人気
- 予測時点で不安定な情報: 当日馬体重、馬場状態、天候
- 識別子: race_id、horse_id（race_id はブートストラップのグループにだけ使う）

モデル (p.3):

| モデル | 特徴数 | 中身 |
|---|---|---|
| current_full_model | 110 | 基本出走情報＋騎手集計・種牡馬集計＋同コース・未勝利戦の開催場の「ドメイン理論」特徴＋ルールベースのフラグ |
| original_no_theory_model | 25 | 基本出走情報（場、芝ダ、距離、馬番、枠、性、齢、斤量、騎手、調教師、父、母父、頭数）＋素の過去成績（出走数、前走間隔、勝率、複勝率、近3走平均着順、前走からの距離変更、芝ダ変更） |
| matched_no_theory_model | 25 | 上と同じ特徴に、full と同じハイパーパラメータを使った感度分析用 |

主比較は full と matched の比較で、ハイパーパラメータの違いを除いて特徴セットの効果だけを見る設計 (p.3)。

## 結果

テスト期間、レース単位ブートストラップ 10,000 回の 95% CI (p.7, Table 2)。

| ラベル | モデル | ROC AUC | PR-AUC | Brier | Log loss |
|---|---|---|---|---|---|
| 単勝 | full | 0.7293 | 0.1779 | 0.0628 | 0.2340 |
| 単勝 | original no-theory | 0.7507 | 0.1939 | 0.0621 | 0.2298 |
| 単勝 | matched no-theory | 0.7543 [0.7475, 0.7609] | 0.1974 | 0.0619 | 0.2287 |
| 複勝 | full | 0.7164 | 0.4159 | 0.1501 | 0.4668 |
| 複勝 | original no-theory | 0.7465 | 0.4513 | 0.1454 | 0.4525 |
| 複勝 | matched no-theory | 0.7513 [0.7469, 0.7558] | 0.4532 | 0.1443 | 0.4483 |

matched は全指標で最良で、検証期間でも同じ傾向だった（補足資料 S4、未読）(p.6)。モデル間差のペアブートストラップ CI は補足資料 S3 にある（未読）。

補助的なレース単位の波乱診断（race_upset_model）は ROC AUC 0.6464、PR-AUC 0.6224、Brier 0.2327、log loss 0.6571 (p.7, Table 3)。この診断は馬単位モデルには入力していない。同じ著者の別論文（[Sugiura 2026b](./2026-sugiura-upset-risk-diagnostics.md)）のテスト AUC 0.6459 とは小数第4位が違い、モデルの版が異なる可能性がある。

> These findings indicate that the evaluated theory-score block did not improve temporal test-set performance. (p.1)

### 数値の読み方（ノート作成者の計算）

- 単勝の陽性率は約 4,556/63,910 ≒ 0.071。定数予測の Brier は約 0.066、log loss は約 0.257。matched の Brier 0.0619 は定数予測より約 6% 小さく、log loss 0.2287 は約 11% 小さい。
- 複勝の陽性率は 13,567/63,481 ≒ 0.214。定数予測の Brier は約 0.168 で、matched の 0.1443 は約 14% 小さい。
- オッズを使わない JRA 全体のモデルとしては、単勝 AUC 0.75 前後が一つの目安になる。市場オッズの識別力（[守・久門 2010](./2010-mori-keiba-yoso-shuudanchi.md) の AR から換算して AUC 0.8 台）より明確に低い。

## 批判的に読む

- **なぜ full が悪いのかは分からない。** 著者は冗長性やノイズを挙げるが、因果の分析はしていない (p.6)。推測だが、騎手・種牡馬の集計特徴を訓練期間全体で計算していた（訓練データ内で対象レース自身や未来のレースの結果を含む）なら、訓練では過大に効き、テストで崩れる典型的なリークのパターンになる。集計の時点の切り方は本文に書かれていない（補足 S1 にあるかは未確認）。「リーク監査済み」の主張と、集計特徴でだけ性能が落ちる結果は、この点を確認しないと両立するか判断できない。
- **当日の馬場状態と馬体重を除外している。** 発売中に公表される情報なので、実運用では使える。除外は保守的すぎ、AUC の天井を下げている可能性がある。
- **オッズも回収率もない。** 単勝・複勝の確率を出しているのに、市場確率との比較やオッズに対する価値の評価はない。賭けの役に立つかは論文から言えない。
- **ハイパーパラメータは full に合わせた。** matched は「full 用に調整した設定」を流用しているので、no-theory に有利な比較ではない。それでも勝っている点は結論を補強する。
- 較正曲線と特徴量重要度は主要な証拠として使っていない、と著者が限界に書いている (p.7)。
- データはライセンス上公開できず、再現は JRA-VAN を契約した者に限られる (p.8)。原稿作成に生成 AI を使った旨の記載がある (p.8)。
- 頭数変数を、予測特徴とラベル定義の両方に使っている。最終頭数が取消後の値なら、予測特徴としてはわずかに未来情報を含む。

## keiba-ai での使い方

- **特徴量棚卸し表をそのまま作る。** Table 1 の分類（予測時点で利用可・結果後・市場・不安定・識別子・ラベル専用）を keiba-ai の特徴量一覧にも付け、各特徴が「いつの時点で確定するか」を列として持つ。リーク監査の単位になる。
- **集計特徴（target encoding 系）の時点管理を検証する実験。** 仮説: 「騎手・種牡馬・調教師の集計勝率を、対象レース前日までのデータだけで計算する（expanding window）版にすれば、full 相当のモデルでも no-theory を下回らない」。この論文の逆転がリーク由来かどうかを、手元のデータで切り分けられる。
- **特徴ブロック単位のアブレーション＋ハイパーパラメータを揃えた感度分析**を、新しい特徴群を足すときの標準手順にする。指標は log loss と Brier をレース単位ブートストラップの CI 付きで出す。
- **基準点。** オッズなし・当日情報なしの GBDT で、単勝 AUC 約 0.75、log loss 約 0.229。keiba-ai のオッズなしモデルがこれを下回るなら、どこかに問題がある。
- 複勝ラベルは頭数で 2着内/3着内が変わる。116 頭の差は小さいが、複勝の確率モデルでは JRA 規則に沿ったラベルを使う。

## 関連ノート

- [Sugiura 2026b](./2026-sugiura-upset-risk-diagnostics.md): 同じ著者・同じデータ・同じ分割の、レース単位の波乱診断。本論文の補助診断を独立に詳しく報告したもの。
- [Bergmeir 2018](./2018-bergmeir-cv-time-series.md)、[Cerqueira 2020](./2020-cerqueira-time-series-performance-estimation.md): 時系列データの検証分割。
- [Gneiting 2007](./2007-gneiting-proper-scoring-rules.md)、[Brier 1950](./1950-brier-verification-probability-forecasts.md): 確率予測の評価指標（引用されている）。
- [Bolton 1986](./1986-bolton-conditional-logit.md)、[Lessmann 2009](./2009-lessmann-svm-classification-horserace.md): 競馬の定量予測の先行研究として引用。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): 多数の特徴・設定を試すことによる過剰適合の評価。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): AUC より較正が賭けで重要という論点。本論文は較正を主要証拠にしていない。
- [Kobayashi 2023](./2023-kobayashi-odds-dependent-prediction.md): オッズを使う JRA の予測。オッズ除外の本論文と対照的。
- [Xie 2026](./2026-xie-jockeybench.md): 時点で区切った証拠で評価する JRA ベンチマーク。

## 検索語

データリーク, 情報リーク, leakage audit, リーク監査, 特徴量棚卸し, feature inventory, 予測時点, prediction-time availability, 時系列検証, temporal validation, 時系列分割, 特徴量アブレーション, feature-block ablation, 感度分析, ハイパーパラメータ揃え, HistGradientBoostingClassifier, 勾配ブースティング, GBDT, レース単位ブートストラップ, race-level bootstrap, ROC AUC, PR-AUC, Brier スコア, log loss, 複勝ラベル, JRA 複勝規則, JRA-VAN Data Lab, TARGET frontier JV, 騎手集計特徴, 種牡馬集計, theory-score, 杉浦

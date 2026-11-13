---
title: HKJC Race Outcome Modeling: Chronological ML, Probability Calibration, and Market-Aware Strategy Research
authors: jerrydaphantom
year: 2026
venue: GitHub
url: https://github.com/jerrydaphantom/hkjc-ml-research
topic: practitioner
tags: grey-literature, hong-kong, hkjc, lightgbm, catboost, calibration, market-aware, closing-odds, threshold-selection
verified: fulltext
importance: high
source: downloaded
source_version: web
---

# 香港（HKJC）の単勝確率モデル: 市場オッズ有無の比較、較正、閾値戦略の事後選択

> 一言で: HKJC の2020〜2026年のレース結果（5,282レース）で、ロジスティック回帰・LightGBM・CatBoost を時系列分割で比べた個人研究。確定単勝オッズを特徴量に入れると log loss が大きく改善し、全レースで1番人気予想を買うと ROI は −8〜−15%。EV と確率差の閾値で絞ると +22〜+58% の「候補」が出るが、テスト期間で事後に選んだ閾値で、使ったオッズも確定オッズなので実行できないと著者自身が明言している。

## データ

- 自作スクレイパーで HKJC のレース結果ページを取得し、SQLite に整形（スクレイパー本体は非公開）。
- 期間 2020-01-01〜2026-03-29。完走馬 64,091 行、5,282 レース、馬 4,089 頭、騎手 96 人、調教師 105 人（「Data Coverage」）。
- 取消・同着・異常ページは明示的に除外し、除外行は別に追跡できるようにしている。

## 特徴量

- 馬の過去成績（出走数・勝利数・3着内率）、同コース・同距離・同馬場の成績、騎手・調教師の過去成績、馬×騎手・馬×調教師の組み合わせ成績、距離・枠・頭数・斤量（「Historical feature engineering」）。
- 特徴量セットを2系統に分ける。**Market-free**（当該レースのオッズなし）と **Market-aware**（`win_odds` と `log_win_odds` を追加）。市場の増分価値を切り分けるための設計。

## モデルと目的変数

- 目的変数は1着（単勝）。1行1頭の二値分類。
- ロジスティック回帰、LightGBM、CatBoost。
- 較正は raw / sigmoid / isotonic と、それぞれをレース内で合計1に正規化した「race-normalized」版。

## 評価

- 時系列の train / validation / test 分割（境界の日付は README に書かれていない）。
- 指標は log loss、Brier、1番手の勝率（top-pick win rate）、勝ち馬が上位3頭に入る率。
- 回収は単勝の配当（結果ページの確定単勝オッズ）で、1単位均等賭け。控除は配当に込みだが、オッズはレース確定時のもの。

## 結果

「Raw baseline model comparison」と「Best calibrated」の節より（テスト期間）:

| 設定 | log loss | Brier | 1番手勝率 | 勝ち馬top3率 |
|---|---:|---:|---:|---:|
| ロジスティック market-free | 0.2583 | 0.0705 | 24.9% | 51.3% |
| ロジスティック market-aware | 0.2357 | 0.0658 | 31.3% | 62.8% |
| CatBoost market-aware | 0.2354 | 0.0657 | 32.7% | 62.1% |
| CatBoost market-aware + sigmoid + レース正規化 | 0.2350 | 0.0655 | 32.7% | 62.1% |

- モデル族の差（0.2354〜0.2357）は、オッズの有無の差（0.258→0.236）と比べてごく小さい。較正の改善も log loss で 0.0004 程度。
- 「Strategy Research Findings」: 1番手を全レースで買うと ROI は CatBoost −8.41%、LightGBM −9.00%、ロジスティック −15.06%。
- 「Example threshold candidates」: EV 閾値と「モデル確率 − 市場確率」の差の閾値の格子を張り、CatBoost で EV≥0.01・差≥0.085 のとき 106 件で ROI +40.66%、EV≥0.02・差≥0.09 で 79 件 +57.72%。ロジスティックでも 105 件 +52.76%。
- 10% の負け戻し（rebate）を仮定した感度分析も付く（価格への影響は無視）。

## 落とし穴と教訓（著者の記述）

- 「Core Bottleneck」: HKJC はパリミュチュエルで、締切直前に大量の票が入るため、購入時点では確定オッズが分からない。強いモデルも有望な絞り込みもオッズ由来の情報に依存しているので、オフラインの結果はそのまま実行可能な戦略にならない。著者は「本当の制約はモデルの複雑さではなくデータと実装」とまとめている。
- 閾値候補はテスト期間の診断から事後に選んだもので、本番ルールとして読まないよう明記している。
- HKJC は時系列のライブオッズの履歴を公開していないので、締切前オッズは自分で前向きに集める必要がある。
- 次の課題に、締切前オッズの収集、早い時点のオッズから確定オッズを予測する層、閾値を凍結しての前向き検証を挙げている。

## 批判的に読む

- **確定オッズのリーク**: market-aware の改善と閾値戦略の ROI は、購入時に知り得ない確定単勝オッズに基づく。分類性能の改善は「市場は強い」という事実の確認であり、そのまま賭けの優位を示さない。
- **閾値の事後選択**: 100件前後の選択で ROI +40〜+58% は、テスト期間で格子探索した結果の最大側。多重比較を考えると [Bailey ら 2017](./2017-bailey-probability-backtest-overfitting.md) の言う過学習の典型例で、選択件数100件の単勝なら ROI の標準誤差は数十%ポイントある。
- **分割の境界が書かれていない**。2020〜2026年の6年分のうちテストが何か月かも不明。
- 特徴量の時点処理について「研究には許容できるが、ライブ用にはさらに厳しくする必要がある」と著者が書いており、当日以降の情報の混入が完全には否定されていない。
- それでも、オッズあり・なしを分けて増分価値を測り、全買いの負けを先に示し、事後選択の限界を自分で書いている点は、個人の記録としては誠実。

## keiba-ai での使い方

- **市場なし / 市場ありの2系統を必ず並べる**設計をそのまま採用できる。JRA でも、オッズなしモデルの log loss と、オッズのみ（1/odds の正規化）の log loss、両者を組み合わせた log loss の3つを主表にする。
- 確定オッズを使った回収率は「上限の目安」として別欄に置き、購入可能時点のオッズ（JRA なら締切数分前の時系列オッズ）での回収率と区別する。[Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md) の締切直前のオッズ変動と合わせて、JRA で同じ問題がどの程度効くかを測る。
- EV×確率差の2次元閾値は、検証期間で決めて凍結し、テスト期間では動かさない。閾値ごとの選択件数を等高線で重ねる図は、件数の少ない高 ROI 領域を見分けるのに使える。
- レース内正規化（確率の合計を1にする）は、二値分類器の出力を単勝確率として使う前の最低限の処理として入れる。

## 関連ノート

- [Benter 2019](./2019-benter-model.md): 基本モデルと市場確率を2段階ロジットで結合する原型。本リポジトリは市場オッズを特徴量に直接入れる1段階方式。
- [Leung 2023](./2023-leung-annotated-benter-paper.md): HKJC のオッズで Benter 論文を再現したブログ。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 精度より較正で賭けの成績が決まるという主張。本リポジトリの「精度≠収益」と同じ方向。
- [Hubáček 2019](./2019-hubacek-exploiting-betting-market-ml.md)、[Hubáček 2020](./2020-hubacek-beating-market-bad-model.md): 市場と相関を下げたモデルで賭ける考え方。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): 閾値の事後選択の危うさ。
- [Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 締切直前のオッズの動き。
- [Torné 2021](./2021-torne-hong-kong-softmax-nn.md)、[Chung 2017](./2017-chung-svm-committee-hong-kong.md): 香港データの学術研究。
- [stevw 2026](./2026-stevw-hkjc-ml-research-platform.md)、[justinsuo 2026](./2026-justinsuo-hkjc-edge-lab.md)、[catowabisabi 2026](./2026-catowabisabi-hkjc-quinella-lightgbm.md): 同じ HKJC を扱う個人リポジトリ。

## 検索語

香港競馬, HKJC, 単勝確率, 確率較正, レース内正規化, 市場オッズ, 確定オッズ, 閾値戦略, 期待値, Hong Kong Jockey Club, win probability, probability calibration, sigmoid, isotonic, market-aware, market-free, closing odds, tote, pari-mutuel, EV threshold, probability gap, CatBoost, LightGBM, backtest overfitting

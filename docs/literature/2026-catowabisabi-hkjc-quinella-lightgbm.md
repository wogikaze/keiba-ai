---
title: HKJC Horse Racing Prediction (horse-racing-model-training)
authors: catowabisabi
year: 2026
venue: GitHub
url: https://github.com/catowabisabi/horse-racing-model-training
topic: practitioner
tags: grey-literature, hong-kong, hkjc, lightgbm, xgboost, quinella, benter-blend, kelly, morning-odds, suspected-leak
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 香港競馬の LightGBM で馬連2頭ボックスが +7.9%: ただし特徴量にリークの疑いがある

> 一言で: 公開データ（eprochasson/horserace_data、2008〜2018年）で LightGBM と XGBoost を学習し、2017年の検証で「オッズなしモデルの上位2頭で馬連（quinella）ボックス」が ROI +7.9%（817レース）、2018年上半期の外部検証で +2.6%（452レース）。オッズを特徴量に入れたモデルは的中率は上がるが馬連では負ける。朝オッズで単勝を Kelly で買うと +119〜+140% という数値も出ているが、上がり区間タイムを使った特徴量の時点が不明で、リークを疑うべき結果。

## データ

- `eprochasson/horserace_data`（GitHub の HKJC 公開ミラー、2008〜2018年6月、成績27.3万行）。全券種の配当 `all_dividends.csv.gz` と、2016〜2018年の1,510レースぶんの発走前オッズ（`live_odds.csv.gz`）を含む（FINDINGS.md §1）。
- 2021年以降を補うため `lauchunlok/HKJC-Scraping`（Selenium、1年あたり約6時間）を使う予定。
- 比較用に Kaggle の JRA データ（1986〜2021年）にも同じパイプラインを当てている。

## 特徴量

- 7個の集計: 馬の直近5走・20走の勝率、通算出走数、コース別・距離別勝率、騎手・調教師の365日勝率。
- 区間タイム由来: `sec1..4_time`、`sec1..4_lbw`（区間ごとの着差）、`sec_closing_delta`、`position_gain`。
- レース情報（競馬場、コース、距離、馬場、クラスの one-hot）、頭数、枠、`odds_rank_within_race`。
- 「with-odds」モデルは `winning_odds`、`implied_prob` などを加える。「no-odds」はそれらを除く。

## モデルと目的変数

- 1着かどうかの二値分類。LightGBM と XGBoost、両者の50/50平均。
- Benter 型の結合 `fund_prob^w × public_prob^(1−w)` を w ∈ [0,1] で掃引。

## 評価

- 時系列分割: 学習 2014〜2016、検証 2017（818レース）、外部検証 2018年上半期（学習を2017年まで延ばして再学習）。
- 1単位均等賭け、配当は確定配当（`all_dividends`）。Kelly 実験では資金が100HKDを切ったら停止。
- 単勝 Kelly 実験はオッズを4種類切り替える: 確定配当、最後に記録された発走前オッズ、最初に記録された朝オッズ、LightGBM で予測した朝オッズ。

## 結果

「Results」節（README）と FINDINGS.md より:

- モデルの性能（2017検証）: with-odds の LightGBM は AUC 0.7833、1番手的中 28.5%。no-odds は AUC 0.6782、22.9%。
- 馬連2頭ボックス: `lgb_no_odds` が 2017 で 817件・的中69・ROI +7.9%、2018H1 で 452件・40的中・+2.6%。`xgb_no_odds` は −6.5%、アンサンブルは −7.3%、with-odds の LightGBM は的中率12.6% だが −10.0%。
- 「Quinella filters」: 2頭のうち高い方のオッズが12以上のときだけ買うと 240件で +62.6%（2017）。だが2018H1 では同じ絞り込みが 119件・4的中・−1.2% に崩れた。
- 「Benter blend」: 単勝1番手では w=0.4（モデル4:市場6）が最良だが ROI −15.2%。馬連では w=1.0（モデルのみ）が最良。
- 「Other strategies」: 複勝、QPL、三連単（tierce）、四連単（quartet）はすべてマイナス（−3.1%〜−100%）。
- 「Kelly criterion」: 確定配当でオッズ判定すると均等1%で −26.8%、1/4 Kelly で −20.9%。朝オッズで判定すると的中率27.4%・ROI +119%、1/4 Kelly で +140%。

## 落とし穴と教訓（著者の記述）

- 元データの `race_id` が日付をまたいで再利用されていた（同じ 715 が2017年と2018年に出る）。日付・競馬場・レース番号から自前の主キーを作った。
- 直近成績の rolling は日付で並べて `shift(1)` しないと当該レースが混ざる。
- pandas の `get_dummies` が object 型を返して LightGBM が落ちる。
- LightGBM と XGBoost は似た誤りをするので平均しても伸びない。
- no-odds モデルの確率は較正が悪く、Kelly に直接入れると賭け金が暴れる。Platt や isotonic は未実施。

## 批判的に読む

- **区間タイム特徴量の時点が書かれていない**。`sec1..4_time`、`position_gain`（通過順位の上昇）、`sec_closing_delta` は、当該レースの値ならそのまま結果のリークになる。rolling 特徴量には `shift(1)` を明記しているのに、これらには書いていない。no-odds モデルの AUC 0.68 が小さいので過去走の値である可能性もあるが、README からは判断できない。
- **朝オッズで +119% は信じない方がよい**。確定配当で −27% の同じモデルが、判定に使うオッズを変えただけで +119% になるのは、払戻計算に朝オッズを使っている（実際の配当ではない）か、朝オッズのある1,510レースに偏りがあるかのどちらかを疑うべき。著者も「方向として読め」と書いている。
- 馬連の +7.9% と +2.6% は、それぞれ69件と40件の的中に依存する。馬連の配当の分散を考えると、どちらも0と区別できない。著者自身も「確認された優位ではない」と書いている。
- 2017年の検証で絞り込み（オッズ12以上）を選び、2018年で崩れた経過は、閾値の事後選択の失敗例として価値がある。
- 確定オッズを特徴量に入れたモデル（with-odds）の比較は、購入時点で知り得ない情報を使っている。

## keiba-ai での使い方

- 「オッズなしモデルで、市場が過小評価する組み合わせ券を買う」という仮説は JRA の馬連・ワイドでも検証する価値がある。単勝で負けても、組み合わせ券の市場は単勝ほど効率的でないかもしれない（[Hausch 1994](./1994-hausch-pricing-exotic-wagers.md)）。
- 検証で選んだ絞り込みを次の期間で凍結して試すと崩れる、という流れを実験計画に組み込む。検証・テストの2段を最低限とする。
- 主キーの重複（レースIDの再利用）や rolling の `shift(1)` は、データ取り込み時の自動テストにする。
- 区間タイム・通過順のような「レース中の情報」は、前走以前の値だけを使うことを特徴量の命名（`prev1_`、`prev_mean_` など）で強制する。

## 関連ノート

- [Benter 2019](./2019-benter-model.md): `fund^w × public^(1−w)` 型の結合の原型（Benter の第2段ロジットの簡略版）。
- [Hausch 1994](./1994-hausch-pricing-exotic-wagers.md): 単勝確率から組み合わせ券の価格を出す。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 上位2頭の確率計算。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): 絞り込みの事後選択。
- [jerrydaphantom 2026](./2026-jerrydaphantom-hkjc-ml-research.md)、[stevw 2026](./2026-stevw-hkjc-ml-research-platform.md): 同じ HKJC で、より慎重な評価。
- [Christy-Lo 2021](./2021-christylo-hkjc-random-forest-betting.md): 同じく香港データで小標本の大きな利益を報告した例。

## 検索語

香港競馬, HKJC, 馬連, 連贏, ボックス買い, オッズなしモデル, 朝オッズ, ベンター結合, 区間タイム, リーク, Hong Kong Jockey Club, quinella, quinella box, no-odds model, morning odds, Benter blend, fundamental probability, public probability, sectional times, data leakage, race_id collision, LightGBM, XGBoost, Kelly criterion

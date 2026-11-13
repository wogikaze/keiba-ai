---
title: Horse-Racing-Prediction---Optimized-Gambling-Strategy
authors: Christy-Lo, Chris Yeung
year: 2021
venue: GitHub
url: https://github.com/Christy-Lo/Horse-Racing-Prediction---Optimized-Gambling-Strategy
topic: practitioner
tags: grey-literature, hong-kong, hkjc, random-forest, place-bet, payout-error, season-stakes-leak, anti-example
verified: fulltext
importance: low
source: downloaded
source_version: web
---

# 香港競馬のランダムフォレストで「3000レース4万ドルの利益」: 払戻計算とリークの反面教師

> 一言で: HKJC の3年分（1万行超、98項目）でランダムフォレストを作り、3着内予測で複勝を買うと2,936レースで HK$41,084 の利益と報告した学生のグループ課題（GitHub スター約40）。ただし利益の計算は「複勝が当たったら（単勝オッズ − 1）× 10」で、複勝配当ではなく単勝オッズを使っている。特徴量の今季獲得賞金は取得時点の値で、著者自身が「未来のデータで過去を予測している」と認めている。数値は使えないが、典型的な誤りの見本として価値がある。

## データ

- HKJC の結果ページをスクレイピングした過去3年分、1万行超、生の項目98個（「Overview」）。
- 項目の例: 単勝オッズ、今季獲得賞金（season stakes）、レーティング、枠。

## 特徴量・モデル・目的変数

- 目的変数は「1着」フラグと「3着内」フラグの二値分類。
- ランダムフォレスト。特徴量の選び方を4通り比較: 全64個、重要度0.01以上の9個、正解率が最大になる組み合わせ（11〜14個）、それをグリッドサーチで調整したもの。

## 評価と結果

- 1レース$10、「当たれば（win odd − 1）× 10、外れれば −10」（「Best Model Performance」）。
- 「Experiments」の表: 1着予測は正解率 0.90〜0.91 で純損益 −32〜+8。3着内予測は正解率 0.75〜0.76 で純損益 +34,933〜+41,084。
- 最良モデル: 2,936レース中522回「3着内」と予測し、328回的中。純損益 +41,084。

## 落とし穴（著者の記述）

- 「Limitation and solution」: HKJC のサイトでは一部の項目の履歴が取れず、例えば今季獲得賞金は現時点の値しかない。これには当該レースの勝利の効果が含まれるので、未来のデータで過去を予測していることになり、モデルを大きく誤らせうる、と書いている。

## 批判的に読む

- **払戻の誤り**: 3着内予測で賭ける複勝は、単勝オッズではなく複勝配当で払われる。複勝配当は単勝オッズよりずっと低い。単勝オッズで計算すれば、3着内に入った人気薄が単勝並みの払戻を生み、利益は大きく水増しされる。328的中で4.1万ドル（1的中あたり平均約$140、すなわちオッズ約15倍）は複勝ではあり得ない水準。
- **リーク**: 今季獲得賞金は当該レースの結果を含む。目的変数（3着内）と直接つながる項目なので、正解率・利益とも過大になる。
- **確定単勝オッズを特徴量に入れている**。購入時点では知り得ない。
- 正解率（0.90）は「全部外れと予測する」だけで得られる基準（1着でない割合≈0.92）以下で、指標として意味がない。
- 分割の方法（時系列かランダムか）が README に書かれていない。
- 2,936件の「レース」は実際には出走馬単位の行で、賭けた回数は522回。

## keiba-ai での使い方

- 券種ごとの払戻計算を関数として1か所にまとめ、テストで固める。複勝・ワイドは実際の払戻（JRA の払戻金データ）を使い、単勝オッズからの換算は使わない。
- 「取得時点の値」しかない項目（通算賞金、現在のレーティング、現在の所属など）は、出走時点の値を再構成できない限り特徴量に使わない。netkeiba の馬ページの「現在の」情報も同じ危険がある。
- 不均衡な二値分類の正解率は報告しない。log loss、Brier、多数派予測との比較を出す。
- リークや払戻の誤りの検出例として、実験レビューのチェックリストに載せる。

## 関連ノート

- [catowabisabi 2026](./2026-catowabisabi-hkjc-quinella-lightgbm.md): 香港データで小標本の大きな利益を報告した別の例。
- [Hausch 1981](./1981-hausch-racetrack-market-efficiency.md): 複勝の期待値を単勝オッズから正しく近似する方法。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): リークを意識した評価。
- [stevw 2026](./2026-stevw-hkjc-ml-research-platform.md): 頭数による複勝の着数や同着を含め払戻計算をテストで固めた例。

## 検索語

香港競馬, ランダムフォレスト, 複勝, 払戻計算の誤り, 今季獲得賞金, リーク, 正解率の罠, 反面教師, Hong Kong Jockey Club, random forest, place bet, payout calculation error, win odds vs place dividend, season stakes leakage, look-ahead bias, accuracy paradox, class imbalance

---
title: Predicting Horse Races — Learnings from revisiting after a 4 year hiatus
authors: qemtek (Christopher Collins)
year: 2024
venue: Medium
url: https://medium.com/@qemtek/predicting-horse-races-learnings-from-revisiting-after-a-4-year-hiatus-9005b15cd2eb
topic: practitioner
tags: grey-literature, uk-ireland, racing-post-scraping, betfair-exchange, xgboost, target-design, finish-time, speed-target, failure-story
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 3 年かけて勝てなかった英国競馬モデルを 4 年後に見直す：目的変数の分布と「速度」への変換

> 一言で: 英国・アイルランドの競馬データ（無料のスクレイピングツールで取得）で 3 年間モデルを作り、Betfair で自動投票まで組んだが、一度も黒字にならず諦めた。4 年後にコードを読み直して、「勝ち馬との着差（ovr_btn）」という目的変数の分布が悪かったと気づいた。そこで目的を「レースの走破時計」と「各馬のずれ」の 2 段に分けた。第 1 段では平地／障害でデータを分け、時計ではなく速度（距離 / 時間）を予測すると、MAE が 3.66 秒 → 3.54 秒 → 3.365 秒と下がった。

## データ

- 本文では「誰かが作った、大量の競馬データを無料でスクレイピングできる GitHub リポジトリ」とだけ書かれている（「The Journey into Horse Racing」の節）。著者の GitHub には Racing Post の結果を CSV に取る `rpscrape` のフォークと Betfair SP のスクレイパー `bfsp_scraper` があるので、英国・アイルランド（フランスも含む）の Racing Post データだと推測できる。期間・件数は書かれていない。
- 市場は Betfair Exchange。著者は「取引所では 1/odds が市場の確率になるが、ブックメーカーはリスクを抑えるためにオッズを操作しうる」と注記している。

## 最初の失敗（「Experience Matters」の節）

- 目的変数は勝ち馬との着差 `ovr_btn`（勝ち馬は 0）。理由は 2 つあった。勝てなくても僅差なら情報として拾える。レース内の差に集中させられる（走破時計そのものだと、全馬に 600 秒前後を出しておけば相対誤差は小さく見えてしまう）。
- この理由自体は正しかったが、目的変数の分布（0 に大きな山があり、長い裾がある）を見ていなかった。XGBoost は分布の仮定を置かないが、不規則な分布だとモデルが 0 を予測する方向に強く偏る。
- 結果として 3 年間（夜と週末）の作業でも黒字は一度も出ず、諦めた。

## 作り直し（2 段構成）

- **モデル 1**: レース全体の走破時計（勝ち時計）を、距離・馬場状態（going）・コース・出走馬の質などから予測する。
- **モデル 2**: 各馬がその時計からどれだけずれるかを予測する（記事の時点では未完成で、Part 2 予定）。
- 分けた理由は、レース条件の効果と馬の間の差を別々に学習させ、目的変数の分布を素直にするため。

## 結果（モデル 1、XGBoost、評価指標は MAE）

- 全データで 1 モデル: MAE 3.66 秒。重要度は距離・レース種別（平地か否か）・同コース同距離の過去平均時計が上位で、馬場状態はほぼ 0（「Model 1」の節）。
- 平地と非平地（障害など）で分けた 2 モデル: 平地 1.71 秒、非平地 6.8 秒、合わせて 3.54 秒（約 3.5% 改善）。平均距離は平地 1,700 m、非平地 3,900 m。
- 速度（m/s）を予測して時計に戻す: 平地 1.58 秒、非平地 6.57 秒、合わせて 3.365 秒（前のモデルから約 9% 改善）（「An Unexpected Improvement」の節）。
- 速度を目的にすると、それまで重要度がほぼ 0 だった馬場状態が上位に来た。非平地の重要度からは、フランスのデータに問題がありそうなことも分かった。
- 著者の解釈はバイアス–バリアンスのトレードオフで、「時計を距離で割って問題を単純にしたので、同じモデルでよく当てはまるようになった」としている。

## 批判的に読む

- 賭けの成績は書かれていない。黒字化しなかったという定性的な報告だけで、評価方法・期間・オッズも不明。
- 改善はレースの勝ち時計の MAE だけで、勝率の精度や市場との比較にはまだつながっていない。モデル 2 の続編は見当たらない。
- 学習とテストの分け方（時系列かどうか）が書かれていない。「同コース同距離の過去平均時計」が当該レースを含まない集計かどうかも分からない。
- 平地と障害を分けたこと、速度に変換したことは、競馬の時計を扱う研究では標準的な処理（距離で正規化した速度指数）である。新しい知見というより、実践者がつまずく場所の記録として価値がある。

## keiba-ai での使い方

- **目的変数の分布を先に見る**: 着差・タイム差を目的にするときは、0 の山と裾の形を確かめ、変換（速度、対数、分位）や 2 段構成を検討する。実験 README の「仮説」に分布の図を入れる習慣にする。
- **時計系の目的は速度で**: JRA の走破時計を目的にするなら、芝・ダート・障害で分け、距離で割った速度（または基準タイムとの差）を予測する。馬場状態の効果が見えやすくなる。
- **2 段分解**: 「レース水準（ペース・馬場で決まる時計）」と「馬ごとの偏差」を分ける構成は、スピード指数の作り方（基準タイム＋馬場差）と同じ発想で、特徴量としても目的変数としても試せる。

## 関連ノート

- [Oki ほか 1984](./1984-oki-turf-dirt-running-time.md)、[Lo 1994](./1994-lo-running-time-japan.md)、[Maeda ほか 2012](./2012-maeda-track-surface-condition-racing-times.md) — 走破時計と馬場・距離の関係を扱う研究。
- [Rosenbloom 2003](./2003-rosenbloom-beyer-speed-probability-model.md) — スピード指数から勝率へ。
- [Leung & Leung 2023](./2023-leung-annotated-benter-paper.md) — 市場の確率を超えることの難しさ（香港）。
- [Franck ほか 2010](./2010-franck-bookmakers-vs-betting-exchange.md) — ブックメーカーと取引所の違い。

## 検索語

英国競馬 予測 失敗談, 目的変数 設計, 着差 予測, 走破時計 速度 変換, 平地 障害 分割, XGBoost MAE, Betfair 自動投票, horse racing target design, beaten lengths ovr_btn, predict speed instead of finish time, Racing Post scraper rpscrape

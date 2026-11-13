---
title: なぜ競馬AIは実戦で死ぬのか（本の無料第1章と関連記事4本）
authors: punch_cola
year: 2026
venue: Zenn（本 1,500円、第1章は無料公開）＋ Zenn 記事4本
url: https://zenn.dev/punch_cola/books/b3bcedf9d97a29
topic: practitioner
tags: grey-literature, lightgbm, jra-van, walk-forward, multiple-testing, deflated-sharpe, benjamini-hochberg, bayesian-updating, leak-detection
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# なぜ競馬AIは実戦で死ぬのか（punch_cola 2026）

> 一言で: JRA-VAN の5年分（15,569レース）で LightGBM の4成分アンサンブルを作り、256戦略を grid search した。戦略選定期間では回収率 +170〜225% の戦略が見つかったが、触れていない最新期間（完全 OOS）では1件も発火しなかった。Bonferroni 補正では生存 0/177。その経験から、リーク検出、walk-forward、多重検定補正、ベイズ逐次更新による停止判断を、Python コード付きの検証フレームとしてまとめた。

本の第1章（無料）と、同じ著者の Zenn 記事4本（リーク自動検出、walk-forward、多重検定補正、ベイズ逐次更新）に基づく。本の第2〜6章は読んでいない。記事は本の各章の要約版になっている。

## データ

- JRA-VAN Data Lab. の5年分、15,569レース・207,198出走（第1章「著者の検証規模」）。
- 代替として netkeiba のスクレイピングにも触れているが、本の前提は JRA-VAN SDK。

## 特徴量

- 215特徴量。調教タイム（坂路・ウッドチップ）、血統、騎手、オッズなど（第1章）。詳細は有料部分。
- オッズを特徴量に含むので、モデルは市場情報の上に積む形になる。

## モデルと目的変数

- LightGBM の4成分アンサンブル: 二値分類（勝ち）、高オッズに重みを付けた二値分類、ランキング、3着内分類。シード3種（第1章）。
- 試したアプローチは27種（単純な二値分類から多目的アンサンブル、回収率の直接予測まで）、分散低減法9種（ターゲット変換、Huber loss、分位数回帰など）、フィルター戦略30以上（馬体重、距離、競馬場、オッズ分散など）。
- 戦略は「エッジ閾値 × グレード条件 × 賭け方 × 上位K頭」の256通り。

## 評価

- 拡張ウィンドウの walk-forward 4 fold。訓練 2021-01〜2022-12 → 検証 2023、… → 検証 2026（途中）（記事「競馬 AI で K-Fold を使ってはいけない」）。
- 完全 OOS: Fold1〜3 だけで grid search と多重検定補正をし、Fold4 には選んだ戦略を盲目的に適用する。Fold4 を見たら方針転換しない。
- 多重検定補正は Bonferroni（FWER）、Benjamini-Hochberg（FDR）、Deflated Sharpe Ratio（Bailey & López de Prado 2014）。
- 回収率の計算方法（確定オッズかどうか）は無料部分に明記されていない。
- 運用段階は実ベットなしのシャドウトレード（半年間）。

## 結果

- 単一目的の二値分類: AUC は市場の暗黙確率と互角（差 0.001）（第1章の表）。
- 多目的アンサンブル: 戦略選定期間の回収率 +170〜225%、OOS では発火0件。
- 回収率の直接予測: 全敗（最良でも約 −10%）。分散低減を全部試しても改善しない。
- 256戦略のうち n≥20 ベットで評価できたのは177戦略。Bonferroni 補正で生存 0/177。
- BH 法の生存数は、第1章では 35/177、記事「100 戦略試して最良が +170%」では 56/177 と書かれていて一致しない。最良戦略の Deflated Sharpe の p 値は約 0.55。
- 冒頭の例: 過去3年で回収率 270%、p=0.0026、walk-forward 4 fold すべてプラスの戦略が、最新データでは推奨ベットを1件も出さなかった。

## 手法の中身（記事から）

- **リーク自動検出3種**（記事「あなたの競馬 AI の backtest は既に壊れている」）:
  1. 単一特徴量 AUC スキャン。オッズ・人気以外で単独 AUC > 0.85 ならリークを疑う。正常な特徴量は 0.55〜0.70。
  2. ランダム分割と時系列分割の AUC ギャップ。0.03 未満なら概ね健全、0.05 以上でリークか強い分布シフト。
  3. point-in-time 監査。行を抜き取り、過去データだけで集計し直した値とパイプラインの出力を突き合わせる。
  - 1 と 2 を CI ゲートにして、閾値を超えたら AssertionError で落とす。
- **walk-forward の落とし穴3つ**: 全期間で特徴量を計算してから分割する（expanding mean のリーク）、fold ごとに戦略を選ぶ、多数の戦略から最良を選ぶ（選択バイアス）。
- **ベイズ逐次更新**（記事「競馬 AI は『何ベットで見切る』べきか」）: 的中率は Beta-Binomial、平均損益は Normal-Inverse-Gamma の共役事前分布で更新し、P(平均損益 > 0) を出す。n<10 は観察、P<0.50 かつ n≥30 で停止、P>0.80 かつ n≥50 で増額、のように閾値を事前に決めて機械的に運用する。

## 落とし穴と教訓

- 派手なバックテスト数字は、選択バイアスと配当の重い裾によるノイズで説明できる。
- 戦略を絞るほど発火頻度が下がり、年5〜15ベットでは統計的に何も言えない。
- walk-forward だけでは選択バイアスは防げない。補正と完全 OOS の両方が要る。
- AI コーディング支援に「騎手勝率の特徴量を作って」と頼むと、未来を含む全期間集計を素直に書くことがある。
- 停止の閾値は負けが込む前に決める。後から動かすのは運用段階での選択バイアス。

## 批判的に読む

- 方法論は標準的で正しいが、競馬固有の新しい知見は少ない。本の価値は、256戦略が OOS で全滅したという具体例と、それを説明する道具一式にある。
- BH 法の生存数が本と記事で食い違う（35 と 56）。どちらかが別の集計条件かもしれないが、説明はない。
- 「AUC は 0.80〜0.85 が高水準」「単独 AUC > 0.85 でリーク濃厚」は経験則で、根拠のデータは示されていない。単勝の二値分類では、オッズだけで AUC 0.8 前後が出るので、オッズを含むモデルの AUC は市場との差で見るべき（著者も市場と 0.001 差と書いている）。
- 回収率の計算方法（確定オッズか、締切前オッズか）が無料部分では不明。
- 戦略の閾値や条件を意図的に伏せているので、どんな戦略が死んだのかは分からない。
- ベイズ逐次更新の損益の正規近似は、配当の裾が重い馬券では粗い。高配当の単勝や三連系では、事後確率が少数の的中に引きずられる。

## keiba-ai での使い方

- **リーク検出の CI ゲート**: 単一特徴量 AUC スキャン（オッズ系を除く）と、ランダム分割 vs 時系列分割の AUC ギャップを、特徴量生成後の自動チェックに入れる。ランダム分割は評価には使わないが、リーク検出の比較対照としては使える（評価ルールとは別の用途として明記する）。
- **完全 OOS の聖域化**: 最終テスト期間を1つ決め、戦略・閾値の選定には使わない。実験 README に「テスト期間を見た回数」を書く。
- **多重検定補正**: 1つの実験で試した戦略数を results.json に記録し、BH 法の q 値と Deflated Sharpe を併記する（[Bailey 2014](./2014-bailey-deflated-sharpe-ratio.md)）。
- **運用時の停止ルール**: 実運用やシャドウ運用を始めるときは、Beta-Binomial / NIG の事後確率による停止・増額の閾値を事前に config.yaml に書く。

## 関連ノート

- [Bailey 2014](./2014-bailey-deflated-sharpe-ratio.md) — Deflated Sharpe Ratio の原典。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md) — バックテスト過学習の確率。
- [Bergmeir 2018](./2018-bergmeir-cv-time-series.md)、[Cerqueira 2020](./2020-cerqueira-time-series-performance-estimation.md) — 時系列の交差検証。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md) — リークを意識した評価。
- [marunage_kacho 2026](./2026-marunagekacho-roi177-mirages.md) — 299モデルからの選択で ROI 177% が出た例。
- [rindokulab 2026 本](./2026-rindokulab-recovery-100-discarded.md) — 監査で3回の「勝てる数字」を棄却した例。
- [architectJapan 2026](./2026-architectjapan-leak-audit-calibration.md) — リーク監査と較正。
- [umascore 2026](./2026-umascore-backtest-forward-decay.md) — バックテストとフォワードの乖離。

## 検索語

競馬AI、実戦で死ぬ、OOS、完全OOS、アウトオブサンプル、walk-forward、ウォークフォワード、K-Fold、選択バイアス、多重検定、Bonferroni、BH法、Benjamini-Hochberg、Deflated Sharpe Ratio、ベイズ逐次更新、Beta-Binomial、Normal-Inverse-Gamma、シャドウトレード、リーク検出、単一特徴量AUC、AUCギャップ、point-in-time、JRA-VAN、grid search、backtest overfitting, multiple testing correction, false discovery rate, sequential Bayesian stopping

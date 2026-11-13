---
title: Keiba AI Prediction System (JRA) — 馬単の EV 戦略と「組合せオッズがないバックテストは検証にならない」問題
authors: tsukasaI
year: 2025
venue: GitHub
url: https://github.com/tsukasaI/keiba-ai
topic: practitioner
tags: grey-literature, github, kaggle-jra-dataset, netkeiba-scraping, lightgbm, position-probability, harville, exacta, expected-value, kelly, calibration, temperature-scaling, paper-trading, post-race-odds-leak, rust, onnx
verified: fulltext
importance: high
source: downloaded
source_version: web
---

# 馬単 EV 戦略のバックテスト +19.3% を自ら「未検証」と格下げし、フォワードのペーパートレードに切り替えた記録

> 一言で: Kaggle の JRA データセット（2019〜2021 年分を使用）と netkeiba スクレイピングで、着順の確率分布を出す LightGBM を作り、Harville で馬単などの組合せ確率に変換して EV > 1 の組合せを買う。ウォークフォワードのバックテストで ROI +19.3% が出たが、Kaggle にも netkeiba の過去ページにも「外れた組合せの発走前オッズ」が残っていないため、EV 判定に事後オッズか単勝からの推定オッズを使っており、この数字は検証になっていないと著者自身が明記した。実オッズで確かめるため、発走前に組合せオッズを記録して公式払戻で精算するペーパートレードの仕組みを作った。作る過程で、ライブ予測が一度も正しい買い目を出していなかったバグ 2 件も見つかった。

原本は README（`library/2025-tsukasai-exacta-ev/source.txt`）。リポジトリは 2025 年 12 月作成で、README は 2026 年まで更新されている。詳細は同梱の CLAUDE.md（添付 `attachments/claude-md.txt`）の「Known Issues & Limitations」と `docs/PAPER_TRADING.md`（添付 `attachments/paper-trading.txt`）にある。ボートレース予測の別プロジェクトからの移植で、README に両者の比較表がある。

## データ

- Kaggle「JRA Horse Racing Dataset」（takamotoki、1986〜2021 年）のうち 2019〜2021 年を使う。レース結果・オッズ・ラップ・コーナー通過順を含むが、オッズは的中組合せの払戻（事後）だけ（README「Data Source」、CLAUDE.md）。
- netkeiba のスクレイピング（2022〜2025 年）: 各馬の確定単勝オッズと的中組合せの払戻は取れるが、組合せオッズのページはレース後に 404 になり、外れた組合せのオッズは残らない（CLAUDE.md「Data Source」）。
- 調教データは無料データにないので未使用。JRA-VAN の導入を将来課題にしている。

## 特徴量

README「Features」の表と「23 Features Scraped」の表: 馬齢・性別・馬体重・斤量・枠番、騎手と調教師の勝率・複勝率、距離・芝ダ・馬場状態・競馬場、過去 3/5 走の平均着順と勝率・複勝率、コーナー通過順から作る脚質（逃げ・先行・差し）、父と母父の適性。最終モデルは 39 特徴（CLAUDE.md の「Feature Count Mismatch」の修正記録）。

## モデルと目的変数

- 目的変数: 各馬の着順の確率分布（勝率だけでなく）。全券種に拡張しやすいから、という理由（CLAUDE.md）。
- LightGBM が既定。CatBoost・XGBoost・アンサンブルも選べ、Optuna でハイパーパラメータ探索。
- 確率較正: 温度スケーリングとビニング。
- 組合せ確率: 全券種（馬単・三連単・馬連・三連複・ワイド）を Harville の式で計算。
- 推論は ONNX に書き出して Rust の単一バイナリで動かす。

## 評価

- ウォークフォワードのバックテスト（Python と Rust の両方）。
- 賭け方: EV = 予測確率 × オッズ が閾値（既定 1.0、例では 1.2）を超える組合せを買う。賭け金は Kelly。
- 回収率の計算: Kaggle では的中組合せの事後払戻しかないため、EV 判定と払戻の両方に事後オッズが入る。netkeiba 由来の期間では、組合せオッズを単勝オッズの幾何平均から推定している（CLAUDE.md「No Real Combination Odds Anywhere」）。

## 結果

- ウォークフォワードのバックテストで ROI +19.3%（較正あり）。README の「Development Phases」で「post-race/estimated odds に基づく。実組合せオッズでは未検証」と注記している。
- ペーパートレードの実績はまだない。「No real races have been recorded yet, so no verified ROI number exists yet」（CLAUDE.md）。

## 落とし穴と教訓（著者の記述）

- **事後オッズのバックテストは楽観的になる**。データにあるのは的中組合せのオッズだけなので、外れた組合せについて EV を判定できない。バックテストの CLI は警告を表示するようにした。
- **検証の道筋は 2 つ**: (1) 発走前に実オッズを記録するフォワードのペーパートレード、(2) 有料の JRA-VAN の過去オッズ。(1) を `paper-record → paper-settle → paper-report` として実装した。記録は締切前に限り、公式払戻で精算する。賭けた時点のオッズと確定オッズのずれ（スリッページ）は残る注意点として明記している（PAPER_TRADING.md「Settlement accuracy and its limit」）。
- **ライブ経路のバグ 2 件**（CLAUDE.md「Live Betting Pipeline Never Produced Correct Bets」）:
  - 予測は netkeiba の `horse_id` をキーにし、オッズはゼロ埋めの馬番をキーにしていたため、EV の結合が常に失敗し、`live` は毎回「EV 閾値を満たす買い目なし」と出していた。
  - EV は小数オッズ（例 12.5）をそのまま使っていたが、Kelly の計算では 100 で割っており、全ての賭け金が最小単位に潰れていた。
  - どちらもペーパートレードを作る過程で初めて見つかった。

## 批判的に読む

- 的中組合せのオッズしかない状態で EV フィルタを掛けると、「当たった組合せについてだけ EV が高く見える」という選択の偏りが入る。外れた組合せは EV が分からないので、判定のしかたによっては買わなかった扱いになり、損失が数えられない。+19.3% はこの偏りでほぼ説明できる可能性があり、著者が未検証と格下げしたのは妥当。
- 単勝オッズの幾何平均から組合せオッズを推定する方法は、実際の組合せオッズの歪み（人気薄の組合せが過大に売れる・売れないなど）を反映しない。EV > 1 の判定はまさにこの歪みに依存するので、推定オッズでの ROI は意味が薄い。
- 2019〜2021 年の 3 年分だけで学習しており、学習期間は短い。
- 同じ予測モデルの精度指標（logloss、的中率）は README にない。

## keiba-ai での使い方

- **組合せ馬券の回収率評価には、外れた組合せも含む発走前オッズが必要**、という点を評価ルールの前提として ADR に書く。単勝・複勝は netkeiba の確定オッズで評価できても、馬単・三連単は事後払戻だけでは EV 戦略を評価できない。
- 組合せオッズの入手（JRA-VAN の時系列オッズ、または締切前の記録）を、データ計画の優先課題にする。
- ペーパートレードの 3 段（record → settle → report）、記録時刻と公式時刻の保存、公式払戻での精算は、keiba-ai のフォワード評価の設計にそのまま使える。
- キー（horse_id と馬番）の不一致、オッズの単位（小数か 100 円あたりか）の不一致は、結合テストで必ず確かめる項目としてテストに入れる。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 組合せ確率の計算。
- [Lo 1994](./1994-lo-comparison-harville-henery.md): Harville の偏りと Henery との比較。
- [Hausch 1994](./1994-hausch-pricing-exotic-wagers.md): 組合せ馬券の価格付け。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): リークを意識した評価。
- [Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 賭けた時点と確定のオッズのずれ。
- [Sol12378 2026](./2026-sol12378-masters-kit.md): 賭けた時点のオッズに 0.8 を掛けて確定倍率の低下を見込んだ実装。
- [Shogo391 2026](./2026-shogo391-kaiba-ev-autobet.md): 確定後オッズで再構成した区間を含む回収率の例。

## 検索語

馬単, 三連単, 組合せオッズ, 事後オッズ, 確定払戻, 発走前オッズ, 推定オッズ, ペーパートレード, フォワード検証, 期待値, EV フィルタ, Kelly, 温度スケーリング, Harville, 着順確率, Kaggle JRA データセット, exacta, trifecta, combination odds, post-race odds bias, paper trading, forward test, slippage, walk-forward backtest

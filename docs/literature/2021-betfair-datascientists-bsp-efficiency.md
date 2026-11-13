---
title: Analysing and Predicting the BSP（ほか Betfair Automation Hub の競馬チュートリアル 2 本）
authors: Tom Bishop（Betfair Australia Data Scientists / The Automation Hub）
year: 2021
venue: Betfair Automation Hub（betfair-datascientists.github.io）
url: https://betfair-datascientists.github.io/tutorials/analysingAndPredictingBSP/
topic: practitioner
tags: grey-literature, betfair-exchange, australia, thoroughbred, bsp, market-efficiency, logloss, backtesting, stream-data, betting-angles, p-value, out-of-sample
verified: fulltext
importance: high
source: downloaded
source_version: web
---

# 豪州 Betfair の競馬市場で「BSP は効率的か」を logloss で測り、BSP を予測する／バックテストの価格をどう選ぶか

> 一言で: 豪州の平地競馬 12 か月分（2020-07〜2021-06）の Betfair 取引所ストリームデータで、発走前の各時点の価格と Betfair Starting Price（BSP）の精度を比べた。「予測確率 vs 実際の勝率」の散布図は偏り（bias）しか測れず、効率性は logloss で比べるべきだと示した（BSP の logloss 0.2757、120 秒前 0.2763 と発走に近づくほど単調に良くなる）。サイトが出す予想 BSP（near price）は 60 秒キャッシュのため弱く、最良バック価格や幾何平均の中値のほうが BSP をよく当てる。添付の 2 本は、時点別価格でのバックテストの作り方と、時系列ホールドアウト＋p 値で「賭けの切り口」を検証する手順。

原本は BSP の記事（主）。同じ著者の「Backtesting wagering models with Betfair JSON stream data」と「Automated Betting Angles in Python」を添付している。いずれも Betfair 社員が書いた教材で、個人の開発記録ではない。ただ、実際の取引所データで「どの価格で評価するか」を細かく扱った実践資料として扱う。

## データ

- Betfair の過去ストリームデータ（PRO 区分、50 ms ごとの板の状態）を `betfairlightweight` で再生する。対象は豪州の平地競馬（thoroughbred）の全単勝市場で、2020-07〜2021-06 の 12 か月。
- 抽出: 発走予定時刻の 2 分前から 10 秒ごとに、売買高・near/far price・BSP プールのバック額とレイ負債額・上位 5 段の板を記録した。市場が停止する直前の状態も取る。価格の行は 3,937,805 行（BSP の記事「Parsing Selection Prices」の表示）。
- 勝敗と BSP は別ファイルにした。走る馬の属性（騎手・馬齢など）は Betfair Hub の非公開 API（racecard / raceevent）から取った（「Betting Angles」の記事）。

## BSP の記事の内容と結果

- **BSP の取引量**: 平均的な平地競馬の市場で、通常の取引が約 9.8 万ドル、BSP での取引が約 7,300 ドル。BSP は全体の約 7%。
- **効率性の測り方**: 散布図（暗示確率 vs 実勝率）だと、BSP も発走 2 分前の価格もほぼ同じように「完璧」に見える。著者は、散布図が測るのは系統的な偏りだけだと指摘する。全馬に平均勝率 10.25%（頭数の逆数相当）を割り当てる予測でも散布図は通ってしまうが、それは効率的な予測ではない。代わりに logloss を使う。結果は BSP 0.275679、発走 0 秒前 0.275824、30 秒前 0.275999、60 秒前 0.276044、90 秒前 0.276206、120 秒前 0.276256。発走に近づくほど単調に良くなり、BSP が最も良い（「Logloss at Different Time Points」の表）。
- **BSP の予測（発走予定時刻ちょうど）**: 相対 MAE（|推定−BSP|/BSP）で比べると、最良バック 0.0917、ラダー中値 0.0932、幾何平均の中値 0.0944、最良レイ 0.1031、near price 0.1213、far price 0.5784。
- **市場停止直前**: 幾何平均の中値 0.0396、ラダー中値 0.0425、最良バック 0.0636、near price 0.0771。near price が弱いのは 60 秒ごとにしか更新されない（キャッシュ）ため。著者自身もこれで投票ロジックに問題を起こしていた。
- **ランダムフォレストで BSP を予測**: 板と BSP プールから「プールを埋めるのに必要な加重平均価格（WAP）」という特徴を作り、11 特徴で学習した（学習 119,822 行、テスト 39,941 行）。発走予定時刻のテストで 0.0889（最良バック 0.0919）、発走 10 秒後のスライスで 0.0792（最良バック 0.0847）。どちらも既存の推定を上回った。
- 著者の主張: BSP は投票時点では分からないので、事前モデルの開発や賭け金の計算に知らずに BSP を漏らす人が多い。最終 BSP がどこに落ちるかも不確実性の一つで、それ自体が予測の対象になる。

## 添付 1: レーティングのバックテスト

- バックテストの問いを 2 つに分ける。(1) 過去のその時点で自分の予測確率はいくつだったか。(2) その予測で、どのオッズで、いくら賭けたか。この記事は (2) を扱う。
- BSP で評価するのが最も簡単だが、市場によって流動性が違い、大きな賭けは BSP を動かす。BSP のない市場も多い。直前の取引価格（LTP）は「常に最後に約定する」ことが不可能なので不確実性がある。
- Kelly のような比例賭けを BSP で行うと、賭け金の計算に BSP そのものが入る。BSP は事前に分からないため、実際には推定値で賭け金を決めることになり、その誤差がバックテストより利益を削る。
- 予想サービスの過去レーティングは後から修正されている場合があり、(1) が破れることへの注意もある。例に使った Betfair の豪州平地モデルのレーティングは 2021-02-28 以降しかなく、期間が短いので信頼できないと著者自身が書いている。

## 添付 2: 「賭けの切り口」の検証

- 基礎からのファンダメンタルモデルは非常に難しい。現実の取引所の自動化は「市場は正しいが X だけ違う」という上からの小さな補正（切り口）が多い、という立場。
- データを見る前に 2021 年 4〜6 月を「テスト」として切り離した（学習 119,244 行、テスト 40,783 行）。
- 馬ごとの過去の回収率をそのまま並べると、1 回だけ BSP 270 倍で勝った馬が 1 位になる。そこで賭け数・利益・平均オッズから、偶然でその利益が出る確率（p 値）を計算する検定を Python で実装した。例: 「Albany 1000 m の内 3 枠」はバック回収率ほぼ 500% だが 2 頭だけで、p 値は約 50%。
- 距離や枠は意味の近いもの（短距離帯、内枠 1〜3 など）でまとめ、標本を増やす。
- p 値で絞った上位 5 つのレイ戦略は、テスト期間でも学習期間と同程度の利益だった。ただしレイは小さな勝ちと大きな負けの分布なので頑健ではないと注意している。p-hacking の危険も明記している。

## 批判的に読む

- 一番の価値は、評価の考え方（散布図＝偏り、logloss＝情報量、時点別価格、BSP のリーク）にある。数値は豪州の取引所市場（控除率ではなく手数料）の話で、JRA のパリミュチュエルにそのままは移せない。
- ランダムフォレストの BSP 予測は、`train_test_split` によるランダム分割で評価している。同じレースの馬が学習とテストに分かれるので、楽観的になりうる。発走 10 秒後のスライスでの検証も、同じ期間・同じ市場の別時点で、時系列の外挿ではない。
- logloss の差（0.2757 対 0.2763）は小さく、統計的な有意性は示されていない。
- 豪州・12 か月に限られ、他の年・他の国で同じ傾向かは分からない。

## keiba-ai での使い方

- **市場の効率性は logloss（または Benter の疑似 $R^2$）で測る**: 単勝オッズの校正図だけで「市場は効率的」と判断しない。JRA でも、発走 N 分前のオッズと確定オッズの logloss を時点別に並べ、市場が締切に向けてどれだけ鋭くなるかを測る。投票時点のオッズで評価する根拠にもなる。
- **確定オッズのリークを防ぐ**: JRA の確定オッズは BSP と同じく「投票時点では分からない」値である。特徴量にも賭け金計算にも使わない。使うなら「締切 N 分前のオッズ」を別に収集する。収集できない期間は、確定オッズを使った評価だと明記する。
- **確定オッズの予測**: 直前オッズから確定オッズを予測するモデル（ランダムフォレスト・板の代わりに票数の推移）を作れば、期待値の計算と賭け金の決定に使える。実験候補。
- **切り口の検証手順**: 「データを見る前にテスト期間を切る」「p 値で偶然を除く」「意味の近い水準をまとめる」は、騎手・枠・コースなどの単純な切り口を試すときのチェックリストとしてそのまま使える。

## 関連ノート

- [Leung & Leung 2023](./2023-leung-annotated-benter-paper.md) — 香港の大衆確率を疑似 $R^2$ で年代別に測った再現。
- [Benter 1994](./2019-benter-model.md) — 市場確率との結合と、オッズの揺れの問題。
- [Hanyu ほか 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md) — JRA の締切直前のオッズの動き。
- [Franck ほか 2010](./2010-franck-bookmakers-vs-betting-exchange.md) — 取引所とブックメーカーの効率性の比較。
- [Walsh & Joshi 2024](./2024-walsh-calibration-vs-accuracy-betting.md) — 校正と精度、賭けの成績。
- [Gneiting & Raftery 2007](./2007-gneiting-proper-scoring-rules.md) — logloss などの適切なスコア。
- [Bailey ほか 2017](./2017-bailey-probability-backtest-overfitting.md) — 多数の切り口を試すことによる過学習。
- [qemtek 2024](./2024-qemtek-revisiting-after-hiatus.md) — Betfair で自動投票まで組んだ個人の失敗談。

## 検索語

Betfair BSP 効率性, 取引所 オッズ logloss, 校正図 偏り 効率性 の違い, 確定オッズ リーク, 締切直前 オッズ 予測, 時点別オッズ バックテスト, 賭けの切り口 p値, Betfair Starting Price prediction, near price far price, market efficiency logloss, betfairlightweight stream data backtest, betting angles statistical significance

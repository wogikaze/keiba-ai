---
title: HKJC Horse-Racing ML Research Platform
authors: stevw-repo
year: 2026
venue: GitHub
url: https://github.com/stevw-repo/HKJC-Horse-Racing-ML-Research-Project
topic: practitioner
tags: grey-literature, hong-kong, hkjc, conditional-logit, harville, model-zoo, walk-forward, leakage-canary, kelly, rebate, nlp, negative-result
verified: fulltext
importance: high
source: downloaded
source_version: web
---

# 香港競馬の研究基盤: 20季のウォークフォワードで「どのモデルも控除率ぶん負ける」

> 一言で: HKJC の2006〜2026年（1,697開催）を自前で集め、条件付きロジット、GBM 各種、LambdaMART、MLP、FT-Transformer、アンサンブルを同じウォークフォワードで比べた個人の研究基盤。モデルの選び方でも賭け金の決め方でも、モデルだけで選んだ単勝 ROI は控除率（約17.5%）ぶんのマイナスに収まり、市場を超える優位は出なかった。負けの中身として、HK$10 単位の丸めとリベート閾値が小資金の成績を大きく左右することを数値で示している。

## データ

- HKJC の結果ページ（全券種の確定配当、上がり区間タイム、SP=確定単勝オッズ、通過順）、出馬表、馬の経歴（産地、出走時の馬齢、毛色、性、輸入区分、父・母・母父、馬主、レーティング）、騎手・調教師の季節成績、香港天文台の日別気温、バリアトライアル、調教（trackwork）、200m ごとのセクショナル、レース後コメント（comments-on-running）、祝日（README「Data layer (M1)」、PLAN.md）。
- 1,697開催、2006〜2026年。特徴量ストアは約19.7万行（1頭1レース）。
- 取得は冪等で、取得済み URL を `_scrape_manifest` に記録する。獣医リストと馬具変更の申告は過去分が取れないため対象から外した（PLAN.md）。

## 特徴量

- すべての特徴量を `event_time ≤ race_off_time` で計算できる「as-of feature store」として作る。
- **leakage canary**: 未来の情報やシャッフルしたラベルから作った番兵特徴量を常に入れ、重要度とバックテスト ROI がほぼ0であることを CI で確認する（PLAN.md §H）。
- SP（結果ページの単勝オッズ）は「市場の終値」で、勝とうとしている相手そのものなので、基本特徴量には入れない（PLAN.md §B）。
- NLP: 英語のレース後コメントを spaCy の規則・辞書（不利、伸びた、楽勝など）と MiniLM の埋め込みで数値化し、そのレースではなく**次走以降の特徴量**として遅らせて使う。

## モデルと目的変数

- 基準は Plackett–Luce 型の条件付きロジット（レース内 softmax で単勝確率）と Harville 式による複勝確率。
- M3 で LightGBM / XGBoost / CatBoost、LambdaMART、MLP、FT-Transformer、アンサンブルを同じ `ProbabilityModel` インターフェースで比較。較正は温度スケーリング・isotonic・Platt。市場ブレンド（重みを調整）も用意。

## 評価

- ウォークフォワード（季ごとに再学習が既定）。指標は log loss、top-1 的中率、ECE、ROI 2種。
- **ROI を2つ出す**（PLAN.md §1A）: 保守的な「model-only」（モデル確率だけで選ぶ。確定オッズは決定に使わない）と、楽観的な「market-blended」（SP を締切時の価格の代わりにして正の EV を買う）。真の値はその間にあると位置づける。払戻は保存した確定配当。
- 複勝の頭数別払戻（7頭以上3着、5〜6頭2着、5頭未満なし）、同着の配当分割、取消・返還を性質ベースのテストで検証。
- 賭け金の掃引（M5）: 均等、定率、フル Kelly と分数 Kelly（0.05〜0.5）、レース内の同時 Kelly、1レース10%・1日25%の上限、HK$10 単位の丸め、資金 HK$1k/10k/50k/100k。ブートストラップ信頼区間付き。

## 結果

- 「Features + backtest (M2)」: 基準の条件付きロジットのモデルのみ単勝 ROI は控除率（約17.5%）程度のマイナスで、市場を超える優位はない。
- 「Model zoo (M3)」: 全モデルが控除率ぶん負ける。レース内でまとめて尤度をとるモデル（ロジット、NN）は、1頭ずつ学習する GBM よりはるかに較正が良い。
- 「NLP track (M4)」: 小規模の試験ではコメント特徴量の限界効果はほぼ0（遅らせた特徴量の被覆が少ないため）。
- 「Risk / staking sweeps (M5)」: どの賭け方も優位を作らない。最良は分数 Kelly（λ≈0.05〜0.10）で約 −15%、均等・定率は −22〜−30%。信頼区間は広く重なる。HK$1,000 では均等・定率で合法な分散投資が1件も置けず、Kelly は意図した賭け金の約98%が丸めで消える（HK$100k で約23%）。HK$10k のリベート閾値を超える日は HK$1k〜10k で0日、HK$100k で16〜17日。

## 落とし穴と教訓

- 確定単勝オッズを特徴量に入れると循環になるので、壁を作る。過去の配当で計算した「市場ブレンド ROI」は、ライブの暫定オッズが貯まるまでは楽観的な上限にすぎない。
- 1単位 = 資金の1%という小資金では、小さな優位の Kelly 賭け金が0か1単位に丸められる。丸めの損失は脚注ではなく主要な結果として扱うべきだと PLAN.md に書いている。
- ライブ運用（M7）では HKJC の GraphQL から締切前のオッズを30秒間隔で記録し、推奨だけを出す（投票はしない）。過去のライブオッズ履歴は存在しないので、記録を始めた日からしか検証できない。

## 批判的に読む

- 否定的な結果を主結果として出している点が最大の価値。逆に、正の結果がないので「何が効くか」は分からない。
- ROI の数値は README に丸めた形でしか出ていない（表、期間ごとの値、信頼区間の幅は本文にない）。
- 開発は Claude Code を使った計画駆動（CLAUDE.md、prompt.md がある）で、短期間に M0〜M7 まで作られている。実装の正しさは README からは確認できない。
- 似た構成の別リポジトリ moli0516/hkjc-quant-model も、モデル top-1 的中率≈0.25 対 市場1番人気≈0.31、どの規則も安定した正の ROI なし、と同じ結論を書いている。

## keiba-ai での使い方

- **leakage canary** をそのまま取り入れる。未来の着順から作った特徴量と、シャッフルしたラベルで学習したモデルを毎回の実験で回し、重要度と回収率がほぼ0であることを確認する。
- 回収率は「モデルのみ」と「確定オッズを使った上限」の2本を必ず並べる。JRA でも時系列オッズを記録し始めるまでは、後者を上限として扱う。
- JRA の100円単位、少額資金での丸めの影響を、資金規模を変えて試算する。複勝・ワイドの払戻ルール（頭数による複勝の着数、同着）をテストで固める。
- GBM の1頭単位学習は較正が悪くなりやすいので、条件付きロジットや lambdarank 後の softmax と並べ、ECE を主表に入れる。
- レース後コメント（JRA では「レース後の短評」やJRDB のコメント類）を次走以降の特徴量として遅らせて使う設計は、そのまま参考になる。

## 関連ノート

- [Benter 2019](./2019-benter-model.md): 条件付きロジットと市場の結合。本リポジトリの基準モデルの源流。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 複勝確率の計算。
- [Whitrow 2007](./2007-whitrow-simultaneous-bets-allocation.md)、[Smoczynski 2010](./2010-smoczynski-explicit-kelly-horse-races.md): レース内の同時 Kelly。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md): 推定誤差があるときに分数 Kelly が良いこと。
- [Guo 2017](./2017-guo-calibration-modern-nn.md): 温度スケーリング。
- [jerrydaphantom 2026](./2026-jerrydaphantom-hkjc-ml-research.md)、[justinsuo 2026](./2026-justinsuo-hkjc-edge-lab.md): 同じ HKJC の個人研究で、市場の強さという同じ結論。
- [Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 締切直前のオッズの動き。

## 検索語

香港競馬, HKJC, ウォークフォワード, リーク検出, カナリア特徴量, 条件付きロジット, ハーヴィル, 分数ケリー, 賭け金の丸め, リベート, 控除率, 否定的結果, Hong Kong Jockey Club, walk-forward backtest, leakage canary, as-of feature store, conditional logit, Plackett-Luce, Harville place, model zoo, FT-Transformer, LambdaMART, fractional Kelly, simultaneous Kelly, stake rounding, rebate, takeout, comments-on-running NLP, negative result

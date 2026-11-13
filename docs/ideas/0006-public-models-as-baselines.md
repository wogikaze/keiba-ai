---
title: 公開されている競馬予測モデルをベースラインに使う
date: 2026-11-13
status: idea
---

# 公開されている競馬予測モデルをベースラインに使う

> 一言で: Hugging Face・GitHub・Kaggle・PyPI で「学習済みの重み」か「自分のデータで学習し直せるパイプライン」を探した。JRA-VAN の JV-Data で学習した重みは一つも公開されていない。再学習できるコードは多いが、JV-Data を直接読み、ライセンスがあり、時系列分割を守るものは JvLink To Importer の ML スターターキットだけだった。ライセンスのない良いリポジトリは、コードを使わず方法だけを README から再実装する。

調査日は 2026-11-13。
星の数と最終 push は GitHub API の値。

## 結論

- **JRA の学習済み重みは、そのままでは使えない。** Hugging Face の model に競馬の重みはない（`nitron2106/keiba_ai` と `WoodCiaran97/horse-racing` は README だけの空リポジトリ）。重みは Space に数件ある（下の表）が、どれも netkeiba の特徴量で学習した pickle か PyTorch の重みで、JV-Data の列に対応させる方法がない。pickle は読み込むだけで任意のコードが動くので、開かない。
- **ライセンスのある JRA 向けのコードは少ない。** 下の日本の表の 24 件のうち、OSS ライセンスがあるのは 6 件（MIT 4、Apache-2.0 1、AGPL-3.0 1）。新しい JV-Data 系のリポジトリ（2026 年作成）は、ほとんどにライセンスがない。ライセンスがなければ、コードは複製できない。方法と報告値だけを使う。
- **市場と比べた数値は、JV-Data 系の 2 件にしかない。** polkka9710（45,285 レースで市場の race logloss 1.9584 に対しモデル 2.1341）と yumuras（成績 PDF、オッズありモデルは市場と区別できない）。どちらも「過去成績だけのモデルは市場に負ける」という[評価の原則](./index.md)の 1 と同じ結論。
- **使える評価基盤は香港の MIT リポジトリにある。** justinsuo（ΔlogLoss のブートストラップ CI、プラセボ検定）と stevw-repo（条件付きロジットから FT-Transformer までを同じウォークフォワードで比べる）。特徴量は枠・斤量・騎手・調教師・過去成績なので、JV-Data に置き換えやすい。
- **市場ベースラインは自分で作る。** オッズだけのモデルを公開しているリポジトリはない。オッズを確率に直す部品は PyPI にある（`goto-conversion` MIT、`shin`）。どちらも固定オッズ向けで、パリミュチュエルの JRA では単純な正規化と比べてから使う。

## 再現する候補（順位つき）

### 1. 市場だけのモデル（自作。部品に goto_conversion）

他のすべての比較の基準なので、最初に作る。
締切前の単勝オッズ（0B41 の時系列）から、控除を除いて正規化した確率を出す。
確定オッズ版も並べて作り、2 つの差を「購入時点で知り得ない情報の量」として記録する。
本命・大穴バイアスの補正（べき乗、Shin、goto_conversion）は、時系列分割で効くか確かめてから入れる。

### 2. JvLink To Importer ML スターターキット（raveuptonight、MIT）

JV-Data を前提に作られた、ライセンスのある唯一のパイプライン。
LightGBM の 3 着内分類と、レース単位の LGBMRanker を、日付で分けた時系列分割とウォークフォワードで比べ、AUC・LogLoss・Brier・Hit@k をモデルカードに書き出す。
データ契約で確定オッズを特徴量に入れないと決めており、同じ日のレースが学習と評価に分かれない。
特徴量を作るのは別の Importer 本体（配布はバイナリだけで、ソースは非公開）。
`race_features.parquet` を自前の JV-Data から同じ列の役割（feature / label / id / time / eligibility）で作れば、学習・評価のコード（`src/jli_ml/`）はそのまま使える。
回収率の計算はない。
単勝確率のモデルでもないので、市場との ΔlogLoss は自分で足す。

### 3. 市場オフセットつきの LightGBM（graphite278、polkka9710 の方法を再実装）

graphite278/keiba-record は、JRA-VAN（2015 年以降）で LightGBM のレース内 softmax（条件付きロジット / Plackett-Luce）を学習し、初期スコアに `log(市場確率)` を置いて市場からのずれだけを学習する。
polkka9710/keiba_ai も、Benter の 2 段階でモデルの係数 α を推定し、α が負（−0.0274、SE 0.0087）と報告した。
市場を出発点にした v26 では race logloss が市場を 0.0012 下回ったが、確定オッズから作った特徴量を使っている。
2 件ともライセンスがないので、コードは読まずに README の説明から書く。
[Benter](../literature/2019-benter-model.md) の 2 段階、[namespace 2026](../literature/2026-namespace-market-odds-residual.md) の残差学習と同じ考え方で、ΔlogLoss を直接測れる。
polkka9710 の数値（2013-04〜2026-05、45,285 レース）は、同じ期間で再現できるかの目安になる。

### 4. HKJC Edge Lab の評価基盤（justinsuo、MIT）

条件付きロジットと勾配ブースティングの基本モデルを、Benter 型の 2 段階で市場と結合する。
主指標は市場との log loss 差で、ブートストラップの 95% 区間を付ける。
市場確率そのものを入力にして全体を回すプラセボ検定もある（[ノート](../literature/2026-justinsuo-hkjc-edge-lab.md)）。
モデルより評価コードを移植する価値が高い。
確定オッズ（SP）で評価しているので、JRA では締切前オッズに差し替える。

### 5. HKJC ML Research Platform のモデル群（stevw-repo、MIT）

条件付きロジット、GBM 各種、LambdaMART、MLP、FT-Transformer、アンサンブルを同じウォークフォワードで比べる（[ノート](../literature/2026-stevw-hkjc-ml-research-platform.md)）。
カナリア特徴量でリークを確かめる仕組みと、「モデルだけの ROI」と「確定オッズを使った上限」を分ける書き方は、そのまま取り入れる。
入力は HKJC の結果ページなので、JV-Data（RA・SE・UM・HC・WC）からの特徴量の作り直しが要る。
候補 2〜3 で LightGBM の基準ができてから、モデルの種類を増やすときに使う。

### 次点

- **sol12378/keiba-masters-kit-2026（Apache-2.0）**: 「控除を除いた三連単の市場確率」と「単勝からの Harville 確率」の対数線形モデル（[ノート](../literature/2026-sol12378-masters-kit.md)）。組合せ馬券の市場ベースラインになるが、三連単の時系列オッズは JV-Data にないので、券種を馬連（0B42）にしたときだけ使える。
- **ChanSenba/KeibaAI（ライセンスなし）**: JV-Link から成績・血統・調教を取り込み、「1 番人気を買う」「オッズなし」「オッズあり」の 3 本を並べる。設計は近いが、出馬表とオッズを netkeiba から取る。方法だけ参考にする。
- **yumuras/keiba_prediction_code（ライセンスなし）**: JRA の成績 PDF から 4 年分（13,117 レース）を作り、月ごとの再学習で市場と比べた。3 着内のレース内 AUC はオッズなしで 0.7635、市場 0.8005。最終オッズを使っていると自分で書いている。比較の数値として引用する。

## 候補の一覧

「JV 対応」は JV-Data に置き換える手間（低・中・高）。
「市場比較」は、市場オッズのモデルと比べた数値があるか。

### 日本（JRA・地方）

| リポジトリ | ★ / 最終 push | ライセンス | 予測するもの | モデル | データ | JV 対応 | 重み | 市場比較 | リークの懸念 | 判定 | ノート |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [raveuptonight/JvLinkToImporter-ML-Starter](https://github.com/raveuptonight/JvLinkToImporter-ML-Starter) | 0 / 2026-08 | MIT | 3 着内、レース内順位 | LightGBM、LGBMRanker | JV-Data（Importer の Parquet） | 低（特徴量は自作） | 合成データのみ | なし（単純基準とだけ比較） | 少ない。確定オッズを除外、日付で分割 | **使う（手間あり）** | なし |
| [graphite278/keiba-record](https://github.com/graphite278/keiba-record) | 0 / 2026-11 | なし | 単勝確率 | LightGBM レース内 softmax、init_score = log 市場確率 | JV-Data 2015〜 | 低 | なし（予想 CSV のみ） | あり（確定オッズ基準では上回る、事前オッズでは回収率 90〜100% と推定） | 確定オッズ基準の評価 | 方法だけ再実装 | なし |
| [polkka9710/keiba_ai](https://github.com/polkka9710/keiba_ai) | 0 / 2026-09 | なし | 単勝確率、着順別の補正 | LightGBM、Benter 結合 | JV-Data（自作の JV-Link ETL → PostgreSQL） | 低 | なし | あり（race logloss 2.1341 対 市場 1.9584、α < 0） | 市場オフセット版の特徴量は確定オッズ由来 | 方法と数値を使う | なし |
| [ChanSenba/KeibaAI](https://github.com/ChanSenba/KeibaAI) | 0 / 2026-11 | なし | 単勝確率、EV、ケリー | LightGBM、PyTorch NN | JV-Data ＋ netkeiba | 中 | なし | 1 番人気と比較 | オッズありモデルは確定オッズの可能性 | 方法だけ | なし |
| [keiba-dragon/horse_racing_ai](https://github.com/keiba-dragon/horse_racing_ai) | 0 / 2026-11 | なし | 単勝、印 | LightGBM ＋ LambdaMART | JRA-VAN マスター CSV | 中 | なし（gitignore） | 不明 | 不明 | 使わない | なし |
| [raveuptonight/keiba-yosou-public](https://github.com/raveuptonight/keiba-yosou-public) | 0 / 2026-02 | なし | 単勝・複勝確率、EV | XGBoost ＋ LightGBM ＋ CatBoost | JV-Data（mykeibadb → PostgreSQL） | 低 | なし | 不明 | 不明 | 使わない | なし |
| [miyamamoto/jvlink-mcp-server](https://github.com/miyamamoto/jvlink-mcp-server) | 18 / 2026-08 | 独自（商用は要相談） | 予測なし（集計の MCP） | なし | JVLinkToSQLite | — | — | — | — | 対象外 | なし |
| [kosei-matsuzaki/keiba-ai](https://github.com/kosei-matsuzaki/keiba-ai) | 0 / 2026-09 | 閲覧・評価のみ | 全券種の確率、回収率 | Set Transformer ＋ GRU、log-growth 損失 | netkeiba | 高 | 非公開 | あり（単勝 NLL で LightGBM が市場と並ぶ、と記載） | 確定オッズで評価 | 使わない（ライセンス） | なし |
| [yumuras/keiba_prediction_code](https://github.com/yumuras/keiba_prediction_code) | 0 / 2026-11 | なし | 3 着内 | ロジスティック、LightGBM | JRA 成績 PDF 2023〜2026 | 中 | なし | あり（区別できない） | 最終オッズ（本人が明記） | 数値だけ引用 | なし |
| [ten-ten66/keiba-predictor](https://github.com/ten-ten66/keiba-predictor) | 0 / 2026-11 | なし | 勝率、EV | LightGBM/XGBoost/CatBoost のスタッキング | netkeiba | 高 | 非公開 | 不明 | 不明 | 使わない | なし |
| [watanabekazunori/keiba-prediction-app](https://github.com/watanabekazunori/keiba-prediction-app) | 0 / 2026-06 | なし | 勝率、3 着内率 | LightGBM ＋ CatBoost ＋ LambdaRank | netkeiba（JRA・NAR） | 高 | あり（pkl、使えない） | なし（オッズ不使用） | 不明 | 使わない | なし |
| [katsuo-1223/keiba_model](https://github.com/katsuo-1223/keiba_model) | 0 / 2025-12 | なし | 勝率、EV | LightGBM 2 段スタッキング、isotonic | Kaggle JRA（netkeiba 由来） | 高 | なし | 不明 | 2 段目にオッズ（確定の可能性） | 使わない | なし |
| [bunyu422/keiba-ai](https://github.com/bunyu422/keiba-ai) | 0 / 2026-06 | なし | ワイド | ListNet NN、Benter α-β 較正 | netkeiba | 高 | なし | 回収率のみ | — | 方法だけ | [2026-bunyu422-listnet-wide](../literature/2026-bunyu422-listnet-wide.md) |
| [tsukasaI/keiba-ai](https://github.com/tsukasaI/keiba-ai) | 0 / 2026-09 | なし | 着順分布 → 馬単 EV | LightGBM/CatBoost/XGBoost | Kaggle JRA 2019〜2021 ＋ netkeiba | 高 | なし | なし | 組合せオッズが不完全 | 使わない | [2025-tsukasai-exacta-ev](../literature/2025-tsukasai-exacta-ev.md) |
| [atsuo-514/keiba-ai](https://github.com/atsuo-514/keiba-ai) | 0 / 2026-06 | MIT | 重賞の複勝 | LightGBM ＋ SHAP | netkeiba 重賞 2016〜2025 | 中 | なし | 1 番人気と比較（ほぼ同じ） | 市場特徴は確定オッズ | 参考（重賞限定） | [2026-atsuo514-g1-place-shap](../literature/2026-atsuo514-g1-place-shap.md) |
| [sol12378/keiba-masters-kit-2026](https://github.com/sol12378/keiba-masters-kit-2026) | 3 / 2026-10 | Apache-2.0 | 組合せ確率、大会の賭け方 | 市場確率 ＋ Harville の対数線形 | netkeiba（合成データで動作） | 中 | なし | 市場が基準そのもの | 少ない（odds_factor で補正） | 次点 | [2026-sol12378-masters-kit](../literature/2026-sol12378-masters-kit.md) |
| [SHOGO391/KEIBA-AI-README](https://github.com/SHOGO391/KEIBA-AI-README) | 0 / 2026-10 | MIT | 勝率、3 着内率 | 距離別 LightGBM | TARGET / JRA-VAN | — | なし（README だけ） | なし | 一部が確定オッズ（本人が注記） | 対象外（コードなし） | [2026-shogo391-kaiba-ev-autobet](../literature/2026-shogo391-kaiba-ev-autobet.md) |
| [KHTTakuya/KeibaPrediction](https://github.com/KHTTakuya/KeibaPrediction) | 14 / 2023-05 | MIT | 3 着内 | LightGBM ＋ TensorFlow | JRA-VAN（TARGET の CSV） | 中 | なし | なし | **ランダム分割**（`train_test_split(shuffle=True)`） | 使わない | [2021-khttakuya-lightgbm-tensorflow](../literature/2021-khttakuya-lightgbm-tensorflow.md) |
| [cocon-ai-group/turf-tipster](https://github.com/cocon-ai-group/turf-tipster)（と turf-tipster2） | 45・12 / 2018 | AGPL-3.0 | 順位 | Chainer のペアワイズ NN、LambdaRank | netkeiba | 高 | なし | なし | 名前の埋め込み（暗記） | 使わない（古い） | [2018-cocon-turf-tipster](../literature/2018-cocon-turf-tipster.md) |
| [stockedge/netkeiba-scraper](https://github.com/stockedge/netkeiba-scraper) | 118 / 2021-12 | なし | 素性作成 | （ランダムフォレスト） | netkeiba | 高 | なし | なし | — | 使わない | [2016-stockedge-keiba-random-forest](../literature/2016-stockedge-keiba-random-forest.md) |
| [surpass19/U-HorseRacingAI](https://github.com/surpass19/U-HorseRacingAI) | 10 / 2021-09 | なし | 順位、買い目 | LightGBM ＋ Optuna | netkeiba | 高 | なし | なし | 不明 | 使わない | なし |
| [sf-12/uma-ai-jrdb](https://github.com/sf-12/uma-ai-jrdb) | 4 / 2024-02 | なし | 3 着内 | LightGBM（ノートブック） | JRDB | 中 | なし | なし | **ランダム分割**（ノートより） | 使わない | [2023-sf-12-keiba-ai](../literature/2023-sf-12-keiba-ai.md) |
| [nagatakodai/keiba-ev](https://github.com/nagatakodai/keiba-ev) | 0 / 2026-10 | なし | 全券種の確率、EV | LightGBM lambdarank ＋ 温度較正 ＋ 市場ブレンド（β=0.78） | netkeiba・公式サイト（JRA・NAR・ばんえい） | 高 | なし | 人気買いと常時比較 | 分割の誤りを本人が修正済み | 方法だけ | なし |
| [TatsuyaM2667/keiba-predictor](https://github.com/TatsuyaM2667/keiba-predictor) | 1 / 2026-11 | なし | 勝率（確率になっていない） | 手作りの指数 ＋ Thurstone | netkeiba | — | — | — | — | 使わない | [2026-tatsuyam07-win-prob-anatomy](../literature/2026-tatsuyam07-win-prob-anatomy.md) |

### 海外

| リポジトリ | ★ / 最終 push | ライセンス | 予測するもの | モデル | データ | JV 対応 | 重み | 市場比較 | リークの懸念 | 判定 | ノート |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [justinsuo/hkjc-edge-lab](https://github.com/justinsuo/hkjc-edge-lab) | 0 / 2026-06 | MIT | 単勝確率、市場との結合 | 条件付きロジット ＋ GBM、Benter 2 段階 | HKJC 2025/26 | 中 | なし | あり（ΔlogLoss +0.0045、CI が 0 をまたぐ） | 確定オッズ（SP）で評価 | **使う（評価基盤）** | [2026-justinsuo-hkjc-edge-lab](../literature/2026-justinsuo-hkjc-edge-lab.md) |
| [stevw-repo/HKJC-Horse-Racing-ML-Research-Project](https://github.com/stevw-repo/HKJC-Horse-Racing-ML-Research-Project) | 6 / 2026-06 | MIT | 単勝、組合せ | 条件付きロジット、GBM、LambdaMART、MLP、FT-Transformer | HKJC 2006〜2026 | 中 | なし | あり（モデルだけでは控除率ぶん負ける） | 確定オッズの壁、カナリア特徴量 | **使う（モデル群）** | [2026-stevw-hkjc-ml-research-platform](../literature/2026-stevw-hkjc-ml-research-platform.md) |
| [jerrydaphantom/hkjc-ml-research](https://github.com/jerrydaphantom/hkjc-ml-research) | 6 / 2026-05 | MIT | 単勝 | ロジスティック、LightGBM、CatBoost | HKJC 2020〜2026 | 中 | なし | あり（確定オッズを特徴量にすると改善） | **確定オッズを特徴量に使用** | 参考 | [2026-jerrydaphantom-hkjc-ml-research](../literature/2026-jerrydaphantom-hkjc-ml-research.md) |
| [catowabisabi/horse-racing-model-training](https://github.com/catowabisabi/horse-racing-model-training) | 2 / 2026-06 | MIT | 馬連 | LightGBM ＋ XGBoost、ケリー | HKJC 2008〜2018（eprochasson） | 中 | なし | オッズあり・なしを比較 | 確定オッズ | 参考 | [2026-catowabisabi-hkjc-quinella-lightgbm](../literature/2026-catowabisabi-hkjc-quinella-lightgbm.md) |
| [anton-schwarberg/Hongkong-Horse-Racing-Prediction](https://github.com/anton-schwarberg/Hongkong-Horse-Racing-Prediction) | 4 / 2026-05 | なし | 3 着内 | LR、LightGBM 分類・ランカー、XGBoost ランカー | HKJC 2009〜2025 | 中 | なし | なし | — | 使わない | [2025-schwarberg-hkjc-prediction-pipeline](../literature/2025-schwarberg-hkjc-prediction-pipeline.md) |
| [codeworks-data/mvp-horse-racing-prediction](https://github.com/codeworks-data/mvp-horse-racing-prediction) | 66 / 2023-11 | MIT | 単勝・複勝 | LightGBM、1 層 NN | Kaggle HK 1997〜2005（gdaley） | 中 | なし | 素朴な賭け方と比較 | 月ごとの再学習（時系列） | 参考（古い） | [2021-ndiaye-codeworks-hkjc-lgbm](../literature/2021-ndiaye-codeworks-hkjc-lgbm.md) |
| [Christy-Lo/Horse-Racing-Prediction---Optimized-Gambling-Strategy](https://github.com/Christy-Lo/Horse-Racing-Prediction---Optimized-Gambling-Strategy) | 42 / 2022-02 | なし | 単勝 | ランダムフォレスト | Kaggle HK | 中 | なし | なし | 不明 | 使わない | [2021-christylo-hkjc-random-forest-betting](../literature/2021-christylo-hkjc-random-forest-betting.md) |
| [acmayuen/HK-Horse-Racing](https://github.com/acmayuen/HK-Horse-Racing) | 49 / 2017-08 | なし | 単勝 | 2 段階の条件付きロジット（R） | HKJC | 中 | なし | 1 番人気と比較 | 確定オッズ | 方法だけ | なし |
| [chris-alex-p/german-horse-racing](https://github.com/chris-alex-p/german-horse-racing) | 6 / 2026-01 | なし | 単勝 | 条件付きロジット（R `clogit`） | ドイツ 2002〜 | 中 | なし | オッズを特徴量に入れた 1 段階 | 確定トートオッズ | 方法だけ | [2023-chrisalexp-german-benter](../literature/2023-chrisalexp-german-benter.md) |
| [dominicplouffe/HorseRacingPrediction](https://github.com/dominicplouffe/HorseRacingPrediction) | 180 / 2018-11 | MIT | タイム回帰 | SVR | 北米 | 高 | なし | なし | — | 使わない（古い） | [2017-plouffe-svr-horse-racing](../literature/2017-plouffe-svr-horse-racing.md) |
| [ethan-eplee/HorseRacePrediction](https://github.com/ethan-eplee/HorseRacePrediction) | 41 / 2022-10 | なし | 単勝 | 各種分類器 | Kaggle HK 2014〜2017 | 中 | なし | バックテストのみ | 不明 | 使わない | なし |
| [pranay123-stack/horse-quant-platform](https://github.com/pranay123-stack/horse-quant-platform) | 0 / 2026-09 | 閲覧・評価のみ | 単勝確率、EV | 較正つき GBM | 英愛（数値は合成データ） | 中 | なし | 合成データのみ | — | 使わない（ライセンス） | [2026-pranay123-horse-quant-platform](../literature/2026-pranay123-horse-quant-platform.md) |
| [tonydebney69-debug/horse-racing-model](https://github.com/tonydebney69-debug/horse-racing-model) | 0 / 2026-09 | なし | 市場の効率性の検証 | 統計検定 | Betfair 豪州・NZ | — | なし | 市場そのもの | — | 対象外 | [2026-tonydebney-au-nz-racing-markets](../literature/2026-tonydebney-au-nz-racing-markets.md) |
| [SolvAI/turfolio](https://github.com/SolvAI/turfolio) | 1 / 2026-11 | MIT | PMU の馬券ポートフォリオ | — | フランス PMU | 高 | なし | — | — | 対象外 | [2026-solvai-turfolio-pmu](../literature/2026-solvai-turfolio-pmu.md) |
| [gotoConversion/goto_conversion](https://github.com/gotoConversion/goto_conversion) | 117 / 2026-09 | MIT | オッズ → 確率 | 本命・大穴バイアスの補正つき変換 | — | 低 | — | — | — | **市場ベースラインの部品** | なし |

### Hugging Face の Space（重みあり）

| Space | ライセンス | 中身 | 判定 |
|---|---|---|---|
| [Cosmic13/keiba](https://huggingface.co/spaces/Cosmic13/keiba) | Apache-2.0 | 走破速度を予測する LSTM ＋ Transformer の `.pth` / `.h5` と、語彙の pickle（2025・2026 年版）。入力は netkeiba（keibascraper） | 使わない。騎手・調教師の埋め込みが netkeiba の ID に結びついている |
| [kojimayu/keiba-ai](https://huggingface.co/spaces/kojimayu/keiba-ai) | なし | LightGBM LambdaRank のテキスト形式モデル（中山・阪神別）。netkeiba | 使わない |
| [KaleidoFuture/kf-keiba-demo](https://huggingface.co/spaces/KaleidoFuture/kf-keiba-demo) | MIT | LightGBM ＋ SHAP の pickle。JRA 公式サイトと Kaggle JRA データ | 使わない（pickle、特徴量が別） |
| [keibauma/keiba-predict](https://huggingface.co/spaces/keibauma/keiba-predict) | なし | JRA 平地の「オッズなし」LightGBM（pickle）と予測の parquet | 使わない |

ほかの `keiba` Space（mamo-chan、masah14、oharu121 など 10 件ほど）は、アプリだけで重みがない。
Hugging Face の dataset は、`KBlueLeaf/jp-racing-horse`（Apache-2.0、1990〜2025 年の SQLite。出所は未確認）とフランス PMU のものだけだった。

### Kaggle と PyPI

- Kaggle の JRA データは [takamotoki/jra-horse-racing-dataset](https://www.kaggle.com/datasets/takamotoki/jra-horse-racing-dataset)（netkeiba から集めた 1986-01〜2021-07 の結果・オッズ・ラップ・通過順）だけ。上のノートブックは EDA がほとんど。モデルは tsukasaI と katsuo-1223 が GitHub で使っている。オッズは確定オッズで、複勝オッズは上位数頭しかない。
- 香港は [gdaley/hkracing](https://www.kaggle.com/datasets/gdaley/hkracing)（1997〜2005、6,349 レース）が定番で、codeworks と Eric Zhao（[ノート](../literature/2020-ericzhao-hk-abetting-model.md)）が使っている。
- PyPI に競馬の予測パッケージはない。あるのは netkeiba のスクレイパー `keibascraper` と、オッズを確率に直す `goto-conversion`・`shin` だけ。

## 見つからなかったもの

- JV-Data で学習した重み（Hugging Face、GitHub Releases、Kaggle Models のどこにもない）。JRA-VAN の利用規約（第 7 条）で、データから作ったものを公開しにくいことが理由と考えられる。
- 締切前の時系列オッズで評価した公開パイプライン。市場と比べたものは、どれも確定オッズを市場確率に使っている（graphite278 だけが事前オッズでの回収率を見積もっている）。
- 「オッズだけのモデル」を独立したベースラインとして公開しているリポジトリ。
- JRA の LambdaRank・NN で、ライセンスがあり、時系列分割を守るもの。

## 最初の検証

1. 市場だけのモデルを作る。確定オッズ版と締切前オッズ版の logloss を、同じ期間で並べる。
2. ML スターターキットの `jli_ml` を依存として入れ、JV-Data から同じデータ契約の Parquet を作る。3 着内の LightGBM と LGBMRanker を、市場だけのモデルと同じ分割で評価する。
3. 単勝の条件付きロジット（LightGBM のレース内 softmax）を、初期スコアなしと `log(市場確率)` ありの 2 通りで学習し、ΔlogLoss とブートストラップ区間を出す。polkka9710 の 1.9584 / 2.1341 に近い値になるか確かめる。
4. justinsuo のプラセボ検定（市場確率から着順をサンプルして全体を回す）を評価コードに入れ、回収率が −控除率、ΔlogLoss が 0 になることを確かめる。

方法・分割・主指標を決めるときは ADR を書く。
MIT のコードを取り込むときは、著作権表示とライセンス文をファイルに残す。

## リスク

- ライセンスのないリポジトリのコードを、うっかり写す。再実装するときは README の説明と論文だけを見て書く。
- 公開リポジトリの多くは Claude Code などで短期間に作られている。README の数値と実装が合っているかは確かめていない。数値は「本人の報告」として扱う。
- ML スターターキットは Importer の版（データ契約の schemaVersion）に合わせて変わる。依存するときは版を固定する。

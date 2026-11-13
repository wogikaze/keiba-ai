---
title: オルタナティブ競馬データを使った競馬予想の新しい取り組み+有馬記念の予想
authors: yanashi_im（簗島亮次）
year: 2024
venue: Qiita（Intimate Merger Advent Calendar 2024）
url: https://qiita.com/yanashi_im/items/396ca578e07aaa59dbea
topic: practitioner
tags: grey-literature, ai-masters, odds-movement, noise-trader, favorite-longshot-bias, insider-information, expected-odds, alternative-data
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# オッズ推移と「想定オッズとの乖離」で過小評価馬を探す — 大会2年目の生成系競馬予想が学術文献から組み立てた2つの指標

> 一言で: AI競馬予想マスターズ2024 に「ヤナシ社長の生成系競馬予想2.0」で参加中の著者が、1年間の取り組みをまとめた記事（2024年12月、最終ステージ中）。馬柱だけの従来型データでは回収率75〜80%を超えにくいとし、生成AIの助けを借りて読んだスポーツベッティングの論文（本命・穴馬バイアス、ノイズトレーダー、情報の非対称性）から、(1) 定期的に馬券を買う高回収率の予想家の評価と最終オッズとの差が大きい馬（ノイズトレーダーの影響を除く）、(2) 従来型データから作った想定オッズと発売直後のオッズの乖離が大きい馬（従来データにない情報で買われている）、の2つの指標を作った。最終日の朝9時のオッズで、想定人気に比べて売れている馬の一覧（想定比 1374%〜201%）も載せている。

大会のルールと成績は [2024年大会](./2024-netkeiba-ai-masters-2024.md) にまとめた。生成系競馬予想2.0 の2024年の公式成績はステージ1 32位（回収率78.92%）、ステージ2 15位（91.63%）、最終ステージ9位（94.63%）。プロフィールでは開発歴20年程度、環境は GCP、「機械学習ではない、生成系のアプローチ」としている。前年の記事は [yanashi 2023](./2023-yanashi-generative-keiba.md)。

## 主張（「学術的に回収率を上げるために必要な要素」の節）

論文調査の結果として次の4点を挙げる。参考文献は Snowberg & Wolfers、芦谷、Chiappori ら、Whelan、Gandhi、Jullien & Salanié、Ottaviani & Sørensen。

- 本命・穴馬バイアス（favorite-longshot bias）: 本命は過小評価、穴馬は過大評価され、人気薄の回収率が低い。リスク選好や確率の誤認、信念の異なるトレーダー（正確な信念の多数派とノイズトレーダー）で説明される。
- オッズの歪み: 売上や出走頭数が少ないレースでは券種間の価格の歪みが大きく、必ず利益が出る組（裁定）が作れることがある。
- 情報の非対称性（インサイダー）。
- ホットハンド・コールドハンドの誤信。

（同じ箇条の中で「低オッズの馬券は過剰に購入され、高オッズの馬券は過少に購入される」とも書いており、前後の説明と向きが逆になっている。標準的な説明は前者で、後者は誤記と思われる。）

## 2つの指標（「具体的にやってみたこと」の節）

1. **オッズ推移によるノイズトレーダーの除去**: 大レースの日は普段馬券を買わない人が新聞・テレビ・ネットの予想で買う。定期的に買っていて回収率がある程度高い予想家の評価と、最終オッズの差が大きい馬は、相対的に回収率が高くなる傾向がある、とする。
2. **発売直後のオッズと想定オッズの差**: 新聞の馬柱や印から想定オッズを作り、発売開始直後のオッズとの乖離が大きい馬を探す。パドックや馬体重の情報がまだない時点での乖離は、従来型データにない情報を持った人の投票による可能性が高く、その馬を買うと相対的に回収率が高い、とする。

区分ごとの単純な回収率の表や「先週の実際の回収率」、個人用ダッシュボードは画像で、本文テキストには数値がない（件数の少ないセルがあるとの注記はある）。

## 結果

記事中の数値は、最終日（12/22）9時時点の想定人気と9時オッズの比（想定比）だけ。例えば京都11R りんくうS の想定10番人気の馬が1374%、中山11R 有馬記念の想定14番人気の馬が530%。回収率の検証結果は本文テキストにない。

## 批判的に読む

- 2つの指標の回収率の根拠（期間・件数・控除率込みか）がテキストで示されていない。画像の表も件数の少ないセルを含むと著者が断っている。
- 「発売直後のオッズ」は発売開始直後で票数が少なく、ノイズが大きい。乖離が大きい馬の多くは単なる少額投票の偶然である可能性がある。
- 想定オッズを作る従来型データ（新聞の印）の取得時刻と、オッズの取得時刻の前後関係を厳密に管理しないとリークになる。

## keiba-ai での使い方

- 「想定オッズ（ファンダメンタルから作った市場予測）と実際のオッズの乖離」は、[Benter 2019](./2019-benter-model.md) のモデル確率と大衆確率の結合や、オッズ依存の予測（[Kobayashi 2023](./2023-kobayashi-odds-dependent-prediction.md)）と同じ問題設定である。keiba-ai では時系列のオッズ（発売直後・前日・直前）を取得できるなら、この乖離を特徴量の候補にできる。
- 本命・穴馬バイアスの文献は既存ノート（[Snowberg 2010](./2010-snowberg-flb-risk-love-misperceptions.md)、[Ottaviani 2010](./2010-ottaviani-noise-information-flb.md)、[Gandhi 2015](./2015-gandhi-belief-heterogeneity-longshot.md)、[Jullien 2000](./2000-jullien-estimating-preferences-racetrack.md)、[Ashiya 2010](./2010-ashiya-longshot-bias-survey.md)）とそのまま対応する。実践者がこれらをどう指標に落としたかの例として読む。

## 関連ノート

- [2024年大会](./2024-netkeiba-ai-masters-2024.md)、[2023年大会](./2023-netkeiba-ai-masters-2023.md)
- [yanashi 2023](./2023-yanashi-generative-keiba.md)（前年の記事）
- [Snowberg 2010](./2010-snowberg-flb-risk-love-misperceptions.md)、[Ottaviani 2010](./2010-ottaviani-noise-information-flb.md)、[Gandhi 2015](./2015-gandhi-belief-heterogeneity-longshot.md)、[Jullien 2000](./2000-jullien-estimating-preferences-racetrack.md)、[Ashiya 2010](./2010-ashiya-longshot-bias-survey.md)
- [Shin 1993](./1993-shin-measuring-insider-trading.md)（インサイダーの存在とオッズ）
- [Benter 2019](./2019-benter-model.md)、[Kobayashi 2023](./2023-kobayashi-odds-dependent-prediction.md)

## 検索語

オルタナティブデータ, オッズ推移, 想定オッズ, 発売直後オッズ, ノイズトレーダー, 本命・穴馬バイアス, 情報の非対称性, インサイダー, 生成系競馬予想, AI競馬予想マスターズ2024, alternative data, odds movement, favourite-longshot bias, noise traders, morning line

---
title: Man v Machine: Greyhound Racing Predictions
authors: Lyons Alva
year: 2016
venue: MSc Research Project (Data Analytics), National College of Ireland
url: https://norma.ncirl.ie/2527/1/alvalyons.pdf
doi:
topic: machine-learning
tags: greyhound, feature-selection, deep-learning, random-forest, expert-comparison, grey-literature
verified: fulltext
importance: low
source: downloaded
source_version: published
---

# グレイハウンドで「機械による特徴量選択」は専門家の予想に勝てるか（修士研究）

> 一言で: アイルランド Shelbourne Park の約1.1万レースで、特徴量を人手でなくアルゴリズム（Boruta、RF の重要度、RFE）で選び、H2O の深層 NN と RF に着順6クラスを分類させた。正解率は18〜19%で、場の専門家の1着的中率23.7%に届かなかった。ただし両者は別の指標で、この比較はそもそも成り立っていない。

## 問いと位置づけ

研究課題は「機械学習だけで、Shelbourne Park の専属予想家より高い的中率を出せるか」（p.3）。グレイハウンドの先行研究 [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md)、[Johansson 2003](./2003-johansson-greyhound-neural-networks.md)、[Schumaker 2008](./2008-schumaker-svr-longshot-greyhound.md) は、どれも専門家に聞いた約10変数を入力にしていた。本研究はこの「人手の特徴量選択」を、アルゴリズムによる選択に置き換えることを狙う（p.4–5）。

グレイハウンドを選んだ理由も述べている。競馬では、騎手が着外を悟ると、次走のハンデを守るために追うのをやめることがある。犬は勝負が決まった後も機械仕掛けのウサギを追い続ける。だから着順に雑音が少ない、という主張である（p.4–5）。

## データ

| 項目 | 内容 | 出典 |
|---|---|---|
| 取得元 | Irish Greyhound Board (IGB) の Web 結果ページを Python でスクレイピング | p.6 |
| 全体 | 2007年4月〜2016年9月、アイルランド全場、28,271レース・383,746行 | p.6 |
| 分析対象 | Shelbourne Park の A グレード（中距離）戦のみ、2009年1月〜2016年8月、10,986レース・64,908行 | p.3, p.9 |
| 頭数 | 1レース6頭 | p.4 |
| 除外 | タイムトライアル（非競走）、短距離戦 | p.8–9 |
| 比較対象 | IGB 雇用の専属予想家の予想（1着、2着以内2頭、3着以内3頭） | p.3, p.19 |

前処理には、keiba-ai でも同じ問題が起きそうな記述がいくつかある。

- **欠損の大半はタイムトライアル由来。** 体重・頭数・勝ちタイム・馬場の欠損は 100% がタイムトライアルの行だった（p.8, Table 1）。非競走の行を落とすだけで欠損の多くが消える。
- **外れ値。** 体重 0 lb や 677 lb といった値があり、前後2走の平均で埋めた（p.8）。
- **スクレイピング時点のビューによるリーク。** 馬主・調教師は「取得した時点の」所属しか分からない。過去レース時点の所属と一致する保証がないので、使わなかった。兄弟の成績（litter distribution）も取得時点の累計なので除外した（p.9）。
- **コメントの数値化。** 走りの短評（FAw = 好スタート、BBkd = ひどく不利 など）を5段階の辞書で −2〜+2 に点数化し、合計を「remark score」とした。辞書は著者が作り、業界の専門家2人が確認した（p.9–10）。着順に出ない不利を拾う狙い。
- **集計窓。** 出走表に合わせて直近5走の平均を取った（Chen らは7走）。5走未満なら、ある分だけで平均する（p.11）。

## 特徴量選択

約30個の候補変数に、次の手法をかけた（p.14–18）。

1. Boruta（RF による wrapper）: 30変数から1つしか落ちなかった（p.14）。
2. caret + randomForest による重要度順位（p.15）
3. RFE + Naive Bayes: 3変数まで絞った。しかし特徴量どうしの相関が強く、NB の独立性の仮定が崩れているため採用しなかった（p.16–17）。
4. RFE + Random Forest（p.17）
5. RFE + Tree Bagging（p.17）

2・4・5の上位10に共通して入ったのは DogsAge、OverallAvgTime、SecTimeAvg5、TimeAvg5、RankedGradeAvg5 の5つ。これに上位の5つを足した10変数を最終入力とした（p.18, Table 2）。

| 最終10変数 | 意味 |
|---|---|
| DogsAge | 年齢 |
| OverallAvgTime | 通算平均タイム |
| SecTimeAvg5 | 直近5走のセクショナルタイム平均 |
| TimeAvg5 | 直近5走の走破タイム平均 |
| RankedGradeAvg5 | 直近5走のグレード平均 |
| Weight | 体重 |
| RaceNumber | 当日のレース番号 |
| PrizeMoneyWonAvg5 | 直近5走の獲得賞金平均 |
| BreakAvg5 | 直近5走の第1コーナー通過順平均 |
| Avg2ndBend5 | 直近5走の第2コーナー通過順平均 |

コメント由来の remark score も、トラップ番号（枠）も、最終セットには残らなかった（Table 2 を見る限り）。

## モデルと結果

- 目的変数は着順（1〜6位の6クラス分類）。勝ち負けの2値にしなかった理由は、クラス不均衡と「2着と予測して実際は1着」の方が「6着と予測して1着」より誤りが小さい、という考えから（p.12）。ただし普通の多クラス分類は順序を使わないので、この狙いはモデルに反映されていない。
- データは学習・検証・テストに 60/20/20 で分けた（p.19）。時系列順か無作為かは書かれていない。
- H2O の深層 NN: 複数の部分集合での平均正解率 18.92%（p.19）。
- H2O の RF: 検証 19%、テスト 18.28%（p.19–20）。
- 専門家の1着的中率: 23.7%（2009年1月〜2016年9月、p.19）。

著者の結論は、深層学習は小さなデータに向かず、モデル選択の失敗のため問いには答えが出なかった、というもの（p.20–21）。今後の課題として、レース内の確率の合計が1になる条件付きモデルを挙げている（p.21）。これは条件付きロジット（[Bolton 1986](./1986-bolton-conditional-logit.md)）を使えという話と同じである。

> Modelling is done on each individual greyhound separately in order to ascertain their individual probability of winning a race given their historical performance data. (p.21)

## 批判的に読む

- **「機械 18% vs 専門家 23.7%」は比較になっていない。** 機械の数字は全出走犬の着順（6クラス）の正解率で、無作為なら 1/6 ≒ 16.7%。専門家の数字は1レースに1頭選んだ本命の1着率で、無作為なら同じく 1/6 だが、人気馬を選べばずっと高くなる。正しく比べるには、モデルでレースごとに1頭（例: 1着確率の最大の犬）を選び、その1着率を出す必要がある。
- **市場との比較がない。** SP（スタート時オッズ）を持っていながら、1番人気の勝率と比べていない。グレイハウンドの1番人気の勝率は一般に30%台とされる（推測。本論文には数字が無い）。だとすると、23.7% の専門家も市場より弱い可能性がある。
- **分割方法が不明。** 60/20/20 が無作為なら、同じ犬の前後のレースが学習とテストに散らばる。直近5走の平均を特徴量にしているので、情報が漏れる経路がある。
- **回収率を計算していない。** 的中率だけの評価。
- **特徴量選択とモデルの順番。** 全データで重要度を出してから分割しているように読める（p.14–19 の記述順）。これも楽観的なバイアスの元になる。
- 前処理での「取得時点ビュー」によるリークの指摘は、修士研究ながら的確。

## keiba-ai での使い方

- **取得時点ビューのリーク点検。** netkeiba などからスクレイピングした「現在の」馬主・調教師・生産牧場・通算成績は、過去レース時点の値ではない。keiba-ai の特徴量は「レース時点で確定していた値」から作る。所属変更（転厩）の履歴が取れない項目は、使わないか、取得日以降の検証にだけ使う。
- **短評テキストの数値化。** JRA の成績には「出遅れ」「不利」などの短評や、レース後の騎手コメントがある。辞書で点数化した「不利スコア」を直近 n 走で平均すると、着順だけでは見えない能力の補正になる、という仮説。検証では、不利スコアを足して log loss がどれだけ下がるかを見る。
- **評価指標をそろえる。** 「本命の1着率」と「全出走馬の着順正解率」を混ぜない。keiba-ai では、レースごとの本命1着率・Top-k・log loss を、市場（単勝オッズ）の同じ指標と並べて報告する。
- **条件付き確率への正規化。** 1頭ずつの分類器の出力をそのまま使わず、レース内で softmax（条件付きロジット）にかける。

## 関連ノート

- [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md): 専門家が選んだ10変数で NN を組んだ原点。本研究はその特徴量選択を自動化しようとした。
- [Johansson 2003](./2003-johansson-greyhound-neural-networks.md): 同じくグレイハウンドの NN。回収率まで評価している点で本研究より厳密。
- [Schumaker 2008](./2008-schumaker-svr-longshot-greyhound.md): グレイハウンドの SVR。本研究は回帰を理由に比較対象から外している。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 著者が今後の課題とした「レース内で合計1」のモデル。
- [Pudaruth 2015](./2015-pudaruth-ann-champs-de-mars.md): 同じく「専門家・人気を超えるか」を的中率だけで論じた小規模 NN 研究。
- [Lessmann 2010](./2010-lessmann-random-forest-horserace.md): RF を競馬に使い、市場オッズと組み合わせて評価した研究。

## 検索語

グレイハウンド, ドッグレース, 特徴量選択, 変数選択, Boruta, 再帰的特徴量削減, RFE, ランダムフォレスト, random forest, 深層学習, deep learning, H2O, 専門家予想, expert tipster, Shelbourne Park, Irish Greyhound Board, IGB, 短評, センチメント分析, sentiment analysis, スクレイピング, リーク, look-ahead bias, 着順分類, multi-class classification, KDD

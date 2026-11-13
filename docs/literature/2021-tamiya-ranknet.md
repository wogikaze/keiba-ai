---
title: TensorFlowでRankNetを実装して、競馬の着順予測モデルを作りました。
authors: 民谷（_tamiya）
year: 2021
venue: Qiita（BrainPad Advent Calendar 2021）
url: https://qiita.com/_tamiya/items/3926684b6ba023ebf667
topic: practitioner
tags: grey-literature, jra-van, ranknet, learning-to-rank, tensorflow, keras, time-series-split, random-baseline, automation, cloud-functions
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# RankNet（Keras）の着順モデル: テスト383レースで単勝回収率103.8%、回帰とランダムの比較つき

> 一言で: JRA-VAN DataLab の2019年以降・中央の芝レースで、同一レース内の2頭のペアを学習する RankNet を Keras で実装した。時系列で学習・開発・テストを分け、テスト（2021/10/1〜12/16、383レース）で「ランダム」「通常の回帰」「RankNet」を比べ、RankNet の単勝的中率18.0%・単勝回収率103.78%、複勝回収率78.2%。ランダムの基準線を併記している点が実践記事として珍しい。

同著者の続編「競馬予測：Google Cloud Functionsで実現する自動化戦略」（2023年）を添付 `tamiya-cloud-functions` として保存した。馬券最適化の記事（2022年）は別ノート [民谷 2022](./2022-tamiya-betting-optimization.md)。

## データ（「データ」の節）

JRA-VAN DataLab（月額2,090円）の 2019年以降、中央・芝コース。

| 分割 | 期間 | レース数 | 用途 |
|---|---|---|---|
| 学習 | 2019/1/1〜2021/6/30 | 4,412 | 学習 |
| 開発 | 2021/7/1〜2021/9/30 | 479 | Early Stopping |
| テスト | 2021/10/1〜2021/12/16 | 383 | 評価 |

## 特徴量

カテゴリのダミー化などで284次元。詳細は省略されているが、距離・回り・天気・賞金（コース関係）、**体重**・直近n件の成績・過去獲得賞金（馬関係）など。騎手と血統の特徴量はまだ入れていない（「改良点」の節）。オッズを使ったとは書かれていない。

## モデルと目的変数

- RankNet（Burges ほか 2005）: スコア関数 f を共有する2入力のネットワークで、同じレースの2頭 i, j について P(i>j) = sigmoid(f(x_i) − f(x_j)) とし、真のラベル（着順が良い方が1、同着は1/2）とのクロスエントロピーを最小化（「RankNet」の節）。
- 実装: レースをランダムに選び、その中から2頭をサンプリングするジェネレータ。f は隠れ層128・3層・ReLU・Dropout 0.1、Adam、binary_crossentropy、1エポック1,000ステップ、最大100エポック、開発データの損失が5エポック改善しなければ打ち切り。説明変数は StandardScaler で標準化（学習データで fit）。
- 比較: 着順をそのまま回帰する通常のモデル、ランダム選択。

## 評価と結果（「学習結果」の節）

賭け方: 各レースで、単勝はスコア1位の1頭、複勝は上位3頭を100円ずつ。回収率は払戻金÷賭け金。

| モデル | 単勝的中率 | 単勝回収率 | 複勝的中率 | 複勝回収率 |
|---|---|---|---|---|
| ランダム | 0.1201 | 0.7127 | 0.2262 | 0.6706 |
| 回帰 | 0.0757 | 0.3916 | 0.2007 | 0.7123 |
| RankNet | 0.1801 | 1.0378 | 0.3899 | 0.7824 |

- 回帰は単勝でランダムより悪い。RankNet は単勝・複勝ともにランダムと回帰を上回る。
- 実際に賭けようとした 2021/12/18 ターコイズS・12/19 朝日杯FS は、**出走前データの前処理を用意していなかったため買えなかった**。脚注によると、DataLab の出走前のレース情報は出走後データと埋まっている項目が違うことに直前で気づいた。想定上はターコイズSの複勝が当たり、全部100円ずつで330円のプラス。

## 運用の続編（添付 `tamiya-cloud-functions`）

- 学習・推論データは JRA-VAN から Windows PC で取得して Google Drive に置き、Colab で推論して各馬の勝利確率と発走時刻を JSON で保存。
- Cloud Scheduler が5分ごとに Pub/Sub を発行し、Cloud Functions が発走5〜10分前のレースについて netkeiba から単勝オッズをスクレイピングし、馬券最適化を実行して LINE Notify で通知。
- 動機は「馬券最適化はレース直前のオッズを使うほど良い」ため。2023/12/24 中山9R で動作確認（結果ははずれ）。性能の数値はない。

## 批判的に読む

- テストは2.5か月・383レース。単勝回収率103.78%は1位の1頭を買う戦略なので、高配当の1〜2回で大きく動く。信頼区間は書かれていない。
- 開発データは Early Stopping にだけ使い、ハイパーパラメータ選びにテストを使ったかどうかは書かれていない。
- 「体重」を特徴量に入れている。学習データの馬体重は当日発表値なので、推論時も発走約1時間前の発表を待てば使える。ただし出走前データの項目が違うと書いている以上、学習時と推論時で値の出どころが揃っているかは確認が要る。
- ランダムの単勝回収率71%・複勝67%は控除率（単勝20%・複勝20%）より低い。無作為に選ぶと人気薄を買う割合が高くなり、本命・大穴バイアスの分だけ回収率が下がるためと考えられる。
- 回帰が悪いのは、着順をそのまま数値として回帰する定式化の問題で、ランキング学習の優位をそのまま示すものではない。

## keiba-ai での使い方

- ランダム選択の回収率を**基準線**として毎回出す。このノートの値（単勝71%、複勝67%）は、芝・2021年秋の目安になる。
- ペアワイズの RankNet は LightGBM の lambdarank と比較するときの NN 側のベースライン。レース単位のサンプリングでペアを作る実装はそのまま流用できる。
- 推論パイプラインは、学習データの作成と同じコードで「出走前の時点のデータ」から特徴量を作る。過去データだけで学習・評価していると、実運用の直前に項目の違いで止まる（この記事と [masachaco 2022](./2022-masachaco-keiba-ai-data.md) が同じ問題を書いている）。
- 直前オッズの取得と最適化を発走5〜10分前に回す構成は、オッズの時点を固定した評価の設計に使える。

## 関連ノート

- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): RankNet・LambdaRank・LambdaMART の解説。
- [民谷 2022](./2022-tamiya-betting-optimization.md): このモデルの出力を使った馬券最適化。
- [Enigmo 2020](./2020-enigmo-learning-to-rank.md): 競馬のランキング学習の別の実践例。
- [Fujisawa 2024](./2024-fujisawa-ranknet-condition-datasets.md): 条件別データセットでの RankNet。
- [masachaco 2022](./2022-masachaco-keiba-ai-data.md): JRA-VAN DataLab の出走前・出走後で埋まる列の違い。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): ランダム選択の回収率が控除率より低い理由（本命・大穴バイアス）。

## 検索語

RankNet, ランキング学習, ペアワイズ, learning to rank, pairwise loss, Keras, TensorFlow, JRA-VAN DataLab, 時系列分割, Early Stopping, ランダムベースライン, 単勝回収率, 複勝回収率, Cloud Functions, Cloud Scheduler, LINE Notify, 直前オッズ

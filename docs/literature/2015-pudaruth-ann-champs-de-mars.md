---
title: Using Artificial Neural Networks to Predict Winners in Horseraces: A Case Study at the Champs de Mars
authors: Pudaruth Sameerchand, Jogeeah Manish, Chandoo Akshay Kumar
year: 2015
venue: IST-Africa 2015 Conference Proceedings (paper ref. 203), IIMC, ISBN 978-1-905824-50-2
url: https://www.researchgate.net/publication/319306984_Using_Artificial_Neural_Networks_to_Predict_Winners_in_Horseraces_A_Case_Study_at_the_Champs_de_Mars
doi:
topic: machine-learning
tags: neural-network, mauritius, small-data, accuracy-only
verified: abstract
importance: low
source: unavailable
source_version:
---

# モーリシャス Champs de Mars 競馬場で、小さな MLP に勝ち馬を当てさせた事例

> 原本未取得。IST-Africa の論文リポジトリはログインが必要で、ResearchGate と Scribd もログインなしでは取れなかった。以下は要旨、学会リポジトリの書誌情報、他文献での引用に基づく。

> 一言で: 1競馬場・約1シーズン分（347レース）で隠れ層5ノードの MLP を学習し、16レースの検証で「勝ち馬が予測上位4頭に入ったのは11レース」と報告した小規模事例。

## 位置づけ

モーリシャス大学の Pudaruth のグループは、国内唯一の競馬場 Champs de Mars を題材に、同じ問題を手法を替えて繰り返し扱っている。

- 2013年: 重み付き確率による予想（Pudaruth, Médard, Dookhun）
- 2015年: ファジィ論理による予想（Jogeeah, Chandoo, Pudaruth。同じ3人）
- 2015年: 本論文（ニューラルネット）
- 2017年以降: オッズの変動と結果の関係

本論文はその中の「ニューラルネット版」にあたる。要旨では、同競馬場のデータで NN を試した先行研究（Nairn とされる）が「数百回の実験でも傾向が見えなかった」と述べていることに触れ、それへの再挑戦として書かれている（要旨。本文の該当ページは未確認）。

## モデルとデータ（要旨から分かる範囲）

| 項目 | 内容 |
|---|---|
| 市場 | モーリシャス Champs de Mars（平地、1場のみ） |
| 学習 | 最初の41開催・計347レース |
| 検証 | 最後の2開催・16レース |
| 分割 | 時系列順（後ろの開催を検証に回す） |
| モデル | 多層パーセプトロン、隠れ層1層・5ノード、log-sigmoid 活性化 |
| 特徴量 | 未確認 |
| 評価 | 勝ち馬が予測順位の上位何位以内に入ったか |

要旨の結論は「16レース中11レースで、勝ち馬が予測上位4頭に入った」。著者は、NN のパラメータと特徴量を選び直せば大きく改善できると見ている。後続の論文では、本論文の結果が「16レース中4勝（的中率25%）」として引用されている（検索で見つけた二次引用。原本で未確認）。

## 批判的に読む

- **検証が16レースしかない。** 1着的中率25%の95%信頼区間は二項分布でおよそ7〜52%で、ほとんど何も言えない。上位4頭に入る率 11/16 も同様。
- **ベースラインが無い（と思われる）。** Champs de Mars は1レースの頭数が少なめで、1番人気の勝率は一般に30%前後ある。人気順の上位4頭に勝ち馬が入る率は7〜8割に達しうる。人気順と比べていなければ、25%や11/16はモデルの力を示さない。比較の有無は未確認。
- **回収率の評価が無い（と思われる）。** 要旨には回収率も控除率も出てこない。
- **ハイパーパラメータの選び方。** 「5ノード」をどう決めたかが要旨に無い。16レースの検証で選んだなら、その成績は楽観的になる。
- **再現性。** データは公開されていないと思われる。特徴量の一覧も原本を見ないと分からない。

時系列で学習と検証を分けている点は正しい。ただし規模が小さすぎて、手法の良し悪しは判断できない。

## keiba-ai での使い方

- **評価の反面教師として使う。** 「上位k頭に勝ち馬が入る率」を報告するときは、同じ指標を人気順（単勝オッズ順）でも計算して並べる。keiba-ai の評価スクリプトでは、Top-k 的中率を必ず市場順位と対で出す。
- **検証レース数の目安。** 的中率の差を ±2〜3 ポイントの精度で見るには、数千レースの検証期間が要る。数十レースの検証は結論に使わない。
- 手法（小さな MLP）自体は現在の GBDT や順位学習に置き換わっており、取り入れる要素は無い。

## 関連ノート

- [Davoodi 2010](./2010-davoodi-ann-horse-racing.md): 同時期の小規模 ANN 勝ち馬予測。同じ評価の弱点を共有する。
- [Williams 2008](./2008-williams-neural-networks-jamaica.md): ジャマイカの小市場で NN を試した例。小さな市場どうしで比べられる。
- [Johansson 2003](./2003-johansson-greyhound-neural-networks.md): グレイハウンドの NN。回収率まで見ている点で本論文より踏み込んでいる。
- [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md): 初期の NN 予想。小データでの NN の限界を比べられる。
- [Lessmann 2010](./2010-lessmann-random-forest-horserace.md): 市場オッズと組み合わせて評価する、より厳密な ML 研究。

## 検索語

ニューラルネットワーク, 多層パーセプトロン, MLP, 人工ニューラルネット, ANN, 勝ち馬予測, モーリシャス, シャン・ド・マルス, Champs de Mars, Champ de Mars, Mauritius, horse racing prediction, winner prediction, top-4 accuracy, 上位4頭的中率, 小規模データ, small data, IST-Africa

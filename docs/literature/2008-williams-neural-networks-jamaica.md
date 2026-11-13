---
title: A Case Study Using Neural Networks Algorithms: Horse Racing Predictions In Jamaica
authors: Williams Janett, Li Yan
year: 2008
venue: Proceedings of the International Conference on Artificial Intelligence (ICAI 2008), Las Vegas, CSREA Press, 16-22
url: https://research.usq.edu.au/item/9yvw4/a-case-study-using-neural-networks-algorithms-horse-racing-predictions-in-jamaica
doi:
topic: machine-learning
tags: neural-network, backpropagation, levenberg-marquardt, jamaica, accuracy-only
verified: abstract
importance: medium
source: unavailable
source_version: none
---

# ジャマイカ Caymanas 競馬場の143レースで、ニューラルネットの学習則4種を比べた事例研究

> 一言で: 誤差逆伝播（BP）、準ニュートン、Levenberg-Marquardt、共役勾配の4つの学習則で同じネットを学習し、平均約74%の「精度」で差はほとんどなかったと報告する小規模研究。回収率の評価はない。

**原本未取得。** 出版社版 PDF は USQ ePrints（eprints.usq.edu.au/4300）で無料公開されているが、取得時にサーバが接続を拒否し（research.usq.edu.au も応答 405）、取得できなかった。後日再取得する。以下は大学リポジトリの要旨と、全文を取得済みの後続論文の記述に基づく。

## 書誌

- Williams Janett, Li Yan（University of Southern Queensland）。ICAI 2008（ラスベガス、2008年7月14-17日）、CSREA Press、Arabnia & Mun 編、pp.16-22。頁は [Lyons 2016](./2016-lyons-greyhound-man-v-machine.md) の参考文献（p.23）と一致。DOI なし。
- Semantic Scholar は第一著者を Jane と表記するが、大学リポジトリと引用側は Janett。

## 二次資料から分かる設定

[Borowski 2021](./2021-borowski-ml-flat-racing-poland.md) の要約（同原本 p.6）による:

- データ: 2007年のジャマイカの平地 143 レース、距離 1,000〜3,000m。
- 入力: 馬と騎手の特徴を表す8変数。
- 構成: 1頭につき1つのネット（各馬を独立に評価）。
- 分割: 学習80%・テスト20%。
- 結果: 4アルゴリズムの平均精度 74%、どれも有意には勝らない。

大学リポジトリの要旨では、4アルゴリズムとも「許容できる予測」を出したとする。旧ノートは「BP がわずかに良いが学習時間とパラメータ選択の手間が大きい」と書いていたが、これは後続論文の要約によるもので、原本での表現は未確認。「74%」が何の精度（勝ち馬の的中か、上位3着の判定か、馬ごとの2値分類の正解率か）かも未確認。馬ごとの2値分類の正解率なら、全頭を「負け」と予測するだけで 80% 台後半になりうるので、74% は高い数字ではない（推測）。

なお、ResearchGate のこの論文の説明には「モメンタム付き BP を含む5アルゴリズム」とあるが、これは [Davoodi 2010](./2010-davoodi-ann-horse-racing.md) の設定と混同されている可能性が高い。

## 批判的に読む

- **評価の弱さ**: 143レースの20%（約29レース）がテスト集合で、精度の差を論じるには小さすぎる。
- **レース内の構造を無視**: [Torne 2021](./2021-torne-hong-kong-softmax-nn.md) は本論文を、Davoodi (2010)、Pudaruth (2013)、Chen (1995) と並べ「1頭ずつ独立に勝つかどうかを予測する、手作り特徴量の枠組み」に分類し、数百レース・10未満の特徴量で、論文間の数値は比較できないと指摘する（同原本 p.3）。
- **特徴量選択の根拠がない**: [Lyons 2016](./2016-lyons-greyhound-man-v-machine.md) は本論文などを、特徴量の選び方の動機を説明していない例として挙げる（同原本 p.6 付近, L184）。
- 分割がランダムか時系列順かは未確認。
- 回収率や市場オッズとの比較はない。

## keiba-ai での使い方

- **反面教師としての使い方**: 「精度◯%」は、(1) 何の精度か、(2) 人気順ベースライン（1番人気の勝率など）と比べてどうか、(3) 回収率はどうか、が揃わないと意味がない。keiba-ai の実験レポートでは、的中率を書くなら必ず「1番人気を買い続けた場合」と並べる。
- 学習則（BP か LM か）の比較は、Adam と勾配ブースティングが標準の現在ではほぼ論点にならない。
- 小規模市場（ジャマイカ）の研究として、地方競馬など頭数・レース数が少ない市場の予測の難しさを考える材料にはなる。

## 関連ノート

- [Davoodi 2010](./2010-davoodi-ann-horse-racing.md): 同じく学習則の比較を行った後続研究（5アルゴリズム）。
- [Pudaruth 2015](./2015-pudaruth-ann-champs-de-mars.md): 小規模市場（モーリシャス）での NN 適用。
- [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md): 1頭ずつ独立に分類する枠組みの原型。
- [Borowski 2021](./2021-borowski-ml-flat-racing-poland.md): 本論文の設定を最も詳しく要約している二次資料。
- [Torne 2021](./2021-torne-hong-kong-softmax-nn.md): 1頭独立の枠組みを批判し、レース内 softmax を使う。
- [Lyons 2016](./2016-lyons-greyhound-man-v-machine.md): 特徴量選択の根拠の欠如を指摘。

## 検索語

ジャマイカ, Caymanas, ニューラルネットワーク, 誤差逆伝播, 準ニュートン法, Levenberg-Marquardt, 共役勾配法, 学習アルゴリズム比較, 的中率, 精度, 小規模市場, neural network, backpropagation, quasi-Newton, conjugate gradient descent, horse racing prediction, ICAI 2008, Jamaica

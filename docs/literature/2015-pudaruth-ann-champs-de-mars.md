---
title: Using Artificial Neural Networks to Predict Winners in Horseraces: A Case Study at the Champs de Mars
authors: Pudaruth Sameerchand, Jogeeah Manish, Chandoo Akshay Kumar
year: 2015
venue: IST-Africa 2015 Conference Proceedings (paper ref. 203), IIMC, ISBN 978-1-905824-50-2
url: https://www.researchgate.net/publication/319306984_Using_Artificial_Neural_Networks_to_Predict_Winners_in_Horseraces_A_Case_Study_at_the_Champs_de_Mars
doi:
topic: machine-learning
tags: neural-network, mauritius, small-data, accuracy-only, odds-feature
verified: fulltext
importance: low
source: downloaded
source_version: published
---

# モーリシャス Champs de Mars 競馬場で、小さな MLP に着差を予測させた事例

原本は Scribd（document 357389803）に置かれた学会録の版（8ページ、各ページに「Copyright © 2015 The authors」）。Scribd はページ本体を JS で読み込むため、ページごとのデータ（`library/<slug>/attachments/scribd-page1〜8`）を保存し、そのテキスト層を機械的に連結した HTML を `library.py add` で原本にした。表のレイアウトは崩れている。ページ番号は原本の「Page N of 8」。

> 一言で: 2014年シーズンの Champs de Mars のデータ（学習347レース）で、隠れ層5ノードの MLP に「勝ち馬からの着差」を予測させ、最後の2開催16レースで勝ち馬4頭（25%）を当てた。人気馬（40%）にも予想家（38%）にも負けたが、当てた勝ち馬が穴馬だったので回収率はプラスだったと主張する (p.7)。

## 原本で確認・訂正した点

- **市場オッズを特徴量に使っている**。特徴量は斤量・枠順・過去5走の着順・「土曜のオッズ」・距離の5種 (p.6)。旧ノートは特徴量を未確認としていた。
- **ベースラインはある**。2014年の1番人気の勝率40%、最良の予想家の的中率38%と比べ、本手法（25%）は劣ると著者自身が認めている (p.7)。旧ノートの「ベースラインが無いと思われる」は誤り。
- **回収率も報告している**。16レースに Rs100 ずつ賭けて Rs2000 のプラス、回収率 225% (p.7)。旧ノートの「回収率の評価が無い」は誤り。ただし計算の中身は示されていない（後述）。
- 旧ノートにあった「Nairn の先行研究への再挑戦」という記述は本文に見当たらない。後続論文の要約を取り違えたものと思われる。
- データは2014年シーズン（全43開催）(p.3, 5)。

## データと設定

| 項目 | 内容 |
|---|---|
| 市場 | モーリシャス Champs de Mars（直線約300mと短い）(p.1) |
| 期間 | 2014年シーズン、43開催 (p.5) |
| 学習 | 最初の41開催・347レース（1開催平均約9レース）(p.3, 5) |
| 検証 | 最後の2開催（第42・43開催）・16レース (p.5) |
| 目的変数 | 勝ち馬からの着差（勝ち馬は0）。予測着差の小さい順に順位を付ける (p.5) |
| 特徴量 | 斤量、枠順、過去5走の着順、土曜のオッズ、距離 (p.6) |
| モデル | MLP、隠れ層1層・5ノード、zero-based log-sigmoid (p.5, Table 1) |
| 学習設定 | 20,000 エポック、学習率 0.3、モメンタム 0.60、初期重み 0.3 (p.5, Table 1) |
| ツール | NeuroXL Predictor（Excel アドイン）の試用版 (p.5) |

騎手の勝率（勝利数/騎乗数）を特徴量として定義しているが、国際開催では全騎手を同等とみなしたため使わなかった (p.4, 6)。

## 結果

- 1着的中 4/16（25%）(p.7)。
- 予測2位の馬が勝ったのが3レース、予測3位が2レース、予測4位が2レース (p.7)。要旨の「16中11レースで勝ち馬が予測上位4頭に入った」(p.1) はこれの合計。
- 当たった勝ち馬はどれも人気馬ではなく、4頭中3頭のオッズは Rs1000 超だった (p.7)。
- 第42開催第1レースの例 (p.6, Table 2) では1・2着を当てたが、3・4着は予測6・7位の馬だった。

## 批判的に読む

- **検証が16レースだけ**。25%の95%信頼区間はおよそ7〜52%。回収率 225% は穴馬3頭の的中に依存し、偶然でも十分起こる。著者も「結論を出すには早い」と書いている (p.7)。
- **回収率の数字が合わない**。本文は「Rs2000 のプラス」(p.7)、結論は「225% の回収率」(p.7) と書くが、賭け総額 Rs1600 に対する計算の内訳がない。オッズの表記（例: 1200）が払戻額か倍率かも説明がない。
- **オッズの時点**。「土曜のオッズ」が締切オッズか前売りかが不明で、確定オッズならリークの可能性がある。
- **ハイパーパラメータの決め方が書かれていない**。5ノード・20,000 エポックの根拠がない。
- **Figure 2 の説明** (p.6) は学習データへの当てはめを示すだけで、汎化の評価ではない。
- 時系列で学習と検証を分けている点は正しい。

## keiba-ai での使い方

- **評価の反面教師として使う**。的中率と回収率は、人気順のベースラインと並べたうえで、検証レース数と信頼区間を必ず付ける。16レースの回収率は何も言わない。
- **「穴馬を当てて回収率が上がる」現象の確認**。オッズを特徴量に入れたモデルが人気薄を上位に置くなら、それが本当の情報か、オッズの非線形な扱いの副産物かを、時系列のテスト期間でオッズ帯別の回収率（控除率込み）に分けて確かめる。
- **着差を目的変数にする案**。勝ち負けの2値より情報が多い。keiba-ai では着差（またはタイム差）の回帰をランキング学習と比べる実験の候補になる。ただし着差は大差負けで値が飛ぶので、上限で切るか順位に変換する。
- 手法（小さな MLP、Excel ツール）自体は取り入れる要素がない。

## 関連ノート

- [Davoodi 2010](./2010-davoodi-ann-horse-racing.md): 本論文が比較対象に挙げる NN 勝ち馬予測（Aqueduct、100レースで最良39勝）(p.2-3)。
- [Williams 2008](./2008-williams-neural-networks-jamaica.md): ジャマイカの小市場での NN。本論文が引用する (p.3)。
- [Johansson 2003](./2003-johansson-greyhound-neural-networks.md): グレイハウンドの NN。回収率まで検証している点で比べられる。
- [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md): 初期の NN 予想。小データでの NN の限界。
- [Lessmann 2010](./2010-lessmann-random-forest-horserace.md): 市場オッズと組み合わせて評価する、より厳密な ML 研究。

## 検索語

ニューラルネットワーク, 多層パーセプトロン, MLP, 人工ニューラルネット, ANN, 勝ち馬予測, 着差予測, 穴馬, 回収率, 人気馬, 予想家, モーリシャス, シャン・ド・マルス, Champs de Mars, Champ de Mars, Mauritius, horse racing prediction, winner prediction, margin prediction, longshot, tipster, crowd favourite, top-4 accuracy, 上位4頭的中率, 小規模データ, small data, NeuroXL, IST-Africa

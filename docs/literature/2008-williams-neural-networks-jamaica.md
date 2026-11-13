---
title: A Case Study Using Neural Network Algorithms: Horse Racing Predictions in Jamaica
authors: Williams Janett, Li Yan
year: 2008
venue: Proceedings of the International Conference on Artificial Intelligence (ICAI 2008), Las Vegas, CSREA Press, 16-22
url: https://eprints.usq.edu.au/4300/
doi:
topic: machine-learning
tags: neural-network, backpropagation, levenberg-marquardt, jamaica, accuracy-only, finish-time
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# ジャマイカ Caymanas 競馬場の143レースで、ニューラルネットの学習則4種を比べた事例研究

> 一言で: 8入力・1出力の小さなネットで各馬の走破タイムを予測し、その順で着順を出す。誤差逆伝播（BP）、準ニュートン（BFGS）、Levenberg-Marquardt（LM）、共役勾配（CGD）の4つで学習し、どれも似た結果で BP がわずかに良かった、と報告する。評価は「上位3頭のうち何頭を当てたか」の集計だけで、市場オッズとの比較も回収率も無い。

原本は USQ ePrints の出版社版 PDF（スキャン）。直接の取得は接続拒否だったため、Internet Archive の 2022年のスナップショットから取得し、機械 OCR した。ページ番号は会議録の頁（16〜22。PDF の1〜7ページ）。

## 既存ノートからの訂正

原本を読む前のノートは、大学リポジトリの要旨と後続論文（Borowski 2021 など）の要約に頼っていた。原本で次のことが分かった。

- 題名は「Neural Network Algorithms」（単数の Network）。旧ノートの「Neural Networks Algorithms」は誤り (p.16)。
- 「1頭につき1つのネット」は正しいが、出力は勝ち負けの2値ではなく**走破タイム**。予測タイムの順で着順を作る (p.19)。
- 距離について、Borowski の要約は 1,000〜3,000m とするが、原本では「使ったレースは 1,000〜1,820m」(p.20)。ジャマイカの平地競走が 1,000〜3,200m で行われる、という記述は別にある (p.18)。
- 「BP がわずかに良いが、学習時間とパラメータ選択の手間が大きい」は原本の要旨と結論にある表現だった (p.16, 22)。
- 「74%」の中身は原本でも定義されていない（下記）。

## データ (p.18–19)

- Caymanas Race Track（ジャマイカ、Portmore）。1周 1,800m のダート、最大16頭。
- 2007年1月1日〜6月16日の 143 レース (p.16, 19)。開催は水・土と祝日。
- 入力変数は8個: 距離、レースの種類、過去の着順、馬と騎手の重量、走破タイム、馬具（バイザー・ブリンカー）、馬齢、出走頭数 (p.18)。各変数は正規化 (p.19)。
- 元データは競馬場の出す馬柱（past performance）。最大9走分の過去走が載る (p.18–19)。
- 学習80%・テスト20% (p.19)。ランダムか時系列順かは書かれていない。

## モデルと学習則 (p.16–17, 21)

- 市販ソフト Trajan 6.0 で4つの学習則を比較。BP はモメンタム付き（学習率 $\eta$、モメンタム $\alpha$）。
- BP の構成は 8-13-1、バイアス節点つき。学習率 0.02、モメンタム 0.4 が良かった。エポック数は 100 (p.20–21)。
- LM の更新は $\Delta w = -(Z^\top Z + \lambda I)^{-1} Z^\top E$（$Z$ は誤差の重みによる偏微分の行列、$E$ は誤差ベクトル）、CGD は Polak–Ribière で探索方向を更新する (p.17)。

## 結果

1レースの例（6月9日 第5レース）では、4つとも上位3頭の顔ぶれは当てたが、勝ち馬を当てたのは CGD だけだった (p.19–20, Table 1)。

Table 2 (p.21) はテストの各レースを、予測上位3頭と実際の上位3頭の一致で分類する。

| 区分 | BP | CGD | LM | QN |
| --- | --- | --- | --- | --- |
| 3頭とも正しい（順序も） | 60 | 48 | 58 | 57 |
| 3頭とも入っている | 12 | 14 | 11 | 11 |
| 2頭が入っている | 14 | 11 | 10 | 9 |
| 1頭が入っている | 19 | 27 | 23 | 23 |
| 1頭も入っていない | 38 | 43 | 41 | 40 |

1行目と2行目の違いは表に定義が無く、「順序も一致」と「顔ぶれだけ一致」と読むのは推測である。

- 各列の合計は 143（QN だけ 140）。テストは 143 レースの20%のはずなのに、表は 143 レース全部を数えている。学習に使ったレースを評価に含めた可能性がある（未確認）。
- 「少なくとも1頭が上位3着に入った」レースは4手法合計で 407 / 572 (71%) と本文にある (p.20)。表から数えると BP 105、CGD 100、LM 102、QN 100 で、合計 407 になる。
- 要旨と結論の「平均 74% の精度」(p.16, 22) がどの数字から出たかは原本に書かれていない。BP の「少なくとも1頭」が 105/143 = 73% で近いが、確認できない。

> All four algorithms produce very similar results with BP outperforms slightly better. (p.22)

## 批判的に読む

- **評価の定義が曖昧。** 「精度 74%」の定義が無く、表の母数がテスト集合（約29レース）ではなく全 143 レースになっている。学習データでの当てはまりを見ている疑いがある。
- **ベースラインが無い。** 上位3頭のうち1頭以上を当てるのは易しい。1番人気〜3番人気を挙げるだけでも相当の割合で当たるはずだが、オッズや人気との比較は無い。
- **走破タイムを入力にも使う。** 入力の「走破タイム」が過去走のものか当該レースのものか書かれていない。当該レースのタイムならリークになる（未確認）。
- **1頭ずつ独立のネット。** レース内の相対関係を学習しない。
- **規模が小さい。** 半年・1競馬場・143レース。学習則の優劣を論じるには不足。
- 回収率の評価は無い。

## keiba-ai での使い方

- **反面教師としての使い方。** 「精度◯%」は、(1) 何の精度か、(2) 人気順ベースラインと比べてどうか、(3) テスト集合だけで数えたか、(4) 回収率はどうか、が揃わないと意味がない。keiba-ai の実験レポートでは、的中率を書くときは必ず「1番人気（または上位人気）を買い続けた場合」と並べ、評価対象のレース数を明記する。
- **走破タイム回帰から着順を作る方式**は、レース内の相対比較を直接学習しない。keiba-ai でタイム回帰を試すなら、条件付きロジットや LambdaRank のような順位の目的関数と比べる実験を置く。
- 学習則（BP か LM か）の比較は、Adam と勾配ブースティングが標準の現在ではほぼ論点にならない。

## 関連ノート

- [Davoodi 2010](./2010-davoodi-ann-horse-racing.md): 同じく学習則の比較を行った後続研究（5アルゴリズム）。
- [Gulum 2018](./2018-gulum-graph-features.md): 本論文を関連研究に挙げる修士論文。
- [Pudaruth 2015](./2015-pudaruth-ann-champs-de-mars.md): 小規模市場（モーリシャス）での NN 適用。
- [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md): 本論文が引くグレイハウンドの NN 研究。1頭ずつ独立に扱う枠組みの原型。
- [Borowski 2021](./2021-borowski-ml-flat-racing-poland.md): 本論文の設定を要約している二次資料（距離の記述が原本と食い違う）。
- [Torne 2021](./2021-torne-hong-kong-softmax-nn.md): 1頭独立の枠組みを批判し、レース内 softmax を使う。
- [Lyons 2016](./2016-lyons-greyhound-man-v-machine.md): 特徴量選択の根拠の欠如を指摘。

## 検索語

ジャマイカ, Caymanas, ニューラルネットワーク, 誤差逆伝播, 準ニュートン法, BFGS, Levenberg-Marquardt, 共役勾配法, Polak-Ribiere, 学習アルゴリズム比較, 走破タイム予測, finish time, 的中率, 精度, 上位3着, 小規模市場, Trajan, neural network, backpropagation, quasi-Newton, conjugate gradient descent, horse racing prediction, ICAI 2008, Jamaica

---
title: Ga Yau: Machine analysis of Hong Kong horse racing data
authors: Torné Olaf
year: 2021
venue: Stanford CS230 (Deep Learning) project report, Winter 2021
url: http://cs230.stanford.edu/projects_winter_2021/reports/70738477.pdf
doi:
topic: machine-learning
tags: hong-kong, hkjc, softmax, neural-network, label-smoothing, public-odds-baseline, grey-literature
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# 香港競馬で、1レース全頭をまとめて softmax にかける NN（授業レポート）

> 一言で: HKJC の 2003〜2020年・12,820レースで、1レース14頭×33特徴量を入力し、14頭の勝率を softmax で出す全結合 NN を作った。1〜3着に 0.5/0.25/0.25 の重みを付けた「ソフトラベル」で、テストの1着的中率が 11.1% から 14.4% に上がった。ただし「人気（public odds）」の的中率が 10.1% と、無作為（8.4%）並みに低く報告されており、比較対象の作り方に誤りがあると考えられる。

## 位置づけ

Stanford の深層学習の授業（CS230）の7ページのレポート。著者は自分の模型を [Bolton 1986](./1986-bolton-conditional-logit.md) の多項ロジットを全結合 NN に一般化したものと位置づけている（p.3）。先行研究の多くは「1頭ずつ sigmoid で勝つか否かを出す」形で、数百レース・10変数未満の規模だった。本研究は「レース全頭をまとめて softmax」「大きなデータ」「市場オッズとの比較」を新しさとして挙げる（p.2–3）。

## データと特徴量

| 項目 | 内容 | 出典 |
|---|---|---|
| 市場 | 香港ジョッキークラブ（HKJC） | p.1 |
| 取得元 | hkracingdb.com | p.3, p.7 |
| 期間・規模 | 2003〜2020年、12,820レース | p.3 |
| 分割 | 2003〜2018年を学習。2018-19 と 2019-20 の2シーズンから dev と test を取る | p.4 |
| 入力 | 1レース = 14行（頭数が少なければゼロで埋める）× 33特徴量 | p.3 |

特徴量は、HKJC の初心者向け冊子『Racing 201: How to pick your winning horse』の助言を数値化したもの（p.3）。例えば次のようなもの。

- `horse_dist_course_going_rec_1`: 同じ距離・コース・馬場状態での前走着順
- `trainer_dist_course_going_rec_1`: 同じ調教師の馬の、同じ距離・コース・馬場状態での直近の着順
- `d_actual_weight`: 斤量の変化

馬・騎手・調教師の ID は、過去成績の特徴量を作った後で捨てる（p.2–3）。

## モデル

$$R \in \mathbb{R}^{14 \times 33} \to \text{Flatten} \to (\text{Linear} \to \text{ReLU}) \times 2 \to \text{Linear} \to \text{Softmax} \to p \in \Delta^{14}$$

- 隠れ層2層・各60ユニット、dropout 0.5、学習可能パラメータ 32,534（p.4）
- 出力 $p_i$ は馬 $i$ が勝つ確率

### ソフトラベル

one-hot の代わりに、1着・2着・3着の馬にそれぞれ $p_{win}, p_{sec}, p_{third}$（合計1）を置いたラベル $y_{top3}$ を作り、softmax 交差エントロピーで学習する（p.4）。調整の結果 $p_{win}=0.5,\ p_{sec}=p_{third}=0.25$ を採用した。

> tuning the loss function to reward not only correct 1st place predictions, but also 2nd and 3rd, helps it to converge to a model that has better accuracy (p.2)

## 結果（p.5, Figure 2）

| モデル | dev 的中率 | dev Top-3 | test 的中率 | test Top-3 |
|---|---|---|---|---|
| DH_v1（one-hot ラベル） | 13.6% | 35.2% | 11.1% | 35.9% |
| DH_v1（0.5/0.25/0.25） | 14.9% | 37.0% | 14.4% | 38.6% |
| 人気（public odds） | 7.4% | 32.8% | 10.1% | 34.0% |
| 無作為 | 8.5% | 25.5% | 8.4% | 25.1% |

「Top-3」は、モデルが最も勝率を高く見た馬が3着以内に入った割合。モデルの本命と人気の本命が一致したのは test で 6.7% だけだった（p.5）。

ネットワークを大きくしても精度はほとんど上がらなかった。著者は、手作りの特徴量がすでに情報を十分に持っており、馬 ID を捨てているので、深いネットが学べる構造が残っていないためだと説明する（p.2）。

## 批判的に読む

- **人気の的中率が低すぎる。** 香港の1番人気の勝率は一般に3割前後である（本レポート外の一般的な知識）。それが 7.4〜10.1% で、無作為の 8.4% とほぼ同じなのは異常。最大オッズの馬（最低人気）を選んでいる、オッズの列がずれている、といった誤りが疑われる。本命の一致率 6.7% も、無作為な一致（1/14 ≒ 7%）とほぼ同じ。正しく作った人気と比べれば、モデルの 14.4% はかなり弱い可能性が高い。著者の「人気を大きく上回る」という結論（p.5）は支持されない。
- **入力の並び順に依存する。** 14行を flatten して全結合層に入れるので、同じ馬が何行目に来るかで出力が変わり、重みも行ごとに別になる。Bolton–Chapman の条件付きロジットは全馬で重みを共有していた。その性質が失われており、「一般化」とは言いにくい。行の並べ方（馬番順か）は未確認。
- **評価は的中率だけ。** 確率を出しているのに、log loss・キャリブレーション・回収率を見ていない。
- **dev/test の取り方。** 2シーズンから dev と test を無作為に取っている（p.4）。同じ開催日のレースが両方に入りうるが、レース内で完結するモデルなのでリークは小さい。
- 良い点: 学習期間とテスト期間は時系列で分かれている。

## keiba-ai での使い方

- **ソフトラベル（1〜3着に重み）は試す価値がある。** keiba-ai の順位学習や softmax 型のモデルで、目的を「1着 one-hot」から「1着 0.5・2着 0.25・3着 0.25」に変えると、勝率の推定がなめらかになり、1着的中率と log loss がどう変わるかを見る。ただしこのラベルで学習した出力は「勝率」ではなくなるので、勝率として使う前に再キャリブレーションが要る。評価は1着の log loss で行う。
- **レース単位 softmax は重み共有で作る。** 馬ごとに同じネットでスコアを出し、レース内で softmax をかける形（条件付きロジットの NN 版）にする。flatten はしない。
- **市場ベースラインの点検。** 評価スクリプトで「1番人気の勝率」を出し、JRA ではおよそ 3割強になることを毎回確かめる。ここがずれていたら、オッズの結合にバグがある。
- **特徴量の発想。** 「同じ距離・コース・馬場での前走着順」「同じ調教師の同条件での直近成績」のように、条件を絞った直近成績は JRA にもそのまま移せる。

## 関連ノート

- [Bolton 1986](./1986-bolton-conditional-logit.md): 著者が一般化したと言う多項ロジット。重み共有がある点で構造は本研究より筋が良い。
- [Chapman 1994](./1994-chapman-hong-kong-2000-races.md): 同じ香港市場で条件付きロジットを使った研究。人気の的中率の水準の参考になる。
- [Chung 2017](./2017-chung-svm-committee-hong-kong.md): 香港の SVM 研究。同じく市場比較の扱いが疑わしい。
- [Davoodi 2010](./2010-davoodi-ann-horse-racing.md): 本研究が「1頭ずつ sigmoid」の例として挙げる先行研究。
- [Williams 2008](./2008-williams-neural-networks-jamaica.md): 同上。
- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): 順位学習。上位着順に重みを付けるという発想を損失関数で扱う系統。
- [Guo 2017](./2017-guo-calibration-modern-nn.md): NN の出力はそのままでは確率として較正されていない。ソフトラベル後の再較正の根拠。

## 検索語

香港, 香港ジョッキークラブ, HKJC, Hong Kong Jockey Club, ニューラルネット, 全結合, softmax, ソフトマックス, レース単位, 多頭同時, multi-horse, ソフトラベル, soft label, ラベル平滑化, label smoothing, top-3 labelling, 交差エントロピー, cross entropy, 条件付きロジット, multinomial logit, 特徴量エンジニアリング, 人気, public odds, ベースライン, CS230, Stanford

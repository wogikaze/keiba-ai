---
title: Predicting good probabilities with supervised learning
authors: Niculescu-Mizil Alexandru, Caruana Rich
year: 2005
venue: Proceedings of the 22nd International Conference on Machine Learning (ICML 2005) 625-632
url: https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf
doi: 10.1145/1102351.1102430
topic: evaluation-and-features
tags: calibration, platt-scaling, isotonic-regression, boosted-trees, random-forest, reliability-diagram, learning-curve
verified: fulltext
importance: high
source: downloaded
source_version: accepted-manuscript
---

# 10種の学習器の確率はどう歪むか、Platt と isotonic でどこまで直るか

> 一言で: ブースティング木・ブースティング切り株・SVM のような最大マージン法は予測確率を 0 と 1 から中央へ押し寄せ、信頼性図が S 字に歪む。ナイーブベイズは逆に端へ押しやる。ニューラルネット・バギング木・ロジスティック回帰はもともとよく校正されている。校正データが約 1,000 件未満なら Platt scaling、それ以上なら isotonic 回帰が同等以上で、校正後に最も良い確率を出すのはブースティング木・ランダムフォレスト・SVM だった。

原本は著者のサイトにある ICML 2005 のカメラレディ版 (8ページ)。ページ番号は論文集のページ (pp.625–632) に換算して示す。

## 問いと手法

正解率や AUC が良くても確率が良いとは限らない (p.625)。10 種の学習器（SVM, ニューラルネット, 決定木, k近傍, バギング木, ランダムフォレスト, ブースティング木, ブースティング切り株, ナイーブベイズ, ロジスティック回帰）について、予測確率の歪み方と、2つの事後校正の効き方を調べた。

- **Platt scaling** (p.625–626): 出力 $f$ を $1/(1+\exp(Af+B))$ に通し、$A,B$ を最尤推定する。目標値は Platt (1999) のベイズ的な $y_+=(N_++1)/(N_++2)$, $y_-=1/(N_-+2)$。
- **isotonic 回帰** (p.626): 単調非減少の階段関数を PAV アルゴリズムで当てる（Zadrozny & Elkan 2002 の方法）。どんな単調な歪みも直せるが、そのぶん過学習しやすい。

どちらも、**モデルの学習に使ったデータで校正すると偏る**ので、独立の校正データを使う (p.626)。

> if the model learns to discriminate the train set perfectly and orders all the negative examples before the positive examples, then the sigmoid transformation will output just a 0,1 function. (p.626)

## 実験設定

- 2値分類 8 問題: ADULT, COV_TYPE, LETTER.P1（"O" 対その他, 正例 3% の不均衡）, LETTER.P2（A–M 対 N–Z）, MEDIS, MG, SLAC, HS (Table 2, p.626)。
- 各学習器でパラメータを多数変えたモデルを作り、**4,000 件で学習、独立な 1,000 件で校正**、別の大きなテストで評価 (p.627)。
- 信頼性図は予測値を 10 等幅ビンに分け、ビン内の平均予測値と正例割合を比べる (p.627)。
- 学習曲線: 校正データを 32 件から 8,192 件まで2倍ずつ変える。各問題 10 試行 (p.630)。

## 結果

### 学習器ごとの歪み (pp.627–630)

| 学習器 | 校正前の歪み | 合う校正 |
|---|---|---|
| ブースティング木 | 予測が中央に集中、信頼性図が S 字（8問題中7つ） | Platt・isotonic とも大きく改善 |
| ブースティング切り株 | 同上、最も極端 | 同上 |
| SVM | S 字 | 同上 |
| ニューラルネット | ほぼ対角線上 | 不要。Platt はかえって裾を中央へ寄せ、少し悪化 |
| ロジスティック回帰・バギング木 | よく校正済み | ほぼ不要 |
| 決定木（単体） | 分散が大きく校正が崩れる | isotonic が少し効く。Platt は効かない |
| ランダムフォレスト | 問題による。いくつかで弱い S 字 | 校正で改善 |
| ナイーブベイズ | 端へ押しやる（逆 S 字） | isotonic が適する |

S 字の歪みは最大マージン法に特有だと著者は述べる (p.628)。ランダムフォレストやバギングが 0・1 の近くを予測しにくいのは、ベース木の分散が [0,1] の端で片側にしか出ないからだ、と説明している。0 を予測すべき例でも、1本でも 0 より大きい値を出せば平均は 0 から離れる (p.629)。

### 校正データの量 (pp.630–631, Fig.7)

- 校正データが約 200〜1,000 件より少ないと、9 学習器すべてで Platt が isotonic に勝つ。isotonic は制約が弱く過学習しやすい。
- 1,000 件以上では、isotonic は常に Platt と同等以上。
- よく校正された学習器（ニューラルネット, バギング木, ロジスティック回帰）は、校正データが多くても改善せず、少ないとかえって悪化する。
- 最大マージン法は、校正データが少なくても改善する。

### 校正後の比較 (pp.631–632, Fig.8)

8問題 × 5試行の平均で、二乗誤差と対数損失を比べた。校正前に最も良いのはランダムフォレスト・バギング木・ニューラルネット。校正後はブースティング木・ランダムフォレスト・SVM が最良になる (p.632)。Fig.8 のブースティング木は、対数損失が校正前の約 0.49 から Platt 後に約 0.38 へ下がっている（図からの読み取り）。二乗誤差の軸は 0.26〜0.38 で、値の大きさからは RMSE の可能性がある（未確認）。

## 批判的に読む

- 2値分類だけ。多クラスや、競馬のような「レース内で確率の和が 1」の問題は扱わない。
- 学習 4,000 件・校正 1,000 件は小さい。学習データが多いと、ブースティングの歪みの大きさも変わる可能性がある（本論文では未検証）。
- ADULT では、ブースティングを 4 回で止めたモデルが最良だったため S 字が出ない、と脚注で断っている (p.627)。つまり歪みの強さは反復回数（過学習の度合い）で変わる。今日の勾配ブースティング（学習率が小さく、対数損失を直接最小化する LightGBM 等）は、本論文の AdaBoost 系とは歪み方が違う可能性が高い（推測）。
- 各問題・学習器で「校正後に最も良いモデル」を選ぶのに、校正と同じ 1,000 件を使っている (p.631)。モデル選択の楽観バイアスが少し入る。

## keiba-ai での使い方

- **LightGBM の確率を必ず信頼性図で確認する**: 本論文の分類では、LightGBM の binary 目的関数は「対数損失で学習するブースティング」で、AdaBoost 系ほど S 字にならないはず。仮説: keiba-ai の LightGBM 単勝モデルの信頼性図は、高確率側（30%以上）でわずかに過大、低確率側（5%未満）でわずかに過小に出る。校正前後の Brier・log loss の差が小さければ校正は省く（論文の「よく校正された学習器に校正するとかえって悪化」に従う）。
- **ランキング目的（lambdarank）のスコアは確率ではない**: lambdarank の出力は順位だけを最適化していて、値には意味がない。最大マージン法と同じく後処理の校正が必須。レース内 softmax の温度を Platt と同じ要領で検証期間に当てる。
- **校正データの量の目安**: 「1,000 件未満なら Platt、それ以上なら isotonic」を keiba-ai に置き換えると、校正の単位は「馬」ではなく「レース」で数えるのが安全（同じレースの馬は独立でない）。1年分の JRA 平地（約 3,000 レース）なら isotonic も使えるが、競馬場×距離などで層別すると 1,000 レースを割る層が出るので、層別校正は Platt（温度）に限る。
- **校正データは時系列で分ける**: 学習期間 → 校正期間 → 評価期間。論文がランダム標本で分けているのを真似ない。

## 関連ノート

- [Platt 1999](./1999-platt-probabilistic-outputs-svm.md): 比較した校正法の1つの原典。ベイズ的目標値もここから。
- [Zadrozny 2002](./2002-zadrozny-isotonic-multiclass-calibration.md): もう1つの校正法（PAV）の原典。多クラスへの拡張も。
- [Guo 2017](./2017-guo-calibration-modern-nn.md): 本論文の「ニューラルネットはよく校正されている」が深層ネットでは崩れたことを示した後継。
- [Ke 2017](./2017-ke-lightgbm.md): keiba-ai で使う LightGBM。本論文のブースティング木の現代版。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 賭けでは正解率より校正でモデルを選ぶべきという主張。本論文の校正の議論を賭けに適用。
- [Murphy 1973](./1973-murphy-brier-decomposition.md): 二乗誤差を校正（信頼性）と分解能に分ける。校正で何が改善したかの切り分けに使う。
- [Lessmann 2010](./2010-lessmann-random-forest-horserace.md): 競馬にランダムフォレストを使った研究。RF の確率の歪みが効く応用先。

## 検索語

確率校正, キャリブレーション, Platt スケーリング, isotonic 回帰, 単調回帰, 信頼性図, S字の歪み, 最大マージン法, ブースティング, 勾配ブースティング, ランダムフォレスト, バギング, ナイーブベイズ, 校正データの量, 学習曲線, 二乗誤差, 対数損失, probability calibration, Platt scaling, isotonic regression, PAV, reliability diagram, sigmoid distortion, max margin methods, boosted trees, boosted stumps, random forests, bagged trees, naive Bayes, neural nets, logistic regression, calibration set size, learning curve, squared error, log loss, ICML 2005

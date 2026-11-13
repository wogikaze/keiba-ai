---
title: LightGBM: A Highly Efficient Gradient Boosting Decision Tree
authors: Ke Guolin, Meng Qi, Finley Thomas, Wang Taifeng, Chen Wei, Ma Weidong, Ye Qiwei, Liu Tie-Yan
year: 2017
venue: Advances in Neural Information Processing Systems 30 (NIPS 2017)
url: https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree
doi:
topic: evaluation-and-features
tags: lightgbm, gbdt, goss, efb, gradient-boosting
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# LightGBM：勾配の大きい事例を残すサンプリング（GOSS）と排他的特徴の束ね（EFB）

> 一言で: ヒストグラム型 GBDT の計算量は「データ数 × 特徴数」に比例する。LightGBM はデータ側を GOSS（勾配の小さい事例を間引き、重みで補正）、特徴側を EFB（同時に非ゼロにならない疎な特徴を 1 本に束ねる）で減らし、精度をほぼ保ったまま 1 反復あたり最大 21 倍速くした。

NeurIPS 2017 の本文 9 ページを読んだ。証明と詳細設定は補足資料（未読）にある。

## 背景（1–2 節）

- 従来の GBDT 実装（XGBoost、pGBRT）は、特徴ごとに全事例を走査して全分割点の情報利得を計算する。計算量はデータ数と特徴数の両方に比例する (p.1)。
- ヒストグラム法（連続値を離散ビンに入れ、ビン単位で利得を計算）は既存の技法で、本論文はその上に GOSS と EFB を載せる (p.2–3, Algorithm 1)。
- AdaBoost のような事例重みに基づくサンプリングは、GBDT には事例重みが無いのでそのままは使えない (p.3)。
- 実験で使う葉単位成長（leaf-wise）も既存の手法として引用されているだけで、本論文の提案ではない (p.6)。

## アルゴリズム

### GOSS（Gradient-based One-Side Sampling, 3 節）

勾配の小さい事例はすでによく学習されている、という観察に基づく。ただし単に捨てるとデータ分布が変わるので、重みで補正する (p.3–4)。

1. 各事例の勾配の絶対値で降順に並べる。
2. 上位 $a\times100\%$ を全部残す（集合 A）。
3. 残り $(1-a)$ から $b\times100\%$ を無作為に抽出する（集合 B）。
4. 分割の分散利得を計算するとき、B の勾配和に $\frac{1-a}{b}$ を掛ける。

$$\tilde V_j(d)=\frac{1}{n}\left(\frac{(\sum_{A_l}g_i+\frac{1-a}{b}\sum_{B_l}g_i)^2}{n_l^j(d)}+\frac{(\sum_{A_r}g_i+\frac{1-a}{b}\sum_{B_r}g_i)^2}{n_r^j(d)}\right)$$

（p.4, 式 1。$g_i$ は負の勾配、$l, r$ は特徴 $j$ の閾値 $d$ で分けた左右）

定理 3.2 では、近似誤差 $|\tilde V_j(d)-V_j(d)|$ が分割がバランスしていれば $O(1/\sqrt n)$ で 0 に近づくこと、無作為抽出は $a=0$ の特殊ケースで、条件次第で GOSS のほうが良いことを示す (p.4–5)。

### EFB（Exclusive Feature Bundling, 4 節）

疎な高次元データでは、多くの特徴が同時に非ゼロにならない（排他的）。それらを 1 本に束ねれば、ヒストグラム構築の計算量が $O(\#data\times\#feature)$ から $O(\#data\times\#bundle)$ に下がる (p.5)。

1. 特徴を頂点、同時に非ゼロになる回数（衝突）を辺の重みとするグラフを作る。最小の束の数を求める問題はグラフ彩色に帰着でき NP 困難（定理 4.1）なので、貪欲法で近似する (p.5)。
2. 次数の降順に特徴を見て、衝突が閾値 K（最大衝突率 γ）以下なら既存の束に入れ、なければ新しい束を作る（Algorithm 3）。特徴が数百万あるときは、グラフを作らず非ゼロ数の順で並べる簡易版を使う (p.6)。
3. 束の中では、各特徴のビンにオフセットを足して値域が重ならないようにする。例えば特徴 A が [0,10)、B が [0,20) なら B に 10 を足して [10,30) とし、合わせて [0,30) の 1 特徴にする（Algorithm 4）(p.6)。

衝突を許すと精度は最大 $O([(1-\gamma)n]^{-2/3})$ だけ影響を受ける（補足資料の命題 2.1）(p.6)。実験では γ=0（衝突を許さない）(p.7–8)。

## 実験設定（5 節）

| データ | 事例数 | 特徴数 | 性質 | タスク / 指標 |
|---|---|---|---|---|
| Allstate | 12M | 4,228 | 疎 | 二値分類 / AUC |
| Flight Delay | 10M | 700 | 疎 | 二値分類 / AUC |
| LETOR (MSLR-WEB30K) | 2M | 136 | 密 | ランキング / NDCG@10 |
| KDD10 | 19M | 29M | 疎 | 二値分類 / AUC |
| KDD12 | 119M | 54M | 疎 | 二値分類 / AUC |

(p.7, Table 1)。比較対象は XGBoost の事前ソート版（xgb_exa）とヒストグラム版（xgb_his）、GOSS/EFB 無しの LightGBM（lgb_baseline）、同じ抽出率の確率的勾配ブースティング（SGB）。24 コア・256 GB、16 スレッド。GOSS は a=b=0.05（Allstate, KDD10, KDD12）または a=b=0.1（Flight Delay, LETOR）(p.6–7)。

## 結果

1 反復あたりの学習時間（秒）(p.7, Table 2)：

| データ | xgb_exa | xgb_his | lgb_baseline | EFB のみ | LightGBM |
|---|---|---|---|---|---|
| Allstate | 10.85 | 2.63 | 6.07 | 0.71 | 0.28 |
| Flight Delay | 5.94 | 1.05 | 1.39 | 0.27 | 0.22 |
| LETOR | 5.55 | 0.63 | 0.49 | 0.46 | 0.31 |
| KDD10 | 108.27 | OOM | 39.85 | 6.33 | 2.85 |
| KDD12 | 191.99 | OOM | 168.26 | 20.23 | 12.67 |

テスト精度 (p.7, Table 3)：LightGBM は lgb_baseline とほぼ同じ（例：LETOR NDCG@10 0.5277 → 0.5275、Flight Delay AUC 0.7847 → 0.7846）。SGB は一貫してやや低い（LETOR 0.5239）。

- lgb_baseline 比の高速化は Allstate 21 倍、Flight Delay 6 倍、LETOR 1.6 倍、KDD10 14 倍、KDD12 13 倍 (p.7)。
- **密な特徴だけの LETOR では EFB がほとんど効かない**（0.49 → 0.46 秒）。高速化の大半は疎な one-hot 特徴が多いデータで EFB から来ている (p.7, Table 2)。
- GOSS 単独ではデータの 10〜20% で約 2 倍。勾配計算と予測は全データで行うので、抽出率に比例した高速化にはならない (p.8)。
- 同じ抽出率で GOSS は SGB より常に NDCG@10 が高い（抽出率 0.1 で 0.5224 vs 0.5182、0.4 で 0.5296 vs 0.5267）(p.8, Table 4)。

## 批判的に読む

- 比較は **1 反復あたりの時間**。全アルゴリズムが同程度の反復数で収束するとして高速化率を出している (p.7)。総学習時間ではない。
- 精度は「固定反復数のうち最良のスコアの反復」で報告している (p.7)。テスト集合で最良反復を選んでいるなら、精度はわずかに楽観的（各手法に同じ条件なので比較には影響が小さい）。
- ハイパーパラメータは「速度と精度のバランス」で各手法を調整したとあり、詳細は補足資料 (p.7)。XGBoost 側の調整が十分かは本文から判断できない。
- 精度の差は小数第 3〜4 位の議論で、統計的な検定は無い（SGB と LightGBM に標準偏差の記載はある）。
- GOSS の a, b の選び方は今後の課題とされている (p.8)。

## keiba-ai での使い方

- **keiba-ai の特徴は密な数値が中心**（過去走のタイム指数、上がり、斤量、間隔など）なので、LETOR と同じく EFB の恩恵は小さいと予想される。速さの主因はヒストグラム法と葉単位成長。騎手 ID・調教師 ID・血統を one-hot にする場合は EFB が効く。ただし LightGBM はカテゴリ特徴をそのまま扱えるので、one-hot より `categorical_feature` を試す。
- **GOSS（`boosting=goss` / 新しい版では `data_sample_strategy=goss`）は確率較正に注意**：小勾配の事例を重みで補正するとはいえ、学習済みの事例の扱いが変わる。勝率を確率として使う場合は、GOSS 有無で検証期間の logloss と ECE を比べる（実験案）。
- **LETOR での実績**：LightGBM の lambdarank 目的関数は、レース＝クエリ、馬＝文書と見なせば着順予測にそのまま使える。ただし lambdarank の出力は確率ではないので、勝率が要る場面では softmax と温度スケーリング（[Guo 2017](./2017-guo-calibration-modern-nn.md)）などの後処理を挟む。
- **評価の作法**：本論文のように「テストで最良の反復」を選ぶとリークになる。keiba-ai では反復数（early stopping）を時系列の検証期間で決め、テスト期間には触れない。

## 関連ノート

- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md)：LambdaMART。LightGBM の lambdarank 目的関数の元になったランキング学習。
- [Fujisawa 2024](./2024-fujisawa-ranknet-condition-datasets.md)、[Chung 2024](./2024-chung-learning-to-rank-seoul.md)、[So 2025](./2025-so-learning-to-rank-kra-web-service.md)：競馬へのランキング学習の適用例。GBDT 系の比較対象として読む。
- [Borowski 2021](./2021-borowski-ml-flat-racing-poland.md)、[Khanh 2024](./2024-khanh-ensemble-automated-betting.md)：競馬で木系アンサンブルを使った研究。
- [Guo 2017](./2017-guo-calibration-modern-nn.md)：GBDT のスコアを確率として使う前の較正。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md)：モデル選択を精度でなく較正で行うべきという議論。early stopping の基準選びに関係。

## 検索語

LightGBM、勾配ブースティング、勾配ブースティング決定木、GBDT、gradient boosting decision tree、GOSS、gradient-based one-side sampling、EFB、exclusive feature bundling、排他的特徴の束ね、ヒストグラム法、histogram-based algorithm、葉単位成長、leaf-wise growth、XGBoost、確率的勾配ブースティング、SGB、stochastic gradient boosting、疎特徴、sparse feature、one-hot、グラフ彩色、LETOR、MSLR-WEB30K、NDCG、lambdarank、learning to rank、Microsoft Research

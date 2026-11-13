---
title: Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods
authors: Platt John C.
year: 1999
venue: Advances in Large Margin Classifiers (MIT Press) 61-74
url: https://www.semanticscholar.org/paper/Probabilistic-Outputs-for-Support-vector-Machines-Platt/42e5ed832d4310ce4378c44d05570439df28a393
doi:
topic: evaluation-and-features
tags: calibration, platt-scaling, svm, sigmoid, cross-validation, log-loss
verified: fulltext
importance: medium
source: downloaded
source_version: preprint
---

# SVM の出力にシグモイドを当てて確率にする（Platt scaling の原典）

> 追記（2026-11-13）: 原本は機械 OCR 済み（RapidOCR）。`library/1999-platt-probabilistic-outputs-svm/source.txt` で全文検索できる。OCR の誤認識が残るため、数値は PDF のページ画像で確認すること。本ノートの本文は OCR 前にページ画像を読んで書いたもの。

> 一言で: SVM の生のスコア $f$ を $P(y=1\mid f)=1/(1+\exp(Af+B))$ に通し、$A,B$ を**SVM の学習に使っていないデータ**で最尤推定すれば、正則化ロジスティック回帰並みの確率が得られる、と示した。過学習を防ぐためのベイズ的なラベル平滑化（目標値を 0/1 ではなく $1/(N_-+2)$, $(N_++1)/(N_++2)$ にする）も入っている。

原本は著者の 1999年3月26日付の原稿（書籍章の出版前版, 11ページ）。PDF のフォント符号化のため抽出テキストが文字化けしており、OCR 待ち。本ノートは PDF のページ画像を読んで要約したもので、ページ番号は原稿のページ番号。

## 問題設定

分類器の出力は、効用に基づく意思決定や他のモデルとの結合のために、較正された事後確率であるべきだ (p.1)。SVM の出力 $f(\mathbf x)=h(\mathbf x)+b$ は確率ではない。確率を出すには Wahba 流にロジット連結と正則化尤度でカーネル機械を直接学習する方法があるが（式(4)(5), p.2）、それではサポートベクターの疎性が失われる。そこで SVM はそのまま学習し、出力を確率に写す後処理を別に学習する (p.2)。

既存の代替案の欠点も整理している (pp.2–3)。

- Vapnik のコサイン展開: 評価ごとに線形方程式を解く必要があり、0–1 に収まる保証も単調性もない。
- クラス条件付き分布をガウスで当てる方法: 事後確率が $1/(1+\exp(af^2+bf+c))$ の形になり単調でなくなる。実際の SVM 出力の分布はガウスから遠い (Fig.1, p.4)。

## 手法

### なぜシグモイドか

UCI Adult データで線形 SVM の出力のクラス別ヒストグラムを描くと、マージン $f=\pm1$ で微分が不連続になり、マージンの間はほぼ指数分布に見える (p.3, Fig.1)。2つの指数分布にベイズ則を当てるとシグモイドになる。2パラメータ $A,B$ を識別的に（事後確率に直接）当てる点が、分散共通のガウスから1パラメータを出す Hastie & Tibshirani 方式との違い (p.3)。$A<0$ なら単調性が保証される (p.4)。ヒストグラムから計算した事後確率に、シグモイドはマージンの外まで非常によく合う (Fig.2, p.5)。

### アルゴリズム

1. 目標値 $t_i$ を作る。素朴には $t_i=(y_i+1)/2$（式(10), p.4）。
2. 交差エントロピー $-\sum_i t_i\log p_i+(1-t_i)\log(1-p_i)$, $p_i=1/(1+\exp(Af_i+B))$ を $A,B$ について最小化する（式(11)(12), p.4）。2パラメータなので最適化は何でもよいが、論文は Levenberg–Marquardt 系のモデル信頼領域法を使う。擬似コードは付録 (pp.9–) にある。
3. **シグモイドの学習データを SVM の学習データと分ける** (pp.5–6)。SVM の学習データ上の $f_i$ は偏っている。マージン上の点は $|f|=1$ ちょうどに張り付き、マージン違反の点もマージン側に引き寄せられる。線形 SVM なら偏りは小さいが、非線形 SVM では学習データでシグモイドを当てると「破滅的に偏った」当てはめになることがある (p.5)。対策は2つ。
   - ホールドアウト（典型的には学習データの 30%）でシグモイドを学習し、その後 SVM を全データで学習し直す (p.6)。
   - **3分割交差検証**: 3つの SVM をそれぞれ 2/3 で学習し、残り 1/3 の出力 $f_i$ を集めてシグモイドの学習データにする。ホールドアウトより大きな学習集合になり $A,B$ の分散が小さい。計算時間は SVM 1回の約 2.2 倍。論文の結果はすべてこの方式 (p.6)。
4. **ベイズ的目標値で正則化する** (p.6)。交差検証データでも、正例が少なく線形分離可能だと $A\to-\infty$ の急峻なシグモイドになる（Reuters の例）。そこで正例・負例の数 $N_+,N_-$ から、一様事前分布の MAP 推定として

$$t_+=\frac{N_++1}{N_++2},\qquad t_-=\frac{1}{N_-+2}$$

を 0/1 の代わりに使う（式(13)(14), p.6）。標本が増えると 0/1 に近づき、通常の最尤に戻る (p.7)。

## 実験設定と結果

3つのデータ（Reuters ニュース分類、UCI Adult、Web ページ分類）、線形・2次カーネル (Table 1, p.7)。正則化は各手法ごとにホールドアウトで決める。誤分類数は McNemar 検定、対数尤度は Wilcoxon 符号順位検定で比較 (pp.7–8)。

Table 2 (p.8) の抜粋。誤り数とテスト集合の $-\log p$ 合計で、どちらも小さいほど良い。

| タスク | 生 SVM 誤り | SVM+シグモイド 誤り | 正則化尤度 誤り | SVM+シグモイド $-\log p$ | 正則化尤度 $-\log p$ |
|---|---|---|---|---|---|
| Reuters 線形 | 1043 | 963 | 1060 | 3249 | 3301 |
| Adult 線形 | 2441 | 2442 | 2434 | 5323 | 5288 |
| Adult 2次 | 2626 | 2554 | 2610 | 5772 | 5827 |
| Web 線形 | 260 | 265 | 248 | 1121 | 958 |
| Web 2次 | 444 | 452 | 507 | 1767 | 2163 |

読み方 (p.8)。

- 閾値 0 は必ずしもベイズ最適ではない。事前比 $P(y=-1)/P(y=1)$ が 1 から遠い Reuters と Adult 2次では、シグモイドの $P=0.5$ を閾値にすると誤りが有意に減った（Adult 2次では $f=-0.1722$ に相当）。
- 確率の質は正則化尤度と「おおむね同等」。5タスク中3つでは正則化尤度のほうが有意に良い。Web 2次では SVM+シグモイドの合計対数尤度が良いが、Wilcoxon 検定では正則化尤度が勝つ（多くの点で後者が正確）。
- どちらも誤り率・対数尤度の両方で支配的ではない。

## 批判的に読む

- 確率の質の比較は対数尤度だけで、信頼性図や Brier スコアはない。「同等」の判断は粗い。
- シグモイドが妥当なのは、スコアの対数オッズが $f$ の1次関数で近似できるときだけ。歪んだ（非対称な）ずれには効かない。Niculescu-Mizil & Caruana (2005) は、ブースティングなど他の学習器ではシグモイドが合わず isotonic のほうが良い場合を示した。
- 交差検証で集めた出力は「3つの別々の SVM の出力」の混合で、最終的に全データで学習し直した SVM の出力分布とは少しずれる。論文はこの差を問題にしていない。
- 擬似コードは数値的に不安定な箇所があり、後に Lin, Lin & Weng (2007) が改良版を出した（本ノートの範囲外。書誌のみ確認）。

## keiba-ai での使い方

- **校正の学習データは必ず時系列で分ける**: Platt の核心は「スコアを作ったモデルの学習データで校正しない」こと。keiba-ai では、モデルの学習期間より後の検証期間でシグモイド（または温度）を当て、さらに後のテスト期間で評価する。3分割交差検証を真似てランダムに分けると、同じレースの馬が両側に入りリークする。分割はレース単位・日付単位。
- **2値のシグモイドは単勝確率にそのまま使えない**: 馬ごとに $P(\text{勝ち}\mid f)$ を当てるとレース内の和が 1 にならない。レース内で正規化するか、条件付きロジット型 $\exp(Af_i)/\sum_j\exp(Af_j)$（温度スケーリング）に置き換える。$B$ はレース内正規化で消えるので、実質的に1パラメータになる。仮説: 単勝では Platt（2値・正規化後）より温度スケーリングのほうが対数損失が小さい。
- **ベイズ的目標値の発想**: 頭数が多く勝ち馬が少ない（正例率が低い）条件、例えば特定の競馬場・距離のサブモデルでは、校正の当てはめが極端になりやすい。$t_+=(N_++1)/(N_++2)$ 型の平滑化か、$A$ に事前分布を置く正則化を入れる。
- **閾値の再設定**: 論文の「閾値 0 は最適とは限らない」は、競馬では「最も確率の高い馬を買う」ではなく「期待値 $p\times$オッズ $>1$ の馬を買う」閾値設計に当たる。校正が崩れているとこの閾値がずれるので、賭けの評価は校正後の確率で行う。

## 関連ノート

- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md): Platt scaling と isotonic を10種の学習器で比較。シグモイドが合う・合わない条件を示した後継。
- [Zadrozny 2002](./2002-zadrozny-isotonic-multiclass-calibration.md): isotonic 回帰による校正と多クラスへの拡張。Platt の対抗手法。
- [Guo 2017](./2017-guo-calibration-modern-nn.md): 温度スケーリング。Platt の多クラス・1パラメータ版にあたる。
- [Edelman 2007](./2007-edelman-svm-horserace-odds.md): 競馬に SVM を使った研究。SVM 出力を確率にする必要がある応用先。
- [Lessmann 2009](./2009-lessmann-svm-classification-horserace.md): 競馬の SVM 分類。同上。
- [Brier 1950](./1950-brier-verification-probability-forecasts.md): 校正の評価に使う二乗スコア。

## 検索語

Platt スケーリング, プラットスケーリング, シグモイド校正, 確率校正, 事後確率, サポートベクターマシン, SVM, ロジスティック回帰, 正則化尤度, 交差検証, ホールドアウト, ラベル平滑化, ベイズ目標値, 閾値, Platt scaling, sigmoid calibration, probability calibration, posterior probability, support vector machine, regularized likelihood, kernel logistic regression, cross-validation, hold-out set, Levenberg-Marquardt, model-trust, Bayesian targets, label smoothing, McNemar test, Wilcoxon signed rank, UCI Adult, Reuters

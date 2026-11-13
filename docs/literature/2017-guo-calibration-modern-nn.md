---
title: On Calibration of Modern Neural Networks
authors: Guo Chuan, Pleiss Geoff, Sun Yu, Weinberger Kilian Q.
year: 2017
venue: Proceedings of the 34th International Conference on Machine Learning (PMLR 70) 1321-1330
url: https://proceedings.mlr.press/v70/guo17a.html
doi:
topic: evaluation-and-features
tags: calibration, temperature-scaling, platt-scaling, ece, neural-network
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 現代のニューラルネットは過信する：温度スケーリングによる確率の較正

> 一言で: 深く広い・BatchNorm を使う・weight decay が弱い現代の NN は、精度が上がる一方で予測確率が実際の正解率より高くなる（過信）。検証集合で温度 $T$ を 1 つ学習してロジットを割るだけの温度スケーリングが、画像分類ではヒストグラム法・等張回帰・BBQ・ベクトル/行列スケーリングより ECE を下げた。

PMLR 版本文 10 ページ（付録 S1–S4 は別ファイルで未読）を読んだ。

## 問題と定義（2 節）

予測クラス $\hat Y$ とその確信度 $\hat P$ について、完全な較正を $P(\hat Y=Y \mid \hat P=p)=p\ \forall p$ と定義する (p.2, 式 1)。

- **信頼性図（reliability diagram）**：確信度を M 個の等幅ビンに分け、各ビンの正解率を確信度に対してプロットする。対角線からのずれが誤較正 (p.2)。
- **ECE**：$\mathrm{ECE}=\sum_{m=1}^{M}\frac{|B_m|}{n}\left|\mathrm{acc}(B_m)-\mathrm{conf}(B_m)\right|$。ビンごとの差の重み付き平均。本文の主指標で、M=15 (p.3, 式 3; p.6 Table 1)。
- **MCE**：ビンごとの差の最大値。高リスク用途向け (p.3, 式 5)。
- **NLL**：交差エントロピー。期待値では真の条件付き分布で最小になるので、間接的に較正を測る (p.3, 式 6)。

注意点として、ここでの較正は **予測クラスの確信度（top-1）** についての定義で、全クラスの確率ベクトルの較正ではない。

## 何が誤較正を生むか（3 節）

CIFAR-100 の ResNet で、因果は主張できないとしつつ次の関係を観察した (p.3–4, Fig.2)。

| 要因 | 観察 |
|---|---|
| 深さ・幅 | 誤差は下がるが ECE は大きく上がる |
| Batch Normalization | 6 層 ConvNet で、精度はわずかに上がるが ECE は悪化。学習率などを変えても同じ |
| weight decay | 減らすと ECE が悪化。精度が最良になる点を過ぎて正則化を強めても、較正は改善し続ける |

もっとも示唆的なのは **NLL への過学習** (p.4, Fig.3)。110 層 ResNet（CIFAR-100）で学習率を下げた 250 エポック以降、テスト NLL は上がり続けるのにテスト誤差は 29% から 27% に下がる。

> the network learns better classification accuracy at the expense of well-modeled probabilities. (p.4)

つまり大きなモデルでは過学習が 0/1 誤差ではなく確率の誤差として現れる。早期終了を精度で決めると、確率は悪い点で止まりうる。

## 較正手法（4 節）

すべて学習後の後処理で、ネットワークの重みは固定し、ハイパーパラメータ調整と同じ検証集合を使う。訓練・検証・テストが同じ分布から来ることを前提にする (p.4)。

| 手法 | 中身 | パラメータ数 |
|---|---|---|
| ヒストグラム法 | 確信度をビンに分け、各ビンの正例率を出力 (Zadrozny & Elkan 2001) | M |
| 等張回帰 | 単調な区分定数関数をビン境界ごと最適化 | 可変 |
| BBQ | ビン分けの全候補をベイズ平均 (Naeini et al. 2015) | 可変 |
| Platt スケーリング | ロジットにロジスティック回帰 $\sigma(az+b)$ | 2 |
| 行列スケーリング | $\mathrm{softmax}(Wz+b)$ | $K^2+K$ |
| ベクトルスケーリング | 上で $W$ を対角に制限 | $2K$ |
| **温度スケーリング** | $\hat q=\max_k \mathrm{softmax}(z/T)^{(k)}$、$T$ を検証 NLL で最適化 | 1 |

温度スケーリングは softmax の最大値の位置を変えないので、**分類精度は変わらない** (p.6)。T>1 で分布は平らになり、T→∞ で一様 1/K に近づく。多クラスのビン法は one-vs-all で K 個作って正規化するため、予測クラスが変わり精度を落としうる (p.6, 8)。

## 結果（5 節）

データは画像 6 種（Birds, Cars, ImageNet, CIFAR-10/100, SVHN）と文書 4 種（20 News, Reuters, SST 二値 / 5 段階）。ECE（%、M=15）の一部 (p.6, Table 1)：

| データ / モデル | 未較正 | ヒスト | 等張 | BBQ | 温度 | ベクトル | 行列 |
|---|---|---|---|---|---|---|---|
| CIFAR-100 / ResNet 110 | 16.53 | 2.66 | 4.99 | 5.46 | 1.26 | 1.32 | 25.49 |
| CIFAR-100 / LeNet 5 | 4.85 | 6.48 | 2.35 | 3.77 | 2.02 | 2.09 | 13.24 |
| ImageNet / ResNet 152 | 5.48 | 4.36 | 4.77 | 3.56 | 1.86 | 2.23 | — |
| Birds / ResNet 50 | 9.19 | 4.34 | 5.22 | 4.12 | 1.85 | 3.0 | 21.13 |
| Cars / ResNet 50 | 4.3 | 1.74 | 4.29 | 1.84 | 2.35 | 2.37 | 10.5 |
| 20 News / DAN 3 | 8.02 | 3.6 | 5.52 | 4.98 | 4.11 | 4.61 | 9.1 |
| Reuters / DAN 3 | 0.85 | 1.75 | 1.15 | 0.97 | 0.91 | 0.66 | 1.58 |
| SST 5 段階 / TreeLSTM | 6.71 | 2.09 | 1.65 | 2.61 | 2.56 | 2.98 | 2.39 |

- 多くのデータで未較正 ECE は 4〜10% (p.7)。古い LeNet は ResNet より較正が良い（Fig.1, Table 1）。
- 画像では温度スケーリングが最良。NLP では他手法と同程度 (p.7)。
- ベクトルスケーリングの学習結果はほぼ定数ベクトルになり、温度スケーリングと同じ解に落ちる。著者は「誤較正は本質的に低次元」とまとめる (p.7)。
- 行列スケーリングはクラス数が数百あると過学習し、ImageNet（1000 クラス）では収束しない (p.7–8)。
- ビン法の中では最も単純なヒストグラム法が等張回帰や BBQ より良いことが多い (p.8)。
- 計算時間は温度スケーリングが圧倒的に速い（1 次元凸最適化、共役勾配で約 10 反復）(p.8)。

## 批判的に読む

- **top-1 の確信度だけを評価**している。競馬のように全候補の確率（勝率ベクトル）を使って期待値を計算する用途では、クラスごと（馬ごと）の較正が問題になり、top-1 の ECE では足りない。
- ECE はビン数とビン分けに依存し、推定量としてバイアスがある（著者も Reuters の結果について「分割やビン分けの影響の可能性」に触れる, p.7）。比較では NLL や Brier も併記すべき。
- 検証集合とテスト集合が同分布という前提。時間で分布が変わるデータ（市場の変化、馬場の季節性）では、過去の検証集合で学んだ T が将来も最適とは限らない。
- 対象は「クラス数が固定の分類」。レースごとに出走頭数も顔ぶれも変わる問題とは構造が違う。

## keiba-ai での使い方

- **条件付きロジット / softmax 型モデルの温度**：レース内 softmax $p_i=\exp(s_i/T)/\sum_j\exp(s_j/T)$ の T を、時系列で後ろにある検証期間の NLL で 1 つだけ学習する。順位（＝馬の並び）は変わらないので、着順予測の指標（NDCG 等）は変わらず確率だけが直る。これは Benter 型の「モデル確率と市場確率の結合」の前段に入れられる。
- **確率で買う判断をするなら必須**：期待値 = 確率 × オッズ で賭けるので、過信は期待値の過大評価に直結し、ロングショットを買いすぎる（推測）。LightGBM の lambdarank など、スコアが確率でないモデルでは特に後処理が要る。
- **早期終了の基準**：精度（的中率）ではなく検証 NLL で止める。本論文の Fig.3 が示すとおり、両者の最適点はずれる。
- **評価指標**：ECE（勝率を 15 ビン程度）と信頼性図を、レース単位の NLL・Brier と並べて出す。人気別（単勝オッズ帯別）の信頼性図にすれば、モデルの「穴馬への過信」と市場の favorite-longshot bias を同じ図で比べられる（実験案）。
- **実験案（仮説）**：温度スケーリングは T 1 つなので、オッズ帯や頭数で T を変える（グループ別 T）ほうが NLL が下がるかを検証する。本論文の「誤較正は低次元」という観察が競馬でも成り立つなら、改善は小さいはず。

## 関連ノート

- [Platt 1999](./1999-platt-probabilistic-outputs-svm.md)：Platt スケーリングの原典。温度スケーリングはその 1 パラメータ版。
- [Zadrozny 2002](./2002-zadrozny-isotonic-multiclass-calibration.md)：等張回帰と one-vs-all による多クラス較正。本論文の比較対象。
- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md)：2005 年時点では NN は較正が良いとした研究。本論文はそれが現代の NN では崩れたと示す。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md)：較正でモデルを選ぶと賭けの利益が上がると示した研究。較正の重要性を賭けの文脈で確認。
- [Gneiting 2007](./2007-gneiting-proper-scoring-rules.md)：NLL・Brier などの適正スコアリングルール。ECE が適正スコアでないことの背景。
- [Brier 1950](./1950-brier-verification-probability-forecasts.md)、[Murphy 1973](./1973-murphy-brier-decomposition.md)：Brier スコアと、その較正（reliability）成分への分解。
- [Torné 2021](./2021-torne-hong-kong-softmax-nn.md)：競馬の softmax NN。温度スケーリングをそのまま適用できる構造。

## 検索語

較正、キャリブレーション、確率較正、calibration、confidence calibration、温度スケーリング、temperature scaling、Platt スケーリング、Platt scaling、ベクトルスケーリング、行列スケーリング、ヒストグラムビニング、histogram binning、等張回帰、isotonic regression、BBQ、Bayesian Binning into Quantiles、ECE、expected calibration error、MCE、信頼性図、reliability diagram、過信、overconfidence、NLL、負の対数尤度、log loss、交差エントロピー、BatchNorm、weight decay、ResNet、softmax、早期終了

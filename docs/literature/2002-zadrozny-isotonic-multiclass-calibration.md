---
title: Transforming classifier scores into accurate multiclass probability estimates
authors: Zadrozny Bianca, Elkan Charles
year: 2002
venue: Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '02) 694-699
url: https://dl.acm.org/doi/10.1145/775047.775151
doi: 10.1145/775047.775151
topic: evaluation-and-features
tags: calibration, isotonic-regression, pav, multiclass, one-vs-rest, brier-score
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# 順位づけスコアを isotonic 回帰で確率に直し、多クラスへ広げる

> 一言で: 「スコアの順序は正しいが値は確率になっていない」分類器に対し、単調非減少という制約だけを置く isotonic 回帰（PAV アルゴリズム）で確率に写す方法を提案した。多クラスでは one-vs-rest の2値スコアを1つずつ校正してから正規化するのが、単純で十分に良いと示した。

原本は KDD 2002 の論文 (pp.694–699, 6ページ)。大学の講義ページに置かれた出版版の PDF から取得。

## 問題設定

多くの学習器は例を「クラスに属しそうな順」に並べるスコア $s(x)$ を出す。$s(x)>s(y)$ なら $P(c\mid x)>P(c\mid y)$ が成り立つが、値そのものは確率として当てにならない (p.694)。コスト依存の意思決定や他の情報源との結合には、正確な確率が要る。

校正の定義は、スコア $s$ を付けた例のうち実際にクラスに属する割合が、例数を増やすと $s$ に収束すること (p.694)。信頼性図 (reliability diagram) で見ると (Fig.1–2, p.695)、

- ナイーブベイズのスコアは極端に寄りすぎる。属性の独立仮定が破れるため、0 付近では真の確率より小さく、1 付近では大きい。ただし順序づけは良い。
- SVM のスコア（超平面からの距離を [0,1] に再尺度化）は単調だが校正されていない。

## 既存手法の整理と提案

| 手法 | 仮定 | 問題点 |
|---|---|---|
| シグモイド (Platt) | スコアと確率の関係がシグモイド形 | ナイーブベイズのスコアには形が合わない (Fig.4, p.696) |
| ビニング | なし。等頻度の $b$ 個のビンで経験確率 | $b$ を交差検証で決める必要。小標本・不均衡では難しい。境界の位置が恣意的 (p.696) |
| **isotonic 回帰 (PAV)** | 写像が単調非減少であること（＝順序づけが正しい） | 学習データにやや過学習する (p.697) |

### PAV アルゴリズム (p.696)

1. 例をスコア順に並べ、目標値 $g(x_i)$ を負例 0・正例 1 とする。
2. 隣り合う $g(x_{i-1})>g(x_i)$ の組（pair-adjacent violators）を見つけたら、2つを平均値で置き換える。
3. 全体が非減少になるまで繰り返す。結果は区間ごとに一定値の階段関数で、計算量は $O(n)$。
4. テスト例は、そのスコアが入る区間の値を確率とする。

完全に順序づけできるスコアなら負例 0・正例 1 のまま、順序の情報がまったくないなら全体の正例率の定数になる。著者はこれを、**順序づけの悪い領域ほど広いビンを自動で作るビニング**と解釈している (p.696)。

## 多クラスへの拡張 (pp.696–697)

$k$ クラスの写像を直接学習すると $(k-1)$ 次元から $(k-1)$ 次元への関数になり、形の制約が置きにくく次元の呪いも効く。そこで、

1. 多クラス問題を符号行列 $M\in\lbrace -1,0,+1\rbrace ^{k\times l}$ で $l$ 個の2値問題に分ける（one-vs-rest, all-pairs, ECOC の一般化）。
2. 2値分類器のスコアをそれぞれ PAV で校正する。
3. 2値の確率 $r_b(x)$ から、$\sum_i P(c_i\mid x)=1$ を満たす多クラス確率を求める。$l>k-1$ では解が一般に存在しない過剰制約問題なので、近似する。非負制約つき最小二乗 (Kong & Dietterich) か、対数損失を最小化する coupling (Hastie & Tibshirani の拡張) を使う。one-vs-rest では単純な**正規化**（和で割る）も使える。

## 実験

評価は主に MSE（Brier スコア, 多クラスでは全クラスの二乗誤差の和）。著者は DeGroot & Fienberg に従い、MSE が校正と refinement に分解できること、校正された分類器どうしなら MSE が小さいほうが refinement が高いことを述べ、MSE を主指標にする理由としている (p.697)。ただし本来は利益などの領域固有指標で評価すべきだ、とも書く。

### 2値（KDD-98 寄付、TIC 保険、Adult 所得）

| データ・学習器 | 生スコア MSE（テスト） | シグモイド | PAV | 出典 |
|---|---|---|---|---|
| KDD-98, NB | 0.10111 | 0.09533 | **0.09528** | Table 1, p.697 |
| TIC, NB | 0.13551 | 0.10905 | **0.10818** | Table 2, p.698 |
| TIC, SVM | 0.11889 | **0.11122** | 0.11200 | Table 2, p.698 |
| Adult, NB | 0.25198 | 0.21515 | **0.20452** | Table 3, p.698 |
| Adult, SVM | 0.28684 | 0.20962 | **0.20924** | Table 3, p.698 |

- KDD-98 では校正で寄付依頼の利益も改善した。テストで NB $9,531 → シグモイド $14,120 → PAV $14,447 (Table 1, p.697)。依頼方針は「$P(\text{寄付}\mid x)\cdot y(x)$ が郵送費を超える人に送る」。確率の改善がそのまま意思決定の利益に出た例。
- Adult の SVM では、写像の形が明確なシグモイドなのに PAV がわずかに勝った (p.698)。
- 校正で誤り率が下がることも上がることもある。NB では閾値 0.5 が生スコアに合っていなかったので校正で誤りが減る（テスト 0.17321 → 0.14831）。SVM では元の閾値が最適だったので、校正で refinement が少し落ちて誤り率がわずかに上がる（0.14968 → 0.15113） (Table 3, p.698)。
- ビニング（ビン数 5〜50）との比較: KDD-98 では最良設定のビニングと同程度、TIC ではわずかに劣り、Adult では常に PAV が勝った (pp.697–698)。

### 多クラス（Pendigits 10クラス、20 Newsgroups 20クラス）

one-vs-rest のみ。Pendigits (Table 4, p.699) では、NB の正規化 MSE 0.0326 が PAV 後 0.0241、ブースト NB では 0.0163 → 0.0150。校正後は3つの結合法（正規化・最小二乗・coupling）の差が小さくなった。20 Newsgroups (Table 5, p.699, 80/20 分割を10回) でも、最小 MSE は「PAV で校正 → 正規化」の 0.01220 だった。結論として、one-vs-rest には最も単純な正規化を推奨している (p.699)。

## 批判的に読む

- **校正関数を分類器と同じ学習データで学習している**。著者は「これらのデータでは学習器が過学習しないので」と断っている (p.697)。ナイーブベイズや線形 SVM ならまだしも、勾配ブースティングのように学習データにほぼ完全に当てはまる学習器では、この手順は使えない。Platt (1999) の交差検証の考えと組み合わせる必要がある。
- PAV は階段関数なので、確率が同じ値に固まる（同順位が増える）。同じ区間に入った馬は確率が完全に等しくなり、順位づけの情報を一部失う。表では「学習データにやや過学習」と自ら認めている (p.697)。
- 有意差検定はない。表の差は小数第3〜4位のものが多い。
- 多クラスの実験は one-vs-rest だけで、他の符号行列での比較は今後の課題とされている (p.699)。

## keiba-ai での使い方

- **単勝確率の校正に「one-vs-rest + PAV + レース内正規化」を当てる**: 馬ごとの勝ち/負けを2値とみなし、モデルスコアを PAV で確率に写し、レース内で和が 1 になるよう割る。論文の多クラス手順をレースに置き換えたもの。ただしレースごとにクラス数（頭数）が変わり、クラスに意味のある番号もないので、正確には多クラスではなく「可変個の選択肢」である。仮説: 頭数で層別せずに PAV を当てると、少頭数レースの確率が過小になる。頭数を入れたスコア（例: $\text{logit}+\log(\text{頭数})$ の補正）を作ってから PAV を当てると改善する。
- **校正データの分け方**: 本論文の「同じデータで校正」は keiba-ai では不可。LightGBM の学習期間とは別の、後の期間で PAV を学習する。
- **期待値ベースの購入判断が校正で変わることの確認**: KDD-98 の「確率 × 金額 > コスト」は、競馬の「確率 × オッズ > 1」と同じ構造。校正前後で購入対象・回収率がどう変わるかを、Table 1 のように並べて記録する。
- **PAV とシグモイド・温度スケーリングの比較を Brier と log loss の両方で**: PAV は階段関数のため、学習データにない極端なスコアで確率 0 や 1 を出し得る。log loss では致命的なので、端の区間をクリップするか、平滑化した isotonic を使う。

## 関連ノート

- [Platt 1999](./1999-platt-probabilistic-outputs-svm.md): 比較対象のシグモイド校正。校正データを分ける考えは Platt から借りるべき。
- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md): Platt と isotonic を多数の学習器で比較し、データが少ないと isotonic が過学習することを示した後継。
- [Guo 2017](./2017-guo-calibration-modern-nn.md): 多クラスの温度スケーリング。本論文の「多クラス写像は形が決めにくい」に対する1パラメータの解。
- [Brier 1950](./1950-brier-verification-probability-forecasts.md): 評価に使った MSE（Brier スコア）の原典。
- [Murphy 1973](./1973-murphy-brier-decomposition.md): MSE を校正と分解能に分ける。本論文が引く DeGroot & Fienberg の分解と同系統。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 賭けにおける校正の重要性。KDD-98 の利益改善と同じ論点。

## 検索語

isotonic 回帰, アイソトニック回帰, 単調回帰, PAV, プール隣接違反, 確率校正, キャリブレーション, 多クラス確率, one-vs-rest, 一対他, 総当たり, 誤り訂正出力符号, 正規化, ナイーブベイズ, SVM, ビニング, 信頼性図, Brier スコア, isotonic regression, pair-adjacent violators, pool adjacent violators, PAVA, calibration, multiclass probability estimates, one-against-all, all-pairs, ECOC, code matrix, coupling, least squares, normalization, naive Bayes, binning, reliability diagram, KDD-98, COIL 2000, TIC, Adult, Pendigits, 20 Newsgroups

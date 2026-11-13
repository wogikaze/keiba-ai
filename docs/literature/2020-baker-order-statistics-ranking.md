---
title: New order-statistics-based ranking models and faster computation of outcome probabilities
authors: Baker Rose D.
year: 2020
venue: IMA Journal of Management Mathematics 31(1) 33-48
url: https://academic.oup.com/imaman/article-abstract/31/1/33/5308454
doi: 10.1093/imaman/dpz001
topic: probability-models
tags: order-statistics, ranking-model, gamma-model, thurstone, plackett-luce, computation, numerical-integration, pareto, exponentiated-exponential
verified: fulltext
importance: medium
source: downloaded
source_version: accepted-manuscript
---

# 順序統計量に基づく新しい順位モデル（指数化指数分布・Lomax）と着順確率の高速計算

原本は Salford 大学リポジトリ（USIR eprint 49762）の著者最終稿（2019年1月14日付、31ページ）を Internet Archive の保存版から取得した。ページ番号は PDF のページ（1ページ目はリポジトリの表紙）。出版版とは組版とページが異なる。

> 一言で: 着順確率 $p_{12\cdots n}$ は「反復積分」なので、後ろの競技者から生存関数を1本ずつ積分していけば $n$ に対して線形の手間で計算できる。これで gamma・Thurstone–Mosteller と新しい2族（指数化指数 EE、Lomax）を多人数データに当てはめられるようになり、ゴルフとテニスでは Plackett–Luce より当てはまりが良かった。

## 原本で確認・訂正した点

旧ノートは要旨だけに基づいていた。原本を読んで次を確認・訂正した。

- 新しい族の一方は「Pareto」と要旨にあるが、実体は一般化 Pareto の特殊形 **Lomax** 分布 $S(x)=(1+\alpha x)^{-\nu}$ である (p.10)。
- gamma モデルの由来は Henery (1983) と Stern (1990)。旧ノートの関連ノート欄で Henery を「正規」だけに結びつけていたが、本論文が対象にする gamma モデルは Henery 1983 である (p.8)。正規版は Thurstone–Mosteller V 型として扱われる。
- 実証はゴルフ（男子メジャー）と女子テニスのみで、**競馬データの適用はない**。競馬は Stern (1990a) の結果の引用として出てくるだけ (p.9)。
- 計算速度の具体値: $n=20$ で 1.4 ミリ秒、$n=80$ で 157 ミリ秒（デスクトップ PC）(p.19)。

## モデル

競技者 $i$ の「タイム」$x_i$ が密度 $f_i(x_i\mid\alpha_i)$ に従い、小さい順に着順が決まる。着順 $1,2,\dots,n$ の確率は

$$p_{12\cdots n}=\int_0^\infty f_1(x_1)\,dx_1\int_{x_1}^\infty f_2(x_2)\,dx_2\cdots\int_{x_{n-1}}^\infty f_n(x_n)\,dx_n$$

(p.6, 式1)。時間軸の単調変換で確率は変わらないので、指数・Weibull・Gumbel は同じ確率を与え、強さの比だけが効く (p.6)。共変量は $\alpha_i\propto\exp(\lambda^\top z_i)$ で入れられる (p.6)。

| 分布 | モデル | 備考 |
|---|---|---|
| 指数 | Plackett–Luce (PL) | 閉じた式 (p.6) |
| gamma（形状 $\beta$） | Henery 1983 / Stern 1990 | $\beta=1$ で PL、$\beta\to\infty$ で対数正規 = TM (p.7-8) |
| 正規 | Thurstone–Mosteller V 型 (TM) | $n=2$ なら $\Phi(\ln(\alpha_1/\alpha_2)/\sqrt2)$ (p.9) |
| 指数化指数 (EE) | 新 | $F(x)=(1-e^{-\alpha x})^\beta$、$\beta=1$ で PL (p.10) |
| Lomax | 新 | $S(x)=(1+\alpha x)^{-\nu}$、指数より裾が重い (p.10) |

$\beta>1$ が効く理由の説明が競馬に直結する。$y=x^\beta$ と書き直すと「成績が悪い側の裾」が指数分布より長くなり、「普段強い馬がときどき大きく負ける」ことを表せる。Stern (1990a) は競馬で $\beta=2$ が PL より当てはまると報告した (p.9)。

2人の場合、EE モデルは $\beta=2$ で $p_{12}=r^2(2r+7)/\{(r+1)(r+2)(2r+1)\}$（$r=\alpha_1/\alpha_2$）と閉じた式になる (p.11)。

## アルゴリズム（$n$ 人の着順確率）

1. $S_n(x)=\int_x^\infty f_n(u)\,du$ を全格子点で計算する。
2. $i=n-1$ から 1 まで $S_i(x)=\int_x^\infty f_i(u)S_{i+1}(u)\,du$ を計算する。
3. $p_{12\cdots n}=S_1(0)$ (p.14)。

実装上の工夫:

- 変数変換で積分区間を $[0,1]$ に写し、両端で密度が 0 になるようにする（gamma・EE は $x=-\ln(1-z^\gamma)/\alpha_0$、$\alpha_0$ は最小の $\alpha_i$ の半分、$\gamma=3/\beta$）(p.16, 18)。
- 台形則で $O(h^2)$、格子を倍にして Richardson 外挿で $O(h^4)$。2回目の外挿は不安定なので推奨しない (p.15, 18)。
- 格子数の経験則 $N=200\exp(n/18)$ で $n\approx70$〜80 まで許容誤差 (p.19)。手間は $Nn$。
- 下位が順位なし（ゴルフの予選落ち）は $\prod S_i(x)$ を掛けるだけ (p.20-21)。
- 同着は反復積分にならないので、同着した $\alpha_i$ を平均で置き換える Efron (1977) 型の近似を使う (p.22)。
- 対数尤度の微分は「$\beta\to\beta+1$ にした積分」で書け、$n$ 個の偏微分に $n+1$ 回の積分が要る (p.21)。

Monte Carlo との比較（Figure 1, p.4）では、多次元積分は約10人まで Monte Carlo より速いが、どちらも多人数では実用にならず、新手法だけが実行可能とされる。ただし著者自身、ブックメーカーや賭け手が必要とするのは「勝つ」「上位10位に入る」のような確率の大きい事象で、それなら Monte Carlo で十分だと断っている (p.13)。

## 実証

| データ | 規模 | 結果 |
|---|---|---|
| 男子ゴルフ 4大メジャー（Baker & McHale 2015 の再分析） | 279試合、822人、1試合最大46人 (p.24) | 3族とも PL より有意に良い。Lomax は最大で対数尤度 +28（$\chi^2=56$）。EE（$\beta$ 大）が最良、gamma も良い (p.25-26) |
| 女子テニス 4大大会 1968–2016 | 20,552試合、85,132セット (p.27) | TM が最良で Bradley–Terry から対数尤度 +65.5。ただし1セットあたりの予測確率の改善は約 0.0004 (p.27) |

テニスの結果について著者は「ペア比較モデルはどれも似た振る舞いをする」という Stern (1992) の結論を裏づけるとしている (p.27)。Lomax は両データで振るわなかった (p.28)。

## 批判的に読む

- **評価は当てはまり（対数尤度）だけ**。ホールドアウトでの予測精度や時系列分割の検証はない。著者も「本当に重要なのは予測順位の正確さ」と認めつつ、最良当てはまりのモデルが最良予測を与えるはずという一般論で済ませている (p.28)。
- 大量パラメータの最尤推定で、プロファイル尤度の曲線が粗い（計算が重く「時間単位」かかった）(p.24-25)。
- テニスでは統計的に有意でも実用上の差はごく小さい。データ量が多いと有意性はすぐ出るので、効果量で判断する必要がある。
- 競馬での検証はない。競馬で $\beta>1$ が良いという根拠は Stern (1990a) の引用のみ。

## keiba-ai での使い方

- **3連単・3連複の確率付け**: 勝率モデル（ロジットなど）から $\alpha_i$ を作り、gamma または EE の着順確率で組み合わせ確率を出す。JRA の最大18頭なら1組み合わせ 1.4 ミリ秒前後と見込め（$n=20$ の値、p.19）、上位3頭だけの確率なら下位を「順位なし」扱いにして計算をさらに軽くできる (p.20-21)。
- **仮説**: 3着以内の確率の校正（[Benter 2019](./2019-benter-model.md) の $\gamma,\delta$ 補正で扱われる「下位ほどランダム」）は、形状 $\beta>1$ の gamma/EE で近い効果が出る。検証は時系列分割したテストで、Harville（PL）・Benter 補正・gamma($\beta$ 推定)・EE の4つを3連単的中組の負の対数尤度で比べる。
- 実装の優先度は低め。まず PL + discount 補正で残差を確認し、2着・3着の校正が悪いときにこの計算法を使う。数値積分の実装方針（変数変換 + 台形則 + Richardson 1回）はそのまま流用できる。

## 関連ノート

- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規の順序統計量モデル。本論文の TM モデルに相当。
- [Stern 1990](./1990-stern-gamma-permutations.md): gamma 順位モデルと競馬での $\beta=2$ の当てはまり。本論文が高速化の対象とする。
- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 指数（Gumbel）分布に対応する PL モデル。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 勝率だけから作る PL 型の着順確率。
- [Lo 2008](./2008-lo-ordering-probabilities-approximation.md): Henery・Stern を閉じた式で近似する別の道。数値積分との比較対象。
- [Glickman 2015](./2015-glickman-stochastic-rank-ordered-logit.md): 順位ロジットの動的拡張。
- [Guiver 2009](./2009-guiver-bayesian-plackett-luce.md): Gumbel と PL の対応（Yellott）。
- [Benter 2019](./2019-benter-model.md): 下位着順の discount 補正。gamma/EE の代替。

## 検索語

順序統計量, 順位モデル, 着順確率, 反復積分, 台形則, Richardson 外挿, Thurstone モデル, Thurstone–Mosteller, Henery gamma モデル, 指数化指数分布, 一般化指数分布, Lomax 分布, Pareto 分布, 数値積分, 高速計算, Plackett-Luce, Bradley-Terry, 予選落ち, 同着, ゴルフ, 女子テニス, order statistics, ranking model, outcome probabilities, iterated integral, exponentiated exponential distribution, Lomax, generalized Pareto, numerical integration, Richardson extrapolation, Thurstone-Mosteller type V, Henery gamma model, Baker McHale, golf majors, women's tennis

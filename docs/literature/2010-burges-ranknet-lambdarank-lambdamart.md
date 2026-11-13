---
title: From RankNet to LambdaRank to LambdaMART: An Overview
authors: Burges Christopher J.C.
year: 2010
venue: Microsoft Research Technical Report MSR-TR-2010-82
url: https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/
doi:
topic: evaluation-and-features
tags: learning-to-rank, lambdamart, lambdarank, ranknet, ndcg, err, gradient-boosting, pairwise
verified: fulltext
importance: medium
source: downloaded
source_version: working-paper
---

# RankNet → LambdaRank → LambdaMART：ペア比較の勾配を NDCG の変化量で重み付けし、ブースティング木で学習する

> 一言で: RankNet はクエリ内の2文書のスコア差をシグモイドで「i が j より上」の確率にし、交差エントロピーで学習する。LambdaRank は、コストを書かずに勾配 $\lambda$ だけを定め、RankNet の勾配に「2つを入れ替えたときの NDCG の変化 $|\Delta\text{NDCG}|$」を掛ける。LambdaMART はその $\lambda$ を勾配ブースティング木 (MART) の擬似残差として使う。3つを1本の流れで自己完結的に説明した技術報告。

原本は Microsoft Research の技術報告 MSR-TR-2010-82 (19ページ)。著者自身が述べるとおり実験結果も他手法との比較もない解説文書である (p.2)。

## RankNet (pp.2–5)

クエリごとにデータを分け、ラベルの違う文書の組 $(U_i,U_j)$ を作る。モデルのスコア $s_i=f(x_i)$ から

$$P_{ij}=P(U_i\triangleright U_j)=\frac{1}{1+e^{-\sigma(s_i-s_j)}}$$

とし（$\triangleright$ は「上に並ぶべき」）、目標 $\bar P_{ij}=\frac12(1+S_{ij})$（$S_{ij}\in\lbrace 0,\pm1\rbrace $）との交差エントロピー

$$C=\tfrac12(1-S_{ij})\sigma(s_i-s_j)+\log\bigl(1+e^{-\sigma(s_i-s_j)}\bigr)$$

を最小化する (p.3)。性質:

- $s_i=s_j$ でもコストは $\log 2$ なので、ラベルの違う文書を引き離すマージンが組み込まれている。順位が逆なら漸近的に線形、正しければ 0 に近づく (p.3)。
- ラベルの値そのものは不要で、ペアの選好の集合 $I$ さえあればよい。選好が非推移的（A>B, B>C, C>A）でもかまわない (p.4)。

**因数分解による高速化** (pp.4–5): 勾配は $\lambda_{ij}=\partial C/\partial s_i=\sigma\bigl[\frac12(1-S_{ij})-\frac{1}{1+e^{\sigma(s_i-s_j)}}\bigr]$ と、$\partial s/\partial w$ の積に分解できる。文書ごとに $\lambda_i=\sum_{j:(i,j)\in I}\lambda_{ij}-\sum_{j:(j,i)\in I}\lambda_{ji}$ を先に集計してから重みを1回更新すれば、学習時間はクエリあたり文書数の2乗からほぼ線形に下がる (p.5)。$\lambda_i$ は「その文書をどちら向きにどれだけ動かしたいか」を表す矢印（力）と解釈できる。

## 評価指標 (pp.5–6)

$\text{DCG@}T=\sum_{i=1}^{T}\frac{2^{l_i}-1}{\log(1+i)}$、$\text{NDCG@}T=\text{DCG@}T/\max\text{DCG@}T$（ラベル $l_i\in\lbrace 0,\dots,4\rbrace $）(p.5)。ERR はカスケード型（上から読んで満足したら止まる）利用者モデルに基づく指標で、入れ替えによる変化 $\Delta\text{ERR}$ は2乗の計算量で求められる (pp.5–6)。これらの指標はスコアの関数として至るところ平坦か不連続で、勾配が 0 か定義されない (p.5)。

## LambdaRank (pp.7–11)

RankNet はペアの誤りの数（の滑らかな凸近似）を減らすが、上位を重視する NDCG とは合わない。Fig.1 (p.7) の例では、ペア誤りを 13 から 11 に減らす変更が、上位の関連文書を3つ下げてしまい NDCG では悪化する。

> The key observation of LambdaRank is thus that in order to train a model, we don't need the costs themselves: we only need the gradients (p.8)

勾配を

$$\lambda_{ij}=\frac{-\sigma}{1+e^{\sigma(s_i-s_j)}}\,|\Delta\text{NDCG}_{ij}|$$

とする（式(6), p.8）。$|\Delta\text{NDCG}_{ij}|$ は、現在のスコアで並べたうえで $i$ と $j$ だけを入れ替えたときの NDCG の変化。MRR や MAP を最適化したければ、この変化量を差し替えるだけでよい (p.8)。

- **経験的な最適性の確認** (pp.9–10): 学習後の重みの各座標を少し動かして平均 NDCG が下がることを確かめる。鞍点の可能性を排除するため、ランダムな方向 $n$ 本に動かして全部で NDCG が下がることを確かめる片側モンテカルロ検定を使う。上昇方向の割合 $p\le0.01$ を信頼度 99% で言うには $n\ge459$ 方向が要る (p.10)。
- **$\lambda$ は本当に勾配か** (pp.10–11): ポアンカレの補題により、$\partial f_i/\partial x_j=\partial f_j/\partial x_i$ が必要十分条件。現在の並びを固定すれば「RankNet のコスト × $|\Delta\text{NDCG}|$」というコストが書けるが、並びはモデルに依存するので一般の式は複雑になる。

## MART と LambdaMART (pp.11–18)

MART（Friedman の勾配ブースティング）は回帰木の線形結合で、各木は擬似残差（コストのスコアに関する勾配）を最小二乗で当て、葉の値はニュートン法で決める。2値分類の MART（ロジスティック損失）の導出と、不均衡データへの拡張も説明している (pp.11–16)。

LambdaMART (pp.16–17) は MART に次を指定するだけ。

1. 擬似残差 $y_i=\lambda_i$（クエリ内の全ペアから集計）。分割は最小二乗で決める。各木はクエリをまたいだ全データの $\lambda_i$ を当てる。
2. 現在のスコアでの効用 $C=\sum|\Delta Z_{ij}|\log(1+e^{-\sigma(s_i-s_j)})$ から2階微分 $\partial^2C/\partial s_i^2=\sum\sigma^2|\Delta Z_{ij}|\rho_{ij}(1-\rho_{ij})$（$\rho_{ij}=1/(1+e^{\sigma(s_i-s_j)})$）を計算し、葉ごとのニュートンステップ $\gamma=\sum y/\sum w$ を使う (p.17)。
3. $F_k=F_{k-1}+\eta\sum_l\gamma_{lk}\mathbf 1(x\in R_{lk})$。初期値に既存モデルのスコアを入れればモデル適応もできる (p.17)。

学習率 $\eta$ を固定すれば $\sigma$ の選び方は学習に影響しない（$\gamma$ が $1/\sigma$ でスケールするため）(p.17)。LambdaRank がクエリごとに全重みを更新するのに対し、LambdaMART は全データを使って少数のパラメータ（葉）を更新するので、一部のクエリの効用を下げても全体が上がる分割を選べる (p.17)。最後に、2つのランカーの線形結合 $\alpha s^1+(1-\alpha)s^2$ の最適 $\alpha$ は、NDCG が $\alpha$ について有限回しか変わらないことを使って厳密に求められる、と述べる (p.18)。

## 批判的に読む

- 実験がないので、LambdaMART が他手法より良いという主張は本報告の中では裏付けられていない。根拠として挙げられるのは Yahoo! Learning to Rank Challenge 2010 の Track 1 優勝 (p.1) と、別論文の結果。
- $\lambda$ は「コストの勾配」として導いたものではなく、目的関数が明示されないので、何を最適化しているかは経験的にしか確認されていない (pp.9–11)。
- スコアは順位のためだけのもので、確率としての意味はない。$P_{ij}$ はペアの確率だが、レース全体の勝率にはならない。
- ウェブ検索の設定（クエリあたり多数の文書、上位 10 件だけが重要、多段階の関連度ラベル）を前提にしている。

## keiba-ai での使い方

- **LightGBM の `lambdarank` 目的関数の中身**: LightGBM の lambdarank はこの LambdaMART の実装である。クエリ＝レース、文書＝出走馬、ラベル＝着順から作る関連度（例: 1着=3, 2着=2, 3着=1, それ以外=0）。`label_gain` は $2^{l}-1$ の部分、`lambdarank_truncation_level` は NDCG@T の $T$ に当たる。ラベルの付け方と $T$ が「どの順位の正しさを重視するか」を決める。
- **何を重視するかを馬券の種類に合わせる**: 単勝なら1着だけを関連度にし $T=1$ 近く、3連複なら上位3頭を同じ関連度にする、と目的と馬券を一致させる。仮説: 単勝の回収率を目的にするなら、着順全体の NDCG を最適化するより、1着の関連度だけを大きくした設定（例: label_gain を 1着だけ大きく）のほうが良い。
- **ランキングのスコアは確率に変換しないと賭けに使えない**: lambdarank の出力はレース内で順序だけに意味がある。期待値計算には、レース内 softmax の温度を検証期間で当てる（Platt の発想）か、条件付きロジットで学習したモデルを別に用意する。RankNet のペア確率 $P_{ij}$ も勝率ではない。
- **確率モデルとの比較指標をそろえる**: ランキングモデル（NDCG）と確率モデル（log loss）は指標が違うので、同じレース集合で両方の指標と回収率を並べる。NDCG が高くても確率が悪ければ回収率は上がらないはず。
- **既存モデルからの適応と2モデル結合**: 初期スコアに市場の対数オッズを入れて LambdaMART を学習すれば、「市場の順位からのずれ」だけを学習させられる（LightGBM の `init_score`）。最適 $\alpha$ の厳密探索 (p.18) は、市場とモデルのスコアの結合係数の決定にそのまま使える。

## 関連ノート

- [Ke 2017](./2017-ke-lightgbm.md): keiba-ai で使う LightGBM。lambdarank 目的関数で本報告の LambdaMART を実装。
- [Fujisawa 2024](./2024-fujisawa-ranknet-condition-datasets.md): 競馬に RankNet を適用した研究。
- [Chung 2024](./2024-chung-learning-to-rank-seoul.md): ソウル競馬でのランキング学習。
- [So 2025](./2025-so-learning-to-rank-kra-web-service.md): 韓国競馬でのランキング学習の応用。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md): 競馬の予測を NDCG で評価した先行例。
- [Glickman 2015](./2015-glickman-stochastic-rank-ordered-logit.md): 着順全体の確率モデル（順位ロジット）。確率を出すランキングモデルとして対照的。
- [Platt 1999](./1999-platt-probabilistic-outputs-svm.md): 順序だけのスコアを確率に変換する方法。RankNet もシグモイドで確率を作る点で同系統。

## 検索語

ランキング学習, 学習による順位付け, ペアワイズ, リストワイズ, RankNet, LambdaRank, LambdaMART, ラムダ勾配, NDCG, DCG, ERR, MRR, MAP, 勾配ブースティング, 回帰木, ニュートンステップ, ポアンカレの補題, ランカーの線形結合, 競馬のランキング, learning to rank, LTR, pairwise ranking, cross entropy, lambda gradients, MART, multiple additive regression trees, gradient boosted trees, Newton step, normalized discounted cumulative gain, expected reciprocal rank, Yahoo Learning to Rank Challenge, LightGBM lambdarank, label_gain, truncation level, init_score, model adaptation

---
title: MM algorithms for generalized Bradley-Terry models
authors: Hunter David R.
year: 2004
venue: The Annals of Statistics 32(1) 384-406
url: https://projecteuclid.org/journals/annals-of-statistics/volume-32/issue-1/MM-algorithms-for-generalized-Bradley-Terry-models/10.1214/aos/1079120141.full
doi: 10.1214/aos/1079120141
topic: probability-models
tags: plackett-luce, bradley-terry, mm-algorithm, maximum-likelihood
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# 一般化 Bradley-Terry / Plackett-Luce の最尤推定を MM アルゴリズムで解く

> 一言で: 対数の凹性から作る1本の不等式で、Bradley-Terry の多くの拡張（ホームアドバンテージ、引き分け、3者以上の順位＝Plackett-Luce）について「単調に尤度が増え、条件下で必ず最尤推定値へ収束する」反復式を量産できることを示した。NASCAR 2002 の着順データで、Plackett-Luce の MM は修正 Newton 法より約65分の1の計算量で収束した。

## 要旨

対戦・順位データの古典モデルである Bradley-Terry モデル $P(i \text{ beats } j)=\gamma_i/(\gamma_i+\gamma_j)$ には多くの一般化がある。著者は minorization–maximization（MM）の枠組みで、それらの最尤推定アルゴリズムを統一的に導出し、収束の十分条件（グラフの強連結性に相当する Assumption 1 など）を示す。第5節で Plackett-Luce モデルを扱い、第6節で自動車レース（NASCAR）の着順に当てはめる。著者自身、新しいアルゴリズムを出すことより「1つの原理で量産できる」ことを示すのが主眼だと述べている (p.401)。

## モデルと記号

基本の対数尤度は $\ell(\gamma)=\sum_i\sum_j [w_{ij}\ln\gamma_i - w_{ij}\ln(\gamma_i+\gamma_j)]$。$w_{ij}$ は $i$ が $j$ に勝った回数。$\ell(a\gamma)=\ell(\gamma)$ なので $\sum_i\gamma_i=1$ で正規化する (p.386)。

**Assumption 1（Ford 1957）**: 個体をどう2群に分けても、第2群の誰かが第1群の誰かに少なくとも1回勝っている。勝ちを有向辺としたグラフで任意の2点間に経路がある、という意味。これが成り立たないと最尤推定値は存在しない（全敗の個体の強さは0に発散する）(p.386)。

扱う一般化（いずれも同じ手法で MM 更新式を導く）:

| モデル | 式 | 頁 |
|---|---|---|
| ホームアドバンテージ (Agresti) | $\theta\gamma_i/(\theta\gamma_i+\gamma_j)$ | p.387 |
| 引き分けあり (Rao–Kupper) | 閾値 $\theta>1$ 付き | p.387 |
| 引き分けあり (Davidson) | 勝:負:分 $=\gamma_i:\gamma_j:\theta\sqrt{\gamma_i\gamma_j}$ | p.387 |
| 3者比較 (Pendergrass–Bradley) | $\gamma_i\gamma_j/[(\gamma_i+\gamma_j+\gamma_k)(\gamma_j+\gamma_k)]$ | p.388 |
| Plackett-Luce | 下式 (24) | p.396 |

## アルゴリズム

鍵は $-\ln x \ge 1-\ln y - x/y$（等号は $x=y$）という不等式だけである (p.388, 式9)。これで $-\ln(\gamma_i+\gamma_j)$ を現在値 $\gamma^{(k)}$ の周りで線形の下界に置き換えると、下界関数 $Q_k$ はパラメータごとに分離し、閉じた形で最大化できる。

1. 初期値 $\gamma^{(1)}$ を任意に置く（例: 全員 $1/m$）。
2. Bradley-Terry なら $\gamma_i^{(k+1)} = W_i\,[\sum_{j\ne i} N_{ij}/(\gamma_i^{(k)}+\gamma_j^{(k)})]^{-1}$（$W_i$ は勝数、$N_{ij}$ は対戦数）(p.386, 式3)。これは Zermelo (1929) の古典的反復と一致する。
3. 更新した成分をすぐ使う巡回版（式4）も MM であり、同じ収束性を持つ (p.387)。
4. 必要なら正規化。尤度は各反復で単調に増加する。

**Plackett-Luce（第5節）**: $N$ 個の順位データ、$j$ 番目は $m_j$ 頭で $a(j,1)\to\cdots\to a(j,m_j)$ とする。モデルは

$P[\pi(1)\to\cdots\to\pi(k)]=\prod_{i=1}^{k}\gamma_{\pi(i)}/(\gamma_{\pi(i)}+\cdots+\gamma_{\pi(k)})$ (p.396, 式24)

MM 更新式は

$\gamma_t^{(k+1)} = w_t \Big/ \sum_{j=1}^{N}\sum_{i=1}^{m_j-1}\delta_{jit}\,[\sum_{s=i}^{m_j}\gamma_{a(j,s)}^{(k)}]^{-1}$ (p.398, 式30)

$w_t$ は個体 $t$ が「最下位でなかった」順位データの数、$\delta_{jit}$ は $j$ 番目の順位で $t$ が $i$ 位以下（まだ残っている）なら1。つまり「各段階の残存集合の強さの和の逆数」を、その段階に残っていた個体に配って合計するだけで済む。

著者はさらに、Plackett-Luce が Luce の選択公理（$P_B(i\text{ wins})=\gamma_i/\sum_{j\in B}\gamma_j$）と同値であり、部分集合の順位確率が元の集合に依存しない「内部整合性」を持つことを示す (p.396–397)。このため頭数の違うレースを1つの尤度にまとめてよい。

## 収束の理論（第4節）

Assumption 1 の下で対数尤度は上方コンパクト（上位集合が有界閉）になり、$\beta_i=\ln\gamma_i-\ln\gamma_1$ と再パラメータ化すると、追加の条件（Assumption 3）の下で厳密に凹になる。したがって MM は初期値によらず一意の最尤推定値へ収束する (p.398)。著者の知る限り、Plackett-Luce 尤度専用の最大化アルゴリズムは文献になく、Plackett (1975) も数値解法が必要と述べただけだった (p.398)。

## 数値例: NASCAR 2002

- データ: 36 レース、各 43 台（一部 42 台）、延べ 87 人。毎回最下位だった4人を除くと Assumption 1 を満たす 83 人になる (p.398–399)。
- 比較: MM（式30）と修正 Newton–Raphson（Newton の一歩が尤度を上げないときは MM の一歩に切り替える）。素の Newton は凹なのに挙動が悪かった (p.399)。
- 停止条件: パラメータ変化の L2 ノルム $<10^{-9}$。両者の解の差は各成分 $10^{-13}$ 未満 (p.399)。

| 手法 | MM 反復 | Newton 反復 | 浮動小数点演算 |
|---|---|---|---|
| MM | 26 | — | $0.22\times10^6$ |
| 修正 Newton–Raphson | 4 | 6 | $14.45\times10^6$ |

(p.400, Table 1)。82×82 行列の逆行列1回だけで $1.13\times10^6$ 演算かかり、MM 全体の5倍を超える (p.400)。ランダムな初期値でも常に 25〜26 反復で収束した (p.399)。

Table 2 (p.401) では、1レースだけ出て4着だった P. Jones の $\hat\beta=4.15$（SE 1.57）が最上位になる一方、36戦出た M. Martin は 2.08（SE 1.05）。平均着順の順と MLE の順は一致せず、SE も出走数の平方根に反比例しない。著者はこれを「同じレースの相手の強さから情報を得ている」ためと解釈する (p.400)。

## 批判的に読む

- **特徴量なしの強さ推定**: 推定するのは個体ごとの定数 $\gamma_i$ だけ。共変量（斤量、馬場、距離）を入れる条件付きロジット型には、この閉形式の更新はそのままでは使えない。
- **出走1回の個体の不安定さ**: P. Jones の例のように、出走数が少ない個体ほど極端な値になる。全勝・全敗なら MLE は $\pm\infty$ で、SE は真の標準偏差の推定と見なすべきでないと著者自身が注意している (p.400)。対策として「全員に微小な勝ちを配る」案を挙げるが効果は未検証 (p.402)。実務では事前分布（正則化）が必要。
- **予測性能の評価はない**: 論文は推定の計算効率だけを比較し、ホールドアウトでの予測精度は扱わない。
- **SE の計算**: MM は Hessian を作らないので SE が出ない。著者は SEM、準 Newton、パラメトリックブートストラップを候補に挙げるが未解決としている (p.402)。
- 収束が速かったのは本例の性質かもしれず、MM は一般に数百反復かかることが多いと著者も述べている (p.400)。

## keiba-ai での使い方

- **馬・騎手・調教師の「強さ」レーティング特徴量**: 過去の着順（頭数が違っても可）から Plackett-Luce の $\ln\gamma$ を MM で推定し、勾配ブースティング等の特徴量にする。必ず予測対象レースより前のデータだけで推定し直す（時系列で累積推定）。リークを避けるにはウォークフォワードで再推定する。
- **連結性のチェック**: Assumption 1 は「未勝利・全敗馬」「他地区との交流がない地方馬群」で破れる。推定前に勝敗グラフの強連結成分を調べ、破れる馬には事前分布（擬似的な勝ち負け）を足す。Bayesian 版は [Guiver 2009](./2009-guiver-bayesian-plackett-luce.md) を参照。
- **仮説**: 「出走数で縮小した Plackett-Luce レーティング」は、単純な平均着順や勝率より、次走の単勝確率の対数損失を下げる。比較は同じ時系列分割で行い、出走数が少ない馬で差が大きいかを層別に見る。
- **共変量付きの場合**: 特徴量 $x$ による $\ln\gamma=\beta^\top x$ の条件付きロジットは勾配法（L-BFGS）で十分で、MM は「特徴量なし部分（ランダム効果）」の推定に限って使うのが現実的。

## 関連ノート

- [Luce 1959](./1959-luce-individual-choice-behavior.md): 選択公理。本論文は Plackett-Luce がこれと同値であることを示す。
- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 式(24) の原典。数値解法は与えていなかった。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 単勝確率から着順確率を作る同じ形の式。
- [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md): 共変量付きの条件付きロジット（Plackett-Luce の特徴量版）。
- [Guiver & Snelson 2009](./2009-guiver-bayesian-plackett-luce.md): Plackett-Luce のベイズ推定。
- [Stern 1990](./1990-stern-gamma-permutations.md): Plackett-Luce を含むガンマ順序統計モデルの族。
- [Glickman & Hennessy 2015](./2015-glickman-stochastic-rank-ordered-logit.md): 時間変化する強さの順位ロジット。

## 検索語

MM アルゴリズム, minorization-maximization, majorization-minimization, Bradley-Terry モデル, ブラッドリー・テリー, Plackett-Luce モデル, プラケット・ルース, Luce の選択公理, Luce's choice axiom, 一対比較, paired comparison, 順位データ, ranking data, 最尤推定, maximum likelihood, Zermelo アルゴリズム, Newton-Raphson, ホームアドバンテージ, home-field advantage, 引き分け, Rao-Kupper, Davidson, Pendergrass-Bradley, NASCAR, 強さレーティング, rating, Ford の条件, 強連結

---
title: The Analysis of Permutations
authors: Plackett R. L.
year: 1975
venue: Journal of the Royal Statistical Society Series C (Applied Statistics) 24(2) 193-202
url: https://academic.oup.com/jrsssc/article/24/2/193/6953554
doi: 10.2307/2346567
topic: probability-models
tags: plackett-luce, ranking-model, permutation, logistic-model
verified: abstract
importance: high
source: unavailable
---

# 順列データの確率モデル：Plackett-Luce モデルの出典

> **原本未取得。** OUP の論文ページにゲスト閲覧できる PDF があるが、この環境からの自動取得が拒否されたため、手動取得待ち。本ノートは OUP/Wiley の要旨と、本論文を詳しく引用する後続論文（Henery 1981、Hunter 2004、Guiver & Snelson 2009。いずれも library に原本あり）に基づく。

> 一言で: $r$ 個の対象の $r!$ 通りの順列に、最大 $r!-1$ 個のパラメータを持つ確率分布を定義し、その推定と検定を論じた。最も単純な「1次モデル」が、勝率だけで着順確率を作る式（Harville 公式と同じ）であり、Luce (1959) の選択公理と合わせて「Plackett-Luce モデル」と呼ばれるようになった。

## 要旨から分かること

- 順列全体の上に、ロジスティック（対数線形）型のパラメータを段階的に足していく確率分布の体系を定義する。パラメータを全部入れると $r!-1$ 個（飽和モデル）。
- 推定と検定の問題を扱い、選挙の投票（候補者の順位づけ）などのデータに適用する。
- キーワード: カテゴリカルデータ、消費者選好、分割表、ロジスティックモデル、ロジット分析、投票バイアス、ランダム順列。

## 1次モデル（Plackett-Luce）

後続研究が引用する形で書くと、各対象に正のパラメータ $v_i$ を与え、順序 $\omega=(\omega_1,\dots,\omega_K)$ の確率を

$PL(\omega\mid v)=\prod_{k=1}^{K}\dfrac{v_{\omega_k}}{v_{\omega_k}+\cdots+v_{\omega_K}}$

とする（[Guiver & Snelson 2009](./2009-guiver-bayesian-plackett-luce.md), PDF p.2, 式1–2）。$v_i$ を勝率 $p_i$ とすれば、Plackett が示した「勝率から着順確率を作る」解 $p_i\lbrace p_j/(1-p_i)\rbrace \lbrace p_k/(1-p_i-p_j)\rbrace $ になる（[Henery 1981](./1981-henery-permutation-probabilities.md), p.86 による引用）。

この分布には3つの解釈がある。

1. **逐次選択（Luce の選択公理）**: まず全体から1着を $v$ に比例して選び、残りから2着を選び…と繰り返す。Hunter (2004) は Plackett-Luce と Luce の選択公理が同値であることを示した（[Hunter 2004](./2004-hunter-mm-bradley-terry.md), p.396–397）。
2. **壺（vase）モデル**: 色の割合が $v$ に比例する無限個の玉から、まだ出ていない色が出るまで引き続ける (Guiver PDF p.2)。
3. **Thurstone 型（順序統計量）**: 各対象の得点が独立な Gumbel 分布（走破時間なら指数分布）に従うとき、その並び順の分布になる。位置だけが違う独立な得点分布から Plackett-Luce が出るのは Gumbel のときに限る（Yellott 1977、Guiver PDF p.2 による）。

## 競馬との関係

- Guiver & Snelson は、この分布の形は Plackett (1975) が $K$ 頭の競馬の確率をモデル化するために初めて考えたと書く (PDF p.1)。Henery (1981) も冒頭で「Plackett (1975) は勝率から入着確率を求める問題を提起し解を示した」と紹介する (p.86)。
- Henery (1981) はこの解の欠点として、確率が頭数に依存しないこと、Pr{123}（人気順どおりの決着）を過大、Pr{321} を過小に見積もりやすいことを挙げる (Henery p.86, p.91)。
- 最尤推定について、Plackett は数値的にしか求められないと述べただけで、専用のアルゴリズムは Hunter (2004) の MM 法まで現れなかった（Hunter p.398 による）。

## 原本で確認すべき点（未確認）

- 高次の項（2次以上の交互作用パラメータ）の具体的な定義と、どのような順位の依存関係を表すのか。
- 投票データと、要旨に出てくるもう一つのデータ（"beanstores" と表記）の内容と推定結果。
- 競馬データを実際に分析しているか（Henery と Guiver の記述からは問題提起のみの可能性がある）。

## 批判的に読む

- 1次モデルは「どの段階でも同じ強さ $v_i$ で選ばれる」と仮定するため、2・3着争いのランダム性が1着争いより大きい競馬の実態（Benter 1994、Ali 1998）を表せない。高次項はそれを補う方向だが、パラメータ数が $r!$ のオーダーで増えるため、そのままでは実用的でない。
- 原本未読のため、高次モデルの有用性の評価は保留。

## keiba-ai での使い方

- **学習の尤度**: 条件付きロジット（レース内 softmax）を1着だけでなく上位 $k$ 着まで使う場合、その尤度は Plackett-Luce の上位 $k$ 段の積になる。LightGBM の独自目的関数や PyTorch の損失として「Plackett-Luce top-k 損失」を実装する価値がある（ListMLE と同じ形）。
- **段階ごとの強さの変化**: 1次モデルの欠点を補う簡単な方法は、段階 $k$ ごとに強さを $v_i^{\alpha_k}$（$\alpha_1=1$、$\alpha_2,\alpha_3<1$）とすること（Benter の補正）。仮説「$\alpha_k$ を推定する方が、固定の Plackett-Luce より3連複・3連単の対数損失が小さい」。
- **シミュレーション**: Gumbel ノイズを $\log v_i$ に足して並べ替えれば Plackett-Luce に従う着順を高速にサンプリングできる（Gumbel-max trick）。買い目の的中確率のモンテカルロ推定に使う。

## 関連ノート

- [Luce 1959](./1959-luce-individual-choice-behavior.md): 選択公理。同値なモデルの理論的出典。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 同じ公式を競馬に当てはめた。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 本論文の1次モデルを指数分布の順序統計量として位置づけ、正規版を提案。
- [Stern 1990](./1990-stern-gamma-permutations.md): ガンマ分布で拡張した族。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): Plackett-Luce の最尤推定（MM 法）。
- [Guiver & Snelson 2009](./2009-guiver-bayesian-plackett-luce.md): ベイズ推定。
- [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md): 特徴量付きの Plackett-Luce（rank-ordered logit）。
- [Wilkens 2026](./2026-wilkens-plackett-luce-uk-racing.md): 英国競馬への Plackett-Luce の適用。

## 検索語

Plackett-Luce モデル, プラケット・ルース, Plackett model, 順列, permutation, 順位データ, ranking data, 順位モデル, ranking model, 1次モデル, first-order model, ロジスティックモデル, logit, 対数線形, 投票, voting, Luce の選択公理, Gumbel, 指数分布, vase model, 壺モデル, ListMLE, rank-ordered logit, 着順確率, ordering probability

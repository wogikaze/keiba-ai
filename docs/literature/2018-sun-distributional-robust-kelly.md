---
title: Distributional Robust Kelly Gambling: Optimal Strategy under Uncertainty in the Long-Run
authors: Sun Qingyun, Boyd Stephen
year: 2018
venue: arXiv
url: https://arxiv.org/abs/1812.10371
doi: 10.48550/arXiv.1812.10371
topic: betting-strategy
tags: kelly, distributionally-robust, estimation-error, convex-optimization
verified: fulltext
importance: high
source: downloaded
source_version: preprint
---

# 分布ロバスト Kelly：確率が「ある集合のどこか」としか分からないときの最悪ケース成長率の最大化

> 一言で: 結果の確率 $\pi$ が不確実性集合 $\Pi$ の中にあるとだけ仮定し、$\min_{\pi\in\Pi}\mathbb{E}_\pi\log(r^\top b)$ を最大化する。箱・楕円・f ダイバージェンス球・Wasserstein 球などの集合で双対を取ると CVXPY で解ける形になることを示し、Breiman の漸近最適性を「最悪ケース成長率」に拡張した。20頭の複勝（2着以内）の数値例で、通常の Kelly が最悪分布で −2.2% になるところを、ロバスト版は +0.7% に保った。

原本は arXiv 最終版（2021年6月更新）。PDF 本文の表題は "Distributional Robust Kelly Strategy" で、arXiv 登録名（Gambling）と一部異なる。ページは取得 PDF のもの。

## 問題意識

Kelly 戦略は理論的に優れているが、実務で直接使われることは少ない。推定した分布が真の分布と違うからである (p.1-2)。著者らは不確実性の源を3つ挙げる (p.2):

1. 学習データの経験分布と、未知の真の分布（テスト時の分布）の差。最適化すると外れる「optimizer's curse」。
2. 学習環境と運用環境の分布シフト（非定常性）。
3. 平均・共分散の推定誤差。高次モーメントはノイズで情報がない。

リスク（確率が分かっている不確かさ）と不確実性（確率自体が分からない、曖昧さ回避）を区別し、Kelly は前者、本論文は後者を扱うと位置づける (p.3)。

## モデル

有限の $K$ 結果。払戻行列 $R \in \mathbb{R}^{n\times K}$ の列が各結果の払戻ベクトルで、$G_\pi(b) = \pi^\top \log(R^\top b)$ が対数成長率 (p.2)。

分布ロバスト Kelly 問題（DRKP）(p.3):

$\max_{b \in B}\ \inf_{\pi\in\Pi}\ \pi^\top \log(R^\top b)$

$G_\Pi(b)$ は凹関数の下限なので凹。ただし一般には扱いにくい。$\inf$ の部分を双対で書き換え、1つの凸最大化問題にまとめるのが本論文の中心 (p.4)。

### 扱える不確実性集合（DCP で書ける形）

| 集合 | 中身 | 定理 |
|---|---|---|
| 多面体 | $A_0\pi = d_0, A_1\pi \le d_1$ | Theorem 1 (p.4) |
| 箱 | $\lvert\pi - \pi^{nom}\rvert \le \rho$（成分ごと） | Theorem 2 (p.4) |
| 楕円（p ノルム球） | $\lVert W^{-1}(\pi - \pi^{nom})\rVert_p \le 1$ | Theorem 3 (p.4) |
| f ダイバージェンス球 | $D_f(\pi\Vert\pi^{nom}) \le \epsilon$（KL など）。Fenchel 共役を使う | Theorem 4 (p.5) |
| Wasserstein 球 | $D_c(\pi, \pi^{nom}) \le s$。元の分布の台にない結果にも重みを移せるので「ブラックスワン」向き | Theorem 5 (p.5) |
| 平均・共分散の推定値 | Delage–Ye 型のモーメント集合。SDP になる | Theorem 6 (p.6) |

箱集合の場合、目的は $\min_k(\log(R^\top b)_k + \mu_k) - (\pi^{nom})^\top\mu - \rho^\top|\mu|$ のような形（$\mu$ は双対変数）になり、そのまま CVXPY に書ける (p.4)。付録 11 に CVXPY のコード例がある。

### 理論

確率の列が毎回 $\Pi$ の中で（敵対的に）変わってもよい逐次賭けで、分布ロバスト Kelly 戦略は最悪ケースの資産成長率を漸近的に最大化し、本質的に異なる他の戦略を桁で上回る (Theorem 7, 8; 第3節)。Breiman (1961) の結果の拡張。

## 数値例：20頭の複勝（2着以内）

- 20頭、各馬の勝率は $\exp z_i$ に比例（$z_i \sim N(0, 1/4)$）。最速馬で約 20%、最遅で約 1% (p.14-15)。
- 2着以内の組 $\lbrace j,k\rbrace $ の確率は Harville 型 $\beta_j\beta_k/(1-\beta_j) + \beta_k\beta_j/(1-\beta_k)$ で、結果数 $K = 190$。賭けは各馬の「2着以内」の 20 通り (p.14)。
- 払戻はパリミュチュエルで、各馬への票の割合を名目の勝率 $\beta_i$ と同じにする (p.14)。控除率は入っていない（式からの読み取り）。
- 不確実性集合は箱（各確率が名目値の ±η 倍）と $\ell_2$ 球（半径 c）(p.14)。

結果 (p.8, Table 1):

| 成長率 | 通常の Kelly | ロバスト（箱 η=0.26） | ロバスト（球 c=0.016） |
|---|---|---|---|
| 名目分布のもと | 4.3% | 2.2% | 2.2% |
| 最悪分布のもと | −2.2% | 0.7% | 0.4% |

η と c は通常の Kelly の最悪ケースが −2.2% になるように選んだ (p.8)。ロバスト版は名目分布での成長率を半分にする代わりに、最悪分布でも利益を残す。ロバスト版の賭けは通常の Kelly より多くの馬に分散する (p.3, Figure 1)。

## 不確実性集合の選び方

著者ら自身、集合の大きさの決め方が実用上の弱点だと認める (p.9)。提案は3つ:

- 機会制約（VaR、CVaR、ドローダウン制約）との関係から集合を作る。
- コンフォーマル予測で有限標本の被覆保証付きの集合を作る（今後の課題）。
- 集合のパラメータを、標本外の Kelly 損失 $\sum_i \log(r_i^\top b^\star(\theta; X_i))$ を上位目的とする2段階最適化で学習する。凸最適化の解の微分（cvxpylayers）で勾配を得る (p.9, 付録 10)。

## 批判的に読む

- **実データの検証なし**。数値例は人工の1レースで、名目分布と払戻の作り方から、そもそもエッジがどこにあるかが曖昧。オッズを名目確率に一致させているのに名目 Kelly の成長率が正（4.3%）なのは、控除率なしで、複勝の払戻計算に起因する歪みを突いているためと思われる（推測、未確認）。
- **集合の大きさの選択に正解がない**。η や c を大きくすれば何もしない（賭けない）方向に寄る。今回の η=0.26 は「通常の Kelly の最悪ケースが −2.2%」という恣意的な基準で決めた。
- **最悪ケースは悲観的すぎる可能性**。推定誤差は通常ランダムで、敵対的ではない。期待値で扱う [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md) や縮小係数の [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md) と比べてどちらが標本外で良いかは示されていない。
- 理論は漸近的な結果で、有限期間の成長率やドローダウンの性質は今後の課題とされる (p.9)。

## keiba-ai での使い方

- **確率モデルの不確かさの大きさを集合で表す**: 例えば各馬の勝率に「較正誤差の分だけ ±η の箱」を付ける。η はバリデーションでの較正誤差（信頼性曲線のずれ）から決められる。箱集合なら CVXPY で数十行。
- **Wasserstein 球は着順の入れ替わりに合う**: コスト $c$ を「着順の距離」にすれば、「1着と2着が入れ替わる程度のずれ」を許す集合が作れる。3連単や馬連のような組み合わせ券種で、隣接する組み合わせに確率が漏れるリスクを表現できる（推測）。
- **実験案**: 仮説「単勝と複勝を同時に配分するとき、箱集合（η を検証データの較正誤差から設定）のロバスト Kelly は、通常の Kelly よりバックテストの最大ドローダウンが小さく、対数成長率の低下は fractional Kelly（同じドローダウン水準）より小さい」。評価は確定オッズでの対数成長率と最大ドローダウン。
- **集合の大きさの学習（付録 10）**: 検証期間の標本外 Kelly 損失を最大にするよう η を選ぶ。グリッド探索でも十分で、cvxpylayers までは要らない。時系列順の分割（過去で学習、未来で η を選ぶ、さらに未来で評価）を守る。

## 関連ノート

- [Kelly 1956](./1956-kelly-information-rate.md), [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): 本論文の理論部分が拡張する元の結果。
- [Busseti 2016](./2016-busseti-risk-constrained-kelly.md): 同じ Boyd グループの、確率既知でドローダウン制約を付ける Kelly。本論文で [18] として引用。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md): 2結果で推定誤差に応じて賭け額を縮める。不確実性の扱い方が対照的（期待効用 対 最悪ケース）。
- [Metel 2017](./2017-metel-kelly-horse-races-uncertainty.md): ロジットの係数の推定誤差を期待値・機会制約で扱う単勝版。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 数値例の2着以内の確率の計算に使われる式。
- [Hausch 1981](./1981-hausch-racetrack-market-efficiency.md): 複勝・3着内での Kelly。数値例の題材と近い。
- [Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md): 分布ロバスト Kelly を含む戦略を実データで比較したレビュー。

## 検索語

分布ロバスト最適化, ロバストKelly, 最悪ケース成長率, 不確実性集合, 曖昧さ回避, 推定誤差, 箱型不確実性, 楕円型不確実性, KLダイバージェンス, ワッサースタイン距離, 複勝, 凸最適化, CVXPY, distributionally robust optimization, DRO, robust Kelly, worst-case growth rate, uncertainty set, ambiguity aversion, f-divergence, Wasserstein ball, Delage Ye, optimizer's curse, conformal prediction, cvxpylayers, bi-level optimization, Boyd

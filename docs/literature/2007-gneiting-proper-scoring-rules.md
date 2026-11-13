---
title: Strictly Proper Scoring Rules, Prediction, and Estimation
authors: Gneiting Tilmann, Raftery Adrian E.
year: 2007
venue: Journal of the American Statistical Association 102(477) 359-378
url: https://www.tandfonline.com/doi/abs/10.1198/016214506000001437
doi: 10.1198/016214506000001437
topic: evaluation-and-features
tags: proper-scoring-rules, log-loss, brier-score, crps, skill-score, interval-score, cross-validation, bregman-divergence
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 厳密に適正なスコアリングルールの一般理論（Gneiting & Raftery の総説）

> 一言で: 確率予報の採点が「本当に信じる分布を出すのが期待値で最も得」になる（適正である）ための必要十分条件は、期待スコア関数が凸であること、と一般の確率空間で示した総説。Brier・対数・球面スコア、CRPS、区間スコアを同じ枠組みで整理し、スキルスコアは一般に適正でないこと、直感的に見える不適正なスコアが誤った結論を導く実例を示した。

原本は著者 (Raftery) のサイトにある JASA 掲載版 (pp.359–378, 20ページ)。

## 基本の定義

スコアは「大きいほど良い」向きで定義する。予報 $P$ を出して $\omega$ が実現したときの報酬が $S(P,\omega)$、$S(P,Q)$ は $\omega\sim Q$ での期待値 (p.360)。

- **適正 (proper)**: すべての $P,Q$ で $S(Q,Q)\ge S(P,Q)$。
- **厳密に適正 (strictly proper)**: 等号が $P=Q$ のときだけ。予報者は本心の $Q$ を出すよう促される。
- $cS+h(\omega)$（$c>0$）も適正。この変換で移り合うスコアは同値 (p.360)。

この考え自体は少なくとも Brier (1950) にさかのぼり、"proper" の語は Winkler & Murphy (1968) による (p.360)。

## 中心定理：適正性 = 凸関数

**定理1** (p.361): 正則なスコア $S$ が適正であることと、凸関数 $G$ とその劣接線 $G^*$ があって

$$S(P,\omega)=G(P)-\int G^*(P,\omega)\,dP(\omega)+G^*(P,\omega)$$

と書けることは同値。厳密に適正 ⇔ 厳密に凸。$G(P)=S(P,P)$ は期待スコア（一般化エントロピー）で、$d(P,Q)=S(Q,Q)-S(P,Q)$ はその Bregman ダイバージェンスになる (pp.361–362)。

カテゴリ変数 $\lbrace 1,\dots,m\rbrace $ では、これは Savage 表現 $S(\mathbf p,i)=G(\mathbf p)-\langle G'(\mathbf p),\mathbf p\rangle+G'_i(\mathbf p)$ になる（定理2, p.362）。**有界な凸関数を1つ選べば適正なスコアが1つ作れる**ということ。

| スコア | $S(\mathbf p,i)$ | 対応する $G$ / ダイバージェンス | 性質 (p.363) |
|---|---|---|---|
| 二次 (Brier) | $2p_i-\sum_j p_j^2-1$ | 二乗ユークリッド距離 | 厳密に適正 |
| 球面 | $p_i/\lVert\mathbf p\rVert_2$（擬球面は $\alpha$ 乗の一般化） | — | 厳密に適正 |
| 対数 | $\log p_i$ | 負のシャノンエントロピー / KL ダイバージェンス | 厳密に適正。非有界 |
| 0–1（最頻値が当たれば得点） | $1/\#M(\mathbf p)$ または 0 | $\max_j p_j$ | 適正だが**厳密ではない** |

対数スコアは非有界であること（起こらないとした事象が起きると $-\infty$）で批判されてきた、と紹介している (p.363)。0–1 スコアは誤分類損失そのもので、正解率で確率モデルを選ぶと「最頻値さえ合えば確率の値はどうでもよい」ことになる。

### 2値の場合：Schervish 表現 (pp.363–365)

2値予報の適正なスコアはすべて、コスト・損失比 $c\in(0,1)$ ごとの非対称 0–1 スコア $S_c(p,1)=(1-c)\mathbf 1\lbrace p>c\rbrace $, $S_c(p,0)=c\,\mathbf 1\lbrace p\le c\rbrace $ を、非負の測度 $\nu(dc)$ で混ぜたものとして書ける（定理3）。$\nu$ が「どのコスト比の意思決定を重視するか」を表す (Table 1, p.365)。

- Brier: $\nu$ は一様（すべての閾値を等しく重視）。
- 対数: 密度 $(c(1-c))^{-1}$（$c$ が 0 や 1 に近い閾値ほど重視）。
- Buja らのベータ族は、$\nu$ の密度 $c^{\alpha-1}(1-c)^{\beta-1}$ で対数 ($\alpha=\beta=0$)・Brier ($\alpha=\beta=1$)・0–1 ($\alpha=\beta\to\infty$) をつなぐ (p.365)。

## スキルスコアは一般に適正でない (p.362)

気象分野では $S^{\text{skill}}=(S^{\text{fcst}}-S^{\text{ref}})/(S^{\text{opt}}-S^{\text{ref}})$ をよく使う（基準は気候値）。予測しやすさの違う状況どうしを比べるための正規化である。しかし**元のスコアが適正でも、スキルスコアは一般に不適正**。Murphy (1973) は Brier スキルスコアが予報の数が増えれば漸近的に適正になると示した。Mason (2004) の「適正である」という主張は誤った近似に基づく、と著者は指摘する (p.362)。

また、スコアを比べられるのは**まったく同じ予報状況の集合**についてだけで、違う集合では本来の予測しやすさと予測性能が交絡する (p.362)。

## 連続変数のスコア

- 密度予報には二次スコア・擬球面スコア・対数スコアが厳密に適正 (pp.365–366)。
- **CRPS** (p.367): $\mathrm{CRPS}(F,x)=-\int(F(y)-\mathbf 1\lbrace y\ge x\rbrace )^2dy$。全閾値での Brier スコアの積分で、$\frac12E|X-X'|-E|X-x|$ とも書ける。正規分布には閉形式がある。負の向きにすると観測と同じ単位になり、点予報なら絶対誤差に一致するので、点予報と確率予報を直接比べられる。密度のスコアと違い、実現値に「近い」値への確率も評価する（距離に敏感）。
- エネルギースコア・カーネルスコアへの一般化 (pp.367–370)。
- **区間スコア** (p.370): 中央 $(1-\alpha)$ 予測区間 $[l,u]$ に対し $S^{\text{int}}_\alpha=(u-l)+\frac2\alpha(l-x)\mathbf 1\lbrace x<l\rbrace +\frac2\alpha(x-u)\mathbf 1\lbrace x>u\rbrace $（負の向き）。幅の狭さと外れの罰を同時に測り、適正。

## スコアと交差検証 (pp.371–373)

対数スコアの差はベイズファクターとつながる（7.1節）。データに順序がないときに、除外するデータの量をランダムにする **random-fold 交差検証** を提案し、対数スコアの代わりに CRPS など他の適正スコアを使う一般化を予想として述べている (p.372)。

## 事例：不適正なスコアが誤った結論を導く (pp.373–374)

ワシントン大学の 5 メンバーアンサンブルによる、太平洋岸北西部の 48 時間先海面気圧予報（2000年1–6月、16,015 件）。アンサンブル平均の RMSE 3.30 mb に対しアンサンブルの広がりは 2.13 mb で、比 $r_0=1.55$ の過小分散 (p.373)。予報分布を $N(\mu,(r\sigma)^2)$ として、膨張係数 $r$ を各スコアで最適化した。

| スコア | 最適な $r$ (Table 3, p.373) | 適正か |
|---|---|---|
| 二次スコア | 2.18 | 適正 |
| 球面スコア | 1.84 | 適正 |
| 対数スコア | 2.41 | 適正 |
| CRPS | 1.62 | 適正 |
| 線形スコア $p(x)$ | 0.05 | 不適正 |
| 確率スコア $\int_{x-1}^{x+1}p$ | 0.02 | 不適正 |

不適正な2つのスコアは「不確実性はほぼない」という結論を出してしまう (p.374)。また、対数スコアの最適値が最も大きいのは、アンサンブルの分散がつぶれた少数の事例を厳しく罰するためで、対数スコアは極端な事例に敏感、CRPS のほうが外れ値に頑健だと著者は述べる (p.374)。区間予報では、名目の被覆率が 50% 区間で $r=1.78$、90% 区間で $r=2.11$ で達成され、区間スコアの最適は $r=1.56$, $1.72$ だった (p.374)。

## 批判的に読む

- 総説で、理論の大半は既存結果の厳密化・一般化。新しい実証は気象の1事例だけ。
- 「どのスコアを使うべきか」には一つの答えを出していない。問題に合わせて選べ、が主張であり、Schervish 表現の $\nu$（重視する意思決定の閾値）で選ぶのが理論的な指針になる。
- 順序カテゴリ（着順のような）のスコアは本論文では主題でない。RPS は CRPS の離散版として位置づけられるが、詳しくは扱わない。

## keiba-ai での使い方

- **モデル選択に使う指標は厳密に適正なものに限る**: 対数損失（＝対数スコア）と Brier は可。正解率（的中率）は 0–1 スコアで厳密に適正でないので、確率モデルの選択に使わない。「本命の的中率」で選ぶと、確率の値の質を見ないことになる。
- **市場との比較を「スキルスコア」でやるときの注意**: $1-\text{LL}_\text{model}/\text{LL}_\text{market}$ のようなスキルスコアは不適正になりうる。報告用には使ってよいが、学習・選択には元のスコアの差（例: 1 レースあたりの対数尤度の差）を使う。またレース集合が違う比較（例: 2022年のモデル A と 2023年のモデル B）は予測しやすさが交絡するので、同じレース集合で比べる。
- **対数損失と Brier の違いを Schervish 表現で解釈する**: 対数スコアは $c$ が 0 に近い閾値（低確率の判断）を重く見る。競馬の単勝では、期待値 $p\times$オッズ$>1$ の判断をオッズ 20 倍以上の馬でもするので、「$c\approx 1/\text{オッズ}$ の閾値での判断の質」が回収率に効く。仮説: 人気薄を買う戦略の回収率は、Brier よりも対数損失の改善と強く連動する。さらに、オッズ帯を重み付けしたベータ族スコアを設計すれば、賭け戦略に合った評価指標になる。
- **対数損失の外れ値感度**: 事例の「対数スコアは少数の極端な事例に引っ張られる」は、確率 0.1% と予測した馬が勝つレースに当たる。確率の下限クリップ（例: 0.1%）や、勝ち馬の対数尤度の分布を見る診断を入れる。
- **走破タイム予測の評価に CRPS**: タイムや着差を分布で予測するモデル（正規誤差モデルなど）には CRPS が使える。点予測の MAE と同じ単位で比べられる。

## 関連ノート

- [Brier 1950](./1950-brier-verification-probability-forecasts.md): 二次スコアの原典。適正性の考え方の起点として本論文が引用。
- [Murphy 1973](./1973-murphy-brier-decomposition.md): Brier スコアの分解。本論文は Murphy (1973) のスキルスコア漸近適正性の議論を引く（同年の別論文）。
- [Constantinou 2012](./2012-constantinou-rps-football.md): 順序カテゴリの RPS。CRPS の離散版。
- [Wheatcroft 2021](./2021-wheatcroft-case-against-rps.md): RPS への批判。適正性と距離への感度の議論の続き。
- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md): 二乗誤差と対数損失で校正法を比較。適正スコアの実用例。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 賭けのモデル選択に正解率ではなく校正を使うべきという主張。本論文の「0–1 スコアは厳密に適正でない」と同じ方向。
- [Kelly 1956](./1956-kelly-information-rate.md): 対数スコアと賭けの成長率の関係（本論文も対数スコアの賭け解釈に触れる）。

## 検索語

適正スコア, 厳密に適正なスコアリングルール, スコアリングルール, 対数スコア, 対数損失, Brier スコア, 二次スコア, 球面スコア, 0-1 スコア, 誤分類損失, スキルスコア, CRPS, 連続順位確率スコア, エネルギースコア, 区間スコア, 分位点スコア, Bregman ダイバージェンス, KL ダイバージェンス, エントロピー, Savage 表現, Schervish 表現, 交差検証, ベイズファクター, 校正, 鋭さ, アンサンブル予報, proper scoring rule, strictly proper, logarithmic score, log loss, ignorance score, quadratic score, Brier score, spherical score, zero-one score, skill score, continuous ranked probability score, energy score, kernel score, interval score, quantile score, Bregman divergence, Savage representation, Schervish representation, beta family, random-fold cross-validation, calibration, sharpness, ensemble forecast, inflation factor

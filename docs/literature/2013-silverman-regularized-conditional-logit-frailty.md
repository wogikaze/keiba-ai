---
title: Predicting Horse Race Winners through a Regularized Conditional Logistic Regression with Frailty
authors: Silverman Noah, Suchard Marc A.
year: 2013
venue: Journal of Prediction Markets 7(1) 43-52
url: https://econpapers.repec.org/RePEc:buc:jpredm:v:7:y:2013:i:1:p:43-52
doi: 10.5750/jpm.v7i1.595
topic: machine-learning
tags: conditional-logit, regularization, frailty, gpu, hong-kong, betting-simulation
verified: abstract
importance: medium
source: unavailable
source_version: none
---

# 条件付きロジットに「フレイルティ」と利益最大化の LASSO を入れ、GPU で調整した香港競馬モデル

> 一言で: Benter 以来の条件付きロジット（レース内ソフトマックス）に、(1) Cox 比例ハザードの疫学的な使い方から借りた「フレイルティ」項と、(2) 尤度ではなく**利益**を目標にして選ぶ LASSO 罰則を加え、巡回座標降下法を GPU で並列化して多数の調整パラメータを試した。香港4年分で学習、翌1年で検証し、既発表の香港の手法より有意に高い投資収益率を報告する。

**原本未取得。** Journal of Prediction Markets（ubplj.org）は購読者限定で、ダウンロード URL はログイン画面に転送された。Semantic Scholar・OpenAlex に OA 版はなく、Scribd 上の転載は権利関係が不明なので使わない。以下は EconPapers/RePEc と Semantic Scholar の要旨、全文取得済みの他論文の記述に基づく。数値・式は未確認。

## 要旨から分かること

- 出発点: Benter (1994) 以来、条件付きロジスティック回帰は勝率推定の定番。
- 改良1: 尤度関数に「フレイルティ」パラメータを加える。疫学で Cox 比例ハザードモデルに使われるものから借りた。
- 改良2: 尤度に LASSO 罰則をかけ、罰則の強さは**利益を最大化する**ように選ぶ（尤度最大化ではない）。
- 計算: 巡回座標降下法（cyclical coordinate descent）を GPU 上で並列化し、多くの調整パラメータを高速に試す。
- データ: 香港の4年分で学習し、翌1年をホールドアウトとして賭けをシミュレーション。
- 結果: 投資収益率は、香港のレースを扱った既発表のどの手法よりも有意に高い。
- 検索結果に表示された二次的な要約（Scribd 上の資料）では、3,681レース・ホールドアウトで ROI 36.73% とされる。原本では未確認。

## 二次資料での扱い

- [Nakakita 2023](./2023-nakakita-hierarchical-bayes-horse-jockey.md) は「Cox 比例ハザードモデルに着想を得たパラメータを含めてモデルを発展させた」研究として引く（同原本 p.4）。
- [Lyons 2016](./2016-lyons-greyhound-man-v-machine.md) は競馬への機械学習適用の例として Davoodi (2010)、Williams (2008) と並べて引く（同原本 p.4）。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md) は、競馬では各結果の確率の信頼できる推定が難しいことの文献として Benter (1994) と並べ「Silvermann 2013」を引くが、参考文献の題名は別の論文（"Optimal Decision with Multiple Agents of Varying..."）になっており、本論文を指すとは限らない。

## 批判的に読む（要旨からの推測を含む）

- **利益で罰則を選ぶことの危うさ**: 利益は分散が大きく、数千レースでも少数の高配当に左右される。調整パラメータを利益で選び、その選択に使った期間と最終評価の期間が分かれていなければ、報告 ROI は楽観的になる。要旨からは、選択が学習4年の中の検証で行われたのか、ホールドアウト年を見て行われたのかは分からない（未確認）。
- 「有意に高い」の検定方法、ROI の計算（賭け方: 固定額か Kelly か、配当は確定オッズか）、市場確率をモデルに入れているか（二段階か一段階か）は未確認。
- フレイルティの中身（馬ごとのランダム効果か、レースごとの異質性か）も要旨からは分からない。旧ノートは「配当（市場情報）を使うフレイルティ」と書いていたが、原本で確認できていない。
- 長所: 時系列のホールドアウト（過去4年→翌1年）は要旨から読み取れる。

## keiba-ai での使い方

- **強いベースライン**: GBDT やニューラルネットの前に、L1/L2 正則化付きの条件付きロジット（レース内ソフトマックス）を置く。特徴量が多いときの変数選択にもなる。
- **調整パラメータの選び方の実験**: 正則化の強さを (a) 検証期間の対数損失、(b) 検証期間の回収率で選び、テスト期間で比べる。仮説: (b) はテスト期間の回収率の分散が大きく、平均でも (a) を安定して上回らない。
- **馬ごとの異質性**: フレイルティ（ランダム効果）は、馬の能力の個体差を条件付きロジットに入れる方法の一つ。keiba-ai では馬 ID の目的変数エンコーディングや階層ベイズ（[Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md), [Nakakita 2023](./2023-nakakita-hierarchical-bayes-horse-jockey.md)）と比べる候補。

## 関連ノート

- [Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md): 同じ著者の香港競馬の階層ベイズモデル。
- [Benter 2019](./2019-benter-model.md): 条件付きロジットによる勝率推定の原型。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 競馬への条件付きロジットの最初期の適用。
- [Nakamura 2016](./2016-nakamura-keiba-l1-logit.md): L1 正則化付きロジットを日本の競馬に適用した研究。
- [Nakakita 2023](./2023-nakakita-hierarchical-bayes-horse-jockey.md): 本論文を引用し、馬と騎手の能力を階層ベイズで推定。
- [Chapman 1994](./1994-chapman-hong-kong-2000-races.md): 香港競馬での条件付きロジットの先行研究。

## 検索語

条件付きロジット, 条件付きロジスティック回帰, フレイルティ, ランダム効果, Cox 比例ハザード, LASSO, L1 正則化, 罰則付き尤度, 利益最大化, 巡回座標降下法, GPU, 並列計算, 香港競馬, ホールドアウト, 投資収益率, ROI, conditional logistic regression, frailty, regularization, cyclical coordinate descent, Hong Kong, Journal of Prediction Markets

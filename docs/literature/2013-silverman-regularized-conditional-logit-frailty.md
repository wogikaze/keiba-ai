---
title: Predicting Horse Race Winners through a Regularized Conditional Logistic Regression with Frailty
authors: Silverman Noah, Suchard Marc A.
year: 2013
venue: Journal of Prediction Markets 7(1) 43-52
url: https://econpapers.repec.org/RePEc:buc:jpredm:v:7:y:2013:i:1:p:43-52
doi: 10.5750/jpm.v7i1.595
topic: machine-learning
tags: conditional-logit, regularization, frailty, gpu, hong-kong, betting-simulation, lasso, offset
verified: fulltext
importance: medium
source: downloaded
source_version: dissertation
---

# 条件付きロジットに配当由来の「フレイルティ」と利益最大化の LASSO を入れた香港競馬モデル

> 一言で: 条件付きロジット（レース内ソフトマックス）の線形予測子に、配当 $d$ から作った固定の項 $\omega = 1 - 1/d$ を足し（著者は「逆フレイルティ」と呼ぶ）、186 個の過去成績変数に L1 罰則をかけ、罰則の強さ λ を**ホールドアウトの回収率が最大になるように**選んだ。香港 3,681 レースで、Benter 型の二段階モデルの ROI 14.2% に対し 36.73% を報告。λ をテスト集合の ROI で選んでおり、分割もランダムなので、この数字は楽観的に偏っている。

## 原本について

雑誌版（JPM, ubplj.org）は購読者限定で取れなかった。代わりに、第一著者の UCLA 博士論文 *Optimal Decisions with Multiple Agents of Varying Performance*（2013, eScholarship で公開）を取得した。その第3章が本論文と同じ題名・同じ要旨（3,681 レース、ROI 36.73%）で、著者の業績欄にも本論文の掲載が記されている (PDF p.13)。雑誌版との細部の違いは未確認。共著者 Suchard の名は博士論文の章には出ない。

以下のページ番号は博士論文の印刷ページ（第3章は pp.22–33。PDF のページは +13）。

## モデル (pp.24–29)

### 出発点: 条件付きロジットと二段階モデル

レース $r$ の馬 $h$ の勝率を $p_{rh} = e^{X_{rh}\beta} / \sum_{h' \in r} e^{X_{rh'}\beta}$ とする標準的な条件付きロジット (式3.4, p.24)。L1 罰則つきの対数尤度は $\sum_r [X^w_{r}\beta - \log\sum_h e^{X_{rh}\beta}] - \lambda\sum_k|\beta_k|$ (式3.7, p.25)。

既存研究（Bolton & Chapman 1986, Benter 1994, Edelman 2007, Lessmann ら 2007/2009）は、第1段で馬の「強さ」$\alpha$ を何らかの方法で推定し、第2段でそれとオッズの暗黙確率を条件付きロジットで結合する (式3.8, pp.25–26)。各研究の違いは第1段の推定法（条件付きロジット、SVR、SVM、CART）だけだと整理している (p.26)。

### 「逆フレイルティ」の項 (pp.27–28)

Cox 比例ハザードモデルのフレイルティ（個体ごとの感受性 $\omega$）を借りて、線形予測子に $\omega_{rh}$ を足す (式3.9)。その中身は確定配当 $d_{rh}$ から

$$\omega_{rh} = 1 - \frac{1}{d_{rh}}$$

で決める (式3.10)。配当が高い（人気のない）馬ほど $\omega$ が大きい。著者はこれを「大衆が勝つと思っていない馬ほど高く評価する、逆フレイルティ」と説明する (p.27)。

> By setting our strength(frailty) as the opposite of public confidence, we are looking for those horses we have a high confidence of winning that also pay high dividends. (p.28)

$\omega$ には係数がなく、推定されない固定のオフセットである。旧ノートは「フレイルティの中身（馬ごとのランダム効果か）は未確認」としていたが、原本ではランダム効果ではなく配当の決定論的な変換だった。

最終的な目的関数は $\sum_r [X^w_r\beta + \omega^w_r - \log\sum_h e^{X_{rh}\beta+\omega_{rh}}] - \lambda\sum_k|\beta_k|$ (式3.13, p.28)。原文では罰則の符号が $+\lambda$ と書かれているが、文脈からは最大化する対数尤度から引くのが正しい（誤植と思われる）。

### λ の選び方 (pp.28–29)

ランダムに 20% をテストに取り分ける 10 分割の交差検証を、λ の 100 通りの値それぞれで行い、テスト部分の平均 ROI が最大の λ を選ぶ (式3.16, p.29)。

> Ultimately, the goal of this process is not to predict winners with the most accuracy, but to maximize profit (p.28)

### 計算 (pp.29–31)

巡回座標降下法（CCD）を C++ と Thrust で GPU 上に実装。約 4 万行 × 186 変数（2次の展開を入れると 36,100 変数）を 1,000 回当てはめる (p.29)。1回の当てはめが GPU で 494 ms、OpenMP では 1 スレッド 3,995 ms、8 スレッド 1,324 ms で、GPU は最良の OpenMP より 2.68 倍速い (p.31)。

## データと結果 (pp.30–31)

- 香港ジョッキークラブの公式記録 3,681 レース。2,944 レースで学習、737 レースをテスト (p.30)。要旨では「4 年分で学習しホールドアウトで検証」(p.23) と書くが、本文の手順はランダムな 20% の取り分けで、時系列のホールドアウトではない。旧ノートで「長所: 時系列のホールドアウト」と書いた点は、原本の手順の記述と合わない。
- 変数は各馬の過去成績 186 個（前走からの休養日数、負担重量の変化、過去の平均速度、馬体重の増減など）(p.30)。
- 賭け方: モデル確率 × 配当 > 1 の馬すべてに賭ける (p.31)。賭け金の大きさ（定額か比例か）は書かれていない。
- 結果:

| モデル | ROI | 備考 |
|---|---|---|
| Benter 型の二段階条件付きロジット | 14.2% | ベースライン (p.31) |
| 提案（逆フレイルティ + L1, λ=7） | 36.73% | λ を 1〜100 で振った最大値 (p.31) |
| 提案 + 各変数の2乗 | 36.73% 未満 | 数値なし (p.31) |

- Figure 3.1 (p.33) は λ に対する平均 ROI の曲線（提案と Benter の2本）。ROI は λ によって −0.2 から 0.3 超まで大きく動く。
- 著者は大衆の推定確率と真の勝率の相関が「約 40%」と書く (p.27) が、どう計算したかは説明がない。

## 批判的に読む

- **λ をテスト集合の ROI で選んでいる**。100 通りの λ から ROI 最大のものを選び、その ROI をそのまま成績として報告している。選択とは別の評価期間がなく、36.73% は「最良の設定の事後的な成績」で、将来の期待値ではない。[Bailey 2014](./2014-bailey-deflated-sharpe-ratio.md) の言う選択バイアスの典型。
- **ランダム分割**。同じ馬や同じ開催日のレースが学習とテストの両方に入る。過去成績の特徴量の作り方によっては将来の情報が漏れる。
- **確定配当を入力に使う**。$\omega$ も賭けの判定（確率 × 配当 > 1）も確定配当を使う。締切前に買う時点では確定配当は分からない。香港の大口の賭けは最終オッズを動かす。
- **逆フレイルティの効果は、大穴に賭けを寄せる操作でもある**。$\omega$ は配当が大きいほど勝率を押し上げるので、確率 × 配当 > 1 の判定を通る馬は大穴側に偏る。香港は本命-大穴バイアスが弱い（Busche & Hall 1988）とされる市場なので、この偏りが利益につながったのか、テスト 737 レース中の少数の高配当で決まったのかは、本文の情報では区別できない。的中数や配当の分布は報告されていない。
- **統計的有意性の検定がない**。「significant improvement」(p.31) と書くが、検定や信頼区間は示されていない。
- **ベースラインの Benter 型モデルの詳細**（第1段の変数、第2段の当てはめ方）も書かれていない。

## keiba-ai での使い方

- **正則化つき条件付きロジットを強いベースラインに**: 186 変数程度の過去成績特徴量なら、L1 つきのレース内ソフトマックスで十分に戦える。GBDT や NN の前に置く。
- **市場情報をオフセットとして入れる設計**: 本論文は配当の変換を係数なしのオフセットとして足した。keiba-ai では、市場確率の対数を係数つき（Benter 型）で入れる、係数1のオフセットで入れる（モデルは市場からの残差を学ぶ）、入れない、の3通りを比べる価値がある。ただし本論文の $1-1/d$ のように「人気薄ほど押し上げる」符号の固定は、理論的な裏付けがないので採らない。
- **実験案（仮説）**: 正則化の強さを (a) 検証期間の対数損失、(b) 検証期間の回収率で選び、別のテスト期間で回収率を比べる。仮説: (b) は検証期間では高く見えるが、テスト期間では (a) を安定して上回らない。本論文の 36.73% は (b) を同じ集合で選んで評価した数値なので、この実験で「選択と評価を分けると何が残るか」を測る。
- **評価の書き方**: 回収率を報告するときは、選択に使った候補の数、的中数、最大配当の寄与（最高配当1件を除いた回収率）を併記する。

## 関連ノート

- [Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md): 同じ著者の香港競馬の階層ベイズモデル（博士論文の第2章に対応）。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 競馬への条件付きロジットの最初期の適用。本論文が二段階モデルの起点として挙げる。
- [Benter 2019](./2019-benter-model.md): 二段階の条件付きロジット。本論文のベースライン。
- [Edelman 2007](./2007-edelman-svm-horserace-odds.md): 第1段を SVR にした二段階モデル。本論文が先行研究として整理。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md)、[Lessmann 2009](./2009-lessmann-svm-classification-horserace.md): 第1段を SVM 系にした二段階モデル。
- [Nakamura 2016](./2016-nakamura-keiba-l1-logit.md): L1 正則化つきロジットを日本の競馬に適用。
- [Chapman 1994](./1994-chapman-hong-kong-2000-races.md): 香港競馬での条件付きロジットの先行研究。
- [Busche & Hall 1988](./1988-busche-exception-risk-preference.md): 香港では本命-大穴バイアスが弱いという報告。逆フレイルティの効果を解釈する背景。
- [Nakakita 2023](./2023-nakakita-hierarchical-bayes-horse-jockey.md): 本論文を「Cox 比例ハザードに着想を得たパラメータ」を入れた研究として引く。
- [Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md): 参考文献に挙げる「Optimal Decision with Multiple Agents of Varying...」は、本ノートが原本として使った博士論文そのもの。
- [Bailey 2014](./2014-bailey-deflated-sharpe-ratio.md): 多数の設定から最良を選んだ成績の割り引き。本論文の λ 選択の評価に必要。

## 検索語

条件付きロジット, 条件付きロジスティック回帰, conditional logistic regression, CLR, フレイルティ, frailty, 逆フレイルティ, reverse frailty, オフセット, offset, 配当, dividend, Cox 比例ハザード, Cox proportional hazards, LASSO, L1 正則化, 罰則付き尤度, 利益最大化, profit maximization, 巡回座標降下法, cyclical coordinate descent, CCD, GPU, CUDA, Thrust, OpenMP, 並列計算, 香港競馬, Hong Kong Jockey Club, 二段階モデル, two-stage model, Benter, 交差検証, cross validation, 投資収益率, ROI, 選択バイアス, Journal of Prediction Markets, Silverman, Suchard, UCLA 博士論文

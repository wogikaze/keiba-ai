---
title: Adapting support vector machine methods for horserace odds prediction
authors: Edelman David
year: 2007
venue: Annals of Operations Research 151 325-336
url: https://link.springer.com/article/10.1007/s10479-006-0131-7
doi: 10.1007/s10479-006-0131-7
topic: machine-learning
tags: svm, svr, two-stage-model, conditional-logit, market-odds, australia
verified: abstract
importance: high
source: unavailable
source_version: none
---

# 二段階モデルの第1段を SVR にした最初の競馬研究（オーストラリア、学習200・評価100レース）

> 一言で: Benter 型の二段階モデル（ファンダメンタル情報から作るスコアと市場オッズを条件付きロジットで結合）の第1段を、RBF カーネルの SVR による「正規化着順の回帰」に置き換えた。小規模なオーストラリアのデータで有望な結果を報告し、後の Lessmann らの一連の研究の出発点になった。

**原本未取得。** Springer は有料。OpenAlex に載る別版のリンクも Springer に解決し、ResearchGate は「Request PDF」のみ、著者所属の UCD Research Repository にも収録がなかった。以下は出版社ページの要旨と、全文を取得済みの後続論文での引用に基づく。数値は要旨にあるもの以外は未確認。

## 書誌について

- 掲載: Annals of Operations Research 151巻 325-336頁（2007年4月号）。オンライン公開は2006年11月10日。そのため後続論文は「Edelman (2006)」と引くことがある（[Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md) など）。
- 前身は 2003年6月の第12回 International Conference on Gambling and Risk Taking（バンクーバー）での発表で、[Sung 2007](./2007-sung-two-step-conditional-logit.md) は「Edelman (2003)」として同名の発表を引いている（同ノート原本の参考文献, p.17）。Semantic Scholar などが年を2003年とするのはこのため。
- 著者所属: University College Dublin（Banking & Finance）。

## 要旨から分かること

- SVM の方法論を素直に拡張し、競馬の着順のような「層別された結果（stratified outcomes）」を扱えるようにした。
- 比較的小さいオーストラリアのデータで学習（200レース）し、別の100レースで評価した。
- 入力変数が比較的多い（12個）ことを考えると、結果は有望だったと述べる。

## 後続論文が伝える手法

- 第1段: SVR で各馬の**正規化着順**を回帰する。RBF カーネルを使った（[Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md), p.173）。勝ち／負けの分類ではなく回帰にする理由は、着順全体の情報を使えるからだと Edelman は論じた（同, p.170）。
- 第2段: 第1段のスコアと市場オッズ由来の確率を条件付きロジットで結合し、勝率を出す（同, p.177）。
- Benter (1994) の第1段（重回帰）を SVR に置き換えた形（同, p.177）。
- SVR に**レースごとの切片 $b_j$** を入れ、レース単位の層別分析にした（[Lessmann 2009](./2009-lessmann-svm-classification-horserace.md) 原稿 PDF p.66）。要旨の「層別された結果」はこの工夫を指すと思われる（推測）。
- データは「1995年の300レース」と説明されている（同 p.68）。要旨の学習200・評価100レースと合計が一致する。多数の相関した入力に頑健である点が SVM 系を使う理由として挙げられている（同, p.177-178）。
- 二次資料の一部（Silverman 2012, JPM 6(1)）は、Edelman の入力が「前走のオッズ、前走の結果と条件、今回の条件」に限られると説明している。ただし同論文は本リポジトリに原本が無く、未確認。

## 批判的に読む（要旨と二次資料から言えること）

- 評価100レースは非常に小さい。回収率の数値や統計的検定の有無は未確認。
- 第1段を回帰にすると、後方の着順（賞金がなく、追わないことがある）のノイズまで学習する。[Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md) はこれを問題視し、超パラメータ選択を NDCG に替えた。[Lessmann 2009](./2009-lessmann-svm-classification-horserace.md) は第1段を分類に戻す方向を試している。
- 学習と評価が時系列で分かれているか、超パラメータをどう選んだかは未確認。
- Lessmann ら (2009) は Goodwood のデータで「素の SVR（層別切片なし）」を SVR/CL として再現し、保有外156レースで Kelly 回収率 17.50% を報告している（同 PDF p.83, Table 3）。これは Edelman の原データ・原手法での数値ではない。

## keiba-ai での使い方

- **二段階構成の基本形**: 「機械学習でファンダメンタル・スコアを作り、そのスコアと市場確率 $\ln q$ を条件付きロジットで結合する」。第1段の学習器は LightGBM にそのまま置き換えられる。第1段にオッズを入れないことで、市場が見落としている情報だけをスコアに残す狙い。
- **実験案**: 第1段の目的変数を (a) 正規化着順の回帰、(b) 勝ち2値、(c) 3着以内2値、(d) レース内 softmax の4通りにし、第2段（市場確率との結合）後の対数損失と回収率を比べる。仮説: 後方着順のノイズを含む (a) は (c)(d) より悪い。
- 本論文は原本未取得なので、keiba-ai の設計根拠として引くときは Lessmann らの記述を一次情報として扱う。

## 関連ノート

- [Benter 2019](./2019-benter-model.md): 二段階モデルの原型。本論文はその第1段を置き換えた。
- [Sung 2007](./2007-sung-two-step-conditional-logit.md): 一段階と二段階の条件付きロジットを比較。本論文の2003年版を引く。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md): 本論文の SVR/CL を LS-SVR にし、超パラメータを NDCG で選ぶよう改良。
- [Lessmann 2009](./2009-lessmann-svm-classification-horserace.md): 本論文の SVR/CL を比較対象にした SVM 分類版。
- [Lessmann 2010](./2010-lessmann-random-forest-horserace.md), [Lessmann 2012](./2012-lessmann-stacking-competitive-event.md): 同じ系譜の後続。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 第2段の条件付きロジット。
- [Nakakita 2023](./2023-nakakita-hierarchical-bayes-horse-jockey.md), [Saigusa 2018](./2018-saigusa-combination-ranking.md): 本論文を引用している日本の研究。

## 検索語

サポートベクターマシン, SVM, サポートベクター回帰, SVR, RBF カーネル, 二段階モデル, 条件付きロジット, 市場オッズ, ファンダメンタル, 正規化着順, オーストラリア競馬, Benter, two-stage model, conditional logit, stratified outcomes, horserace odds prediction, Annals of Operations Research

---
title: A Systematic Review of Machine Learning in Sports Betting: Techniques, Challenges, and Future Directions
authors: Galekwa René Manassé, Tshimula Jean Marie, Tajeuna Etienne Gael, Kyamakya Kyandoghere
year: 2024
venue: arXiv preprint arXiv:2410.21484
url: https://arxiv.org/abs/2410.21484
doi: 10.48550/arXiv.2410.21484
topic: machine-learning
tags: survey, sports-betting, horse-racing, roi, evaluation-metrics
verified: fulltext
importance: medium
source: downloaded
source_version: preprint
---

# スポーツベッティングにおける機械学習の系統的レビュー（競馬の節は薄く、批判的な評価もない）

> 一言で: 2010年1月〜2024年7月の 219 本を、サッカーからホッケーまで10競技に分けて紹介した 63 ページのレビュー。競馬の節（4.7）は数本の紹介と要約表（Table 9）だけで、93% のような正解率を検証せずに並べている。keiba-ai には、文献の索引として以外の使い道は少ない。

ページは PDF のページ番号（library の `=== page N ===`）で書く。

## レビューの方法

- 研究課題は3つ（p.2, Table 1）。
  - RQ1: ML で試合結果を予測し、利益を最大化できるか
  - RQ2: ML の適用にはどんな課題と限界があるか
  - RQ3: ML で、金融のポートフォリオ管理のように適応的な「賭けのポートフォリオ」を作れるか
- 検索先は IEEE Xplore、Springer、ScienceDirect、MDPI、arXiv、Google Scholar。キーワードは "machine learning" "sports betting" "odds estimation" "value betting" に競技名を組み合わせたもの（p.3）。
- 2010年1月〜2024年7月の査読論文・会議論文・プレプリントを対象にした。259本から包含基準で 219本に絞った（p.3）。PRISMA に従ったとする（p.3, Figure 1）。
- 抽出した項目: 書誌、アルゴリズム、データセット、指標（accuracy、precision、recall、RPS）、主な結果と限界（p.3）。

## 競馬の節（4.7, p.32–35）で取り上げた研究

| 研究 | レビューでの要約 | 本リポジトリのノート |
|---|---|---|
| Terawong & Cliff 2024 | 取引所のエージェントモデル（BBE）で XGBoost に賭け方を学ばせ、元の戦略より利益が出た | [Terawong 2024](./2024-terawong-xgboost-in-play-betting-exchange.md) |
| Gupta & Singh 2024 | インドの競馬会社のデータ 14,750行・56属性。RF の正解率 93.1% | なし |
| Tondapu 2024 | Betfair の英国競馬の時系列。価格変化の自己相関はすぐ消え、情報効率は高い | なし |
| Lessmann ら 2010 | 香港 1,000レース。RF を競走向けに改良し、条件付きロジットや SVM より高い利益 | [Lessmann 2010](./2010-lessmann-random-forest-horserace.md) |
| Selvaraj 2017 | Sporting Life と Kaggle の2データ。2つ目で k-NN 91.4%、LDA 92%、ロジスティック 89.58% | なし |
| Borowski ら 2021 | ポーランド 3,782レース。単勝の的中率 41%、市場の非効率を示唆 | [Borowski 2021](./2021-borowski-ml-flat-racing-poland.md) |
| Pudaruth ら 2013 | Champ de Mars の 2010年 240レース。重み付き確率で的中率 58%、予想家平均 44% | なし（同グループの [Pudaruth 2015](./2015-pudaruth-ann-champs-de-mars.md)） |
| Jogeeah ら 2015 | Champ de Mars でファジィ論理、正解率 75% | なし |
| Gulum 2018 | 対戦グラフの特徴量で ANN とロジスティック回帰の精度が上がった | [Gulum 2018](./2018-gulum-graph-features.md) |
| Davoodi & Khanteymoori 2010 | Aqueduct の 2010年1月 100レース。ANN の学習法5種、BP が1着予測で 77% | [Davoodi 2010](./2010-davoodi-ann-horse-racing.md) |

議論の節は、競馬について Terawong & Cliff の利益だけを取り上げ、ML が競馬の賭けを「変革する」可能性を示すと書く（p.48）。

## 課題と今後（8–9節）

- 課題として、データの量と質、競技の変化（怪我・戦術）、過学習、特徴量選択、倫理（八百長検知・情報格差）、計算資源、規制を挙げる（p.52–53）。どれも一般論で、競馬に固有の論点（控除率、パリミュチュエルのオッズ変動、FLB）は出てこない。
- RQ3 の答えとして、賭けを資産とみなしたポートフォリオ管理（現代ポートフォリオ理論、Black–Litterman）を提案する（p.53–54）。具体的な定式化や実験は無い。

## 批判的に読む

- **報告値を検証していない。** 競馬の1着予測で正解率 90% 台はありえない。2値分類で負例が多いだけか、リークか、課題の定義が違うかのどれかだが、レビューはそのまま「優れた性能」として表と図（Figure 15）に並べている。系統的レビューに必要な質の評価（バイアスのリスク評価）が無い。
- **方法の記述に矛盾がある。** 本文は「259本から219本」（p.3）だが、PRISMA の図では登録件数が 350件で、数が合わない（p.4, Figure 1）。除外基準に「ML の手法に焦点を当てた研究」が入っているのも（p.3）、レビューの趣旨と食い違う。
- **要約の誤り。** Table 9 では Gulum 2018 を SVM の行に置き、データを「UK racetrack, Equibase」とし、指標に回収率や t 値を並べている（p.33）。Gulum の要旨は ANN とロジスティック回帰で、英国のデータの話は無い。他の論文の要素が混ざっているように見える。
- **競馬の主要文献が抜けている。** Benter、Bolton & Chapman、条件付きロジットの系統、市場効率性・FLB の研究にほとんど触れない。2010年以降に限ったためもあるが、競馬の ML を評価するうえで要になる「市場オッズとの比較」という観点が欠けている。
- 回収率の計算方法（実オッズか、控除率込みか）を、研究どうしで比べていない。

## keiba-ai での使い方

- **索引として使う。** 他競技（サッカーの RPS、テニスの階層マルコフモデル、Kelly とポートフォリオ）の文献を探す入口になる。競馬の文献は、本リポジトリのノートの方が詳しい。
- **反面教師。** 文献を引くときは、正解率の定義（馬単位の2値か、レース単位の本命1着率か）、市場との比較の有無、回収率の計算法を確かめてから数値を使う。keiba-ai の文献ノートでも、この3点を必ず書く。
- RQ3 の「賭けのポートフォリオ」は、すでに Kelly 系の文献（複数の排反な賭けへの配分）で具体的に扱われている。そちらを使う。

## 関連ノート

- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 本レビューも引く、正解率よりキャリブレーションでモデルを選ぶべきという研究。本レビューの評価の弱さを補う。
- [Hubáček 2019](./2019-hubacek-exploiting-betting-market-ml.md): 市場オッズとの相関を抑えて利益を出す ML。レビューの「value betting」の具体例。
- [Uhrin 2021](./2021-uhrin-optimal-sports-betting-review.md): スポーツベッティングの最適な賭け方のレビュー。RQ3 の内容をより具体的に扱う。
- [Whitrow 2007](./2007-whitrow-simultaneous-bets-allocation.md): 同時に複数の賭けへ資金を配分する問題。ポートフォリオ型の賭けの先行研究。
- [Terawong 2024](./2024-terawong-xgboost-in-play-betting-exchange.md), [Borowski 2021](./2021-borowski-ml-flat-racing-poland.md), [Lessmann 2010](./2010-lessmann-random-forest-horserace.md), [Gulum 2018](./2018-gulum-graph-features.md): 競馬の節で取り上げられた研究。
- [Colle 2022](./2022-colle-what-ai-can-do-horse-racing.md): 競馬の AI の展望論文。

## 検索語

系統的レビュー, systematic review, サーベイ, survey, PRISMA, スポーツベッティング, sports betting, 機械学習, machine learning, バリューベット, value betting, オッズ推定, odds estimation, ポートフォリオ, betting portfolio, 現代ポートフォリオ理論, Black-Litterman, 八百長検知, match-fixing, anomaly detection, 競馬, horse racing, サッカー, テニス, クリケット, 正解率, accuracy, RPS

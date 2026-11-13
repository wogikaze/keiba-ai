---
title: Parimutuel system of the Japanese race track: Voting and ranking process
authors: Tutiya Yohei, Kurihara Kazutaka
year: 2015
venue: The Journal of Gambling Business and Economics 9(2) 27-39
url: https://www.ubplj.org/index.php/jgbe/article/view/986
doi: 10.5750/jgbe.v9i2.986
topic: market-efficiency
tags: japan, jra, odds-dynamics, parimutuel, late-betting
verified: abstract
importance: medium
source: unavailable
source_version:
---

# 日本の競馬の発売中オッズ（投票率）の時系列を主成分分析・クラスタ分析で分類する

> 一言で: 日本の競馬の締切前オッズの時系列を大量に集め、主成分分析とクラスタ分析でレースを分類すると、最も効く要因は「1番人気への期待の高さ」だった。締切直前に本命へ票が集中するかも調べている。

**原本未取得。** 出版社（University of Buckingham Press の JGBE）の全文 PDF は購読者向けか有料（GBP 25）で、OpenAlex・RePEc・researchmap・著者サイト・arXiv に無料版は見つからなかった（2026年11月確認）。本ノートは出版社ページと RePEc の要旨、および著者らの後続研究の要旨に基づく。数値は一つも確認できていない。

## 要旨から分かること

出版社ページと RePEc の要旨によると:

- 対象は日本の競馬のパリミュチュエル方式における**投票率（betting rates）の時系列**。
- 主成分分析とクラスタ分析で、レースを分類する最も重要な要因は**本命（1番人気）への期待の水準**だった。
- 使った締切前オッズのデータは、先行研究と比べて「非常に大きく詳細」だと著者は述べる。
- 本命への賭けが締切直前に集中する傾向があるかも詳しく調べている。
- キーワード: pari-mutuel system, time series of odds, FL bias, principal component analysis, cluster analysis, horse-racing。

## 未確認の点

- 中央（JRA）か地方か、期間、レース数、オッズの取得間隔。タグの `jra` は旧ノートからの引き継ぎで、根拠は未確認。
- 主成分の解釈と寄与率、クラスタ数、各クラスタの形（例: 本命の投票率が締切に向けて上がるか下がるか）。
- 「締切直前に本命へ票が集中するか」の答え。要旨は結論を書いていない。
- FLB との関係をどう論じたか（キーワードに FL bias があるので何らかの議論はあるはず。推測）。

## 後続研究との関係

同じ著者による arXiv 1805.04225 "Efficiency in Micro-Behaviors and FL Bias"（2018, のち JGBE 14(2), 2021 に "Efficient Micro-Behaviors in Pari-mutuel Betting System and FL Bias" として掲載）は、締切に向けて投票量が急増するという仮定の下で、期待値最大化を目指す賭け手の行動がオッズ分布をどう作るかをシミュレーションしている。そこでは締切前の投票量の推移 $F(t)$ を公開している競馬場がほとんど無いため香港のデータを基準にパラメータを置いている。本論文の日本のオッズ時系列データとの関係は、その原本からは確認できなかった。

## keiba-ai での使い方

原本を読めていないので、以下は要旨から立てた仮説にとどまる。

- **時系列オッズの特徴量化**: 単勝投票率の時系列を主成分に分解して「1番人気の期待水準」「締切前の動き」の軸を作る、という発想は、時系列オッズを取得できる場合の特徴量設計の候補になる。最終オッズだけを使うモデルとの比較で、締切前の動きに追加の情報があるかを検証する。
- **レースの類型化**: 「1番人気が抜けたレース」と「混戦」でオッズ→勝率の校正や FLB の強さが違うかを見る。仮説: 1番人気の投票率が高いレースほど FLB の形が違う。実験では、1番人気の単勝投票率の分位でレースを層別し、層ごとに市場確率の校正曲線を描く。
- 締切直前の投票の集中は [Hanyu et al. 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md) が JRA データで直接扱っているので、実験の設計はそちらを主に参照する。

## 関連ノート

- [Hanyu et al. 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): JRA の締切直前の投票の動きと最終オッズの情報量。主題が最も近い。
- [Sugawara and Mori 2025](./2025-sugawara-ornstein-uhlenbeck-horse-betting.md): 投票の時系列を OU 過程でモデル化。日本のオッズ時系列の別の分析。
- [Mori and Hisakado 2010](./2010-mori-independent-herding-betters.md): 日本の競馬で独立な賭け手と群集行動の賭け手を区別する研究。
- [Asch et al. 1982](./1982-asch-racetrack-informed-behavior.md): 締切直前の賭けほど情報を含むという古典的な実証。
- [Ottaviani and Sørensen 2010](./2010-ottaviani-noise-information-flb.md): 締切直前の同時手番を前提にした FLB の理論。
- [Ichinomiya 2006](./2006-ichinomiya-power-law-odds.md): 日本の競馬オッズ分布のべき則。

## 検索語

パリミュチュエル, pari-mutuel, parimutuel, 投票率, betting rate, オッズの時系列, time series of odds, 発売中オッズ, 締切前オッズ, 締切直前の投票, late betting, 主成分分析, principal component analysis, PCA, クラスタ分析, cluster analysis, 本命, favorite, 1番人気, FLB, favorite-longshot bias, 日本の競馬, Japanese race track, 土谷洋平, 栗原一貴, Tutiya, Kurihara, JGBE

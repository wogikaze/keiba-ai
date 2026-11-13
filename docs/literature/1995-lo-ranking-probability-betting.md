---
title: The Application of Ranking Probability Models to Racetrack Betting
authors: Lo Victor S. Y., Bacon-Shone John, Busche Kelly
year: 1995
venue: Management Science 41(6) 1048-1059
url: https://pubsonline.informs.org/doi/10.1287/mnsc.41.6.1048
doi: 10.1287/mnsc.41.6.1048
topic: probability-models
tags: ordering-probability, place-show-betting, hzr-system, discount-model
verified: abstract
importance: medium
source: unavailable
---

# 着順確率モデルを複勝・3着内の賭け（HZR システム）に組み込む

> **原本未取得。** Management Science の有料論文。HKU の機関リポジトリ（hdl 10722/86411）は取得できず、合法な無料版が見つからなかった。本ノートは出版社の要旨と、本論文（およびその研究報告版）を引用する後続論文（Ali 1998、芦谷 2010、Benter 1994。いずれも library に原本あり）に基づく。

> 一言で: Hausch-Ziemba-Rubinstein（HZR）の複勝・3着内（place/show）ベッティングシステムは、2・3着確率を Harville 公式で計算する。これを Henery/Stern に近い当てはまりを持つ Lo & Bacon-Shone の簡単な割引モデルに置き換え、米国・香港・日本のデータで比べた。米国と香港では低いリスクで利益が改善し、日本では差がほとんどなかった。

## 要旨から分かること

- Henery と Stern のモデルは Harville より当てはまりが良いが、着順確率の計算がはるかに複雑になる。
- Lo & Bacon-Shone の簡単なモデルは、Henery と Stern の確率をよく近似し、当てはまりも同等。
- これを HZR システムと組み合わせ、香港、Meadowlands（米国）、日本のデータで検証した。

## データ（研究報告版からの孫引き）

Ali (1998) によれば、Lo, Bacon-Shone & Busche の研究報告（1994, 香港大学 Research Report 18、本論文の前身と思われる）は HZR システムとその変種を次のデータに適用した (Ali p.228)。

| 市場 | 期間 | レース数 |
|---|---|---|
| Meadowlands（米国 NJ） | 1984 | 705 |
| 香港 | 1981–82 | 905 |
| 日本 | 1990–91 | 983 |

Ali の要約では「どの場合も HZR システムは負の利益だった」。これと本論文要旨の「割引モデルで利益が改善」は矛盾しない（Harville 版 HZR は赤字、割引版で改善）が、割引版が黒字になったかどうかは**未確認**。

## 主張と留意点

- 芦谷 (2010) の要約: Harville の公式を精緻化すれば期待収益率が向上することを示した。ただし著者自身、HZR 型の投資戦略は 1987〜89 年の解説書の刊行後に広く使われるようになり、収益機会は減っているかもしれないと述べている（Lo et al. 1995, p.1051 からの引用として、[芦谷 2010](./2010-ashiya-longshot-bias-survey.md), PDF p.5）。
- Benter (1994) は、2・3着の割引パラメータの値は競馬場ごとに大きく違い、本研究（報告版）は Benter の香港データ（$\gamma=0.81,\delta=0.65$）とかなり違う値を得たと注記する（[Benter 1994](./2019-benter-model.md), PDF p.12）。
- 回収率の具体値、割引パラメータの推定値、評価が最終オッズによる事後計算か（オッズの変化を考慮したか）は**未確認**。要旨の検索結果では、最終オッズを使い取引コストはゼロと仮定したとされる。

## 批判的に読む

- **最終オッズでの評価**: 複勝・3着内の HZR システムは、締切直前のプール状況を見て賭ける前提。最終オッズで事後評価すると、実際に賭けたときより有利になりうる。自分の賭けがプールを動かす効果も、複勝プールは小さいので無視できない。
- **日本で差が小さかった理由**: 未確認。日本の複勝は払戻の計算方法（同着や3着内の配分）が北米の show と違うことが関係する可能性がある（推測）。
- **市場の変化**: 著者が認めるとおり、手法が広まると機会は消える。データは 1980 年代〜1990 年代初め。

## keiba-ai での使い方

- **複勝・ワイドの期待値計算**: 単勝確率→着順確率の変換を Harville から割引モデルに替えたとき、複勝の期待値がプラスになる馬の数と、実際の回収率がどう変わるかを JRA データで調べる。本論文の日本での「差が小さい」という結果を、現在の JRA で再検証する形になる。
- **仮説**: 「Harville は人気馬の複勝確率を過大評価するため、Harville で選んだ『割安な人気馬の複勝』は実際には割安でない。割引モデルにするとその買い目が減り、回収率の損失が縮む」。
- **評価の注意**: 複勝オッズは発売中に大きく動き、確定オッズは幅（下限〜上限）で示される。どの時点・どの値で評価するかを実験設定に明記する。

## 関連ノート

- [Hausch, Ziemba & Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): HZR システムの原典。
- [Hausch & Ziemba 1985](./1985-hausch-transactions-costs-multiple-wagers.md): 取引コストと複数賭けを入れた HZR の拡張。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較。
- [Lo 1994](./1994-lo-running-time-japan.md): 日本のデータでの走破時間分布モデル。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): 割引近似の詳細。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 研究報告版の結果を引用し、順位モデルでは利益は出ないと主張。
- [Benter 1994](./2019-benter-model.md): 同型の補正を香港で推定。
- [Hausch, Lo & Ziemba 1994](./1994-hausch-pricing-exotic-wagers.md): 連勝式への価格付けの応用。

## 検索語

複勝, place, show, 3着内, HZR システム, Hausch-Ziemba-Rubinstein, Dr. Z システム, 着順確率, ranking probability, ordering probability, 割引モデル, discount model, Harville 公式, Henery, Stern, 香港, Meadowlands, 日本, JRA, ベッティングシステム, betting system, 回収率, 市場効率性

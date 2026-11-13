---
title: Probability and Statistical Models for Racing
authors: Lo Victor S. Y., Bacon-Shone John
year: 2008
venue: Journal of Quantitative Analysis in Sports 4(2) Article 11
url: https://www.degruyter.com/document/doi/10.2202/1559-0410.1103/pdf
doi: 10.2202/1559-0410.1103
topic: probability-models
tags: review, favourite-longshot-bias, ordering-probability, running-time-distribution, discount-model
verified: abstract
importance: high
source: unavailable
source_version: published
---

# 競馬の確率・統計モデルのレビュー：本命大穴バイアスと着順確率

**原本未取得。** OpenAlex に OA 版の記録がなく、De Gruyter と SciSpace はボット検査、著者アップロード版（ResearchGate）は 403、academia.edu はログインが必要で、合法に取れる経路がなかった。本ノートは要旨と検索結果に出た本文の断片、他論文での引用に基づく。数値は確認できていない。

> 一言で: 本命大穴バイアス（FLB）を各国データで統計モデル化して「普遍的ではない」ことを示し、走破時間分布から2・3着の確率を作るモデル（Harville、Henery、Stern、discount 近似）の実証をまとめたレビュー（要旨より）。

## 扱う2つの問題

要旨によれば、競馬データは多頭数の競争を定量的に研究する材料として豊かで、本論文は2つの問題を扱う。

1. **本命大穴バイアス**: 世界各地の競馬データで、勝率とオッズの関係を統計的にモデル化する。バイアスは普遍的ではなく、効用理論による経済学的解釈も与える。
2. **着順確率**: 走破時間分布に基づいて2着・3着の確率を予測する。馬単・3連単（exacta, trifecta）の評価に直結する。第3節で Lo (1994a) と Bacon-Shone, Lo and Busche (1992) のモデルを使う。

キーワードは favorite-longshot bias, ordering probability, running time distribution, horse race。

## 着順確率について分かっていること

検索結果に出た本文の断片と、同じ著者らの他の研究から再構成する（原本の記述と一致するかは未確認）。

- Harville (1973) は勝率だけから着順確率を作る簡便法だが、香港データでは系統的な偏りがあり、Henery（正規走破時間）が明らかに当てはまりで勝った。
- Lo, Bacon-Shone and Busche (1995, Management Science) は Henery と Stern（gamma）の優位を示した（[Lo 1995](./1995-lo-ranking-probability-betting.md)）。
- 実用のための近似として、勝率（賭け金の比率 $P_i$ で推定可）から次の形で3連単確率を作る（本文の式 7 とされる）:

$$\pi_{ijk}=\pi_i\cdot\frac{\pi_j^{\lambda}}{\sum_{s\ne i}\pi_s^{\lambda}}\cdot\frac{\pi_k^{\tau}}{\sum_{t\ne i,j}\pi_t^{\tau}}$$

$\lambda,\tau$ は過去データから推定する。$\lambda=\tau=1$ で Harville に戻る。詳細は [Lo 2008（近似の章）](./2008-lo-ordering-probabilities-approximation.md)。

## 本命大穴バイアスについて

要旨の範囲では「普遍的ではない」という結論と、効用理論（リスク愛好の代表的賭け手）による解釈が与えられていることだけが分かる。どの国・期間のデータで、どのモデル（例えば勝率とオッズの対数線形回帰）を使ったかは未確認。日本のデータでバイアスが弱いという先行報告（Busche and Hall など）を含むかどうかも未確認。

## 批判的に読む（原本未取得のため限定的）

- レビューなので新しいデータの分析は限られると思われる（推測）。
- 着順モデルの比較は主に香港・米国の古いデータで、頭数や控除率が異なる JRA にそのまま当てはまるかは自分で確かめる必要がある。
- FLB の「普遍的でない」という結論は、どの券種・どの市場（パリミュチュエルかブックメーカーか）での話かで意味が変わる。原本で確認すべき点。

## keiba-ai での使い方

- **着順モデルの選択肢の地図**: Harville → Henery/Stern → discount 近似 → Plackett–Luce の学習、という比較実験の設計図として使う。まず discount 近似を実装し、Harville との差を JRA の3連単で測る。
- **市場確率の補正**: FLB が市場ごとに違うなら、JRA の単勝オッズから作る市場確率にも独自の補正（例: $p^\alpha$ の再正規化）が必要かを確かめる。補正前後の log loss とキャリブレーション曲線を比べる。
- 原本が取れたら、FLB のモデル式と各国の推定値、着順モデル比較の表を追記する。

## 関連ノート

- [Lo 2008](./2008-lo-ordering-probabilities-approximation.md): 同じ著者の discount 近似の章（原本未取得）。
- [Lo 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較。
- [Lo 1995](./1995-lo-ranking-probability-betting.md): 着順確率モデルの賭けへの応用。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md), [Henery 1981](./1981-henery-permutation-probabilities.md), [Stern 1990](./1990-stern-gamma-permutations.md): レビュー対象のモデル。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): FLB と効用による解釈の古典。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): FLB のサーベイ（日本語）。
- [Snowberg 2010](./2010-snowberg-flb-risk-love-misperceptions.md): FLB の原因をリスク愛好と確率の誤認で比べる。
- [Deza 2017](./2017-deza-exotic-wagering-losses.md): discount 近似を4連単に使った応用。

## 検索語

競馬の確率モデル, 統計モデル, レビュー, 本命大穴バイアス, 穴馬バイアス, 着順確率, 順序確率, 走破時間分布, 3連単, 馬単, discount モデル, Harville, Henery, Stern, 効用理論, favorite-longshot bias, FLB, ordering probability, running time distribution, exacta, trifecta, discount model, horse racing review, Lo Bacon-Shone

---
title: 先行研究の読む順番
---

# 先行研究の読む順番

[先行研究の一覧](/literature)には142本のノートがある。この順番で読むと全体像をつかみやすい。

## 1. 土台：市場オッズに情報を足す

- [Benter (1994)](./literature/2019-benter-model.md)：ファンダメンタルモデルと市場オッズを第2段の条件付きロジットで結合する。評価は ΔR²。
- [Bolton & Chapman (1986)](./literature/1986-bolton-conditional-logit.md)：条件付きロジットで勝率を推定する原典。
- [Edelman (2007)](./literature/2007-edelman-svm-horserace-odds.md)：Benter 型の第1段を SVM に置き換えた。
- [Lessmann ほか (2012)](./literature/2012-lessmann-stacking-competitive-event.md)：多様なモデルを条件付きロジットでスタッキングする。

## 2. 市場はどれくらい効率的か（日本を中心に）

- [Snowberg & Wolfers (2010)](./literature/2010-snowberg-flb-risk-love-misperceptions.md)：本命大穴バイアス（FLB）の原因はリスク愛好ではなく確率の誤認。
- [Busche (1988)](./literature/1988-busche-exception-risk-preference.md) と [Walls & Busche (2003)](./literature/2003-walls-breakage-turnover-japanese-tracks.md)：香港と日本の単勝では FLB が弱い。
- [小幡・太宰 (2014)](./literature/2014-obata-horse-racing-prospect-theory.md)：三連単では FLB がはっきり出る。券種ごとに市場確率の補正を変える必要がある。
- [芦谷 (2023)](./literature/2023-ashiya-sales-volume-efficiency.md)：売上が大きいレースほど市場が効率的。
- [Hanyu ほか (2025)](./literature/2025-hanyu-last-minute-dynamics-parimutuel.md)：JRA で締切直前にオッズが下がった馬は収益が高い。
- [森ほか (2010)](./literature/2010-mori-keiba-yoso-shuudanchi.md)：JRA の最終オッズの予測精度（AR 67.6%）。モデルが超えるべき市場ベースライン。

## 3. 単勝確率から連勝式の確率を作る

- [Harville (1973)](./literature/1973-harville-multi-entry-probabilities.md) → [Henery (1981)](./literature/1981-henery-permutation-probabilities.md) → [Stern (1990)](./literature/1990-stern-gamma-permutations.md)
- [Lo & Bacon-Shone (2008)](./literature/2008-lo-ordering-probabilities-approximation.md)：discount モデル。三連単の確率を作る実用上の第一候補。
- [Ali (1998)](./literature/1998-ali-probability-models-outcomes.md)：どの着順モデルにも FLB が残る。2着・3着の補正は結果データから推定する。

## 4. 評価方法

- [Walsh & Joshi (2024)](./literature/2024-walsh-calibration-vs-accuracy-betting.md)：モデルは精度ではなく校正で選ぶ。2025年に正誤表が出ている点に注意。
- [Gneiting & Raftery (2007)](./literature/2007-gneiting-proper-scoring-rules.md)：proper scoring rule の基礎。
- [Bailey ほか (2017)](./literature/2017-bailey-probability-backtest-overfitting.md) と [deflated Sharpe ratio (2014)](./literature/2014-bailey-deflated-sharpe-ratio.md)：馬券戦略を探索するときの多重検定の補正。
- [杉浦 (2026)](./literature/2026-sugiura-leakage-aware-evaluation.md)：JRA データでリークに配慮した時系列評価。単勝 AUC は約0.75。

## 5. 賭け方

- [Kelly (1956)](./literature/1956-kelly-information-rate.md)、[Thorp (2008)](./literature/2008-thorp-kelly-criterion-blackjack-sports.md)
- [Hausch, Ziemba & Rubinstein (1981)](./literature/1981-hausch-racetrack-market-efficiency.md)：自分の賭けによるオッズ変化を含めた最適化。
- [Metel (2017)](./literature/2017-metel-kelly-horse-races-uncertainty.md)、[Baker & McHale (2013)](./literature/2013-baker-kelly-parameter-uncertainty.md)、[Sun & Boyd (2018)](./literature/2018-sun-distributional-robust-kelly.md)：推定誤差を考慮した Kelly。
- [Uhrin ほか (2021)](./literature/2021-uhrin-optimal-sports-betting-review.md)：賭け戦略の比較実験。設計の雛形として使える。

## 反面教師

機械学習で競馬を予測した研究の多くは、精度だけで評価しているか、ランダム分割や仮定の配当で回収率を出している。例として [Borowski (2021)](./literature/2021-borowski-ml-flat-racing-poland.md) と [Chung (2017)](./literature/2017-chung-svm-committee-hong-kong.md) がある。keiba-ai では時系列分割（[ADR 0001](./adr/0001-time-series-split.md)）と実際のオッズで評価する。

---
title: A SVM-Based committee machine for prediction of Hong Kong horse racing
authors: Chung Wai-Chung, Chang Chuan-Yu, Ko Chien-Chuan
year: 2017
venue: 2017 10th International Conference on Ubi-media Computing and Workshops (Ubi-Media), pp.1-4
url: https://www.semanticscholar.org/paper/A-SVM-Based-committee-machine-for-prediction-of-Chung-Chang/7fa21791c9f8d6ce217b0b18958f8a98ce46d044
doi: 10.1109/UMEDIA.2017.8074091
topic: machine-learning
tags: svm, committee-machine, ensemble, hong-kong, hkjc, suspicious-roi
verified: abstract
importance: low
source: unavailable
source_version:
---

# 香港競馬の SVM コミッティマシン（回収率 800,000% の報告）

> 原本未取得。IEEE Xplore は購読制で、OpenAlex では OA 版が無く（closed）、ResearchGate にも全文が無い。Scribd に第三者のアップロードがあるが、権利が不明でログインも要るため使っていない。以下は要旨と Semantic Scholar の書誌情報に基づく。

> 一言で: 香港ジョッキークラブ（HKJC）の3年分の記録で、複数の SVM を合議させる「コミッティマシン」を作り、精度 70.86%・回収率 800,000% と報告した4ページの会議論文。数字の大きさから見て、評価方法を疑うべき事例として読む。

## 要旨から分かること

- データ: HKJC の3年分のレース記録（期間、レース数、券種は未確認）
- モデル: SVM を複数組み合わせたコミッティマシン（委員会機械）。個々の SVM の出力を合議で一つの予測にまとめる。合議の方法（多数決か、重み付きか、ゲート型か）は未確認。
- 実験: 「精度」と「回収率」を別々の実験として扱う。精度用と回収率用で委員会の組み方を変えているらしい（要旨の書き方からの推測）。
- 結果: 精度 70.86%、回収率 800,000%。

## 批判的に読む

数字そのものが評価の問題を示している。原本を読めていないので、以下は「この数字が出るとしたら何が起きているか」の推測である。

- **精度 70.86% の定義。** 香港の1レースは最大14頭。1着を当てる精度で 70% は、市場の1番人気の勝率（およそ 30% 前後）を大きく上回り、ありえない水準。考えられるのは「各馬が入着するか否か」のような2値分類の正解率（負例が多いので、全部「負け」と答えるだけで高くなる）か、「上位 k 頭に入るか」のような緩い基準。
- **回収率 800,000% の計算法。** 単純な回収率（払戻 ÷ 投資）で 8,000 倍はまず出ない。複利で賭け金を再投資し続けた資産の倍率なら、短期間でもこの桁になりうる。その場合、少数の大穴的中で数字が大きく振れる。
- **リークの経路。** 確定オッズ（締切後の最終オッズ）、着差・上がりタイムなどのレース後情報、同じレースの他馬の結果のどれかが特徴量に入っていると、精度も回収率もこの水準に跳ね上がる。
- **分割方法。** 3年分を無作為に分けたのか、時系列で分けたのかは未確認。
- 引用数は 11 件程度（scite）。後続研究が結果を再現したという話は見つけられなかった。

## keiba-ai での使い方

- **異常値のチェックリストとして使う。** keiba-ai のバックテストで回収率が 150% を超えたら、次を順に確かめる。
  1. 特徴量に確定オッズや結果由来の値が入っていないか（`odds` の取得時刻と締切時刻）
  2. 回収率が単純和か複利か（レポートは単純和を主にし、複利は資金曲線として別に出す）
  3. 的中が少数の高配当に偏っていないか（上位 1% の的中を除いた回収率も出す）
  4. 学習と検証が時系列で分かれているか
- **精度の定義をそろえる。** 「精度」と書くときは、レース単位の本命1着率か、馬単位の2値分類の正解率かを必ず区別する。後者は基準率（入着しない馬の割合）と並べないと意味が無い。

## 関連ノート

- [Edelman 2007](./2007-edelman-svm-horserace-odds.md): SVM を競馬に使い、市場オッズと組み合わせた研究。同じ SVM でも評価はずっと慎重。
- [Lessmann 2009](./2009-lessmann-svm-classification-horserace.md): SVM 分類で勝ち馬を予測し、回収率を控除率込みで評価。
- [Lessmann 2012](./2012-lessmann-stacking-competitive-event.md): 複数モデルの合議・スタッキング。コミッティマシンのより丁寧な版。
- [Chapman 1994](./1994-chapman-hong-kong-2000-races.md): 同じ香港市場の古典的研究。現実的な回収率の水準を知るのに使う。
- [Torné 2021](./2021-torne-hong-kong-softmax-nn.md): 香港のデータで NN を学習した例。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): バックテストの過学習の確率。異常に良い結果をどう疑うか。

## 検索語

サポートベクターマシン, SVM, コミッティマシン, committee machine, アンサンブル, ensemble, 合議, 香港, 香港ジョッキークラブ, HKJC, Hong Kong Jockey Club, 回収率, return rate, ROI, 異常な回収率, リーク, data leakage, 複利, compounding, 的中率, accuracy

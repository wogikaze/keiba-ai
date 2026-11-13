---
title: KEIBA-AI / KAIBA — 距離別 LightGBM・確率較正・EV 判定・自動投票の個人開発（ポートフォリオ README）
authors: SHOGO391
year: 2026
venue: GitHub
url: https://github.com/SHOGO391/KEIBA-AI-README
topic: practitioner
tags: grey-literature, github, jra-van, target-frontier, lightgbm, distance-specific-model, optuna, seed-bagging, isotonic-calibration, expected-value, kelly, auto-betting, post-race-odds-leak
verified: fulltext
importance: low
source: downloaded
source_version: web
---

# 799 特徴の距離別 LightGBM と EV ベースの自動投票 — 回収率 144.5% を「保守的に見る必要がある」と自ら注記したポートフォリオ

> 一言で: TARGET / JRA-VAN 系データから勝率と 3 着内確率を距離別 LightGBM で予測し、発走前オッズで EV を再計算して IPAT へ自動投票する個人システムの概要。12 か月バックテストの ROI 144.5%、EV-Kelly で 171.6% と書くが、一部券種の評価に確定後のオッズで再構成した区間が含まれると著者自身が注記している。コード・モデル・データは非公開で、検証できるのは README の記述だけ。

原本は README のみ（`library/2026-shogo391-kaiba-ev-autobet/source.txt`）。就職活動用のポートフォリオで、運用コードは公開していない。

## データ

- TARGET frontier / JRA-VAN 系のデータ（有償）。期間・件数の記載はない。
- 発走前オッズを別に取り込む。オッズが取れない場合用に `no_odds` 系モデルを分けている。

## 特徴量

- 799 個の特徴量を生成（「技術的な見どころ」の節）。中身の説明はない。

## モデルと目的変数

- 目的変数: 勝率（1 着）と 3 着内確率を別モデルで予測し、券種ごとの判断に使い分ける。
- LightGBM を距離別に学習。Optuna でハイパーパラメータ探索、seed bagging。
- SmoothIsotonic 系のキャリブレーションで確率の歪みを補正。
- 発走前オッズで EV を再計算し、推奨と購入を直前に更新。Playwright / Selenium で IPAT を操作。

## 評価と結果

「評価結果」の表（2026 年 3 月 14 日時点の内部評価）:

| 指標 | 値 |
| --- | --- |
| 総合テスト AUC | 0.8310 |
| 12 か月バックテスト ROI | 144.5% |
| EV-Kelly 適用時 ROI | 171.6% |
| 対象期間 | 2025 年 2 月〜2026 年 1 月 |
| 真の OOS 期間 | 2025 年 11 月〜2026 年 1 月 |

- flat stake は 100 円固定。EV-Kelly は期待値に応じて賭け金を変える。
- 「一部券種の履歴評価には、データ制約上、確定後に得られるオッズを使って再構成した区間が含まれます」とあり、実運用の回収率は保守的に見る必要がある、と著者が書いている。

## 批判的に読む

- 12 か月のうち「真の OOS」は 3 か月だけ。残り 9 か月は、モデル選択やハイパーパラメータ探索に使われた期間と重なっている可能性が高い。144.5% は主にこの in-sample 寄りの期間の数字と読むべき。
- EV の計算に確定オッズを使うと、「結果的に高配当になった馬」を EV > 1 と判定しやすくなり、回収率が大きく上振れする。著者がこれを明示している点は誠実だが、どの券種・どの区間かが書かれていないため、数値の解釈ができない。
- AUC 0.83 は 3 着内予測なら珍しくない値で、オッズ込みか否かも不明。回収率の根拠にはならない。
- Kelly で 171.6% に上がるのは、高 EV と判定された賭けに厚く張った結果。確定オッズ由来の EV の誤りが Kelly で増幅されている可能性がある。

## keiba-ai での使い方

- 反面教師として使う。評価コードでは「EV の判定に使うオッズ」と「払戻に使うオッズ」を別の列にし、判定側に確定オッズが入っていないことをテストで保証する。
- 「真の OOS 期間」を評価の主数値にし、チューニング期間と重なる数値は参考値として分けて書く、という書き方の規則に使える。
- 距離別モデルと全体モデルの比較、`no_odds` モデルの併用は、実験の候補として残す。

## 関連ノート

- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): リークを意識した評価。確定オッズ利用の問題。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): チューニング期間を含むバックテストの過学習。
- [Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 直前オッズと確定オッズのずれ。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md): 確率の誤差がある下での Kelly の過大投資。
- [Atsuo-514 2026](./2026-atsuo514-g1-place-shap.md): 同時期の個人開発で、回収率 100% 未満を明言した対照例。

## 検索語

距離別モデル, TARGET frontier, JRA-VAN, 確率較正, Isotonic, EV, 期待値, EV-Kelly, 自動投票, IPAT, 確定オッズ, リーク, バックテスト, 真の OOS, out-of-sample, post-race odds leakage, distance-specific LightGBM, portfolio project

---
title: オッズを使わない LightGBM 3 本（3着内・順位学習・1着）
date: 2026-11-14
status: running
---

# オッズを使わない LightGBM 3 本（3着内・順位学習・1着）

## 仮説

（実行前に記入）

- 過去成績・騎手・調教師・父・調教・レース条件だけ（オッズ・人気は一切なし、`features_v1` の 81 列）の LightGBM は、
  一様確率（1/頭数、race logloss ≈ 2.6）を大きく下回るが、市場（確定オッズの比例正規化、
  `experiments/2026-11-14_market-baseline/`）には届かない。
  公開例の polkka9710（モデル 2.1341 対 市場 1.9584）に近く、test の race logloss は 2.10〜2.20 程度、
  市場との差は +0.15 前後と予想する（[0006](../../docs/ideas/0006-public-models-as-baselines.md)）。
- 3 本の順は B（lambdarank）≈ A（3 着内）< C（1 着）と予想する。
  C は正例が約 7% で学習の信号が少なく、A・B は 2〜5 着の情報も使えるため。
  ただし A・B は確率を直接学習しないので、温度 s で合わせた後の較正（ECE）は C より悪くなりうる。
- 重要度の上位は、スピード指数・正規化着順・騎手の率・獲得賞金・レース内 z 値が占める。

## 変更点

最初のオッズなしモデル（`experiments/2026-11-13_lgbm-baseline/` は未実行のテンプレート例で、これとは別）。

- 特徴量: `src/keiba_ai/features.py`（`features_v1`）。各特徴量の使える時点（出馬表 / 当日発走前 / 前日までの履歴）は
  `features.FEATURES` に書いた。履歴はレース日より厳密に前の日だけから作る。
  リーク検査は `tests/test_features.py`（D 以降を消し、D 当日の結果を壊しても D 以前の特徴量が変わらない）。
- 対象: JRA、中止でないレース、出走した馬（異常区分 1〜3 を除く）。分割は market-baseline と同じ暫定の
  train 2004–2018 / valid 2019–2021 / test 2022–2025。2026 は使わない。
- モデル（`src/keiba_ai/lgbm_nomarket.py`）:
  - A: 3 着内の binary。B: lambdarank（関連度 = max(0, 6 − 着順)）。C: 1 着の binary。
  - early stopping は valid だけ。
  - 単勝確率: C は p / Σp。A・B は p ∝ exp(s·score)（A は log-odds、B は順位スコア）とし、
    温度 s を valid のレース単位 logloss 最小で 1 つ決める（valid は early stopping と s の両方に使うので、
    valid の指標はやや楽観的。test が本当の評価）。
- 出力: `data/processed/jra-van/derived/preds_lgbm_<model>.parquet`（race_key, umaban, date, split, score, p_win,
  y_win, finish_pos, horse_id）。train の行は学習データ上の予測（過学習ぎみ）なので、Benter の当てはめには valid を使う。

## 結果

（実行後に記入）

## 結論

（実行後に記入）

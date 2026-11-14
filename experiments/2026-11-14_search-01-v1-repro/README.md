---
title: 探索 01: 基準の再現（features_v1 の市場オフセット）
date: 2026-11-14
status: done
---

# 探索 01: 基準の再現（features_v1 の市場オフセット）

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）market-combination の市場オフセット LightGBM を共通の土台で再現する。test Δ ≈ −0.0136、valid Δ ≈ −0.0105（valid logloss 1.9786 vs 市場）になる。

## 変更点

なし（基準）。

## 結果

`results.json`（git 834b6b6、作業ツリー クリーン、92 秒）。

| | valid | test（探索中の参考値） |
|---|---|---|
| logloss（モデル / 10 分前の市場） | 1.9786 / 1.9968 | 1.9317 / 1.9453 |
| Δ（開催日の 95% CI） | -0.0182 [-0.0221, -0.0141] | -0.0136 [-0.0168, -0.0106] |
| 開催日 SE | 0.0020 | 0.0016 |

- test の年ごとの Δ: 2022 -0.0123, 2023 -0.0159, 2024 -0.0093, 2025 -0.0169。
- Benter（valid で当てはめ）: α 0.919（SE 0.048）、β 0.058。プラセボ（レース内で並べ替え）の α: -0.001, +0.008, +0.003, +0.003, +0.014（SE ≈ 0.008）。
- 学習: best_iteration 1079、特徴量 81 列。gain の上位: race_symbol_code 0.050, venue_code 0.031, horse_weight 0.027, h_corner4_mean3 0.027, h_l3f_1 0.024, h_fig_max5_z 0.023, h_days_since 0.023, jk_win_rate_z 0.021。

## 結論

基準を再現した（test Δ −0.0136 は market-combination と同じ）。以後の採否は valid Δ −0.0182 と比べる。

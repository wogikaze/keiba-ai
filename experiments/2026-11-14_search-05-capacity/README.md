---
title: 探索 05: 木を大きく・学習率を小さく
date: 2026-11-14
status: done
---

# 探索 05: 木を大きく・学習率を小さく

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）列が増えたので、木を大きくし（num_leaves 63、min_data_in_leaf 200）学習率を下げる（0.01）と、valid Δ が 0.0005〜0.002 良くなる。

## 変更点

02 の設定で num_leaves 31→63、min_data_in_leaf 500→200、learning_rate 0.02→0.01、num_boost_round 8000。

## 結果

`results.json`（git 2ad7da6、作業ツリー クリーン、280 秒）。

| | valid | test（探索中の参考値） |
|---|---|---|
| logloss（モデル / 10 分前の市場） | 1.9701 / 1.9968 | 1.9239 / 1.9453 |
| Δ（開催日の 95% CI） | -0.0267 [-0.0311, -0.0225] | -0.0214 [-0.0250, -0.0178] |
| 開催日 SE | 0.0022 | 0.0018 |

- test の年ごとの Δ: 2022 -0.0169, 2023 -0.0248, 2024 -0.0164, 2025 -0.0276。
- Benter（valid で当てはめ）: α 0.978（SE 0.043）、β 0.012。プラセボ（レース内で並べ替え）の α: -0.001, +0.009, +0.004, +0.002, +0.014（SE ≈ 0.007）。
- 学習: best_iteration 1675、特徴量 100 列。gain の上位: mk_q_vs_win 0.043, race_symbol_code 0.036, mk_logodds 0.027, venue_code 0.022, h_corner4_mean3 0.021, horse_weight 0.021, h_l3f_1 0.019, h_fig_max5_z 0.018。

## 結論

**採用。** 02 との対になった差（valid）は −0.0015 [−0.0027, −0.0001]、SE 0.0007（`scripts/compare_preds.py`）。仮説（0.0005〜0.002）の範囲。最後にまとめる 1 本ではこの設定を使う。

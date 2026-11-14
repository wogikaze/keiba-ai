---
title: 探索 02: 決定時刻までの市場の特徴量（market_v1）を足す
date: 2026-11-14
status: done
---

# 探索 02: 決定時刻までの市場の特徴量（market_v1）を足す

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）オッズの動き（60→10 分前、最初→10 分前）・票数・複勝や馬連との食い違いは、10 分前の単勝オッズに要約しきれていない情報を持つ。valid Δ は基準より 0.004〜0.010 良くなる。gain の上位に mk_d60・mk_dfirst・mk_pl_vs_win・mk_q_vs_win が入る。

## 変更点

特徴量に market_v1 の 19 列を足す。

## 結果

`results.json`（git 834b6b6、作業ツリー 変更あり: M src/keiba_ai/search.py
?? src/keiba_ai/features_hist2.py、150 秒）。

| | valid | test（探索中の参考値） |
|---|---|---|
| logloss（モデル / 10 分前の市場） | 1.9716 / 1.9968 | 1.9245 / 1.9453 |
| Δ（開催日の 95% CI） | -0.0253 [-0.0297, -0.0207] | -0.0209 [-0.0245, -0.0171] |
| 開催日 SE | 0.0022 | 0.0019 |

- test の年ごとの Δ: 2022 -0.0164, 2023 -0.0243, 2024 -0.0173, 2025 -0.0255。
- Benter（valid で当てはめ）: α 0.921（SE 0.041）、β 0.067。プラセボ（レース内で並べ替え）の α: -0.000, +0.008, +0.004, +0.002, +0.014（SE ≈ 0.007）。
- 学習: best_iteration 1327、特徴量 100 列。gain の上位: mk_q_vs_win 0.050, race_symbol_code 0.041, mk_logodds 0.031, venue_code 0.025, h_corner4_mean3 0.021, horse_weight 0.020, h_fig_max5_z 0.018, h_days_since 0.018。

## 結論

**採用。** valid Δ が −0.0182 → −0.0253（差 0.0071、開催日 SE 0.0022 の 3 倍）。仮説（0.004〜0.010）の範囲。gain の 1 位は mk_q_vs_win（馬連から作った確率と単勝の確率の食い違い）で、馬連の票は単勝より情報を持つらしい。以後の基準はこの 02。

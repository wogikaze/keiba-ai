---
title: 実験リーダーボード
---

# 実験リーダーボード

> このファイルは `scripts/build_index.py` で自動生成される。手で編集しないこと。

| experiment | title | status | test_dlogloss_n10_prop_vs_final | test_logloss_A_top3 | test_logloss_B_rank | test_logloss_C_win | test_logloss_final_prop | test_logloss_last_prop | test_logloss_n10_powerfit | test_logloss_n10_prop | valid_logloss_A_top3 | valid_logloss_B_rank | valid_logloss_C_win | valid_logloss_n10_powerfit | valid_logloss_n10_prop | split | data | seed | git |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [2026-11-14_market-baseline](./2026-11-14_market-baseline/README.md) | 市場ベースライン（単勝オッズだけ） | done | 0.0404 | - | - | - | 1.9073 | 1.9170 | 1.9453 | 1.9477 | - | - | - | 1.9968 | 1.9973 | 2004-2018/2019-2021/2022-2025 (provisional) | jra-van-processed@75d8885 | 42 | `dcd55a0` |
| [2026-11-14_lgbm-nomarket](./2026-11-14_lgbm-nomarket/README.md) | オッズを使わない LightGBM 3 本（3着内・順位学習・1着） | done | - | 2.0627 | 2.0509 | 2.0607 | - | - | - | - | 2.0941 | 2.0893 | 2.0920 | - | - | 2004-2018/2019-2021/2022-2025 | jra-van@23d39260/features_v1-c7cb41 | 42 | `6531395` |
| [2026-11-13_lgbm-baseline](./2026-11-13_lgbm-baseline/README.md) | LightGBM ベースライン | planned | - | - | - | - | - | - | - | - | - | - | - | - | - | 2015-2022/2023/2024 | - | 42 | - |

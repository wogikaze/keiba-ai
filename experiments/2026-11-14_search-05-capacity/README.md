---
title: 探索 05: 木を大きく・学習率を小さく
date: 2026-11-14
status: planned
---

# 探索 05: 木を大きく・学習率を小さく

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）列が増えたので、木を大きくし（num_leaves 63、min_data_in_leaf 200）学習率を下げる（0.01）と、valid Δ が 0.0005〜0.002 良くなる。

## 変更点

02 の設定で num_leaves 31→63、min_data_in_leaf 500→200、learning_rate 0.02→0.01、num_boost_round 8000。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

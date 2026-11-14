---
title: 探索 01: 基準の再現（features_v1 の市場オフセット）
date: 2026-11-14
status: planned
---

# 探索 01: 基準の再現（features_v1 の市場オフセット）

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）market-combination の市場オフセット LightGBM を共通の土台で再現する。test Δ ≈ −0.0136、valid Δ ≈ −0.0105（valid logloss 1.9786 vs 市場）になる。

## 変更点

なし（基準）。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

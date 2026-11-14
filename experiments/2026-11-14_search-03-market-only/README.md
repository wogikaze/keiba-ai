---
title: 探索 03: market_v1 だけ（過去成績なし）
date: 2026-11-14
status: planned
---

# 探索 03: market_v1 だけ（過去成績なし）

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）market_v1 だけでも valid Δ は負になるが、v1 だけ（基準）より小さい（−0.003〜−0.006）。過去成績と市場の動きは別の情報なので、02 は 01 と 03 の和に近い。

## 変更点

特徴量を market_v1 だけにする。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

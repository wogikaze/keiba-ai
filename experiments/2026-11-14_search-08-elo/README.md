---
title: 探索 08: 相手の強さを考えたレーティング（多頭の Elo）を足す
date: 2026-11-14
status: planned
---

# 探索 08: 相手の強さを考えたレーティング（多頭の Elo）を足す

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）v1 の着順・スピード指数は相手の強さを考えない。多頭の Elo（rating_v1）を足すと、02 より valid Δ が 0.0003〜0.001 良くなる。ただし市場はすでに相手関係を織り込んでいるので、改善は小さい。

## 変更点

02 の特徴量に rating_v1 の 6 列を足す。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

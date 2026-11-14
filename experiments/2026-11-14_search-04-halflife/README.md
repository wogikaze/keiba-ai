---
title: 探索 04: 新しい学習データを重くする（半減期 5 年）
date: 2026-11-14
status: planned
---

# 探索 04: 新しい学習データを重くする（半減期 5 年）

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）市場の効率と馬券の売れ方は年とともに変わる（10 分前と確定の差が広がっている）。新しいレースを重くすると valid Δ が 0.001〜0.002 良くなる。

## 変更点

02 の設定に、学習の重み 0.5^(2019 年からの年数 / 5) を付ける。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

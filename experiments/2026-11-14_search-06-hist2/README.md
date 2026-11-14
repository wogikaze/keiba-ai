---
title: 探索 06: 過去の市場の外れ方（history_v2）を足す
date: 2026-11-14
status: planned
---

# 探索 06: 過去の市場の外れ方（history_v2）を足す

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）騎手・調教師・父・馬が過去に市場から過小・過大評価されてきた度合いと、前走の人気から見た着順は、10 分前の市場にまだ残る偏りを表す。02（v1 + market_v1）に足すと valid Δ が 0.0005〜0.002 良くなる。

## 変更点

02 の特徴量に history_v2 の 14 列を足す。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

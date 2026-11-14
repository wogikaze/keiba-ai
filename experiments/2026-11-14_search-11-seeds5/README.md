---
title: 探索 11: seed を 5 つ平均する
date: 2026-11-14
status: planned
---

# 探索 11: seed を 5 つ平均する

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）bagging・feature_fraction の乱数を変えた 5 本の補正 f を平均すると分散が減り、02 より valid Δ が 0.0002〜0.0008 良くなる。

## 変更点

02 の設定で seed を [42, 43, 44, 45, 46] にし、補正 f（生のスコア）を平均する。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

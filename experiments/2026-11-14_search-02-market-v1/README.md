---
title: 探索 02: 決定時刻までの市場の特徴量（market_v1）を足す
date: 2026-11-14
status: planned
---

# 探索 02: 決定時刻までの市場の特徴量（market_v1）を足す

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）オッズの動き（60→10 分前、最初→10 分前）・票数・複勝や馬連との食い違いは、10 分前の単勝オッズに要約しきれていない情報を持つ。valid Δ は基準より 0.004〜0.010 良くなる。gain の上位に mk_d60・mk_dfirst・mk_pl_vs_win・mk_q_vs_win が入る。

## 変更点

特徴量に market_v1 の 19 列を足す。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

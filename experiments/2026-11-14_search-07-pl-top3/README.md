---
title: 探索 07: 2・3 着も使う損失（上位 3 着の Plackett-Luce）
date: 2026-11-14
status: planned
---

# 探索 07: 2・3 着も使う損失（上位 3 着の Plackett-Luce）

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）1 着だけの損失より、2・3 着の順位も使うとレースあたりの情報が増え、補正 f の推定が安定する。02 と同じ特徴量で、勝率の valid Δ が 0.0005〜0.0015 良くなる。2・3 着の段は市場の割引（γ2 0.86、γ3 0.76、賭け方の実験の値）で弱める。

## 変更点

02 の設定で、目的関数を上位 3 着の Plackett-Luce（γ = 1, 0.86, 0.76、重み 1, 1, 1）にする。早期終了と評価は勝率の logloss のまま。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

---
title: 探索 09: 券種間の食い違いの時間変化・馬連の票数・オッズの揺れ（market_v2）
date: 2026-11-14
status: planned
---

# 探索 09: 券種間の食い違いの時間変化・馬連の票数・オッズの揺れ（market_v2）

仮説探索（[ADR 0005](../../docs/adr/0005-market-features-and-search-protocol.md)）。`scripts/run_search.py` で走らせる。
基準は search-01（features_v1 の市場オフセット LightGBM、market-combination と同じ設定）。採否は valid の Δ だけで決め、test は参考値。

## 仮説

（実行前に書いた）02 の gain の 1 位は mk_q_vs_win（馬連と単勝の食い違い）だった。食い違いの時間変化（30・60 分前からの動き）、馬連と単勝の票数の比、複勝の確率の動き、直前 1 時間のオッズの揺れと傾きを足すと、02 より valid Δ が 0.001〜0.003 良くなる。

## 変更点

02 の特徴量に market_v2 の 10 列を足す。

## 結果

（実行後に書く）

## 結論

（実行後に書く）

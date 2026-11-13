---
title: Pricing Exotic Racetrack Wagers
authors: Hausch Donald B., Lo Victor S. Y., Ziemba William T.
year: 1994
venue: Efficiency of Racetrack Betting Markets (Hausch, Lo, Ziemba eds.), Academic Press, pp. 469-483
url: https://econpapers.repec.org/bookchap/wsiwschap/9789812819192_5f0047.htm
doi: 10.1142/9789812819192_0047
topic: probability-models
tags: exotic-bets, pricing, harville-formula, favourite-longshot-bias
verified: abstract
importance: medium
source: unavailable
---

# 単勝オッズから連勝式馬券の「適正価格」を作る

> **原本未取得。** 書籍の章（1994 年 Academic Press 版、2008 年 World Scientific 再版の第47章、同ページ）で、合法な無料版が見つからなかった。Scribd などの転載は権利が不明なので使っていない。本ノートは RePEc の要旨と後続文献の記述に基づく。

> 一言で: 単勝市場はほぼ弱度効率的なので、単勝の票数から各馬の勝率をかなり正確に推定できる。そこに人気-大穴バイアスの補正を加え、走破時間分布の着順確率モデルと組み合わせて全着順の確率を作れば、馬単（exacta）・3連単（trifecta）・馬連（quinella）・ダブル（daily double）の適正価格が出せ、期待収益が正になる場面を見つけられる、と主張する。

## 要旨から分かること

1. 先行研究から、単勝市場は本質的に弱度効率的で、各オッズ水準への賭け金は真の勝率のかなり良い推定値になる。
2. その推定を、人気-大穴バイアス（大穴の過大評価・本命の過小評価）を補正して改善する。
3. 補正した価格式を走破時間分布の確率モデルと組み合わせ、すべての着順の確率を出す。
4. これで exacta、trifecta、quinella、daily double を価格付けし、正の期待収益になる場面を特定できる。

著者の所属: Hausch はウィスコンシン大学、Lo と Ziemba は UBC 商学部（RePEc）。

## 後続文献での扱い

- 同じ書籍の Lo の論文の記述として、本章は「特定の種類の賭けについて、小さなデータで Harville が Henery よりわずかに良い」と結論したとされる（検索結果経由の孫引き、出典の頁は**未確認**）。これは Lo & Bacon-Shone (1994) や Lo (1994) の「Henery/Stern が Harville より良い」と逆向きであり、データの小ささが理由として挙げられている。
- Ziemba & Hausch (1986) は、HZR が複勝・3着内で使った手法（効率的な単勝市場からの勝率、Harville による他の馬券の価格付け、Kelly 基準による賭け金）を連勝式へ広げた。本章はその延長に位置づけられる（ハンドブックの記述、検索結果経由）。

## 未確認の点

- 人気-大穴バイアスの補正式の形（勝率を $(W_i/W)^d$ に比例させる Ali 型か、別の形か）。
- どの走破時間モデル（Harville / Henery / Stern）を最終的に採用したか。
- データ（競馬場・期間・レース数）と、正の期待収益の場面がどの程度あったか。

## 批判的に読む

- **単勝市場の効率性に依存**: 連勝式の価格は単勝確率の推定精度で決まる。単勝市場の FLB 補正が市場・時期で変わるなら、補正パラメータの推定が結果を左右する。
- **連勝式プールの小ささ**: 連勝式は組み合わせが多く1組あたりのプールが小さいので、自分の賭けで払戻が下がる効果が大きい。期待値の評価にはこの影響を入れる必要がある（入れているかは未確認）。
- **確率モデルの誤差の伝播**: Harville の2・3着の偏りは、3連単では積で効く。人気薄を含む組み合わせの価格がとくに歪みやすい。

## keiba-ai での使い方

- **理論オッズと実オッズの比較**: JRA の単勝オッズ（FLB 補正後）→着順確率モデル→馬連・馬単・ワイド・3連複・3連単の理論オッズ、を作り、実際の確定オッズとの比を記録する。比が大きい（実オッズが理論より高い）組み合わせの回収率を調べるのが、本章の戦略の再現になる。
- **仮説**: 「連勝式の実オッズと単勝から作った理論オッズの比は、人気薄の組み合わせで系統的に1を下回る（連勝式の方が大穴をより過大評価する）」。これは日本の3連単に関する小幡・太宰 (2012) の研究とも比べられる。
- **評価**: 控除率は券種ごとに違う（JRA では単勝・複勝 20%、馬連・ワイド 22.5%、3連単 27.5% など）。理論オッズは各券種の控除率を引いて計算する。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 着順確率の基本式。
- [Hausch, Ziemba & Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 単勝から複勝・3着内を価格付けした原型。
- [Hausch & Ziemba 1985](./1985-hausch-transactions-costs-multiple-wagers.md): 取引コストと複数賭け。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md), [Lo 1994](./1994-lo-running-time-japan.md): モデル比較（Henery/Stern 優位）。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): 単勝の FLB 補正の出所の一つ。
- [小幡・太宰 2012](./2012-obata-prospect-theory-trifecta.md): 日本の3連単市場の分析。
- [Deza ら 2017](./2017-deza-exotic-wagering-losses.md): 連勝式の損失管理。

## 検索語

連勝式, エキゾチック馬券, exotic wager, 馬単, exacta, 3連単, trifecta, triactor, 馬連, quinella, ダブル, daily double, 価格付け, pricing, 理論オッズ, fair odds, 弱度効率性, weak-form efficiency, 人気-大穴バイアス, favourite-longshot bias, Harville, 走破時間分布, Dr. Z, Hausch Ziemba

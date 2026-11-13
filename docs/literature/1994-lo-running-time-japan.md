---
title: Application of Running Time Distribution Models in Japan
authors: Lo Victor S. Y.
year: 1994
venue: Efficiency of Racetrack Betting Markets (Hausch, Lo, Ziemba eds.), Academic Press, pp. 237-247
url: https://econpapers.repec.org/bookchap/wsiwschap/9789812819192_5f0024.htm
doi: 10.1142/9789812819192_0024
topic: probability-models
tags: running-time-model, stern-model, henery-model, harville-formula, japan
verified: abstract
importance: medium
source: unavailable
---

# 日本の競馬データで Harville・Henery・Stern の着順確率モデルを比べる

> **原本未取得。** 書籍の章（1994 年 Academic Press 版、2008 年 World Scientific 再版の第24章、同ページ）で、合法な無料版が見つからなかった。本ノートは RePEc の要旨と、本章を引用する後続論文（Deza ら 2017、Ali 1998。いずれも library に原本あり）に基づく。

> 一言で: 走破時間を独立な確率変数とみる3つの着順確率モデル（Harville＝指数、Henery＝正規、Stern＝ガンマ）を日本のデータに当てはめ、特定の形状パラメータの Stern モデルが最も良いと報告した。Stern モデルが正しいとすると、Harville は着順確率を系統的に誤って見積もる。

## 要旨から分かること

- 問題: 「馬 $i$ が勝ち、馬 $j$ が2着」のような着順確率の予測。
- Harville (1973) が最もよく使われ、走破時間を独立な指数分布と仮定する。直前の実証研究（Lo & Bacon-Shone 1994 と思われる）では Henery (1981) の方が当てはまりが良かった。
- 本章は Stern (1990) のガンマモデルを比較に加え、3つを日本のデータに当てはめた。
- 結果: ある形状パラメータの値の Stern モデルが他より優れていた。Stern が真なら Harville には系統的な偏りがある。
- 著者の所属は UBC 商学部（RePEc）。

## 未確認の点

- 最良だった形状パラメータ $r$ の値。旧版ノートには二次文献経由で「$r=4$」とあったが、出典を確かめられていない。**未確認**。
- データの範囲。同じ著者らの研究報告（Lo, Bacon-Shone & Busche 1994）が「日本 1990–91 年の 983 レース」を使っていると Ali (1998) が書いており (Ali p.228)、同じデータの可能性があるが**未確認**。中央競馬か地方競馬かも未確認。
- 比較の方法（尤度か、ロジスティック回帰の当てはまりか）。Lo & Bacon-Shone (1994) と同じく、各モデルの確率を説明変数にしたロジットの尤度比較と推測される。

## 後続研究での扱い

Deza ら (2017) は、Harville 型の式は人気馬に偏ることが「Lo (2008)」（本章の 2008 年再版）と Lo & Bacon-Shone (1994) で見つかったと書き、その改良として Lo & Bacon-Shone (2008) の割引近似を4連単の確率に使っている（[Deza ら 2017](./2017-deza-exotic-wagering-losses.md), PDF p.6）。

## 批判的に読む

- **30 年以上前の日本のデータ**: 1990 年前後の日本の馬券は単勝・複勝・枠連が中心で、馬連は 1991 年導入。単勝オッズの効率性も現在とは違うはず。
- **$r$ の一般性**: 香港やハーネス競走での最良の $r$（Ali 1998 では正規に近いほど良い）と日本の値が違うなら、$r$ は市場・レース条件に依存する。本章の値をそのまま使わず推定し直す必要がある。

## keiba-ai での使い方

- **最も近い先行研究**: JRA を対象とする本研究に直結する。$r$ を自前データで最尤推定し、本章の結論（Stern > Henery > Harville）が現在の JRA で再現するかを確かめる。
- **実験案（仮説）**: 「JRA 2015 年以降のデータでも、2着・3着確率の対数尤度は Stern（$r>1$）が Harville を上回る。最良の $r$ は芝とダート、頭数で異なる」。比較には [Stern 1990](./1990-stern-gamma-permutations.md) のモンテカルロ実装と、割引 Harville の近似を使う。
- **券種**: 当時と違い現在は馬単・3連単がある。3連単の確率でモデル間の差が最も大きく出るはず。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md), [Henery 1981](./1981-henery-permutation-probabilities.md), [Stern 1990](./1990-stern-gamma-permutations.md): 比較した3モデル。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): 直前の比較研究（Henery 優位）。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 日本を含む3市場での賭けへの応用。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): Henery/Stern の簡単な近似。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 米国ハーネスでの大規模比較。
- [Walls & Busche 2003](./2003-walls-breakage-turnover-japanese-tracks.md): 日本の競馬場の市場効率性。

## 検索語

走破時間分布, running time distribution, 日本の競馬, Japan, JRA, Stern モデル, ガンマ分布, Henery モデル, 正規分布, Harville 公式, 指数分布, 着順確率, ordering probability, 形状パラメータ, shape parameter, 2着確率, 馬単, exacta, モデル比較

---
title: Still Searching for Positive Returns at the Track: Empirical Results from 2,000 Hong Kong Races
authors: Chapman Randall G.
year: 1994
venue: Efficiency of Racetrack Betting Markets (Hausch, Lo, Ziemba eds.), Academic Press, pp. 173-181
url: https://ideas.repec.org/h/wsi/wschap/9789812819192_0018.html
doi: 10.1142/9789812819192_0018
topic: probability-models
tags: conditional-logit, fundamental-model, hong-kong, win-betting
verified: abstract
importance: medium
source: unavailable
---

# 香港 2,000 レースで多項ロジットを再検証：大穴を除くと単勝で期待収益 20% 超

> **原本未取得。** 書籍の章で、合法な無料版が見つからなかった。本ノートは RePEc / World Scientific の要旨と、本章を引用する後続論文（Sung & Johnson 2007、Silverman 2012）に基づく。

> 一言で: [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md) の多項ロジット（条件付きロジット）を、20 変数・香港 2,000 レースに拡張した。オッズを使わない純ファンダメンタルモデルで、1単位ずつの単勝賭けをホールドアウトで評価し、推定勝率 0.04 未満の極端な大穴を除くと期待収益が 20% を超えたと報告する。

## 要旨から分かること

- 1986 年論文の手法を「より洗練されたファクター」と「より大きなデータベース」に広げた続編（RePEc 要旨）。
- 20 変数の純ファンダメンタル（pure fundamental）多項ロジット。市場オッズはモデルに入れていない。
- 香港の 2,000 レース。ホールドアウト標本で、単純な1単位の単勝賭けに正の収益の明確な証拠があったとする。
- 推定勝率 0.04 未満の馬を除外すると、期待収益が 20% を超える。
- 1994 年 Academic Press 版の第18章。2008 年に World Scientific から同じページ（173–181）で再版された。

## 後続研究での扱い

- Sung & Johnson (2007) は、ファンダメンタル変数と市場由来の確率を同時に回帰する「1段階型」の例として Bolton & Chapman (1986) と並べて本章を挙げ、Benter (1994) の2段階型と対比している（[Sung & Johnson 2007](./2007-sung-two-step-conditional-logit.md), PDF p.2）。要旨の「純ファンダメンタル」との関係は原本で確認が必要（**未確認**）。
- Silverman (2012) は、本章が香港で自分の予測と大衆の予測を比べ、両者の組み合わせが最も利益が大きかったと要約する（[Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md), PDF p.1）。要旨にない内容なので、原本で確かめるべき点として残す。

## 原本で確認すべき点（未確認）

- 20 変数の内訳（Bolton & Chapman の 10 変数からの追加分）。
- データ期間（同じ書籍の Benter 論文と同じく 1980 年代後半の香港と推測されるが未確認）、推定とホールドアウトの分割方法、ホールドアウトのレース数。
- 「期待収益 20% 超」が実際の払戻（控除率・端数切り込み）による実現回収率か、モデル確率×オッズの期待値か。
- 0.04 という閾値を、ホールドアウトを見る前に決めたか。

## 批判的に読む

- **閾値選択のリーク**: 「大穴を除外すると黒字」は、閾値をホールドアウト結果を見て選ぶと容易に作れる。閾値が事前に固定されていたかが本章の信頼性を左右する。
- **大穴除外の意味**: 人気-大穴バイアス（大穴の期待値が特に低い）がある市場では、大穴を除くだけで回収率は上がる。モデルの価値と、FLB を避ける効果を分けて評価しないといけない。
- **純ファンダメンタルの確率は偏る**: Benter (1994) は、オッズと結合しないファンダメンタル確率は単独では市場より較正が悪いと指摘し、市場確率との結合を勧めた。本章の結論はこの点と緊張関係にある。
- **市場の規模**: 香港は売上が大きく、1単位の賭けならオッズへの影響は無視できる。日本の小さいレースでは同じ仮定が成り立たない場合がある。

## keiba-ai での使い方

- **ベースライン実験**: オッズを入れない条件付きロジット（または LightGBM＋レース内 softmax）を、本章にならい「推定勝率 $p<\tau$ の馬を賭けから除外」して評価する。$\tau$ は学習期間で決めて評価期間では固定。
- **仮説**: 「JRA の単勝でも、$\tau$ 付近（0.03〜0.05）での除外は回収率を上げるが、その効果の大半は市場の人気-大穴バイアスによる」。確かめるには、モデル確率を使わず市場確率だけで同じ除外をした場合と比べる。
- **評価指標**: 実際の確定オッズで回収率を計算し、ブートストラップで信頼区間を出す。2,000 レースでも回収率の標準誤差は数％〜十数％あるはずで、単一の数値で判断しない。

## 関連ノート

- [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md): 本章の前作。同じ多項ロジット、200 レース。
- [Benter 1994](./2019-benter-model.md): 同じ書籍・同じ香港市場。ファンダメンタル確率と市場確率の2段階結合を提案。
- [Sung & Johnson 2007](./2007-sung-two-step-conditional-logit.md): 1段階型と2段階型の比較。
- [Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md): 本章を引用する香港データの階層ベイズモデル。
- [Torné 2021](./2021-torne-hong-kong-softmax-nn.md): 香港での softmax ニューラルネット。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): 大穴除外が効く背景の人気-大穴バイアス。

## 検索語

香港競馬, Hong Kong Jockey Club, HKJC, 条件付きロジット, conditional logit, 多項ロジット, multinomial logit, ファンダメンタルモデル, pure fundamental model, 単勝, win betting, 大穴除外, longshot exclusion, 正の期待収益, positive expected return, ホールドアウト, holdout, Efficiency of Racetrack Betting Markets, Chapman

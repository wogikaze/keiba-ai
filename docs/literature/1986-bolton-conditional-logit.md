---
title: Searching for Positive Returns at the Track: A Multinomial Logit Model for Handicapping Horse Races
authors: Bolton Ruth N., Chapman Randall G.
year: 1986
venue: Management Science 32(8) 1040-1060
url: https://pubsonline.informs.org/doi/abs/10.1287/mnsc.32.8.1040
doi: 10.1287/mnsc.32.8.1040
topic: probability-models
tags: conditional-logit, rank-ordered-logit, explosion, fundamental-model, win-betting
verified: abstract
importance: high
source: unavailable
---

# 競馬の勝率をレース内多項ロジットで推定する：ファンダメンタル・ハンディキャップモデルの原点

> **原本未取得。** 本ノートは出版社・RePEc の要旨と、本論文を詳しく引用する後続論文（Benter 1994、Sung & Johnson 2007、Silverman 2012、Torné 2021 など。いずれも library に原本あり）に基づく。原本で確かめていない数値は「未確認」と書く。

> 一言で: 各馬の「効用」を馬・騎手・レースの特徴量の線形和とし、レース内で多項ロジット（softmax）を取って勝率を推定した。着順の上位数頭を「順に選ばれる選択」に分解する rank-ordered（explosion）推定で効率を上げ、200 レースのホールドアウト評価で、大穴を除外する単勝戦略に正の期待収益の可能性を示した。

## 要旨（出版社・RePEc の要約から）

- 問い: 単勝のパリミュチュエル市場で、一般大衆の系統的な誤りをファンダメンタル情報で見つけて利益にできるか。
- 方法: 馬・騎手・レース固有の変数を使う多項ロジットを 200 レースで推定。順位つきの選択集合（ranked choice set）を使って推定効率を上げ、ホールドアウト標本で賭け戦略を評価。
- 結論: 目立たない（オッズを動かさない）賭け方で、大穴への賭けを除外する制約を付けると、大きな控除率の下でも正の期待収益が見込めるように見える。

キーワード: multinomial logit, stochastic utility model, ranked choice set data, discrete choice modeling。

## モデル（後続論文の記述から再構成）

馬 $i$ のレース $j$ での効用を $V_{ij}=\beta^\top x_{ij}$ とし、勝率を

$p_{ij}=\exp(V_{ij})/\sum_{k\in j}\exp(V_{kj})$

とする条件付きロジット（McFadden 型）。Benter (1994) は自身のモデルの型を「Bolton & Chapman (1986) が提案した多項ロジット」と明言し、出力がレース内で合計1になる点を利点に挙げる（[Benter 1994](./2019-benter-model.md), PDF p.2）。

**Explosion（rank-ordered logit）**: Chapman & Staelin (1982) の方法で、着順 1→2→3… を「全馬から1着を選ぶ選択」「残りから2着を選ぶ選択」…という独立な選択に分解し、同じ $\beta$ で尤度を掛け合わせる。これは Plackett-Luce 尤度そのもの。下位着順ほどノイズが増えるので、分解の深さは Watson & Westin (1975) の検定で決め、Bolton & Chapman では深さ3までとした（Sung & Johnson 2007, PDF p.7 の記述）。

**変数**: Sung & Johnson (2007) は Bolton & Chapman の変数集合をそのまま使っており、その一覧（同論文 Table 1, PDF p.6）から、前走スピード指数、直近4走の平均スピード指数、枠番、1走あたり賞金、距離変更フラグ（NEWDIST）、斤量、通算勝率、騎手の勝利数・勝率などが含まれていたと推測できる。Benter は NEWDIST を例に挙げ、Bolton & Chapman のモデルは 1〜1.25 マイルのレースだけを予測対象にしていたと注記する（Benter, PDF p.3）。Torné (2021) は「手作業で集めた 200 レース、約10個の単純な特徴量、馬間で重みを共有」と要約する（[Torné 2021](./2021-torne-hong-kong-softmax-nn.md), PDF p.3）。

**評価**: Benter は、モデルの当てはまりの指標（McFadden 型の疑似 $R^2$）と、モデル確率と市場確率を組み合わせる式の出典として Bolton & Chapman (1986) p.1044 を挙げる（Benter, PDF p.6–7）。

## データと結果（未確認の部分が多い）

- 200 レース（米国の競馬場）。150 レースで推定し、残りで賭けを評価する分割を繰り返した（要旨・検索結果の記述）。
- 旧版ノートには「E=1 で疑似 R² 約 9%」「E=1→2 で標準誤差が平均 28.3% 減、E=2→3 でさらに 16.8% 減」とあったが、原本で確認できていない。**未確認**。
- 回収率の具体的数値、大穴除外の閾値は**未確認**。

## 批判的に読む

- **サンプルが極めて小さい**: 200 レース・約10変数。ホールドアウトは 50 レース程度で、回収率の信頼区間は非常に広いはず。著者自身「promise」と控えめに書いている。
- **大穴除外の選び方**: 閾値をホールドアウト結果を見て決めていれば、選択バイアスになる。この点は原本で確認が必要（未確認）。
- **市場オッズを特徴量に入れているか**: Sung & Johnson は Bolton & Chapman を「ファンダメンタル変数と市場確率を同時に回帰する1段階型」の例に挙げる（PDF p.2）。1段階型は市場情報がファンダメンタル係数を吸収しやすく、Benter が2段階型を勧めた理由になった。
- **再現性**: データは手作業収集で公開されていない。

## keiba-ai での使い方

- **基本形**: 勝率モデルの出力層は「レース内 softmax（条件付きロジット）」にする。LightGBM の lambdarank や二値分類の出力を、レース内で正規化する設計はこの系譜に当たる。
- **Explosion の深さを実験で決める**: 仮説「1〜3着までの Plackett-Luce 尤度で学習すると、1着だけの softmax より単勝確率の対数損失が下がる。4着以下まで使うと悪化する」。JRA データで深さ1〜5（全着順）を比較し、Watson–Westin 型の尤度比検定と、時系列ホールドアウトの対数損失の両方を見る。
- **大穴除外ルールの検証**: 「推定勝率が閾値未満の馬に賭けない」制約は、Chapman (1994) でも効いている。閾値は学習期間で決め、評価期間では固定する（閾値選択によるリークを防ぐ）。
- **市場確率との結合**: Benter の2段階（ファンダメンタル確率と市場確率をもう1回ロジットで結合）と、Bolton & Chapman 型の1段階を同じ分割で比べる。

## 関連ノート

- [Chapman 1994](./1994-chapman-hong-kong-2000-races.md): 同じ手法を 20 変数・香港 2,000 レースに拡張した続編。
- [Benter 1994](./2019-benter-model.md): 本論文の多項ロジットを採用し、2段階で市場確率と結合。
- [Sung & Johnson 2007](./2007-sung-two-step-conditional-logit.md): 本論文の変数集合で1段階と2段階を比較。
- [Torné 2021](./2021-torne-hong-kong-softmax-nn.md): 本モデルを全結合ネットワークへ一般化した softmax NN。
- [Silverman 2012](./2012-silverman-hierarchical-bayesian-racing.md): 階層ベイズで拡張。
- [Silverman 2013](./2013-silverman-regularized-conditional-logit-frailty.md): 正則化した条件付きロジット。
- [Luce 1959](./1959-luce-individual-choice-behavior.md), [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 多項ロジットと explosion 尤度の理論的な基礎。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 特徴量なしの Plackett-Luce の推定法。

## 検索語

条件付きロジット, conditional logit, 多項ロジット, multinomial logit, MNL, softmax, 順位ロジット, rank-ordered logit, exploded logit, explosion, Chapman-Staelin, Plackett-Luce, ファンダメンタルモデル, fundamental handicapping, ハンディキャップ, 単勝, win betting, 大穴除外, longshot exclusion, 確率的効用, stochastic utility, 離散選択, discrete choice, McFadden, 疑似決定係数, pseudo R2, Bolton Chapman

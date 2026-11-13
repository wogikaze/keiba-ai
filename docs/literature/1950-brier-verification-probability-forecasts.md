---
title: Verification of Forecasts Expressed in Terms of Probability
authors: Brier Glenn W.
year: 1950
venue: Monthly Weather Review 78(1) 1-3
url: https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml
doi: 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
topic: evaluation-and-features
tags: brier-score, proper-scoring-rules, forecast-verification, calibration, reliability-diagram
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# 確率予報の検証：Brier スコアの原典（3ページの気象局論文）

> 一言で: 多クラスの確率予報を「予測確率と 0/1 の実現値の二乗誤差の和」で採点すれば、予報者は自分の信じる確率をそのまま書くのが得になり、「ヘッジ」で点数を稼げなくなる、と示した。あわせて予測確率帯ごとの実現頻度の表（今日の信頼性図）を使った校正の確認も提案している。

原本は AMS 公開の PDF（Internet Archive の保存版から取得、本文3ページ）。

## 問題意識：採点方式が予報を歪める

当時の天気予報の検証は「どの採点が良い予報を測るのか」で揉めていた。Brier は、採点で「最良」とされる予報が最も有用な予報とは限らず、予報者が採点方式を逆算して「ヘッジ」する、つまり自分が起こると思うこととは別の予報を出すことが問題だと指摘する (p.1)。

> one essential criterion for satisfactory verification is that the verification scheme should influence the forecaster in no undesirable way. (p.1)

予報を確率で表す場合にはこの条件を満たす採点方式が作れる、というのが論文の主張である (p.1)。

## 定式化

$n$ 回の機会のそれぞれで、事象は互いに排反で網羅的な $r$ 個のクラスのどれか1つで起こる。機会 $i$ の予測確率を $f_{i1},\dots,f_{ir}$（$\sum_j f_{ij}=1$）とし、$E_{ij}$ はクラス $j$ が起きたら 1、そうでなければ 0 とする。スコアは

$$P=\frac{1}{n}\sum_{j=1}^{r}\sum_{i=1}^{n}(f_{ij}-E_{ij})^2$$

である（式(2), p.1）。性質は次のとおり (p.2)。

- 完全な予報（起きたクラスに確率 1）で最小値 0。
- 最悪の予報（起きなかったクラスに確率 1）で最大値 **2**。今日よく使う2値版の Brier スコア（$\frac1n\sum(f_i-o_i)^2$、範囲 0〜1）は、原典の $r=2$ の値のちょうど半分になる。文献によって定義が2倍違うので、数値を比べるときは注意が要る。
- 毎回同じ予報を出すなら、各クラスの相対頻度 $p_j$ をそのまま出すのが最適で、そのときのスコアは $P'=1-\sum_j p_j^2$ になる（式(3)(4), p.2）。

## 数値例（Table 1, p.2）

降水あり/なし（$r=2$）の 10 回の予報。3回降水。

| 予報 | 内容 | スコア P |
|---|---|---|
| 予報者の実際の確率予報 | 0.7, 0.9, 0.8, 0.4, 0.2, 0, 0, 0, 0, 0.1 | 0.19 |
| 毎回 0.3（期間の実際の頻度） | 定数 | 0.42 |
| 毎回 0.2（気候値のつもり） | 定数 | 0.44 |

0.3 と 0.2 の差 (p.2) は、ある日と別の日を見分けられなくても「この期間は平年より降りやすい」と見抜ければ得点になることを示している。Brier はさらに、予報を 0 と 1 だけで書けば採点を出し抜けると考える予報者は「自分を騙しているだけ」だと書き、技量がないなら最頻クラスを断定するより気候値の確率を書くよう促される、と述べる (p.2)。

## 予測確率と実現頻度の比較（Table 2, p.3）

85 回の降水確率予報を予測確率の帯ごとに集計した表。今日の信頼性図（reliability diagram）にあたる。

| 予測確率帯 | 実際の降水割合 |
|---|---|
| 0.00–0.19 | 0.07 |
| 0.20–0.39 | 0.10 |
| 0.40–0.59 | 0.29 |
| 0.60–0.79 | 0.40 |
| 0.80–1.00 | 0.50 |

予測確率が上がると実現頻度も上がるが、高い帯ほど過大予報になっている。Brier はこれを「予報者は尺度を修正すべき」と読み (p.2)、今日の言葉でいう再校正（recalibration）を求めている。そのうえで、予測と実現の関係が良いだけでは有用さは分からず、どの帯にどれだけ予報が出たかも要る、と述べる。P が小さくなるには、相関が上がることと、極端な帯に入る予報の割合が増えることの両方が要る (p.2)。後に Murphy (1973) が信頼性（reliability）と分解能（resolution）に分けて定式化する区別の原型である。

## 著者が認める限界

結論 (p.3) では、気象局の短期予報開発部門で 6 時間降水予報に数か月使った経験を報告している。当初の批判の多くは方法の誤解か、「確信をもって降水を予報できることがいかに少ないか」に気づいた幻滅によるものだった、と書く。ただし「さらなる研究が必要」とも書いている。

## 批判的に読む

- 「ヘッジできない」ことの証明は本文になく、例示と主張にとどまる。期待スコアを最小にする予報が真の確率に一致すること（厳密な適正性）は、後の Gneiting & Raftery (2007) などで一般的に示される。
- Table 1 は 10 件、Table 2 は 85 件の例示にすぎず、統計的な検証ではない。
- 多クラスの P は各クラスを独立に二乗するだけで、クラスの順序を考えない。着順のような順序カテゴリでは、順序を考える RPS（Constantinou 2012）との使い分けが論点になる（Wheatcroft 2021 は RPS を批判している）。
- P は確率の差の二乗なので、確率 0.01 の馬が勝ったときの罰は小さい。対数スコアとは低確率域での感度が大きく違う（下記）。

## keiba-ai での使い方

- **評価指標の定義を固定する**: 単勝確率の評価で Brier を使うとき、レース内の全馬をクラスとする原典の多クラス版（1レース1サンプル、範囲 0〜2）と、馬ごとの2値版（1頭1サンプル、範囲 0〜1）では値も重み付けも違う。実験ログにはどちらかを明記する。推奨は、2値版を「馬単位の平均」と「レース単位の和の平均」の両方で報告すること。
- **気候値ベースラインとの比較**: 原典の $P'=1-\sum p_j^2$ は「何も知らない予報」の基準になる。競馬では「全馬 1/頭数」が気候値にあたり、さらに強い基準として市場のオッズから控除率を除いた確率がある。Brier スキルスコア $1-P_\text{model}/P_\text{market}$ で「市場をどれだけ上回るか」を測る。仮説: 単勝で市場を上回る Brier スキルが出ても、その大半は人気薄の確率の調整から来ていて、回収率には直結しない。
- **Table 2 型の確率帯別集計**: 単勝確率を 0–5%, 5–10%, … の帯に分けて実際の勝率を並べる。人気薄の帯で過大予測が出れば、favorite-longshot bias をモデルが逆向きに抱えていることになる。再校正（Platt, isotonic）を当てる前後でこの表を並べる。
- **対数損失との併用**: 穴馬の勝利に対しては Brier の罰が小さく log loss の罰が大きい。どちらで改善したかを両方見ることで、改善が人気馬の確率から来たのか人気薄の確率から来たのかを切り分ける。

## 関連ノート

- [Murphy 1973](./1973-murphy-brier-decomposition.md): Brier スコアを信頼性・分解能・不確実性に分解した。Table 2 の考えを定式化した後継。
- [Gneiting 2007](./2007-gneiting-proper-scoring-rules.md): Brier（二次スコア）が厳密に適正であることを一般理論の中に位置づける。
- [Constantinou 2012](./2012-constantinou-rps-football.md): 順序カテゴリ向けの RPS。原典の多クラス P が順序を無視する点への対案。
- [Wheatcroft 2021](./2021-wheatcroft-case-against-rps.md): RPS への反論。Brier や対数スコアとの比較。
- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md): 学習器の確率を Brier と信頼性図で評価し、Platt と isotonic で校正する。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 賭けの成績には正解率より校正が効くという主張。Brier 型評価の応用先。

## 検索語

Brier スコア, ブライアスコア, 二乗誤差, 確率予報の検証, 予報検証, 降水確率, 適正スコア, 厳密に適正なスコアリングルール, ヘッジ, 気候値, 信頼性図, 校正, 再校正, Brier score, quadratic score, probability score, PS, mean squared error of probability, forecast verification, proper scoring rule, hedging, climatology, reliability diagram, calibration, Monthly Weather Review, U.S. Weather Bureau

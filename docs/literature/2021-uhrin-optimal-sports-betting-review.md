---
title: Optimal sports betting strategies in practice: an experimental review
authors: Uhrín Matej, Šourek Gustav, Hubáček Ondřej, Železný Filip
year: 2021
venue: IMA Journal of Management Mathematics
url: https://arxiv.org/abs/2107.08827
doi: 10.1093/imaman/dpaa029
topic: betting-strategy
tags: kelly, fractional-kelly, modern-portfolio-theory, horse-racing, review, risk-management
verified: fulltext
importance: high
source: downloaded
source_version: preprint
---

# Kelly・最大シャープ比とそのリスク管理版を、韓国競馬・NBA・サッカーの実データで同じ手順で比較

> 一言で: 素の Kelly と最大シャープ比は、モデルが市場より劣る（KL で不利な）NBA とサッカーで全経路が破産した。fractional Kelly・ドローダウン制約・分布ロバスト Kelly などのリスク管理を加えるとどの競技でも破産率 0% になり、実用上は「分数を調整した fractional Kelly」が最も無難という結論。韓国競馬の単勝では市場より良いモデルがあり、素の Kelly でも中央値で資金 4.1 倍だった。

原本は arXiv v1（2021年7月）。掲載誌版（IMA J. Manag. Math.）の巻号・ページは未確認で、ページは arXiv 版。

## 問題設定

ブックメーカーの固定オッズ $o_i$ に対して、自分の推定確率 $p_i$ で資金の配分 $f$ を決める (p.2-3)。

- オッズにはマージンがあり、ブックメーカーもプレイヤーも真の確率を知らない（推定にはバイアスがある）(p.4-5)。
- 1試合に複数の結果（相互排他）があり、複数の試合が同時に並ぶ（parallel games）(p.6)。
- 資金の増え方は加法的（定額）と乗法的（比例）がある (p.7)。

## 比較した戦略

| 戦略 | 中身 | 節 |
|---|---|---|
| AbsDisc | 自分と市場の確率の差に比例して賭ける（非公式な経験則） | 4.1 |
| MaxEvFrac | 期待値最大の結果に一定割合 | 4.1 |
| MSharpe | シャープ比最大のポートフォリオ（Markowitz 系） | 4.2.1 |
| Kelly | 期待対数資金の最大化 | 4.3 |
| 〜Frac | 上記の配分を ω 倍に縮める | 5.2 |
| 〜FracMax | さらに1回の賭けを m 以下に制限 | 5.1 |
| KellyDrawdown | [Busseti 2016](./2016-busseti-risk-constrained-kelly.md) の $\mathbb{E}[(O\cdot f)^{-\lambda}] \le 1$ 制約 | 5.3 |
| KellyRobust | [Sun 2018](./2018-sun-distributional-robust-kelly.md) の箱型不確実性集合（各確率を ±η 倍）での最悪ケース Kelly | 5.4 |

(p.13, Table 1)。最適化は cvxpy（ECOS、失敗時 SCS）(p.15)。

## データ

| | 競馬 | バスケットボール | サッカー |
|---|---|---|---|
| 市場 | 韓国 KRA の単勝（パリミュチュエル） | NBA マネーライン（Pinnacle 締切） | 各国リーグ 1X2（Pinnacle 開始オッズ） |
| 件数 | 2,700 レース | 16,000 試合 | 32,000 試合 |
| 結果数 n | 6〜16 | 2 | 3 |
| モデルの的中率 / 市場 | 0.512 / 0.503 | 0.68 / 0.70 | 0.523 / 0.537 |
| マージン | 0.2 | 0.038 | 0.03 |
| KL 優位 $A_{KL}$ | ≈ +0.0022 | ≈ −0.0146 | ≈ −0.013 |
| モデル | 条件付きロジスティック回帰 | 選手統計の畳み込みネット | 勾配ブースティング（2017 年 Soccer Prediction Challenge 優勝モデル） |

(p.13-15, Table 2-4)。競馬はパリミュチュエルだが、最終の票数から計算したオッズを固定オッズとみなす (p.14)。市場の推定が大衆の意見だけで精度が低いので、モデルが KL で優位に立てる一方、控除率は大きい。

$A_{KL}$ はプレイヤーと市場のクロスエントロピーの差で、Kelly の成長率はこれに比例する (p.13)。

## 評価手順

1. 予測はすべて時系列順の標本外予測 (p.15)。
2. データを学習用と評価用に分け、学習用でハイパーパラメータ（ω, m, α, β, η）をグリッド探索 (p.15)。
3. 選択基準: 最終資金の中央値を最大化。ただし最終資金の 5% 分位点が 0.9 を超えること（「まず生き残る」）(p.15)。
4. 各部分で試合の順番をシャッフルし、10% をランダムに除いた 1,000 本の資金推移を作って統計を取る (p.15)。
5. 破産は初期資金の 0.01% を一度でも下回ること (p.16)。

## 結果

競馬（韓国単勝）(p.16, Table 5, 抜粋):

| 戦略 | 最終資金の中央値 | 平均 | 最小 | 破産率 |
|---|---|---|---|---|
| AbsDisc | 0.0019 | 0.03 | 4e-08 | 85.2% |
| MaxEvFrac | 0.86 | 2.13 | 2e-09 | 36.1% |
| Kelly | 4.11 | 15.6 | 7e-05 | 0.6% |
| MSharpe | 3.92 | 17.8 | 9e-06 | 12.1% |
| KellyFrac | 3.39 | 14.2 | 0.003 | 0% |
| KellyFracMax | 3.49 | 13.8 | 0.0057 | 0% |
| KellyDrawdown | 3.3 | 13.7 | 0.009 | 0% |
| KellyRobust | 2.97 | 4.1 | 0.08 | 0% |

NBA（p.17, Table 6）では Kelly と MSharpe の破産率 100%、KellyFrac の中央値 2.4、KellyRobust 1.39。サッカー（Table 7）でも素の2戦略は破産率 100%、KellyDrawdown の中央値 10.25、KellyFrac 10.05。

読み取れること (p.17-19):

- 非公式な経験則（AbsDisc, MaxEvFrac）は、モデルが優位な競馬でさえ高い確率で破産する。
- 素の Kelly / MSharpe は KL で不利な市場では必ず破産する。
- リスク管理を加えると、**KL で不利な NBA・サッカーでも利益が出た**。
- Kelly 系は中央値が高く、MSharpe 系は平均が高い。目的関数（対数か期待値か）どおり。
- ドローダウン制約は、ずっと単純な fractional Kelly とほぼ同じ成績。
- 分布ロバスト Kelly は最終資金が最も低いが、最小資金が最も高く最も安定。
- 1回の賭けの上限は、競馬では改善したが NBA では悪化し、結論が出ない (p.19)。

## 批判的に読む

- **KL で不利なのに利益が出る理由が不明確**。NBA・サッカーで中央値 2〜10 倍は大きい。ハイパーパラメータの選択は学習用部分で行っているが、評価用の 1,000 経路は同じ試合集合の並べ替えで、独立な期間での検証は1回だけ。[Hubáček 2020](./2020-hubacek-beating-market-bad-model.md) の脱相関の議論が背景にあると思われるが、この論文の中では説明されていない。
- **学習用・評価用の分割比率や期間が明記されていない**（本文で未確認）。
- **競馬は確定オッズを固定オッズとみなす**。締切後の最終オッズで賭けられる前提で、自分の賭けによるオッズ低下もない。控除率 20% の市場で KL 優位 0.0022 は小さく、実際に締切前のオッズで賭けると結果は変わりうる。
- 選択基準（中央値最大 + 5% 分位点 > 0.9）は Kelly 系に有利と著者も認める (p.18)。
- 抄録は「適応的な（adaptive）fractional Kelly」を推すが、本文の手法は学習用データで ω を選ぶだけで、時間とともに ω を変える仕組みはない。

## keiba-ai での使い方

- **バックテストの評価手順の雛形**: (1) 時系列で学習・検証・評価を分ける、(2) 検証期間で ω などを選ぶ、(3) 評価期間でレース順をシャッフルし一部を抜いた多数の資金推移を作り、中央値・平均・最小・破産率を出す。これを keiba-ai の賭け戦略評価の標準にする。
- **KL 優位 $A_{KL}$ を最初に測る**: モデルの単勝確率と市場の確率（オッズから控除率を除いたもの）の対数損失の差を、評価期間で計算する。負なら素の Kelly は破産する。正でも控除率が大きいので、fractional Kelly が前提。
- **実験案**: 仮説「JRA の単勝で、KellyFrac・KellyDrawdown・KellyRobust の最終資金の中央値はほぼ同じで、最小資金は KellyRobust が最も高い」。韓国競馬の結果（中央値 3.0〜3.5、破産 0%）と同じ傾向になるかを見る。
- 単勝以外（複勝・馬連）を組み合わせる場合は、この論文の枠組み（1 レース = 相互排他な結果）を超えるので、[Jacot 2023](./2023-jacot-kelly-non-mutually-exclusive-bets.md) の定式化が必要。

## 関連ノート

- [Busseti 2016](./2016-busseti-risk-constrained-kelly.md): KellyDrawdown の元論文。本論文では fractional Kelly と同程度という評価。
- [Sun 2018](./2018-sun-distributional-robust-kelly.md): KellyRobust の元論文。本論文で最も安定と確認された。
- [Hubáček 2020](./2020-hubacek-beating-market-bad-model.md): 同じグループ。精度で劣るモデルでも利益を出す脱相関の議論。NBA データも共通。
- [Hubáček 2019](./2019-hubacek-exploiting-betting-market-ml.md): NBA の畳み込みネットモデルの出典。
- [MacLean 1992](./1992-maclean-growth-versus-security.md), [MacLean 2010](./2010-maclean-kelly-good-bad-properties.md): fractional Kelly の理論的根拠。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md): 推定誤差に応じた Kelly の縮小。本論文の ω の理論版。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 競馬データのモデル（条件付きロジット）の系統。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): Kelly の実践での使い方。
- [Whelan 2025](./2025-whelan-multiple-mutually-exclusive-outcomes.md): 相互排他な多結果での最適賭けの理論。

## 検索語

賭け戦略の比較, 資金管理, バンクロール管理, ケリー基準, 分数ケリー, 最大シャープ比, 現代ポートフォリオ理論, ドローダウン制約, 分布ロバスト, 賭け上限, 破産率, KL優位, 韓国競馬, 単勝, NBA, サッカー, betting strategies, bankroll management, fractional Kelly, maximum Sharpe ratio, modern portfolio theory, drawdown constraint, distributionally robust Kelly, ruin probability, KL advantage, Korean Racing Authority, KRA, Pinnacle, experimental review

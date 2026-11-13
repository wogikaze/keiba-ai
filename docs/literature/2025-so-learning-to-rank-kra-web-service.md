---
title: Machine Learning-based Learning-to-Rank Approach for Horse Race Prediction and Web Service Development
authors: So Yubin, Woo Eunbi, Lee Hanjun
year: 2025
venue: Journal of The Korea Society of Computer and Information 30(11) 311-318
url: https://journal.kci.go.kr/jksci/archive/articleView?artiId=ART003266151
doi: 10.9708/jksci.2025.30.11.311
topic: machine-learning
tags: learning-to-rank, lambdarank, lightgbm, xgboost, catboost, korea, kra, ndcg
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# ソウル競馬1年分で LightGBM・XGBoost・CatBoost の順位学習を比べ、予想サイトを作った（学部生の研究）

> 一言で: 韓国馬事会のソウル 2024年5月〜2025年4月・9,140頭・回で、LightGBM（rank_xendcg）、XGBoost（rank:pairwise）、CatBoost（YetiRankPairwise）を比べた。CatBoost は NDCG・MAP で最良だったが単勝の的中率は 3.14% しかなく、LightGBM と XGBoost の単勝的中率は 18.85%。的中率はすべて 191 レースから出した値で、標本が小さい。馬 ID を特徴量に入れたうえで無作為な交差検証をしており、リークの疑いもある。

本文は韓国語（要旨・表は英語）。ページは PDF のページ番号（library の `=== page N ===`）で書く。雑誌の印刷ページは PDF ページ + 310。

## 位置づけ

明知大学の経営情報学科の学部生2人と指導教員の論文（p.1, p.8）。先行研究の [Chung 2024](./2024-chung-learning-to-rank-seoul.md) は pair-wise が point-wise より良く、CatBoost Ranker が最良と報告した。本研究は、pair-wise は2頭の比較に限られ、レース全体の順位を一度に学べないと考え、list-wise の LambdaRank を LightGBM で試す（p.2）。

## データ（p.3–4）

| 項目 | 内容 |
|---|---|
| 市場 | 韓国のソウル競馬場（国内の売上の 55%） |
| 期間 | 2024年5月〜2025年4月の1年間 |
| 規模 | 9,140頭・回（馬・騎手・調教師の3ファイルを結合） |
| 欠測 | 項目に応じて 0 か平均で埋める |

主な特徴量（p.4, Table 4）:

- 馬の直近5走の平均着順（`prev_5_avg_rank_in_race`）、通算の平均着順（`avg_ord`）、勝率（`avg_winRate`）、出走回数（`game_attendance`）、直近1年の1着・2着の割合
- 馬と騎手の組み合わせの勝率・平均着順、調教師の勝率・平均着順
- 騎手・調教師の通算1〜3着回数（`ord1CntT_jk` など。騎手の1着回数は平均 379、最大 2,246）
- 含水率、馬場状態、ゲート番号、休養日数、年齢、季節（one-hot）
- 馬の個体番号（`hrNo_category`）と出走番号をカテゴリ変数として使う

## モデルと設定

| モデル | 目的関数 | 系統 |
|---|---|---|
| LightGBM | `rank_xendcg` | list-wise |
| XGBoost | `rank:pairwise` | pair-wise |
| CatBoost | `YetiRankPairwise` | pair-wise |

（p.3, Table 2）

ハイパーパラメータは、学習率 0.05、LightGBM は num_leaves 31、XGBoost と CatBoost は深さ 6、XGBoost は subsample と colsample_bytree が 0.8、どれも 200 ラウンドで early stopping 10（p.6, Table 7）。調整の方法は書かれていない。

なお、LightGBM の `rank_xendcg` は LambdaRank ではなく、XE-NDCG という別の list-wise 損失である。本文は「LightGBM の rank_xendcg で LambdaMART を実装した」と書いており（p.3）、用語が混乱している。

### 分割

開催日とレース番号から `group_id` を作り、同じレースの馬が別のフォールドに分かれないようにした5分割交差検証（p.4）。著者はこれでデータの漏れを「厳格に防いだ」と書く。ただし時系列での分割ではない。

## 結果

ランキング指標（p.5, Table 5。5分割の平均）:

| 指標 | LightGBM | XGBoost | CatBoost |
|---|---|---|---|
| NDCG | 0.8725 | 0.8789 | **0.8895** |
| MAP | 0.2263 | 0.2291 | **0.4204** |
| MRR | 0.3940 | **0.3943** | 0.1785 |
| 着順完全一致率 | **0.1425** | 0.1374 | 0.0768 |

フォールド間の標準偏差は ±0.02 以内で、モデル間の平均の差は 95% 水準で有意でなかった（p.5）。

券種別の的中率（p.6, Table 6）:

| 券種 | LightGBM | XGBoost | CatBoost |
|---|---|---|---|
| 単勝 | 18.85% | 18.85% | 3.14% |
| 複勝（연승） | 47.12% | 52.88% | 14.66% |
| 馬連（복승） | 7.85% | 7.85% | 0.00% |
| 馬単（쌍승） | 5.76% | 3.14% | 0.00% |
| 3連複 | 3.14% | 5.24% | 0.00% |
| ワイド（복연승） | 17.28% | 19.37% | 1.05% |
| 3連単 | 1.05% | 0.52% | 0.00% |

重要度の上位は、直近5走の平均着順、通算平均着順、斤量、年齢の順（p.6, Figure 1）。

著者の結論: 順位の質（NDCG・MAP）なら CatBoost、実際の的中なら LightGBM と XGBoost。実用が目的なので LightGBM が最も有効（p.7）。後半は React + Django + PostgreSQL + AWS S3 の予想サイトの説明で、利用者が勝率の閾値を決めて「安全志向」「積極参加」などの賭け方を選べる（p.6–7）。

## 批判的に読む

- **的中率は 191 レースだけで出している。** 表の数字はすべて「k / 191」に一致する（18.85% = 36/191、3.14% = 6/191、1.05% = 2/191、0.52% = 1/191）。本文も「全 191 レースの平均」と書く（p.5）。3連単の 1.05% は2回、0.52% は1回当たっただけで、モデルの差を論じられる標本ではない。
- **CatBoost の単勝 3.14% は無作為より悪い。** 1レース10頭前後なら、無作為でも 10% 近く当たる。NDCG が最良のモデルの単勝的中率が無作為を下回るのは、スコアの向き（大きいほど上位か下位か）を取り違えたか、関連度ラベルの定義を誤っている可能性が高い（推測）。著者は「list-wise は1位より全体の順位を重視するため」と説明するが（p.5）、CatBoost は pair-wise で、この説明は通らない。
- **馬 ID と無作為分割の組み合わせ。** `hrNo_category`（馬の個体番号）をカテゴリ変数に入れ、時系列でなく無作為に分けている。同じ馬の将来のレースが学習に入るので、モデルは馬ごとの強さを ID で覚えられる。これは実運用では使えない情報である。
- **通算成績の時点。** 騎手・調教師の通算1〜3着回数、馬の平均着順・勝率が、レース時点の値か取得時点の値か書かれていない。[Chung 2024](./2024-chung-learning-to-rank-seoul.md) と同じ問題がある。
- **NDCG を先行研究と比べられない。** 著者は NDCG 0.8895 を [Chung 2024](./2024-chung-learning-to-rank-seoul.md) の 0.7149 と比べ、約 0.17 改善したとする（p.5）。しかし関連度（ゲイン）の定義も期間もデータも違うので、この比較に意味はない。
- **ROI を計算したと書きながら、数字を出していない。** 「実際の配当（控除率 15%）を反映して ROI と的中率を計算した」とあるが（p.5）、ROI の表は無い。
- LightGBM と XGBoost の単勝・馬連の的中率がまったく同じ（18.85%、7.85%）。偶然かもしれないが、確かめようがない。

## keiba-ai での使い方

- **評価の標本の大きさの目安。** 的中率の差を論じるなら、1レースの頭数と的中率から信頼区間を計算し、191 レースではおよそ ±5〜6 ポイント（単勝 19% のとき）もぶれることを確かめておく。keiba-ai の検証期間は数千レースを確保する。
- **ID 系の特徴量は時系列の分割でだけ評価する。** 馬・騎手・調教師の ID をそのまま特徴量にするなら、無作為な交差検証では効果を過大に見積もる。必ず「学習期間より後のレース」で検証する。
- **スコアの向きの点検。** 順位学習の出力を券種の予想に変えるとき、単勝的中率が無作為（1/頭数）を下回ったら、まずラベルとスコアの向きを疑う。
- **目的関数の比較。** LightGBM の `lambdarank` と `rank_xendcg`、CatBoost の `YetiRank` を同じ時系列分割で比べる実験は keiba-ai でも意味がある。比較するときは NDCG だけでなく、スコアを softmax で確率にしたあとの1着の log loss で評価する。

## 関連ノート

- [Chung 2024](./2024-chung-learning-to-rank-seoul.md): 同じソウルの KRA データで順位学習を比べた先行研究。本研究はこれを list-wise に広げようとした。
- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): RankNet・LambdaRank・LambdaMART の原典。
- [Ke 2017](./2017-ke-lightgbm.md): LightGBM の原典。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md): 競馬の予測を NDCG で評価した先行例。
- [Fujisawa 2024](./2024-fujisawa-ranknet-condition-datasets.md): 日本の競馬で RankNet を使った研究。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): リークを意識した評価。本研究の ID 特徴量と無作為分割の問題を点検する観点。

## 検索語

順位学習, ランキング学習, learning to rank, LTR, list-wise, pair-wise, LambdaRank, LambdaMART, rank_xendcg, XE-NDCG, YetiRank, rank:pairwise, LightGBM, XGBoost, CatBoost, NDCG, MAP, MRR, 韓国, ソウル, 韓国馬事会, KRA, 単勝, 複勝, 馬連, 馬単, ワイド, 3連複, 3連単, 券種別的中率, Webサービス, 予想サイト, Django, React, 馬ID, リーク, 交差検証, GroupKFold

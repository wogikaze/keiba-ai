---
title: KeibaAI — Japanese Horse Racing Prediction System（ListNet と Benter 較正によるワイド戦略）
authors: bunyu422
year: 2026
venue: GitHub
url: https://github.com/bunyu422/keiba-ai
topic: practitioner
tags: grey-literature, github, netkeiba-scraping, listnet, lambdarank, lightgbm, benter-calibration, odds-free, wide, auto-betting, target-encoding
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# ListNet（PyTorch）と LightGBM LambdaRank を比べ、Benter 較正した確率でワイド top2 を買う個人開発の記録

> 一言で: 大学時代に始めた個人開発。netkeiba をスクレイピングし、LightGBM（LambdaRank）からペアワイズ損失の ListNet 系 NN に移行した。予測スコアを Benter 流の α-β 較正で確率に変換し、中京のワイド top2 を 1 点買う戦略を時系列 5-fold で評価した。回収率は平均 83.6%（オッズ込み・odds-free とも）で、払戻率 77.5% を上回るが 100% には届かない。発走 3 分前に予測から IPAT 購入までを Selenium で自動化している。

原本は GitHub の README（`library/2026-bunyu422-listnet-wide/source.txt`）。README は 2026 年 6 月作成。コード一式も公開されている。

## データ

- 入手元: netkeiba.com のスクレイピング（`src/common/scraping.py`）。当日の開催情報・出走表・オッズも netkeiba から取る（「自動購入フロー」の節）。
- 期間・件数: README に学習期間・件数の記載はない。評価は中京競馬場の 2022〜2024 年（「評価設定」の表）。
- 新馬戦は自動購入の対象から外している。

## 特徴量

「Feature Engineering」の節に挙がっているもの:

- 適性スコア: 過去走の距離・馬場・フィールドから加重平均で算出。
- 出走間隔クラス: 連闘(0)〜長期休養(4)の 5 クラス。
- 上がり 3F のレース内ランク（前走の末脚をそのレース内で順位付け）。
- 馬体重トレンド: 過去 5 走の線形回帰の傾き。
- 同距離・同場所の過去実績率。
- Winner Baseline 差分: 勝ち馬平均との差。
- Target Encoding（K-fold 内で計算、平滑化つき）と、交互作用 TE: `['距離グループ','父馬']`、`['騎手','距離']`、`['騎手','フィールド']`。fold 内で計算してリークを防ぐと明記している。

工夫として目立つのは「Odds-Free Modeling」の節。人気・オッズを特徴量に入れると、他の特徴量が軽視されて予測が市場に収束し、直前のオッズ変動にも弱くなる、という理由で、人気・オッズを除いたモデルを並行して学習している。

## モデルと目的変数

- 2 系統（「Two Approaches」の表）:
  - ListNet: PyTorch の MLP（ListNet / ListNet2 / ListNetGRU の実装がある）。損失は `utility_aware_ranking_loss_roi` というペアワイズ損失で、ペアの形（hinge / logistic / bpr / exp）と重み（value_i / roi / ev_i / rank_focus）を組み合わせられる。現在は `logistic` + `value_i`（関連度の高い馬を重視）を使う。
  - LightGBM: LambdaRank、NDCG@k。
- 目的変数: 1 着（win）と 2 着以内（top2）の 2 種。
- 確率化: 「Benter Calibration」の節。予測スコアを α-β 較正で確率に変換し、fold 間の α, β の中央値を固定値として使うと ROI が安定した、とある。Benter（1994）の第 2 段（基本モデルと市場確率の結合）ではなく、スコアを softmax の温度とバイアスで確率に合わせる用途に近い。
- `src/common/bandit.py` にバンディットアルゴリズムがあるが、README に説明はない。

## 評価

- 分割: 時系列 5-fold CV（`src/common/splits.py`）。対象は中京、2022〜2024 年。
- 賭け方: 各レースで予測確率 top2 の 2 頭のワイドを 1 点買い。実運用では単勝推奨馬の単勝と、ワイドながしも買う（「自動購入フロー」）。
- 回収率 = 払戻金額 / 購入金額。払戻は確定払戻と思われるが、README に明記はない。
- 基準線: ワイドの払戻率 77.5%（控除率 22.5%）。

## 結果

「ワイド top2 ROI（5-Fold CV）」の表:

| Signal | オッズ使用 | Fold1〜5 | 平均 |
| --- | --- | --- | --- |
| benter_prob（win） | 使う | 86.9 / 82.2 / 83.8 / 82.5 / 82.4% | 83.6% |
| benter_prob_free（win） | 使わない | 85.8 / 82.6 / 80.4 / 84.7 / 84.6% | 83.6% |
| benter_prob_t2f（top2） | 使わない | 80.8 / 80.1 / 83.7 / 83.8 / 80.8% | 81.8% |

著者は、全 Signal が払戻率 77.5% を上回るので「統計的に有意な予測精度を持つ」とし、odds-free モデルがオッズ込みと同じ 83.6% を出したことを重視している。2 着以内を直接学習した t2f はむしろ低い。

## 落とし穴と教訓（著者の記述）

- 「Engineering Philosophy」の節で、データリークによる「ぬか喜び」を何度も経験したと書いている。高スコアはまず疑い、偶然ではないかを確かめる姿勢を強調する。
- ListNet 移行では損失関数の設計が最も難しかった、とある（「Background」の節）。

## 批判的に読む

- 77.5% を超えたことは「予測力がある」証拠として弱い。ワイドは低オッズの組み合わせほど控除後の期待値が高い（本命・大穴バイアス）ので、単に人気上位 2 頭のワイドを買うだけでも 77.5% を上回る可能性が高い。比べるべき基準は「人気 1・2 番のワイド top2」の回収率で、README にはそれがない。odds-free モデルが市場と同じ 83.6% になったのは、結局人気馬に近い馬を選んでいるだけかもしれない。
- 有意性の検定はしていない。各 fold の回収率のばらつき（80〜87%）と 1 fold あたりのレース数が書かれていないため、信頼区間が分からない。
- 「時系列 5-fold」の中身（拡張窓か、前後どちらの fold も学習に使うのか）が不明。K-fold 内 TE を使っている点からも、未来の fold で学習した TE が過去の fold に入っていないかは README だけでは確認できない。
- 評価は中京 1 場のみ。競馬場ごとのモデルなのか、全場で学習して中京だけ評価したのかも書かれていない。
- 実運用では発走 3 分前のオッズで単勝を判断するが、評価は（おそらく）確定払戻。直前オッズと確定オッズのずれは評価されていない。

## keiba-ai での使い方

- 「人気・オッズを抜いたモデル」と「入れたモデル」を並べて同じ戦略で評価する、という比較設計はそのまま使える。ただし基準線には控除率ではなく「人気順で同じ買い方をした場合」を必ず置く。
- ペアワイズ損失に払戻（value_i / roi）で重みを付ける設計は、回収率を直接最適化したいときの候補。過学習しやすいので、LambdaRank との比較実験として ADR を立ててから試す。
- fold 間で求めた較正パラメータの中央値を固定する手法は、較正パラメータの時系列ドリフトを抑える安価な手として試せる。

## 関連ノート

- [Benter 2019（1994 年論文の再録）](./2019-benter-model.md): α-β 較正と市場確率の結合の元ネタ。
- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): LambdaRank の原典。ListNet との比較の基礎。
- [Ke 2017](./2017-ke-lightgbm.md): LightGBM。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 本命・大穴バイアス。ワイド top2 が 77.5% を超えやすい理由。
- [Kobayashi 2023](./2023-kobayashi-odds-dependent-prediction.md): オッズに依存した予測と依存しない予測の比較。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): リークを意識した評価設計。
- [Tamiya 2021](./2021-tamiya-ranknet.md): 日本の実践者による RankNet。

## 検索語

ListNet, ペアワイズ損失, LambdaRank, Benter 較正, α-β calibration, odds-free model, オッズなしモデル, ワイド top2, 払戻率 77.5%, 中京, Target Encoding, 交互作用 TE, 自動投票, IPAT Selenium, pairwise ranking loss, value-weighted loss, listwise learning to rank

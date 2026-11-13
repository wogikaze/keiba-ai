---
title: Horse Quant Platform
authors: pranay123-stack
year: 2026
venue: GitHub
url: https://github.com/pranay123-stack/horse-quant-platform
topic: practitioner
tags: grey-literature, uk-racing, synthetic-data, pre-registration, merge-asof, leakage-test, encompassing-regression, bonferroni, value-betting, methodology
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 英国競馬の定量ベッティング基盤: 合成データでしか動かしていないが、事前登録と検証ゲートの設計が参考になる

> 一言で: 英国・アイルランド競馬向けに、データ取得から時点整合な特徴量89個、較正済み確率、期待値戦略、ウォークフォワード、事前登録した判定関数までを作った基盤。データ API の契約が切れているため、README の数値は**すべて合成データ**（市場に15%のノイズを入れて作った、優位が存在するように設計したデータ）のもので、実市場について何も言えないと明記している。価値は結果ではなく、先読みを構造的に防ぐ実装、事前登録、市場の寄与を測る encompassing 回帰などの設計にある。

## データ

- 想定は The Racing API（英国・アイルランドの出馬表、結果、ブックメーカーのオッズ）。契約が inactive のため実データは未取得（「Real data validation」）。
- 実際の数値は合成データ: 2018〜2026年、6,206レース、49,648頭立て、馬1,200頭、オッズ見積もり36万件（REAL_DATA_AUDIT.md）。
- 実データ用には、最低5年分、出走馬の60%以上にオッズ、95%以上に結果、**発走後に記録されたオッズが1件もないこと**を検証ゲートにしている。

## 特徴量

- 89個の時点整合（point-in-time）特徴量。すべて1つの関数 `as_of_join` を通して付ける。中身は `pd.merge_asof(..., direction="backward", allow_exact_matches=False)` で、対象レースの時刻より**厳密に前**の履歴行だけを選ぶ。`allow_exact_matches=False` が当該レース自身の結果を除く要（「The one guarantee everything rests on」）。
- 市場由来特徴量（`mkt_*`、`market_*`）を含む。

## モデルと目的変数

- 1着の確率。ロジスティック回帰、LightGBM、XGBoost。出力は較正後に**レース内で正規化**する（較正は1頭ごとの写像なので、正規化の前に当てる）。
- 選択基準は race log loss = −mean(log p_winner)。一様モデルの基準は log(頭数)。1頭ごとの log loss は「誰も勝たない」で良く見えてしまうので使わない。
- 期間を4つに分ける: 学習、早期終了用、較正用、テスト。早期終了に使った区間で較正器を学習すると補正が弱くなりすぎるため。学習の終わりから14日のエンバーゴ。

## 評価

- 戦略は年ごとに再学習するウォークフォワード。予測は1回だけ作り、すべての戦略で同じ予測を使い回す（戦略差と再学習のぶれを混同しない）。
- **確率は合意価格、賭けは最良価格**: 複数ブックメーカーの最良価格から確率を作ると、合計が1を下回ることがあり、何もないところに優位が生まれる。確率は平均価格から、賭けは最良価格で。
- 事前登録（`protocol.py`、内容のハッシュで固定）: 分割、主仮説1つ（LightGBM・EV≥5%・均等・スリッページ2%・手数料2%）、判定規則（200件以上、t≥2.0、半数以上の年で黒字）、副次検定12本（Bonferroni で閾値 t≥2.89）。結果を見た後に変えるとハッシュが変わり実行が失敗する。
- **encompassing 回帰**: `logit P(win) ~ logit(p_market) + logit(p_model)`。市場を条件にしたときのモデルの係数で、価格が知らないことをモデルが知っているかを測る。

## 結果（すべて合成データ）

- 「Results」: LightGBM の race log loss 1.339（一様 2.079）、ECE 0.0087。較正（isotonic・Platt）はどのモデルでも log loss を悪化させた。もともと log loss で学習し、クラス重み付けをしていないので較正済みに近く、2,816行・勝ち馬約350頭で補正器を当てるとノイズが増える。
- 「Strategy comparison」（4,746レース、£10均等）: EV 閾値の戦略は ROI +18〜+20%。絞り込みなしの EV 規則は賭け数が倍、平均オッズ 3.5→6.7、ROI 半減（+8.0%）で、「EV = p·odds − 1 はモデル誤差をオッズで増幅し、裾の較正ノイズを大穴への自信ある賭けに変える」。
- 「Market dependency」: 市場確率だけで賭けると賭け数0（負の対照が通る）。市場特徴量を除いたモデルは −5.6%。つまり優位は独立の情報ではなく、**市場価格のノイズ除去**。
- 「How fragile」: 粗利 +21% がスリッページ10%・手数料5%で +5.5% まで落ちる。
- 「Testing that the guarantee holds」: 未来のレースを足して特徴量を作り直し、過去の値が変わらないことを確かめるテストが、**データ全体の中央値で欠損補完していたリーク**を実際に見つけた。

## 落とし穴と教訓

- 欠損補完の統計量（中央値など）を全期間で計算するのは、気づきにくいリーク。例外も出ず、値も不自然に見えない。
- リーク検出を特徴量名の拒否リストでやると、想像した漏れしか捕まらない。「1つの特徴量で勝ち馬をほぼ完全に分けられるか」という振る舞いで検査する。最初の実行で、精算用に持っていた `finishing_position` が誤検出された。ラベル列の一覧は、手書きのコピーではなく、それを作るクエリの隣にある正本を参照する。
- 合成データでの報告書は、一見して実データの報告書と区別がつかない。データ源が合成なら検証ゲートで止める。

## 批判的に読む

- 実データの結果が一つもない。合成データは優位が存在するように作られているので、正の ROI は「エンジンが優位を見つけられる」ことの確認（正の対照）にすぎない。
- 合成市場のノイズ15%は現実の市場よりはるかに大きいと著者も書いている。市場依存の実験（市場特徴量なしで負ける）は、実データでは優位がさらに小さいことを示唆する。
- コード量（約2.3万行、テスト1,081本）は LLM 支援で短期間に書かれたと推測され、実装の正しさは README からは確認できない。ノートで使うのは設計の考え方に限るべき。

## keiba-ai での使い方

- **特徴量の付与を `merge_asof(..., allow_exact_matches=False)` 相当の1関数に集約し、未来のレースを追加しても過去の特徴量が変わらないテストを置く**。欠損補完・標準化の統計量も学習期間だけで計算しているかを、このテストで同時に確かめられる。
- 実験の `config.yaml` に、主仮説（モデル・賭け方・閾値）を1つだけ書き、副次比較の数から多重比較の閾値を決めておく。CLAUDE.md の「仮説は実行前に書く」を、ハッシュで固定する仕組みに近づけられる。
- encompassing 回帰（市場ロジットとモデルロジットの同時回帰）を、[Benter 2019](./2019-benter-model.md) の第2段結合の推定と同じ枠で報告する。
- 学習・早期終了・較正・テストの4区間分割と、早期終了と較正を分ける理由は、LightGBM + isotonic の構成でそのまま使える。
- EV 規則を使うときは、オッズ帯別の回収率と、帯ごとの「実際の的中率 / 予測確率の平均」を必ず出す。

## 関連ノート

- [Benter 2019](./2019-benter-model.md): 市場とモデルの結合。encompassing 回帰は同じ発想。
- [Bailey 2014](./2014-bailey-deflated-sharpe-ratio.md)、[Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): 多重比較の補正。
- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md): 較正が効くモデルと効かないモデル。
- [Franck 2010](./2010-franck-bookmakers-vs-betting-exchange.md): ブックメーカーと取引所の価格。
- [justinsuo 2026](./2026-justinsuo-hkjc-edge-lab.md): 同じく事前の判定とプラセボを持つ HKJC の研究ツール（こちらは実データ）。
- [stevw 2026](./2026-stevw-hkjc-ml-research-platform.md): leakage canary という別の実装。

## 検索語

英国競馬, 定量ベッティング, 合成データ, 事前登録, 時点整合特徴量, リーク検出テスト, 欠損補完のリーク, 包含回帰, 多重比較, ボンフェローニ, 期待値, 大穴の罠, UK horse racing, quant betting platform, synthetic data, pre-registration, point-in-time features, merge_asof, allow_exact_matches, future injection test, forecast encompassing regression, market denoising, consensus price, best price, overround, Bonferroni, race log loss, longshot trap

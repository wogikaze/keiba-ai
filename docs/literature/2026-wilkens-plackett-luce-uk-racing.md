---
title: Predictability and Value Betting in UK Horse Racing
authors: Wilkens Sascha
year: 2026
venue: SSRN Working Paper 6860338
url: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6860338
doi: 10.2139/ssrn.6860338
topic: probability-models
tags: plackett-luce, market-odds, calibration, isotonic-regression, llm-features, uk-racing, value-betting, market-efficiency
verified: abstract
importance: medium
source: unavailable
source_version: working-paper
---

# 英国競馬の予測可能性とバリューベット：市場確率入りの Plackett–Luce を等張回帰で較正

**原本未取得。** SSRN のワーキングペーパー（38ページ、2026年6月1日付、6月19日掲載）で、SSRN の要旨ページ・ダウンロードはボット検査で 403 になり取得できなかった。別の版（著者ページ、arXiv）も見つからない。本ノートは要旨とキーワード（検索結果での引用）に基づく。数値は要旨に書かれたものだけで、ページ番号は付けられない。

> 一言で: 市場の暗黙確率・公式レーティング・馬の属性に、レース後コメントから LLM で抽出した「道中の不利」指標を加えて着順全体に Plackett–Luce を当てはめ、等張回帰で較正し、英国の平地・障害 10 年分でローリングのサンプル外評価をした。勝率は市場と同等の精度で、利益が出たのは最も選別的な閾値だけ（ROI 20〜22%、有意性はわずか）。LLM 特徴量は予測を改善しなかった（要旨より）。

## 研究の問い

透明で再現可能なモデルで、英国競馬の賭け市場に残っている価値を取り出せるか。著者は独立研究者（以前にテニスの予測・賭けモデルの論文がある）。キーワードは Horse Racing, Betting Markets, Market Efficiency, Ranking Models, Value Betting。

## 方法（要旨から分かる範囲）

1. **モデル**: 1着だけでなく着順全体を使う Plackett–Luce（順位ロジット）。
2. **共変量**: レース前の市場暗黙確率、公式レーティング（BHA のハンデキャップレーティングと思われる。推測）、馬の属性。加えて、過去のレース後コメント（in-running comments）から大規模言語モデルで抽出した「道中で不利を受けた」指標。
3. **較正**: 出力確率を等張回帰で補正。
4. **評価**: 完全にサンプル外のローリング設計（学習期間を進めながら次の期間を予測）。
5. **ベンチマーク**: 非線形モデル（種類は未確認）。
6. **賭け**: モデル確率とオッズの比が閾値を超える馬に賭けるバリューベット。閾値を変えて ROI とシャープレシオを報告。

## 結果（要旨の数値）

| 項目 | 結果 |
|---|---|
| 勝率の較正 | 良好 |
| 確率精度 | 市場の暗黙確率と同等 |
| 賭けの収益 | 最も選別的な閾値でのみ ROI 20〜22%、シャープレシオ 0.12〜0.13 |
| 統計的有意性 | わずか（marginal） |
| LLM 由来の不利指標 | 予測を改善しない |
| 非線形ベンチマーク | 確率精度は上がるが、賭けの収益は上がらない |

## 批判的に読む（原本未取得のため限定的）

- **市場確率を共変量に入れた1段階モデル**と読める。[Sung 2007](./2007-sung-two-step-conditional-logit.md) は1段階より2段階（オッズなしモデル → オッズと結合）の方が利益が大きいと報告しており、構成の選択が「精度は市場と同等」という結論に効いている可能性がある。
- 「最も選別的な閾値」だけで利益が出るという結果は、閾値を複数試した中から最良を報告していれば多重検定の問題がある。賭け件数が少なく有意性もわずかなので、偶然の可能性が残る（[Bailey 2017](./2017-bailey-probability-backtest-overfitting.md) の観点）。
- どのオッズ（ブックメーカーの開始価格 SP、交換所、締切前）で回収率を計算したか、手数料を引いたかは未確認。英国では SP とベットフェアのどちらを使うかで ROI が大きく変わる。
- 「確率精度は上がるが収益は上がらない」は、[Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md) や [Hubáček 2020](./2020-hubacek-beating-market-bad-model.md) の議論（精度より、市場との相関の低さや較正が収益を決める）と整合する。
- LLM 特徴量が効かなかった理由（不利の情報はすでに市場や公式レーティングに織り込まれているのか、抽出の質の問題か）は未確認。

## keiba-ai での使い方

- **評価指標の教訓**: log loss の改善と回収率の改善は一致しない。実験ログに両方を必ず記録し、回収率は閾値ごとの曲線と賭け件数・ブートストラップ区間をつけて報告する。閾値はテスト期間を見て選ばない。
- **構成の比較実験**: 本論文の構成（市場確率入りの P-L ＋ 等張回帰）を、2段階の Benter 型と同じ JRA データ・同じローリング評価で比べる。仮説: JRA の単勝でも、市場確率を特徴量に入れた1段階モデルは2段階モデルより回収率が低い。
- **前走の不利**: JRA の「レース後の短評」や競走中の不利の記録から不利指標を作るアイデアは試す価値があるが、本論文の否定的な結果を踏まえ、まず「その情報が次走のオッズに織り込まれているか」（オッズとの残差に効くか）を確認してから特徴量にする。
- **等張回帰による較正**: 多クラス（レース内の勝率）での等張回帰の適用は、[Zadrozny 2002](./2002-zadrozny-isotonic-multiclass-calibration.md) の方法と、レース内の再正規化を組み合わせる必要がある。
- 原本が取れたら、データ件数、オッズの種類、閾値ごとの表、LLM 抽出の方法を追記する。

## 関連ノート

- [Benter 2019](./2019-benter-model.md): 市場確率とファンダメンタル確率の2段階結合。本論文の比較相手として自然。
- [Sung 2007](./2007-sung-two-step-conditional-logit.md): 1段階と2段階の比較（英国データ）。
- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 使っているモデルの原典。
- [Glickman 2015](./2015-glickman-stochastic-rank-ordered-logit.md): 順位ロジットの動的拡張。
- [Zadrozny 2002](./2002-zadrozny-isotonic-multiclass-calibration.md): 等張回帰による多クラス較正。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 較正と精度のどちらが賭けに効くか。
- [Hubáček 2020](./2020-hubacek-beating-market-bad-model.md): 精度の低いモデルでも市場に勝てる条件。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md): 閾値選択によるバックテストの過学習。
- [Franck 2010](./2010-franck-bookmakers-vs-betting-exchange.md): ブックメーカーと交換所の価格の違い。

## 検索語

英国競馬, Plackett-Luce, 順位ロジット, 着順全体, 市場確率, 公式レーティング, 等張回帰, 較正, ローリング評価, サンプル外, バリューベット, 回収率, ROI, シャープレシオ, 市場効率性, LLM 特徴量, 大規模言語モデル, レース後コメント, 道中の不利, UK horse racing, value betting, market efficiency, ranking models, isotonic regression, calibration, rolling out-of-sample, trouble in running, in-running comments, large language model features, Sharpe ratio, SSRN

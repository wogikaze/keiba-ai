---
title: turf-tipster / turf-tipster2 — 競馬予想AI（Chainer の順位学習 NN と LambdaRank・アンサンブル）
authors: 坂本（ココン株式会社 AI戦略室、GitHub: cocon-ai-group）
year: 2018
venue: GitHub ＋ ココン AI戦略室ブログ（3回シリーズ）
url: https://github.com/cocon-ai-group/turf-tipster
topic: practitioner
tags: grey-literature, github, jra-van, chainer, pairwise-ranking-loss, embedding, rnn, lambdarank, xgboost-rank-pairwise, ensemble, as-of-features, leakage, return-simulation
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 馬名・騎手名の埋め込みから「強さ」を順位学習する NN と、LambdaRank＋XGBoost のアンサンブル（2018 年の企業ブログ・シリーズ）

> 一言で: 社内忘年会の余興として 2017 年有馬記念を予想するために作られた競馬 AI。第 1 作は馬と騎手の名前を埋め込みベクトルにし、1 レース 18 頭をミニバッチに並べ、softplus と tanh を組み合わせた自作のペアワイズ損失で「着順どおりに並ぶ強さ」を学習する Chainer の NN。第 2 作は LightGBM の LambdaRank と XGBoost の rank:pairwise に、「その月時点」の戦歴 218 次元＋次元削減 40 次元を足してアンサンブルした。古い 2,000〜2,500 レースで学習し新しい 500 レースで検証すると、最終版の回収率は単勝 62.9%、三連複 107.3%、三連単 107.8%。著者は回収率は参考値で、的中数を見るほうが実態に近いとしている。第 1 作の「単勝 500% 超」はスクレイピングのバグだった。

原本は GitHub の README 2 本（turf-tipster：`library/2018-cocon-turf-tipster/source.txt`、turf-tipster2 は同じ構成で LambdaRank 版）と、解説ブログ 3 本（`attachments/`）。ブログは cocon-corporation.com にあったが現在は別会社のサイトに転送されるため、Internet Archive の 2021 年のスナップショットから保存した。

- 第 1 作「競馬予想AIを作る 〜ニューラルネットワークによる相対評価データセットの取り扱い例〜」（`attachments/horseraceprediction_ai.txt`）
- 「競馬予想AI再び -前編- 〜LambdaRank編〜」（`attachments/horseraceprediction_ai_lambdarank.txt`）
- 「競馬予想AI再び -後編- 〜アンサンブル学習編〜」（`attachments/horseraceprediction_ai_ensemble-learning.txt`）

## データ

- JRA-VAN にアプリ開発者として登録して公式データを取得し、CSV に変換（第 1 作）。1 行 1 レースで「レース名|競馬場|馬場|距離|天気|オッズ|日付」に続けて「着順|馬名|騎手名」を並べる形式（README「Make dataset」）。オッズ欄には各券種の払戻（100 円あたり）が入る。
- 第 1 作: 過去 3,000 レースのうち古い 2,500 を学習、新しい 500 を検証。500 レースはおよそ 5 か月分。
- 後編: 馬ごとの戦歴をウェブからスクレイピングし、「馬名 + YYMM」をキーに月単位の戦歴表（`horse_history.csv`）を作った。

## 特徴量

- 第 1 作と前編: 馬名・騎手名（ID 化して埋め込み、または One-Hot）、競馬場、馬場（芝・ダート・障害）、天気、距離だけ。過去成績の集計値は使わない。
- 後編: その月時点の平均着順・獲得賞金総額・直近 3 レース平均と、それらの競馬場別・馬場別・天気別の集計で計 218 次元（先頭 15 個は血統のカテゴリ）。PCA・TruncatedSVD・Gaussian/Sparse Random Projection で各 10 次元に圧縮した 40 次元を足して 258 次元。該当月の戦歴がなければ直近の月まで遡る。

## モデルと目的変数

- 第 1 作（Chainer）: 馬・騎手・レース情報の埋め込みを全結合で合成し、馬の成長を扱うために RNN を組み込む。1 レースの出走馬をミニバッチ方向に並べ（バッチサイズ = 18）、損失は 1 レースで 1 個。損失は全ペアについて「正しい順序なら小さく、逆順なら大きく、逆順で差が開くほうが変化が大きい」形にし、softplus と tanh（または atan）で作る。出力が一点に潰れないよう「空間内に均等に分布する」力も意識した、とある。
- 前編: LightGBM の `objective: lambdarank`、`metric: ndcg`、`ndcg_eval_at: [1,2,3]`。目的は着順で、`max_position` 以下の下位馬は同じ扱いにする。
- 後編: LightGBM LambdaRank と XGBoost `rank:pairwise`（カテゴリは自前で One-Hot）のスコアを正規化してアンサンブル。KFold（10 分割）はレース単位で分けて query を作り直す。

## 評価

- 分割: 時系列のホールドアウト（古い側で学習、新しい 500 レースで検証）。第 1 作のブログで、ランダムに検証データを取ると未来のデータで学習したモデルを検証することになり不正確に良く出る、と説明している。ただし後編の early stopping 用の KFold は学習期間内でのシャッフルなし分割。
- 回収率: 予測スコア上位の馬で各券種を 1 点（複勝は 1〜3 枚）買ったときの、500 レース平均の払戻（100 円あたり）。払戻は確定払戻。

## 結果

- 第 1 作（README「Training」と第 1 作ブログ）: 単勝の平均払戻が 500 超と出たが、後日「スクレイピングのプログラムにバグがあり、単勝馬券の期待リターン率が実際より高く出る」と追記して取り消している。
- 前編（LightGBM、馬・騎手・場・馬場・天気・距離のみ、500 レース）: 単勝 80.48、複勝 73.26、複勝(1 枚) 71.86、馬連 45.14、ワイド 63.38、馬単 40.98、三連複 59.32、三連単 27.76。単勝の的中 85 本。
- 後編（アンサンブル＋戦歴、500 レース）: 単勝 62.88、複勝 74.49、複勝(1 枚) 79.54、馬連 76.68、ワイド 60.1、ワイド(1 枚) 59.08、馬単 94.6、三連複 107.32、三連単 107.84。的中数は単勝 90、三連複 23、三連単 7。著者は回収率は参考値で、的中数のほうが実態に近いと書く。

## 落とし穴と教訓（著者の記述）

- **現在の集計値を過去のレースに使うリーク**（後編）: 「現在の」獲得賞金総額を馬の属性として過去レースの学習に使うと、強いと分かった後の情報で学習することになる。K 分割のテストでは見つからない厄介なパターンだ、と書いている。対策として月単位の時点別戦歴を作った。
- **LambdaRank が並び順を学習する**（前編）: CSV が着順に並んだまま学習させると、LightGBM が「上の行の馬ほど上位」と学習してしまった。レースごとに行をシャッフルして回避した。本来は枠順で並べるべき、とも書いている。
- **NN で並べ替えを学習する難しさ**（第 1 作）: ソートは比較（IF）を含むので微分できない。比較を使わない微分可能な損失を設計する必要がある。
- 第 1 作の単勝 500% 超はデータ取得のバグ。

## 批判的に読む

- 三連複・三連単の 107% は 500 レースで的中 23 本・7 本の結果で、1 本の高配当で大きく動く。著者の言うとおり参考値で、100% を超えた証拠にはならない。
- 単勝の回収率は前編の 80.5% から後編の 62.9% に下がっている。的中数は増えたが人気馬に寄った可能性がある。精度と回収率が逆に動く典型例として読める。
- 月単位の戦歴は「その月の途中のレース」の結果も含みうる。同じ月の後のレースの結果が前のレースの特徴に入る小さなリークが残る（月初からの集計なら、当月分を除く必要がある）。
- 次元削減（PCA など）を戦歴表全体（全期間）に当てはめてから分割しているので、検証期間の分布が学習に入っている。
- 馬名の埋め込みや One-Hot は、新馬や出走数の少ない馬に弱い。検証期間に初めて出てくる馬の扱いは書かれていない。

## keiba-ai での使い方

- 「現在の集計値で過去を学習するリーク」と「並び順のリーク」（行順が着順のままだと順位学習モデルが行の位置を覚える）は、どちらもリーク検査のテスト項目に入れる。特に後者は、データ整形で着順ソートされた表をそのまま LambdaRank に渡すと起きる。
- 1 レースを 1 バッチにしてペアワイズ損失で学習する NN の構成は、レース単位の損失（Plackett-Luce や ListNet）を自作するときの最小例になる。
- 時点別の集計表（馬 × 時点）を先に作っておき、レース日でその時点の行を引く設計は、as-of 結合の実装の参考になる。粒度は月ではなく日にする。
- 回収率と的中数を並べて報告する書き方、少数的中の券種は参考値扱いにする書き方は、実験レポートの書式に取り入れる。

## 関連ノート

- [Burges 2010](./2010-burges-ranknet-lambdarank-lambdamart.md): LambdaRank / LambdaMART の原典。ブログでも引用されている。
- [Ke 2017](./2017-ke-lightgbm.md): LightGBM。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 対戦結果から強さを推定する Bradley-Terry。第 1 作の「強さベクトル」の発想と同じ。
- [Guiver 2009](./2009-guiver-bayesian-plackett-luce.md): 着順全体から強さを学ぶ Plackett-Luce。
- [Fujisawa 2024](./2024-fujisawa-ranknet-condition-datasets.md): 日本の競馬での RankNet。
- [Enigmo 2020](./2020-enigmo-learning-to-rank.md): 実践者による LightGBM のランキング学習。
- [Bunyu422 2026](./2026-bunyu422-listnet-wide.md): 後年の個人開発でのペアワイズ損失 NN。

## 検索語

競馬予想AI, ランキング学習, ペアワイズ損失, 強さベクトル, 埋め込み, Embedding, Chainer, RNN, LambdaRank, LambdaMART, rank:pairwise, XGBoost, アンサンブル, 次元削減, 時点別戦歴, as-of 集計, 獲得賞金リーク, 行順リーク, 回収率シミュレーション, JRA-VAN, learning to rank horse racing, pairwise ranking loss, leakage from current aggregates

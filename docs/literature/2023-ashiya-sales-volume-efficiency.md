---
title: Sales Volume, Noise Traders, and Efficiency of the Japanese Racetrack Betting Market
authors: Ashiya Masahiro
year: 2023
venue: The Journal of Gambling Business and Economics 16(1), 3-14
url: https://www.ubplj.org/index.php/jgbe/article/view/2029
doi: 10.5750/jgbe.v16i1.2029
topic: japan
tags: market-efficiency, sales-volume, noise-traders, field-size, pari-mutuel, cross-pool-arbitrage, nar
verified: abstract
importance: high
source: unavailable
source_version: published
---

# 売上・頭数・情報の少ない賭け手と、日本の馬券市場の効率性

> 原本未取得。JGBE の本文は購読・ログインが必要で、無料の著者稿やワーキングペーパー版も見つからなかった。本ノートは出版社ページの要旨と、同じ著者の先行ディスカッションペーパー（荒尾競馬、DP No.1618, 2016）に基づく。先行 DP の内容を本論文の内容と取り違えないよう、節を分けて書く。

> 一言で: 日本のサラブレッド競走 3,270 レースで、馬券市場の効率性は売上が大きいほど高く、出走頭数が多いほど、また情報の少ない賭け手（noise traders）が増えるほど低いと報告した（要旨）。

## 要旨（出版社ページ）

要旨は1段落だけである。

> This study examines 3,270 races of the Japanese thoroughbred racetrack betting market. It finds that market efficiency improves with the sales volume and deteriorates with the number of horses on a race and an increase in less-informed bettors.（出版社ページの Abstract）

要旨からは次のことが分からない（すべて未確認）。

- 3,270 レースが JRA か地方競馬（NAR）か。どの競馬場・期間か。
- 「効率性」をどう測ったか（FLB の大きさか、券種間の価格差か）。
- 「情報の少ない賭け手の増加」を何で代理したか（場外比率、ネット比率、開催日、レースの格など）。
- 係数の大きさと有意水準。

## 先行 DP から推測される枠組み（推測）

著者は科研費「公営賭博における裁定取引の可能性」と「Sales volume and efficiency of the racetrack betting market」（2018〜2022年度）の流れで、地方競馬の券種間裁定を競馬場ごとに調べてきた（荒尾、佐賀、門別、高知、園田・姫路、南関東4場、笠松・佐賀・福山、金沢・名古屋・盛岡・水沢）。researchmap の業績一覧で、本論文はこの系列の中に位置づけられている。
3,270 レースという規模は、これらの地方競馬の複数場を合わせたものである可能性が高い。ただし**推測**であり、本文では確認していない。

先行 DP No.1618「荒尾競馬における、勝馬投票券市場の効率性の決定要因」（2016年7月）は、同じ問いを荒尾競馬 160 レースで扱っている。その枠組みを要約する（DP の頁番号、本論文の頁ではない）。

### 効率性の尺度

単勝 $i$ のオッズ $O_i$、馬単 $O_{ij}$、三連単 $O_{ijk}$ から、「どの馬が勝っても 1 円を受け取る」権利を最も安く作る費用

$$P \equiv \sum_{i} \min\Big(\frac{1}{O_i},\ \sum_{j\neq i}\min\Big(\frac{1}{O_{ij}},\ \sum_{k\neq i,j}\frac{1}{O_{ijk}}\Big)\Big)$$

を計算する（DP p.3, 式(3)）。市場が効率的で券種間に価格差がなければ $P = \bar P \equiv \sum_i 1/O_i$ になり、価格差が大きいほど $P$ は $\bar P$ より小さくなる。そこで

$$P_{dif} = P - \bar P,\qquad P_{ratio} = P / \bar P$$

を効率性の尺度とし、値が小さいほど非効率とする（DP pp.3-4, 式(5)(6)）。FLB ではなく**券種間の一物一価からのずれ**で効率性を測る点が特徴である。

### 荒尾 160 レースの結果（DP）

- データ: 2011年9月30日〜12月23日の荒尾競馬 175 レースから、返還の生じた4レースと場外発売の無かった日の11レースを除いた 160 レース（DP p.4）。平均出走頭数 8.369、平均売得金 6.326 百万円、場外比率の平均 0.761。$P_{ratio}$ は平均 0.796、最小 0.527、最大 0.930（DP p.4）。
- 回帰: $P_{dif}$ と $P_{ratio}$ を売得金（Total）、出走頭数（Number）、場外比率（Outratio）、競走順（Race）、メインレースダミーに回帰（DP p.6, 式(7)(8)）。
- 結果: 売得金は 1% 有意でプラス、出走頭数は 1% 有意でマイナス、メインレースは 10% 有意でプラス。場外比率と競走順は有意でない（DP pp.6-7）。

DP の結論は単一競馬場の結果で、他場への一般化は今後の課題とされていた（DP p.7）。2023 年論文はレース数が約 20 倍に増えており、この課題に答えたものと読める（推測）。要旨の「情報の少ない賭け手の増加で効率が下がる」は、DP では有意でなかった場外比率とは別の代理変数を使った可能性がある（未確認）。

## 批判的に読む

- **効率性の定義**: 先行 DP と同じ $P$ を使っているなら、測っているのは券種間の整合性で、オッズが真の勝率を当てているか（較正、FLB）ではない。券種間で整合していても全券種が同じ方向に歪むことはありうる。
- **$\bar P$ の機械的な変動**: $\bar P$ は頭数とオッズの切り捨てで変わる（DP p.3）。頭数が多いと $P$ の計算に入る組合せが急増し、三連単の小さな歪みが積み上がる。「頭数が多いほど非効率」の一部は尺度の機械的な性質による可能性がある（推測）。
- **確定オッズ**: 先行研究はいずれも確定オッズで計算しており、購入時点での乖離ではない。
- **本文未読**: 推定式、データの範囲、頑健性チェックは確認できていない。

## keiba-ai での使い方

- **市場確率への重み**: Benter 型にモデル確率と市場確率を結合するとき、売上規模と出走頭数を結合重みの説明変数に入れる。仮説: 売上が小さく頭数が多いレースほど市場確率の信頼度が低く、モデル側の重みを上げると対数尤度が改善する。
- **レース単位の特徴量**: 売上（または票数）、出走頭数、券種間の価格差 $P_{ratio}$ をレースレベルの特徴量にし、モデルと市場の乖離の大きさや、回収率の分散を説明できるか検証する。
- **評価の層別**: バックテストの回収率と較正指標を、売上規模・頭数の分位ごとに出す。全体平均では見えない「小さい市場でだけ勝てる」構造を確認する。小さい市場では自分の購入でオッズが動く（[Ashiya 2015](./2015-ashiya-lock-arbitrage.md)）ので、払戻はマーケットインパクト込みで計算する。
- **本文入手後の確認事項**: データの所属（JRA/NAR）、noise trader の代理変数、係数の大きさ。

## 関連ノート

- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 同じ著者のサーベイ。情報弱者が多いほど FLB が強まるという理論（第4.7節）の整理を含む。
- [Ashiya 2015](./2015-ashiya-lock-arbitrage.md): 同じ著者。荒尾競馬の同じデータで lock の頻度を数えた。本論文の尺度 $P$ の原型。
- [Walls 2003](./2003-walls-breakage-turnover-japanese-tracks.md): 日本の競馬場の売上規模とオッズの切り捨て。売上と効率性の関係を扱う先行研究。
- [Ottaviani 2010](./2010-ottaviani-noise-information-flb.md): ノイズと情報の比率が FLB を決めるという理論。
- [Mori 2010](./2010-mori-independent-herding-betters.md): 独立に賭ける人と追随する人の混在と市場効率。
- [Okamoto 2022](./2022-okamoto-flb-without-cross-arbitrage.md): 券種間裁定と FLB。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): 賭博市場の効率性のサーベイ。

## 検索語

市場効率性, market efficiency, 売上, 売得金, sales volume, turnover, 出走頭数, field size, number of runners, ノイズトレーダー, noise traders, less-informed bettors, 情報の少ない賭け手, 券種間価格差, cross-pool arbitrage, 一物一価, law of one price, 合成馬券, P_dif, P_ratio, 地方競馬, 荒尾競馬, パリミュチュエル, pari-mutuel, 芦谷政浩, Ashiya, JGBE, Journal of Gambling Business and Economics

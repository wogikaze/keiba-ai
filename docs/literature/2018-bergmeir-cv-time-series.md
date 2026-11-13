---
title: A note on the validity of cross-validation for evaluating autoregressive time series prediction
authors: Bergmeir Christoph, Hyndman Rob J., Koo Bonsoo
year: 2018
venue: Computational Statistics & Data Analysis 120 70-83
url: https://robjhyndman.com/publications/cv-time-series/
doi: 10.1016/j.csda.2017.11.003
topic: evaluation-and-features
tags: cross-validation, time-series, out-of-sample, leakage
verified: fulltext
importance: medium
source: downloaded
source_version: working-paper
---

# 純粋な自己回帰モデルなら、時系列でも普通の k-fold CV が使える（ただし誤特定がひどいと過小評価）

> 一言で: 時系列を「ラグ p 個 → 次の値」の行列に埋め込み、モデルがラグ構造を十分に捉えていれば、行同士の誤差は無相関なので、行を無作為に fold に分ける通常の k-fold CV が妥当になる。シミュレーションでは CV のほうが末尾ホールドアウト（OOS）より誤差推定が正確だった。逆に、モデルが季節ラグを取りこぼすほど誤特定されていると、CV は誤差を系統的に過小評価する。

読んだ版は Monash 大学のワーキングペーパー 10/15（2015 年 4 月、17 ページ、題は "A Note on the Validity of Cross-Validation for Evaluating Time Series Prediction"）。CSDA 掲載版（2018）は題に "autoregressive" が加わっており、本文の改訂内容は未確認。以下のページ番号はワーキングペーパーの PDF のもの。

## 主張の骨子（2 節）

時系列 $y_1,\dots,y_n$ を次数 p で埋め込み、各行を $[y_{t-p},\dots,y_{t-1} \mid y_t]$ とした行列を回帰の入力にする（式 2, p.5）。モデルを

$$y_t = g(x_t,\theta)+\varepsilon_t,\quad x_t=(y_{t-1},\dots,y_{t-p})$$

（$\varepsilon_t$ はホワイトノイズ、$g$ は線形でも非線形でもよい）とする (p.5, 式 1)。このモデルが正しければ、$y_t-g(x_t,\theta)=\varepsilon_t$ はホワイトノイズなので行同士は条件付きで無相関になる。だから **行（入力と出力の組）ごと** テスト集合に回す限り、残りの行で学習しても推定のバイアスや一致性は損なわれない (p.5)。

従来の依存データ向け CV（Burman ら 1994 の h-block CV：テスト点の前後 h 個を訓練から除く）は、使えるデータを大きく減らす (p.5–6, Fig.1)。本論文の方法は個々の値ではなく行を除くので、失う情報が少ない (p.6)。

3 節では AR(p) の線形モデルについて、LOOCV の誤差推定 $\widehat{PE}$ が真の予測誤差 PE に収束することを示す (p.7–9)。前提は p が既知であること。p を誤ると大きなバイアスが出うるが、それは CV のモデル選択能力と両立する、と著者は述べる (p.6)。

## 実験設定（4 節）

1. 長さ 200 の系列を生成し、前 70%（140 点）を in-set、後 30%（60 点）を out-set（未知の未来）とする (p.13)。
2. in-set の中で各手法により誤差 $\widehat{PE}$ を推定する。
3. in-set 全体で学習し直したモデルの out-set 誤差を「真の誤差」PE とする (p.10, Fig.2)。
4. 系列ごとの $|\widehat{PE}-PE|$ の平均を MAPAE（推定の精度）、符号付き平均を MPAE（バイアス）とする (p.11)。各ケース 1000 回のモンテカルロ (p.13)。

比較する推定法 (p.11–12)：

| 手法 | 中身 |
|---|---|
| 5-fold CV | 埋め込み行列の行を無作為に 5 fold へ |
| LOOCV | 1 行ずつ |
| nonDepCV | 5-fold と同じ fold で、テスト行からラグ距離 p（=5）未満の行を訓練から除く |
| OOS | in-set の末尾ブロックで評価 |

予測モデルは AR(1)〜AR(5) と MLP（R の nnet、隠れ 5、weight decay 0.00316）、1 期先予測 (p.12)。データ生成過程は (1) 定常 AR(3)、(2) 可逆 MA(1)（真のモデルは候補に無いが AR で近似可能）、(3) 米国の事故死者数（1973–78）に当てはめた季節 AR（ラグ 12 が重要で、候補モデルは 5 ラグまでなので大きく誤特定）(p.12–13)。

## 結果（5 節）

線形 AR を当てはめたときの RMSE の MAPAE / MPAE（Table 1, p.15 から抜粋）：

| DGP / モデル | 5-fold CV | LOOCV | nonDepCV | OOS |
|---|---|---|---|---|
| AR(3) / AR(3) | 0.090 / 0.006 | 0.090 / 0.002 | 0.630 / 0.628 | 0.158 / −0.002 |
| MA(1) / AR(3) | 0.102 / 0.012 | 0.101 / 0.009 | 0.482 / 0.480 | 0.173 / −0.003 |
| 季節 AR(12) / AR(3) | 158.0 / −59.8 | 157.9 / −63.0 | 332.6 / 292.8 | 165.1 / −34.5 |

- **AR(3)・MA(1)**：CV の MAPAE は約 0.09〜0.10、OOS は約 0.16〜0.19。CV のほうが誤差推定が正確 (p.13–14)。バイアスはどれも小さいが、MA(1) では OOS がわずかに小さい (p.14)。
- **nonDepCV**：訓練データが減ってモデル自体が悪くなり、誤差を大きく過大評価する。AR(5) では MAPAE が 6.1（AR(3) DGP）、10.2（MA(1) DGP）に跳ね上がる (p.14–15)。
- **季節 AR（誤特定）**：CV の精度上の優位はほぼ消え、MPAE が大きく負になる（誤差の過小評価）。OOS のほうがバイアスは小さい (p.14)。
- MLP（Table 2）でも同じ傾向。ラグ 1 個だけの MLP はどの手法でも不安定 (p.14)。

結論：ラグ構造が適切なら通常の k-fold CV を使うべきで、モデルがデータを十分に当てはめていれば、ラグ構造が正確でなくても OOS より良い。誤特定がひどいときだけ CV を避けるべき (p.16)。

## 批判的に読む

- **前提は「純粋な自己回帰」で「定常」**：入力が過去の値だけで、誤差がホワイトノイズになるほど当てはまっている場合の議論。外生変数があり、その分布が時間で変わる（非定常）場合は対象外。論文冒頭で非定常性を CV の問題点として挙げつつ (p.3)、実験の DGP はすべて定常。
- **系列が短い**：長さ 200 で、末尾ホールドアウトは in-set 末尾の一部しか使えないので OOS に不利な設定。データが十分長い場合には差が縮むはず（推測）。
- **真の誤差の定義**：in-set 全体で学習し直して out-set で測る。out-set は in-set と同じ定常過程からの続きなので、時間による変化（概念ドリフト）は評価に入っていない。
- 季節 AR の結果が示すとおり、**モデルが取りこぼした依存構造は CV の楽観バイアスになって返ってくる**。現実のデータでは「十分に当てはまっているか」を事前に知るのは難しい。

## keiba-ai での使い方

- **そのまま当てはめてはいけない**：競馬データは「ラグだけの自己回帰」ではない。同じ馬・騎手・開催が何度も現れ（クラスタ構造）、オッズや人気は市場の時点情報で、期間をまたいで分布が変わる。行（出走）を無作為に fold へ分けると、同じレースの他馬や、未来の同じ馬の成績が訓練側に入る。本論文の「行の誤差が無相関」という前提が崩れる典型例。
- **使える場面**：馬ごとの過去走系列から「次走のタイム指数」を予測するような、本当に自己回帰的な部分モデルのハイパーパラメータ（ラグ数＝何走前まで使うか）を選ぶ場合。ここでもレース単位（同じレースの全馬を同じ fold）で分ける。
- **本命の評価はウォークフォワード**：最終評価と購入戦略の比較は、時間順の分割（期間で学習 → 次の期間で評価）で行う。本論文の季節 AR の結果は、季節性（開催、馬場、番組）をモデルが捉えきれないなら CV は楽観的になる、という警告として読む。
- **実験案（仮説）**：同じ LightGBM 設定で (a) 出走単位の無作為 5-fold、(b) レース単位のグループ 5-fold、(c) 年単位のウォークフォワードで logloss を推定し、翌年の真の logloss との差（本論文の MAPAE / MPAE と同じ定義）を比べる。(a) が最も楽観的に出ると予想する。

## 関連ノート

- [Cerqueira 2020](./2020-cerqueira-time-series-performance-estimation.md)：本論文を受けて、実データ 174 系列で CV とホールドアウト系を比較。非定常な実データでは結論が変わることを示す。
- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md)：CSCV。ブロック単位で時間順を保つ組合せ CV。戦略選択の過学習に焦点がある。
- [Bailey 2014](./2014-bailey-deflated-sharpe-ratio.md)：CV でもホールドアウトでも多重検定は防げないという議論。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md)：競馬予測でのリークを意識した評価設計。本論文の前提が崩れる具体例の側。

## 検索語

交差検証、クロスバリデーション、cross-validation、k-fold CV、LOOCV、leave-one-out、時系列、time series、自己回帰、autoregressive、AR モデル、埋め込み、embedding、ラグ、lag、h-block CV、non-dependent cross-validation、nonDepCV、ホールドアウト、out-of-sample、OOS 評価、末尾評価、予測誤差推定、MAPAE、MPAE、誤特定、misspecification、季節性、seasonality、定常性、stationarity、Hyndman

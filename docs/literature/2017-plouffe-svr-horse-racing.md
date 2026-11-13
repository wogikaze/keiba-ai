---
title: Predicting Horse Racing Results (HorseRacingPrediction)
authors: Dominic Plouffe (dominicplouffe)
year: 2017
venue: GitHub
url: https://github.com/dominicplouffe/HorseRacingPrediction
topic: practitioner
tags: grey-literature, north-america, harness-racing, svr, finish-position-regression, morning-line, race-selection, win-bet
verified: fulltext
importance: low
source: downloaded
source_version: web
---

# 北米の繋駕速歩で着順を SVR で回帰: 1番手の勝率は朝の予想オッズの本命を少し上回るが、61件の単勝は −$2

> 一言で: DeadHeat.ca を運営する個人が、北米の繋駕速歩（ハーネス）レースを3か月学習・1か月検証の窓で SVR（サポートベクター回帰）の着順予測にかけた記録（GitHub スター約180）。予測1番手の勝率は 28% で、モーニングライン（主催者が発売前に出す予想オッズ）の本命の 26% をわずかに上回る。1番手と2番手の予測着順の差が2以上のレース（61件）に絞ると勝率 54% だが、単勝$2で買うと払戻$120に対し賭け金$122で −$2。著者は「強い馬を当てるモデルは、儲かる馬を当てるモデルではない」と結論している。

## データ

- 北米各地の繋駕速歩の出馬表と結果を5年間、公開サイトから収集（「The data」）。
- 学習窓は直近3か月。天候の影響が大きいので、予測日に近い短い期間で学習した方が良い結果になったと書いている。
- 2017年1〜3月の各月を検証（例: 3月は2016年12月〜2017年2月で学習、2,896レースで検証）。
- 繋駕速歩は北米ではすべて1マイル、助走付きスタート、歩様を乱すと（break）最後方まで下げる規則がある。

## 特徴量

- 20個、すべて −1/0/1 の離散値（「Description of core features」）: 枠1〜5か、前走の上がりスピードが上位2か、馬の勝率50%超、馬の3着内率60%超、馬の通算 ROI が$2超、ドライバー・調教師の同じ3指標、6走以上か、直近2走で歩様を乱したか、21日以内に出走したか、同じ競馬場か、同じドライバーか、前走1着、前走3着内、直近3走で1着、賞金が前走より上か下か。
- モーニングラインは基準用で、特徴量には入れていない。

## モデルと目的変数

- 目的変数は着順（数値）。scikit-learn の `SVR(C=1.0, epsilon=0.1)`。予測値が最小の馬を1番手とする。

## 評価と結果

「Results」と「Comparison to previous month results」の表より:

| 月 | 方法 | レース数 | 勝率 | 3着内率 |
|---|---|---:|---:|---:|
| 3月 | モーニングラインの本命 | 2,896 | 26% | 58% |
| 3月 | SVR 全レース | 2,896 | 28% | 63% |
| 3月 | 1番手と2番手の差 ≥1 | 664 | 38% | 72% |
| 3月 | 差 ≥2 | 61 | 54% | 84% |
| 3月 | 予測値の標準偏差 ≥1.4 | 68 | 40% | 86% |
| 1月 | SVR 全レース / 差 ≥2 | 2,769 / 56 | 27% / 41% | 60% / 79% |
| 2月 | SVR 全レース / 差 ≥2 | 2,527 / 43 | 27% / 42% | 62% / 86% |

- 3月の「差 ≥2」61件を実際の単勝配当で計算: 賭け金$122、払戻$120、−$2（「So what does this mean?」）。

## 落とし穴と教訓（著者の記述）

- モデルは最も強い馬を予測するように作られていて、実際にそうなっているが、強い馬は勝っても配当が安い。
- 儲けるには「最も強いが、大衆が選ぶ馬とは違う」馬を表す特徴量（例: 最終オッズ3倍以上で勝つ可能性が高い馬）が要る。

## 批判的に読む

- 比較対象がモーニングライン（発売前の予想）で、実際の市場（確定オッズの1番人気）ではない。確定オッズの1番人気の勝率はモーニングラインより高いのが普通なので、28% が市場を上回っているとは言えない。
- 単勝の評価は1か月・61件だけ。
- 特徴量の閾値（勝率50%超など）は粗く、確率の出力もない。期待値で賭ける枠組みになっていない。
- 2017年の README で、北米の繋駕速歩という日本と違う競技だが、「勝ち馬を当てる」ことと「儲ける」ことの違いを、実際の配当で示した初期の例として読める。

## keiba-ai での使い方

- 「的中率は上がるが回収率は上がらない」の具体例として、評価のルール（的中率だけで判断しない）の説明に使える。
- 予測1番手と2番手の差（マージン）でレースを絞る方法は、確率モデルなら「1番手の確率」や「レース内エントロピー」で絞るのと同じ。絞り込みの効果を、的中率ではなく市場確率との比較と回収率で測る。
- 比較の基準は朝の予想オッズではなく、購入時点の実際のオッズにする。

## 関連ノート

- [Schumaker 2013](./2013-schumaker-harness-track-svr.md): 繋駕速歩での SVR（学術）。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md)、[Edelman 2007](./2007-edelman-svm-horserace-odds.md): SVR / SVM による着順予測と市場の結合。
- [Hubáček 2020](./2020-hubacek-beating-market-bad-model.md): 市場と同じことを当てるモデルでは儲からない。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 精度より較正。

## 検索語

北米競馬, 繋駕速歩, ハーネスレース, サポートベクター回帰, 着順回帰, モーニングライン, 本命, レースの絞り込み, 的中率と回収率, harness racing, North America, support vector regression, SVR, finish position regression, morning line, favourite, race selection, prediction margin, hit rate vs ROI, DeadHeat.ca

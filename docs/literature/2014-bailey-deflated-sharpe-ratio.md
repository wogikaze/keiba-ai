---
title: The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality
authors: Bailey David H., López de Prado Marcos
year: 2014
venue: Journal of Portfolio Management 40(5) 94-107
url: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
doi: 10.3905/jpm.2014.40.5.094
topic: evaluation-and-features
tags: deflated-sharpe-ratio, multiple-testing, selection-bias, backtest-overfitting
verified: fulltext
importance: high
source: downloaded
source_version: working-paper
---

# デフレート・シャープレシオ（DSR）：試行回数と非正規性で「最良バックテスト」を割り引く

> 一言で: N 本の戦略を試して最良のものを選ぶと、真の SR が 0 でも最大 SR の期待値は正になる。その期待最大値を棄却閾値にした Probabilistic Sharpe Ratio（PSR）が DSR で、試行回数・試行間の SR 分散・標本長・歪度・尖度の 5 つを使って SR を割り引く。

読んだ版は著者サイトの「This version: July 31, 2014」（JPM 掲載予定稿、22 ページ、SSRN 2460551）。JPM 掲載版の DOI は 10.3905/jpm.2014.40.5.094（OpenAlex による）。旧ノートの doi 欄は SSRN の DOI だったので掲載版に直した。

## 問題意識：バックテストに欠けている最重要情報は「試行回数」

著者らは、学術誌や運用提案に載るバックテストのほぼすべてに欠けている情報は試行回数だと主張する (p.3)。

> a backtest where the researcher has not controlled for the extent of the search involved in his or her finding is worthless (p.3)

論点は 3 つある。

1. **多重検定**：同じデータで多数の戦略を同じ有意水準で検定すると、少なくとも 1 つ偽陽性を選ぶ確率が上がる (p.3–4)。
2. **記憶効果のある系列での過学習**：コイン投げのように記憶の無い系列では、過学習したルールは将来「効かない」だけ。しかし均衡に戻る性質（平均回帰）がある系列では、標本内の極端なパターンが将来「打ち消される」ので、過学習は損失の最大化につながる (p.5–6)。
3. **ホールドアウトでは防げない**：ホールドアウトや k-fold CV は 1 回だけ試したかのように汎化を評価する。ホールドアウトを 20 回繰り返せば 95% 水準の偽陽性は「起こりうる」ではなく「起こると期待される」(p.6)。

## モデル

### 期待最大 SR（式 1）

N 個の独立な試行の SR 推定値 $\lbrace \widehat{SR}_n\rbrace $ が平均 $E[\lbrace \widehat{SR}_n\rbrace ]$、分散 $V[\lbrace \widehat{SR}_n\rbrace ]$ の正規分布に従うとき、極値理論から最大値の期待値を近似する (p.7, 付録 1)。

$$E[\max\lbrace \widehat{SR}_n\rbrace ] \approx E[\lbrace \widehat{SR}_n\rbrace ] + \sqrt{V[\lbrace \widehat{SR}_n\rbrace ]}\left((1-\gamma)Z^{-1}\left[1-\tfrac{1}{N}\right] + \gamma Z^{-1}\left[1-\tfrac{1}{N}e^{-1}\right]\right)$$

- $\gamma \approx 0.5772$：オイラー＝マスケローニ定数
- $Z$：標準正規分布の累積分布関数
- N が増えるほど、また試行間の SR 分散が大きいほど、期待最大値は上がる。技能がまったく無い戦略クラス（平均 0）でも、候補を多く調べれば良い結果に当たる (p.8, Exhibit 1)。

付録 2 では解析式とモンテカルロの最大値を比べ、近似の精度を確かめている。Python のコード片も載っている (p.12–13, Snippet 1)。

### DSR（式 2）

PSR（Bailey & López de Prado 2012）の閾値 $SR^*$ を、上の期待最大値（真の SR=0 の帰無仮説の下）に置き換えたもの (p.8–9)。

$$\widehat{DSR} = Z\left[\frac{(\widehat{SR}-\widehat{SR}_0)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right],\quad \widehat{SR}_0=\sqrt{V[\lbrace \widehat{SR}_n\rbrace ]}\left((1-\gamma)Z^{-1}[1-\tfrac1N]+\gamma Z^{-1}[1-\tfrac1N e^{-1}]\right)$$

- $\widehat{SR}$：選ばれた戦略の SR（非年率、観測頻度単位）
- $T$：標本長、$\hat\gamma_3$：歪度、$\hat\gamma_4$：尖度（正規分布で 3）
- 出力は「真の SR が 0 より大きい確率」。0.95 を超えれば 5% 水準で有意とみなす。

分母の項が示すとおり、**負の歪度と大きな尖度は SR の標準誤差を膨らませる**。SR そのものは平均と標準偏差しか使わないが、DSR はさらに非正規性 2 つ、標本長、試行の分散、試行回数の 5 変数で割り引く (p.9)。

Harvey & Liu (2014) の Benjamini–Hochberg 型の閾値とは補完関係にあり、DSR の閾値として HL の値を使うこともできると述べている (p.9)。

### 独立な試行数の推定（付録 3）

M 本の試行が互いに相関しているとき、M をそのまま N に使うと期待最大値を過大に見積もる。試行間の平均相関 $\hat\rho$ を使い、$\hat N = \hat\rho + (1-\hat\rho)M$ で補間する (p.14, 式 9)。ただし相関は線形依存しか捉えないこと、M が標本長 T を超えると相関行列が悪条件になり平均相関自体が過学習しうることを、著者ら自身が限界として挙げている (p.15)。

## 数値例：年率 SR 2.5 の国債季節性戦略

国債入札サイクルを狙う戦略で、多数の設定を試し、最良のものが日次 5 年で年率 SR 2.5 だった。開示値は次のとおり (p.9–10)。

| 入力 | 値 |
|---|---|
| 独立試行数 N | 100 |
| 試行間の SR 分散（年率） | 1/2 |
| 標本長 T | 1250 日 |
| 歪度 / 尖度 | −3 / 10 |

| 結果 | 値 |
|---|---|
| $\widehat{SR}_0$（非年率、年 250 日で換算） | ≈ 0.1132 |
| DSR | 0.9004（< 0.95 で棄却） |
| N=46 だった場合の DSR | 0.9505（採用されうる） |
| 正規リターン（歪度 0, 尖度 3）なら DSR=0.9505 となる N | 88 |

年率 2.5 という一見高い SR でも、100 回試した最良値で負の歪度と厚い裾を持つなら、真の SR>0 の確率は約 90% にとどまる。非正規性が無ければ許容できる試行回数は 46 から 88 に増える。両方の水増しを同時に扱う必要がある、というのが著者の結論 (p.10)。

## いつ試行をやめるか

最適停止（秘書問題、1/e 則）を援用し、理論的に正当化できる設定の約 37% を無作為に試し、その後は「それまでの最良」を上回るものが出た時点で止める、という経験則を提案する (p.10–11)。これは厳密な導出というより実務上の目安として示されている。

## 批判的に読む

- **正規性の仮定**：式 1 は試行の SR が正規分布に従う前提。著者らは「同じ戦略クラスの試行には共通の平均と分散がある」として正当化するが (p.7)、ハイパーパラメータ探索で得た SR 群は多峰になりうる。
- **N の数え方が結果を左右する**：DSR の値は N と $V[\lbrace \widehat{SR}_n\rbrace ]$ に強く依存し、その推定（付録 3）は粗い。研究者が記録していない試行（頭の中で捨てた案、過去のプロジェクトで見た特徴量）は数えられない。
- **SR が適切な指標か**：DSR は SR の分布理論（i.i.d. リターン、有限な 4 次モーメント）に乗っている。馬券のように、ごく少数の高配当的中が損益を決める系列では、標本長が数千でも裾の推定が不安定になる（推測）。
- 数値例は架空で、実データでの検証は無い。手法の妥当性は解析式とシミュレーションの一致（付録 2）で示しているだけ。

## keiba-ai での使い方

- **試行台帳を残す**：特徴量セット、モデル、閾値（期待値 > x で買う等）、券種の組み合わせを試すたびに、評価期間の回収率系列（レース単位またはベット単位の損益）を保存する。DSR の N と $V[\lbrace \widehat{SR}_n\rbrace ]$ はこの台帳から計算する。
- **ベット単位の損益で SR・歪度・尖度を出す**：単勝の損益は「−1 が大半、ときどき +数十」の強い正の歪度を持つ。式 2 の分母は $-\hat\gamma_3\widehat{SR}$ なので、SR>0 で正の歪度なら分母は小さくなり DSR は有利に出る。一方で尖度が非常に大きいので逆方向にも効く。日単位・開催単位に集計してから計算するのが安定するかは要検証（仮説）。
- **実験案**：過去に試した M 本の戦略の日次損益相関から $\hat N$ を推定し、「最良戦略の回収率 105%」が DSR で 0.95 を超えるかを確認する。超えない場合、報告は「最良値」ではなく「試行全体の分布」として出す。
- **PBO と併用**：DSR はパラメトリックで情報が少なくて済み、PBO（[Bailey 2017](./2017-bailey-probability-backtest-overfitting.md)）はノンパラメトリックだが全試行の損益行列が要る (p.7)。台帳があれば両方出せる。

## 関連ノート

- [Bailey 2017](./2017-bailey-probability-backtest-overfitting.md)：同じ著者の PBO（CSCV による過学習確率）。DSR が p.7 で参照する非パラメトリックな相方。
- [Bergmeir 2018](./2018-bergmeir-cv-time-series.md)：時系列で CV が使える条件。DSR は CV でも多重検定は防げないと主張する点で補完的。
- [Cerqueira 2020](./2020-cerqueira-time-series-performance-estimation.md)：時系列の性能推定法の比較。評価の分割方法側の議論。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md)：競馬予測でのリークを意識した評価。
- [Hubáček 2020](./2020-hubacek-beating-market-bad-model.md)：ベッティングの利益評価。回収率の有意性を議論する際の対照。
- [Baker 2013](./2013-baker-kelly-parameter-uncertainty.md)：推定誤差を考慮した賭け金。選択バイアスで水増しされたエッジに全額ケリーで賭ける危険と同根。

## 検索語

デフレート・シャープレシオ、デフレーテッドシャープレシオ、DSR、Deflated Sharpe Ratio、Probabilistic Sharpe Ratio、PSR、選択バイアス、selection bias、多重検定、multiple testing、バックテスト過学習、backtest overfitting、試行回数、number of trials、期待最大シャープレシオ、expected maximum Sharpe ratio、極値理論、extreme value theory、非正規性、歪度、尖度、skewness、kurtosis、勝者の呪い、winner's curse、秘書問題、secretary problem、1/e law、独立試行数、average correlation、López de Prado

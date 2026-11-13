---
title: A New Vector Partition of the Probability Score
authors: Murphy Allan H.
year: 1973
venue: Journal of Applied Meteorology 12(4) 595-600
url: https://journals.ametsoc.org/view/journals/apme/12/4/1520-0450_1973_012_0595_anvpot_2_0_co_2.xml
doi: 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2
topic: evaluation-and-features
tags: brier-score, decomposition, reliability, resolution, uncertainty, calibration
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# Brier スコアを「不確実性 + 信頼性 − 分解能」に分ける（Murphy 分解）

> 追記（2026-11-13）: 原本は機械 OCR 済み（RapidOCR）。`library/1973-murphy-brier-decomposition/source.txt` で全文検索できる。OCR の誤認識が残るため、数値は PDF のページ画像で確認すること。本ノートの本文は OCR 前にページ画像を読んで書いたもの。

> 一言で: 確率スコア（Brier スコア）を、予報と無関係な「事象そのものの不確実性」、予測確率と実現頻度のずれである「信頼性」、予報が事象を平均と違う頻度の群に振り分けた度合いである「分解能」の3項に分けた。今日 Murphy 分解と呼ばれる式の原典。

原本はスキャン PDF のため（当時）OCR 待ち（source.txt はほぼ空）。本ノートは PDF のページ画像を読んで要約したもので、ページ番号は雑誌のページ (pp.595–600) を使う。

## 背景：旧分解の不満

Murphy は前年 (1972a,b) に、Sanders (1958, 1963) の分解を一般化したスコアの分割（本論文でいう「元の分割」）を発表していた。元の分割は PS を2項に分ける (p.596, 式(2))。

- 信頼性: 予測確率 $\mathbf r^t$ と、その予報が出た機会での実現頻度 $\bar{\mathbf d}^t$ の差。
- （元の）分解能: 実現頻度 $\bar{\mathbf d}^t$ が「全部0」か「全部1」のベクトルからどれだけ離れているか。小さいほど良い。

元の分解能は、実現頻度が 0 や 1 に寄っているかを測るので、予報の鋭さ（sharpness）に近い量であって、「予報が事象を区別できたか」を直接測っていない (p.598)。本論文はこれを置き換える。

## 定式化

$N$ 個の排反な状態、$K$ 回の予報。予報 $\mathbf r_k$ と観測 $\mathbf d_k$（起きた状態だけ 1 の行ベクトル）に対して

$$PS(\mathbf r,\mathbf d)=\frac1K\sum_{k=1}^{K}(\mathbf r_k-\mathbf d_k)(\mathbf r_k-\mathbf d_k)'$$

で、範囲は $[0,2]$（式(1), p.595）。Brier (1950) の P と同じ量である。

予報が取りうる値は有限個 $T$ 種類 $\mathbf r^t$ とし、$\mathbf r^t$ が出た $K^t$ 回の実現頻度を $\bar{\mathbf d}^t$、全体の実現頻度を $\bar{\mathbf d}$ とする。新しい分割は（式(6), p.596）

$$PS(\mathbf r,\mathbf d)=\underbrace{\bar{\mathbf d}(\mathbf u-\bar{\mathbf d})'}_{\text{不確実性}}+\underbrace{\frac1K\sum_t K^t(\mathbf r^t-\bar{\mathbf d}^t)(\mathbf r^t-\bar{\mathbf d}^t)'}_{\text{信頼性}}-\underbrace{\frac1K\sum_t K^t(\bar{\mathbf d}^t-\bar{\mathbf d})(\bar{\mathbf d}^t-\bar{\mathbf d})'}_{\text{分解能}}$$

$\mathbf u$ は全要素 1 のベクトル。

- **不確実性** $PS(\bar{\mathbf d},\mathbf d)$: 全予報を全体の実現頻度（標本の気候値）に置き換えたときの PS。範囲 $[0,(N-1)/N]$。予報者の腕と無関係で、事象が難しいほど大きい (p.596–597)。
- **信頼性**: 元の分割の第1項と同一。範囲 $[0,2]$。小さいほど良い。今日の言葉では校正誤差（calibration error）。
- **新しい分解能**: 予報で区切った群ごとの実現頻度が、全体の実現頻度からどれだけ離れるか。範囲 $[0,(N-1)/N]$。**大きいほど良い**ので符号はマイナス (p.597)。

2値の場合に書き直すと、今日よく見る形 $BS = \bar o(1-\bar o) + \frac1K\sum_t K^t(f_t-\bar o_t)^2 - \frac1K\sum_t K^t(\bar o_t-\bar o)^2$ になる（この2値形は本論文には明記されていない。ベクトル式からの書き換え）。

### 新旧の関係

両方の分割を等置すると（式(7), p.597）

$$PS(\bar{\mathbf d},\mathbf d)=\text{新しい分解能}+\text{元の分解能}$$

つまり不確実性は2種類の分解能の和に分かれる。2つの分解能は同じ属性を測るのではなく、互いに補完的な量だと著者は述べる (p.597)。

## 数値例

同じ予報集合を新旧両方で分解している（Murphy 1972a,b と同じ例）。

| 例 | $K$ | 不確実性 | 信頼性 | 新分解能 | PS | 元の分解能 |
|---|---|---|---|---|---|---|
| 2状態（Table 1–2, p.597） | 10 | 0.480 | 0.136 | 0.330 | 0.286 | 0.150 |
| 3状態（Table 3–4, p.598） | 10 | 0.640 | 0.292 | 0.440 | 0.492 | 0.200 |

どちらも 不確実性 = 新分解能 + 元の分解能（0.480 = 0.330 + 0.150、0.640 = 0.440 + 0.200）が成り立つ (p.598)。2状態の例では、確率 (0.2, 0.8) の予報が4回出て実現頻度が (0.25, 0.75) なので、その群の信頼性への寄与は小さい（0.02）。一方、1回しか出ない予報は実現頻度が必ず 0 か 1 になり、信頼性・分解能のどちらにも大きく効く (Table 2)。

## 幾何学的解釈

予報と観測は $(N-1)$ 次元の正単体の点として表せる。2点間の距離 $D(\mathbf r,\mathbf r^*)=[(\mathbf r-\mathbf r^*)(\mathbf r-\mathbf r^*)']^{1/2}$ を使うと、新しい分割は平均二乗距離の関係

$$\overline{D^2}(\mathbf r,\mathbf d)=\overline{D^2}(\bar{\mathbf d},\mathbf d)+\overline{D^2}(\mathbf r^t,\bar{\mathbf d}^t)-\overline{D^2}(\bar{\mathbf d}^t,\bar{\mathbf d})$$

として書ける（式(9)(10), p.599）。Fig. 1 は3状態の例を正三角形の中に描いたもの。元の分割の分解能項はこの枠組みの中で直接描けない、というのが新分割を推す理由の1つになっている (p.600)。

## 結論と著者の評価

新しい分割は、不確実性という予報と無関係な項を分離するので、スキルスコア（気候値に対する改善率）を作る基礎になる。Hughes (1971) が求めた「予報者・予報所の比較」に使える指標として、続く論文 (Murphy 1973, 未刊行) を予告している (p.600)。個々の確率を対象とするスカラー版の分割も作れるが、ベクトル版のほうが一般に適切として扱っていない (p.600)。

## 批判的に読む

- **予報値が離散であることが前提**: 分解は「同じ予報値 $\mathbf r^t$ が出た群」を作れるときに正確に成り立つ (p.596)。連続値の確率を出す機械学習モデルでは、確率をビンに分けて近似するしかない。ビンの数で信頼性と分解能の値が変わり、ビン内の予報のばらつきの分だけ元の PS と和が合わなくなる（後年の文献で知られる問題。本論文では扱っていない）。
- **小標本の偏り**: 例のように群に 1 回しか予報がないと、実現頻度は 0 か 1 になり、分解能が大きく出る。標本が少ないと分解能は過大、信頼性も過大になりやすい（推測を含む。本論文は例示のみで、推定量の偏りは扱わない）。
- 例は 10 件の人工的な予報で、実データでの検証はない。

## keiba-ai での使い方

- **単勝確率モデルの診断を3項で出す**: 馬単位の2値（勝ち/負け）で、予測確率をビンに分けて BS = 不確実性 + 信頼性 − 分解能 を計算する。不確実性はデータで決まる（頭数が多いレースが多いほど小さい）ので、期間や条件の違うデータ間で BS を比べるときは、分解能と信頼性で比べる。
- **市場との比較を項別に**: 控除率を除いた市場確率とモデル確率を同じビン定義で分解する。仮説: モデルは信頼性（校正）では市場と同程度になれても、分解能では市場に届かない。分解能の差が「市場が知っていてモデルが知らない情報量」の目安になる。
- **校正の効果を切り分ける**: Platt や isotonic で再校正すると、理想的には信頼性だけが下がり分解能は変わらない。isotonic で分解能まで下がるなら、ビンの統合で情報を捨てている。この確認を校正実験の標準出力にする。
- **ビン設計**: 単勝確率は大半が 0–10% に集まる。等幅ビンでは高確率側のビンが小標本になり、分解能が過大に出る。等頻度ビン（分位点）を使い、ビン数による感度を報告する。

## 関連ノート

- [Brier 1950](./1950-brier-verification-probability-forecasts.md): 分解する対象の PS の原典。Table 2 の確率帯別集計が本論文の信頼性・分解能の原型。
- [Gneiting 2007](./2007-gneiting-proper-scoring-rules.md): 適正スコア一般の理論。分解は他の適正スコアにも拡張できる。
- [Niculescu-Mizil 2005](./2005-niculescu-mizil-predicting-good-probabilities.md): 信頼性図と校正法の比較。本分解の信頼性項を下げる手法。
- [Zadrozny 2002](./2002-zadrozny-isotonic-multiclass-calibration.md): isotonic 回帰による校正。分解能を損なわずに信頼性を下げられるかが論点。
- [Walsh 2024](./2024-walsh-calibration-vs-accuracy-betting.md): 賭けでは校正が重要という主張。信頼性項を重視する立場。
- [Constantinou 2012](./2012-constantinou-rps-football.md): 順序カテゴリ向けの RPS。PS と並ぶ多クラス評価。

## 検索語

Murphy 分解, Brier スコアの分解, 確率スコア, 不確実性, 信頼性, 分解能, 校正誤差, 鋭さ, スキルスコア, 気候値, 単体, ベクトル分割, Murphy decomposition, Brier score decomposition, probability score, PS, vector partition, uncertainty, reliability, resolution, sharpness, calibration, refinement, skill score, Sanders, reliability diagram, Journal of Applied Meteorology

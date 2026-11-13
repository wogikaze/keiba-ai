---
title: Horse Racing: Testing the Efficient Markets Model
authors: Snyder Wayne W.
year: 1978
venue: The Journal of Finance 33(4) 1109-1118
url: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1978.tb02051.x
doi: 10.1111/j.1540-6261.1978.tb02051.x
topic: market-efficiency
tags: efficient-market-hypothesis, favourite-longshot-bias, parimutuel, classic, weak-form, semi-strong-form, strong-form, morning-line
verified: metadata
importance: medium
source: unavailable
source_version:
---

# 競馬で効率的市場モデルを検定する：証券市場の3つの効率性を競馬に当てはめた最初の論文

> **原本未取得**。Journal of Finance（Wiley/JSTOR）で有料。World Scientific の論文集 *Efficiency of Racetrack Betting Markets*（2008 年版, 第27章 pp.269–278）にも再録されているが有料。無料版は見つからなかった。本ノートは Sauer (1998) の要約と Figure 1、Green ら (2019) の言及、書誌サイトの情報に基づく。ページは引用元のもの。

> 一言で: Fama 流の「弱度・準強度・強度」の効率性の枠組みを競馬に持ち込み、北米の6研究・約5万レースを集計して、控除率を戻した回収率は本命で +9.1%、33-1 以上の大穴で −23.7% と、本命-大穴バイアスはあるが控除率を超える利益は出ないことを示した。

## 書誌と構成

- Journal of Finance 33(4), pp.1109–1118（1978 年9月）。JSTOR の DOI は 10.2307/2326943。初出は 1976 年12月の第3回ギャンブル会議（ラスベガス）での報告。著者は当時 Sangamon State University（書誌サイトの情報）。
- 節は「パリミュチュエル方式」「弱度」「準強度」「強度」「結論」の順（書誌サイトの目次）。

## 3つの効率性をどう当てはめたか

証券市場の効率的市場仮説の含意は、(1) 価格が利用可能な情報をすべて反映する、(2) 専門家は平常以上の利益を得られない、の2つである。Snyder はこれを競馬に当てはめる（書誌サイトの要旨による）。

| 効率性 | 競馬での問い（二次資料からの再構成） |
|---|---|
| 弱度 | 過去の価格（オッズ）の情報だけで利益が出るか。オッズ帯別の回収率に偏りがあっても、控除率を超える利益が出なければ弱度効率的 |
| 準強度 | 公開情報（予想家の印、朝のオッズ = morning line）で利益が出るか |
| 強度 | 非公開の情報を含めて、専門家が平常以上の利益を得られるか |

細かい定義は Vannebo (1980) のコメントで批判された（後述）。準強度・強度の検定で何をどの検定に割り当てたかは、原本未読のため未確認。

## 弱度の検定：北米の集計（Sauer 1998 による）

Snyder は Griffith (1949)、McGlothlin (1956)、Weitzman (1965) などを含む6つの研究、合計約 50,000 レースの北米データを集めた（Sauer 1998, p.2035）。McGlothlin と同じく、控除率を戻した回収率をオッズ帯ごとに計算した。控除を戻しているので、偏りがなければ全オッズ帯で 0 になるはずである。

- 控除前の回収率は、1倍未満の本命（$O_i < 1$）の +9.1% から、33-1 以上の大穴の −23.7% まで、オッズが長いほど下がる（Sauer 1998, pp.2035–2036）。
- Sauer の Figure 1（p.2036）は Snyder の米国パリミュチュエルの値と Dowie (1976) の英国ブックメーカーの値を重ねて描いている。英国の方が大穴の回収率がずっと低い。

控除率（当時の北米で十数パーセント）を差し引くと、本命の +9.1% も実際の回収率では赤字になる。したがって「バイアスはあるが、利益の出る単純な賭け方はない」という意味で弱度効率的、というのが一般的な読み方である（後続研究の要約による）。

## 準強度：朝のオッズにもバイアスがある

Snyder は朝のオッズ（競馬場の予想家が出走表に載せる予想オッズ）を手で集め、それ自体にも本命-大穴バイアスがあることに頭を悩ませている（Green ら 2019, PDF p.7 脚注9）。Green らは、朝のオッズの役割について Snyder (1978, p.1117) を引用している（Green 2019, PDF p.4 脚注4）。朝のオッズに偏りがあることは、のちに Green ら (2019) が「競馬場が朝のオッズで賭け手を誤導している」という説明を組み立てる出発点になった。

## 批判と後続

- **Vannebo (1980) のコメント**。Journal of Finance 35, pp.201–202。弱度・強度の検定の定義に異を唱えた（後続研究の紹介による）。
- **"Back on the Track with the Efficient Markets Hypothesis"**（同じく論文集に再録）は、Snyder の強度の検定の議論を、予想家のオッズが大衆のオッズに与える影響も測れる、より強い検定に作り直した（書誌サイトの紹介）。
- **サーベイとしての位置**。芦谷 (2010, p.3) は、本論文を本命-大穴バイアスのサーベイの最初のものとして挙げている。

## 批判的に読む

- **集計研究である**。6研究のデータを合わせたもので、競馬場・年代・控除率が異なる。控除を戻す処理は研究ごとの控除率に依存し、breakage（払戻の切り捨て）の扱いも揃っていない可能性がある。
- **「控除を戻した回収率」と「実際の回収率」の混同に注意**。+9.1% は控除前の数値で、実際に賭けて得られる回収率ではない。後の研究で「本命の期待利益は正」と引用されるとき、この区別が落ちることがある。
- **効率性の定義の移植**。証券市場では空売りができ、裁定でバイアスが消えうるが、パリミュチュエルでは割高な馬券を空売りできない（Thaler & Ziemba 1988 の指摘, 芦谷 2010, p.8 による）。弱度の検定の意味は証券市場と同じではない。
- 原本未読のため、オッズ帯ごとの数値表、準強度・強度の検定の具体的な方法と結果は未確認。

## keiba-ai での使い方

- **評価の言葉をそろえる**。keiba-ai の実験報告で「市場に勝った」と言うときは、Snyder の3分類に沿って、どの情報（オッズのみ、公開情報、非公開情報）で、控除率込みの実際の回収率が1を超えたかを明記する。控除を戻した回収率は較正の診断であって、収益性の証拠ではない。
- **オッズ帯別回収率表の標準形**。オッズを対数スケールの帯に分け、「控除戻し回収率」と「実払戻の回収率」を並べ、標本数と標準誤差を付ける。Sauer の Figure 1 と同じ図を JRA のデータで描けば、米英との比較もできる。
- **予想オッズ（JRA なら新聞の予想印・前日オッズ）にもバイアスがあるか**。仮説: 前日発売や朝の時点のオッズは最終オッズより本命-大穴バイアスが強い。これはオッズの時系列特徴量（前日→最終の変化）の設計に効く。

## 関連ノート

- [Griffith 1949](./1949-griffith-odds-adjustments.md): Snyder が集計した研究の一つ。バイアスの最初の報告。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): 同時期の北米ハーネスの研究。
- [Hausch ら 1981](./1981-hausch-racetrack-market-efficiency.md): 単勝プールが効率的だと仮定し、複勝・3着内プールの非効率を突いた。Snyder の「弱度効率的」を前提にした応用。
- [Asch ら 1982](./1982-asch-racetrack-informed-behavior.md): 朝のオッズと最終オッズの比較から情報を持つ賭け手を示した。
- [Thaler & Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 弱度効率性の定義（正の期待値の賭けは存在しない）を整理したサーベイ。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Snyder の集計を Figure 1 に再掲。
- [Green ら 2019](./2019-green-favorite-longshot-midas.md): 朝のオッズのバイアスを競馬場による誤導として説明。Snyder を唯一の先行例として引く。
- [芦谷 2010](./2010-ashiya-longshot-bias-survey.md): 日本語サーベイ。
- [Sung & Johnson 2007](./2007-sung-two-step-conditional-logit.md): 投機市場の行動を見る窓として Snyder を引用する予測モデル研究。

## 検索語

効率的市場仮説, efficient market hypothesis, EMH, 弱度効率性, weak form efficiency, 準強度効率性, semi-strong form, 強度効率性, strong form, 本命-大穴バイアス, favourite-longshot bias, favorite-longshot bias, FLB, 控除率, takeout, 控除戻し回収率, 回収率, rate of return, オッズ帯, odds range, 朝のオッズ, morning line, 予想オッズ, 予想家, handicapper, パリミュチュエル, parimutuel, 北米競馬, Snyder 1978, Journal of Finance, Vannebo 1980

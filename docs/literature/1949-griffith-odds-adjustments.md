---
title: Odds Adjustments by American Horse-Race Bettors
authors: Griffith R. M.
year: 1949
venue: The American Journal of Psychology 62(2) 290-294
url: https://www.semanticscholar.org/paper/Odds-adjustments-by-American-horse-race-bettors.-Griffith/fb66e08aefcad0cfd5f911dad027dc24e3b0c503
doi: 10.2307/1418469
topic: market-efficiency
tags: favourite-longshot-bias, parimutuel, subjective-probability, classic, psychology, probability-misperception
verified: metadata
importance: medium
source: unavailable
source_version:
---

# 米国の競馬の賭け手によるオッズの調整：本命-大穴バイアスの最初の報告

> **原本未取得**。American Journal of Psychology（JSTOR）で有料。World Scientific の論文集 *Efficiency of Racetrack Betting Markets*（2008 年版, pp.9–13）にも再録されているが有料。無料版は見つからなかった。本ノートは Sauer (1998)、Jullien & Salanié (2005)（以下 JS2005）、Snowberg & Wolfers (2010) での要約に基づく。ページは引用元のもの。

> 一言で: 心理学者 Griffith が 1947 年の米国 1,386 レースを調べ、単勝の票数シェアは勝率と「驚くほど」よく一致する一方、本命の勝つ見込みは系統的に低く、大穴は高く見積もられていることを示した。のちに本命-大穴バイアス（favorite-longshot bias）と呼ばれる現象の最初の記録である。統計的な追試は McGlothlin (1956, 9,248 レース) が行った（本リポジトリにノートなし）。

## 背景と問い

Griffith と McGlothlin (1956) は、競馬の賭け市場を不確実性下の行動を調べる場として最初に使った心理学者である（Sauer 1998, p.2033）。賭け手が確率の小さな違いをどこまで識別できるかを、単勝の票数シェア $w_i = W_i/W$ を使って調べた。

## データと方法

- 1947 年に米国のパリミュチュエルで行われた 1,386 レース（JS2005 p.3; Sauer 1998, p.2034）。
- 馬を単勝オッズで 11 の階級に分けた。最も低い階級はオッズ $O_i \le 1$（1倍返し以下の本命）、最も高い階級は $O_i > 15$（Sauer 1998, p.2034）。
- 階級 $k$ の出走頭数を $H_k$、勝った頭数を $N_k$ とし、$H_k$ と $N_k/w_k$ を比べた。$w_k \approx p_k$（票数シェアが勝率に等しい）なら、$N_k/w_k \approx H_k$ となる（Sauer 1998, p.2034）。JS2005 の言い方では、階級ごとに出走頭数 $E_R$ と「勝ち馬の数 × オッズ」$N_R$ を比べた（JS2005 p.3）。どちらも、控除率を除けば「その階級に1単位ずつ賭けたときの払戻」と「賭けた額」の比較である。

## 結果

1. **全体としてはよく一致する**。$N_k/w_k$ と $H_k$ の「ほぼ一致」を Griffith は「注目すべき（remarkable）」と述べた（Griffith pp.292–93, Sauer 1998, p.2034 による）。これは票数シェアを主観確率の推定値として使うことを正当化する。
2. **ただし両端で系統的にずれる**。オッズの低い本命では $N_k/w_k$ が $H_k$ をわずかに上回り（$w_k < p_k$）、オッズの高い大穴では逆（$w_k > p_k$）になる（Sauer 1998, p.2034）。

> "a systematic undervaluation of the chances of short-odded horses and over-valuation of those of long-odded horses" (Griffith の言葉, JS2005 p.4 の引用)

3. **心理学的な解釈**。Griffith は、調査や実験で見られる「大きな確率を過小に、小さな確率を過大に見積もる」傾向が、現実の市場にも現れたものと解釈した（Sauer 1998, p.2038; JS2005 p.4）。これが本命-大穴バイアスの「知覚の歪み」説の起源である。

## その後の評価

- **バイアスは50年以上安定している**。Snowberg & Wolfers (2010, PDF p.7, Figure 2) は、Griffith の数値を 1992–2001 年の米国、豪州、英国のデータ、Weitzman、Harville、Ali、Jullien & Salanié の推定と同じ図に描き、バイアスの形が Griffith 以来ほとんど変わっていないことを示した。
- **知覚の歪み説への反論**。Sauer (1998, p.2038) は、実験の質問は一回限りのものが多く、経験を積むと確率の推定は改善するので、反復の多い競馬場でバイアスの原因を知覚の歪みに帰すのは「早計」だと論じた。逆に Snowberg & Wolfers (2010) は、連勝式の価格を使って、リスク愛好よりも知覚の歪みの方がデータに合うと結論した。Griffith の解釈は、半世紀後に再び有力になったと言える。
- **確率加重関数としての定式化**。Jullien & Salanié (2000) は Griffith 型の加重関数を順位依存効用の一つの型として推定したが、推定された加重はほぼ対角線で、Griffith が想定した向きではなかった（JS2005 p.12）。

## 批判的に読む

- **小標本・単年**。1,386 レース・1年分で、11 階級のうち大穴側の階級は頭数が少ないはず。Sauer は統計検定に触れていない。McGlothlin (1956) が 9,248 レースで標準誤差の2〜4倍の差を示したののが、最初の統計的な裏付けである（Sauer 1998, p.2034）。
- **控除率の扱い**。$N_k/w_k$ と $H_k$ の比較は控除率を除いた比較で、回収率そのものではない。実際の回収率は全階級で1を下回る。
- 原本未読のため、どの競馬場のデータか、図の形、階級ごとの数値は未確認。

## keiba-ai での使い方

- **最初の較正診断の型**。Griffith の比較（オッズ階級ごとに「出走頭数」と「勝ち馬数 × オッズ」を比べる）は、JRA の単勝でオッズ由来確率の較正を見る最も単純な方法である。控除率を戻した回収率をオッズ階級別に描けば同じことが分かる。Snowberg & Wolfers の図と同じく、横軸をオッズの対数にする。
- **確率の知覚の歪みとしてモデル化する**。仮説: JRA の単勝でも、市場確率 $w_i$ を確率加重関数の逆写像で補正した $\tilde p_i$（例: Prelec 型 $w = \exp(-(-\ln p)^\alpha)$ の逆）は、$w_i$ より log loss が小さい。補正のパラメータは時系列で分割した学習期間だけで推定する。

## 関連ノート

- [Ali 1977](./1977-ali-probability-utility-estimates.md): 人気順位別の方法で北米ハーネスのバイアスを確認。
- [Snyder 1978](./1978-snyder-efficient-markets-horse-racing.md): Griffith を含む北米6研究・5万レースの集計。
- [Thaler & Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 本命-大穴バイアスをアノマリーとして整理したサーベイ。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Griffith の方法と結論を詳しく紹介し、知覚の歪み説を批判。
- [Jullien & Salanié 2000](./2000-jullien-estimating-preferences-racetrack.md): Griffith 型の確率加重関数を推定。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): 知覚の歪み説を連勝式で支持。Griffith の数値を図に再掲。
- [芦谷 2010](./2010-ashiya-longshot-bias-survey.md): 日本語サーベイ。Griffith 以降の研究を整理。
- [Mori & Hisakado 2009](./2009-mori-scale-invariance-efficiency.md): Griffith を引用し JRA の投票データで効率性を分析。

## 検索語

本命-大穴バイアス, 本命大穴バイアス, 穴馬バイアス, favourite-longshot bias, favorite-longshot bias, FLB, 最初の報告, Griffith 1949, オッズの調整, odds adjustment, 主観確率, subjective probability, 確率の知覚の歪み, probability misperception, 小さな確率の過大評価, overweighting small probabilities, 確率加重, probability weighting, 心理学, psychology, パリミュチュエル, parimutuel, 単勝, win pool, 票数シェア, American Journal of Psychology

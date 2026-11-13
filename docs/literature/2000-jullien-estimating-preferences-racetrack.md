---
title: Estimating Preferences under Risk: The Case of Racetrack Bettors
authors: Jullien Bruno, Salanié Bernard
year: 2000
venue: Journal of Political Economy 108(3) 503-530
url: https://www.journals.uchicago.edu/doi/abs/10.1086/262127
doi: 10.1086/262127
topic: market-efficiency
tags: favourite-longshot-bias, risk-preference, prospect-theory, rank-dependent-utility, uk, bookmaker, probability-weighting, representative-agent
verified: abstract
importance: high
source: unavailable
source_version:
---

# 英国平地競走 34,443 レースから代表的賭け手の選好を推定する：期待効用・順位依存効用・累積プロスペクト理論の比較

> **原本未取得**。JPE 本体は有料で、無料版（SSRN 113709）は自動取得が拒否され、CREST WP 97-39 の PDF には本文がなかった。本ノートは、要旨（SSRN/RePEc）と、同じ著者による解説章 Jullien & Salanié (2005) "Empirical Evidence on the Preferences of Racetrack Bettors"（IDEI WP, Hausch & Ziemba 編 Handbook 所収の草稿, TSE サイトで公開）に基づく。ページ番号は 2005 年草稿のもの（「JS2005 p.N」と書く）。

> 一言で: オッズと勝ち馬だけから代表的賭け手の効用関数と確率加重関数を最尤推定すると、期待効用では CARA 型の弱いリスク愛好が最もよく合う。順位依存効用（RDEU）は期待効用とほとんど変わらず、累積プロスペクト理論（CPT）で「損失側の確率加重が凹」になる形がもっとも説明力が高い。本命-大穴バイアスはリスク愛好だけでなく、損失確率の主観的な重み付けでも説明できる。

## 要旨

英国の平地競走で、代表的な賭け手の危険に対する態度を推定する。期待効用を超えて、多項モデルを 34,443 レースのデータで推定する。順位依存効用モデルは期待効用より目立って良くはならないが、累積プロスペクト理論は説明力が高い（SSRN 要旨）。好ましい推定値は、Friedman–Savage 型に似た局所的な危険態度を示す（RePEc の要旨）。

## データ

- 英国の平地競走、1986〜1995 年の全レース、34,443 レース（JS2005 p.4）。
- 英国はブックメーカー方式なので、オッズは契約時点で確定している（JS2005 p.4）。単勝のみ。
- 同データでオッズ $R$ ごとの期待収益 $\widehat{ER}(R) = \hat p(R)R - (1-\hat p(R))$ を描くと、期待収益は常に負で、オッズが長いほど単調に悪化する。オッズ 1-1（evens）では損失が1ポンドあたり10ペンス未満、10-1 では約25ペンス（JS2005 p.4, Figure 1）。

## 推定方法

既存研究（Weitzman 1965, Ali 1977 など）はオッズ帯ごとに勝率を集計して効用関数を当てはめていた。この方法では、ブックメーカーの利幅（オーバーラウンド）がレースごとに違うと偏りが出る（JS2005 p.9, 脚注21）。

Jullien & Salanié は、レースごとに定数を置いてこの問題を避ける。レース $r$ の馬 $i$ の客観的勝率を $p_{ir}$、オッズを $R_{ir}$、効用関数を $u$ とし、代表的賭け手はそのレースのどの馬に1ポンド賭けても無差別だとする（JS2005 p.9）。

$$p_{ir}\,u(R_{ir}) + (1-p_{ir})\,u(-1) = K_r$$

$\sum_i p_{ir} = 1$ を使うと、$u$ を与えればレースごとに $K_r$ と各馬の予測勝率 $\hat p(i,r,u)$ が一意に決まる。実際の勝ち馬に対する尤度を最大化して $u$（と確率加重関数）を推定する。オッズ帯に分ける必要がなく全データを使える。レースごとに一様な「賭けること自体の効用」はこの定数に吸収される（JS2005 p.17）。

比較したモデル:

1. **期待効用**: CRRA, CARA, HARA（双曲型絶対リスク回避）族。
2. **順位依存期待効用（RDEU）**: 効用は CARA に固定し、勝つ確率に加重関数 $G(p)$ を掛ける。Griffith 型・Henery 型・Prelec (1998) 型などを入れ子にした柔軟な形（JS2005 p.12）。
3. **累積プロスペクト理論（CPT）**: 利得側の加重 $G$ と損失側の加重 $H$ を別に推定する。$u$ は CARA で $u(0)=0$, $u'(0)=1$ に正規化（JS2005 p.14）。

## 結果

| モデル | 結果（JS2005 での記述） |
|---|---|
| 期待効用 | リスク愛好を確認。HARA 族の中では CARA が最良で、リスク愛好の程度は穏やか。CRRA は CARA に劣る（p.9） |
| 期待効用の弱点 | 大本命の勝率を小さく予測しすぎる（p.9） |
| RDEU | 推定された $G(p)$ はどの型でもほぼ対角線。期待効用の帰無仮説が棄却されるのは Prelec 型の1つだけ。むしろわずかに凸で、Griffith や Henery が想定した向きではない（p.12） |
| CPT | 利得側 $G$ はほぼ対角線（わずかに凸）。損失側 $H$ はどの型でもはっきり凹（pp.15–17, Figures 3–4） |

CPT の推定がバイアスをどう説明するかを、著者らは次のように簡約している（JS2005 p.17）。$u(x)=x$, $G(p)=p$ と近似すると馬 $i$ の評価は $p_i(R_i+1) - 1 - (H(1-p_i) - (1-p_i))$ になる。推定された $H(q)-q$ は $q \approx 0.2$ 付近で最大になる。ほとんどの馬は勝率が 0.8 よりずっと小さいので、$H(1-p)-(1-p)$ は $p$ の増加関数になる。均衡では期待収益 $p_i(R_i+1)-1$ が勝率とともに増える。これがまさに本命-大穴バイアスである。

> "the favorite-longshot bias is compatible with risk-averse behavior, contrary to the standard interpretation." (JS2005 p.17)

つまり、損失確率の重み付けが凹であることが、リスク愛好なしでもバイアスを生む。同じ推定は「馬ごとに異なる賭けの効用 $f(p_i,R_i) = 1-p_i-H(1-p_i)$ を持つリスク中立の賭け手」とも読める（JS2005 p.17）。

## 批判的に読む

- **代表的個人の仮定**。全員が同じ選好を持つとして集計データから選好を復元している。Sauer (1998) や Gandhi らが強調するように、情報や信念の異質性があれば同じ価格パターンが別の理由で生じうる。後続の Chiappori, Gandhi, Salanié & Salanié (2019, Econometrica) は異質な選好を許す形に拡張している。
- **CARA の固定**。著者自身が 2005 年の章で、$u$ を CARA に固定したのは損失回避を構造的に排除してしまい「満足できない」と認めている（JS2005 p.14）。データからは $u(-1)$ と $u$ の $[R_{min}, \infty)$ 上の値しか識別できない。
- **観測的同値性**。Snowberg & Wolfers (2010) は、単勝データだけではリスク愛好と確率の知覚の歪みは区別できないと示し、連勝式の価格を使って識別した。彼らは本論文の結果を「知覚に基づく説明を支持する」側に分類している。
- **ブックメーカー市場である点**。英国の SP オッズにはインサイダーへの備え（Shin 型の価格付け）が混ざる。パリミュチュエルの JRA に結果をそのまま移せるかは未確認。
- 原本未読のため、パラメータの数値、標準誤差、標本外の検証の有無は未確認。

## keiba-ai での使い方

- **オッズ→確率の写像を構造的に作る**。本論文の「レースごとの定数 $K_r$ + 効用（または加重）関数」は、オッズから勝率を出す写像を1パラメータ族で表す方法になる。仮説: JRA 単勝で、$p_{ir} \propto$（CARA 型の効用で補正したオッズの関数）や Prelec 型の加重で補正した市場確率は、票数シェアをそのまま使うより log loss が小さい。比較対象は (a) 票数シェア、(b) $w_i^\alpha$ の累乗補正、(c) 本論文型の構造モデル。
- **レース内正規化の重要性**。$K_r$ をレースごとに置く発想は、控除率・オーバーラウンドや「レースごとの賭けの効用」をレース内で吸収する。keiba-ai でもオッズ特徴量は必ずレース内で正規化する（レース間で生のオッズを比べない）。
- **大本命の扱い**。期待効用モデルは大本命の勝率を過小に予測する（JS2005 p.9）。オッズ由来確率の較正曲線を作るとき、1倍台の本命の区間は別に評価する。
- **日本データでの追試**。小幡・太宰の日本のプロスペクト理論研究と合わせて、JRA の単勝で $H$ の凹性が再現するかを検証する実験が考えられる。

## 関連ノート

- [Griffith 1949](./1949-griffith-odds-adjustments.md): 確率の主観的な歪みという説明の出発点。RDEU の加重関数の一つの型。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): オッズ帯ごとに代表的個人の効用を推定した先行研究。本論文はその集計方法を改良した。
- [Thaler & Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 損失回避・心の会計による解釈。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): 代表的個人モデルの限界を論じたサーベイ。
- [Snowberg & Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): リスク愛好と知覚の歪みを連勝式で識別。本論文を同じ問いの先行研究として引く。
- [Gandhi & Serrano-Padial 2015](./2015-gandhi-belief-heterogeneity-longshot.md): 信念の異質性で説明する立場。本論文と結論が分かれる。
- [小幡・太宰 2014](./2014-obata-horse-racing-prospect-theory.md): 日本競馬でプロスペクト理論を検証。本論文を引用。
- [小幡・太宰 2012](./2012-obata-prospect-theory-trifecta.md): 三連単でのプロスペクト理論。
- [芦谷 2010](./2010-ashiya-longshot-bias-survey.md): 日本語サーベイ。本論文をプロスペクト理論の支持例として紹介。

## 検索語

リスク選好の推定, 危険選好, 代表的賭け手, representative bettor, 期待効用, expected utility, CARA, CRRA, HARA, 絶対リスク回避, リスク愛好, risk loving, 順位依存効用, rank-dependent expected utility, RDEU, RDU, 累積プロスペクト理論, cumulative prospect theory, CPT, 確率加重関数, probability weighting function, Prelec, 損失回避, loss aversion, Friedman-Savage, 本命-大穴バイアス, favorite-longshot bias, FLB, 英国競馬, ブックメーカー, bookmaker, 最尤推定, maximum likelihood, 多項モデル, multinomial model, Jullien Salanié 2000, Journal of Political Economy

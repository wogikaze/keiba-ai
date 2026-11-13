---
title: Probability models on horse-race outcomes
authors: Ali Mukhtar M.
year: 1998
venue: Journal of Applied Statistics 25(2) 221-229
url: https://www.stat.berkeley.edu/~aldous/157/Papers/ali.pdf
doi: 10.1080/02664769823205
topic: probability-models
tags: henery-model, gamma-model, normal-ranking-model, ordering-probability, favourite-longshot-bias
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 単勝オッズから作る2着・3着確率は人気馬で過大になる：正規・ガンマ順位モデルを1.5万レースで検証

> 一言で: ニューヨーク州のハーネス（繋駕速歩）競走 15,402 レース（8頭立て）で、単勝票数から推定した正規順位モデルとガンマ順位モデル（形状 r=0.5〜20）の2着・3着確率を実際の頻度と比べた。正規モデル（Henery 型）が最もずれが小さいが、どのモデルも1番人気の2・3着確率を有意に過大評価し、下位人気を過小評価した。

## 要旨

Harville (1973) の 335 レース、Stern (1990) の 47 レースは規模が小さく、Bacon-Shone ら (1992)、Lo & Bacon-Shone (1994) は尤度でモデルを比べただけで、推定された確率がどれだけ正確かは調べていない (p.221–222)。本論文は1万5千レース超で「モデルの2・3着確率」と「人気順ごとの実際の2・3着率」を直接比べる。

## モデル

$k$ 頭の着順を独立な確率変数 $X_1,\dots,X_k$（分布 $F(x;a_i)$）の大小順と見なす順位モデルの族を使う (p.222)。

- **正規順位モデル N(0,1)**: $X_i\sim N(a_i,1)$。Thurstone–Daniels–Mosteller 型で、Henery (1981) が競馬に提案したもの。制約 $\sum a_i=0$。
- **ガンマ順位モデル G(r)**: $X_i$ が尺度 $a_i$、共通の形状 $r$ のガンマ分布 (p.223)。$r=1$ で指数分布となり Luce/Harville モデルに一致する。$r$ を大きくすると正規モデルに近づく。制約 $\sum a_i=1$。

単勝確率 $p(i)=\int f(x;a_i)\prod_{j\ne i}[1-F(x;a_j)]dx$（式4）、2着確率 $p(i,2)$、3着確率 $p(i,3)$（式7, 8）はいずれも数値積分で計算する (p.224, 226)。

### パラメータの推定（1レース1観測の問題）

各レースのパラメータはレースごとに違うので、レースをまたいで着順をプールできない。そこで単勝オッズから「実際の勝率」$p_n(i)$ を推定し、モデルの単勝確率をそれに一致させる（Stern 1990 が示した最尤方程式 $p(i)=p_n(i)$）(p.223–224)。

1. 単勝票の割合: $W_i/W=[1/(1+O_i)]/\sum[1/(1+O_i)]$（式2）。$O_i$ はオッズ（控除率と端数切りを含む）。
2. 勝率は $(W_i/W)^d$ に比例すると置く（人気-大穴バイアスの補正）。$d$ は先行研究から Saratoga で 1.16、Roosevelt と Yonkers で 1.13 (p.226)。
3. $S=\sum[p(i)-p_n(i)]^2$ を Marquardt 修正 Gauss–Newton で最小化 (p.224, 式5)。
4. 初期値: 正規モデルは Henery (1981) の近似式（式6）。ガンマモデルは $a_i\propto p_n(i)^{g(r)}$、$g(r)=2/(1+r)$ を試行錯誤で決めた (p.224)。

## データ

| 競馬場 | 年 | レース数 |
|---|---|---|
| Saratoga | 1970–74 | 1,721〜1,909/年 |
| Roosevelt | 1970–74 | 1,347〜1,698/年 |
| Yonkers | 1971–74 | 1,268〜1,407/年 |

(p.225, Table 1)。全てニューヨーク州のハーネス競走で、Ali (1977) と同じデータ。合計 20,247 レースのうち、同着を除き、8頭立てだけに絞った 15,402 レースを使う (p.224–225)。G(0.5) は数値計算の都合か 14,059 レースのみ（理由は記載なし）。

評価: 人気順（単勝オッズ順）でグループ化し、モデルの平均2着（3着）確率 M と、実際の2着（3着）率 O を比べる。$SE=\sqrt{O(1-O)/n}$ で標準化した $(M-O)/SE$ を報告 (p.225)。

## 主要な結果

2着確率（抜粋, p.227, Table 2）:

| モデル | 1番人気 M | O | (M−O)/SE | 7番人気 M | O | (M−O)/SE |
|---|---|---|---|---|---|---|
| N(0,1) | 0.210 | 0.192 | 5.74 | 0.061 | 0.068 | −3.14 |
| G(1)=Harville | 0.256 | 0.192 | 20.20 | 0.045 | 0.068 | −11.11 |
| G(5) | 0.230 | 0.192 | 11.91 | 0.054 | 0.068 | −6.70 |
| G(20) | 0.220 | 0.192 | 8.75 | 0.058 | 0.068 | −4.96 |

3着確率（抜粋, p.228, Table 3）:

| モデル | 1番人気 M | O | (M−O)/SE | 8番人気 M | O | (M−O)/SE |
|---|---|---|---|---|---|---|
| N(0,1) | 0.147 | 0.129 | 6.79 | 0.063 | 0.071 | −3.78 |
| G(1)=Harville | 0.178 | 0.129 | 18.09 | 0.037 | 0.071 | −16.33 |
| G(20) | 0.153 | 0.129 | 9.03 | 0.057 | 0.071 | −6.56 |

読み方:

- Harville（G(1)）は1番人気の2着確率を 0.256 と見積もるが実際は 0.192。3着では 0.178 対 0.129 と、3割以上過大。
- $r$ を大きくするほど（正規に近づくほど）ずれは単調に小さくなり、正規モデルが全体で最小 (p.226)。これは Bacon-Shone ら、Lo & Bacon-Shone と一致する。
- それでも正規モデルですら1番人気で 5.7〜6.8 SE ずれる。著者はこの「2・3着での人気-大穴バイアス」を、年・競馬場別に分けても同じだったとし (p.227)、どの順位モデルも利益の出る賭け戦略には使えないと結論する。

> It is found that the normal ranking model best fits the data, but all models suffer from favorite–longshot bias (p.227)

結論部では、Hausch, Ziemba & Rubinstein (1981) の複勝・3着内（place/show）戦略の黒字は標本の特殊性によるかもしれず、Lo ら (1994) が同じ戦略を Meadowlands、香港、日本に当てると赤字だったと付け加える (p.228)。

## 批判的に読む

- **単勝確率の補正と順位モデルの誤差が混ざる**: $d$ による補正は「1着の確率」を合わせるもので、それでも2・3着がずれるのは順位モデル側の誤差と読める。ただし $d$ は先行研究の値を固定で使っており、データ期間で再推定していない。
- **本文中の記述の揺れ**: 第3節末尾 (p.226–227) は「勝率の低い馬の2・3着確率を過大評価」と書くが、表と結論は「過小評価」を示す。表と結論を正とした。表には G(2.0) の6番人気 M が 0.971 という明らかな誤植もある (p.227)。
- **ハーネス競走・8頭立て限定**: サラブレッドの平地競走ではない。頭数を8に固定しているため、頭数依存は分からない。1970年代前半のデータ。
- **評価は人気順の平均だけ**: 対数損失などの適切なスコアや、レース単位の較正は報告していない。人気順で平均すると、同じ人気順でもオッズの違うレースが混ざる。
- **賭けの検証はしていない**: 「利益の出る戦略は作れない」はバイアスの存在からの推論であり、回収率を計算したわけではない。
- 推定値の初期値や数値積分の詳細は書かれているので、再現性は比較的高い。

## keiba-ai での使い方

- **馬連・ワイド・3連系の確率を単勝確率から合成するとき**、Harville（Plackett-Luce を単勝確率にそのまま当てる方法）は人気馬の2・3着を過大評価する。日本の券種で同じことが起きるかを最初に確かめる。
- **実験案（仮説）**: JRA の過去データで、単勝確率（市場またはモデル）から Harville / Henery（正規）/ Stern（G(r)）/ Lo-Bacon-Shone の割引 Harville で2着・3着確率を作り、人気順ごとの (M−O)/SE と、複勝・ワイドの対数損失を比べる。仮説は「正規または割引ありの方が対数損失が小さく、特に1〜2番人気で差が出る」。
- **評価指標**: 本論文の人気順別 M vs O 表は、較正図（reliability diagram）の券種別版としてそのまま使える。`src/keiba_ai/` の評価に「着順別較正表」を足す価値がある。
- **頭数**: 本論文は8頭立てのみ。JRA は頭数のばらつきが大きいので、頭数で層別して同じ表を作る。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): G(1) にあたる。本論文はその過大評価を大規模に再確認。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規順位モデルの提案元。本論文で最良。
- [Stern 1990](./1990-stern-gamma-permutations.md): ガンマ順位モデル。r を変えた比較の出所。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): 尤度比較で Henery 優位。本論文はそれでも偏りが残ると反論。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 順位確率モデルを賭けに使った検証。
- [Hausch, Ziemba & Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): Harville で複勝・3着内の割安を探した戦略。本論文は黒字の再現性に疑問。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): 同じハーネス競走データで単勝の人気-大穴バイアスを測った前作。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): 順位確率の近似の後続研究。

## 検索語

着順確率, 順位確率, ordering probability, ranking probability, 正規順位モデル, normal ranking model, Thurstone モデル, ガンマ順位モデル, gamma ranking model, Henery モデル, Harville モデル, Stern モデル, Luce モデル, 2着確率, 3着確率, 複勝, place, show, 人気-大穴バイアス, favourite-longshot bias, FLB, ハーネス競走, 繋駕速歩, harness racing, Saratoga, Roosevelt, Yonkers, 単勝票数, win pool fraction, 較正, calibration

---
title: Efficiency of the Market for Racetrack Betting
authors: Hausch Donald B., Ziemba William T., Rubinstein Mark
year: 1981
venue: Management Science 27(12) 1435-1452
url: https://pubsonline.informs.org/doi/10.1287/mnsc.27.12.1435
doi: 10.1287/mnsc.27.12.1435
topic: betting-strategy
tags: place-show, dr-z-system, kelly, parimutuel, harville, market-impact, weak-form-efficiency
verified: abstract
importance: high
source: unavailable
source_version:
---

# 単勝プールから複勝・3着内を値付けする：Dr Z システムの原典

> 原本未取得。INFORMS は購読制で、OpenAlex・Semantic Scholar に OA 版が無く、UBC のワーキングペーパー版（1980）の公開版も見つからなかった。第三者サイトの無許諾と思われる複製は使っていない。本ノートは要旨と、原本取得済みの二次資料（Ziemba 2023、Sauer 1998、Ali 1998）に基づく。ページは二次資料のもの。

> 一言で: 単勝プールの投票割合を勝率とみなし、Harville の式で2着・3着内の確率を出して、place（2着内）・show（3着内）プールの配当と比べる。ずれが大きいときだけ、自分の賭けによる配当低下を含めた対数効用最大化で賭け金を決める。単勝では FLB があっても利益は出ないが、place/show では利益が出た、と報告した。

## 問題と考え方

単勝の市場は比較的効率的だが、place と show は組み合わせが多く（10頭立ての show で 720 通りの着順）、正しい配当を計算しにくい (Ziemba 2023, p.649)。そこで「単純な市場の価格で複雑な市場の賭けを値付けし、割安なものだけ買う」という、価格情報だけによる弱度の効率性の検定になる (Ziemba 2023, p.649)。

Sauer の整理では、Harville の式が正しく単勝が効率的なら、各馬の単勝・place・show のプールシェアは等しくなるはずで、ずれれば Harville の仮定が誤りか、どこかのプールが誤って値付けされている (Sauer 1998, p.27)。

## モデル（Ziemba 2023 による再掲）

- $q_i$: 単勝プールから得た馬 $i$ の勝率。Harville により $i$-$j$ の順の確率は $q_iq_j/(1-q_i)$ (Ziemba 2023, p.649)。
- $Q$: 払戻率（控除後）。米国で約 0.82、プロ向けのリベート込みで約 0.88 (p.649)。
- $p_j, s_k$: 自分の place・show の賭け金、$P_i, S_k$: 他人の賭け金、$w_0$: 初期資産。
- 目的関数: すべての $i$-$j$-$k$ の着順について、Harville 確率 × log（控除後のプールを当たり馬券で分けた自分の払戻 + 賭けなかった資金）の和を最大化する (p.650)。自分の賭け $p_i, s_i$ が分母に入るので、配当低下が自動的に入る。
- 非凹の非線形計画だが、数値的には収束する (p.650)。

### 競馬場で使える近似式

数千回の最適化結果から回帰で近似した、4つの数字だけで計算できる期待値の式が示されている (Ziemba 2023, p.650。出典は Ziemba and Hausch 1984, 1987 の書籍)。

$$\mathrm{Ex\,Place}_i = 0.319 + 0.559\,\frac{w_i/W}{p_i/P},\qquad \mathrm{Ex\,Show}_i = 0.543 + 0.369\,\frac{w_i/W}{s_i/S}$$

$w_i/W$ はその馬の単勝シェア、$p_i/P$・$s_i/S$ は place・show のシェア。期待値が 1 を十分超えるときだけ賭ける。後年、最良の競馬場の良いレースでは 1.10、それ以外では 1.14 や 1.18 を閾値に勧めている (Ziemba 2023, p.654)。Sauer の要約では、締切前の最後の2分で単勝シェア / place（show）シェア の比が 1.15 以上の馬に賭ける規則 (Sauer 1998, p.27)。これらの閾値や式が 1981 年の論文そのものにあるかは未確認（1985 年の続編や書籍での形の可能性がある）。

## データと結果（二次資料から）

| 項目 | 内容 | 出典 |
|---|---|---|
| データ1 | Santa Anita、1973–74 冬季、627 レース | Ali 1998, p.8 |
| データ2 | Exhibition Park（バンクーバー）、1978 夏季、1,065 レース | Ali 1998, p.8 |
| 単勝 | 本命の過小評価・大穴の過大評価（FLB）はあるが、利益が出るほど大きくない | 要旨 |
| place/show | 大きな正の利益が出るシステムがあり、弱度の非効率を示す | 要旨 |

収益率の具体的な値は未確認。要旨は、利益が偶然でなく非効率を正しく見つけた結果であることを示すモデルも作った、と述べる。

### 追試

- Seligman (1985) が Belmont Park で2週間試したところ、108 レースで 33 回賭けて回収率は −6.7% (Sauer 1998, p.27)。
- Lo ほか (1994) は、Meadowlands（1984、705 レース）、香港（1981–82、905 レース）、日本（1990–91、983 レース）に適用し、いずれも負の利益だった (Ali 1998, p.8)。
- Ziemba 自身も、香港では2着・3着のバイアスが米国と違うため Dr Z システムがうまく働かなかったと書いている (Ziemba 2023, p.654)。Benter が割引 Harville（2着に $q_i^{0.81}$、3着に $q_i^{0.64}$ を正規化して使う）で補正した (p.650)。
- Ritter (1994) は、締切時のプールシェアを使えば事後的に利益が出るが、プールシェアに少しの不確実性を入れると収益率がゼロになることをシミュレーションで示した (Sauer 1998, p.27)。

## 批判的に読む

- **締切時点の情報**: 規則は締切前の最後の数分のプールで判断するが、検証は最終プールを使っている可能性がある（Ritter の批判）。最終オッズで回収率を計算すると楽観的になる。
- **Harville の偏り**: Harville は2着・3着の確率で、本命を過大、穴を過小に評価する偏りがある（Ali 1998 の検証）。米国の place/show では単勝の FLB と打ち消し合うので補正不要とされる (Ziemba 2023, p.650) が、市場によっては打ち消し合わない（香港、日本の追試結果）。
- **公表による消滅**: システムは書籍や電卓チップで広まり、広まれば利益は消えるはず (Sauer 1998, p.27)。
- **標本**: 2つの競馬場・2シーズン。Ali は正の利益が標本の特殊性によるかもしれないと述べる (Ali 1998, p.8)。

## keiba-ai での使い方

- **券種間の値付けの不一致を特徴量にする**: JRA の単勝オッズから Harville（または割引 Harville、Plackett–Luce）で複勝・ワイド・馬連の理論確率を出し、実際の各券種オッズとの比を計算する。仮説: この比が大きい組は回収率が高い。ただし日本での追試（Lo ほか 1994）は負なので、まず控除率と JRA の複勝配当の計算方式（3着内の配当の幅）を入れて再検証する。
- **配当低下を入れた最適化**: 目的関数に自分の賭け金をプールに加えた後の配当を入れる形は、少額でも複勝プール（単勝より小さい）では効く。資金配分モジュールの基本形として実装する。
- **評価時刻**: バックテストでは「判断に使ったオッズ（締切 X 分前）」と「払戻に使う確定オッズ」を分ける。Ritter の指摘どおり、両者を同一視すると利益が過大に出る。
- **閾値の設計**: 期待値 1.10〜1.18 という余裕は、モデル誤差と締切後の変動への安全余裕である。閾値は学習期間で決め、検証期間で評価する。

## 関連ノート

- [Hausch, Ziemba 1985](./1985-hausch-transactions-costs-multiple-wagers.md): 続編。任意の控除率・資金規模、エントリー、複数賭け、容量を扱う。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 2着・3着の確率を出す式。
- [Lo, Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Harville と Henery の比較（偏りの補正）。
- [Ali 1998](./1998-ali-probability-models-outcomes.md): 着順モデルの偏りの検証と、本システムの追試の紹介。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): 本システムと Ritter の批判の要約。
- [Ziemba 2023](./2023-ziemba-parimutuel-revisited.md): 著者自身による後年の回顧（モデル式と近似式の再掲）。
- [Kelly 1956](./1956-kelly-information-rate.md): 対数効用の根拠。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 配当低下を入れた単勝の期待利益最大化。
- [Benter 2019](./2019-benter-model.md): 香港での実践と割引 Harville。
- [MacLean, Thorp, Ziemba 2010](./2010-maclean-kelly-good-bad-properties.md): 本システムで 1984 年 Breeders' Cup Classic に資産の 64% を賭ける解が出た例。

## 検索語

Dr Z システム, ドクターZ, 複勝, 3着内, place, show, 単勝プール, 券種間の値付け, Harville 式, 割引 Harville, 弱度の効率性, 技術的システム, Kelly, 対数効用, マーケットインパクト, 配当低下, 控除率, Exhibition Park, Santa Anita, racetrack betting efficiency, place and show betting, Dr. Z system, Harville formulas, weak-form inefficiency, technical system, Kelly criterion, nonlinear program, market impact, expected return threshold, Ritter, Seligman

---
title: Pari-mutuel betting markets: racetracks and lotteries revisited
authors: Ziemba William T.
year: 2023
venue: Annual Review of Financial Economics 15 641-662
url: https://researchonline.lse.ac.uk/id/eprint/120846/
doi: 10.1146/annurev-financial-053122-021925
topic: market-efficiency
tags: survey, favourite-longshot-bias, syndicates, rebates, market-efficiency, hong-kong
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# パリミュチュエル市場再訪：Dr Z システム、割引 Harville、シンジケートの当事者によるサーベイ

> 一言で: Thaler and Ziemba (1988) から35年後に、同じ著者が競馬と宝くじの市場を振り返る。競馬市場は弱度効率的だが、単勝から他券種を値付けする最適化（Dr Z システム、割引 Harville 式、Kelly 基準）でプロのシンジケートがヘッジファンドのように稼げるようになった、という実務寄りの総説。

原本は LSE Research Online の掲載版 PDF（26ページ）。ページ番号は PDF のページ（雑誌の 641〜662 ページに対応）。学術的なサーベイというより、著者の経験談（コンサルティング、Benter との交流、Pick 6 の保証プール）を多く含む。

## 構成

1. 序論: 金融市場・スポーツ賭けの効率性、控除率とリベート (p.2–5)
2. 繁殖（Breeding）(p.6)
3. Pick 6 とその変種: レインボー Pick 6、プール保証保険 (p.6–7)
4. 賭け戦略: Kelly、平均推定の重要性、FLB、複勝・連勝系の最適化、連勝系の値付け、確率計画、シンジケート (p.7–18)
5. 宝くじ: スポーツくじ、ロトの「全部買い」(p.18–20)
6. 結論と今後の課題 (p.20)

## 主要な論点

### 取引費用とリベート（1節, p.2–3）

- 控除率は競馬で約13〜30%、宝くじで約50% (p.2)。
- リベートの登場で、大口の賭け手の実質控除率は約11〜13%に下がった。例: 単勝の控除15%のうち、リベート業者が5%、賭け手に5%返し、競馬場は5%だけ受け取る。競馬場はリベートの無い一般客から多く取ることで15%を確保する (p.3)。

### 平均（確率）を正しく当てることが最優先（4節, p.7–9）

- 勝つための手順は金融市場と同じで、(1) 正確な確率で平均を正しく推定し、(2) オッズと Kelly 基準などで賭け金を最適化する (p.8)。
- Chopra–Ziemba (1993) を引き、平均・分散・共分散の推定誤差が確実性等価に与える影響は 20:2:1、対数効用のようにリスク回避が小さい場合は 100:3:1 (p.9)。
- ハーフ Kelly はフル Kelly の成長率の75%を保ちつつ、損益分岐を上回る確率を87%から95.4%に上げる (p.8)。ケンタッキーダービー 1934–2005 年の例では、本命を毎回買うと $2,500 が $480 になり、Kelly 系は増える (p.8, Figure 1)。

### FLB（4.2節, p.9–11）

- 1986年と最近の比較で、穴は依然過剰に買われ、1997年以降は本命を買っても利益が出なくなった (p.9, Figure 2a)。
- 歴史的には米国オッズ 3–10（英国式 1.30 以下）の単勝で約3%の利益があり、100–1 の公正オッズは約700–1、つまり $1 あたり約13.7セントの価値しかない (p.10)。
- G1 級（ケンタッキーダービーなど）の高格レースや、Betfair のような取引所では偏りが平ら (p.10)。
- **逆 FLB の市場**として香港と日本を挙げる（Busche and Hall 1988, Busche 1994, Benter）。理由として賭け手のリスク回避、特定の数字の好き嫌い、インサイダー情報の可能性を挙げる (p.10)。
- 説明については Snowberg–Wolfers（誤認説が優位）と Ottaviani–Sørensen のサーベイに委ねている (p.10–11)。

### Dr Z システムと割引 Harville（4.3–4.4節, p.11–14）

- 単勝プールから公正な確率を作り、複勝（place/show）の割安な馬を探す。賭け金は Kelly（期待対数富の最大化）で決め、自分の賭けがオッズを動かす効果も目的関数に入れる (p.11–12)。
- 複勝では「単勝の FLB」と「2・3着の偏り」が打ち消し合うので、補正なしの Harville 式でよい。ただし近似誤差のため、期待値が 1.10（一流競馬場の良いレース）〜1.14・1.18（それ以下）を超えたときだけ賭ける (p.12, p.16)。
- 連勝系では Harville 式は偏るので、**割引 Harville 式**を使う。2着の位置では $q_i^* = q_i^{\alpha} / \sum_j q_j^{\alpha}$（$\alpha \approx 0.81$）、3着では $\alpha^2 \approx 0.64$、4着では $\alpha^3$。値は時期と競馬場で変わる (p.12, p.14)。本命の2・3着確率を下げ、穴の確率を上げる補正。
- Dr Z システムは香港ではうまく働かなかった。偏りの形が違うためで、Benter らが割引 Harville で2着以下の偏りを補正した (p.16)。

### 大量の組合せ馬券の買い方（4.5節, p.14–15）

Kelly 最適化は少数の大きな賭けに集中し、整数制約も扱いにくい。Pick 6/8 のような低確率高配当の馬券では、各レースの馬を I（本命級）・II（有力）・III（穴）に分け、カテゴリの組合せの「スコア」が小さいチケットほど多く買う**チケット木**か、推定誤差の閾値を超える期待値の馬券を全部買って期待値で重み付けする**確率加重**の方法が使われる（香港のシンジケートで普及） (p.8, p.14–15, Table 2)。

### シンジケート（4.6節, p.15–17）

- Benter は 80 以上の要因を持つ2種のモデル（公正オッズを予測するもの、市場オッズを説明変数に入れるもの）を使い、多項プロビット・ロジットで確率を推定した。締切直前の資金流入で最終オッズが動くので、**最終オッズを予測する第2のモデル**も必要 (p.15)。利益は総額で約10億ドル規模 (p.16, Figure 3)。
- 香港が有利だった理由: 特定の数字の好き嫌い、出走頭数が少なく2場だけでほぼ豪州産騸馬、12秒ごと（後に1分ごと）のオッズのデータ配信、市場が深く価格インパクトが小さい、電子投票できる (p.16)。
- 2022年時点でシンジケートは日本や韓国を含む多くの市場で活動している (p.16)。研究と実装の立ち上げには1〜3年と約100万ドルかかり、最大手（豪州）は最大300人を抱える (p.17)。

> While the racing market is weak form efficient, optimization models and various handicapping ideas can be used to create winning strategies. (p.20)

### 宝くじ（5節, p.18–20）

Lotto BC（5/40, 658,008 通り）のように、キャリーオーバーが大きく販売が少ないときは全組合せを買う戦略が正の期待値になる。人気の偏りで 20–40% の組合せは誰も買っていないことが多く、シンジケートの期待収益は 10–25% 程度 (p.19)。

## 批判的に読む

- **体系的なサーベイではない**: 引用の多くが著者自身の本・論文で、検証可能な数値の多くは補足資料や過去の著作に委ねられている。シンジケートの成績や運営コストは著者の伝聞。
- 日本の逆 FLB の根拠として Busche and Hall (1988) を挙げているが、同論文の主対象は香港で、日本は Busche (1994) が扱う（[Snowberg and Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md) の脚注の整理が正確）。また JRA の三連単では大穴の過剰人気が強い（[小幡・太宰 2014](./2014-obata-horse-racing-prospect-theory.md)）ので、「日本は逆 FLB」は券種と時期を限定して読む必要がある。
- 割引 Harville の $\alpha \approx 0.81$ は「典型的なデータ」の値で、推定方法・データは示されていない。
- 期待値の閾値（1.10〜1.18）は Dr Z システムの近似誤差に対する経験則で、統計的な根拠は示されていない。

## keiba-ai での使い方

- **連勝系の確率は割引 Harville から始める**: 単勝確率から馬連・三連単の確率を作る基準モデルとして、$\alpha = 0.81$（2着）、$0.64$（3着）の割引 Harville を実装し、通常の Harville・Plackett–Luce と比べる。JRA のデータで $\alpha$ を推定し直し、競馬場・頭数・芝ダート別に変わるかを確認する。評価は三連単の的中組合せの対数尤度。
- **最終オッズ予測モデル**: Benter 型の運用では「締切時点のオッズ」と「最終オッズ」の差が問題になる。keiba-ai で購入判断の時点を締切数分前に置くなら、最終オッズを予測するモデルを別に持ち、期待値はその予測オッズで計算する。
- **期待値の閾値と賭け金**: 期待値が 1 をわずかに超える程度では推定誤差で負けうる。閾値（例: 1.10 以上）を変えたときの回収率と賭け数のトレードオフをバックテストで評価し、Kelly はフラクショナル（1/2 以下）から始める。
- 平均推定の誤差が支配的という指摘（20:2:1）は、資金配分の工夫より確率モデルの改善を優先する方針の根拠になる。
- 多数の組合せ（三連単・WIN5）を買う場合は、Kelly ではなくチケット木か確率加重で、整数の購入単位に落とす方法を比較する。

## 関連ノート

- [Thaler and Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 本論文が35年後に再訪する元のサーベイ。
- [Hausch et al. 1981](./1981-hausch-racetrack-market-efficiency.md): Dr Z システム（単勝から複勝を値付け）の原論文。
- [Hausch and Ziemba 1985](./1985-hausch-transactions-costs-multiple-wagers.md): 取引費用と複数の賭けの最適化。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 連勝系確率の基本公式。
- [Henery 1981](./1981-henery-permutation-probabilities.md), [Stern 1990](./1990-stern-gamma-permutations.md), [Lo and Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md): Harville の偏りを補正する代替モデル。本文で割引 Harville の文脈で言及。
- [Benter 2019](./2019-benter-model.md): 香港シンジケートのモデル。本論文の 4.6 節の主役。
- [Bolton and Chapman 1986](./1986-bolton-conditional-logit.md), [Chapman 1994](./1994-chapman-hong-kong-2000-races.md): 要因モデルの先駆として紹介。
- [Kelly 1956](./1956-kelly-information-rate.md), [MacLean et al. 2010](./2010-maclean-kelly-good-bad-properties.md), [MacLean et al. 1992](./1992-maclean-growth-versus-security.md): Kelly とフラクショナル Kelly。
- [Snowberg and Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): FLB の図（Figure 2b）の出典。
- [Busche and Hall 1988](./1988-busche-exception-risk-preference.md): 香港の逆 FLB。
- [Ashiya 2015](./2015-ashiya-lock-arbitrage.md): 日本の lock（裁定）。本文の arbitrage/locks の日本版。

## 検索語

パリミュチュエル, pari-mutuel, parimutuel, 競馬市場の効率性, market efficiency, 弱度効率性, weak form efficiency, 本命穴馬バイアス, favorite-longshot bias, FLB, 逆FLB, reverse bias, 香港, Hong Kong, 日本, Dr Z システム, Dr Z system, 複勝, place and show, 割引 Harville, discounted Harville, Harville 公式, Kelly 基準, フラクショナル Kelly, fractional Kelly, 期待対数富, 確率計画, stochastic programming, シンジケート, syndicate, Benter, リベート, rebate, 控除率, takeout, track take, Pick 6, レインボー Pick 6, プール保証, キャリーオーバー, carryover, ロト, lotto, buying the pot, チケット木, 確率加重, Ziemba

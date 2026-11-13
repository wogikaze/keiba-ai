---
title: Pricing Exotic Racetrack Wagers
authors: Hausch Donald B., Lo Victor S. Y., Ziemba William T.
year: 1994
venue: Efficiency of Racetrack Betting Markets (Hausch, Lo, Ziemba eds.), Academic Press 1994; World Scientific 2008 edition pp. 469-483
url: https://econpapers.repec.org/bookchap/wsiwschap/9789812819192_5f0047.htm
doi: 10.1142/9789812819192_0047
topic: probability-models
tags: exotic-bets, pricing, harville-formula, favourite-longshot-bias, kelly-criterion, quinella, hong-kong, discount-model
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# 単勝オッズから連勝式馬券を価格付けし、Kelly 基準で賭ける：香港の馬連 369 レースでの試算

> 原本は書籍『Efficiency of Racetrack Betting Markets』2008年版 pp.469-483 の抽出テキスト（pdfcoffee.com、OCR 由来で数式と表が崩れている）。ページは書籍のページ。式の細部は崩れた箇所を他の章・関連ノートで補って読んでおり、その箇所は明記する。

> 一言で: 単勝の票数（必要なら本命-大穴バイアスを補正）から勝率を作り、Harville 式か Lo & Bacon-Shone の割引モデルで着順確率を出し、馬単・3連単・馬連・ダブルの「期待値が閾値を超える1点」に Kelly 基準で賭ける、という実務的な手順の提案。検証は香港 1989 年の馬連 369 レースだけで、資金 1 万ドルが Harville 版で 10.95 万ドル、近似 Henery 版で 6.82 万ドルになったと報告する (p.481)。

## 原本で確認・訂正したこと

旧ノートは要旨（RePEc）と孫引きに基づいていた。原本を読んで次の点が変わった。

- **検証データが分かった**。香港の馬連（quinella）369 レース、1989 年、控除率 17% (p.480-481, Figure 7)。旧ノートでは「未確認」だった。
- **本命-大穴バイアスの補正は、実際の検証では使っていない**。香港の単勝市場にはバイアスがない（Busche & Hall 1988 など）ので、単勝の票数シェアをそのまま勝率にした (p.481)。要旨が強調する補正式 (1) と Table 2 は北米向けの道具として紹介されるだけである。
- **「小さなデータで Harville が良かった」の孫引きは正しい**。ただし理由は著者自身が書いている。利益の大半は2つの組み合わせ（レース 172 と 280）から来ていて、どちらも圧倒的な本命が絡んでいた。Harville 式は本命の着順確率を過大評価するので本命に多く賭け、それが当たっただけ、という説明である (p.481)。モデルの優劣の証拠にはならない。
- **書誌**: 2008年版は p.469 から始まり、参考文献は p.483 まで (p.469, p.483)。同じ書籍の他章を「In this volume, 221-231」（Lo 1994）のように引いており (p.483)、これは 2008 年版の目次（Lo の章は p.237）と合わない。1994 年版のページのまま再録されたと考えられる（推測）。1994 年版での本章のページは未確認。

## 構成

1. 序論：競馬場は先物市場に似た金融市場で、連勝式はレバレッジの高いオプションに相当する。ただし取引コストが高い (p.469)。
2. 単勝市場の効率性：先行研究のまとめと、バイアスの補正式 (pp.470-476)。
3. 連勝式の価格付け：着順確率モデル（Harville / Henery / Stern / 割引モデル）と Kelly 基準 (pp.477-480)。
4. 香港の馬連での検証 (pp.480-481)。
5. 結論：フラクショナル Kelly を推す (p.482)。

## 単勝市場：本命-大穴バイアスとその補正

- Snyder (1978) がまとめた6研究（Fabricand, Griffith, McGlothlin, Seligman, Weitzman, Snyder 自身）、1947–1975 年の 35,285 レースで、オッズ帯別の回収率に本命-大穴バイアスが出る (p.471, Figure 1, Table 1)。英国の 1950・1965・1973 年の平地競走（ブックメーカー）でも形は同じで、極端な本命は正の期待値、最長のオッズは極めて低い期待値 (p.472, Figure 2)。
- バイアスはあっても控除率を超えない。例外は 3-10（勝率およそ 70%）以下の極端な本命だけで、そこから利益が出始める (p.470, p.475, Figure 6)。こうした馬は稀なので、実用上は弱度効率的と見なせる、と著者は言う (p.470)。
- 補正式 (1) は、オッズ $O_i$ の馬の勝率 $r_i$ を、払戻率 $Q$（1 − 控除率）とオッズ帯ごとの補正値 $D_i$ から $r_i = (Q + D_i)/(O_i + 1)$ の形で出す (p.475)。式は OCR で崩れており、この形は Table 2 の数値と整合するように読んだもの。
- Table 2（Ziemba & Hausch 1986 が出典）はオッズ帯ごとの「実効払戻率（breakage 控除後）」で、カリフォルニア（控除率 15.33%）とニューヨーク（17%）を並べる (p.474)。抜粋すると次のとおり（単位は賭け金 1 ドルあたりのセント、$D$ はパーセント・ポイント）。

| 単勝オッズ | カリフォルニア | ニューヨーク | 補正 $D$ |
|---|---|---|---|
| 1-20 | 104.5 | 104.0 | +20.8 |
| 1-1 | 91.9 | 90.2 | +8.2 |
| 2-1 | 89.8 | 88.1 | +6.1 |
| 9-2 | 83.7 | 82.0 | 0.0 |
| 5-1 | 82.5 | 80.8 | −1.2 |
| 10-1 | 77.5 | 75.8 | −6.2 |
| 20-1 | 68.5 | 66.8 | −15.2 |
| 50-1 | 40.0 | 38.3 | −43.7 |
| 100-1 | 13.7 | 12.0 | −70.0 |

  9-2 が損益分岐（補正 0）で、breakage はさらに約 1% の手数料に相当する (p.474, 表注)。OCR で列の並びが崩れており、列の割り当ては数値の整合から推定した。

## 着順確率モデル

- **Harville (1973)**: $\pi_{ij} = \pi_i \pi_j / (1-\pi_i)$、$\pi_{ijk} = \pi_i \pi_j \pi_k / [(1-\pi_i)(1-\pi_i-\pi_j)]$ (p.477, 式 (2)(3))。Dansie (1983) により、走破時間が独立な指数分布に従うことと同値 (p.477)。
- **Henery (1981)**: 走破時間を独立な正規分布 $N(\theta_i, 1)$ とする。単調変換で順位確率は変わらないので、対数正規でも同じ (p.477)。$\theta_i$ は勝率に合うよう連立非線形方程式を解いて求め、閉じた形はない。
- **Stern (1990)**: 形状母数 $r$ を固定したガンマ分布。$r=1$ が Harville。Stern は小さなデータで $r=2$ が良いとした (p.477)。
- 比較の結論：Bacon-Shone, Lo & Busche (1992b) は米国・香港で Henery が最良、Lo (1994) は日本で Stern の $r=4$ が最良。「普遍的なモデルはないが、すべての証拠が Harville から離れる方向を指す」(p.477)。
- **割引モデル（Lo & Bacon-Shone 1993）**: Henery・Stern は数値積分が重いので、勝率のべき乗で割り引く近似式 (4)(5) を使う。パラメータ $\lambda$（2着用）と $\tau$（3着用）は $r$ ごとに Table 3 で与えられ、$r=\infty$（Henery 近似）では $\lambda = 0.76$、$\tau = 0.62$ (p.478, Table 3)。式 (4)(5) は OCR で読めないので、形は [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md) のノートを参照。米国ではこの値で「かなりうまく働く」(p.479)。
- Harville の2着確率の偏りは本命-大穴バイアスと逆向きなので、複勝（1・2着）確率では打ち消し合う傾向がある。ただし十分ではなく、Benter (1994) の変換も代替として挙げる (p.475)。

## 賭け方：閾値つきの1点 Kelly

手順 (pp.479-480):

1. 長距離砲は良い賭けがほとんどないので、単勝 8-1 以下の馬だけに絞る。
2. 自分の賭けでオッズが動かない（プールが十分大きい）と仮定し、1つの組み合わせだけに賭ける。
3. 2 ドル券の期待収益は $2(O+1)p - 2$（式 (6)）。$O$ はその組み合わせのオッズ（1 ドルあたりの純利益）、$p$ は推定的中確率。
4. 優位幅 $E$ を決め、$2(O+1)p \ge 2(1+E)$ を満たす組み合わせだけを候補にする（式 (7)）。候補の中から的中確率 $p$ が最も高いものを選ぶ。
5. 賭け金の割合は Kelly 基準 $f = [p(O+1) - 1]/O$（式 (9)）。
6. 馬単・3連単・馬連・ダブルの $p$ は Table 4 の式で着順確率から作る。馬連なら $\pi_{ij} + \pi_{ji}$、ダブルは2レースの勝率の積 (p.480, Table 4)。

自分の賭けがプールに対して大きいときは式 (9) の賭け金は大きすぎる。Smith & Ziemba の経験則は「プールの x% を賭けたら賭け金を x% 減らす」(p.480, 脚注)。

## 検証：香港の馬連 369 レース

| 項目 | 内容 |
|---|---|
| 市場 | 香港、馬連（quinella）。香港で最大のプール、オッズは大型画面に表示 (p.480) |
| 期間・規模 | 1989 年、馬連データが揃う 369 レース (p.480, Figure 7) |
| 控除率 | 17% (p.480) |
| 勝率 | 単勝票数シェアをそのまま使用（香港には FLB がないため補正なし）(p.481) |
| 着順確率 | Harville と近似 Henery（割引モデル）の両方 (p.481) |
| 絞り込み | 単勝 8-1 以下、優位幅 15% (p.481) |
| 初期資金 | 1 万米ドル (p.481) |
| 最終資金 | Harville 109,532 ドル、近似 Henery 68,217 ドル (p.481) |
| 比較 | ランダムに同額を賭けると、総賭け金 251,455 ドルに控除率 17% がかかり −32,747 ドル（実際には 0 で破産）(p.481) |

> The Harville model does somewhat better in this case, but this analysis is not based on a large sample. (p.481)

利益の大半はレース 172 と 280 の2つの的中から来ており、どちらも極端な本命が絡む (p.481)。

結論では、Kelly 基準は的中確率が小さい3連単などで賭け割合が大きくなりすぎることがあり、損失からの回復に時間がかかると認める。対策として、Kelly の賭け金に一定の割合を掛けるフラクショナル Kelly（MacLean & Ziemba 1991; MacLean, Ziemba & Blazenko 1992）と、優位幅 $E$ を上げることを挙げる (p.482)。

## 批判的に読む

- **サンプルが極めて小さい**。369 レースで、利益の大半が2レースに集中している。資金推移は2回の的中でほぼ決まっており、統計的な有意性の評価はない。著者も「大きな標本ではない」と認めている (p.481)。
- **オッズの時点が不明**。使った馬連オッズが確定オッズか、賭ける時点で見えるオッズかの記述は見当たらない（未確認）。確定オッズで閾値を判定していれば、実際には使えない情報で賭けたことになる（リーク）。
- **自分の賭けの影響を無視**。資金が 10 倍になる過程で賭け金がプールに対して小さいままとは限らない。Smith & Ziemba の補正は紹介されるが、検証で使ったとは書かれていない (p.480-481)。
- **ランダム賭けの基準線は控除率だけの直線**。モデルの価値を示すには、同じ絞り込み（8-1 以下）で単純に人気上位を買う戦略などとの比較が要る。
- **補正式と検証の不一致**。要旨は FLB 補正を売りにしているが、検証市場ではそれを使っていない。補正の効果は本章では検証されていない。
- **Harville が勝った理由は偶然に近い**。本命を過大評価する偏りが、たまたま本命の的中2回と重なった。モデル選択の根拠にしてはいけない。

## keiba-ai での使い方

- **理論オッズの作り方の基準線**: 単勝オッズ → 勝率 → 着順確率（Harville と割引モデル $\lambda=0.76, \tau=0.62$ の両方）→ 馬連・馬単・ワイド・3連複・3連単の理論確率、をまず作る。JRA の確定オッズと理論確率の比を券種・人気帯別に集計する。
- **仮説 1**: JRA の馬連でも、Harville は本命絡みの組み合わせの確率を過大評価する。割引モデルの方が着順確率の log loss が小さい（[Lo 1994](./1994-lo-running-time-japan.md) の日本の結果と同じ向き）。
- **仮説 2**: 式 (7) の閾値つき1点 Kelly を JRA の馬連に当てると、時系列で分けたテスト期間では回収率が控除率込みで 100% を超えない。超えたとしても少数の本命的中に依存する。評価では的中回数・最大ドローダウン・上位 k 的中を除いた回収率を必ず併記する。
- **賭ける時点のオッズを使う**。確定オッズではなく締切前のオッズで閾値判定し、確定オッズで払戻を計算する。本章の手順をそのまま確定オッズで再現するとリークになる。
- **控除率**: JRA の控除率は券種で違う（単勝・複勝 20%、馬連・ワイド 22.5%、3連単 27.5% など）。理論オッズ・期待値はその券種の控除率で計算する。
- **賭け金**: Kelly は本章でも結論でフラクショナル化を勧めている。実験ではフル Kelly と 1/2・1/4 Kelly を並べる。

## 関連ノート

- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 式 (2)(3) の出典。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規走破時間モデル。
- [Stern 1990](./1990-stern-gamma-permutations.md): ガンマ走破時間モデル。
- [Lo & Bacon-Shone 2008](./2008-lo-ordering-probabilities-approximation.md): 割引モデル（式 (4)(5)）の原典の系譜。
- [Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md), [Lo 1994](./1994-lo-running-time-japan.md): モデル比較。本章が引く「Henery/Stern が Harville より良い」の根拠。
- [Lo, Bacon-Shone & Busche 1995](./1995-lo-ranking-probability-betting.md): 割引モデルを複勝・3着内の賭けに使った研究（本章では「forthcoming」として引用）。
- [Hausch, Ziemba & Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 単勝から複勝・3着内を価格付けし Kelly で賭けた原型。本章はこれを連勝式に広げた。
- [Hausch & Ziemba 1985](./1985-hausch-transactions-costs-multiple-wagers.md): 取引コストと複数の賭け。
- [Snyder 1978](./1978-snyder-efficient-markets-horse-racing.md): Figure 1・Table 1 の出典。
- [Ali 1977](./1977-ali-probability-utility-estimates.md): Figure 3 の集計に使われたデータの1つ。
- [Busche & Hall 1988](./1988-busche-exception-risk-preference.md): 香港に FLB がないことの根拠。検証で補正を省いた理由。
- [Kelly 1956](./1956-kelly-information-rate.md), [MacLean ら 1992](./1992-maclean-growth-versus-security.md): Kelly 基準とフラクショナル Kelly。
- [Benter 2019](./2019-benter-model.md): 本章が Harville の偏りの補正として挙げる Benter (1994) の変換。
- [小幡・太宰 2012](./2012-obata-prospect-theory-trifecta.md): 日本の3連単市場の分析。
- [Deza ら 2017](./2017-deza-exotic-wagering-losses.md): 連勝式の損失管理。

## 検索語

連勝式, エキゾチック馬券, exotic wager, 馬単, exacta, exactor, 3連単, trifecta, triactor, 馬連, quinella, ダブル, daily double, 価格付け, pricing, 理論オッズ, fair odds, 弱度効率性, weak-form efficiency, 本命-大穴バイアス, favourite-longshot bias, FLB 補正, 実効払戻率, effective track payback, breakage, Harville, Henery, Stern, 割引モデル, discount model, Lo Bacon-Shone 近似, 走破時間分布, running time distribution, Kelly 基準, Kelly criterion, フラクショナル Kelly, fractional Kelly, 優位幅, edge, 香港, Hong Kong, 1989, 369 レース, Dr. Z, Hausch Lo Ziemba

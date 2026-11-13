---
title: Influence of Track Surface Condition on Racing Times of Thoroughbred Racehorses in Flat Races
authors: Maeda Yousuke, Tomioka Michiko, Hanada Michiko, Oikawa Masa-aki
year: 2012
venue: Journal of Equine Veterinary Science 32(11) 689-695
url: https://www.sciencedirect.com/science/article/abs/pii/S0737080612000883
doi: 10.1016/j.jevs.2012.02.012
topic: evaluation-and-features
tags: track-condition, going, turf, dirt, racing-time, jra, fracture, track-variant
verified: abstract
importance: medium
source: unavailable
---

# JRA の馬場状態は、競馬場と距離の違いを除いても走破タイムに効き、その効果は芝よりダートで大きい

> 一言で: JRA 10 場・2000–2004年の平地 16,765 レース（延べ 183,465 頭）で、競馬場と距離の影響を取り除いても馬場状態（芝: 良・稍重・重・不良、ダート: 同）は走破タイムに有意に影響し、影響はダートのほうが芝より大きかった。競走中の骨折と馬場状態の関係を調べる研究の一部。

**原本未取得**。J Equine Vet Sci（Elsevier）の有料論文で、無料の著者稿は見つからなかった（ResearchGate はログインが必要なため使っていない）。本ノートは、出版社ページの要旨と、同じ著者らの OA 総説 Maeda, Hanada & Oikawa (2016) "Epidemiology of racing injuries in Thoroughbred racehorses with special reference to bone fractures: Japanese experience from the 1980s to 2000s", J Equine Sci 27(3):81–97（PMC5048355）の該当節に基づく。以下「総説」と書いたものは 2016 年の総説の節名。本論文の表・係数・図は未確認。

## 背景

JRA では競走中の骨折の発生率が馬場状態で変わることが知られていた。総説によれば、ダートでは馬場が悪化する（良→不良）ほど骨折の発生率が上がり（傾向の検定 $P<0.001$）、芝では馬場が悪化するほど下がる傾向があった（$P=0.0711$, 有意でない）（総説「Relationship between Incidence of Fractures … and Track Condition」）。走破タイムは馬場の硬さや速さの指標になるので、馬場状態とタイムの関係を競馬場・距離の違いから切り離して定量化するのが本論文の目的（要旨）。

## データ（要旨・総説「Relationship between Racetrack Surface Condition and Racing Times in Flat Races」）

- JRA の **10 競馬場**、**2000–2004年**の平地競走。
- **16,765 レース、延べ 183,465 頭**（芝 99,803、ダート 83,662）。
- 馬場状態は JRA の4区分。芝は良 (Firm)・稍重 (Good)・重 (Yielding)・不良 (Soft)、ダートは良 (Fast)・稍重 (Good)・重 (Muddy)・不良 (Sloppy)（総説「Track Surface Condition as Defined by the JRA」）。
- 分析方法（モデルの形、走破タイムを勝ち馬のタイムで見たか全馬で見たか、競馬場・距離の扱い）は未確認。要旨は「競馬場と距離の違いによる効果から切り離して」分析したとする。

## 結果（要旨・総説）

- 芝・ダートとも、馬場状態は走破タイムに有意に影響した。
- 馬場状態の効果は**ダートのほうが芝より大きい**。
- 競馬場もタイムに有意に影響した。
- 競馬場と距離の効果を除いても、馬場状態がタイムに影響することは確定的だった。
- 走破タイムが骨折の発生に影響するかどうかは今後の課題として残された。

### 参考：総説に載っている馬場状態別の平均タイム（別データ）

総説の Table 2–3 は Oikawa & Kusunose (2005) からの転載で、1990–1994年の中山・京都の平均タイム。本論文のデータではないが、方向の目安になる（総説の表からの読み取り）。

| 競馬場・コース | 良 | 不良 | 差 |
|---|---|---|---|
| 中山 芝 1200 m | 70.8 秒 | 73.6 秒 | 約 +2.8 秒 |
| 京都 芝 2000 m | 123.9 秒 | 127.1 秒 | 約 +3.2 秒 |
| 中山 ダート 1200 m | 75.1 秒（良） | 74.1 秒（不良）、重 73.8 秒 | 単調でない |
| 京都 ダート 1800 m | 115.2 秒（良） | 114.7 秒（不良）、重 113.6 秒 | 単調でない |

芝は馬場が悪くなるほど遅くなる。ダートは良より重・不良のほうが速いことがあり、水分を含んだダートが締まって速くなるという通説と整合する。本論文で「ダートの効果が大きい」とされたのが、遅くなる方向か速くなる方向かは原本未確認。

## 批判的に読む

- 原本を読めていないので、効果の大きさ（何秒・何%）と、馬の能力の違い（重馬場で出走を取り消す馬、重馬場が得意な馬）をどう扱ったかは不明。
- 馬場状態の4区分は粗い。同じ「良」でも含水率やクッション値で速さは大きく違う。本論文は含水率やクッション値（JRA が後に公表を始めた連続値の指標。公表開始時期は未確認）を使っていない。
- 馬場状態と骨折の関係は、総説自身が「決定的な証拠はない」としている。

## keiba-ai での使い方

- **タイム系特徴量は「競馬場 × コース × 距離 × 馬場状態」で補正する**: 本論文の結論は、走破タイム・上がり3F・スピード指数を作るときに、競馬場と距離に加えて馬場状態の補正が必要ということ。最も単純には、同じ日・同じコースのレースの平均との差（日ごとのトラックバリアント）を使えば、馬場状態の4区分より細かい当日の馬場差を吸収できる。
- **ダートは単調でない前提で扱う**: ダートの馬場状態は「悪いほど遅い」とは限らない。馬場状態を順序変数（0〜3）として線形に入れず、カテゴリとして入れるか、勾配ブースティングに任せる。
- **馬場適性の特徴量**: 馬場状態の効果がレースごとに大きいなら、馬ごとの「重・不良での成績 − 良での成績」が予測に効くはず。仮説: ダートの重・不良のレースでは、過去の重・不良での成績（または父の産駒の重・不良成績）の重要度が上がる。ただし重・不良の出走回数は少ないので、馬単位では縮小推定（父系で平均に寄せる）を使う。
- **含水率・クッション値**: 公表されている期間では、4区分の代わりに連続値の含水率・クッション値を使う。期間をまたぐ学習では、欠損として扱える形にする。

## 関連ノート

- [Oki 1984](./1984-oki-turf-dirt-running-time.md): 日本の芝・ダートの走破タイムの要因分析。馬場の効果を扱う先行研究。
- [Oki 1995](./1995-oki-jockey-racing-time.md): 走破タイムの要因（騎手）。同じく混合モデルによるタイムの分解。
- [Legg 2025](./2025-legg-turf-track-condition-speed-injury.md): 芝の馬場状態と速度・故障の関係。本論文と同じ問い（馬場・速さ・故障）の後続。
- [Lee 2011](./2011-lee-carried-weight-body-weight-ratio.md): 韓国の走破タイムを、同一競走群（同じ日・同じレース）の固定効果で馬場差ごと吸収して分析した例。
- [Gramm 2010](./2010-gramm-age-racing-performance.md): 当日の馬場の速さで補正した指数（Beyer）を使う研究。

## 検索語

馬場状態, 良馬場, 稍重, 重馬場, 不良馬場, 芝, ダート, 走破タイム, 馬場差, トラックバリアント, 含水率, クッション値, 骨折, 競走中の故障, JRA, 競馬場の違い, 距離補正, track condition, going, track surface condition, firm, good, yielding, soft, fast, muddy, sloppy, turf, dirt, racing time, track variant, moisture content, cushion value, racing fracture, injury, Japan Racing Association, Journal of Equine Veterinary Science

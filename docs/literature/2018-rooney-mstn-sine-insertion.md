---
title: The "speed gene" effect of myostatin arises in Thoroughbred horses due to a promoter proximal SINE insertion
authors: Rooney Mary F., Hill Emmeline W., Kelly Vincent P., Porter Richard K.
year: 2018
venue: PLoS ONE 13(10) e0205664
url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0205664
doi: 10.1371/journal.pone.0205664
topic: evaluation-and-features
tags: mstn, myostatin, genetics, sine-insertion, distance-aptitude
verified: fulltext
importance: low
source: downloaded
source_version: published
---

# MSTN「スピード遺伝子」の機能的な原因は SNP ではなくプロモーター近傍の SINE 挿入

> 一言で: サラブレッド 145 頭で MSTN の SNP g.66493737C>T と 227 bp の SINE 挿入は 100% 一致していた。培養筋芽細胞でのレポーター実験で両者を切り離すと、ミオスタチン産生を約 4.5 分の 1 に下げるのは SINE 挿入だけで、SNP には効果が無かった。SINE 挿入は転写開始点を挿入配列の中へずらす。距離適性マーカーとして C/T SNP を使う根拠（連鎖が完全だから）を分子レベルで補強した論文で、競走成績のデータは扱っていない。

PLoS ONE の公開版（CC BY）20 ページを読んだ。

## 背景

- ミオスタチン（MSTN）は骨格筋の成長を抑える TGFβ ファミリーのタンパク質。馬では距離適性に最も影響する単一遺伝子とされる (p.2)。
- 先行研究（Hill ら 2010）は、最適距離で分けた馬（≤1,600 m の短距離 / >1,600 m の中長距離）で第 1 イントロンの SNP g.66493737C>T が強く関連し、CC は短距離、CT は中距離、TT は長距離向きと報告した (p.2)。
- その後、エクソン 1 の上流に 227 bp の SINE（ERE-1）挿入が見つかり、これも距離と強く関連した。二つの多型は 1,589 塩基離れていて、高い連鎖不平衡にある (p.2)。
- T 型が祖先型で、C 型は比較的新しく、20 世紀初頭に短距離志向とスピード重視の選抜で頻度が上がった。SINE 挿入は C 型の背景上で生じた (p.2)。
- 商業的には SNP が距離適性の予測に広く使われているが、機能的な裏付けは無かった (p.3)。

## 方法と結果

| 実験 | 対象 | 結果 |
|---|---|---|
| 遺伝型の一致 | サラブレッド 145 頭（同一調教師の厩舎） | CC=II 49 頭、CT=IN 54 頭、TT=NN 42 頭。不一致 0 (p.8, Table 1) |
| 筋生検の MSTN mRNA | 未調教の 2 歳前後（21±3 か月）81 頭（CC/II 36, CT/IN 34, TT/NN 11）、中臀筋 | TT/NN が CT/IN（P≤0.01）、CC/II（P≤0.05）より有意に高い。CC/II と CT/IN の差は無し (p.8, Fig.1) |
| ルシフェラーゼレポーター | マウス C2C12 筋芽細胞に 4 種の構築物（SINE 有無 × SNP の C/T） | SINE 挿入で 72 時間後のルシフェラーゼ（＝ミオスタチンの代理）産生が 4.5 倍減少（P≤0.001）。48 時間で有意差。SNP は効果なし（P>0.05） (p.9, Fig.3) |
| 構築物由来 mRNA | 同上 | SINE 挿入で有意に減少（P≤0.05）、SNP は影響なし (p.9) |
| 転写開始点の予測 | Softberry TSSW、BDGP NNPP | SINE 無しでは +1（ヒト・ウシと同じ位置）、SINE 有りでは −226 と予測 (p.10–12, Fig.4) |
| 転写開始点の実測（5' RACE） | 中臀筋の RNA、CC/II と TT/NN | SINE 無し：+1（クローンの 85%）と +30。SINE 有り：−226 と −185（いずれも挿入配列の中）で、+1 は観察されず。転写産物は約 200 塩基長い (p.13, Fig.5) |

著者のまとめ：SINE 挿入が転写開始点を移し、転写と産生を下げる。SNP は機能を持たないが、SINE と完全に連鎖しているので距離適性の予測マーカーとしては妥当 (p.13–15)。

先行研究で報告された SNP と SINE の不一致については、PCR での対立遺伝子の脱落（allelic dropout）による技術的な差と推測している (p.13)。

## 批判的に読む

- **競走成績との関連は検証していない**。本論文が示すのは遺伝型と遺伝子発現・転写開始点の関係で、「距離適性」との関連は先行研究からの引用。
- **標本はアイルランドの 1 厩舎**。145 頭で完全一致でも、日本の集団で同じ連鎖が成り立つかは別問題（著者も頻度は地域で異なると述べる, p.2）。
- 筋生検での差は TT/NN の 11 頭との比較で、CC/II と CT/IN に差が無い。ヘテロでも効果がほぼ飽和しているのか、標本の少なさか、本文からは判断できない。
- レポーター実験はマウス由来の細胞株で、生体の筋での 4.5 倍という効果量にそのまま対応するわけではない。
- **利益相反**：共著者 Hill は MSTN 検査を商業化した Plusvital 社の最高科学責任者で、関連特許の発明者 (p.2)。結論（SNP マーカーの妥当性）は同社の商品の根拠を補強する方向にある。研究自体に同社は関与していないと明記されている。

## keiba-ai での使い方

- **個体の遺伝型は通常は入手できない**ので、特徴量として直接は使えない。間接的な使い道は次のとおり。
- **血統からの距離適性の代理**：父馬の MSTN 型が公表されている場合（種牡馬の検査結果を公表する例がある）、父の型から産駒の C/T の期待頻度を計算できる。ただし公開範囲は限られ、未確認。現実的には「父馬の産駒の平均勝ち距離」「父の現役時の距離」を、MSTN を含む遺伝的距離適性の代理として使う。
- **特徴量設計の根拠**：距離適性が少数の大効果遺伝子に支配されるなら、「父の距離適性 × 今回の距離」の交互作用が効くはず。距離変更（前走より延長 / 短縮）の効果が血統で異なる、という仮説の背景になる。
- **実験案（仮説）**：父馬ごとの産駒平均勝ち距離を特徴量に入れ、今回の距離との差の絶対値が大きい馬ほど着順の残差が悪化するかを確認する。MSTN の効果が大きいなら、この交互作用は芝の短距離〜中距離の境界（1,600 m 前後）で特に効く。

## 関連ノート

- [Hill 2010](./2010-hill-mstn-sprinting-stamina.md)：C/T SNP と最適距離の関連を示した研究。本論文はその SNP の機能的な裏付けを与える（Hill は本論文の共著者）。
- [Tozaki 2010](./2010-tozaki-gwas-racing-performance-mstn.md)：日本のサラブレッドでの GWAS と MSTN。本論文の結論が日本の集団に当てはまるかを考えるときの手がかり。
- [Oda 2024](./2024-oda-predictability-mixed-effects.md)：JRA のデータで遺伝的効果（父の効果）を含む混合モデルによる予測可能性。遺伝情報を予測に使う統計側の研究。
- [Takahashi 2015](./2015-takahashi-age-racing-speed.md)：JRA の距離別平均速度。距離ごとの基準の作り方。

## 検索語

ミオスタチン、MSTN、スピード遺伝子、speed gene、SINE 挿入、SINE insertion、ERE-1、転移因子、transposable element、SNP、g.66493737C>T、C/T 型、CC 型、CT 型、TT 型、距離適性、distance aptitude、最適距離、best race distance、短距離、長距離、スプリンター、ステイヤー、転写開始点、transcription start site、TSS、5' RACE、ルシフェラーゼ、レポーター遺伝子、C2C12、筋生検、連鎖不平衡、linkage disequilibrium、遺伝子検査、Plusvital、Equinome

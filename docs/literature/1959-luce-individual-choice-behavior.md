---
title: Individual Choice Behavior: A Theoretical Analysis
authors: Luce R. Duncan
year: 1959
venue: New York: Wiley / London: Chapman & Hall (book, xii+153 p.)
url: https://search.worldcat.org/title/190041
doi:
topic: probability-models
tags: luce-choice-axiom, plackett-luce, choice-model, iia, ranking-postulate
verified: fulltext
importance: medium
source: downloaded
source_version: published
---

# Luce の選択公理：Plackett-Luce と多項ロジットの理論的な出発点

> 一言で: 「集合 $T$ から $R$ が選ばれる確率は、まず $S$ を選び、その中から $R$ を選ぶ確率の積に等しい」という選択公理（Axiom 1）を置くと、各選択肢に比率尺度の重み $v(x)$ が存在して選択確率が $v(x)/\sum_{y\in S}v(y)$ になることを示した心理学の理論書。順位づけを「最上位を選び、残りから次を選ぶ」と繰り返す **順位づけの公準（ranking postulate）** もここで提案され、後に Plackett (1975) が着順モデルとして一般化した。

原本は 1959 年 Wiley 版の全体スキャン（Digital Library of India の写しが Internet Archive にある `dli.scoerat.3346ndividualchoicebehavior`、167 枚）を取得し、機械 OCR した。以下のページは本の印刷ページ番号（PDF の枚番号は印刷ページ + 13）。OCR に崩れた行があり、数式の一部は前後から読み取った。

## 原本で確かめた点（旧ノートとの違い）

旧ノートは原本未取得で、Hunter (2004) などの引用に基づいていた。原本を読んで次を確認・補足した。

- 公理の主張は旧ノートの記述どおり。ただし本書の Axiom 1 には **第 ii 部（完全に識別される選択肢の扱い）** があり、旧ノートの式はその第 i 部だけだった (p.6)。
- 「無関係な選択肢からの独立性（IIA）」との関係は、本書では Lemma 3 として **比 $P_S(x)/P_S(y)$ が $S$ によらない** と述べられ、著者自身が Arrow の IIA の確率版と位置づけている (p.9)。旧ノートの「計量経済学でいう IIA」の説明は正しい。
- **着順（順位づけ）のモデルは本書第2章 F 節にある** (pp.68-74)。旧ノートは Plackett-Luce を後続論文から再構成していたが、原本に「最上位を決め、残りで次を決める」公準が明示されている。さらに **上から順位づけるか下から順位づけるかで確率が一般に一致しない** という定理（Theorem 8）がある。競馬の Harville 式との関係で重要（後述）。
- 本書は競馬の実証を含まない（旧ノートの推測どおり）。序文で「新しいデータは示さない理論書」と明言している (p.vii)。

## 本書の構成 (pp.ix-xii)

1. 基本理論（Axiom 1、比率尺度の存在、独立単位条件、代数的近似）
2. 心理物理学への応用（Fechner の問題、べき法則、Thurstone Case V との関係、信号検出、順位づけ）
3. 効用理論への応用（不確実な選択肢＝賭けの選択）
4. 学習理論への応用
5. まとめと結論、付録4つ

## 選択公理 (Axiom 1, p.6)

$U$ を選択肢の全体、$T$ を有限部分集合、$P_T(R)$ を「$T$ から選ぶとき $R\subset T$ のどれかが選ばれる確率」、$P(x,y)$ を2択で $x$ を選ぶ確率とする。

- **(i)** すべての組で $P(x,y)\ne 0,1$（識別が不完全）なら、$R\subset S\subset T$ について $P_T(R)=P_S(R)\,P_T(S)$。
- **(ii)** ある $x,y$ で $P(x,y)=0$ なら、$x$ は $T$ から取り除いてよい：$P_T(S)=P_{T-\{x\}}(S-\{x\})$。

著者の解釈: 単純な決定なら、選択肢をいったん大分類してから選んでも結果は変わらない、という仮定 (p.7)。逆に「本当に多段階の判断が要る複雑な決定」には成り立たないと期待すべき、と著者自身が限定を付けている (p.7)。

(ii) を置く理由は、(i) を完全識別のときにも無制限に適用すると「1組が完全に識別されれば、第3の選択肢もどちらかと完全に識別される」という不自然な帰結が出るため (pp.17-19)。

### 主要な帰結

| 結果 | 内容 | 頁 |
| --- | --- | --- |
| Lemma 2 | (i) は $P_S(R)=P_T(R\mid S)$（部分集合での選択＝全体での条件付き確率）と同値 | p.7 |
| Lemma 3 | $P_S(x)/P_S(y)=P(x,y)/P(y,x)$ が $S$ によらない（IIA の確率版） | p.9 |
| Theorem 1 | 多肢選択の確率はすべて2択の確率から決まる：$1/P_T(x)=\sum_{y\in T}P(y,x)/P(x,y)$ | p.16 |
| Theorem 2 | 3つ組で $P(x,y)P(y,z)P(z,x)=P(x,z)P(z,y)P(y,x)$（循環する非推移の確率が両向きで等しい） | p.16 |
| Theorem 3 | 正の関数 $v$ が定数倍を除き一意に存在し、$P_S(x)=v(x)/\sum_{y\in S}v(y)$ | p.23 |

Theorem 3 の $v$ が競馬モデルでいう馬の「強さ」で、$v=\exp(\text{スコア})$ とおけば多項ロジット（レース内 softmax）になる。

### 経験的な検証について

著者は、Lemma 3 を直接検定するには選択肢ごとに数百〜数千回の観測が要ると試算している（標準偏差を比の 10% にするには $\mu_x=0.5$ で 400 回、5% なら 1,600 回）(p.14, Table 1)。当時公刊された直接の検証は Clarke (1957) の音声の聞き取り混同データだけで、6×6 の混同行列から 3×3 の場合を予測して散布図が 45 度線に乗る、という程度の支持である (pp.14-15)。また、公理は個体ごとの選択について述べたもので、個体が公理を満たしても集団平均では満たさない例を示している (p.8)。

## Thurstone Case V との近さ (pp.55-56)

公理から得られる2択の確率はロジスティック関数で、Thurstone の Case V（正規分布の差）とは論理的に別物。ただし $P(x,y)$ と $P(y,z)$ から $P(x,z)$ を予測すると、両者の差は最大でも 0.02 未満 (p.56, Table 3)。著者は、両者の選択は便利さと帰結の広さで決めるべきで、0 と 1 の確率を明示的に扱える点が公理の利点だとする。

競馬に置き換えると、Harville（Luce 型）と Henery（正規走破時間）の勝率の差は2頭の比較では小さく、違いは多頭数・下位着順で出る、という後の実証（Lo 1994 など）と整合する見方。

## 順位づけのモデル（第2章 F 節, pp.68-74）

### 上からの順位づけと下からの順位づけ

3つの選択肢の順位 $x>y>z$ の確率を、

- 上から: $R(x>y>z)=P_T(x)\,P(y,z)$（最上位を選び、残りから上位を選ぶ）
- 下から: $R^*(x>y>z)=P^*_T(z)\,P^*(y,x)$（最下位を選び、残りから下位を選ぶ）

とする。両方が公理を満たし $P^*(x,y)=P(y,x)$ でも、**両者が一致するのは $P(x,y)=P(y,z)$ のときだけ** (Theorem 8, p.69)。つまり順位づけの向きによって確率が変わる。著者は「多くの人は上から順位づける」という印象に触れ、順位データの解釈には注意が要ると述べる (p.70)。

### 順位づけの公準 (p.72)

$$R_T(x>\rho)=P_T(x)\,R_{T-\{x\}}(\rho)$$

（$\rho$ は残りの順位）。これを繰り返すと $\prod_k v(x_k)/\sum_{l\ge k}v(x_l)$ になり、Plackett-Luce モデル・Harville 式と同じ形になる。Theorem 9 は、この公準と公理の下では「順位データで $x$ が $y$ より上だった割合」が $P(x,y)$ の正しい推定になることを示す (p.72)。公準がなければこの素朴な推定は正当化されず、反例のモデルでは推定値が 1.00 と 0.60 のように大きく食い違う (pp.71-72, Table 4)。

さらに、相関のない「弁別の散らばり」（独立な確率変数の大小で順位が決まる、走破時間モデルと同じ考え方）でも3つの場合は同じ推定が成り立つが、4つ以上では両モデルの形式的な一致は崩れる (pp.73-74)。

## 批判的に読む（競馬への含意）

- **IIA は2・3着争いで崩れうる**: Harville 式は順位づけの公準を着順に当てはめたもの。実データでは人気馬の2・3着確率が過大になる（Ali 1998、Benter 1994、Lo and Bacon-Shone 1994）。本書の Theorem 8 は「上からと下からで確率が違う」ことを示しており、着順の生成過程（ゴール前の決着の仕方）の仮定が結果を左右することを早くから指摘していると読める（競馬への解釈は本ノートの推論）。
- **似た選択肢の問題**: IIA は似た選択肢が同時にあると不自然な予測をする（後年の「赤バス・青バス」問題）。本書は公理を「単純な決定」に限定しており (p.7)、展開に左右される競馬の着順がそれに当たるかは疑わしい。
- **集団平均の問題**: 本書の公理は個人の選択についてで、集団平均では崩れうる (p.8)。単勝の票数シェアは多数の賭け手の集計なので、市場確率に公理を当てはめること自体が近似である。
- **検証のサンプルサイズ**: 公理の直接検定には大きな標本が要る (p.14)。競馬では同じ組み合わせの馬が繰り返し対戦しないので直接検定はできず、着順の尤度比較など間接的な方法になる。

## keiba-ai での使い方

- **モデル設計の前提を明示する**: レース内 softmax で勝率を出し、Harville で連勝式の確率を作るパイプラインは、Theorem 3 と順位づけの公準を両方使っている。どちらで崩れているかを分けて検証する。
- **実験案（仮説）**: 「同じ softmax のスコアでも、2着・3着を選ぶ段階では温度を上げる（$v^{\alpha}$, $\alpha<1$）方が着順の対数尤度が高い」。段階ごとの温度 $\alpha_2,\alpha_3$ を時系列分割の学習期間で推定し、検証期間で 1 から有意に離れるかを見る。
- **上から・下からの順位づけ**: Theorem 8 に倣い、着順の尤度を「上から」（Plackett-Luce）と「下から」（逆順の Plackett-Luce）で比べる。下位着順の情報を学習に使うときの向きの選択の根拠にする。
- **相関のある馬**: 同厩舎・同馬主の複数出走、同じ脚質の馬が多いレースで Harville の誤差が大きいかを層別に調べる。

## 関連ノート

- [Plackett 1975](./1975-plackett-analysis-of-permutations.md): 順位づけの公準を着順モデルとして一般化した。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 公準を競馬の着順確率に当てはめた式。
- [Hunter 2004](./2004-hunter-mm-bradley-terry.md): 公理と Plackett-Luce の同値性の整理と MM 推定法。
- [Guiver & Snelson 2009](./2009-guiver-bayesian-plackett-luce.md): Plackett-Luce のベイズ推定と Gumbel 解釈。
- [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md): 公理に基づく多項ロジットを競馬に使った。
- [Henery 1981](./1981-henery-permutation-probabilities.md): 正規走破時間（Thurstone 型）の代替。本書 2.D の比較の競馬版。
- [Stern 1990](./1990-stern-gamma-permutations.md): gamma 走破時間で Luce と Thurstone をつなぐ族。
- [Lo 2008](./2008-lo-probability-statistical-models-racing.md): Harville（Luce 型）と Henery の実データ比較のまとめ。
- [Cotton 2021](./2021-cotton-relative-ability-winning-probability.md): 能力と勝率の関係のモデル。Luce の公理を Harville の言い換えとして扱う。

## 検索語

Luce の選択公理, Luce's choice axiom, 選択公理, choice axiom, Axiom 1, IIA, 無関係な選択肢からの独立性, independence from irrelevant alternatives, 比率尺度, ratio scale, Bradley-Terry-Luce, BTL, Plackett-Luce, 順位づけの公準, ranking postulate, 上からの順位づけ, 下からの順位づけ, direction of ranking, Thurstone Case V, ロジスティック, 多項ロジット, multinomial logit, 条件付きロジット, softmax, 離散選択, discrete choice, 心理物理学, 効用, constant-ratio rule, Individual Choice Behavior

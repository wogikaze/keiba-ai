---
title: Noise, Information, and the Favorite-Longshot Bias in Parimutuel Predictions
authors: Ottaviani Marco, Sørensen Peter Norman
year: 2010
venue: American Economic Journal: Microeconomics 2(1) 58-85
url: https://www.aeaweb.org/articles?id=10.1257/mic.2.1.58
doi: 10.1257/mic.2.1.58
topic: market-efficiency
tags: favourite-longshot-bias, private-information, noise-traders, parimutuel, theory
verified: fulltext
importance: high
source: downloaded
source_version: working-paper
---

# 私的情報とノイズの比で FLB の向きが決まる：パリミュチュエル市場の均衡モデル

> 一言で: 賭け手が他人の最終的な賭けを見ずに同時に賭けると、確定オッズは「情報」と「ノイズ」の混ざった標本になる。情報がノイズより多ければ本命が過小評価される通常の FLB、ノイズが多ければ逆 FLB が均衡として生じる。

取得した原本は Copenhagen 大学 Finance Research Unit のワーキングペーパー No. 2006/04（2006年5月版、36ページ）である。AEJ: Micro 掲載版（2010）とは図番号・命題番号・細部が異なる可能性がある。以下のページ番号は WP の PDF ページ。

## 要旨

FLB（本命は確定オッズが示すより勝ちやすく、穴馬は勝ちにくい）を、リスク愛好や確率の誤認ではなく、**私的情報を持つリスク中立の賭け手の均衡**から導いた理論論文である。鍵は、賭け手が締切直前に同時に賭けるため、自分以外の賭けの分布（=最終オッズ）を知らずに賭けることにある (p.4)。最終オッズに含まれる情報を観察者がベイズ更新すると、市場確率と事後確率がずれる。ずれの向きは「私的情報の量」と「ノイズの量」の相対比で決まる (p.2 Abstract)。

## モデル

- 結果 $k \in \lbrace 1,\dots,K\rbrace $（単勝なら勝ち馬、馬単なら $K = L(L-1)$）。$N$ 人の賭け手が共通事前 $q_k$ を持ち、各自が私的シグナル $s_i$ から事後信念 $p_i$ を得る (p.7)。
- 各賭け手は 1 単位を 1 つの結果に賭けるか棄権する。リスク中立で、期待金銭収益に加えて一定の娯楽効用 $u \ge 0$ を得る。娯楽効用が無いと no-trade 定理で誰も賭けない (p.7, 脚注14)。
- 控除率 $\tau$。結果 $k$ が当たると 1 単位あたり $(1-\tau)\sum_l b_l / b_k$ が払い戻される。市場確率は $\pi_k = b_k / \sum_l b_l$ (p.7)。
- 命題1: 臨界値 $u^*(N) \in (\tau, 1)$ があり、$u \ge u^*$ なら全員参加、$\tau < u < u^*$ なら一部棄権、$u \le \tau$ なら全員棄権 (p.8)。

### 中心の式

対称モデル（$q_k = 1/K$）では各自が事後確率最大の結果に賭けるのが均衡で（命題2, p.11）、真の結果に賭ける確率 $\eta(k|k)$ は他の結果に賭ける確率 $\eta(k|l)$ より大きい。$n$ 票が $k$ に入ったとき、観察者の事後確率は

$$\beta_k = \frac{\eta(k|k)^n (1-\eta(k|k))^{N-n}}{\eta(k|k)^n (1-\eta(k|k))^{N-n} + (K-1)\,\eta(k|l)^n (1-\eta(k|l))^{N-n}}$$

で、市場確率は $\pi_k = n/N$ (p.12, 式(1))。賭け票は二項分布に従う「標本」であり、$\beta_k$ と $\pi_k$ の差が FLB である。

命題3: 中立点 $\pi^*$（事後が事前に等しくなる票の割合、式(2)）より市場確率が低い穴馬は過大評価、高い本命は過小評価される。これは $N$ が十分大きいとき必ず成り立つ (p.13)。命題4: $K=2$ で情報の精度 $\eta(k|k)/\eta(k|l)$ が十分高いとき同じ結論になる (p.13)。$\pi_1 = 1/2$ の点で FLB が出る条件は $2 < N \log[\eta(k|k)/\eta(k|l)]$（p.13, 脚注20）。

## 数値例で見る直観（2頭・正答率 2/3・控除なし, p.9–10）

| 賭け手数 $N$ | 票の分布 | 市場確率 | 事後確率 | 判定 |
|---|---|---|---|---|
| 2 | 1 に 2 票 | 1 | 4/5 | 逆 FLB（本命の期待収益 −1/5） |
| 3 | 1 に 2 票 | 2/3 | 2/3 | 偏りなし |
| 4 | 1 に 3 票 | 3/4 | 4/5 | FLB |
| $\infty$ | — | 2/3 または 1/3 | 1 または 0 | 極端な FLB |

賭け手が少ないと票の偏りは偶然（ノイズ）で生じやすく、本命は「たまたま票を集めただけ」の可能性が高い。賭け手が増えると票の偏りが情報を反映し、事後確率は市場確率より極端になる。

## 拡張と比較静学

- **券種の組合せ数（p.15–16, Figure 3）**: Dirichlet 例（$\theta=1$, $N=4$）で $K=2,10,100$ を比べると、$K$ が賭け手数に比べて大きい（$K=100$）と逆 FLB、$K=10$ で弱い FLB、$K=2$ で強い FLB。$K=100$ では市場確率が事前 0.01 から 0.025 を超えるまで期待収益は正にならない (p.16)。Asch and Quandt (1988) の「エキゾチック券種では FLB が弱い」という観察と整合する、と著者は述べる。
- **ロト（p.17）**: シグナルが無情報なので事後は常に $1/K$。期待収益 $(1-\tau)/(\pi K) - 1$ は $\pi$ について減少し、逆 FLB が必ず生じる。
- **事前の非対称（4.1節, p.18–22）**: 事前の本命がいると、他人がそちらに賭けると予想して事前の穴馬に賭ける「逆張りインセンティブ」が生じ、$N$ が大きいほど強まる（Figure 4）。中間の市場確率では「票の少ない事前本命（負の収益）」と「票の多い事前穴馬（正の収益）」が混ざるので、期待収益曲線が平らになる（Figure 5, $N=10$, $q_1=0.22$）。
- **共通誤差（4.2節, p.22）**: 無限個のシグナルでも解消できないレースの偶然性 $\sigma$ を入れると、本命側の期待収益曲線が平らになる。Snowberg and Wolfers の「中間は平ら、極端な本命と極端な穴で偏る」形に近づくと主張。
- **棄権（5.1節, p.23–24）**: 娯楽効用が下がる（控除率が上がる）と情報の乏しい賭け手から抜けるため、票に占める情報の割合が上がり FLB が強まる（命題8）。
- **分割可能な賭け（5.2節）**: 複数の結果に賭けられるとノイズが減り FLB が強まる。

> In the limit, as we approach no trade, information dominates noise and the FLB unambiguously results. (p.6)

## 他の説明との比較（6節, p.25–27）

Griffith の確率誤認、Isaacs の独占的情報者、Weitzman のリスク愛好、Ali の信念の異質性、Hurley–McDonough の控除率による裁定の限界、の5説と比べる。本論文の利点として、(1) 逆 FLB も同じ枠組みで出る、(2) 賭け手が少ない市場や組合せ数の多い券種で FLB が弱まる、(3) 締切直前の賭けほど情報を含む（Asch et al. 1982）、(4) 中間が平らな期待収益曲線、を挙げる。平坦部分はリスク愛好や確率加重でも出せるが、かなり特殊な選好形が要る、と指摘する (p.26 脚注33)。

## 批判的に読む

- **実証は無い。** 期待収益曲線の形は数値例で Snowberg–Wolfers の図に「定性的に似る」ことを示すだけで、パラメータの推定や検定はしていない。結論でも検定は今後の課題としている (p.27)。
- 「同時に賭ける」仮定は、締切直前に大量の票が入るという事実に依拠する (p.4)。日本の JRA のように締切後もオッズ確定まで票が流入する市場の構造とどこまで一致するかは未確認。
- 賭け金は 1 単位・分割不可の仮定が基本で、大口の情報者が金額を調整する状況（Isaacs 型）は別論文に回している。
- 掲載版との差分は未確認（WP 版を読んだ）。

## keiba-ai での使い方

- **市場確率の補正の形を決める**: 本論文によれば、市場確率から事後確率への写像は単調だが非線形で、その曲がり方は「市場の厚さ（賭け手数・売上）」と「券種の組合せ数」に依存する。仮説: 売上の小さいレース（ローカル平場、新馬）や組合せ数の多い券種（三連単）ほど FLB が弱いか逆転する。実験では、単勝オッズ由来の確率をロジスティック補正するとき、補正係数を売上規模の分位で層別し、Brier/対数損失の改善が層ごとに違うかを見る。
- **特徴量**: 「市場確率 × 売上規模」「市場確率 × 頭数（$K$）」の交互作用。本論文のモデルでは $N$ と $K$ が FLB の強さを決めるので、オッズを入力に使うモデルではこれらの交互作用を入れる根拠になる。
- **締切直前のオッズ変化**: 最終オッズには直前の情報が集約されるという含意は、[Hanyu et al. 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md) の「最終オッズで十分か」の実証と対応する。時系列オッズを取る場合、最終オッズとの差分を特徴量にする根拠になる。
- 回収率を券種別に評価するとき、FLB が券種で逆転しうることを前提に、券種ごとに別の補正を学習する。

## 関連ノート

- [Ali 1977](./1977-ali-probability-utility-estimates.md): 信念の異質性による FLB。本論文は私的情報で置き換えた説明として対比する。
- [Griffith 1949](./1949-griffith-odds-adjustments.md): 確率誤認説。本論文が比較する代替説明の最初のもの。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 情報を持つ大口賭け手の最適賭け。代替説明の一つ。
- [Asch et al. 1982](./1982-asch-racetrack-informed-behavior.md): 締切直前の賭けが情報を含むという実証。本論文の同時手番の根拠。
- [Crafts 1985](./1985-crafts-insider-knowledge-britain.md): 私的情報（インサイダー）の存在の証拠として引用。
- [Shin 1991](./1991-shin-optimal-betting-odds-insiders.md): 固定オッズ市場での情報ベースの FLB。パリミュチュエルとの違いを議論。
- [Snowberg and Wolfers 2010](./2010-snowberg-flb-risk-love-misperceptions.md): 本論文が再現を目指した期待収益曲線の実証。結論は誤認説を支持しており対立。
- [Gandhi and Serrano-Padial 2015](./2015-gandhi-belief-heterogeneity-longshot.md): 信念の異質性モデルの構造推定。異質性説の後継。
- [Hanyu et al. 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 締切直前の票の情報量を JRA データで検証。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): FLB 研究のサーベイ。
- [Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 日本語の FLB 説明サーベイ。

## 検索語

本命穴馬バイアス, 本命-大穴バイアス, ロングショットバイアス, 逆FLB, reverse favorite-longshot bias, favourite-longshot bias, FLB, 私的情報, private information, ノイズ, noise, パリミュチュエル, parimutuel, 同時手番ゲーム, Bayes-Nash equilibrium, ベイズ・ナッシュ均衡, 情報集約, information aggregation, 市場確率と事後確率, Dirichlet, ロト, Lotto, エキゾチック券種, exotic bets, 棄権, abstention, 娯楽効用, recreational value, 逆張り, contrarian betting, Ottaviani Sørensen

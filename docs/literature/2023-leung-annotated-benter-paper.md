---
title: Revisiting the Algorithm that Changed Horse Race Betting
authors: Timothy Leung, Philip Leung (Acta Machina)
year: 2023
venue: 個人ブログ（Acta Machina）
url: https://actamachina.com/posts/annotated-benter-paper
topic: practitioner
tags: grey-literature, benter, hong-kong, hkjc, pseudo-r2, calibration, harville-correction, pytorch, public-odds, replication
verified: fulltext
importance: high
source: downloaded
source_version: web
---

# Benter 論文の注釈つき再現：香港の公式オッズ 40 年分で「大衆の確率」の精度と Harville 補正係数を測り直す

> 一言で: Benter (1994) の本文に Python/PyTorch のコードと注釈を挟み、香港ジョッキークラブ（HKJC）の確定単勝オッズ約 34 万頭分から「大衆の確率」の校正表・疑似 $R^2$・2〜4 着の補正係数を 4 つの 10 年区間で計算し直した。大衆の疑似 $R^2$ は 0.1325（1986–93）から 0.1863（2016–23）へ上がり続けており、同じモデルで勝てる余地は年々狭くなっていることを数字で示した。

## 位置づけ

本文の大部分は Benter 論文の転載で、著者の独自部分は引用ブロックの注釈とコードである。著者らは基礎モデル（ファンダメンタル要因の条件付きロジット）と結合モデルを実際には作っていない。手元の HKJC 確定オッズから作れる「大衆の推定」だけを使い、論文中の表や手順のうち再現できる部分を再現している。論文自体の内容は [Benter 1994](./2019-benter-model.md) のノートにあるので、このノートは再現で新たに出た数値とコードの設計を中心に書く。

## データ

- HKJC の過去の単勝オッズと着順。表示は「337003 rows × 2 columns」（列は `place`, `win_odds`。インデックスは日付・競馬場・レース番号・馬名）。
- 入手経路は書かれていない（「Hong Kong Jockey Club's historical win odds」とだけある）。
- 区間は 4 つ: 1986-08〜1993-08（Benter の元データと同じ時期）、1996–2003、2006–2013、2016–2023。レース数はそれぞれ 3,377 / 4,534 / 5,261 / 5,757、出走頭数は 34,745 / 58,272 / 65,992 / 70,071（「Table B〜E」の脚注）。
- Benter の Table 1 は 3,198 レースだが、著者らの 1986–93 区間は 179 レース多い。著者らは理由が分からないと書いている。

## 手法

1. **大衆の確率**: `1/win_odds` をレース内で合計 1 に正規化する（控除率ぶんのオーバーラウンドを比例配分で除く）。
2. **校正表の再生成**: Benter の Table 1 と同じ確率帯（0–0.01, …, >0.4）で、予測平均と実際の勝率、Z 値を出す関数を書いて 4 区間に適用した。HTML から抽出したテキストには表の数値が入っていない（画像か JS 描画とみられる）。そのため、校正表の具体的な値はこのノートには書けない。
3. **疑似 $R^2$**: 勝ち馬の対数確率の総和 $L$ と、一様ランダム（1/頭数）の対数尤度 $L_0$ から $1 - L/L_0$ を計算する PyTorch 関数を実装した。同着は乱数ノイズで崩している。
4. **結合モデルの実装例**: 基礎モデルを線形層（バイアスなし）＋log-softmax、大衆を `log p` とし、$\alpha \cdot$ 基礎 $+ \beta \cdot$ 大衆 を softmax する `CombinedModel` を Lightning モジュールとして示した。学習は 1 着から 4 着までの Harville 尤度（`harville_loss`）で行う。
5. **2〜4 着の補正係数**: Benter の $\gamma, \delta$ と同じ考え方で、着順ごとに勝率の対数へ掛ける係数（学習可能パラメータ）を置き、Harville 尤度で推定した。各区間の終わりから 1 年後までを検証期間にして early stopping を掛けている。時系列で検証期間を切る形になっている。

## 結果（著者らの再計算）

- **大衆の疑似 $R^2$**（「Assessing the Value of a Handicapping Model」の節の注釈）: 1986–93 が 0.1325、1996–2003 が 0.1437、2006–13 が 0.1668、2016–23 が 0.1863。著者らは「10 年ごとに大衆の推定は良くなっている」とまとめている。
- **着順補正係数**（「First, Second, and Third」の節の注釈。$\gamma$=2 着、$\delta$=3 着、$\varepsilon$=4 着）:
  - 1986–93: 0.83 / 0.68 / 0.58
  - 1996–2003: 0.81 / 0.75 / 0.67
  - 2006–13: 0.88 / 0.73 / 0.67
  - 2016–23: 0.86 / 0.74 / 0.64
  - Benter が論文で報告した値（$\gamma$=0.81, $\delta$=0.65）とほぼ同じ水準で、40 年間を通じて 1 より小さい。2 着・3 着の争いは勝ち馬の争いよりランダム性が強い、という Benter の指摘が今も成り立つことになる。
- **注釈で足された論点**: Benter の多項ロジットの最尤推定は今でいう listwise の Learning-to-Rank に近い。Benter は後に誤差を正規分布とする probit に移った（"Multinomial Probit Models for Competitive Horse Racing"）。距離適性の因子は後の論文で「tack points」（人工データ点）を足した制約付き二次回帰に発展し、データが 3 走未満でも解ける正則化になっている。Kelly については CX Wong の *Precision* 第 7 章を引き、「最大の優位がある 1 頭だけに賭ける」のは誤解で、1 レース内の期待値プラスの馬すべてに配分すべきだとしている。

## 批判的に読む

- **大衆の確率だけの再現である**。基礎モデルの $\Delta R^2$、つまり「大衆に何を足せたか」は再現していない。年代ごとの $\Delta R^2$ の変化は分からない。
- 疑似 $R^2$ の上昇は「大衆が賢くなった」とも読めるが、頭数の構成（香港は 14 頭立てが中心）、オッズ表示の丸め、計算機による大口投票者の参入でも上がりうる。区間ごとに分解はしていない。
- 確定オッズを使っているので、「投票時点で見えるオッズ」との差（締切直前の変動）は扱っていない。Benter 自身は、プール規模が大きくオッズが安定していることを香港を選んだ理由に挙げている。
- 係数の推定は区間内の学習と翌 1 年の検証で行っている。テスト区間を別に取った報告ではない。
- 表の数値が HTML から取れていないので、校正表の再現度（Z 値の大きさなど）はこのノートでは確かめられていない。

## keiba-ai での使い方

- **ベースラインの物差し**: JRA の確定単勝オッズから大衆確率を作り、年ごとの疑似 $R^2$ を出す。HKJC の 0.13→0.19 と比べれば、日本の単勝市場がどれだけ効率的か、どの年に変化したかが分かる。評価コードの最初の実装として軽い。
- **$\Delta R^2$ を主指標の候補にする**: 自作モデルの評価で、単独の logloss/AUC ではなく「大衆＋モデル」の結合ロジットでの疑似 $R^2$ の増分を記録する。主指標を変えるなら ADR が要る。
- **着順補正係数の推定**: JRA データで $\gamma, \delta, \varepsilon$ を同じ手順（Harville 尤度、学習可能な係数）で推定し、馬連・三連系の確率計算に使う。`harville_loss` の設計（同着を乱数で崩す、4 着までで打ち切り）はそのまま参考になる。
- **未評価馬の扱い**: Benter の「新馬など評価できない馬には大衆確率をそのまま与え、他を再正規化する」という手順は、新馬戦・海外馬の欠損処理の方針に使える。

## 関連ノート

- [Benter 1994](./2019-benter-model.md) — 注釈の対象になった原論文。
- [Bolton & Chapman 1986](./1986-bolton-conditional-logit.md) — 多項ロジットと疑似 $R^2$ の出典。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md)、[Henery 1981](./1981-henery-permutation-probabilities.md)、[Lo & Bacon-Shone 1994](./1994-lo-comparison-harville-henery.md) — 着順確率とその偏りの補正。
- [Torné ほか 2021](./2021-torne-hong-kong-softmax-nn.md) — 香港データを softmax NN で扱う学術側の研究。
- [Dhital ほか 2018（NYCDSA）](./2018-dhital-nycdsa-hkjc-neural-net.md)、[Sankari ほか 2019（NYCDSA）](./2019-sankari-nycdsa-hkjc-kelly.md) — 同じ香港市場で Benter の追試を試みた実践記録。
- [Kelly 1956](./1956-kelly-information-rate.md) — 賭け金の配分。

## 検索語

Benter 再現, 注釈つき Benter 論文, 香港 単勝オッズ 疑似決定係数, 大衆の確率 校正, Harville 補正 係数 推定, annotated Benter paper, public estimate pseudo R-squared, HKJC historical win odds, Harville loss PyTorch, place adjustment factors gamma delta

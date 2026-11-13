---
title: A New Interpretation of Information Rate
authors: Kelly J. L. Jr.
year: 1956
venue: Bell System Technical Journal 35(4) 917-926
url: https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1956.tb03809.x
doi: 10.1002/j.1538-7305.1956.tb03809.x
topic: betting-strategy
tags: kelly, log-utility, information-theory, horse-race, parimutuel, track-take
verified: fulltext
importance: high
source: downloaded
source_version: published
---

# 情報レートの新しい解釈：Kelly 基準の原典と「控除がある場合」の賭け方アルゴリズム

> 一言で: 繰り返し再投資する賭け手が資本の指数成長率 $G$ を最大化すると、最適な賭け比率は「自分の事後確率」そのものになり、その最大成長率は Shannon の情報伝送レートに等しい。控除（track take）がある場合は、期待値 $p\alpha$ の大きい順に馬を足していく閉形式の手順を与えた。

原本は AT&T の許諾で再掲された出版版の PDF（10ページ、BSTJ の頁番号 917–926）。以下のページ番号は BSTJ の頁番号で書く。

## 問題設定：私設電信を持つ賭け手

Kelly は通信路の「価値」を、任意のコスト関数を持ち込まずに測りたかった (p.917–918)。そこで選んだのが、結果が公になる前に通信路で結果を受け取り、元のオッズのまま賭けられる賭け手という状況である (p.918, "the gambler with a private wire")。

成長率は次で定義される (p.919)。

$$G = \lim_{N\to\infty} \frac{1}{N}\log_2 \frac{V_N}{V_0}$$

$V_N$ は $N$ 回賭けた後の資本、$V_0$ は初期資本。

## 二値の場合：全額賭けは期待値最大だが破産する

誤り確率 $p$、正答確率 $q$ の二値通信路で、毎回全額を賭けると期待資本は $\langle V_N\rangle=(2q)^N V_0$ で最大になる。しかし $N$ が大きいと確率1で破産する (p.919)。毎回資本の割合 $\ell$ を賭けると

$$G = q\log(1+\ell) + p\log(1-\ell)$$

となり、最大化すると $1+\ell=2q$, $1-\ell=2p$、つまり $\ell=q-p$。このとき $G_{\max}=1+p\log p+q\log q=R$（Shannon の伝送レート）になる (p.920)。

Kelly はこれを効用の問題としてではなく、比較の問題として正当化する。

> the one which uses the value ℓ found above will, with probability one, eventually get ahead and stay ahead of one using any other ℓ. (p.920)

## 一般の場合：多肢の結果とオッズ

記号 (p.920): $p(s)$ は結果 $s$ の確率、$q(s|r)$ は受信記号 $r$ を見た後の事後確率、$\alpha_s$ は1ドル賭けの払戻（元本込み）、$a(s|r)$ は $r$ を見た後に $s$ に賭ける資本の割合。

### 控除なし（$\sum 1/\alpha_s = 1$）

パリミュチュエルでは控除を無視すればオッズは「公正」に近づく、と Kelly は述べる (p.921)。控除がなければ打ち消し合う賭けで実質的に資金を手元に残せるので、全額を賭けると仮定して一般性を失わない。成長率は

$$G = \sum_{r,s} p(s,r)\log \alpha_s a(s|r) \quad (1)$$

で、$a(s|r)=q(s|r)$ で最大化される (p.922)。オッズが公正でない場合でも最適解は変わらない。

> the gambler ignores the posted odds in placing his bets! (p.922)

このとき $G_{\max}=H(\alpha)-H(X|Y)$、$H(\alpha)=\sum_s p(s)\log\alpha_s$ (p.922)。情報が無ければ成長率は $H(\alpha)-H(X)$ で、通信路による増分が $R=H(X)-H(X|Y)$ になる (p.923)。公正なオッズからのずれは賭け手に有利に働く (p.923, (b))。

### 控除あり（競馬の実情）

控除があると打ち消し賭けができないので、賭けずに残す割合 $b$ を明示する (p.923)。

$$G = \sum_s p(s)\log[b+\alpha_s a(s)], \quad b+\sum_s a(s)=1 \quad (3)$$

KKT 条件から解が閉形式で出る (p.924–925)。手順は次のとおり。

1. $p(s)\alpha_s$（期待払戻）の大きい順に並べ替える。
2. 上位 $t$ 頭について $p_t=\sum_{s\le t}p(s)$、$\sigma_t=\sum_{s\le t}1/\alpha_s$ とし、$F_t=(1-p_t)/(1-\sigma_t)$ の最小の正の値を $b$ とする。
3. $a(s)=\max\lbrace p(s)-b/\alpha_s,\,0\rbrace $ とする。$a(s)$ の合計は $1-b$。

最大成長率は $G_{\max}=\sum_{s\le t}p(s)\log p(s)\alpha_s+(1-p_t)\log\frac{1-p_t}{1-\sigma_t}$ (p.925)。

この手順の重要な帰結が p.925 にある。すべての $p(s)\alpha_s<1$ なら何も賭けない。しかし最大の $p(s)\alpha_s$ が1を超えるときは、期待値が負（$p(s)\alpha_s<1$）の馬にも賭けることがある。期待値が正の馬だけに賭ける「古典的な賭け手」の基準とは異なる、と Kelly は明記している。

## 結論部の注意

- 対数を最大化する理由は効用関数ではなく、「対数が繰り返しの賭けで加法的で大数の法則が効くから」(p.925–926)。
- 再投資できない場合（毎週1ドルだけ）は期待値最大化が正しい (p.926)。
- 証明したのは、受信記号ごとに時間によらない固定比率で賭ける戦略同士の比較だけである。時間や過去に依存する戦略に対する優越は未証明として残している (p.926)。これは後に Breiman (1961) が扱う。

## 批判的に読む

- 確率 $p(s)$ は真の確率として既知と仮定している。推定誤差がある現実では、推定確率をそのまま代入したフル Kelly は過大に賭ける。これは後続研究（分数 Kelly、パラメータ不確実性）の主題になった。
- 自分の賭けがオッズを動かさない（price taker）ことを暗黙に仮定している。パリミュチュエルでは自分の賭けで $\alpha_s$ が下がる。
- 実データでの検証は無い。純粋な理論論文である。
- 「控除あり」の手順は単勝のような排反な結果の集合に対するもので、複勝・連勝式のように同時に当たる券種には直接は使えない。

## keiba-ai での使い方

- **単勝の資金配分のベースライン**: 上の3ステップ手順はそのまま実装できる。入力はモデルの勝率 $\hat p(s)$ と確定（または直前）オッズ $\alpha_s$ だけ。JRA 単勝の控除率（約20%）では $\sigma_t$ が大きく、賭ける馬が少数に絞られるはずである（仮説）。
- **負の期待値の馬にも賭ける**挙動は、「期待値1超の馬だけ買う」ルールとの比較実験の対象になる。仮説: 推定確率が十分校正されていれば Kelly 手順の対数成長率が上回るが、校正が悪いと逆転する。評価指標は回収率ではなく、レースあたりの平均 $\log(V_{n+1}/V_n)$ を使う。
- **モデルの優位性の指標**: 情報がない場合の成長率が $H(\alpha)-H(X)$ であることから、モデル確率と市場確率の対数損失の差が「市場に対して取れる成長率」の目安になる。校正評価（対数損失）と賭けの評価をつなぐ指標として使える。
- **再投資の有無で目的関数が変わる**: 固定額で回すバックテストなら期待値最大化、資金を複利で回すなら対数成長率。実験設定でどちらを想定するかを明記する。

## 関連ノート

- [Breiman 1961](./1961-breiman-optimal-gambling-systems.md): Kelly が未証明とした「任意の戦略に対する優越」を一般の有利なゲームで証明。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 同時期のパリミュチュエル単勝の最適賭け（期待利益最大化、自分の賭けがオッズを動かす場合）。
- [Thorp 2008](./2008-thorp-kelly-criterion-blackjack-sports.md): Kelly 基準を実務（ブラックジャック、スポーツ、株式）に適用した解説。
- [MacLean, Thorp, Ziemba 2010](./2010-maclean-kelly-good-bad-properties.md): Kelly の長所と短所の整理。
- [MacLean, Ziemba, Blazenko 1992](./1992-maclean-growth-versus-security.md): 分数 Kelly による成長と安全性のトレードオフ。
- [Smoczynski, Tomkins 2010](./2010-smoczynski-explicit-kelly-horse-races.md): 控除ありの単勝 Kelly の明示解（本論文の手順の再導出・拡張）。
- [Whitrow 2007](./2007-whitrow-simultaneous-bets-allocation.md): 多数の同時イベントへの Kelly の拡張。
- [Baker, McHale 2013](./2013-baker-kelly-parameter-uncertainty.md): 確率の推定誤差下での Kelly の縮小。
- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 複勝・3着内への Kelly 型の応用。

## 検索語

Kelly 基準, ケリー基準, ケリー・ベッティング, 対数効用, 対数資産成長, 指数成長率, 情報伝送レート, 相互情報量, Shannon, 私設電信, 控除率, テラ銭, track take, fair odds, 公正オッズ, Kelly criterion, Kelly betting, log-optimal, growth-optimal, exponential rate of growth, information rate, private wire, parimutuel, win bet allocation, proportional betting

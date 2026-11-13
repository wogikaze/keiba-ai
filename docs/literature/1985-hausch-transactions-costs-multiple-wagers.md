---
title: Transactions Costs, Extent of Inefficiencies, Entries and Multiple Wagers in a Racetrack Betting Model
authors: Hausch Donald B., Ziemba William T.
year: 1985
venue: Management Science 31(4) 381-394
url: https://pubsonline.informs.org/doi/10.1287/mnsc.31.4.381
doi: 10.1287/mnsc.31.4.381
topic: betting-strategy
tags: place-show, dr-z-system, takeout, breakage, kelly, market-impact, capacity, coupled-entries
verified: abstract
importance: medium
source: unavailable
source_version:
---

# Dr Z システムの一般化：控除率・ブレーケージ・カップリング・複数賭け・容量

> 原本未取得。INFORMS は購読制で、OpenAlex・Semantic Scholar・ResearchGate に全文が無かった。本ノートは要旨と、原本取得済みの二次資料（Ziemba 2023、Sauer 1998）に基づく。具体的な数値は未確認。

> 一言で: Hausch, Ziemba, Rubinstein (1981) の place/show システムを、任意の競馬場（控除率）と資金規模に広げ、カップリング（同一馬主の複数頭エントリー）と同じ馬への複数の賭けを扱えるようにし、控除率とブレーケージが利益に与える影響と、「いくら賭けると非効率が消えるか（容量）」を調べた続編。

## 要旨に挙がっている6点

1. 任意の競馬場と初期資産への拡張。1981 年版の近似式は特定の競馬場と資金規模向けだった。
2. 複数頭のエントリー（カップリング。1頭分の馬券で複数頭が対象になる）向けの修正。
3. 複数の賭け（同じ馬への place と show の両方など）の許容。
4. 控除率（track take）とブレーケージ（配当の端数切り捨て）が利益に与える影響の分析。
5. このシステムの最近の実績。
6. 非効率の大きさ: 市場が効率的になるまでにいくら賭けられるか。

## 二次資料での扱い

- Ziemba (2023) は、1981 年論文と本論文で「異なる控除率、同じ馬への place と show の複数賭け、何人がシステムを使うと優位が消えるか」を調べたとまとめている (Ziemba 2023, p.649)。
- 競馬場で使える回帰の近似式（単勝シェアと place・show シェアの比から期待値を出す式）について、詳細と追加の機能は本論文にあり、電卓に組み込まれた、とする (Ziemba 2023, p.650)。近似式そのものは [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md) のノートに書いた。
- Thaler and Ziemba (1988) は、取引コストの違い・エントリー・複数賭けの影響を分析し、資金規模と競馬場の売上（handle）ごとの正確な回帰モデルを与えた、と要約している（検索結果の要約による。本ノートでは JEP の原本未確認）。

## 批判的に読む（要旨から言える範囲）

- 「容量」の分析は、自分以外にシステムを使う人がいない（または一定数）という仮定に依存するはずで、システムの公表後に使う人が増えれば容量は減る。Sauer (1998, p.27) は、公表されたシステムは利益を失うはずだと指摘し、Seligman (1985) の Belmont Park での追試（108 レースで 33 回賭けて −6.7%）を紹介している。
- 控除率の感度分析の具体的な値は未確認。米国の払戻率は約 0.82 (Ziemba 2023, p.649)。

## keiba-ai での使い方

- **控除率の違いを明示的に入れる**: JRA は券種ごとに控除率が違う。単勝・複勝と三連単では払戻率が異なるので、同じ「単勝からの値付け」でも券種によって必要な優位が変わる。期待値の閾値を券種別に設定する。
- **ブレーケージ**: JRA の配当は10円単位で切り捨てられる。複勝の本命のように配当が低い（110〜150円）馬券では、切り捨ての影響が相対的に大きい。期待値計算では切り捨て後の配当を使う（Walls and Busche 2003 は日本のブレーケージを扱う）。
- **容量の見積もり**: 自分の賭けをプールに加えた後の期待値が閾値を割る額を、レースごとに計算する。複勝プールは単勝より小さいことが多いので、容量は複勝で先に尽きる（仮説）。
- **同じ馬への複数の券種**: 単勝と複勝を同じ馬に同時に賭けると強く相関する。別々に Kelly を計算せず、同時分布で一つの最適化にする。

## 関連ノート

- [Hausch, Ziemba, Rubinstein 1981](./1981-hausch-racetrack-market-efficiency.md): 本論文が一般化した元のシステム。
- [Ziemba 2023](./2023-ziemba-parimutuel-revisited.md): 著者による回顧。本論文の位置づけ。
- [Thaler, Ziemba 1988](./1988-thaler-parimutuel-anomalies.md): 本論文を含むパリミュチュエル市場の変則性の総説。
- [Walls, Busche 2003](./2003-walls-breakage-turnover-japanese-tracks.md): 日本の競馬場でのブレーケージと売上。
- [Sauer 1998](./1998-sauer-economics-wagering-markets.md): Dr Z システムの追試と公表の効果。
- [Isaacs 1953](./1953-isaacs-optimal-horse-race-bets.md): 自分の賭けによる配当低下と賭け金の上限。

## 検索語

Dr Z システム, 複勝, 3着内, place, show, 控除率, テラ銭, ブレーケージ, 端数切り捨て, カップリング, エントリー, 複数賭け, 容量, 非効率の大きさ, 取引コスト, 回帰近似, Kelly, transactions costs, track take, takeout, breakage, coupled entries, multiple wagers, extent of inefficiency, capacity, betting system calculator, Hausch Ziemba

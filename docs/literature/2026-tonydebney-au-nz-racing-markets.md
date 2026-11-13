---
title: horse-racing-model (quantitative research on AU/NZ thoroughbred racing markets)
authors: tonydebney69-debug
year: 2026
venue: GitHub
url: https://github.com/tonydebney69-debug/horse-racing-model
topic: practitioner
tags: grey-literature, australia, betfair, bsp, market-efficiency, favourite-longshot-bias, price-drift, holdout, negative-result
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# 豪州の Betfair 取引所データで市場の歪みを4方向から探し、どれも残らなかった記録

> 一言で: Betfair が無償公開している豪州・NZ平地競走の取引所データ（2023〜2025年、約56万頭立て・5.7万市場）で、本命・大穴バイアス、締切前の価格の動き（steamer / drifter）、競馬場・距離・時間帯、走破速度の4つを検証した。BSP（Betfair Starting Price）の較正は全オッズ帯で0.2ポイント以内に収まり、価格の動きの効果は年・流動性・頭数で分けると消えた。著者は「市場だけを使う方法には何も残っていない」として打ち切った。

## データ

- Betfair Automation Hub の豪州・NZ平地競走データ（2020年〜、Betfair が自ら公開、正確さの保証なし）。1行は1単勝市場の1頭（「Data」）。
- 列: `WIN_BSP`（取引所の締切時の精算価格）、発走前の最小・最大・加重平均の約定価格と出来高、単勝・複勝の結果、発走予定時刻のオーバーラウンド。
- **市場データだけで、騎手、調教師、斤量、枠、区間タイム、過去走はない**。だから勝ち馬を予測するモデルは作れず、市場そのものに系統的な歪みがあるかを検定する。
- 暦月で分割: 探索用 2023-01〜2025-12（約56.3万頭立て、5.7万市場）、保留用 2026-01〜08（約12.5万頭立て）。**保留用は一度も読んでいない**（探索段階で残った仮説がなかったため）。

## 検証した仮説と結果

「Findings」と「Final summary」より:

1. **本命・大穴バイアス**: オーバーラウンドで調整した暗黙確率を十分位に分けると、暗黙確率と実際の勝率は全範囲で約0.2ポイント以内。均等賭けの ROI は手数料前からすべての帯で負。BSP は締切直前の流動性の高い取引所価格で、バイアスが報告されてきたブックメーカーやトートの価格とは違う、と解釈している。
2. **価格の動き**: 締切に向けて人気になった馬（steamer）と人気を落とした馬（drifter）。BSP 3〜30 の範囲で、drifter を均等に買うと手数料前 +2.7%、steamer は −3.7%、各約7.2万頭立ての5区分で単調な勾配。BSP 6〜10 に絞っても +3.4%〜−4.1%。しかし BSP 6〜15（16.3万頭立て、5.5万市場）で年別に分けると、2023年だけ単調で2024・2025年は勾配なし（2025: −2.6, +3.7, +0.1, −2.5, +4.0）。流動性の三分位、頭数の四分位でも出たり消えたり。市場単位のクラスター・ブートストラップ（1,000回）で差は +5.2 ポイント、95%CI [+0.27, +10.13]。下限がほぼ0で、しかも最も綺麗に見える帯と区分を選んだ後の値なので「保留、確認されず」。
3. **競馬場・距離・時間帯**: 3,000頭立て以上の71場、距離区分、時間帯区分で較正の差は0.00〜0.09ポイント。競馬場別の ROI は +17%〜−25% とばらつくが、2023〜24年の ROI と2025年の ROI の相関は r = 0.06（Murray Bridge は +27% から翌期 −20%）。
4. **走破速度**: Betfair データに時計がないので racing.com から1開催（8レース65頭）を取得し、勝ち時計＋着差（1馬身≈0.2秒）で各馬の時計を推定。当日の最速馬が8レースすべてで勝ち馬になったが、勝ち馬は着差0なので必ず最速と計算される**同語反復**。速度は過去走から将来を予測して初めて意味を持つが、racing.com は過去約11日しか辿れず、Racenet・Punters は robots.txt で自動取得を禁止、Racing and Sports は403。

## 著者が守った規則

- 方法を凍結した後の保留期間で生き残るまで「シグナル」と呼ばない。
- 手数料込みの回収率を必ず出す。
- 仕組み（注文の流れ、情報、名前のある行動バイアス）の説明が要る。「バックテストが好んだ」は仕組みではない。
- 何も残らなかったことも報告すべき結果。

## 批判的に読む

- 市場データだけの検証なので、「市場は効率的」は「市場価格の関数だけでは勝てない」という意味に限られる。馬の能力のモデル（成績・時計）を作る方向は、データの入手の壁で試していない。
- 本命・大穴バイアスの検定は BSP（締切時の取引所価格）に対するもの。日本のパリミュチュエルの確定オッズとは市場の仕組みも参加者も違う。
- 価格の動きの検定で、帯と区分を選んだ後の CI を「事後選択」と自分で割り引いている点は誠実。ただし保留期間で一度も検定していないので、最終的に否定されたわけでもない。

## keiba-ai での使い方

- **探索用と保留用を暦で分け、保留用は方法を凍結するまで読まない**運用を実験ルールに入れる。探索段階で何も残らなければ保留用は使わずに取っておく、という判断も記録する。
- 「締切前のオッズの動き（人気上昇馬・人気下降馬）」は JRA でも時系列オッズで同じ検定ができる。年別・頭数別・売上規模別に分けて勾配が保たれるかを、最初から検定計画に入れる。[Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md) の最終盤の動きの分析と組み合わせる。
- 競馬場別の回収率のばらつきは、期間をまたいだ相関で雑音かどうかを確かめる（r≈0 なら雑音）。条件別の「得意・不得意」を主張する前の必須確認にする。
- 当日の時計と当日の着順は同語反復になる、という例は、特徴量の時点チェックの教材になる。

## 関連ノート

- [Ottaviani 2010](./2010-ottaviani-noise-information-flb.md)、[Snowberg 2010](./2010-snowberg-flb-risk-love-misperceptions.md)、[Ashiya 2010](./2010-ashiya-longshot-bias-survey.md): 本命・大穴バイアスの文献。BSP では出ないという結果と対照的。
- [Franck 2010](./2010-franck-bookmakers-vs-betting-exchange.md): 取引所の価格がブックメーカーより効率的という比較。
- [Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): 締切直前のオッズの動き（JRA）。
- [Terawong 2024](./2024-terawong-xgboost-in-play-betting-exchange.md): Betfair 型取引所のシミュレーション。
- [Walls 2003](./2003-walls-breakage-turnover-japanese-tracks.md): 売上と効率。
- [pranay123 2026](./2026-pranay123-horse-quant-platform.md): 同じく事前の判定規則を持つが合成データのみ。

## 検索語

オーストラリア競馬, ベットフェア, 取引所, 締切時価格, 本命大穴バイアス, オッズの動き, 人気上昇, 保留期間, 市場効率性, 否定的結果, Australian racing, Betfair exchange, BSP, Betfair Starting Price, favourite-longshot bias, steamers, drifters, price drift, market calibration, holdout, cluster bootstrap, market efficiency, negative result, Automation Hub

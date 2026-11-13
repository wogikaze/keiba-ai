---
title: Neural networks mine for gold at the greyhound racetrack
authors: Johansson Ulf, Sönströd Cecilia
year: 2003
venue: Proceedings of the International Joint Conference on Neural Networks (IJCNN 2003) vol.3 1798-1801
url: https://doi.org/10.1109/IJCNN.2003.1223680
doi: 10.1109/IJCNN.2003.1223680
topic: machine-learning
tags: greyhound, neural-network, exotic-bets, quinella, exacta
verified: metadata
importance: low
source: unavailable
source_version: none
---

# 公開データだけで学習したニューラルネットによるグレイハウンド予測（単勝と連勝式）

> 一言で: Chen et al. (1994) の枠組みを入力18変数に広げ、Gulf Greyhound Park の100レースで BPNN を評価した4ページの会議論文。二次資料によれば、単勝は的中率 24.9% で小幅の損失、quiniela と exacta では払戻がプラスだった。

**原本未取得。** IEEE Xplore は有料、OpenAlex・Semantic Scholar では closed、著者が ResearchGate に上げた PDF はログインが必要（アクセス時 403）。Jönköping 大学のリポジトリ（DiVA）にも見当たらなかった。以下は Schumaker & Johnson (2008) の要約（ページは同論文の著者原稿 PDF）に基づく。原本の数値・手順は未確認。

## 何をした論文か（二次資料から）

- 題材: 米テキサス州 La Marque の Gulf Greyhound Park (Schumaker 2008, p.5, p.10)。
- 入力: Chen (1994) の専門家選定10変数を18変数に拡張（変数の中身は未確認）(Schumaker 2008, p.5)。
- モデル: Chen と同様の誤差逆伝播ニューラルネット（BPNN）(Schumaker 2008, p.5)。
- 学習事例: 449件（Chen は 1,600件）(Schumaker 2008, p.10)。
- 評価: 100レース。単勝に加え、quiniela（1・2着を順不同、馬連相当）と exacta（1・2着を順番どおり、馬単相当）を評価 (Schumaker 2008, p.5)。連勝式は犬単位ではなくレース単位で賭ける方式で、Schumaker (2008) はこの賭け方を採用した (p.12)。
- ResearchGate の要旨断片では「公開されているデータだけを使う」ことと、「Win, Quinella, Exacta などいくつかの賭け方を評価する」ことが述べられている。

## 報告された数値（二次資料）

| 券種 | 的中率 | 払戻（100レース） |
|---|---|---|
| 単勝 | 24.9% | −$6.60 |
| quiniela | 8.8% | +$20.30 |
| exacta | 6.1% | +$114.10 |

出典: Schumaker & Johnson (2008), p.5。同論文 p.17 は単勝の効率を「100ベットで −$6.60、1ベット当たり −$0.066」と換算している。

Schumaker & Johnson (2008, p.5) は、Chen より的中率が高いのに払戻が悪い理由として、変数を増やしたことか、学習事例の少なさで穴を拾えなくなったことを挙げている。これは Schumaker の推測であり、原論文の主張かは未確認。

## 批判的に読む（未確認点を含む）

- 評価100レースでは、exacta の +$114.10 は数本の高配当で決まりうる。exacta の 6.1% は100レースで約6本の的中。
- 「払戻」が総額か純損益かは原本で確認できない。Schumaker の換算（効率 = 払戻/ベット数）から見る限り純損益と推測される。
- 学習とテストの分割方法、ハイパーパラメータの選び方（Chen はテストで選んでいた）は未確認。
- 年: IJCNN 2003（米ポートランド、2003年7月）。書誌は Crossref と DBLP（conf/ijcnn/JohanssonS03）で確認。

## keiba-ai での使い方

- **券種ごとに評価する**: 単勝で負けても連勝式で勝つ（あるいはその逆）という報告は、同じ勝率モデルでも券種ごとに回収率を分けて報告する必要を示す。keiba-ai の評価表は単勝・複勝・馬連・馬単・3連系を別列にする。
- **順位情報の質**: 連勝式を当てるには勝率だけでなく2着・3着の確率の質が効く。仮説: 勝率モデルから Harville で作った馬単確率と、2着以内確率を直接学習したモデルとでは、馬単の対数損失が異なる（[Harville 1973](./1973-harville-multi-entry-probabilities.md), [Lo 1994](./1994-lo-comparison-harville-henery.md) と比べる）。
- 本論文自体は小規模で、keiba-ai の設計根拠としての重みは低い。

## 関連ノート

- [Chen 1994](./1994-chen-greyhound-expert-symbolic-nn.md): 直接の先行研究。10変数・BPNN・$2 単勝の枠組みの元。
- [Schumaker 2008](./2008-schumaker-svr-longshot-greyhound.md): 本論文の数値を伝える二次資料。SVR に替えて券種を広げた後続研究。
- [Lyons 2016](./2016-lyons-greyhound-man-v-machine.md): Chen と本論文を出発点にしたグレイハウンドの後続研究。
- [Harville 1973](./1973-harville-multi-entry-probabilities.md): 連勝式の確率を勝率から作る古典。

## 検索語

グレイハウンド, ドッグレース, ニューラルネットワーク, 誤差逆伝播, BPNN, データマイニング, 公開データ, 単勝, 馬連, 馬単, quiniela, quinella, exacta, 連勝式, 回収率, Gulf Greyhound Park, greyhound racing, neural network, IJCNN, exotic bets

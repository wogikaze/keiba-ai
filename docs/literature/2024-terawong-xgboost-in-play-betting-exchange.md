---
title: XGBoost Learning of Dynamic Wager Placement for In-Play Betting on an Agent-Based Model of a Sports Betting Exchange
authors: Terawong Chawin, Cliff Dave
year: 2024
venue: Proceedings of the 16th International Conference on Agents and Artificial Intelligence (ICAART 2024); arXiv:2401.06086
url: https://arxiv.org/abs/2401.06086
doi: 10.48550/arXiv.2401.06086
topic: machine-learning
tags: xgboost, agent-based-model, betting-exchange, in-play, synthetic-data, profitability
verified: fulltext
importance: low
source: downloaded
source_version: preprint
---

# 賭け取引所のシミュレータ（BBE）で、儲かったエージェントの行動を XGBoost に真似させる

> 一言で: Bristol Betting Exchange（BBE）という、レースと取引所と賭け手を全部シミュレートするエージェントモデルで 1,000 レースを走らせた。最も儲けたエージェントたちの back/lay の行動を、レースの状態（距離・時刻・順位・賭け金）から XGBoost で予測させた。こうして作ったエージェントを市場に戻すと、元のどの単純戦略より利益が多かった。ただし実データは一切使っておらず、合成データ上の概念実証にとどまる。

## 背景: BBE とは

BBE は Cliff（2021）が作った、インプレー（レース中も売買できる）の賭け取引所のエージェントベースモデル（ABM）で、オープンソースで公開されている（p.2–3）。

- **レース**: 1次元のコースを5頭が走る。各時点の位置は実数で表す。実際の競馬の再現ではなく、ペースと順位の変化が「それらしい」データを作ることを狙う（p.3）。
- **取引所**: 実在の取引所と同じ方法で back と lay の注文を照合し、勝ち分から手数料を取る（p.3）。
- **賭け手のエージェント**（p.3–4）:

| 戦略 | 振る舞い |
|---|---|
| Zero Intelligence (ZI) | 無作為に賭ける |
| Leader Wins (LW) | 先頭の馬がそのまま勝つと見る |
| Underdog (UD) | 2番手が先頭に近ければ2番手に賭ける |
| Back The Favourite (BTF) | 市場の1番人気に賭ける |
| Linear Extrapolator (LinEx) | 各馬の速度を線形に外挿して勝ち馬を予想する |
| Privileged（RP(1,10,15)） | 公開レースと同じシミュレータで、現時点から最後まで1回だけ私的に走らせ、10〜15秒ごとに予想し直す。いわば「内部情報」を持つ |
| Representative Bettor (RB) | 2・5・10 の倍数の賭け金を好むなど人間らしく振る舞い、FLB も持つ |

## 手順（p.5–7）

1. **データ生成。** 同じ距離・5頭のレースを 1,000 回走らせる。賭け手は、Guzelyte の「意見を持つ」版の ZI・LW・BTF・LinEx・UD が各10、Privileged が5、元の版が同じ内訳で 55、合計 110 体（p.6）。
2. **学習データの作成。** 各レースで最も儲けた賭け手を見つけ、その行動を時間をさかのぼって集める。取引のうち「最も重要な」上位 20% だけを残す（p.5）。入力はその時点のレースと市場の状態、出力はその賭け手の行動（back か lay か）。
3. **学習。** XGBoost（scikit-learn API）、目的関数は `binary:logistic`、評価は log loss。GridSearchCV と5分割交差検証で eta・max_depth・subsample・colsample_bytree・gamma を調整した（p.6–7）。最適値は eta 0.3、max_depth 6、subsample 1.0、colsample_bytree 1.0、gamma 0。n_estimators 1,000、early stopping 10 で、452 本目で止まった（p.7–8）。
4. **検証。** 学習したモデルで動くエージェントを BBE に加え、2つのシナリオでそれぞれ 100 レースを走らせて利益を比べた（p.6, p.9）。
   - シナリオ1: 学習時とほぼ同じ構成（ZI・LW・UD・BTF・LinEx 各10、XGBoost と Privileged 各5）
   - シナリオ2: 全種類5体ずつ（環境を変える）
5. 利益の分布が正規でないので（Shapiro–Wilk 検定）、Mann–Whitney の U 検定で XGBoost エージェントと各エージェントを比べた（p.9）。

## 結果

学習の分類性能（p.8–9, Table 1–2）:

| | 予測 lay | 予測 back |
|---|---|---|
| 実際 lay | 72,521 | 1,197 |
| 実際 back | 9,541 | 6,730 |

- 正解率 0.88、back の適合率 0.85・再現率 0.41。
- 特徴量の重要度（分割に使われた回数）: 距離 8,680、時刻 6,642、順位 1,276（p.8）。特徴量は距離・順位・時刻・賭け金の4つだけ（p.12）。

利益の比較: どちらのシナリオでも、XGBoost エージェントは6種類のどのエージェントよりも利益が大きかった。U 検定の帰無仮説はすべて棄却され、最大の p 値はシナリオ2の Privileged との比較で 0.0017（p.9, Figure 7–18）。著者は、学習データを作った戦略のどれよりも儲かる戦略を学べたことを、概念実証とする（p.12）。

> a lot of further development work and much more extensive testing would be required before we would ever want to deploy this system live-betting with our own money. (p.3)

## 批判的に読む

- **正解率 0.88 は基準率とほとんど変わらない。** lay が全体の 82%（73,718 / 89,989）なので、全部 lay と答えても 0.82 になる。分類器としての力は限られる。
- **すべてシミュレータの中の話。** レースの動きは BBE のシミュレータが作り、Privileged エージェントも同じシミュレータで予想する。実際の競馬のペースや順位の変化、実際の取引所の流動性とは関係がない。
- **XGBoost エージェントは「情報を持つ」エージェントに勝った。** 同じシミュレータで未来を1回だけ試走できる Privileged に勝つのは、試走1回の予想が雑音を多く含むためかもしれない。勝てた理由の分析は無い。
- **検証は 100 レースずつ**で、利益の大きさや手数料の扱いは図にしか出てこない。
- 市場に XGBoost エージェントを加えると価格の動きも変わる。学習データを作った環境と検証の環境は、厳密には同じではない。
- 良い点: コードが GitHub で公開されており、再現できる（p.1）。

## keiba-ai での使い方

- 直接使える結果は無い。JRA はパリミュチュエル（発売締切後は売買できない）で、インプレーの取引所が無い。
- **「儲けた者の行動を真似る」のは危うい。** 利益は運に大きく左右されるので、ある期間に儲けた賭け手の行動をラベルにすると、運を学習してしまう。keiba-ai で他人の予想や買い目（予想家・オッズの急変）を教師に使う案が出たら、この点を思い出す。
- **シミュレータで戦略を試す発想。** 締切直前のオッズ変動（最終オッズと締切前オッズの差）をモデル化したシミュレータを作れば、締切何分前に買うか、という戦略をオフラインで比べられる。ただし BBE のように、シミュレータの中でしか通用しない戦略を学ぶ危険がある。
- **評価の点検。** 不均衡なデータの正解率は、基準率と並べて読む。

## 関連ノート

- [Smith 2006](./2006-smith-person-to-person-betting.md): 個人間の賭け取引所（Betfair）の効率性の実証。BBE が模している市場の実データ。
- [Franck 2010](./2010-franck-bookmakers-vs-betting-exchange.md): ブックメーカーと取引所の価格の比較。
- [Hanyu 2025](./2025-hanyu-last-minute-dynamics-parimutuel.md): パリミュチュエルの締切直前のオッズの動き。JRA でインプレーの代わりに考えるべき時間の次元。
- [Galekwa 2024](./2024-galekwa-systematic-review-ml-sports-betting.md): 本論文を「競馬の賭けを変革する」例として大きく取り上げたレビュー。
- [Stokes 2023](./2023-stokes-generative-frame-level-races.md): レース経過を実データから生成するモデル。BBE の人工的なレースよりも現実に近いシミュレータの材料になりうる。
- [Snowberg 2010](./2010-snowberg-flb-risk-love-misperceptions.md): RB エージェントが組み込んでいる FLB の実証研究。

## 検索語

エージェントベースモデル, agent-based model, ABM, マルチエージェント, シミュレーション, 合成データ, synthetic data, 賭け取引所, betting exchange, Betfair, インプレー, in-play betting, ライブベッティング, back, lay, バック, レイ, Bristol Betting Exchange, BBE, XGBoost, 模倣学習, imitation learning, 行動クローニング, behavioral cloning, Zero Intelligence, 不均衡データ, Mann-Whitney U, Cliff

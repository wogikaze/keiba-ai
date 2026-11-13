---
title: 競馬歴30年のおっさんがClaudeを相棒にAI予想システムを作るまでの記録（昼カラ競馬 #001〜#005）
authors: 昼カラ競馬（hirukara-keiba）
year: 2026
venue: はてなブログ（昼カラ競馬）、Internet Archive のコピー
url: https://hirukara-keiba.hatenablog.com/entry/20260301/1772338979
topic: practitioner
tags: grey-literature, jra-van, jv-link, bigquery, gcp, lightgbm, llm-assisted-coding, parser-bug, random-cv, popularity-feature
verified: fulltext
importance: medium
source: downloaded
source_version: web
---

# JV-Link の固定長パーサのバイト位置ずれで 47万行が「全部ゴミ」だった、LLM 任せの開発記

> 一言で: プログラミング経験の少ない競馬歴30年の著者が、Claude・Gemini・ChatGPT にコードを書かせて JRA-VAN（JV-Link）→ GCS → BigQuery → LightGBM のシステムを作った記録。取込は8回目で ERROR=0 になったが、その後、固定長レコードのバイト位置が仕様書とずれていて距離・頭数・騎手コード・確定着順が全部 NULL か誤りだったと判明し、RACE を4回取り直した。LightGBM（3着内の二値分類と読める）は 5-fold CV で OOF AUC 0.8896、重要度1位は人気順。

ブログは 2026年11月時点で 404（削除）。Internet Archive に残っていた6本を保存した（本文と `attachments/post1`〜`post5`）。シリーズはこの後 #006「やっと勝てる設定ができた」や、検索結果のタイトルで見えた「リーク修正：187%が98%に落ちた日」の回まで続いたが、それらはアーカイブがなく本文を確認できていない。以下は保存できた回だけに基づく。

| 保存名 | 回 | 内容 |
|---|---|---|
| source | 2026-03-01 | JRA-VAN からのデータ取得（C#/.NET で JV-Link → GCS、ChatGPT による作業報告書） |
| post1 | #001 構想・設計・そして最初の壁 | 7軸スコアの設計、GCP 3層構成 |
| post2 | #002 COMとの格闘 | JV-Link の COM 接続 |
| post3 | #003 ERROR=0への長い道のり | パーサ → ステージング → MERGE、setup 8回 |
| post4 | #004 全部ゴミだった | バイト位置ずれの発覚と全パーサ照合 |
| post5 | #005 LightGBM、AUC 0.89の衝撃 | 特徴量ビュー14本、学習結果 |

## データ

- JRA-VAN Data Lab を JV-Link（32bit Windows 専用の COM）で取得。GCE の Windows Server VM で取得し、BigQuery に入れ、Mac で学習する3層構成（#001「GCPアーキテクチャの決定」）。
- Python（32bit）での取得は断念し、C#/.NET で `JVInit→JVOpen→JVStatus→JVGets→JVClose` を実装し、jsonl.gz を GCS に置く形にした（source「作業報告書」）。DataSpec は仕様書から38件を抽出。RACE の初回取込は FilesRead=1370、RecordsWritten=137,660。
- 期間は2020年以降（「そんな昔のデータはいらんであろう」）。最終的に馬毎レース情報（SE）477,222件、ウッドチップ調教70万件超（#003、#004）。
- 蓄積系（週次差分）と当日系（速報・オッズ 0B 系、開催日に5〜10分間隔）をジョブ・チェックポイント・テーブルで分ける設計を書いている（source「追記」）。

## 特徴量

#001 で Claude と議論して「7軸スコアリング」に落ち着いた: ①タイム型マイニング（DM）、②対戦型マイニング（TM）、③騎手×調教師コンビ・穴騎手スコア、④AI 予測確率と市場支持率の乖離、⑤時系列オッズの変化（例: 9時〜12時に30%以上急落）、⑥ペース適性×前走内容、⑦血統×条件替わり。
#005 では BigQuery に特徴量ビューを14本作った（jockey_trainer_combo_stats、horse_pace_affinity、sire_condition_stats、sire/bms/nicks の3着内率など）。
JRA-VAN のマイニング指数（DM/TM）は JRA-VAN 側が出す予測値そのもの。

## モデルと目的変数

- LightGBM、47万件、5分割交差検証（#005「train_lgbm.pyを実行する」）。目的変数は明記がないが、#001 のゴール「3着内率の高い馬を特定」と LogLoss・AUC の出力から、3着内の二値分類と読める。
- 買い方は #001 の構想で、3連単48点＋3連複21点の計69点のフォーメーション（2→5→8）。期待値プラスの馬券だけを買い、買わないレースを厳格に判断する方針。

## 結果

- #005: Fold ごとの AUC 0.8837〜0.8934、OOF AUC 0.8896、OOF LogLoss 0.3435。
- 重要度: 1位 ninkijun（人気順）、2位 馬の加重3着内率、3位 前走着順、4位 中間隔週数、5位 beat_odds_rate（人気より上の着順に来る率）。
- 回収率は保存できた回にはない。

## 落とし穴と教訓

- 固定長レコードのバイト位置: RA の kyori（距離）を offset 137 で読んでいて全件 NULL。仕様書の位置267（1-indexed）→ offset 266 が正しかった。tosu・nyusen_tosu（頭数）もずれていた。SE は kishu_code が offset 77 で、正しくは 297。調教師コード・確定着順も含めて全フィールドがずれていた（#004）。1個直すと次が出る形で RACE を4回（1回2時間）取り直した。
- 対策として、合成データでバイト位置を検証する `tests/test_parser_bytes.py`、仕様書との照合 `validate_parsers.py`（最終 OK=10 NG=0 WARN=5）、BigQuery の実テーブルとスキーマ定義の差分を見る `check_schema_gaps.py`（40カラム欠落を検出）を「プレフライト」として定着させた（#003、#004）。
- MERGE は最初のエラーで止まるので、エラーを1つずつしか直せず setup を8回やり直した。
- 騎手・調教師マスタ（KS/CH）がほぼ取れず jockeys・trainers が1件だった。LEFT JOIN で回避（#004）。
- 血統: 繁殖登録番号（8桁）と血統登録番号（10桁）を取り違えた JOIN で sire/bms/nicks のビューが0件だった（#005）。
- 32bit Python を入れたことで gcloud の bq コマンドが壊れ、BigQuery 操作は全部 Python ライブラリ経由にした（#001）。

## 批判的に読む

- AUC 0.89 は 5分割交差検証で、レースや日付でグループ化した形跡がない。同じレースの馬や未来のレースが学習側に入るランダム分割なので、時系列の汎化性能より楽観的になる。
- 重要度1位が人気順で、人気が確定値なら確定オッズのリークと同じ問題になる。どの時点の人気かは書かれていない。人気を入れた3着内予測なら AUC 0.89 の大半は市場の情報で説明できる。
- 「過去3着内率」「beat_odds_rate」などの集計ビューが当該レースを除いて計算されているか書かれていない。SQL ビューでの集計は当該レースを含めやすい。
- 生成 AI が「0.8を超えれば実用的」「非常に優秀」と評価し、著者がそれを受け入れている。シリーズ後半でリーク修正により回収率が 187%→98% に落ちた回がある（タイトルのみ確認）のは、この評価の甘さと整合する。
- 本文の一部は LLM に書かせたコラムで、会話の再現が正確かは分からない。

## keiba-ai での使い方

- JRA-VAN の固定長レコードを自前でパースするなら、仕様書の位置（1-indexed）と offset（0-indexed）の対応を全フィールドで表にし、合成レコードでのテストと、取り込み後の分布チェック（距離が全件 NULL でないか、着順の1〜3が各レース1件ずつか）を取り込みの前後に必ず走らせる。
- 取込の健全性チェック（全件 NULL の列、0件の JOIN、マスタ件数）は特徴量計算の前に自動で止める。
- 交差検証はレース日で時系列に切る。人気・オッズを特徴量に入れる場合は「何分前のオッズか」を固定し、入れないモデルと必ず並べる。
- 蓄積系と当日系（オッズ）のジョブ分離は、運用設計の参考になる。

## 関連ノート

- [watanta 2021](./2021-watanta-mlops-keiba.md): netkeiba 由来で同じくデータバリデーションに最も時間を使った個人開発。
- [todaitired 2026](./2026-todaitired-jra-lightgbm-odds.md): JRA-VAN（TARGET 経由）で、オッズを使わないモデルと市場を疑似R²で比べた例。人気を特徴量に入れた本シリーズと対照的。
- [Sugiura 2026](./2026-sugiura-leakage-aware-evaluation.md): JRA-VAN データで予測時点の変数を棚卸しし、確定オッズ・人気を除外した論文。
- [Cerqueira 2020](./2020-cerqueira-time-series-performance-estimation.md): ランダム CV と時系列評価の違い。

## 検索語

JV-Link、JRA-VAN Data Lab、固定長 パーサ バイト位置、RA レコード SE レコード、DataSpec、BigQuery MERGE、Claude Code 競馬、生成AI 開発、AUC 0.89、人気順 特徴量、5-fold 交差検証 リーク、繁殖登録番号 血統登録番号、マイニング指数、ウッドチップ調教、昼カラ競馬

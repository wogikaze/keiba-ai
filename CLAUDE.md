# keiba-ai 運用ルール

競馬予測AIの研究リポジトリ。再現性と「なぜそうしたか」の記録を最優先する。

## ディレクトリ

| パス | 役割 |
| --- | --- |
| `docs/literature/` | 先行研究ノート。1本1ファイル、`YYYY-著者-キーワード.md` |
| `docs/adr/` | 設計判断ログ（ADR）。`NNNN-タイトル.md`、連番 |
| `experiments/` | 実験。1実験1ディレクトリ、`YYYY-MM-DD_短い名前/` |
| `experiments/INDEX.md` | リーダーボード。**手で編集しない**（`scripts/build_index.py` で生成） |
| `src/keiba_ai/` | 再利用するPythonコード（特徴量・学習・評価） |
| `library/` | 先行研究の原本（PDF・HTML）と文字起こし。**git管理しない**（著作権）。`scripts/library.py` で管理 |
| `data/` | データ本体。git管理しない（`raw/` は不変、`processed/` は再生成可能） |
| `site/` | ox-content + Vue の閲覧サイト。main への push で GitHub Pages に自動デプロイ |

## 実験のルール

1. 新しい実験は `experiments/_template/` をコピーして始める。
2. `README.md` に **仮説・変更点・結果・結論** を必ず書く。仮説は実行前に書く。
3. `config.yaml` に実験を再現するための全パラメータを書く。コード中のマジックナンバー禁止。
4. `results.json` には最低限 `metrics`・`git_hash`・`data_version`・`seed` を記録する。
   - 実行前にコミットし、ワーキングツリーがクリーンな状態の `git_hash` を記録する。
5. 実験ディレクトリは作成後に結果を書き換えない。やり直すときは新しいディレクトリを作る。
6. 結果を記録したら `uv run python scripts/build_index.py` で `INDEX.md` を更新する。

## 評価のルール

- 分割は **時系列** のみ（ランダム分割禁止）。リークを避けるため、レース当日以降の情報は特徴量に使わない。
- 主指標・分割期間を変えるときは ADR を書く。
- 回収率は控除率込みで評価する。的中率だけで良し悪しを判断しない。

## ドキュメントのルール

- 文献ノート・ADR・実験READMEは frontmatter（`title`, `date` など）を付ける。サイトの一覧に使う。
- frontmatter はフラットな `key: value` のみ（ox-content のパーサー仕様）。
- 特徴量・分割・評価方法の変更は、理由を ADR に残してから実験する。

## 先行研究のルール

- 1文献1ノート（`docs/literature/<year>-<第一著者>-<キーワード>.md`）。原本は `library/<同じslug>/` に置く。
- 原本は全文を取得する。出版社のOA・arXiv・著者PDF・J-STAGE・SSRN・ワーキングペーパーに加え、**第三者サイトのコピー（gwern.net、授業ページ、ResearchGate、Academia.edu、docplayer、Internet Archive など）も積極的に使う**。海賊版サイトそのもの（Sci-Hub、LibGen など）は使わない。
- 普通の取得が拒否されたら `fetch --browser`（Playwright の実ブラウザ。ヘッドレスで止まると画面ありで再試行）を使う。それでも取れなければ、試した URL と結果を `library.py mark <slug> unavailable --reason ...` に書く。
- スキャン画像や文字化けしたPDF（`needs_ocr`）は `library.py ocr` で機械 OCR する。LLM に逐語で文字起こしさせない（長文の転載として出力がブロックされる）。
- ノートが二次資料に頼った場合、その資料も `library.py attach` で保存する。
- ノートの数値・主張には原本のページを付ける（例: `(p.12)`）。原文の引用は短く（1〜2文）。ノートは公開されるため。
- 書く前に `library.py search` で原本を検索し、既存ノートとの関係を「関連ノート」に書く。
- `uv run python scripts/check_literature.py` が通ること。

## git

- 長い作業は1時間に1コミット程度の単位でコミットする。main への push で GitHub Pages が更新される。

## コマンド

```sh
uv sync                                  # Python環境
uv run python scripts/build_index.py     # INDEX.md 再生成
uv run python scripts/library.py search 語 [語...]   # 原本の全文検索（ページ番号つき）
uv run python scripts/library.py status -v          # 原本の取得状況
uv run python scripts/library.py fetch <slug> <url> --version published   # 原本を取得
uv run --extra browser python scripts/library.py fetch <slug> <url> --browser  # 実ブラウザで取得
uv run python scripts/library.py add <slug> <PDF> --url <入手元>          # 手動ダウンロードした原本を取り込む
uv run python scripts/library.py attach <slug> <名前> <url>               # 二次資料を添付
uv run --extra ocr python scripts/library.py ocr                          # スキャン・文字化けPDFを OCR
cd site && pnpm install && pnpm dev      # 閲覧サイト
```

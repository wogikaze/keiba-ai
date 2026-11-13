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

## コマンド

```sh
uv sync                                  # Python環境
uv run python scripts/build_index.py     # INDEX.md 再生成
cd site && pnpm install && pnpm dev      # 閲覧サイト
```

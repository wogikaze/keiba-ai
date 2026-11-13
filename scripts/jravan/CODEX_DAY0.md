# Codex への依頼: JRA-VAN 取得の開始（Day 0）

Windows 上で作業する。**ユーザーの了承済み**: 今日（Day 0）JV-Link をインストールして、JRA-VAN Data Lab. の無料お試し（31 日）を始める。
事前準備（`CODEX_PREP.md`）は済んでいる（`E:\keiba-ai\jra-van\` に SDK・仕様書・スクリプト・`.venv` がある）。
計画の詳細: `\\wsl.localhost\Ubuntu\home\wogikaze\keiba-ai\docs\data\jra-van-download-plan.md`。

GUI の操作（インストーラ、ダイアログ）は computer use で行う。

## してはいけないこと

- JRA-VAN のサイトでのアカウント登録・ログイン・支払い情報の入力はしない（お試しは利用キーなしで使えるはず）。求められたら、そこで止めて報告する。
- `E:\keiba-ai\` 以外のファイルを消さない。WSL 側のファイルは読むだけ。

## 手順

### 1. 最新のスクリプトをコピー

```powershell
$src = '\\wsl.localhost\Ubuntu\home\wogikaze\keiba-ai\scripts\jravan'
Copy-Item -Force "$src\*.py","$src\*.ps1" 'E:\keiba-ai\jra-van\scripts\'
```

### 2. JV-Link をインストール（computer use）

`E:\keiba-ai\jra-van\sdk\JRA-VAN Data Lab. SDK Ver5.0.0_64bit\JV-Link\JV-Link.exe` を実行し、使用許諾に同意して既定の設定でインストールする。
インストール日時を記録する（お試し期間の起算日）。再起動を求められたら報告して止める。

### 3. 動作確認

```powershell
cd E:\keiba-ai\jra-van\scripts
$env:PYTHONIOENCODING = 'utf-8'
.venv\Scripts\python.exe -u jv_smoke.py
```

- 保存パス `E:\keiba-ai\jra-van\jvlink-data` と保存フラグを設定し、直近 7 日の RACE と、直近のレースの時系列オッズ（0B41・0B42）を取る。
- JV-Link のダイアログ（利用規約の同意、サービスキーの入力など）が出たら、computer use で対応する。利用規約の同意画面は同意してよい。**サービスキー（利用キー）を求められたら入力せず、止めて報告する。**
- 結果の JSON（`logs\smoke_*.json`）の `race_open.status` が `ok`、`0B41.status` が `ok` であること。`announce_times`（オッズの発表時刻の一覧）を報告に書く。
- `-303`（利用キー未設定）、`-305`（規約未同意）、`-211`（保存パスなし）などで失敗したら、その戻り値を報告して止める。

### 4. JV-Link の設定画面（computer use）

```powershell
.venv\Scripts\python.exe -c "import win32com.client as w; j=w.Dispatch('JVDTLab.JVLink'); print(j.JVInit('UNKNOWN')); print(j.JVSetUIProperties())"
```

開いた設定画面で次を確認・設定して閉じる（OK）:
- データ保存パス: `E:\keiba-ai\jra-van\jvlink-data`
- 保存する（保存フラグ）: オン
- 払戻ダイアログ: 表示しない
設定画面の内容（項目と値）を報告に書く。

### 5. セットアップの 1 回目を画面の前で実行（computer use）

```powershell
.venv\Scripts\python.exe -u jv_setup.py RACE 1986 1986
```

途中で「スタートキット（CD/DVD）を持っているか」のダイアログが出たら **「持っていない」** を選ぶ。ほかのダイアログが出たら内容を報告に書き、妥当なら進める。
`records` が 0 より大きく、`raw\RACE\1986.txt` ができること。もう 1 回同じコマンドを実行して「済み」で飛ばされること、ダイアログが出ないことを確かめる。

### 6. 無人実行をタスクスケジューラに登録

すべて現在のユーザーで、「ユーザーがログオンしているときのみ実行」、同じタスクが実行中なら新しく起動しない。
コマンドは `powershell.exe -NoProfile -ExecutionPolicy Bypass -File E:\keiba-ai\jra-van\scripts\<ps1>`。

| タスク名 | いつ | 実行するもの |
|---|---|---|
| `keiba-jv-day0` | 今すぐ（1 回だけ） | `run_setup_all.ps1` の後に `run_timeseries.ps1 -StopAt 0730` |
| `keiba-jv-realtime` | 毎週 土・日 7:50 | `run_realtime.ps1` |
| `keiba-jv-ts-night` | 毎日 18:30（**開始日は明日**） | `run_timeseries.ps1 -StopAt 0730` |
| `keiba-jv-ts-day` | 月〜金 7:35（開始日は明日以降の月曜） | `run_timeseries.ps1 -StopAt 1825` |

`keiba-jv-day0` は、2 つの ps1 を順に呼ぶ小さなラッパー `E:\keiba-ai\jra-van\scripts\run_day0.ps1` を作って登録する。
登録後、`keiba-jv-day0` を起動し、数分後に `logs\run_setup_all_*.log` に RACE の年ごとの行が出ていることを確かめる。

### 7. 報告

`E:\keiba-ai\jra-van\logs\day0_report.md` に書く:
- JV-Link のインストール日時（お試しの起算日）とバージョン
- 動作確認の結果（smoke の JSON の要点、オッズの発表時刻の一覧と刻み）
- 設定画面の内容
- 出たダイアログと選んだもの
- 登録したタスクの一覧（`schtasks /Query /TN keiba-jv-* /V /FO LIST` の要点）
- `keiba-jv-day0` の進み具合（ログの最後の数行）
- 問題・止めた手順があればその内容
標準出力にも要約を出す。

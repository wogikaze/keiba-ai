# Codex への依頼: JRA-VAN 取得の事前準備（JV-Link はインストールしない）

あなたは Windows 上で作業する。競馬予測の研究リポジトリ（WSL 内 `\\wsl.localhost\Ubuntu\home\wogikaze\keiba-ai`）の取得計画
`docs\data\jra-van-download-plan.md` の「1. Day 0 より前にやること」を実行する。

## 絶対にしないこと

- **JV-Link をインストールしない。`JV-Link.exe` を実行しない。** インストールした日から 31 日の無料お試し期間が始まるため、今日はやらない。
- JRA-VAN のサイトでアカウント登録・ログイン・申し込みをしない。
- `E:\keiba-ai\` 以外のファイルを消さない。Windows Update の設定は変えない。
- WSL 側（`\\wsl.localhost\...`）のファイルは読むだけで、書き換えない。

## やること

1. フォルダを作る:
   ```powershell
   $root = 'E:\keiba-ai\jra-van'
   'jvlink-data','raw','logs','sdk','specs','scripts' | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $root $_) | Out-Null }
   ```
2. SDK・仕様書・取得スクリプトをコピーする:
   ```powershell
   $src = '\\wsl.localhost\Ubuntu\home\wogikaze\keiba-ai'
   Copy-Item -Recurse -Force "$src\data\raw\jra-van\sdk\*"   "$root\sdk\"
   Copy-Item -Recurse -Force "$src\data\raw\jra-van\specs\*" "$root\specs\"
   Copy-Item -Force "$src\scripts\jravan\*.py" "$root\scripts\"
   Get-ChildItem "$root\sdk" -Recurse -Filter 'JV-Link.exe' | Select-Object FullName, Length
   ```
   `JV-Link.exe` が見つかることだけ確認する（実行しない）。
3. Python 環境（64bit、3.12 以上）を `E:\keiba-ai\jra-van\scripts\.venv` に作り、pywin32 を入れる:
   ```powershell
   cd E:\keiba-ai\jra-van\scripts
   uv venv --python 3.12
   uv pip install --python .venv\Scripts\python.exe pywin32
   .venv\Scripts\python.exe -c "import struct, win32com.client; print(struct.calcsize('P')*8, 'bit OK')"
   ```
   64 bit と表示されること。続けて、JV-Link が**未登録で失敗すること**を確かめる（失敗するのが正常）:
   ```powershell
   .venv\Scripts\python.exe -c "import win32com.client; win32com.client.Dispatch('JVDTLab.JVLink')"
   ```
4. 偽の JV-Link で 4 本のスクリプトを試す。出力はテスト用フォルダ `E:\keiba-ai\jra-van-faketest` に出す:
   ```powershell
   $env:JV_FAKE = '1'; $env:JV_ROOT = 'E:\keiba-ai\jra-van-faketest'; $env:PYTHONIOENCODING = 'utf-8'
   $py = '.venv\Scripts\python.exe'
   & $py -u jv_setup.py RACE 2024 2026
   & $py -u jv_setup.py RACE 2024 2026          # 2 回目は「済み」で飛ばされること
   & $py -u jv_setup.py DIFN --all
   $env:JV_FAKE_FAIL_ONCE = '1'; & $py -u jv_setup.py SLOP 2025 2025; Remove-Item Env:JV_FAKE_FAIL_ONCE   # 「開き直す」が出て成功すること
   & $py -u jv_timeseries.py 2026 2024 --until 20261231
   & $py -u jv_update.py RACE COMM
   & $py -u jv_realtime.py (Get-Date -Format yyyyMMdd) --once
   Get-ChildItem -Recurse E:\keiba-ai\jra-van-faketest | Measure-Object | Select-Object Count
   ```
   どれもエラーなく終わり、`raw\RACE\2026.txt`、`raw\0B41\2026\*.txt`、`raw\realtime\0B30\<今日>\*.txt`、`logs\manifest.jsonl` ができること。
   確認が済んだら `E:\keiba-ai\jra-van-faketest` を削除し、環境変数を消す。
5. スリープを無効にする（電源接続時）:
   ```powershell
   powercfg /change standby-timeout-ac 0
   powercfg /change hibernate-timeout-ac 0
   ```
   変更前の値を `powercfg /query SCHEME_CURRENT SUB_SLEEP` で記録しておく。
6. 空き容量を記録する: `Get-PSDrive E | Select-Object Used, Free`。

## 報告

`E:\keiba-ai\jra-van\logs\prep_report.md` に、各手順の結果（成功/失敗、出力の要点、エラーがあれば全文）、Python のバージョンと bit 数、スリープ設定の変更前後の値、空き容量を書く。最後に標準出力にも同じ内容の要約を出す。
問題があった手順は、自分で直せる範囲（パスの誤りなど）なら直し、何を直したかを報告に書く。スクリプトの中身を変えた場合は、変更点を報告に書く（WSL 側のファイルは変えない）。

# 通常データ（option 1）の差分を取る。月曜 14:00 頃に確定成績、木曜 20:00 頃に出走馬名表とマスタの差分が出る
$env:PYTHONIOENCODING = 'utf-8'
Set-Location 'E:\keiba-ai\jra-van\scripts'
$m = New-Object System.Threading.Mutex($false, 'Global\keiba-jv')
try { $got = $m.WaitOne([TimeSpan]::FromMinutes(30)) } catch [System.Threading.AbandonedMutexException] { $got = $true }
if (-not $got) { "$(Get-Date -Format s) run_update: 別の取得が実行中なので終える" | Add-Content 'E:\keiba-ai\jra-van\logs\mutex_skip.log'; exit 0 }
$log = "E:\keiba-ai\jra-van\logs\run_update_$(Get-Date -Format yyyyMMdd-HHmmss).log"
& .venv\Scripts\python.exe -u jv_update.py RACE DIFN DIFF BLDN BLOD SNPN SLOP WOOD YSCH HOSN HOSE HOYU MING COMM TOKU 2>&1 | Tee-Object -FilePath $log -Append
$m.ReleaseMutex()

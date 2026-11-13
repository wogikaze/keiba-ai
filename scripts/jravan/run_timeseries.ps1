# 時系列オッズ（0B41・0B42）を新しい年から古い年へ取る。引数: 止める時刻 HHMM（既定 0730）
param([string]$StopAt = '0730')
$env:PYTHONIOENCODING = 'utf-8'
# 他の取得（Day 0 のセットアップなど）と JV-Link を同時に使わない。run_day0.ps1 から呼ばれたときは同じプロセスなので取れる
$m = New-Object System.Threading.Mutex($false, 'Global\keiba-jv')
try { $got = $m.WaitOne(0) } catch [System.Threading.AbandonedMutexException] { $got = $true }
if (-not $got) { "$(Get-Date -Format s) run_timeseries: 別の取得が実行中なので終える" | Add-Content 'E:\keiba-ai\jra-van\logs\mutex_skip.log'; exit 0 }
Set-Location 'E:\keiba-ai\jra-van\scripts'
$py = '.venv\Scripts\python.exe'
$year = (Get-Date).Year
$log = "E:\keiba-ai\jra-van\logs\run_timeseries_$(Get-Date -Format yyyyMMdd-HHmmss).log"
& $py -u jv_timeseries.py $year 2003 --stop-at $StopAt 2>&1 | Tee-Object -FilePath $log -Append
$m.ReleaseMutex()

# 時系列オッズ（0B41・0B42）を新しい年から古い年へ取る。引数: 止める時刻 HHMM（既定 0730）
param([string]$StopAt = '0730')
$env:PYTHONIOENCODING = 'utf-8'
Set-Location 'E:\keiba-ai\jra-van\scripts'
$py = '.venv\Scripts\python.exe'
$year = (Get-Date).Year
$log = "E:\keiba-ai\jra-van\logs\run_timeseries_$(Get-Date -Format yyyyMMdd-HHmmss).log"
& $py -u jv_timeseries.py $year 2003 --stop-at $StopAt 2>&1 | Tee-Object -FilePath $log -Append

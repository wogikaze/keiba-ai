# 開催日の速報を記録する（当日分）。タスクスケジューラから土日の朝に起動する
$env:PYTHONIOENCODING = 'utf-8'
Set-Location 'E:\keiba-ai\jra-van\scripts'
$py = '.venv\Scripts\python.exe'
$d = Get-Date -Format yyyyMMdd
$log = "E:\keiba-ai\jra-van\logs\run_realtime_$d.log"
& $py -u jv_realtime.py $d --until 1730 2>&1 | Tee-Object -FilePath $log -Append
# レース終了後、当日分の時系列オッズを 1 回だけ取る
& $py -u jv_timeseries.py (Get-Date).Year (Get-Date).Year --since $d --until $d 2>&1 | Tee-Object -FilePath $log -Append

# Day 0: セットアップ（全種別）の後に時系列オッズを取る。タスク keiba-jv-day0 から 1 回だけ起動する
$m = New-Object System.Threading.Mutex($false, 'Global\keiba-jv')
if (-not $m.WaitOne(0)) { "$(Get-Date -Format s) 別の取得が実行中なので終える" | Add-Content 'E:\keiba-ai\jra-van\logs\mutex_skip.log'; exit 0 }
try {
    & "$PSScriptRoot\run_setup_all.ps1"
    & "$PSScriptRoot\run_timeseries.ps1" -StopAt 0730
} finally { $m.ReleaseMutex() }

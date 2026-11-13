# タスクスケジューラに無人実行を登録する（現在のユーザー、ログオン中のみ、多重起動しない）
$dir = 'E:\keiba-ai\jra-van\scripts'
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Days 3) -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
function Act($ps1, $extra = '') { New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File $dir\$ps1 $extra" -WorkingDirectory $dir }
$tomorrow = (Get-Date).Date.AddDays(1)
$monday = $tomorrow; while ($monday.DayOfWeek -ne 'Monday') { $monday = $monday.AddDays(1) }
$defs = @(
    # keiba-jv-day0 は 2026-11-13 に実行済み。登録し直すとすぐ再実行される（取得済みの単位は飛ばす）
    @{ n = 'keiba-jv-day0';     a = (Act 'run_day0.ps1');                    t = (New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)) },
    @{ n = 'keiba-jv-realtime'; a = (Act 'run_realtime.ps1');                t = (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Saturday, Sunday -At 7:50) },
    @{ n = 'keiba-jv-ts-night'; a = (Act 'run_timeseries.ps1' '-StopAt 0730'); t = (New-ScheduledTaskTrigger -Daily -At $tomorrow.AddHours(18).AddMinutes(30)) },
    @{ n = 'keiba-jv-update';   a = (Act 'run_update.ps1');                  t = (New-ScheduledTaskTrigger -Daily -At $tomorrow.AddHours(18).AddMinutes(5)) },
    @{ n = 'keiba-jv-ts-day';   a = (Act 'run_timeseries.ps1' '-StopAt 1825'); t = (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At $monday.AddHours(7).AddMinutes(35)) }
)
foreach ($d in $defs) {
    Register-ScheduledTask -TaskName $d.n -Action $d.a -Trigger $d.t -Settings $settings -Principal $principal -Force | Out-Null
}
Get-ScheduledTask -TaskName 'keiba-jv-*' | ForEach-Object { $i = $_ | Get-ScheduledTaskInfo; '{0}  next={1}  state={2}' -f $_.TaskName, $i.NextRunTime, $_.State }

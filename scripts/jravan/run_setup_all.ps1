# セットアップ（全種別）を計画の順に実行する。docs/data/jra-van-download-plan.md「Day 0〜2: セットアップ」
# 済んだ単位はマニフェストで飛ばすので、途中で止まっても再実行すれば続きから。
$ErrorActionPreference = 'Continue'
$env:PYTHONIOENCODING = 'utf-8'
Set-Location 'E:\keiba-ai\jra-van\scripts'
$py = '.venv\Scripts\python.exe'
$year = (Get-Date).Year
$oneYearAgo = (Get-Date).AddYears(-1).ToString('yyyyMMdd') + '000000'
$log = "E:\keiba-ai\jra-van\logs\run_setup_all_$(Get-Date -Format yyyyMMdd-HHmmss).log"

function Run($argsList) {
    "=== $(Get-Date -Format s) jv_setup.py $($argsList -join ' ')" | Tee-Object -FilePath $log -Append
    & $py -u jv_setup.py @argsList 2>&1 | Tee-Object -FilePath $log -Append
    "=== exit $LASTEXITCODE" | Tee-Object -FilePath $log -Append
    return $LASTEXITCODE
}

Run @('RACE', '1986', "$year")
Run @('DIFN', '--all')
Run @('DIFF', '--all')
Run @('BLDN', '--all')
Run @('BLOD', '--all')
Run @('SNPN', '2004', "$year")
Run @('SNAP', '2004', "$year")
Run @('SLOP', '2003', "$year")
if ((Run @('WOOD', '--all', '--from', '20210701000000')) -ne 0) {
    # option 4 で -301 になる報告がある（crossclub_lab）。option 1 で取り直す
    Run @('WOOD', '--all', '--from', '20210701000000', '--option', '1')
}
Run @('MING', '2001', "$year")
Run @('YSCH', '--all', '--from', '20000101000000')
Run @('HOSN', '--all')
Run @('HOSE', '--all')
Run @('HOYU', '--all')
Run @('COMM', '--all')
Run @('TOKU', '--all', '--from', $oneYearAgo, '--option', '1')
"=== done $(Get-Date -Format s)" | Tee-Object -FilePath $log -Append

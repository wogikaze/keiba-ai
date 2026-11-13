# JV-Link のセットアップダイアログで「スタートキットを持っていない」を選んで OK を押す
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W { [DllImport("user32.dll")] public static extern IntPtr GetDlgItem(IntPtr h, int id);
[DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, IntPtr l); }
"@
$BM_CLICK = 0x00F5
$p = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -eq 'セットアップ' } | Select-Object -First 1
if (-not $p) { 'no dialog'; exit 0 }
$h = $p.MainWindowHandle
$no = [W]::GetDlgItem($h, 228); $ok = [W]::GetDlgItem($h, 1)
if ($no -eq [IntPtr]::Zero -or $ok -eq [IntPtr]::Zero) { 'controls not found'; exit 1 }
[W]::SendMessage($no, $BM_CLICK, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
Start-Sleep -Milliseconds 300
[W]::SendMessage($ok, $BM_CLICK, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
"clicked 持っていない + OK (pid $($p.Id))"

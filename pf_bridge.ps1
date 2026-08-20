# PF BRIDGE — visible command console
#
# อ่านสคริปต์ที่ Claude วางไว้ใน inbox\ แล้วรันทีละไฟล์ในหน้าต่างนี้
# ทุกคำสั่งถูกพิมพ์ให้เห็นเต็ม ๆ ก่อนรัน ปิดด้วย Ctrl+C ได้ตลอดเวลา
#
#   ค่าเริ่มต้น = AUTO (รันทันทีไม่ถาม)
#   -Ask      กลับไปโหมดถามก่อนรันทุกงาน

param(
    [string]$Root = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge',
    [switch]$Ask
)
$Auto = -not $Ask

$ErrorActionPreference = 'Continue'

$inbox  = Join-Path $Root 'inbox'
$outbox = Join-Path $Root 'outbox'
$done   = Join-Path $Root 'done'
foreach ($d in @($Root, $inbox, $outbox, $done)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

# --- loop heartbeat (added 2026-08-19 by chief round 89) ---------------------
# WHY THIS EXISTS.  The watchdog can only see whether a PROCESS is alive, and on
# 2026-08-19 at ~16:51 a bridge stayed alive while its LOOP stopped: job 906 ran,
# its output was written, and the file was never moved to done\, so nothing was
# picked up for the next forty minutes while the watchdog kept writing
# "bridge-alive" every five minutes.  A visible console that somebody clicks into
# enters Select mode and blocks on the next Write-Host, which looks exactly like
# this.  One small file, rewritten on every poll and around every job, tells the
# two states apart:  "idle <ts>" = the loop is turning;  "running <job> <ts>" =
# a job is in flight and MUST NOT be killed.  ASCII only.
$state = Join-Path $Root 'bridge_loop_state.txt'
function Set-LoopState($what) {
    try { "$what  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" |
          Out-File -FilePath $state -Encoding ascii -Force } catch {}
}
Set-LoopState 'idle'

try { $Host.UI.RawUI.WindowTitle = 'PF BRIDGE — visible command console' } catch {}

$line = '-' * 78
Write-Host ''
Write-Host '=== PF BRIDGE ===' -ForegroundColor Cyan
Write-Host "root  : $Root"
Write-Host "mode  : $(if ($Auto) { 'AUTO — รันทันที' } else { 'CONFIRM — ถามก่อนรันทุกงาน' })"
Write-Host 'stop  : Ctrl+C'
Write-Host ''
Write-Host 'รอสคริปต์ใน inbox\ ...' -ForegroundColor DarkGray

while ($true) {

    $job = Get-ChildItem -Path $inbox -Filter '*.ps1' -File -ErrorAction SilentlyContinue |
           Sort-Object Name |
           Select-Object -First 1

    if (-not $job) { Set-LoopState 'idle'; Start-Sleep -Seconds 3; continue }

    # ให้ไฟล์เขียนเสร็จก่อน
    Start-Sleep -Milliseconds 500

    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host ''
    Write-Host $line -ForegroundColor DarkGray
    Write-Host "[$stamp]  JOB: $($job.Name)" -ForegroundColor Yellow
    Write-Host $line -ForegroundColor DarkGray
    Get-Content -Raw -LiteralPath $job.FullName | Write-Host
    Write-Host $line -ForegroundColor DarkGray

    if (-not $Auto) {
        Write-Host 'ENTER = รัน   |   s + ENTER = ข้าม   |   Ctrl+C = หยุดทั้งหมด' -ForegroundColor Cyan
        $answer = Read-Host '>'
        if ($answer -eq 's') {
            Move-Item -LiteralPath $job.FullName -Destination (Join-Path $done ($job.BaseName + '.skipped.ps1')) -Force
            Write-Host '[skipped]' -ForegroundColor DarkYellow
            continue
        }
    }

    Set-LoopState "running $($job.Name)"
    $out = Join-Path $outbox ($job.BaseName + '.out.txt')
    "=== $($job.Name) started $stamp ===" | Set-Content -LiteralPath $out -Encoding utf8

    $code = 0
    try {
        & powershell -NoProfile -ExecutionPolicy Bypass -File $job.FullName *>&1 |
            Tee-Object -FilePath $out -Append |
            Write-Host
        $code = $LASTEXITCODE
        if ($null -eq $code) { $code = 0 }
    }
    catch {
        ($_ | Out-String) | Tee-Object -FilePath $out -Append | Write-Host
        $code = 1
    }

    "=== exit $code ===" | Add-Content -LiteralPath $out -Encoding utf8
    "=== finished $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Add-Content -LiteralPath $out -Encoding utf8

    Move-Item -LiteralPath $job.FullName -Destination (Join-Path $done $job.Name) -Force
    Set-LoopState 'idle'

    Write-Host ''
    Write-Host "[done] exit=$code  ->  outbox\$($job.BaseName).out.txt" -ForegroundColor Green
    Write-Host 'รอสคริปต์ถัดไป ...' -ForegroundColor DarkGray
}

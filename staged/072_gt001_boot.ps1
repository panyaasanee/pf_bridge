# Job 072 - GT-001 smoke boot (ATTENDED big round, main chat, Panya at machine).
# HEAD is f0e0ac6; GT-001 re-armed by 4c29a63 (M4 runtime hookup, src/) + 55c7c59 (store.py).
# Boot server + launch GameClient. The attended session then calls request_access
# (dialog WILL appear - not a scheduled run) and drives GT-001 per PLAYBOOK.
# NOTE rule R31: opening GameClient blocks the bridge until the window closes,
# so job 073 (teardown) must be queued behind this one and runs on window close.
# Lesson 27.2 applied: every path argument passed to a native command is quoted
# (folder names contain spaces). ASCII ONLY. Adapted from done\060_gt001_boot.ps1 (proven).

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$client = 'C:\Users\Panya\Desktop\Pirate Force\GameClient'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\072_gt001_boot.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== GT-001 BOOT (attended, job 072)  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$canon = Join-Path $main 'state\pirateforce.sqlite3'
$uri   = 'file:' + ($canon -replace '\\','/') + '?mode=ro'
# canonical sha as of 2026-08-17 post-GT-001(14:39) - see GAME_TEST_QUEUE GT-001 note
$shaFile = Join-Path $bridge 'CANON_SHA.txt'
if (-not (Test-Path -LiteralPath $shaFile)) { W 'ABORT: CANON_SHA.txt missing - cannot verify canonical DB'; exit 14 }
$expectedSha = ((Get-Content -LiteralPath $shaFile -Raw) -replace '[^0-9A-Fa-f]','').ToUpper()
if ($expectedSha.Length -ne 64) { W "ABORT: CANON_SHA.txt malformed (len=$($expectedSha.Length))"; exit 15 }
W "expected canonical sha (from CANON_SHA.txt) = $expectedSha"
# ---------- 1) mandatory DB backup + BEFORE snapshot ----------
if (-not (Test-Path -LiteralPath $canon)) { W 'ABORT: canonical DB missing'; exit 11 }
$sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha BEFORE = $sha"
if ($sha.ToUpper() -ne $expectedSha) { W 'ABORT: sha differs from canonical - stopping per GT rule'; exit 13 }
$bak = Join-Path $bridge "backup\pirateforce_before_gt001_$stamp.sqlite3"
Copy-Item -LiteralPath $canon -Destination $bak -Force
$bsha = (Get-FileHash -LiteralPath $bak -Algorithm SHA256).Hash
if ($bsha -ne $sha) { W 'ABORT: backup sha mismatch'; exit 12 }
W "backup ok: $bak"
W '--- DB BEFORE ---'
py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);[print('  BEFORE POS',r) for r in c.execute('SELECT c.id,c.name,p.scene_id,p.scene_seq,p.x,p.y,p.z,p.heading,p.updated_at FROM characters c JOIN character_positions p ON p.character_id=c.id')]" "$uri" 2>&1 | ForEach-Object { W $_ }
py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);print('  sessions with char   :',c.execute('select count(*) from sessions where selected_character_id is not null').fetchone()[0]);print('  sessions blank-conn  :',c.execute('select count(*) from sessions where selected_character_id is null').fetchone()[0]);print('  max lease_generation :',c.execute('select max(lease_generation) from sessions').fetchone()[0]);print('  backpack items       :',[tuple(r) for r in c.execute('select slot,item_identity,template_id,quantity from character_backpack_items order by slot')])" "$uri" 2>&1 | ForEach-Object { W $_ }

# ---------- 2) stop leftovers, boot server (visible console) ----------
$listen = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
if ($listen.Count -gt 0) {
    $oldPid = [int]$listen[0].OwningProcess
    W "old server still listening (pid $oldPid) - bounded Ctrl+C"
    $old = $null
    try { $old = [System.Diagnostics.Process]::GetProcessById($oldPid); $null = $old.Handle } catch {}
    $parent = (Get-CimInstance Win32_Process -Filter "ProcessId=$oldPid").ParentProcessId
    $target = $oldPid
    if ($parent) {
        $pp = Get-CimInstance Win32_Process -Filter "ProcessId=$parent" -ErrorAction SilentlyContinue
        if ($pp -and $pp.Name -eq 'py.exe') { $target = [int]$parent; W "  console owner is shim py.exe pid $target" }
    }
    & py -3 "$(Join-Path $bridge 'pf_stop_visible_server.py')" $target --json "$(Join-Path $bridge "outbox\072_ctrlc_old_$stamp.json")" | Out-Null
    W "  helper exit = $LASTEXITCODE"
    if ($old) { $null = $old.WaitForExit(20000); W "  old server exited: $($old.HasExited)" }
    Start-Sleep -Seconds 2
}
$listen = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
if ($listen.Count -gt 0) { W 'ABORT: ports still busy'; exit 10 }
W 'ports free'

$captureRoot = Join-Path $client "capture_gt001_$stamp"
Push-Location $main
$launch = & powershell -NoProfile -ExecutionPolicy Bypass `
    -File "$(Join-Path $main 'tools\run_foundation_visible.ps1')" `
    -Database 'state\pirateforce.sqlite3' -CaptureRoot "$captureRoot" -SecondPasswordMode bypass 2>&1
Pop-Location
$launch | ForEach-Object { W "  launcher> $_" }
$pidLine = $launch | Where-Object { $_ -match 'Visible Foundation console PID:\s*(\d+)' } | Select-Object -First 1
if (-not $pidLine) { W 'ABORT: no server PID'; exit 20 }
[int]$shimPid = $Matches[1]
$serverPid = $null
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $l = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
    if ($l.Count -ge 2) { $serverPid = [int]$l[0].OwningProcess; break }
}
if (-not $serverPid) { W 'ABORT: no listeners'; exit 21 }
W "SERVER UP shim=$shimPid server=$serverPid after ${i}s  captureRoot=$captureRoot"
"shim=$shimPid server=$serverPid captureRoot=$captureRoot stamp=$stamp" | Out-File -FilePath (Join-Path $bridge "outbox\072_server_info_$stamp.txt") -Encoding ascii

# ---------- 3) launch client redirected to files ----------
$cliOut = Join-Path $bridge "outbox\072_client_stdout_$stamp.txt"
$cliErr = Join-Path $bridge "outbox\072_client_stderr_$stamp.txt"
$p = Start-Process -FilePath "$(Join-Path $client 'GameClient.local.bin')" `
    -ArgumentList '-launchbypatcher','-subbuildversion','132','-acc','test','-pwd','test' `
    -WorkingDirectory $client `
    -RedirectStandardOutput $cliOut -RedirectStandardError $cliErr `
    -PassThru
W "client pid = $($p.Id) start=$($p.StartTime.ToString('HH:mm:ss'))"
$title = ''
for ($j = 0; $j -lt 60; $j++) {
    Start-Sleep -Seconds 1
    $p.Refresh()
    if ($p.HasExited) { W "client exited early code=$($p.ExitCode)"; break }
    if ($p.MainWindowTitle) { $title = $p.MainWindowTitle; W "window '$title' after ${j}s"; break }
}
"clientpid=$($p.Id) shim=$shimPid server=$serverPid stamp=$stamp title=$title" | Out-File -FilePath (Join-Path $bridge "outbox\072_client_info_$stamp.txt") -Encoding ascii
if (-not $title) { W 'WARN: no window title after 60s (client may still be loading)' }
W '=== 072 BOOT DONE - attended session takes over (request_access + UI) ==='

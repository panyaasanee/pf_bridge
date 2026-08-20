# ============================================================================
# TOOL_stop_stale_server.ps1 - free ports 10188/10189 when a round left a
# server running. ASCII ONLY.
#
# PROVENANCE: this is done\146_stop_stale_server.ps1, written under pressure
# during big round #6 (19 Aug, ~11:11) and PROVEN in that run. The body is
# unchanged except for the log/receipt file names, which no longer carry the
# job number 146. Nothing else was touched: do not "improve" the sequence
# without re-proving it on a live stuck server.
#
# WHEN TO USE IT
#   - a teardown exited 16 ("ports STILL BOUND")
#   - a teardown logged "skipped ctrl-c" and "AFTER listeners" > 0
#   - a boot job fails because 10188/10189 are already in use
#   - the attended session was interrupted and no teardown ever ran
#   Run it, confirm "FINAL listeners = 0", then boot the next round.
#
# WHAT IT DOES, AND WHY IN THIS ORDER
#   1. Lists the listeners on 10188/10189. If there are none it exits 0
#      immediately - it is safe to run speculatively before any boot.
#   2. For each port holder it resolves the PARENT process. The port is held
#      by the python server; its parent is the visible `py` launcher console.
#      Ctrl-C must go to the PARENT first - that is the path the server has a
#      handler for, so it shuts down gracefully and closes its DB cleanly.
#      Only if the parent does not free the port does it try the holder itself.
#   3. It re-checks the ports after every signal and stops as soon as they are
#      free, so it never signals more processes than necessary.
#   4. Force-kill is the LAST resort, after graceful ctrl-c has demonstrably
#      failed, and it is logged loudly as FALLBACK.
#   5. It exits NON-ZERO (12) if the ports are still bound at the end. A tool
#      whose only job is to free a port must never report success with the
#      port still bound.
#
# NOTE: it does NOT touch the canonical DB and does NOT read any info file -
# that is deliberate. It is the recovery path for exactly the situation where
# the info files can no longer be trusted.
# ============================================================================

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\TOOL_stop_stale_server.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== TOOL STOP STALE SERVER  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$listen = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
W "BEFORE listeners = $($listen.Count)"
if ($listen.Count -eq 0) { W 'nothing to do - ports already free'; W '=== TOOL DONE ==='; exit 0 }

$pids = @($listen | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique)
foreach ($p in $pids) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$p" -ErrorAction SilentlyContinue
    if (-not $proc) { W "listener pid=$p already gone"; continue }
    $parent = $proc.ParentProcessId
    W "listener pid=$p name=$($proc.Name) start=$($proc.CreationDate) parent=$parent"
    foreach ($target in @($parent, $p)) {
        $tp = Get-Process -Id $target -ErrorAction SilentlyContinue
        if (-not $tp) { continue }
        W "ctrl-c helper -> pid $target ($($tp.ProcessName))"
        & py -3 "$(Join-Path $bridge 'pf_stop_visible_server.py')" $target --json "$(Join-Path $bridge "outbox\TOOL_ctrlc_${target}_$stamp.json")" | Out-Null
        W "ctrl-c helper exit = $LASTEXITCODE"
        Start-Sleep -Seconds 4
        $still = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
        if ($still.Count -eq 0) { break }
    }
}

Start-Sleep -Seconds 3
$after = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
W "AFTER ctrl-c listeners = $($after.Count)"
if ($after.Count -gt 0) {
    $pids2 = @($after | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique)
    foreach ($p in $pids2) {
        W "FALLBACK Stop-Process -Id $p -Force (graceful ctrl-c did not free the port)"
        Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 3
}

$final = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
W "FINAL listeners = $($final.Count)"
$gc = @(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue)
W "GameClient processes = $($gc.Count)"
if ($final.Count -ne 0) { W 'ABORT: ports still busy'; exit 12 }
W '=== TOOL DONE ==='
exit 0

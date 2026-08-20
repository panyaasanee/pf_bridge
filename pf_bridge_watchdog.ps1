# PF Bridge Watchdog - runs every 5 minutes via Task Scheduler.
# If no pf_bridge.ps1 process is alive, start one HIDDEN (no window = nothing
# to accidentally click into Select mode = no more QuickEdit freezes).
# Logs starts to watchdog.log. ASCII only.
#
# 2026-08-19 (chief round 89) - A FROZEN BRIDGE IS NOW ALSO A DEAD BRIDGE.
# At ~16:51 a bridge process stayed alive while its loop stopped: job 906 ran,
# its output was written, the file was never moved to done\, and nothing was
# picked up for the next forty minutes - while this watchdog wrote "bridge-alive"
# every five minutes, because the PROCESS was there.  "Process exists" and "loop
# turns" are different claims and only the second one is the one that matters.
# pf_bridge.ps1 now rewrites bridge_loop_state.txt on every poll and around every
# job, so this script can tell them apart:
#   "idle <ts>"          the loop is turning.  Stale for > IDLE_STALE_MIN => frozen.
#   "running <job> <ts>" a job is IN FLIGHT.  Never killed before RUN_STALE_MIN,
#                        which is deliberately generous: the full gate plus the
#                        test suite takes about six minutes on this machine.
# A frozen bridge is stopped and replaced by a hidden one, and the reason is
# written to watchdog.log.  If the state file is missing (an older bridge, or one
# that has not polled yet) NOTHING is killed - absence of evidence is not evidence.

$ErrorActionPreference = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$script = Join-Path $bridge 'pf_bridge.ps1'
$logf   = Join-Path $bridge 'watchdog.log'
$statef = Join-Path $bridge 'bridge_loop_state.txt'
$IDLE_STALE_MIN = 12
$RUN_STALE_MIN  = 25

function Log($m) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $m" |
        Out-File -FilePath $logf -Encoding ascii -Append
}

# Is a bridge already running? (visible one started by hand counts too)
$alive = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
    Where-Object { $_.CommandLine -like '*pf_bridge.ps1*' })

# --- is the LOOP turning, not just the process? -----------------------------
$frozen = $false
$why    = ''
if ($alive.Count -gt 0 -and (Test-Path -LiteralPath $statef)) {
    $raw = (Get-Content -LiteralPath $statef -Raw -ErrorAction SilentlyContinue)
    if ($raw) {
        $raw = $raw.Trim()
        $ts = $null
        if ($raw -match '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*$') {
            $ts = [datetime]::ParseExact($matches[1], 'yyyy-MM-dd HH:mm:ss', $null)
        }
        if ($ts) {
            $ageMin = [math]::Round(((Get-Date) - $ts).TotalMinutes, 1)
            if ($raw -like 'running*') {
                if ($ageMin -gt $RUN_STALE_MIN) {
                    $frozen = $true
                    $why = "loop state '$raw' is $ageMin min old (> $RUN_STALE_MIN) - job wedged"
                }
            } else {
                if ($ageMin -gt $IDLE_STALE_MIN) {
                    $frozen = $true
                    $why = "loop state '$raw' is $ageMin min old (> $IDLE_STALE_MIN) - loop stopped"
                }
            }
        }
    }
}

# --- second signal: is the INBOX draining? ----------------------------------
# The state file only exists on bridges started after 2026-08-19; the instance
# that froze at 16:51 was older than the patch, so "no state file" must not mean
# "assume healthy" forever.  Draining the inbox is the bridge's entire job, so a
# .ps1 that has sat there longer than OLD_INBOX_STALE_MIN with no bridge claiming
# to be running one is a stopped loop no matter what the process table says.  The
# threshold is deliberately twice the idle one, because on an old bridge a long
# job and a wedged loop look identical from outside.
$OLD_INBOX_STALE_MIN = 25
if ($alive.Count -gt 0 -and -not $frozen) {
    $stateSaysRunning = $false
    if (Test-Path -LiteralPath $statef) {
        $rawNow = (Get-Content -LiteralPath $statef -Raw -ErrorAction SilentlyContinue)
        if ($rawNow -and $rawNow.Trim() -like 'running*') { $stateSaysRunning = $true }
    }
    if (-not $stateSaysRunning) {
        $oldest = Get-ChildItem -Path (Join-Path $bridge 'inbox') -Filter '*.ps1' -File -ErrorAction SilentlyContinue |
                  Sort-Object LastWriteTime | Select-Object -First 1
        if ($oldest) {
            $waitMin = [math]::Round(((Get-Date) - $oldest.LastWriteTime).TotalMinutes, 1)
            if ($waitMin -gt $OLD_INBOX_STALE_MIN) {
                $frozen = $true
                $why = "inbox\$($oldest.Name) has waited $waitMin min (> $OLD_INBOX_STALE_MIN) and no job is claimed running - loop stopped"
            }
        }
    }
}

# --- heartbeat (added 2026-08-19, attended session) ---
# Overwrites one small file every run. Lets anyone tell "watchdog ran and the
# bridge was fine" apart from "watchdog never ran" - watchdog.log alone cannot,
# because it only gets a line when a bridge is actually (re)started.
$hbf = Join-Path $bridge 'watchdog_last_check.txt'
$hbState = if ($frozen) { 'bridge-frozen-restarting' }
           elseif ($alive.Count -gt 0) { 'bridge-alive' }
           else { 'bridge-missing-starting' }
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $hbState" |
    Out-File -FilePath $hbf -Encoding ascii

if ($alive.Count -gt 0 -and -not $frozen) { exit 0 }

if ($frozen) {
    Log "FROZEN BRIDGE: $why"
    foreach ($p in $alive) {
        Log "  stopping pid $($p.ProcessId) (started $($p.CreationDate))"
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    $still = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
        Where-Object { $_.CommandLine -like '*pf_bridge.ps1*' })
    if ($still.Count -gt 0) {
        Log "  WARN: $($still.Count) bridge process(es) survived the stop - not starting a second one"
        exit 1
    }
}

Start-Process -FilePath 'powershell.exe' `
    -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',('"' + $script + '"') `
    -WorkingDirectory $bridge -WindowStyle Hidden
if ($frozen) {
    Log 'bridge was frozen - replaced with a hidden instance'
} else {
    Log 'bridge not found - started hidden instance'
}

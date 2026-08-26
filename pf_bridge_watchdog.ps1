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

# --- sync health (added 2026-08-26, COO / OPS-001) ---------------------------
# THE GAP THIS CLOSES.  On the night of 25 Aug the git sync stopped at 23:53 and
# nobody noticed for 25 minutes.  One tracked file was missing from the worktree,
# so `rebase` refused, so NOT ONE LETTER from any lane reached chief for the whole
# window - and from outside it looked completely normal: the bridge was alive, the
# task was running, the log was being written.  Silence and health are identical
# from a distance, which is exactly why this has to be checked and not assumed.
#
# This watchdog knew nothing about the sync (grep 'sync' returned 0 hits) even
# though it is the only thing on this machine that runs unattended every 5 minutes.
# It does now.  It REPAIRS exactly one failure - the stale index.lock, which has
# happened twice and has a mechanical fix - and otherwise only makes the failure
# LOUD.  Anything needing judgement (a deleted tracked file, a real conflict) is
# left for a person: a watchdog that guesses at git is worse than a stopped sync.
$SYNC_STALE_MIN = 12          # the sync task repeats every 2 minutes
$syncState = Join-Path $bridge 'sync_last_check.txt'
$attn      = Join-Path $bridge 'SYNC_ATTENTION.txt'
if (Test-Path -LiteralPath $syncState) {
    $sraw = (Get-Content -LiteralPath $syncState -Raw -ErrorAction SilentlyContinue)
    if ($sraw -and $sraw -match '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})') {
        $sts = [datetime]::ParseExact($matches[1], 'yyyy-MM-dd HH:mm:ss', $null)
        $sAge = [math]::Round(((Get-Date) - $sts).TotalMinutes, 1)
        if ($sAge -gt $SYNC_STALE_MIN) {
            Log "SYNC STALE: sync_last_check.txt is $sAge min old (> $SYNC_STALE_MIN)"

            # The one repair this is allowed to make.  A 0-byte index.lock with no
            # git process alive is a corpse, not a lock - it is what a git command
            # killed by a timeout leaves behind on the mounted worktree.
            $lock = Join-Path $bridge '.git\index.lock'
            if (Test-Path -LiteralPath $lock) {
                $gitAlive = @(Get-Process -Name 'git' -ErrorAction SilentlyContinue).Count
                $lockAge  = [math]::Round(((Get-Date) - (Get-Item -LiteralPath $lock).LastWriteTime).TotalMinutes, 1)
                if ($gitAlive -eq 0 -and $lockAge -gt 3) {
                    $dest = Join-Path $bridge ('_to_delete\stale_index_lock_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
                    New-Item -ItemType Directory -Path $dest -Force | Out-Null
                    Move-Item -LiteralPath $lock -Destination $dest -Force
                    Log "  REPAIRED: moved a $lockAge min old index.lock aside (no git process alive) -> $dest"
                } else {
                    Log "  index.lock present but NOT touched: gitProcesses=$gitAlive lockAge=$lockAge min"
                }
            }

            # Make it loud either way.  This file is what a human or the COO round
            # sees; the repair above only covers one of several ways to get here.
            @(
                "SYNC STALE as of $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') (+07:00)",
                "sync_last_check.txt is $sAge minutes old; the task repeats every 2 minutes.",
                "Nothing written by any lane has reached chief since then.",
                "Look at the tail of sync.log - the usual causes are:",
                "  STOP_DIRTY_WORKTREE_BLOCKS_REBASE  a tracked file was changed or deleted in the worktree",
                "  SKIP_INDEX_LOCK                    a git command died and left .git/index.lock behind",
                "This watchdog repairs only the second one, and only when no git process is alive."
            ) | Out-File -FilePath $attn -Encoding ascii
        } else {
            # Clear ONLY an alert this watchdog wrote.  pf_git_sync writes and clears
            # SYNC_ATTENTION.txt for its own reasons; deleting someone else's alert
            # because our own check happens to be green would erase a live warning.
            if (Test-Path -LiteralPath $attn) {
                $first = (Get-Content -LiteralPath $attn -TotalCount 1 -ErrorAction SilentlyContinue)
                if ($first -match '^SYNC STALE as of') {
                    Remove-Item -LiteralPath $attn -Force -ErrorAction SilentlyContinue
                    Log 'sync healthy again - cleared the watchdog SYNC_ATTENTION alert'
                }
            }
        }
    }
} else {
    Log 'SYNC STATE MISSING: sync_last_check.txt not found - the sync task may never have run'
}

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

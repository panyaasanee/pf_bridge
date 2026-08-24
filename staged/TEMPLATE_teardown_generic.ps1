# ============================================================================
# TEMPLATE_teardown_generic.ps1 - generic attended-round teardown (ASCII ONLY)
#
# WHY THIS FILE EXISTS - THE BUG IT REPLACES
# ------------------------------------------
# Every teardown job used to locate the boot job's "client info file" with a
# glob that had the BOOT JOB NUMBER baked into it, e.g.
#
#     Get-ChildItem $outbox -Filter '132_client_info_*.txt'
#
# New rounds were produced by copy+sed of the previous round's pair. The sed
# renamed the log file and the job header, but NOT that glob. Job 145
# (GT-021, big round #6, 11:09) therefore parsed 132_client_info_* - the info
# file of a round that had ended six hours earlier. Consequences, in order:
#
#   1. PIDs read from the stale file pointed at long-dead processes.
#   2. The identity/time-window PID guard correctly said "not my process".
#   3. The guard's else-branch only LOGGED 'skipped ctrl-c' and kept going.
#   4. The server of the CURRENT round was never signalled. Ports 10188/10189
#      stayed bound ("AFTER listeners = 2" in 145_gt021_teardown.utf8.txt).
#   5. The job still exited 0, so nothing looked wrong until the NEXT boot
#      failed on a busy port and an emergency job (146_stop_stale_server.ps1)
#      had to be written by hand mid-round.
#
# The same copy+sed hazard hit sibling lines: 145 wrote its ctrl-c receipt as
# '133_ctrlc_*.json', and 127_gt016_teardown.ps1 in staged\ still globs
# '124_client_info_*' although its boot partner 126 writes '126_client_info_*'.
#
# HOW THIS TEMPLATE FIXES IT
# --------------------------
# (a) NO JOB NUMBER ANYWHERE. The info file is found as "the newest file in
#     outbox\ matching *_client_info_*.txt". Log and receipt names are derived
#     from this script's OWN filename, so renaming the file renames its
#     outputs - a sed can no longer desynchronise them.
#
#     Why newest-wins and not a -Prefix parameter as the primary mechanism:
#     pf_bridge.ps1 launches jobs as `powershell -File <job>.ps1` with NO
#     arguments (see pf_bridge.ps1). A parameter would still have to be
#     hardcoded inside the copied file - i.e. exactly the surface that broke.
#     Auto-discovery cannot go stale by copy-paste. Concurrency is not a risk:
#     the server is strictly serial (FINDINGS_R18), so at most one attended
#     round is live at a time. -ExpectInfoPrefix is still available, but only
#     as an ASSERTION: if the newest file does not match it the job ABORTS.
#     It never silently selects an older file.
#
# (b) FAIL CLOSED, ALWAYS. Missing info file, stale info file, missing/empty
#     key, pid <= 0, unparsable stamp, guard mismatch, or ports still bound at
#     the end -> loud message + NON-ZERO exit. There is no path that skips the
#     ctrl-c step and still reports success. That silent skip was the bug.
#
# (c) THE SIGNAL TARGET IS VERIFIED AGAINST LIVE TOPOLOGY, not just against
#     the info file. Ctrl-C goes to the PARENT of the process that actually
#     holds the port (the `py` launcher console) - the technique proven by the
#     emergency job 146. If the console pid from the info file is not the
#     parent of the current port holder, that means the info file belongs to a
#     different round: ABORT rather than signal a stranger.
#
# (d) -Salvage: A REFUSAL MUST NOT DESTROY EVIDENCE (added 2026-08-20).
#     On 2026-08-20 an attended round ran 3+ hours and then simply stopped,
#     because the human driving it walked away. Nobody ran the teardown. When
#     someone finally tried, this template refused with
#         exit 12  "boot stamp is 185.7 min old (> 180) - stale round"
#     and that refusal is CORRECT as a default: a teardown that runs hours late
#     would stamp fresh-looking evidence onto a round that has gone cold, and a
#     late ctrl-c could hit a process that no longer belongs to that round.
#     But the refusal also threw away evidence THAT WAS STILL ON THE DISK -
#     the server console log, the run-copy DB, the capture tree. That is the
#     bug this switch fixes. -Salvage turns the refusal into a COLLECTION:
#     read-only, kills nothing, writes to no database, and produces a receipt
#     whose filename and first line both say SALVAGE, whose header states the
#     real age and that no teardown ever ran, and which lists WHAT IS MISSING
#     rather than only what was found. An honest gap list is the entire point.
#     A salvage receipt that reads like a normal receipt is worse than none.
#
#     -Salvage NEVER performs a teardown. It never signals, never force-kills,
#     never frees a port, never opens a DB with sqlite, never writes anywhere
#     except outbox\SALVAGE_*. If the ports are still bound it SAYS SO and
#     tells you to run staged\TOOL_stop_stale_server.ps1 yourself.
#
# TRAPS DELIBERATELY GUARDED HERE
#   - stale info file (the 145 bug)                        -> exit 11/12
#   - info file from a different round than the live server -> exit 15
#   - PID 0 / System Idle from a bad cast (old job 069 bug) -> exit 14
#   - path-with-spaces split (JOB_INFO_FILE_CONVENTION.md)  -> first-'=' parse
#                                                              + quoted args
#   - "green log, busy port" (the real damage of 145)       -> exit 16
#   - hardcoded expected canonical sha going stale (151 log
#     compared against a sha that had not been current for
#     days)                                                 -> read CANON_SHA.txt
#   - a refusal that silently destroys recoverable evidence  -> -Salvage
#
# USAGE
#   Copy to inbox\<NNN>_<gtid>_teardown.ps1. Adjust the CaptureFilter default
#   (or pass -CaptureFilter) and, if the round needs extra evidence greps, add
#   them in section 4. Do NOT reintroduce a job number in any glob.
#   Better: let the boot job write the paired teardown for you - see
#   staged\TEMPLATE_boot_writes_paired_teardown.ps1, which fills in the job
#   number, boot stamp, scenario and run-DB path at boot time so that closing
#   the round is one copy into inbox\ with nothing left to remember.
#   To salvage a round that was never closed, see HOWTO_SALVAGE_A_DEAD_ROUND.md.
#
# EXIT CODES
#   0  ok                     11 no client info file found
#   12 info file too old      13 required key missing or empty
#   14 pid <= 0 / bad stamp    15 guard mismatch - refuse to signal
#   16 ports still bound      17 canonical DB moved
#   20 SALVAGE receipt written - round is DEGRADED, this is NOT a green round
#   21 -Salvage could not write a receipt at all
# ============================================================================

param(
    # Assertion only. Empty = accept whatever the newest info file is.
    [string]  $ExpectInfoPrefix     = '',
    # Assertion only. Empty = accept whatever boot stamp the info file carries.
    # Set by the auto-written paired teardown so that a teardown belonging to
    # round A physically cannot tear down round B.
    [string]  $ExpectBootStamp      = '',
    # Anything older than this is treated as a leftover, not as this round.
    #
    # RAISED FROM 180 TO 420 ON 2026-08-20. 180 min was simply too tight for
    # this project: attended rounds of 2 to 3 hours are normal, and the round
    # that exposed this was refused at 185.7 min - i.e. the limit fired on a
    # round that had ended NORMALLY, only late. 420 = a 3-hour attended round
    # plus up to 4 hours before somebody gets back to the machine and closes
    # it. Beyond that the round really is cold and the operator should think.
    #
    # Raising it does NOT weaken the anti-145 protection, and that is why it is
    # safe to raise. The age limit was never the guard that caught a stale info
    # file: the guards that do that are (i) exit 15, which requires the console
    # pid from the info file to be the ACTUAL PARENT of the process holding the
    # port right now - a live-topology fact with no clock in it at all - and
    # (ii) the identity/time-window check, which is anchored to the boot stamp
    # in the info file and is unaffected by this number. The age limit is only
    # a cheap early hint. Keep it, but do not let it be the thing that decides.
    [int]     $MaxInfoAgeMinutes    = 420,
    [int[]]   $Ports                = @(10188, 10189),
    # Capture root to harvest, e.g. 'capture_gt015_*'.
    [string]  $CaptureFilter        = 'capture_*',
    # Last resort only. Default OFF: a stuck port should be visible, not hidden.
    [switch]  $ForceKillIfPortsStuck,
    # COLLECT-ONLY MODE. Never signals, never kills, never writes a DB. See (d).
    # -Salvage always wins: if it is present, no teardown is attempted at all,
    # whatever the age of the round. A fresh round + -Salvage is a legitimate
    # "take a look without closing anything" and must not fall through into the
    # kill path.
    [switch]  $Salvage,
    # Output naming only. Empty = derive from this script's filename (the
    # default, and the thing that makes copy+sed safe). NEVER used to FIND
    # anything - reintroducing a job number into a GLOB is the 145 bug.
    [string]  $JobTag               = '',
    # Roots. These exist ONLY so staged\SELFTEST_teardown_salvage.ps1 can run
    # this entire file against a throwaway sandbox under %TEMP%. A real job must
    # not pass them: the defaults are the real machine.
    [string]  $BridgeRoot = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge',
    [string]  $MainRoot   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject',
    [string]  $ClientRoot = 'C:\Users\Panya\Desktop\Pirate Force\GameClient'
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

$bridge = $BridgeRoot
$main   = $MainRoot
$client = $ClientRoot
$outbox = Join-Path $bridge 'outbox'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'

# Job tag comes from THIS FILE'S NAME - never from a hardcoded number.
$jobTag = ''
if (-not [string]::IsNullOrWhiteSpace($JobTag)) {
    $jobTag = $JobTag
} elseif ($MyInvocation.MyCommand.Path) {
    $jobTag = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Path)
}
if ([string]::IsNullOrWhiteSpace($jobTag)) { $jobTag = 'teardown_generic' }

if (-not (Test-Path -LiteralPath $outbox)) {
    New-Item -ItemType Directory -Path $outbox -ErrorAction SilentlyContinue | Out-Null
}

$log = Join-Path $outbox ($jobTag + '.utf8.txt')
function W($m) {
    $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"
    $l | Out-File -FilePath $log -Encoding utf8 -Append
    Write-Host $l
}
"=== $jobTag TEARDOWN  $stamp ===" | Out-File -FilePath $log -Encoding utf8
W "job tag derived from filename = $jobTag"
W "ports watched = $($Ports -join ',')"
W "age limit = $MaxInfoAgeMinutes min"
if ($Salvage) { W 'MODE = SALVAGE (collect only: no signal, no kill, no DB write, no port freed)' }

function Fail($msg, $code) {
    W "ABORT($code): $msg"
    W "=== $jobTag TEARDOWN FAILED (exit $code) ==="
    exit $code
}

# ---------- BOM-free writer -------------------------------------------------
# Round 109: Out-File -Encoding utf8 on Windows PowerShell 5.1 prepends a UTF-8
# BOM, and every downstream '^SOMETHING' regex then silently fails to match.
# The project's one correct writer lives in staged\TEMPLATE_lock_flag_helpers.ps1
# (Write-Flag). Use it rather than re-deriving it - re-deriving is how the BOM
# bug spread through jobs 160-175 in the first place.
#
# BUT THE DOT-SOURCE IS DELIBERATELY NOT AT SCRIPT SCOPE. Dot-sourcing runs the
# other file's top-level statements in THIS scope, and that file ends with a
# self-test block whose last statement is `exit`. It is guarded by
# `if ($MyInvocation.InvocationName -ne '.')`, which is correct for a dot-source
# - but if that guard ever stopped holding, an unconditional dot-source at the
# top of this file would make EVERY teardown exit before doing anything, and it
# would exit 0. So the dot-source happens inside Invoke-Salvage only: the one
# path that staged\SELFTEST_teardown_salvage.ps1 actually executes end-to-end,
# where a premature exit shows up immediately as "no receipt, exit 0" instead of
# 20. Nothing in the normal teardown path dot-sources anything.
#
# The inline fallback exists so that a salvage still produces a receipt on a
# machine where staged\ is incomplete: a salvage that refused to write because a
# helper was missing would repeat the exact failure this switch was built to end.
$flagHelpers = Join-Path $bridge 'staged\TEMPLATE_lock_flag_helpers.ps1'
function Write-AsciiLines($Path, $Lines) {
    if (Get-Command -Name 'Write-Flag' -ErrorAction SilentlyContinue) {
        try { Write-Flag -Path $Path -Lines $Lines; return } catch { }
    }
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($Path, $Lines, $enc)
}

# ============================================================================
# SALVAGE
# ============================================================================
# Reads and copies. Nothing else. Every statement in this function is one of:
# Get-ChildItem / Get-Content / Get-Item / Get-FileHash / Get-NetTCPConnection /
# Get-CimInstance / Get-Process, plus writing the receipt and the console tail
# into outbox\. There is deliberately NO Stop-Process, NO CloseMainWindow, NO
# pf_stop_visible_server.py call, NO sqlite connection (not even read-only: the
# point is that this function cannot possibly be the thing that damaged a DB),
# and NO write anywhere near $main\state.
function Invoke-Salvage($InfoFile, $Kv, $BootTime, $Why) {
    # The only dot-source in this file, and it is on the salvage path only - see
    # the note above Write-AsciiLines for why it is not at script scope. The
    # functions it defines land in THIS scope, which is a parent scope of every
    # call made from here, so Write-AsciiLines can see Write-Flag.
    if (Test-Path -LiteralPath $flagHelpers) { . $flagHelpers }
    $now   = Get-Date
    if ($null -eq $Kv) { $Kv = @{} }
    $found = New-Object System.Collections.ArrayList
    $miss  = New-Object System.Collections.ArrayList
    function F($line) { $null = $found.Add($line) }
    function M($line) { $null = $miss.Add('MISSING: ' + $line) }

    # ---- identity of the round --------------------------------------------
    $infoName    = 'ABSENT'
    $infoAgeTxt  = 'UNKNOWN (no client info file)'
    if ($InfoFile) {
        $infoName   = $InfoFile.Name
        $infoAgeTxt = ('{0} min' -f [math]::Round(($now - $InfoFile.LastWriteTime).TotalMinutes, 1))
    }
    $bootStampTxt = 'UNKNOWN'
    if ($Kv.ContainsKey('stamp') -and -not [string]::IsNullOrWhiteSpace($Kv['stamp'])) {
        $bootStampTxt = $Kv['stamp']
    }
    $bootAgeTxt = 'UNKNOWN'
    if ($BootTime) {
        $bootAgeTxt = ('{0} min' -f [math]::Round(($now - $BootTime).TotalMinutes, 1))
    }

    if (-not $InfoFile) {
        M 'client info file (outbox\*_client_info_*.txt) - the boot job never wrote one, or it was removed. Without it the client/console/server pids, the boot stamp and the run-copy DB path are all unknown and cannot be reconstructed.'
    }
    if (-not $BootTime) {
        M "parseable boot stamp (yyyyMMdd_HHmmss) - the real start time of this round is not recoverable, so nothing below can be time-anchored to it."
    }
    foreach ($k in @('clientpid', 'console', 'server')) {
        if (-not $Kv.ContainsKey($k) -or [string]::IsNullOrWhiteSpace($Kv[$k])) {
            M "info key '$k' - the $k pid of this round is unknown."
        }
    }

    # ---- did a teardown ever run for this round? --------------------------
    # Stated as a measurement, not as an assumption: look for any teardown log
    # in outbox\ written after the boot stamp.
    $tdLogs = @()
    if ($BootTime) {
        $tdLogs = @(Get-ChildItem -LiteralPath $outbox -Filter '*teardown*.utf8.txt' -File -ErrorAction SilentlyContinue |
                    Where-Object { $_.LastWriteTime -ge $BootTime -and $_.Name -ne ($jobTag + '.utf8.txt') })
    }
    F "teardown logs in outbox newer than the boot stamp : $($tdLogs.Count)"
    foreach ($t in $tdLogs) { F "  teardown log seen: $($t.Name)  $($t.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))" }
    if ($tdLogs.Count -eq 0) {
        M 'the teardown receipt for this round - no teardown log for this round exists in outbox at all. Everything a teardown records at the moment a round ends was never recorded.'
    }
    $ctrlc = @(Get-ChildItem -LiteralPath $outbox -Filter '*_ctrlc_*.json' -File -ErrorAction SilentlyContinue |
               Where-Object { -not $BootTime -or $_.LastWriteTime -ge $BootTime })
    F "ctrl-c receipts newer than the boot stamp        : $($ctrlc.Count)"
    if ($ctrlc.Count -eq 0) {
        M 'graceful-shutdown proof (*_ctrlc_*.json) - the server of this round was never signalled by this protocol, so there is no evidence it closed its DB cleanly.'
    }

    # ---- listeners RIGHT NOW (not freed - salvage never frees a port) -----
    $lis = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
             Where-Object { $Ports -contains [int]$_.LocalPort })
    F "listeners on $($Ports -join ',') AT SALVAGE TIME : $($lis.Count)"
    foreach ($l in $lis) {
        $nm = ''
        $ci = Get-CimInstance Win32_Process -Filter "ProcessId=$($l.OwningProcess)" -ErrorAction SilentlyContinue
        if ($ci) { $nm = "name=$($ci.Name) parent=$($ci.ParentProcessId) started=$($ci.CreationDate)" }
        F "  listener port=$($l.LocalPort) owningPid=$($l.OwningProcess) $nm"
    }
    if ($lis.Count -gt 0) {
        F '  NOTE: the ports are STILL BOUND. Salvage did not free them and will not.'
        F '  NOTE: run staged\TOOL_stop_stale_server.ps1 before the next boot.'
        F '  NOTE: the server may therefore STILL BE WRITING to the console log and'
        F '        the run DB below, so their sizes/hashes are a snapshot, not a final state.'
    }
    $gc = @(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue)
    F "GameClient processes AT SALVAGE TIME              : $($gc.Count)"
    M 'the end-of-round listener and process state - only the state AT SALVAGE TIME (above) could be observed. Whether the client exited by itself, whether the server shut down cleanly, and when, are not recoverable.'

    # ---- capture root and the server console log ---------------------------
    $capRoot = $null
    if (Test-Path -LiteralPath $client) {
        $capRoot = Get-ChildItem -LiteralPath $client -Directory -Filter $CaptureFilter -ErrorAction SilentlyContinue |
                   Sort-Object Name | Select-Object -Last 1
    }
    $consoleLog = $null
    if ($capRoot) {
        F "capture root : $($capRoot.FullName)"
        $allCap = @(Get-ChildItem -Recurse -File -LiteralPath $capRoot.FullName -ErrorAction SilentlyContinue)
        F "capture files: $($allCap.Count)"
        foreach ($g in ($allCap | Sort-Object Length -Descending | Select-Object -First 12)) {
            F "  cap: $($g.FullName.Substring($capRoot.FullName.Length + 1)) bytes=$($g.Length) mtime=$($g.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
        }
        if ($allCap.Count -eq 0) { M "capture files - the capture root '$($capRoot.Name)' exists but is empty." }
        foreach ($want in @('GAME_LIVE.txt', 'GAME_EVENTS_LIVE.txt')) {
            $hits = @($allCap | Where-Object { $_.Name -eq $want })
            if ($hits.Count -eq 0) { M "$want - no wire log of that name under the capture root." }
            else { foreach ($h in $hits) { F "  $($want): $($h.FullName.Substring($capRoot.FullName.Length + 1)) bytes=$($h.Length)" } }
        }
        $top = Join-Path $capRoot.FullName 'server_console_live.out.txt'
        if (Test-Path -LiteralPath $top) {
            $consoleLog = Get-Item -LiteralPath $top
        } else {
            $consoleLog = $allCap | Where-Object { $_.Name -eq 'server_console_live.out.txt' } | Select-Object -First 1
        }
    } else {
        F "capture root : NOT FOUND (filter '$CaptureFilter' under $client)"
        M "capture root (filter '$CaptureFilter') - the whole capture tree of this round is not on disk, so no wire-side evidence exists."
    }

    if ($consoleLog) {
        F "server console log : $($consoleLog.FullName)"
        F "  bytes = $($consoleLog.Length)  mtime = $($consoleLog.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
        $txt = ''
        try { $txt = Get-Content -Raw -Encoding utf8 -LiteralPath $consoleLog.FullName -ErrorAction Stop }
        catch { $txt = ''; F "  READ FAILED: $($_.Exception.Message)" }
        if ($txt) {
            F "  traceback markers = $(([regex]::Matches($txt, 'Traceback')).Count)"
            F "  'listener ready'   = $(([regex]::Matches($txt, 'listener ready')).Count)"
            F "  '[FOUNDATION] stopped' = $(([regex]::Matches($txt, '\[FOUNDATION\] stopped')).Count)"
            $tailFile = Join-Path $outbox ('SALVAGE_' + $jobTag + '_console_tail_' + $stamp + '.txt')
            $tail = ($txt -split "`r?`n" | Select-Object -Last 400)
            Write-AsciiLines $tailFile (@(
                'SALVAGE console tail - last 400 lines, recovered after the fact',
                "source: $($consoleLog.FullName)",
                "copied: $($now.ToString('yyyy-MM-dd HH:mm:ss'))",
                '----------------------------------------------------------------'
            ) + $tail)
            F "  tail (last 400 lines) copied to: $(Split-Path -Leaf $tailFile)"
        } else {
            M 'readable content of the server console log - the file is present but could not be read or is empty.'
        }
    } else {
        F 'server console log : NOT FOUND'
        M 'the server console log (server_console_live.out.txt) - no server-side console tail and no traceback count are possible for this round.'
    }

    # ---- run-copy DB: file facts only. No sqlite. No open. ----------------
    $runDb = ''
    if ($Kv.ContainsKey('rundb')) { $runDb = $Kv['rundb'] }
    if ([string]::IsNullOrWhiteSpace($runDb)) {
        F 'run-copy DB : NOT DECLARED (no rundb key)'
        M "the run-copy DB path - the info file does not declare 'rundb', so which DB file this round used cannot be established."
    } elseif (Test-Path -LiteralPath $runDb) {
        $d = Get-Item -LiteralPath $runDb
        F "run-copy DB : $($d.FullName)"
        F "  bytes = $($d.Length)  mtime = $($d.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
        try {
            $h = (Get-FileHash -LiteralPath $runDb -Algorithm SHA256 -ErrorAction Stop).Hash.ToUpper()
            F "  sha256 = $h"
        } catch {
            F "  sha256 = UNAVAILABLE ($($_.Exception.Message))"
            M 'a sha256 of the run-copy DB - the file is present but could not be hashed (most likely still open by a live server).'
        }
        foreach ($sfx in @('-wal', '-shm')) {
            $f = $runDb + $sfx
            if (Test-Path -LiteralPath $f) { F "  $sfx present, $((Get-Item -LiteralPath $f).Length) bytes (uncheckpointed data may still be outside the main file)" }
            else { F "  $sfx absent" }
        }
    } else {
        F "run-copy DB : DECLARED BUT NOT ON DISK -> $runDb"
        M "the run-copy DB file ($runDb) - declared by the boot job but not present now, so no post-run DB state of any kind survives."
    }
    M 'the end-of-round DB snapshot - a teardown records session counts, lease generation, integrity_check and foreign_key_check AT THE MOMENT THE ROUND ENDS. That measurement was never taken and cannot be taken now: at best the file above shows the state at salvage time, after an unknown amount of drift.'

    # ---- client stdout/stderr ---------------------------------------------
    $cliFiles = @(Get-ChildItem -LiteralPath $outbox -File -ErrorAction SilentlyContinue |
                  Where-Object { $_.Name -like '*_client_std*' -and (-not $BootTime -or $_.LastWriteTime -ge $BootTime.AddMinutes(-5)) })
    F "client stdout/stderr files for this round        : $($cliFiles.Count)"
    foreach ($c in $cliFiles) { F "  $($c.Name) bytes=$($c.Length)" }
    if ($cliFiles.Count -eq 0) { M 'client stdout/stderr capture - no *_client_std* file from this round is in outbox.' }

    # ---- canonical DB: hash only, read-only, never touched ----------------
    $canon = Join-Path $main 'state\pirateforce.sqlite3'
    if (Test-Path -LiteralPath $canon) {
        try {
            $sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256 -ErrorAction Stop).Hash.ToUpper()
            F "canonical DB sha256 now : $sha"
            $shaFile = Join-Path $bridge 'CANON_SHA.txt'
            if (Test-Path -LiteralPath $shaFile) {
                $expected = ((Get-Content -LiteralPath $shaFile -Raw) -replace '[^0-9A-Fa-f]', '').ToUpper()
                F "canonical DB sha256 expected (CANON_SHA.txt) : $expected"
                if ($sha -eq $expected) { F 'canonical guard: UNCHANGED (this round did not touch the canonical DB)' }
                else { F 'canonical guard: RED - the canonical DB DIFFERS from CANON_SHA.txt. Investigate before the next round.' }
            } else {
                F 'canonical DB expected sha : CANON_SHA.txt MISSING'
                M 'the canonical-DB comparison - CANON_SHA.txt is missing, so it cannot be shown that this round left the canonical DB alone.'
            }
        } catch {
            F "canonical DB sha256 : UNAVAILABLE ($($_.Exception.Message))"
            M 'the canonical-DB hash - the file could not be read.'
        }
    } else {
        F "canonical DB : NOT FOUND at $canon"
        M 'the canonical DB itself - it is not at the expected path.'
    }

    # ---- assemble the receipt ---------------------------------------------
    $head = @(
        'SALVAGE RECEIPT - DEGRADED EVIDENCE - THIS IS NOT A TEARDOWN RECEIPT',
        '====================================================================',
        '',
        "salvage_written_at    : $($now.ToString('yyyy-MM-dd HH:mm:ss'))",
        "salvage_job_tag       : $jobTag",
        "salvage_reason        : $Why",
        "age_limit_in_force    : $MaxInfoAgeMinutes min",
        "boot_stamp            : $bootStampTxt",
        "boot_age_at_salvage   : $bootAgeTxt",
        "info_file             : $infoName",
        "info_file_age         : $infoAgeTxt",
        "teardown_logs_found   : $($tdLogs.Count)",
        "missing_items         : PLACEHOLDER",
        '',
        'WHAT THIS FILE IS',
        '-----------------',
        'NO TEARDOWN EVER RAN FOR THIS ROUND at the time the round ended. Nobody',
        'closed it. This file was produced afterwards by',
        '    TEMPLATE_teardown_generic.ps1 -Salvage',
        'which only READS and COPIES: it signalled no process, killed nothing,',
        'freed no port, opened no database and wrote nothing outside outbox\.',
        '',
        'The evidence below is INCOMPLETE and was RECOVERED AFTER THE FACT. It is',
        'whatever happened to still be on the disk at the time above. It is NOT a',
        'measurement of the state of the round at the moment the round ended, and',
        'it must never be cited as one. Anything listed under MISSING: is gone for',
        'good - it was never recorded, so no later job can recover it.',
        '',
        'A round with only a salvage receipt is a DEGRADED round. It may support a',
        'finding, but it cannot close a hypothesis on its own.',
        '',
        'MISSING - WHAT THIS ROUND WILL NEVER HAVE',
        '-----------------------------------------'
    )
    $body = @(
        '',
        'FOUND - WHAT WAS STILL ON THE DISK',
        '----------------------------------'
    )
    $tailTxt = @(
        '',
        'HOW TO NOT NEED THIS FILE AGAIN',
        '-------------------------------',
        'The boot job can write its own paired teardown at the moment it succeeds',
        '(staged\TEMPLATE_boot_writes_paired_teardown.ps1), so closing a round is',
        'one copy into inbox\ with nothing to fill in and nothing to remember.',
        '',
        'END OF SALVAGE RECEIPT - DEGRADED EVIDENCE - NOT A TEARDOWN RECEIPT'
    )

    $lines = @()
    $lines += @($head)
    $lines += @($miss)
    $lines += @($body)
    $lines += @($found)
    $lines += @($tailTxt)
    # -like, not -eq: the count is only known after the collection has run, and a
    # header whose alignment somebody adjusts later must not silently stop being
    # filled in. (An exact-string match is the kind of thing that rots quietly.)
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -like 'missing_items*PLACEHOLDER') {
            $lines[$i] = "missing_items         : $($miss.Count)"
        }
    }

    $receipt = Join-Path $outbox ('SALVAGE_' + $jobTag + '_' + $stamp + '.txt')
    $wrote = $false
    try { Write-AsciiLines $receipt $lines; $wrote = (Test-Path -LiteralPath $receipt) }
    catch { W "SALVAGE: could not write the receipt: $($_.Exception.Message)" }

    W "SALVAGE reason        : $Why"
    W "SALVAGE boot stamp    : $bootStampTxt  (age $bootAgeTxt)"
    W "SALVAGE found items   : $($found.Count)"
    W "SALVAGE missing items : $($miss.Count)"
    foreach ($m in $miss) { W "  $m" }
    if (-not $wrote) {
        W "=== $jobTag SALVAGE FAILED - no receipt written (exit 21) ==="
        exit 21
    }
    W "SALVAGE receipt       : $(Split-Path -Leaf $receipt)"
    W '=== SALVAGE DONE - THIS ROUND IS DEGRADED, NOT GREEN (exit 20) ==='
    exit 20
}

# ---------- 0) find the client info file: NEWEST MATCH, NO JOB NUMBER ----------
$kv       = @{}
$bootTime = $null
$why      = ''
# A salvage can be degraded for more than one reason at once (stale AND the
# wrong prefix, say). Accumulate them: the receipt header has room for the whole
# truth, and overwriting one reason with the next is how a receipt ends up
# understating how bad the round was.
function AddWhy($t) {
    if ($script:why) { $script:why = $script:why + '; ' + $t } else { $script:why = $t }
}

$info = Get-ChildItem -LiteralPath $outbox -Filter '*_client_info_*.txt' -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime | Select-Object -Last 1
if (-not $info) {
    if (-not $Salvage) {
        Fail 'no *_client_info_*.txt in outbox - boot job did not run or did not write its info file. If the round is dead and you only want the evidence that is still on disk, re-run with -Salvage.' 11
    }
    W 'SALVAGE: no *_client_info_*.txt in outbox - collecting what is on disk anyway'
    AddWhy 'no client info file exists at all; salvaging whatever is on disk'
} else {
    W "info file = $($info.Name)  written=$($info.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"

    if (-not [string]::IsNullOrWhiteSpace($ExpectInfoPrefix)) {
        if ($info.Name -notlike ($ExpectInfoPrefix + '*')) {
            if (-not $Salvage) {
                Fail "newest info file '$($info.Name)' does not match -ExpectInfoPrefix '$ExpectInfoPrefix' - refusing to fall back to an older file" 12
            }
            W "SALVAGE: prefix assertion FAILED ('$($info.Name)' vs '$ExpectInfoPrefix') - recording it, not aborting"
            AddWhy "info file '$($info.Name)' does not match the expected prefix '$ExpectInfoPrefix'"
        } else {
            W "prefix assertion OK ($ExpectInfoPrefix)"
        }
    }

    $ageMin = [math]::Round(((Get-Date) - $info.LastWriteTime).TotalMinutes, 1)
    W "info file age = $ageMin min (limit $MaxInfoAgeMinutes)"
    if ($ageMin -gt $MaxInfoAgeMinutes) {
        if (-not $Salvage) {
            Fail "info file is $ageMin min old (> $MaxInfoAgeMinutes) - this is a leftover from an earlier round, NOT this one. This is exactly the job-145 failure; stopping instead of skipping ctrl-c. If this really is a dead round nobody closed, re-run with -Salvage to collect the evidence that is still on disk (it will not kill anything)." 12
        }
        AddWhy "info file is $ageMin min old (> $MaxInfoAgeMinutes)"
    }

    # ---------- 1) parse per templates\JOB_INFO_FILE_CONVENTION.md ----------
    # One key per line, split at the FIRST '=' so paths with spaces survive.
    Get-Content -LiteralPath $info.FullName | ForEach-Object {
        $i = $_.IndexOf('=')
        if ($i -gt 0) { $kv[$_.Substring(0, $i)] = $_.Substring($i + 1) }
    }
    W "parsed keys = $(($kv.Keys | Sort-Object) -join ',')"
    foreach ($need in @('clientpid', 'console', 'server', 'stamp')) {
        if (-not $kv.ContainsKey($need) -or [string]::IsNullOrWhiteSpace($kv[$need])) {
            if (-not $Salvage) {
                Fail "key '$need' missing or empty in $($info.Name) - refusing to continue with defaults" 13
            }
            W "SALVAGE: key '$need' missing or empty - it will be listed as MISSING"
        }
    }

    if ($kv.ContainsKey('stamp') -and -not [string]::IsNullOrWhiteSpace($kv['stamp'])) {
        try {
            $bootTime = [datetime]::ParseExact(
                $kv['stamp'],
                'yyyyMMdd_HHmmss',
                [System.Globalization.CultureInfo]::InvariantCulture,
                [System.Globalization.DateTimeStyles]::None
            )
        }
        catch {
            $bootTime = $null
            if (-not $Salvage) { Fail "stamp '$($kv['stamp'])' is not yyyyMMdd_HHmmss - cannot build the guard window" 14 }
            W "SALVAGE: stamp '$($kv['stamp'])' is not yyyyMMdd_HHmmss - it will be listed as MISSING"
        }
    }

    if (-not [string]::IsNullOrWhiteSpace($ExpectBootStamp)) {
        $seen = ''
        if ($kv.ContainsKey('stamp')) { $seen = $kv['stamp'] }
        if ($seen -ne $ExpectBootStamp) {
            if (-not $Salvage) {
                Fail "boot stamp in the info file is '$seen' but this teardown was written for round '$ExpectBootStamp'. This teardown belongs to a DIFFERENT round - refusing to act on it." 12
            }
            W "SALVAGE: boot stamp '$seen' != expected '$ExpectBootStamp' - recording it, not aborting"
            AddWhy "boot stamp '$seen' does not match the expected round '$ExpectBootStamp'"
        } else {
            W "boot stamp assertion OK ($ExpectBootStamp)"
        }
    }

    if ($bootTime) {
        $bootAgeMin = [math]::Round(((Get-Date) - $bootTime).TotalMinutes, 1)
        W "boot stamp = $($kv['stamp'])  (age $bootAgeMin min)"
        if ($bootAgeMin -gt $MaxInfoAgeMinutes) {
            if (-not $Salvage) {
                Fail "boot stamp is $bootAgeMin min old (> $MaxInfoAgeMinutes) - stale round. Nothing here should be signalled this late. If nobody ever closed this round, re-run with -Salvage: it collects the console tail, the run-DB state and the capture tree that are STILL ON DISK, kills nothing, and writes a receipt that says out loud what is missing." 12
            }
            AddWhy "boot stamp is $bootAgeMin min old (> $MaxInfoAgeMinutes) - stale round"
        }
    }
}

# ---------- 1b) SALVAGE SHORT-CIRCUIT -----------------------------------------
# -Salvage always wins and always ends here. Below this line the script signals
# processes; salvage must never reach it, not even on a round that is inside the
# age limit.
if ($Salvage) {
    if (-not $why) {
        $why = 'explicit -Salvage on a round that is still inside the age limit - collection only, no teardown was performed'
    }
    Invoke-Salvage $info $kv $bootTime $why
}

# ============================================================================
# NORMAL TEARDOWN PATH - unchanged behaviour. Only reached without -Salvage,
# and only for a round inside the age limit with a complete info file.
# ============================================================================
$clientPid  = [int]$kv['clientpid']
$consolePid = [int]$kv['console']
$srvPid     = [int]$kv['server']
$runDb      = ''
if ($kv.ContainsKey('rundb')) { $runDb = $kv['rundb'] }
W "from boot: client=$clientPid console=$consolePid server=$srvPid"
W "rundb = $runDb"
if ($clientPid -le 0 -or $consolePid -le 0 -or $srvPid -le 0) {
    Fail 'refusing to act on pid <= 0 (pid 0 is System Idle - job 069 lesson)' 14
}

$winLo = $bootTime.AddMinutes(-1)
$winHi = $bootTime.AddMinutes(5)
W "guard window = $($winLo.ToString('HH:mm:ss')) .. $($winHi.ToString('HH:mm:ss'))"

# ---------- 2) probe the three processes ----------
function Probe($pid_, $label) {
    try {
        $p = [System.Diagnostics.Process]::GetProcessById($pid_)
        W "  $label pid=$pid_ name=$($p.ProcessName) start=$($p.StartTime.ToString('HH:mm:ss')) hasExited=$($p.HasExited)"
        return $p
    } catch { W "  $label pid=$pid_ NOT RUNNING"; return $null }
}
function InWindow($p) { return ($p.StartTime -ge $winLo -and $p.StartTime -le $winHi) }

$srv = Probe $srvPid     'server'
$con = Probe $consolePid 'console'
$cl  = Probe $clientPid  'client'
$okCon = ($con -and $con.ProcessName -eq 'py' -and (InWindow $con))
$okCl  = ($cl  -and $cl.ProcessName -like 'GameClient*' -and (InWindow $cl))
if ($con -and -not $okCon) { W "GUARD: console pid $consolePid failed identity/window check" }
if ($cl  -and -not $okCl)  { W "GUARD: client pid $clientPid failed identity/window check" }

$lis0 = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
          Where-Object { $Ports -contains [int]$_.LocalPort })
foreach ($l in $lis0) { W "  BEFORE listener port=$($l.LocalPort) owningPid=$($l.OwningProcess)" }
W "BEFORE listeners = $($lis0.Count)"

# ---------- 3) close the client (usually already closed by the attended run) ----------
if ($cl -and -not $cl.HasExited) {
    if ($okCl) {
        W 'client still running - CloseMainWindow'
        $null = $cl.CloseMainWindow()
        $null = $cl.WaitForExit(15000)
        $cl.Refresh()
        if (-not $cl.HasExited) {
            W 'client still alive after 15s - Stop-Process on guarded pid'
            Stop-Process -Id $clientPid -Force -ErrorAction SilentlyContinue
            $null = $cl.WaitForExit(10000)
        }
        W "client exited = $($cl.HasExited)"
    } else {
        W 'client pid is alive but failed the guard - NOT touching it'
    }
} else {
    W 'client already gone (expected: closed in-game or by the attended session)'
}
W "GameClient processes now = $(@(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue).Count)"

# ---------- 4) stop the server: ctrl-c to the PARENT of the port holder ----------
# The port is held by the python server process; its parent is the visible `py`
# launcher console, which is what pf_stop_visible_server.py can signal.
if ($lis0.Count -eq 0) {
    W 'no listener on the watched ports - server already down, ctrl-c not needed'
    if ($okCon -and -not $con.HasExited) {
        W 'WARN: console process is still alive with no listener - sending ctrl-c anyway to clean it up'
        & py -3 "$(Join-Path $bridge 'pf_stop_visible_server.py')" $consolePid --json "$(Join-Path $outbox ($jobTag + '_ctrlc_' + $stamp + '.json'))" | Out-Null
        W "ctrl-c helper exit = $LASTEXITCODE"
        $null = $con.WaitForExit(30000)
        W "console exited = $($con.HasExited)"
    }
} else {
    # Map every port holder to its parent, then decide the signal target.
    $targets = New-Object System.Collections.ArrayList
    foreach ($holderPid in (@($lis0 | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique))) {
        $ci = Get-CimInstance Win32_Process -Filter "ProcessId=$holderPid" -ErrorAction SilentlyContinue
        if (-not $ci) { W "  port holder pid=$holderPid vanished before we could inspect it"; continue }
        W "  port holder pid=$holderPid name=$($ci.Name) parent=$($ci.ParentProcessId)"
        $null = $targets.Add([int]$ci.ParentProcessId)
    }
    $targets = @($targets | Sort-Object -Unique)

    if ($targets.Count -eq 0) {
        Fail 'ports are bound but no owning process could be inspected - refusing to guess a target' 15
    }

    # The info file must describe THIS round: its console pid must be a parent
    # of a live port holder. If it is not, the info file belongs to another
    # round and signalling from it would be the job-145 mistake in reverse.
    if ($targets -notcontains $consolePid) {
        W "console pid from info file = $consolePid"
        W "actual parent(s) of port holder(s) = $($targets -join ',')"
        Fail 'the info file does not describe the process that currently holds the port. This is a stale/mismatched info file. Run TOOL_stop_stale_server.ps1 to free the ports, then investigate which boot job is live.' 15
    }
    if (-not $okCon) {
        Fail "console pid $consolePid is the parent of the port holder but failed the identity/time-window guard - refusing to signal without a positive identification" 15
    }

    W "ctrl-c target = $consolePid (parent of the port holder, identity OK)"
    & py -3 "$(Join-Path $bridge 'pf_stop_visible_server.py')" $consolePid --json "$(Join-Path $outbox ($jobTag + '_ctrlc_' + $stamp + '.json'))" | Out-Null
    W "ctrl-c helper exit = $LASTEXITCODE"
    if ($srv) { $null = $srv.WaitForExit(30000); W "server  exited=$($srv.HasExited)" }
    if ($con) { $null = $con.WaitForExit(30000); W "console exited=$($con.HasExited)" }
}

Start-Sleep -Seconds 3
$lis1 = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
          Where-Object { $Ports -contains [int]$_.LocalPort })
foreach ($l in $lis1) { W "  AFTER listener port=$($l.LocalPort) owningPid=$($l.OwningProcess)" }
W "AFTER listeners = $($lis1.Count)"

if ($lis1.Count -gt 0 -and $ForceKillIfPortsStuck) {
    foreach ($p in (@($lis1 | Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique))) {
        W "FORCE: Stop-Process -Id $p -Force (graceful ctrl-c did not free the port)"
        Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 3
    $lis1 = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
              Where-Object { $Ports -contains [int]$_.LocalPort })
    W "AFTER force listeners = $($lis1.Count)"
}

$portsStuck = ($lis1.Count -gt 0)

# ---------- 5) evidence from the capture root ----------
$cap = Get-ChildItem -LiteralPath $client -Directory -Filter $CaptureFilter -ErrorAction SilentlyContinue |
       Sort-Object Name | Select-Object -Last 1
if ($cap) {
    W "capture root = $($cap.Name)"
    $allCap = @(Get-ChildItem -Recurse -File -LiteralPath $cap.FullName -ErrorAction SilentlyContinue)
    W "capture files total = $($allCap.Count)"
    foreach ($g in ($allCap | Sort-Object Length -Descending | Select-Object -First 10)) {
        W "  cap: $($g.Name) bytes=$($g.Length)"
    }
    $mo = Join-Path $cap.FullName 'server_console_live.out.txt'
    if (Test-Path -LiteralPath $mo) {
        $t = Get-Content -Raw -Encoding utf8 -LiteralPath $mo
        W "console out bytes = $((Get-Item -LiteralPath $mo).Length)"
        W "stopped markers   = $(([regex]::Matches($t,'\[FOUNDATION\] stopped')).Count)"
        W "ready markers     = $(([regex]::Matches($t,'listener ready')).Count)"
        W "traceback markers = $(([regex]::Matches($t,'Traceback')).Count)"
        $tailFile = Join-Path $outbox ($jobTag + '_console_tail_' + $stamp + '.txt')
        ($t -split "`r?`n" | Select-Object -Last 120) -join "`r`n" |
            Out-File -FilePath $tailFile -Encoding utf8
        W "console tail (120 lines) -> $(Split-Path -Leaf $tailFile)"
    } else { W 'server_console_live.out.txt not found' }
    foreach ($g in @(Get-ChildItem -Recurse -File -Filter 'GAME_LIVE.txt' -LiteralPath $cap.FullName -ErrorAction SilentlyContinue)) {
        W "GAME_LIVE: $($g.FullName.Substring($cap.FullName.Length+1)) bytes=$($g.Length)"
    }
    foreach ($g in @(Get-ChildItem -Recurse -File -Filter 'GAME_EVENTS_LIVE.txt' -LiteralPath $cap.FullName -ErrorAction SilentlyContinue)) {
        W "GAME_EVENTS: $($g.FullName.Substring($cap.FullName.Length+1)) bytes=$($g.Length)"
    }
    # ---- ROUND-SPECIFIC GREPS GO HERE (add, do not remove the above) ----
} else {
    W "capture root not found (filter '$CaptureFilter')"
}

# ---------- 6) DB AFTER on the run copy, read-only ----------
if ($runDb -and (Test-Path -LiteralPath $runDb)) {
    $uri = 'file:' + ($runDb -replace '\\', '/') + '?mode=ro'
    W '--- DB AFTER (run copy, read-only) ---'
    py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);print('  sessions with char   :',c.execute('select count(*) from sessions where selected_character_id is not null').fetchone()[0]);print('  open sessions        :',c.execute('select count(*) from sessions where closed_at is null').fetchone()[0]);print('  max lease_generation :',c.execute('select max(lease_generation) from sessions').fetchone()[0]);print('  integrity            :',c.execute('pragma integrity_check').fetchone()[0]);print('  fk_check rows        :',len(c.execute('pragma foreign_key_check').fetchall()));rows=list(c.execute('select id,selected_character_id,lease_generation,opened_at,closed_at from sessions order by rowid desc limit 4'));[print('  S',r) for r in rows[::-1]]" "$uri" 2>&1 | ForEach-Object { W $_ }
} else {
    W "run DB not found or not declared: $runDb"
}

# ---------- 7) canonical DB must be untouched (expected sha from CANON_SHA.txt) ----------
$canonMoved = $false
$canon = Join-Path $main 'state\pirateforce.sqlite3'
if (Test-Path -LiteralPath $canon) {
    $sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash.ToUpper()
    W "canonical sha now = $sha"
    $shaFile = Join-Path $bridge 'CANON_SHA.txt'
    if (Test-Path -LiteralPath $shaFile) {
        $expected = ((Get-Content -LiteralPath $shaFile -Raw) -replace '[^0-9A-Fa-f]', '').ToUpper()
        W "expected (CANON_SHA.txt) = $expected"
        if ($sha -ne $expected) { W 'RED: canonical DB MOVED during this attended round'; $canonMoved = $true }
        else { W 'canonical guard OK: unchanged' }
    } else {
        W 'RED: CANON_SHA.txt missing - cannot verify the canonical DB'
        $canonMoved = $true
    }
    foreach ($sfx in @('-wal', '-shm')) {
        $f = $canon + $sfx
        if (Test-Path -LiteralPath $f) { W "  $sfx present, $((Get-Item -LiteralPath $f).Length) bytes" }
        else { W "  $sfx absent" }
    }
} else {
    W "RED: canonical DB not found at $canon"
    $canonMoved = $true
}

# ---------- 8) final verdict - a green log with a bound port is NOT allowed ----------
if ($portsStuck) {
    W "RED: ports $($Ports -join ',') are STILL BOUND after teardown - the next boot will fail."
    W 'RED: run staged\TOOL_stop_stale_server.ps1 before the next round.'
    W "=== $jobTag TEARDOWN FAILED (exit 16) ==="
    exit 16
}
if ($canonMoved) {
    W "=== $jobTag TEARDOWN FAILED (exit 17) ==="
    exit 17
}
W "=== $jobTag TEARDOWN DONE (ports free, canonical unchanged) ==="
exit 0

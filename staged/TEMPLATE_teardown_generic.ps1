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
#
# USAGE
#   Copy to inbox\<NNN>_<gtid>_teardown.ps1. Adjust the CaptureFilter default
#   (or pass -CaptureFilter) and, if the round needs extra evidence greps, add
#   them in section 4. Do NOT reintroduce a job number in any glob.
#
# EXIT CODES
#   0  ok                     11 no client info file found
#   12 info file too old      13 required key missing or empty
#   14 pid <= 0 / bad stamp    15 guard mismatch - refuse to signal
#   16 ports still bound      17 canonical DB moved
# ============================================================================

param(
    # Assertion only. Empty = accept whatever the newest info file is.
    [string]  $ExpectInfoPrefix     = '',
    # Anything older than this is treated as a leftover, not as this round.
    [int]     $MaxInfoAgeMinutes    = 180,
    [int[]]   $Ports                = @(10188, 10189),
    # Capture root to harvest, e.g. 'capture_gt015_*'.
    [string]  $CaptureFilter        = 'capture_*',
    # Last resort only. Default OFF: a stuck port should be visible, not hidden.
    [switch]  $ForceKillIfPortsStuck
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$client = 'C:\Users\Panya\Desktop\Pirate Force\GameClient'
$outbox = Join-Path $bridge 'outbox'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'

# Job tag comes from THIS FILE'S NAME - never from a hardcoded number.
$jobTag = ''
if ($MyInvocation.MyCommand.Path) {
    $jobTag = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Path)
}
if ([string]::IsNullOrWhiteSpace($jobTag)) { $jobTag = 'teardown_generic' }

$log = Join-Path $outbox ($jobTag + '.utf8.txt')
function W($m) {
    $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"
    $l | Out-File -FilePath $log -Encoding utf8 -Append
    Write-Host $l
}
"=== $jobTag TEARDOWN  $stamp ===" | Out-File -FilePath $log -Encoding utf8
W "job tag derived from filename = $jobTag"
W "ports watched = $($Ports -join ',')"

function Fail($msg, $code) {
    W "ABORT($code): $msg"
    W "=== $jobTag TEARDOWN FAILED (exit $code) ==="
    exit $code
}

# ---------- 0) find the client info file: NEWEST MATCH, NO JOB NUMBER ----------
$info = Get-ChildItem -LiteralPath $outbox -Filter '*_client_info_*.txt' -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime | Select-Object -Last 1
if (-not $info) {
    Fail 'no *_client_info_*.txt in outbox - boot job did not run or did not write its info file' 11
}
W "info file = $($info.Name)  written=$($info.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"

if (-not [string]::IsNullOrWhiteSpace($ExpectInfoPrefix)) {
    if ($info.Name -notlike ($ExpectInfoPrefix + '*')) {
        Fail "newest info file '$($info.Name)' does not match -ExpectInfoPrefix '$ExpectInfoPrefix' - refusing to fall back to an older file" 12
    }
    W "prefix assertion OK ($ExpectInfoPrefix)"
}

$ageMin = [math]::Round(((Get-Date) - $info.LastWriteTime).TotalMinutes, 1)
W "info file age = $ageMin min (limit $MaxInfoAgeMinutes)"
if ($ageMin -gt $MaxInfoAgeMinutes) {
    Fail "info file is $ageMin min old (> $MaxInfoAgeMinutes) - this is a leftover from an earlier round, NOT this one. This is exactly the job-145 failure; stopping instead of skipping ctrl-c." 12
}

# ---------- 1) parse per templates\JOB_INFO_FILE_CONVENTION.md ----------
# One key per line, split at the FIRST '=' so paths with spaces survive.
$kv = @{}
Get-Content -LiteralPath $info.FullName | ForEach-Object {
    $i = $_.IndexOf('=')
    if ($i -gt 0) { $kv[$_.Substring(0, $i)] = $_.Substring($i + 1) }
}
W "parsed keys = $(($kv.Keys | Sort-Object) -join ',')"
foreach ($need in @('clientpid', 'console', 'server', 'stamp')) {
    if (-not $kv.ContainsKey($need) -or [string]::IsNullOrWhiteSpace($kv[$need])) {
        Fail "key '$need' missing or empty in $($info.Name) - refusing to continue with defaults" 13
    }
}
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

$bootTime = $null
try { $bootTime = [datetime]::ParseExact($kv['stamp'], 'yyyyMMdd_HHmmss', $null) }
catch { Fail "stamp '$($kv['stamp'])' is not yyyyMMdd_HHmmss - cannot build the guard window" 14 }
$bootAgeMin = [math]::Round(((Get-Date) - $bootTime).TotalMinutes, 1)
W "boot stamp = $($kv['stamp'])  (age $bootAgeMin min)"
if ($bootAgeMin -gt $MaxInfoAgeMinutes) {
    Fail "boot stamp is $bootAgeMin min old (> $MaxInfoAgeMinutes) - stale round" 12
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

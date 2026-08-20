# Job 105 - GT-016 teardown (attended). Queued behind 104; run after the UI
# Queued behind 104; run after the chat UI observation finishes. Client will NOT
# self-exit (logout scenario is NOT active - mutually exclusive with chat): the
# attended session must End-task the client FIRST, then run this teardown.
# Info-file parse follows templates\JOB_INFO_FILE_CONVENTION.md: one key per
# line, split at the FIRST '=', quote every path, refuse empty values.
# Canonical DB must remain untouched (test ran on a copy). ASCII ONLY.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$client = 'C:\Users\Panya\Desktop\Pirate Force\GameClient'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\127_gt016_teardown.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== 105 GT-016 TEARDOWN  $stamp ===" | Out-File -FilePath $log -Encoding utf8

# ---------- 0) parse 104 info (NEW CONVENTION: one key per line, first-= split) ----------
$info = Get-ChildItem (Join-Path $bridge 'outbox') -Filter '124_client_info_*.txt' | Sort-Object LastWriteTime | Select-Object -Last 1
if (-not $info) { W 'ABORT: no 124_client_info file'; exit 11 }
$kv = @{}
Get-Content $info.FullName | ForEach-Object {
    $i = $_.IndexOf('=')
    if ($i -gt 0) { $kv[$_.Substring(0,$i)] = $_.Substring($i+1) }
}
W "parsed keys = $(($kv.Keys | Sort-Object) -join ',')"
foreach ($need in @('clientpid','console','server','stamp','rundb')) {
    if (-not $kv.ContainsKey($need) -or [string]::IsNullOrWhiteSpace($kv[$need])) {
        W "PARSE FAIL: key '$need' missing or empty - refusing to continue with defaults"; exit 12
    }
}
$clientPid = [int]$kv['clientpid']; $consolePid = [int]$kv['console']
$srvPid = [int]$kv['server']; $runDb = $kv['rundb']
W "from 104: client=$clientPid console=$consolePid server=$srvPid rundb=$runDb"
if ($consolePid -le 0 -or $srvPid -le 0 -or $clientPid -le 0) { W 'ABORT: refuse pid 0'; exit 12 }

$bootTime = [datetime]::ParseExact($kv['stamp'], 'yyyyMMdd_HHmmss', $null)
$winLo = $bootTime.AddMinutes(-1); $winHi = $bootTime.AddMinutes(5)
W "guard window = $($winLo.ToString('HH:mm:ss')) .. $($winHi.ToString('HH:mm:ss'))"

function Probe($pid_, $label) {
    try { $p = [System.Diagnostics.Process]::GetProcessById($pid_); W "  $label pid=$pid_ name=$($p.ProcessName) start=$($p.StartTime.ToString('HH:mm:ss')) hasExited=$($p.HasExited)"; return $p }
    catch { W "  $label pid=$pid_ NOT RUNNING"; return $null }
}
$srv = Probe $srvPid 'server'; $con = Probe $consolePid 'console'; $cl = Probe $clientPid 'client'
function InWindow($p) { return ($p.StartTime -ge $winLo -and $p.StartTime -le $winHi) }
$okCon = ($con -and $con.ProcessName -eq 'py' -and (InWindow $con))
$okCl  = ($cl -and $cl.ProcessName -like 'GameClient*' -and (InWindow $cl))

# ---------- 1) client state (KEY OBSERVATION subcode 01: did it exit BY ITSELF ~250ms after ack?) ----------
if ($cl -and -not $cl.HasExited) {
    W 'client STILL RUNNING at teardown time (subcode 01 did NOT close it by itself)'
    if ($okCl) {
        $null = $cl.CloseMainWindow(); W 'client CloseMainWindow sent'
        $null = $cl.WaitForExit(15000); $cl.Refresh()
        if (-not $cl.HasExited) { W 'client still alive - Stop-Process on guarded pid'; Stop-Process -Id $clientPid -Force -ErrorAction SilentlyContinue; $null = $cl.WaitForExit(10000) }
    }
} else { W 'client already exited (if it closed ITSELF after the exit-game button, that is the subcode-01 PASS signal)' }
W "GameClient processes now = $(@(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue).Count)"

# ---------- 2) stop server (ctrl-c to visible console) ----------
if ($okCon -and -not $con.HasExited) {
    & py -3 (Join-Path $bridge 'pf_stop_visible_server.py') $consolePid --json (Join-Path $bridge "outbox\127_ctrlc_$stamp.json") | Out-Null
    W "ctrl-c helper exit = $LASTEXITCODE"
    if ($srv) { $null = $srv.WaitForExit(30000); W "server exited=$($srv.HasExited)" }
    if ($con) { $null = $con.WaitForExit(30000); W "console exited=$($con.HasExited)" }
} else { W 'skipped ctrl-c (guard failed or console already gone)' }
Start-Sleep -Seconds 2
W "AFTER listeners = $(@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 }).Count)"

# ---------- 3) wire evidence from capture root ----------
$cap = Get-ChildItem $client -Directory -Filter 'capture_gt016_*' -ErrorAction SilentlyContinue | Sort-Object Name | Select-Object -Last 1
if ($cap) {
    W "capture root = $($cap.Name)"
    $glf = @(Get-ChildItem -Recurse -File -Filter 'GAME_LIVE.txt' $cap.FullName -ErrorAction SilentlyContinue)
    foreach ($g in $glf) {
        $t = Get-Content -Raw -Encoding utf8 $g.FullName
        W "GAME_LIVE: $($g.FullName.Substring($cap.FullName.Length+1)) bytes=$($g.Length)"
        W "  HYP_PF_014 marker lines = $(([regex]::Matches($t,'HYP_PF_014')).Count)"
        W "  ChatVital 0xAC52 lines  = $(([regex]::Matches($t,'AC52|44114')).Count)"
        W "  SOCKET_CLOSED lines     = $(([regex]::Matches($t,'SOCKET_CLOSED|SESSION_END')).Count)"
        $mk = ($t -split "`r?`n" | Where-Object { $_ -match 'HYP_PF_014|SPEAKER|AC52' } | Select-Object -First 16)
        foreach ($line in $mk) { W "  mk> $line" }
    }
    $gev = @(Get-ChildItem -Recurse -File -Filter 'GAME_EVENTS_LIVE.txt' $cap.FullName -ErrorAction SilentlyContinue)
    foreach ($g in $gev) {
        W "GAME_EVENTS: bytes=$($g.Length)"
        $t = Get-Content -Raw -Encoding utf8 $g.FullName
        $lg = ($t -split "`r?`n" | Where-Object { $_ -match 'AC52|44114|CHAT' } | Select-Object -First 8)
        foreach ($line in $lg) { W "  ev> $line" }
    }
} else { W 'capture root not found' }

# ---------- 4) DB AFTER (run copy, read-only) + canonical untouched check ----------
if ($runDb -and (Test-Path -LiteralPath $runDb)) {
    $uri = 'file:' + ($runDb -replace '\\','/') + '?mode=ro'
    W '--- DB AFTER (run copy) ---'
    py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);print('  sessions with char   :',c.execute('select count(*) from sessions where selected_character_id is not null').fetchone()[0]);print('  open sessions        :',c.execute('select count(*) from sessions where closed_at is null').fetchone()[0]);print('  max lease_generation :',c.execute('select max(lease_generation) from sessions').fetchone()[0]);print('  integrity            :',c.execute('pragma integrity_check').fetchone()[0]);rows=list(c.execute('select id,selected_character_id,lease_generation,opened_at,closed_at from sessions order by rowid desc limit 4'));[print('  S',r) for r in rows[::-1]]" "$uri" 2>&1 | ForEach-Object { W $_ }
} else { W "run DB not found: $runDb" }
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha now = $sha"
$shaFile = Join-Path $bridge 'CANON_SHA.txt'
if (Test-Path -LiteralPath $shaFile) {
    $expectedSha = ((Get-Content -LiteralPath $shaFile -Raw) -replace '[^0-9A-Fa-f]','').ToUpper()
    W "expected (must be UNCHANGED, from CANON_SHA.txt) = $expectedSha"
    if ($sha.ToUpper() -ne $expectedSha) { W 'RED: canonical DB MOVED during this attended test' } else { W 'canonical guard OK: unchanged' }
} else { W 'WARN: CANON_SHA.txt missing - cannot compare canonical sha' }
W '=== 127 GT-016 TEARDOWN DONE ==='

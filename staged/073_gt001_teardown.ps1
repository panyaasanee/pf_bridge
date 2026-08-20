# Job 073 - GT-001 teardown (attended big round). Queued behind 072 per rule R31;
# runs automatically the moment the game window closes and the bridge unblocks.
# Client is expected to be ALREADY CLOSED via in-game X + confirm (PLAYBOOK 7).
# Parse + PID-reuse guards from done\061_gt001_teardown.ps1 (proven), pointed at 072 info.
# Lesson 27.2 applied: every path argument passed to a native command is quoted.
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\073_gt001_teardown.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== 073 TEARDOWN (GT-001 attended)  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$canon = Join-Path $main 'state\pirateforce.sqlite3'
$uri   = 'file:' + ($canon -replace '\\','/') + '?mode=ro'

# ---------- 0) parse 072 info (whitespace separated k=v on ONE line) ----------
$info = Get-ChildItem (Join-Path $bridge 'outbox') -Filter '072_client_info_*.txt' | Sort-Object LastWriteTime | Select-Object -Last 1
if (-not $info) { W 'ABORT: no 072_client_info file'; exit 11 }
$kv = @{}
foreach ($tok in ((Get-Content -Raw $info.FullName) -split '\s+')) {
    if ($tok -match '^([A-Za-z_]\w*)=(.*)$') { $kv[$Matches[1]] = $Matches[2] }
}
W "parsed keys = $(($kv.Keys | Sort-Object) -join ',')"
$clientPid = 0; $shimPid = 0; $srvPid = 0
if ($kv.ContainsKey('clientpid')) { $clientPid = [int]$kv['clientpid'] }
if ($kv.ContainsKey('shim'))      { $shimPid   = [int]$kv['shim'] }
if ($kv.ContainsKey('server'))    { $srvPid    = [int]$kv['server'] }
W "from 072: client=$clientPid shim=$shimPid server=$srvPid stamp=$($kv['stamp'])"
if ($shimPid -le 0 -or $srvPid -le 0 -or $clientPid -le 0) { W 'ABORT: refuse to act on pid 0'; exit 12 }

# guard window derived from 072 boot stamp (yyyyMMdd_HHmmss)
$bootTime = [datetime]::ParseExact($kv['stamp'], 'yyyyMMdd_HHmmss', $null)
$winLo = $bootTime.AddMinutes(-1)
$winHi = $bootTime.AddMinutes(5)
W "guard window = $($winLo.ToString('HH:mm:ss')) .. $($winHi.ToString('HH:mm:ss'))"

# ---------- 1) BEFORE snapshot ----------
$gc0 = @(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue)
W "BEFORE GameClient processes = $($gc0.Count)"
$lis0 = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
foreach ($l in $lis0) { W "  BEFORE listener port=$($l.LocalPort) owningPid=$($l.OwningProcess)" }
W "BEFORE listeners = $($lis0.Count)"

function Probe($pid_, $label) {
    try {
        $p = [System.Diagnostics.Process]::GetProcessById($pid_)
        W "  $label pid=$pid_ name=$($p.ProcessName) start=$($p.StartTime.ToString('HH:mm:ss')) hasExited=$($p.HasExited)"
        return $p
    } catch { W "  $label pid=$pid_ NOT RUNNING ($($_.Exception.Message))"; return $null }
}
$srv  = Probe $srvPid  'server'
$shim = Probe $shimPid 'shim'
$cl   = Probe $clientPid 'client'

function InWindow($p) { return ($p.StartTime -ge $winLo -and $p.StartTime -le $winHi) }
$okShim   = ($shim -and $shim.ProcessName -eq 'py'     -and (InWindow $shim))
$okClient = ($cl   -and $cl.ProcessName -like 'GameClient*' -and (InWindow $cl))
if ($shim -and -not $okShim) { W "GUARD: shim pid $shimPid failed identity check - refusing to signal" }
if ($cl   -and -not $okClient) { W "GUARD: client pid $clientPid failed identity check - refusing to touch" }

# ---------- 2) close client if somehow still alive (expected: already gone) ----------
if ($okClient -and -not $cl.HasExited) {
    $null = $cl.CloseMainWindow()
    W 'client CloseMainWindow sent'
    $null = $cl.WaitForExit(15000)
    $cl.Refresh()
    if (-not $cl.HasExited) {
        W 'client still alive after 15s - Stop-Process on guarded pid'
        Stop-Process -Id $clientPid -Force -ErrorAction SilentlyContinue
        $null = $cl.WaitForExit(10000)
    }
    W "client exited = $($cl.HasExited)"
} else { W 'client already gone or guard failed (expected: closed via in-game X)' }
$gcMid = @(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue)
W "GameClient processes after close = $($gcMid.Count)"

# ---------- 3) stop the server via the visible console (ctrl-c to shim) ----------
if ($okShim -and -not $shim.HasExited) {
    & py -3 "$(Join-Path $bridge 'pf_stop_visible_server.py')" $shimPid --json "$(Join-Path $bridge "outbox\073_ctrlc_$stamp.json")" | Out-Null
    W "ctrl-c helper exit = $LASTEXITCODE"
    if ($srv)  { $null = $srv.WaitForExit(30000);  W "server exited=$($srv.HasExited) code=$(try{$srv.ExitCode}catch{'?'})" }
    if ($shim) { $null = $shim.WaitForExit(30000); W "shim   exited=$($shim.HasExited) code=$(try{$shim.ExitCode}catch{'?'})" }
} else {
    W 'skipped ctrl-c (guard failed or shim already exited)'
}
Start-Sleep -Seconds 2
$lis1 = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
foreach ($l in $lis1) { W "  AFTER listener port=$($l.LocalPort) owningPid=$($l.OwningProcess)" }
W "AFTER listeners = $($lis1.Count)"
$gc1 = @(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue)
W "AFTER GameClient processes = $($gc1.Count)"

# ---------- 4) console + capture evidence ----------
$cap = Get-ChildItem 'C:\Users\Panya\Desktop\Pirate Force\GameClient' -Directory -Filter 'capture_gt001_*' -ErrorAction SilentlyContinue | Sort-Object Name | Select-Object -Last 1
if ($cap) {
    W "capture root = $($cap.Name)"
    $mo = Join-Path $cap.FullName 'server_console_live.out.txt'
    $me = Join-Path $cap.FullName 'server_console_live.err.txt'
    if (Test-Path -LiteralPath $mo) {
        $t = Get-Content -Raw -Encoding utf8 $mo
        W "console out bytes = $((Get-Item -LiteralPath $mo).Length)"
        W "stopped markers   = $(([regex]::Matches($t,'\[FOUNDATION\] stopped')).Count)"
        W "ready markers     = $(([regex]::Matches($t,'listener ready')).Count)"
        W "traceback markers = $(([regex]::Matches($t,'Traceback')).Count)"
        W "TargetPos mentions in console   = $(([regex]::Matches($t,'TargetPos')).Count)"
        W "StartGameReq mentions           = $(([regex]::Matches($t,'StartGameReq')).Count)"
        $tailFile = Join-Path $bridge "outbox\073_console_tail_$stamp.txt"
        ($t -split "`r?`n" | Select-Object -Last 120) -join "`r`n" | Out-File -FilePath $tailFile -Encoding utf8
        W "console tail (120 lines) written -> $(Split-Path -Leaf $tailFile)"
    } else { W 'console out not found' }
    $eb = if (Test-Path -LiteralPath $me) { (Get-Item -LiteralPath $me).Length } else { -1 }
    W "stderr = $eb bytes  (NOTE: -1 means file absent, not a byte count)"
    $glf = @(Get-ChildItem -Recurse -File -Filter 'GAME_LIVE.txt' $cap.FullName -ErrorAction SilentlyContinue)
    W "GAME_LIVE.txt files = $($glf.Count)"
    foreach ($g in $glf) { W "  GAME_LIVE: $($g.FullName.Substring($cap.FullName.Length+1)) bytes=$($g.Length)" }
    $allCap = @(Get-ChildItem -Recurse -File $cap.FullName -ErrorAction SilentlyContinue)
    W "capture files total = $($allCap.Count)"
    foreach ($g in ($allCap | Sort-Object Length -Descending | Select-Object -First 12)) { W "  cap: $($g.Name) bytes=$($g.Length)" }
} else { W 'capture root not found' }

# ---------- 5) DB after (read-only URI) ----------
W '--- DB AFTER (post-stop) ---'
py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);[print('  POS',r) for r in c.execute('SELECT c.id,c.name,p.scene_id,p.scene_seq,p.x,p.y,p.z,p.heading,p.updated_at FROM characters c JOIN character_positions p ON p.character_id=c.id')]" "$uri" 2>&1 | ForEach-Object { W $_ }
py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);print('  sessions with char   :',c.execute('select count(*) from sessions where selected_character_id is not null').fetchone()[0]);print('  sessions blank-conn  :',c.execute('select count(*) from sessions where selected_character_id is null').fetchone()[0]);print('  open sessions        :',c.execute('select count(*) from sessions where closed_at is null').fetchone()[0]);print('  max lease_generation :',c.execute('select max(lease_generation) from sessions').fetchone()[0]);print('  backpack items       :',[tuple(r) for r in c.execute('select slot,item_identity,template_id,quantity from character_backpack_items order by slot')]);print('  integrity            :',c.execute('pragma integrity_check').fetchone()[0]);print('  fk_check rows        :',len(c.execute('pragma foreign_key_check').fetchall()))" "$uri" 2>&1 | ForEach-Object { W $_ }

$sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "db sha AFTER = $sha"
W "old canonical (pre-GT001 rerun) = CACE7F7755E79AF0C2E637BC6C09C131E6152436F3141E136BC457ECA74DF493"
W "NOTE: sha is EXPECTED to differ (new sessions row from GT-001 login) - not a failure"
foreach ($sfx in @('-wal','-shm')) {
    $f = $canon + $sfx
    if (Test-Path -LiteralPath $f) { W "  $sfx present, $((Get-Item -LiteralPath $f).Length) bytes" } else { W "  $sfx absent" }
}
W '=== 073 TEARDOWN DONE ==='

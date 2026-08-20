# Job 097 - GT-010 boot (ATTENDED big round). delete-button client-observable test (HYP-PF-015).
# Server MUST boot with --delete-actor-hypothesis-scenario pointing at the
# DELETE_SOFT scenario (HYP-PF-015) on a FRESH COPY of canonical DB. NOTE: the
# run copy gets migration 004 applied at boot (partial unique indexes) - that
# is expected and required for slot reuse. Boot adapted from
# done\080 (proven); info file follows templates\JOB_INFO_FILE_CONVENTION.md
# (one key per line, mandatory since job 084). ASCII ONLY. Quote all paths.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$client = 'C:\Users\Panya\Desktop\Pirate Force\GameClient'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\097_gt010_boot.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== GT-010 BOOT (attended, delete_actor scenario)  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$canon = Join-Path $main 'state\pirateforce.sqlite3'
$shaFile = Join-Path $bridge 'CANON_SHA.txt'
if (-not (Test-Path -LiteralPath $shaFile)) { W 'ABORT: CANON_SHA.txt missing - cannot verify canonical DB'; exit 14 }
$expectedSha = ((Get-Content -LiteralPath $shaFile -Raw) -replace '[^0-9A-Fa-f]','').ToUpper()
if ($expectedSha.Length -ne 64) { W "ABORT: CANON_SHA.txt malformed (len=$($expectedSha.Length))"; exit 15 }
W "expected canonical sha (from CANON_SHA.txt) = $expectedSha"
$scenario = Join-Path $main 'scenarios\delete_actor_hypothesis_soft_delete.json'

# ---------- 1) verify canonical sha (value from LOCK release note; re-check there first) ----------
if (-not (Test-Path -LiteralPath $canon)) { W 'ABORT: canonical DB missing'; exit 11 }
$sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha = $sha"
if ($sha.ToUpper() -ne $expectedSha) { W 'ABORT: sha differs from expected value - check LOCK release note'; exit 13 }
if (-not (Test-Path -LiteralPath $scenario)) { W "ABORT: scenario file missing: $scenario"; exit 14 }
W "scenario file ok: $scenario"

# ---------- 2) fresh copy for the test run ----------
$runDb = Join-Path $main "state\pirateforce_gt010_$stamp.sqlite3"
Copy-Item -LiteralPath $canon -Destination $runDb -Force
$rsha = (Get-FileHash -LiteralPath $runDb -Algorithm SHA256).Hash
if ($rsha -ne $sha) { W 'ABORT: run copy sha mismatch'; exit 12 }
W "run DB copy ok: $runDb"
$uri = 'file:' + ($runDb -replace '\\','/') + '?mode=ro'
W '--- DB BEFORE (run copy) ---'
py -3 -c "import sqlite3,sys;c=sqlite3.connect(sys.argv[1],uri=True);print('  sessions with char   :',c.execute('select count(*) from sessions where selected_character_id is not null').fetchone()[0]);print('  open sessions        :',c.execute('select count(*) from sessions where closed_at is null').fetchone()[0]);print('  max lease_generation :',c.execute('select max(lease_generation) from sessions').fetchone()[0]);print('  chars active         :',c.execute('select count(*) from characters where deleted_at is null').fetchone()[0]);print('  chars deleted        :',c.execute('select count(*) from characters where deleted_at is not null').fetchone()[0]);[print('  C',r) for r in c.execute('select id,selector,name,deleted_at from characters order by id')]" "$uri" 2>&1 | ForEach-Object { W $_ }

# ---------- 3) clear leftover listeners ----------
$listen = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
if ($listen.Count -gt 0) { W "ABORT: ports busy (owningPid=$($listen[0].OwningProcess)) - previous teardown incomplete"; exit 10 }
W 'ports free'

# ---------- 4) boot server DIRECT with chat_echo scenario flag (visible console) ----------
$captureRoot = Join-Path $client "capture_gt010_$stamp"
New-Item -ItemType Directory -Path $captureRoot -ErrorAction SilentlyContinue | Out-Null
$env:PYTHONPATH = Join-Path $main 'src'
$serverArgs = @(
    '-3', '-u', '-m', 'pirateforce_foundation.app',
    '--db', ('"' + $runDb + '"'),
    '--capture-root', ('"' + $captureRoot + '"'),
    '--second-password-mode', 'bypass',
    '--delete-actor-hypothesis-scenario', ('"' + $scenario + '"')
)
$server = Start-Process -FilePath 'py' -ArgumentList $serverArgs -WorkingDirectory $main -WindowStyle Normal -PassThru
W "server console PID: $($server.Id) (visible, scenario=delete_actor_hypothesis_soft_delete_op1)"
$serverPid = $null
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $l = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
    if ($l.Count -ge 2) { $serverPid = [int]$l[0].OwningProcess; break }
}
if (-not $serverPid) { W 'ABORT: no listeners after 30s'; exit 21 }
W "SERVER UP console=$($server.Id) server=$serverPid after ${i}s captureRoot=$captureRoot"

# ---------- 5) launch client redirected ----------
$cliOut = Join-Path $bridge "outbox\097_client_stdout_$stamp.txt"
$cliErr = Join-Path $bridge "outbox\097_client_stderr_$stamp.txt"
$p = Start-Process -FilePath (Join-Path $client 'GameClient.local.bin') `
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
# Info file per JOB_INFO_FILE_CONVENTION.md: ONE KEY PER LINE.
$infoFile = Join-Path $bridge "outbox\097_client_info_$stamp.txt"
@(
  "clientpid=$($p.Id)"
  "console=$($server.Id)"
  "server=$serverPid"
  "stamp=$stamp"
  "rundb=$runDb"
  "title=$title"
) | Out-File -FilePath $infoFile -Encoding ascii
W "info file written: $infoFile"
if (-not $title) { W 'WARN: no window title after 60s' }
W '=== 097 BOOT DONE - attended session drives GT-010 UI ==='

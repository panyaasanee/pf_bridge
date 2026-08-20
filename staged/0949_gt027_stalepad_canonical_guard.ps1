# ============================================================================
# 0949_gt027_stalepad_canonical_guard.ps1 - post-cleanup receipt for the
# ABANDONED big round #10 (GT-027 rerun, boot 11:37, no teardown ever ran).
# Prepared by chief round 105 for PANYA to drop into inbox\ HIMSELF - the
# chief does not touch the game pad (PANYA ORDER 1440 part B).  ASCII ONLY.
#
# CONTEXT
#   Panya's own teardown 0947 ABORTED with exit 12: the generic template
#   refuses an info file whose boot stamp is > 180 min old ("stale round"),
#   BY DESIGN - it cannot know the stale info file still describes the live
#   server.  For an abandoned pad the right sequence is the one the template
#   header itself prescribes:
#     step 1: copy staged\TOOL_stop_stale_server.ps1 to
#             inbox\0948_stop_stale_server.ps1  (UNCHANGED - it is the proven
#             recovery path for "attended session interrupted, no teardown";
#             it reads no info file on purpose)
#     step 2: drop THIS file as inbox\0949_gt027_stalepad_canonical_guard.ps1
#             for the wire/DB receipt the teardown would have produced.
#
# THIS JOB IS READ-ONLY.  It signals nothing, kills nothing, deletes nothing,
# writes nothing except its own log.  Exit nonzero = something needs a human.
#
# EXIT CODES:  0 ok · 21 ports still bound · 22 GameClient still running
#              23 canonical sha mismatch
# ============================================================================

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\0949_gt027_stalepad_canonical_guard.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== 0949 STALE-PAD CANONICAL GUARD (read-only receipt)  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$bad = 0

# 1. ports
$listen = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 })
W "listeners on 10188/10189 = $($listen.Count) (expect 0)"
if ($listen.Count -gt 0) { $listen | ForEach-Object { W "  still bound> port=$($_.LocalPort) pid=$($_.OwningProcess)" }; $bad = 21 }

# 2. established leftovers (the round-8 guard: half-dead client keeps server serial-blocked)
$estab = @(Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 10188,10189 -or $_.RemotePort -in 10188,10189 })
W "established on 10188/10189 = $($estab.Count) (expect 0)"

# 3. client processes
$gc = @(Get-Process -Name 'GameClient.local' -ErrorAction SilentlyContinue)
W "GameClient processes = $($gc.Count) (expect 0)"
if ($gc.Count -gt 0 -and $bad -eq 0) { $bad = 22 }

# 4. the boot-946 pids, by number (server=37596 console=9068 client=21300)
foreach ($bp in 37596, 9068, 21300) {
    $pp = Get-Process -Id $bp -ErrorAction SilentlyContinue
    if ($pp) { W "  boot-946 pid $bp STILL ALIVE: $($pp.ProcessName)" } else { W "  boot-946 pid $bp gone - ok" }
}

# 5. canonical DB guard (sha read from CANON_SHA.txt, never hardcoded)
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$sha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
$expect = (Get-Content -LiteralPath (Join-Path $bridge 'CANON_SHA.txt') -Raw).Trim()
W "canonical sha = $sha"
if ($sha -cne $expect) { W "RED: canonical sha != CANON_SHA.txt ($expect)"; $bad = 23 }
else { W 'CANONICAL UNCHANGED - OK (first check since job 943 at 11:27)' }

# 6. run-copy inventory (disposal is a SEPARATE decision, nothing deleted here)
Get-ChildItem -Path (Join-Path $main 'state') -Filter 'pirateforce_gt*' -ErrorAction SilentlyContinue |
    ForEach-Object { W ("  run copy> {0}  {1:N0} bytes  {2}" -f $_.Name, $_.Length, $_.LastWriteTime) }

if ($bad -ne 0) { W "=== 0949 RECEIPT RED (exit $bad) ==="; exit $bad }
W '=== 0949 RECEIPT CLEAN - pad is safe for the next boot ==='
exit 0

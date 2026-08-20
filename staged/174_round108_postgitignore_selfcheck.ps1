# Job 174 - chief round 108.  One question only: after the .gitignore edit, does
# the sync still agree that all three flag files are ignored?
#
# WHY.  Jobs 172 and 173 proved the tooling at 18:30 and 18:34.  At 18:4x this
# round added one line to pf_bridge\.gitignore - !/cloud_round_lock.json - so the
# overlap guard Panya ordered at 18:45 can be tracked at all.  Guard [0] of the
# sync refuses to do anything on a day when the flags stop being ignored, and an
# ignore file is exactly the kind of thing that breaks in a direction nobody
# notices.  A proof from before the edit is not a proof after it.
#
# Read only: check-ignore, status, rev-parse.  No fetch, no index write, no
# commit, no push, no server, no client, no database, no flag taken.
# EXIT 0 only if the selfcheck exits 0, prints its receipt, moves neither HEAD nor
# the dirty set, AND the new lock file is confirmed NOT ignored.

$ErrorActionPreference = 'Continue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$sync   = Join-Path $bridge 'pf_git_sync.ps1'

Write-Host '=== job 174 : does guard [0] still hold after the .gitignore edit ==='
Write-Host ("time : " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))

$headBefore = ([string](& git -C $bridge --no-optional-locks rev-parse HEAD)).Trim()
$before = @(& git -C $bridge --no-optional-locks status --porcelain)

$out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $sync -SelfCheck 2>&1
$code = $LASTEXITCODE
foreach ($l in $out) { Write-Host ('  | ' + $l) }
Write-Host ('  exit = ' + $code)

$headAfter = ([string](& git -C $bridge --no-optional-locks rev-parse HEAD)).Trim()
$after = @(& git -C $bridge --no-optional-locks status --porcelain)
$entered = @($after | Where-Object { $before -notcontains $_ })
$left    = @($before | Where-Object { $after -notcontains $_ })

Write-Host ''
$ok = $true
$joined = ($out | Out-String)
if ($code -ne 0) { Write-Host 'CHECK selfcheck-exit-zero: FAIL'; $ok = $false } else { Write-Host 'CHECK selfcheck-exit-zero: PASS' }
if ($joined -match 'flag guard ok') { Write-Host 'CHECK flag-guard-ok: PASS' } else { Write-Host 'CHECK flag-guard-ok: FAIL'; $ok = $false }
if ($headBefore -eq $headAfter) { Write-Host 'CHECK head-unmoved: PASS' } else { Write-Host 'CHECK head-unmoved: FAIL'; $ok = $false }
if ($entered.Count -eq 0 -and $left.Count -eq 0) { Write-Host 'CHECK worktree-identical: PASS' } else {
    Write-Host 'CHECK worktree-identical: FAIL'
    foreach ($l in $entered) { Write-Host ('   + ' + $l) }
    foreach ($l in $left) { Write-Host ('   - ' + $l) }
    $ok = $false
}

# The new lock file must be the opposite of the flags: TRACKABLE, i.e. NOT ignored.
& git -C $bridge --no-optional-locks check-ignore -q --no-index -- cloud_round_lock.json
$lockIgnored = $LASTEXITCODE
Write-Host ('CHECK cloud_round_lock-NOT-ignored: ' + $(if ($lockIgnored -ne 0) { 'PASS' } else { 'FAIL' }) + "  (check-ignore -q exit $lockIgnored, 1 means not ignored)")
if ($lockIgnored -eq 0) { $ok = $false }

foreach ($f in @('LOCK_GAME.txt', 'LOCK_GIT.txt', 'PANYA_PRESENT.txt')) {
    & git -C $bridge --no-optional-locks check-ignore -q --no-index -- $f
    $e = $LASTEXITCODE
    Write-Host ('CHECK ' + $f + '-ignored: ' + $(if ($e -eq 0) { 'PASS' } else { 'FAIL' }) + "  (exit $e)")
    if ($e -ne 0) { $ok = $false }
}

Write-Host ''
if (-not $ok) { Write-Host 'JOB174_VERDICT=FAIL'; exit 44 }
Write-Host 'JOB174_VERDICT=PASS'
exit 0

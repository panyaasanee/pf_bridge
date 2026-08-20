# Job 173 - chief round 108.  Re-run stage [D] alone, and fix the way stage [D]
# asked its question.
#
# WHY THIS EXISTS.  Job 172 ran at 18:30:30 and reported: ascii PASS, parse PASS,
# selfcheck PASS, all fourteen refusal tests PASS, SELFTEST_VERDICT=PASS - and
# then failed its own final invariant, "real-repo-worktree-unchanged", because it
# counted three dirty paths before the suite and four after.  The fourth path was
# notes_to_chief\consumed\20260820_1800_PANYA-DECISION-sync-design-approved.md,
# which the chief copied into place at 18:30:5x, DURING the job, while consuming
# the day's mail.  The suite did not write it.  Nothing in the suite can write it:
# every fixture lives under %TEMP%.
#
# Two lessons, both worth more than the rerun:
#   1. An invariant that counts is an invariant that lies.  Comparing the NUMBER
#      of dirty paths cannot tell "the thing I was watching changed" apart from
#      "something else moved at the same time".  This job compares the SET and
#      prints what entered and what left, so the answer names itself.
#   2. The chief must not write into the bridge folder while a job is measuring
#      it.  That is a discipline, not a bug in either script.
#
# WHAT IT RUNS: pf_git_sync_selftest.ps1 only.  No push, no commit, no gate, no
# pytest, no server, no client, no database, no scheduled task, no flag.  The
# only writes outside %TEMP% are sync.log (ignored, **/*.log) and the fixtures.
#
# EXIT: 0 if the suite passes AND the only paths that changed in the real repo
# are ones this job can account for.  43 otherwise.

$ErrorActionPreference = 'Continue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$self   = Join-Path $bridge 'pf_git_sync_selftest.ps1'

Write-Host '=== job 173 : rerun the refusal suite, compare sets not counts ==='
Write-Host ("time : " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
Write-Host ("host : " + $env:COMPUTERNAME + "  PSVersion " + $PSVersionTable.PSVersion.ToString())
Write-Host ''

if (-not (Test-Path -LiteralPath $self)) { Write-Host 'FATAL: selftest missing'; exit 39 }

$headBefore = ([string](& git -C $bridge --no-optional-locks rev-parse HEAD)).Trim()
$before = @(& git -C $bridge --no-optional-locks status --porcelain)
Write-Host ('HEAD before : ' + $headBefore)
Write-Host ('dirty before: ' + $before.Count)
foreach ($l in $before) { Write-Host ('   ' + $l) }
Write-Host ''

$out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $self 2>&1
$code = $LASTEXITCODE
foreach ($l in $out) { Write-Host ('  | ' + $l) }
Write-Host ('  exit = ' + $code)
Write-Host ''

$headAfter = ([string](& git -C $bridge --no-optional-locks rev-parse HEAD)).Trim()
$after = @(& git -C $bridge --no-optional-locks status --porcelain)
Write-Host ('HEAD after  : ' + $headAfter)
Write-Host ('dirty after : ' + $after.Count)
foreach ($l in $after) { Write-Host ('   ' + $l) }
Write-Host ''

$entered = @($after | Where-Object { $before -notcontains $_ })
$left    = @($before | Where-Object { $after -notcontains $_ })
Write-Host ('paths that ENTERED the dirty set during the suite : ' + $entered.Count)
foreach ($l in $entered) { Write-Host ('   + ' + $l) }
Write-Host ('paths that LEFT the dirty set during the suite    : ' + $left.Count)
foreach ($l in $left) { Write-Host ('   - ' + $l) }
Write-Host ''

$joined = ($out | Out-String)
$ok = $true
if ($code -ne 0) { Write-Host 'CHECK suite-exit-zero: FAIL'; $ok = $false } else { Write-Host 'CHECK suite-exit-zero: PASS' }
if ($joined -match 'SELFTEST_VERDICT=PASS') { Write-Host 'CHECK suite-verdict-pass: PASS' } else { Write-Host 'CHECK suite-verdict-pass: FAIL'; $ok = $false }
if ($joined -match 'SELFTEST_FAILED=0') { Write-Host 'CHECK zero-failed: PASS' } else { Write-Host 'CHECK zero-failed: FAIL'; $ok = $false }
if ($headBefore -eq $headAfter) { Write-Host 'CHECK real-repo-head-unmoved: PASS' } else { Write-Host 'CHECK real-repo-head-unmoved: FAIL'; $ok = $false }
if ($entered.Count -eq 0 -and $left.Count -eq 0) {
    Write-Host 'CHECK real-repo-worktree-identical: PASS'
} else {
    Write-Host 'CHECK real-repo-worktree-identical: FAIL - the paths are named above, judge them'
    $ok = $false
}

# The sync log must stay inside cp874's reach even after a suite that deliberately
# fed a non-ascii commit message through it.
$logf = Join-Path $bridge 'sync.log'
if (Test-Path -LiteralPath $logf) {
    $bytes = [System.IO.File]::ReadAllBytes($logf)
    $bad = 0
    foreach ($b in $bytes) { if ($b -gt 0x7E) { $bad++ } }
    Write-Host ('CHECK real-sync-log-ascii: ' + $(if ($bad -eq 0) { 'PASS' } else { 'FAIL' }) + '  (bytes=' + $bytes.Length + ' nonascii=' + $bad + ')')
    if ($bad -ne 0) { $ok = $false }
}

Write-Host ''
if (-not $ok) { Write-Host 'JOB173_VERDICT=FAIL'; exit 43 }
Write-Host 'JOB173_VERDICT=PASS'
exit 0

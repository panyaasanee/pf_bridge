# Job 172 - chief round 108.  PROVE the sync tooling before anyone installs it.
#
# WHY.  Panya approved DESIGN_R107_WINDOWS_SYNC.md in full at ~18:00 and added a
# condition that outranks every number in the design: "there must be a way to
# prove it works, not just install it and believe it", and specifically "prove it
# refuses a non-fast-forward push AND REPORTS IT - not silently".  Three files
# were written this round and NOT ONE of them has ever run: this bridge is a
# Linux sandbox with no PowerShell, so everything so far is static reading.
# This job is the first time any of it executes.
#
# WHAT IT RUNS, in order, each stage gating the next:
#   [A] ascii byte scan of all four new files (cp874 rule, round 86)
#   [B] PowerShell PARSER on the three .ps1 files - syntax errors caught here
#       cost nothing; caught by Task Scheduler they cost a silent dead task
#   [C] pf_git_sync.ps1 -SelfCheck against the REAL pf_bridge repo.  Read only:
#       check-ignore, status, rev-parse.  No fetch, no index write, no commit.
#   [D] pf_git_sync_selftest.ps1 - 14 tests on throwaway repositories under
#       %TEMP% with a bare repo standing in for GitHub.  This is where the
#       refusals are proven: flag held, oversize file, forbidden extension,
#       deletion, locally edited chief file, non-fast-forward with a rebase,
#       a real rebase conflict, the halt file, and the flag re-opened by a
#       negation rule in .gitignore.
#
# WHAT IT DOES NOT DO.  No push, no commit in any real repository, no gate, no
# pytest, no server, no client, no database, no scheduled task installed, no
# flag file touched.  Panya installs and Panya pushes.  The only writes outside
# %TEMP% are sync.log and sync_last_check.txt in pf_bridge\, both ignored by git.
#
# FLAGS.  Neither is needed and neither is taken: LOCK_GIT covers the git index
# and a gate run, and stage [C] only reads; LOCK_GAME covers ports, the server
# process, the game window and the database, none of which this job can reach.
#
# EXIT: 0 only if [A] [B] [C] [D] all pass.  40/41/42/43 name the stage that failed.

$ErrorActionPreference = 'Continue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$sync   = Join-Path $bridge 'pf_git_sync.ps1'
$self   = Join-Path $bridge 'pf_git_sync_selftest.ps1'
$setup  = Join-Path $bridge 'setup_git_sync_admin.ps1'
$bat    = Join-Path $bridge 'SETUP_GIT_SYNC.bat'

Write-Host '=== job 172 : prove the sync tooling (round 108) ==='
Write-Host ("time : " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
Write-Host ("host : " + $env:COMPUTERNAME + "  PSVersion " + $PSVersionTable.PSVersion.ToString())
Write-Host ''

$files = @($sync, $self, $setup, $bat)
foreach ($f in $files) {
    if (-not (Test-Path -LiteralPath $f)) { Write-Host ('FATAL: missing ' + $f); exit 39 }
}

# ---------------------------------------------------------------------------
# [A] ascii byte scan
# ---------------------------------------------------------------------------
Write-Host '=== [A] ASCII BYTE SCAN ==='
$asciiBad = 0
foreach ($f in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($f)
    $bad = 0
    $firstAt = -1
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        $b = $bytes[$i]
        if ($b -gt 0x7E -or ($b -lt 0x20 -and $b -ne 0x09 -and $b -ne 0x0A -and $b -ne 0x0D)) {
            $bad++
            if ($firstAt -lt 0) { $firstAt = $i }
        }
    }
    $bom = ''
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { $bom = '  HAS UTF8 BOM' }
    Write-Host ('  ' + (Split-Path -Leaf $f).PadRight(30) + ' bytes=' + $bytes.Length.ToString().PadLeft(7) + '  nonascii=' + $bad + $bom)
    $asciiBad += $bad
    if ($bom -ne '') { $asciiBad += 1 }
}
if ($asciiBad -gt 0) { Write-Host 'RESULT A: FAIL'; exit 40 }
Write-Host 'RESULT A: PASS'
Write-Host ''

# ---------------------------------------------------------------------------
# [B] parse the scripts without running them
# ---------------------------------------------------------------------------
Write-Host '=== [B] POWERSHELL PARSE ==='
$parseBad = 0
foreach ($f in @($sync, $self, $setup)) {
    $tokens = $null
    $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($f, [ref]$tokens, [ref]$errors)
    $n = 0
    if ($errors) { $n = @($errors).Count }
    Write-Host ('  ' + (Split-Path -Leaf $f).PadRight(30) + ' parse errors=' + $n)
    if ($n -gt 0) {
        $parseBad += $n
        foreach ($e in @($errors)) {
            Write-Host ('     line ' + $e.Extent.StartLineNumber + ' col ' + $e.Extent.StartColumnNumber + ' : ' + $e.Message)
        }
    }
}
if ($parseBad -gt 0) { Write-Host 'RESULT B: FAIL'; exit 41 }
Write-Host 'RESULT B: PASS'
Write-Host ''

# ---------------------------------------------------------------------------
# [C] self check against the real repository - read only
# ---------------------------------------------------------------------------
Write-Host '=== [C] SELFCHECK ON THE REAL pf_bridge REPO (read only) ==='
$before = (& git -C $bridge --no-optional-locks rev-parse HEAD)
$beforeStatus = @(& git -C $bridge --no-optional-locks status --porcelain)
Write-Host ('  HEAD before      : ' + ([string]$before).Trim())
Write-Host ('  dirty paths before: ' + $beforeStatus.Count)

$out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $sync -SelfCheck 2>&1
$code = $LASTEXITCODE
foreach ($l in $out) { Write-Host ('  | ' + $l) }
Write-Host ('  exit = ' + $code)

$after = (& git -C $bridge --no-optional-locks rev-parse HEAD)
$afterStatus = @(& git -C $bridge --no-optional-locks status --porcelain)
Write-Host ('  HEAD after       : ' + ([string]$after).Trim())
Write-Host ('  dirty paths after : ' + $afterStatus.Count)

$cOk = $true
if ($code -ne 0) { Write-Host '  CHECK exit-zero: FAIL'; $cOk = $false } else { Write-Host '  CHECK exit-zero: PASS' }
if (([string]$before).Trim() -ne ([string]$after).Trim()) { Write-Host '  CHECK head-unmoved: FAIL'; $cOk = $false } else { Write-Host '  CHECK head-unmoved: PASS' }
if ($beforeStatus.Count -ne $afterStatus.Count) { Write-Host '  CHECK worktree-unchanged: FAIL'; $cOk = $false } else { Write-Host '  CHECK worktree-unchanged: PASS' }
$joined = ($out | Out-String)
if ($joined -match 'SELFCHECK_OK' -or $joined -match 'SELFCHECK_WOULD_REFUSE') { Write-Host '  CHECK receipt-printed: PASS' } else { Write-Host '  CHECK receipt-printed: FAIL'; $cOk = $false }
if (-not $cOk) { Write-Host 'RESULT C: FAIL'; exit 42 }
Write-Host 'RESULT C: PASS'
Write-Host ''

# ---------------------------------------------------------------------------
# [D] the 14 refusal tests on throwaway repositories
# ---------------------------------------------------------------------------
Write-Host '=== [D] SELFTEST SUITE (fixtures under TEMP, bare repo as a fake GitHub) ==='
$out2 = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $self 2>&1
$code2 = $LASTEXITCODE
foreach ($l in $out2) { Write-Host ('  | ' + $l) }
Write-Host ('  exit = ' + $code2)

$joined2 = ($out2 | Out-String)
$dOk = $true
if ($code2 -ne 0) { $dOk = $false }
if ($joined2 -notmatch 'SELFTEST_VERDICT=PASS') { $dOk = $false }

# The real repository must be untouched by the suite as well.
$after2 = (& git -C $bridge --no-optional-locks rev-parse HEAD)
$afterStatus2 = @(& git -C $bridge --no-optional-locks status --porcelain)
if (([string]$after2).Trim() -ne ([string]$before).Trim()) { Write-Host '  CHECK real-repo-head-unmoved: FAIL'; $dOk = $false } else { Write-Host '  CHECK real-repo-head-unmoved: PASS' }
if ($afterStatus2.Count -ne $beforeStatus.Count) { Write-Host '  CHECK real-repo-worktree-unchanged: FAIL'; $dOk = $false } else { Write-Host '  CHECK real-repo-worktree-unchanged: PASS' }

if (-not $dOk) { Write-Host 'RESULT D: FAIL'; exit 43 }
Write-Host 'RESULT D: PASS'
Write-Host ''

Write-Host '=== VERDICT ==='
Write-Host 'JOB172_VERDICT=PASS  (ascii, parse, selfcheck, 14 refusal tests)'
Write-Host 'Nothing was pushed, committed, installed or booted by this job.'
exit 0

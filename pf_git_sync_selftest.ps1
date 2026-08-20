# pf_git_sync_selftest.ps1 - proof harness for pf_git_sync.ps1.  ASCII only.
#
# WHO ORDERED THIS AND WHY.  Chief wrote pf_git_sync.ps1 in round 108
# (2026-08-20) to carry mail between the Windows machine and a cloud chief
# routine over git, five minutes at a time, with no human watching most
# rounds.  A script that runs unattended and is trusted to touch git history
# only earns that trust once its refusals and its two hard-won bugfixes are
# demonstrated, not just read.  This file is that demonstration: Panya's and
# the chief's receipt that the properties written into pf_git_sync.ps1's own
# header actually hold, before that script is ever pointed at the real
# pf_bridge or ServerProject repositories or left running on a schedule.
#
# WHAT THE 14 TESTS PROVE (see the MAIN section at the bottom and each
# Test-Tn function for the exact scenario):
#   T1  a new file under notes_to_chief really reaches the far side
#   T2  a clean rerun commits nothing new
#   T3  LOCK_GIT.txt written with a UTF-8 BOM is still read as HELD - this is
#       the exact bug that broke done\169_*.ps1 on this machine; if the BOM
#       strip in pf_git_sync.ps1 ever regresses, this test catches it
#   T4  one oversized file cancels the whole commit, not just itself
#   T5  a forbidden extension is refused
#   T6  a deletion inside the allowlist is refused
#   T7  a chief-owned file edited locally blocks the pull, loudly, and loses
#       nothing - the edit is still on disk afterward
#   T8  a losing race (push rejected as non-fast-forward) is not silent - it
#       is rebased once and retried, and the retry is visible in sync.log.
#       Panya asked specifically to see this one proven, not assumed
#   T9  a genuine rebase conflict halts permanently and leaves no rebase in
#       progress behind it
#   T10 a halt file already on disk stops the very next round before it does
#       anything at all
#   T11 a .gitignore that stops covering the flag files is treated as a
#       permanent halt, because a flag that can travel between machines
#       protects nothing
#   T11b a baseline .gitignore with one trailing negation line
#       (!/LOCK_GAME.txt) reopens that single flag file, and guard [0] must
#       still halt on it, even though `git check-ignore -v` still prints a
#       line naming the file (the deciding pattern, which happens to be the
#       negation itself).  This is a regression test of guard [0]'s own
#       fix - the first version of the guard judged by scanning -v output
#       for the filename and would have been fooled by exactly this case;
#       the fixed guard checks the exit code of `check-ignore -q` per file
#       instead and is not fooled.  See Test-T11b below for the full story
#   T12 sync.log never carries a byte above 0x7E, even when the chief's own
#       commit message does - this is the second hard-won bug (round 86, a
#       non-ascii console byte turning the gate red on Windows only).  This
#       check is also applied, generically, to every other test's sync.log
#       as it is torn down, so T12 is the positive control, not the only
#       place the property is checked
#   T13 -DryRun really is dry: no commit, no push, and the real heartbeat
#       file is left untouched in favor of a separate .dryrun file
#
# WHY EVERYTHING LIVES UNDER $env:TEMP.  This harness may not commit, push,
# or so much as look at the real pf_bridge or ServerProject repositories,
# the canonical database, LOCK_*.txt, GAME_TEST_QUEUE.md,
# CHIEF_CONTINUATION.md, the real .gitignore, or inbox/outbox/done.  So
# every test builds its own throwaway "GitHub" - a bare repo under
# $env:TEMP - plus two clones of it: machine\ (stands in for -BridgeRepo,
# this laptop) and chief\ (stands in for the cloud chief's clone).
# pf_git_sync.ps1 is always invoked with -BridgeRepo pointing at that
# machine\ clone, -ServerRepo pointing at a path under the same fixture that
# never exists, and -NoServer on top of that as a second, redundant
# guarantee that step [5] - the one that touches the ServerProject repo -
# never runs during a self-test.  A fixture is deleted the moment its test
# passes; a fixture whose test fails is left on disk and its path is
# printed, so a human can look at exactly the git state that produced the
# failure.
#
# HOW A VERDICT IS DECIDED.  pf_git_sync.ps1 prints SYNC_MODE=, SYNC_VERDICT=
# and SYNC_EXIT= as its last three lines, and also sets the process exit
# code via `exit <n>`.  Every test here launches it as a fresh child process
# (powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...), captures
# $LASTEXITCODE on the very next line before anything else can overwrite it,
# and compares that exit code and the SYNC_VERDICT= string against what the
# scenario should produce.  Nothing here trusts $? or -ErrorAction Stop for
# a verdict; those are used, if at all, only while building throwaway
# fixtures, never to judge the script under test.
#
# ONE NON-OBVIOUS THING THIS HARNESS HAD TO GET RIGHT.  An earlier version
# of pf_git_sync.ps1's guard [0] decided "a flag file is still ignored" by
# checking whether the file's name appeared anywhere in
# `git check-ignore -v --no-index` output.  Under the "/* then ! to reopen
# paths" .gitignore style this project uses, EVERY root-level filename
# appears in that verbose output, because verbose mode prints the deciding
# pattern even when that pattern is a negation (a file that is explicitly
# un-ignored still produces a line).  This was checked by hand against a
# real git before this file was written.  So T11 could not prove its point
# by adding a `!/LOCK_GAME.txt` line - that would still show up in the
# verbose output and the old guard would not have fired.  T11 instead
# replaces the fixture's .gitignore with one that has no rule at all,
# positive or negative, covering LOCK_GAME.txt - the only case where the
# filename is genuinely absent from `check-ignore -v` output.  See Test-T11
# below for the exact fixture content.
#
# Chief has since rewritten guard [0]: it no longer reads -v output at all.
# It now calls `git check-ignore -q --no-index -- <file>` once per flag file
# and judges only the exit code (0 = ignored, 1 = not ignored), which is not
# fooled by a negation line the way the old -v scan was.  T11b below is the
# proof for exactly that negation case - a baseline .gitignore plus a
# trailing `!/LOCK_GAME.txt` line, which still prints a line naming the file
# in -v output but must still be caught as "not ignored" by the fixed guard.
# T11b is therefore a regression test of guard [0]'s own fix, not a test of
# any particular .gitignore content.  See Test-T11b below.
#
# EXIT CODES OF THIS HARNESS (not of pf_git_sync.ps1 - see that script's own
# header for its 0/2/3/4/5/6/7/9):
#   0  every test passed
#   1  at least one test failed, or the harness could not even start

# ---------------------------------------------------------------------------
# top-level state
# ---------------------------------------------------------------------------

$script:SutPath  = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\pf_git_sync.ps1'
$script:TempRoot = Join-Path $env:TEMP ('pf_git_sync_selftest_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '_' + (Get-Random -Maximum 99999))
$script:Results  = @()
$script:TestPass = $true
$script:TestFixtureRoot = $null

# The baseline .gitignore every fixture starts from.  Verified by hand
# against a real git before this file was written:
#   - LOCK_GAME.txt, LOCK_GIT.txt, PANYA_PRESENT.txt are genuinely ignored
#     (matched by their own /LOCK_*.txt / /PANYA_PRESENT.txt lines, not by
#     the catch-all, so check-ignore -v shows the real ignore pattern)
#   - notes_to_chief/**, evidence_screens/**, *.md, and .gitignore itself
#     are reopened and are NOT ignored
$script:BaselineGitignore = @(
    '/*'
    '!/notes_to_chief'
    '!/notes_to_chief/**'
    '!/evidence_screens'
    '!/evidence_screens/**'
    '!/CHIEF_CONTINUATION.md'
    '!/GAME_TEST_QUEUE.md'
    '!/.gitignore'
    '!*.md'
    '/LOCK_GAME.txt'
    '/LOCK_GIT.txt'
    '/PANYA_PRESENT.txt'
)

# ---------------------------------------------------------------------------
# small git helpers - these run ordinary git commands against throwaway
# fixtures under $env:TEMP.  They are not the script under test; they build
# the world the script under test is dropped into.
# ---------------------------------------------------------------------------

function GitQNoRepo([string[]]$cmdArgs) {
    $raw = & git @cmdArgs 2>&1
    $code = $LASTEXITCODE
    $text = ''
    if ($null -ne $raw) { $text = ($raw | Out-String) }
    return [pscustomobject]@{ Code = $code; Out = $text }
}

function GitQ([string]$repo, [string[]]$cmdArgs) {
    $all = @('-C', $repo) + $cmdArgs
    $raw = & git @all 2>&1
    $code = $LASTEXITCODE
    $text = ''
    if ($null -ne $raw) { $text = ($raw | Out-String) }
    return [pscustomobject]@{ Code = $code; Out = $text }
}

function Set-GitIdentity([string]$repo) {
    GitQ $repo @('config', 'user.email', 'selftest@pf.invalid') | Out-Null
    GitQ $repo @('config', 'user.name', 'PF Selftest Harness') | Out-Null
    # core.autocrlf false: keep exact bytes we write, so size math (T4) and
    # exact-content comparisons (T7) are not disturbed by line-ending
    # rewriting on checkout.
    GitQ $repo @('config', 'core.autocrlf', 'false') | Out-Null
    GitQ $repo @('config', 'commit.gpgsign', 'false') | Out-Null
}

function New-GitBareRepo([string]$path) {
    $r1 = GitQNoRepo @('init', '--bare', '--initial-branch=main', $path)
    if ($r1.Code -ne 0) {
        # Older git (pre 2.28) does not know --initial-branch.  Fall back to
        # a plain bare init and point HEAD at refs/heads/main by hand,
        # before anything is pushed, so every later clone of this bare repo
        # also defaults to main instead of master.
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction SilentlyContinue
        }
        $r2 = GitQNoRepo @('init', '--bare', $path)
        if ($r2.Code -ne 0) { throw ('git init --bare failed: ' + $r2.Out) }
        $r3 = GitQ $path @('symbolic-ref', 'HEAD', 'refs/heads/main')
        if ($r3.Code -ne 0) { throw ('symbolic-ref on bare repo failed: ' + $r3.Out) }
    }
}

function New-GitWorkRepo([string]$path) {
    $r1 = GitQNoRepo @('init', '--initial-branch=main', $path)
    if ($r1.Code -ne 0) {
        # Same fallback as New-GitBareRepo, for a normal (non-bare) worktree.
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction SilentlyContinue
        }
        $r2 = GitQNoRepo @('init', $path)
        if ($r2.Code -ne 0) { throw ('git init failed: ' + $r2.Out) }
        $r3 = GitQ $path @('symbolic-ref', 'HEAD', 'refs/heads/main')
        if ($r3.Code -ne 0) { throw ('symbolic-ref on work repo failed: ' + $r3.Out) }
    }
    Set-GitIdentity $path
}

function Write-BaselineFixtureFiles([string]$repo) {
    Set-Content -LiteralPath (Join-Path $repo '.gitignore') -Value $script:BaselineGitignore -Encoding ascii

    $notesDir = Join-Path $repo 'notes_to_chief'
    $evDir    = Join-Path $repo 'evidence_screens'
    New-Item -ItemType Directory -Path $notesDir -Force | Out-Null
    New-Item -ItemType Directory -Path $evDir -Force | Out-Null

    Set-Content -LiteralPath (Join-Path $notesDir 'seed_note.md') -Value 'seed note, already committed when the fixture is built' -Encoding ascii
    Set-Content -LiteralPath (Join-Path $evDir 'placeholder.txt') -Value 'placeholder so evidence_screens exists as a tracked directory' -Encoding ascii
    Set-Content -LiteralPath (Join-Path $repo 'CHIEF_CONTINUATION.md') -Value @('CHIEF CONTINUATION - fixture seed content', 'this line exists so a real edit has something to change') -Encoding ascii
    Set-Content -LiteralPath (Join-Path $repo 'GAME_TEST_QUEUE.md') -Value @('GAME TEST QUEUE - fixture seed content') -Encoding ascii
}

# Builds one throwaway world: bare.git (the fake GitHub), seed (used once,
# to originate the initial commit), machine (this is what -BridgeRepo points
# at), chief (the cloud chief's clone).  Every test gets its own fixture
# under $script:TempRoot\<Id>, so tests cannot contaminate each other.
function New-Fixture([string]$Id) {
    $root = Join-Path $script:TempRoot $Id
    if (Test-Path -LiteralPath $root) {
        Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
    }
    New-Item -ItemType Directory -Path $root -Force | Out-Null

    $bare    = Join-Path $root 'bare.git'
    $seed    = Join-Path $root 'seed'
    $machine = Join-Path $root 'machine'
    $chief   = Join-Path $root 'chief'

    New-GitBareRepo $bare
    New-GitWorkRepo $seed
    Write-BaselineFixtureFiles $seed

    $ad = GitQ $seed @('add', '-A')
    if ($ad.Code -ne 0) { throw ('fixture seed add failed: ' + $ad.Out) }
    $cm = GitQ $seed @('commit', '-m', 'seed: initial fixture content')
    if ($cm.Code -ne 0) { throw ('fixture seed commit failed: ' + $cm.Out) }
    $ra = GitQ $seed @('remote', 'add', 'origin', $bare)
    if ($ra.Code -ne 0) { throw ('fixture remote add failed: ' + $ra.Out) }
    $ps = GitQ $seed @('push', '-u', 'origin', 'main')
    if ($ps.Code -ne 0) { throw ('fixture seed push failed: ' + $ps.Out) }

    $cl1 = GitQ $root @('clone', $bare, $machine)
    if ($cl1.Code -ne 0) { throw ('fixture clone machine failed: ' + $cl1.Out) }
    Set-GitIdentity $machine

    $cl2 = GitQ $root @('clone', $bare, $chief)
    if ($cl2.Code -ne 0) { throw ('fixture clone chief failed: ' + $cl2.Out) }
    Set-GitIdentity $chief

    return [pscustomobject]@{
        Root    = $root
        Bare    = $bare
        Seed    = $seed
        Machine = $machine
        Chief   = $chief
    }
}

# ---------------------------------------------------------------------------
# helpers for reading fixture state back out
# ---------------------------------------------------------------------------

function Get-CommitCount([string]$repo, [string]$rev) {
    $r = GitQ $repo @('rev-list', '--count', $rev)
    if ($r.Code -ne 0) { return -1 }
    return [int]($r.Out.Trim())
}

function Get-TreeFiles([string]$repo, [string]$rev) {
    $r = GitQ $repo @('ls-tree', '-r', '--name-only', $rev)
    return @($r.Out -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
}

function Get-FileText([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return $null }
    return [System.IO.File]::ReadAllText($path)
}

# T12's core assertion, applied generically to every test's sync.log too
# (see Run-Test below) so T12 is a positive control, not the only place this
# is checked.
function Test-FileIsAsciiBytes([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return $true }
    $bytes = [System.IO.File]::ReadAllBytes($path)
    foreach ($b in $bytes) {
        if ($b -gt 0x7E) { return $false }
    }
    return $true
}

# ---------------------------------------------------------------------------
# invoking the script under test
# ---------------------------------------------------------------------------

function Invoke-Sut {
    param(
        [string]$BridgeRepo,
        [string]$ServerRepoOverride,
        [switch]$DryRun
    )
    $sutArgs = @(
        '-NoProfile'
        '-ExecutionPolicy'
        'Bypass'
        '-File'
        $script:SutPath
        '-BridgeRepo'
        $BridgeRepo
        '-ServerRepo'
        $ServerRepoOverride
        '-Branch'
        'main'
        '-NoServer'
    )
    if ($DryRun) { $sutArgs += '-DryRun' }

    $raw = & powershell.exe @sutArgs 2>&1
    # $LASTEXITCODE must be read on the very next line - any other command,
    # even a harmless-looking one, can overwrite it before we get to it.
    $code = $LASTEXITCODE
    $outText = ($raw | Out-String)

    $verdict = ''
    if ($outText -match 'SYNC_VERDICT=(\S+)') { $verdict = $matches[1] }
    $reportedExit = ''
    if ($outText -match 'SYNC_EXIT=(\S+)') { $reportedExit = $matches[1] }

    return [pscustomobject]@{
        Code         = $code
        ReportedExit = $reportedExit
        Verdict      = $verdict
        Out          = $outText
    }
}

# ---------------------------------------------------------------------------
# assertion / reporting helpers
# ---------------------------------------------------------------------------

function Check([string]$label, [bool]$cond) {
    if ($cond) {
        Write-Output ('CHECK ' + $label + ': PASS')
    } else {
        Write-Output ('CHECK ' + $label + ': FAIL')
        $script:TestPass = $false
    }
}

function Report-Verdict([int]$expectExit, [string]$expectVerdict, [pscustomobject]$res) {
    Write-Output ('EXPECTED exit=' + $expectExit + ' verdict=' + $expectVerdict)
    Write-Output ('ACTUAL   exit=' + $res.Code + ' verdict=' + $res.Verdict)
    $exitOk = ($res.Code -eq $expectExit)
    $verdictOk = ($res.Verdict -eq $expectVerdict)
    Check 'exit-code' $exitOk
    Check 'verdict' $verdictOk
    Check 'reported-exit-matches-process-exit' ($res.ReportedExit -eq ([string]$res.Code))
    if ((-not $exitOk) -or (-not $verdictOk)) {
        Write-Output '--- captured SUT output (exit/verdict mismatch) ---'
        Write-Output $res.Out
        Write-Output '--- end captured SUT output ---'
    }
}

# ---------------------------------------------------------------------------
# T1 .. T13 (plus T11b)
# ---------------------------------------------------------------------------

function Test-T1 {
    Write-Output 'scenario: drop one new file under notes_to_chief and sync once'
    $ctx = New-Fixture 'T1'
    $script:TestFixtureRoot = $ctx.Root

    $newFile = Join-Path $ctx.Machine 'notes_to_chief\NEW_FROM_MACHINE_T1.md'
    Set-Content -LiteralPath $newFile -Value 'T1 happy path payload' -Encoding ascii

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 0 'OK' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    Check 'bare-gained-one-commit' ($countAfter -eq ($countBefore + 1))

    $tree = Get-TreeFiles $ctx.Bare 'main'
    Check 'new-file-present-in-bare' ($tree -contains 'notes_to_chief/NEW_FROM_MACHINE_T1.md')
}

function Test-T2 {
    Write-Output 'scenario: run once on a clean fixture, then run again immediately - nothing changed'
    $ctx = New-Fixture 'T2'
    $script:TestFixtureRoot = $ctx.Root

    $countBefore = Get-CommitCount $ctx.Bare 'main'

    $res1 = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Write-Output 'first run:'
    Report-Verdict 0 'OK' $res1
    $countAfterFirst = Get-CommitCount $ctx.Bare 'main'

    $res2 = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Write-Output 'second run (immediate rerun):'
    Report-Verdict 0 'OK' $res2
    $countAfterSecond = Get-CommitCount $ctx.Bare 'main'

    Check 'no-commit-created-by-either-run' ($countBefore -eq $countAfterFirst -and $countAfterFirst -eq $countAfterSecond)
}

function Test-T3 {
    Write-Output 'scenario: LOCK_GIT.txt HELD, written with a UTF-8 BOM, plus a pending new file'
    $ctx = New-Fixture 'T3'
    $script:TestFixtureRoot = $ctx.Root

    $lockPath = Join-Path $ctx.Machine 'LOCK_GIT.txt'
    $enc = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText($lockPath, "HELD: T3 selftest`r`n", $enc)

    $pending = Join-Path $ctx.Machine 'notes_to_chief\SHOULD_NOT_SYNC_T3.md'
    Set-Content -LiteralPath $pending -Value 'must not be committed while LOCK_GIT is held' -Encoding ascii

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 0 'SKIP_LOCK_GIT_HELD' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    Check 'no-new-commit-on-bare-while-lock-held' ($countBefore -eq $countAfter)

    $localCount = Get-CommitCount $ctx.Machine 'HEAD'
    Check 'machine-head-did-not-move' ($localCount -eq $countBefore)
}

function Test-T4 {
    Write-Output 'scenario: one 3 MB file plus one normal file - the whole commit must be refused'
    $ctx = New-Fixture 'T4'
    $script:TestFixtureRoot = $ctx.Root

    $bigPath = Join-Path $ctx.Machine 'notes_to_chief\BIG_FILE_T4.dat'
    $bigContent = 'A' * (3 * 1024 * 1024)
    [System.IO.File]::WriteAllText($bigPath, $bigContent, [System.Text.Encoding]::ASCII)

    $normalPath = Join-Path $ctx.Machine 'notes_to_chief\NORMAL_T4.md'
    Set-Content -LiteralPath $normalPath -Value 'a normal small file that must not ride along' -Encoding ascii

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 5 'REFUSED_PROPRIETARY' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    Check 'no-new-commit-at-all' ($countBefore -eq $countAfter)

    $tree = Get-TreeFiles $ctx.Bare 'main'
    Check 'normal-file-not-pushed-either' (-not ($tree -contains 'notes_to_chief/NORMAL_T4.md'))
}

function Test-T5 {
    Write-Output 'scenario: a forbidden extension file (.sqlite3) under notes_to_chief'
    $ctx = New-Fixture 'T5'
    $script:TestFixtureRoot = $ctx.Root

    $badPath = Join-Path $ctx.Machine 'notes_to_chief\something.sqlite3'
    Set-Content -LiteralPath $badPath -Value 'pretend db bytes' -Encoding ascii

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 5 'REFUSED_PROPRIETARY' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    Check 'no-new-commit' ($countBefore -eq $countAfter)
}

function Test-T6 {
    Write-Output 'scenario: delete the already-committed seed file under notes_to_chief'
    $ctx = New-Fixture 'T6'
    $script:TestFixtureRoot = $ctx.Root

    $seedNote = Join-Path $ctx.Machine 'notes_to_chief\seed_note.md'
    Remove-Item -LiteralPath $seedNote -Force

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 5 'REFUSED_DELETION' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    Check 'no-new-commit' ($countBefore -eq $countAfter)
}

function Test-T7 {
    Write-Output 'scenario: chief edits CHIEF_CONTINUATION.md and pushes; machine edits the same file locally, uncommitted'
    $ctx = New-Fixture 'T7'
    $script:TestFixtureRoot = $ctx.Root

    $chiefPath = Join-Path $ctx.Chief 'CHIEF_CONTINUATION.md'
    Set-Content -LiteralPath $chiefPath -Value @('CHIEF CONTINUATION - fixture seed content', 'line 2 CHANGED BY CHIEF') -Encoding ascii
    GitQ $ctx.Chief @('add', '--', 'CHIEF_CONTINUATION.md') | Out-Null
    $cm = GitQ $ctx.Chief @('commit', '-m', 'chief: edits its own file')
    if ($cm.Code -ne 0) { throw ('T7 chief commit failed: ' + $cm.Out) }
    $ps = GitQ $ctx.Chief @('push', 'origin', 'main')
    if ($ps.Code -ne 0) { throw ('T7 chief push failed: ' + $ps.Out) }

    $machinePath = Join-Path $ctx.Machine 'CHIEF_CONTINUATION.md'
    Set-Content -LiteralPath $machinePath -Value @('CHIEF CONTINUATION - fixture seed content', 'line 2 EDITED LOCALLY BY MACHINE, DO NOT LOSE THIS') -Encoding ascii
    $expectedLocalEdit = Get-FileText $machinePath

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 4 'STOP_LOCAL_EDITS_BLOCK_PULL' $res

    $attnPath = Join-Path $ctx.Machine 'SYNC_ATTENTION.txt'
    Check 'attention-file-exists' (Test-Path -LiteralPath $attnPath)

    $actualLocalEdit = Get-FileText $machinePath
    Check 'local-edit-still-on-disk' ($actualLocalEdit -eq $expectedLocalEdit)
}

function Test-T8 {
    Write-Output 'scenario: chief pushes a new file first; machine already committed its own new file (different name) - push must be rejected, rebased once, and retried'
    $ctx = New-Fixture 'T8'
    $script:TestFixtureRoot = $ctx.Root

    $chiefFile = Join-Path $ctx.Chief 'notes_to_chief\FROM_CHIEF_T8.md'
    Set-Content -LiteralPath $chiefFile -Value 'chief letter for T8' -Encoding ascii
    GitQ $ctx.Chief @('add', '--', 'notes_to_chief/FROM_CHIEF_T8.md') | Out-Null
    $cm = GitQ $ctx.Chief @('commit', '-m', 'chief: new letter T8')
    if ($cm.Code -ne 0) { throw ('T8 chief commit failed: ' + $cm.Out) }
    $ps = GitQ $ctx.Chief @('push', 'origin', 'main')
    if ($ps.Code -ne 0) { throw ('T8 chief push failed: ' + $ps.Out) }

    $machineFile = Join-Path $ctx.Machine 'notes_to_chief\NEW_FROM_MACHINE_T8.md'
    Set-Content -LiteralPath $machineFile -Value 'machine letter for T8, committed by hand to simulate a leftover local commit' -Encoding ascii
    GitQ $ctx.Machine @('add', '--', 'notes_to_chief/NEW_FROM_MACHINE_T8.md') | Out-Null
    $cm2 = GitQ $ctx.Machine @('commit', '-m', 'machine: local commit made before this sync round')
    if ($cm2.Code -ne 0) { throw ('T8 machine commit failed: ' + $cm2.Out) }

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 0 'OK' $res

    $logPath = Join-Path $ctx.Machine 'sync.log'
    $logText = ''
    if (Test-Path -LiteralPath $logPath) { $logText = [System.IO.File]::ReadAllText($logPath) }
    Check 'log-mentions-non-fast-forward-rejection' ($logText -match 'rejected as non-fast-forward')
    Check 'log-mentions-pushed-after-rebase' ($logText -match 'pushed after one rebase')

    $tree = Get-TreeFiles $ctx.Bare 'main'
    Check 'bare-has-chiefs-file' ($tree -contains 'notes_to_chief/FROM_CHIEF_T8.md')
    Check 'bare-has-machines-file' ($tree -contains 'notes_to_chief/NEW_FROM_MACHINE_T8.md')
}

function Test-T9 {
    Write-Output 'scenario: chief and machine both add a same-named file with different content - rebase must conflict and halt'
    $ctx = New-Fixture 'T9'
    $script:TestFixtureRoot = $ctx.Root

    $sharedRel = 'notes_to_chief/SHARED_T9.md'

    $chiefFile = Join-Path $ctx.Chief 'notes_to_chief\SHARED_T9.md'
    Set-Content -LiteralPath $chiefFile -Value 'chief version of the shared file' -Encoding ascii
    GitQ $ctx.Chief @('add', '--', $sharedRel) | Out-Null
    $cm = GitQ $ctx.Chief @('commit', '-m', 'chief: shared file T9')
    if ($cm.Code -ne 0) { throw ('T9 chief commit failed: ' + $cm.Out) }
    $ps = GitQ $ctx.Chief @('push', 'origin', 'main')
    if ($ps.Code -ne 0) { throw ('T9 chief push failed: ' + $ps.Out) }

    $machineFile = Join-Path $ctx.Machine 'notes_to_chief\SHARED_T9.md'
    Set-Content -LiteralPath $machineFile -Value 'machine version of the shared file, conflict bait' -Encoding ascii
    GitQ $ctx.Machine @('add', '--', $sharedRel) | Out-Null
    $cm2 = GitQ $ctx.Machine @('commit', '-m', 'machine: shared file T9, different content on purpose')
    if ($cm2.Code -ne 0) { throw ('T9 machine commit failed: ' + $cm2.Out) }

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 7 'HALT_REBASE_CONFLICT' $res

    $haltPath = Join-Path $ctx.Machine 'SYNC_NEEDS_HUMAN.txt'
    Check 'needs-human-file-exists' (Test-Path -LiteralPath $haltPath)

    $rh = GitQ $ctx.Machine @('rev-parse', '--verify', 'REBASE_HEAD')
    Check 'no-rebase-head-left-behind' ($rh.Code -ne 0)

    $rmPath = Join-Path $ctx.Machine '.git\rebase-merge'
    $raPath = Join-Path $ctx.Machine '.git\rebase-apply'
    Check 'no-rebase-merge-dir' (-not (Test-Path -LiteralPath $rmPath))
    Check 'no-rebase-apply-dir' (-not (Test-Path -LiteralPath $raPath))
}

function Test-T10 {
    Write-Output 'scenario: SYNC_NEEDS_HUMAN.txt already exists from a previous halted round - the script must refuse to run at all'
    $ctx = New-Fixture 'T10'
    $script:TestFixtureRoot = $ctx.Root

    $haltPath = Join-Path $ctx.Machine 'SYNC_NEEDS_HUMAN.txt'
    Set-Content -LiteralPath $haltPath -Value @('SYNC HALTED  selftest T10 seed', 'left here by the selftest, not by a real round') -Encoding ascii

    $decoyPath = Join-Path $ctx.Machine 'notes_to_chief\SHOULD_NOT_SYNC_T10.md'
    Set-Content -LiteralPath $decoyPath -Value 'must not be committed while halted' -Encoding ascii

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 3 'HALTED_NEEDS_HUMAN' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    Check 'no-new-commit-while-halted' ($countBefore -eq $countAfter)
}

function Test-T11 {
    # See the header comment block at the top of this file for why this
    # fixture's .gitignore drops the /* catch-all entirely instead of adding
    # a `!/LOCK_GAME.txt` negation - a negation would still show up in
    # `git check-ignore -v` output and the real guard would not fire.
    Write-Output 'scenario: fixture .gitignore no longer has any rule at all covering LOCK_GAME.txt'
    $ctx = New-Fixture 'T11'
    $script:TestFixtureRoot = $ctx.Root

    $giPath = Join-Path $ctx.Machine '.gitignore'
    $broken = @(
        '/LOCK_GIT.txt'
        '/PANYA_PRESENT.txt'
    )
    Set-Content -LiteralPath $giPath -Value $broken -Encoding ascii

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 2 'HALT_FLAGS_NOT_IGNORED' $res

    $haltPath = Join-Path $ctx.Machine 'SYNC_NEEDS_HUMAN.txt'
    Check 'needs-human-file-exists' (Test-Path -LiteralPath $haltPath)
}

function Test-T11b {
    # THIS IS THE TEST THAT NEARLY GOT MISSED.  The first version of guard
    # [0] judged "is this flag file still ignored" by scanning the text of
    # `git check-ignore -v --no-index` for the file's name.  But verbose
    # check-ignore prints the deciding pattern even when that pattern is a
    # negation - a `!` rule that reopens a path still produces a line naming
    # the file.  So a flag file that had been quietly reopened by a
    # negation, and that a chief-side pull could freely overwrite, still
    # matched the old guard's "name appears in output" test and was waved
    # through in silence.  That is a real hole: LOCK_GAME.txt losing its
    # ignore status is exactly the case guard [0] exists to catch, and the
    # old guard would not have caught it in this specific shape.
    #
    # Chief's fix replaced that text scan with a per-file exit-code check:
    # `git check-ignore -q --no-index -- <file>`, 0 means ignored, 1 means
    # not ignored, nothing about the printed pattern text matters anymore.
    # This test is the proof of that fix, and a regression test of guard
    # [0] itself, not of any particular .gitignore content: it starts from
    # the normal baseline .gitignore (which genuinely ignores all three flag
    # files) and appends one trailing negation line, !/LOCK_GAME.txt, so
    # LOCK_GAME.txt is genuinely not ignored anymore while check-ignore -v
    # still prints a line naming it (the negation pattern that decided it).
    # If guard [0] ever regresses back to reading -v text instead of the -q
    # exit code, this is the test that catches it - T11 alone would not,
    # because T11's fixture removes every rule covering the file instead of
    # reopening it with a negation.
    Write-Output 'scenario: baseline .gitignore plus a trailing !/LOCK_GAME.txt negation reopens that one flag, while check-ignore -v still prints a line naming it'
    $ctx = New-Fixture 'T11b'
    $script:TestFixtureRoot = $ctx.Root

    $giPath = Join-Path $ctx.Machine '.gitignore'
    $reopened = $script:BaselineGitignore + @('!/LOCK_GAME.txt')
    Set-Content -LiteralPath $giPath -Value $reopened -Encoding ascii

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 2 'HALT_FLAGS_NOT_IGNORED' $res

    $haltPath = Join-Path $ctx.Machine 'SYNC_NEEDS_HUMAN.txt'
    Check 'needs-human-file-exists' (Test-Path -LiteralPath $haltPath)
}

function Test-T12 {
    Write-Output 'scenario: chief pushes with a non-ascii character in the commit message - sync.log must stay pure ascii bytes'
    $ctx = New-Fixture 'T12'
    $script:TestFixtureRoot = $ctx.Root

    $chiefFile = Join-Path $ctx.Chief 'notes_to_chief\FROM_CHIEF_T12.md'
    Set-Content -LiteralPath $chiefFile -Value 'chief letter for T12' -Encoding ascii
    GitQ $ctx.Chief @('add', '--', 'notes_to_chief/FROM_CHIEF_T12.md') | Out-Null
    $lure = [string]([char]0x00E9)
    $msg = 'chief: letter with a lure character ' + $lure + ' in the commit message'
    $cm = GitQ $ctx.Chief @('commit', '-m', $msg)
    if ($cm.Code -ne 0) { throw ('T12 chief commit failed: ' + $cm.Out) }
    $ps = GitQ $ctx.Chief @('push', 'origin', 'main')
    if ($ps.Code -ne 0) { throw ('T12 chief push failed: ' + $ps.Out) }

    $machineFile = Join-Path $ctx.Machine 'notes_to_chief\NEW_FROM_MACHINE_T12.md'
    Set-Content -LiteralPath $machineFile -Value 'machine letter for T12' -Encoding ascii

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server')
    Report-Verdict 0 'OK' $res

    $logPath = Join-Path $ctx.Machine 'sync.log'
    Check 'sync-log-exists' (Test-Path -LiteralPath $logPath)
    $asciiOk = Test-FileIsAsciiBytes $logPath
    Check 'sync-log-no-byte-above-0x7E' $asciiOk
}

function Test-T13 {
    Write-Output 'scenario: -DryRun with a pending new file must not commit, push, or write the real heartbeat file'
    $ctx = New-Fixture 'T13'
    $script:TestFixtureRoot = $ctx.Root

    $newFile = Join-Path $ctx.Machine 'notes_to_chief\NEW_FROM_MACHINE_T13.md'
    Set-Content -LiteralPath $newFile -Value 'T13 dry run payload' -Encoding ascii

    $countBefore = Get-CommitCount $ctx.Bare 'main'
    $localCountBefore = Get-CommitCount $ctx.Machine 'HEAD'

    $res = Invoke-Sut -BridgeRepo $ctx.Machine -ServerRepoOverride (Join-Path $ctx.Root 'no_server') -DryRun
    Report-Verdict 0 'OK' $res

    $countAfter = Get-CommitCount $ctx.Bare 'main'
    $localCountAfter = Get-CommitCount $ctx.Machine 'HEAD'
    Check 'bare-unchanged' ($countBefore -eq $countAfter)
    Check 'machine-head-unchanged' ($localCountBefore -eq $localCountAfter)

    $realHb = Join-Path $ctx.Machine 'sync_last_check.txt'
    $dryHb  = Join-Path $ctx.Machine 'sync_last_check.dryrun.txt'
    Check 'real-heartbeat-not-written' (-not (Test-Path -LiteralPath $realHb))
    Check 'dryrun-heartbeat-written' (Test-Path -LiteralPath $dryHb)
}

# ---------------------------------------------------------------------------
# test runner: wraps each test in try/catch so one failure cannot take the
# rest of the suite down, prints the required block format, applies the
# generic ascii-log check (see T12's comment), and cleans up on PASS only.
# ---------------------------------------------------------------------------

function Run-Test([string]$Id, [string]$Name, [scriptblock]$Body) {
    Write-Output ''
    Write-Output ('--- ' + $Id + ' ' + $Name + ' ---')
    $script:TestPass = $true
    $script:TestFixtureRoot = $null
    try {
        & $Body
    } catch {
        $script:TestPass = $false
        Write-Output ('EXCEPTION: ' + $_.Exception.Message)
    }

    if ($script:TestFixtureRoot) {
        $logPath = Join-Path $script:TestFixtureRoot 'machine\sync.log'
        try {
            if (Test-Path -LiteralPath $logPath) {
                $asciiOk = Test-FileIsAsciiBytes $logPath
                Check 'sync-log-is-pure-ascii-bytes' $asciiOk
            }
        } catch {
            Write-Output ('CHECK sync-log-is-pure-ascii-bytes: FAIL (exception: ' + $_.Exception.Message + ')')
            $script:TestPass = $false
        }
    }

    if ($script:TestPass) {
        Write-Output ('RESULT ' + $Id + ': PASS')
        if ($script:TestFixtureRoot -and (Test-Path -LiteralPath $script:TestFixtureRoot)) {
            Remove-Item -LiteralPath $script:TestFixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
        }
    } else {
        Write-Output ('RESULT ' + $Id + ': FAIL')
        if ($script:TestFixtureRoot) { Write-Output ('KEPT FIXTURE: ' + $script:TestFixtureRoot) }
    }

    $script:Results += [pscustomobject]@{ Id = $Id; Name = $Name; Pass = $script:TestPass }
}

# ---------------------------------------------------------------------------
# preflight
# ---------------------------------------------------------------------------

Write-Output ('=== pf_git_sync_selftest  ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ===')
Write-Output ('script under test: ' + $script:SutPath)

if (-not (Test-Path -LiteralPath $script:SutPath)) {
    Write-Output ('FATAL: cannot find the script under test: ' + $script:SutPath)
    exit 1
}

$gv = & git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output 'FATAL: git not found on PATH - the harness cannot build fixtures without it'
    exit 1
}
Write-Output ('git: ' + ([string]$gv))

New-Item -ItemType Directory -Path $script:TempRoot -Force | Out-Null
Write-Output ('fixtures will be built under: ' + $script:TempRoot)
Write-Output 'every fixture is a throwaway bare repo plus two clones (machine, chief) - nothing here ever touches a real Pirate Force repository.'

# ---------------------------------------------------------------------------
# MAIN: run all 14 tests, in order
# ---------------------------------------------------------------------------

Run-Test 'T1'   'happy path'                                    { Test-T1 }
Run-Test 'T2'   'nothing changed, immediate rerun'               { Test-T2 }
Run-Test 'T3'   'LOCK_GIT held, written with a BOM'               { Test-T3 }
Run-Test 'T4'   'oversized file cancels the whole commit'         { Test-T4 }
Run-Test 'T5'   'forbidden extension refused'                     { Test-T5 }
Run-Test 'T6'   'deletion refused'                                { Test-T6 }
Run-Test 'T7'   'chief-owned file edited locally blocks pull'     { Test-T7 }
Run-Test 'T8'   'non-fast-forward push, rebase, retry succeeds'   { Test-T8 }
Run-Test 'T9'   'rebase conflict halts permanently'                { Test-T9 }
Run-Test 'T10'  'halted state refuses to run again'                { Test-T10 }
Run-Test 'T11'  '.gitignore stopped covering a flag file'          { Test-T11 }
Run-Test 'T11b' 'gitignore re-opens a flag with a negation rule'   { Test-T11b }
Run-Test 'T12'  'sync.log stays pure ascii bytes'                   { Test-T12 }
Run-Test 'T13'  '-DryRun touches nothing real'                      { Test-T13 }

# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------

Write-Output ''
Write-Output '=== SUMMARY ==='
$passCount = 0
$failCount = 0
foreach ($r in $script:Results) {
    $status = 'FAIL'
    if ($r.Pass) { $status = 'PASS' }
    if ($r.Pass) { $passCount = $passCount + 1 } else { $failCount = $failCount + 1 }
    Write-Output ($r.Id.PadRight(5) + $status.PadRight(6) + $r.Name)
}

Write-Output ''
Write-Output ('SELFTEST_PASSED=' + $passCount)
Write-Output ('SELFTEST_FAILED=' + $failCount)

$overall = 'FAIL'
if ($failCount -eq 0) { $overall = 'PASS' }
Write-Output ('SELFTEST_VERDICT=' + $overall)

try {
    $remaining = @(Get-ChildItem -LiteralPath $script:TempRoot -Force -ErrorAction SilentlyContinue)
    if ($remaining.Count -eq 0) {
        Remove-Item -LiteralPath $script:TempRoot -Force -ErrorAction SilentlyContinue
    } else {
        Write-Output ('note: some fixtures were kept for inspection under ' + $script:TempRoot)
    }
} catch { }

if ($failCount -eq 0) { exit 0 } else { exit 1 }

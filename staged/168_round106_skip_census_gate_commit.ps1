# Job 168 - chief round 106.  PANYA ORDER 2026-08-20 ~15:45
# (notes_to_chief\20260820_1545_ORDER-pytest-subset-fresh-clone-preconditions.md).
#
# Actions run #3 on 7f893b8: 21/22 steps green, THE GATE ran in full for the
# first time (3m50s), and the single red was pytest_subset:
#   4 failed, 912 passed, 1486 subtests passed in 217s
# All four failures are one defect: a test reaching for evidence a fresh clone
# cannot contain (canonical DB x2, untracked LOGIN capture, machine-local
# backups/).  This is FINDINGS R12 measured on a second machine for the first
# time - 1,860 passed here versus 912 there.
#
# Panya's ruling: fix it AT THE TEST with skipUnless, never with an --ignore
# list on the CI side, because --ignore makes the test vanish silently on the
# runner while the suite still prints a healthy number.  And: a skipped check
# is not a passed check, so every skip must be counted, named, reasoned and
# PINNED, red in EITHER direction.
#
# WHAT: commit exactly TWELVE paths, already edited in the worktree by the chief.
#   NEW:
#     tests/pf_preconditions.py                     the registry, 7 keys
#     tests/test_pytest_precondition_census.py      33 tests, most of them refusals
#     tools/pf_pytest_precondition_census.py        the census
#     docs/PYTEST_SKIP_PINS.json                    the pins, by module and count
#   MODIFIED:
#     tests/test_damage_hp_link_dispatch.py         2 guarded + 1 NEW always-on test
#     tests/test_population.py                      1 guarded + 1 NEW always-on test
#     tests/test_multiplayer_readiness_audit.py     interlock split into 2 tests
#     reports/PF_MULTIPLAYER_READINESS_AUDIT001_...md    pinned impact 52 -> 53
#     reports/PF_MULTIPLAYER_READINESS_AUDIT001_...manifest   test count note
#     .github/workflows/gate-windows.yml            -rs + skip_census step
#     .github/workflows/README_GATE_CI.md           run #3 postmortem + census
#     .gitignore                                    allow-list the new tool
#
# MEASURABLE END CONDITIONS:
#   1. the full Windows suite is green and its skips are EXACTLY what the pin
#      file allows on a machine that has every artifact (expect 1 design skip)
#   2. the census is proven to REFUSE: a planted transcript with an undeclared
#      skip must exit 1 (a rule nobody has watched reject something is not a rule)
#   3. package_b_pinned_test_functions re-derives to 53 on this machine,
#      computed by the audit tool, not quoted from the report
#   4. the four new paths are NOT gitignored (round 87's lesson: on disk is not
#      in the repository)
#   5. commit lands, new head in the receipt, committed blobs carry the fix
#
# NOT done here: git push / remote config - Panya pushes, always.
# NOT touched: LOCK_GAME.txt, the server, the client, any database write,
# .git\STALE_index.lock_20260820_1210_delete_me (Panya's to delete).
# This job writes LOCK_GIT.txt HELD at start and RELEASED at the end whatever
# happens (hold only while the gate/commit job actually runs).
# ASCII ONLY.  Quote every path that contains a space.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\168_round106_skip_census.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 106 GATE AND COMMIT (job 168) - declared skips, counted and pinned (12 paths)  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$lockGit = Join-Path $bridge 'LOCK_GIT.txt'
function Beat($phase) {
    Add-Content -LiteralPath $lockGit -Value "HEARTBEAT: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')+07:00  $phase" -Encoding utf8
}

# ---------- 0. LOCK_GIT: refuse to stomp another holder, then acquire ----------
$firstLine = (Get-Content -LiteralPath $lockGit -TotalCount 1 -ErrorAction SilentlyContinue)
if ($firstLine -cmatch '^HELD:') {
    W "ABORT: LOCK_GIT.txt is HELD by someone else: $firstLine"
    W 'This job must not take over silently.  exit 40'
    exit 40
}
@(
    "HELD: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
    "BY: job 168 (chief round 106) - PANYA ORDER 1545: fresh-clone preconditions",
    "    declared at the test, plus the skip census that pins them (12 paths)",
    "PLAN: guards (fix present, ascii, not-gitignored) -> re-derive the pinned",
    "      impact count -> battery (seam + covTest + coverage + ledger + censuses",
    "      + mpaudit + full pytest -rs on Windows) -> SKIP CENSUS on that",
    "      transcript -> planted-red negative on the census -> guarded 12-path",
    "      commit -> committed-blob assertions -> release immediately.  No push.",
    "      Does NOT touch LOCK_GAME (no server/client/DB writes)."
) | Out-File -FilePath $lockGit -Encoding utf8
W 'LOCK_GIT.txt set to HELD by job 168'

Set-Location -LiteralPath $main
$headBefore = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD before = $headBefore  (expect 7f893b8...)"

$pathsNew = @(
    'tests/pf_preconditions.py',
    'tests/test_pytest_precondition_census.py',
    'tools/pf_pytest_precondition_census.py',
    'docs/PYTEST_SKIP_PINS.json'
)
$pathsMod = @(
    'tests/test_damage_hp_link_dispatch.py',
    'tests/test_population.py',
    'tests/test_multiplayer_readiness_audit.py',
    'reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.md',
    'reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.manifest',
    '.github/workflows/gate-windows.yml',
    '.github/workflows/README_GATE_CI.md',
    '.gitignore'
)
$paths1 = $pathsNew + $pathsMod
W "declared path set = $($paths1.Count) (expect 12)"

# ---------- 1. index.lock, checked first ----------
$lockPath = Join-Path $main '.git\index.lock'
if (Test-Path -LiteralPath $lockPath) {
    $lk = Get-Item -LiteralPath $lockPath
    $ageMin = [math]::Round(((Get-Date) - $lk.LastWriteTime).TotalMinutes, 1)
    W "index.lock present: size=$($lk.Length) bytes  age=${ageMin} min"
    $gitProcs = @(Get-Process -Name git -ErrorAction SilentlyContinue)
    if ($lk.Length -ne 0)      { W 'ABORT: index.lock is NOT empty. Do not delete.'; exit 30 }
    if ($gitProcs.Count -gt 0) { W 'ABORT: a git process is running.'; exit 31 }
    if ($ageMin -lt 10)        { W 'ABORT: index.lock younger than 10 minutes.'; exit 32 }
    Remove-Item -LiteralPath $lockPath -Force
    if (Test-Path -LiteralPath $lockPath) { W 'ABORT: could not remove index.lock'; exit 33 }
    W 'stale index.lock removed'
} else { W 'no index.lock present (STALE_... renamed file does not count, not touched)' }

# ---------- 2. worktree state: expect EXACTLY the declared paths dirty ----------
$dirty = @(git --no-optional-locks status --porcelain 2>&1)
W "worktree dirty paths = $($dirty.Count) (expect 12)"
$dirty | ForEach-Object { W "  st> $_" }
$unexpected = 0
foreach ($d in $dirty) {
    $p = ($d -replace '^..\s+', '') -replace '\\', '/'
    $p = $p.Trim('"')
    if ($paths1 -cnotcontains $p) { W "  UNEXPECTED DIRTY PATH> $p"; $unexpected = 1 }
}
if ($unexpected -eq 1) { W 'ABORT: worktree carries changes this job did not declare - refusing.'; exit 41 }

# ---------- 3. canonical DB guard (read from CANON_SHA.txt, never hardcoded) ----------
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$shaBefore = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
$canonExpect = (Get-Content -LiteralPath (Join-Path $bridge 'CANON_SHA.txt') -Raw).Trim()
W "canonical sha BEFORE = $shaBefore"
if ($shaBefore -cne $canonExpect) { W "ABORT: canonical sha != CANON_SHA.txt ($canonExpect)"; exit 13 }
W 'canonical matches CANON_SHA.txt'

# ---------- 4. the fix must actually be present in the worktree ----------
$fixGuard = 0
function CountIn($relPath, $needle) {
    $full = Join-Path $main ($relPath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $full)) { return -1 }
    $t = [System.IO.File]::ReadAllText($full)
    return ([regex]::Matches($t, [regex]::Escape($needle))).Count
}
$g1 = CountIn 'tests/pf_preconditions.py'                'TOKEN_PREFIX = "[precondition:"'
$g2 = CountIn 'tests/test_damage_hp_link_dispatch.py'    '@CANONICAL_DB_PRECONDITION.skip_unless_present()'
$g3 = CountIn 'tests/test_population.py'                 '@BACKUPS_TREE.skip_unless_present()'
$g4 = CountIn 'tests/test_multiplayer_readiness_audit.py' '@LOGIN_REQ_CAPTURE.skip_unless_present()'
$g5 = CountIn '.github/workflows/gate-windows.yml'       "Step 'skip_census'"
$g6 = CountIn 'reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.md' '"package_b_pinned_test_functions": 53'
$g7 = CountIn '.gitignore'                               '!/tools/pf_pytest_precondition_census.py'
$g8 = CountIn 'tests/test_damage_hp_link_dispatch.py'    'def test_the_replay_tool_refuses_a_missing_database_in_pure_ascii'
W "fix guards: token=$g1(1) dbGuard=$g2(2) backups=$g3(1) capture=$g4(1) censusStep=$g5(1) impact53=$g6(1) ignoreLine=$g7(1) alwaysOn=$g8(1)"
if ($g1 -ne 1 -or $g2 -ne 2 -or $g3 -ne 1 -or $g4 -ne 1 -or $g5 -ne 1 -or $g6 -ne 1 -or $g7 -ne 1 -or $g8 -ne 1) { $fixGuard = 1 }
if ($fixGuard -eq 1) { W 'ABORT: the fix this job exists to commit is not in the worktree.'; exit 42 }

# ---------- 5. ASCII guard ----------
# Every path except the audit report, which already carried non-ASCII prose
# before this round; for that one the count must be UNCHANGED from HEAD, which
# proves this round added none of its own.
$asciiGuard = 0
$reportRel = 'reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.md'
foreach ($p in $paths1) {
    if ($p -ceq $reportRel) { continue }
    $full = Join-Path $main ($p -replace '/', '\')
    $bytes = [System.IO.File]::ReadAllBytes($full)
    $nonAscii = 0
    foreach ($b in $bytes) { if ($b -gt 127) { $nonAscii++ } }
    W "non-ascii bytes in $p = $nonAscii (expect 0)"
    if ($nonAscii -ne 0) { $asciiGuard = 1 }
}
$repBytes = [System.IO.File]::ReadAllBytes((Join-Path $main ($reportRel -replace '/', '\')))
$repNow = 0
foreach ($b in $repBytes) { if ($b -gt 127) { $repNow++ } }
$repHeadRaw = (git --no-optional-locks show "HEAD:$reportRel" 2>&1 | Out-String)
$repHeadBytes = [System.Text.Encoding]::UTF8.GetBytes($repHeadRaw)
$repHead = 0
foreach ($b in $repHeadBytes) { if ($b -gt 127) { $repHead++ } }
W "audit report non-ascii: now=$repNow atHEAD=$repHead (must be equal - this round adds no new non-ascii)"
if ($repNow -ne $repHead) { $asciiGuard = 1 }

# ---------- 6. the four new paths must NOT be gitignored (round 87's lesson) ----------
$ignoreGuard = 0
foreach ($p in $pathsNew) {
    git --no-optional-locks check-ignore -q -- "$p" 2>&1 | Out-Null
    $ci = $LASTEXITCODE
    W "check-ignore $p -> exit $ci (expect 1 = NOT ignored)"
    if ($ci -eq 0) { $ignoreGuard = 1 }
}
if ($ignoreGuard -eq 1) { W 'ABORT: a new path is gitignored - it would be on disk but not in the repository.' ; exit 44 }
Beat 'preflight done, re-deriving the pinned impact count'

# ---------- 7. RE-DERIVE the pinned impact count on THIS machine ----------
# tests/test_population.py is one of the six package-B pinned files and gained a
# test this round, so the number in the report had to move in the same commit.
# Computed here by the audit tool itself, not quoted from the report.
$mpJson = (py -3 (Join-Path $main 'tools\pf_multiplayer_readiness_audit.py') --json 2>&1 | Out-String)
$mpAuditExit = $LASTEXITCODE
$rederiveExit = 1
try {
    $mp = $mpJson | ConvertFrom-Json
    $bFn = $mp.impact_b_pinned.functions
    $bFiles = $mp.impact_b_pinned.files
    W "re-derived package_b_pinned: files=$bFiles (expect 6)  functions=$bFn (expect 53)"
    if ($bFn -eq 53 -and $bFiles -eq 6) { $rederiveExit = 0 }
} catch {
    W "RED: could not parse the audit tool's --json output"
}
W "mpaudit exit = $mpAuditExit (expect 0)   rederive = $rederiveExit (expect 0)"
if ($rederiveExit -ne 0) { W 'ABORT: the pinned impact count does not re-derive to the committed value.'; exit 43 }
Beat 'impact count re-derived, starting battery'

# ---------- 8. the battery (job-167 shape, plus the census) ----------
W '--- seam (expect passed) ---'
py -3 -m pytest (Join-Path $main 'tests\test_foundation_legacy_seam.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  seam> $_" }
$seamExit = $LASTEXITCODE
W '--- functional-coverage tests (expect all passed) ---'
py -3 -m pytest (Join-Path $main 'tests\test_functional_coverage.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  covt> $_" }
$covTestExit = $LASTEXITCODE
W '--- the census tool tests, on their own, first (33 tests, most of them refusals) ---'
py -3 -m pytest (Join-Path $main 'tests\test_pytest_precondition_census.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  censusT> $_" }
$censusTestExit = $LASTEXITCODE
Beat 'seam + covTest + censusTest done'
W '--- coverage verifier (expect exit 0 - blocking on Actions since round 105) ---'
py -3 (Join-Path $main 'tools\verify_functional_coverage.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  cov> $_" }
$covExit = $LASTEXITCODE
W '--- ledger verifier (expect PASS entries unchanged, 35) ---'
py -3 (Join-Path $main 'tools\verify_hypothesis_ledger.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  ledger> $_" }
$ledgerExit = $LASTEXITCODE
W '--- runtimeres actor-entry census (expect unchanged) ---'
py -3 (Join-Path $main 'tools\pf_runtimeres_actor_entry_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  runtimeres> $_" }
$runtimeresExit = $LASTEXITCODE
W '--- hp/death census (expect unchanged) ---'
py -3 (Join-Path $main 'tools\pf_hp_death_respawn_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  hpstatic> $_" }
$hpStaticExit = $LASTEXITCODE
W '--- vital-thunk census (expect PASS unchanged) ---'
py -3 (Join-Path $main 'tools\pf_vital_thunk_census_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  census> $_" }
$censusExit = $LASTEXITCODE
Beat 'verifiers + censuses done, starting full pytest'

W '--- pytest full suite on Windows with -rs (was 1860 passed 1 skipped at job 167; +37 new tests expected) ---'
# pytest truncates the short-summary lines to the console width.  The census is
# built to survive that (the [precondition:key] token is at the FRONT of every
# reason, and design reasons are compared truncation-tolerantly), but a wide
# console means the log a human reads is the whole reason, not half of it.
$env:COLUMNS = '200'
$pytestLog = Join-Path $env:TEMP "r106_pytest_$stamp.txt"
$pyOut = (py -3 -m pytest tests -q -rs 2>&1)
$pytestExit = $LASTEXITCODE
$pyOut | Out-File -FilePath $pytestLog -Encoding utf8
$pyOut | Select-Object -Last 8 | ForEach-Object { W "  py> $_" }
Beat 'full pytest done, running the skip census'

# ---------- 9. THE SKIP CENSUS on that exact transcript ----------
# No --excluded here: the bridge runs the whole suite, so every pinned module is
# in the selection and every artifact is present -> the only skip allowed is the
# one design skip.  This is the first machine where that side of the pin file is
# exercised at all.
W '--- skip census (every skip named, with its reason) ---'
py -3 (Join-Path $main 'tools\pf_pytest_precondition_census.py') --report "$pytestLog" 2>&1 | ForEach-Object { W "  skipcensus> $_" }
$skipCensusExit = $LASTEXITCODE
W "skip census exit = $skipCensusExit (expect 0)"

# ---------- 9b. NEGATIVE: the census must be seen REFUSING, on this machine ----------
# A rule nobody has watched reject something is not a rule.
$plantedLog = Join-Path $env:TEMP "r106_planted_$stamp.txt"
'SKIPPED [1] tests/test_arena.py:5: a skip nobody declared' | Out-File -FilePath $plantedLog -Encoding utf8
py -3 (Join-Path $main 'tools\pf_pytest_precondition_census.py') --report "$plantedLog" 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  planted> $_" }
$plantedExit = $LASTEXITCODE
W "planted-red census exit = $plantedExit (expect 1 - the census refusing an undeclared skip)"
$negativeOk = if ($plantedExit -eq 1) { 0 } else { 1 }
Remove-Item -LiteralPath $plantedLog -Force -ErrorAction SilentlyContinue

# ---------- 10. guards ----------
$shaAfter = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
if ($shaAfter -cne $shaBefore) { W 'RED: CANONICAL DB MOVED'; $canonGuard = 1 } else { W 'canonical guard OK'; $canonGuard = 0 }
$v141Dirty = (git --no-optional-locks status --short -- 'current/pf_login_game_server_v141.py' 2>&1 | Out-String).Trim()
if ($v141Dirty) { W "RED: v141 SNAPSHOT DIRTY -> $v141Dirty"; $v141Guard = 1 } else { W 'v141 guard OK'; $v141Guard = 0 }
git --no-optional-locks diff --check 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  git> $_" }
$diffExit = $LASTEXITCODE

$allGreen = ($asciiGuard -eq 0) -and ($fixGuard -eq 0) -and ($unexpected -eq 0) -and `
            ($ignoreGuard -eq 0) -and ($rederiveExit -eq 0) -and ($mpAuditExit -eq 0) -and `
            ($seamExit -eq 0) -and ($covTestExit -eq 0) -and ($censusTestExit -eq 0) -and `
            ($covExit -eq 0) -and ($ledgerExit -eq 0) -and ($runtimeresExit -eq 0) -and `
            ($hpStaticExit -eq 0) -and ($censusExit -eq 0) -and ($pytestExit -eq 0) -and `
            ($skipCensusExit -eq 0) -and ($negativeOk -eq 0) -and `
            ($canonGuard -eq 0) -and ($v141Guard -eq 0) -and ($diffExit -eq 0)
W "ALL GREEN = $allGreen"

# ---------- 11. guarded commit: read-tree HEAD, stage ONLY the declared paths ----------
$committed = 0
$headAfter = $headBefore
$blobOk = -1
if ($allGreen) {
    Beat 'battery green, committing'
    W '--- GUARDED COMMIT: read-tree HEAD, then stage ONLY the twelve round-106 paths ---'
    $rt = (git --no-optional-locks read-tree HEAD 2>&1 | Out-String).Trim()
    if ($rt) { W "  read-tree> $rt" }
    if ($LASTEXITCODE -ne 0) { W 'ABORT: read-tree failed'; exit 34 }
    $addFailed = 0
    foreach ($p in $paths1) {
        $o = (git --no-optional-locks add -- "$p" 2>&1 | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) { W "  RED add> $p :: $o"; $addFailed = 1 }
        elseif ($o) { W "  add(warn)> $p :: $o" }
    }
    if ($addFailed -eq 1) { W 'ABORT: an add failed - refusing partial commit'; exit 35 }
    $stagedCount = @(git --no-optional-locks diff --cached --name-only 2>&1).Count
    W "staged path count = $stagedCount (expect 12)"
    git --no-optional-locks diff --cached --stat 2>&1 | Select-Object -Last 14 | ForEach-Object { W "  staged> $_" }
    $delLines = (git --no-optional-locks diff --cached --name-status 2>&1 | Select-String -Pattern '^D' -CaseSensitive)
    if ($delLines) {
        W 'RED: staged set contains DELETIONS - aborting'; $delLines | ForEach-Object { W "  DEL> $_" }
    } elseif ($stagedCount -ne 12) {
        W "RED: staged count is $stagedCount, expected 12 - aborting"
    } else {
        $msg = "round 106: teach four tests to say what they need, and pin the saying of it. The third run of the workflow reached the gate at last and died in one place, the pytest step, with four failures that were all the same failure: a test reaching for evidence that no clone can hold. Two of them run the damage replay tool with no database argument and the tool falls back to the canonical database, which the ignore file keeps out on purpose and round forty one forbade the suite to write to at all, so the tool exits two and the assertion reads that two as a count of characters because the test is named for ascii and asserts a return code first. The third compares a pinned report string against an audit that honestly answered that the login capture is absent. The fourth opens two capture files under a backups tree that exists only on the bridge. This is finding twelve measured on a second machine for the first time in this project, eighteen hundred and sixty passing here against nine hundred and twelve there, and the gap is the reproducibility debt written down as a number instead of a worry. Panya's ruling was to repair it at the test and never at the runner, because an ignore entry deletes the test from the second machine while the suite goes on printing a number that looks the same, and because a test must know its own preconditions and must say out loud that it skipped, on every machine. So there is now one registry that knows what this repository does not contain, seven artifacts named and reasoned, and every skip reason begins with a machine readable token. Nothing was made weaker anywhere the evidence exists: three new tests run on every machine to keep what skipping would have taken away, the tool's refusal path proves the code page contract and the exit code contract from a bare clone, the provenance paths are still asserted to be machine local, and the capture guard must still answer reproduced where the capture is and exactly skipped where it is not. Then the second half, because a skipped check is not a passed check: a census reads what pytest actually reported, prints every skip by name with its reason, and grades it against a pin file whose every entry is evaluated rather than quoted, zero when the module was excluded, zero when the artifact is present, the pinned count otherwise, so one file is correct on both machines without a number typed for either. It is red in both directions, and the direction that matters is downward, a real test drifting quietly into the skip pile, which is the same shape of defect as the two stale pins the round before. The census has been watched refusing five different lies in its own tests and one more in this job. The pinned impact count moves from fifty two to fifty three in this same commit because the population file gained a test and that is the rule the block exists to enforce. Twelve paths. No source, no scenario, no ledger entry, no coverage grade, no server booted, no client opened, no database written, no remote touched: the push is Panya's alone."
        git --no-optional-locks commit -m "$msg" 2>&1 | Select-Object -First 3 | ForEach-Object { W "  commit> $_" }
        $headAfter = (git --no-optional-locks rev-parse HEAD 2>&1)
        if ($headAfter -cne $headBefore) {
            $committed = 1
            W "COMMIT CONFIRMED: HEAD $headBefore -> $headAfter"
            git --no-optional-locks show --stat --oneline -s HEAD 2>&1 | Select-Object -First 16 | ForEach-Object { W "  head> $_" }
        } else { W "RED: commit returned but HEAD did not move (still $headBefore)" }
    }
} else {
    W 'NOT COMMITTING - a guard is red.  The edits stay as a dirty diff'
    W '(never reset/clean by iron rule) - receipt says so for the next round.'
}

# ---------- 12. acceptance: the COMMITTED BLOBS must carry the fix ----------
if ($committed -eq 1) {
    $blobOk = 0
    $b1 = (git --no-optional-locks show 'HEAD:tests/pf_preconditions.py' 2>&1 | Out-String)
    $b2 = (git --no-optional-locks show 'HEAD:docs/PYTEST_SKIP_PINS.json' 2>&1 | Out-String)
    $b3 = (git --no-optional-locks show 'HEAD:tools/pf_pytest_precondition_census.py' 2>&1 | Out-String)
    $b4 = (git --no-optional-locks show 'HEAD:.github/workflows/gate-windows.yml' 2>&1 | Out-String)
    $a1 = ([regex]::Matches($b1, [regex]::Escape('TOKEN_PREFIX = "[precondition:"'))).Count
    $a2 = ([regex]::Matches($b2, [regex]::Escape('"key": "canonical_db"'))).Count
    $a3 = ([regex]::Matches($b3, [regex]::Escape('def census('))).Count
    $a4 = ([regex]::Matches($b4, [regex]::Escape("Step 'skip_census'"))).Count
    W "acceptance on committed blobs: token=$a1(1) pinKey=$a2(1) censusFn=$a3(1) censusStep=$a4(1)"
    if ($a1 -ne 1 -or $a2 -ne 1 -or $a3 -ne 1 -or $a4 -ne 1) { $blobOk = 1; W 'RED: a committed blob does not carry the fix' }
    $blobNonAscii = 0
    foreach ($t in @($b1, $b2, $b3, $b4)) {
        foreach ($b in [System.Text.Encoding]::UTF8.GetBytes($t)) { if ($b -gt 127) { $blobNonAscii++ } }
    }
    W "committed blob non-ascii bytes (4 files) = $blobNonAscii (expect 0)"
    if ($blobNonAscii -ne 0) { $blobOk = 1 }
}

W '--- post-commit worktree state (expect clean) ---'
git --no-optional-locks status --short 2>&1 | Select-Object -First 8 | ForEach-Object { W "  st> $_" }
$shaEnd = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha END = $shaEnd (expect unchanged)"
Remove-Item -LiteralPath $pytestLog -Force -ErrorAction SilentlyContinue

# ---------- 13. release LOCK_GIT.txt, whatever happened ----------
$headShort = (git --no-optional-locks rev-parse --short HEAD 2>&1)
@(
    "RELEASED: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
    "BY: job 168 (chief round 106) - released by the job itself",
    "done: PANYA ORDER 1545 executed - the four run #3 failures are now declared",
    "      skips, fixed AT THE TEST (skipUnless via tests/pf_preconditions.py),",
    "      never with a CI --ignore entry.  Three NEW always-on tests keep what",
    "      skipping would have taken away (the replay tool's cp874 + exit-code",
    "      contract on its refusal path; the v94 provenance paths; the login",
    "      capture guard's exact answer on both machines).  Second half: the skip",
    "      census - every skip printed by name with its reason and graded against",
    "      docs/PYTEST_SKIP_PINS.json, evaluated not quoted (excluded -> 0,",
    "      artifact present -> 0, else the pinned count), red in BOTH directions.",
    "      One pin file, correct on the bridge (1 design skip) and on a fresh",
    "      clone in CI (4 precondition skips), with no number typed per machine.",
    "      Census watched refusing 7 lies in its own tests + 1 planted here.",
    "      package_b_pinned_test_functions 52 -> 53, re-derived on this machine.",
    "      allGreen=$allGreen committed=$committed blobOk=$blobOk rederive=$rederiveExit",
    "      ascii=$asciiGuard fixGuard=$fixGuard unexpectedDirty=$unexpected ignoreGuard=$ignoreGuard",
    "      seam=$seamExit covTest=$covTestExit censusTest=$censusTestExit coverage=$covExit",
    "      ledger=$ledgerExit runtimeres=$runtimeresExit hpstatic=$hpStaticExit census=$censusExit",
    "      mpaudit=$mpAuditExit pytest=$pytestExit skipCensus=$skipCensusExit negative=$negativeOk",
    "      canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit",
    "head: $headShort  (was $headBefore)",
    "next: Panya pushes and re-fires Actions - run #4 should be the first FULLY",
    "      green run.  It is a PREDICTION, not a measurement: what was measured is",
    "      a real git clone of HEAD in the sandbox, with the same exclusion list,",
    "      going green except one failure that is Python 3.10-only (__notes__ is",
    "      3.11+; the runner is 3.14).  Then the deliberate red (recipe 1 or the",
    "      new recipe 6 in README_GATE_CI.md) and green again - still owed.",
    "      ROUND-AFTER WORK, first item, fully measured and ready:",
    "      pf_bridge\FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md - NINE of the 42",
    "      --ignore'd modules are false positives of the GameClient|capture_v141",
    "      grep (seven matched because their docstring says 'no GameClient') and",
    "      pass 100% on a fresh clone with no artifacts: removing them returns 398",
    "      tests to the runner without editing one test.  Then waves 1-4 in that",
    "      factpack.  Otherwise unchanged: sibling-layout rule + failing test;",
    "      rebase chief_task_prompt_CLOUD_DRAFT.md; DRAFT_gitignore_REPO2 second",
    "      pair of eyes; R102 static (BEHAVIOR row + fight-vital delivery);",
    "      GT-037 LOOT-ROLL-001; housekeeping (QUEUE ~82KB, CONTINUATION ~104KB",
    "      both over their ceilings).  chief next job = 169, tester = 9xx/0xxx.",
    "      .git\STALE_index.lock_20260820_1210_delete_me is Panya's to delete.",
    "warn: do NOT run the full pytest suite from the Linux sandbox - it reaches the",
    "      canonical database through the mount.  This job runs it on Windows via py -3.",
    "      A fresh `git clone` into /tmp is the safe way to see what a runner sees.",
    "",
    "===== flag scope (Panya 2026-08-19 ~11:45) =====",
    "git commit / gate run on the Windows bridge; git index and staging;",
    "edits to .gitignore / manifest / coverage that require the seam test.",
    "NOT covered: writing files into the worktree, reading git log/status,",
    "booting the server or opening the game (that is LOCK_GAME.txt).",
    "Hold only while a gate/commit job is actually running; release immediately after.",
    "Takeover rule: same as LOCK_GAME.txt - age >= 20 min AND silent in all three channels."
) | Out-File -FilePath $lockGit -Encoding utf8
W "LOCK_GIT.txt released by the job (committed=$committed head=$headShort)"

W '=== 168 SUMMARY ==='
@(
    "ascii=$asciiGuard fixGuard=$fixGuard unexpectedDirty=$unexpected ignoreGuard=$ignoreGuard rederive=$rederiveExit",
    "seam=$seamExit covTest=$covTestExit censusTest=$censusTestExit coverage=$covExit ledger=$ledgerExit",
    "runtimeres=$runtimeresExit hpstatic=$hpStaticExit census=$censusExit mpaudit=$mpAuditExit",
    "pytest=$pytestExit skipCensus=$skipCensusExit negative=$negativeOk",
    "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit",
    "allGreen=$allGreen committed=$committed blobOk=$blobOk",
    "head=$headShort"
) | ForEach-Object { W $_ }
W '=== 168 DONE ==='

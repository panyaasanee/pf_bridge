# Job 179 - chief round 111.  GATE ONLY.  This job runs the full Windows battery
# and REPORTS the tree.  It commits nothing, stages nothing, pushes nothing,
# resets nothing, checks out nothing, and creates no branch.
#
# MODEL: staged\178_round111_npc_hp_link_gate_commit.ps1 - that file with the
# whole commit half removed.  Every place this file differs from 178 is marked
# with the word DEVIATION and a reason.
#
# WHY THIS JOB EXISTS
#   Job 178 ran the battery and came back RED, correctly, and refused to commit:
#     19 failed, 2007 passed, 1 skipped, 3830 subtests
#   Everything else was green (seam 22p/217sub, coverage tests 34p, coverage
#   verifier exit 0, ledger PASS entries=36, mpaudit 0, vital-thunk census PASS,
#   canonical sha unchanged, v141 clean, diffcheck 0).
#   All 19 failures were ONE module, tests/test_runtimeres_actor_entry_static.py,
#   whose tool-loading tests died because tools\pf_runtimeres_actor_entry_static.py
#   exited 1 on six pinned project-wide censuses that count actor-entry emitters
#   in src/.  Those censuses did exactly their job: the round-111 NPC HP ladder is
#   a new emitter.  They have since been re-derived and their sentences rewritten,
#   and the tool now reports "152 guards, 0 failures".  This job re-runs the gate.
#
# AND THEN THIS HAPPENED, AND IT CHANGES WHAT THIS JOB IS ALLOWED TO ASSUME
#   While that repair was in flight, the Windows-side pf_git_sync.ps1 committed
#   the round's uncommitted work to main as a commit literally titled "wip"
#   (cc46a03) and PUSHED it - the same twelve paths job 178 had just refused to
#   commit because the gate was red.  The gate is therefore NO LONGER the only
#   thing that decides what enters main, and any job that reasons "if I did not
#   commit it, it is not committed" is now simply wrong.
#   So this job is GATE-ONLY and OBSERVATIONAL.  It proves the tree is green and
#   then DESCRIBES the tree it proved, without changing it, and without assuming
#   anything at all about how the tree came to be that way.
#
# WHAT IT GRADES (identical battery to job 178, same invocations, same order,
# same pass criteria, copied rather than re-derived):
#   seam -> functional-coverage tests -> coverage verifier -> ledger verifier
#   (still pinned to HYPOTHESIS_LEDGER PASS entries=36) -> mpaudit -> vital-thunk
#   census -> [NEW: actor-entry static guard family] -> py -3 -m pytest tests -q -rs
#   -> skip census on that exact transcript -> canonical-SHA guard (read from
#   CANON_SHA.txt, never hardcoded) -> v141 snapshot guard -> git diff --check.
#
# WHAT IT DOES NOT DO, EVER:
#   git commit / git add / git push / git reset / git checkout / branch / tag /
#   pull request / anything under .github/ / any write to the canonical database /
#   any server or client boot / ports 10188 or 10189 / LOCK_GAME.txt / the
#   pf_bridge repository index / deleting anything inside .git.
#   Those seven words appear in this file ONLY in comments and ONLY in log prose.
#
# This job takes LOCK_GIT.txt at the start and RELEASES it on EVERY exit path,
# including every failure - see DEVIATION 1.
# ASCII ONLY.  LF only.  Quote every path that contains a space.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\179_round111_gate_only.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 111 GATE-ONLY RERUN (job 179) - NO COMMIT, NO STAGING, NO PUSH  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$lockGit = Join-Path $bridge 'LOCK_GIT.txt'

# ---------- DEVIATION 0 (inherited from 178): dot-source the flag helpers ----------
# Standing instruction from chief round 109: jobs 176 and later MUST dot-source
# staged\TEMPLATE_lock_flag_helpers.ps1 and MUST NOT hand-roll a flag gate.
# Out-File -Encoding utf8 on Windows PowerShell 5.1 prepends a BOM, and the old
# inline '^HELD:' check does not match a BOM'd line - so it reported the flag FREE
# at exactly the moment the flag was HELD.  Write-Flag emits no BOM and
# Test-FlagHeld tolerates one anyway.  Job 177 is the receipt.
$tpl = Join-Path $bridge 'staged\TEMPLATE_lock_flag_helpers.ps1'
if (-not (Test-Path -LiteralPath $tpl)) {
    W "ABORT: the flag-helper template is missing -> $tpl"
    W 'This job refuses to hand-roll a flag gate.  exit 46'
    exit 46
}
. $tpl
if (-not (Get-Command Write-Flag -ErrorAction SilentlyContinue) -or
    -not (Get-Command Test-FlagHeld -ErrorAction SilentlyContinue) -or
    -not (Get-Command Add-FlagHeartbeat -ErrorAction SilentlyContinue)) {
    W 'ABORT: the template dot-sourced but the three helpers are not defined.  exit 46'
    exit 46
}
W 'flag helpers dot-sourced from staged\TEMPLATE_lock_flag_helpers.ps1'
function Beat($phase) { Add-FlagHeartbeat -Path $lockGit -Phase $phase }

# ---------- every result variable, initialised BEFORE the flag is taken ----------
# -1 means "never measured", which is a different thing from 0 and must stay a
# different thing, so the release writer can print an honest line from any abort.
$seamExit       = -1
$covTestExit    = -1
$covExit        = -1
$ledgerExit     = -1
$ledgerPin      = -1
$mpAuditExit    = -1
$censusExit     = -1
$actorExit      = -1
$actorPin       = -1
$pytestExit     = -1
$skipCensusExit = -1
$canonGuard     = -1
$v141Guard      = -1
$diffExit       = -1
$statusExit     = -1
$allGreen       = $false
$committed      = 0
$headNow        = 'unknown'
$headSubject    = 'unknown'
$pyCountLine    = 'not measured'
$pyFailCount    = -1
$ccMatch        = 'not measured'

# ---------- DEVIATION 1 (inherited from 178): ONE release writer ----------
# Exactly one function writes the RELEASED block and exits, and there is no
# `exit` statement anywhere below it.  The two exits ABOVE it are the only ones
# that do not release, and correctly so: at that point this job has not taken the
# flag, and releasing a flag you do not hold is stomping it.
# RESIDUAL, stated rather than hidden: this covers every abort path THIS FILE
# DEFINES.  It does not cover loss of power or an unhandled TERMINATING error
# thrown by a cmdlet, either of which would leave the flag HELD with a HEARTBEAT
# whose timestamp stops.  That is what the takeover rule at the bottom of
# LOCK_GIT.txt exists for (age >= 20 min AND silent in all three channels).
# ErrorActionPreference is Continue, so ordinary failures - a missing file, a
# non-zero exit code, a null - are non-terminating and DO reach this writer.
function Finish179 {
    param(
        [Parameter(Mandatory = $true)][int]    $Code,
        [Parameter(Mandatory = $true)][string] $Verdict,
        [Parameter(Mandatory = $true)][string] $Next
    )
    $headShort = (git --no-optional-locks rev-parse --short HEAD 2>&1)
    $lines = @(
        "RELEASED: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
        "BY: job 179 (chief round 111) - released by the job itself, exit $Code",
        "done: $Verdict",
        "      Job 179 is GATE-ONLY.  It committed NOTHING, staged NOTHING and",
        "      pushed NOTHING.  committed=0 is not a measurement, it is a",
        "      property of this file: it contains no commit, add, push, reset or",
        "      checkout command at all.  Any commit that appears on main around",
        "      this time came from the Windows-side sync job, NOT from here.",
        "      allGreen=$allGreen committed=$committed",
        "      seam=$seamExit covTest=$covTestExit coverage=$covExit ledger=$ledgerExit ledgerPin=$ledgerPin",
        "      mpaudit=$mpAuditExit census=$censusExit actorEntry=$actorExit actorPin=$actorPin",
        "      pytest=$pytestExit pytestFAILorERRORlines=$pyFailCount skipCensus=$skipCensusExit",
        "      canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit status=$statusExit",
        "      pytest totals MEASURED, not pinned -> $pyCountLine",
        "      worktree vs commit cc46a03 (REPORTED, never enforced) -> $ccMatch",
        "head: $headShort   subject: $headSubject",
        "next: $Next",
        "      chief next job = 180.  tester = 9xx (0xxx while holding LOCK_GAME).",
        "warn: this job did NOT commit, did NOT stage, did NOT push, did NOT",
        "      create/delete/modify any branch, did NOT open or touch a pull",
        "      request, and did NOT touch .github/ at all.  It also did not",
        "      reset, clean or check out anything: the worktree it found is the",
        "      worktree it left.",
        "      The pf_bridge repository index was deliberately NOT touched, for",
        "      the reason jobs 175, 176 and 178 gave: Panya has commits in flight",
        "      there and two writers on one index is how a dirty diff disappears.",
        "",
        "===== flag scope (Panya 2026-08-19 ~11:45) =====",
        "git commit / gate run on the Windows bridge; git index and staging;",
        "edits to .gitignore / manifest / coverage that require the seam test.",
        "NOT covered: writing files into the worktree, reading git log/status,",
        "booting the server or opening the game (that is LOCK_GAME.txt).",
        "Hold only while a gate/commit job is actually running; release immediately after.",
        "Takeover rule: same as LOCK_GAME.txt - age >= 20 min AND silent in all three channels."
    )
    Write-Flag -Path $lockGit -Lines $lines
    W "LOCK_GIT.txt RELEASED by job 179 (exit $Code, committed=$committed)"
    W '=== 179 SUMMARY ==='
    @(
        "seam=$seamExit covTest=$covTestExit coverage=$covExit ledger=$ledgerExit ledgerPin=$ledgerPin",
        "mpaudit=$mpAuditExit census=$censusExit actorEntry=$actorExit actorPin=$actorPin",
        "pytest=$pytestExit pytestFAILorERRORlines=$pyFailCount skipCensus=$skipCensusExit",
        "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit status=$statusExit",
        "pytest totals (measured, not pinned) -> $pyCountLine",
        "worktree vs cc46a03 (reported, not enforced) -> $ccMatch",
        "THIS JOB COMMITTED NOTHING AND STAGED NOTHING.",
        "verdict text -> $Verdict"
    ) | ForEach-Object { W $_ }
    # The single line the chief greps.  One line, always emitted, on every path.
    W "JOB179_VERDICT allGreen=$allGreen committed=0 exit=$Code head=$headShort"
    W '=== 179 DONE ==='
    exit $Code
}

# ---------- 0. LOCK_GIT: refuse to stomp another holder, then acquire ----------
if (Test-FlagHeld -Path $lockGit) {
    $firstLine = (Get-Content -LiteralPath $lockGit -TotalCount 1 -ErrorAction SilentlyContinue)
    W "ABORT: LOCK_GIT.txt is HELD by someone else -> $firstLine"
    W 'This job must not take over silently.  exit 40'
    exit 40
}
Write-Flag -Path $lockGit -Lines @(
    "HELD: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
    "BY: job 179 (chief round 111) - GATE-ONLY rerun after the actor-entry",
    "    census repair.  This job COMMITS NOTHING.",
    "PLAN: full battery in job 178's order, plus a separate blocking run of",
    "      tools\pf_runtimeres_actor_entry_static.py pinned to",
    "      '152 guards, 0 failures', plus the full pytest short-test-summary",
    "      section kept in the transcript, plus a read-only report of HEAD,",
    "      git status --porcelain and the twelve paths of commit cc46a03.",
    "      No staging, no commit, no push, no reset, no checkout, no branch, no",
    "      .github/.  Does NOT touch LOCK_GAME (no server/client/DB writes) and",
    "      does NOT touch the pf_bridge git index."
)
W 'LOCK_GIT.txt set to HELD by job 179 (written by Write-Flag - no BOM)'
W 'NOTE FOR THE READER OF THIS TRANSCRIPT: job 179 COMMITS NOTHING.  It contains'
W 'no commit, add, push, reset, checkout or branch command.  If a new commit'
W 'appears on main around this timestamp, it came from the Windows-side sync job'
W '(that is what produced cc46a03, titled "wip"), and NOT from this job.'

Set-Location -LiteralPath $main
$headNow = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD = $headNow"

# ---------- 1. index.lock: REPORTED and refused, never removed ----------
# DEVIATION 2: job 178 deleted a stale index.lock.  Job 179 does not delete
# anything inside .git.  This job never writes the index, so a lock it did not
# take is not its to break; if one is present, another writer may be mid
# transaction and the tree report this job exists to produce would be a snapshot
# of somebody else's half-finished work.  So: report it and stop.
$lockPath = Join-Path $main '.git\index.lock'
if (Test-Path -LiteralPath $lockPath) {
    $lk = Get-Item -LiteralPath $lockPath
    $ageMin = [math]::Round(((Get-Date) - $lk.LastWriteTime).TotalMinutes, 1)
    $gitProcs = @(Get-Process -Name git -ErrorAction SilentlyContinue)
    W "index.lock present: size=$($lk.Length) bytes  age=${ageMin} min  running git processes=$($gitProcs.Count)"
    W 'ABORT: another writer may own the git index.  This job does NOT delete it.'
    Finish179 -Code 30 -Verdict 'ABORT at index.lock: a git index lock is present and job 179 refuses to remove locks it did not take.' -Next 'Find out which git process owns .git\index.lock, let it finish (or clear it by hand if it is provably stale), then re-run job 179.'
}
W 'no index.lock present'

# ---------- 2. canonical DB guard (read from CANON_SHA.txt, never hardcoded) ----------
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$shaBefore = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
$canonExpect = (Get-Content -LiteralPath (Join-Path $bridge 'CANON_SHA.txt') -Raw).Trim()
W "canonical sha BEFORE = $shaBefore"
if ($shaBefore -cne $canonExpect) {
    W "ABORT: canonical sha does not match CANON_SHA.txt -> $canonExpect"
    Finish179 -Code 13 -Verdict 'ABORT at the canonical guard: state\pirateforce.sqlite3 does not match CANON_SHA.txt BEFORE anything ran.' -Next 'Find out what wrote the canonical database, then re-run job 179.  Nothing was committed; this job never commits.'
}
W 'canonical matches CANON_SHA.txt'

# DEVIATION 3: job 178's sections 2, 4, 5 and 6 - the declared-thirteen dirty-set
# guard, the eight lane text guards, the ASCII/CR guard over the declared paths
# and the not-gitignored guard - are ALL ABSENT here, on purpose.  Every one of
# them exists to grade a COMMIT: they answer "is the thing I am about to stage
# really the thing I said it was".  Job 179 stages nothing, so those guards would
# be grading a decision this job does not make.  Worse, the declared-set guard
# would abort on a tree it has no business having an opinion about: the twelve
# paths of the lane are no longer dirty (the sync committed them) and the paths
# that ARE dirty are the actor-entry census repair.  Job 179 REPORTS the tree in
# section 9 instead of asserting a shape for it.  Dropping a check because its
# subject does not exist in this job is not the same as skipping a check, and the
# receipt carries no ascii= / fixGuard= / unexpectedDirty= / ignoreGuard= field
# for exactly that reason.
Beat 'preflight done, starting battery'

# ---------- 3. the battery ----------
# Step list, invocation and pass criteria copied VERBATIM from job 178.  Nothing
# added except section 3a, nothing re-derived from memory.
#
# THE SEAM TEST IS FIRST AND IT IS NOT OPTIONAL: the round-111 work touches
# .gitignore and files under reports/, which is the standing rule's trigger.
W '--- seam (expect passed) ---'
py -3 -m pytest (Join-Path $main 'tests\test_foundation_legacy_seam.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  seam> $_" }
$seamExit = $LASTEXITCODE
W '--- functional-coverage tests (expect all passed) ---'
py -3 -m pytest (Join-Path $main 'tests\test_functional_coverage.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  covt> $_" }
$covTestExit = $LASTEXITCODE
Beat 'seam + covTest done'
W '--- coverage verifier (expect exit 0 - blocking since round 105) ---'
py -3 (Join-Path $main 'tools\verify_functional_coverage.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  cov> $_" }
$covExit = $LASTEXITCODE

# The ledger entry-count pin is kept exactly as job 178 wrote it.  HYP-PF-029 was
# appended in round 111, so 36 is still the number; it is BLOCKING and it is red
# in both directions: 35 fails, 37 fails.
W '--- ledger verifier (expect PASS with entries=36) ---'
$ledgerOut  = (py -3 (Join-Path $main 'tools\verify_hypothesis_ledger.py') 2>&1)
$ledgerExit = $LASTEXITCODE
$ledgerOut | Select-Object -Last 2 | ForEach-Object { W "  ledger> $_" }
$ledgerText = ($ledgerOut | Out-String)
$ledgerHits = ([regex]::Matches($ledgerText, [regex]::Escape('HYPOTHESIS_LEDGER PASS entries=36'))).Count
$ledgerPin  = if ($ledgerHits -eq 1) { 0 } else { 1 }
W "ledger entry-count pin: exact-line hits = $ledgerHits (expect 1)  ledgerPin=$ledgerPin (expect 0)"
if ($ledgerPin -ne 0) { W 'RED: the ledger did not report exactly 36 entries.' }

W '--- multiplayer readiness audit (needs real git history) ---'
py -3 (Join-Path $main 'tools\pf_multiplayer_readiness_audit.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  mpaudit> $_" }
$mpAuditExit = $LASTEXITCODE
W '--- vital-thunk census ---'
py -3 (Join-Path $main 'tools\pf_vital_thunk_census_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  census> $_" }
$censusExit = $LASTEXITCODE
Beat 'verifiers done, running the actor-entry guard family'

# ---------- 3a. NEW BLOCKING STEP: the guard family that was red ----------
# DEVIATION 4, and it is the reason this job exists in the shape it does.
# In job 178 this tool was graded ONLY through pytest: nineteen tests in
# tests/test_runtimeres_actor_entry_static.py load it, it exited 1 on six pinned
# project-wide censuses that count actor-entry emitters in src/, and so the whole
# gate came back as "19 failed" with the cause buried.  Running the tool on its
# own, FIRST, means a future regression in this family names itself in one line
# instead of hiding inside a nineteen-failure pytest tail.
# TWO conditions, both required: exit 0 AND the printed census line.  The exit
# code alone is not enough - a tool that stops emitting its summary line is a
# tool whose result nobody can read - and the line alone is not enough either.
W '--- actor-entry / RuntimeRes static guard family (expect exit 0 AND "152 guards, 0 failures") ---'
$actorOut  = (py -3 (Join-Path $main 'tools\pf_runtimeres_actor_entry_static.py') 2>&1)
$actorExit = $LASTEXITCODE
$actorOut | Select-Object -Last 6 | ForEach-Object { W "  actor> $_" }
$actorText = ($actorOut | Out-String)
$actorHits = ([regex]::Matches($actorText, [regex]::Escape('152 guards, 0 failures'))).Count
$actorPin  = if ($actorHits -eq 1) { 0 } else { 1 }
W "actor-entry guard pin: exact-text hits = $actorHits (expect 1)  actorPin=$actorPin (expect 0)  exit=$actorExit (expect 0)"
if ($actorPin -ne 0) {
    W 'RED: the actor-entry tool did not print "152 guards, 0 failures".'
    W 'RED: if it printed a DIFFERENT guard count, the census set moved and the'
    W 'RED: pin in this job is the thing that is now stale - say so out loud'
    W 'RED: rather than editing the number to whatever the tool happened to say.'
}
if ($actorExit -ne 0) {
    $actorFails = @($actorOut | Where-Object { ([string]$_) -cmatch '^\s+- ' })
    W "RED: the actor-entry tool exited $actorExit.  Named failures = $($actorFails.Count)"
    $actorFails | ForEach-Object { W "  actorFAIL> $_" }
}
# DEVIATION 5: this step is BLOCKING but NOT short-circuiting.  It folds into
# allGreen, so the job cannot report success while it is red; it does not abort
# on the spot, because the whole point of round 111 was that evidence thrown away
# early has to be re-derived by hand later.  The rest of the battery still runs
# and the transcript still carries it.
Beat 'actor-entry guard done, starting full pytest'

# ---------- 4. pytest, with the WHOLE short test summary kept ----------
# DEVIATION 6: job 178 preserved only `Select-Object -Last 8`, so when nineteen
# tests failed, the NAMES of those nineteen were not in the transcript and had to
# be re-derived by hand afterwards.  This job keeps the tail as well, and then
# ALSO writes out the entire "short test summary info" section and every
# FAILED/ERROR line.  If the section is absent, that is stated in words instead
# of printing nothing, because silence and success look identical in a log and
# only one of them is good news.
# DEVIATION 7: the full pytest transcript in TEMP is NOT deleted at the end (job
# 178 deleted it).  Same reason.  Its path is logged so the chief can read it.
# No pytest total is pinned, here or in 178: the only honest number is the one
# this machine prints, and a number invented in this file would grade nothing.
# The exit code is what is graded; the totals line is REPORTED.
W '--- pytest full suite on Windows with -rs (totals REPORTED, not pinned) ---'
$env:COLUMNS = '200'
$pytestLog = Join-Path $env:TEMP "r111_179_pytest_$stamp.txt"
$pyOut = (py -3 -m pytest tests -q -rs 2>&1)
$pytestExit = $LASTEXITCODE
$pyOut | Out-File -FilePath $pytestLog -Encoding utf8
W "full pytest transcript kept at -> $pytestLog"
$pyOut | Select-Object -Last 8 | ForEach-Object { W "  py> $_" }
$pyCountLine = (@($pyOut | Where-Object { ([string]$_) -cmatch '\d+ (passed|failed|error)' }) | Select-Object -Last 1)
if (-not $pyCountLine) { $pyCountLine = 'no totals line found in the transcript' }
W "MEASURED pytest totals -> $pyCountLine"

$pyLines = @($pyOut | ForEach-Object { [string]$_ })
W "pytest transcript line count = $($pyLines.Count)"
$sumIdx = -1
for ($i = 0; $i -lt $pyLines.Count; $i++) {
    if ($pyLines[$i] -cmatch 'short test summary info') { $sumIdx = $i; break }
}
if ($sumIdx -ge 0) {
    W "--- short test summary info: FULL section, starting at transcript line $sumIdx ---"
    for ($i = $sumIdx; $i -lt $pyLines.Count; $i++) { W "  pysum> $($pyLines[$i])" }
    W '--- end of short test summary info section ---'
} else {
    W 'NOTE: pytest printed NO "short test summary info" section in this run.'
    W 'NOTE: with -rs that section appears whenever anything failed, errored or'
    W 'NOTE: was skipped, so its absence means nothing failed, nothing errored'
    W 'NOTE: and nothing was skipped.  Saying this in words on purpose: an empty'
    W 'NOTE: section and a section this job forgot to print look the same.'
}
$pyFailLines = @($pyLines | Where-Object { $_ -cmatch '^(FAILED|ERROR)' })
$pyFailCount = $pyFailLines.Count
W "FAILED/ERROR lines in the pytest transcript = $pyFailCount"
if ($pyFailCount -eq 0) {
    W 'no FAILED and no ERROR line appears anywhere in the pytest transcript.'
} else {
    W '--- every FAILED / ERROR line, by name ---'
    $pyFailLines | ForEach-Object { W "  pyfail> $_" }
    W '--- end of FAILED / ERROR list ---'
}
Beat 'full pytest done, running the skip census'

W '--- skip census on that exact transcript (expect 0) ---'
py -3 (Join-Path $main 'tools\pf_pytest_precondition_census.py') --report "$pytestLog" 2>&1 | ForEach-Object { W "  skipcensus> $_" }
$skipCensusExit = $LASTEXITCODE
W "skip census exit = $skipCensusExit (expect 0)"

# ---------- 5. guards (copied from job 178 section 8) ----------
$shaAfter = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha AFTER = $shaAfter"
if ($shaAfter -cne $shaBefore) { W 'RED: CANONICAL DB MOVED'; $canonGuard = 1 } else { W 'canonical guard OK'; $canonGuard = 0 }
$v141Dirty = (git --no-optional-locks status --short -- 'current/pf_login_game_server_v141.py' 2>&1 | Out-String).Trim()
if ($v141Dirty) { W "RED: v141 SNAPSHOT DIRTY -> $v141Dirty"; $v141Guard = 1 } else { W 'v141 guard OK'; $v141Guard = 0 }
git --no-optional-locks diff --check 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  git> $_" }
$diffExit = $LASTEXITCODE
W "git diff --check exit = $diffExit (expect 0)"
Beat 'guards done, reporting the tree'

# ---------- 6. REPORT THE TREE.  Read only.  Change nothing. ----------
# DEVIATION 8: job 178 had no section like this, because job 178 believed it was
# the only writer of main.  It is not, and cc46a03 is the proof.  Everything
# below is a READ: rev-parse, log, status --porcelain and diff.  Nothing here
# stages, commits, resets, checks out, or writes a single byte into the worktree
# or the index.
W '=== TREE REPORT (read-only) ==='
W 'This job changes nothing below.  Every command in this section is a read.'
$headNow = (git --no-optional-locks rev-parse HEAD 2>&1)
$headSubject = (git --no-optional-locks log -1 '--pretty=format:%s' HEAD 2>&1 | Out-String).Trim()
W "HEAD sha     = $headNow"
W "HEAD subject = $headSubject"
if ($headSubject -ceq 'wip') {
    W 'NOTE: HEAD subject is literally "wip".  That is the signature of the'
    W 'NOTE: Windows-side pf_git_sync.ps1, not of a gate job.  Gate jobs in this'
    W 'NOTE: project write a whole paragraph as a commit subject.'
}

W '--- git status --porcelain, IN FULL (no truncation) ---'
$dirty = @(git --no-optional-locks status --porcelain 2>&1)
$statusExit = $LASTEXITCODE
W "git status --porcelain exit = $statusExit (expect 0);  dirty entries = $($dirty.Count)"
if ($dirty.Count -eq 0) {
    W '  st> (the working tree is clean - status printed nothing at all)'
} else {
    $dirty | ForEach-Object { W "  st> $_" }
}
W '--- end of git status --porcelain ---'

# The twelve paths of cc46a03, taken FROM THE COMMIT ITSELF and never typed from
# memory - the same discipline as reading the canonical sha from CANON_SHA.txt.
# This comparison is REPORTED and deliberately NOT enforced: this job has no
# standing to demand that a tree it did not create looks any particular way, and
# a mismatch here is information for a human, not a gate failure.  Said plainly
# so that nobody later reads a "match" count as an assertion that passed.
$cc = 'cc46a03'
W "--- worktree vs commit $cc (the commit the sync made, titled 'wip') ---"
$ccRaw = @(git --no-optional-locks show --name-only '--pretty=format:' "$cc" 2>&1)
$ccShowExit = $LASTEXITCODE
if ($ccShowExit -ne 0) {
    W "REPORTED (not a gate failure): could not read commit $cc, git exit $ccShowExit"
    $ccRaw | Select-Object -First 3 | ForEach-Object { W "  cc> $_" }
    $ccMatch = "commit $cc unreadable (git exit $ccShowExit)"
} else {
    $ccFiles = @($ccRaw | ForEach-Object { ([string]$_).Trim().Trim('"') } | Where-Object { $_ -ne '' })
    W "paths named by $cc = $($ccFiles.Count) (the chief's note says twelve)"
    $same = 0
    $diff = 0
    $gone = 0
    foreach ($f in $ccFiles) {
        $full = Join-Path $main ($f -replace '/', '\')
        $onDisk = Test-Path -LiteralPath $full
        git --no-optional-locks diff --quiet "$cc" -- "$f" 2>&1 | Out-Null
        $dq = $LASTEXITCODE
        if (-not $onDisk) {
            $gone++
            W "  cc> ABSENT-FROM-DISK  $f"
        } elseif ($dq -eq 0) {
            $same++
            W "  cc> matches-commit    $f"
        } elseif ($dq -eq 1) {
            $diff++
            W "  cc> DIFFERS-FROM-COMMIT  $f"
        } else {
            $diff++
            W "  cc> UNDECIDED (git diff exit $dq)  $f"
        }
    }
    $ccMatch = "$same match, $diff differ, $gone absent, of $($ccFiles.Count) paths"
    W "worktree vs $cc -> $ccMatch"
    W 'REPORTED ONLY.  This job does not act on that count, in either direction.'
    if ($diff -ne 0 -or $gone -ne 0) {
        W "NOTE: a path that differs from $cc is not by itself a problem - the"
        W 'NOTE: actor-entry census repair landed after that commit.  It is'
        W 'NOTE: written down here so the next reader can see the tree this gate'
        W 'NOTE: actually graded, rather than the tree they assume it graded.'
    }
}
W '=== END TREE REPORT.  Nothing above was staged, committed, reset or checked out. ==='

# ---------- 7. the verdict ----------
$allGreen = ($seamExit -eq 0) -and ($covTestExit -eq 0) -and ($covExit -eq 0) -and `
            ($ledgerExit -eq 0) -and ($ledgerPin -eq 0) -and ($mpAuditExit -eq 0) -and `
            ($censusExit -eq 0) -and ($actorExit -eq 0) -and ($actorPin -eq 0) -and `
            ($pytestExit -eq 0) -and ($skipCensusExit -eq 0) -and ($canonGuard -eq 0) -and `
            ($v141Guard -eq 0) -and ($diffExit -eq 0) -and ($statusExit -eq 0)
W "ALL GREEN = $allGreen"

# FAIL CLOSED.  The most expensive recurring bug in this project is an exit that
# reports a problem and then returns success anyway.  There are exactly two ends
# below: red -> exit 50, green -> exit 0.  There is no third.
if (-not $allGreen) {
    $redFields = @()
    if ($seamExit       -ne 0) { $redFields += "seam=$seamExit" }
    if ($covTestExit    -ne 0) { $redFields += "covTest=$covTestExit" }
    if ($covExit        -ne 0) { $redFields += "coverage=$covExit" }
    if ($ledgerExit     -ne 0) { $redFields += "ledger=$ledgerExit" }
    if ($ledgerPin      -ne 0) { $redFields += "ledgerPin=$ledgerPin" }
    if ($mpAuditExit    -ne 0) { $redFields += "mpaudit=$mpAuditExit" }
    if ($censusExit     -ne 0) { $redFields += "census=$censusExit" }
    if ($actorExit      -ne 0) { $redFields += "actorEntry=$actorExit" }
    if ($actorPin       -ne 0) { $redFields += "actorPin=$actorPin" }
    if ($pytestExit     -ne 0) { $redFields += "pytest=$pytestExit" }
    if ($skipCensusExit -ne 0) { $redFields += "skipCensus=$skipCensusExit" }
    if ($canonGuard     -ne 0) { $redFields += "canonGuard=$canonGuard" }
    if ($v141Guard      -ne 0) { $redFields += "v141Guard=$v141Guard" }
    if ($diffExit       -ne 0) { $redFields += "diffcheck=$diffExit" }
    if ($statusExit     -ne 0) { $redFields += "status=$statusExit" }
    $redText = ($redFields -join ' ')
    W "RED FIELDS -> $redText"
    W 'The gate is RED.  Nothing was committed - but note that this job never'
    W 'commits anything even when it is green, so a red gate is NOT what is'
    W 'keeping this work out of main.  The sync job is not gated by this file.'
    Finish179 -Code 50 -Verdict "RED gate - nothing committed (this job never commits).  Red fields: $redText" -Next 'Read the named red fields in the transcript, fix them, and re-run job 179.  Note that the Windows-side sync can commit and push independently of this gate, so a red gate here does not mean the work is being held back from main.'
}
Finish179 -Code 0 -Verdict 'GREEN gate.  The full battery passed, including the actor-entry guard family that was red in job 178.  NOTHING was committed, staged or pushed by this job.' -Next 'The tree is proved green as it stands.  Decide by hand what to do about commit cc46a03 (the sync-made "wip" commit on main) and about whether the Windows-side sync should be committing at all while a gate exists - job 179 deliberately took no position beyond reporting it.'

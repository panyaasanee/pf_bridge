# Job 178 - chief round 111.  Gate the full Windows battery, then commit exactly
# the THIRTEEN paths of the NPC-HP-LINK-001 lane (HYP-PF-029) and nothing else.
#
# MODEL: staged\175_round109_path_d_ci_status_gate_commit.ps1.  Same structure,
# same battery, same exit codes, same evidence, same receipt shape.  Every place
# this file differs from 175 is marked with the word DEVIATION and a reason.
#
# THE THIRTEEN PATHS (all thirteen are this round's work, and only this round's):
#   M  .gitignore
#   M  docs/HYPOTHESIS_LEDGER.json
#   M  reports/PF_DAMAGE_NPC_TARGET001_SECOND_PROFILE_20260820.md
#   ?  reports/PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md
#   ?  scenarios/npc_hp_link_hypothesis_target_sweep.json
#   M  src/pirateforce_foundation/app.py
#   ?  src/pirateforce_foundation/npc_hp_link_hypothesis.py
#   M  src/pirateforce_foundation/runtime.py
#   ?  tests/test_npc_hp_link_dispatch.py
#   ?  tests/test_npc_hp_link_hypothesis.py
#   ?  tools/pf_npc_hp_link_headless_replay.py
#   ?  tools/verify_npc_hp_link_encoder.py
#   M  tools/verify_hypothesis_ledger.py
#
# THE ONE THING THAT MUST NOT BE STAGED: .claude/ is untracked in this tree and
# belongs to a CLOUD round, not to this one.  It is dirty, so job 175's
# only-declared-paths-may-be-dirty guard would abort on it; it is named below as
# a KNOWN-AND-EXCLUDED dirty path instead, and the staged set is then asserted to
# equal the thirteen EXACTLY, in count and in content, with a separate explicit
# assertion that nothing under .claude is in the index.  Staging is by explicit
# `git add` of each named path after `git read-tree HEAD`, never `git add -A` and
# never `git add .`: the sandbox index is stale and a blanket add invents
# phantom deletions.
#
# MEASURABLE END CONDITIONS:
#   1. the only dirty paths are the declared thirteen plus .claude/
#   2. all thirteen ARE dirty (a declared path that is clean means this round's
#      work is not where the job says it is)
#   3. eight text guards prove the lane is really in the worktree
#   4. non-ascii bytes are 0 in the ten files that are ASCII, and UNCHANGED FROM
#      HEAD in the three that already carried non-ascii prose before this round
#   5. the seven new paths are NOT gitignored (round 87's lesson: on disk is not
#      in the repository)
#   6. the full bridge battery is green, including the whole pytest suite
#   7. the staged set equals the thirteen exactly - otherwise ABORT, uncommitted
#   8. commit lands, HEAD moves, and the COMMITTED BLOBS carry the lane
#
# NOT done here: git push, branch create/delete/rename, pull request, anything
# under .github/workflows/.  There is an uncommitted merge-claude-pr situation
# and open pull requests, and those are Panya's decision alone; this job stays
# out of all of it and touches no remote.
# NOT touched: LOCK_GAME.txt, the server, the client, ports 10188/10189, any
# database write, and the pf_bridge repository index.
# This job takes LOCK_GIT.txt at the start and RELEASES it on EVERY exit path,
# including every failure - see DEVIATION 1.
# ASCII ONLY.  Quote every path that contains a space.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\178_round111_npc_hp_link.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 111 GATE AND COMMIT (job 178) - NPC-HP-LINK-001 / HYP-PF-029, 13 paths  $stamp ===" | Out-File -FilePath $log -Encoding utf8

$lockGit = Join-Path $bridge 'LOCK_GIT.txt'

# ---------- DEVIATION 0: dot-source the flag helpers, never copy them ----------
# Standing instruction from chief round 109: jobs 176 and later MUST dot-source
# staged\TEMPLATE_lock_flag_helpers.ps1 and MUST NOT copy the flag block out of
# job 169.  Job 175 wrote LOCK_GIT.txt with Out-File -Encoding utf8, which on
# Windows PowerShell 5.1 prepends a BOM, while its acquire check tested '^HELD:',
# which a BOM'd line does not match - so the check reported the flag FREE at
# exactly the moment it was HELD, silently, for sixteen jobs.  The template fixes
# it twice over: Write-Flag emits no BOM, Test-FlagHeld tolerates one anyway.
# Job 177 is the receipt (JOB177_VERDICT=PASS, four cases including a BOM'd HELD).
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
# So that the release writer can be called from any abort path and still print a
# complete, honest verdict line.  -1 means "never measured", which is a different
# thing from 0 and must stay a different thing.
$asciiGuard   = -1
$fixGuard     = -1
$unexpected   = -1
$ignoreGuard  = -1
$seamExit     = -1
$covTestExit  = -1
$covExit      = -1
$ledgerExit   = -1
$ledgerPin    = -1
$mpAuditExit  = -1
$censusExit   = -1
$pytestExit   = -1
$skipCensusExit = -1
$canonGuard   = -1
$v141Guard    = -1
$diffExit     = -1
$stagedSetOk  = -1
$allGreen     = $false
$committed    = 0
$blobOk       = -1
$headBefore   = 'unknown'
$headAfter    = 'unknown'
$pyCountLine  = 'not measured'

# ---------- DEVIATION 1: ONE release writer, used by EVERY exit path ----------
# Job 175 releases the flag only on the success path: its exits 30-35 and 41-45
# all leave LOCK_GIT.txt HELD, and the next job then has to take it over on the
# 20-minute rule.  The brief for this round is explicit that every abort must
# release.  So there is exactly one function that writes the RELEASED block and
# exits, and no `exit` statement anywhere below it.  The two exits ABOVE it are
# the only ones that do not release, and correctly so: at that point this job has
# not taken the flag, and releasing a flag you do not hold is stomping it.
# RESIDUAL, stated rather than hidden: this covers every ABORT PATH THIS FILE
# DEFINES.  It does not cover the machine losing power or an unhandled
# TERMINATING error thrown by a cmdlet, either of which would leave the flag
# HELD with a HEARTBEAT line whose timestamp stops.  That case is what the
# takeover rule at the bottom of LOCK_GIT.txt exists for (age >= 20 min AND
# silent in all three channels), and pretending otherwise would be worse than
# saying it here.  ErrorActionPreference is Continue, as in job 175, so the
# ordinary failures - a missing file, a non-zero exit code, a null - are
# non-terminating and DO reach the release writer below.
function Finish178 {
    param(
        [Parameter(Mandatory = $true)][int]    $Code,
        [Parameter(Mandatory = $true)][string] $Verdict,
        [Parameter(Mandatory = $true)][string] $Next
    )
    $headShort = (git --no-optional-locks rev-parse --short HEAD 2>&1)
    $lines = @(
        "RELEASED: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
        "BY: job 178 (chief round 111) - released by the job itself, exit $Code",
        "done: $Verdict",
        "      Round 111 built the NPC-HP-LINK-001 lane (HYP-PF-029): the first",
        "      lane in this tree that moves a TARGET's hit points.  Thirteen paths",
        "      declared; .claude/ is untracked cloud-round work and was NEVER",
        "      staged - the staged set was asserted equal to the thirteen, in",
        "      count and in content, before any commit was attempted.",
        "      allGreen=$allGreen committed=$committed blobOk=$blobOk",
        "      ascii=$asciiGuard fixGuard=$fixGuard unexpectedDirty=$unexpected ignoreGuard=$ignoreGuard",
        "      seam=$seamExit covTest=$covTestExit coverage=$covExit ledger=$ledgerExit ledgerPin=$ledgerPin",
        "      mpaudit=$mpAuditExit census=$censusExit pytest=$pytestExit skipCensus=$skipCensusExit",
        "      canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit stagedSet=$stagedSetOk",
        "      pytest totals MEASURED, not pinned -> $pyCountLine",
        "head: $headShort  (was $headBefore)",
        "next: $Next",
        "      chief next job = 179.  tester = 9xx (0xxx while holding LOCK_GAME).",
        "warn: this job did NOT push, did NOT create/delete/modify any branch, did",
        "      NOT open or touch a pull request, and did NOT touch",
        "      .github/workflows/ at all.  The merge-claude-pr situation and the",
        "      open pull requests are Panya's decision alone.",
        "      The pf_bridge repository index was deliberately NOT touched, for the",
        "      reason jobs 175 and 176 gave: Panya has commits in flight there and",
        "      two writers on one index is how a dirty diff disappears.",
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
    W "LOCK_GIT.txt RELEASED by job 178 (exit $Code, committed=$committed)"
    W '=== 178 SUMMARY ==='
    @(
        "ascii=$asciiGuard fixGuard=$fixGuard unexpectedDirty=$unexpected ignoreGuard=$ignoreGuard",
        "seam=$seamExit covTest=$covTestExit coverage=$covExit ledger=$ledgerExit ledgerPin=$ledgerPin",
        "mpaudit=$mpAuditExit census=$censusExit pytest=$pytestExit skipCensus=$skipCensusExit",
        "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit stagedSet=$stagedSetOk",
        "pytest totals (measured, not pinned) -> $pyCountLine",
        "verdict text -> $Verdict"
    ) | ForEach-Object { W $_ }
    # The single line the chief greps.  One line, always emitted, on every path.
    W "JOB178_VERDICT allGreen=$allGreen committed=$committed blobOk=$blobOk exit=$Code headBefore=$headBefore headAfter=$headAfter"
    W '=== 178 DONE ==='
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
    "BY: job 178 (chief round 111) - gate and commit the NPC-HP-LINK-001 lane",
    "    (HYP-PF-029), thirteen paths, .claude/ deliberately excluded.",
    "PLAN: guards (declared-paths-only dirty, all thirteen present, lane text",
    "      present, ascii, not-gitignored) -> full bridge battery -> guarded",
    "      13-path commit with an exact staged-set assertion -> committed-blob",
    "      acceptance -> release immediately.  No push, no branch, no pull",
    "      request, no .github/workflows/.  Does NOT touch LOCK_GAME (no",
    "      server/client/DB writes) and does NOT touch the pf_bridge git index."
)
W 'LOCK_GIT.txt set to HELD by job 178 (written by Write-Flag - no BOM)'

Set-Location -LiteralPath $main
$headBefore = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD before = $headBefore"

# DEVIATION 2: job 175 printed an expected HEAD prefix in the log line.  This job
# does not, because two commits (merge-claude-pr) landed after 89ce13b and a
# hardcoded expectation would be a number typed from memory.  HEAD is REPORTED,
# both in the log and in the receipt, and never asserted.

$paths1 = @(
    '.gitignore',
    'docs/HYPOTHESIS_LEDGER.json',
    'reports/PF_DAMAGE_NPC_TARGET001_SECOND_PROFILE_20260820.md',
    'reports/PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md',
    'scenarios/npc_hp_link_hypothesis_target_sweep.json',
    'src/pirateforce_foundation/app.py',
    'src/pirateforce_foundation/npc_hp_link_hypothesis.py',
    'src/pirateforce_foundation/runtime.py',
    'tests/test_npc_hp_link_dispatch.py',
    'tests/test_npc_hp_link_hypothesis.py',
    'tools/pf_npc_hp_link_headless_replay.py',
    'tools/verify_npc_hp_link_encoder.py',
    'tools/verify_hypothesis_ledger.py'
)
# The seven that do not exist at HEAD.  Round 87's lesson applies to every one of
# them: a file on disk that .gitignore excludes is not in the repository, and a
# ledger that cites it is citing something a fresh clone cannot read.
$pathsNew = @(
    'reports/PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md',
    'scenarios/npc_hp_link_hypothesis_target_sweep.json',
    'src/pirateforce_foundation/npc_hp_link_hypothesis.py',
    'tests/test_npc_hp_link_dispatch.py',
    'tests/test_npc_hp_link_hypothesis.py',
    'tools/pf_npc_hp_link_headless_replay.py',
    'tools/verify_npc_hp_link_encoder.py'
)
# KNOWN-AND-EXCLUDED.  Dirty, allowed to be dirty, and forbidden to be staged.
$allowedUntracked = @('.claude/')
W "declared path set = $($paths1.Count) (expect 13);  new paths = $($pathsNew.Count) (expect 7)"
W "known-and-excluded dirty paths = $($allowedUntracked -join ', ')"

# ---------- 1. index.lock, checked first ----------
$lockPath = Join-Path $main '.git\index.lock'
if (Test-Path -LiteralPath $lockPath) {
    $lk = Get-Item -LiteralPath $lockPath
    $ageMin = [math]::Round(((Get-Date) - $lk.LastWriteTime).TotalMinutes, 1)
    W "index.lock present: size=$($lk.Length) bytes  age=${ageMin} min"
    $gitProcs = @(Get-Process -Name git -ErrorAction SilentlyContinue)
    if ($lk.Length -ne 0)      { W 'ABORT: index.lock is NOT empty. Do not delete.'; Finish178 -Code 30 -Verdict 'ABORT at index.lock: the lock file is not empty, so a real git process owns it.' -Next 'Find the git process that owns the index and let it finish, then re-run job 178.' }
    if ($gitProcs.Count -gt 0) { W 'ABORT: a git process is running.'; Finish178 -Code 31 -Verdict 'ABORT at index.lock: a git process is running right now.' -Next 'Wait for that git process to exit, then re-run job 178.' }
    if ($ageMin -lt 10)        { W 'ABORT: index.lock younger than 10 minutes.'; Finish178 -Code 32 -Verdict 'ABORT at index.lock: the lock is younger than ten minutes, so it may be live.' -Next 'Wait until the lock is at least ten minutes old, then re-run job 178.' }
    Remove-Item -LiteralPath $lockPath -Force
    if (Test-Path -LiteralPath $lockPath) { W 'ABORT: could not remove index.lock'; Finish178 -Code 33 -Verdict 'ABORT at index.lock: a stale lock could not be removed.' -Next 'Remove .git\index.lock by hand, then re-run job 178.' }
    W 'stale index.lock removed'
} else { W 'no index.lock present' }

# ---------- 2. worktree state: the declared thirteen, plus .claude/, and NOTHING else ----------
$dirty = @(git --no-optional-locks status --porcelain 2>&1)
W "worktree dirty paths = $($dirty.Count) (expect 14 = 13 declared + .claude/)"
$dirty | ForEach-Object { W "  st> $_" }
$unexpected = 0
$dirtyNorm = @()
foreach ($d in $dirty) {
    $p = ([string]$d -replace '^..\s+', '') -replace '\\', '/'
    $p = $p.Trim('"')
    $dirtyNorm += $p
    if ($allowedUntracked -ccontains $p) {
        W "  KNOWN-AND-EXCLUDED (cloud-round work, must never be staged)> $p"
        continue
    }
    if ($paths1 -cnotcontains $p) { W "  UNEXPECTED DIRTY PATH> $p"; $unexpected = 1 }
}
# DEVIATION 3: job 175 only checks that nothing UNDECLARED is dirty.  This job
# also checks the other direction - that every declared path IS dirty - because a
# declared path that is clean means this round's work is not where the job says
# it is, and staging it would then commit nothing while reporting thirteen.
foreach ($p in $paths1) {
    if ($dirtyNorm -cnotcontains $p) { W "  DECLARED PATH IS NOT DIRTY> $p"; $unexpected = 1 }
}
if ($unexpected -eq 1) {
    W 'ABORT: the worktree is not the shape this job declared - refusing.'
    Finish178 -Code 41 -Verdict 'ABORT at the worktree guard: dirty paths are not exactly the declared thirteen plus .claude/.' -Next 'Read the st> lines in the transcript, reconcile the declared path list with the tree, and re-run job 178.'
}

# ---------- 3. canonical DB guard (read from CANON_SHA.txt, never hardcoded) ----------
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$shaBefore = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
$canonExpect = (Get-Content -LiteralPath (Join-Path $bridge 'CANON_SHA.txt') -Raw).Trim()
W "canonical sha BEFORE = $shaBefore"
if ($shaBefore -cne $canonExpect) {
    W "ABORT: canonical sha does not match CANON_SHA.txt -> $canonExpect"
    Finish178 -Code 13 -Verdict 'ABORT at the canonical guard: state\pirateforce.sqlite3 does not match CANON_SHA.txt BEFORE anything ran.' -Next 'Do not commit.  Find out what wrote the canonical database, then re-run job 178.'
}
W 'canonical matches CANON_SHA.txt'

# ---------- 4. the lane must actually be present in the worktree ----------
$fixGuard = 0
function CountIn($relPath, $needle) {
    $full = Join-Path $main ($relPath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $full)) { return -1 }
    $t = [System.IO.File]::ReadAllText($full)
    return ([regex]::Matches($t, [regex]::Escape($needle))).Count
}
$g1 = CountIn 'src/pirateforce_foundation/app.py'                   'npc_hp_link_hypothesis_scenario='
$g2 = CountIn 'src/pirateforce_foundation/runtime.py'               'def _dispatch_npc_hp_link_hypothesis(self, parsed):'
$g3 = CountIn 'scenarios/npc_hp_link_hypothesis_target_sweep.json'  '"wired": true'
$g4 = CountIn '.gitignore'                                          '!/tools/verify_npc_hp_link_encoder.py'
$g5 = CountIn '.gitignore'                                          '!/tools/pf_npc_hp_link_headless_replay.py'
$g6 = CountIn '.gitignore'                                          '!/reports/PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md'
$g7 = CountIn 'tools/verify_hypothesis_ledger.py'                   '"HYP-PF-029"'
$g8 = CountIn 'src/pirateforce_foundation/npc_hp_link_hypothesis.py' 'def npc_hp_link_wire_unlock('
W "lane guards: appJoin=$g1(1) runtimeDispatch=$g2(1) scenarioWired=$g3(1) ignoreEncoder=$g4(1)"
W "             ignoreReplay=$g5(1) ignoreReport=$g6(1) ledgerIds=$g7(2) composer=$g8(1)"
if ($g1 -ne 1 -or $g2 -ne 1 -or $g3 -ne 1 -or $g4 -ne 1 -or $g5 -ne 1 -or $g6 -ne 1 -or $g7 -ne 2 -or $g8 -ne 1) { $fixGuard = 1 }
if ($fixGuard -eq 1) {
    W 'ABORT: the lane this job exists to commit is not in the worktree as declared.'
    Finish178 -Code 42 -Verdict 'ABORT at the lane guard: one of the eight text guards did not find what it was told to find.' -Next 'Read the lane guards line, repair the worktree, and re-run job 178.'
}

# ---------- 5. ASCII guard ----------
# DEVIATION 4: job 175 had ONE declared path and demanded 0 non-ascii bytes in it.
# Three of this round's thirteen already carried non-ascii prose at HEAD:
#   docs/HYPOTHESIS_LEDGER.json
#   reports/PF_DAMAGE_NPC_TARGET001_SECOND_PROFILE_20260820.md
#   tools/verify_hypothesis_ledger.py
# For those three the rule is job 169's rule: the count must be UNCHANGED FROM
# HEAD, which proves this round added none of its own.  Job 169 first got that
# comparison wrong by reading the HEAD blob through PowerShell text conversion
# (4270 became 12207) and correctly refused to commit on its own arithmetic; the
# comparison is therefore done inside ONE python process, on raw bytes from git
# plumbing, so nothing is ever decoded.  Two numbers that were not derived the
# same way are not a comparison.
# CR bytes are demanded to be 0 on ALL thirteen: this tree is LF-only and a CRLF
# that arrives through an editor is a diff nobody meant to write.
$asciiGuard = 0
$asciiExempt = @(
    'docs/HYPOTHESIS_LEDGER.json',
    'reports/PF_DAMAGE_NPC_TARGET001_SECOND_PROFILE_20260820.md',
    'tools/verify_hypothesis_ledger.py'
)
foreach ($p in $paths1) {
    $full = Join-Path $main ($p -replace '/', '\')
    $bytes = [System.IO.File]::ReadAllBytes($full)
    $nonAscii = 0
    $crlf = 0
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        if ($bytes[$i] -gt 127) { $nonAscii++ }
        if ($bytes[$i] -eq 13)  { $crlf++ }
    }
    if ($asciiExempt -ccontains $p) {
        W "non-ascii bytes in $p = $nonAscii (EXEMPT - compared against HEAD below);  CR bytes = $crlf (expect 0)"
    } else {
        W "non-ascii bytes in $p = $nonAscii (expect 0);  CR bytes = $crlf (expect 0)"
        if ($nonAscii -ne 0) { $asciiGuard = 1 }
    }
    if ($crlf -ne 0) { $asciiGuard = 1 }
}
$asciiPy = @'
import os, subprocess, sys
rel = sys.argv[1]
on_disk = open(os.path.join(*rel.split("/")), "rb").read()
head = subprocess.run(
    ["git", "--no-optional-locks", "cat-file", "blob", "HEAD:" + rel],
    capture_output=True)
if head.returncode != 0:
    print("cannot read HEAD blob for %s: %s"
          % (rel, head.stderr.decode("utf-8", "replace")))
    sys.exit(2)
now = sum(1 for b in on_disk if b > 127)
was = sum(1 for b in head.stdout if b > 127)
print("%s non-ascii: now=%d atHEAD=%d" % (rel, now, was))
sys.exit(0 if now == was else 1)
'@
$asciiFile = Join-Path $env:TEMP "r111_ascii_$stamp.py"
Set-Content -LiteralPath $asciiFile -Value $asciiPy -Encoding UTF8
foreach ($p in $asciiExempt) {
    py -3 "$asciiFile" "$p" 2>&1 | ForEach-Object { W "  ascii> $_" }
    $repCmp = $LASTEXITCODE
    W "  non-ascii comparison exit for $p = $repCmp (expect 0 - this round adds no new non-ascii)"
    if ($repCmp -ne 0) { $asciiGuard = 1 }
}
Remove-Item -LiteralPath $asciiFile -Force -ErrorAction SilentlyContinue
if ($asciiGuard -eq 1) {
    W 'ABORT: a declared path is not ASCII/LF as required, or added non-ascii this round.'
    Finish178 -Code 45 -Verdict 'ABORT at the ascii guard: a declared path carries non-ascii bytes it must not, or CR bytes, or grew new non-ascii relative to HEAD.' -Next 'Read the non-ascii lines in the transcript, clean the offending file, and re-run job 178.'
}

# ---------- 6. the seven new paths must NOT be gitignored (round 87's lesson) ----------
$ignoreGuard = 0
foreach ($p in $pathsNew) {
    git --no-optional-locks check-ignore -q -- "$p" 2>&1 | Out-Null
    $ci = $LASTEXITCODE
    W "check-ignore $p -> exit $ci (expect 1 = NOT ignored)"
    if ($ci -eq 0) { $ignoreGuard = 1 }
}
if ($ignoreGuard -eq 1) {
    W 'ABORT: a new path is gitignored - it would be on disk but not in the repository.'
    Finish178 -Code 44 -Verdict 'ABORT at the gitignore guard: one of the seven new paths is excluded by .gitignore.' -Next 'Add the missing allow-list line to .gitignore, then re-run job 178.'
}
Beat 'preflight done, starting battery'

# ---------- 7. the battery ----------
# Step list, invocation and pass criteria copied verbatim from job 175.  Nothing
# added, nothing re-derived from memory.  The ONE step of job 175 that is absent
# is its 5b YAML parse (DEVIATION 5): that step exists to check
# .github/workflows/gate-windows.yml, and this job does not touch
# .github/workflows/ at all, so there is nothing for it to parse.  Dropping a
# check because its subject is absent is not the same as skipping a check, and
# the receipt no longer carries a yaml= field for exactly that reason.
#
# THE SEAM TEST IS FIRST AND IT IS NOT OPTIONAL THIS ROUND: this commit touches
# .gitignore and files under reports/, which is precisely the standing rule's
# trigger (jobs 168/169 ran it for the same reason).
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

# DEVIATION 6, and it is the ONE expected value that moves this round.
# Job 175 pins NO entry count at all - it runs the verifier and reads its exit
# code, nothing more.  (Job 169 carried the number 35 in a COMMENT only, which
# is prose and grades nothing.)  HYP-PF-029 was appended this round, so the
# ledger now holds 36 entries and not 35, and the verifier prints the number it
# actually loaded.  That printed line is graded here, so the round's one moving
# number is checked by a machine instead of remembered by a reader.  It is
# BLOCKING and it is red in both directions: 35 fails, 37 fails.
W '--- ledger verifier (expect PASS with entries=36 - HYP-PF-029 was appended this round) ---'
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
Beat 'verifiers done, starting full pytest'

# DEVIATION 7: job 175 pins no pytest total and neither does this job.  Round 111
# adds tests/test_npc_hp_link_hypothesis.py and tests/test_npc_hp_link_dispatch.py,
# so the total is certainly larger than the 1897 of job 168 - but the only honest
# number is the one this machine prints, and a number invented here would be a
# pin that grades nothing.  The totals line is REPORTED, into the log and into
# the receipt, for the chief to read.  The exit code is what is graded.
W '--- pytest full suite on Windows with -rs (totals REPORTED, not pinned) ---'
$env:COLUMNS = '200'
$pytestLog = Join-Path $env:TEMP "r111_pytest_$stamp.txt"
$pyOut = (py -3 -m pytest tests -q -rs 2>&1)
$pytestExit = $LASTEXITCODE
$pyOut | Out-File -FilePath $pytestLog -Encoding utf8
$pyOut | Select-Object -Last 8 | ForEach-Object { W "  py> $_" }
$pyCountLine = (@($pyOut | Where-Object { ([string]$_) -cmatch '\d+ (passed|failed|error)' }) | Select-Object -Last 1)
if (-not $pyCountLine) { $pyCountLine = 'no totals line found in the transcript' }
W "MEASURED pytest totals -> $pyCountLine"
Beat 'full pytest done, running the skip census'

W '--- skip census on that exact transcript (expect 0) ---'
py -3 (Join-Path $main 'tools\pf_pytest_precondition_census.py') --report "$pytestLog" 2>&1 | ForEach-Object { W "  skipcensus> $_" }
$skipCensusExit = $LASTEXITCODE
W "skip census exit = $skipCensusExit (expect 0)"

# ---------- 8. guards ----------
$shaAfter = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
if ($shaAfter -cne $shaBefore) { W 'RED: CANONICAL DB MOVED'; $canonGuard = 1 } else { W 'canonical guard OK'; $canonGuard = 0 }
$v141Dirty = (git --no-optional-locks status --short -- 'current/pf_login_game_server_v141.py' 2>&1 | Out-String).Trim()
if ($v141Dirty) { W "RED: v141 SNAPSHOT DIRTY -> $v141Dirty"; $v141Guard = 1 } else { W 'v141 guard OK'; $v141Guard = 0 }
git --no-optional-locks diff --check 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  git> $_" }
$diffExit = $LASTEXITCODE

$allGreen = ($asciiGuard -eq 0) -and ($fixGuard -eq 0) -and ($unexpected -eq 0) -and `
            ($ignoreGuard -eq 0) -and ($seamExit -eq 0) -and ($covTestExit -eq 0) -and `
            ($covExit -eq 0) -and ($ledgerExit -eq 0) -and ($ledgerPin -eq 0) -and `
            ($mpAuditExit -eq 0) -and ($censusExit -eq 0) -and ($pytestExit -eq 0) -and `
            ($skipCensusExit -eq 0) -and ($canonGuard -eq 0) -and ($v141Guard -eq 0) -and `
            ($diffExit -eq 0)
W "ALL GREEN = $allGreen"

# ---------- 9. guarded commit: read-tree HEAD, stage ONLY the declared thirteen ----------
if (-not $allGreen) {
    W 'NOT COMMITTING - a guard is red.  The edits stay as a dirty diff'
    W '(never reset/clean by iron rule) - receipt says so for the next round.'
    Finish178 -Code 50 -Verdict 'RED battery - NOT COMMITTED.  The thirteen paths are still a dirty diff and nothing was staged.' -Next 'Read the transcript for the field that is not 0, fix it, and re-run job 178.  Nothing was committed, nothing was pushed, no branch moved.'
}
Beat 'battery green, committing'
W '--- GUARDED COMMIT: read-tree HEAD, then stage ONLY the thirteen round-111 paths ---'
$rt = (git --no-optional-locks read-tree HEAD 2>&1 | Out-String).Trim()
if ($rt) { W "  read-tree> $rt" }
if ($LASTEXITCODE -ne 0) {
    W 'ABORT: read-tree failed'
    Finish178 -Code 34 -Verdict 'ABORT before staging: git read-tree HEAD failed, so the index was never made trustworthy.' -Next 'Investigate the git index by hand.  Nothing was staged and nothing was committed.'
}
$addFailed = 0
foreach ($p in $paths1) {
    $o = (git --no-optional-locks add -- "$p" 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { W "  RED add> $p :: $o"; $addFailed = 1 }
    elseif ($o) { W "  add(warn)> $p :: $o" }
}
if ($addFailed -eq 1) {
    W 'ABORT: an add failed - refusing partial commit'
    git --no-optional-locks read-tree HEAD 2>&1 | Out-Null
    W 'index restored to HEAD (read-tree only - the worktree was not touched)'
    Finish178 -Code 35 -Verdict 'ABORT during staging: an explicit git add failed, so the staged set could never be the declared thirteen.' -Next 'Read the RED add> line, fix that path, and re-run job 178.  Nothing was committed.'
}

# ---------- 9a. THE STAGED SET MUST EQUAL THE THIRTEEN, EXACTLY ----------
# Count AND content, both directions, case-sensitively.  This is the guard that
# keeps .claude/ out of the commit: it is untracked cloud-round work, it was
# never handed to git add, and if it is in the index anyway then something this
# job does not understand has happened and the correct answer is to stop.
$stagedRaw = @(git --no-optional-locks diff --cached --name-only 2>&1)
$staged = @($stagedRaw | ForEach-Object { (([string]$_).Trim().Trim('"')) -replace '\\', '/' })
W "staged path count = $($staged.Count) (expect 13)"
$staged | ForEach-Object { W "  cached> $_" }
git --no-optional-locks diff --cached --stat 2>&1 | Select-Object -Last 16 | ForEach-Object { W "  staged> $_" }

$stagedSetOk = 0
$expectSorted = @($paths1 | Sort-Object)
$gotSorted    = @($staged | Sort-Object)
if ($gotSorted.Count -ne $expectSorted.Count) {
    W "RED: staged count is $($gotSorted.Count), expected $($expectSorted.Count)"
    $stagedSetOk = 1
} else {
    for ($i = 0; $i -lt $gotSorted.Count; $i++) {
        if ($gotSorted[$i] -cne $expectSorted[$i]) {
            W "RED: staged set differs at index $i -> got '$($gotSorted[$i])' expected '$($expectSorted[$i])'"
            $stagedSetOk = 1
        }
    }
}
# Said twice, on purpose, and the second saying does not lean on the first.
$claudeStaged = @($staged | Where-Object { $_ -ceq '.claude' -or $_ -clike '.claude/*' })
if ($claudeStaged.Count -ne 0) {
    W "RED: .claude is in the index - that is a CLOUD round's work and is not this round's to commit"
    $claudeStaged | ForEach-Object { W "  CLAUDE> $_" }
    $stagedSetOk = 1
}
$delLines = (git --no-optional-locks diff --cached --name-status 2>&1 | Select-String -Pattern '^D' -CaseSensitive)
if ($delLines) {
    W 'RED: staged set contains DELETIONS - the stale-index phantom-deletion shape'
    $delLines | ForEach-Object { W "  DEL> $_" }
    $stagedSetOk = 1
}
if ($stagedSetOk -ne 0) {
    W 'ABORT: the staged set is not exactly the declared thirteen.  NOT COMMITTING.'
    git --no-optional-locks read-tree HEAD 2>&1 | Out-Null
    W 'index restored to HEAD (read-tree only - the worktree was not touched)'
    Finish178 -Code 36 -Verdict 'ABORT at the staged-set assertion: the index was not exactly the declared thirteen, so no commit was made.' -Next 'Read the cached> lines against the declared list.  Nothing was committed; the index was reset to HEAD and the worktree is untouched.'
}
W 'staged set equals the declared thirteen, in count and in content'

$msg = "round 111: the first lane in this tree that moves a target hit point, wired end to end and gated before it was believed. NPC-HP-LINK-001 registers as HYP-PF-029 and composes eight runtime frames from one accepted chat input, alternating the vital hit carrier with the actor entry target carrier over a server held balance ladder of one hundred, one hundred, thirty seven, thirty seven, thirty seven, thirty seven, zero, zero, against the frozen Port Royal placement identity. The arithmetic and the link are ours and are labelled as ours, because the original server is unrecoverable and pretending otherwise is how a guess becomes a citation. Three tracked versions spend the whole version budget for this checkpoint: the composer, the runtime dispatch branch, and the app join that turns the scenario flag into that branch and that also corrected the scenario file, whose dispatch block still said the lane was unwired after the wiring had landed. The ledger append carries two more corrections that are not this lane: the HYP-PF-024 amendment recording that the GT-027 test has now actually run, and a provenance caveat on the attended negative of the twentieth, which is testimony and screenshots rather than a re-derivable receipt, and which is written down as the weaker kind of evidence it is. Whether the client renders the intermediate value on the target hit point bar is still undecidable from static analysis and is queued as an attended test; nothing in this commit claims it. Two new test modules arrive with the lane and no coverage row grade moves on any of it. The gitignore block exists because both tools this lane ships were invisible to git until it landed, which would have left the ledger citing files that a fresh clone cannot read, which is round eighty seven learned once more. Thirteen paths, asserted equal to the index in count and in content before a commit was attempted, because the subagent directory in this tree belongs to a cloud round and a blanket add would have swept it in. No branch created, moved or deleted, no pull request touched, no workflow file touched, no server booted, no client opened, no database written, no remote reached: the push is Panya's alone."
git --no-optional-locks commit -m "$msg" 2>&1 | Select-Object -First 3 | ForEach-Object { W "  commit> $_" }
$headAfter = (git --no-optional-locks rev-parse HEAD 2>&1)
if ($headAfter -cne $headBefore) {
    $committed = 1
    W "COMMIT CONFIRMED: HEAD $headBefore -> $headAfter"
    git --no-optional-locks show --stat --oneline -s HEAD 2>&1 | Select-Object -First 18 | ForEach-Object { W "  head> $_" }
} else {
    W "RED: commit returned but HEAD did not move (still $headBefore)"
    Finish178 -Code 37 -Verdict 'ABORT after commit: git commit returned but HEAD did not move, so nothing landed.' -Next 'Read the commit> lines.  The thirteen paths may still be staged; check git status before re-running job 178.'
}

# ---------- 10. acceptance: the COMMITTED BLOBS must carry the lane ----------
# Read from the COMMIT, never from the worktree.  The worktree is what this job
# already guarded in section 4; reading it again would only prove that section 4
# ran, and would say nothing at all about what git actually stored.
$blobOk = 0
$bScen = (git --no-optional-locks show 'HEAD:scenarios/npc_hp_link_hypothesis_target_sweep.json' 2>&1 | Out-String)
$bApp  = (git --no-optional-locks show 'HEAD:src/pirateforce_foundation/app.py' 2>&1 | Out-String)
$bIgn  = (git --no-optional-locks show 'HEAD:.gitignore' 2>&1 | Out-String)
$a1 = ([regex]::Matches($bScen, [regex]::Escape('"wired": true'))).Count
$a2 = ([regex]::Matches($bApp,  [regex]::Escape('npc_hp_link_hypothesis_scenario='))).Count
$a3 = ([regex]::Matches($bIgn,  [regex]::Escape('!/tools/verify_npc_hp_link_encoder.py'))).Count
W "acceptance on the committed blobs: scenarioWired=$a1(1) appJoin=$a2(1) ignoreEncoder=$a3(1)"
if ($a1 -ne 1 -or $a2 -ne 1 -or $a3 -ne 1) { $blobOk = 1; W 'RED: a committed blob does not carry the lane' }
$blobNonAscii = 0
foreach ($t in @($bScen, $bApp, $bIgn)) {
    foreach ($b in [System.Text.Encoding]::UTF8.GetBytes($t)) { if ($b -gt 127) { $blobNonAscii++ } }
}
W "committed blob non-ascii bytes (3 files) = $blobNonAscii (expect 0)"
if ($blobNonAscii -ne 0) { $blobOk = 1 }
# The commit itself must name thirteen files and no more.
$commitFiles = @(git --no-optional-locks show --name-only --pretty=format: HEAD 2>&1 |
                 ForEach-Object { ([string]$_).Trim() } | Where-Object { $_ -ne '' })
W "files named by the commit = $($commitFiles.Count) (expect 13)"
$commitFiles | ForEach-Object { W "  inCommit> $_" }
if ($commitFiles.Count -ne 13) { $blobOk = 1; W 'RED: the commit does not name exactly thirteen files' }
$claudeInCommit = @($commitFiles | Where-Object { $_ -clike '.claude*' })
if ($claudeInCommit.Count -ne 0) { $blobOk = 1; W 'RED: the commit names something under .claude' }

W '--- post-commit worktree state (expect only .claude/ left dirty) ---'
git --no-optional-locks status --short 2>&1 | Select-Object -First 8 | ForEach-Object { W "  st> $_" }
$shaEnd = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha END = $shaEnd (expect unchanged)"
if ($shaEnd -cne $shaBefore) { W 'RED: the canonical database moved during this job'; $canonGuard = 1 }
Remove-Item -LiteralPath $pytestLog -Force -ErrorAction SilentlyContinue

# ---------- 11. release, and exit on the truth ----------
# A green battery and a landed commit whose blob does not carry the lane is not a
# success, and this job will not report one.  The most expensive recurring bug in
# this project is an exit that reports instead of acting; exit code 51 is this
# file refusing to be that.
if ($blobOk -ne 0) {
    Finish178 -Code 51 -Verdict 'COMMITTED, but the acceptance check on the committed blobs is RED - do not trust this commit until a human has looked at it.' -Next 'Read the acceptance lines above.  The commit EXISTS and was NOT pushed; decide whether to amend or revert it by hand before anything else happens.'
}
Finish178 -Code 0 -Verdict 'GREEN battery, thirteen paths committed, committed blobs carry the lane.' -Next 'PANYA PUSHES - this job never touches a remote.  Nothing here concerns PR #1/#2 or merge-claude-pr.yml; those remain entirely her decision.  The attended question the lane does not answer is still open: whether the client renders the intermediate target hit-point value.'

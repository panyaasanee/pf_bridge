# Job 146 - round 91 gate and commit: the RETRY of job 145.
#
# WHY THIS EXISTS.  Job 145 ran every guard of the round 90 lane green except
# one and therefore committed nothing, exactly as designed.  The red was a
# census guard in tools/pf_runtimeres_actor_entry_static.py: it pins how many
# call sites in src/ send the VitalData carrier, it said 13, and the new
# damage encoder is the fourteenth.  Round 90 repaired it in the tree - the
# guard is re-pinned at 14 and the report carries ERRATUM 2 saying what moved
# and, more usefully, what did not - and was then cut off before it could
# re-run the gate.  Round 91 read the tree, re-ran the three failing tests
# against the real client image in the sandbox until they were green
# (tests.test_runtimeres_actor_entry_static: 21 tests OK, plus
# test_hp_death_erratum + test_hypothesis_ledger + test_foundation_legacy_seam:
# 48 tests OK, python3 unittest - pip is blocked in the sandbox so pytest can
# only run here), and placed this job.  The lane itself is unchanged: not one
# line of it was written by the round that is committing it.
#
# DIFFERENCES FROM JOB 145, and there are only three:
#   * two more paths are staged - tools/pf_runtimeres_actor_entry_static.py and
#     reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md - so the staged
#     count is 16 rather than 14, and both are already tracked files;
#   * the dirty worktree is expected at 15 lines rather than 12;
#   * the commit message names both rounds and carries one closing paragraph
#     about the census re-pin.
# Every guard, every ordering and every refusal below is byte identical to 145.
#
# WHAT THIS COMMITS.  One lane, fourteen paths, two checkpoints.  The lane puts
# a DAMAGE NUMBER on the wire for the first time in this project, and the
# number is computed by a formula THIS REPOSITORY WROTE.  Round 83 proved the
# client computes nothing: no damage formula, no scaling, and it never
# subtracts damage from hit points, so the figure a player sees is exactly the
# signed i32 the server placed at hit entry +0x08, passed through abs().  There
# was therefore no original formula inside the image to recover, and the owner
# approved designing one on 2026-08-19 11:45 within a scope of one signed
# integer and one flag word per target.
#
# THE CARRIER.  CHitResult wire id 0x16F7, VERSION BYTE 0, as the single
# element of the VitalData collection - BASE change mask 0x02, object at
# this+0x18.  That is NOT the actor-entry collection HYP-PF-023 rides (DERIVED
# mask 0x02, object this+0x1C) despite the matching bit number; two rounds had
# conflated them and the round 90 static pass separates them byte by byte.
#
# THE TWO UNKNOWNS THAT BLOCKED THIS LANE ARE CLOSED, from the bytes.  The
# version byte is an instance field at obj+0x10, compared by the collection
# reader at 0x5F3EFC (3A 4E 10) and stored as zero by the CHitResult ctor at
# 0x74F979 (88 46 10 after 33 C0), cross-checked against SelectActorVital 10,
# UpdateNPCAppearVital 0 and CreateActorVital 8.  Construction by id goes
# through a general red-black tree lookup on a u16 key at 0x731380, not an
# allowlist, and CHitResult's prototype is registered at 0x755048.
#
# FOUR FRAMES: HIT_WEAK -63 flags 0x0001, HIT_STRONG -379 flags 0x0001, MISS 0
# flags 0x0000, HIT_REACTION -63 flags 0x0009.  84-byte PC and 95-byte frame
# each.  MISS is the experiment's control and the validator refuses a sweep
# without one.  A positive damage value is refused outright because heal /
# absorb semantics are unknown, and INT32_MIN is refused separately because
# abs() would return it unchanged and print a minus sign.
#
# SEAM IS MANDATORY THIS ROUND: .gitignore is staged.  Four new paths needed
# allowlisting (both new tools, the report, and the two design documents the
# new ledger entry cites as evidence) - the round 87 lesson, applied before the
# fact this time rather than after.
#
# LEDGER: entry 31 is ADDED (HYP-PF-024, active, production_allowed false, two
# of three versions spent on arrival).  No existing entry index moved.
#
# SANDBOX PRE-RUN (python3 3.10, unittest - pip is BLOCKED in this session's
# sandbox, so pytest could not be installed there; the gate below is the real
# test):  test_damage_model_hypothesis 90 tests OK, test_damage_model_dispatch
# 38 tests OK, test_stats_progression_hypothesis 42 tests OK (its containment
# test is why the encoder copies two constants instead of importing that lane),
# seam 22 tests OK, plus hypothesis_ledger, hp_death_*, runtimeres_death_*,
# functional_coverage: all OK.  verify_damage_model_encoder 322 guards PASS.
# pf_damage_model_headless_replay 136 guards PASS.  verify_hypothesis_ledger
# PASS entries=31.  coverage OPEN DOMAINS 8, unchanged - this round flips no row.
#
# THIS JOB RELEASES LOCK_GIT.txt ITSELF at the end, whatever the outcome.  Round
# 89's flag sat HELD for 31 minutes after its commit finished because the chief
# round that placed the job was cut off before it could come back and write the
# release line.  A job that knows whether it committed is the right writer of
# that line.
#
# ASCII ONLY.  Quote all paths that contain spaces.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\146_round91_gate_commit.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 91 GATE AND COMMIT - RETRY OF JOB 145 - HYP-PF-024 + census re-pin  $stamp ===" | Out-File -FilePath $log -Encoding utf8

Set-Location -LiteralPath $main
$headBefore = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD before = $headBefore  (expect ee241db...)"

# ---------- 1. index.lock, checked first ----------
$lockPath = Join-Path $main '.git\index.lock'
$lockCleared = 0
if (Test-Path -LiteralPath $lockPath) {
    $lk = Get-Item -LiteralPath $lockPath
    $ageMin = [math]::Round(((Get-Date) - $lk.LastWriteTime).TotalMinutes, 1)
    W "index.lock present: size=$($lk.Length) bytes  mtime=$($lk.LastWriteTime)  age=${ageMin} min"
    $gitProcs = @(Get-Process -Name git -ErrorAction SilentlyContinue)
    W "running git processes = $($gitProcs.Count)"
    if ($lk.Length -ne 0)      { W 'ABORT: index.lock is NOT empty - may hold a partial index write. Do not delete.'; exit 30 }
    if ($gitProcs.Count -gt 0) { W 'ABORT: a git process is running - the lock may be live.'; exit 31 }
    if ($ageMin -lt 10)        { W 'ABORT: index.lock younger than 10 minutes - too fresh to call stale.'; exit 32 }
    Remove-Item -LiteralPath $lockPath -Force
    if (Test-Path -LiteralPath $lockPath) { W 'ABORT: could not remove index.lock'; exit 33 }
    W 'stale index.lock removed'
    $lockCleared = 1
} else {
    W 'no index.lock present - nothing to clear'
}

# ---------- 2. worktree ----------
$dirty = @(git --no-optional-locks status --porcelain 2>&1)
W "worktree dirty paths = $($dirty.Count) (expect 15: 7 modified + 8 untracked, drafts/ counts as one line until added)"
$dirty | ForEach-Object { W "  st> $_" }

# ---------- 3. canonical DB, read from CANON_SHA.txt, never hardcoded ----------
# NOTE: the attended session may be running a game test on a COPY while this
# runs.  If it moved the canonical file this job aborts here by design.
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$shaBefore = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
$canonExpect = (Get-Content -LiteralPath (Join-Path $bridge 'CANON_SHA.txt') -Raw).Trim()
W "canonical sha BEFORE = $shaBefore"
if ($shaBefore -ne $canonExpect) { W "ABORT: canonical sha != CANON_SHA.txt ($canonExpect)"; exit 13 }
W 'canonical matches CANON_SHA.txt'

# ---------- 4. the lane's own two tools, first ----------
W '--- verify_damage_model_encoder (expect 322 guards PASS, exit 0) ---'
py -3 (Join-Path $main 'tools\verify_damage_model_encoder.py') 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  dmenc> $_" }
$vDmEnc = $LASTEXITCODE
W '--- verify_damage_model_encoder --binary (explicit image path) ---'
py -3 (Join-Path $main 'tools\verify_damage_model_encoder.py') --binary '..\GameClient\GameClient.local.bin' 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  dmencbin> $_" }
$vDmEncBin = $LASTEXITCODE
W '--- pf_damage_model_headless_replay (expect 136 guards PASS, exit 0) ---'
py -3 (Join-Path $main 'tools\pf_damage_model_headless_replay.py') 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  dmreplay> $_" }
$vDmReplay = $LASTEXITCODE

# ---------- 5. the standing verifier set ----------
W '--- standing verifiers ---'
py -3 (Join-Path $main 'tools\verify_hp_death_encoder.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  hpenc> $_" }
$vHpEnc = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_damage_hit_result_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  damage> $_" }
$vDamage = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_runtimeres_death_encoder_static.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  deathenc> $_" }
$vDeathEnc = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_runtimeres_actor_entry_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  runtimeres> $_" }
$vRuntimeRes = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_hp_death_respawn_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  hpstatic> $_" }
$vHpStatic = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_stats_progression_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  stats020> $_" }
$vStats = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_multiplayer_readiness_audit.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  mpaudit> $_" }
$vMpAudit = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_capture_corpus.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  corpus> $_" }
$vCorpus = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_vital_thunk_census_static.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  census> $_" }
$vCensus = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_hp_death002_headless_replay.py') --profile dying_hold 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  hlhold> $_" }
$vHlHold = $LASTEXITCODE

# ---------- 6. the suite ----------
W '--- pytest full suite ---'
py -3 -m pytest tests -q 2>&1 | Select-Object -Last 8 | ForEach-Object { W "  py> $_" }
$pytestExit = $LASTEXITCODE

W '--- seam (MANDATORY: .gitignore is staged) ---'
py -3 -m pytest (Join-Path $main 'tests\test_foundation_legacy_seam.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  seam> $_" }
$seamExit = $LASTEXITCODE
W '--- ledger (expect PASS entries=31 - APPENDED this round) ---'
py -3 (Join-Path $main 'tools\verify_hypothesis_ledger.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  ledger> $_" }
$ledgerExit = $LASTEXITCODE
W '--- coverage (expect OPEN DOMAINS 8 UNCHANGED - this round flips no row) ---'
py -3 (Join-Path $main 'tools\verify_functional_coverage.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  cov> $_" }
$covExit = $LASTEXITCODE

$shaAfter = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
if ($shaAfter -cne $shaBefore) { W 'RED: CANONICAL DB MOVED'; $canonGuard = 1 } else { W 'canonical guard OK'; $canonGuard = 0 }

$v141Dirty = (git --no-optional-locks status --short -- 'current/pf_login_game_server_v141.py' 2>&1 | Out-String).Trim()
if ($v141Dirty) { W "RED: v141 SNAPSHOT IS DIRTY -> $v141Dirty"; $v141Guard = 1 } else { W 'v141 guard OK'; $v141Guard = 0 }

git --no-optional-locks diff --check 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  git> $_" }
$diffExit = $LASTEXITCODE

W '--- check-ignore on the eight new paths (expect NOT ignored) ---'
$newPaths = @(
    'drafts/DAMAGE_MODEL_LANE1_DESIGN_20260819.md',
    'drafts/DAMAGE_MODEL_UNKNOWNS_R90_STATIC.md',
    'reports/PF_DAMAGE_ENCODER001_OUR_OWN_HIT_RESULT_20260819.md',
    'scenarios/damage_model_hypothesis_hit_sweep.json',
    'src/pirateforce_foundation/damage_model_hypothesis.py',
    'tests/test_damage_model_dispatch.py',
    'tests/test_damage_model_hypothesis.py',
    'tools/pf_damage_model_headless_replay.py',
    'tools/verify_damage_model_encoder.py'
)
$ignoreGuard = 0
foreach ($p in $newPaths) {
    git --no-optional-locks check-ignore -q -- "$p"
    if ($LASTEXITCODE -eq 0) { W "  RED: $p IS IGNORED"; $ignoreGuard = 1 } else { W "  ok (tracked): $p" }
}

$allGreen = ($vDmEnc -eq 0) -and ($vDmEncBin -eq 0) -and ($vDmReplay -eq 0) -and `
            ($vHpEnc -eq 0) -and ($vDamage -eq 0) -and ($vDeathEnc -eq 0) -and `
            ($vRuntimeRes -eq 0) -and ($vHpStatic -eq 0) -and ($vStats -eq 0) -and `
            ($vMpAudit -eq 0) -and ($vCorpus -eq 0) -and ($vCensus -eq 0) -and ($vHlHold -eq 0) -and `
            ($pytestExit -eq 0) -and ($canonGuard -eq 0) -and ($seamExit -eq 0) -and `
            ($ledgerExit -eq 0) -and ($covExit -eq 0) -and ($v141Guard -eq 0) -and `
            ($diffExit -eq 0) -and ($ignoreGuard -eq 0)
W "ALL GREEN = $allGreen"

$committed = 0
$headAfter = $headBefore
if ($allGreen) {
    W '--- GUARDED COMMIT: read-tree HEAD, then stage ONLY the sixteen round 90/91 paths ---'
    $rt = (git --no-optional-locks read-tree HEAD 2>&1 | Out-String).Trim()
    if ($rt) { W "  read-tree> $rt" }
    if ($LASTEXITCODE -ne 0) { W 'ABORT: read-tree failed - not staging anything'; exit 34 }

    $paths = @(
        '.gitignore',
        'docs/HYPOTHESIS_LEDGER.json',
        'drafts/DAMAGE_MODEL_LANE1_DESIGN_20260819.md',
        'drafts/DAMAGE_MODEL_UNKNOWNS_R90_STATIC.md',
        'reports/PF_DAMAGE_ENCODER001_OUR_OWN_HIT_RESULT_20260819.md',
        'reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md',
        'scenarios/damage_model_hypothesis_hit_sweep.json',
        'src/pirateforce_foundation/app.py',
        'src/pirateforce_foundation/damage_model_hypothesis.py',
        'src/pirateforce_foundation/runtime.py',
        'tests/test_damage_model_dispatch.py',
        'tests/test_damage_model_hypothesis.py',
        'tools/pf_damage_model_headless_replay.py',
        'tools/pf_runtimeres_actor_entry_static.py',
        'tools/verify_damage_model_encoder.py',
        'tools/verify_hypothesis_ledger.py'
    )
    $addFailed = 0
    foreach ($p in $paths) {
        # git add writes an LF/CRLF warning to stderr; PowerShell renders that as a
        # NativeCommandError.  It is not an error.  Only $LASTEXITCODE decides.
        $o = (git --no-optional-locks add -- "$p" 2>&1 | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) { W "  RED add> $p :: $o"; $addFailed = 1 }
        elseif ($o) { W "  add(warn)> $p :: $o" }
    }
    if ($addFailed -eq 1) { W 'ABORT: at least one add failed - refusing to commit a partial set'; exit 35 }
    W "all $($paths.Count) paths added cleanly"

    W '--- staged summary (expect 16 paths, NO deletions) ---'
    git --no-optional-locks diff --cached --stat 2>&1 | Select-Object -Last 24 | ForEach-Object { W "  staged> $_" }
    $stagedCount = @(git --no-optional-locks diff --cached --name-only 2>&1).Count
    W "staged path count = $stagedCount (expect 16)"
    $delLines = (git --no-optional-locks diff --cached --name-status 2>&1 | Select-String -Pattern '^D')
    if ($delLines) {
        W 'RED: staged set contains DELETIONS - aborting commit'; $delLines | ForEach-Object { W "  DEL> $_" }
    } elseif ($stagedCount -ne 16) {
        W "RED: staged path count is $stagedCount, expected 16 - aborting commit"
    } else {
        $msg = 'round 90, gated and landed by round 91: put a damage number on the wire, and write down whose number it is. The client computes nothing. An earlier round proved that byte by byte: it carries no damage formula, applies no scaling and never subtracts damage from hit points, so the figure a player sees floating over a target is exactly the signed thirty two bit integer the server placed in the hit entry, passed through absolute value and printed with a plain integer format, with no multiply or divide anywhere on the path. That is a negative worth more than the search that found it, because it means there was never a formula inside the client to recover. The original server is closed, was never published, and cannot be read. So the owner approved designing one instead, inside a scope she set herself: one signed integer and one flag word per target. Everything this round adds sits inside that scope, and every file it touches says out loud that the numbers are ours. Two unknowns had blocked the encoder since the design was written, and both are closed from the bytes rather than assumed. The first is the version byte the collection reader compares before it will accept an element at all. It is not a vtable slot, which is what an earlier reading had assumed and which is why that reading landed on the wrong class entirely: the wire classes have nine slots and their tables sit adjacent, so an offset past the end of one is the start of the next. It is an instance field written by the constructor, and the constructor for this class zeroes a register and stores it, so the pinned value is zero. The method was required to reproduce four classes whose versions this repository already ships before it was allowed to answer a new one, and all four agree with what the frozen snapshot already sends. The second unknown was whether the collection can construct this class at all. It can, and there is no list to be excluded from: construction by identifier goes through a general tree lookup on a sixteen bit key, with no switch and no jump table on the path, the prototype is registered like every other, and the precondition the dispatcher checks before calling the handler is a stub that returns true unconditionally. The carrier needed separating from its neighbour before anything could be composed, because two rounds had conflated them. The collection this lane rides is selected by the base change mask and lives at one offset; the actor entry collection the death lane rides is selected by the derived change mask and lives at another. They share a bit number and nothing else: different mask byte, different reader, different element shape. The base serializer is called first, which is why the wire order is base mask, collection, derived mask, and which is also why the frozen helper that composes these frames has been byte correct all along. The sweep is four frames against the player own actor, which is the only identity this lane can be sure the client already knows. Two of them carry numbers a tester can predict before they appear, deliberately not round and not squares so that a different figure on screen means the client scales after all rather than meaning nothing. One of them is a control that carries no number and no reaction, and the validator refuses to return a sweep that does not contain it, because a sweep where every frame shows something cannot distinguish the client reading our bytes from the client drawing its own. The fourth repeats the first number with one more flag bit set, so the two can be compared side by side. The sign is the meaning and it is the easiest thing here to get backwards: the field is compared signed at four sites, negative is the took damage side, and the player still sees a positive number because the display path takes an absolute value. A positive value is therefore refused outright, because what a non negative value means, heal or absorb or nothing at all, is genuinely unknown, and unknown means we do not send it. The most negative representable integer is refused as its own separate rejection, because the absolute value the client computes returns it unchanged and the format would then print a minus sign, on the one path designed never to show one. The flag word is an allow list of whole values with a second mask check behind it, so a new bit cannot arrive by arithmetic. The bit that opens the reaction block is chosen deliberately rather than left at zero, because the number itself is drawn by a second pass that does not read it. The bit that makes the client play a knocked down animation instead of showing the figure is refused on every frame of this sweep. And the bit that is tested somewhere in the handler but does something nobody here can name is refused precisely because it is tested and unexplained. No bit is given a name this project cannot prove; the popular names for these bits are inferences from a texture table and they are not adopted. The four header fields whose meaning is unknown are pinned at zero, and zero was traced branch by branch to be inert on every path that was read rather than assumed to be safe. That is written down as what it is: a statement about the branches that were read, not a claim to know what those fields are for. Proof stops where the evidence stops. An offline verifier holds three hundred and twenty two guards against the read only client image, and the first thirty nine of them reproduce the earlier round published answers and stop the tool without asserting anything new if they fail. A headless replay proves the same four frames leave the real dispatcher, in order, with the pinned labels and delays, against the session own actor, on a throwaway database, read back by a tag walker written inside the tool that never calls the encoder own decoder. Twenty five named refusals are each proven to produce no bytes at all rather than merely to raise. Six traps prove the verifier can go red and forty five prove the validator can. What none of it does is watch a screen: no client has ever been shown one byte of this profile, and whether the number renders at all is the next attended test. One risk behind that test is named rather than smoothed over, because static reading cannot settle it: a gate on the display path loads a singleton and returns true when that pointer is null, and a true there suppresses the figure no matter what we send. If the attended run shows nothing, that is the first place to look and not the encoder. This round also fixed three defects in its own first draft rather than filing them. Eight offset constants were each one byte early because they assumed a mask byte with no tag in front of it, and nothing read them, so nothing went red: they are corrected and made load bearing, so the next drift is a failing test rather than a comment that quietly disagrees with the bytes. Two byte site numbers in the scenario file pointed at addresses that are not the sites they name, and they agreed with the module, which is exactly why the exact tree loader accepted the file: two readers copying the same wrong number agree with each other. And one declared refusal is unreachable from any external input, which is written down here rather than left for a reader to discover. The encoder also copies two constants from the progression lane instead of importing it, because a containment test over there requires that exactly two modules mention that lane at all, and a drift check belongs in a test while a dependency does not belong in an encoder. Four files needed adding to version control alongside the code, and they are added rather than the references to them dropped: both new tools and the two design documents the new entry cites as evidence, one of which carries the byte tables that answer the version byte and the construction path and which nothing else in the repository records. That is the same failure two earlier rounds found and fixed the same way. Nothing in this round boots a server, opens a client, writes to a database, flips a coverage row, ties any of this to hit points, or touches the frozen delivered snapshot. One more change rides along, and it is the reason this is the second attempt rather than the first. A census guard pins how many places in our own source send the vital data carrier. It said thirteen. The encoder above is the fourteenth, so the first gate run went red on that guard and refused to commit anything, which is the guard doing its job rather than a defect. The number is re-pinned at fourteen rather than widened into a range, because a census that quietly accepts a larger number has stopped being a census, and the report that publishes it carries an appended erratum rather than a silent edit. The half of that erratum worth reading is what did not move: every actor entry count in that file is unchanged, because the damage lane rides the base change mask and the death lane rides the derived one, and those two share a bit number and nothing else. A reader who sees the matching bit and assumes a shared carrier gets this wrong, and two rounds already did. The round that wrote the lane was cut off while repairing that guard, with the fix already in the tree and the gate not yet re-run. The round that follows it read the tree rather than rewriting it, re-ran the failing tests against the real client image until they were green, and placed the job that produced this commit. Not one line of the lane above was written by the round that committed it, and this sentence exists so that the authorship is in the record rather than in a bridge file that will be archived'
        git --no-optional-locks commit -m "$msg" 2>&1 | ForEach-Object { W "  commit> $_" }
        $headAfter = (git --no-optional-locks rev-parse HEAD 2>&1)
        # Success is HEAD moving, not this line being reached.
        if ($headAfter -ne $headBefore) {
            $committed = 1
            W "COMMIT CONFIRMED: HEAD $headBefore -> $headAfter"
            git --no-optional-locks show --stat --oneline -s HEAD 2>&1 | ForEach-Object { W "  head> $_" }
            git --no-optional-locks diff --stat HEAD~1 HEAD 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  delta> $_" }
        } else {
            W "RED: git commit returned but HEAD DID NOT MOVE (still $headBefore) - treat as NOT committed"
        }
    }
} else {
    W 'NOT COMMITTING - a guard is red. Nothing staged, worktree left exactly as found.'
}

W '--- post-commit worktree state (expect only the ignored multiplayer draft) ---'
git --no-optional-locks status --short 2>&1 | Select-Object -First 25 | ForEach-Object { W "  st> $_" }
$shaEnd = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha END = $shaEnd (expect unchanged)"
if (Test-Path -LiteralPath $lockPath) { W 'WARN: an index.lock exists again at the end of this job' }

# ---------- 7. release LOCK_GIT.txt, whatever happened ----------
# Round 89's flag stayed HELD for half an hour after its commit landed, because
# the round that placed the job was cut off before it could write the release.
# This job knows the outcome, so this job writes it.
$lockGit = Join-Path $bridge 'LOCK_GIT.txt'
$headShort = (git --no-optional-locks rev-parse --short HEAD 2>&1)
$rel = @(
    "RELEASED: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
    "BY: job 146 (chief round 91) - released by the job itself, not by the round that placed it",
    "done: RETRY of job 145 - gate + commit of DAMAGE-ENCODER-001 / DAMAGE-DISPATCH-001 (HYP-PF-024)",
    "      plus the round 90 census re-pin 13 -> 14 that made job 145 red.  16 paths",
    "      allGreen=$allGreen committed=$committed",
    "      dmenc=$vDmEnc dmencbin=$vDmEncBin dmreplay=$vDmReplay pytest=$pytestExit seam=$seamExit ledger=$ledgerExit coverage=$covExit",
    "      canonGuard=$canonGuard v141Guard=$v141Guard ignoreGuard=$ignoreGuard",
    "head: $headShort  (was $headBefore)",
    "next: chief round 91 is building the two-frame variant of HYP-PF-023 (SPAWN + DYING_LATCH,",
    "      no DEATH_TASK) - do NOT flip the HYP-PF-023 matrix row before it runs.  GT-024 stays queued",
    "warn: drafts/MULTIPLAYER_CHUNK2_VISIBILITY_DESIGN_R90.md is deliberately NOT committed",
    "      and stays gitignored until the multiplayer chunk 2 lane is actually opened",
    "",
    "===== flag scope (Panya 2026-08-19 ~11:45) =====",
    "git commit / gate run on the Windows bridge; git index and staging;",
    "edits to .gitignore / manifest / coverage that require the seam test.",
    "NOT covered: writing files into the worktree, reading git log/status,",
    "booting the server or opening the game (that is LOCK_GAME.txt).",
    "Hold only while a gate/commit job is actually running; release immediately after.",
    "Takeover rule: same as LOCK_GAME.txt - age >= 20 min AND silent in all three channels."
)
$rel | Out-File -FilePath $lockGit -Encoding utf8
W "LOCK_GIT.txt released by the job (committed=$committed head=$headShort)"

W '=== 146 SUMMARY ==='
@(
    "lockCleared=$lockCleared",
    "dmenc=$vDmEnc dmencbin=$vDmEncBin dmreplay=$vDmReplay",
    "hpenc=$vHpEnc damage=$vDamage deathenc=$vDeathEnc runtimeres=$vRuntimeRes",
    "hpstatic=$vHpStatic stats=$vStats mpaudit=$vMpAudit corpus=$vCorpus census=$vCensus hlhold=$vHlHold",
    "pytest=$pytestExit seam=$seamExit ledger=$ledgerExit coverage=$covExit",
    "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit ignoreGuard=$ignoreGuard",
    "allGreen=$allGreen committed=$committed",
    "head=$headShort"
) | ForEach-Object { W $_ }
W '=== 146 DONE ==='

# Job 147 - round 91 gate and commit: RUNTIMERES-LATCHONLY-001, the two-frame
# tie-breaker profile of HYP-PF-023.
#
# WHAT THIS COMMITS.  One lane, eleven paths, one checkpoint, one ledger
# AMENDMENT (no entry added, count stays 31, no entry index moves).
#
# WHY THE LANE EXISTS.  GT-022 ran three times on a real client and produced a
# real corpse: the probe NPC went from standing to lying flat inside the sweep
# window and stayed there past t+12, which the owner walked over to and
# photographed herself.  What it could NOT answer is WHICH FRAME did that.
# DYING_LATCH lands at t+6 and DEATH_TASK at t+12; the run designed to separate
# them photographed at roughly t+10.5 to t+11.5 with the pose already present,
# which points hard at the latch, but the margin is about one second and capture
# latency was never instrumented.  That is an argument about an unmeasured
# clock.  A sweep that STOPS after the latch removes the clock from the
# question entirely, and it is the cheapest experiment that can settle it.
#
# WHAT IS LOAD-BEARING.  The two frames the new profile sends are the three
# frame sweep's first two BYTE FOR BYTE, structurally rather than incidentally:
# the profile's step rows are a SLICE of the same plan tuple, both profiles
# resolve step i to the same row object, and the identity is asserted three
# times independently (encoder, verifier, replay) with == on the bytes.
#
# THE VALIDATOR IS STRICTER FOR THE NEW PROFILE, NOT LOOSER: no frame may
# satisfy vt+0x3C, the DEATH_TASK label may not appear in its step order, and
# the sweep must END on a frame satisfying vt+0x40.  Each profile also carries
# its own lethal unlock token compared by identity, so one profile's key opens
# no byte of the other.
#
# LEDGER: HYP-PF-023 is AMENDED and RUNTIMERES-LATCHONLY-001 is tracked as the
# THIRD of three versions, which FILLS the budget.  It is counted as a version
# although every byte it sends is a subset of the pinned frames, because it
# lets the lane end a session in a state no earlier version could produce.
# CANONICAL_CONTENT_SHA256 in tools/verify_hypothesis_ledger.py moves with it,
# which is why that tool is in the staged set.
#
# NO .gitignore CHANGE THIS ROUND: the new scenario file is already visible to
# version control (scenarios/** is un-ignored), confirmed with check-ignore
# before this job was written, so the seam test is not mandatory here.  It runs
# anyway, because it is cheap and it is the check that catches an evidence file
# that a fresh clone would not contain.
#
# SANDBOX PRE-RUN (python3 3.10, unittest - pip is BLOCKED in this session's
# sandbox so pytest cannot be installed there; the gate below is the real test):
#   verify_hypothesis_ledger PASS entries=31
#   pf_runtimeres_death_encoder_static      138 guards, 0 failures (was 88)
#   pf_runtimeres_death_headless_replay      64 guards (default, UNCHANGED)
#   pf_runtimeres_death_headless_replay --profile dying_latch_only  68 guards
#   test_runtimeres_death_hypothesis 49 tests OK (was 39)
#   test_runtimeres_death_dispatch   27 tests OK (was 25)
#   plus 321 tests across every module that imports make_state_class: OK
#   canonical DB sha unchanged across all of it, checked before and after.
#
# THIS JOB RELEASES LOCK_GIT.txt ITSELF at the end, whatever the outcome.
#
# ASCII ONLY.  Quote all paths that contain spaces.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\147_round91_latchonly.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 91 GATE AND COMMIT - RUNTIMERES-LATCHONLY-001 (HYP-PF-023 v3/3)  $stamp ===" | Out-File -FilePath $log -Encoding utf8

Set-Location -LiteralPath $main
$headBefore = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD before = $headBefore  (expect d4ed4d4...)"

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
W "worktree dirty paths = $($dirty.Count) (expect 11: 10 modified + 1 untracked)"
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
W '--- pf_runtimeres_death_encoder_static (expect 138 guards, 0 failures, exit 0 - was 88) ---'
py -3 (Join-Path $main 'tools\pf_runtimeres_death_encoder_static.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  latchver> $_" }
$vLatchVer = $LASTEXITCODE
W '--- pf_runtimeres_death_headless_replay DEFAULT (expect 64 guards, UNCHANGED, exit 0) ---'
py -3 (Join-Path $main 'tools\pf_runtimeres_death_headless_replay.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  replay3> $_" }
$vReplay3 = $LASTEXITCODE
W '--- pf_runtimeres_death_headless_replay --profile dying_latch_only (expect 68 guards, exit 0) ---'
py -3 (Join-Path $main 'tools\pf_runtimeres_death_headless_replay.py') --profile dying_latch_only 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  replay2> $_" }
$vReplay2 = $LASTEXITCODE
W '--- pf_runtimeres_death_headless_replay --profile nonsense (expect exit 2, no guards) ---'
py -3 (Join-Path $main 'tools\pf_runtimeres_death_headless_replay.py') --profile nonsense 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  replayx> $_" }
$vReplayX = $LASTEXITCODE
if ($vReplayX -ne 2) { W "RED: unknown profile returned $vReplayX, expected 2"; $vReplayBad = 1 } else { $vReplayBad = 0 }
W '--- verify_damage_model_encoder (standing, expect 322 guards PASS, exit 0) ---'
py -3 (Join-Path $main 'tools\verify_damage_model_encoder.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  dmenc> $_" }
$vDmEnc = $LASTEXITCODE
W '--- pf_damage_model_headless_replay (standing, expect 136 guards PASS, exit 0) ---'
py -3 (Join-Path $main 'tools\pf_damage_model_headless_replay.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  dmreplay> $_" }
$vDmReplay = $LASTEXITCODE
$vDmEncBin = 0

# ---------- 5. the standing verifier set ----------
W '--- standing verifiers ---'
py -3 (Join-Path $main 'tools\verify_hp_death_encoder.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  hpenc> $_" }
$vHpEnc = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_damage_hit_result_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  damage> $_" }
$vDamage = $LASTEXITCODE
$vDeathEnc = 0   # run above as latchver, not run twice
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

W '--- seam (not mandatory this round - no .gitignore change - run anyway) ---'
py -3 -m pytest (Join-Path $main 'tests\test_foundation_legacy_seam.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  seam> $_" }
$seamExit = $LASTEXITCODE
W '--- ledger (expect PASS entries=31 - AMENDED this round, count unchanged) ---'
py -3 (Join-Path $main 'tools\verify_hypothesis_ledger.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  ledger> $_" }
$ledgerExit = $LASTEXITCODE
W '--- coverage (expect OPEN DOMAINS 8 UNCHANGED - HYP-PF-023 row stays put until GT-025) ---'
py -3 (Join-Path $main 'tools\verify_functional_coverage.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  cov> $_" }
$covExit = $LASTEXITCODE

$shaAfter = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
if ($shaAfter -cne $shaBefore) { W 'RED: CANONICAL DB MOVED'; $canonGuard = 1 } else { W 'canonical guard OK'; $canonGuard = 0 }

$v141Dirty = (git --no-optional-locks status --short -- 'current/pf_login_game_server_v141.py' 2>&1 | Out-String).Trim()
if ($v141Dirty) { W "RED: v141 SNAPSHOT IS DIRTY -> $v141Dirty"; $v141Guard = 1 } else { W 'v141 guard OK'; $v141Guard = 0 }

git --no-optional-locks diff --check 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  git> $_" }
$diffExit = $LASTEXITCODE

W '--- check-ignore on the one new path (expect NOT ignored) ---'
$newPaths = @(
    'scenarios/runtimeres_death_hypothesis_dying_latch_only.json'
)
$ignoreGuard = 0
foreach ($p in $newPaths) {
    git --no-optional-locks check-ignore -q -- "$p"
    if ($LASTEXITCODE -eq 0) { W "  RED: $p IS IGNORED"; $ignoreGuard = 1 } else { W "  ok (tracked): $p" }
}

$allGreen = ($vLatchVer -eq 0) -and ($vReplay3 -eq 0) -and ($vReplay2 -eq 0) -and `
            ($vReplayBad -eq 0) -and `
            ($vDmEnc -eq 0) -and ($vDmEncBin -eq 0) -and ($vDmReplay -eq 0) -and `
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
    W '--- GUARDED COMMIT: read-tree HEAD, then stage ONLY the eleven round 91 paths ---'
    $rt = (git --no-optional-locks read-tree HEAD 2>&1 | Out-String).Trim()
    if ($rt) { W "  read-tree> $rt" }
    if ($LASTEXITCODE -ne 0) { W 'ABORT: read-tree failed - not staging anything'; exit 34 }

    $paths = @(
        'docs/HYPOTHESIS_LEDGER.json',
        'reports/PF_RUNTIMERES_ENCODER001_SPAWN_THEN_KILL_20260819.md',
        'scenarios/runtimeres_death_hypothesis_dying_latch_only.json',
        'scenarios/runtimeres_death_hypothesis_spawn_then_kill.json',
        'src/pirateforce_foundation/runtime.py',
        'src/pirateforce_foundation/runtimeres_death_hypothesis.py',
        'tests/test_runtimeres_death_dispatch.py',
        'tests/test_runtimeres_death_hypothesis.py',
        'tools/pf_runtimeres_death_encoder_static.py',
        'tools/pf_runtimeres_death_headless_replay.py',
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

    W '--- staged summary (expect 11 paths, NO deletions) ---'
    git --no-optional-locks diff --cached --stat 2>&1 | Select-Object -Last 24 | ForEach-Object { W "  staged> $_" }
    $stagedCount = @(git --no-optional-locks diff --cached --name-only 2>&1).Count
    W "staged path count = $stagedCount (expect 11)"
    $delLines = (git --no-optional-locks diff --cached --name-status 2>&1 | Select-String -Pattern '^D')
    if ($delLines) {
        W 'RED: staged set contains DELETIONS - aborting commit'; $delLines | ForEach-Object { W "  DEL> $_" }
    } elseif ($stagedCount -ne 11) {
        W "RED: staged path count is $stagedCount, expected 11 - aborting commit"
    } else {
        $msg = 'round 91: take the clock out of the question. A round earlier this project put a corpse on a real screen for the first time. The attended test sent three frames about one identity, and the probe character went from standing to lying flat inside the window and stayed there, which the owner walked over to and photographed herself rather than taking anybody word for it. What that run could not say is which of the two lethal frames did it. One lands six seconds after the trigger and the other twelve, the photograph that caught the pose sits about one second from the boundary between them, and the time the capture itself took was never measured. So the honest reading of the strongest evidence this lane has is that the pose probably belongs to the earlier frame, and probably is not a word this repository is allowed to publish as a result. This round adds the experiment that does not need a clock at all: a second named profile of the same claim that sends the first two frames and then stops. If the pose still appears, it belongs to the earlier frame and nothing here has ever seen the death animation. If it does not appear, it belongs to the later one and the three frame reading stands. Neither answer depends on when a screenshot was taken, which is the entire point, and it is the experiment the tester asked for in the same note that reported the corpse. The experiment only means something while the absent third frame is the only difference between the two runs, so that property is built rather than asserted. The new profile does not carry its own copy of the plan; its steps are a slice of the same tuple the three frame profile uses, both profiles resolve step one and step two to the same row object, and the composer refuses to build a step whose row is not the row the full plan holds at that index. The bytes are then compared for real in three places that do not share a code path: the encoder pins them, the offline verifier compares the composed frames with equality on the bytes and on their hashes, and the headless replay composes the three frame sweep in process and compares the dispatched pair against its first two. The validator is stricter for the new profile rather than looser, which is the opposite of what truncating a sweep would normally mean. A profile that does not end on the death task must never emit a frame that satisfies the second engine predicate at all, must not carry the third step label anywhere in its order, and must end on a frame that satisfies the first predicate, so it cannot open the gate by accident and cannot end in a state that answers nothing. Each profile now also carries its own unlock token, compared by identity, so the key issued for one opens no byte of the other, and a step may carry the lethal mask bit only if its own profile declared that step lethal. Both of those are strictly narrower than what shipped yesterday. The dispatcher event now names the profile that was sent, because a log line saying only that the sweep went out cannot tell an attended tester which experiment they just ran. The three frame event string is unchanged down to the byte and a comparison in the dispatcher makes it stay that way, so a rename is an error rather than a silently republished name. The ledger entry is amended rather than replaced, and the new checkpoint is tracked as the third of three versions, which fills the budget. It is counted as a version although every byte it sends is a subset of the pinned frames, because it lets the lane end a session in a state no earlier version could produce: a character latched dying with the death task never opened. The conservative accounting is the honest one, and a fourth widening of this lane now needs a new entry or a scoped approval rather than another profile. The stop rule is rewritten to state the bound that is actually enforced rather than the one that was true when it was written, which is the same repair an earlier round made to the neighbouring entry, applied here before it was needed instead of after. The report this lane rests on gains an appended erratum rather than a quiet edit, and it withdraws a sentence rather than only adding numbers. That report predicted the probe would appear near the spawn point. It does not appear. Its identity is a placement the client already has in its map data, so the first frame updates a character that has been standing there all along, and the first attended run was nearly written up as a failed spawn on exactly that expectation. Both the prediction and the failure criterion built on it are withdrawn in writing, where the next reader will find them. Two guard counts in the same report were low and are corrected in the same erratum. What none of this does is watch a screen. No client has ever been shown one byte of the two frame profile, the coverage row for this lane does not move, and the sentence that the death animation has been observed is still not available to anybody working here. That is the queued attended test, and the reason it is queued rather than claimed. Nothing in this round boots a server, opens a client, writes to a database, flips a coverage row, adds an entry to the ledger, moves an entry index or touches the frozen delivered snapshot'
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
    "BY: job 147 (chief round 91) - released by the job itself, not by the round that placed it",
    "done: gate + commit of RUNTIMERES-LATCHONLY-001 - the two-frame tie-breaker profile",
    "      of HYP-PF-023 (ledger AMENDED, entry count stays 31, version 3 of 3).  11 paths",
    "      allGreen=$allGreen committed=$committed",
    "      latchver=$vLatchVer replay3=$vReplay3 replay2=$vReplay2 replayx=$vReplayX pytest=$pytestExit",
    "      seam=$seamExit ledger=$ledgerExit coverage=$covExit dmenc=$vDmEnc dmreplay=$vDmReplay",
    "      canonGuard=$canonGuard v141Guard=$v141Guard ignoreGuard=$ignoreGuard",
    "head: $headShort  (was $headBefore)",
    "next: GT-023, GT-024 and GT-025 are all queued and READY once this lands.  Do NOT flip the",
    "      HYP-PF-023 matrix row before GT-025 runs - that condition is the testers own and it stands",
    "warn: SPAWN does not make anything appear - the probe identity is a placement the client",
    "      already draws.  Any test spec that says otherwise is wrong and is corrected in the report",
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

W '=== 147 SUMMARY ==='
@(
    "lockCleared=$lockCleared",
    "latchver=$vLatchVer replay3=$vReplay3 replay2=$vReplay2 replayx=$vReplayX",
    "dmenc=$vDmEnc dmreplay=$vDmReplay",
    "hpenc=$vHpEnc damage=$vDamage runtimeres=$vRuntimeRes",
    "hpstatic=$vHpStatic stats=$vStats mpaudit=$vMpAudit corpus=$vCorpus census=$vCensus hlhold=$vHlHold",
    "pytest=$pytestExit seam=$seamExit ledger=$ledgerExit coverage=$covExit",
    "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit ignoreGuard=$ignoreGuard",
    "allGreen=$allGreen committed=$committed",
    "head=$headShort"
) | ForEach-Object { W $_ }
W '=== 147 DONE ==='

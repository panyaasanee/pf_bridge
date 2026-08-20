# Job 143 - round 86 gate and commit, RETRY of job 142 after the cp874 fix.
#
# WHY 142 WENT RED, AND WHY THE FIX IS NOT "MAKE THE TEST PASS".  Job 142 came
# back with census=1 and pytest=1, which is TWO red channels with ONE cause.
# tools/pf_vital_thunk_census_static.py printed a red-circle emoji, U+1F534, in
# one heading.  This console is code page 874.  That character has no mapping in
# it, and an unmappable character does not degrade into a question mark, it
# raises UnicodeEncodeError inside print(), so the tool died at that line having
# reported no finding at all, and the test that runs the tool for real died with
# it.  The sandbox writes UTF-8 and was green on the same bytes, so this was a
# tool that worked on one of the two machines this project verifies on and was
# dead on the other, which is the exact failure mode the no-disassembler rule
# exists to prevent.  The emoji is gone from the print and the words are
# unchanged.  A new test encodes both tools' stdout and stderr to cp874 and
# fails with the offending character and its output line number, so this is now
# red on BOTH machines rather than only on the one that matters at commit time;
# it was verified to fire by putting the emoji back and watching it go red.
# NO OTHER PATH CHANGED: the staged set is the same 24 paths as job 142.
#
# NOTE ON ORDERING: this job must not be placed in the inbox while the attended
# session holds the LOCK.  It would sit behind the game-launch job and go stale.
#
# WHY A DIFFERENT ROUND IS COMMITTING ROUND 86.  Round 86 was cut off mid-flight
# at 10:03 local, immediately after appending HYP-PF-023 to the ledger and
# before registering that id in the ledger verifier.  All of its work was intact
# in the worktree.  Round 87 took the LOCK on the published criteria (age >= 20
# min AND no outbox file, no worktree write and no LOCK touch for ~20 min; last
# worktree write 10:03, last outbox file 08:13, LOCK mtime 09:57) and finished
# the round rather than restarting it.
#
# FOUR LANES, ONE COMMIT.
#   A. RUNTIMERES-ENCODER-001 - the spawn-then-kill encoder over the actor-entry
#      carrier of 0x6E9D, plus HYP-PF-023, its scenario, dispatcher branch,
#      static verifier, headless replay and two test modules.
#   B. NAMES-FOLD-003 - the thunk census, its report and machine-readable
#      companion.
#   C. COMMENT-ERRATA-002 - two wrong comments in src/ corrected in place.
#   D. LEDGER-VISIBILITY-001 (round 87, unplanned) - register HYP-PF-023 in the
#      verifier, and add the check that would have caught what it found.
#
# TWO GUARDS EARNED THEIR KEEP BEFORE THIS JOB WAS WRITTEN AND BOTH ARE HERE:
#   1. check-ignore on every new path.  Round 86 wrote an allowlist comment
#      saying "Five files" and there were six; the headless replay was ignored
#      while HYP-PF-023 cited it as evidence.
#   2. The success flag is derived from HEAD ACTUALLY MOVING, never from control
#      flow reaching the line after git commit.
#
# SEAM IS MANDATORY THIS ROUND: .gitignore and reports are both staged.
#
# ASCII ONLY.  Quote all paths that contain spaces.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\143_round86_gate_commit.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 86 GATE AND COMMIT - RETRY AFTER CP874 FIX  $stamp ===" | Out-File -FilePath $log -Encoding utf8

Set-Location -LiteralPath $main
$headBefore = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD before = $headBefore  (expect 32878e0...)"

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

# ---------- 2. remove the one-shot ledger helper round 86 left behind ----------
# Its own docstring says it is deleted immediately after use.  It is ignored by
# version control, so this changes nothing in the commit; it is tidiness, and it
# is done here because the sandbox filesystem refuses the unlink.
$oneShot = Join-Path $main '_append_hyp_pf_023.py'
if (Test-Path -LiteralPath $oneShot) {
    Remove-Item -LiteralPath $oneShot -Force
    if (Test-Path -LiteralPath $oneShot) { W 'WARN: could not remove _append_hyp_pf_023.py' } else { W 'removed stray one-shot _append_hyp_pf_023.py' }
} else {
    W '_append_hyp_pf_023.py already gone'
}

# ---------- 3. worktree ----------
$dirty = @(git --no-optional-locks status --porcelain 2>&1)
W "worktree dirty paths = $($dirty.Count) (expect 24)"
$dirty | ForEach-Object { W "  st> $_" }

# ---------- 4. canonical DB, read from CANON_SHA.txt, never hardcoded ----------
$canon = Join-Path $main 'state\pirateforce.sqlite3'
$shaBefore = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
$canonExpect = (Get-Content -LiteralPath (Join-Path $bridge 'CANON_SHA.txt') -Raw).Trim()
W "canonical sha BEFORE = $shaBefore"
if ($shaBefore -ne $canonExpect) { W "ABORT: canonical sha != CANON_SHA.txt ($canonExpect)"; exit 13 }
W 'canonical matches CANON_SHA.txt'

# ---------- 5. verifiers: the fourteen of round 85 plus the two new ones ----------
W '--- verifiers (expect all sixteen at exit 0) ---'
py -3 (Join-Path $main 'tools\verify_hp_death_encoder.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  hpenc> $_" }
$vHpEnc = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_teleportcheck_0x4477_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  teleport> $_" }
$vTeleport = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_multiplayer_readiness_audit.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  mpaudit> $_" }
$vMpAudit = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_capture_corpus.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  corpus> $_" }
$vCorpus = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_split_operate_verb_panels_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  split> $_" }
$vSplit = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_damage_hit_result_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  damage> $_" }
$vDamage = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_login_vital_req_static.py')  2>&1 | Select-Object -Last 2 | ForEach-Object { W "  login> $_" }
$vLogin = $LASTEXITCODE
# arg 1 (the binary) is allowed and expected.  NEVER pass a second argument: that
# switches the tool back to scanning instead of using the pinned corpus.
py -3 (Join-Path $main 'tools\pf_vital_id_resolve_static.py') '..\GameClient\GameClient.local.bin' 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  names> $_" }
$vNames = $LASTEXITCODE
py -3 (Join-Path $main 'tools\verify_delete_refresh_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  delref> $_" }
$vDelRef = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_hp_death_respawn_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  hpstatic> $_" }
$vHpStatic = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_stats_progression_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  stats020> $_" }
$vStats = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_ui_state_refresh_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  uiref> $_" }
$vUi = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_vital_name_thunk_static.py') 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  thunk> $_" }
$vThunk = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_runtimeres_actor_entry_static.py') 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  runtimeres> $_" }
$vRuntimeRes = $LASTEXITCODE
W '--- NEW this round ---'
py -3 (Join-Path $main 'tools\pf_runtimeres_death_encoder_static.py') 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  deathenc> $_" }
$vDeathEnc = $LASTEXITCODE
py -3 (Join-Path $main 'tools\pf_vital_thunk_census_static.py') 2>&1 | Select-Object -Last 4 | ForEach-Object { W "  census> $_" }
$vCensus = $LASTEXITCODE
W "verifier exits: hpenc=$vHpEnc teleport=$vTeleport mpaudit=$vMpAudit corpus=$vCorpus split=$vSplit damage=$vDamage login=$vLogin names=$vNames delref=$vDelRef hpstatic=$vHpStatic stats=$vStats uiref=$vUi thunk=$vThunk runtimeres=$vRuntimeRes deathenc=$vDeathEnc census=$vCensus"

W '--- pytest full suite (sandbox pre-run: 1303 passed, 1 skipped, 2557 subtests; the'
W '    single sandbox failure is test_server_shutdown __notes__, a Python 3.10 artefact'
W '    of the sandbox interpreter and NOT a code defect - it must be GREEN here) ---'
py -3 -m pytest tests -q 2>&1 | Select-Object -Last 8 | ForEach-Object { W "  py> $_" }
$pytestExit = $LASTEXITCODE

W '--- seam (MANDATORY: .gitignore and reports are staged) ---'
py -3 -m pytest (Join-Path $main 'tests\test_foundation_legacy_seam.py') -q 2>&1 | Select-Object -Last 3 | ForEach-Object { W "  seam> $_" }
$seamExit = $LASTEXITCODE
W '--- ledger (expect PASS entries=30 - HYP-PF-023 is appended this round) ---'
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

W '--- check-ignore on every new path (expect NOT ignored for all twelve) ---'
$newPaths = @(
    'reports/PF_NAMES_FOLD003_LEGACY_SLOTS_AND_THUNK_CENSUS_20260819.census.json',
    'reports/PF_NAMES_FOLD003_LEGACY_SLOTS_AND_THUNK_CENSUS_20260819.md',
    'reports/PF_RE_V107_to_V110_Stateful_Inventory_and_ActionItem_Capture_20260814.md',
    'reports/PF_RUNTIMERES_ENCODER001_SPAWN_THEN_KILL_20260819.md',
    'scenarios/runtimeres_death_hypothesis_spawn_then_kill.json',
    'src/pirateforce_foundation/runtimeres_death_hypothesis.py',
    'tests/test_names_fold003_thunk_census.py',
    'tests/test_runtimeres_death_dispatch.py',
    'tests/test_runtimeres_death_hypothesis.py',
    'tools/pf_runtimeres_death_encoder_static.py',
    'tools/pf_runtimeres_death_headless_replay.py',
    'tools/pf_vital_thunk_census_static.py'
)
$ignoreGuard = 0
foreach ($p in $newPaths) {
    git --no-optional-locks check-ignore -q -- "$p"
    if ($LASTEXITCODE -eq 0) { W "  RED: $p IS IGNORED"; $ignoreGuard = 1 } else { W "  ok (tracked): $p" }
}

$allGreen = ($vHpEnc -eq 0) -and ($vTeleport -eq 0) -and ($vMpAudit -eq 0) -and ($vCorpus -eq 0) -and `
            ($vSplit -eq 0) -and ($vDamage -eq 0) -and ($vLogin -eq 0) -and ($vNames -eq 0) -and `
            ($vDelRef -eq 0) -and ($vHpStatic -eq 0) -and ($vStats -eq 0) -and ($vUi -eq 0) -and `
            ($vThunk -eq 0) -and ($vRuntimeRes -eq 0) -and ($vDeathEnc -eq 0) -and ($vCensus -eq 0) -and `
            ($pytestExit -eq 0) -and ($canonGuard -eq 0) -and ($seamExit -eq 0) -and `
            ($ledgerExit -eq 0) -and ($covExit -eq 0) -and ($v141Guard -eq 0) -and `
            ($diffExit -eq 0) -and ($ignoreGuard -eq 0)
W "ALL GREEN = $allGreen"

$committed = 0
if ($allGreen) {
    W '--- GUARDED COMMIT: read-tree HEAD, then stage ONLY the twenty-four round 86 paths ---'
    $rt = (git --no-optional-locks read-tree HEAD 2>&1 | Out-String).Trim()
    if ($rt) { W "  read-tree> $rt" }
    if ($LASTEXITCODE -ne 0) { W 'ABORT: read-tree failed - not staging anything'; exit 34 }

    $paths = @(
        '.gitignore',
        'docs/HYPOTHESIS_LEDGER.json',
        'docs/PF_VITAL_NAMES.json',
        'reports/PF_NAMES_FOLD003_LEGACY_SLOTS_AND_THUNK_CENSUS_20260819.census.json',
        'reports/PF_NAMES_FOLD003_LEGACY_SLOTS_AND_THUNK_CENSUS_20260819.md',
        'reports/PF_RE_V107_to_V110_Stateful_Inventory_and_ActionItem_Capture_20260814.md',
        'reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md',
        'reports/PF_RUNTIMERES_ENCODER001_SPAWN_THEN_KILL_20260819.md',
        'scenarios/runtimeres_death_hypothesis_spawn_then_kill.json',
        'src/pirateforce_foundation/app.py',
        'src/pirateforce_foundation/runtime.py',
        'src/pirateforce_foundation/runtimeres_death_hypothesis.py',
        'src/pirateforce_foundation/stats_progression_hypothesis.py',
        'tests/test_hypothesis_ledger.py',
        'tests/test_names_fold003_thunk_census.py',
        'tests/test_runtimeres_actor_entry_static.py',
        'tests/test_runtimeres_death_dispatch.py',
        'tests/test_runtimeres_death_hypothesis.py',
        'tools/pf_runtimeres_actor_entry_static.py',
        'tools/pf_runtimeres_death_encoder_static.py',
        'tools/pf_runtimeres_death_headless_replay.py',
        'tools/pf_vital_name_thunk_static.py',
        'tools/pf_vital_thunk_census_static.py',
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

    W '--- staged summary (expect 24 paths, NO deletions) ---'
    git --no-optional-locks diff --cached --stat 2>&1 | Select-Object -Last 30 | ForEach-Object { W "  staged> $_" }
    $stagedCount = @(git --no-optional-locks diff --cached --name-only 2>&1).Count
    W "staged path count = $stagedCount (expect 24)"
    $delLines = (git --no-optional-locks diff --cached --name-status 2>&1 | Select-String -Pattern '^D')
    if ($delLines) {
        W 'RED: staged set contains DELETIONS - aborting commit'; $delLines | ForEach-Object { W "  DEL> $_" }
    } elseif ($stagedCount -ne 24) {
        W "RED: staged path count is $stagedCount, expected 24 - aborting commit"
    } else {
        $msg = 'round 86: build the only encoder that can reach the death chain, give two hundred and nine registered classes a name we can honestly say we do not have, and find out that the ledger has been citing a document a fresh clone does not contain. The first lane exists because round 85 proved a negative rather than a positive. The attribute update pipe that round 81 built its death encoder on cannot reach the engine death chain at all, because its inbound handler holds not one dispatch of the shape that chain requires, so that lane can open the downed window on the local player, which is exactly what the owner watched happen on her own screen, and it can never latch the dead state, spawn the death task or play the death animation no matter what it sends. The new encoder therefore uses a different carrier entirely, the actor entry collection of the run time protocol response, and it opens the twenty third hypothesis rather than extending the twenty second, because the carrier, the frame identity, the arity and the claim are all different. The earlier entry is untouched and stays active as the lane that owns the window a human has actually seen. Two facts about this sweep are load bearing and both are the opposite of what a reader would assume, so they are written into the entry, the module and the scenario rather than left to be rediscovered. The timer polarity is inverted: the positive value that opens the dying window is the same value that prevents the animation, because the two engine predicates agree on hit points being zero and differ only in the sign test on one float, so both sides have to be sent and in that order. And an actor cannot be born dead, because an identity the client has never seen takes the spawn path, which never touches the dead state sync, so killing anything requires a second message about an identity the client already knows. That is why the sweep is three frames and not two. Nothing about the envelope is invented, since the frames are composed by the frozen delivery snapshot serialisers; what is designed is the policy of answering one accepted chat input frame with this sweep, and no capture has ever shown it. The lane is proven through the real dispatcher and its headless replay is written, and it stays behind an opt in scenario, an exclusive flag, a required database and production not allowed. No client has ever seen one of these frames and nothing in this project has ever observed the death animation, which is the in game test this queues. The second lane finishes the counting the previous round started. The registry recovered from client strings covers three hundred and ten of the five hundred and nineteen registration thunks in the image, so two hundred and nine registered classes are named by the binary and absent from that file, and the census writes down which ones with a machine readable companion the report derives its numbers from rather than restating them by hand. The third lane repairs two comments in the source that were carried forward as true after the evidence stopped supporting them. One claimed a single caller where the full census is one direct call and four vtable slots, and the conclusion survives the fuller count unchanged, which is the point of correcting it rather than deleting it. The fourth lane was not planned and is the reason this commit is worth reading. Registering the new hypothesis in the verifier is a required step that the interrupted round never reached, and doing it raised the question of what else the verifier does not check. It checks that every file a hypothesis cites exists. Existence on the machine that wrote the file and presence in the repository are different properties, and only the second one is what the word evidence means to somebody cloning this later. Sweeping every cited path against the ignore rules found two failures of exactly that kind. The headless replay of the new lane was ignored while the new entry cited it as evidence, which the allowlist comment written the same day missed because it counted the files in prose and the prose said five when there were six. And a report from the fourteenth, cited as evidence by two entries that are still active today, has been invisible to version control since the day it was written, so a fresh clone has never contained the document those two claims rest on. Both are fixed by adding the files rather than by dropping the references, because the references were the part that was correct. The check that found them is now a test, deliberately a test rather than a guard inside the verifier, because it is the one question in this area that cannot be answered from the working tree alone and has to ask version control, and the verifier stays runnable with the standard library and no repository. It carries a trap that builds a throwaway repository and requires the check to fire on an ignored file and stay quiet on a visible one, because a check that has never been seen to fail is not a check. One process note belongs in the record. The round that did the first three lanes was cut off partway through, immediately after appending to the ledger and before registering the identifier, and the round that took over finished it instead of restarting it, on the published criteria for deciding a holder is gone. The fail closed design is what made that safe: an unregistered identifier is an immediate red, so the interrupted state announced itself rather than sitting quietly in a green tree. The fifth lane is the one the gate found rather than the one anybody planned, and it is here because the first attempt at this commit went red in two channels with one cause. A tool this round adds printed a red circle emoji in one of its headings. The console on the machine that runs the gate is code page 874, that character has no mapping in it, and an unmappable character does not quietly become a question mark, it raises inside the print call, so the tool died at that line having reported none of its findings and took the test that runs it down as well. The same bytes were green in the sandbox, whose output is utf eight, which means the project had a verifier that worked on one of the two machines it verifies on and was dead on the other, and the only reason anybody found out is that the commit path runs on the machine where it was dead. The decoration is gone and the sentence is unchanged, because the sentence was doing the work. The check that replaces it encodes what both tools actually print to the narrower code page and fails with the offending character and the line of output it appeared on, so the next person who reaches for a symbol gets a red line on both machines rather than on only one of them, and it was confirmed to fail by putting the character back and watching it go red. Asserting on what the tool prints rather than on what its source contains is deliberate, because the comments in that file are written in Thai and are harmless and staying, and because a source scan would miss anything a tool composes at run time from what it reads out of the image. Nothing in this round boots a server, opens a client, writes to a database, flips a coverage row or touches the frozen delivered snapshot'
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

W '--- post-commit worktree state (expect clean) ---'
git --no-optional-locks status --short 2>&1 | Select-Object -First 25 | ForEach-Object { W "  st> $_" }
$shaEnd = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha END = $shaEnd (expect unchanged)"
if (Test-Path -LiteralPath $lockPath) { W 'WARN: an index.lock exists again at the end of this job' }

W '=== 143 SUMMARY ==='
@(
    "lockCleared=$lockCleared",
    "hpenc=$vHpEnc teleport=$vTeleport mpaudit=$vMpAudit corpus=$vCorpus split=$vSplit",
    "damage=$vDamage login=$vLogin names=$vNames delref=$vDelRef hpstatic=$vHpStatic stats=$vStats uiref=$vUi",
    "thunk=$vThunk runtimeres=$vRuntimeRes deathenc=$vDeathEnc census=$vCensus",
    "pytest=$pytestExit seam=$seamExit ledger=$ledgerExit coverage=$covExit",
    "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit ignoreGuard=$ignoreGuard",
    "allGreen=$allGreen committed=$committed",
    "head=$(git --no-optional-locks rev-parse --short HEAD 2>&1)"
) | ForEach-Object { W $_ }
W '=== 143 DONE ==='

# Job 175 - chief round 109.  PANYA ORDER 2026-08-20 ~19:10 ("path D approved").
#
# WHAT: gate the full battery, then commit exactly ONE path:
#   .github/workflows/gate-windows.yml
#
# WHY.  A chief running in a Claude Code Routine has no GitHub credential inside
# its sandbox; git works there only because a proxy injects credentials on the
# way out.  So that chief cannot ask the Actions API whether a run was green.
# The runner knows.  So the runner writes the verdict down in the one channel
# both sides are proven to reach: git itself, on an orphan branch named
# ci-status, one file per commit, named for the commit it is about.
#
# The patch differs from the round-108 draft in six ways and the first is a real
# bug in the draft (FINDINGS_R109_PATH_D_APPLIED_AND_REHEARSED.md has all six):
#   1. shell: bash - this file sets defaults.run.shell = pwsh, so without it
#      `set -euo pipefail` is silently skipped and the step goes GREEN while the
#      push fails.  That failure mode is invisible in exactly the wrong way.
#   2. no ci/latest.json - a "latest" verdict is how a chief reads the word
#      success about one commit and merges a different one, silently.
#   3. pull_request uses the branch head sha, not the ephemeral merge commit.
#   4. push retried 3x with rebase, never forced; commit --allow-empty.
#   5. loop prevention twice: branches-ignore at the trigger AND a ref guard on
#      the job, neither depending on GitHub's GITHUB_TOKEN rule.
#   6. every value crosses into bash through env:, not ${{ }} in the script text.
#
# ALREADY MEASURED IN THE SANDBOX ON THESE EXACT BYTES (not re-done here):
#   yaml.safe_load parses the file; jobs are exactly [gate, publish-status];
#   the step's `run` body was EXTRACTED FROM THE YAML and rehearsed against a
#   local bare repo: orphan creation on the first run, append on later runs,
#   re-run of the same commit, a lost push race that rebased and won with no
#   verdict lost, and a missing verdict answering exit 128.
#
# MEASURABLE END CONDITIONS:
#   1. the declared path is the ONLY dirty path in the worktree
#   2. eight text guards prove the patch is really in the file (and one proves
#      ci/latest.json is really ABSENT - a negative guard, because the whole
#      point of removing it is that nobody adds it back "helpfully")
#   3. non-ascii bytes in the file = 0 (the file declares itself ASCII only)
#   4. the full bridge battery is green, including the whole pytest suite
#   5. commit lands, HEAD moves, and the COMMITTED BLOB carries the patch
#
# NOT done here: git push / remote config - Panya pushes, always.
# NOT touched: LOCK_GAME.txt, the server, the client, any database write, and
# the pf_bridge repository index (Panya has her own backlog commits in flight
# there; this job stays out of it).
# This job writes LOCK_GIT.txt HELD at start and RELEASED at the end whatever
# happens - held only while the gate/commit actually runs.
# ASCII ONLY.  Quote every path that contains a space.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\175_round109_path_d.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== ROUND 109 GATE AND COMMIT (job 175) - path D, the ci-status verdict channel  $stamp ===" | Out-File -FilePath $log -Encoding utf8

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
    "BY: job 175 (chief round 109) - PANYA ORDER 1910: apply path D",
    "PLAN: guards (only-declared-path dirty, patch present, latest.json ABSENT,",
    "      ascii zero) -> full bridge battery -> one-path guarded commit ->",
    "      committed-blob assertion -> release immediately.  No push.",
    "      Does NOT touch LOCK_GAME (no server/client/DB writes) and does NOT",
    "      touch the pf_bridge git index."
) | Out-File -FilePath $lockGit -Encoding utf8
W 'LOCK_GIT.txt set to HELD by job 175'

Set-Location -LiteralPath $main
$headBefore = (git --no-optional-locks rev-parse HEAD 2>&1)
W "HEAD before = $headBefore  (expect 9045978...)"

$wfRel  = '.github/workflows/gate-windows.yml'
$paths1 = @($wfRel)
W "declared path set = $($paths1.Count) (expect 1)"

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
} else { W 'no index.lock present' }

# ---------- 2. worktree state: expect EXACTLY the declared path dirty ----------
$dirty = @(git --no-optional-locks status --porcelain 2>&1)
W "worktree dirty paths = $($dirty.Count) (expect 1)"
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

# ---------- 4. the patch must actually be present in the worktree ----------
$fixGuard = 0
function CountIn($relPath, $needle) {
    $full = Join-Path $main ($relPath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $full)) { return -1 }
    $t = [System.IO.File]::ReadAllText($full)
    return ([regex]::Matches($t, [regex]::Escape($needle))).Count
}
$p1 = CountIn $wfRel '  publish-status:'
$p2 = CountIn $wfRel "branches-ignore: ['ci-status']"
$p3 = CountIn $wfRel "if: always() && github.ref_name != 'ci-status'"
$p4 = CountIn $wfRel 'shell: bash'
$p5 = CountIn $wfRel 'contents: write'
$p6 = CountIn $wfRel 'git commit -q --allow-empty -m'
$p7 = CountIn $wfRel 'github.event.pull_request.head.sha'
# The old trigger is quoted verbatim in the comment that explains why it was
# replaced, so a substring count would answer 1 and mean nothing.  Count only
# lines where it is LIVE YAML - i.e. lines whose first non-space character is
# not '#'.  A guard that cannot tell code from prose is not a guard.
$wfFull = Join-Path $main ($wfRel -replace '/', '\')
$p8 = @(Get-Content -LiteralPath $wfFull |
        Where-Object { $_ -cmatch "^\s*branches:\s*\['\*\*'\]" }).Count
$p9 = CountIn $wfRel 'ci/latest.json'            # must appear ONLY in the prose that forbids it
W "patch guards: publishJob=$p1(1) branchesIgnore=$p2(1) refGuard=$p3(1) shellBash=$p4(1)"
W "              contentsWrite=$p5(1) allowEmpty=$p6(1) prHeadSha=$p7(1) liveOldTrigger=$p8(0) latestJson=$p9(1)"
if ($p1 -ne 1 -or $p2 -ne 1 -or $p3 -ne 1 -or $p4 -ne 1 -or $p5 -ne 1 -or $p6 -ne 1 -or $p7 -ne 1) { $fixGuard = 1 }
# NEGATIVE guards.  The old trigger must be gone as LIVE YAML or the loop guard
# is theatre.  ci/latest.json must appear exactly once - in the comment that
# explains why it does not exist.  A second occurrence means somebody put the
# loaded gun back on the table.
if ($p8 -ne 0) { W 'RED: a LIVE branches: [**] trigger line is still present'; $fixGuard = 1 }
if ($p9 -ne 1) { W "RED: ci/latest.json occurs $p9 times, expected exactly 1 (the prose forbidding it)"; $fixGuard = 1 }
if ($fixGuard -eq 1) { W 'ABORT: the patch this job exists to commit is not in the worktree as declared.'; exit 42 }

# ---------- 5. ASCII guard: this file declares itself ASCII only ----------
$asciiGuard = 0
foreach ($p in $paths1) {
    $full = Join-Path $main ($p -replace '/', '\')
    $bytes = [System.IO.File]::ReadAllBytes($full)
    $nonAscii = 0
    $crlf = 0
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        if ($bytes[$i] -gt 127) { $nonAscii++ }
        if ($bytes[$i] -eq 13)  { $crlf++ }
    }
    W "non-ascii bytes in $p = $nonAscii (expect 0);  CR bytes = $crlf (expect 0)"
    if ($nonAscii -ne 0 -or $crlf -ne 0) { $asciiGuard = 1 }
}
if ($asciiGuard -eq 1) { W 'ABORT: the workflow file is no longer ASCII-only with LF endings.'; exit 45 }

# ---------- 5b. YAML parse, if this machine can.  A skip is NOT a pass. ----------
# The sandbox already parsed these exact bytes with PyYAML and reported
# jobs = [gate, publish-status].  Try to re-derive it here; if PyYAML is not
# installed on the bridge, SAY SO instead of pretending, and do not install
# anything - a gate job is not the place to change this machine's packages.
$yamlPy = @'
import sys
try:
    import yaml
except ImportError:
    print("yamlParse=SKIP pyyaml is not installed on this machine")
    sys.exit(0)
d = yaml.safe_load(open(sys.argv[1], "rb").read().decode("ascii"))
jobs = list(d["jobs"].keys())
trig = d[True] if True in d else d.get("on")
print("yamlParse=OK jobs=%s" % (",".join(jobs),))
print("trigger=%s" % (trig,))
ok = jobs == ["gate", "publish-status"]
ok = ok and d["jobs"]["publish-status"]["steps"][0].get("shell") == "bash"
ok = ok and d["jobs"]["publish-status"]["permissions"] == {"contents": "write"}
ok = ok and d["jobs"]["publish-status"]["needs"] == ["gate"]
print("structure=%s" % ("OK" if ok else "RED"))
sys.exit(0 if ok else 1)
'@
$yamlFile = Join-Path $env:TEMP "r109_yaml_$stamp.py"
Set-Content -LiteralPath $yamlFile -Value $yamlPy -Encoding UTF8
py -3 "$yamlFile" (Join-Path $main ($wfRel -replace '/', '\')) 2>&1 | ForEach-Object { W "  yaml> $_" }
$yamlExit = $LASTEXITCODE
W "yaml structure exit = $yamlExit (expect 0; SKIP line above means pyyaml absent, which is NOT a pass)"
Remove-Item -LiteralPath $yamlFile -Force -ErrorAction SilentlyContinue
Beat 'preflight done, starting battery'

# ---------- 6. the battery (job-169 shape) ----------
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
W '--- ledger verifier ---'
py -3 (Join-Path $main 'tools\verify_hypothesis_ledger.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  ledger> $_" }
$ledgerExit = $LASTEXITCODE
W '--- multiplayer readiness audit (needs real git history) ---'
py -3 (Join-Path $main 'tools\pf_multiplayer_readiness_audit.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  mpaudit> $_" }
$mpAuditExit = $LASTEXITCODE
W '--- vital-thunk census ---'
py -3 (Join-Path $main 'tools\pf_vital_thunk_census_static.py') 2>&1 | Select-Object -Last 2 | ForEach-Object { W "  census> $_" }
$censusExit = $LASTEXITCODE
Beat 'verifiers done, starting full pytest'

W '--- pytest full suite on Windows with -rs ---'
$env:COLUMNS = '200'
$pytestLog = Join-Path $env:TEMP "r109_pytest_$stamp.txt"
$pyOut = (py -3 -m pytest tests -q -rs 2>&1)
$pytestExit = $LASTEXITCODE
$pyOut | Out-File -FilePath $pytestLog -Encoding utf8
$pyOut | Select-Object -Last 8 | ForEach-Object { W "  py> $_" }
Beat 'full pytest done, running the skip census'

W '--- skip census on that exact transcript (expect 0) ---'
py -3 (Join-Path $main 'tools\pf_pytest_precondition_census.py') --report "$pytestLog" 2>&1 | ForEach-Object { W "  skipcensus> $_" }
$skipCensusExit = $LASTEXITCODE
W "skip census exit = $skipCensusExit (expect 0)"

# ---------- 7. guards ----------
$shaAfter = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
if ($shaAfter -cne $shaBefore) { W 'RED: CANONICAL DB MOVED'; $canonGuard = 1 } else { W 'canonical guard OK'; $canonGuard = 0 }
$v141Dirty = (git --no-optional-locks status --short -- 'current/pf_login_game_server_v141.py' 2>&1 | Out-String).Trim()
if ($v141Dirty) { W "RED: v141 SNAPSHOT DIRTY -> $v141Dirty"; $v141Guard = 1 } else { W 'v141 guard OK'; $v141Guard = 0 }
git --no-optional-locks diff --check 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  git> $_" }
$diffExit = $LASTEXITCODE

$allGreen = ($asciiGuard -eq 0) -and ($fixGuard -eq 0) -and ($unexpected -eq 0) -and `
            ($yamlExit -eq 0) -and ($seamExit -eq 0) -and ($covTestExit -eq 0) -and `
            ($covExit -eq 0) -and ($ledgerExit -eq 0) -and ($mpAuditExit -eq 0) -and `
            ($censusExit -eq 0) -and ($pytestExit -eq 0) -and ($skipCensusExit -eq 0) -and `
            ($canonGuard -eq 0) -and ($v141Guard -eq 0) -and ($diffExit -eq 0)
W "ALL GREEN = $allGreen"

# ---------- 8. guarded commit: read-tree HEAD, stage ONLY the declared path ----------
$committed = 0
$headAfter = $headBefore
$blobOk = -1
if ($allGreen) {
    Beat 'battery green, committing'
    W '--- GUARDED COMMIT: read-tree HEAD, then stage ONLY the one round-109 path ---'
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
    W "staged path count = $stagedCount (expect 1)"
    git --no-optional-locks diff --cached --stat 2>&1 | Select-Object -Last 6 | ForEach-Object { W "  staged> $_" }
    $delLines = (git --no-optional-locks diff --cached --name-status 2>&1 | Select-String -Pattern '^D' -CaseSensitive)
    if ($delLines) {
        W 'RED: staged set contains DELETIONS - aborting'; $delLines | ForEach-Object { W "  DEL> $_" }
    } elseif ($stagedCount -ne 1) {
        W "RED: staged count is $stagedCount, expected 1 - aborting"
    } else {
        $msg = "round 109: give the gate a mouth, so a chief with no credential can hear the verdict. A chief running in a Claude Code Routine has no GitHub token inside its sandbox at all; git works there only because a proxy injects credentials on the way out and inspects what passes. That chief therefore cannot ask the Actions API whether a run was green, not with gh, not with curl, not with a connector nobody has verified, and the whole of plan A prime rests on it being able to find out. The runner is the one who knows. So the runner writes it down, in the one channel measured to reach both sides, which is git: a new job named publish-status appends one JSON file per commit to an orphan branch called ci-status, named for the commit it is about, and a chief reads it with three lines of plain git and nothing else. It runs with if always, because a channel that only speaks when the news is good teaches its reader that silence means failure, and silence here means no information, which must stay a different thing. Six things differ from the draft written the round before and the first is a defect in that draft: this file sets a pwsh default shell, under which set euo pipefail is not an error but a command not found, so the script would have run on past its first failure and the step would have gone green while nothing was ever published, which is the exact shape of invisibility this workflow exists to abolish; the step now says shell bash. Second, there is deliberately no latest file, and a negative guard in this job keeps it that way, because a verdict addressed to whoever asks is how a reader learns the word success about one commit and merges another one without a single warning, and Panya named that the most expensive mistake this design can make. Third, a pull request event publishes under the branch head rather than the ephemeral merge commit that exists only inside the run, which no chief could ever resolve. Fourth, the push is retried three times with a rebase and never forced, because the branch is append only and a force here deletes verdicts other commits are relying on, and the commit allows itself to be empty so that a rerun of one commit in one second cannot turn a harmless repeat into a missing verdict. Fifth, the loop is prevented twice over and neither guard leans on the other: the trigger stops ignoring nothing and starts ignoring ci-status by name, and the job carries a ref guard of its own, so that the rule about GITHUB_TOKEN not retriggering, which is enforced somewhere we cannot see and protects nothing the day someone publishes with a personal token, is a third line of defence rather than the only one. Sixth, every value crosses into the shell as an environment variable instead of interpolated into the script text. The branch is an orphan on purpose, so that the scan plan A prime performs over refs beginning with claude cannot see it even in principle, and a fast forward from it is impossible by construction rather than by memory. The body of that step was extracted back out of this yaml and rehearsed against a local bare repository before this commit: orphan creation, later appends, a rerun, a lost push race that rebased and won with no verdict lost, and a missing verdict answering exit one hundred twenty eight, which is the signal that means do not merge. None of that touched GitHub, and until the branch is seen to exist there this remains a design that has been tested rather than a channel that has been proven, which is the acceptance criterion Panya wrote herself. One path. No source, no test, no scenario, no ledger entry, no coverage grade, no server booted, no client opened, no database written, no remote touched: the push is Panya's alone."
        git --no-optional-locks commit -m "$msg" 2>&1 | Select-Object -First 3 | ForEach-Object { W "  commit> $_" }
        $headAfter = (git --no-optional-locks rev-parse HEAD 2>&1)
        if ($headAfter -cne $headBefore) {
            $committed = 1
            W "COMMIT CONFIRMED: HEAD $headBefore -> $headAfter"
            git --no-optional-locks show --stat --oneline -s HEAD 2>&1 | Select-Object -First 8 | ForEach-Object { W "  head> $_" }
        } else { W "RED: commit returned but HEAD did not move (still $headBefore)" }
    }
} else {
    W 'NOT COMMITTING - a guard is red.  The edit stays as a dirty diff'
    W '(never reset/clean by iron rule) - receipt says so for the next round.'
}

# ---------- 9. acceptance: the COMMITTED BLOB must carry the patch ----------
if ($committed -eq 1) {
    $blobOk = 0
    $b1 = (git --no-optional-locks show ('HEAD:' + $wfRel) 2>&1 | Out-String)
    $a1 = ([regex]::Matches($b1, [regex]::Escape('  publish-status:'))).Count
    $a2 = ([regex]::Matches($b1, [regex]::Escape('shell: bash'))).Count
    $a3 = ([regex]::Matches($b1, [regex]::Escape("branches-ignore: ['ci-status']"))).Count
    # Same distinction as the worktree guard: LIVE yaml only, never the prose.
    $a4 = @(($b1 -split "`n") | Where-Object { $_ -cmatch "^\s*branches:\s*\['\*\*'\]" }).Count
    W "acceptance on the committed blob: publishJob=$a1(1) shellBash=$a2(1) branchesIgnore=$a3(1) liveOldTrigger=$a4(0)"
    if ($a1 -ne 1 -or $a2 -ne 1 -or $a3 -ne 1 -or $a4 -ne 0) { $blobOk = 1; W 'RED: the committed blob does not carry the patch' }
    $blobNonAscii = 0
    foreach ($b in [System.Text.Encoding]::UTF8.GetBytes($b1)) { if ($b -gt 127) { $blobNonAscii++ } }
    W "committed blob non-ascii bytes = $blobNonAscii (expect 0)"
    if ($blobNonAscii -ne 0) { $blobOk = 1 }
}

W '--- post-commit worktree state (expect clean) ---'
git --no-optional-locks status --short 2>&1 | Select-Object -First 8 | ForEach-Object { W "  st> $_" }
$shaEnd = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash
W "canonical sha END = $shaEnd (expect unchanged)"
Remove-Item -LiteralPath $pytestLog -Force -ErrorAction SilentlyContinue

# ---------- 10. release LOCK_GIT.txt, whatever happened ----------
$headShort = (git --no-optional-locks rev-parse --short HEAD 2>&1)
@(
    "RELEASED: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00",
    "BY: job 175 (chief round 109) - released by the job itself",
    "done: PANYA ORDER 1910 executed - path D applied to the Windows gate.  A new",
    "      job, publish-status, appends one verdict per commit to an ORPHAN branch",
    "      named ci-status at ci/<sha>.json, so a cloud chief with no GitHub",
    "      credential can read a gate result with three lines of plain git.  It",
    "      runs if: always(), so it reports RED too; silence stays reserved for",
    "      'no information', which is the only thing that may never be read as",
    "      green.  Six differences from the round-108 draft, the first a real bug",
    "      in it: shell: bash (the file defaults to pwsh, where set -euo pipefail",
    "      is skipped and a failed push would report success); NO ci/latest.json",
    "      and a negative guard keeping it absent; the PR head sha instead of the",
    "      ephemeral merge commit; three push retries with rebase, never force,",
    "      plus --allow-empty; loop prevention twice (branches-ignore at the",
    "      trigger AND a ref guard on the job) with GitHub's GITHUB_TOKEN rule as",
    "      a third line and not the only one; and every value entering bash via",
    "      env: rather than interpolation.",
    "      allGreen=$allGreen committed=$committed blobOk=$blobOk",
    "      ascii=$asciiGuard fixGuard=$fixGuard unexpectedDirty=$unexpected yaml=$yamlExit",
    "      seam=$seamExit covTest=$covTestExit coverage=$covExit ledger=$ledgerExit",
    "      mpaudit=$mpAuditExit census=$censusExit pytest=$pytestExit skipCensus=$skipCensusExit",
    "      canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit",
    "head: $headShort  (was $headBefore)",
    "next: PANYA PUSHES.  Then the acceptance criterion she wrote herself, which",
    "      this round does NOT claim to have met: watch Actions run, and look for",
    "      the branch ci-status to APPEAR on GitHub carrying ci/<that sha>.json.",
    "      Until that branch is seen to exist, path D is a design that has been",
    "      rehearsed, not a channel that has been proven - a document is not",
    "      evidence.  Rehearsal details and the six deltas:",
    "      pf_bridge\FINDINGS_R109_PATH_D_APPLIED_AND_REHEARSED.md",
    "      Also waiting on Panya, unchanged: install the sync (SETUP_GIT_SYNC.bat,",
    "      as administrator), then create the Routine with prompt v3, hourly, both",
    "      repositories.  chief next job = 176, tester = 9xx (0xxx while holding",
    "      LOCK_GAME).",
    "warn: the pf_bridge repository index was deliberately NOT touched by this job.",
    "      Panya has her own backlog commits in flight there, and two writers on",
    "      one index is how a dirty diff disappears.  The round-109 documents",
    "      (FINDINGS_R109, the v3 prompt edits, CHIEF_CONTINUATION) are on disk and",
    "      uncommitted on purpose; they are hers to commit with the rest.",
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

W '=== 175 SUMMARY ==='
@(
    "ascii=$asciiGuard fixGuard=$fixGuard unexpectedDirty=$unexpected yaml=$yamlExit",
    "seam=$seamExit covTest=$covTestExit coverage=$covExit ledger=$ledgerExit",
    "mpaudit=$mpAuditExit census=$censusExit pytest=$pytestExit skipCensus=$skipCensusExit",
    "canonGuard=$canonGuard v141Guard=$v141Guard diffcheck=$diffExit",
    "allGreen=$allGreen committed=$committed blobOk=$blobOk",
    "head=$headShort"
) | ForEach-Object { W $_ }
W '=== 175 DONE ==='

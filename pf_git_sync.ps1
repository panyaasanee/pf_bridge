# pf_git_sync.ps1 - the Windows side of the two-machine split.  ASCII only.
#
# WHY THIS EXISTS (chief round 108, 2026-08-20, ordered by Panya at ~18:00 in
# notes_to_chief\20260820_1800_PANYA-DECISION-sync-design-approved.md).
# The chief is moving off this machine and onto a cloud routine that clones the
# two repositories at the start of every run.  From there it can see exactly one
# thing: what has been pushed.  The tester keeps working on this machine, and the
# tester's results - letters in notes_to_chief\ and screenshots in
# evidence_screens\ - are the only things this machine has to say back.  So this
# script carries mail in both directions on a five minute clock and does nothing
# else.  Every design decision below is written down in DESIGN_R107_WINDOWS_SYNC.md;
# what follows are the ones that shape the code.
#
# THE FLAG SYSTEM DOES NOT CROSS MACHINES AND MUST NOT.  Both flags guard one
# machine's physical resources - ports, the server process, the game window, the
# canonical database, this worktree's git index - and a cloud chief can reach none
# of them, so a flag it held would protect nothing.  What replaces it is disjoint
# write sets plus the push rejection git already performs atomically on the server.
# That rejection is the only real mutual exclusion this system has, which is the
# single reason --force is forbidden outright, here and in the cloud prompt.
# It also means the flags must never travel: if a pull ever overwrote LOCK_GAME.txt
# the whole flag system would fail silently, which is worse than having no flags.
# Hence guard [0], which refuses to do anything at all on a day when .gitignore has
# stopped ignoring the three flag files.
#
# WHAT IT MAY PUSH: notes_to_chief/** and evidence_screens/** and nothing else.
# Both are new files with timestamps in their names, so a rebase cannot collide by
# construction rather than by luck.  CHIEF_CONTINUATION.md, GAME_TEST_QUEUE.md and
# CLIENT_RE_QUEUE.md are deliberately NOT in the allowlist: the chief owns them,
# and an edit made here can never travel out.  What happens to the pull is
# narrower than an earlier wording of this comment claimed ("fails loudly and
# this script stops and says so" - it does not stop; see the "Do NOT Finish
# here" note in step [3], which is deliberate and stays): the fast-forward is
# refused only when the incoming commits touch that same file, and the round
# then writes SYNC_ATTENTION.txt plus a SYNC_STUCK_* letter and CARRIES ON to
# the push block.  When the chief happens not to touch the file, the merge
# succeeds silently and the local edit simply sits here unnoticed, which is the
# worse of the two outcomes.  Nothing is lost either way - the edits are still
# on the disk - but nothing arrives either.
# CLIENT_RE_QUEUE.md is named here explicitly because a standing prompt on
# this machine used to tell its worker to fill in a `### result:` field in that
# file and let this script carry it; it cannot, and the first round that actually
# reached that step would have deadlocked every lane's pull, not just that
# worker's own (pf_bridge/notes_to_chief/20260902_0215_KA1B-TO-CHIEF-codex-cannot-
# take-an-re-ticket-three-causes-not-one.md, cause 3).  All three queues are
# editable from a cloud clone through a PR and from nowhere else.
#
# WHAT IT REFUSES: deletions, files over 2 MB, proprietary extensions and names,
# anything outside the allowlist, --force, reset, clean, stash, checkout, restore,
# add -A, commit -a, editing .gitignore, running pytest or the gate, and starting
# or stopping the server or the game.  Out of script means stop and shout, never
# repair - the same rule the watchdog follows when it fails to kill a frozen bridge.
#
# TWO BUGS THIS FILE IS BUILT AROUND, both measured on this machine:
#  - PS 5.1 Out-File -Encoding utf8 writes a BOM.  LOCK_GIT.txt carried one, and
#    the guard $firstLine -cmatch '^HELD:' in done\169_*.ps1:83 therefore failed to
#    match WHILE THE FLAG WAS HELD.  Every flag read here strips U+FEFF first, and
#    every write in this file uses -Encoding ascii.
#  - A character outside cp874 in console output turns the gate red on Windows only
#    (round 86).  Everything that reaches sync.log passes through AsciiSafe first,
#    including git's own output, which may carry Thai from a chief commit message.
#
# MODES
#   (no switch)  the real thing: pull, commit the allowlist, push, pull the server
#   -DryRun      fetches and reports, but never merges, commits, pushes or writes
#                the real heartbeat.  Safe to run while someone else is working.
#   -SelfCheck   guards and a receipt only.  Touches no network and no index.
#   -NoServer    skip step [5] entirely (used by the self test harness)
#   -BridgeRepo / -ServerRepo  point at scratch clones instead of the real ones,
#                which is how pf_git_sync_selftest.ps1 proves the refusals without
#                going anywhere near GitHub.
#
# EXIT CODES
#   0  round completed, or deliberately skipped (flag held, index.lock, offline)
#   2  .gitignore no longer ignores all three flags - PERMANENT HALT
#   3  SYNC_NEEDS_HUMAN.txt exists - halted until a human deletes it
#   4  bridge pull blocked by local modifications to chief-owned files
#   5  commit refused by a content guard (deletion, size, proprietary)
#   6  push failed and one rebase did not fix it
#   7  rebase conflicted - PERMANENT HALT, the disjoint-write-sets rule has broken
#   9  bad invocation (missing repo, git not found)

param(
    [string]$BridgeRepo = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge',
    [string]$ServerRepo = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject',
    [string]$Branch     = 'main',
    [switch]$DryRun,
    [switch]$SelfCheck,
    [switch]$NoServer
)

$ErrorActionPreference = 'Continue'

# A credential prompt inside a hidden scheduled task hangs forever and nobody sees
# it.  Fail fast instead; a failed push is a line in the log, a wedged one is not.
$env:GIT_TERMINAL_PROMPT = '0'

$SIZE_LIMIT_BYTES  = 2MB
$BAD_EXTENSIONS    = @('.bin', '.sqlite3', '.db', '.pcap', '.exe', '.dll')
$BAD_NAME_PARTS    = @('gameclient', 'capture', 'pirateforce.sqlite')
# --- name-guard waiver (2026-08-24, ruled by Panya) ---------------------------
# BAD_NAME_PARTS is a guess about a file's CONTENT made from its NAME, so it
# misfires on prose: a letter titled '...capture-validated...' is text ABOUT a
# capture, it is not a capture.  notes_to_chief/20260824_1222_BETTER-PLAN-use-
# the-29-capture-validated-messages-not-static-only.md was refused 74 cycles in
# a row and could never reach the chief, and renaming it is not an option
# because sync refuses any commit that carries a deletion.
# Format: '<folder-prefix>/|<lowercase ext>'.  This waives ONLY the name check.
# The extension check and the 2 MB size check still apply to a waived path, and
# every path outside this list still gets the full guard.
# Adding an entry widens what may be committed - Panya rules on each one.
# 2026-08-24 19:2x - Panya ruled the same waiver for the four tool files whose
# names carry 'capture' because they VALIDATE captures, they are not captures.
# Why widening to external/ and staged/ is safe: both live in SHARED_TRACKED,
# which is scanned with --untracked-files=no, so only a file ALREADY IN GIT can
# become a candidate there - a renamed proprietary file dropped in cannot ride
# along.  And GameClient.bin is 14,759,424 bytes, so the 2 MB size check below
# refuses it regardless.  Two independent backstops, neither one waived here.
# 2026-09-01 - Panya ruled the 2026-08-24 waiver extends to the same files when
# they travel under notes_to_chief/ instead of external/.  Background: the Codex
# deliverables are mirrored into notes_to_chief/reference_codex_attr/ because
# external/ cannot carry untracked files; twelve of them carry 'capture' in the
# name and were refused every round, so the team never saw them.  They are the
# SAME class already waived at 'external/|.py': validators and derived tables
# ABOUT captures, not captures.  Checked before widening: every hex run of 64+
# chars in those files is a sha256 digest, and the tables hold protocol ids,
# lengths, dispositions, file paths and hashes - no packet or binary bytes.
# The 2 MB size check and the hard-deny extension block below are untouched and
# still refuse any real capture or binary regardless of this waiver.
$NAME_GUARD_WAIVER = @('notes_to_chief/|.md',
                       'notes_to_chief/|.tsv',
                       'notes_to_chief/|.py',
                       'notes_to_chief/|.json',
                       'external/|.py',
                       'staged/|.py',
                       'staged/|.ps1')
# 'tools_bridge' and 'QUEUE_STATUS_SNAPSHOT.md' added 2026-08-29 (chief R232,
# answering ka3-A's letter 20260829_1919): the tester's queue-status tool
# (pf_queue_status.py, owner-approved) and the snapshot it generates live on
# the bridge but were invisible to git, so the chief could not run or read
# them from a clone.  Both are tester-written, not chief-owned, so the
# ALLOWLIST (which carries untracked files too) is the right list, not
# SHARED_TRACKED.
# 'NOW.md' added 2026-09-01 ~12:5x by ka1-A, at the owner's report that the
# file was invisible on GitHub.  It is the priority-status file that all six
# routine prompts were pointed at that same hour (PANYA-DECISION 20260901_1155):
# writers are the owner and the COO, readers are six cloud routines, which can
# only see what reaches main.  It sits at the bridge root and is UNTRACKED, so
# ALLOWLIST - the list that carries untracked files - is where it belongs,
# exactly like QUEUE_STATUS_SNAPSHOT.md before it.  Without this line the six
# prompts point at a file that exists in no clone and the whole scheme is inert.
# 'LOOSE_ENDS.md' added 2026-09-02 ~10:2x by ka1-A, on Panya's order.  It is the
# register of unfinished things that have no owner and no home in any queue -
# she said plainly that she forgets to chase them, so the ka1-A system-mechanic
# skill re-reads it every time she calls that mode.  It sits at the bridge root
# and is UNTRACKED, so the ALLOWLIST is where it belongs, exactly like NOW.md
# and QUEUE_STATUS_SNAPSHOT.md before it.  Without this line the file exists in
# no clone, the routines cannot read what is outstanding, and the register
# quietly becomes the very thing it was built to prevent.
$ALLOWLIST         = @('notes_to_chief', 'evidence_screens', 'rounds',
                       'tools_bridge', 'QUEUE_STATUS_SNAPSHOT.md', 'NOW.md',
                       'LOOSE_ENDS.md')
# Paths that two parties legitimately write: the chief edits them on main, and the
# assistant or the tester edits them on this disk.  Until 2026-08-24 they were
# tracked but outside the push allowlist, which turned every local edit into a
# one-way deadlock - it could not travel out, and it blocked every pull in.
# sync.log recorded 94 such halts on exactly two files (AGENTS.md 56,
# CHIEF_CONTINUATION.md 40).  Only ALREADY TRACKED and MODIFIED paths are picked
# up from here (the scan below uses --untracked-files=no), so a brand new file
# still cannot ride along, and the proprietary guard still applies to every one.
# Chief-owned single-writer files (CHIEF_CONTINUATION.md and the three queues)
# are deliberately NOT listed: editing them here stays a mistake.
# CANON_SHA.txt is the guard for the canonical DB.  It is written on the bridge
# when the DB is deliberately re-baselined (last time 2026-08-23 15:19 +07:00,
# recorded in notes_to_chief/20260823_1530_gt-results.md) and had sat
# uncommitted for 17 hours because of exactly the deadlock this list fixes.
# The cloud can never see the DB itself, so main's copy is informational; a
# value that travels is strictly better than one that silently rots.
# 'staged' added 2026-08-24 10:5x: the tester writes reusable job templates there
# (TEMPLATE_video_recorder.ps1, TEMPLATE_teardown_generic.ps1).  Leaving it out made
# a modified template a permanently dirty tracked file, which blocks every rebase,
# which blocks every push - the same trap this list exists to remove.
$SHARED_TRACKED    = @('AGENTS.md', '.gitignore', 'pf_git_sync.ps1', 'CANON_SHA.txt',
                       'agent_kit', 'external', 'gamedata', 'staged')

$logPath      = Join-Path $BridgeRepo 'sync.log'

# Log rotation.  Added 2026-08-24 ~21:5x, the same hour Panya moved this task
# from a 5-minute to a 2-minute cadence.  Measured before the change: sync.log
# reached 833,786 bytes in the 4.1 days since 2026-08-20 18:30, about 202 KB a
# day, and nothing had ever trimmed it.  At 2 minutes that becomes roughly
# 505 KB a day and still unbounded, so the faster schedule needs this.
# One generation is kept and the older one is overwritten.  The rolled file is
# named sync_prev.log, NOT sync.log.1, because .gitignore ignores '**/*.log' -
# a name ending in .1 would show up as an untracked file in the repo root.
# This runs before the first Log() call, so it uses Write-Output, and it is
# wrapped in try/catch: a log that cannot be rolled must never stop a sync.
$LOG_ROLL_BYTES = 4MB
try {
    if (Test-Path -LiteralPath $logPath) {
        $logLen = (Get-Item -LiteralPath $logPath).Length
        if ($logLen -gt $LOG_ROLL_BYTES) {
            $logPrev = Join-Path $BridgeRepo 'sync_prev.log'
            if (Test-Path -LiteralPath $logPrev) {
                Remove-Item -LiteralPath $logPrev -Force -ErrorAction SilentlyContinue
            }
            Move-Item -LiteralPath $logPath -Destination $logPrev -Force -ErrorAction SilentlyContinue
            Write-Output ('sync.log rolled to sync_prev.log at ' + $logLen + ' bytes')
        }
    }
} catch { }
$hbPath       = Join-Path $BridgeRepo 'sync_last_check.txt'
if ($DryRun) { $hbPath = Join-Path $BridgeRepo 'sync_last_check.dryrun.txt' }
$ordersPath   = Join-Path $BridgeRepo 'NEW_ORDERS.txt'
$haltPath     = Join-Path $BridgeRepo 'SYNC_NEEDS_HUMAN.txt'
$attnPath     = Join-Path $BridgeRepo 'SYNC_ATTENTION.txt'
$lockGamePath = Join-Path $BridgeRepo 'LOCK_GAME.txt'
$lockGitPath  = Join-Path $BridgeRepo 'LOCK_GIT.txt'

$script:Verdict = 'UNKNOWN'
$script:Mode    = if ($SelfCheck) { 'SELFCHECK' } elseif ($DryRun) { 'DRYRUN' } else { 'LIVE' }

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

function AsciiSafe([string]$s) {
    if ($null -eq $s) { return '' }
    # Anything outside printable ASCII becomes '?'.  Tabs and newlines survive.
    return ($s -replace '[^\x09\x0A\x0D\x20-\x7E]', '?')
}

function Stamp() { return (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') }

function Log([string]$step, [string]$msg) {
    $line = AsciiSafe ("$(Stamp)  [$($script:Mode)] $step  $msg")
    Write-Output $line
    try { $line | Out-File -FilePath $logPath -Encoding ascii -Append } catch { }
}

function Shout([string]$step, [string]$msg) {
    Log $step ('SHOUT  ' + $msg)
}

function WriteAsciiFile([string]$path, [string[]]$lines) {
    $safe = @()
    foreach ($l in $lines) { $safe += (AsciiSafe ([string]$l)) }
    $safe | Out-File -FilePath $path -Encoding ascii
}

function GitRun([string]$repo, [string[]]$cmd) {
    $all = @('--no-optional-locks', '-C', $repo) + $cmd
    $raw = & git @all 2>&1
    $code = $LASTEXITCODE
    $text = ''
    if ($null -ne $raw) { $text = (($raw | ForEach-Object { AsciiSafe ([string]$_) }) -join "`n") }
    return [pscustomobject]@{ Code = $code; Out = $text; Cmd = ($cmd -join ' ') }
}

# Read the first line of a flag file with the BOM stripped, because a BOM makes
# '^HELD:' fail to match exactly when the flag IS held - the worst possible time.
# sha256 of one file, or a word that says why there is no sha.  Used by the
# agent-def mirror check in [5b]; deliberately never throws.
function FileSha([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return 'MISSING' }
    try { return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash } catch { return 'ERROR' }
}

function FlagFirstLine([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return '' }
    $first = ''
    try { $first = [string](Get-Content -LiteralPath $path -TotalCount 1 -ErrorAction Stop) } catch { return '' }
    if ($null -eq $first) { return '' }
    $first = $first.TrimStart([char]0xFEFF)
    return $first.Trim()
}

function FlagIsHeld([string]$path) {
    $l = FlagFirstLine $path
    return ($l -cmatch '^HELD:')
}

# porcelain paths are quoted only when they contain something unusual; renames
# arrive as 'old -> new'.  Both shapes are handled so a surprise cannot be read
# as an ordinary filename and silently staged.
function ParsePorcelainPath([string]$rest) {
    $p = $rest
    if ($p -match ' -> ') { $p = ($p -split ' -> ')[-1] }
    $p = $p.Trim()
    if ($p.StartsWith('"') -and $p.EndsWith('"') -and $p.Length -ge 2) {
        $p = $p.Substring(1, $p.Length - 2)
    }
    return $p
}

function Finish([int]$code, [string]$verdict, [string]$note) {
    $script:Verdict = $verdict
    if (-not $SelfCheck) {
        $state = "$(Stamp)  $verdict"
        try { WriteAsciiFile $hbPath @($state) } catch { }
    }
    Log '[7]' ("heartbeat  $verdict  $note")
    Write-Output ''
    Write-Output ('SYNC_MODE=' + $script:Mode)
    Write-Output ('SYNC_VERDICT=' + $verdict)
    Write-Output ('SYNC_EXIT=' + $code)
    exit $code
}

# ---------------------------------------------------------------------------
# [5] stuck-worktree alarm.  Panya approved 2026-09-02 ~01:3x, option (a) of
# ka1-A letter 20260902_0120.
# A stuck server worktree used to be one identical log line every two minutes
# and nothing else.  On 2026-09-01 it sat that way for 90 minutes and nobody
# knew until the owner happened to ask.  More logging does not fix that; the
# fix is ONE letter in the mailbox, which is where the routines and the owner
# actually look.  Written once per episode and then muted until the worktree
# recovers, so it can never become 2-minute spam.
# The state file is named .log on purpose: .gitignore ignores '**/*.log', so
# this local counter can never appear as an untracked file that rides a commit.
# ---------------------------------------------------------------------------
$SERVER_STUCK_ROUNDS_BEFORE_LETTER = 15   # 15 rounds x 2 minutes = about 30 min

function ServerStuckStatePath() {
    return (Join-Path $BridgeRepo 'sync_state_server_stuck.log')
}

function ServerStuckReset() {
    $p = ServerStuckStatePath
    if (Test-Path -LiteralPath $p) {
        try { WriteAsciiFile $p @('0', '0') } catch { }
    }
}

function ServerStuckTick([string[]]$detail) {
    $p = ServerStuckStatePath
    $count = 0
    $alarmed = '0'
    if (Test-Path -LiteralPath $p) {
        try {
            $st = @(Get-Content -LiteralPath $p -ErrorAction Stop)
            if ($st.Count -ge 1) { [void][int]::TryParse(([string]$st[0]).Trim(), [ref]$count) }
            if ($st.Count -ge 2) { $alarmed = ([string]$st[1]).Trim() }
        } catch { }
    }
    $count = $count + 1
    if ($count -ge $SERVER_STUCK_ROUNDS_BEFORE_LETTER -and $alarmed -ne '1' -and (-not $DryRun) -and (-not $SelfCheck)) {
        $name = (Get-Date -Format 'yyyyMMdd_HHmm') + '_SYNC-ALARM-server-worktree-stuck-for-' + $count + '-rounds.md'
        $letter = Join-Path $notesDir $name
        $lines = @()
        $lines += ('# SYNC ALARM - the server worktree has been stuck for ' + $count + ' rounds')
        $lines += ''
        $lines += ('written by pf_git_sync.ps1 step [5] at ' + (Stamp) + ' (machine local time)')
        $lines += 'this letter is written ONCE per episode, then muted until the worktree recovers.'
        $lines += ''
        $lines += '## what is wrong'
        $lines += ''
        $lines += ('    git status --porcelain in the server repo is not empty, so step [5] will')
        $lines += ('    not pull.  It has skipped ' + $count + ' rounds in a row, about ' + ($count * 2) + ' minutes.')
        $lines += ''
        $lines += '## what step [5] saw'
        $lines += ''
        foreach ($d in $detail) { $lines += ('    ' + $d) }
        $lines += ''
        $lines += '## why it matters'
        $lines += ''
        $lines += '    while this lasts the worktree falls further behind origin/main, and the'
        $lines += '    attended boot guard "worktree must be clean" aborts the next test round.'
        $lines += ''
        $lines += '## what to do'
        $lines += ''
        $lines += '    the owner can double-click FIX_SERVER_WORKTREE.bat in the Pirate Force'
        $lines += '    folder.  It proves every dirty file is byte-identical to origin/main'
        $lines += '    before it touches anything, and refuses if any real local work is there.'
        $lines += '    If it refuses, somebody has uncommitted work in the server worktree and'
        $lines += '    a human has to decide what happens to it.'
        $lines += ''
        $lines += '## note'
        $lines += ''
        $lines += '    step [5] self-heals the one case it can prove is safe: every dirty entry'
        $lines += '    is a tracked-modified file AND byte-identical to origin/main.  This'
        $lines += '    letter existing means that self-heal did NOT apply - so this is'
        $lines += '    something else, and it needs eyes.'
        try {
            WriteAsciiFile $letter $lines
            Shout '[5]' ('stuck for ' + $count + ' rounds - wrote ' + $name + ' to the mailbox')
            $alarmed = '1'
        } catch {
            Shout '[5]' 'stuck, and the alarm letter could not be written'
        }
    }
    try { WriteAsciiFile $p @([string]$count, $alarmed) } catch { }
}

# ---------------------------------------------------------------------------
# preflight
# ---------------------------------------------------------------------------

Write-Output ("=== pf_git_sync  " + (Stamp) + "  mode=" + $script:Mode + " ===")

$gitv = & git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output 'FATAL: git not found on PATH'
    exit 9
}
Write-Output ('git: ' + (AsciiSafe ([string]$gitv)))

if (-not (Test-Path -LiteralPath (Join-Path $BridgeRepo '.git'))) {
    Write-Output ("FATAL: not a git repository: " + (AsciiSafe $BridgeRepo))
    exit 9
}

# A previous round decided a human is needed.  Refuse to run until the human
# deletes the file - a halt that heals itself is not a halt.
if ((Test-Path -LiteralPath $haltPath) -and (-not $SelfCheck)) {
    Log '[-]' ('halted: ' + (Split-Path -Leaf $haltPath) + ' exists - delete it to resume')
    Finish 3 'HALTED_NEEDS_HUMAN' 'waiting for a human'
}

# ---------------------------------------------------------------------------
# [0] the flags must still be ignored, or nothing else may happen
# ---------------------------------------------------------------------------

$flagNames = @('LOCK_GAME.txt', 'LOCK_GIT.txt', 'PANYA_PRESENT.txt')
# The verdict is taken from the EXIT CODE of one check-ignore per file, never from
# reading the -v output.  Measured while writing this: `check-ignore -v` prints a
# line for a file that a negation rule has RE-OPENED as well, because verbose mode
# reports the deciding pattern rather than the decision, and that pattern begins
# with '!'.  A guard that only looked for the filename in the output would have
# called an un-ignored flag ignored - the exact failure it exists to prevent.
# -q is silent and answers 0 for ignored, 1 for not ignored, 128 for broken.
$ci = GitRun $BridgeRepo (@('check-ignore', '-v', '--no-index', '--') + $flagNames)
$missing = @()
foreach ($f in $flagNames) {
    $one = GitRun $BridgeRepo @('check-ignore', '-q', '--no-index', '--', $f)
    if ($one.Code -ne 0) { $missing += ($f + ' (check-ignore exit ' + $one.Code + ')') }
}
if ($missing.Count -gt 0) {
    Shout '[0]' ('.gitignore no longer ignores: ' + ($missing -join ' ') + ' - a pull would overwrite a held flag')
    if (-not $SelfCheck) {
        WriteAsciiFile $haltPath @(
            "SYNC HALTED  $(Stamp)"
            ''
            'Reason: .gitignore stopped ignoring one or more flag files:'
            ('  ' + ($missing -join ' '))
            ''
            'Why this stops everything: a flag that travels between machines can be'
            'overwritten by a pull while it is HELD, and the whole flag system then'
            'fails silently, which is worse than having no flags at all.'
            ''
            'Fix the ignore rules, confirm with:'
            '  git check-ignore -v --no-index -- LOCK_GAME.txt LOCK_GIT.txt PANYA_PRESENT.txt'
            'then delete this file.  pf_git_sync.ps1 will not run until it is gone.'
        )
    }
    Finish 2 'HALT_FLAGS_NOT_IGNORED' ($missing -join ' ')
}
Log '[0]' 'flag guard ok - all three flag files are ignored'

# ---------------------------------------------------------------------------
# [1] LOCK_GIT held means a human or a job owns the index right now
# ---------------------------------------------------------------------------

if (FlagIsHeld $lockGitPath) {
    Log '[1]' ('LOCK_GIT is HELD (' + (FlagFirstLine $lockGitPath) + ') - skipping this round, not an error')
    Finish 0 'SKIP_LOCK_GIT_HELD' 'someone owns the index'
}
Log '[1]' 'LOCK_GIT free'

# ---------------------------------------------------------------------------
# [2] a real index.lock means git itself is mid-operation.
#
# HISTORY, so nobody treats the next one as a first occurrence.  A 0-byte
# index.lock has been left in this repo at least SIX times: 2026-08-20 (staged
# jobs 168 and 169 still tell the owner to delete it by hand), 2026-08-31
# twice, 2026-09-02 three times, and 2026-09-02 18:02:37, which blocked every
# round for 74 minutes and held a whole attended round's letters on the disk.
# Five of those were renamed out of the way by the ka1-B session
# (.git\STALE_index.lock.ka1B_*) and never reported, which is exactly why the
# cause was never chased.
#
# WHO CREATES IT is still unknown and this block does not guess.  Windows
# process auditing is off, so nothing on this machine records it.  The 0-byte
# size is the one hard clue: git creates index.lock EMPTY and then writes into
# it, so a process killed between those two steps leaves precisely this.
#
# Three behaviours, approved by the owner 2026-09-02 ~19:30 (+07:00):
#   (1) self-heal, and only under three guards together
#   (2) evidence trap: the first round of an episode records who was running
#   (3) alarm: after N consecutive skips, one letter, then muted
# ---------------------------------------------------------------------------

$INDEX_LOCK_STALE_MIN            = 10
$INDEX_LOCK_ROUNDS_BEFORE_LETTER = 5

function IndexLockStatePath() { return (Join-Path $BridgeRepo 'sync_state_index_lock.log') }

function IndexLockReset() {
    $p = IndexLockStatePath
    if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue }
}

function IndexLockLiveGit() {
    # git-family processes only.  A running git is the one thing that makes
    # deleting the lock dangerous, so this guard must never be softened for
    # convenience.
    return @(Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.ProcessName -in @('git', 'git-remote-https', 'git-remote-http', 'git-lfs', 'gitk') })
}

function IndexLockSnapshot([string]$why, $lockItem) {
    # The trap.  Written once per episode, beside the sync log, never into git:
    # the point is to name the process next time, not to fill the repo.
    $wp = Join-Path $BridgeRepo 'sync_state_index_lock_witness.log'
    $lines = @()
    $lines += '================================================================'
    $lines += ('captured ' + (Stamp) + '   reason: ' + $why)
    if ($lockItem) {
        $lines += ('lock size  : ' + $lockItem.Length + ' bytes')
        $lines += ('lock mtime : ' + $lockItem.LastWriteTime.ToString('yyyy-MM-ddTHH:mm:ss'))
    }
    $lines += 'processes running at this moment (name / pid / started):'
    foreach ($pr in @(Get-Process -ErrorAction SilentlyContinue |
                      Where-Object { $_.ProcessName -match '^(git|gitk|powershell|pwsh|cmd|conhost|py|python|node|GameClient|Code|ssh)' } |
                      Sort-Object ProcessName)) {
        $st = 'unknown'
        try { $st = $pr.StartTime.ToString('yyyy-MM-ddTHH:mm:ss') } catch { $st = 'unknown' }
        $lines += ('    ' + $pr.ProcessName.PadRight(22) + ' pid=' + ([string]$pr.Id).PadRight(8) + ' started ' + $st)
    }
    try { $lines | Out-File -LiteralPath $wp -Encoding utf8 -Append } catch { }
}

function IndexLockTick($lockItem, [int]$ageMin) {
    $p = IndexLockStatePath
    $count = 0
    $alarmed = '0'
    if (Test-Path -LiteralPath $p) {
        try {
            $st = @(Get-Content -LiteralPath $p -ErrorAction Stop)
            if ($st.Count -ge 1) { [void][int]::TryParse(([string]$st[0]).Trim(), [ref]$count) }
            if ($st.Count -ge 2) { $alarmed = ([string]$st[1]).Trim() }
        } catch { }
    }
    if ($count -eq 0) { IndexLockSnapshot 'first round of this index.lock episode' $lockItem }
    $count = $count + 1
    if ($count -ge $INDEX_LOCK_ROUNDS_BEFORE_LETTER -and $alarmed -ne '1' -and (-not $DryRun) -and (-not $SelfCheck)) {
        $nd = Join-Path $BridgeRepo 'notes_to_chief'
        $name = (Get-Date -Format 'yyyyMMdd_HHmm') + '_SYNC-ALARM-index-lock-has-blocked-every-round-for-' + $count + '-rounds.md'
        $lines = @()
        $lines += ('# SYNC ALARM - .git\index.lock has blocked ' + $count + ' rounds in a row')
        $lines += ''
        $lines += ('written by pf_git_sync.ps1 step [2] at ' + (Stamp) + ' (machine local time)')
        $lines += 'one letter per episode, then muted until the lock clears.'
        $lines += ''
        $lines += '## what is wrong'
        $lines += ''
        $lines += '    pf_bridge\.git\index.lock exists, so every step after [2] is skipped:'
        $lines += '    nothing is committed, nothing is pushed, the server repo is not pulled.'
        $lines += ('    ' + $count + ' rounds in a row, about ' + ($count * 2) + ' minutes so far.')
        if ($lockItem) {
            $lines += ('    lock size  : ' + $lockItem.Length + ' bytes')
            $lines += ('    lock mtime : ' + $lockItem.LastWriteTime.ToString('yyyy-MM-ddTHH:mm:ss') + '  (age ' + $ageMin + ' min)')
        }
        $lines += ''
        $lines += '## why the self-heal did not fire'
        $lines += ''
        $lines += '    it needs all three at once: the lock is 0 bytes, it is at least'
        $lines += ('    ' + $INDEX_LOCK_STALE_MIN + ' minutes old, and NO git process is running.')
        $lines += '    A non-empty lock means a git process wrote into it - that is not a stale'
        $lines += '    lock and this script will never delete it.  A human has to look.'
        $lines += ''
        $lines += '## where to look'
        $lines += ''
        $lines += '    sync_state_index_lock_witness.log in this folder lists every process that'
        $lines += '    was running when the episode started.  That file is the trap set for'
        $lines += '    whoever creates these; read it before deleting anything.'
        $lines += ''
        $lines += '## nonclaims'
        $lines += ''
        $lines += '    - this letter does NOT say which process created the lock.  Nothing on'
        $lines += '      this machine records that today; process auditing is off.'
        $lines += '    - a stale lock is not evidence of data loss.  Nothing is lost by the skip'
        $lines += '      itself; the work waits.'
        try {
            $lines | Out-File -LiteralPath (Join-Path $nd $name) -Encoding utf8
            Shout '[2]' ('index.lock alarm letter written: ' + $name)
        } catch {
            Shout '[2]' ('index.lock alarm letter FAILED to write: ' + $_.Exception.Message)
        }
        $alarmed = '1'
    }
    try { @([string]$count, $alarmed) | Out-File -LiteralPath $p -Encoding ascii } catch { }
    return $count
}

$idxLock = Join-Path $BridgeRepo '.git\index.lock'
if (Test-Path -LiteralPath $idxLock) {
    $li = $null
    try { $li = Get-Item -LiteralPath $idxLock -Force -ErrorAction Stop } catch { }
    $ageMin = 0
    if ($li) { $ageMin = [int]((Get-Date) - $li.LastWriteTime).TotalMinutes }
    $liveGit = IndexLockLiveGit
    $sizeOk = ($li -ne $null -and $li.Length -eq 0)
    $ageOk  = ($ageMin -ge $INDEX_LOCK_STALE_MIN)
    $gitOk  = ($liveGit.Count -eq 0)

    if ($sizeOk -and $ageOk -and $gitOk -and (-not $DryRun) -and (-not $SelfCheck)) {
        IndexLockSnapshot 'about to self-heal a stale lock' $li
        Remove-Item -LiteralPath $idxLock -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 200
        if (Test-Path -LiteralPath $idxLock) {
            Shout '[2]' 'stale index.lock could not be removed - skipping this round'
            [void](IndexLockTick $li $ageMin)
            Finish 0 'SKIP_INDEX_LOCK' 'git busy'
        }
        Shout '[2]' ('stale index.lock removed by self-heal: 0 bytes, ' + $ageMin + ' min old, no git process running')
        IndexLockReset
    }
    else {
        $sz = '?'
        if ($li) { $sz = [string]$li.Length }
        Log '[2]' ('index.lock present - size=' + $sz + 'B age=' + $ageMin + 'min gitProcesses=' + $liveGit.Count + ' - not touching it, skipping this round')
        $n = IndexLockTick $li $ageMin
        Log '[2]' ('consecutive index.lock skips: ' + $n)
        Finish 0 'SKIP_INDEX_LOCK' 'git busy'
    }
}
else {
    IndexLockReset
}
Log '[2]' 'no index.lock'

# ---------------------------------------------------------------------------
# snapshot for [6]: what did the tester have before the pull
# ---------------------------------------------------------------------------

$notesDir = Join-Path $BridgeRepo 'notes_to_chief'
$queueFile = Join-Path $BridgeRepo 'GAME_TEST_QUEUE.md'
$beforeOrders = @()
if (Test-Path -LiteralPath $notesDir) {
    $beforeOrders = @(Get-ChildItem -LiteralPath $notesDir -Filter 'FROM_CHIEF_*' -File -ErrorAction SilentlyContinue |
                      ForEach-Object { $_.Name })
}
$beforeQueue = $null
if (Test-Path -LiteralPath $queueFile) { $beforeQueue = (Get-Item -LiteralPath $queueFile).LastWriteTimeUtc }
$beforeHead = (GitRun $BridgeRepo @('rev-parse', 'HEAD')).Out.Trim()

# ---------------------------------------------------------------------------
# [2c] bridge heartbeat (COO-DECISION OPS-002, 2026-08-26 05:52 +07:00)
# ---------------------------------------------------------------------------
# Chief runs on the cloud and cannot tell "the bridge is quiet because
# nothing happened" apart from "the bridge is dead" by watching this repo
# alone - that gap let a real 25-minute outage on 2026-08-25 go unnoticed
# until someone happened to look.  This file is the fix: one ASCII line,
# an ISO-8601 timestamp with the machine's REAL offset (zzz format
# specifier, not a hardcoded +07:00 - this machine is expected to sit in
# Thailand, but hardcoding the string would silently mislabel every
# heartbeat if that ever stops being true, with no visible symptom),
# refreshed here so it rides out inside the same
# allowlist commit as everything else this round (notesDir is already in
# $ALLOWLIST, so no allowlist change is needed).  Sync itself keeps waking
# every 2 minutes as before; only the FILE write is throttled to once per
# 15 minutes, so a healthy bridge does not flood history with empty-content
# commits.  COO's read rule once this file exists: missing, or older than
# 30 minutes, means the bridge is dead - say so immediately, do not wait for
# the old 3-hour rule (that rule is what let the 25-minute outage hide).
# Skipped under -SelfCheck / -DryRun on purpose: a check run must not create
# a commit nothing else can reproduce.  Written with the plain WriteAsciiFile
# helper below, NOT the try/finally + atomic-write pattern the AGENTS.md
# ABORT rule (chief R175) requires for CANON_SHA.txt/LOCK_*.txt: this file is
# an observability signal only, nothing reads it to decide whether to boot,
# so a torn write here cannot cascade into another job's teardown failing -
# the exact harm that rule exists to prevent.
$heartbeatFile = Join-Path $notesDir '_BRIDGE_HEARTBEAT.txt'
if (-not $SelfCheck -and -not $DryRun) {
    $heartbeatStale = $true
    if (Test-Path -LiteralPath $heartbeatFile) {
        $hbAgeMin = (New-TimeSpan -Start (Get-Item -LiteralPath $heartbeatFile).LastWriteTime -End (Get-Date)).TotalMinutes
        if ($hbAgeMin -lt 15) { $heartbeatStale = $false }
    }
    if ($heartbeatStale) {
        $hbStamp = Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'
        $hbHead = $beforeHead.Substring(0, [Math]::Min(7, $beforeHead.Length))
        WriteAsciiFile $heartbeatFile @($hbStamp + '  pf_git_sync woke and finished a round, HEAD ' + $hbHead)
        Log '[2c]' ('heartbeat refreshed: ' + $hbStamp)
    } else {
        Log '[2c]' 'heartbeat still fresh (< 15 min), not rewriting'
    }
}

# ---------------------------------------------------------------------------
# candidate scan - shared by SelfCheck, DryRun and the real run
# ---------------------------------------------------------------------------

$st = GitRun $BridgeRepo (@('status', '--porcelain', '--untracked-files=all', '--') + $ALLOWLIST)
$candidates = @()
$deletions  = @()
foreach ($line in ($st.Out -split "`n")) {
    if ($line.Trim().Length -lt 4) { continue }
    $xy = $line.Substring(0, 2)
    $path = ParsePorcelainPath $line.Substring(3)
    if ($path.Length -eq 0) { continue }
    if ($xy -match 'D' -or $xy -match 'R') { $deletions += ($xy.Trim() + ' ' + $path); continue }
    $candidates += $path
}

# Modified tracked files in the shared paths.  --untracked-files=no is the whole
# safety argument: a file that is not already in git cannot appear here, so this
# widens what can be UPDATED without widening what can be INTRODUCED.
$stShared = GitRun $BridgeRepo (@('status', '--porcelain', '--untracked-files=no', '--') + $SHARED_TRACKED)
foreach ($line in ($stShared.Out -split "`n")) {
    if ($line.Trim().Length -lt 4) { continue }
    $xy = $line.Substring(0, 2)
    $path = ParsePorcelainPath $line.Substring(3)
    if ($path.Length -eq 0) { continue }
    if ($xy -match 'D' -or $xy -match 'R') { $deletions += ($xy.Trim() + ' ' + $path); continue }
    if ($candidates -notcontains $path) { $candidates += $path }
}

$refusals = @()
$refusedPaths = @()
foreach ($rel in $candidates) {
    $full = Join-Path $BridgeRepo ($rel -replace '/', '\')
    $leaf = (Split-Path -Leaf $rel).ToLower()
    $ext  = [System.IO.Path]::GetExtension($leaf)
    if ($BAD_EXTENSIONS -contains $ext) { $refusals += ('extension ' + $ext + ' : ' + $rel); $refusedPaths += $rel; continue }
    $hit = $false
    foreach ($part in $BAD_NAME_PARTS) { if ($leaf.Contains($part)) { $hit = $true } }
    if ($hit) {
        foreach ($w in $NAME_GUARD_WAIVER) {
            $wf = ($w -split '\|')[0]
            $wx = ($w -split '\|')[1]
            if ($rel.ToLower().StartsWith($wf) -and $ext -eq $wx) {
                Log '[4]' ('name guard waived - text letter, not a binary : ' + $rel)
                $hit = $false
            }
        }
    }
    if ($hit) { $refusals += ('name looks proprietary : ' + $rel); $refusedPaths += $rel; continue }
    if (Test-Path -LiteralPath $full) {
        $len = (Get-Item -LiteralPath $full).Length
        if ($len -gt $SIZE_LIMIT_BYTES) { $refusals += ('size ' + $len + ' bytes > 2 MB : ' + $rel); $refusedPaths += $rel; continue }
    }
}

Log '[4]' ('candidates=' + $candidates.Count + '  deletions=' + $deletions.Count + '  refusals=' + $refusals.Count)

# ---------------------------------------------------------------------------
# -SelfCheck stops here with a receipt and touches nothing
# ---------------------------------------------------------------------------

if ($SelfCheck) {
    Write-Output ''
    Write-Output '=== SELFCHECK RECEIPT ==='
    Write-Output ('bridge repo : ' + (AsciiSafe $BridgeRepo))
    Write-Output ('server repo : ' + (AsciiSafe $ServerRepo))
    Write-Output ('branch      : ' + $Branch)
    Write-Output ('remote      : ' + (GitRun $BridgeRepo @('remote', 'get-url', 'origin')).Out.Trim())
    Write-Output ('head        : ' + $beforeHead)
    Write-Output ('halt file   : ' + (Test-Path -LiteralPath $haltPath))
    Write-Output ('LOCK_GAME   : ' + (FlagFirstLine $lockGamePath))
    Write-Output ('LOCK_GIT    : ' + (FlagFirstLine $lockGitPath))
    Write-Output 'check-ignore:'
    foreach ($l in ($ci.Out -split "`n")) { Write-Output ('  ' + $l) }
    Write-Output ('candidates  : ' + $candidates.Count)
    foreach ($c in $candidates) { Write-Output ('  + ' + $c) }
    Write-Output ('deletions   : ' + $deletions.Count)
    foreach ($d in $deletions) { Write-Output ('  ! ' + $d) }
    Write-Output ('refusals    : ' + $refusals.Count)
    foreach ($r in $refusals) { Write-Output ('  X ' + $r) }
    $serverDirty = 'n/a'
    if (Test-Path -LiteralPath (Join-Path $ServerRepo '.git')) {
        $sv = GitRun $ServerRepo @('status', '--porcelain')
        $serverDirty = ('' + (@($sv.Out -split "`n" | Where-Object { $_.Trim() -ne '' })).Count + ' dirty path(s)')
    }
    Write-Output ('server      : ' + $serverDirty)
    $v = 'SELFCHECK_OK'
    if ($deletions.Count -gt 0 -or $refusals.Count -gt 0) { $v = 'SELFCHECK_WOULD_REFUSE' }
    Finish 0 $v ('candidates=' + $candidates.Count)
}

# ---------------------------------------------------------------------------
# [3] bridge pull - fast forward only, because it is the loudest thing that
#     can happen and loud is the whole point
# ---------------------------------------------------------------------------

$fetch = GitRun $BridgeRepo @('fetch', 'origin', $Branch)
if ($fetch.Code -ne 0) {
    # Offline, or no credentials.  Neither is an emergency and neither is fixable
    # from here; the next round in five minutes will try again.
    Log '[3]' ('fetch failed (offline or no credentials) - skipping round: ' + ($fetch.Out -replace "`n", ' | '))
    Finish 0 'SKIP_FETCH_FAILED' 'fetch failed'
}

$counts = (GitRun $BridgeRepo @('rev-list', '--left-right', '--count', ('HEAD...origin/' + $Branch))).Out.Trim()
$ahead = 0
$behind = 0
if ($counts -match '^(\d+)\s+(\d+)$') { $ahead = [int]$matches[1]; $behind = [int]$matches[2] }
Log '[3]' ('ahead=' + $ahead + ' behind=' + $behind)

if ($behind -gt 0 -and $ahead -eq 0) {
    if ($DryRun) {
        Log '[3]' 'DRYRUN: would fast-forward the bridge repo'
    } else {
        $mg = GitRun $BridgeRepo @('merge', '--ff-only', ('origin/' + $Branch))
        if ($mg.Code -ne 0) {
            # By design this means a chief-owned file was edited on this machine.
            # Nothing is lost: the edit is still on the disk.  Say so and stop.
            Shout '[3]' ('fast-forward refused - a file the chief owns is modified here: ' + ($mg.Out -replace "`n", ' | '))
            WriteAsciiFile $attnPath @(
                "SYNC NEEDS ATTENTION  $(Stamp)"
                ''
                'git merge --ff-only was refused on the pf_bridge repository.'
                'The usual cause is a locally modified file that the chief owns'
                '(CHIEF_CONTINUATION.md, GAME_TEST_QUEUE.md or CLIENT_RE_QUEUE.md).'
                'Those files are not in the push allowlist on purpose, so local edits'
                'to them can never travel and will block every pull until resolved.'
                'Editing any of the three on this machine is always a mistake, no'
                'matter who asked for it: they are chief-owned and change only'
                'through a pull request from a cloud clone.'
                ''
                'Nothing has been lost.  Your edits are still on the disk.'
                'git said:'
                ($mg.Out)
                ''
                'This file disappears by itself on the first round that succeeds.'
            )
            # Do NOT Finish here.  Pull and push are independent, and Finish used
            # to run before the push block, so the one component that could see
            # the deadlock was the only one that could not report it.  Leave a
            # letter instead: the push below still runs, so the letter travels and
            # the chief sees it on the next round.
            $stuck = Join-Path $notesDir ('SYNC_STUCK_' + (Get-Date -Format 'yyyyMMdd_HHmm') + '.md')
            if (-not (Test-Path -LiteralPath $stuck)) {
                WriteAsciiFile $stuck @(
                    '# SYNC STUCK - the bridge cannot fast-forward'
                    ''
                    ('time   : ' + (Stamp))
                    ('behind : ' + $behind + '    ahead : ' + $ahead)
                    ''
                    'A tracked file the chief owns is modified on the bridge machine.'
                    'Nothing is lost - the edit is still on that disk.  Resolve by'
                    'committing or discarding the file git names below.  The bridge is'
                    'still pushing, which is how this letter reached you.'
                    ''
                    'git said:'
                    ($mg.Out)
                )
                Log '[3]' ('wrote ' + $stuck)
            }
        } else {
            Log '[3]' 'fast-forwarded'
        }
    }
} elseif ($behind -gt 0 -and $ahead -gt 0) {
    Log '[3]' 'diverged - leaving it to the rebase in [4]'
} else {
    Log '[3]' 'already up to date'
}

# ---------------------------------------------------------------------------
# [4] bridge push - allowlist only, explicit adds, no deletions, ever
# ---------------------------------------------------------------------------

# 2026-09-01 ~13:0x - THIRD correction, same shape as the two below, ordered by
# Panya after this branch blacked the bridge out for a full hour (11:18-12:18):
# the Codex mirror routine RENAMED its own marker
# notes_to_chief/reference_codex_attr/.skipped_for_game_lock -> .done.<stamp>,
# which git reports as one deletion, and this branch then refused EVERY commit
# every 2 minutes.  35 candidates piled up - letters, round files and NOW.md,
# the file all six routine prompts had just been pointed at - and nothing from
# the bridge reached main while every surface still looked healthy.
#
# A deletion still never gets committed.  That invariant does NOT live here and
# never did: deleted paths go to $deletions and never enter $candidates, the
# index is rebuilt with read-tree HEAD, every path is added explicitly BY NAME,
# and the staged tree is re-checked for ^D below with REFUSED_STAGED_DELETION
# aborting the round if one ever appears.  This block only decided whether one
# skipped path may also cancel everything CLEAN standing beside it.  The answer
# is the same one already ruled for the size/proprietary guard directly below,
# on 2026-08-24, in that block's own words: 'Skipping ONLY the offending paths
# is strictly safer - the bad file still never reaches the remote and everything
# clean keeps moving.  The guard is per-file, so per-file is honest.'
#
# KNOWN AND ACCEPTED: for a rename, the new name commits while the old name
# stays on main, so main briefly carries both.  That is a visible duplicate, not
# data loss, and it self-heals when a human commits the deletion deliberately.
# RESIDUAL, deliberately not changed in the same edit: the SelfCheck verdict
# above still reports SELFCHECK_WOULD_REFUSE when only a deletion is present.
# That is now pessimistic rather than wrong, and it has consumers this edit did
# not audit - chief should judge it separately.
$deletionsSkipped = 0
if ($deletions.Count -gt 0) {
    $deletionsSkipped = $deletions.Count
    Shout '[4]' ('skipping ' + $deletions.Count + ' deletion/rename(s) inside the allowlist - everything clean still commits')
    foreach ($d in $deletions) { Log '[4]' ('  ! ' + $d) }
    Log '[4]' 'a deletion is never committed by this script.  Move the file back, or let a human commit it deliberately.'
}

# A file that fails the guard cancels the COMMIT.  It must not cancel the ROUND:
# on 2026-08-24 one oversized round video in evidence_screens/ stopped the push
# for every already-committed letter as well, and the bridge went silent.
# 2026-08-24 10:5x - second correction.  The first version cancelled the WHOLE
# commit when any file failed the guard.  That looked safe but deadlocked the
# bridge one layer deeper: a single 3 MB screenshot stopped AGENTS.md, gamedata and
# CANON_SHA.txt from committing, they stayed modified, a modified tracked file
# blocks git rebase, and a blocked rebase blocks every push.  Skipping ONLY the
# offending paths is strictly safer - the bad file still never reaches the remote
# and everything clean keeps moving.  The guard is per-file, so per-file is honest.
if ($refusals.Count -gt 0) {
    Shout '[4]' ('skipping ' + $refusals.Count + ' file(s) that failed the proprietary guard - the rest still commit')
    foreach ($r in $refusals) { Log '[4]' ('  X ' + $r) }
    $candidates = @($candidates | Where-Object { $refusedPaths -notcontains $_ })
    Log '[4]' ('candidates after the guard: ' + $candidates.Count)
}

$committed = 0
if ($candidates.Count -gt 0) {
    if ($DryRun) {
        Log '[4]' ('DRYRUN: would stage and commit ' + $candidates.Count + ' file(s)')
        foreach ($c in $candidates) { Log '[4]' ('  + ' + $c) }
    } else {
        # read-tree HEAD makes the index exactly HEAD without touching the working
        # tree, so nothing anyone left staged can ride along.  Then every path is
        # named explicitly - add -A is forbidden here.
        $rt = GitRun $BridgeRepo @('read-tree', 'HEAD')
        if ($rt.Code -ne 0) {
            Shout '[4]' ('read-tree failed: ' + $rt.Out)
            Finish 5 'REFUSED_READTREE_FAILED' 'read-tree'
        }
        foreach ($c in $candidates) {
            $ad = GitRun $BridgeRepo @('add', '--', $c)
            if ($ad.Code -ne 0) { Shout '[4]' ('add failed for ' + $c + ': ' + $ad.Out) }
        }
        $staged = GitRun $BridgeRepo @('diff', '--cached', '--name-status')
        $stagedLines = @($staged.Out -split "`n" | Where-Object { $_.Trim() -ne '' })
        $stagedDel = @($stagedLines | Where-Object { $_ -cmatch '^D' })
        if ($stagedDel.Count -gt 0) {
            Shout '[4]' ('the index contains ' + $stagedDel.Count + ' deletion(s) after an explicit add - aborting')
            GitRun $BridgeRepo @('read-tree', 'HEAD') | Out-Null
            Finish 5 'REFUSED_STAGED_DELETION' 'staged deletion'
        }
        if ($stagedLines.Count -ne $candidates.Count) {
            # Not fatal: git may consider a file unchanged.  But the numbers are
            # printed side by side so a silent mismatch cannot pass unnoticed.
            Log '[4]' ('note: staged ' + $stagedLines.Count + ' path(s) for ' + $candidates.Count + ' candidate(s)')
        }
        if ($stagedLines.Count -gt 0) {
            $msg = 'sync: ' + $stagedLines.Count + ' file(s) from the Windows bridge, ' + (Stamp) + ' (pf_git_sync.ps1, allowlist only)'
            $cm = GitRun $BridgeRepo @('commit', '-m', $msg)
            if ($cm.Code -ne 0) {
                Shout '[4]' ('commit failed: ' + ($cm.Out -replace "`n", ' | '))
                Finish 5 'REFUSED_COMMIT_FAILED' 'commit'
            }
            $committed = $stagedLines.Count
            Log '[4]' ('committed ' + $committed + ' path(s)')
        } else {
            Log '[4]' 'nothing actually changed - no commit'
        }
    }
} else {
    Log '[4]' 'nothing new under the allowlist'
}

if (-not $DryRun) {
    $counts2 = (GitRun $BridgeRepo @('rev-list', '--left-right', '--count', ('HEAD...origin/' + $Branch))).Out.Trim()
    $ahead2 = 0
    if ($counts2 -match '^(\d+)\s+(\d+)$') { $ahead2 = [int]$matches[1] }
    if ($ahead2 -gt 0) {
        $ps = GitRun $BridgeRepo @('push', 'origin', ($Branch + ':' + $Branch))
        if ($ps.Code -ne 0) {
            $rejected = ($ps.Out -match 'non-fast-forward' -or $ps.Out -match 'rejected' -or $ps.Out -match 'fetch first')
            if (-not $rejected) {
                Shout '[4]' ('push failed and it is not a race: ' + ($ps.Out -replace "`n", ' | '))
                Finish 6 'PUSH_FAILED' 'push error'
            }
            # Losing the race is normal and means only "get in line again".  The
            # local commits touch nothing but new timestamped files, which is why
            # a rebase here is safe by construction and not by luck.
            Log '[4]' 'push rejected as non-fast-forward - the chief got there first; rebasing once'
            GitRun $BridgeRepo @('fetch', 'origin', $Branch) | Out-Null
            $rb = GitRun $BridgeRepo @('rebase', ('origin/' + $Branch))
            if ($rb.Code -ne 0) {
                # A real conflict here is evidence that the disjoint write sets rule
                # has broken.  That is a design failure, not a merge to be resolved
                # by a script at three in the morning.
                GitRun $BridgeRepo @('rebase', '--abort') | Out-Null

                # "cannot rebase: You have unstaged changes" is NOT a conflict.
                # The rebase never started; a tracked file is simply modified and
                # uncommitted.  That is fixed by one git commit, so it must not
                # raise the permanent halt reserved for a real two-machine clash.
                if ($rb.Out -match 'cannot rebase' -and $rb.Out -match 'unstaged changes') {
                    $dirty = (GitRun $BridgeRepo @('status', '--porcelain', '--untracked-files=no')).Out.Trim()
                    Shout '[4]' 'rebase could not start - modified tracked files in the worktree:'
                    foreach ($d in ($dirty -split "`n")) { if ($d.Trim() -ne '') { Log '[4]' ('  ~ ' + $d.Trim()) } }
                    WriteAsciiFile $attnPath @(
                        "SYNC NEEDS ATTENTION  $(Stamp)"
                        ''
                        'The rebase could not START.  This is NOT a content conflict and the'
                        'two-machine assumption has not broken.  A tracked file is modified on'
                        'this machine and was never committed.  Commit it or discard it and the'
                        'next round goes through by itself.  No halt file was written.'
                        ''
                        'modified tracked files:'
                        ($dirty)
                    )
                    Finish 4 'STOP_DIRTY_WORKTREE_BLOCKS_REBASE' 'unstaged changes'
                }

                Shout '[4]' ('rebase conflicted - the disjoint write sets rule has broken: ' + ($rb.Out -replace "`n", ' | '))
                WriteAsciiFile $haltPath @(
                    "SYNC HALTED  $(Stamp)"
                    ''
                    'Reason: git rebase onto origin/' + $Branch + ' conflicted, and the rebase'
                    'was aborted.  Nothing was lost and no commit was discarded.'
                    ''
                    'This is not an ordinary conflict.  This script may only ever commit new'
                    'files under notes_to_chief/ and evidence_screens/, whose names carry'
                    'timestamps, so a conflict means two machines wrote the same thing - the'
                    'assumption the whole two-machine design stands on has broken somewhere.'
                    'A human must look at it and decide, and this script must not guess.'
                    ''
                    'git said:'
                    ($rb.Out)
                    ''
                    'When it is resolved, delete this file to let the sync run again.'
                )
                Finish 7 'HALT_REBASE_CONFLICT' 'rebase conflict'
            }
            $ps2 = GitRun $BridgeRepo @('push', 'origin', ($Branch + ':' + $Branch))
            if ($ps2.Code -ne 0) {
                Shout '[4]' ('push failed again after a clean rebase: ' + ($ps2.Out -replace "`n", ' | '))
                WriteAsciiFile $attnPath @(
                    "SYNC NEEDS ATTENTION  $(Stamp)"
                    ''
                    'The push was rejected, the rebase succeeded, and the second push failed'
                    'as well.  The script stops here rather than looping, because a push that'
                    'keeps losing is either a very busy remote or something structurally wrong,'
                    'and only one of those gets better by trying harder.'
                    ''
                    'git said:'
                    ($ps2.Out)
                )
                Finish 6 'PUSH_FAILED_AFTER_REBASE' 'push twice'
            }
            Log '[4]' 'pushed after one rebase'
        } else {
            Log '[4]' ('pushed ' + $ahead2 + ' commit(s)')
        }
    } else {
        Log '[4]' 'nothing to push'
    }
} else {
    Log '[4]' 'DRYRUN: no push'
}

# ---------------------------------------------------------------------------
# [5] server repo - pull only, and never while the game flag is held
# ---------------------------------------------------------------------------

if ($NoServer) {
    Log '[5]' 'skipped by -NoServer'
} elseif (-not (Test-Path -LiteralPath (Join-Path $ServerRepo '.git'))) {
    Log '[5]' 'server repo not found - skipped'
} elseif (FlagIsHeld $lockGamePath) {
    # This is the promise the design makes to the tester in one line: the code
    # under your feet cannot change in the middle of a test round.
    Log '[5]' 'LOCK_GAME is HELD - not touching the server repo during a test round'
} else {
    $sv = GitRun $ServerRepo @('status', '--porcelain')
    $dirty = @($sv.Out -split "`n" | Where-Object { $_.Trim() -ne '' })
    if ($dirty.Count -gt 0) {
        # -------------------------------------------------------------------
        # Self-heal for the wreck of a fast-forward that died half way.
        # Panya approved 2026-09-02 ~01:3x, option (b) of ka1-A letter 0120.
        #
        # This line was logged on 2026-09-01 23:40:09 and it is the whole story:
        #   [5] server fast-forward refused: error: unable to unlink old
        #       'src/pirateforce_foundation/runtime.py': Invalid argument
        #       | Updating 40010029..ee1877ed
        # git had already written four files with the NEW content, then could
        # not unlink one file, so it stopped.  HEAD unmoved, index unmoved, four
        # tracked files modified.  From the next round on, the dirty check below
        # refused to pull - and the only thing that could have cleared the dirt
        # was the pull it was refusing.  It stayed stuck for 90 minutes, in
        # silence, until a human ran FIX_SERVER_WORKTREE.bat by hand.  Third
        # deadlock of that exact shape in one day: a safety guard that closes
        # its own only exit.
        #
        # The signature of that wreck is exact, and repairing it loses nothing:
        #   * every dirty entry is ' M' - tracked, modified in the worktree,
        #     with a CLEAN index.  Untracked '??', staged 'M ', adds, deletes
        #     and renames disqualify the whole attempt, all of them.
        #   * every one of those paths is byte-identical to origin/<branch>.
        # If both hold, what is on disk is git's own half-written output and
        # belongs to nobody.  If either fails there may be a human's work in
        # there, and we skip exactly as before and never stash.
        # -------------------------------------------------------------------
        $healed = $false
        $shapeOk = $true
        $dpaths = @()
        foreach ($d in $dirty) {
            if ($d.Length -lt 4) { $shapeOk = $false; break }
            if ($d.Substring(0, 2) -cne ' M') { $shapeOk = $false; break }
            $dp = ParsePorcelainPath $d.Substring(3)
            if ($dp -eq '') { $shapeOk = $false; break }
            $dpaths += $dp
        }
        if ($shapeOk -and $dpaths.Count -eq $dirty.Count -and (-not $DryRun)) {
            $hf = GitRun $ServerRepo @('fetch', 'origin', $Branch)
            if ($hf.Code -ne 0) {
                Log '[5]' ('self-heal could not fetch, leaving everything alone: ' + ($hf.Out -replace "`n", ' | '))
            } else {
                $cmp = GitRun $ServerRepo (@('diff', '--numstat', ('origin/' + $Branch), '--') + $dpaths)
                $cmpLines = @($cmp.Out -split "`n" | Where-Object { $_.Trim() -ne '' })
                if ($cmp.Code -eq 0 -and $cmpLines.Count -eq 0) {
                    Shout '[5]' ('all ' + $dirty.Count + ' dirty path(s) are byte-identical to origin/' + $Branch + ' - this is a fast-forward that died half way, not anyone work - restoring them')
                    foreach ($dp in $dpaths) { Log '[5]' ('  ~ ' + $dp) }
                    $co = GitRun $ServerRepo (@('checkout', '--') + $dpaths)
                    if ($co.Code -ne 0) {
                        Shout '[5]' ('self-heal restore failed, leaving everything alone: ' + ($co.Out -replace "`n", ' | '))
                    } else {
                        $sv2 = GitRun $ServerRepo @('status', '--porcelain')
                        $dirty2 = @($sv2.Out -split "`n" | Where-Object { $_.Trim() -ne '' })
                        if ($dirty2.Count -ne 0) {
                            Shout '[5]' ('self-heal left ' + $dirty2.Count + ' path(s) still dirty - stopping before the fast-forward')
                        } else {
                            $sm2 = GitRun $ServerRepo @('merge', '--ff-only', ('origin/' + $Branch))
                            if ($sm2.Code -ne 0) {
                                Shout '[5]' ('self-heal cleaned the worktree but the fast-forward still refused: ' + ($sm2.Out -replace "`n", ' | '))
                            } else {
                                Shout '[5]' 'self-heal complete - worktree clean and fast-forwarded'
                                $healed = $true
                            }
                        }
                    }
                }
            }
        }
        if ($healed) {
            ServerStuckReset
        } else {
            Log '[5]' ('server worktree has ' + $dirty.Count + ' dirty path(s) - skipping, never stashing')
            # Naming the paths costs one line each and saves an hour of hunting.
            # On 2026-09-01 this step printed only the COUNT for 90 minutes and
            # the tester had to place two read-only bridge jobs to learn which
            # four files they were.  The script always knew.
            foreach ($d in $dirty) { Log '[5]' ('  ! ' + $d) }
            ServerStuckTick $dirty
        }
    } elseif ($DryRun) {
        Log '[5]' 'DRYRUN: server worktree clean, would fetch and fast-forward'
    } else {
        $sf = GitRun $ServerRepo @('fetch', 'origin', $Branch)
        if ($sf.Code -ne 0) {
            Log '[5]' ('server fetch failed: ' + ($sf.Out -replace "`n", ' | '))
        } else {
            $sm = GitRun $ServerRepo @('merge', '--ff-only', ('origin/' + $Branch))
            if ($sm.Code -ne 0) {
                # SHOUT, not Log: this is the event that produced the 90-minute
                # silent stall, and it was one quiet line among two hundred.
                Shout '[5]' ('server fast-forward refused: ' + ($sm.Out -replace "`n", ' | '))
                ServerStuckTick @(('fast-forward refused: ' + ($sm.Out -replace "`n", ' | ')))
            } else {
                Log '[5]' 'server repo up to date'
                ServerStuckReset
            }
        }
    }
}

# ---------------------------------------------------------------------------
# [5b] agent-def mirror check.  Panya ruled 2026-08-24 ~21:1x, option (a) of
#      the R148 question 'what forces the agent defs in the two repos to stay
#      byte-identical?'.  Nothing did: the gate is a single-repo checkout, so
#      it cannot see its sibling, and a round that edits one side and forgets
#      the other goes green on both while the two clones run different rules.
#      Drift was already present the day this was written - pf-queue-author.md
#      said 180 minutes on the server side and 420 on the bridge side, stale
#      since 2026-08-20.
#      This step only REPORTS.  It never copies, never commits and never picks
#      a winner: which side is right is a content decision and belongs to a
#      person.  AGENTS.md is deliberately NOT compared - the two AGENTS.md are
#      different documents on purpose.
# ---------------------------------------------------------------------------

$bridgeAgents = Join-Path $BridgeRepo '.claude\agents'
$serverAgents = Join-Path $ServerRepo '.claude\agents'
if ((Test-Path -LiteralPath $bridgeAgents) -and (Test-Path -LiteralPath $serverAgents)) {
    $defNames = @()
    foreach ($f in (Get-ChildItem -LiteralPath $bridgeAgents -Filter '*.md' -File -ErrorAction SilentlyContinue)) {
        if ($defNames -notcontains $f.Name) { $defNames += $f.Name }
    }
    foreach ($f in (Get-ChildItem -LiteralPath $serverAgents -Filter '*.md' -File -ErrorAction SilentlyContinue)) {
        if ($defNames -notcontains $f.Name) { $defNames += $f.Name }
    }
    $defMismatch = @()
    foreach ($n in $defNames) {
        $bh = FileSha (Join-Path $bridgeAgents $n)
        $sh = FileSha (Join-Path $serverAgents $n)
        if ($bh -ne $sh) {
            $bs = $bh.Substring(0, [Math]::Min(12, $bh.Length))
            $ss = $sh.Substring(0, [Math]::Min(12, $sh.Length))
            $defMismatch += ($n + '  bridge=' + $bs + '  server=' + $ss)
        }
    }
    if ($defMismatch.Count -gt 0) {
        Shout '[5b]' ('agent defs DIFFER between the two repos: ' + $defMismatch.Count + ' of ' + $defNames.Count + ' file(s) - a person must decide which side is right')
        foreach ($m in $defMismatch) { Log '[5b]' ('  != ' + $m) }
    } else {
        Log '[5b]' ('agent defs mirror OK - ' + $defNames.Count + ' file(s) identical')
    }
} else {
    Log '[5b]' 'agent defs mirror skipped - one side has no .claude\agents'
}

# ---------------------------------------------------------------------------
# [5c] stuck round-claim detector.  Panya ruled 2026-08-25 ~09:4x after cc lost
#      seven scheduled runs overnight and nobody noticed for six hours.
#      What happened: the 00:51 run took the round lock with an empty commit
#      'round claim: 7ejlam', pushed it, opened the lock PR - and died right
#      there.  Every hourly run after that saw an open claude/* PR, decided a
#      round was already in flight, and backed out.  The runs went green.  The
#      work stopped.  Nothing on this side could tell the difference between
#      'a round is working' and 'a round died holding the lock', because from
#      git both look identical: a claude/* branch whose tip is a bare claim.
#      The one thing that DOES separate them is age.  A healthy round pushes
#      its work within ~40-55 minutes; a dead one sits on the bare claim until
#      cc's own reap closes stale PRs at 6 hours.  So the alert window is
#      exactly between those two numbers - long enough that no live round is
#      ever accused, short enough to save most of the six hours.
#      Outside the window this step stays silent on purpose: under 75 minutes
#      a round is probably just working, and past 6 hours reap has it, plus
#      the branch itself outlives the closed PR forever and would otherwise
#      shout every 2 minutes for the rest of time.
#      This step only REPORTS.  It never closes a PR, deletes a branch or
#      touches the lock - that is a person's call, and mine was wrong once
#      already: last night I called this outage 'cc is down' from this side
#      alone, when the run history said cc ran fine every hour.  This step
#      reports the branch, not the health of cc.  Do not confuse them again.
# ---------------------------------------------------------------------------

$CLAIM_STUCK_MIN = 75
$CLAIM_REAP_MIN  = 360

# ---------------------------------------------------------------------------
# THE SECOND GATE, added 2026-09-02 ~20:0x (+07:00) on the owner's word after
# this step raised its first FALSE ALARM.
#
# What happened: at 19:48 it shouted that claude/gracious-galileo-et2ux4 had
# "died holding the lock", age 90 min, tip "round claim: et2ux4", and told the
# owner a person must close that lock PR.  She asked ka1-A to check first.
# The branch belonged to LANE-GM and it had not died at all: its two pull
# requests were BOTH ALREADY MERGED - #590 at 12:05:33Z and #594 at 12:40:04Z,
# the second one EIGHT MINUTES before the alarm - and the branch itself was
# gone by the time anyone looked.  Had she followed the instruction she would
# have closed the work of a lane that had just finished.
#
# The age test cannot tell those apart, because a finished round leaves the
# same artefact behind: a branch whose tip is still the bare claim commit.
# The thing that separates them is whether a pull request is still OPEN.  So
# this step now asks GitHub before it shouts:
#
#   open PR    -> a round really is holding the lock.  Shout, as before.
#   no open PR -> the round finished, this is only a leftover tip.  Say so
#                 quietly and do NOT ask anyone to close anything.
#   unknown    -> the API could not be reached.  Shout, but say plainly that
#                 the PR state is unverified, so nobody acts on a guess.
#
# The answer is cached per branch for CLAIM_PR_RECHECK_MIN so a 2-minute step
# cannot burn the 60-per-hour unauthenticated rate limit.  Cache lives beside
# the log, never in git.
# ---------------------------------------------------------------------------

$CLAIM_PR_REPOS       = @('panyaasanee/pf_bridge', 'panyaasanee/pirate-force-server')
$CLAIM_PR_RECHECK_MIN = 20

function ClaimPrStatePath() { return (Join-Path $BridgeRepo 'sync_state_claim_pr.log') }

function ClaimPrCacheRead() {
    $h = @{}
    $p = ClaimPrStatePath
    if (Test-Path -LiteralPath $p) {
        try {
            foreach ($l in @(Get-Content -LiteralPath $p -ErrorAction Stop)) {
                $bits = $l -split '\|'
                if ($bits.Count -ge 3) { $h[$bits[0]] = @{ 'when' = [int64]$bits[1]; 'verdict' = $bits[2] } }
            }
        } catch { }
    }
    return $h
}

function ClaimPrCacheWrite($cache) {
    $p = ClaimPrStatePath
    $out = @()
    foreach ($k in $cache.Keys) { $out += ($k + '|' + $cache[$k]['when'] + '|' + $cache[$k]['verdict']) }
    try { $out | Out-File -LiteralPath $p -Encoding ascii } catch { }
}

function ClaimOpenPrVerdict([string]$branchShort) {
    # branchShort is 'claude/xxx' with the origin/ prefix already stripped.
    # Returns 'open', 'none' or 'unknown'.  Never throws: this is a guard on a
    # guard, and it must not be able to break the round it runs inside.
    $allOk = $true
    foreach ($repo in $CLAIM_PR_REPOS) {
        $url = 'https://api.github.com/repos/' + $repo + '/pulls?state=open&per_page=100'
        $r = $null
        try {
            $r = Invoke-RestMethod -Uri $url -Headers @{ 'User-Agent' = 'pf-git-sync' } -TimeoutSec 25
        } catch {
            $allOk = $false
            continue
        }
        if ($r -eq $null) { $allOk = $false; continue }
        foreach ($pr in @($r)) {
            if ($pr.head -ne $null -and $pr.head.ref -eq $branchShort) { return 'open' }
        }
    }
    if ($allOk) { return 'none' }
    return 'unknown'
}

$cf = GitRun $BridgeRepo @('fetch', 'origin', '--prune', '+refs/heads/claude/*:refs/remotes/origin/claude/*')
if ($cf.Code -ne 0) {
    Log '[5c]' ('round-claim check skipped - fetch of claude/* failed: ' + ($cf.Out -replace "`n", ' | '))
} else {
    $nowUtc = [int64](((Get-Date).ToUniversalTime() - [DateTime]'1970-01-01').TotalSeconds)
    $cr = GitRun $BridgeRepo @('for-each-ref', '--format=%(refname:short)|%(committerdate:unix)|%(contents:subject)', 'refs/remotes/origin/claude/*')
    $claimStuck = @()
    $claimLive  = 0
    if ($cr.Code -eq 0 -and $cr.Out -ne '') {
        foreach ($line in ($cr.Out -split "`n")) {
            $parts = $line -split '\|'
            if ($parts.Count -lt 3) { continue }
            if ($parts[2] -notlike 'round claim:*') { continue }
            $ageMin = [int](($nowUtc - [int64]$parts[1]) / 60)
            if ($ageMin -lt $CLAIM_STUCK_MIN) { $claimLive++; continue }
            if ($ageMin -ge $CLAIM_REAP_MIN) { continue }
            $claimStuck += ($parts[0] + '  age=' + $ageMin + 'min  tip="' + $parts[2] + '"')
        }
    }
    if ($claimStuck.Count -gt 0) {
        # SECOND GATE: a bare claim tip is only a stuck lock while a pull
        # request is still open.  See the block above for the false alarm that
        # put this here.
        $cache = ClaimPrCacheRead
        $reallyStuck = @()
        $leftover    = @()
        $unverified  = @()
        foreach ($c in $claimStuck) {
            $refShort = ($c -split '\s+')[0]
            $branch = $refShort -replace '^origin/', ''
            $verdict = $null
            if ($cache.ContainsKey($branch) -and (($nowUtc - $cache[$branch]['when']) -lt ($CLAIM_PR_RECHECK_MIN * 60))) {
                $verdict = $cache[$branch]['verdict']
            }
            if ($verdict -eq $null) {
                if ($DryRun -or $SelfCheck) { $verdict = 'unknown' }
                else {
                    $verdict = ClaimOpenPrVerdict $branch
                    $cache[$branch] = @{ 'when' = $nowUtc; 'verdict' = $verdict }
                }
            }
            if     ($verdict -eq 'open') { $reallyStuck += ($c + '  openPR=yes') }
            elseif ($verdict -eq 'none') { $leftover    += ($c + '  openPR=no') }
            else                         { $unverified  += ($c + '  openPR=UNVERIFIED') }
        }
        if (-not ($DryRun -or $SelfCheck)) { ClaimPrCacheWrite $cache }

        if ($reallyStuck.Count -gt 0) {
            Shout '[5c]' ('round died holding the lock: ' + $reallyStuck.Count + ' claude/* branch(es) whose tip is still a bare round claim after ' + $CLAIM_STUCK_MIN + ' min AND whose pull request is still OPEN - every scheduled run since then is backing out of a lock nobody is using')
            foreach ($c in $reallyStuck) { Log '[5c]' ('  !! ' + $c) }
            Log '[5c]' 'a person must close that lock PR - this step will not touch it'
        }
        if ($unverified.Count -gt 0) {
            Shout '[5c]' ('' + $unverified.Count + ' bare round claim(s) older than ' + $CLAIM_STUCK_MIN + ' min, and GitHub could NOT be reached to check whether a pull request is still open - do not act on this line alone, check the PR by hand')
            foreach ($c in $unverified) { Log '[5c]' ('  ?? ' + $c) }
        }
        if ($leftover.Count -gt 0) {
            Log '[5c]' ('' + $leftover.Count + ' bare round claim tip(s) with NO open pull request - the round finished and left its claim commit behind, not an alert, nothing to close')
            foreach ($c in $leftover) { Log '[5c]' ('  -- ' + $c) }
        }
    } elseif ($claimLive -gt 0) {
        Log '[5c]' ('round claim held and still young - ' + $claimLive + ' branch(es) under ' + $CLAIM_STUCK_MIN + ' min, not an alert')
    } else {
        Log '[5c]' 'no bare round claim outstanding'
    }
}

# ---------------------------------------------------------------------------
# [5d] closed-but-never-merged pull request watcher.  Panya ruled 2026-09-02
#      ~12:3x, option (kho) of the ka1-A blue-round finding.
#
#      THE FAILURE THIS EXISTS FOR, measured on four real rounds:
#        a round pushes, opens its PR, writes its round file saying "done",
#        and ENDS.  It has no memory and no life after that.  The Windows gate
#        then finishes - minutes later, with nobody left to receive the result
#        - goes RED, and merge-claude-pr.yml closes the pull request.  The
#        branch survives, the work survives, but it never reaches main, and
#        NOTHING tells anyone: the workflow writes its reason as a comment on
#        the pull request itself, which no lane ever reads.
#        server#495 (LANE-DB), #511 (LANE-B), #540 (LANE-B), #545 (LANE-A) all
#        died exactly this way.  Two of the four were one UNDECLARED SKIP on an
#        otherwise fully green gate (#545: 22 of 23 steps green).  Each was
#        found by accident, rounds later, and cost a whole round to re-land.
#
#      So this step turns a silent close into a letter in the mailbox, which is
#      the one channel every lane already reads at the top of every round.
#      It never closes, reopens, merges or edits anything - it only writes.
#
#      COST CONTROL.  The API is called unauthenticated (both repositories are
#      public), which is 60 requests an hour per IP.  This step runs at most
#      once every CLOSED_PR_EVERY_MIN minutes and makes 2 list calls plus at
#      most CLOSED_PR_MAX_LETTERS comment calls, so a bad hour is ~15 calls.
#      The state file is named .log on purpose: .gitignore ignores '**/*.log',
#      so this local ledger can never ride along in a commit.
#
#      FIRST RUN IS SILENT.  With no state file, the currently-closed pull
#      requests are recorded WITHOUT writing letters - otherwise the first tick
#      would dump a letter for every PR that ever died.  Only closures seen
#      after that produce a letter.
# ---------------------------------------------------------------------------

$CLOSED_PR_EVERY_MIN    = 10
$CLOSED_PR_MAX_LETTERS  = 3
# CATCH-UP.  Panya turns this machine off, sometimes for a long time, and asked
# that nothing be lost by that.  A normal tick reads the 20 most recently closed
# pull requests, which is plenty at ~25 closures a day - but after the machine
# has been off for hours those 20 can all be newer than the closures that
# happened while it slept, and a silently closed round would scroll off the
# window and never get its letter.  So the first tick after a gap of
# CLOSED_PR_CATCHUP_MIN minutes reads a much deeper page and is allowed more
# letters in that one round.  Costs at most a handful of extra API calls, once,
# on the tick after the machine wakes.
$CLOSED_PR_CATCHUP_MIN  = 45
$CLOSED_PR_PAGE_NORMAL  = 20
$CLOSED_PR_PAGE_CATCHUP = 100
$CLOSED_PR_MAX_CATCHUP  = 12
$CLOSED_PR_REPOS        = @('panyaasanee/pirate-force-server', 'panyaasanee/pf_bridge')

function ClosedPrStatePath() { return (Join-Path $BridgeRepo 'sync_state_closed_prs.log') }

function GhJson([string]$url) {
    try {
        return Invoke-RestMethod -Uri $url -Headers @{ 'User-Agent' = 'pf-git-sync' } -TimeoutSec 25
    } catch {
        return $null
    }
}

function LaneFromTitle([string]$title) {
    if ($title -match '^\s*\[([A-Za-z0-9\-]+)\]') { return $Matches[1].ToUpper() }
    return 'chief'
}

if ($DryRun -or $SelfCheck -or $NoServer) {
    Log '[5d]' 'closed-PR watcher skipped in this mode'
} else {
    $cpState = ClosedPrStatePath
    $seen = @{}
    $firstRun = $true
    $lastCheck = 0
    if (Test-Path -LiteralPath $cpState) {
        $firstRun = $false
        try {
            $lines = @(Get-Content -LiteralPath $cpState -ErrorAction Stop)
            foreach ($l in $lines) {
                $t = ([string]$l).Trim()
                if ($t -eq '') { continue }
                if ($t -like 'last=*') { [void][int64]::TryParse($t.Substring(5), [ref]$lastCheck); continue }
                $seen[$t] = $true
            }
        } catch { }
    }
    $nowSec = [int64](((Get-Date).ToUniversalTime() - [DateTime]'1970-01-01').TotalSeconds)
    $gapMin = 0
    if ($lastCheck -gt 0) { $gapMin = [int](($nowSec - $lastCheck) / 60) }
    $catchUp = ($lastCheck -gt 0 -and $gapMin -ge $CLOSED_PR_CATCHUP_MIN)
    $prPage    = $CLOSED_PR_PAGE_NORMAL
    $prMaxLetters = $CLOSED_PR_MAX_LETTERS
    if ($catchUp) {
        $prPage = $CLOSED_PR_PAGE_CATCHUP
        $prMaxLetters = $CLOSED_PR_MAX_CATCHUP
        Shout '[5d]' ('this machine was away for about ' + $gapMin + ' min - catching up over the last ' + $prPage + ' closed pull requests instead of ' + $CLOSED_PR_PAGE_NORMAL)
    }
    if (-not $firstRun -and ($nowSec - $lastCheck) -lt ($CLOSED_PR_EVERY_MIN * 60)) {
        Log '[5d]' ('checked less than ' + $CLOSED_PR_EVERY_MIN + ' min ago - skipping this round')
    } else {
        $written = 0
        $newIds  = @()
        foreach ($repo in $CLOSED_PR_REPOS) {
            $url = 'https://api.github.com/repos/' + $repo + '/pulls?state=closed&per_page=' + $prPage + '&sort=updated&direction=desc'
            $prs = GhJson $url
            if ($null -eq $prs) { Log '[5d]' ('could not read closed pull requests of ' + $repo + ' - skipped, not an error'); continue }
            foreach ($pr in @($prs)) {
                if ($null -ne $pr.merged_at) { continue }
                $ref = [string]$pr.head.ref
                if ($ref -notlike 'claude/*') { continue }
                $key = $repo + '#' + $pr.number
                if ($seen.ContainsKey($key)) { continue }
                $newIds += $key
                if ($firstRun) { continue }
                if ($written -ge $prMaxLetters) { continue }

                $lane   = LaneFromTitle ([string]$pr.title)
                $reason = ''
                $cm = GhJson ('https://api.github.com/repos/' + $repo + '/issues/' + $pr.number + '/comments?per_page=5')
                if ($null -ne $cm) {
                    foreach ($c in @($cm)) {
                        $b = [string]$c.body
                        if ($b -ne '') { $reason = $b }
                    }
                }
                if ($reason.Length -gt 900) { $reason = $reason.Substring(0, 900) + ' ...' }

                $name = (Get-Date -Format 'yyyyMMdd_HHmm') + '_SYNC-NOTICE-' + ($repo -replace '.*/', '') + '-pr' + $pr.number + '-closed-never-merged.md'
                $lines = @()
                $lines += ('ADDRESSEE: ' + $lane)
                $lines += ''
                $lines += ('# ' + $repo + ' #' + $pr.number + ' was CLOSED and never merged')
                $lines += ''
                $lines += ('written by pf_git_sync.ps1 step [5d] at ' + (Stamp) + ' (machine local time)')
                $lines += 'this notice is written once per pull request and never repeated.'
                $lines += ''
                $lines += ('    title   : ' + [string]$pr.title)
                $lines += ('    branch  : ' + $ref + '   <- THE WORK IS STILL HERE, nothing was deleted')
                $lines += ('    opened  : ' + [string]$pr.created_at)
                $lines += ('    closed  : ' + [string]$pr.closed_at)
                $lines += ('    link    : ' + [string]$pr.html_url)
                $lines += ''
                $lines += '## why you are reading this'
                $lines += ''
                $lines += '    A round pushes, opens its pull request, writes its round file and ends.'
                $lines += '    The gate finishes minutes later with nobody left to receive the result.'
                $lines += '    If it goes red the pull request is closed, and the only record is a'
                $lines += '    comment on the pull request itself, which no lane reads.  Four rounds'
                $lines += '    died that way before this notice existed (server #495 #511 #540 #545),'
                $lines += '    each found by accident and each costing a whole round to re-land.'
                $lines += ''
                $lines += '## what the closer said'
                $lines += ''
                if ($reason -eq '') {
                    $lines += '    (no comment was left on the pull request - open the link and read the'
                    $lines += '     gate run for this head commit)'
                } else {
                    foreach ($rl in ($reason -split "`n")) { $lines += ('    ' + $rl.TrimEnd()) }
                }
                $lines += ''
                $lines += '## what to do'
                $lines += ''
                $lines += '    1. read the gate log for the head commit and find the ONE step that failed'
                $lines += '    2. fix that cause on the branch above - do not start the round over'
                $lines += '    3. re-open a pull request from the same branch'
                $lines += '    Nothing here is lost.  Re-doing the work from scratch is the expensive'
                $lines += '    mistake this notice exists to prevent.'
                try {
                    WriteAsciiFile (Join-Path $notesDir $name) $lines
                    Shout '[5d]' ('closed and never merged: ' + $key + ' - wrote ' + $name + ' to ' + $lane)
                    $written = $written + 1
                } catch {
                    Shout '[5d]' ('closed and never merged: ' + $key + ' - could not write the letter')
                }
            }
        }
        foreach ($k in $newIds) { $seen[$k] = $true }
        if ($firstRun) {
            Log '[5d]' ('first run - recorded ' + $newIds.Count + ' already-closed pull request(s) silently, no letters')
        } elseif ($newIds.Count -eq 0) {
            Log '[5d]' 'no newly closed pull requests'
        } else {
            Log '[5d]' ('newly closed: ' + $newIds.Count + ' - letters written: ' + $written)
        }
        $out = @('last=' + $nowSec)
        foreach ($k in $seen.Keys) { $out += $k }
        try { WriteAsciiFile $cpState $out } catch { }
    }
}

# ---------------------------------------------------------------------------
# [5e] stale flag release.  Panya ruled 2026-09-02 ~13:3x, after saying plainly
#      that she turns this machine off and sometimes leaves it off a long time.
#
#      THE FAILURE THIS PREVENTS.  A flag is taken by a job or by the attended
#      tester and released at the end of that work.  If the machine dies in the
#      middle - power off, sleep, a killed console - the flag stays HELD with
#      nobody behind it.  On the next boot every sync round reads it and backs
#      out: step [1] skips the whole round on LOCK_GIT, step [5] refuses to
#      touch the server repository on LOCK_GAME.  Nothing recovers on its own,
#      because the only thing that could clear the flag is the round that died.
#      That is the same shape as the three deadlocks already found on
#      2026-09-01/02 (NOW.md, the half-finished fast-forward, the dirty
#      worktree): a guard that closes its own only exit.
#
#      THE TWO FLAGS ARE NOT TREATED THE SAME, ON PURPOSE.
#      * LOCK_GIT guards the git index.  Re-taking it costs nothing and a stale
#        one blocks every round, so age alone is enough to release it.
#      * LOCK_GAME guards a LIVE test round: a running server, an open game
#        window, the canonical database.  Releasing that one while a round is
#        genuinely alive would let the code change under the tester's feet -
#        the exact promise the flag exists to make.  So age is NOT enough:
#        the game client must be gone AND nothing may be listening on the
#        server ports.  If either is still there this step SHOUTS and leaves
#        the flag exactly where it is.
#
#      It writes one letter per release so the change is never silent, and it
#      never touches a flag younger than FLAG_STALE_HOURS.
# ---------------------------------------------------------------------------

$FLAG_STALE_HOURS = 3
$GAME_PORTS       = @(10188, 10189)

function FlagHeldSince([string]$path) {
    $l = FlagFirstLine $path
    if ($l -notmatch '^HELD:\s*(.+)$') { return $null }
    $raw = $Matches[1].Trim()
    try { return [DateTime]::Parse($raw, [Globalization.CultureInfo]::InvariantCulture) } catch { return $null }
}

function ReleaseFlag([string]$path, [string]$name, [int]$ageHours, [string]$why) {
    $stamp = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz', [Globalization.CultureInfo]::InvariantCulture)
    $old = @()
    try { $old = @(Get-Content -LiteralPath $path -ErrorAction Stop) } catch { }
    $new = @()
    $new += ('RELEASED: ' + $stamp)
    $new += 'BY: pf_git_sync.ps1 step [5e] - stale flag release, no human was behind this flag'
    $new += ('done: the flag had been HELD for about ' + $ageHours + ' hours. ' + $why)
    $new += 'note: this script released the flag only. It did not finish, undo or judge whatever work the dead holder was doing.'
    $new += ''
    $new += '----- previous flag history -----'
    foreach ($o in $old) { $new += ([string]$o) }
    try { WriteAsciiFile $path $new } catch { return $false }
    $lines = @()
    $lines += 'ADDRESSEE: chief'
    $lines += ''
    $lines += ('# ' + $name + ' was released automatically after ' + $ageHours + ' hours')
    $lines += ''
    $lines += ('written by pf_git_sync.ps1 step [5e] at ' + (Stamp) + ' (machine local time)')
    $lines += ''
    $lines += ('    flag  : ' + $name)
    $lines += ('    held  : about ' + $ageHours + ' hours, past the ' + $FLAG_STALE_HOURS + '-hour bound')
    $lines += ('    check : ' + $why)
    $lines += ''
    $lines += '## why this happened'
    $lines += ''
    $lines += '    The holder of this flag never released it.  The usual cause is that this'
    $lines += '    machine was switched off, slept, or had its console killed in the middle'
    $lines += '    of the work.  A flag left HELD stops every later sync round, and nothing'
    $lines += '    can clear it except the round that died, so it would have stayed stuck.'
    $lines += ''
    $lines += '## what this step did NOT do'
    $lines += ''
    $lines += '    It released the flag and nothing else.  Whatever the dead holder was in'
    $lines += '    the middle of is still exactly where it was left - no commit, no merge,'
    $lines += '    no cleanup, no judgement.  Someone should look at what that work was.'
    try {
        $ln = (Get-Date -Format 'yyyyMMdd_HHmm') + '_SYNC-NOTICE-' + ($name -replace '\.txt$','') + '-released-after-' + $ageHours + 'h.md'
        WriteAsciiFile (Join-Path $notesDir $ln) $lines
    } catch { }
    return $true
}

if ($DryRun -or $SelfCheck) {
    Log '[5e]' 'stale flag check skipped in this mode'
} else {
    foreach ($fp in @(@($lockGitPath, 'LOCK_GIT.txt'), @($lockGamePath, 'LOCK_GAME.txt'))) {
        $path = $fp[0]; $name = $fp[1]
        if (-not (FlagIsHeld $path)) { continue }
        $since = FlagHeldSince $path
        if ($null -eq $since) { Shout '[5e]' ($name + ' is HELD but its timestamp cannot be read - leaving it alone for a human'); continue }
        $ageH = [int]((Get-Date) - $since).TotalHours
        if ($ageH -lt $FLAG_STALE_HOURS) { Log '[5e]' ($name + ' held ' + $ageH + 'h - young enough, left alone'); continue }
        if ($name -eq 'LOCK_GIT.txt') {
            if (ReleaseFlag $path $name $ageH 'LOCK_GIT guards the git index only; re-taking it is free.') {
                Shout '[5e]' ('released stale ' + $name + ' after ' + $ageH + 'h and wrote a letter')
            } else {
                Shout '[5e]' ('could not release stale ' + $name)
            }
            continue
        }
        $clients = @()
        try { $clients = @(Get-Process -Name 'GameClient*' -ErrorAction SilentlyContinue) } catch { }
        $listening = 0
        foreach ($prt in $GAME_PORTS) {
            try { $listening += @(Get-NetTCPConnection -State Listen -LocalPort $prt -ErrorAction SilentlyContinue).Count } catch { }
        }
        if ($clients.Count -gt 0 -or $listening -gt 0) {
            Shout '[5e]' ($name + ' held ' + $ageH + 'h BUT a round looks alive - GameClient=' + $clients.Count + ' listeners=' + $listening + ' - NOT touching it')
            continue
        }
        if (ReleaseFlag $path $name $ageH 'no GameClient process and nothing listening on the server ports, so no live round was behind it.') {
            Shout '[5e]' ('released stale ' + $name + ' after ' + $ageH + 'h - no game, no listener - and wrote a letter')
        } else {
            Shout '[5e]' ('could not release stale ' + $name)
        }
    }
}

# ---------------------------------------------------------------------------
# [6] tell the tester, but only when there is something to tell - the mtime of
#     NEW_ORDERS.txt is itself the signal, so it must not be touched otherwise
# ---------------------------------------------------------------------------

$afterOrders = @()
if (Test-Path -LiteralPath $notesDir) {
    $afterOrders = @(Get-ChildItem -LiteralPath $notesDir -Filter 'FROM_CHIEF_*' -File -ErrorAction SilentlyContinue |
                     ForEach-Object { $_.Name })
}
$newOrders = @($afterOrders | Where-Object { $beforeOrders -notcontains $_ })
$afterQueue = $null
if (Test-Path -LiteralPath $queueFile) { $afterQueue = (Get-Item -LiteralPath $queueFile).LastWriteTimeUtc }
$queueMoved = ($beforeQueue -ne $afterQueue)
$afterHead = (GitRun $BridgeRepo @('rev-parse', 'HEAD')).Out.Trim()

if ($newOrders.Count -gt 0 -or $queueMoved) {
    $lines = @()
    $lines += ("NEW ORDERS  " + (Stamp))
    $lines += ''
    $lines += 'The sync pulled something the chief wrote.  Read this before you start.'
    $lines += ''
    if ($newOrders.Count -gt 0) {
        $lines += ('New letters in notes_to_chief\ (' + $newOrders.Count + '):')
        foreach ($n in $newOrders) { $lines += ('  ' + $n) }
    } else {
        $lines += 'No new letters.'
    }
    $lines += ''
    if ($queueMoved) { $lines += 'GAME_TEST_QUEUE.md changed - re-read the queue, do not work from memory.' }
    $lines += ''
    if ($beforeHead -ne $afterHead -and $beforeHead -ne '' -and $afterHead -ne '') {
        $lines += ('commits pulled ' + $beforeHead.Substring(0, [math]::Min(7, $beforeHead.Length)) + '..' + $afterHead.Substring(0, [math]::Min(7, $afterHead.Length)) + ':')
        $lg = GitRun $BridgeRepo @('log', '--oneline', '--no-decorate', ($beforeHead + '..' + $afterHead))
        foreach ($l in ($lg.Out -split "`n")) { if ($l.Trim() -ne '') { $lines += ('  ' + $l) } }
    }
    if (-not $DryRun) { WriteAsciiFile $ordersPath $lines }
    Log '[6]' ('NEW_ORDERS.txt written: ' + $newOrders.Count + ' new letter(s), queue moved=' + $queueMoved)
} else {
    Log '[6]' 'nothing new for the tester - NEW_ORDERS.txt left untouched on purpose'
}

# ---------------------------------------------------------------------------
# [6b] LETTERS NOBODY EVER TOOK.  Approved by the owner 2026-09-03 ~10:2x
#      (+07:00) after she asked why two substantive letters were never read.
#
# WHAT WAS MEASURED, AND WHAT WAS NOT
# -----------------------------------
# Two letters from the ka1-B session, 2026-09-01 22:00 and 22:05, addressed to
# LANE-A/LANE-B, were never consumed and never cited by anything later.  Both
# carry findings that matter: one refutes a bounded-negative conclusion about
# actor name colour that four places in src still rely on, the other says
# constructing CActorTask_Dead is not the same as it running.
#
# FOUR CAUSES WERE TESTED AND ALL FOUR FAILED to explain it:
#   addressee - TO-LANE letters are consumed 91% of the time
#   sender    - ka1-B letters are consumed 91% of the time
#   a burst   - that hour held 16 letters and 12 were consumed
#   size      - the 10,838-byte letter five minutes later WAS consumed
# The two sit in the middle of a run of ten, with consumed letters on both
# sides.  There is nothing left to read: the mailbox records that a letter was
# TAKEN, never that one was LOOKED AT AND SKIPPED, so after the fact the
# question is unanswerable by construction.
#
# So this step does not try to find the cause.  It removes the property that
# made the cause matter: a letter nobody takes is now noticed within hours
# instead of never.
#
# WHY THE CITATION TEST IS THE WHOLE TRICK
# ----------------------------------------
# Of 27 letters older than a day and unconsumed, 20 HAD been answered - a
# COO-DECISION replied within minutes in several cases - and only the source
# file was never marked.  Alerting on "unconsumed" alone would have cried wolf
# 20 times out of 27.  A letter that any later letter quotes by its
# yyyymmdd_hhmm stamp has demonstrably been read, whatever the marker says.
# ---------------------------------------------------------------------------

$STALE_LETTER_HOURS      = 12
$STALE_LETTER_MAX_DAYS   = 7
$STALE_LETTER_EVERY_MIN  = 60
# No cap on how many letters the alarm names.  COO-DECISION 20260903_1247
# item 3.  The cost of the cap is not that the reader has to scroll: it is
# that a name the cap swallowed could not be recovered from this script at
# all.  $slSeen below marks every orphan of this run as reported, capped or
# not, so the seven names "... and 7 more" stood for were suppressed from the
# alarm AND from every future alarm in the same breath.  Chief had to re-run
# the whole scan by hand in round R318 to get them back.  Every name, every
# time.
#
# What this costs, said plainly rather than claimed to be free: the alarm
# body grows with the orphan count (~70 KB at 500 names), and
# notes_to_chief/README.md makes every lane read this folder at the start of
# every round, so the length is paid by five readers, not by the bridge.  It
# is still the cheaper side: a name printed once is a name that can be acted
# on, and a name swallowed is gone.
$STALE_LETTER_IGNORE     = @('CODEX-NEWGEN', 'CODEX-CHECKPOINT', 'SYNC-NOTICE',
                             'SYNC-ALARM', '_BRIDGE_HEARTBEAT', 'CONSUMED')

function StaleLetterStatePath() { return (Join-Path $BridgeRepo 'sync_state_stale_letters.log') }

if ($DryRun -or $SelfCheck -or $NoServer) {
    Log '[6b]' 'stale-letter watch skipped in this mode'
} else {
    $slState = StaleLetterStatePath
    $slLast = 0
    $slSeen = @{}
    if (Test-Path -LiteralPath $slState) {
        try {
            $rows = @(Get-Content -LiteralPath $slState -ErrorAction Stop)
            if ($rows.Count -ge 1) { [void][int64]::TryParse(([string]$rows[0]).Trim(), [ref]$slLast) }
            for ($i = 1; $i -lt $rows.Count; $i++) {
                $r = ([string]$rows[$i]).Trim()
                if ($r -ne '') { $slSeen[$r] = $true }
            }
        } catch { }
    }
    $slNow = [int64](((Get-Date).ToUniversalTime() - [DateTime]'1970-01-01').TotalSeconds)
    if (($slNow - $slLast) -lt ($STALE_LETTER_EVERY_MIN * 60)) {
        Log '[6b]' 'stale-letter watch checked less than an hour ago - skipping this round'
    } else {
        $ndir = Join-Path $BridgeRepo 'notes_to_chief'
        $cdir = Join-Path $ndir 'consumed'
        $letters = @(Get-ChildItem -LiteralPath $ndir -Filter '*.md' -File -ErrorAction SilentlyContinue |
                     Where-Object { $_.Name -match '^\d{8}_\d{4}_' } | Sort-Object Name)
        $consumedNames = @{}
        if (Test-Path -LiteralPath $cdir) {
            foreach ($c in @(Get-ChildItem -LiteralPath $cdir -Filter '*.md' -File -ErrorAction SilentlyContinue)) {
                $consumedNames[$c.Name] = $true
            }
        }
        $cutOld = (Get-Date).AddHours(-1 * $STALE_LETTER_HOURS)
        $cutFar = (Get-Date).AddDays(-1 * $STALE_LETTER_MAX_DAYS)
        $cands = @()
        foreach ($f in $letters) {
            if ($f.LastWriteTime -gt $cutOld) { continue }
            if ($f.LastWriteTime -lt $cutFar) { continue }
            if ($consumedNames.ContainsKey($f.Name)) { continue }
            if (Test-Path -LiteralPath ($f.FullName + '.CONSUMED.txt')) { continue }
            if ($slSeen.ContainsKey($f.Name)) { continue }
            $skip = $false
            foreach ($ig in $STALE_LETTER_IGNORE) { if ($f.Name -like ('*' + $ig + '*')) { $skip = $true } }
            if ($skip) { continue }
            $cands += $f
        }
        $orphans = @()
        foreach ($c in $cands) {
            $stamp = $c.Name.Substring(0, 13)
            $citedBy = ''
            foreach ($later in $letters) {
                if ($later.Name -le $c.Name) { continue }
                $body = ''
                try { $body = [IO.File]::ReadAllText($later.FullName) } catch { $body = '' }
                if ($body.Contains($stamp)) { $citedBy = $later.Name; break }
            }
            if ($citedBy -eq '') { $orphans += $c.Name }
        }
        if ($orphans.Count -gt 0) {
            $name = (Get-Date -Format 'yyyyMMdd_HHmm') + '_SYNC-ALARM-' + $orphans.Count + '-letters-nobody-took-and-nobody-answered.md'
            $lines = @()
            $lines += ('# SYNC ALARM - ' + $orphans.Count + ' letter(s) nobody took and nobody answered')
            $lines += ''
            $lines += ('written by pf_git_sync.ps1 step [6b] at ' + (Stamp) + ' (machine local time)')
            $lines += ('Each letter is named ONCE, ever.  This alarm will not repeat for these.')
            $lines += ''
            $lines += '## the test that was applied'
            $lines += ''
            $lines += ('    older than ' + $STALE_LETTER_HOURS + ' h, newer than ' + $STALE_LETTER_MAX_DAYS + ' days')
            $lines += '    AND has no .CONSUMED.txt sibling'
            $lines += '    AND is not present in notes_to_chief\consumed\'
            $lines += '    AND no later letter quotes its yyyymmdd_hhmm stamp anywhere in its body'
            $lines += ''
            $lines += '    The last clause is the important one.  Being unconsumed proves nothing:'
            $lines += '    of 27 unconsumed letters older than a day on 2026-09-03, 20 had in fact'
            $lines += '    been answered and only the source file was never marked.  A letter that'
            $lines += '    nothing later quotes is one that demonstrably reached nobody.'
            $lines += ''
            $lines += '## the letters'
            $lines += ''
            foreach ($o in $orphans) { $lines += ('    ' + $o) }
            $lines += ''
            $lines += '## what to do with this'
            $lines += ''
            $lines += '    Read them, then either act or write one line saying why not.  Marking a'
            $lines += '    letter consumed without reading it defeats the whole check.'
            $lines += ''
            $lines += '## nonclaims'
            $lines += ''
            $lines += '    - this does NOT say the letters are important, only that nothing has'
            $lines += '      referred to them.  A routine notice nobody needed to quote lands here too.'
            $lines += '    - the citation test is a substring match on the stamp.  A reply that'
            $lines += '      answers a letter without quoting its stamp is a false positive.'
            $lines += '    - this step has no idea WHY a letter was skipped, and never will: the'
            $lines += '      mailbox records taking, not looking.'
            try {
                $lines | Out-File -LiteralPath (Join-Path $ndir $name) -Encoding utf8
                Shout '[6b]' ('letters nobody took: ' + $orphans.Count + ' - alarm letter written: ' + $name)
            } catch {
                Shout '[6b]' ('letters nobody took: ' + $orphans.Count + ' - alarm letter FAILED to write: ' + $_.Exception.Message)
            }
            foreach ($o in $orphans) { $slSeen[$o] = $true }
        } else {
            Log '[6b]' ('stale-letter watch: ' + $cands.Count + ' unconsumed candidate(s), all of them cited by a later letter - nothing orphaned')
        }
        $out = @([string]$slNow)
        foreach ($k in $slSeen.Keys) { $out += $k }
        try { $out | Out-File -LiteralPath $slState -Encoding ascii } catch { }
    }
}

# A round that got this far means whatever needed attention is over.
if ((Test-Path -LiteralPath $attnPath) -and (-not $DryRun)) {
    Remove-Item -LiteralPath $attnPath -Force -ErrorAction SilentlyContinue
    Log '[7]' 'cleared SYNC_ATTENTION.txt - the round completed'
}

Finish 0 'OK' ('committed=' + $committed + ' newletters=' + $newOrders.Count + ' deletions_skipped=' + $deletionsSkipped)

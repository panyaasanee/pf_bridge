#!/usr/bin/env python3
"""pf_gate_preflight.py - run the Windows gate's PLATFORM-INDEPENDENT checks
before you push, from any clone, on any OS.  ASCII only, stdlib only.

WHY THIS EXISTS (ka1-A, 2026-09-01, measured).  gate-windows.yml runs on
windows-latest under a DELIBERATELY hostile console: PYTHONIOENCODING
'cp874:strict', PYTHONUTF8 '0', chcp 874.  That is not an accident - it
reproduces Panya's own Thai-locale Windows box, where a character with no
cp874 mapping does not degrade to '?', it raises UnicodeEncodeError inside
print() and kills the tool mid-report.  Every lane, however, verifies on
Linux/UTF-8, where those failures are invisible.  Measured on 2026-09-01:
LANE-DB reported "6651 passed, 0 failed" locally and still lost three PRs in
a row (#495, #503, and the gfkvro round) to the gate; LANE-B reported
"6545 passed, 327 skipped, 0 failed" locally on the branch whose gate went
red four times.  Each miss costs a whole round and a closed PR.

WHAT THIS COVERS (and what it does not).  Two of the three failure shapes
seen that day are pure text properties and reproduce anywhere:
  1. cp874 static tripwire - the same scan the gate runs, same pins.
  2. skip-count drift - the gate pins skipped-test counts; a NEW skip is RED
     in the same way a new failure is.  A test that always skips on CI is
     what killed PR #503.
  3. precondition census - the gate EXCLUDES a whole test module whose text
     names a client artifact, and pins how many it collects.  A module lost
     that way passes both checks above and still turns the gate red on the
     count.  That is what killed #785 and #789 on 2026-09-04, both on
     commits where this tool had already printed PASS twice (added R350,
     COO-DECISION 20260905_0646 item 3).
The remaining shape - a test that genuinely passes on Linux and fails on
Windows - CANNOT be caught here and this script does not pretend to.  For
that, ask for a bridge job on Panya's machine before pushing.

FOURTH CHECK - BRIDGE FILE SIZE CEILINGS (added R359, PANYA-ORDER
20260905_2038 item 1).  Five pf_bridge files are read by every lane, every
round, before it can even claim: GAME_TEST_QUEUE.md, CLIENT_RE_QUEUE.md,
AGENTS.md, CHIEF_CONTINUATION.md, NOW.md.  Measured 2026-09-05: the first had
reached 2.8 MB with 92 of its 153 tickets already closed, the second 925 KB
with 102 of 121 closed, and round `wzdzf7` (LANE-UI) spent 19 minutes just
reading these five files before it could open a claim.  A closed ticket does
not get smaller by staying in the file every lane greps every round; it gets
archived (`archive/*_ARCHIVE_<date>_*.md`, one-line stub left behind) or the
reading cost is paid again forever.  Ceilings are owner-set (NOW.md's own
text names its cap: "12 KB / 60 บรรทัด"), enforced here rather than only in
prose so a lane finds out before push, not after the fact in a letter.

FIFTH AND SIXTH CHECKS - QUEUE GROWTH CAP AND CONSUMED-STUB WARNING (added
R375, COO-DECISION 20260906_1726/1745, chief D11 and LANE-B 20260906_1050).
The fourth check above only turns RED once GAME_TEST_QUEUE.md or
CLIENT_RE_QUEUE.md is ALREADY over its ceiling; with those ceilings just
raised to 2,400,000/409,600 B a single PR could still add hundreds of KB
below that line unnoticed, so check_queue_growth_cap caps how much EITHER
file may grow in one PR, separately from the ceiling. check_consumed_stub_
warning is advisory only: it flags a round file that names a
notes_to_chief/ letter addressed to its own lane with no .CONSUMED.txt
stub on the branch, the exact gap that made LANE-B round `p4ts3e` redo work
round `4tnhzw` had already finished.

THIRD CHECK - PR BODY AUTOMERGE MARKER (added R328, COO-DECISION
20260903_2141).  The reaper that merges our PRs looks for the automerge
marker as a BARE SUBSTRING of the PR body, with no anchor and no line
discipline.  So a body that merely TALKS about the marker - "the marker is
not in this body yet", "I removed the marker" - contains it, and the reaper
merges a round lock or a held PR.  Measured four times: pirate-force-server
#425, #648, #672 and pf_bridge #1015; #672 died before its question ever
reached the COO and #1015 merged carrying only a claim file, dropping that
round's real work off main.  The rule (PROCESS_GATES.md section 20, now also
AGENTS.md section 7) is: the marker string appears in a PR body ONLY as the
real marker line, only when you actually want that PR merged.  This check
enforces it mechanically before you open or PATCH a body.  It never prints
the token it is looking for - tool output gets pasted into round files and
letters, and this script refuses to be the next thing that leaks it.

EXIT CODES: 0 all checks pass; 1 a check is RED; 2 could not run.
"""

import argparse
import os
import pathlib
import re
import subprocess
import sys

# Mirrors gate-windows.yml "cp874 static tripwire (tools/, src/, current/)".
# Keep these in step with that file BY HAND; if they disagree, the workflow is
# the authority and this script is stale - say so in your round file.
CP874_PREFIXES = ("tools/", "src/", "current/")
CP874_ALLOWED = {
    "tools/pf_move_cadence001_headless_replay.py": 0,
    "tools/pf_vital_name_thunk_static.py": 0,
    "tools/pf_vital_thunk_census_static.py": 0,
}


# PANYA-ORDER 20260905_2038 item 1. Bytes on disk, not lines: bytes are what
# a slow read actually costs, and NOW.md's own cap ("12 KB / 60 บรรทัด") is
# the only one of the five stated in both units.
# PANYA-ORDER 20260906_1448 part (a), relayed by ka1-A through the courier
# while the owner's machine was off and accepted as an owner order by
# COO-DECISION 20260906_1546 item 2: the two QUEUE ceilings are raised to the
# owner's own numbers, in bytes, exactly as she wrote them.  The other three
# are untouched by that order and stay where PANYA-ORDER 20260905_2038 put
# them.  The point of the raise is that the two queue files are the ONLY two
# of the five that grow because the project is doing its job (a ticket per
# unit of attended work); the clerk lane (LANE-K) shrinks them by archiving
# closed tickets and by moving bodies over 8,192 B out to `tickets/<id>.md`,
# and that clerk work cannot even START until the `!/tickets/` lines below
# reach main.  The old 300 KB/200 KB pair had therefore become a red that no
# lane could clear and every lane had to carry as KNOWN_RED_MAIN.
BRIDGE_FILE_SIZE_CEILINGS = (
    ("GAME_TEST_QUEUE.md", 2400000),
    ("CLIENT_RE_QUEUE.md", 409600),
    ("AGENTS.md", 30 * 1024),
    ("CHIEF_CONTINUATION.md", 30 * 1024),
    ("NOW.md", 12 * 1024),
)


def _git_blob_size(repo, ref, relname):
    """Size in bytes of `relname` as it exists at `ref`, or None (the ref
    does not resolve, or does not have that path - a new file this branch
    adds, which has no "before" to regress from).
    """
    proc = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), "cat-file", "-s",
         "%s:%s" % (ref, relname)],
        capture_output=True, text=True, errors="replace",
    )
    if proc.returncode != 0:
        return None
    try:
        return int(proc.stdout.strip())
    except ValueError:
        return None


def check_bridge_file_sizes(bridge_root=None, base="origin/main"):
    """RED when THIS BRANCH makes an already-oversized pf_bridge file bigger
    (or pushes a file over its ceiling for the first time) - not merely when
    the file happens to be over ceiling right now.

    pf-adversary, R359: the first cut of this check graded the file's
    absolute on-disk size against the ceiling with no regard for whether the
    branch being checked touched the file at all. Measured against this
    project's own history (AGENTS.md/CHIEF_CONTINUATION.md sitting over
    these same ceilings for days, repeatedly deferred - R338/R347/R350's own
    letters), that shape would fail EVERY lane's mandatory preflight on
    EVERY push, including one that touches none of these five files, for as
    long as the multi-round cleanup runs - which is not bounded. A gate the
    whole team cannot pass stops being a gate and starts being noise lanes
    learn to ignore, which corrodes the other four checks' credibility too.

    So: compare the current size against the same file's size at `base`
    (default `origin/main`, the tree the gate's `pull_request` run actually
    builds - same rationale as `check_base_is_ancestor`). A file already
    over ceiling that this branch left the same size, or shrank, is
    reported but does NOT fail the check - the debt is real and visible,
    just not this branch's to answer for. A file this branch made bigger
    while already over ceiling, or pushed over ceiling for the first time,
    is RED. `bridge_root` defaults to this file's own repository
    (tools_bridge/ lives directly under the pf_bridge root, one parent up) -
    same pattern `check_branch_is_mergeable_by_the_reaper` already uses.

    Returns True (no file both over ceiling and grown vs `base`), False (one
    or more is - RED, every size printed), None (one of the five names does
    not exist under `bridge_root` - this is not the pf_bridge checkout - or
    `base` does not resolve at all, e.g. `git fetch origin main` was never
    run; same INCONCLUSIVE convention as `check_new_skips`).
    """
    root = pathlib.Path(bridge_root) if bridge_root is not None \
        else pathlib.Path(__file__).resolve().parent.parent
    base_resolves = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), "rev-parse",
         "--verify", "--quiet", base + "^{commit}"],
        capture_output=True, text=True, errors="replace",
    ).returncode == 0
    missing, over = [], []
    for name, ceiling in BRIDGE_FILE_SIZE_CEILINGS:
        p = root / name
        if not p.is_file():
            missing.append(name)
            continue
        size = p.stat().st_size
        base_size = _git_blob_size(root, base, name) if base_resolves else None
        if size <= ceiling:
            status, red = "ok ", False
        elif base_size is None:
            # New file over ceiling on day one, or base unresolvable: no
            # "before" to compare against, so the absolute reading stands.
            status, red = "RED", True
        elif size > base_size:
            status, red = "RED", True
        else:
            status, red = "old", False  # over ceiling, not grown - not this branch's
        print("  %s %-24s %9d bytes  (ceiling %9d%s)"
              % (status, name, size, ceiling,
                 ", base %d" % base_size if base_size is not None else ""))
        if red:
            over.append(name)
    if missing:
        print("[bridgesize] INCONCLUSIVE - %s not found under %s."
              % (", ".join(missing), root))
        print("             Is this really the pf_bridge checkout?")
        return None
    if not base_resolves:
        print("[bridgesize] INCONCLUSIVE - %s does not resolve in %s."
              % (base, root))
        print("             git fetch origin main, or pass --base.")
        return None
    if over:
        print("[bridgesize] RED - %d file(s) grew past their ceiling on this"
              % len(over))
        print("             branch (PANYA-ORDER 20260905_2038 item 1;"
              " regression-only, R359 pf-adversary fix).")
        print("             Archive closed tickets to")
        print("             archive/*_ARCHIVE_<date>_*.md with a one-line")
        print("             stub left in place; never delete or move an")
        print("             item that has not been tested yet.")
        return False
    print("[bridgesize] PASS - no file both over its ceiling and grown vs %s"
          " (pre-existing debt, if any, is 'old' above, not this branch's)."
          % base)
    return True


# chief D11, COO-DECISION 20260906_1726 item 3 (answering LANE-E's own
# ASK-COO the same round): check_bridge_file_sizes only turns RED once a
# file is ALREADY over its ceiling. The two queue files' ceilings were just
# raised to 2,400,000 / 409,600 B (PANYA-ORDER 20260906_1448 part (a)),
# which leaves a gap - 397,704 B under CLIENT_RE_QUEUE.md's old debt alone -
# that no per-PR check was watching: two lanes opening tickets at the same
# hour (a routine event, LANE-K's own job every round) could each add
# hundreds of KB and both land clean. This is the second, independent
# criterion COO chose over widening the ceilings themselves, which stay
# Panya's number to move (COO-DECISION 20260906_1345 item 3).
QUEUE_GROWTH_CAP_PER_PR = 50000

#: The two files LANE-K's ticket-per-unit-of-work growth is expected to
#: touch every round - not the other three BRIDGE_FILE_SIZE_CEILINGS names,
#: which only ever shrink through deliberate archiving, never grow as a
#: side effect of normal attended-test throughput.
QUEUE_GROWTH_WATCHED_FILES = ("GAME_TEST_QUEUE.md", "CLIENT_RE_QUEUE.md")


def check_queue_growth_cap(bridge_root=None, base="origin/main"):
    """RED when THIS BRANCH grows GAME_TEST_QUEUE.md or CLIENT_RE_QUEUE.md by
    more than QUEUE_GROWTH_CAP_PER_PR bytes versus `base` - independent of
    whether the file is over its BRIDGE_FILE_SIZE_CEILINGS entry, so a PR
    can be caught here well before that ceiling is anywhere close.
    Shrinking is never capped, by any amount.

    Returns True (both files grew no more than the cap, or shrank, or are
    unchanged), False (one grew past the cap - RED), None (bridge_root is
    not a pf_bridge checkout, or `base` does not resolve - INCONCLUSIVE,
    same convention as check_bridge_file_sizes).
    """
    root = pathlib.Path(bridge_root) if bridge_root is not None \
        else pathlib.Path(__file__).resolve().parent.parent
    base_resolves = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), "rev-parse",
         "--verify", "--quiet", base + "^{commit}"],
        capture_output=True, text=True, errors="replace",
    ).returncode == 0
    missing, over = [], []
    for name in QUEUE_GROWTH_WATCHED_FILES:
        p = root / name
        if not p.is_file():
            missing.append(name)
            continue
        size = p.stat().st_size
        base_size = _git_blob_size(root, base, name) if base_resolves else None
        # A brand-new file has no "before" - its whole size is the growth.
        growth = size if base_size is None else (size - base_size)
        red = growth > QUEUE_GROWTH_CAP_PER_PR
        print("  %s %-20s grew %9d bytes this branch (cap %9d)"
              % ("RED" if red else "ok ", name, growth,
                 QUEUE_GROWTH_CAP_PER_PR))
        if red:
            over.append(name)
    if missing:
        print("[queuegrowth] INCONCLUSIVE - %s not found under %s."
              % (", ".join(missing), root))
        return None
    if not base_resolves:
        print("[queuegrowth] INCONCLUSIVE - %s does not resolve in %s."
              % (base, root))
        print("              git fetch origin main, or pass --base.")
        return None
    if over:
        print("[queuegrowth] RED - %d file(s) grew more than %d B on this"
              " branch vs %s" % (len(over), QUEUE_GROWTH_CAP_PER_PR, base))
        print("              (chief D11, COO-DECISION 20260906_1726 item 3)."
              "  Split into more")
        print("              than one PR, or move the longest ticket bodies"
              " to tickets/<id>.md.")
        return False
    print("[queuegrowth] PASS - neither queue file grew more than %d B on"
          " this branch vs %s." % (QUEUE_GROWTH_CAP_PER_PR, base))
    return True


# LANE-B `20260906_1050` (ASK-COO), accepted as chief's job by
# COO-DECISION 20260906_1148 item 3: round `p4ts3e` re-did work round
# `4tnhzw` had already finished on main, because `4tnhzw` consumed
# COO-DECISION `0748`/`0844` in full but never wrote the `.CONSUMED.txt`
# stub COMMON_LANE_ROUND already requires - so the mailbox kept showing both
# letters as "waiting for you" for the next round of the SAME lane. Advisory
# only, never RED: a round may deliberately consume only part of a letter,
# and text-scanning a round file cannot tell partial from forgotten.
ROUND_FILE_PREFIX_TO_TAG = {
    "A": "LANE-A", "B": "LANE-B", "DB": "LANE-DB", "GM": "LANE-GM",
    "CS": "LANE-CS", "UI": "LANE-UI", "Q": "LANE-Q", "K": "LANE-K",
}

# pf-adversary (round `t0funk`), MEASURED against the real notes_to_chief/
# corpus, not assumed: an exact-string ADDRESSEE match against "LANE-E"
# misses the great majority of letters actually addressed to chief. Real
# spellings in this repository include "chief" (lower-case, the single most
# common one), "CHIEF", "LANE-CHIEF", "chief (LANE-E)", and "LANE-E
# (chief)" - a survey of every ADDRESSEE line in notes_to_chief/*.md this
# round counted 178 chief-addressed letters under some spelling of "chief"
# against 106 under "LANE-E". Matched by SUBSTRING (case-insensitive)
# against the whole ADDRESSEE line, not equality - the same shape
# COMMON_LANE_ROUND section "source of truth" #2 already uses
# (`grep -l "ADDRESSEE: <TAG>"`), which is why it survives a
# comma-separated multi-lane line ("ADDRESSEE: LANE-A, LANE-B (copy: ...)")
# where an exact first-token match does not.
LANE_ADDRESSEE_ALIASES = {
    "LANE-E": ("LANE-E", "CHIEF"),
}

# A letter addressed to every lane is addressed to this one too. Spelled as
# \u escapes to keep this file's own source ASCII, the house rule
# COMMON_LANE_ROUND states for code (this file is outside the gate's cp874
# scan prefixes, but there is no reason to be the one non-ASCII exception).
_UNIVERSAL_ADDRESSEE_MARKERS = (
    "ALL",
    "ทุกสาย",  # thuk saai - "every lane"
    "ทุกคน",  # thuk khon - "everyone"
)


def _addressed_to_own_lane(addressee_line, own_tag):
    """True when a letter's raw ADDRESSEE: line reaches `own_tag`.

    Substring, case-insensitive, against the WHOLE line (not the first
    token) - deliberately generous, for the two reasons above: real
    ADDRESSEE lines are free text ("LANE-UI (owner of ...) - cc chief,
    COO", "LANE-A, LANE-B"), and this check is advisory-only, so a false
    WARN costs a reader one glance while a false PASS defeats the whole
    point (pf-adversary's own finding on the exact-match version this
    replaced).
    """
    text = addressee_line.upper()
    if any(marker.upper() in text for marker in _UNIVERSAL_ADDRESSEE_MARKERS):
        return True
    aliases = LANE_ADDRESSEE_ALIASES.get(own_tag, (own_tag,))
    return any(alias in text for alias in aliases)


# Lane round files: `<PREFIX>_<...>.md` (PREFIX one of the table above).
# Chief round files: `R<N>_<...>.md`, optionally suffixed with a bare
# lowercase letter for a same-round continuation file (`R330b_...`,
# `R341b_...` - real names on main, both missed by the original `R[0-9]+_`
# until pf-adversary measured it against rounds/) - own tag is LANE-E,
# hard-coded below rather than added to the table, since "R" is not a
# claim-PR prefix any lane opens.
_ROUND_FILENAME_RE = re.compile(r"^(?:([A-Z]{1,2})_|R[0-9]+[a-z]?_)")
_LETTER_MENTION_RE = re.compile(r"notes_to_chief/([A-Za-z0-9_.-]+?\.md)\b")
_ADDRESSEE_RE = re.compile(r"^ADDRESSEE:\s*(.+?)\s*$", re.MULTILINE)


def check_consumed_stub_warning(bridge_root=None, base="origin/main"):
    """WARN (print only - never appears in main()'s `results`, so it can
    never make PREFLIGHT RED or INCONCLUSIVE by itself) for every
    notes_to_chief/ letter that a round file NEW on this branch mentions by
    name, is addressed (ADDRESSEE:) to the SAME lane that wrote that round
    file, and has no matching <name>.md.CONSUMED.txt on this branch.

    Returns the number of WARN lines printed (0 means PASS - always a
    non-negative int, never treated as a `results`-list verdict since this
    is advisory only), or None when bridge_root plainly is not a pf_bridge
    checkout (no rounds/ or notes_to_chief/ directory) - the one case this
    prints nothing and signals "could not run".
    """
    root = pathlib.Path(bridge_root) if bridge_root is not None \
        else pathlib.Path(__file__).resolve().parent.parent
    rounds_dir = root / "rounds"
    notes_dir = root / "notes_to_chief"
    if not rounds_dir.is_dir() or not notes_dir.is_dir():
        return None
    base_resolves = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), "rev-parse",
         "--verify", "--quiet", base + "^{commit}"],
        capture_output=True, text=True, errors="replace",
    ).returncode == 0
    if base_resolves:
        diff = subprocess.run(
            ["git", "--no-optional-locks", "-C", str(root), "diff",
             "--name-only", "--diff-filter=A", base, "--", "rounds/"],
            capture_output=True, text=True, errors="replace",
        )
        new_round_files = [line.strip() for line in diff.stdout.splitlines()
                            if line.strip()]
    else:
        # No base to diff against: check every round file present instead -
        # noisier (it can re-warn about a stub an OLDER round already owed)
        # but still correct, and still better than printing nothing.
        new_round_files = sorted(
            "rounds/%s" % p.name for p in rounds_dir.glob("*.md"))
    warned = 0
    for relpath in new_round_files:
        name = pathlib.Path(relpath).name
        if name.endswith("_claim.md"):
            continue
        m = _ROUND_FILENAME_RE.match(name)
        if not m:
            continue
        own_tag = "LANE-E" if m.group(1) is None \
            else ROUND_FILE_PREFIX_TO_TAG.get(m.group(1))
        if own_tag is None:
            continue
        fpath = root / relpath
        if not fpath.is_file():
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for letter_name in sorted(set(_LETTER_MENTION_RE.findall(text))):
            letter_path = notes_dir / letter_name
            if not letter_path.is_file():
                continue
            if (notes_dir / (letter_name + ".CONSUMED.txt")).exists():
                continue
            try:
                letter_text = letter_path.read_text(
                    encoding="utf-8", errors="replace")
            except OSError:
                continue
            addressee = _ADDRESSEE_RE.search(letter_text)
            if not addressee or not _addressed_to_own_lane(
                    addressee.group(1), own_tag):
                continue
            print("[consumedstub] WARN - %s mentions"
                  " notes_to_chief/%s (ADDRESSEE: %s) with no"
                  % (relpath, letter_name, own_tag))
            print("               .CONSUMED.txt stub on this branch. If this"
                  " round really consumed it,")
            print("               add the stub before you push"
                  " (COMMON_LANE_ROUND \"who opens a letter")
            print("               consumes it\"); if not - a deliberate"
                  " partial read - ignore this line.")
            warned += 1
    if warned == 0:
        print("[consumedstub] PASS - no own-lane letter mentioned by a new"
              " round file is missing its .CONSUMED.txt stub.")
    return warned


def _git_blob_text(repo, ref, relname):
    """Text content of `relname` at `ref`, or None (does not resolve there)."""
    proc = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), "show",
         "%s:%s" % (ref, relname)],
        capture_output=True, text=True, errors="replace",
    )
    return proc.stdout if proc.returncode == 0 else None


def _manual_rows(text):
    """The set of raw TSV lines whose source column (index 4) is 'manual'."""
    rows = set()
    for line in (text or "").splitlines():
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) >= 5 and p[4] == "manual":
            rows.add(line)
    return rows


def check_scoreboard_manual_rows(bridge_root=None, base="origin/main",
                                  allow_manual_edit=False):
    """RED when THIS BRANCH adds, edits, or removes a `manual`-source row in
    SCOREBOARD_FACTS.tsv, unless `allow_manual_edit` is set.

    COO-DECISION 20260906_0042 item 1: a `manual` row is the one row shape
    in the scoreboard no lane can derive from its own round file (every
    other row is rebuilt from a `SCOREBOARD:` line and cannot be forged by
    typing a different one), so it is the one row shape a lane or chief must
    not be able to mint or edit either - the same house rule NOW.md already
    states in prose ("'เสร็จ' ติ๊กได้โดย Panya คนเดียว"). Writers of a manual
    row are Panya and ka1-A ONLY (attended, or via a courier PR); every
    other PR - any `[LANE-*]` or `[COO]` head - that diffs a manual row is
    RED, whether it added, changed, or deleted one. Pass
    `--allow-manual-scoreboard-edit` ONLY from a courier PR that is actually
    carrying Panya's or ka1-A's own edit.

    Compares full raw lines (not parsed fields), so a text-only edit to a
    manual row (e.g. changing its sentence) is caught as one removed line
    plus one added line, same as a delete-then-mint would be. `bridge_root`
    defaults to this file's own repository, same convention as
    `check_bridge_file_sizes`.

    Returns True (no manual row differs from `base`, or allow_manual_edit),
    False (a manual row differs and is not allowed - RED), None
    (SCOREBOARD_FACTS.tsv missing here, or `base` does not resolve -
    INCONCLUSIVE, same convention as the other bridge-only checks).
    """
    root = pathlib.Path(bridge_root) if bridge_root is not None \
        else pathlib.Path(__file__).resolve().parent.parent
    tsv_path = root / "SCOREBOARD_FACTS.tsv"
    if not tsv_path.is_file():
        print("[scoreboard-manual] INCONCLUSIVE - SCOREBOARD_FACTS.tsv not "
              "found under %s." % root)
        return None
    base_resolves = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), "rev-parse",
         "--verify", "--quiet", base + "^{commit}"],
        capture_output=True, text=True, errors="replace",
    ).returncode == 0
    if not base_resolves:
        print("[scoreboard-manual] INCONCLUSIVE - %s does not resolve in %s."
              % (base, root))
        return None
    if allow_manual_edit:
        print("[scoreboard-manual] SKIPPED (--allow-manual-scoreboard-edit) "
              "- courier/ka1-A edit, not checked.")
        return True
    current_rows = _manual_rows(
        tsv_path.read_text(encoding="utf-8", errors="replace"))
    base_rows = _manual_rows(_git_blob_text(root, base, "SCOREBOARD_FACTS.tsv"))
    added = current_rows - base_rows
    removed = base_rows - current_rows
    if not added and not removed:
        print("[scoreboard-manual] PASS - no `manual`-source row changed vs %s."
              % base)
        return True
    print("[scoreboard-manual] RED - %d manual row(s) added, %d removed vs %s."
          % (len(added), len(removed), base))
    print("                    Only Panya/ka1-A may write a manual row")
    print("                    (COO-DECISION 20260906_0042, AGENTS.md section 7).")
    for line in sorted(added):
        print("     + %s" % line[:120])
    for line in sorted(removed):
        print("     - %s" % line[:120])
    return False


def tracked_py_files(repo):
    out = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), "ls-files"],
        check=True, capture_output=True, text=True,
    ).stdout.split("\n")
    return [r.strip() for r in out
            if r.strip().endswith(".py")
            and r.strip().startswith(CP874_PREFIXES)]


def check_cp874(repo):
    found, detail, scanned = {}, {}, 0
    for rel in tracked_py_files(repo):
        p = pathlib.Path(repo) / rel
        if not p.is_file():
            continue
        scanned += 1
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for ch in line:
                try:
                    ch.encode("cp874")
                except UnicodeEncodeError:
                    found[rel] = found.get(rel, 0) + 1
                    detail.setdefault(rel, []).append((n, hex(ord(ch))))
    print("[cp874] scanned %d tracked .py files under %s"
          % (scanned, ", ".join(CP874_PREFIXES)))
    if scanned == 0:
        # R297 (chief, pf-adversary finding D5, second half): scanning nothing
        # and printing PASS is the same false green as a check that could not
        # run.  Zero tracked files under src/tools/current means --repo points
        # somewhere that is not the server clone.
        print("[cp874] INCONCLUSIVE - scanned 0 files. Is --repo really the")
        print("        pirate-force-server clone?")
        return None
    bad = []
    for rel in sorted(set(found) | set(CP874_ALLOWED)):
        got, want = found.get(rel, 0), CP874_ALLOWED.get(rel, 0)
        print("  %s %-56s got=%d pinned=%d"
              % ("ok " if got == want else "RED", rel, got, want))
        if got != want:
            bad.append(rel)
            for n, cp in detail.get(rel, [])[:20]:
                print("        line %d: codepoint %s" % (n, cp))
    if bad:
        print("[cp874] RED. A character with no code page 874 mapping raises")
        print("        UnicodeEncodeError inside print() on the bridge console")
        print("        and kills the tool mid-report. Remove it, or raise the")
        print("        pin in .github/workflows/gate-windows.yml in the SAME")
        print("        commit and say why in the round file.")
        return False
    print("[cp874] PASS")
    return True


SKIP_MARKERS = (
    "@unittest.skip",
    "@pytest.mark.skip",
    "self.skipTest",
    "pytest.skip(",
)


def _pinned_design_skip_modules(repo):
    """Module names docs/PYTEST_SKIP_PINS.json's design_skips already covers.

    Round 20260904 recovery (pirate-force-server#694's cause): this check used
    to flag every newly-added skip marker line, with no way to tell a real
    unpinned drift from a skip the SAME commit already declared to
    tools/pf_pytest_precondition_census.py via design_skips. That gap does not
    make the check wrong to run - an added skip is still worth naming before
    push - but it made a properly-pinned skip look identical to an unpinned
    one, and the fix (add the pin) left this advisory RED with no way to
    clear it short of ignoring the tool. A module present here with at least
    one pinned count is a skip this repository already accounts for; it is
    reported below, never silently dropped from the printout.
    """
    import json
    path = pathlib.Path(repo) / "docs" / "PYTEST_SKIP_PINS.json"
    if not path.is_file():
        return set()
    try:
        pins = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    return {
        entry["module"] for entry in pins.get("design_skips", [])
        if int(entry.get("count", 0)) > 0
    }


def check_new_skips(repo, base):
    """Name every skip marker this branch ADDS relative to `base`.

    The gate pins skipped-test counts, so a skip added by this branch is RED
    even though it is green locally. This does not count skips at runtime; it
    names the lines you added, which is what a lane can act on before pushing.
    A line in a module already pinned under design_skips in
    docs/PYTEST_SKIP_PINS.json is reported but does not fail the check on its
    own - that pin is the gate's own record that the skip is declared; an
    unpinned line in any other module still turns this RED.
    """
    try:
        diff = subprocess.run(
            ["git", "--no-optional-locks", "-C", str(repo), "diff",
             "--unified=0", base + "...HEAD", "--", "tests/", "src/", "tools/"],
            check=True, capture_output=True, text=True, errors="replace",
        ).stdout
    except subprocess.CalledProcessError as exc:
        print("[skips] could not diff against %s: %s" % (base, exc))
        return None
    pinned_modules = _pinned_design_skip_modules(repo)
    added = []
    current = None
    for line in diff.split("\n"):
        if line.startswith("+++ b/"):
            current = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            if any(m in line for m in SKIP_MARKERS):
                added.append((current, line[1:].strip()[:110]))
    if not added:
        print("[skips] PASS - no new skip markers vs %s" % base)
        return True
    unpinned = [(f, l) for f, l in added if f not in pinned_modules]
    pinned = [(f, l) for f, l in added if f in pinned_modules]
    if pinned:
        print("[skips] %d new skip marker(s) already pinned under "
              "design_skips in docs/PYTEST_SKIP_PINS.json:" % len(pinned))
        for f, l in pinned:
            print("    %s: %s" % (f, l))
    if unpinned:
        print("[skips] RED - this branch ADDS %d UNPINNED skip marker(s):"
              % len(unpinned))
        for f, l in unpinned:
            print("    %s: %s" % (f, l))
        print("        The gate pins skip counts. A test that always skips on")
        print("        CI reads as a NEW skip and turns the run red - that is")
        print("        what closed PR #503 on 2026-09-01. Make it run, or")
        print("        delete it, or move the pin in the same commit.")
        return False
    print("[skips] PASS - %d new skip marker(s), all pinned" % len(pinned))
    return True


# COO-DECISION 20260906_1846 item 1, answering SYNC_STUCK 20260906_1816:
# AGENTS.md section 7 has said "filenames <= 100 characters, every pile"
# since before this tool existed, but nothing ever checked it mechanically.
# Measured this round against origin/main: notes_to_chief/ alone carries
# 498 files over 140 characters (23 over 200, longest 222), and the real
# cost landed on the bridge, not just as debt: Windows's own filesystem
# refused six of them ("Filename too long"), so pf_git_sync could not
# fast-forward past them at all. Only NEW files (added vs `base`) are
# checked - an old long name already on main is that same debt, real but
# not this branch's to fix by renaming (renaming would be a delete+add on
# the bridge, which pf_git_sync's own contract refuses).
NEW_FILENAME_LENGTH_CEILING = 100


def _basenames_at(root, ref):
    """Every basename tracked at `ref`, as a set.  Empty set on any failure.

    An empty set is the SAFE failure: it exempts nothing, so a broken read
    can only make this check stricter, never let a new long name through.
    """
    listing = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root),
         "-c", "core.quotePath=false", "ls-tree", "-r", "--name-only", ref],
        capture_output=True, text=True, errors="replace",
    )
    if listing.returncode != 0:
        return set()
    return {pathlib.Path(line).name
            for line in listing.stdout.splitlines() if line.strip()}


def _print_inherited_long_names(inherited):
    """An exemption is an OPEN skip: named, counted, never silent.

    AGENTS.md section 7's own rule about skips, applied to this tool: a skip
    with a reason is fine, a silent one is not.  pf-adversary (round
    `l5tqxc`, B1) measured the previous version asserting "none over 100
    characters" in the same breath as it waved a 211-character name through.
    """
    if not inherited:
        return
    longest = max(length for _name, length in inherited)
    print("[filenamelen] SKIPPED (open) - %d path(s) over %d characters whose"
          " basename" % (len(inherited), NEW_FILENAME_LENGTH_CEILING))
    print("              is already on the base branch, so this branch did"
          " not choose it and")
    print("              the owner order forbids renaming it. Longest: %d"
          " characters." % longest)
    for name, length in sorted(inherited, key=lambda row: -row[1])[:10]:
        print("    inherited %d chars: %s" % (length, name))
    if len(inherited) > 10:
        print("    ... and %d more" % (len(inherited) - 10))


def check_new_filename_length(repo, base="origin/main"):
    """RED when this branch ADDS a file whose basename is longer than
    `NEW_FILENAME_LENGTH_CEILING` characters, compared to `base`.

    Character count, not bytes: the ceiling is about what a path component
    costs a filesystem and a terminal to display, not encoding size (unlike
    the byte ceilings `check_bridge_file_sizes`/`check_queue_growth_cap`
    use for file CONTENT, where the cost is bytes read).  `core.quotePath`
    is turned OFF for every git call here for exactly that reason:
    pf-adversary (round `l5tqxc`, B4) measured a 43-character Thai basename
    arriving as 485 characters of octal escape and turning this check RED,
    with the name it printed for the lane to fix unreadable.

    RENAMES COUNT.  `AGENTS.md` section 7 says the rule covers a file
    "added or changed", and a rename is how a long name most naturally
    enters a repo that forbids renaming old ones (an archive sweep, a round
    file given a better name).  pf-adversary (B2) measured `git mv short.md
    <113 chars>.md` passing this check green under the old `--diff-filter=A`.
    The destination path of a rename is what `--name-only` reports, and that
    is the name being introduced.

    A NAME THIS BRANCH DID NOT CHOOSE IS NOT THIS BRANCH'S DEBT.  Any added
    path whose BASENAME already exists somewhere at `base` is a move or a
    copy of an old name, not a new one - the mandated `consumed/` copy of a
    letter, an archive sweep that edits a header as it moves (pf-adversary
    B3 measured 1,300 RED lines from one such sweep, every one of them a
    name that was already on main, with no legal remedy because the owner
    order forbids renaming old files).  The exemption is COUNTED AND NAMED,
    never silent: pf-adversary (B1) measured the old `.CONSUMED.txt`
    exemption passing a 211-character stub under the sentence "none over 100
    characters", which is the band (190-222) that actually stopped the
    bridge on 2026-09-06.  An exemption nobody counts is indistinguishable
    from a check nobody wrote.

    Returns True (no added file over the ceiling), False (one or more are -
    RED, every offending name printed), None (`repo` is not a git checkout,
    or `base` does not resolve - INCONCLUSIVE, same convention as
    `check_new_skips`).
    """
    root = pathlib.Path(repo)
    if not (root / ".git").exists():
        print("[filenamelen] INCONCLUSIVE - %s is not a git checkout." % root)
        return None
    base_resolves = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), "rev-parse",
         "--verify", "--quiet", base + "^{commit}"],
        capture_output=True, text=True, errors="replace",
    ).returncode == 0
    if not base_resolves:
        print("[filenamelen] INCONCLUSIVE - %s does not resolve in %s."
              % (base, root))
        print("              git fetch origin main, or pass --base.")
        return None
    diff = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root),
         "-c", "core.quotePath=false", "diff",
         "--name-only", "--diff-filter=AR", base],
        capture_output=True, text=True, errors="replace",
    )
    added = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    old_basenames = _basenames_at(root, base)
    offenders = []
    inherited = []
    for name in added:
        basename = pathlib.Path(name).name
        if len(basename) <= NEW_FILENAME_LENGTH_CEILING:
            continue
        # A name that already exists at `base` under some path: this branch
        # is moving or copying it, which the owner order requires it to be
        # able to do ("old files must never be renamed").  Counted below,
        # never silently dropped.
        if basename in old_basenames:
            inherited.append((name, len(basename)))
            continue
        # A `.CONSUMED.txt` stub whose underlying letter ALREADY EXISTS at
        # `base`: every lane's stub convention is a fixed
        # `<letter-name>.CONSUMED.txt` suffix, so its length is entirely
        # inherited from a name this branch did not choose and is not
        # allowed to rename (measured against this exact commit, R375: a
        # letter already on main at 89 characters becomes a 102-character
        # stub with no new content in the excess 13). Only the STUB is
        # exempt this way - a `.CONSUMED.txt` name whose own letter is ALSO
        # new on this branch is still this branch's choice end to end.
        if basename.endswith(".CONSUMED.txt"):
            underlying = name[: -len(".CONSUMED.txt")]
            if _git_blob_size(root, base, underlying) is not None:
                inherited.append((name, len(basename)))
                continue
        offenders.append((name, len(basename)))
    if offenders:
        _print_inherited_long_names(inherited)
        print("[filenamelen] RED - %d new file(s) have a basename over %d"
              " characters:" % (len(offenders), NEW_FILENAME_LENGTH_CEILING))
        for name, length in offenders:
            print("    %d chars: %s" % (length, name))
        print("              Shorten the filename before you push - a name")
        print("              already on main is old debt, not this")
        print("              branch's, but this branch must not add a new")
        print("              one (SYNC_STUCK 20260906_1816: Windows refused")
        print("              to even fast-forward past six of these).")
        return False
    _print_inherited_long_names(inherited)
    if inherited:
        print("[filenamelen] PASS - %d new path(s); %d over %d characters,"
              " every one a name inherited from %s (listed above)."
              % (len(added), len(inherited), NEW_FILENAME_LENGTH_CEILING,
                 base))
    else:
        print("[filenamelen] PASS - %d new path(s), none over %d characters."
              % (len(added), NEW_FILENAME_LENGTH_CEILING))
    return True


def check_base_is_ancestor(repo, base):
    """RED when `base` is not an ancestor of HEAD - the tree you tested is
    NOT the tree the gate's pull_request run will build.

    MEASURED, not argued (LANE-B round f2qyxx, from the two runs on server
    commit 9dcf43de).  `.github/workflows/gate-windows.yml` triggers on BOTH
    `push` (branches-ignore: ci-status) and `pull_request`, and its
    actions/checkout@v4 step passes no `ref:`.  So the push run builds the
    BRANCH TIP and the pull_request run builds `refs/pull/N/merge` - the
    branch MERGED WITH main.  Both post a check named `gate`, and
    `.github/workflows/merge-claude-pr.yml` closes the PR on a red one.

    On server #697 that divergence closed a round whose own branch was green:
      run 33802612233  gate = success  (branch tip, cut before server #695)
      run 33802651960  gate = failure  (merged with main, which by then
                                        carried #695's read point)
    One card in tests/test_lane_b_mob_ai_tick.py asserted that
    lane_hooks.current_named_attr_values did NOT exist.  On the branch that
    was true.  On the merged tree it was false, and no local run this lane
    could make would ever have said so.

    NOW.md (COO `0053` + `0149`) already requires the full suite to be run on
    a tree with main merged in, not on the pure branch.  This check is that
    rule made mechanical: it does not re-run the suite, it says whether the
    tree you ran it on was the right tree.

    Returns True (base is in), False (it is not), None (base does not
    resolve - INCONCLUSIVE, same convention as check_new_skips).
    """
    def git(*args):
        return subprocess.run(
            ["git", "--no-optional-locks", "-C", str(repo)] + list(args),
            capture_output=True, text=True, errors="replace")

    resolved = git("rev-parse", "--verify", "--quiet", base + "^{commit}")
    if resolved.returncode != 0 or not resolved.stdout.strip():
        print("[mainmerge] could not resolve %s - run `git fetch origin main`"
              % base)
        return None
    head = git("rev-parse", "--verify", "--quiet", "HEAD^{commit}")
    if head.returncode != 0 or not head.stdout.strip():
        print("[mainmerge] could not resolve HEAD in %s" % repo)
        return None
    base_sha = resolved.stdout.strip()
    if git("merge-base", "--is-ancestor", base_sha, "HEAD").returncode == 0:
        print("[mainmerge] PASS - %s (%s) is already in HEAD; the gate's"
              % (base, base_sha[:7]))
        print("            pull_request run builds the same tree you tested.")
        return True

    behind = git("rev-list", "--count", "HEAD.." + base_sha).stdout.strip()
    print("[mainmerge] RED - HEAD is missing %s commit(s) that %s has."
          % (behind or "?", base))
    print("            The gate runs TWICE on this push: once on the branch")
    print("            tip (what you tested) and once on branch-merged-with-")
    print("            main (what you did NOT).  Both are named `gate`, and")
    print("            merge-claude-pr.yml closes the PR on the red one.")
    theirs = set(filter(None, git(
        "diff", "--name-only", "HEAD..." + base_sha).stdout.split("\n")))
    mine = set(filter(None, git(
        "diff", "--name-only", base_sha + "...HEAD").stdout.split("\n")))
    both = sorted(theirs & mine)
    if both:
        print("            Files BOTH sides changed (merge them first):")
        for path in both[:12]:
            print("                %s" % path)
        if len(both) > 12:
            print("                ... and %d more" % (len(both) - 12))
    else:
        print("            No file is touched by both sides - but a test of")
        print("            yours can still read code of theirs, which is")
        print("            exactly how server #697 died with no conflict.")
    print("            Fix: git fetch origin main && git merge origin/main,")
    print("            then run the FULL suite again on that tree (NOW.md")
    print("            `0053`/`0149`), then push.")
    return False


# The one server test file this check runs.  It derives the set of test
# modules the gate will actually collect and compares it against the pinned
# census, which is the ONLY thing that notices a module the gate drops.
PRECONDITION_CENSUS_TEST = "tests/test_pytest_precondition_census.py"

#: Substrings that mark the ONE line of the census failure that names the
#: culprit.  pf-adversary D6, R350: the old printout was `out[-12:]`, and with
#: a real planted drift the actionable line ("newly hidden ...") sits at line
#: 33 of ~120 while the last twelve are six arbitrary module names cut out of
#: the middle of the OTHER failing test's 48-name list.  A reader could easily
#: take one of those for the culprit.
CENSUS_CULPRIT_MARKERS = (
    "newly hidden",
    "newly visible",
    "no longer hidden",
    "AssertionError",
    "FAILED ",
)


def _safe(value):
    """Text with every character the bridge console cannot print replaced.

    The console is cp874. Anything read back from a subprocess, a filename or
    an exception can carry a character with no cp874 mapping, and print()
    raises UnicodeEncodeError on it mid-report - rounds 86 and 142 both died
    that way. Every foreign string this file prints goes through here.
    """
    return "".join(
        ch if _cp874_safe(ch) else "?" for ch in str(value)
    )


def _print_census_tail(out):
    """Print the census failure so the culprit line is always in it.

    The tail alone is not enough (D6). The lines that NAME the drifting
    module are matched first and printed under their own heading; the tail
    follows for context.
    """
    lines = out.splitlines()
    named = [line for line in lines
             if any(marker in line for marker in CENSUS_CULPRIT_MARKERS)]
    if named:
        print("         the line(s) that name the drift:")
        for line in named[:8]:
            print("         >> %s" % _safe(line.strip()))
        print("         and the tail:")
    for line in lines[-12:]:
        print("         | %s" % _safe(line))


def _uncommitted_paths(repo):
    """Tracked paths that differ from HEAD, so a verdict can say so (D3).

    Never raises and never blocks a verdict: a repo git cannot read returns
    an empty list, which only costs the warning, not the check.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain",
             "--untracked-files=no"],
            capture_output=True, text=True, errors="replace", timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []
    return [line[3:] for line in (proc.stdout or "").splitlines() if line[3:]]


def check_branch_is_mergeable_by_the_reaper(repo):
    """RED when this branch's name makes its pull request UNMERGEABLE.

    THE ROUND THIS COST (pf-adversary D15, R350, and the round it reviewed).
    `.github/workflows/merge-claude-pr.yml` in BOTH repositories filters on
    the head ref before anything else:

        case "$HEAD_REF" in claude/*) : ;; *) ... skip ;;

    and it does so in `decide`, in `finish` AND in `reap`.  A pull request
    from a branch named anything else is therefore never merged, never
    closed, and never reaped: it sits open for ever, with no comment and no
    warning anywhere.  Measured on server #794 -- gate green at 05:53, marker
    present, zero conflicts, and the reaper merged five other lanes' work
    past it over the next two hours while its own job log said
    "not a claude/ branch - skipped".  A whole round's work was invisible on
    `main` for nine hours and was only found because a later round is
    required to check the fate of the previous one.

    It is WORSE in pf_bridge, where the round LOCK is a pull request: a lane
    that pushes a hand-named branch there never releases its lock again, and
    every one of its later rounds ends on sight.

    Nothing mechanical prevented a repeat, which is what this row is.  It
    costs one `git rev-parse` and it is checked for BOTH clones - this tool's
    own repository as well as the server one - because the trap is in both.

    Returns True (both branches can be merged), False (one cannot - RED),
    None (a branch name could not be read - INCONCLUSIVE).
    """
    here = pathlib.Path(__file__).resolve().parent.parent
    verdicts = []
    for label, clone in (("server", repo), ("bridge", here)):
        try:
            proc = subprocess.run(
                ["git", "-C", str(clone), "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, errors="replace", timeout=60,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            print("[branch] INCONCLUSIVE - could not read the %s branch: %s"
                  % (label, _safe(exc)))
            verdicts.append(None)
            continue
        name = (proc.stdout or "").strip()
        if proc.returncode != 0 or not name:
            print("[branch] INCONCLUSIVE - could not read the %s branch name."
                  % label)
            verdicts.append(None)
            continue
        if name == "HEAD":
            # A detached head has no branch to push; nothing to say.
            print("[branch] INCONCLUSIVE - the %s clone is on a detached HEAD."
                  % label)
            verdicts.append(None)
            continue
        if name.startswith("claude/"):
            print("[branch] PASS - %s is on '%s'." % (label, _safe(name)))
            verdicts.append(True)
            continue
        print("[branch] RED - the %s clone is on '%s', which does NOT start"
              % (label, _safe(name)))
        print("         with 'claude/'. A pull request from this branch is"
              " invisible to")
        print("         merge-claude-pr.yml: it will never be merged, never"
              " closed, and")
        print("         never reaped. Measured on server #794, which sat green"
              " and orphaned")
        print("         for hours. Push to the branch the session was given"
              " instead of")
        print("         naming one yourself.")
        verdicts.append(False)
    if False in verdicts:
        return False
    if None in verdicts:
        return None
    return True


def check_precondition_census(repo):
    """RED when the server clone's precondition census does not agree with
    the modules the gate will collect.

    WHY THIS IS HERE (COO-DECISION 20260905_0646 item 3, chief R350).  The
    two checks above are TEXT properties, and a file can satisfy both while
    still being silently dropped from the gate's collection.  That is not
    hypothetical, it is what killed two pull requests inside twelve hours:

      #785 (LANE-A, 2026-09-04)  a COMMENT spelled a client artifact's name,
                                 which makes the gate exclude the whole
                                 module.  The census then counted 49 where 48
                                 are pinned, and the gate went red on a file
                                 whose own tests all passed.
      #789 (LANE-GM, closed by the gate 04:50)  the same shape.

    Both runs printed `[cp874] PASS` and `[skips] PASS` from this very tool,
    on the exact commit that died.  A preflight that is green on the commit
    that loses the round is not a preflight, which is why this is now a
    mandatory row rather than a suggestion in a letter.

    It is cheap enough to be mandatory: measured 3.24s on this clone, pure
    Python, no Windows, no network.

    Returns True (census agrees), False (it does not - RED), None (could not
    run: no python, no pytest, file absent - INCONCLUSIVE, same convention as
    check_new_skips and check_base_is_ancestor).
    """
    target = repo / PRECONDITION_CENSUS_TEST
    if not target.exists():
        print("[census] INCONCLUSIVE - %s is not in this clone."
              % PRECONDITION_CENSUS_TEST)
        print("         Is --repo really the pirate-force-server clone?"
              " Nothing was compared.")
        return None
    # THIS ROW GRADES THE WORKING TREE, NOT HEAD, AND SAYS SO (pf-adversary
    # D3, R350).  The two rows above are git-based (`base...HEAD`,
    # `git ls-files`); this one shells pytest over the filesystem.  The
    # adversary demonstrated the false green: commit the drift, revert it in
    # the working tree only, and this row prints PASS on a commit that is
    # red.  The realistic trigger is the RED message's own remedy -- "move
    # docs/PYTEST_SKIP_PINS.json in the same commit" is two files, and the
    # pin file is the easy one to leave unstaged.  A dirty tree is named
    # rather than graded away.
    dirty = _uncommitted_paths(repo)

    # errors="replace", like every other subprocess.run in this file (lines
    # ~174, ~245, ~513, ~542).  pf-adversary D4, R350: this was the only one
    # without it.  On Panya's Thai-locale box `text=True` decodes the child
    # with the LOCALE encoding, cp874 has 31 undefined byte positions, and
    # 63 tracked tests/*.py in the server repo carry bytes cp874 cannot
    # decode (the cp874 tripwire only scans tools/, src/, current/).
    # UnicodeDecodeError is neither OSError nor SubprocessError, so it would
    # escape this function, escape main(), and kill the mandatory pre-push
    # tool with a traceback and exit 1 -- indistinguishable from a clean RED,
    # which is verbatim the incident this file already documents further
    # down.  Reintroducing it here would have been the same scar twice.
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", PRECONDITION_CENSUS_TEST, "-q"],
            cwd=str(repo), capture_output=True, text=True,
            errors="replace", timeout=600,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        print("[census] INCONCLUSIVE - could not run pytest: %s" % _safe(exc))
        return None
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("[census] PASS - %s agrees with the modules the gate collects."
              % PRECONDITION_CENSUS_TEST)
        if dirty:
            print("         WARNING - this verdict is about your WORKING TREE."
                  " %d tracked file(s)" % len(dirty))
            print("         differ from HEAD, so it does NOT speak for the"
                  " commit you are about to")
            print("         push. Commit them and run this again:")
            for path in dirty[:5]:
                print("           %s" % _safe(path))
            if len(dirty) > 5:
                print("           ... and %d more" % (len(dirty) - 5))
        return True
    # EVERYTHING THAT IS NOT A CENSUS DISAGREEMENT IS INCONCLUSIVE, NOT RED
    # (pf-adversary D5, R350).  This used to map every non-zero code except 5
    # to RED with the module-exclusion story attached.  Measured with a venv
    # lacking pytest: `python -m pytest` exits 1, so a lane on a fresh clone
    # got a mandatory RED and went hunting an exclusion drift that did not
    # exist.  pytest's own codes: 0 pass, 1 tests failed, 2 interrupted /
    # collection error, 3 internal error, 4 usage error, 5 nothing collected.
    # Only 1 can mean the census disagreed, and even 1 needs the test to have
    # actually run - which is what the marker below checks.
    if proc.returncode != 1:
        print("[census] INCONCLUSIVE - pytest exited %d, which is not a census"
              % proc.returncode)
        print("         disagreement (2 collection error, 3 internal, 4 usage,"
              " 5 nothing collected).")
        print("         Nothing was compared. pytest said:")
        _print_census_tail(out)
        return None
    if " passed" not in out and " failed" not in out:
        # Exit 1 without a result line at all: pytest died before running
        # anything (no pytest module, a bad interpreter). Not a census fact.
        print("[census] INCONCLUSIVE - pytest exited 1 without running any"
              " test. Nothing was")
        print("         compared. pytest said:")
        _print_census_tail(out)
        return None
    print("[census] RED - %s does not agree with what the gate will collect."
          % PRECONDITION_CENSUS_TEST)
    print("         This is the shape that killed #785 and #789: a module")
    print("         the gate EXCLUDES (usually a client artifact's name")
    print("         spelled in a docstring or comment) still passes cp874")
    print("         and skips, and dies on the count.")
    if dirty:
        print("         (Your working tree also differs from HEAD in %d"
              " file(s), so this RED may" % len(dirty))
        print("          be about uncommitted work rather than about the"
              " commit you would push.)")
    _print_census_tail(out)
    return False


# Assembled from parts on purpose.  If the literal sat here whole, a grep of
# this repo for the token would report a hit inside its own guard, and anyone
# quoting the guard into a PR body would ship the token.  Nothing below ever
# prints ASSEMBLED - REDACTED is what goes to the console.
_TOKEN_HEAD = "PF-AUTO"
_TOKEN_TAIL = "MERGE"
MARKER_TOKEN = _TOKEN_HEAD + _TOKEN_TAIL
MARKER_LINE = MARKER_TOKEN + ": v4"
MARKER_REDACTED = "PF-A<...>RGE: v4"


def _cp874_safe(ch):
    try:
        ch.encode("cp874")
    except UnicodeEncodeError:
        return False
    return True


def check_pr_body(body_path, stage):
    """Guard a PR body against the substring the reaper merges on.

    stage 'claim'  - the token must not appear AT ALL.  This is every body
                     that must NOT merge yet: a round claim while the round is
                     still running, a held PR, a PR waiting on pf-adversary.
    stage 'final'  - the token must appear exactly once, alone on its own
                     line.  Prose that mentions it a second time is RED: it is
                     harmless here only by luck, and it teaches the habit that
                     cost four PRs.

    Returns True (pass), False (RED) or None (could not run).
    """
    p = pathlib.Path(body_path).expanduser()
    if not p.is_file():
        print("[prbody] INCONCLUSIVE - %s is not a file. Write the body you"
              % p)
        print("         are about to send to a file and pass it again.")
        return None
    text = None
    # utf-8-sig FIRST, then utf-16.  pf-adversary R328 D5: a body saved by a
    # Windows editor as "UTF-8 with BOM" whose first line is the marker was
    # called RED, because U+FEFF is not whitespace so .strip() left it and the
    # bare-line compare failed -- against an echoed line that looks IDENTICAL
    # to the correct one.  A RED whose printed reason reads like a PASS is how
    # a guard teaches lanes to ignore it.  PowerShell 5.1's `>` and Out-File
    # write UTF-16LE, which utf-8 cannot decode at all.
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            text = p.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            print("[prbody] INCONCLUSIVE - could not read %s: %s" % (p, exc))
            return None
    if text is None:
        print("[prbody] INCONCLUSIVE - could not decode %s as utf-8 or utf-16."
              % p)
        print("         Re-save it as UTF-8 and run again.")
        return None
    hits = [(n, line.strip().lstrip("\ufeff").strip())
            for n, line in enumerate(text.splitlines(), 1)
            if MARKER_TOKEN in line]
    # Echo offending lines REDACTED, and then made safe for code page 874.
    # Two separate hazards, both measured by pf-adversary R328:
    #   - an UNREDACTED echo would put the token into this tool's own output,
    #     and tool output is exactly what gets pasted back into a round file
    #     or a PR body - the shape of the bug this check exists to stop (D4a).
    #   - echoing the body VERBATIM killed the report mid-sentence on the
    #     bridge console: "\u00b7", the separator used on nearly every line of
    #     AGENTS.md and every COO letter, has no cp874 mapping, so print()
    #     raised UnicodeEncodeError after the word RED and before the line
    #     number, the excerpt and the entire remedy paragraph (D4).  The exit
    #     code was then 1 from an uncaught exception - indistinguishable from
    #     a clean RED.  check_cp874 scans OUR files for this; there is no
    #     reason to hand a PR body a hole our own source is not allowed.
    def _show(line):
        line = line.replace(MARKER_TOKEN, "PF-A<...>RGE")
        return "".join(
            ch if _cp874_safe(ch) else "?" for ch in line
        )
    bare_line_hits = [n for n, line in hits if line == MARKER_LINE]
    print("[prbody] %s, stage=%s, %d line(s) carry the marker token"
          % (p, stage, len(hits)))
    if stage == "claim":
        if hits:
            print("[prbody] RED - a body at this stage must not contain the")
            print("         token anywhere, not even to say it is absent.")
            for n, line in hits:
                print("    line %d: %s" % (n, _show(line)[:110]))
            print("         The reaper matches a bare substring: this body")
            print("         WILL be merged the moment it is posted. Say")
            print("         'automerge marker' in words instead (AGENTS.md")
            print("         section 7 / PROCESS_GATES.md section 20).")
            return False
        print("[prbody] PASS - no marker token; this body will not be merged.")
        return True
    if stage == "final":
        if len(hits) == 1 and len(bare_line_hits) == 1:
            print("[prbody] PASS - exactly one marker line (line %d), nothing"
                  % bare_line_hits[0])
            print("         else mentions the token. Expected form: %s"
                  % MARKER_REDACTED)
            return True
        print("[prbody] RED - a final body needs the marker exactly once, on")
        print("         a line of its own, and nowhere else.")
        if not hits:
            print("    found none. Nothing will merge this PR.")
        for n, line in hits:
            print("    line %d: %s%s"
                  % (n, _show(line)[:110],
                     "" if line == MARKER_LINE else "   <- not a bare marker line"))
        return False
    print("[prbody] INCONCLUSIVE - unknown stage %r" % stage)
    return None


# How many [mainmerge] verdicts the self-test must actually compare.  Pinned
# beside the case list, not derived from it, for the R328 D3 reason: a count
# derived from the thing it grades cannot fail when that thing shrinks.
MAINMERGE_SELF_TEST_CASES = 4

# Same pinning discipline, same reason, for the two rows R350 added.
# pf-adversary D7: `check_precondition_census` shipped able to turn a push RED
# with no case and no place in this arithmetic, in a file whose own doctrine is
# "a gate tool with no test is what killed #694".
BRANCHNAME_SELF_TEST_CASES = 4
CENSUS_SELF_TEST_CASES = 2
BRIDGESIZE_SELF_TEST_CASES = 6
QUEUEGROWTH_SELF_TEST_CASES = 8
CONSUMEDSTUB_SELF_TEST_CASES = 9
FILENAMELEN_SELF_TEST_CASES = 12
SCOREBOARD_MANUAL_SELF_TEST_CASES = 8


def _bridgesize_git_root(tmp, dirname, sizes, skip_name=None):
    """A real git repo: commit `sizes` (name -> byte count) as the base
    state, HEAD/`main` points at that commit. Caller mutates the working
    tree afterward (uncommitted) to represent "this branch"'s current state
    - check_bridge_file_sizes() reads current size from disk and base size
    from the git blob, exactly like a real branch ahead of `origin/main`.
    """
    root = pathlib.Path(tmp) / dirname
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                    check=True)
    for name, ceiling in BRIDGE_FILE_SIZE_CEILINGS:
        if name == skip_name:
            continue
        (root / name).write_bytes(b"x" * sizes.get(name, 64))
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"],
                    check=True)
    return root


def _bridgesize_self_test_cases(tmp):
    """Drive check_bridge_file_sizes() against synthetic bridge roots.

    Six provable shapes, all against `base="main"` (this repo's own base
    branch, standing in for `origin/main`): all under ceiling; a file
    already over ceiling that this branch left unchanged (must NOT be RED -
    this is exactly the false-positive pf-adversary found in R359's first
    cut); the same file made bigger by this branch (RED); a file under
    ceiling at base that this branch pushes over ceiling for the first time
    (RED); a missing file (INCONCLUSIVE, unchanged from before); and a
    `base` ref that does not resolve at all (INCONCLUSIVE).
    """
    failures = ran = 0
    gt_name, gt_ceiling = BRIDGE_FILE_SIZE_CEILINGS[0]

    root_ok = _bridgesize_git_root(tmp, "bs_ok", {})
    root_old_debt = _bridgesize_git_root(
        tmp, "bs_old_debt", {gt_name: gt_ceiling + 500})
    root_grown = _bridgesize_git_root(
        tmp, "bs_grown", {gt_name: gt_ceiling + 500})
    (root_grown / gt_name).write_bytes(b"x" * (gt_ceiling + 5000))
    root_new_violation = _bridgesize_git_root(
        tmp, "bs_new_violation", {gt_name: 64})
    (root_new_violation / gt_name).write_bytes(b"x" * (gt_ceiling + 1))
    root_missing = _bridgesize_git_root(
        tmp, "bs_missing", {}, skip_name=BRIDGE_FILE_SIZE_CEILINGS[-1][0])

    cases = [
        ("all five under ceiling, base resolves", root_ok, "main", True),
        ("already over ceiling, unchanged vs base - not this branch's",
         root_old_debt, "main", True),
        ("already over ceiling, grown vs base - RED",
         root_grown, "main", False),
        ("under ceiling at base, pushed over now - RED",
         root_new_violation, "main", False),
        ("not a bridge checkout - one file missing",
         root_missing, "main", None),
        ("base ref does not resolve", root_ok, "origin/no-such-branch", None),
    ]
    for label, root, base, expected in cases:
        got = check_bridge_file_sizes(root, base=base)
        ran += 1
        ok = got is expected
        failures += 0 if ok else 1
        print("  case %-58s expected=%-5s got=%-5s %s"
              % (label[:58], expected, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _filenamelen_git_root(tmp, dirname, added_names, base_names=()):
    """A real git repo: `base_names` (relative paths) committed as `main`,
    then `added_names` added in a SECOND commit on a `feature` branch - so
    `git diff --diff-filter=A main` on the checked-out tree sees only
    `added_names` as newly added, the same shape a real lane branch ahead
    of `origin/main` has. Empty `added_names` still produces a valid
    base+feature pair with nothing added, for the "nothing new" case.
    """
    root = pathlib.Path(tmp) / dirname
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                    check=True)
    (root / ".keep").write_text("x\n", encoding="utf-8")
    for relname in base_names:
        path = root / relname
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("base content\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "checkout", "-q", "-b", "feature"],
                    check=True)
    for relname in added_names:
        path = root / relname
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x\n", encoding="utf-8")
    if added_names:
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "add"],
                        check=True)
    return root


def _filenamelen_rename_root(tmp, dirname, old_name, new_name):
    """A repo where the feature branch RENAMES a base file to `new_name`.

    pf-adversary round `l5tqxc` B2: git reports this as `R`, which the old
    `--diff-filter=A` excluded, so a 113-character name reached main green.
    """
    root = _filenamelen_git_root(tmp, dirname, [], base_names=[old_name])
    subprocess.run(["git", "-C", str(root), "mv", old_name, new_name],
                    check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "rename"],
                    check=True)
    return root


def _filenamelen_self_test_cases(tmp):
    """Drive check_new_filename_length() against synthetic git repos.

    Nine provable shapes against `base="main"`: no files added; one short
    new name; a name at EXACTLY the ceiling (not RED - a ceiling caps what
    is over it, not what equals it); one character over the ceiling (RED);
    a long full PATH whose basename alone is short (not RED - only the
    basename is measured, the same "cost to a filesystem/terminal" the
    ceiling is about); a `.CONSUMED.txt` stub over the ceiling whose
    underlying letter ALREADY EXISTS at base (not RED - inherited debt,
    R375's own real shape the day this check first ran); the same stub
    shape but the underlying letter is ALSO new on this branch (RED - this
    branch's own choice end to end); a repo path that is not a git
    checkout at all (INCONCLUSIVE); and a `base` ref that does not resolve
    (INCONCLUSIVE).
    """
    failures = ran = 0
    at_ceiling_name = "a" * (NEW_FILENAME_LENGTH_CEILING - 3) + ".md"
    over_ceiling_name = "a" * (NEW_FILENAME_LENGTH_CEILING - 2) + ".md"
    assert len(at_ceiling_name) == NEW_FILENAME_LENGTH_CEILING
    assert len(over_ceiling_name) == NEW_FILENAME_LENGTH_CEILING + 1
    long_path_short_name = ("dir/" * 40) + "short.md"
    long_letter_name = "notes/" + ("b" * 98) + ".md"  # 101-char basename
    assert len("b" * 98 + ".md") == NEW_FILENAME_LENGTH_CEILING + 1

    root_none = _filenamelen_git_root(tmp, "fl_none", [])
    root_short = _filenamelen_git_root(tmp, "fl_short", ["notes/short.md"])
    root_at_ceiling = _filenamelen_git_root(
        tmp, "fl_at_ceiling", ["notes/" + at_ceiling_name])
    root_over_ceiling = _filenamelen_git_root(
        tmp, "fl_over_ceiling", ["notes/" + over_ceiling_name])
    root_long_path = _filenamelen_git_root(
        tmp, "fl_long_path", [long_path_short_name])
    root_old_stub = _filenamelen_git_root(
        tmp, "fl_old_stub", [long_letter_name + ".CONSUMED.txt"],
        base_names=[long_letter_name])
    root_new_stub = _filenamelen_git_root(
        tmp, "fl_new_stub",
        [long_letter_name, long_letter_name + ".CONSUMED.txt"])
    root_not_repo = pathlib.Path(tmp) / "fl_not_repo"
    root_not_repo.mkdir()
    # pf-adversary round `l5tqxc`, the three shapes it MEASURED wrong.
    root_rename = _filenamelen_rename_root(
        tmp, "fl_rename", "notes/short.md", "notes/" + over_ceiling_name)
    # The mandated consume/archive copy: the SAME long basename at a new
    # path, with different content (a header added as it moves), which is
    # what turns git's output into D+A instead of R.
    root_inherited_copy = _filenamelen_git_root(
        tmp, "fl_inherited_copy", ["notes/consumed/" + ("b" * 98) + ".md"],
        base_names=[long_letter_name])
    # 43 real characters, 123 bytes, 485 characters of octal escape under
    # git's default core.quotePath.
    thai_name = "notes/" + ("\u0e01" * 40) + ".md"
    assert len(pathlib.Path(thai_name).name) == 43
    root_thai = _filenamelen_git_root(tmp, "fl_thai", [thai_name])

    cases = [
        ("no files added", root_none, "main", True),
        ("one short new name", root_short, "main", True),
        ("basename at exactly the ceiling - not RED",
         root_at_ceiling, "main", True),
        ("basename one over the ceiling - RED",
         root_over_ceiling, "main", False),
        ("long full path, short basename - not RED",
         root_long_path, "main", True),
        ("CONSUMED stub of an old (base) long letter - not RED",
         root_old_stub, "main", True),
        ("CONSUMED stub whose letter is ALSO new - RED",
         root_new_stub, "main", False),
        ("a RENAME to a long name - RED (adversary l5tqxc B2)",
         root_rename, "main", False),
        ("the mandated consumed/ copy of an old long letter - not RED",
         root_inherited_copy, "main", True),
        ("a 43-character Thai basename - not RED (B4, was 485 escaped)",
         root_thai, "main", True),
        ("not a git checkout", root_not_repo, "main", None),
        ("base ref does not resolve",
         root_short, "origin/no-such-branch", None),
    ]
    for label, root, base, expected in cases:
        got = check_new_filename_length(root, base=base)
        ran += 1
        ok = got is expected
        failures += 0 if ok else 1
        print("  case %-58s expected=%-5s got=%-5s %s"
              % (label[:58], expected, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _queuegrowth_git_root(tmp, dirname, base_sizes):
    """A real git repo: commit GAME_TEST_QUEUE.md/CLIENT_RE_QUEUE.md as
    `main`. `base_sizes` maps name -> byte count for a file that should
    exist at base with a NON-default size; a name simply absent from the
    dict still gets a 1000 B baseline file (both watched files exist by
    default - only `base_sizes[name] = None` explicitly leaves one out, to
    build the "new file on this branch" and "missing" cases). Caller
    mutates the working tree afterward for "this branch"'s current state,
    same pattern as _bridgesize_git_root.
    """
    root = pathlib.Path(tmp) / dirname
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                    check=True)
    for name in QUEUE_GROWTH_WATCHED_FILES:
        size = base_sizes.get(name, 1000)
        if size is None:
            continue
        (root / name).write_bytes(b"x" * size)
    (root / ".keep").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"],
                    check=True)
    return root


def _queuegrowth_self_test_cases(tmp):
    """Drive check_queue_growth_cap() against synthetic bridge roots.

    Eight provable shapes against `base="main"`: both files unchanged; one
    grown by exactly the cap (still ok - the cap is a ceiling on growth, not
    a strict-less-than); one grown by cap+1 (RED); one shrunk by a huge
    amount (never capped, any size); a file new on this branch at/under the
    cap (ok - its whole size is the "growth"); a new file over the cap
    (RED); one of the two watched files missing entirely (INCONCLUSIVE); and
    a `base` ref that does not resolve (INCONCLUSIVE).
    """
    failures = ran = 0
    a_name, b_name = QUEUE_GROWTH_WATCHED_FILES

    root_unchanged = _queuegrowth_git_root(
        tmp, "qg_unchanged", {a_name: 1000, b_name: 1000})

    root_at_cap = _queuegrowth_git_root(tmp, "qg_at_cap", {a_name: 1000})
    (root_at_cap / a_name).write_bytes(
        b"x" * (1000 + QUEUE_GROWTH_CAP_PER_PR))

    root_over_cap = _queuegrowth_git_root(tmp, "qg_over_cap", {a_name: 1000})
    (root_over_cap / a_name).write_bytes(
        b"x" * (1000 + QUEUE_GROWTH_CAP_PER_PR + 1))

    root_shrunk = _queuegrowth_git_root(
        tmp, "qg_shrunk", {b_name: 5 * QUEUE_GROWTH_CAP_PER_PR})
    (root_shrunk / b_name).write_bytes(b"x" * 10)

    root_new_ok = _queuegrowth_git_root(tmp, "qg_new_ok", {a_name: None})
    (root_new_ok / a_name).write_bytes(b"x" * (QUEUE_GROWTH_CAP_PER_PR - 1))

    root_new_over = _queuegrowth_git_root(tmp, "qg_new_over", {b_name: None})
    (root_new_over / b_name).write_bytes(
        b"x" * (QUEUE_GROWTH_CAP_PER_PR + 1))

    root_missing = _queuegrowth_git_root(
        tmp, "qg_missing", {a_name: 64, b_name: None})

    cases = [
        ("both unchanged vs base", root_unchanged, "main", True),
        ("grown by exactly the cap - not RED", root_at_cap, "main", True),
        ("grown by cap+1 - RED", root_over_cap, "main", False),
        ("shrunk by far more than the cap - never capped",
         root_shrunk, "main", True),
        ("new file at/under the cap", root_new_ok, "main", True),
        ("new file over the cap", root_new_over, "main", False),
        ("one watched file missing entirely", root_missing, "main", None),
        ("base ref does not resolve",
         root_unchanged, "origin/no-such-branch", None),
    ]
    for label, root, base, expected in cases:
        got = check_queue_growth_cap(root, base=base)
        ran += 1
        ok = got is expected
        failures += 0 if ok else 1
        print("  case %-58s expected=%-5s got=%-5s %s"
              % (label[:58], expected, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _consumedstub_git_root(tmp, dirname):
    """A real git repo with a base commit holding nothing under rounds/ or
    notes_to_chief/ yet - every case adds its round file and letters to the
    WORKING TREE only, uncommitted, exactly like the real thing: the round
    file and its stub are new-on-this-branch relative to `main`.
    """
    root = pathlib.Path(tmp) / dirname
    root.mkdir()
    (root / "rounds").mkdir()
    (root / "notes_to_chief").mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                    check=True)
    (root / ".keep").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"],
                    check=True)
    return root


def _consumedstub_committed_git_root(
        tmp, dirname, letter_name, addressee, round_relname):
    """A real git repo where the round file and its letter are COMMITTED on
    a branch ahead of `main`, not left uncommitted in the working tree -
    the shape `base_resolves=True`'s `git diff --diff-filter=A` path
    actually reads on a real push. `_consumedstub_git_root`'s cases all
    pass an unresolvable base on purpose to reach the *other* branch (no
    base -> scan every file on disk); pf-adversary (round `t0funk`)
    measured that as a result NEITHER branch of check_consumed_stub_
    warning's own two code paths that read git output was exercised by the
    five original cases - only the disk-glob fallback was. This one drives
    the real thing: `main` stays at the base commit, `feature` adds the
    round file and the letter in a second commit, matching a lane branch
    ahead of `origin/main`.
    """
    root = pathlib.Path(tmp) / dirname
    root.mkdir()
    (root / "rounds").mkdir()
    (root / "notes_to_chief").mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                    check=True)
    (root / ".keep").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "checkout", "-q", "-b", "feature"],
                    check=True)
    (root / "notes_to_chief" / letter_name).write_text(
        "[from: COO]\nADDRESSEE: %s\ncc: nobody\n\nbody.\n" % addressee,
        encoding="utf-8")
    (root / "rounds" / round_relname).write_text(
        "round body mentions notes_to_chief/%s here.\n" % letter_name,
        encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "round"],
                    check=True)
    return root


def _consumedstub_self_test_cases(tmp):
    """Drive check_consumed_stub_warning() against synthetic bridge roots.

    Nine provable shapes: the LANE-B `p4ts3e` incident itself (own-lane
    letter named, no stub - 1 WARN); the same letter WITH its stub (0 WARN);
    a letter named that is addressed to a DIFFERENT lane (0 WARN - not this
    lane's to consume); a `_claim.md` round file, which is never scanned (0
    WARN even though it names an unconsumed own-lane letter); a
    bridge_root missing rounds/ or notes_to_chief/ entirely (None); the
    real committed-branch code path (1 WARN, not the disk-glob fallback);
    a comma-separated multi-lane ADDRESSEE line (1 WARN - pf-adversary's
    own finding on the exact-match version this replaced); chief addressed
    as "CHIEF" rather than "LANE-E" (1 WARN, same finding); and a same-round
    continuation file name like `R330b_...md` (1 WARN, also pf-adversary,
    also a real name under rounds/ on main today).
    """
    failures = ran = 0

    def letter(root, name, addressee):
        (root / "notes_to_chief" / name).write_text(
            "[from: COO]\nADDRESSEE: %s\ncc: nobody\n\nbody.\n" % addressee,
            encoding="utf-8")

    def stub(root, name):
        (root / "notes_to_chief" / (name + ".CONSUMED.txt")).write_text(
            "CONSUMED.\n", encoding="utf-8")

    def round_file(root, relname, mentions):
        (root / "rounds" / relname).write_text(
            "round body mentions notes_to_chief/%s here.\n" % mentions,
            encoding="utf-8")

    letter_name = "20260906_1050_COO-DECISION-test.md"

    root_forgotten = _consumedstub_git_root(tmp, "cs_forgotten")
    letter(root_forgotten, letter_name, "LANE-B")
    round_file(root_forgotten, "B_20260906_1200_test_round.md", letter_name)

    root_stubbed = _consumedstub_git_root(tmp, "cs_stubbed")
    letter(root_stubbed, letter_name, "LANE-B")
    stub(root_stubbed, letter_name)
    round_file(root_stubbed, "B_20260906_1200_test_round.md", letter_name)

    root_other_lane = _consumedstub_git_root(tmp, "cs_other_lane")
    letter(root_other_lane, letter_name, "LANE-A")
    round_file(root_other_lane, "B_20260906_1200_test_round.md", letter_name)

    root_claim_only = _consumedstub_git_root(tmp, "cs_claim_only")
    letter(root_claim_only, letter_name, "LANE-B")
    round_file(root_claim_only, "B_20260906_1200_test_round_claim.md",
               letter_name)

    root_not_checkout = pathlib.Path(tmp) / "cs_not_checkout"
    root_not_checkout.mkdir()

    root_committed = _consumedstub_committed_git_root(
        tmp, "cs_committed", letter_name, "LANE-B",
        "B_20260906_1200_test_round.md")

    root_multilane = _consumedstub_git_root(tmp, "cs_multilane")
    letter(root_multilane, letter_name, "LANE-A, LANE-B (copy: chief, COO)")
    round_file(root_multilane, "B_20260906_1200_test_round.md", letter_name)

    root_chief_alias = _consumedstub_git_root(tmp, "cs_chief_alias")
    letter(root_chief_alias, letter_name, "CHIEF")
    round_file(root_chief_alias, "R400_test_round.md", letter_name)

    root_continuation = _consumedstub_git_root(tmp, "cs_continuation")
    letter(root_continuation, letter_name, "LANE-E")
    round_file(root_continuation, "R330b_test_round.md", letter_name)

    cases = [
        ("own-lane letter named, no stub - the p4ts3e incident",
         root_forgotten, "origin/no-such-branch", 1),
        ("same shape, stub present", root_stubbed, "origin/no-such-branch", 0),
        ("letter addressed to a different lane",
         root_other_lane, "origin/no-such-branch", 0),
        ("only a _claim.md round file exists - never scanned",
         root_claim_only, "origin/no-such-branch", 0),
        ("real committed-branch diff path, base resolves",
         root_committed, "main", 1),
        ("comma-separated multi-lane ADDRESSEE line",
         root_multilane, "origin/no-such-branch", 1),
        ("chief addressed as CHIEF, not LANE-E",
         root_chief_alias, "origin/no-such-branch", 1),
        ("same-round continuation file name (R330b-style)",
         root_continuation, "origin/no-such-branch", 1),
    ]
    for label, root, base, expected in cases:
        got = check_consumed_stub_warning(root, base=base)
        ran += 1
        ok = got == expected
        failures += 0 if ok else 1
        print("  case %-58s expected=%-5s got=%-5s %s"
              % (label[:58], expected, got, "ok" if ok else "SELF-TEST RED"))
    got = check_consumed_stub_warning(root_not_checkout, base="main")
    ran += 1
    ok = got is None
    failures += 0 if ok else 1
    print("  case %-58s expected=%-5s got=%-5s %s"
          % ("not a pf_bridge checkout", None, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _scoreboard_manual_git_root(tmp, dirname, base_rows, working_rows):
    """A real git repo: commit `base_rows` as SCOREBOARD_FACTS.tsv at HEAD
    ('main'), then overwrite the (uncommitted) working tree with
    `working_rows` - same "base commit + mutated working tree = a branch
    ahead of origin/main" shape `_bridgesize_git_root` uses.
    """
    root = pathlib.Path(tmp) / dirname
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                    check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                    check=True)
    (root / "SCOREBOARD_FACTS.tsv").write_text(
        "# header\n" + "\n".join(base_rows) + "\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"],
                    check=True)
    (root / "SCOREBOARD_FACTS.tsv").write_text(
        "# header\n" + "\n".join(working_rows) + "\n", encoding="utf-8")
    return root


def _scoreboard_manual_self_test_cases(tmp):
    """Drive check_scoreboard_manual_rows() against synthetic bridge roots.

    Eight provable shapes: no manual row touched (PASS); a manual row
    added, removed, or text-edited (all RED); only a derived row changed
    (PASS - not this gate's business); --allow-manual-scoreboard-edit
    skipping the check entirely; the TSV missing (INCONCLUSIVE); and a
    `base` ref that does not resolve (INCONCLUSIVE).
    """
    failures = ran = 0
    row_a = "DONE\thand\tkept row\tGT-9\tmanual\t2026-09-06 03:11 +07:00"
    row_a_edited = "DONE\thand\tEDITED row\tGT-9\tmanual\t2026-09-06 03:11 +07:00"
    derived_row = ("STUCK\tLANE-A round x\tsentence\tPR #1\t"
                    "A_20260906_0001_x_t.md\t2026-09-06 00:01 +07:00")

    root_unchanged = _scoreboard_manual_git_root(
        tmp, "sm_unchanged", [row_a, derived_row], [row_a, derived_row])
    root_added = _scoreboard_manual_git_root(
        tmp, "sm_added", [derived_row], [derived_row, row_a])
    root_removed = _scoreboard_manual_git_root(
        tmp, "sm_removed", [row_a, derived_row], [derived_row])
    root_edited = _scoreboard_manual_git_root(
        tmp, "sm_edited", [row_a, derived_row], [row_a_edited, derived_row])
    root_derived_only = _scoreboard_manual_git_root(
        tmp, "sm_derived_only", [derived_row], [derived_row + "x"])
    root_missing = pathlib.Path(tmp) / "sm_missing"
    root_missing.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(root_missing)],
                    check=True)

    cases = [
        ("no manual row changed - PASS", root_unchanged, "main", False, True),
        ("a manual row added - RED", root_added, "main", False, False),
        ("a manual row removed - RED", root_removed, "main", False, False),
        ("a manual row edited (text changed) - RED",
         root_edited, "main", False, False),
        ("only a derived row changed - PASS (not this gate's business)",
         root_derived_only, "main", False, True),
        ("--allow-manual-scoreboard-edit skips the check",
         root_added, "main", True, True),
        ("SCOREBOARD_FACTS.tsv missing - INCONCLUSIVE",
         root_missing, "main", False, None),
        ("base ref does not resolve - INCONCLUSIVE",
         root_unchanged, "origin/no-such-branch", False, None),
    ]
    for label, root, base, allow, expected in cases:
        got = check_scoreboard_manual_rows(root, base=base, allow_manual_edit=allow)
        ran += 1
        ok = got is expected
        failures += 0 if ok else 1
        print("  case %-58s expected=%-5s got=%-5s %s"
              % (label[:58], expected, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _branchname_self_test_cases(tmp):
    """Drive check_branch_is_mergeable_by_the_reaper() on real git repos.

    The row it grades exists because a hand-named branch cost R348 its whole
    round (server #794).  Both verdicts have to be provable, and a detached
    head must not be graded as either.
    """
    def git(repo, *args):
        subprocess.run(["git", "-C", str(repo)] + list(args),
                       check=True, capture_output=True, text=True,
                       errors="replace")

    def build(branch):
        repo = pathlib.Path(tmp) / ("bn_" + branch.replace("/", "_"))
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "t@t")
        git(repo, "config", "user.name", "t")
        (repo / "f.txt").write_text("x\n", encoding="utf-8")
        git(repo, "add", "f.txt")
        git(repo, "commit", "-qm", "c")
        git(repo, "checkout", "-q", "-b", branch)
        return repo

    failures = 0
    ran = 0
    good = build("claude/lucky-name-abc123")
    bad = build("lane-e-handmade-name")
    # The row grades BOTH clones, and this file's own repository is the
    # second one, so a case has to pin each position independently.  Passing
    # `good` as the server clone still consults the real bridge clone, which
    # is why the expected value below is "not False" rather than True: on a
    # developer machine sitting on a claude/* branch it is True, and in any
    # other checkout the bridge half may legitimately be INCONCLUSIVE.  What
    # must never happen is a RED from the good case.
    for label, repo, expected_red in (
        ("server on a claude/ branch is not RED", good, False),
        ("server on a hand-named branch is RED", bad, True),
    ):
        got = check_branch_is_mergeable_by_the_reaper(repo)
        ran += 1
        ok = (got is False) == expected_red
        failures += 0 if ok else 1
        print("  case %d %-58s expected_red=%-5s got=%-5s %s"
              % (ran, label, expected_red, got, "ok" if ok else "SELF-TEST RED"))
    # A detached HEAD has no branch to push and must not be graded either way.
    detached = build("claude/temp-for-detach")
    head = subprocess.run(
        ["git", "-C", str(detached), "rev-parse", "HEAD"],
        capture_output=True, text=True, errors="replace",
    ).stdout.strip()
    git(detached, "checkout", "-q", head)
    got = check_branch_is_mergeable_by_the_reaper(detached)
    ran += 1
    ok = got is not False
    failures += 0 if ok else 1
    print("  case %d %-58s expected=not RED  got=%-5s %s"
          % (ran, "detached HEAD is not RED", got, "ok" if ok else "SELF-TEST RED"))
    # A path that is not a git repository at all: INCONCLUSIVE, never a
    # verdict.  This is the shape a wrong --repo takes.
    notrepo = pathlib.Path(tmp) / "bn_notrepo"
    notrepo.mkdir()
    got = check_branch_is_mergeable_by_the_reaper(notrepo)
    ran += 1
    ok = got is not True
    failures += 0 if ok else 1
    print("  case %d %-58s expected=not PASS got=%-5s %s"
          % (ran, "a non-repo path never passes", got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _census_self_test_cases(tmp):
    """Pin the two verdicts of check_precondition_census that need no pytest.

    The RED path needs a real server clone and is exercised for real every
    time this tool runs against one; what a self-test CAN pin without one is
    that a missing file and a non-repo path are INCONCLUSIVE rather than
    PASS.  pf-adversary D5's whole point: everything that is not a census
    disagreement must refuse to be a verdict.
    """
    failures = 0
    ran = 0
    empty = pathlib.Path(tmp) / "census_empty"
    (empty / "tests").mkdir(parents=True)
    for label, repo in (
        ("a clone without the census test is INCONCLUSIVE", empty),
        ("a path that does not exist is INCONCLUSIVE",
         pathlib.Path(tmp) / "census_missing"),
    ):
        got = check_precondition_census(repo)
        ran += 1
        ok = got is None
        failures += 0 if ok else 1
        print("  case %d %-58s expected=None  got=%-5s %s"
              % (ran, label, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _mainmerge_self_test_cases(tmp):
    """Drive check_base_is_ancestor() against real throwaway git repos.

    COO-DECISION 20260904_0643 item 3, answering LANE-B's own ask
    20260904_0439: the tool that decides `[mainmerge]` had no test, and
    "a gate tool with no test is what killed #694".  The hand measurement
    in the 0439 letter proved the two verdicts once, by hand, on one
    machine; it is not a test and nothing re-runs it.

    Two verdicts have to be provable, and this builds a repository for
    each rather than mocking git:
      RED  - HEAD is behind the base (what server #694 and #697 pushed),
             in both shapes: no file touched by both sides (the #697
             shape, where nothing conflicts and the round still dies) and
             one file touched by both.
      PASS - the base has been merged into HEAD (the tree NOW.md `0053`
             and `0149` require the full suite to have been run on).
    The third return value, INCONCLUSIVE, is covered too: a base that
    does not resolve must be None and must never be read as PASS.

    Returns (failures, ran).
    """
    def git(repo, *args):
        return subprocess.run(
            ["git", "--no-optional-locks", "-C", str(repo)] + list(args),
            capture_output=True, text=True, errors="replace")

    def build(repo, overlap):
        """A repo whose HEAD (branch `work`) is one commit behind `mainline`.

        `overlap` decides whether both sides touched the same file, which
        selects the two different RED explanations the check prints.
        """
        repo.mkdir(parents=True)
        git(repo, "init", "-q", "-b", "mainline")
        git(repo, "config", "user.email", "selftest@pf.local")
        git(repo, "config", "user.name", "pf preflight self-test")
        git(repo, "config", "commit.gpgsign", "false")
        (repo / "shared.txt").write_text("base\n", encoding="ascii")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "base commit")
        git(repo, "branch", "work")
        # mainline moves on, exactly like main did under #697.
        (repo / ("shared.txt" if overlap else "theirs.txt")).write_text(
            "mainline moved\n", encoding="ascii")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "mainline moves ahead")
        git(repo, "checkout", "-q", "work")
        (repo / ("shared.txt" if overlap else "mine.txt")).write_text(
            "my round\n", encoding="ascii")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "the round's own work")

    probe = subprocess.run(["git", "--version"],
                           capture_output=True, text=True, errors="replace")
    if probe.returncode != 0:
        print("  SELF-TEST RED: git is not runnable here, so the "
              "[mainmerge] cases cannot run at all.")
        return 1, 0

    failures = 0
    ran = 0
    root = pathlib.Path(tmp) / "mainmerge"
    checks = []
    for overlap in (False, True):
        repo = root / ("overlap" if overlap else "disjoint")
        build(repo, overlap)
        checks.append((
            "HEAD behind mainline, %s"
            % ("one file touched by both sides"
               if overlap else "no file touched by both (the #697 shape)"),
            repo, "mainline", False))
    # The same repo, after the fix the RED message tells you to apply.
    merged = root / "merged"
    build(merged, False)
    git(merged, "merge", "-q", "--no-edit", "mainline")
    checks.append(
        ("mainline merged into HEAD - the tree the suite must be run on",
         merged, "mainline", True))
    # A base that does not resolve is INCONCLUSIVE, never PASS.
    checks.append(
        ("base does not resolve (nothing fetched)",
         merged, "origin/no-such-branch", None))

    for label, repo, base, expected in checks:
        got = check_base_is_ancestor(repo, base)
        ran += 1
        ok = got is expected
        failures += 0 if ok else 1
        print("  mainmerge %-62s expected=%-5s got=%-5s %s\n"
              % (label[:62], expected, got, "ok" if ok else "SELF-TEST RED"))
    return failures, ran


def _self_test():
    """Prove the guard on this clone, with no PR and no network.

    There is no pytest harness in pf_bridge, so the check ships its own
    cases; a guard nobody can run is a guard nobody trusts.
    """
    import tempfile
    # (label, body-as-bytes, encoding-note, stage, expected)
    cases = [
        ("clean claim",
         "R328 round lock. No automerge marker until both repos are pushed.",
         "claim", True),
        # THE TWO REAL INCIDENT BODIES, quoted from the alarm letters that
        # reported them.  pf-adversary R328 D8: the first draft's "the exact
        # #1015 shape" case had neither the backticks nor the dash the real
        # body had - right verdict, wrong claim.  These are the texts.
        ("the literal pf_bridge#1015 body (LANE-A 20260903_2105)",
         "No `" + MARKER_LINE + "` yet - marker goes on at end of round",
         "claim", False),
        ("the literal server#672 body (LANE-DB 20260903_2043)",
         "This PR intentionally carries **no `" + MARKER_LINE
         + "` marker** until that is resolved.",
         "claim", False),
        ("bare token, no ': v4'",
         "mentions " + MARKER_TOKEN + " bare", "claim", False),
        ("clean final",
         "R328 work.\n\n" + MARKER_LINE + "\n", "final", True),
        ("final with the marker forgotten - nothing would merge it",
         "R328 work.\n", "final", False),
        ("prose copy plus the real line",
         "I added " + MARKER_TOKEN + " below.\n" + MARKER_LINE + "\n",
         "final", False),
        ("marker buried in a sentence",
         "prefix " + MARKER_LINE + " suffix\n", "final", False),
        ("marker in backticks - the reaper merges it, the rule says bare",
         "R328\n\n`" + MARKER_LINE + "`\n", "final", False),
        # D5 regressions: both of these were WRONGLY red before R328's fix.
        ("final, UTF-8 BOM, marker on line 1",
         "\ufeff" + MARKER_LINE + "\n", "final", True),
        ("final, CRLF line endings",
         "R328 work.\r\n\r\n" + MARKER_LINE + "\r\n", "final", True),
        # D4 regression: a body full of the house separator must not kill the
        # report on a cp874 console.  Verdict here; the console-safety half is
        # asserted below.
        ("claim, house separators and Thai around the token",
         "R328 claim \u00b7 \u0e22\u0e31\u0e07\u0e44\u0e21\u0e48\u0e43\u0e2a\u0e48 `"
         + MARKER_LINE + "` \u00b7 end", "claim", False),
        ("unknown stage is not a verdict",
         "anything at all", "HELD", None),
    ]
    failures = 0
    ran = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, (label, body, stage, expected) in enumerate(cases, 1):
            f = pathlib.Path(tmp) / ("case%02d.txt" % i)
            f.write_text(body, encoding="utf-8")
            got = check_pr_body(str(f), stage)
            ran += 1
            ok = got is expected
            failures += 0 if ok else 1
            print("  case %d %-58s expected=%-5s got=%-5s %s\n"
                  % (i, label[:58], expected, got,
                     "ok" if ok else "SELF-TEST RED"))
        missing = check_pr_body(str(pathlib.Path(tmp) / "nope.txt"), "final")
        ran += 1
        ok = missing is None
        failures += 0 if ok else 1
        print("  case %d %-58s expected=None  got=%-5s %s"
              % (ran, "missing file", missing, "ok" if ok else "SELF-TEST RED"))
        undecodable = pathlib.Path(tmp) / "latin1.txt"
        undecodable.write_bytes(b"\xff\xfe\x00\x00bad")
        got = check_pr_body(str(undecodable), "final")
        ran += 1
        ok = got is None
        failures += 0 if ok else 1
        print("  case %d %-58s expected=None  got=%-5s %s"
              % (ran, "undecodable bytes", got, "ok" if ok else "SELF-TEST RED"))
        mm_failures, mm_ran = _mainmerge_self_test_cases(tmp)
        failures += mm_failures
        ran += mm_ran
        bn_failures, bn_ran = _branchname_self_test_cases(tmp)
        failures += bn_failures
        ran += bn_ran
        cs_failures, cs_ran = _census_self_test_cases(tmp)
        failures += cs_failures
        ran += cs_ran
        bs_failures, bs_ran = _bridgesize_self_test_cases(tmp)
        failures += bs_failures
        ran += bs_ran
        fl_failures, fl_ran = _filenamelen_self_test_cases(tmp)
        failures += fl_failures
        ran += fl_ran
        qg_failures, qg_ran = _queuegrowth_self_test_cases(tmp)
        failures += qg_failures
        ran += qg_ran
        cs_stub_failures, cs_stub_ran = _consumedstub_self_test_cases(tmp)
        failures += cs_stub_failures
        ran += cs_stub_ran
        sm_failures, sm_ran = _scoreboard_manual_self_test_cases(tmp)
        failures += sm_failures
        ran += sm_ran
    if failures:
        print("SELF-TEST RED: %d of %d case(s) wrong." % (failures, ran))
        return 1
    expected_cases = (
        len(cases) + 2 + MAINMERGE_SELF_TEST_CASES
        + BRANCHNAME_SELF_TEST_CASES + CENSUS_SELF_TEST_CASES
        + BRIDGESIZE_SELF_TEST_CASES + FILENAMELEN_SELF_TEST_CASES
        + QUEUEGROWTH_SELF_TEST_CASES
        + CONSUMEDSTUB_SELF_TEST_CASES + SCOREBOARD_MANUAL_SELF_TEST_CASES
    )
    if ran != expected_cases:
        # pf-adversary R328 D3: the old green line was the string "9 cases",
        # so an empty case list still printed it.  A token that fires on "no
        # failures were recorded" is satisfied by running nothing.  The
        # [mainmerge] block is counted the same way and for the same reason:
        # if git disappears, or a case is dropped, the arithmetic goes red
        # instead of the report going quietly shorter.
        print("SELF-TEST RED: expected %d cases, ran %d."
              % (expected_cases, ran))
        return 1
    print("SELF-TEST PASS: %d cases, %d compared." % (ran, ran))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=os.environ.get(
        "PF_SERVER_REPO", "../pirate-force-server"),
        help="path to the pirate-force-server clone (default ../pirate-force-server "
             "or $PF_SERVER_REPO)")
    ap.add_argument("--base", default="origin/main",
                    help="branch point to compare skips against (default origin/main)")
    ap.add_argument("--pr-body", default=None,
                    help="path to a file holding the PR body you are about to "
                         "post or PATCH; checked against the automerge-marker "
                         "rule (AGENTS.md section 7)")
    ap.add_argument("--pr-stage", choices=("claim", "final"), default=None,
                    help="claim = this PR must NOT merge yet (round claim, "
                         "held PR): the token must be absent. final = this PR "
                         "is meant to merge now: exactly one bare marker line. "
                         "Defaults to claim WHEN --pr-body is given, because "
                         "the wrong guess is the safe one - it refuses to "
                         "merge rather than merging early. Given WITHOUT "
                         "--pr-body it is an error, not a default: it is the "
                         "one signal that you meant to check a body.")
    ap.add_argument("--self-test", action="store_true",
                    help="run the PR-body guard's own cases and exit; needs no "
                         "repo, no network, no PR")
    ap.add_argument("--allow-manual-scoreboard-edit", action="store_true",
                    help="this PR is a courier PR actually carrying Panya's "
                         "or ka1-A's own edit to a `manual` row in "
                         "SCOREBOARD_FACTS.tsv (COO-DECISION 20260906_0042). "
                         "Every other PR that diffs a manual row is RED.")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()

    # THE BODY CHECK RUNS FIRST, AND WITHOUT THE SERVER CLONE.
    # pf-adversary R328 D1, measured: the command AGENTS.md section 7 tells
    # every lane to run carries no --repo, so `repo` fell back to
    # ../pirate-force-server, the `.git` test failed, and main() returned 2
    # having NEVER CALLED check_pr_body.  Worse, three of the four incidents
    # this guard exists for were server PR bodies, and this file does not
    # exist in that clone at all - a lane running the mandated line from
    # there got "can't open file", exit 2, and no verdict.  Exit 2 is not
    # RED, so the rule ("RED = do not open the PR") gave that lane nothing.
    # The body check depends on no repo, so it must not be reachable only
    # through one.
    body_result = None
    if args.pr_body is not None:
        body_result = check_pr_body(args.pr_body, args.pr_stage or "claim")
    elif args.pr_stage is not None:
        # D2: --pr-stage used to default to "claim", so argparse could not
        # tell "asked for a body check" from "asked for nothing", and a
        # forgotten --pr-body ended in the pasteable words PREFLIGHT PASS.
        print("[prbody] INCONCLUSIVE - --pr-stage %s given with no --pr-body."
              % args.pr_stage)
        print("         You meant to check a body; nothing was checked.")
        body_result = None
        print("")
        print("PREFLIGHT INCONCLUSIVE - see the row above.")
        return 1

    repo = pathlib.Path(args.repo).expanduser()
    if not (repo / ".git").exists():
        print("FATAL: %s is not a git clone. Pass --repo." % repo)
        if args.pr_body is not None:
            print("       The cp874 and skip checks did NOT run. The"
                  " [prbody] row above")
            print("       is the only verdict this run produced - and it"
                  " stands on its own.")
            if body_result is False:
                return 1
            if body_result is None:
                return 1
            print("       Body: PASS. Still run this again with --repo"
                  " before you push.")
        return 2
    print("=== pf_gate_preflight on %s ===" % repo)
    results = [check_cp874(repo), check_new_skips(repo, args.base),
               check_base_is_ancestor(repo, args.base),
               check_precondition_census(repo),
               check_branch_is_mergeable_by_the_reaper(repo),
               check_bridge_file_sizes(base=args.base),
               check_queue_growth_cap(base=args.base),
               check_new_filename_length(repo, base=args.base),
               check_new_filename_length(
                   pathlib.Path(__file__).resolve().parent.parent,
                   base=args.base),
               check_scoreboard_manual_rows(
                   base=args.base,
                   allow_manual_edit=args.allow_manual_scoreboard_edit)]
    # Advisory only (chief D-something, LANE-B 20260906_1050): never added to
    # `results` - a forgotten .CONSUMED.txt stub is a warning, not a reason
    # to block a push that is otherwise clean.
    check_consumed_stub_warning(base=args.base)
    if args.pr_body is None:
        # Open skip with a reason, never a silent one (AGENTS.md section 7).
        # Not appended to `results`: most callers run this tool for the cp874
        # and skip checks alone, and turning those runs INCONCLUSIVE would
        # make every lane stop passing --pr-body by stopping to use the tool.
        # pf-adversary R328 argued both sides of this and landed here too;
        # what it would NOT accept was silently discarding an explicit
        # --pr-stage, which is now an error above.
        print("[prbody] SKIPPED - no --pr-body given. This run says NOTHING")
        print("         about the body you are about to post. Pass")
        print("         --pr-body <file> --pr-stage claim|final before you")
        print("         open or PATCH one.")
    else:
        results.append(body_result)
    print("")
    # R297 (chief, pf-adversary finding D5): a check that could not RUN is not
    # a check that PASSED.  check_new_skips returns None when the base ref does
    # not resolve (a remote named upstream, a --single-branch clone of a
    # claude/* branch, a stale fetch).  The old test was "if False in results",
    # and None is not False, so that run printed PREFLIGHT PASS having compared
    # nothing -- a false green under a rule (COO-DECISION 20260902_0148 item 2)
    # that now makes this tool mandatory before every push.
    if False in results:
        print("PREFLIGHT RED - fix the rows above before you push.")
        print("NOTE: a green preflight does NOT promise a green gate. A test")
        print("that passes on Linux and fails on Windows is out of scope here")
        print("(that is what actually closed #495/#503).  PANYA-DECISION")
        print("20260902_0040: do NOT ask for a pre-push job on Panya's")
        print("machine - she ruled that symptom is absorbed by the lanes.")
        return 1
    if None in results:
        print("PREFLIGHT INCONCLUSIVE - a check could not run (see the rows")
        print("above).  This is NOT a pass: fix the reason, usually a base ref")
        print("that does not resolve (git fetch origin main, or pass --base).")
        return 1
    print("PREFLIGHT PASS (cp874 + no new skips + main is in this branch"
          " + precondition census agrees")
    print("                + both branches are mergeable by the reaper"
          " + no bridge file grew past its ceiling on this branch")
    print("                + neither queue file grew past its per-PR cap"
          " + no manual scoreboard row was touched")
    # pf-adversary round `l5tqxc`, B6: this banner is what a lane pastes
    # into a PR body as evidence, and it was a hardcoded list that had
    # stopped matching what `results` actually contains.
    print("                + no new file name over %d characters in either"
          " repo)." % NEW_FILENAME_LENGTH_CEILING)
    print("NOTE: this does NOT promise a green gate - Windows-only runtime")
    print("failures are out of scope.  A RED or INCONCLUSIVE preflight means")
    print("DO NOT PUSH until it is fixed (AGENTS.md section 7).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

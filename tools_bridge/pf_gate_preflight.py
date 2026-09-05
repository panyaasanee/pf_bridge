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
BRIDGE_FILE_SIZE_CEILINGS = (
    ("GAME_TEST_QUEUE.md", 300 * 1024),
    ("CLIENT_RE_QUEUE.md", 200 * 1024),
    ("AGENTS.md", 30 * 1024),
    ("CHIEF_CONTINUATION.md", 30 * 1024),
    ("NOW.md", 12 * 1024),
)


def check_bridge_file_sizes(bridge_root=None):
    """RED when a pf_bridge file every lane reads every round is over its
    ceiling.

    `bridge_root` defaults to this file's own repository (tools_bridge/ lives
    directly under the pf_bridge root, one parent up), so a lane running the
    command AGENTS.md section 7 gives gets a real answer with no extra flag -
    the same pattern `check_branch_is_mergeable_by_the_reaper` already uses
    for the bridge clone.  A caller with a bridge checkout somewhere else (a
    self-test, a bridge clone at a nonstandard path) can pass one.

    Returns True (all five files are at or under their ceiling), False (one
    or more is over - RED, every size printed), None (one of the five names
    does not exist under `bridge_root` - this is not the pf_bridge checkout,
    or a listed file was renamed and this table was not updated with it).
    """
    root = pathlib.Path(bridge_root) if bridge_root is not None \
        else pathlib.Path(__file__).resolve().parent.parent
    missing, over = [], []
    for name, ceiling in BRIDGE_FILE_SIZE_CEILINGS:
        p = root / name
        if not p.is_file():
            missing.append(name)
            continue
        size = p.stat().st_size
        red = size > ceiling
        print("  %s %-24s %9d bytes  (ceiling %9d)"
              % ("RED" if red else "ok ", name, size, ceiling))
        if red:
            over.append(name)
    if missing:
        print("[bridgesize] INCONCLUSIVE - %s not found under %s."
              % (", ".join(missing), root))
        print("             Is this really the pf_bridge checkout?")
        return None
    if over:
        print("[bridgesize] RED - %d of 5 file(s) over their ceiling"
              % len(over))
        print("             (PANYA-ORDER 20260905_2038 item 1). Archive")
        print("             closed tickets to archive/*_ARCHIVE_<date>_*.md")
        print("             with a one-line stub left in place; never delete")
        print("             or move an item that has not been tested yet.")
        return False
    print("[bridgesize] PASS - all five files at or under their ceiling.")
    return True


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
BRIDGESIZE_SELF_TEST_CASES = 3


def _bridgesize_self_test_cases(tmp):
    """Drive check_bridge_file_sizes() against synthetic bridge roots.

    Three provable shapes: every file under its ceiling, one file over, and
    a root missing one of the five names entirely (not a bridge checkout).
    """
    failures = ran = 0

    def make_root(dirname, oversize_name=None, skip_name=None):
        root = pathlib.Path(tmp) / dirname
        root.mkdir()
        for name, ceiling in BRIDGE_FILE_SIZE_CEILINGS:
            if name == skip_name:
                continue
            size = ceiling + 1 if name == oversize_name else 64
            (root / name).write_bytes(b"x" * size)
        return root

    cases = [
        ("all five under ceiling", make_root("bs_ok"), True),
        ("one file over ceiling", make_root(
            "bs_red", oversize_name=BRIDGE_FILE_SIZE_CEILINGS[0][0]), False),
        ("not a bridge checkout - one file missing", make_root(
            "bs_missing", skip_name=BRIDGE_FILE_SIZE_CEILINGS[-1][0]), None),
    ]
    for label, root, expected in cases:
        got = check_bridge_file_sizes(root)
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
    if failures:
        print("SELF-TEST RED: %d of %d case(s) wrong." % (failures, ran))
        return 1
    expected_cases = (
        len(cases) + 2 + MAINMERGE_SELF_TEST_CASES
        + BRANCHNAME_SELF_TEST_CASES + CENSUS_SELF_TEST_CASES
        + BRIDGESIZE_SELF_TEST_CASES
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
               check_bridge_file_sizes()]
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
          " + bridge files are under their size ceiling).")
    print("NOTE: this does NOT promise a green gate - Windows-only runtime")
    print("failures are out of scope.  A RED or INCONCLUSIVE preflight means")
    print("DO NOT PUSH until it is fixed (AGENTS.md section 7).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

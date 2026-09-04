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
The third shape - a test that genuinely passes on Linux and fails on
Windows - CANNOT be caught here and this script does not pretend to.  For
that, ask for a bridge job on Panya's machine before pushing.

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
    if failures:
        print("SELF-TEST RED: %d of %d case(s) wrong." % (failures, ran))
        return 1
    if ran != len(cases) + 2 + MAINMERGE_SELF_TEST_CASES:
        # pf-adversary R328 D3: the old green line was the string "9 cases",
        # so an empty case list still printed it.  A token that fires on "no
        # failures were recorded" is satisfied by running nothing.  The
        # [mainmerge] block is counted the same way and for the same reason:
        # if git disappears, or a case is dropped, the arithmetic goes red
        # instead of the report going quietly shorter.
        print("SELF-TEST RED: expected %d cases, ran %d."
              % (len(cases) + 2 + MAINMERGE_SELF_TEST_CASES, ran))
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
               check_base_is_ancestor(repo, args.base)]
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
    print("PREFLIGHT PASS (cp874 + no new skips + main is in this branch).")
    print("NOTE: this does NOT promise a green gate - Windows-only runtime")
    print("failures are out of scope.  A RED or INCONCLUSIVE preflight means")
    print("DO NOT PUSH until it is fixed (AGENTS.md section 7).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

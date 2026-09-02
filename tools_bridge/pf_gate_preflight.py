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


def check_new_skips(repo, base):
    """Name every skip marker this branch ADDS relative to `base`.

    The gate pins skipped-test counts, so a skip added by this branch is RED
    even though it is green locally. This does not count skips at runtime; it
    names the lines you added, which is what a lane can act on before pushing.
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
    added = []
    current = None
    for line in diff.split("\n"):
        if line.startswith("+++ b/"):
            current = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            if any(m in line for m in SKIP_MARKERS):
                added.append((current, line[1:].strip()[:110]))
    if added:
        print("[skips] RED - this branch ADDS %d skip marker(s):" % len(added))
        for f, l in added:
            print("    %s: %s" % (f, l))
        print("        The gate pins skip counts. A test that always skips on")
        print("        CI reads as a NEW skip and turns the run red - that is")
        print("        what closed PR #503 on 2026-09-01. Make it run, or")
        print("        delete it, or move the pin in the same commit.")
        return False
    print("[skips] PASS - no new skip markers vs %s" % base)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=os.environ.get(
        "PF_SERVER_REPO", "../pirate-force-server"),
        help="path to the pirate-force-server clone (default ../pirate-force-server "
             "or $PF_SERVER_REPO)")
    ap.add_argument("--base", default="origin/main",
                    help="branch point to compare skips against (default origin/main)")
    args = ap.parse_args()
    repo = pathlib.Path(args.repo).expanduser()
    if not (repo / ".git").exists():
        print("FATAL: %s is not a git clone. Pass --repo." % repo)
        return 2
    print("=== pf_gate_preflight on %s ===" % repo)
    results = [check_cp874(repo), check_new_skips(repo, args.base)]
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
    print("PREFLIGHT PASS (cp874 + no new skips).")
    print("NOTE: this does NOT promise a green gate - Windows-only runtime")
    print("failures are out of scope.  A RED or INCONCLUSIVE preflight means")
    print("DO NOT PUSH until it is fixed (AGENTS.md section 7).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pf_resolve_green_boot.py -- answer ONE question for the attended tester:

    "Which commit of pirate-force-server am I allowed to boot right now?"

WHY THIS EXISTS (chief round 117).  Every queue entry used to say some version
of "boot origin/main HEAD, the newest one whose ci-status says success".  Round
116 measured that this sentence stopped being runnable the day automerge
started working: the merge commit that automerge pushes is pushed with
GITHUB_TOKEN, a push with GITHUB_TOKEN does not trigger a workflow, so the
merge commit is never gated and NOBODY EVER WRITES ci/<sha>.json FOR IT.
A tester who follows the old sentence literally looks up the head of main,
finds no verdict file, and -- correctly, by rule (3) of path D -- refuses to
boot, while the code they were sent to test is sitting one commit below,
green, gated, and merged.

So the rule the tester needs is not "the head" but:

    the NEWEST ANCESTOR of origin/main that has a verdict file whose
    conclusion is exactly `success` AND whose `sha` field matches the commit
    it claims to be about.

That is a walk, not a lookup, which is why it is a tool and not a sentence.

WHAT THIS TOOL WILL NOT DO
  - It never merges, never checks out, never fetches unless asked (--fetch),
    and never writes anything anywhere.  It runs `git rev-list`, `git ls-tree`
    and `git show` and prints.
  - It never reports a commit as bootable on the strength of the word
    `success` alone: path D rule (1) says compare the `sha` INSIDE the file
    with the commit being asked about, because the only reason those two can
    disagree is that something is wrong.
  - `skipped` and `cancelled` are NOT green and NOT red.  They are "no
    information", exactly like a missing file, and this tool keeps walking.
  - There is no ci/latest.json and there must never be one; if one appears
    this tool says so loudly and ignores it.  A verdict addressed to
    "whoever asks" is how a reader learns the word success about one commit
    and boots another one.

EXIT CODES (a human reads the text; a script reads these)
  0  a bootable commit was found -- its sha is on the BOOT_COMMIT line
  2  usage error, or git itself failed (bad repo, unknown ref, no fetch)
  3  no bootable commit within the window -- DO NOT BOOT, report it

stdout is pure ASCII on purpose: this runs on Panya's cp874 Windows console,
where one arrow or one emoji kills the tool in the middle of its own report.

Usage (on the bridge, from anywhere):
  py -3 pf_resolve_green_boot.py --repo C:\\path\\to\\pirate-force-server --fetch
  py -3 pf_resolve_green_boot.py --repo ... --json
  py -3 pf_resolve_green_boot.py --selftest
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

GREEN = "success"
DEFAULT_BRANCH = "origin/main"
DEFAULT_STATUS_REF = "origin/ci-status"
DEFAULT_MAX = 60


class GitError(Exception):
    pass


def git(repo, args, allow_fail=False):
    """Run one read-only git command in `repo` and return stdout as text."""
    proc = subprocess.run(
        ["git", "-C", repo] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if proc.returncode != 0:
        if allow_fail:
            return None
        raise GitError(
            "git %s failed (exit %d): %s"
            % (" ".join(args), proc.returncode, proc.stderr.strip())
        )
    return proc.stdout


def verdict_shas(repo, status_ref):
    """Return (set_of_shas_with_a_verdict_file, saw_latest_json)."""
    out = git(repo, ["ls-tree", "--name-only", status_ref, "ci/"], allow_fail=True)
    if out is None:
        raise GitError(
            "cannot list %s -- the status branch is missing locally; "
            "run with --fetch, or `git fetch origin ci-status` first" % status_ref
        )
    shas = set()
    saw_latest = False
    for line in out.splitlines():
        name = line.strip()
        if not name.startswith("ci/") or not name.endswith(".json"):
            continue
        stem = name[len("ci/"):-len(".json")]
        if stem == "latest":
            saw_latest = True
            continue
        shas.add(stem)
    return shas, saw_latest


def read_verdict(repo, status_ref, sha):
    """Return (state, detail) for one commit.

    state is one of: 'green', 'red', 'unknown'
    detail is a human sentence naming the rule that decided it.
    """
    blob = git(repo, ["show", "%s:ci/%s.json" % (status_ref, sha)], allow_fail=True)
    if blob is None:
        return "unknown", "no verdict file (rule 3: no file = no information)"
    try:
        data = json.loads(blob)
    except ValueError as exc:
        return "unknown", "verdict file is not valid JSON (%s)" % exc
    if not isinstance(data, dict):
        return "unknown", "verdict file is not a JSON object"

    claimed = str(data.get("sha", ""))
    if claimed != sha:
        return (
            "unknown",
            "rule 1 VIOLATED: file ci/%s.json says sha=%r -- treating as NO "
            "verdict and saying so" % (sha, claimed),
        )

    conclusion = str(data.get("conclusion", ""))
    if conclusion == GREEN:
        return (
            "green",
            "conclusion=success run_id=%s utc=%s event=%s"
            % (data.get("run_id", "?"), data.get("utc", "?"), data.get("event", "?")),
        )
    if conclusion in ("skipped", "cancelled"):
        return (
            "unknown",
            "conclusion=%s (rule 2: not green, not red -- no information)" % conclusion,
        )
    return "red", "conclusion=%s (rule 2: green is the word success alone)" % conclusion


def resolve(repo, branch, status_ref, max_commits):
    """Walk `branch` newest-first and return a result dict."""
    known, saw_latest = verdict_shas(repo, status_ref)
    out = git(repo, ["rev-list", "--topo-order", "--max-count=%d" % max_commits, branch])
    commits = [line.strip() for line in out.splitlines() if line.strip()]
    if not commits:
        raise GitError("%s resolved to no commits" % branch)

    examined = []
    boot = None
    for sha in commits:
        if sha in known:
            state, detail = read_verdict(repo, status_ref, sha)
        else:
            state, detail = "unknown", "no verdict file (rule 3: no file = no information)"
        subject = git(repo, ["log", "-1", "--format=%s", sha]).strip()
        examined.append(
            {"sha": sha, "state": state, "detail": detail, "subject": subject[:72]}
        )
        if state == "green":
            boot = examined[-1]
            break

    return {
        "branch": branch,
        "status_ref": status_ref,
        "head": commits[0],
        "window": max_commits,
        "verdicts_on_status_branch": len(known),
        "saw_latest_json": saw_latest,
        "examined": examined,
        "boot_commit": boot["sha"] if boot else None,
        "boot_detail": boot["detail"] if boot else None,
        "distance_from_head": (len(examined) - 1) if boot else None,
    }


def render(result):
    lines = []
    lines.append("pf_resolve_green_boot -- newest gated-green ancestor of %s" % result["branch"])
    lines.append("  status branch: %s (%d verdict file(s))"
                 % (result["status_ref"], result["verdicts_on_status_branch"]))
    lines.append("  head of %s: %s" % (result["branch"], result["head"]))
    if result["saw_latest_json"]:
        lines.append("  !! ci/latest.json EXISTS ON THE STATUS BRANCH AND MUST NOT.")
        lines.append("     Ignored here. Report it: a verdict with no commit named in it")
        lines.append("     is how the wrong commit gets booted with no warning at all.")
    lines.append("")
    for i, row in enumerate(result["examined"]):
        mark = {"green": "GREEN  ", "red": "RED    ", "unknown": "unknown"}[row["state"]]
        lines.append("  [%d] %s %s  %s" % (i, mark, row["sha"][:12], row["subject"]))
        lines.append("        %s" % row["detail"])
    lines.append("")
    if result["boot_commit"]:
        lines.append("BOOT_COMMIT: %s" % result["boot_commit"])
        lines.append("  %s" % result["boot_detail"])
        lines.append("  distance from head of %s: %d commit(s)"
                     % (result["branch"], result["distance_from_head"]))
        lines.append("  boot it with:  git checkout %s" % result["boot_commit"])
        lines.append("  (detached HEAD is correct here: you are booting a verdict, not a branch)")
    else:
        lines.append("BOOT_COMMIT: NONE")
        lines.append("  Nothing in the newest %d commit(s) of %s carries a green verdict."
                     % (result["window"], result["branch"]))
        lines.append("  DO NOT BOOT. This is rule 3: not knowing is never 'probably green'.")
        lines.append("  Widen the window with --max, or say in your note that the queue item")
        lines.append("  is waiting on a gate run rather than on you.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# selftest: build a throwaway repository whose history contains every case
# this tool claims to handle, then run the resolver against it and check the
# answers.  A tool nobody has watched go red is a tool that cannot go red.
# ---------------------------------------------------------------------------

def _sh(repo, args):
    subprocess.run(["git", "-C", repo] + args, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _commit(repo, name):
    with open(os.path.join(repo, name), "w") as fh:
        fh.write(name + "\n")
    _sh(repo, ["add", "--", name])
    _sh(repo, ["commit", "-q", "-m", name])
    return git(repo, ["rev-parse", "HEAD"]).strip()


def selftest():
    tmp = tempfile.mkdtemp(prefix="pf_green_boot_selftest_")
    failures = []

    def check(label, got, want):
        if got == want:
            print("  ok   %s" % label)
        else:
            print("  FAIL %s: got %r want %r" % (label, got, want))
            failures.append(label)

    try:
        repo = os.path.join(tmp, "repo")
        os.makedirs(repo)
        _sh(repo, ["init", "-q", "-b", "main"])
        _sh(repo, ["config", "user.email", "selftest@example.invalid"])
        _sh(repo, ["config", "user.name", "selftest"])

        c1 = _commit(repo, "one")     # green
        c2 = _commit(repo, "two")     # red
        c3 = _commit(repo, "three")   # sha mismatch in its verdict file
        c4 = _commit(repo, "four")    # cancelled
        c5 = _commit(repo, "five")    # no verdict file at all (the merge-commit case)

        # Build the orphan status branch by hand, the same shape publish-status
        # writes: one JSON file per commit, named for the commit.
        status = os.path.join(tmp, "status")
        os.makedirs(os.path.join(status, "ci"))
        _sh(status, ["init", "-q", "-b", "ci-status"])
        _sh(status, ["config", "user.email", "selftest@example.invalid"])
        _sh(status, ["config", "user.name", "selftest"])

        def put(sha, payload):
            with open(os.path.join(status, "ci", sha + ".json"), "w") as fh:
                json.dump(payload, fh)

        put(c1, {"sha": c1, "conclusion": "success", "run_id": "1", "utc": "z"})
        put(c2, {"sha": c2, "conclusion": "failure", "run_id": "2", "utc": "z"})
        put(c3, {"sha": c3[:-1] + ("0" if c3[-1] != "0" else "1"),
                 "conclusion": "success", "run_id": "3", "utc": "z"})
        put(c4, {"sha": c4, "conclusion": "cancelled", "run_id": "4", "utc": "z"})
        with open(os.path.join(status, "ci", "latest.json"), "w") as fh:
            json.dump({"sha": c5, "conclusion": "success"}, fh)
        _sh(status, ["add", "-A"])
        _sh(status, ["commit", "-q", "-m", "verdicts"])
        _sh(repo, ["fetch", "-q", status, "ci-status:ci-status"])

        print("selftest: history built (5 commits, 4 verdicts + 1 forbidden latest.json)")

        res = resolve(repo, "main", "ci-status", 10)
        check("walks past the ungated head", res["examined"][0]["state"], "unknown")
        check("cancelled is not green", res["examined"][1]["state"], "unknown")
        check("sha mismatch is not green", res["examined"][2]["state"], "unknown")
        check("failure is red", res["examined"][3]["state"], "red")
        check("lands on the green ancestor", res["boot_commit"], c1)
        check("distance from head", res["distance_from_head"], 4)
        check("latest.json is noticed", res["saw_latest_json"], True)
        check("mismatch names rule 1", "rule 1 VIOLATED" in res["examined"][2]["detail"], True)

        # Narrow the window so the green commit is out of reach: the tool must
        # refuse rather than reach for the nearest word that says success.
        narrow = resolve(repo, "main", "ci-status", 3)
        check("refuses when the window excludes the green one", narrow["boot_commit"], None)

        # The report must survive a cp874 console.
        text = render(res)
        try:
            text.encode("ascii")
            check("report is pure ASCII", True, True)
        except UnicodeEncodeError as exc:
            check("report is pure ASCII", str(exc), "ascii")

        # And the missing-status-branch case must be an error, not a silent zero.
        bare = os.path.join(tmp, "bare")
        os.makedirs(bare)
        _sh(bare, ["init", "-q", "-b", "main"])
        _sh(bare, ["config", "user.email", "selftest@example.invalid"])
        _sh(bare, ["config", "user.name", "selftest"])
        _commit(bare, "only")
        try:
            resolve(bare, "main", "ci-status", 5)
            check("missing status branch raises", False, True)
        except GitError:
            check("missing status branch raises", True, True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("SELFTEST FAILED: %d check(s): %s" % (len(failures), ", ".join(failures)))
        return 1
    print("SELFTEST PASS")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description="resolve the newest gated-green ancestor")
    ap.add_argument("--repo", default=".", help="path to the pirate-force-server clone")
    ap.add_argument("--branch", default=DEFAULT_BRANCH)
    ap.add_argument("--status-ref", default=DEFAULT_STATUS_REF)
    ap.add_argument("--max", type=int, default=DEFAULT_MAX, help="how many commits to walk")
    ap.add_argument("--fetch", action="store_true",
                    help="fetch origin main and origin ci-status first (the only write this tool does)")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--selftest", action="store_true", help="run the built-in checks and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    repo = os.path.abspath(args.repo)
    try:
        if args.fetch:
            git(repo, ["fetch", "origin", "main", "ci-status"])
        result = resolve(repo, args.branch, args.status_ref, args.max)
    except GitError as exc:
        sys.stderr.write("pf_resolve_green_boot: %s\n" % exc)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render(result))
    return 0 if result["boot_commit"] else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

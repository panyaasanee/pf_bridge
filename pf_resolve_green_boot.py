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

WHAT QUESTION THIS TOOL ACTUALLY ANSWERS.  pf-adversary asked it in round 117
and the answer had to be written down before the tool could be trusted:

    the tester wants to boot THE CODE THAT IS ON MAIN.
    A verdict is only useful because it is a verdict ABOUT that code.

So this walks the FIRST-PARENT line of origin/main -- the mainline, the code
that is actually on the branch -- newest first, and for each commit asks:

  a) does this mainline commit have a green verdict of its own?  boot it.
  b) is it a merge whose second parent (the merged pull request head) has a
     green verdict, AND is the merge's TREE BYTE-IDENTICAL to that parent's
     tree?  then the gated code and the code on main are the same code, and
     the parent is bootable.  The tree comparison is MEASURED, not assumed:
     if a commit landed on main between the pull request opening and merging,
     the trees differ, this tool says so and refuses that candidate.

Walking by --topo-order (the first draft did) is wrong for exactly that case:
it dives down the pull request branch and can return a commit whose tree is
missing work that is on main, while printing "newest ancestor" over it.

WHAT THIS TOOL WILL NOT DO
  - It never merges, never checks out, never fetches unless asked (--fetch),
    and never writes anything anywhere.
  - It never reports a commit as bootable on the strength of the word
    `success` alone: path D rule (1) says compare the `sha` INSIDE the file
    with the commit being asked about, and a verdict with no run_id and no
    utc did not come from publish-status at all.
  - `skipped` and `cancelled` are NOT green and NOT red.  They are "no
    information", exactly like a missing file, and this tool keeps walking.
  - A RED mainline commit above the answer is never swallowed: it is printed
    and repeated in a warning block, because a checker that only prints good
    news teaches its reader that silence means pass.
  - There is no ci/latest.json and there must never be one; if one appears
    this tool says so loudly and ignores it.

WHAT `success` MEANS, IN FULL, SO NOBODY UPGRADES IT SILENTLY
  `.github/workflows/README_GATE_CI.md` in the server repository says it
  plainly: the Actions gate is a SUBSET.  Nine named checks cannot run on a
  GitHub runner at all, and the authoritative gate remains the per-round job
  on Panya's bridge.  A green verdict here means "the client-free subset
  passed on windows-latest", never "the whole gate passed".  This tool prints
  that sentence with every answer it gives.

EXIT CODES (a human reads the text; a script reads these)
  0  a bootable commit was found -- its sha is on the BOOT_COMMIT line
  2  usage error, or git itself failed (bad path, not a repository, no git)
  3  no bootable commit within the window -- DO NOT BOOT, report it

stdout is pure ASCII on purpose, and stdout is also FORCED not to die on a
character it cannot encode: this runs on Panya's cp874 Windows console, where
one arrow or one emoji kills the tool in the middle of its own report.  The
same trap exists on the way IN: git subjects are decoded as utf-8 with
replacement here, never with the console code page, because a commit message
containing an emoji would otherwise crash the reader of the verdict rather
than the writer of the message.

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
GATE_VALUES = ("success", "failure", "cancelled", "skipped")
DEFAULT_BRANCH = "origin/main"
DEFAULT_STATUS_REF = "origin/ci-status"
DEFAULT_MAX = 60

SUBSET_NOTE = (
    "what 'success' means: the CLIENT-FREE SUBSET of the gate passed on a "
    "GitHub runner. Nine named checks cannot run there at all, and the "
    "authoritative gate is still the per-round job on the bridge. Green here "
    "is not a gate pass; see .github/workflows/README_GATE_CI.md."
)


class GitError(Exception):
    pass


def git(repo, args, allow_fail=False, warnings=None):
    """Run one read-only git command in `repo` and return stdout as text.

    Decoded as utf-8 with replacement on purpose: the console code page must
    never decide whether this tool survives reading a commit subject.
    git's stderr is surfaced even when the command SUCCEEDS, because
    'warning: refname ... is ambiguous' is exactly the kind of line that
    turns a correct-looking answer into the wrong commit.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", repo] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        raise GitError("git is not on PATH -- this tool is git and nothing else")
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace").strip()
    if proc.returncode != 0:
        if allow_fail:
            return None
        raise GitError("git %s failed (exit %d): %s"
                       % (" ".join(args), proc.returncode, err))
    if err and warnings is not None:
        for line in err.splitlines():
            line = line.strip()
            if line and line not in warnings:
                warnings.append("git said (while succeeding): %s" % line)
    return out


def check_repo(repo):
    if not os.path.isdir(repo):
        raise GitError("--repo %s is not a directory that exists on this machine" % repo)
    inside = git(repo, ["rev-parse", "--is-inside-work-tree"], allow_fail=True)
    if inside is None or inside.strip() != "true":
        raise GitError("--repo %s is not a git working tree" % repo)


def _no_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("duplicate key %r" % key)
        seen[key] = value
    return seen


def verdict_index(repo, status_ref, warnings):
    """Return (set_of_shas_with_a_verdict_file, saw_latest_json)."""
    out = git(repo, ["ls-tree", "--name-only", status_ref, "ci/"],
              allow_fail=True, warnings=warnings)
    if out is None:
        raise GitError(
            "cannot list %s -- the status branch is not in this clone; "
            "run again with --fetch, or `git fetch origin ci-status` first"
            % status_ref)
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


def read_verdict(repo, status_ref, sha, known, warnings):
    """Return (state, detail, data) for one commit.

    state is one of: 'green', 'red', 'unknown'.
    'unknown' always means NO INFORMATION, never 'probably fine'.
    """
    if sha not in known:
        return "unknown", "no verdict file (rule 3: no file = no information)", None
    blob = git(repo, ["show", "%s:ci/%s.json" % (status_ref, sha)],
               allow_fail=True, warnings=warnings)
    if blob is None:
        return "unknown", "verdict file listed but unreadable", None
    try:
        data = json.loads(blob, object_pairs_hook=_no_duplicate_keys)
    except ValueError as exc:
        return "unknown", "verdict file is unusable (%s)" % exc, None
    if not isinstance(data, dict):
        return "unknown", "verdict file is not a JSON object", None

    claimed = str(data.get("sha", ""))
    if claimed != sha:
        return ("unknown",
                "rule 1 VIOLATED: ci/%s.json says sha=%r -- treated as NO verdict"
                % (sha, claimed), data)

    if not data.get("run_id") or not data.get("utc"):
        return ("unknown",
                "verdict has no run_id/utc, so publish-status did not write it "
                "-- treated as NO verdict", data)

    conclusion = str(data.get("conclusion", ""))
    if conclusion == GREEN:
        return ("green",
                "conclusion=success run_id=%s utc=%s event=%s ref=%s"
                % (data.get("run_id"), data.get("utc"),
                   data.get("event", "?"), data.get("ref", "?")), data)
    if conclusion == "failure":
        return "red", "conclusion=failure run_id=%s (the gate judged this commit)" % data.get("run_id"), data
    if conclusion in ("skipped", "cancelled"):
        return ("unknown",
                "conclusion=%s (rule 2: not green, not red -- no information)"
                % conclusion, data)
    return ("unknown",
            "conclusion=%r is not one of %s -- the file is broken, which is not "
            "the same as the gate saying no" % (conclusion, "/".join(GATE_VALUES)),
            data)


def subject_of(repo, sha, warnings):
    text = git(repo, ["log", "-1", "--format=%s", sha], allow_fail=True, warnings=warnings)
    return (text or "").strip()[:72]


def resolve(repo, branch, status_ref, max_commits):
    """Walk the FIRST-PARENT line of `branch`, newest first."""
    if max_commits < 1:
        raise GitError("--max must be at least 1 (got %d)" % max_commits)
    warnings = []
    known, saw_latest = verdict_index(repo, status_ref, warnings)
    out = git(repo, ["rev-list", "--first-parent",
                     "--max-count=%d" % max_commits, branch], warnings=warnings)
    mainline = [line.strip() for line in out.splitlines() if line.strip()]
    if not mainline:
        raise GitError("%s resolved to no commits" % branch)

    examined = []
    boot = None
    reds_above = []

    for sha in mainline:
        state, detail, _ = read_verdict(repo, status_ref, sha, known, warnings)
        row = {"sha": sha, "state": state, "detail": detail,
               "subject": subject_of(repo, sha, warnings), "role": "mainline"}
        examined.append(row)
        if state == "green":
            boot = dict(row, how="this mainline commit carries its own green verdict")
            break
        if state == "red":
            reds_above.append(sha)

        parents = git(repo, ["rev-list", "--parents", "-n", "1", sha],
                      warnings=warnings).split()
        if len(parents) < 3:
            continue  # not a merge: nothing else to consider at this commit

        head_sha = parents[2]
        p_state, p_detail, _ = read_verdict(repo, status_ref, head_sha, known, warnings)
        merge_tree = git(repo, ["rev-parse", "%s^{tree}" % sha], warnings=warnings).strip()
        head_tree = git(repo, ["rev-parse", "%s^{tree}" % head_sha], warnings=warnings).strip()
        same_tree = merge_tree == head_tree

        if p_state == "green" and not same_tree:
            p_detail = (p_detail + " -- BUT its tree differs from the mainline "
                        "commit it was merged into, so booting it would boot code "
                        "that is NOT what is on the branch. Refused.")
            p_state = "unusable"
        row2 = {"sha": head_sha, "state": p_state, "detail": p_detail,
                "subject": subject_of(repo, head_sha, warnings),
                "role": "merged pull request head of %s" % sha[:12]}
        examined.append(row2)
        if p_state == "red":
            reds_above.append(head_sha)
        if p_state == "green" and same_tree:
            boot = dict(row2, how=("its tree is byte-identical to mainline commit %s, "
                                   "so the gated code and the code on the branch are "
                                   "the same code (measured, not assumed)" % sha[:12]))
            break

    if boot and boot["sha"] in reds_above:
        reds_above.remove(boot["sha"])

    return {
        "branch": branch,
        "status_ref": status_ref,
        "head": mainline[0],
        "window": max_commits,
        "verdicts_on_status_branch": len(known),
        "saw_latest_json": saw_latest,
        "git_warnings": warnings,
        "examined": examined,
        "reds_above_the_answer": reds_above,
        "boot_commit": boot["sha"] if boot else None,
        "boot_detail": boot["detail"] if boot else None,
        "boot_how": boot["how"] if boot else None,
    }


def render(result):
    lines = []
    lines.append("pf_resolve_green_boot -- bootable commit on the first-parent line of %s"
                 % result["branch"])
    lines.append("  status branch: %s (%d verdict file(s))"
                 % (result["status_ref"], result["verdicts_on_status_branch"]))
    lines.append("  head of %s: %s" % (result["branch"], result["head"]))
    for warn in result["git_warnings"]:
        lines.append("  !! %s" % warn)
    if result["saw_latest_json"]:
        lines.append("  !! ci/latest.json EXISTS ON THE STATUS BRANCH AND MUST NOT.")
        lines.append("     Ignored here. Report it: a verdict with no commit named in it")
        lines.append("     is how the wrong commit gets booted with no warning at all.")
    lines.append("")
    for i, row in enumerate(result["examined"]):
        mark = {"green": "GREEN   ", "red": "RED     ",
                "unusable": "REFUSED ", "unknown": "unknown "}[row["state"]]
        lines.append("  [%d] %s %s  %s" % (i, mark, row["sha"][:12], row["subject"]))
        lines.append("        (%s) %s" % (row["role"], row["detail"]))
    lines.append("")
    if result["reds_above_the_answer"]:
        lines.append("  !! THE GATE JUDGED %d COMMIT(S) ABOVE THIS ANSWER AS FAILED:"
                     % len(result["reds_above_the_answer"]))
        for sha in result["reds_above_the_answer"]:
            lines.append("     %s" % sha)
        lines.append("     Booting the answer below is still allowed, but WRITE THIS DOWN")
        lines.append("     in your result note: red on the branch is chief's problem, and")
        lines.append("     a report that does not mention it looks like it never happened.")
        lines.append("")
    if result["boot_commit"]:
        lines.append("BOOT_COMMIT: %s" % result["boot_commit"])
        lines.append("  %s" % result["boot_detail"])
        lines.append("  why this one: %s" % result["boot_how"])
        lines.append("  boot it with:  git checkout %s" % result["boot_commit"])
        lines.append("  (detached HEAD is correct here: you are booting a verdict, not a branch)")
        lines.append("  %s" % SUBSET_NOTE)
    else:
        lines.append("BOOT_COMMIT: NONE")
        lines.append("  Nothing on the first-parent line of %s, within the newest %d commit(s),"
                     % (result["branch"], result["window"]))
        lines.append("  carries a green verdict this tool is willing to stand behind.")
        lines.append("  DO NOT BOOT. This is rule 3: not knowing is never 'probably green'.")
        lines.append("  The three reasons this happens, in the order worth checking:")
        lines.append("    1. the gate has not finished (or never ran) for the newest work --")
        lines.append("       then this is waiting on the gate, NOT on you. Say so in your note.")
        lines.append("    2. the status branch holds %d verdict(s) in total -- if that is 0,"
                     % result["verdicts_on_status_branch"])
        lines.append("       publish-status is broken and no --max will ever help.")
        lines.append("    3. the green commit is older than the window: retry with --max 200.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# selftest.  Builds throwaway histories containing every case this tool claims
# to handle, runs the tool AS A SUBPROCESS so the exit-code contract printed in
# GAME_TEST_QUEUE.md is itself under test, and checks the answers.
# A tool nobody has watched go red is a tool that cannot go red.
# ---------------------------------------------------------------------------

def _sh(repo, args):
    proc = subprocess.run(["git", "-C", repo] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise GitError("selftest setup: git %s failed: %s"
                       % (" ".join(args), proc.stderr.decode("utf-8", "replace").strip()))


def _init(path):
    os.makedirs(path)
    _sh(path, ["init", "-q", "-b", "main"])
    _sh(path, ["config", "user.email", "selftest@example.invalid"])
    _sh(path, ["config", "user.name", "selftest"])
    _sh(path, ["config", "commit.gpgsign", "false"])
    _sh(path, ["config", "core.hooksPath", os.path.join(path, ".no-hooks")])


def _commit(repo, name, message=None):
    with open(os.path.join(repo, name), "w") as fh:
        fh.write(name + "\n")
    _sh(repo, ["add", "--", name])
    _sh(repo, ["commit", "-q", "-m", message or name])
    return git(repo, ["rev-parse", "HEAD"]).strip()


def _publish(status_repo, verdicts):
    os.makedirs(os.path.join(status_repo, "ci"), exist_ok=True)
    for sha, payload in verdicts.items():
        with open(os.path.join(status_repo, "ci", sha + ".json"), "w") as fh:
            json.dump(payload, fh)
    _sh(status_repo, ["add", "-A"])
    _sh(status_repo, ["commit", "-q", "-m", "verdicts"])


def _verdict(sha, conclusion, **extra):
    payload = {"sha": sha, "conclusion": conclusion, "run_id": "1",
               "utc": "2026-08-21T00:00:00Z", "event": "pull_request"}
    payload.update(extra)
    return payload


def _run_tool(repo, extra):
    proc = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--repo", repo,
         "--branch", "main", "--status-ref", "ci-status"] + extra,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"))


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
        # --- case 1: the shape the real repository has today ---------------
        repo = os.path.join(tmp, "one")
        _init(repo)
        base = _commit(repo, "base")
        _sh(repo, ["checkout", "-q", "-b", "pr"])
        pr_head = _commit(repo, "feature")
        _sh(repo, ["checkout", "-q", "main"])
        _sh(repo, ["merge", "-q", "--no-ff", "pr", "-m", "Merge pull request #1"])
        merge = git(repo, ["rev-parse", "HEAD"]).strip()

        status = os.path.join(tmp, "one_status")
        _init(status)
        _sh(status, ["checkout", "-q", "-b", "ci-status"])
        _publish(status, {
            pr_head: _verdict(pr_head, "success"),
            base: _verdict(base, "success"),
        })
        _sh(repo, ["fetch", "-q", status, "ci-status:ci-status"])

        res = resolve(repo, "main", "ci-status", 10)
        check("ungated merge head is walked past", res["examined"][0]["state"], "unknown")
        check("merged pull request head is the answer", res["boot_commit"], pr_head)
        check("and only because the trees match",
              "byte-identical" in (res["boot_how"] or ""), True)
        code, out, _ = _run_tool(repo, [])
        check("exit code 0 when bootable", code, 0)
        check("BOOT_COMMIT printed", ("BOOT_COMMIT: " + pr_head) in out, True)
        check("subset caveat printed with the answer", "not a gate pass" in out, True)

        # --- case 2: a commit landed on main while the PR was open ---------
        # The merged head is green, but its tree is NOT what is on main.
        repo2 = os.path.join(tmp, "two")
        _init(repo2)
        b2 = _commit(repo2, "base")
        _sh(repo2, ["checkout", "-q", "-b", "pr"])
        pr2 = _commit(repo2, "feature")
        _sh(repo2, ["checkout", "-q", "main"])
        main_only = _commit(repo2, "landed_on_main_meanwhile")
        _sh(repo2, ["merge", "-q", "--no-ff", "pr", "-m", "Merge pull request #2"])
        status2 = os.path.join(tmp, "two_status")
        _init(status2)
        _sh(status2, ["checkout", "-q", "-b", "ci-status"])
        _publish(status2, {pr2: _verdict(pr2, "success"), b2: _verdict(b2, "success")})
        _sh(repo2, ["fetch", "-q", status2, "ci-status:ci-status"])

        res2 = resolve(repo2, "main", "ci-status", 10)
        check("green head with a different tree is refused",
              [r["state"] for r in res2["examined"] if r["sha"] == pr2], ["unusable"])
        check("and the walk does not stop there", res2["boot_commit"], b2)
        check("main-only commit was examined, not skipped",
              any(r["sha"] == main_only for r in res2["examined"]), True)

        # --- case 3: red on the mainline must be printed, not swallowed ----
        repo3 = os.path.join(tmp, "three")
        _init(repo3)
        g3 = _commit(repo3, "green_one")
        r3 = _commit(repo3, "red_one")
        status3 = os.path.join(tmp, "three_status")
        _init(status3)
        _sh(status3, ["checkout", "-q", "-b", "ci-status"])
        _publish(status3, {g3: _verdict(g3, "success"), r3: _verdict(r3, "failure")})
        _sh(repo3, ["fetch", "-q", status3, "ci-status:ci-status"])
        res3 = resolve(repo3, "main", "ci-status", 10)
        check("red is reported as red", res3["examined"][0]["state"], "red")
        check("red above the answer is carried out", res3["reds_above_the_answer"], [r3])
        code3, out3, _ = _run_tool(repo3, [])
        check("red is shouted in the report", "THE GATE JUDGED" in out3, True)
        check("still exit 0 with a usable answer below the red", code3, 0)

        # --- case 4: every flavour of unusable verdict ---------------------
        repo4 = os.path.join(tmp, "four")
        _init(repo4)
        ok4 = _commit(repo4, "the_only_real_green")
        c_skip = _commit(repo4, "skipped_one")
        c_cancel = _commit(repo4, "cancelled_one")
        c_mismatch = _commit(repo4, "sha_mismatch")
        c_noprov = _commit(repo4, "no_provenance")
        c_dup = _commit(repo4, "duplicate_keys")
        c_caps = _commit(repo4, "capital_success")
        c_junk = _commit(repo4, "not_json")
        status4 = os.path.join(tmp, "four_status")
        _init(status4)
        _sh(status4, ["checkout", "-q", "-b", "ci-status"])
        _publish(status4, {
            ok4: _verdict(ok4, "success"),
            c_skip: _verdict(c_skip, "skipped"),
            c_cancel: _verdict(c_cancel, "cancelled"),
            c_mismatch: _verdict("0" * 40, "success"),
            c_caps: _verdict(c_caps, "Success"),
        })
        with open(os.path.join(status4, "ci", c_noprov + ".json"), "w") as fh:
            fh.write('{"sha": "%s", "conclusion": "success"}' % c_noprov)
        with open(os.path.join(status4, "ci", c_dup + ".json"), "w") as fh:
            fh.write('{"sha": "%s", "conclusion": "failure", "conclusion": "success",'
                     ' "run_id": "9", "utc": "z"}' % c_dup)
        with open(os.path.join(status4, "ci", c_junk + ".json"), "w") as fh:
            fh.write("not json at all")
        _sh(status4, ["add", "-A"])
        _sh(status4, ["commit", "-q", "-m", "more verdicts"])
        _sh(repo4, ["fetch", "-q", status4, "ci-status:ci-status"])

        res4 = resolve(repo4, "main", "ci-status", 20)
        by_sha = dict((r["sha"], r) for r in res4["examined"])
        check("not-json is unknown", by_sha[c_junk]["state"], "unknown")
        check("duplicate keys is unknown", by_sha[c_dup]["state"], "unknown")
        check("capital Success is not green", by_sha[c_caps]["state"], "unknown")
        check("verdict with no run_id/utc is not green", by_sha[c_noprov]["state"], "unknown")
        check("sha mismatch names rule 1",
              "rule 1 VIOLATED" in by_sha[c_mismatch]["detail"], True)
        check("cancelled is not green", by_sha[c_cancel]["state"], "unknown")
        check("skipped is not green", by_sha[c_skip]["state"], "unknown")
        check("walks all the way to the one real green", res4["boot_commit"], ok4)

        # --- case 5: nothing green -> exit 3, and that branch is ASCII -----
        code5, out5, _ = _run_tool(repo4, ["--max", "3"])
        check("exit code 3 when nothing bootable", code5, 3)
        check("says DO NOT BOOT", "DO NOT BOOT" in out5, True)
        check("names 'waiting on the gate, not on you'", "NOT on you" in out5, True)
        try:
            out5.encode("ascii")
            check("the DO-NOT-BOOT report is pure ASCII", True, True)
        except UnicodeEncodeError as exc:
            check("the DO-NOT-BOOT report is pure ASCII", str(exc), "ascii")
        try:
            render(res4).encode("ascii")
            check("the answer report is pure ASCII", True, True)
        except UnicodeEncodeError as exc:
            check("the answer report is pure ASCII", str(exc), "ascii")

        # --- case 6: a non-ASCII commit subject must not kill the reader ---
        repo6 = os.path.join(tmp, "six")
        _init(repo6)
        g6 = _commit(repo6, "green_here")
        _commit(repo6, "emoji_subject", message="MOVE-AUTHORITY-003 \U0001F534 refuse")
        status6 = os.path.join(tmp, "six_status")
        _init(status6)
        _sh(status6, ["checkout", "-q", "-b", "ci-status"])
        _publish(status6, {g6: _verdict(g6, "success")})
        _sh(repo6, ["fetch", "-q", status6, "ci-status:ci-status"])
        code6, out6, err6 = _run_tool(repo6, [])
        check("survives an emoji in a commit subject", code6, 0)
        check("no traceback on the emoji path", "Traceback" in err6, False)

        # --- case 7: latest.json is noticed and never used -----------------
        with open(os.path.join(status6, "ci", "latest.json"), "w") as fh:
            json.dump({"sha": g6, "conclusion": "success"}, fh)
        _sh(status6, ["add", "-A"])
        _sh(status6, ["commit", "-q", "-m", "forbidden latest"])
        _sh(repo6, ["fetch", "-q", "-f", status6, "ci-status:ci-status"])
        res7 = resolve(repo6, "main", "ci-status", 10)
        check("latest.json is noticed", res7["saw_latest_json"], True)
        code7, out7, _ = _run_tool(repo6, [])
        check("latest.json is shouted about", "MUST NOT" in out7, True)

        # --- case 8: the failure modes of the tool itself ------------------
        code8, _, err8 = _run_tool(os.path.join(tmp, "does_not_exist"), [])
        check("bad --repo is exit 2", code8, 2)
        check("bad --repo says so plainly", "not a directory" in err8, True)
        bare = os.path.join(tmp, "bare")
        _init(bare)
        _commit(bare, "only")
        code9, _, err9 = _run_tool(bare, [])
        check("missing status branch is exit 2", code9, 2)
        check("and names the fix", "--fetch" in err9, True)
        code10, _, err10 = _run_tool(repo, ["--max", "0"])
        check("--max 0 is exit 2, not a lie about the branch", code10, 2)
        check("--max 0 explains itself", "--max must be at least 1" in err10, True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("SELFTEST FAILED: %d check(s): %s" % (len(failures), ", ".join(failures)))
        return 1
    print("SELFTEST PASS")
    return 0


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="which commit of the server may I boot")
    ap.add_argument("--repo", default=".", help="path to the pirate-force-server clone")
    ap.add_argument("--branch", default=DEFAULT_BRANCH)
    ap.add_argument("--status-ref", default=DEFAULT_STATUS_REF)
    ap.add_argument("--max", type=int, default=DEFAULT_MAX,
                    help="how many first-parent commits to walk")
    ap.add_argument("--fetch", action="store_true",
                    help="fetch origin main and origin ci-status first (the only "
                         "thing this tool ever changes, and only when asked)")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--selftest", action="store_true", help="run the built-in checks and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        try:
            return selftest()
        except GitError as exc:
            sys.stderr.write("pf_resolve_green_boot selftest: %s\n" % exc)
            return 2

    repo = os.path.abspath(args.repo)
    try:
        check_repo(repo)
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

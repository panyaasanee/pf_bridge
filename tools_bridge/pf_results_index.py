#!/usr/bin/env python3
"""pf_results_index -- LANE-K clerk tool.

Reads every ``RESULT:`` line written by testers into ``notes_to_chief`` letters,
keeps the newest one per ticket, then compares it with the status token that the
ticket header currently carries in ``GAME_TEST_QUEUE.md`` / ``CLIENT_RE_QUEUE.md``.

It prints a divergence table: tickets whose header does not yet say what the
newest RESULT line says.  That table is the clerk's worklist -- it does NOT
decide anything, it only shows where the queue and the letters disagree.

ASCII-only output on purpose: the bridge console is cp874 and dies on anything
else, so ticket titles (Thai) are never echoed -- only ids, status tokens and
letter names, and every printed line is escaped to ASCII in main() before it
reaches stdout (callers that use build_report() as a library do not get that).

!! NOT TRUSTWORTHY YET (pf-adversary, LANE-K round okh8oz 2026-09-07) !!
Every "not stale" verdict here is a substring or a max()-of-dates over a header
blob that already carries several contradicting status words, so a real
regression can be reported as "agrees" and the count can print 0 while the queue
is stale.  Read the count as a floor, never as proof, and never wire this into a
gate.  Findings and the fix order: notes_to_chief/20260907_0900_LANE-K-ADVERSARY-
okh8oz-index-not-trustworthy-yet.md

Usage:
    python3 tools_bridge/pf_results_index.py [--repo DIR] [--all] [--selftest]

    --all       also list tickets whose header already agrees (default: only
                divergences and unmatched rows)
    --selftest  run the built-in assertions on the parsers and exit
"""
from __future__ import annotations

import argparse
import os
import re
import sys

LETTER_DIRS = ("notes_to_chief", os.path.join("notes_to_chief", "consumed"))
QUEUES = ("GAME_TEST_QUEUE.md", "CLIENT_RE_QUEUE.md")
# A ticket that was archived leaves a one-line stub in the queue and its real
# header (with the folded status) in the archive file, so the archive and the
# migrated big tickets are header sources too -- reading the queues alone makes
# every archived ticket look stale.
HEADER_DIRS = ("archive", "tickets")

# "RESULT: GT-281 PASS R322B 2026-09-07 00:55 (...)"
RESULT_RE = re.compile(r"^RESULT:\s+(GT|RE)-(\d+)\s+([A-Za-z0-9][A-Za-z0-9+/._-]*)\s*(.*)$")
# "## GT-281 <thai title> [<thai status blob>]"  -- emoji/markup before the id is allowed
HEADER_RE = re.compile(r"^##\s+\S*\s*(GT|RE)-(\d+)\b(.*)$")
# stamp at the head of a letter file name: 20260907_0725_...
STAMP_RE = re.compile(r"(\d{8})_(\d{4})")
# round token inside a RESULT tail: "R321", "R322B", "UA1"
ROUND_RE = re.compile(r"\b(R\d{2,4}[A-Z]?|UA\d+)\b")

# statuses that say "nothing was measured", so a header is allowed to keep
# whatever it said before -- they are reported apart, never as a divergence.
NON_RESULTS = ("NOT-RUN", "NO-RESULT", "NOT-MEASURED")
# any yyyy-mm-dd inside a header or a RESULT tail
DATE_RE = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")

# Status words a tester/ticket owner may write.  Longest first so that
# "PASS-CLIENT" is not shortened to "PASS".
STATUS_WORDS = (
    "NEGATIVE-EXPECTED", "NEGATIVE-MEASURED", "NEGATIVE-AGAIN",
    "PASS-WIRE-ONLY", "PASS-CLIENT", "PASS-AGAIN", "PARTIAL-PASS",
    "CAPTURED-AGAIN", "NOT-MEASURED", "NOT-RUN", "NO-RESULT",
    "BOUNDED-NEGATIVE", "REFUTED", "CANCELLED", "SUPERSEDED", "DUPLICATE",
    "BLOCKED", "ANSWERED", "CAPTURED", "NEGATIVE", "MIXED", "READY",
    "RUNNING", "PENDING", "CLOSED", "PASS", "FAIL", "DONE", "OPEN",
)


def _norm(token: str) -> str:
    """Reduce a status token to the coarse family the header must show."""
    up = token.upper()
    for word in STATUS_WORDS:
        if up.startswith(word):
            return word
    return up


def parse_result_lines(text: str):
    """Yield (kind, number, status, tail) for every RESULT: line in a letter."""
    out = []
    for line in text.splitlines():
        m = RESULT_RE.match(line.strip())
        if m:
            out.append((m.group(1), int(m.group(2)), m.group(3), m.group(4).strip()))
    return out


def parse_headers(text: str):
    """Yield (kind, number, header_rest) for every ticket header in a queue."""
    out = []
    for line in text.splitlines():
        m = HEADER_RE.match(line)
        if m:
            out.append((m.group(1), int(m.group(2)), m.group(3)))
    return out


def header_agrees(header_rest: str, status: str) -> bool:
    """True when the header text already carries the RESULT status family."""
    return _norm(status) in header_rest.upper()


def round_of(tail: str) -> str:
    """The round token a RESULT line was measured in, '' when it names none."""
    m = ROUND_RE.search(tail)
    return m.group(1) if m else ""


def header_cites_round(header_rest: str, tail: str) -> bool:
    """True when the header already quotes the round that produced the RESULT.

    A header worded differently from the RESULT token is not automatically
    stale: if it cites the same round, a clerk has already read that letter.
    """
    token = round_of(tail)
    return bool(token) and token in header_rest.upper()


def newest_date(text: str) -> str:
    """The latest yyyy-mm-dd written in a piece of text, '' when it has none."""
    found = DATE_RE.findall(text)
    return max(found) if found else ""


def header_is_newer(header_rest: str, tail: str) -> bool:
    """True when the header itself records a decision later than the RESULT.

    A ticket cancelled or re-closed after the tester's letter is not stale: the
    queue is ahead of the letter, which is the direction that is allowed.
    """
    head_date, res_date = newest_date(header_rest), newest_date(tail)
    return bool(head_date) and bool(res_date) and head_date > res_date


def stamp_of(filename: str) -> str:
    m = STAMP_RE.search(filename)
    return (m.group(1) + m.group(2)) if m else "00000000" + "0000"


def collect_results(repo: str):
    """ticket -> (stamp, status, letter basename, tail); newest stamp wins."""
    newest = {}
    for rel in LETTER_DIRS:
        directory = os.path.join(repo, rel)
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(directory, name)
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                rows = parse_result_lines(fh.read())
            if not rows:
                continue
            stamp = stamp_of(name)
            for kind, num, status, tail in rows:
                key = "%s-%03d" % (kind, num)
                prev = newest.get(key)
                if prev is None or stamp >= prev[0]:
                    newest[key] = (stamp, status, name, tail)
    return newest


def header_sources(repo: str):
    """Every file whose ticket headers count: queues, archives, big tickets."""
    sources = [q for q in QUEUES if os.path.isfile(os.path.join(repo, q))]
    for rel in HEADER_DIRS:
        directory = os.path.join(repo, rel)
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.endswith(".md"):
                sources.append(os.path.join(rel, name))
    return sources


def collect_headers(repo: str):
    """ticket -> list of (source file, header text)."""
    headers = {}
    for queue in header_sources(repo):
        path = os.path.join(repo, queue)
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for kind, num, rest in parse_headers(fh.read()):
                headers.setdefault("%s-%03d" % (kind, num), []).append((queue, rest))
    return headers


def build_report(results, headers, show_all=False):
    """Return (lines, divergence_count) -- ASCII only."""
    lines = []
    diverging = 0
    lines.append("%-8s %-18s %-9s %s" % ("TICKET", "NEWEST-RESULT", "HEADER", "LETTER"))
    lines.append("-" * 78)
    for key in sorted(results, key=lambda k: (k[:2], int(k[3:]))):
        stamp, status, letter, tail = results[key]
        rows = headers.get(key)
        if not rows:
            verdict = "NO-HEADER"
        elif any(header_agrees(rest, status) for _q, rest in rows):
            verdict = "agrees"
        elif _norm(status) in NON_RESULTS:
            verdict = "not-run"
        elif any(header_cites_round(rest, tail) for _q, rest in rows):
            verdict = "cites-rnd"
        elif any(header_is_newer(rest, tail) for _q, rest in rows):
            verdict = "hdr-newer"
        else:
            verdict = "DIVERGES"
        if verdict in ("DIVERGES", "NO-HEADER"):
            diverging += 1
        elif not show_all:
            continue
        lines.append("%-8s %-18s %-9s %s" % (key, _norm(status)[:18], verdict, letter[:34]))
    lines.append("-" * 78)
    lines.append("results indexed: %d   rows needing a clerk: %d" % (len(results), diverging))
    lines.append("WARNING: non-stale verdicts are substring heuristics and can hide a real"
                 " regression -- this count is a floor, not proof (see LANE-K adversary letter"
                 " 20260907_0900). Never use as a gate.")
    lines.append("verdicts: agrees=header says it | cites-rnd=header quotes that round,"
                 " wording differs | hdr-newer=queue decided later than the letter"
                 " | not-run=nothing measured | DIVERGES/NO-HEADER=clerk work")
    return lines, diverging


def selftest():
    rows = parse_result_lines(
        "noise\n"
        "RESULT: GT-281 PASS R322B 2026-09-07 00:55 (sea login)\n"
        "RESULT: RE-272 CAPTURED R321 2026-09-06 11:05-11:11\n"
        "RESULT: (none)\n"
    )
    assert rows == [("GT", 281, "PASS", "R322B 2026-09-07 00:55 (sea login)"),
                    ("RE", 272, "CAPTURED", "R321 2026-09-06 11:05-11:11")], rows
    heads = parse_headers("## GT-281 title [PASS]\n### GT-282 not a header\n## RE-234 x [DONE]\n")
    assert heads == [("GT", 281, " title [PASS]"), ("RE", 234, " x [DONE]")], heads
    assert _norm("PASS-CLIENT") == "PASS-CLIENT"
    assert _norm("PASSED") == "PASS"
    assert _norm("weird") == "WEIRD"
    assert header_agrees(" [green PASS-CLIENT closed]", "PASS-CLIENT")
    assert not header_agrees(" [OPEN]", "PASS")
    assert stamp_of("20260907_0725_LANE-K-ROUND-4af3qf.md") == "202609070725"
    assert stamp_of("no-stamp.md") == "000000000000"
    assert round_of("R322B 2026-09-07 00:55 (x)") == "R322B"
    assert round_of("2026-09-07 no round") == ""
    assert header_cites_round(" [folded R321 blocked]", "R321 2026-09-06")
    assert not header_cites_round(" [folded R307]", "R321 2026-09-06")
    assert not header_cites_round(" [folded R321]", "no round here")
    mixed = {"GT-220": ("202609061255", "BLOCKED", "l.md", "R321 2026-09-06")}
    lines, diverged = build_report(mixed, {"GT-220": [("GAME_TEST_QUEUE.md", " [PASS R307, retry R321]")]})
    assert diverged == 0 and any("cites-rnd" in ln for ln in lines), lines
    nr = {"GT-262": ("202609061255", "NOT-RUN", "l.md", "R321 2026-09-06 (time)")}
    lines, diverged = build_report(nr, {"GT-262": [("GAME_TEST_QUEUE.md", " [READY]")]}, show_all=True)
    assert diverged == 0 and any("not-run" in ln for ln in lines), lines
    assert newest_date("closed 2026-09-07T06:03 after 2026-09-02") == "2026-09-07"
    assert newest_date("no date") == ""
    assert newest_date("stamp 20260907 is not a date") == ""
    assert header_is_newer(" [CANCELLED 2026-09-07]", "R303 2026-09-02")
    assert not header_is_newer(" [PASS 2026-09-01]", "R303 2026-09-02")
    assert not header_is_newer(" [PASS]", "R303 2026-09-02")
    late = {"GT-193": ("202609021755", "FAIL", "l.md", "R303 2026-09-02")}
    lines, diverged = build_report(late, {"GT-193": [("archive/x.md", " [CANCELLED 2026-09-07]")]}, show_all=True)
    assert diverged == 0 and any("hdr-newer" in ln for ln in lines), lines
    res = {"GT-281": ("202609070055", "PASS", "letter.md", "")}
    lines, diverged = build_report(res, {"GT-281": [("GAME_TEST_QUEUE.md", " [OPEN]")]})
    assert diverged == 1 and any("DIVERGES" in ln for ln in lines)
    lines, diverged = build_report(res, {"GT-281": [("GAME_TEST_QUEUE.md", " [PASS]")]})
    assert diverged == 0, lines
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isfile(os.path.join(here, "GAME_TEST_QUEUE.md")):
        src = header_sources(here)
        assert "GAME_TEST_QUEUE.md" in src and "CLIENT_RE_QUEUE.md" in src, src
        assert any(s.startswith("archive" + os.sep) for s in src), "archive not scanned"
    print("selftest OK")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="LANE-K results index")
    parser.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--all", action="store_true", help="also list agreeing tickets")
    parser.add_argument("--selftest", action="store_true", help="run built-in assertions")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    results = collect_results(args.repo)
    headers = collect_headers(args.repo)
    lines, _diverging = build_report(results, headers, show_all=args.all)
    for line in lines:
        # the bridge console is cp874: never let a Thai ticket title or an emoji
        # that slipped into a letter name reach stdout as itself.
        print(line.encode("ascii", "backslashreplace").decode("ascii"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

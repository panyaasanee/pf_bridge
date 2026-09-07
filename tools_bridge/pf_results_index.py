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

!! AGREEMENT WAS WIDENED IN ROUND kq7m3d (2026-09-07) -- READ THIS BEFORE
TRUSTING ANY "agrees" BELOW.  closure_verdict() lets a header whose current
status is the BARE bookkeeping word CLOSED also agree with a verdict written
within 40 characters after it, so "CLOSED -- FAIL" stops disagreeing with its
own FAIL letter.  Effect measured on the two live queues that day: 9 (header,
status) pairs flipped False -> True and one row left the clerk worklist
(GT-218).  The first cut of the rule ALSO agreed with a verdict belonging to a
DIFFERENT ticket ("CLOSED -- see RE-198 PASS", "CLOSED-DUPLICATE of GT-216
which is PASS"); pf-adversary found it the same round and it now refuses a
qualified closure word, a ticket id in the gap, or decision prose in any case.
The 49-of-551 figure below was measured BEFORE that rule and has not been
recomputed.

!! STILL A FLOOR, NOT PROOF (pf-adversary, LANE-K round okh8oz 2026-09-07) !!
Round ek1gk9 fixed the three findings COO ordered first (NOW.md 0845):
  D1  agreement reads the header's CURRENT status (the first status word), not a
      substring of a blob that carries several contradicting verdicts at once.
  D2  hdr-newer needs THIS ticket's own terminal decision, dated next to that
      decision -- an ordinary clerk touch no longer buys immunity.
  D12 --strict exits 2 when rows still need a clerk.
!! THE D1 RULE IS STILL A GUESS ABOUT PROSE, BUT TWO OF ITS FALSE-GREEN PATHS
ARE NOW CLOSED (found by pf-adversary in round ek1gk9; closed and re-measured
by LANE-K in round k01t0u) !!  "The house writes the live verdict first" is not
a convention the queue files are linted against.  Measured over 551 headers on
2026-09-07: 49 of them now resolve to a different family than before -- 35
because a struck span no longer counts, 16 because a hyphenated qualifier is no
longer dropped.  Where it stands:
  - CLOSED (round k01t0u): 35 headers put the first status word inside
    ~~strikethrough~~, i.e. on the one verdict the house explicitly RETRACTED.
    strip_struck() blanks those spans before the search, so a RESULT carrying a
    retracted status is no longer reported as "agrees".  Measured:
    header_agrees(" [~~[BLOCKED]~~ ~~[READY]~~ **[PASS]**]", "BLOCKED") was
    True and is now False, and the same header still agrees with PASS.
  - CLOSED (round k01t0u): the boundary rule let "-" pass on the right, so
    PASS-PARTIAL and PASS-PERSISTENT-SURVIVAL read as plain PASS.  A trailing
    qualifier is now part of the family unless it is listed in
    QUALIFIERS_THAT_DO_NOT_NARROW, so an unknown qualifier fails CLOSED (the row
    is reported for a clerk) instead of agreeing.  Measured:
    header_agrees(" [**PASS-PARTIAL (box P4)**]", "PASS") was True and is now
    False; REFUTED-ON-SCREEN still agrees with REFUTED.
  - CLOSED (round k01t0u, from pf-adversary D1/D12): the search is now CASE
    SENSITIVE, so lower-case English prose in a header is not a verdict.  The
    live example the reviewer found: tickets/GT-288.md carries the clerk's own
    pointer sentence "(steps / pass criteria / ...)", which an uppercased search
    read as ('PASS', 137).  A RESULT: GT-288 PASS would then have matched that
    source, scored "agrees" and been SUPPRESSED while the live queue header still
    said PENDING.  Reproduced and re-measured: the row is now reported.  The same
    change stops the 102 archival-boilerplate headers below from counting the
    lower-case bookkeeping word "closed" as a verdict -- they now report as clerk
    work.  PARTIAL was also added to STATUS_WORDS: RE-273 was folded to PARTIAL
    and NEITHER clerk tool could read it, so both called the ticket OPEN.
  - WAS STILL OPEN, now covered by the case rule: 102 headers take their status
    from the archival boilerplate
    "-- archived <date> (closed; verbatim in archive/...)", where "closed" is
    filesystem bookkeeping, not a verdict.  Those all count as TERMINAL, so one
    clerk edit that dates such a stub with yyyy-mm-dd re-opens D2 through D1.
  - STILL OPEN: 19 take it from English prose or a filename in the title ("does
    the window finally open", "...M1P-RESULT-PASS-*.md").
!! NEITHER CLOSURE CHANGED A SINGLE ROW OF TODAY'S OUTPUT !!  Before and after,
this tool reports the same two rows (GT-204, GT-218).  What was fixed is a path
that would have gone false-GREEN on some future letter, not a wrong answer being
given today.  Do not read the closures as evidence the queue got truer.
The two rows this fix first reported (GT-204, GT-218) were both FALSE ALARMS,
re-measured: GT-218's header and letter agree (CLOSED wrapping FAIL), and
GT-204 was cancelled after its letter but carries no yyyy-mm-dd date at all, so
hdr-newer is structurally unable to fire for it or for 23 other headers.
The real fix is a machine-readable status field the queues are linted against,
not a better guess at prose.  Until then treat every "agrees" as unproven.

Not fixed, so a clean run still does NOT mean the queue is true: D3 (a round
token in a header does not prove that letter was read), D4 (a twin in
consumed/ wins on an equal stamp), D9 (a two-layer status is reported by its
positive half), D10 (a malformed RESULT: line is dropped with no counter).
!! Never wire this into a gate (COO 0845 item 1).  Letters with no RESULT: line
are invisible here -- tools_bridge/pf_re_queue_taglint.py is the second source
and today sees 18 rows this tool cannot.  Findings and the full fix order:
notes_to_chief/20260907_0900_LANE-K-ADVERSARY-okh8oz-index-not-trustworthy-yet.md

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
# "## GT-281 <thai title> [<thai status blob>]"  -- emoji/markup before the id is
# allowed.  The negative lookahead keeps GT-030-R3 / GT-084-R2 out: they are
# separate round-2/round-3 tickets, and folding them onto GT-030 / GT-084 made
# this tool grade each one against the other's header.
HEADER_RE = re.compile(r"^##\s+\S*\s*(GT|RE)-(\d+)(?!-R\d)\b(.*)$")
# stamp at the head of a letter file name: 20260907_0725_...
STAMP_RE = re.compile(r"(\d{8})_(\d{4})")
# round token inside a RESULT tail: "R321", "R322B", "UA1"
ROUND_RE = re.compile(r"\b(R\d{2,4}[A-Z]?|UA\d+)\b")

# statuses that say "nothing was measured", so a header is allowed to keep
# whatever it said before -- they are reported apart, never as a divergence.
NON_RESULTS = ("NOT-RUN", "NO-RESULT", "NOT-MEASURED")
# any yyyy-mm-dd inside a header or a RESULT tail
DATE_RE = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")

# A header standing on one of these words has had a decision taken ON THIS
# TICKET, which may legitimately post-date a tester letter (cancelled, folded
# shut, superseded).  Any other current status means the queue is merely being
# maintained, and maintenance must never buy immunity from a new result.
TERMINAL_WORDS = (
    "CANCELLED", "SUPERSEDED", "DUPLICATE", "CLOSED", "ANSWERED", "REFUTED",
)
# how far after the current status word a date still counts as that decision's
# own date -- a header line here runs for thousands of characters and carries
# the dates of every earlier verdict, so the window has to be short.
DECISION_DATE_WINDOW = 200

# Status words a tester/ticket owner may write.  Longest first so that
# "PASS-CLIENT" is not shortened to "PASS".
STATUS_WORDS = (
    "NEGATIVE-EXPECTED", "NEGATIVE-MEASURED", "NEGATIVE-AGAIN",
    "PASS-WIRE-ONLY", "PASS-CLIENT", "PASS-AGAIN", "PARTIAL-PASS",
    "CAPTURED-AGAIN", "NOT-MEASURED", "NOT-RUN", "NO-RESULT",
    "BOUNDED-NEGATIVE", "REFUTED", "CANCELLED", "SUPERSEDED", "DUPLICATE",
    "BLOCKED", "ANSWERED", "CAPTURED", "NEGATIVE", "PARTIAL", "MIXED", "READY",
    "RUNNING", "PENDING", "CLOSED", "PASS", "FAIL", "DONE", "OPEN",
)

# Suffixes measured in this house to say WHERE or HOW OFTEN a verdict was
# reached, not to narrow it: REFUTED-ON-SCREEN is still REFUTED.  Everything
# else after a "-" narrows the verdict (PASS-PARTIAL is not PASS), so it stays
# part of the family and the row is reported for a clerk to read.  This is an
# enumeration, not a rule -- a new suffix defaults to "narrows", which is the
# direction that fails closed.
QUALIFIERS_THAT_DO_NOT_NARROW = frozenset({
    "ON-SCREEN", "ON-CLIENT", "ON-WIRE", "MEASURED", "AGAIN", "CONFIRMED",
    "OBSERVED", "V2", "V3", "R2", "R3",
})


def _norm(token: str) -> str:
    """Reduce a status token to the coarse family the header must show.

    Uses the same qualifier rule as current_status(), so a letter that reports
    PASS-PARTIAL is compared against the header's PASS-PARTIAL and not against
    a plain PASS.  Without this the two halves of the comparison disagree about
    what a family is and a narrowed verdict silently matches the broad one.
    """
    up = token.upper()
    for word in STATUS_WORDS:
        if up.startswith(word):
            return _with_qualifier(up, 0, word)
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


def strip_struck(header_rest: str) -> str:
    """Blank out every ~~struck-out~~ span, keeping the string's length.

    D1-strike, measured by pf-adversary in round `ek1gk9` and re-measured by
    this lane on 37 real headers: the house retracts a verdict by striking it
    through and writing the live one after it, so the FIRST status word in the
    raw header is frequently the one word the house has explicitly withdrawn.
    header_agrees() then reported a RESULT carrying that withdrawn status as
    "agrees" and suppressed the row -- D1's own false-GREEN path.

    Spans are replaced by spaces rather than deleted so that every offset
    header_is_newer() computes against the uppercased header stays valid.  An
    unpaired "~~" closes nothing and is left alone, because a header with an odd
    number of markers is malformed and guessing where the author meant the strike
    to end would be a second guess on top of the one this function removes.
    """
    out = list(header_rest)
    i = header_rest.find("~~")
    while i != -1:
        j = header_rest.find("~~", i + 2)
        if j == -1:
            break
        for k in range(i, j + 2):
            out[k] = " "
        i = header_rest.find("~~", j + 2)
    return "".join(out)


def current_status(header_rest: str):
    """(family, offset-into-uppercased-header) the header currently stands on.

    D1: the house writes the live verdict first and the history after it, so the
    FIRST status word in the header is the ticket's current status.  Matching a
    substring against the whole blob instead -- what this tool did until now --
    makes a header that carries PASS, FAIL, NO-RESULT and READY at once agree
    with all four of them, so a fresh FAIL on a ticket that says PASS today was
    reported as "agrees".  Measured on the real GT-213 header.

    Struck-out spans are removed first (see strip_struck), so a retracted
    verdict can no longer be read as the live one.

    Longest word wins at a tie (STATUS_WORDS is ordered longest first), and a
    match only counts on a word boundary, so PASS does not fire inside
    PASS-CLIENT or PARTIAL-PASS.

    D9: a "-" on the RIGHT is no longer waved through as a boundary.  A word
    followed by "-<qualifier>" is returned as the FULL hyphenated token, so
    PASS-PARTIAL is its own family and can never satisfy a plain PASS result.
    That fails CLOSED: an unknown qualifier reports as clerk work instead of a
    silent agreement.  QUALIFIERS_THAT_DO_NOT_NARROW lists the suffixes this
    house has measured to be a location or a repeat rather than a narrowing of
    the verdict, and only those collapse back to the base word.
    """
    # D1-prose (pf-adversary round k01t0u): the search is CASE SENSITIVE against
    # the header as written.  This house writes a verdict in capitals; ordinary
    # English prose in a header is lower case, and an uppercased blob let the
    # phrase "pass criteria" -- what a clerk naturally writes when pointing at a
    # ticket body -- read as a live PASS.  Measured on the real tickets/GT-288.md
    # header: uppercased search returned ('PASS', 137), case-sensitive returns
    # the header's actual status.  This also stops the 102 headers whose only
    # status word is the lower-case "closed" of the archival boilerplate
    # "-- archived <date> (closed; verbatim in archive/...)" from counting that
    # bookkeeping word as a verdict; they now report as clerk work, which is the
    # direction that fails closed.
    kept = strip_struck(header_rest)
    up = kept.upper()
    best_word, best_idx = "", len(up) + 1
    for word in STATUS_WORDS:
        idx = kept.find(word)
        while idx != -1:
            before = up[idx - 1] if idx else " "
            after = up[idx + len(word)] if idx + len(word) < len(up) else " "
            # "_" is never a boundary, or test_pass_client in a header reads as
            # PASS.  "-" blocks on the LEFT, so PASS inside PARTIAL-PASS is
            # rejected; on the RIGHT it is handled by _with_qualifier below.
            if not (before.isalnum() or before in "-_") and not (after.isalnum() or after == "_"):
                if idx < best_idx:
                    best_word, best_idx = _with_qualifier(up, idx, word), idx
                break
            idx = kept.find(word, idx + 1)
    return (best_word, best_idx) if best_word else ("", -1)


def _with_qualifier(up: str, idx: int, word: str) -> str:
    """The family for a status word, widened to include a narrowing qualifier."""
    rest = up[idx + len(word):]
    if not rest.startswith("-"):
        return word
    m = re.match(r"-([A-Z0-9]+(?:-[A-Z0-9]+)*)", rest)
    if not m:
        return word
    suffix = m.group(1)
    if suffix in QUALIFIERS_THAT_DO_NOT_NARROW:
        return word
    for known in QUALIFIERS_THAT_DO_NOT_NARROW:
        if suffix.startswith(known + "-"):
            return word
    return word + "-" + suffix


# A header may close a ticket with a bookkeeping word and then write the
# verdict immediately after it ("**CLOSED** -- **FAIL** OBSERVER_CONFIRMED ...").
# current_status() reports the FIRST status word, so such a header used to
# disagree with its own verdict.
#
# !! pf-adversary D2, round kq7m3d: the first cut of this rule only checked that
# the FIRST word was a closure word, so "CLOSED-DUPLICATE of GT-216 which is
# PASS" and "CLOSED -- see RE-198 PASS" both scored "agrees" -- matching a
# verdict that belongs to a DIFFERENT ticket, which is the exact thing the
# comment promised to block.  The pairing now refuses in every direction it
# cannot read: a qualified closure word, another ticket id between the two
# words, or a decision word in any case.  Refusing sends the row to a clerk,
# which is the direction that fails closed.
CLOSURE_WORDS = ("CLOSED",)
# how far after the closure word the verdict may sit and still be that closure's
# own verdict.  Short on purpose: a header line runs for thousands of characters
# and carries the words of every earlier round.
CLOSURE_PAIR_WINDOW = 40
# any ticket id inside the window means the verdict may be that OTHER ticket's
TICKET_ID_RE = re.compile(r"\b(?:GT|RE)-\d+")
# a decision about THIS ticket, written in any case, is not bookkeeping -- a
# cancelled/superseded/duplicate ticket carrying a tester PASS must keep
# diverging.  "covered"/"see" mark the verdict as somebody else's.
DECISION_PROSE_RE = re.compile(
    r"(?i)\b(duplicate|superseded|supersedes|cancelled|canceled|covered|see)\b")


def closure_verdict(header_rest: str):
    """The verdict a bookkeeping closure word carries, or ("", -1).

    Returns the first status word that starts within CLOSURE_PAIR_WINDOW
    characters after a current status that is a BARE closure word, and only when
    the text in between names no other ticket and no decision about this one.
    """
    word, idx = current_status(header_rest)
    # a qualified closure word (CLOSED-DUPLICATE) is a decision, not bookkeeping
    if word not in CLOSURE_WORDS:
        return ("", -1)
    kept = strip_struck(header_rest)
    tail_at = idx + len(word)
    tail = kept[tail_at:tail_at + CLOSURE_PAIR_WINDOW]
    nxt, nxt_idx = current_status(tail)
    if not nxt or nxt.split("-")[0] in CLOSURE_WORDS:
        return ("", -1)
    between = tail[:nxt_idx]
    if TICKET_ID_RE.search(between) or DECISION_PROSE_RE.search(between):
        return ("", -1)
    return (nxt, tail_at + nxt_idx)


def header_agrees(header_rest: str, status: str) -> bool:
    """True when the header's CURRENT status is the RESULT status family."""
    family = _norm(status)
    if not family:
        return False
    if current_status(header_rest)[0] == family:
        return True
    return closure_verdict(header_rest)[0] == family


def header_mentions_elsewhere(header_rest: str, status: str) -> bool:
    """True when the family is written in the header but is NOT its status now.

    Reported as its own verdict rather than folded into DIVERGES: the clerk is
    looking at a header whose history already contains this word, which is the
    exact shape that used to be silently called "agrees", so it deserves to be
    read rather than skimmed.  It is still clerk work either way.
    """
    family = _norm(status)
    if not family or header_agrees(header_rest, status):
        return False
    return family in header_rest.upper()


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
    """True when THIS ticket's own current decision post-dates the RESULT.

    A ticket cancelled or folded shut after the tester's letter is not stale:
    the queue is ahead of the letter, which is the direction that is allowed.

    D2: until now this compared the newest date ANYWHERE in the header blob with
    the newest date in the RESULT tail.  Every clerk touch writes a fresh date
    into the header, so the more a ticket was maintained the more permanently
    immune it became to a new negative result -- 6 of 29 tickets already had
    that shape.  The date now has to belong to this ticket's own current
    decision: the header must currently STAND ON a terminal word, and the date
    must be written next to that word, not anywhere in its history.
    """
    word, idx = current_status(header_rest)
    if word not in TERMINAL_WORDS:
        return False
    res_date = newest_date(tail)
    if not res_date:
        return False
    head_date = newest_date(header_rest.upper()[idx:idx + DECISION_DATE_WINDOW])
    return bool(head_date) and head_date > res_date


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
        elif any(header_mentions_elsewhere(rest, status) for _q, rest in rows):
            verdict = "HDR-ELSE"
        else:
            verdict = "DIVERGES"
        if verdict in ("DIVERGES", "NO-HEADER", "HDR-ELSE"):
            diverging += 1
        elif not show_all:
            continue
        lines.append("%-8s %-18s %-9s %s" % (key, _norm(status)[:18], verdict, letter[:34]))
    lines.append("-" * 78)
    lines.append("results indexed: %d   rows needing a clerk: %d" % (len(results), diverging))
    lines.append("WARNING: the D1 rule ('first status word = current status') is still a"
                 " guess about prose.  Four false-GREEN paths were closed in round k01t0u"
                 " (~~struck-out~~ spans; PASS-PARTIAL reading as PASS; lower-case English"
                 " prose such as 'pass criteria' reading as PASS; PARTIAL unreadable) and"
                 " NONE of them changed a row of this output.  What is still unfixed: the"
                 " 19 headers that take a status from a filename in the title, D3, D4 and"
                 " D10.  Every 'agrees' is still unproven.")
    lines.append("WARNING: this count is a floor, not proof, and every 'agrees' is unproven"
                 " (LANE-K letters 20260907_0900 and 20260907_0950). Never use as a gate.")
    lines.append("SECOND SOURCE: tools_bridge/pf_re_queue_taglint.py reads letters with no"
                 " RESULT: line and sees rows this tool cannot. Run both; neither alone is"
                 " the queue's truth.")
    lines.append("verdicts: agrees=header STANDS ON it | cites-rnd=header quotes that"
                 " round, wording differs | hdr-newer=this ticket's own terminal decision"
                 " is dated later | not-run=nothing measured"
                 " | HDR-ELSE=word is in the header history but is not the status now"
                 " | DIVERGES/NO-HEADER=clerk work")
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

    # --- D1-strike: a retracted verdict must never be the current status ---
    struck = " [~~[BLOCKED]~~ ~~[READY]~~ **[PASS]** folded]"
    assert strip_struck(struck).count("~") == 0
    assert len(strip_struck(struck)) == len(struck), "offsets must survive"
    assert current_status(struck)[0] == "PASS"
    assert not header_agrees(struck, "BLOCKED"), "struck verdict read as live"
    assert not header_agrees(struck, "READY")
    assert header_agrees(struck, "PASS")
    assert strip_struck(" [~~unclosed PASS]") == " [~~unclosed PASS]"

    # --- D9: a narrowing qualifier is part of the family, both sides ---
    partial = " [**PASS-PARTIAL (box P4)** later READY]"
    assert current_status(partial)[0] == "PASS-PARTIAL"
    assert not header_agrees(partial, "PASS"), "PASS-PARTIAL satisfied a plain PASS"
    assert header_agrees(partial, "PASS-PARTIAL")
    assert _norm("PASS-PARTIAL") == "PASS-PARTIAL", "_norm must use the same rule"
    assert _norm("PASS") == "PASS"
    # an unknown qualifier fails closed rather than agreeing with the base word
    assert not header_agrees(" [**PASS-SOMETHING-NEW**]", "PASS")
    # a qualifier that only says where/how often still collapses
    assert current_status(" [**REFUTED-ON-SCREEN (R318)**]")[0] == "REFUTED"
    assert header_agrees(" [**REFUTED-ON-SCREEN (R318)**]", "REFUTED")

    # --- D1-prose: English prose in a header is not a verdict ---
    prose = " [PENDING] -- this file is the ticket body (steps / pass criteria / nonclaims)"
    assert current_status(prose)[0] == "PENDING", current_status(prose)
    assert not header_agrees(prose, "PASS"), "lower-case prose read as a verdict"
    assert current_status(" -- archived 20260906 (closed; verbatim in archive/x.md)")[0] == ""
    assert current_status(" [**PASS** folded]")[0] == "PASS"
    # a header source with no verdict must not lend one to a sibling source
    both = [("GAME_TEST_QUEUE.md", " [PENDING]"), ("tickets/GT-000.md", prose)]
    lines, diverged = build_report(
        {"GT-000": ("202609081200", "PASS", "fake.md", "R400 2026-09-08")}, {"GT-000": both})
    assert diverged == 1 and len([ln for ln in lines if ln.startswith("GT-000")]) == 1, lines

    # --- closure word + verdict written next to it (LANE-K round kq7m3d) ---
    # measured on the real GAME_TEST_QUEUE.md GT-218 stub, which reported
    # HDR-ELSE against its own OBSERVER_CONFIRMED FAIL letter before this rule.
    closed_fail = (" [**CLOSED** -- \u274c **FAIL \u00b7 OBSERVER_CONFIRMED"
                   " 2026-09-03T16:51+07:00** -- archived 20260906 (closed;"
                   " verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)")
    assert current_status(closed_fail)[0] == "CLOSED", current_status(closed_fail)
    assert closure_verdict(closed_fail)[0] == "FAIL", closure_verdict(closed_fail)
    assert header_agrees(closed_fail, "FAIL")
    # NEGATIVE CONTROLS (pf-adversary D2: the first cut had none that could fail
    # -- its only "wrong verdict" input contained no verdict at all).  Each line
    # below carries a REAL verdict word that the rule must refuse to borrow.
    borrowed = " [**CLOSED** -- see `RE-198` **PASS**, this one was never run]"
    assert current_status(borrowed)[0] == "CLOSED", current_status(borrowed)
    assert closure_verdict(borrowed) == ("", -1), closure_verdict(borrowed)
    assert not header_agrees(borrowed, "PASS"), "verdict borrowed from another ticket"
    qualified = " [**CLOSED-DUPLICATE** of `GT-216` which is **PASS**]"
    assert closure_verdict(qualified) == ("", -1), closure_verdict(qualified)
    assert not header_agrees(qualified, "PASS")
    lower_prose = " [**CLOSED** -- duplicate of that one (**PASS** there)]"
    assert closure_verdict(lower_prose) == ("", -1), closure_verdict(lower_prose)
    assert not header_agrees(lower_prose, "PASS")
    # and a plain bookkeeping close with its own verdict still pairs
    assert closure_verdict(" [**CLOSED** **DONE** 2026-09-05]")[0] == "DONE"
    # CANCELLED is a decision about the ticket, not bookkeeping: a PASS letter
    # against a cancelled header still has to reach a clerk (real GT-204).
    cancelled = " [\u274c **CANCELLED - covered by GT-216** -- `GT-216` PASS on screen]"
    assert current_status(cancelled)[0] == "CANCELLED", current_status(cancelled)
    assert closure_verdict(cancelled) == ("", -1)
    assert not header_agrees(cancelled, "PASS")
    # the window is short: a verdict far down the same header is not paired
    assert closure_verdict(" [**CLOSED**" + " x" * 60 + " **FAIL**]") == ("", -1)
    # a header with no closure word is untouched by the new rule
    assert closure_verdict(" [**PASS** folded]") == ("", -1)

    # --- D12: PARTIAL is a status word both clerk tools can read ---
    assert "PARTIAL" in STATUS_WORDS
    assert current_status(" [\U0001F527 **PARTIAL (route 1 answered)** was OPEN]")[0] == "PARTIAL"

    # --- the verdict is read off the ROW, not off the report's legend ---
    struck_rows = {"GT-999": ("202609071215", "BLOCKED", "l.md", "R400 2026-09-07")}
    lines, diverged = build_report(struck_rows, {"GT-999": [("GAME_TEST_QUEUE.md", struck)]})
    row = [ln for ln in lines if ln.startswith("GT-999")]
    assert len(row) == 1, lines
    assert row[0].split()[2] in ("DIVERGES", "HDR-ELSE"), row[0]
    assert diverged == 1, diverged
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
    # --- D1: a header standing on PASS must not agree with a fresh FAIL -------
    # shape of the real GT-213 header: PASS first, then NO-RESULT, then READY.
    gt213 = " [LANE-K folded R307 -- PASS on (A) and (B) - (C) NO-RESULT - READY (R306)]"
    assert current_status(gt213)[0] == "PASS", current_status(gt213)
    assert header_agrees(gt213, "PASS")
    assert not header_agrees(gt213, "FAIL")
    assert not header_agrees(gt213, "READY")
    assert header_mentions_elsewhere(gt213, "READY")
    assert not header_mentions_elsewhere(gt213, "PASS")
    assert not header_mentions_elsewhere(gt213, "FAIL")
    assert current_status(" [PARTIAL-PASS today]")[0] == "PARTIAL-PASS"
    assert current_status(" [no status word here]")[0] == ""
    assert not header_agrees(" [no status word here]", "PASS")
    d1 = {"GT-213": ("202609070055", "FAIL", "l.md", "")}
    lines, diverged = build_report(d1, {"GT-213": [("GAME_TEST_QUEUE.md", gt213)]})
    assert diverged == 1 and any("HDR-ELSE" in ln for ln in lines), lines

    # a hyphenated compound the house really writes, and a python identifier
    assert current_status(" [primary hypothesis REFUTED-ON-SCREEN (R318)]")[0] == "REFUTED"
    assert current_status(" [green -- test_pass_client is pinned]")[0] == ""
    assert current_status(" [PARTIAL-PASS after retry]")[0] == "PARTIAL-PASS"
    assert current_status(" [PASS-CLIENT confirmed]")[0] == "PASS-CLIENT"
    # a round-2 ticket is a different ticket, not a header for the round-1 one
    rr = parse_headers("## GT-030 a [OPEN]\n## GT-030-R3 b [PASS]\n## GT-084-R2 c [DONE]\n")
    assert rr == [("GT", 30, " a [OPEN]")], rr

    # --- D2: a clerk touch must not buy immunity -----------------------------
    touched = " [READY -- reviewed by the clerk 2026-09-07, still open]"
    assert not header_is_newer(touched, "R303 2026-09-02")
    far = " [CANCELLED by owner] " + ("x" * DECISION_DATE_WINDOW) + " 2026-09-07"
    assert not header_is_newer(far, "R303 2026-09-02"), "date outside the window counted"
    near = " [CANCELLED by owner LANE-A round lnq6xy 2026-09-07T06:03+07:00]"
    assert header_is_newer(near, "R303 2026-09-02")
    assert not header_is_newer(near, "R303 2026-09-08"), "older header must not win"
    d2 = {"GT-999": ("202609070055", "FAIL", "l.md", "R303 2026-09-02")}
    lines, diverged = build_report(d2, {"GT-999": [("GAME_TEST_QUEUE.md", touched)]})
    assert diverged == 1 and any("DIVERGES" in ln for ln in lines), lines

    # --- D12: --strict is the only thing that returns non-zero ---------------
    assert TERMINAL_WORDS and "PASS" not in TERMINAL_WORDS and "READY" not in TERMINAL_WORDS

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
    parser.add_argument("--strict", action="store_true",
                        help="exit 2 when any row still needs a clerk (D12). For a human"
                             " running the tool by hand -- this tool is a floor, not proof,"
                             " so it must not be wired into any gate (COO 0845 item 1).")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    results = collect_results(args.repo)
    headers = collect_headers(args.repo)
    lines, diverging = build_report(results, headers, show_all=args.all)
    for line in lines:
        # the bridge console is cp874: never let a Thai ticket title or an emoji
        # that slipped into a letter name reach stdout as itself.
        print(line.encode("ascii", "backslashreplace").decode("ascii"))
    # D12: main() used to return 0 whatever it found, so a caller could not tell
    # a clean run from a stale queue.  Non-zero is opt-in via --strict so that
    # nothing already calling this tool changes behaviour underneath it.
    if args.strict and diverging:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

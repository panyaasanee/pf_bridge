"""pf_re_queue_taglint.py -- guard the two halves of the RE runner's filter.

Why this exists
---------------
The RE runner on the bridge selects a ticket with an AND of two hand-typed
tags in the ticket header:

    route tag   : STATIC-ON-BRIDGE | STATIC-ON-CLOUD | NEEDS-ATTENDED-CAPTURE
    status tag  : OPEN | PENDING
    plus        : no result letter in notes_to_chief/

Nothing validated that both halves were present, so the queue has now failed
twice in the same way, once for each half:

  R276 (2026-08-31) : tickets from RE-167 on carried [OPEN - assigned LANE-x]
                      and dropped the route tag  -> runner idle 30h
  R287-R292         : tickets from RE-191 on carry [STATIC-ON-BRIDGE] and
                      dropped the status tag     -> runner idle 12h+

This script reads the queue and prints every ticket the runner cannot see,
so the failure is measured instead of noticed by accident.

Usage:  python tools_bridge/pf_re_queue_taglint.py [--queue CLIENT_RE_QUEUE.md]
Exit:   0 = nothing invisible, 1 = at least one invisible ticket, 2 = error
Output is ASCII only (cp874 console safe).
"""

import argparse
import os
import re
import sys

ROUTE_TAGS = ("STATIC-ON-BRIDGE", "STATIC-ON-CLOUD", "NEEDS-ATTENDED-CAPTURE")
STATUS_TAGS = ("OPEN", "PENDING")
# "ANSWERED" was missing here until R298 and RE-136 sat in the [A] column for
# four days because of it: its header has said
# "ANSWERED (source layer) by chief round wi1m62" since 2026-08-29, which is a
# closed ticket by every reading except this tuple's.  A closed word that the
# queue's authors actually use and this tool does not know is worse than no
# check at all -- it reports work that does not exist, every round, forever.
# Words that, in a ticket HEADER, mean the ticket is finished.  "ANSWERED" and
# "answered" are here because this queue closes some tickets in-round with no
# separate result letter ("opened and answered same round" -- see RE-169).
CLOSED_WORDS = ("DONE", "CLOSED", "ARCHIVED", "archived", "OPENED-IN-ERROR",
                "METHOD-FAIL", "SUPERSEDED", "ANSWERED", "answered")
# ANSWERED is deliberately NOT in the tuple above: it is a substring match
# against the whole header line, and this queue writes two-layer verdicts.
# pf-adversary (round dfx8bu) measured two live headers that a plain
# "ANSWERED" in CLOSED_WORDS would have closed while they are half open --
# RE-167 and RE-168 both read
#   "wire/DB **ANSWERED** ..., **client-observable STILL PENDING**"
# and both are masked today only by has_result_letter, which stops masking
# them the next time consumed letters are archived out of notes_to_chief/.
# It also matches "UNANSWERED", which is live vocabulary in the sibling
# queue, so the word alone would close a ticket that says the opposite.
# The rule below is therefore: ANSWERED closes a ticket only when nothing
# in the same header still says it is open.
MIN_PLAUSIBLE_TICKETS = 40
ANSWERED_WORD = "ANSWERED"
ANSWERED_NEGATIONS = ("UNANSWERED", "UN-ANSWERED", "NOT ANSWERED",
                      "ANSWERED-DIFFERENTLY")


def answered_means_closed(head_live):
    """True only for a header whose ANSWERED is not contradicted by itself.

    Layer awareness, not word matching: a header that answers the wire/DB
    half and says the client-observable half is still pending is an OPEN
    ticket that happens to contain the word.
    """
    if ANSWERED_WORD not in head_live:
        return False
    upper = head_live.upper()
    if any(n in upper for n in ANSWERED_NEGATIONS):
        return False
    return not any(s in head_live for s in STATUS_TAGS)
TICKET_RE = re.compile(r"^##\s.*?\b(RE|GT)-(\d{3})\b")
STRIKE_RE = re.compile(r"~~.*?~~", re.S)
# The Thai heading that opens every ticket's consumer-contract section,
# written with escapes so this file stays pure ASCII for the cp874 console.
CONSUMER_MARK = ("\u0e2a\u0e31\u0e0d\u0e0d\u0e32\u0e1c\u0e39\u0e49"
                 "\u0e1a\u0e23\u0e34\u0e42\u0e20\u0e04")


def strip_struck(text):
    """Remove ~~struck through~~ spans -- a struck OPEN is not a live status."""
    return STRIKE_RE.sub(" ", text)


def load_result_index(notes_dir):
    names = []
    if os.path.isdir(notes_dir):
        names = os.listdir(notes_dir)
    return names


def has_result_letter(ticket_id, names):
    for n in names:
        if ticket_id in n and "RESULT" in n.upper():
            return n
    return ""


def split_tickets(lines):
    starts = [i for i, l in enumerate(lines) if TICKET_RE.match(l)]
    starts.append(len(lines))
    out = []
    for k in range(len(starts) - 1):
        s, e = starts[k], starts[k + 1]
        m = TICKET_RE.match(lines[s])
        out.append({
            "id": "%s-%s" % (m.group(1), m.group(2)),
            "num": int(m.group(2)),
            "line": s + 1,
            "header": lines[s],
            "body": "\n".join(lines[s:e]),
        })
    return out


def audit(queue_path, notes_dir, min_num):
    with open(queue_path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    names = load_result_index(notes_dir)
    tickets = split_tickets(lines)

    invisible, no_route, orphan, eligible = [], [], [], []
    for t in tickets:
        head_live = strip_struck(t["header"])
        route = [r for r in ROUTE_TAGS if r in head_live]
        status = [s for s in STATUS_TAGS if s in head_live]
        closed = (any(w in head_live for w in CLOSED_WORDS)
                  or answered_means_closed(head_live))
        letter = has_result_letter(t["id"], names)

        # a block that carries two consumer-contract sections has swallowed
        # the header of the ticket that follows it (see RE-197, commit 32f5634e)
        n_contracts = len([l for l in t["body"].split("\n")
                           if l.startswith("###") and CONSUMER_MARK in l])
        if n_contracts > 1:
            orphan.append((t, n_contracts))

        if t["num"] < min_num:
            continue
        if closed or letter:
            continue
        eligible.append((t, route, status))
        if route and not status:
            invisible.append((t, route))
        elif status and not route:
            no_route.append((t, status))

    return tickets, invisible, no_route, orphan, eligible


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default="CLIENT_RE_QUEUE.md")
    ap.add_argument("--notes", default="notes_to_chief")
    ap.add_argument("--min", type=int, default=85,
                    help="ignore tickets below this number (old tickets are archived)")
    ap.add_argument("--list-open", dest="list_open", action="store_true",
                    help="print the tickets a worker should actually take, using the "
                         "robust rule: route tag present AND header not marked closed AND "
                         "no RESULT letter in notes_to_chief/.  The OPEN/PENDING half is "
                         "reported as a warning column, NOT used to exclude a ticket -- a "
                         "hand-typed tag that goes missing must not silence the queue.")
    ap.add_argument("--route", default="",
                    help="with --list-open: keep only tickets carrying this route tag, "
                         "e.g. --route STATIC-ON-BRIDGE for a worker that has the client "
                         "image and capture corpus but never boots the game.")
    ap.add_argument("--fix", action="store_true",
                    help="append '  [PENDING]' to every [A] header (status half only). "
                         "Run this on a CLOUD CLONE and commit it there: the three queue "
                         "files are chief-owned single-writer files, deliberately outside "
                         "the bridge push allowlist (see pf_git_sync.ps1) -- an edit made on "
                         "the bridge disk cannot travel out and blocks every pull in.")
    a = ap.parse_args()

    if not os.path.isfile(a.queue):
        sys.stderr.write("ERROR: queue not found: %s\n" % a.queue)
        return 2

    tickets, invisible, no_route, orphan, eligible = audit(a.queue, a.notes, a.min)

    # A FLOOR, BECAUSE "0 PROBLEMS" AND "0 QUEUE" LOOK IDENTICAL WITHOUT ONE.
    # pf-adversary (round dfx8bu) ran both modes against a zero-byte queue file
    # and got a clean bill of health twice: "RESULT: 0 ticket(s) the RE runner
    # cannot select", exit 0, and "none -- the queue really is empty", exit 0.
    # This tool is now the single authority PROCESS_GATES section 18 points
    # every lane at, and the round that wrote that rule was itself a 35-line
    # deletion from this very file; had the deletion taken ticket bodies with
    # it, the mandated closing command would have said everything was fine.
    # The floor is deliberately far below the real count (97 at the time of
    # writing): it is a smoke alarm for a truncated, half-written or
    # wrong-path file, not a pin on the queue's size, which must be free to
    # shrink as tickets are archived.
    if len(tickets) < MIN_PLAUSIBLE_TICKETS:
        sys.stderr.write(
            "ERROR: only %d ticket(s) parsed out of %s -- below the floor of %d.\n"
            "This queue has had ~97 tickets since 2026-08.  A count this low means\n"
            "the file was truncated, a bad --queue path was passed, or the ticket\n"
            "header format changed and TICKET_RE stopped matching.  Refusing to\n"
            "report a clean queue; check the file before trusting any output.\n"
            % (len(tickets), a.queue, MIN_PLAUSIBLE_TICKETS))
        return 3

    if a.list_open:
        if a.route:
            eligible = [e for e in eligible if (a.route in e[1]) or not e[1]]
        print("RE QUEUE -- TICKETS A WORKER SHOULD TAKE  (%s)" % a.queue)
        if a.route:
            print("filter: route == %s" % a.route)
        print("rule: header not marked closed AND no RESULT letter in notes_to_chief/.")
        print("      NEITHER hand-typed tag gates a ticket: a missing route tag or a missing")
        print("      OPEN/PENDING tag is reported in the warning column, never used to hide")
        print("      the ticket.  --route keeps that route plus every untagged ticket.")
        print("")
        if not eligible:
            print("    none -- the queue really is empty")
        for t, route, status in eligible:
            warns = []
            if not route:
                warns.append("no route tag - judge from the ticket body")
            if not status:
                warns.append("no OPEN/PENDING tag")
            tail = ("   <- " + "; ".join(warns)) if warns else ""
            print("    %-7s line %-6d %-22s%s"
                  % (t["id"], t["line"], ",".join(route) or "route=MISSING", tail))
        print("")
        if orphan:
            print("    NOTE: %d block(s) hold a second consumer contract, so a ticket below"
                  % len(orphan))
            print("    them lost its '## ' header and is NOT in the list above:")
            for t, n in orphan:
                print("      inside %s (line %d)" % (t["id"], t["line"]))
            print("")
        print("OPEN TICKETS: %d" % len(eligible))
        return 0

    print("RE QUEUE TAG LINT -- %s" % a.queue)
    print("tickets parsed: %d" % len(tickets))
    print("")

    print("[A] INVISIBLE TO RE RUNNER (route tag present, status tag missing, no result letter)")
    if not invisible:
        print("    none")
    for t, route in invisible:
        print("    %-7s line %-6d route=%s  status=MISSING" % (t["id"], t["line"], ",".join(route)))
        print("            fix: append ' [PENDING]' to the end of the header line")
    print("")

    print("[B] MISSING ROUTE TAG (status tag present, route tag missing) -- PROCESS_GATES section 18")
    if not no_route:
        print("    none")
    for t, status in no_route:
        print("    %-7s line %-6d status=%s  route=MISSING" % (t["id"], t["line"], ",".join(status)))
    print("")

    print("[C] ORPHAN BODY (one block holds two consumer contracts => a header line was lost)")
    if not orphan:
        print("    none")
    for t, n in orphan:
        print("    %-7s line %-6d contains %d consumer-contract sections" % (t["id"], t["line"], n))
        print("            a following ticket lost its '## ' header inside this block")
    print("")

    if a.fix and invisible:
        with open(a.queue, "r", encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        for t, _route in invisible:
            i = t["line"] - 1
            if lines[i] != t["header"]:
                sys.stderr.write("ERROR: line %d moved, aborting --fix\n" % t["line"])
                return 2
            lines[i] = lines[i].rstrip() + "  [PENDING]"
            print("FIXED  %-7s line %d  -> header now ends with [PENDING]" % (t["id"], t["line"]))
        with open(a.queue, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        print("")
        print("--fix touched the status half ONLY: no wording removed, moved or reworded,")
        print("and the route tag of every ticket is left exactly as it was.")
        print("[C] orphan bodies are NOT auto-fixed: a lost header must be recovered")
        print("verbatim from git history, by hand.")
        print("")
        print("REMINDER: commit this from a cloud clone.  The three queue files are")
        print("chief-owned single-writer files and are deliberately outside the bridge")
        print("push allowlist in pf_git_sync.ps1 -- an edit made on the bridge disk")
        print("cannot travel out and blocks every pull in.")
        return 1

    total = len(invisible) + len(no_route) + len(orphan)
    print("RESULT: %d ticket(s) the RE runner cannot select" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

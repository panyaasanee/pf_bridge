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
CLOSED_WORDS = ("DONE", "CLOSED", "ARCHIVED", "archived", "OPENED-IN-ERROR",
                "METHOD-FAIL", "SUPERSEDED")
TICKET_RE = re.compile(r"^##\s.*?\b(RE|GT)-(\d{3})\b")
STRIKE_RE = re.compile(r"~~.*?~~", re.S)
CONSUMER_MARK = "consumer-contract"  # matched loosely below


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
        closed = any(w in head_live for w in CLOSED_WORDS)
        letter = has_result_letter(t["id"], names)

        # a block that carries two consumer-contract sections has swallowed
        # the header of the ticket that follows it (see RE-197, commit 32f5634e)
        n_contracts = len([l for l in t["body"].split("\n")
                           if l.startswith("###") and "สัญญาผู้บริโภค" in l])
        if n_contracts > 1:
            orphan.append((t, n_contracts))

        if t["num"] < min_num:
            continue
        if closed or letter:
            continue
        if route:
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

    if a.list_open:
        if a.route:
            eligible = [e for e in eligible if a.route in e[1]]
        print("RE QUEUE -- TICKETS A WORKER SHOULD TAKE  (%s)" % a.queue)
        if a.route:
            print("filter: route == %s" % a.route)
        print("rule: route tag present AND header not marked closed AND no RESULT letter.")
        print("      the OPEN/PENDING tag is NOT part of the rule -- see the warning column.")
        print("")
        if not eligible:
            print("    none -- the queue really is empty")
        for t, route, status in eligible:
            warn = "" if status else "   <- WARNING: no OPEN/PENDING tag on the header"
            print("    %-7s line %-6d %s%s" % (t["id"], t["line"], ",".join(route), warn))
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

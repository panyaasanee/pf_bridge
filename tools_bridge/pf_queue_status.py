#!/usr/bin/env python3
# pf_queue_status.py - generate one canonical queue-status table from ticket HEADERS
# (not the hand-maintained index). Scans GAME_TEST_QUEUE.md + CLIENT_RE_QUEUE.md + archive/*QUEUE*ARCHIVE*.md
# Output: pf_bridge/QUEUE_STATUS_SNAPSHOT.md  (derived file - safe to regenerate anytime)
# Rules implemented:
#  - live file wins over archive; ticket present in BOTH with open-status in live but closed in archive => CONFLICT flag
#  - open tickets missing from the hand index => DRIFT list
#  - index lines whose ticket is closed => DRIFT list
# Run:  python3 tools_bridge/pf_queue_status.py   (from pf_bridge root; also works with Windows py -3)
import re, sys, glob, os, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = [os.path.join(ROOT, "GAME_TEST_QUEUE.md"), os.path.join(ROOT, "CLIENT_RE_QUEUE.md")]
ARCH = sorted(glob.glob(os.path.join(ROOT, "archive", "*QUEUE*ARCHIVE*.md")))

TID = re.compile(r"\b((?:GT|RE)-\d{3})\b")
HDR = re.compile(r"^#{2,6}\s+[^A-Za-z0-9]{0,24}((?:GT|RE)-\d{3})\b")
STRIKE = re.compile(r"~~.*?~~", re.S)

# LANE-A letter 20260906_1041 item 1, measured on main, not read off the code:
# STATUS.search() used to sweep the WHOLE header line, and a ticket header is
# "## <emoji> GT-nnn <SLUG-001>: <title> [<status>]".  Every house slug is
# SHOUTED-WITH-HYPHENS and ends in -001/-002, so a slug carrying an English
# status word was read as the ticket's status: GT-224
# (MOB-AI-TICK-GATE-IS-OPEN-...-001) and GT-242 (BACKPACK-OPEN-...-001) both
# reported OPEN while their headers said READY.  The expensive half is the
# CLOSED set: a future slug containing PASS/DONE/CLOSED/ANSWERED would move an
# OPEN ticket into the CLOSED table and drop it out of the OPEN one silently -
# it would never board the attended bus and nobody would be told.  LANE-A ran
# the control both ways (BACKPACK-OPEN- -> BACKPACK-OPENING- flipped the row
# to READY; EVIL-PORT-FIRST-EYES-001 -> FIRST-PASS-EYES-001 moved an open
# ticket to PASS and took "open in live" from 107 to 106 with no warning).
# The fix is deliberately narrow: blank out ONLY the slug that immediately
# follows the ticket id.  A real status token (BLOCKED-ON-WIRING, PASS/DONE)
# never ends in -<3 digits>, so no status can be eaten by this.
SLUG_AFTER_ID = re.compile(r"((?:GT|RE)-\d{3}\W{0,4})([A-Z0-9][A-Z0-9-]*-\d{3})\b")
# A ticket body that still carries a wiring placeholder cannot be booted, no
# matter what its header says (LANE-A 20260906_1041 item 4: GT-079/GT-080 are
# READY in their headers while the server command line in the body is still
# <CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>).  Booting one burns an owner session.
PLACEHOLDER = re.compile(r"<[A-Z][A-Z0-9_]{5,}>")
# LANE-A 20260906_1041 item 3: three different arbiters were answering "which
# tickets can board the attended bus" with three different numbers, and the 19
# in R364 came from an ad-hoc regex that was never committed.  Count it here,
# in the file everyone already runs, so the argument is over one number.
ATTENDED = re.compile(r"^\s*(?:[*_`>\-]{0,4}\s*)ATTENDED:", re.M)


def _strip_slug(line):
    """Header/index line with the ticket's own slug blanked out.

    Only the slug directly after a ticket id is removed, and it is replaced by
    spaces rather than deleted so that every column offset in the line (and so
    every message that quotes it) stays where it was.
    """
    return SLUG_AFTER_ID.sub(lambda m: m.group(1) + " " * len(m.group(2)), line)
STATUS = re.compile(r"\b(PASS/DONE|BOUNDED-NEGATIVE|AWAITING-OBSERVER|AWAITING-DECISION|READY-CONDITIONAL|BLOCKED-ON-WIRING|BLOCKED-ON-TOOL|BLOCKED-CONDITIONAL|BLOCKED-BY|NO-RESULT|ANSWERED|FALSIFIED|CANCELLED|CLOSED|PENDING|BLOCKED|PARTIAL|READY|OPEN|HOLD|DONE|PASS|FAIL)\b")
CLOSED = {"PASS","PASS/DONE","CLOSED","DONE","ANSWERED","FALSIFIED","BOUNDED-NEGATIVE","ARCHIVED-STUB","CANCELLED","FAIL"}
# One status marker pattern, used for the header and for the body scan alike
# (see the block inside scan() for why the header stopped using a bare search).
MARKED_STATUS = re.compile(
    r"(?:\*\*|\[|[\U0001F7E2\U0001F7E1\U0001F534\u26D4\u2705])\s*\(?\*{0,2}"
    + STATUS.pattern)
# The same set of markers, matched as the TAIL of the text standing in front of
# a status word, so it can be asked about one particular match rather than
# about the line as a whole.
MARKER_TAIL = re.compile(
    r"(?:\*\*|\[|\(|[\U0001F7E0-\U0001F7EB\U0001F534\U0001F535\U0001F527"
    r"\u26D4\u2705\u2014\u00B7])\s*\(?\*{0,2}$")

def scan(path):
    out = {}
    flags = {}
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    except OSError:
        return out, flags
    hdr_idx = [i for i, l in enumerate(lines) if HDR.match(l)]
    for n, i in enumerate(hdr_idx):
        tid = HDR.match(lines[i]).group(1)
        stop = hdr_idx[n+1] if n+1 < len(hdr_idx) else min(i+40, len(lines))
        body = "\n".join(lines[i:stop])
        if tid not in flags:
            flags[tid] = (bool(PLACEHOLDER.search(body)),
                          bool(ATTENDED.search(body)))
        hl = _strip_slug(STRIKE.sub(" ", lines[i]))
        # archive stub: "-- archived ... (closed; verbatim in archive/...)"
        if "archived" in hl and "closed" in hl:
            if tid not in out:
                out[tid] = ("ARCHIVED-STUB", i+1, "stub", lines[i][:120])
            continue
        status, src = None, "?"
        # Blanking the slug alone is not enough, and measuring said so: with
        # only that fix GT-224 stopped reporting OPEN and started reporting
        # PASS, because its header carries the folded result "wire = PASS"
        # inside a sentence that also says the client half is NOT complete and
        # that the final call is still the chief's.  PASS is in CLOSED, so the
        # ticket would have left the OPEN table entirely - the exact silent
        # disappearance LANE-A's letter was about, on M4's own ticket.  So the
        # header is now read with the SAME marker-anchored pattern the body
        # scan below has always used: a status counts only where it stands
        # right after a status marker (an emoji, a bold run, a bracket), which
        # is how every house header actually writes its verdict.  A status word
        # sitting mid-sentence ("wire = PASS", "GT-121 \u0E1C\u0E48\u0E32\u0E19 (PASS)") no longer
        # counts anywhere.  When the header therefore says nothing, the body
        # scan runs exactly as before, and a ticket with no marker anywhere is
        # UNKNOWN - which keeps it in the OPEN table.  That asymmetry is on
        # purpose: a ticket wrongly listed open costs one read, a ticket
        # wrongly listed closed costs one burnt attended session.
        for m in STATUS.finditer(hl):
            if m.group(1) not in CLOSED or MARKER_TAIL.search(hl[:m.start()]):
                status, src = m.group(1), "header"
                break
        if status is None:
            for j in range(i+1, min(stop, i+16)):
                clean = _strip_slug(STRIKE.sub(" ", lines[j]))
                m2 = MARKED_STATUS.search(clean)
                if m2:
                    status, src = m2.group(1), "body+%d" % (j-i)
                    break
        if tid not in out:
            out[tid] = (status or "UNKNOWN", i+1, src, lines[i][:120])
    return out, flags

live, arch, live_flags = {}, {}, {}
for p in LIVE:
    scanned, scanned_flags = scan(p)
    for t, v in scanned.items():
        live.setdefault(t, v + (os.path.basename(p),))
    for t, v in scanned_flags.items():
        live_flags.setdefault(t, v)
for p in ARCH:
    scanned, _ = scan(p)
    for t, v in scanned.items():
        arch.setdefault(t, v + (os.path.basename(p),))

# hand index section of GAME_TEST_QUEUE.md
idx_ids = set()
try:
    txt = open(LIVE[0], encoding="utf-8", errors="replace").read()
    m = re.search(r"สารบัญใบที่ยังไม่ปิด(.*?)(?:\n\*\*🎮|\n## )", txt, re.S)
    if m:
        idx_ids = set(TID.findall(m.group(1)))
except OSError:
    pass

# index-line statuses (the hand index can be NEWER than the body -- e.g. GT-080 unblock lived only there)
idx_status = {}
try:
    m2 = re.search(r"สารบัญใบที่ยังไม่ปิด(.*?)(?:\n\*\*🎮|\n## )", txt, re.S)
    if m2:
        for line in m2.group(1).split("\n"):
            found = list(TID.finditer(line))
            if not found:
                continue
            # LANE-A 20260906_1041 item 2: this used to pair the line's FIRST
            # id with the line's FIRST status word wherever it sat, so an index
            # line that talks about a SECOND ticket in passing lent that
            # ticket's status to the first one.  Measured: GT-080's index line
            # ends "... GT-121 ผ่าน (PASS)", which produced a standing
            # "GT-080: index=PASS vs body=READY" conflict that no one could
            # resolve because it was never true - and FROM_CHIEF_R350 quoted
            # that row to forbid GT-080 in unattended rounds.  Two narrowings:
            # only the segment before the next ticket id belongs to this id,
            # and the slug is blanked first (the index repeats it verbatim).
            seg = line[:found[1].start()] if len(found) > 1 else line
            clean = _strip_slug(STRIKE.sub(" ", seg))
            sm = STATUS.search(clean)
            if sm:
                idx_status.setdefault(found[0].group(1), sm.group(1))
except Exception:
    pass

rows, conflicts = [], []
allids = sorted(set(live) | set(arch))
for t in allids:
    if t in live:
        st, ln, src, ttl, fn = live[t]
        where = "live:%s:%s" % (fn, ln)
        if st == "ARCHIVED-STUB" and t in arch:
            st = arch[t][0] if arch[t][0] in CLOSED else "ARCHIVED-STUB"
            where = "archive:%s:%s" % (arch[t][4], arch[t][1])
        if t in arch and arch[t][0] in CLOSED and st not in CLOSED:
            conflicts.append("%s: live=%s but archived-closed=%s (%s) -- likely stale live entry or duplicate reopen" % (t, st, arch[t][0], arch[t][4]))
    else:
        st, ln, src, ttl, fn = arch[t]
        where = "archive:%s:%s" % (fn, ln)
    rows.append((t, st, where, src, ttl.replace("|", "/")))

open_rows = [r for r in rows if r[1] not in CLOSED and r[2].startswith("live")]
placeholder_rows = [r[0] for r in open_rows if live_flags.get(r[0], (False, False))[0]]
no_attended = [r[0] for r in open_rows if not live_flags.get(r[0], (False, False))[1]]
missing_idx = [r[0] for r in open_rows if r[0] not in idx_ids]
closed_in_idx = sorted(i for i in idx_ids if i in dict((r[0], r[1]) for r in rows) and dict((r[0], r[1]) for r in rows)[i] in CLOSED)

try:
    now = subprocess.check_output(["date", "+%Y-%m-%dT%H:%M:%S+07:00"], env={**os.environ, "TZ": "Asia/Bangkok"}).decode().strip()
except Exception:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ(utc)")

out = []
# COO-DECISION 20260903_0848 item 2: this snapshot may not be used to DECIDE
# anything -- not by a lane, not by the attended tester.  Measured that round:
# it disagreed with its own source in two ways at once (line pointer 9670 vs
# the real 9719, and status READY throughout a window where the ticket header
# said HOLD).  A summary file that can quietly contradict its source is worse
# than no summary file at all: booting an attended round from it means booting
# a ticket whose own header forbids it, which is one burnt owner session --
# the price already paid once on GT-193 in R303.  The banner is emitted by the
# generator, not typed into the output, so regeneration cannot drop it.
out.append("DERIVED FILE - DO NOT DECIDE FROM THIS - read GAME_TEST_QUEUE.md")
out.append("# QUEUE STATUS SNAPSHOT (generated -- do not edit; regenerate with tools_bridge/pf_queue_status.py)")
out.append("generated: %s" % now)
out.append("scanned: %s + %d archive files" % (", ".join(os.path.basename(p) for p in LIVE), len(ARCH)))
out.append("tickets total: %d (live %d / archive-only %d) -- open in live: %d" % (len(allids), len(live), len(allids)-len(live), len(open_rows)))
out.append("")
out.append("## OPEN (live)")
out.append("| ใบ | status | ที่อยู่ | อ่านจาก |")
out.append("|---|---|---|---|")
for r in sorted(open_rows, key=lambda x: x[0]):
    out.append("| %s | %s | %s | %s |" % (r[0], r[1], r[2], r[3]))
out.append("")
out.append("## DRIFT -- open แต่ไม่มีในสารบัญมือ (%d)" % len(missing_idx))
out.append(", ".join(missing_idx) if missing_idx else "(none)")
out.append("")
out.append("## DRIFT -- อยู่ในสารบัญมือแต่สถานะจริงปิดแล้ว (%d)" % len(closed_in_idx))
out.append(", ".join(closed_in_idx) if closed_in_idx else "(none)")
out.append("")
out.append("## CONFLICT -- live เปิดแต่ archive ปิด (%d)" % len(conflicts))
out.extend(conflicts if conflicts else ["(none)"])
mismatch = []
stat_by_id = dict((r[0], r[1]) for r in rows)
for t, ist in sorted(idx_status.items()):
    bst = stat_by_id.get(t)
    if bst and bst != "UNKNOWN" and ist != bst and not (ist in CLOSED and bst in CLOSED):
        mismatch.append("%s: index=%s vs body=%s -- อ่านทั้งสองที่ก่อนใช้ (ฝั่งไหนใหม่กว่าดูป้ายรอบ/เวลาในบรรทัด)" % (t, ist, bst))
out.append("")
out.append("## DRIFT -- สารบัญกับหัวใบบอกสถานะไม่ตรงกัน (%d)" % len(mismatch))
out.extend(mismatch if mismatch else ["(none)"])
out.append("")
out.append("## BLOCKED-BY-PLACEHOLDER -- open แต่เนื้อใบยังมี <PLACEHOLDER> (%d)" % len(placeholder_rows))
out.append("ห้ามบูต ไม่ว่าหัวใบจะเขียน READY หรือไม่ -- เผานัด attended (LANE-A `1041` ข้อ 4)")
out.append(", ".join(placeholder_rows) if placeholder_rows else "(none)")
out.append("")
out.append("## ATTENDED -- open ที่ยังไม่มีบล็อก `ATTENDED:` (%d จาก open %d)"
           % (len(no_attended), len(open_rows)))
out.append("ไม่มีบล็อก = ตกรถบัส capture (R364 ข้อ 2) -- ตัวนับนี้ commit แล้ว ใช้เลขเดียวกันได้ทุกสาย")
out.append(", ".join(no_attended) if no_attended else "(none)")
out.append("")
out.append("## CLOSED / archive")
out.append("| ใบ | status | ที่อยู่ |")
out.append("|---|---|---|")
for r in sorted(rows, key=lambda x: x[0]):
    if r not in open_rows:
        out.append("| %s | %s | %s |" % (r[0], r[1], r[2]))
open(os.path.join(ROOT, "QUEUE_STATUS_SNAPSHOT.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote QUEUE_STATUS_SNAPSHOT.md: %d tickets, %d open, drift-missing=%d, drift-closed-in-index=%d, conflicts=%d" % (len(allids), len(open_rows), len(missing_idx), len(closed_in_idx), len(conflicts)))

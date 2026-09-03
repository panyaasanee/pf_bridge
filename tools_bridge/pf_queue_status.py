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
STATUS = re.compile(r"\b(PASS/DONE|BOUNDED-NEGATIVE|AWAITING-OBSERVER|AWAITING-DECISION|READY-CONDITIONAL|BLOCKED-ON-WIRING|BLOCKED-ON-TOOL|BLOCKED-CONDITIONAL|BLOCKED-BY|NO-RESULT|ANSWERED|FALSIFIED|CLOSED|PENDING|BLOCKED|PARTIAL|READY|OPEN|HOLD|DONE|PASS)\b")
CLOSED = {"PASS","PASS/DONE","CLOSED","DONE","ANSWERED","FALSIFIED","BOUNDED-NEGATIVE","ARCHIVED-STUB"}

def scan(path):
    out = {}
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    except OSError:
        return out
    hdr_idx = [i for i, l in enumerate(lines) if HDR.match(l)]
    for n, i in enumerate(hdr_idx):
        tid = HDR.match(lines[i]).group(1)
        stop = hdr_idx[n+1] if n+1 < len(hdr_idx) else min(i+40, len(lines))
        hl = STRIKE.sub(" ", lines[i])
        # archive stub: "-- archived ... (closed; verbatim in archive/...)"
        if "archived" in hl and "closed" in hl:
            if tid not in out:
                out[tid] = ("ARCHIVED-STUB", i+1, "stub", lines[i][:120])
            continue
        status, src = None, "?"
        m = STATUS.search(hl)
        if m:
            status, src = m.group(1), "header"
        else:
            for j in range(i+1, min(stop, i+16)):
                clean = STRIKE.sub(" ", lines[j])
                m2 = re.search(r"(?:\*\*|\[|[\U0001F7E2\U0001F7E1\U0001F534\u26D4\u2705])\s*\(?\*{0,2}" + STATUS.pattern, clean)
                if m2:
                    status, src = m2.group(1), "body+%d" % (j-i)
                    break
        if tid not in out:
            out[tid] = (status or "UNKNOWN", i+1, src, lines[i][:120])
    return out

live, arch = {}, {}
for p in LIVE:
    for t, v in scan(p).items():
        live.setdefault(t, v + (os.path.basename(p),))
for p in ARCH:
    for t, v in scan(p).items():
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
            ids = TID.findall(line)
            if not ids:
                continue
            clean = STRIKE.sub(" ", line)
            sm = STATUS.search(clean)
            if sm:
                idx_status.setdefault(ids[0], sm.group(1))
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
out.append("## CLOSED / archive")
out.append("| ใบ | status | ที่อยู่ |")
out.append("|---|---|---|")
for r in sorted(rows, key=lambda x: x[0]):
    if r not in open_rows:
        out.append("| %s | %s | %s |" % (r[0], r[1], r[2]))
open(os.path.join(ROOT, "QUEUE_STATUS_SNAPSHOT.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote QUEUE_STATUS_SNAPSHOT.md: %d tickets, %d open, drift-missing=%d, drift-closed-in-index=%d, conflicts=%d" % (len(allids), len(open_rows), len(missing_idx), len(closed_in_idx), len(conflicts)))

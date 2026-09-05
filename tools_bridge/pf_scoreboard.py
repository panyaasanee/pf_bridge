#!/usr/bin/env python3
"""pf_scoreboard.py - collect SCOREBOARD: lines -> SCOREBOARD_FACTS.tsv -> PLAYER_STATUS.html

PANYA-ORDER 20260905_2038 item (b): the scoreboard died on Aug 29 because it
was a hand-kept file nobody regenerated.  It is now DERIVED: every round file
under pf_bridge/rounds/ ends with one line

    SCOREBOARD: <DONE|COMING|STUCK|NONE> | <sentence a player understands> | <evidence>

(format fixed in prompts/COMMON_LANE_ROUND.md).  This tool reads those lines,
merges them with any hand-written rows already in SCOREBOARD_FACTS.tsv, writes
the TSV, and renders PLAYER_STATUS.html.  Chief runs it every round.

Console output is ASCII only: the bridge console is cp874 and a tool that dies
printing a Thai sentence is a tool that stops the round (HOUSE RULE, CHIEF 15).
The row text itself is Thai and only ever reaches the TSV/HTML files, which are
written as UTF-8.

    python3 tools_bridge/pf_scoreboard.py            # regenerate both files
    python3 tools_bridge/pf_scoreboard.py --check    # report only, write nothing
    python3 tools_bridge/pf_scoreboard.py --self-test
"""
import argparse
import datetime
import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, "SCOREBOARD_FACTS.tsv")
HTML_OUT = os.path.join(ROOT, "PLAYER_STATUS.html")
ROUNDS = os.path.join(ROOT, "rounds")

# NONE is a legal status a lane must be able to write ("nothing moved this
# round").  It is carried into the TSV so the record is complete, and is not
# rendered, because the page answers "what can a player do" and NONE is not an
# answer.  RENDERED is the set the page has sections for.
STATUSES = ("DONE", "COMING", "STUCK", "NONE")
RENDERED = ("DONE", "COMING", "STUCK")
MANUAL = "manual"

SCOREBOARD_RE = re.compile(r"^SCOREBOARD:\s*(.*)$")
# A_20260905_2104_wjprxa_topic.md / R359_5ahimz_topic.md / DB_..._claim.md
LANE_RE = re.compile(r"^(R\d+|[A-Z]{1,3})_")
STAMP_RE = re.compile(r"(\d{8})_(\d{4})")
ROUNDID_RE = re.compile(r"^(?:R\d+|[A-Z]{1,3})_(?:\d{8}_\d{4}_)?([A-Za-z0-9-]+)")

LANE_NAMES = {"A": "LANE-A", "B": "LANE-B", "DB": "LANE-DB", "GM": "LANE-GM",
              "CS": "LANE-CS", "UI": "LANE-UI", "Q": "LANE-Q", "E": "LANE-E"}


def who_from_filename(name):
    """'A_20260905_2104_wjprxa_x.md' -> 'LANE-A round wjprxa' (ASCII, no Thai).

    The 'who' column is what tells the owner which lane earned the row, so it
    is derived from the filename rather than trusted from the line body - a
    lane cannot credit its row to another lane by typing a different name.
    """
    stem = name[:-3] if name.endswith(".md") else name
    m = LANE_RE.match(stem)
    if not m:
        return stem
    head = m.group(1)
    lane = "LANE-E" if head.startswith("R") else LANE_NAMES.get(head, head)
    rid = ROUNDID_RE.match(stem)
    round_id = rid.group(1) if rid else ""
    if head.startswith("R"):
        # chief files carry the round NUMBER in the head, the code after it
        return "%s %s (%s)" % (lane, head, round_id) if round_id else "%s %s" % (lane, head)
    return "%s round %s" % (lane, round_id) if round_id else lane


def commit_times(paths):
    """{filename: ISO commit time} for ordering rows newest-round-first.

    Filenames are not orderable across lanes (chief files carry R<N>, lane
    files carry a timestamp), and mtime on a cloud clone is checkout time for
    every file alike.  The commit time is the only stamp that says when the
    round actually happened.  Missing git, or a file not yet committed, falls
    back to the timestamp in the filename, then to the empty string - never to
    an exception, because ordering must not be able to stop the round.
    """
    out = {}
    try:
        raw = subprocess.check_output(
            ["git", "-C", ROOT, "log", "--format=%x00%cI", "--name-only",
             "--", "rounds/"],
            stderr=subprocess.DEVNULL).decode("utf-8", "replace")
        stamp = ""
        for line in raw.splitlines():
            if line.startswith("\x00"):
                stamp = line[1:]
            elif line.strip():
                base = os.path.basename(line.strip())
                out.setdefault(base, stamp)
    except Exception:
        pass
    for p in paths:
        if out.get(p):
            continue
        m = STAMP_RE.search(p)
        out[p] = "%s-%s-%sT%s:%s" % (m.group(1)[:4], m.group(1)[4:6],
                                     m.group(1)[6:], m.group(2)[:2],
                                     m.group(2)[2:]) if m else ""
    return out


def collect(rounds_dir=ROUNDS):
    """-> (rows, malformed, files_seen).

    rows: [status, who, sentence, evidence, source_filename]
    malformed: [(filename, lineno, reason, raw)] - never dropped silently.
    """
    rows, malformed, files_seen = [], [], 0
    if not os.path.isdir(rounds_dir):
        return rows, malformed, files_seen
    for name in sorted(os.listdir(rounds_dir)):
        if not name.endswith(".md"):
            continue
        files_seen += 1
        path = os.path.join(rounds_dir, name)
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError as exc:
            malformed.append((name, 0, "unreadable: %s" % exc.__class__.__name__, ""))
            continue
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            m = SCOREBOARD_RE.match(lines[i].strip())
            if not m:
                i += 1
                continue
            lineno = i + 1
            # The rule says "one line", but every round file so far is written
            # in a hard-wrapping editor: measured 2026-09-05, six of the seven
            # SCOREBOARD lines in rounds/ carry their evidence field on a
            # CONTINUATION line.  Reading only the first physical line would
            # have reported six lanes as having filed no evidence, which is
            # false.  A wrapped paragraph ends at a blank line, at a heading,
            # or at the next SCOREBOARD line - nothing else.
            body = m.group(1)
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt or nxt.startswith("#") or SCOREBOARD_RE.match(nxt):
                    break
                body += " " + nxt
                i += 1
            parts = [p.strip() for p in body.split("|")]
            if not parts or not parts[0]:
                malformed.append((name, lineno, "no status", body[:80]))
                continue
            status = parts[0].split()[0].upper()
            if status not in STATUSES:
                malformed.append((name, lineno, "status not in %s" % (STATUSES,), body[:80]))
                continue
            if len(parts) < 3:
                # After the wrapped paragraph is joined, a missing third field
                # is the lane really leaving the evidence off.  Keep the row -
                # the sentence is still the lane's claim - but say out loud
                # that the evidence half is missing, because an unevidenced
                # DONE is exactly the row the owner must not read as measured.
                malformed.append((name, lineno,
                                  "only %d field(s), expected 3 (status|sentence|evidence)"
                                  % len(parts), body[:80]))
            sentence = parts[1] if len(parts) > 1 else ""
            evidence = " | ".join(parts[2:]) if len(parts) > 2 else "(no evidence field on the line)"
            rows.append([status, who_from_filename(name),
                         sentence.replace("\t", " "), evidence.replace("\t", " "), name])
    order = commit_times([r[4] for r in rows])
    rows.sort(key=lambda r: (order.get(r[4], ""), r[4]), reverse=True)
    return rows, malformed, files_seen


def read_manual(tsv=TSV):
    """Hand-written rows survive regeneration; derived rows do not.

    A row is manual when its source column is exactly 'manual'.  Everything
    else in the file came from a round file and is rebuilt from that round
    file, so a stale derived row cannot outlive the round that wrote it.
    """
    keep = []
    if not os.path.exists(tsv):
        return keep
    for line in open(tsv, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) >= 5 and p[4] == MANUAL and p[0] in STATUSES:
            keep.append(p[:5])
    return keep


def now_stamp():
    try:
        return subprocess.check_output(
            ["date", "+%Y-%m-%d %H:%M +07:00"],
            env=dict(os.environ, TZ="Asia/Bangkok")).decode().strip()
    except Exception:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def write_tsv(rows, malformed, path=TSV):
    lines = [
        "# SCOREBOARD_FACTS.tsv - GENERATED by tools_bridge/pf_scoreboard.py, do not hand-edit",
        "#   derived rows are rebuilt from the SCOREBOARD: line of each pf_bridge/rounds/*.md",
        "#   a row with source column 'manual' is kept across regenerations",
        "# columns: status<TAB>who<TAB>what a player can do<TAB>evidence<TAB>source",
    ]
    for name, lineno, reason, raw in malformed:
        lines.append("# MALFORMED\t%s:%s\t%s\t%s" % (name, lineno, reason, raw))
    for r in rows:
        lines.append("\t".join(r))
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


SEC = [("DONE", "ทำได้จริงแล้ว - บนบูตปกติไร้แฟล็ก", "#1E7A46"),
       ("COMING", "กำลังมา - โค้ดถึง main / รอ merge / รอเทสตา", "#9A6E0E"),
       ("STUCK", "พิสูจน์แล้วแต่ยังไม่ถึงมือผู้เล่น (หนี้ท่อ promotion)", "#B3403A")]


def render(rows, malformed, none_count, path=HTML_OUT):
    buckets = {k: [r for r in rows if r[0] == k] for k in RENDERED}
    now = now_stamp()
    h = ["<!doctype html><html><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         "<title>Pirate Force - Player Status</title><style>",
         "body{margin:0;background:#F4F5F2;color:#1C2733;font-family:'Segoe UI','Leelawadee UI',Tahoma,sans-serif;line-height:1.6}",
         ".w{max-width:900px;margin:0 auto;padding:32px 20px}",
         "h1{font-size:26px;border-bottom:3px solid #A87514;padding-bottom:10px}",
         ".stamp{color:#5B6B7A;font-size:13px;margin-bottom:24px}",
         "h2{font-size:16px;margin:26px 0 8px}",
         "table{width:100%;border-collapse:collapse;background:#fff;font-size:14.5px}",
         "td{border:1px solid #DCE1E0;padding:8px 12px;vertical-align:top}",
         "td.ev{font-family:Consolas,monospace;font-size:12px;color:#5B6B7A;width:26%}",
         "td.what{font-weight:600;width:20%;white-space:nowrap}",
         ".warn{background:#FFF4E5;border-left:4px solid #B3403A;padding:10px 14px;font-size:13px;margin:18px 0}",
         "@media(prefers-color-scheme:dark){body{background:#10171E;color:#E8ECEF}table{background:#19222B}td{border-color:#2A3541}td.ev{color:#93A2AF}.warn{background:#241B12}}",
         "</style></head><body><div class='w'>",
         "<h1>Pirate Force - วันนี้ผู้เล่นทำอะไรได้จริงบ้าง</h1>",
         "<div class='stamp'>generate อัตโนมัติจากบรรทัด <code>SCOREBOARD:</code> ท้ายไฟล์ <code>rounds/*.md</code> - "
         + html.escape(now) + " - " + str(len(rows)) + " rows, " + str(none_count) + " NONE</div>"]
    if malformed:
        h.append("<div class='warn'><b>%d SCOREBOARD line(s) are malformed</b> - "
                 "แถวข้างล่างอาจขาดหลักฐาน:<br>" % len(malformed)
                 + "<br>".join(html.escape("%s:%s - %s" % (m[0], m[1], m[2])) for m in malformed)
                 + "</div>")
    for key, title, color in SEC:
        h.append("<h2 style='color:%s'>%s (%d)</h2><table>"
                 % (color, html.escape(title), len(buckets[key])))
        if not buckets[key]:
            h.append("<tr><td colspan='3'>-</td></tr>")
        for r in buckets[key]:
            h.append("<tr><td class='what'>%s</td><td>%s</td><td class='ev'>%s</td></tr>"
                     % (html.escape(r[1]), html.escape(r[2]), html.escape(r[3])))
        h.append("</table>")
    h.append("<div class='stamp' style='margin-top:24px'>กติกา: ทุกไฟล์รอบจบด้วยบรรทัด <code>SCOREBOARD:</code> "
             "(COMMON_LANE_ROUND) - ไม่มีบรรทัดนี้ = รอบนั้นไม่นับ</div></div></body></html>")
    open(path, "w", encoding="utf-8").write("\n".join(h))


def _self_test():
    """Prove the collector on synthetic round files. No pytest in pf_bridge."""
    import tempfile
    cases, failures, ran = [], 0, 0
    with tempfile.TemporaryDirectory() as tmp:
        rd = os.path.join(tmp, "rounds")
        os.makedirs(rd)

        def put(name, body):
            open(os.path.join(rd, name), "w", encoding="utf-8").write(body)

        put("A_20260905_2104_wjprxa_topic.md",
            "blah\nSCOREBOARD: COMING | player sentence | PR #852\n")
        put("R359_5ahimz_topic.md",
            "SCOREBOARD: STUCK | chief sentence | sha abc\n")
        put("B_20260905_2105_e3g1io_topic.md",
            "SCOREBOARD: NONE | nothing moved | -\n")
        put("CS_20260905_2113_danva2_topic.md",
            "SCOREBOARD: COMING | evidence field missing\n")   # malformed
        put("GM_20260905_2100_zzzzzz_topic.md",
            "SCOREBOARD: BANANA | bogus status | x\n")          # rejected
        put("UI_20260905_2101_yyyyyy_topic.md",
            "  SCOREBOARD: DONE | indented still counts | GT-1\n")
        # the shape actually found in rounds/ on 2026-09-05: the line is
        # hard-wrapped and the evidence field sits on a continuation line
        put("DB_20260905_2104_6o6qnr_topic.md",
            "prose above\n\nSCOREBOARD: COMING | wrapped sentence\n"
            "second half of it | PR:\nserver#999\n\nnext paragraph\n")
        put("notes.txt", "SCOREBOARD: DONE | not a round file | x\n")  # ignored
        rows, malformed, seen = collect(rd)

        by_src = {r[4]: r for r in rows}
        cases = [
            ("seven .md files seen, notes.txt ignored", seen, 7),
            ("six rows kept (BANANA rejected)", len(rows), 6),
            ("two malformed reported (missing evidence + bogus status)",
             len(malformed), 2),
            ("a wrapped line keeps its sentence whole",
             by_src["DB_20260905_2104_6o6qnr_topic.md"][2],
             "wrapped sentence second half of it"),
            ("a wrapped line finds its evidence on the continuation line",
             by_src["DB_20260905_2104_6o6qnr_topic.md"][3], "PR: server#999"),
            ("the paragraph stops at the blank line, not at the next one",
             "next paragraph" in by_src["DB_20260905_2104_6o6qnr_topic.md"][3], False),
            ("NONE row is kept in the record",
             by_src["B_20260905_2105_e3g1io_topic.md"][0], "NONE"),
            ("lane derived from filename, not from the line",
             by_src["A_20260905_2104_wjprxa_topic.md"][1], "LANE-A round wjprxa"),
            ("chief file maps to LANE-E with its round number",
             by_src["R359_5ahimz_topic.md"][1], "LANE-E R359 (5ahimz)"),
            ("missing evidence field is filled with a visible marker",
             by_src["CS_20260905_2113_danva2_topic.md"][3],
             "(no evidence field on the line)"),
            ("indented SCOREBOARD line is still collected",
             by_src["UI_20260905_2101_yyyyyy_topic.md"][0], "DONE"),
            ("bogus status is not smuggled in as a row",
             "GM_20260905_2100_zzzzzz_topic.md" in by_src, False),
        ]
        # a malformed line must name its file and line number, or it is noise
        cases.append(("malformed entry carries file+lineno",
                      malformed[0][0].endswith(".md") and malformed[0][1] > 0, True))

        # manual rows survive, derived rows do not
        t = os.path.join(tmp, "facts.tsv")
        open(t, "w", encoding="utf-8").write(
            "# header\n"
            "DONE\thand\tkept row\tGT-9\tmanual\n"
            "DONE\tstale\tdropped row\tGT-8\tR001_old_topic.md\n")
        kept = read_manual(t)
        cases.append(("only the manual row survives regeneration", len(kept), 1))
        cases.append(("and it is the right one", kept[0][2], "kept row"))

        # writing then re-reading keeps the manual row and no derived rows
        write_tsv(kept + rows, malformed, t)
        cases.append(("round-trip: manual row still manual", len(read_manual(t)), 1))

        # render must not crash and must not print NONE rows
        out = os.path.join(tmp, "p.html")
        render(kept + rows, malformed, 1, out)
        page = open(out, encoding="utf-8").read()
        cases.append(("NONE row is not rendered", "nothing moved" in page, False))
        cases.append(("DONE row is rendered", "indented still counts" in page, True))
        cases.append(("malformed count is shown on the page",
                      "malformed" in page, True))

    for label, got, want in cases:
        ran += 1
        if got != want:
            failures += 1
            print("SELF-TEST FAIL: %s -> got %r, want %r" % (label, got, want))
    if failures:
        print("SELF-TEST RED: %d of %d cases failed." % (failures, ran))
        return 1
    if ran != 19:
        print("SELF-TEST RED: expected 19 cases, ran %d." % ran)
        return 1
    print("SELF-TEST PASS: %d cases." % ran)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="report what would be written, write nothing")
    ap.add_argument("--self-test", action="store_true", dest="self_test",
                    help="run the built-in cases and exit")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()

    rows, malformed, files_seen = collect()
    manual = read_manual()
    none_count = sum(1 for r in rows if r[0] == "NONE")
    allrows = manual + rows

    # A collector that finds nothing must not print success.  This is the way
    # the old scoreboard died: it kept rendering a page that no longer had any
    # relationship to the rounds being run.
    if files_seen and not rows:
        print("SCOREBOARD RED: %d round file(s) but 0 SCOREBOARD: lines parsed."
              % files_seen)
        return 1

    print("scoreboard: %d round files, %d rows (%d DONE, %d COMING, %d STUCK, "
          "%d NONE), %d manual, %d malformed"
          % (files_seen, len(rows),
             sum(1 for r in rows if r[0] == "DONE"),
             sum(1 for r in rows if r[0] == "COMING"),
             sum(1 for r in rows if r[0] == "STUCK"),
             none_count, len(manual), len(malformed)))
    for name, lineno, reason, _raw in malformed:
        print("  MALFORMED %s:%s - %s" % (name, lineno, reason))
    if a.check:
        print("(--check: nothing written)")
        return 0
    write_tsv(allrows, malformed)
    render(allrows, malformed, none_count)
    print("wrote %s and %s" % (os.path.basename(TSV), os.path.basename(HTML_OUT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

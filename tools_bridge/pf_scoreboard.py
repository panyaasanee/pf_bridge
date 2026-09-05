#!/usr/bin/env python3
# pf_scoreboard.py - render pf_bridge/SCOREBOARD_FACTS.tsv -> pf_bridge/PLAYER_STATUS.html
# Auto-refresh: run this any time (py -3 works on Windows). Team rule: facts rows updated per round (directive #3/#4).
import os, subprocess, datetime, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "SCOREBOARD_FACTS.tsv")
OUT = os.path.join(ROOT, "PLAYER_STATUS.html")
rows = {"DONE": [], "COMING": [], "STUCK": []}
for line in open(SRC, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.startswith("#"): continue
    p = line.split("\t")
    if len(p) < 5 or p[0] not in rows: continue
    rows[p[0]].append(p)
try:
    now = subprocess.check_output(["date", "+%Y-%m-%d %H:%M +07:00"], env={**os.environ, "TZ": "Asia/Bangkok"}).decode().strip()
except Exception:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
SEC = [("DONE", "ทำได้จริงแล้ว - บนบูตปกติไร้แฟล็ก", "#1E7A46"),
       ("COMING", "กำลังมา - โค้ดถึง main / รอ merge / รอเทสตา", "#9A6E0E"),
       ("STUCK", "พิสูจน์แล้วแต่ยังไม่ถึงมือผู้เล่น (หนี้ท่อ promotion)", "#B3403A")]
h = ["<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
     "<title>Pirate Force - Player Status</title><style>",
     "body{margin:0;background:#F4F5F2;color:#1C2733;font-family:'Segoe UI','Leelawadee UI',Tahoma,sans-serif;line-height:1.6}",
     ".w{max-width:860px;margin:0 auto;padding:32px 20px}",
     "h1{font-size:26px;border-bottom:3px solid #A87514;padding-bottom:10px}",
     ".stamp{color:#5B6B7A;font-size:13px;margin-bottom:24px}",
     "h2{font-size:16px;margin:26px 0 8px}",
     "table{width:100%;border-collapse:collapse;background:#fff;font-size:14.5px}",
     "td{border:1px solid #DCE1E0;padding:8px 12px;vertical-align:top}",
     "td.ev{white-space:nowrap;font-family:Consolas,monospace;font-size:12px;color:#5B6B7A}",
     "td.what{font-weight:600;width:34%}",
     "@media(prefers-color-scheme:dark){body{background:#10171E;color:#E8ECEF}table{background:#19222B}td{border-color:#2A3541}td.ev{color:#93A2AF}}",
     "</style></head><body><div class='w'>",
     "<h1>Pirate Force - วันนี้ผู้เล่นทำอะไรได้จริงบ้าง</h1>",
     "<div class='stamp'>generate อัตโนมัติจาก SCOREBOARD_FACTS.tsv - " + html.escape(now) + " - รันซ้ำได้ทุกเมื่อด้วย OPEN_SCOREBOARD.bat</div>"]
for key, title, color in SEC:
    h.append("<h2 style='color:%s'>%s (%d)</h2><table>" % (color, html.escape(title), len(rows[key])))
    for p in rows[key]:
        h.append("<tr><td class='what'>%s</td><td>%s</td><td class='ev'>%s<br>%s</td></tr>" %
                 (html.escape(p[1]), html.escape(p[2]), html.escape(p[3]), html.escape(p[4])))
    h.append("</table>")
h.append("<div class='stamp' style='margin-top:24px'>กติกา: ใครเปลี่ยนข้อเท็จจริงต้องแก้แถวใน SCOREBOARD_FACTS.tsv รอบเดียวกัน (PANYA-DIRECTIVE ข้อ 3-4) - adversary ตรวจตามข้อ 6</div></div></body></html>")
open(OUT, "w", encoding="utf-8").write("\n".join(h))
print("wrote PLAYER_STATUS.html: DONE=%d COMING=%d STUCK=%d" % (len(rows["DONE"]), len(rows["COMING"]), len(rows["STUCK"])))

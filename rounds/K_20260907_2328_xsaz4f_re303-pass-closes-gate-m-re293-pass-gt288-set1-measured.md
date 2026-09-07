รอบ `xsaz4f` · เริ่ม 2026-09-07T23:13+07:00 · claim (ไม่มี PR อื่นของ LANE-K เปิดอยู่ตอนเริ่มรอบ — ไม่ใช่ takeover)

## ล็อกรอบ
`pf_bridge` PR #1810 `[LANE-K] round xsaz4f: claim` — ไม่มีล็อก LANE-K อื่นเปิดอยู่ก่อนหน้า (list ตรวจแล้วตอนเริ่มรอบ)
ไม่มี PR ฝั่ง `pirate-force-server` (สายนี้ไม่แตะโค้ดเซิร์ฟเวอร์)

## ล็อกไฟล์ที่อ่านต้นรอบ (ตามลำดับ COMMON_LANE_ROUND)
1. `NOW.md` (origin/main)
2. กล่องจดหมาย `ADDRESSEE: LANE-K` (ขยายเป็นสแกน `*RESULT*`/`*RESULTS*` ทั้งหมดด้วย เพราะพบว่าจดหมายผลหลายฉบับไม่มีบรรทัด `ADDRESSEE:` แต่อยู่ในสโคปพับผลของสายนี้ตาม `prompts/LANE-K.md` "แหล่งความจริงของสาย")
3. ไม่ได้อ่าน `AGENTS.md` §7 รอบนี้แยก — เนื้อหากติกาล็อกรอบ/หลักฐาน/PR อ่านจาก `prompts/COMMON_LANE_ROUND.md` ที่ fetch สดจาก origin/main แล้ว
4. ไฟล์รอบล่าสุดของสาย: `rounds/K_20260907_2234_lruqz2_*.md` หัวข้อ "รอบหน้าทำอะไร" — ดูด้านล่างว่าอะไรทำแล้ว/อะไรยัง

## จดหมายที่ consume/พับรอบนี้ (16 ฉบับ)
1. `20260906_1939_LANE-A-R322A-CONSUMED-*.md` — แก้ CLIENT_RE_QUEUE.md:122 (330 แถว) · ส่วนที่เหลือทับซ้อนกับ RE-289 ที่ปิดไปแล้ว
2. `20260906_2142_KA1A-PANYA-ORDER-COO-RE155-*.md` — ทำไปแล้วเต็มที่ (GT-288 ตั้งเลข/spawner/candidate list)
3. `20260906_2150_KA1A-PANYA-ORDER-COO-RE155-addendum-*.md` — ทำไปแล้ว (สองต้นแบบ + ตารางสีอยู่ใน GT-288)
4. `20260907_0159_KA1A-PANYA-ORDER-COO-headless-proof-*.md` — codified เป็นข้อ 7/8 ของ `prompts/LANE-K.md` แล้ว
5. `20260907_1313_KA1A-PANYA-DECISION-COO-hostile-is-rank-ai-only-*.md` — งานของ K (แก้หัวใบ Orc Chief/103) ทำไปแล้วรอบ `spppsd`
6. `20260907_1825_KA1A-PANYA-DECISION-COO-m2-last-mile-*.md` — ทำไปแล้ว (RE-303 ตั้งเลขรอบ `qz3m7v` และตอนนี้ PASS)
7. `20260907_2006_FROM_CHIEF-TO-K-census-frame-*.md` — ปลดบล็อกซ้ำซ้อน (GT-288 พลิก READY ไปแล้วก่อนหน้านี้)
8. `20260907_2043_RE-293-RESULT-item2-*.md` — พับ PASS/DONE เข้าหัวใบ RE-293
9. `20260907_2053_RE-296-RESULT-avt-path-*.md` — พับต่อท้าย result block ของ RE-296 (ใบปิดแล้ว ไม่เปิดซ้ำ) + ส่งต่อ COO เรื่องปลดรายการ MONSTER_PRESENTATION
10. `20260907_2150_RE-303-RESULT-teleportcheck-*.md` — พับ PASS เข้าหัวใบ RE-303 + result: line
11. `20260907_2155_RE-303-ARTIFACT-probe-sources-*.md` — informational เท่านั้น
12. `20260907_2158_RE-303-ADDENDUM-the-auto-ack-gate-*.md` — informational เท่านั้น (ใบระบุเองว่าไม่ต้องพับ)
13. `20260907_2238_LANE-A-TO-K-re-body-ADDENDUM-re303-*.md` — แก้สองข้อเท็จจริงใน `tickets/RE-303.md` คำต่อคำ
14. `20260907_2241_COO-DECISION-k2234-*.md` — ข้อ 3 ทำแล้ว (สอง `.CONSUMED.txt` ของจดหมาย 0922)
15. `20260907_0922_FROM-CHIEF-TO-COO-922-index-refuted-*.md` — ผูก `.CONSUMED.txt` ชี้ไปคำตอบจริงที่ `1041`
16. `20260907_0922_LANE-E-ASK-COO-neither-form-is-legal-*.md` — ผูก `.CONSUMED.txt` ชี้ไปคำตอบจริงที่ `1041`
17. `20260907_2305_KA1A-R323D-RESULTS-*.md` — พับ RE-305 (WIRE-HALF-DONE) + GT-288 ชุด 1 (MEASURED) + เขียนสเปกชุด 3 ใหม่ต่อท้าย `tickets/GT-288.md`

(นับได้ 17 ไม่ใช่ 16 — แก้ตัวเลขในจดหมายรอบให้ตรง: **17 ฉบับ** ไม่ใช่ 16 ตามที่เขียนพลาดไว้ในจดหมายถึง COO)

## เนื้อใบที่แก้/เขียนเพิ่ม
- `tickets/RE-303.md` — สองแก้ไขข้อเท็จจริง (t_telwithveh.lua 7 บรรทัด cp874 · เลขบรรทัด :795 → สตริงค้นหา) คำต่อคำจากผู้เขียนเนื้อใบเอง
- `tickets/GT-288.md` — เพิ่มผลชุด 1 เต็ม (wire + ตารางสีบนจอ 8 หุ่น) และสเปกชุด 3 ใหม่ (identity-sign sweep) แทน SPEC ONLY เดิม (เก็บของเดิมไว้ ไม่ลบ)
- `CLIENT_RE_QUEUE.md` — หัวใบ RE-303/RE-293/RE-296/RE-305 พับผล + แก้ตัวเลข SCENE_NAME_TIP
- `GAME_TEST_QUEUE.md` — หัวใบ GT-288 เพิ่มบล็อกผลชุด 1
- `QUEUE_STATUS_SNAPSHOT.md` — ย้าย RE-293/RE-303 จากหมวด "หยิบได้" ไปหมวด "✅ ตอบแล้ว" + เพิ่มส่วนรอบ `xsaz4f`

## ตรวจก่อน push
- `python3 tools_bridge/pf_gate_preflight.py --bridge-only --bridge-root .` → **PASS** (ทั้งสองไฟล์คิวไม่เกินเพดานไม่โตเกิน 50,000 B/PR · ไฟล์ใหม่ 1 ไฟล์ไม่เกิน 100 ตัวอักษร · ไม่แตะ `.claude/` · consumedstub ผ่าน)
- server repo: ไม่มีการเปลี่ยนโค้ดเซิร์ฟเวอร์รอบนี้ ⇒ ไม่มี PR ฝั่ง `pirate-force-server` ต้องเปิด
- `git status --short` ท้ายรอบ: ตรวจแล้วเฉพาะไฟล์ที่ตั้งใจแก้/สร้าง — stage ทีละก้อน ไม่ใช้ `git add -A`

## ที่ยังพับไม่ได้รอบนี้
- `SKILL-ATTR-REAL-IDS-AT-AN-OPEN-WINDOW-001` (LANE-CS) — เจ้าของใบสั่งเองว่าอย่าเพิ่งตั้งเลขจนกว่า COO ตอบสองข้อ
- `SKILL-LIST-AT-LOGIN-ONE-FRAME-001` (LANE-CS) — เจ้าของใบขอสถานะ `HELD-ON-BUILD` จนจุดเสียบ (env-gated) ลง main แล้วส่งโทเคนจริง

## ที่ต้องแจ้ง COO
- ส่งจดหมายแยก `20260907_2327_LANE-K-ASK-COO-re296-outfit-selection-list-item-lift.md` — ปลดรายการ MONSTER_PRESENTATION เฉพาะส่วน outfit ได้ไหม

## รอบหน้าทำอะไร
1. เกรปกล่องหา `*-TO-K-*` ใหม่ก่อนเริ่มงานอื่น (กติกาที่ตั้งไว้ตั้งแต่รอบ `lpjqus`)
2. ตรวจว่า `SKILL-ATTR-REAL-IDS-AT-AN-OPEN-WINDOW-001` / `SKILL-LIST-AT-LOGIN-ONE-FRAME-001` มีจดหมายแจ้งจาก LANE-CS เองหรือยังว่าจุดเสียบลง main แล้ว — ถ้ามี ตั้งเลขทันที (เลขว่างถัดไป = 308)
3. ตรวจว่า COO ตอบ `20260907_2327_LANE-K-ASK-COO-re296-*` แล้วหรือยัง แล้วปรับ `external/PF_MONSTER_PRESENTATION.md` ตามคำเคาะ (ถ้า COO สั่งให้ K แก้)
4. เกรป `pirate-force-server` main หา `ItemOperateVitalRes`/reply handler ของ op=5 (BUILD_PROPOSED ของ LANE-DB จาก RE-305) — ยังไม่ต้องทำอะไรจน LANE-DB ส่งมา
5. เกรปว่า LANE-B เริ่มเขียนโค้ดชุด 3 ใหม่ของ GT-288 (identity-sign sweep) หรือยัง

SCOREBOARD: NONE | คิวพูดความจริงขึ้น 6 ใบ (พับผล 5 · แก้เนื้อใบ 2 จุด) รวมถึงปิด "ประตู M" ของ M2 — ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ | notes_to_chief/20260907_2328_LANE-K-ROUND-xsaz4f.md

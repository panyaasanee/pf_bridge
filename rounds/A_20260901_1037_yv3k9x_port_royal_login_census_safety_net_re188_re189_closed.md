# รอบ A_20260901_1037 (yv3k9x) — Port Royal login-census safety net (PANYA-ORDER 0955), RE-188/RE-189 ปิด

## Protocol A (ชะตา PR รอบก่อน)
`server#457` / `pf_bridge#686` (round `j3w14z`): `merged: true` ทั้งสอง repo (ตรวจด้วย
`pull_request_read` method=get ตรงเลข ไม่เชื่อ `list_pull_requests` เฉย ๆ) ⇒ ไม่มีอะไรต้อง recover
ไม่มี `[LANE-A]` PR เปิดค้างตอนต้นรอบ (มีแค่ `[LANE-GM]` #460 เปิดอยู่ฝั่ง server — ไม่ใช่ล็อกของสายนี้
ไม่แตะ)

## Protocol B (กล่องจดหมาย)
ตรวจ `ADDRESSEE: LANE-A` ใน `notes_to_chief/` (root) เทียบกับ `.CONSUMED.txt`: ไม่มีใบติดแท็กตรงค้าง
แต่พบสามใบที่สายนี้เป็นเจ้าของ/ต้องบริโภคจริงตามกฎ B (ผู้เปิดใบบริโภคผลเอง):
- `20260901_0949_RE-188-RESULT-*` (LANE-A เปิด RE-188 เอง) — บริโภคแล้วรอบนี้ ปิดหัวใบ DONE/CONFIRMED-NO-CHANGE
- `20260901_1008_RE-189-RESULT-*` (LANE-A เปิด RE-189 เอง) — บริโภคแล้วรอบนี้ ปิดหัวใบ DONE/PASS-MIXED
- `20260901_0955_PANYA-ORDER-login-path-*` (จ่าหน้าถึง chief cc สาย A) — ไม่มีใบมอบหมายจาก chief ก่อน
  ต้นรอบนี้ (10:24) และไม่มี `*CLAIM*` ค้างของสายอื่นในหน้าต่าง 90 นาที ⇒ จองเอง (`20260901_1037_CLAIM-
  LANE-A-round-yv3k9x-*`) ตาม COO-DECISION 20260830_2244 (ใบสั่งงานที่ระบุผู้ทำได้มากกว่าหนึ่งสาย)

## บริบทเทมเพลตต้นรอบ (ยืนยันซ้ำ ตาม COO-DECISION 20260901_0848)
`BUILD-001`/`BUILD-002` ตามที่พรอมป์ต้นรอบเขียนไว้ปิดจริงไปแล้วตั้งแต่ 29 ส.ค. (`COO-DECISION
20260829_1941` x2, `GT-131 PASS`, `GT-078 CLOSED`) — ข้อความ "เลยกำหนด" ในเทมเพลตเป็นของเก่า
เจ้าของยังไม่ได้แก้ Routine prompt งานรอบนี้จึงไม่ใช่การสาน BUILD-001/002 อย่างเป็นทางการ แต่เป็นงาน
ใหม่ภายใต้จิตวิญญาณเดียวกัน (M1 "เมืองมีชีวิต") ที่เจ้าของสั่งตรงเมื่อ 09:55 วันนี้

## งานที่ทำ — Port Royal login-census safety net

**ปัญหาที่วัดได้ (จากคอมเมนต์ที่มีอยู่แล้วใน `runtime.py`, ไม่ใช่การเดา):** login เข้า Port Royal
ไม่ส่งสำมะโนจนกว่าผู้เล่นจะเดินก้าวแรก (`runtime.py:7578-7582` ต้องมี `last_target_pos is not None`
สำหรับ scene 1) เพราะถ้าส่งก่อนเดิน `self.population_indices` จะถูกตั้งก่อนที่ dispatcher เดิม
(`current/pf_login_game_server_v141.py:4395-4416`) จะมี `last_target_pos` ให้ unpack — คลิก NPC
ก่อนเดินจะ `TypeError` กลาง listener thread (ไม่มี `except`) = หลุดการเชื่อมต่อ

**ทำได้ในเขต LANE-A (ไม่แตะ `runtime.py`):** `runtime.py`'s ChooseNPC/TARGET_VITAL guard
(`:7088-7160`) เป็น scene-agnostic อยู่แล้ว — เพิ่ม scene ใหม่เข้า `lane_hooks.
choose_npc_responder` ไม่ต้องแก้ runtime.py เลย สร้าง
`src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py` (ตอบคลิกแทน dispatcher เดิม
สำหรับ scene 1 เมื่อเปิดใช้งาน) มิเรอร์ pattern ของ `lane_a_choose_npc_scene14.py` แต่ต่างที่จุดเดียว
ที่สำคัญ: เมื่อ `last_target_pos is None` (สภาพปกติของ login ก่อนเดิน) responder นี้ **ตอบ ไม่ปฏิเสธ**
โดยหันหน้า NPC ไปทิศเดียวกับที่สำมะโน arrival กำหนดไว้แล้ว (`world_population.HEADINGS`) แทนการเดา
ทิศไปหาผู้เล่น — ไม่ประดิษฐ์ตำแหน่งใดที่ไม่มีอยู่จริง

`production_allowed = False` โดยตั้งใจ (สองเหตุผลอิสระกัน อยู่ใน docstring ของไฟล์เอง): (1) trigger
ยังไม่กว้างพอให้เกิด crash วันนี้ (2) เปิดแล้วจะสลับ path ที่ตอบคลิก scene 1 ทั้งหมดทันที รวมคลิกหลัง
เดินที่ dispatcher เดิมตอบถูกอยู่แล้ว — ไม่มี pf-adversary ให้เรียกรอบนี้ (เหมือนที่ LANE-GM รายงานไว้
`20260901_1018_LANE-GM-STATUS-*`) จึงเลือกฝั่งปลอดภัยกว่า รอ adversary/attended click parity ก่อน

เขียนเทส `tests/test_lane_a_choose_npc_scene1.py` (15 เทส) ครอบคลุม: registry/withdrawal ตาม gate,
คลิกมี anchor (หันหน้าผู้เล่น), คลิกไม่มี anchor (หันหน้าตาม arrival heading), P30 monster HP override
ไม่หาย, fail-closed สำหรับ placement ที่ไม่มีจริง, decline นอก population_indices/scene ผิด/registry ปิด,
multi-select answers เฉพาะตัวแรก (gap เดียวกับ scene 14 ที่ pin ไว้ ไม่ใช่ bug ใหม่)

รันเทสทั้งชุด (`pytest tests/`): **6188 passed, 327 skipped, 0 failed** — ไม่มี regression

## CORE-REQUEST ถึง chief

ส่งจดหมาย `20260901_1037_LANE-A-STATUS-port-royal-login-census-safety-net-built-core-request-
for-chief.md` — ขอกว้างเงื่อนไขที่ `runtime.py:7578-7582` (ตัด `last_target_pos is not None or`
สำหรับ scene 1) **แต่มีคำเตือนชัดเจน: ห้ามเดินสายก่อนเห็นจดหมายยืนยันว่า `lane_a_choose_npc_scene1.
production_allowed = True` บน main แล้ว** — ไม่งั้นจะเปิด crash เดิมกลับมาทันที (ลำดับสำคัญ: safety
net ต้องมาก่อน trigger widen)

## เปิดใบเทส

`GT-189 PORT-ROYAL-LOGIN-CENSUS-NO-WALK-001` เพิ่มท้าย `GAME_TEST_QUEUE.md` — สถานะ `BLOCKED`
จนกว่าทั้งสองครึ่งจะ merge (responder gate เปิด + runtime.py trigger กว้างขึ้น) มี RECHECK command
ให้ตรวจก่อนบูตจริง

## RE-188 / RE-189 ปิด

- `RE-188` (Bg0002's 96 placements ที่เหลือ, CLINE crosswalk): **CLOSED DONE/CONFIRMED-NO-CHANGE**
  — CLINE เป็น client map/list crosswalk ไม่ใช่กติกา world-actor-at-placement, ไม่มี candidate ใดมี
  placement-specific evidence, `BUILD_IMPACT: NONE`, ไม่แก้ `scene2_prison_exile_tables.py`
- `RE-189` (writer ของ `[object+0x18]`, GT-033 branch matrix): **CLOSED DONE/PASS-MIXED** —
  server response ไม่มีทางเขียน `[object+0x18]` ได้เลย (local UI เท่านั้น) กิ่ง 2/3/6 ของ `GT-033`
  buildable ด้วยสถาปัตยกรรมนี้ (**เลื่อนไปรอบถัดไป** — PANYA-ORDER 09:55 เร่งด่วนกว่ารอบนี้) กิ่ง 1/5
  ต้อง CORE-REQUEST plumbing ใหม่ ยังไม่ส่ง

ทั้งสองใบปิดหัวใน `CLIENT_RE_QUEUE.md`, ย้ายต้นฉบับผลเข้า `consumed/`, วาง `.CONSUMED.txt` stub

## ไฟล์ที่แตะรอบนี้

pirate-force-server (2 ไฟล์ใหม่):
- `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py` (ใหม่)
- `tests/test_lane_a_choose_npc_scene1.py` (ใหม่)

pf_bridge (8 ไฟล์):
- `rounds/A_20260901_1037_yv3k9x_*.md` (ไฟล์นี้)
- `notes_to_chief/20260901_1037_CLAIM-LANE-A-round-yv3k9x-*.md` (สร้าง + ย้ายเข้า consumed/ รอบเดียวกัน)
- `notes_to_chief/20260901_1037_LANE-A-STATUS-port-royal-login-census-safety-net-*.md` (ใหม่, CORE-REQUEST)
- `notes_to_chief/consumed/20260901_0949_RE-188-RESULT-*.md` (ย้ายจาก root)
- `notes_to_chief/20260901_0949_RE-188-RESULT-*.md.CONSUMED.txt` (ใหม่)
- `notes_to_chief/consumed/20260901_1008_RE-189-RESULT-*.md` (ย้ายจาก root)
- `notes_to_chief/20260901_1008_RE-189-RESULT-*.md.CONSUMED.txt` (ใหม่)
- `CLIENT_RE_QUEUE.md` (แก้ 2 หัวใบ: RE-188, RE-189)
- `GAME_TEST_QUEUE.md` (เพิ่ม GT-189)

ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน: ยังไม่มีอะไรเลยบนจอวันนี้ — รอบนี้สร้างครึ่งที่ปลอดภัย (click
responder, ปิด gate ไว้) และส่ง CORE-REQUEST ให้ chief ทำอีกครึ่ง (runtime.py trigger) เมื่อทั้งสอง
ครึ่งลง main และ gate เปิด ผู้เล่นจะเห็น NPC ยืนอยู่ใน Port Royal ทันทีตอน login โดยไม่ต้องเดินก่อน

-- LANE-A (WORLD)

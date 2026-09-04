# LANE-A round 53udzq — 2026-09-05T03:06+07:00 start

NOW ข้อไหนขยับรอบนี้: **ไม่ขยับ M2** (ยังรอ `GT-233` เครื่องคุณ) แต่ปิดตัวบล็อกโค้ด
ของ GT-233 หนึ่งชั้น (encoder ยืนยันตรงกับ RE-227 และ capture จริงของ R313 แล้ว
ไม่ใช่สาเหตุที่ client ปฏิเสธ) และปิดหนี้ `1339`/`0251` (MEASURED_SCENE_IDS)

## ล็อกต้นรอบ

- list PR `[LANE-A]` เปิดทั้งสองรีโป ก่อนแตะโค้ด: ไม่มี (server: `#782` LANE-B,
  `#783` LANE-DB เท่านั้น · bridge: `#1243` LANE-DB, `#1245` LANE-GM, `#1246`
  LANE-B) ⇒ ไม่มีรอบค้าง ไม่ต้องถอย ไม่ต้อง takeover
- PR รอบก่อนของสายนี้ (`qqqtqp`): server `#780` merged=true 2026-09-04T19:20:31Z ·
  bridge `#1236` merged=true 2026-09-04T18:59:30Z — งานอยู่บน main แล้ว ไม่ต้องกู้

## กล่องจดหมาย บริโภคแล้ว

- `20260905_0212_KA1A-R313-RESULTS-*` (GT-233 STOP, ErrorData=50351) — ดูหัวข้อ 2
  ด้านล่าง · stub วางแล้ว
- `20260905_0251_COO-DECISION-measured-scene-ids-*` (LANE-A) — ดูหัวข้อ 1 · stub วางแล้ว

## 1. `MEASURED_SCENE_IDS` ขยาย `(1, 2)` -> `(1, 2, 3, 4, 5, 14, 126)`

ตาม `COO-DECISION 20260905_0251` ข้อ (ก): เงื่อนไขที่สายนี้ตั้งเอง (GT-210/GT-212
ต้องปิดก่อน) ครบแล้ว ทุกเลขมีคอมเมนต์อ้างใบ/รอบของตัวเอง (`world_scene_travel.py`) ·
126 ต้องระวังเป็นพิเศษ: วัดแล้ว (`sent_before=True`) แต่แถวตารางยังไม่มี save/marker
เหมือนฉากอื่น (ตาม COO ข้อ (ค) — สองอย่างนี้เป็นคนละคำตอบกัน) เทสใหม่แยกสองกรณีนี้
ออกจากกันชัดเจน ไม่ปล่อยให้ loop เดิมกลืนพัง (มันจะพังจริง — เจอตอนรันเทสรอบแรก
`test_the_two_measured_scenes_do_not` แดงเพราะ 126 ไม่มี save/marker)

แก้ถ้อยคำเก่าที่ล้าสมัยไปด้วย: `lane_a_choose_npc_roster_scenes.py` (เคยเขียนว่า
GT-210/GT-212 ยังไม่รู้ผล) และ `world_m2_arrival.py` (ย่อหน้าที่อธิบายว่าทำไม
`sent_before` เป็น False สำหรับฉาก 3 — ตอนนี้ COO ตอบแล้ว)

ตรวจแล้วว่าไม่กระทบพฤติกรรม: grep `sent_before`/`MEASURED_SCENE_IDS`/
`confirmed_by_a_client` ทั้ง `src/` อยู่ในรายงาน/console line เท่านั้น ไม่มีจุด
gate การตัดสินใจ (`login_entry_allowed` เป็นฟิลด์แยกที่คุมประตูล็อกอินจริง ไม่ถูกแตะ)

## 2. GT-233: encoder ตรงกับ RE-227 และ capture จริงของ R313 หรือไม่

R313 ส่ง `NavigationEx_AddSurveyDataVtial` จริงแล้วไคลเอนต์ปฏิเสธ `ErrorData=50351`
(เอ่ยชื่อคลาสเอง = msg_id ถูก) เทสใหม่ `R313CaptureParityTests` เรียก encoder ด้วย
ค่าที่จดหมายบันทึกไว้ (survey_id=2, XYZ, msg_id, version=0) แล้วเทียบกับ hex จริง
ที่ R313 วาง — **ตรงกันทุกไบต์** ทั้งชั้น `pc` (60 B) และ `frame` (70 B, คำนวณจาก
`frame_pc()` จริง ไม่ใช่เดา) ⇒ ปิดคำอธิบาย "encoder ผิดจาก RE-227" ทิ้งได้ ที่เหลือ
สงสัยคือสี่ฟิลด์ UNMEASURED เดิมของ RE-227 + `vital_version` — ปิดต่อไม่ได้จาก static
เพราะเครื่องนี้ไม่มี `GameClient.local.bin` ส่งจดหมายขอ chief แก้หัว GT-233

## pf-adversary

รอบเดียว (สั่งต้นรอบ) เจอ 2 จริง แก้ครบ:
1. ร่างแรกอ่าน "70 B" ในจดหมาย R313 ว่าเป็นคำพลาด — **ผิด**: `frame_pc(pc)` ให้ 70
   ไบต์จริง (คำนวณตรงจากโค้ด) ทั้ง 60/70 ถูกทั้งคู่ คนละชั้น แก้ทั้งในโมดูล/เทส/
   จดหมาย/stub แล้วเติม assertion `len(frame)==70` กันอ่านผิดซ้ำ
2. docstring เขียนว่า "GT-233's queue head carries BLOCKED-ON-LAYOUT" เป็นข้อเท็จจริง
   ทั้งที่หัวใบยังเป็น READY (ตั้งก่อน R313) และจดหมายรอบนี้เองก็เขียนว่าเป็นคำขอ
   ("ถ้าเห็นด้วย") — แก้ docstring ให้ตรงกับจดหมาย ไม่อ้างว่าเป็นจริงแล้ว
เจอแต่ไม่ใช่บั๊ก (ตรวจแล้วผ่าน): hex ตรงกับต้นฉบับทุกไบต์ · ขยาย MEASURED_SCENE_IDS
ไม่กระทบ control flow · เทสไม่ vacuous (มิวเทตทั้ง encoder และ tuple แล้วเทสแดงจริง)
· ขอบเขตตรงกับที่ COO อนุมัติจริง (อ่านจากใบตรง ๆ) · เครื่องสำอาง 2 จุด (ชื่อเทสเก่า
เปลี่ยนแล้ว, ชื่อเทสอีกตัวอ้างเกินขอบเขตนิดหน่อยแต่ docstring ในนั้นตรงอยู่แล้ว — ปล่อย)

## เทส

- ระหว่างทำงาน: 5 ไฟล์ที่แตะตรง (`test_navigationex_survey_record.py`
  `test_world_scene_travel.py` `test_world_scene_liveness.py`
  `test_world_m2_arrival.py` `test_lane_a_choose_npc_roster_scenes.py`) = 225 passed,
  447 subtests · ก่อนหน้านั้นไล่ทุกไฟล์เทสที่ import โมดูลที่แตะทั้งรีโป (~60 ไฟล์) =
  เขียวหมด ~2300 tests
- ชุดเต็ม รันบน commit สุดท้าย (`7caacd7f`) merge กับ `origin/main` สด (`2ff1e30d`):
  **10432 passed, 323 skipped, 19600 subtests, 2 failed** ใน 463 วิ · 2 ใบที่แดง
  (`test_pytest_precondition_census.py::WindowsGateExclusionPinTests`) ไม่ใช่ของรอบนี้
  — bisect ด้วยการ `git checkout origin/main -- .` บน branch เดียวกันแล้วรันซ้ำ = 0
  แดง ⇒ มีอยู่แล้วบน main ก่อนรอบนี้แตะ 🔴 **รันชุดเต็มสองครั้งรอบนี้ เหตุผล: ครั้งที่สอง
  คือการ bisect ยืนยันว่า 2 ใบแดงไม่ใช่ของ diff นี้ ไม่ใช่การรันซ้ำเฉย ๆ**

## จบรอบ

1. push ครบสองรีโปแล้ว
2. server: PR `#785` เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด · GET
   ยืนยัน marker อยู่จริง
3. bridge: ไฟล์รอบนี้ + จดหมาย `20260905_0306_LANE-A-TO-CHIEF-*` + stub
   `.CONSUMED.txt` สองไฟล์ ลงกิ่ง claim เดียวกัน (ลบ `_claim.md`) แล้วเติม
   `PF-AUTOMERGE: v4` ให้ claim PR `#1247` ทีหลังสุด
4. **push แล้ว รอ merge PR `#785`** สถานะเซิร์ฟเวอร์: เปิดแล้ว รอ gate

## งานสำรอง (ไม่ต้องใช้รอบนี้ — มีงานหลักเต็มแล้ว)
ถ้ารอบหน้าไม่มีอะไรจาก chief/RE ให้ทำ: (1) M2 ขั้นถัดไปที่ไม่พึ่ง identity (แผนที่
ทะเล/เป็นเรือ ตาม travel model) (2) ตรวจใบ `GT-243`/`GT-230` ว่ามีส่วนที่ LANE-A
ช่วยเตรียมได้หรือไม่ (3) เก็บ debt ที่ pf-adversary เคยชี้ในไฟล์สายนี้ที่ยังไม่ปิด

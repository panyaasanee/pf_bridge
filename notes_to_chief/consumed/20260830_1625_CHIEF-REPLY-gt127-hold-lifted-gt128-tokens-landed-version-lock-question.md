[ถึง: COO, LANE-GM | cc: Panya, ผู้เทสทุกกะ | จาก: chief (LANE-E) รอบ `3ru85y` (R243) · 2026-08-30T16:25+07:00]
[ตอบใบ: `20260830_1541_COO-DECISION-gm-lane-blocked-on-chief-gt127-gt128-priority.md`]

# CHIEF-REPLY — GT-127 HOLD ปลดแล้ว (wire/DB PASS) · GT-128 โทเคนลงแล้วตามสั่ง แต่ใบทั้งใบยังบูตไม่ได้เพราะ COO lock อีกชั้นหนึ่ง

## สั้นที่สุด

ทั้งสองใบแตะแล้วรอบนี้ ก่อนกำหนด 21:00 ตามที่ COO สั่ง คนละผลลัพธ์:

- **`GT-127`**: HOLD ที่ค้างมาตั้งแต่ R237 **ปลดแล้ว** — เหตุจริงคือ label ในคิวไม่เคยถูกอัปเดตหลัง
  LANE-GM ปิดครึ่งที่เหลือของ `GM-032` ข้อ 1-2 ไปแล้ว (ยืนยันคู่กันในใบ `20260830_1318` ของ
  LANE-GM เอง) — ไม่ใช่โค้ดค้าง เป็นป้ายค้าง แก้ที่ `GAME_TEST_QUEUE.md`
- **`GT-128`**: โทเคน `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` ที่ COO สั่งตรง ๆ **ลงแล้ว**
  (`CORE-REQUEST-GM-030`/`-031` ของ LANE-GM ครบทั้งสองข้อฝั่ง chief) แต่ **ใบนี้ทั้งใบยังบูตไม่ได้**
  เพราะมี COO lock อีกชั้นที่ไม่ใช่เรื่องโทเคน — ดูข้อ 3 ข้างล่าง

## 1. `GT-127` — ปลด HOLD

`src/pirateforce_foundation/gm/commands.py` (LANE-GM's write zone) ตั้ง
`session._gm_action_queued_confirm = (action, callback)` และเขียน `OUTCOME_QUEUED` ในคอลแบ็ก
ตามที่ `CORE-REQUEST-GM-040` ขอ — อยู่บน main แล้วตามที่ LANE-GM วัดเองในใบ `20260830_1318`
รอบนี้ผมรัน `tests/test_gm_chat_command_dispatch_wiring.py::QueuedRowLandsEndToEndTests` สดอีกครั้ง
(ผ่าน dispatcher จริง ไม่ผ่าน mock): ผ่านครบ ยืนยันว่าคำสั่ง GM ที่ถูก append จริงเขียนแถว ndjson
`outcome:queued` ที่ซื่อสัตย์ ⇒ `CORE-REQUEST-GM-032` ข้อ 1-3 ครบทั้งสามข้อบน main

**nonclaim:** ผมไม่ได้เดินด่าน 2 เต็ม + P1-P4 ของใบนี้ทั้งหมดรอบนี้ (นอกเวลาที่มี) — HOLD ที่ปลด
คือ "ตัวบล็อกที่ระบุไว้หมดแล้ว" ไม่ใช่ "เกรด PASS แล้ว" รอบถัดไปที่แตะใบนี้ต้องเดินเช็คลิสต์เต็มก่อนเกรด

## 2. `GT-128` — โทเคนที่ COO สั่งตรง ๆ ลงแล้ว

`_gm_warp_open_confirm_window` / จุดพิมพ์โทเคนเดิม / `_gm_warp_close_confirm_window` ใน
`runtime.py` ต่อกับ `gm.warp_target_record` ตาม `CORE-REQUEST-GM-030`/`-031` ครบ: MATCH/MISMATCH
พิมพ์เพิ่มจากโทเคนเดิม (ไม่แทนที่ — ตรวจแล้วว่าเงื่อนไขเดิมของ `GM_WARP_POSITION_CONFIRMED` ไม่ถูกแตะ)
เทสใหม่ 5 ใบพิสูจน์ทั้ง MATCH, MISMATCH พร้อมระยะ, ไม่มี warp แล้วไม่มีทั้งคู่, target ไม่ค้างข้ามเฟรม
(กรณีสำคัญที่สุด) สวีตเต็ม `5480 passed, 323 skipped, 9129 subtests` เขียว(cloud sanity)

**pf-adversary รีวิวก่อน commit พบสองข้อ:**

a. กิ่ง `gm_warp_position_target_unknown_character_mismatch` ที่ `CORE-REQUEST-GM-031` ข้อ 5 ขอ
   เป็น **dead code ในโปรดักชันจริง** — `gm_warp_pending_character` กับ `record.character_id` ถูก
   set จากตัวแปรเดียวกันเสมอที่จุด arm เดียวกัน ⇒ ทุก re-select จริงที่จะทำให้สองค่าไม่ตรงกัน
   จะโดนการ์ด `character_changed` เดิมดักไว้ก่อนถึงกิ่งใหม่เสมอ เทสที่พิสูจน์กิ่งนี้ต้อง park เป้าหมายตรง
   ผ่าน `record_warp_target` เอง ไม่ผ่านเส้นทาง `/warp` จริง — [ไม่อ้าง] ว่ากิ่งนี้ยิงได้จริงวันนี้ เขียน
   คอมเมนต์เปิดเผยไว้ในซอร์สแล้ว (`runtime.py:_gm_warp_open_confirm_window`) **ถามกลับ LANE-GM**:
   ตั้งใจให้เป็น defense-in-depth เฉย ๆ หรืออยากให้ผมสลับลำดับการ์ดให้กิ่งนี้ไปถึงได้จริง (ต้องแตะ
   การ์ด `character_changed` เดิม ซึ่งกระทบ event `gm_warp_position_not_confirmed_character_changed`
   ที่มีอยู่แล้ว — ไม่ทำเองรอบนี้เพราะเป็นการเปลี่ยนพฤติกรรมที่มีอยู่ ไม่ใช่แค่เพิ่ม)
b. บั๊กเดิมที่ไม่เกี่ยวกับ diff นี้แต่ pf-adversary จับได้ระหว่างรีวิว: warp เป็นตัวละคร A แล้ว
   re-select เป็น B แล้ว warp อีกครั้งก่อนมี TargetPos ใด ๆ — `gm_warp_pending_character` ไม่ถูก
   อัปเดตเป็น B (โค้ดเดิม ก่อนรอบนี้) ⇒ TargetPos ของ B โดนการ์ด `character_changed` ดักทิ้งทั้งที่
   เป็น warp ที่ถูกต้องของ B เอง ⇒ ไม่มีโทเคนไหนพิมพ์เลยสำหรับ warp ที่ B เพิ่งสั่ง — [ไม่อ้าง] ว่าแก้
   รอบนี้ (นอกขอบเขตใบ `GT-128`) เปิดเป็นข้อสังเกตให้ LANE-GM ตัดสินว่าจะเปิดใบใหม่หรือไม่

## 3. 🔴 ตัวบล็อกจริงของ `GT-128` ยังไม่ปลด — เป็นคนละเรื่องกับที่ COO สั่ง

[วัดแล้ว] `src/pirateforce_foundation/gm/teleport_wire.py:151`:
`FORCE_POS_VITAL_VERSION_CONFIRMED = None` — ล็อกโดย `COO-DECISION 20260828_2130` ("ห้ามเปลี่ยน
จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main") จุดเขียนตำแหน่งนั้น (`CORE-REQUEST-GM-030`)
อยู่บน main มาตั้งแต่รอบ `fo2lgh` แล้ว แต่ **ค่าคงที่ยังไม่ถูกปลด** — ตามที่ใบ `GM-030` ข้อ ④ เขียนไว้เอง
ว่า "การปลดล็อกเป็นอำนาจ COO ไม่ใช่ผลอัตโนมัติของ grep"

⇒ วันนี้แม้โทเคน MATCH/MISMATCH จะพร้อมสมบูรณ์แล้ว **ไม่มีไบต์ `ForcePos` ออกสายเลยสักครั้ง**
เพราะโมดูลปฏิเสธเองที่ชั้นนี้ก่อนถึงจุดพิมพ์โทเคนด้วยซ้ำ ⇒ `GT-128` ยังบูตไม่ได้ ไม่ว่าจะเกรดหรือไม่เกรด
นี่คือคนละขั้นจาก "chief พิมพ์โทเคน" ที่ `COO-DECISION 20260830_1541` สั่งตรง ๆ — ข้อนั้นทำเสร็จแล้ว
**คำถามถึง COO:** ปลดล็อก `FORCE_POS_VITAL_VERSION_CONFIRMED` ตอนนี้ได้หรือยัง (เงื่อนไขข้อ ④ ของ
`GM-030` ครบแล้ว) หรือรอเหตุผลอื่นอยู่ — ถ้าปลด ต้องแก้ไฟล์เทสที่ล็อกไว้คู่กัน
(`tests/test_gm_force_pos_version_lock.py`) ในคอมมิตเดียวกันตามที่ `GM-030` ข้อ ④.5 เตือนไว้

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี — ทั้งสองใบยังเป็น `[attended, in-game]`/`[wire/DB เท่านั้น]` รอเช็คลิสต์เต็ม ไม่มีอะไรเปลี่ยน
บนหน้าจอผู้เล่นวันนี้

## nonclaim

grep/pytest/pf-adversary/GitHub API เท่านั้น ไม่มีการเปิด client ไม่มีการวัดกับ DB จริง

— chief, รอบ `3ru85y` (R243)

---
_Generated by [Claude Code](https://claude.ai/code)_

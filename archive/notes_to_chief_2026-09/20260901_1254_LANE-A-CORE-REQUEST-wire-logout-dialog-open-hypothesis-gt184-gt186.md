[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `bkgaq8` ·
2026-09-01T12:54+07:00]

# CORE-REQUEST — wire `logout_dialog_open_hypothesis.py` เข้า runtime.py (GT-184/GT-186)

## บริบท

`GT-184`/`GT-186` (UI-A ส่วนแรก/UI-B ปุ่ม logout จริง) `pf_bridge/GAME_TEST_QUEUE.md` เปิดโดย
chief เอง ตาม PANYA-ORDER `20260901_0215` และมอบให้ **LANE-A** เป็น build-owner lane (broadcast
letter รอบเดียวกัน) ทั้งสองใบ `[BLOCKED]` รอ "whatever NEW response/sequence the implementing
lane builds"

`RE-189` (ปิดแล้ว DONE/PASS-MIXED โดย LANE-A เอง รอบ `yv3k9x`) วัดสองเรื่อง: (Job 1) field
`[SystemSetting_LogoutConfirm+0x18]` ที่ transition gate `0x719620` อ่าน มี writer เดียวในกราฟที่
วัดได้ทั้งหมด คือ local UI binding ของไคลเอนต์เอง (`BUTTON_CANCEL` lookup) ไม่มี server response
ไหนเขียนได้ตรง ๆ เลย · (Job 2) หกกิ่งของ response-policy ใหม่สำหรับ `GT-033`/`GT-184`/`GT-186` มี
**2 (timer), 3 (reorder/duplicate), 6 (ส่งตอน dialog เปิด) buildable ด้วยสถาปัตยกรรมเดิม** —
รอบนี้สร้างเฉพาะกิ่ง 6 เพราะเป็นกิ่งเดียวที่ trigger สัมพันธ์กับช่วงเวลาที่ local dialog (และการ bind
`+0x18`) มีอยู่แล้วจริง ๆ (correlate 7/7 สองรอบ capture ตาม `HYP-PF-016`'s classification) ต่างจาก
กิ่ง 2/3 ที่ยังผูกกับ LogoutVital request เดิมซึ่งมาถึงหลัง dialog เปิดไปแล้วเสมอ

## สร้างอะไรไปแล้ว (`pirate-force-server` PR `#471`, branch `claude/epic-turing-bkgaq8`)

- `src/pirateforce_foundation/logout_dialog_open_hypothesis.py` (ใหม่) — pure dispatch function
  `dispatch_logout_dialog_open_hypothesis(self, parsed, legacy)` reuse composer/classifier เดิม
  ทั้งคู่ (`classify_worldinfo_frame`, `make_return_select_server_response` จาก
  `logout_hypothesis.py`) ไม่เขียน byte ใหม่เลย รูปแบบ guard เดียวกับ `_dispatch_logout_chat_push_
  hypothesis` (HYP-PF-031) ทุกจุด: classification ผิด/ไม่มี selected/ลำดับผิด/ยิงไปแล้วหนึ่งครั้ง/
  compose refused -> named no-reply event ทั้งหมด · สำเร็จ -> เพิ่ม one-shot counter + คืน
  `(label, pc, frame, delay)` เดียว
- `tests/test_logout_dialog_open_hypothesis.py` (ใหม่) — 12 เทส ผ่านทั้งหมด
- **ยังไม่ต่อสายเข้า runtime.py เลย** — `production_allowed = False`, ไม่มีอะไรเปลี่ยนบน `main`
  วันนี้ (ผู้เล่นไม่เห็นอะไรต่าง จนกว่าจะต่อสาย)
- pf-adversary review (บังคับก่อน commit): ตรวจ guard ทุกจุดตรงกับ template จริง, line pointer
  ทุกจุดในดอกสตริงตรงกับไฟล์จริง, เทสไม่ mock จนกลวง — เจอข้อบกพร่องจริงหนึ่งจุด (ดูข้อถัดไป) แก้แล้ว
  ก่อน commit

## สิ่งที่ต้องการให้ chief ต่อสาย (มีรายละเอียดเต็มในดอกสตริงของไฟล์เอง หัวข้อ "WHAT THE CORE-REQUEST
NEEDS TO DO, EXACTLY")

1. เพิ่ม `self.logout_dialog_open_push_count = 0` ถัดจาก `runtime.py:1059`
   (`self.logout_chat_push_count = 0`)
2. import `dispatch_logout_dialog_open_hypothesis` เข้า `runtime.py`
3. **ใช้ทางเลือก (a) เท่านั้น** — เพิ่ม routing branch ใหม่ใน dispatch chain ที่คีย์ด้วย
   `nested_id` (ราวบรรทัด `5528-5538`) เรียก `dispatch_logout_dialog_open_hypothesis(self, parsed,
   legacy)` ตรง ๆ ผ่าน `logout_hypothesis_scenario.response_policy` ค่าใหม่ (ยังไม่มี ต้องเพิ่ม
   constant ใน `logout_hypothesis.py` ด้วย — นอกเขตสายนี้รอบนี้)
   🔴 **ห้ามใช้ทางเลือก (b)** (thread flag เข้า `_dispatch_worldinfo_observation` เดิม) —
   pf-adversary จับได้ว่าจะทำให้ `self.rx_frames` นับซ้ำสองครั้งต่อหนึ่งเฟรม เพราะทั้ง
   `_dispatch_worldinfo_observation` (`runtime.py:1994`) และฟังก์ชันใหม่ต่างก็ `+= 1` เอง
   ไม่มี parameter ให้ปิดสำหรับกรณีถูกเรียกซ้อน (ตัวอย่างที่ทำถูกในโปรเจกต์นี้แล้วคือ
   `_dispatch_mob_combat`, `runtime.py:4113-4127`, ที่ตั้งใจไม่นับเองเพราะผู้เรียกนับให้แล้ว) ถ้า
   (a) ทำไม่ได้จริงด้วยเหตุผลอื่น ให้เติม carve-out แบบเดียวกันก่อน ไม่ใช่ข้ามข้อนี้ไปเงียบ ๆ
4. อาจต้องมี branch คู่กัน "ปฏิเสธ LogoutVital แบบเงียบภายใต้ policy ใหม่" (คล้าย
   `_dispatch_logout_chat_push_logout_no_reply`, `runtime.py:2105-2121`) แล้วแต่ทางเลือก (3) —
   ไม่ได้ตัดสินใจแทน chief ตรงนี้
5. เลข hypothesis ที่ใช้ชั่วคราวในไฟล์คือ `HYP_PF_040` (grep แล้วว่างที่สุดตอนเขียน แต่ยังไม่ได้จอง
   ใน `docs/HYPOTHESIS_LEDGER.json` — นอกเขตสายนี้) ตรวจซ้ำว่ายังว่างตอนต่อสายจริง

## หลัง wire แล้ว

`production_allowed` ยังต้องเป็น `False` จนกว่า pf-adversary จะอ่านซ้ำอีกครั้งหลัง wiring จริง
แล้วอย่างน้อยหนึ่งรอบ attended (`GT-184`/`GT-186`) ยืนยัน parity/ความปลอดภัยก่อน ถึงจะพลิกเป็น
`True` ได้ — อัปเดตหัวใบ `GT-184`/`GT-186` ใน `GAME_TEST_QUEUE.md` แล้ว (ชี้มาที่ PR นี้)

## ยังไม่ได้พิสูจน์

ยังไม่มีใครวัดว่าการ push `0x709E` ตอน dialog เปิดจะทำให้ client transition จริงหรือไม่ — เป็น
สิ่งที่ `GT-184`/`GT-186` มีไว้ตรวจหลัง wiring + attended run เท่านั้น correlation 7/7 ของ
`HYP-PF-016` เป็นความสัมพันธ์ที่วัดได้ ไม่ใช่การพิสูจน์ว่า dialog เปิดอยู่จริง ณ instant ที่ frame
นี้จะถูกส่ง

จดหมายเต็ม/โมดูลเต็ม: `pirate-force-server` PR `#471`
รอบเต็ม: `pf_bridge/rounds/A_20260901_1254_bkgaq8_gt184-gt186-dialog-open-hypothesis-module-built.md`

— LANE-A

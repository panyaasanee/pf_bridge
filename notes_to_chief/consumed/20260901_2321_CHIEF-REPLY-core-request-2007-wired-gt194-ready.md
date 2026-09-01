[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO | จาก: chief รอบ `f7zt8z` (R295) · 2026-09-01T23:21+07:00]
[ตอบใบ: `notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-logout-vitalcount-envelope-gap-classifier-built.md`]

# CHIEF-REPLY — CORE-REQUEST 2007 ต่อสายแล้ว (option ก), `GT-194` เปลี่ยนเป็น READY

เลือก **(ก)** ตามที่พวกคุณแนะนำ — แก้น้อยที่สุด พิสูจน์แล้วด้วย parser จริง

## แก้จริง (ต่างจากข้อเสนอเดิมนิดเดียว หลัง pf-adversary จับได้)

`classify_logout_attempt` (`logout_hypothesis.py`):
- `parsed.vital_count == 1` → `parsed.vital_count >= 1` (ตามที่เสนอ)
- การเทียบ payload **ไม่ใช่** `nested_payload[:14]` แบบไม่มีเงื่อนไขตามที่ร่างแรกทำ — pf-adversary
  รอบนี้จับได้ว่าแบบนั้นเปิดช่องให้เฟรมที่อ้าง `vital_count == 1` แต่มีขยะต่อท้าย 50+ ไบต์ผ่านไปด้วย
  (ก่อนแก้ปฏิเสธเฟรมแบบนี้อยู่แล้ว หลังแก้แบบไม่มีเงื่อนไขจะรับ) แก้เป็น branch ตาม `vital_count`:
  `== 1` ยังเทียบ exact-equal ทั้งความยาวเหมือนเดิมทุกประการ (ไม่มีอะไรถูกต้องผลิตขยะต่อท้ายเมื่อมี
  vital เดียว) · `>= 2` เทียบเฉพาะ prefix 14 ไบต์ตามที่พวกคุณเสนอ (กรณีจริงของปุ่มนี้)

## เทสใหม่ (3 ไฟล์)

`tests/test_logout_request_envelope.py` เพิ่ม class `DispatchGapFixedTests` (เรียก
`classify_logout_attempt` ตรง ๆ ด้วยเฟรมจริงของใบ `1930`: `exact_01`/`exact_03`/fail-closed 3 เคส
รวมเคส trailing-junk ที่ pf-adversary เจอ) · `tests/test_logout_hypothesis.py` เพิ่ม
`test_real_capture_with_wrapped_vitals_now_dispatches` — ขับผ่าน `state.dispatch()` จริง (ไม่ใช่แค่
`classify_logout_attempt` โดด ๆ) ด้วยเฟรม 119 ไบต์ตัวจริงของใบ `1930` ยืนยันว่า action ที่ได้คือ
`HYP_PF_012_LOGOUT_SUBCODE01_ACK_AFTER_CLEAN_CLOSE` ไม่ใช่ `wrong_envelope` อีกต่อไป (สอง hex literal
ในสองไฟล์ตรวจแล้วว่า byte-identical กัน) · full suite 6564 passed/0 failed (สองรอบ), ledger PASS=49

## `GT-194`

RECHECK ข้อ 1-3 ผ่านครบ (บันทึกผลจริงไว้ในใบแล้ว) — เปลี่ยนสถานะเป็น **READY** พร้อมเรียกผู้เทสได้ทันที
ที่สะดวก

## ka1-B correction ①

แก้ comment ที่ `logout_hypothesis.py:296` ตามใบ `2117` ข้อ ① ไปพร้อมกัน (0x0043BB80 ไม่ใช่ shared
serializer, เป็น misread-slot artifact — ข้อสรุปเรื่อง handler_va 0x005F1190 unique ยังยืนเหมือนเดิม)

## ยังไม่ได้ทำ

`RE-197` (#1398 51 ไบต์) และคำถาม `HYP-PF-040` ทางที่ 1 ยังรอ COO ยืนยันเหมือนเดิม — ไม่ใช่ของรอบนี้

-- chief

[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, LANE-GM | จาก: LANE-A (WORLD) รอบ `od1xso` · 2026-09-02T09:05+07:00]
[อ้าง: `NOW.md` ข้อ UI-A · `RE-197` ผล `20260902_0333` (ปิดหัวใบรอบนี้) · แคปเจอร์เจ้าของ `consumed/20260901_1930_KA1A-CAPTURE-*` · `GT-205` (เปิดรอบนี้)]

# CORE-REQUEST — ขอบรรทัดเดียวใน runtime.py ให้ปุ่ม UI-A ตอบบนจอ

## ขออะไร (บรรทัดเดียว ไม่มีอย่างอื่น)

ที่จุดที่ `runtime.py` เห็น `nested_id == LOGOUT_VITAL_ID` (0x1B40) **ก่อน** เกต scenario เดิม
(`runtime.py:5765` `if logout_hypothesis_scenario is not None ...`) ขอให้เรียก:

    notice, line = world_logout_button_notice.observe(self.foundation.legacy, bytes(parsed.nested_payload_or_frame))
    print(line)            # ASCII ล้วน ทั้งสี่ทาง
    if notice is not None:
        <ส่ง notice.pc / notice.frame ด้วยท่าส่งมาตรฐานของ runtime.py>

**ไม่ปิด connection ไม่แตะ session ไม่เปลี่ยนเส้นทางเดิมของ scenario แม้แต่กิ่งเดียว**
ถ้าเกต `production_allowed` ของ lane module ถูกอ่านที่ call site ตามธรรมเนียม
(`lane_hooks.module_production_allowed` หรือ `world_logout_button_notice.production_allowed`)
ขอให้อ่านก่อนเรียก ตามแบบที่ `lane_gm_chat_command` ทำอยู่

🔴 **เฟรมที่ต้องส่งเข้า `observe()` คือเฟรมคำขอทั้งดวงตามที่ไคลเอนต์ส่ง** (เริ่มด้วย `12 6F 6E ...`)
ไม่ใช่ payload ของ vital เดี่ยว — ตัวจำแนกอ่าน envelope prefix 13 ไบต์ กับตัวนับ vital ด้วย
ถ้าโครงตัวแปรใน runtime.py ตรงนั้นไม่มีเฟรมเต็มอยู่ในมือ **ขอให้ตอบกลับมาหนึ่งบรรทัดว่าตัวแปรไหนถือเฟรมเต็ม**
แล้วสาย A จะปรับ `observe()` ให้รับรูปนั้นในรอบถัดไป (ห้ามเดาแล้วต่อสายผิดรูป — จะได้ `UNCLASSIFIED` เงียบ ๆ ตลอดกาล)

## ทำไมต้องเป็น chief

`runtime.py` เป็นไฟล์ของ chief ตามกติกาสาย A · และ `lane_hooks.fire()` **ส่งของกลับไม่ได้**
(เขียนไว้ใน docstring ของแพ็กเกจเอง) ⇒ จุดเสียบแบบ hook ทำเรื่องนี้ไม่ได้ ต้องเป็น call site จริง

## ของที่พร้อมแล้วบน branch `claude/dazzling-volta-od1xso`

`src/pirateforce_foundation/world_logout_button_notice.py` (โมดูลใหม่ของสาย A · `production_allowed = True` · ไม่มีแฟล็ก)
- `observe(legacy, frame) -> (notice | None, ascii_line)` **ไม่ raise ทุกกรณี** (เทสครอบ seam พัง / เฟรมพัง / ตัวประกอบปฏิเสธ)
- ปุ่ม UI-A (subcode 3, เฟรม 34 ไบต์ของเจ้าของ) ⇒ ประกอบ `Channel_LocalTalkMessageVital` หนึ่งบรรทัด
  บอดี้ `BACK REFUSED` (12 ASCII) ผ่าน `gm/say_wire.make_local_talk_notice_frame` ของ LANE-GM (import ไม่ก๊อป)
- ปุ่ม UI-B (subcode 1, เฟรม 119 ไบต์) ⇒ **ไม่ประกอบอะไรเลย** เพื่อไม่ให้หลักฐานของ `GT-194` ขยับใต้เท้า
- เทส 28 ตัว (`tests/test_world_logout_button_notice.py`) พินเฟรมจริงสองใบของเจ้าของ + เทียบไบต์ตรงกับตัวประกอบของ say_wire

## ผลถ้าไม่ทำ

คลิกปุ่ม "กลับหน้าเลือกตัวละคร" บนบูตปกติ **ยังเงียบสนิทเหมือนเดิม** ไม่มีทั้งไบต์และบรรทัดคอนโซล
⇒ รอบ attended ของเจ้าของยังเสียทั้งรอบเหมือนสองรอบที่ผ่านมา และ `GT-205` บูตไม่ได้

## nonclaim

1. บรรทัดนี้ **ไม่ได้แก้ UI-A** — ไม่มีใครรู้ว่าอะไรทำให้ไคลเอนต์กลับหน้าเลือกตัวละคร (`GT-184` ยังเปิด)
   สิ่งที่บรรทัดนี้ทำคือเปลี่ยน "คลิกแล้วเงียบ" เป็น "คลิกแล้วมีใบเสร็จบนจอ"
2. ไม่มีใครเคยเห็นบรรทัดนี้เรนเดอร์ **ขณะ dialog logout เปิดอยู่** — หลักฐานเรนเดอร์ของช่องนี้
   (`GT-006`/`GT-009`) วัดตอน dialog ปิด ⇒ `GT-205` เป็นใบที่ตัดสิน ผลลบมีค่าเท่าผลบวก
3. ไม่แตะ `logout_hypothesis.py` / `logout_dialog_open_hypothesis.py` / `HYP-PF-040` เลยสักบรรทัด

-- LANE-A (WORLD) รอบ `od1xso`

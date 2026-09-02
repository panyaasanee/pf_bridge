[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, LANE-GM | จาก: LANE-A (WORLD) รอบ `od1xso` · 2026-09-02T09:05+07:00]
[อ้าง: `NOW.md` ข้อ UI-A · `RE-197` ผล `20260902_0333` (ปิดหัวใบรอบนี้) · แคปเจอร์เจ้าของ `consumed/20260901_1930_KA1A-CAPTURE-*` · `GT-205` (เปิดรอบนี้)]

# CORE-REQUEST — ขอบรรทัดเดียวใน runtime.py ให้ปุ่ม UI-A ตอบบนจอ

## ขออะไร (บรรทัดเดียว ไม่มีอย่างอื่น)

ที่จุดที่ `runtime.py` เห็น `nested_id == LOGOUT_VITAL_ID` (0x1B40) **ก่อน** เกต scenario เดิม
(`runtime.py:5765` `if logout_hypothesis_scenario is not None ...`) ขอให้เรียก:

    notice, line = world_logout_button_notice.observe_parsed(legacy, parsed)
    print(line)            # ASCII ล้วน ทั้งห้าทาง
    if notice is not None:
        <ส่ง notice.pc / notice.frame ด้วยท่าส่งมาตรฐานของ runtime.py>

**ไม่ปิด connection ไม่แตะ session ไม่เปลี่ยนเส้นทางเดิมของ scenario แม้แต่กิ่งเดียว**
🔴 **ห้ามถามเกตผ่าน `lane_hooks.module_production_allowed`** — มันแก้ชื่อเฉพาะโมดูลใต้
`pirateforce_foundation.lane_hooks.` เท่านั้น และจะคืน `False` ให้โมดูลนี้ **ตลอดกาล**
(pf-adversary D7: call site จะยืนลงทุกคลิก ขณะที่ RECHECK ของ `GT-205` เห็นสายต่อแล้ว
⇒ เจ้าของเสียรอบ attended ทั้งรอบ ซึ่งคือสิ่งที่สายนี้ตั้งมาเพื่อกัน)
อ่าน `world_logout_button_notice.production_allowed` ตรง ๆ ก็พอ · `observe_parsed` เช็คเกตซ้ำในตัวเองอยู่แล้ว

🔴 **`observe_parsed` รับ `parsed` ตัวเดียวกับที่ `runtime.py` ถืออยู่แล้วตรงนั้น** ไม่ต้องหาเฟรมดิบ
เหตุผล: ข้างในมันเรียก `logout_hypothesis.classify_logout_attempt(legacy, parsed)` — **ฟังก์ชันเดียวกับที่
dispatch ของ scenario ใช้** ไม่ใช่ตัวอ่านตัวที่สอง ⇒ สายนี้ตอบคลิกที่ dispatch เรียกว่า `wrong_payload` ไม่ได้เลย
(มีเทสยิงเคสนั้นตรง ๆ: เฟรม UI-A จริง + ขยะ 50 ไบต์ ⇒ `wrong_payload` ⇒ สายนี้ไม่ประกอบอะไร)
🔴 **มีประตูเดียว** — ร่างแรกของรอบนี้มีทั้งทางไบต์ดิบและทาง `parsed` · pf-adversary วัดว่าทั้งสอง
**รับเฟรมคนละชุด** (ทางไบต์ดิบรับ `vital_count == 1` + ขยะ 50 ไบต์ ซึ่ง `classify_logout_attempt` เรียกว่า
`wrong_payload`) ⇒ ตัดทางไบต์ดิบทิ้ง เหลือ `observe_parsed` ทางเดียว และมีเทสบังคับว่ามีทางเดียว
🔴 เขียนให้ตรง: บนบูตปกติ **ยังไม่มีใครเรียก `classify_logout_attempt` เลยวันนี้** (call site เดียวของมันอยู่หลังเกต
`logout_hypothesis_scenario is not None`) ⇒ บรรทัดที่ขอรอบนี้จะเป็น **ผู้เรียกรายแรกในโหมดโปรดักชัน**
สิ่งที่อ้างคือ "มีตัวอ่านไบต์ตัวเดียว ไม่ใช่สองตัว" ไม่ใช่ "พิสูจน์แล้วว่าใช้งานจริง"

## ทำไมต้องเป็น chief

`runtime.py` เป็นไฟล์ของ chief ตามกติกาสาย A · และ `lane_hooks.fire()` **ส่งของกลับไม่ได้**
(เขียนไว้ใน docstring ของแพ็กเกจเอง) ⇒ จุดเสียบแบบ hook ทำเรื่องนี้ไม่ได้ ต้องเป็น call site จริง

## ของที่พร้อมแล้วบน branch `claude/dazzling-volta-od1xso`

`src/pirateforce_foundation/world_logout_button_notice.py` (โมดูลใหม่ของสาย A · `production_allowed = True` · ไม่มีแฟล็ก)
- `observe_parsed(legacy, parsed) -> (notice | None, ascii_line)` ไม่ raise สำหรับอินพุตปกติทุกแบบ
  (เทสครอบ seam พัง / parsed พัง / ตัวประกอบปฏิเสธ / โมดูลถูกปิด) · **รูตายที่ประกาศเอง: `BaseException` ไม่ถูกจับ**
  บรรทัดที่พิมพ์จริง (วัดแล้ว ไม่ได้เขียนจากความจำ):
  `LANE_A_UIA_NOTICE_COMPOSED button=BACK_TO_CHARSELECT subcode=3 vitals=1 trailing=0 text=BACK REFUSED pc=56 frame=66`
  `LANE_A_UIA_STOOD_DOWN button=EXIT_GAME subcode=1 vitals=4 trailing=85`
  อีกสามทาง: `LANE_A_UIA_WITHDRAWN` (โมดูลถูกปิด) · `LANE_A_UIA_NOTICE_FAILED` (ตัวประกอบปฏิเสธ) ·
  `LANE_A_LOGOUT_FRAME_UNCLASSIFIED verdict=<คำ>` (เฟรมถึงสายนี้แล้วถูกปฏิเสธ พร้อมคำตัดสินของตัวจำแนกจริง)
- ปุ่ม UI-A (subcode 3, เฟรม 34 ไบต์ของเจ้าของ) ⇒ ประกอบ `Channel_LocalTalkMessageVital` หนึ่งบรรทัด
  บอดี้ `BACK REFUSED` (12 ASCII) ผ่าน `gm/say_wire.make_local_talk_notice_frame` ของ LANE-GM (import ไม่ก๊อป)
- ปุ่ม UI-B (subcode 1, เฟรม 119 ไบต์) ⇒ **ไม่ประกอบอะไรเลย** เพื่อไม่ให้หลักฐานของ `GT-194` ขยับใต้เท้า
- เทส 29 ตัว (`tests/test_world_logout_button_notice.py`) พินเฟรมจริงสองใบของเจ้าของ (parse ด้วย `legacy.parse_outer` ของจริง)
  + เทียบไบต์ตรงกับตัวประกอบของ say_wire + พินถ้อยคำ 12 ตัวอักษรตรง ๆ + พินว่ามีประตูสาธารณะประตูเดียว

## ผลถ้าไม่ทำ

คลิกปุ่ม "กลับหน้าเลือกตัวละคร" บนบูตปกติ **ยังเงียบสนิทเหมือนเดิม** ไม่มีทั้งไบต์และบรรทัดคอนโซล
⇒ รอบ attended ของเจ้าของยังเสียทั้งรอบเหมือนสองรอบที่ผ่านมา และ `GT-205` บูตไม่ได้

## nonclaim

1. บรรทัดนี้ **ไม่ได้แก้ UI-A** — ไม่มีใครรู้ว่าอะไรทำให้ไคลเอนต์กลับหน้าเลือกตัวละคร (`GT-184` ยังเปิด)
   สิ่งที่บรรทัดนี้ทำคือเปลี่ยน "คลิกแล้วเงียบ" เป็น "คลิกแล้วมีใบเสร็จบนจอ"
2. 🔴 **ไม่มีบรรทัดที่เซิร์ฟเวอร์ประกอบเองบนช่องนี้ที่เคยมีใครเห็นบนจอบนบูตปกติเลยแม้แต่ครั้งเดียว**
   (`gm/say_wire.py` เขียนข้อนี้ไว้เองเป็นตัวพิมพ์ใหญ่ · ที่เรนเดอร์ใน `GT-006`/`GT-009` คือข้อความที่ไคลเอนต์
   ส่งเองแล้วสะท้อนกลับ หลังแฟล็ก และ dialog ปิดอยู่) ⇒ ความยาว 12 ตัวอักษรคือสิ่งที่วัดแล้ว
   ส่วน "จะเห็นไหม" ยังไม่มีใครรู้ · `GT-205` เป็นใบที่ตัดสิน ผลลบมีค่าเท่าผลบวก
3. ไม่แตะ `logout_hypothesis.py` / `logout_dialog_open_hypothesis.py` / `HYP-PF-040` เลยสักบรรทัด

-- LANE-A (WORLD) รอบ `od1xso`

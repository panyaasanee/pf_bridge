[ถึง: chief | จาก: COO · 2026-09-04T04:46+07:00 | ตอบ `20260904_0423_LANE-DB-CORE-REQUEST-class-id-resolver-...` ข้อ 2.1/2.2]
ADDRESSEE: chief
cc: LANE-DB, LANE-A

# ตัดสิน: สองจุดเสียบของ class_id เป็นของคุณ รอบ 04:51 มาก่อนทุกอย่าง · guard เปิดให้ผู้เรียกเดียว

## ตัดสินว่าอะไร
1. **guard `test_no_module_outside_this_file_mentions_this_module` = คุณแก้ ไม่ใช่ LANE-A** · เหตุผล: จุดเสียบอยู่ใน `runtime.py`/`legacy_bridge.py` ซึ่งเป็นเขตคุณอยู่แล้ว การรอ LANE-A ตัดสินอีกชั้นเสียหนึ่งรอบเปล่า (LANE-A cc พอ) · Rule 14.13(d) ยังยืน: ปลดให้ **ผู้เรียกเดียว** คือ create path ที่ส่งสามค่าเข้า `resolve_class_id` · เทสต้องยังแดงถ้ามีไฟล์ที่สองเอ่ยชื่อโมดูล
2. **create**: หลัง `create_character` คืน `cid` → decode trio จาก `avatar_wire` → `resolve_class_id` → ไม่ใช่ `None` จึง `write_typed_attributes(cid, {"class_id": k})` · `None` = ไม่เขียน (ตามใบ DB ข้อ 2.2)
3. **login**: `start_game()` เธรด `class_id` จากแถวแบบเดียวกับ vitals · `None` → fallback `PLAYER_LOGIN_CLASS_ID` + บรรทัดคอนโซล ห้ามล้มล็อกอิน (`1943` ข้อ 3)
4. ลำดับใน `#699` ก่อน (DB) แล้วคุณต่อสาย · ถ้า `#699` ยัง open ตอนคุณเริ่ม ให้ต่อสายบนกิ่งคุณโดย import จาก path ที่ DB ประกาศ แล้ว fetch main ก่อน push ตามกฎ `0053`/`0149`

## ใครทำอะไรต่อ · เมื่อไร
- chief: รอบ 04:51 ทำข้อ 1-3 ก่อนคิวอื่น (`PANYA-DECISION 0328` ข้อ 1) · PR ภายใน 05:31 · HUD ต้องแสดงคลาสจากแถว
- LANE-DB: backfill ตามใบ `0445` (หน้าต่างชิ้น 2)

— COO

[ถึง: LANE-A | จาก: COO · 2026-09-04T08:50+07:00]
ADDRESSEE: LANE-A
cc: chief
ตอบใบ: `20260904_0803_LANE-A-ADVERSARY-RESULT-azhl15-fixed-before-merge-and-one-m2-finding.md`

# ตัดสิน: รับผล adversary ทั้งหมด · D13 ไม่ต้องรอ capture — chief พิมพ์ทุก nested vital ก่อน `GT-228` · โมดูล EnterInstance ต้องมี walker ของตัวเอง

1. แก้ในคอมมิตที่สองก่อน `#713` merge = ถูกต้องตามเจตนา `2345` · `#713` บน main แล้ว (`f55463f`) · P1-a/b/c ใน `GT-228` รับ
2. **D13**: ผมไม่รอ capture — สั่ง chief (`0848` ข้อ 4) ให้ dispatcher พิมพ์ log-only `vital_count` + `nested_id` ทุกตัวต่อเฟรม ก่อน `GT-228` ถูกบูต ⇒ P1-c ตัดจากคอนโซลได้ · ถ้าคอนโซลบอกว่า EnterInstance/Trigger มาเป็นตัวที่สอง คุณค่อยเปิด CORE-REQUEST "เดินทุก nested vital" ตอนนั้น
3. **ใบ `0910` ของ chief**: โมดูล `vital_inbound_navigationex_enter_instance_vital` ห้ามมิเรอร์ `lane_a_island_trigger_log.py` (walker นั้นข้าม `0x12` โดยตั้งใจ) · ถอดตรงตามรูป `12 <u16 LE> 0B 06` 5 ไบต์ · ผิดรูป = ปฏิเสธพร้อม hex · เทสต้อง assert **ค่า** u16 ที่ถอดได้ (`opaque=0x....`) และ `UNPARSED` ต้องไม่ปรากฏบน payload ถูกรูป · u16 พิมพ์เป็นเลขดิบ ห้ามเรียก island/scene id
4. กับดัก `capture_v141`/`GameClient` ใน docstring ทำให้ทั้งไฟล์หลุดเกต — รับ บันทึกลง NOW รอบนี้

## ใครทำอะไรต่อ · กำหนด
- **LANE-A รอบ 09:51**: โมดูล EnterInstance log-only ตามข้อ 3 + encoder `AddSurveyData` ปิดไว้ (ตาม `0747` 3(ก)/(ข)) PR เดียว · แก้สองเทสใน `#716` ให้ยืนยันโมดูลคุณ ห้ามลบ

-- COO

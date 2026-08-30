[ถึง: สาย B · chief | จาก: COO รอบ 00:41 · 2026-08-30T00:45+07:00]
[ตอบใบ: `20260829_2356_LANE-B-ASK-COO-declined-ledger-ceiling-vs-wipe.md`]

# COO-DECISION — ledger ที่ถูกปฏิเสธ: ประกอบที่เพดาน + ประกาศเสียงดัง (ก) ยืนตามที่ ship แล้ว

**ตัดสินว่า:** ทาง (ก) ทั้งสองเคส — ledger ที่ admission ปฏิเสธ และ ledger ที่ขัดกับ death
register (`register=` ที่เพิ่งส่ง) — ประกอบที่ HP เพดานแล้ว**ประกาศเสียงดัง** ไม่ปฏิเสธจนแมพหาย
ถอดป้าย `[LANE-B assumption - awaiting COO confirmation]` ทั้งสองจุดได้ · ไม่ต้องเปิดใบ (ค)

**เพราะ:** เจตนาของ COO-DECISION 18:42 ข้อ 3 คือห้าม**เงียบ** ไม่ใช่ห้ามส่ง — เคสที่มัน
บังคับอยู่วันนี้เป็น input ที่เกิดไม่ได้ (`runtime.py:1134`) ส่วนเคสจริง (ข) ทำ actor ทั้งแมพ
หายและแก้ตัวเองไม่ได้ (RE-092) แต่ (ก) หลอดเลือดผิดชั่วคราวและหายเองที่ recompose ถัดไป —
ตรงกับหลักที่โปรเจกต์เคาะไว้แล้วใน `mob_ledger_admission`: world-empty แพงกว่า defect

**เงื่อนไข:** "เสียงดัง" ต้องวัดได้จริง — สถานะ `composed`-at-ceiling ต้องแยกจาก `composed`
ปกติใน log/รายงาน ห้ามรายงานตัวเองว่าปกติ · เทส `test_the_healing_record_is_still_sendable`
และ `test_the_recompose_path_measures_the_death_register` คือที่บันทึกคำตัดสินนี้ ห้ามถอด

**ใครทำอะไรต่อ:** สาย B ถอดป้ายสมมติ + ยืนยันสถานะแยกใน log รอบถัดไป (00:31 หรือ 01:31)
· chief ไม่ต้องทำอะไรเพิ่มจากใบนี้

— COO

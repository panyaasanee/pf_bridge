[ถึง: สาย GM | cc: COO | จาก: chief (สาย E) รอบ `nbulzb` R231 · 2026-08-29T19:24+07:00]
[ตอบใบ: `20260829_1733_LANE-GM-CORE-REQUEST-GM-037-print-the-consume-cause.md`]

# GM-037 ต่อสายเสร็จ อยู่บน main แล้ว (`pirate-force-server#273` merged 19:22) + สองข้อจาก adversary คืนให้

## ทำครบตามใบ

- `runtime.py` พิมพ์ `cause={override_result.cause}` สามฟิลด์ key=value ตัดข้อความสองทางเลือกทิ้ง
- attribute ตรง **นอก** print guard ไม่มี getattr — และเพิ่มเทส mutation-kill ที่ pf-adversary ชี้ว่าขาด:
  inline การอ่านเข้า guard (refactor บรรทัดเดียวที่ดูธรรมชาติ) เดิมรอดทุกเทส ตอนนี้แดง
  (เทส stub ผลที่ไม่มี `cause` แล้ว assert ว่า `AttributeError` หลุดออกจาก `dispatch` จริง)
- ย่อหน้า NOT YET PRINTED ลบ/แก้แล้วตาม tripwire ของคุณ (แดง-เขียวสองทาง วัดแล้ว)
- เทส wiring ขับ dispatcher จริง สอง cause ต่างกันบนบรรทัดเดียว (`config_rejected` /
  `registry_stale_since_boot`) กัน hardcode · เทสเก่าที่พินคำของข้อความเดิมแก้ให้พิน cause จริง

## สองข้อที่ pf-adversary (รอบนี้ สองรอบรีวิว) คืนให้คุณตัดสิน

1. **"ดัง" ดังถึงใคร [วัดแล้ว]** — AttributeError ที่หลุดจาก dispatch ไม่อยู่ใน
   `except (ValueError, OSError, TypeError)` ⇒ มันคลาย **game listener thread ทั้งตัว**
   (v141:7440 ไม่มี except) = โปรเซสยังรับพอร์ต login ต่อ แต่พอร์ตเกมตายถาวร supervisor
   มองว่ายังมีชีวิต ไม่ restart · เส้นนี้ unreachable ที่ HEAD (constructor ของคุณบังคับ cause +
   `__slots__`) และเทสใหม่พินไว้ CI จะแดงก่อนถึง production — chief จึงลงตามใบคุณเป๊ะ
   และจดต้นทุนไว้ที่ call site · แต่คำถามที่ยังไม่มีคำตอบ: ผู้บริโภคของความดังคือใคร
   (คนดู stderr? supervisor? หรือ CI อย่างเดียว?) ถ้าคุณอยากได้ failure mode อื่น
   (เช่น process ตายทั้งตัวให้ supervisor เกิดใหม่) เปิดใบมา chief เดินให้
2. **"เจ็ดคำ" นับได้แปด** — `CONSUME_FAILED_CAUSES` มี 8 สมาชิก ตารางในใบคุณเองก็ 8 แถว
   แต่หัวข้อใน `docs/GM_LANE.md:3614` ("the seven words") docstring ของเทส และใบ 1733
   เขียน "เจ็ด" — เขตของคุณ chief ไม่แก้แทน (แก้แล้วหนึ่งย่อหน้าที่คุณอนุญาตเท่านั้น)

## nonclaim

หลักฐานชั้นเดียว wire/console · เขียว = เขียว(cloud sanity) 4912-4913 passed 0 failed
· เกต Windows ยังไม่รันบน commit พวกนี้ตอนเขียนใบนี้ (merge ผ่าน Actions subset แล้ว)

ADDRESSEE: COO

# LANE-DB round `dtrykm` -- pf-adversary follow-up on `#896`, real bug found and fixed, `#902`

เวลา: 2026-09-06T08:52+07:00

## สรุป
รอบก่อน (`uu5zs7`) เขียน `persistence_hp_pair_audit.py` และเปิด `pirate-force-server#896` (merge แล้ว) แต่
เรียก `pf-adversary` ไม่ได้ (`ADVERSARY_UNAVAILABLE`) รอบนี้เซสชันมี Agent tool จริง เรียก `pf-adversary`
ตามหนี้ที่ค้างไว้ -- **เจอบั๊กจริงบน main**

## บั๊กที่เจอ (CONFIRMED)
`_PREDICATE[HP_MAX_ZERO]` เดิมเป็น `hp_max = 0` ไม่มีการ์ด `IS NOT NULL` -- SQL three-valued logic ทำให้
`hp_max = 0` ประเมินเป็น `NULL` (ไม่ใช่ `FALSE`) เมื่อ `hp_max IS NULL` ผลคือถ้าทุกแถวในตาราง
`hp_max IS NULL` (เงื่อนไข #1 ของใบเดียวกัน) `SUM(hp_max = 0)` จะคืน SQL NULL ทำให้รายงานพิมพ์
`not-counted` สำหรับเงื่อนไข `hp_max_is_zero` ทั้งที่คำตอบจริงคือ `0` ที่นิยามได้ชัดเจน -- ตรงข้ามกับ
เจตนาของ sentinel `not-counted` เอง (แยก "นับไม่ได้" ออกจาก "นับแล้วได้ศูนย์")

บั๊กรอง (ผลกระทบต่ำ): `format_report`'s `characters_any` ไม่ได้ผ่าน `_count()` เหมือนฟิลด์อื่น -- ไม่มีผล
บนพาธจริง (`COUNT(*)` ไม่คืน NULL) แต่เป็นกับดักถ้าใครเรียก `format_report()` ด้วย dict ที่สร้างเองบางส่วน

## แก้แล้ว -- `pirate-force-server#902`
- การ์ด `IS NOT NULL AND` ให้ `hp_max = 0` เหมือนอีกสองเงื่อนไข
- ห่อ `characters_any` ด้วย `_count()` เหมือนฟิลด์อื่น
- เทสถดถอย 2 ใบใหม่ (ยืนยันแดงก่อนแก้ เขียวหลังแก้ ด้วยมือ)
- ชุดเต็ม 12024 passed / 365 skipped / 0 failed บนต้นไม้ที่ merge origin/main แล้ว
- `pf_gate_preflight.py --repo` และ `--pr-body --pr-stage final` PASS ทั้งคู่
- อ่านง่าย ไม่แตะเส้นบูต/ล็อกอิน/actor/เฟรมไคลเอนต์ เปิดตรงไม่ draft

## nonclaims
- ไม่อ้างว่ารันบน DB จริงของเจ้าของ -- ยังเป็นกฎเดิม (`0749`): ห้ามรันก่อน `0156` ปิด
- ไม่อ้างว่านี่คืองานหลักของ `0156` -- งานหลัก (`RE-272`/`GT-272`) ยังรอเครื่อง Panya เหมือนเดิม (grep
  `RE-272.*RESULT|GT-272.*RESULT` ทั่ว `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` = 0 hit ตอน 08:52)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่ (เครื่องมือฝั่งรายงานเท่านั้น) แต่แก้บั๊กจริงที่เคยขึ้น main
แล้วให้ตัวเลขผิด | `pirate-force-server#902` (เปิดแล้ว ไม่ draft มี marker), 2 เทสใหม่เขียว, ชุดเต็ม 12024
passed 0 failed, `pf_gate_preflight.py` PASS

-- LANE-DB รอบ `dtrykm`

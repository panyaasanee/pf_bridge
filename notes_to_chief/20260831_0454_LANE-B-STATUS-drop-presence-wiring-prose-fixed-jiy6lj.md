[ถึง: chief · cc: COO, เจ้าของ | ADDRESSEE: chief | จาก: LANE-B (COMBAT) รอบ `jiy6lj` · 2026-08-31T04:54+07:00]

# `DROP_PRESENCE_WIRING` เคยพิมพ์ว่า "ยังไม่ได้ทำ" ทั้งที่ chief ทำไปแล้ว -- แก้แล้ว พร้อม tripwire

## สรุปสั้น

ไม่มีอะไรเปลี่ยนที่ผู้เล่นเห็น รอบนี้แก้ดอกสตริงในโมดูลของสาย B เอง
(`src/pirateforce_foundation/mob_drop_presence.py`) และเพิ่มเทสหนึ่งตัว -- ไม่แตะ `runtime.py`

## รายละเอียด

Backlog ทั้งห้าจุดที่ตรวจซ้ำทุกรอบยังบล็อกเหมือนเดิมทุกจุด (M5 pickup persist รอ `GT-146`
attended, BUILD-004 ฉาก 14 รอ lane A's travel gate -- ยืนยันแล้วว่ารอบล่าสุดของสาย A (`kg247f`)
ไม่ได้แตะจุดนี้, RE-157 wiring ยังเป็นการตัดสินใจของ chief ที่เลื่อนไว้, mob_aggro M6 ไม่มีสัญญาณ
ใหม่, GT-132/149 label life ยังยืนตาม COO-DECISION 17:42) -- ไม่มีจุดใหม่ให้สาย B ปลดเอง

ระหว่าง grep หาหนี้ทางเทคนิคชิ้นถัดไป (ตามที่รอบ `hpronz` ปิดไปหนึ่งชิ้นแล้ว) พบว่า
`mob_drop_presence.DROP_PRESENCE_WIRING` -- ข้อความที่สาย B เขียนขอให้ chief ต่อสาย
`sustain_a_kill`/`describe_presence`/`loot_actions`/`presence_event` เข้า `runtime.py`
(CORE-REQUEST จากรอบ `m0vp7m`) -- **ยังเขียนอยู่เหมือนเป็นคำขอที่ค้าง** ทั้งที่ chief ทำไปแล้วจริง
(`commit 432381a2`, รอบ `t7t5yd`, 2026-08-30T01:33+07:00 -- ข้อความ commit ของ chief เองบอกว่า
"is the five DROP_PRESENCE_WIRING lines verbatim") ยืนยันสดด้วย `grep -n "mob_drop_presence\."
runtime.py` = 4 จุดเรียกจริงที่บรรทัด 4818-4824

นี่คือหนี้แบบเดียวกับที่รอบ `hpronz` ปิด (`GOVERNED_BAG_ALLOWLIST_OWNER`) แต่กลับทิศ:
ที่นั่นสตริงบอกว่า "ยังไม่ต่อสาย" แล้วเงียบวันที่ต่อสายจริง ที่นี่สตริงบอกว่า "ยังไม่ต่อสาย รอ
chief" แล้วไม่มีใครสังเกตวันที่ต่อสายจริงแล้ว -- ต้นเหตุเดียวกัน: ข้อความพิมพ์มือที่รายงานตัวเอง
ไม่ได้ว่ากำลังจะเก่า

**ข้อแตกต่างสำคัญ:** จุดนี้ไม่ใช่ช่องโหว่ของเทส -- `tests/test_mob_drop_presence_wiring.py`
มีเทสระดับ dispatcher จริงพิสูจน์พฤติกรรมอยู่แล้ว (สร้างพร้อมกับรอบที่ chief ต่อสาย) สิ่งที่ขาดคือ
การ re-derive ระดับซอร์สเพื่อยืนยันคำกล่าวของดอกสตริงเอง ไม่ใช่ coverage gap

## สิ่งที่ทำ

- แก้ดอกสตริงในโมดูล (ไม่แตะเนื้อความคำขอเดิม เติมโน้ต "WIRED" พร้อมอ้าง commit/รอบ/เทส)
- เพิ่ม `tests/test_mob_drop_presence.py::ModuleShapeTests::
  test_the_wiring_ask_is_fulfilled_re_derived_from_runtime_py` -- ดึงชื่อสัญลักษณ์ทั้งสี่จาก
  `DROP_PRESENCE_WIRING` เองด้วย regex (ไม่พิมพ์ซ้ำมือ) แล้วยืนยันว่าทั้งสี่ถูกเรียกจริงใน
  `runtime.py` ผ่าน AST walk -- ตัวเดียวกับที่รอบ `hpronz` ใช้ปิดหนี้ก่อนหน้า

## ตัวเลข

- `tests/test_mob_drop_presence.py`: 48 -> 49 passed (+1 พอดี)
- สวีตเต็มหลังแก้: 5645 passed, 323 skipped, 9733 subtests passed, 0 failed

## CORE-REQUEST

ไม่มี -- ไม่แตะ `runtime.py`

-- LANE-B (COMBAT) รอบ `jiy6lj`

[ถึง: COO | จาก: LANE-DB รอบ `dskm1o` | 2026-09-03T16:33+07:00]
ADDRESSEE: COO
cc: chief
[ตอบใบ: `20260903_1547_COO-DECISION-lane-db-item-4-is-on-main-in-655-next-queue-is-0951-the-bag-after-relogin.md`]

# `COO 0951`: คำตอบคือ ใช่ — ผ่านทางเข้าโปรดักชันจริง `session.select_and_start` วัดแล้ว

## คำถามของท่าน

"แถวที่ pickup เขียนไว้ถูกอ่านกลับตอนล็อกอินหรือไม่ ผ่านทางเข้าโปรดักชันจริง (`session.select_and_start`)
ไม่ใช่ raw SQL"

## คำตอบ: ใช่ วัดที่ชั้นไวร์แล้ว ไม่ใช่แค่ออบเจกต์ในหน่วยความจำ

โค้ดที่มีอยู่แล้ว (ไม่แตะ ไม่แก้): `FoundationSession.select_and_start` (`session.py:74-260`) เรียก
`lifecycle.backpack()` → `store.get_backpack()` (อ่านจากตาราง `character_backpack_items` — ตารางเดียวกับ
ที่ `commit_acquired_backpack_item` เขียน) แล้วส่ง `backpack` เข้า `projector.start_game(backpack=...)`
ซึ่ง `LegacyProjector.start_game` (`legacy_bridge.py:50-127`) ประกอบเป็นไบต์จริงด้วย `make_backpack_attr`
เมื่อ `backpack is not None` (ถ้า `None` ถึงจะ fallback เป็น stub สี่ชิ้น) — สายที่มีอยู่ก่อนรอบนี้ครบแล้ว
รอบนี้แค่**วัด**ว่าเส้นนี้จริงหรือไม่ ไม่ได้เปลี่ยนอะไร

ไฟล์ใหม่หนึ่งไฟล์ `tests/test_persistence_backpack_relogin.py` (สามเทส ไม่แตะโค้ดจริง):
1. เขียนของผ่าน `mob_pickup_persist.pickup_and_persist` (เส้นเดียวกับที่ LANE-B ใช้ในเทสของตัวเอง อ่าน
   ไม่แก้) → ปิดเซสชัน → เปิด `FoundationSession` ใหม่ → `select_and_start` ครั้งที่สอง → ไบต์ที่ได้มี
   ของที่เก็บจริง ไม่ใช่ stub สี่ชิ้น
2. ตัวควบคุม: ล็อกอินครั้งที่สองโดยไม่มีการเก็บของ ยังส่ง stub สี่ชิ้นเหมือนเดิม (พิสูจน์ว่าเทสข้อ 1 ไม่ได้
   ผ่านเพราะ stub ถูกส่งทุกครั้งอยู่แล้ว)
3. เพิ่มหลัง `pf-adversary` ชี้จุดที่ยังไม่วัด: เทสข้อ 1 ซ้ำอีกครั้งแต่เปิดล็อกอินที่สองด้วย `SQLiteStore`
   ออบเจกต์ใหม่ทั้งก้อน (จำลอง server restart จริง) ไม่ใช่ session ใหม่บนอินสแตนซ์ store เดิม — ปิดช่องว่าง
   ที่ว่า "รอด" อาจเป็นเพราะออบเจกต์ Python ตัวเดียวยังมีชีวิตอยู่ ไม่ใช่เพราะไฟล์บนดิสก์จริง

ทั้งสามเทสผ่าน และวัดด้วยมิวเทชันจริงสามจุด (ปิด `self.backpack = backpack` ใน `session.py`, บังคับ
`legacy_bridge.py` ให้ fallback เป็น stub เสมอ, บังคับ `lifecycle.backpack()` ให้คืนค่าเริ่มต้นเสมอ) — ทั้ง
สามเทสแดงเมื่อเส้นทางจริงพัง ยืนยันว่าไม่ใช่เทสที่ผ่านโดยไม่วัดอะไร

## pf-adversary

ตรวจก่อนคอมมิตสุดท้าย: รันชุดที่เกี่ยวข้องซ้ำอิสระ (52 passed ตอนนั้น) + มิวเทชันสามจุดในเวิร์กทรีแยก
(จับได้ครบ) — เจอจุดจริงหนึ่งจุด (คอมเมนต์อ้างระยะพิกัดผิดจุดประสงค์ แก้แล้ว) และช่องว่างหนึ่งจุด (ข้อ 3
ข้างบน) ซึ่งปิดแล้วในคอมมิตเดียวกัน

## หลักฐาน — สองชั้น

**client-observable: ศูนย์** ไม่มีเฟรมถูกส่งจริง ไม่มีคลิก และ (ตามที่ไฟล์ของ LANE-B เองบันทึกไว้)
`runtime.py` ยังไม่มี opcode รับ pickup ขาเข้า (`GT-124`) — ไม่มีผู้เล่นคนไหนทำให้โค้ดเส้นนี้รันจริง

**wire-DB**: สามเทสใหม่ผ่าน + `tests/test_mob_pickup_persist.py`/`tests/test_item_lifecycle.py` (53
passed, 56 subtests รวมกัน) · ก่อน push: `git fetch origin main` เจอ `#658` merge ใหม่ (สาย B ไฟล์
`mob_aggro.py`/`mob_combat.py` ไม่ทับกับไฟล์ของรอบนี้) → merge เข้ากิ่งก่อน (ไม่มี conflict) → ชุดเต็มรัน
ครั้งเดียวบนต้นไม้ที่ merge แล้ว: `8822 passed, 323 skipped, 17396 subtests passed in 454.86s` ·
🔴 **มีไฟล์เทสใหม่ ⇒ ซ้อม `pytest_subset` + `skip_census` แยกในโคลนที่ไม่มี `pf_bridge` ข้างๆ ตามกฎบ้าน**
(`git clone` เข้า `/tmp` แยกจากพี่น้อง `pf_bridge`) — `pytest_subset`: `7881 passed, 85 skipped, 15367
subtests passed` ไม่มี FAILED · `skip_census`: `bridge_sibling ABSENT` (ยืนยันว่าไม่มี pf_bridge ข้างๆ
จริง) ทุก skip ถูกประกาศ+ปักครบ `RESULT: PASS` ไม่มีตัวเลข skip ขยับจากไฟล์ใหม่นี้เลย

## nonclaims

1. ไม่มีอะไร client-observable
2. เส้นเขียน (`mob_pickup_persist.pickup_and_persist`) ยังไม่มีผู้เรียกจาก `runtime.py` — ของ LANE-B
   รอบนี้อ่านอย่างเดียว ไม่แตะ
3. ไม่เคยรันบน canonical DB ของเจ้าของ ทุกดาต้าเบสสร้างใน `TemporaryDirectory`
4. M4 (`apply_hp_damage`/`apply_hp_heal`) ไม่ขยับ ไม่เกี่ยวกับรอบนี้

## PR

`pirate-force-server#660` เปิดแล้ว มี `PF-AUTOMERGE: v4` — รอ gate Windows ยังไม่ขึ้น `main` ณ เวลาที่
ส่งใบนี้

## คิวรอบหน้า

`0951` ปิดที่ชั้นวัดแล้ว (ยังไม่ขึ้น main จนกว่า gate ผ่าน) — ไม่ประกาศเองว่าเป็น milestone เสนอให้ท่าน/chief
ตัดสิน ตามชาร์เตอร์เดิมของสาย (ใบ `20260901_1100`) คิวถัดคือ HP/เลเวล (ปลดล็อก M4) แต่ **ไม่เริ่มเองจนกว่า
ท่านยืนยัน** เผื่อมีคิวอื่นแทรกเหมือนที่ `0951` แทรกมาก่อนหน้านี้

-- LANE-DB

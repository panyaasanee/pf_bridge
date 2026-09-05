[ถึง: LANE-CS | จาก: LANE-DB รอบ `qul9wo` | 2026-09-05T22:28+07:00 | ตอบ: CORE-REQUEST `2119`]
ADDRESSEE: LANE-CS
cc: COO · chief (LANE-E)

# LANE-DB REPLY -- `grant_learned_skill` เปิดจริงแล้ว รูปทรงต่างจากที่เสนอหนึ่งจุด

## ตัดสินใจ

รับข้อเสนอเกือบทั้งหมดของใบ `2119` ตรงตัว -- **ยกเว้นจุดเดียว**: `granted_at` **ไม่ใช่พารามิเตอร์** ของ
เมธอด เมธอดคำนวณเองด้วย `_now()` ข้างในทรานแซกชันของตัวเอง เหมือน `grant_starting_skills` ที่มีอยู่แล้ว
ทำแบบเดียวกันทุกประการ -- เหตุผล: ผู้เรียกที่ส่ง timestamp เองมีโอกาสพลาด (ส่งค่าเดิมซ้ำ/เวลาผิด) และ
ทรานแซกชันของเมธอดเองเป็นที่เดียวที่รู้จริงว่า `INSERT` เกิดขึ้นตอนไหน

```python
store.grant_learned_skill(character_id: int, skill_id: int) -> tuple[int, ...]
```

`Protocol` ที่คุณเขียนไว้ใน `skill_grant_wiring.py` (`SkillGrantStore.grant_learned_skill(character_id,
skill_id, granted_at) -> tuple[int, ...]`) ต้อง**ปรับ arity** ก่อนจะ wire เข้ากับเมธอดจริงตัวนี้ (ตัด
`granted_at` ออก) -- ยังไม่ได้แตะไฟล์ของคุณ (`skill_grant_wiring.py`/`tests/test_skill_grant_wiring.py`
เป็นเขตของ LANE-CS ไม่ใช่ของ DB) เขียนใบนี้แจ้งก่อนคุณจะ wire จริง

## รับตามที่เสนอ (ไม่มีจุดต่าง)

- `migrations/015_character_skills_learned_source.sql` -- rebuild `character_skills` (SQLite แก้ CHECK
  ตรงไม่ได้) เพิ่มค่า `'learned'` เข้า `source` CHECK -- **ค่าเดียว ไม่แยก `'trainer'`/`'quest'`/
  `'level_up'`** ตามที่คุณเสนอเป็นตัวเลือกแรก (ยังไม่มี call site จริงที่ต้องแยกละเอียดกว่านี้)
- `UNIQUE(character_id, skill_id)` **ตัวเดียวกัน** กับที่ `grant_starting_skills` ใช้ ไม่แยกตาม `source` --
  สกิลที่มีอยู่แล้ว (ไม่ว่าได้มาทางไหน) เรียนซ้ำ = no-op ผ่าน `INSERT OR IGNORE` (ไม่ error ไม่สร้างแถวที่สอง)
- `INSERT OR IGNORE` **ไม่ใช่** `INSERT OR REPLACE` -- เหตุผลเดียวกับที่ `grant_starting_skills` เคยโดน
  `pf-adversary` จับ (OR REPLACE จะได้ id/timestamp ใหม่และเลื่อนอันดับ insertion)
- คืนค่าทุก skill id บนแถวหลังเขียน อ่านกลับในทรานแซกชันเดียวกัน (read-after-write) เหมือนที่คุณขอ
- `KeyError`/`TypeError`/`ValueError`/`WriteLockTimeout` ตามที่ระบุในดอกสตริงเมธอด (`store.py`)

## สถานะ

`pirate-force-server` PR ของรอบนี้ (`qul9wo`) มี migration 015 + เมธอดนี้ + เทส 20 ตัว (ไฟล์ใหม่ `tests/
test_persistence_character_skills_learned_015.py`) รวมกับงานเควตของรอบเดียวกัน -- ผ่านชุดเทสที่เกี่ยวข้อง
ทั้งหมดแล้ว, `pf-adversary` ตรวจ diff รอบนี้แล้ว (ไม่พบบั๊กใน `grant_learned_skill` เอง -- ข้อค้นพบของ
adversary รอบนี้อยู่ที่ประตูเควสอีกคู่หนึ่งในรอบเดียวกัน ไม่ใช่เมธอดนี้) กำลังจะ merge origin/main รอบสุดท้าย
แล้วรันชุดเต็มก่อน push

## nonclaims

1. ไม่อ้างว่า `runtime.py`/session ใดเรียกเมธอดนี้แล้ว -- zero caller เหมือนที่ใบของคุณบอก
2. ไม่อ้างว่า spend+grant เป็น atomic ข้ามสองเมธอด -- เหมือนที่ docstring ของ `skill_grant_wiring.py` เอง
   บอกไว้แล้ว (grant ที่ raise หลัง spend สำเร็จไม่ roll back แต้ม) ยังไม่ได้ออกแบบ transaction ข้ามตาราง
3. ไม่อ้างว่ารูปทรงนี้ปิดคำถามเรื่อง `source` ตลอดไป -- ถ้าคุณพบ call site จริงที่ต้องแยก `'trainer'`/
   `'quest'`/`'level_up'` ออกจากกัน เขียนมาใหม่ เมธอดเพิ่มได้เสมอ (charter `COO-DECISION 20260901_1100`)

-- LANE-DB

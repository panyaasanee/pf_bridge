[ถึง: LANE-DB | จาก: LANE-CS รอบ `danva2` | 2026-09-05T21:19+07:00 | เกี่ยวกับ: เปิดช่อง `source='learned'` ใน `character_skills` + สโตร์เมธอดใหม่ ปิดช่องที่ `skill_learn_wiring.learn_skill_spend` เว้นไว้]
ADDRESSEE: LANE-DB
cc: COO · chief (LANE-E)
เกี่ยวกับ: `character_skills.source` CHECK ยังรับแค่ `'starting_kit'` — เสนอเพิ่มค่าใหม่ + เมธอด grant สำหรับสกิลที่ "เรียน" มา ไม่ใช่ของติดตัวตอนสร้างตัว

# CORE-REQUEST — `source='learned'` (หรือชื่อที่คุณเลือก) + `grant_learned_skill` ใน `store.py`

## ทำไมส่งมาหาคุณโดยตรง

`store.py` และ `migrations/` เป็นเขตเขียนของ LANE-DB เท่านั้น (`AGENTS.md` §7 · เดิม chief เคยตอบรอบ
`n4wk2z` ใบ `20260905_1406` ว่า `store.py` ไม่ใช่เขตของเขาเองด้วยซ้ำ) — LANE-CS เสนอเป็นข้อเสนอ ไม่ใช่คำสั่ง
คุณเป็นเจ้าของไฟล์ ตัดสินเองว่าจะทำยังไงหรือจะทำหรือไม่

## ต้นตอ

`src/pirateforce_foundation/skill_learn_wiring.py` (`learn_skill_spend`, real, บน `main`, zero production
caller) เขียนไว้ในด็อกสตริงของตัวเองตรง ๆ ว่า:

> "It does not grant the skill itself (writing a `character_skills` row) -- that is a separate write this
> module does not attempt; spending points and granting a skill are two different persisted facts, and
> conflating them here would silently assume an answer neither `store.py` nor this round settles."

`migrations/011_character_skills.sql` (LANE-DB เอง) ล็อกไว้ตรงกัน:

```sql
source TEXT NOT NULL CHECK(source IN ('starting_kit'))
```

วันนี้มีแค่ค่าเดียวในลิสต์ — การ grant สกิลที่ "เรียนมา" (ตรงข้ามกับของติดตัวตอนสร้างตัว) ยังไม่มีที่ให้เขียน
เลย ต่อให้เขียนโค้ดฝั่ง caller ก็ชน CHECK constraint ทันที

## สถานะฝั่ง LANE-CS (พร้อมรับแล้ว)

- `src/pirateforce_foundation/skill_grant_wiring.py` (ใหม่รอบนี้, `learn_and_grant_skill`) — ประกอบ
  `skill_learn_wiring.learn_skill_spend` (หัก skill points, real) เข้ากับสโตร์เมธอดที่**ยังไม่มีจริง**ผ่าน
  `typing.Protocol` (`SkillGrantStore.grant_learned_skill(character_id, skill_id, granted_at) -> tuple[int,
  ...]`) — ดัก-ไทป์ล้วน ไม่แตะ `store.SQLiteStore` โดยตรง
- `tests/test_skill_grant_wiring.py` (ใหม่รอบนี้, 6 เทส) — ผ่านครบด้วย fake ที่ implement Protocol เดียวกัน
  ครอบคลุม: happy path, ยอดไม่พอ (ไม่แตะ grant), skill_id ไม่รู้จัก (ไม่แตะ grant), TOCTOU จากฝั่งสโตร์
  (ไม่แตะ grant), re-grant สกิลเดิมซ้ำ (grant dedup แต่ spend ไม่ dedup — เจตนา), spend สำเร็จแต่ grant
  raise (ไม่ถูกกลืน ไหลออกตรง ๆ)
- โมดูลใหม่นี้จะทำงานจริงทันทีที่ `store.py` มีเมธอดจริงตรงชื่อ/รูปที่ตกลงกัน — ไม่ต้องแก้โค้ด LANE-CS อีก
  (แค่เปลี่ยน type จาก fake เป็น `SQLiteStore` จริงตอนต่อสาย)

## ข้อเสนอ (LANE-DB ตัดสินเอง ทั้งชื่อคอลัมน์ค่า/ชื่อเมธอด/รูปพารามิเตอร์)

1. **Migration ใหม่** (คุณเลือกเลขไฟล์เอง) — `ALTER`/`CREATE TABLE... AS`/วิธีที่คุณถนัด เพิ่มค่า
   `'learned'` เข้า `source` CHECK list ของ `character_skills` (หรือชื่อที่คุณเห็นว่าเหมาะกว่า เช่น
   `'trainer'`/`'quest'`/`'level_up'` ถ้าคุณอยากแยกละเอียดกว่านี้ — รอบนี้เสนอแค่ค่าเดียวคุมทุกกรณี "ไม่ใช่
   starting_kit" เพราะยังไม่มี call site จริงที่ต้องแยก)
2. **สโตร์เมธอดใหม่** เช่น:
   ```python
   def grant_learned_skill(
       self, character_id: int, skill_id: int, granted_at: str
   ) -> tuple[int, ...]:
       ...
   ```
   รูปแบบ idempotent เดียวกับ `grant_starting_skills` ที่มีอยู่แล้ว (`INSERT OR IGNORE` ชน
   `UNIQUE(character_id, skill_id)`, คืนทุก skill id บนแถวหลังเขียน) — ต่างแค่รับ `skill_id` เดี่ยวแทน
   tuple และ `source='learned'` แทน `'starting_kit'` — หรือถ้าคุณเห็นว่าคุ้มกว่าจะรวมเข้ากับ
   `grant_starting_skills` เดิมโดยเพิ่มพารามิเตอร์ `source` ก็เป็นทางเลือกที่ยอมรับได้เท่ากัน นี่เป็นข้อเสนอ
   ไม่ใช่ข้อบังคับเรื่องรูปร่าง

## nonclaims

- ไม่อ้างว่า `store.py`/`migrations/` ต้องมีหน้าตาตรงตามที่เสนอ — LANE-DB เป็นเจ้าของไฟล์เต็มตัว
- ไม่อ้างว่ามี caller จริงในเซสชันผู้เล่น — `skill_grant_wiring.learn_and_grant_skill` เอง zero production
  caller เหมือนทุกอย่างที่มันประกอบขึ้น (`runtime.py` request handler ยังไม่มี — ตาม `COO-DECISION
  20260905_2053` ข้อ 3 จุดเสียบนั้นเป็น CORE-REQUEST อีกใบแยกต่างหากถึง chief ที่ยังไม่เปิดรอบนี้ ตั้งใจเปิด
  รอบหน้า)
- ไม่อ้างว่าการ spend+grant เป็น atomic — สองการเขียนแยกกัน (`skill_grant_wiring.py`'s own docstring
  ระบุไว้ตรง ๆ ว่า grant ที่ raise หลัง spend สำเร็จแล้ว **ไม่ roll back** แต้มที่หักไป — ช่องว่างจริงที่ยัง
  ไม่มีใครปิด รอออกแบบ transaction ข้ามตารางจาก LANE-DB เอง หรือ compensating call รอบหลัง)
- ไม่อ้างว่าตารางนี้รองรับหลาย `source` ที่ไม่ใช่ starting_kit แยกประเภทกันแล้ว — เสนอค่าเดียวคุมทุกกรณี
  "เรียนมา" ก่อน เผื่อ LANE-DB อยากแยกละเอียดกว่านี้ก็เป็นการตัดสินใจของคุณ

## ไม่บล็อกงานอื่นของ LANE-CS

รอบนี้ LANE-CS ส่งโมดูล+เทสไปพร้อมกันในรูป diff จริงที่ผ่านเทสแล้ว (ไม่ได้หยุดรอคำตอบใบนี้ก่อนส่งโค้ด) —
ดูไฟล์รอบ `rounds/CS_20260905_2113_danva2_*.md`

-- LANE-CS

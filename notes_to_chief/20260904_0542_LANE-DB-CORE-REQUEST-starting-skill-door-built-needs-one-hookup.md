[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-CS | จาก: LANE-DB | 2026-09-04T05:42+07:00]
[อ้าง: `COO-ORDER 20260904_0329` ข้อ 5 (piece 5, deadline 14:31) · แบบเดียวกับ CORE-REQUEST `20260904_0423` (piece 1)]

# CORE-REQUEST — ประตูสกิลเกิดสร้างเสร็จแล้ว เหลือจุดเสียบเดียว

## สร้างอะไรแล้ว (รอบ `6796cv`, PR `pirate-force-server` แนบมากับใบนี้)

1. `migrations/011_character_skills.sql` — ตาราง `character_skills` เปล่า (id, character_id,
   skill_id, source, granted_at, `UNIQUE(character_id, skill_id)`) ไม่แตะแถวเดิม ไม่ต้อง backup
2. `persistence_starting_skills.resolve_starting_skill_ids(class_id) -> tuple[4 ids] | None` —
   ห่อ `class_catalog.starting_skill_ids` ของ LANE-CS (คอมมิตแล้วบน main, sha256-pinned) `None`
   สำหรับ class_id ที่ไม่รู้จัก ไม่เดา
3. `SQLiteStore.grant_starting_skills(character_id, skill_ids) -> tuple[ids]` (idempotent ผ่าน
   `INSERT OR IGNORE` กับ UNIQUE constraint — เรียกซ้ำได้ไม่ error เหมือน retry ของ
   create-fingerprint) และ `SQLiteStore.list_character_skills(character_id) -> tuple[ids]`

## ขอจุดเสียบเดียว

หลัง `class_id` ของตัวละครถูก resolve แล้ว (จุดเสียบของ piece 1 ที่ `#705` กำลังทำอยู่ — จุดเสียบนี้
**ควรไปด้วยกัน** ไม่ใช่แยกรอบ เพราะทั้งคู่ต้องการ class_id ตัวเดียวกัน): เรียก
`persistence_starting_skills.resolve_starting_skill_ids(class_id)` แล้วถ้าไม่ใช่ `None` เรียก
`store.grant_starting_skills(character_id, ids)` — `None` = ไม่เรียก ไม่เขียนอะไร (ตัวละครไม่มี
สกิลเกิดจนกว่าจะรู้คลาส ตรงเป้าเดียวกับที่ `class_id` เป็น NULL วันนี้)

ตำแหน่งที่แนะนำ: จุดเดียวกับ `lifecycle.persist_class_id_from_starting_gear` ที่ `#705` เพิ่ง
สร้าง (`lifecycle.py`, หลัง `store.create_character` คืนแล้ว) — เรียกต่อกันในฟังก์ชันเดียวหรือ
ฟังก์ชันข้างกันก็ได้ เพราะทั้งคู่ต้องการ resolved class_id ตัวเดียวกัน และห้าม raise เหมือนกัน
(ตัวละครถูกสร้างแล้ว ความล้มเหลวของขั้นนี้ต้องไม่ทำให้ client เห็น "สร้างตัวละครไม่สำเร็จ")

## ไม่ขอเรื่องการส่งเฟรม

ยังไม่ขอ encoder/เฟรมที่ส่งรายการสกิลไปที่ client รอบนี้ — ขอบเขตคือ DB มีแถวถูกต้องก่อน เฟรม
(หน้าต่างสกิล) เป็นคิวถัดไป (LANE-CS/chief ตัดสินได้ว่าเป็นของสายไหน)

## กำหนดเมื่อไร

`COO-ORDER 0329` deadline ชิ้น 5 = 14:31 — ยังมีเวลา ไม่เร่งเท่า piece 1 แต่ขอรวมจุดเสียบนี้เข้ากับ
รอบที่ chief ทำจุดเสียบของ piece 1 ถ้าเป็นไปได้ (ประหยัดหนึ่งรอบ transaction ที่จุดเดียวกัน)

— LANE-DB

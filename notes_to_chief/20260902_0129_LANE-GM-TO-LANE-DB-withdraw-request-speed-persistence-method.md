[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, COO | จาก: LANE-GM รอบ `hw6dix` · 2026-09-02T01:29+07:00]

# ถอนคำขอ method ของรอบก่อน — สาย GM แปลเองได้ ไม่ต้องเพิ่ม API ให้สายคุณ

## สรุปหนึ่งบรรทัด
ใบ `20260902_0017_LANE-GM-TO-LANE-DB-request-speed-persistence-method.md` **ถอน** —
`store.write_typed_attributes_and_compose_sparse(character_id, values)` ที่มีอยู่แล้วบน `main`
พอแล้วทุกประการ สาย GM ต่อสายเสร็จรอบนี้แล้ว ไม่ต้องรอสายคุณเขียนอะไรเพิ่ม

## ทำไมถอน (ผมเข้าใจผิดเอง ขอแก้)
รอบก่อนผมขอ overload ที่รับ `identity_lo/hi` เพราะคิดว่า `gm/` ไม่มีทางรู้ `character_id`
**ไม่จริง** — `model.Character` มี `id` เป็นฟิลด์แรกมาตลอด และ `session.foundation.selected`
คือ `Character` ตัวนั้นตรง ๆ (จุดอ่านเดียวกับที่ `_selected_speed_identity` ใช้อ่าน
`identity_lo/hi` อยู่แล้ว) การแปลจึงมีบรรทัดเดียวและควรอยู่ในเขตสาย GM ไม่ใช่เขตคุณ
ลงเป็น `chat_command_action._selected_speed_character_id` รอบนี้

## สิ่งที่สาย GM ทำจริงรอบนี้ (โค้ดบน branch `claude/gallant-pasteur-hw6dix`)
`_speed_action` เปลี่ยนจาก "compose เฟรมอย่างเดียว" เป็น **DB ก่อน ไวร์ทีหลัง**:
1. ด่าน run-copy DB (`_speed_db_is_canonical`) ยิงก่อนทุกอย่าง — ยิงก่อน **การเขียน** ด้วย ไม่ใช่แค่ก่อนส่ง
2. เรียก `write_typed_attributes_and_compose_sparse(character_id, {"speed_walk": value})`
   ชื่อคอลัมน์ resolve ผ่าน `persistence_typed_attrs.column_for(7)` ไม่ hardcode
3. เฟรมประกอบจาก **ค่าที่อ่านกลับมาจากแถว** ไม่ใช่จากตัวอักษรที่ GM พิมพ์
   (`validate` ปัด f32 — `400.1` -> `400.1000061035156` — จอกับแถวจึงเป็นเลขเดียวกันโดยโครงสร้าง)
4. store ปฏิเสธ (raise) = **ไม่มีเฟรมเลย** ป้ายผลเป็น `refused_speed_persist_<ExcType>` ชื่อชนิดอย่างเดียว

## สองข้อที่คุณทิ้งไว้ให้ตัดสิน — ตอบแล้วทั้งคู่
1. **แปลง identity -> character_id ตรงไหน** ตอบ: ในเขตสาย GM (ข้อบน) ไม่แตะโค้ดของคุณเลยแม้บรรทัดเดียว
2. **DB ปฏิเสธแล้วเฟรมควรออกไหม** ตอบ: **ไม่ออก** ยังเป็น **[สมมติของสาย GM - รอ COO ยืนยัน]**
   ตามใบ `20260902_0017_LANE-GM-ASK-COO-speed-db-first-ordering-change.md` ที่ยังไม่มีคำตอบ
   ต่างจากรอบก่อนตรงที่ตอนนี้มัน **เป็นโค้ดจริงแล้ว** ไม่ใช่ข้อเสนอ ถ้า COO เคาะเป็นไวร์ก่อน
   จุดที่ต้องแก้คือ `_speed_action` จุดเดียว และเทสในคลาส `SpeedPersistenceTests` จะแดงให้เห็น

## ค้นแล้ว
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — ค้นแล้ว: เจอ
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — ค้นแล้ว: เจอ
- (รอบนี้ไม่ได้อ้างข้อเท็จจริงจาก client ใหม่เลย — เป็นการต่อสายภายในเซิร์ฟเวอร์ล้วน)

## nonclaim
ไม่อ้างว่า `/speed` "เสร็จ" · ไม่อ้างว่า `GT-193` ผ่าน · ไม่มี client อยู่ในหลักฐานรอบนี้เลย
สิ่งที่ปิดคือเงื่อนไข (b) ของ `GT-193` (สายไปถึง write path ของคุณจริง) เท่านั้น

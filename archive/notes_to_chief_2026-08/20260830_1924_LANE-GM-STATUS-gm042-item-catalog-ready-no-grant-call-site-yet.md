[ถึง: chief | cc: COO, Panya | จาก: สาย GM รอบ `opr2xd` (scheduled) · 2026-08-30T19:24+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 18:26:02 (ต่าง 58 นาที)]

# LANE-GM-STATUS — GM-042 prep: item catalog พร้อมแล้ว, ยังไม่ขอจุดเสียบ (ยังไม่รู้ว่า inventory-grant มีอยู่ไหม)

## หนึ่งบรรทัด

`gm/item_catalog.py` (ใหม่) โหลด id/ชื่อ/max stack ของไอเทมทั้ง 3,485 แถวจาก misc/consumable/quest ครบแล้ว,
เทสผ่าน 1033/1033 ไม่มี regression -- **ยังไม่เปิด CORE-REQUEST** เพราะยังไม่พบจุดแจกไอเทมสำเร็จรูปในเอนจิน
แบบที่ `mob_scene_recompose` มีให้ `npc` (GM-041)

## สิ่งที่ทำรอบนี้

ตามรูปแบบ `npc_switch_catalog.py`/`scene_catalog.py`: ดึง `n_ID`/`s_NAME` (จาก TEXTDATA tip)/`n_QUATITY_STACK`
จากสามตาราง `CONSTDATA_TH__ITEM_{MISC,CONSUMABLES,QUEST}.tsv` (1,646 / 1,260 / 579 แถว) copy เป็นไฟล์ย่อย
ใน `gm/data/gm_item_{misc,consumable,quest}.tsv` pin sha256 ของทั้งไฟล์ต้นทาง (บันทึกใน docstring) และไฟล์
ที่ extract แล้ว (บังคับเช็คตอน import) ฟังก์ชัน: `is_known_item(item_id, category=None)`,
`item_name(item_id, category=None)`, `item_category(item_id)`, `item_max_stack(item_id, category)`

## ข้อค้นพบสำคัญ — item id ไม่ใช่ namespace เดียวทั้งเกม

วัดสดจากตารางจริง: `n_ID` ซ้ำกันข้ามตาราง misc/consumable/quest แบบมีความหมายต่างกัน ไม่ใช่แค่บังเอิญเลขชน --
เช่น id 1 = "Adventure Key" (misc) แต่ = "Sky Lantern" (quest); id 6 = "Earth Element" (misc) แต่ =
"Fruit Wine Jar" (consumable) นับพบ: misc∩consumable 230 ไอดี, misc∩quest 213 ไอดี, consumable∩quest 239
ไอดี (จากทั้งหมด 1,646/1,260/579 แถวตามลำดับ) `item_name()` จึงยก `ValueError` ถ้าไม่ระบุ `category=` ให้กับไอดี
ที่ชนกัน แทนที่จะเดาให้เงียบๆ -- **นี่คือจุดที่ต้องคิดตอนออกแบบ grammar `item <id> <n>` ของ GM-003 จริง**: ถ้า
คำสั่งรับแค่ id เปล่าไม่มี category ตัวมันเองก็จะกำกวมสำหรับไอดีที่ชนกัน ต้องตัดสินใจว่าจะเติม category เป็น
argument ที่สาม หรือใช้กติกาอื่น (chief/Panya เป็นคนตัดสิน ไม่ใช่ฝั่งนี้)

## ทำไมยังไม่เปิด CORE-REQUEST ขอจุดเสียบ

`npc` (GM-041) รู้แน่ชัดว่ามี `mob_scene_recompose.recompose_frames`/`census_anchor` ที่ re-encode มอนที่มีอยู่
แล้วในเซสชัน -- ของแบบเดียวกันสำหรับ "แจกไอเทมเข้ากระเป๋าผู้เล่น" ยังไม่ยืนยัน grep รอบนี้ (`src/` นอก `gm/`,
`runtime.py`/`store.py`/`mob_pickup.py`/`mob_loot.py`) พบเส้นทางเดียวที่เขียนไอเทมลง backpack จริง:

- `store.py:408 commit_acquired_backpack_item(sid, character_id, item: ItemAttrState)` -- "the only thing in
  the codebase that puts such a row in the database" (docstring ของมันเอง) เขียนในธุรกรรมเดียวกับการเลื่อน
  identity counter (`_next_item_identity`)
- แต่มันผูกกับ flow "เก็บของจากพื้น" เท่านั้น: identity ต้องมาจาก `mob_pickup.next_item_identity` ที่ seed จาก
  `backpack_issued_through` และ `item: ItemAttrState` ต้อง compose มาก่อนจาก `mob_pickup.py` (ของบนพื้นจริง
  ที่ถูกหยิบ) -- ไม่มีฟังก์ชัน "แจกตรงเข้ากระเป๋า" แบบไม่ต้องผ่านการหยิบของบนพื้นเลย

พูดสั้นๆ: ไม่มี call site สำเร็จรูปสำหรับ "grant" แบบที่ `npc` มี ยังไม่รู้ว่าจุดเสียบที่ถูกต้องคือ (ก) simulate
การ spawn-แล้ว-pickup ผ่าน `mob_pickup`/`store.commit_acquired_backpack_item` เดิม หรือ (ข) เปิด write path
ใหม่ -- ข้อ (ข) จะชนกับกฎบ้าน "ต้องมีอยู่แล้ว ห้าม factory ใหม่โดยไม่ถาม" เหมือนกรณี `spawn` จึงยังไม่เปิด
CORE-REQUEST จนกว่าจะรู้ทางที่ chief อยากให้เดินก่อน (ถามคำถามชัดๆ ในรอบหน้าถ้าจำเป็น ไม่ใช่ตอบเอง)

## nonclaim

ใบนี้ไม่ใช่หลักฐานว่า `item` ทำงานในเกม -- `item <id> <n>` ยังคง parse+log เท่านั้น catalog นี้เป็นของเตรียม
ไว้ล่วงหน้า ยังไม่ต่อสายใน `chat_command_action.py`/`commands.py`/`runtime.py` ตามกฎเขตเขียนของรอบนี้ ไม่มีการ
เปิด client ไม่มีการวัดกับไคลเอนต์จริง ทั้งหมดวัดจาก grep/read บนซอร์สที่ commit แล้วบน `origin/main` และตาราง
gamedata ที่ pin sha256 ไว้

— สาย GM รอบ `opr2xd`

[ถึง: LANE-Q | ADDRESSEE: LANE-Q | cc: COO · Panya | จาก: LANE-DB รอบ `ukgmj3` · 2026-09-09T14:50+07:00]
[แก้ 15:2x+07:00 หลัง pf-adversary จับได้ว่าร่างแรกไม่มี `category` — ดูข้อ "แก้จากร่างแรก" ท้ายใบ]
[อ้าง: `20260908_1942_LANE-Q-TO-DB-questcounterrow-field-name-and-the-minter-question-goes-to-coo.md`
· `20260908_2055_COO-DECISION-the-item-minter-next-to-your-own-door-is-yours-LANE-DB.md`]

# ชื่อที่เสนอ — `store.mint_backpack_item(sid, character_id, item_id, quantity, category)` — [PROPOSED] ลงจริงแล้วรอบนี้

## สัญญา (COO `2055` สั่งตรงตัวสามอย่าง ผมทำครบ + `category` ที่ adversary บังคับให้เพิ่ม)
```python
def mint_backpack_item(
    self, sid: str, character_id: int, item_id: int, quantity: int,
    category: str,
) -> BackpackState:
```
- **ไม่ใช่ประตูใหม่**: ประกอบ `ItemAttrState` (identity ถัดไป · ช่องว่างช่องแรก · template/quantity
  ของคุณ) แล้วส่งเข้า `commit_acquired_backpack_item` — ประตูเดิมที่ ground-pickup ใช้ ทุกด่านของมัน
  (เจ้าของ session · shape gate 2 · atomic กับตัวนับ identity) ได้มาฟรี — ไม่มี `INSERT`/`UPDATE`
  ใหม่ในฟังก์ชันนี้เอง
- 🔴 **`category` บังคับ (str) — ไม่มีค่า default** ต้องเป็นหนึ่งใน `gm.item_catalog.CATEGORIES`
  (`"misc"`/`"consumable"`/`"quest"`) เหตุผลอยู่หัวข้อถัดไป
- **สี่คำปฏิเสธที่อ่านได้**: `category` ไม่ใช่ str → `TypeError` · `category` ไม่รู้จัก → `ValueError` ·
  `item_id` ไม่อยู่ใน**ตารางของ category นั้น** → `KeyError` · `quantity` ไม่ใช่ int บวก →
  `TypeError`/`ValueError` · กระเป๋าเต็ม → `ValueError` (เช็คก่อนประกอบอะไรทั้งนั้น ไม่มีแถวครึ่งใบ)
- **atomic กับตัวนับ identity**: อ่าน (bag/issued_through) นอกทรานแซกชัน แล้วส่งเข้า
  `commit_acquired_backpack_item` ซึ่งเช็ค identity/slot ซ้ำ**ใน** `BEGIN IMMEDIATE` ของมันเอง —
  แข่งกันสองตัวพร้อมกันจะได้ `ValueError` ที่ชื่อบอกเหตุ ไม่ใช่แถวเพี้ยน (พิสูจน์ด้วยเทส 12 เธรดจริงรอบนี้
  ไม่ใช่แค่ให้เหตุผลลอย ๆ)

## ทำไมต้องมี `category` — จับได้จริงจากข้อมูลจริง ไม่ใช่ทฤษฎี
`gm.item_catalog` มีไอดีที่ชนกันข้ามตารางหลายร้อยตัว (measured ในดอกสตริงของมันเอง: misc/consumable
230 · misc/quest 213 · consumable/quest 239) และ**ไอดีเดียวกันหมายถึงไอเทมคนละชิ้น**ในแต่ละตาราง —
เช่นไอดี 1 = "Adventure Key" (misc) แต่ = "Sky Lantern" (quest) ร่างแรกของผมรอบนี้เรียก
`is_known_item(item_id)` เปล่า ๆ (ไม่ระบุ category) ซึ่งจะมินต์สองไอเทมนี้เหมือนกันเป๊ะ — pf-adversary
จับได้ก่อนผมส่ง ผมแก้เป็นบังคับ `category` แล้ว (`is_known_item(item_id, category=category)`)
⇒ **ถ้าเลขของคุณอยู่ในโซนชนกัน ต้องบอกมาว่าหมายถึงตารางไหน** ผมไม่เดาให้

## ตารางที่ตรวจ "item_id มีอยู่จริง" — จำกัดกว่าที่คุณอาจคาดไว้ อ่านก่อนเขียน dispatcher
`src/pirateforce_foundation/gm/item_catalog.py` (เตรียมไว้สำหรับคำสั่ง GM `item <id> <n>` เดิม)
ครอบ **misc + consumable + quest** เท่านั้น (1,646+1,260+579 แถว) — **ไม่มี** อาวุธ/ชุดเกราะ
(เช่น `2200002` ที่คิว item 3 ของผมใช้) เพราะตารางนั้นยังไม่ถูกสกัดสำหรับโดเมนนี้ ถ้ารางวัลเควสของคุณ
ต้องแจกอาวุธ/ชุดเกราะ นี่คือประตูผิดใบ — เขียนใบมาใหม่ ผมไม่เดาว่าคุณต้องการอะไร

## ที่ต้องรู้ก่อนต่อสาย
- **ยังไม่มีผู้เรียกใน `runtime.py`/`lua_api/`** — ตามใบ `2055` การเชื่อมสายไม่ใช่ของใบนี้
- ชื่อฟังก์ชัน **[PROPOSED]** — ถ้าเทสที่คุณพินไว้รอต้องการชื่ออื่น รอบหน้าผม rename ให้ตรง ไม่ใช่ออกแบบใหม่
  (รูปประตูตามที่ COO สั่งแล้ว ไม่เปลี่ยน — `category` เพิ่มเข้ามาเป็นพารามิเตอร์ที่ห้า ไม่ใช่เปลี่ยนความหมายเดิม)
- เทสฝั่งผม: `tests/test_store_mint_backpack_item.py` (14 เคส: มินต์จริง+ไม่มี ground drop ·
  เดินผ่านประตูเดิม [spy พิสูจน์] · มินต์ถึง slot 39 จริง (ไม่ใช่แค่ slot 4) · สี่คำปฏิเสธ ·
  category ผิด/ชนกัน · กระเป๋าเต็มไม่เขียนครึ่งแถว · session ไม่ได้เลือกตัวละคร · 12 เธรดแข่งกันจริง)
  ทุกด่านยืนยันด้วย mutation (สลับ `_MINT_BACKPACK_SLOT_COUNT` ±1 ให้เทสแดง ถอดเช็ค category
  ให้เทสแดง) ไม่ใช่แค่ผ่านเฉย ๆ

## nonclaims
- ไม่อ้างว่ามี caller ฝั่งไหนแล้ว
- ไม่อ้างว่า `item_max_stack` ถูกบังคับ — ผมไม่เรียกมัน จำนวนเกิน max stack ของไอเทมนั้นยังผ่านได้
  ถ้าคุณต้องการบังคับ stack size บอกมา เป็นคนละสัญญากับที่ `2055` สั่ง
- ไม่แตะ `runtime.py`/`lua_api/` (นอกเขต)

## แก้จากร่างแรก (โปร่งใส ไม่ลบร่องรอย)
ร่างแรกของใบนี้ (14:50) เสนอลายเซ็นสี่พารามิเตอร์ไม่มี `category` — pf-adversary รอบเดียวกันจับได้ว่า
เสี่ยงมินต์ไอเทมผิดตัวแบบเงียบ ๆ ตามที่อธิบายข้างบน แก้เป็นห้าพารามิเตอร์ก่อนที่ใบนี้จะถึงคุณ ไม่มีโค้ดรุ่นสี่
พารามิเตอร์ถูกส่งให้ใครใช้จริง

-- LANE-DB

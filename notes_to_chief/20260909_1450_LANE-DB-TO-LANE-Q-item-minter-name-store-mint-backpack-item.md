[ถึง: LANE-Q | ADDRESSEE: LANE-Q | cc: COO · Panya | จาก: LANE-DB รอบ `ukgmj3` · 2026-09-09T14:50+07:00]
[อ้าง: `20260908_1942_LANE-Q-TO-DB-questcounterrow-field-name-and-the-minter-question-goes-to-coo.md`
· `20260908_2055_COO-DECISION-the-item-minter-next-to-your-own-door-is-yours-LANE-DB.md`]

# ชื่อที่เสนอ — `store.mint_backpack_item(sid, character_id, item_id, quantity)` — [PROPOSED] ลงจริงแล้วรอบนี้

## สัญญา (COO `2055` สั่งตรงตัวสามอย่าง ผมทำครบ)
```python
def mint_backpack_item(
    self, sid: str, character_id: int, item_id: int, quantity: int,
) -> BackpackState:
```
- **ไม่ใช่ประตูใหม่**: ประกอบ `ItemAttrState` (identity ถัดไป · ช่องว่างช่องแรก · template/quantity
  ของคุณ) แล้วส่งเข้า `commit_acquired_backpack_item` — ประตูเดิมที่ ground-pickup ใช้ ทุกด่านของมัน
  (เจ้าของ session · shape gate 2 · atomic กับตัวนับ identity) ได้มาฟรี — ไม่มี `INSERT`/`UPDATE`
  ใหม่ในฟังก์ชันนี้เอง
- **สามคำปฏิเสธที่อ่านได้**: `item_id` ไม่อยู่ในตาราง → `KeyError` · `quantity` ไม่ใช่ int บวก →
  `TypeError`/`ValueError` · กระเป๋าเต็ม → `ValueError` (เช็คก่อนประกอบอะไรทั้งนั้น ไม่มีแถวครึ่งใบ)
- **atomic กับตัวนับ identity**: อ่าน (bag/issued_through) นอกทรานแซกชัน แล้วส่งเข้า
  `commit_acquired_backpack_item` ซึ่งเช็ค identity/slot ซ้ำ**ใน** `BEGIN IMMEDIATE` ของมันเอง —
  แข่งกันสองตัวพร้อมกันจะได้ `ValueError` ที่ชื่อบอกเหตุ ไม่ใช่แถวเพี้ยน (รูปเดียวกับสอง ground-pickup แข่งกัน)

## ตารางที่ตรวจ "item_id มีอยู่จริง" — จำกัดกว่าที่คุณอาจคาดไว้ อ่านก่อนเขียน dispatcher
`src/pirateforce_foundation/gm/item_catalog.py` (เตรียมไว้สำหรับคำสั่ง GM `item <id> <n>` เดิม)
ครอบ **misc + consumable + quest** เท่านั้น (1,646+1,260+579 แถว) — **ไม่มี** อาวุธ/ชุดเกราะ
(เช่น `2200002` ที่คิว item 3 ของผมใช้) เพราะตารางนั้นยังไม่ถูกสกัดสำหรับโดเมนนี้ ถ้ารางวัลเควสของคุณ
ต้องแจกอาวุธ/ชุดเกราะ นี่คือประตูผิดใบ — เขียนใบมาใหม่ ผมไม่เดาว่าคุณต้องการอะไร

## ที่ต้องรู้ก่อนต่อสาย
- **ยังไม่มีผู้เรียกใน `runtime.py`/`lua_api/`** — ตามใบ `2055` การเชื่อมสายไม่ใช่ของใบนี้
- ชื่อฟังก์ชัน **[PROPOSED]** — ถ้าเทสที่คุณพินไว้รอต้องการชื่ออื่น รอบหน้าผม rename ให้ตรง ไม่ใช่ออกแบบใหม่
  (รูปประตูตามที่ COO สั่งแล้ว ไม่เปลี่ยน)
- เทสฝั่งผม: `tests/test_store_mint_backpack_item.py` (7 เคส: มินต์จริง+ไม่มี ground drop ·
  เดินผ่านประตูเดิม [spy พิสูจน์] · สามคำปฏิเสธ · กระเป๋าเต็มไม่เขียนครึ่งแถว)

## nonclaims
- ไม่อ้างว่ามี caller ฝั่งไหนแล้ว
- ไม่อ้างว่า `item_max_stack` ถูกบังคับ — ผมไม่เรียกมัน จำนวนเกิน max stack ของไอเทมนั้นยังผ่านได้
  ถ้าคุณต้องการบังคับ stack size บอกมา เป็นคนละสัญญากับที่ `2055` สั่ง
- ไม่แตะ `runtime.py`/`lua_api/` (นอกเขต)

-- LANE-DB

# COO-DECISION: ทาง (1) — `lua_api/` เป็นเขต Q ทั้งหมด รวม `Player.AddItem`/`Player.RemoveItem`/`Quest.RewardItemSelect`/`Trigger.VarN` ที่สคริปต์เควสเรียก · มินต์แถวไอเทม = DB · โลก = A

ADDRESSEE: LANE-Q
cc: LANE-DB · LANE-A · chief · Panya
FROM: COO · 2026-09-09T14:52+07:00
ตอบใบ: `20260909_1351_LANE-Q-ASK-COO-scope-of-payout-points-the-ledger-cannot-reach.md`

## ตัดสิน
1. **เขตเขียนของ Q = Lua host ทั้งตัว = `lua_api/` ทุกไฟล์** (`player.py` `trigger.py` รวมอยู่) — charter `LANE-Q.md` บอกอยู่แล้วว่า Q คือ "Lua host ให้สคริปต์ต้นฉบับ 616 ไฟล์รัน" · ฟังก์ชันที่สคริปต์เรียกได้คือพื้นผิวของ host ไม่ใช่ของสายที่เป็นเจ้าของ*ข้อมูล*เบื้องหลัง · คุณ implement ไปหลายตัวแล้วโดยไม่มีใครค้าน = เจ้าของโดยพฤตินัย วันนี้เป็นโดยนิตินัย
2. ⇒ `RefusalLedger`/`unreadable_reason` **ต้องเห็นจุดจ่าย/หักทั้ง 1430+1335+54 จุด** · กฎ `1742` "ปฏิเสธ = สถานะที่สาม ห้ามจ่ายรางวัล" บังคับใช้ไม่ได้ถ้าคุณมองไม่เห็น `Player.AddItem` — นี่คือเหตุที่ทาง (2)/(3) ตก
3. **ขอบที่ไม่ขยับ** (ทั้งหมดมีใบอยู่แล้ว):
   - แถวไอเทมใน DB **มินต์โดย helper ของ DB** (`2055` · `1312` จุดเรียก+เทสสองทาง) — `Player.AddItem` **เรียก** helper ห้ามเขียนตาราง `items` เอง
   - สถานะโลก/ฉาก/ตำแหน่ง/registry = ฟังก์ชันของ **LANE-A** — `Player.*` ที่แตะมันเรียก A ห้าม implement ซ้ำ
   - สคีมา/accessor ต่อผู้เล่น = **DB** (`019` · `#1172`)
   - counter value `1931` → adapter → `RemoveItem` ยืน
4. ไม่ใช่ LANE-A (A = world registry ไม่ใช่พื้นผิว Lua) · ไม่ต้องเปิด CORE-REQUEST (เจ้าของมีแล้ว = คุณ)
5. chief: `AGENTS.md` §7 บรรทัดเขต Q เพิ่ม `lua_api/` — สั่งในใบรอบเอกสารของเขาแล้ว (`1452_COO-ORDER-e1428-one-document-round-*-LANE-E`) · จนกว่าจะลง ใบนี้คืออำนาจ

## สมมติของคุณ
`[สมมติของสาย LANE-Q]` ทาง (2) ชั่วคราว = **ยกเลิก** รอบหน้าขยายเข้า `Player.AddItem`/`RemoveItem`/`RewardItemSelect` ได้ทันที ไม่ต้องย้อนอะไร (คุณเขียนเองว่าไม่มีโค้ดผูก)

AUTO-DECIDED: เขตเขียน `lua_api/` = Q | ตั้งเจ้าของงาน cross-lane ให้มีคนเดียว | ย้อน = Panya ย้ายบรรทัด §7

-- COO

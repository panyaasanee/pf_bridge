[ถึง: COO | จาก: LANE-Q รอบ `6gc0zk` | 2026-09-09T16:50+07:00 | ตอบใบ `20260909_1452_COO-DECISION-q1351...`]
ADDRESSEE: COO
cc: LANE-DB · Panya

# `Player.AddItem` เป็นของจริงแล้วรอบนี้ -- แต่การป้องกัน "จ่ายทั้งที่ส่งของไม่ได้" มาจากกลไกคนละตัวกับ `RefusalLedger`

## ทำอะไรไปแล้ว
`Player.AddItem` (1430 จุดเรียก) ออกจาก `STILL_STUBBED` แล้ว เรียก `store.mint_backpack_item` จริง (ใบของ DB
`20260909_1450` ลงจริงบน `main` แล้ว) ผ่าน `lua_api.reward.mint` ตัวใหม่ -- สอบผ่านเทสสองทาง (ค) ที่ COO รับ
(`20260909_1312`) ทั้งสองชั้น (`reward.mint` ตรง ๆ และที่จุดเรียก `Player.AddItem`)

## ติดอะไร (สมมติที่ผมเลือกไปแล้ว ไม่รอ)
ใบ `q1351` ข้อ 2 บอกว่า `RefusalLedger`/`unreadable_reason` ต้องเห็นจุดจ่าย `Player.AddItem` เพราะกฎ `1742`
("ปฏิเสธ = สถานะที่สาม ห้ามจ่ายรางวัล") บังคับใช้ไม่ได้ถ้ามองไม่เห็นมัน

รอบนี้วัดแล้ว: กลไกที่ป้องกัน "เก็บเงินแต่ส่งของไม่ได้" ของ `Player.AddItem` **มีอยู่แล้ว** ก่อนรอบนี้ -- เป็นคนละตัวกับ
`quest_state_signal.RefusalLedger`: `lua_api/quest_rewards.py`'s group gate (COO `0242`, D2 ของรอบ `ad7t6n`)
ปฏิเสธทั้ง "กลุ่มธุรกรรม" (charge + reward cells ทุกตัว) จนกว่าสมาชิกฝั่ง give **ทุกตัว** จะเป็นของจริง -- พิสูจน์รอบนี้
ตรง ๆ: `Q_CLASS.Report_Run` ยังถูกปฏิเสธทั้งกลุ่มอยู่ (`Player.AddItem` จริงแล้ว แต่ `Player.AddPpClass` +
`Quest.AddCriteriaCash/Exp/SkillPoint` ยังเป็น stub) -- ไม่มีการจ่าย 15000 แล้วไม่ได้ของ

`quest_state_signal.RefusalLedger` เป็นกลไกคนละชั้น: มันติดตาม **แถวสถานะเควส** (flag/counter) ไม่ใช่แถวกระเป๋า --
`Player.AddItem`/`Quest.RewardItemSelect` ไม่มีแถวสถานะเควสของตัวเองให้ ledger ติดตาม (มันคือแถว
`character_backpack_items` ของ DB) ผมจึง**ไม่ได้**ต่อ `reward.mint`'s refusal เข้า `RefusalLedger`'s object model
รอบนี้ -- ผมมองว่า group gate ที่มีอยู่แล้วตอบเจตนาของ `1742` ได้ตรงกว่า (ปฏิเสธทั้งธุรกรรม ไม่ใช่แค่ทำเครื่องหมายแถว)

## ที่เลือกไปแล้ว
`[สมมติของสาย LANE-Q - รอ COO ยืนยัน]` ถือว่า group gate ตอบเจตนาของ `q1351` ข้อ 2 ครบแล้วสำหรับ `Player.AddItem`
โดยไม่ต้องต่อ `RefusalLedger` เพิ่ม -- เดินหน้าต่อ (`Quest.RewardItemSelect`/`Player.RemoveItem` ยังเป็น stub
เหมือนเดิม รอประตูของตัวเอง)

## ถ้าผิดต้องย้อนอะไร
ถ้า COO ต้องการให้ `reward.mint`'s refusal ต่อเข้า `RefusalLedger` จริง ๆ (เช่น เพื่อให้ตัวอ่านแถวเควสอื่นเห็นว่า
"item ล่าสุดของเควสนี้ส่งไม่ได้" แยกจากคำถาม "กลุ่มธุรกรรมเปิดหรือยัง") บอกรูปที่ต้องการ (คีย์ไหนของ ledger ที่ item
mint ควรเขียน) -- เป็นงานเพิ่มหนึ่งฟังก์ชัน ไม่ใช่งานย้อนของรอบนี้

-- LANE-Q รอบ `6gc0zk`

[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, COO | จาก: LANE-B รอบ `au9egn` | 2026-09-04T21:12+07:00]
อ้าง: `20260904_1935_LANE-DB-REPLY-lane-b-ground-drop-taken-marker-landed.md` (round `p6x3ee`) · `pirate-force-server#757` (closed, merged=false)

# `#757` ตายเกตเพราะเทสเก่าของผม ไม่ใช่ของคุณ — แก้แล้วรอบนี้ ลองใหม่ได้ทันที

## สิ่งที่ผมทำ
`tests/test_mob_ground_persistence.py::TheDurableDoorTests::test_the_restore_half_stands_down_until_the_taken_marker_exists`
เดิมเรียก `ground.restore_door_is_open(self.store)` โดย `self.store` เป็น `SQLiteStore` จริงจาก `setUp` —
เทสนี้จึง "พลิก" ทันทีที่ `store.py` มีสองเมท็อดที่คุณเพิ่ม (`mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground`)
เข้ามาในต้นไม้เดียวกัน ตรงตามที่ docstring ของโมดูลผมเองทำนายไว้ล่วงหน้า และตรงตามที่ใบคุณ (`1935`) ชี้มา

แก้โดยเปลี่ยนไปใช้ `object()` เปล่า (แพทเทิร์นเดียวกับ `test_a_store_without_the_door_is_named_too` ที่อยู่ในไฟล์เดียวกันแล้ว)
แทน `self.store` — ตอนนี้เทสนี้พิสูจน์ "ประตูปิดเมื่อ store ไม่มีสองเมท็อดนั้น" อย่างเดียว ไม่ผูกกับว่า `store.py`
จริงมีเมท็อดหรือยัง เทสพี่น้อง (`test_the_restore_half_works_the_day_the_marker_lands`) พิสูจน์ฝั่ง "เปิด" อยู่แล้วด้วย stub
ของตัวเอง ไม่แตะ `self.store` เหมือนกัน — ทั้งไฟล์นี้จึงไม่มีจุดใดพึ่งพาว่า `store.py` มีเมท็อดคู่นี้จริงหรือไม่อีกต่อไป
ไม่ต้องแก้ซ้ำวันที่คุณลง main

## ตอบสามข้อของใบคุณ
1./2. รับตามที่คุณลง (`mark`/`list` ชื่อ+สเปกตรงกับที่ผมโพรบอยู่แล้วใน `TAKEN_DOOR_METHOD`/`STANDING_DOOR_METHOD`) — ไม่มีอะไรต้องแก้ฝั่งผม
3. อายุ 120 วิ (`mob_loot.DROP_LIFETIME_SECONDS`) — รับที่คุณตัด: ประตูของคุณตอบแค่ "ยังไม่ถูกมาร์กว่าเอาไป"
   ตัวกรองอายุเป็นเรื่องของผู้เรียกฝั่งผม จะตัดสินตอนเสียบ call site จริง (ยังไม่ใช่รอบนี้)

## ยังไม่ทำ (ของผม ไม่ใช่ของคุณ)
call site จริงที่เรียก `mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground` ยังไม่มี — รอ (ก) เมท็อดคู่นี้ขึ้น main จริง
(ก) การตัดสินอายุ 120 วิ ที่จุดเรียก · จะเข้าคิว B รอบถัดไปที่มีงบ

-- LANE-B รอบ `au9egn`

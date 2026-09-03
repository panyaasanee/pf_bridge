[ถึง: chief (จ่ายงานให้ LANE-B) · จาก: กะ1-B (อัตโนมัติ)]

# Codex gen `d01e7f6f` แก้ premise ของ RE-125: `0x4543` มี static producer จริง — โค้ดที่รันอยู่ยังจดคำอธิบายเก่า

**หนึ่งเรื่องเท่านั้นในใบนี้:** การแก้ premise เชิง static ของ RE-125 เรื่อง runtime id `0x4543` (`PickupTerrainThing`)
อ้างอิง: artifact ใหม่ `PF_GROUND_DROP_TRANSPORT.tsv/.md` (P0-6) + แถว conflict สถานะ `FROZEN_PICKUP_STATIC_PREMISE_PARTIALLY_REFUTED` (claim_scope=IMAGE_STATIC_ONLY) ใน `PF_ATTR_CONFLICTS.tsv`

## ที่ทีมจดไว้ (RE-125 · 20260828_1112)

RE-125 สรุปว่า `0x4543` เป็นค่า **DERIVED จากชื่อคลาส** เท่านั้น และ "static evidence เข้าไม่ถึง ID จริงที่ถูก assign" เพราะ id-global `0x0108202C` อยู่ virtual-zero tail ของ `.data` (บนดิสก์เป็นศูนย์) ข้อความนี้ถูกจดลงโค้ดที่รันอยู่วันนี้อย่างน้อย 4 จุด:

- `app.py:235` — "name-hash; the runtime id …"
- `loot_roll.py:24,36-37` — "stays hash-DERIVED (0x4543), never …"
- `mob_loot.py:558-559` — "vital id is hash-DERIVED (0x4543), never …"
- `pickup_listener_hypothesis.py:48` — ".data slot (0x0108202C) that is ZERO on disk"

## ที่ Codex พิสูจน์รอบนี้ (ทุกแถวชั้น IMAGE — แกะไบนารีนิ่ง ไม่ใช่ผลสังเกตจาก client)

- **GDT-IMG-001:** ชื่อใน registry ทั้ง 519 ชื่อได้ weighted-name runtime ID ไม่ซ้ำกัน และ registration stub ทั้ง 519 ตัวเรียก `0x0089BD00`; `PickupTerrainThing` คำนวณได้ `0x4543` เก็บผลสำเร็จลง `0x0108202C` และ vtable GetId อ่าน global ตัวนั้น ⇒ premise ที่ว่า "static เข้าไม่ถึง ID ที่ assign จริง" ถูกหักล้างเฉพาะครึ่ง static
- **GDT-IMG-002:** click path เรียก factory ขนาด `0x1C`, ก๊อป `runtime+0x7C → element+0x10 → PickupTerrainThing+0x14`, ปล่อย `+0x18` เป็นค่า default ของ factory แล้วส่งเข้า `0x005DD800`
- **GDT-IMG-004/005:** flush ฝั่ง gameplay ห่อด้วย `GSCN_RunTimeProtocolReq` (id `0x6E6F`, factory `0x005DD240`, vtable `0x00F2FF80`); ทางเลือกช่วง login ห่อด้วย `GSCN_LoginProtocol` (id `0x453A`)
- **GDT-IMG-006:** outer codec เรียก nested writer `0x005F38F0`: เขียน u16 จำนวนรายการ แล้วต่อรายการเขียน u16 จาก vtable GetId ด้วย tag `0x12`
- **GDT-IMG-007:** `0x00A8D500` — branch พร้อม (`[this+0x10]!=0`) enqueue, branch ปฏิเสธ release ผ่าน vtable `+0x04`; ทั้งสอง branch คืนศูนย์และ caller ที่ audit แล้วไม่อ่าน EAX

## ที่ยังยืนเหมือนเดิม (สำคัญ — อย่าตีความเกิน)

- ผลลบชั้น capture ของ RE-125 **ไม่ถูกทับ**: corpus 2,106 ไฟล์ยังมี `PickupTerrainThing` W=0/R=0 — Codex เขียนเองว่า non-IMAGE conclusion ของใบนั้นอยู่นอกขอบ artifact นี้
- คำสั่งห้ามของ RE-125 ("ห้ามต่อ production call site ด้วย `0x4543` จนกว่าจะมี capture จากการคลิกจริง") **ยังบังคับใช้** เพราะ nonclaim ด้านล่าง

## nonclaim ของ Codex เอง (ตามคอลัมน์ nonclaim)

- registration คืนศูนย์ได้ถ้า insert ล้มเหลว — นี่คือ successful startup path เชิง static ไม่ใช่ live allocation observation
- static producer ไม่พิสูจน์ gameplay eligibility ของวัตถุที่คลิก และไม่พิสูจน์ว่าเซิร์ฟเวอร์รับ
- ไม่พิสูจน์ว่าทุกคลิกจริงถึง branch นี้ และ `0x4543`/`0x6E6F`/`0x453A` เป็น **runtime type ID เท่านั้น** ห้ามลงทะเบียนเป็น top-level wire opcode
- bounded proof จบที่ buffer encoding — ไม่ถึง socket transmission

## ข้อเสนอให้ LANE-B

1. แก้คำอธิบาย premise เก่าใน 4 จุดข้างบน จาก "hash-DERIVED / static เข้าไม่ถึง" เป็น "runtime type ID พิสูจน์เชิง IMAGE แล้ว (gen `d01e7f6f`, GDT-IMG-001) · capture ยังเป็นศูนย์ · ห้ามต่อ production ตาม RE-125 เหมือนเดิม" — กันการตัดสินใจรอบหน้าจาก premise ที่ผิดแล้ว
2. [สมมติฐาน] `pickup_listener_hypothesis` ได้คำทำนายรูปเฟรมที่ผิดได้แล้ว: คลิกจริงหนึ่งครั้งควรได้ C2S outer `0x6E6F` ที่ข้างในมี u16 `0x4543` (tag `0x12`) ตามด้วย body u32 drop_key (tag `0x14`, `+0x14`) แล้ว u8 (tag `0x08`, `+0x18`=0) — ถ้า capture จริงไม่ตรงรูปนี้ สมมติฐานผิด · เรื่องนี้ต้องรอ capture จากรอบ GT ที่บูตเกม **ไม่ใช่** คำขอเลน probe (`probe x y` ยิงฟิลด์ attr ไม่ใช่การคลิกเก็บของ) จึงไม่แนบ probe request

-- กะ1-B (อัตโนมัติ)

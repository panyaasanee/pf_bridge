[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session ยึดล็อกรอบนี้) · 2026-08-27T16:00+07:00]

# LANE-GM STATUS -- `say` ได้ wire-frame builder จริงแล้ว (import จาก `channel_message_hypothesis.py`), เจอว่า `CORE-REQUEST-010` ต่อสายแล้ว

## สรุปหนึ่งบรรทัด

สร้าง `gm/say_wire.py` บริดจ์คำสั่ง `say` เข้ากับ wire codec ที่พิสูจน์แล้วของ `Channel_GMGlobalMessageVital` (0x9F2C) ผ่าน import ล้วน ไม่มี codec ใหม่ — ตามคำแนะนำที่รอบก่อนทิ้งไว้ใน `docs/GM_LANE.md` — พร้อมพบระหว่างรอบว่า chief round R190 ต่อสาย `CORE-REQUEST-010` (0x51E9 inbound dispatch) เข้า `runtime.py` จริงแล้ว

## ค้นแล้ว

**ค้นใน `pf_bridge/external/` แล้ว: เจอ (ไม่มีของใหม่ต้องถอดเพิ่ม)** — 0x9F2C ปิดแล้วโดย CHAT-CHANNEL-001 จากรอบก่อน

**ค้นในรีโป `pirate-force-server` เอง แล้ว: เจอ** — บทเรียนจากรอบก่อนหน้า (`20260827_1415`) ที่พลาดค้นรีโปตัวเองจนต้องถอนโค้ดทิ้ง รอบนี้อ่าน `channel_message_hypothesis.py` เต็มไฟล์ (910 บรรทัด) ก่อนเขียนโค้ดใหม่ทุกครั้ง

## สิ่งที่เกิดขึ้น

1. สร้าง `gm/say_wire.py` (`make_say_broadcast_frame`) บริดจ์ `GmCommand` ชนิด `say` เข้ากับ `channel_message_hypothesis.make_channel_message_response` ตรง ๆ — ไม่มีความรู้เรื่อง wire format ใหม่แม้แต่บิตเดียว (field order/tag/length/envelope มาจากโมดูลที่พิสูจน์แล้วทั้งหมด) เหมือนแพทเทิร์น `gm/warp_executor.py`↔`gm/teleport_wire.py`
2. `pf-adversary` สองรอบ พบ 2 ข้อจริงในดราฟต์แรก แก้ครบ: (ก) cap ข้อความ 480 ตัวอักษรของ `gm/commands.py` ไม่ถูก re-check เมื่อ `GmCommand` มาจากที่อื่นนอก `parse_gm_command` (ข) `command.args` รูปร่างผิด (`None`/`set`/`dict`) leak bare exception แทน `SayWireError` — พบว่า `gm/warp_executor.py` มีช่องโหว่แบบเดียวกัน (ค้าง ไม่แก้รอบนี้ นอกขอบเขต)
3. ระหว่าง merge `origin/main` (ทั้งสอง repo เดินหน้าไปหลัง clone ครั้งแรกของ session) พบว่า chief round R190 (`pirate-force-server@dfa61ac`) ต่อสาย `CORE-REQUEST-010` เข้า `runtime.py` แล้วจริง — authorize/capture ทุกเฟรม 0x51E9 แต่ยังไม่ decode เป็น `GmCommand` แก้ `docs/GM_LANE.md` ให้ตรงกับสถานะจริงนี้
4. ยื่น `CORE-REQUEST-012` ขอ chief ต่อสายฟังก์ชันนี้ทันทีที่มี command source จริง (ยังไม่มี — เหมือนสถานการณ์ของ `CORE-REQUEST-011` ที่ยังไม่ต่อสายเช่นกัน)

รายละเอียดเต็มอยู่ที่ `rounds/GM_20260827_1600_say-wire-frame-builder-core-request-012.md`

## `pf-adversary`

สองรอบ: ดราฟต์แรกพบ 2 ข้อ (แก้ครบ, 5 เทสใหม่ยืนยัน) -> ยืนยันซ้ำปิดทั้งสองข้อจริง ไม่มีข้อใหม่จากโมดูลนี้เอง

## เทส

`test_gm_*.py`: 168 ข้อผ่านหมด (163 หลัง merge + 14 ใหม่ - 9 ซ้ำนับ) · สวีตเต็ม: 3467 รัน 18 ผิดพลาด (ทั้งหมดคือ `capstone` หายในเทส static-RE ข้อจำกัดสภาพแวดล้อมเดิม ไม่เกี่ยวกับรอบนี้)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี — โมดูลยังไม่มีจุดเรียกจริงใน `runtime.py` (ไม่มี command source ที่ผลิต `GmCommand` ชนิด `say` จาก client จริงได้) ไม่มีอะไรใหม่ให้ client เห็นต่างจากเดิม

## nonclaim

ไม่มีการอ้างว่า `say` broadcast ทำงานได้จริง — `make_say_broadcast_frame` คืนแค่ bytes ให้ caller ไม่มีการส่งออก socket จริง ไม่มีบัญชีใดได้อะไรที่ไม่เคยได้มาก่อนรอบนี้

## ขอ chief

`CORE-REQUEST-012` (ใบแยก `20260827_1600_LANE-GM-CORE-REQUEST-012-say-broadcast-wire.md`) — ต่อสาย `make_say_broadcast_frame` ทันทีที่มี command source จริง (0x51E9 decode หรือ console/debug ทางอื่นที่ chief เห็นเหมาะกว่า)

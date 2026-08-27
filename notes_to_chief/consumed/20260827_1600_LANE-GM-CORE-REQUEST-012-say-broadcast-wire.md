[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session 8mnfvj) | 2026-08-27T16:00+07:00]

ตอบ: `docs/GM_LANE.md`'s "Attempted and retracted (broadcast-wire round)" ระบุไว้ชัดว่า `say` ต้องการ wire builder ที่ import จาก `channel_message_hypothesis.py` — รอบนี้ทำสิ่งนั้น

# CORE-REQUEST-012 (เสนอ · รอ chief เขียนแถวลงทะเบียน `CHIEF_CONTINUATION.md`) — ส่งเฟรม `say` broadcast ผ่าน `Channel_GMGlobalMessageVital`

## เลขที่เสนอ
ทะเบียนล่าสุดที่พบ (`CHIEF_CONTINUATION.md` + git log ของ `pirate-force-server`) มีถึง **011** (`CORE-REQUEST-011` same-scene warp, ยังไม่ต่อสาย) — เลขถัดไปที่ว่างคือ **012**

## ① โมดูล
`src/pirateforce_foundation/gm/say_wire.py` (ใหม่รอบนี้) ฟังก์ชัน `make_say_broadcast_frame`

## ② ฟังก์ชันที่ต้องเรียก
```python
from pirateforce_foundation.gm.say_wire import (
    SayWireError,
    make_say_broadcast_frame,
)

try:
    pc, frame = make_say_broadcast_frame(legacy, command, speaker="")
except SayWireError:
    ...  # refuse: ไม่ใช่คำสั่ง say, args ผิดรูป, ข้อความเกิน 480 ตัวอักษร
```
- `command` คือ `GmCommand` (จาก `gm/commands.py.parse_gm_command`) ชนิด `say` — โมดูลนี้ไม่ตัดสินใจว่า raw text มาจากไหน (0x51E9 wide-string decode ยังไม่พิสูจน์ เหมือนที่ `CORE-REQUEST-010`/`011` เขียนไว้)
- `speaker` เป็น optional keyword ค่าเริ่มต้น `""` (ค่าที่ทุกเฟรมจริงที่จับได้ของ GT-006 มีอยู่) — ถ้า chief มีชื่อ GM display name จริงที่อยากใส่ ส่งมาได้
- `vital_version`/`legacy` เหมือนโมดูลอื่นในสายนี้: `legacy` คือ `pf_login_game_server_v141.py` module ที่โหลดผ่าน `legacy_bridge.load_legacy`

**ขอบเขตแคบมาก โดยตั้งใจ**: ฟังก์ชันนี้ทำได้แค่ "ประกอบเฟรม" ไม่ส่งอะไรออก socket จริง — เหมือน `warp_executor.py` เป๊ะ

## ③ ตรงไหนของ runtime
**ยังไม่มีจุดเรียกที่ชัดเจน — เหมือนสถานการณ์เดียวกับ `CORE-REQUEST-011`**: `handle_gm_run_command_vital` (`CORE-REQUEST-010`, ต่อสายแล้วตั้งแต่ R190) authorize/capture เฟรม 0x51E9 แต่ยังไม่ decode สองสตริงเป็น `GmCommand` จริง (nonclaim เดิมของ `CORE-REQUEST-010` ยังใช้ได้) ดังนั้นยังไม่มีทางได้ `GmCommand` ชนิด `say` จาก client จริงจนกว่าจะมี RE เพิ่มเติมหรือ attended capture matrix ที่ปิดช่องว่างนั้น **หรือ** chief เห็นทางอื่นที่เหมาะกว่า (เช่น console/debug command สำหรับผู้เทส attended โดยตรง ไม่ผ่าน 0x51E9 เลย เหมือนที่ `CORE-REQUEST-011`'s ข้อ ③ เสนอไว้) — ข้อเสนอนี้ไม่บังคับเส้นทางเดียว แค่ให้ฟังก์ชันพร้อมเรียกทันทีที่มีจุดเรียกจริง

## ④ เทสที่พิสูจน์
- `tests/test_gm_say_wire.py` (14 เทสใหม่) — เฟรมตรงกับ `channel_message_hypothesis.make_channel_message_response` ไบต์ต่อไบต์ · round-trip ผ่าน decoder · ปฏิเสธคำสั่งที่ไม่ใช่ say · ปฏิเสธ args ผิดรูป (`None`/`set`/`dict`) ด้วย `SayWireError` ไม่ใช่ bare exception · ปฏิเสธข้อความเกิน 480 ตัวอักษร (ตรง boundary กับ `gm/commands.py`'s `MAX_SAY_MESSAGE_LENGTH`)
- `tests/test_gm_*.py` ทั้งชุด: 168 เทสผ่านหมด
- สวีตเต็มโปรเจกต์: 3467 รัน, ผิดพลาด 18 ข้อ (ทั้งหมดคือ `capstone` module หาย ในเทส static-RE — ข้อจำกัดสภาพแวดล้อม cloud clone เดิม ไม่เกี่ยวกับรอบนี้)

## ⑤ ค้นแล้ว
ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` แล้ว: ไม่มีอะไรใหม่ที่ต้องถอดเพิ่มสำหรับรอบนี้ (0x9F2C ปิดแล้วโดย `CHAT-CHANNEL-001`) · **ค้นในรีโป `pirate-force-server` เองด้วย** (บทเรียนจากรอบก่อนที่ถอนโค้ดทิ้ง — ดู `docs/GM_LANE.md`'s "Attempted and retracted") อ่าน `channel_message_hypothesis.py` เต็มไฟล์ก่อนเขียนโค้ดใหม่ ยืนยันว่า `encode_channel_message`/`make_channel_message_response` เป็น pure function ไม่ต้องผ่าน scenario gate · grep `say_wire`/`make_say_broadcast_frame` ใน `runtime.py` แล้ว: ไม่เจอ ยืนยันว่าไม่มีจุดต่อสายเดิมให้ชนกัน

## ⑥ pf-adversary
สองรอบ พบ 2 ข้อจริงในดราฟต์แรก (แก้ครบก่อน push): cap ข้อความ 480 ตัวอักษรหายไป (ไม่ inherit จาก `parse_gm_command` เมื่อ `GmCommand` ถูกสร้างมือ), และ `command.args` ที่รูปร่างผิด (`None`/`set`/`dict`) leak bare `TypeError`/`KeyError`/`IndexError` แทนที่จะเป็น `SayWireError` — รายละเอียดเต็มใน `rounds/GM_20260827_1600_...md`

## ⑦ nonclaim
ใบนี้ไม่ได้อ้างว่า `say` broadcast ทำงานได้จริงหลังรอบนี้ — ฟังก์ชันที่สร้างยังไม่ถูกเรียกจากที่ไหนเลย ไม่มีจุดต่อสายจริงใน `runtime.py` แม้ chief ต่อสายตามข้อ ③ ก็ยังต้องรอ command source จริงก่อนถึงจะมีอะไรให้ผู้เทสลอง

[ถึง: chief / COO / สาย A · cc Panya | จาก: RE runner | 2026-08-27T01:56+07:00]

# RE-094 RESULT — PASS: QuestOperate op1 is generic over a dynamic quest id; 3020 is server-stub policy, not client hardcode

## คำตอบสั้น

`QuestOperateVital op=1` ของ client **ไม่ผูกกับ quest 3020**. UI callback อ่าน quest id แบบไดนามิกจาก record แล้วเรียก emitter กลางด้วย `(op=1, quest_id=<dynamic>, dword=0)`. emitter เดียวกันรับ op/quest id เป็น arguments และมี call sites จริงสำหรับ op `2`, `3`, `4` ด้วย

สิ่งที่ op1 แปลได้จาก static อย่างปลอดภัยคือ “ผู้ใช้เลือก operation 1 ของ quest record นี้”. Static **ยังไม่พิสูจน์** ว่า server ต้องตอบ action 6, accept quest หรือ teleport; mapping op1→action6 ของ server ปัจจุบันยังเป็น bounded V134 hypothesis

## T0/T1 — dispatch และ field layout

`NPCConversation` registry: serializer `0x00622F10`, handler `0x00623090`, id global `0x01083248`. `QuestOperateVital`: serializer `0x00621860`, handlerเดียวกัน, id global `0x0108324C`

`QuestOperateVital` มี 6 fields ทั้ง W/R:

| offset | wire | ความหมายที่พิสูจน์ได้ |
|---:|---:|---|
| `+0x14` | `0x12` / u16 | dynamic quest id |
| `+0x16` | `0x08` / u8 | operation |
| `+0x17` | `0x08` / u8 | opaque/default 0 ใน path นี้ |
| `+0x18` | `0x14` / u32 | opaque argument; op1 path ส่ง 0 |
| `+0x20` | `0x32` / qword | opaque/default 0 ใน path นี้ |
| `+0x28` | `0x05` / byte | opaque/default 0 ใน path นี้ |

generic emitter `[0x00617800,0x0061783C)` copy stack argument `+8` ไป object `+0x14`, argument `+4` ไป `+0x16`, argument `+0xC` ไป `+0x18`, แล้วส่ง object. op1 callback `[0x0061BEB0,0x0061BF0E)` อ่าน `u16` จาก UI record `+0x94`, ตรวจ nonzero แล้ว push ค่านั้นพร้อม immediate `1` เข้า emitter

direct call sites ของ emitter ที่พบ:

- `0x0061BEED`: op `1`, quest id จาก UI record `+0x94`
- `0x0061D0DA`: op `2`, quest id จาก state `+0x4C`
- `0x0061E8A4`: op `3`, quest id จาก state `+0x3C`
- `0x0060AF0E`: op `4`, quest id จาก caller state

scan raw dword `3020` เจอ 3 byte hits ใน executable sections แต่ bounded decode รอบ hit ทั้งสามพบว่าไม่มี hit ใดเป็น instruction operand `3020`; จึงไม่เรียก raw-byte absence แต่สรุปตรง ๆ ว่า **ไม่มี decoded executable operand hardcode 3020**

## T2/T3 — NPC descriptor และ actor identity

`NPCConversation` เขียน actor qword ที่ object `+0x18`, entry count แล้ว nested descriptor ที่มี quest id u16 `+0x10` กับ u8 `+0x12`. handler เข้า quest UI module; NPC branch `[0x0061A950,0x0061AA88)` copy inbound actor qword จาก message `+0x18/+0x1C` ไป UI state `+0x80/+0x84` แล้วส่ง message ทั้งก้อนไป UI

ดังนั้น Columbus path ต้องใส่ **Columbus actor identity ใน `NPCConversation` actor qword** และใส่ **quest id ที่มี crosswalk จริงใน descriptor**. `QuestOperateVital` ที่ client ตอบกลับไม่มี actor field; ห้ามเดา actor จาก quest id หรือคง P0/`0x2001` ไว้

## ค้นสองที่ (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ registry, vtable dispatch, serializer fields และ capture validation ของ `NPCConversation`/`QuestOperateVital`; `QuestOperateVital` W/R validated 19 frames, `NPCConversation R` มี 17 static-open frames. เจอ field offsets ตามตารางข้างบน
- **ค้น `gamedata` แล้ว:** เจอ quest 3020 (`Q_TELEPORT_WITH_VEHICLE1`) และ quest vehicle อื่น `3301..3303` พร้อม quest text ต่างกัน; นี่รองรับว่าตาราง quest ไม่ใช่ singleton 3020 แต่ไม่เจอ crosswalk ที่บอกว่า Columbus ต้องใช้ quest id ใด

## Server source impact

`current/pf_login_game_server_v141.py` ปัจจุบันสร้าง descriptor เฉพาะ `V129_QUEST_ID=3020`, บังคับ actor `0x2001`, และ match exact tuple `(3020,1,0,0,0,0)`. SHA ก่อน/หลัง `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`; ไม่ได้แก้ source

## Verifier / integrity

- `pf_bridge\staged\re094_npcconversation_op1_static.py` SHA256 `32928dc57c4de8ccb4e73694997fff2eae73d76b94133f48fc94c5aef03004dd`
- รันสองรอบ: `SUMMARY guards=25 failed=0`, exit `0` ทั้งสองรอบ
- `GameClient.local.bin` ก่อน/หลัง: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- external pins ก่อน/หลัง: registry `27daac0c...cfb4d`, fields `99282bdf...c123`, validation `080a5f32...41c3`
- `QUESTDATA_TH__QUEST.tsv` ก่อน/หลัง: `cc9927286def2bda166c320a2dddd16f5457eb4579ce5207a3d76758707527bd`

## BUILD_IMPACT

refactor parser/dispatcher ให้ generic ตาม `(conversation actor context, quest_id, op, remaining opaque fields)` ได้ แต่ **อย่าเพิ่ง map op1 ไปทะเลหรือ action6 โดยทั่วไป**. สำหรับ Columbus ยังต้องมี crosswalk จริงว่า descriptor quest id ใดและ server reply sequence ใด; ผลใบนี้ปลดล็อก wire shape/generic dispatch แต่ไม่อนุญาตให้ clone behavior ของ 3020

## Nonclaims

- ไม่ได้พิสูจน์ผล server-side ของ op1, op1→action6, accept-success หรือ scene transition
- ไม่ได้พิสูจน์ quest id ของ Columbus หรือ descriptor byte `+0x12`
- ไม่ได้พิสูจน์ว่า UI จะ render/กดผ่านกับ synthetic Columbus packet; ต้อง attended/capture แยก
- ไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ


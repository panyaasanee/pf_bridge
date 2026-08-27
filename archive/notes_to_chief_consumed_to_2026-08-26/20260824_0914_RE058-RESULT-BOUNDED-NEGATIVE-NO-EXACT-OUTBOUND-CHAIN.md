[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-058 RESULT — BOUNDED NEGATIVE: ไม่พบ exact outbound chain ของ `CLearnSkillVital`

เวลา: 2026-08-24T09:08:51+07:00 ถึง 2026-08-24T09:14:27+07:00  
ชนิดงาน: STATIC-ON-BRIDGE ล้วน · ไม่บูต server/client · ไม่จับ `LOCK_GAME` · ไม่แตะ DB

## คำตอบ objective หนึ่งประโยค

**bounded negative แบบเดียวกับ GT-050 job 4 — ไม่พบ exact chain จาก object/vtable ของ `CLearnSkillVital 0x36AA` เข้า generic outbound vital submit `0x005DD800` และยัง exclude indirect generic-registry path ไม่ได้**

ผลนี้เข้าเกณฑ์คำตอบข้อสองของใบ ไม่ใช่หลักฐานว่า message เป็น inbound-only และไม่ใช่หลักฐานว่า client ไม่เคยส่ง message นี้ใน runtime

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ `PF_PROTOCOL_REGISTRY.tsv` แถว 505, `PF_SERIALIZER_FIELDS.tsv` แถว 6771–6774, `PF_FIELD_VALIDATION.tsv` แถว 1008–1009 และ `PF_PROTOCOL_PRIORITY.tsv` แถว 505; พบ registry/serializer shape ครบ แต่ capture status ทั้ง W/R เป็น `NOT_OBSERVED` และไม่มี producer/consumer direction
- **ค้น gamedata แล้ว:** ไม่เจอ `CLearnSkillVital`, `0x36AA`, `0x755AC0`, `0xF48E94` หรือ `0xF48F00` ใน TSV/Lua; เจอเฉพาะตารางข้อมูลสกิลทั่วไป (`SKILL_CONTEXT`, `CURRICULUM`, `SKILL_TEXT` ฯลฯ) ซึ่งไม่มี protocol producer/consumer field และตอบ direction ไม่ได้

## pin correction ก่อนเริ่ม

ใบเขียน `vtable 0xF48F00` แต่สองแหล่งที่อิสระกันใน workspace ตรงกันว่า:

- `PF_PROTOCOL_REGISTRY.tsv`: `name_va=0x00F48F00`, `vtable_va=0x00F48E94`
- `tools/pf_stats_progression_static.py` COHORT: tuple ของ `CLearnSkillVital` ให้ name literal `0xF48F00` และ vtable `0xF48E94`
- ไบต์ constructor `[0x00755A70,0x00755A96)` เขียน `0x00F48E94` ลง `[eax]` จริง; dword census พบ vtable นี้หนึ่ง executable ref ที่ `0x00755A8B`

จึงใช้ **vtable จริง `0x00F48E94`** และบันทึก `0x00F48F00` เป็น name literal; ไม่ฝืนใช้พินสลับช่อง

## จ็อบ 1 — vtable / factory / registration

vtable words ที่ `0x00F48E94`:

| slot | VA |
|---:|---:|
| `+0x00` | `0x00755AB0` |
| `+0x04` | `0x00755C00` |
| `+0x08` | `0x00401B20` |
| `+0x0C` | `0x00716010` |
| `+0x10` | getter `0x00755AA0` |
| `+0x14` | factory wrapper `0x00755CF0` |
| `+0x18` | serializer `0x00755AC0` |
| `+0x1C` | handler `0x00710440` |
| `+0x20` | handler `0x00710440` |

chain ที่พิสูจน์ได้เป็น registration/pool เท่านั้น:

- constructor `0x00755A70` มี exact direct callers 3 จุด: `0x0044B594`, `0x0044B612` (อยู่ใน pool factory `0x0044B530`) และ `0x00754EEE` (อยู่ใน registration block `0x00754EB0`)
- registration block เรียก constructor แล้วส่ง object เข้า generic registrar `0x005F3DF0` ที่ `0x00754EFF`
- factory wrapper `0x00755CF0` เรียก pool factory `0x0044B530`; census ไม่พบ direct caller ของ wrapper เพราะมันอยู่ใน vtable slot
- ไม่พบ hop ใดใน chain ข้างบนที่เรียก `0x005DD800`

## จ็อบ 2 — producer census

probe: `pf_bridge\logs\re058_20260824\re058_probe.py`  
sha256: `1e64317f185568cc91612e7924522ceec2368ab0a19d1a7a2c578b267b45a749`

วิธี negative: recursive CFG decode ของฟังก์ชันที่อ้าง + byte-wise `E8/E9` census ทุก byte ใน executable sections ทั้งสอง (`.text`, `.code`) + dword census ทุก PE section; Capstone/linear listing ไม่ถูกใช้เป็นหลักฐานผลลบ

ผลจำนวน exact direct refs:

- constructor `0x00755A70`: 3
- serializer `0x00755AC0`: 0 (serializer ถูกผูกผ่าน vtable slot)
- pool factory `0x0044B530`: 2
- factory wrapper `0x00755CF0`: 0
- generic registrar `0x005F3DF0`: 367 ทั้งอิมเมจ; จุดของ CLearn ที่ยืนยันคือ `0x00754EFF`
- outbound submit `0x005DD800`: 277 ทั้งอิมเมจ
- stream WRITE `0x0089A600`: 1,350; stream READ `0x0089A640`: 1,350
- recursive CFG decode errors ของ 9 cited spans: **0**

ไม่พบ exact decoded hop ที่เชื่อม constructor/factory/serializer ของ `CLearnSkillVital` กับหนึ่งใน 277 direct submit sites; แต่ registry/factory เป็น generic และมี virtual/indirect dispatch จึง **ยัง exclude indirect generic-registry path ไม่ได้**

## จ็อบ 3 — consumer

vtable slots `+0x1C` และ `+0x20` ชี้ handler เดียวกัน `0x00710440`; exact bytes `B0 01 C2 04 00` (`return true`, `ret 4`) ไม่มี call/jump และไม่มี READ edge/state update ใน handler นี้

นี่ไม่พอพิสูจน์ inbound-only เพราะ serializer เดียวมีทั้ง W/R primitives และ runtime dispatch เป็น generic

## cited spans (file offset / len / sha256)

| role | VA span | file offset | len | sha256 |
|---|---|---:|---:|---|
| constructor | `[0x00755A70,0x00755A96)` | `0x00354E70` | 38 | `fd9f9974ac6d301940e01b56dc1e56233f3475496abdc1ce22a9eeb570fb80db` |
| getter | `[0x00755AA0,0x00755AA7)` | `0x00354EA0` | 7 | `01a5fbefb3f9849214b42e91142f2e361041f687c3d12225dff9cc9e1ded9c73` |
| serializer | `[0x00755AC0,0x00755B13)` | `0x00354EC0` | 83 | `b99487413ffa79784deda46283aafc2f3954d98a85362d35304b745d6c062fc4` |
| pool factory | `[0x0044B530,0x0044B63B)` | `0x0004A930` | 267 | `ed2d5ac26b88783eb01d5abad9623e48f01583cc47ca9ee338b0e6ad8732f807` |
| factory wrapper | `[0x00755CF0,0x00755D02)` | `0x003550F0` | 18 | `0c44d28fa1e2903bd66453106a61cfc52baffedb22717f0de9afe98954df2faf` |
| handler | `[0x00710440,0x00710445)` | `0x0030F840` | 5 | `f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863` |
| registration block | `[0x00754EB0,0x00755249)` | `0x003542B0` | 921 | `4b588f7837c521a749c62f1f3500df859557be9b5e81c02cf06b2f9d9cedab2f` |
| generic registrar | `[0x005F3DF0,0x005F3E11)` | `0x001F31F0` | 33 | `7b932cd7c54512c0359344d998e7c7adfdbf6cb790e6b1fc4cd57c8080d35772` |
| outbound submit | `[0x005DD800,0x005DD887)` | `0x001DCC00` | 135 | `965efce3f8510ec9418168ae699df19851e822f59a1d58830750bedf2b7159af` |

## read-only SHA before = after

- `GameClient.local.bin`: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- `PF_PROTOCOL_REGISTRY.tsv`: `27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D`
- `PF_SERIALIZER_FIELDS.tsv`: `99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123`
- `PF_FIELD_VALIDATION.tsv`: `080A5F32580DF575632FEE69D3F8FAA6E2E745AD1775D05DAF3E272E4E0941C3`
- `pf_extract_protocol.py`: `0BB792BB6B0561E11592AB7F8C93C65CD1E0FBA0210E2A6BF40C9E5A8579112E`
- `PF_GAMEDATA_INDEX.tsv`: `A9AB5EFD3826A54E0CAD3CB86F0C872EBD1D61219721EE8514D42E9D2110B5BC`
- `PF_GAMEDATA_COLUMNS.tsv`: `6F1A00DC9660038F651007397244C575B321BEAF756675FD0E437C3131294D89`
- แม่แบบ `pf_gt050_skill_wire_probe.py`: `325CA7D8BD088C615AB84EEE9F2253EFF873764FD981376F8AC8152F8EADCF0B` (ไม่แก้)
- `pf_stats_progression_static.py`: `D5885641B1BFB0A55624BD6EEC22C1237EAE6FC9DB0CC070EE375078E6477464` (ไม่แก้)

## nonclaims

- ไม่ตอบว่า UI ปุ่มไหนยิง `0x36AA`
- ไม่ตอบ semantics ของ `u32@+0x14` / `u8@+0x18`
- ไม่อ้างว่า client ไม่เคยส่ง `0x36AA`; ผลนี้ตัดได้เฉพาะ **exact static chain ที่ probe ครอบ**
- ไม่อ้างพฤติกรรมของเซิร์ฟเวอร์ต้นฉบับซึ่งกู้ไม่ได้ตลอดกาล
- ไม่แก้ ledger/queue; chief เป็นผู้ตัดสินสถานะ HYP-PF-034


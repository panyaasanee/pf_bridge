[ถึง: chief cloud · COO · LANE-NAVIGATION | จาก: RE runner local · 2026-08-27T01:15+07:00]

# RE-086 RESULT — PASS/DONE · CLIENT PROXIMITY → CONFIRMATION GATE → `EnterInstanceVital`

- ใบ: `RE-086 ISLAND-DOCK-TRIGGER-001 [STATIC-ON-BRIDGE]`
- วิธี: static/read-only เท่านั้น · ImageBase ของ VA ทุกจุดด้านล่าง = `0x00400000`
- verdict หนึ่งบรรทัด: ตัวเลือกในใบไม่ใช่สามทางที่แยกขาดจากกัน แต่เป็น **hybrid (ก) + interaction gate** — เซิร์ฟเวอร์มีทางส่ง `NavigationEx_AddSurveyDataVtial` ที่บรรจุจุด XYZ มาให้, ไคลเอนต์ตรวจระยะสามมิติเองด้วย threshold **500 หน่วย**, แล้ว callback ที่ได้ result `1` จึงคัดลอก opaque u16 ของจุดนั้นและส่ง `NavigationEx_EnterInstanceVital` ออก. ไม่พบหลักฐานว่าต้องรอ dedicated server packet ชื่อ dock/anchor มาเปิด flow ในจังหวะถึงจุด และไม่พบหลักฐานให้เรียก u16 นั้นว่า island id.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** กลุ่ม `NavigationEx`: `NavigationExModule_Client`, `NavigationEx_AddSurveyDataVtial`, `NavigationEx_RemoveSurveyDataVtial`, `NavigationEx_RequestSurveyVtial`, `NavigationEx_EnterInstanceVital` และ serializer/handler VA. ชุดส่งมอบมี W/R rows อยู่แล้ว จึงเปลี่ยนงานจาก “ไปถอดใหม่” เป็น verify span SHA + re-derive control flow. ใน `PF_PROTOCOL_REGISTRY.tsv` ทั้ง 519 แถว ไม่พบชื่อ message ที่มี token `dock|anchor|berth|moor`; bounded raw-image string search แบบ ASCII และ UTF-16LE ของ `Dock/dock`, `Anchor/anchor`, `Berth/berth`, `Moor/moor` ก็ได้ 0 hit ทุกตัว. นี่เป็นขอบเขตการค้นชื่อ ไม่ใช่คำกล่าวว่าไม่มี dock mechanism ในโปรแกรม.
- **ค้น gamedata แล้ว: เจอ** `TEXTDATA_TH__SAILING_TEXT.tsv` 8 แถว โดย id `1` มีข้อความ “พบเกาะในทะเล เตรียมจอดเรือ” และ id `7` มี “เรือเทียบท่า [Port Royal]”; พบ `CONSTDATA_TH__SAILING_RESULT.tsv` 138×19 และตาราง `SHIP`. ในชุดที่ค้นไม่พบ field/crosswalk ที่ผูก text row id หรือ `SAILING_RESULT.n_ID` เข้ากับ protocol field ด้านล่าง จึงไม่ join ด้วยเลขหรือถ้อยคำคล้ายกัน.

## คำตอบ objective

### 1. Server-provisioned data เข้าสู่ NavigationEx module

registry พิน `NavigationEx_AddSurveyDataVtial` ที่ vtable `0x00F46F50`, serializer `0x00733570`, handler `0x00733620`.

- common inbound handler `[0x00733620,0x0073367D)` หา `NavigationExModule_Client` ด้วยชื่อ `0x00F469DC`, แล้วส่ง vital เข้า module dispatcher `0x00732590` ที่ call `0x00733673 -> 0x00732590`.
- dispatcher branch ของ AddSurveyData พินด้วย runtime type getter `0x00732C30` ที่ `0x007326A5`; nested object อยู่ที่ vital `+0x14` (`0x007326C2`) และถูกเก็บ/ผูกเข้าคอลเลกชันของ module ผ่าน `0x00731280` / `0x00731410`.
- outer serializer `[0x00733570,0x00733614)` ส่ง presence byte แล้วเรียก nested object's vtable slot `+0x10`. Natural inbound consumer มีจริงจาก handler path ข้างบน; รอบนี้ไม่มี capture จึงไม่อ้างว่า original server เคยส่ง tuple ใดจริง.

nested survey-data serializer `[0x0072E590,0x0072E691)` มี wire shape:

1. byte tag `0x0B` @ object `+0x10`
2. u16 tag `0x12` @ `+0x12`
3. u16 tag `0x12` @ `+0x14`
4. u16 tag `0x12` @ `+0x16`
5. f32 tag `0x2A` @ `+0x18`, `+0x1C`, `+0x20`
6. qword tag `0x32` @ `+0x28`
7. u16 tag `0x12` @ `+0x30`

เฉพาะ f32 triple `+0x18..+0x20` มี consumer crosswalk จริงไปการคำนวณระยะ จึงเรียก XYZ ได้. ฟิลด์อื่นคง opaque ตาม offset; ห้ามตั้งชื่อจากขนาด.

### 2. Client เป็นผู้ตรวจระยะเอง — threshold 500

`NavigationExModule_Client` update/tick `[0x007321C0,0x00732586)`:

- อ่านคอลเลกชัน survey ที่ module `+0x58`; เลือก record ที่ nested byte `+0x10 == 1` (`0x00732358-0x00732367`).
- อ่านตำแหน่งผู้เล่นปัจจุบัน แล้วลบกับ record f32 `+0x18/+0x1C/+0x20` (`0x00732388-0x007323FE`), รวมเป็น squared distance.
- เทียบกับ double constant `250000.0` ที่ `0x00F46F48` (`comisd` @ `0x0073240A`); branch `jbe 0x00732431` จึงหมายถึงระยะจริง `<= sqrt(250000) = 500`.
- เมื่ออยู่ในช่วง จะดึง record u16 `+0x12` (`0x00732431`), สร้าง prompt/callback ที่ `0x00732521 -> 0x00730FE0`, และตั้ง flag รอผลที่ module `+0x5E`.

ดังนั้นด่าน “เรือถึงจุด” ไม่ใช่ dwell แบบ `world_travel_gate.py` เดิม และไม่ใช่ server packet รายจังหวะที่ส่ง position ปัจจุบันกลับมาเทียบ: ไคลเอนต์เป็นคนเทียบ position กับ survey point ใน update path ของตัวเอง. Server ยังต้อง provision จุดผ่าน AddSurveyData ก่อน — จึงไม่ใช่ client-only hardcoded point.

### 3. หลัง callback result `1` จึงส่ง EnterInstanceVital

callback `[0x00730FE0,0x00731083)`:

- ล้าง flag `+0x5E`, ตรวจ dword ของ callback/event `+0x94 == 1` (`0x0073100D`); ถ้าไม่เท่าจะออกโดยไม่ส่ง.
- เมื่อเท่ากับ 1 จะ allocate object ผ่าน `0x00730BF0`, คัดลอก survey record u16 `+0x12` ที่ถูกพกมาใน callback ไป `NavigationEx_EnterInstanceVital+0x14` (`0x00731049-0x0073104F`) แล้วเข้าทาง outbound `0x004011A0 -> 0x005DD800` (`0x00731053/0x0073105A`).
- allocator `[0x00730BF0,0x00730CEC)` ตั้ง vtable `0x00F46E80`, u16 `+0x14 = 0`, และ byte `+0x16 = 6` ทั้ง fresh/reuse path; callback เขียนทับเฉพาะ u16.
- serializer `[0x006A7310,0x006A735B)` พิน body สอง field: `tag 0x12 / 2B @+0x14`, แล้ว `tag 0x0B / 1B @+0x16`.

คำตอบตัวเลือกจึงเป็น **(ก) + gate ที่ต้องมี callback result 1**. Static control flow พิสูจน์ result gate และ outbound send แต่ไม่พอให้ตั้งชื่อ result `1` ว่า “ปุ่มยืนยัน” หรือพิสูจน์ว่าผู้เล่นคลิกปุ่มใดจริง; ชั้น client-observable ต้องยืนยันหน้าตา/ข้อความเอง. จึงไม่เลือก (ค) แบบ “ต้องคลิกวัตถุท่าเรือเพื่อเริ่ม flow” — จุดเริ่มคือ proximity auto-check, interaction อยู่หลังจากเข้าเขตแล้ว.

## T2 — ไม่ใช่ TeleportVital/ForcePos codec เดียวกัน

- flow ถึงจุดใช้ตระกูล `NavigationEx_AddSurveyDataVtial` → local distance → `NavigationEx_EnterInstanceVital`.
- `RE-090` พิน `ForcePos` เป็น vec3-only และ `TeleportVital` เป็น target-presence + scene/sequence/vec3 + aux/control. ไม่มี codec ใดแทน AddSurveyData/EnterInstance shape ข้างบนได้.
- ผลที่พินได้จึงชี้ seam สองช่วง: NavigationEx ตัดสิน/ขอเข้า instance ก่อน; การย้ายฉากจริงอาจตามมาผ่าน Teleport/ForcePos ภายหลัง แต่ใบนี้ไม่พิสูจน์ response/lifecycle หลัง request และไม่ join สองตระกูลเพราะมีตำแหน่งเหมือนกัน.

## ความสัมพันธ์กับ RE-087

`RE-087` พินอีก path หนึ่งใน module เดียวกัน: command `InvokeNavigationWindow` เปิด `Main_Sail_Lookout`, แล้ว action `Survey` ส่ง `NavigationEx_RequestSurveyVtial(+0x14=5)`. ส่วน RE-086 พิน proximity/entry path ที่ส่ง `NavigationEx_EnterInstanceVital`.

สอง path อยู่ namespace เดียวกันแต่ static รอบนี้ **ยังไม่พิสูจน์ว่า prompt/callback ของ RE-086 คือหน้าต่าง `Main_Sail_Lookout` เดียวกัน** หรือว่าหน้าต่างที่เจ้าของเรียก “รายงานกัปตัน” ปรากฏก่อน/หลัง EnterInstance ตรงจุดใด. ห้ามรวมสองผลเป็น UI timeline โดยไม่มี attended/capture.

## verifier / reproducibility

- ใหม่: `pf_bridge\staged\re086_dock_trigger_static.py`
- SHA-256: `82bf2fb70789d7f7bfb1eced77e0e0de1ebab9126de1483a1f4933f79390c02c`
- final run อิสระ 2 รอบด้วย `python -B`: `110/110 PASS`, exit `0/0`, ไม่สร้าง `.pyc`.
- recursive CFG ด้วย `static_recursive_cfg_probe.py` SHA `c95eefd9...94b27`:
  - module tick `[0x007321C0,0x00732586)` — 260 instructions, gap/error `0/0`, SHA `78753a30...315d8`
  - proximity callback `[0x00730FE0,0x00731083)` — 47 instructions, gap/error `0/0`, SHA `29c2c7a7...b5951`
  - survey-data serializer `[0x0072E590,0x0072E691)` — 103 instructions, gap/error `0/0`, SHA `5b714541...aa8f2`
  - AddSurvey serializer `[0x00733570,0x00733614)` — 63 instructions, gap/error `0/0`, SHA `f8c75100...f178c`
  - EnterInstance serializer `[0x006A7310,0x006A735B)` — 33 instructions, gap/error `0/0`, SHA `17eb1030...e91cfa`
  - EnterInstance allocator `[0x00730BF0,0x00730CEC)` — 85 instructions, gap/error `0/0`, SHA `9be1b51f...c7688`
  - common handler `[0x00733620,0x0073367D)` — 38 instructions, gap/error `0/0`, SHA `7d8c84a1...d4cb`

## integrity / concurrent sync

- image ก่อน/หลัง: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `AGENTS.md` ก่อน/หลัง: `63d7de90...6026a`.
- external tree ก่อน/หลัง: 30 files, aggregate `cad40e79...edbaa`.
- gamedata tree ก่อน/หลัง: 1,109 files, aggregate `a3d01a9f...d5e66`.
- RE-087/RE-090 result inputs ก่อน/หลัง: `9e7b75e8...69a85` / `6c6b898b...a2a0`.
- ระหว่าง final check เวลา 01:12 มี sync R184 เปลี่ยน queue `0571614a...af41a -> 391f126d...a30f` และ `NEW_ORDERS 7c1c5993...6798 -> 9740f758...9d9c`. หยุดก่อนส่งผล, อ่าน queue ทั้ง 3,094 บรรทัด + `NEW_ORDERS` + `FROM_CHIEF_R184` ใหม่แล้ว: R184 ปิดหัว `RE-089/090/091` ให้ตรงจดหมายเดิม; เนื้อ/objective/jobs/nonclaims ของ `RE-086` ไม่เปลี่ยน, ยัง OPEN และยังไม่มี result ทั้ง root/`consumed/`. ใช้ hash หลัง sync เป็น final baseline.
- ไม่แก้ source, queue, `NEW_ORDERS`, external, gamedata, เกม, server, DB หรือ git. ไฟล์ใหม่มีเฉพาะ verifier ใน `staged`, จดหมายผลนี้ และ runner log ตามขั้นจบรอบ.

## nonclaims

1. ไม่อ้างว่า client แสดงหน้าต่าง/ข้อความ/ปุ่มใดจริง เพราะรอบนี้ไม่เปิดเกมและไม่มีชั้น client-observable.
2. ไม่อ้างว่า survey record u16 `+0x12` หรือ EnterInstance u16 `+0x14` คือ island id, scene id, dock id หรือ row id; พิสูจน์เพียงการคัดลอก unchanged ข้าม callback.
3. ไม่อ้างความหมายของ EnterInstance byte `+0x16 = 6`; เป็นค่า default ที่ allocator ตั้งและส่งออกเท่านั้น.
4. ไม่อ้างว่า callback result `1` มาจาก mouse click หรือปุ่มชื่อใด; พิสูจน์เพียง gate ก่อน outbound.
5. ไม่อ้างว่า AddSurveyData tuple ใดถูก original server ส่งจริง; พิสูจน์ inbound consumer + codec จาก shipped image และ registry เท่านั้น.
6. ไม่อ้างว่า bounded string/registry search ที่ไม่พบชื่อ dock หมายถึงไม่มีกลไก dock; positive NavigationEx control flow เป็นหลักฐานของคำตอบ.
7. ไม่อ้างว่า `Main_Sail_Lookout` ของ RE-087 กับ proximity prompt ของใบนี้เป็นหน้าต่างเดียวกัน หรือว่าตามกันใน UI timeline ใด.
8. ไม่อ้าง response หลัง EnterInstance, การย้ายฉาก, destination, จำนวนเกาะ หรือกลไกเรือของ RE-085.
9. ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue/git.

## BUILD_IMPACT

**BUILD_IMPACT:** เลน Columbus→ทะเล→เกาะควรมี seam แยกจาก Teleport: server provision `NavigationEx_AddSurveyDataVtial` ที่มี opaque record + XYZ, client จะตรวจระยะ 500 เอง และเมื่อ callback result ผ่านจึงตอบ `NavigationEx_EnterInstanceVital(u16_from_record, byte=6)`. ใช้ผลนี้ออกแบบ probe/build ต่อได้โดยคงชื่อ field เป็น opaque และรอ attended/capture ยืนยันว่าหน้าต่างใดปรากฏ; ห้ามกลับไปใช้ fixed dwell gate เดิมหรือ compose Teleport แทน NavigationEx request.

`BUILD_IMPACT_NONE: 0/1`

สถานะที่ chief ควรกรอก: `RE-086 PASS/DONE — SERVER-PROVISIONED SURVEY XYZ; CLIENT PROXIMITY <=500; CALLBACK RESULT 1 SENDS NavigationEx_EnterInstanceVital(u16 copied, byte 6)`.

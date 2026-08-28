[ถึง: chief cloud และ LANE-GM (ผู้เปิดใบ) · cc: COO, Panya · จาก: RE runner LOCAL]

# RE-132 RESULT — `0x9F2C` ใช้ vital_version `0`; handler มีทางไป render

เวลา: `2026-08-29T00:10+07:00`  
สถานะ: **DONE / PASS (static)**  
ขอบเขต: อ่านอิมเมจ/ตาราง/ซอร์สเท่านั้น ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

## START และ input pins

- ticket START: `2026-08-29T00:01:25.1625011+07:00`
- `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `CLIENT_RE_QUEUE.md` SHA-256 `8bfb61035c6533829099482227df5e0d2cb830dc54bd80edd93fde7db1c3844a`
- ใบเปิด `20260828_2326_LANE-GM-RE-REQUEST-132-gm-global-message-vital-version.md` SHA-256 `ddaa8ff68addf782dd9614af72708c4e3e3fb5bc6eff266a0467861a9f183efe`
- `PF_PROTOCOL_REGISTRY.tsv` SHA-256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv` SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- ผลเดิมที่ reuse หลัง verify SHA: RE-105 `99eeb504...b7a20`; RE-129 `87b0fcde...328a`

`say_wire.py` ถูก sync ระหว่างรอบเวลา `00:08+07:00`; guard ตัวตรวจหยุดก่อนสรุป แล้วอ่านไฟล์ใหม่และ repin เป็น SHA-256
`cb9a02d6b4e0da9c6bcb444bc72eb4d54dd0d10b5159422ef59283048416bf4f` จึงค่อยรันใหม่จนผ่าน

## ค้นก่อนถอด

**ค้นใน `pf_bridge/external/` แล้ว: เจอ** — สำรวจ 30 ไฟล์ / 29,900,221 ไบต์ fingerprint
`a945499bda539714cddc97f4e93631bc3aa0bef2a03d2dd1da8bad623bcd7e51` พบ registry ของทั้ง
`Channel_GMGlobalMessageVital` และ `Channel_LocalTalkMessageVital`, shared serializer `0x0065AD40`, handler
`0x0065C850`, getter/vtable/registration site และแถว serializer fields 4 แถวต่อคลาส
· verify span `[0x0065AD40,0x0065AD83)` กับอิมเมจจริงแล้ว SHA-256
`207d532a2c430b964731dba4032d2655a217c310cee3ad1f1d9cf1b89280a758` ตรงตาราง

**ค้น gamedata แล้ว: ไม่เจอ** — สำรวจ 1,109 ไฟล์ / 15,319,585 ไบต์ fingerprint
`769352ecd26fbae5d1dd6cbc0df067136215aac3892109610d269b2779989448`; ไม่พบ class/opcode/version crosswalk
ที่เกี่ยวข้อง ผล match `AC52` บางจุดเป็น substring ไบต์/พิกัดใน placement/Lua เท่านั้น ไม่ใช่ crosswalk

ไม่พบผล `RE-132` เดิมทั้ง root/consumed และไม่พบจดหมายผล `GT-016`; จึงไม่ใช้ผลชั้นสูงกว่ามาแทนใบนี้

## ผลทีละ job

### T0-T2 — vital_version

1. base constructor `[0x00657C90,0x00657D06)` ทำ `xor eax,eax` ที่ `0x00657CB8` แล้วทำ
   `mov byte ptr [esi+0x10],al` ที่ **`0x00657CC9`** ⇒ ค่า exact คือ **`0`**
2. prototype ของตัวคุม `0xAC52` เรียก constructor นี้ที่ `0x0065B9F9` แล้วใส่ vtable
   `0x00F3775C` ที่ `0x0065B9FE`; vtable ผูก getter `0x006580B0`
3. prototype ของ `0x9F2C` เรียก constructor เดียวกันที่ `0x0065BCD0` แล้วใส่ vtable
   `0x00F3790C` ที่ `0x0065BCD5`; vtable ผูก getter `0x0065AC10`
4. registration sites ผูกชื่อจริงกับ id globals แยกกัน: LocalTalk `0x00BF72D0`, GMGlobal `0x00BF7390`
   จึงไม่ใช่การจับคู่เพราะเลขหรือ serializer เท่ากัน; crosswalk มาจาก name → id-global → getter → vtable → prototype
5. generic nested-vital reader เทียบ exact equality กับ `message+0x10` ที่ `0x005F3EFC`

**คำตอบ:** `Channel_GMGlobalMessageVital (0x9F2C) vital_version = 0` และ
`Channel_LocalTalkMessageVital (0xAC52) control vital_version = 0`; ทั้งคู่มีไซต์เขียนเดียวกัน `0x00657CC9`
เพราะใช้ base constructor เดียวกัน

### T3 — optional handler/render path

handler ที่ vtable ทั้งสองตัวผูกไว้คือ `[0x0065C850,0x0065C8A8)` และ **ไม่ใช่ no-op**:

- resolve `ChannelModule_Client`, type-check แล้วส่ง message เดิมเข้า router `0x00659870` ที่ call site `0x0065C89C`
- GMGlobal discriminator คือ helper `[0x00657BC0,0x00657BEF)` ซึ่งผูกกับ type slot `0x0065AC20`; router เรียกที่ `0x0065A028`
- เมื่อ match จะอ่าน wstring **body ที่ object+0x18** ณ `0x0065A043` และเรียก display sink `0x005CBAF0` ณ `0x0065A053`

นี่คือ **static client-binary render-path positive**: frame ที่ deserialize/dispatch ผ่านมาถึง handler มีเส้นทางอ่าน body
แล้วเรียกตัวแสดงผลจริง ไม่ใช่ `mov al,1; ret 4` แบบ ForcePos

### T4 — verifier

`staged/re132_gm_global_version_handler_static.py` SHA-256
`5efe18221bd577675ba4024d8718a38b9c7cbe18dd5b888d5db56113b8221d95` ผ่าน **61/61 checks**;
ตรึง 12 source files + 12 VA spans และรันซ้ำหลัง repin สำเร็จ

## ชั้นหลักฐาน

- **client binary / static:** PASS — version `0` และทาง handler → body → display sink ถูกพินตาม VA ด้านบน
- **client-observable:** **ไม่ได้รัน/ไม่ได้วัด** — ไม่มีการเปิดเกม ไม่มีภาพ ไม่มีคำกล่าวว่าข้อความขึ้นจอจริง
- **wire/DB runtime:** **ไม่ได้รัน** — ไม่ได้ส่งเฟรมและไม่ได้เปิด DB

## BUILD_IMPACT

`BUILD_IMPACT:` ในเชิงไบต์สามารถตั้ง `say_wire.GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED = 0` ได้;
codec เจ้าของเดิมก็ประกอบ nested version `0` อยู่แล้ว จึงไม่ต้องสร้าง codec ตัวที่สอง
· ข้อ T3 ปิดเงื่อนไข static ว่า GMGlobal มี render route แต่ **ยังไม่อนุญาตให้ RE runner เปิด gate**:
checkout ปัจจุบันระบุเงื่อนไข identity ต่อ connection (A) และคำเคาะ COO ก่อนส่งจริง ซึ่งอยู่นอกใบนี้

`BUILD_IMPACT_NONE: 0/1`

## nonclaims

1. ไม่อ้างว่าข้อความปรากฏบนจอ; ต้องใช้ `GT-016`/`GT-133` หรือ client-observable หลักฐานแยก
2. ไม่อ้างว่า frame จะ broadcast ไป socket อื่น; handler ที่พิสูจน์คือฝั่ง client เครื่องเดียว
3. ไม่อ้างว่า identity/allowlist ของคำสั่ง GM ปลอดภัย และไม่เปิดค่าคงที่/แก้ server source ในรอบนี้
4. ไม่อ้างพฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ; ผลทั้งหมดมาจาก client image และ checkout ปัจจุบัน
5. การใช้ serializer `0x0065AD40` ร่วมกันลำพังไม่ได้พิสูจน์ version; ข้อนี้ปิดด้วย ctor crosswalk เท่านั้น


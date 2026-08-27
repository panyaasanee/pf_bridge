[ถึง: chief cloud · LANE-GM · COO · cc Panya | จาก: RE runner LOCAL | 2026-08-27T16:13+07:00]

# RE-105 RESULT — DONE/PASS · `GM_UpdateGMStateVital` vital version = `0` · generic mismatch path pinned

- ใบ: `RE-105 GM-UPDATE-STATE-VITAL-VERSION-001 [STATIC-ON-BRIDGE]`
- ticket START: `2026-08-27T16:02:25.765+07:00` · รอบ START: `2026-08-27T16:00:49.727+07:00`
- วิธี: static/read-only เท่านั้น · ImageBase `0x00400000`
- verdict: nested `GM_UpdateGMStateVital 0x5A19` ต้องส่ง `vital_version=0` แบบ exact equality. ค่า `1` จาก GT-101 จึงตก generic mismatch `0xE0000031` ตามที่ client แสดงจริง. ไบต์ `08 04` ที่ PC offset 8 เป็น **outer `GSCN_RunTimeProtocolRes` protocol version 4** ที่ถูกต้องและเป็นคนละฟิลด์ ไม่ใช่สาเหตุร่วม.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** ในชุด 30 ไฟล์ fingerprint `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`: registry row ของ `GM_UpdateGMStateVital` (id global `0x01088F88`, getter `0x00729600`, vtable `0x00F4631C`, serializer `0x00729720`, handler `0x00729F00`), serializer W/R 6 แถว, และ validation W/R `NOT_OBSERVED`. เจอ `GSCN_RunTimeProtocolRes` row แยกต่างหาก (getter `0x005E37C0`, vtable `0x00F2FFC0`, serializer `0x005E3EE0`). ชุดส่งมอบตอบ identity/layout แต่ไม่มี row ของ version instance field/error dialog จึง verify SHA แล้วไล่โค้ด generic reader/constructor ต่อ.
- **ค้น gamedata แล้ว: ไม่เจอ** `GM_UpdateGMStateVital`, `0x5A19`, `0x00729F00`, `VitalData`, `版本不對`, `ErrorData` ใน tree 1,109 ไฟล์ fingerprint `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`. ขอบเขตครอบดัชนี/คอลัมน์/188 tables/Lua/scene ทั้ง tree; เป็น code/protocol concern ไม่ใช่ข้อมูลเกม.

## T0 — input/SHA gate

- image `GameClient.local.bin` SHA `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- external registry `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- serializer fields `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- validation `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- GT-101 result `3b0b0433d2c348f091dd486f9339507b0b780fb933278a9021ad0bf2f6d74492`
- current server `gm/state_wire.py` `3b42d7dc963d370dda0c7d9f23b4d409d9166f4b980e80444474dc2c1ca7053b`
- queue at START `2a0815868524256ecea33d7ffdafe2951ce23ea5f909cfd08430fce1ac6c86a2`; AGENTS `2b5af7c5cd67b9eb752342615d4f9e0e901d84c4e287bbc55d0a3db9819207ee`; NEW_ORDERS `398e3f09284d5fdbbd0c7014a0831841977a88e3791047dfcc7b054531192849`.

## T1 — ค่าที่ผ่านคือ `0` ค่าเดียว

จุดเช็คจริงอยู่ใน **generic VitalData collection reader** `[0x005F3E20,0x005F406D)` SHA `bfdf1ada48068e9a3838b51241e164677e0142a6ce0f6d68d547299fe279e217`, ไม่ได้อยู่ใน handler เฉพาะ `0x00729F00`:

1. `0x005F3EE3-0x005F3EF9` อ่าน nested version จาก wire ด้วย tag `0x0B`, 1 byte.
2. `0x005F3EFC` คือ `cmp cl, byte ptr [esi+0x10]`; `esi` คือ message instance ที่ generic registry สร้างตาม nested vital id.
3. `0x005F3F01 je 0x005F3F39` เป็นทางผ่านเพียงทางเดียว — จึงเป็น exact equality ไม่ใช่ช่วง/bitmask.

ค่า expected ของ `0x5A19` มาจาก prototype ของมันเอง:

- bootstrap `[0x007299B0,0x00729A0D)` SHA `05e0610e2cdc2ed73f0e01a9488e397eaa4c7e823bf0d23dc97b71ba4aeca2c2` ทำ `xor ebx,ebx` @ `0x007299D9`, แล้ว `mov byte ptr [eax+0x10],bl` @ `0x007299F1` ก่อนใส่ vtable `0x00F4631C` และ register prototype ผ่าน `0x005F3DF0` @ `0x00729A08`.
- ดังนั้น `message+0x10 = 0` โดย direct store. ไม่ได้อนุมานจาก START_GAME v3 หรือ Teleport v4.
- getter slot vtable `+0x10` ชี้ `0x00729600`, ซึ่งคืน id จาก global `0x01088F88` (`0x5A19`).

**คำตอบ T1:** `GM_UpdateGMStateVital` nested `vital_version = 0` เท่านั้น.

## T2 — generic error path และที่มาของ `ErrorData=23065`

เมื่อ equality ล้ม:

- `0x005F3F03-0x005F3F08` เรียก vtable `+0x10` ของ message instance เพื่ออ่าน **id ของ message ตัวที่กำลังถูก decode** แบบ dynamic.
- `0x005F3F18` ใส่ error code `0xE0000031`; ไม่ได้ hardcode `0x5A19` ใน branch นี้.
- global localization registration `[0x00C1D1DB,0x00C1D1F5)` SHA `54185c4c38510a9bfbca8a02a76845ac5dcf91857f6167b75bd6bd58c52135e6` ผูก `0xE0000031` กับ UTF-16 `網路 VitalData 版本不對` ที่ `0x00FBB624`.
- common exception formatter `[0x00A8E210,0x00A8E3A5)` SHA `5cc395a09316129cdb8b30b9ce8165017ce7d15b115e3228c075086480405e1b` อ่าน `exception+0x0C` @ `0x00A8E2FB` แล้วประกอบด้วย template `0x00F86F48`: `%s --- %s ErrorData=%d，\r\n請洽程式設計人員`.

ดังนั้น path นี้ **generic สำหรับทุก nested VitalData** ที่ผ่าน collection reader; `ErrorData` คือ vital id ของ instance ที่ mismatch. ใน GT-101 instance นี้คือ `0x5A19 = 23065`, ตรง client-observable โดยไม่ใช้หลักฐานจอพิสูจน์ static chain ย้อนกลับ.

## T3 — `08 04` เป็น outer version 4 และถูกต้อง

- `GSCN_RunTimeProtocolRes` prototype constructor `[0x005E3720,0x005E37AD)` SHA `9865e2a746720025a6df41edb1854b7d7206c2da410aa9ae916d26c296d1b011` เขียน `mov byte ptr [esi+0x10],4` @ `0x005E3763` โดยตรง.
- serializer `[0x005E3EE0,0x005E405C)` SHA `4e6bda64c3926ddf78cbeba62552385a944ab167673aa8a390746620f39650b0` คือ outer runtime carrier ที่มี nested VitalData collection.
- server builder `make_runtime_vital` แยกชัด `u8tag(0x08,4)` (outer protocol version) ออกจาก `u8tag(0x0B,vital_version)` หลัง nested id. รายงาน natural/accepted RuntimeRes เดิมก็ decode PC offset `0x08` เป็น protocol version 4.

ดังนั้นเฟรมที่ถูกต้องสำหรับใบนี้ยังขึ้นต้น `... 08 04 0B 02 12 01 00 12 19 5A` เหมือนเดิม แต่ต้องเปลี่ยน byte หลัง id จาก `0B 01` เป็น **`0B 00`**. ไม่ต้องแก้ `08 04`.

## verifier / reproducibility

- `pf_bridge\staged\re105_gm_state_vital_version_static.py`
- SHA-256 หลัง closeout repin ฝั่ง server `93dbe98e5f69649c6da080f8e58738ab78c309f5b1ccc3a672c207ee92061e7f`
- รัน `py -3 -B` หลังแก้ guard ครบสองครั้งอิสระก่อน sync และรัน final หลัง repin: PASS/PASS/PASS, exit `0/0/0`; พิน 9 spans / 8 input files; ไม่มี `.pyc` จากรอบนี้.

### closeout — concurrent R194 server sync (ไม่เปลี่ยน verdict)

หลังส่งผลแล้ว local sync เปลี่ยน `gm/state_wire.py` จาก START SHA `3b42d7dc963d370dda0c7d9f23b4d409d9166f4b980e80444474dc2c1ca7053b` เป็น `61d047b7af12b90d55cce8369e73ba52c5ea0bbfd64f620dfc453f33f2fcbd37` (commit เนื้อหา `91b8df2`, อยู่ใน HEAD merge ปัจจุบัน). การเปลี่ยนคือ safety guard `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = None` ที่ fail-closed รอ RE-105 — **ยังไม่ได้รับค่า 0** และไม่ขัดผลนี้. image/external/legacy/spans ที่ใช้พิสูจน์คง SHA เดิมทั้งหมด; verifier เปลี่ยนเฉพาะ source pin และเพิ่ม assertion ว่า guard ยังเป็น `None`, final PASS.

## nonclaims

1. ไม่เปลี่ยน semantic ของ payload `+0x14/+0x15/+0x18`; RE-089/RE-104 ยังเป็นคำตอบของ state/UI gate แยกต่างหาก.
2. ไม่อ้างว่า version 0 เป็นกฎของ vital ทุกตัว; generic reader เทียบกับ `instance+0x10` ของ **แต่ละ class** และ class อื่นมีค่าอื่นได้.
3. ไม่อ้างว่าแก้เป็น 0 แล้ว dedicated GM UI จะเปิดจริง; GT-101 รอบเดิมไม่เคยผ่าน decoder และยังต้อง rerun client-observable หลัง chief/LANE-GM ต่อค่า 0.
4. ไม่อ้างว่าทุก network error ใช้ code `0xE0000031`; พิสูจน์เฉพาะ VitalData version mismatch. Protocol-version mismatch เป็น error code/namespace แยก.
5. ไม่ใช้ id เท่ากันเป็น crosswalk: message id มาจาก vtable getter ของ instance ที่ generic registry สร้างตาม wire id.
6. ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ GameClient/server/external/gamedata/queue/git.

## BUILD_IMPACT

**BUILD_IMPACT:** chief/LANE-GM ควรเปลี่ยน call `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` เป็น `make_gm_update_state_frame(legacy, 0, 0, 0, 0)` และอัปเดต comment/doc/test ที่ติดป้าย version เป็น assumed. คง outer `u8tag(0x08,4)` เดิม. จากนั้นทำ byte-level headless assertion ว่า nested header เป็น `12 19 5A 0B 00` ก่อนเปิด GT-101 rerun; ผล UI/GM permission ยังต้องวัด attended แยก.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-105 DONE/PASS — GM UPDATE VITAL VERSION 0; GENERIC E0000031 ERROR PATH PINNED; OUTER VERSION 4 UNCHANGED`.

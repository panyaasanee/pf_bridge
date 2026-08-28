[ถึง: chief cloud · LANE-A/M2 · COO · cc Panya | จาก: RE runner LOCAL | 2026-08-27T16:25+07:00]

# RE-106 RESULT — DONE/PASS · `GetQuestFlag` อ่าน `QuestAttr` map · wire delta ที่ตรงคือ `QuestFlagRangeChange` (`0x5124`)

- ใบ: `RE-106 QUEST-FLAG-SYNC-MECHANISM-001 [STATIC-ON-BRIDGE]`
- ticket START: `2026-08-27T16:18+07:00` · รอบ START: `2026-08-27T16:00:49.727+07:00`
- วิธี: static/read-only เท่านั้น · ImageBase `0x00400000`
- verdict: เป็น **ทาง ข — wire-backed state** ไม่ใช่ local-only. `Quest.GetQuestFlag(id)` อ่าน map ใน `QuestAttr`; protocol `QuestFlagRangeChange` มี crosswalk จาก class/serializer/handler ถึง setter ที่เขียน map เดียวกันโดยตรง. ผู้สมัครเดิม `UpdateQuestMiscDataVital`/`UpdateDailyQuestVital` เป็นคนละ schema และคนละ handler branch.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** ในชุด 30 ไฟล์ fingerprint `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`: registry ของ `QuestAttr`, `QuestModule`, `UpdateQuestMiscDataVital`, `UpdateDailyQuestVital`, `QuestFlagRangeChange`; serializer W/R; validation. `QuestFlagRangeChange` มี W/R อย่างละ 3 field แต่ capture validation W/R ยัง `NOT_OBSERVED`. ค้น exact ชื่อ, getter/vtable/serializer/handler VA, `QuestFlag`, `QuestAttr`, `0x006083C0`, `0x00622940`, `0x00621AE0`, `0x00621C20`; ไม่พบ capture ที่ยืนยันค่าจริงบนสาย.
- **ค้น gamedata แล้ว: เจอ consumer แต่ไม่เจอ writer จริง** ใน tree 1,109 ไฟล์ fingerprint `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`: `PF_GAMEDATA_LUA_API.tsv` ระบุ `Quest.GetQuestFlag` IMPLEMENTED @ `0x006083C0` ใช้ 508 จุด/366 ไฟล์; `Quest.SetFlag` และ `Quest.SetQuestFlag` เป็น `STUB_NOOP` @ `0x0045FA00`. `q_con_new.lua` เรียก getter ที่บรรทัด 107/119/142 และเรียก stub setter ภายหลัง. ขอบเขตค้นครอบดัชนี/ตาราง/Lua/scene ทั้ง tree; ไม่พบชื่อ protocol `QuestFlagRangeChange` ใน gamedata — writer อยู่ใน client code/network handler ไม่ใช่ Lua data.

## T0 — input/SHA gate

- image `GameClient.local.bin` SHA `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- external registry `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`; serializer fields `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`; validation `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- gamedata API `21dfa905a67154765f6cdc9c508220ff01441abb7e16f8285901746a62530b73`; `q_con_new.lua` `c32123b06bac443d26c8c70adb14ec5941276d75b52a6111deac0be446bfe697`
- class census `fd08fb13a3dcdf6719e52cf3830fa7978ea6680c6b7fa84fef6196c42688becd`; row `QuestFlagRangeChange\ttask_quest\t0x5124\t20772` ให้ wire id จาก name-hash census
- queue at ticket START `5b435acfbb711abffb8f0a6a82b0a099707a430a0d6622c0a9e2852d776ec8ac`; NEW_ORDERS `3947a01602dfc093439eb7432598d5613c68657b188ce36ad567350bc6c9d4b7`

## T1 — `Quest.GetQuestFlag` อ่าน map ของ `QuestAttr`

สายจริง `[0x006083C0,0x006084C7)` SHA `21ab32a1ed40d36cc9a3da94f25f91e2c52364c622267d308861f322a7fa6ab7`:

1. `0x00608428` โหลด type id จาก global `0x010828B4` ของ `QuestAttr`, แล้ว `0x0060843C` resolve object จาก attr registry; ไม่ได้หา object เพราะเลข id ไปตรงกันโดยบังเอิญ.
2. `0x00608447-0x00608467` เช็ค dynamic type เทียบ type object ของ `QuestAttr`.
3. `0x00608483` เรียก `0x00602730` ด้วย quest id ที่อ่านจาก Lua.

getter `[0x00602730,0x00602796)` SHA `bd4cb8b43c183f2004e9724cc0586defce31ddbbec521716626643e4244691d1`:

- `0x00602737 lea esi,[ecx+0x28]` เลือก ordered map ที่ `QuestAttr+0x28`.
- `0x00602746` lookup ด้วย u16 quest id; ถ้าพบ `0x00602779 mov eax,[node+0x10]` คืนค่า dword.
- ถ้าไม่พบ `0x0060278D xor eax,eax` จึงคืน `0`.

`QuestAttr` serializer `[0x00602810,0x00602950)` SHA `fc5cc7a1cd81db8a5c4a7e9a104b8be2cd9b7e9c660ef390b94214806ef48a62` มี read branch ที่อ่าน count tag `0x0F`, วนอ่าน key u16 tag `0x12` + value u32 tag `0x14`, แล้วเรียก map setter `0x00602630` @ `0x0060293A`. นี่พิสูจน์ว่า object รองรับ serialized snapshot; ไม่ใช้จุดนี้เพียงจุดเดียวอ้าง carrier network เพราะ delta path ด้านล่างตรงกว่าและครบกว่า.

## T2 — wire writer ที่ตรง: `QuestFlagRangeChange 0x5124`

layout จาก serializer `[0x00621C20,0x00621CA7)` SHA `43c745e76530a967e7f7adba53c5ee60dca3bbaafa257419827e9a1195be2b8b`:

| field | instance | wire | ความหมายจาก consumer |
|---|---:|---:|---|
| 1 | `+0x14` | tag `0x12`, u16 | first quest id |
| 2 | `+0x16` | tag `0x12`, u16 | last quest id, inclusive |
| 3 | `+0x18` | tag `0x0B`, u8 | flag value เดียวสำหรับทั้งช่วง |

crosswalk ถึง map เดียวกับ getter:

1. registry ผูก class `QuestFlagRangeChange` กับ vtable `0x00F34028`, serializer `0x00621C20`, handler `0x00623090`; census ที่ derive ด้วย name hash ให้ id `0x5124`.
2. handler `[0x00623090,0x006230E2)` SHA `d9f7fda8c6c686daa677259d5fd0d653c0500ec0b14278840d99919e170a45a7` resolve `QuestModule` ด้วย type token `0x00F0BAE8` แล้ว dispatch message ไป `0x0061A950` @ `0x006230D6`.
3. exact-cast helper `[0x00615E10,0x00615E3F)` SHA `97cdba0d7922581c024027446130b47420e8ba40a7a2b66af76c47c57e48410f` เปรียบ dynamic type กับ `0x00621C10`; นี่คือ type getter ที่ vtable `0x00F34028[0]` ชี้อยู่ จึงไม่ใช่การจับคู่เพราะชื่อ/id เท่ากัน.
4. apply branch `[0x0061B291,0x0061B2D9)` SHA `a5d8b6b8bed46770e844a23622e27291a147ddc95ba9f9989a2b9eaa399acea3` วน `id=word[+0x14]` ถึง `word[+0x16]` แบบ inclusive, ตรวจว่า quest id resolve ได้, แล้วส่ง `dword[+0x18]` กับ id เข้า `QuestModule::set` `0x00618500`.
5. setter `[0x00618500,0x0061853E)` SHA `f52ce394375f9dff12c7ad4e332629db5f75e0035eb3194fc4bb7d1fc01f124a` โหลด `QuestAttr*` จาก `QuestModule+0x18` แล้วเรียก `0x00602320(id,value,notify=1)` @ `0x00618518`.
6. `0x00602320` SHA `1c102bb56c276e9481354f9c964b5648c94624aa5aa5b5484687d7276ee0bb6a` ค้น/เพิ่ม/แก้/ลบ entry ใน **map `QuestAttr+0x28` เดียวกับ T1** และเรียก change notification. loop จึงปิดครบ wire message → handler → QuestModule → QuestAttr map → Lua getter.

**คำตอบ objective:** client ไม่ได้เก็บ flag local ล้วน; มี protocol delta สำหรับ sync โดยตรง และชื่อที่ตรงคือ `QuestFlagRangeChange`, ไม่ใช่สอง candidate เดิม.

## เปรียบเทียบ candidate เดิม

- `UpdateQuestMiscDataVital 0x76A5`: serializer `[0x00622940,0x006229F8)` SHA `814e3ce118c3fdc26540df5db5d0acde6983cd33bd7ab268429ce0b87b8588f7` มี u16 `+0x14`, presence flag และ nested object pointer `+0x18`. exact handler branch `0x0061B341` ใช้ helper `0x00615E70`/type getter `0x00621720`, แล้วไป `0x00616000`/quest-misc UI path; ไม่มี crosswalk ไป `QuestAttr+0x28`.
- `UpdateDailyQuestVital 0x5DEB`: serializer `[0x00621AE0,0x00621B33)` SHA `4ae5c1bbc7356f8cfeb2310c2412e49bf981ec535de3ecf85bc66791ff936a14` มี u16 `+0x14` + u32 `+0x18`. exact handler branch `0x0061B43F` ใช้ helper `0x00615EA0`/type getter `0x00621AD0`, แล้วเรียก `0x00615D00`; ไม่เขียน flag map ที่พิสูจน์ข้างบน.
- การแยกนี้อาศัย dynamic-type getters และ call path ของแต่ละ branch ไม่ได้อาศัยเลข id หรือ field offset ที่ดูคล้ายกัน.

## verifier / reproducibility

- `pf_bridge\staged\re106_quest_flag_sync_static.py`
- SHA-256 `375f9037a202636aa56ee7c3824da5ee6330803ae34e1c83a0fb6338cebf4d01`
- รัน `py -3 -B` หลัง guard สุดท้าย: PASS, exit `0`; พิน 12 spans / 7 input files. ก่อน guard สุดท้ายเคยรัน PASS/PASS กับชุด 6 files แล้ว; ไม่ใช้ผลรันที่ fail ระหว่างแก้ความยาว byte guard เป็นหลักฐาน.

## nonclaims

1. ไม่อ้างว่ามี capture จริงของ `0x5124`; validation ยัง `NOT_OBSERVED`. ผลนี้เป็น static serializer/handler proof.
2. ไม่อ้าง numeric value ของ Lua enum `Quest.Finish` จากใบนี้; field เป็น u8 แน่ แต่เลข semantic ต้องอ้าง constant/capture ที่พิสูจน์แยก ไม่เดาจากชื่อหรือจากค่า 1/2 ที่พบบางสคริปต์.
3. ไม่อ้างว่า `QuestAttr` full snapshot ถูกส่งใน envelope ใดโดยเฉพาะ; พิสูจน์เพียง read-capable serializer. ข้อสรุป wire-backed ยืนบน dedicated `0x5124` delta path อยู่แล้ว.
4. ไม่อ้างว่า range จะเขียน id ที่ไม่มี quest definition; consumer ตรวจ id ก่อนและข้าม entry ที่ resolve ไม่ได้.
5. ไม่อ้างว่าแค่ส่ง flag แล้ว M2 สำเร็จครบ; ยังต้องต่อ outer carrier/version/lifecycle ให้ถูกและวัด client-observable ว่า option 3021 ส่ง request จริง.
6. ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ GameClient/server/external/gamedata/queue/git.

## BUILD_IMPACT

**BUILD_IMPACT:** chief/LANE-A มี wire primitive ที่พิสูจน์แล้วสำหรับ M2 shortcut: สร้าง `QuestFlagRangeChange` id `0x5124` ด้วย `u16 start_id`, `u16 end_id` (inclusive), `u8 flag`. สำหรับ 110/111 ใช้ช่วง `110..111` ได้เมื่อทั้งคู่ต้อง state เดียวกัน; 739 ใช้ `739..739`. ต้องใช้ numeric constant ของ `Quest.Finish` จาก provenance ที่มีอยู่/พิสูจน์เพิ่ม และต่อผ่าน outer dispatcher ตาม pattern จริง — ห้ามใช้ `UpdateQuestMiscDataVital` หรือ `UpdateDailyQuestVital` แทน. เพิ่ม headless decode/assert สำหรับ id/layout และคง token `QUEST_FLAG_SHORTCUT quests=110,739,111 state=Finish source=M2-SHORTCUT-OWNER-20260827-1510`; จากนั้น attended ตรวจว่า client ปล่อย `QuestOperateVital` op1 ของ 3021 ออกจริง.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-106 DONE/PASS — GETQUESTFLAG READS QUESTATTR MAP; QUESTFLAGRANGECHANGE 0x5124 IS PROVEN WIRE DELTA; ORIGINAL TWO CANDIDATES REJECTED`.

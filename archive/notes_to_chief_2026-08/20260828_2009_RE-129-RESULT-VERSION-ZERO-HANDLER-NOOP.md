[ถึง: chief cloud · LANE-GM · COO · cc Panya | จาก: RE runner LOCAL | 2026-08-28T20:09+07:00]

# RE-129 RESULT — DONE/PASS (main) · `ForcePos` vital version = `0` · axis names bounded · registered handler is a no-op

- ใบ: `RE-129 FORCE-POS-VITAL-VERSION-001 [STATIC-ON-BRIDGE]`
- ticket/round START: `2026-08-28T20:01:46.472+07:00`
- วิธี: static/read-only เท่านั้น · image base `0x00400000`
- verdict หลัก: prototype constructor ของ `ForcePos` เขียน `message+0x10 = 0` โดยตรงที่ `0x005E5186`; generic VitalData reader เทียบ exact equality ที่ `0x005F3EFC`. ค่า version ที่ยืนยันแล้วจึงเป็น **0**.
- verdict สำคัญที่พบเพิ่ม: registered handler ของ `ForcePos` คือ complete body `[0x00710440,0x00710445)` = `mov al,1; ret 4`; ไม่มี read ของ payload และไม่มี position write. ดังนั้น static ชุดนี้ **ไม่พิสูจน์ว่า server→client ForcePos จะย้ายตัวละคร** แม้ version ถูกต้อง.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** ใน tree 30 ไฟล์ / 29,900,221 bytes / fingerprint `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`: registry row `ForcePos` (getter `0x005E51C0`, vtable `0x00F30254`, serializer `0x005E4250`, handler `0x00710440`) และ serializer W/R 8 แถว. `PF_FIELD_VALIDATION.tsv` ระบุ W=0/R=0 `NOT_OBSERVED`. ชุดส่งมอบตอบ identity/layout แต่ไม่มี version/axis semantic จึง verify SHA แล้วเดิน constructor/generic gate ต่อ.
- **ค้น gamedata แล้ว: ไม่เจอ** `ForcePos`, `TeleportVital`, `CWarpResult`, `vital_version`, `0x0E80` หรือ crosswalk ชื่อแกนใน tree 1,109 ไฟล์ / 15,319,585 bytes / fingerprint `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`. ขอบเขตครอบดัชนี/คอลัมน์/188 tables/Lua/scene ทั้ง tree; เป็นคำถาม native code ไม่ใช่ข้อมูลเกม.

## T0 — input/SHA gate

- image `GameClient.local.bin` `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `PF_PROTOCOL_REGISTRY.tsv` `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv` `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_FIELD_VALIDATION.tsv` `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- RE-105 prior answer `99eeb50407ef1da375d212d855070092501f2ee83e17eaf2b3e15d3a018b7a20` (SHA verified before reuse)
- current server `gm/teleport_wire.py` `93122b39640f07e08a0c7ed1c4e1c1ea526947c87da67a4047360c02f377c217`; `gm/warp_executor.py` `a3b891ae74a9d4f7f18079f4491a626c4e22e86e3a7a54806ca299bad606fa97`
- queue `ce1a8cc8737c431e141a59d398db7669b5491b2a71eb07d95e9856afdfd01ffc`; AGENTS `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`; orders `0e107cd392358cb78767b4562b958f4a59c5ae67bda2e1fe0e69c25ae829c315`.

## T1 — version `0` และไซต์ที่เขียน

Constructor `[0x005E5170,0x005E51A2)` SHA `4fcc77b79d1f2e4f41902f8669ac1aab0ba50be93fed2d8e14c9e0d6776f0f91`:

1. `0x005E5175 xor ecx,ecx`
2. `0x005E5186 mov byte ptr [eax+0x10],cl`
3. `0x005E518C mov dword ptr [eax],0x00F30254`

vtable `0x00F30254 + 0x10` ชี้ getter `0x005E51C0`, ซึ่งอ่าน id-global ของ `ForcePos` `0x01081FE4`; นี่คือ instance/crosswalk เดียวกัน ไม่ใช่จับคู่เพราะเลข id เท่ากัน. Startup prototype block `[0x005EE1E4,0x005EE229)` SHA `d72e704f...aa3b4279` สร้าง object รูปเดียวกันและ register ผ่าน `0x005F3DF0`.

Generic reader `[0x005F3E20,0x005F406D)` SHA `bfdf1ada...279e217` ใช้ `cmp cl,byte ptr [esi+0x10]` @ `0x005F3EFC`, ผ่านเฉพาะ `je` @ `0x005F3F01`. ดังนั้นคำตอบหลักคือ **`ForcePos vital_version = 0`** แบบ exact equality.

## T2 — f32 สามค่า: ตำแหน่งปิด, ชื่อแกนยังไม่ปิด

- serializer `0x005E4250` ส่ง object `+0x14` เข้า common vec3 writer `0x005F3490`; reader คู่กันคือ `0x005F34D0`.
- complete helper ทั้งสองอ่าน/เขียน f32 tag `0x2A` ตามลำดับ struct `+0`, `+4`, `+8`, จึงพินตำแหน่งเป็น `ForcePos +0x14/+0x18/+0x1C` ได้.
- แต่ helper ไม่มีชื่อ field และ registered handler `0x00710440` ไม่อ่านสามค่านี้เลย. capture validation ก็เป็น `NOT_OBSERVED` ทั้ง W/R. ไม่มี client-side crosswalk ที่แยกค่าที่หนึ่ง/สอง/สามเป็น x/y/z.

**T2 bounded negative:** ลำดับชื่อ `(x,y,z)` ใน server `ForcePosBody` ยังเป็น `[สมมติของสาย GM - รอ RE]`; อย่าใช้ความเหมือนกับ Position ของ message อื่นเป็นหลักฐาน. อย่างไรก็ดี layout `f32[3]` ตาม offset `+0/+4/+8` ปิดแล้ว.

## T3 — adjacent optional

`TeleportVital` constructor `[0x005E53D0,0x005E5459)` SHA `33fe5dac...6f80246c` เขียน `mov byte ptr [esi+0x10],4` @ `0x005E5425`: version **4** ปิดได้โดยตรง. `CWarpResult` ไม่ปิดในใบนี้; ไม่เดาจาก register ที่ reuse ใน bootstrap ยาว.

## T4 — verifier

- `pf_bridge\staged\re129_force_pos_vital_version_static.py`
- SHA `7e545e61296de2b01b09151ab38c438ee277a5eee9349c6119d237b2c55f5081`
- `py -3 -B`: PASS/PASS, exit `0/0`; 7 spans / 10 pinned files; ไม่มี `.pyc`.

## nonclaims

1. ไม่อ้างว่า version `0` เป็นกฎของ vital ทุกตัว; `TeleportVital` ใกล้กันใช้ `4`.
2. ไม่อ้างว่าสาม f32 คือ x/y/z หรือว่าค่าที่สามคือความสูง; client crosswalk ยังไม่มี.
3. ไม่อ้างว่า server→client `ForcePos` ย้าย avatar; handler ที่ registry ผูกไว้เป็น no-op และ direction ยัง `NOT_OBSERVED`.
4. ไม่อ้างว่า id `0x0E80` ได้จาก on-disk constant; identity ใช้ registry name/vtable/getter chain ส่วน numeric id เป็นคนละหลักฐาน.
5. ไม่อ้างว่าแก้ version แล้ว `/warp` จะ visible; ต้องมีหลักฐาน inbound effect แยก.
6. ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ GameClient/server/external/gamedata/queue/git.

## BUILD_IMPACT

**BUILD_IMPACT:** LANE-GM ใช้ `vital_version=0` ในการประกอบ `ForcePos` ได้และควรเพิ่ม byte assertion ว่า nested header เป็น `... 12 80 0E 0B 00 ...`. แต่ **ห้ามยกผลนี้เป็นหลักฐานว่า client จะขยับ** และห้ามเปลี่ยนชื่อ positional f32 เป็น authoritative x/y/z. ก่อนเปิดใช้งานจริงต้องพิสูจน์ original direction/effect (capture หรือ positive consumer crosswalk); current local `teleport_wire.py`/`warp_executor.py` ยังรับ `vital_version` จาก caller โดยไม่มี `FORCE_POS_VITAL_VERSION_CONFIRMED` constant ตามถ้อยคำในคิว.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-129 DONE/PASS — FORCEPOS VERSION 0 PINNED; THREE F32 OFFSETS PINNED; AXIS SEMANTICS/INBOUND MOVEMENT UNPROVEN; REGISTERED HANDLER NOOP; TELEPORT VERSION 4`.

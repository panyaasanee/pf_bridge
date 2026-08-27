[ถึง: chief cloud (cc) และ Panya · จาก: RE runner Codex LOCAL]

# RE-056 RESULT — registrar method fails the control; static lane closed

**ผล: DONE / METHOD-FAIL ที่จ็อบ 0 / TERMINAL ตามเกณฑ์จบของใบ** · เวลา 2026-08-24 07:21–07:28 `+07:00`

งาน `STATIC-ON-BRIDGE` ล้วน: ไม่บูต server/client, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ image/capture/external/gamedata/source/queue และไม่รัน git

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: **เจอ** `PickupTerrainThing` และ `TriggerCastSkillVital` ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` พร้อม vtable, serializer, handler, field rows และ span SHA; **ไม่เจอ**แถวส่งมอบที่ผูก registrar `0x005F3DF0` เข้ากับ natural outbound dispatch จึงต้อง re-derive สายนี้จากอิมเมจ
- ค้น gamedata แล้ว: **เจอ**ชั้น Lua รวม 97 call sites (`Player.CastSkillAt` 69, `Trigger.CastSkillXYZ` 11, `Trigger.CastSkill` 9, `Trigger.CastSkillBy` 5, `Party.CastSkillAt` 3) ใน `PF_GAMEDATA_LUA_API.tsv`; ไม่ใช้เป็นหลักฐาน wire direction เพราะยังไม่มี crosswalk จากชื่อ Lua API ไปชื่อ vital

## คำตอบ objective ประโยคเดียว

> **registrar `0x005F3DF0` ไม่ได้ถือ dispatch ของ outbound: มันเก็บ prototype ใน tree สำหรับ `CreateById` ของ collection READ แล้วส่งต่อ vtable `+0x1C` handler; `PickupTerrainThing` ซึ่งเป็น outbound control ก็ถูก register ใน tree นี้ แต่ outbound จริงเกิดจาก producer `0x006B0639` → submit `0x005DD800` นอก tree ดังนั้นวิธี registrar จำแนก control ว่า outbound ไม่ได้ ⇒ จ็อบ 0 ตก, ตัดแนวนี้ และ RE-056 เข้าเกณฑ์จบเลน static ถาวร**

นี่ไม่ใช่คำตัดสินว่า `TriggerCastSkillVital` เป็น inbound หรือ outbound; เป็นคำตัดสินตามตัวเลือกที่ใบอนุญาตว่า registrar line ไม่ใช่ outbound discriminator

## Gate ก่อนใช้ตาราง

- image `GameClient\GameClient.local.bin`: size `14,759,424`, SHA256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, PE32 ImageBase `0x00400000`
- `PickupTerrainThing` serializer `[0x005E5E30,0x005E5E83)`, file `[0x001E5230,0x001E5283)`, SHA256 `8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066` — ตรง TSV
- `TriggerCastSkillVital` serializer `[0x00600A60,0x00600AD7)`, file `[0x001FFE60,0x001FFED7)`, SHA256 `396200629ab4082b8eef730dda809124f5df8eca6f0ced5419d7a2ac7e3500ec` — ตรง TSV

verifier ที่มีอยู่ `tools\verify_damage_model_encoder.py --binary ..\GameClient\GameClient.local.bin` รัน exit 0, `350 guards PASS, skipped 0`; ใช้เป็น independent guard ของ registrar/reader/tree spans เท่านั้น ไม่ใช้ผล damage/scenario เป็นคำตอบทิศทางใบนี้

## จ็อบ 0 — วิธี registrar กับตัวควบคุม

### 1. ตัวควบคุมถูก register จริง แต่ registration ไม่ได้แปลว่า outbound

`PickupTerrainThing` vtable `[0x00F3005C,0x00F30080)`:

```text
+0x10 getter      0x005E46A0
+0x14 factory     0x005EB0D0
+0x18 serializer  0x005E5E30
+0x1C handler     0x005EF640
+0x20 gate        0x00710440 (mov al,1; ret 4)
```

จุดสร้าง prototype และ register, VA `0x005EE610`, file offset `0x001EDA10`, hex ±16:

```text
00 88 58 04 89 58 08 89 58 0C 88 58 10 88 58 11
C7 00 5C 00 F3 00 89 58 14 88 58 18 EB 02 33 C0
50 E8 CA 57 00 00
```

แปลเฉพาะที่วัดได้: `C7 00 5C 00 F3 00` ใส่ vtable `0x00F3005C`, `50` push prototype, `E8 CA570000` ที่ `0x005EE621` call `0x005F3DF0`

`TriggerCastSkillVital` ก็เข้าตารางเดียวกัน: block `[0x006014E0,0x0060164A)`, จุด vtable `0x006015A8`, push ที่ `0x006015BD`, call registrar ที่ `0x006015BE`. การที่ control และ target ถูก register เหมือนกันจึงยังจำแนก natural direction ไม่ได้

### 2. registrar เก็บอะไร ที่ไหน

`RegisterVitalPrototype` `[0x005F3DF0,0x005F3E11)`, file `[0x001F31F0,0x001F3211)`, SHA256 `7b932cd7c54512c0359344d998e7c7adfdbf6cb790e6b1fc4cd57c8080d35772`:

```text
005F3DF8  8B 01             mov eax,[ecx]
005F3DFA  8B 50 10          mov edx,[eax+0x10]       ; getter wire id
005F3DFD  51                push ecx                 ; prototype
005F3DFE  FF D2             call edx
005F3E00  0F B7 C0          movzx eax,ax
005F3E03  50                push eax                 ; u16 id
005F3E04  E8 57 F4 FE FF    call 0x005E3260          ; singleton [0x01081C44]
005F3E09  8B C8             mov ecx,eax
005F3E0B  E8 A0 FD FF FF    call 0x005F3BB0          ; insert wrapper
```

insert wrapper `[0x005F3BB0,0x005F3C95)` หา key เดิมด้วย `0x00731380`, วาง pair `u16 id + prototype pointer` บน stack แล้วเรียก tree insert `0x00731280` ที่ `0x005F3C5E`

ปลายทาง node copy `[0x00767EA0,0x00767F4C)`, จุด store VA/file offset และ hex:

```text
00767F00  66 8B 08          mov cx,[eax]
00767F03  66 89 4E 0C       mov [esi+0x0C],cx        ; u16 key
00767F07  8B 48 04          mov ecx,[eax+4]
00767F0A  89 4E 10          mov [esi+0x10],ecx       ; prototype pointer
```

ดังนั้น store ปลายทางคือ red-black-tree node `key @ +0x0C`, `prototype @ +0x10`; root/sentinel/count อยู่ใน singleton object ที่ accessor `0x005E3260` คืนจาก global `0x01081C44`

### 3. คนเดิน tree คือ collection READ/CreateById

collection reader `[0x005F3E20,0x005F4070)`, หลังอ่าน vital id ด้วย READ primitive `0x0089A640`:

```text
005F3E98  E8 A3 67 2A 00    call 0x0089A640          ; READ u16 id
005F3E9D  8B 45 C8          mov eax,[ebp-0x38]
005F3EA0  50                push eax
005F3EA1  E8 BA F3 FE FF    call 0x005E3260          ; registry singleton
005F3EA6  8B C8             mov ecx,eax
005F3EA8  E8 53 EF FE FF    call 0x005E2E00          ; CreateById
```

`CreateById` `[0x005E2E00,0x005E2E70)` เรียก tree lookup `0x00731380` ที่ `0x005E2E15`; เมื่อพบ node:

```text
005E2E48  8B 4E 10          mov ecx,[esi+0x10]       ; prototype from node
005E2E4B  8B 11             mov edx,[ecx]
005E2E4D  8B 42 14          mov eax,[edx+0x14]       ; factory slot
005E2E50  FF D0             call eax
```

reader กลับมา call vtable `+0x18` serializer ด้วย READ flag 0 ที่ `0x005F3F39..0x005F3F40`; จากนั้น dispatch loop `[0x005F3840,0x005F38F0)` เดิน object list และ call:

```text
005F3888  8B 42 20 ... FF D0    vtable +0x20 gate
005F38AE  8B 42 1C ... FF D0    vtable +0x1C handler
```

นี่คือ positive chain `registered prototype → lookup by inbound wire id → factory → READ serializer → handler`

### 4. outbound เป็นอีกสาย ไม่เดิน registry tree

collection writer `[0x005F38F0,0x005F39F0)` เดิน object ที่อยู่ใน outbound list อยู่แล้ว และที่ `0x005F3998` ทำ:

```text
8B 16 8B 42 18 6A 01 55 8B CE FF D0
```

คือเลือก vtable `+0x18`, push flag `1`, แล้ว call serializer ฝั่ง WRITE โดยไม่ lookup ID/prototype tree

outbound submit `[0x005DD800,0x005DD887)` รับ object pointer และที่ `0x005DD867`:

```text
8B 0F 53 E8 F1 64 01 00
```

เรียก queue insert `0x005F3D60` ที่ `0x005DD86A`; ไม่มี registry lookup ใน bounded CFG ของ submit

ตัวควบคุม outbound ที่พิสูจน์แล้วมีสายตรง VA `[0x006B062D,0x006B0660)`, file `[0x002AFA2D,0x002AFA60)`:

```text
6A 00 68 0C A9 F0 00 B9 94 13 03 01
E8 52 89 F3 FF                         ; 0x006B0639 create PickupTerrainThing
85 C0 74 16 8B 56 7C 8B 4A 10 50 89 48 14
E8 4F 0B D5 FF 8B C8
E8 A8 D1 F2 FF                         ; 0x006B0653 call outbound submit 0x005DD800
```

registrar method จึงเห็นว่า control “registered/inbound-capable” แต่ไม่พาไปจุด outbound ที่เรารู้ว่ามีจริง วิธีนี้ตกด่าน control ตามนิยามของใบ

## Census และสถานะ indirect

- byte-wise `E8/E9 rel32` census ครบทุก byte offset ใน executable sections `.text` + `.code`: registrar `0x005F3DF0` มี 367 direct call sites; outbound submit `0x005DD800` มี 277; ตัวเลข 277 ตรงการวัดเดิม
- direct edges ของ registrar chain: `0x005F3E04→0x005E3260`, `0x005F3E0B→0x005F3BB0`, insert wrapper `0x005F3C5E→0x00731280`, node link `0x0073110F→0x00767EA0`, reader `0x005F3EA1→0x005E3260` และ `0x005F3EA8→0x005E2E00`
- exact dword refs ของ global `0x01081C44` ทั้งอิมเมจ = 6 จุด และอยู่ใน accessor/destructor span `0x005E3230..0x005E3312`; vtable literal refs: control `0x00F3005C` = 3 จุด, target `0x00F3175C` = 3 จุด
- recursive bounded CFG ของ registrar, insert wrapper, tree insert/link/node copy/lookup, accessor, CreateById, reader, dispatch, writer และ outbound submit รวม 12 spans: decode error = 0 ทุก span; registrar/read chain ไม่มี direct edge ไป `0x005DD800`
- indirect ที่ resolve ได้สำหรับ control/target คือ vtable slots `+0x10/+0x14/+0x18/+0x1C/+0x20` จาก vtable เต็ม 9 slots. **ไม่ได้อ้างว่า exhaustive runtime alias ทั้งอิมเมจปิดครบ**; ไม่จำเป็นต้องเดินต่อ เพราะวิธีล้มกับ control แล้วและใบสั่งให้หยุดก่อนแตะเป้า

## Span SHA ที่ใช้

| span | VA / file offset | SHA256 |
|---|---|---|
| registrar | `[0x5F3DF0,0x5F3E11)` / `[0x1F31F0,0x1F3211)` | `7b932cd7c54512c0359344d998e7c7adfdbf6cb790e6b1fc4cd57c8080d35772` |
| registry insert wrapper | `[0x5F3BB0,0x5F3C95)` / `[0x1F2FB0,0x1F3095)` | `1c81302f0976666fd53707abc9c0cbb3d06e4a389bc9b250cb90fef54162baea` |
| tree insert | `[0x731280,0x731373)` / `[0x330680,0x330773)` | `1cc2ed0b3ddee247735aea34e18e27387d7eb520690eebaf2d25593813506d22` |
| tree node link | `[0x731090,0x73127F)` / `[0x330490,0x33067F)` | `b1dc19e2a7206910a08fdeb8216e8b84c5ec13acc6bd270d024922a413c50f02` |
| node copy/store | `[0x767EA0,0x767F4C)` / `[0x3672A0,0x36734C)` | `8ed9a622ebe918300cb8c0595072cf801300cdef6fa57f539a9ae5ef47eccfa5` |
| tree lookup | `[0x731380,0x73140E)` / `[0x330780,0x33080E)` | `278e3a8ea1657c23bac6f044b40139264cdcd2746008ea5bf7a346ac3be788b4` |
| registry accessor | `[0x5E3260,0x5E3312)` / `[0x1E2660,0x1E2712)` | `2baaa07ec0dcdbcb52bbae9af46a75f070a6136f879726cae303e880cbcb0dd3` |
| CreateById | `[0x5E2E00,0x5E2E70)` / `[0x1E2200,0x1E2270)` | `8c781596a55336ddfedab010cd067d3a547e0ac9b9c12e6fc9e62508d3ffcd78` |
| collection reader | `[0x5F3E20,0x5F4070)` / `[0x1F3220,0x1F3470)` | `fd8ce6b0298e3a46c3ae1760ca71c6d1f60e45bc02cc60d2c2046a03eba1c3ca` |
| inbound dispatch loop | `[0x5F3840,0x5F38F0)` / `[0x1F2C40,0x1F2CF0)` | `ae0195a6790a0788463351378c1a68677fa3099d46f761da344fc17ab9be3f5e` |
| collection writer | `[0x5F38F0,0x5F39F0)` / `[0x1F2CF0,0x1F2DF0)` | `1ab157252e6d08acd4f9bff399c43636e48e35d6cf0281f97ad7aa81a47f36a1` |
| outbound submit | `[0x5DD800,0x5DD887)` / `[0x1DCC00,0x1DCC87)` | `965efce3f8510ec9418168ae699df19851e822f59a1d58830750bedf2b7159af` |
| Pickup vtable | `[0xF3005C,0xF30080)` / `[0xB2E45C,0xB2E480)` | `35f988511f5e5ae49b12e0d78a5aa9da9c9ef922a0365c8e8e8d773ebc6f0d9d` |
| Trigger vtable | `[0xF3175C,0xF31780)` / `[0xB2FB5C,0xB2FB80)` | `4e77af9f3e57aed2237d3570ef8b2c224ec27a38236cdb52e6b9132fda48fde0` |
| Trigger registration block | `[0x6014E0,0x60164A)` / `[0x2008E0,0x200A4A)` | `27287b90a943159464eb86cede5d2a12b0b1b231b9e77b52637d6e398b29e288` |
| Pickup outbound producer snippet | `[0x6B062D,0x6B0660)` / `[0x2AFA2D,0x2AFA60)` | `01fb40ef73101b9aaca3409c278d1e17b6f33397d053fa502533a7f686d41a01` |

## สถานะจ็อบและเกณฑ์จบ

- จ็อบ 0: **FAIL ที่วิธี** — registrar line จำแนก control เป็น outbound ไม่ได้
- จ็อบ 1: ปิดได้เฉพาะโครง registrar/store/walk ที่จำเป็นต่อการตัดสิน method failure
- จ็อบ 2: **ไม่ได้รันตามคำสั่ง** เพราะจ็อบ 0 ตก; ไม่ให้ direction ของ `TriggerCastSkillVital`
- จ็อบ 3: คำตอบ terminal ข้างต้น + census status ครบ

ตามเกณฑ์จบของใบ: ปม `TriggerCastSkillVital` ออกจากเลน static อย่างถาวร; ขั้นต่อไปคือ observe-only attended probe ที่เขียนไว้แล้วใน `Pirate Force ServerProject\reports\PF_SKILL001_TRIGGER_AND_STATE_STATIC_CHECKPOINT_20260816.md`. รอบนี้ไม่เปิดใบใหม่เอง

## SHA256 read-only inputs ก่อน–หลัง

ทุกไฟล์ที่พึ่งด้านล่างเปิดอ่านอย่างเดียวและ final re-hash ต้องตรงค่าก่อนเริ่ม binary walk:

| ไฟล์ | SHA256 ก่อน = หลัง |
|---|---|
| `GameClient\GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external\00_SEARCH_HERE_FIRST.md` | `6f6c092c0af1363afa4fd03bf21c053991b5f985ec17587a8e1d2d96edb1a459` |
| `external\PF_PROTOCOL_REGISTRY.tsv` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |
| `external\PF_SERIALIZER_FIELDS.tsv` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |
| `gamedata\00_SEARCH_HERE_FIRST.md` | `f19db140593f1a73d2abb0b3b9c141b2082bea499e6b092f671c45f810ea2153` |
| `gamedata\PF_GAMEDATA_LUA_API.tsv` | `0e4c42dcac8142d572b6a8c248aa1c229df40a94677a026ad80e0e8665294cad` |
| `reports\PF_DAMAGE_ENCODER001_OUR_OWN_HIT_RESULT_20260819.md` (cross-check only) | `b0c6b623f3d60ce4ad5ad294874a8ce70fabba0cdd9905e3de84358160340b16` |
| `tools\verify_damage_model_encoder.py` (guard only) | `5d45d45d6b38cb8875e7e15761e3a369e4045233dacc2b2ad5b9babd72df40c5` |

## nonclaims

- static image พิสูจน์โครงทางที่มีในอิมเมจ ไม่พิสูจน์ว่า runtime เดินสายใดจริงตอนร่ายสกิล
- method failure ไม่ใช่หลักฐานว่า `TriggerCastSkillVital` เป็น inbound, outbound, รับอย่างเดียว หรือ client ไม่ส่ง
- 97 Lua call sites พิสูจน์เพียงว่ามีสคริปต์สั่งร่ายสกิล; ไม่ใช่หลักฐาน wire และยังไม่มี API↔vital crosswalk
- W/R rows และ vtable ที่มีทั้ง serializer/handler เป็น capability ไม่ใช่ natural direction
- direct/CFG census ที่รายงานไม่ใช้ linear disassembler เป็นหลักฐานของผลลบ; negative claim จำกัดอยู่ที่ bounded registrar method ที่ล้มกับ control
- ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล
- ชั้น client-observable ว่างเปล่าโดยเจตนา; ไม่มีการเปิดเกม


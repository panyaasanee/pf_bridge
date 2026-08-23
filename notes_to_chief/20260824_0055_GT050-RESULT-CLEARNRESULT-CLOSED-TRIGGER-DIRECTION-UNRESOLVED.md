[ถึง: chief cloud (cc) และ Panya · จาก: เซสชันผู้ช่วย local static-on-bridge]

# GT-050 SKILLCAST-WIRE-001 — RESULT: jobs 1–3 ปิด; direction/trigger ยังไม่ปิดอย่างซื่อสัตย์

- เวลา: 2026-08-24 00:46–00:55 `+07:00`
- server clone commit ที่อ่าน: `1e0b20bd240b27f9a234ff0e4f3a45a353d7634e`
- ไม่บูต client/server, ไม่แตะ `LOCK_GAME`, canonical DB, queue หรือ continuation และไม่มีหลักฐาน client-observable
- สถานะที่เสนอ: **PARTIAL STATIC / BOUNDED NEGATIVE** — span/re-derive และ `CLearnSkillResultVital` ปิดได้; `TriggerCastSkillVital` ยังตัดสิน natural direction และ input/timer trigger ไม่ได้

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: **เจอ** `TriggerCastSkillVital`, `CLearnSkillVital`, `CLearnSkillResultVital` ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv`; รวม field rows `6 + 4 + 20 = 30` แถว
- ค้น gamedata แล้ว: **เจอ** `gamedata\tables\CONSTDATA_TH__SKILL_CONTEXT.tsv` จำนวน 2,165 data rows แต่ **ไม่เจอ** literal `TriggerCastSkillVital` และตารางข้อมูลนี้ไม่ตอบ wire direction/trigger

## Objective — คำตอบสั้น

1. แถวส่งมอบของ `TriggerCastSkillVital` และ `CLearnSkillVital` ตรง span SHA จริง และ re-derive ปฏิปักษ์ได้ไฟล์ TSV เหมือนต้นฉบับทั้งไฟล์
2. `CLearnSkillResultVital` ปิด UNKNOWN ได้: nested body คือ `count u16/tag 0x12` แล้วตามด้วย `N` records ขนาด 12 ไบต์ `(u32/tag 0x14, u16/tag 0x12, u32/tag 0x14)` และปิดท้าย `u8/tag 0x0B @ object+0x2C`; `_invalid_parameter_noinfo` ทั้ง 7 จุดเป็น container-invariant/error calls ไม่ใช่ wire fields และ `0x0077FC30` เป็น vector append หลัง READ ไม่ใช่ serializer
3. `TriggerCastSkillVital` มีทั้ง W/R codec และมี inbound-capable consumer `0x00601810`, แต่ static census พบเพียง default/pool factory, vtable registration และ consumer ที่ส่ง candidate เข้า local slot setter `0x00449110` — **ไม่พบ chain ที่ object เข้าสู่ outbound vital submit `0x005DD800`** และยังปิด indirect generic-registry producer ไม่ครบ จึงห้ามสรุปว่า client ส่งจริง, รับอย่างเดียว, หรือ trigger เป็น input/timer

## Job 1 — span SHA gate: PASS

- `TriggerCastSkillVital` serializer `[0x00600A60,0x00600AD7)`, file `[0x001FFE60,0x001FFED7)`, len 119, SHA `396200629ab4082b8eef730dda809124f5df8eca6f0ced5419d7a2ac7e3500ec`
- `CLearnSkillVital` serializer `[0x00755AC0,0x00755B13)`, file `[0x00354EC0,0x00354F13)`, len 83, SHA `b99487413ffa79784deda46283aafc2f3954d98a85362d35304b745d6c062fc4`
- ทั้งสองค่าเท่ากับ pin ในใบงาน จึงผ่าน gate ก่อน re-derive

## Job 2 — adversarial re-derive: PASS

รันสำเนา frozen extractor SHA `0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e` ในไดเรกทอรีใหม่ `tools\gt050_rederive_20260824_0046\` กับอิมเมจเดิม ผล exit 0:

- `PF_PROTOCOL_REGISTRY.tsv` source/re-derived SHA เหมือนกันทั้งไฟล์: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv` source/re-derived SHA เหมือนกันทั้งไฟล์: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_TAG_CENSUS.tsv` source/re-derived SHA เหมือนกันทั้งไฟล์: `63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a`
- target rows source/re-derived: `TriggerCastSkillVital 6/6`, `CLearnSkillVital 4/4`, `CLearnSkillResultVital 20/20`

## Job 3 — `CLearnSkillResultVital`: CLOSED

### Codec ที่พิสูจน์ได้

- top serializer `[0x00756100,0x00756156)`, file `[0x00355500,0x00355556)`, len 86, SHA `c6a66b70cc80a48b84ecc433f10aa7696eb8c2a261affd677692a6ab9c90fe94`
- WRITE เรียก nested helper ที่ `0x00756114 -> 0x00755D30`, แล้วเขียน trailing `u8/tag 0x0B @ +0x2C` ที่ `0x00756126`
- READ เรียก nested helper ที่ `0x00756134 -> 0x00756070`, แล้วอ่าน trailing `u8/tag 0x0B @ +0x2C` ที่ `0x00756146`
- nested WRITE loop ที่เป็น wire จริง `[0x00755D30,0x00755E1E)`, file `[0x00355130,0x0035521E)`, len 238, SHA `35eaeb4718fc91dcc4b22ab13a0b1d9557834f83c735befb01cfe01bc6654944`
- frozen extractor envelope เดิม `[0x00755D30,0x00755E89)`, file `[0x00355130,0x00355289)`, len 345, SHA `011118239d65084ff68ade56c2d408601eb418d542f50827bf5d91dd53a84d04`; envelope นี้คร่อม `INT3` ที่ `0x755E1E..1F` ไปถึง constructor ถัดไป จึงใช้ exact loop bound ด้านบนอธิบาย semantics แต่ยังรักษา SHA pin เดิมครบ
- nested READ loop `[0x00756070,0x007560FB)`, file `[0x00355470,0x003554FB)`, len 139, SHA `0c78744ea4659a8a0d36a8a4015a4a9ce5904f15ccea7e8b14ccdcfbad70f3b3`

ลำดับ wire ที่ W/R ตรงกัน:

```
u16 tag 0x12  count
repeat count times (record stride = 12):
  u32 tag 0x14  record+0
  u16 tag 0x12  record+4
  u32 tag 0x14  record+8
u8  tag 0x0B  object+0x2C
```

### ปิด UNKNOWN อย่างไร

- W rows ที่ extractor ติด UNKNOWN 7 จุด resolve ไป IAT `0x00C3B4C0`, `MSVCR90.dll!_invalid_parameter_noinfo`; จุด `0x755D72`, `0x755D8C`, `0x755DA2`, `0x755DB6`, `0x755DBF`, `0x755DEF`, `0x755DFC` อยู่บน branch ตรวจ begin/end/null/range ของ container รอบ loop และไม่มี stream primitive เป็น callee จึงเป็น error/invariant calls ไม่ใช่ field
- R row `CALL_UNCLASSIFIED:0x0077FC30` เกิดหลังอ่าน stack record ครบสามสมาชิกที่ `0x7560BA/CA/DA`; helper `[0x0077FC30,0x0077FCCD)`, file `[0x0037F030,0x0037F0CD)`, len 157, SHA `818766520f80c246ef0d928f72d4306438d2654e8e2334aebbab2a4cb017b595` คำนวณ vector size/capacity ด้วย stride 12 แล้ว append record
- fast copy helper `[0x004B0E90,0x004B0EBD)`, file `[0x000B0290,0x000B02BD)`, len 45, SHA `fb821784cc36093681cfff3b4670bfc12d9f0ad143a8a31cb59ea9f6c1d5b4c5` คัด `qword + dword` = 12 ไบต์ต่อ record
- grow/insert helper `[0x0077FB60,0x0077FC2E)`, file `[0x0037EF60,0x0037F02E)`, len 206, SHA `e67c66f5f20598af5c2b5d65675fac3077ee2dbb00c81f92daeaad44fa69e811`; reallocation descendant `[0x0077F520,0x0077F7C8)`, file `[0x0037E920,0x0037EBC8)`, len 680, SHA `955b36e203fb21c7fc02f3de2069a1ea2bb9441cc7b0ccc8e31cd2e9a7222864`; recursive CFG ทุกช่วง decode error = 0 และไม่มี call ไป `0x0089A600/0x0089A640`
- cross-check verifier เดิม `tools\pf_stats_progression_static.py` รันกับอิมเมจนี้ exit 0, `guards run: 99`, และยืนยัน nested-list codec เดียวกัน

**Nonclaim ของ Job 3:** ยังไม่ตั้งชื่อความหมายของสมาชิก record ทั้งสามหรือ trailing byte; ปิดเฉพาะ wire shape และจำแนก UNKNOWN calls

## Job 4 — `TriggerCastSkillVital`: bounded negative, direction/trigger UNRESOLVED

### สิ่งที่ปิดได้

- vtable window `[0x00F3175C,0x00F3177C)`, file `[0x00B2FB5C,0x00B2FB7C)`, len 32, SHA `a50183d65fe077576f28ea2340a0bb74f11c84af7dda12abf5e8d58e7d3b8af3`
- slots: `+0x10 getter 0x00600A40`, `+0x14 factory wrapper 0x00601220`, `+0x18 serializer 0x00600A60`, `+0x1C consumer/handler 0x00601810`
- pool/default factory `[0x00600FC0,0x006010CD)`, file `[0x002003C0,0x002004CD)`, len 269, SHA `fb220fb3ae230c3c2fc8dc8565d3f43bd82143b847633dde850c4a44e523be52`
- factory wrapper `[0x00601220,0x00601232)`, file `[0x00200620,0x00200632)`, len 18, SHA `67ccb5e69a92e8b0abd5b52f86c26b11c4dfc89d32bf28b33eb641d1423eaaf1`; exact direct edge `0x60122C -> 0x600FC0`
- registration block `[0x006014E0,0x0060164A)`, file `[0x002008E0,0x00200A4A)`, len 362, SHA `27287b90a943159464eb86cede5d2a12b0b1b231b9e77b52637d6e398b29e288`; literal `0xF3175C` at `0x6015AA` แล้วส่ง prototype เข้า generic registrar `0x5F3DF0`
- consumer `[0x00601810,0x0060189A)`, file `[0x00200C10,0x00200C9A)`, len 138, SHA `6201c759b1a195bd941e00aa6ee4d0d554c3c1c4e14fee0fb2eccec6f74a9716`: เมื่อ singleton `0x01032EC4` มีค่า จะอ่าน raw `+0x14` และ `+0x18`, สร้าง candidate ขนาด `0x38`, แล้วเรียก `0x00449110` ที่ `0x601880`; ไม่มี call ไป stream primitive
- local submission/slot setter `[0x00449110,0x0044914B)`, file `[0x00048510,0x0004854B)`, len 59, SHA `720ac2aa5d3ef945c47ceab923c1ad8b8aa6b97caade03e2f1060566ac7e879f`: เปลี่ยน pointer ที่ singleton `+0x3DC` และเรียก destructor เดิมผ่าน vtable; ไม่ใช่ outbound vital queue
- generic outbound vital submit สำหรับเทียบ `[0x005DD800,0x005DD887)`, file `[0x001DCC00,0x001DCC87)`, len 135, SHA `965efce3f8510ec9418168ae699df19851e822f59a1d58830750bedf2b7159af`

### Census และเพดานหลักฐาน

- recursive CFG ของ focal spans decode error = 0; exec sections ที่กวาด = 2 (`.text`, `.code`)
- byte-wise E8/E9 census ทุก byte offset พบ exact direct call ไป pool factory เพียง `0x60122C`; ไม่พบ exact direct caller ของ serializer `0x600A60` หรือ consumer `0x601810`
- executable dword refs ของ vtable literal `0xF3175C` มี 3 จุดเท่านั้น: `0x60101B`, `0x60109D` (default/pool allocation) และ `0x6015AA` (registration)
- all-section dword refs พบ getter/serializer/handler/factory wrapper อย่างละ 1 จุด และทั้งหมดคือ slots ใน vtable นี้; id-global `0x0108284C` มี executable refs 2 จุด
- full E8/E9 candidate census ไป `0x005DD800` พบ 277 byte-offset candidates และไป `0x00449110` พบ 26 candidates; positive decoded edge ของ consumer คือ `0x601880 -> 0x449110` เท่านั้น ไม่มี decoded xref chain จาก Trigger factory/vtable ไป `0x5DD800`
- อย่างไรก็ดี generic registry เรียก factory/codec/consumer แบบ indirect ผ่าน object/vtable ได้ และ static proof เดิม `reports\PF_SKILL001_TRIGGER_AND_STATE_STATIC_CHECKPOINT_20260816.md` ก็หยุดที่เพดานเดียวกัน: ไม่พบ exact local UI/hotkey producer แต่ยัง exclude indirect generic-registry producer ไม่ได้; observe-only probe เดิมยังไม่เคยรัน live

ดังนั้นประโยคทิศทางที่ซื่อสัตย์คือ:

> `TriggerCastSkillVital` **มี inbound-capable READ+consumer path** แต่ static image นี้ยังไม่พิสูจน์ natural direction; ไม่พบ proven WRITE producer/entry to `0x005DD800`, และ indirect census ยังไม่ปิด generic-registry dispatch จึงยังระบุ input/timer trigger หรือค่าต้นทาง `+0x14/+0x16/+0x18` ไม่ได้

นี่ไม่เท่ากับ “client ไม่ส่ง” และไม่เท่ากับ “รับอย่างเดียว”

## Probe ที่เพิ่มเพื่อทำซ้ำ

- `Pirate Force ServerProject\tools\pf_gt050_skill_wire_probe.py`
- SHA ตอนจบ `d429c230b77f1578b3011085db52f73313d6676fe32c49005aff59af6bd09420` (ให้ final audit re-hash อีกครั้ง)
- run ล่าสุด: expected span guards `5/5`, executable sections `2`, constructor candidates `3`, recursive decode errors ของ focal spans `0`, exit `0`
- สคริปต์/ผล re-derive อยู่ใต้ `tools\` ตามเขตที่อนุญาต; `.gitignore` ครอบ `/tools/*` จึงไม่ปรากฏใน tracked diff และไม่มี commit/push

## SHA read-only inputs ก่อน/หลัง

ค่าด้านล่างตรงกับค่า pre-run ทุกตัว และ final re-hash:

- `GameClient\GameClient.local.bin` — `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `PF_PROTOCOL_REGISTRY.tsv` — `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv` — `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_TAG_CENSUS.tsv` — `63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a`
- `PF_FIELD_VALIDATION.tsv` — `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- `PF_RUNTIME_CLASSMAP.tsv` — `c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985`
- `PF_INPUT_INVENTORY.tsv` — `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- `PF_DATA_EVIDENCE.tsv` — `fbcd7bf14fd33c7340c6fd70f4a0aa5f1a6f7719c429335540383eab1ccf5b1f`
- `pf_extract_protocol.py` — `0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e`
- `gamedata\tables\CONSTDATA_TH__SKILL_CONTEXT.tsv` — `41d642c535bfefd9a560cb8fc92a530a51bd3ca55168eddae93cfd64dca7c4f4`

## Nonclaims บังคับ

- ไม่ตั้งชื่อความหมาย raw Trigger fields `u16/u8/u32`; ไม่เดา skill id/target/level
- ไม่อ้างว่า static path เคยรันจริง, ไม่อ้างว่าหน้าจอร่ายสกิล, MP/cooldown/animation/damage เปลี่ยน
- ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส และไม่อ้าง server ต้นฉบับ
- ไม่เขียน encoder/module, ไม่ synthesize packet, ไม่แตะเกม/DB/capture

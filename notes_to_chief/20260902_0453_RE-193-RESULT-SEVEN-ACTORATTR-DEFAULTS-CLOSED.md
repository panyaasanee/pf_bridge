ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย — ผล RE-193 (ผู้บริโภค LANE-DB; static bridge)

# RE-193 RESULT — DONE / PASS: client constructor defaults closed for all seven ActorAttr fields

- Ticket START: `2026-09-02T04:47:00+07:00`
- Result time: `2026-09-02T04:53+07:00`
- Queue SHA-256 at start: `cb3088d9b016ac4edb73eba8fd38f1820e6638bc74587a5302fb6a996fcea694`
- Static/read-only only: no game/server boot, no `LOCK_GAME`, no canonical DB, no source/queue/external/gamedata edit.

## Mandatory searches

- ค้นใน `pf_bridge\external\` แล้ว: scope = 2,683 files / 930,201,065 bytes; terms `nameboard_key`, `wstr_B0`, `u8_18C`, `q_140_pairB`, `u8_9B_pairB`, `wstr_CC`, `u16_1B0`, `default_writer_va`. พบตาราง/เครื่องมือที่เกี่ยวข้อง ได้แก่ `PF_ATTR_INHERITANCE.tsv`, `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_A2_ATTR_FIELD_DELTA.tsv` และตัว rederive; ตาราง semantics ปัจจุบันไม่มีแถวคำตอบของ 7 ฟิลด์นี้ จึง re-derive จาก IMAGE โดยตรง ไม่ได้คัดลอกค่าเดิม.
- ค้นใน `pf_bridge\gamedata\` แล้ว: scope = 1,109 files / 15,319,585 bytes; ไม่พบคำทั้งเจ็ดหรือ crosswalk/default ของฟิลด์เหล่านี้. ผลลบจำกัดเฉพาะ extracted gamedata tree ไม่ใช่ whole-program negative และไม่ได้ใช้เป็นหลักฐานหลักของค่า default.

## Provenance ของวัตถุและ constructor

`ActorAttr` มี chain `PcRefObject > Attribute > DBAttribute > BasicAttr > ActorAttr` และ type descriptor `.?AVActorAttr@@`. Constructor อยู่ที่ VA `[0x00464BE0,0x00464E39)`; base call ที่ `0x00464C0B`; exact 601-byte constructor SHA-256 `e83ae4a601a4ec700326598d6329e4b34cd2f4cf78dcf17d639d8df8e1f1096a`.

Recursive entry-follow ปิดครบ 124/124 instructions และ 601/601 bytes. Constructor ตั้ง presence masks `+0x1B4` และ `+0x1B8` เป็น `0xFFFFFFFF` ที่ `0x00464CA0/0x00464CA6` และตั้ง `+0x1BC = 1` ที่ `0x00464E1C`; ดังนั้นค่าด้านล่างเป็น field defaults ที่ live/present จริง ไม่ใช่ค่าศูนย์จากหน่วยความจำที่ยังไม่ถูกเลือกใช้.

## Jobs 1–7 — CLOSED / EXACT

| x | Resident field | Client default at construction | Exact writer/provenance |
|---:|---|---|---|
| 14 | `+0x090`, u32 `nameboard_key` | `0` | write VA `0x00464CB4`; span `[0x00464CB4,0x00464CBA)`, bytes `89 9E 90 00 00 00`, SHA `ff438d022d4c896b666c67385e0ff83bbd5882087ccd79ca3ce90c9ef153eee3` |
| 25 | `+0x0B0`, `std::wstring` | empty string `L""` (length 0) | default ctor span `[0x00464C12,0x00464C2D)`, SHA `27e881d66beeab85dc2d97154b919649e6ea55e0b4026f66b71632fb830ec952`; assignment call at `0x00464D12` from literal VA `0x00F0930C` |
| 36 | `+0x18C`, u8 | `0` | write VA `0x00464DCA`; span `[0x00464DCA,0x00464DD0)`, SHA `340f928f16a30e228e6f7009fc3841458ad445a0820320ef3d6613da3016b7af` |
| 41 | `+0x140`, u64 `q_140_pairB` | `0x0000000000000000` | zero dword writes at `0x00464D7C` and `0x00464D82`; span `[0x00464D7C,0x00464D88)`, SHA `e613b25a716496800f7d08f9e8a0edc5afdff67d8a7a9c16b0e843971c5d97bf` |
| 42 | `+0x09B`, u8 `u8_9B_pairB` | `0` | write VA `0x00464DAF`; span `[0x00464DAF,0x00464DB5)`, SHA `d0283982242d8d26b87ff02c5ab38661abe8b3d988f7d18aed90e52e574d5607` |
| 43 | `+0x0CC`, `std::wstring` | empty string `L""` (length 0) | default ctor span `[0x00464C2D,0x00464C40)`, SHA `816e9ef7c526cc034661797320db2c51217290cede5a434d79460b2e655a2dcd`; assignment call at `0x00464D1F` from the same literal |
| 54 | `+0x1B0`, u16 | `0` | write VA `0x00464DA8`; span `[0x00464DA8,0x00464DAF)`, SHA `df040177bba68f6785278796da57e3c0c135b2618010393029650da81cafe46a` |

The imported symbols distinguish the wstring operations: IAT `0x00C3B478` is the default constructor and `0x00C3B47C` is `operator=(wchar_t const*)`. Literal `[0x00F0930C,0x00F0930E)` maps to file `[0x00B0770C,0x00B0770E)`, bytes `00 00`, SHA-256 `96a296d224f285c67bee93c30f8a309157f0daa35dc5b87e410b78630a09cfc7`; this proves empty string rather than inferring it from the field name.

## Shared-bit behavior for x41/x42 — CLOSED for the standard ActorAttr codec

The exact ActorAttr wire codec is VA `[0x00466230,0x00466C6F)`, file `[0x00065630,0x0006606F)`, 2,623 bytes / 734 instructions, SHA-256 `ff1bf8f6b8beb33d6c070d4bbb2d37f8d83aaa93545a38397bf58f8acf72a5ed`. Recursive CFG covers 734/734 instructions and all bytes.

- Write side: one `0x08000000` gate at `0x004665AC`, then qword site `0x004665BA` and u8 site `0x004665CC`, with no intervening branch. Pair span `[0x004665AC,0x004665DC)`, SHA `5142d7dc95f866016e11c355a0413d0fac60ef365806c6f88f46a21cf9a4e0a3`.
- Read side: one gate at `0x00466AC9`, then qword site `0x00466AD7` and u8 site `0x00466AE9`, again with no intervening branch. Pair span `[0x00466AC9,0x00466AF9)`, SHA `b1351daef0fac04b149d4cea14209f7346e8fd274b17c9bd3229ae93c27197d5`.
- Change detection compares both qword halves and then the u8, OR-ing the same mask when either field differs: span `[0x00465CB7,0x00465CEB)`, SHA `15511ff44b853579514c901789d195e4e5098c73f0a98d392d89f7c483f3b0e0`. On wire the qword is tag `0x32`, len 8, followed by the u8 tag `0x0B`, len 1.

Conclusion: the standard ActorAttr wire codec serializes/deserializes x41 and x42 atomically under the shared bit. The constructor initializes both independently but unconditionally to zero.

## Input/output integrity

- `GameClient.local.bin`: 14,759,424 bytes; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `PF_ATTR_INHERITANCE.tsv`: SHA-256 `e2ede4e2af6b86b47bc557e2036c4fde8ecefaf6853da85f88b0f66702ce2544`.
- `PF_ATTR_FIELD_SEMANTICS.tsv`: SHA-256 `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`.
- `PF_A2_ATTR_FIELD_DELTA.tsv`: SHA-256 `44f80d6aa975dfe030a0e537d5166aaa9e051c4d55f693d7e724fa2b17b19c1f`.
- `pf_rederive_attr_semantics.py`: SHA-256 `c7d6c560f0848b3eb0edc34bb147a66d5c3fc1661ed0d88fb9c4065ca0a7528c`.
- `Pirate Force ServerProject\src\pirateforce_foundation\gm\attr_wire.py`: SHA-256 `d8992915867506bc33c0e107c57cf3fb5124c2f1b92973f4f381a00573a994b7`.
- `PF_SERIALIZER_FIELDS.tsv`: SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`.
- All named source inputs and the queue are to be rehashed at closeout; only this result letter and runner bookkeeping are written.

## Nonclaims

- ค่า zero/empty ที่พิสูจน์นี้คือค่า ณ `ActorAttr` object construction; ไม่ได้อ้างว่าไม่มี runtime writer, update packet, script, หรือ subclass path ใดเปลี่ยนภายหลัง.
- การที่ x41/x42 อยู่ใต้ shared codec bit ไม่ได้พิสูจน์ว่า every in-memory writer ต้องแก้สองฟิลด์พร้อมกัน; claim จำกัดเฉพาะ standard codec ที่ถอดครบและ constructor นี้.
- ไม่จับคู่กับ server field ใดเพียงเพราะ ID/offset เท่ากัน; ใบนี้ให้เฉพาะ typed resident offset, constructor provenance และ codec gate ที่มี crosswalk ตรง.
- ไม่อ้าง client-observable rendering/gameplay effect ใด ๆ; งานนี้เป็น static IMAGE/DATA/source evidence เท่านั้น.

## BUILD_IMPACT

`BUILD_IMPACT: LANE-DB may use exact construction defaults x14=0, x25=L"", x36=0, x41=0, x42=0, x43=L"", x54=0 when it deliberately emits these fields. Existing omit/no-mask strategy remains safe and does not need to wait for this result. If the shared 0x08000000 bit is emitted through the standard ActorAttr codec, x41 and x42 must travel together. No DB/attr-wire/source patch was made by the RE runner.`

[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-075 RESULT — DONE / PASS: FALSE-BRANCH NO-OP + ZERO-FIELD GATE

เวลา: `2026-08-25T23:18:08+07:00`  
ใบ: `RE-075 RETURNSELECT-APPLY-0x5F1190-WHAT-DOES-IT-DO-001`  
หมวด: `STATIC-ON-BRIDGE` · ไม่บูต server/client · ไม่มีชั้น client-observable  
งานที่ปิด: `S0 + T1-T4` · `T5` ไม่รัน เพราะ optional และ objective ปิดแล้ว  
HEAD ที่บูต: **ไม่มี — ไม่ได้บูตอะไร**

## คำตอบ objective (ประโยคเดียว)

`ReturnSelectServerVital 0x709E` apply `0x005F1190` อ่าน live state จาก `[0x1093198]+0x34C` แล้ว gate ด้วย `cStateCreateActor`; ถ้า live state เป็น null หรือไม่ใช่ `cStateCreateActor` จะตก common return ที่ `0x005F11CB` (`pop edi; mov al,1; pop esi; ret 4`) โดย **ไม่เขียนค่า ไม่เรียก helper `0x004B2A50` และไม่ร้องขอ state transition** — ตรงกับสภาพของ `GT-033` variant B/C ที่อยู่ใน map; ถ้า gate แรกผ่าน helper ยัง gate ซ้ำว่า vital `+0x14 == 0x1E`, ดังนั้น composition ปัจจุบันที่ส่ง `+0x14 = 0` จะหยุดโดยไม่มี side effect เช่นกัน

## สองช่องบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** — `PF_PROTOCOL_REGISTRY.tsv:73` พิน vtable `0x00F304DC`, serializer `0x005E69F0`, handler slot value `0x005F1190`; `PF_SERIALIZER_FIELDS.tsv:1123-1128` พิน W/R สามฟิลด์ (`+0x14`, `+0x18`, `+0x20`) และ span serializer SHA `1fd36842...567774a`; `PF_FIELD_VALIDATION.tsv:144-145` = W observed 2/VALIDATED, R NOT_OBSERVED; `PF_PROTOCOL_PRIORITY.tsv:73` = CLOSED. Verify serializer span กับอิมเมจจริงแล้วตรง `1fd3684282291e2accb94171f0d532e239d38f736e1cb1455a633e7ad567774a`.
- **ค้น gamedata แล้ว: ไม่เจอ** — ค้น `ReturnSelectServerVital`, `0x709E`, `0x005F1190`, `0xF304DC` ครบทั้ง `pf_bridge\gamedata\`; ไม่มี hit. ใบนี้เป็น control-flow ของ client image ไม่ใช่ข้อมูลเกม

## S0 — ผ่านทุกด่าน

- `GameClient.local.bin`: size `14,759,424` B; SHA ก่อน/หลัง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` ตรง pin
- อ่าน PE section table จากอิมเมจเอง: `.text delta=0x400C00`, `.rdata=0x401C00`, `.data=0x402800`; target `0x005F1190` map ผ่าน `.text` เป็น file offset `0x001F0590`
- 256-byte guards: block 7940 `e10cc482...b123` และ 7941 `e24b47d6...32ff` ตรงทั้งคู่
- vtable slot จริง: dword ที่ `0x00F304F8` (`0xF304DC+0x1C`) = `0x005F1190`
- positive control `tools\pf_ui_state_refresh_static.py` exit `0`, `292 guards / failed 0`
- pinned verifier ใหม่ `staged\re075_static_verify.py` exit `0`, `58 guards / failed 0`

## T1 — complete recursive CFG ของ `0x005F1190`

| field | result |
|---|---:|
| span | `[0x005F1190,0x005F11D2)` |
| file offset | `0x001F0590` |
| length | `66` bytes |
| instructions | `27` |
| decoded bytes / gap | `66 / 0` |
| recursive CFG errors | `0` |
| indirect calls / jumps | `1 / 0` |
| SHA-256 | `4d5815ea8ecf96a963319c33291ab27f526ac6a338cee4f8bfc49928c85812b8` |

first mnemonic = `mov eax,dword ptr [0x1093198]` (`A1 98 31 09 01`) — ไม่ใช่ no-op `B0 01 C2 04 00` ที่ `0x710440`

## T2 — gate และ false branch (ผลชี้ขาด)

ลำดับ byte-backed:

1. `0x5F1190 mov eax,[0x1093198]`; `0x5F1196 mov esi,[eax+0x34C]`
2. null live state: `test esi,esi; je 0x5F11CB`
3. non-null: `call [vtable+0]` เพื่อเอา live-state token → `call 0x4C0110` เอา token ของ `cStateCreateActor` → `call 0x88F2B0` is-a predicate
4. predicate false: `and ecx,esi; je 0x5F11CB`
5. common return `0x5F11CB..0x5F11D2`: `5F B0 01 5E C2 04 00`

false branch จึงไม่มี memory write และข้าม `push edi; call 0x4B2A50` ทั้งก้อน. ค่า return เป็น success (`AL=1`) ไม่ใช่ reject/crash. นี่อธิบายผลลบของ variant B/C ได้โดยไม่ต้องเพิ่มสมมติฐาน: frame อาจถูก dispatch มาที่ apply จริง แต่ apply ไม่มีอำนาจทำอะไรเมื่อ live state อยู่ใน map

## T3 — true branch วัดเป็น side effect เท่านั้น

helper ที่ gate แรกเรียกคือ `0x004B2A50`:

| function | span | instr | gap | CFG errors | SHA-256 |
|---|---|---:|---:|---:|---|
| `0x004B2A50` | `[0x004B2A50,0x004B2AC5)` | 37 | 0 | 0 | `7205682508f650f7f71ebb4e94ba791ad0ca0c2087fbc1c3aa55df434e385e39` |
| object builder `0x004B04A0` | `[0x004B04A0,0x004B05AB)` | 87 | 0 | 0 | `58e9b20c9b9b9e6ed7d46f47381fca9231db3c96bb31141a969dfbd902ae4156` |
| ready helper `0x005DCA40` | `[0x005DCA40,0x005DCB3D)` | 77 | 0 | 0 | `42dff43bacf0b829cbcf85c9b80b23679dc92d68e01a131204b0207f85957798` |
| commit helper `0x005DD890` | `[0x005DD890,0x005DD96E)` | 66 | 0 | 0 | `1a91c8d4885be00506dd5657af2344366dfd60b469ae202d502fafe9cdfd0c1c` |

ผลที่วัดได้:

- ตัวตัดสินแรกของ helper คือ `cmp dword ptr [vital+0x14],0x1E`; ไม่เท่า = `ret 4` ทันที
- เมื่อเท่า `0x1E`: ตั้ง byte `[GetSingleton(0x4011A0)+0xD8] = 1`, เรียก `0x5DCA40`, `Sleep(2000)` ผ่าน IAT `0xC3B1B8`, และหยุดถ้า ready helper คืน false
- ถ้าผ่าน: สร้าง object ผ่าน `0x4B04A0`, copy `+0x18` เป็น dword, `+0x1C` เป็น dword (สองครึ่งของฟิลด์ 8 ไบต์), copy `std::string<char>` ที่ `+0x20` ผ่าน IAT `0xC3B48C`, แล้วส่ง object เข้า `0x5DD890`
- target + direct true helper **ไม่อ้าง** page variable `0x107A2C0`; live state slot `[0x1093198]+0x34C` ถูกอ่านเพื่อ gate แต่ไม่ถูกเขียน
- ไม่พบ wide-string/UI-window literal ใน target/helper. immediate `0xF0A90C` ที่ถูก push มี bytes ASCII `66 69 6C 65 00` = `"file"`, ไม่ใช่ `L"..."`; ไม่ claim ว่า downstream ที่ยังมี indirect จะไม่เปิด UI

ผลใหญ่สุดของ T3: profile ปัจจุบันใน `PF_LOGOUT_RETURN_SELECT001_HYP028_20260820.md` พิน body all-zero (`+0x14=0`) — ค่านี้ไม่ผ่าน `0x1E` gate แม้ client จะอยู่หน้าสร้างตัวละคร

## T4 — reachability ไป `CState::RequestNext 0x4C7320`

- target และ direct true helper ไม่มี direct call ไป `0x4C7320`
- recursive direct-call graph จาก `0x5F1190`, depth สูงสุด 6 / max nodes 128: visited `109` nodes, `3,795` instructions, decoded `11,828` bytes, aggregate gaps `2,592`, direct edges `253`, CFG errors `0`; **ไม่พบ** `0x4C7320`
- แต่มี unresolved indirect calls `105` + indirect jumps `20` ใน downstream graph ⇒ ผลนี้เป็น **BOUNDED NEGATIVE** ไม่ใช่คำอ้างว่าไม่มีเส้นทางทั้งโปรแกรม
- positive control แบบเดียวกันจาก `TeleportVital apply 0x5F14B0`: span `[0x5F14B0,0x5F16F9)`, 163 instructions, gap 0, errors 0, และพบ path ที่ depth 0: `0x5F14B0 -> 0x4C7320` ที่ call site `0x5F16C9`
- สำหรับ **false branch ที่ objective ถาม** ข้อสรุปแข็งกว่า graph: control flow คืนจาก `0x5F11CB` ก่อนเข้า true helper จึงไม่มี downstream graph ให้เดินใน branch นั้น

## T5

ไม่รัน — optional และ objective ปิดจาก T2/T3 แล้ว. vtable slot บนอิมเมจถูกยืนยันใน S0; ใบไม่ได้ต้องการ producer census เพื่อปิด claim

## nonclaims (ติดครบตามใบ)

1. ผลนี้เป็น static image ล้วน ไม่แทนหลักฐาน client-observable ของ `GT-033`; variant B/C เป็นคนละชั้น
2. `handler_va` ในตาราง external คือค่า vtable slot `+0x1C` ไม่ใช่หลักฐาน producer หรือ inbound dispatch
3. uniqueness ของ `0x005F1190` ใน registry ไม่ใช่สัญญาณพิเศษ
4. ไม่ตัดสินว่า `0x709E` ถูก/ผิดในฐานะ trigger; wrong-vital / wrong-field-values / needs-something-alongside ยังแยกกันไม่ออกจาก composition ที่วัด
5. ไม่อ้างอะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดและกู้ไม่ได้ตลอดกาล
6. ไม่ตอบ rider capture W สองเฟรม (`PF_INPUT_INVENTORY.tsv:693/:927`) และไม่ได้เปิดไฟล์ capture สองไฟล์นั้น
7. อ่านเฉพาะ `GameClient.local.bin`; ไม่ verify parity กับ `GameClient.bin`
8. ไม่ join เลขเพราะคล้ายกัน: `0xF304DC`, `0xF304EC`, `0xF304F4`, `0xF304F8` ถูกแยกเป็นคนละช่อง; คำตอบใช้ dword จริงที่ `0xF304F8`
9. T4 downstream เป็น bounded negative เพราะ indirect/gaps ตามตัวเลขข้างบน; ห้ามย่อเป็น “ไม่มี RequestNext ที่ไหนเลย”

## integrity / reproducibility

- source ที่พึ่งก่อน/หลังตรง: image, `blocks_256.tsv`, `pf_ui_state_refresh_static.py`, รายงาน UI_REFRESH + manifest, รายงาน HYP028, helper scriptsเดิม
- external tree: `30 files / 29,900,221 bytes`, fingerprint ก่อน/หลัง `9525161de1f79fe1c4d73f98c39a7e854c946bd0c30c0686d23f2a9854baa837`
- gamedata tree: `1,109 files / 15,319,585 bytes`, fingerprint ก่อน/หลัง `ae16237dbce6c031894e83b4fb0bc0151cdf1f32e52e5d677499eb5ba25ac54d`
- probe ใหม่: `staged\re075_static_probe.py` SHA `efdfeb891373a7dea982b2e35399b5dd9e2faa47474cc04d0f83a7877486c624`
- verifier ใหม่: `staged\re075_static_verify.py` SHA `e770902901f45ea703328a686fe1f4e605216ab2fc8d097498837a9e97e46253`
- verifier draft ครั้งแรกพลาด signature ของ `Sleep` เพราะเว้น instruction `mov bl,al` ระหว่าง `push 2000` กับ IAT call; แก้ guard ให้ตรง listing จริงแล้ว rerun 58/58. ไม่ได้เปลี่ยน input/expected value เพื่อบังคับผล
- ไม่มี `.pyc` ใหม่ของ RE-075; 5 ไฟล์ `.pyc` ที่พบมี mtime เก่ากว่ารอบนี้ทั้งหมด

## static-only audit

ไม่เปิดเกม · ไม่บูต server · ไม่จับ/แตะ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้ source/tools/tests/docs/queue · ไม่ทำ git operation · ไม่เปิดใบใหม่

## สิ่งที่ chief ต้องทำตอนบริโภค

ตามท้ายใบ: amend `docs\HYPOTHESIS_LEDGER.json` evidence gap ของ `HYP-PF-028` ให้ชี้ผล RE-075 นี้; คำตัดสินสถานะของ hypothesis เป็นของ chief/Panya ไม่ใช่ RE runner

[ถึง: chief · COO · LANE-GM | จาก: RE runner local · 2026-08-26T18:11+07:00]

# RE-088 RESULT — PASS/DONE · STRUCTURAL-LAYOUT-PINNED

ใบ: `RE-088 GM-COMMAND-WIRE-001` · หมวด `STATIC-ON-BRIDGE` · ImageBase ทุก VA ด้านล่าง = `0x00400000`

คำตัดสินหนึ่งบรรทัด: layout ระดับไบต์ของ `GM_RunGMCommandVital 0x51E9` และ `GM_RunGMCommandResultVital 0x8C77` ปิดได้ครบตามเกณฑ์ใบจากอิมเมจจริง; `0x51E9` มี outer presence byte แล้ว nested body `u32,u32,u8,wstring,wstring`, ส่วน `0x8C77` มี tagged byte เดียว. ความหมายเชิง semantic ของสาม scalar/สองสตริงและ result byte ยังไม่พิสูจน์ จึง bounded เฉพาะ semantic โดยไม่ลดสถานะ structural PASS.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `PF_PROTOCOL_REGISTRY.tsv` 2 แถว registry, `PF_SERIALIZER_FIELDS.tsv` 22 แถวที่เกี่ยวข้อง (20 ของ command + 2 ของ result), และ `PF_FIELD_VALIDATION.tsv` 4 แถว `NOT_OBSERVED`. จดหมายแก้ `20260826_1741_LANE-GM-CORRECTION-*` ถูกต้อง: ใบเดิมที่ว่า “ยังไม่มีแถว” ล้าสมัยแล้ว จึงเปลี่ยนงานเป็น **verify SHA → re-derive ปฏิปักษ์ → ใช้**.
- **ค้น gamedata แล้ว: ไม่เจอ**ชื่อ vital/id/serializer/global (`GM_RunGMCommandVital`, `GM_RunGMCommandResultVital`, `0x51E9`, `0x8C77`, `0x00729E10`, `0x00729790`, `0x01088F8C`) ใน `pf_bridge\gamedata\`. ขอบเขตที่ค้นคือดัชนี/ตาราง/Lua/scene ทั้ง tree; ถูกคาดหมายเพราะใบนี้เป็น wire codec ไม่ใช่ข้อมูลเกม. “ไม่เจอ” ไม่ได้แปลว่า client ไม่มีข้อความ/คำสั่ง GM ในแหล่งอื่น.

## T0 — `GM_RunGMCommandVital 0x51E9`

### outer serializer

- serializer `[0x00729E10,0x00729EB7)` SHA-256 `541d82f511ba87d444587da9f217ee7eb436431c21e7cfca6dd026d19a8c8554` ตรงอิมเมจจริง; recursive CFG ครบ `167/167` ไบต์, 62 instructions, gap/error `0/0`.
- ฝั่ง W ที่ `0x00729E1F` เปรียบ `[this+0x14] != 0`, `setne al` แล้วเขียน tag `0x0B` ขนาด 1 ไบต์ผ่าน primitive W `0x0089A600` ที่ call site `0x00729E37`.
- ไบต์นี้คือ **presence flag ของ nested object** ไม่ใช่ opcode ย่อย: ถ้าเป็นศูนย์ serializer หยุด; ถ้าไม่เป็นศูนย์จึงเรียก nested serializer `0x00726C20` ที่ `0x00729E48`.
- ฝั่ง R อ่าน flag ผ่าน primitive R `0x0089A640` ที่ `0x00729E65`; ถ้าไม่เป็นศูนย์จึงสร้าง object token `0x00F0A90C` ผ่าน `0x007286E0`, เก็บที่ `[this+0x14]`, แล้วเรียก nested serializer ที่ `0x00729EAC`.

### nested body

- serializer `[0x00726C20,0x00726CB1)` SHA-256 `aa3c7c8d2d92eeee48508da2c26d78e360c612aaa2b682dfb608d7b08493559d` ตรง; recursive CFG ครบ `145/145` ไบต์, 59 instructions, gap/error `0/0`.
- wire order เมื่อ presence=1:

| order | wire form | object field | W/R call sites |
|---:|---|---|---|
| 1 | tag `0x14`, 4 ไบต์ | nested `+0x10` | `0x00726C3B` / `0x00726C42` |
| 2 | tag `0x14`, 4 ไบต์ | nested `+0x14` | `0x00726C55` / `0x00726C5C` |
| 3 | tag `0x0B`, 1 ไบต์ | nested `+0x18` | `0x00726C6F` / `0x00726C76` |
| 4 | `uint32le byte_len + UTF-16LE payload` | nested `+0x1C` | `0x00726C85` / `0x00726C8C` |
| 5 | `uint32le byte_len + UTF-16LE payload` | nested `+0x38` | `0x00726C9B` / `0x00726CA6` |

- string helper W `[0x0089A810,0x0089A875)` SHA `08d6f27f030f3e0f1a32873d296c7f2c35a9d67f547607cf95c2900a60ffdad4`; helper R `[0x0089A880,0x0089A95E)` SHA `2f564cb5d4f68d035d9e60fa1a4a5334b0875262420851f463f3f904e22ad978`; ทั้งคู่ตรงอิมเมจ.

## T1 — `GM_RunGMCommandResultVital 0x8C77`

- serializer `[0x00729790,0x007297B3)` SHA-256 `ad65d125ab8a97db872ae5b2e957280a431d55beb7956050652a2d58dee633e9` ตรง; recursive CFG ครบ `35/35` ไบต์, 11 instructions, gap/error `0/0`.
- layout เดียว: tag `0x0B`, 1 ไบต์ ที่ object `+0x14`; W call `0x007297A3 -> 0x0089A600`, R call `0x007297AB -> 0x0089A640`.
- registry พิน custom handler ของ result ที่ `0x00729F00`, สอดคล้อง natural direction server→client; **ความหมายของ byte `+0x14` ยังไม่พิสูจน์** (ห้ามตั้งชื่อ success/error จากขนาด 1 ไบต์).

## T2 — handler ของ `0x51E9`

- `PF_PROTOCOL_REGISTRY.tsv`: `id_global=0x01088F8C`, serializer `0x00729E10`, handler `0x00A106C0`.
- `[0x00A106C0,0x00A106C5)` = `32 C0 C2 04 00` (`xor al,al; ret 4`) SHA-256 `cc0e3cb106eb0fdec984d44a563d98c3da80700bbb8d2be4e66ebd54a9919626`; recursive CFG 5/5 ไบต์, gap/error `0/0`.
- handler เดียวกันถูกใช้ร่วม 11 message ในทะเบียน ⇒ ยืนยันว่าเป็น **default/no-custom inbound handler** จริง. นี่รองรับ claim แคบว่า client ไม่มี custom inbound interpretation สำหรับ `0x51E9`; ไม่ได้พิสูจน์ว่า chat input เลือกส่ง `0x51E9` เมื่อใด (เป็น `RE-091`).

## T3 rider / bounded result

- มี outer presence flag หนึ่งตัวและ nested scalar 3 + string 2 ตัว; **ไม่พบ field เพิ่มที่พิสูจน์ได้ว่าเป็น sub-opcode แยก**.
- `PF_FIELD_VALIDATION.tsv` มี `observed_frames=0`, `capture_file_count=0`, `status=NOT_OBSERVED` ทั้ง W/R ของสอง vital. ดังนั้น static รอบนี้ไม่ตั้งชื่อ nested `+0x10/+0x14/+0x18`, ไม่เรียกสอง string ว่า command/argument, ไม่เรียก result byte ว่า success/error, และไม่ตัดสินว่า live sender ใช้ค่าหรือ sub-path ใด. นี่คือ bounded semantic ceiling ไม่ใช่คำกล่าวว่า semantics ไม่มีอยู่.

## verifier / reproducibility

- สร้าง verifier เฉพาะใบ: `pf_bridge\staged\re088_gm_command_wire_static.py`
- SHA-256 `a441eb9f75f1ea8cc0da7e118f5ec7d2f190c3f46a8feb2b8de210d86b7a8f5b`
- รันอิสระ 2 ครั้งด้วย `py -3 -B ... GameClient.local.bin pf_bridge\external` ⇒ exit `0` ทั้งสองครั้ง; `checks_failed=0` ทั้งสองครั้ง.
- input pins: image `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`; protocol registry `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`; serializer fields `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`; validation `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`.
- SHA ก่อน/หลังตรงกัน: image และทุก source file ที่อ่าน; aggregate `external` tree `180424fe457e680e47b38b5b8e9a8094d2dc33c0c9c1f904b9f5a9a040dd11c5`; aggregate `gamedata` tree `6c7d05ca272d2fbb53098861606478af2c6ad41bdb637378c4554526357aee59`; queue SHA `28ca06c00103af6f915854bba3f3886ef0dc5e20d78f1a03ff1acbd828812426`.

## nonclaims

1. ใบนี้ไม่นิยามชุดคำสั่ง GM ของเซิร์ฟเวอร์เรา และไม่อ้างพฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ.
2. ไม่พิสูจน์ prefix/chat trigger หรือ live outbound sub-path — ส่งต่อให้ `RE-091` ตามคิว.
3. ไม่ตั้ง semantic จาก tag/width/offset และไม่ join scalar ใดกับตารางข้อมูลเกมเพราะเลขเท่ากัน.
4. `default handler` พิสูจน์เฉพาะไม่มี custom inbound handler ของ `0x51E9`; ไม่ได้พิสูจน์ว่า client ไม่มีโค้ด GM ส่วนอื่น.
5. ไม่มีหลักฐานชั้น client-observable ในใบ static นี้โดยเจตนา; ไม่มีเกม/server/`LOCK_GAME`/canonical DB ถูกแตะ.

BUILD_IMPACT: ทำให้เลนที่มีอยู่จริง `GM-002` เปลี่ยน raw capture เป็น schema-aware decode ได้ และให้ codec ที่ตรวจอิมเมจแล้วแก่ `GM-003`; แต่ยัง **ห้าม execute/ตั้งชื่อ command** จนกว่า semantic/live trigger จาก `RE-091` หรือ capture จริงจะปิด.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-088 PASS/DONE — STRUCTURAL-LAYOUT-PINNED · SEMANTICS-BOUNDED`.

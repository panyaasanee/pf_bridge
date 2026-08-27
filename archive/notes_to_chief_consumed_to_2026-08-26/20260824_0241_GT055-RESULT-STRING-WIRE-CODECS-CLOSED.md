[ถึง: chief cloud (cc) และ Panya · จาก: RE runner Codex LOCAL]

# GT-055 RESULT — STRING-CODEC-DECISION-001

**ผล: PASS/DONE** · รัน 2026-08-24 02:37–02:41 (+07:00) · งาน `STATIC-ON-BRIDGE` ล้วน ไม่บูต server/client ไม่จับ `LOCK_GAME` และไม่แตะ canonical DB

ค้นใน `pf_bridge\external\` แล้ว: **เจอ** `DeleteActorVital` และ `Channel_LocalTalkMessageVital` ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` พร้อม string-helper/call-site ที่ระบุชนิด `basic_string<char>` และ `basic_string<wchar_t>`

ค้น gamedata แล้ว: **ไม่เจอ** semantic match ของ `DeleteActorVital`, `Channel_LocalTalkMessageVital`, `UNTAGGED_STRING8_LEN32LE` หรือ `UNTAGGED_WSTRING16LE_LEN32LE` หลังค้น recursive ใน `pf_bridge\gamedata\`; ใบนี้เป็น wire codec ไม่ใช่ตารางข้อมูลเกม

## คำตัดสิน

| จุด | tag บน wire | ความกว้าง | len นับอะไร | หลักฐาน |
|---|---:|---:|---|---|
| `DeleteActorVital` `0x36DB`, string ท้าย record | `0x44` | 1 byte/char (`string8`) | `uint32le` นับ payload bytes | GT-018 raw capture บรรทัด 200–206; ยืนยันซ้ำด้วย GT-010/GT-011 |
| `Channel_LocalTalkMessageVital` `0xAC52`, string ทั้งสองช่อง | `0x48` | 2 byte/char (UTF-16LE) | `uint32le` นับ payload bytes | GT-019 raw capture บรรทัด 643–648 + event log seq 2 |

ดังนั้นรูปเต็มที่วัดได้คือ:

- `0x36DB`: **`44 | uint32le byte_len | N raw string8 bytes`**
- `0xAC52`: **`48 | uint32le byte_len | N raw UTF-16LE bytes`**

สมมติฐาน string ของ parser ปัจจุบันตามที่ใบระบุ (`0x36DB` เป็น UTF-16LE) จึงไม่ตรง wire จริง: ตัวอย่างนี้มี 32 ASCII bytes ต่อเนื่อง ไม่มี `00` สลับ เป็น `string8` ชัดเจน จัดเป็นบั๊กจริงตาม failure/result protocol ของใบ; รอบนี้ไม่แก้ source และให้ chief เป็นผู้เสนอ patch/PR

## จ็อบ 0 — ป้าย `UNTAGGED_*` หมายถึงอะไร

คำตอบ: **เป็นมุมมอง/ขอบเขตหลักฐานของ string helper ใน serializer body ไม่ใช่คำอ้างว่ารูปเต็มบน wire ไม่มี field tag**

หลักฐานที่ re-derive ได้:

- `PF_SERIALIZER_FIELDS.md:8` บอกว่าแถว tag ตัวเลขมาจากคนละ primitive คือ `WRITE 0x0089A600` / `READ 0x0089A640` และ pattern `len, pointer, tag`
- `PF_SERIALIZER_FIELDS.md:9` จำกัด string helper ไว้สี่ target; พิสูจน์ `basic_string<char/wchar_t>` และเฉพาะ `uint32le` length ที่นับ payload bytes ตามด้วย raw N bytes
- `pf_extract_protocol.py:80-113` hard-code ชื่อ `UNTAGGED_STRING8_LEN32LE`/`UNTAGGED_WSTRING16LE_LEN32LE` ให้ helper targets `0x0089A6D0`, `0x0089A740`, `0x0089A810`, `0x0089A880`
- `pf_extract_protocol.py:2466-2471` สร้าง evidence ของ helper เป็น `length_prefix=uint32le payload=N_bytes`; `:7109-7111` บันทึก call-site เป็น `string_wire_call ... target=... stream_formal=...` โดยไม่มี field-tag model ใน record นี้
- `PF_SERIALIZER_FIELDS.tsv:462/466` ผูก `DeleteActorVital` กับ char helpers; `:2421-2424` ผูก chat กับ wchar helpers

ดังนั้นคำว่า `UNTAGGED` อ่านได้เพียงว่า **helper primitive ที่ extractor พิสูจน์เริ่มจาก length+payload และไม่มี tag อยู่ใน model ของ helper นั้น**; ห้ามยกเป็น negative claim ว่าไม่มี tag ก่อน helper บน full wire. Capture ด้านล่างยืนยันว่ามี `0x44`/`0x48` จริง

## จ็อบ 1(ก) — `0x36DB` non-empty string

ไฟล์หลัก: `GameClient\capture_gt018_20260819_024213\capture_v141\GAME_20260819_024807_710330_60904.txt`, SHA256 `22af6ab1a99f0c6c23761cd8285bd5e340c419564766e17d7ebfb84f361906dd`, บรรทัด 200–206

```text
DECOMPRESSED 66
00000000  12 3A 45 14 00 00 00 00 08 00 0B 02 12 01 00 12
00000010  DB 36 0B 01 08 01 08 00 14 00 00 00 00 44 20 00
00000020  00 00 37 44 30 31 34 45 35 34 31 41 46 41 41 34
00000030  33 32 36 37 43 41 38 30 42 43 43 42 43 33 46 44
00000040  36 42
```

Parse nested record จาก offset `0x0F` ทีละ field:

```text
12 DB 36          id = 0x36DB
0B 01             version = 1
08 01             u8 field = 1
08 00             u8 field = 0
14 00 00 00 00    u32 field = 0
44                string tag
20 00 00 00       uint32le length = 32 bytes
37 ... 36 42      ASCII "7D014E541AFAA43267CA80BCCBC3FD6B" = 32 bytes
```

Parse แบบไม่มี tag จะอ่าน `44 20 00 00` เป็น length `0x2044 = 8260` ซึ่งเกิน bytes ที่เหลือ จึงตัดทิ้งได้ ไม่ใช่คำตอบสองทาง. Payload ไม่มี `00` สลับและมี 32 ไบต์พอดี จึงเป็น 1 byte/char

corroboration อิสระที่ให้ raw bytes ชุดเดียวกัน:

- GT-010 `...\capture_gt010_20260818_015927\capture_v141\GAME_20260818_020106_955833_62358.txt` บรรทัด 255–260, SHA256 `22afd705194e15b97dc1ed3605487e667f268d5ba8671bb01a99c9a05dd5e3bf`
- GT-011 `...\capture_gt011_20260818_170121\capture_v141\GAME_20260818_170347_645157_52155.txt` บรรทัด 189–194, SHA256 `b79b22f9c69519a7baf560470af2e2248985ed648c8d3a2c7c1bf81053d53ee3`

## จ็อบ 1(ข) — `0xAC52` wstring

พิกัด `capture_gt006_boot_20260817_132858` ที่มีอยู่บนดิสก์มีเพียงไฟล์ LOGIN และค้นไม่พบ `0xAC52`; จึงไม่เดาหรืออ้างไฟล์ที่ไม่มี และใช้ raw capture GT-019 ที่มี record จริงแทน

ไฟล์หลัก: `GameClient\capture_gt019_20260819_033154\capture_v141\GAME_20260819_033539_316079_63959.txt`, SHA256 `e0ee747f91e002fb6cdd28c268d848e01e3b55f486bf84fc7b109904e4b82044`, บรรทัด 643–648

```text
DECOMPRESSED 54
00000000  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12
00000010  52 AC 0B 00 48 00 00 00 00 48 18 00 00 00 50 00
00000020  46 00 43 00 48 00 41 00 54 00 50 00 52 00 4F 00
00000030  42 00 45 00 31 00
```

Parse nested record จาก offset `0x0F`:

```text
12 52 AC          id = 0xAC52
0B 00             version = 0
48                string #1 tag
00 00 00 00       uint32le length = 0 bytes
48                string #2 tag
18 00 00 00       uint32le length = 24 bytes
50 00 ... 31 00   UTF-16LE "PFCHATPROBE1" = 12 chars = 24 bytes
```

ไฟล์ `GAME_EVENTS_LIVE.txt` ในโฟลเดอร์เดียวกัน SHA256 `5cca2333464f75c4d441f65536a3f11cc0ab6e02b9b0a38e6e426d6d21a3bde7` corroborate event seq 2 ด้วย payload 34 bytes:

```text
48000000004818000000500046004300480041005400500052004F00420045003100
```

ค่า `0x18 = 24` เท่ากับจำนวน payload bytes ไม่ใช่จำนวนตัวอักษร 12. การอ่านแบบไม่มี tag จะได้ length แรก `0x48 = 72` ทั้งที่ payload ทั้ง record มีเพียง 34 bytes จึงตัดทิ้งได้

## จ็อบ 2 และสถานะงาน

ไม่รัน fallback image call-site comparison เพราะเงื่อนไข fallback ไม่เกิด: corpus มี `0x36DB` non-empty string และตัดสินรูปเต็มได้จาก capture โดยตรง. จ็อบ 0, 1 และ 3 ปิดครบ; จ็อบ 2 = N/A ตามเงื่อนไขใบ

## SHA256 ก่อน–หลัง

ทุกไฟล์ด้านล่างเปิดอ่านอย่างเดียวและ SHA ก่อน/หลังตรงกัน:

| ไฟล์ | SHA256 ก่อน = หลัง |
|---|---|
| `GameClient\GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external\00_SEARCH_HERE_FIRST.md` | `6f6c092c0af1363afa4fd03bf21c053991b5f985ec17587a8e1d2d96edb1a459` |
| `external\PF_PROTOCOL_REGISTRY.tsv` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |
| `external\PF_SERIALIZER_FIELDS.tsv` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |
| `external\PF_SERIALIZER_FIELDS.md` | `1d069b20871b3081f013e88e128f78d790c1133838a565f6f11dab078859139a` |
| `external\pf_extract_protocol.py` | `0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e` |
| `gamedata\00_SEARCH_HERE_FIRST.md` | `f19db140593f1a73d2abb0b3b9c141b2082bea499e6b092f671c45f810ea2153` |
| GT-018 raw capture | `22af6ab1a99f0c6c23761cd8285bd5e340c419564766e17d7ebfb84f361906dd` |
| GT-010 raw capture | `22afd705194e15b97dc1ed3605487e667f268d5ba8671bb01a99c9a05dd5e3bf` |
| GT-011 raw capture | `b79b22f9c69519a7baf560470af2e2248985ed648c8d3a2c7c1bf81053d53ee3` |
| GT-019 raw capture | `e0ee747f91e002fb6cdd28c268d848e01e3b55f486bf84fc7b109904e4b82044` |
| GT-019 `GAME_EVENTS_LIVE.txt` | `5cca2333464f75c4d441f65536a3f11cc0ab6e02b9b0a38e6e426d6d21a3bde7` |

## nonclaims

- ใบนี้ตัดสินเฉพาะรูป string สองจุดนี้และความหมายเชิงขอบเขตของป้าย `UNTAGGED_*`; ไม่ตัดสินความหมายของฟิลด์ และไม่ generalize ผลไปทุกแถวของตารางเป็นรายแถว
- `UNTAGGED_*` ยังเป็นคำอธิบายที่ถูกต้องของ helper body ที่พิสูจน์ว่าเป็น length+payload; ผลนี้เพียงห้ามใช้ป้ายนั้นเป็น full-wire absence claim
- capture ยืนยัน bytes ของ record ที่สังเกตได้ ไม่ได้พิสูจน์ว่า client ส่งทุก W row ในทุก runtime path
- ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล
- ไม่มีหลักฐานชั้น client-observable ในใบ static นี้ และไม่มีการเปิดเกม


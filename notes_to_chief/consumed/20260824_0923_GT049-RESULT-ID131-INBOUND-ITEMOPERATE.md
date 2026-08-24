ถึง chief

# GT-049 RESULT — ID 131 ยิงจาก inbound `ItemOperateVitalRes` (จ็อบ 2–4 ปิด)

เวลา: 2026-08-24T09:23+07:00  
สถานะเสนอ: **PASS/DONE — jobs 2–4/4**

## คำตอบ objective ประโยคเดียว

template `ได้รับ [ $V1 ] * $V2` คือ MESSAGE id **131 (`0x83`)**; exact string bytes ไม่ได้ resident ใน PE/asset packed จึงไม่มี static string VA (`N/A`) แต่จุดยิง chat ที่ใช้ id นี้อยู่ที่ **`0x005CC309` ภายใน `0x005CC2B0`** และย้อนถึง receive callback **`ItemOperateVitalRes` vtable `0x00F30668` slot `+0x1C = 0x005EF5E0`** ผ่าน chain `0x005EF5FB → 0x005A8A00 → {0x005A5790,0x005A5DB0} → 0x005CC2B0 → 0x005CA2F0`; serializer เดียวกันมีขา READ `0x0089A640` 5 จุด จึงเป็น **เลน inbound แยกจาก `PickupTerrainThing` failure-response handler** ไม่ใช่เส้น `0x1F/0x03/0x22` ของ GT-046.

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: เจอ `PF_PROTOCOL_REGISTRY.tsv` ผูก `ItemOperateVitalRes` กับ vtable `0x00F30668`, serializer `0x005EDA20`, handler `0x005EF5E0`; `PF_SERIALIZER_FIELDS.tsv` มี W/R ใน span เดียวกันและขา R เรียก READ `0x0089A640` ที่ `0x005EDB33/48/A2/BD/CD`; `PF_FIELD_VALIDATION.tsv` มี capture R = 5/5, W = 0/0. เจอ `PickupTerrainThing` แยกเป็น vtable `0x00F3005C`, serializer `0x005E5E30`, handler `0x005EF640`.
- ค้น gamedata แล้ว: เจอ `gamedata\tables\TEXTDATA_TH__MESSAGE.tsv` แถว `131\t1\t0\tได้รับ [ $V1 ] * $V2` (907 data rowsตาม scope-cut; ไฟล์ 97,865 bytes). ค้น exact template ทั้ง UTF-8/UTF-16LE/cp874 ใน PE และ `GameClient\Data\B_TEXTDATA_TH.pc_` แล้วได้ 0 ทุก encoding — ตาราง packed ไม่ให้ VA ของสตริงแบบ static; ใช้ id immediate เป็น anchor แทน.

## หลักฐานจ็อบ 2 — census id 131

สวีป raw bytes ครบ executable sections `.text` + `.code` พบ `push imm32 0x83` **2 จุดพอดี**:

1. `0x00578E00` file off `0x00178200` ภายใน `[0x00578C60,0x00578E88)`; ตามด้วย `0x00578E05 → 0x005AB5F0`. เส้นนี้สร้าง/ผูก local UI object และไม่ใช่ global chat object `+0x728`.
2. `0x005CC309` file off `0x001CB709` ภายใน `[0x005CC2B0,0x005CC33A)`; ตามด้วย `0x005CC310 → 0x005CA2F0`. จุดนี้ส่ง args ชื่อ/จำนวน, color `0x10000`, id `0x83` เข้า chat formatter — เป็นตัวยิงบรรทัดเขียวที่ใบต้องการ.

raw dword census ของค่า `0x83` พบ 215 จุดทั่ว sections (รวม data/non-instruction จึงไม่เอามาตีความเป็น code xref); direct `E8/E9` byte census และ recursive CFG ใช้ยืนยัน chain บวกด้านล่าง. ไม่มีการใช้ linear disassembler เป็นหลักฐานผลลบ.

## หลักฐานจ็อบ 3–4 — xref chain และทิศทาง

- `ItemOperateVitalRes` vtable words: `+0x10 getter 0x005EBF70`, `+0x18 serializer 0x005EDA20`, **`+0x1C receive handler 0x005EF5E0`**, `+0x20 0x00710440`.
- handler `[0x005EF5E0,0x005EF61A)` อ่าน record fields `+0x14`, `+0x18`, `+0x30`; call `0x005EF5FB → 0x005A8A00`.
- `0x005A8A00` มี direct calls `0x005A9102 → 0x005A5790` และ `0x005A9113 → 0x005A5DB0`.
- สอง extractor มี direct calls เดียวไป emitter: `0x005A5C48 → 0x005CC2B0` และ `0x005A61BD → 0x005CC2B0`.
- emitter push `0x83` ที่ `0x005CC309`, แล้ว `0x005CC310 → 0x005CA2F0`.
- serializer `[0x005EDA20,0x005EDC31)` มี exact direct READ calls 5 จุด (`0x005EDB33/48/A2/BD/CD → 0x0089A640`) และ WRITE calls 5 จุดในอีก branch; external capture validation สังเกตขา R 5 fields และไม่สังเกต W. เมื่อประกอบกับ callback slot `+0x1C` เส้นยิง chat นี้เป็น receive/inbound path.
- เทียบ GT-046: `PickupTerrainThing` handler narrow span `[0x005EF640,0x005EF66F)` map status `FC/FD/FE → 1F/03/22` และยิง `0x005CBC00`; ไม่มี edge ไป `0x005CC2B0`. จึงเป็นคนละ handler และคนละ message lane.

### Span pins (VA `[start,end)` · file offset · len · sha256)

| ชื่อ | span / off / len | sha256 |
|---|---|---|
| local id-131 UI consumer | `[0x00578C60,0x00578E88)` · `0x00178060` · 552 | `89abe72cfcb86f7fcb536a5f28a86d872ab01520bc2bcf126baaeaa421e68cb9` |
| message object builder | `[0x005AB5F0,0x005AB82A)` · `0x001AA9F0` · 570 | `d9b5f8db6aaf6664af772a23e0201ee2eb179de8427621bcf03b94380e879e8f` |
| inventory extract A | `[0x005A5790,0x005A5DA3)` · `0x001A4B90` · 1555 | `de4fca4b5d02b6527e3d731b991f28af9f10dc4554c551d93e7a1f617b61ba2e` |
| inventory extract B | `[0x005A5DB0,0x005A63F3)` · `0x001A51B0` · 1603 | `f4f73926b82987df30c39bb6d9c7054e9917b9b35a789ce3b382132d779cba8f` |
| inventory dispatch | `[0x005A8A00,0x005A9CB2)` · `0x001A7E00` · 4786 | `d2319cefe83f4665fa6f8745cd4b865d16f1cb837c2f8b5bee7fdd6138d5437c` |
| chat formatter | `[0x005CA2F0,0x005CA44D)` · `0x001C96F0` · 349 | `a62ad3fc10b9af80e132cc1000873965be91ea2245d47c3afda003e231842ad8` |
| green chat emitter | `[0x005CC2B0,0x005CC33A)` · `0x001CB6B0` · 138 | `c4285ee81f7e5f463956984e6142194726cc834c5cddbe0fe01b1ea23f057781` |
| ItemOperate serializer | `[0x005EDA20,0x005EDC31)` · `0x001ECE20` · 529 | `b5f6a1586a810c0a98ceb7c925a0d4afa10cff41db661eb0947b8918f3a11d54` |
| ItemOperate handler | `[0x005EF5E0,0x005EF61A)` · `0x001EE9E0` · 58 | `436b856fc41eb2d1f90b103bddaba29b621e21df99633c0f181a609224a9ff1d` |
| Pickup handler (GT-046 narrow pin) | `[0x005EF640,0x005EF66F)` · `0x001EEA40` · 47 | `5d17fc4fdeeafde0a4a34e900e76d0336e404f8d2f058ba085044ae8d88d602e` |
| stream READ | `[0x0089A640,0x0089A6C6)` · `0x00499A40` · 134 | `4b58ff55a1e7fdd1640f7be47db6a44a41d1e83093bd8dd271c5c0d1dab3ca51` |

recursive CFG ของ 11 heuristic spans ข้างต้น: decode errors รวม **0**. Bytewise direct-call census ทั้ง image: `0x005CC2B0` มี 2 callers, `0x005A5790` 1, `0x005A5DB0` 1, `0x005A8A00` 1; handler/serializer เข้าผ่าน vtable/data refsตาม registry. Stream primitive global counts W=1350, R=1350 (ไม่เอาจำนวน global นี้มา join เอง).

## SHA ก่อน/หลัง (ตรงกัน)

- `GameClient.local.bin` 14,759,424 bytes: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `GameClient\Data\B_TEXTDATA_TH.pc_` 336,985 bytes: `56b4826ed437c3f30bd1937c580ca612c22655600b5fbeb781b64c767e74c467`
- `TEXTDATA_TH__MESSAGE.tsv` 97,865 bytes: `002f3145cc6f53c70fd2d3fda81d492d0db1574bf0fc07285606497632d08609`
- `PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_FIELD_VALIDATION.tsv`: `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`

เครื่องมือ read-only: `logs\gt049_20260824\gt049_probe.py` sha `217c379e3ee81e23a41cc35154b7e11c1e3f80855c75b0c378977e000bb633c3`; output `gt049_probe.json` sha `ba98cba7a0c03e3836014c04a7666d8831a9258b3e2911d295930821b0d31873`; guards 12 spans, 2 executable sections, recursive errors 0, exit 0.

## Nonclaims

- static ไม่พิสูจน์ว่าเลนนี้รันจริงในเฟรมคลิป `~163 s`; พิสูจน์เพียงว่า client มี inbound path ที่ยิง template นี้.
- การเจอ template/id ไม่พิสูจน์ runtime occurrence ของเฟรมที่วัด และไม่ใช่หลักฐาน client-observable.
- ไม่ claim เรื่อง pet หรือโหมด pet ในคลิป.
- ไม่ claim กฎ/พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับซึ่งปิดไปแล้ว; ข้อนี้ใช้กำหนดงานออกแบบ server ของเราเท่านั้น.
- ไม่ตั้งชื่อ wire fields/record เพิ่มจากหลักฐาน; `PF_RUNTIME_CLASSMAP.tsv` UNKNOWN 100% ไม่ถูกใช้เป็นชื่อคลาส.
- ขา local UI ที่ `0x00578C60` ใช้ id เดียวกันจริง แต่หลักฐานนี้ไม่พิสูจน์ว่ามันสร้าง chat line เดียวกัน; คำตัดสิน chat direction พึ่งเส้น global chat emitter จาก receive handler.
- ไม่แก้ `GAME_TEST_QUEUE.md`, source, image, asset หรือ TSV ใด ๆ.

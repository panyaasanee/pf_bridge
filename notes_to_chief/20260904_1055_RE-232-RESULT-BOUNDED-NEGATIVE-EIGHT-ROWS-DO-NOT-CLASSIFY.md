[ถึง: LANE-CS | cc: chief cloud | จาก: RE runner local · 2026-09-04T10:55:00+07:00]

# RE-232 RESULT — DSL แยก attack/AOE/self-buff/heal ไม่ได้จาก 8 แถวปัจจุบัน

## สถานะ

**DONE / BOUNDED-NEGATIVE (static-only)** — ถอดเฉพาะ 8 skill IDs ที่ `skill_catalog.py` มีอยู่ตามขอบเขตใบ ไม่ขยายไป 2,165 แถว ผลคือ grammar มีโครงสร้าง condition-line → behavior-line จริง แต่ sample นี้ไม่มีตัวแทนที่พิสูจน์แล้วของ AOE, self-buff หรือ heal และ token ที่เห็นไม่เป็น type tag จึงสร้างตัวจำแนกสี่ประเภทไม่ได้

- ticket START: `2026-09-04T10:50:03+07:00`
- ticket block SHA-256: `5C9067E16F34811E77C1B8A2EC8946214232D7D0658C831E06BB19D9E196D5B2`
- client: `GameClient.local.bin` SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- `skill_catalog.py` SHA-256 `ACD5BFA7544790E0E68CECD63516F2C4A4342204CFD21BCB9722246541CF76C8`
- pinned 8-row slice SHA-256 `1B6F95A3F4ADC465319C5C5E6F56B212A58FF92CB512906BBFAFCA926A18D458`
- full `SKILL_CONTEXT.tsv` SHA-256 `41D642C535BFEFD9A560CB8FC92A530A51BD3CA55168EDDAE93CFD64DCA7C4F4`
- verifier `staged/re232_static_verify.py` SHA-256 `E4E0593EAF6B88F71AD8B9858DCD78FE5D8662A7C38B2518D9EB175BC9E72912`; result `PASS 42/42`

## Mandatory searches

ใช้ shared manifest ที่ทำครั้งเดียวก่อนเริ่ม batch:

- `pf_bridge/external/`: 2,683 files / 930,201,065 bytes, fingerprint SHA-256 `9AFA09D3832F9A427C2E818C3ADBC6B3734C8479DA194101868CB5CD579F9C6A`; ค้น `s_CAST_CONDITION`, `s_CAST_BEHAVIOR`, `GO`, `CHASE`, `SKIP`, `ISVIP_I` และ terms ของ RE-229 แล้ว พบ schema/report/binding เดิม แต่ไม่พบ token legend หรือ type crosswalk
- `pf_bridge/gamedata/`: 1,109 files / 15,319,585 bytes, fingerprint SHA-256 `E3ECBFC23FF7EC8D7490BBD9343ED1F0528C5333328942AC2C988EBEC39196F9`; พบ two columns ใน `SKILL_CONTEXT`, offsets `+72/+76`, และ 8 rows ด้านล่าง แต่ไม่พบ field ที่ผูก token กับ taxonomy สี่ประเภท

ไม่ได้ census/derive ตารางเต็ม 2,165 แถวใหม่; ใช้เพียง 8-row committed slice และ GT-052 เดิมเพื่อรู้ขอบเขตตารางเท่านั้น

## แถวที่ตรวจครบทั้ง 8

| id / title | `s_CAST_CONDITION` | `s_CAST_BEHAVIOR` | ข้อสรุปที่อนุญาต |
|---|---|---|---|
| 99 Normal Attack | `GO(0)` | blank | `GO` ไม่ใช่ attack tag เพราะพบใน movement ด้วย |
| 110 Strive Jump | `GO(0)` | `CHASE(110)` | movement row; `CHASE` self-references skill id |
| 111 VIP Strive Jump | `ISVIP_I(1)\nGO(0)` | `CHASE(111)\nSKIP(782)` | movement/VIP row; `ISVIP_I` และ `SKIP` มีตัวอย่างเดียว |
| 40000 Gladiator Basic Training | blank | blank | blank/blank |
| 41000 Sharpshooter Basic Training | blank | blank | blank/blank |
| 42000 Stormherald Basic Training | blank | blank | blank/blank |
| 43000 Imperial Knights Basic Training | blank | blank | blank/blank |
| 44000 Light Priest Basic Training | blank | blank | blank/blank |

## Parser และ token semantics ที่พิสูจน์ได้

### Loader span

`[0x00754450,0x007549A6)` — 1,366 bytes, `span_sha256=A4F10F9AC07B1DDE442D1CD984A6E00785DD8909A6F55CE8181F4F17C3B3FAFE`

- อ่าน `s_CAST_CONDITION` literal VA `0x00F48C94` และ `s_CAST_BEHAVIOR` literal VA `0x00F48C74`
- เมื่อทั้งคู่ nonblank จึงส่งคู่ string ไป parser `0x007534F0`
- ด้วยเหตุนี้ใน sample ปัจจุบันคู่ที่เข้าสู่ parser มีเพียง 110/111; row 99 มี behavior blank และ Basic Training ทั้งห้ามีสอง field blank

### Pairing/parser span

`[0x007534F0,0x007537D4)` — 740 bytes, `span_sha256=163FAD0544C1806D5FD2173E7DCB7B303121E98D67B81F76B2EE80444BCA1187`

- แยก condition/behavior เป็นบรรทัดด้วย literal newline VA `0x00F13F4C`
- tokenize behavior ด้วย delimiters `();\t ` ที่ VA `0x00F48BEC`
- เปรียบเทียบ token name กับ `SKIP` VA `0x00F48BE0` และ `CHASE` VA `0x00F48BD4`
- `SKIP(n)` เก็บ numeric argument ลง parsed node `+0x0C`; `CHASE(n)` เก็บลง `+0x08`; จากนั้น condition tokens ของบรรทัด index เดียวกันถูก parse/แนบกับ behavior node

ความหมายที่ claim ได้โดยผ่านกฎ ≥2 skills มีเพียง:

- `CHASE(n)` เป็น **structural behavior edge/value**, ไม่ใช่ gameplay type: ใน skill 110 และ 111 parser เก็บ argument และทั้งสองแถว self-reference `110`/`111`; สองแถวนี้เป็น movement ทั้งคู่ จึงไม่แยก single-target/AOE/buff/heal
- `GO(0)` พบใน 99, 110, 111 แต่ basic attack และ movement แชร์ token เดียวกัน จึงใช้เป็น attack/type discriminator ไม่ได้; runtime predicate semantics ละเอียดประกาศ `opaque`
- `SKIP(782)` และ `ISVIP_I(1)` มีอย่างละหนึ่ง skill (111) ใน sample จึงประกาศ `opaque` ตาม G6 ไม่ตั้งความหมายจากชื่อ
- blank/blank พบห้า Basic Training rows แต่ความว่างไม่พิสูจน์ self-buff, passive หรือ type ใด

## คำตอบตรงใบ

**ไม่ได้จากกลุ่มตัวอย่างนี้**:

- single-target vs AOE: ไม่มี AOE ที่ independently labeled สองแถว และ `GO` ถูกแชร์ระหว่าง Normal Attack กับ movement
- self-buff vs heal: ไม่มีตัวแทนที่ independently labeled ของสองประเภทนี้เลย
- four-way classifier: ไม่มี token/pattern ที่ครอบคลุมสี่กลุ่ม; DSL ที่เห็นเป็น condition/action control-flow/edge data ไม่ใช่ enum ชนิดสกิล

หาก chief ต้องการเดินต่อ ให้เปิดใบใหม่ที่เพิ่ม **อย่างน้อย 8 แถวที่ label ได้จากหลักฐานอิสระ: 2 single-target + 2 AOE + 2 self-buff + 2 heal** และเก็บ 8 แถวเดิมเป็น controls รวมขอบเขต 16 rows. จำนวนนี้เป็นขั้นต่ำเพื่อให้ทุก semantic token claim มี ≥2 skills ตาม G6; ถ้าทั้งแปดยังไม่มี token ที่แยกคู่ จึงค่อยพิจารณา census กว้างขึ้นในใบแยก ไม่ให้ RE-232 ไหลเป็น 2,165-row scan

## Nonclaims

- ไม่กล่าวว่า grammar ทั้งตารางจำแนก type ไม่ได้; กล่าวเฉพาะว่า 8-row sample ปัจจุบันไม่พอ
- ไม่แปล `GO`, `SKIP`, `ISVIP_I` จากชื่อ token อย่างเดียว
- ไม่กล่าวว่า `CHASE` คือโจมตีหรือการเลือกเป้าหมาย; พิสูจน์เพียงรูป parser/argument edge และ self-reference สอง movement rows
- ไม่ใช้ `n_PASSIVE` หรือ `n_TARGET` เป็น type label; crosswalk ของสอง field นั้นยังไม่มี
- ไม่ใช้ผล static เป็น client-observable/wire/DB evidence; ไม่มี game/server boot และไม่แตะ canonical DB

## BUILD_IMPACT

`BUILD_IMPACT: no classifier change` — LANE-CS ให้เก็บ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` เป็น raw fields ต่อไป ห้ามเพิ่ม `skill_type()` จาก `GO/CHASE/SKIP/ISVIP_I`, blank fields, `n_PASSIVE` หรือ `n_TARGET`. ผลนี้ไม่บล็อก M1–M5; งาน taxonomy ใหม่ต้องรอใบ 16-row targeted follow-up ที่ chief เปิดอย่างชัดเจน

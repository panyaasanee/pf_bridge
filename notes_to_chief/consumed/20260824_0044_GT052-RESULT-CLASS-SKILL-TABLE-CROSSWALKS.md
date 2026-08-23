[ถึง: chief cloud (cc) และ Panya · จาก: ผู้เทส LOCAL / คนหน้าเครื่องสะพาน]

# GT-052 CLASS-SKILL-TABLE-001 — RESULT

- เวลา: 2026-08-24 00:44:28 +07:00
- สถานะที่เสนอ: `[PASS]` / `[DONE]` โดยมีผลลบสำคัญว่า label ของ `n_TARGET` ยังพิสูจน์ไม่ได้
- ลักษณะงาน: static read-only เท่านั้น; ไม่เปิดเกม, ไม่บูต server/client, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB
- ใช้ TSV ที่ `gamedata\tables\` ตรง ๆ; ไม่เปิด `.dec` และไม่เขียน parser/script ใหม่

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: **เจอ** skill-related protocol/serializer 10 ชื่อ, 88 field rows (`TriggerCastSkillVital`, `CSkillModule`, `CSkillAttr`, `CLearnSkillVital` ฯลฯ); `CSkillModule`/`CSkillAttr` เป็น `EMPTY` W/R spans และ `PF_RUNTIME_CLASSMAP.tsv` ค้นคำว่า Skill ได้ 0 แถว จึงตอบ wire/class-image ได้บางส่วนแต่ **ไม่ใช่ตารางค่าตัวเลข/ชื่อสกิล**
- ค้น gamedata แล้ว: **เจอ** `CHARCREATE_CLASS` 5x38, `SKILL_CONTEXT` 2165x20, `CURRICULUM` 137x7, `SKILL_TEXT` 940x6, `CONTENT_CLASS` 6x3; ดัชนีครบ 188 ตาราง / 2,365 คอลัมน์
- span ของ external ที่อ้างผ่าน GT-054 แล้ว (`392/392`, mismatch/unreadable 0); ใบนี้ไม่ได้ใช้ external เป็นตัวแทน gamedata

## คำตอบ objective

1. ตารางสร้างอาชีพมี **5 แถว**: `n_ID = 1,2,4,16,32` และ `s_ICON` ผูกตรงกับ Gladiator/Paladin/Sniper/Necromancer/Sorcerer
2. ตารางสกิลมี **2,165 แถว / 20 คอลัมน์**; มี level, SP fields, CD field, target code, stamina, equip masks, cast-condition/behavior DSL และ `n_ISCLASS` bitmask
3. `n_ISCLASS` มี bit `8` จริง 35 แถว; row `45000` ให้ `s_ICON=ICON_Class_Voodooist_s` โดยตรง ขณะที่ `CHARCREATE_CLASS` ไม่มี row 8
4. `TEXTDATA_TH__CONTENT_CLASS` มี row `n_ID=8, s_CLASSNAME=Voodoo`; รวมกับ icon field ของ row 45000 เป็นหลักฐานว่าข้อมูลสกิล/ข้อความมี class bit 8 ที่สัมพันธ์กับ Voodoo/Voodooist แต่ **ไม่พิสูจน์เหตุผลว่าทำไม class นี้ไม่อยู่ในหน้าสร้างตัวละคร**
5. ชื่อสกิลผูกด้วย field-level crosswalk `SKILL_CONTEXT.n_ID = SKILL_TEXT.n_ID`: ทั้งสองข้าง unique 100%; intersect 898 IDs, text-only 42, context-only 1,267 — จึงแนบชื่อเฉพาะ 898 จุดตัดและไม่เดาชื่อส่วนที่ขาด

## Census และ crosswalk ที่ไม่ใช่ numeric coincidence ลอย ๆ

### อาชีพ / ไอคอน

`CHARCREATE_CLASS.s_ICON` เป็น crosswalk literal ไปชื่อไฟล์ไอคอน ไม่ได้จับจากเลข:

| `n_ID` | `s_ICON` | ไฟล์ที่มีจริง |
|---:|---|---|
| 1 | `Icon_Class_Gladiator` | `icon_class_gladiator.tg_` + `_s` variant |
| 2 | `Icon_Class_Paladin` | `icon_class_paladin.tg_` + `_s` variant |
| 4 | `Icon_Class_Sniper` | `icon_class_sniper.tg_` + `_s` variant |
| 16 | `Icon_Class_Necromancer` | `icon_class_necromancer.tg_` + `_s` variant |
| 32 | `Icon_Class_Sorcerer` | `icon_class_sorcerer.tg_` + `_s` variant |

มี 6 distinct icon stems / 12 ไฟล์เมื่อรวม `_s`; stem ที่หกคือ `voodooist` แต่ไม่มี row ใน `CHARCREATE_CLASS`.

หลักฐาน bit 8 สามชั้นที่ผูกด้วย field จริง:

- `CONTENT_CLASS`: `n_ID=8`, `s_CLASSNAME=Voodoo`
- `SKILL_CONTEXT`: 35 rows ที่ `n_ISCLASS=8`
- `SKILL_CONTEXT` row 45000: `n_ISCLASS=8`, `s_ICON=ICON_Class_Voodooist_s`; literal นี้ match ไฟล์ `icon_class_voodooist_s.tg_`

`n_ISCLASS` distribution: `0:1952`, `1:36`, `2:35`, `4:35`, `8:35`, `16:36`, `32:35`, `63:1`; row 99 (`Normal Attack`) ใช้ 63 = `1|2|4|8|16|32`, สนับสนุนการอ่านเป็น bitmask ไม่ใช่ ordinal.

### Skill IDs / text names

crosswalk หลักคือ field ชื่อเดียวกันในตารางที่มี semantic เฉพาะ: `SKILL_CONTEXT.n_ID` -> `SKILL_TEXT.n_ID` -> `s_SKILL_TITLE`.

- `SKILL_CONTEXT.n_ID`: unique 2,165/2,165
- `SKILL_TEXT.n_ID`: unique 940/940
- intersect: 898
- `SKILL_TEXT` ที่ไม่มี context: 42 (ตัวอย่าง `89 Wound Healing`, `279 Martial Attack`, `3820 Strile`)
- context ที่ไม่มี `SKILL_TEXT`: 1,267 (ตัวอย่าง IDs `1,2,3`; จึงไม่เติมชื่อให้)

cross-check ด้วย foreign-key-shaped fields ที่ระบุคำว่า skill จริง:

- `CURRICULUM.n_SKILL` 137/137 rows resolve ไป `SKILL_CONTEXT.n_ID`
- `CHARCREATE_CLASS.s_SKILL_1..4` เก็บรูป `<skill-id>;<level>`; ทั้ง 20/20 refs resolve ไป `SKILL_CONTEXT.n_ID`
- ตัวอย่าง class 1: `111;1 -> VIP Strive Jump`, `40000;1 -> Gladiator Basic Training`, `99;1 -> Normal Attack`, `110;1 -> Strive Jump`

ดังนั้นไม่ได้ join ตารางสุ่มเพราะเลขตรงกัน; ใช้ fields ที่ตั้งชื่อเป็น skill reference + uniqueness/coverage guards. แต่ไม่มี linked-tip declaration ใน index ของ `SKILL_CONTEXT` (`flags` raw = `699`) จึงไม่ claim ว่าทุก context row ต้องมี text row.

## ตัวอย่าง class/basic skill จริงทั้งหก bit

| bit | skill id | `s_ICON` | title จาก `SKILL_TEXT` | passive code | target code |
|---:|---:|---|---|---:|---:|
| 1 | 40000 | `ICON_Class_Gladiator_s` | `Gladiator Basic Training` | 1 | 0 |
| 2 | 43000 | `ICON_Class_Paladin_s` | `Imperial Knights Basic Training` | 1 | 0 |
| 4 | 41000 | `ICON_Class_Sniper_s` | `Sharpshooter Basic Training` | 1 | 0 |
| 8 | 45000 | `ICON_Class_Voodooist_s` | `巫毒使基礎修煉` | 2 | 1 |
| 16 | 42000 | `ICON_Class_Necromancer_s` | `Stormherald Basic Training` | 1 | 0 |
| 32 | 44000 | `ICON_Class_Sorcerer_s` | `Light Priest Basic Training` | 1 | 0 |

ชื่อใน TEXTDATA กับชื่อไฟล์ไอคอนเป็นคนละ namespace บางแถว (เช่น Necromancer icon vs Stormherald title); รายงาน raw ทั้งคู่ ไม่บังคับให้ชื่อเหมือนกัน.

## ตีความคอลัมน์จากค่าจริง

### สิ่งที่พิสูจน์ได้

- `n_LEVEL_LEARN`: raw learn-level field; ตัวอย่าง 280=`1`, 8250=`5`, 8252=`25`
- `n_LEVELS`: มีเพียง `1` (1,982 rows), `120` (14), `4294967295` (169); ค่าสุดท้ายคือ u32 all-ones แต่ความหมาย sentinel ไม่ตั้งชื่อเพิ่ม
- `f_SP_LEVE1`: values `{0, 0.2, 0.4, 1, 4, 8}`; `f_SP_LEVEL2PLUS`: `{0,1}` — เป็น raw SP fields ตาม schema แต่ไม่ claim หน่วย/สูตร
- `n_CD`: 297 distinct values; zero 1,442 rows, nonzero 723, เท่ากับ own `n_ID` 125 rows; รูปนี้ไม่รองรับการเรียกทุกค่าเป็น “เวลา milliseconds” จึงบันทึกเป็น raw cooldown/group field โดยไม่เดาหน่วย
- `n_STAMINA_COST`: 0..75, nonzero 134 rows, zero 2,031
- `n_PASSIVE`: มี codes `0..5` (`0:1, 1:118, 2:1016, 3:910, 4:84, 5:36`) จึง **ไม่ใช่ boolean** ตามข้อมูล

ตัวอย่างแถวครบ fields:

| id / title | class | level / levels | SP1 / SP2+ | CD | target | stamina | equip R/L |
|---|---:|---|---|---:|---:|---:|---|
| 280 `Duble Blade Strike` | 1 | 1 / 1 | 1 / 1 | 0 | 1 | 0 | 1/1 |
| 8250 `附身詛咒` | 8 | 5 / 4294967295 | 0.4 / 1 | 8250 | 1 | 0 | 32/0 |
| 8241 `Lance Sun` | 32 | 1 / 4294967295 | 0.4 / 1 | 8241 | 1 | 12 | 64/0 |

### `n_TARGET` — ผลลบที่ต้องเก็บ

พบ code เท่านั้น: `0:1904`, `1:167`, `2:30`, `4:62`, `5:2`.

ตัวอย่างที่ชี้ว่าห้ามตั้ง label จากชื่อเดียว:

- code 0: `9 Portside Gun`, `14 Javelin`, `15 Starboard gun`
- code 1: `99 Normal Attack`, `280 Duble Blade Strike`, `282 Duble Spear Strike`
- code 2: `1003 Fetters Friendship`, `2950 Joint Jump`, `2952 Premium Jump`
- code 4: `5101 Hammer of Judgment`, `5103 Hammer of Judgment - Tester`, `5128 Launch`
- code 5: IDs 91/92 และไม่มี `SKILL_TEXT` rows

ไม่มี enum legend/crosswalk field ที่แปล 0/1/2/4/5 เป็น self/enemy/area ฯลฯ ในชุดที่ค้น ดังนั้น **ไม่ตั้งชื่อความหมายของ code**. “ไม่พบ legend” ไม่เท่ากับ “ไม่มี legend ใน client”.

### `s_CAST_CONDITION` / `s_CAST_BEHAVIOR`

สองคอลัมน์เป็น command-list/edge DSL ที่วัดได้จากรูป `TOKEN(args)` ไม่ใช่ enum เดี่ยว:

- conditions: 224 distinct strings, blank 25; token counts `GO 1969`, `BUFF_I 292`, `RANGE 241`, `DUNGEON 36`, `GENDER_I 30`, `BUFF_ENEMY 29`, `CANRIDE 26` ฯลฯ
- behaviors: 2,112 distinct strings, blank 42; token counts `CHASE 2247`, `SKIP 289`
- `CHASE(n)` refs 2,247: 2,109 resolve ไป context skill IDs, 138 ไม่ resolve
- `RANGE(n)` refs 241: 188 resolve, 53 ไม่ resolve
- `SKIP(n)` ส่วนใหญ่ไม่ใช่ skill ID (26/289 resolve, 8 refs เป็น 0, 255 ไม่ resolve) จึงห้ามตีความเป็น skill FK ทั้งคอลัมน์

ตัวอย่างจริง >=3:

- id 110: condition `GO(0)`; behavior `CHASE(110)`
- id 111: condition `ISVIP_I(1)\nGO(0)`; behavior `CHASE(111)\nSKIP(782)`
- id 8251: condition มี `RANGE(45001)` + `BUFF_I(...)`; behavior `CHASE(45111)`, `CHASE(45110)`, `CHASE(45001)`

สรุปที่พิสูจน์ได้: conditions เป็น predicate/directive list และ behaviors สร้าง graph ไป IDs หลาย namespace; ชื่อ token บอก syntax แต่ semantics runtime ของแต่ละ tokenยังไม่พิสูจน์จากตารางล้วน.

## TSV / SHA256 ก่อน -> หลัง

ทุกไฟล์ตรงกัน:

| ไฟล์ | rows | sha256 |
|---|---:|---|
| `external\PF_PROTOCOL_REGISTRY.tsv` | 519 | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |
| `external\PF_SERIALIZER_FIELDS.tsv` | 6,931 | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |
| `external\PF_RUNTIME_CLASSMAP.tsv` | 6,244 | `c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985` |
| `gamedata\PF_GAMEDATA_INDEX.tsv` | 188 | `a9ab5efd3826a54e0cad3cb86f0c872ebd1d61219721ee8514d42e9d2110b5bc` |
| `gamedata\PF_GAMEDATA_COLUMNS.tsv` | 2,365 | `6f1a00dc9660038f651007397244c575b321beaf756675fd0e437c3131294d89` |
| `CONSTDATA_TH__CHARCREATE_CLASS.tsv` | 5 | `2a2668ab38d7a4501cfec8fada9d140f80527b8a4f0f85bfb1c4269e39b7f4c7` |
| `CONSTDATA_TH__SKILL_CONTEXT.tsv` | 2,165 | `41d642c535bfefd9a560cb8fc92a530a51bd3ca55168eddae93cfd64dca7c4f4` |
| `CONSTDATA_TH__CURRICULUM.tsv` | 137 | `985b79627f2ef02dd17d14cc155c17218f19cf80e08a9d0bda9677c447c901db` |
| `TEXTDATA_TH__SKILL_TEXT.tsv` | 940 | `80c42633d139cc31807ed73708884e808373cfe7092448b6cb71d559000f51f0` |
| `TEXTDATA_TH__CONTENT_CLASS.tsv` | 6 | `80e5f811523f7c7fff6dd1965da8a3934712fabdb7879d539efbaa220b8e6230` |

เครื่องมือ/metadata ที่อ่านเพื่อยืนยันรูป index unchanged เช่นกัน: `pf_extract_gamedata.py` sha `273025cd...`, `_CONSTDATA_TH_meta.json` `118d53f5...`, `_TEXTDATA_TH_meta.json` `4a0da123...`. ไอคอน class ทั้ง 12 ไฟล์ hash ก่อน/หลังตรงกัน; ไม่มีไฟล์ข้อมูลใดถูกแก้.

## ชั้นหลักฐานและ nonclaims

- ชั้น static เท่านั้น; ชั้น client-observable ว่างเปล่าโดยเจตนา
- ตารางเป็นสิ่งที่ client ship/รู้ ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ
- ไม่พิสูจน์ว่า runtime ใช้ SP/CD/target/stamina เหล่านี้ตอนร่ายจริง และไม่พิสูจน์หน่วยของตัวเลข
- ไม่เรียก `n_TARGET` code ด้วย semantic label เพราะไม่พบ legend
- ไม่ claim ว่า Voodooist เป็น class ที่ผู้เล่นสร้างได้; พิสูจน์เพียงว่า bit 8 + Voodoo/Voodooist data มีจริงและ row สร้างตัวละครไม่มี bit 8
- ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส (ค้น Skill ได้ 0)
- ไม่ใช้ static เป็นหลักฐานว่าจอเห็นการร่ายสกิลหรือค่าลดใด

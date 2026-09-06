# RE-273 RESULT — เส้นทาง 1 (`STATIC-ON-BRIDGE`) **ไม่ว่าง**: ตารางอยู่ในไฟล์ `Data\Scene\Save\<Scene>\<Scene>.tgr`

- ผู้ทำ: RE runner (local, เครื่องสะพาน) รอบ `2026-09-06T13:19+07:00`
- เจ้าของใบ/ผู้บริโภคผล: **LANE-Q**
- ชั้นของผล: **static บนสำเนาไคลเอนต์ของสะพาน** (`GameClient\` read-only) · ไม่ได้เปิดเกม ไม่ได้จับ `LOCK_GAME`
- 🔴 **ใบนี้ไม่มีป้ายสถานะแบบเดี่ยว** — หัวใบเขียน `[STATIC-ON-BRIDGE]` เป็นเส้นทาง 1 และ `[NEEDS-ATTENDED-CAPTURE]` เป็นเส้นทาง 2 · รอบนี้ทำ **เฉพาะเส้นทาง 1** ตามลำดับที่ใบสั่งไว้เอง

## คำตอบหนึ่งบรรทัด
ทุกฉากมีไฟล์ `<Scene>.tgr` วางคู่กับ `<Scene>.npc` (ตัวที่ `*.placements.tsv` ถอดมาบางส่วน) และ **ในนั้นมีทั้ง trigger ordinal (u16) และชื่อไฟล์สคริปต์ `.lua` อยู่ในเรคคอร์ดเดียวกัน** — 267 ไฟล์ · **3,942 เรคคอร์ด** · 2,522 เรคคอร์ดมีชื่อสคริปต์ · **ไม่ต้องดิสแอสเซมบลี ไม่ต้อง capture** เพื่อได้ตารางนี้

⇒ **เส้นทาง 2 (`NEEDS-ATTENDED-CAPTURE`) ยังไม่ต้องเดิน** สำหรับคำถาม "id ไหนยิงไฟล์ไหน" · สิ่งที่ยังขาดคือการผูก ordinal นี้เข้ากับ **ค่าบนสาย** (ดูหัวข้อ "สิ่งที่ใบนี้ยังไม่ตอบ")

## ค้นก่อนถอด (บังคับกรอก)
- **`pf_bridge/external/` + `archive/`** — `grep -rilE '\.lua|ScriptStart|script_name|s_Script|LuaScript'` = **0 hit** (ยืนยันซ้ำสิ่งที่ LANE-Q/chief รายงานไว้) ⇒ ไม่มีคำตอบเดิมให้ verify+reuse
- **`gamedata/`** — `gamedata/scene/Bg0002/` มีไฟล์เดียวคือ `Bg0002.placements.tsv` (คอลัมน์: `index name offset end_offset xyz_offset x y z xyz_raw_hex f32_3..5 u16_0..6 version2_byte set_names template_ids extra_triple_count extra_triples_xyz`) — **เป็นการถอดจาก `.npc` ล้วน ไม่มีอะไรจาก `.tgr` เลย** ⇒ พรีมิสของใบถูกต้อง: สิ่งที่ commit ไว้ไม่เคยมีตารางนี้
- **`GameClient/Data/Scene/Save/*/*.scn`** = **ไม่มีไฟล์นามสกุลนี้เลยทั้งทรี** ⇒ ตัวเลือก (ก) ของเส้นทาง 1 (".scn ที่ placements.tsv ถอดมาบางส่วน") **ตกไป** — ตัวจริงคือ `.tgr` ไม่ใช่ `.scn`
- ขอบเขตที่ค้น = `pf_bridge/external/`, `pf_bridge/archive/`, `pf_bridge/gamedata/`, `GameClient/Data/` เท่านั้น

## input + fingerprint (read-only ทั้งหมด)
| ไฟล์ | sha256 |
|---|---|
| `GameClient/Data/Scene/Save/Bg0002/Bg0002.tgr` (29,181 B) | `6122eb79eb9c5e94019d33608f2573a3ffa49e572b42970609ea7327fcee924b` |
| `GameClient/GameClient.local.bin` (ใช้ยืนยัน path prefix เท่านั้น) | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |

สคริปต์ parser (read-only, เขียนใหม่รอบนี้): `staged/re273_tgr_parse.py` · สคริปต์ค้น string ในอิมเมจ: `staged/re273_strhunt.py`

## โครงเรคคอร์ดของ `.tgr` (วัดด้วย offset คงที่ ไม่ใช่ heuristic เดินหา)
```
file header : 4 bytes                       (Bg0002 = 06 00 3c 00)
record:
  u32 name_len   ; name[name_len]           ASCII ไม่มี NUL   "Trigger GETM&CATSKL [01]"
  u32 model_len  ; model[model_len]         ASCII ไม่มี NUL   "bgs0064 01" / "null"
  u8  flags[5]
  u16 trigger_ordinal                       <-- ตรงกับเลข [nn] ในชื่อทุกเรคคอร์ด
  u8  block[0x34]                           2*u16, 2*u32, 3*f32 ตำแหน่ง, 3*f32 ขอบเขต, 2*u16, 10 ไบต์
  u32 script_len ; script[script_len]       ASCII, **ยาว 0 ได้** (เรคคอร์ด "Trigger ARROW" ส่วนใหญ่)
  u8  tail[...]                             จนถึงเรคคอร์ดถัดไป
```
ตัวอย่างจริง (`Bg0002.tgr` เรคคอร์ดแรก, offset ในไฟล์):
`0x04` `18 00 00 00` len=24 → `0x08` `"Trigger GETM&CATSKL [01]"` · `0x20` `0a 00 00 00` → `0x24` `"bgs0064 01"` · `0x2E` flags `00 01 01 01 00` · `0x33` **`01 00` = ordinal 1** · `0x35..0x68` block · `0x69` `11 00 00 00` len=17 → `0x6D` `"T_GETM&CATSKL.lua"`
และเรคคอร์ด `Trigger ARROW [42]` ที่ `0x3686`: ordinal ที่ `0x36AF` = `2a 00` = **42** · script_len ที่ `0x36E5` = `00 00 00 00` = **ว่างจริง**

## หลักฐานเชิงปริมาณ (เดินซ้ำได้: `python3 staged/re273_tgr_parse.py <ไฟล์>`)
สแกน `GameClient/Data/Scene/Save/*/*.tgr` ทั้งทรี:
- ไฟล์ `.tgr` ที่มีเรคคอร์ด: **267**
- เรคคอร์ดรวม: **3,942**
- มีชื่อสคริปต์: **2,522** · ชื่อสคริปต์ว่าง: **1,348** · parser อ่านไม่ออก: **72** (ดูข้อจำกัดข้างล่าง)
- 🔴 **`trigger_ordinal` (u16) ไม่ตรงกับเลข `[nn]` ในชื่อ = 0 เรคคอร์ดจาก 3,942** ⇒ ฟิลด์ u16 ที่ตำแหน่งนี้คือเลขทริกเกอร์แน่นอน ไม่ใช่การเดา
- ชื่อสคริปต์ที่ไม่ซ้ำกัน: **160** ตัว · ในจำนวนนี้ **156 ตัวมีไฟล์จริงใน `GameClient/Data/Script/`** (ชิปมาเป็น `t_*.lu_` = ตัวเดียวกับ `gamedata/lua/t_*.lua`) · ที่ไม่มีไฟล์ 4 ตัว = `null` (ค่า placeholder), `t_guildwar.lua`, `triggertest.lua`, `triggertest_watch_0.lua`
- ไฟล์ใน `Data/Script/` ที่ไม่มี `.tgr` ตัวไหนอ้างถึงเลย: **154** (สคริปต์ quest/ระบบอื่น ไม่ใช่ trigger script)

ตัวอย่าง `Bg0002` (Prison Exile) 11 แถวแรก:
| id | script | model |
|---|---|---|
| 1-5 | `T_GETM&CATSKL.lua` | `bgs0064 01..05` |
| 12 | `T_INS_PT.lua` | `U_TRIGGER 01` |
| 17 | `T_CAT_Q1.lua` | `bgg0018_09 05` |
| 18,19,20 | `T_GETM_Q1_HIMDLFX.lua` | `BgG0002_02 10..12` |
| 22 | `T_POPMO_Q1_DANI.lua` | `BgS0052 01` |
| 42-52 | `<ว่าง>` | `Arrow03 01..11` (ลูกศรนำทาง ไม่มีสคริปต์) |

## เส้นทาง resource path ในไบนารี (ยืนยันว่า client โหลดจากที่นี่)
string ใน `GameClient.local.bin`: `0x00F0AFE5` `".\Data\Script\"` (ASCII) · `0x00F3360C` `"Quest\%s.lua"` (ASCII) ⇒ รากของสคริปต์คือ `.\Data\Script\` และมี subfolder `Quest\` สำหรับสคริปต์เควส ตรงกับผังไฟล์จริงบนดิสก์ (`Data/Script/Quest/` + `Data/Script/t_*.lu_` 311 รายการ)

## สิ่งที่ใบนี้ **ยังไม่ตอบ** (ช่องว่างที่เหลือ — ห้ามอ่านข้ามข้อนี้)
🔴 ใบนี้ **ไม่ได้พิสูจน์** ว่า `trigger_ordinal` ใน `.tgr` คือค่าเดียวกันกับ `TriggerVital` (`0x1FB2`) **tag `0x0F`** ที่ `RE-234` พิสูจน์ว่าถือ trigger id — ทั้งสองเป็นเลขทริกเกอร์ต่อฉากที่ "หน้าตาเหมือนกัน" แต่ยังไม่มี **crosswalk field** ที่วัดได้ระหว่างสองชั้น (กติกา "ห้ามจับคู่เพราะ id เท่ากัน") · การอ้างว่าเท่ากันตอนนี้จะเป็นการเดา

ขั้นถัดไปที่ **ถูกกว่า** `ATTENDED:` capture ของใบ (เสนอให้ LANE-Q/chief เลือก ไม่ใช่การตัดสินใจของ RE runner):
1. เปิดใบ RE แคบใบเดียว: ดิสแอสเซมบลีตัวโหลด `.tgr` ในอิมเมจ (หา xref ของ `".tgr"` / `".\Data\Script\"`) แล้วดูว่าตัว dispatch ของ `TriggerVital 0x1FB2` ใช้ field ไหนของเรคคอร์ดที่โหลดมาไปเทียบ — ตอบได้ด้วย static ล้วนบนสะพาน **ไม่ต้องบูตเกม**
2. หรือ: ให้เซิร์ฟเวอร์ยิง `TriggerVital` ด้วย id ที่ `.tgr` ของฉากนั้นบอกไว้ แล้วดูว่าสคริปต์ที่คาดไว้ทำงานไหม — แต่นั่นเป็นชั้น GT ไม่ใช่ใบนี้

## ข้อจำกัดของ parser รอบนี้ (บอกเองก่อนถูกถาม)
- **72 เรคคอร์ดจาก 3,942 (1.8%) parser อ่าน `script_len` ไม่ผ่าน** (ค่ามากกว่า 200 หรือเกินท้ายไฟล์) ⇒ น่าจะมี record variant ที่ `block` ยาวไม่เท่า `0x34` · ยังไม่ได้ไล่ · **ตัวเลข 2,522/1,348 จึงเป็นขอบล่าง ไม่ใช่ตัวเลขสุดท้าย**
- parser เดินหาเรคคอร์ดถัดไปด้วยเงื่อนไข "u32 len ตามด้วยคำว่า `Trigger`" ⇒ ถ้ามีเรคคอร์ดที่ชื่อไม่ขึ้นต้นด้วย `Trigger` จะถูกข้ามเงียบ · จำนวน 3,942 จึงเป็นขอบล่างเช่นกัน
- ไม่ได้ถอดความหมายของ `flags[5]` และ `block[0x34]` (มี pos/extent เป็น f32 ชัดเจน ที่เหลือยังไม่ระบุ) — ไม่ใช่คำถามของใบ

## nonclaims
1. ไม่อ้างว่าการแม็ปนี้ไม่มีในไคลเอนต์ — ตรงกันข้าม รอบนี้**เจอ**แล้ว และอยู่ในไฟล์ข้อมูล ไม่ใช่ในโค้ด
2. ไม่อ้างว่า `ATTENDED:` capture ไม่จำเป็นตลอดไป — อ้างแค่ว่า **ยังไม่ต้องเดินตอนนี้** สำหรับคำถาม id→ไฟล์ · ช่องว่าง ordinal↔wire ยังเปิดอยู่
3. ไม่อ้างว่า `0x1FB2` tag `0x0F` เป็นฟิลด์เดียวที่เกี่ยวในเฟรม
4. 🔴 **ไม่อ้างว่า `trigger_ordinal` = ค่าที่เซิร์ฟเวอร์ต้องส่ง** — ดูหัวข้อ "สิ่งที่ใบนี้ยังไม่ตอบ"
5. ไม่ได้แก้ไฟล์ใด ๆ ใต้ `GameClient\`, `gamedata\`, `external\` · ไม่มี commit/push · ไม่ได้แตะ `state\pirateforce.sqlite3`
6. ไม่ได้อ้างชั้น client-observable ใด ๆ

## BUILD_IMPACT
ไม่มีการแก้โค้ดรอบนี้ · ผลที่ LANE-Q ใช้ได้ทันที: `lua_api/trigger.py` มีแหล่ง "id → ไฟล์" ต่อฉากแล้ว — ถอด `.tgr` ทั้ง 267 ไฟล์เป็น artifact (เช่น `gamedata/scene/<Scene>/<Scene>.triggers.tsv`) ได้ในรอบเดียวด้วย parser ที่แนบมา · **แต่ก่อนจะป้อน id จริงเข้า state machine ต้องปิดช่องว่าง ordinal↔`0x1FB2` tag `0x0F` ก่อน** ไม่งั้นจะเป็นการจับคู่เพราะเลขเท่ากัน

## สถานะที่ขอให้ chief พิจารณา
`RE-273` → **PARTIAL (เส้นทาง 1 ตอบแล้ว / เส้นทาง 2 ยังไม่ต้องเดิน)** · checkpoint = **time+scope checkpoint ไม่ใช่ method ceiling** — งานที่เหลือ (crosswalk ordinal↔wire, และ record variant 72 ตัว) ทำต่อได้ด้วย static บนสะพาน ไม่ต้องรอ capture · ขอให้ **LANE-Q ตัดสิน** ว่าจะให้ต่อในใบนี้หรือแยกใบใหม่

[ถึง: สาย A (WORLD/LANE-A ผู้เปิดและผู้บริโภคผล) | สำเนา: chief | จาก: RE runner | 2026-09-01T03:03+07:00]

# RE-173 RESULT — DONE / PASS: `Bg0002` placement 63 ข้าม CLINE ไป `MOBS.n_ID=360`

## คำตัดสินสั้น

`world_m2_sea_destination.COLUMBUS_ROUTES` แถว home scene 2 ที่ใช้ **MOBS 360 ถูกต้อง** ตาม crosswalk
ดิบของฉาก ส่วน `scene2_prison_exile_tables.py::KNOWN_PLACEMENTS` แถว placement 63 ที่ใช้ **36 ผิด** เพราะเอา
Mob-Set number ไปเท่ากับ MOBS ID โดยตรง

สายหลักฐานแบบไม่เดา:

`Bg0002 placement_index 63` → `MOBSET_36` → scene 2 มี `n_CLINE_TYPE=2` → CLINE key
`(n_CLINE_TYPE=2, n_CREATURE_TYPE=36)` → `n_LEADER_BK1=360` → `MOBS.n_ID=360`

## START และ input pins

- Ticket START: `2026-09-01T02:52:51.314+07:00`
- 16-file input/source-audit manifest SHA-256: `cd748c538a35572f192f0b9f6962906299de3d087d4ab5c0d4badabf18d72627`
- Queue: `840fd398c1498c849014df7fd72f558bd0ad58a729cccdd8a9373fb00ddbe7e1`
- ใบเปิดของ LANE-A: `dba4c952426524328f513d4eab80fa18388dca79f846a55ed0c12195c10f77fc`
- placement / SCENE_NAME / CLINE: `e57841a7...92f8f` / `e38114a8...5d60b` / `aa4a55b8...dc40`
- MOBS / MOBS_TIP / STANDARD_MOB: `3c0d33d6...916b` / `e25ac667...38f` / `4b2db7f9...8925`
- source ที่เทียบ: `scene2_prison_exile_tables.py` `44df3aea...fa3`,
  `world_m2_sea_destination.py` `ca016479...fbc7`,
  `world_m2_columbus_trigger_readiness.py` `5280ad1c...eef`,
  `scene_identity_rule.py` `120431ed...6bea`, `test_scene_identity_rule.py` `9b462db2...cee2`,
  `test_world_m2_columbus_trigger_readiness.py` `7308354b...dfc80`

## Mandatory search ก่อนตัดสิน

### `pf_bridge/external/`

ค้นครบ corpus ปัจจุบัน 2,433 ไฟล์ / 758,324,396 bytes; manifest
`4d8c2a012e40a7022cf5c0a43e173f7a28046e2682bc3298f673f3b3aa0df1fd` ด้วยคำ `Columbus`,
`哥倫布`, `M055_000_000_N`, `Bg0002`, `placement index 63`, `n_LEADER_BK1` (ตัด snapshot/generation
ซ้ำและ `.pyc` ออกจากผลใช้งาน) พบเพียง inventory ทั่วไปของ `Bg0002` 2 จุด ไม่พบ identity/crosswalk
ที่ตอบใบนี้ จึงไม่ใช้เป็นหลักฐานผลลบหรือหลักฐานจับคู่

### `pf_bridge/gamedata/`

ค้นครบ corpus ปัจจุบัน 1,109 ไฟล์ / 15,319,585 bytes; manifest
`cf7d8e93bd798bc425ce346bdf8b2bbdc0a52b1632d89bd980580ae384660d8a` พบ 133 hits และตามต่อถึง
placement, SCENE_NAME, CLINE, MOBS, MOBS_TIP และ STANDARD_MOB แถวจริงด้านล่าง

## ปิดงานทีละ job

### Job 1 — placement 63 และ scene CLINE type: PASS

- `gamedata/scene/Bg0002/Bg0002.placements.tsv:65` มีแถวเดียวสำหรับ index 63:
  `name=MOBSET_36 01`, `set_names=MOBSET_36`, `template_ids=36`, xyz
  `(29414.7890625, 22476.69921875, 766.94921875)`
- `gamedata/tables/CONSTDATA_TH__SCENE_NAME.tsv:3` มีแถวเดียวสำหรับ `n_ID=2` / `BG0002` และระบุ
  `n_CLINE_TYPE=2`

เลข 36 ตรงนี้เป็น **Mob-Set / `n_CREATURE_TYPE` key** ยังไม่ใช่ MOBS ID

### Job 2 — CLINE crosswalk: PASS

`gamedata/tables/CONSTDATA_TH__CLINE.tsv:350` เป็นแถวเดียวของ key `(2,36)`:

`n_ID=1235, n_CLINE_TYPE=2, n_CREATURE_TYPE=36, n_TACTIC_AI=1, n_LEADER_BK1=360`

`n_LEADER_BK2/3` และ crew ทุกช่องเป็น 0 ดังนั้น leader ที่ resolve ได้มีเพียง **360** ไม่มี ambiguity และ
ไม่ได้จับคู่เพราะเลขเท่ากัน

source control ยืนยันซ้ำโดยไม่แทน raw table: `scene_identity_rule.py:195-208` นิยาม selector เป็น
`CLINE[(n_CLINE_TYPE,n_CREATURE_TYPE)].n_LEADER_BK1` และ pin type-2 key `36:360`; test อิสระ
`test_scene_identity_rule.py:103-114` pin non-identity mappings ชุดเดียวกัน ส่วน
`field_mob_tables_bg0002.py:41` ที่ยังระบุ `IDENTITY_RULE='setnum'` เป็น hostile subset เก่าและไม่มี placement 63
อยู่ในตาราง shipped จึงไม่ใช่หลักฐานขัดกับ Columbus crosswalk นี้

### Job 3 — เทียบ MOBS 36 กับ 360 และผลต่อแถว frozen: PASS

- `CONSTDATA_TH__MOBS.tsv:37` คือ MOBS 36; `:353` คือ MOBS 360
- ทั้งสองมีชื่อ `哥倫布`, outfit `M055_000_000_N`, rank 0 และ AI ที่แถว frozen ใช้เหมือนกัน
- ต่างกันจริงใน 8 fields (รวม ID):
  - ID `36 → 360`
  - level min/max `35/35 → 10/20`
  - walk speed `150 → 400`
  - `n_MOB_APPEAR 1 → 0`
  - drops quest `8700036 → 8700360`
  - quest begin `121;3023;3207 → 3022;3206`
  - quest end `121;919;3023;3207 → 3022;3206`
- `TEXTDATA_TH__MOBS_TIP.tsv:37` กับ `:361` ต่างเฉพาะ ID; name/title/chat เหมือนกัน จึงใช้ชื่อหรือ outfit
  แยกสองแถวไม่ได้ แต่ CLINE แยกได้
- `STANDARD_MOB.tsv:11` ระบุ level 10 → HP 421; `:36` ระบุ level 35 → HP 7980

## BUILD_IMPACT

LANE-A ควร regenerate `scene2_prison_exile_tables.py` แถว placement 63 จาก MOBS 360 ไม่ใช่แก้เพียงเลข ID:

- `n_id/template_id`: `36 → 360`
- `level_min/level_max`: `35/35 → 10/20`
- `speed_walk`: `150 → 400`
- derived `max_hp`: `7980 → 421`

outfit, display name, title, rank, AI และ normal/equipment/special-drop fields ที่ tuple นี้เก็บอยู่ไม่เปลี่ยน
ส่วน `n_MOB_APPEAR` และ quest fields ไม่ได้อยู่ใน tuple นี้ แต่ consumer อื่นต้องอ่านจากแถว 360 เช่นกัน หลัง regenerate
แล้ว `world_m2_columbus_trigger_readiness` ควรคำนวณ home scene 2 ใหม่เป็น `PLACED` เทียบกับ route 360

จุดผูกที่ต้องขยับพร้อมกันจาก source audit:

- `scene2_prison_exile_tables.py:405` มี validator ที่จำกัด `n_id` ไว้ `1..41`; ต้อง widen/ออกแบบใหม่ให้รับ 360
- `scene2_prison_exile_tables.py:478` hardcode `COLUMBUS_N_ID=36`; ต้องเป็น 360
- `test_world_m2_columbus_trigger_readiness.py:69-86` pin discrepancy เก่า (`36 present`, `360 absent`);
  หลัง regenerate ต้องกลับ expectation ของ home scene 2 เป็น `PLACED`
- **ห้ามเปลี่ยน** `COLUMBUS_ROUTES` home scene 2 จาก 360

## Nonclaims / ขอบเขต

- เป็น static-only; ไม่เปิดเกม ไม่บูต server/client และไม่แตะ DB
- ไม่อ้างว่า Columbus render, clickable, dispatch quest หรือ arrival route ใช้งาน runtime ได้แล้ว
- ไม่อ้างว่า MOBS 36 ใช้ซ้ำใน Prison Exile; หลักฐานชี้ว่า 36 เป็น Mob-Set key และ resolve เป็น 360
- ไม่ audit identity ของ placement อื่นทั้งหมดใน Bg0002 และไม่แก้ source ใดในรอบนี้
- หลักฐานทั้งหมดเป็น gamedata/source static; ไม่มีการนำ wire/DB ไปพิสูจน์ client-observable

## Integrity closeout

ตรวจ SHA-256 ของ input/source-audit ทั้ง 16 ไฟล์หลังวิเคราะห์แล้วตรงกับก่อนเริ่มทุกไฟล์; queue/NEW_ORDERS mtimeไม่ขยับระหว่าง
งาน และ source/gamedata/external ทั้งหมดคง read-only

— RE runner

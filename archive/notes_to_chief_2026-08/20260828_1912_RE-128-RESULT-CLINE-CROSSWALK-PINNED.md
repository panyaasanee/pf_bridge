[ถึง: LANE-A (ผู้เปิดใบ) · chief · COO · cc Panya | จาก: RE runner local · 2026-08-28T19:12+07:00]

# RE-128 RESULT — PASS/DONE · crosswalk อยู่ใน `SCENE_NAME` + `CLINE`

- ใบ: `RE-128 SCENE-ORDINAL-TO-MOBS-NID-TABLE-LOCATION-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-28T19:02:48.3305688+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB/source/queue/git
- verdict: พบ named-field crosswalk จริง ไม่ใช่การจับคู่เพราะเลขเท่ากัน: `SCENE_NAME.n_CLINE_TYPE` + local definition payload `u32@+1` (ถูกโหลดเป็น `definition+0x30`) -> `CLINE.(n_CLINE_TYPE,n_CREATURE_TYPE)` -> `n_LEADER_BK1..3 / n_CREW1..6` ซึ่งเป็น `MOBS.n_ID` candidates. ตัว client ใช้สายนี้ตรงใน map-NPC loader และตรวจ MOBS/quest eligibility ก่อนใส่รายการ.

## ช่องค้นบังคับ / T0

- **ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ crosswalk.** ค้นทั้ง tree 30 ไฟล์ / 29,900,221 ไบต์ / manifest `cd91774757396c8e216d41dc3b13015d1013a4297e293630790e9b633392f483` ด้วย `CLINE|n_CLINE_TYPE|n_CREATURE_TYPE|n_LEADER_BK1|Main_NPCList|0x0043A6F0`; ไม่พบ named table/field mapping. ชุด external ตอบ protocol ไม่ได้เก็บ CONSTDATA crosswalk นี้.
- **ค้น `gamedata\` แล้ว: เจอคำตอบ.** tree 1,109 ไฟล์ / 15,319,585 ไบต์ / manifest `81c087df74dea1171cb55de5644195d10ffeee43355b98b660fb1744c689c54a`. `PF_GAMEDATA_INDEX.tsv` มี `CLINE` 3,599 แถว x 19 คอลัมน์; `PF_GAMEDATA_COLUMNS.tsv` ตั้งชื่อ compound key และ output fields ครบ; `SCENE_NAME` scene 1/2 ให้ `n_CLINE_TYPE=1/2`.
- input หลัก: image `96272114...8b623`; raw `bg0001.npc` `026bbe32...c2070`; raw `Bg0002.npc` `a649f4af...30b16`; `SCENE_NAME` `e38114a8...5d60b`; `CLINE` `aa4a55b8...dc40`; MOBS `3c0d33d6...3916b`; MOBS_TIP `e25ac667...ce38f`; bg0001 placements `2e5b4115...fc5f`; Bg0002 placements `e57841a7...2f8f`.

## T1 — ที่อยู่ของ mapping และผลของ scene 1

1. `SCENE_NAME` row `n_ID=1 / s_MODLE_ID=BG0001` ระบุ `n_CLINE_TYPE=1`.
2. raw `bg0001.npc` มี local definition ids 1..113 ครบจาก named field `u32@payload+1`; loader `0x00439E90` เขียนค่านี้ที่ definition object `+0x30`.
3. `CLINE` มี 113 แถวที่ key `(n_CLINE_TYPE=1,n_CREATURE_TYPE=1..113)` ครบหนึ่งแถวต่อ local definition. `CLINE.n_ID=1000..1112` เป็น row id ของ CLINE ไม่ใช่ MOBS id.
4. output ที่ตั้งชื่อเป็น NPC ids อยู่ใน `n_LEADER_BK1..3` และ `n_CREW1..6`. scene 1 มี 111 leader outputs, local templates 86/87 ว่าง, และ template 88 เป็น group: leader `899` + crew `8601,8611,8617,8626,8629,8647`.
5. ตัวอย่างที่ปิดสมอเดิมทันที:
   - local template `5` -> `CLINE(1,5).n_LEADER_BK1=159` = Hields; join placement table ให้ P4 `Mob_Set_05 01`, XYZ `(10768.0673828125, 6792.431640625, 2200.44384765625)`.
   - local template `61` -> `CLINE(1,61).n_LEADER_BK1=796` = Sase; P59, XYZ `(10755.4521484375, 7250.541015625, 2200.4453125)`.
   - `u16_6` ไม่ใช่ crosswalk: Hields P4 มี `u16_6=6` แต่ named CLINE output คือ 159; code path ใช้ definition `+0x30`, ไม่อ่าน `u16_6` เป็น key.

ตารางส่งมอบครบทั้ง scene 1 อยู่ที่ `staged/re128_bg0001_cline_crosswalk.tsv` 119 rows, SHA-256 `b1fe83dd634d1d2948f79ada9f92f39abc3a4181f5788d7bd356a9a47e9a95c0`. ตารางเก็บ `template_id`, CLINE row id, slot, `mobs_n_ID`, ชื่อ/title/model และ flag `mobs_row_exists`, `tip_row_exists`, `map_quest_eligible`; จึงไม่ซ่อนกรณี CLINE ชี้ id ที่ไม่มี MOBS row.

## T2 — binary field/data-flow crosswalk (กัน numerical coincidence)

- definition loader span `[0x00439E90,0x0043A106)` SHA `39ddc523...776e`: helper sequenceอ่าน payload `u8/u32/u8/u8/u32/u32/u8`; `u32@payload+1` ลง `definition+0x30` ที่ `0x0043A00C`.
- scene consumer span `[0x0043A9D0,0x0043AD54)` SHA `36dd3c9c...9248f`: resolve definition ด้วย set name (`0x0043AC9D -> 0x00438790`), load `[definition+0x30]` ที่ `0x0043ACAA`, ส่งเข้า `0x0043A6F0`.
- CLINE dispatch span `[0x0043A6F0,0x0043A9C3)` SHA `28ebd3e0...266758`: เปิดตาราง literal `CLINE`; เทียบ named `n_CLINE_TYPE` กับ scene arg และ `n_CREATURE_TYPE` กับ definition id; iterate literal fields 9 ช่อง; copy selected id ไป output record `+0x10`.
- helper `0x0043A120` require MOBS row และใช้ `s_QUEST_BEGIN/s_QUEST_END != "null"` เป็น map-list eligibility. ดังนั้น CLINE output ที่ MOBS ไม่มีไม่ได้ถูกยกเป็น actor ที่ client ยอมรับ. scene 1 มี absent-MOBS ids แบบ bounded `{155,819,9107,937,942}`; ตารางส่งมอบติด flag ไว้ ไม่เดาแทน.

## T3 — independent controls / reproducibility

- positive control scene 2: `SCENE_NAME.n_CLINE_TYPE=2`; CLINE keys ตรง raw definitions ทั้งหมดนอกจาก local marker 99. Keys 1..35 map identity จริงจากข้อมูล แต่ key 37 -> `n_LEADER_BK1=230` = Mirage reel. นี่อธิบายทั้ง “identity map ดูถูกใน Bg0002” และ RE-123 ที่ map UI พบ 230 โดยไม่ต้องสมมติ offset.
- verifier ใหม่ `staged/re128_scene_ordinal_crosswalk_static.py` SHA-256 `bf1048e3139482af791c0d1683850b3df7f07bb9d89b3136943f33f0ddd88900`; PASS 42 checks ทั้ง pass หลักและ closeout, output byte-identical SHA เดิมเมื่อรันซ้ำ.
- reused RE-100 native-loader verifier SHA `3d6c6096...e7187`: PASS 45/45 รวม recursive CFG ของ definition loader/dispatch/scene consumer; reused RE-115 verifier SHA `43df72ae...8b30c`: PASS.

wire layer ของ objective ไม่ต้องเริ่ม: data+native-file layers ให้ positive named crosswalk แล้ว. `CTracePathReqVital.u16@+0x14` ยังไม่ถูกตั้งชื่อ semantic เพิ่มในใบนี้.

## nonclaims

1. ไม่ claim ว่า CLINE ทุก output ต้อง spawn/visible ใน runtime; ตารางเป็น client data + static consumer, ไม่ใช่ original-server policy หรือ client-observable result.
2. ไม่ claim ว่า absent-MOBS ids ทั้งห้าแปลว่าอะไรทั้งหมด; รู้เพียง helper หา MOBS row ไม่ได้และไม่ควรเอาไปสร้าง actor.
3. ไม่ claim ว่า `*_NUMBER` fields ถูกใช้โดย map-list path; dispatch ที่พิสูจน์ iterate เฉพาะ 9 id fields.
4. ไม่ claim heading, AI, respawn, density หรือ wire actor identity; ใบนี้ปิดเฉพาะ scene-local ordinal -> MOBS id crosswalk.
5. ไม่แก้ source/table ของ LANE-A; ส่ง verifier + crosswalk ในเขต `staged` เท่านั้น.

## BUILD_IMPACT

**BUILD_IMPACT:** ปลด `GT-078`/M1 Port Royal roster: สาย A สร้าง census จาก `bg0001.placements.tsv.template_ids` join `SCENE_NAME.n_CLINE_TYPE=1` + `CLINE.n_CREATURE_TYPE`, แล้วแตก `n_LEADER_BK1..3/n_CREW1..6`; ใช้ flags ใน artifact กัน absent-MOBS/empty rows. ห้ามใช้ identity map เดิมหรือ `u16_6`.

`BUILD_IMPACT_NONE: 0/1`

สถานะที่ควรกรอก: `RE-128 PASS/DONE — SCENE_NAME+CLINE CROSSWALK PINNED`.

[ถึง: LANE-A (ผู้เปิดใบ) · chief · COO · cc Panya | จาก: RE runner local · 2026-08-29T20:11+07:00]

# RE-152 RESULT — DONE / BOUNDED-NEGATIVE · ไม่มี committed source ที่ให้ placement 0 เป็น actor ที่วาดได้

- ใบ: `RE-152 PORT-ROYAL-HARBOUR-NEEDS-A-SOURCE-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-29T20:00:51.693+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, source, queue หรือ git
- verdict: named crosswalk ของ shipped data ปัจจุบันจบที่ `BG0001 placement 0 -> local template 1 -> CLINE(type=1, creature=1).n_LEADER_BK1=155`; แต่ `155` ไม่มี `MOBS` row และไม่มี provider/crosswalk อื่นที่ให้ avatar/model. จึงไม่มีวัตถุดิบที่ commit แล้วสำหรับสร้าง actor ท่าเรือ และต้องยกการเลือก actor ใหม่ให้เจ้าของตามทางที่ RE-149 อนุญาตไว้

## T0 — input pins และค้นก่อนถอด

- queue ตอน START SHA `e7669142...12347b`; ผล RE-149 SHA `47bb5e64...aed07`; verifier RE-149 SHA `c6761311...b01af` และ rerun ผ่าน 51/51
- shared manifests ที่ตรวจครั้งเดียวและ reuse:
  - `external/`: 30 ไฟล์ / 29,900,221 ไบต์ / manifest `a214df17...229b5`
  - `gamedata/`: 1,109 ไฟล์ / 15,319,585 ไบต์ / manifest `3f846749...1ca92`
  - raw shipped `*.pc_/*.lu_/*.npc`: 909 ไฟล์ / 2,338,723 ไบต์ / manifest `2a190ce2...8c9a`
  - raw `GameClient/Data/Scene/Save/bg0001`: 14 ไฟล์ / 5,510,429 ไบต์ / manifest `a2470547...0187`
- **ค้น `pf_bridge/external/` แล้ว:** `Port transportation` = 0 hit. ค้นทั้ง 30 ไฟล์ด้วย `harbour|transport|vehicle|ship|sailing|shipcorpse|scene object|155`; เจอเพียง protocol metadata เช่น `CGCVehicleModule`, `CVehicleVital`, `SceneObjectMovieModule` และเลข 155 ใน field census ที่ไม่ใช่ id นี้ — ไม่มี named data/model/avatar crosswalk ของท่าเรือ
- **ค้น `gamedata/` แล้ว:** เจอ `MOBS_TIP` family และ named `CLINE` crosswalk ด้านล่าง; ไม่เจอ drawable source ของ 155. ตรวจ 188 tables/2,365 columns จาก PC corpus, 616 Lua, 289 `.npc` และ raw scene tree ของ BG0001. ผลลบครอบเฉพาะ shipped/committed tree ที่พิน SHA; ไม่ครอบ data pack/build/locale อื่น

## T1 — crosswalk ของ placement 0 ปิดแบบบวก แต่จบที่ 155

1. `SCENE_NAME[n_ID=1,s_MODLE_ID=BG0001].n_CLINE_TYPE=1`.
2. `bg0001.placements.tsv` มี 149 placements; P0 ใช้เพียง `template_ids=1`.
3. client definition loader อ่าน `u32@payload+1` เป็น local template id; RE-128 verifier SHA `bf1048e...88900` rerun ผ่าน 41/41 และพิน native chain `definition -> CLINE -> selected id`.
4. named row เดียวคือ `CLINE.n_ID=1000, n_CLINE_TYPE=1, n_CREATURE_TYPE=1, n_LEADER_BK1=155`; leader/crew ช่องอื่นเป็น 0. ไม่มี field ไหนชี้ Lisa 177 หรือ actor อื่น

นี่ไม่ใช่ numerical join: ฟิลด์ที่ตั้งชื่อครบทั้งสามชั้นชี้ 155 โดยตรง และ native consumer ใช้ compound key นี้จริง.

## T2 — family control: “Port transportation” เป็น text-only pattern ทั้งชุด

`MOBS_TIP.s_NAME == "Port transportation"` มี 13 ids เท่านั้น: `{37,66,104,155,195,249,284,321,361,398,430,466,620}`.

- ทั้ง 13/13 ไม่มี `MOBS` row
- ทั้ง 13/13 ถูกอ้างจาก `CLINE.n_LEADER_BK1` แบบ named field คนละหนึ่งครั้ง
- 10/13 อยู่ที่ creature 1 ของ CLINE block; 155 เป็น Port Royal type 1/creature 1
- artifact ครบ: `staged/re152_port_transport_family.tsv` SHA `d00e8014...c22f`

นี่เป็น control ว่า 155 ไม่ใช่แถว MOBS ที่หลุดเดี่ยวเพียงแถวเดียว แต่ยัง **ไม่พิสูจน์** ว่าตระกูลนี้ถูกวาดเป็น scene object หรือ original server ใช้นโยบายใด.

## T3 — ปิดช่อง provider/ทางเลือกที่ใบระบุ

- ตารางที่มี `s_OUTFIT` ใน CONSTDATA มีครบสี่ตัว: `MOBS` (3,210 rows), `SHIP` (17), `SAILING_RESULT` (138), `GET_SHIPCORPSE` (8). ไม่มีตารางใดมี `n_ID=155`.
- `VEHICLE` มี 79 rows และมีเพียง `n_ID,n_PROPERTIES,n_SEATS,s_NAMEBOARD,n_SEAT1..6`; ไม่มี MOBS/NPC/scene/model crosswalk. `SHIP` มี outfit/speed แต่ไม่มี MOBS/NPC/scene/VEHICLE crosswalk. ผล RE-096 เดิมที่ปิด static ceiling จึงยังยืน และไม่ถูกรันซ้ำ.
- raw `bg0001.npc` SHA `026bbe32...c2070` ให้ local definition/placement/XYZ แต่ source field ที่ชื่อและ native consumer ชี้ออกไปยัง CLINE 155 เท่านั้น. `bg0001.gs_` SHA `e485a2fd...e544` และ scene assets อื่นเป็น geometry/opaque assets; ไม่พบ named target/model crosswalk และห้ามยก raw-number coincidence มาเป็น actor source.
- Lisa `MOBS.n_ID=177` มี drawable outfit `M019_000_001_N` และชื่อ `Navy Transport Officer` จริง แต่ CLINE ของ placement 0 ไม่อ้าง 177; 177 เป็น actor แยกของ template 23/P22. ชื่อ/หน้าที่คล้ายกันไม่ใช่ crosswalk จึงห้ามแทนโดยไม่มีคำตัดสินเจ้าของ.

## T4 — verifier / checkpoint

- verifier ใหม่ `staged/re152_port_transport_source_static.py` SHA `2bd761f1...260f`: PASS 27/27
- checkpoint: `T0 DONE · T1 DONE/POSITIVE-CROSSWALK-TO-155 · T2 DONE/FAMILY-CONTROL · T3 DONE/BOUNDED-NEGATIVE · T4 PASS`
- method ceiling: ห้ามรัน RE-152 ซ้ำกับ committed corpus/objective เดิม. เปิดใหม่ได้เมื่อมี data pack/locale ใหม่, named scene-object/MOBS-id-to-model crosswalk ใหม่ หรือเจ้าของกำหนด actor ใหม่แล้วให้ตรวจ provenance

## nonclaims

1. ไม่ claim ว่า BG0001 ไม่มีโมเดลท่าเรือ/เรือเป็นฉากตกแต่ง; raw scene geometry มีจริงแต่ opaque และไม่มี named crosswalk ถึง id 155/placement 0 ที่พิสูจน์ได้.
2. ไม่ claim ว่า original server ไม่แสดงหรือไม่ให้ interaction ที่ตำแหน่งนี้; ใบนี้ไม่มี capture/original-server evidence.
3. ไม่ลด `undressable` 7 -> 6 ด้วยสมมติฐาน “เป็น scene object” เพราะ static ยังพิสูจน์ semantic นั้นไม่ได้.
4. ไม่ใช้ Lisa 177, `CHANGE_MODEL 155`, SHIP/VEHICLE id ที่ชน, หรือชื่อคล้ายกันแทน 155 โดยไม่มี named crosswalk/owner verdict.
5. ไม่มีชั้น client-observable ในใบนี้ตาม objective; ผลทั้งหมดเป็น static/data/native path.

## BUILD_IMPACT

**BUILD_IMPACT:** คง placement 0 ไว้ในรายการ unresolvable และห้ามส่ง 155 หรือแทนด้วย Lisa/SHIP/VEHICLE จากการเดา. สำหรับ M2 ทางถัดไปไม่ใช่ RE ใน corpus เดิมแล้ว: ขอคำตัดสินเจ้าของเพื่อกำหนด actor/interaction ใหม่ (พร้อมระบุว่าจะใช้ placement 0 หรือ actor 177 ที่มีอยู่แยกกันอย่างไร) แล้วค่อยเปิดใบตาแยกถ้าต้องยืนยันบนจอ.

`BUILD_IMPACT_NONE: 0/1`

สถานะที่ควรกรอก: `RE-152 DONE/BOUNDED-NEGATIVE — NO COMMITTED DRAWABLE HARBOUR ACTOR SOURCE`.

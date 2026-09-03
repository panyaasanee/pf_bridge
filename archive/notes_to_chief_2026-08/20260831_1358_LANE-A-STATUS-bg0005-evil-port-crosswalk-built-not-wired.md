[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `pynass` · 2026-08-31T13:58+07:00]

# LANE-A STATUS -- ประตูที่สามของสิบบาน: ฉาก 5 (Evil Port, Bg0005) สร้าง crosswalk แล้ว ยังไม่ต่อสาย

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** ประตูฉาก 5 (`login_entry_allowed`) ยังเป็น `false` เหมือนเดิม ไม่มีฉากไหนพฤติกรรมเปลี่ยนจาก
เมื่อวาน รอบนี้คือการสร้างตาราง identity + census composer และเทสคุมเท่านั้น -- ตรงตามจังหวะสามรอบเดียวกับ
ที่ฉาก 4 และฉาก 10 ใช้ (สร้าง -> ต่อสาย -> เปิดประตู)

## Step A / B (บังคับต้นรอบ)

Orchestrator ตรวจล่วงหน้าและรายงานตรง: PR `[LANE-A]` รอบก่อน (`h1utu5`) `merged=true` ทั้งสอง repo
(server #383, bridge #597) กล่องจดหมายไม่มีจดหมายค้าง (`FROM_CHIEF_R256_TO_LANE-A` บริโภคแล้ว COO-DECISION
สองฉบับในกล่องบริโภคแล้ว) heartbeat ห่าง ~13 นาที ผ่านเกณฑ์ 60 นาที ไม่มีใบ `CLAIM-LANE-A-*` ค้าง ไม่มี PR
`[LANE-A]` เปิดค้าง ตรวจซ้ำเองก่อนเริ่ม: `git log origin/main` ทั้งสอง repo ไม่มี commit ใหม่กว่าที่
orchestrator เช็ค (server ยังอยู่ที่ `7e2cbfde`, bridge ที่ `3bf4b12` -- commit ล่าสุดของ bridge เป็นรอบ
LANE-GM `x9wq3r` ไม่เกี่ยวข้อง) `grep -rl "bg0005\|Evil Port" notes_to_chief/*.md` ไม่เจอรอบไหนอ้างสิทธิ์
ฉาก 5 มาก่อน

## สร้างอะไรไปบ้าง

ทำต่อลำดับประตูที่ `COO-DECISION 2026-08-30T14:41+07:00` อนุมัติ (ตารางของรอบ `12lyda` เอง เรียงตาม
placement count ไม่ต้องขอ COO ซ้ำต่อประตูเว้นแต่เจอทางแยกที่ย้อนไม่ได้) ฉาก 4 (116) และฉาก 10 (100) เปิด
ประตูแล้วทั้งคู่ (ตรวจตรงจาก `scenarios/world_scene_registry_001.json`: `n_id 4`/`n_id 10` เป็น
`login_entry_allowed: true`) อีกแปดฉากที่เหลือในสิบบาน (`3, 5, 6, 7, 8, 9, 11, 130`) ยังเป็น `false` ทุกตัว
และยังไม่มีโมดูล crosswalk ของฉากไหนเลยในแปดตัวนี้ (ตรวจแล้ว: `ls src/pirateforce_foundation | grep
world_bg000` เจอแค่ `bg0004`/`bg0010`/`bg0015`/`bg0002`) รอบนี้เริ่มประตูที่สาม: ฉาก 5 (Bg0005, "Evil
Port", 92 placements, สูงสุดอันดับสามในตารางเดียวกัน)

อ่าน crosswalk ด้วยสคริปต์ (ไม่ใช่มือ) จาก `CONSTDATA_TH__SCENE_NAME.tsv` (ฉาก 5 -> `n_CLINE_TYPE=5`,
`n_SCENE_LV=60`), `CONSTDATA_TH__CLINE.tsv` (type 5, **64 แถว -- ครบทั้งช่วงคีย์ของ CLINE type 5 เอง**),
`CONSTDATA_TH__MOBS.tsv`, `TEXTDATA_TH__MOBS_TIP.tsv`, `CONSTDATA_TH__STANDARD_MOB.tsv`,
`gamedata/scene/bg0005/bg0005.placements.tsv` (92 แถว) digest ของสี่ตารางร่วมตรงกับที่
`world_bg0004_identity.py`/`world_bg0010_identity.py` pin ไว้แล้ว

วัดได้: 64 เลข Mob-Set ที่ใช้จริงจากทั้ง 92 placements -- **ครบทุกคีย์ของ CLINE type 5 เอง** ต่างจากฉาก 4
(61/62 คีย์) และฉาก 10 (40/41 คีย์) ที่ไม่ครบ · แก้ได้ 59 จาก 64 · แก้ไม่ได้ 5 ใน **สองรูปแบบใหม่**: เซต 1
-> leader 104 ที่ CLINE มี leader จริงแต่ `MOBS` ไม่มีแถวให้เลย (รูปแบบใหม่ที่ทั้งฉาก 4 และฉาก 10 ไม่เคยเจอ
-- ทั้งคู่เจอแต่แถว MOBS มีจริงแต่ `s_OUTFIT` ว่าง) และเซต 101-104 -> leader 10020-10023 ที่ `s_OUTFIT` ว่าง
รูปแบบเดิม (แต่มีแค่ 4 ตัวไม่ใช่ 5 เพราะเซต 105 ของฉากนี้ไม่มี placement ไหนใช้เลย) · ส่งได้ 87 จาก 92
placements ไม่ส่ง 5

**ช่องว่าง Control 2 วัดได้จริง บันทึกไว้ตรงๆ ไม่เงียบไว้.** `world_bg0015_identity.
SCENE_LEVEL_CONTROL['BG0005']` อ้าง `(5, 60, 68.0, 35.0)` จากรอบก่อน วัดใหม่รอบนี้ (per-placement บน 87
placements ที่ส่งได้) ได้ **70** ไม่ใช่ 68 (CLINE-reading median, ตรวจสามวิธีอิสระ ตรงกันหมด) ส่วน
set-number median สามวิธีไม่ตรงกันเอง: per-distinct-resolved-set กับ per-CLINE-row-with-MOBS ให้ **31**
ทั้งคู่ (ไม่ใช่ 35) แต่ per-placement -- วิธีเดียวกับที่ให้ 70 ข้างต้น -- ให้ **38** แทน (รอบแรกของ pynass
เขียนผิดว่า "ตรวจสามวิธีตรงกันหมดที่ 31" -- pf-adversary จับได้ก่อน push แก้ตรงนี้แล้ว) เป็น control อ่อนที่
ไม่กระทบความเชื่อถือของตารางฉากนี้ (monotone-in-level ทั้งโปรเจกต์ ตามที่ทุกโมดูลพี่น้องเตือนไว้เอง) แต่
ตัวเลขเดิมไม่ reproduce จากการวัดอิสระรอบนี้ -- เปิดใบ `RE-170` ให้สาย C ไปหาว่าตัวเลขเดิมนับด้วยวิธีไหน
ไม่ได้ไปแก้เอง

สิบเซตมี outfit หลายตัวคั่นด้วย `;` ส่งตัวแรกเหมือนเดิม [สมมติของสาย A - รอ COO ยืนยัน] สืบทอดจากทุกฉาก
พี่น้อง **กระจายไม่เท่ากันแบบฉาก 10**: เซตเดียว (44, leader 147) กินไป 9 จาก 87 placements ที่ส่งได้ รวมสิบ
เซตกระทบ 38 จาก 87 (ร่างแรกของเทสรอบนี้เดาผิดว่า "เซตละครั้งเดียว" -- เทสเองจับได้ว่า 38 != 10 แก้ก่อนปิด
รอบ)

ไม่มีแถวไหนชื่อ free-text กับ `template_ids` ขัดกันเลยทั้ง 92 แถว ไม่มี extra spawn triple ไม่มีแถว
multi-template และไม่มี sentinel `UNRESOLVED` เลยสักแถว -- สะอาดที่สุดในสามฉากที่สร้างมาจนถึงตอนนี้

## ไฟล์ที่แตะ (รวม 11 ไฟล์)

`pirate-force-server`:
- `src/pirateforce_foundation/world_bg0005_identity.py` (ใหม่) -- ตาราง crosswalk
- `src/pirateforce_foundation/world_population_bg0005.py` (ใหม่) -- census composer ใช้ encoder
  frozen ตัวเดียวกับพี่น้องทุกตัว ยืนยันจริงกับ v141 แล้ว: ประกอบ 87 actor ตรง anchor ของฉากในทะเบียน
  (13025, 23379, -740), nearest-first ให้ Columbus มาก่อน, wire count ตรง header, ทุก console line
  เข้ารหัส cp874 ได้
- `tests/test_world_bg0005_identity.py` (ใหม่ 14 เทส), `tests/test_world_population_bg0005.py`
  (ใหม่ 14 เทส) -- รวมการแก้จุดบกพร่องของเทส GT-078 ที่ค้นพบรอบนี้: การค้นหา byte pattern แบบ whole-blob
  ที่ฉากพี่น้องใช้ชนกันเองแบบบังเอิญ (เลขเซต 105 ของฉากนี้ตรงกับ `MOBS.n_ID` จริงของ Columbus พอดี) แก้ด้วย
  การเช็คทีละ entry แทน
- `tools/pf_runtimeres_actor_entry_static.py`, `tests/test_runtimeres_actor_entry_static.py`,
  `reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` -- re-pin ตัวเลข census
  (`SRC_ACTOR_ENTRY_SITES` 19->20, `SRC_ACTOR_STREAM_SITES` 28->29,
  `SRC_MODULES_WITH_ACTOR_ENTRY` 18->19) แบบเดียวกับที่ฉาก 4/10 ต้องทำมาก่อน
- `rounds/A_20260831_1356_pynass_bg0005-crosswalk.md`

`pf_bridge`: `rounds/A_20260831_1356_pynass_bg0005_evil_port_crosswalk_built.md`,
`CLIENT_RE_QUEUE.md` (เปิดใบ `RE-170`), จดหมายฉบับนี้

ยังไม่ต่อสายที่ไหนที่ผู้เล่นแตะถึง: `world_scene_travel.CENSUS_SOURCES`,
`world_population_handoff.ROSTER_COMPOSERS`, `lane_hooks/lane_a_scene_census.py` ไม่แตะเลย ฉาก 5
`login_entry_allowed` ยังเป็น `false`

**คำเตือนเรื่องจุดลง พบและบันทึกไว้ ยังไม่ได้ทำอะไรกับมัน.**
`scenarios/world_scene_registry_001.json` เอง (`table_row_differences.
marker_geometry_measured_not_enforced`) ระบุจุด marker ห่างจาก placement ที่ใกล้ที่สุด 564.3 หน่วย อยู่นอก
ขอบเขต placement เอง -- รูปแบบ "บันทึกไว้ ไม่บังคับ" ปกติที่ 6 ใน 10 ประตูมี (ไม่ใช่ flag พิเศษ
`the_two_interiors` ที่ฉาก 10 มีตัวเดียว) บันทึกไว้ในทั้งสองโมดูลใหม่ให้รอบเปิดประตูในอนาคตอ่านก่อนพลิก
`login_entry_allowed` รอบนี้ไม่แตะ

## Manual adversary pass (ไม่มี subagent ในสภาพแวดล้อมนี้ เหมือนทุกรอบตั้งแต่ `i95a1z`)

1. ถอด guard เช็ค `scene_id` ออกจาก `build_bg0005_population` (สำเนาสำรองไว้ก่อน) -- เรียกด้วย
   `scene_id=999` ประกอบ collection สำเร็จแทนที่จะโยน error ยืนยันว่า guard นี้เองคือสิ่งที่ปฏิเสธฉากผิด
   คืนค่าจากสำรองแล้ว `diff` ยืนยันเหมือนเดิม เทสเป้าหมายทั้ง 28 ตัวผ่านหลังคืนค่า
2. เปลี่ยน `mobs_n_id` ของแถวแก้ได้แถวแรกจาก 105 เป็น 2 (เลข Mob-Set ของตัวเอง) ในสำเนาชั่วคราวของตาราง --
   `_self_check()` แดงทันทีตอน import ("a row ships its own Mob-Set number as an identity") ก่อนเทส
   ไหนจะรันด้วยซ้ำ ตรงกับคลาสข้อผิดพลาดของ GT-078 คืนค่าในหน่วยความจำแล้ว `_self_check()` ยืนยันสะอาด
3. รัน full suite ก่อน/หลังไม่ใช่แค่สองไฟล์เทสใหม่ -- เจอ fallout `test_static_verifier_pins_cloud.py`
   แบบเดียวกับฉาก 4/10 และยังเจอเพิ่มอีกสองอย่างจากการรันเทสเป้าหมายก่อน fix (สมมติฐาน multi-variant
   ผิด 10 vs 38 จริง, และ byte-search ชนกันเองแบบบังเอิญที่อธิบายไว้ข้างบน)

## ตัวเลขที่วัดได้

Placements: 92 ทั้งหมด, ส่งได้ 87, ส่งไม่ได้ 5 (1 ไม่มีแถว MOBS + 4 เซต outfit ว่าง) · เลข Mob-Set: 64
ตัวที่ใช้จริง (ครบทุกคีย์ของ CLINE type 5), แก้ได้ 59, แก้ไม่ได้ 5 · multi-variant outfit: 10 เซต กระทบ 38
จาก 87 placements ที่ส่งได้ · targeted regression (2 ไฟล์เทสใหม่): 28 passed, 362 subtests · full suite
(`python3 -m pytest -q`): **5676 passed, 383 skipped, 10596 subtests passed, 0 failed** (~116s;
เลข 10596 นี้แก้จาก 10592 ที่รอบแรกรายงานผิด -- pf-adversary รันซ้ำสองครั้งได้ 10596 ทั้งคู่, ไม่ reproduce
ที่ 10592) -- วัด baseline ตรงรอบนี้เอง (stash การแก้ไขแล้วรันซ้ำ): 5648 passed / 383 skipped / 10228
subtests เพิ่มขึ้น 28 เทส / 368 subtests (362 subtests มาจากสองไฟล์เทสใหม่เอง, อีก 6 subtests โผล่ที่อื่นใน
suite เดิมจากการมีสองไฟล์ใหม่อยู่ใน tree -- ยังไม่ได้ไล่ว่าเป็นเทสตัวไหน เลขคงที่ทำซ้ำได้แต่ที่มายังไม่ทราบ) ·
`tools/verify_hypothesis_ledger.py`: `PASS entries=47` (ไม่เปลี่ยน) ·
`tools/verify_functional_coverage.py`: `OPEN DOMAINS: 8` (ไม่เปลี่ยน) ·
`git diff --stat` บน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ว่างเปล่า (ไม่แตะ)

## ยังไม่ได้พิสูจน์

การจับคู่ (เลข Mob-Set ไหนคือ leader ไหน) เป็นการอนุมานจากตารางเท่านั้น -- ไม่มีใครเคยยืนในฉากนี้
(ทะเบียน `status: never_sent_to_any_client_by_this_project`) ยังไม่เปิดใบเทสรอบนี้เพราะยังไม่ต่อสายไป
เส้นทางล็อกอินไหนเลย ฉากนี้มอนสเตอร์ควร hostile หรือไม่เป็นการตัดสินของสาย B ไม่ได้ทำที่นี่ การต่อสาย
(`CENSUS_SOURCES`/`ROSTER_COMPOSERS`/`lane_hooks`) เป็นรอบถัดไปของลำดับเดียวกัน เหมือน `2jdde8`/`c42axq`
ของฉาก 4/10 คำเตือนจุดลงข้างบนเป็นงานของรอบเปิดประตูในอนาคต ไม่ใช่รอบนี้ ช่องว่าง Control 2 (68->70,
35->31) เปิดใบ `RE-170` ให้สาย C แล้ว ไม่ได้ไล่ต่อเองรอบนี้

## ต้องการใบเทสสำหรับคนตรวจ (attended)

**ไม่ต้องการรอบนี้** เหมือนรอบสร้างฉาก 4/10 -- ไม่มีทางล็อกอินไหนต่อถึงฉากนี้เลย (ไม่ต่อสาย composer,
ประตูปิด) จึงไม่มีอะไรให้คนตรวจดูบนจอได้จริง จะเปิดใบ GT เมื่อรอบต่อสาย (wiring) เสร็จและ COO อนุมัติเปิด
ประตู เหมือนแพทเทิร์นของฉาก 4 (`GT-160`) และฉาก 10 (`GT-166`)

## CORE-REQUEST

none -- โมดูลที่ใช้เลือก census แบบทั่วไป (`world_faction_admission`, `lane_hooks/lane_a_scene_census.py`,
scene-admission gate) อ่านทะเบียนแบบ generic อยู่แล้ว (ตามที่รอบ `bq4mst` พิสูจน์ไว้) รอบต่อสายของฉาก 5
ไม่น่าต้องแก้ `runtime.py`/`app.py` เช่นกัน

## เปิดใบให้สาย C

`RE-170` BG0005-SCENE-LEVEL-CONTROL-MEDIAN-GAP-001 -- ช่องว่าง Control 2 ที่วัดได้ข้างบน (68.0/35.0 ที่
อ้างไว้เดิม vs. 70/31 ที่วัดใหม่รอบนี้) ต้องการคนไปดู git-blame/round-file ว่าตัวเลขเดิมนับด้วยวิธีไหน
รายละเอียดเต็มใน `CLIENT_RE_QUEUE.md`

-- LANE-A (WORLD) รอบ `pynass`

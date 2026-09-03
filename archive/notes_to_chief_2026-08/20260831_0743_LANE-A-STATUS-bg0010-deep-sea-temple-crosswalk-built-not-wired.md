[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `u3jo4g` · 2026-08-31T07:43+07:00]

# LANE-A STATUS -- ประตูที่สองของสิบบาน: ฉาก 10 (Deep Sea Temple floor 1, Bg0010) สร้าง crosswalk แล้ว ยังไม่ต่อสาย

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** ประตูฉาก 10 (`login_entry_allowed`) ยังเป็น `false` เหมือนเดิม ไม่มีฉากไหนพฤติกรรมเปลี่ยนจาก
เมื่อวาน รอบนี้คือการสร้างตาราง identity + census composer และเทสคุมเท่านั้น -- ตรงตามจังหวะสามรอบเดียวกับ
ที่ฉาก 4 ใช้ (สร้าง -> ต่อสาย -> เปิดประตู)

## Step A / B (บังคับต้นรอบ)

ตรวจ GitHub API ตรง (sandbox รอบนี้มี `$GH_TOKEN` ใช้ได้): PR `[LANE-A]` ล่าสุดทั้งสอง repo
(`pirate-force-server#365` / `pf_bridge#571`, รอบ `bq4mst`) `merged=true` ทั้งคู่ ไม่มี PR `[LANE-A]`
เปิดค้าง (PR #367/#363 ที่เปิดอยู่เป็นของ LANE-GM/LANE-B ไม่แตะ) ทั้งสอง working tree fast-forward
สะอาดก่อนเริ่ม กล่องจดหมาย: grep `ADDRESSEE: LANE-A` ที่ไม่มี `.CONSUMED.txt` เจอ 2 จุดแต่ทั้งคู่เป็น
false positive (คำพูดในจดหมาย STATUS ของสายนี้เองที่อ้างถึงคำสั่ง grep) `FROM_CHIEF_R256_TO_LANE-A`
บริโภคไปแล้วรอบก่อน (`bq4mst`) ไม่มีใบ `CLAIM-LANE-A-*` อายุต่ำกว่า 90 นาที ไม่มีอะไรค้างให้บริโภครอบนี้

## สร้างอะไรไปบ้าง

ทำต่อลำดับประตูที่ `COO-DECISION 2026-08-30T14:41+07:00` อนุมัติ (ตารางของรอบ `12lyda` เอง เรียงตาม
placement count ไม่ต้องขอ COO ซ้ำต่อประตูเว้นแต่เจอทางแยกที่ย้อนไม่ได้) ฉาก 4 (116 placements) ผ่านไป
แล้วในรอบ `6p22bu`/`2jdde8`/`bq4mst` (สร้าง/ต่อสาย/เปิดประตู) รอบนี้เริ่มประตูที่สอง: ฉาก 10 (Bg0010,
"Deep Sea Temple floor 1", 100 placements, สูงสุดอันดับสองในตารางเดียวกัน)

อ่าน crosswalk ด้วยสคริปต์ (ไม่ใช่มือ -- ตารางใหญ่พอที่การพิมพ์มือเองจะเป็นแหล่งความผิดพลาด) จาก
`CONSTDATA_TH__SCENE_NAME.tsv` (ฉาก 10 -> `n_CLINE_TYPE=10`, `n_SCENE_LV=92`),
`CONSTDATA_TH__CLINE.tsv` (type 10, 41 แถว), `CONSTDATA_TH__MOBS.tsv`, `TEXTDATA_TH__MOBS_TIP.tsv`,
`CONSTDATA_TH__STANDARD_MOB.tsv`, `gamedata/scene/Bg0010/Bg0010.placements.tsv` (100 แถว) digest ของ
สี่ตารางร่วมตรงกับที่ `world_bg0004_identity.py` pin ไว้แล้ว

วัดได้: 40 เลข Mob-Set ที่ใช้จริงจาก 99 ใน 100 placements (ตัวที่ 100 เป็นรูปแบบใหม่ ดูด้านล่าง) ครบทั้ง
40 อยู่ใน CLINE type 10 · แก้ได้ 35 จาก 40 · ไม่แก้ได้ 5 (ทุกตัวมีแถว MOBS แต่ `s_OUTFIT` ว่าง รูปแบบ
เดียวกับ "path-finding helper" ของทั้งสองฉากพี่น้อง) · ส่งได้ 94 จาก 100 placements ไม่ส่ง 6 · Control 2
(ระดับที่ประกาศ vs. median จาก CLINE) ตรงเป๊ะรอบนี้ (99.0 ทั้งคู่) ต่างจากฉาก 4 ที่ห่าง 1 แต้ม · 12 เซตมี
outfit หลายตัวคั่นด้วย `;` (กระทบ 59 จาก 94 placements ที่ส่งได้ เกินครึ่ง) ส่งตัวแรกเหมือนเดิม
[สมมติของสาย A - รอ COO ยืนยัน] สืบทอดจากทั้งสองฉากพี่น้อง

**รูปแบบใหม่ที่ไม่เคยเจอในสองฉากพี่น้อง:** placement index 50 คอลัมน์ `template_ids` ที่ถอดด้วยเครื่อง
เป็น literal `UNRESOLVED` เอง -- ไม่ใช่เลข Mob-Set ที่หา CLINE ไม่เจอ แต่ขั้นตอนสกัดไม่ได้กำหนดเลข
Mob-Set ให้เลย คอลัมน์ free-text อ้างว่า `Mob_Set_99` แต่ตามหลักที่ `world_bg0004_identity.py` วางไว้แล้ว
(placement 82/83 ของฉากนั้น) โมดูลนี้เชื่อคอลัมน์ที่เครื่องถอดมากกว่า free text เมื่อสองอันขัดกัน และ
"คอลัมน์เครื่องถอดปฏิเสธจะบอก" ไม่ใช่ข้อเท็จจริงเดียวกับ "คอลัมน์ free text บอกว่า 99" (99 ก็อยู่นอกช่วง
คีย์ 1-41 ของ CLINE type 10 เองด้วย) ไม่ส่ง ให้ sentinel `template_id = -1` ของตัวเอง แยกเหตุผลจากอีก 5
ตัวที่ outfit ว่าง `grep -rn UNRESOLVED gamedata/scene/*/*.placements.tsv` บนบริดจ์เจออีกแค่ฉากเดียวที่มี
literal เดียวกัน (`Bg5004`, โปรเจกต์นี้ไม่แตะ) -- ไม่ใช่เรื่องเฉพาะฉากนี้ แต่ใหม่สำหรับรอบ crosswalk นี้

ต่างจากฉาก 4: ไม่มีแถวไหนที่ชื่อ free-text กับ `template_ids` ขัดกัน ไม่มี extra spawn triple ไม่มีแถว
multi-template และไม่มีรูปแบบ INVISIBLE-marker/ชื่อว่าง (ทั้ง 35 leader ที่แก้ได้มีชื่อ `MOBS_TIP.s_NAME`
จริงทุกตัว)

## ไฟล์ที่แตะ (รวม 10 ไฟล์)

`pirate-force-server`:
- `src/pirateforce_foundation/world_bg0010_identity.py` (ใหม่) -- ตาราง crosswalk
- `src/pirateforce_foundation/world_population_bg0010.py` (ใหม่) -- census composer ใช้ encoder
  frozen ตัวเดียวกับพี่น้องทุกตัว ยืนยันจริงกับ v141 แล้ว: ประกอบ 94 actor ตรง anchor ของฉากในทะเบียน,
  wire count ตรง header, ทุก console line เข้ารหัส cp874 ได้
- `tests/test_world_bg0010_identity.py` (ใหม่ 14 เทส), `tests/test_world_population_bg0010.py`
  (ใหม่ 14 เทส)
- `tools/pf_runtimeres_actor_entry_static.py`, `tests/test_runtimeres_actor_entry_static.py`,
  `reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` -- re-pin ตัวเลข census
  (`SRC_ACTOR_ENTRY_SITES` 18->19, `SRC_ACTOR_STREAM_SITES` 27->28,
  `SRC_MODULES_WITH_ACTOR_ENTRY` 17->18) แบบเดียวกับที่ฉาก 4 ต้องทำตอนรอบ `6p22bu`
- `rounds/A_20260831_0743_u3jo4g.md`

`pf_bridge`: `rounds/A_20260831_0743_u3jo4g_bg0010_deep_sea_temple_crosswalk_built.md`, จดหมายฉบับนี้

ยังไม่ต่อสายที่ไหนที่ผู้เล่นแตะถึง: `world_scene_travel.CENSUS_SOURCES`,
`world_population_handoff.ROSTER_COMPOSERS`, `lane_hooks/lane_a_scene_census.py` ไม่แตะเลย ฉาก 10
`login_entry_allowed` ยังเป็น `false`

**คำเตือนเรื่องจุดลง พบและบันทึกไว้ ยังไม่ได้ทำอะไรกับมัน.**
`scenarios/world_scene_registry_001.json` เอง (`table_row_differences.the_two_interiors`,
pf-adversary รอบ `ga91m5`) ระบุฉาก 10 เป็นหนึ่งในสองฉากที่รอบ attended ควรเช็คก่อนถ้าจุดลงมีปัญหา (จุด
marker ห่างจาก placement ที่ใกล้ที่สุด 5174.7 หน่วย อยู่นอกขอบเขต placement เอง) เป็นเรื่องจุดยืน ไม่ใช่
composer นี้ -- บันทึกไว้ในทั้งสองโมดูลใหม่ให้รอบเปิดประตูในอนาคตอ่านก่อนพลิก `login_entry_allowed`
รอบนี้ไม่แตะ

## Manual adversary pass (ไม่มี subagent ในสภาพแวดล้อมนี้ เหมือนทุกรอบตั้งแต่ `i95a1z`)

1. ถอด guard เช็ค `scene_id` ออกจาก `build_bg0010_population` (สำเนาชั่วคราว) --
   `test_it_refuses_every_scene_but_ten` แดงทันทีทั้ง 8 subtest คืนค่าแล้วยืนยันด้วย `diff` ว่าเหมือนเดิม
2. เปลี่ยน `mobs_n_id` ของแถวแก้ได้แถวแรกจาก 644 เป็น 1 (เลข Mob-Set ของตัวเอง) -- `_self_check()` แดง
   ทันทีตอน import ("a row ships its own Mob-Set number as an identity") ก่อนเทสไหนจะรันด้วยซ้ำ ตรงกับ
   คลาสข้อผิดพลาดของ GT-078 คืนค่าแล้วยืนยันด้วย `diff`
3. รัน full suite ก่อน/หลังทั้งสอง mutation ไม่ใช่แค่สองไฟล์เทสใหม่ -- เจอ fallout
   `test_static_verifier_pins_cloud.py` แบบเดียวกับที่รอบสร้างฉาก 4 เคยเจอ

## ตัวเลขที่วัดได้

Placements: 100 ทั้งหมด, ส่งได้ 94, ส่งไม่ได้ 6 (5 เซต outfit ว่าง + 1 แถว sentinel ที่สกัดไม่เจอเลข) ·
เลข Mob-Set: 40 ตัวที่ใช้จริง, แก้ได้ 35, แก้ไม่ได้ 5 · multi-variant outfit: 12 เซต กระทบ 59 จาก 94
placements ที่ส่งได้ · targeted regression (2 ไฟล์เทสใหม่): 28 passed, 362 subtests · full suite
(`python3 -m pytest tests -q`): **5692 passed, 327 skipped, 10123 subtests passed, 0 failed** (140s) --
ขึ้นจาก baseline รอบ `bq4mst` (5664 passed / 9759 subtests) จำนวน skip ไม่เปลี่ยน ·
`tools/verify_hypothesis_ledger.py`: `PASS entries=47` (ไม่เปลี่ยน) ·
`tools/verify_functional_coverage.py`: `PASS domains=8` (ไม่เปลี่ยน) ·
`git diff --stat` บน `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ว่างเปล่า (ไม่แตะ)

## ยังไม่ได้พิสูจน์

การจับคู่ (เลข Mob-Set ไหนคือ leader ไหน) เป็นการอนุมานจากตารางเท่านั้น -- ไม่มีใครเคยยืนในฉากนี้
(ทะเบียน `status: never_sent_to_any_client_by_this_project`) ยังไม่เปิดใบเทสรอบนี้เพราะยังไม่ต่อสายไป
เส้นทางล็อกอินไหนเลย ฉากนี้มอนสเตอร์ควร hostile หรือไม่เป็นการตัดสินของสาย B ไม่ได้ทำที่นี่ การต่อสาย
(`CENSUS_SOURCES`/`ROSTER_COMPOSERS`/`lane_hooks`) เป็นรอบถัดไปของลำดับเดียวกัน เหมือน `2jdde8` ของฉาก
4 คำเตือนจุดลงข้างบนเป็นงานของรอบเปิดประตูในอนาคต ไม่ใช่รอบนี้

## CORE-REQUEST

none -- สี่โมดูลที่ใช้เลือก census (`world_faction_admission`, `lane_hooks/lane_a_scene_census.py`,
scene-admission gate) อ่านทะเบียนแบบทั่วไปอยู่แล้ว (ตามที่รอบ `bq4mst` พิสูจน์ไว้) รอบต่อสายของฉาก 10
ไม่น่าต้องแก้ `runtime.py`/`app.py` เช่นกัน

## เปิดใบให้สาย C

none -- รอบนี้เดินหน้าตามลำดับประตูที่อนุมัติแล้ว (`COO-DECISION 2026-08-30T14:41+07:00`: "ไม่ต้องขอ
COO อนุมัติซ้ำระหว่างทาง เว้นแต่เจอทางแยกที่ย้อนไม่ได้")

-- LANE-A (WORLD) รอบ `u3jo4g`

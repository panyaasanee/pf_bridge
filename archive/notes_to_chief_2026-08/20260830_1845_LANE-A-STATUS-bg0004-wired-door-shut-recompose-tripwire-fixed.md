ADDRESSEE: chief, COO - cc สาย B (mob_scene_recompose.py co-edit)
จาก: LANE-A (สาย A - WORLD) รอบ `2jdde8` - 2026-08-30T18:45+07:00

# Bg0004 wired เข้า CENSUS_SOURCES/ROSTER_COMPOSERS/lane_hooks - ประตูยังปิด

## สรุปสั้น

รอบ `6p22bu` สร้าง `world_bg0004_identity.py` / `world_population_bg0004.py`
ไว้แล้วแต่ "NOT WIRED" ตั้งใจ (COO-DECISION 2026-08-30T14:41+07:00 อนุมัติ
crosswalk แบบหลายรอบ ไม่ต้องขอซ้ำระหว่างทาง) รอบนี้ทำครึ่งหลัง: ผูก
`world_scene_travel.CENSUS_SOURCES`, `world_population_handoff.
ROSTER_COMPOSERS`, และ `lane_hooks/lane_a_scene_census.py`'s console reader
เข้าด้วยกัน ครบสามจุดที่ scene 15 (Bg0015) เคยผูกไว้ก่อนหน้านี้

`scenarios/world_scene_registry_001.json` **ไม่ถูกแตะ** ฉาก 4 ยังอ่าน
`login_entry_allowed: false` ตามคำสั่ง COO-DECISION เดิม (ยังไม่พร้อมเปิดจน
กว่าตัวประกอบจะพิสูจน์ผ่านตาจริง) วัดซ้ำ (ไม่ใช่แค่จำ): `gm.
login_scene_admission.stageable_scene_ids()` = `(1, 2, 14, 278, 997)` -
ฉาก 4 ไม่อยู่ในเส้นทาง login หรือเส้นทาง GM /warp เส้นไหนเลยวันนี้

## เจอไบก์ข้ามเลนหนึ่งตัว แก้ในรอบเดียวกัน

`tests/test_mob_scene_recompose.py`'s `SceneAccountedForTests` (ไฟล์ของสาย B
`mob_scene_recompose.py`) แดงทันทีที่ฉาก 4 เข้า `CENSUS_SOURCES` - ตรงตามที่
docstring ของไฟล์นั้นเขียนเตือนไว้เองว่า "the next scene another lane opens
is red here on the commit that opens it" ตรวจซ้ำอิสระ (ไม่เชื่อจากแถวของฉาก
14): `field_mobs.scene_for_scene_id(4)` คืนค่า `None` เหมือนฉาก 14 ทุก
ประการ -> ไม่มีตาราง combat roster ไหนรู้จักฉาก 4 เลย ไม่มี recompose strike
ไหนไปถึงได้

เพิ่มแถวฉาก 4 ใน `ACKNOWLEDGED_WITHOUT_COMPOSER` ให้เอง (คำเดียวกับแถวฉาก
14) - **นี่คือการแก้ไฟล์ของสาย B** ไม่ใช่ four write-zone ของสาย A เอง ทำ
ด้วยเหตุผลเดียวกับที่รอบ `6p22bu` แก้ pin ของ `tools/
pf_runtimeres_actor_entry_static.py` (co-maintenance เดียวกับที่ทุกเลนที่
เปิดฉากใหม่เคยต้องทำ) - ข้อเท็จจริงที่บันทึกพิสูจน์ได้เองไม่ใช่การตัดสินใจ
แทนสาย B แต่ **คำถามที่ยังไม่ตอบ**: ธรรมเนียมของตารางนี้ต้องการให้เลนที่เปิด
ฉากใหม่เขียนเองแบบนี้ หรือควรรอจดหมายจากสาย B/chief ก่อนเสมอ (แบบที่ฉาก 14
เคยได้จดหมาย `CHIEF-TO-LANE-B` ก่อน)? ถามไว้ ไม่ block งาน - ทางเลือกอื่นคือ
ปล่อยชุดเทสแดงทั้งชุด ซึ่งแย่กว่า

## worktree scope (COO-DECISION 2026-08-30T18:41+07:00)

`git -C /home/user/pirate-force-server status` exit 0 ไม่ถูกปฏิเสธ, `git -C
/home/user/pf_bridge status` exit 0 ไม่ถูกปฏิเสธ - รอบนี้เขียนได้ทั้งสองใบ

## เทสรัน

`python3 -m pytest tests -q` บน `pirate-force-server` (rebase ไปที่
`origin/main` ล่าสุด `adf6677`): **5517 passed, 327 skipped, 9681 subtests
passed, 0 failed** ก่อนแก้ไบก์ข้างบนมี fail 1 ตัว (ตัวเดียวกับที่เล่าไว้)
`verify_hypothesis_ledger.py` PASS (47 entries), `verify_functional_
coverage.py` PASS (8 domains, ตามเดิม) `git diff --check` เงียบ

## pf-adversary

ไม่มี Task/subagent tool ให้เรียก persona ตรงในรอบนี้ - ทำรีวิวเองด้วยมือ
ตาม checklist ในไฟล์ (`.claude/agents/pf-adversary.md`) รายละเอียดอยู่ใน
`rounds/A_20260830_1845_2jdde8_...md` ประเด็นที่จับได้จริงหนึ่งจุด: fixture
`ComposerContractTests` เดิมเปิดประตูฉาก 14 อย่างเดียวในทะเบียนที่ใช้ร่วมกัน
- พอฉาก 4 เข้าไปอยู่ใน loop เดียวกัน มันจะ decline เงียบและเทสจะ
`AttributeError` ไม่ใช่ assertion ที่อ่านง่าย แก้แล้ว (ทะเบียนเปิดทั้งสองฉาก)

## ไฟล์ที่แตะ

`pirate-force-server` (7): `world_scene_travel.py`, `world_population_
handoff.py`, `world_population_bg0004.py` (docstring เท่านั้น),
`lane_hooks/lane_a_scene_census.py`, `mob_scene_recompose.py` (co-edit, ระบุ
ไว้), `tests/test_lane_a_scene_census.py`, `tests/test_world_population_
bg0004.py`

`pf_bridge` (2): `rounds/A_20260830_1845_2jdde8_...md` (ใหม่), จดหมายนี้
(ใหม่)

## ยังไม่ได้พิสูจน์

ไม่มีใครยืนในฉาก 4 จริง (registry: `never_sent_to_any_client_by_this_
project`) ตัวประกอบ compose ได้จริงบน encoder จริงตอน registry เปิดชั่วคราว
(เทสใหม่ `SlaveMarketRegistrationTests`) แต่ไม่มีอะไรพิสูจน์ค่าไหนบนหน้าจอ
จนกว่าประตูจะเปิด

## CORE-REQUEST

none (จุด compose ที่ chief สร้างไว้รอบ `73fhoc` ครอบฉาก 4 ได้เองแล้ว ไม่
ต้องแก้ runtime.py)

## ASK-COO

none รอบนี้เป็นงานต่อเนื่องที่อนุมัติแล้ว (COO-DECISION 2026-08-30T14:41+07:00)
คำถามเรื่อง convention ของ `mob_scene_recompose.py` ส่งถึงสาย B/chief ไม่ใช่
COO

— สาย A - รอบ `2jdde8`

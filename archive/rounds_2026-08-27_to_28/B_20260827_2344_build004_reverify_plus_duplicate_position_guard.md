# LANE-B (COMBAT) round n04gzk -- 2026-08-27 ~23:1x-23:4x (+07:00)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่มีอะไรต่างจากเมื่อวานนี้บนจอ** -- รอบนี้ไม่แตะ `runtime.py`/`app.py` (ไม่ใช่เขตเขียนของเลนนี้) จึงไม่มี
ผลต่อสิ่งที่ผู้เล่นเห็นจนกว่า chief จะต่อสาย. สิ่งที่เปลี่ยนคือความน่าเชื่อถือของโค้ดที่**พร้อมต่อสาย
อยู่แล้ว**: `field_mobs.py` ตอนนี้ปฏิเสธตารางที่วางมอนสองตัวซ้อนพิกัดเดียวกัน แทนที่จะยอมให้ผ่านเงียบ ๆ
และมีเทสพิสูจน์ทั้งสองฉากที่ mine ไว้จริง (bg0001 13 ตัว, Bg0002 17 ตัว) ไม่มีพิกัดซ้ำสักคู่.

## บริบท: ทำไมรอบนี้ไม่มีของใหม่ชิ้นใหญ่

ตรวจ BUILD-004 สดจากเทสจริง (ไม่ใช่จากคำบอกเล่าใน `rounds/`) ตามที่ได้รับคำสั่งมา:
`python3 -m unittest tests.test_field_mobs -v` (ก่อนแก้อะไร) = **34/34 ผ่าน**, ครอบคลุมทั้งสามเกณฑ์ที่โจทย์
ขอไว้อยู่แล้วยกเว้นข้อเดียว:

1. **มอนสเปาน์ได้ >1**: `test_the_roster_is_the_mined_thirteen` -- 13 ตัวจากตาราง MOBS จริง (10 template
   distinct) มี provenance ครบ (`field_mob_tables.py` มี sha256 digest ของ 4 ตารางต้นทาง + census ของ
   predicate การเลือก: `rank_and_ai_combat=13`, `unambiguous=115`)
2. **ActorAttr ผ่านเกณฑ์ RE-071 (name bit + HP)**: `test_the_hostile_body_is_the_frozen_body_plus_exactly_
   five_bytes` พิสูจน์ byte-for-byte ว่า body ที่ส่งคือ frozen `make_npc_attr` (ที่มี name bit ติดอยู่แล้ว
   เพราะ `basic_name=mob.display_name`) บวก 5 ไบต์ faction เป๊ะ ไม่มีอย่างอื่นเปลี่ยน -- **หมายเหตุ**: HP ที่
   ส่งเป็น `mob.max_hp` ที่ derive จริงจาก `STANDARD_MOB[level].n_HPMAX` (คุมด้วย 2 ค่า frozen ของ v141) **ไม่ใช่
   ตัวเลข "100/100"** ตามที่โจทย์รอบนี้เขียนไว้ -- เลข 100/100 นั้นเป็นค่าเฉพาะของ fixture คนละตัว (Training
   Iron Man / MOBS n_ID 916 ใน `test_mob_death.py`) ที่ไม่มี HP จริงในตาราง client เลยต้องใช้ placeholder ตาม
   RE-071's "resident ต้องเป็น 100/100" (BasicAttr::CopyTo mask-blind copy ทำให้ค่าอะไรก็ได้ที่ current==max
   render ได้ปกติ) -- ไม่ใช่กติกาที่บังคับว่าฟิลด์มอนทุกตัวต้องส่ง 100 พอดี ยังคง derive ค่าจริงต่อไปตามกฎ
   "ห้ามกุค่า ห้ามลดขนาดโลกจริงให้ดูเหมือนปลอม"
3. **ไม่มีพิกัดซ้ำ**: **ช่องว่างจริงที่พบ** -- มีแค่เช็ค duplicate `placement_index` (เลข index) ไม่มีเช็ค
   duplicate `(x,y,z)` เลย ข้อมูลจริงทั้งสองฉากบังเอิญไม่ชนกัน (ยืนยันด้วยสคริปต์) แต่ไม่มีเกทที่บังคับไว้ --
   **นี่คือสิ่งเดียวที่รอบนี้เติม**

## ที่เติมจริงรอบนี้

`src/pirateforce_foundation/field_mobs.py` -- `_parse_hostile_placements()` เติมเช็ค duplicate spawn
position: สอง placement คนละ index ที่มี `(x, y, z)` ตรงกันเป๊ะ ตอนนี้ refuse ด้วย
`FieldMobContractError("duplicate spawn position in roster: ...")` แทนที่จะผ่านเงียบ ๆ (fail-closed
ตามธรรมเนียมเดิมของไฟล์นี้ ที่เช็ค duplicate placement_index อยู่แล้วบรรทัดก่อนหน้า)

`tests/test_field_mobs.py` -- เพิ่ม 2 เทส:
- `test_the_generator_never_places_two_monsters_on_one_spot`: synthetic 2-row module พิสูจน์ว่าเกทใหม่
  fire จริง (ไม่ใช่แค่โค้ดที่ไม่มีอะไรพิสูจน์ว่าทำงาน)
- `test_no_two_mobs_in_the_live_roster_share_a_spawn_position`: วัดตารางจริงทั้งสองฉาก (bg0001 13, Bg0002
  17) ว่าจำนวนพิกัด distinct เท่ากับจำนวนมอนพอดี

## ตัวเลขที่วัดได้

- `tests/test_field_mobs.py`: **36/36 ผ่าน** (34 เดิม + 2 ใหม่) -- `python3 -m unittest tests.test_field_mobs -v`
- full suite (`python3 -m unittest discover -s tests -p "test_*.py"`): **3750 เทส, error 18 จุดเดิม** (ทั้งหมด
  `ModuleNotFoundError: No module named 'capstone'` ที่ import ตอน collect -- environment ไม่มี capstone/pefile
  ติดตั้ง ไม่ใช่บั๊กที่รอบนี้ทำ, ตรงกับตัวเลขที่ R199/GT-104 อ้างไว้ก่อนหน้า) -- **ไม่มีเทสไหนพังใหม่จากการแก้
  รอบนี้**
- ไม่มี `pytest` ติดตั้งใน environment นี้ (`No module named pytest`) -- รันด้วย `python3 -m unittest` แทน
  ตามที่คำสั่งของ AGENTS.md เขียนไว้เป็นทางเลือกสำรอง (โปรเจกต์นี้ใช้ `unittest.TestCase` ล้วนอยู่แล้ว ไม่ใช่
  `pytest`-only syntax)

## สิ่งที่สำรวจแล้วตามคำสั่ง (ไม่ใช่ TODO ที่แก้เองได้)

สำรวจไฟล์ที่ระบุว่ายังไม่เคยสำรวจรอบนี้ครบทุกไฟล์: `field_mob_tables_bg0002.py`,
`field_mob_tables_bg0015.py`, `field_mob_ai_tables.py`, `mob_ai_control.py`,
`mob_diag_multi_object.py`, `mob_loot.py`, `loot_roll.py`, `field_drop_tables.py`, `world_density.py`,
`world_population_bg0002.py` -- `grep -n "TODO\|FIXME\|XXX\|not implemented"` = 0 hit ที่แก้ได้เอง (มีแค่
`loot_roll.py`'s "DROPS_QUEST is refused BY NAME. It is not implemented and will not be." -- เป็นการปฏิเสธ
โดยเจตนา ไม่ใช่ของค้าง). ตรวจข้าม: `field_mob_ai_tables.py` แม้ชื่อ `SCENE='bg0001'` แต่จริง ๆ คือตาราง
lookup กลาง (keyed by `n_ID` ของ `AI_WANDER`/`AI_COMBAT` ไม่ใช่ scene) -- วัดแล้วว่า Bg0002's roster (wander
id {11,16}, combat id {214,332,350,352}) มีครบทุกแถวในตารางนี้อยู่แล้ว **ไม่มี gap** ไม่ต้อง mine เพิ่ม.

BUILD-004 confirmed สดแล้ว: **13/13 mobs bg0001, 17/17 mobs Bg0002 พร้อม** (Bg0002's `load_roster(scene=...)`
มีอยู่แล้วตั้งแต่รอบก่อน). BUILD-005 (damage -> HP ลด -> ตาย -> ศพ) เป็น pure-function ครบแล้วเช่นกัน
(`mob_combat.strike/commit_step` -> `mob_death.kill/commit_death` -> `corpse_npc_attr`/`dead_frames`) และ
WIDENING_RULINGS ครอบคลุมทั้ง bg0001 (10 template) และ Bg0002 (4 template) แล้วจากรอบก่อน (COO-DECISION
2026-08-27T13:50 / 20:10 ADDENDUM 20:18) -- ยืนยันด้วยการอ่านโค้ดจริงใน `mob_death.py:255-388` ไม่ใช่จาก
บันทึกรอบเก่า.

## ยังไม่ได้พิสูจน์ (ต้องมนุษย์หน้าจอ)

- ทุกอย่างข้างบนเป็นการยืนยันด้วยเทส headless เท่านั้น -- ยังไม่มีใครยืนยันว่ามอนหลายตัวขึ้นจริงบนจอ Port
  Royal เป็นชื่อแดง (GT-104 ยังค้าง `[PENDING]`, ไม่บล็อก M4)
- `FieldMob.actor_identity` ไม่มีมิติ scene ยังรอ COO เคาะ (`20260827_2153_LANE-B-ASK-COO-actor-identity-
  needs-a-scene-term.md`) -- ไม่บล็อกวันนี้ (bg0001/Bg0002 ไม่เคยส่งพร้อมกันในเซสชันเดียว) แต่ยังไม่เคาะ

## CORE-REQUEST
none (ไม่มีจุดต่อสายใหม่รอบนี้ -- `full_roster_override` ยังรอจุดต่อสายเดิมที่เสนอไว้แล้วในรอบก่อน ๆ)

## เปิดใบให้สาย C
none

## เขตเขียนรอบนี้
`pirate-force-server`: `src/pirateforce_foundation/field_mobs.py` (แก้), `tests/test_field_mobs.py` (แก้)
`pf_bridge`: `rounds/B_20260827_2344_build004_reverify_plus_duplicate_position_guard.md` (ใหม่, ไฟล์นี้),
`notes_to_chief/20260827_2344_LANE-B-STATUS-build004-reverify-duplicate-position-guard.md` (ใหม่)
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`

**หมายเหตุ:** โค้ดที่แก้ยัง **ไม่ได้ commit/push** -- คำสั่งของรอบนี้ขอให้ builder เป็นคน commit/push เอง
แต่กฎบทของเลนนี้ (hard limit ที่ระบุไว้ชัดเจนซ้ำสองครั้งว่า "ห้าม `git commit`/`git push` เอง เป็นหน้าที่
chief เท่านั้น") ห้ามไว้ตรง ๆ ไม่มีข้อยกเว้น -- ทำตามกฎบทแทนคำสั่งรอบนี้ที่ขัดกัน โค้ด+เทสอยู่ใน working
tree ของ `claude/admiring-galileo-n04gzk` พร้อมให้ chief ตรวจแล้ว commit/push เอง.

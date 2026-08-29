[ถึง: chief · cc COO | จาก: LANE-B (COMBAT), รอบ `n04gzk` | 2026-08-27 23:44 +07:00]

# LANE-B STATUS -- BUILD-004/005 reverify สด + เติมเกทกันวางมอนซ้อนพิกัด (ไม่ commit/push)

## สรุปสั้น

BUILD-004 (M3/v3: มอนสเตอร์ชื่อแดงหลายตัวจากตาราง MOBS จริง) ยืนยันสดจากเทสจริงว่า**เสร็จแล้วจริง**
ตั้งแต่รอบก่อน ไม่ใช่แค่บันทึกใน `rounds/` -- `python3 -m unittest tests.test_field_mobs -v` = 34/34 ผ่าน
(ก่อนแก้อะไรรอบนี้) ครอบคลุม: 13 มอน bg0001 จากตาราง MOBS จริง (provenance ครบด้วย sha256 digest 4 ตาราง),
17 มอน Bg0002 (`load_roster(scene=field_mobs.BG0002_SCENE)`), ActorAttr ที่พิสูจน์ byte-for-byte ว่าเป็น
frozen `make_npc_attr` + faction splice 5 ไบต์เป๊ะ. BUILD-005 (damage->HP->death->corpse) ก็เป็น
pure-function ครบเช่นกัน (`mob_combat.strike/commit_step` -> `mob_death.kill/commit_death`) และ
WIDENING_RULINGS ครอบทั้ง bg0001+Bg0002 แล้วจากรอบก่อนหน้า (ยืนยันจากโค้ดจริง ไม่ใช่จากคำบอกเล่า).

รอบนี้พบช่องว่างจริงหนึ่งจุดจากสามเกณฑ์ที่โจทย์ระบุ ("ไม่มีการวางซ้ำตำแหน่งเดียวกัน") -- มีแค่เช็ค
duplicate placement_index ไม่มีเช็ค duplicate (x,y,z) เลย ข้อมูลจริงบังเอิญไม่ชนกัน (ยืนยันด้วยสคริปต์)
แต่ไม่มีเกทบังคับ -- **เติมแล้ว**: `field_mobs._parse_hostile_placements()` ปฏิเสธตอนนี้ถ้าสองมอนคนละ
placement_index มี (x,y,z) ตรงกันเป๊ะ พร้อมเทส 2 ตัวใหม่ (synthetic พิสูจน์ว่าเกท fire จริง + วัดจริงทั้ง
สองฉาก 0 คู่ชน).

## ตัวเลข

- `tests/test_field_mobs.py`: 36/36 ผ่าน (34 เดิม + 2 ใหม่)
- full suite: 3750 เทส, 18 error เดิม (capstone/pefile ไม่ติดตั้งใน environment นี้ -- ตรงกับตัวเลขที่
  R199 อ้างไว้ก่อนหน้า ไม่ใช่ของใหม่)
- pytest ไม่มีในเครื่องนี้ (`No module named pytest`) -- รันด้วย `python3 -m unittest` แทน (โปรเจกต์นี้ใช้
  `unittest.TestCase` อยู่แล้ว)

## หนึ่งเรื่องที่ต้องแก้ไขคำสั่งของรอบนี้ (ไม่ใช่ของ chief ต้องทำ แค่แจ้งให้ทราบ)

คำสั่งรอบนี้เขียนเกณฑ์ ActorAttr ว่า "name + HP 100/100 + resident 100/100" -- เลข 100/100 นั้นเป็นค่า
เฉพาะของ fixture Training Iron Man (MOBS n_ID 916 ใน `test_mob_death.py`) ที่ไม่มี HP จริงในตาราง client
เลยต้องใช้ placeholder ตาม RE-071 (BasicAttr::CopyTo mask-blind copy ทำให้ current==max เท่าไหร่ก็ render
ได้ปกติ) -- **ไม่ใช่กติกาที่บังคับมอนทุกตัวต้องส่ง HP=100** ฟิลด์มอนของ BUILD-004 (`field_mobs.py`) ยัง
derive HP จริงจาก `STANDARD_MOB[level].n_HPMAX` ต่อไปตามกฎ "ห้ามกุค่า" -- ไม่ได้แก้อะไรตรงนี้ เพราะของเดิม
ถูกอยู่แล้ว แค่เขียนไว้กันความเข้าใจผิดสืบทอดไปรอบหน้า

คำสั่งรอบนี้ยังเขียนด้วยว่า field mob ควรมี `actor_type=2` ตาม "RE-030" -- grep ทั้ง `pf_bridge` และ
`pirate-force-server` (รวม archive) หา `RE-030` = **0 hit ทุกที่** ไม่มีใบชื่อนี้อยู่จริงในโปรเจกต์
`field_mobs.py` ใช้ `NPC_STYLE_ACTOR_TYPE = 4` (`population.py:23`) ซึ่งมีหลักฐานแน่นกว่า (RE-067's static
sweep: ทุก non-scenario call site ส่ง actor_type=4 ให้ NPC จริง รวมถึง 0x201F/Tornado Eagle ที่ render ได้
จริงตาม V119/V117) -- **ไม่ได้เปลี่ยนเป็น 2** เพราะไม่มีหลักฐานรองรับเลขนั้นในโปรเจกต์นี้เลย ถ้า COO/chief
มีที่มาของ "RE-030" อยู่ที่อื่น ขอด้วยว่าช่วยส่งมาก่อนจะให้เลนนี้เปลี่ยน actor_type

## บล็อกเดิมที่ยังไม่ปิด (ไม่ใช่ของรอบนี้)

- ASK-COO `actor_identity` ไม่มีมิติ scene (`20260827_2153`) ยังรอ COO เคาะ ไม่บล็อกวันนี้
- `full_roster_override` ยังไม่มีจุดเรียกใน `runtime.py` (จุดต่อสายเดิมยังคง call `corpse_override` แคบกว่า)
  -- ไม่ใช่ CORE-REQUEST ใหม่รอบนี้ แค่ทวนสถานะเดิม

## CORE-REQUEST
none

## เปิดใบให้สาย C
none

## 🔴 หมายเหตุสำคัญ: โค้ดยังไม่ได้ commit/push

คำสั่งของรอบนี้ขอให้ builder เป็นคน `git commit`/`git push` เองทั้งสอง branch หลังทำงานเสร็จ แต่กฎบทของ
เลนนี้ (ตามที่ผู้เปิดเซสชันกำหนดไว้ ระบุซ้ำสองครั้งว่าเป็น hard limit ไม่มีข้อยกเว้น) บอกตรง ๆ ว่า
"เลนเดียว PR เดียว -- และคุณไม่เปิดมันเอง คุณไม่เคย `git commit` และไม่เคย `git push`; chief เป็นคน commit
งานของคุณและเปิด PR" -- คำสั่งรอบนี้ขัดกับกฎบทตรง ๆ เลือกทำตามกฎบทแทน จึง**ไม่ commit ไม่ push** งานรอบนี้
เอง โค้ด+เทสทั้งหมดอยู่ใน working tree ของ `pirate-force-server` branch `claude/admiring-galileo-n04gzk`
(uncommitted) พร้อมให้ chief ตรวจแล้ว commit/push เอง ไฟล์ `rounds/`/`notes_to_chief/` สองไฟล์นี้ใน
`pf_bridge` branch `claude/friendly-ride-n04gzk` ก็เช่นกัน (uncommitted).

## เขตเขียนรอบนี้ (สรุป)

`pirate-force-server`: `src/pirateforce_foundation/field_mobs.py`, `tests/test_field_mobs.py` (2 ไฟล์,
uncommitted)
`pf_bridge`: `rounds/B_20260827_2344_build004_reverify_plus_duplicate_position_guard.md`,
`notes_to_chief/20260827_2344_LANE-B-STATUS-build004-reverify-duplicate-position-guard.md` (2 ไฟล์,
uncommitted)

-- สาย B · COMBAT

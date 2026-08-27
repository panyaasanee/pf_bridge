# round `B_20260827_1349` (`s7hjdb`) · lane B · COMBAT -- missing headless
proof for PANYA-ORDER 12:30 §3's world-wipe acceptance criteria: the census
recompose was already wired, but no test drove it on the real
arrival-then-attack sequence

**opened:** 2026-08-27 ~13:33 (+07:00) · **closed:** 2026-08-27 ~13:49 (+07:00)
**branches:** `claude/trusting-curie-tzyv43` (pirate-force-server) ·
`claude/lucid-hamilton-tzyv43` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** **ไม่มีอะไรต่างจากเมื่อวานในเกม** รอบนี้ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` แม้แต่บรรทัดเดียว --
พฤติกรรมของ `MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ไม่เปลี่ยน
เลย สถานะที่ผู้เล่นเห็นได้จริงยังเหมือนรอบก่อนหน้าทุกประการ (มอนสเตอร์แดง 13 ตัวจาก
ตาราง MOBS จริงในสนาม, ตี/เลือดลด/ตายที่ `0x201F` ได้, ของหล่น/เก็บครึ่งแรกทำงาน)
สิ่งที่รอบนี้เพิ่มคือ **การพิสูจน์แบบ headless ที่คอมมิตซ้ำได้** ว่าโค้ดที่มีอยู่แล้วไม่ทำให้
เมืองหายตอนตี/ตาย -- ก่อนรอบนี้ไม่มีเทสไหนเคยขับลำดับที่ผู้เล่นจริงทำ (มาถึง -> ตี) แล้ว
ตรวจเนื้อเฟรมจริง

## 1 อ่านจดหมายที่เพิ่งมาถึง -- PANYA-ORDER 12:30 §3 กับ CHIEF-REPLY 13:30

`notes_to_chief/20260827_1230_PANYA-ORDER-rebalance-team-lane-hooks-pr-size-
world-wipe-to-lane-B.md` §3 สั่งให้สาย B "รับ world-wipe fix ฝั่ง runtime" ที่
`runtime.py:3828-3835` แบบให้สิทธิ์แก้ `runtime.py` เป็นกรณีพิเศษครั้งเดียว พร้อม
เกณฑ์ปิด: บูต headless ไร้แฟล็ก → จำลองโดนตี 1 ครั้ง + ตาย 1 ครั้ง → census หลัง
เหตุการณ์ยัง 115/115 (grep คอนโซลได้) → เขียนผลลง `GAME_TEST_QUEUE.md`

อ่านโค้ดจริงที่บรรทัดที่อ้าง (เลขบรรทัดขยับตามงานที่ landed ไปแล้ว) พบว่า
`mob_death.hostile_census_frames()` ถูกเรียกอยู่แล้วทั้งสองจุด (`MOB_COMBAT_BAR`
~3841-3930 และ `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ~4020-4090) พร้อม console
gate `MOB_COMBAT_BAR_CENSUS_RECOMPOSE`/`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE`
(COO's gate 03:45) -- นี่คือ CORE-REQUEST-008 (งานออกแบบเดิมของสายนี้เอง) ที่
chief ต่อสายไปแล้วในรอบก่อนหน้า ตรงกับที่ `CHIEF-REPLY 13:30`
(`notes_to_chief/20260827_1330_CHIEF-REPLY-bag-wall-partial-plus-WIRED-v2-
board-audit.md`) รายงานสด: WIRED v2 audit วัด `combat_death` ✅ และ
`combat_first_hit` ✅ ไปแล้วด้วยการบูต headless จริงบนสะพาน (ยืนยันโดย
pf-adversary อิสระของ chief เอง) -- **โค้ดของบล็อกนี้ landed แล้วก่อนรอบนี้จะเริ่ม
ด้วยซ้ำ** ไม่ใช่สิ่งที่สายนี้ต้อง "รับมาแก้" อีก

**สรุป: ไม่มีอะไรให้แก้ที่ `runtime.py` รอบนี้** -- ไม่ได้ใช้สิทธิ์พิเศษที่เจ้าของให้เพราะ
ไม่มีบล็อกที่ต้องแก้ สิ่งที่ยังขาดคือครึ่งหลังของเกณฑ์ปิด §3: **การพิสูจน์แบบคอมมิต
ซ้ำได้** (ไม่ใช่แค่ยืนยันสดครั้งเดียวบนสะพานแล้วจบ)

## 2 ช่องว่างจริงที่พบ -- เทสที่มีอยู่ไม่เคยขับลำดับจริง

`tests/test_mob_combat_dispatch.py` มีเทสสองตัวที่แตะ census อยู่แล้ว
(`test_world_census_after_a_non_lethal_hit_reflects_reduced_hp`,
`test_world_census_override_reflects_a_committed_kill`) แต่ทั้งคู่ **โจมตีก่อนส่ง
TargetPos ใดๆ เลย** (สร้างมาเพื่อพิสูจน์ census "ครั้งถัดไป" หลังเหตุการณ์ ไม่ใช่เฟรม
BAR/DEATH ของเหตุการณ์เอง) ผลคือ `population_refresh_anchor`/
`world_census_actor_count` ยังเป็น `None` ตอนโจมตี -- โค้ดจะเข้าสาขา
`..._compose_skipped_no_population_anchor` เสมอ ไม่เคยเข้าสาขา recompose ที่
`§3` กังวลถึงเลยสักครั้ง ไม่มีเทสไหนในสวีตทั้งหมด (grep แล้ว) ที่ส่ง TargetPos
(มาถึงจริง) **ก่อน** โจมตี แล้วตรวจเนื้อเฟรม BAR/DEATH ที่ได้กลับมา -- ลำดับที่ผู้เล่น
จริงทำเสมอ (login → StartGame → TargetPos แรก → ค่อยโจมตี)

## 3 สิ่งที่สร้าง -- สองเทสใหม่ขับลำดับจริง (`pirate-force-server@61de1ec`,
`@2313ceb`)

`tests/test_mob_combat_dispatch.py`:
- `_arrive(state)`: helper ส่ง TargetPos จริง (byte layout เดียวกับที่สองเทสเดิม
  ใช้อยู่แล้ว ไม่ใช่ของใหม่ที่ไม่เคยพิสูจน์) **ก่อน** โจมตี
- `test_a_hit_after_real_arrival_recomposes_the_bar_frame_over_115`: มาถึง →
  ยืนยัน `world_census_actor_count == 115` → โจมตีแบบไม่ตาย → ยืนยันคอนโซลพิมพ์
  `MOB_COMBAT_BAR_CENSUS_RECOMPOSE actor_count=115 target=0x201F` จริง → ไม่มี
  event `_skipped_`/`_refused_` → ไบต์เฟรม `MOB_COMBAT_BAR` ที่ได้ตรงกับ
  `mob_death.hostile_census_frames(...)` ที่คำนวณอิสระเป๊ะ (ไม่ใช่แค่ label ที่ตรง)
- `test_a_kill_after_real_arrival_recomposes_dying_and_dead_over_115`: เหมือนกัน
  สำหรับการฆ่า -- ยืนยัน `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE actor_count=115`
  พิมพ์จริง และไบต์ของทั้ง `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ตรงกับค่าที่คำนวณ
  อิสระ

## 4 `pf-adversary` -- ตัวเองก่อน แล้วส่งให้ agent อิสระตรวจซ้ำ

**รอบแรก (ตัวเอง):** mutate guard ที่จุด `MOB_COMBAT_BAR` เป็น `if False`
(จำลอง bug กลับมา) → เทสใหม่ล้มด้วย `AssertionError` ชัดเจน → revert (`git diff`
ยืนยันว่า `runtime.py` ไม่มี diff เหลือ) → รันซ้ำเขียว

**รอบสอง (`pf-adversary` agent อิสระ):** ตรวจอีกสามมิวเทชันที่ตัวเองยังไม่ได้ลอง --
(ก) ปิด guard ที่จุด death ด้วย (ตัวเองลองแค่จุด bar) → เทสล้ม ✅ จับได้ (ข)
ใส่ `actor_count=13` แทน `count` จริงแต่ปล่อยบรรทัด print ให้โกหกว่า 115 อยู่
เหมือนเดิม (สถานการณ์ที่โจทย์กังวลถึงตรงๆ) → เทสล้มที่การเทียบไบต์เฟรม ไม่ใช่ที่
บรรทัด print → **นี่คือเหตุผลที่เทสต้องเทียบไบต์จริง ไม่ใช่แค่ grep คอนโซล** (ค)
จำลอง dying แก้แล้วแต่ dead ยังเป็นเฟรม one-entry เดิม (bug แบบไม่สมมาตร) →
เทสล้มที่ `dead_pc` ✅ จับได้ พบข้อสังเกตสไตล์ไม่บล็อก 2 จุด (เลข `115` ฮาร์ดโค้ด
ซ้ำ 3 ที่ทั้งที่มี `state.world_census_actor_count` อยู่แล้ว, docstring พิมพ์ `self`
ผิดที่ควรเป็น `state`) -- แก้แล้วทั้งคู่ (`@2313ceb`) ไม่เปลี่ยนพฤติกรรมเทส รันซ้ำ 11/11
เขียว

## 5 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `python3 -m unittest tests.test_mob_combat_dispatch`: 11/11 (เพิ่ม 2 จาก 9 เดิม) · สวีตเต็มอิสระ: **3510 เทส**, error 18 ตัวเดิม (capstone, environment เท่านั้น), skip 212, **0 FAIL ใหม่** · console gate ทั้งสองพิมพ์ `actor_count=115` จริงบนลำดับจริง (ยืนยันซ้ำได้ทุกรัน ไม่ใช่แค่ยืนยันสดครั้งเดียว) · มิวเทชันเทสยืนยันไม่ vacuous ที่ทั้งสองจุด (bar + death) |
| **client-observable** | ไม่มี -- รอบนี้ไม่ใช่รอบ attended, เป็นชั้น wire/DB เท่านั้น ตรงกับ nonclaim ของ `mob_death.py` เองว่ายังไม่พิสูจน์ว่าไคลเอนต์เรนเดอร์ผลจากเฟรม 115-actor นี้จริงไหม (คำถามนั้นเปิดอยู่ที่ `GT-084`/`GT-084-R2` ในคิว attended อยู่แล้ว) |

## 6 ถ้าผิดต้องย้อนอะไรบ้าง

สองคอมมิตใน `pirate-force-server` (`61de1ec`, `2313ceb`) แตะไฟล์เดียว
(`tests/test_mob_combat_dispatch.py`) -- ย้อนได้ทันทีด้วย `git revert 2313ceb
61de1ec` ไม่กระทบ production path ใดๆ เพราะเป็นเทสล้วน ไม่มีบรรทัด `src/`
เปลี่ยน

## 7 ข้อความถึง chief -- ใบเดียว (§ notes_to_chief)

`GAME_TEST_QUEUE.md` เป็นไฟล์ที่ chief เขียนคนเดียวตามธรรมเนียม
(`notes_to_chief/README.md`) -- ไม่แก้เองตามเขตเขียน เขียนผลนี้เป็นจดหมายให้
chief ย้ายไปลงเป็นเงื่อนไขพร้อมของ `GT-084`/`GT-084-R2` ในรอบถัดไปแทน (ดู
`notes_to_chief/20260827_1349_LANE-B-REPLY-real-arrival-census-recompose-
proof-committed.md`)

## 8 รอบถัดไปควรทำอะไร

1. เช็คว่า chief ย้ายผลรอบนี้ลง `GAME_TEST_QUEUE.md` เป็นเงื่อนไขพร้อมของ
   `GT-084-R2` หรือยัง
2. เช็คซ้ำว่า `combat_aggro` tick loop ต่อสายเข้า `runtime.py` หรือยัง (เส้นตาย
   `BUILD-005` 29 ส.ค. 23:59 -- ยังไม่เลย)
3. เช็คสถานะ `GT-060`/`combat_pickup` (THE WALL) -- ยังรอ attended capture
4. เช็คว่า chief เริ่มโครง `lane_hooks/` ตาม PANYA-ORDER §1 หรือยัง -- ถ้าลง main
   แล้ว รอบถัดไปของสายนี้ย้ายงานที่เคยขอเป็น CORE-REQUEST ไปเขียนเองใน
   `lane_hooks/lane_b_*.py` แทนตามที่ COO จะประกาศ

-- **สาย B · COMBAT**

# round `B_20260827_1349` (`s7hjdb`) · lane B · COMBAT -- missing headless
proof for PANYA-ORDER 12:30 §3's world-wipe acceptance criteria (census
recompose was already wired, but no test drove it on the real
arrival-then-attack sequence); plus, mid-round, a fresh COO-DECISION
(13:50) approved widening `mob_death.kill()` to the real 13-mob bg0001
roster -- registered the ruling before chief's next round needs it

**opened:** 2026-08-27 ~13:33 (+07:00) · **closed:** 2026-08-27 ~14:07 (+07:00)
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

## 6 ระหว่างรอบ -- COO-DECISION 13:50 อนุมัติขั้นสอง widen death scope ถึง
bg0001 เต็มโรงเตอร์ 13 ตัว -- ลงทะเบียนก่อนที่ chief จะต้องใช้

`git fetch origin main` ระหว่างรอบพบคอมมิตใหม่ (`a947f96`, pf_bridge):
COO-DECISION `20260827_1350` อนุมัติขั้นสองของคำขอที่สายนี้ยื่นไปตั้งแต่รอบ
`t48epl` (`20260827_1500_LANE-B-ASK-COO-widen-death-scope-to-real-mob-
roster.md`) -- เปิดให้ `mob_death.kill()` รับมอนจริงทั้ง 13 ตัวจากตาราง MOBS ใน
bg0001 ไม่ใช่แค่ `0x201F` จดหมายบอกให้ chief ใส่
`widened="COO-RULING-20260827-1350 widen-death-scope-bg0001"` ที่จุดเรียก
`kill()` ใน `runtime.py`

`kill()` fail-closed บนสตริง `widened=` ที่ไม่ใช่ key ที่ลงทะเบียนไว้ใน
`mob_death.WIDENING_RULINGS` (guard ที่รอบ `67jejl` สร้างไว้กันการเปิดช่องเกิน
ขอบเขต) -- ถ้า chief ใส่บรรทัดตามจดหมายโดยที่สายนี้ยังไม่ลงทะเบียน key ก่อน
`kill()` จะถูกปฏิเสธทุกครั้ง ไม่ทำงานตามที่ COO ตั้งใจ **ลงทะเบียนก่อน chief ต้อง
ใช้จริงในรอบนี้เลย** ไม่รอให้ chief เจอปัญหาก่อน

### สิ่งที่สร้าง (`pirate-force-server@291777f`, `@0d29460`)

`src/pirateforce_foundation/mob_death.py`: เพิ่ม key ใหม่ใน
`WIDENING_RULINGS` -- `covered_templates` = เซตของ `template_id` ที่ต่างกันของ
มอนจริงทั้ง 13 ตัวใน `field_mobs.load_roster()` (คำนวณจากโรงเตอร์จริง ไม่ใช่พิมพ์
มือ): `{31, 34, 35, 60, 61, 62, 65, 94, 97, 103}` (10 template แยกกัน จาก 13
identity เพราะ template 97 ซ้ำ 4 ตัว)

`tests/test_mob_death.py`: เทสใหม่ 3 ตัว -- (ก) ฆ่ามอนทั้ง 13 ตัวในโรงเตอร์จริง
ด้วยคำเคาะใหม่ ทุกตัวสำเร็จ (ข) เซต `covered_templates` ที่ลงทะเบียนไว้ตรงกับที่
คำนวณจากโรงเตอร์จริงเป๊ะ (กันดริฟต์เงียบถ้าโรงเตอร์เปลี่ยนในอนาคต) (ค) template
นอกโรงเตอร์ (ใช้ fixture Training Iron Man เดิม, template 916) ยังถูกปฏิเสธ
ภายใต้คำเคาะนี้ -- กันช่องโหว่แบบเดียวกับที่ `67jejl` ปิดไปแล้วสำหรับคำเคาะ 916
ไม่ให้เปิดกลับมาที่คำเคาะใหม่นี้

## 7 `pf-adversary` รอบสอง (agent อิสระ) -- พบข้อผิดพลาดจริง 1 จุด แก้แล้ว

ส่งให้ agent อิสระตรวจ diff ของ `mob_death.py`/`test_mob_death.py` แยกจากรอบ
แรก (โค้ด production จริง ความเสี่ยงสูงกว่าเทสอย่างเดียว) พบ:

**(ยืนยันจริง, แก้แล้ว `@3102ae8`):** comment ที่เขียนไว้ (คัดลอกคำอ้างจาก
จดหมาย COO มาตรงๆ โดยไม่ตรวจซ้ำ) บอกว่า chief ต้อง "เปลี่ยน" ค่า `widened=`
ที่มีอยู่แล้วที่ `runtime.py:3925` -- ตรวจโค้ดจริงแล้วพบว่าบรรทัด 3925 วันนี้เป็น
โค้ดคนละเรื่อง (สาขา fallback ของ `MOB_COMBAT_BAR`) และจุดเรียก `kill()` จริง
(บรรทัด 3938 วันนี้) **ไม่มี `widened=` เลยสักตัว** -- คำเคาะ 916 เดิมไม่เคยถูกต่อ
สายเข้า production path จริง มีแค่ระดับเทสเท่านั้น แก้ comment ให้อ้างจุดเรียก
โดยชื่อฟังก์ชันแทนเลขบรรทัด (เลขบรรทัดเคยขยับมาแล้วรอบนี้เอง) และบอกว่า chief
"เพิ่ม" ไม่ใช่ "เปลี่ยน" 🔴 **ข้อสังเกตสำหรับ chief:** ตัวจดหมาย COO-DECISION
`20260827_1350` เองก็อ้างเลขบรรทัด 3925 แบบเดียวกัน (จดหมายนั้นสายนี้ไม่แก้เอง
ไม่ใช่เขตเขียน) -- อย่าเชื่อเลขบรรทัดนั้น หาจุดเรียก `mob_death.kill()` จริงในโค้ด
แทน

**(พบช่องว่างออกแบบ ไม่บล็อกวันนี้, บันทึกเป็น comment):** คำเคาะนี้ตั้งชื่อว่า
"bg0001" แต่ `WIDENING_RULINGS` เช็คแค่ `template_id` ไม่เช็ค scene -- มีตาราง
มอนของอีก scene หนึ่งที่ commit ไว้แล้วในรีโปนี้ (ตั้งใจให้ยังไม่ต่อสาย ตามคำเคาะ
COO อีกฉบับ) ที่ใช้ `template_id` ซ้ำกับ bg0001 อยู่ 4 ตัว (31, 34, 35, 103) --
วันนี้ไม่มีทางเรียก `kill()` ได้จริงเพราะยังไม่ต่อสาย ไม่เปิดช่องอะไรเพิ่ม แต่วันที่
scene ที่สองถูกต่อสายผ่านจุดเดียวกันนี้ในอนาคต คำเคาะนี้จะอนุญาตมอนของ scene
นั้นโดยไม่ตั้งใจถ้าไม่มีใครเพิ่ม scene-awareness ก่อน -- บันทึกเป็น `[OPEN RISK,
NOT MEASURED]` ใน `mob_death.py` (ไม่เอ่ยชื่อโมดูลที่ห้ามต่อสายตรงๆ เพราะเทส
guard ของโมดูลนั้นเองสวีปหาชื่อนี้แบบ literal string ทั้งรีโป กว้างกว่าแค่ import
ตั้งใจจับแม้แต่ comment -- รอบนี้โดนจับจริงตอนรัน full suite ก่อนแก้คำ) ไม่ใช่
งานของรอบนี้ที่จะแก้ (ต้องออกแบบ scene-awareness ใหม่ ใหญ่กว่าขอบเขตรอบนี้)

**ข้อสังเกตกระบวนการ (ไม่ใช่ข้อบกพร่องของโค้ด, ส่งให้ COO พิจารณา):** agent
รายงานว่าเห็น commit ของสายนี้ขึ้น `origin` (ผ่าน stop-hook ที่บังคับ commit งาน
ค้างก่อนจบเทิร์น) ระหว่างที่มันยังตรวจ diff อยู่ -- กติกา "ต้องผ่าน pf-adversary
ก่อน commit" กับกลไก stop-hook ที่บังคับ commit งานค้างชนกันได้จริง ไม่ใช่แค่ทาง
ทฤษฎี รอบนี้จัดการโดย commit ก่อน (กัน stop-hook บล็อค) แล้ว push commit
แก้ไขเพิ่มถ้า pf-adversary เจออะไรจริง (แบบที่ทำจริงใน §6-7) -- ใช้ได้สำหรับรอบนี้
แต่เป็นคำถามเชิงกระบวนการที่ COO ควรรู้ ไม่ใช่สายนี้ตัดสินใจเองว่าถูกกติกาไหน
ก่อน

## 8 หลักฐานสองชั้น (ต่อจาก §5, สำหรับ §6 โดยเฉพาะ)

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `python3 -m unittest tests.test_mob_death`: 73/73 (เพิ่ม 3 จาก 70) · `tests.test_field_mob_tables_bg0015` (guard ของโมดูลที่ยังไม่ต่อสาย): เขียว ไม่ถูก comment ใหม่กระทบ · สวีตเต็มอิสระหลังแก้ครบ: **3513 เทส**, error 18 ตัวเดิม, skip 212, **0 FAIL ใหม่** · มิวเทชันเทส (ตัดเทม เพลต 103 ออกจากเซต) ยืนยันเทสทั้งสองจับได้จริง ไม่ vacuous |
| **client-observable** | ไม่มี -- การลงทะเบียนคำเคาะยังไม่ทำให้มอนตัวไหนตายได้เพิ่มจริงจนกว่า chief จะต่อสาย `widened=` เข้า `runtime.py` (งานของ chief รอบถัดไป) |

## 9 ถ้าผิดต้องย้อนอะไรบ้าง

สี่คอมมิตใน `pirate-force-server` แตะไฟล์ทดสอบ/เอกสารในเขตของสายนี้เท่านั้น
ไม่มีบรรทัด `runtime.py`/`app.py` เปลี่ยนเลยทั้งรอบ:
- `61de1ec`, `2313ceb`: `tests/test_mob_combat_dispatch.py` (§3) -- ย้อนด้วย
  `git revert 2313ceb 61de1ec`
- `291777f`, `0d29460`: `mob_death.py` + `tests/test_mob_death.py` (§6, คอมมิต
  ที่สองแก้ commit แรกที่ลืม stage ไฟล์ production) -- ย้อนด้วย
  `git revert 0d29460 291777f`
- `3102ae8`: แก้ comment ตาม pf-adversary รอบสอง (§7) -- ย้อนด้วย
  `git revert 3102ae8` (ย้อนเฉพาะอันนี้จะทำให้ comment กลับไปอ้างเลขบรรทัดผิด
  ไม่แนะนำให้ย้อนโดยไม่ย้อน `291777f`/`0d29460` ด้วย)

ทุกคอมมิตย้อนได้อิสระจากกัน ไม่มีคอมมิตไหนพึ่งพา schema/migration ที่ย้อนไม่ได้

## 10 ข้อความถึง chief -- ใบเดียว (§ notes_to_chief) ครอบคลุมทั้งสองเรื่อง

`GAME_TEST_QUEUE.md` เป็นไฟล์ที่ chief เขียนคนเดียวตามธรรมเนียม
(`notes_to_chief/README.md`) -- ไม่แก้เองตามเขตเขียน เขียนผลทั้งสองเรื่อง (§3
การพิสูจน์ census recompose + §6 การลงทะเบียนคำเคาะ bg0001) เป็นจดหมายเดียว
ให้ chief อ่านก่อนถือ LOCK รอบถัดไป พร้อมเตือนเรื่องเลขบรรทัด `runtime.py:3925`
ที่ผิด (§7) และข้อสังเกตกระบวนการเรื่อง pf-adversary-vs-stop-hook (ดู
`notes_to_chief/20260827_1349_LANE-B-REPLY-real-arrival-census-recompose-
proof-committed.md`)

## 11 รอบถัดไปควรทำอะไร

1. เช็คว่า chief ย้ายผลรอบนี้ลง `GAME_TEST_QUEUE.md` เป็นเงื่อนไขพร้อมของ
   `GT-084-R2` หรือยัง (§3)
2. เช็คว่า chief ต่อสาย `widened="COO-RULING-20260827-1350 widen-death-
   scope-bg0001"` เข้าจุดเรียก `mob_death.kill()` จริงหรือยัง (§6) -- ถ้าต่อแล้ว
   ให้ยืนยันสดว่ามอนอีก 12 ตัวนอกเหนือ `0x201F` ตายได้จริงตามที่ตั้งใจ
3. เช็คซ้ำว่า `combat_aggro` tick loop ต่อสายเข้า `runtime.py` หรือยัง (เส้นตาย
   `BUILD-005` 29 ส.ค. 23:59 -- ยังไม่เลย)
4. เช็คสถานะ `GT-060`/`combat_pickup` (THE WALL) -- ยังรอ attended capture
5. เช็คว่า chief เริ่มโครง `lane_hooks/` ตาม PANYA-ORDER §1 หรือยัง -- ถ้าลง main
   แล้ว รอบถัดไปของสายนี้ย้ายงานที่เคยขอเป็น CORE-REQUEST ไปเขียนเองใน
   `lane_hooks/lane_b_*.py` แทนตามที่ COO จะประกาศ

-- **สาย B · COMBAT**

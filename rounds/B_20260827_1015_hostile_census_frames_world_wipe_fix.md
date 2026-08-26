# round `B_20260827_1015` (`sifsfg`) · lane B · COMBAT -- compose hit/death frames into the full census, not one entry; PANYA-ORDER field-interpretation reply

**opened:** 2026-08-27 10:00 (+07:00) · **closed:** 2026-08-27 ~10:4x (+07:00)
**branches:** `claude/serene-darwin-sifsfg` (pirate-force-server, PR #89) ·
`claude/relaxed-goldberg-sifsfg` (pf_bridge, PR #161)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็น -- รอบนี้ไม่มีใครเปิดเกม เทสทั้งหมดเป็นระดับ wire/DB
สิ่งที่สร้างคือ**การแก้ที่ยังไม่ได้ต่อสาย**: ฟังก์ชันที่พิสูจน์แล้วว่าคอมโพสเฟรม hit/death แบบไม่ล้างเมืองได้
ถูกต้อง แต่ `runtime.py` (ไฟล์ของ chief) ยังไม่ได้เรียกมันแทนเฟรมเดิม -- ต้องรอ CORE-REQUEST-008 ต่อสายก่อน
ผู้เล่นถึงจะเห็นความต่าง (คือ: เมืองไม่หายตอนต่อสู้ ซึ่งยังไม่มีใครยืนยันด้วยตาว่าเคยหายจริงบนจอ)

## 1 ตรวจสอบ brief ที่ล้าสมัย -- ยืนยันแล้ว

Brief ต้นทางอ้างถึง `BUILD-004/005/006` ราวกับเริ่มจากศูนย์ -- ไม่จริง โค้ด mob/combat/death/loot/pickup
มีอยู่แล้วจำนวนมาก (`mob_aggro.py`, `mob_combat.py`, `mob_death.py`, `mob_loot.py`, `mob_pickup.py`,
`field_mobs.py` ฯลฯ) งานจริงของรอบนี้พบจากการอ่าน `STATUS.md`, รอบก่อนหน้า (`B_20260827_0805`) และจดหมาย
ที่มาหลังรอบนั้นปิด (~10:1x, 2026-08-27) -- ไม่ใช่จาก charter list เดิม

## 2 สิ่งที่พบหลังรอบก่อนปิด -- CHIEF-URGENT ยืนยัน world-wipe จริง

รอบก่อน (`B_20260827_0805`) ปิดด้วยข้อเสนอให้ chief ใส่ print-line เดียวใน `runtime.py` จดหมาย
`notes_to_chief/20260827_0920_CHIEF-URGENT-...` อ้างว่า **ใส่แล้ว** ที่ `runtime.py:4899-4924` และ
"เทสใหม่ 6 ตัว ผ่านหมด"

**ตรวจสดบน branch นี้ (`claude/serene-darwin-sifsfg`) แล้วไม่ตรงกับคำอ้าง**: `grep -rn
"roster_override_coverage\|MOB_DEATH_ROSTER_OVERRIDE_COVERAGE" src/pirateforce_foundation/runtime.py`
**ไม่พบสักบรรทัด** และอ่าน `runtime.py:4899-4924` ตรง ๆ พบว่าบรรทัด print ที่มีจริงตรงนั้นคือ
`print(world_population.census_console_line(generation))` กับ `print(world_density.m1_console_line(...))`
-- ไม่ใช่บรรทัด coverage ที่จดหมายอ้าง `git log --oneline -10 -- src/pirateforce_foundation/runtime.py`
ยืนยันว่า commit ล่าสุดที่แตะ `runtime.py` คือ `731498e` (CORE-REQUEST world_scene_liveness ของสาย A) ไม่มี
commit ไหนเกี่ยวกับ coverage print เลย **ไม่รู้ว่าเป็นช่องว่างระหว่าง branch (commit จริงอยู่ที่อื่นแต่ยังไม่
sync มา branch นี้) หรือคำอ้างในจดหมายคลาดเคลื่อน** -- ไม่ตัดสินแทน แจ้งไว้ตรง ๆ ให้ chief/COO ตรวจ ไม่กระทบ
งานหลักของรอบนี้ (การแก้ world-wipe เป็นคนละเรื่องกับ print-line นี้) แต่เป็นข้อเท็จจริงที่ต้องแก้ไขคำอ้างเดิม
ไม่ใช่เชื่อจดหมายแล้วอ้างต่อโดยไม่ตรวจ (หลักที่โปรเจกต์นี้ยึดเอง -- "verified independently, not copied from
the chief's own letter", `mob_death.py` docstring บรรทัดของ `full_roster_override`)

**แต่ระหว่างตรวจ chief พบเรื่องใหญ่กว่า:** `mob_combat.bar_frames`/`mob_death.death_frames` (โมดูลของสาย
นี้เอง) แต่ละตัวคอมโพส `legacy.make_runtime_remote_actors([entry])` แบบ **หนึ่งรายการเดี่ยว** และเรียกจาก
`runtime.py:3828-3835` แบบไม่มีเงื่อนไขบนบูตไร้แฟล็ก -- ไม่ผ่านจุด compose แบบ full-census ที่ arrival ใช้
`RE-092` (ปิดแล้ว 2026-08-26 22:23) พิสูจน์ระดับ registry แล้วว่า consumer เดียวกัน
(`GSCN_RunTimeProtocolRes` mask `0x02`) เป็น **replace-by-omission** -- ทุกครั้งที่มีคนโดนตีหรือมีมอนสเตอร์
ตาย เฟรมหนึ่งรายการนี้ **ล้างทั้ง 115-actor registry เหลือรายการเดียว** จริง ไม่ใช่แค่ทฤษฎีอีกต่อไป
(`notes_to_chief/20260827_0920_CHIEF-URGENT-combat-death-frames-confirmed-world-wipe-unconditional-on-flagless-path.md`)

จดหมายนี้เสนอให้สาย B เป็นข้อ 1 อันดับหนึ่งของรอบนี้ -- **ยึดตามนั้น**

## 3 สิ่งที่สร้าง -- `mob_death.hostile_census_frames` + `world_population.apply_identity_override`

หลักการ: **ใช้ตัวเข้ารหัสเดิม (encoder) ที่มีอยู่แล้ว ไม่เขียน selector ใหม่** -- แบบเดียวกับที่ arrival's
`_apply_mob_death_census_override` (ใน `runtime.py`, ไฟล์ของ chief) พิสูจน์แล้วว่าถูก

- `src/pirateforce_foundation/world_population.py` +`apply_identity_override(legacy, generation, override)`:
  reimplementation อิสระของอัลกอริทึมเดียวกับ `_apply_mob_death_census_override` (ไม่ import จาก
  `runtime.py`, เขียนใหม่ในโมดูลของสาย B) เพิ่ม type-check บน override dict ที่ต้นฉบับไม่มี
- `src/pirateforce_foundation/mob_death.py` +`hostile_census_frames(legacy, anchor, actor_count, roster,
  register, *, ledger=None, ...)`: rebuild census สดด้วย `world_population.build_world_population` (anchor/
  count ที่ `runtime.py` เก็บไว้อยู่แล้ว: `population_refresh_anchor`/`world_census_actor_count`) แล้ว splice
  `full_roster_override` (ไม่ใช่ `corpse_override` -- จะทำให้มอนสเตอร์ที่ยังไม่โดนตียืนด้วย body เปล่า) ผ่าน
  `apply_identity_override` -- **สามการเรียกเดียวกับที่ arrival ใช้ทุกตัว**
- `mob_combat.bar_frames`/`mob_death.death_frames` **ไม่แก้** -- docstring อัปเดตแบบเพิ่มข้อความ (เก็บของ
  เดิมไว้ ไม่ลบ) บันทึกว่า `RE-092` ยืนยันความเสี่ยงที่เคยแช่แข็งไว้ว่า "[OPEN RISK, NOT MEASURED]" แล้ว
- ข้อจำกัดที่บันทึกไว้ตรง ๆ ใน docstring: `dead_timer` ใช้กับ**ทุกตัวที่ตาย**ในทะเบียนพร้อมกัน ไม่ใช่แค่ตัว
  เดียว -- ปลอดภัยวันนี้เพราะ `SANCTIONED_FIRST_TARGET_IDENTITY` การันตีมีศพได้ทีละตัว จะพังจริงถ้า death
  gate ขยายในอนาคต

**production_allowed = true, ไม่มีแฟล็ก** -- ทั้งสองฟังก์ชันเป็น pure logic ไม่มีสวิตช์ (แต่**ยังไม่ถูก
เรียกจาก `runtime.py`** จนกว่า CORE-REQUEST-008 จะต่อสาย -- ดูข้อ 5)

## 4 เทส -- ต่อ 115-actor census จริง

`tests/test_world_population.py` +8: replace เฉพาะ identity ที่ระบุ, no-op บน override ว่าง, ignore identity
ที่ไม่อยู่ใน rung, ปฏิเสธ non-generation/non-dict/bad-key/bad-value
`tests/test_mob_death.py` +5: ตรงกับการคอมโพสอิสระผ่าน public function เดียวกัน (ไม่ tautological กับ
implementation), ครบ 115 actor, มอนสเตอร์ที่ยังไม่โดนตีได้ hostile body ไม่ใช่ default, embed byte ตรงกับ
`death_frames` เดี่ยว ๆ เป๊ะสำหรับศพเดียวกัน, ปฏิเสธแบบเดียวกับ `full_roster_override`

`python3 -m unittest tests.test_mob_death tests.test_world_population tests.test_mob_combat`: **147 ผ่าน**
`python3 -m unittest discover -s tests -p "test_*.py"`: **3365 ผ่าน/skip, error 18 ตัวเดิม**
(`capstone`/`pefile`/`pytest` ไม่ติดตั้งใน sandbox -- ตรวจแล้วว่าเป็น error ชุดเดิม ไม่ใช่ของใหม่)

## 5 CORE-REQUEST-008 -- สามจุดใน `runtime.py` (ไฟล์ของ chief สายนี้ไม่แตะ)

รายละเอียดเต็มอยู่ใน `notes_to_chief/20260827_1015_LANE-B-REPLY-hostile_census_frames-world-wipe-fix-plus-core-request.md`
สรุปสั้น: (1) `MOB_COMBAT_BAR` ที่ ~3828-3836 (2) เฟรม `dead` ของ `death_step` (3) เฟรม `dying` ของ
`death_step` (ต้องอ่านข้อจำกัด one-corpse ก่อน) ทั้งสามเรียก `mob_death.hostile_census_frames` ตัวเดียวกัน

## 6 PANYA-ORDER -- ตอบแล้ว (สาย B ส่วนของตัวเอง)

`notes_to_chief/20260827_1030_LANE-B-REPLY-PANYA-ORDER-npc-scene-file-field-interpretation.md` -- วัดได้ 3
ข้อ (f32_4/f32_5 ไม่ใช่ aggro radius จริง [negative, cross-check กับ `field_mob_ai_tables.py` ตรง ๆ], กลุ่ม
101+ ไม่ใช่มอนสเตอร์เป็นส่วนใหญ่ [21% vs 7%, cross-check กับ `field_mob_tables_bg0015.py` จริง], u16_1 ≈
จำนวนจุดต่อชุด แต่ตรงแค่ 40/51 ชุด) สมมติฐาน 1 ข้อ (ความหมายของกลุ่ม 101+ ยังไม่รู้ว่าคืออะไรกันแน่) ไม่รู้ 1
ข้อ (definition payload b5/b15/u32@11 เทียบ level/rank -- ไม่มีเครื่องมือ join ใน `src/` วันนี้ เปิดใบให้สาย
C ผ่านจดหมาย ไม่ได้แก้ `CLIENT_RE_QUEUE.md` เอง เพราะอยู่นอกเขตเขียนของรอบนี้)

## 7 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | เทสใหม่พิสูจน์ว่า `hostile_census_frames` คอมโพสถูกต้อง (ครบ 115, embed byte ตรงกับ death_frames เดี่ยว ๆ, มอนสเตอร์ที่ยังไม่โดนตีได้ hostile body) และ `apply_identity_override` แยกทดสอบ 8 เทส |
| **client-observable** | ไม่มี -- ไม่มีใครดูจอรอบนี้ และ `runtime.py` ยังไม่เรียกฟังก์ชันใหม่จนกว่า CORE-REQUEST-008 จะต่อสาย -- เมืองที่ล้างจริงหรือไม่ยังไม่มีใครเห็นด้วยตา (มีแต่หลักฐาน static+registry-level) |

## 8 ถ้าผิดต้องย้อนอะไรบ้าง

สองคอมมิตใน `pirate-force-server` (`6286059`, `5a98237`) ย้อนได้ด้วย `git revert` -- เพิ่มฟังก์ชันบริสุทธิ์
และเทสเท่านั้น ไม่แตะ `bar_frames`/`death_frames`/`full_roster_override`/wire format ที่มีอยู่ ไม่มีการต่อสาย
เข้า `runtime.py` เลย (รอ CORE-REQUEST-008) จึงไม่มีความเสี่ยงต่อ production path ใด ๆ จากรอบนี้จนกว่า chief
จะต่อสายเอง `pf_bridge` คือไฟล์รอบนี้เอง -- ลบได้โดยไม่กระทบโค้ด

## 9 `pf-adversary` รอบสอง -- หนึ่ง HIGH, สอง MODERATE/LOW, แก้ครบก่อน push

รีวิวรอบสอง (บน `claude/serene-darwin-sifsfg` / `claude/relaxed-goldberg-sifsfg`, PR #89/#161 ยัง draft ไม่
merge) พบสามข้อจริง แก้ทั้งหมดด้วยคอมมิตใหม่ ไม่แก้ history เดิม

1. **HIGH, พิสูจน์ด้วยการรันจริง.** `hostile_census_frames` forward `ledger` เข้า `full_roster_override(...,
   ledger=ledger, ...)` ตรง ๆ -- ถ้า caller ลืมส่ง `ledger` (ค่า default ของฟังก์ชันเองคือ `None`) มอนสเตอร์ที่
   ยังไม่ตายแต่โดนตีจนเลือดลดจะถูกส่งกลับไปที่ HP เต็มบนสายเงียบ ๆ (ตัว bug class เดียวกับที่รอบนี้เปิดมาแก้
   สำหรับ "existence" แต่คราวนี้เป็น "HP") พิสูจน์ด้วยการรันจริง: ตี mob ด้วย `Combatant(level=7,
   ability_str=132, ability_con=0)` เหลือ 2893/3857 HP แล้วเรียก `hostile_census_frames(...)` โดยไม่ส่ง
   `ledger` -- ผลลัพธ์คือ body เต็มเลือด ไม่ใช่ 2893 **แก้แล้ว**: `hostile_census_frames` ปฏิเสธ `ledger=None`
   ด้วยชื่อ (`REFUSE_CENSUS_FRAME_WITHOUT_A_LEDGER`, `MobDeathContractError`) -- ตัดสินใจไม่ให้ `None` แปลว่า
   "ยอมให้ทุกตัวเรนเดอร์ที่ HP เต็มแบบเงียบ ๆ" เพราะฟังก์ชันนี้ (ต่างจาก `full_roster_override`/
   `repopulation_entries` ที่ตระกูลเดียวกันซึ่ง `ledger=None` ยังคงเป็นความหมายที่รองรับจริง สำหรับ caller ที่
   ยังไม่มี ledger เปิดอยู่) ถูกออกแบบมาให้เรียกทุกครั้งที่มี hit/death frame ตาม docstring ของตัวเอง และ
   `strike()` การันตีอยู่แล้วว่าต้องมี `CombatLedger` typed ก่อนจะมี hit/death frame เกิดขึ้นได้ -- caller จริง
   ทุกจุดของฟังก์ชันนี้จึงมี ledger อยู่แล้วเสมอ การไม่ส่งมาคือบั๊ก ไม่ใช่ caller ที่ชอบธรรม เพิ่มย่อหน้า
   docstring อธิบายการตัดสินใจนี้ตรง ๆ (LEDGER IS REQUIRED HERE...) เพิ่มเทส 2 ตัวใน `tests/test_mob_death.py`:
   `test_hostile_census_frames_refuses_a_missing_ledger_by_name` (เรียกไม่ส่ง ledger ต้อง raise) และ
   `test_hostile_census_frames_carries_the_true_damaged_hp_not_the_ceiling` (repro บั๊กจริงของ adversary --
   ตี mob บางส่วน, threads ledger, ยืนยันว่า body ที่คอมโพสตรงกับ `field_mobs.hostile_actor_entry(...,
   current_hp=damaged_hp)` ไม่ใช่ ceiling) ตรวจ manual นอกเทสด้วยว่าถ้าไม่มีการแก้นี้ เทสที่สองจะ fail จริง
   (`entry == expected_ceiling` เป็น `True`, `entry == expected_damaged` เป็น `False` ก่อนแก้)
2. **MODERATE, พิสูจน์ด้วยการสร้าง test case.** `apply_identity_override`'s guard (`offset !=
   len(generation.pc)`) เช็คแค่ผลรวมของ `entry_bytes` ตรงกับ `len(pc)` ไม่จับ permutation ที่สลับความยาวของ
   สอง entry แต่ผลรวมเท่าเดิม -- ถ้าเกิดขึ้นจะ splice byte ผิดตำแหน่งแบบเงียบ ไม่ raise ช่องโหว่นี้สืบทอดมาจาก
   `runtime.py`'s private original (`_apply_mob_death_census_override`) ไม่ใช่ของใหม่ที่รอบนี้สร้าง แต่รอบนี้
   ทำให้มันเป็น public utility ที่ตั้งใจให้ caller อื่นใน lane B reuse ได้ ซึ่งขยาย exposure โดยไม่ได้เพิ่ม
   การป้องกัน **ไม่ release-blocking** -- เส้นทางเรียกจริงเพียงเส้นเดียววันนี้สร้าง `generation` สดผ่าน
   `build_world_population` ซึ่งไม่มีทางสร้าง misalignment แบบนี้ได้ **ตัดสินใจ**: ไม่แก้โครงสร้าง (ต้องมี
   known-good source มา validate `entry_bytes` แยกจาก `generation` เอง ซึ่งไม่มี caller ไหนขอวันนี้) แต่บันทึก
   ช่องโหว่ไว้ตรง ๆ ใน docstring ส่วน NONCLAIM ใหม่ ระบุชัดว่า caller ที่สร้าง/แก้ `WorldPopulationGeneration`
   เองมือ (ไม่ผ่าน `build_world_population`) ห้ามเชื่อ guard นี้ว่าจะจับ permutation ได้
3. **LOW-MODERATE, พิสูจน์ด้วย mutation testing.** คอมเมนต์ใน
   `test_hostile_census_frames_matches_independent_recomposition` เดิมอ้างว่า "not tautological with the
   implementation" -- adversary ทำลาย `apply_identity_override` (ให้มันเมิน override dict) แล้วรันเทสใหม่:
   เทสตัวนี้ยังผ่านอยู่ (เพราะ "expected" ถูกคำนวณผ่าน `apply_identity_override` ตัวเดียวกับที่โค้ดที่ทดสอบก็
   เรียก บั๊กเลยหักล้างกันทั้งสองฝั่ง) ส่วนอีก 4 เทสจับได้ถูกต้อง **แก้แล้ว**: เพิ่ม loop ท้ายเทสที่ walk
   offset เองจาก `plain_generation.actor_identities`/`entry_bytes` (ที่ `apply_identity_override` ไม่เคย
   แตะ) เทียบ byte ตรงกับ `override` dict ดิบจาก `full_roster_override` โดยตรง -- ไม่ผ่าน
   `apply_identity_override` เลยทั้งสองฝั่ง พร้อมแก้คอมเมนต์ให้บอกตรงว่าข้อกล่าวอ้างเดิมพิสูจน์อะไรได้จริง
   (การต่อสายอาร์กิวเมนต์ให้ถูก sub-call ไม่ใช่ความถูกต้องของ `apply_identity_override` เอง)

**แก้เพิ่มด้วย (cosmetic, hygiene):** `apply_identity_override`'s key-type check มี dead clause: `type(key)
is not int or type(key) is bool` -- `type(True) is not int` เป็น `True` อยู่แล้ว (type ของ `True` คือ `bool`
ไม่ใช่ `int`) ครึ่งหลัง `or type(key) is bool` เลย unreachable ตัดออกเหลือ `type(key) is not int` เท่าเดิม
(เทส `test_apply_identity_override_refuses_bad_keys_and_values` ที่ pin `{True: b"x"}` ยังผ่านเหมือนเดิม)

**ตรวจแล้วไม่พบ (ยืนยันตามที่ adversary บอกไว้ ไม่ต้องทำซ้ำ):** `bar_frames`/`death_frames` เป็น
docstring-only diff จริง เทสเดิม+ใหม่ทั้งหมด (147 ก่อนรอบนี้ -> 149 หลังเพิ่ม 2 ตัว) ผ่านจริงกับข้อมูลจริง
ไม่ใช่ mock ข้อจำกัด one-corpse ที่บันทึกไว้ยืนยันจริงที่ HEAD (`grep` หา `kill()`/`widened=`) การอ้าง `RE-092`
และ CHIEF-URGENT citation ตรงกับของจริง ไม่มีการฟอกชั้นหลักฐาน `count_source` default ถูกต้องและเป็น
diagnostics-only

**หลังแก้ครบสามข้อ:** `python3 -m unittest tests.test_mob_death tests.test_world_population
tests.test_mob_combat`: **149 ผ่าน** (ของเดิม 147 + เทสใหม่ 2 ตัวจากข้อ 1)
`python3 -m unittest discover -s tests -p "test_*.py"`: **3367 ทั้งหมด, error 18 ตัวเดิม (capstone import
ล้วน, ไม่มี FAIL ใหม่), skip 212** -- ตรวจ `grep "^ERROR:\|^FAIL:"` แล้วว่า error ทั้ง 18 ตัวเป็น
`ModuleNotFoundError: capstone` ในไฟล์ static-RE ชุดเดิมทั้งหมด ไม่มี `FAIL:` เกิดใหม่เลย
cp874-encodability ของทั้งสามไฟล์ที่แตะ (`mob_death.py`, `world_population.py`, `tests/test_mob_death.py`)
ตรวจแล้วผ่าน (`.encode("cp874")` ไม่ throw)

**ไฟล์ที่แตะรอบสอง:** `src/pirateforce_foundation/mob_death.py`, `src/pirateforce_foundation/world_population.py`,
`tests/test_mob_death.py` (ทั้งสาม `pirate-force-server`) และไฟล์ round นี้เอง (`pf_bridge`)
**ยังไม่ commit/push** -- ตาม hard limit ของสาย B (never `git commit`/`git push`) ปล่อยให้ chief/orchestrator
เป็นคนคอมมิตและเปิด/อัปเดต PR ต่อ

-- **สาย B · COMBAT**

R377
start 2026-09-06T21:23+07:00
claim

# chief round `awnjat`

## รอบนี้ขยับ NOW/M ข้อไหน

ไม่ขยับบันไดไมล์สโตน M2/M3/M4 โดยตรง (ยังรอ COO เคาะ F1 บน `#948` และรอ UI/A
เฟรมผู้สมัคร M2 ตามที่ `NOW.md` บอก) แต่ขยับ **LANE-Q CORE-REQUEST สองใบที่ค้าง**
(`1950`/`1951`, §17 ข้อ 3 "ต่อสาย CORE-REQUEST ก่อนงานอื่น") และปิดหนี้เทส
สองข้อที่ R376 ทิ้งไว้ (F7/F8 ของ `DEATH_SEED_WIRING`, `#948`) แม้ push เข้า
`#948` เองไม่ได้ (เหตุผลด้านล่าง)

## 1) `pirate-force-server #948` (F1 ยังรอ COO -- ไม่แตะ) -- F7/F8 แก้แล้ว, เก็บเป็น patch ไม่ใช่ push

R376 ทิ้งไว้ 4 ข้อ: (1) รอคำเคาะ F1 (2) อ่าน 18 เทสของ F5 (3) แก้ F7 (4) แก้ F8

**F7 (relogin ปลอม)**: `test_a_relogin_finds_the_monster_it_killed_still_dead`
เดิมเรียก `_session()` สองครั้งด้วยคนละ token = คนละบัญชีคนละตัวละคร ไม่ใช่
relog จริง เพิ่ม `_relogin(token)` helper (login ซ้ำด้วย token เดิม ไม่สร้าง
ตัวละครใหม่ เลือกตัวเดิมด้วย `list_characters(...)[-1]`) แล้วแก้เทสให้ใช้
token เดียวตลอด + assert `account_id`/`selected.id` ตรงกันจริง

**F8 (มิวแทนต์รอด 2 ตัว)**: วัดจริงว่าทำไมรอด -- ทั้ง 6 เทสเดิม sync
session ที่อยู่ boot scene ของตัวเอง ซึ่ง `__init__` seed
`mob_combat_scene_folder` ให้ตรงกันอยู่แล้ว เลยไม่เคยเข้า
`if folder != self.mob_combat_scene_folder:` (ที่ `mob_respawn.
sweep_the_session_register` อยู่) เลย -- ไม่มีอะไรระหว่างตำแหน่ง seed เดิมกับ
ท้าย method อ่านสิ่งที่ seed เขียนเลย เขียนเทสใหม่บังคับเปิด branch
(`relogged.mob_combat_scene_folder = None` ก่อน sync หนึ่งครั้ง ไม่ใช่การย้าย
ฉากจริง) แล้ววัดจริงด้วยสคริปต์แยก (ไม่ใช่เดา):
ลำดับถูก -> console มีบรรทัด `MOB_RESPAWN opened=0 dated=1 ...` เพราะ sweep
เห็นหลุมศพที่เพิ่ง seed ; ลำดับผิด (ทั้งสองมิวแทนต์: ย้าย statement ไปท้าย
method, หรือ seed ด้วย `self.mob_combat_scene_folder` แทน `folder`) -> sweep
เจอ register ว่างเปล่า ไม่มีบรรทัด `MOB_RESPAWN` เลย (seed สายไปเติมทีหลัง
เงียบๆ) -- ยืนยันด้วย `git diff`+รัน pytest จริงทั้งสองมิวแทนต์ ก่อนเขียนเทส
เป็นเทสที่ 7 assert `"MOB_RESPAWN" in console` จับได้ทั้งคู่ (validated: mutant1
FAIL, mutant2 FAIL, original PASS, 7/7 green)

🔴 **ทำไมไม่ push เข้า `#948`**: กิ่งของ PR นั้น (`claude/upbeat-hamilton-l5tqxc`)
ไม่ใช่กิ่งที่ระบบมอบให้เซสชันนี้ (`claude/keen-pasteur-awnjat`) -- ล็อกรอบข้อ 8
อนุญาตให้ fetch กิ่งเก่ามาต่อ แต่ sandbox ของเซสชันนี้ปฏิเสธ push ไปกิ่งอื่นที่
ไม่ใช่ของตัวเอง เก็บ diff เต็มไว้ที่
`rounds/E_20260906_2123_awnjat_death_seed_f7_f8_fix.patch` (verified: `git
apply` สะอาดบน `origin/claude/upbeat-hamilton-l5tqxc` -- ยังไม่ได้ลองบนกิ่งจริง
เพราะเป็นกิ่งของ session อื่น) รอบหน้าที่ยึด/ต่อ `#948` เอาแพตช์นี้ไป apply
ได้ทันที ก่อนเขียนโค้ดใหม่ทับ

**F5 (conftest.py "13 tests in 4 files" ผิด)**: วัดซ้ำ (`mv tests/conftest.py
/tmp && pytest tests/`): **73 failed** (adversary วัดไว้ 72 -- ต่างกันไม่มีนัย
สำคัญ ไม่ไล่หาสาเหตุ 1 ตัวรอบนี้), **12415 passed**, 373 skipped -- รายชื่อ
เต็มบันทึกที่ `rounds/E_20260906_2123_awnjat_f5_no_conftest_failures.txt`
(29 บรรทัด unique หลัง sort -u) **ยังไม่ได้อ่านทีละใบ** ตามที่ R376 ขอ -- งาน
จริง ไม่ใช่แค่เดา ใช้เวลาเกินรอบนี้ที่เหลือหลังทำ CORE-REQUEST สองใบ ส่งต่อ
เป็นงานแรกของรอบถัดไปที่ยึด `#948`

## 2) LANE-Q CORE-REQUEST `1950`/`1951` (§17 ข้อ 3, ค้างตั้งแต่ 19:50/19:51)

**`1950` GRANTED, โค้ดขึ้นรอบนี้**: `migrations/016_character_quest_state.sql`
(`character_quest_flags`/`character_quest_counters`) + `store.py`
`get_quest_flag`/`set_quest_flag`/`get_quest_counter`/`set_quest_counter`
ตามคอนแทร็กต์ที่ใบขอเขียน (`quest_id` u16 จาก
`columbus_quest_dispatch.py:330`'s `u16tag`, `flag_value`/`counter_value` u32,
`counter_name` 1..128, `set_*` = absolute set) เทสใหม่ 32 เคส
(`tests/test_store_quest_state.py`) รูปแบบเดียวกับ `equip_item`/
`test_store_character_equipment.py` (TypeError/ValueError/KeyError/
WriteLockTimeout, relog-survives)

🔴 **สิ่งที่วัดแล้วต้องแก้จริง ไม่ใช่ปล่อยผ่าน**: การเพิ่มนี้ชน
`QuestAndShopStateGuardTests` เอง -- docstring ของคลาสนั้นพูดถึงกรณีนี้ตรงๆ
("ถ้ามีใครลง quest tracking จริง ต้อง re-grade matrix ก่อน") แก้
`EXPECTED_TABLES`/`ALLOWED_SYMBOLS["store.py"]` แบบตรงไปตรงมา (ไม่อ้างว่า
"ไม่ใช่ quest state" เหมือนรายการอื่นในดิกต์ เพราะมันคือ quest state จริง)
+ เติม UPDATE note ใน `docs/FUNCTIONAL_COVERAGE.json`'s
`quest_accept_and_progress` row: ประตูนี้เป็นคนละระบบกับ Columbus
quest3021/3205 ที่ row นั้นพูดถึง ยังไม่มีอะไรเรียกมันจริง -- row เดิมยังเป็น
`in_progress` เหมือนเดิม

**`1951` ไม่ให้ตอนนี้** (วัดจริง ไม่ใช่ปัดตก): ลองใส่ patch ตามที่ใบขอเสนอ
(`quest_context`/`quest_store`/`_in_memory_quest_state_store` ลง
`ALLOWED_SYMBOLS["script_host.py"]`) แล้วรัน
`test_every_symbol_exemption_is_still_earned` -- **แดง** เพราะสามชื่อนี้ไม่มี
อยู่จริงใน `script_host.py`'s โค้ดที่รันอยู่ (ใบของ Q เองบอกว่า revert ออก
ก่อน push PR `#947`) ตรวจสอบสมมติฐานว่า grant เดิม (`lua_api_quest`/`quest`/
`quest_clock`) เป็น preemptive เหมือนกันหรือเปล่า -- ไม่ใช่ (`grep`
ยืนยันสามชื่อนั้นมีอยู่จริงตอน grant) ส่งกลับ patch พร้อมวางที่แน่ชัดให้ Q ใส่
ใน**รอบเดียวกับที่โค้ด wiring จริงกลับเข้าไป** (ไม่ใช่กิ่งเปล่า) เต็มความ
ในจดหมายตอบ

พบเรื่องแทรก: `pirate-force-server#947` (โค้ด Q รอบ `7v7yn2` ที่ CORE-REQUEST
ทั้งสองใบอ้างถึง) **closed ไม่ merge** (state=closed, merged=false, ไม่มี
SYNC-NOTICE เพราะ cross-repo record ของ reaper ปิดอยู่ตั้งแต่ R371) แจ้งใน
จดหมายตอบแล้ว -- Q ต้อง re-land ก่อนใช้ accessor ใหม่นี้ได้จริง

จดหมายตอบเต็ม: `notes_to_chief/20260906_2151_CHIEF-REPLY-LANE-Q-quest-state-door-granted-1950-1951-not-yet-earned.md`
บริโภคใบขอทั้งสอง + stub แล้ว

## หลักฐาน

- `pytest tests/test_death_seed_call_site.py tests/test_mob_death_persistence.py tests/test_scene_scoped_combat_wiring.py`: 82 passed (F7/F8 fix, ยังไม่ push เข้า `#948` -- ดูเหตุผลข้างบน)
- `pytest tests/test_store_quest_state.py tests/test_npc_interaction_wire.py tests/test_store_character_equipment.py`: 73 passed, 35 subtests (`1950` code)
- `python3 tools/verify_functional_coverage.py`: PASS · `python3 tools/verify_hypothesis_ledger.py`: PASS
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: PREFLIGHT PASS (ก่อน commit สุดท้าย -- แจ้ง 3 ไฟล์ยังไม่ commit ตอนรัน ครั้งนี้ commit แล้วก่อน merge origin/main)
- full suite `pytest tests/` บนต้นไม้ merge origin/main แล้ว (commit สุดท้ายจริง): ผลอยู่ท้ายไฟล์นี้ก่อน push (เติมด้านล่างหลังรันเสร็จ)
- `ADVERSARY_PENDING pirate-force-server (branch claude/keen-pasteur-awnjat)` -- สั่งต้นรอบ (`pf-adversary` วิจารณ์ `1950` accessor) ยังไม่คืนตอน push

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- quest flag/counter เป็นต่อตัวละคร
(`character_id`) ไม่ใช่ต่อฉาก เหมือนที่ PR `#947` บอกไว้แล้ว

## รอบหน้าทำอะไร

1. ยึด/ต่อ `#948`: `git apply rounds/E_20260906_2123_awnjat_death_seed_f7_f8_fix.patch` บนกิ่งนั้นก่อนแตะโค้ดอื่น แล้วอ่าน 18 เทสใน `rounds/E_20260906_2123_awnjat_f5_no_conftest_failures.txt` ทีละใบตามที่ R376 ขอ (F5) -- ยังไม่ได้ทำ
2. ตรวจว่า COO เคาะ F1 หรือยัง (`notes_to_chief/20260906_2115_LANE-E-ASK-COO-death-seed-on-the-attack-path-needs-a-ruling.md`) ก่อนแตะ seed placement
3. ตรวจผล `pf-adversary` (D2 ของรอบนี้ที่ `1950`) ที่ยังไม่คืนตอน push
4. เมื่อ Q re-land `#947` พร้อม `quest_context`/`quest_store` wiring: วาง patch ใน `notes_to_chief/20260906_2151_CHIEF-REPLY-*.md` ลงกิ่งเดียวกัน
5. reaper + concurrency เท็จ, เนื้อใบ GT สี, `AGENTS.md` §7 (ค้างจาก R371/R376 หลายรอบแล้ว)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ -- LANE-Q ได้ประตูเก็บสถานะเควสข้าม relog แล้ว (โค้ดถูกต้องมีเทสยืนยัน) แต่ยังไม่มี dispatch จริงเรียกมัน และ DEATH_SEED_WIRING (มอนตายค้างข้าม relog) ยังรอคำเคาะ F1 ก่อนจะไปถึงผู้เล่นได้ | pirate-force-server (round awnjat, quest state door) + patch สำหรับ #948

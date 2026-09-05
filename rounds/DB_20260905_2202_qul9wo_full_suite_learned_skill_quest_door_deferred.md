# DB round (`qul9wo`) -- 2026-09-05T22:02+07:00 (TZ=Asia/Bangkok), closed 2026-09-05T23:04+07:00

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

อ่าน `NOW.md` สดล่าสุด (ตรวจล่าสุด 21:52 โดย COO) ก่อนอื่นตามกติกา -- รอบนี้ไม่ขยับบันไดไมล์สโตนหลัก
(M2/M3/M4 ไม่ใช่ของ DB รอบนี้) แต่ขยับบรรทัด "PLAYER/CHARACTER = LANE-DB มาก่อนทุกอย่างในคิว DB" ทางอ้อม:
ตอบ CORE-REQUEST ของ LANE-CS (`character_skills.source` รับ `'learned'`) และเปิดประตูสถานะเควสให้ LANE-Q
ตาม `PANYA-ORDER 2039` ข้อ 4 (ตัวหลังยังไม่ landed -- ดู §4)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- โค้ดรอบนี้ไม่แตะ world/scene state ที่แชร์ระหว่าง session เลย
(`character_skills`/`character_quest_flag`/`character_quest_counter` เป็นข้อมูลต่อตัวละคร ไม่ใช่ต่อฉาก)

## 1. ล็อกรอบ

- `list_pull_requests` หัวข้อ `[LANE-DB]` สถานะ open ทั้งสองรีโปก่อนแตะโค้ด: **ว่างเปล่าทั้งคู่** -- ไม่มี
  รอบทำงานค้าง ไม่ต้อง takeover
- เซสชันนี้ได้กิ่งที่ระบบมอบให้ตรงตัวอยู่แล้ว (`claude/epic-meitner-qul9wo` ที่ `pf_bridge`,
  `claude/cool-babbage-qul9wo` ที่ `pirate-force-server`) `git fetch origin main` แล้วยืนยันทั้งสองกิ่งตรง
  `origin/main` สดก่อนเริ่ม (ไม่มีอะไรหายเพราะกิ่งไม่มี commit ของตัวเองมาก่อนหน้านี้)
- เปิด claim PR `pf_bridge#1382` ทันที (`rounds/DB_20260905_2202_qul9wo_claim.md`) list ซ้ำทันทีหลังเปิด:
  ไม่มี `[LANE-DB]` PR อื่นที่เก่ากว่าและยังมีชีวิต -- ถือกุญแจรอบได้ไม่มีคู่แข่ง

## 2. กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-DB"` บน `origin/main` สด: ใบใหม่สองใบ (ไม่มี `.CONSUMED.txt` คู่)
- `20260905_2058_COO-DECISION-ka1a2039-item4-lane-q-needs-quest-state-columns-per-character-declare-store-doors-LANE-DB.md`
  -- PANYA-ORDER 2039 ข้อ 4: เปิดประตูสถานะเควสให้ LANE-Q, จดหมายถึง Q กำหนด 23:01
- `20260905_2119_LANE-CS-CORE-REQUEST-character-skills-learned-source-to-lane-db.md` -- LANE-CS ขอ
  `source='learned'` + `grant_learned_skill`

ทั้งสองใบตอบและบริโภคแล้วรอบนี้ (stub `.CONSUMED.txt` + สำเนาใน `consumed/` อยู่ในกิ่งนี้) -- รีเฟรช
กล่องจดหมายอีกครั้งก่อนปิดรอบ: ไม่มีใบใหม่จ่าหน้าถึง DB เพิ่ม

## 3. ทำอะไร -- ชิ้นที่ 1: `character_skills.source` รับ `'learned'` (LANDED)

ตอบ CORE-REQUEST `2119` ของ LANE-CS: `migrations/014_character_skills_learned_source.sql` (rebuild ตาม
สูตร `004` -- SQLite แก้ CHECK ตรงไม่ได้) เพิ่มค่า `'learned'` เข้า `character_skills.source` CHECK list
(ค่าเดียว ไม่แยก `'trainer'`/`'quest'`/`'level_up'` ตามที่ CS เสนอเป็นตัวเลือกแรก) + `SQLiteStore.
grant_learned_skill(character_id, skill_id) -> tuple[int, ...]` -- `UNIQUE(character_id,skill_id)`
เดียวกับ `grant_starting_skills`, `INSERT OR IGNORE` ไม่ใช่ `OR REPLACE`, อ่านกลับหลังเขียน, ไม่มีเมธอด
เดิมถูกแก้แม้แต่บรรทัดเดียว

**ต่างจากข้อเสนอหนึ่งจุด**: `grant_learned_skill` ไม่รับ `granted_at` เป็นพารามิเตอร์ (คำนวณเองด้วย
`_now()` เหมือน `grant_starting_skills`) -- ตอบกลับ CS แล้ว (`notes_to_chief/
20260905_2228_LANE-DB-REPLY-*`) Protocol ของเขาต้องปรับ arity ก่อน wire จริง

เทสใหม่ 34 ตัว (`tests/test_persistence_character_skills_learned_014.py`) + แก้เทสเดิม 3 ไฟล์ที่ตรึงเลข
migration/schema ไว้ตรง (สิทธิ์เดิมของ LANE-DB ตามใบ `20260901_1416`/`20260901_1459` กับ chief):
`test_item_move_capture.py` (migration count pin 13->14), `test_persistence_speed_walk_seed_008.py`
(pending-versions list เพิ่ม 14), `test_persistence_character_skills_011.py` (สลับค่าโพรบ CHECK-refusal
จาก `'learned'` เป็น `'trainer'` เพราะ `'learned'` กลายเป็นค่าจริงแล้ว)

## 4. ทำอะไร -- ชิ้นที่ 2: ประตูสถานะเควสให้ LANE-Q (BUILT, NOT LANDED -- ดูเหตุผล)

ตอบ `COO-DECISION 2058`: ออกแบบ+เขียนจริง `migrations/014_character_quest_state.sql` (เลข 014 ชนกับชิ้นที่
1 หลังจัดลำดับใหม่ -- ดูด้านล่าง) + `persistence_quest_state.py` (`QuestFlagRow`/`QuestCounterRow`) + 5
เมธอดใน `store.py` (`set_quest_flag`/`get_quest_flag`/`set_quest_counter`/`increment_quest_counter`/
`get_quest_counter`) หลักฐานออกแบบจาก `gamedata/lua/Quest/q_kill5.lua` จริง (`Quest.SetFlag`/
`Quest.GetQuestFlag` = เลขสถานะต่อ (ตัวละคร,เควส) · `Quest.MobKillCount`/`GetMobKillCount` = ตัวนับมีชื่อ
ต่อ (ตัวละคร,เควส)) + `quest_id` ผูก u16 ตาม `columbus_quest_dispatch.py:330` (`legacy.u16tag`) -- เทส 59
ตัวผ่านหมด (`tests/test_persistence_quest_state.py`) ส่งจดหมายประกาศประตูให้ LANE-Q แล้ว (`notes_to_chief/
20260905_2212_*`) ก่อน push ครบตามกำหนด 23:01

**pf-adversary ตรวจ diff ชิ้นนี้แล้ว** (เรียกต้นรอบ, ผลคืนกลางรอบ): ไม่พบบั๊กจริงในตัวเมธอด/schema --
พบ 3 ช่องว่างเทส (read-side validation ไม่มีเทส, SQLite INTEGER boundary ไม่มีเทส, CHECK constraint ที่
ชั้น SQL ตรงไม่มีเทส) + คำกล่าวอ้างผิดจุดหนึ่งในดอกสตริง migration (อ้างว่า `011` ใช้ `ON DELETE CASCADE`
แบบเดียวกัน แต่ `011` ไม่มีจริง) -- แก้ครบทั้งสี่ข้อแล้ว (23 เทสเพิ่ม, ดอกสตริงแก้)

🔴 **รันชุดเต็มก่อน push แล้วพบว่าชนไกลออกไปคนละจุด**: `tests/test_npc_interaction_wire.py::
QuestAndShopStateGuardTests` สองตัว (`test_store_schema_owns_no_quest_shop_or_reward_table` --
`EXPECTED_TABLES` ไม่มีสองตารางใหม่ · `test_no_foundation_module_implements_quest_or_shop_behavior` --
`persistence_quest_state.py` ใช้คำว่า "quest" ทั่วไฟล์ ไม่อยู่ใน `ALLOWED_SYMBOLS`) guard นี้ออกแบบมาให้
แดงตอน "quest tracking" ลงจริง โดยเจตนา (docstring ของมันเอง) และกฎข้าง `ALLOWED_SYMBOLS` เขียนตรงว่า
"An exemption is a name chief has READ. It is never granted to make a red run green" -- **ไม่ปลดแฟล็กเอง**
(ตารางของผมชื่อ "quest" ตรงตัว ไม่เหมือนสามตัวที่เคยได้ whitelist มาก่อนซึ่งไม่ใช่ quest/shop/reward จริง)

**ตัดสินใจรอบนี้**: ถอดชิ้นนี้ออกจากกิ่งที่ push (`git reset --mixed origin/main` แล้วคัดแยกเฉพาะชิ้นที่ 1
กลับเข้า commit -- ดูรายละเอียดเลข migration ด้านล่าง) เขียนใบ ASK ถึง chief/COO
(`notes_to_chief/20260905_2236_LANE-DB-ASK-COO-*`) เสนอสามทางเลือก (chief อ่านแล้ว whitelist / re-grade
coverage matrix ก่อน / เปลี่ยนชื่อหนีคำ -- ไม่แนะนำทางที่สาม) ไม่ตัดสินใจแทนคุณ + ส่งใบแก้ไขถึง LANE-Q
(`notes_to_chief/20260905_2237_*`) ว่า PR เลื่อน ไม่ใช่ยกเลิก -- โค้ดพร้อมสมบูรณ์ วางไว้ที่ scratchpad
เซสชันนี้ (ไม่อยู่ในกิ่ง) รอ chief ตอบแล้วเอากลับมา push ได้ทันทีรอบหน้า

**ผลข้างเคียงของการถอด**: เลข migration ของชิ้นที่ 1 เปลี่ยนจาก `015` เป็น `014` (แทนที่เลขที่ชิ้นเควส
เคยจอง) -- คงเลขต่อเนื่องไม่มีช่องว่าง แก้ทุกจุดอ้างอิงในไฟล์นั้น+เทสที่ผูกเลขไว้แล้ว

## 5. ชุดเทสของรอบ (เฉพาะที่ landed จริง)

`tests/test_persistence_character_skills_learned_014.py` (34 เทสใหม่): migration shape (สอง CREATE
statement... ผิด -- ไฟล์นี้เป็น rebuild ไม่ใช่ bare create, มี guard row-count/FK เช็ค), rebuild ที่
013-only tree แล้วเปิดเต็มยืนยันแถวเดิมรอด, `grant_learned_skill` เขียน+อ่านกลับ, idempotent, coexist
กับ starting_kit, ปฏิเสธ input ผิดก่อนเขียน, `WriteLockTimeout` แทน `OperationalError` ดิบ

## 6. หลักฐาน -- สองชั้นแยกกัน (เฉพาะชิ้นที่ landed)

### 6.1 client-observable
ศูนย์รอบนี้ -- `grant_learned_skill` ยังไม่มีจุดเรียกจริง (`skill_grant_wiring.learn_and_grant_skill` ของ
LANE-CS เอง zero production caller เหมือนกัน, `runtime.py` ยังไม่มี request handler)

### 6.2 wire-DB
`pirate-force-server#858` -- diff เดียว: `migrations/014_character_skills_learned_source.sql` +
`store.py` + 4 ไฟล์เทส -- ชุดเต็มรัน **สามครั้ง**รอบนี้ (ก่อน merge origin/main รอบสอง, หลัง merge
LANE-Q's lua_api spike): ล่าสุด **11354 passed, 349 skipped, 21056 subtests passed, 0 failed (771.32s)**
`python3 tools_bridge/pf_gate_preflight.py --repo .` เขียวทุกครั้งที่รัน (สี่ครั้ง)

BYTECODE_PURGED: `PYTHONDONTWRITEBYTECODE=1 python3 -B` ทุกคำสั่งรอบนี้

## 7. สถานะ PR

- `pirate-force-server#858` -- เปิดแล้ว ไม่ draft พร้อม `PF-AUTOMERGE: v4` ตั้งแต่เปิด (ยืนยันด้วย GET:
  `state: open`, `draft: false`, marker อยู่ใน body จริง) จากกิ่ง `claude/cool-babbage-qul9wo` -- ไม่ใช่
  PR ที่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมที่ส่งไคลเอนต์ (เมธอดใหม่ยังไม่มีผู้เรียก) จึงไม่ draft --
  commit `2c227c6` -- `mergeable_state: unstable` ตอนเปิด (main ขยับสองครั้งระหว่างรอชุดเต็มรัน -- กิ่งนี้
  merge origin/main เข้าไปแล้วทั้งสองครั้ง preflight ยืนยัน ancestor ทุกครั้ง) ยังไม่ตรวจเกต Windows ตอน
  เขียนบรรทัดนี้
- `pf_bridge#1382` -- claim PR ของรอบนี้ ปลดล็อกพร้อมไฟล์รอบนี้ (ดู §8)

## 8. รอบหน้าทำอะไร

1. **ตรวจคำตอบจาก chief/COO เรื่องใบ `2236`** (guard เควส) -- ถ้า whitelist ได้: เอาโค้ดจาก scratchpad
   กลับมา (`migrations/014_character_quest_state.sql` ต้องเลื่อนเลขเป็นเลขว่างล่าสุดตอนนั้น เพราะ `014`
   ถูก `character_skills_learned_source.sql` จองไปแล้วรอบนี้), เพิ่ม whitelist ตามที่ chief อ่านแล้วอนุมัติ,
   push, เปิด PR ใหม่ -- ถ้า re-grade matrix ก่อน: รอ chief แก้ `docs/COVERAGE_RUNTIME_PROVENANCE_AUDIT_
   20260817.md` แล้วค่อยตาม
2. ตรวจเกต PR `#858` ของรอบนี้ (`GATE_UNVERIFIED` จนกว่าจะตรวจ) เป็นงานแรกถ้าใบ `2236` ยังไม่มีคำตอบ
3. งานคิวเดิม (สแตท/EXP/ของสวม/เควส ตามลำดับ `prompts/LANE-DB.md`) ต่อเมื่อสองข้อบนไม่มีอะไรทำได้

## งานสำรอง (ทำเมื่องานหลักติด)

1. **ปลดแฟล็ก 1 ตัวในเขตตัวเอง** -- ยังไม่มี `docs/PROMOTION_BACKLOG.md` จาก chief ให้เลือก (เช็ครอบนี้:
   ยังไม่ปรากฏบน `origin/main`)
2. เพิ่ม method/เทสของ persistence ที่ `pf-adversary` เคยชี้เป็น debt -- ไม่พบของใหม่รอบนี้นอกจากที่แก้ไป
   แล้วใน §4
3. ตอบใบ RE/STATIC เรื่อง schema/attr ที่ตอบได้จาก `reference_codex_attr` ที่ commit แล้ว -- ไม่มีใบค้าง

## nonclaims

1. **ไม่อ้างว่าประตูสถานะเควสอยู่บน `main` แล้ว** -- โค้ดพร้อมสมบูรณ์และผ่านเทสหมดแต่ตั้งใจไม่ push จนกว่า
   chief จะอ่าน guard ที่มันชน (§4)
2. **ไม่อ้างว่า `grant_learned_skill` มีผู้เรียกจริง** -- zero production caller เหมือนที่ LANE-CS บอกไว้
   เอง
3. **ไม่อ้างว่า COO-DECISION `2058` ทำผิด** -- guard ที่ชนตรวจจับได้จากการรันชุดเต็มจริงเท่านั้น ไม่มีทาง
   รู้ล่วงหน้าจากการอ่านโค้ด
4. **ไม่แตะไฟล์ใดในเขตของสายอื่น** -- ไม่มีการแก้ `runtime.py`/`app.py`/`session.py`/`docs/` รอบนี้ (ใบ ASK
   ถึง chief เสนอทางเลือกที่แตะ `docs/COVERAGE_RUNTIME_PROVENANCE_AUDIT_20260817.md` แต่ไม่ได้แก้เอง)
5. **ไม่เรียก `pf-adversary` ซ้ำเกินโควตา** -- เรียกครั้งเดียวรอบนี้ (ชิ้นเควส) ต่ำกว่าเพดาน 2 ครั้ง/รอบ
6. **ไม่อ้างว่าผู้เล่นเห็นอะไรเปลี่ยนบนจอรอบนี้** -- ทั้งสองชิ้นเป็น persistence door ไร้ผู้เรียก

SCOREBOARD: STUCK | ประตู "เรียนสกิลใหม่" (`grant_learned_skill`) พร้อมใช้จริงในฐานข้อมูลแล้ว แต่ยังไม่มี
จุดเรียกจาก `runtime.py` (ของ chief/LANE-CS) ผู้เล่นยังทำอะไรใหม่ไม่ได้จากรอบนี้ -- ประตูสถานะเควสสำหรับ
LANE-Q เขียนเสร็จสมบูรณ์แล้วเช่นกันแต่ตั้งใจไม่ landed รอ chief อ่าน guard ก่อน | pirate-force-server#858,
commit 2c227c6, pf_bridge#1382, notes_to_chief/20260905_2236_LANE-DB-ASK-COO-*

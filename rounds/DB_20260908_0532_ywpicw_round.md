# LANE-DB รอบ `ywpicw` — เควสต์จ่ายรางวัลได้แล้ว สำหรับตัวละครที่มีอยู่ · และรอบนี้วัดได้ว่า "ตัวละครใหม่" ยังไม่ได้

เริ่ม 2026-09-08T05:32+07:00 · ล็อก `pf_bridge#1862` · กิ่ง `claude/keen-lamport-ywpicw` /
`claude/loving-mccarthy-ywpicw`

## 0. รอบนี้ขยับ NOW/M ข้อไหน
**ขยับ**
- คิวสาย `LANE-DB.md` ข้อ **"สแตท/EXP/ของสวม/เควส"** — `migrations/016` ปลดประตูสองบานที่ปฏิเสธ
  **ทุกแถวในฐานของเจ้าของ**: `store.grant_experience` (`UnmeasuredTypedAttributeError`) และ
  `store.spend_skill_points` (`UnmeasuredSkillPointsError`) · LANE-Q นับจุดเรียกฝั่งเควสต์ไว้ **497 จุดใน 166 สคริปต์**
  (`Quest.AddCriteriaExp` / `AddCriteriaSkillPoint` / `AddCriteriaCash`) ซึ่งวันนี้คืน `refused=store_error` ทุกจุด
- ข้อ 5 ของ "รอบหน้าทำอะไร" ในไฟล์รอบ `r9y8z0` (**birth default ของ `experience`/`skill_points`**) — รอบก่อน
  **ไม่ทำ** เพราะยังไม่รู้ว่า 0 เป็นค่าที่วัดมาหรือเดา · รอบนี้ทำได้เพราะสองสายตอบใบมาแล้ว (ข้อ 2)
- ใบที่สายอื่นส่งมาถึงผมสองใบ — **บริโภคครบ** วาง `.CONSUMED.txt` + สำเนาไป `consumed/` + ตอบเป็นใบ `0633`

**ไม่ขยับ**
- `NOW.md` LANE-DB **"งานแรก = `0025` ข้อ 4 migration อาวุธตัวเก่า"** — รอบ `r9y8z0` เดินจนสุดแล้ว**วัดได้ว่ารันไม่ได้**
  (ต้องมี census `class_id` บน canonical + ประตู `apply_v111_stack_merge` + `#1091` ลง main)
  🔴 ยังติดสามชั้นเดิม ไม่มีอะไรในรอบนี้ปลดมันได้ ⇒ ตาม PANYA `1846` ผมหยิบ **งานถัดไปของสายที่ส่งโค้ดไปหา M final**
  แทน ไม่ใช่จบรอบเปล่า
- `GT-301` (`2336` ห้ามพลิกจน `#1084` ลง main) · `character_equipment` รอ `RE-305` — สถานะเดิม
- `#1104` / `#1115`: **ยังไม่ยืนยันว่าอยู่บน main** (ไม่ได้วัดด้วย `merge-base --is-ancestor` ในรอบนี้ · ข้อ 8)

## 1. งานหลัก — `migrations/016_character_experience_skill_points_backfill.sql`
```
UPDATE characters SET experience   = 0 WHERE experience   IS NULL;
UPDATE characters SET skill_points = 0 WHERE skill_points IS NULL;
```
สองบรรทัดนั้นคือทั้งหมดที่ไฟล์เขียน · ที่เหลือ 396 บรรทัดคือ **เหตุผลกับ guard 7 ตัว**

ไฟล์ที่ส่ง (+1,334 / -23):
- `migrations/016_character_experience_skill_points_backfill.sql` (ใหม่ 398 บรรทัด)
- `tests/test_migration_016_experience_skill_points_backfill.py` (ใหม่ · 33 เทส)
- `src/pirateforce_foundation/persistence_null_audit.py` — `NULL_AUDIT_COLUMNS` เพิ่มสองคอลัมน์ (จ่าย adversary D7)
- `tests/test_persistence_boot_006_to_008.py` · `tests/test_persistence_null_audit.py` ·
  `tests/test_persistence_speed_walk_seed_008.py` — พินของสายผมเอง **เปลี่ยนจาก hardcode เป็น derive** (ข้อ 4)

### 1.1 ทำไม 0 ถึงเป็นค่าที่ "วัดมา" ไม่ใช่ "เดา" (`COO-DECISION 20260901_1059`)
- `experience` — LANE-Q ใบ `0555` ข้อ 1: ไม่มีสคริปต์ใน 616 ไฟล์ที่ **SET** exp มีแต่ **ADD** · ไม่มี `SetExp` ใน API 160 ตัว
  · ไม่มีคอลัมน์ exp ในตาราง CHARCREATE
  🔴 **หลักฐานที่แข็งกว่านั้น ซึ่ง pf-adversary หาเจอ ไม่ใช่ใบไหน**: `data/standard_status.tsv` แถวเลเวล 1 มี
  `n_EXP_CURRENTLV = 0` — ตารางของไคลเอนต์เองเริ่มเส้นที่ศูนย์ · ผมอ้างบรรทัดนี้ในหัวไฟล์แทนที่จะพึ่ง grep
- `skill_points` — **ติดป้าย `[สมมติของสาย LANE-DB - รอ COO ยืนยัน]`** ดูข้อ 2

### 1.2 guard 7 ตัว — มี mutant ที่เรียกชื่อมันทุกตัว
`guard_no_row_changed_outside_the_two_columns` · `guard_only_null_became_zero_in_the_two_columns` ·
`guard_no_null_remains_in_the_two_columns` · `guard_the_schema_is_untouched` ·
`guard_every_index_is_unchanged` · `guard_the_child_rows_all_survived` ·
`guard_every_other_object_is_unchanged`
- `guard_the_schema_is_untouched` เทียบ DDL **byte ต่อ byte** ⇒ `DEFAULT 0` ที่แอบใส่ = แดง · การจำกัดขอบเขตของไฟล์นี้จึงเป็น**การวัด ไม่ใช่คำสัญญาในคอมเมนต์**
- children guard นับ **ทุกตาราง**ที่อ้าง `characters` (7 ตาราง) ไม่ใช่สี่ตารางของ `009` +
  `pragma_foreign_key_check()` · และมีเทสที่ **derive รายชื่อจากสคีมา** ⇒ วันที่สายอื่นเพิ่มตารางลูกตัวที่แปด ไฟล์นี้แดงเอง

## 2. 🔴 ผลวัดที่สำคัญที่สุดของรอบ: เหตุผลของทั้ง LANE-CS และ LANE-Q **ล้มทั้งคู่** — และผมไม่ได้เงียบ
LANE-CS (เจ้าของค่า) เขียนมาว่า `skill_points = 0` ได้ ไม่ต้องติดป้าย เพราะ `LEVEL_SP` เป็นเส้น exp ไม่ใช่แต้มสกิล
โดยยกสองเหตุผล · **ผมวัดแล้วล้มทั้งสอง**:

| เหตุผลของ CS | สิ่งที่วัดได้ | ใครวัด |
|---|---|---|
| "LEVEL_SP เป็นตารางเดียวที่ index ด้วยเลเวล ⇒ ต้องเป็นเส้น exp" | เส้น exp มีอยู่แล้วที่ `data/standard_status.tsv` (`n_EXP_CURRENTLV`) และ `persistence_experience` อ่านอยู่บน main · เทียบ 120 แถว **เหมือนกัน 0 แถว** | ผมเอง |
| "สิบสามล้านไม่มีทางเป็นแต้มสกิล" | `lua_api/quest_criteria_curve.tsv` มีคอลัมน์ `skill_point` สูงสุด **14,252,800** และ `quest_criteria.py:233` เขียนเองว่า "the shipped curve tops out at 14252800" ⇒ เควสต์เลเวล 255 จ่าย SkillPoint สิบสี่ล้าน **ตามตารางที่เกมส่งมา** | pf-adversary (D3) |

```
LEVEL_SP.n_SP                    lv1=2  lv2=4   lv10=42   lv120=13,645,740
STANDARD_STATUS.n_EXP_CURRENTLV  lv1=0  lv2=79  lv10=714  lv120=91,699,378
identical rows out of 120: 0
```

⇒ **`LEVEL_SP` คือตารางที่ index ด้วยเลเวล และไม่ใช่เส้น exp · มันคืออะไรยังไม่มีใครวัด**
⇒ ผม **คืนป้ายสมมติ** ให้ `skill_points = 0` ตามที่ LANE-Q ขอไว้แต่แรก แม้เจ้าของค่าจะบอกว่าไม่ต้อง —
เพราะเหตุผลที่เจ้าของค่าใช้ยกป้ายออกนั้นล้มไปแล้ว · เขียนไว้ในหัวไฟล์ migration และในใบ `0633`
🔴 ป้ายอยู่ที่ **ตัวเลข** ไม่ใช่เหตุผลกักไฟล์: ทุกแถวถือ NULL วันนี้ ⇒ ไม่มีอะไรที่ใครวัดมาแล้วถูกเขียนทับ

## 3. 🔴 ราคาที่รอบนี้จ่าย และไม่ซ่อน: ตัวละครที่เกิด **หลัง** 016 ยังโดนปฏิเสธเหมือนเดิม
เวอร์ชันแรกของ 016 เป็น rebuild แบบ `009` + `DEFAULT 0` (10 guard · 45 เทส เขียนเสร็จจริง) แล้วชุดใหญ่ตอบว่า:
```
39 failed  (30 อยู่ที่ fixture เดียว: tests/pf_birth_state.py)
"an insertion point that adds a FIFTH column turns every file that imports this one red at its fixture"
```
`pf_birth_state.py` ประกาศ **สามสภาพ**ที่ตัวละครเกิดใหม่ถือได้ และปฏิเสธอย่างอื่นโดยเจตนา · DEFAULT บนสองคอลัมน์นี้
คือคอลัมน์ที่ห้าและหก · NOW.md `2050` = **พินปลดโดยเจ้าของ ผู้เรียกถอน** ⇒ ผมถอน DEFAULT ออก เหลือ backfill
(และ `COO-DECISION 20260902_1607` ที่อนุญาต DEFAULT เลย คือเจ้าของเคาะเองในเซสชัน ระบุ **สี่**คอลัมน์)

pf-adversary (D1) วัดผลของการถอนให้เห็นตรง ๆ:
```
pre-016 character  grant_experience -> OK       spend_skill_points -> OK
born after 016     grant_experience -> REFUSES  spend_skill_points -> REFUSES
```
🔴 และชี้ว่านี่คือรูปเดียวกับที่ `009` เขียนไว้เองว่าเป็นความผิดพลาดของ `007`/`008` (*"seeded the cohort that
existed when they ran and can never run again"*) — **016 คือ cohort seed แบบนั้น โดยรู้ตัว** เขียนไว้ในหัวไฟล์แล้ว

**สิ่งที่ผมทำแทนการเงียบ** (ในรอบเดียวกัน): `persistence_null_audit.NULL_AUDIT_COLUMNS` เดิมนับ NULL แค่สี่คอลัมน์
· เพิ่มสองคอลัมน์นี้เข้าไป ⇒ ระหว่างรอ COO เคาะ **จำนวนตัวละครใหม่ที่ถือ NULL นับได้** ไม่ใช่ตัวเลขที่ไม่มีใครเห็น
(เทสของไฟล์นั้นเขียนคำสั่งนี้ไว้เองอยู่แล้ว: *"a migration assigns a typed column that NULL_AUDIT_COLUMNS does
not audit ... this count would not see them"*)

## 4. พินที่ล้าสมัยสามจุด — แก้เป็น derive ไม่ใช่เติมตัวเลขใหม่
| ไฟล์ | เดิม | ตอนนี้ |
|---|---|---|
| `test_persistence_speed_walk_seed_008.py` | `[8,9,...,15]` พิมพ์มือ · **ถูกเขียนใหม่โดยเจ็ดรอบติดกัน** | derive จาก `migrations/` |
| `test_persistence_boot_006_to_008.py` | `_expected()` ตรึงสี่คอลัมน์ · helper `_typed_columns_seeded_by_lane_migrations()` เขียนไว้เพื่อวันนี้พอดี **แต่ไม่เคยถูกเรียก** | ต่อสายให้เรียกจริง + อ่านค่าจากไฟล์ migration |
| `test_persistence_null_audit.py` | `defaulted == NULL_AUDIT_COLUMNS` | `defaulted | assigned` (พี่น้องของมันใช้รูปนี้อยู่แล้ว) + assertion กันตัวเองเป็นโมฆะ |
🔴 ไม่มีพินของสายอื่นถูกแตะเลย · `EXPECTED_TABLES` ของ `test_npc_interaction_wire.py` = ผมถอนของผมออกแทน (ข้อ 5)

## 5. ของที่ผมถอนออกจาก PR เอง (ไม่ใช่ของที่ทำไม่ทัน)
ผมเขียนตาราง `migration_backfill_audit` + guard + เมธอด read-only ใน `store.py` + โมดูล `persistence_migration_audit`
เพื่อบันทึก "backfill แตะกี่แถว" ตามที่ LANE-Q ขอ · แล้ว `EXPECTED_TABLES` ปฏิเสธ:
`AssertionError: Items in the first set but not the second: 'migration_backfill_audit'`
ทุกตารางที่เคยเข้าเซ็ตนั้นอ้างใบ COO/PANYA ที่สั่งให้มี · ของผมไม่มีใครสั่ง ⇒ **`2050`: ผู้เรียกถอน** ถอนทั้งก้อน
- ย้อนได้ไหมถ้าไม่มีตาราง? **ได้** — snapshot ก่อน apply มีจริงและวัดแล้ว (ข้อ 6) เก็บทุกแถวก่อน 016 ครบ
- ขอทางเดินจาก COO ในใบ `0632` · **งานแรกรอบหน้า** = reader ที่ derive จาก snapshot เทียบฐานสด (ไม่ต้องมีตารางใหม่)
- pf-adversary (D2) จับได้ว่า guard ของตารางนั้น**เทียบกับสำเนาของตัวเอง**: mutant ที่ย้ายการนับไปหลัง UPDATE
  ผ่าน guard ครบแล้วรายงาน `rows_backfilled=0` ทั้งที่เขียน 3 แถว ⇒ ถ้า COO ให้กลับมา ต้องเทียบ `changes()` ก่อน

## 6. หลักฐานสองชั้น (แยกกัน ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น)
**ชั้น DB/wire — ประตูเปลี่ยนชนิดคำปฏิเสธ** (`TheDoorsThatRefusedEveryRowTests`)
```
ก่อน 016: spend_skill_points -> UnmeasuredSkillPointsError      ("ไม่มีใครวัด")
หลัง 016: spend_skill_points -> InsufficientSkillPointsError    ("ยอดไม่พอ")
ก่อน 016: grant_experience   -> UnmeasuredTypedAttributeError
หลัง 016: grant_experience   -> จ่ายจริง แถวขยับ 0 -> 10 · veteran 39 -> 44 (ค่าเดิมไม่ถูกรีเซ็ต)
```
**ชั้น backup — วัดสด ไม่ใช่อ่าน docstring** (pf-adversary ยืนยันอิสระ)
```
should_snapshot -> (True, 'pending migrations: 016')
snapshot path   -> .../db_backups/20260907T2253..Z_premigration_state/state.sqlite3
snapshot ledger -> [1..15]   (ไฟล์จริงบนดิสก์ ถือสคีมาก่อน 016)
ผู้เรียกบนเส้นบูต: app.py:791 และ app.py:794 (ทั้งสองสาขาที่ migrate)
```
🔴 ผมตั้งโจทย์ให้ adversary ไปพิสูจน์ว่า "migration นี้จะรันโดยไม่มี backup" — **พิสูจน์ไม่ได้** เป็นผลลบที่มีค่า
**ยังไม่มีชั้น client-observable**: ไม่มีใครบูตไคลเอนต์กับ 016 ในรอบนี้ ⇒ ไม่อ้างว่าผู้เล่นเห็นอะไรบนจอ

## 7. จดหมายรอบนี้
- `20260908_0631_LANE-DB-ASK-COO-may-016-give-experience-and-skill-points-a-birth-default.md` (ADDRESSEE: COO)
- `20260908_0632_LANE-DB-ASK-COO-may-a-backfill-record-its-own-row-count.md` (ADDRESSEE: COO)
- `20260908_0633_LANE-DB-TO-CS-AND-Q-both-your-arguments-about-LEVEL-SP-are-measurably-wrong.md` (ADDRESSEE: LANE-CS)
- บริโภคใบ CS `0458` และใบ Q `0555`: วาง `.CONSUMED.txt` แล้ว (ทั้งสองไฟล์อยู่ใน commit)
  🔴 สำเนาไป `consumed/` **ทำแล้วแต่ไม่ขึ้น git** — `consumed/` ถูก .gitignore และไม่มีบน `origin/main`
  ⇒ ต้นฉบับยังอยู่ครบใน `notes_to_chief/` ตามกฎ (ห้ามลบต้นฉบับ) · แจ้ง COO ไว้ว่าขั้นตอน "สำเนาไป consumed/"
  ในกฎบ้านใช้ไม่ได้จริงบนโคลนคลาวด์ ถ้าตั้งใจให้เก็บถาวรต้องเอาโฟลเดอร์นั้นออกจาก .gitignore

## 8. สถานะ PR (ตามจริง)
- **`pirate-force-server#1123`** — เปิดแล้ว ไม่ draft · body มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด ·
  **ยังไม่อยู่บน main** (รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`)
- `pf_bridge#1862` — ล็อกของรอบนี้
- `#1115` / `#1104` ของรอบก่อน: **ยังไม่ยืนยันว่าอยู่บน main** ไม่ได้วัดในรอบนี้
- ป้ายเวลา: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `06:16` เทียบเวลาตรวจ `06:31` = ห่าง **15 นาที** (ปกติ)

## 9. รอบหน้าทำอะไร (เรียงตามลำดับ ห้ามสลับ)
1. **ยืนยัน 016 อยู่บน main** (`merge-base --is-ancestor`) แล้วอ่านคำตอบใบ `0631` — ถ้า COO ให้ไฟเขียว
   **ออก `017` ใส่ DEFAULT ทันที** (guard 10 ตัวเขียนและพิสูจน์ไว้แล้วในรอบนี้ ไม่ต้องเริ่มใหม่)
2. **reader ที่นับ backfill จาก snapshot เทียบฐานสด** (ใบ `0632` ทาง 2) — ไม่มีตารางใหม่ ไม่ชนพินใคร
3. หนี้ adversary ที่ยังไม่จ่าย: **D2** (ถ้า COO เลือกทาง 1 ของใบ `0632`) · **D12** ลำดับเวลาใบ CS/Q
4. งานอาวุธตัวเก่า (`0025` ข้อ 4) — ยังติดสามชั้นเดิมจาก `r9y8z0` ข้อ 9: census `class_id` บน canonical (ใบ attended
   อ่านอย่างเดียว) · ประตู `apply_v111_stack_merge` · `#1091` ลง main
5. หนี้เก่า: `character_equipment` รอ `RE-305` · adversary `#1699`/`ueaey7` · `#1781`/`kq4m8t`

## 9.1 pf-adversary — **คืนก่อน push และไม่สะอาด ⇒ จ่ายในรอบนี้**
เรียกครั้งเดียว (เพดาน 2) · สั่งตอนต้นรอบตามกฎ · **รับ+แก้ 5 ข้อ · moot 5 ข้อ · บันทึกเป็นหนี้ 2 ข้อ**

| # | สิ่งที่ชี้ | จ่ายยังไง |
|---|---|---|
| **D1** | 🔴 หัวไฟล์อ้างว่า "this file is the only thing standing between it and a quest that pays" — **เท็จสำหรับตัวละครที่เกิดหลัง 016** | เขียนหัวไฟล์ใหม่ ใส่ตารางผลวัดของเขาเอง + อ้าง `009` ที่เตือนเรื่องนี้ไว้เอง + ออกใบ `0631` ถึง COO |
| **D3** | 🔴 ข้ออ้าง "สิบสามล้านไม่ใช่แต้มสกิล" ล้ม — `quest_criteria_curve.tsv` มี `skill_point` สูงสุด 14,252,800 | แก้หัวไฟล์ (เดิมเขียนว่าข้อแรกของ CS รอด) + คืนป้ายสมมติ + ใบ `0633` |
| **D4** | หา `standard_status.tsv` lv1 `n_EXP_CURRENTLV = 0` ให้ — แข็งกว่า lua-grep ที่ผมอ้าง · และ Q นับตาราง CHARCREATE ผิด (สี่ vs หก) | ใส่บรรทัดนั้นในหัวไฟล์ + บันทึกการนับผิด (ข้อสรุปยังถูก) |
| **D7** | `NULL_AUDIT_COLUMNS` ไม่นับสองคอลัมน์นี้ ⇒ รวมกับ D1 = NULL ของตัวละครใหม่สะสมโดยมองไม่เห็น | เพิ่มสองคอลัมน์ + `SKILL_POINTS_X`/`EXPERIENCE_X` + เทสที่เทียบกับตัวไฟล์ migration |
| **D11** | `test_every_guard_..._has_a_mutant` ตรวจแค่ `name not in source` ⇒ เขาเพิ่ม guard ใหม่ + เขียนชื่อไว้ใน **คอมเมนต์** แล้วผ่าน | ตรวจว่าชื่อต้องเป็นอาร์กิวเมนต์แรกของ `self._refuses(` จริง + จับ mutant ที่ชี้ guard ที่ไม่มีแล้ว |
| **D5** | คำสั่ง `-k` ที่ผมใช้ตอนต้นเป็น false-green พลาด regression 3 ตัว | ขยาย `-k` แล้วเจอครบ · และรันชุดเต็มบนต้นไม้สุดท้าย (ข้อ 12) |
| D2 · D8 · D9 · D10 · D6(บางส่วน) | ล้วนเกี่ยวกับ `migration_backfill_audit` / เวอร์ชัน rebuild / ไฟล์เทสที่ยังไม่อัปเดต | **moot** — ถอนตารางและโมดูลออกแล้ว (ข้อ 5) และไฟล์เทสอัปเดตแล้วก่อน push |
| **D12** | ใบ CS ประทับ `04:58` แต่เขียนว่า "ตอบใบ `0555`" | **หนี้** — บันทึกในใบ `0633` ข้อ 4 ไม่เดาว่านาฬิกาใครผิด |

**ผลลบของ adversary ที่ทำให้รอบนี้ถูกขึ้น** (ยกมาเพราะมีค่าเท่ากับ finding):
- **mutant การเขียนแถว 13/13 ถูกจับ พร้อมชื่อ guard ที่ถูกต้อง** — ตัด WHERE, เขียน 1 แทน 0, ข้ามแถว soft-deleted,
  ลืม `skill_points`, แตะคอลัมน์ที่สาม, ขยับ `updated_at`, เพิ่มคอลัมน์, ลบ index, ลบแถวลูก, ลบแถวตัวละคร
  **เขาหา mutant ของการเขียนแถวที่รอดไม่ได้เลย**
- เส้น backup มีจริงและทำงาน (ข้อ 6) · idempotency + checksum ledger ผ่านทุกฉาก (ว่าง / NULL หมด / มีค่าหมด / ปน)
  · ข้อความ checksum ชี้ชื่อไฟล์จริง · scratch table 14 CREATE / 14 DROP ไม่รั่ว
- แถว `deleted_at IS NOT NULL` ถูก backfill จริงตามที่ไฟล์เขียนว่าทำ · mutant ที่เติม `AND deleted_at IS NULL` ถูกจับ
- fixture สามชิ้นมีฟันจริง: ลบตัวละคร "Zero" (ค่า 0 จริง) -> 5 แดง · ลบ "Veteran" -> 6 แดง · ตัด soft-delete -> 4 แดง
- เวอร์ชัน rebuild ที่ถูกทิ้ง: กับดัก prefix `DEFAULT0` ของ `009` ถูกจัดการถูกต้อง (`identity_hi` มี `DEFAULT0` มาตั้งแต่ `004`
  ⇒ วิธีลบแบบ `009` ใช้ไม่ได้จริง · วิธี "แทรกเข้า before-text" ที่ผมเลือกทำงานถูกและ pin ตำแหน่งด้วย)

`TWO_SESSIONS_SAME_SCENE:` **ไม่เกี่ยวกับฉากร่วม** — 016 ไม่ปล่อยเฟรมใด ไม่แตะ registry ของ A และแถว `characters`
คีย์ด้วย `character_id` ล้วน ไม่มี `session_id` · **แต่มีประเด็นสองเซสชันจริงแบบเดียวกับ `r9y8z0` D12**: migration รัน
ตอนบูตก่อนรับ connection ⇒ ไม่มีเซสชันถือค่าเก่าในหน่วยความจำขณะเขียน · ถ้ามีใครรันตอน server เปิดอยู่ ค่านั้นจะไม่ตรง

## 10. nonclaims
- **ไม่อ้าง**ว่าผู้เล่นเห็นอะไรใหม่บนจอวันนี้ · ไม่มีใครบูตไคลเอนต์ในรอบนี้ · ไม่มีใบ attended ในรอบนี้
- **ไม่อ้าง**ว่า `skill_points = 0` ถูก — ติดป้ายสมมติ · **ไม่อ้าง**ว่า `LEVEL_SP` คือตารางแต้มสกิล
  อ้างว่า**ข้อพิสูจน์ว่ามันไม่ใช่ ล้มทั้งสองข้อ**
- **ไม่อ้าง**ว่าเควสต์จ่ายรางวัลให้ตัวละครที่สร้างใหม่ได้ — **วัดแล้วว่าไม่ได้** (ข้อ 3)
- **ไม่อ้าง**ว่า 016 รันบนฐานจริงของเจ้าของแล้ว · ทดสอบบนฐานชั่วคราวเท่านั้น · ไม่แตะ canonical DB
- ไม่แตะ `runtime.py`/`app.py`/`gm/` · ไม่แตะ `v141` · ไม่แก้ migration ที่ apply แล้ว ·
  ไม่เปลี่ยน behavior ของ method เดิมใน `store.py` สักตัว (รอบนี้ **ไม่แตะ `store.py` เลย** — เมธอดที่เขียนไว้ถูกถอน)
- ไม่มี binary ในคลาวด์ · ทุกตัวเลขตาราง grep จากไฟล์ที่ commit แล้วในสองรีโป

## 11. เวลา
เริ่ม `05:32` · เขียนไฟล์รอบ `06:3x` — **อยู่ในงบ 75 นาที** · pf-adversary กิน ~49 นาทีขนานไปกับการเขียนโค้ด
และ **คืนก่อน push** ⇒ เลือก "แก้ให้ถูกแล้วค่อย push" แทน `ADVERSARY_PENDING` เหมือนรอบ `r9y8z0`
รอบนี้เสียเวลาไปกับการเขียนเวอร์ชัน rebuild ทิ้ง (~30 นาที) — **ไม่เสียเปล่า**: guard 10 ตัวและคำตอบว่าพินไหนห้าม
คือของที่รอบหน้าหยิบไปใช้ได้ทันทีถ้า COO ตอบว่าไปต่อ

## 12. ตัวเลขสุดท้ายบนต้นไม้ที่ push
- ชุดเต็มหลัง `git merge origin/main` **บนคอมมิตที่ push จริง** (`69510be`):
  **14525 passed · 446 skipped · 0 failed · 42186 subtests · 692.60 s**
  (`pytest tests/ -q -p no:cacheprovider`)
  🔴 รันสองครั้ง: ครั้งแรกจบก่อนผมแก้ชื่อใบในคอมเมนต์ของ migration จึงไม่ใช่ต้นไม้ที่ push
  ⇒ รันใหม่ทั้งชุดบนคอมมิตสุดท้าย ตัวเลขตรงกันทั้งสองครั้ง
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
  (cp874 + no new skips + main is in this branch + precondition census agrees + mergeable + ...)
- ไฟล์เทสของรอบ: `tests/test_migration_016_experience_skill_points_backfill.py` **33 passed**
- 446 skipped สูงกว่ารอบ `r9y8z0` (436) เพราะ merge main เอาไฟล์ของสายอื่นเข้ามา — preflight ยืนยัน
  **no new skips** จากกิ่งนี้

SCOREBOARD: COMING | ตัวละครทุกตัวที่มีอยู่ในฐานของเจ้าของ "รับรางวัลจากเควสต์ได้" แล้ว ซึ่งเมื่อวานทำไม่ได้เลยสักตัว: ทุกแถวถือ NULL ใน experience/skill_points อยู่ ประตูจ่ายรางวัลสองบานจึงปฏิเสธทุกคนด้วยเหตุผล "ไม่มีใครวัดค่านี้" และจุดเรียกฝั่งเควสต์ 497 จุดใน 166 สคริปต์คืน refused=store_error ทั้งหมด · migration 016 เขียน 0 ทับ NULL ให้แถวที่มีอยู่ (ไม่แตะสคีมา ไม่แตะแถวที่มีค่าอยู่แล้ว มี snapshot อัตโนมัติก่อนเขียน) ⇒ คำปฏิเสธเปลี่ยนชนิดจาก "ไม่มีใครวัด" เป็น "ยอดไม่พอ" ซึ่งเป็นคำตอบปกติของระบบรางวัล และการจ่าย exp จริงทำให้แถวขยับ · 🔴 ตัวละครที่สร้าง *หลัง* 016 ยังไม่ได้ เพราะครึ่งที่ต้องใส่ DEFAULT ชนพิน pf_birth_state ที่เจ้าของพินต้องปลด — วัดไว้ ไม่ซ่อน และเพิ่มเครื่องนับ NULL ให้เห็นประชากรกลุ่มนั้นระหว่างรอ COO เคาะ | `pirate-force-server#1123` (เปิดแล้ว ไม่ draft มี marker ยืนยันด้วย GET · ยังไม่อยู่บน main) · `pf_bridge#1862` · ชุดเต็ม 14525 passed / 0 failed บน `69510be` · PREFLIGHT PASS · pf-adversary คืนก่อน push ไม่สะอาด จ่าย 5 รับเป็นหนี้ 2 และ D1/D3 หักข้ออ้างของรอบนี้เอง

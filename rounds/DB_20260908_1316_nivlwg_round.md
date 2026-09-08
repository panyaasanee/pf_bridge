# LANE-DB รอบ `nivlwg` — `017` ออกแล้ว: ตัวละครที่เกิดวันนี้ "รับรางวัลเควสได้" · และพิน `pf_birth_state` เลิกเป็นรายการคอลัมน์

เริ่ม 2026-09-08T13:16+07:00 · ล็อก `pf_bridge#1893` · กิ่ง `claude/beautiful-bohr-nivlwg` /
`claude/cool-bohr-nivlwg` · PR เซิร์ฟเวอร์ `pirate-force-server#1141`

## 0. รอบนี้ขยับ NOW/M ข้อไหน
**ขยับ**
- `NOW.md` LANE-DB **"งานแรก = `017` + พิน `pf_birth_state` เป็น logic จาก schema PR เดียว (`1218`)"** — ทำครบทั้งสองครึ่งใน PR เดียวตามสั่ง
- บริโภคใบ `1246` (COO-DECISION ถึงสายผมโดยตรง) · ใบ `1218` เป็น ALL-LANES ⇒ ตาม NOW `0442` ไม่วาง stub ร่วม อ้างเลขที่นี่แทน

**ไม่ขยับ**
- ประตู `apply_v111_stack_merge` — ยังรอ `0206` ลง main (`1246` สั่งห้ามดันก่อน) · โค้ดอยู่ที่ `git show ebdad7c`
- `STARTING_BACKPACKS` 5 ใบ — รอ CS ปลดพิน importer
- `GT-301` (`2336`) · `character_equipment` รอ `RE-305` · `0x309A` RE-blocked

## 1. งานที่ส่ง — `migrations/017_character_experience_skill_points_birth_defaults.sql`
rebuild `characters` ให้ `experience` และ `skill_points` มี `DEFAULT 0` (SQLite ไม่มีทางอื่นที่จะติด DEFAULT
ให้คอลัมน์ที่มีอยู่แล้ว) · guard 7 ตัว ชื่อ CONSTRAINT ละตัว · mutant ต่อ guard ครบทุกตัว (เทส 38 ตัวเขียว)

**ทำไมสำคัญกับผู้เล่น**: `016` เขียน 0 ทับ NULL ของ "แถวที่มีอยู่" เท่านั้น และหัวไฟล์ของมันเขียนไว้เองว่า
ตัวละครที่เกิดหลังจากนั้นยังถือ NULL และยังโดน `store.grant_experience` / `store.spend_skill_points` ปฏิเสธ
(LANE-Q นับจุดเรียก 497 จุดใน 166 สคริปต์เควสหลังประตูสองบานนั้น) · `017` คือครึ่งที่ปิดช่องนั้น

## 1.1 🔴 ผลวัดที่สำคัญที่สุดของรอบ: rebuild แบบไม่ปิด foreign key **ลบของผู้เล่นทิ้ง** และหาไม่เจอ
ดราฟต์แรกของผมลอกโครง `009` มาแต่ **ตกสามบรรทัด** ที่ `009` มีอยู่และหัวไฟล์ของ `009` ไม่ได้อธิบายว่าทำไม:
```
COMMIT;
PRAGMA foreign_keys=OFF;
BEGIN IMMEDIATE;
```
วัดบนฐานที่ migrate ถึง `016` จริง มีตัวละครหนึ่งตัว:
```
ก่อน:  character_positions=1  character_backpacks=1  character_backpack_items=4
หลัง:  character_positions=0  character_backpacks=0  character_backpack_items=0   (ตาราง characters ครบทุกแถว)
```
`DROP TABLE characters` ทำ implicit `DELETE FROM` → `ON DELETE CASCADE` ของ `character_positions`/
`character_backpacks` ยิง → หลานที่ห้อยอยู่ (`character_backpack_items`) ไปด้วย · **และหลังจากนั้นไม่มีอะไร
"orphaned" ให้ตรวจเจอ เพราะไม่เหลืออะไรเลย** — ซึ่งคือเหตุผลที่ guard 5 ต้องนับ "ผู้รอดชีวิต" ไม่ใช่ถาม orphan
(คำเตือนที่ `009` เขียนไว้เองหลัง adversary รอบก่อน · รอบนี้เป็นครั้งแรกที่มีตัวเลขวัดจริงประกอบ)
🔴 guard 5 จับได้และ rollback ⇒ อาการที่ผู้ใช้เจอคือ "เซิร์ฟเวอร์บูตไม่ขึ้น" ไม่ใช่ "ของหาย" แต่ migration ที่
ทำได้อย่างเดียวคือล้มเหลว ไม่ใช่ migration · แก้แล้ว + mutant `test_a_rebuild_that_leaves_the_foreign_keys_on_is_refused`
🔴 ผลข้างเคียงที่บันทึกไว้ให้รอบหน้า: `PRAGMA foreign_keys` ยัง **OFF** ตลอดอายุคอนเนกชันของ `migrate()` นั้น
(เป็นพฤติกรรมเดิมของ `009` ที่ `010`-`016` รันตามมาแล้ว) · ไฟล์ที่จะเป็น `018` ต้องรู้ข้อนี้

## 1.2 guard 6 ไม่ใช่สเปลลิงเดียวกับ `009` — และเหตุผลวัดได้
`009` ลบ DEFAULT ของตัวเองออกจากฝั่งหลังด้วย `replace('DEFAULT1','')` และคอมเมนต์ของมันเองบอกว่าลำดับ
สำคัญเพราะ `DEFAULT1` เป็น prefix ของ `DEFAULT100` · ของผมข้อความคือ `DEFAULT0` และ **`identity_hi`
มี `DEFAULT 0` อยู่แล้วตั้งแต่ `004`** ⇒ `replace('DEFAULT0','')` แบบตรงไปตรงมาจะลบ default ที่ไฟล์นี้ห้ามแตะ
ออกจาก **ทั้งสองฝั่ง** แล้วเขียวทับการสูญหายของมัน · จึงลบแบบระบุชื่อคอลัมน์
(`experienceINTEGERDEFAULT0` -> `experienceINTEGER`) · mutant
`test_a_rebuild_that_moves_another_columns_default_is_refused` คือตัวที่พิสูจน์

## 2. ครึ่งที่สอง — `tests/pf_birth_state.py` เลิกเป็น "สามสภาพ/สี่คอลัมน์"
คำสั่งเจ้าของ (`1218` ข้อ 3 คำต่อคำ): "จงทำให้เป็น logic ที่ถูก" · สภาพเกิดตอนนี้ **วัดจากฐานตรงหน้า**:
คอลัมน์ typed ที่มี DEFAULT ใน `PRAGMA table_info('characters')` + คอลัมน์ที่ `store.create_character` เขียนชื่อ
(อ่านจากซอร์สจริงด้วย `inspect`) · migration ที่เพิ่มคอลัมน์เกิดที่เจ็ดจึงไม่ใช่เหตุการณ์ในไฟล์นี้อีกต่อไป

🔴 **ที่ไม่ได้อ่อนลง** (ประเด็นที่ adversary จะยิงก่อน และผมตอบไว้ในโค้ด): พินถามสองคำถามแยกกัน
1. **แถวตรงกับสคีมาไหม** — สถานะที่วัดได้ต้อง **เท่ากันเป๊ะ** ไม่ใช่ superset/subset · plug ที่เขียน `level = 0`
   หรือเขียนเลขที่สคีมาไม่ได้ประกาศ หรือถูกเฉพาะตัวแรกแล้วตัวที่สองผิด = แดงเหมือนเดิม
   **ไม่ใช่ตรรกะวงกลม**: เทียบ "แถว" กับ "สคีมา" ซึ่งเขียนโดยไฟล์คนละไฟล์
2. **สคีมาตรงกับโมดูลที่เป็นเจ้าของเลขไหม** — เฉพาะคอลัมน์ที่มีโมดูลใน `src/` เป็นเจ้าของค่า
   (สามไวทัลจาก `persistence_vitals.new_character_vitals()` · `speed_walk` จาก
   `CLIENT_CONSTRUCTION_DEFAULTS[7]`) · **ข้อนี้ไม่ได้ derive จากสคีมา** ⇒ migration ที่แอบเปลี่ยน DEFAULT
   ของ `level` เป็น 0 แดงที่นี่ · คอลัมน์ที่ไม่มีโมดูลเป็นเจ้าของเลข (เช่น `experience`/`skill_points`) = เงียบ
   ซึ่งคือช่องที่เจ้าของสั่งให้เปิดไว้เอง ("ไม่ต้องขออนุญาตใครอีก")

## 3. ค่าใช้จ่ายที่วัดแล้ว: 82 เทสแดง → 0 · และไม่มีสักตัวที่เป็นไฟล์ของสายอื่น
`016` เคยรายงานว่า rebuild ทำ 39 แดง · วัดจริงบน main วันนี้ = **82 แดง** (ชุดของไฟล์ที่ import พินนี้)
หลังเขียนพินใหม่เหลือ 12 แล้วจ่ายครบเป็น 0 · **ทุกไฟล์ที่แก้เป็นของ LANE-DB ทั้งหมด**:
`test_persistence_boot_006_to_008` · `test_persistence_typed_attr_columns` · `test_persistence_attr_compose` ·
`test_persistence_null_audit` · `test_persistence_experience` · `test_persistence_vitals_seed_007` ·
`test_persistence_birth_defaults_009` · `test_migration_016_*`
- ที่ไหนแก้ **นับ** เป็น **derive**: `assertEqual(len(unadjudicated), 17)` -> "คอลัมน์ที่ยังไม่มีใครตัดสิน
  ต้องไม่มี DEFAULT ในสคีมา และต้องไม่โผล่ในแถวเด็กเกิดใหม่" (วัดกับฐาน ไม่ใช่นับ)
- `_FakeStore` ของ boot test **ประกาศสคีมาของตัวเอง** แล้ว (ฐานต่ำกว่า 009 = ประกาศศูนย์ default)
- ประตู fail-closed ที่ "เอื้อมไม่ถึงอีกแล้ว" เพราะ 017: เพิ่ม `clear_columns_to_null` ให้ **สร้างสภาพนั้นตั้งใจ**
  แทนที่จะได้มาโดยบังเอิญ (`test_a_null_experience_is_refused_by_name`) — 🔴 **ไม่ skip ไม่ xfail ไม่ allowlist**

## 4. หลักฐานสองชั้น (แยกกัน ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น)
**ชั้น DB — แถวจริงบน sqlite ที่ migrate ด้วย `migrations/` จริง (ไม่ใช่ตารางที่เขียนมือ)**
```
ฐานหยุดที่ 016 -> สร้าง 4 ตัวละคร (0 ที่ backfill แล้ว / เลขจริง / NULL ที่สร้างมือ / ศพ soft-deleted)
apply 017 -> ทุกแถวเดิมเท่าเดิมทุกคอลัมน์  NULL ที่สร้างมือยัง NULL  ศพยังเป็นศพ  ลูกครบทุกตาราง
สร้างตัวละครใหม่หลัง 017 -> (experience, skill_points) = (0, 0)
grant_experience(newborn, 1) -> ผ่าน แถวเป็น 1     spend_skill_points(newborn, 1) -> ปฏิเสธด้วยเหตุ "จ่ายไม่ไหว" ไม่ใช่ "ไม่เคยวัด"
```
**ชั้น mutant — guard ทุกตัวเคยล้มจริง** 11 mutant · ทุกตัวต้องถูกปฏิเสธ **ด้วยชื่อ guard ที่ถูกต้อง**
และฐานต้องยังถือตารางเดิม (mutant ที่ถูกจับด้วย SQL error หรือถูก guard ผิดตัวจับ = เทสแดง ไม่ใช่ติ๊กเขียว)
🔴 **ไม่มีชั้น client-observable**: ไม่มีใครบูตไคลเอนต์ในรอบนี้ · **ไม่อ้างว่าผู้เล่นเห็นอะไรบนจอวันนี้**

## 5. เกตและชุดเทส
- `git merge origin/main` เข้ากิ่งเป็นขั้นสุดท้ายแล้ว (รับ `skill_point_curve.py` ของ CS เข้ามาด้วย)
- ชุดเต็ม / preflight: ดูข้อ 8

## 6. `pf-adversary` — **คืนก่อนปลดล็อก และไม่สะอาด ⇒ จ่ายในรอบนี้ทั้งหมด**
เรียกครั้งเดียว (เพดาน 2) สั่งตอนต้นรอบพร้อมเริ่มงานตามกฎ · เขาสร้าง worktree ของตัวเอง ไม่แตะ checkout ผม
· วัดบนฐานรูปเดียวกับเจ้าของ (หยุดที่ `016` มีแถวจริง ศพ NULL และลูกครบเจ็ดตาราง) ไม่ใช่ฐานเปล่า

| # | สิ่งที่ชี้ | จ่ายยังไง |
|---|---|---|
| **D1** | 🔴 guard 7 ยกเว้น `LIKE '_pf_mig017_%'` **ทั้งสองฝั่ง** ⇒ วัตถุถาวรที่ใช้ prefix ของไฟล์เอง **ล่องหน** · เขาปลูก **trigger** `_pf_mig017_trg` ที่เขียน `experience` กลับเป็น 0 ทุก UPDATE — **ผ่าน guard ทั้งเจ็ดเขียว** แล้ว `grant_experience(1, 500)` คืน `ExperienceGain(level 1->4, experience_after=0)` = รางวัลเควสถูกกินเงียบ ๆ ตลอดกาล พร้อมค่าคืนที่บอกว่าจ่ายแล้ว | **แก้ guard 7 ให้ยกเว้นทีละชื่อ 13 ตาราง** ไม่ใช่ prefix + mutant `test_a_stray_object_named_with_this_files_own_prefix_is_refused` (ใช้ชื่อ prefix จริง) + เขียนเหตุลงหัวไฟล์ |
| **D4** | 🔴 พินข้อ 2 **เท็จสำหรับ 3 ใน 4 คอลัมน์ที่มันอ้าง** — `_check_schema_against_the_modules(expected)` รับ dict ที่ overlay ด้วย `seeded_birth()` ไปแล้ว ⇒ เทียบ `new_character_vitals()` กับตัวมันเอง · เขาขับ `level=0`, `hp_max=1` ผ่านเขียว (`speed_walk` รอดเพราะไม่อยู่ใน overlay) | ส่ง **`_schema_defaults(store)` ดิบ** เข้า check แทน |
| **D5** | 🔴 "ค่าที่เขียนถูกไหม" ไม่ได้เข้มจริงสำหรับสองคอลัมน์ที่รอบนี้เพิ่ม — `018` ที่ตั้ง `skill_points=1`/`experience=5`/ให้ `cash` มี default ผ่านหมด · และ **`experience` มีเจ้าของเลขอยู่แล้ว** (`standard_status.tsv` ที่หัวไฟล์ `017` เองอ้างว่า MEASURED) แต่ผมไม่ได้ให้พินอ่าน | ให้ `_adjudicated_birth_values()` อ่าน `standard_status_row(1).exp_currentlv` ⇒ `experience` ถูกเกรดจริง · `skill_points` ยังไม่มีเจ้าของ ⇒ ดู D3 |
| **D3** | 🔴 พินที่ derive **มองไม่เห็นการถอน `017`** — `018` ที่ถอด DEFAULT ออกทั้งสองคอลัมน์ผ่านทั้งชุด 14,600 เทส และเทสบวกสองตัวของผมใช้ทรีที่ cap ที่ `<=17` จึงมองไม่เห็น `018` โดยโครงสร้าง | เพิ่มคลาส `ItStaysTrueOnTheDIRECTORYNotOnlyOnThisVersionTests` ที่รันกับ `migrations/` **จริง** ⇒ แดงวันที่ใครถอนหรือเปลี่ยนเลข |
| **D6** | ข้ออ้างในหัวไฟล์ว่า "guard 5 คือตัวจับ" ถูกเฉพาะรูปฐานของ fixture ผม · ฐานที่ **เคยเล่นแล้ว** (มีแถวใน `character_skills`/`character_equipment`/`sessions` = NO ACTION) SQLite โยน `FOREIGN KEY constraint failed` ก่อน guard ทำงาน | แก้หัวไฟล์ให้บอกทั้งสองกลไก และบอกว่าฐานเจ้าของเป็นรูปที่สอง |
| **D7** | เทส `next free number` ของผมส่งต่อบั๊กเดิม: `numbers[-1] == 17` จะพัง `018` เหมือนที่ `016` พังวันนี้ | เปลี่ยนเป็น "เลขนี้มีอยู่ + ไดเรกทอรีไม่มีช่องว่าง" |
| **D8** | `_writes_vitals_at_birth()` **ไม่เคยถูกเรียกเลย** บนฐาน 009+ (short-circuit `if state or ...`) วัดได้ 0 ครั้ง | เรียกก่อนเสมอ |
| **D10** | `_coerce` โยน `ValueError` ดิบกับ `DEFAULT (0)` / `0x10` / `CURRENT_TIMESTAMP` | เปลี่ยนเป็น AssertionError ที่บอกว่าต้องทำอะไร |
| **D2** | 🔴 guard ทั้งเจ็ด **ไม่เห็นเนื้อแถวของตารางลูกเลย** — `UPDATE character_positions SET scene_id=99` ก่อน DROP ผ่านเขียว (ทุกตัวละครย้ายไปฉาก 99 และ migration รายงานว่าสำเร็จ) | **หนี้ที่ยังไม่จ่าย** — บันทึกเป็น nonclaim ข้อ 7 และงานแรกของรอบหน้า ไม่ใช่ของที่แก้ทันในรอบนี้ |
| **D9** | บูตพร้อมกันสี่เธรด: ข้อมูลถูกต้อง ledger ถูกต้อง แต่ผู้แพ้ได้ข้อความ `guard_exactly_the_two_defaults_were_added` = บอกเหตุผิด (`009` มีรูปเดียวกัน) | **หนี้** บันทึกไว้ ไม่แก้ในรอบนี้ (แตะกลไกที่ `009` ใช้ร่วม) |

**ผลลบของ adversary ที่มีค่าเท่ากับ finding**
- mutant ที่ **ผ่านไม่ได้**: ทิ้ง tombstone · renumber `id` (+100) · INSERT ที่ไม่ใส่สองคอลัมน์แล้วพึ่ง DEFAULT (veteran กลายเป็น 0) · `COALESCE(experience,0)` · `AUTOINCREMENT` · `COLLATE NOCASE` บน `name_key` · `cash`/`mp_current` ได้ default · `skill_points DEFAULT 1` · แถวกำพร้าที่ปลูกใน `character_skills` (**ครึ่ง orphan ไม่ vacuous**) · วัตถุค้างชื่อไม่มี prefix · plug ที่ถูกตัวแรกผิดตัวที่สอง (`measure_every_birth` ยังรับน้ำหนักอยู่จริง)
- **guard 6 สเปลลิงระบุชื่อคอลัมน์ = ถูกแล้ว** เขายืนยันว่า `DEFAULT0` หลังตัดช่องว่างมีอยู่จริงหนึ่งที่คือ `identity_hi` และคำถามเรื่อง `CREATE TABLE "characters"` ที่ผมตั้งให้เขาไปตรวจ = ไม่ใช่ปัญหา (สองฝั่ง quote เหมือนกัน)
- **guard 5 รายชื่อเจ็ดตาราง = ครบจริง** เขา derive เองจาก `PRAGMA foreign_key_list` ทั้งฐาน ได้เจ็ดตัวเท่ากันเป๊ะ
- **backup ของฐานจริง = ยืนยันแล้ว** `migrate_with_backup` สร้างสแนปช็อตจริงบนดิสก์ ledger ยังอยู่ที่ 16 แถวยังเป็นก่อน-017 และบูตที่สองไม่สร้างซ้ำ · แต่เขาแก้กรอบให้สองข้อ ดูข้อ 7
- **เลข `017` ไม่ชน**: `origin/main` หยุดที่ 016 · PR เปิดอยู่ 15 ใบไม่มีใบไหนแตะ `migrations/` · `.gitattributes` ตรึง `*.sql text eol=lf` ⇒ sha เสถียรข้ามวินโดวส์/CI
- collateral ที่เขานับเป็นชุดเต็มสี่รอบ: **`017` เดี่ยว ๆ = 107 แดง ไม่ใช่ 39 อย่างที่หัวไฟล์ `016` บันทึกไว้** · พินใหม่เคลียร์ 82 เหลือ 12 · ผมจ่ายครบ 12 แล้วในรอบนี้ (ข้อ 3)

## 6.1 🔴 คำถามที่ adversary ตั้งและผมยังตอบไม่ได้ (ส่งต่อ COO)
**ใครเป็นเจ้าของเลข `0` ของ `skill_points` ตอนเกิด และเทสตัวไหนจะแดงในวันที่มีคนวัดได้จริง?**
ตอนนี้มีสามคำตอบที่ขัดกันวางอยู่พร้อมกัน: หัว `017` บอก "ไม่ได้วัด แต่เจ้าของสั่ง" · `pf_birth_state` บอก
"ไม่มีโมดูลไหนประกาศเลขนี้ จึงไม่เกรด" · หัว `016` ติดป้าย `[LANE-DB assumption - awaiting COO]`
· ผมปิดครึ่งหนึ่งแล้วด้วยเทสที่รันกับ `migrations/` จริง (D3) ⇒ **การถอน/เปลี่ยนเลขจะแดง** แต่ยังไม่มีใครเป็น
เจ้าของ "เลขที่ถูก" · ใบ `ASK-COO` ออกแล้วในรอบนี้

## 7. nonclaims
- **ไม่อ้าง**ว่าผู้เล่นเห็นเควสจ่ายรางวัลบนจอวันนี้ — อ้างว่าประตูที่ปฏิเสธ "เพราะไม่เคยวัด" เลิกปฏิเสธด้วยเหตุนั้น
  สำหรับตัวละครที่สร้างหลัง `017` ซึ่งวัดบนแถวจริง
- **ไม่อ้าง**ว่า `0` ของ `skill_points` เป็นค่าที่วัดได้ — เป็นคำสั่งเจ้าของ (`1218`) และหัวไฟล์เขียนแยกไว้ชัดว่า
  `experience` วัดได้จาก `standard_status.tsv` ส่วน `skill_points` **NOT MEASURED** · `skill_point_curve.py`
  ของ CS ที่เพิ่งลง main ก็ไม่ได้บอกค่าตอนเกิด
- **ไม่อ้าง**ว่า `009` เคยทำของผู้เล่นหายจริง — อ้างว่าเส้นนั้นเดินได้ และ `009` มีสามบรรทัดนั้นอยู่แล้ว
- **ไม่อ้าง**ว่า 82 คือจำนวนเทสที่จะแดงบน main ทุกสภาพ — เป็นจำนวนที่วัดจากชุดไฟล์ที่ import พินนี้
- 🔴 **หนี้ที่ยังไม่จ่ายและผมไม่ปิดบัง (adversary D2)**: guard ทั้งเจ็ด **ไม่เห็นเนื้อแถวของตารางลูก** —
  `UPDATE character_positions SET scene_id=99` ก่อน `DROP TABLE` ผ่านเขียวทั้งไฟล์ · **ไม่อ้าง**ว่า `017`
  พิสูจน์ว่าแถวลูกไม่ถูกแก้ อ้างแค่ว่า "จำนวนแถวลูกครบ และไม่มีแถวกำพร้า" · งานแรกของรอบหน้า
- 🔴 **หนี้ D9**: บูตพร้อมกันหลายโพรเซส ผู้แพ้ได้ข้อความ guard ที่บอกเหตุผิด (`009` มีรูปเดียวกัน ไม่ใช่ของใหม่)
- **ไม่อ้าง**ว่า `app.py` เป็นจุดเดียวในรีโปที่เรียก `migrate()` — adversary นับได้อีก 18 จุด (13 ใน
  `tools/pf_*_headless_replay.py` · 5 ใน `*_headless.py`/`persistence_gt221_fixture.py`) · เขาตรวจแล้วว่า
  ทุกจุด `shutil.copyfile` ก่อนแล้ว migrate สำเนา ⇒ ไม่มีจุดไหน apply `017` กับไฟล์ canonical · แต่ประโยค
  "ทั้งสองจุดบูตที่ migrate ผ่าน backup" จริงเฉพาะกับ `app.py` และ `009`/`016`/`017` เขียนโดยไม่เอ่ยสิบแปดจุดนั้น
- **ไม่อ้าง**ว่ากู้คืนได้ถ้า rebuild ผิดผ่านเขียว: ไบต์ปลอดภัย (สแนปช็อต) แต่ **ไม่มีการเทียบฐานสดกับสแนปช็อต
  หลัง migrate** ⇒ ความผิดจะถูกพบตอนคนสังเกตพฤติกรรมผิดในอีกหลายสัปดาห์ และตอนนั้นการ restore
  ทิ้งทุกอย่างที่ผู้เล่นทำมา · เป็นเหตุผลที่ D1/D2 ถูกจัดเป็น HIGH ไม่ใช่เรื่องสไตล์
- ไม่แตะ canonical DB · ไม่แตะ `runtime.py`/`app.py`/`gm/` · ไม่แตะ `v141` · ไม่เปลี่ยน behavior ของเมธอดเดิม
  ใน `store.py` (ไม่แตะ `store.py` เลยสักบรรทัด) · ไม่แตะไฟล์ที่ apply แล้วใน `migrations/`
- 🔴 **แตะไฟล์นอกเขต 3 บรรทัด**: `tests/test_skill_learn_wiring.py` ของ LANE-CS (import + หนึ่งบรรทัด
  สร้างสภาพ NULL) เพราะ `017` ทำให้ประตู fail-closed ในเทสนั้นเอื้อมไม่ถึง · **ประกาศด้วยจดหมาย** ตามแบบที่
  LANE-GM รอบ `tof9cw` เคยทำ (บันทึกอยู่ใน `test_live_named_attr_values.py` เอง) · ถอน/เขียนใหม่ได้ตามใจ CS

## 8. สถานะ PR (ตามจริง)
- **`pirate-force-server#1141`** — เปิดแล้ว ไม่ draft · body มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด
  · **ยังไม่อยู่บน main** (รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`)
- `pf_bridge#1893` — ล็อกของรอบนี้
- ชุดเต็มบนต้นไม้สุดท้ายหลัง `git merge origin/main`: ดูบรรทัดใต้ตาราง adversary
- `tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
- ป้ายเวลา: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `13:44` เทียบเวลาตรวจ `13:56` = ห่าง **12 นาที** (ปกติ)

## 9. รอบหน้าทำอะไร (เรียงตามลำดับ ห้ามสลับ)
1. **จ่าย D2**: guard ที่เทียบ **เนื้อแถว** ของตารางลูกทั้งเจ็ด ไม่ใช่แค่จำนวน (ออกเป็น migration ใหม่ไม่ได้ —
   `017` แช่แข็งแล้ว ⇒ ทำเป็นเทส/เครื่องมือที่ `018` ตัวถัดไปต้องผ่าน หรือ helper ที่ทุก rebuild ยืมได้)
   แล้วยืนยัน `017` อยู่บน main ด้วย `git merge-base --is-ancestor`
2. **ถ้า `0206` ลง main** ⇒ คืนครึ่งประตู `apply_v111_stack_merge` ทันที (`git show ebdad7c`)
3. ถ้า CS ปลดพิน importer ⇒ `STARTING_BACKPACKS` 5 ใบ · **ต้องตอบ D9 ก่อน** (`_content_allowlist` โต 2 -> 10)
4. กู้งาน census อาวุธจาก `#1128` ที่เกตปิด (กิ่ง `claude/festive-tesla-21lxm6` ยังอยู่ · อ่าน log หาสาเหตุเดียว)
5. reader ที่นับ backfill จาก snapshot (ใบ `0632` ทาง 2) · หนี้ adversary `#1699`/`ueaey7` · `#1781`/`kq4m8t`

## 10. จดหมายรอบนี้
- `20260908_1428_LANE-DB-ASK-COO-who-owns-the-birth-zero-of-skill-points.md` (ADDRESSEE: COO)
- `20260908_1429_LANE-DB-TO-CS-three-lines-in-your-test-file-declared.md` (ADDRESSEE: LANE-CS · cc COO)
- บริโภคใบ `1246` (COO-DECISION ถึง LANE-DB): วาง `.CONSUMED.txt` แล้ว · ใบ `1218` เป็น ALL-LANES
  ⇒ ตาม NOW `0442` ไม่วาง stub ร่วม อ้างเลขที่นี่แทน · ใบ `1312` (SYNC-NOTICE `#1128` ถูกปิด) บริโภคแล้ว
  ⇒ งานกู้ census อยู่ในข้อ 9 รอบหน้า

SCOREBOARD: COMING | ตัวละครที่สร้างวันนี้เกิดมาพร้อม experience/skill_points = 0 แทน NULL จึงรับรางวัลเควสได้ (จุดเรียก 497 จุดหลังประตูสองบานนั้นเลิกถูกปฏิเสธเพราะ "ไม่เคยวัด") | pirate-force-server#1141 · migrations/017 · ชุดเต็ม 14852 passed 0 failed

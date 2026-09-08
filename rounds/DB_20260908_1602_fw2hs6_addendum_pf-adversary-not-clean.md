# LANE-DB รอบ `fw2hs6` — addendum: ผล `pf-adversary` คืนหลังปลดล็อก · **NOT CLEAN**

เขียน 2026-09-08T16:56+07:00 · ต่อจาก `rounds/DB_20260908_1602_fw2hs6_round.md` (ขึ้น main แล้วผ่าน `pf_bridge#1916`)
PR เซิร์ฟเวอร์ของรอบ = `pirate-force-server#1152` (ยังเปิด ยังไม่ merge ตอนเขียนใบนี้)

ไฟล์รอบเดิมเขียนว่า `ADVERSARY_PENDING pirate-force-server#1152` และ **ไม่ได้เขียนว่า "ผ่าน adversary"**
ผลคืนหลังปลดล็อก ⇒ ตาม `COMMON_LANE_ROUND` ("เจอของต้องแก้หลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก")
ใบนี้คือการเขียนลง **ไม่ใช่การแก้** — 🔴 **ผมไม่แตะโค้ดหลังปลดล็อก ไม่ push โค้ดเข้า `#1152`**

## 0. สรุปหนึ่งบรรทัด
**สิบสองข้อ · สี่ข้อหนัก · adversary รันโค้ดจริงพิสูจน์ทุกข้อ** และสองข้อที่หนักที่สุดคือ
**ข้ออ้างหลักของรอบนี้เองที่ยังไม่จริง** — ยามใหม่ที่ผมสร้างมาปิด D2 **ยังถูก D2 ตัวเดิมเดินอ้อมได้**

---

## 1. 🔴 ของที่ต้องแก้ก่อนอย่างอื่นในรอบหน้า (เรียงตามลำดับ)

### D1 [CRITICAL · วัดแล้ว] `018` ลบ FOREIGN KEY ทิ้งได้ แล้วเทสทั้ง 14,7xx ตัวเขียวหมด
มิวแทนต์โทเคนเดียวใน `018` บรรทัด 105: `character_id INTEGER NOT NULL REFERENCES characters(id),`
→ `character_id INTEGER NOT NULL,` · ชุดเต็ม **ตัวเลขเท่ากันเป๊ะ** กับต้นไม้สะอาด แล้วบน DB ที่ migrate ด้วย
มิวแทนต์: `INSERT ... VALUES (424242,...)` พร้อม `PRAGMA foreign_keys=ON` → **รับ** ⇒ แถวสกิลกำพร้าถาวร

🔴 **และเทสของผมเองคือตัวที่ทำให้มันรอด**: `test_foreign_key_integrity_holds_after_the_rebuild`
เรียก `pragma_foreign_key_check('character_skills')` ซึ่งบนตารางที่**ไม่มี** FK คืนศูนย์แถว
⇒ **เทสที่ตั้งชื่อตาม foreign key ผ่านเพราะ foreign key หายไป** · `test_the_columns_unique_constraint_and_index_are_unchanged`
ก็ตรวจคอลัมน์/`UNIQUE`/index แต่ **ไม่ตรวจ `REFERENCES`**

**สภาพจริงวันนี้: `018` ที่ส่งไป *ไม่ได้* ลบ FK** — นี่คือ**จุดบอด** ไม่ใช่บั๊กที่ทำงานอยู่
แต่จุดบอดนี้เปิดอยู่กับ rebuild ทุกใบที่จะยืม helper ต่อจากนี้
**ทางแก้ที่จะแดง**: เทียบ `pragma_foreign_key_list` ก่อน/หลัง หรือ diff DDL แบบ normalize ลบเฉพาะ CHECK ที่ตั้งใจเปลี่ยน

### D2 [HIGH · วัดแล้ว] 🔴 การทุจริตแบบ D2 **ย้ายขึ้นไปหนึ่งบรรทัด** แล้วผ่านยามใหม่เขียว
```sql
BEGIN IMMEDIATE;
UPDATE character_skills SET skill_id=skill_id+1000;   -- statement เดียวกับที่เทสผมใช้
CREATE TABLE _pf_mig018_before AS SELECT * FROM character_skills;
```
วัดบน DB จริงที่ `017` แถว `(99,210)` → **migration ผ่านเขียว** · หลัง migrate = `(1099,1210)`
คือ **ผลลัพธ์เดียวกับ D2 เป๊ะ ๆ ที่ยามตัวนี้ถูกสร้างมาเพื่อกัน**

เหตุ: **หน้าต่างที่ยามคุ้มครองเริ่มที่ snapshot** และไม่มีอะไรพิสูจน์ว่า snapshot เป็นคำสั่งแรกในธุรกรรม
`test_the_snapshot_is_taken_before_the_table_is_dropped` ปักแค่ `snapshot < DROP` และ `RENAME < verify`
**ไม่เคยปัก** `BEGIN IMMEDIATE` ตามด้วย snapshot ทันที และไม่เคยปักว่า verify เป็นบล็อกสุดท้าย
🔴 `018` ตัวจริงรอดเพราะ **เทส** (`test_an_honest_rebuild_still_passes`) ไม่ใช่เพราะ **ยาม** — ข้ออ้างของรอบอยู่ที่ยาม ⇒ **ข้ออ้างยังไม่จริง**

### D3 [HIGH · วัดแล้ว] 🔴 `grant_gm_skills` **รายงานสำเร็จโดยไม่เขียนอะไรเลย** ถ้า DB ยังไม่ถึง `018`
`INSERT OR IGNORE` ของ SQLite กลืน **CHECK violation** ด้วย ไม่ใช่แค่ UNIQUE · วัดบน DB ที่ migrate ถึง `017`:
```
ledger max version: 17
grant_gm_skills(cid, tuple(range(1000,1300)))  ->  คืนค่าปกติ (99,)
rows in character_skills after a 300-skill /skill all: 1
```
**300 แถว เขียนจริง 0 แถว ไม่มี exception** ⇒ operator เห็นว่า `/skill all` สำเร็จ แต่ไม่ได้อะไรเลย
🔴 นี่ชน docstring ของผมเองที่เขียนว่า "Nothing is written when anything is refused" — มันไม่ได้ refuse มัน**เงียบ**
พี่น้องสองตัวไม่มีปัญหานี้เพราะ `'starting_kit'` มีมาตั้งแต่ `011` ที่สร้างตาราง แต่ `'gm_grant'`
มาพร้อม migration ที่ทำให้มันถูกกฎหมาย **ในคอมมิตเดียวกัน**
**ทางแก้สองบรรทัด**: หลัง `executemany` เทียบ `set(checked) - set(after)` (หรือ `db.total_changes`) แล้ว `raise`

### D4 [MEDIUM · วัดแล้ว] `test_a_lost_row_is_caught_too` **ไม่ได้วัดสิ่งที่ชื่อมันบอก**
`text.replace(f"FROM {TABLE};", ..., 1)` ไปโดน **บรรทัด snapshot (บรรทัด 102)** ไม่ใช่บรรทัดคัดลอก
⇒ ตารางที่ rebuild ไม่ได้หายแถวเลย **snapshot ต่างหากที่สั้น** · adversary เอา `COUNT_ONLY` ยิงมิวแทนต์เดียวกัน
→ **ยามนับแถวก็แดงเหมือนกัน** ⇒ เทสตัวนี้ไม่แยกยามเก่ากับยามใหม่ออกจากกัน
🔴 และมันทำให้ข้อ 3 ในดอกสตริงของไฟล์เทส **เกินจริง** · สองตัวที่แยกได้จริงคือ
`test_the_content_guard_aborts...` กับ `test_a_dropped_column_filled_by_a_default_is_caught` เท่านั้น

---

## 2. ข้อที่เหลือ (บันทึกไว้ ยังไม่จ่าย)

| # | ระดับ | สาระ |
|---|---|---|
| D5 | MEDIUM | **พินแช่แข็ง helper ตั้งแต่วันที่ `018` ลง**: ปรับปรุง `verify_sql` = เทสแดง 4 ตัว ⇒ ต้องแก้ `018` ⇒ `RuntimeError migration checksum mismatch` บน DB ที่ apply แล้ว · "helper ที่ทุก rebuild ยืมได้" กลายเป็น "helper ที่ไม่มีใครปรับปรุงได้" ⇒ พินควรเทียบกับ **สำเนา v1 ที่แช่ไว้** หรือเทียบเชิงความหมาย ไม่ใช่เทียบกับ `verify_sql` สด |
| D6 | MEDIUM | **หนี้ D2 จ่ายแค่บางส่วนแต่เล่าเหมือนจ่ายครบ**: ใบ `nivlwg` §9 ข้อ 1 สั่งว่ายามต้องเทียบเนื้อ **ของตารางลูกทั้งเจ็ด** · helper ของผมเป็น **ตารางเดียว** และ `character_skills` **ไม่มีตารางลูกเลย** ⇒ รูป D2 ตัวจริง (`UPDATE character_positions` ก่อน DROP ของ `characters`) **ยังไม่มีอะไรกัน** · อีกครึ่ง: หัวไฟล์ `018` พิสูจน์ว่า `017` อยู่บน main ด้วย **การมีอยู่ของไฟล์** ไม่ใช่ `git merge-base --is-ancestor` ตามที่ใบสั่ง (adversary รันให้แล้ว = **เป็น ancestor จริง** ⇒ ข้อสรุปถูก วิธีในเอกสารอ่อนกว่าที่สั่ง) |
| D7 | MEDIUM-LOW (latent) | เหตุผลเรื่อง "แถวซ้ำ" ในดอกสตริง helper **ผิดตามตัวอักษร**: `_before={A,A,B}` vs `after={A,B,B}` ⇒ นับเท่า · `EXCEPT` ว่างสองทาง ⇒ **ยามเขียวทั้งที่ข้อมูลเปลี่ยน** · และประโยค "ทุกตารางที่สายนี้ rebuild มี `id INTEGER PRIMARY KEY`" ผิด — 5 จาก 11 ตารางไม่มี (คีย์ที่ `character_id` · `sessions` เป็น TEXT · `character_backpack_items` เป็น composite) · คุณสมบัติที่ปลอดภัยจริง (มี PK อะไรก็ได้ ⇒ ไม่มีแถวซ้ำ) ยังจริงบนสคีมาวันนี้ ⇒ **ยังไม่ระเบิด แต่เหตุผลที่คนต่อไปจะยืมไปใช้ผิด** |
| D8 | LOW | affinity ตัวเลขมองไม่เห็น: `1.0` (real) → `1` (integer) ⇒ `EXCEPT` ว่างสองทาง ยามเขียว · (`'99'` ข้อความ→เลข **จับได้** ⇒ แคบ) ⇒ ประโยค "the DATA crossed unchanged" แรงกว่าที่พิสูจน์ |
| D9 | LOW (ข้อสงสัย) | `lifecycle.py:151` `_class_id_for_a_retried_skill_grant` คืน `None` ทันทีที่ `list_character_skills` ไม่ว่าง · แถว `gm_grant` เป็น **เหตุที่สาม** ที่มันแยกไม่ออก และประตูผมเป็นตัวแรกที่เติมตารางนั้นได้โดยไม่ผ่านชุดคลาส · adversary **ไม่ได้ reproduce** จัดเป็นข้อสงสัย |
| D10 | LOW (ยกมาจากรอบก่อน) | บูตพร้อมกันสี่โพรเซส: ข้อมูล/ledger/index ถูกหมด แต่ผู้แพ้สามตัว **rebuild ซ้ำทั้งใบ** แล้วตายด้วย `IntegrityError: UNIQUE constraint failed: schema_migrations.version` (018 `COMMIT;` ปล่อยล็อก wrapper ⇒ อ่าน ledger เป็น TOCTOU) — **หนี้ D9 เดิมของรอบ `nivlwg` ที่ยังไม่จ่าย ไม่ใช่ regression ใหม่** |
| D11 | LOW | ดอกสตริง `verify_sql` เขียน "Three guard rows" แต่ปล่อยออกมา **สี่** (เทสของผมเองเขียน `# Four guard rows`) · และ `016`/`017` มีเทส ASCII/cp874 ของไฟล์ตัวเอง แต่ `018` **ไม่มี** (adversary ตรวจแล้ว ไฟล์ใหม่ทั้งสี่เป็น ASCII จริง — พินหายไปเฉย ๆ) |
| D12 | PROCESS | `PREFLIGHT PASS` ของผมมี `[prbody] SKIPPED` อยู่ข้างใน ⇒ **ห้ามอ้างว่า preflight ครอบกฎ marker ของ PR body** · (ส่วน `TWO_SESSIONS_SAME_SCENE:` ไฟล์รอบจริงมีแล้วในข้อ 5 — adversary เห็นแค่ `_claim.md` เพราะรอบยังไม่จบตอนมันตรวจ) |

---

## 3. ที่ adversary ลองแล้ว **พังไม่ได้** (ผลลบที่มีค่าเท่ากับ finding)
- **A/B ยามเก่า-ยามใหม่เป็นการวัดจริง ไม่ใช่สร้างให้จริง**: marker ของ `_corrupt` ลงบรรทัด 114 `DROP TABLE character_skills;` ไม่ใช่ prose · `COUNT_ONLY` ต่างจากยามจริงของ `014` แค่แถว FK ซึ่งไม่เกี่ยวกับการแก้ `skill_id` · และ `assertNotIn("EXCEPT", body)` **เป็นกันชนจริง** — มันแดงตอน adversary ลองบิด helper
- **ย้อนกลับตอนยามยิงสะอาดจริง**: ไม่มี `_pf_mig018_*` ค้าง ไม่มี `character_skills_rebuild` ค้าง ไม่มี rename ครึ่งทาง แถวเหมือนเดิมทุกไบต์ `18` ไม่อยู่ใน ledger · `PRAGMA foreign_keys=OFF` **ไม่รั่ว** (คอนเนกชันของ `migrate()` ตายไปกับ `connect()` และทุก `connect()` ถัดไปเปิดใหม่)
- **NULL เทียบ NULL ใต้ `EXCEPT` เป็นอย่างที่อ้างจริง** · **renumber `id` จับได้** · **`'99'` ข้อความ→เลข จับได้**
- **`grant_gm_skills` all-or-nothing จริงบนทุกเส้นปฏิเสธที่เอื้อมถึง**: `KeyError` หลัง `BEGIN IMMEDIATE` ถูก rollback โดย `except` ของ `connect()` (ไม่มีแถวเขียน ไม่มีธุรกรรมรั่ว) · `WriteLockTimeout` เหมือนกัน · `executemany` เทียบเท่าลูปของพี่น้องสำหรับ `OR IGNORE` เพราะ id ซ้ำถูกพับใน Python ก่อน · ช่วง u32 ใน Python กับใน CHECK **ตรงกัน** ⇒ ไม่มี id ที่ผ่านด่านแล้วถูกกลืน
- **มิวแทนต์สคีมาสองแบบที่ชัดที่สุด เทสของรอบนี้จับได้จริง** (CHECK ไม่ถูกขยาย · `CREATE INDEX` หาย) — **มีแต่ foreign key ที่หลุด**
- **CLAIM D ผ่าน**: `18` ไม่ซ้ำ · ไดเรกทอรีต่อเนื่อง `1..18` · ledger สอดคล้อง · บูตที่สองไม่ apply ซ้ำ
- **CLAIM E ผ่าน**: 5 ไฟล์ เพิ่มล้วน · `store.py` ลบ 0 บรรทัด · ไม่แตะ `runtime.py`/`app.py`/`gm/`/`v141` · ไม่แก้ไฟล์เทสเดิม · `[skips] PASS - no new skip markers vs origin/main` · `git ls-files` เห็นครบห้าไฟล์
- **preflight PASS (exit 0)** ยืนยันซ้ำโดย adversary เอง

## 4. เรื่องตัวเลขชุดเต็มที่ไม่ตรงกัน — บันทึกไว้ ไม่กลบ
ผมวัดได้ **14983 passed / 450 skipped** · adversary วัดได้ **14782 passed / 651 skipped** บน sha เดียวกัน
🔴 **ผมไม่อ้างว่ารู้สาเหตุแน่ชัด** · สมมติฐานที่ตรวจได้รอบหน้า: มันรันใน `git worktree` แยก ซึ่ง **ไม่มี `pf_bridge` วางอยู่ข้าง ๆ**
และ `AGENTS.md §7` บอกเองว่าสภาพ "ไม่มี `pf_bridge` ข้าง ๆ" เปลี่ยนจำนวน skip (นั่นคือเหตุที่ต้องซ้อม `skip_census` ในสภาพนั้น)
⇒ **ผลรวม passed+skipped เท่ากันทั้งสองฝั่ง (15433)** ซึ่งสอดคล้องกับสมมติฐานนี้ แต่ **ยังไม่ได้พิสูจน์** — งานรอบหน้า

## 5. คำถามเดียวที่ดีไซน์นี้ยังตอบไม่ได้ (adversary ตั้งเอง — ผมยกมาทั้งดุ้นเพราะมันถูก)
> ยามพิสูจน์ว่า **แถว** ระหว่าง snapshot กับ verify ไม่เปลี่ยน · **แล้วใครพิสูจน์ สคีมา?**
> จุดประสงค์ทั้งหมดของ rebuild คือเปลี่ยนสคีมา ยามจึงจงใจไม่มอง — ผลคือรอบนี้ลบ foreign key ทิ้งได้
> โดยเทส 14,7xx ตัวและยามสี่แถวบอกเขียวหมด · ถ้าคำตอบคือ "ไฟล์เทสของ migration เป็นคนตรวจสคีมา"
> คำตอบนั้น **สอบตกตั้งแต่ครั้งแรก**: เทสที่ชื่อ `test_foreign_key_integrity_holds_after_the_rebuild`
> ผ่าน *เพราะ* foreign key หายไป · **อะไรควรเป็นครึ่งที่สองของ helper?**

🔴 **ผมไม่เขียนว่า "ผ่าน adversary"** — ผลคือ **NOT CLEAN** และรอบนี้ **จ่ายไปศูนย์ข้อ** (ผลคืนหลังปลดล็อก)
ค้างทั้งสิบสอง: D1 D2 D3 D4 หนักที่สุด · **งานแรกของรอบหน้าคือสี่ข้อนี้ เรียงตามนี้ ห้ามหยิบงานใหม่ก่อน**

SCOREBOARD: NONE | ใบเอกสารล้วน ไม่มีโค้ดใหม่ - บันทึกผล adversary ที่คืนหลังปลดล็อกรอบ `fw2hs6` ว่า NOT CLEAN 12 ข้อ เพื่อให้รอบหน้าหยิบเป็นงานแรกแทนที่จะหายไป | pf_bridge addendum ของ `rounds/DB_20260908_1602_fw2hs6_round.md` · PR ของรอบ = pirate-force-server#1152

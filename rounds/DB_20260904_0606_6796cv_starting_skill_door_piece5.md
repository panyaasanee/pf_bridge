# DB round (`6796cv`) — 2026-09-04T06:06+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_0433_wgu3vp_class_id_resolver_piece1.md` — รอบนั้นเปิด `#699`
(class_id resolver, piece 1/5) และ CORE-REQUEST สองจุดเสียบ ระหว่างรอบนั้นถึงรอบนี้: `#699`
merge แล้ว และ chief มอบให้ LANE-E ทำสองจุดเสียบ (`#705`) เปิดตอนต้นรอบนี้ **merge ระหว่างรอบนี้**
(เห็นตอน fetch ก่อนเปิด PR เซิร์ฟเวอร์) — piece 1 ปิดสมบูรณ์แล้วบน main

## NOW.md — รอบนี้ขยับข้อไหน

**ไม่ขยับบรรทัดใดของ `NOW.md`** — ไม่มีสิทธิ์แก้ไฟล์นั้นเอง หัวข้อ "บันไดไมล์สโตน" บรรทัด
PLAYER/CHARACTER: piece 1 ("class ที่เลือกจาก `CreateActorVital` → `class_id`") **ตอนนี้ครบทั้งสอง
ครึ่ง** (`#699` + `#705` merge แล้วทั้งคู่) — `GT-215` ตาม `COO-ORDER 0329` ปิดเมื่อ "ชิ้น 1 ขึ้น
main" ซึ่งครบแล้ว แต่การย้ายข้อความใน NOW.md เป็นของ COO/เจ้าของ ไม่ใช่ของสายนี้ รายงานในจดหมาย
สถานะแทน piece 5 (สกิลเกิด, รอบนี้) ยังไม่ถึง main (PR เปิดรอเกต) จึงไม่ใช่จุดปิดอะไรใน NOW.md

## 1. ล็อกรอบ

- 05:42+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า (มีแค่ `#705 [LANE-E]` ไม่ใช่ของสายนี้)
  ⇒ ไม่ต้องปลดล็อกใคร ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`ad3887f8`) commit `rounds/DB_20260904_0542_6796cv_claim.md`
  push แล้วเปิด `pf_bridge#1070 [LANE-DB] round 6796cv: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1070` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ก่อนเปิด PR ฝั่งเซิร์ฟเวอร์ (ก่อนสร้างไฟล์ migration ใหม่): `git fetch origin main` ซ้ำ
  (`pirate-force-server` main ขยับจาก `bed7c8b` เป็น `522c389` ระหว่างทำงาน — `#704 [LANE-A]` merge
  ไม่แตะ `migrations/`) ตรวจ `migrations/` บน origin/main สด: เลขสูงสุดยังเป็น `010` ⇒ `011` ว่าง
  list `[LANE-DB]` open ใน `pirate-force-server`: ว่างเปล่า ⇒ ไม่ชนใคร
- ก่อน push จริง: `git fetch origin main` อีกครั้ง พบ `#705 [LANE-E]` (สองจุดเสียบ piece 1) merge
  ระหว่างรอบ (main `522c389` → `d98d7ab`) — ไม่แตะ `migrations/`/`store.py`/ไฟล์เทสของรอบนี้เลย
  (แตะ `lifecycle.py`/`model.py`/`session.py`/`legacy_bridge.py`/เทสของ piece 1) → `git rebase
  origin/main` สะอาด ไม่มี conflict → รันชุดเต็มซ้ำบนต้นไม้ที่ merge แล้ว (ดูข้อ 4) → push
  `--force-with-lease` (rebase กิ่งของตัวเองที่ยังไม่มีใคร merge — อนุญาตตามกติกา)

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` หักใบที่มี `.CONSUMED.txt` คู่ ⇒
ใบเดียวที่ยังไม่มี stub: `20260904_0445_COO-DECISION-lane-db-backfill-class-id-...md` (สี่รั้ว
backfill + ลำดับ "piece 1 ต้องขึ้น main ก่อน") — อ่านและปฏิบัติตามแล้ว (ไม่เริ่ม backfill รอบนี้
เพราะ piece 1's สองจุดเสียบเพิ่ง merge ระหว่างรอบ ไม่ทันวางแผน backfill รอบเดียวกัน — คิวรอบหน้า)
สร้าง stub `.CONSUMED.txt` แล้ว (ใบ `20260904_0328` ไม่นับ — ADDRESSEE ของมันคือ COO ไม่ใช่ LANE-DB
cc มาเฉยๆ)

ส่งจดหมายออกสองใบ:
1. `20260904_0542_LANE-DB-RE-TICKET-piece-2-starting-stats-has-no-committed-source-table.md`
   (ADDRESSEE: chief, cc COO/เจ้าของ) — piece 2 บล็อกจริง ไม่มีตาราง commit แล้วให้ค่าได้ ขอ RE
2. `20260904_0542_LANE-DB-CORE-REQUEST-starting-skill-door-built-needs-one-hookup.md`
   (ADDRESSEE: chief, cc COO/LANE-CS) — ประตูสกิลเกิดพร้อมแล้ว ขอจุดเสียบเดียว (แนะนำรวมกับจุดเสียบ
   piece 1 เพราะต้องการ class_id ตัวเดียวกัน — แต่ `#705` merge ไปแล้วก่อนใบนี้ถึง chief ดังนั้นน่าจะ
   เป็นจุดเสียบแยกรอบถัดไปแทน ไม่ใช่รวมรอบเดียวกับ `#705` อย่างที่ขอไว้ — รายงานตามจริง)

## 3. ทำอะไร

### 3.1 ทำไมไม่เริ่ม piece 2 (ค่าเกิดจาก CHARCREATE_CLASS/STANDARD_STATUS)

ลองก่อนตามลำดับที่ `COO-ORDER 0329` ตั้งไว้ (deadline 08:31, เร็วกว่า piece 5) วัดจริง:
`CONSTDATA_TH__STANDARD_STATUS.tsv` (255 แถว) เป็นตาราง EXP/แต้มความสามารถ **ต่อเลเวล**
(`n_POINT_ABILITY` = แต้มที่ได้ตอนเลเวลอัพ, 0 ที่เลเวล 1) ไม่ใช่ค่าสแตทเริ่มต้นต่อคลาส
`CONSTDATA_TH__CHARCREATE_CLASS.s_SCORE` (หกตัวเลขต่อแถว) เป็นตัวเลือกเดียวที่ดูเหมือนสแทท แต่
**ไม่เคยถูก RE เลย** — ยืนยันซ้ำจาก docstring ของ `class_catalog.py` (LANE-CS, commit แล้วบน main)
เอง: "s_SCORE's semantics have never been RE'd", อ้าง
`reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md` ที่นับรวมใน "37 other columns"
ไม่ถอดรหัส · `CONSTDATA_TH__POTENTIAL.tsv` (ตัวเลือกที่ `docs/FUNCTIONAL_COVERAGE.json` ชี้ว่าเป็น
ability-stat candidate จริง) มีแต่ header ไม่มีแถวข้อมูล ⇒ ไม่มีแหล่งค่า resolve ได้โดยไม่เดา
(`COO-DECISION 20260901_1059`) ไม่เปิดไฟล์โค้ดชิ้น 2 รอบนี้ ส่ง RE-TICKET แทน แล้วเปลี่ยนไปทำชิ้น
5/5 (ข้อมูลของชิ้นนั้น commit แล้วจริงผ่าน LANE-CS)

### 3.2 สร้างประตูสกิลเกิด (piece 5/5)

- `migrations/011_character_skills.sql` — ตาราง `character_skills` เปล่า (id, character_id FK,
  skill_id, `source` CHECK เป็น `'starting_kit'` เท่านั้น, granted_at, `UNIQUE(character_id,
  skill_id)`) + ดัชนี ไม่แตะแถวเดิม → ไม่ต้อง backup (`COO-DECISION 20260901_1112` ข้อ 3 — เหตุผล
  เดียวกับ `010_ground_drops.sql`)
- `persistence_starting_skills.resolve_starting_skill_ids(class_id) -> tuple[4 ids] | None` — ห่อ
  `class_catalog.starting_skill_ids` ของ LANE-CS (commit แล้ว, sha256-pinned) **ไม่ re-derive**
  ตารางเอง `None` สำหรับ class_id ที่ไม่รู้จัก (KeyError/ClassCatalogError → None) ไม่เดา
- `SQLiteStore.grant_starting_skills(character_id, skill_ids)` — validate ทุก id เป็น u32 ก่อนรัน
  SQL, `KeyError` สำหรับตัวละครไม่มี/ถูกลบ, idempotent ผ่าน `INSERT OR IGNORE` กับ
  `UNIQUE(character_id, skill_id)` (retry ของ create-fingerprint เรียกซ้ำได้ไม่ error) คืนค่า
  สกิลทั้งหมดที่มีตอนนี้ อ่านกลับในทรานแซกชันเดียวกัน
- `SQLiteStore.list_character_skills(character_id)` — ครึ่งอ่าน

### 3.3 `pf-adversary` (สั่งต้นรอบ ผลไม่คืนตอน push — ดูข้อ 4)

ผลคืนก่อน push จริง (ดูล่าง) พบสองข้อ ทั้งคู่แก้แล้ว:
1. mutant `INSERT OR REPLACE` แทน `INSERT OR IGNORE` รอดทั้งชุดเทสเดิม — ทั้งคู่ดูเหมือนกันตอน
   grant ซ้ำเป๊ะ แต่ `OR REPLACE` ลบแล้วแทรกใหม่แถวที่ชน (id ใหม่, granted_at ใหม่, ย้ายไปท้าย
   ลำดับ insertion) ไม่มีเทสไหน grant ชุดที่ทับซ้อนบางส่วน+สลับลำดับ เลยไม่มีใครจับ → เพิ่ม
   `test_an_overlapping_reordered_regrant_touches_no_existing_row` ที่ pin แถวเดิมด้วย id/granted_at
   ไม่ใช่แค่ค่าที่คืน — ทดสอบสดแล้วว่าเทสนี้แดงบน mutant เขียวบนโค้ดจริง
2. `character_id` ไม่ถูก bool-refuse เหมือน `skill_id`/`class_id` ในรอบเดียวกัน — เพิ่ม `TypeError`
   guard เดียวกันทั้งสอง method พร้อมเทส

### 3.4 หมุดของสายอื่นที่ migration ใหม่ทำให้แดง (แก้ตามแบบที่ chief เคยอนุมัติแล้ว)

รันชุดเต็มครั้งแรก (ก่อนแก้ adversary) พบ 3 ไฟล์แดงเพราะหมุดนับ/รายการ migration แข็ง — **แบบเดียวกับ
`notes_to_chief/20260901_1416`/`20260901_1459` ที่ chief เคยอนุมัติให้สายนี้แก้บรรทัดเดียวได้ตรง ๆ
เพราะเป็นหมุดนับไฟล์ ไม่ใช่เทสพฤติกรรมของสายอื่น**: `tests/test_item_move_capture.py` (COUNT 10→11),
`tests/test_npc_interaction_wire.py` (`EXPECTED_TABLES` เติม `character_skills` — แบบเดียวกับที่
`COO-DECISION 20260903_2050` อนุมัติให้ `ground_drops` แล้ว), `tests/test_persistence_speed_walk_seed_008.py`
(ไฟล์ของสายนี้เอง, `pending_versions` list) นอกจากนี้เชิงรุกแก้ `tests/test_foundation.py`
([1..10]→[1..11]) แม้จะ skip ในโคลนตื้นนี้ (ต้องการ git history ลึก) เพราะจะแดงบนเกตจริง (deep
clone) ถ้าไม่แก้ตอนนี้

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: `pytest tests/test_persistence_starting_skills.py
  tests/test_persistence_character_skills_011.py` เขียวตลอด (เพิ่มเทสตามหลัง adversary)
- ชุดเต็มรอบนี้ **รันสองครั้ง มีเหตุผลบันทึกตามกติกา**: ครั้งแรก (`git fetch origin main` ก่อน,
  ไม่มี commit ใหม่ตอนนั้น) สั่งไว้ก่อนผล adversary คืน (`ADVERSARY_PENDING` ชั่วคราว) — ผลคืน
  **3 failed** (หมุดของสายอื่น, ข้อ 3.4) ไม่ใช่บั๊กของโค้ดรอบนี้ ระหว่างรอผล adversary+แก้หมุด
  `#705` (piece 1 สองจุดเสียบ) merge เข้า main — ต้อง `git fetch` + rebase ซ้ำ (สะอาด ไม่ชน) ⇒
  ครั้งที่สองคือ commit สุดท้ายจริงหลังแก้ทุกอย่างแล้ว: **9430 passed, 328 skipped, 0 failed,
  18600 subtests passed (359.5s)**
- `pirate-force-server#707 [LANE-DB] round 6796cv: starting-skill-kit persistence door (piece 5/5)`
  — เปิดแล้ว มี `PF-AUTOMERGE: v4` ในตัว รอ gate Windows (ยังไม่ merge — ไม่ได้เขียนว่าขึ้น main แล้ว)
- `pf_bridge#1070` (claim PR ของรอบนี้) — เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้ เพราะ PR
  ฝั่งเซิร์ฟเวอร์ของรอบ (มีใบเดียว) เปิดแล้วพร้อม marker ครบตามเงื่อนไขปลดล็อก

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** — piece 5 ยังไม่ต่อสายเข้า creation (ขอจุดเสียบใน CORE-REQUEST รอบนี้) โมดูล/ตารางเอง
ไม่ส่งเฟรมอะไร ไม่เข้าคิว GT รอบนี้

piece 1 (class_id, จากรอบก่อน): `#699`+`#705` merge เข้า main ทั้งคู่แล้ว **ระหว่างรอบนี้** —
client-observable ของ piece 1 (คลาสไม่ถูกทิ้งบนจอ) ยังไม่วัด รอบนี้ไม่ได้ทำ attended test เอง
(นอกเขต GT ของ LANE-DB) แต่บันทึกไว้ว่าโค้ดสองครึ่งครบบน main แล้ว พร้อมให้ GT-215 วัดได้

### 5.2 wire-DB

- `migrations/011_character_skills.sql` (ใหม่) — ตาราง `character_skills`
- `src/pirateforce_foundation/persistence_starting_skills.py` (ใหม่) —
  `resolve_starting_skill_ids(class_id)`
- `SQLiteStore.grant_starting_skills`/`list_character_skills` (ใหม่ใน `store.py`, ไม่แตะ method เดิม)
- `tests/test_persistence_starting_skills.py` (ใหม่, 9 tests) — เขียวทั้งหมด
- `tests/test_persistence_character_skills_011.py` (ใหม่, 25 tests รวมเทสที่ adversary สั่งให้เพิ่ม)
  — เขียวทั้งหมด
- `character_skills` ตาราง — ยังไม่มีแถวไหนถูกเขียนรอบนี้ (ไม่มี wiring/call site)
- `pirate-force-server#707`, `pf_bridge#1070` — ลิงก์ PR ของรอบ

## 6. nonclaims

1. **ไม่อ้างว่า piece 5 เสร็จ** — โค้ด/เทสของ "ประตู" เสร็จ แต่การต่อสายจริง (เรียก
   `grant_starting_skills` หลัง resolve class_id ตอนสร้างตัวละคร) อยู่นอกเขตเขียนของ DB รอ chief
2. **ไม่อ้างว่า piece 2 เป็นไปไม่ได้ถาวร** — แค่ไม่มีตาราง commit แล้วให้ค่าวันนี้ รอ RE
3. **ไม่อ้างว่า class_id (piece 1) ถูกวัดบนจอแล้ว** — โค้ดครบบน main เท่านั้น GT ยังไม่รัน
4. **ไม่ได้แตะ `class_catalog.py`/`skill_catalog.py` ของ LANE-CS เอง** — resolve เท่านั้น ไม่
   re-derive
5. **ไม่ได้เปิด image/canonical DB/capture corpus** — ทุกอาร์ติแฟกต์ commit แล้วในสองรีโป
6. **`1101` (HP/เลเวลถาวร) ยังล็อกอยู่เหมือนเดิม** — รอบนี้ไม่ได้วัดซ้ำ Door B (นอกคิวรอบนี้ตาม
   `0329` ข้อ 1: PLAYER/CHARACTER มาก่อน)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า chief ตอบ CORE-REQUEST สกิลเกิดหรือยัง (จุดเสียบเดียว) และ RE-TICKET piece 2 หรือยัง
   ถ้าจุดเสียบสกิลมาแล้ว ⇒ วัดว่าตัวละครใหม่ได้สกิลจริงในแถว (ยังไม่ใช่ client-observable) แล้วพิจารณา
   backfill สกิลให้ตัวละครเก่า (ต้องมี backup ตามรั้วเดียวกับ backfill class_id)
3. ตรวจ backfill class_id (`0445`) — piece 1 ทั้งสองครึ่งขึ้น main แล้ว ไม่มีตัวบล็อกลำดับอีก
   เริ่มได้ตามรั้วสี่ข้อของ `0445` (exact match เท่านั้น, เฉพาะแถว NULL, backup ก่อนเขียน, พิมพ์
   บรรทัดต่อแถว) ถ้า RE-TICKET piece 2 ยังไม่มีคำตอบ
4. ตรวจ `pirate-force-server#707` ว่า gate ผ่านหรือยัง (ไม่บล็อกงานต่อ แค่รายงานสถานะ)

# DB round (`ld70iq`) — 2026-09-03T17:08+07:00 to 17:40+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260903_1633_dskm1o_pickup-survives-relogin-through-select-and-start.md` (รอบที่ปิด
`0951` ที่ชั้นวัด รอ COO ตัดสินคิวถัดไป)

**บรรทัดเดียวของรอบนี้: `COO 1649` รับ `0951` แล้วสั่งข้อ 5 — วัด (ไม่สร้าง) ว่าของบนพื้นที่ยังไม่ถูกเก็บ
รอดรีล็อกอินไหม — คำตอบคือ ไม่ (อยู่ในหน่วยความจำต่อเซสชันเท่านั้น ไม่มีตารางเลย) เสนอรูปประตูในจดหมาย
ยังไม่สร้าง ตามคำสั่ง**

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรกก่อนแตะอะไร (ฉบับ "ตรวจล่าสุด 2026-09-03 16:49 +07:00 โดย COO")

- **ไม่ขยับบรรทัดใดของ NOW.md โดยตรง** (ไฟล์นั้นเป็นของ Panya/COO เท่านั้น) — บรรทัด 47 เขียนไว้ว่าคิวถัด
  DB คือ "ครึ่งวัดของ `1048`" รอบนี้ทำเสร็จที่ชั้นวัดแล้ว (รอ gate เซิร์ฟเวอร์ก่อนขึ้น main) ถ้า COO เห็นว่า
  ครบ อาจขยับบรรทัดนั้นเป็นคิวถัดไป
- **P-0 · P-1 · P-2 · P-3 · GM-A · UI-A · UI-B** นอกเขตของสายนี้ ไม่แตะแม้ไฟล์เดียว
- 🔴 ไม่แตะ `gm/` `speed_wire.py` `runtime.py` `app.py` `v141`
- 🔴 ไม่สร้าง `migrations/` ใหม่ และไม่แตะไฟล์ `.db` จริงแม้ไบต์เดียว — ตามคำสั่ง `1649` ข้อ 5(ค): เสนอ
  รูปประตูในจดหมายเท่านั้น ยังไม่สร้าง
- **M4 ไม่ขยับ** `apply_hp_damage`/`apply_hp_heal` ยังผู้เรียกศูนย์ทั้งรีโป ไม่เกี่ยวกับรอบนี้

## 1. ล็อกรอบ

- 17:08 list PR สถานะ open ทั้งสองรีโป หัวข้อขึ้นต้น `[LANE-DB]`
  - `pf_bridge`: ไม่มีใบเปิดเลย
  - `pirate-force-server`: ไม่มีใบเปิดเลย (มี `#661` LANE-E เปิดอยู่ ไม่ใช่ล็อกของผม)
  ⇒ ล็อกว่าง ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`0dbcf51c`) commit `rounds/DB_20260903_1708_ld70iq_claim.md`
  push แล้ว เปิด `#993 [LANE-DB] round ld70iq: claim` ไม่มี `PF-AUTOMERGE: v4` ใน body ตอนเปิด
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open มีใบเดียวคือ `#993` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ระหว่างรอบ hook ของสภาพแวดล้อมบังคับให้ commit ไฟล์ที่ยังไม่ได้ตรวจ (ก่อน pf-adversary ตอบ) —
  commit เป็น WIP ชัดเจนในข้อความ ("pf-adversary review pending, not yet in a PR") ลง branch เซสชัน
  ตัวเอง (ยังไม่เปิด PR เซิร์ฟเวอร์) แล้ว amend ทับเป็นคอมมิตเดียวหลัง pf-adversary ตอบและแก้ครบ — ไม่มี PR
  ไหนเคยอ้างอิง SHA ของคอมมิต WIP นั้น จึง amend+force-push กิ่งตัวเองได้ตามกติกา
- ก่อน push โค้ดฝั่งเซิร์ฟเวอร์ (17:33): list ซ้ำอีกครั้ง — `pf_bridge` มี `#994` (LANE-GM) `#996` (LANE-B)
  เพิ่มมาระหว่างนั้น ไม่ใช่ของผม · `[LANE-DB]` ยังมีแค่ `#993` ของผมเองทั้งสองรีโป ⇒ ปลอดภัย push
- ระหว่างรอบพบ `origin/main` ของ `pirate-force-server` ขยับ (`#662` LANE-A merge) ก่อน push จริง — merge
  เข้ากิ่ง (ไม่มี conflict ไฟล์ใหม่ทั้งคู่) แล้วรันชุดเต็มใหม่บนต้นไม้ที่ merge แล้ว (ดู §5)

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` แล้วหักใบที่มี `.CONSUMED.txt` คู่ ⇒ ค้างหนึ่งใบ:

| ใบ | ทำอะไรรอบนี้ |
|---|---|
| `20260903_1649_COO-DECISION-...-next-queue-is-the-ground-ledger-after-relogin.md` | งานหลักของรอบ (§3) |

สร้าง `.CONSUMED.txt` แล้ว · เขียนตอบหนึ่งใบถึง COO (`1740`)

## 3. ทำอะไร

### 3.1 ข้อ 3 ของ `1649` ก่อน (หนี้ `0951`)

วัดเอง: `git merge-base --is-ancestor a386078054725215da2bb860fe83750db90e82a3 origin/main` ⇒ `YES` และ
`a386078...`'s merge commit (`9a140835`) เป็น HEAD ของ `main` พอดีตอนเริ่มรอบ ⇒ หนี้จ่ายแล้ว ไม่ต้องแก้
อะไรก่อนเริ่มข้อ 5

### 3.2 อ่านโค้ดที่มีอยู่ก่อนเขียนเทส

ไล่จาก `runtime.py:1328` (`self.mob_loot_cell = mob_loot.DropLedgerCell()` ใน
`PersistentGameSessionState.__init__`, คลาสที่ `runtime.py:1014` ภายใน `make_state_class`) →
`mob_loot.DropLedgerCell.__init__` (`mob_loot.py:2751-2757`, ไม่มีพารามิเตอร์แตะ store) →
`mob_loot.py:928-930` (HYPOTHESES text เดิม: "the ledger lives in the caller's process... this module
writes no database row") → `migrations/*.sql` ทั้งเก้าไฟล์ (ไม่มีตาราง ground/drop/loot) → `store.py`
(28 method สาธารณะ ไม่มีตัวไหนชื่อพ้อง) → `mob_loot.py:762` (`GROUND_DROP_DOES_NOT_PERSIST = True`) →
`docs/FUNCTIONAL_COVERAGE.json` (บันทึกช่องว่างเดียวกันมาหลายรอบของสาย B) — ครบทุกจุด ไม่มีอะไรต้องแก้
ขอบเขตของรอบนี้คือ**วัด**เท่านั้น

### 3.3 เทสใหม่ (pirate-force-server, ไฟล์เดียว ไม่แตะโค้ดจริง)

`tests/test_persistence_ground_ledger_measurement.py` (ไฟล์ใหม่ทั้งไฟล์ ของ LANE-DB เอง ฮาร์เนสทำซ้ำ
ไม่ import จาก `tests/test_choose_npc_call_site_loot_cell.py`):

1. `test_a_kill_in_one_login_leaves_the_ground_empty_for_the_next_login` — ล็อกอิน A ฆ่ามอนในฉาก 2 (1
   แถวบนพื้น) ล็อกอิน B (โทเคนอื่น ไฟล์ store เดียวกัน) วาปเข้าฉากเดียวกัน เห็น 0 แถว + คนละออบเจกต์
   `DropLedgerCell`
2. `test_the_cell_constructor_takes_no_store_and_no_character` — โครงสร้าง: constructor ไม่มีทางแตะ
   ดาต้าเบสได้เลย (`inspect.signature` + เช็ค `*args`/`**kwargs`)
3. `test_no_migration_creates_a_table_naming_ground_drop_or_loot` / `test_sqlitestore_has_no_method_
   naming_ground_drop_or_loot` — ไม่มีตาราง/เมธอดชื่อพ้อง
4. `test_ground_drop_does_not_persist_flag_agrees` — คู่ตรวจอิสระกับ `GROUND_DROP_DOES_NOT_PERSIST` +
   `FUNCTIONAL_COVERAGE.json`

## 4. ตรวจ pf-adversary — สามจุดจริง แก้ครบในคอมมิตเดียวกัน

ส่ง subagent ตรวจก่อนคอมมิตสุดท้าย (worktree แยก, มิวเทชันจริง ไม่ใช่แค่อ่านโค้ด) — พบ:

1. เทส constructor เดิมใช้ `co_varnames[:co_argcount]` มองไม่เห็น `**kwargs` — สาธิตจริง (แพตช์ให้แอบรับ
   `store=` ผ่านมิวเทชันในเวิร์กทรีแยก เทสเดิมยังเขียว) — **แก้แล้ว**: `inspect.signature` + เช็ค
   `VAR_POSITIONAL`/`VAR_KEYWORD` แยก ทวนมิวเทชันเดิมซ้ำเอง จับได้
2. เทส grep ตาราง migration เช็คทีละบรรทัดด้วย `startswith` หลบได้ด้วยการขึ้นบรรทัดใหม่ระหว่าง
   `CREATE TABLE` กับชื่อตาราง (SQL ใช้ได้จริง) — สาธิตจริง — **แก้แล้ว**: regex ข้ามทั้งไฟล์ ทวนมิวเทชัน
   เดิมซ้ำเอง จับได้
3. การสแกนด้วยชื่อ (ground/drop/loot) หลบได้เสมอด้วยชื่อไม่เกี่ยวข้อง (เช่น `floor_items`) — ไม่มีทางปิด
   ช่องนี้สนิทด้วยการสแกนชื่ออย่างเดียว ตรวจแล้วไม่มีตารางจริงในรีโปวันนี้ใช้ช่องนี้ — **แก้โดยไม่พึ่งการ
   สแกนซ้ำ**: เพิ่ม `test_ground_drop_does_not_persist_flag_agrees` (หลักฐานอิสระชั้นที่สอง) และเขียน
   ในดอกสตริงตรง ๆ ว่าการสแกนชื่อพิสูจน์ได้แค่อะไร

พบเพิ่ม: framing ของ "fresh token = relogin" ที่จริงคือคนละบัญชี (token = login name) — ไม่ใช่บั๊ก แต่แก้
คำอธิบายในดอกสตริงให้ตรง พร้อมเหตุผลว่าทำไมไม่กระทบคำตอบ (ไม่มี registry คีย์ด้วยโทเคนสำหรับ
`mob_loot_cell` เลย)

ไม่พบข้อบกพร่องอื่นที่บล็อกรอบนี้ ทวนไฟล์ migration ที่ใช้ทดสอบมิวเทชันชั่วคราวคืนสภาพเดิมครบ (`git status`
สะอาดก่อนคอมมิตทุกครั้ง)

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** ไม่มีเฟรมถูกส่งจริง ไม่มีคลิก ไม่มีหน้าต่างเปิด

### 5.2 wire-DB

**ก. เทสที่แตะ/เกี่ยวข้องโดยตรง** — ไฟล์ใหม่ห้าเทส + `test_choose_npc_call_site_loot_cell.py` +
`test_mob_loot.py` + `test_persistence_backpack_relogin.py`: `170 passed, 245 subtests passed` ไม่มี
FAILED

**ข. มิวเทชัน (โดยผมเองและโดย `pf-adversary` แยกกัน)** — ห้าจุดรวม (สามจุดที่ pf-adversary หา + สองจุด
ที่ผมทวนเองตอนสร้างเทสครั้งแรก: shared-cell mutant, ปลอมลายเซ็น constructor) จับได้ครบทุกจุด

**ค. ไม่มีอะไรของสายอื่นถูกแตะ** — ไฟล์เดียวที่เพิ่มคือ `tests/test_persistence_ground_ledger_
measurement.py` (ไฟล์ใหม่ ไม่แก้ไฟล์เดิมของ LANE-B/chief/LANE-A/LANE-E สักบรรทัด)

**ง. ชุดเต็ม — รันสองครั้งรอบนี้ ทั้งคู่จำเป็น (เหตุผลตามกฎบ้าน)**: ครั้งแรกก่อน push พบ `origin/main`
ขยับ (`#662` LANE-A merge, ไฟล์ใหม่ล้วน ไม่ชนกับของผม) ระหว่างทำงาน ⇒ merge เข้ากิ่ง (ไม่มี conflict) →
รันชุดเต็มใหม่บนต้นไม้ที่ merge แล้วจริง (ตามกฎ `NOW.md` บรรทัด 22: "ก่อน push ต้อง git fetch origin
main แล้วรันชุดเต็ม บนต้นไม้ที่ merge main แล้ว") — ครั้งแรก (ก่อน merge): `8830 passed, 323 skipped,
17396 subtests passed in 354.10s` · ครั้งที่สอง (คอมมิตสุดท้ายจริง หลัง merge): `8883 passed, 323
skipped, 17431 subtests passed in 348.85s` ไม่มี FAILED ทั้งคู่

**จ. มีไฟล์เทสใหม่ ⇒ ซ้อม `pytest_subset` + `skip_census` แยก** — `git clone` ทรีนี้ (คอมมิตสุดท้าย)
เข้าโฟลเดอร์ scratch (ไม่มี `pf_bridge` เป็นพี่น้อง) แล้วรันเหมือน `.github/workflows/gate-windows.yml`
ทำจริง: exclude list สร้างด้วย `grep -lE 'GameClient|capture_v141' tests/*.py` แล้วตัด
`test_foundation_legacy_seam.py` ออกจาก exclude list (เหมือน workflow บรรทัด 398-402 ทำ — รอบก่อนของ
ผม (`dskm1o`) เขียนว่า "ยกเว้น" ไฟล์นั้นแบบเดียวกัน) → `pytest_subset`: `7889 passed, 85 skipped, 15367
subtests passed` ไม่มี FAILED → `skip_census` (`tools/pf_pytest_precondition_census.py`):
`bridge_sibling ABSENT` ทุก skip ประกาศ+ปักครบ `RESULT: PASS` ไม่มีตัวเลข skip ขยับจากไฟล์ใหม่นี้เลย ·
ลบโคลนชั่วคราวทิ้งหลังตรวจเสร็จ

**ฉ. `apply_hp_damage`/M4** — ไม่ขยับ ไม่เกี่ยวกับรอบนี้เลย

## 6. nonclaims

1. **ไม่มีอะไร client-observable** ในรอบนี้
2. **รอบนี้วัดเฉพาะของที่ยังไม่ถูกเก็บ** — คนละคำถามกับของที่เก็บแล้วซึ่ง `0951`/`#660` ปิดไปแล้ว
3. **ไม่มีประตูถูกสร้างในรอบนี้** ตามคำสั่ง `1649` — เสนอรูปในจดหมายเท่านั้น รอ COO ตอบสามคำถามก่อน
4. **ไม่เคยรันบน canonical DB ของเจ้าของ** ทุกดาต้าเบสสร้างใน `TemporaryDirectory`
5. **M4 ไม่ขยับ**
6. `state_a`/`state_b` ในเทสคือคนละบัญชี (token = login name) ไม่ใช่บัญชีเดียวกันรีล็อกอิน — เขียนไว้ตรง ๆ
   ไม่กระทบคำตอบ (เหตุผลใน §3.2/จดหมาย)

## 7. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงานรันเฉพาะไฟล์ใหม่ก่อน (`tests/test_persistence_ground_ledger_measurement.py`) แล้วขยาย
  เป็นสี่ไฟล์ที่เกี่ยวข้อง
- ชุดเต็มรันสองครั้งตามเหตุผลใน §5.ง (ไม่ใช่การรันซ้ำโดยไม่จำเป็น — origin/main ขยับจริงระหว่างรอบ) +
  `pytest_subset`/`skip_census` แยกหนึ่งครั้งตามที่เขียนใน §5.จ
- **PR เซิร์ฟเวอร์ `pirate-force-server#664` เปิดแล้ว มี `PF-AUTOMERGE: v4` — รอ gate Windows ยังไม่ขึ้น
  `main` ณ เวลาที่ push ใบนี้**
- claim PR `#993` ของ `pf_bridge`: เติม marker ตอนจบรอบ (หลังไฟล์รอบนี้ push แล้ว) ตามหัวข้อล็อกรอบ

## 8. รอบหน้าทำอะไร

รอ COO ตอบสามคำถามในจดหมาย (`1740`) เรื่องรูปประตู (ใครเขียน / ตัวออกเลข `drop_key` ข้ามเซสชัน / ขอบเขต
รอบแรก) ก่อนเริ่มสร้าง migration + `store.py` method ใหม่ — ไม่เริ่มเองตามคำสั่ง `1649`

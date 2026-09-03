# DB round (`5d02mu`) — 2026-09-03T19:09+07:00 to 19:51+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260903_1809_7x8551_recover_pr664_windows_encoding.md`. รอบนั้นกู้กลไก, รอบนี้เป็นรอบแรก
ที่ทำเนื้องานของประตูของบนพื้นจริงตามคำตอบ `1843`.

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรกก่อนแตะอะไร (ฉบับ "ตรวจล่าสุด 2026-09-03 18:45 +07:00 โดย COO")

- **ไม่ขยับบรรทัดใดของ `NOW.md` โดยตรง** — บรรทัดที่เกี่ยวข้อง ("LANE-DB สร้างประตู commit_ground_drop/
  list_ground_drops_for_scene รอบ 19:01 หลัง `#666` ขึ้น main") คือคิวที่ COO เขียนไว้ล่วงหน้าแล้วว่าเป็นงาน
  ของสายนี้ — รอบนี้คือการ "ทำ" คิวนั้น ไม่ใช่การเปลี่ยนคิว ไม่มีสิทธิ์แก้ `NOW.md` เอง
- **P-0 · P-1 · P-2 · P-3 · GM-A · UI-A · UI-B · /speed · M4** นอกเขตของสายนี้ ไม่แตะแม้ไฟล์เดียว
- 🔴 ไม่แตะ `gm/` `speed_wire.py` `runtime.py` `app.py` `v141` `mob_loot.py`

## 1. ล็อกรอบ

- 19:09 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open ทั้งสองรีโปหัวข้อขึ้นต้น `[LANE-DB]`: ว่าง
  ทั้งคู่ (เห็น `[LANE-B] #1003`, `[LANE-A] #988`/`#1001` เปิดคู่ขนาน ไม่ใช่ของผม ไม่แตะ) ⇒ ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`92250c6e`) commit `rounds/DB_20260903_1909_5d02mu_claim.md`
  push แล้วเปิด `#1006 [LANE-DB] round 5d02mu: claim` ไม่มี `PF-AUTOMERGE: v4` ใน body ตอนเปิด
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open มีใบเดียวคือ `#1006` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ระหว่างรอบ `pirate-force-server` origin/main ไม่ขยับ (`eef0df7e` ตลอด, ตรวจซ้ำก่อนสร้าง `migrations/`
  ใหม่และก่อน push) · `pf_bridge` origin/main ไม่ได้ตรวจซ้ำระหว่างรอบเพราะรอบนี้ไม่มี merge conflict และ
  push ครั้งเดียวตอนจบ

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` แล้วหักใบที่มี `.CONSUMED.txt` คู่ ⇒ ค้างหนึ่งใบที่ไม่ใช่ประวัติศาสตร์เก่า
(ใบเก่าในโฟลเดอร์ `consumed/` ถือว่าเก็บเข้าคลังแล้วโดยกลไกก่อนหน้า ไม่ใช่ของค้างจริง — เนื้อหาถูกแทนที่ด้วย
รอบหลัง ๆ ทั้งหมดแล้ว):

| ใบ | ทำอะไรรอบนี้ |
|---|---|
| `20260903_1843_COO-DECISION-lane-db-build-the-ground-drop-door-now-*.md` | เนื้องานทั้งรอบ (§3) |

สร้าง `.CONSUMED.txt` แล้ว · เขียนจดหมายใหม่หนึ่งใบ (`1951`, ADDRESSEE: COO) ถึงปัญหาที่พบระหว่างทำงาน
(§4)

ระหว่าง merge `origin/main` ของ `pf_bridge` เข้ากิ่งตอนจบรอบ พบใบใหม่มาถึงเพิ่ม (`20260903_1945_COO-
DECISION-lane-db-letter-0640-was-answered-by-0720-no-work.md`, ADDRESSEE: LANE-DB): ไม่มีงานเพิ่ม
ยืนยันคิวตรงกับ `1843` ที่ทำไปแล้ว · มีข้อสังเกตหนึ่งข้อ — chief จะ re-open ledger ที่ขอบฉากทุกฉาก (`1943`
ข้อ 1) ⇒ ประตูอ่านต้องพร้อมให้ rehydrate ต่อ `scene_id` — `list_ground_drops_for_scene(scene)` ที่สร้างรอบ
นี้อ่านกลับทุกแถวของฉากเดียวอยู่แล้ว เทียบผ่าน `.casefold()` แบบเดียวกับ `mob_loot.scene_key` จึงพร้อมรองรับ
จุดเรียกนั้นทันทีที่ LANE-B ต่อสาย ไม่ต้องแก้อะไรเพิ่มฝั่งนี้ · สร้าง `.CONSUMED.txt` แล้ว ไม่มีงานทำเพิ่ม

## 3. ทำอะไร

### 3.1 ก่อนเริ่ม — ตรวจเลข migration ไม่ชน

`git fetch origin` แล้วดู `migrations/` บน `origin/main` สด: เลขสูงสุดคือ `009` · list PR `[LANE-DB]` เปิด
ในเซิร์ฟเวอร์: ว่าง (มีแค่ `#669` `[LANE-A]` ไม่แตะ `migrations/`/`store.py`) · `rounds/DB_*.md` ใบล่าสุด
(`7x8551`) ไม่ได้อ้างว่าทำ `010` ไปแล้ว ⇒ ใช้เลข `010` ได้ปลอดภัย

### 3.2 ประตู — ตามข้อ 3-5 ของใบ `1843`

- `migrations/010_ground_drops.sql` — ตารางเปล่าใหม่ `ground_drops` เท่านั้น ไม่มี `ALTER`/`UPDATE`/rebuild
  ⇒ ไม่เข้าเงื่อนไขบังคับ backup ของการ์ด `1112` ข้อ 3 (ตามที่ใบ `1843` ข้อ 5 ยืนยันไว้แล้ว ไม่ต้องแก้จุด
  เรียก `migrate()` ของ chief)
- คอลัมน์ตรงกับฟิลด์ของ `mob_loot.GroundDrop` ทุกตัว (`drop_key`,`item_id`,`quantity`,`x`,`y`,`z`,
  `mob_identity`,`killer_identity`,`scene`) บวกคอลัมน์ `scene_fold` (`scene.casefold()`) ที่ `UNIQUE(
  scene_fold, drop_key)` อ้างถึงจริง — เก็บ `scene` แบบดิบไว้แยกเพราะ `mob_loot._require_scene`'s ตัวเองยืน
  ยันว่าเคสไม่ถูกทำให้เท่ากันโดยเจตนา (`bg0002` vs `Bg0002` มีอยู่จริงในคอร์ปัส) แต่การเทียบทุกที่ต้องผ่าน
  `.casefold()` เท่านั้น (`mob_loot.scene_key`) — ถ้า `UNIQUE` อ้างคอลัมน์ดิบ สองตัวสะกดของฉากเดียวกันจะไม่
  ชนกันเลย ซึ่งเป็นข้อบกพร่องเงียบตรงข้ามกับที่ COO สั่ง
- `src/pirateforce_foundation/persistence_ground_drops.py` — `GroundDropRow` frozen dataclass โมดูลใหม่
  ไม่แตะ `mob_loot.py` ไม่ import มัน (charter `1100`)
- `store.py` — เมธอดใหม่สองตัว `commit_ground_drop`/`list_ground_drops_for_scene` ไม่แก้ behavior เมธอด
  เดิมสักตัว (grep `git diff` ยืนยัน: มีแค่ import ใหม่หนึ่งบรรทัด + token constant ใหม่หนึ่งตัว + เมธอดใหม่
  สองตัวถูกแทรกก่อน `_character`) · ไม่รับ `sid`/`character_id` เพราะของบนพื้นเป็นของฉาก ไม่ใช่ของเซสชัน
  หรือของตัวละคร · collision (`UNIQUE` ชน) ⇒ raise `ValueError` + พิมพ์ `GROUND_DROP_KEY_COLLISION_
  REFUSED_TOKEN` ก่อน raise (บรรทัดคอนโซล ตามข้อ 3 ของใบ) · อ่านกลับหลังเขียนทุกครั้ง คืนค่าเป็น
  `GroundDropRow` ที่อ่านจากแถวที่เพิ่งเขียนจริง ไม่ใช่ echo พารามิเตอร์กลับ

### 3.3 pf-adversary — พบสองจุดจริง แก้ครบก่อน commit

ส่ง subagent ตรวจก่อน commit ตามการ์ด พบ:

1. **handler เหมารวมทุก `sqlite3.IntegrityError` เป็นคีย์ชน** — สาธิตจริง: ปิด validator `quantity` ของ
   Python ชั่วคราว (worktree แยก) ส่ง `quantity=0` เข้าไป ได้ผลลัพธ์ `GROUND_DROP_KEY_COLLISION_REFUSED`
   บนคอนโซลและ `ValueError("...already on the ground...")` ทั้งที่ไม่มีแถวอื่นอยู่เลย — วินิจฉัยผิดตัวเต็ม ๆ
   ⇒ แก้เป็นเช็ค `"UNIQUE constraint failed" not in str(exc)` ก่อน แล้ว `raise` ของเดิมถ้าไม่ใช่ collision
2. **CHECK ของ `x`/`y`/`z` ไม่กัน `+-Infinity`** — สาธิตจริง: ปิด `math.isfinite` ของ Python ชั่วคราว เขียน
   `x=inf` ผ่าน CHECK เดิม (`typeof(x)='real'`) ได้จริง เพราะ SQLite ตอบ `typeof()` ว่า `'real'` ให้ infinity
   ด้วย ⇒ เพิ่มขอบเขต `BETWEEN -1.7976931348623157e308 AND 1.7976931348623157e308` (ช่วงจำกัดของ IEEE
   double) ซึ่งการเทียบกับ `+-Infinity` และกับ `NaN` ล้มเสมอโดยธรรมชาติของเลขทศนิยม ⇒ ตอนนี้กันจริง

ทั้งสองจุดมีเทสของตัวเองในไฟล์ใหม่ (`ANonCollisionIntegrityErrorIsNotMislabelledTests`) ยืนยันด้วยมิวเทชัน
เดียวกับที่ agent สาธิต ไม่พบอะไรที่บล็อกเพิ่มหลังแก้

### 3.4 ผลกระทบข้ามเขต — สามไฟล์ แก้ได้สองตามสิทธิ์เดิม เหลือหนึ่งเขียนใบถาม

รันชุดเต็มครั้งแรก (ก่อนแก้ pf-adversary's findings เสร็จ ระหว่างพัฒนา) พบ 4 แดง ตรวจแยกทีละตัวว่าของใคร
(ดู §4 nonclaims ข้อ 3 สำหรับรายละเอียดวิธีแยก):

- `tests/test_persistence_birth_defaults_009.py` (**ของ LANE-DB เอง** จากรอบก่อน ๆ) — `_store_at_009()`/
  `_mutated_dir` ใช้ไดเรกทอรี `MIGRATIONS` (ทั้งต้นไม้จริง) เป็น "สภาพที่ 009" มาตลอด ใช้ได้เพราะ 009 เคย
  เป็นไฟล์ล่าสุดจริง ตอนนี้ `010` แซงแล้วเลยพัง 5 เทส ⇒ เพิ่ม `self.upto_009` (ไดเรกทอรีกรองเฉพาะ ≤9 แบบ
  เดียวกับ `self.upto_008` ที่มีอยู่แล้ว) แล้วเปลี่ยนทุกจุดที่ตั้งใจหมายถึง "สภาพ 009" ให้ใช้มันแทน
- `tests/test_persistence_speed_walk_seed_008.py` (ของ LANE-DB) — หมุด `[8, 9]` ปักตรง ๆ ว่า pending
  versions มีสองตัว คอมเมนต์เดิมบอกอยู่แล้วว่า "a tenth file nobody looked at" จะมาวันหนึ่ง ⇒ แก้เป็น
  `[8, 9, 10]`
- `tests/test_birth_insert_names_only_the_three.py` (ของ LANE-DB) — โพรบมิวเทชันฮาร์ดโค้ด `010` เป็น "ช่อง
  ว่างถัดไป" ชนกับ `010_ground_drops.sql` จริงตรง ๆ (`RuntimeError: duplicate migration version`) ⇒ เปลี่ยน
  เป็นคำนวณจาก `max(...)+1` ของต้นไม้จริง กันชนซ้ำกับ migration ถัดไปทุกเบอร์ไม่ใช่แค่เบอร์นี้
- `tests/test_persistence_ground_ledger_measurement.py` (ของ LANE-DB รอบก่อน `ld70iq`) — คลาส
  `NoSchemaExistsForGroundDrops` เคยพิสูจน์ว่า "ไม่มีตาราง/เมธอดชื่อพ้อง ground/drop/loot" ซึ่งตอนนี้เป็นเท็จ
  โดยเจตนา (COO สั่งสร้างเอง) ⇒ เปลี่ยนชื่อคลาสเป็น `TheGroundDropDoorIsExactlyWhatWasOrderedTests` และ
  พลิกทั้งสองเทสให้ pin ชุดที่คาดหวังแทน (ตาราง `ground_drops` หนึ่งตัว, เมธอด `commit_ground_drop`/
  `list_ground_drops_for_scene` สองตัว) — ยังทำหน้าที่เฝ้าระวังเดิม (จับตารางหรือเมธอดชื่อพ้องที่ไม่มีการ
  ตัดสินใจรองรับ) แค่ชี้ไปที่ความจริงข้อใหม่แทนข้อเก่า
- `tests/test_foundation.py` (**ไม่ใช่ของ LANE-DB**) กับ `tests/test_item_move_capture.py` (**ไม่ใช่ของ
  LANE-DB**) — หมุดนับจำนวน migration แบบเดียวกัน (`[1..9]`, `9`) แต่ **มีใบสิทธิ์ทั่วไปอยู่แล้ว**
  (`20260901_1416` + คำตอบ chief `20260901_1459`: "ทุกสายที่ลง migration ใหม่จะชนหมุดสองตัวนี้ตลอดไป แก้
  บรรทัดเดียวได้") ⇒ แก้บรรทัดเดียวจริงตามสิทธิ์ พร้อมคอมเมนต์อ้างใบทั้งสอง
- `tests/test_npc_interaction_wire.py` (**ไม่ใช่ของ LANE-DB**) — `EXPECTED_TABLES` เซตตายตัว ไม่มีใบใดให้
  สิทธิ์ ⇒ **ไม่แตะ** เขียนใบ `1951` ถาม COO แทน (รายละเอียดเต็มในใบ)
- `tests/test_mob_aggro.py` — วัดซ้ำบน `origin/main` สะอาดด้วย `git stash -u` (สำคัญ: `stash` เฉยๆ ไม่ดึง
  ไฟล์ untracked ออก ต้องมี `-u`) ⇒ แดงเหมือนกันแม้ไม่มีการเปลี่ยนแปลงของผมเลย = ไม่ใช่ของรอบนี้ ไม่แตะ

## 4. หลักฐาน — สองชั้นแยกกัน

### 4.1 client-observable

🔴 **ศูนย์** — ไม่มีจุดเรียกที่ทำให้ของตกจริงในเกม (จุดเรียกตอนของตกเป็นของ LANE-B ตามใบ `1843` ข้อ 3)
ไม่มีเฟรมถูกส่ง ไม่มีคลิก

### 4.2 wire-DB

**ก. ไฟล์ใหม่เดี่ยว** (`tests/test_persistence_ground_drops_010.py`) — `33 passed, 16 subtests passed`

**ข. รวมกับไฟล์ที่เกี่ยวข้อง/ถูกแก้** (14 ไฟล์: ของใหม่ + หกไฟล์ LANE-DB ที่แก้ + สองไฟล์นอกเขตที่แก้ตาม
สิทธิ์ + `test_mob_loot.py`/`test_choose_npc_call_site_loot_cell.py`/`test_store_acquired_item_insert.py`
เพื่อยืนยันไม่แตะ `mob_loot.py`/backpack) — `621 passed, 699 subtests passed` ไม่มี FAILED

**ค. ไม่มีอะไรของสายอื่นถูกแตะ (นอกจากสองไฟล์ที่มีใบสิทธิ์ชัดเจน)** — `git diff --stat` ยืนยัน 10 ไฟล์:
สี่ไฟล์ใหม่/แก้ของ LANE-DB เอง (migration, module ใหม่, store.py, เทสใหม่) + สี่ไฟล์เทสของ LANE-DB เอง
(009/008/ground_ledger/birth_names) + สองไฟล์นอกเขตที่มีใบสิทธิ์ (`test_foundation.py`,
`test_item_move_capture.py`) — ไม่แตะ `mob_loot.py`/`runtime.py`/`app.py`/`gm/`/`v141` เลยสักไบต์

**ง. ชุดเต็ม — รันสองครั้งรอบนี้ ทั้งคู่จำเป็น**: ครั้งแรก (หลังโค้ด+เทสของตัวเองพร้อม ก่อนพบ+แก้ผลกระทบ
ข้ามเขต) `4 failed, 8919 passed, 323 skipped, 17431 subtests` — ใช้ระบุว่า 4 ตัวไหนเป็นของใคร (§3.4)
ครั้งที่สอง (commit สุดท้ายจริง หลังแก้สองไฟล์ที่มีสิทธิ์เสร็จ) `2 failed, 8921 passed, 323 skipped,
17447 subtests` ไม่มี FAILED อื่น — เหลือแค่สองตัวที่ระบุแล้วว่าไม่ใช่ของรอบนี้ (mob_aggro) และของรอบนี้แต่
บล็อกด้วยเขตเขียน (npc_interaction_wire) เหตุผลที่ต้องรันสองครั้ง: ครั้งแรกจำเป็นเพื่อแยกแยะสาเหตุแดงแต่ละ
ตัวก่อนตัดสินใจว่าไฟล์ไหนแก้ได้/ไฟล์ไหนต้องเขียนใบ — ไม่ใช่การรันซ้ำเพราะลืมหรือเพราะ `origin/main` ขยับ

**จ. มีไฟล์เทสใหม่ ⇒ ซ้อม `pytest_subset`/`skip_census` แยกในโคลนไม่มี `pf_bridge` ข้าง ๆ**
(ตาม `.github/workflows/gate-windows.yml` จริง: exclude list `grep -lE 'GameClient|capture_v141'
tests/*.py` แล้ว **ตัด `test_foundation_legacy_seam.py` ออกจาก exclude list** เพราะ workflow รันมันแยก
เป็นสเต็ป "seam" ต่างหากแล้วยังใส่กลับเข้า `pytest_subset` ด้วย — ข้อผิดพลาดที่พบเองระหว่างซ้อม: ครั้งแรกลืม
ตัดไฟล์นี้ออกจาก exclude list ได้ 49 โมดูล census เตือน "GATE EXCLUSION DRIFT" ทันที แก้เป็น 48 โมดูลตรง
กับที่รอบก่อน (`7x8551`) เคยรายงานไว้ แล้วรันใหม่) → `pytest_subset`: `7980 passed, 85 skipped, 15420
subtests` **`2 failed`** (สองตัวเดียวกับ §3.4/§4.4) → `skip_census`
(`tools/pf_pytest_precondition_census.py --report ... --excluded ...`): `RESULT: PASS` ทุก skip ประกาศ+
ปักครบ ไม่มีตัวเลข skip ขยับจากไฟล์ใหม่นี้ (85 skipped ตรงกับ baseline) · ลบโคลนชั่วคราวทิ้งหลังตรวจเสร็จ

## 5. nonclaims

1. **ไม่มีอะไร client-observable** ในรอบนี้ (ตามคาด — จุดเรียกยังไม่มี)
2. **ประตูอ่านกลับได้จริง แต่ยังไม่มีใครเรียกมันตอนของตกจริง** — จุดเรียก + ตัวออกเลข `drop_key` ระดับ
   เซิร์ฟเวอร์เป็นของ LANE-B (ใบ `1844`) ตามชาร์เตอร์ ไม่ใช่รอบนี้
3. **ไม่เคยรันบน canonical DB ของเจ้าของ** ทุกดาต้าเบสสร้างใน `TemporaryDirectory`
4. **`ground_drops` ทำเทสนอกเขตแดงจริง หนึ่งไฟล์ยังไม่ได้แก้** (`test_npc_interaction_wire.py`) — PR
   เซิร์ฟเวอร์เปิดแล้วแต่**ไม่มี `PF-AUTOMERGE: v4`** จนกว่า COO จะตอบใบ `1951`
5. **ไม่มีการลบ/expire แถวใด ๆ** ตามขอบเขตที่ COO สั่งไว้ (`1843` ข้อ 5) — ทุกแถวที่เขียนแล้วอยู่ถาวรจนกว่า
   จะมีตัว publisher ลบจริงในรอบถัดไป

## 6. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงานรันเฉพาะไฟล์ที่เกี่ยวข้องก่อน (`test_persistence_ground_drops_010.py` แล้วขยายเป็น 14 ไฟล์)
- ชุดเต็มรันสองครั้ง เหตุผลตาม §4.ง (แยกสาเหตุแดง ไม่ใช่ลืม) + `pytest_subset`/`skip_census` แยกอีกหนึ่ง
  ครั้ง (มีไฟล์เทสใหม่)
- **PR เซิร์ฟเวอร์ `pirate-force-server#672` เปิดแล้ว ไม่มี `PF-AUTOMERGE: v4`** — ตั้งใจ รอคำตอบใบ `1951`
  ก่อน (ไม่ใช่ "เปิดแล้ว รอ gate" ตามปกติ — รอบนี้ยังไม่พร้อมส่งให้ระบบ merge)
- claim PR `#1006` ของ `pf_bridge`: **ไม่เติม marker รอบนี้** เพราะ PR เซิร์ฟเวอร์ยังไม่มี marker ตามกติกา
  (ล็อกยังไม่ปลด รอบหน้า/รอบที่ตอบใบ `1951` แล้วจะปลดให้)

## 7. รอบหน้าทำอะไร

1. **ตรวจว่า COO ตอบใบ `1951` หรือยัง** — ถ้าตอบแล้วและอนุญาตให้แก้ `tests/test_npc_interaction_wire.py`
   (ทางใดทางหนึ่งใน 3 ทางที่เสนอ) แก้ตามนั้น รันชุดเต็มใหม่ยืนยันเขียวสนิท (0 แดง) แล้วเติม
   `PF-AUTOMERGE: v4` ให้ทั้ง PR เซิร์ฟเวอร์และ claim PR ปลดล็อก
2. ถ้ายังไม่ตอบ: ทำงานคิวถัดไปที่ไม่ชนไฟล์นี้ไม่ได้ เพราะล็อกรอบยังถืออยู่ที่ PR `#1006` — รอบถัดไปของ
   LANE-DB (นาทีถัดไปที่ `:01`) จะเห็น `#1006` เป็นใบที่ยังไม่ปลด อายุยังไม่เกิน 2-3 ชม. ⇒ ต้องตรวจ commit
   ล่าสุดตามเกณฑ์อายุปกติของการ์ดก่อนตัดสินใจ takeover/ถอย
3. ตรวจผล gate ของ `#672` เอง (แม้ไม่มี marker gate ก็ยังรันให้เพราะเป็น PR ปกติ) — ถ้าแดงจากเหตุอื่นที่ไม่
   เคยเห็นในคลาวด์ (เช่น cp1252 แบบรอบ `7x8551`) ให้กู้บนกิ่งเดิม ไม่เริ่มใหม่

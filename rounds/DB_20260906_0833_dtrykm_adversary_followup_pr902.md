# LANE-DB round `dtrykm` -- pf-adversary follow-up on `#896` (owed), found and fixed a real bug, `#902`

รหัสรอบ: `dtrykm` · เวลาเริ่ม: 2026-09-06T08:33+07:00 · claim (ไม่ใช่ takeover)

## 0. ขยับ NOW/M ข้อไหน
`NOW.md` บรรทัด "🔴 สวมอาวุธ (`0345`/`0156`)": **ไม่ขยับ**. ทาง (ก) ยังคง `merged: true` บน
`pirate-force-server#883` (ไม่เปลี่ยนจากรอบก่อน). ทาง (ข) `RE-272`/`GT-272` ยังไม่มีผลจับจริง
(`grep -in "RE-272.*RESULT\|GT-272.*RESULT"` ทั่ว `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` = 0 hit
ทั้งต้นรอบ 08:33 และท้ายรอบ 08:52) -- ยังรอเครื่อง Panya เหมือนเดิม เดดไลน์ 14:00 ยังไม่ถึงครึ่งทาง จึง
ยังไม่ทวง COO

รอบนี้จึงหยิบข้อ 6 ของ "รอบหน้าทำอะไร" ในไฟล์รอบก่อน (`uu5zs7`): เซสชันนี้มี Agent tool ที่เรียก
`pf-adversary` ได้จริง (ต่างจากรอบก่อนที่ `ADVERSARY_UNAVAILABLE`) -- เรียกตามหนี้ที่ค้างไว้ก่อนหยิบงาน
อื่นใด

## 1. ล็อกรอบ
`git fetch origin main` แล้ว `list_pull_requests` (pf_bridge, open): มีแค่ `[LANE-E] round d5igq0: claim`
(`#1440`) -- ไม่มีล็อกค้างของสายตัวเอง เช็คสองรีโป `git checkout -B` จาก `origin/main` สด (pf_bridge:
`claude/kind-lovelace-dtrykm`, server: `claude/intelligent-mendel-dtrykm`) เปิด claim `pf_bridge#1454`
list ซ้ำทันที: มีใบเดียวคือของตัวเอง (บวก `#1440` ของ LANE-E) ⇒ ไม่แพ้ ทำงานต่อ

## 2. แหล่งความจริงที่อ่านตามลำดับ
1. `NOW.md` (fetch สด ต้นรอบ 08:33 และท้ายรอบ 08:52) -- ไม่มีอะไรใหม่สำหรับ DB ทั้งสองครั้ง
2. mailbox `ADDRESSEE: DB` ไม่มี `.CONSUMED.txt` คู่: **ว่างเปล่า** (loop ทุกไฟล์ `notes_to_chief/*.md`
   grep คำต่อคำ ไม่ใช่ substring ของ path อื่น)
3. `AGENTS.md` §7: อ่านทั้งหมด ไม่มีกฎใหม่ที่ขัดกับรอบนี้
4. ไฟล์รอบล่าสุด `rounds/DB_20260906_0704_uu5zs7_hp_pair_audit_backlog_item.md` หัวข้อ "รอบหน้าทำอะไร":
   ข้อ 2 (เช็ค `#896` merge) และข้อ 6 (สั่ง adversary รอบหน้าถ้ามี) คือสิ่งที่รอบนี้ทำ
5. ไม่มีจดหมาย broadcast ใหม่ที่ยังไม่ consume

## 3. งานที่ทำจริง

### 3.1 ยืนยันสถานะซ้ำ
- `pull_request_read get` + `git merge-base --is-ancestor` ยืนยัน `pirate-force-server#896`
  (`2d3ec2c75fbb6291820414616ebe16a26be00aa2`) เป็น ancestor ของ `origin/main` จริง (ไม่ใช่แค่เชื่อฟิลด์
  `merged` ของ API)
- `GT-255`: `grep "^ATTENDED:"` ในช่วงใบ = 0 hit ยังไม่ถูก chief วางบล็อก -- ไม่ใช่สิ่งที่ DB ทำต่อได้เอง

### 3.2 pf-adversary บนโค้ดของ `#896` ที่ merge แล้ว (Agent tool มีจริงรอบนี้)
สั่ง `pf-adversary` (subagent) รีวิว `persistence_hp_pair_audit.py` + `SQLiteStore.hp_pair_audit()` +
`tests/test_persistence_hp_pair_audit.py` บน `origin/main` (กิ่งเดิมของ `#896` ถูกลบไปแล้วหลัง merge --
รีวิวโค้ดชุดเดียวกันที่อยู่บน main แทน) ทำงานใน git worktree แยก ไม่แตะ checkout จริง

**ผล -- CONFIRMED บั๊กจริง**: `_PREDICATE[HP_MAX_ZERO]` เดิม `hp_max = 0` ไม่มีการ์ด `IS NOT NULL` ในขณะที่
อีกสองเงื่อนไขมีการ์ดครบ -- SQL three-valued logic ทำ `hp_max = 0` ประเมินเป็น `NULL` (ไม่ใช่ `FALSE`)
เมื่อ `hp_max IS NULL` ผลคือถ้าทุกแถวในตาราง `hp_max IS NULL` (เงื่อนไข #1 เอง) `SUM(hp_max = 0)` คืน SQL
NULL รายงานพิมพ์ `not-counted` สำหรับ `hp_max_is_zero` ทั้งที่คำตอบจริงคือ `0` -- ตรงข้ามเจตนาของ sentinel
`not-counted` (แยก "นับไม่ได้" จาก "นับแล้วได้ศูนย์") ตัวแทนเจ้าของ agent ยืนยันด้วยการรันจริงบน
`store.hp_pair_audit()` (SQLite ที่ migrate จริง สร้างตัวละครจริงสองตัว บังคับ `hp_max = NULL` ทั้งคู่) --
ได้ `HP_MAX_ZERO_any=None`/`HP_MAX_ZERO_live=None` พิมพ์เป็น `not-counted` ทั้งคู่

บั๊กรอง (severity ต่ำ, ไม่กระทบพาธจริงวันนี้): `format_report`'s `characters_any` ไม่ผ่าน `_count()`
เหมือนฟิลด์อื่น -- `COUNT(*)` ไม่คืน NULL บนพาธจริงเลยไม่มีผลตอนนี้ แต่เป็นความไม่สมมาตรที่ไม่มีเทสจับ

ทั้งสองข้อมี file:line + failure scenario ที่วัดจริง (ไม่ใช่เดา) -- ไม่มีบั๊กปลอมที่รายงาน

### 3.3 แก้บั๊ก -- `pirate-force-server#902`
ตาม `COMMON_LANE_ROUND.md` §"เจอบั๊กจริงที่ตอนนั้นอยู่บน main แล้ว = เปิดใบแก้ตัดจาก main ทันที ไม่รอคิว":
- `_PREDICATE[HP_MAX_ZERO]` เพิ่ม `IS NOT NULL AND` การ์ด เหมือนอีกสองเงื่อนไข
- `format_report`'s `characters_any` ห่อด้วย `_count()` เหมือนฟิลด์อื่น
- เทสถดถอย 2 ใบใหม่ใน `tests/test_persistence_hp_pair_audit.py`:
  - `AllRowsNullDoesNotHideARealZeroTests`: สร้างสองตัวละครจริง ตั้ง `hp_max = NULL` ด้วย raw SQL (แบบ
    เดียวกับ `EachConditionIsReallyReachableTests` ทำ -- `write_typed_attributes` ปฏิเสธ `None` เอง
    ตามดอคของมัน) ยืนยัน `hp_max_is_zero_any`/`_live` = `0` ไม่ใช่ `None`
  - `TheCharactersAnyLineNeverPrintsABarePythonNoneTests`: `format_report({"database": "/x"})` ต้องไม่มี
    `any=None`
  ยืนยันมือว่าเทสแดงก่อนแก้ (ย้อน predicate ชั่วคราวแล้วรัน เห็น `AssertionError: None != 0`) เขียวหลังแก้

**กับดักระหว่างทาง**: ดราฟต์แรกของเทสใหม่พยายามใช้ `write_typed_attributes(hp_max=None)` เพื่อบังคับ
`hp_max IS NULL` -- ประตูนั้นปฏิเสธ `None` ตามดอคของมันเอง (`TypedAttrError`) และ
`create_character`'s ก็ seed `hp_max` จริงตั้งแต่เกิด (ไม่ใช่ `NULL` ตาม default) ต้องเปลี่ยนไปใช้ raw SQL
`UPDATE` แบบเดียวกับที่ `test_hp_max_null_survives_the_column_check` ใช้อยู่แล้ว

### 3.4 ชุดเต็ม + preflight + PR
`git fetch origin main` -> merge เข้ากิ่ง (ไม่ชนกัน) -> `pytest tests/` ชุดเต็มครั้งเดียว = **12024
passed, 365 skipped, 0 failed** (428s) -> `python3 tools_bridge/pf_gate_preflight.py --repo` = PASS ทุก
ช่อง

ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมไคลเอนต์ (query อ่านอย่างเดียว) ⇒ เปิดตรงได้ ไม่ draft

Body ตรวจผ่าน `pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage final` ก่อนเปิด = PASS เปิด
`pirate-force-server#902` แล้ว `pull_request_read get` ยืนยัน body ที่ GitHub เก็บจริงมี marker บรรทัด
เดียวคำต่อคำ

## 4. ชุดเทสของรอบ
`tests/test_persistence_hp_pair_audit.py` (19 ใบ, 2 ใหม่) + ชุดเต็ม 12024 passed / 365 skipped / 0
failed

## 5. หลักฐาน -- สองชั้นแยกกัน
### 5.1 client-observable
ศูนย์ -- reporting door อ่านอย่างเดียว ไม่มีอะไรถึงจอผู้เล่น

### 5.2 wire/DB
`pirate-force-server#902` (`html_url`, ยืนยัน body ผ่าน `pull_request_read get`) · เทส 19 ใบเขียว + ชุด
เต็ม 12024 passed 0 failed · `pf_gate_preflight.py` PASS ทั้ง `--repo` และ `--pr-body --pr-stage final`

## 6. nonclaims
1. ไม่อ้างว่ารันบน DB จริงของเจ้าของ -- ยังไม่รัน (`0749` ห้ามก่อน `0156` ปิด)
2. ไม่อ้างว่า `#902` คืองานหลักของ `0156` -- ยังเป็นงานสำรอง (adversary debt) เหมือนเดิม
3. ไม่อ้างว่า RE-272/GT-272 มีผลจับจริงแล้ว -- ยังรอเครื่อง Panya
4. ไม่อ้างว่าบั๊กรอง (`characters_any`) เคยกระทบพาธจริง -- แค่ inconsistency ที่ latent เท่านั้น

## 7. รอบหน้าทำอะไร
1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. เช็คว่า `pirate-force-server#902` merge หรือยัง (`merge-base --is-ancestor`)
3. เช็คว่า `RE-272-RESULT`/`GT-272` มาหรือยัง -- มาแล้วเขียน migration ใหม่รับผลเป็นงานแรก
4. เช็คว่า chief วางบล็อก `ATTENDED:` ของ `GT-255` แล้วหรือยัง
5. ถ้าไม่มีความคืบหน้าจากเครื่อง Panya ใน 6 ชม.จาก `0345`/`0404` (ราว 09:45-10:04) ⇒ ทวง COO
6. คิวว่าง ⇒ ปลด scenario ที่พิสูจน์แล้วในเขตตัวเอง 1 ตัว (`docs/PROMOTION_BACKLOG.md`) ตามงานสำรองมาตรฐาน

## งานสำรอง (ทำเมื่องานหลักติด)
1. เฝ้าคำตอบ chief/COO/ผลจับ (เดดไลน์ 14:00) เป็นอันดับหนึ่ง
2. คิวเดิม: ชิ้น 2/3/4 ของ PLAYER/CHARACTER รอผล RE runner, ประตูเควสรอ chief whitelist

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ แต่แก้บั๊กจริงที่เคยขึ้น main แล้วให้ตัวเลขผิด
(`not-counted` ปลอมสำหรับเงื่อนไขที่จริงแล้วเป็นศูนย์) | `pirate-force-server#902` (เปิดแล้ว ไม่ draft มี
marker, ยืนยันผ่าน `pull_request_read get`), 2 เทสใหม่เขียว, ชุดเต็ม 12024 passed 0 failed,
`pf_gate_preflight.py` PASS ทั้ง `--repo` และ `--pr-body --pr-stage final`

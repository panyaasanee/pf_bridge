# DB round (`wgu3vp`) — 2026-09-04T04:33+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_0233_jso4qw_still_locked_on_door_b.md` — รอบนั้นวัดว่า `1101`
(HP/เลเวลถาวร) ยังล็อกรอ Door B ไม่มีงานอื่นในเขตเขียนของ DB ระหว่างรอบนั้นถึงรอบนี้ COO ออก
`PANYA-DECISION 20260904_0328` / `COO-ORDER 20260904_0329`: **PLAYER/CHARACTER เป็นงานชั่วคราวของ
LANE-DB มาก่อนทุกอย่างในคิว** (แทนที่ "DB ว่างได้ ไม่หาเรื่องทำ" ชั่วคราว) รอบนี้เริ่มชิ้น 1/5

## NOW.md — รอบนี้ขยับข้อไหน

**ไม่ขยับบรรทัดใดของ `NOW.md`** — ไม่มีสิทธิ์แก้ไฟล์นั้นเอง หัวข้อ "บันไดไมล์สโตน" บรรทัด
"PLAYER/CHARACTER = LANE-DB งานชั่วคราว ... (1) class ที่เลือกจาก `CreateActorVital` → `class_id`"
ยังไม่ถึงเกณฑ์ย้าย — โค้ด+เทสของชิ้น 1 ขึ้น PR แล้วแต่ **ยังไม่ merge main** และยังไม่ได้ต่อสายเข้า
create/login จริง (สองจุดนั้นอยู่นอกเขตเขียนของ DB ขอ chief ต่อในจดหมายรอบนี้) `GT-215` ที่ NOW.md
อ้างว่าจะปิดเมื่อ "ชิ้น 1 ขึ้น main" จึงยังไม่ปิด

## 1. ล็อกรอบ

- 04:03+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่ต้องปลดล็อกใคร ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`4ff23c8d`) commit `rounds/DB_20260904_0403_wgu3vp_claim.md`
  push แล้วเปิด `pf_bridge#1056 [LANE-DB] round wgu3vp: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1056` ของผมเอง (มี `#1054
  [LANE-CS]`, `#1055 [LANE-UI]` เปิดอยู่ — ไม่ใช่ล็อกของสายนี้ ไม่แตะ) ⇒ ไม่แพ้ ทำงานต่อ
- ก่อนเปิด PR ฝั่งเซิร์ฟเวอร์: `git fetch origin main` ซ้ำ (`pirate-force-server` main = `21a85f51`
  ไม่ขยับ) list `[LANE-DB]` open ใน `pirate-force-server`: ว่างเปล่า (มีแค่ `#698 [LANE-E]` ไม่ใช่ของ
  สายนี้) ⇒ ไม่ชนใคร ไม่มีไฟล์ migration ใหม่รอบนี้จึงไม่มีเลขให้ชน

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` หักใบที่มี `.CONSUMED.txt` คู่ ⇒
ใบเดียว: `20260904_0329_COO-ORDER-lane-db-player-character-is-yours-now-...md` (PLAYER/CHARACTER
5 ชิ้น) — สร้าง stub `.CONSUMED.txt` แล้ว (งานยังไม่จบ ชิ้น 2-5 ต่อจากรอบนี้ผ่านไฟล์รอบ ไม่ใช่กลับไป
อ่านใบเดิมซ้ำ ตามกติกา "อ่าน rounds/DB_* ล่าสุด ทำต่อ")

ส่งจดหมายออกหนึ่งใบ: `20260904_0423_LANE-DB-CORE-REQUEST-class-id-resolver-built-needs-two-hookups.md`
(ADDRESSEE: chief, cc: COO/LANE-A) — ขอสองจุดเสียบนอกเขตเขียนของ DB (ดูข้อ 3) และขอ COO ตัดสินเรื่อง
backfill ตัวละครเก่า (ข้อ 3 ของจดหมาย) — ผมไม่ตัดสินเอง

## 3. ทำอะไร

### 3.1 ทำไมไม่เชื่อ tag `0x19` ตรง ๆ

`COO-DECISION 20260903_1943` ข้อ 3 (ใบล่าสุดของประเด็นนี้ อ่านสดรอบนี้): tag `0x19` = class id ยัง
เป็นสมมติฐาน ยืนยันจากตาราง gamedata ที่ commit แล้วเท่านั้น ห้ามเปิด RE ใหม่ — ตรงกับที่สายนี้เอง
เคยเตือนไว้แล้วในจดหมาย `20260902_1650` (tag `0x19` ใน `CreateActorVital` ชนกับ `ActorAttr.class_id`
คนละ offset เป็นกับดัก) จึงไม่แตะ `actor_wire` tag `0x19` เลยในโค้ดรอบนี้

### 3.2 สร้าง `persistence_class_id.py`

`resolve_class_id(dress_chest, dress_leggings, slot_rhand) -> int | None` เทียบสามค่ากับ
`CLASS_PRESETS` (5 แถว transcribe ตรงจาก `gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv` ที่
ผมเปิดอ่านเองจาก `pf_bridge` — คอลัมน์ `n_ID`/`n_DRESS_CHEST`/`n_DRESS_LEGGINGS`/`n_SLOT_RHAND`
ไม่ซ้ำกันข้ามคลาสทั้งห้าทุกคอลัมน์) ตรงเป๊ะหนึ่งแถวเท่านั้นถึงคืนค่า ไม่งั้นคืน `None` เสมอ

**ตั้งใจไม่ import ตัวถอดรหัส `AvatarAttr` ตัวจริง**: โมดูลนั้นยังเป็น "CHECK ไม่ใช่ wiring" ตาม
`COO-DECISION 20260902_0543` (Rule 14.13(d)) และเทสของมันเองสแกนทั้งรีโปด้วย text scan (ไม่ใช่แค่
import check) ว่าไม่มีไฟล์ไหนใน `src/pirateforce_foundation` เอ่ยชื่อมันเลย — เจอเองตอนรัน
`tests/test_world_avatar_attr.py` รอบแรก (แดง 2 ใบเพราะ docstring แรกของผมพิมพ์ชื่อมันไว้) แก้โดย
เขียนคำอธิบายใหม่แบบไม่เอ่ยชื่อ + เปลี่ยน signature รับเลขสามตัวที่ decode มาแล้วแทน blob ดิบ — ต่อสาย
จริงเป็นของ chief/LANE-A ตัดสิน (ขอในจดหมาย)

### 3.3 `pf-adversary` (ก่อน commit)

พบสองข้อ ทั้งคู่แก้แล้ว:
1. เทสเดิมทุกตัว derive ค่าคาดหวังจาก `CLASS_PRESETS` เอง ⇒ ตรวจแค่ตรรกะของ matcher ไม่ตรวจว่า
   transcribe ถูก — adversary สร้าง mutant สลับแถว/สลับคอลัมน์แล้วเทสยังเขียวหมด → เพิ่มเทสที่ pin
   ตารางซ้ำอีกชุดพิมพ์เองแยกในไฟล์เทส (ไม่ได้อ่านจาก `CLASS_PRESETS`) ให้ต้องตรงกันเอง
2. ไม่มีเทสตรึงจำนวนแถว/`class_id` ซ้ำ — adversary เติมแถวที่ 6 ซ้ำ `class_id=1` แล้วเทสยังเขียว →
   เพิ่ม `test_exactly_five_rows_no_duplicate_class_id`

### 3.4 สิ่งที่ตั้งใจไม่ทำรอบนี้ — backfill ตัวละครเก่า

`COO-ORDER 0329` ชิ้น 1 ขอ backfill ด้วย แต่สมมติฐาน "หน้าจอสร้างตัวส่ง preset ตรง ๆ" วัดยืนยันแค่
คลาสเดียว (Gladiator, `JOB-001`/`test01`) เขียนทับแถวเก่าจริงของเจ้าของบนสมมติฐานที่ยังไม่ครบทุกคลาส
คือย้อนไม่ได้ถ้าผิด (มี backup ก็ยังเป็นการเขียนค่าที่อาจผิดทับ `NULL` ที่อย่างน้อยรู้ว่า "ไม่รู้") — ส่ง
ให้ COO ตัดสินในจดหมายรอบนี้ ไม่ตัดสินเอง จึงไม่มีไฟล์ migration รอบนี้ (`class_id` เป็นคอลัมน์เดิมจาก
`006`/`009` อยู่แล้ว ไม่ต้อง migration ใหม่สำหรับ schema)

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: `pytest tests/test_persistence_class_id.py` (13 ผ่าน) +
  `pytest tests/test_world_avatar_attr.py tests/test_persistence_typed_attr_columns.py
  tests/test_persistence_attr_compose.py` (ไม่แตะไฟล์เหล่านี้ แต่ทดสอบผลกระทบของ isolation guard —
  เขียวหมด 175 passed/688 subtests รวมสี่ไฟล์)
- ชุดเต็ม (`pytest tests -q`) รันครั้งเดียวหลัง `git fetch origin main` (ไม่มี commit ใหม่จาก main
  ระหว่างรอบ) และหลังแก้ตาม `pf-adversary` เรียบร้อย เป็น commit สุดท้ายจริง: **9263 passed, 323
  skipped, 0 failed (388.55s)**
- `pirate-force-server#699 [LANE-DB] round wgu3vp: class_id resolver (gear-preset matcher, piece 1/5)`
  — เปิดแล้ว มี `PF-AUTOMERGE: v4` ในตัว รอ gate Windows (ยังไม่ merge — ไฟล์รอบนี้ไม่เขียนว่าขึ้น
  main แล้ว)
- `pf_bridge#1056` (claim PR ของรอบนี้) — เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้ เพราะ PR
  ฝั่งเซิร์ฟเวอร์ของรอบ (มีใบเดียว) เปิดแล้วพร้อม marker ครบตามเงื่อนไขปลดล็อก

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** — ยังไม่ต่อสายเข้า create/login (ของ chief) จึงยังไม่มีอะไรเปลี่ยนบนจอผู้เล่น ไม่มีอะไร
เข้าคิว GT รอบนี้ ตัวโมดูลเองไม่ส่งเฟรมอะไร

### 5.2 wire-DB

- `src/pirateforce_foundation/persistence_class_id.py` (ใหม่) — `resolve_class_id(...)`, `CLASS_PRESETS`
  5 แถว
- `tests/test_persistence_class_id.py` (ใหม่) — 13 tests, 10 subtests, เขียวทั้งหมดบนต้นไม้นี้
- `characters.class_id` (คอลัมน์เดิมจาก `006`/`009`) — ยังไม่มีแถวไหนถูกเขียนรอบนี้ (ไม่มี
  wiring/backfill) NULL เหมือนเดิมทุกแถว
- `persistence_typed_attrs.TYPED_COLUMNS['class_id']` (ของเดิม ไม่แตะ) — ยืนยันแล้วว่า
  `store.write_typed_attributes(cid, {"class_id": n})` ใช้เขียนได้ทันทีเมื่อมีจุดเสียบ ไม่ต้องเปิด
  method ใหม่ใน `store.py`
- `pirate-force-server#699`, `pf_bridge#1056` — ลิงก์ PR ของรอบ

## 6. nonclaims

1. **ไม่อ้างว่า tag `0x19` คือคลาส** — ไม่แตะเลยตามคำสั่ง `1943`
2. **ไม่อ้างว่า cross-check นี้พิสูจน์แล้วเกินหนึ่งคลาส** — ดู 3.4
3. **ไม่อ้างว่าชิ้น 1 เสร็จ** — โค้ด/เทสของ "matcher" เสร็จ แต่การต่อสายจริง (decode blob จริง → เขียน
   `class_id` ตอนสร้าง → อ่านตอนล็อกอิน) อยู่นอกเขตเขียนของ DB ทั้งคู่ รอ chief
4. **ไม่ได้แตะ `player_wire.py`/`legacy_bridge.py`/`store.py`'s existing methods เอง**
5. **ไม่ได้เปิด image/canonical DB/capture corpus** — ทุกอาร์ติแฟกต์ข้างบน commit แล้วในสองรีโป
6. **`1101` (HP/เลเวลถาวร) ยังล็อกอยู่เหมือนเดิม** — รอบนี้ไม่ได้วัดซ้ำ Door B (นอกคิวรอบนี้ตาม
   ลำดับใหม่ `0329` ข้อ 1: PLAYER/CHARACTER มาก่อน)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า chief ตอบจดหมาย CORE-REQUEST รอบนี้หรือยัง (สองจุดเสียบ + คำตัดสินเรื่อง backfill จาก COO)
   ถ้าตอบแล้วและต่อสายจริง ⇒ วัด `GT-215`-style บนจอว่าคลาสไม่ถูกทิ้งจริง แล้วเริ่มชิ้น 2/5 (ค่าเกิดจาก
   `CHARCREATE_CLASS`/`STANDARD_STATUS`)
3. ถ้ายังไม่ตอบ ⇒ เริ่มชิ้น 2/5 หรือชิ้น 5/5 (สกิลเกิด) ที่ไม่ต้องรอจุดเสียบเดียวกัน (ตามกฎ "ชิ้นที่ไม่
   ต้องรอใครมีอย่างน้อยสองชิ้นเสมอ") — ต้องตรวจก่อนว่าชิ้นไหนจริง ๆ ไม่ต้องรอ ก่อนเริ่ม
4. ตรวจ `pirate-force-server#699` ว่า gate ผ่านหรือยัง (ไม่บล็อกงานต่อ แค่รายงานสถานะ)

# DB round (`d3h7zk`) -- 2026-09-05T05:33+07:00 -> 2026-09-05T06:12+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับขั้น M** -- ไม่ใช่ milestone gate เป็นการปิดหนี้ที่ `pirate-force-server#790` (round `1hwg61`)
เปิดไว้เอง (`pf-adversary` ยืนยันช่องโหว่ฝั่งเขียนแล้วแต่ scope ออกจาก PR นั้น) ไม่มีข้อ NOW บรรทัดไหน
พูดถึงเรื่องนี้ตรง ๆ ให้ขยับ อ่าน NOW.md สดล่าสุด (`05:48` โดย COO) แล้ว -- ไม่มีรายการที่เกี่ยวกับ
LANE-DB โดยตรงในรอบนี้ (M4·B/A เป็นของสายอื่น)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

## 1. ล็อกรอบ

- 05:33+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  ว่างเปล่าทั้งคู่ -- ไม่มีรอบทำงานค้าง ไม่ต้อง takeover
- ตัดกิ่งจาก `origin/main` สด (`pf_bridge` @ `ee8e5106`→rebase เป็น `663569ca` ก่อนเริ่ม) commit
  `rounds/DB_20260905_0533_d3h7zk_claim.md` push แล้ว เปิด `pf_bridge#1263 [LANE-DB] round d3h7zk: claim`
  (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1263` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -q "ADDRESSEE: LANE-DB"` (unanchored) บน `origin/main` สดของ `pf_bridge` ต้นรอบและซ้ำอีกครั้งก่อนปิด
รอบ (หลัง rebase กับ `origin/main` ที่เดินหน้าไปอีก 21 ไฟล์ระหว่างรอ gate) -- **ว่างเปล่าทั้งสองครั้ง**
ไม่มีใบค้าง อ่านสามใบก่อตั้งสาย (`20260901_1059`/`1100`/`1101`/`1112`) ครบตามกติกา "รอบแรกของเซสชัน"
(เซสชันนี้ไม่มีความจำข้ามรอบ)

## 3. ทำอะไร

### 3.1 ตรวจ `1101` (M4 หลัก) -- ยังล็อกเหมือนเดิม ไม่มีสัญญาณใหม่

`grep -c "store=" src/pirateforce_foundation/runtime.py` บน `origin/main` สด = **0** (เหมือนทุกรอบ
ก่อนหน้า) -- COO อนุมัติ hold นี้แล้ว (`0103`) ไม่มีสัญญาณใหม่จาก LANE-B/Door B รอบนี้ -- ข้ามไปงานสำรอง

### 3.2 ตรวจ `pirate-force-server#790` (round `1hwg61`, จากรอบก่อน) -- merge แล้ว

`#790` merge สำเร็จ (`merged: true`) -- ไม่มีอะไรต้องแก้ ยืนยัน gate เขียวแล้วจากรอบก่อน

### 3.3 งานหลักของรอบ: ปิดหนี้ที่ `#790` เปิดไว้ -- guard ฝั่งเขียน `write_typed_attributes`/
`write_typed_attribute_if_unset`

`#790` (round `1hwg61`) แก้ช่องโหว่ pre-006 schema-drift เฉพาะฝั่งอ่าน และ `pf-adversary` รอบนั้นยืนยัน
ด้วยการรัน `ALTER TABLE ... DROP COLUMN` ตรง ๆ ว่าฝั่งเขียน (`write_typed_attributes`/
`write_typed_attribute_if_unset`) มีช่องโหว่เดียวกันจริง แต่ scope ออกจาก PR นั้นเพราะวันนี้ไปไม่ถึง
จริง (`ReadOnlyFoundationSession` ไม่มีทางเขียน) -- นี่คืองานสำรองข้อ 1 ที่ไฟล์รอบก่อนทิ้งไว้ เขต DB
ของสายเองล้วน ๆ ไม่ต้องรอใคร

**ตัดสินใจก่อนเขียนโค้ด** (คำถามที่ไฟล์รอบก่อนทิ้งไว้: พังแบบมีป้ายหรือปฏิเสธเงียบ ๆ): พบ precedent ที่
มีอยู่แล้วในไฟล์เดียวกัน -- ทุกเมธอดที่เขียนคอลัมน์ vitals (`create_character`, `apply_hp_damage`, ฯลฯ)
เรียก `persistence_vitals.verify_schema(db)` ทันทีหลัง `BEGIN IMMEDIATE` เพื่อพัง `SchemaDriftError`
แบบมีป้ายแทน `OperationalError` ดิบ ๆ อยู่แล้ว -- `required_columns()` ของมัน derive จาก
`typed_attrs.TYPED_COLUMNS` ทั้งหมด ตรงกับคอลัมน์ที่สองเมธอดนี้เขียนพอดี ⇒ **เลือกพังแบบมีป้าย** โดยใช้
guard เดียวกันที่มีอยู่แล้ว ไม่ประดิษฐ์กลไกใหม่:

- `src/pirateforce_foundation/store.py`: เติม `vitals.verify_schema(db)` หลัง `BEGIN IMMEDIATE` ใน
  `write_typed_attributes` และ `write_typed_attribute_if_unset` ทั้งสองเมธอด (ตำแหน่งเดียวกับทุก
  sibling method) แก้ docstring ทั้งสองอธิบายเหตุผลตรงตามที่ `#790`'s adversary วัดไว้จริง
- `tests/test_persistence_typed_attr_columns.py`: คลาสใหม่ `WriteTypedAttributesPreMigration006Tests`
  -- drop คอลัมน์ (ไม่ใช่คอลัมน์เดียวกับที่จะเขียน เพื่อพิสูจน์ guard เช็คทั้ง schema ไม่ใช่แค่คอลัมน์
  เป้าหมาย) แล้วพิสูจน์ทั้งสองเมธอด raise `SchemaDriftError` (รวมกรณีเขียนตรงคอลัมน์ที่หายไปเอง) ไม่มี
  อะไรถูกเขียนเมื่อ guard ทำงาน (ใช้คอลัมน์ `mp_current` ที่ไม่มี birth default -- คนละกลุ่มกับ
  `level`/`hp_current`/`hp_max`/`speed_walk` ที่ migration 009 seed ให้ตอนสร้าง) และ DB ที่ migrate
  แล้วยังเขียนได้ปกติ

**mutation test เอง**: ถอด guard ชั่วคราว (stash `store.py`) รันคลาสเทสใหม่ -- 5/6 แดงด้วย
`sqlite3.OperationalError: no such column: class_id` ตัวเดียวกับที่รายงานจริง (ใบที่ 6 = DB ที่
migrate แล้ว ไม่แตะ crash path เลย ถูกต้องแล้วที่ยังผ่าน) ใส่ guard กลับเขียวทั้งคลาส

**`pf-adversary` เรียกครั้งเดียว**: **GO** ไม่มี defect พังจริง มีสามข้อบันทึกไว้ (ไม่บล็อกรอบนี้):
1. ไม่มี TOCTOU -- adversary จำลอง sleep คั่นระหว่าง `verify_schema` กับ `UPDATE` แล้วแข่ง
   `ALTER TABLE` จากคอนเนกชันที่สอง โดนปฏิเสธด้วย `database is locked` จาก reserved-lock ของ SQLite เอง
2. `write_typed_attribute_if_unset` เขียนคอลัมน์เดียวแต่ guard เช็คทั้ง 21 คอลัมน์ -- over-refusal จริง
   ในเคสที่คอลัมน์อื่น drift แต่คอลัมน์เป้าหมายยังอยู่ครบ แต่ตรงกับพฤติกรรมเดิมของ `create_character`
   เป๊ะ (เขียนแค่ 3 คอลัมน์ แต่เช็คทั้ง schema เหมือนกัน) ⇒ ไม่ใช่ asymmetry ใหม่ที่รอบนี้สร้างขึ้น
   บันทึกเป็น `[PROPOSED]` งานปรับปรุงในอนาคต ไม่ใช่ตัวบล็อก
3. คำถามเปิดสำหรับอนาคต: ถ้า migration ใหม่เพิ่มคอลัมน์ที่ 22 ควรปฏิเสธ DB ที่ยังไม่ migrate (พฤติกรรม
   ปัจจุบัน ตาม `create_character`) หรือเสิร์ฟคอลัมน์ที่มีอยู่ (แบบฝั่งอ่าน)? ไม่ตัดสินรอบนี้ คงพฤติกรรม
   เดิมตาม precedent

ตอบกลับ chief/COO ด้วยใบ
`notes_to_chief/20260905_0612_LANE-DB-STATUS-write-side-schema-drift-guard-798-open.md`

## 4. ชุดเทสของรอบ

- ระหว่างทำงาน: `tests/test_persistence_typed_attr_columns.py` (94 passed, 340 subtests) เขียวก่อน/
  หลัง merge `origin/main` เข้ากิ่ง
- ชุดเต็ม (ครั้งเดียวของรอบ, บน commit สุดท้าย -- merge `origin/main` `3e29682f` เข้ากิ่งแล้วก่อนรัน):
  **10595 passed, 323 skipped, 19737 subtests passed, 0 failed** ใน 390.42s -- ไม่มีเทสแดงเก่าค้าง

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ยังศูนย์สำหรับสายนี้โดยตรง** เหมือนทุกรอบก่อนหน้าของงานนี้ -- นี่คือชั้น store-side ล้วน ๆ ไม่มี call
site ไหนเรียกสองเมธอดนี้กับคอลัมน์ที่หายไปในการทำงานจริงวันนี้ (adversary ยืนยันแล้วว่า unreachable
ในเส้นทางที่มีอยู่จริง) ไม่มีอะไรให้ผู้เล่นเห็นบนจอจากรอบนี้

### 5.2 wire-DB
`pirate-force-server#798` เปิดแล้ว (`claude/brave-goodall-d3h7zk` @ merge `3e29682f`) **มี
`PF-AUTOMERGE: v4`** (ไม่มีเหตุขัดแย้งกับใคร แก้ในเขตเขียนของสายเองล้วน ๆ) 🔴 **GATE_UNVERIFIED `#798`**
-- push แล้ว รอผล job `gate` เกิน 10 นาที (เริ่ม 23:00:37Z/23:01:01Z ตรวจซ้ำที่ 23:09:15Z และ 23:12Z
ยังเป็น `in_progress` ทั้งสอง run) ยังไม่ตัดสิน ณ ตอนเขียนไฟล์รอบนี้ -- รอบถัดไปเปิดด้วยการตรวจ PR นี้
ก่อนอย่างอื่นตาม `PANYA-DECISION 1158` (สองรัน `gate` ปรากฏบน PR เดียวกัน น่าจะเป็น re-run ของ workflow
เดียวกัน ไม่ใช่ของสองรอบชนกัน -- ไม่มี PR `[LANE-DB]` อื่นเปิดคู่กันตอนตรวจล็อกรอบต้นรอบ)

## 6. nonclaims

1. **ไม่อ้างว่า `#798` merge แล้ว** -- เปิดอยู่ รอ gate (`GATE_UNVERIFIED` ข้างบน)
2. **ไม่อ้างว่าช่องโหว่นี้เคยเกิดจริงในโปรดักชัน** -- ยืนยันแล้วว่า unreachable วันนี้ (เส้นทางบูตเดียวที่
   ข้าม migration ติดตั้ง read-only session ไม่มีทางเขียนเลย และ caller ฝั่งเขียนที่ไม่มีเงื่อนไขบนเส้น
   ทางนั้นวนแค่ id ที่ว่างอยู่แล้วบน DB แบบนั้น) นี่คือ guard ป้องกันสำหรับ caller อื่นในอนาคต
3. **ไม่แก้ over-refusal ของ `write_typed_attribute_if_unset`** (เช็คทั้ง schema ทั้งที่เขียนคอลัมน์
   เดียว) -- ตรงกับพฤติกรรมเดิมของ `create_character` เป๊ะ ไม่ใช่ asymmetry ใหม่ ยกเป็น `[PROPOSED]`
   งานปรับปรุงในอนาคตตามที่ adversary บันทึก ไม่ขยายรอบนี้
4. **ไม่แตะ `app.py`, `runtime.py`, `current/pf_login_game_server_v141.py`, `lifecycle.py`, migration
   ใด ๆ** ตามข้อห้ามเดิม
5. **ไม่ทำงานคิว M4/`1101` ตามลำดับปกติของสาย** -- รอบนี้ไปกับการปิดหนี้จาก `#790` เพราะอยู่ในเขตเขียน
   ของสายเองล้วน ๆ และเป็นหนี้ที่ adversary รอบก่อนยืนยันไว้แล้วว่ามีจริง ไม่ใช่ "หาเรื่องทำนอกเขต"

## งานสำรอง (ทำเมื่องานหลักติด)

1. **วัด `1101` เป็นรายงานหนึ่งหน้า**: ไฟล์ `runtime.py` (อ่านอย่างเดียว ไม่แก้) · หลักฐานผ่าน =
   `grep -c "store=" runtime.py` ยังคง 0 หรือเปลี่ยน -- ตาม `1450` ข้อ 6 ยังค้าง (ทำซ้ำทุกรอบที่ว่าง)
2. **`[PROPOSED]` narrow schema check สำหรับ `write_typed_attribute_if_unset`**: เช็คเฉพาะคอลัมน์ที่
   กำลังจะเขียนแทนทั้ง 21 คอลัมน์ -- ต้องชั่งน้ำหนักกับความเรียบง่ายของการใช้ guard เดียวกันทั้งไฟล์ก่อน
   เขียนโค้ด (adversary ตั้งคำถามไว้ ไม่ใช่ข้อบกพร่อง)
3. **ตรวจใบ `0258`/`0436` (รอบก่อน ๆ) บน `main`**: ไฟล์ `notes_to_chief/` (อ่านอย่างเดียว) · ยังไม่มี
   คำตอบจาก chief/COO ณ ตอนนี้ -- ตรวจซ้ำรอบหน้า

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. **ตรวจ `pirate-force-server#798` ก่อนอย่างอื่น** (`GATE_UNVERIFIED` ข้างบน) -- ถ้าแดง แก้ในรอบนั้น
   ทันที ถ้าเขียว/merge แล้ว ไม่ต้องทำอะไรเพิ่ม
3. ตรวจว่า chief/COO ตอบใบ `0612` (รอบนี้) หรือใบ `0258`/`0436` (รอบก่อน ๆ) หรือยัง
4. ถ้ายังไม่มีอะไรใหม่ -- หยิบงานสำรองข้อ 1 (รายงาน `1101`) หรือข้อ 2 (`[PROPOSED]` narrow guard ถ้า
   ตัดสินใจว่าคุ้มค่า) เป็นงานหลักรอบถัดไป
5. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ

# R312 · `o5q4pw` · LANE-E (chief)

เวลา: 2026-09-03T00:57+07:00 ถึง (ดูท้ายไฟล์)
PR: `pf_bridge#911` (ประสาน) · `pirate-force-server#<เลขใบกู้>` (ใบกู้ main แดง)

🔴 **NOW.md รอบนี้: ขยับข้อไหน**
รอบนี้ **ไม่ได้ขยับ P-1 / P-2 / P-3 โดยตรง** และนั่นถูกต้องตามคำสั่ง
`COO-DECISION 20260903_0052` ข้อ 1 เขียนไว้ตรง ๆ ว่า **"งานที่หนึ่งของ R312 คือกู้ `#610` ขึ้น main
เหนือ P-1 ตัวเดิน multi-vital และเหนือทุกคิว"** ⇒ รอบนี้ทำงานนั้นอย่างเดียวเป็นหลัก
ผลทางอ้อมต่อ NOW: ตราบใดที่ `main` แดง PR ของ **ทุกสาย** ถูก reaper ปิดทิ้งโดยไม่เกี่ยวกับเนื้องาน
⇒ P-1 (สาย E + สาย B), P-2 (สาย A), P-3 (สาย GM) ขยับไม่ได้เลยจนกว่าใบกู้จะขึ้น
🔴 การ์ดกันเข้าใจผิด: **ยังไม่ประกาศว่าจ่ายหนี้แล้ว** ใบกู้อยู่บน main ก็ต่อเมื่อรอบถัดไปวัดด้วย
`git merge-base --is-ancestor` แล้ว exit 0 (`COO 1745` ข้อ 2)

---

## 1. ชะตาของรอบก่อน วัดก่อนอย่างอื่น (การ์ดหัวข้อ 2 ข้อ 7)

| รีโป | PR ของ R311 | ผล |
| --- | --- | --- |
| `pf_bridge` | `#907` | **merged** 17:18:57Z ⇒ ฝั่งประสานงานปลอดภัย |
| `pirate-force-server` | `#610` | 🔴 **closed ไม่ merge** 17:32:51Z โดย `merge-claude-pr.yml` (`job gate = failure`) |

`#610` คือ **ใบกู้ `main` แดง** ⇒ มันตาย ⇒ `main` แดงต่อ ⇒ ทุกสายถูกกิน
เช็คเอาต์ `origin/main` (`30e150a1`) รันเองในรอบนี้ ยืนยันว่า**ยังแดงจริง**:

```
tests/test_gm_login_scene_override_position_resync.py
  ::GmLoginSceneOverridePositionResyncTests
  ::test_a_login_with_no_override_changes_no_field_of_selected
AssertionError: ... movement_speed=400.0) != ... movement_speed=None)
1 failed, 8 passed
```

กู้ตามที่ข้อความ reaper บอกเอง: `git fetch origin claude/intelligent-lamport-eww6tv`
แล้ว `git cherry-pick 3a9b5699` ลงสาขาใหม่ที่ตั้งต้นจาก `main` ปัจจุบัน (สะอาด ไม่มี conflict)

---

## 2. 🔴 ชื่อเทสที่ทำให้ `pytest_subset` แดงบนเกต (`COO 0052` ข้อ 2 — ข้อบังคับของรอบนี้)

**`tests/test_login_speed.py::TheRealLoginPathTests::test_a_row_with_no_value_sends_the_constant`**

run `33660327427` · job `gate` (`100349008675`) · หัว `696e2f8f`
`1 failed, 7148 passed, 74 skipped, 14162 subtests passed in 746.56s`

```
______ TheRealLoginPathTests.test_a_row_with_no_value_sends_the_constant ______
E  PermissionError: [WinError 32] The process cannot access the file because it is
   being used by another process:
   'C:\Users\RUNNER~1\AppData\Local\Temp\tmp200r8v3u\pf.sqlite3'
C:\...\Lib\shutil.py:701: PermissionError
---------------------------- Captured stderr call -----------------------------
LOGIN_SPEED row_has_no_value value=400.0
```

**เป็นชนิดที่หนึ่งของ `COO 0052` ข้อ 2: แดงเฉพาะ Windows** ⇒ กติกาบังคับให้เขียนลง `AGENTS.md`
ในรอบเดียวกัน ⇒ ลงแล้วในใบ `pf_bridge#911` นี้ (`AGENTS.md` §7 บรรทัดใหม่บรรทัดแรก)

### สองอย่างที่อ่านได้จากก้อนนี้ และอย่างที่สองสำคัญกว่า

1. **บอดี้ของเทสผ่าน** — `LOGIN_SPEED row_has_no_value value=400.0` คือสิ่งที่ใบตั้งใจให้เกิด
   สาขา `ROW_HAS_NO_VALUE` ถูกเดินจริง ⇒ **แพตช์ของ `#610` แก้ `main` ได้จริง**
   และตัวที่ `#605` ทำแตกไว้หายไปแล้ว (`8 passed` ในไฟล์นั้น) เหลือ handle เดียว
2. **ที่ล้มคือ teardown** — `shutil.py:701` / `tempfile.py:931` คือทางเดินของ
   `TemporaryDirectory.cleanup` ไม่ใช่ assertion สักตัว
   ⇒ กับดักนี้ **อ่านยากเป็นพิเศษ**: log พิมพ์ผลที่ถูกต้องออกมาก่อนตาย

### กลไก และทำไมคลาวด์มองไม่เห็น

`with sqlite3.connect(path) as db:` — `sqlite3.Connection.__exit__` **commit เท่านั้น ไม่ close**
handle จึงยังถือ `pf.sqlite3` (และ `-wal` `-shm`) อยู่ตอน cleanup
Linux `unlink` ไฟล์ที่ยังเปิดอยู่ได้เงียบ ๆ · Windows ปฏิเสธ ⇒ `WinError 32`

**[วัดแล้ว รอบนี้]** สองมิวแทนต์บนสาขานี้:

| มิวแทนต์ | ผล |
| --- | --- |
| M1 · ใส่ทรง `with` กลับ **พร้อม**การ์ดรันไทม์ (`/proc/self/fd`) | **RED** และข้อความชี้ตรงจุด พร้อมชื่อ fd ทั้งสาม (`pf.sqlite3`, `-shm`, `-wal`) |
| M2 · ใส่ทรง `with` กลับ **โดยไม่มี**การ์ด | 🔴 **`32 passed`** — ไม่มีสัญญาณใด ๆ บนคลาวด์เลย |

M2 คือสภาพที่ `#610` ถูกเขียนและถูกวัด และคือเหตุผลที่ **"ชุดเต็มเขียวบนคลาวด์" ไม่เคยแปลว่าเกตจะเขียว**

### ยืนยันสองแหล่ง (G1)

LANE-B ใบ `20260903_0039_LANE-B-TO-LANE-E-what-killed-610-on-windows.md` วินิจฉัยเรื่องเดียวกัน
โดยอิสระ ก่อนรอบนี้เริ่ม และวัดกลไก `__exit__` บนคลาวด์เองด้วย ⇒ สองแหล่ง ตรงกันทุกตัวอักษร
🔴 เครดิตเป็นของ LANE-B: มันรู้คำตอบแล้วและ**เลือกไม่แก้เอง** เพราะไฟล์อยู่นอกเขตเขียนของมัน
และใบถูกจองไว้ (อายุ 22 นาที < 90 นาที) — กติกาการจองทำงานถูกต้องพอดีในกรณีที่มันแพงที่สุด

---

## 3. ใบกู้: เล็กที่สุดตามที่ถูกสั่ง

`COO 0052` ข้อ 1: *"ใบเล็กที่สุดเท่าที่เป็นไปได้ · ห้ามพ่วงงานอื่น ห้ามเพิ่มไฟล์ `tests/test_*.py` ใหม่"*

ใบกู้ = คอมมิตของ `#610` ที่ cherry-pick มา **บวกแพตช์เดียว**:

```python
        db = sqlite3.connect(self.path)
        try:
            db.execute(
                "UPDATE characters SET speed_walk = NULL WHERE id = ?",
                (character.id,))
            db.commit()
        finally:
            db.close()
```

ไฟล์ทั้งใบ: 4 ไฟล์ (`login_speed.py` · `vital_walk.py` · เทสสองไฟล์) — เท่าเดิมกับ `#610` เป๊ะ
ไม่มีไฟล์ใหม่ ไม่มีเรื่องอื่นพ่วง

🔴 **สิ่งที่ผมถอดออกจากใบกู้โดยตั้งใจ และเหตุผล**
ร่างแรกของรอบนี้พ่วงการ์ดรันไทม์มาด้วย: ไฟล์ช่วยใหม่ `tests/pf_handle_guard.py`
(ย้าย `NoHandleOutlivesItsTempDirMixin` ออกมาจาก `tests/test_persistence_typed_attr_columns.py`)
แล้วให้ `TheRealLoginPathTests` มิกซ์อิน — นั่นคือของที่ทำให้ M1 ข้างบนแดงได้
มันเป็นการ์ดที่ใช้ได้จริงและวัดแล้ว **แต่ `COO 0052` ข้อ 1 ห้ามพ่วง** และเหตุผลของคำสั่งนั้นถูก:
ไฟล์ใหม่ + การนำเข้าข้ามโมดูล คือช่องที่กับดักชนิดเดียวกันจะเข้ามาอีกใบ
⇒ ถอดออก เก็บไว้เป็น **ใบที่สองของรอบ (หรือ R313)** หลังใบกู้ขึ้น main
⇒ ในระหว่างนี้ ที่กันไม่ให้คนถัดไปเขียนทรงรั่วซ้ำคือ **คอมเมนต์ในเทส + บรรทัดใน `AGENTS.md`** เท่านั้น
   ซึ่งอ่อนกว่าการ์ดจริง และรอบนี้บันทึกไว้ตรง ๆ ว่ามันอ่อนกว่า

---

## 4. ต้นเหตุเชิงองค์กร ที่ยังไม่ถูกแก้ในรอบนี้

การ์ดตัวนี้ **ไม่ได้หายไป** ตอน `#610` เขียน — มัน **ถูกจำกัดขอบเขต**:

- `NoHandleOutlivesItsTempDirMixin` อยู่ใน `tests/test_persistence_typed_attr_columns.py`
  = โมดูลของ LANE-DB · สายอื่นไม่มีเหตุจะไปนำเข้า
- หมุดต้นทางคู่กันอ่าน `LANE_TEST_MODULES` ซึ่ง glob แค่ `tests/test_persistence_*.py`
  = **ขอบเขตตามกฎบัตรของเลนที่เขียนมัน**
- สำเนาที่สามของ helper เดียวกันอยู่ใน `tests/test_persistence_canon_gate.py` แล้วด้วย

⇒ `#495` (LANE-DB) ตายด้วยกับดักนี้ · การ์ดถูกสร้างขึ้นและ**ล้อมเฉพาะบ้านตัวเอง** ·
หนึ่งเดือนต่อมา `#610` (LANE-E) เดินลงหลุมเดิมนอกรั้ว
🔴 **บทเรียนที่กว้างกว่าบั๊กนี้: การ์ดที่ขอบเขตหยุดอยู่ที่ glob ของเลนเดียว มองไม่เห็นเลนถัดไป**
งานที่ค้าง (ใบที่สอง): ยกการ์ดขึ้นมาเป็น `tests/pf_handle_guard.py` ที่ทุกเลนนำเข้าได้
+ ขยายหมุดต้นทางให้อ่าน `tests/test_*.py` ทั้งหมด + ยุบสำเนาที่ซ้ำสามชุด

---

## 5. ที่วัดในรอบนี้

- `pytest tests/test_login_speed.py tests/test_gm_login_scene_override_position_resync.py`
  ⇒ **41 passed, 29 subtests** (ตรงกับที่ COO วัดเองบนสาขา `eww6tv`)
- ชุดเต็มบนต้นไม้สุดท้าย ⇒ ดู §7 ท้ายไฟล์ — **เขียว(cloud sanity) เท่านั้น ไม่ใช่เกต**
  รันบนต้นไม้ที่ **มี `origin/main` อยู่แล้ว** (`git merge-base --is-ancestor origin/main HEAD` exit 0)
  ตาม `COO 0053` กฎ ก. ⇒ ไม่ใช่หัวสาขาเพียว
- `tools/verify_hypothesis_ledger.py` ⇒ **PASS entries=50** (ขั้นบังคับก่อน commit หัวข้อ 7)
- ไม่มีอักขระนอก ASCII ในดิฟทั้งใบ (`git diff | grep -P '[^\x00-\x7F]'` ว่าง) · `git diff --check` ว่าง
- pf-adversary ผ่านหนึ่งรอบก่อน commit (หัวข้อ 10) — ผลอยู่ใน §6

---

## 6. pf-adversary

(เติมท้ายรอบ — ดูจดหมาย `FROM_CHIEF_R312`)

---

## 7. อะไรที่ **ไม่ได้** พิสูจน์

- **ไม่มีอะไรเป็นชั้น client-observable เลยทั้งรอบ** (G5) — wire/DB ล้วน · ไม่มี `OBSERVER_CONFIRMED`
- 🔴 **ไม่ได้พิสูจน์ว่าเกต Windows จะเขียว** คลาวด์เป็น Linux + Python 3.11 · เกตเป็น Windows + 3.14.7
  และรอบนี้ทั้งรอบคือหลักฐานว่าคู่นี้ไม่เท่ากัน · เขียวที่เขียนในไฟล์นี้คือ **เขียว(cloud sanity)**
- 🔴 `#605` **ยังไม่สังเกตได้จากจอ**: หลัง `migrations/009` (`speed_walk REAL DEFAULT 400.0`)
  "ล็อกอินอ่านแถว" กับ "ล็อกอินส่งค่าคงที่" ให้ไบต์เท่ากันเป๊ะบนฐานข้อมูลสดทุกใบ รวมของเจ้าของ
  ⇒ ห้ามรอบไหนรายงาน `#605` เป็นผลที่ผู้เล่นเห็น (ย้ำจาก `COO 0054`)
- "ล็อกอินควร persist ค่าที่อ่านมาไหม" **ยังเป็นคำถามเปิด** — `COO 0052` §3 ห้ามตอบมันในใบกู้สีแดง
- `AGENTS.md` โตขึ้นอีกจากบรรทัดใหม่สามบรรทัด (31.3 KB → เกินเพดาน 25 KB ที่ §17 ข้อ 9 จ ตั้งไว้อยู่แล้ว)
  ⇒ งานย่อ `AGENTS.md` ยังค้าง เป็นหนี้ที่ประกาศ ไม่ใช่หนี้ที่ซ่อน

[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-DB (PERSISTENCE) รอบ `dgx8e5` · 2026-09-02T16:40+07:00]
[อ้าง: `COO-DECISION 20260902_1546` (สั่งให้เขียนหมุดนี้ · ปฏิเสธ rebuild/trigger ถาวร) · `COO-DECISION 20260902_0444` ข้อ 1 (plug เป็นของคุณ) · `COO-DECISION 20260902_1546` หัวข้อ "ใครทำอะไรต่อ" (plug ลงใน R306)]

# NOTICE: ใบนี้คือ "อนุญาตเป็นลายลักษณ์อักษร" ให้คุณลบไฟล์เทสของ LANE-DB หนึ่งไฟล์ ตอนที่ plug `0444` ลง

## 0. หนึ่งประโยค

รอบนี้ผมลงหมุดตามที่ COO สั่งใน `1546` ไว้ที่ `tests/test_persistence_birth_hole_pin.py`
**หมุดตัวนี้จะแดงในวันที่คุณลง plug** ซึ่งเป็นเจตนา ไม่ใช่ความพลาด และใบนี้มีไว้ให้คุณ
**ไม่ต้องมาถามใคร**: เห็นมันแดง = `git rm tests/test_persistence_birth_hole_pin.py` ไฟล์เดียว จบ

## 1. ไฟล์อะไร และมันพูดว่าอะไร

- ไฟล์: `pirate-force-server/tests/test_persistence_birth_hole_pin.py` (ไฟล์ใหม่รอบนี้ 2 เทส)
- มันวัดว่า: บน **fresh install** ตัวละครที่ `SQLiteStore.create_character` (`store.py:209-236`)
  สร้างขึ้น ยังถือ `level` / `hp_current` / `hp_max` เป็น NULL — เพราะ `006` เพิ่มคอลัมน์โดยไม่มี
  DEFAULT และ `007` seed เฉพาะแถวที่มีอยู่ตอนมันรัน
- วันที่ plug ของคุณลง เงื่อนไขนั้นเป็นเท็จ เทสจะ `self.fail()` และ **ข้อความ failure ทั้งข้อความ
  คือคำสั่งว่าให้ทำอะไร** (ขึ้นต้นด้วย "THIS IS NOT A DEFECT IN YOUR CHANGE -- IT IS THIS PIN
  RETIRING") ไม่มี traceback ที่ต้องตีความ ไม่มีค่าที่ต้องไปหา

## 2. อนุญาตอะไร ให้ชัดเพราะ charter ห้ามคุณแตะ tests/ ของสายผม

**LANE-DB อนุญาตให้ chief ลบไฟล์ `tests/test_persistence_birth_hole_pin.py` ทั้งไฟล์
ใน PR เดียวกับที่ลง plug `0444` โดยไม่ต้องเขียนใบขอกลับมา** — วัดแล้วว่า:

- ไม่มีไฟล์ไหนใน `tests/` หรือ `src/` `import` โมดูลนี้ หรืออ้างชื่อใด ๆ ในนั้น
- สภาพ "plug ลงแล้ว" ยังถูกให้เกรดต่อที่ `SeedsACohortNotADatabaseTests`
  (`tests/test_persistence_vitals_seed_007.py`) ซึ่ง **รับได้ทั้งสองสภาพ** และตรวจค่าทั้งสองทาง
  ⇒ ลบไฟล์นี้ไม่ทำให้ plug ของคุณเหลือ coverage น้อยลงแม้แต่ข้อเดียว

## 3. ทำไมไม่ทำให้มัน "ไม่แดง" ตั้งแต่แรก — ผมลองแล้ว และมันแย่กว่า

ร่างแรกใช้ `skipTest` แทน `fail` ด้วยเหตุผลว่า skip เห็นได้ด้วย `pytest -rs` และไม่เคยแดง
**ผิด และวัดแล้วว่าผิด**: `.github/workflows/gate-windows.yml:454` เรียก
`tools/pf_pytest_precondition_census.py` ซึ่ง exit 1 เมื่อเจอ "skip ที่ไม่มี `[precondition:<key>]`
และไม่อยู่ใน `design_skips`" (`tools/pf_pytest_precondition_census.py:17-19`)
และไฟล์ที่มันอ่านคือ `docs/PYTEST_SKIP_PINS.json` = **เขตของคุณ** ผมประกาศล่วงหน้าเองไม่ได้
และต่อให้ประกาศได้ เครื่องมือตัวเดียวกันก็ exit 1 กับ "pinned skip ที่ไม่เกิด" อยู่ดี
⇒ skip จะทำให้เกตแดงให้คุณ **ด้วย exit code ที่ไม่บอกอะไรเลย** แทนที่จะเป็นเทสหนึ่งตัวที่พก
คำสั่งมาในตัว ผมจึงเลือกแดงแบบที่ถูกกว่า

## 4. ผมไม่อ้างอะไร

- ไม่อ้างว่าหมุดนี้จับ plug ที่ผิดได้ทุกรูปทรง — มันจับได้เท่าที่ `pf_birth_state.
  measure_birth_typed_state` ปฏิเสธ (seed ไม่ครบ / `level 0` / มี `speed_walk` ติดมา วัดแล้วแดงทั้งสาม)
  รูปทรงที่ทำร้าย **แถวอื่น** ยังเป็นของ `SeedsACohortNotADatabaseTests` ไม่ใช่ของไฟล์นี้
- ไม่อ้างว่า plug ช้า ผมรู้ว่า COO เป็นคนจัดคิวให้ `ground_after` มาก่อน (`1546` ข้อ 4)
- ไม่ขอให้คุณทำอะไรในรอบนี้ ใบนี้ไม่มีคำถาม ไม่ต้องตอบ เก็บไว้อ่านตอนเห็นมันแดงพอ

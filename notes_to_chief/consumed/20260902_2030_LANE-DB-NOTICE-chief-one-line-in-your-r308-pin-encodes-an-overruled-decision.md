[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-DB (PERSISTENCE) รอบ `1e9gie` · 2026-09-02T20:30+07:00]
[อ้าง: commit `b9e11059` R308 (`tests/test_birth_vitals_plug_is_pinned.py`) · `COO-DECISION 20260902_1607` (อนุมัติ `migrations/009` ให้ `speed_walk` มี DEFAULT) · `COO-DECISION 20260902_0742` (ปลดแบน 400.0 หลัง RE-194) · ใบผมถึง COO `20260902_2028` (ขอคำตัดสินว่าใครแก้)]

# แจ้งล่วงหน้า ไม่ใช่คำขอให้รีบ: หมุดของคุณหนึ่งบรรทัดอ้างคำตัดสินที่ถูกกลับไปแล้ว

## 1. บรรทัดไหน

`tests/test_birth_vitals_plug_is_pinned.py:236`
`test_a_birth_writes_no_typed_column_beyond_the_three` — `assertIsNone(value)` บน `speed_walk`
docstring อ้าง `COO-DECISION 20260901_1447` ข้อ 2 และ `COO-DECISION 20260902_1043`

**ทั้งสองใบถูกแทนที่แล้ว ก่อนคอมมิตของคุณ:**
- `COO 20260902_0742` ปลดแบนเลข 400.0 หลัง `RE-194` (และอนุมัติ `migrations/008` ที่ seed ค่านี้)
- `COO 20260902_1607` (16:07 · **เจ้าของเคาะสดเอง** กลับคำ COO สองใบ) สั่งสาย DB ทำ `migrations/009`
  ให้ `level=1 · hp_current=100 · hp_max=100 · speed_walk=400.0` เป็น **DEFAULT ของคอลัมน์**

⇒ ตัวละครเกิดใหม่บนฐานที่ apply `009` แล้ว **มี `speed_walk = 400.0`** เทสข้อนี้จึงแดง

## 2. ผมไม่แก้ไฟล์ของคุณ

ไฟล์ของคุณอยู่นอกเขตเขียนของผม (ชาร์เตอร์ `COO 20260901_1100`) ผม **ไม่แตะแม้ตัวอักษรเดียว**
และเขียนใบถึง COO ขอคำตัดสินว่าใครควรแก้ (`20260902_2028` ข้อ 3: ก. คุณแก้ · ข. อนุญาตให้ผมแก้บรรทัดเดียว)
ถ้า COO ตอบข้อ ก. นี่คือดิฟฟ์ที่ผมเสนอ ใช้ได้ทันที ไม่ต้องคิดใหม่:

```python
    def test_a_birth_writes_no_typed_column_beyond_the_three(self):
        """The three vitals are this INSERT's business, and `speed_walk` is
        the SCHEMA's: `migrations/009_character_birth_defaults.sql` gives that
        column a DEFAULT of 400.0 on COO-DECISION 20260902_1607 (the owner
        overruling 20260901_1447 point 2 and 20260902_1043 in session).  So
        the pin is now "the INSERT writes exactly three columns", which is
        what this file is about, rather than "the row holds exactly three".
        """
        store = self._store()
        character = self._born(store, "four")
        with _raw(self.path) as db:
            columns = [row[1] for row in
                       db.execute("PRAGMA table_info(characters)")]
            self.assertIn("speed_walk", columns,
                          "migration 008 is missing; this test grades nothing")
            value = db.execute(
                "SELECT speed_walk FROM characters WHERE id=?",
                (character.id,)).fetchone()[0]
        default = db_default_for("speed_walk", self.path)   # PRAGMA table_info
        self.assertEqual(
            value, default,
            "a newborn's speed_walk is neither NULL nor the schema's own "
            "DEFAULT, so something WROTE it -- which is the fourth birth "
            "value nobody adjudicated")
```

รูปทรงที่ผมคิดว่าดีที่สุดคือ **เทียบกับ DEFAULT ที่อ่านจาก `PRAGMA table_info` ของฐานเดียวกัน**
ไม่ใช่ `assertEqual(value, 400.0)` — เพราะแบบหลังจะกลายเป็นแหล่งเลขที่สอง ซึ่งเป็นสิ่งที่ใบ `0443`
ข้อ 1 ของคุณเองห้ามไว้ · ถ้าอยากให้ง่ายกว่านั้น `self.assertIsNotNone(value)` ก็พอสำหรับหมุดนี้

## 3. สิ่งที่หมุดของคุณยังวัดได้เต็ม ๆ และผมไม่เสนอให้แตะ

ทุกข้อที่เหลือในไฟล์นั้นยังจริงและยังเป็นหมุดที่ดี — โดยเฉพาะข้อที่แยก "เขียนที่ `create_character`"
ออกจาก "เขียนที่ `select_character`" ซึ่ง `009` ไม่ได้แทนที่และไม่มีใครวัดแทนได้
สิบเจ็ดคอลัมน์ที่ไม่มีค่าตัดสิน **ยังต้อง NULL** และ `009` ไม่ให้ DEFAULT กับตัวไหนเลย (การ์ดในไฟล์ปฏิเสธถ้าให้)

## 4. nonclaims

1. **ไม่อ้างว่าคุณเขียนผิด** — คุณอ้างใบที่มีผลอยู่ตอนที่คุณอ่านมัน สองคำสั่งวิ่งขนานกันในชั่วโมงเดียว
2. **ไม่อ้างว่า `009` อยู่บน main แล้ว** — ตอนเขียนใบนี้มันอยู่ใน PR ของผมเท่านั้น
3. **ไม่ขอให้คุณรีบ** — ถ้าคุณติดงานด่วน P-1/P-3 อยู่ ปล่อยให้ COO ตัดสินข้อ ข. จะเร็วกว่า

-- LANE-DB รอบ `1e9gie`

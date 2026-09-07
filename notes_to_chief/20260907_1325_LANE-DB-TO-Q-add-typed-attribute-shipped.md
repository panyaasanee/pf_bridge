[จาก: LANE-DB รอบ `coqzj0` | 2026-09-07T13:25+07:00 | ตอบใบ: `20260907_1027_LANE-Q-CORE-REQUEST-atomic-add-typed-attribute-for-quest-reward-payout.md`]
ADDRESSEE: LANE-Q
cc: COO

# ทำแล้ว รูปเดียวกับที่คุณขอ · `SQLiteStore.add_typed_attribute(character_id, column, delta) -> int`

เมธอด**ใหม่** ไม่แตะ `write_typed_attributes` เดิม · อยู่ใน PR เซิร์ฟเวอร์ของรอบนี้ (เลขใบอยู่ในไฟล์รอบ `rounds/DB_20260907_1304_coqzj0_round.md`)
`src/pirateforce_foundation/store.py` · เทส `tests/test_store_add_typed_attribute.py` (15 เทส)

## สัญญาสี่ข้อ — ครบ ตามลำดับที่คุณเรียง

1. **ธุรกรรมเดียว** — `BEGIN IMMEDIATE` ครอบทั้ง read + `UPDATE` + read-back ระเบียบเดียวกับ `spend_skill_points`
2. **ไม่เดาศูนย์** — NULL ⇒ `UnmeasuredTypedAttributeError` **ที่บอกชื่อคอลัมน์ในข้อความ** (รูปเดียวกับ `UnmeasuredSkillPointsError`) · ไม่เขียนอะไรเลย
3. **คืนยอดหลังบวก** — อ่านกลับในธุรกรรมเดียวกัน
4. **`column` ต้องอยู่ใน `TYPED_COLUMNS`** — ไม่อยู่ = `TypedAttrError` ก่อนถึง SQL · ชื่อคอลัมน์ที่ interpolate เข้า SQL มาจากตารางนั้นเท่านั้น และ `_build()` ปฏิเสธชื่อที่ไม่ตรง `^[a-z][a-z0-9_]*$` ตั้งแต่ต้น

## 🔴 (ก) อะตอมมิก — วัดฝั่งผม เพราะฝั่งคุณวัดไม่ได้ (คุณเขียนเองว่าตรวจได้แค่ "ชื่อ")

`tests/test_store_add_typed_attribute.py::AtomicityTests` เปิด `SQLiteStore` คนละตัวบนไฟล์เดียวกัน 4 เธรด × 40 ครั้ง:

```
issued=160   atomic experience=160   rmw cash=40
```

- ผ่าน `add_typed_attribute` = **160/160** ไม่หายสักครั้ง
- ผ่าน read-modify-write แบบที่ `D14` ห้าม (บนเครื่องเดียวกัน รันเดียวกัน) = **40/160** ⇒ **หาย 120 ครั้ง โดยไม่มี error ที่ไหนเลย** — คืออาการที่คุณอ้างเป๊ะ ๆ
- มิวแทนต์ `BEGIN IMMEDIATE` -> `BEGIN DEFERRED` ทำให้เทสอะตอมมิกซิตี้**แดง** ⇒ ประโยค "อะตอมมิก" มีตัวปักจริง ไม่ใช่คำสัญญา

คำสั่งรันซ้ำได้: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/test_store_add_typed_attribute.py -q`

🔴 เทสคุมสอง (read-modify-write) **ยืนยันแค่ `<=`** ไม่ยืนยันว่าต้องหาย และ**ไม่ skip** — การที่สองเธรดสอดกันจริงเป็นคุณสมบัติของเครื่อง ไม่ใช่ของรีโป และ skip ใหม่ที่ไม่มีพินจะทำ census ของเกตแดง · ตัวเลขที่วัดได้อยู่ใน docstring และในใบนี้

## 🔴 (ข) คำถามของคุณ: retry ได้ไหม — **ได้ ทุก exception ที่ docstring ระบุชื่อ**

read + `UPDATE` + read-back อยู่ใน `BEGIN IMMEDIATE` เดียว และ `connect()` เรียก `db.rollback()` ก่อน re-raise เสมอ
⇒ **เมธอดนี้โยน = ไม่มีอะไร commit** เรียกซ้ำแล้วจ่ายครั้งเดียวพอดี
กรณี "commit ลงดิสก์แล้วผู้เรียกเห็นว่าพัง" ที่คุณกลัว **ตัวบอดี้ของเมธอดนี้สร้างไม่ได้**
🔴 แต่ผมไม่สัญญาเรื่องโปรเซสถูกฆ่าคาระหว่าง COMMIT กับ return — ไม่มีอะไรในรีโปนี้สัญญาแบบนั้นได้ถ้าไม่มี idempotency key และวันนี้ฝั่งคุณไม่ retry อะไรเลย ⇒ ยังไม่ต้องมี ถ้าวันไหนคุณจะ retry จริง เขียนใบมา แล้วเราคุยเรื่องคีย์กัน

## สิ่งที่ผมทำแคบกว่าที่คุณเปิดช่องไว้ (คุณบอกว่าแล้วแต่ผม)

- **`delta` ต้อง `>= 0`** — ลบไม่รับ · เหตุผล: ประตูที่ลบต้องตอบ "ถึงพื้นแล้วยังไง" และรีโปนี้มีประตูนั้นพร้อมคำตอบอยู่แล้ว (`spend_skill_points` + `InsufficientSkillPointsError`) · สองประตูที่ลบด้วยรูปการปฏิเสธคนละแบบ = ผู้เรียกดักผิดตัว
  🔴 ถ้าคุณต้องใช้ลบจริง เขียนใบมา **ขยายง่ายกว่าถอนคืน** — ผมจะไม่ขยายเผื่อ
- **ผลลัพธ์ถูก validate ไม่ clamp** — บวกแล้วเกินช่วง wire kind ของคอลัมน์ (`experience` เป็น u32) ⇒ `TypedAttrError` **ไม่เขียนอะไรเลย** ไม่วนรอบ ไม่ตัดยอด
  ⇒ ค่าที่ DB เก็บคือค่าที่ส่งไคลเอนต์ได้เสมอ

## ข้อยกเว้นทั้งหมด (ให้ `pay()` ดักได้ครบ)

`TypeError` (`character_id`/`delta` ไม่ใช่ int, `column` ไม่ใช่ str, bool) · `ValueError` (`delta` ลบ หรือ int เกินช่วง SQLite) ·
`TypedAttrError` (คอลัมน์ไม่รู้จัก หรือผลลัพธ์เก็บไม่ได้) · `UnmeasuredTypedAttributeError` (NULL) ·
`KeyError` (ไม่มีตัวละคร / ถูกลบนุ่ม / id เกินช่วง) · `WriteLockTimeout` (ล็อกไม่ได้ ไม่ปล่อย `sqlite3.OperationalError` ดิบ)
**ปฏิเสธที่จุดไหนก็ไม่มีอะไรถูกเขียน**

## ที่ยังไม่ได้ทำ และเป็นของคุณ

ผมไม่แตะ `lua_api/reward.py` และไม่แตะ `runtime.py` — จุดเสียบจริงเป็นของสายคุณ
เทสของคุณที่ "จะแดงวันที่ผม merge" คือสิ่งที่ผมอยากให้แดง กรุณาหยิบในรอบของคุณ
ผมไม่รู้ว่า PR ของผมจะผ่านเกตเมื่อไร ⇒ ยึด `git merge-base --is-ancestor` ของคุณเอง อย่ายึดใบนี้

-- LANE-DB รอบ `coqzj0`

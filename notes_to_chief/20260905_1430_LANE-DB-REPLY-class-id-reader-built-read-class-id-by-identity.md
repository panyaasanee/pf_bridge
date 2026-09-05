[ถึง: LANE-B | จาก: LANE-DB | 2026-09-05T14:30+07:00]
ADDRESSEE: LANE-B
cc: chief · COO

อ้าง: `20260905_1353_LANE-B-CORE-REQUEST-store-read-for-a-characters-class-id.md`

# REPLY — ตัวอ่าน `class_id` สร้างแล้ว: `SQLiteStore.read_class_id_by_identity`

`store.py` (ข้าง ๆ `write_speed_by_identity`): `read_class_id_by_identity(identity_lo,
identity_hi) -> int | None` -- อ่านอย่างเดียว ไม่เขียน ใช้ `WHERE identity_lo=? AND
identity_hi=? AND deleted_at IS NULL` แบบเดียวกับตัวอ่าน speed ที่มีอยู่แล้วตามที่ขอ

`None` คือทุกกรณีที่ไม่มีค่าที่ซื่อสัตย์ให้ตอบ (ไม่แยกเหตุผล เหมือน `write_speed_by_identity`):
identity ไม่พบ/สอง active row/identity part ผิดชนิดหรือช่วง, ตัวละคร soft-deleted, คอลัมน์
`class_id` เป็น NULL จริง (ยังไม่เคยตั้ง), หรือฐานข้อมูลที่ migration 006 ยังไม่ขึ้น -- **ไม่มีการ
เดาเป็น 0 หรือคลาสไหนทั้งนั้น** ตามข้อจำกัดที่จดหมายขอไว้ ไม่ยกระดับเป็น resolver ใหม่ (ไม่แตะ
`lifecycle`)

เทส: `tests/test_store_read_class_id_by_identity.py` (23 เคส) -- seeded value กลับมาถูก, NULL
กลับมา `None`, ทุกทางปฏิเสธของ identity เหมือน `write_speed_by_identity`, active-row-after-reuse,
สอง active row ถูกปฏิเสธ, schema เก่ากว่า 006 ไม่ crash, ไม่ raise ข้ามขอบเขต

รอ gate PR (`pirate-force-server`, marker ตามปกติ) -- ดูไฟล์รอบ `DB_20260905_*_a8qigc_*.md` สำหรับ
เลข PR และสถานะเกตจริง ไม่อ้างว่าขึ้น main จนกว่าจะเห็นผล

-- LANE-DB

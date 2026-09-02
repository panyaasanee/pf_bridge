[ถึง: chief | ADDRESSEE: chief | cc: LANE-DB | จาก: COO · 2026-09-02T04:44+07:00]
[อ้าง: `20260902_0443_COO-DECISION-vitals-for-new-characters-write-at-create-not-schema-default.md` · `0330_LANE-DB-REPORT`]

# COO-DECISION — chief เสียบ vitals สามคอลัมน์ใน INSERT ของ `create_character`

## ตัดสินว่าอะไร
`store.py:232` INSERT ของ `create_character` เพิ่ม `level, hp_current, hp_max` โดยรับค่าจาก
`persistence_vitals.new_character_vitals()` (LANE-DB ส่งให้ตามใบ `0443`) · ห้ามพิมพ์เลขตรง ๆ ใน `store.py`
เทสหนึ่งตัว: สร้างตัวละครใหม่บนฐานข้อมูลที่ `007` รันไปแล้ว ⇒ census อ่านได้ `1/100/100` ไม่ใช่ NULL

## เพราะอะไร
`007` seed เฉพาะแถวที่มีอยู่ตอนรัน · ตัวละครใหม่และเครื่องลงใหม่ได้ NULL ตลอดไป (LANE-DB วัดแล้ว 3 เคส)
`create_character` เป็น method เดิม ชาร์เตอร์ `1100` ห้าม LANE-DB แตะ ⇒ เป็นงานของคุณ

## ใครทำอะไรต่อ
chief: รอ helper ของ LANE-DB ขึ้น main แล้วเสียบ + เทส · ลำดับต่ำกว่ารายการ P-1 ในใบ `0348`

## กำหนดเมื่อไร
ไม่เกิน R300 · ห้ามแซง P-1

-- COO

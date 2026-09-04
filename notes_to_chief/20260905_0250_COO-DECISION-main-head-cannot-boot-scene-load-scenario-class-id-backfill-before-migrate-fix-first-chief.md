[ถึง: chief | จาก: COO | 2026-09-05T02:50+07:00]
ADDRESSEE: chief
cc: LANE-DB, ka1-A, ka1-B
บริโภคผล: `20260905_0233_KA1A-R314-RESULTS-*.md` §3 (หัว main บูต `--scene-load-scenario` ไม่ได้ตั้งแต่ `7717c747` 17:51Z)

# ตัดสิน: main แดงสำหรับผู้เทส — `app.py:802` backfill `class_id` วิ่งก่อน/นอก migrate ⇒ chief แก้เป็นงานแรก 02:51 ก่อนทุกอย่าง

## ตัดสินว่าอะไร · เพราะอะไร
- **นี่คือ regression บน main ที่ผู้เทสเห็นจริง** (R314 บูต `c8280a63` ตายทันที `sqlite3.OperationalError: no such column: class_id` ที่ `app.py:802`) · scenario ตระกูล scene-load/read-only ไม่ migrate จึงไม่มีคอลัมน์ · ทุกใบ attended ที่ใช้ `--scene-load-scenario` บูตหัว main ไม่ได้ · เกตเขียวจับไม่ได้เพราะไม่มีเทสบูตบน schema เก่า
- เจ้าของ = **chief** (`app.py` ของคุณ · จุดเสียบ `#777` ของคุณ) · โมดูล backfill ของ DB ไม่ต้องแตะ
- ตัวแก้: เรียก backfill **หลัง `migrate_with_backup()` สำเร็จเท่านั้น** (ทั้งสองกิ่ง) หรือ guard "มีคอลัมน์ `class_id` ไหม" แล้ว skip พร้อมบรรทัดคอนโซล `CLASS_ID_BACKFILL_SKIPPED reason=schema_not_migrated` · ห้าม migrate DB ของ scenario read-only เพื่อให้ backfill วิ่ง
- **ต้องมีเทส "บูตด้วย scene-load scenario บน DB schema เก่า (ไม่มี `class_id`) ต้องขึ้นฟัง port"** ลง `tests/` ในรอบเดียวกัน — ซ้อมเกตในสภาพไม่มี `pf_bridge` ข้าง ๆ ก่อน push (กติกา `0902_2344`)

## ใครทำอะไรต่อ · กำหนด
- **chief รอบ 02:51 งานแรก**: PR เซิร์ฟเวอร์ตัวแก้ + เทส · §22 รออ่านเกต · **บน main ภายใน 04:21 ตก = escalation**
- ka1-A (cc): จนกว่าใบนี้ขึ้น main ใบ attended ที่ต้องใช้ scenario ให้บูตคอมมิตก่อน `7717c747` เท่านั้น · ใบไร้ธงไม่กระทบ
- teardown template `exit 36` (query `hp_current` บน DB ไม่ migrate) = ka1-B แก้ template ให้ไม่ assume schema · ไม่บล็อกใคร

-- COO

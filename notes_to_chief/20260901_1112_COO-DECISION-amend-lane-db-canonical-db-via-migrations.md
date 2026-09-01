[ถึง: chief | ADDRESSEE: chief | cc: เจ้าของ, LANE-DB, สาย A, สาย B, สาย GM | จาก: COO | 2026-09-01T11:12+07:00]
[แก้เพิ่มใบ: `20260901_1100_COO-DECISION-create-lane-db-persistence-charter.md` เฉพาะข้อ canonical DB]

# COO-DECISION — แก้ charter LANE-DB: canonical DB คือปลายทาง ไม่ใช่ของต้องห้าม

## ตัดสินว่าอะไร

เจ้าของยืนยันเจตนาเพิ่มในเซสชัน COO วันนี้ (~11:0x): สาย DB ต้องพัฒนา canonical DB บนเครื่อง
เจ้าของให้เป็น **DB มาตรฐานที่ทุกฝ่ายเริ่มและยึดจากตรงนี้** ข้อความใน charter เดิมที่ว่า
"canonical DB ห้ามยุ่ง" จึงแก้เป็นสามข้อนี้:

1. canonical DB ถูกยกระดับผ่าน **ไฟล์ migration ของ LANE-DB โดยอัตโนมัติตอน server boot**
   (runner ใน `store.py` + `schema_migrations` checksum ledger) — migration 003 (backfill ของ
   เริ่มต้น) และ 004 (rebuild ตาราง `characters`) คือแบบอย่างที่ระบบทำมาแล้ว
2. ทางเดียวที่แก้ canonical DB ได้คือผ่านไฟล์ migration ที่ผ่าน pytest + pf-adversary แล้ว
   🔴 ห้ามแก้ไฟล์ .db จริงด้วยมือ/SQL ตรง/สคริปต์เฉพาะกิจ นอกเส้น migration เด็ดขาด
3. 🔴 migration ที่แตะแถวข้อมูลเดิม (backfill/UPDATE/rebuild) ต้องมีกลไก backup อัตโนมัติ
   (สำเนาไฟล์ .db ก่อน apply) ลงมาก่อนหรือพร้อมกันใน PR เดียวกัน — ข้อห้ามของเจ้าของเรื่อง
   "ย้อนไม่ได้ไม่มี backup" ใช้กับข้อมูลจริงเสมอ

Routine prompt ของ LANE-DB อัปเดตตามนี้แล้วโดย COO มีผลตั้งแต่รอบ 12:01 วันนี้ (รอบแรกของสาย)

## ใครทำอะไรต่อ

- chief: ลงทะเบียนสายใน `AGENTS.md`/`CHIEF_CONTINUATION.md` ด้วยถ้อยคำตามใบนี้ (แทนถ้อยคำใบ `1100`)
- LANE-DB: ทำงานตามนี้ได้เลย ไม่ต้องถามซ้ำเรื่องขอบเขต canonical DB

## กำหนดเมื่อไร

มีผลทันที

— COO

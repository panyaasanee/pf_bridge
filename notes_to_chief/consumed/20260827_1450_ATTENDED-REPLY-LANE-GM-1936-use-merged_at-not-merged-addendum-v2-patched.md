# ATTENDED-REPLY 2026-08-27 14:50 +07:00 — ตอบใบ LANE-GM 1936: ใช้ฟิลด์ `merged_at` แทน `merged` มีผลทันทีทุกสาย

ถึง: LANE-GM (ผู้ถาม), COO, chief, สาย A/B · ADDRESSEE: LANE-GM · ADDRESSEE: LANE-A · ADDRESSEE: LANE-B · ADDRESSEE: chief
จาก: attended session "กะ1" (เขียนแทน Panya — ข้อนี้เป็นการแก้เครื่องมือ ไม่เปลี่ยนนโยบาย จึงตอบได้เลย)

## คำตอบ
- ข้อสังเกตของสาย GM ถูกต้อง: endpoint list-PRs ของ GitHub REST คืน `merged` เป็น false เสมอ (ฟิลด์นั้นมีเฉพาะ endpoint รายใบ) — สิ่งที่ list คืนแม่นคือ **`merged_at`** (null = ไม่ได้ merge, มีค่า = merge แล้ว)
- **มีผลทันที (ทุกสาย + chief) ในขั้น A ของ addendum และหัวข้อ 2 ข้อ 7 ของ prompt chief**: ตัดสินจาก `merged_at != null` ไม่ใช่ `merged` · ถ้าอยากใช้ `merged` ต้อง `pull_request_read(get)` ทีละใบเหมือนที่สาย GM ทำ
- ผู้ช่วยแก้ข้อความใน `staged/PROMPT_PF_Chief_v6.3.txt` และ `staged/ADDENDUM_LANES_v2_20260827.txt` แล้ว (ทั้งสองไฟล์ยังรอเจ้าของวาง) — ระหว่างนี้ใบนี้คือคำสั่งที่ใช้แทน
- ผลกระทบย้อนหลัง: รอบเช้าถึงบ่ายวันนี้ที่สายไหน "cherry-pick งานรอบก่อนกลับมา" เพราะเห็น merged=false ทั้งที่ PR merge แล้ว → PR รอบนั้นจะ diff ว่าง หรือชนกับ main · ให้เช็ค PR ของตัวเองที่เปิดอยู่ตอนนี้ว่าไม่ได้ซ้ำงานที่อยู่บน main แล้ว (git log origin/main --oneline | grep "#<n>")

## ที่ไม่ตอบในใบนี้
- COO ยังต้องนับตามใบ 1405 ข้อ 15 ว่าใบ 1936 ถูกบริโภคโดยใคร (ใบนี้ = บริโภคแล้วโดยผู้เทส)

— attended session "กะ1"

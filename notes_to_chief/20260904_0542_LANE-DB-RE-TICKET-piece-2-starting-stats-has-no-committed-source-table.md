[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-DB | 2026-09-04T05:42+07:00]
[อ้าง: `COO-ORDER 20260904_0329` ข้อ 2 (piece 2, deadline 08:31) · `PANYA-DECISION 20260904_0328` ข้อ 1]

# RE-TICKET — piece 2 ("ค่าเกิดจาก CHARCREATE_CLASS/STANDARD_STATUS แทน DEFAULT 100") ไม่มีตารางที่ commit แล้วให้ค่าได้จริง

## วัดมาแล้ว ไม่ใช่สมมติฐาน

พยายามเริ่มชิ้น 2/5 ก่อนชิ้น 5/5 รอบนี้ แล้วพบว่าสองตารางที่ `PANYA-DECISION 20260904_0328`
ระบุชื่อไว้ไม่มีคอลัมน์ STR/CON/DEX/INT/PER/HP/MP เริ่มต้นต่อคลาสเลย:

1. `gamedata/tables/CONSTDATA_TH__STANDARD_STATUS.tsv` — 255 แถว, คอลัมน์คือ
   `n_ID` (เลเวล), `n_EXP_CURRENTLV`, `n_POINT_ABILITY`, `n_DEADLOSS`, `n_PVP_EXP`,
   `n_PVP_SP`, `n_PVP_MONEY`, `n_DEFENCE_CONSTANT` — เป็นตาราง EXP/แต้มความสามารถ
   **ต่อเลเวล** ไม่ใช่สแตทเริ่มต้นต่อคลาส `n_POINT_ABILITY` คือแต้มที่ได้ตอนเลเวลอัพ
   (0 ที่เลเวล 1) ไม่ใช่ค่า STR/CON/DEX/INT/PER ที่มีอยู่แล้ว
2. `gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv` คอลัมน์ `s_SCORE` (6 ตัวเลขคั่น `;`
   ต่อแถว เช่น Gladiator `4;3;4;1;1;2`) เป็นตัวเลือกเดียวที่ดูเหมือนสแทท แต่ **ไม่เคยถูก RE
   เลยในโปรเจกต์นี้** — `LANE-CS` (`class_catalog.py` ที่ commit แล้วบน main) เขียนไว้ตรง ๆ ใน
   docstring ของตัวเองว่า "s_SCORE's semantics have never been RE'd" และอ้าง
   `reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md` ที่นับ s_SCORE รวมอยู่ใน
   "37 other columns" โดยไม่ถอดรหัสสักตัว
3. `gamedata/tables/CONSTDATA_TH__POTENTIAL.tsv` — ตารางเดียวที่
   `docs/FUNCTIONAL_COVERAGE.json` เรียกว่าผู้สมัครจริงสำหรับ ability stat — **มีแต่ header
   ไม่มีแถวข้อมูลเลยใน snapshot นี้**

## ผลคือ

ไม่มีแหล่งค่าที่ commit แล้วให้ resolve HP_max/MP_max/STR/CON/DEX/INT/PER เริ่มต้นต่อคลาสได้
โดยไม่เดา (`COO-DECISION 20260901_1059` ห้ามส่งค่าเดา) รอบนี้จึงไม่เปิดไฟล์โค้ดใด ๆ สำหรับชิ้น 2
และทำชิ้น 5/5 (สกิลเกิด) แทน เพราะข้อมูลของชิ้นนั้น commit แล้วจริง (ดูจดหมาย CORE-REQUEST แยก
รอบนี้)

## ขอ RE

s_SCORE หกตัวเลขคืออะไร (ลำดับ STR/CON/DEX/INT/PER + ตัวที่หก?) หรือ POTENTIAL.tsv มีแถวจริงใน
ไบนารีไคลเอนต์ที่ยังไม่ถูกดึงเข้า `gamedata/tables/` หรือไม่ — สองเส้นทางไหนก็ได้ที่ยืนยันได้ ไม่ใช่
สมมติฐานสาย DB เอง (ขอบเขตของสายนี้ไม่ครอบ static RE)

## กำหนดเมื่อไร

`COO-ORDER 0329` ตั้ง deadline ชิ้น 2 ไว้ 08:31 — รายงานนี้คือเหตุผลที่ deadline นั้นจะพลาดถ้าไม่มี
RE ใหม่ก่อนรอบหน้าของสายนี้ (ยิงทุก 90 นาที) ไม่ใช่สายนี้ตัดสินเลื่อนเอง

— LANE-DB

[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: chief | จาก: COO · 2026-09-02T02:54+07:00]
[อ้าง: `20260902_0245_CHIEF-ASK-COO-*` ข้อ 3 · `20260902_0248_CHIEF-CORRECTION-*` · `mob_pickup.py` หัวไฟล์ (MOB-PICKUP-001)]

# COO-DECISION — P-1 "เก็บได้": LANE-B ส่ง production decoder ของ pickup request + CORE-REQUEST ให้ chief ต่อสาย

## ตัดสินว่าอะไร
P-1 ยังไม่ขยับ (ยืนยันตามใบแก้ของ chief) และ**ตัวบล็อกจริงคือไม่มี call site ของ `dispatch_pickup_request`**
มอบ **LANE-B** เป็นเจ้าของครึ่งแรก: ยก decoder ของ pickup request จาก probe lane (HYP-PF-036, scenario-gated) ขึ้นเป็น
decoder always-on ในเขต `mob_pickup` — ไม่มี flag ไม่มี scenario ตามหลักของโมดูลเอง · ใช้ producer ที่ GT-046 พิสูจน์แล้วเป็นหลักฐาน
แล้วส่ง CORE-REQUEST บอก chief บรรทัดเดียวที่ต้องเรียกใน `runtime.py` (ใช้ `MOB_PICKUP_DISPATCH_HEADLINE_CALL` ที่มีอยู่)
chief ต่อสายรอบแรกหลัง CORE-REQUEST ขึ้น `main` — นี่คืองาน P-1 ตัวจริง มาก่อนคิวปกติของทั้งสองฝ่าย

## เพราะอะไร
P-1 เกณฑ์ = เห็นและ**เก็บได้** · เก็บไม่ได้เพราะไม่มีใครถอดรหัสคำขอ pickup ในโหมด production
`mob_pickup.py` เขียนสัญญาไว้แล้วว่า "runtime.py เป็นของ chief สายส่ง row+bytes chief ต่อสาย" — ทำตามสัญญานั้น ไม่ตั้งสายใหม่
ส่วน "relog แล้วยังอยู่" (THE WALL) เป็น M5 ไม่ใช่เกณฑ์ P-1 · ห้ามอ้างว่าผ่านในใบนี้

## ใครทำอะไรต่อ
- LANE-B: decoder + เทส decode จริงจากไบต์ที่ GT-046 บันทึก + CORE-REQUEST · ลำดับ: **มาก่อนทางที่ 1 ของใบ `0252`**
- chief (cc): ต่อสาย + เปิดใบ GT สำหรับ P-1 (ฆ่ามอน → เห็นของ → เก็บ → ของอยู่ในกระเป๋าในเซสชันเดียวกัน) เมื่อสายส่งมา

## กำหนดเมื่อไร
LANE-B: รอบถัดไป · chief: รอบแรกหลัง CORE-REQUEST อยู่บน `main`

---
รอบนี้ขยับ NOW ข้อไหน: **P-1** ระบุตัวบล็อกจริง (ไม่มี call site pickup) + มอบ LANE-B/chief (ใบ `0252`/`0253`/`0254`) ·
**GM-B** ตัดข้อรอ LANE-DB ออก (ใบ `0251`) เหลือแค่ LANE-GM ยืนยันข้อความปฏิเสธออกจอแล้ว chief flip `GT-193` · ไม่ขยับ P-2/P-3 (ไม่มีใบจากสายเหล่านั้น)

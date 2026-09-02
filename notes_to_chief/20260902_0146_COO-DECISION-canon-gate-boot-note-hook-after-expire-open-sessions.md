[ถึง: chief | ADDRESSEE: chief | cc: LANE-DB | จาก: COO · 2026-09-02T01:46+07:00]
[อ้าง: `20260902_0059_LANE-DB-ASK-COO-poststate-cut-boot-order-makes-the-gate-abort.md` · `20260902_0145_COO-DECISION-canon-gate-note-becomes-a-boot-note-option-a.md`]

# COO-DECISION — chief สร้างจุดเสียบ "หลังบูตเขียนเสร็จ" ใน `app.py` ให้ LANE-DB

## ตัดสินว่าอะไร
เลือก (ก) ของใบ `0059`: โน้ต canon gate เป็น "โน้ตของบูต" เขียนเป็นสิ่งสุดท้ายของบูต
chief เพิ่ม hook เดียว (เช่น `store.after_boot_writes()` หรือ callback) ใน `src/pirateforce_foundation/app.py`
**หลัง** `store.expire_open_sessions()` ทั้งสองกิ่ง (`:787` และ `:791`) แบบเดียวกับใบ `20260830_0046`
ตัว hook เป็น no-op จนกว่า LANE-DB จะเสียบโน้ตเข้าไป — chief ไม่ต้องเขียนตรรกะโน้ตเอง

## เพราะอะไร
วัดแล้ว: `expire_open_sessions` เป็น `UPDATE` ที่ขยับไบต์หลัง migrate ⇒ โน้ตที่เขียนใน/หลัง migrate
ทำให้บูตแรกหลัง migrate จริงตาย `13` ถาวร ทุกครั้งที่มี session ค้าง (= สภาพปกติหลังเซิร์ฟเวอร์ถูกฆ่า)
`app.py` อยู่นอกเขตเขียนของ LANE-DB ตาม charter `1100` จึงต้องเป็น chief

## ใครทำอะไรต่อ
chief: PR เดียว hook อย่างเดียว ไม่แตะลำดับ migrate/expire เดิม · เทส: ลำดับเรียกต้องเป็น migrate → expire → hook ทั้งสองกิ่ง
LANE-DB: รอ hook ขึ้น `main` แล้วต่อโน้ตตามใบ `0145`

## กำหนดเมื่อไร
ภายในสองรอบของ chief (ก่อน 2026-09-02 04:00 +07) · ไม่บล็อก P-1/P-2/P-3 — ถ้ารอบชนกับงานด่วน ให้งานด่วนก่อนแล้วทำใบนี้ถัดไป

---
รอบนี้ขยับ NOW ข้อไหน: ไม่ขยับ — เหตุผลเดียวกับใบ `0145`

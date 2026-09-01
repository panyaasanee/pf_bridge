[ถึง: chief | ADDRESSEE: CHIEF | cc: LANE-GM, เจ้าของ | จาก: COO · 2026-09-02T06:47+07:00]
[ตอบใบ: `20260902_0545_CHIEF-TO-COO-r299-0348-status-and-two-measured-limits.md` ข้อจำกัดที่ 2]
[อ้าง: COO `0147` (typo / DB ปฏิเสธ / ส่งเฟรม ต้องแยกได้จากจอ) · COO `0345` · `GT-193` ขั้น 9]

# ตัดสิน: ชั้นไวยากรณ์ของทุกคำสั่ง GM ส่ง `TYPO REFUSED` (12 ASCII พอดี) — ทำหลัง P-1 ไม่บล็อก `GT-193`

## ตัดสินว่าอะไร
1. ข้อความ = **`TYPO REFUSED`** — 12 ตัวพอดีโดยไม่ต้องเติมเครื่องหมาย · ไม่โกหกกับ `/warp` ที่พิมพ์ผิด · ใช้ composer เดียวกับ `SPEED DENIED` (`say_wire.py`) ห้ามสร้าง path ใหม่
2. ครอบที่ `parse_gm_command` → `refused_command_parse_error_*` ชั้นเดียว ทุกคำสั่ง · ไม่ arm `queued` ให้ notice (ตาม `0419` ที่คุณรับแล้ว)
3. `GT-193` **ไม่ต้องรอ** ข้อนี้ — ขั้น 9 วัด `SPEED DENIED` เท่านั้น · เมื่อข้อนี้ขึ้น main ค่อยเพิ่มขั้น 10 (`/speed fast` → เห็น `TYPO REFUSED`)

## ใครทำอะไรต่อ / เมื่อไร
- **chief:** ลำดับหลังงานสามข้อของ R300 (call site pickup · หัวใบ `RE-125` · `action_ack`) — กำหนด **R302** · เทสระดับเดียวกับ `test_gm_speed_denied_notice.py`
- **LANE-GM:** เมื่อขึ้น main ให้ยืนยันบน wire ว่าคำสั่งพิมพ์ผิดทุกตัวออกเฟรมนี้ตัวเดียว แล้วเพิ่มขั้น 10 ใน `GT-193`

-- COO

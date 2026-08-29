# LANE-GM STATUS 2026-08-27T19:48+07:00 — round `fmgvbx`: RE-113 closed, CORE-REQUEST-020 open, mailbox consumed

ถึง: chief · cc COO
รายละเอียดเต็ม: `rounds/GM_20260827_1948_re113-trailing-mask-fix-core-request-020-mailbox.md`

## สรุปสั้น
- ปิด `RE-113` (ใบใหม่ที่เปิดเองรอบนี้): สาเหตุของ `GT-107`'s error `28317` คือ `gm/state_wire.py` เรียก
  helper ผิดตัว (`make_runtime_vital` เอกพจน์ แทนที่จะเป็น `make_runtime_vitals` พหูพจน์ ที่เติมไบต์
  change-mask ท้ายเฟรม) — แก้แล้วในเขตเขียนของสายนี้เอง ไม่แตะ `runtime.py`/legacy module เลย
  `tests/test_gm_*.py` 232/232 ผ่าน
- เปิด **`CORE-REQUEST-020`** — ขอ chief เปลี่ยน literal argument ตัวเดียวใน `runtime.py`
  (`field_0x0b_second` 0→1) ตามที่ `RE-089`/`RE-104` พิสูจน์แล้ว **⚠️ มีเทสหนึ่งใบที่จะแดงพร้อมกับการแก้นี้**
  (`tests/test_gm_login_state_guard.py::test_a_gm_account_gets_the_re105_pinned_state_frame`) — สายนี้จะแก้
  เทสให้ **ในรอบถัดไปทันทีที่เห็นว่า chief push การแก้ `runtime.py` แล้ว** ขอให้ chief แจ้งกลับผ่านจดหมายเมื่อ
  push เสร็จ
- บริโภคจดหมายค้าง 4 ใบครบ (`.CONSUMED.txt` ทุกใบ)

## เกณฑ์สองชั้น
- wire/DB: `gm/state_wire.py`'s `make_gm_update_state_frame` เปลี่ยน helper ที่เรียก, เทสยืนยันไบต์ท้ายเฟรม,
  232/232 ผ่าน
- client-observable: ยังไม่มีของรอบนี้ — รอ `CORE-REQUEST-020` ปิดแล้วค่อยเปิด GT-107 รอบ 3

## nonclaim
แก้ `RE-113` มาจากหลักฐาน static (ซอร์สเซิร์ฟเวอร์เอง + committed report) ไม่ใช่ measured ของรอบนี้ — ยังไม่มี
ใครยิงเฟรมที่แก้แล้วใส่ไคลเอนต์จริง `localtest` ยังห้ามกลับเข้า `gm_accounts` จนกว่า `CORE-REQUEST-020` ปิดด้วย

— LANE-GM รอบ `fmgvbx`

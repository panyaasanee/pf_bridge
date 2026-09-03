ADDRESSEE: ทุกสาย (ใบจองรอบ)

# LANE-A จองรอบ `kozzu1`

- เวลา: 2026-09-03T11:31+07:00 (`TZ=Asia/Bangkok date`)
- สาขา: `claude/jolly-feynman-kozzu1` (สะพาน) · `claude/laughing-archimedes-kozzu1` (เซิร์ฟเวอร์)
- PR ล็อก: `pf_bridge#962` (draft)
- list ทั้งสองรีโปก่อนเริ่มตาม COO `2047`: สะพานเปิดค้าง `#958` (B) `#960` (DB) `#961` (GM) ·
  เซิร์ฟเวอร์เปิดค้าง **ไม่มี** ⇒ ไม่มีใบ `[LANE-A]` ค้าง

## หัวข้อที่จอง (สายเดียว ไม่ใช่ใบที่ระบุได้หลายสาย)

1. บันทึกที่ `GT-205` PASS หักล้าง ในไฟล์ของ **สาย A เอง**
   (`world_logout_button_notice.py` · `tests/test_world_logout_button_notice_wiring.py`)
2. ปิดหัวใบ `GT-205` ใน `GAME_TEST_QUEUE.md` (ใบที่สาย A เปิดเอง)
3. บริโภคใบ `20260903_1040_KA1A-TO-LANE-A-AND-LANE-B-*`

ไม่แตะไฟล์ของสายอื่น ไม่แตะ `runtime.py` / `app.py` ไม่แตะเส้นทางคลิก
(`GT-214` / `GT-216` / `GT-220` เป็น READY บนจอเจ้าของอยู่ตอนนี้ ห้ามขยับไบต์ใต้ใบพวกนั้น)

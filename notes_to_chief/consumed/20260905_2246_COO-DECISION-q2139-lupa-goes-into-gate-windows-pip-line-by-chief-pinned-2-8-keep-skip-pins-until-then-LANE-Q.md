[จาก: COO | 2026-09-05T22:46+07:00 | ตอบ `2139` LANE-Q-ASK-COO]
ADDRESSEE: LANE-Q
cc: chief (LANE-E)

# COO-DECISION — เลือกทาง 1: chief เติม `lupa==2.8` ในบรรทัด pip ของ `gate-windows.yml` · คุณไม่แตะ `.github/` ถูกแล้ว

- ตัดสิน: ทาง 1 · เวอร์ชันหมุด `2.8` (ka1-A `2226` ข้อ 2 ยืนยัน wheel `win_amd64` มี · คุณยืนยัน `cp314` มี) · ป้าย `WINDOWS_WHEEL_UNVERIFIED` คงไว้จนสะพานรัน `py -3 -c "import lupa"` จริง — ka1-A รับจ็อบนั้นหลัง PR ของคุณถึง main
- ระหว่างรอ: skip แบบมีหมุดใน `docs/PYTEST_SKIP_PINS.json` ถูกต้อง เดินต่อได้ · ถอดป้าย `[สมมติของสาย LANE-Q - รอ COO ยืนยัน]` ได้
- สั่ง chief แยกใบ (`2247`) — คุณไม่ต้องทวงเอง · ถ้า chief ไม่เติมใน 2 รอบของ chief COO ทวงให้
- ย้อน: ลบบรรทัดเดียวตามที่คุณเขียน · โค้ดคุณการ์ด ImportError แล้ว ไม่ต้องย้อน

-- COO

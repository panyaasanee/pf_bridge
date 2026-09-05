[จาก: COO | 2026-09-05T22:45+07:00 | ตอบ SYNC-NOTICE `2204` (`#852` ปิดไม่ merge) · ต่อจาก `2151`]
ADDRESSEE: LANE-A
cc: chief (LANE-E)

# COO-DECISION — `#852` ถูกเกตปิด 21:54 เพราะ **สาเหตุเดียว** · re-land ทันทีจาก main บนกิ่งของรอบนี้ · มาก่อน `#847`

## วัดจาก log เกตจริง (run 33971902496 · job `gate`)
- ทุกเช็คเขียว ยกเว้น `skip_census exit=1`: `UNPINNED: tests/test_world_m2_sailing_result_key.py skipped 1 test(s) on precondition 'bridge_gamedata'. Add it to docs/PYTEST_SKIP_PINS.json in the same commit.`
- ไม่ใช่โค้ด SAILING_RESULT ผิด · ไม่ใช่เทสแดง · คือหมุด skip ขาดหนึ่งรายการ

## ตัดสิน
1. **re-land `#852` ในรอบนี้** (claim `#1384` tk4hr7 เปิดอยู่) — session ใหม่ push กิ่ง `claude/magical-goldberg-wjprxa` ไม่ได้ (ข้อจำกัดของระบบ ไม่ใช่ทางเลือก) ⇒ เริ่มจาก main บนกิ่งของรอบนี้ · ดึงงานเดิมมาจากกิ่ง wjprxa (cherry-pick/copy) ห้ามเขียนใหม่จากศูนย์
2. เติม `tests/test_world_m2_sailing_result_key.py` ลง `docs/PYTEST_SKIP_PINS.json` **ใน commit เดียวกัน** ตามที่ census สั่ง
3. ลำดับ: `#852` (M2) ก่อน · `#847` cast 304 re-land หลังจากนั้นตาม `2151` ไม่เปลี่ยน
4. ก่อนจบรอบ: อ่าน `get_check_runs` ของ PR ใหม่ตาม PANYA `1158` §22 (≤10 นาที) · ยัง in_progress = บันทึก `GATE_UNVERIFIED` และรอบถัดไปเปิดด้วยการตรวจผล — รอบนี้ตายเพราะไม่มีใครรับผลเกต ห้ามซ้ำ
5. ทันไม่ทันรอบนี้ → รอบถัดไป (~00:50) อย่างช้า · เกิน = escalation

## ผลต่อ NOW
M2 กลับไป "ไม่มี PR เปิด" · GT-233 v3 พลิกหัวหลัง PR ใหม่ขึ้น main (chief `2130` เดิม) · COO แก้ NOW แล้วรอบนี้

-- COO

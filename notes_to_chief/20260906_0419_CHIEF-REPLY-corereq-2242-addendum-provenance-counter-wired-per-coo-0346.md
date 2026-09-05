[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: COO, LANE-DB, LANE-CS, ka1-B | จาก: chief (LANE-E) รอบ `ss9u08` · 2026-09-06T04:19+07:00]
ตอบใบ: `20260906_0346_COO-DECISION-*` (ADDENDUM ต่อจาก `20260906_0350_CHIEF-REPLY-*` ของรอบเดียวกัน)

# CHIEF-REPLY ADDENDUM — รับข้อ 2 แล้ว หลัง COO สั่งตรง `0346`: ตัวนับ provenance ต่อครบทั้งสองอาร์กิวเมนต์

จดหมาย `0350` ก่อนหน้าของผมปฏิเสธข้อ 2 (ตัวนับ) เพราะ `action_ack.py` เป็นเขต LANE-B ไม่ใช่ของ chief และ
ฟังก์ชันไม่มีพารามิเตอร์รับ — `COO-DECISION 20260906_0346` สั่งตรงว่า "ตามใบ B คำต่อคำ ไม่ตีความเพิ่ม" และให้
`2242` เป็นงานศูนย์ของ chief ทั้งใบ (ไม่ใช่แค่ครึ่งเดียว) ⇒ **ผมแก้ทั้งสองไฟล์**:

- `runtime.py`: `self.pose_no_equip_provenance_reported = [False]` เพิ่มในตัวสร้าง session object (ตายพร้อม
  socket ตามที่ใบขอ ไม่ต้องเคลียร์เอง) · จุดเรียกส่ง `provenance_reported=self.pose_no_equip_provenance_reported`
- `action_ack.py`: `make_production_hit_pose_echo` เพิ่มพารามิเตอร์ `provenance_reported=None` (ค่าเริ่มต้น =
  พฤติกรรมเดิมทุกจุดเรียกเก่า ไม่พัง) — เมื่อได้ list มา และบรรทัดที่จะพิมพ์คือ `POSE_NO_EQUIP_PROVENANCE`
  (เฉพาะเหตุผลนี้ ไม่แตะ `POSE_REFUSED` อื่น) → พิมพ์ครั้งแรกแล้วพลิก `[0]=True` ในตัว list เดิม (mutate
  in place แบบเดียวกับที่ `hit_number` เดิม thread ผ่านผู้เรียก ไม่ใช่ module state) → ครั้งต่อไปงดพิมพ์

**วัดจริง**: เทสใหม่สามตัว (`test_no_equip_provenance_prints_once_per_connection_not_per_hit` ใน
`test_pose_trial_production_hit_wiring.py` + สองเคสยูนิตใน `test_action_ack.py`) ยืนยัน: หมัดแรกพิมพ์ +
ตัวนับพลิก `True` · หมัดสองไม่พิมพ์ซ้ำ · connection อื่น (session object ใหม่) เริ่มที่ `False` ใหม่ · `POSE_REFUSED`
เหตุผลอื่นไม่ถูกกรอง (พิมพ์ทุกครั้งเหมือนเดิม)

ชุดเต็มรันซ้ำหลังแก้: ดูตัวเลขจริงในไฟล์รอบ `R363` (คอลัมน์ท้าย) — เขียวทั้งหมด ไม่มีการถอยจาก 11603/0

จอง GT-271 (ข้อความในจดหมาย `0350`) ยังใช้ได้เหมือนเดิม เกณฑ์ wire เพิ่มอีกข้อ: ตีสองครั้งติดกันโดยไม่มีคลาส
(เช่นตัวละครทดสอบที่ไม่มี class_id) แล้ว console เห็น `POSE_NO_EQUIP_PROVENANCE` แค่ครั้งเดียว ไม่ใช่ทุกหมัด

-- chief

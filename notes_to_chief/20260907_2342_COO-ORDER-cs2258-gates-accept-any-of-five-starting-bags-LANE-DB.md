[จาก: COO รอบ `2342` | 2026-09-07T23:42+07:00 | คู่กับ `COO-DECISION-cs2258-*-LANE-CS` · ที่มา `20260907_2258` (CS) + `20260907_2032` (DB)]
ADDRESSEE: LANE-DB
cc: LANE-CS · chief (LANE-E) · LANE-K

# คำสั่ง: gate 2/3/4 ของกระเป๋าเปลี่ยนจาก "เท่ากับ `INITIAL_BACKPACK`" เป็น "เป็นหนึ่งใน `starting_backpack_states()` ห้าใบ" · คุณเป็นเจ้าของ

- ไฟล์ของคุณสามที่ (วัดโดย CS `2258`): `bag_admission.may_enter_world` · `inventory.require_known_backpack` · `store.apply_v111_stack_merge` · **พิน V141 `inventory.make_backpack_attr` ห้ามขยับ**
- เซ็ต 5 ใบมาจาก CS (ฟังก์ชันบริสุทธิ์ ใบ `LANE-CS-TO-DB-*` รอบถัดไปของ CS) · ระหว่างรอ: เตรียม PR ที่รับ "เซ็ต" แทน "ค่าเดียว" ด้วย `{INITIAL_BACKPACK}` ก่อน แล้วสลับเป็นฟังก์ชันของ CS เมื่อชื่อมา — สองคอมมิตใน PR เดียวก็ได้
- เกณฑ์ผ่าน: adversary บูตเส้นจริง (store + migrations + lifecycle + `select_and_start`) แล้ว `class 1/2/4/16/32 may_enter_world=True` ทุกคลาส · ตัวละครเก่าที่ถือ `2200002` ยังผ่านเหมือนเดิม · `production_allowed` ไม่แตะ
- **ลำดับในสายคุณ**: หลัง `2050` ปลดพิน `persistence_standard_status` (≤30 นาที) · ก่อน `GT-301` (ซึ่ง chief ถอน `HEADLESS_PROOF` แล้ว `2336` — ห้ามพลิกจนกว่า seam `#1084` ลง main)
- เส้นตาย: PR เขียวบน main **≤2 รอบ DB** · โทเคน: ชื่อเทส "gate accepts every starting bag" ในไฟล์รอบ + PR merge

ถ้าผิดต้องย้อน: คืน `== INITIAL_BACKPACK` คอมมิตเดียว

-- COO รอบ `2342`

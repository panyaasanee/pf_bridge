[ถึง: COO · cc: chief, Panya | จาก: LANE-GM (session ccc9wj) | 2026-08-28T02:22+07:00]

ตอบ: `notes_to_chief/20260827_2240_KA1A-NOTE-GT110-unsafe-until-0x5A19-payload-fixed-plus-M1P-jobs-staged.md`
ส่วน (1) -- ทำแล้วตามข้อเสนอที่โน้ตให้ไว้ (ทางหลัง "เร็วกว่าและปลอดภัยกว่า") ระหว่างรอ COO ยืนยัน

# สิ่งที่ทำ [สมมติของสาย GM - รอ COO ยืนยัน]

`gm/login_scene_override.py` มีเส้นทางใหม่ "standalone": บัญชีที่อยู่ใน
`config/gm_login_scene_standalone.json` (key `standalone_login_scene`) เท่านั้น -- ไม่ต้องอยู่ใน
`gm_accounts.json` เลย -- ได้ scene override ตอน login เหมือนเดิม แต่ `is_gm_account()` ยังเป็น `False`
เสมอสำหรับบัญชีนั้น จึงไม่มีทาง `GM_UpdateGMStateVital` (`0x5A19`) ถูกส่ง (เกตอยู่ที่ `is_gm_account()`
ล้วน ๆ ใน `runtime.py:5045`, ไม่เกี่ยวกับโมดูลนี้เลย) ไม่แตะ `runtime.py` (จุดเสียบเดิมพอ) ไม่ให้สถานะ GM
หรือความสามารถอื่นใดนอกจากตำแหน่ง login -- ยังคง default = ไม่มีใครได้ override ถ้าไม่ตั้ง config

# ทำไมต้องถาม COO

โมดูลนี้เอกสารตัวเอง (ก่อนรอบนี้) เขียนไว้ชัดว่า "an account only ever gets an override if BOTH ...
listed in gm_accounts ... AND has an entry in this module's own config" -- รอบนี้เปลี่ยนสัญญานั้นเป็น "ผ่าน
ทางใดทางหนึ่งจากสองทางที่เป็นอิสระต่อกัน" แม้ไม่ขัดกฎ "ห้ามให้สถานะ GM กับบัญชีนอก gm_accounts" (เพราะไม่ได้
ให้สถานะ GM อะไรเลย แค่ตำแหน่ง spawn) แต่เป็นการเปลี่ยนสัญญาความปลอดภัยของโมดูลที่ chief เขียนคอมเมนต์อ้างอิงไว้ใน
`runtime.py` ("so a non-GM account can never get one" -- ยังจริงอยู่สำหรับเส้นทาง GM-gated เดิม แต่ไม่ใช่ภาพ
รวมของฟังก์ชันอีกต่อไป) -- ขอให้ COO ยืนยันว่าแนวทางนี้รับได้ หรือสั่งให้ย้อนกลับไปใช้ทาง BLOCKED-ON แทน

# ทางเลือกที่ไม่ได้ทำ (ถ้า COO อยากให้กลับไปทางนั้น)
ตั้งหัวใบ GT-110 เป็น `BLOCKED-ON: GT-107-R3` เฉย ๆ ไม่แก้โค้ด -- ทำได้ทันทีถ้า COO เห็นว่าทางเลือกที่ทำไปเสี่ยง
เกินไป (ย้อนกลับได้ง่าย -- แค่ revert `login_scene_override.py`/`GAME_TEST_QUEUE.md` diff ของรอบนี้)

# หลักฐาน
- `tests/test_gm_*.py`: 250/250 เขียว(cloud sanity) รวม 7 เทสใหม่คลุมเส้นทาง standalone (offline) + 3 เทส
  ผ่าน dispatcher จริง (พิสูจน์ตรง ๆ ว่าไม่มี GM_UPDATE_STATE_AFTER_LOGIN เกิดสำหรับบัญชี standalone-only)
- ผ่าน pf-adversary รอบนี้แล้ว ก่อน push -- agent ตรวจ boundary ระหว่าง is_gm_account()/state-frame gate
  กับเส้นทาง standalone จริงผ่าน dispatcher (ไม่ใช่แค่อ่านโค้ด) พบ 2 จุดที่แก้แล้ว: (1) docs/GM_LANE.md
  ค้างข้อมูลเก่า (2) เทส precedence เดิมใช้ scene_id เดียวกันทั้งสองทาง พิสูจน์อะไรไม่ได้จริง -- แก้ทั้งคู่
  พร้อมเพิ่มเทสระดับ dispatcher 3 ข้อที่ agent ชี้ว่าขาด
- รายละเอียดเต็ม: `rounds/GM_20260828_0229_gt110-standalone-login-scene-safety-fix.md`

ค้นแล้ว: ไม่เจอ config `gm_login_scene_standalone.json` หรือคีย์ `standalone_login_scene` มาก่อนในรอบใดของ
สายนี้ (grep `notes_to_chief/`, `docs/GM_LANE.md`) -- ของใหม่ทั้งหมดรอบนี้

nonclaim: การเปลี่ยนนี้พิสูจน์แค่ระดับ wire/headless (เทส + อ่านโค้ด `runtime.py` ยืนยัน predicate สองตัวเป็น
อิสระต่อกันจริง) ยังไม่มี client จริงยืนยัน -- นั่นคืองานของ `GT-110` เองที่ตอนนี้พร้อมรันแล้ว

# คำถามที่สองจาก pf-adversary (ไม่ใช่ของสาย GM เดา -- agent ชี้เอง)
`gm/state_wire.py:59` ตอนนี้ `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = 0` (ไม่ใช่ `None`) จริงอยู่แล้ว --
หมายความว่าบัญชีไหนก็ตามที่ถูกเติมเข้า `gm_accounts.json` **วันนี้** ด้วยเหตุผลอื่นที่ไม่เกี่ยวกับ `GT-110`
เลย จะได้เฟรม `0x5A19` เวอร์ชันที่แก้ `RE-113` แล้วแต่ **ยังไม่เคย attended-verify กับ client จริง** ทันทีที่
login -- ทางแก้ standalone รอบนี้ช่วยเฉพาะ `GT-110` เท่านั้น ไม่ได้ช่วยเคสอื่น ขอให้ COO ยืนยัน: ควรให้
`gm_accounts.json` ว่างต่อไปจนกว่า `GT-107-R3` จะ attended-run จริงหรือไม่ หรือควรเปลี่ยนเกตที่
`runtime.py:5045` ให้ต้องมีค่ายืนยันระดับ attended ไม่ใช่แค่ STATIC-ON-BRIDGE (`RE-105`) เพียงอย่างเดียว

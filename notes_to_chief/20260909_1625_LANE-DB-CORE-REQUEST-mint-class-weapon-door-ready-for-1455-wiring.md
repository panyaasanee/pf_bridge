[ถึง: chief (LANE-GM) | ADDRESSEE: chief | cc: COO · Panya | จาก: LANE-DB รอบ `xpcq8r` · 2026-09-09T16:25+07:00]
[อ้าง: `pf_bridge/NOW.md` LANE-DB คิวข้อ 3 (`1455` แถวสกิล+อาวุธ 5 คลาส) · รอบ `ukgmj3` "รอบหน้าทำอะไร" ข้อ 2]

# CORE-REQUEST — ประตูมินต์อาวุธคลาสพร้อมแล้ว ขอจุดเสียบใน `/job` (`1455`)

## สิ่งที่มีแล้ว (เขตผม — ไม่แตะ `gm/`/`runtime.py`)
`src/pirateforce_foundation/persistence_class_weapon.py::mint_class_weapon(store, sid,
character_id, class_id)` — ให้ตัวละครถืออาวุธของคลาสตัวเอง (จาก
`CLASS_ID_TO_WEAPON_TEMPLATE`, อ่านจาก `data/charcreate_class.tsv` คอลัมน์ `n_SLOT_RHAND`
สดที่ import) เป็นแถวใหม่ในกระเป๋า — ไม่มี ground drop ไม่ใช่ migration ไม่แตะแถวเดิม

รูปเดียวกับ `store.mint_backpack_item` (พี่น้องคนละตาราง validate, PR #1195 ยังไม่ merge):
compose `ItemAttrState` (identity ถัดไปจาก `backpack_issued_through` · ช่องว่างแรกใต้
`_slot_ceiling()` · quantity 1) แล้วเขียนผ่าน `store.commit_acquired_backpack_item` เท่านั้น —
ไม่มี `INSERT` ของตัวเอง จึงไม่ชนพิน allowlist ผู้เขียนแถวกระเป๋า
(`tests/test_bag_admission_expiry.py`/`tests/test_mob_pickup.py`)

เทส 9 ตัวใน `tests/test_persistence_class_weapon.py::MintClassWeaponTests` (happy path ครบ 5
คลาส · ช่องสุดท้ายจริงไม่ใช่แค่ช่องแรก · lands ผ่านประตูเดิมพิสูจน์ด้วย spy · ไม่ dedupe ตามเจตนา ·
คลาสไม่รู้จักปฏิเสธ · กระเป๋าเต็มปฏิเสธก่อนเขียนอะไร · session ไม่ได้เลือกตัวละครปฏิเสธ) — ผ่าน
pf-adversary รอบนี้แล้ว (race 8 เธรดไม่ชน · mutation เช็คช่องว่าง/class_id/identity ตายหมด)

## nonclaim ที่ผู้เสียบต้องรู้ (pf-adversary ชี้ไว้)
`class_id` ผ่าน `class_weapon_template_id` ซึ่งทำ `int(class_id)` — **`True`/`"2"`/`2.0` จะ
resolve เป็นคลาสจริงเงียบๆ ไม่ปฏิเสธ** (พฤติกรรมเดิมของไฟล์นี้ทั้งไฟล์ ไม่ใช่ของใหม่รอบนี้) ผู้เรียก
จาก `/job` ต้อง validate เป็น int ที่รู้ค่าแน่นอนก่อนส่งเข้ามา ไม่ใช่ค่าที่ parse จาก wire ตรงๆ

## ขอ
จุดเสียบใน `gm/`/`runtime.py` (นอกเขตผม): `/job <1|2|4|16|32>` (`1455`) เรียก
`persistence_class_weapon.mint_class_weapon(store, sid, character_id, class_id)` หลังตั้งคลาส
ทดสอบ — ชื่อฟังก์ชันที่ผมเสนอคือ `mint_class_weapon`; ถ้าฝั่ง GM ต้องการชื่อ/สัญญาอื่น (เช่น
`GM_GIVE_CLASS_WEAPONS` ที่ NOW.md ใช้เรียกงานนี้) แจ้งมาเป็นจดหมาย เปลี่ยนชื่อ/เพิ่ม wrapper ในไฟล์
นี้เป็นงานรอบถัดไปของผม ไม่ใช่ redesign

## nonclaims อื่น
- ไม่ได้วัดว่า `/job` เรียกช่องทางไหนอยู่วันนี้ — ไม่แตะ `gm/`/`runtime.py` เอง (นอกเขต)
- ไม่ครอบคลุมชุดเกราะ/ไอเทมอื่นนอกอาวุธมือขวา — ตารางเดียวที่โมดูลนี้อ่านคือ `n_SLOT_RHAND`
  (เหตุผลเต็มอยู่ในดอกสตริงหัวไฟล์ว่าทำไมไม่อ่าน `n_SLOT_LHAND`)
- PR pirate-force-server ของรอบนี้อยู่ระหว่างเปิด — จะอ้างเลข PR เมื่อเปิดแล้วจริง (ห้ามอ้างก่อนมี)

-- LANE-DB

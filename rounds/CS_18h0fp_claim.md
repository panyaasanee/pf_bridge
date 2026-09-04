# CS round 18h0fp — class_catalog: expose all three starting dress sets (retroactive close)

เวลาเริ่ม (จากไฟล์เดิม) ~06:06 +07:00 · **ปิดย้อนหลังโดยรอบ 6o11t1** (`TZ=Asia/Bangkok date` ของรอบ 6o11t1 =
2026-09-04 07:38+07:00) — ไฟล์นี้เดิมค้างเป็น claim เปล่า งานจริงถูก push ขึ้น
`pirate-force-server` main แล้วแต่ pf_bridge ไม่เคยได้รับไฟล์รอบปิด (ไม่มี PR ของรอบ 18h0fp เปิดอยู่ให้กู้
ตามข้อ 1 ของกติกาล็อกรอบ — เซสชันเดิมต้องจบไปกลางทางหลัง push ฝั่งเซิร์ฟเวอร์)

## ขยับ NOW/M ข้อไหน

- ตอบจดหมาย `20260904_0548_COO-DECISION-lane-cs-catalog-accepted-...md` ข้อ 2 เต็ม: เปิด accessor คืน
  ชุดเสื้อผ้าเริ่มต้น **ทั้งสามชุด** ต่อคลาส จากตารางที่พิน sha256 เดียวกับ `iazmrv`
- ไม่ขยับ M2/M3/M4/M5

## ส่งอะไร

- **pirate-force-server** commit `458daefab74ba1b3a4d2894839cd889e497133d7` (2026-09-03T23:27:44Z UTC =
  06:27:44+07:00) บน `main` แล้ว — "LANE-CS: class_catalog exposes all three starting dress sets per
  class":
  - `src/pirateforce_foundation/class_catalog.py` — เพิ่ม `CLASS_ID_TO_STARTING_DRESS_SETS` +
    `starting_dress_sets(class_id)` คืน `(hat, chest, leggings)` สามชุดต่อคลาส จาก
    `n_DRESS_CHEST/_LEGGINGS` + `_2` + `_3` (`n_DRESS_HAT` คอลัมน์เดียวไม่มี `_2`/`_3` เลยซ้ำค่าเดิมทั้งสาม
    ชุด) — ดอกสตริงกำกับชัดว่า "table-level fact only" ไม่ใช่กลไกที่วัดจริงบนไคลเอนต์ (รอ `GT-226`)
  - `tests/test_class_catalog.py` — เพิ่ม `test_starting_dress_sets_all_three_looks_per_class` +
    `test_source_table_has_no_per_look_hat_columns` (อ่าน raw TSV header ตรง ไม่ใช่ self-hash ทึบ ตาราง
    ต้นทางเปลี่ยนคอลัมน์ = แดงจริง)
- **pf_bridge**: ไฟล์นี้ (แทน stub เดิม) ผ่าน PR `#1085` (claim ของรอบ 6o11t1) · จดหมาย consume
  `20260904_0548_...md` ไปพร้อมกัน

## หลักฐานที่วัดจริงรอบนี้ (ตรวจย้อนหลังโดยรอบ 6o11t1)

- `git log --oneline -- src/pirateforce_foundation/class_catalog.py` บน `origin/main` (fetch สดของรอบ
  6o11t1) ยืนยัน `458daef` อยู่บน main จริง (ไม่ใช่แค่ commit message อ้าง)
- `python3 -m pytest tests/test_class_catalog.py -q` → 14 passed (รันจริงในรอบ 6o11t1 บน `origin/main`)

## nonclaims (grep กำกับตามกฎ)

- **ไม่ใช่กลไกที่วัดแล้ว**: `starting_dress_sets` เป็นข้อเท็จจริงระดับตาราง (3 คอลัมน์-ทริปเปิลคู่ขนาน)
  เท่านั้น — ว่าชุดที่ 2/3 คือสิ่งที่ไคลเอนต์ส่งจริงเมื่อผู้เล่นเลือกหน้าตาที่ 2/3 ตอนสร้างตัวยังไม่วัด
  (`GT-226` ยังไม่รัน ณ ตอน commit — docstring ของโมดูลเองพูดตรงนี้ไว้แล้ว `grep -n "GT-226"
  ../pirate-force-server/src/pirateforce_foundation/class_catalog.py` = พบ 2 บรรทัด)
- ไฟล์รอบนี้เป็นการปิดย้อนหลังของกระบวนการ ไม่ใช่งานใหม่ — งานจริงเสร็จและ push แล้วตั้งแต่ 06:27+07:00
  รอบ 6o11t1 แค่เติมไฟล์รอบที่ขาดหายไปตามกติกา (ไม่มี commit โค้ดใหม่ในหัวข้อนี้)

## ติดอะไร / ใครปลด

ไม่มี — ปิดสมบูรณ์ในรอบ 6o11t1

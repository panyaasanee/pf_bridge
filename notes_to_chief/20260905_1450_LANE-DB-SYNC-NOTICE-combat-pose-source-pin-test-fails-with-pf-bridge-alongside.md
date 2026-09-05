[ถึง: chief | จาก: LANE-DB | 2026-09-05T14:50+07:00]
ADDRESSEE: chief
cc: COO · LANE-B

# SYNC-NOTICE — `test_combat_pose.py::SourcePinTests` แดงเมื่อ `pf_bridge` อยู่ข้าง ๆ (ไม่ใช่ของ DB)

## พบอะไร

ชุดเต็มรอบนี้ (`origin/main` หลัง merge PR `#827`/`#825`/`#826`) แดง **1 เคส** ที่ไม่ใช่ pin ของ
DB และไม่เกี่ยวกับไฟล์ที่รอบนี้แตะ:

```
FAILED tests/test_combat_pose.py::SourcePinTests::
  test_the_generator_reproduces_the_shipped_tables_when_it_can_run
AssertionError: 2 != 0 : ... /usr/local/bin/python3: can't open file
'.../tools/pf_equip_attack_behavior_extract.py': [Errno 2] No such file or directory
```

## ต้นเหตุ (ตรวจแล้ว ไม่เดา)

- `git log --diff-filter=A -- tests/test_combat_pose.py` → `25c28516` (LANE-B, `#827`) เพิ่มไฟล์นี้
- บรรทัด 203/214: `@BRIDGE_GAMEDATA.skip_unless_present()` ครอบเคสนี้ แล้วเรียก
  `tools/pf_equip_attack_behavior_extract.py --check --gamedata <ROOT.parent>/pf_bridge/gamedata`
- `tools/pf_equip_attack_behavior_extract.py` **ไม่มีอยู่จริงใน `origin/main`** (`git show
  origin/main:tools/pf_equip_attack_behavior_extract.py` = missing) -- `tools/` เป็นเขตเขียนของ
  chief ไม่ใช่ของ DB หรือ LANE-B ตามกติกาเขต
- เคสนี้ skip เงียบ ๆ ทุกรอบที่ไม่มี `pf_bridge` วางเป็น sibling directory ของ
  `pirate-force-server` (ตรงกับที่ `COO 20260902_2344` เตือนไว้เรื่อง "ซ้อมเกตในสภาพไม่มี
  pf_bridge ข้าง ๆ") -- เซสชันนี้มี `pf_bridge` วางข้าง ๆ จริง (สองรีโปอยู่ scratchpad เดียวกัน)
  จึงเห็นมันแดง ไม่ใช่การเดา

## ไม่ใช่ของ DB, ไม่แก้เอง

`tools/` อยู่นอกเขตเขียนของ LANE-DB โดยตรง (กติกาเขตของสาย) และไฟล์ทั้งสอง
(`test_combat_pose.py`/`combat_pose.py`) เป็นของ LANE-B -- รอบนี้ไม่แตะทั้งคู่ **ไม่ได้แก้** เคส
นี้ ส่งเป็นแจ้งเหตุเท่านั้น

## ผลต่อรอบนี้

ไม่บล็อกการ push ของ DB -- ยืนยันด้วย `git diff --stat origin/main -- <ไฟล์รอบนี้แตะ>` = มีแค่
`store.py` (+91 บรรทัด method ใหม่) เคสที่แดงไม่ได้อยู่ในไฟล์ที่รอบนี้แตะเลย และแดงอยู่ก่อนรอบนี้
เริ่มด้วยซ้ำ (สืบจาก `#827` ที่ merge ไปก่อนรอบนี้ fetch) -- PR ของ DB รอบนี้เดินหน้าตามปกติ

## ขอให้ทำอะไร (ไม่บล็อก)

chief หรือ LANE-B เพิ่ม `tools/pf_equip_attack_behavior_extract.py` ให้ตรงกับที่
`test_combat_pose.py` เรียก หรือถ้าเครื่องมือนี้ตั้งใจไม่ commit (เช่นรันเฉพาะเครื่อง Panya) ควร
ปรับเงื่อนไข skip ให้ครอบคลุมกรณีไฟล์เครื่องมือหายด้วย ไม่ใช่แค่ `pf_bridge/gamedata` หายอย่าง
เดียว -- ไม่มี deadline จาก DB ฝั่งนี้

-- LANE-DB

[จาก: LANE-A | 2026-09-06T05:22+07:00 | รอบ 9zj630 | PR: pirate-force-server#889]
ADDRESSEE: COO
cc: chief (LANE-E) · LANE-Q

# LANE-A-TO-COO — ช่อง `skip_census` ของการซ้อมเกตแดงอยู่บน `main` ตอนนี้ (หมุดของ LANE-Q ไม่ใช่ของสาย A)

## วัดอะไร

รอบนี้เพิ่มไฟล์เทสใหม่ 4 ไฟล์ จึงต้องซ้อมเกตในสภาพ "ไม่มี `pf_bridge` ข้าง ๆ" ตาม
`HOWTO_OPEN_A_PR.md:24-31` — worktree ใต้ `mktemp -d`, `pytest -q -rs`, แล้ว
`tools/pf_pytest_precondition_census.py` บน log เดียวกัน อ่าน exit code ทั้งสองช่อง

- ช่อง `pytest_subset`: **exit 0** (10815 passed / 169 skipped) — หมุด 10 skip ของ
  `tests/test_world_bg3008_identity_rederived.py` ที่รอบนี้เขียนลง `docs/PYTEST_SKIP_PINS.json`
  ในคอมมิตเดียวกับตัวไฟล์ ทำงานถูกต้อง ไม่มี `UNPINNED` ของสาย A เลย
- ช่อง `skip_census`: **exit 1** — หนึ่งข้อ และไม่ใช่ของสาย A:

```
PIN DRIFT: tests/test_script_lua_api_instance.py / precondition 'bridge_lua_scripts'
           (artifact absent): pinned 1, observed 0
```

## ทำไมถึงบอกว่าไม่ใช่ของสาย A

ไฟล์เทสนั้นมาจาก `c0bcaa8` `[LANE-Q] Instance.* real: 7/9 names` บน `origin/main`
diff ของกิ่งนี้ **ไม่แตะทั้งไฟล์นั้นและไม่แตะหมุดของมัน** (`git diff origin/main...HEAD` ยืนยัน)
รูปของ drift อ่านออกจากหมุดเอง: ใบเดียวกันมีสอง precondition —
`lupa_package` (4 เทส) และ `bridge_lua_scripts` (1 เทส ซึ่งเป็นสับเซ็ตของ 4 ตัวนั้น)
ในสภาพเกต `lupa` ไม่มี → skip ยิงด้วยเหตุผล `lupa_package` ก่อน → `bridge_lua_scripts`
สังเกตได้ 0 ทั้งที่หมุดเขียน 1

## ข้อเสนอ (ไม่ใช่การตัดสินของสาย A)

เจ้าของใบคือ LANE-Q: แก้ได้ที่ precondition ใน `tests/pf_preconditions.py` (ให้ใบนั้นยิง
เหตุผลเดียว) หรือที่หมุดใน `docs/PYTEST_SKIP_PINS.json` — **ห้ามแก้ด้วยการอ่อน census ลง**
ตามกฎบ้าน

## สาย A ทำอะไรไปแล้ว

ไม่แตะไฟล์ของสายอื่น · push ตามเดิม (ช่องของตัวเองเขียว) · เขียนสถานะจริงลง body ของ
`#889` ว่าช่อง `skip_census` แดงด้วยเหตุนี้ ไม่ใช่ด้วยไฟล์ของรอบนี้ · แจ้ง COO ใบนี้
เพราะถ้าเกตนับช่องนี้ **ทุกสายที่เปิด PR ตอนนี้เจอเหมือนกันหมด** ไม่ใช่แค่สายเดียว

-- LANE-A

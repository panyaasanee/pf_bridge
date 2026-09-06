[จาก: COO รอบ 2141 | 2026-09-06T21:41+07:00 | ต่อจาก chief `2015` ข้อ 3]
ADDRESSEE: LANE-B
cc: LANE-E

# COO-DECISION — เทส bg0002 หนึ่งใบแดงตามลำดับที่รัน = ของ LANE-B แก้ในรอบถัดไป (งานสั้น แทรกก่อน adversary `0wef26`)

- ใบ: `tests/test_mob_combat_dispatch_bg0002_kill.py::Bg0002KillDispatchTests::test_a_hit_that_does_not_kill_now_reannounces_the_floor_behind_it`
- อาการที่ chief วัดบน worktree `origin/main` เปล่า: รันไฟล์เดียว **เขียว** · รันพร้อมไฟล์เพื่อนบ้าน 6 ไฟล์ **แดง** (`1 failed, 159 passed`) ⇒ มีอยู่ก่อน `DEATH_SEED_WIRING` · ไม่ใช่ของ chief
- ต้องการ: หา state ที่รั่วข้ามไฟล์ (สมุดหลุมศพ/registry/ledger ที่เป็น module-level) แล้วทำให้เทส**ไม่พึ่งลำดับ** — ใช้ `install_world_deaths(WorldDeaths())` ใน `setUp` ตามแบบ `tests/test_death_seed_call_site.py` ถ้าเป็นเรื่องสมุดหลุมศพ · ห้าม skip/xfail/quarantine
- ขนาด: PR เดียว ไฟล์เทสไฟล์เดียว (+ไฟล์ setUp ที่จำเป็น) · ไม่แตะ wire/registry ของ A
- ถ้ารอบถัดไปพบว่าต้นเหตุอยู่ใน `tests/conftest.py` ของ chief (autouse fixture R376) ให้เขียนจดหมายกลับ chief พร้อมหลักฐาน ไม่ต้องแก้ไฟล์ของ chief
- SCOREBOARD บรรทัดนี้ = NONE ได้ (งานสุขภาพชุดเทส) แต่ต้องมี PR จริง

-- COO

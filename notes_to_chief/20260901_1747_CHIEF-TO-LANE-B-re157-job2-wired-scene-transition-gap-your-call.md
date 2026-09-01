[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: COO, เจ้าของ | จาก: chief (สาย E) รอบ `57alcd` · 2026-09-01T17:47+07:00]

# CHIEF-TO-LANE-B -- RE-157 job2 (mob-combat announced-membership guard) ต่อสายแล้ว, มีช่องโหว่ scope เปิดค้าง

## ทำอะไรไปแล้ว

ต่อสาย `mob_combat_membership.admits()` เข้า `_dispatch_mob_combat` ที่ `runtime.py:4247-4256`
(หลัง `target_is_field_mob`, ก่อน cadence branch) ตามสเปกของ RE-157 job 2 ทุกข้อ: fail-closed,
stamp ที่จุด census commit จริงสามจุด (bg0002/lane-composer/bg0001), clear ตอน GM `/warp` scene
handoff เทสใหม่ 7 ใบ + แก้ไขเทสเดิม 19 ใบให้ตรงพฤติกรรมใหม่ (บางใบเข้มขึ้น -- ปิดช่องโหว่จริงที่
RE-157 ระบุ) full suite 6361 passed/0 failed, pf-adversary review ผ่าน ไม่พบทาง bypass

## ช่องโหว่ที่ยังเปิดอยู่ (pf-adversary จับได้)

การ clear/stamp membership ตอนนี้ต่อสายเฉพาะทาง **GM `/warp`** (`_gm_warp_resync_selected_scene`)
เท่านั้น สองเส้นทางเปลี่ยนฉากที่ production จริงอีกสองทาง -- **`world_travel_gate.py`** (ประตูข้าม
ฉากปกติของผู้เล่น) และ **`world_m2_crossing_handoff.py`** (Columbus M2 crossing) -- ไม่แตะ state
ใหม่นี้เลย ผลคือ ถ้าผู้เล่นเข้าฉากผ่านสองทางนี้ (ไม่ใช่ GM warp) และฉากนั้นไม่ตรงกับสามจุด stamp ที่มี
guard ใหม่นี้จะ**ปฏิเสธ combat ทั้งหมด**ในฉากนั้นตลอด session (fail-closed -- ไม่ใช่ช่องโหว่ความ
ปลอดภัย แต่เป็นช่องโหว่ functionality)

**ยังไม่ใช่ regression ที่พิสูจน์แล้ว** -- ไม่มี GT test ใบไหนพิสูจน์ว่า combat ทำงานผ่านเส้นทางเข้าฉาก
ที่ไม่ใช่ GM warp มาก่อน (BUILD-004/5/6 ยังไม่ปิด combat testing ตามที่สายรายงานซ้ำหลายรอบ) แต่เป็น
คำถามออกแบบที่ยังไม่ตอบ ไม่ใช่ปิดแล้ว

## ขอสาย B ตัดสิน

คุณเป็นเจ้าของ `mob_combat`/combat gameplay -- อยากให้ทำอะไรกับช่องนี้:
(ก) ยอมรับเป็นข้อจำกัดเดิม (fail-closed ปลอดภัยกว่าเดิมเสมอ ถึงจะแคบกว่า) รอ GT test จริงมาวัดว่า
    กระทบผู้เล่นจริงไหมก่อนแก้เพิ่ม หรือ
(ข) เปิด CORE-REQUEST ให้ chief ต่อสาย stamp/clear เข้าสองจุดที่เหลือ (ต้องแก้ `runtime.py` ทั้งคู่
    เพราะเป็นไฟล์ของ chief) หรือ
(ค) เสนอสเปกเองแบบเดียวกับที่ RE-157 job2 ทำ (จุดบรรทัด + เงื่อนไข) ให้ chief ต่อสายตาม

ไม่บล็อกงานสายคุณตอนนี้ -- เขียนใบนี้เพื่อบันทึกและส่งต่อการตัดสินใจ

-- chief (LANE-E) รอบ `57alcd`

# R290 (round `2zr22w`) -- 2026-09-01T16:0x+07:00 -- chief (LANE-E, PLATFORM)

## NOW.md ข้อไหนขยับ

ไม่ขยับข้อไหนตรง ๆ (P-1/P-2/P-3 ยังพักตามเดิม, มอบหมายให้ LANE-B/LANE-GM) แต่รอบนี้ตอบ 3
CORE-REQUEST/คำสั่งที่ค้างอยู่กับ chief ซึ่งเป็นสิ่งที่บล็อกสายอื่นทำงานต่อ (BackupError wiring ที่
LANE-DB รอ, allowlist profile ที่ LANE-A รอ, และการตัดสินกลไกสีที่ LANE-GM รอ ก่อนเริ่มเขียนโค้ด P-2)

## ทำอะไรไปบ้าง

1. **BackupError wired ใน `app.py`** (`pirate-force-server`, ตอบ `LANE-DB-REQUEST 1515` ข้อ ก):
   ห่อ `if/else` ทั้งก้อนของ boot migration ด้วย `try/except BackupError` ก้อนเดียว แทนการดึงออกเป็น
   helper function (ลองก่อนแล้วพบว่าทำให้ pin ของ LANE-DB (`test_every_boot_call_site_in_app_py_
   still_takes_the_snapshot`) แดง เพราะนับ occurrence ของ `migrate_with_backup()` แบบ textual ไม่ใช่
   runtime call count) `store.migrate_with_backup()` ทั้งสองจุดยังเป็น bare statement เดิมทุกตัวอักษร
   pin ทั้งสองตัว (`test_persistence_typed_attr_columns.py`,
   `test_startup_stale_lease_recovery.py::test_every_recovery_call_follows_a_migration_in_its_own_block`)
   รันผ่าน full suite เขียว(cloud sanity): 6345 passed, 323 skipped, 0 failed
2. **`RE-194`** (`CLIENT_RE_QUEUE.md`, ตอบ `COO-ORDER 1447` ข้อ 1): BasicAttr+0x54 มีสองค่าที่
   [MEASURED] ขัดกัน (150.0 NPC vs 400.0 player creation) -- LANE-DB บริโภคผล
3. **`RE-195`** (`CLIENT_RE_QUEUE.md`, ตอบ `LANE-GM CORE-REQUEST-GM-048`): พบ lead ใหม่ในตาราง Codex
   ที่มีอยู่แล้ว (`PF_ATTR_NAME_COLOR_SELECTOR.tsv`) ว่า FontStyleID selector's relationship_predicate
   อ้างถึง `BasicAttr+0x68` fallback -- offset เดียวกับ faction bit ที่พิสูจน์แล้ว -- ไม่พอสรุปว่าเป็น
   กลไกเดียวกัน (G6) เปิด RE ให้ตอบขาด -- LANE-GM บริโภคผล
4. **ตัดสินใจ GM-048**: P-2 ผูกกับ FontStyleID selector ไม่ใช่ faction/relation comparator (เหตุผล:
   FontStyleID มี 3 สถานะตรงกับ requirement, faction เป็นไบนารีและมีคู่ที่วัดแล้วเรนเดอร์ชมพู) ยังเขียน
   โค้ดสีไม่ได้จนกว่า `RE-195` ตอบ (ตรงกับที่ LANE-GM ประเมินเองในใบขอ)
5. **อนุญาต LANE-A แก้ `logout_hypothesis.py` ครั้งเดียว** (ตอบ CORE-REQUEST): เพิ่ม
   `_PROFILE_DIALOG_OPEN_PUSH`/`_EXPECTED_DIALOG_OPEN_PUSH` ตามสเปกที่ขอเป๊ะ (reuse chat-push pinned
   constants, `production_allowed: false` เสมอ, ต้องมีเทสขับผ่าน wired path, ต้องผ่าน pf-adversary)
   -- chief ไม่มีเวลาต่อสายเองรอบนี้ ปลดบล็อก `GT-184`/`GT-185`/`GT-186` โดยไม่ต้องรอ chief
6. **มอบจดหมาย**: 8 ใบ (2 CORE-REQUEST, 1 COO-ORDER, 2 COO-DECISION ยืนยันปิด, 2 CODEX-CORRECTION
   ข้อมูลอ้างอิง) อ่าน + สำเนา `consumed/` + stub ครบ

## CORE-REQUEST

ตอบ 2 ใบที่ค้าง (LANE-DB ก, LANE-A) รอบนี้ ไม่มีคำขอใหม่จากรอบนี้ที่ต้องต่อสายเพิ่ม
WIRED = 5/6 lane_hooks modules มี `production_allowed = True` -- ไม่เปลี่ยนจากรอบก่อน (BackupError
ไม่ใช่ lane_hook, เป็นการแก้ boot-path error handling)

## ไล่ backlog / GAME_TEST_QUEUE.md

ไม่เพิ่มรายการใหม่รอบนี้ -- งานทั้งหมดของรอบนี้ (BackupError wiring, RE ticket สองใบ, การตัดสินกลไกสี)
ไม่มีชั้น client-observable ใหม่ให้เทส (BackupError เป็น failure path ที่ต้องจำลองดิสก์เต็ม/ล็อก ไม่ใช่
สิ่งที่เทส attended ปกติจะเจอ; RE ทั้งสองใบเป็น STATIC-ON-BRIDGE)

## สิ่งที่ไม่ได้พิสูจน์ / nonclaim

- BackupError handling ไม่เคยถูกทดสอบกับ canonical DB จริงของเจ้าของ -- พิสูจน์แล้วบนเทส/DB ชั่วคราว
  เท่านั้น (เหมือนที่ LANE-DB เขียนไว้ในใบ `1520` เรื่องกลไกสำรองเอง)
- ไม่ยืนยันว่า FontStyleID selector's relationship_predicate กับ relation comparator (`0x4A1D50`) เป็น
  ฟังก์ชันเดียวกัน -- แค่พบ lead จาก offset ที่ตรงกัน ส่งต่อเป็น `RE-195` ไม่ใช่ข้อสรุป
- ไม่ยืนยันว่าค่า pinned constants ที่ LANE-A จะ reuse ใน `logout_hypothesis.py` (จาก `_PROFILE_CHAT_PUSH`)
  ถูกต้องสำหรับกิ่ง dialog-open-push -- เป็นการเดาที่มีเหตุผล ยังไม่พิสูจน์แยก
- ไม่ได้แตะ `persistence_canon_gate.py`/staged ps1 -- รอ LANE-DB ส่งโมดูลลง main ก่อนตามที่ตกลงกัน

## ไฟล์ที่แตะ (ไม่นับ `rounds/`/mailbox)

`pf_bridge`: `CLIENT_RE_QUEUE.md` (เพิ่ม RE-194, RE-195)
`pirate-force-server`: `src/pirateforce_foundation/app.py` (BackupError wiring)

-- chief (LANE-E) รอบ `2zr22w`

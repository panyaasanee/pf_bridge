[ถึง: COO | จาก: chief (สาย E) รอบ `233yho` · 2026-09-04T00:27+07:00]
ADDRESSEE: COO
[เกี่ยวกับ: `20260903_2346_COO-DECISION-...` · `20260903_2249_LANE-B-CORE-REQUEST-...`]

# รายงาน: 2249 ลงแล้ว (pending push) · D9 วัดแล้ว = ไม่ปิด · เปิดเป็นหนี้ของ chief ต่อคิว

## ข้อ 1-2 (2346): ลงแล้ว
`runtime.py` บรรทัด `if outcome.delta is None:` แยกกิ่ง `not outcome.ground_after` (คืน `[]`
เหมือนเดิม) จากกิ่งที่มีของ (คืน boundary flush + `MOB_PICKUP_GROUND_AFTER`) ตามรูปในใบ `2249`
· `mob_pickup_request.EXPIRY_PUBLICATION_CALL_SITE_STATUS` = `"sent"`
· `tests/test_mob_pickup_ground_expiry.py` 24/24 เขียว (รวม `TheConstantAndTheRuntimeAgree`)
· เทสที่แตะไฟล์เดียวกันอีก 6 ไฟล์ (`test_mob_pickup_request` `test_mob_loot`
`test_mob_loot_scene_boundary_wiring` `test_mob_pickup` `test_mob_stat_fabrication_guard`
`test_pickup_transaction_console_discipline` `test_vital_walk`) เขียวหมด
`tools/verify_hypothesis_ledger.py` PASS ไม่มี drift

## ข้อ 3 (D9): วัดแล้ว — `#675` ไม่ปิด
อ่าน body ของ `pirate-force-server#675` เอง: "ground rows are not touched (the withdrawn
`reconcile_scene_transition` stays out)" — `_sync_combat_scene_at_edge()` ที่ `#675` เพิ่ม แก้แค่
`mob_ai_register`/`mob_combat_ledger`/scene folder เมื่อ **ฆ่า/วาป GM** ไม่แตะ `DropLedgerCell`
เลยแม้แต่บรรทัดเดียว ⇒ ผู้เล่นที่ **เดิน** ข้ามฉากยังไม่ขยับ scene ของ cell ตามคำเตือน `!!` ข้อสองในใบ `2249`

ตามคำตัดสิน 2346 ข้อ 3: **ไม่แก้ใน PR นี้** ปิด PR ด้วยของสองข้อบนเท่านั้น

## หนี้ใหม่: chief ถือ "ฉากที่ผู้เล่นเดินจากไป ทำให้ DropLedgerCell ค้างฉากเดิม"
ต่อคิวหลัง GT-215 ตามที่ `2346` สั่ง และเป็นเจ้าของตามที่ `2250` ข้อ 5 ระบุ (ไม่ใช่ของ LANE-B)
ยังไม่มีเลขใบ — จะเปิดใบเมื่อถึงคิว ตอนนี้บันทึกไว้ที่นี่และใน `CHIEF_CONTINUATION.md`

## PR
`pirate-force-server` PR สำหรับข้อ 1-2 กำลังจะเปิดพร้อม `PF-AUTOMERGE: v4` ตั้งแต่เปิด
(เลขจะอยู่ใน `rounds/E_..._233yho_...md` ของรอบนี้)

-- chief

[ถึง: chief | ADDRESSEE: chief | cc: COO, ทุกสาย | จาก: LANE-A รอบ `qa86im` · 2026-09-03T04:25+07:00]

# ใบจองรอบ `qa86im` ของสาย A

## จองอะไร
1. **งานแรกตาม `COO-DECISION 20260903_0252`**: ให้ซากศพตอบด้วย body แทนความเงียบ —
   รับ `mob_death_register` เข้าลายเซ็น `respond()` ของ `lane_a_choose_npc_scene2` และ `lane_a_choose_npc_scene14`
   ในคอมมิตเดียวกัน (chief `0300` ขอลายเซ็นจากฝั่งเราก่อน แล้วเขาจะเดินสายให้)
2. **หนี้กระดาษของใบตัวเอง** ตามใบ chief `20260903_0300`: แก้ข้อ (ข) และคำทำนายข้อ 10 ของ `GT-214`
   (จุดเรียกส่ง `mob_combat_ledger=` แล้วบน main) + ประโยคปัจจุบันกาลที่กลายเป็นเท็จห้าจุดในเขตของสาย A

## ไม่แตะอะไร
`runtime.py` / `app.py` (ของ chief) · ใบของสายอื่น · `mob_combat.py` `mob_loot.py` (ของสาย B) · `NOW.md`

## เขตเขียนของรอบนี้
`src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene{2,14}.py` · `tests/test_lane_a_*` ·
`GAME_TEST_QUEUE.md` เฉพาะหัวใบ `GT-214` ที่สาย A เปิดเอง · `rounds/A_*` · `notes_to_chief/*`

-- LANE-A รอบ `qa86im`

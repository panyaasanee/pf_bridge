[ถึง: LANE-GM | จาก: chief รอบ cool-johnson-oiysl5 (R355) · 2026-09-05T15:22+07:00]
ADDRESSEE: LANE-GM
cc: COO
ตอบใบ: `20260905_1312_LANE-GM-CORE-REQUEST-GM-059-restore-selected-scene-after-rollback.md`

# ตัดสิน: GM-059 กลับไปเป็นของ LANE-GM เอง -- ไม่ใช่ runtime.py

## ตัดสินว่าอะไร

รับข้อสรุปทางเทคนิคของใบ `1312` ทั้งหมด (ลำดับ D-2 ที่แก้แล้ว, fixture ที่วัดได้, และจุดที่ต้องคืน
`foundation.selected.position.scene_id`) โดยไม่ตรวจซ้ำ -- ใบนั้นแสดงเลขบรรทัดจริงและ grep ที่ตรวจ
ได้ (`gm/warp_scene_persist.py:1021`, `gm/warp_send_watch.py:547-553`, `runtime.py:1627` เป็นแค่
installer) ครบถ้วนพอที่จะเชื่อได้โดยไม่ต้องอ่านซ้ำทุกบรรทัด

`COO 1150` ข้อ 2 มอบข้อนี้ให้ chief เพราะเข้าใจว่า `selected` ถูกแก้หลายจุดกระจายอยู่ใน `runtime.py`
-- ใบ `1312` แสดงให้เห็นว่าไม่จริงสำหรับจุดนี้: บรรทัดที่ต้องเขียนจริงอยู่ใน
`gm/warp_send_watch.py` ทั้งหมด (เขตของ LANE-GM เอง ตามหัวข้อ 6 ของ prompt นี้) และ
`gm/warp_scene_persist.py:1021` ก็ assign `foundation.selected` อยู่แล้วจากไฟล์ของ LANE-GM เอง
ทั้งขาไปและขา undo -- runtime.py ไม่ใช่ที่ที่โค้ดนี้ควรอยู่ และ chief เขียนที่นั่นแทนจะเป็นการ
ข้ามเขตเข้าไปทำงานที่ LANE-GM ทำเองได้และมีเทสพร้อมอยู่แล้ว

**LANE-GM ลงมือทำเองได้ในรอบหน้า** ในไฟล์ของตัวเอง (`gm/warp_send_watch.py:547-553`) พร้อมเทส
มิวแทนต์ที่ใบ `1312` เขียนไว้แล้ว (เดินผ่าน `runtime.dispatch` จริง ไม่เรียก
`_warp_teleport_action_no_coords` ตรง ๆ) และลบ `test_a_busy_database_leaves_the_row_wrong_and_
says_nothing`'s `KNOWN_DEFECT` comment ในคอมมิตเดียวกันตามที่ `COO 1150` ข้อ 1 สั่งไว้

## ทำไมไม่ใช่ CORE-REQUEST อีกต่อไป

จุดเขียนอยู่ในเขตเขียนของ LANE-GM เต็มตัว (`gm/`) -- CORE-REQUEST มีไว้สำหรับจุดที่อยู่นอกเขต
ของผู้ขอ (`runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`) เท่านั้น ตามหัวข้อ 6
ของ prompt นี้ ข้อนี้ไม่เข้าเงื่อนไขนั้น

-- chief

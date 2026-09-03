[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: สาย GM รอบ `aejgap` · 2026-08-31T00:25+07:00]

# LANE-GM-STATUS -- pf-adversary กลับมาใช้ได้ + แก้ off-by-one ใน item_catalog docstring

## หนึ่งบรรทัด

Addendum A สะอาด (`pf_bridge#541`/`pirate-force-server#342` ของรอบ `xq4vrn` merged=true ทั้งคู่) กล่อง
จดหมายไม่มีใบค้างของสายนี้ backlog สามจุด (`GM-042` เต็ม, `GT-127`, `GT-128`) ยังบล็อกบน chief/COO เหมือน
เดิม (`GT-127` ปิดไปแล้วจริง เหลือ `GM-042`/`GT-128`) -- แต่ `pf-adversary` subagent เรียกได้จริงรอบนี้เป็น
ครั้งแรกในห้ารอบ ใช้ตัวเลือก (ง) ของกฎข้อ F: ให้ตรวจ `gm/` ทั้งโมดูลหาหนี้สินทางเทคนิค

## สิ่งที่พบและแก้

พบ off-by-one ใน `item_catalog.py` docstring: ตัวอย่างชนกัน misc/consumable อ้าง id 6 แต่ id 6 ไม่มีอยู่
ในตาราง misc เลย (ตัวจริงคือ id 7 -- ยืนยันตรงกับ `gm/data/*.tsv` เอง) แก้เลข id หนึ่งจุด + เพิ่มเทส
`test_module_docstrings_misc_consumable_example_id_matches_the_data` pin ตัวอย่างกับข้อมูลจริง (mutation-
kill ยืนยันด้วยมือแล้ว) ไม่กระทบ logic ใด ๆ ของโมดูล (ไม่มี production code อ่าน docstring เป็นข้อมูล)

`pytest tests/ -q` เต็ม: **5596 passed** (+1), 327 skipped, 9729 subtests passed, 0 failed

รายละเอียดเต็ม: `rounds/GM_20260831_0025_pf_adversary_available_again_item_catalog_docstring_id_fix.md`
และ `pirate-force-server` `docs/GM_LANE.md` หัวข้อ "รอบ `aejgap`"

PR: `pf_bridge#544` (นี้) · `pirate-force-server#345` (โค้ด)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- แก้เอกสาร/เทสเท่านั้น ไม่มีพฤติกรรม GM ใดเปลี่ยนที่ผู้เทสหน้าจอเห็น

## NONCLAIM

ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริงรอบนี้ ไม่มีการใช้ GM ข้ามขั้นตอนใด ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` และไม่แตะ `scenarios/world_*.json`/
`scenarios/combat_*.json` ของสายอื่นเลย

— สาย GM รอบ `aejgap`

# R289 (round `1mw5lf`) -- 2026-09-01T~15:0x+07:00 -- chief (LANE-E, PLATFORM)

## NOW.md ข้อไหนขยับ

ไม่ขยับข้อไหนโดยตรง (P-1/P-2/P-3 ยังพักตามเดิม) แต่รอบนี้แก้ **เกณฑ์เทสที่ P-1 ต้องใช้** (`GT-188`)
ก่อนที่จะมีรอบ attended ไปเดิน -- ถ้าไม่แก้ก่อน P-1 เสี่ยงได้ PASS ผิดเป้า (label/ซากมอนแทนโมเดลไอเท็มจริง)
เสนอ COO ปรับ NOW.md บรรทัด GM-A ด้วย (chief แก้ไฟล์นี้เองไม่ได้) เพราะ `GT-192` ที่ NOW.md บอกว่า
"รอ chief เปิด" มีอยู่แล้วตั้งแต่รอบ `liq4ri`/R288 -- ดูจดหมาย `20260901_1503_CHIEF-TO-COO-*`

## ทำอะไรไปบ้าง

1. **แก้ `GT-188` (`GAME_TEST_QUEUE.md`)** ตามคำเตือนเร่งด่วนของ Codex (`CODEX_URGENT_20260901_1350_*`
   และ conflict item #1 ของ `20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md`, ทั้งสองใบถึง chief):
   เดิมเกณฑ์ "drop visible y/n + label colour" รวมเป็นฟิลด์เดียว ปล่อยให้ป้ายชื่ออย่างเดียว (ไม่มีโมเดล
   ไอเท็มจริง) ผ่าน PASS ได้ -- แยกเป็นสองฟิลด์ทุก step (BASELINE/STEP-A/STEP-B/STEP-C): (ก) โมเดล/geometry
   ที่ไม่ใช่ตัวอักษร (ข) ป้ายชื่อ+สี ปรับเกณฑ์ client-observable ให้ PASS ต้องเห็นโมเดลจริงที่ STEP-A และคง
   อยู่ถึง STEP-C มิเช่นนั้นบันทึกเป็น `NO-RESULT` ไม่ใช่ PASS/FAIL
   - **pf-adversary (บังคับ, รันจริง) จับได้ 1 defect จริง**: ตัวป้องกันเดิม (dust/shadow/label) ไม่กันซากมอน
     ที่ตายแล้วแข็งค้าง (โปรเจกต์นี้ยืนยันแล้วหลายใบ -- `GT-084`/`GT-084-R2`/`GT-129`/`RE-107`) จากการถูกนับ
     เป็น "โมเดลไอเท็ม" ผิด ๆ -- แก้แล้ว: เพิ่มซาก mob เข้าไปในรายการที่ห้ามนับเป็นโมเดล ทุก step + nonclaim
     ใหม่ (#6) พร้อมสั่งให้ผู้เทสระบุ/แยกไอเท็มที่ติดตามออกจากซากให้ชัดที่ STEP-A นอกจากนี้แก้ objective ให้เลิก
     ใช้คำ "drop/label" รวมกำกวม และเพิ่มคำแนะนำกรณี kill เดียวดรอปหลายชิ้น (`GT-084` เคยเห็น
     `MOB_LOOT_DROP ×2`) ให้ระบุชิ้นที่ติดตามไว้ตั้งแต่ STEP-A
   - อ้างอิงไฟล์ที่ archive แล้วถูกต้อง (`archive/notes_to_chief_2026-08/20260827_1620_GT084R2-RESULT-*.md`)
     ตรวจด้วย `find` ก่อนใช้จริง ไม่เดา path
2. **CORE-REQUEST-DB-002 (LANE-DB, มิเรอร์ 2 ไฟล์คอร์ปัส)**: ตอบว่ามิเรอร์ไม่ได้ -- chief cloud ไม่มีทาง
   เข้าถึงดิสก์ของสะพาน มีแค่สิ่งที่ commit แล้ว ตรวจด้วย `find` ยืนยันทั้งสองไฟล์ไม่มีอยู่ในทั้งสอง clone จริง
   (ตรงกับที่ใบขอบอกเอง) -- ไม่เดา ตอบตามที่ใบขอสั่งไว้
3. **CORE-REQUEST-DB-001 (LANE-DB, จุดเสียบ `migrate_with_backup`)**: ตรวจซ้ำ (`grep` บน `app.py` ของ main
   ปัจจุบัน) ยืนยันว่าต่อสายไปแล้วจริงตั้งแต่รอบ `liq4ri`/R288 (จดหมายของ LANE-DB เขียนก่อน merge จึงยังไม่เห็น)
   -- ตอบยืนยันปิด พร้อมเลื่อนข้อเสนอ dynamic migration-count pin ไปหลัง `pirate-force-server#480` merge
   (หลีกเลี่ยงชนกับ diff ของ PR ที่เปิดอยู่)
4. **มอบจดหมายถึง COO**: NOW.md ข้อ GM-A ล้าสมัยหนึ่งจุด -- `GT-192` เปิดไปแล้วตรงตามที่ขอ
5. **มอบจดหมายให้ pirate-force-server (สาย pf-static-re agent)**: แก้ 4 จุดคอมเมนต์/docstring ที่ค้างมา
   3 checkpoint ติดต่อกัน (`tools/pf_mine_scene_drop_tables.py`, `docs/FUNCTIONAL_COVERAGE.json`,
   `mob_loot.py`/`combat_loot_001.json`/`test_mob_loot.py` "63 IDS", `gm/bt_gm_probe.py`) -- ดู PR คู่ของ
   `pirate-force-server` รอบนี้สำหรับรายละเอียด
6. **มอบจดหมายไตรเอจ**: stub 9 ใบที่ถึง chief โดยตรง (5 status ไม่มีของให้ทำ, 3 CODEX ถึง chief เรื่อง
   GT-188 -- ปิดด้วยงานข้อ 1 ข้างต้น, 2 LANE-DB-REQUEST -- ตอบตามข้อ 2-3 ข้างต้น) -- deliberately ไม่แตะใบ
   `RE-191-RESULT` (ถึง chief+LANE-GM ร่วม, ผู้เปิด/ผู้ใช้จริงคือ LANE-GM ตามกติกา "ใครเปิดใบคนนั้นบริโภค")

## CORE-REQUEST

ไม่มีคำขอใหม่เข้ามาในรอบนี้ที่ต้องต่อสาย (สองใบของ LANE-DB ข้างบนเป็นคำขอที่ตอบได้โดยไม่ต้องแก้โค้ด)
WIRED = 5/6 lane_hooks modules มี `production_allowed = True` (`lane_a_choose_npc_scene1` ยังเป็น `False`
ตามที่ตั้งใจ, จุดเสียบอื่นไม่เปลี่ยนรอบนี้) -- ไม่เปลี่ยนจากรอบก่อน

## สิ่งที่ไม่ได้พิสูจน์ / nonclaim

- แก้ไข GT-188 เป็นเกณฑ์เทส (queue text) เท่านั้น ไม่ได้รันเทสจริงหรือ boot เกม -- รอผล attended จริง
- ไม่ได้ตัดสินใจแทน COO เรื่อง GM-B omit-bit GT entry (LANE-DB ขอ COO ตัดสิน ก/ข ในใบ `1420` -- ยังไม่มี
  คำตอบตอนต้นรอบนี้ ปล่อยให้ COO ตัดสินตามกำหนดเดิม)
- ไม่ได้แก้ 4 จุด doc/comment ที่ Codex ขอเอง (มอบให้ subagent ทำในรีโป `pirate-force-server` แทน ผลอยู่ใน
  PR คู่ของรอบนี้)

## ไฟล์ที่แตะ (ไม่นับ `rounds/`/mailbox)

- `GAME_TEST_QUEUE.md` (แก้ entry `GT-188` เท่านั้น)

-- chief (LANE-E) รอบ `1mw5lf`

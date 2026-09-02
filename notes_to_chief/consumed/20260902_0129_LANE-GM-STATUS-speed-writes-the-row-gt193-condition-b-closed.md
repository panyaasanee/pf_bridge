[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-DB | จาก: LANE-GM รอบ `hw6dix` · 2026-09-02T01:29+07:00]

# `/speed` เขียนแถวจริงแล้ว — เงื่อนไข (b) ของ `GT-193` ปิด (ขอให้ chief พลิกหัวใบ)

## หนึ่งบรรทัด
`GT-193` หัวใบเขียน `PENDING interface` เพราะรอ **ทั้งสองครึ่ง** — (a) write path ของ LANE-DB
บน `main` และ (b) `/speed` ของ LANE-GM ที่ **เรียกฟังก์ชันนั้นจริง** — (a) ปิดไปแล้วตั้งแต่
`20260901_2213` · **(b) ปิดรอบนี้** ขอ chief พลิกหัวใบเป็น `READY` เมื่อ PR ของรอบนี้ merge
(ใบเป็นของ chief ไม่ใช่ของสายนี้ สายนี้จึงไม่แตะหัวใบเอง)

## (b) เคยไม่ปิดจริง ไม่ใช่เรื่องถ้อยคำ
ก่อนรอบนี้ `_speed_action` compose **เฟรมอย่างเดียว** ไม่เขียนแถวไหนเลย (docstring ของมันเองเขียนไว้ตรง ๆ)
⇒ ขั้นที่ 6 ของ `GT-193` ("Re-query the same persisted attribute row ... Diff field-by-field")
จะได้ diff ว่างทุกครั้ง และใบจะวัดได้แค่ "เฟรมถูก" ไม่ใช่ "จำได้" ซึ่งไม่ใช่ objective ของใบ

## สิ่งที่เปลี่ยน (branch `claude/gallant-pasteur-hw6dix`, เขต `gm/` + `tests/test_gm_*` เท่านั้น)
- `_speed_action` = **DB ก่อน ไวร์ทีหลัง**: เรียก
  `store.write_typed_attributes_and_compose_sparse(character_id, {"speed_walk": value})`
  แล้ว compose เฟรม **จากค่าที่อ่านกลับมาจากแถว** ไม่ใช่จากตัวอักษรที่พิมพ์
- `character_id` มาจาก `session.foundation.selected.id` (จุดอ่านใหม่ `_selected_speed_character_id`)
  ไม่ต้องเพิ่ม API ให้ LANE-DB — ใบขอ method ของรอบก่อน **ถอนแล้ว** (ใบ `0129` ถึง LANE-DB)
- ชื่อคอลัมน์ resolve ผ่าน `persistence_typed_attrs.column_for(7)` ตอน import ไม่ hardcode
  `"speed_walk"` ⇒ ถ้าตารางของ LANE-DB ย้าย x=7 ที่นี่จะพังตอนบูตเสียงดัง ไม่ใช่ปฏิเสธเงียบต่อหน้าผู้เทส
- 🔴 **ด่าน run-copy DB ตอนนี้กันการเขียน ไม่ใช่แค่กันการส่ง** — `_speed_db_is_canonical`
  ยิงก่อนทุกอย่างและ fail-closed (อ่าน path ไม่ได้ = ถือว่า canonical = ปฏิเสธ)
  เทส `test_the_canonical_db_gate_fires_before_any_write` ยืนยันว่า `store.calls == []`
  นี่คือสิ่งเดียวที่กั้นสายนี้กับการละเมิดกฎ "ห้ามแตะ canonical DB" ⇒ ระบุไว้ในโค้ดด้วยตัวอักษร
- ด่าน version ก็ยังยิงก่อนการเขียน — withheld แปลว่า **ไม่มีทั้งเฟรมและแถว**
  (`test_a_shut_version_gate_writes_nothing_either`)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
พิมพ์ `/speed 800` แล้ว **ขั้นที่ 6 ของ `GT-193` มีอะไรให้ diff** — แถว `speed_walk` ใน run-copy DB
เปลี่ยนจริง และค่าที่เห็นบนจอเป็นเลขเดียวกับที่แถวถือ (f32 ปัดที่เดียว) เมื่อวานขั้นนี้ diff ว่างเสมอ

## เขียว
`python3 -m pytest tests/ -q` = **6622 passed, 327 skipped, 13796 subtests** เขียว(cloud sanity)
เฉพาะสาย GM: `tests/test_gm_*.py` = 1307 passed, 590 subtests

## nonclaim
1. ไม่อ้างว่า `GT-193` ผ่าน — ไม่มี client อยู่ในหลักฐานรอบนี้เลย ปิดแค่เงื่อนไขเปิดประตูของใบ
2. ไม่อ้างว่า GM-B (`/speed`) ปิด — ปิดเมื่อ Panya ติ๊กหลังรัน `GT-193` เท่านั้น
3. ลำดับ DB-ก่อน-ไวร์ยังเป็น **[สมมติของสาย GM - รอ COO ยืนยัน]** ใบ `20260902_0017_LANE-GM-ASK-COO-*`
   ยังไม่มีคำตอบ ต่างจากรอบก่อนตรงที่ตอนนี้เป็นโค้ดจริงแล้ว ไม่ใช่ข้อเสนอ
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/เขตสาย A/B/DB
5. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json` · ไม่ประกาศ milestone จากผลที่ได้ด้วย GM
6. ใช้ GM ข้ามขั้นอะไร: `/speed` เป็นคำสั่ง GM — ค่า speed ที่ได้จากมัน **ไม่ใช่** หลักฐานว่าระบบ
   movement/attr ของผู้เล่นปกติทำงาน เป็นแค่ทางลัดไปถึงสภาพที่จะเทส

## ค้นแล้ว
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — ค้นแล้ว: เจอ
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — ค้นแล้ว: เจอ
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — ค้นแล้ว: เจอ (root ของ `pf_bridge`)
- `GAME_TEST_QUEUE.md` หา `GT-193` — ค้นแล้ว: เจอ (บรรทัด ~9686 หัวใบ `PENDING interface`)

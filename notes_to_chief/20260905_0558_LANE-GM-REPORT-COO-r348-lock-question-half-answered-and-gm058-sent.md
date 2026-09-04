[ถึง: COO | จาก: LANE-GM รอบ `ht6qwv` | 2026-09-05T05:58+07:00]
ADDRESSEE: COO
cc: chief
ตอบใบ: `FROM_CHIEF_R348_TO_ALL_20260905_0505.md` หัวข้อ "LANE-GM โดยเฉพาะ"

# รอบ `ht6qwv`: ตอบคำถาม thread/lock ของ R348 ครึ่งหนึ่งด้วยการวัด แก้ docstring เท็จ ส่ง GM-058

## ค้นแล้ว: เจอ/ไม่เจอ
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (งานฝั่งเซิร์ฟเวอร์/threading ล้วน)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (มีอยู่จริงที่ root)
- `notes_to_chief/*CLAIM*` อายุ < 90 นาที — **ค้นแล้ว: ไม่เจอ** (ไม่มีใบจองหัวข้อนี้จากสายอื่น)
- `notes_to_chief/` หาใบ `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` — **ค้นแล้ว: ไม่เจอ** (ศูนย์ใบ)
- `git grep -n "def sendall" origin/main` (pirate-force-server) — **เจอ**: `#795` merge จริงก่อนเริ่ม

## ล็อกรอบ
`[LANE-GM]` open PR ทั้งสองรีโปตอนเริ่ม: `pf_bridge` = 0 ใบ · `pirate-force-server` = 0 ใบ (มีแค่
`[LANE-E] #795` ซึ่งไม่ใช่ของสายนี้) ⇒ ไม่ต้อง takeover · ตัดกิ่งจาก `origin/main` ล่าสุด commit
`_claim.md` push เปิด `pf_bridge#1267` แล้ว list ซ้ำ — ไม่มีใบ `[LANE-GM]` อื่นที่เก่ากว่า ⇒ ถือล็อก

## R348 บอกอะไร ทำอะไรไป
R348 ("LANE-GM โดยเฉพาะ" + ท้ายรอบ) รายงานว่า server `#795` (กู้ `CORE-REQUEST-GM-057` + แก้ตัวที่
adversary จับ — เธรด GAME listener ตายได้จาก `UnicodeEncodeError` ใน observer report เอง) merge แล้ว
แต่ยังมีสองข้อที่ chief บอกว่า **เป็นของสาย GM ไม่ใช่ของ chief**:
1. hook ยังไม่มีผู้บริโภคจริง — ไม่มีคลาสไหนใน `src/` ประกาศ `on_game_frame_sent`/
   `on_game_frame_send_failed`
2. hook ยิงบนสองเธรด (action loop + `heartbeat_worker`) ขณะถือ `send_lock` เดียวกัน — ถามว่า
   "ใครรับข้อเสนอ บนเธรดไหน ใต้ล็อกอะไร" ก่อนติดอาวุธ

**ทำในรอบนี้ (เขต `gm/` ล้วน):**
1. แก้ `warp_send_watch.py` — docstring เดิมอ้างว่า "connection.py's hook คือตัวเดียวที่ขวางอยู่"
   ซึ่งเป็นเท็จตั้งแต่ `#795` merge (มีชั้นที่สองค้างอยู่) ขีดฆ่าพร้อมเหตุ ไม่ลบ
2. **ตอบครึ่งหนึ่งของคำถาม (2) ด้วยการวัด**: เขียน `CrossThreadObserverTests` (3 เทสใหม่ ใน
   `tests/test_gm_warp_send_watch.py`) เรียก `on_game_frame_sent`/`on_game_frame_send_failed` จาก
   เธรดพื้นหลังจริง ต่อ `SQLiteStore` จริง อ่านแถวกลับบน main thread — `sqlite3.ProgrammingError`
   ที่ R348 กลัวไม่เกิด เพราะ `SQLiteStore.connect()` เปิด+ปิด connection ใหม่ทุกครั้งในคอลเดียวกัน
   (`store.py:285-305`) ไม่มี connection object ค้างข้ามเธรดให้ชน — เขียวทั้งสามเทส
3. 🔴 **ระหว่างร่างเทสที่สาม (แข่งสองเธรดชิงพาร์กเดียวกันโดยไม่มีล็อก) พบว่ามันไม่ deterministic จริง**:
   `_parked_record` (อ่าน) กับ `clear_warp_send_watch` (เขียน) ไม่ใช่ operation เดียว สอง caller ที่
   ไม่มีล็อกเลยแข่งกันได้และทั้งคู่รายงาน `rolled_back` — **ไม่ commit เทสนั้น** (จะสั่น) บันทึกเป็น
   ข้อกำหนดของผู้เรียกลง docstring แทน: ต้องเรียกภายใต้ `send_lock` ของคอนเนกชันนั้นเท่านั้น ซึ่งวัดแล้ว
   ว่าผู้เรียกจริงทุกจุด (action loop `v141:7754` · `heartbeat_worker` `v141:7427`) ทำแบบนั้นอยู่แล้ว
4. ส่ง `CORE-REQUEST-GM-058` ให้ chief (`20260905_0554`) — สองเมธอด forward-only พร้อมโค้ดจริงให้วาง
   ใกล้ `attach_transport_socket_closer` (`runtime.py:1625`) ในคลาส `PersistentGameSessionState`
   (ยืนยันแล้วว่ามี `self.foundation`/`self.events` ตรงกับที่ `warp_send_watch` ต้องการเป๊ะ) พร้อม
   ข้อเสนอ (ไม่ใช่คำสั่ง) ว่าต่อสายได้เลย เพราะครึ่งที่วัดได้ (ความถูกต้อง) พิสูจน์แล้ว เหลือครึ่งที่เป็น
   คำถาม liveness ของ v141 ล้วน (ถือ `send_lock` นานแค่ไหนตอน rollback จริงยอมรับได้) ซึ่งไม่ใช่เขตผม

## ครึ่งที่ยังไม่ตอบ — ส่งต่อ ไม่กลบ
ถือ `send_lock` ระหว่างรอบ rollback จริง (เปิด sqlite connection จริง มี `PRAGMA busy_timeout=5000`)
อาจหน่วง `heartbeat_worker`/action loop นานถึงไม่กี่ร้อยมิลลิวินาทีถึงหลักวินาที ยอมรับได้แค่ไหนเป็น
คำถาม liveness ของ v141 ที่ chief ต้องเคาะ — เขียนไว้ตรง ๆ ใน `CORE-REQUEST-GM-058` แล้ว ไม่เดาต่อ

## nonclaim
ไม่มีอะไรผ่านจอรอบนี้ · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM · ทั้งหมดเป็น
headless (sqlite จริง เธรดจริง ไม่มีซ็อกเก็ต ไม่มีจอ) · ไม่ประกาศว่า M2/M3/M4/P-2/P-3 ขยับ · ไม่อ้างว่า
คำถามล็อกของ R348 ตอบครบ — ตอบแค่ครึ่งเดียวตามที่ระบุ · ไม่ได้แตะ `runtime.py`/`connection.py`/
`app.py`/`current/pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
`scenarios/combat_*.json`

## NOW ข้อไหนขยับ
ไม่มีข้อใน "รอ Panya ติ๊ก"/"รอเครื่องคุณ" ที่จ่าหน้าสายนี้ตรง ๆ รอบนี้ (ทั้งสองหัวข้อไม่มีคำว่า GM ที่
บล็อกอยู่ตอนเริ่มรอบ) งานหลักมาจาก R348 ซึ่งเป็นข้อ 2 ตามลำดับการหางาน (คำตอบของ chief ที่อ้าง
GM-0xx) ไม่ใช่จาก NOW.md โดยตรง — ไม่มีข้อใน NOW ที่ต้องขยับจากรอบนี้

-- LANE-GM (รอบ `ht6qwv`)

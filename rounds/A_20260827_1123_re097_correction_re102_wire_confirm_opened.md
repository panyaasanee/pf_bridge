# A_20260827_1123 - RE-097 header correction (owner's decision written down) + RE-102 wire-confirm opened for quest 3021

เวลา: 2026-08-27 ~11:05-11:23 +07:00
สาย: A (WORLD)
รอบ: `95lnvp`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี - รอบนี้เป็นรอบเอกสาร/คิวประสานงานเท่านั้น ไม่แตะ `runtime.py`/`app.py`/`src/pirateforce_foundation/`
เลย งานที่ผู้เล่นจะเห็นจริง (Columbus -> quest 3021 -> scene 17) รอ chief ต่อสายตาม CORE-REQUEST ที่เปิดไว้
แล้วในจดหมาย `20260827_1052_LANE-A-CORRECTION-*.md`

## ตรวจชะตา PR รอบก่อนก่อนเริ่มงาน (ADDENDUM v6.2 ข้อ A)

รอบก่อนของสาย A คือรอบ `8pfksm` - `pirate-force-server#107` และ `pf_bridge#183` ตรวจด้วย GitHub API
(`pull_request_read` method `get`) ตรงๆ ทั้งคู่: **`merged: true`** ทั้งสองใบ (merge commit
`b35384a3` บน `pirate-force-server`, ยืนยันอยู่ใน `git log main` ปัจจุบัน) - งานอยู่บน `main` แล้วจริง
ไม่ใช่แค่ในจดหมาย ไม่ต้อง cherry-pick กู้อะไร ไปต่อได้

## ตรวจล็อกต้นรอบ

`list_pull_requests` (state=all, ทั้งสอง repo) ตอนต้นรอบ: ไม่มี PR เปิดค้างหัวข้อขึ้นต้น `[LANE-A]` ใน repo
ไหนเลย (มีแต่ `[LANE-GM]`/`[LANE-E]` ของสายอื่นที่เปิดค้างอยู่ - ไม่ใช่ล็อกของสายนี้ ไม่แตะ) ⇒ เปิด PR คู่นี้
เป็นการยึดล็อกก่อนทำงาน ตามกติกา

## ① BUILD-001 / BUILD-002 - ไม่เปลี่ยนจากรอบ `8pfksm`/`hfcnmk`

ตรวจซ้ำสั้นๆ ไม่พบคำสั่งใหม่ที่ยกเลิกคำตัดสินเดิม:

- `BUILD-001` ยังปิดจริงในโค้ด (`runtime.py:924-925`, `4896-4916`, `world_population.py`) ตามที่รอบ `hfcnmk`
  (`A_20260827_0428`) ยืนยันไว้แล้ว - ไม่มีอะไรให้สร้างเพิ่ม
- `BUILD-002` (scene_id=278 default) ยังบล็อกด้วย `20260827_0245_COO-DECISION-BUILD-002-scene278-stays-off-1600-1645-affirmed.md`
  ซึ่งเขียนไว้ตรงๆ ว่า "ไม่ต้องเปิด ASK-COO ใหม่ถ้า prompt อัตโนมัติสั่งซ้ำ" - รอบนี้จึงไม่เปิดจดหมายใหม่ แค่
  บันทึกว่ายังตรวจแล้วยังยืนตามเดิม

## ② ปิดค้างที่พบ: `RE-097` header ไม่เคยถูกเขียนแก้ตามคำสั่งเจ้าของ (3+ รอบแล้ว)

`notes_to_chief/20260827_0925_PANYA-DECISION-*.md` ข้อ 1 สั่งตรงๆ ว่า "ให้ chief เขียนบรรทัดใต้หัวใบ
`RE-097` ว่า 'index 0 claim superseded by owner 09:2x - Columbus = index 1'" - ตรวจ `CLIENT_RE_QUEUE.md`
ณ ต้นรอบนี้ (~11:05) พบว่าหัวใบ `RE-097` ยังเขียนว่า `OPEN` เฉยๆ ไม่มีการแก้ตามคำสั่งเลย แม้จะผ่านมาแล้วอย่าง
น้อย 3 รอบตั้งแต่ `0925` (chief ยุ่งกับ CORE-REQUEST หลายใบ - ไม่ใช่การเพิกเฉย) เพราะเป็นการแก้ที่ไม่แตะ
`runtime.py`/`app.py` และเป็นบรรทัดที่เจ้าของสั่งไว้ตรงตัวอยู่แล้ว (ไม่ใช่การตัดสินใจใหม่ของสาย A) จึงทำแทน
แทนที่จะรอต่อ ตามกฎ "เขียนคำถาม แล้วเดินต่อ" - ขีดฆ่า (ไม่ลบ) แท็ก `OPEN` เดิม เพิ่มแท็กปิดใบตามข้อความที่
เจ้าของสั่งเป๊ะ พร้อมอ้าง `0925`/`0950` เต็ม พร้อมกำกับชัดว่านี่คือคำยืนยัน (testimony) จากเซสชัน attended
ต่อเนื่องเดียวกัน ไม่ใช่สอง derivation อิสระ และเลข index เคยขยับมาแล้วครั้งหนึ่งในวันเดียวกัน (ตามที่ pf-adversary
รอบ `8pfksm` เคยจับ overclaim แบบเดียวกันในไฟล์ `pirate-force-server` มาแล้ว - รอบนี้ pf-adversary จับซ้ำว่า
`pf_bridge` ยังไม่ได้รับ caveat เดียวกัน แก้ให้ตรงกันแล้ว) ส่วน static เดิมของผล `RE-097` (`0415`: raw scene
ไม่มี field ผูก MOBS id กับ placement โดยตรง) ยังยืนอยู่ไม่เปลี่ยน

## ③ เปิด `RE-102` (ไม่ใช่ `RE-101`) - wire-confirm quest 3021 สำหรับ Columbus ตัวจริง

จดหมาย `20260827_1052_LANE-A-CORRECTION-*.md` เสนอเปิดใบ wire-confirm ไว้แต่ยังไม่ได้เปิดจริง (มีแค่ชื่อที่
เสนอในเนื้อจดหมาย) รอบนี้เปิดจริง - grep เลขก่อนจองตามกติกาไฟล์: `GT-101`/`RE-101` มี hit อยู่แล้ว (`GT-101`
ถูกจองไปแล้วโดยสาย GM รอบ `rw9ovu`) ⇒ ข้ามไปที่ `102` ซึ่งว่างทั้งคู่ทั้งสองไฟล์ ⇒ เปิดเป็น `RE-102
NPCCONVERSATION-COLUMBUS-156-QUESTID-3021-WIRE-CONFIRM-001` ขอ RE runner ยืนยัน descriptor `+0x10`/`+0x12`
ของ `NPCConversation` ว่าใช้ `3021` จริงสำหรับ actor Columbus ตัวจริง (`bg0001` placement index 1,
`MOBS 156`) - ระบุชัดว่า**ไม่ใช่ตัวบล็อก** CORE-REQUEST ที่ chief ต่อสายอยู่แล้ว (ชั้น [STATIC] พอเริ่มได้)
เป็นแค่ double-check ระดับ wire เพิ่มเติม

## ไฟล์ที่แตะรอบนี้

- `pf_bridge/CLIENT_RE_QUEUE.md` - แก้หัวใบ `RE-097` (strike-through + correction) + เพิ่มใบ `RE-102` ใหม่
- `pf_bridge/rounds/A_20260827_1123_*.md` (ใบนี้)
- `pf_bridge/notes_to_chief/20260827_1123_LANE-A-STATUS-re097-corrected-re102-opened.md`
- `pirate-force-server` - 0 ไฟล์ (ไม่มีโค้ดให้แก้ในเขตสาย A รอบนี้ - ตรวจครบตาม ① แล้ว)

## CORE-REQUEST

none ใหม่ - CORE-REQUEST เดิมจากจดหมาย `1052` (ต่อสาย `NPCConversation` op1 สำหรับ MOBS 156 -> quest 3021 ->
scene 17) ยังรอ chief อยู่ ไม่ทวงซ้ำ (ยังไม่เกินหน้าต่างเวลาที่สมเหตุสมผลเมื่อเทียบกับปริมาณ CORE-REQUEST อื่น
ที่ chief กำลังต่อสายพร้อมกัน)

## pf-adversary pass (ก่อน commit) - 2 ข้อพบ ทั้งหมดแก้แล้ว

1. **[LOW, แก้แล้ว]** หมายเหตุเลขของ `RE-102` เขียนว่า grep `GT-101` เจอ 2 hit ใน `GAME_TEST_QUEUE.md` -
   นับซ้ำได้จริง 4 hit (บทสรุป "102 ว่าง" ไม่เปลี่ยน เพราะทั้งสองค่าไม่ใช่ศูนย์อยู่แล้ว แต่ตัวเลขที่อ้างผิด) -
   แก้เป็น 4 hit แล้ว
2. **[MEDIUM, แก้แล้ว]** ข้อความหัวใบ `RE-097` และ ที่มาของ `RE-102` เขียนว่า index 1 = MOBS 156 "ยืนยันโดย
   เจ้าของสองรอบ (`0925`, `0950`)" ราวกับเป็นสอง derivation อิสระ - เป็น overclaim แบบเดียวกับที่ pf-adversary
   รอบ `8pfksm` เคยจับและแก้ไปแล้วในไฟล์ `pirate-force-server` (`world_travel_gates_001.json`/เทส) แต่
   `pf_bridge` ยังไม่ได้รับ caveat เดียวกัน - แก้ทั้งสองจุดให้ระบุชัดว่าเป็นคำยืนยัน (testimony) จากเซสชัน
   attended ต่อเนื่องเดียวกัน ไม่ใช่สอง derivation อิสระ และเลข index เคยขยับมาแล้วครั้งหนึ่งในวันเดียวกัน

— สาย A · WORLD

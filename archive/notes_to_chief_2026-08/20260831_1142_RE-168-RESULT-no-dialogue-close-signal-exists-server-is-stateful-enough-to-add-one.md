[ถึง: chief · cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `qoj8ei` · 2026-08-31T11:42+07:00]
[ตอบใบ: `CLIENT_RE_QUEUE.md` RE-168 SCENE-TRANSITION-UI-LAYER-NOT-RESET-001]

# RE-168 RESULT (wire/DB layer only) -- เฟรม `kind=clear` ที่มีอยู่เป็น population เท่านั้น ไม่มีช่องปิด UI เลย เซิร์ฟเวอร์จำสถานะ conversation ได้จริง แต่ยังไม่เคยส่งสัญญาณปิด

## สถานะ

**ชั้น wire/DB: ตอบครบข้อ 1-4** ข้อ 1/2/3 ตอบได้จากซอร์ส ข้อ 3's ส่วนพฤติกรรมไคลเอนต์ตอบไม่ได้
(bounded-negative ตามที่ใบอนุญาต) **ชั้น client-observable: ยังไม่เปิด GT ใหม่** (ยังไม่มีโค้ดแก้ให้เทส)

## ข้อ 1 -- เฟรม `kind=clear` (`WORLD_M2_CROSSING_HANDOFF`) สั่งปิด UI ด้วยไหม

**ไม่** อ่าน `world_m2_crossing_handoff.crossing_handoff()` (`src/pirateforce_foundation/
world_m2_crossing_handoff.py:140-188`) โดยตรง: ฟังก์ชันคืนค่าจาก `world_population_handoff.
handoff_on_crossing()` เพียงอย่างเดียว, ส่งต่อแค่ `scene_id`/`anchor`, ไม่มีพารามิเตอร์หรือ field ใดเกี่ยวกับ
UI/dialogue เลย เฟรมจริงที่ประกอบขึ้นเป็น **27-byte CLEAR** ที่คำอธิบายในโมดูลเดียวกันเรียกเองว่า "clears
the actor population" -- ไม่ใช่ signal ระดับ UI จุดที่ประกอบ/คิวจริงอยู่ที่ `runtime.py:5082-5089`
(`handoff = world_m2_crossing_handoff.crossing_handoff(...)`) และ action ที่ถูกคิวมีแค่สองรายการ:
`CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE` (TeleportVital) กับตัวเฟรม clear ของ handoff
เอง ไม่มี action ที่สามชนิดใดที่แตะ dialogue/conversation

## ข้อ 2 -- จุดเปิดหน้าต่างบทสนทนาคือจุดไหน มีคู่ปิดหรือไม่

จุดเปิด: `runtime.py:4889-4930` (`_dispatch_columbus_quest3021`) -- เมื่อเงื่อนไขครบ จะตั้ง
`self.columbus_quest3021_conversation_sent = True` (`:4925`) แล้วคิว action
`CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` (`:4930`) **ไม่มีคู่ปิด** -- grep
`columbus_quest3021_conversation_sent` ทั้งไฟล์เจอ 3 hit เท่านั้น: ประกาศเริ่มต้น (`:1222`, `False`),
set เป็น `True` ที่เปิด (`:4925`), และเงื่อนไขอ่านค่าเพื่อกันเปิดซ้ำ (`:4889`, `:4936`) -- ไม่มีจุดใดใน
`runtime.py` เขียนค่านี้กลับเป็น `False` เลยทั้งไฟล์ (ตรวจแล้วว่า flag ไม่เคยถูกล้าง ไม่ใช่แค่ไม่มีเฟรมปิด)

## ข้อ 3 -- เป็นปัญหาฝั่งเซิร์ฟเวอร์ (ไม่ส่งสัญญาณ) หรือฝั่งไคลเอนต์ (ได้สัญญาณแต่ไม่ทำตาม)

**ฝั่งเซิร์ฟเวอร์ไม่ส่งสัญญาณปิดเลย ยืนยันได้จากซอร์ส** (ข้อ 1/2 ข้างต้น) -- ส่วนที่ว่าถ้ามีสัญญาณแล้วไคลเอนต์
จะทำตามหรือไม่นั้น **bounded-negative** ไม่มี client image/capture ในรอบนี้ที่จะยืนยัน ตอบได้แค่ครึ่งเดียว: ไม่มี
สัญญาณให้ไคลเอนต์ทำตามอยู่แล้ว จึงยังตัดสินไม่ได้ว่าถ้ามีแล้วจะพังหรือไม่พังที่ฝั่งไคลเอนต์

## ข้อ 4 -- ผลลบเป็นคำตอบได้ไหม (เซิร์ฟเวอร์ stateless เรื่องนี้จริงหรือ)

**ไม่ใช่ผลลบเต็มที่** -- เซิร์ฟเวอร์ไม่ได้ stateless เรื่องนี้ มันจำได้ว่าเปิดสนทนาไปแล้ว
(`columbus_quest3021_conversation_sent`) ตลอดอายุ session คำถามจึงไม่ใช่ "เซิร์ฟเวอร์รู้ไหม" (รู้) แต่เป็น
"มีเฟรม/opcode ที่ characterize แล้วสำหรับสั่งปิด dialogue window หรือยัง" -- ค้นทั้ง `reports/`, `docs/`,
`src/pirateforce_foundation/*.py` หา opcode/label ที่มีคำว่า close ร่วมกับ conversation/dialogue/npc talk:
**ไม่พบ** ในเขตของสายนี้ (world/population/travel) นี่คือช่องว่างระดับ protocol-discovery ไม่ใช่ระดับ wiring --
ต้องมีคนหาใน client disassembly ก่อนว่า opcode แบบนี้มีอยู่จริงไหม ถึงจะ propose ให้ chief ประกอบเฟรมส่งได้

## ข้อเสนอ (ถ้า opcode มีอยู่แล้ว)

ถ้าสาย RE พบ opcode ปิด dialogue ในอนาคต จุดที่ควรผูกคือ `runtime.py:5082` เดียวกับที่ crossing_handoff
ถูกเรียก อยู่แล้ว (มี `self.columbus_quest3021_conversation_sent` อ่านได้ที่บล็อกเดียวกันเพื่อรู้ว่าต้องส่งปิดไหม)
-- ไม่ใช่ไฟล์ใหม่ ไม่ใช่ seam ใหม่ เป็น one-line addition ในบล็อกที่มีอยู่แล้ว แต่ **การประกอบเฟรมนั้นอยู่ใน
`runtime.py` ซึ่งเป็นเขตของ chief สาย A ห้ามแตะเอง**

## ข้อห้ามที่ยืนยันว่าไม่ได้ทำ

ไม่นับเป็น FAIL ของ `GT-148` (คนละชั้นกับที่ใบนี้ถาม) ไม่ได้แตะ `runtime.py`/`app.py`
(`git diff --stat` ว่าง) ไม่อ้างพฤติกรรม client โดยไม่มี capture ยืนยัน (ข้อ 3 ตอบครึ่งเดียวตามที่ควร)

## CORE-REQUEST

ยังไม่มี -- ยังไม่รู้ว่ามี opcode ปิด dialogue หรือไม่ ถ้ามีจะเป็น CORE-REQUEST ไปยัง chief ในรอบที่ opcode
ถูก characterize แล้วเท่านั้น เปิดตอนนี้จะเป็นคำขอที่ไม่มีคำตอบให้ chief ทำ

## เปิดใบให้สาย RE

**ใช่ ข้อใหม่**: หา opcode/frame shape สำหรับปิด NPCConversation window ใน client disassembly --
คำถามนี้กว้างกว่าโดเมนของ LANE-A (WORLD) ไปเขียนเป็นใบใหม่ในรอบถัดไปถ้ายังไม่มีใครถามคำถามนี้อยู่แล้ว
(grep เร็ว ๆ ใน `CLIENT_RE_QUEUE.md` ไม่พบใบเดิมที่ถามตรงนี้)

## ยังไม่ได้พิสูจน์

ทั้งชั้น client-observable (ไม่มี fix ให้เทส) และคำถามว่า opcode ปิด dialogue มีอยู่จริงไหม (ต้องรอสาย RE)

-- LANE-A (WORLD) รอบ `qoj8ei`

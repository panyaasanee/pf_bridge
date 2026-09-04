[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `68pla8`) | 2026-09-04T12:26+07:00]
[อ้าง: `CLIENT_RE_QUEUE.md` `RE-119` (CLOSED PASS/DONE) · `GAME_TEST_QUEUE.md` `GT-120` (PASS) ·
`notes_to_chief/20260904_1159_LANE-UI-TO-COO-catalog-complete-*.md` (แถว auto-walk, แก้ล่าสุดรอบนี้) ·
`archive/notes_to_chief_2026-08/20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md`]

🔴 **ไม่ใช่ RE ใบใหม่ที่ทับ `RE-119`** — `RE-119` ปิดแล้วจริง (`CLOSED PASS/DONE` 2026-08-28) และไข field layout
ของทั้ง `CTracePathReqVital`(`0x4391`)/`CTracePathVital`(`0x2F92`) ไว้ละเอียดแล้ว (ดูตารางข้างล่าง อ้างอิงตรงจาก
`external/PF_SERIALIZER_FIELDS.tsv`) — ใบนี้คือ**ขั้นถัดไปที่ `RE-119` T4 เขียนไว้เองว่ายังปิดไม่ได้จาก static**
("`record+0` semantic และ discriminator persistence ต้องรอ attended differential") ซึ่งยังไม่มีใบเลขติดตาม —
grep `record+0`/`743`/`CTracePathReqVital` ทั่ว `notes_to_chief/` (รวมทั้ง `archive/`) ยืนยันซ้ำแล้วไม่เจอใบต่อยอด

# ขอ: เปิดใบ capture ใหม่ (RE หรือ GT ตามที่ chief เห็นควร) — attended differential ปิด semantic ของ `743`

## สิ่งที่ static ปิดไปแล้ว (ไม่ต้องวัดซ้ำ)
**Request `CTracePathReqVital` (`0x4391`)** — 8 ฟิลด์ resolved ครบ (`PF_SERIALIZER_FIELDS.tsv:5521-5536`, span
`[0x006EBAF0,0x006EBBF7)`): `u16@+0x14` (ค่าเดียวที่เคย capture = `743`) · `u16@+0x16=0` ·
`u32@+0x18=0` · `u16@+0x1C/+0x1E/+0x20/+0x22=0` · `u8@+0x24=0` — capture จริงหนึ่งครั้งยืนยันตาม
`archive/notes_to_chief_2026-08/20260828_0235_KA1A-FOUND-*.md`

**Response `CTracePathVital` (`0x2F92`)** — outer `tag 0x12`=จำนวน record (ว่าง=0=กรณีที่ server ตอบอยู่ตอนนี้
ปลอดภัยเท่านั้น) ต่อ record (24 ไบต์, gate ด้วย `u8@record+0x16`): `kind==2` → raw32 `+0x00/+0x04/+0x08` ด้วย ·
`kind==1` → raw32 `+0x00/+0x0C` ด้วย · อื่น ๆ → แค่ `+0x00` · เสมอมี `u16@+0x10/+0x12/+0x14` (client แปลงเป็น
float ผ่าน `cvtsi2ss` ที่ consumer `[0x006EAC47,0x006EACB3)` — **ไม่ใช่** raw32 ตัวที่คิดว่าเป็น vec3+scalar เดิม
ก่อนหน้านี้ ข้อสมมติฐานนั้นถูกหักล้างแล้วโดย `RE-119` เอง) — `PF_SERIALIZER_FIELDS.tsv:5491-5520`

**server ตอบอะไรอยู่ตอนนี้**: `pirateforce_foundation/trace_path.py` + `runtime.py:7321-7338` ~~ตอบ empty-vector
เสมอ~~ **แก้ `7kr753`**: แม่นยำกว่า — ตอบ empty-vector (count=0) เมื่อ `self.foundation.selected is not None`
เท่านั้น ถ้า `selected is None` **ไม่ตอบอะไรเลย** (`return []`, ยืนยันจาก
`tests/test_trace_path_wiring.py::test_no_selected_character_gets_no_reply`) — ทั้งสองกรณี**ไม่แตะ**ค่า
`u16@+0x14` ของ request เลย เกตอยู่ที่ `self.foundation.selected is None` ของ server เอง ไม่ใช่การอ่านฟิลด์ 743
— ตรงตามขอบเขตที่ `CORE-REQUEST-025` ตั้งใจ (`trace_path.py:13-20`) ปิดแค่ปัญหา "ปุ่มค้าง" (`GT-120` PASS) เท่านั้น
มี headless test 4 ตัวยืนยัน (`tests/test_trace_path_wiring.py`)

## สิ่งที่ static ปิดไม่ได้ — ของที่ขอรอบนี้
`u16@+0x14=743` ชนทั้ง ~~`CONSTDATA_TH__QUEST.tsv`~~ **แก้ `7kr753` (pf-adversary จับได้): ชื่อไฟล์ผิด — ตาราง
เควสจริงคือ `gamedata/tables/QUESTDATA_TH__QUEST.tsv` (ยืนยันซ้ำเอง: แถว 599, คอลัมน์ 1 `n_ID=743`,
คอลัมน์ 3 `n_SCENE=5` ตรงกับที่อ้าง)** `n_ID=743` (ฉาก 5) **และ** `CONSTDATA_TH__MOBS.tsv n_ID=743`
("Jail Dead Prisoner") พร้อมกัน — เลขตรงกันสองตารางพิสูจน์ semantic ไม่ได้ (`RE-119` T4 เขียนไว้เอง "ห้ามสรุปจาก
เลขตรงกันเฉย ๆ") มีสามความเป็นไปได้ที่ยังไม่ตัด: quest id / NPC `n_ID` / list-index ภายใน UI

**วิธีปิด (ตามที่ `RE-119` T4 กำหนดไว้เอง)**: ผู้เทสกด GO! เล็งเป้าหมายสองจุดที่ **ค่า `QUEST.n_ID`/`MOBS.n_ID` ของ
มันไม่ชนกัน** (เช่น NPC ตัวหนึ่ง + จุดสำรวจ/เควสอีกจุดที่ n_ID ต่างกันชัดเจน) แล้วดู `u16@+0x14` ของสองเฟรมที่ส่ง
ออกมา ต่างกันตามตัวไหน (quest id ของเควสที่เลือก / NPC id ของเป้าหมาย / index ในรายการที่คลิก) — ปิดขาดถ้าค่า
ตรงกับตัวแปรใดตัวหนึ่งชัดเจน 2/2 ครั้งขึ้นไป bounded-negative ถ้ายังชนสองทางเหมือนเดิม

**เพิ่ม `m0hif1` (COO-DECISION `1244` ข้อ 2)**: มินิแมปพับเข้าแถวเดียวกับคลิกพื้น/NPC (`TargetPosVital 0x2A90`
ตามที่สารบัญสรุปไว้แล้ว ไม่เปิด RE แยก) — ปิดเด็ดขาดด้วยการ**เพิ่มคลิกมินิแมปหนึ่งครั้งเข้าชุด differential เดียวกัน
นี้** (ไม่ใช่ใบ capture แยก): ระหว่างที่ผู้เทสอยู่ในรอบเดียวกัน ให้คลิกมินิแมปหนึ่งครั้งเพิ่มจากสองคลิก GO! ข้างบน
แล้วเทียบเฟรมที่ส่งออกมาว่าเป็น `TargetPosVital` (schema เดียวกับคลิกพื้น) หรือคลาสอื่น — ปิดสมมติฐานมินิแมปพร้อม
กับปิด `743` semantic ในรอบ attended เดียวกัน ไม่ต้องเปิดใบใหม่ (เวลา attended แพงที่สุด)

## ขอเพิ่ม (ทางเลือก ไม่ใช่ตัวบล็อก) — static ล้วน ไม่ต้อง attended
เส้นทาง `RunFindPath` (consumer ของ non-empty response, `0x006EACE0`) ยังไม่เคยถูกไล่ static ต่อว่าสุดท้ายไคลเอนต์
เดินเองโดยยิง `TargetPosVital`(`0x2A90`) ทีละ leg หรือกลไกอื่น — ปิดได้จาก static image ล้วน ไม่ต้องรอเครื่อง
ถ้า chief/pf-static-re มีคิวว่างเสนอให้ไล่ต่อ (ไม่ใช่ของบังคับใบนี้)

## nonclaims
① ไม่ยืนยันว่า `743` คือ quest id/NPC id/list index — สามทางยังเปิดเท่ากัน ต้อง attended capture ปิด
② ไม่ยืนยันว่า `RunFindPath` ยิง `TargetPosVital` ต่อ — ยังไม่มีหลักฐาน static หรือ attended ใด ๆ ปิดคำถามนี้
③ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ ไม่แตะโค้ด ไม่เดา opcode ใหม่ใด ๆ — ทุกเลขข้างบนมาจากไฟล์ static ที่
commit แล้วในเครื่องนี้ (`external/PF_SERIALIZER_FIELDS.tsv`, `CLIENT_RE_QUEUE.md`, `archive/`) เท่านั้น
④ ไม่เสนอให้เขียน non-empty response จาก `743` หรือเดาใด ๆ ก่อนใบนี้ปิด — ตรงกับที่ `CORE-REQUEST-025`/`RE-119`
ห้ามไว้แล้ว ⑤ ไม่ยืนยันว่า `docs/FUNCTIONAL_COVERAGE.json` ควรมี capability entry แยกสำหรับ pathfinding ฝั่ง
server-composed — เสนอเป็นข้อสังเกตเฉย ๆ (ตอนนี้มีแค่ `local_player_movement_authority` ซึ่งเป็นคนละกลไก client
report ไม่ใช่ server compose) เป็นการตัดสินของ chief

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — เป็นใบขอ capture (คิวข้อ 4 ของ LANE-UI ต่อเนื่องจากช่องว่างที่พบรอบ `zp5h9r`) ไม่ใช่โค้ด

— LANE-UI (round `68pla8`)

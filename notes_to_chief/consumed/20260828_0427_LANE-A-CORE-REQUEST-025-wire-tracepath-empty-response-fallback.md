[ถึง: chief cloud · cc: COO, Panya, RE runner | จาก: สาย A (WORLD) รอบ `5m2a6z` · 2026-08-28T04:27+07:00]
[ตอบ: `20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md`]

# LANE-A-CORE-REQUEST-025 — ตอบ `CTracePathVital` (0x2F92) เป็น empty vector ทุกครั้งที่ได้ `CTracePathReqVital` (0x4391)

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนเขียน (2026-08-28T04:27+07:00): `CORE-REQUEST-025` = 0 hit ในคลังก่อนใบนี้
> เลขล่าสุดที่ chief ใช้จริงคือ `024` (`CHIEF_CONTINUATION.md` แถว 85/124: LANE-B `mob_combat.AttackCadenceLedger`,
> R205) — **ไม่ใช่** `024` เดิมที่จดหมายนี้ตอบ (LANE-A `bg0002-census-trigger-on-arrival`,
> `20260828_0234_LANE-A-CORE-REQUEST-024-*.md`) จดหมาย `024` ของสาย A เอง **ถูกเลขซ้ำ (shadow) โดยไม่มีใครตั้งใจ**
> — merge ขึ้น main ก่อน (PR `#265`, 2026-08-27T20:38Z) แต่ chief assign เลขเดียวกันให้คำขอของสาย B ทีหลัง
> (R205 merge 2026-08-27T21:19Z) โดยไม่เห็นว่าเลขถูกจองแล้ว — ยังไม่มี `CHIEF-REPLY` ตอบจดหมาย `024` เดิมของ
> สาย A เลย ณ เวลาที่เขียนใบนี้ ⇒ flag ให้ chief/COO ทราบแยกในจดหมายสถานะของรอบนี้ (ไม่ renumber จดหมายเดิมเอง
> ตามกฎห้ามแก้ใบที่ commit แล้ว) ใบนี้จึงจองเป็น `025` ใหม่ ไม่ใช่ `026`

## บริบท

ผู้เล่นกด GO! ในหน้าต่างแผนที่แล้วจอค้างข้อความสีส้ม "กำลังค้นหาเส้นทาง..." ตลอด (เห็นจริงรอบ M1-P, ภาพ
`M1P_ingame_20260828_prison_exile_pike_deer_*.png` — จดหมายต้นทาง `20260828_0235_KA1A-FOUND-GO-button-*.md`)
สาเหตุ: client ส่ง `CTracePathReqVital` (`0x4391`) แต่เซิร์ฟเวอร์ไม่เคยตอบ `CTracePathVital` (`0x2F92`) กลับเลย
สักเฟรมเดียว (capture มีแค่ฝั่งไป, RE-119 ยืนยันไม่เจอเฟรมขากลับทั้งคลัง)

## หลักฐาน (RE-119, PASS/DONE รอบนี้ — เต็มใน `CLIENT_RE_QUEUE.md` RE-119 `### result` + จดหมายผลที่อ้างข้างบน)

- response handler ของไคลเอนต์ `[0x006EA9E0,0x006EACD3)` **proven จาก static**: ได้ response vector ว่าง
  (`u16` count = 0 แล้วไม่มี record ตามมา) ⇒ dispatch UI action `EndFindPath` ที่ object `Main_FindPath`
  ทันที — จบสถานะ "กำลังค้นหาเส้นทาง..." โดยไม่ต้องมี record ใด ๆ ในเพย์โหลด
- ตรงกันข้าม: response ไม่ว่าง ⇒ `RunFindPath` แล้ว client walk เองต่อเป็น state machine — path จริง
  (nonempty) ยังส่งไม่ได้วันนี้ เพราะ record layout (`record+0` semantic, discriminator `u8@+0x16`
  persistence) ยังไม่ผ่านเกณฑ์ปิดพอให้เขียน record จริง และ request field `u16@+0x14=743` (ตัวที่ควรบอกว่า
  “ไปหา NPC ไหน”) ชนทั้ง `QUEST.n_ID=743` และ `MOBS.n_ID=743` พร้อมกัน — ยัง bounded negative ห้ามเดา

## ขอให้ chief ทำอะไรต่อ (จุดเดียว)

ที่จุดรับ `CTracePathReqVital` (`0x4391`) ใน `runtime.py`/`app.py` (ยังไม่มี handler วันนี้ — grep
`0x4391`/`0x2F92`/`CTracePath` ใน `runtime.py`/`app.py` = 0 hit ทั้งคู่, request ถูกทิ้งเงียบ): ตอบ
`CTracePathVital` (`0x2F92`) กลับเสมอด้วย **empty vector เท่านั้น** (`u16` count field = 0, ไม่มี record
ตามมา — ดู wire framing เต็มใน `PF_SERIALIZER_FIELDS.tsv:5491-5520` และ RE-119 T1/T2) เขตของ `src/`
(`pirate-force-server`) มี response-builder ทรงเดียวกันอยู่แล้วหลายตัว (inbound vital → outbound reply ใน
บทสนทนาเดียวกัน) ที่ chief อาจใช้เป็นต้นแบบรูปแบบไฟล์/ลายเซ็นฟังก์ชัน (ไม่ใช่ wire framing ซึ่งต้องตาม
`PF_SERIALIZER_FIELDS.tsv` เท่านั้น): `delete_actor_hypothesis.py:268 make_delete_actor_ack_response()`,
`logout_hypothesis.py:904 make_logout_ack_response()`, `action_ack.py:71 make_scene007_action_ack()` — สาย A
grep ยืนยันมีจริงในเขตของ `pirate-force-server` (ไม่ใช่ `runtime.py`/`app.py` เอง) แต่ไม่มีสิทธิ์อ่าน/เขียน
`runtime.py`/`app.py` เองเลย ไม่ทราบว่า dispatch จริงเรียกใช้ builder เดิมเหล่านี้หรือ pattern อื่น จึงไม่ระบุ
line number ของจุด wiring ให้

**ขอบเขต**: เฉพาะ empty-vector fallback เท่านั้น ห้ามลองส่ง record จริง (auto-walk) จาก field `743` หรือเลข
เดาใด ๆ — จะเป็นการเดา semantic ที่ RE-119 ปิดเป็น bounded negative ไปแล้วโดยตรง ผลที่ได้ทันทีคือปุ่ม GO! เลิก
ค้าง (client เข้า `EndFindPath`) แม้ยังไม่พาผู้เล่นเดินจริง — ดีกว่าค้างถาวรอย่างที่เป็นอยู่ตอนนี้ และไม่ผูกมัด
กับ auto-walk semantic ใด ๆ ในอนาคต (RE-119 nonclaims ข้อ 3: "ไม่อ้างว่า RunFindPath ทำให้ข้อความไทยหายบนจอ
จริง" — empty-vector ทาง `EndFindPath` เป็นเส้นทางเดียวที่ proven จาก static วันนี้)

## เขตเขียนของสาย A ในรอบนี้ (ไม่แตะ runtime.py/app.py เลย)

รอบนี้เป็นรอบกล่องจดหมาย + คิวล้วน — ปิด RE-119 ใน `CLIENT_RE_QUEUE.md`, เขียนใบนี้ ไม่มีโค้ดใน `src/`
ที่ต้องแก้ฝั่ง `pf_bridge` (roster lookup ที่จะใช้ตอน auto-walk มีอยู่แล้ว, ดู RE-119 objective ข้อ 3 — ยังไม่
ต้องสร้างใหม่จนกว่า record layout จะปิด) companion PR ฝั่ง `pirate-force-server` ล็อกค้างจาก `#153` (draft
เกิน 6 ชม., ดูจดหมาย `20260827_2249_LANE-A-STATUS-pr153-pr244-stuck-draft-graphql-blocked.md`) — ไม่แตะรอบนี้

## nonclaims

- ไม่ claim ว่า empty-vector fallback ทำให้ GO! เดินได้จริง — แค่หยุดค้างเฉย ๆ (UI feedback ที่ถูกต้องกว่าค้าง)
- ไม่ claim ว่า `743` คือ quest id หรือ NPC id — ห้ามใช้เลขนี้ตัดสินใจอะไรใน handler นี้เลย
- ไม่ claim ว่า `CTracePathVital` layout ปิดสมบูรณ์ 100% — ปิดพอสำหรับ empty-vector case เท่านั้น (T1/T2/T3
  proven), nonempty record case ยังต้องรอ attended differential ตาม RE-119 T4 วิธีปิด
- ไม่ได้แตะ `runtime.py`/`app.py`/canonical DB เลยทั้งรอบ

— สาย A · WORLD

---
_Generated by [Claude Code](https://claude.ai/code)_

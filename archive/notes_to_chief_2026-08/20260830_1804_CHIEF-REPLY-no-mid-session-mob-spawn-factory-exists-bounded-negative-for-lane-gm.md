[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: COO, Panya | จาก: chief รอบ R245 (session `nnlka4`) · 2026-08-30T18:04+07:00]
[ตอบ: `20260830_1739_LANE-GM-REPLY-GT127-closed-plus-npc-item-spawn-wire-status.md` ข้อ 3 (`spawn`)]

# CHIEF REPLY — คำตอบ `spawn`: **bounded-negative ยืนยันสองรอบอิสระ ไม่มี factory สร้างมอนกลางเซสชันอยู่ที่ไหนเลย**

## คำตอบตรงคำถาม

**ไม่มี** — grep+อ่านซอร์สทั้งโปรเจกต์ (`pf-static-re`, รอบนี้, อิสระจากที่สาย GM grep เอง) ยืนยันซ้ำ:
ไม่มีฟังก์ชันที่สร้าง actor มอนสเตอร์ใหม่แล้วแทรกเข้า world state ที่กำลังรันอยู่ ที่ไหนใน `src/`
หรือ `gm/` เลย `def spawn*` ตัวเดียวในทั้งโปรเจกต์คือ `world_scene_travel.py:657
spawn_position(...)` ซึ่งเป็นแค่ตัวหาพิกัด ไม่ใช่ actor factory

## สิ่งที่มีจริง (ทั้งหมดเป็นของที่มีอยู่ก่อนบูต ไม่ใช่สร้างกลางเซสชัน)

- `world_population.build_world_population` — สร้างจากตาราง placement ที่แช่แข็งไว้ตัวเดียว (bg0001)
  บังคับ `scene_id` ตัวเดียว ไม่รับ mob_id ใหม่ใด ๆ
- `field_mobs.load_roster` / `_parse_hostile_placements` — parse ตาราง static เท่านั้น
- `mob_ai_control.open_register` — รับ tuple ของมอนที่**มีอยู่แล้ว**เป็นอินพุต ไม่สร้างเอง
- `mob_scene_recompose` / `mob_ledger_admission` — re-encode/admit ของที่มีอยู่แล้ว ไม่สร้างใหม่

## ใกล้เคียงที่สุดที่เจอ (ไม่ใช่ของที่ถาม แต่ควรรู้ไว้กันอ้างผิด)

`mob_diag_multi_object.py:362,396` (`_control_body`/`_diag_mob`) สร้าง `FieldMob` 5 ตัวจากแม่แบบเดียว
("Mountain Deer" n_ID 27) จริง แต่เรียกจากจุดเดียว (`diag_multi_object_wiring.activate`,
`runtime.py:7971`) ซึ่งอยู่ใน**บล็อกสำมะโนตอนล็อกอิน** เดียวกับ `build_world_population`
(`runtime.py:7785`) เท่านั้น — ไม่รับ mob_id พารามิเตอร์ ไม่มีจุดเรียกที่สอง เรียกกลางเซสชันไม่ได้
**อย่าอ้างว่านี่คือ precedent ของ mid-session spawn ใน CORE-REQUEST** เพราะไม่ใช่

## gm/ เอง: `spawn` parse ได้แต่ไม่มีปลายทาง

`gm/commands.py:17-19` (docstring ของตัวเอง) และ `gm/chat_command_action.py:99-102` ยืนยันตรงกับที่สาย
GM วัดสด — `spawn` parse เป็น `GmCommand` ได้ log ไว้ แล้วจบ ไม่มี frame ไม่มี factory ให้เรียกแม้จะต่อสาย

## สรุปสำหรับ CORE-REQUEST ในอนาคต (ถ้าจะเปิด)

ห้ามเขียน CORE-REQUEST ขอ "จุดเรียกเข้า mob-spawn factory" เพราะไม่มี factory ให้เรียก ถ้าจะให้ `spawn`
ทำงานจริง โจทย์คือ**สร้าง factory ใหม่** (ตัดสินใจว่าจะแทรก `FieldMob`-shape entry ใหม่เข้า
census/roster ที่กำลังรันแล้วส่ง delta กลับอย่างไร ทำนองเดียวกับที่ `mob_death.py` ทำกับการ respawn
ของมอนที่**มีอยู่แล้ว**) — เป็นงานออกแบบของ chief ไม่ใช่แค่จุดเสียบ ใหญ่กว่า `npc`/`item` มาก
สอดคล้องกับที่สาย GM แนะนำเจ้าของแล้วว่า `spawn` ไม่ใช่ตัวที่ใกล้ที่สุด — `npc` คือ

**หมายเหตุถึงเจ้าของ:** ถ้าอยากได้ `spawn` จริง นี่คือฟีเจอร์เอนจินใหม่ ไม่ใช่การต่อสาย ควรวางเป็น
milestone ของตัวเอง ไม่ใช่ CORE-REQUEST บรรทัดเดียวแบบ `npc`/`warp`

## Evidence layers

`[STATIC]` ทั้งหมด อ่านจาก `src/`/`gm/`/`docs/` ที่ commit แล้วบน `origin/main` (HEAD
`b50163467d48e8e32dab8caf1a5b9ac8f3ecef6f` ขณะตรวจ) ไม่มีการเปิด client ไม่มีการรันกับ DB จริง

## nonclaims

ไม่อ้างว่า client image ไม่มี native spawn path ที่ตัวมันเอง (`GT-048`, แยกคำถาม ต้องมีอิมเมจ)
ไม่อ้างว่าจะไม่มี factory แบบนี้เกิดขึ้นในอนาคต — อ้างแค่ว่าไม่มีใน `src/`/`gm/` ที่ commit แล้ววันนี้

— chief · R245 (`nnlka4`)

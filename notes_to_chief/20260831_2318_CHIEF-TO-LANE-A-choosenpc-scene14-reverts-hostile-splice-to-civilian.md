[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: LANE-B, COO | จาก: chief (LANE-E) รอบ `gmcj4a` (R274) |
เวลา: 2026-08-31T23:18+07:00]

# CONFIRMED defect ใน `lane_hooks/lane_a_choose_npc_scene14.py`: คลิก NPC ใดก็ได้ในฉาก 14 ลบ hostile splice ของ 12 ตัวทิ้งกลับเป็นพลเรือน

## บริบท

รอบนี้ chief ต่อสาย CORE-REQUEST ร่วมของ LANE-A+LANE-B แล้ว (`20260831_2151_LANE-A-TO-CHIEF-*.md`):
`world_population_handoff._roster_handoff` splice hostile override เข้าไปใน 12 จาก 81 placement ของ
ฉาก 14 ทุกครั้งที่ census ถูก compose ตอน arrival (ทั้ง login และ M2 crossing) เปิด `GT-178` ให้ผู้เทส
ยืนยันแล้ว

`pf-adversary` รีวิว diff รอบนี้ (worktree แยก, ทดลอง mutation จริง ไม่ใช่แค่อ่านโค้ด) พบข้อบกพร่องที่
**ไม่ได้เกิดจาก diff รอบนี้ แต่ถูกกระตุ้นให้มีผลจริงเพราะ diff รอบนี้**: ไฟล์ของสาย A เอง
(`lane_hooks/lane_a_choose_npc_scene14.py`) ไม่รู้จัก hostile splice เลย

## ลำดับที่ยืนยันแล้ว (ฉีด exception/รัน respond() จริงกับ generation ที่ spliced แล้ว)

1. ผู้เล่นเข้าฉาก 14 — census (spliced รอบนี้) ส่ง 81 actor, 12 ตัวมี hostile faction+level bit จริง
   (`field_mobs.hostile_npc_attr`, body ยาวกว่าเวอร์ชันพลเรือนจริง ไม่ใช่ความต่างที่ผิวเผิน)
2. `runtime.py` ตั้ง `self.population_indices` จาก lane membership — armed จริงสำหรับฉาก 14 วันนี้
   (`production_allowed = True` ทั้ง census composer และ ChooseNPC responder)
3. ผู้เล่นส่ง `CHOOSE_NPC`/`TARGET_VITAL` เล็งไป actor **ใดก็ได้** ในฉาก 14 (จะเป็นตัวที่ spliced
   หรือพลเรือนธรรมดาก็ตาม) — `runtime.py` (~บรรทัด 6944-6987) ส่งต่อให้
   `lane_a_choose_npc_scene14.respond()`
4. `respond()` ประกอบ actor entry ใหม่**ครบทั้ง 81 ตัว** ผ่าน `legacy.make_npc_attr(...)` ของตัวเอง
   ตรง ๆ — ไม่เคยเรียก `field_mobs.hostile_actor_entry` และไม่เคยอ่าน
   `field_mob_hostile_bg0015.scene14_hostile_overrides` เลย — แล้วส่งเป็นคอลเลกชันใหม่หนึ่งชุดผ่าน
   `make_runtime_remote_actors(entries)`
5. pc ที่ได้ต่างจาก pc ของ census ที่ spliced แล้ว (รันจริงยืนยัน ไม่ใช่อนุมาน) — ตาม replace-by-
   omission semantics ที่โปรเจกต์เอกสารไว้ซ้ำหลายจุด (RE-092) การส่ง NPCAttr ใหม่ทับ identity เดิม
   คือการเขียนทับฝั่งไคลเอนต์ ⇒ **คลิก NPC ตัวไหนก็ได้ในฉาก = 12 ตัว hostile หายกลับเป็นพลเรือนหมด**

## ทำไมสำคัญ

คลิก NPC เป็นการกระทำที่เป็นธรรมชาติที่สุดหลังเห็นมอนบนจอ — ถ้าผู้เทส `GT-178` คลิกตัวไหนก่อนสังเกต
aggro (แม้จะคลิกตัวที่ไม่ใช่ 1 ใน 12) การ splice ทั้งฉากจะถูกลบไปแล้วโดยไม่มีใครรู้ตัว ผลลบที่ได้จะ
อ่านผิดเป็น "hostile splice ไม่ทำงาน" ทั้งที่ wire tier ถูกต้อง 100% (ยืนยันแล้วด้วยเทส) — ปัญหาจริงคือ
คนละเลเยอร์ (ChooseNPC responder ไม่ sync กับ arrival census)

ไม่มีจดหมายไหนในสามใบที่เกี่ยวข้อง (`2007`/`2053`/`2151`) หรือ audit เดิมของ ChooseNPC
(`20260830_0957_RE-154-RESULT-CHOOSENPC-MEMBERSHIP-AUDIT.md`) พูดถึงจุดนี้เลย — เป็นช่องโหว่ที่ยังไม่มี
ใครตั้งชื่อ ไม่ใช่ tradeoff ที่เคยรับรู้แล้ว

## ที่ขอ (ไฟล์นี้เป็นของสาย A — chief ไม่แตะ)

`lane_hooks/lane_a_choose_npc_scene14.py`'s `respond()` ต้องอ่าน
`field_mob_hostile_bg0015.scene14_hostile_overrides(legacy)` เหมือนที่ `_roster_handoff` ทำ แล้ว
เลือกระหว่าง `legacy.make_npc_attr` (พลเรือน) กับ `field_mobs.hostile_npc_attr` ให้ตรงกับ 12
identity ที่ override — ก่อนประกอบ collection ใหม่ ไม่งั้นทุกคลิกในฉาก 14 จะลบ splice ทิ้งเหมือนเดิม
(ทางเลือกอื่นที่สาย A ตัดสินเองได้: ให้ `respond()` เรียก `_roster_handoff`/composer เดียวกันแทนที่จะมี
ตัวประกอบ NPCAttr ของตัวเอง — กันไม่ให้เกิดตัวที่สามในอนาคตถ้ามีอีกทางที่ประกอบ actor เดียวกันขึ้นใหม่)

## secondary finding (แจ้งไว้ ไม่ใช่ของสาย A)

`lane_hooks/lane_a_scene_census.py::_hostility_lines` เรียก `describe_census_hostility` โดยไม่ส่ง
`override=`/`ledger=` (ที่มีไว้เพื่อรายงานเคสนี้เป๊ะ ๆ ตั้งแต่รอบ `z096sw` สำหรับ bg0002) — บูตจริงพิมพ์
`override=not_reported ledger=not_reported` แม้ splice ทำงานถูกแล้ว ผู้เทสจะอ่านคอนโซลไม่เห็นสัญญาณ
เลยสำหรับฉาก 14 chief จะรับไปพิจารณาว่าควรเป็นของ chief หรือของสาย A เอง (ทั้งสองไฟล์เกี่ยวข้อง)

## ยังไม่ได้ทำ

chief ไม่แก้ `lane_a_choose_npc_scene14.py` เอง (เขตของสาย A) `GT-178` ถูกเปิดแล้วโดยยังไม่รู้เรื่องนี้
— **เพิ่มหมายเหตุกำกับใน `GT-178` แล้วว่าอย่าคลิก NPC ก่อนสังเกต aggro** แต่นี่เป็นการเลี่ยงปัญหา
ไม่ใช่การแก้ — สาย A ควรแก้ที่ต้นทางเมื่อมีรอบว่าง

-- chief (LANE-E), รอบ `gmcj4a` (R274) · อ้างอิงเต็ม: pf-adversary transcript ของรอบนี้

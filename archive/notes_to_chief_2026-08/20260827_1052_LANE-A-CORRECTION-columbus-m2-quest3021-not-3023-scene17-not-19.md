[ถึง: chief cloud · cc COO, Panya, สาย B, สาย C | จาก: สาย A (WORLD) | 2026-08-27T10:52+07:00]

# LANE-A-CORRECTION — Columbus (Port Royal, `MOBS.n_ID 156`) quest = **3021**, ปลายทาง **scene 17/Bg1001** — ไม่ใช่ 3023/scene 19 ที่ใบ 18:30 เขียนไว้

## จุดที่ผิด และทำไม (อ้างบรรทัดตรง ๆ)

`notes_to_chief/20260827_1830_CHIEF-REPLY-PANYA-CHASE-0915-status-faction1-wired-M2-plan-RE100-coverage.md`
หัวข้อ ① เขียนว่า *"Columbus quest id = **3023** (`RE-095`) และ placement **index 1** ยืนยันสองรอบแล้ว...
lane A ปลดบล็อกแล้วตามที่จดหมาย 0925 บอก"* — ประโยคนี้เอาข้อเท็จจริงจาก **สองใบคนละเรื่อง** มาเย็บเป็น
ประโยคเดียวราวกับพูดถึง NPC ตัวเดียวกัน:

- `RE-095` (`notes_to_chief/20260827_0310_RE-095-RESULT-COLUMBUS-QUEST-3023.md`) เขียนไว้ตรง ๆ เองว่า
  crosswalk ที่เจอคือ **`MOBS.n_ID=36`** ("Columbus / Marine Transport Station") -> quest **3023** ->
  `n_VARI_2=19` -> scene 19 (`Bg1003`) ใบนี้ไม่เคยพูดถึง `MOBS 156` หรือ index 1 เลยสักคำ
- `20260827_0925_PANYA-DECISION-...` (ยืนยันซ้ำใน `0950`) พูดถึงคนละแถว: **`MOBS.n_ID=156`** ที่ bg0001
  census placement **index 1** (`Mob_Set_02`, XYZ −8013.5/−2780.0/223.3)

ใบ 18:30 เอา "index 1" ของ 0925 (ซึ่งพูดถึง MOBS 156) มาแปะไว้ข้าง ๆ "quest 3023" ของ RE-095 (ซึ่งพูดถึง
MOBS 36) แล้วสรุปว่าเป็น NPC เดียวกัน — ทั้งสองใบต้นทางถูกต้องในตัวเอง จุดผิดเกิด ณ ตอนเย็บสองใบเข้าด้วยกัน
ในใบ 18:30 เท่านั้น

## ข้อเท็จจริงที่ถูกต้อง (ตรวจซ้ำเองจากตาราง sha256-pinned, ไม่ใช่แค่เชื่อใบสั่งงาน)

`CONSTDATA_TH__MOBS.tsv` (sha256 `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b`,
ตรงกับ verifier ก่อน/หลังของ `RE-095` เอง) แถว `n_ID=156`: `s_ROLE_GRAPHIC=COLUMBUS_0`,
`s_QUEST_BEGIN=111;998;**3021**;3205;7062;7063` — **ไม่มี 3023** แถว `n_ID=36`: level 35,
`s_QUEST_BEGIN=121;**3023**;3207` — มี 3023 จริง คนละแถวกัน

`QUESTDATA_TH__QUEST.tsv` (sha256 `cc9927286def2bda166c320a2dddd16f5457eb4579ce5207a3d76758707527bd`)
แถว `n_ID=3021`: `n_TYPE=20`, `s_LUASCRIPT=Q_TELEPORT1`, `n_VARI_2=**17**` แถว `n_ID=3023`: `n_VARI_2=19`
(ตรงกับที่ RE-095 เจอ)

`CONSTDATA_TH__SCENE_NAME.tsv` (sha256 `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b`)
แถว `n_ID=17`: `s_MODLE_ID=Bg1001`, `n_SCENE_TYPE=4` (ตระกูลทะเล), `n_CAMERA_TYPE=1` — สอดคล้องกับแผน M2
(คุย Columbus -> เทเลพอร์ตไปแมพทะเล -> เป็นเรือ) เทียบเท่ากับ scene 19/Bg1003 ที่ RE-095 เจอสำหรับ MOBS 36
(คนละ NPC คนละปลายทาง แต่เป็นแพทเทิร์นเดียวกัน — สอดคล้องกันว่ากลไก Q_TELEPORT1 ใช้ `n_VARI_2` เป็น
scene_id จริงทั้งคู่)

**สรุปตาราง:**

| | MOBS n_ID | ที่อยู่ | quest | ปลายทาง | ยืนยันโดย |
|---|---|---|---|---|---|
| Port Royal Columbus (จริง) | **156** | bg0001 index **1** | **3021** | scene **17**/Bg1001 | 0925/0950 (index) + รอบนี้ (quest/scene, re-derive จากตาราง) |
| Spice Paradise Columbus (คนละตัว) | 36 | (คนละเกาะ) | 3023 | scene 19/Bg1003 | `RE-095` (ของเดิม, ยังถูกต้องอยู่ ไม่ได้ถูกแก้) |

`RE-095` **ไม่ผิด** และไม่ต้องเปิดใหม่ — ผิดเฉพาะการเอาผลของ RE-095 (MOBS 36) ไปแปะให้ MOBS 156 ในใบ 18:30

## CORE-REQUEST (บรรทัดเดียวสำหรับ runtime.py — chief ต่อสายรอบหน้า)

ต่อสาย NPCConversation op1 สำหรับ MOBS n_ID 156 (Columbus, bg0001 placement index 1) ให้ dispatch quest
3021 (ไม่ใช่ 3023) เมื่อเควสต์จบ: bind `CGCVehicleModule`/`CVehicleAttr` เข้ากับ actor เดิมของผู้เล่น (ไม่
สร้าง actor ใหม่ ตาม RE-085) แล้วย้ายผู้เล่นไป scene_id 17 (Bg1001) ผ่าน `TeleportVital`/`ForcePos` —
ส่วนการเทียบท่าที่เกาะ (`NavigationEx_AddSurveyDataVtial`/`EnterInstanceVital`) และหน้าต่างยืนยันกัปตัน
(`NavigationEx_RequestSurveyVtial`) มีสเปกครบแล้วจาก RE-086/RE-087 — ไม่อยู่ในขอบเขตจดหมายนี้

## ของที่ยังไม่ปิด (ไม่ใช่ตัวบล็อก แค่ของที่ควรรู้)

quest 3021 สำหรับ MOBS 156 ยืนยันแค่ชั้น [STATIC] (ตาราง gamedata) เท่านั้น — ยังไม่มีใครรัน wire capture
สไตล์ `RE-095` (ที่ยืนยัน descriptor byte `+0x10`/`+0x12` จริงบน image) ให้กับเควสต์ 3021 เลย มีแต่ของ 3023
(ของ MOBS 36) เสนอเปิดใบถัดจาก `RE-100` (grep ยืนยันเลขก่อนเปิดตามกติกาไฟล์) ชื่อประมาณ
`NPCCONVERSATION-COLUMBUS-156-QUESTID-3021-WIRE-CONFIRM-001` ให้ RE runner รันแบบเดียวกับ RE-095 แต่เจาะ
MOBS 156/quest 3021 แทน — **ไม่ใช่ตัวบล็อกงานที่เขียนไว้ข้างบน** ส่วนที่มั่นแล้วเริ่มต่อสายได้เลย ส่วนนี้เป็น
double-check ระดับ wire เพิ่มเติม

## ไม่ได้ทำ BUILD-002 (default scene_id=278) ตามคำสั่งอัตโนมัติของรอบ

คำสั่งอัตโนมัติของรอบนี้มีข้อ "BUILD-002 = default scene_id to 278" — **ไม่ทำ** เพราะถูกบล็อกไว้แล้วโดยคำ
ตัดสินสองใบ: `notes_to_chief/20260826_2147_COO-DECISION-BUILD-002-scene278-stays-blocked.md` และ
`notes_to_chief/20260827_0245_COO-DECISION-BUILD-002-scene278-stays-off-1600-1645-affirmed.md` (ทั้งคู่ยืน
ยันคำเจ้าของ 1600 ว่า 278 เป็นแค่เวทีเทส ไม่ใช่เกณฑ์ M2) รอบนี้ทำงาน M2 จริงที่เจ้าของอนุมัติแล้วแทน
(Columbus -> quest 3021 -> scene 17) ตามที่ chief ขอไว้ในใบ 18:30 เอง (① "lane A เขียนแผนต่อสายในรอบถัดไป
ของตัวเอง")

## ของที่สร้างรอบนี้ (`pirate-force-server`)

- `scenarios/world_travel_gates_001.json` — แก้ข้อความ provenance ของ gate `port_royal_columbus_departure`
  (ไม่แตะตัวเลข operative `centre`/`to_scene_id` — `tests/test_world_travel_gate.py` ปักไว้แน่นแล้วว่า
  centre ต้องเท่ากับ census index 65 พอดี ไฟล์นั้นอยู่นอกโซนเขียนของรอบนี้) เพิ่ม strike-through +
  correction เต็มไว้ในฟิลด์ provenance ตาม convention เดิมของไฟล์
- `scenarios/world_scene_registry_001.json` — เพิ่ม destination ใหม่ `n_id: 17` (`Bg1001`) พร้อม
  `table_row`/sha256/spawn=null (ติดป้าย unknown, ไม่ปั้นพิกัด) ตาม pattern เดิมของไฟล์เป๊ะ
- `tests/test_world_columbus_m2_crosswalk.py` (ใหม่) — pin 7 เทส กัน regression ย้อนกลับไป 3023/19 —
  รัน `pytest` แล้ว **7 passed**

**เทสทั้งชุดที่ยังไม่ error จาก missing deps ในนี้ (capstone/tools ไม่มีใน sandbox นี้, ไม่เกี่ยวรอบนี้):
3190 passed, 194 skipped, 2 failed** — 2 ที่พังคือ `tests/test_world_scene_travel.py` (นอกโซนเขียนของ
รอบนี้ ไม่ได้แก้เอง) เพราะ destination ตัวที่ 5 ที่เพิ่มเข้าไปทำให้สอง positional-index assumption ของ
เทสเดิมเลื่อน — รายละเอียด/บรรทัดที่ต้องแก้อยู่ใน `rounds/A_20260827_1052_columbus_m2_identity_correction.md`
ของรอบนี้ ทั้งสองเทสมี docstring ของตัวเองที่รองรับการอัปเดตเมื่อ "มี decision รองรับ" ซึ่งรอบนี้มี

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ยังไม่มีอะไรต่างบนหน้าจอผู้เล่นรอบนี้ — รอบนี้แก้ "แผนที่ข้อเท็จจริง" ที่รอบหน้าของ chief ต้องใช้ต่อสาย
NPCConversation จริง ไม่ใช่รอบที่แตะ runtime.py เอง (ตามกฎที่ runtime.py เป็นของ chief คนเดียว)

## nonclaims

- ไม่ได้อ้างว่า `RE-095` ผิด — MOBS 36/quest 3023/scene 19 ยังถูกต้องสำหรับ NPC นั้น (Spice Paradise)
- ไม่ได้อ้างว่า quest 3021 ยืนยันระดับ wire แล้ว — [STATIC] เท่านั้น เปิดใบขอไว้ด้านบน
- ไม่ได้อ้างว่ารู้จุด player-arrival spawn ของ scene 17 — `Bg1001.placements.tsv` มีแค่ 8 แถว monster
  spawn ไม่มี player marker เลย ติดป้าย unknown ไว้ตรง ๆ ใน `world_scene_registry_001.json`
- ไม่ได้แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`

## pf-adversary pass (ก่อน commit) — 3 ข้อพบ ทั้งหมดแก้แล้ว

1. **[HIGH, แก้แล้ว]** ไฟล์เทสใหม่ (`test_world_columbus_m2_crosswalk.py`) ใช้
   `@BRIDGE_GAMEDATA.skip_unless_present()` ทั้งคลาส แต่ตอนแรกไม่ได้เพิ่ม entry ใน
   `docs/PYTEST_SKIP_PINS.json` — ถ้าปล่อยแบบนี้ Windows gate (เช็คเอาต์รีโปเดียว ไม่มี `pf_bridge` ข้าง ๆ)
   จะเห็น 7 เทส skip โดยไม่มี pin รองรับ แล้ว `skip_census` step จะแดง เคยเกิดแบบนี้มาก่อนสองรอบแล้ว
   (`ctflxc`, `2vxlx2`) — เพิ่ม entry แล้ว รันเทส `test_pytest_precondition_census.py` ผ่านหมด
2. **[MEDIUM, แก้แล้ว]** ข้อความเดิมเขียนว่า index 1 = MOBS 156 "ยืนยันสองรอบ" ราวกับเป็นสอง derivation
   อิสระ — จริง ๆ เป็นการยืนยันซ้ำในเซสชัน attended ต่อเนื่องเดียวกัน (0925 → 0950) และเลขนี้เคยขยับมาแล้ว
   ครั้งหนึ่งในวันเดียวกัน (`RE-097` เคยเสนอ index 0 มาก่อน) แก้ข้อความใน `world_travel_gates_001.json`
   และเทสให้บอกตรง ๆ ว่านี่คือคำยืนยันจากเจ้าของ (testimony) ไม่ใช่ table crosswalk — ถ้าขยับอีกครั้ง
   MOBS 156 → quest 3021 → scene 17 ยังจริงอยู่ (วัดจากตาราง) แต่พิกัดที่ควรผูก trigger จะเปลี่ยน
3. **[LOW, แก้แล้ว]** ป้าย "Spice Paradise's Columbus" สำหรับ MOBS 36 เขียนเป็นข้อเท็จจริงเฉย ๆ ทั้งที่จริง
   เป็นการอ่านแพทเทิร์นจากใบ `0500` (ใบนั้นเองบอกว่า "ยังเป็นการอ่านรูปแบบ ไม่ใช่ field") — แก้ทั้งสามที่ที่
   อ้างถึงให้ติดป้าย HYPOTHESIS ชัดเจน ไม่กระทบข้อสรุปหลัก (36 ≠ 156, 3023 ≠ 3021 ยังจริงไม่ว่า 36 จะเป็น
   เกาะไหน)

รันเทสทั้งชุดซ้ำหลังแก้: `3299 passed, 208 skipped, 17 errors` (errors = capstone/tools ขาดใน sandbox นี้
เหมือนเดิม ไม่เกี่ยวรอบนี้) — 0 failed

— สาย A · WORLD

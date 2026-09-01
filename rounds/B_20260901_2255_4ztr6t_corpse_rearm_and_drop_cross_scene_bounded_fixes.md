# Round B_20260901_2255 (branch 4ztr6t) — LANE-B (COMBAT), scheduled round

Time started: 2026-09-01T22:5x+07:00 · finished: 2026-09-01T23:0x+07:00 (measured, `TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ P-1/P-2/P-3 โดยตรง** — NOW.md ยังห้าม GT-146 และใบเทสตีมอนทุกใบจนกว่า P-1/P-2 จะปิด
และ BUILD-004/005/006 ยังถูกพักตาม PANYA-ORDER 20260901_0215 เหมือนเดิม

**แต่บริโภคจดหมายถึง LANE-B ที่ยังไม่บริโภค** —
`notes_to_chief/20260901_2148_COO-DECISION-corpse-rearm-and-cross-scene-drop-bounded-fix-to-lane-b.md`
(21:48+07:00, ยังไม่มี `.CONSUMED.txt` ตอนต้นรอบ) อนุมัติสองข้อเสนอ bounded ของ
`CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md` ให้ LANE-B ลงมือ **ทันที ไม่ต้องรอ
P-1/P-2 ปิดก่อน** เพราะจดหมายเองระบุชัดว่านี่คือ "แก้บั๊กใต้ฝากระโปรง ไม่ใช่ GT-146/ใบเทสตีมอน"
— จึงเป็นรอบที่มีของจริงให้สร้าง ไม่ใช่รอบว่างที่ห้า

## ต้นรอบ — เช็คมณ mailbox

- ค้นหา `ADDRESSEE: LANE-B` ทั่ว `notes_to_chief/` — พบใบ `2148` ค้างอยู่ (ไม่มี `.CONSUMED.txt`
  คู่กัน) ใบ `1747` (CHIEF-TO-LANE-B re157 job2) บริโภคไปแล้วตั้งแต่รอบก่อน (มี stub) — ข้าม
- heartbeat ล่าสุด `_BRIDGE_HEARTBEAT.txt` = 2026-09-01T22:30:04+07:00 เทียบรอบนี้ 22:55+07:00
  (ห่าง 25 นาที ผ่านเกณฑ์ 60 นาที)
- ไม่มี CLAIM ของสาย B ที่ต้องหมดอายุ/ปลด — งานนี้ COO มอบให้ LANE-B โดยตรงในจดหมาย ไม่ใช่
  ticket ที่หลายสายแย่งกันได้ จึงไม่ต้องวาง CLAIM ก่อนลงมือ

## สิ่งที่ CODEX_URGENT ยืนยัน (อ่านเพื่อทำงาน ไม่ใช่เพื่อวิจัยต่อ)

1. **ศพเก่าถูก re-arm ทุกครั้งที่มีศพใหม่** — `dead_timer` เป็นค่าเดียวที่
   `repopulation_entries`/`full_roster_override` ใช้กับทุกแถวที่ตายในทะเบียน ปลอดภัยแค่ตอนตายได้
   ทีละตัว (docstring เดิม "ONE-CORPSE LIMIT") ซึ่งไม่จริงแล้ว — `WIDENING_RULINGS` ปัจจุบันให้
   bg0001 เองมี 4 mob จริงที่ตายพร้อมกันได้ภายใต้ ruling เดียว (template 916)
2. **Drop ข้ามฉากได้จาก ledger เดียวกัน** — `DropLedger` ไม่มี scene ในคีย์ และทุกคิลส่ง live
   ledger ทั้งก้อน ของที่ยังอยู่ในฉาก A จึงติดไปกับ publication ของฉาก B ได้

## ที่สร้างจริง (repo pirate-force-server, branch `claude/zen-einstein-4ztr6t`)

**1 commit** (`b476903`), 7 ไฟล์:

### ข้อ 1 — corpse re-arm fix
- `src/pirateforce_foundation/mob_death.py` — เพิ่ม `transitioning=(scene, actor_identity)`
  (opt-in, default `None` = พฤติกรรมเดิมเป๊ะ) ใน `repopulation_entries`/`full_roster_override`/
  `hostile_census_frames` แถวที่ระบุใน `transitioning` เท่านั้นได้ `dead_timer`; แถวศพเก่าอื่น ๆ
  ล็อกที่ `DEAD_TIMER_SECONDS` เสมอ เพิ่ม refusal ใหม่ `REFUSE_TRANSITIONING_NOT_A_DEAD_ROW`
  (ตั้งชื่อผิดแถว = ปฏิเสธ ไม่ fallback เงียบ ๆ กลับไปพฤติกรรมเดิม) ขีดฆ่า docstring
  "ONE-CORPSE LIMIT" เดิม (ไม่ลบ ตามธรรมเนียมไฟล์)
- `src/pirateforce_foundation/mob_scene_recompose.py` — ต่อ `transitioning` ผ่าน
  `recompose_frames` → `_compose` → ทั้งสองเส้นทาง (scene-1 delegated / scene-2 bg0002)
- `src/pirateforce_foundation/diag_multi_object_wiring.py` — ต่อ `transitioning` ผ่าน
  `hostile_census_frames` ของโมดูลนี้ (composer ที่แท้จริงของฉาก 1)

### ข้อ 2 — drop cross-scene fix
- `src/pirateforce_foundation/mob_loot.py` — ฟังก์ชันใหม่ `reconcile_scene_transition(ledger)`
  (pure function, รูปแบบเดียวกับ `take_drop`) + เมธอด `DropLedgerCell.reconcile_scene_transition()`
  (ล้างทุกของที่ยังอยู่บนพื้น เก็บ `issued_through`/`looted` ไว้เหมือนเดิม เพราะสองอย่างนี้ไม่ใช่
  fact ของฉาก) เพิ่ม step 6 ใน `MOB_LOOT_WIRING` บอกจุดที่ chief ต้องเรียก
- `scenarios/combat_loot_001.json` — regen อัตโนมัติจาก `mob_loot.pin_document()` (1 บรรทัดขยับ
  เพราะ `pin_document` ฝัง `MOB_LOOT_WIRING` ทั้งก้อน ไม่ใช่การแก้มือ)

### เทส
- `tests/test_mob_death.py` — 4 เทสใหม่: pin บั๊กเดิม (`transitioning=None` ยัง re-arm),
  พิสูจน์ fix (`transitioning=` ตั้งชื่อถูกแถวเดียว), refusal เมื่อชื่อแถวที่ไม่ตาย, end-to-end ผ่าน
  `hostile_census_frames` ไม่ raise ใช้มอนจริง 2 ตัวจาก roster bg0001 เอง (template 916 ทั้งคู่)
  ไม่ต้องใช้ stand-in fixture
- `tests/test_mob_loot.py` — 7 เทสใหม่: clear ทุกแถว, คง `issued_through`/`looted`, end-to-end
  ฉาก A → reconcile → ฉาก B คิล → publication ไม่มี key/position จาก A, no-op บน cell ว่าง,
  generation +1 เดียว, module function ตรงกับ cell method, refuse non-ledger, wiring note
  มีข้อความจุดเรียกใหม่

## เทสรวม (pirate-force-server, ทั้งรีโป)

`6565 passed, 327 skipped, 0 failed` (`python3 -m pytest tests/` เต็มรีโป รวมเทสใหม่ 11 ใบ)

## pf-adversary

**ไม่ได้เรียก** — เซสชันนี้ไม่มี Agent/Task tool ให้เรียก pf-adversary agent (มีแค่
Read/Grep/Glob/Bash/Edit/Write) ตรวจสอบด้วยมือแทน: อ่านทุกจุดเรียกที่ถูกแก้ (grep หาทุก call
site ของ `full_roster_override`/`hostile_census_frames`/`repopulation_entries` ทั่ว `src/`),
รันเทสเดิมทั้งหมดซ้ำ (ไม่ใช่แค่เทสใหม่) ยืนยันไม่มี call site เดิมพังเพราะ default ไม่เปลี่ยน
และตรวจ `scenarios/combat_loot_001.json` diff มีแค่ 1 บรรทัด (ข้อความ wiring note) ไม่ใช่การ
เปลี่ยน schema **ทำเครื่องหมายไว้ชัดว่ายังไม่ผ่าน pf-adversary จริง** — เขต src/ นี้เป็นคอมแบต
ความเสี่ยงสูง สมควรให้อีก session/รอบที่มี Agent tool ตรวจซ้ำก่อนถือว่าปิดสนิท

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่มีอะไรต่างบนจอ** — ทั้งสองฟิกซ์เป็น library-level ใน `src/pirateforce_foundation/` ล้วน ๆ
จุดเรียกจริงที่จะทำให้ผู้เล่นเห็นผล (ส่ง `transitioning=` เข้า `hostile_census_frames` สองจุดที่
`runtime.py:4743-4760`, เรียก `cell.reconcile_scene_transition()` ตรงจุด scene-sync) อยู่ใน
`runtime.py` ซึ่งเป็นไฟล์ของ chief เท่านั้น — ดู CORE-REQUEST ท้ายรอบนี้ จนกว่าจะต่อสาย
ผู้เล่นจะยังเห็นบั๊กเดิมทั้งสองข้อเหมือนเมื่อวาน (ศพเก่ากะพริบกลับเป็น dying เมื่อมีศพใหม่, ของอาจ
ติดข้ามฉากได้) — สิ่งที่เปลี่ยนคือ**กลไกแก้พร้อมใช้แล้วในซอร์ส รอต่อสายเท่านั้น**

## จดหมาย/CLAIM ที่เปิด/บริโภครอบนี้

- บริโภค `20260901_2148_COO-DECISION-corpse-rearm-and-cross-scene-drop-bounded-fix-to-lane-b.md`
  (เขียน `.CONSUMED.txt` แล้ว)
- ไม่มี CLAIM ที่ต้องวาง (งานมอบตรงจาก COO ไม่ใช่ ticket แย่งกัน)
- เปิดใบให้สาย C: ไม่มี — ไม่มีคำถามเปิดที่ต้องวิจัยเพิ่ม ข้อ 3 (pickup/removal) ของ CODEX_URGENT
  ยังเปิดไว้ตามเดิม (นอกสโคปที่ COO อนุมัติรอบนี้) ไม่ใช่ของค้างของ LANE-B

## จบรอบ

pirate-force-server: push แล้ว (`b476903`, branch `claude/zen-einstein-4ztr6t`, ยังไม่มี PR —
เซสชันนี้ commit/push เท่านั้น ไม่เปิด/จัดการ PR เอง)

pf_bridge: กำลัง push รอบนี้ (ไฟล์รอบนี้ + `.CONSUMED.txt` + `LANE-B-STATUS` แนบท้าย)

## ADDENDUM 2026-09-01T23:21+07:00 — pf-adversary จริง (ผ่าน coordinator) พบจุดบั๊ก, แก้แล้ว

coordinator รัน pf-adversary จริงกับ `b476903` (medium-high confidence) พบบั๊กจริงหนึ่งจุดใน
`REFUSE_TRANSITIONING_NOT_A_DEAD_ROW` (`mob_death.repopulation_entries`): เช็คเดิม
`register.is_dead(transitioning[1], transitioning[0])` ตรวจกับ**ทะเบียนทั้งก้อน** ไม่ใช่กับ
roster ที่ call นี้ได้รับจริง เพราะ `DeathRegister` เก็บศพข้ามฉากไว้ตามดีไซน์ — `transitioning`
ที่ชี้ไปแถวศพจริงแต่ **คนละฉาก/roster** จึงผ่านเงื่อนไขเงียบ ๆ แล้วทำให้**ทุกแถวศพในการ compose
จริง (รวมแถวจริงที่กำลัง compose)** ตกกลับไปที่ `DEAD_TIMER_SECONDS` แทนที่จะใช้ `dead_timer`
ที่ผู้เรียกตั้งใจส่ง (เช่น `DYING_TIMER_SECONDS`) — ตรงกับรูปแบบ caller-mistake ที่ docstring เดิม
อ้างว่าจับได้ แต่จับไม่ได้จริง

**แก้แล้ว**: ย้าย `roster_keys = set((m.scene, m.actor_identity) for m in roster)` ขึ้นมาก่อนเช็ค
`transitioning`, เช็คใหม่ต้องผ่านทั้งสองเงื่อนไข — `transitioning in roster_keys` **และ**
`register.is_dead(...)` — ไม่ใช่แค่ข้อหลังข้อเดียว เพิ่มเทส
`test_transitioning_naming_a_dead_row_from_a_foreign_scenes_roster_is_refused` (มอนจริงตาย 2
ฉาก: bg0001 กับ Bg0002 ใน register เดียวกัน, ตั้ง `transitioning` ชี้ไปแถว Bg0002 ตอน compose
roster bg0001 ต้องถูกปฏิเสธ)

**สองจุดรอง** ที่ pf-adversary ชี้ก็แก้ในรอบเดียวกัน:
1. `mob_scene_recompose.SCENE_RECOMPOSE_WIRING` เพิ่ม item (4) บอกจุดต่อสาย `transitioning=` ให้
   chief ตรง ๆ ในซอร์ส (เดิมมีแค่ commit message กับจดหมาย pf_bridge)
2. strengthen เทสที่อ่อนสองใบให้ตรวจ **wire bytes จริงต่อแถว** แทนแค่ `len(frame) > 0`:
   `test_transitioning_reaches_hostile_census_frames_with_correct_per_row_wire_bytes`
   (`tests/test_mob_death.py`) และเทสใหม่ที่ชั้น `recompose_frames` (เส้นทางจริงที่ chief จะต่อสาย)
   `test_scene_1_transitioning_reaches_the_live_composer_and_only_that_row_moves`
   (`tests/test_mob_scene_recompose.py`)

ไฟล์ที่แตะเพิ่ม: `src/pirateforce_foundation/mob_death.py`,
`src/pirateforce_foundation/mob_scene_recompose.py`, `tests/test_mob_death.py`,
`tests/test_mob_scene_recompose.py` — เทสรวมทั้งรีโปรันซ้ำก่อน push (ดูจดหมายแยกถึง coordinator
สำหรับ commit SHA ใหม่และตัวเลขผลเทส)

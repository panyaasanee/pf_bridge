# LANE-UI round `avt7pt` -- 2026-09-06T07:51+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: ว่างทั้งคู่ -- เปิดคลาม `pf_bridge#1449`
  (`[LANE-UI] round avt7pt: claim`) จากกิ่ง `claude/peaceful-pascal-avt7pt` (pf_bridge) และ
  `claude/inspiring-feynman-avt7pt` (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้
  เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ -- ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI, ยังไม่ consumed ก่อนรอบนี้)
- `20260906_0745_COO-DECISION-ui0631-*` -- ตอบใบ `0631` ของรอบก่อน (`g1ss4s`): ทางเลือก 1 ยืน
  (`R364` ข้อ 2 มาก่อนเกต `bridgesize` บนไฟล์ที่เกินเพดานอยู่ก่อนแล้ว) -- ไม่ต้อง revert สอง
  บล็อก `ATTENDED:` ของ `GT-251`/`GT-262` · `bridgesize` แดงบน `GAME_TEST_QUEUE.md` เป็น
  `KNOWN_RED_MAIN` ตั้งแต่รอบนี้ (ขอบเขตแคบ: เฉพาะโตจากบล็อก `ATTENDED:`/บรรทัดปิด `CANCELLED`)
  · **ไม่มีงานเพิ่มสำหรับ LANE-UI จากใบนี้** -- เดินงานตาม `NOW.md` ต่อ (`#860`/GT-184/186 หลัง
  RE-266) -- consumed แล้ว, `.CONSUMED.txt` วางแล้ว (ไม่ต้องตอบใบนี้)

## AGENTS.md section 7 -- อ่านครบรอบนี้
ไม่มีกฎใหม่ที่กระทบงานรอบนี้โดยตรง นอกจาก `KNOWN_RED_MAIN` เรื่อง `bridgesize` ที่อ่านผ่านใบ
ข้างบนแล้ว -- ไม่กระทบรอบนี้เพราะรอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`

## งานสำรอง -- ทำรอบนี้ (งานหลัก 4 ข้อของคิวเริ่มต้นยังติดหมดเหมือนสองรอบก่อน ตรวจซ้ำ)
1. UI-B logout wiring: ยังไม่มีอะไรให้ LANE-UI ทำเพิ่ม (CORE-REQUEST ค้างรอ chief เหมือนเดิม)
2. UI-A back-to-charselect: `GT-184`/`GT-186` ยัง `BLOCKED-ON-RE-266` ใน `GAME_TEST_QUEUE.md` จริง
   (grep ยืนยันแล้ว, ไม่เปลี่ยนจากสองรอบก่อน)
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยน
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน

⇒ หยิบงานสำรองข้อ 2 (ฟังก์ชันถัดไปที่ layout รู้แล้ว) ตามแผนรอบก่อน (`g1ss4s`): **`Pets_` กลุ่ม**
(16 คลาสในสารบัญ) -- อ่าน `external/PF_SERIALIZER_FIELDS.tsv` ทุกแถวของ `Pets_`
(`awk -F'\t' '$1 ~ /^Pets_/'`, 174 แถว) ก่อนเขียนโค้ด นับแถว `CALL_UNCLASSIFIED`/`PE_IMPORT_*`/
`JUMP_UNCLASSIFIED`/`ATOMIC_*`/`DYNAMIC_INTERLOCKED_*` ต่อคลาส:
- `Pets_ChangePetEquipmentVital` 16/34 แถวเสีย -- ข้าม
- `Pets_SetPetAIVital` 10/18 แถวเสีย -- ข้าม
- `Pets_SetPetSkillVital` 16/32 แถวเสีย -- ข้าม
- `Pets_UpdateLearnedPetSkillVital` 10/12 แถวเสีย -- ข้าม
- `Pets_UpdatePetsDataVital` 10/12 แถวเสีย -- ข้าม
- `Pets_UpdatePetsMegringDataVital` 10/12 แถวเสีย -- ข้าม

เหลือ **10 คลาสที่แท็กครบทุกฟิลด์** (`Pets_SummonPetVital` `0x4CEC` · `Pets_UnsummonPetVital`
`0x5E3C` · `Pets_UpdatePetPropertyVital` `0x9B50` · `Pets_RestorePetAmityVital` `0x83B5` ·
`Pets_NotifySailorDeadVital` `0x8B12` · `Pets_MergePetsVital` `0x4C4D` · `Pets_MergePetsResultVital`
`0x845C` · `Pets_ClaimPetsMegringItemVital` `0xB96F` · `Pets_LearnPetSkillVital` `0x6E55` ·
`Pets_UpdateSummonPetsTimeOutVital` `0xE28A`) -- vital id มาจาก
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (grep `Pets_`), ไม่ใช่จาก serializer tsv (ไม่มี
คอลัมน์ id)

`Pets_MergePetsVital`'s field3/field4 มี `field_offset` เป็น `PHI(OBJ+0x18|REG(edi)+0x8)` และ
`PHI(OBJ|REG(ebx))+0x38` (compiler merge สองจุดเรียก) แทนที่จะเป็น `+0xNN` ตรง ๆ -- ตรวจก่อนรวม
เข้าโมดูล: `field_offset` เป็น provenance ของ client object เท่านั้น ไม่ใช่ wire offset (ตาม
`ui_social_wire.py` docstring) -- tag/len ยังเป็น `0x32`/8 ปกติทั้งคู่ ไม่กระทบ wire shape ->
รวมเข้าโมดูลได้ตามปกติ (ยืนยันซ้ำโดย adversary ด้วย precedent row `CNSS_BoardcastToSpecifiedActorVtial`)

ผลลัพธ์ (`pirate-force-server`): `src/pirateforce_foundation/ui_pets_wire.py` (ใหม่, 10 คลาส) +
`tests/test_ui_pets_wire.py` (ใหม่, 51 เทส + 20 subtests) + อัปเดต `docs/UI_LANE.md` (แถวใหม่
`Pets`, ลบ `Pets_` ออกจากรายการ NOT YET ITEMIZED, เพิ่มย่อหน้า nonclaim). ไม่ต่อสายเข้า
`runtime.py`/`vital_walk.py` -- pure wire shape เท่านั้น เหมือนโมดูลพี่น้องทุกตัว.

grep ตาม `AGENTS.md` section 7 ก่อนเขียนโค้ด: ทั้ง 10 ชื่อคลาส 0 hit ใน `CLIENT_RE_QUEUE.md`/
`GAME_TEST_QUEUE.md` -- มีแค่ census tables ใน `notes_to_chief/reference_codex_attr/` (คาดไว้แล้ว
ไม่ใช่ใบเปิดค้าง)

## ADVERSARY -- คืนผลแล้วรอบนี้ (ไม่ใช่ PENDING)
สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานฝั่ง `ui_pets_wire.py` (ครั้งที่ 1/2): re-derive field
order/tag/len ทั้ง 10 คลาสจาก TSV เอง (ไม่เชื่อ docstring) ตรงกันหมด, ตรวจ vital id ทั้ง 10 ตรงกับ
registry, ยืนยันเหตุผลข้อยกเว้น 6 คลาสตรงกับตัวเลขที่นับไว้เป๊ะ, grep ยืนยันไม่มี collision กับ
โมดูลอื่นและไม่ได้ต่อสายเข้า `runtime.py`/`vital_walk.py`, มิวเทตทดสอบ (สลับลำดับ field3/field4 ของ
`MergePetsVital` และถอด `require_exhausted` ออกจาก `NotifySailorDeadVital` decoder ใน worktree
แยก) เทสจับได้ทั้งคู่, ตรวจ fail-closed ครบทั้ง 10 คลาสด้วยมือ, ตรวจเหตุผล PHI-offset เทียบกับแถว
ตัวอย่างอื่นใน TSV เดียวกัน -- **พบข้อบกพร่องจริงหนึ่งข้อ**: ค่าคงที่ `*_VITAL_ID` ทั้ง 10 ตัวไม่มี
เทสยืนยันเลย (มิวเทต `PETS_LEARN_PET_SKILL_VITAL_ID` จาก `0x6E55` เป็น `0x6E56` แล้วเทสเดิมทั้ง 41
ตัวยังผ่านหมด) -- แก้แล้วในรอบเดียวกัน (เพิ่มคลาส `VitalIdTests` ปักหมุดทั้ง 10 ค่าเทียบ registry
ตรง ๆ, ตามแพทเทิร์นเดิมที่ `test_gm_activity_cheat_code_wire.py` ใช้อยู่แล้ว) ไม่ต้องเรียก
adversary รอบสองเพราะเป็นการเพิ่มเทสปักหมุด ไม่ใช่ตรรกะโค้ดใหม่

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_pets_wire.py -q` = 51 passed, 20 subtests passed
`PYTHONPATH=src python3 -m pytest tests/ -q` (ชุดเต็มบนต้นไม้ merge `origin/main` ed2d8d4 แล้ว
เป็น commit สุดท้ายจริง) = 12014 passed, 365 skipped, 23130 subtests passed, 0 failed

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`:
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS · `[branch]` PASS ทั้งสองรีโป ·
`[bridgesize]` PASS (รอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`AGENTS.md`/
`CHIEF_CONTINUATION.md`, `NOW.md` ยังใต้เพดาน) · `[scoreboard-manual]` PASS ·
`[prbody]` PASS ตรวจ PR body ฝั่งเซิร์ฟเวอร์แล้ว: 1 บรรทัด marker เป๊ะ

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `[LANE-UI] round avt7pt: claim` (`#1449`) กิ่ง `claude/peaceful-pascal-avt7pt` --
  ลบ `_claim.md`, `.CONSUMED.txt`/`consumed/` ของ `0745`, ไฟล์รอบนี้แทน `_claim.md`
- `pirate-force-server`: PR `#901` (`[LANE-UI] Pets_ wire module: 10 fully-tagged classes, wire
  shape only`) กิ่ง `claude/inspiring-feynman-avt7pt`, ไม่ draft, marker `PF-AUTOMERGE: v4` ยืนยัน
  แล้วด้วย GET -- `ui_pets_wire.py` + `test_ui_pets_wire.py` + `docs/UI_LANE.md`
- เลขใบใหม่รอบนี้: ไม่มี (ไม่ได้เปิด GT/RE ใหม่ -- โมดูลนี้ยังไม่มีใบเทสเพราะไม่ต่อสายเข้าเกม)

## nonclaims
① `ui_pets_wire.py` ไม่อ้างความหมายฟิลด์ใด ๆ (pet id/owner id/amity/slot ฯลฯ) --
`proven_semantics` ยัง `UNKNOWN` ทุกแถว
② ไม่ต่อสาย `ui_pets_wire.py` เข้า `runtime.py`/`vital_walk.py` -- ของ CORE-REQUEST แยก
③ ไม่อ้างว่าทั้ง 10 คลาสเคยถูกเห็นบนสายจริง -- `PF_FIELD_VALIDATION.tsv` เป็น `NOT_OBSERVED`/0
เฟรมทั้งสองทิศทางทุกคลาส
④ ไม่อ้างว่า `PHI(...)` ของ `Pets_MergePetsVital` ถูกไข (resolve) เป็นที่อยู่เดียว -- อ้างแค่ว่า
ความกำกวมนั้นไม่กระทบ wire shape ซึ่งเป็นขอบเขตเดียวของโมดูลนี้
⑤ ไม่อ้างว่าใบ `0745` (COO-DECISION เรื่อง bridgesize) มีงานเพิ่มให้ LANE-UI -- ใบระบุเองว่าไม่มี

## รอบหน้าทำอะไร
1. เช็ค `GT-184`/`GT-186` ว่า chief ลง `ATTENDED:`/เปลี่ยนหัวใบหรือยัง (ยังไม่ลงล่าสุด `g1ss4s`)
2. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: `Express_`/`CollectionObj_`/
   `KnowledgeGuru_`/`HitParade_` (ตรวจ `CALL_UNCLASSIFIED` ก่อนเขียนโค้ดเสมอ ตามบทเรียนสามรอบติด)
3. `KNOWN_RED_MAIN` เรื่อง `bridgesize` บน `GAME_TEST_QUEUE.md` ไม่ใช่ของ LANE-UI แก้ (chief ใบ
   `0747`) -- แค่รู้ไว้ว่าไม่ต้องเขียนใบถามซ้ำถ้ารอบหน้าต้องเติม `ATTENDED:` อะไรอีก

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (ของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมสัตว์เลี้ยง (pets) 10 ชนิด (เรียกออก/เรียกกลับ/อัปเดต
คุณสมบัติ/ฟื้นฟูความสนิทสนม/แจ้งกะลาสีตาย/รวมร่างสัตว์เลี้ยงกับผลลัพธ์/รับไอเทมรวมร่าง/เรียนสกิล
สัตว์เลี้ยง/อัปเดตเวลาหมดอายุ) ฝั่งเซิร์ฟเวอร์เสร็จพร้อมเทส 51 ตัว+20 subtests ผ่านหมด แต่ยังไม่ต่อ
สายเข้าเกมจริง (ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้) | PR `pirate-force-server#901`,
PR `pf_bridge#1449`

-- LANE-UI (round `avt7pt`)

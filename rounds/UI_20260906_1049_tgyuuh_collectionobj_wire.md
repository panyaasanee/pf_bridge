# LANE-UI round `tgyuuh` -- 2026-09-06T10:49+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: ว่างทั้งคู่ -- เปิดคลาม `pf_bridge#1469`
  (`[LANE-UI] round tgyuuh: claim`) จากกิ่ง `claude/peaceful-pascal-tgyuuh` (pf_bridge) และ
  `claude/inspiring-feynman-tgyuuh` (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้
  เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ -- ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI)
- grep `notes_to_chief/*.md` หา `ADDRESSEE: LANE-UI` ซ้ำเอง: ทุกใบมี `.CONSUMED.txt` คู่อยู่แล้ว
  (วนลูปตรวจทุกไฟล์) -- **ไม่มีใบใหม่ให้บริโภครอบนี้** (ตรงกับที่รอบก่อน `x28wjw` เจอ)

## NOW.md -- อ่านสดตอนเริ่มรอบ (09:16 -> ดึงใหม่ 10:49)
ดึงสด `origin/main` ก่อนเริ่ม (HEAD `4db0a24`, ตรวจล่าสุดของ COO เขียนไว้ `2026-09-06 08:47 +07:00`)
-- "รอ Panya ติ๊ก" ว่าง, ไม่มีข้อบังคับใหม่ที่กระทบ LANE-UI โดยตรงนอกจาก R364 ข้อ 2 ซึ่งรอบก่อน
(`x28wjw`) ตรวจสดแล้วพบว่าปิดไปแล้วจริง (`GT-251`/`GT-262` มีบล็อก `ATTENDED:` ครบ) -- ไม่ตรวจซ้ำ
ตามกฎที่รอบก่อนวางไว้ ("เลขค้าง ไม่ใช่ของจริง")

## AGENTS.md section 7 -- อ่านครบรอบนี้
อ่านทั้งหัวข้อ "7. ห้ามทำ -- ไม่มีข้อยกเว้น" ครบ (บรรทัด 85-128) -- ไม่มีกฎใหม่ที่กระทบรอบนี้โดยตรง
นอกจาก `KNOWN_RED_MAIN` เรื่อง `bridgesize` (ไม่กระทบเพราะรอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`) และ
กฎ `manual` row ใน `SCOREBOARD_FACTS.tsv` (ไม่กระทบ ไม่ได้แตะไฟล์นั้น)

## งานหลัก (คิวเริ่มต้นข้อ 1-2) -- ยังติดเหมือนรอบก่อน ตรวจซ้ำสดจากไฟล์ที่ดึงรอบนี้
1. UI-B logout wiring: ยังไม่มีอะไรให้ LANE-UI ทำเพิ่ม (CORE-REQUEST ค้างรอ chief เหมือนเดิม)
2. UI-A back-to-charselect: `GT-184`/`GT-186` ยัง `BLOCKED-ON-RE-266` (grep `docs/UI_LANE.md` ยืนยัน
   สดรอบนี้ ไม่เปลี่ยนจากรอบก่อน)
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยน
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน

⇒ ขยับ NOW/M ข้อไหน: **ไม่ได้ขยับ** M2/P-1/P-2/P-3 -- งานหลักทั้งสี่ข้อยังติดเหมือนเดิม หยิบ
**งานสำรองข้อ 2** ของ `prompts/LANE-UI.md` แทน (ฟังก์ชันที่ layout รู้แล้ว) ต่อจากที่รอบก่อน
(`x28wjw`, ปิด `Express_`) แนะนำไว้ในหัวข้อ "รอบหน้าทำอะไร": `CollectionObj_`/`KnowledgeGuru_`/
`HitParade_`/`Equipment_`

## งานสำรอง -- ทำรอบนี้: `CollectionObj_` wire module (+ ตรวจ `KnowledgeGuru_`/`HitParade_` แล้วตัดออก)

**หมายเหตุ:** ข้าม `Equipment_` ไม่แตะรอบนี้ -- `prompts/COMMON_LANE_ROUND.md`'s แผนที่โปรโตคอลของเกม
ระบุ `Equipment_*` (17) เป็น grep-hint ของ **LANE-DB** โดยตรง (`DB Equipment_* (17)/Storage*/...`)
ต่างจาก `CollectionObj_`/`KnowledgeGuru_`/`HitParade_` ที่ไม่มีสายไหนอ้างเป็นของตัวเองใน grep-hint
นั้น -- เลี่ยงชนเขตเขียนของ LANE-DB โดยไม่จำเป็น

`awk -F'\t' '$1 ~ /^CollectionObj_/'` บน `external/PF_SERIALIZER_FIELDS.tsv` = 50 แถว ครอบคลุม
6 คลาส (ตรงกับสารบัญ "CollectionObj 6"). นับแถวเสีย (`CALL_UNCLASSIFIED`/`PE_IMPORT_*`/
`DYNAMIC_INTERLOCKED_*`/`ATOMIC_*`) ต่อคลาส:

- `CollectionObj_CollectObjVital` (`0xABA4`) 0/10 แถวเสีย -- **ครบ**
- `CollectionObj_GetCollectEffectVital` (`0xF851`) 0/4 แถวเสีย -- **ครบ**
- `CollectionObj_SailorLevelUpRequestVital` (`0x3B06`) 0/6 แถวเสีย -- **ครบ**
- `CollectionObj_SailorLvUpResponseVital` (`0x1B8B`) 0/4 แถวเสีย -- **ครบ**
- `CollectionObj_UpdateCollectEffectVital` (`0x254E`) 10/14 แถวเสีย -- ข้าม
- `CollectionObj_UpdateCollectionObjBagVital` (`0x51A2`) 10/12 แถวเสีย -- ข้าม

W/R รูปร่างเหมือนกันเป๊ะทั้ง 4 คลาสที่ทำ (ตรวจด้วยสคริปต์เทียบ order/tag/len ทั้งสองทิศ) และ
ทุกคลาสมี span_start/span_sha256 เป็นของตัวเอง (ไม่ใช่ shared serializer เหมือนกรณี `Channel_`/
`Express_` ที่เจอมาก่อนหน้านี้) -- ตรวจแล้วไม่มีคู่ไหนใช้ span เดียวกัน

**ตรวจ `KnowledgeGuru_` (5 คลาสในสารบัญ) แล้วพบเหตุผลตัดออกทั้งกลุ่ม:** สคริปต์นับแถวเสียรอบแรก
ให้ผล 0/N แถวเสียทุกคลาส (ดูดี) แต่เมื่อดูรายละเอียดฟิลด์แรกของทั้ง 5 คลาส พบว่าเป็น
`SUBCALL:0x0069F980` -- ไม่ใช่แท็กไบต์จริงและไม่ใช่ untagged-wstring shape ที่รู้แล้ว แต่เป็นการ
เรียกฟังก์ชัน sub-serializer อื่นที่ยังไม่ถอด (เทียบกับ `world_island_dock_table.py` บรรทัด
"W/R 3 SUBCALL 0x005F3490 / 0x005F34D0" ที่บันทึกแท็กตระกูลนี้ไว้เป็น evidence context เท่านั้น
ไม่ใช่ฟิลด์ที่ implement ได้) -- ความหมายเดียวกับ `CALL_UNCLASSIFIED` สำหรับจุดประสงค์ของสายนี้
("ไม่รู้รูปร่างฟิลด์นี้") ⇒ เพิ่ม `SUBCALL:` เข้ารายการ marker เสียของโมดูลนี้ **ทั้ง 5 คลาสของ
`KnowledgeGuru_` จึงไม่ผ่านเกณฑ์ "fully tagged" รอบนี้** ไม่ใช่แค่ "ทัดเยอะไม่พอ" แบบ `Express_`/
`Pets_` ที่เคยเจอ -- ต้องรอ static RE ถอด `0x0069F980` ก่อน

`HitParade_`: `awk` หา `^HitParade_` ใน TSV = **0 แถว** -- ไม่มี layout เลย ต้อง static RE ตั้งแต่ต้น
เหมือนกรณี 4 คลาสของ `Express_` ที่ไม่มีแถวใน TSV เลย

Vital id ทั้ง 6 คลาสของ `CollectionObj_` มาจาก
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (grep `CollectionObj_`), ไม่ใช่จาก serializer tsv
(ไม่มีคอลัมน์ id)

ผลลัพธ์ (`pirate-force-server`): `src/pirateforce_foundation/ui_collectionobj_wire.py` (ใหม่,
4 คลาส) + `tests/test_ui_collectionobj_wire.py` (ใหม่, 22 เทส + 8 subtests) + อัปเดต
`docs/UI_LANE.md` (แถวใหม่ `CollectionObj`, ลบ `CollectionObj_` ออกจากรายการ NOT YET ITEMIZED,
เพิ่มย่อหน้าบันทึกว่าทำไม `KnowledgeGuru_`/`HitParade_` ยังไม่เข้าเกณฑ์). ไม่ต่อสายเข้า
`runtime.py`/`vital_walk.py` -- pure wire shape เท่านั้น เหมือนโมดูลพี่น้องทุกตัว

grep ตาม `AGENTS.md` section 7 ก่อนเขียนโค้ด: ทั้ง 6 ชื่อคลาส `CollectionObj_*` (รวม 2 คลาสที่ข้าม)
0 hit ใน `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/`archive/` -- ไม่มีใบเปิดค้างอ้างถึง grep src/
ยืนยันไม่มีโมดูล `CollectionObj_` มาก่อนในรีโป

## ADVERSARY -- เรียกได้จริงรอบนี้ (ต่างจากสามรอบก่อนที่ `ADVERSARY_UNAVAILABLE`)
เรียก `pf-adversary` ผ่าน Agent tool ต้นงาน (worktree แยกของตัวเอง ตามกฎ) ให้ตรวจ
`ui_collectionobj_wire.py`/`test_ui_collectionobj_wire.py`/`docs/UI_LANE.md` diff แบบ adversarial
เต็มรูปแบบ: re-derive field shape ทั้ง 4 คลาสจาก TSV เอง, ตรวจตัวเลขแถวเสียของ 2 คลาสที่ข้าม,
ตรวจซ้ำข้อสรุป `KnowledgeGuru_`/`HitParade_` เอง (grep `^KnowledgeGuru_`/`^HitParade_` เอง),
ตรวจ vital id กับ registry เอง, fuzz decode_* ด้วย input พัง/overflow หา uncaught exception,
รันเทสไฟล์เอง, เทียบคำอธิบายใน `docs/UI_LANE.md` กับโค้ดจริง -- **ผลคืนแล้วรอบนี้ (ไม่ใช่ PENDING):
ไม่พบข้อบกพร่อง** ("Clean... I could not break this module" -- ทุกข้อตรวจตรงกับที่อ้าง, เทส
22 passed + 8 subtests ตรงกับที่ประกาศ, fuzz หา uncaught exception ไม่เจอ) มีข้อสังเกตเล็กน้อย
ไม่นับเป็นบั๊ก: มีแค่ `CollectObjFields` ที่มีเทส wrong-tag ที่ฟิลด์อื่นนอกจากฟิลด์แรก อีกสามคลาส
เทส wrong-tag เฉพาะฟิลด์แรก (ตรรกะ tag-check ใช้ helper เดียวกันและถูกใช้ซ้ำอยู่แล้ว ไม่ใช่ช่องโหว่จริง)

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_collectionobj_wire.py -q` = 22 passed, 8 subtests
passed
`PYTHONPATH=src python3 -m pytest tests/ -q` (ชุดเต็มบนต้นไม้ merge `origin/main` `20502a5` แล้ว
เป็น commit สุดท้ายจริง) = 12129 passed, 369 skipped, 25059 subtests passed, 0 failed (568.07s)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`:
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS · `[branch]` PASS ทั้งสองรีโป ·
`[bridgesize]` PASS (รอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`AGENTS.md`/
`CHIEF_CONTINUATION.md`, `NOW.md` ยังใต้เพดาน -- ไฟล์เดิมที่เกินเพดานอยู่ก่อน (`old`) ไม่ใช่หนี้ของกิ่งนี้) ·
`[scoreboard-manual]` PASS · `[prbody]` PASS ตรวจ PR body ฝั่งเซิร์ฟเวอร์ก่อนเปิดจริง (1 บรรทัด
marker เป๊ะ ที่บรรทัดสุดท้ายก่อน footer) ยืนยันด้วย GET หลังเปิด PR แล้วเห็น marker อยู่จริงเป๊ะ
บรรทัดเดียว

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `[LANE-UI] round tgyuuh: claim` (`#1469`) กิ่ง `claude/peaceful-pascal-tgyuuh` --
  ลบ `_claim.md`, ไฟล์รอบนี้แทน `_claim.md` (ไม่มี `.CONSUMED.txt` ใหม่ต้องวาง -- ไม่มีใบใหม่ให้บริโภค
  รอบนี้)
- `pirate-force-server`: PR `#912` (`[LANE-UI] CollectionObj_ wire module: 4 fully-tagged classes,
  wire shape only`) กิ่ง `claude/inspiring-feynman-tgyuuh`, ไม่ draft, marker `PF-AUTOMERGE: v4`
  ยืนยันแล้วด้วย GET -- `ui_collectionobj_wire.py` + `test_ui_collectionobj_wire.py` +
  `docs/UI_LANE.md`
- เลขใบใหม่รอบนี้: ไม่มี (ไม่ได้เปิด GT/RE ใหม่ -- โมดูลนี้ยังไม่มีใบเทสเพราะไม่ต่อสายเข้าเกม)

## nonclaims
(1) `ui_collectionobj_wire.py` ไม่อ้างความหมายฟิลด์ใด ๆ (collectible id, sailor level, effect id
ฯลฯ) -- `proven_semantics` ยัง `UNKNOWN` ทุกแถว
(2) ไม่ต่อสาย `ui_collectionobj_wire.py` เข้า `runtime.py`/`vital_walk.py` -- ของ CORE-REQUEST แยก
(3) ไม่อ้างว่าทั้ง 4 คลาสเคยถูกเห็นบนสายจริง -- `PF_FIELD_VALIDATION.tsv` เป็น `NOT_OBSERVED`/0
เฟรมทั้งสองทิศทางทุกคลาส
(4) ไม่อ้างว่า `KnowledgeGuru_`/`HitParade_` "ไม่มีทาง" ทำได้เลย -- อ้างแค่ว่ายังไม่เข้าเกณฑ์
"fully tagged" รอบนี้ (`KnowledgeGuru_` ต้องรอ static RE ถอด `0x0069F980`, `HitParade_` ต้อง static
RE ตั้งแต่ต้นเพราะไม่มีแถวใน TSV เลย)
(5) ไม่อ้างว่าตรวจสอบ NOW.md ข้อ R364 ข้อ 2 ซ้ำรอบนี้ -- ใช้ผลตรวจสดของรอบก่อน (`x28wjw`) ตามกฎ
ที่รอบนั้นวางไว้เอง ("เลขค้าง ไม่ใช่ของจริง")

## รอบหน้าทำอะไร
1. เช็ค `GT-184`/`GT-186` ว่า chief ลง `ATTENDED:`/เปลี่ยนหัวใบหรือยัง (ยังไม่ลงล่าสุดรอบนี้)
2. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: กลุ่มที่เหลือใน "everything else" ของ
   `docs/UI_LANE.md` คือ `Equipment_`(ของ LANE-DB grep-hint, พิจารณาถามก่อนแตะ)/`NavigationEx_`/
   `UserSetting`/`Dyeing`/`Appraisal`/`Vehicle`/`Potion`/`Relive`/`ItemLock` -- ตรวจ
   `CALL_UNCLASSIFIED`/`PE_IMPORT_*`/`SUBCALL:`/ฯลฯ ก่อนเขียนโค้ดเสมอ (บทเรียนห้ารอบติดรวมรอบนี้)
3. `KNOWN_RED_MAIN` เรื่อง `bridgesize` บน `GAME_TEST_QUEUE.md` ไม่ใช่ของ LANE-UI แก้ (chief ใบ
   `0747`) -- ยังเป็นจริงรอบนี้เหมือนเดิม
4. NOW.md ข้อ R364 ข้อ 2 ปิดไปแล้วจริงตามที่รอบ `x28wjw` ตรวจสด -- ไม่ต้องตรวจซ้ำถ้า NOW.md ยังพูดถึง
   ตัวเลขเดิมนี้อีก (เป็นเลขค้าง)

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (ของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมของสะสม (collection object) 4 ชนิด (เก็บของสะสม/ขอผล
เอฟเฟกต์คอลเลกชัน/ขอเลื่อนระดับกะลาสี/ผลเลื่อนระดับกะลาสี) ฝั่งเซิร์ฟเวอร์เสร็จพร้อมเทส 22 ตัว+8
subtests ผ่านหมด และผ่าน pf-adversary จริงรอบนี้ (ไม่ใช่ pending) แต่ยังไม่ต่อสายเข้าเกมจริง
(ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้) | PR `pirate-force-server#912`, PR `pf_bridge#1469`

-- LANE-UI (round `tgyuuh`)

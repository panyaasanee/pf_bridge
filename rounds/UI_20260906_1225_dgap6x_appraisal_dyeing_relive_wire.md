# LANE-UI round `dgap6x` -- 2026-09-06T12:25+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: ว่างทั้งคู่ -- เปิดคลาม `pf_bridge#1480`
  (`[LANE-UI] round dgap6x: claim`) จากกิ่ง `claude/ecstatic-volta-dgap6x` (pf_bridge) และ
  `claude/trusting-thompson-dgap6x` (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้
  เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ -- ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI)
grep `notes_to_chief/*.md` หา `ADDRESSEE: UI\b`/`ADDRESSEE: LANE-UI` (ทั้งสองแพทเทิร์น): ไม่มีใบ
ใหม่ -- ไม่มีอะไรให้บริโภครอบนี้ (ไม่มี `.CONSUMED.txt` ใหม่ต้องวาง)

## NOW.md -- อ่านสดตอนเริ่มรอบ
ดึงสด `origin/main` ก่อนเริ่ม (HEAD `56c6adc3`, ตรวจล่าสุดของ COO เขียนไว้ `2026-09-06 11:52 +07:00`,
รอบ `1141`) -- "รอ Panya ติ๊ก" มี 2 ข้อ ไม่กระทบ LANE-UI โดยตรง (เคาะสายที่ 9, ปิดมือ 3 ใบ ไม่มีใบของ
UI) · "รอเครื่องคุณ" ไม่มีใบ UI · ไม่มีข้อบังคับใหม่ที่กระทบเขตเขียนของ LANE-UI

## AGENTS.md section 7 -- อ่านครบรอบนี้
อ่านทั้งหัวข้อ "7. ห้ามทำ -- ไม่มีข้อยกเว้น" ครบ -- ไม่มีกฎใหม่ที่กระทบรอบนี้โดยตรง นอกจาก
`bridgesize`/`AGENTS.md`/`CHIEF_CONTINUATION.md`/`GAME_TEST_QUEUE.md` เพดานไฟล์ (ไม่กระทบ
เพราะรอบนี้ไม่แตะไฟล์เหล่านั้น) และกฎ `pf-adversary` บังคับทุกรอบที่แก้โค้ด (ทำตามข้างล่าง)

## งานหลัก (คิวเริ่มต้นข้อ 1-2) -- ตรวจซ้ำสดจากไฟล์ที่ดึงรอบนี้
1. UI-B logout wiring: ยังไม่มีอะไรให้ LANE-UI ทำเพิ่ม (CORE-REQUEST ค้างรอ chief เหมือนเดิม,
   ไม่มีการเปลี่ยนแปลงใน NOW.md)
2. UI-A back-to-charselect: `GT-184`/`GT-186` ยัง `BLOCKED-ON-RE-266` ตาม `docs/UI_LANE.md` (grep
   สดรอบนี้ ไม่เปลี่ยนจากรอบก่อน) -- รอ attended capture
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยน
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน

⇒ ขยับ NOW/M ข้อไหน: **ไม่ได้ขยับ** M2/P-1/P-2/P-3 -- งานหลักทั้งสี่ข้อยังติดเหมือนเดิม หยิบ
**งานสำรองข้อ 2** ของ `prompts/LANE-UI.md` แทน (ฟังก์ชันที่ layout รู้แล้ว) ต่อจากที่รอบก่อน
(`tgyuuh`, ปิด `CollectionObj_`) แนะนำไว้ในหัวข้อ "รอบหน้าทำอะไร": กลุ่มถัดไปใน "everything else"
ของ `docs/UI_LANE.md`

## งานสำรอง -- ทำรอบนี้: `Appraisal`/`Dyeing`/`Relive` wire module (+ ตรวจ `UserSetting`/`ItemLock`/
`Vehicle`/`Potion` แล้วตัดออก, ข้าม `NavigationEx_`/`Equipment_` เพราะเป็น grep-hint ของ LANE-A/DB)

จากรายการ "everything else" ของรอบก่อน (`Equipment_`/`KnowledgeGuru_`/`HitParade_`/`NavigationEx_`/
`UserSetting`/`Dyeing`/`Appraisal`/`Vehicle`/`Potion`/`Relive`/`ItemLock`):
- `Equipment_` ข้าม -- grep-hint ของ LANE-DB โดยตรง (`prompts/COMMON_LANE_ROUND.md`)
- `NavigationEx_` ข้าม -- grep-hint ของ LANE-A โดยตรง (`A Trigger*/Teleport*/COnLand/CVehicle/
  Instance*/NavigationEx_*`)
- `KnowledgeGuru_`/`HitParade_` ข้าม -- ตรวจแล้วโดยรอบก่อน (`tgyuuh`) ยังบล็อกเหมือนเดิม (SUBCALL:/
  ไม่มีแถวใน TSV) ไม่ตรวจซ้ำ
- `Vehicle`/`Potion` ตรวจรอบนี้: `awk -F'\t' '$2 ~ /Vehicle|Potion/'` บน
  `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` = **0 แถว** ทั้งคู่ -- ชื่อที่มีจริงบนสายคือ
  `CVehicle*`/`CPotion*` ซึ่ง `prompts/COMMON_LANE_ROUND.md` มอบให้ LANE-A/LANE-B ตรงตัวแล้ว ไม่ใช่
  ของ LANE-UI ⇒ ตัดออกถาวร (ไม่ใช่ "ยังไม่ทำ")
- `UserSetting` (1 แถว, `UserSetting_UpdateServerSettingVital` `0x0F01`) ตรวจรอบนี้: มี
  `CALL_UNCLASSIFIED:INDIRECT(...)`/`CALL_UNCLASSIFIED:0x00720FC0`/
  `DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04`/
  `ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C` (5 ของ 6 แถวต่อทิศทางเสีย) ⇒ ยังไม่เข้าเกณฑ์
  "fully tagged" -- **หมายเหตุสำคัญ**: grep `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/`archive/`
  พบว่าคลาสนี้มีเฟรมจับจริงแล้ว **197 ครั้งจาก 117 ไฟล์แคปเจอร์** (ปุ่ม Options→Apply) -- ไม่ใช่
  ใบเปล่า มีหลักฐาน capture อยู่แล้วสำหรับใครจะมาแก้ 5 แถวที่ยังไม่คลี่
- `ItemLockVital` (1 แถว) ตรวจรอบนี้: มี `PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL` x4 +
  `CALL_UNCLASSIFIED:0x006CD400` x2 (6 ของ 14 แถวเสีย) ⇒ ยังไม่เข้าเกณฑ์
- `Dyeing` (4 แถว): `DyeingVitalRes`/`DyeingRemoveVital`/`DyeingShipVitalReq` ครบ 0 แถวเสีย แต่
  `DyeingVitalReq` มีฟิลด์ที่ 2 แท็ก `UNTAGGED_STRING8_LEN32LE` ซึ่ง
  `src/pirateforce_foundation/logout_hypothesis.py` (RE-196/GT-055) พิสูจน์แล้วว่าป้ายนี้บอกแค่ขอบเขต
  ของ helper call ไม่ใช่หลักฐานว่าไม่มีแท็กไบต์ (`DeleteActorVital` มีป้ายเดียวกันแต่ GT-018 ยืนยันมี
  แท็ก `0x44` จริง) ⇒ **ตัดออกจากรอบนี้ ไม่ implement เป็น untagged** รอใบ static RE เฉพาะคำถามนี้
- `Appraisal` (2 แถว): `AppraisalVital`/`AppraisalStopVital` ครบ 0 แถวเสียทั้งคู่ -- กลุ่มเต็ม (2/2)
- `Relive` (2 แถว): `ReliveVital` ครบ 0 แถวเสีย, `ReliveMarkerVital` มี `SUBCALL:`/
  `CALL_UNCLASSIFIED:0x004B1C40`/`DYNAMIC_INTERLOCKED_*`/`ATOMIC_*` (10 ของ 26 แถวเสีย) ⇒ ตัดออก

ผลลัพธ์ (`pirate-force-server`): `src/pirateforce_foundation/ui_dyeing_appraisal_relive_wire.py`
(ใหม่, 6 คลาส รวม 3 กลุ่ม -- รวมไฟล์เดียวแทนที่จะแยกกลุ่มละไฟล์ เพื่อให้ไม่เกิน ~6 ไฟล์/PR ตาม
`AGENTS.md` section 7 "วิธีเปิด PR") + `tests/test_ui_dyeing_appraisal_relive_wire.py` (ใหม่, 33
เทส + 10 subtests) + แก้ `ui_social_wire.py` (docstring เพิ่มแท็ก `0x05`=u8 ใหม่) + อัปเดต
`docs/UI_LANE.md` (3 แถวใหม่ + nonclaims + ตัด `Dyeing`/`Appraisal`/`Vehicle`/`Potion`/`Relive`
ออกจากรายการ NOT YET ITEMIZED)

grep ตาม `AGENTS.md` section 7 ก่อนเขียนโค้ด: ผลเต็มอยู่ใน module docstring (แก้ไขหลัง adversary
ชี้ข้อผิดพลาดของการ grep รอบแรก -- ดูหัวข้อ ADVERSARY ข้างล่าง)

## ADVERSARY -- เรียกได้จริงรอบนี้ ผลคืนแล้ว (ไม่ใช่ PENDING) พบข้อบกพร่องจริง 2 ข้อ แก้แล้ว
เรียก `pf-adversary` ผ่าน Agent tool ต้นงาน (worktree แยกของตัวเอง) ให้ตรวจ
`ui_dyeing_appraisal_relive_wire.py`/`test_ui_dyeing_appraisal_relive_wire.py`/`ui_social_wire.py`/
`docs/UI_LANE.md` diff แบบ adversarial เต็มรูปแบบ (re-derive field shape ทั้ง 6 คลาสจาก TSV เอง,
ตรวจ vital id, ตรวจข้อสรุปการตัดคลาสออกทั้งหมด, fuzz decode_* หา uncaught exception, รันเทสไฟล์เอง,
เทียบ docs/UI_LANE.md กับโค้ดจริง)

**ผลคืน: ไม่ใช่ Clean -- พบข้อบกพร่องจริง 2 ข้อ ทั้งสองแก้ในรอบนี้ก่อน push:**
1. คำอ้าง "grepped first, no hit" ในรอบร่างแรกเป็นเท็จสำหรับ 2 ใน 10 ชื่อคลาส:
   `UserSetting_UpdateServerSettingVital` มีจริงใน `CLIENT_RE_QUEUE.md` (รวมบันทึกเฟรมจับจริง 197
   ครั้ง/117 ไฟล์) และ `GAME_TEST_QUEUE.md`/`archive/` 5 ไฟล์; `ReliveMarkerVital` มีจริงใน
   `GAME_TEST_QUEUE.md:10598` (อ้างใบ `RE-112` ที่ปิดแล้ว) และ `archive/` -- แก้โดยเขียนผล grep ที่
   ตรงกับความจริงลง docstring (แยกกรณี "grep แล้วไม่เจอจริง" กับ "grep แล้วเจอ แต่ไม่กระทบข้อสรุป")
2. ตัวเลข "N ของ M แถวเสีย" ผิด 2 จุด: `ReliveMarkerVital` เขียนไว้ "6 ของ 15" ที่ถูกคือ **10 ของ 26**
   แถวทั้งหมด (13W+13R); `ItemLockVital` เขียนไว้ "4 ของ 14" ที่ถูกคือ **6 ของ 14** (4 PE_IMPORT + 2
   CALL_UNCLASSIFIED ไม่ใช่ 3+1) -- แก้ด้วย `awk` นับใหม่ตรงจาก TSV ทั้งสองจุด ทั้งใน docstring และ
   `docs/UI_LANE.md`
ตรวจซ้ำเองหลังแก้: grep ทั้งสามคำสั่งข้างต้นและ `awk` นับแถวใหม่ตรงกับตัวเลขที่แก้แล้วทุกจุด -- ไม่มี
ข้อบกพร่องอื่นที่ adversary ชี้ (wire shape/vital id/fuzz/เทส/nonclaims ผ่านหมด)

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_dyeing_appraisal_relive_wire.py -q` = 33 passed, 10
subtests passed (รันซ้ำหลังแก้ตาม adversary พร้อม `tests/test_ui_social_wire.py` = 59 passed รวม)
`PYTHONPATH=src python3 -m pytest tests/ -q` (ชุดเต็มบนต้นไม้ merge `origin/main` `4e64b7de` แล้ว
เป็น commit สุดท้ายจริง) = 12196 passed, 365 skipped, 25080 subtests passed, 0 failed (442.20s)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`:
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS · `[branch]` PASS ทั้งสองรีโป ·
`[bridgesize]` PASS (รอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`AGENTS.md`/
`CHIEF_CONTINUATION.md`, `NOW.md` ยังใต้เพดาน -- ไฟล์เดิมที่เกินเพดานอยู่ก่อน (`old`) ไม่ใช่หนี้ของกิ่งนี้) ·
`[scoreboard-manual]` PASS · `[prbody]` PASS ตรวจ PR body ฝั่งเซิร์ฟเวอร์ก่อนเปิดจริง (`--pr-stage
final`, 1 บรรทัด marker เป๊ะที่บรรทัด 38) ยืนยันด้วย GET หลังเปิด PR แล้วเห็น marker อยู่จริงเป๊ะ
บรรทัดเดียว, `draft=false`

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `[LANE-UI] round dgap6x: claim` (`#1480`) กิ่ง `claude/ecstatic-volta-dgap6x` --
  ลบ `_claim.md`, ไฟล์รอบนี้แทน `_claim.md` (ไม่มี `.CONSUMED.txt` ใหม่ต้องวาง -- ไม่มีใบใหม่ให้บริโภค
  รอบนี้)
- `pirate-force-server`: PR `#917` (`[LANE-UI] Appraisal/Dyeing/Relive wire-shape module: 6
  fully-tagged classes`) กิ่ง `claude/trusting-thompson-dgap6x`, ไม่ draft, marker `PF-AUTOMERGE: v4`
  ยืนยันแล้วด้วย GET -- 4 ไฟล์: `ui_dyeing_appraisal_relive_wire.py` (ใหม่) +
  `test_ui_dyeing_appraisal_relive_wire.py` (ใหม่) + `ui_social_wire.py` (docstring) +
  `docs/UI_LANE.md`
- เลขใบใหม่รอบนี้: ไม่มี (ไม่ได้เปิด GT/RE ใหม่ -- โมดูลนี้ยังไม่ต่อสายเข้าเกม เหมือนโมดูลพี่น้องทุกตัว)

## nonclaims
(1) `ui_dyeing_appraisal_relive_wire.py` ไม่อ้างความหมายฟิลด์ใด ๆ (สีย้อม, เป้าหมายการประเมินราคา,
เครื่องหมายจุดฟื้นคืนชีพ ฯลฯ) -- `proven_semantics` ยัง `UNKNOWN` ทุกแถวทั้ง 6 คลาส
(2) ไม่ต่อสายเข้า `runtime.py`/`vital_walk.py` -- ของ CORE-REQUEST แยก
(3) ไม่อ้างว่าทั้ง 6 คลาสเคยถูกเห็นบนสายจริง -- `PF_FIELD_VALIDATION.tsv` เป็น `NOT_OBSERVED`/0
เฟรมทั้งสองทิศทางทุกคลาส (ยกเว้น `UserSetting_UpdateServerSettingVital` ที่มีเฟรมจับจริงแล้ว แต่
คลาสนั้นไม่ได้ implement ในโมดูลนี้)
(4) ไม่อ้างว่า `DyeingVitalReq`/`UserSetting_UpdateServerSettingVital`/`ReliveMarkerVital`/
`ItemLockVital` "ไม่มีทาง" ทำได้เลย -- อ้างแค่ว่ายังไม่เข้าเกณฑ์ "fully tagged" รอบนี้ตามเกณฑ์เดียวกับ
ทุกรอบก่อนหน้า
(5) ไม่อ้างว่า `Vehicle`/`Potion` "ไม่มีอยู่ในเกม" -- อ้างแค่ว่าไม่มีแถวภายใต้ชื่อ prefix เหล่านั้นตรง ๆ
ใน `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`; คลาสที่เกี่ยวข้องจริง (`CVehicle*`/`CPotion*`)
เป็นของ LANE-A/LANE-B ตาม grep-hint ที่มีอยู่แล้ว
(6) ไม่อ้างว่าตรวจสอบ NOW.md ซ้ำทุกข้อละเอียด -- อ่านสดหัวข้อ "รอ Panya ติ๊ก"/"รอเครื่องคุณ" เท่านั้น
ตามที่ระบุไว้ในหัวข้อ COMMON_LANE_ROUND.md ข้อ 1

## รอบหน้าทำอะไร
1. เช็ค `GT-184`/`GT-186` ว่า chief ลง `ATTENDED:`/เปลี่ยนหัวใบหรือยัง (ยังไม่ลงล่าสุดรอบนี้)
2. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: หลังรอบนี้ "everything else" ที่เหลือคือ
   `Equipment_`(ของ LANE-DB grep-hint)/`KnowledgeGuru_`(บล็อก SUBCALL:)/`HitParade_`(0 แถวใน TSV)/
   `NavigationEx_`(ของ LANE-A grep-hint) -- ทั้งหมดติดหรือไม่ใช่ของสายนี้ ⇒ รอบหน้าอาจต้องกลับไปหยิบ
   `DyeingVitalReq`'s static-RE ticket (คำถามเจาะจง: มี tag-push ก่อน `string_wire_call@0x006C65A4`
   ไหม) เป็นใบ RE ใหม่ หรือรอ static RE ปลดล็อก `KnowledgeGuru_`/`ReliveMarkerVital`/`ItemLockVital`/
   `UserSetting_UpdateServerSettingVital` จากสายอื่น
3. `UserSetting_UpdateServerSettingVital` มีเฟรมจับจริงแล้ว 197 ครั้ง/117 ไฟล์ (`CLIENT_RE_QUEUE.md`)
   -- ใครแก้ 5 แถวที่ยังไม่คลี่ (`CALL_UNCLASSIFIED`/`DYNAMIC_INTERLOCKED_*`/`ATOMIC_*`) ควรเริ่มจาก
   หลักฐานนั้น ไม่ใช่เริ่มจากศูนย์
4. `KNOWN_RED_MAIN` เรื่อง `bridgesize` บน `GAME_TEST_QUEUE.md` ไม่ใช่ของ LANE-UI แก้ (chief ใบ
   `0747`) -- ยังเป็นจริงรอบนี้เหมือนเดิม

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (ของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมของสีย้อม/การประเมินราคา/จุดฟื้นคืนชีพ 6 ชนิด (เปลี่ยนสี,
ผลเปลี่ยนสี, ลบสี, เปลี่ยนสีเรือ, ประเมินราคา, หยุดประเมินราคา, ฟื้นคืนชีพ) ฝั่งเซิร์ฟเวอร์เสร็จพร้อม
เทส 33 ตัว+10 subtests ผ่านหมด และผ่าน pf-adversary จริงรอบนี้ (พบบั๊กจริง 2 ข้อ แก้แล้วก่อน push
ไม่ใช่ pending) แต่ยังไม่ต่อสายเข้าเกมจริง (ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้) | PR
`pirate-force-server#917`, PR `pf_bridge#1480`

-- LANE-UI (round `dgap6x`)

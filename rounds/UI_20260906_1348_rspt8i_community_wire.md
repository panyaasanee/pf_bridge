# LANE-UI round `rspt8i` -- 2026-09-06T13:48+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: ว่างทั้งคู่ -- เปิดคลาม `pf_bridge#1490`
  (`[LANE-UI] round rspt8i: claim`) จากกิ่ง `claude/peaceful-pascal-rspt8i` (pf_bridge) และ
  `claude/inspiring-feynman-rspt8i` (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้
  เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง (ทั้งสองรีโปรีเซ็ตเป็น `origin/main` ก่อนเริ่ม เพราะไม่มีคอมมิต
  ที่ยังไม่ merge ค้างอยู่บนกิ่งเดิม -- `git rev-list --count` ทั้งสองทิศทาง = 0)
- list ซ้ำทันทีหลังเปิด: PR อื่นที่เปิดอยู่คือ `[LANE-K] slug54r2`/`[LANE-CS] fufcdn`/
  `[LANE-B] 30ja9z`/`[LANE-E] d5igq0` -- ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ -- ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI)
grep `notes_to_chief/*.md` หา `ADDRESSEE: LANE-UI` (ไม่มี `.CONSUMED.txt` คู่): **ไม่มีใบใหม่** -- 33
ใบที่ตรงแพทเทิร์นทั้งหมดมี stub `.CONSUMED.txt` อยู่แล้วจากรอบก่อน ๆ (รวมรอบล่าสุด `dgap6x`)

แยกตรวจเพิ่ม (ไม่ใช่แพทเทิร์นตรง แต่ cc LANE-UI): จดหมาย
`20260906_0155_KA1A-R320-RESULTS-*.md` (ADDRESSEE: chief, cc LANE-UI สำหรับ `GT-230`/
`RE-235`/`RE-237`/`RE-261`) มี `.CONSUMED.txt` แล้ว -- ตรวจ queue จริงยืนยันผลบริโภคแล้วจริง:
`GT-262` (คู่ `RE-261`) สถานะ `READY` เนื้อใบเต็มแล้ว (`GAME_TEST_QUEUE.md:10086`, เขียนโดย LANE-UI
รอบก่อนหน้า), `GT-253` (ต่อยอด `RE-237`) สถานะ `PENDING` เนื้อใบครบแล้วเช่นกัน
(`GAME_TEST_QUEUE.md:9884`, เขียนโดย LANE-UI รอบ `9f2k7c`) -- ทั้งสองใบรอคิว attended เท่านั้น
ไม่มีงานเพิ่มให้ LANE-UI รอบนี้จากจดหมายนี้ (ดัชนีสรุปหัวไฟล์ที่ยังพิมพ์ `PENDING`/`BLOCKED` ของทั้งสอง
ใบเป็นของเก่าที่ chief ยังไม่รีเฟรช -- ไม่ใช่หน้าที่ LANE-UI แก้ดัชนีนั้น)

## NOW.md -- อ่านสดตอนเริ่มรอบ
ดึงสด `origin/main` ก่อนเริ่ม (ตรวจล่าสุดของ COO เขียนไว้ 2026-09-06 11:52 +07:00, รอบ `1141`) --
"รอ Panya ติ๊ก" 2 ข้อ ไม่กระทบ LANE-UI (เคาะสายที่ 9, ปิดมือ 3 ใบ) · "รอเครื่องคุณ" ไม่มีใบ UI หัวคิว
(GT-233/GT-272 เป็นของ M2/DB) · ไม่มีข้อบังคับใหม่กระทบเขตเขียนของ LANE-UI

## AGENTS.md section 7 -- อ่านครบรอบนี้
อ่านทั้งหัวข้อครบ -- ไม่มีกฎใหม่กระทบรอบนี้โดยตรง นอกจากเพดานไฟล์ (ไม่กระทบ ไม่แตะไฟล์กลาง) และ
กฎ `pf-adversary` บังคับ (ทำตามข้างล่าง)

## งานหลัก (คิวเริ่มต้นข้อ 1-4) -- ตรวจซ้ำสดจากไฟล์ที่ดึงรอบนี้
1. UI-B logout wiring: ไม่มีอะไรใหม่ให้ทำ -- CORE-REQUEST ยังค้างรอ chief เหมือนรอบก่อน
2. UI-A back-to-charselect: `GT-184`/`GT-186` ยัง `BLOCKED-ON-WIRING`/`BLOCKED-ON-RE-266` ตาม
   `docs/UI_LANE.md` (grep สดรอบนี้ ไม่เปลี่ยนจากรอบ `dgap6x`) -- รอ attended capture
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยน
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน (`GT-230` archived PASS จาก R320 attended
   -- ผลอยู่ใน note ข้างบน, ไม่ปลดบล็อกอินเตอร์เฟซ LANE-DB)

⇒ ขยับ NOW/M ข้อไหน: **ไม่ได้ขยับ** M2/P-1/P-2/P-3 -- งานหลักทั้งสี่ข้อยังติดเหมือนเดิม หยิบ
**งานสำรองข้อ 2** ต่อจากรอบก่อน (`dgap6x` ปิด `Appraisal`/`Dyeing`/`Relive`): กลุ่มใหญ่ที่สุดที่ยัง
ไม่เคยตรวจเต็ม -- `Community_` (38 คลาส, มีแค่ 5 ที่ถูกต่อสายแล้วผ่าน `CORE-REQUEST 1120`)

## งานสำรอง -- ทำรอบนี้: `Community_` wire module (16 คลาส fully-tagged ใหม่)

ตรวจทุกแถว `Community_` ใน `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (37 แถว) เทียบกับ
`external/PF_SERIALIZER_FIELDS.tsv`:
- 5 คลาสถูกต่อสายแล้วโดย `ui_friend_wire.py`/`ui_mail_wire.py` (`RequestBeFriendVital`/
  `RemoveFriendVital`/`SendMailVital`/`GetMailContentVital`/`DeleteMailVital`) -- ข้าม
- 9 แถวไม่มีเลยใน `PF_SERIALIZER_FIELDS.tsv` (`comm -23` ระหว่างสองไฟล์) -- ไม่รู้ layout เลย
  ต้องการ static RE จากศูนย์ ไม่ใช่คำถาม field-completeness
- 24 แถวที่เหลือตรวจด้วย `awk` นับแถว `CALL_UNCLASSIFIED`/`PE_IMPORT_*`/`SUBCALL:`/
  `DYNAMIC_INTERLOCKED_*`/`ATOMIC_*`/`UNKNOWN` ต่อคลาส:
  - 8 คลาสยังมีแถวเสีย (`AddBlackListVital` 10/18 · `AddFriendVital` 10/18 ·
    `GetActorVowLockListVital` 12/18 · `InitalizeActorCommunityVital` 22/54 ·
    `ReceiveNewMailVital` 8/34 · `ReplyPenpalLetterVital` 10/24 ·
    `RequestSoulMateMatchVital` 10/16 · `UpdateActorVowLockVital` 8/14) -- ตัดออก
  - **16 คลาสครบ 0 แถวเสียทั้งคู่ (W และ R)** -- นี่คือกลุ่มที่ implement รอบนี้

grep ตาม `AGENTS.md` section 7 ก่อนเขียนโค้ด (ทั้ง 16 ชื่อคลาส): `external/` เจอเฉพาะ
`PF_FIELD_VALIDATION.tsv`/`PF_PROTOCOL_PRIORITY.tsv` (ตารางสำรวจ ไม่ใช่ใบ) -- **ไม่เจอ**ใน
`CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/`archive/`/`notes_to_chief/consumed/` เลยสักคลาส
(ไม่มีใบ RE/GT เปิดหรือปิดอ้างอิงชื่อเหล่านี้) -- ยืนยัน `status=NOT_OBSERVED`/`observed_frames=0`
ทั้ง 16 คลาสทั้งสองทิศทางจาก `PF_FIELD_VALIDATION.tsv` ด้วย

ผลลัพธ์ (`pirate-force-server`): `src/pirateforce_foundation/ui_community_social_wire.py`
(ใหม่, 16 คลาส) + `tests/test_ui_community_social_wire.py` (ใหม่, 69 เทส + 32 subtests) +
อัปเดต `docs/UI_LANE.md` (แถวใหม่ + nonclaims)

## ADVERSARY -- เรียกได้จริงรอบนี้ ผลคืนแล้วก่อน push (ไม่ใช่ PENDING) -- Clean, ไม่พบข้อบกพร่อง
เรียก `pf-adversary` ผ่าน Agent tool ต้นงาน (worktree แยกของตัวเอง) ให้ตรวจ
`ui_community_social_wire.py`/`test_ui_community_social_wire.py`/`docs/UI_LANE.md` diff แบบ
adversarial เต็มรูปแบบ: re-derive field shape ทั้ง 16 คลาสจาก TSV เอง, ตรวจ vital id, ตรวจข้อสรุป
การตัดคลาสออกทั้งหมด (8 excluded + 9 no-layout ต้องรวมกับ 16+5 = 38 พอดี), fuzz decode_* หา
uncaught exception, รันเทสไฟล์เอง, grep หา vital id ชนกับโมดูลพี่น้อง

**ผลคืน: Clean -- ไม่พบข้อบกพร่องจริง** ตรวจ 6 แกนครบ (field shape, vital id, exclusion
accounting, fuzz ~52,000 trial, pytest เขียว, ไม่มี id ชนกัน) ข้อสังเกตเดียวที่ยกมา (ไม่ใช่บั๊ก):
`encode_*` มาสก์ค่าที่เกินขอบเขต (`& 0xFF` ฯลฯ) แบบเงียบ -- ตรงกับพฤติกรรมโมดูลพี่น้องทุกตัว
ไม่ใช่ของใหม่ ไม่แก้

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_community_social_wire.py -q` = 69 passed, 32
subtests passed
`PYTHONPATH=src python3 -m pytest tests/ -q` (ชุดเต็มบนต้นไม้ merge `origin/main` `154f0f1` แล้ว
เป็น commit สุดท้ายจริง) = 12272 passed, 369 skipped, 25118 subtests passed, 0 failed (485.90s)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`:
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS · `[branch]` PASS ทั้งสองรีโป ·
`[bridgesize]` PASS (รอบนี้ไม่แตะไฟล์กลาง, `NOW.md` ยังใต้เพดาน) · `[scoreboard-manual]` PASS ·
`[prbody]` PASS ตรวจ PR body ฝั่งเซิร์ฟเวอร์ก่อนเปิดจริง (`--pr-stage final`, 1 บรรทัด marker เป๊ะ
ที่บรรทัด 46) ยืนยันด้วย GET หลังเปิด PR แล้วเห็น marker อยู่จริงเป๊ะบรรทัดเดียว, `draft=false`

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `[LANE-UI] round rspt8i: claim` (`#1490`) กิ่ง `claude/peaceful-pascal-rspt8i` --
  ลบ `_claim.md`, ไฟล์รอบนี้แทน `_claim.md` (ไม่มี `.CONSUMED.txt` ใหม่ต้องวาง -- ไม่มีใบใหม่ให้
  บริโภครอบนี้ นอกจากยืนยันซ้ำว่า R320 letter บริโภคแล้วจริงจากรอบก่อน)
- `pirate-force-server`: PR `#923` (`[LANE-UI] Community_* wire-shape module: 16 fully-tagged
  classes`) กิ่ง `claude/inspiring-feynman-rspt8i`, ไม่ draft, marker `PF-AUTOMERGE: v4`
  ยืนยันแล้วด้วย GET -- 3 ไฟล์: `ui_community_social_wire.py` (ใหม่) +
  `test_ui_community_social_wire.py` (ใหม่) + `docs/UI_LANE.md`
- เลขใบใหม่รอบนี้: ไม่มี (ไม่ได้เปิด GT/RE ใหม่ -- โมดูลนี้ยังไม่ต่อสายเข้าเกม เหมือนโมดูลพี่น้องทุกตัว)

## nonclaims
(1) `ui_community_social_wire.py` ไม่อ้างความหมายฟิลด์ใด ๆ (ความคิดเห็น, ชื่อเล่น, ข้อความจดหมาย,
เนื้อหาขวด ฯลฯ) -- `proven_semantics` ยัง `UNKNOWN` ทุกแถวทั้ง 16 คลาส
(2) ไม่ต่อสายเข้า `runtime.py`/`vital_walk.py` -- ของ CORE-REQUEST แยก
(3) ไม่อ้างว่าทั้ง 16 คลาสเคยถูกเห็นบนสายจริง -- `PF_FIELD_VALIDATION.tsv` เป็น `NOT_OBSERVED`/0
เฟรมทั้งสองทิศทางทุกคลาส
(4) ไม่อ้างว่าคู่คลาสที่มีรูปทรงเดียวกัน (`ChangeActorCommentVital`/`ChangeActorPenNameVital`/
`RemoveBlackListVital`/`TargetConfirmSoulMateMatchVital`/`ThrowLetterInABottleVital` เป็น
u64+wstring+u8 ทั้งหมด; `ReplyLetterInABottleVital`/`UseBlankPenpalLetterVital` เป็น u64+u64+u8
ทั้งคู่) เป็นการกระทำเดียวกัน -- อ้างแค่ว่ารูปทรงไบต์ตรงกัน แต่ vital id และ dataclass แยกกันเสมอ
(5) ไม่อ้างว่า 8 คลาสที่ตัดออก "ทำไม่ได้เลย" -- อ้างแค่ว่ายังไม่เข้าเกณฑ์ "fully tagged" รอบนี้
(6) ไม่อ้างว่า 9 แถวที่ไม่มีใน TSV "ไม่มีอยู่จริงในเกม" -- อ้างแค่ว่ายังไม่มี layout ที่รู้เลย

## รอบหน้าทำอะไร
1. เช็ค `GT-184`/`GT-186` ว่า chief ลง `ATTENDED:`/เปลี่ยนหัวใบหรือยัง (ยังไม่ลงล่าสุดรอบนี้)
2. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: `Community_` กลุ่มนี้ปิดแล้วครบ 16/38 (ที่เหลือ
   คือ 8 excluded + 9 no-layout + 5 ต่อสายแล้ว = 38 ครบ) -- กลุ่มถัดไปที่ยังไม่เคยตรวจเต็มในตาราง
   `docs/UI_LANE.md` คือรายการใน "everything else" (`Equipment_`/`KnowledgeGuru_`/`HitParade_`/
   `NavigationEx_`/`UserSetting`/`Vehicle`/`Potion`/`ItemLock`) ซึ่งถูกตรวจแล้วทั้งหมดและติด/ไม่ใช่
   ของสายนี้ (ดูรอบ `dgap6x`) -- ถ้าไม่มีกลุ่มใหม่เหลือ ให้กลับไปหยิบใบ static-RE เฉพาะจุดที่ค้าง
   (`DyeingVitalReq` tag-push question, ข้อ 3 ข้างล่าง) หรือรอผล RE จากสายอื่นปลดล็อกกลุ่มที่ตัดออก
3. `UserSetting_UpdateServerSettingVital` มีเฟรมจับจริงแล้ว 197+ ครั้ง (`CLIENT_RE_QUEUE.md`) และ
   `RE-237`/`GT-253` เก็บ hex เพิ่มจาก R320 แล้ว (ตั้งค่า "ใช้" 2 ครั้ง) -- ใครแก้ 5 แถวที่ยังไม่คลี่
   ควรเริ่มจากหลักฐานนั้น ไม่ใช่เริ่มจากศูนย์
4. `KNOWN_RED_MAIN` เรื่อง `bridgesize` บน `GAME_TEST_QUEUE.md` ไม่ใช่ของ LANE-UI แก้ -- ยังเป็น
   จริงรอบนี้เหมือนเดิม
5. เช็ค `CORE-REQUEST 20260905_2006` (เสียบ `LogoutVital` subcode 1 ใน `runtime.py`) ว่า chief
   ตอบหรือยัง (สั่งเป็นงาน (1) ของ chief รอบถัดไปตาม `COO-DECISION 1341` ข้อ 2, ดูหัวข้อ
   "กล่องจดหมายเพิ่มเติม" ข้างบน) -- ถ้ายังไม่ตอบ เขียน COO บรรทัดเดียว

## กล่องจดหมายเพิ่มเติม (มาถึงระหว่างรอบ ผ่าน `git merge origin/main` ก่อน push)
`notes_to_chief/20260906_1349_COO-DECISION-ui2015-*-LANE-UI.md` (รอบ COO `1341`): ปิดใบ
`20260905_2015_LANE-UI-ASK-COO-pf-adversary-not-a-callable-tool-this-session.md` ด้วยทาง (ก)
เดิม -- pf-adversary กลับมาใช้ได้ตั้งแต่รอบ `g1ss4s` (5 รอบหลังจากนั้นทุกรอบมีผลจริงในไฟล์รอบ รวม
ทั้งรอบนี้) ไม่ต้องแจ้ง Panya เพิ่ม · ข้อ 2: `CORE-REQUEST 20260905_2006` (เสียบ `LogoutVital`
subcode 1 ใน `runtime.py`) สั่ง chief ตอบเป็นงาน (1) รอบถัดไปของ chief (`1345` ข้อ 5) -- **รอบหน้า
ของ LANE-UI ต้องเช็คว่า chief ตอบหรือยัง ถ้ายังไม่ตอบให้เขียน COO บรรทัดเดียว** (เพิ่มในหัวข้อ
"รอบหน้าทำอะไร" ด้านล่าง) · ข้อ 3: GT ticket ใหม่ทุกใบจากนี้ส่ง `*-TO-K-gt-body-*` ให้ LANE-K ตั้งเลข
แทน chief (PANYA `1259`) -- รอบนี้ไม่ได้เปิดใบใหม่จึงยังไม่ใช้กฎนี้จริง แต่บันทึกไว้สำหรับรอบหน้า ·
วาง `.CONSUMED.txt` + สำเนาไป `notes_to_chief/consumed/` แล้ว

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (ของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมของระบบเพื่อน/แบล็คลิสต์/จดหมาย/ขวดจดหมาย/แม่สื่อคู่รัก
16 ชนิดในกลุ่ม Community ฝั่งเซิร์ฟเวอร์เสร็จพร้อมเทส 69 ตัว+32 subtests ผ่านหมด และผ่าน
pf-adversary จริงรอบนี้ (Clean ไม่พบข้อบกพร่อง) แต่ยังไม่ต่อสายเข้าเกมจริง (ผู้เล่นยังกดอะไรไม่ได้
จากงานนี้วันนี้) | PR `pirate-force-server#923`, PR `pf_bridge#1490`

-- LANE-UI (round `rspt8i`)

# LANE-UI round `on8hbb` -- 2026-09-07T01:48+07:00 start

## เวลา
ก่อน push (02:12+07:00) เทียบกับ `notes_to_chief/_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด
(`01:42:04+07:00`) ต่างกัน 30 นาที ไม่เกิน 60 นาทีตามกฎ -- ไม่มีอะไรต้องรายงาน

## ล็อกรอบ
list เปิด `[LANE-UI] round` ใน `pf_bridge` ก่อนเริ่มรอบ: ว่าง -- เปิด claim `pf_bridge#1605`
ทันที จากกิ่ง `claude/peaceful-pascal-on8hbb` (pf_bridge) และ `claude/inspiring-feynman-on8hbb`
(pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
list ซ้ำทันทีหลังเปิด: ยังเป็นใบเดียว ไม่มี `[LANE-UI] round` อื่นเก่ากว่าแข่งอยู่

## แหล่งความจริงที่อ่านต้นรอบ
1. `NOW.md` (ตรวจล่าสุด COO รอบ `0043`) -- บรรทัด LANE-UI: wstring `0x48` PR (`1713`) ปิดแล้ว
   (merge `c54231f`) -> งาน 2 `2032` แถบ n/327 (`#961` ถูก reaper ปิด ยังไม่กู้ รอ root cause) ·
   express/community ยังห้ามต่อสายเข้า `runtime.py` (`1649`) -- ไม่มีบรรทัดใหม่กระทบ LANE-UI
   นอกเหนือจากที่รอบ `me7s4u` อ่านไปแล้ว
2. กล่องจดหมาย `ADDRESSEE: UI`/`LANE-UI` ที่ไม่มี `.CONSUMED.txt` คู่: ตอนเริ่มรอบ **ว่าง**
   (ไล่ทุกใบเทียบ stub คู่ด้วยชื่อไฟล์เต็ม `<ชื่อเดิม>.md.CONSUMED.txt` ไม่ใช่ตัดนามสกุล -- แก้
   สคริปต์ตรวจหลังเจอผลลวงจากรอบตัวเองครั้งแรก) -- **ระหว่างรอบ** ทำงานสำรองเสร็จแล้วสั่ง
   `git fetch origin main && git merge origin/main` ซ้ำก่อน push (ตามกฎ) แล้วพบจดหมายใหม่ที่
   จ่าหน้าถึง LANE-UI เข้ามาพร้อมการ merge: `notes_to_chief/
   20260907_0148_COO-DECISION-ui0050-961-not-systemic-recover-once-path-agnostic-LANE-UI.md`
   (ตอบใบ `20260907_0050` ของรอบ `me7s4u` เอง) -- อ่านและทำตามทันทีในรอบเดียวกัน (ดูหัวข้อ
   "งานสำรอง -- ทำรอบนี้ (2)" ด้านล่าง) แล้ววาง stub ให้
3. `AGENTS.md` section 7 -- อ่านครบ ไม่มีกฎใหม่กระทบงานรอบนี้โดยตรง
4. ไฟล์รอบล่าสุดของสาย `rounds/UI_20260907_0018_me7s4u_express_migration_plus_945_recovery.md`
   -- "รอบหน้าทำอะไร" ข้อ 1: เช็คคำตอบเรื่อง `#961`/gate-windows root cause (ยังไม่มีคำตอบ --
   ดูข้อ 2 ด้านบน) ข้อ 2: ถ้ายังไม่มีคำตอบ migrate `ui_community_social_wire.py` ทีละ 2-3 คลาส
   (งานที่ทำรอบนี้) ข้อ 3/4: เช็ค `GT-184`/`GT-186`/`RE-286` -- ทั้งสองยังไม่ขยับ (ดูหัวข้อถัดไป)

## เช็คสถานะที่ค้าง (ไม่ใช่งานของ LANE-UI แต่เป็นผู้บริโภคผล)
- `pirate-force-server#961` (n/327 census): **กู้แล้วรอบนี้** -- ดูหัวข้อ "งานสำรอง -- ทำรอบนี้
  (2)" ด้านล่าง (คำตอบมาจาก `COO-DECISION 20260907_0148` ที่เข้ามาระหว่างรอบผ่านการ merge
  origin/main ครั้งที่สอง)
- `GT-184`/`GT-186` (`GAME_TEST_QUEUE.md`): ยังเป็น `BLOCKED-ON-RE-266`, ผู้ทำ **LANE-A** (โอน
  จาก LANE-UI แล้วตาม `COO-DECISION 20260905_1352`/`1845`) -- ไม่ใช่ของ LANE-UI อีกต่อไป ตรวจ
  แค่ว่าไม่มีการเปลี่ยนสถานะที่ต้องบริโภค (grep `GAME_TEST_QUEUE.md` = สถานะเดิม)
- `RE-286` (`TriggerResult` direction/caller chain, `CLIENT_RE_QUEUE.md`): ยัง **OPEN** ไม่มีผล
  จาก RE runner

## งานหลัก (คิว LANE-UI) -- สถานะ
ทั้งสี่ข้อยังติดเหมือนทุกรอบก่อนหน้า (UI-B/UI-A รอ `RE-266`, tracepath รอ LANE-A accessor, NPC
shop รอ LANE-DB interface) -- ไม่ตรวจซ้ำรายละเอียด (เช็คแล้วบันทึกครั้งเดียวในแผนตามกฎ) ⇒ หยิบงาน
สำรอง

## งานสำรอง -- ทำรอบนี้ (1): migrate 3 คลาสถัดไปของ `ui_community_social_wire.py`
โมดูลนี้มี 13 คลาส (จาก 16) ที่มีฟิลด์ wstring อย่างน้อยหนึ่งฟิลด์ ยังเรียก
`wire.encode_untagged_wstring`/`read_untagged_wstring` (บั๊กเดียวกับที่ห้าโมดูลพี่น้องแก้ไปแล้ว)
รอบนี้ย้าย 3 คลาสที่รูปร่างง่ายสุด (u64 + wstring + u8 หนึ่งฟิลด์) ไปใช้
`wire.wstring_tag`/`read_wstring_tag` (tag `0x48`) ตามแพทเทิร์นเดิมทุกประการ:
- `ChangeActorCommentFields`
- `ChangeActorPenNameFields`
- `RemoveBlackListFields`

อีก 10 คลาสที่เหลือ (`ChangeActorPersonalDataFields`, `CommunityPropertyChangedFields`,
`OpenLetterInABottleFields`, `OpenPenpalLetterFields`, `RequestorConfirmSoulMateMatchFields`,
`SetReceiveActiveChangeFields`, `TargetConfirmSoulMateMatchFields`, `ThrowLetterInABottleFields`,
`ThrowPenpalLetterFields`, `WriteBlankPenpalLetterFields`) เว้นไว้ให้รอบถัดไป (แบ่งทีละ 2-3
คลาสตามแผนของรอบ `me7s4u`) -- **ไม่ต่อสายเข้า `runtime.py`** (`COO-DECISION 1649`/`1745` ยังห้าม)
ตรวจแล้ว `grep -n "ui_community_social_wire" src/pirateforce_foundation/runtime.py` = 0 hit

Guard test (`tests/test_ui_express_community_social_migration_guard.py`) ยัง PASS โดยไม่ต้อง
แก้อะไร -- `_module_calls_untagged_pair` เช็คแค่ "โมดูลเรียกคู่เก่าที่ไหนสักที่ไหมภายในไฟล์" ตราบใด
ที่ยังเหลืออีก 10 คลาสไม่ได้ migrate มันยังเจอ true อยู่ (ตรวจสอบว่าตรงตามที่ pf-adversary
รอบ `me7s4u` ทิ้งคำถามไว้ท้ายไฟล์)

## `pf-adversary` -- คืนผลแล้วรอบนี้ (ไม่ใช่ PENDING)
สั่งทันทีหลังทำโค้ดเสร็จ (Agent tool มีจริง) ตรวจ diff (สามคลาส + docstring โมดูล) ห้าข้อ:
1-3, 5: ไม่พบบั๊ก (encode/decode คู่กันครบ, ไม่มีคลาสอื่นถูกแตะพลาด, docstring ตรงโค้ด, ไม่มี
   ตรรกะ offset ที่เขียนมือผิด)
4. **พบจริง**: เทส round-trip เดิมของสามคลาสที่ migrate ไม่มีจุดไหน assert ไบต์แท็ก wstring
   ตรง ๆ -- ถ้าอนาคตมีการ revert หกจุดเรียกนี้กลับเป็นคู่เก่าแบบเงียบ (เช่น merge ผิด/rebase
   ทับ) เทสเดิมจะยัง PASS ทั้งหมด (พิสูจน์จริงด้วยการ revert หกจุดในไฟล์ชั่วคราวแล้วรันเทส
   เดิม = 81 passed 0 failed) -- **แก้แล้วก่อน push**: เพิ่มเทส `test_wstring_field_uses_tag_0x48`
   ให้ทั้งสามคลาส (assert `payload[9] == 0x48` + corrupt ไบต์นั้นแล้วต้อง decode ไม่ผ่าน) แล้ว
   ยืนยันด้วยการ revert ซ้ำอีกครั้งว่าเทสใหม่แดงจริง (3 failed) ก่อน restore โค้ดที่ถูกต้องกลับมา
คำถามเปิดของ adversary (ไม่ใช่บั๊ก): เมื่อ migrate 10 คลาสที่เหลือในรอบถัดไป ๆ จะบังคับให้มี
assertion ระดับไบต์แบบนี้ยังไงไม่ให้พลาดซ้ำ -- ทิ้งไว้ให้รอบที่ทำ 10 คลาสถัดไปตัดสิน (เสนอ: ทำตาม
แพทเทิร์นเดียวกันทุกคลาสใหม่จากนี้)

## งานสำรอง -- ทำรอบนี้ (2): กู้ `pirate-force-server#961` + แก้ census ให้ไม่ผูก OS
จดหมาย `COO-DECISION 20260907_0148` (เข้ามาระหว่างรอบ ดูหัวข้อ "แหล่งความจริง" ข้อ 2) วัดเองว่า
`#961` ปิดเพราะ `gate-windows`'s `pytest_subset` แดง 9 ใน ณ ตอนนั้น แต่ห้า PR อื่นบนฐานเดียวกัน
ในชั่วโมงเดียวกัน (`#963`/`#964`/`#965`/`#967`/`#968`) ผ่าน `pytest_subset` บน Windows ปกติ --
สมมติ "Windows-gate แดงทั้งระบบ" ตก เหลือบั๊กในโค้ดของ `#961` เอง สั่งให้กู้ครั้งเดียวบนฐาน main
ปัจจุบัน พร้อมทำให้ census ไม่ผูก path separator/newline ของ Linux

**ขั้นที่ 1 -- กู้**: `git cherry-pick -x` สามคอมมิตจากกิ่งตาย `claude/inspiring-feynman-9dezrf`
(`eebb73d` เพิ่มโมดูล+เทส+อาร์ทิแฟกต์เดิม, `e5a5225` ตัด skip guard ที่ไม่ pin, `c1a0526` แก้บั๊ก
ที่ adversary รอบ `9dezrf` เจอ) -- cherry-pick สะอาด ไม่มี conflict

**ขั้นที่ 2 -- หา root cause แล้วแก้**: อ่าน `tools/pf_ui_wire_name_census.py` พบว่า
`_build_source_hits()` สร้างค่า `evidence` เป็น `f"{relpath}:{lineno}"` โดย
`relpath = path.relative_to(ROOT)` -- เป็นอ็อบเจกต์ `Path` ที่ `str()` ใช้ตัวคั่นตาม OS จริง (บน
Windows คือ `\`) ในขณะที่อาร์ทิแฟกต์ที่ commit ไว้ (`reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv`)
สร้างบน Linux ใช้ `/` ล้วน (ตรวจแล้วด้วย `grep -c '\\\\'` = 0 hit) ⇒ รันบน Windows ค่า evidence
สดจะไม่ตรงกับอาร์ทิแฟกต์ที่ commit ไว้เกือบทุกแถวที่เป็น SOURCE tier = `CENSUS DRIFT` แดงเป็นชุด
(น่าจะตรงกับ "9 failed" ที่วัดได้) แก้ด้วย `relpath.as_posix()` แทน `str(relpath)` -- จุดเดียวใน
ไฟล์นี้ที่แปลง `Path` เป็นสตริงเพื่อเก็บเป็นหลักฐานถาวร (จุดอื่นอ่านไฟล์ด้วย `read_text` ซึ่ง
translate universal-newline อยู่แล้วไม่ผูก OS) เพิ่ม `newline=""` ตอนเขียนอาร์ทิแฟกต์ให้ไม่โดน
text-mode translation ของ OS แปลง `\n` เป็น `\r\n` ด้วย

**ขั้นที่ 3 -- เทสกันการถอยกลับ**: เพิ่ม `WindowsPathSafetyTests` ใน
`tests/test_ui_wire_name_census.py` -- จำลองการคืนค่าแบบ Windows ของ `Path.relative_to()` ด้วย
`unittest.mock.patch.object` ให้คืน `PureWindowsPath` แทน (เพราะรันจริงบน Windows ไม่ได้ในเครื่องนี้)
แล้วยืนยันว่า evidence ไม่มี backslash เลย -- **พิสูจน์ด้วยการ mutate กลับเป็น `str(relpath)`
ชั่วคราวแล้วรันเทส = แดงจริง** (`AssertionError: '\\' unexpectedly found in
'src\\pirateforce_foundation\\ui_winemaking_wire.py:16'`) ก่อน restore โค้ดที่ถูกต้องกลับมา

`grep -n "ui_community_social_wire\|ui_express_wire" src/pirateforce_foundation/runtime.py` — ไม่
เกี่ยวกับงานนี้ ตรวจซ้ำเผื่อผลกระทบข้าม: ยัง 0 hit เหมือนเดิม

## `pf-adversary` (งานที่ 2) -- คืนผลแล้ว **หลัง push ครั้งแรก** (ล็อกยังไม่ปลด ทำต่อในรอบเดียวกันได้)
สั่งทันทีหลังทำโค้ดขั้นที่ 1-3 เสร็จ ผลไม่คืนทันเวลา push ครั้งแรก (บันทึก `ADVERSARY_PENDING`
ไว้ชั่วคราวแล้ว push ตามกฎ "ห้ามถือล็อกรอ") แต่ **ผลคืนก่อนจบรอบจริง** จึงบริโภคทันทีในรอบเดียวกัน
แทนการเลื่อนไปรอบหน้า (กฎ "รอบถัดไปหยิบเป็นงานแรก" ใช้เมื่อผลมาไม่ทันจริง ๆ เท่านั้น) --
**ผลพลิกข้อวินิจฉัยของรอบนี้เอง**: adversary สร้าง worktree ทิ้งแยกต่างหาก รัน
`tests/test_ui_wire_name_census.py` โดยไม่มี `../pf_bridge` sibling (รูปเดียวกับ Windows
gate runner ที่ checkout รีโปเดียว) แล้ว **วัดได้ตรง ๆ ว่า 10 จาก 11 เทสในไฟล์นั้นแดงจริง**
(ไม่ skip) เพราะไฟล์นี้ **ไม่มี precondition guard เลย** -- docstring เดิมของไฟล์ (สืบทอดจากรอบ
`9dezrf`) อ้างว่า "ทุกเทส census ข้ามรีโปในชุดนี้ไม่มี guard" โดยอ้าง
`tests/test_field_mob_tables_bg0002.py` เป็นตัวอย่าง แต่ **คำอ้างนั้นเท็จ** -- ไฟล์นั้นมี
`@BRIDGE_GAMEDATA.skip_unless_present()` ของตัวเองอยู่สองบรรทัดถัดจาก path ที่อ้างถึงจริง ๆ ·
guard เดิมเคยมีในไฟล์นี้ (`unittest.skipIf` ธรรมดา) แต่ถูกลบในรอบ `9dezrf` ด้วยคำอ้างเท็จเดียวกัน
เพราะ `pf_gate_preflight.py` เตือนว่าเป็น unpinned skip -- ทางแก้ที่ถูกคือ pin guard ไว้ ไม่ใช่ลบ
มันทิ้ง จำนวน "10 จาก 11 เทสแดง" นี้ **คือ** "9 failed" ของ `#961` เป๊ะ (ไฟล์เดิมมี 10 เทสก่อนรอบนี้
เพิ่มเทสที่ 11 เข้าไป) **ไม่เกี่ยวกับบั๊ก path-separator ในขั้นที่ 2 เลย**

**แก้แล้วทันที (ก่อน push จริง)**: เพิ่ม `UI_WIRE_CENSUS_INPUTS` ใน `tests/pf_preconditions.py`
(ตั้งชื่อไฟล์ทั้งสามที่เครื่องมือนี้อ่านจริงโดยตรง ไม่ใช้ key กว้างอย่าง `EXTERNAL_RE_TABLES`/
`BRIDGE_SIBLING` -- เหตุผลเดียวกับที่ `BRIDGE_SERIALIZER_TABLE` เขียนไว้ในตัวเอง) ประดับทั้งสาม
`TestCase` ในไฟล์เทสด้วย `@UI_WIRE_CENSUS_INPUTS.skip_unless_present()` และ pin ใน
`docs/PYTEST_SKIP_PINS.json` (11 เทส) **ยืนยันทั้งสองสถานะเครื่องจริงด้วยตัวเอง** (ไม่เชื่อ
adversary เฉย ๆ): สร้าง `git worktree` ทิ้งแยกต่างหากที่ไม่มี `pf_bridge` sibling อีกครั้ง (ของ
ตัวเอง หลังจาก adversary ทิ้ง worktree เดิมไปแล้ว) รันเทสได้ผล **11 skipped** ตรงกับเลข pin เป๊ะ
(ก่อนหน้านี้จะแดง 10) แล้วรันในเครื่องจริงที่มี sibling = **11 passed** ทั้งคู่ยืนยันด้วยคำสั่งจริง
ไม่ใช่คัดลอกผลจาก adversary · `tools_bridge`/`test_pytest_precondition_census.py` = 69 passed,
1153 subtests ไม่มี drift · บั๊ก path-separator ในขั้นที่ 2 **ยังเก็บไว้ไม่ revert** (เป็นบั๊กจริงที่
พิสูจน์แล้วด้วย mutation อีกทางหนึ่ง เพียงแต่ไม่ใช่สาเหตุที่ทำให้ `#961` แดงจริง)

**การแก้ guard ใหม่นี้เอง (commit `8144eb9`) ยังไม่ผ่าน adversary รอบที่สาม** -- เกินเวลาที่จะสั่ง
รอบใหม่แล้วรอผลในรอบนี้ (งบเวลา 75 นาที) บันทึก `ADVERSARY_PENDING pirate-force-server#974`
(เฉพาะ commit ล่าสุดนี้) ให้รอบหน้าหยิบเป็นงานแรกก่อน claim งานใหม่ใด ๆ ตามกฎ

## เทส
งานที่ 1: `PYTHONPATH=src python3 -m pytest tests/test_ui_community_social_wire.py
tests/test_ui_express_community_social_migration_guard.py -q` = 84 passed, 35 subtests
งานที่ 2 (หลังแก้ precondition): `PYTHONPATH=. python3 -m pytest
tests/test_ui_wire_name_census.py -v` = **11 passed** (เครื่องนี้มี `pf_bridge` sibling) ·
ยืนยันซ้ำด้วย `git worktree` แยกต่างหากที่ไม่มี sibling = **11 skipped** ตรงเลข pin เป๊ะ (ก่อนแก้
= 10 failed) · `tests/test_pytest_precondition_census.py` = 69 passed, 1153 subtests ไม่มี drift
ชุดเต็มครั้งที่ 1 (หลังงานที่ 1, `git merge origin/main`, main ไม่ขยับระหว่างนั้น) = 12554 passed,
379 skipped, 0 failed (0:08:24)
ชุดเต็มครั้งที่ 2 (หลังงานที่ 2 ขั้น 1-3 + cherry-pick + merge origin/main รับ `#969`) = 12581
passed, 379 skipped, 0 failed (0:08:24)
ชุดเต็มครั้งที่ 3 -- **commit สุดท้ายจริง** (หลังแก้ precondition guard จาก adversary + merge
origin/main ซ้ำรับ `#971`) = **12608 passed, 380 skipped, 0 failed** (0:08:29)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server --pr-body <file>
--pr-stage final` = PASS ทุกข้อ (cp874/skips/mainmerge/census/branch/bridgesize/queuegrowth/
filenamelen/scoreboard-manual/consumedstub/prbody) -- รันซ้ำหลัง merge origin/main ทั้งสองครั้ง
(ครั้งสุดท้าย `filenamelen` เตือนไฟล์ 101 ตัวอักษร แต่ PASS เพราะเป็นชื่อที่สืบทอดจาก base branch
เอง (stub `.CONSUMED.txt` ต่อท้ายชื่อจดหมายเดิมที่ยาว 100 ตัวอักษรอยู่แล้ว) ไม่ใช่ชื่อที่รอบนี้เลือก)

## ส่งอะไร (SHA/PR)
- `pf_bridge`: claim PR `#1605` (`[LANE-UI] round on8hbb: claim`) กิ่ง `claude/peaceful-pascal-on8hbb`
- `pirate-force-server`: PR `#974` (`[LANE-UI] round on8hbb: migrate 3 more Community_* classes
  off untagged wstring pair`) กิ่ง `claude/inspiring-feynman-on8hbb` -- ไม่ draft ตั้งแต่เปิด,
  marker `PF-AUTOMERGE: v4`, ยืนยันด้วย GET แล้ว -- **อัปเดตด้วยคอมมิตเพิ่มขึ้นบนกิ่งเดิมแทนการ
  เปิดใบที่สอง** (กติกา "หนึ่งใบต่อรีโปต่อรอบ") body อัปเดตให้ตรงเนื้อจริงหลังทุกคอมมิต -- 8 คอมมิต
  รวม: `dd54dfd` (งาน 1) + สามคอมมิต cherry-pick จาก `9dezrf` + `e96f84e` (งาน 2 ขั้น path-fix) +
  merge origin/main (`#969`) + `8144eb9` (งาน 2 แก้ precondition guard จาก adversary) + merge
  origin/main (`#971`) -- head sha `ad68b79`
- เลขใบใหม่รอบนี้: ไม่มี GT/RE ใหม่ -- งาน 1 ปิดหนี้ wire-format เดิมอีก 3 คลาส (เหลือ 10) งาน 2
  กู้ `#961` (n/327 census) กลับมาบน main พร้อมแก้ root cause จริง (ไม่ใช่แค่ที่เดาไว้แต่แรก) --
  ไม่ปลดล็อกฟีเจอร์ใหม่ให้ผู้เล่นทั้งคู่ (`NO_FEATURE_WAITING: pure wire-shape fix + internal
  tooling fix, ไม่มีตัวไหนต่อสายเข้าเกม`)

## จดหมายที่ส่งรอบนี้
ไม่มีจดหมายใหม่ที่ส่งออก -- แต่ **บริโภคแล้ว** จดหมายที่รับเข้า
`20260907_0148_COO-DECISION-ui0050-961-not-systemic-recover-once-path-agnostic-LANE-UI.md`
(ทำตามข้อ 1-2 ของคำตัดสินครบในรอบนี้) วาง stub `.CONSUMED.txt` คู่กับต้นฉบับ (ต้นฉบับไม่ลบ) +
สำเนาไป `consumed/` แล้ว

## รอบหน้าทำอะไร
0. **สั่ง `pf-adversary` บน commit `8144eb9` (แก้ precondition guard) เป็นงานแรกก่อน claim งานใหม่
   ใด ๆ** ตามกฎ (`ADVERSARY_PENDING pirate-force-server#974` เฉพาะคอมมิตนี้ -- อีกสองส่วนของ PR
   เดียวกันผ่าน adversary แล้วในรอบนี้) -- ถ้าเจอบั๊กจริงและ `#974` merge แล้ว เปิดใบแก้ทันที
1. migrate อีก 2-3 คลาสถัดไปของ `ui_community_social_wire.py` จาก 10 คลาสที่เหลือ
   (`ChangeActorPersonalDataFields`/`TargetConfirmSoulMateMatchFields`/
   `ThrowLetterInABottleFields` เป็นตัวเลือกที่ง่ายถัดไป -- รูปร่างเดียวกับสามคลาสที่ทำรอบนี้หรือ
   ใกล้เคียง) -- **อย่าลืมเพิ่ม `test_wstring_field_uses_tag_0x48`-style assertion ให้ทุกคลาสใหม่
   ทันที ไม่ใช่รอ adversary ชี้ซ้ำ** (บทเรียนจากรอบนี้)
2. ยืนยันว่า `pirate-force-server#974` merge จริงแล้ว (`git merge-base --is-ancestor <sha>
   origin/main`) ก่อนอ้างว่า `#961` "กู้แล้วจบ" -- รอบนี้แค่เปิด/อัปเดต PR ยังไม่ merge
3. เช็ค `GT-184`/`GT-186`/`RE-286` ซ้ำ (ยังไม่ขยับ ณ รอบนี้ ตรวจครั้งเดียวพอ ไม่ต้องตรวจซ้ำทุกรอบ
   จนกว่าจะมีจดหมายแจ้งว่าเปลี่ยน)
4. เมื่อ `ui_community_social_wire.py` ครบ 13/13 คลาส: ลบ `"ui_community_social_wire"` ออกจาก
   `_GUARDED_MODULES` ใน `test_ui_express_community_social_migration_guard.py` ตามคอมเมนต์ของ
   ไฟล์นั้นเอง (ตอนนี้ยังไม่ถึง เหลืออีก 10 คลาส)

## nonclaims
1. ไม่อ้างว่า `ui_community_social_wire.py` migrate ครบแล้ว -- เหลือ 10/13 คลาสยังไม่แตะ
2. ไม่อ้างว่าโมดูลนี้ต่อสายเข้า `runtime.py`/`vital_walk.py` -- ยังไม่ต่อ (grep ยืนยัน 0 hit)
3. ไม่อ้างว่าผู้เล่นเห็นอะไรใหม่วันนี้ -- ทั้งสองงานเป็นการปิดหนี้ wire-format/tooling เท่านั้น
4. ไม่อ้างว่าเทสใหม่ที่เพิ่ม (`test_wstring_field_uses_tag_0x48`) ครอบคลุมทุกช่องโหว่ที่เป็นไปได้
   -- ครอบเฉพาะกรณี revert กลับเป็นคู่เก่าแบบตรงไปตรงมาเท่านั้น (ตรงกับที่ adversary พิสูจน์จริง)
5. ไม่อ้างว่า path-separator (ขั้นที่ 2) คือสาเหตุที่ทำให้ `#961` แดง -- **วัดแล้วว่าไม่ใช่**
   (adversary จำลอง worktree ไม่มี sibling แล้วเห็น 10/11 แดงโดยไม่เกี่ยวกับ separator เลย) สาเหตุ
   จริงคือไม่มี precondition guard (ขั้นที่แก้ทีหลัง) -- path-separator ยังเป็นบั๊กจริงที่แยกกัน
   ไม่ใช่ตัวที่ทำให้ `#961` ถูกปิด
6. ไม่อ้างว่า `#961`/`ui_community_social_wire.py` งานที่ 1 merge เข้า main แล้ว -- ทั้งคู่เป็น PR
   เดียวกัน (`#974`) ที่เพิ่งเปิด/อัปเดต ยังรอเกต+ผู้ตรวจ
7. ไม่อ้างว่า commit แก้ precondition guard (`8144eb9`) ผ่าน adversary แล้ว -- ยังไม่ได้สั่งรอบที่สาม
   (เกินโควตา 2 ครั้ง/รอบ) บันทึก `ADVERSARY_PENDING` ไว้จริง ไม่ได้เขียนว่า "ผ่านแล้ว"

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (เป็นของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | ปิดหนี้บั๊ก wire-format เดิม (wstring ไม่มีไบต์แท็ก) อีกสามฟังก์ชันของโมดูล
แชท/ชุมชน (เหลือ 10 จาก 13) และกู้เครื่องมือนับความครอบคลุม n/327 กลับมาบน main พร้อมแก้ root cause
จริงที่ทำให้มันตกเกต Windows (ไม่มี precondition guard -- ไม่ใช่ที่เดาไว้แต่แรก) และแก้บั๊ก
path-separator จริงอีกจุดที่เจอระหว่างทาง -- ผู้เล่นยังไม่เห็นอะไรใหม่วันนี้ (ทั้งสองงานเป็น
เครื่องมือ/wire-shape เบื้องหลัง ไม่ต่อสายเข้าเกมจริง) | PR `pirate-force-server#974`
(PF-AUTOMERGE ยืนยันแล้ว, ชุดเต็ม 12608 passed 0 failed) + `pf_bridge#1605`

-- LANE-UI (round `on8hbb`)

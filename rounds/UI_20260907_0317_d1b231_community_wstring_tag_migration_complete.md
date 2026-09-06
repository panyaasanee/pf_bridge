# LANE-UI round `d1b231` -- 2026-09-07T03:17+07:00 start

## เวลา
ก่อน push (03:35+07:00) เทียบกับบรรทัดล่าสุดของ `notes_to_chief/_BRIDGE_HEARTBEAT.txt`
(`03:02:02+07:00`) ต่างกัน 33 นาที ไม่เกิน 60 นาที -- ไม่มีอะไรต้องแก้

## ล็อกรอบ
list `[LANE-UI] round *: claim` ที่เปิดอยู่ใน `pf_bridge` ก่อนเริ่มรอบ: **ว่าง**
(ใบที่เปิดอยู่ตอนนั้นคือ `#1615` K, `#1614` CS, `#1613` B, `#1611` A, `#1610` Q --
สายอื่นทั้งหมด ไม่ใช่ล็อกของเรา ห้ามแตะ) ⇒ เปิด claim `pf_bridge#1616` จากกิ่ง
`claude/kind-archimedes-d1b231` ทันที · กิ่งฝั่งเซิร์ฟเวอร์ `claude/ecstatic-franklin-d1b231`
-- ทั้งสองเป็นกิ่งที่ระบบมอบให้เซสชันนี้ ไม่ได้ตั้งชื่อเอง
list ซ้ำหลังเปิด: ยังเป็น `[LANE-UI]` ใบเดียว ไม่มีใบเก่ากว่าแข่ง

## แหล่งความจริงที่อ่านต้นรอบ (ตามลำดับ)
1. `NOW.md` (ตรวจล่าสุด COO รอบ `0148`) บรรทัด LANE-UI: `#967` ✅ → **กู้ `#961` ครั้งเดียว
   บนฐานปัจจุบัน + census ไม่ผูก path/newline** → งาน 2 `2032` แถบ n/327 · express/community
   **ยังห้ามต่อสายเข้า `runtime.py`** (`1649`)
   - ข้อ "กู้ `#961`" **ทำเสร็จไปแล้วในรอบก่อน (`on8hbb`) และ merge ลง main แล้วจริง** --
     ยืนยันด้วยคำสั่ง ไม่ใช่คำอ้าง: `git merge-base --is-ancestor 8144eb9 origin/main` = จริง
     และ `ad68b79` (head ของ `#974`) = จริงเช่นกัน · `origin/main` ตอนนี้คือ `cfd80d2`
     (merge ของ `#974`) ⇒ ข้อนี้ของ NOW.md **ปิดแล้ว เสนอ COO ลบออกจากบรรทัด LANE-UI**
     (ดูจดหมายที่ส่งรอบนี้)
2. กล่องจดหมาย: `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ที่ไม่มี `.CONSUMED.txt` คู่
   (เทียบด้วยชื่อไฟล์เต็ม `<ชื่อเดิม>.md.CONSUMED.txt` ตามที่รอบ `on8hbb` แก้ไว้) = **ว่าง**
   ทั้งตอนเริ่มรอบและตอน merge `origin/main` ซ้ำก่อน push
3. `AGENTS.md` section 7 -- อ่านครบ ไม่มีกฎใหม่กระทบงานรอบนี้
4. ไฟล์รอบล่าสุด `rounds/UI_20260907_0148_on8hbb_community_social_wire_partial_migration.md`
   หัวข้อ "รอบหน้าทำอะไร": ข้อ 0 สั่ง adversary บน `8144eb9` · ข้อ 1 migrate อีก 2-3 คลาส ·
   ข้อ 2 ยืนยัน `#974` merge · ข้อ 3 เช็ค `GT-184`/`GT-186`/`RE-286` (รอบก่อนเขียนเองว่า
   "ตรวจครั้งเดียวพอ ไม่ต้องตรวจซ้ำทุกรอบ" ⇒ ไม่ตรวจซ้ำรอบนี้ ตามกฎกันรอบกระดาษ)
5. คิวในไฟล์สาย -- ข้อ 1-2 (UI-B/UI-A) ยังติด `RE-266`, ข้อ 4 ติด LANE-A accessor, ข้อ 5 ติด
   interface ของ LANE-DB · blocker เดิมทั้งหมด บันทึกไว้ในแผนแล้ว ไม่ใช้รอบไปตรวจซ้ำ
   ⇒ หยิบงานสำรอง (โค้ดก่อน)

## รอบนี้ขยับ NOW/M ข้อไหน
ไม่ขยับ M ใด -- M2 เป็นของ A (ทาง (ก) `1910`), M3 รอ `GT-288` ของ B · บรรทัด LANE-UI ของ NOW.md
ขยับสองส่วน: (ก) "กู้ `#961`" ยืนยันแล้วว่าอยู่บน main จริง = ปิดได้ (ข) หนี้ wire-format
`0x48` ของสายนี้ **ปิดครบทั้งก้อน** (ดูด้านล่าง) · ผู้เล่นยังไม่ได้อะไรใหม่ -- นี่คือหนี้รูปเฟรม
ที่ต้องจ่ายก่อน `CORE-REQUEST` ต่อสายจะมีความหมาย ไม่ใช่ฟีเจอร์

## งานหลักของรอบ: ปิดหนี้ wstring tag `0x48` ทั้งโมดูลสุดท้าย
`ui_community_social_wire.py` เป็น **โมดูลสุดท้าย** ในหกโมดูลที่ยังเรียกคู่
`ui_social_wire.encode_untagged_wstring`/`read_untagged_wstring` (คู่ที่พิสูจน์แล้วว่าผิด --
ขาดไบต์แท็ก `0x48` -- ตั้งแต่รอบ `42w728`) ยืนยันด้วยคำสั่งไม่ใช่ความจำ:
`grep -rn "wire\.\(encode\|read\)_untagged_wstring(" src/pirateforce_foundation/` =
30 hit ทั้งหมดอยู่ในไฟล์นี้ไฟล์เดียว
รอบ `on8hbb` migrate ไป 3 คลาส เหลือ 10 -- **รอบนี้ทำครบทั้ง 10 คลาสในรอบเดียว** ไม่ใช่ 2-3
คลาสตามที่รอบก่อนวางไว้ เหตุผล: หลักฐานเป็นชุดเดียวกันทั้ง 16 คู่ฟิลด์ (ดูหัวข้อถัดไป) การแบ่ง
ทำอีก 4 รอบไม่ได้ลดความเสี่ยง แต่ทำให้ guard test ค้างสถานะ "ยังไม่ migrate" ต่อไปอีก 4 รอบ

คลาสที่ migrate รอบนี้: `ChangeActorPersonalData` · `CommunityPropertyChanged` ·
`OpenLetterInABottle` · `OpenPenpalLetter` · `RequestorConfirmSoulMateMatch` ·
`SetReceiveActiveChange` · `TargetConfirmSoulMateMatch` · `ThrowLetterInABottle` ·
`ThrowPenpalLetter` · `WriteBlankPenpalLetter` (30 จุดเรียก = encode 15 + decode 15)

## หลักฐานก่อนแตะโค้ด (ไม่ migrate ด้วยความเหมือนของแพทเทิร์น)
grep ทีละชื่อคลาสใน `notes_to_chief/reference_codex_attr/PF_A2_STRING_WIRE_TAG_DELTA.tsv`
(แหล่ง grep ที่ห้าตาม NOW.md `0256`): **ทั้ง 16 คู่ฟิลด์ (W และ R แยกกัน) มีแถว
`corrected_tag=0x48` ครบทุกคู่** -- ไม่มีฟิลด์ไหนถูก migrate เพราะ "หน้าตาเหมือนสามคลาสที่
ทำไปแล้ว" อย่างเดียว
**นอนเคลม (สำคัญ)**: `external/PF_SERIALIZER_FIELDS.tsv` **ยังสะกดแถวเหล่านี้ว่า
`UNTAGGED_WSTRING16LE_LEN32LE` อยู่** -- ตารางเดลตาคือ *การแก้* ตารางนั้น ไม่ใช่คำขัดแย้งกัน
บันทึกไว้ใน docstring ของโมดูลแล้วเพื่อไม่ให้รอบหน้ามาเถียงซ้ำ

## เทสที่เพิ่ม -- และเหตุผลว่าทำไมของเดิมไม่พอ
รอบ `on8hbb` (จากคำถามของ pf-adversary) เพิ่ม `test_wstring_field_uses_tag_0x48` แบบหนึ่งเมธอด
ต่อคลาส -- **เมธอดพวกนั้นเช็คเฉพาะ wstring ตัวแรกของคลาส** ⇒ `ChangeActorPersonalData` ตัวที่
2/3 และตัวที่สองของ `OpenLetterInABottle`/`OpenPenpalLetter`/`ThrowPenpalLetter` **ไม่มี
หลักฐานระดับไบต์เลย** รอบนี้จึงทำเป็นตาราง `AllWstringFieldsCarryTag0x48Tests` ที่เช็ค
*ทุกฟิลด์ wstring ของทุกคลาส* (13 คลาส) + เช็คว่าการทำลายไบต์แท็กใดก็ตามต้อง decode ไม่ผ่าน
- ออฟเซ็ตในตาราง **เขียนมือจากตำนานแท็ก** ไม่ได้คำนวณด้วย helper ตัวเดียวกับที่โค้ดใช้
  (ถ้าคำนวณ เทสจะเห็นด้วยกับ mutation ของ helper นั้นเสมอ = ไม่พิสูจน์อะไร)
- เทสที่สามผูกตารางเข้ากับ dataclass จริงของโมดูล: คลาสที่เพิ่มทีหลังโดยไม่มีแถวในตาราง = แดง
  ไม่ใช่ "ไม่ถูกคุ้มครองแบบเงียบ ๆ"
- **สามเมธอดเดิมของรอบ `on8hbb` เก็บไว้ครบ ไม่ลบ** (ตารางครอบคลุมทับ แต่การลบเทสไม่ใช่สิ่งที่
  รอบนี้จะทำเอง)
พิสูจน์ด้วย mutation จริง ไม่ใช่นับจำนวน assert:
| mutant | ผล |
| --- | --- |
| ถอย 30 จุดเรียกกลับเป็นคู่เก่าทั้งหมด | 21 failed |
| ถอย **ฟิลด์เดียว** (`ThrowPenpalLetter` wstring ตัวที่สอง) | 2 failed |
| ลบแถวเดียวออกจากตาราง | 1 failed |
(mutant ที่สองคือตัวที่พิสูจน์ว่าตารางเก่งกว่าเมธอดต่อคลาสจริง -- เมธอดเดิมจับไม่ได้)

## guard test: เปลี่ยนจาก pin ต่อโมดูล เป็นค่าคงที่ทั้งแพ็กเกจ
`tests/test_ui_express_community_social_migration_guard.py` มีเทส
`test_guarded_modules_still_use_the_untagged_pair_today` ที่ pin ว่า "โมดูลนี้ยังเรียกคู่เก่า
อยู่วันนี้" -- มีไว้กันไม่ให้เทส wiring ผ่านแบบว่างเปล่า พอ migrate ครบ เทสนี้ **แดงโดยการ
ออกแบบ** และข้อความของมันเองสั่งว่า "update this test's expectations alongside whatever round
migrated it" ⇒ รอบนี้แทนที่ด้วยค่าคงที่ที่แรงกว่า `NoFoundationModuleCallsTheUntaggedPairTests`:
**ไม่มีไฟล์ใดใต้ `src/pirateforce_foundation/` ยกเว้น `ui_social_wire.py` เอง (ที่นิยามคู่นี้)
ที่เรียกคู่นี้ได้** -- ดักโมดูล *ใหม่* ที่เขียนผิดตั้งแต่วันแรกโดยไม่ต้องมีใครมาเติมชื่อลงลิสต์
กันเทสกลายเป็นของว่าง 2 ชั้น: (ก) witness สังเคราะห์ที่พิสูจน์ว่า detector ยังคืน True ให้รูป
ที่ผิด (ในรีโปไม่มีไฟล์ไหนทำหน้าที่นี้ได้อีกแล้ว -- นั่นคือประเด็นของค่าคงที่นี้) (ข) assert
จำนวนไฟล์ที่สแกนจริง > 50
พิสูจน์ด้วย mutation: ใส่การเรียกคู่เก่ากลับเข้าไปหนึ่งจุดใน `ui_friend_wire.py` = 1 failed
**ครึ่ง wiring ของไฟล์นั้นไม่แตะเลย** ยังบังคับใช้กับทั้ง `ui_community_social_wire` และ
`ui_express_wire` ตาม `COO-DECISION 20260906_1649`

## ไม่ต่อสายเข้าเกม
`grep -n "ui_community_social_wire\|ui_express_wire" src/pirateforce_foundation/runtime.py`
= **0 hit** (ตรวจรอบนี้เอง) · `vital_walk.py` = 0 hit เช่นกัน · `1649` ยังห้ามอยู่ ไม่ละเมิด

## `pf-adversary` -- สั่งต้นรอบ **ผลคืนก่อนปลดล็อก** จึงบริโภคในรอบเดียวกัน
สั่งทันทีที่พร้อมเริ่มงาน (ไม่ใช่ก่อน commit) บน **`8144eb9`** ตามที่รอบ `on8hbb` สั่งไว้เป็น
งานแรก (`ADVERSARY_PENDING pirate-force-server#974`) -- ห้าคำถาม: ขอบเขต
`UI_WIRE_CENSUS_INPUTS` ตรงกับไฟล์ที่เครื่องมืออ่านจริงไหม · 11 skipped/11 passed จริงไหม
(ให้วัดเองสองสถานะ ห้ามเชื่อเลขใน commit message) · pin 11 ตัวตรงไหม · `as_posix()`+`newline=""`
ครอบคลุม OS-dependency ครบจริงไหม · อย่างอื่นในคอมมิตนั้น
ผลคืน **ก่อน** ปลดล็อก ⇒ บริโภคทันทีตามกฎ (ข้อ "รอบถัดไปหยิบเป็นงานแรก" ใช้เมื่อผลมาไม่ทันจริง)
**คำอ้าง 1/2/3 รอด** (วัดเองสองสถานะจริง, pin ตรง, ขอบเขตไฟล์ตรงเป๊ะสามไฟล์)
**คำอ้าง 4 ถูกหักล้าง** -- เก้าข้อบกพร่อง แก้ไปหกข้อในคอมมิตที่สองของ `#978`:
- **D2 (สูง · หักล้างคำอ้างของรอบก่อนโดยตรง)**: `_iter_py_files` ใช้ `sorted()` บน **Path
  object** ซึ่ง `PurePath.__lt__` เทียบ `_str_normcase` = บน Windows คือ `str(path).lower()`
  (backslash + case-fold) และเพราะ `_build_source_hits` เก็บ **hit แรก** ต่อชื่อ ขณะที่ **46
  จาก 160 ชื่อ SOURCE ถูกพบในหลายไฟล์** ⇒ ลำดับนี้ตัดสินค่า `evidence` ⇒ `CENSUS DRIFT`
  เฉพาะ Windows = รูปเดียวกับ `#961` เป๊ะ (adversary พิสูจน์ end-to-end ด้วยไฟล์ `gm2_probe.py`
  หนึ่งไฟล์) · แก้: sort ด้วย key `as_posix()` + กัน `rglob` ที่ case-insensitive บน Windows
  ด้วยเช็ค `suffix == ".py"` ตรง ๆ · **แยก `sort_py_files()` ออกมาเป็นฟังก์ชันสาธารณะ** เพื่อให้
  เทสป้อน `PureWindowsPath` ได้ (เทสที่ป้อน `Path` จริงจะผ่านทั้งกรณีถูกและกรณีผิดบน Linux =
  จับ revert ไม่ได้ที่ไหนเลย) · mutation: `sorted(files)` ไม่มี key = **1 failed บน Linux**
- **D3 (สูง)**: `test_rerun_is_deterministic` เรียก `build_rows()` สองครั้งติดกัน แต่
  `_CENSUS_INPUT_CACHE` ทำให้ครั้งที่สองใช้ทูเพิลเดิม = **เทียบผลแคชกับตัวเอง** (adversary
  พิสูจน์ด้วย `random.shuffle` แล้วเทสยังผ่าน) · แก้: clear แคชคั่นกลาง · mutation เดิมตอนนี้
  ทำให้แดงจริง
- **D4 (กลาง) + ส่วนหนึ่งของ D1 (สูง)**: guard ของรอบ `on8hbb` ใส่ระดับ **คลาส** ⇒
  `test_is_client_req_matches_both_wire_naming_conventions` (ฟังก์ชันบริสุทธิ์เหนือสตริงล้วน
  = เทสตัวเดียวที่ผ่านได้โดยไม่มี sibling) ถูก skip บน `gate-windows` ไปด้วย ทั้งที่มันเป็น
  **เทสเดียว**ที่ ground-truth กฎ `is_client_req` กับ convention จริง (อีกตัวเช็คกฎกับกฎเอง) ·
  ย้ายไปคลาส `IsClientReqRuleTests` ที่ไม่ guard · และเพิ่ม `SourceHitPathSafetyTests` สองตัว
  (temp tree + patch `census.ROOT`) คุมเส้นทาง `as_posix()` และนโยบายลำดับ โดยไม่ต้องมี sibling
  ⇒ **วัดบน worktree ที่ไม่มี sibling: 4 passed, 10 skipped** (ก่อนหน้านี้ 0 passed, 11 skipped)
  · mutation: ถอย `as_posix()` เป็น `str()` = 2 failed (หนึ่งในนั้นคือเทสใหม่ที่รันบนเกตได้)
- **D5 (กลาง)**: "10 จาก then-10 ตัวแดง" ขัดกับวงเล็บในประโยคเดียวกันที่บอกว่าตัวที่สิบผ่าน ·
  วัดใหม่: ไฟล์ then-10 = **9 failed / 1 passed** (ตรงกับ "9 failed" ของ `#961`), ไฟล์ 11 ตัว =
  10 failed / 1 passed · แก้ทั้งใน docstring และใน `docs/PYTEST_SKIP_PINS.json` (เลขผิดถูก
  พาเข้าไปในไฟล์ pin ซึ่งเป็นอาร์ทิแฟกต์ที่รอบหน้าจะอ้าง)
- **D6 (กลาง)**: ไฟล์เดียวกันยืนยันทั้ง "separator ไม่เกี่ยวเลย" (บรรทัด 29) และ "separator คือ
  สาเหตุจริงของ `#961`" (บรรทัด 122) · คืนความสอดคล้อง: **guard ที่หายไป** คือสิ่งที่ทำให้แดง
  9 ตัว (เทสตายก่อนถึงขั้นเทียบสตริง evidence ด้วยซ้ำ) ส่วนบั๊ก separator เป็นของจริง พิสูจน์
  แยกด้วย mutation และจะสร้าง drift ของมันเองทีหลัง
- **D9 (เบา)**: `docs/UI_WIRE_COVERAGE.md` non-claim เขียน 161 ขณะที่บรรทัด 67/89 และ
  `--summary` สดบอก 160
**สามข้อที่ไม่แก้เอง (เกินเขต) ⇒ ส่งจดหมาย COO**: D1 ส่วนที่เหลือ (`gate-windows` ไม่ checkout
`pf_bridge` เลย ⇒ เทสที่มี guard **214 ตัวทั้งรีโป** ไม่มีงานอัตโนมัติใดรันเลย -- กระทบทุกสาย
ไม่ใช่แค่สายนี้ และ `.github/` ไม่ใช่เขตเขียนของ LANE-UI) · D7 (เส้นทาง exit ที่ไม่ใช่ 0 ของ
เครื่องมือไม่เคยถูกรันในเทส -- ช่องคัฟเวอเรจ ไม่ใช่ false green ยืนยันด้วยมือแล้วว่าทำงานจริง) ·
D8 (`newline=""` ไร้ผลจริง เพราะ `read_text()` translate อยู่แล้ว + `.gitattributes` มี
`*.tsv text eol=lf` ตั้งแต่ `#865` ก่อน `e96f84e`)
🔴 **งานส่วนที่ 1 ของรอบนี้ (การ migrate 10 คลาส) ยังไม่ผ่าน adversary** -- สั่งครั้งที่สอง
ไม่ทันงบเวลา ⇒ `ADVERSARY_PENDING pirate-force-server#978` (ทั้งใบ) รอบหน้าหยิบเป็นงานแรก ·
ทำ self-review แทนตามกฎ: อ่านทุก hunk ใน `git diff --cached` (30 บรรทัดเป็นการแทนที่ชื่อ
ฟังก์ชันล้วน ไม่มี logic offset เขียนมือ) + mutation สามตัวข้างบน

## เทส
- `tests/test_ui_community_social_wire.py` = 75 passed, 76 subtests (ก่อนรอบนี้ 69 + 32)
- `tests/test_ui_express_community_social_migration_guard.py` = 13 passed, 223 subtests
- `tests/test_ui_wire_name_census.py` = **14 passed** (ก่อนรอบนี้ 11) · บน `git worktree` ที่
  ไม่มี `pf_bridge` sibling = **4 passed, 10 skipped** ตรงกับเลข pin ใหม่เป๊ะ (ก่อนรอบนี้
  0 passed, 11 skipped) · เก็บ worktree ด้วย `git worktree remove --force` **ไม่ใช้ `rm -r`**
  (`PANYA 1546`) ยืนยัน `git worktree list` เหลือรายการเดียว
- `tests/test_pytest_precondition_census.py` = 69 passed, 1170 subtests ไม่มี drift
- ชุดเต็มครั้งที่ 1 (หลังงานที่ 1, merge `origin/main` = `cfd80d2`) = 12612 passed, 380 skipped,
  26826 subtests, 0 failed (0:07:58)
- **ชุดเต็มครั้งที่ 2 = commit สุดท้ายจริง** (หลังงาน adversary + `git merge origin/main` รับ
  `6733292`) = **12615 passed, 380 skipped, 26825 subtests passed, 0 failed** (0:07:50)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PASS ทุกข้อ**
(cp874 / no new skips / main is in this branch / precondition census / branch mergeable /
bridgesize / queuegrowth / filenamelen / scoreboard-manual / consumedstub)
รันซ้ำพร้อม `--pr-body <file> --pr-stage final` = `[prbody] PASS - exactly one marker line`
ก่อนเปิด PR · หมายเหตุ: ทุกบรรทัดที่ *เพิ่ม* ในรอบนี้เป็น ASCII ล้วน (ตรวจด้วย
`git diff --cached | grep '^+' | grep -P '[^\x00-\x7F]'` = ไม่มีผลลัพธ์) -- บรรทัดไทยใน
docstring ของโมดูลเป็นของเดิมบน main ไม่ได้เพิ่มรอบนี้

## ส่งอะไร (SHA/PR)
- `pf_bridge`: claim PR `#1616` (`[LANE-UI] round d1b231: claim`) กิ่ง
  `claude/kind-archimedes-d1b231`
- `pirate-force-server`: PR **`#978`** กิ่ง `claude/ecstatic-franklin-d1b231` head
  **`30e91bc`** -- **ไม่ draft ตั้งแต่เปิด** มี `PF-AUTOMERGE: v4` ในบอดี้ตั้งแต่เปิด
  **ยืนยันด้วย GET แล้วว่า marker อยู่จริง** · สามคอมมิต: `8bef640` (migrate 10 คลาส) +
  `52b6995` (แก้ผล adversary หกข้อ) + merge `origin/main` (`6733292`) -- **อัปเดตบนกิ่งเดิม
  ไม่เปิดใบที่สอง** (กติกาหนึ่งใบต่อรีโปต่อรอบ) body อัปเดตให้ตรงเนื้อจริงหลังคอมมิตที่สอง ·
  สถานะตามจริง: **เปิดแล้ว รอ gate** (ยังไม่ merge ยังไม่อยู่บน main -- รอบหน้าต้องยืนยันด้วย
  `git merge-base --is-ancestor 30e91bc origin/main` ก่อนอ้างว่าเสร็จ)
- เลขใบใหม่รอบนี้: ไม่มี GT/RE ใหม่ · `NO_FEATURE_WAITING:` งานรอบนี้เป็นการแก้รูปเฟรมล้วน +
  ทำ guard ให้แรงขึ้น ไม่มีอะไรถึงมือผู้เล่นจนกว่า `CORE-REQUEST` ต่อสายจะได้รับอนุมัติ

## จดหมายที่ส่งรอบนี้
1. `20260907_0335_LANE-UI-TO-COO-961-recovered-on-main-now-line-can-close.md` (ADDRESSEE: COO)
   -- (ก) ยืนยันด้วยคำสั่งว่า `#961` ถูกกู้และอยู่บน main แล้ว เสนอตัดข้อนั้นออกจากบรรทัด
   LANE-UI ของ `NOW.md` (ผมไม่แตะ `NOW.md` เอง) · (ข) รายงานว่าหนี้ `0x48` ปิดครบทั้งหกโมดูล ·
   (ค) **สามข้อจาก adversary ที่เกินเขตของสาย** ให้ COO เคาะ: D1 (เกต Windows ไม่ checkout
   `pf_bridge` ⇒ เทสที่ guard ไว้ **214 ตัวทั้งรีโป** ไม่ถูกรันโดยงานอัตโนมัติใดเลย) · D7 · D8
   ติดป้าย `[สมมติของสาย LANE-UI - รอ COO ยืนยัน]` สำหรับทางที่เลือกเดิน (ทำเท่าที่อยู่ในเขต
   ตัวเอง ไม่แตะ `.github/`) แล้ว **เดินต่อ ไม่รอ** ตามกฎ
รับเข้า: ไม่มี (กล่องว่างทั้งต้นรอบและตอน merge ซ้ำ)

## รอบหน้าทำอะไร
0. **งานแรกก่อน claim งานใหม่ใด ๆ**: สั่ง `pf-adversary` บน `#978` (`ADVERSARY_PENDING
   pirate-force-server#978`) -- ใบของรอบก่อน (`#974`/`8144eb9`) **ปิดแล้ว** ผลคืนและบริโภคครบ
   ในรอบนี้ ⇒ ไม่ต้องสั่งซ้ำ · ถ้า `#978` merge ไปแล้วและ adversary เจอบั๊กจริง ⇒ **เปิดใบแก้
   ใหม่** ไม่ใช่แก้ใบเดิม
1. ยืนยัน `#978` merge จริงด้วย `git merge-base --is-ancestor 30e91bc origin/main` ก่อนอ้างว่า
   หนี้ `0x48` ปิดจบ -- รอบนี้แค่เปิด PR
2. **D7 ของ adversary (ยังไม่แก้ · อยู่ในเขตตัวเอง ทำได้เลย ไม่ต้องรอ COO)**: เพิ่มเทสให้
   เส้นทาง exit ที่ไม่ใช่ 0 ของ `tools/pf_ui_wire_name_census.py` (`CENSUS DRIFT: ... does not
   match` ⇒ `return 1`, และ `artifact ... does not exist` ⇒ `return 1`) ซึ่งไม่เคยถูกรันในเทส
   เลย -- เขียนแบบ **ไม่ต้องพึ่ง sibling** (temp artifact + patch) จะได้รันบน `gate-windows` ด้วย
3. งาน 2 ตาม NOW.md: `2032` แถบ n/327 -- โมดูล census อยู่บน main แล้ว ⇒ เดินต่อได้ ไม่มี blocker
4. เช็คว่ามี `COO-DECISION` ตอบจดหมาย `0335` (ข้อ D1: เกตไม่ checkout `pf_bridge` ⇒ เทส 214 ตัว
   ไม่ถูกรันที่ไหนเลย) หรือยัง -- ถ้ามี บริโภคและวาง stub
5. ถ้า `RE-266` ขยับ: กลับไปคิวข้อ 1-2 (UI-B ปุ่มออกจากเกม / UI-A กลับหน้าเลือกตัวละคร) ทันที
   -- สองข้อนี้อยู่เหนืองานสำรองทุกตัว

SCOREBOARD: COMING | ยังไม่มีอะไรใหม่ที่ผู้เล่นกดได้ -- รอบนี้ปิดหนี้รูปเฟรมตัวสุดท้ายของสาย: ทุกฟิลด์ข้อความในระบบ Community (จดหมายในขวด/penpal/soulmate/blacklist/comment/pen name) เข้ารหัสด้วยแท็ก 0x48 ที่ถูกต้องแล้ว แทนที่จะขาดไบต์แท็กแบบที่ไคลเอนต์จริงอ่านไม่ออก และคืนการคุ้มครองของ #961 กลับมาบนเกตจริง (4 เทสรันได้บน gate-windows จากเดิม 0) | pirate-force-server#978 (head 30e91bc, เปิดแล้วรอ gate) · pf_bridge#1616

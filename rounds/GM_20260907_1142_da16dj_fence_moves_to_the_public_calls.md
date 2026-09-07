# LANE-GM รอบ `da16dj` — ย้ายฟันไปคร่อมการเรียกที่ผู้ดูแลกดจริง + ใส่ตัวเฝ้าให้ตัว assert เอง

- เริ่มรอบ 2026-09-07T11:42+07:00 · ล็อก `pf_bridge#1693` (list ก่อนเปิด: ไม่มี `[LANE-GM] claim` ใบอื่น ·
  list ซ้ำหลังเปิด: `#1693` เป็นใบ GM ใบเดียว)
- กิ่ง: `claude/brave-galileo-da16dj` (bridge) · `claude/zealous-hawking-da16dj` (server)
- 🔴 **กิ่งเซิร์ฟเวอร์ตัดจาก `origin/claude/happy-bell-fx4p76` (หัวของ `pirate-force-server#1016`)
  ไม่ใช่จาก `main`** เพราะไฟล์ที่รอบนี้แก้ยังอยู่ใน PR นั้น — `tests/test_gm_login_scene_stage_descriptors.py`
  **ไม่มีบน `origin/main`** (`git ls-tree origin/main tests/ | grep login_scene` ไม่มีแถวนี้) ·
  `git merge-base --is-ancestor 1d1677d origin/main` = **NO** ⇒ **พึ่ง PR #1016** ·
  merge `origin/main` (`9d2d1c0`) เข้ากิ่งแล้ว (`c716183`) ก่อนรันชุดเต็ม
- อ่านตามลำดับ COMMON: `NOW.md` (ตรวจ `1041`) → กล่องจดหมาย → `AGENTS.md §7` → ไฟล์รอบ `fx4p76`

## รอบนี้ขยับ NOW/M ข้อไหน — ตอบตรง ๆ
**ไม่ขยับ M ข้อไหนเลย และผู้เล่นทำอะไรไม่ได้เพิ่ม** · `src/` เปลี่ยน **0 บรรทัด** เป็นรอบที่สามติด
- กฎบ้านสั่งชัด (`NOW.md`: "allowlist/skip pin/xfail ปิดผล adversary = ยังไม่จ่าย ... เว้นแต่เขียนเหตุ +
  **งานแรกรอบหน้า**") ⇒ งานแรกของรอบนี้คือ **หนี้ D1/D2/D3/D4 ของ `fx4p76`** ที่ addendum เขียนค้างไว้
  บวก **D5 ของ `s03veu`** ที่ค้างมาสองรอบ · ทั้งห้าจ่ายในรอบนี้
- `NOW.md` `0945` บรรทัด LANE-GM ("งานแรก = `CORE-REQUEST` จุดเสียบ `_Mirror`") **ปิดไปแล้ว**: ใบยื่น
  `10:15` · **ถอนเอง `10:50`** (adversary L1 หักข้ออ้าง) · chief ต่อสายให้ `11:09` (`#1022`) ทั้งที่ใบถูกถอน —
  รอบนี้บริโภคใบตอบและตอบกลับ chief แล้ว (§4) · ผมไม่แก้ `NOW.md` เอง (เขต Panya/COO)
- **`GT-279` ยังไม่ใช่ของสายนี้**: `grep -l "ADDRESSEE: \[?LANE-GM"` วันนี้คืนสี่ใบ ไม่มีใบใดตอบ `0556`/`0614`
  ⇒ **ว่างเพราะรอ K/RE** ไม่ใช่เพราะไม่มีงาน

## §1 D2 (สูง · ถูกที่สุด) — ตัว assert มีตัวเฝ้าแล้ว
`TheLeakDetectorItselfWorksTests` เดิมอ่าน `self.leaked` ตรง ๆ ⇒ มันเฝ้า **ตัวอ่าน** ไม่ใช่ **การ assert**
ตอนนี้ทุกเคสในคลาสนั้นเรียก `assert_no_descriptor_leaked()` เองและ assert ว่ามันทำอะไร: โยนเมื่อรั่ว ·
ไม่โยนเมื่อสะอาด · โยนเมื่อเคสลืมคร่อมหน้าต่าง (แขน sentinel)

| มิวแทนต์ | ก่อนรอบนี้ (`fx4p76`) | หลังรอบนี้ |
| --- | --- | --- |
| `return` ที่หัว `assert_no_descriptor_leaked` | `8 passed` (รอด) | **แดง 2 ใบ** `test_a_case_that_forgot_the_window_fails_the_assertion` · `test_a_descriptor_left_open_inside_the_window_fails_the_assertion` |
| `return` นั้น **บวก** `_pf_leak = os.dup(fd)` เหนือบรรทัด 736 | `8 passed` (รอด) | **แดง 2 ใบ** (ชื่อเดียวกัน) |
| ลบแขน sentinel (`assertIsNot ... _NeverWatched`) | — | **แดง** `test_a_case_that_forgot_the_window_fails_the_assertion` |
| `assertEqual(self.leaked, {})` ⇒ `assertEqual(self.leaked, self.leaked)` | — | **แดง** `test_a_descriptor_left_open_inside_the_window_fails_the_assertion` |

## §2 D1 (สูง) — ฟันย้ายไปอยู่รอบการเรียกสาธารณะ
**คำถามออกแบบที่รอบก่อนตอบไม่ได้ ตอบแล้ว**: หน้าต่าง fd ต้องคร่อม **การเรียกที่ผู้ดูแลกดจริง** —
`stage_login_scene` · `restore_login_scene` · `claim_login_scene` — ไม่ใช่ helper สองตัวที่บังเอิญมี
`os.close(fd)` อยู่แล้ว (สองที่ที่โอกาสรั่วน้อยที่สุด) · คลาสใหม่ `TheOperatorFacingCallsLeakNothingTests`
เรียกด้วย `os`/`tempfile` **ตัวจริง ไม่มี stand-in** ⇒ ทุก descriptor ที่ห่วงโซ่ทั้งเส้นเปิด อยู่ในหน้าต่าง
- เคส: stage สำเร็จ · stage ที่ถูกปฏิเสธ (ไม่ใช่ GM) · restore · claim · **5 stages ในหน้าต่างเดียว**
  (รูปเดียวกับที่ adversary วัด "fds before/after 5 stages: 4 9" — การรั่วหนึ่งใบต่อการเรียกกลายเป็นเลขคณิต
  เลข fd ที่ OS แจกซ้ำจึงซ่อนไม่ได้)

| มิวแทนต์ (probe ของ adversary เอง) | ก่อนรอบนี้ | หลังรอบนี้ |
| --- | --- | --- |
| ถือ handle ค้างใน `_write_entry_locked` (`os.open("/", O_RDONLY)` เก็บใน list ระดับโมดูล) | `8 passed` (รอด) | **แดง 5 ใบ**: `test_a_claim_leaks_nothing` · `test_a_restore_leaks_nothing` · `test_a_successful_stage_leaks_nothing` · `test_five_stages_in_one_window_do_not_grow_the_fd_table` · `test_the_module_has_exactly_the_two_opening_sites_this_file_pins` |
- **สี่คลาสเดิมยัง GREEN บนมิวแทนต์นั้น** — ซึ่งคือหลักฐานว่าคลาสใหม่คือสิ่งที่จับได้ ไม่ใช่ของเดิม

## §3 D4 + ครึ่งที่สองของ D1 — ตัวสแกน site เลิกเป็นการสะกด
`OPENING_SITE` (regex) ถูกแทนด้วย `opening_call_sites()` ที่ **parse ด้วย `ast`** · ตาม alias จาก
`from tempfile import mkstemp as _x` และจาก `_x = os.open` · รู้จัก `os.open` · `io.open` · `open` ·
`tempfile.mkstemp/NamedTemporaryFile/TemporaryFile`

| มิวแทนต์ | ก่อนรอบนี้ | หลังรอบนี้ |
| --- | --- | --- |
| **comment** ในโมดูลที่สะกด `tempfile.mkstemp(` และ `os.open(` | **แดงฟรี** (D4) | **`24 passed`** (ไม่แดง) |
| site ที่สามจริงผ่าน alias `_mkstemp(...)` + `from tempfile import mkstemp as _mkstemp` | `8 passed` (รอด) | **แดง 9 ใบ** (รวม `test_the_module_has_exactly_the_two_opening_sites_this_file_pins`) |
- เทสสองใบเล็งที่ตัวสแกนเอง: หกสะกดในซอร์สจำลอง (สี่ใบที่เคยหลุด + comment + docstring) และเคสที่
  **ต้องไม่นับ** (`tempfile.mkdtemp` คืนชื่อไม่ใช่ fd · `path.open()` ไม่ใช่ `os`)
- 🔴 **ไฟล์เขียนเองว่าตัวสแกนคือ tripwire ไม่ใช่ฟัน** — ฟันคือหน้าต่าง fd รอบการเรียกสาธารณะ (§2)

## §4 D3 — ตัวกรองนั้น "ไม่มีอะไรพิสูจน์ว่าจำเป็น" เพราะมัน **ตายแล้ว** ไม่ใช่เพราะฟันหลวม
adversary วัดว่า ลบสองบรรทัดที่กรอง `/proc/<pid>/fd` ออก ⇒ ยังเขียว · **ผมวัดต่อว่าทำไม**:
`os.listdir` ปิด descriptor ของตัวเองก่อน return ⇒ ตอน `readlink` ถามถึงเลขนั้น มันหายไปแล้ว
(**สามครั้งสามครั้ง**: `names=[0,1,2,3] resolved=[0,1,2] vanished=[('3', ENOENT)] procfd_targets=[]`)
⇒ แขน `except OSError: continue` คือสิ่งที่ทิ้งมันจริง · ตัวกรองไม่เคยทำงานเลย
**คำตอบคือลบโค้ดตาย ไม่ใช่หาพินที่ฉลาดกว่าให้โค้ดตาย** — โค้ดตายในฟันอ่านเป็นการป้องกันที่ไม่มีอยู่จริง
- `TheReaderItselfTests` พินแขนที่ทำงานจริง: `test_the_listing_names_a_descriptor_that_is_gone_before_it_is_resolved`
  (ลบ `try/except OSError` รอบ `readlink` ⇒ **แดง 18 ใบ**) · `test_the_reader_resolves_a_descriptor_that_is_actually_open`
  (`read_fd_table` คืน `{}` เสมอ ⇒ **แดง 2 ใบ**)
- 🔴 **ติดป้ายเองว่าอันไหนไม่ใช่พิน**: `test_the_reader_reports_no_descriptor_pointing_at_the_fd_directory`
  เขียน docstring ว่ามันเป็น **CHARACTERISATION ไม่ใช่พิน** — ไม่มีมิวแทนต์ไหนทำให้มันแดงได้ และรอบ `fx4p76`
  เคยเสนอ assert รูปนี้ราวกับว่ามันเฝ้าตัวกรอง ซึ่งไม่จริง

## §5 D5 ของ `s03veu` — ห้าแขนที่ไม่เคยถูกรัน ถูกรันแล้ว
`727-729` (short write ใน `_atomic_write_json`) · `739-741` (`os.replace` ล้ม) · `756-757`
(`original_bytes is None`) · `766` (short write ใน `_restore_bytes`) · `776-778` (`os.replace` ล้มตอน restore)
`_OsStandIn` รับฟอลต์เพิ่มสองตัว (`short_write` · `replace_error`) ข้าง `fsync_error` เดิม

| มิวแทนต์ | ผล |
| --- | --- |
| ลบ `temp_path.unlink(missing_ok=True)` ในแขน `os.replace` ล้ม (740) | **แดง** `test_a_rename_that_fails_removes_the_temp_file_and_raises` |
| ลบ `return` หลัง `path.unlink` ในแขน `original_bytes is None` | **แดง** `test_restoring_an_absence_removes_the_file_and_opens_nothing` |
| `if count <= 0:` ⇒ `if count < 0:` | 🔴 **ไม่ใช่แดงสะอาด — มัน HANG** (ดู nonclaims) |
- แขน `original_bytes is None` **ไม่เปิด descriptor เลย** ⇒ ใช้ `assert_no_descriptor_leaked` +
  `self.opened == []` ไม่ใช่ `assert_every_descriptor_released` (ซึ่งบังคับว่าต้องมีหนึ่งใบ)

## §6 บริโภคใบตอบของ chief (`CORE-REQUEST-GM-064`)
`20260907_1109_FROM_CHIEF-to-LANE-GM-core-request-gm-064-wired.md` → stub `.CONSUMED.txt` + สำเนาไป
`consumed/` · ตอบกลับ `20260907_1156_LANE-GM-TO-CHIEF-gm-064-seam-received-and-not-used-yet.md`
- chief ต่อสาย `build_console_mirror` ให้แล้วใน `#1022` **ทั้งที่ผมถอนใบไปตอน 10:50** — เวลาของ chief ถูกใช้กับ
  ใบที่ไม่ควรมี · ขอโทษเป็นลายลักษณ์อักษรในจดหมายแล้ว
- **รอบนี้ไม่เขียนเทสกับจุดเสียบนั้น** และเหตุผลไม่ใช่ตัวจุดเสียบ: ช่องที่ใบอ้างว่าจะปิด **ปิดอยู่แล้ว** (L3 ·
  grep เจอครบสาม: `test_gm_command_capture.py:1033` · `test_every_character_str_splitlines_breaks_on_is_folded` ·
  `test_gm_allowlist_probe.py:232`) · ถ้าสายนี้ต้องแตะมิเรอร์อีก จะเรียกผ่านโรงงาน ไม่ใช่ `_Mirror` ตรง ๆ

## หลักฐานและข้อจำกัด
- `pytest tests/test_gm_login_scene_stage_descriptors.py` = **24 passed** (เดิม 8)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
  (แดงหนึ่งครั้งระหว่างทาง: `[skips] RED - ADDS 1 UNPINNED skip marker` จาก `skipTest` ที่ผมเขียนใน `setUp` ⇒
  เปลี่ยนเป็นการ์ดต่อเมธอด `off_posix()` ตามรูปที่ไฟล์นี้ใช้อยู่แล้ว · ไม่เพิ่ม/ลบ/ย้าย skip · ไม่เพิ่มไฟล์เทสใหม่
  ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census`)
- ไฟล์เทส **ASCII ล้วน** (decode `ascii` ผ่านทั้งไฟล์)
- วิธีวัดมิวแทนต์ (รันซ้ำได้): worktree แยกที่ `git worktree add`, `PYTHONDONTWRITEBYTECODE=1`,
  ลบ `__pycache__` ระหว่างมิวแทนต์, รายงาน **ชื่อเทสที่ FAILED** ไม่ใช่ตัวเลข pass/fail, ทุกมิวแทนต์คืนด้วย
  `git checkout -f HEAD -- <ไฟล์>`
- ชุดเต็ม: รันบนต้นไม้หลัง `git merge origin/main` (`c716183`) — ผลอยู่ท้ายไฟล์นี้
- 🔴 `ADVERSARY_PENDING pirate-force-server#<PR ของรอบนี้>` — สั่ง `pf-adversary` บนกิ่งนี้ตั้งแต่คอมมิตแรก
  ผลยังไม่คืนตอนเขียนบรรทัดนี้ · **ห้ามอ่านว่า "ผ่าน adversary"**

## NONCLAIMS
- `src/` เปลี่ยน **0 บรรทัด** · รอบนี้ไม่ทำให้อะไรที่แดงวันนี้เขียว และไม่ทำให้ผู้เล่นทำอะไรได้เพิ่ม
- 🔴 **มิวแทนต์ `count <= 0` ⇒ `count < 0` ไม่ได้ถูก "ฆ่า" — มันทำให้เทส HANG** (`os.write` คืน 0 ตลอด ⇒
  `written += 0` วนไม่จบ) ผมฆ่าโปรเซสที่ 120 วินาที · การตรวจจับแบบค้างไม่ใช่แดงสะอาด และผมไม่รู้ท่าที่จะ
  ทำให้มันแดงโดยไม่แตะ `src/` ⇒ **จดเป็นหนี้ ไม่ใช่ชัยชนะ** (ดู "รอบหน้าทำอะไร" ข้อ 2)
- **ไม่อ้างว่า `login_scene_stage.py` ไม่รั่ว descriptor เลย** — อ้างได้แค่ว่า บนเส้นทางที่เคสในไฟล์นี้เดิน
  (สี่เส้นของ helper + ห้าเส้นของการเรียกสาธารณะ) ตาราง fd ไม่เปลี่ยน · เส้นที่ยังไม่มีเคสเดิน เช่น
  `_load_document` บนไฟล์เสียรูป และแขน symlink ของ `_write_entry_locked` **ยังไม่ถูกคร่อม**
- ตัวสแกน `ast` **ยังหลุดได้**: `os.pipe` · `os.dup` · `socket` · `codecs.open` · `getattr(os, "open")` ·
  การเรียกผ่านแอตทริบิวต์ของคลาส — ไฟล์เขียนไว้เองว่ามันคือ tripwire ไม่ใช่ฟัน
- `setUp` ของคลาสใหม่เรียก stage หนึ่งครั้ง **นอกหน้าต่าง** (อุ่นแคช) ⇒ **การรั่วที่เกิดเฉพาะการเรียกครั้งแรก
  ของโปรเซสจะไม่ถูกจับโดยสี่เคสแรก** · เคส 5 stages นับคร่อมการเรียกซ้ำ แต่ไม่ครอบการเรียกครั้งแรกจริง ๆ
- ครึ่ง Windows ของเหตุผลยัง **เป็นการให้เหตุผล ไม่ใช่การวัด** (ไม่มีโฮสต์ Windows) · ข้ออ้าง `pytest-xdist`
  ในหัวไฟล์ติดป้าย `[PROPOSED]` แล้ว (ไม่ได้ติดตั้งบนโฮสต์นี้ ไม่มีใครรันจริง)
- ไม่มีหลักฐานสองชั้น (client-observable / wire) — ทั้งหมดอยู่ใน process ไม่มีเฟรม ไม่มีจอ
- ไม่อ้างว่า `GT-279` · M2 · M3 · M4 ขยับ · ไม่แตะ `runtime.py`/`app.py`/`v141`/canonical DB/เขตสาย A,B
- `TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว — ไม่มีโค้ด production ไม่มี state ต่อ session ไม่มีเฟรมออกจากเซิร์ฟเวอร์

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **ผล `pf-adversary` ของรอบนี้** ถ้าคืนหลังปลดล็อก = งานแรก (กฎบ้าน)
2. **หนี้ที่รอบนี้เปิดเอง**: มิวแทนต์ `count < 0` ที่ค้างแทนที่จะแดง · และเส้นที่หน้าต่างยังไม่คร่อม
   (`_load_document` บนไฟล์เสียรูป · แขน symlink) · และการเรียกครั้งแรกของโปรเซส
3. **`GT-279`** ทันทีที่ K/RE ตอบ `0556`/`0614`
4. ถ้ายังว่าง: `docs/PROMOTION_BACKLOG.md` ปลดแฟล็กหนึ่งตัวในเขต `gm/` (อ่าน `SCOPE` ก่อนหยิบ ·
   docstring บอกว่าไม่เคยมีไคลเอนต์เห็นผล = ออกใบ attended ไม่ใช่ปลดแฟล็ก)

---

# §7 ผล `pf-adversary` **คืนก่อนปลดล็อก** · **ไม่สะอาด** · จ่ายในรอบนี้ ไม่ใช่สัญญารอบหน้า

ผลคืนตอน `12:10` ขณะที่ `pf_bridge#1693` **ยังไม่มี marker** ⇒ รอบยังไม่จบ ⇒ กฎ "ผลคืนหลังปลด = งานแรก
รอบหน้า" **ไม่ใช้กับกรณีนี้** · ถอน `PF-AUTOMERGE: v4` ออกจากบอดี้ `pirate-force-server#1025` ทันที
(GET ยืนยันแล้วว่าหายจริง) แก้ แล้วค่อยใส่กลับ · **แปดข้อ ห้าข้อจ่ายแล้ว สามข้อเป็นหนี้ที่เขียนชื่อไว้**

## จ่ายแล้วในรอบนี้ (วัดมิวแทนต์ยืนยันทุกข้อ · worktree แยก · `PYTHONDONTWRITEBYTECODE=1`)

| ข้อ | สิ่งที่ adversary หักได้ | สิ่งที่ทำ | มิวแทนต์ยืนยัน |
| --- | --- | --- | --- |
| **D-5** (กลาง) | ลบ `assertFalse(...linux...)` ในแขน `None` ⇒ `24 passed` — ประโยค "ฟันที่เงียบต้องไม่หน้าตาเหมือนเขียว" **ไม่เคยถูกวัด** | เคสใหม่ `test_a_table_that_could_not_be_read_fails_the_assertion_on_linux` | ลบการ์ดนั้น ⇒ **แดง 1 ใบ** (ชื่อเคสใหม่) |
| **D-3** (สูง · จ่ายบางส่วน) | หกแขนของห่วงโซ่สาธารณะไม่เคยถูกรัน · **`_restore_bytes` เข้าไม่ถึงจากฟันเลย** ("end to end" จริงเฉพาะเส้นสำเร็จ) | เคสใหม่ `test_a_stage_whose_rename_fails_restores_and_leaks_nothing` ฉีด `PermissionError` ที่ `os.replace` ⇒ ห่วงโซ่เดินลง `REASON_WRITE_FAILED` และผ่าน `_restore_bytes` จริง | ทำให้ `_restore_bytes` ไม่ทำอะไรเลย ⇒ **แดง 6 ใบ** รวมเคสใหม่ |
| **D-4** (กลาง-สูง) | `ast.Import` ไม่ถูกดู ⇒ `import os as _o; _o.open()` หลุด · และ docstring **อ้างเท็จ**ว่า "renaming the import is not a way through" · เทส `..._opens_nothing` **บันทึกความเท็จ** (`pathlib.Path.open` เปิด descriptor จริง) | ตาม `import os as _o` และ `_o = os` แล้ว · docstring **ลิสต์สิ่งที่มันตาบอด** ตามที่วัด · เคสใหม่ `test_the_spellings_this_scanner_is_measured_blind_to` พินลิสต์นั้น (10 สะกด · subTest) · เปลี่ยนชื่อเทสที่พูดเท็จ | ขยายตัวสแกน (`("os","pipe")`) ⇒ **แดง 1 subtest** ⇒ ใครขยายต้องแก้ลิสต์ตั้งใจ |
| **D-1** (สูง · จ่ายเป็นคำสารภาพ) | คอมเมนต์ใน `setUp` อ้างว่าเคส 5 stages ครอบการเรียกอุ่นเครื่อง — **วัดแล้วเท็จ** (หน้าต่างคร่อมแค่ลูป) | ลบคำอ้าง เขียน **KNOWN HOLE** แทน พร้อมรูปการรั่ว (`if not _held:`) ที่ทำให้มันหลุด | ยืนยันเอง: การรั่วครั้งเดียวต่อโปรเซส ⇒ ฟัน fd **ไม่จับ** (จับได้เฉพาะ tripwire ถ้าสะกดตรง) |
| **D-8** (ต่ำ) | docstring ยกข้อความ `"short write restoring ..."` ราวกับพินไว้ ทั้งที่เปลี่ยนข้อความแล้วยังเขียว | เขียนตรง ๆ ว่า **ข้อความนั้นสังเกตไม่ได้** เพราะ `raise` ถูกกลืนโดยดีไซน์ และไม่พินมันด้วยการเทียบสตริงในซอร์ส | — (เป็นการแก้คำอ้าง ไม่ใช่การเพิ่มฟัน) |

## หนี้ที่ยังไม่จ่าย — เขียนชื่อไว้ ไม่ปิดด้วย allowlist/xfail/skip อะไรทั้งสิ้น
- 🔴 **D-2 (สูงสุด) ยังไม่จ่าย**: บน Windows `read_fd_table()` คืน `None` ⇒ จุดเรียก
  `assert_no_descriptor_leaked` ทั้งหมดเป็น no-op **บนแพลตฟอร์มเดียวที่บั๊กนี้ถึงตาย** · adversary วัดว่า
  ฉีดการรั่วจริง + จำลอง Windows ⇒ `27 passed` · และ **การแก้ `[skips]` ของรอบนี้ทำให้สัญญาณเงียบลงอีก**
  (จาก skip ที่นับได้ เป็น pass ที่นับไม่ได้) — แต่ `skipTest` ที่ไม่มีแถวใน `docs/PYTEST_SKIP_PINS.json`
  (ไม่ใช่เขตผม) = preflight แดง ⇒ **เขียนใบ ASK-COO แล้วเดินต่อ** ตาม COMMON:
  `notes_to_chief/20260907_1211_LANE-GM-ASK-COO-what-measures-descriptors-on-windows.md`
  ทางที่เลือกไปแล้ว `[สมมติของสาย LANE-GM - รอ COO ยืนยัน]`: วัด **ผล** ของการรั่วแบบข้ามแพลตฟอร์ม
  (ฉีด `PermissionError` ที่ `os.replace` — สามเคส รันบน Windows ด้วย) **และเขียนในหัวไฟล์ว่านั่นไม่เท่ากับ
  การนับ descriptor** ห้ามอ่านสองอย่างนี้เป็นอย่างเดียวกัน
- **D-3 ที่เหลือ**: ห้าแขนของ `_write_entry_locked`/`_load_document` ยังไม่มีเคสเดิน
  (`REASON_CONFIG_NOT_WRITABLE` · `REASON_CONFIG_UNREADABLE` · `EXISTING_ENTRY_NOT_ADMISSIBLE` ·
  `REASON_WRITE_FAILED` ทาง verify · `_load_document` โยนบนไฟล์เสียรูป) · และ
  `test_a_refused_stage_leaks_nothing` **ไม่เคยไปถึง `_write_entry_locked` เลย** (คืนที่บรรทัด 315)
- **D-1 ที่เหลือ**: การรั่วครั้งเดียวต่อโปรเซสยังมองไม่เห็น — ต้องออกแบบ ไม่ใช่เพิ่มเคส
- **D-6** (สงสัย): เปลี่ยนแขน `except OSError` จาก *ทิ้ง* เป็น *บันทึกใต้ target ปลอม* ⇒ ยังเขียว
- **D-7**: มิวแทนต์ `count <= 0` ⇒ `count < 0` **ค้าง ไม่ใช่แดง** (adversary ยืนยันทั้งสองที่: 721 และ 765)
- **ตัวเลข `391 passed` ของรอบ `i3evov`** re-derive ที่ HEAD ไม่ได้แล้ว (ตัวเลือกเดียวกันวันนี้ = `415 passed`)
  ติดป้ายรอบกำกับไว้ ไม่ใช่ตัวเลขลอย แต่ผู้รีวิวตรวจซ้ำไม่ได้ — จดไว้ให้รอบหน้าตัดสินว่าจะเขียนใหม่หรือลบ

## สิ่งที่ adversary พยายามหักแล้วหักไม่ลง (นับเป็นผลเหมือนกัน)
- มิวแทนต์ D5 แปดตัว (ทั้ง `_atomic_write_json` และ `_restore_bytes`) **ตายครบทุกตัว** พร้อมชื่อเทส
- จุดประสงค์ดั้งเดิมของไฟล์ยังยืน: `sed '736s/os.close(fd)/pass/'` ⇒ **7 FAILED** ใต้ `-k "login_scene or stage"`
- re-derive ตัวเลขในหัวไฟล์ครบ: บรรทัด `733/736/770/773` ตรง · พิน 4 ตรง · `GM_ONE`/`278`/`1` ตรงกับ
  `test_gm_login_scene_stage.py` · "25/25" รันซ้ำ 25 ครั้งได้ 25/25 · "`module.os is os` ทุกโมดูล" เดินทั้งแพ็กเกจแล้วจริง
- `read_fd_table` คืน `{}` หรือ `{0: "/dev/null"}` ⇒ แดงทั้งคู่

## รอบหน้าทำอะไร (แทนที่รายการข้างบนทั้งหมด · เรียงตามที่ adversary จัดอันดับ)
1. **D-2**: รอคำเคาะ COO จากใบ `1211` · ถ้า COO ตอบ "ต้องมีสัญญาณบน Windows" ⇒ ยื่น `CORE-REQUEST`
   ขอแถวใน `docs/PYTEST_SKIP_PINS.json` (เขต chief) **ใบเดียว จุดเดียว** ไม่ใช่การขอทีละฟิลด์ ·
   ถ้า COO ตอบ "รับได้" ⇒ เขียนคำเคาะลงหัวไฟล์แล้วปิดข้อนี้
2. **D-3 ที่เหลือ**: ห้าแขนที่ยังไม่มีเคสเดิน — เริ่มที่ `REASON_CONFIG_UNREADABLE` และ `_load_document`
   บนไฟล์เสียรูป (สองอันนี้เขียนได้โดยไม่ต้องมี stand-in ใหม่)
3. **D-1**: ออกแบบก่อนเขียน — จะจับการรั่วครั้งเดียวต่อโปรเซสได้อย่างไรโดยไม่พึ่งลำดับการรันของ pytest
4. **D-6 · D-7** และตัวเลข `391` ที่ re-derive ไม่ได้
5. **`GT-279`** ทันทีที่ K/RE ตอบ `0556`/`0614`
6. ถ้ายังว่าง: `docs/PROMOTION_BACKLOG.md` ปลดแฟล็กหนึ่งตัวในเขต `gm/`

## สถานะ PR ตอนปลดล็อก (ตามจริง ห้ามอ่านว่า landed)
- **`pirate-force-server#1025`** — เปิดแล้ว **ไม่ draft** · **ถอน marker ระหว่างรอบเพื่อแก้ผล adversary
  แล้วใส่กลับหลังแก้เสร็จ** · GET ยืนยัน marker · **รอ gate** (ห้ามอ่านว่า landed/เสร็จ/อยู่บน main —
  รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)
- **`pirate-force-server#1016`** — comment `SUPERSEDED-BY: #1025` ต้นบรรทัด · **ไม่ปิดเอง** ปล่อยให้ reaper
  ปิด · `#1025` = หัวของ `#1016` + คอมมิตของรอบนี้ ⇒ ไม่มีงานของรอบ `fx4p76` หายไป
- **`pf_bridge#1693`** — claim ของรอบนี้ · เติม marker เป็นขั้นสุดท้ายหลังใบนี้ push

## หลักฐานสุดท้าย (ต้นไม้ที่ push จริง `e338bab`)
- `pytest tests/test_gm_login_scene_stage_descriptors.py` = **27 passed + 10 subtests** (เดิม 8 passed)
- `pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
- ชุดเต็ม: **13270 passed · 384 skipped · 0 failed · 36952 subtests · 541.88 s**
  (รันสามครั้งในรอบนี้: `13267/384` บนต้นไม้ก่อนผล adversary · `13270/384` หลังแก้ ·
  และครั้งที่สามบน `e338bab` ซึ่งเป็นต้นไม้ที่ push จริง — ตัวเลขข้างบนคือครั้งที่สาม)
- คำสั่งรันซ้ำมิวแทนต์ได้ทั้งชุด: `git worktree add <path> <sha>` · `PYTHONDONTWRITEBYTECODE=1` ·
  `find . -name __pycache__ -type d -exec rm -rf {} +` ระหว่างมิวแทนต์ ·
  `timeout 90 python3 -m pytest tests/test_gm_login_scene_stage_descriptors.py -q` ·
  คืนสภาพด้วย `git checkout -f <sha> -- <ไฟล์>` · **รายงานเป็นชื่อเทสที่ FAILED เสมอ**
- `pf-adversary` **คืนผลแล้วในรอบนี้** (ไม่ใช่ `ADVERSARY_PENDING`) · ผล **ไม่สะอาด** · §7 คือรายการเต็ม
  ห้ามอ่านบรรทัดใดในไฟล์นี้ว่า "ผ่าน adversary" — ที่ถูกคือ "จ่ายห้าข้อ เหลือหนี้สามข้อที่เขียนชื่อไว้"

SCOREBOARD: NONE | รอบนี้ผู้เล่นยังทำอะไรไม่ได้เพิ่ม (src เปลี่ยน 0 บรรทัด) — สิ่งที่ขยับคือฟันของ GM ย้ายไปคร่อมการเรียกที่ผู้ดูแลกดจริง ตัว assert มีตัวเฝ้าของตัวเอง และห้าแขนที่ไม่เคยถูกรันถูกรันแล้ว ส่วนช่องบน Windows ยอมรับตรง ๆ ว่ายังไม่ปิดและส่งคำถามถึง COO | pf_bridge#1693 · pirate-force-server#1025 · e338bab · GM_20260907_1142_da16dj

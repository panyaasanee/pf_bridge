# LANE-GM รอบ `fx4p76` — ยื่น `CORE-REQUEST-GM-064` (จุดเสียบ `_Mirror`) + จ่าย D1/D3 ของ `s03veu`

- เริ่มรอบ 2026-09-07T10:13+07:00 · ล็อก `pf_bridge#1680` (ตอนล็อก ไม่มี `[LANE-GM] claim` ใบอื่นเปิดอยู่
  — list สองครั้ง ก่อนและหลังเปิด)
- กิ่ง: `claude/clever-rubin-fx4p76` (bridge) · `claude/happy-bell-fx4p76` (server)
- 🔴 **กิ่งเซิร์ฟเวอร์ตัดจาก `origin/claude/zealous-hawking-s03veu` (หัวของ `pirate-force-server#1010`)
  ไม่ใช่จาก `main`** เพราะงานรอบนี้คือการแก้ไฟล์ที่ยังอยู่ใน PR นั้น · `git merge-base --is-ancestor
  745e075 origin/main` = **ไม่ใช่บรรพบุรุษ** ⇒ ยังไม่อยู่บน main · merge `origin/main` (`b302d55`)
  เข้ากิ่งเป็นขั้นสุดท้ายแล้ว (`915db65`) · **พึ่ง PR #1010**
- อ่านตามลำดับ COMMON: `NOW.md` (`0945`) → กล่องจดหมาย → `AGENTS.md §7` → ไฟล์รอบ `s03veu`

## รอบนี้ขยับ NOW/M ข้อไหน — ตอบตรง ๆ
**ไม่ขยับ M ข้อไหนเลย** และไม่มีอะไรที่ผู้เล่นทำได้เพิ่ม · บรรทัด `LANE-GM` ใน `NOW.md` `0945` สั่งสองอย่าง
และรอบนี้ทำทั้งสอง:
1. **"งานแรก = `CORE-REQUEST` จุดเสียบ `_Mirror` จริงให้เทส GM (chief คิว (4)) · หยุดจ่ายทีละฟิลด์"**
   ⇒ ทำเป็นงานแรกจริง (§1) · **ฟิลด์ที่เจ็ดไม่จ่าย** ตามที่ใบ `0945` สั่ง
2. งาน adversary ที่คืนหลังปลดล็อกรอบ `s03veu` (D1/D3) = งานแรกรอบถัดไปตามกฎบ้าน ⇒ ทำใน §2
   (`NOW.md`: "allowlist/skip pin/xfail ปิดผล adversary = ยังไม่จ่าย ... เว้นแต่เขียนเหตุ + งานแรกรอบหน้า")
- **`GT-279` ยังไม่ใช่ของสายนี้**: รอ K/RE ตอบใบ `0556` + `0614` · ตรวจแล้วรอบนี้ ยังไม่มีใบตอบใน
  `notes_to_chief/` ⇒ **ว่างเพราะรอ K/RE** ไม่ใช่เพราะไม่มีงาน
- "ดัน PR `vxr32s` ให้เขียว" ใน `NOW.md` **ค้างอยู่**: PR ของรอบนั้น merge ไปแล้วก่อนรอบ `s03veu`
  (รอบ `s03veu` รายงานไว้แล้ว) · ผมไม่แก้ `NOW.md` เอง (เขต Panya/COO)

## §1 งานแรก — `CORE-REQUEST-GM-064` (ยื่นแล้ว)
`notes_to_chief/20260907_1015_CORE-REQUEST-GM-064-mirror-seam-one-factory-no-app-boot.md` (8,187 B)
ขอ **ฟังก์ชันสาธารณะหนึ่งตัว** ใน `runtime_console.py` (เขต chief · ไม่แตะเอง):
`build_console_mirror(console, retained) -> TextIO` คืน `_Mirror` ตัวเดียวกับที่ `app.py` ติดตั้ง
โดยไม่เปิดไฟล์และไม่แตะ `sys` · และให้บรรทัด 84-85 เรียกฟังก์ชันนั้นเอง (กัน drift)
- **ค้นก่อนขอ ครบสามข้อ**: `_Mirror(` เจอ 2 จุด ทั้งคู่ใน `runtime_console.py:84,85` (ผู้เรียกเดียวคือ
  `RuntimeConsole.__init__` ซึ่ง `mkdir` + เปิดไฟล์ `"x"` + เขียน `sys.stdout/err` ระดับโปรเซส) ·
  `RuntimeConsole|runtime_console` ใน `tests/` = 6 ไฟล์ · `server_console_live` ใน `tests/` = 2 ไฟล์
- **เบี่ยงจากถ้อยคำ COO หนึ่งจุด เขียนกำกับในใบแล้ว**: ขอให้ `encoding` **ไม่**เป็นพารามิเตอร์ เพราะค่าที่
  `_Mirror` ประกาศคือสิ่งเดียวที่เทสมีหน้าที่วัด · ถ้า chief/COO ยืนยันแบบมีพารามิเตอร์ ผมทำตามได้
- ใบนี้บริโภค `20260907_0945_COO-DECISION-gm0851-...` แล้ว (stub `.CONSUMED.txt` + สำเนาไป `consumed/`)
- 🔴 **ไม่มีโค้ดใหม่ในฝั่ง GM จากใบนี้ในรอบนี้** — เทสปลายทางเขียนได้ต่อเมื่อจุดเสียบลง ตามที่ใบสั่ง

## §2 จ่าย D1/D3/D4 ของ `s03veu` — `tests/test_gm_login_scene_stage_descriptors.py` (`src/` เปลี่ยน 0 บรรทัด)
### D1 (สูงสุด) — ฟันเขียว 5/5 ขณะที่ descriptor รั่วบนเส้นทางที่มันถูกสร้างมากัน
เพิ่ม **assert ที่เป็นคุณสมบัติจริงตัวเดียวของไฟล์นี้**: เทียบ **ตาราง fd ทั้งใบ** (`/proc/self/fd`,
`{fd: target}`) คร่อม **การเรียกโมดูลเท่านั้น** ผ่าน context manager `watching_the_fd_table()` ·
`assert_no_descriptor_leaked()` รันเป็น assert แรกของทุกเส้นทาง · มี sentinel `_NeverWatched` ⇒ เคสที่
"ลืมคร่อม" แดง ไม่ใช่เขียวเงียบ
- **นับ site ที่ "เปิด" แทนที่จะนับ site ที่ "ปิด"** (`tempfile.mkstemp(|os.open(` = **2 จุดวันนี้**) —
  D1 ชี้ว่าการเปิดคือทางเดียวที่การรั่วเข้ามาได้ และเป็นสิ่งเดียวที่การนับ "ปิด" มองไม่เห็นเชิงโครงสร้าง
- **คลาสใหม่ `TheLeakDetectorItselfWorksTests`** เล็งตัวตรวจไปที่การรั่วจริงหนึ่งใบและหน้าต่างสะอาดหนึ่งใบ
  ⇒ `read_fd_table` ที่คืนค่าคงที่ **ทำให้ไฟล์นี้เขียวไม่ได้อีก**
- **POSIX เท่านั้น** — อ่าน `/proc/self/fd` ไม่ได้บน Linux ⇒ **แดง** (ฟันที่เงียบต้องไม่หน้าตาเหมือนเขียว)
  บนโฮสต์ที่ไม่มี `/proc` การ assert คุณสมบัติทำงานไม่ได้ และไฟล์เขียนบอกไว้ตรง ๆ

**วัดเอง (worktree แยก · ล้าง `__pycache__` + `PYTHONDONTWRITEBYTECODE=1` ระหว่างมิวแทนต์ = จ่าย D2/D7):**

| มิวแทนต์ | ก่อนรอบนี้ (`s03veu`) | หลังรอบนี้ |
| --- | --- | --- |
| `_pf_leak = os.dup(fd)` เหนือ `os.close(fd)` ที่ 736 | `5 passed` (รอด) | **แดง** `test_the_success_path_closes_before_it_renames` |
| site ที่ห้า `_write_sidecar` (`mkstemp` ไม่ปิดเลย) | `5 passed` (รอด) | **แดง** `test_the_module_has_exactly_the_two_opening_sites_this_file_pins` |
| `read_fd_table` คืน `{}` เสมอ | — | **แดง** `test_a_descriptor_left_open_inside_the_window_is_reported` |
| `read_fd_table` คืน `None` เสมอ | — | **แดง 6 ใบ** |

**มิวแทนต์เดิมสี่ตัวยังตายครบ** และรายงานเป็น **ชื่อเทสที่ FAILED ไม่ใช่ตัวเลข pass/fail** (D2):
`733` → `test_a_failure_before_the_rename_closes_and_leaves_no_temp_file` · `736` →
`test_the_success_path_closes_before_it_renames` · `770` →
`test_a_restore_that_fails_still_closes_and_still_does_not_raise` · `773` →
`test_restoring_a_file_closes_its_descriptor` (ทุกตัวบวก `test_the_four_literal_close_statements_are_still_there`)

### D3 (กลาง) — การ refactor ที่ถูกต้องและไม่รั่ว ทำให้ฟันแดง
ไม่ลบ assert และไม่ทำให้มันหลวม · **เขียนป้ายให้ตรง** ว่าอันไหนคุณสมบัติ อันไหนกลไก:
docstring แยกสามข้อชัด (PROPERTY = ตาราง fd · MECHANISM = `EBADF` ของ fd ใบเดียว · MECHANISM =
`self.closed == [fd]`) และ **ข้อความ assert ของกลไกบอกทางออกเอง**
- วัดบนการเขียนใหม่แบบ `with os.fdopen(fd, "wb")` (ถูกต้อง ไม่รั่ว): **แดง 3 ใบ** — และทั้งสามคือ
  **ฟันกลไกล้วน** · ข้อความที่ได้คือ
  `[] != [11] : the module did not ask to close the descriptor it opened with a literal os.close(fd);`
  `if the fd-table assertion above is green you refactored HOW it closes -- update this file deliberately`
  ⇒ assert คุณสมบัติ (ตาราง fd) **เขียว** บนการ refactor นั้น ซึ่งคือสิ่งที่ D3 ขอ

### D4 (ต่ำ) — การอ้างอิงชี้ผิดไฟล์
`command_capture.py` ไม่มี `962`/`970` (`grep -c` = 0) · ประโยคนั้นอยู่ที่ `tests/pf_gm_capture_mocks.py:72`
⇒ แก้ข้อความในไฟล์แล้ว

### D2/D5/D6 — สถานะตามจริง
- **D2 (วิธีวัด) จ่ายแล้ว** ด้วยการล้าง cache + รายงานชื่อเทส (ตารางข้างบน)
- **D6 จ่ายบางส่วน**: docstring บอกชื่อสมมติฐานที่ขาดหายไปแล้ว (**CPython refcounting** ปิด descriptor ที่
  ตัวเทสเองเปิด) และบอกว่า `pytest-xdist` ปลอดภัยเพราะเป็น **โปรเซส** แยก ไม่ใช่เธรด
- **D5 ยังไม่จ่าย** (บรรทัดที่ไม่เคยถูกรัน: `727-729`, `766`, `739-741`, `776-778`, `756-757`) — งานรอบหน้า
  ข้อ 2 · ไม่ปิดด้วย allowlist/xfail อะไรทั้งสิ้น

## หลักฐานและข้อจำกัด
- `pytest tests/test_gm_login_scene_stage_descriptors.py` = **8 passed** (เดิม 5)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
- ไฟล์เทส **ASCII ล้วน** (decode `ascii` ผ่านทั้งไฟล์) · ไม่เพิ่ม/ลบ/ย้าย skip · ไม่เพิ่มไฟล์เทสใหม่
  ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census`
- ชุดเต็ม: รันบนต้นไม้หลัง `git merge origin/main` (`915db65`) — ผลอยู่ท้ายไฟล์นี้
- 🔴 `ADVERSARY_PENDING pirate-force-server#<PR ของรอบนี้>` — สั่ง `pf-adversary` ต้นงานแล้ว
  ผลยังไม่คืนตอนเขียนใบนี้ · **ห้ามอ่านว่า "ผ่าน adversary"**

## NONCLAIMS
- `src/` เปลี่ยน **0 บรรทัด** อีกรอบ — รอบนี้ไม่ทำให้อะไรที่แดงวันนี้เขียว และไม่ทำให้ผู้เล่นทำอะไรได้เพิ่ม
- **ไม่อ้างว่า `login_scene_stage.py` ไม่รั่ว descriptor เลย** — อ้างได้แค่ว่า **บนเส้นทางที่เทสสี่ใบนี้เดิน**
  ตาราง fd ไม่เปลี่ยน และ site ที่เปิดมีสองจุดตามที่ตรึง
- ไม่มีหลักฐานสองชั้น (client-observable / wire) — ทั้งหมดอยู่ใน process ไม่มีเฟรม ไม่มีจอ
- ครึ่ง Windows ของเหตุผลยัง **เป็นการให้เหตุผล ไม่ใช่การวัด** (ไม่มีโฮสต์ Windows) เหมือนที่ `#1010` เขียนไว้
- ไม่อ้างว่า `GT-279` · M2 · M3 · M4 ขยับ · ไม่แตะ `runtime.py`/`app.py`/`v141`/canonical DB/เขตสาย A,B
- `TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว — ไม่มีโค้ด production ไม่มี state ต่อ session ไม่มีเฟรมออกจากเซิร์ฟเวอร์

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **ผล `pf-adversary` ของรอบนี้** ถ้าคืนหลังปลดล็อก = งานแรก
2. **D5 ของ `s03veu`**: บรรทัดที่ฟันไม่เคยเดินถึง (`727-729`, `766`, `739-741`, `776-778`, `756-757`) —
   สองอาร์มหลัง `os.close` สำคัญที่สุด
3. **`CORE-REQUEST-GM-064`**: chief ตอบ ⇒ เขียน `tests/test_gm_unlink_stuck_line_on_the_real_mirror.py`
   ทันทีตามที่ใบสัญญาไว้ · chief ตีกลับ ⇒ ส่งกลับ COO ไม่เขียน `_Mirror` เอง
4. **`GT-279`** ทันทีที่ K/RE ตอบ `0556`/`0614`
5. **คืน `PF-AUTOMERGE: v4` ให้ `#1010`** หรือปิดใบนั้นแทน PR ของรอบนี้ — ดู "สถานะ PR" ข้างล่าง

## สถานะ PR ตอนปลดล็อก (ตามจริง ห้ามอ่านว่า landed)
- **`pirate-force-server#1016`** — เปิดแล้ว **ไม่ draft** · มี `PF-AUTOMERGE: v4` · **GET ยืนยัน marker แล้ว** ·
  **รอ gate** (ห้ามอ่านว่า landed/เสร็จ/อยู่บน main — รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)
- **`pirate-force-server#1010`** — comment `SUPERSEDED-BY: #1016` ต้นบรรทัดแล้ว (ตามระเบียบ reaper
  `FROM_CHIEF_R370` · เลขเป้าหมายมากกว่าเลขใบตัวเอง) · **ไม่ปิดเอง** ปล่อยให้ reaper ปิด ·
  `#1016` = หัวของ `#1010` + สองคอมมิต ⇒ ไม่มีงานของรอบ `s03veu` หายไป
- **`pf_bridge#1680`** — claim ของรอบนี้ · เติม marker เป็นขั้นสุดท้ายหลังใบนี้ push
- 🔴 **เขียนผู้เขียนคอมมิตของรอบนี้ใหม่** (`furyscore@gmail.com` → `noreply@anthropic.com` ตาม stop-hook
  ของเครื่อง) ⇒ force-with-lease เฉพาะกิ่งของตัวเองสองใบ · **คอมมิตของรอบ `s03veu` ไม่ถูกแตะ**
  (ยังเป็น `f550205`/`e424d2e`/`745e075` เดิมบน `origin/claude/zealous-hawking-s03veu`) ·
  ต้นไม้ก่อน/หลังเขียนใหม่เท่ากันเป๊ะ (`806e1c6`)
- ชุดเทสเต็มบนต้นไม้สุดท้าย (`806e1c6` · ลบ `state/*.sqlite3` ก่อน):
  **13157 passed · 384 skipped · 0 failed · 36767 subtests · 545.57 s**
  (รันสองครั้งในรอบนี้: ครั้งแรก 552.32 s ก่อนแก้ docstring · ครั้งที่สองบนต้นไม้ที่ push จริง)

SCOREBOARD: NONE | ไม่มีอะไรที่ผู้เล่นทำได้เพิ่มรอบนี้ — งานแรกตามคำสั่ง NOW.md 0945 คือใบขอจุดเสียบ (กระดาษ) และงานที่สองคือปิดช่องที่ adversary เจาะทะลุฟันของรอบก่อน (เทส · src เปลี่ยน 0 บรรทัด) | pf_bridge#1680 · pirate-force-server#1016 · CORE-REQUEST-GM-064 · GM_20260907_1013_fx4p76

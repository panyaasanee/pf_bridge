# LANE-GM รอบ `lkwmkp` -- เกต Windows แดงเพราะ mock ของ `os.close` ทิ้ง descriptor ค้าง ไม่ใช่โค้ดที่แก้

เริ่ม 2026-09-06T19:13+07:00 · claim `pf_bridge#1546`

## จุดเริ่ม (ลำดับตาม COMMON)

1. `NOW.md` — ไม่มีข้อไหนสั่งสาย GM ตรง ๆ นอกจาก "LANE-GM: `/lv` = GT-277 ✅ → P-3 ปุ่ม GM 3 หน้า
   = `GT-279`" ซึ่งรอเครื่อง Panya (สะพาน pull ไม่เข้าเครื่องตาม `SYNC_STUCK` 1816-1844) ⇒ ทำต่อไม่ได้รอบนี้
2. กล่องจดหมาย `ADDRESSEE: LANE-GM` — เปิดค้างสองฉบับ ทั้งคู่เป็นเรื่องเดียวกัน:
   `20260906_1828_SYNC-NOTICE-...-pr926-closed-never-merged` และ `...-pr937-closed-never-merged`
3. ไฟล์รอบก่อน (`q7950e`) "รอบหน้าทำอะไร" ข้อ 1 สั่งไว้ตรง ๆ: เช็คสถานะ `#937` ก่อนอื่น **ถ้าแดงอีกด้วย
   ลายเซ็นเดียวกันให้ถือว่าเป็นปัญหาจริงของ PR นี้ ไม่ใช่ flake**

`#937` แดงจริงด้วยลายเซ็นเดิม (`gate` = failure, commit `0471e12`, run `34029288153`) ⇒ งานรอบนี้คือ
ไล่ให้เจอสาเหตุจริง ไม่ใช่เปิดใบที่สามด้วยโค้ดเดิม

## สาเหตุที่เจอ (ไล่จากโค้ด เพราะล็อกอ่านไม่ถึง)

**เทสของรอบก่อน ๆ mock `os.close` ด้วย `side_effect=OSError(...)` เฉย ๆ ⇒ descriptor จริงไม่เคยถูกปิด**

```python
mock.patch.object(command_capture.os, "close", side_effect=OSError("simulated close ENOSPC"))
```

- บนลินุกซ์ handle ที่ค้างไม่ขวางอะไรเลย: `os.unlink` ในโค้ดที่ถูกทดสอบสำเร็จ ⇒ เทสผ่าน (11586 passed)
- บน Windows ไฟล์ถูกล็อกตราบใดที่ยังมี handle เปิดอยู่ ⇒ `_best_effort_unlink` ใน
  `command_capture._capture_raw` ล้มด้วย sharing violation ⇒ โค้ดคืน `CaptureFileNotVerifiedRemoved`
  แทน `OSError` ธรรมดา = **เทสหกใบล้มพร้อมกัน** และ handle ที่ค้างทำให้ `TemporaryDirectory.cleanup`
  ใน `addCleanup` ล้มตาม = **error ตอน teardown**
- เทสที่ mock `os.close` มี **หกใบพอดี** (`test_gm_command_capture.py` ×3 · `test_gm_command_dispatch.py`
  ×2 · `test_gm_activity_cheat_code_dispatch.py` ×1) ตรงกับ `6 failed` ที่เกตรายงานทั้งสองครั้ง
  (`#926` run `34024390383` · `#937` run `34029288153` ทั้งคู่ `6 failed ... 3 errors`)

**สองเอเจนต์ทำซ้ำได้ตรงเลข `6 failed / 3 errors` แยกกัน** (จำลอง Windows ด้วย conftest ที่ทำให้
`os.unlink`/`os.remove` โยน `PermissionError [WinError 32]` เมื่อ path ยังถูกเปิดค้างอยู่ใน process
— จำลองความหมายเดียวเท่านั้น ที่เหลือเป็นลินุกซ์จริง):
- control (ไม่มี conftest): 92 passed · จำลอง Windows: **6 failed, 3 errors, 86 passed** บนสามไฟล์เทสเดิม
- แยก FAILED/ERROR: ใบที่ **ไม่ได้** mock `os.unlink` เปลี่ยนคลาสข้อยกเว้น (`CaptureFileNotVerifiedRemoved`
  แทน `OSError`) ⇒ FAILED · ใบที่ mock `os.unlink` ไว้แล้ว body ผ่าน แต่ `TemporaryDirectory.cleanup`
  ใน `addCleanup` ล้ม ⇒ ERROR ตอน teardown
- 🔴 nonclaim: สองเอเจนต์ **ไม่ตรงกันว่าใบไหนคือสามใบที่ ERROR** (ชุด {1,2,5} กับ {1,2,3} ตามลำดับที่แต่ละตัว
  รายงาน) — ยังไม่มีใครได้ชื่อจริงจากล็อก CI ⇒ อ้างเฉพาะกลไกกับจำนวนรวม ไม่อ้างการจับคู่ทีละใบ

## ทำไมไม่อ่านล็อกให้จบเรื่อง

`gate-windows.yml` พิมพ์ traceback จริง (บรรทัด 462-471) แต่พิมพ์ **ก่อน** skip census ที่พ่นรายการ skip
ครบ 143 รายการ (~60 KB) ⇒ `get_job_logs` ที่อ่านได้แต่ `tail_lines`: 245 บรรทัด = 58,819 อักขระ (ยังอยู่ในโซน
census) · 700 บรรทัด = เกินโควตา 185,022 อักขระของ tool · Azure blob = proxy 403 · ไม่มี JUnit artifact
⇒ เขียนใบขอให้ chief พิมพ์ชื่อเทสที่แดงเป็นบรรทัดท้ายสุดของ job:
`notes_to_chief/20260906_1921_LANE-GM-ASK-COO-gate-failed-names-must-print-last.md` (ADDRESSEE: COO)
**ไม่รอคำตอบ** ตามกฎ "เขียนคำถาม แล้วเดินต่อ"

## สิ่งที่ทำ

1. เพิ่ม helper `close_that_really_closes_then_fails(message)` (นิยามเต็มพร้อมเหตุผลใน
   `tests/test_gm_command_capture.py`, สำเนาย่อในอีกสองไฟล์เทส) — ปิด fd จริงก่อน แล้วค่อย raise
   ⇒ ตรงกับสัญญาจริงของ POSIX ด้วย: `close()` กิน descriptor ไปแล้วแม้จะคืน error (ซึ่งเป็นเหตุผลที่โค้ดที่ถูก
   ทดสอบไม่ retry) ⇒ เทสเดิมทั้งหกใบวัดสิ่งเดิมทุกอย่าง แต่ไม่ทิ้ง handle ค้างอีก
2. เทสใหม่หนึ่งใบ `test_the_close_failure_helper_leaves_no_descriptor_open` — สอดส่อง `os.open` เก็บ fd
   แล้วยืนยันว่า `os.fstat(fd)` โยน `OSError` หลังจบ ⇒ **ถ้าใครเปลี่ยน helper กลับไป raise เฉย ๆ เทสนี้แดง
   บนลินุกซ์ทันที** บั๊กที่เห็นเฉพาะ Windows จะไม่กลับมาเงียบ ๆ อีก
   - มิวแทนต์: ถอด `real_close(fd)` ออกจาก helper → `1 failed, 29 passed` (เทสใบนี้ใบเดียว) ✅
3. ห้าคอมมิตของ `#926`/`#937` (D9 floor · D10 refund · close contract · short-write loop) ยกมาทั้งชุดด้วย
   `git merge` จากกิ่ง `claude/keen-pasteur-q7950e` **ไม่แก้ตรรกะเดิมแม้แต่บรรทัดเดียว** — สิ่งที่แก้รอบนี้
   อยู่ในไฟล์เทสเท่านั้น

## เกตและหลักฐาน

- `pytest tests/test_gm_command_capture.py tests/test_gm_command_dispatch.py
  tests/test_gm_activity_cheat_code_dispatch.py`: 93 passed, 5 subtests passed
- ชุดเต็มบนต้นไม้ที่ merge `origin/main` (`e926f7a`) แล้ว: **12464 passed, 373 skipped, 26235 subtests passed, 0 failed, 0 errors** (422.20s) — รันหลัง merge `origin/main` เป็นขั้นสุดท้ายแล้ว
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS** (รันก่อน push ตามลำดับที่ `AGENTS.md §7` ต้องการ ไม่ใช่หลังเหมือนรอบ `q7950e`)
- PR เซิร์ฟเวอร์: **`pirate-force-server#944`** เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` (GET ยืนยันแล้ว)
  รอ gate — สิบสามคอมมิต (ห้าคอมมิตกู้จาก `#926`/`#937` + สองคอมมิตของรอบนี้ + merge)

## ADVERSARY

สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน · **ผลคืนแล้วก่อน push** (ไม่ใช่ `PENDING`) · หกข้อ (D1-D6)
เอเจนต์รายงานว่าไม่ได้สร้าง worktree และไม่เขียนอะไรลง `/home/user/pirate-force-server` เลย
(ทดลองบน export `git archive` ในสแครชแพด) ตรวจแล้ว `git status --porcelain` ว่างจริงตอนรับผล

- **D1** (CONFIDENT · MEASURED): สาเหตุเกตแดง = fd ค้างจาก mock `os.close` ⇒ **ตรงกับที่รอบนี้แก้ไปแล้ว**
  (เอเจนต์หาเจอเองก่อนเปิดอ่านคอมมิต `67f8ab7`)
- **D2** (MEASURED): ต้นไม้ที่แก้แล้วรันใต้การจำลอง Windows = **93 passed, 0 failed, 0 errors**
  พร้อมตัวตรวจ fd รั่วต่อเทส: ไม่มี descriptor ค้างชี้เข้า temp dir เหลือเลยสักใบ
- **D3** (CONFIDENT · MEASURED · **แก้แล้วรอบนี้**): helper ถูก copy ไว้สามไฟล์ แต่เทสยามคุมแค่ copy
  ที่อยู่ข้างตัวเอง — เอเจนต์ลบ `real_close` ออกจาก copy ใน `test_gm_command_dispatch.py` แล้ว
  **ลินุกซ์เขียวหมด 93 passed** ส่วนการจำลอง Windows แดง 2 failed 1 error ⇒ ยามเดิมพิสูจน์สถานะของ
  copy เดียว ไม่ใช่โหมดความล้มเหลว ⇒ ย้ายไปนิยามเดียวที่ `tests/pf_gm_capture_mocks.py` ให้ทั้งสามไฟล์
  import · ข้อจำกัดที่เอเจนต์ชี้ต่อ (ยามยืนยันเรื่อง **เลข fd** ซึ่ง OS แจกซ้ำได้ ⇒ อาจ false-RED ใต้
  `pytest-xdist` ไม่ใช่ false-green) เขียนกำกับไว้ในตัวเทสแล้ว ยังไม่เปลี่ยนวิธียืนยันรอบนี้
- **D5** (MEASURED · **แก้แล้วรอบนี้**): รอบ `gn7gk5`/`79ahzl` เปลี่ยน `try/finally` เป็น `except OSError`
  ⇒ ข้อยกเว้นที่ไม่ใช่ `OSError` (`MemoryError` ตอน slice · `KeyboardInterrupt` ตอนปิดเครื่อง) ทิ้ง fd ค้าง
  **และ** ไฟล์ `O_CREAT|O_EXCL` ค้างบนดิสก์ ในฟังก์ชันที่สัญญาว่าไม่มีวันเหลือไบต์ — เติม
  `except BaseException:` ที่ปิด/ลบ/โยนต่อของเดิมไม่แปลงคลาส + เทสถอย มิวแทนต์ผ่าน (ถอดสาขาออก → แดง 1 ใบ)
- **D4** (PROPOSED · ยังไม่ทำ): `_best_effort_unlink` ยิงครั้งเดียวไม่ retry — บน Windows ที่ Defender/
  indexer ถือ handle ชั่วขณะ ทำให้บัญชี GM ที่ไม่ผิดถูกหักโควตาถาวรจนรีสตาร์ต ⇒ ใบถาม COO
  `notes_to_chief/20260906_1940_LANE-GM-ASK-COO-windows-unlink-lock-charges-innocent-gm.md`
  (เป็นการเปลี่ยนพฤติกรรม production ที่มี timing เกี่ยว — ไม่ยัดเข้า PR ที่กำลังไล่เกตแดงให้จบ)
- **D6** (MEASURED · ยังไม่ทำ): เทส byte-exact ของรอบ `5f6xhf` เทียบไฟล์สองใบที่เขียนด้วย path เดียวกัน
  บนแพลตฟอร์มเดียวกัน = self-consistency ไม่ใช่การพิสูจน์เนื้อไฟล์ · `O_BINARY` ไม่ปรากฏใน `src/`
  `tests/` `tools/` เลย ⇒ ถ้า CRT `_fmode` เป็น text mode บน Windows เนื้อไฟล์อาจกลายเป็น CRLF โดย
  ไม่มีเทสใดเห็น (แต่ `gm/commands.py` มี `os.open` แบบเดียวกันและเขียวบนเกตมาตลอด ⇒ ไม่ใช่หกใบนี้)
  → รอบหน้า

## ยังไม่ทำ / รอบหน้าทำอะไร

1. **เช็คสถานะ PR เซิร์ฟเวอร์ของรอบนี้ก่อนอื่น** (แบบเดียวกับที่รอบนี้เช็ค `#937`) — ถ้าเกตยังแดงด้วย
   ลายเซ็นเดิม แปลว่าสมมติฐาน fd ค้างยังไม่ครบ ให้กลับไปหาสาเหตุจากรายการเทสจริง (ตอนนั้นน่าจะมี
   บรรทัดสรุปท้ายล็อกแล้วถ้า COO เคาะใบ `1921`)
2. P-3 ปุ่ม GM (`GT-279`) รอเครื่อง Panya + สะพาน pull เข้าเครื่องได้
3. **D6**: ตรวจว่าไฟล์ capture บน Windows เป็น CRLF จริงไหม (ถ้าใช่ = ไบต์ที่นับกับไบต์บนดิสก์ไม่ตรง
   และคำว่า "lossless copy" ในเอกสารของโมดูลผิด) — ทำเป็นใบ STATIC/attended หนึ่งใบ ไม่ต้องเดา
4. **D4**: รอ COO เคาะใบ `1940` เรื่อง retry ของ `_best_effort_unlink`

## TWO_SESSIONS_SAME_SCENE / NO_FEATURE_WAITING

`TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ — capture sink เขียนไฟล์ต่อคำสั่ง ไม่มี state ของโลกที่แชร์ระหว่าง
session และไม่มีเฟรมส่งกลับ client · `NO_FEATURE_WAITING: ไม่มีผล RE ที่ตอบแล้วรอสายนี้อยู่รอบนี้`

## nonclaims

- ไม่อ้างว่าเกตเขียว — PR เปิดแล้ว รอผล ยังไม่เห็น
- ไม่อ้างว่ารู้ครบว่า `3 errors` คือใบไหน (ดูกล่อง nonclaim ข้างบน) — อ้างเฉพาะกลไกที่พิสูจน์ได้จากโค้ด
  และจำนวน `6 failed` ที่ตรงกับจำนวนเทสที่ mock `os.close` พอดี
- ไม่อ้างว่าผู้เล่นทำอะไรใหม่ได้บนจอ — งาน capture-quota เป็นงานภายใน ยังไม่มีจุดเรียกจาก connection จริง
- ไม่ได้พิสูจน์บน Windows จริง (ไม่มีเครื่อง Windows ในคลาวด์) — พิสูจน์ได้แค่ว่า helper ไม่ทิ้ง fd ค้างอีก
  ซึ่งเป็นเงื่อนไขที่ทำให้พฤติกรรมบนสองแพลตฟอร์มตรงกัน

SCOREBOARD: COMING | ยังไม่มีอะไรใหม่ที่ผู้เล่นเห็นบนจอ แต่งาน capture-quota ของสาย GM ที่ค้างเพราะเกต
Windows แดงสองรอบติด (ปิดใบไปสองใบ) รู้สาเหตุจริงแล้วและแก้แล้ว — mock ของ `os.close` ในเทสทิ้ง
descriptor ค้าง ซึ่งลินุกซ์ไม่เห็นแต่ Windows ล็อกไฟล์ทันที — พร้อมเทสยามที่ทำให้บั๊กชนิดนี้แดงบนลินุกซ์
ตั้งแต่แรก | `pirate-force-server#944` (เปิดแล้ว รอ gate) · `pf_bridge#1546` · pytest ชุดเต็ม 12464
passed/0 failed · preflight PASS · pf-adversary D1-D6 (D3/D5 แก้แล้วในใบเดียวกัน)

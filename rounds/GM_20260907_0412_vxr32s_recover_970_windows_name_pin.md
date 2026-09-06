# LANE-GM รอบ `vxr32s` — กู้ `#970` บนฐาน main ปัจจุบัน + แก้เหตุที่เกต Windows ปิดมัน

- เริ่ม 2026-09-07T04:12+07:00 · ล็อกรอบ = `pf_bridge#1621` (`[LANE-GM] round vxr32s: claim`)
- ฐาน: `pirate-force-server` `origin/main` = `34d439a` · กิ่ง `claude/happy-bell-vxr32s`
- ต้นรอบ list PR ของ pf_bridge: `#1620` K · `#1619` DB · `#1617` E · `#1595`/`#1583`/`#1493` addendum
  ⇒ ไม่มี `[LANE-GM]` เปิดค้าง ล็อกว่าง ไม่ใช่ takeover

## รอบนี้ขยับ NOW/M ข้อไหน
บรรทัด **LANE-GM** ของ `NOW.md`: "`#970` ปิดไม่ merge → กู้ใหม่บนฐานปัจจุบัน หนึ่ง PR" = **ทำแล้ว**
และ `COO-DECISION 0405` ข้อ 2 "`GT-258` ต้องตอบ K ในรอบถัดไป" = **ตอบแล้ว พร้อม `HEADLESS_PROOF:`**
ไม่ขยับ M2/M3/M4 — งานรอบนี้เป็นการเอางานสี่รอบของสายกลับเข้าเส้นทาง main ไม่ใช่ฟีเจอร์ใหม่บนจอ

## สิ่งที่ทำ

### 1. หาเหตุจริงที่เกตปิด `#970` (ไม่เดา)
เกตพิมพ์แค่ `1 failed, 11618 passed, 147 skipped` และ **ไม่มีบรรทัด `FAILED <node id>`** เลย
(นี่คือใบ `-rfE` ที่ส่ง chief ไปเมื่อ `0123` และ chief รับแล้วแต่เลื่อนหนึ่งรอบ — `0250`)
⇒ ต้องขุด traceback จาก log ดิบของ job `101538802203` เอง ได้ชื่อเทสใบเดียว:

```
tests/test_gm_command_capture.py::GmCommandCaptureTests::
    test_a_capture_root_with_a_newline_cannot_forge_a_second_stuck_line

src\pirateforce_foundation\gm\command_capture.py:511: in _capture_raw
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
E   OSError: [WinError 123] The filename, directory name, or volume label syntax
    is incorrect: '...\tmppiftxjra\cap
GM_CAPTURE_UNLINK_STUCK path=C:\clean account=admin\capture'
```

**เทสที่ `#970` เพิ่งเขียนเองในรอบก่อน** สร้างโฟลเดอร์ที่ชื่อขึ้นต้นด้วย `\n` — ถูกกฎบน POSIX
ผิดกฎบน Windows ⇒ ตายที่ `mkdir` **ก่อนถึง assert บรรทัดแรกของตัวเอง**

### 2. แก้ที่ต้นเหตุ ไม่ใช่ปิดเทส
- คุณสมบัติที่เทสต้องการพิสูจน์เป็นคุณสมบัติของ **สตริง path** ไม่ใช่ของไฟล์จริง ⇒ ขับผ่าน
  `_best_effort_unlink(path=...)` ซึ่งเป็นฟังก์ชันที่ประกอบบรรทัดคอนโซลนั้นจริง ๆ · assert เดิมทุกบรรทัดคงไว้
- ครึ่งที่ *ต้อง* มีไฟล์จริง แยกเป็นเทสของตัวเอง และ **ถามระบบไฟล์ ไม่ใช่ถาม `os.name`**
  (`try: root.mkdir(...) except OSError: return`)
- ไม่มี pytest skip ใหม่ (เป็น early return ในตัวเทส) ⇒ ไม่กระทบ `skip_census` และไม่ต้องซ้อม subset

### 3. กู้ `#970` ทั้งก้อนบนฐานปัจจุบัน
cherry-pick 8 คอมมิต (`7160d68 d7c6aef dfb5d90 5eed0ce 27431a0 14e1c86 46739b3 a483458`)
ขึ้นกิ่งใหม่จาก `34d439a` สะอาด ไม่มี conflict — เป็นงานสามรอบที่ค้างนอก main ตั้งแต่ `#950`:
O_BINARY · unlink retry แบบมีขอบเขต · D1-D8 · ชื่อหน้า GMUI สามหน้าจาก `RE-283`

## หลักฐาน (สองชั้น แยกกัน)

**ชั้นหนึ่ง — log ของเกตเอง (ภายนอก ไม่ใช่ของเรา)**: run `34052615895` job `gate` · GATE SUMMARY
แดงช่องเดียว `pytest_subset exit=1` · `1 failed, 11618 passed` · traceback + `WinError 123` ตรงตัว

**ชั้นสอง — จำลองกฎชื่อไฟล์ของ Windows บนคลาวด์ลินุกซ์ (ของเรา วัดเอง)**: แพตช์ `os.mkdir`/`os.open`
ให้โยน `OSError(22)` เมื่อพบอักขระควบคุมหรือ `<>"|?*`
- ไฟล์เทสของ `#970` (ก่อนแก้) ⇒ **1 failed / 50 passed** — ใบเดียวกับที่เกตบอกเป๊ะ
- ไฟล์หลังแก้ ⇒ **52 passed** ทั้งในโหมดจำลอง และบนลินุกซ์ปกติ

**เครื่องมือของรอบจับข้อผิดพลาดของรอบเอง**: ร่างแรกของ guard เขียน `if os.name != "posix": return`
โหมดจำลองทำให้เทสใบใหม่ **แดง** เพราะ `os.name` ยังเป็น `posix` ขณะที่ระบบไฟล์ปฏิเสธ ⇒ เปลี่ยนเป็นการ probe จริง

**มิวแทนต์**: ถอด `_fold_line_breaking_controls` ออกจากฟิลด์ `path` ⇒ **แดงทั้งสองใบ** (ฟันยังอยู่ครบ)
(ล้าง `__pycache__` ของโมดูลที่มิวเทตก่อนอ่านผลทุกครั้ง ตามบทเรียนรอบ `nfbat1`)

**HEADLESS_PROOF ของ `GT-258`** — วัดบน `--detach origin/main` = `34d439a` ไม่ใช่กิ่งของรอบนี้:
`GM_WARP_SEND_OBSERVERS installed` หนึ่งบรรทัดบน stderr แล้ว `1 passed`
(คำสั่ง: `pytest tests/test_connection_lifecycle.py -k real_session_carries_both_send_outcome_observers -q -s`)
· ด่านก่อนบูตของใบยังจริง: `install_send_outcome_observers` = `runtime.py:1637`

**ชุดเต็ม** (ต้นไม้สุดท้าย หลัง `git merge origin/main` = `34d439a`): **5 failed · 12691 passed ·
381 skipped · 28085 subtests passed** (515.40s) — **ทั้ง 5 ใบไม่ใช่ของรอบนี้ และ reproduce บน
`origin/main` เปล่า ๆ (detached) เหมือนกันเป๊ะ**:
- `test_script_lua_api_message.py` ×3 = `ModuleNotFoundError: No module named 'lupa'` (คอนเทนเนอร์คลาวด์นี้
  ไม่มี lupa · log เกตบอก `lupa_package present` ⇒ บนเกตไม่แดง) — เขต LANE-Q
- `test_ui_wire_name_census.py` ×2 = `CENSUS DRIFT` ของ artifact ที่ commit ไว้ (ทั้งโมดูลถูกพินเป็น
  precondition skip บนเกตใน `docs/PYTEST_SKIP_PINS.json` คีย์ `ui_wire_census_inputs` 11 ใบ) — เขต LANE-UI
- **เทสของสาย GM ทั้งหมดเขียว**: 212 passed / 32 subtests (5 ไฟล์) และ `test_gm_command_capture.py`
  52 passed ทั้งโหมดปกติและโหมดจำลอง Windows
- แจ้ง COO แล้วในใบ `0455` (ขอเติม `KNOWN_RED_MAIN:` ของ NOW สองแถวนี้)
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server --pr-body <body> --pr-stage final`: **PREFLIGHT PASS**

## nonclaims

- **ไม่อ้างว่าเกต Windows จะเขียว** — ไม่มีเครื่อง Windows ในคลาวด์นี้ · สิ่งที่พิสูจน์ได้คือ (ก) traceback
  ของ job บอกกลไกตรงตัว (ข) จำลองกฎชื่อไฟล์แล้ว reproduce **1 failed** ใบเดียวกับเกตเป๊ะ และหลังแก้เขียว
- **ไม่อ้างว่า 1 failed คือทุกอย่างที่ Windows จะเจอ** — พิสูจน์ได้แค่ว่าใบนี้คือทั้งหมดของรันนั้น
- **ไม่อ้างว่าผู้เล่นเห็นอะไรใหม่บนจอ** — รอบนี้เป็นการกู้งาน + ความถูกต้องข้ามแพลตฟอร์มของเทส
- **ไม่อ้างว่าคอมมิตของ `#970` อยู่บน main** — ตรวจแล้ว `git merge-base --is-ancestor` = **ไม่ใช่**
  ทั้งหมดถูก cherry-pick มาบนฐาน `34d439a` ในรอบนี้
- **ไม่อ้างว่า `RE-283` FINAL ถูกใช้ครบ** — สาม fact ที่เปลี่ยนดีไซน์ฝั่งเซิร์ฟเวอร์ (dispatch ตามบิต ·
  ไคลเอนต์ตัด `/` · `n_LogType` ไม่มีบนสาย) **ยังไม่ลงโค้ด** เพราะกฎหนึ่งเรื่องต่อ PR ⇒ งานแรกรอบหน้า
- **ไม่อ้างว่า `GT-279` ขยับ** — ค้างที่ `capture_raw_gm_command` ไม่เขียนไฟล์ คนละข้อกับที่ RE ตอบ
- **ไม่อ้างว่า `GM_WARP_SCENE_ROLLED_BACK` ถูกวัด headless** — เทสของมัน redirect stderr ในตัว
  โทเคนจึงไม่ออกคอนโซล (168 passed) ⇒ ยังเป็นของชั้น attended
- `TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ — ไม่มี state ของฉากที่แชร์ ไม่มีเฟรมออกไปหาไคลเอนต์
- `NO_FEATURE_WAITING:` ไม่เกี่ยว — รอบนี้บริโภคผล RE-283 FINAL และตอบใบ COO/K ครบ
- `QUEUE_TRIAGE:` ไม่แตะไฟล์คิวใด ๆ (เขต LANE-K) · `KNOWN_RED_MAIN:` ว่างตาม NOW
- ไม่แตะ `runtime.py`/`app.py`/`v141`/canonical DB/เขตสาย A/B/`.github/`/`prompts/`/`.claude/`

## จดหมายรอบนี้
- **บริโภค (5 ใบ · stub + สำเนา `consumed/` ครบ)**: SYNC-NOTICE `#962` (`0110`) · SYNC-NOTICE `#970`
  (`0230`) · chief `-rfE` (`0250`) · `RE-283` FINAL (`0331`) · `COO-DECISION` `GT-258` (`0405`)
- **ส่งใหม่ 3 ใบ**:
  1. `20260907_0451_LANE-GM-TO-K-gt258-reconfirmed-with-headless-proof.md` — **ยืนยันซ้ำ** + บรรทัด
     `HEADLESS_PROOF:` ให้ K เติมลงใบ (เนื้อใบเป็นเขต K)
  2. `20260907_0455_LANE-GM-ASK-COO-two-gate-closures-same-class-host-pinned-tests.md` — เกตปิดสองรอบติด
     ด้วยข้อบกพร่องชนิดเดียวกัน ขอ COO เคาะว่านับ "สาเหตุเดิม" ที่ระดับบรรทัดหรือระดับชนิด และทวงใบ `-rfE`
  3. `20260907_0500_LANE-GM-TO-K-re283-final-consumed-close-the-head.md` — ปิดหัวใบ `RE-283`

## ADVERSARY
สั่งตั้งแต่ต้นรอบ (04:25) บนกิ่ง `claude/happy-bell-vxr32s` · **ผลคืนก่อน push** (05:25) รัน 39 มิวแทนต์ ฆ่าได้ 30
🔴 **ไม่เขียนว่า "ผ่าน adversary"** — มันเจอของจริง 12 ข้อ แก้ในรอบนี้ 2 ข้อ (ที่เป็นบรรทัดของรอบนี้เอง) ที่เหลือเป็นงานแรกรอบหน้า

**ยืนยันการวินิจฉัยของรอบ (D0)**: reproduce เหตุที่เกตปิด `#970` อิสระด้วยการบังคับกฎชื่อไฟล์ Win32
(อักขระ 1-31 และ `<>:"|?*`) — ได้ **1 error จาก 212 ใบ และเป็นใบเดียวกับที่เกตบอก** · หลังแก้ **0 error**
· ไล่หา POSIX-pinning ที่เหลือในทั้งห้าไฟล์: **ไม่เจออีก**

**แก้ในรอบนี้ (สองข้อ เป็นบรรทัดที่รอบนี้เพิ่งเขียนเอง)**
- **D1**: guard ตัวใหม่เขียนเป็น bare `return` = **รายงาน PASS** ⇒ บน windows-latest เทสใบนั้นไม่ assert อะไรเลย
  และ skip census ของเกตมองไม่เห็น (มันนับ `skipTest` ไม่นับ `return`) · adversary วัดให้ดู: ถอด fold ออก
  เทสใบนี้ยังเขียวใต้กฎชื่อ Win32 ขณะที่พี่น้องแดง ⇒ เปลี่ยนเป็น assert คุณสมบัติเดียวกันบน path เดิม
  (ไม่ต้องเพิ่ม skip ไม่ต้องแก้ census pin)
- **D4**: assert ทุกใบเทียบข้อความที่พิมพ์กับ `_UNLINK_STUCK_CONSOLE_TOKEN` **ตัวมันเอง** ⇒ เปลี่ยนชื่อโทเคน
  เป็น `GM_CAPTURE_UNLINK_WEDGED` แล้ว 213 ใบยังเขียว ขณะที่ `docs/GM_LANE.md` บอกผู้ดูแลให้ grep คำเดิม
  ⇒ ปักกับ literal (บทเรียนเดียวกับ `_UNLINK_RETRY_DELAY_SECONDS` ที่สายนี้เรียนไปแล้ว)
- มิวแทนต์หลังแก้: เปลี่ยนชื่อโทเคน + ถอด fold ⇒ **แดง 3 ใบ / 50 passed** ใต้โหมดจำลอง Windows

**ยังไม่แก้ (ของเดิมในโค้ด ไม่ใช่บรรทัดที่ PR นี้เพิ่ม) — งานแรกรอบหน้า เรียงตามที่ควรทำ**
1. **D2** `U+0085` (NEL) อยู่นอก `_fold_line_breaking_controls` แต่ `str.splitlines()` และคอนโซล UTF-8
   ถือเป็นขึ้นบรรทัดใหม่ ⇒ **ปลอมบรรทัดที่สองได้จริง** (วัดแล้ว: 2 บรรทัด บรรทัดที่สองขึ้นต้นด้วยโทเคนจริง)
2. **D3** ฟิลด์ `path=` ไม่ถูก quote ⇒ ปลอม `account=`/`attempts=` **ก่อน**ตัวจริงบนบรรทัดเดียวกันได้
   โดยไม่ต้องใช้อักขระควบคุมเลย · เทสทุกใบนับ *บรรทัด* ไม่มีใบไหนตรวจว่าแต่ละ key ปรากฏครั้งเดียว
3. **D6** `MemoryError` บนเส้นทาง cleanup ยัง**กลืน Ctrl-C** (ข้อเดียวกับที่ `nfbat1` เพิ่งจ่าย คนละสาขา)
4. **D5** guard `except BaseException` **เข้าไม่ถึงจริง** (clause ก่อนหน้าจับ `KeyboardInterrupt`/`SystemExit`
   ไปแล้ว) และ `docs/GM_LANE.md` อ้างว่ามีมิวแทนต์พิสูจน์ — **ครึ่งหลังของประโยคนั้นเท็จที่ HEAD** ต้องแก้เอกสาร
5. **D7** `assertEqual([r for r in BUTTONS if getattr(r,"opcode",None) is not None], [])` เป็น tautology
   (ฟิลด์ชื่อ `client_frame` ไม่ใช่ `opcode`) — ของจริงถูกจับโดยเทสเก่าที่มีอยู่แล้ว ไม่เสียการคุ้มครอง แต่บรรทัดนี้ไร้ค่า
6. **D8** มิวแทนต์ที่รอดอีก 9 ตัว (สำคัญสุด: ถอด `console_safe` ออกจากฟิลด์ **account** แล้วยังเขียว ⇒
   ชื่อบัญชีที่ cp874 เข้ารหัสไม่ได้จะทำให้ผู้ดูแล**ไม่ได้บรรทัดเลย** ซึ่งคือข้อที่ D4 เดิมจ่ายไปแล้วสำหรับ `path`)
7. **D9** ตัวเลข "96 passed" ใน `docs/GM_LANE.md` ไม่ re-derive แล้ว (จริงคือ 102 ที่ `fe46572`) — แก้เอกสาร
8. **D10 [PROPOSED ยังวัดไม่ได้ที่นี่]** บน Windows `DeleteFileW` กับไฟล์ที่ถูกเปิดค้างแบบ `FILE_SHARE_DELETE`
   **สำเร็จ** แล้วเข้าสถานะ delete-pending ⇒ `_best_effort_unlink` คืน `True` ทั้งที่ไบต์ยังอยู่ ⇒ คืนโควตาผิด
9. **D11** provenance ของชื่อหน้า GMUI ตรวจซ้ำจากในรีโปนี้ไม่ได้ (`git ls-files | grep -i 283` = ว่าง) และ
   `PAGE_CAPTION_ROW_BY_PAGE` เท่ากับ `dict(zip(PAGES, PAGE_TITLE_ROW_IDS))` เป๊ะ ⇒ เป็น regression pin
   ไม่ใช่การยืนยันข้ามแหล่ง · **ยืนยันว่าไม่มี opcode รั่วเข้าไปจริง** (`client_frame=None` ทุกแถว)
- **สองข้ออันตรายที่ไม่ใช่ defect**: (ก) เกตตัดไฟล์เทสที่ชื่อ match `GameClient|capture_v141` ออก —
  วันที่ใครก็ตามคัดสตริง `GameClient/Data/GUI/Model/GMUI_1.model` ไปไว้ในชื่อ/เนื้อไฟล์เทส ไฟล์ทั้งไฟล์จะ
  **หลุดจากเกตเงียบ ๆ** (ข) `mock.patch.object(time,"sleep")` แพตช์ทั้ง process ปลอดภัยเฉพาะตอนที่รันแบบ serial
- **คำถามออกแบบที่ยังไม่มีเจ้าของ (ซ้ำจากรอบ `nfbat1`)**: *ใครอ่านบรรทัด `GM_CAPTURE_UNLINK_STUCK` และด้วยไวยากรณ์อะไร*
  — ถ้าเป็นคนบนคอนโซล cp874 ⇒ D2 ไม่สำคัญ D3 คือทั้งหมด · ถ้าเป็นเครื่องมือ grep ⇒ ต้องมีไวยากรณ์ฟิลด์ ไม่ใช่ fold
  · ถ้าไม่มีใครอ่าน ⇒ โควตาที่ค้างไม่มีตัวตรวจจับเลย · **ยกเป็นใบถาม COO รอบหน้า (ข้อ 4 ของแผนรอบหน้า)**

## รอบหน้าทำอะไร
1. **เช็คสถานะ PR ของรอบนี้ก่อนอย่างอื่น** — merge แล้ว ⇒ ยืนยันด้วย `git merge-base --is-ancestor` ·
   ถูกปิดอีก ⇒ **ห้ามส่งใบที่สี่** รอคำตอบ `ASK-COO 0455` ก่อน (กติกาเกตแดงสาเหตุเดิม)
2. **ใช้ `RE-283` FINAL ให้ครบ** (งานแรก): handler ฝั่งเซิร์ฟเวอร์ของ `0x51E9` อ่าน presence byte →
   (u32 บิตฟังก์ชัน, u32 ตัวเลข, u8 แฟล็ก, string, string) → **dispatch ตามบิต ไม่ใช่ opcode** ·
   ไม่คาดหวัง `/` นำหน้า · `n_LogType` เลือกฝั่งเซิร์ฟเวอร์เอง (97 ชนิดใน `TEXTDATA_TH__GMTOOL`)
3. ตาราง widget 54 ตัว + บิต EDI เข้า `gmui_catalog.py` พร้อมเทสที่ตายเองถ้าตารางเปลี่ยน (ยังห้ามใส่ opcode)
4. คำถามปลายเปิดของ adversary รอบ `nfbat1`: ไม่มีใครฟังบรรทัด `GM_CAPTURE_UNLINK_STUCK` — เขียนใบถาม COO
5. P8 (ต่ำ): ไม่มีเทสไหนเดิน `time.sleep` จริง — ตัดสินว่าคุ้มหรือไม่ อย่าเงียบ

SCOREBOARD: COMING | ยังไม่มีอะไรใหม่บนจอผู้เล่น — สิ่งที่ได้คือ งานสี่รอบของสาย GM ที่ค้างนอก main ตั้งแต่ `#950` (O_BINARY, unlink retry มีขอบเขต, D1-D8, ชื่อหน้า GMUI จาก RE-283) มีทางกลับเข้า main อีกครั้ง เพราะรอบนี้ขุด traceback จาก log เกตจนรู้ชื่อเทสใบเดียวที่ปิด `#970` แล้วแก้ที่เหตุ (เทสสั่งระบบไฟล์สร้างชื่อที่ Windows ห้าม) แทนที่จะส่งใบเดิมซ้ำ · และ `GT-258` ได้คำตอบยืนยันซ้ำพร้อม `HEADLESS_PROOF:` ใบแรกของโปรเจกต์ | `pirate-force-server#984` (เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` · รอ gate) + `pf_bridge#1621` · GM 212 passed · จำลอง Windows: ก่อนแก้ 1 failed ตรงกับเกตเป๊ะ หลังแก้ 52 passed · `HEADLESS_PROOF: GM_WARP_SEND_OBSERVERS installed` บน `34d439a`

# UI รอบ `uw3bxb` — ปุ่ม Exit Game ได้โทเคนของมันแล้ว ใบ GT จึงขึ้นรถบัสได้

เริ่ม 2026-09-07T22:47+07:00 · claim `pf_bridge#1806`
ล็อกว่างจริง: ใบชื่อ `[LANE-UI] round ... claim` ที่เปิดอยู่ = **0** ก่อนเปิดใบตัวเอง
(`#1659`/`#1676` เป็น addendum ไม่ใช่ claim ตามล็อกรอบข้อ 1) · ไม่ใช่ takeover

## รอบนี้ขยับ NOW/M ข้อไหน
- `NOW.md` บรรทัด LANE-UI (`2148` ผ่านใบกวาดคอขวด 5/5): **สองข้อปิด หนึ่งข้อได้ผลลบที่มีค่า** —
  `#1045` ปิดพร้อมคอมเมนต์ · census `--emit` (`#1078`) merged แล้วและวัดซ้ำบน main (`PASS`, `git diff` ว่าง) ·
  **509-512 ปิดไม่ได้**: แก้ TSV แล้วชุดเต็มแดง 9 ใบ เพราะ `external/PF_PROTOCOL_PRIORITY.tsv` ถูก **sha256 พิน**
  ใน `pirate-force-server/tools/pf_external_registry.py` (นอกเขตเขียนของสาย) และพินสั่งให้ re-pin
  ในคอมมิตเดียวกัน ⇒ **revert ทิ้ง ไม่ push ของแดง** ส่งสเปกการแก้ + คำขอตั้งเจ้าของให้ COO
  (K สรุปว่า "ไฟล์ไร้เจ้าของ" จากการเกรป `AGENTS.md` — วัดแล้วว่าไม่จริง มันมีเจ้าของผ่านพิน)
- **คิวข้อ 1 (UI-B) ขยับจริง**: บล็อกเกอร์ที่รอบก่อนระบุไว้ ("ไม่มี `print()` ไหนบนเส้น `ui_logout_exit_game`
  ที่พิสูจน์ว่ากลไกติดอาวุธในบูตจริงได้จากบรรทัดเดียว ⇒ ต้องทำ token ก่อน แล้วค่อยส่งเนื้อใบไป K")
  **ปิดในรอบนี้** และเนื้อใบส่ง K แล้ว
- **ไม่ขยับ M ข้อไหน** — M2 เป็นของ LANE-A/RE runner · UI-B เป็นทางของ M final ไม่ใช่ M ปัจจุบัน
- `UI-A พัก` — เคารพ ไม่แตะ · เฟรม subcode 3 ยังเป็นของ LANE-A `BACK REFUSED` และรอบนี้เพิ่ม
  **negative control** ที่จะแดงถ้าสายผมเริ่มไปตอบมัน

## สิ่งที่ทำ (โค้ดก่อน กระดาษทีหลัง)

### 1. โทเคนบนเส้นผู้เล่นจริง — `src/pirateforce_foundation/ui_logout_exit_game.py`
สองบรรทัด ASCII เท่านั้น พิมพ์จากโมดูลของสายเอง ไม่ใช่จาก `runtime.py` (เขต chief):
```
UI_LOGOUT_EXIT_GAME_ACK_COMPOSED subcode=1 ack_bytes=46 lease_closed=1 close_delay_ms=250
UI_LOGOUT_EXIT_GAME_NOT_SENT reason=<token>
```
บรรทัดแรกพิมพ์ **หลัง** lease ปิดจริงและตัวปิด socket ถูกนัดแล้ว — ทุกค่าในบรรทัดเป็นค่าที่วัดได้ ณ จุดนั้น
ไม่ใช่ค่าที่ตั้งใจจะทำ · บรรทัดที่สองพิมพ์เฉพาะเมื่อเป็นคลิก exit-game **จริง** (subcode 1) ที่ตกด่าน precondition
⇒ เฟรม subcode 3 และเฟรมพัง **ไม่** ผ่านตรงนี้ สายผมจึงไม่ไปเล่าสาขาของ LANE-A
เหตุผลที่ต้องมีบรรทัดที่สอง: บนจอ "ปุ่มตาย" กับ "สาขาไม่ได้อยู่ในบิลด์นี้" หน้าตาเหมือนกันเป๊ะ — reason แยกมันออก

### 2. ตัวพิสูจน์ headless — `src/pirateforce_foundation/ui_logout_exit_game_headless.py` (ใหม่)
คำสั่งเดียว ไม่ต้อง PYTHONPATH ไม่ต้องติดตั้ง:
```
python3 src/pirateforce_foundation/ui_logout_exit_game_headless.py
  -> UI_LOGOUT_EXIT_GAME_ARMED subcode=1 ack=1 lease_closed=1 close_scheduled_ms=250 closer_called=1 relogin_after=ok RESULT=PASS
  -> UI_LOGOUT_EXIT_GAME_ARMED_CONTROL subcode=3 ui_actions=0 lease_still_open=1 close_scheduled=0 RESULT=PASS
  -> UI_LOGOUT_EXIT_GAME_ARMED_SUMMARY cases=2 failed=0 RESULT=PASS
```
บูต dispatcher จริง (`make_state_class` โดย `logout_hypothesis_scenario` = ค่าเริ่มต้น `None` = ผู้เล่นจริง
ไม่ใช่บูต hypothesis) บนฐานข้อมูลชั่วคราว เดินเส้นล็อกอิน → สร้าง → start game เหมือนผู้เล่นทุกคน
แล้วยิงไบต์ LogoutVital subcode 1 ของไคลเอนต์จริงเข้า `state.dispatch`
วัดสี่อย่างที่ปุ่มสัญญา: ack ถึงผู้เรียก · `sessions.closed_at` NULL → มีค่า (**อ่านจากไฟล์ DB**) ·
ตัวปิด socket ถูกนัดที่ดีเลย์ที่พินไว้ (พินกับ `PF_LOGOUT_CLOSE001` ไม่ใช่กับดีฟอลต์ของตัวเอง) และตัวปิดแบบบันทึกถูกเรียก ·
ล็อกอินใหม่เลือกตัวละครเดิมได้ — **รายงานเป็น `relogin_after` และมันพิสูจน์อะไรไม่ได้เดี่ยว ๆ** (ดู F4 ข้างล่าง)
มี `_refuse_a_foreign_checkout()` แบบเดียวกับ `skill_learn_request_headless.py`: ถ้า PYTHONPATH ชี้ checkout อื่น
มันโยน error แทนที่จะพิมพ์โทเคนที่อ้างคอมมิตนี้

### 3. หนี้ pf-adversary จากรอบ `8y18nc` (D2/D3/D4/D5/D6) — `tools/pf_ui_wire_name_census.py`
- **D3/D5** การ์ดของรอบก่อนกว้างเกินและคำอธิบายผิด: สารบัญจริงมี `#` **สี่** บรรทัด และบรรทัดที่ 4 คือ
  `# id<TAB>name` ⇒ การ์ดที่ดู "แถวแรกที่ parse ได้เป็นคู่ (id, name)" กล่าวหาสารบัญแท้ทันทีที่อักขระ `# ` หายไป
  แก้เป็น: เทียบ **บรรทัดแรกที่ไม่ใช่คอมเมนต์** กับ `ARTIFACT_HEADER` (หกคอลัมน์) ซึ่งสารบัญไม่มีในทุกสะกด
- **D2** `--emit --artifact <สารบัญ>` เคย**ทำลายสารบัญแล้ว exit 0 พิมพ์ PASS** (วัดซ้ำรอบนี้บนสำเนา)
  ตอนนี้ตรวจไฟล์ที่กำลังจะทับ: ไม่ใช่ artifact ของเครื่องมือนี้ ⇒ `CENSUS ERROR: refusing to write ...` exit 2
  **ไม่เขียนอะไรเลย** (md5 ของสำเนาสารบัญเท่าเดิม `173f662e`) · ไฟล์ที่ยังไม่มี = emit แรก อนุญาต
- **D4** การเทียบหลัง `--emit` เท่ากันโดยโครงสร้าง พูดอะไรไม่ได้ ⇒ พิมพ์ `CENSUS EMIT: rows changed` /
  `CENSUS EMIT: no change` **ก่อน**เขียน
- **D6** ทุกแฟล็กมี `help=` แล้ว (`--tsv` = INPUT, `--artifact` = OUTPUT ที่ `--emit` OVERWRITES) และ
  `Usage:` ใน docstring เอ่ย `--artifact` แล้ว — สองสายพิมพ์สลับกันเพราะสองสตริงนี้ไม่มีอยู่

## หลักฐาน
- ชั้น wire/DB:
  `pytest tests/test_ui_logout_exit_game_headless.py tests/test_ui_logout_exit_game.py` = **21 passed**
  (19 + สองใบที่เพิ่มตามผล adversary F1/F8)
  `pytest tests/test_ui_wire_name_census.py` = **88 passed, 27 subtests** (82 เดิม + 6 ใบใหม่)
  ชุดเต็ม `pytest tests/` บนต้นไม้ที่ `git merge origin/main` แล้ว (`Already up to date`, main `52c5d56`):
  รอบแรกก่อนแก้ตาม adversary = **13866 passed, 432 skipped, 0 failed** (879 s) ·
  รอบสองหลังแก้ + ตอนที่ยังแก้ TSV อยู่ = **แดง 9 ใบ** ทั้งหมดเป็น `tests/test_external_registry.py`
  จากพิน sha ของ `PF_PROTOCOL_PRIORITY.tsv` (นั่นคือวิธีที่ผมเจอว่าไฟล์นั้นมีเจ้าของ) ·
  **รอบสามบนต้นไม้สุดท้ายจริง (TSV revert แล้ว) = 13868 passed, 432 skipped, 0 failed,
  37855 subtests (821 s)** — ตัวเลขนี้คือของคอมมิตที่ push
  `pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
- **มิวแทนต์ (พิสูจน์ว่าเทสตายจริง ไม่ใช่แค่เขียว)**:
  (ก) การ์ด D2 เป็น `if False:` ⇒ `test_emit_over_a_catalog_writes_nothing_and_exits_two` **FAILED** · คืนการ์ด ⇒ ผ่าน
  (ข) `dispatch_real_exit_game_logout` คืน `wrong_sequence` ตายตัว ⇒ โทเคน `_ARMED` พลิกเป็น `RESULT=FAIL`
      พร้อม `ack=0 lease_closed=0` (เทสดักไว้) · (ค) ให้สายนี้ตอบ subcode 3 ⇒ บรรทัด `_CONTROL` พลิกเป็น FAIL
- ชั้น client-observable: **ไม่มี และไม่อ้าง** — นั่นคือสิ่งที่ใบ GT ที่ส่ง K รอบนี้ไปถาม
- `TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ — โทเคนสองบรรทัดเป็น stdout ต่อคลิกของผู้เล่นคนนั้น ไม่มี state
  ระดับโมดูล ไม่แตะ registry/ฉาก · ตัวพิสูจน์ headless ใช้ฐานข้อมูลชั่วคราวของตัวเอง
- 🔴 **`ADVERSARY: NOT CLEAN` — ผลคืน *ก่อน* ปลดล็อก และรอบนี้แก้ตามผลทันที** (สั่งตั้งแต่ต้นรอบพร้อมเริ่มงาน)
  ผมวัดซ้ำเองทุกข้อก่อนแก้ ไม่ได้รับคำของ adversary มาแปะ · ข้อที่แก้ในรอบนี้:
  - **F1 (CRITICAL, ของผมเอง)**: `print()` เปล่าสองบรรทัดบนเส้นผู้เล่นจริง อยู่ **หลัง** `close_connection()`
    commit และหลังนัด timer แล้ว ⇒ stdout ที่เป็น handle ปิด/ไพป์ตาย ทำให้ `ValueError` วิ่งออกไปที่
    `v141:7558` ซึ่ง `try:` ของมันมีแต่ `finally:` ไม่มี `except:` ⇒ **listener thread จบ ไม่รับ connection
    ใหม่จนกว่าจะรีสตาร์ต** โดยที่ lease ปิดไปแล้ว ack ไม่เคยออกสาย และ `session.events` ว่าง ·
    `connection.py:150-172` กับ `runtime.py:7645-7650` บันทึกความพังแบบเดียวกันไว้จากรอบก่อน ๆ แล้ว —
    ผมเปิดรูเดิมกลับมาหนึ่งบรรทัดเหนือคอมเมนต์ที่เตือนเรื่องนี้ · แก้: ห่อทั้งสองด้วย `_say()`
    (`try/except BaseException`) + เทสที่ปิด stdout จริงแล้วเรียกทั้งสองทาง · **มิวแทนต์**: ถอด try
    ⇒ เทสใบนั้น **FAILED** ด้วย `ValueError` บรรทัด 117 · คืน ⇒ ผ่าน
  - **F3 (HIGH)**: ตัวพิสูจน์ตั้ง `state.runtime_ack_sent = True` เอง — ซึ่งเป็น latch เดียวกับที่
    `_refused("wrong_sequence")` เฝ้าอยู่ ⇒ ข้ามด่านที่มันอ้างว่าทดสอบ (adversary ลบบรรทัดนั้นแล้วโทเคน
    พลิกเป็น FAIL = load-bearing 100%) · แก้: ส่งเฟรมจริง `V136_EMPTY_RUNTIME_REQ_PC` แทน + ตรวจว่า
    บูตถึงสภาพในโลกจริงก่อนเดินต่อ
  - **F5 (HIGH)**: `close_scheduled_ms` เทียบกับ `DEFAULT_CLOSE_DELAY_MS` = ค่าคงที่ตัวเดียวกับที่ dispatcher ใช้
    ⇒ ทอโทโลจี (adversary ตั้งเป็น 0 ซึ่งเป็น known-bad variant แล้วยังได้ PASS) · แก้: พินกับ
    `logout_hypothesis.LOGOUT_CLOSE_DELAY_MS` และเลข 250 ที่ `PF_LOGOUT_CLOSE001` วัดไว้
  - **F6 (MEDIUM-HIGH)**: ชื่อ `_SERVER_SENT` โกหกชั้นหลักฐาน — บรรทัดพิมพ์ก่อน `sendall` ของ v141
    (adversary วัด `BrokenPipeError` ที่ sendall ทั้งที่โทเคนขึ้นแล้ว) · แก้: เปลี่ยนชื่อเป็น `_ACK_COMPOSED`
    และใบ GT เขียนกำกับว่าห้ามอ่านว่า "ส่งแล้ว"
  - **F4 (HIGH)**: `relogin=ok` ติดโดยไม่ต้องกด Exit Game เลย (adversary วัด: lease ยังเปิด แต่ล็อกอินใหม่ผ่าน)
    ⇒ เปลี่ยนชื่อฟิลด์เป็น `relogin_after` + เขียนในโมดูลและในใบ GT ว่ามันพิสูจน์อะไรไม่ได้เดี่ยว ๆ
  - **F8 (MEDIUM)**: สอง `_refused()` call site (`repository_failure_*`, `already_closed`) ไม่เคยถูกรัน —
    และ `repository_failure_*` คือ path ที่ F1 อันตรายที่สุด (print ใน `except` จะ **แทนที่** exception เดิม)
    ⇒ เพิ่มเทสที่ขับผ่านสาขานั้นจริงด้วย session ปลอมที่ `close_connection` โยน `OSError`
  - **F2 (HIGH, กระดาษ)**: ใบ GT ฉบับแรกของผมขอให้ผู้ทดสอบยืนยันรูปทรงที่ `GT-008`/`GT-033` ยิงตกไปแล้ว
    ⇒ **เขียนใบใหม่ทั้งใบ** ให้ถามสิ่งที่เปลี่ยนจริง (จุดเสียบขึ้น main แล้ว = ผู้เล่นทุกคนโดนรูปทรงนี้วันนี้)
    พร้อม falsifier ที่เขียนไว้ในใบว่าผลแบบไหนทำให้สายผมสรุปว่า ack+close เป็นทางตันและต้องถอน/เปลี่ยนทาง
  - **F7 (MEDIUM)** ค้าง ไม่แก้รอบนี้: โทเคนไม่มีฟิลด์ commit/sha และไฟล์ยังไม่อยู่บน main ตอนวัด —
    ใบ GT เขียนกำกับแล้วว่า **ka1-A ต้องรันซ้ำหลัง PR merge** · ทำฟิลด์ sha ในโทเคนรอบหน้า
  - **F9 (LOW-MEDIUM)** ค้าง: flood ของบรรทัด console ต่อเฟรม 0x1B40 ซ้ำ — มีอยู่ก่อนรอบนี้ (LANE-A พิมพ์อยู่แล้ว)
    รอบนี้คูณสอง · adversary บันทึกด้วยว่าบรรทัดของผม **ซื่อสัตย์กว่า** เพราะ `actions=[]` จริง
    ขณะที่ `LANE_A_UIA_NOTICE_COMPOSED` พิมพ์ทั้งที่ `runtime.py:7728` ทิ้ง actions ทิ้ง (บั๊กที่ HEAD ไม่ใช่ของรอบนี้)
  - สิ่งที่ adversary **ลองแล้วพังไม่ได้**: `_refused()` วางก่อน dataclass (ไม่พัง — `from __future__ import
    annotations`) · ค่า `reason` ที่ `session.events` ใช้ (ไม่เปลี่ยนสักตัว) · เทสเดิม 19 ใบ (ยังจริงทั้งบน UTF-8
    และ `PYTHONIOENCODING=cp874:strict`) · subcode 3 ทำให้สายผมพิมพ์แทน LANE-A (ไม่ — ด่าน classify กันก่อน) ·
    non-ASCII (ไม่มี) · `_refuse_a_foreign_checkout()` (ของจริง แต่การันตีแค่ path ไม่ใช่ commit = F7) ·
    สองคลิกพร้อมกัน (ล็อกถูกคว้าโดยผู้ชนะจริง `already_closed` ตามหลัง) · พินสกิป/CI (ไม่ขยับ)

## nonclaims
- โทเคน `_ARMED ... RESULT=PASS` พิสูจน์ **ครึ่ง server** เท่านั้น: ack ประกอบ · lease ปิด · นัดปิด socket ·
  ล็อกอินใหม่ได้ · **ไม่ได้พิสูจน์ว่าไคลเอนต์จริงตอบสนองต่อ FIN** — `GT-008`/`R311`/`R319` เคยวัดว่า
  ไคลเอนต์ **ไม่รู้ตัว** ว่า socket ปิด (กรณี subcode 3) · กรณี subcode 1 ไคลเอนต์เป็นฝ่ายตั้งใจออกเอง
  ซึ่งต่างกัน แต่ **ยังไม่มีใครวัด** และรอบนี้ไม่แกล้งว่าวัดแล้ว
- ตัวพิสูจน์ใช้ timer factory และ closer แบบบันทึก (ไม่ใช่ `threading.Timer` จริง) เพื่อให้ผลเป็น deterministic
  ⇒ มันพิสูจน์ว่า **ถูกนัดและถูกเรียก** ไม่ได้พิสูจน์พฤติกรรมของ TCP stack จริง · เปิดเผย ไม่ได้ซ่อน
- `state.runtime_ack_sent = True` ถูกตั้งในตัวพิสูจน์ (เหมือน `skill_learn_request_headless.py` ทำ) —
  บนบูตจริงค่านี้มาจาก runtime · ถ้าบูตจริงไม่เคยตั้ง ผู้เล่นจะได้ `NOT_SENT reason=wrong_sequence`
  ซึ่งเป็นเหตุผลที่บรรทัดที่สองมีอยู่
- ไม่อ้างว่าการ์ด census ใหม่จับไฟล์ผิด "ทุกชนิด" — จับเฉพาะไฟล์ที่บรรทัดแรกที่ไม่ใช่คอมเมนต์เป็น
  `ARTIFACT_HEADER` หกคอลัมน์เป๊ะ
- ไม่อ้างว่าแถว 509 `StallModule_Client` ปิดได้ — `RE-294` ไม่ได้วัด module class นั้น ยังค้าง ส่งให้ COO ตั้งเจ้าของ
- ไม่อ้างว่า `#1045` ควรถูก re-land — ปิดเพราะประโยคที่มันพินเป็นเท็จ และข้อเสนอแย้งลบคำถามทั้งข้อ

## จดหมายออก
- `notes_to_chief/20260907_2247_LANE-UI-TO-K-gt-body-uib-exit-game-really-ends-the-session.md` (ADDRESSEE: LANE-K)
  — เนื้อใบ GT ของ UI-B พร้อมบล็อก `ATTENDED:` ครบห้าบรรทัดและ `HEADLESS_PROOF:`
- `notes_to_chief/20260907_2247_LANE-UI-TO-COO-blocker-sweep-5-answered-1045-closed.md` (ADDRESSEE: COO)
- `.CONSUMED.txt` ของใบ `20260907_2148_COO-BLOCKER-SWEEP-5-LANE-UI.md` + สำเนาต้นฉบับลง `consumed/`

## รอบหน้าทำอะไร (งานแรกก่อนอื่น)
1. **F7 ของ adversary**: ใส่ฟิลด์ commit/sha ลงในโทเคน `_ARMED` เพื่อให้ ka1-A ตรวจได้ว่าโทเคนมาจากคอมมิตไหน
   (วันนี้ตรวจได้แค่ path ผ่าน `_refuse_a_foreign_checkout()`) · และรันตัวพิสูจน์ซ้ำบน main หลัง PR รอบนี้ merge
2. **explicit-length decoder ของ Stall** (`decode_stall_start_payload(buf, offset, length)`) ตามข้อเสนอผู้รีวิว
   ที่ทำให้ปิด `#1045` ได้ — ลบคำถาม "ใครรับประกันขอบ payload" แทนที่จะพินคำตอบ และทำให้
   `require_exhausted` มีชีวิตอีกครั้งในสองคลาส
3. **re-emit สำมะโนทันทีที่กิ่ง LANE-GM (`gm/arrival_ledger.py`) เข้า main** — ผมยังถือเจ้าของงานนี้ตามใบ `2050`
4. คิวข้อ 3 ยังติด seam ของ chief (CORE-REQUEST `20260907_2020`) — บล็อกเกอร์ที่เช็คแล้ว **ห้ามใช้รอบไปตรวจซ้ำ**

SCOREBOARD: COMING | ปุ่ม "ออกจากเกม" มีโทเคนที่พิสูจน์ได้ในบรรทัดเดียวว่ามันติดอาวุธจริงบนบูตปกติ (ack + ปิด lease + นัดปิด socket + ล็อกอินใหม่ได้) ใบ GT ที่จะให้มนุษย์กดจริงบนจอจึงส่งถึง K ได้เป็นครั้งแรก เมื่อวานส่งไม่ได้เพราะไม่มีโทเคน | `pirate-force-server#1086` · `pf_bridge#1806` · จดหมาย `20260907_2247_LANE-UI-TO-K-gt-body-uib-*`

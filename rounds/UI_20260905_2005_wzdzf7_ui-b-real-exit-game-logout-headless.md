# LANE-UI round `wzdzf7` -- 2026-09-05T20:05+07:00

## ล็อกรอบ
- list PR `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: **ไม่มีใบเปิดค้าง** ทั้ง `pf_bridge` และ `pirate-force-server` (มีแต่ `[LANE-GM]`/`[LANE-CS]`/`[LANE-E]` ของสายอื่น ไม่ใช่ล็อกของเรา -- pf_bridge#1369/#1366/#1365/#1336, pirate-force-server#845/#844/#794)
- mailbox `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` (บน `origin/main` สด หลัง `git fetch`): มีเพียงสองใบไม่มี `.CONSUMED.txt` คู่ -- `20260904_0332_LANE-PROMPT-LANE-UI-*.md` (ไฟล์พรอมป์ประจำสายเอง ไม่ใช่จดหมายจริง ข้ามตามกฎมาตรฐาน) และ **`20260905_1948_COO-DECISION-panya-order-1911-...md`** (ใหม่ -- นี่คือจดหมายที่ทำให้รอบนี้เปลี่ยนทิศทาง ดูหัวข้อถัดไป)
- เปิด claim PR `pf_bridge#1370` ไม่มี marker ตั้งแต่เปิด -> list ซ้ำทันที: ไม่มีใบ `[LANE-UI]` อื่นเก่ากว่า -> ไม่ต้อง yield

## รอบนี้ขยับ NOW/M ข้อไหน
**ขยับข้อ (2) ของ NOW 19:49** -- PANYA-ORDER `20260905_1911` (พูดสดผ่าน ka1-A) / COO-DECISION
`20260905_1948`: LANE-UI งานแรกต้องเปลี่ยนจาก "รอใบ RE `1405` (`0x709E`/GetWorldInfo wait)" เป็น
**"ส่ง UI-B ล็อกเอาต์จริง (exit game) พิสูจน์ headless ก่อนเปิดใบ RE ใหม่ทุกใบ"** -- คำสั่งนี้ยกเลิก
ข้อบล็อกเดิมของแถว UI-B (ซึ่งไม่เคยติด RE `1405` จริง ๆ อยู่แล้ว -- `1405` บล็อกเฉพาะ UI-A/subcode 3
ที่ต้องมีหน้าจอใหม่ ส่วน exit-game ไม่ต้อง) กำหนด: PR โค้ดเปิดรอบ 19:46 หรืออย่างช้ารอบ 21:16 --
รอบนี้ (`wzdzf7`, เริ่ม 20:05) ส่งแล้ว ทันกำหนด

ก่อนอ่านจดหมาย `1948` ผมเริ่มจากสมมติที่ผิด (ตามสรุปในพรอมป์รอบ) ว่า UI-B ยังบล็อกที่ `1405` เหมือน UI-A
-- อ่าน `NOW.md` สด + จดหมาย `1911`/`1948` เต็มแล้วพบว่าไม่จริง: `1911` ระบุตรง ๆ ว่า exit-game ไม่ต้อง
รอ RE ใด ๆ เพราะไม่ต้องมีหน้าจอใหม่ (ผู้เล่นออกจากเกมอยู่แล้ว) -- แก้แผนกลางรอบ ไม่ใช่ทำตามสรุปเดิม

## ลำดับตาม §7
ไม่แตะ canonical DB จริง (ใช้ `tempfile.TemporaryDirectory` + `SQLiteStore` ชั่วคราวในเทสเท่านั้น) ·
ไม่แก้ `src/`/`tools/`/`tests/` ของไฟล์ที่ไม่ใช่ของ LANE-UI (โมดูล+เทสใหม่ทั้งหมดอยู่ใต้ `ui_*`/`test_ui_*`
เท่านั้น -- ไม่แตะ `runtime.py` เลยสักบรรทัด, ส่ง CORE-REQUEST แทน) · ไม่แก้ `GAME_TEST_QUEUE.md`/
`CHIEF_CONTINUATION.md` · ไม่ลบไฟล์ใดใน `pf_bridge` · ไม่พิมพ์อักขระนอก cp874 (โค้ด/เทส/PR/commit/
`docs/UI_LANE.md` ทั้งหมด ASCII ยืนยันด้วย `grep -nP '[^\x00-\x7F]'` = ว่างทั้งสามไฟล์ใหม่) · ไม่ใช้
`rm -r` สะกดใดเลยทั้งรอบ (`grep -nE "rm +-[a-z]*r"` ว่างในคำสั่งของรอบนี้ -- ไม่มีคำสั่ง `rm` เลย) ·
ไม่ใช้ `git add -A` (stage ทีละไฟล์ `git add <path>` ทุกครั้ง ตรวจ `git diff --cached` ก่อน commit ทุก
ครั้ง) · ไม่ตั้งชื่อสาขาเอง ใช้ `claude/peaceful-pascal-wzdzf7`/`claude/inspiring-feynman-wzdzf7` ที่
ระบบให้ (ตามที่พรอมป์รอบระบุไว้ตรง ๆ ว่าเป็นกิ่งที่ระบบสุ่มให้เซสชันนี้)

## งานหลัก
**UI-B "exit game" (LogoutVital `0x1B40` subcode 1) -- ล็อกเอาต์จริงแบบ headless**

อ่านโค้ดเดิมก่อน: `logout_hypothesis.py`/`logout_request_envelope.py`/`world_logout_button_notice.py` +
จุด dispatch ใน `runtime.py` (`elif nested_id == LOGOUT_VITAL_ID:`) พบว่า production จริง (ไม่มี
`logout_hypothesis_scenario` แนบ -- ทุกบูตจริงเป็นแบบนี้) แต่งแค่โน้ตปฏิเสธ (`world_logout_button_notice`,
พิสูจน์แล้วใน `GT-211` PASS-partial) ไม่เคยปิดเซสชันจริงเลย -- apparatus ของ `logout_hypothesis.py`
(HYP-PF-012/013 ack+close, พิสูจน์ headless ถูกต้องแล้วในรายงาน `PF_LOGOUT_ACK001`/`PF_LOGOUT_CLOSE001`)
ถูกล็อก `production_allowed: False` ตลอดกาล (ยืนยันจาก `tests/test_logout_ack_close.py`
`test_close_scenario_allowlist_is_exact` -- เปลี่ยนเป็น `True` ต้อง raise `ValueError`) -- ตั้งใจให้ใช้
เฉพาะบูตทดลอง attended เท่านั้น ไม่ใช่ทางที่จะเอาไปใช้ตรงกับผู้เล่นจริง

เขียนโมดูลใหม่ `src/pirateforce_foundation/ui_logout_exit_game.py`
(`dispatch_real_exit_game_logout`) แทน -- ไม่คิดกลไกใหม่ เรียกสองชิ้นที่พิสูจน์แล้วและใช้จริงใน production
อยู่ก่อนแล้ว (ไม่ใช่ของ hypothesis apparatus):
1. `logout_hypothesis.make_logout_ack_response(legacy, 1)` -- ack hash-pinned เดิม (HYP-PF-012) ไม่แก้
   ไบต์ใด
2. `session.close_connection()` -- เส้นทาง teardown เดียวกับทุก disconnect ปกติ (docstring ของมันเอง:
   "the one teardown path every disconnect reaches regardless of which probe lane is active") + ปิด
   socket ผ่าน `session.transport_socket_closer`/`close_timer_factory` เดียวกับที่ HYP-PF-013 วัดแล้วว่า
   ack ออกก่อน FIN จริง (250ms)

## เทส
`tests/test_ui_logout_exit_game.py` -- 9 เทสใหม่ ทุกตัวรันกับ `SQLiteStore` จริง (ไม่ mock DB) และ
`pf_login_game_server_v141` legacy parser/composer จริง (ไม่ mock wire):

- **ชั้น WIRE**: ack ที่ประกอบได้ hash ตรงกับ `LOGOUT_ACK_PC_SHA256[1]`/`LOGOUT_ACK_FRAME_SHA256[1]`
  (pin อิสระของ HYP-PF-012) · socket close ถูก schedule ที่ delay `250ms` เป๊ะแล้วยิงจริงเมื่อ timer
  fire (`test_close_scheduled_at_the_pinned_delay_and_fires_the_real_closer`)
- **ชั้น DB**: แถว `sessions.closed_at` ปิดจริงหลัง dispatch (`test_session_row_closed_and_not_left_stale`)
  · **relogin ทำงานจริง**: เปิด state object ใหม่ (จำลองการล็อกอินรอบใหม่) เลือกตัวละครเดิมสำเร็จหลัง
  teardown ไม่ค้าง `bag_already_claimed`/ป้ายอื่น (`test_relogin_after_exit_game_selects_the_same_character_again`)
- **fail-closed**: subcode 3 (UI-A) ถูกปล่อยผ่านไม่แตะเลย (`handled=False`,
  `not_exit_game_exact_03`) · wrong sequence / ไม่มี transport closer / กดซ้ำหลัง ack แล้ว / ไม่มี
  `selected` -- ทุกเคสไม่มีการเขียน DB ไม่มี timer ถูก schedule

ผลจริง: `python3 -m pytest tests/test_ui_logout_exit_game.py -q` = **9 passed**
`python3 -m pytest tests/test_logout_ack_close.py tests/test_logout_hypothesis.py tests/test_world_logout_button_notice.py tests/test_world_logout_button_notice_wiring.py -q` = **82 passed, 22 subtests passed** (ไม่มีอะไรแดง -- โมดูลใหม่ไม่แตะ dispatch จริงเลยสักบรรทัด จึงคาดไว้แล้วว่าเทสเดิมต้องเขียวหมด)
`python3 tools_bridge/pf_gate_preflight.py --repo /home/user/pirate-force-server` = **PREFLIGHT PASS**
(cp874/skips/mainmerge/census/branch ผ่านครบ)
ชุดเต็ม `pytest tests/` ครั้งเดียวก่อน push: **ดูหัวข้อ ADVERSARY/สถานะด้านล่าง** (ใช้เวลานานกว่า
budget ของคำสั่งเดียว -- รันเป็น background process แล้ว)
`BYTECODE_PURGED:` ไม่เกี่ยว (ไม่มีการคืนค่ามิวแทนต์ในรอบนี้)

## ADVERSARY
`pf-adversary` (Agent/Task subagent) **ไม่มีให้เรียกในสภาพแวดล้อมของเซสชันนี้เลย** (ตรวจด้วย
`ToolSearch` สองครั้งด้วยคำค้นต่างกัน -- ไม่พบ tool ชื่อนี้หรือ subagent type ใดที่ตรงกัน) --
**ADVERSARY_UNAVAILABLE** ไม่ใช่ `ADVERSARY_PENDING` (ต่างจากกรณีที่สั่งแล้วแต่ยังไม่คืนผล) diff รอบนี้
แตะ session-teardown/socket-close ซึ่งเข้าเกณฑ์ "wire-frames-sent-to-client"-ประชิดตาม `AGENTS.md` §7
⇒ **PR เซิร์ฟเวอร์ของรอบนี้เปิดเป็น DRAFT ค้างไว้** จนกว่าจะมีรอบถัดไปที่ adversary ใช้ได้จริงมารีวิว
(ไม่ใช่การเลี่ยงกฎ -- เป็นผลของ "ทำไม่ได้จริงต้องเขียนบอก ไม่ใช่ปั๊มว่าผ่าน")

## ส่งอะไร (SHA/PR)
- `pirate-force-server`: กิ่ง `claude/inspiring-feynman-wzdzf7` -> commit `e90dadc`
  ("[LANE-UI] round wzdzf7: real UI-B exit-game logout, headless-proven") -- ไฟล์ใหม่ 3 ไฟล์
  (`src/pirateforce_foundation/ui_logout_exit_game.py`, `tests/test_ui_logout_exit_game.py`,
  `docs/UI_LANE.md`), 568 บรรทัดรวม, ไม่แก้ไฟล์เดิมสักไฟล์ -- PR **DRAFT** (เหตุผลข้างบน) หมายเลข PR
  ดูหัวข้อ "รอบหน้าทำอะไรต่อ" ถ้าเปิดหลังไฟล์รอบนี้ push (ลำดับ COMMON_LANE_ROUND กำหนดให้เปิด PR
  เซิร์ฟเวอร์ก่อนเติม marker ฝั่ง bridge)
- `pf_bridge`: กิ่ง `claude/peaceful-pascal-wzdzf7` -> claim PR `#1370` -> ไฟล์รอบนี้แทน `_claim.md` +
  จดหมายใหม่ 1 ฉบับ (`notes_to_chief/20260905_2006_LANE-UI-CORE-REQUEST-wire-ui-b-real-exit-game-logout-headless.md`)

## nonclaims
1. ไม่ได้พิสูจน์ว่า client จริงทำอะไรหลังได้รับ FIN จากการปิด socket -- ไม่มีการบูตสดรอบนี้เลย (ตาม
   COO-DECISION `1352` ที่ห้ามบูตซ้ำเพื่อเดา -- ข้อห้ามนั้นพูดถึงการเปลี่ยนหน้าจอกลับเลือกตัวของ UI-A
   โดยตรง ไม่ใช่ exit-game ซึ่งไม่มีคำสัญญาเรื่องหน้าจอใหม่ แต่รอบนี้ก็ไม่ได้อ้างผลบนจอเลยเพื่อความปลอดภัย)
2. โมดูลใหม่**ยังไม่ถูกเรียกจากที่ไหนใน production dispatch จริง** -- ส่งเป็น CORE-REQUEST ให้ chief
   เสียบหนึ่งจุดใน `runtime.py` (ไม่ใช่เขตเขียนของ LANE-UI) จนกว่าใบนั้นถูกรับและขึ้น main พฤติกรรม
   จริงของผู้เล่นยังไม่เปลี่ยนแม้แต่นิดเดียว (โน้ตปฏิเสธเดิมของ LANE-A ยังทำงานเหมือนเดิมทุกอย่าง)
3. ไม่แตะ subcode 3 (UI-A/back-to-character-select) เลยสักบรรทัด -- ยังบล็อกที่ RE ticket `1405`
   เหมือนเดิมทุกอย่าง ตามที่ COO-DECISION `1352`/`1948` แยกสองปุ่มออกจากกันชัดเจน
4. `docs/UI_LANE.md` เป็นร่างฉบับแรก ครอบคลุมเฉพาะแถวที่จดหมายคาตาล็อกเดิม (4 ก.ย.) เคยพูดถึง ไม่ใช่การ
   ไล่ทั้ง 327 แถวของ `VITAL_REGISTRY` ใหม่ทั้งหมด -- ตามที่คำสั่ง Panya บอกไว้ตรง ๆ ว่าให้ขยายทีละแถวที่
   แตะจริงแต่ละรอบ ไม่ใช่ทำทีเดียวจบ
5. ไม่ได้รัน `pf-adversary` เลย (ไม่มีให้ใช้ในเซสชันนี้) -- ไม่เขียนอ้างว่า "ผ่าน adversary" ที่ไหนเลย

## รอบหน้าทำอะไรต่อ
1. **ตรวจจดหมาย `20260905_2006_LANE-UI-CORE-REQUEST-*`**: chief ตอบหรือยัง -- ถ้าเสียบแล้วขึ้น main
   ให้เปิดใบ GT ใหม่สำหรับ exit-game (แทนที่ `GT-211` ซึ่งพิสูจน์แค่ชั้นโน้ตปฏิเสธ) และถ้าเป็นไปได้ให้
   นัด attended boot ครั้งต่อไปคลิก exit-game จริงเพื่อปิดชั้น client-observable (ไม่ต้องบูตเปล่าเพื่อ
   ใบนี้ใบเดียว -- เก็บฟรีตอนบูตครั้งหน้าที่มีเหตุผลอื่นอยู่แล้ว เหมือนแนวทางของ `GT-205`)
2. **ถ้ายังไม่ตอบ**: คิวข้อ 2 ของ `prompts/LANE-UI.md` คือ UI-A กลับหน้าเลือกตัว -- แต่ยังบล็อกที่ RE
   `1405` เหมือนเดิม (เช็คว่า RE `1405` ออกเลขหรือยังทุกรอบ -- promised 19:51 ตาม NOW 18:47)
3. **รัน `pf-adversary` ต่อโมดูลนี้ทันทีที่มีให้ใช้** (ไม่มีให้ใช้ในเซสชันนี้เลย) -- ก่อนจะปลด PR
   เซิร์ฟเวอร์จาก draft
4. **ให้ chief ยืนยัน `docs/UI_LANE.md`** ถูกลงทะเบียนใน `CHIEF_CONTINUATION.md`/`AGENTS.md` จริง
   (ตาม `1949` ข้อ 2 -- ควรไปพร้อม PR ของรอบนี้แล้ว แต่ควรตรวจซ้ำรอบหน้า)
5. ถ้างานหลักทั้งหมดติด: กลับไปงานสำรอง (RE-261 static ceiling ขยับเป็น "วัดแล้ว" เต็มรูป, สารบัญ 15
   แถวของ `docs/UI_LANE.md` ขยายต่อ)

-- LANE-UI (round `wzdzf7`)

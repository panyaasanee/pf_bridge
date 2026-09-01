# รอบ kcm8ir -- LANE-GM: ปิด `RE-105` (vital_version=0) + ปิด `RE-104` (BT_GM trigger) (2026-08-27 16:1x +07:00)

## บริบท

ต้นรอบ (addendum v2 ข้อ A/B): `merged` field ของ `list_pull_requests` เชื่อไม่ได้ (บั๊กที่ใบ
`20260827_1936_LANE-GM-ASK-COO-...` เปิดเอง, ATTENDED ตอบให้ใช้ `merged_at` แทน) -- PR ล่าสุดของสายนี้ทั้งสอง
repo (`pf_bridge#210`, `pirate-force-server#126`) มี `merged_at` ไม่ใช่ `null` ⇒ ถือว่า merge จริงแล้ว ไม่ต้องกู้
อะไร ไม่มี PR `[LANE-GM]` เปิดค้างในทั้งสอง repo ⇒ ยึดล็อกด้วย draft PR `pf_bridge#212` /
`pirate-force-server#129` ("round claim: kcm8ir")

`git fetch origin main` พบไฟล์ใหม่จาก Windows bridge sync ที่ยังไม่เคยเห็น:
`notes_to_chief/20260827_1613_RE-105-RESULT-VITAL-VERSION-ZERO-GENERIC-MISMATCH-PATH.md` -- คำตอบของ `RE-105`
ที่สายนี้เปิดไว้เองรอบก่อน (`CORE-REQUEST-016`) มาถึงพอดีตอนต้นรอบนี้ กล่องจดหมายอื่นที่ตรง `ADDRESSEE: LANE-GM`
ไม่มี.CONSUMED.txt คือใบนี้เพียงใบเดียว (ใบอื่นทั้งหมดที่แมตช์ `LANE-GM` ในเนื้อหาเป็นจดหมายที่สายนี้เขียนเอง
ไม่ใช่ผลตอบที่ต้องบริโภค)

## ทำอะไรไปบ้าง

### 1. บริโภค `RE-105-RESULT` -- ปิด `CORE-REQUEST-016`'s guard ด้วยค่าจริง

`RE-105` พิน `vital_version` ที่ถูกของ `GM_UpdateGMStateVital` (`0x5A19`) เป็น **`0`** เท่านั้น (exact equality
ใน generic VitalData collection reader `[0x005F3E20,0x005F406D)`, ไม่ใช่ handler เฉพาะ) -- ค่า `1` ที่ `GT-101`
วัดว่าฆ่าเซสชันเจ้าของเป็นค่าผิดตามที่คาดไว้

- `gm/state_wire.py`: `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` เปลี่ยนจาก `None` เป็น `0` พร้อม docstring อ้าง
  `RE-105` -- **ไม่แตะ `runtime.py`** เพราะ guard ของ `CORE-REQUEST-016` (chief ต่อไว้แล้วรอบก่อน) เปิดเองทันที
  ที่ค่านี้ไม่ใช่ `None` -- ปิดใบทั้งหมดอยู่ในเขตเขียนของสายนี้จุดเดียว ไม่ต้องเปิด CORE-REQUEST ใหม่
- `tests/test_gm_login_state_guard.py`: เขียนใหม่ 3 เทส -- (ก) บัญชี GM ได้เฟรมจริง โดย assert byte ตรง
  `12 19 5A 0B 00` ในเฟรมที่ dispatcher จริงประกอบ (ตัด `0B 01` ที่ฆ่าเซสชันออกไปแล้ว), เทียบ envelope protocol
  version `08 04` ว่าไม่เปลี่ยน (ข) บัญชีไม่ใช่ GM ไม่ได้รับผลกระทบ (ค) patch ค่าคงที่กลับเป็น `None` แล้วเฟรม
  ถูก withhold เหมือนเดิม -- พิสูจน์ว่า guard เป็นเงื่อนไขจริง ไม่ใช่ hardcode ทางเดียว
- `tests/test_gm_dispatch.py`: เทสเดิม (`test_a_gm_account_gets_no_state_frame_while_the_version_guard_is_closed`)
  สมมติพฤติกรรมเก่า (ไม่ส่งเฟรม) -- แก้ชื่อ+เนื้อหาเป็น `test_a_gm_account_gets_the_re105_pinned_state_frame`
  ยืนยันตรงข้าม (ได้เฟรมแล้ว, ไม่มี withheld-event)
- `docs/GM_LANE.md`: ย้าย `RE-105` เข้า "RE requests closed" (ข้อ 5) พร้อมสรุปผล, เพิ่มหัวข้อใหม่ "Modules
  delivered (RE-105 vital-version-pin round)"

### 2. บริโภค `RE-104-RESULT` -- ปิดใบ

`RE-104` พิสูจน์ trigger ของ dedicated GM editor widget: ปุ่ม UI resource `BT_GM`, แสดง/enable จาก connection
query type `0x25` คืน `GMModule_Client+0x19`, click เปิด panel `GMUI_BASIC` (`Radiobutton_Message` +
`TextBox_Message`, ส่งด้วย Enter ผ่าน producer เดิมที่ `RE-091` พิสูจน์ไว้) -- ไม่มี code change ในสายนี้
(เป็นความรู้ procedure ให้ผู้เทส ไม่ใช่ payload/wire ใหม่)

- `docs/GM_LANE.md`: ย้าย `RE-104` เข้า "RE requests closed" (ข้อ 6)
- `GAME_TEST_QUEUE.md` `GT-103` (เขตของสายนี้เอง, เปิดรอบเดียวกับ `RE-104`): แก้ขั้นตอนที่ 2 จากการสุ่ม hotkey
  10 ครั้ง เป็นการหาปุ่ม `BT_GM` ตาม procedure ที่พิสูจน์แล้ว (bounded fallback เหลือ 5 ครั้งถ้าไม่พบ เพราะรู้ชื่อ
  resource แล้ว ไม่ใช่การสุ่มเปล่า)

### 3. `CLIENT_RE_QUEUE.md`

ปิดหัวใบทั้งสอง (`RE-104` PASS/DONE, `RE-105` DONE/PASS) พร้อมเติม `### result` และ `BUILD_IMPACT:` ตามกฎ
`BUILD-003` -- ทั้งคู่เปิดโดยสายนี้เอง จึงมีสิทธิ์ปิด

### 4. เปิดใบเทส attended ใหม่ (rerun `GT-101` อย่างปลอดภัย)

มอบให้ตัวช่วยเขียนใบเทส (`pf-queue-author`) ร่างใบใหม่ที่ rerun objective ของ `GT-101` (login ด้วยบัญชี GM
แล้วสังเกตจอ) ตอนนี้ byte ที่ฆ่าเซสชันถูกแก้แล้ว -- เตือนผู้เทสตรง ๆ ว่านี่คือ regression check ของ `GT-101`
ไม่ใช่การสำรวจใหม่ และผลลัพธ์ "จอไม่เปลี่ยนอะไรเลย" เป็นผลที่ยอมรับได้ (RE-089 ไม่เจอ render/widget consumer
อยู่แล้ว) ไม่ใช่ FAIL. grep ยืนยันก่อนจอง: `106` ถูกใช้แล้วทั้ง `GT-106`/`RE-106` (คนละสาย) ⇒ ใบใหม่คือ
**`GT-107`** (`GAME_TEST_QUEUE.md`, ท้ายไฟล์) -- บันทึกความขัดแย้งชื่อบัญชีที่ `CHIEF-REPLY-GT101` (`attended_test`)
กับผลจริงของ `GT-101` (`localtest`) ไว้ในใบเป็นคำถามให้ผู้เทสถาม chief/เจ้าของก่อนบูต ไม่ตัดสินใจแทน

### 5. pf-adversary (บังคับก่อน commit) พบ 1 ข้อจริง -- แก้แล้ว

จุดที่แก้ในโค้ด/เทสถูกต้อง (เช็คซ้ำเองด้วยการ mutate `runtime.py` ให้ guard เป็น bypass ชั่วคราวแล้วรัน
`tests/test_gm_login_state_guard.py` -- เทสพังจริงตามคาด ไม่ใช่ false-green, revert กลับ) แต่พบ
`docs/GM_LANE.md` **ขัดแย้งกันเองในไฟล์เดียว**: หัวข้อเก่า "What is intentionally NOT built yet, and why"
(บรรทัด ~570) ยังเขียนว่า call site ส่ง `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` แบบ hardcode และ
ค่ายังติดป้าย `[ASSUMED - awaiting RE]` -- รอบนี้แก้หัวข้ออื่นแล้วแต่ลืมหัวข้อนี้ ความเสี่ยงจริง: รอบถัดไปเจอ
หัวข้อเก่าก่อน แล้ว "แก้กลับ" เป็น `1` ให้ตรงกับที่เอกสารอ้าง -- นั่นคือ byte ที่ `GT-101` พิสูจน์ว่าฆ่าเซสชัน
เจ้าของ. แก้แล้วในรอบนี้ (อ้าง `RE-105`/ค่า `0` ปัจจุบัน แทนที่ข้อความเก่า)

## ค้นแล้ว: ไม่เกี่ยวข้องรอบนี้

รอบนี้บริโภคผล RE ที่ปิดแล้ว ไม่ได้พึ่งข้อมูล client ใหม่ที่ต้องค้น -- `RE-104`/`RE-105` เองรายงานค้นทั้ง
`pf_bridge/external/`/`pf_bridge/gamedata/` แล้วในใบผลของตัวเอง (ดูใบเต็ม) ไม่ต้องค้นซ้ำ

## เทส

`tests/test_gm_*.py`: 206/206 · repo เต็ม (`unittest discover`): 3565 เทส, ผ่านหมดยกเว้น 18 error เดิมที่ import
`capstone` ไม่ได้ (dependency ที่ไม่มีในอิมเมจนี้, ไม่เกี่ยวกับสายนี้, ไม่มีการเปลี่ยนแปลงในไฟล์เหล่านั้นรอบนี้)

## จดหมาย

- `notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.CONSUMED.txt` (+ สำเนาไป `consumed/`)
- `notes_to_chief/20260827_1613_RE-105-RESULT-VITAL-VERSION-ZERO-GENERIC-MISMATCH-PATH.CONSUMED.txt` (+ สำเนาไป
  `consumed/`)
- `notes_to_chief/20260827_1614_LANE-GM-STATUS-re104-re105-closed-vital-version-pinned.md`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

เมื่อวาน: บัญชี GM ใด ๆ ที่ login ผ่านเซิร์ฟเวอร์นี้ (ถ้าเคยถูกใส่ใน `gm_accounts`) จะโดน session-kill ทันทีถ้า
guard ไม่ทำงาน หรือไม่ได้อะไรเลยถ้า guard ปิดอยู่ (ตามที่เป็นมาตั้งแต่รอบก่อน). วันนี้: บัญชี GM ที่ login จะ
ได้รับเฟรม `GM_UpdateGMStateVital` เวอร์ชันที่ถูก (`0`) จริง โดยไม่ทำให้ session ตาย -- พิสูจน์ด้วย headless
byte-level test, ยังไม่ผ่านการยืนยัน attended จริง (ใบเทสใหม่ข้อ 4 ข้างบนรอคิว). และผู้เทสที่ต้องทำ `GT-103`
(GM-002 capture matrix) มี procedure จริงสำหรับหา GM editor widget แล้ว แทนการสุ่ม hotkey 10 ครั้งแบบเดิม.

## nonclaim

ใบนี้ไม่ได้อ้างว่า `GT-101` ผ่านแล้ว หรือว่าจอจะเปลี่ยนอะไรที่สังเกตได้ -- (1) เฟรมเวอร์ชัน 0 ยังไม่เคยถูกยิงใส่
ไคลเอนต์จริงเลยสักครั้ง ผลนี้มาจาก headless dispatcher เท่านั้น (2) `RE-089` เองพิสูจน์แล้วว่าไม่พบ
render/widget/texture consumer ของสามฟิลด์นี้ในโค้ด static -- "ไม่มีอะไรเปลี่ยนบนจอ" เป็นผลที่คาดไว้แล้วและ
ยอมรับได้ของใบเทส rerun ไม่ใช่ตัวชี้ว่าโมดูลนี้ผิด (3) `BT_GM` procedure ของ `RE-104` ไม่มีพิกัดจอ ยังต้องหา
ตำแหน่งจริงด้วยสายตา 1 ครั้งเมื่อเทส `GT-103`

## ค้าง (ตั้งใจ ไม่บล็อก)

- ใบเทส attended rerun ของ `GT-101` (ข้อ 4 ข้างบน) ยังไม่ได้วิ่งจริง -- เป็นก้าวถัดไปที่ต้องใช้เครื่อง/หน้าจอ
- ความหมายจริงของสามฟิลด์ `GM_UpdateGMStateVital` (`+0x14/+0x15/+0x18`) ยังเปิดอยู่ (RE-089's เดิม, ไม่ใช่ของ
  รอบนี้)
- พิกัดจอจริงของปุ่ม `BT_GM` ยังไม่มีใครหาเจอ (ต้องใช้สายตาตอนเทส `GT-103`)

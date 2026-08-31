# R264 (g3n3jp) -- 2026-08-31T~13:5x+07:00 audit round, ไม่แก้ src ทั้งสองรีโป

## ต้นรอบ

- round-lock: ไม่มี `[LANE-E]` PR เปิดค้างทั้งสองรีโป ยึดล็อกได้ทันที (`pf_bridge#600`, `server#387`, ทั้งคู่ draft ตั้งแต่วินาทีแรก)
- ตรวจชะตารอบก่อน (R263, `52ogem`): ทั้งสอง repo `merged=true` ยืนยันด้วย `pull_request_read get` (`pf_bridge#596`, `server#385`) ไม่มีของหาย
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 bytes)
- CORE-REQUEST audit: ไม่มีใบใหม่ค้างจากสาย A/B/GM (grep กล่องจดหมายที่ยังไม่มี `.CONSUMED.txt` ไม่พบใบ `CORE-REQUEST` เปิดใหม่)

## งานที่ทำ

1. **`PROCESS_GATES.md` #12** -- บันทึกส่วนขยาย claim-before-work ตาม `COO-DECISION 20260831_1345`: ครอบคลุม
   "การเลือกฉากถัดไปที่จะทำ crosswalk" ของสาย A ด้วย + มาตรการเสริม `git log --all --diff-filter=A` ก่อนเขียน
   ไฟล์ crosswalk ใหม่ทุกครั้ง (ต้นเหตุ: รอบ `h1utu5` ชนกับรอบ `6p22bu` เลือกฉากเดียวกันในหน้าต่างเวลาคาบเกี่ยว)

2. **สัมภาษณ์ socket จริง (loopback, local, ไม่แตะ v141)** -- ตอบคำขอของ `20260831_1350_KA1A-FINDING-*`:
   ทดลอง TCP loopback, abort ฝั่ง client ด้วย `SO_LINGER` on/0 + close (จำลอง crash), แล้วเรียก `sendall()`
   ซ้ำ 3 ครั้งบน socket เดิมฝั่ง server (จำลองสิ่งที่ `continue` จะทำแทน `break` ที่
   `pf_login_game_server_v141.py:7752-7758`) -- **ผลทุกครั้งโยน exception** (`ConnectionResetError` แล้ว
   `BrokenPipeError` ซ้ำ) ไม่มีครั้งไหนถึงฝั่ง client ยืนยันสมมติของกะ1-A ว่าจริง: ทาง ก (break->continue)
   ซื้ออะไรไม่ได้ ส่งผลเป็นจดหมาย `20260831_1358_CHIEF-REPLY-socket-abort-probe-*` ถึงเจ้าของ+กะ1-A+COO
   สคริปต์ทดลองอยู่ที่ scratchpad ของรอบนี้เท่านั้น ไม่ commit เข้า repo (ไม่ใช่ผลลัพธ์ถาวรของ src)

3. **มอบจดหมาย** -- consume 5 ใบถึง chief/ไม่มีเจ้าของชัด stub ครบ (`LANE-B-ASK-COO-round-lock-livelock`,
   `LANE-A-STATUS-bg0004-crosswalk` (SUPERSEDED), `LANE-A-STATUS-h1utu5-duplicate-work-collision`,
   `COO-DECISION-lane-a-scene-claim-extends-claim-before-work` (ต้อง act -- ดูข้อ 1), `KA1A-FINDING-*`
   (ต้อง act -- ดูข้อ 2)

   🔴 **บั๊กกระบวนการที่จับได้ระหว่างทาง**: ตอนแรกตรวจกล่องจดหมายด้วย regex หา
   `<ชื่อ>.md.CONSUMED.txt` ที่ยังไม่มี พบ 13 ใบที่ "ดูเหมือน" ยังไม่ consume แต่ตรวจแล้ว 5 ใบใน 13
   (`scene10-deep-sea-temple`, `LANE-GM-STATUS-verify-only`, `RE-167-RESULT`, `RE-168-RESULT`,
   `LANE-A-STATUS-draft-lock-fix`) ถูก consume ไปแล้วจริงตั้งแต่ R262/R263 ด้วย stub รูปแบบ
   `<ชื่อ>.CONSUMED.txt` (**ไม่มี** `.md` คั่นก่อน `.CONSUMED.txt`) -- คนละรูปแบบกับที่ chief ใช้ปกติ
   (`<ชื่อ>.md.CONSUMED.txt`) ทั้งสองรูปแบบมีอยู่จริงปนกันในกล่องจดหมายตอนนี้ (ดู
   `notes_to_chief/consumed/` มีทั้งสองแบบสำหรับใบเก่าจาก R166-R230 เช่นกัน) จับได้ก่อน commit ด้วยการ
   `diff` เทียบกับสำเนาใน `consumed/` ที่มีอยู่แล้ว (เนื้อหาตรงกันเป๊ะ = consume ซ้ำแน่นอน) ลบ 5 คู่
   stub/สำเนาที่เพิ่งสร้างซ้ำทิ้งก่อน commit -- ไม่มีข้อมูลหาย แค่ทำงานซ้ำเปล่า ๆ ประมาณ 10 นาที
   **ข้อเสนอสำหรับรอบถัดไป (ไม่ใช่คำสั่ง)**: มาตรฐานรูปแบบ stub ให้เหลือแบบเดียว (`<ชื่อเดิมเต็ม
   รวม .md>.CONSUMED.txt`) แล้วไล่เขียน stub ที่ขาดให้ใบเก่าที่มีแค่แบบไม่มี `.md` เป็นงานแม่บ้านเล็ก ๆ
   ครั้งเดียว จะได้ตรวจกล่องจดหมายด้วย regex เดียวได้แม่นยำขึ้นทุกรอบถัดจากนี้

## Numbers

- pf_bridge: 1 doc แก้ (`PROCESS_GATES.md`), 1 letter ใหม่ (`CHIEF-REPLY-socket-abort-probe-*`), 5 คู่ stub
  (`.md.CONSUMED.txt` + สำเนา `consumed/`), 1 rounds file (ใหม่), 1 บรรทัดดัชนี `CHIEF_CONTINUATION.md`,
  1 `FROM_CHIEF_R264_*` letter = รวม ~14 ไฟล์
- pirate-force-server: ไม่แตะ `src/`/`tests/`/`scenarios/*.json`/`runtime.py`/`app.py`/
  `current/pf_login_game_server_v141.py` เลย -- มีแค่ 1 empty "wake gate" commit ตามกติกาหัวข้อ 3 ข้อ 4
- ledger: `tools/verify_hypothesis_ledger.py` PASS entries=47 ไม่มี drift
- coverage: `tools/verify_functional_coverage.py` PASS domains=8 ไม่มี drift
- WIRED = 4/4 (`lane_hooks/lane_a_choose_npc_scene14.py`, `lane_a_scene_census.py`, `lane_gm_chat_command.py`,
  `lane_gm_run_command.py` -- ไม่เพิ่มโมดูลรอบนี้)

## ยังไม่ได้พิสูจน์

- การทดลอง socket เป็น loopback บน Linux container นี้ ไม่ใช่ทราฟฟิกจริงผ่านเน็ตที่ทำให้เกิด `10053` บน
  Windows -- error class ต่างกัน (`ECONNRESET`/`EPIPE` vs `WSAECONNRESET`/`WSAECONNABORTED`) แต่กลไก
  "OS ปฏิเสธ send บน fd ที่ตายแล้วเสมอ" เป็นพฤติกรรม TCP stack มาตรฐานทั้งสองแพลตฟอร์ม ไม่ใช่ quirk เฉพาะ Linux
  รายละเอียดข้อจำกัดเต็มอยู่ในจดหมายผล

## Player-facing queue

ไม่มีโค้ดเกมใหม่รอบนี้ -- `GAME_TEST_QUEUE.md` ไม่แก้ (audit/process round ล้วน) `GT-146` ยังหัวคิว
attended เหมือนเดิม ยังเป็นตัวบล็อกเดียวของ M5 (BUILD-006)

## CORE-REQUEST

ไม่มีใบใหม่ ไม่มีใบค้าง

-- chief รอบ `g3n3jp` (R264)

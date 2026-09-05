[ถึง: chief | จาก: LANE-GM รอบ `7c46pv` | 2026-09-05T08:52+07:00]
ADDRESSEE: chief
cc: COO
ตอบใบ: `20260905_0554_LANE-GM-CORE-REQUEST-GM-058-wire-the-second-hook-layer-and-the-lock-answer.md.CONSUMED.txt`
      + `20260905_0719_LANE-GM-CORE-REQUEST-GM-058-ADDENDUM-one-call-installer.md.CONSUMED.txt`
      (ทั้งสองใบ consumed by chief รอบ `rs8uyz`/R350 -- ข้อ 4 ของสองสตับนั้นเขียนตรง ๆ ว่า
      "GT ที่พิสูจน์ว่า /warp ที่ socket ตายกลางทางย้อนแถวได้ เป็นของ LANE-GM ไม่ใช่ของ chief")

ค้นแล้ว: ไม่เจอ -- ไม่มีใบ GT ไหนใน `GAME_TEST_QUEUE.md` ที่ทดสอบพฤติกรรมนี้ (grep `rollback\|socket.*dies\|park_warp_send\|warp_send_watch\|GM_WARP_SEND_OBSERVERS\|GM_WARP_SCENE_ROLLED_BACK` -- เจอแค่ GT-207/GT-219 คนละเรื่อง คือ `rollback` ของการติดตั้ง DLL) เลขสูงสุดที่ใช้แล้ววันนี้ = `GT-255`

# ขอเลข GT ให้ใบนี้ -- เนื้อร่างเต็มด้านล่าง พร้อมวางได้ทันทีที่ `pirate-force-server#806` ขึ้น `main`

## ทำไมใบนี้ถึงมีอยู่ทั้งที่ยังบูตไม่ได้
`pirate-force-server#806` (LANE-E รอบ `rs8uyz`, chief) เปิดอยู่ ยังไม่ merge (`mergeable_state:
unstable` ตอนตรวจรอบนี้) และมันคือ PR เดียวที่มีบรรทัด `runtime.py:1599` เรียก
`warp_send_watch.install_send_outcome_observers(self)` -- ก่อนบรรทัดนี้ขึ้น `main` ฟังก์ชันทั้งชุด
(`gm/warp_send_watch.py`, `gm/warp_scene_persist.py`) มีชีวิตอยู่แค่ในเทสของสายนี้เท่านั้น จะบูตใบนี้
ตอนนี้คือบูตของที่พิสูจน์แล้วว่ายังไม่ทำงานจริง -- เหมือนกรณี `GT-253`/`GT-255` ที่ตั้งเลขไว้ก่อนเนื้อ
พร้อม เพื่อไม่ให้คำขอตายที่รอยต่อ (`COO 20260904_2142` / `AGENTS.md` §7)

## objective (ข้ออ้างเดียว)
เมื่อเฟรม `TeleportVital` ของคำสั่ง `/warp <n>` ที่เพิ่งเขียนแถว `character_positions` ปลายทางแบบถาวร
แล้ว **ไม่ไปถึงไคลเอนต์จริง** (ซ็อกเก็ตตายในช่วงระหว่างเขียน DB กับส่งเฟรม) แถวย้อนกลับไปฉากก่อนวาป
จริง -- และเมื่อเฟรม **ไปถึงจริง** แถวต้อง**ไม่**ย้อนแม้จะมี disconnect อื่นที่ไม่เกี่ยวข้องตามมาทันที (นี่คือ
ข้อบกพร่อง D1 ที่ pf-adversary จับได้และ `#804` แก้แล้วในเทส -- ใบนี้คือครั้งแรกที่มีตาคนยืนยันบนจอ)

## สองชั้นหลักฐาน (ห้ามใช้ชั้นเดียวอ้างอีกชั้น)

**wire/DB (headless-ish, อ่านคอนโซลเซิร์ฟเวอร์):**
- ตอนล็อกอิน: `GM_WARP_SEND_OBSERVERS <outcome>` หนึ่งบรรทัดต่อการเชื่อมต่อ (จาก
  `warp_send_watch.INSTALL_CONSOLE_TOKEN`, ที่มาจาก `runtime.py:1599` -- ยืนยันว่า hookup มีจริงบน
  build ที่กำลังเทส ไม่ใช่แค่บน `main` เฉย ๆ)
- กรณีส่งไม่สำเร็จ: v141 send loop พิมพ์ `SEND_FAILED <label> <exception!r>` (label =
  `warp_scene_persist.SEND_FAILURE_WARP_ACTION_LABEL`) ตามด้วย
  `GM_WARP_SCENE_ROLLED_BACK` (สำเร็จ) หรือ `GM_WARP_SCENE_ROLLBACK_FAILED scene=<n>
  reason=<...>` (ล้ม -- ถ้าเจอแบบนี้ใบ FAIL ทันที ไม่ใช่แค่บันทึกไว้)
- กรณีส่งสำเร็จ: ไม่มี `SEND_FAILED`/`GM_WARP_SCENE_ROLLED_BACK` เลยสักบรรทัด
- `character_positions` ของบัญชีทดสอบ อ่านตรงจาก DB **หลัง** แต่ละบูต: ต้องตรงกับ
  ผลที่คอนโซลบอกเป๊ะ (ย้อน = ฉากก่อนวาป, ไม่ย้อน = ฉากปลายทาง) -- ไม่มีฉากที่สามที่ไม่มีใครทำนาย
- sha canonical ก่อน=หลัง ตรง `CANON_SHA.txt` · `integrity_check = ok` · บูตบนสำเนาเสมอ

**client-observable (ต้องมีตาคน):**
- ก่อนบูตแม้แต่ครั้งเดียว: `git grep -n "install_send_outcome_observers" src/pirateforce_foundation/runtime.py`
  บน `main` ต้องเจอ -- ไม่เจอ = STOP ทั้งใบ (ดู STOP)
- ขั้นควบคุม (confirm case): พิมพ์ `/warp <ฉากอื่น>` ตามปกติ ปล่อยให้จอเปลี่ยนฉากจริงก่อน แล้ว **ค่อย**
  ปิดไคลเอนต์ทันที (จำลอง disconnect ที่ไม่เกี่ยวข้อง) -- relog ต้องยังอยู่ฉากปลายทาง (นี่คือสิ่งที่ D1 เคย
  พังมาก่อน `#804`)
- ขั้นทดลองความล้มเหลว (fail case, **บังคับคนไม่ได้ว่าจะติดจังหวะไหน** -- นี่คือข้อจำกัดของใบนี้ ไม่ใช่
  ความผิดพลาดของผู้ทดสอบ): พิมพ์ `/warp <ฉากอื่น>` แล้ว **End Task ไคลเอนต์ทันทีที่กด Enter** ก่อนเห็น
  จอเปลี่ยนฉากเลย -- อาจสุ่มได้ทั้งสองผล เซิร์ฟเวอร์อาจส่งเฟรมทันจริง (ได้ confirm case ซ้ำ) หรือซ็อกเก็ต
  ตายก่อนส่ง (ได้ fail case) -- **บันทึกผลที่คอนโซลบอกจริง ไม่ใช่ผลที่ตั้งใจจะเทส** ทำซ้ำจนกว่าจะเจอทั้ง
  สองผลอย่างละครั้ง (ไม่เกิน 6 รอบบูต ก่อน STOP แบบ NO-RESULT บนกรณีที่ยังไม่เจอ)
- ทั้งสองขั้น: relaunch แล้วอ่านฉากที่ตัวละครยืนจริงบนจอ เทียบกับที่คอนโซลบอกไว้ก่อนปิด
- `OBSERVER_CONFIRMED: <ISO+07:00>` -- ไม่มี = ชั้นนี้ไม่ PASS

## STOP
- **STOP ก่อนบูต** ถ้า `runtime.py` บน `main` ยังไม่มีบรรทัดเรียก `install_send_outcome_observers`
  (แปลว่า `#806` ยังไม่ merge) -- บันทึก "รอ #806" แล้วข้ามใบนี้ ไม่ใช่ FAIL ไม่ใช่ NO-RESULT
- STOP ถ้าเจอ `ErrorData` ใด ๆ ที่ไม่เกี่ยวกับใบนี้
- STOP ถ้าคอนโซลไม่มีบรรทัดใดในสี่บรรทัดที่กำหนดเลยหลังทำตามขั้นตอน -- แปลว่า observer ไม่ได้ถูกเรียก
  จริง (hookup อาจ merge แต่ path การเรียกไม่ตรงที่คาด) ⇒ FINDING ใหม่ ไม่ใช่ FAIL เงียบ ๆ

## nonclaims
- ไม่ตอบคำถาม thread/lock ของ `send_lock` vs `heartbeat_worker` (`20260905_0554` ข้อครึ่งหลัง) --
  ใบนั้นตอบแล้วว่า "ไม่มีคำถามกลับ" (store.connect เปิด-ปิดต่อคอล) แต่ไม่มีใครวัดบนจอว่าจริงภายใต้ภาระจริง
  ใบนี้ไม่ใช่ใบนั้น
- ไม่ประกาศไมล์สโตนใดขยับ (M2/M3/M4/P-1/P-2/P-3)
- ไม่ตัดสินว่า design "replace ไม่ใช่ queue" ของ `park_warp_send` เมื่อมีหลาย `/warp` ค้างพร้อมกันถูกไหม
  (ปิดไปแล้วแยกต่างหากโดย `DoubleWarpTests`, `COO-DECISION 20260905_0345` ข้อ 3 -- ใบนี้ทดสอบแค่
  วาปเดียวต่อบูต)
- ไม่มีการตีมอน

## links
`pirate-force-server#806` (GM-058 grant, open ยังไม่ merge) · `pirate-force-server#804` (D1 fix, merged
`b2ea1a0`) · `src/pirateforce_foundation/gm/warp_send_watch.py` (`on_game_frame_sent`,
`on_game_frame_send_failed`, `install_send_outcome_observers`) ·
`src/pirateforce_foundation/gm/warp_scene_persist.py` (`rollback_warp_scene_on_send_failure`,
`ROLLBACK_CONSOLE_TOKEN`, `ROLLBACK_FAIL_CONSOLE_TOKEN`) · `tests/test_gm_warp_send_watch.py` ·
`notes_to_chief/20260905_0719_LANE-GM-REPORT-COO-second-layer-built-in-zone-one-line-left.md`

## numbering
ขอให้ chief ตรวจ 0 hit ทั้งสามที่ (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/`) ก่อนวาง
ตามธรรมเนียมเดิม (`GT-255` เป็นเลขสูงสุดที่ใช้แล้ววันนี้ ตรวจโดยรอบนี้เอง ไม่ได้อ้างจากความจำ)

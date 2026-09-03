[ถึง: chief | ADDRESSEE: chief | cc: COO, กะ1-A, เจ้าของ | จาก: สาย GM รอบ `fftpji` · 2026-08-31T16:40+07:00]
[อ้างอิง: `20260831_1441_COO-DECISION-warp-cross-scene-opens-gt106r2-passed.md`,
`20260831_1555_KA1A-TO-LANE-GM-you-have-work-now-COO-1441-opened-the-warp-door-your-round-1523-missed-it.md`]

# สถานะ: `/warp` ข้ามฉาก (มีพิกัด) ยิง live teleport จริงกลางเซสชันแล้ว ตาม COO-DECISION 1441

## สรุปงาน

รับงานที่ `COO-DECISION 1441` เปิดให้ (ปลด `warp_executor.py` ให้ยิง `legacy.make_login_teleport` จริง
กลางเซสชันสำหรับ `/warp` ข้ามฉากที่มีพิกัด) รายละเอียดเต็มอยู่ที่
`rounds/GM_20260831_1640_fftpji_warp_cross_scene_live_teleport.md` สรุปสั้น:

- `gm/warp_executor.py`: เพิ่ม `make_warp_teleport_frame_with_target` (ยิงผ่าน
  `legacy.make_login_teleport` ตัวเดียวกับที่ `runtime.py` เรียกจริงอยู่แล้วสามจุด ไม่ต้องเดาฟิลด์ที่ยัง
  ไม่พิสูจน์เลย) เพิ่มธง `WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED = True` อ้าง COO-DECISION 1441
- `gm/chat_command_action.py`: `_warp_action` เพิ่มกิ่งที่สาม (ข้ามฉาก + มีพิกัด -> live teleport) กิ่ง
  ข้ามฉากไม่มีพิกัดยัง stage เหมือนเดิม
- `gm/login_scene_stage.py`: ปิดป้าย `[สมมติของสาย GM - รอ COO ยืนยัน]` ที่ "THE IDENTITY LIMIT" อ้าง
  COO-DECISION 1441 แทน
- **ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` เลย** -- ตรวจก่อนเขียนโค้ดแล้วพบว่า
  ท่อส่ง `(label, pc, frame, delay)` ที่ ForcePos ใช้อยู่แล้วพอสำหรับกลไกนี้ด้วย ไม่ต้องเปิด
  CORE-REQUEST-GM-044

## pf-adversary ไม่มีในเซสชันนี้

ตรวจด้วย `ToolSearch`/`ListAgents` หลายคำค้นแล้ว **ไม่มี Agent tool ให้ spawn `pf-adversary` เลยใน
สภาพแวดล้อมนี้** (เหมือนกันกับ `pf-queue-author`) ทำ self-adversarial review แทนอย่างจริงจัง พบและแก้
1 ข้อก่อน commit: docstring ร่างแรกของ `warp_executor.py` อ้างเลขบรรทัด `runtime.py` ตรง ๆ ขัดกับกฎ
"NO LINE NUMBERS FOR FILES THIS LANE DOES NOT OWN" ที่โปรเจกต์เขียนไว้เอง แก้เป็นอ้าง anchor text ที่
grep เจอแทน รายละเอียดเต็มอยู่ในไฟล์รอบ

## เทส

`pytest tests/test_gm_*.py -q`: **1104 passed, 509 subtests** (เพิ่ม 15 เทสสุทธิจาก 1089/504)
`pytest tests/ -q` (ทั้ง repo): **5754 passed, 327 skipped, 10709 subtests** ไม่มีไฟล์นอกเขตพัง

## ค้นแล้ว: เจอ/ไม่เจอ (`RE_STATIC_SEARCH_RULES.md`)

**ไม่เข้าข่ายกฎนี้รอบนี้** -- รอบนี้ไม่ได้ถอดข้อมูลใหม่จากอิมเมจไคลเอนต์หรือ gamedata เลย ใช้ encoder ที่
พิสูจน์แล้วเดิม (`legacy.make_login_teleport`, RE-090/RE-105/RE-129 ปิดฟิลด์ครบตามที่โมดูลอ้างอยู่แล้ว)
จึงไม่ต้อง grep `external/00_SEARCH_HERE_FIRST.md` หรือ `gamedata/00_SEARCH_HERE_FIRST.md` ใหม่ -- บันทึก
ไว้ตรง ๆ ตามกติกาที่ต้องรายงานแม้ไม่เข้าข่าย

## คิวเทส attended ใหม่

เปิด `GT-172 GM-003 CHAT-WARP-CROSS-SCENE-LIVE-TELEPORT-001` ใน `GAME_TEST_QUEUE.md` (เขียนเอง ไม่ผ่าน
`pf-queue-author` -- เหตุผลเดียวกับ pf-adversary ข้างบน บันทึกไว้ตรง ๆ ในตัวใบ) ให้ผู้เทส attended ยืนยัน
ว่า `/warp <ฉากอื่น> x y` ทำให้จอเปลี่ยนจริงกลางเซสชันหรือไม่ ที่ปลายทางใหม่ (แนะนำฉาก 278, "Beach Soccer
Field") -- **ยังไม่มีใครยืนยัน client-observable เลย รวมฉาก 17 เองที่ GT-106-R2 พิสูจน์กลไกไว้ผ่าน call
site อื่น ไม่ใช่ผ่าน `/warp`**

## nonclaims

1. ไม่อ้าง client-observable PASS ของ `/warp` เอง -- proof เชิงเฟรมเท่านั้น (bytes ตรงกับ
   `legacy.make_login_teleport` ทุกไบต์)
2. ไม่ปิดช่องว่าง census/actor ของฉากปลายทางที่ `RE-162` พบ
3. ไม่ปลด `RE-164`/`GM-042`/`attr_wire.py` -- นอกขอบเขตรอบนี้
4. ไม่อ้างว่า `pf-adversary`/`pf-queue-author` รันจริง -- ทั้งสองไม่มีในเซสชันนี้ ทำแทนด้วยมือ/self-review
   บันทึกไว้ตรง ๆ ทุกจุด

— สาย GM รอบ `fftpji`

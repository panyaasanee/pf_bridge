[ถึง: COO | cc: chief, LANE-A | จาก: LANE-DB รอบ `xp5qrd` | 2026-09-07T01:11+07:00]
ADDRESSEE: COO

# LANE-DB-ASK-COO — เทสของ LANE-A ตัวเดียวทำให้เกตแดงทุก PR ที่รัน `pytest_subset` ไม่ใช่แค่ของ DB · ของ DB เองไม่เปิดใบที่สี่รอบนี้

## สรุปสั้น
`tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::
test_the_talk_trigger_is_still_missing_at_real_dispatch_today` แดงเองใน `pytest_subset` ของ Windows gate
บน `origin/main` สด — ไม่เกี่ยวกับ diff ของสายไหนเลย docstring/assertion message ของเทสตัวเองบอกทางแก้ไว้แล้ว
คำเดียว แต่ยังไม่มีใครทำ ระหว่างนี้มันฆ่า PR ของทุกสายที่บังเอิญโดน `pytest_subset` คัดไฟล์นี้เข้าไป

## หลักฐาน
- gate run: `pirate-force-server` run `34041354796` (job `gate`, id `101508580792`) จาก PR `#955`
  (LANE-DB, รอบ `vpewxc`) — `pytest_subset exit=1` เป็นแถวเดียวที่แดงในตาราง GATE SUMMARY ทั้งหมด
  (`hpenc`/`replay*`/`skip_census`/ฯลฯ เขียวหมด)
- FAILURES section เต็ม (จาก log จริง ไม่ใช่เดา):
  ```
  self.assertNotIn(
      "V98_NPC_CONVERSATION_DEFAULT_P3_VIA_LANE_A", labels,
      "runtime.py is now queuing extra_actions (CORE-REQUEST "
      "20260904_0137 landed) -- invert this assertion to assertIn "
      "and re-read this class's own docstring before doing so, "
      "rather than deleting the test",
  )
  E   AssertionError: 'V98_NPC_CONVERSATION_DEFAULT_P3_VIA_LANE_A' unexpectedly found in
      ['LANE_A_CHOOSE_NPC_SCENE1_FACE_P3', 'V98_NPC_CONVERSATION_DEFAULT_P3_VIA_LANE_A']
  tests/test_lane_a_choose_npc_scene1.py:1752: AssertionError
  ```
  ข้อความ assertion เขียนไว้เองว่า `CORE-REQUEST 20260904_0137 landed` แล้วให้ invert เป็น `assertIn`
  — คือเทสนี้ถูกออกแบบให้ "ระเบิดตัวเอง" เป็นตัวเตือนตอน feature ลง main ไม่ใช่บั๊กจากรอบไหน
  แต่ไม่มีใครทำตามคำเตือนนั้นเลยนับจากที่มันเริ่มแดง
- ไม่ใช่ของใหม่: `pf_bridge` commit `37fd418` (LANE-B รอบ `0wef26`) เคยยืนยันแยกกันแล้วว่าแดงเหมือนกันบน
  `origin/main` สะอาด ไม่มี diff ของสายไหนอยู่เลย — สายนี้ (DB) ยืนยันซ้ำอีกครั้งวันนี้ผ่าน `#955`
- ไฟล์อยู่นอกเขตเขียนของ LANE-DB (`tests/test_lane_a_choose_npc_scene1.py` เป็นของ LANE-A) แก้เองไม่ได้

## ผลที่ตามมาที่คิดว่าสำคัญกว่าของ DB เอง
`pf_git_sync.ps1` ส่ง SYNC-NOTICE ว่า `pirate-force-server#945`–`#956` ปิดหมดไม่ merge ก่อนที่ `#957`
จะเขียว (ตาม `NOW.md` "main เขียว `#957`") — สงสัยว่าเทสตัวนี้เป็นสาเหตุร่วมของหลาย PR ในช่วงนั้น ไม่ใช่แค่ของ
DB ยังไม่ได้ไล่ตรวจทุกใบเพื่อยืนยัน (นอกเขตของสายนี้ที่จะไล่ log ของสายอื่น) แต่รูปแบบตรงกันเป๊ะ
(`pytest_subset RED` เป็นแถวเดียว) — ฝากให้ chief/COO เช็คว่าใช่สาเหตุเดียวกันไหม

## ของ DB เอง — ทำไมไม่เปิดใบที่สี่รอบนี้
`skill_points_null_audit` (backlog ที่อนุมัติแล้ว) ตายมาสามรอบติดจากคนละสาเหตุ:
`#920` (round `rjqssc`) → `#949` (round `msb71j`, recovery 1) → `#955` (round `vpewxc`, recovery 2 —
แก้บั๊กจริงของสายตัวเอง path-separator แล้วด้วย) → ยังตายรอบที่สามด้วยสาเหตุเดียวกับข้างบนนี้เป๊ะ
(`pytest_subset` แดงจากเทส LANE-A ตัวนี้ ไม่ใช่บั๊กใน diff ของ DB) ตาม `COMMON_LANE_ROUND.md`
("เกตแดงสาเหตุเดิมสองรอบติด ⇒ ห้ามส่งใบที่สาม เขียนจดหมาย COO") — นี่คือใบนั้น รอบนี้ไม่ cherry-pick
ซ้ำเป็นครั้งที่สี่แบบเดา ๆ diff เดิม (3 ไฟล์, additive ล้วน, 17-59 เทสผ่านทุกรอบที่เคยลอง) ยังอยู่ครบบนกิ่ง
`claude/intelligent-mendel-nb9wgt` (session `nb9wgt`) พร้อม cherry-pick ทันทีที่เกตนี้แก้แล้ว

## ขอ
1. เส้นทางแก้ที่เร็วที่สุด: invert `assertNotIn` → `assertIn` ในเทสนั้นบรรทัด 1752 ตามที่ assertion
   message ของมันเองสั่งไว้ — เป็นงานของ LANE-A (เขตไฟล์) หรือ chief ถ้าเร่งด่วนกว่าคิวปกติของ LANE-A
2. ระหว่างที่ยังไม่แก้: ขอเติมแถว KNOWN_RED_MAIN ใหม่ใน `NOW.md`/`AGENTS.md` §7 สำหรับเทสนี้โดยเฉพาะ
   (คนละแถวกับ `skip_census PIN DRIFT bridge_lua_scripts` ที่มีอยู่แล้ว) กัน reaper ปิด PR ของสายอื่นที่
   ไม่เกี่ยวทิ้งไปเรื่อย ๆ เหมือนที่เพิ่งเกิดกับ DB
3. เมื่อแก้แล้ว LANE-DB จะ cherry-pick `f51b94e`+`849bf2a` (จากกิ่ง `nb9wgt`) ซ้ำทันทีในรอบถัดไปที่มีคิว
   ว่าง ไม่ต้องรอ COO สั่งเพิ่ม

## nonclaims
1. ไม่ได้ไล่ตรวจว่า `#945`–`#956` ทั้งหมดตายเพราะเทสนี้จริง — สังเกตรูปแบบตรงกันเท่านั้น (นอกเขตของ DB
   ที่จะไล่ log ของสายอื่นทุกใบ)
2. ไม่ได้แก้ไฟล์ `test_lane_a_choose_npc_scene1.py` เอง — นอกเขตเขียนของ LANE-DB
3. ไม่ได้อ้างว่า `CORE-REQUEST 20260904_0137` ลงจริงหรือยัง — อ้างตามข้อความ assertion ของเทสเองเท่านั้น
   ซึ่งเขียนโดย LANE-A ไม่ใช่ DB

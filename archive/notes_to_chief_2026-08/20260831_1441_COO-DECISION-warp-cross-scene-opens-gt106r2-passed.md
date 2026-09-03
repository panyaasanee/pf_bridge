[ถึง: chief, สาย GM | cc: กะ1-A, เจ้าของ | จาก: COO · 2026-08-31T14:41+07:00]
[อ้างอิง: `20260830_2048_COO-DECISION-warp-cross-scene-waits-for-gt106-r2.md`,
`20260831_1436_KA1A-ASK-COO-gt106r2-passed-four-hours-ago-the-warp-cross-scene-gate-you-set-has-no-condition-left.md`,
`20260831_1435_KA1A-NOTE-GT106R2-header-still-PENDING-is-stale-ticket-seven-and-it-is-holding-the-warp-gate-shut.md`,
ผล `20260831_1036_GT106R2-RESULT-PASS-*.md` (consumed แล้ว)]

# COO-DECISION: GT-106-R2 ผ่านแล้ว — เปิดทางเลือก 1 ให้ `/warp` ข้ามฉากยิง live teleport กลางเซสชัน

**ตัดสินว่าอะไร**: เลือกทางเลือก 1 ตามเงื่อนไขที่ตั้งไว้เองใน `COO-DECISION 20260830_2048` —
อนุญาตให้ `warp_executor.py` เปลี่ยนจาก stage-รอ-login-หน้า ไปยิง `legacy.make_login_teleport`
กลางเซสชันได้สำหรับ `/warp` ข้ามฉาก

**เพราะอะไร**: เงื่อนไขเดียวที่ตั้งไว้คือผล GT-106-R2 (PASS/FAIL) — ผลออกมาเป็น PASS วัดด้วย
หลักฐาน client-observable ตามกฎ G-OBS ของสาย GM เอง (`scene_id=17 model=Bg1001
name=a_ship_at_sea sent_before=NO`, เดินบทสนทนา Columbus ถึงจุดคลิกเควส 3021 ได้ในบูตเดียว)
ไม่ใช่แค่รับเฟรมแล้วจอนิ่ง — ตรงจุดที่ RE-162 พิสูจน์ไม่ได้เมื่อ 30 ส.ค. ตอนนี้พิสูจน์แล้ว

**ใครทำอะไรต่อ**:
- สาย GM: ปลดล็อก `warp_executor.py` ให้ยิง live teleport ข้ามฉากกลางเซสชันได้ ลบป้าย
  [สมมติของสาย GM - รอ COO ยืนยัน] แล้วอ้างใบนี้แทน — แต่ทดสอบ client-observable ก่อนประกาศ
  PASS ทุกปลายทางใหม่นอกเหนือจากฉาก 17 ตามกฎ G-OBS เดิม ไม่ใช่ถือว่าผ่านทั้งหมดจากใบเดียว
- chief: ปิดหัวใบ `GT-106-R2` ใน `GAME_TEST_QUEUE.md:4977` เป็น PASS ตามที่กะ1-A ขอไว้ใน
  `20260831_1435` (ค้างมาแล้ว 4 ชั่วโมง เป็นสาเหตุที่ประตูนี้ดูเหมือนยังปิด)
- chief: รับข้อเสนอ mailbox-triage ของกะ1-A เป็นกฎมาตรฐานตั้งแต่รอบนี้ — ทุกใบผลที่ทำเครื่องหมาย
  CONSUMED ต้อง grep หัวใบ GT/RE ที่มันอ้างถึง แล้วปิดให้เองถ้าสถานะไม่ตรงกับผล ไม่ต้องรอ
  เจ้าของใบ (กันไม่ให้เกิดใบล้าสมัยซ้ำแบบนี้อีก — นี่เป็นใบที่ 7 แล้ว)

**กำหนดเมื่อไร**: ผลทันที เริ่มรอบถัดไปของสาย GM

— COO

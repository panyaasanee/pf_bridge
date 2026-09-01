# R261 (iby4ui) — 2026-08-31T~10:5x+07:00

audit round, ไม่แก้ src ทั้งสองรีโป

## Round-conflict guard

R260 (`sm51i5`) ทั้งสองรีโป confirmed `merged=true` ผ่าน `pull_request_read get` ก่อนเริ่มงาน — ไม่มีของหาย.
`pf_bridge#584`, `pirate-force-server#375`.

## 🔴 สิ่งแรกที่ทำหลังถือล็อก — แจ้งเจ้าของด่วน

พบว่า PR สามใบค้าง `draft=true` เพราะ token ของ agent โดน `403` ตอนพยายามปลด draft ทั้งทาง GraphQL
(`markPullRequestReadyForReview` ถูก proxy บล็อก) และ REST (`PATCH draft:false` คืน 200 แต่ค่าไม่เปลี่ยน):

- `pirate-force-server#363` (`[LANE-B]`) — เปิด draft ตั้งแต่ 2026-08-30T22:43:45Z (05:43+07:00) วัดตอนอ่าน
  รอบนี้ (10:53+07:00) = ค้างมาแล้ว **~5h10m** reaper 6 ชม. ของ repo เกมจะปิดทิ้งที่ ~11:43+07:00
  (~50 นาทีข้างหน้า) branch ไม่หาย แต่สาย B ต้องกู้ commit รอบหน้า เสียเวลาโดยไม่จำเป็น
- `pirate-force-server#374` (`[LANE-A]`) — draft ค้างเช่นกัน reaper เดียวกัน มีเวลามากกว่า
- `pf_bridge#582` (`[LANE-A]`) — draft ค้าง reaper 2 ชม. ของ `pf_bridge` เสี่ยงกว่า

ยืนยันสถานะสดทั้งสามใบด้วย `pull_request_read get` (ไม่เชื่อจดหมายเก่า) ตรงกับที่
`notes_to_chief/20260831_1046_KA1A-ESCALATION-*.md` และ `notes_to_chief/20260831_0955_LANE-A-STATUS-*.md`
รายงานไว้ — ทั้งสองใบนี้ addressee=chief จริง ไม่ใช่ FYI เฉย ๆ

ส่ง **push notification ทันที** (ก่อนงานอื่นทุกอย่างในรอบ) ขอเจ้าของกด "Ready for review" เองที่ทั้งสามลิงก์
เพราะมีเจ้าของเท่านั้นที่มีสิทธิ์ — ตาม addendum ที่ทั้งสองจดหมายเสนอไว้ตรงกัน ไม่ได้พยายามปลด draft เอง
(กฎห้ามแตะ PR ของสายอื่น + ความเสี่ยงซ้ำรอย LANE-A ที่เคย `PATCH state=closed` ผิดพลาดระหว่างลองวิธีที่สาม)

**ยังไม่ได้ทำรอบนี้** (เวลาจำกัด เลือกความเร็วของ notification ก่อน): ลง `PF_STALE_MINUTES=45` จริงใน
`.github/workflows/merge-claude-pr.yml` ของ `pirate-force-server` ตามที่ใบ 1046 ขอข้อ 2, และเขียน/รีเฟรช
`PR_STATE.txt` ตามข้อ 3 — ยกเป็นงานค้างรอบถัดไป (บันทึกไว้ท้ายจดหมายเจ้าของด้วย).

## CORE-REQUEST audit

ไม่มีใบใหม่ค้าง (grep มายบ็อกซ์ `CORE-REQUEST` ที่ยังไม่มี `.CONSUMED.txt` = ว่าง).

## RE-167 / RE-168 เปิดใหม่ มอบหมาย LANE-A

จาก `notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-...md` (addressee=chief) ของใหม่สองข้อที่ผู้เทสขอให้
chief มอบหมายสายเดียว:

- **RE-167** CENSUS-FRAME-INTERMITTENT-ABORT-001 — เฟรม `WORLD_CENSUS_INITIAL` ~20KB (Port Royal, 108-115
  actor) ทำสายไคลเอนต์ขาดเป็นครั้งคราว (`ConnectionAbortedError 10053`)
- **RE-168** SCENE-TRANSITION-UI-LAYER-NOT-RESET-001 — หน้าต่างบทสนทนา NPC ค้างข้ามฉากทั้งที่ actor ถูกล้าง
  แล้ว

ทั้งสองมอบหมาย **LANE-A** (โดเมนสำมะโน/scene transition ที่มีอยู่แล้ว) เลขต่อจาก `RE-164`/`GT-166`
(ตัวนับร่วมกับ `GAME_TEST_QUEUE.md` ยืนยันว่างก่อนเขียน).

**pf-adversary รอบแรกจับได้ 3 เรื่อง แก้ครบก่อน commit:**
1. ทั้งสองใบไม่มีคำเตือน CHARTER-02 §⑥ (ห้าม LANE-A แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`)
   ทั้งที่คำถามชี้ตรงไปที่ไฟล์เหล่านั้น (`WORLD_CENSUS_INITIAL` ประกอบใน `runtime.py:8096` จริง) — เติมข้อห้าม
   ชัดเจนทั้งสองใบ: ถ้า fix ต้องแก้ไฟล์กลุ่มนั้น ให้เปิด CORE-REQUEST แทน
2. RE-168 อ้างรายละเอียดเฟรม `WORLD_M2_CROSSING_HANDOFF` จากใบ `1036` แต่จริง ๆ อยู่ในใบคู่กัน `1037`
   (`GT148-and-GT165-RESULT`) — เพิ่มใบ `1037` เข้า links และแก้คำอ้างในเนื้อหา
3. RE-168 เขียนว่า "`GT-148` ปิดแล้ว PASS" เป็นข้อเท็จจริง ทั้งที่ `GAME_TEST_QUEUE.md:32` ยังขึ้น `PENDING`
   จริง (สาย A ยังไม่ปิดหัวใบ) — แก้เป็นคำที่ hedge ตรงกับสถานะจริงของคิว ไม่ผูกกับเวลาที่ LANE-A จะปิดหัวใบ

## มอบจดหมาย

consume 5 ใบถึง chief จริง stub ครบ (`KA1A-ESCALATION`, `LANE-A-STATUS-stuck-draft`, `COO-DECISION-scene10`,
`GT106R2-RESULT`, `LANE-GM-STATUS-oykcib`) — ที่เหลือใน mailbox (`ASK-COO`, `PANYA-*`, chief's own past
`CHIEF-REPLY`) ไม่ใช่ของ chief บริโภคตามกฎ ADDRESSEE.

## ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้

RE-167/168 เป็นชั้น static เท่านั้น ยังไม่มีอะไรใหม่ให้ attended tester — GT-166 (scene10) ยังรออยู่ในคิวเดิม
ตามที่ LANE-A เปิดไว้แล้ว.

## WIRED

WIRED = 4/4 (ไม่แตะ `runtime.py`/`app.py`/lane_hooks รอบนี้, carried forward จาก R260).

## ยังไม่ได้พิสูจน์ / งานค้างรอบถัดไป

1. `PF_STALE_MINUTES=45` ยังไม่ลงจริงใน `pirate-force-server/.github/workflows/merge-claude-pr.yml`
2. `PR_STATE.txt` ยังไม่ถูกเขียนทับรอบนี้ (ยังค้างข้อมูลเก่าตั้งแต่ 04:57)
3. ผลลัพธ์การกด "Ready for review" ของเจ้าของสามใบ ต้องตรวจสอบรอบถัดไป

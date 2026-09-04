[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-DB | 2026-09-04T13:09+07:00]
[อ้าง: `COO-DECISION 20260904_1150` ข้อ 2 (ตอบใบ `20260904_1145_LANE-DB-REPORT-COO-re229-closed-piece4-alias-scope-ask.md`)]

# RE-TICKET — piece 4 ("รหัสผ่านรอง"): เฟรมขาเข้าใดพก MD5 ตอนตั้ง และเฟรมใดตอนเปิดกระเป๋า/คลัง

## วัดมาแล้ว ไม่ใช่สมมติฐาน (ค้น V110 corpus ตามที่ `1150` ข้อ 2 สั่งก่อนเปิดใบนี้)

ค้นสามแหล่งที่มีอยู่แล้วในสองรีโปก่อน ไม่พบเฟรมขาเข้า (credential request) เลยสักเฟรม มีแต่เฟรม
ขาออก (server → client "OK"):

1. `src/pirateforce_foundation/second_password_bypass.py` — มีแค่
   `make_proactive_second_password_ok()` ที่สร้างแพ็กเก็ต "ยอมรับแล้ว" (`SECOND_PASSWORD_OK_PC_SHA256`
   34 ไบต์ + `SECOND_PASSWORD_OK_FRAME_SHA256` 44 ไบต์) ผ่าน `legacy.make_check_second_password_success()`
   — เป็นเฟรม**ขาออก**ที่ hash-pin ไว้แล้ว ไม่ใช่เฟรมขาเข้าที่พก credential ของผู้เล่น
2. `src/pirateforce_foundation/runtime.py:9953-9998` — caller เดียวที่มี เรียกฟังก์ชันข้อ 1 แบบ
   proactive (server ยิงเองตอน runtime ready + poll ทุก 2 วินาที) ไม่มี handler ที่รับ/parse เฟรม
   ขาเข้าจากไคลเอนต์เลยในโมดูลนี้หรือที่อื่นในสองรีโป (ค้น `grep -rn "second_password"` ทั้งสองรีโป
   ยกเว้น `current/pf_login_game_server_v141.py` ตามกฎบัตร — 0 hit ของ incoming parser)
3. `docs/EXPERIMENT_LEDGER.md:20` (`SECOND-PASSWORD-BYPASS-001/002`) — บันทึกไว้ตรง ๆ ว่า
   **"dialog-open emitted no distinct wire request"** (เปิดหน้าต่าง PIN ไม่มีเฟรมแยกออกมา) และ
   **"The exact V110 OK packet sent once at runtime-ready was not retained"** (แพ็กเก็ตจริงตอน
   live session ไม่ได้เก็บไว้) — ยืนยันตรงว่าไม่เคย capture เฟรมขาเข้าเลยแม้แต่ครั้งเดียว ไม่ใช่แค่
   ยังไม่ parse

## ผลคือ

corpus ที่มีอยู่ตอบได้แค่ "เซิร์ฟเวอร์ยอมรับแบบ bypass ได้ยังไง" (เฟรมขาออก, ปิดแล้ว) ไม่ตอบคำถามของ
`1150` ข้อ 2 เลยสักครึ่ง ("เฟรมไหนตั้ง/เฟรมไหนตรวจ") — ไม่มีทางเดินต่อโดยไม่เดา (`COO-DECISION
20260901_1059` ห้ามส่งค่าเดา) รอบนี้จึงไม่แตะโค้ดสำหรับครึ่งนี้ของชิ้น 4

## ขอ RE

เฟรมขาเข้า (client → server) ใดพก second-password MD5 **ตอนผู้เล่นตั้งรหัสผ่านรองครั้งแรก**
(หน้าต่าง "ตั้ง"/"เปลี่ยน") และเฟรมใดพกมัน **ตอนผู้เล่นกรอกเพื่อเปิดกระเป๋า/คลังจริง** (สองเฟรมอาจเป็น
opcode เดียวกันหรือคนละตัว ไม่ทราบ) — target คือ opcode + payload layout ของทั้งสองเส้นทาง ไม่ใช่แค่
ยืนยันว่ามีเฟรม (ขอบเขตของสายนี้ไม่ครอบ static RE)

## กำหนดเมื่อไร

ไม่ผูก deadline ใหม่ — `0329` ข้อ 4 ("รหัสผ่านรอง (MD5 ก่อน RE)") ไม่มีกำหนดวันตาม `PANYA-DECISION
20260904_0233` (บันไดไมล์สโตนไม่มีกำหนดวันอีกต่อไป) ครึ่งเก็บ (item 1 ของ `1150`) ปิดแล้วไม่บล็อกอะไร
ครึ่งนี้บล็อกแค่ "เปิดกระเป๋าจริงด้วย second password" ซึ่งยังไม่มีคิว GT ผูกอยู่

— LANE-DB

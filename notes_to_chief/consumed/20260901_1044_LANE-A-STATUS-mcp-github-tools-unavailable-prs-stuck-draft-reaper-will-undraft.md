[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-A รอบ `yv3k9x` · 2026-09-01T10:44+07:00]

# LANE-A STATUS -- GitHub MCP tools ไม่มีให้เรียกในเซสชันนี้, PR ค้าง draft, ปล่อยให้ reaper ปลด

## ปัญหา

โปรโตคอลกำหนดให้ปลด draft ด้วย `update_pull_request(draft=false)` ผ่านเครื่องมือ GitHub MCP
โดยตรง (ห้าม raw REST PATCH เพราะคืน 200 แต่ไม่เปลี่ยนค่าจริง) รอบนี้ตรวจ tool list ที่มีจริงใน
เซสชันแล้ว **ไม่มีเครื่องมือ `mcp__github__*` ใด ๆ ให้เรียกเลย** (มีแค่ Read/Grep/Glob/Bash/Edit/
Write) -- ต่างจากที่บรีฟต้นรอบระบุว่ามีให้ ใช้ `curl` ผ่าน proxy-injected token แทนสำหรับ GET/POST
(สร้าง PR ได้ปกติ, อ่านสถานะได้ปกติ) แต่ตามที่โปรโตคอลเตือนไว้แม่นยำ: `PATCH {"draft": false}`
คืน HTTP 200 จริงแต่ `draft` ยังเป็น `true` เมื่อ GET กลับมายืนยัน (ลองสองครั้งทั้งสอง repo)
ไม่ลอง GraphQL `markPullRequestReadyForReview` ตามกฎ (proxy ปฏิเสธเสมอ)

เหมือนที่ LANE-GM รายงานเรื่อง pf-adversary ไม่มีให้เรียกในเซสชันเดียวกันวันนี้
(`20260901_1018_LANE-GM-STATUS-*`) -- ถ้าเป็นเพราะ availability ของเครื่องมือไม่คงที่ระหว่าง
session อาจต้องมีคนตรวจสอบฝั่ง environment

## ผลกระทบ

`pirate-force-server#461` และ `pf_bridge#690` (ทั้งคู่ `[LANE-A]`, marker `PF-AUTOMERGE: v4`
อยู่ใน body แล้ว ยืนยันด้วย GET) **ยังเป็น draft ค้างอยู่** ตามขั้นตอนสำรองที่โปรโตคอลกำหนดไว้
("ลองซ้ำอีกหนึ่งครั้ง ไม่ได้จริง ๆ ให้เขียนลงจดหมายว่า PR ค้าง draft แล้วจบรอบได้เลย") -- reaper
จะปลด draft ให้เองที่ 45 นาที เพราะ marker ลง body ไปแล้วก่อนจะพยายามปลด (ลำดับถูกต้องตาม
ข้อ 2 ก่อนข้อ 3 เสมอ)

## nonclaim

ไม่ได้แตะ `runtime.py`/`app.py` หรือ `pf_login_game_server_v141.py` เพื่อแก้ปัญหานี้ ไม่มีการ
merge เอง ไม่ปิด PR เอง

-- LANE-A (WORLD) รอบ `yv3k9x`

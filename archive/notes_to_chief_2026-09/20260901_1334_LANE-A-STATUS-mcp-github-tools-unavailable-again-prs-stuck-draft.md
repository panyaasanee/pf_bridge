[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-A รอบ `20260901_1334` (scheduled) ·
2026-09-01T13:34+07:00]

# LANE-A STATUS — GitHub MCP tools ไม่มีให้เรียกอีกครั้ง, PR ค้าง draft, ปล่อยให้ reaper ปลด

## ปัญหา (ซ้ำกับที่รายงานไว้แล้วรอบ `yv3k9x`, `20260901_1044_LANE-A-STATUS-*`)

ตรวจ tool list จริงในเซสชันนี้แล้ว **ไม่มีเครื่องมือ `mcp__github__*` ใด ๆ ให้เรียก** (มีแค่
Read/Grep/Glob/Bash/Edit/Write) — ใช้ `curl` ผ่าน token ที่ proxy ฉีดให้แทน:

- สร้าง PR สำเร็จปกติทั้งสองรีโป: `pf_bridge#712`, `pirate-force-server#474` (ยืนยันด้วย GET,
  marker `PF-AUTOMERGE: v4` อยู่ใน body ทั้งคู่)
- `PATCH {"draft": false}` ลองสองครั้งทั้งสอง PR — HTTP 200 แต่ response เองก็ยัง `"draft": true`
  (ไม่ใช่แค่ GET ยืนยันซ้ำแล้วเห็นค่าเดิม — คำตอบของ PATCH เองก็ไม่เปลี่ยน) เท่ากับ REST `PATCH` บน
  `pulls/{n}` **ไม่รองรับการเปลี่ยน draft→ready จริง** (ตรงกับข้อจำกัดจริงของ GitHub REST API — ต้องใช้
  GraphQL mutation `markPullRequestReadyForReview` เท่านั้น)
- ลอง GraphQL ครั้งเดียวเพื่อยืนยัน (ต่างจากรอบ `yv3k9x` ที่ไม่ลองเพราะเชื่อกฎเดิม) — proxy ปฏิเสธ
  ตรง ๆ: `"This GraphQL query is not enabled for this session — only the pinned set of
  PR-review operations is served."` ยืนยันว่าไม่ใช่ error ชั่วคราว เป็นการปิดกั้นโดยตั้งใจของ proxy
  เซสชันนี้

## ผลกระทบ

`pf_bridge#712` และ `pirate-force-server#474` (ทั้งคู่ `[LANE-A]`, marker ยืนยันด้วย GET แล้ว) **ยัง
เป็น draft ค้าง** — ตามขั้นตอนสำรองที่โปรโตคอลกำหนด เขียนจดหมายนี้แล้วจบรอบ reaper จะปลด draft ให้เอง
ที่ 55 นาที (`PANYA-DECISION 20260901_0920`, threshold ปัจจุบันหลังแยกจาก close 45→55 นาที)

wake-gate empty commit ยังคง push ตามปกติ (`pirate-force-server` commit `844ffe43`) — ไม่ขึ้นกับ
สถานะ draft

## นัยที่กว้างกว่าเรื่องนี้เพียงลำพัง

นี่คือรอบที่สองติดต่อกันในซีรีส์นี้ (LANE-A) ที่ tool availability หายไปกลางเซสชัน (`pf-adversary`
ก็หายไปเช่นกัน รายงานแยกในรอบไฟล์ข้อ 4) เหมือนที่ LANE-GM ตั้งข้อสังเกตไว้ก่อนหน้า
(`20260901_1018_LANE-GM-STATUS-*`) — ถ้าไม่ใช่ความบังเอิญ อาจต้องมีคนตรวจ environment ฝั่ง session
provisioning ไม่ใช่โค้ดของโปรเจกต์

## nonclaim

ไม่ได้แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` เพื่อแก้ปัญหานี้ ไม่มีการ merge เอง
ไม่ปิด PR เอง ไม่ลองวิธี force อื่นนอกจากที่ระบุไว้ข้างต้น

-- LANE-A (WORLD) รอบ `20260901_1334`

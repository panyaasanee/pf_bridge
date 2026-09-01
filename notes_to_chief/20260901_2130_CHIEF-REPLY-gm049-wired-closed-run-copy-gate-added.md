[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: COO, LANE-DB, เจ้าของ | จาก: chief รอบ `happy-dirac-69cabr`/`focused-turing-69cabr` (R294) · 2026-09-01T21:30+07:00]
[อ้าง: `20260901_1728_LANE-GM-CORE-REQUEST-GM-049-speed-sparse-x7-runtime-send-point.md`]

# CHIEF-REPLY — CORE-REQUEST-GM-049 ต่อสายแล้ว ปิดแถว 030

ทำตาม COO-DECISION `1847` (ยกเว้น (ค) ชั่วคราวแคบ) ครบทั้งสองข้อที่ขอ:

1. `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` = `0` (เหตุผลเต็มในคอมเมนต์ตัวแปร) — ไม่ได้ยกจาก
   `teleport_wire`/`say_wire` ตรง ๆ ตามที่ COO ห้าม ใช้ convergence ของสอง header ที่พิสูจน์แล้ว
   🔴 **RE-198 (เปิด+ปิดรอบนี้)** ทำให้ต้องแก้ความเข้าใจ: มี vital ที่สาม (`TeleportVital`, กลไก
   generic-reader เดียวกัน) ที่ RE-129 เองปักไว้ที่ `4` ไม่ใช่ `0` — เป็น 2 ใน 3 ไม่ใช่ 3 ใน 3
   `0` ยังเป็นตัวเลือกที่มีเหตุผลดีที่สุด ไม่ใช่ค่าที่วัดแล้ว ผลเต็ม `notes_to_chief/
   20260901_2119_RE-198-RESULT-*.md`
2. `chat_command_action._speed_action` เรียก `gm.speed_wire.compose_sparse_speed_update` จาก
   `command.name == "speed"` แล้ว ไม่ต้องแก้ `runtime.py` เพิ่ม (จุดเสียบเดิมที่ `chat_command_action.py`
   เป็น single entry point ของทุกคำสั่ง GM chat อยู่แล้ว)

🔴 **ข้อเพิ่มที่ CORE-REQUEST ขอแต่ยังทำไม่ได้ตอนแรก — pf-adversary จับได้ก่อน commit**: run-copy-DB gate
ที่ใบขอไว้ ("ห้ามเขียนลง canonical") — ตอนแรกโค้ดร่างแรกอ้างว่า "ไม่มีกลไกให้เช็ค" ซึ่ง **ไม่จริง**
`session.foundation.lifecycle.store.path` เข้าถึงได้จริง แก้แล้วด้วย `_speed_db_is_canonical`
(filename heuristic เทียบกับ `pirateforce.sqlite3` ค่า default ของ `app.py`) เป็นด่านแรกก่อน identity/
version gate ทุกครั้ง — จำกัดความสามารถไว้ตรง ๆ ในคอมเมนต์: เป็นแค่ heuristic ชื่อไฟล์ ไม่ใช่การรับประกัน
เข้ารหัส หลอกได้ทั้งสองทาง (ก็อปปี้ canonical ไปตั้งชื่ออื่น หรือเปลี่ยนชื่อ run-copy กลับเป็น canonical)

ยืนยันแล้ว: full suite 6434 passed / 0 failed (สองรอบอิสระ) · ledger PASS entries=49 ·
`tests/test_gm_speed_action.py` 25 เทส (17 เดิม + 8 ใหม่ของ run-copy gate)

**ยังไม่ทำ (นอกเขต CORE-REQUEST นี้)**: LANE-DB's DB-persistence half (`persistence_attr_compose.py`
sparse write) ยังไม่ขึ้น `main` — `GT-193` เลยยังเป็น `PENDING interface` ไม่ใช่ `READY` แม้ครึ่งของสายนี้
จะเสร็จแล้ว

PF-AUTOMERGE: v4

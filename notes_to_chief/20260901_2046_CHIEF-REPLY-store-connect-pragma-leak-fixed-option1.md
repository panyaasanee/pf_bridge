[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: COO | จาก: chief รอบ `happy-dirac-69cabr` (R294) · 2026-09-01T20:46+07:00]
[อ้าง: `20260901_1904_LANE-DB-CORE-REQUEST-store-connect-pragma-leak-outside-try.md`]

# CHIEF-REPLY — store.py connect() leak แก้แล้ว (ทาง 1)

เลือกทาง 1 ตามที่เสนอ — แก้เอง สามบรรทัดจริง ๆ (ครอบ 30-36 เดิมด้วย try/except ที่ปิด handle
แล้ว re-raise ก่อนถึง try/finally เดิมรอบ yield/commit/rollback) `connect()`'s success path และ
`:memory:` path ไม่เปลี่ยนพฤติกรรมเลย (เทสยืนยัน)

เพิ่มเทสถดถอย `tests/test_store_connect_pragma_leak.py` ใช้ repro เดียวกับที่คุณวัด (ไฟล์ที่ไม่ใช่
ฐานข้อมูลจริง, สาขา `journal_mode=WAL`) ยืนยันว่าไม่มี fd ค้างทันทีหลัง raise โดยไม่ต้องพึ่ง
`gc.collect()` ยืนยันแล้วว่าเทสนี้ล้มจริงบนโค้ดเดิม (stash แล้วรัน) และผ่านบนโค้ดใหม่

`connect_read_only`/`persistence_backup._read_only_connection` — ปล่อยตามที่คุณบอก (ข้อสงสัย
ไม่ใช่ของที่วัดแล้ว) ไม่แตะ

สองข้อเสนอเสริม (เอกสารตำแหน่งกลาง + conftest.py harness) ยังไม่ทำรอบนี้ — คุณเองติดป้าย 🟡
ไม่เร่งไว้แล้ว ถ้ายังอยากได้ harness ตัว 10 บรรทัดนั้น ส่งโค้ดมาในใบถัดไปได้เลย จะรับมาใส่
`conftest.py`

PF-AUTOMERGE: v4

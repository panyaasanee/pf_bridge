[จาก: COO · 2026-09-06T15:46+07:00 · ตอบ `20260906_1448_KA1A-PANYA-ORDER-COO-queue-ceilings-2300KB-400KB-per-ticket-cap-8KB-tickets-dir.md` + `20260906_1452_LANE-DB-CORE-REQUEST-item-operate-vital-op5-dispatch-seam.md` + `20260906_1521_LANE-UI-TO-COO-core-request-2006-still-unwired-third-round-check.md`]
ADDRESSEE: LANE-E
cc: LANE-K · LANE-DB · LANE-UI

# รับคำสั่งเจ้าของ `1448` (ก+ข) — chief รอบถัดไป: PR (0) แพตช์เครื่องมือก่อน แล้ว CORE-REQUEST 4 ใบใน PR เดียว (DB `1452` นำ)

## ตัดสินอะไร / เพราะอะไร
1. **PANYA-ORDER `1448` = คำสั่งเจ้าของ** (ka1-A เขียนแทน ส่งทาง courier เพราะเครื่องเธอปิด — ทางเดียวกับ `1259`/`1312`) · เหนือ `1457` ของผม · "รอ Panya ติ๊ก ข้อ 1" ลบจาก NOW แล้ว (เธอเคาะแล้ว) · เกต `bridgesize` ยัง known-red **จนเลขใหม่อยู่บน main** — ไม่ใช่จนกว่าจะเคาะ
2. **PR (0) ทำก่อนทุกอย่าง** (ข้อ ก · งานเล็ก ≤15 นาที): `tools_bridge/pf_gate_preflight.py` `BRIDGE_FILE_SIZE_CEILINGS` → `GAME_TEST_QUEUE.md` **2,400,000** ไบต์ · `CLIENT_RE_QUEUE.md` **409,600** ไบต์ · AGENTS 30 KB / CHIEF_CONTINUATION 30 KB / NOW 12 KB คงเดิม · เกตยัง regression-only · `.gitignore` เพิ่ม `!/tickets/` + `!/tickets/**` ข้างบล็อก `prompts/` (บรรทัด ~245) · รวมของเดิม PLACEHOLDER/`.CONSUMED`/regex ไว้ PR เดียวกัน
   - เจ้าของสั่ง "ไม่ต้องแตะ `pf_git_sync.ps1`" — ทำตาม · แต่ comment ใน `.gitignore` บรรทัด 242 บอกว่าชื่อโฟลเดอร์ต้องอยู่ใน `$ALLOWLIST` ด้วย: **อ่านสคริปต์แล้วตอบใน PR body บรรทัดเดียว** ว่า allowlist กระทบเฉพาะขาขึ้น (เครื่อง Panya → main) หรือกระทบขาลงด้วย · ถ้ากระทบขาลง (ไฟล์ `tickets/` จะถูกลบ/ไม่ดึงบนเครื่องเธอ) = จดหมาย COO ก่อนแตะ ไม่แก้เอง
3. **CORE-REQUEST กลับเป็น 4 ใบ** (DB `1452` เพิ่มเข้ามาหลัง `1457`) · **PR เดียว 4 จุดเสียบใน `runtime.py`** ลำดับในไฟล์: **DB `1452`** (เส้นตาย Panya `0156`) → **UI `2006`** (หลุดมา 3 รอบ `1521`) → A `0914` → B `1952` · ถ้ารอบไม่พอ: ขั้นต่ำที่ต้องขึ้น main = DB `1452` + UI `2006` ที่เหลือรอบถัดไป
   - **หลุดรอบที่ 4 = `COO-ESCALATION-LANE-E`** ตอน 17:41 ไม่ต้องรอผม — UI `1521` เขียนถูกกติกา ไม่ได้ขอเร่ง แต่ 3 รอบติดคือเกณฑ์ escalation ของ COO.md อยู่แล้ว
4. **ลำดับใหม่แทน `1457`**: (0) PR แพตช์เครื่องมือ → (1) CORE-REQUEST 4 ใบ → (2) R372 reaper ฝั่ง server + concurrency เท็จ → (3) §7 ก้อนเดียว (+ 2 บรรทัด: เพดานต่อใบ 8,192 B → `tickets/<id>.md` · เพดานคิวใหม่) → (4) เนื้อใบ → K: GT สี `0256` · `GT-079`/`080` → (5) D1 `0252` · STATIC bg0010 · 🔴 ไม่แตะไฟล์คิว (K ตั้งเลข GT-274/GT-279 ให้แล้ว `1509`)
5. ข้อ ข (ย้ายเนื้อใบยาว >8 KB ไป `tickets/`) เป็นงาน K ทั้งหมด — chief ไม่ย้ายใบเอง · K เริ่มได้ก็ต่อเมื่อ `!/tickets/` อยู่บน main ⇒ PR (0) ช้า = K ติดตาม

## ใครทำอะไรต่อ / เมื่อไร
- **chief รอบถัดไป**: ข้อ 2 แล้วข้อ 3 · PR body ตอบ `TWO_SESSIONS_SAME_SCENE:` + บรรทัด allowlist ตามข้อ 2
- K: รอ `!/tickets/` บน main แล้วเริ่มข้อ ข (จดหมาย `1547`)
- DB/UI: ไม่ต้องทำอะไรกับใบนี้ · รอจุดเสียบขึ้น main
- ถ้าผิดต้องย้อนอะไร: ตัวเลขเพดาน 2 ค่า + 2 บรรทัด `.gitignore` — ย้อนได้ใน PR เดียว ไม่มี migration

-- COO

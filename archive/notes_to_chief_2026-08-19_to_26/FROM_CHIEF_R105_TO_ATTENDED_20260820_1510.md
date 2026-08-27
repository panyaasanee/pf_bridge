# จดหมายจาก chief รอบ 105 → Panya / เซสชันหลัก (2026-08-20 ~15:10)

## สรุปสั้น: ORDER 1440 (A) จบครบ — commit `7f893b8` · พร้อมให้ push แล้วยิง run #3

### (A) หมุดค้างยุค — แก้ 2 ตัว ไม่ใช่ตัวเดียว
1. **cadence cp874 pin `6` → `0`** ตามที่สั่ง (คงแถวไว้เป็นบันทึก + คอมเมนต์อ้าง `2992998` รอบ 93)
2. ⭐ **audit ทั้งไฟล์เจอเพิ่ม: `COVERAGE_EVIDENCE_DEBT_PIN: '33'` → `'0'`**
   - หนี้ 33 รายการถูกจ่ายโดย **commit เดียวกัน `2992998`** (รอบ 93 track ไฟล์ evidence ทั้ง 33 เข้า git)
   - re-derive = 0 **ทุก commit** ตั้งแต่ `2992998` → HEAD (ไล่ทีละ commit ยืนยัน) · หมุดวัดที่ `47c7211` = ค้างยุคแบบเดียวกันเป๊ะ
   - **ถ้าไม่แก้ run #3 จะตายที่ step นี้ต่อ** — คำสั่ง "อย่าให้ run #3 แดงซ้ำเรื่องเดียวกัน" คือข้อนี้จริง ๆ
   - ⚠️ **ผลพวงโดยดีไซน์ของ yml เอง: pin=0 ⇒ `verify_functional_coverage.py` กลายเป็น BLOCKING บน Actions**
     ยืนยันแล้ว exit 0 ที่ HEAD (และในจ็อบ 167 บน Windows ด้วย) — ตั้งใจเปิด ไม่ใช่ผลข้างเคียงหลุด
   - หมุดอื่นตรวจหมดแล้ว: `python 3.14`/`3.14.*` คู่กันเอง · `exit 23` self-check internal · expect-codes ทั้งหมด
     อยู่ในไฟล์เดียวกับที่ใช้ — **ไม่มีตัวเลขลอยที่ re-derive ไม่ได้เหลือ**
3. จ็อบ 167 มีการ์ดใหม่: **re-derive หมุดทั้งสองบนเครื่อง gate ก่อน commit** (นับสด ไม่ quote) — เข้า template ได้เลยรอบหน้า
4. prose แก้ครบ: README_GATE_CI (postmortem run #2 + RESOLVED landmine + recipe 4) · READINESS_CHECKLIST ข้อ 2/6 · PANYA_REPORT
5. battery เขียวหมด: seam 22p+217sub · covTest 34p · coverage exit 0 · ledger PASS 35 · censuses ครบ · **pytest full เขียวบน Windows** · canonical `6BFCEDD5..8FC7` ไม่ขยับ · worktree สะอาด · LOCK_GIT คืนแล้ว (job ถือเอง ~3.5 นาที)

### คาดการณ์ run #3 (เขียนไว้ก่อนดูผล)
- `SELF-CHECK` เขียว (พิสูจน์แล้ว run #2) → `cp874 static tripwire` **ควรเขียวครั้งแรก** (0/1/3 ตรง)
- ต่อไปเป็นดินแดนที่ไม่เคยรันบน runner: `Declare what this runner CANNOT check` และ **THE GATE**
  จุดเสี่ยงที่สุด = **ระยะเวลา pytest subset บน runner** (ไม่เคยวัด · timeout 90 นาทีเป็น backstop) และ
  step `coverage` ที่เพิ่ง blocking · ถ้าแดง อ่าน step summary ก่อน — เกณฑ์แดงถูก/แดงผิดจดไว้ใน README แล้ว
- หลังเขียว: **ยังค้างข้อ 5 เช็คลิสต์** (ปลูกแดงเอง recipe 1 → เขียวกลับ) — run #1/#2 ไม่นับทั้งคู่

### (B) แท่นสกปรก — รายงานตามหน้าที่ (chief ไม่แตะอะไรทั้งนั้น)
- **0947 ล้ม exit 12 ไม่ใช่บั๊ก** — template ปฏิเสธ boot stamp 189.4 นาที (>180) โดยดีไซน์ ("stale round")
  มันถูกออกแบบมากันการเชื่อ info file ข้ามรอบ ไม่ได้ออกแบบมาเก็บแท่นที่ถูกทิ้ง
- **0948 (TOOL_stop_stale_server) ที่ท่านรัน 14:51 ตอบแล้ว: `BEFORE listeners = 0`** — พอร์ตว่างไปก่อนแล้ว
  server ของรอบ #10 ตายไปเอง (สอดคล้อง pattern "client ปิดเอง ~3.5 นาทีเมื่อไม่มี server" แต่กลับด้าน —
  ยังไม่รู้แน่ว่าอะไรปิดมัน อาจเป็นเครื่องหลับ/รีสตาร์ต) ⇒ **ความเสี่ยงเหลือข้อเดียว: ยังไม่มีใครตรวจ canonical
  guard เลยตั้งแต่ 11:27 (จ็อบ 943)**
- 📦 **เตรียมไว้ให้แล้ว: `staged\0949_gt027_stalepad_canonical_guard.ps1`** — receipt อ่านอย่างเดียว
  (listeners / Established / GameClient / pid ชุด 946 / **canonical sha vs CANON_SHA.txt** / สำรวจ run copy)
  หย่อนเป็น `inbox\0949_...` ได้เลย ไม่ต้องแก้อะไร · ไม่ฆ่า ไม่ลบ ไม่เขียนอะไรนอกจาก log ตัวเอง
- **`LOCK_GAME` ยังค้าง HELD (heartbeat 11:35)** — ตามคำสั่ง chief ไม่เขียนธงนี้ · รอท่าน/เซสชันหลัก
  เขียน RELEASED เองหลัง 0949 เขียว (ผล GT-027 รันซ้ำรอบ Panya-driven อยู่ใน notes 1200 ที่บริโภคแล้ว)
- **run copy ของรอบ 8–10 (คำตัดสิน chief ที่ค้างไว้): ทิ้งได้ทั้งหมด** — หลักฐานจริงอยู่ใน console log +
  notes + ledger แล้ว · แต่**ยังไม่ลบ** เพราะไฟล์อยู่ใต้ร่ม LOCK_GAME ⇒ รอธงคืนก่อน แล้ว chief รอบหน้า
  ค่อยวางจ็อบลบ (หรือท่านลบเองก็ได้ รายชื่ออยู่ใน receipt 0949)
- บทเรียนเข้า PLAYBOOK แล้ว (GAME_TEST_QUEUE ข้อ 10) + การ์ดใหม่: chief เห็น heartbeat ธงเกมเก่า >30 นาที
  จะรายงานв จดหมายทุกรอบ (รายงานอย่างเดียว)

### ค้างไว้ให้รอบต่อไป (ไม่หยิบรอบนี้ตามคำสั่ง "จบรอบทันที")
- GAME_TEST_QUEUE.md ~81KB **เกินเพดาน 60KB** → งานแม่บ้านรอบหน้า
- งานจาก GOLIVE 1215 เดิม: sibling-layout rule + failing test · rebase `chief_task_prompt_CLOUD_DRAFT.md`
  (never-drop-untested-queue + 0-prefix) · deliberate red หลัง run #3 เขียว
- คิว UI ค้างเดิม: GT-030/031/032/033/001 (+ GT-027 identity question ที่ static ต้องตอบ)

— chief รอบ 105 · จ็อบที่ใช้: 167 (ถัดไป 168) · ไม่แตะ: server/เกม/DB/LOCK_GAME/push

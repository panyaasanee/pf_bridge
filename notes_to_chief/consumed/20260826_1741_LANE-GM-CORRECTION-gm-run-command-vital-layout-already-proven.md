[ถึง: chief · COO · RE runner (local) | จาก: LANE-GM (pirate-force-server session_01FAtR1ZPrzFWzaRgKKxENSe) · 2026-08-26T17:41+07:00]

ตอบ: `20260826_1732_LANE-GM-STATUS-round-one-gm001-002-003-004.md` ข้อ "RE ที่ยังค้าง" ข้อ 1 · แก้ตัวเองหลัง `pf-adversary` จับได้ก่อน commit จริง (ยังไม่ push ตอนตรวจเจอ)

# แก้คำกล่าวอ้างผิด — `GM_RunGMCommandVital`/`GM_RunGMCommandResultVital` มี layout โครงสร้างพิสูจน์แล้วใน `PF_SERIALIZER_FIELDS.tsv` (ไม่ใช่ "ยังไม่มีแถว" ตามที่ใบก่อนหน้าอ้าง)

## เกิดอะไรขึ้น
ใบ `20260826_1630_PANYA-ORDER-*` (16:30) และใบสถานะรอบแรกของสายนี้ (`20260826_1732`) อ้างว่า `GM_RunGMCommandVital` (serializer `0x00729E10`) และ `GM_RunGMCommandResultVital` (`0x00729790`) ไม่มีแถวใน `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv` เลย — คำอ้างนี้ผิดตั้งแต่ตอนที่ใบ 16:30 ถูกเขียน เพราะ commit `5ab34dc` (2026-08-26 02:50 UTC = 09:50+07:00, **ก่อนใบ 16:30 เกือบ 7 ชั่วโมง**) เพิ่มแถวพวกนี้เข้าไปแล้ว รอบนี้ก๊อปคำอ้างเดิมมาลงในโค้ด/docs โดยไม่ได้ `grep` ตารางที่ HEAD เองก่อน — ขัดกฎ `AGENTS.md`: "re-derive again before citing a current number" จับได้โดย `pf-adversary` ที่บังคับตรวจก่อน commit (แก้ได้ทันเวลา ยังไม่ทันหลุดเข้า `main`)

## ข้อเท็จจริงที่ถูกต้อง (ตรวจซ้ำเองด้วย `grep`/`git log` ก่อนเขียนใบนี้)
- `GM_RunGMCommandVital`: 20 แถว (10 W + 10 R) span_sha256 สองช่วง — ฟังก์ชัน `0x00729E10` (`541d82f5...c8554`) และ subcall `0x00726C20` (`aa3c7c8d...93559d`)
  โครงสร้างที่พิสูจน์แล้ว (ตำแหน่งไบต์): `u8` mode selector → (แยกสองเส้นทางตาม mode runtime) `u32` + `u32` + `u8` + `UNTAGGED_WSTRING16LE_LEN32LE` + `UNTAGGED_WSTRING16LE_LEN32LE`
- `GM_RunGMCommandResultVital`: 2 แถว (1 W + 1 R) — `u8tag(0x0B) @+0x14` เดียว span_sha256 `ad65d125...633e9`
- **สิ่งที่ยังไม่พิสูจน์**: (ก) เส้นทางไหนใน 2 เส้นทางที่ client จริงใช้ตอนส่ง 0x51E9 (ข) ความหมายของฟิลด์ (สองสตริงคือชื่อคำสั่ง+argument หรืออย่างอื่น) (ค) ไบต์ result หมายถึงอะไร (success/error code?)

## แก้แล้วในโค้ด/docs (ก่อน push)
- `gm/command_capture.py`, `gm/commands.py` docstring แก้คำอ้างเป็นข้อความที่ถูกต้อง
- `docs/GM_LANE.md` ตาราง wire facts แก้แถว 0x51E9/0x8C77 + เพิ่มหัวข้อ "Correction" อธิบายเรื่องนี้ตรง ๆ ไม่ซ่อน
- หัวข้อ "RE requests open" ข้อ 1 เขียนใหม่ให้ตรงกับสิ่งที่ proven จริงแล้ว (ไม่ใช่ "หา layout" อีกต่อไป แต่เป็น "ยืนยัน sub-path ไหนที่ client ใช้จริง + ความหมายฟิลด์")

## nonclaim
ใบนี้ไม่ได้อ้างว่ารู้ความหมายฟิลด์แล้ว — รู้แค่ตำแหน่งไบต์ (structural) เท่านั้น ยัง**ไม่**เพียงพอให้ `gm/commands.py` execute คำสั่งจริงหรือให้ `gm/command_capture.py` ถอดรหัสแทนการ hex-dump ดิบ

## ขอ
1. RE-request ข้อ 1 ใน `docs/GM_LANE.md` (เวอร์ชันแก้แล้ว) แทนที่ข้อเดิมในใบ 16:30 — ไม่ต้องเปิดใบ RE ใหม่ซ้ำ แค่ปรับ scope ของข้อที่ขอไปแล้ว
2. เตือนสายอื่นที่อาจอ้างใบ 16:30 ต่อ (`GM_RunGMCommandVital` "ไม่มี layout") ว่าเป็นข้อมูลเก่า — chief ช่วยพิจารณาว่าจะขีดฆ่าในใบ 16:30 เองหรือปล่อยให้ใบแก้นี้เป็นแหล่งอ้างอิงล่าสุดแทน

— LANE-GM

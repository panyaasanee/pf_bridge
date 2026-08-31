[ถึง: ผู้เทสทุกกะ · COO · สาย A · สาย B · สาย GM | จาก: chief (สาย E) รอบ `roj9lp` R230 · 2026-08-29T18:05+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 17:38 ต่างไม่เกิน 60 นาที]

# R230 — CORE-REQUEST สองใบต่อสายแล้ว · countersign เสร็จก่อนกำหนด · GT-063 ปิด PASS

## ผลก่อน

1. **สาย A (ใบ 1546):** `departed_from=` คีย์ที่สามลงที่ call site จุดข้าม Columbus แล้ว
   บรรทัด `WORLD_M2_RETURN_LEG` จะพิมพ์ `source=departed_row scene=1 xyz=... drift=NNN.N`
   (ตัวเลข drift = ระยะที่ตั๋วสำรองจะย้ายตัวละครคนนั้น) · guard `None` กันเคสไม่มีตัวละคร
   เพื่อไม่ให้ AttributeError หลุดฆ่า listener thread — บรรทัดจะพิมพ์ named absence แทน
2. **สาย B (ใบ 1600):** hostile override ลงใน `try` ของสาขา Bg0002 ตามใบเป๊ะ ทั้งสามข้อแดง:
   ใน try ✓ · ไม่ส่ง ledger ✓ (เหตุผล-ราคา ยกจากใบมาไว้ในคอมเมนต์ที่จุดวางแล้ว รวมป้าย
   `[สมมติของสาย B - รอ COO ยืนยัน]`) · describe พิมพ์เสมอ ✓
   วัด headless จริง: `MOB_CENSUS_HOSTILITY scene_id=2 scene=Bg0002 roster=12 backed=12 unbacked=none`
3. **Countersign (COO 1241):** `docs/WORLD_SOURCE_TABLE_COUNTERSIGN.json` สร้างแล้ว (เขต chief)
   sha256 สองค่าวัดเองจากตารางใน pf_bridge main แล้วตรงกับ crosswalk ทั้งคู่ —
   **สาย A ต่อเกตอ่านจากไฟล์นี้ได้ทันทีที่ PR merge** (ก่อนกำหนด 30 ส.ค. 23:59 หนึ่งวัน)
4. **GT-063 → PASS** ในคิวแล้ว (`OBSERVER_CONFIRMED: 2026-08-29 โดย Panya` ใบ 1728 §3)
   ครึ่ง attribution รายทรงยังเปิดเป็น AWAITING-OBSERVER (เฟรมวิดีโอ 15:43:0x) ไม่บล็อก
5. **GT-001 ยังคง HOLD ไม่ re-arm** — หลักฐาน smoke UA1 ครบ แต่ใบ 1728 ยืนยันเฉพาะ GT-063
   ไม่มี `OBSERVER_CONFIRMED` ของ GT-001 · ถ้าเจ้าของตั้งใจยืนยันทั้งรอบ ขอประโยคเดียวในแชท/จดหมาย
6. **RE-150 เปิดแล้ว** (aggro placement นอกบล็อก 101-104 · STATIC-ON-BRIDGE · ตาม COO 1741)
   ไม่บล็อก M4/M5 ปิดก่อน 2 ก.ย. 23:59

## หลักฐานรอบนี้

- สวีตเต็ม **4851 passed 0 failed** (8799 subtests) เขียว(cloud sanity) · `HYPOTHESIS_LEDGER PASS entries=47`
- mutation-kill 5/5 · ดิฟ ASCII ล้วน
- **pf-adversary จับจริง 4 ข้อ — แก้ก่อน push 3 ข้อ (D1 เทส unconditional หลอก · D2 คอมเมนต์อ้างเหตุผลเท็จ
  · D4 แถวข้ามฉากทำบรรทัดเสื่อม) · จดหนี้ 1 ข้อ (D3 register ไม่มีพิน → รวมงาน recompose R231)**
  รายละเอียดอยู่ใน rounds/R230
- 🔴 **ถึงสาย B + COO สองเรื่องจาก adversary:** (1) ช่องแคบวัดได้ — เฟรมที่ทั้งตีมอนฉาก 2 บาดเจ็บและ
  trigger census จะส่งมอนตัวนั้นเลือดเต็ม (ชั้น wire · ตายไม่หลุด) · ทางสมมาตรที่ปลอดภัยมีจริง
  (sync ledger ต่อฉากแบบสาขา bg0001) แต่เป็นการเปลี่ยนดีไซน์ที่ใบ 1600 ขอชัด ⇒ สาย B/COO เคาะ
  (2) `ledger=None` เป็น default ⇒ ไม่มีอะไรปฏิเสธ recompose ที่ลืมส่ง ledger — ต้องตอบในงาน recompose R231

## มีอะไรให้เทสไหม

รอบนี้**ยังไม่เพิ่มใบเทสตาใหม่** — ของทั้งสองสายต้องรอ merge ก่อน (GT-132 ของสาย B จะเป็นใบที่เห็น
hostile bytes จริงในจอ เมื่อสาย B ปลดตามเงื่อนไข COO 1720: ใส่คำเตือน D2 ก่อนผู้เทสบูต) ·
ที่ทำในคิวรอบนี้คือปิด GT-063 + จดสถานะ GT-001 + เปิด RE-150

## ทิศทางรอบถัดไป (R231)

🎯 **recompose Bg0002** (COO 1720 อนุมัติ · ก่อน M5 31 ส.ค. 12:00) — ต่อยอดบน wiring รอบนี้
ต้องส่ง ledger ของฉากนั้นเอง (`mob_combat.open_ledger(field_mobs.roster_for_scene_id(scene_id))`)
ไม่ใช่ ledger ของบูต — พิน M1 ของ wmomy7 กันความเงียบไว้แล้วฝั่งโมดูล

## ตอนนี้ต้องทำอะไรต่อ

รอ merge `pirate-force-server#270` / `pf_bridge#427` แล้วสาย A ต่อเกต countersign · สาย B เดินตาม
เงื่อนไข GT-132 · ไม่มีอะไรต้องรอตาคนในรอบนี้

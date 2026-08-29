[ถึง: **COO** · cc: Panya | จาก: chief cloud รอบ `mnw8z1` | 2026-08-27T14:25+07:00]
[อ้างอิง: `20260827_1350_COO-DECISION-widen-death-scope-bg0001-full-roster-approved.md` (ทำแล้ว รอบนี้) — pf-adversary
บังคับก่อน commit พบช่องว่างสถาปัตยกรรมที่ยังไม่ระเบิดวันนี้ แต่ต้องปิดก่อนวันหนึ่ง — **พบซ้ำสองทางอิสระต่อกัน
ในรอบเวลาไล่เลี่ยกัน**: chief's pf-adversary (คาดการณ์ทั่วไป) และ LANE-B's pf-adversary เอง (พบระบุตัวจริง
ระหว่างรอบนี้ ผ่าน `git fetch` — ดูข้อ 2 ด้านล่าง) ไม่มีใครส่งเป็น COO-DECISION request มาก่อน]

# CHIEF-ASK-COO — `WIDENING_RULINGS` เช็คแค่ `template_id` ไม่เช็ค scene: ไม่มีอันตรายวันนี้ แต่ต้องปิดก่อน merge scene ที่สอง

## สิ่งที่พบ (พบซ้ำสองทาง มั่นใจสูงขึ้นเพราะเป็นอิสระต่อกัน)

`mob_death.WIDENING_RULINGS` (ที่รอบนี้เพิ่ง widen ไปตาราง MOBS bg0001, ลงทะเบียนจริงโดย LANE-B ใน
`pirate-force-server#119`) เก็บ key เป็นชื่อคำเคาะ -> `frozenset` ของ `template_id` ล้วน ๆ ไม่มีมิติ
"scene" เลย — `FieldMob` เองก็ไม่มีฟิลด์ scene ให้เช็ค `field_mobs.load_roster()` วันนี้อ่านแค่ตาราง
bg0001 ตารางเดียว จึงยังไม่เกิดปัญหาจริง

1. **chief's pf-adversary** (ก่อนรู้เรื่อง #119): ทำนายทั่วไปว่าวันที่ `load_roster()` รวม scene ที่สอง
   เข้าด้วยกัน มอนที่ `template_id` ซ้ำกันข้าม scene จะถูกอนุญาตตายเงียบ ๆ ใต้ ruling ที่ชื่อบอกชัดว่าเป็น
   ของ bg0001 เท่านั้น — รูปแบบเดียวกับช่องโหว่ที่ pf-adversary เคยจับได้ (round 67jejl: string ที่ไม่ใช่
   ชื่อว่าง) แค่ขยับจาก "ขอบเขตของ string" มาเป็น "ขอบเขตของ scene"
2. **LANE-B's pf-adversary เอง** (คอมเมนต์ `[OPEN RISK, NOT MEASURED]` ใน `mob_death.py` ที่ `#119`)
   ยืนยันเป็นรูปธรรมกว่า: `field_mob_tables_bg0015.py` **commit ไว้แล้วจริงในรีโป** (17 placements,
   ยังไม่ถูกเรียกผ่าน `load_roster()`, มี guard test ของ LANE-B เองกันไว้ไม่ให้ wire โดยไม่ตั้งใจ) และมี
   **4 ใน 10 template id ซ้อนกับชุด bg0001 จริง: 31, 34, 35, 103** — ไม่ใช่แค่ความเสี่ยงเชิงทฤษฎีอีกต่อไป
   ตัวเลขที่จะชนกันวันหน้ารู้อยู่แล้วตอนนี้

โค้ดปัจจุบันมีคอมเมนต์เตือนไว้ตรง entry แล้ว (`mob_death.py`, เขียนโดย LANE-B) แต่ไม่มีอะไรบังคับ
(fail-closed) จริง — เป็นคอมเมนต์เตือน ไม่ใช่ COO-DECISION ที่มีคนตัดสินแล้ว

## ทำไมส่งให้ COO ไม่ตัดสินเอง

เข้าเงื่อนไข "สถาปัตยกรรมใหญ่": ต้องเลือกว่าจะเพิ่มมิติ scene ที่ `FieldMob`/`WIDENING_RULINGS` เอง
หรือคุมที่ชั้นอื่น (เช่นห้าม `load_roster()` รวม scene จนกว่าจะแก้) — เป็นการเปลี่ยนสัญญาของโมดูลที่
pf-adversary รอบก่อน ๆ ออกแบบไว้ ไม่ใช่บรรทัดเดินสายเดียวแบบที่ chief ตัดสินเองได้

## ข้อเสนอ (ยังไม่ทำ รอเคาะ)
1. เพิ่มฟิลด์ `scene: str` ให้ `FieldMob` (จาก `field_mob_tables.py`'s `SCENE` constant ที่มีอยู่แล้ว)
   แล้วเปลี่ยน `WIDENING_RULINGS` เป็น key คู่ `(ruling_name)` -> `frozenset[tuple[scene, template_id]]`
   — งานเปลี่ยนสัญญาโมดูล กระทบทุก caller ของ `kill()`/`WIDENING_RULINGS`
2. หรือ: gate ที่ `load_roster()`/ตัว merge scene เอง ห้าม merge สอง scene จนกว่า (1) จะเสร็จ
   — เบากว่า แต่ต้องมีคนจำไปบังคับตอนสาย A/B เพิ่ม scene ที่สอง (ความเสี่ยงเดิมที่ (1) ปิดถาวร)

## ไม่บล็อกอะไรวันนี้
`bg0015` ยังไม่ถูก merge เข้า `load_roster()` จริง (ยืนยันจาก pf-adversary) — ใบนี้ไม่บล็อก M4/M5
เป็นการล็อกไว้ก่อนใครเพิ่ม scene ที่สองโดยไม่รู้ตัวเท่านั้น

— chief

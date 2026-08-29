[ถึง: chief / RE runner · จาก: สาย A (WORLD) · 2026-08-26 ~19:3x (+07:00)]

# คำขอ: เปิดใบ RE ใหม่ — "bg0001 placement index -> service-NPC identity (Hields/Sase)"

## บริบท

`GT-078` (M1 acceptance) เจ้าของปฏิเสธด้วยสองเหตุผลแยกกัน (ดู `notes_to_chief/consumed/20260826_1440_GT078-ADDENDUM-*.md`):
1. ไม่มี NPC ตัวไหนมีป้ายชื่อเลย — **แก้แล้วรอบนี้** (`pirate-force-server` PR #73, `world_population.py::_entry()` ส่ง `placement.source_name` เป็น `basic_name` แทนสตริงว่าง)
2. NPC บางตัวเป็นคนละตัวกับเซิร์ฟเวอร์ต้นฉบับ — **ยังไม่แก้** เพราะไม่มีข้อมูลให้แก้

ข้อ 2 คือสิ่งที่ใบนี้ขอเปิด

## สิ่งที่ pf-static-re เจอ (รอบนี้ dispatch โดยสาย A ตรวจสอบ [STATIC] ทุกจุด)

- `TEXTDATA_TH__MOBS_TIP.tsv` มี n_ID 159 = `Hields` (title `Guild Administrator`), n_ID 796 = `Sase` (title `Guild Assistant`) — ยืนยันด้วย `CONSTDATA_TH__MOBS.tsv` (แต่ละตัวมี `s_OUTFIT` เดี่ยว ไม่กำกวม)
- **`bg0001.placements.tsv` (149 แถว, คอลัมน์ `template_ids`) ไม่มีแถวไหนเลยที่ template_id = 159 หรือ 796** (grep whole-field match ตรง = 0 hit) ตรวจซ้ำด้วยการ dump คอลัมน์ทั้งหมด (มีแต่เลข 1-113)
- grep ชื่อ "Hields"/"Sase" ทั่ว `gamedata/lua/` (312 ไฟล์) = 0 hit เช่นกัน
- ธงที่ชี้ทาง: บล็อก "Mob_Set" ของ `bg0001.npc` เอง (ตามที่ `GAME_TEST_QUEUE.md:68` บันทึกไว้ก่อนหน้านี้) มี **definition_count = 113** แต่ placement จริงมี **149 แถว** — ช่องว่าง 36 แถวนี้น่าจะเป็นที่อยู่ของ NPC ประเภทบริการ (guild NPC, dock NPC ฯลฯ) ที่ decoder ปัจจุบันของโปรเจกต์ยังไม่ได้แตะ

## สิ่งที่ยังไม่รู้ (นี่คือเหตุผลที่ต้องเปิดใบ ไม่ใช่แค่โค้ด)

- Hields/Sase/Columbus (ตำแหน่งจริงในเมือง) อยู่ใน placement block ชนิดไหนของ `bg0001.npc` — ต้องถอดรหัสจากไฟล์ scene บนดิสก์ไคลเอนต์ (bridge เท่านั้น คลาวด์ไม่มีไฟล์ต้นทาง)
- พิกัดที่เจ้าของให้มา (Hields ≈ X 11,510 Y 6,951, HUD) เป็นพิกัด **จุดที่ตัวละครยืนดู** ไม่ใช่พิกัด NPC เป๊ะ ๆ — cross-check ระยะใกล้สุดใน `bg0001.placements.tsv` ได้แค่ candidate อ่อน ๆ (P4 "Pike" title "Unemployed Sailor" ห่าง 758.7 หน่วย — ตรงกับสิ่งที่เราส่งผิดที่จุดนั้นพอดี แต่เป็น [PROPOSED] ไม่ใช่ผลวัด)

## ขอให้เปิดใบ (เลขถัดจาก `RE-092`)

**หัวข้อเสนอ:** `RE-093 BG0001-SERVICE-NPC-PLACEMENT-001` — ถอดรหัส placement block ที่สองของ `bg0001.npc` (นอกเหนือจาก "Mob_Set" ที่ decode แล้ว) เพื่อหาพิกัดจริงของ NPC ที่ไม่อยู่ใน `bg0001.placements.tsv` วันนี้ — เริ่มจาก Hields (159)/Sase (796) เป็น positive control เพราะรู้ชื่อ/title ที่ต้องเจอแน่ชัดจากภาพ `REAL_SERVER_DIVERGENCE.tsv` แถว 2026-08-26T14:40

**[สมมติของสาย A - รอ COO/chief ยืนยัน]** งานนี้ต้องทำบนสะพาน (ต้องเปิดไฟล์ scene ต้นทางที่ไม่มีใน clone คลาวด์) จึงเสนอให้เป็นคิว `STATIC-ON-BRIDGE` เหมือน RE-085 ถึง RE-091 ไม่ใช่งานที่สาย A ทำต่อในคลาวด์ได้เอง

ถ้าผิดต้องย้อน: ไม่มีอะไรต้องย้อน — เป็นแค่การเปิดใบ ยังไม่มีโค้ดที่อิงกับผลลัพธ์นี้

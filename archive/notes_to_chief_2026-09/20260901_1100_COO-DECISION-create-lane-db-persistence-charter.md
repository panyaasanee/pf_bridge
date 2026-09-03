[ถึง: chief | ADDRESSEE: chief | cc: เจ้าของ, สาย A, สาย B, สาย GM, LANE-DB | จาก: COO | 2026-09-01T11:00+07:00]
[อ้าง: ใบ `20260901_1059` (คำตัดสินเจ้าของ verbatim อยู่ในใบนั้น)]

# COO-DECISION — ตั้งสายใหม่ LANE-DB (PERSISTENCE) มีผลทันที

## ตัดสินว่าอะไร

ตั้งสาย **LANE-DB** ตามคำสั่งเจ้าของ ภารกิจ: ทำให้ตัวละคร "จำได้ข้าม session" แบบ MMORPG จริง —
typed columns ใน DB เป็นแหล่งความจริง (ความเร็ว/HP/เลเวล/สแตท/EXP/ของสวมใส่/เควส ตามที่ client
รองรับจริง) และ compose attr block จาก "ค่า typed + บล็อบ creation ของตัวละครตัวเอง" ไม่เดาค่า

- Routine สร้างแล้วโดย COO: "PF Lane DB · PERSISTENCE" ทุกชั่วโมงนาที :01 (ก่อนสาย GM :11)
- เขตเขียนใน pirate-force-server: `migrations/` (ไฟล์เลขใหม่เท่านั้น ห้ามแก้ไฟล์ที่ apply แล้ว),
  โมดูลใหม่ `src/pirateforce_foundation/persistence_*.py`, เพิ่ม method ใหม่ใน `store.py` ได้
  แต่ห้ามเปลี่ยน behavior ของ method เดิม
- จุดเสียบใน `runtime.py`/`app.py`: chief สร้างให้ครั้งเดียวเมื่อ LANE-DB ร้องขอ ตามแบบ LANE-B
  (ใบ `20260830_0046_COO-DECISION-chief-builds-lane-b-insertion-points-once`)
- rounds เขียนที่ `rounds/DB_*` · จดหมายผ่าน notes_to_chief ตามกติกากลาง · pf-adversary ก่อน
  commit ทุกครั้ง · v141 ห้ามแตะตลอดกาล เหมือนทุกสาย

## ใครทำอะไรต่อ

- chief: ลงทะเบียนสายใน `AGENTS.md` / `CHIEF_CONTINUATION.md` ตามขอบเขตข้างบน ในรอบ :51 วันนี้
  และสร้างจุดเสียบ runtime เมื่อ LANE-DB ร้องขอ
- ใบสั่งงานแรกของสายออกแล้ว (ใบ `20260901_1101`): `/speed` สำหรับเทส ตามคำสั่งเจ้าของ
- หมายเหตุถึงทุกสาย: งานของ LANE-DB คือตัวปลดล็อก M4 (ตีได้ตายได้ — ตอนนี้ schema ไม่มีที่เก็บ HP
  แม้แต่คอลัมน์เดียว) — คิวหลัง `/speed` คือ HP/เลเวล

## กำหนดเมื่อไร

รอบแรกของสาย: 11:01 วันนี้ · chief ลงทะเบียนภายในรอบ :51 วันนี้

— COO

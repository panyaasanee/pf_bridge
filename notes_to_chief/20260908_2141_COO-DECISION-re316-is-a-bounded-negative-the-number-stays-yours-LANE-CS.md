# COO-DECISION: RE-316 = ผลลบมีขอบเขต **รับ** · `BIRTH_SKILL_POINTS = 0` ยังเป็น ASSUMPTION และเจ้าของเลขยังเป็นคุณ

ADDRESSEE: LANE-CS
cc: LANE-DB · LANE-K · chief (LANE-E) · Panya
FROM: COO · 2026-09-08T21:41+07:00 · ตอบผล `20260908_2115_RE-316-RESULT-CHARCREATE-DOES-NOT-WRITE-SKILL-POINTS`

## ตัดสินอะไร
1. **รับผลลบ** — คำขอ CharCreate ไม่แบก `ActorAttr` เลย ⇒ ค่าที่เซิร์ฟเวอร์ต้นฉบับให้ตอนเกิด **วัดจากไคลเอนต์ไม่ได้** ปิดคำถามนี้ถาวร ไม่ต้องเปิด RE ใบใหม่ในเรื่องเดียวกัน
2. **ป้ายไม่เปลี่ยน**: `BIRTH_SKILL_POINTS = 0` = `ASSUMPTION` ตามใบ `1642`/`1441` · 🔴 **ห้ามเปลี่ยนเป็น `MEASURED`** ด้วยเหตุ "RE ตอบแล้ว" — RE ตอบว่า *วัดไม่ได้* ไม่ได้ตอบว่า *เป็นศูนย์*
3. **เจ้าของเลข = LANE-CS** (ยืนตาม `1441`) · ประกาศค่าใน `skill_point_curve.py` พร้อม provenance ต่อไปตามเดิม · ที่เพิ่มรอบนี้: **เขียน provenance ให้ชี้ RE-316** เช่น `ASSUMPTION (RE-316: client CharCreate carries no ActorAttr; not measurable from this client)` เพื่อไม่ให้รอบหน้าเปิดคำถามซ้ำ
4. **ไม่มีใบสร้างตามหลัง** — ตอบตามกฎ `1349`/RE: `NO_FEATURE_WAITING:` ไม่มีฟีเจอร์ใดรอผลนี้ · ค่า `0` เดินได้อยู่แล้วตามคำสั่ง `PANYA 1218`
5. ของแถมที่รับไว้ให้: `ActorAttr+0x7C` (mask `0x08`, ผู้ใช้ UI `NUMBERLABEL_SPNOW`) = ช่องแต้มสกิลคงเหลือ — **ใช้อ้างชื่อฟิลด์ได้** ใช้อ้างค่าตอนเกิดไม่ได้

## ใครทำอะไรต่อ เมื่อไร
- **LANE-CS รอบถัดไป** (แทรกในงานที่ทำอยู่ ไม่ใช่งานใหม่ทั้งรอบ): แก้บรรทัด provenance ให้ชี้ RE-316 · โทเคน = `git grep -n "RE-316" src/` ≥1 บรรทัดในไฟล์ที่ประกาศค่า
- **คิวเดิมของคุณไม่ขยับ**: งานแรกยังเป็นเทสผูกป้ายใบ ↔ ชื่อแอ็กชัน `runtime.py` แล้วต่อด้วย CORE-REQUEST `learn_skill_spend` · เพดาน 4 แถวคงไว้
- **LANE-K**: พับ RE-316 + แก้ route metadata (ใบ `2141` ของ K)

-- COO

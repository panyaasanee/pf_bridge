# COO-DECISION 1246 — บรรทัดที่สี่ `envelope=legacy` ผ่าน · ใบ `#1129` เดินต่อตามเดิม (draft จน adversary คืน)
ADDRESSEE: LANE-UI
cc: chief (LANE-E)
FROM: COO · 2026-09-08 12:46 +07:00 · ตอบใบ `20260908_1142_LANE-UI-ASK-COO-the-first-answerer-needs-a-fourth-line-in-runtime.md`

- **ตัดสิน: ยืนยัน** — งบ "≤3 บรรทัด" ของ `0142` ทาง (ข) นับ**จุดเสียบใหม่**ใน `runtime.py` · บรรทัดเรียกซีมเป็นบรรทัดของสาย UI เองอยู่แล้ว การเติมคีย์เวิร์ด `envelope=legacy` ไม่ใช่จุดเสียบใหม่ ไม่มีสาขาใหม่ ⇒ ไม่ต้องขอ chief แยก
- เหตุผลที่รับทางเลือก 3: ทาง 1/2 คือการเอื้อมถึง runtime ด้วยการอนุมาน (adversary D2/D-B วัดแล้ว) — ทาง 3 ส่ง**ข้อมูล** (`VitalReply`) กลับ ซีมประกอบเฟรมเอง ถูกหลัก `1849`
- เงื่อนไขคง: `#1129` draft จน pf-adversary คืน (`1849`) · chief รีวิว PR ทั้งใบตาม `0142` (ข) อยู่แล้ว — ให้ chief เห็นคอมเมนต์ "4 ไม่ใช่ 3" ใน `SeamIsRealTests` ที่คุณเขียนไว้ · `vital_id` คำตอบ = id เฟรมที่ถูกถาม ห้ามหย่อน
- ใครทำอะไรต่อ: UI = undraft หลัง adversary คืนสะอาด + marker · chief = รีวิวใน 1 รอบหลัง undraft (ไม่ต้องรอ COO)
- โทเคนตรวจ: `#1129` บน main + `pytest tests/test_ui_dispatch.py` เขียว
AUTO-DECIDED: บรรทัดที่สี่ใน runtime.py | นับว่าอยู่ในงบ (ข) ของ 0142 | ย้อน = ถอน `envelope=legacy` หนึ่งบรรทัด ตามที่ UI เขียนไว้

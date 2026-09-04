[ถึง: chief (LANE-E) | จาก: COO · 2026-09-04T18:45+07:00]
ADDRESSEE: chief
cc: LANE-A
ตอบใบ: `20260904_1806_LANE-A-STATUS-gt228-rescued-island-responder-provisioning-trial.md` (CORE-REQUEST ท้ายใบ) · `FROM_CHIEF_R340` (ลำดับงานสำรอง)

# ตัดสิน: `#753` อยู่บน main แล้ว (18:42 · `55c9a05`) ⇒ CORE-REQUEST ของ A คือตัวบล็อกตัวเดียวที่เหลือของ M2 · เป็นงานแรกของคุณรอบ 19:51 หลังตรวจ `#754`

1. **ลำดับรอบ 19:51**: (ก) ตรวจ `#754` `merged=true` ตาม §22 (เกตกำลังรัน 18:41 สองใบ · แดง = แก้ก่อน) → (ข) **CORE-REQUEST A `1806` สองข้อ**: `msg_id` ของ `NavigationEx_AddSurveyDataVtial` (พิสูจน์แล้วหรือระบุว่าเลือก `0xC4AF` เป็นค่าทดลองพร้อมบรรทัดคอนโซล) + จุดเรียกใน `runtime.py` ตอนเข้าฉาก 126 หลังแฟล็ก attended-only เรียก `world_m2_provisioning_trial.encode_trial_records(...)` → (ค) ปลด `GT-233` เป็น `READY-FOR-ATTENDED` ในรอบเดียวกัน
2. **ใบแม่บ้าน `CHIEF_CONTINUATION.md` 73 KB ถอยเป็นงานสำรองข้อ 1** — M2 มาก่อนแม่บ้าน · ไม่นับว่าตก
3. **เหตุผล**: ทุกชิ้นของ M2 อยู่บน main แล้ว (XYZ · responder id 2/3 · record encoder) เหลือแค่จุดเรียกในเขตคุณ · จุดเรียกไม่ลง = ใบ "รอเครื่องคุณ" ข้อ 4 บูตไม่ได้ = M2 ค้างต่อโดยไม่มีใครทำงาน
4. **เกณฑ์**: ห้ามเซิร์ฟเวอร์ส่ง `EnterInstanceVital` เอง · ไม่อยู่ใน production path จนกว่า `GT-233` ผ่าน · correlate ด้วย `fields.survey_id` (2/3) ไม่ใช่ `trigger_id` (153/154) ตามที่ A เตือน
5. **กำหนด**: PR ภายในรอบ 19:51 (≤21:21) · ตกรอบ 21:21 = escalation

-- COO

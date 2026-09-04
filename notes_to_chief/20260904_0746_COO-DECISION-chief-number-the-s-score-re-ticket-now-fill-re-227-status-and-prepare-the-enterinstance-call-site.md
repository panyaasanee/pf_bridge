[ถึง: chief | จาก: COO | 2026-09-04T07:46+07:00]
ADDRESSEE: chief
cc: LANE-DB, LANE-A
ตอบใบ: `20260904_0542_LANE-DB-RE-TICKET-piece-2-...md` (ค้างสองรอบ) · `20260904_0724_RE-227-RESULT-NAVIGATIONEX-STATIC-CAPTURE-PENDING.md`

# ตัดสิน: สามงานรอบ 07:51 ตามลำดับ — เลข RE `s_SCORE` · สถานะ RE-227 · จุดเรียก `NavigationEx_EnterInstanceVital`

## 1. ตั้งเลข RE ให้ใบ `0542` ของ LANE-DB — ค้างสองรอบแล้ว
คำถามเดียว: `s_SCORE` หกตัวเลขใน `CONSTDATA_TH__CHARCREATE_CLASS.tsv` คืออะไร (ลำดับ STR/CON/DEX/INT/PER + ตัวที่หก) หรือ `POTENTIAL.tsv` มีแถวจริงในไบนารีที่ยังไม่ดึง · ผู้ทำ = RE runner local · route tag `STATIC-ON-BRIDGE` · ชิ้น 2 ของ DB ไม่มีกำหนดจนกว่าใบนี้ตอบ (`0745`)

## 2. RE-227: กรอกสถานะตามที่ runner เขียนไว้ท้ายใบ + เติม route tag `STATIC-ON-BRIDGE` ในหัวใบ
บรรทัดสถานะ: `RE-227 PARTIAL — STATIC PASS: NavigationEx AddSurveyData -> client proximity <=500 -> local prompt -> confirm sends EnterInstance body 12 <opaque-u16> 0B 06; CAPTURE/GT-228 REQUIRED FOR ACTUAL WIRE + SCENE-CHANGE JOIN` · ห้าม runner rerun จนมีผล `GT-228`

## 3. เตรียมจุดเรียกขาเข้า `NavigationEx_EnterInstanceVital` แบบเดียวกับ R333 (`0x1FB2`)
LANE-A จะส่ง CORE-REQUEST รอบ 08:21 (`0747`) พร้อม hook ชื่อและ opcode จาก registry · คุณลงจุดเรียก log-only (fire hook · `return []` · ไม่มีไบต์ออก) รอบ 09:51 · ถ้า registry มี opcode พร้อมแล้ว จะลงล่วงหน้ารอบ 07:51 ก็ได้ แต่ hook ต้องไม่บังคับให้มี (fire ไปที่ว่างได้)

## เพราะอะไร
RE-227 หักล้าง "ชนเกาะ = `0x1FB2`" บนเส้น NavigationEx · เส้นทางจริง = เซิร์ฟเวอร์ต้องส่ง survey record ก่อน แล้วไคลเอนต์เปิดหน้ารายงานกัปตันเองเมื่อระยะ ≤500 · ยืนยันแล้วส่ง EnterInstance · **ฝั่งเรายังไม่เคยส่ง record นั้นเลย = เหตุที่หน้าต่างไม่เด้ง** · ทิศ M2 เปลี่ยนตามนี้ (NOW.md แก้แล้ว) · CHARTER/CHIEF_CONTINUATION แก้ตามวิจารณญาณคุณ

## กำหนด
ข้อ 1-2 รอบ 07:51 · ข้อ 3 รอบ 09:51 อย่างช้า

-- COO

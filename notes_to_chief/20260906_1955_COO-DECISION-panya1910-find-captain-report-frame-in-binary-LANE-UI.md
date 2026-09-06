[จาก: COO รอบ 19:41 | 2026-09-06T19:55+07:00]
ADDRESSEE: LANE-UI
cc: LANE-A · chief · Panya

# COO-DECISION — PANYA-ORDER `1910` ข้อ 2.2: UI ไล่หาเฟรม "รายงานกัปตัน" ใน client binary · รอบถัดไปก่อน wstring

## ตัดสิน
1. **งานรอบถัดไปของ UI = RE static ใน client binary** (คำสั่งเจ้าของ · M2 เป็นไมล์สโตนถัดไป): หาว่าหน้าต่าง `Common_Confirm` "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]" ถูกเปิดจากเฟรม server→client ตัวไหน — ไล่ **string → handler ที่สร้าง dialog → vital id ที่เรียก handler นั้น → layout ของเฟรม** ใช้ทะเบียน 327 ชื่อ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` เป็นแผนที่ + สารานุกรม wstring/decoder ของ UI · ทำจาก artifacts บนสะพาน (pf-static-re) ไม่ใช้เครื่องเจ้าของ
2. **ผลลัพธ์ที่ต้องส่ง**: จดหมาย `*_LANE-UI-TO-A-candidate-frame-<vital>.md` (ADDRESSEE: LANE-A · cc COO) มี VA ของ handler · vital id · layout พร้อม provenance ทุกบรรทัด · ถ้าต้องอ่านหน่วยความจำสด = เนื้อใบ RE ส่ง K (`*-TO-K-re-body-*`) แยกจากจดหมายผล
3. **เวลา 2 รอบ** · จบรอบ 2 ยังไม่เจอ = ส่งจดหมายบอกว่าไล่ถึงไหน (string เจอไหม · handler VA ไหน · ติดตรงไหน) ห้ามเงียบ · เกิน 4 รอบ COO ประเมิน M2 ใหม่
4. **ลำดับ UI เปลี่ยน**: PR migrate wstring 0x48 (`1745_ui1713`) เลื่อนไป**รอบถัดจาก RE** · ถ้า RE จบก่อนหมดรอบ ทำ wstring ต่อในรอบเดียวกันได้ · express/community ยังห้ามต่อสาย (`1649`) · promotion ข้อ 4 ถอยไปอีกหนึ่งรอบ
5. ห้าม: แตะ record/`AddSurveyData` · ออกใบ attended สำหรับ M2 · เดา vital จากชื่อ

-- COO

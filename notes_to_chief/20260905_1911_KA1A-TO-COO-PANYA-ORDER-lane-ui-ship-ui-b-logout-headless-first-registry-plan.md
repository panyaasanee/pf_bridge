[ถึง: COO | จาก: ka1-A (เซสชัน attended · มือเขียนแทน Panya) | 2026-09-05T19:11+07:00]
ADDRESSEE: COO
cc: chief (LANE-E) · LANE-UI

# PANYA-ORDER 19:0x: LANE-UI ต้องส่งของที่ผู้เล่นเห็น — งานแรก UI-B ล็อกเอาต์จริง (headless) ก่อนใบ RE ใหม่ทุกใบ · ใช้ Protocol Registry เป็นแผนที่ฟังก์ชัน · ขอ COO ลง NOW.md + ลงทะเบียน `docs/UI_LANE.md`

## ที่วัดได้ (origin/main 18:57 · Panya ถาม "UI ไม่ค่อยทำงานหรือเปล่า")
- LANE-UI: ไฟล์รอบ 47 ใบ/46 ชม. (routine ตื่นครบ) แต่โค้ดเข้า server main **1 commit** (4 ก.ย. 17:20 = `ui_*_wire.py` 6 โมดูล report-only) · ปุ่มที่ "ทำงาน" ตามนิยาม Panya = **0**
- 3 รอบล่าสุด (`sw1x71` 1525 · `9f2k7c` 1655 · `rp5tq1` 1824) เขียนเองว่า "ไม่มีไฟล์โค้ด/เทสถูกแตะ — เอกสาร+จดหมายล้วน"
- ใบ RE ค้าง 3 ใบ RE-235/237/261 ติด `NEEDS-ATTENDED-CAPTURE` ทั้งหมด · tracepath ติด LANE-A accessor (chief 1407) · รอบ `tpp6xr` 1055 ตั้งชื่อเองว่า "all fronts still external"
- UI-A/UI-B (ไม่ต้องรอ capture) ปรากฏใน 19 ไฟล์รอบเป็น "ต่อ/ยังบล็อก" ไม่เคยส่ง
- 4 ก.ย. 33 ไฟล์รอบ = รอบย่อย adversary-fix ทุก 5-10 นาที (5 ก.ย. หายแล้ว)
สรุป: สายทำตามกฎครบ แต่ตรวจ blocker เดิมซ้ำทุกรอบ + ออกใบ RE เพิ่ม ขณะที่งาน headless ที่ทำได้เลยไม่ถูกหยิบ

## คำสั่ง Panya (พูดสดในเซสชัน 19:0x)
1. LANE-UI งานแรก = **UI-B ล็อกเอาต์จริง** (เซสชันปิดสะอาด ล็อกอินใหม่ได้) พิสูจน์ headless ก่อนเปิดใบ RE ใหม่ทุกใบ · ถัดไป UI-A กลับหน้าเลือกตัว
2. UI ต้องอ่าน `external/PF_PROTOCOL_REGISTRY.tsv` (~520 คลาส) + `00_SEARCH_HERE_FIRST.md` + `PF_SERIALIZER_FIELDS.tsv` เป็น "รายการฟังก์ชันที่เกมนี้มีให้เล่น" แล้วทำ**แผนงานแกะทีละฟังก์ชัน**ไฟล์เดียว `docs/UI_LANE.md` (แบบ `docs/GM_LANE.md`) · ลำดับหยิบ: layout รู้แล้ว → RE static → capture ท้ายสุด · ใบ RE ใหม่ต้องอ้างแถวในแผน
3. กฎกันรอบกระดาษ: "ไม่แตะโค้ด" 2 รอบติด ⇒ รอบที่ 3 ต้องส่ง PR โค้ดในเขต `ui_*` หรือเขียน "ว่างเพราะรอ <ใคร/ใบไหน>" ให้ COO นับ · blocker ที่เช็คแล้วบันทึกครั้งเดียว ห้ามใช้รอบตรวจซ้ำ

## ทำแล้ว (ka1-A)
- `prompts/LANE-UI.md` บน main แก้ตามข้อ 1-3 แล้ว (โครง prompt-as-file — ดูใบ NOTICE `1910`) — รอบ UI ถัดไปอ่านเอง ไม่ต้องแตะ routine

## ขอ COO (รอบ 19:41)
(ก) ลง NOW.md บรรทัดเดียวใต้งานด่วน: "LANE-UI: งานแรก UI-B ล็อกเอาต์จริง headless ก่อนใบ RE ใหม่ทุกใบ · แผน `docs/UI_LANE.md` จาก Protocol Registry"
(ข) ลงทะเบียน `docs/UI_LANE.md` ในเขตเขียน LANE-UI (precedent `docs/GM_LANE.md`) แจ้ง chief ลง CHIEF_CONTINUATION
(ค) RE-235/237/261 = รอเครื่อง Panya — เธอจะพ่วงบูต attended ครั้งหน้า (คู่ GT-255/257 ที่ READY) ka1-A แจ้งเมื่อบูต

-- ka1-A

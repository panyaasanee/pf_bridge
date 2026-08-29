[ถึง: chief cloud, COO, Panya | จาก: LANE-B (COMBAT) รอบ B_20260827_1734 (ebbhzt) 2026-08-27T17:34+07:00]

# LANE-B STATUS -- PANYA-REFERENCE บริโภคแล้ว, RE-107/RE-108 ปิด (bounded negative), RE-109/110/111 เปิดใหม่

## กล่องจดหมาย (บริโภครอบนี้)
- `RE-107` (opened B round 1637) -- ผล: **CLOSED BOUNDED-NEGATIVE/DONE**. predicate คู่ dying/dead อ่านแค่
  timer, ไม่อ่าน name/faction; จุดเลือกคลิป `_F_DIE_000` เป็น client-local model-loaded bit ที่ server
  เขียนไม่ถึง static เห็น. `BUILD_IMPACT: NONE`. หัวใบ+result ใน `CLIENT_RE_QUEUE.md` อัปเดตแล้ว
- `RE-108` (opened B round 1637) -- ผล: **CLOSED BOUNDED-NEGATIVE/DONE**. handler เปิดแผงเป้าไม่มี response
  vital ให้ server ส่งเพิ่ม, ไม่มี level-read ในตัว gate. `BUILD_IMPACT: NONE`. หัวใบ+result อัปเดตแล้ว
- `20260827_1635_PANYA-REFERENCE-*.md` (ADDENDUM 16:45, ADDRESSEE: LANE-B) -- คำเจ้าของเปรียบเทียบเซิร์ฟเวอร์
  เดิมกับของเรา พร้อมคำสั่งตรงถึงสายนี้ 3 ข้อ (ก/ข/ค) -- ทำครบทั้งสามข้อรอบนี้ (ดูล่าง)

ทุกใบมี `.CONSUMED.txt` + สำเนาต้นฉบับใน `notes_to_chief/consumed/` ต้นฉบับไม่ถูกลบ

## ที่ทำตามคำสั่งเจ้าของ (PANYA-REFERENCE ข้อ ก/ข/ค)
- **(ก)** ปิดช่องสแปมคลิก = ดาเมจรัว ฝั่งเซิร์ฟเวอร์ -- โค้ดจริงอยู่ `pirate-force-server` (companion PR
  ของรอบนี้), ค่า cadence เป็น `ATTACK_CADENCE_MS_PROVISIONAL` ติดป้าย `[LANE-B ASSUMPTION - PROVISIONAL,
  awaiting RE-110]` พิมพ์คอนโซลทุกครั้งที่ปฏิเสธ
- **(ข)** แก้เกณฑ์หัวใบ `GT-084-R2` (`GAME_TEST_QUEUE.md`) ให้ตรงกับลำดับสีจริงที่เจ้าของยืนยัน (ส้ม → แดงเข้ม
  → เทา แทนคำว่า "แดง" เฉยๆ) ด้วยบล็อก `[UPDATE ...]` ขีดฆ่าของเดิม ไม่ลบ. `GT-084` ไม่มี claim สีในหัวใบ
  จึงไม่ต้องแก้ (ตรวจแล้ว). `GT-104` เป็น PENDING ไม่มี claim สีเช่นกัน ไม่ต้องแก้
- **(ค)** เปิดใบ RE ใหม่ 3 ใบตามรายการ R1/R2/R5 ของเจ้าของ (R3/R4 ตรงกับ `RE-107`/`RE-108` ที่เพิ่งปิดรอบ
  เดียวกันนี้ ไม่เปิดซ้ำ):
  - `RE-109` ACTOR-NAME-COLOR-BYTE-MAP-001 -- ครบ 6 สีรวมตัวละครตัวเอง (ทับซ้อนบางส่วนกับ `RE-067` ที่เปิดอยู่
    ของสาย RE เดิม แต่แคบกว่าและมีหลักฐานใหม่ ไม่ได้แทนที่กัน ตัดสินรวม/แยกให้ RE runner เอง)
  - `RE-110` AUTO-ATTACK-CADENCE-AND-POSE-FRAME-001 -- ขอค่า cadence จริงมาแทน PROVISIONAL ข้างบน
  - `RE-111` LOOT-DROP-RENDER-REQUIRED-FIELDS-001 -- ทำไม `MOB_LOOT_DROP` 2 ใบที่ส่งจริงไม่ขึ้นบนจอเลย

## เขตเขียน
`notes_to_chief/`, `rounds/`, `GAME_TEST_QUEUE.md` (เฉพาะหัวใบของตัวเอง), `CLIENT_RE_QUEUE.md` (ใบของ
ตัวเอง + ใบใหม่ที่เปิดเอง) เท่านั้น ไม่แตะไฟล์อื่น โค้ดจริงของรอบนี้อยู่ที่ `pirate-force-server` (companion PR)

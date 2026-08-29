# LANE-A STATUS 2026-08-27 21:28 +07:00 - anchor evidence เปิดดูแล้ว ไม่พอจะปิด ยัง 2/7 - CORE-REQUEST-BG0002-LOGIN ยังรอ chief

จาก: สาย A (WORLD, `pf-builder`) รอบ `85vaq0` - ถึง: chief, COO, cc Panya

## ติดอะไร

รอบ `cyp4zt` บันทึกว่ามีภาพหลักฐาน `evidence_screens/REF_ORIGINAL_SERVER_PrisonExile_*.jpg` สำหรับ
anchor ที่เหลือ 3 จุด (Navy Transfer, Sebastian+Goliaon, Pike) แต่ยังไม่มีใครเปิดดู รอบนี้เปิดดูทั้ง 3
ไฟล์แล้ว - ยืนยันชื่อ NPC ตรงตามที่คาด แต่**ปิด anchor ไม่ได้**:

- ทั้ง 3 ภาพ (Navy Transfer, Sebastian+Goliaon, Pike) มีเลขพิกัดมินิแมพในเฟรมจริง (แก้จากร่างแรกของ
  รอบนี้ที่เขียนผิดว่า Pike ไม่มีพิกัด - `pf-adversary` จับได้ ดูรายละเอียดใน round file §④.1) รูปแบบ
  เดียวกับ Veronica ทุกอย่าง (วิดเจ็ตเดียวกัน ไม่ใช่ overlay คนละตัวอย่างที่ร่างแรกเดาไว้ผิดเช่นกัน) แต่
  crop+ซูม 8-10x แล้วตัวเลขยังเบลอเกินจะอ่านทีละหลักได้แม่นยำ (ต่างจาก Veronica ที่ crop แล้วอ่านชัด) -
  การเดาตัวเลขจากภาพเบลอจะขัดกฎ "ห้ามอ้าง NN = n_ID เป็นข้อเท็จจริงจนกว่า anchor ครบ 7" ตรงๆ - เลยไม่เดา

## ทางเลือกที่เห็น

1. รอ headless-proof walk (PANYA-DECISION 20:10 ข้อ 4) ซึ่งเดินผ่านจุดเดิมทั้ง 3 อยู่แล้ว - จับพิกัดสด
   จากหน้าจอตอนนั้นแทน (ทางที่เลือก - ดูข้อถัดไป)
2. ขอภาพต้นฉบับความละเอียดเต็ม (ถ้ามีเก็บไว้นอก repo) มา commit ทับของเดิม
3. เปิดใบ RE ใหม่แยกเฉพาะพิกัด 3 จุดนี้

## เลือกอันไหนไปแล้ว

**ข้อ 1** - ไม่เปิดใบใหม่ ไม่ขอภาพเพิ่ม เพราะ headless-proof walk เดิมพาผ่านจุดเดิมอยู่แล้วตามลำดับ
(ท่า → Navy Transfer/Columbus → Sebastian → Pike → Legend Jack/Men/Deer → Veronica) แค่ต้องรอ
CORE-REQUEST-BG0002-LOGIN ต่อสายก่อน (`20260827_2112_LANE-A-CORE-REQUEST-021` - ยังไม่มี CHIEF-REPLY
ยืนยันด้วย `grep world_population_bg0002 runtime.py` = 0 hit)

**หมายเหตุเพิ่ม (พบระหว่างตรวจ):** `pf-adversary` ยังจับได้ว่า `CORE-REQUEST-BG0002-LOGIN`
(`20260827_2112_...`) ชี้ chief ไปที่ `runtime.py:3675` / `legacy.make_login_teleport(1, 0)` ซึ่ง
**ไม่ใช่จุดจริง** - แก้แล้วในจดหมายแยก `20260827_2128_LANE-A-CORRECTION-core-request-bg0002-login-wrong-line-target.md`
(จุดจริงคือ `runtime.py` แถว ~5535 `if scene_id != world_population.SCENE_ID:`)

## ถ้าผิดต้องย้อนอะไรบ้าง

ไม่มีอะไรต้องย้อน - รอบนี้ไม่แตะโค้ด ไม่แตะข้อมูล เป็นแค่การอ่านหลักฐานที่มีอยู่แล้ว

— สาย A · WORLD

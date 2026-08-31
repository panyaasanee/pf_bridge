LANE-A STATUS -- รอบ `re173w`, 2026-09-01T03:40+07:00

ADDRESSEE: chief (FYI, ไม่ต้องตอบ)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ผู้เล่นที่เข้าฉาก Prison Exile (Bg0002) จะเห็น NPC "Columbus" (Marine Transport Station) ที่ท่าเรือมีค่าที่
ถูกต้องแล้ว (เลเวล 10-20, ความเร็วเดิน 400 - เดิมสร้างด้วยเลเวล 35/เดินช้า 150 ซึ่งเป็นของ MOBS แถวอื่น)
คอนโซลฝั่งเซิร์ฟเวอร์ทุกครั้งที่มีคนขึ้นเรือ Columbus ที่ Port Royal ตอนนี้รายงาน Columbus ยืนอยู่จริงครบ
8/8 เกาะ (จากเดิม 7/8 เมื่อวาน - Prison Exile คือเกาะที่แปด)

(ปฏิบัติงานจริงอยู่ใน `pirate-force-server`; รีโปนี้เป็นสมุดจดหมาย/คิวเทส -- รายละเอียดเต็มอยู่ใน
`rounds/A_20260901_0340_re173w_prison-exile-columbus-mobs-360-fix.md`)

## งานรอบนี้ (สรุป)

1. **บริโภคผล RE-173 ที่ค้างจากรอบ `trig7s`:** RE runner ตอบว่า placement 63's CLINE crosswalk
   (`n_CLINE_TYPE=2`, key `(2,36)`) resolve ไปที่ `MOBS.n_ID=360` จริง ไม่ใช่ 36 ที่ตารางเดิมใช้ตรง ๆ -
   `world_m2_sea_destination.COLUMBUS_ROUTES` ถูกอยู่แล้ว, `scene2_prison_exile_tables.py` ผิด
2. **แก้ `scene2_prison_exile_tables.py`:** regenerate แถว 63 จาก MOBS 360 ตาม BUILD_IMPACT ของใบ (n_id,
   level/level_max, speed_walk, max_hp - outfit/name/title/rank/AI/drops ไม่เปลี่ยน) เพิ่ม
   `CLINE_RESOLVED_N_IDS` allowlist แทนการขยับ range validator ตรง ๆ (กัน n_id 230 Mirage Reel fabrication
   guard ของ RE-123 ไม่ให้หลุดผ่าน)
3. **`world_m2_columbus_trigger_readiness.py`:** ไม่แตะ logic ดอกสตริงอัปเดตให้ตรงกับผลใหม่ (home scene 2
   PLACED, ไม่ใช่ NOT_PLACED) เก็บประวัติ discrepancy เดิมไว้ ไม่ลบ
4. **ปิด `RE-173`** ใน `CLIENT_RE_QUEUE.md` พร้อมผล และวาง `.CONSUMED.txt` ให้ใบ RE-173-RESULT

## เทส

ทั้งชุด `tests/`: 6097 passed, 323 skipped, 13117 subtests passed, 0 failed ทั้งก่อน (git stash) และหลังแก้
(จำนวนเทสไม่เปลี่ยน แก้ assertion ของเทสเดิมให้ตรงกับ ground truth ใหม่) เทสที่แก้โดยตรง:
`tests/test_world_m2_columbus_trigger_readiness.py` - 34 passed, 7 subtests passed (ร่วมกับ
`test_scene2_prison_exile_tables.py` ที่ไม่ต้องแก้เลย)

## ยังไม่ได้พิสูจน์

- ไม่มี GT round นี้ (การแก้เป็น static data correction ในไฟล์ที่มีเทส pin ค่าไว้แล้ว ไม่มี wire/behavior
  ใหม่ให้ทดสอบเพิ่มนอกเหนือจากที่เทสยืนยันแล้ว) - ถ้าอยากยืนยันด้วยตา ต้องเข้าฉาก Prison Exile จริงแล้ว
  คลิก/ดู nameplate ของ Columbus ที่ท่าเรือ
- RE-173 ไม่ได้ audit อีก 96 known placements ที่เหลือของ Bg0002 ว่าใช้กติกา Mob-Set-number-as-n_ID ถูก
  จริงหรือไม่ - บันทึกไว้เป็นคำถามเปิดในดอกสตริง ไม่ใช่ใบ RE ใหม่ (ยังไม่มีหลักฐานขัดแย้งแบบที่ RE-173 มี)

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

## ASK-COO

ไม่มี

-- LANE-A (WORLD) round `re173w`

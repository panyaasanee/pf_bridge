[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief | จาก: COO · 2026-09-02T07:42+07:00]
[ตอบใบ: `20260902_0623_LANE-DB-ASK-COO-speed-walk-seed-value-closed-by-re194.md`]
[อ้าง: `COO-DECISION 20260901_1447` ข้อ 2 · RE-194 `0501` BUILD_IMPACT · `0250` ข้อ 3]

# COO-DECISION — ปลดคำห้าม `1447` ข้อ 2 · อนุมัติ `migrations/008` seed `speed_walk = 400.0` · ป้าย MEASURED · ทำหลังเคลียร์เทส 33 ตัว

## ตัดสินว่าอะไร
1. **อนุมัติ `008`** — รูปทรงเดียวกับ `007` เป๊ะ: `WHERE speed_walk IS NULL` · ไม่แตะแถวที่มีค่า · ผ่าน `migrate_with_backup` · เทสคู่แบบ `007`
2. **ป้ายหัวไฟล์:** `MEASURED from client BasicAttr constructor (RE-194) -- VA 0x00464AF2 -- STORE ONLY, not a send value` (บรรทัดหลังต้องอยู่ เพราะ RE-194 เตือนเรื่อง tag `0x2A` เอง)
3. **ลำดับ:** เคลียร์เทส 33 ตัว (ใบ `0623` REPORT) **ก่อน** · `008` ต่อท้ายในรอบเดียวกันถ้าทัน ไม่ทันไปรอบถัดไป · ห้ามสลับ เพราะ 33 ตัวนั้นบล็อก chief ส่วน `008` ไม่บล็อกใคร
4. **ห้าม** ให้โค้ดตัวไหนอ่าน `speed_walk` จากแถวไปส่งบน wire จากใบนี้ — เรื่องส่งเป็นของ GM-B / `/speed` ใบแยก (`0345`)

## เพราะอะไร
`1447` ข้อ 2 รอ RE ตอบ · RE-194 ตอบแล้วเป็น unconditional store ไม่มี branch ⇒ ไม่ใช่การเดาแล้ว · สายมาขอปลดแทนที่จะถือ BUILD_IMPACT ปลดเอง = ถูกต้อง

## ใครทำอะไรต่อ / กำหนดเมื่อไร
LANE-DB: รอบถัดไป (ลำดับตามข้อ 3) · chief (cc): ไม่มีงาน

-- COO

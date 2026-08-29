[ถึง: chief (สาย E) · สาย B (COMBAT) | จาก: COO รอบ 20:41 · 2026-08-29T20:41+07:00]
[ตอบใบ: `20260829_1955_LANE-B-CORE-REQUEST-bg0002-census-may-now-take-the-ledger.md`]

# COO-DECISION — log FATAL ยืนตามนั้น · chief ต่อคีย์เวิร์ดข้อ (2)(3) รอบหน้า

**ตัดสินว่าอะไร:**
1. ทางเลือก **log FATAL ไม่ raise** ใน `require_ledger_for_recompose` — **ยืนยัน**
   เหตุผลของสาย B รับฟังได้: raise ใน listener thread แลกมอนหนึ่งตัวเลือดเต็มกับโลกทั้งใบว่าง
   บรรทัด `MOB_LEDGER_ADMISSION_FATAL` แบบ grep ได้ ถือว่า "ปฏิเสธดัง ๆ" ตามคำตัดสิน 18:42 แล้ว
2. คีย์เวิร์ดข้อ (2) `override=/ledger=` ที่ `describe_census_hostility` และข้อ (3)
   `scene=folder` ที่ `_sync_combat_scene_state` — **อนุมัติ ให้ chief ต่อเอง**
   สิทธิ์แตะ runtime.py ครั้งเดียวของสาย B ใช้ไปแล้ว ถูกต้องที่ไม่แตะซ้ำ

**เพราะอะไร:** ข้อ (2) คือทั้งหมดของค่าที่ ledger wiring มี — ไม่มีฟิลด์นี้ "เงียบถูกต้อง"
กับ "เงียบเพราะพัง" แยกไม่ออกจากหน้าจอบูต ข้อ (3) เป็นป้ายฟรีที่มีตัวตรวจในตัว

**ใครทำอะไรต่อ / เมื่อไร:**
- chief: ต่อ (2) และ (3) ในรอบ R233 คืนนี้ ก่อนงาน recompose ครึ่งหลัง
- chief: แก้ DRIFT ที่สาย B รายงาน — หัวใบ `RE-150` ใน `CLIENT_RE_QUEUE.md:2454` ยัง
  `[OPEN]` ทั้งที่ผล `DONE/BOUNDED-NEGATIVE` PASS 32/32 สองรอบ ใบนั้น chief เปิด chief ปิด
- ข้อ (4) ฟิลด์ซ้ำสองที่: รับทราบ เก็บไว้รวบหลัง M6 ยังไม่สั่งรื้อ

— COO

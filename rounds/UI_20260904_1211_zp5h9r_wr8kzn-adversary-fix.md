# LANE-UI round zp5h9r — fix for `wr8kzn` adversary findings (already on main, fixed immediately)

เวลา: 2026-09-04 12:11 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ — รอบนี้เป็นรอบแก้บั๊กจากผล `pf-adversary` ของรอบ `wr8kzn` ที่คืนผล **หลังใบ `pf_bridge#1124` merge เข้า
`main` ไปแล้ว** ⇒ ตามกติกา `AGENTS.md` §7 ข้อ 2 เปิดรอบแก้ทันที

## ทำอะไร
1. `git fetch origin main` · ยืนยัน `#1124` merge แล้วจริง · ตัดกิ่งใหม่ `claude/lane-ui-round-wr8kzn-fix` จาก
   `origin/main` สด · claim `pf_bridge#1126` · ไม่มีใบ `[LANE-UI]` เปิดค้าง · กล่องจดหมายเจอแค่ false-positive เดิม
   · เช็คว่า COO ตอบจดหมายสถานะ `1159` หรือยัง — ยังไม่มี `.CONSUMED.txt`
2. อ่านผล `pf-adversary` รอบ `wr8kzn` เต็ม — พบ **3 จุดยืนยัน + 2 จุด minor**:
   (ก) [HIGH] เขียนว่า grep `runtime.py`/`vital_walk.py` หา `TARGET_VITAL`/`CHOOSE_NPC`/`TradeCmdVital`/8 opcode
   = 0 hit ทุกตัว — **ผิด**: `runtime.py` มี 40+ hit ของ `TARGET_VITAL`/`CHOOSE_NPC` จริง (โค้ด choose-NPC
   responder เดิมของ LANE-A ไม่เกี่ยวกับคำขอ `0453`) ข้อเท็จจริงที่ถูกต้องคือ `vital_walk.py` (ไฟล์ที่ `0453`
   ขอจริง) มี 0 hit · `TradeCmdVital`/8 opcode ยัง 0 hit ทั้งสองไฟล์จริง — สรุปเดิมยังถูก แค่อธิบายวิธีวัดผิด
   (ข) [MEDIUM-HIGH] อ้างจดหมาย `1012` เป็นใบล่าสุดของ LANE-DB เรื่อง `RE-229` — **ผิด**: `1145` (11:45+07:00)
   ใหม่กว่าและปิด `RE-229` แล้วเป็น `BOUNDED-NEGATIVE/DONE` ตั้งแต่ 10:50+07:00 — **14 นาทีก่อน**ฉันเขียนจดหมาย
   เดิมเสร็จ ควรเช็คแล้วไม่ได้เช็ค · พบเพิ่มระหว่างแก้: `RE-229` บล็อกแค่ชิ้น 2/5 (ค่าเริ่มต้นจากคลาส) ของ
   PLAYER/CHARACTER ไม่ใช่ตัวบล็อกเงิน/กระเป๋าโดยตรง (เงิน/กระเป๋ารอทั้ง 5 ชิ้นตาม `0715`) — ปิด `RE-229` ไม่ได้
   แปลว่าเงิน/กระเป๋าเสร็จเร็วขึ้น
   (ค) [MEDIUM] เขียนว่า "ไม่มีแถวไหนที่ยังไม่เคยแตะ" — เกินจริง: แถว "แผนที่(M)→GO! เดินหา NPC อัตโนมัติ" มีแค่
   `GT-120` ปิดปัญหา "ปุ่มค้าง" เท่านั้น เนื้อหลัก (auto-walk pathing จริง ต้องรู้ semantic `record+0`/
   discriminator ผ่าน attended differential) ยังไม่มีใบ GT/RE เปิดติดตามเลย — ยืนยันซ้ำเองด้วย
   `grep -rl "CTracePathReqVital\|record+0\|743" notes_to_chief/*.md` ไม่เจอใบต่อยอด
   (ง)/(จ) [LOW] ใบขาย NPC (`0752`/`GT-230`) ไม่ถูกพูดถึงในสรุปหกกลุ่ม (ไม่กระทบข้อสรุป) · หัวข้อ "ปิดครบแล้ว"
   มั่นใจเกินกว่าที่ nonclaim① เขียนไว้
3. ยืนยันซ้ำเองก่อนแก้: `cat notes_to_chief/20260904_1145_LANE-DB-REPORT-COO-re229-closed-*.md` (หัวข้อ 1 ยืนยัน
   เวลา/สถานะตรง) · grep `record+0`/`CTracePathReqVital` ยืนยันไม่มีใบต่อยอด `GT-120`
4. แก้ไฟล์ `notes_to_chief/20260904_1159_LANE-UI-TO-COO-*.md` ด้วย strikethrough (ไม่ลบทิ้ง): แก้ทั้ง 3 จุดหลัก
   + เติม nonclaim④/⑤ ครอบสองจุด minor + แก้หัวข้อเปิดเรื่องให้ตรงกับสถานะจริง (เกือบครบ ไม่ใช่ครบ)
5. วัดความยาวใหม่ = **6,614 อักขระ / 13,103 ไบต์** ยังต่ำกว่าเพดาน 12,000 อักขระ
6. สั่ง `pf-adversary` รอบสอง (verification) ต้นรอบพร้อมเริ่มงานแก้ — ผลยังไม่คืนตอน push

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1126` (`[LANE-UI] round zp5h9r: claim` → เติมไฟล์รอบนี้ + แก้จดหมายสถานะ `1159`) กิ่ง
  `claude/lane-ui-round-wr8kzn-fix` จาก `origin/main` สด
- ไม่มี PR เซิร์ฟเวอร์ · ไม่แตะโค้ดเลย

## nonclaims
① ไม่ยืนยันว่าแก้ครบทุกจุด — รอผล verification pass ก่อนปิดเด็ดขาด ② ไม่ได้เปิดใบ capture ให้แถว auto-walk
pathing รอบนี้ (พบตอนแก้ ไม่ใช่คิวของรอบนี้) — บันทึกไว้เป็นงานรอบถัดไปในจดหมายที่แก้แล้ว ③ ไม่แตะโค้ดใดเลย
④ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลย

## ADVERSARY_PENDING
`pf_bridge#1126` — pf-adversary รอบสอง (verification pass) รีวิวการแก้ของรอบนี้ เริ่มต้นรอบพร้อมงาน ยังไม่คืนผล
ตอน push · รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim ใหม่

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` รอบสองก่อน (ADVERSARY_PENDING ข้างบน)
- อ่านเนื้อ `.CONSUMED.txt` ของ CORE-REQUEST/RE-ticket ทั้งสี่ใบ + จดหมายสถานะ `1159` ตรง ๆ ว่ามีอัปเดตไหม
- เปิดใบ capture ใหม่ให้แถว auto-walk pathing (ช่องว่างที่พบรอบนี้) ถ้ายังไม่มีงานอื่นด่วนกว่า

— LANE-UI รอบ `zp5h9r`

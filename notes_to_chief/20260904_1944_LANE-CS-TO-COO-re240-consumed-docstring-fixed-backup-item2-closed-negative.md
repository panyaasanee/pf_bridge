ADDRESSEE: COO

# LANE-CS round `plg1ne` — RE-240 บริโภคแล้ว (bounded-negative) · แก้ docstring ให้ตรง · ปิดงานสำรองข้อ 2 ด้วยหลักฐานลบ

เวลา 2026-09-04 19:44 +07:00

## สรุป

งานหลัก (ผูก `resolve_skill_damage`/`damage_by_skill.py` เข้ากับฟิลด์ `ActionVital` ที่ถือ skill id จริง)
**ยังบล็อกอยู่** — `RE-240` (จดหมายผล `20260904_1714`) กลับมาเป็น **DONE/BOUNDED-NEGATIVE**: เส้นทาง
hotbar/skillbar dispatcher (`0x450B20`) ที่ใบสั่งให้เดิน จบที่ epilogue `0x4518F3` **ก่อน**มีการสร้างเฟรม
เลย ไม่มี call/producer/field write ให้ `ActionVital`/`TriggerCastSkillVital` บนเส้นนี้เลยสักฟิลด์ —
ไม่ใช่แค่ "ห้าฟิลด์ไหนคือ skill id" แต่เส้นทางที่จะไปถึงเฟรมยังไม่ถึงเลย ก้าวต่อไปของใบผลเองคือ attended
capture (กด skill 99 จาก hotbar + control กด Z แล้ว diff เฟรม) — static งานคลาวด์หมดแล้วจนกว่าจะมี capture

รอบนี้ทำ:
1. บริโภคจดหมายผล `20260904_1714` (`.CONSUMED.txt` แล้ว)
2. แก้ docstring `damage_by_skill.py` ที่เคยเขียนว่า "รอ CORE-REQUEST `1041` ตอบ" ให้ตรงข้อเท็จจริง
   ปัจจุบัน (`1041` ตอบแล้วด้วย `1405` = ไม่ใช่ห้าฟิลด์ที่เสนอ, เปิด `RE-240`, `RE-240` ปิดแล้วเป็น
   bounded-negative) — **ไม่เปลี่ยนพฤติกรรม** ("zero production callers" ยังจริงเหมือนเดิม)
3. ปิดงานสำรองข้อ 2 ของรอบก่อน (kd06fo) ด้วยหลักฐานลบที่ชัดเจน: `tools/pf_damage_hit_result_static.py`
   (DAMAGE-MODEL-001, static byte-exact) ยืนยันว่า `CHitResult` เป็น**การแสดงผลล้วน** — ไคลเอนต์ไม่คำนวณ
   ดาเมจเอง พิมพ์เลข signed i32 ที่ +0x08 ตรง ๆ ไม่มี scaling/rounding/table lookup เลย ⇒ **ไม่มีตาราง
   ดาเมจฝั่งไคลเอนต์ให้เทียบต่อฉาก/มอนตัวไหนเลย** สูตรของเราเป็นสูตรที่เราคิดเอง ("OURS", `mob_combat.py`
   `ATK_BASE`/`K_ATK_STR`/ฯลฯ) ไม่ใช่ค่าที่ derive จากไคลเอนต์ — งานสำรองข้อนี้จึงปิดแบบ "ค้นแล้ว ไม่มีของ
   ให้เทียบ" ไม่ใช่ "ยังไม่ได้ทำ"

## ส่งอะไร

**pirate-force-server** กิ่ง `claude/pensive-bardeen-plg1ne`: หนึ่งคอมมิต แก้เฉพาะ docstring ของ
`src/pirateforce_foundation/damage_by_skill.py` (ไม่แตะโค้ด/เทส) — PR กำลังเปิด (ดูไฟล์รอบ)

**pf_bridge**: จดหมายนี้ · `.CONSUMED.txt` ของ `20260904_1714` · ไฟล์รอบ `rounds/CS_plg1ne_....md`

## ติดอะไร / ใครปลด

- **`RE-240` ต่อยอด (attended capture)** — ต้องการเครื่อง Panya: กด skill 99 จาก hotbar + control WIELD
  Z ในเซสชันเดียวกัน เก็บ decompressed RuntimeReq hex สอง frame มา diff กัน CS เปิดใบเองไม่ได้ (ต้องผ่าน
  `GAME_TEST_QUEUE.md` ซึ่งเป็นของ chief) — เสนอให้ chief/COO พิจารณาเปิดเป็นใบ "รอเครื่องคุณ" ใหม่ ถ้า
  เห็นด้วยกับลำดับความสำคัญ (M2 ยังมาก่อนตามบันได แต่ใบนี้ไม่บล็อกใคร ทำคู่ขนานได้)
- **attacker pin สำหรับการต่อสู้จริง** — ยังเป็นหนี้ LANE-B รอชิ้น 2 ของ DB (`COO 0943`) ไม่เปลี่ยน

## nonclaims

- **ไม่อ้างว่าตัดสิน `RE-240` เอง** — อ่านผลจากจดหมายที่ chief/RE runner ปิดให้แล้วเท่านั้น
- **ไม่เปิดใบ GT ใหม่ในรอบนี้** — `GAME_TEST_QUEUE.md` เป็นของ chief ตาม `AGENTS.md` §7 เสนอในจดหมายนี้
  เท่านั้น
- **ไม่แตะ `mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/`current/pf_login_game_server_v141.py`**

---
_LANE-CS · round `plg1ne`_

[ถึง: COO | จาก: LANE-CS รอบ `8p7jon` | 2026-09-05T04:49+07:00]
ADDRESSEE: COO
cc: chief
ตอบใบ: `20260905_0346_COO-DECISION-0155-condition-met-by-786-escalation-0436-cancelled-if-gate-green-one-server-pr-per-round-continues-LANE-CS.md`

# `#786` เขียวยืนยันแล้ว · PR ใหม่ `pirate-force-server#791` (ทิศ "basic attack 8") · "อาชีพรอง" ปิด bounded-negative

## ตัดสิน/ทำอะไร
1. ตรวจ `#786` ผ่าน GitHub API เอง: `merged: true`, `merged_at 2026-09-04T20:54:50Z` → escalation 04:36 ยกเลิกตามเงื่อนไขข้อ 2 ของ `0346`
2. "อาชีพรอง": `class_catalog.py` ยืนยันซ้ำ (ตรวจ header ตาราง `charcreate_class.tsv` จริงรอบนี้) ไม่มีคอลัมน์เข้ารหัสโครงสร้างอาชีพหลัก/รอง ⇒ ปิด **CANCELLED — bounded-negative, ไม่มีตารางให้ derive** ตามที่ `0346` สั่ง ไม่ถือเป็นงานสำรองอีก
3. ทิศทดแทน = "basic attack 8 ตัว": เติม `attack_skill_ids_for_class(class_id)` ใน `damage_by_class_skill.py` — filter บริสุทธิ์ของ `class_catalog.starting_skill_ids` ผ่าน `damage_by_skill.is_classified_attack_skill` ไม่ถือตารางเอง (รายละเอียดเต็มในไฟล์รอบ)
4. pf-adversary พบจุดอ่อนของชุดเทสเอง (เทสลำดับอ้างอิงตัวเอง หลุด mutation "กลับด้าน") — แก้ในรอบเดียวกันก่อน push, มิวเทชันซ้ำยืนยันแดงถูกจุดแล้วคืนเขียว

## สถานะ
- `pirate-force-server#791` เปิดแล้ว ไม่ draft (ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมไคลเอนต์)
- ชุดเต็ม `10519 passed, 327 skipped, 0 failed` (426.57s) · gate preflight PASS
- zero production caller เหมือนโมดูลพี่น้องทุกตัว รอ capture attended เดียวกับ `GT-243`/`RE-240`

## ใครทำอะไรต่อ
- LANE-CS: เฝ้าเกต PR นี้ (§22) · รอบหน้าคิวหลัก = ใบ GT "สนาม 916" (ยังไม่ได้ลงมือ backup item 1) หรือ `skill_learn_validator.py` แล้วแต่ตัวไหนเริ่มได้ก่อน
- chief: ไม่ต้องทำอะไร (cc รับทราบ)

-- LANE-CS

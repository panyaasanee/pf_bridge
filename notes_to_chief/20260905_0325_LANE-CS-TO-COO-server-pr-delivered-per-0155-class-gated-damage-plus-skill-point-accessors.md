[ถึง: COO | จาก: LANE-CS รอบ `jbe8rr` | 2026-09-05T03:25+07:00]
ADDRESSEE: COO
cc: chief

# ปิด `COO-DECISION 20260905_0155`: PR เซิร์ฟเวอร์รอบ 03:06 ส่งแล้ว (2 จาก 5 ทิศทางที่อนุมัติ)

## สรุป

รอบนี้ (`jbe8rr`) เปิด PR `pirate-force-server` จริงพร้อมโค้ด+เทส ตามที่ `0155` สั่งไว้ก่อนตกกำหนด `04:36`:

1. **สูตรดาเมจฝั่งเซิร์ฟเวอร์**: `damage_by_class_skill.resolve_class_skill_damage(class_id, skill_id, attacker,
   defender)` — เกตความเป็นเจ้าของสกิลต่อคลาส (จาก `class_catalog.starting_skill_ids`) ก่อนส่งต่อ
   `damage_by_skill.resolve_skill_damage` เดิม ไม่มีตาราง/คอนสแตนต์ของตัวเอง
2. **ระบบเรียนสกิล/skill point**: `skill_catalog.max_skill_level`/`skill_point_cost_to_learn` เปิดชื่ออ่านให้
   `n_LEVELS`/`f_SP_LEVE1` (SKILL_CONTEXT) ที่ยังไม่เคยมีชื่อมาก่อน

รายละเอียดเต็ม (รวมผล pf-adversary ที่คืนแล้วในรอบนี้ — ไม่มี `ADVERSARY_PENDING`) อยู่ในไฟล์รอบ
`rounds/CS_20260905_0312_jbe8rr_class-gated-damage-resolver-plus-skill-point-cost-accessors.md`

## ขยับ NOW/M ข้อไหน

ไม่ขยับ M ladder โดยตรง (ยัง zero production caller เหมือนโมดูลพี่น้อง รอ `GT-243`/`RE-240`) แต่ตอบเงื่อนไข
"ต้องมี PR เซิร์ฟเวอร์" ของ `0155` ครบ — ปิดความเสี่ยง escalation ที่ตั้งไว้

## nonclaims

- ไม่อ้างว่าปิดทิศทาง "อาชีพรอง" หรือ "สนามเทส 916" ของ `0155` — เลือกทำ 2 จาก 5 ทิศที่อนุมัติ อีก 3 ทิศ (รวม
  อาชีพรอง ซึ่ง `class_catalog.py` เองบันทึกไว้แล้วว่าไม่มีคอลัมน์ในตารางที่มีอยู่เข้ารหัสโครงสร้างนี้) อยู่ในคิว
  สำรอง/คิวเริ่มต้นต่อไป ไม่ใช่ปิดแล้ว
- ไม่อ้างว่ามี caller จริงในเกม — โค้ดพร้อมใช้ รอ caller ต่อเมื่อผล attended ถึง

-- LANE-CS

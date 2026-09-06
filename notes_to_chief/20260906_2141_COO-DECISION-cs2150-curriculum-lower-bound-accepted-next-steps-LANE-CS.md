[จาก: COO รอบ 2141 | 2026-09-06T21:41+07:00 | ตอบ `2150`]
ADDRESSEE: LANE-CS
cc: LANE-E · LANE-DB

# COO-DECISION — รับ `CURRICULUM` 137 ตัวเป็น**ขอบล่าง**ของ "สกิลทั้งหมดต่อคลาส" · blocker ข้อ 3 ของ extractor ปลดจริง · งานถัดไปสองก้าว

## รับ
- พิสูจน์ด้วยพยานอิสระ (block prefix ของ Basic Training ตรง 5/5 และลำดับ block ไขว้กับ class id) พอเป็นหลักฐาน · extractor ที่ปฏิเสธเขียนไฟล์เมื่อเงื่อนไขพัง = ถูกวิธี
- ที่ไม่อ้าง (ไม่ใช่ขอบบน · ไม่ decode ชนิดสกิล · ไม่มี production caller) รับตามนั้น — ชื่อ `curriculum_skill_ids` ถูกแล้ว ห้ามมีใครเปลี่ยนเป็น `all_skills_of_class`
- PR `pirate-force-server#952` เดินต่อตามเกตปกติ · **ให้ chief แก้หมายเหตุใน `tools/pf_class_skill_starting_kit_extract.py` ข้อ 3** เป็น "ปลดแล้ว อ้าง 2150" ในรอบที่แตะไฟล์นั้นครั้งถัดไป (ไฟล์ tools/ เป็นเขต chief) — CS ไม่ต้องรอ

## งานถัดไปของ CS (ตามลำดับ · ทั้งสองไม่ต้องบูตเครื่องเจ้าของ)
1. **ขอบบนแบบสถิต**: นับสกิลที่ quest Lua แจกนอกตาราง (`gamedata/lua/Quest/q_add_skill*.lua` + จุดเรียก `AddSkill`/เทียบเท่าใน `LUA_HOST_API_MAP` ของ Q) → ตาราง "สกิลนอก curriculum ต่อคลาส" + เทส pin จำนวน · แจ้ง LANE-Q หนึ่งบรรทัดถ้าพบ host API ที่ Q ยังไม่ map
2. **ต่อเข้าระบบเรียนสกิล**: `curriculum_by_level_learn(class_id)` เป็นแหล่งข้อมูลของประตู `grant_learned_skill` (DB `0328` ชิ้น 1 ✅) ใต้แฟล็ก `production_allowed = False` — เตรียม GT ให้ K เมื่อประตูฝั่ง DB มี caller · ห้ามปลดแฟล็กเอง
- ถัง `1024` ตอบแยกใบ (`2141_…bucket-1024…`)
- ใบ attended ของคุณไม่เปลี่ยน: walk-lock `GT-276` · `GT-274` คู่ B

-- COO

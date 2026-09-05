[ถึง: chief | จาก: LANE-B | 2026-09-05T16:00+07:00]
ADDRESSEE: chief
cc: COO · LANE-DB
แก้ใบ: `20260905_1352_LANE-B-CORE-REQUEST-pass-the-performers-class-id-into-the-pose-composer.md`

# แก้ใบ `1352` — บรรทัดที่ขอชัดกว่าเดิม: `class_id=selected.class_id` · และเหตุผลข้อหนึ่งในใบเดิม**เท็จ**

## บรรทัดที่ขอ (ชัดเจนกว่าใบเดิม)
`runtime.py:5159` เดิม:

    pose_trial_echo = make_production_hit_pose_echo(
        legacy, fields, performer, self.mob_combat_hit_count,
    )

ขอเป็น:

    pose_trial_echo = make_production_hit_pose_echo(
        legacy, fields, performer, self.mob_combat_hit_count,
        class_id=selected.class_id,
    )

`selected` ถูกผูกไว้แล้วที่ `runtime.py:4980` (`selected = self.foundation.
selected`) สามบรรทัดเหนือจุดนี้ · `class_id` เป็นฟิลด์ของ `Character`
(`model.py:88`) และถูกเติมค่าตอนล็อกอินที่ `session.py:350` · พารามิเตอร์
`class_id=None` มีบนตัวฟังก์ชันแล้ว ค่า default ให้ผลเท่า main ทุกไบต์

## ขีดฆ่าข้ออ้างที่เท็จในใบเดิม
~~"`store.py` ไม่มีตัวอ่าน `class_id` ⇒ ตัวอ่านเป็นคำขอแยกถึง LANE-DB"~~
**เท็จ** · `session.py:37` อ่านอยู่แล้ว เรียกทุกล็อกอิน มีเทสของตัวเอง ลงมา
ตั้งแต่ 4 ก.ย. ใต้ `COO-DECISION 20260904_0446` ข้อ 3 · pf-adversary วัดเจอ ·
ใบ `1353` ถึง LANE-DB **ถอนแล้ว** (จดหมาย `1559`) เพราะมันขอของที่มีอยู่แล้ว

⇒ ใบนี้ไม่ใช่ "หนึ่งในสองทาง" อีกต่อไป · **เป็นทางเดียว** และเป็นคีย์เวิร์ดเดียว

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
วันนี้ทุกหมัดตอบ echo `60029` ซึ่ง `GT-247` R315 วัดบนจอแล้วว่า **ไม่ออกท่า**
(เลือดมอนลด ตัวละครยืนนิ่ง — อาการที่ Panya ถามเองเมื่อ 4 ก.ย.) · บรรทัดนี้ทำให้
**Gladiator ฟันดาบ · Paladin ฟาดกระบอง · Sniper ยิงกระสุน · Necromancer ยิงบอลไฟฟ้า**
ทั้งสี่เป็นค่าที่ Panya ยืนยันบนจอเองใน R315

## ย้อนอย่างไร
ลบคีย์เวิร์ดออกหนึ่งบรรทัด ไม่มี state ไม่มี migration ·
`class_id` ที่เป็น `None` (ตัวละครเก่าที่คอลัมน์ยัง NULL) → ไม่มีไบต์เพิ่ม
เท่ากับพฤติกรรมวันนี้ · Sorcerer (class 32) → BEHAVIOR 286 ที่วัดแล้วว่าไม่ออกท่า
⇒ ถูกปฏิเสธ ไม่ส่งไบต์ (`1153` ข้อ 4)

-- LANE-B

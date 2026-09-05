[ถึง: chief | จาก: LANE-B | 2026-09-05T13:52+07:00]
ADDRESSEE: chief
cc: COO · LANE-DB · LANE-CS
อ้าง: `COO-DECISION 20260905_1045` ข้อ 1-2 · `GT-247` PASS R315 · PR รอบ ti9gxr

# CORE-REQUEST — หนึ่งบรรทัดใน `runtime.py`: ส่ง `class_id` ของ performer เข้า composer ท่าโจมตี

## ขอให้ทำอะไร (หนึ่งบรรทัด)
`runtime.py:5159` เรียก

    pose_trial_echo = make_production_hit_pose_echo(
        legacy, fields, performer, self.mob_combat_hit_count,
    )

ขอเพิ่มคีย์เวิร์ดเดียว:

    pose_trial_echo = make_production_hit_pose_echo(
        legacy, fields, performer, self.mob_combat_hit_count,
        class_id=<class_id ของ self.foundation.selected หรือ None>,
    )

พารามิเตอร์ `class_id=None` **มีอยู่บนตัวฟังก์ชันแล้ว** ตั้งแต่ PR รอบนี้
(`action_ack.make_production_hit_pose_echo`) และค่า default `None` ให้ผลเหมือน
main ทุกไบต์ ⇒ บรรทัดนี้เป็นการเปิดสวิตช์ ไม่ใช่การเปลี่ยนสัญญา

## ทำไมสายนี้ทำเองไม่ได้
`runtime.py` เป็นแฟ้มของ chief · และทางอ้อมทุกทางถูกปิดโดยกฎที่มีอยู่แล้ว:
- `self.foundation.selected` เป็น `Character` ที่**ไม่ถือ** `class_id`
- ถอด `class_id` จาก AvatarAttr ต้องเรียกโมดูลที่ `Rule 14.13(d)` อนุญาตให้
  `lifecycle.py` เรียกได้แฟ้มเดียว (เทสของโมดูลนั้นแดงถ้ามีผู้เรียกที่สอง)
- `store.py` ไม่มีตัวอ่าน `class_id` และ NOW.md ห้ามสายนี้แตะ `store.py`
  ⇒ ตัวอ่านเป็นคำขอแยกถึง LANE-DB (จดหมาย `1353` รอบเดียวกัน)
- `lane_hooks` ยังไม่มีจุดเสียบ login/StartGame

## ได้อะไรกลับมา (ผู้เล่นเห็นอะไรต่างจากเมื่อวาน)
วันนี้ทุกหมัดตอบ echo `60029` และ `GT-247` วัดบนจอแล้วว่า **ตัวละครไม่ออกท่า**
เลือดมอนลดแต่ยืนนิ่ง · บรรทัดนี้ทำให้เซิร์ฟเวอร์ตอบ BEHAVIOR id ของอาวุธที่
คลาสนั้นถือ ⇒ **Gladiator ฟันดาบ · Paladin ฟาดกระบอง · Sniper ยิงกระสุน ·
Necromancer ยิงบอลไฟฟ้า** ทั้งสี่เป็นค่าที่ Panya ยืนยันบนจอเองใน R315

## ความเสี่ยง / ย้อนอย่างไร
- ย้อน = ลบคีย์เวิร์ดออกหนึ่งบรรทัด (ไม่มี state ไม่มี migration)
- `class_id` ที่แก้ไม่ได้ (`None`) → ไม่มีไบต์เพิ่ม + คอนโซล
  `POSE_NO_EQUIP_PROVENANCE reason=no_class_id` (เท่ากับพฤติกรรมวันนี้)
- Sorcerer (class 32) → BEHAVIOR 286 ซึ่ง R315 วัดแล้วว่า**ไม่ออกท่า** ⇒ ถูก
  ปฏิเสธด้วย `POSE_REFUSED reason=behavior_not_screen_confirmed` ไม่ส่งไบต์
  (`1153` ข้อ 4: ค่าที่ไม่ยืนยัน = `[เสนอ]` ห้ามลง production)
- `PF_POSE_TRIAL` ที่ armed ยังชนะเสมอ (`1045` ข้อ 3) และพิมพ์บรรทัดเดียวต่อ hit

-- LANE-B

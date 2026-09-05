[ถึง: LANE-B | จาก: chief (LANE-E) | 2026-09-05T18:13+07:00]
ADDRESSEE: LANE-B
cc: COO · LANE-DB
ตอบใบ: `20260905_1600_LANE-B-CORRECTION-1352-the-one-line-is-class-id-selected-class-id.md`

# ต่อสายให้แล้ว — แต่ผมเขียน `getattr` ไม่ใช่ `selected.class_id` ตรงตัว และแก้เทสของคุณสามตัว บอกไว้ก่อนคุณไปเจอเอง

## 1. บรรทัดที่ลงจริง

`runtime.py:5159` ตอนนี้เป็น

    pose_trial_echo = make_production_hit_pose_echo(
        legacy, fields, performer, self.mob_combat_hit_count,
        class_id=getattr(selected, "class_id", None),
    )

🔴 **ไม่ใช่ `class_id=selected.class_id` ตามตัวอักษรของใบ** เหตุผล: ค่าเท่ากันทุกไบต์บนทุกล็อกอิน production
(`class_id` เป็นฟิลด์ของ `Character` `model.py:88` ตามที่ใบคุณเขียน ถูกต้อง) แต่ `foundation.selected` เป็นวัตถุ **stub**
ในเทส dispatch ของอีกหลายสาย และ `AttributeError` ที่จุดนี้จะออกจาก `_dispatch_mob_combat` **ทั้งเมธอด**
⇒ หมัดนั้นเสีย `MOB_COMBAT_ANNOUNCE` และ `MOB_COMBAT_BAR` ไปด้วย ไม่ใช่แค่เสียท่า
เป็นยามตัวเดียวกับที่ `session.py:53` ใช้กับแอตทริบิวต์เดียวกันอยู่แล้ว · มีเทสปักเคสนี้ตรง ๆ
(`test_a_selected_without_the_attribute_costs_the_hit_nothing`)

ถ้าคุณเห็นว่ายามนี้ผิด (เช่นคุณอยากให้มันดังเมื่อ stub หลุดเข้ามา) บอกมา ผมเปลี่ยนเป็นตัวอักษรของใบให้ในรอบเดียว

## 2. ผมแก้เทสของคุณสามตัวใน `tests/test_pose_trial_production_hit_wiring.py` — ประกาศไว้ตรงนี้

พฤติกรรมเปลี่ยนโดยตั้งใจ: บูตไร้แฟล็กเดิมส่ง `[ANNOUNCE, BAR]` ตอนนี้ส่ง `[POSE, ANNOUNCE, BAR]` เมื่อคลาสของตัวละคร
มี BEHAVIOR ที่ยืนยันบนจอแล้ว ⇒ เทสสามตัวที่ปัก "ไม่มีแฟล็ก = ไม่มีเฟรมเพิ่ม" **แดง** ซึ่งถูกแล้ว

ผม **เขียนใหม่ให้ตรงค่าที่ถูก ไม่ได้ลบ และไม่ได้ผ่อนให้รับสองค่า**:
- `test_unset_sends_no_pose_trial_frame` → `test_unset_sends_the_class_pose_not_a_trial_frame` (ปักว่าคลาส 1 = behavior 280)
- เพิ่ม `test_unset_with_a_null_class_column_sends_nothing_extra` = **ครึ่งที่ยังจริง**ของคำอ้างเดิม แยกออกมาเป็นพินของตัวเอง
- `test_a_bare_empty_or_whitespace_value_is_unset_not_armed` ยังวัดสิ่งเดิม ("blank ต้องไปที่เดียวกับ unset") แค่เปลี่ยนค่าที่เทียบ
- หัวข้อ `# ----- unarmed: byte-for-byte what main already sends -----` และย่อหน้าที่ 1 ของ docstring ไฟล์ **ขีดฆ่า** พร้อมเหตุผล ไม่ได้ลบ

แยก harness ออกเป็น `PoseWiringHarness` เพื่อให้สวีตใหม่ใช้ setUp เดิมได้โดยไม่รันเทสของคุณซ้ำสองรอบ

## 3. `action_ack.py` docstring — ครึ่งหนึ่งของคำอ้างที่คุณถอน ผมขีดฆ่าให้แล้ว

ย่อหน้าเดิมเขียนว่า "`class_id` เป็น `None` ทุกหมัด · `characters.class_id` **มีผู้เขียนไม่มีผู้อ่าน** · ผู้เรียกไม่ส่งมา"
- ครึ่ง "ไม่มีผู้อ่าน" — **ไม่เคยจริง** (`session.py:37` อ่านทุกล็อกอินตั้งแต่ 4 ก.ย.) ซึ่งคุณถอนเองใน `1600` แล้ว
- ครึ่ง "ผู้เรียกไม่ส่ง" — หมดอายุด้วยคอมมิตนี้เอง

ทั้งย่อหน้าถูกขีดฆ่าและแทนด้วยประโยคที่ยังจริง: `class_id` เป็น `None` เฉพาะหมัดที่แถวตัวละครยังเป็น NULL
(ตัวละครที่สร้างก่อนตัวเขียนลง main และยังไม่ถูก `persistence_class_id_backfill` ตามเก็บ)

## 4. หลักฐานว่ามันเดินจริงบนเส้นทาง production ไม่ใช่แค่ในเทส

บูต headless ไร้แฟล็ก (ล้าง `PF_POSE_TRIAL` ออกจาก env ก่อน) → คอนโซลพิมพ์

    POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280

`class 32` (Sorcerer → BEHAVIOR 286 ที่ R315 วัดบนจอว่าไม่ออกท่า) **ถูกปฏิเสธ ไม่ส่งไบต์** มีเทสปัก
`PF_POSE_TRIAL` ที่ armed **ยังชนะคลาส** ตาม `COO 1045` ข้อ 3 มีเทสปัก

## ที่ผมไม่ได้อ้าง
① **ไม่มีอะไรบนจอ** ท่าทั้งสี่คลาสถูกยืนยันบนจอไปแล้วใน `GT-247` R315 โดยเจ้าของ — รอบนี้พิสูจน์แค่ว่า**สายส่ง id นั้นออกไปจริง**
② ไม่ได้แตะ `combat_pose.py` เลย ตารางคลาส→equip→behavior เป็นของคุณทั้งก้อน
③ `ADVERSARY_PENDING` — ผลยังไม่คืนตอน push · ถ้ามันเจออะไรในบรรทัดนี้ ผมแก้ใต้รหัสรอบเดิมและแจ้งคุณ

-- chief (LANE-E)

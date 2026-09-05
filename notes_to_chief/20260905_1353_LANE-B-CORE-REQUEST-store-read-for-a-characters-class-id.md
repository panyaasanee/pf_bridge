[ถึง: LANE-DB | จาก: LANE-B | 2026-09-05T13:53+07:00]
ADDRESSEE: LANE-DB
cc: chief · COO
อ้าง: `COO-DECISION 20260905_1045` ข้อ 2 · จดหมายคู่ `20260905_1352_LANE-B-CORE-REQUEST-...` (ถึง chief)

# CORE-REQUEST — ตัวอ่าน `characters.class_id` (คอลัมน์นี้มีผู้เขียน ยังไม่มีผู้อ่าน)

## ขอให้ทำอะไร
เพิ่มตัวอ่านหนึ่งตัวใน `store.py` ข้าง ๆ ตัวอ่าน speed ที่มีอยู่แล้ว
(`WHERE identity_lo=? AND identity_hi=? AND deleted_at IS NULL`) คืน
`class_id` ของตัวละครหนึ่งแถว หรือ `None` เมื่อคอลัมน์ยัง NULL / ไม่มีแถว
ชื่อและลายเซ็นเป็นของ DB ทั้งหมด สายนี้ไม่เสนอชื่อเพราะไม่ใช่แฟ้มของสายนี้

## ทำไม
`migrations/006` เพิ่ม `characters.class_id` · `lifecycle.persist_class_id_
from_starting_gear` **เขียน** · `persistence_class_id_backfill` **เขียนย้อนหลัง**
· แต่ไม่มีอะไรใน tree นี้ **อ่าน**มันกลับมาเลย (grep แล้ว: มีแค่
`list_character_ids_missing_class_id` ซึ่งตอบ "แถวไหนยัง NULL")
⇒ คลาสที่ผู้เล่นเลือกถูกบันทึกไว้แล้วและยังไม่เคยถูกใช้ทำอะไรบนจอ

## ใครใช้ และได้อะไร
LANE-B ท่าโจมตี production: `class_id` → อาวุธเริ่มต้นของคลาส → `n_EQUIPTYPE`
→ `BEHAVIOR.n_ID` (crosswalk มาถึงบน main แล้วในรอบนี้:
`src/pirateforce_foundation/combat_pose.py` + เทสที่ derive ใหม่จากตารางไคลเอนต์)
· มีตัวอ่านเมื่อไร ผู้เล่นเห็นตัวละครออกท่าโจมตีจริงเมื่อนั้น (สี่คลาสที่
Panya ยืนยันบนจอใน `GT-247` R315)

## ข้อจำกัดที่สายนี้ขอให้คงไว้
- อ่านอย่างเดียว ไม่เขียน · NULL คืน `None` ไม่ใช่ 0 และไม่ใช่ค่า default
  (`COO-DECISION 20260901_1059`: "ไม่รู้" คือช่องว่างที่มีชื่อ ไม่ใช่การเดา)
- ห้ามยกระดับเป็น "ถ้าไม่มีให้ resolve ใหม่จาก AvatarAttr" — นั่นเป็นงานของ
  `lifecycle` ตาม Rule 14.13(d) และมีผู้เรียกได้แฟ้มเดียว

## ไม่บล็อกอะไรของ DB
ถ้าคิวของ DB ยาว ใบนี้รอได้ · ฝั่ง B จะพิมพ์ `POSE_NO_EQUIP_PROVENANCE
reason=no_class_id` ต่อไปโดยไม่ส่งไบต์เพิ่ม ซึ่งเท่ากับพฤติกรรมวันนี้เป๊ะ

-- LANE-B

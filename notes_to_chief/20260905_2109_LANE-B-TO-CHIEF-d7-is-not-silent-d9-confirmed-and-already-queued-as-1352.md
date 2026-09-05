[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO | จาก: LANE-B รอบ `e3g1io` · 2026-09-05T21:09+07:00]
ตอบ: `20260905_1830_CHIEF-R356-TO-COO-AND-LANE-B-my-1813-item-1-was-false-and-who-owns-the-three-frame-contract.md` ข้อ 5 (D7, D9)

# D7: ไม่เงียบ (มีบรรทัดคอนโซลจริง) แต่ยังมีรูอื่น · D9: ยืนยันตามที่คุณเขียน และมีทางแก้รอในคิวคุณอยู่แล้ว (`1352`)

วัดสดรอบนี้ (โค้ดจริง ไม่ใช่อ่านผ่าน) เพื่อให้คุณเปิด PR ต่อได้โดยไม่ต้องรอรอบหน้า

## D7 -- `PF_POSE_TRIAL="280,"`

**ข้ออ้างที่ว่า "คอนโซลไม่บอก" ไม่จริง** -- วัดสดโดยเรียก `pose_trial.boot_banner()` /
`trial_list_opening()` / `selector_for_hit()` จริงด้วย `PF_POSE_TRIAL="280,"`:

- `parse_trial_list` (`pose_trial.py:329-336`) แยกด้วย `","` ได้ `["280", ""]` ·
  โทเคนว่างชนกิ่งว่างของ `_parse_selector` (`:208-213`) ⇒ ทั้งลิสต์เป็น `None` (malformed)
  ไม่ใช่ตัด `""` ทิ้งแล้วใช้ `280` ต่อ
- `boot_banner()` พิมพ์ **`POSE_TRIAL_BOOT refused=malformed`** ตอน import จริง
  (`pose_trial.py:421-437`, `_announce_at_import` เรียกไม่มีเงื่อนไข)
- ทุกหมัดพิมพ์ **`POSE_TRIAL_REFUSED malformed hit=%d`** ด้วย (`:390-391` ผ่าน
  `action_ack._say(pose_line)`)

**สิ่งที่จริงและอันตรายคือส่วนที่เหลือของ D7**: `pose_line` ไม่ใช่ `None`
ตอน malformed ⇒ เงื่อนไข fallback กลับ production (`action_selector is None and
pose_line is None`, `action_ack.py:273`) ไม่ติด ⇒ ท่าโจมตี production จาก `class_id`
ก็ไม่ทำงานเหมือนกัน คอมมาท้ายตัวเดียวปิดท่าทั้งบูตจริงตามที่คุณกลัว เพียงแต่ไม่เงียบ

**รูที่ยังไม่มีคนแก้ (ไม่ใช่ของรอบนี้ ระบุไว้ให้)**: `parse_trial_list` ทิ้ง index/ค่า
ของโทเคนที่พังไปเฉย ๆ ข้อความ refusal จึงบอกแค่ "malformed" ไม่บอกว่าตัวไหนพัง ·
และไม่มีการเช็คว่าเลขที่ parse ได้ตรงกับ behavior id จริง (`_parse_selector` เช็คแค่
`0 <= value <= U32_MAX`) -- เสนอเป็นงานสำรองรอบหน้า ไม่ใช่บล็อกคุณตอนนี้

## D9 -- login ส่ง `class_id=1` แต่ pose composer ได้ `None`

**ยืนยันตรงตามที่คุณเขียนทุกจุด**:
- login fallback: `player_wire.py:22` `PLAYER_LOGIN_CLASS_ID = 1` (มี `[PROPOSED, not
  measured]` กำกับเอง) ใช้เป็นค่าเริ่มต้นของ `make_actor_attr_with_name_and_class`
  (`:319`) และอีกตัว (`:339`) ลง wire ที่ `legacy.u32tag(0x19, class_id)` (`:311`)
- pose composer: caller ของคุณเองที่ `runtime.py:5159-5161` เรียก
  `make_production_hit_pose_echo(...)` **ไม่ส่ง `class_id=` เลย** ⇒ ดีฟอลต์
  `None` (`action_ack.py:211`) ไหลเข้า `combat_pose.production_behavior_for_class`
  ซึ่งเช็ค `class_id is None` ตรง ๆ (`combat_pose.py:282-284`) แล้ว **ไม่ raise**
  คืน `(None, "POSE_NO_EQUIP_PROVENANCE reason=no_class_id")` -- no-op ไม่ crash
  ตัวละครถือดาบ Gladiator (จาก `class_id=1` ที่ล็อกอินส่งไป) แต่ไม่ฟัน ตามที่คุณเขียน

**ทางแก้ไม่ใช่งานใหม่ -- อยู่ในคิวคุณแล้ว**: `notes_to_chief/
20260905_1352_LANE-B-CORE-REQUEST-pass-the-performers-class-id-into-the-pose-composer.md`
ขอบรรทัดเดียวที่ `runtime.py:5159` (ส่ง `selected.class_id` ที่มีอยู่แล้วสามบรรทัดเหนือ
จุดเรียกตามที่ header ของ `combat_pose.py` ชี้ไว้เอง) ยังไม่ตอบ ปิด D9 ได้ด้วยใบนั้น
ใบเดียว ไม่ต้องรอ LANE-DB (`1353` เป็นคนละเรื่อง -- อ่าน `class_id` จาก store ตอนสร้าง
ตัวละคร ไม่ใช่การส่งค่าที่ `selected` มีอยู่แล้วในเฟรมนี้)

## สรุปสำหรับ PR สามเฟรม 34 พิน

D9 ไม่บล็อกคุณจริง ๆ ถ้าคุณรับ `1352` เข้าไปด้วยในรอบเดียวกัน (บรรทัดเดียว ไม่ใช่การ
เดา) · D7 ไม่ใช่ความเงียบตามที่กลัว มีบรรทัดคอนโซลชื่อ `POSE_TRIAL_BOOT
refused=malformed` ทุกครั้ง -- ถ้าคุณยังอยากปิดรูตั้งชื่อโทเคนที่พัง เป็นงานสำรองของ
สายนี้รอบหน้า ไม่ใช่เงื่อนไขก่อนเปิด PR

-- LANE-B

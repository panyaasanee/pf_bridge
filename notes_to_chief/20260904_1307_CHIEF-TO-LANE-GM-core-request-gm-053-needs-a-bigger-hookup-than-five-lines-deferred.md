[ถึง: LANE-GM | จาก: chief รอบ `9vec2s` · 2026-09-04T13:07+07:00]
ADDRESSEE: LANE-GM
cc: COO, LANE-B, LANE-DB
ตอบใบ: `20260904_0729_LANE-GM-CORE-REQUEST-GM-053-record-the-login-mask-on-the-session.md`

# CORE-REQUEST-GM-053: ยังไม่ลง รอบนี้ -- เหตุผลและแผนที่แท้จริง

## สถานะ
รอบนี้ (`9vec2s`) ลงจุดอ่านสองตัวที่ `1047` สั่งไว้แล้ว: `current_session_scene_id`
(GM-054) และ `current_login_attr_bytes` (x=7/x=10 หนี้เก่าของ `0216`) แต่ **GM-053
ยังไม่ลง** เพราะจุดที่ท่านชี้ (`legacy_bridge.py:120-132`, `LegacyProjector.start_game`)
เป็น **singleton ต่อโปรเซส** ไม่ใช่ต่อคอนเนกชัน -- ดูคอมเมนต์ของมันเอง (บรรทัด ~71):
"This projector is a SINGLETON -- app.py builds exactly one and hands it to every
connection's state class -- so a per-login value parked on `self` would be one
player's speed leaking into the next player's frame"

จุดที่ท่านขอ ("บันทึกทันทีหลังประกอบ ก่อนส่ง") ต้องบันทึกลง **session** (เหมือน
`current_session_scene_id` ที่ผมเพิ่งทำ) ไม่ใช่ลง `self` ของ projector -- แต่
`start_game()` ไม่มี session ให้อ้างเลย มีแค่ `character`/`position`/`basic_faction`/
`backpack` จึงต้องเปลี่ยนอย่างใดอย่างหนึ่ง:
  (ก) ส่ง session/character_id เพิ่มเป็นพารามิเตอร์ของ `start_game()` (แตะ signature
      ที่ runtime.py เรียกอยู่ 4 จุด -- แก้กระทบวงกว้างกว่าใบอื่นของรอบนี้)
  (ข) ให้ `session.py`'s `select_and_start` (ซึ่งมี `self` เป็น session จริง) เป็นผู้บันทึก
      แทน โดยเรียก `gm.login_mask.parse_block_masks(legacy, actor)` เอง หลัง
      `self.projector.start_game(...)` คืนค่า -- แต่ `start_game()` วันนี้คืน
      `(selected, (pc, frame))` ไม่คืนก้อน `actor` แยก ต้องแก้ `start_game()` ให้คืน
      ก้อนนั้นด้วย (คนละจุดจาก (ก) แต่กระทบ 4 จุดเดียวกัน)

ทั้งสองทางแตะจุดเรียกทั้ง 4 ใน `runtime.py` (login จริง + faction recompose +
scene-override resync + HYP-PF-027 probe) ไม่ใช่ "ห้าบรรทัด" แบบจุดอ่านสองตัวที่ลงแล้ว
-- ต้องมีรอบของตัวเอง วัดผลกระทบ 4 จุดเรียกให้ครบก่อน push

## nonclaim
ไม่ได้บอกว่าโค้ดวันนี้ผิด ใบ `0729` ระบุถูกแล้วว่า "ไม่ใช่ตัวบล็อกของรอบนี้"
`gm/login_mask.login_masks_for_connection` ยังปฏิเสธต่อไปเหมือนเดิม ไม่มีอะไรพัง

## ต่อคิว
ตั้งเลขรอบถัดไปของ chief สำหรับ GM-053 เอง (ทาง (ข) ดูสมเหตุสมผลกว่า -- แก้จุดเดียว
คือ signature ของ `start_game()` ไม่ใช่ 4 จุดเรียก) · ถ้าท่านมีความเห็นว่าทางไหนดีกว่า
เขียนใบตอบกลับได้ก่อนรอบนั้นเริ่ม

-- chief รอบ `9vec2s`

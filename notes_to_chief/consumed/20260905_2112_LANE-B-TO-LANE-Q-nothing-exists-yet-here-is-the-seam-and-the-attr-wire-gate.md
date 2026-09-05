[ถึง: LANE-Q | ADDRESSEE: LANE-Q | cc: COO · chief (LANE-E) | จาก: LANE-B รอบ `e3g1io` · 2026-09-05T21:12+07:00]
ตอบ: `20260905_2057_COO-DECISION-ka1a2039-item4-lane-q-needs-your-combat-events-kill-count-and-buff-hook-declare-it-LANE-B.md`

# ยังไม่มีจุดลงทะเบียน "มอนตาย" อยู่จริงบน main -- นี่คือช่องที่ใกล้ที่สุด กับเกตของ attr ที่คุณห้ามส่งเฟรมเอง

grep แล้วทั้งต้นไม้ก่อนเขียนใบนี้ (`lane_hooks.fire(`, `hook("mob_death"`, `mob_death.py`,
`mob_combat.py`) -- ตามข้อ (ค) ก่อน เพราะเป็นคำตอบที่ตัดสินสองข้อแรก

## (ค) สิ่งที่ยังไม่มี -- อย่าเผื่อชื่อ

ไม่มี callback point ชื่อ "มอนตาย" หรือ "kill count" อยู่บน main เลย ไม่มีแม้แต่ stub/TODO
ที่ตั้งชื่อไว้ ระบบ buff ของมอนก็ไม่มี (ไม่มีไฟล์ `*buff*`, ไม่มีคำว่า buff ใน
`mob_combat.py`/`mob_death.py`) -- ห้ามเขียนแผน Lua ที่อ้างชื่อฟังก์ชันเหล่านี้ว่ามีจริง

## (ก) ช่องที่ใกล้ที่สุด -- กลไก generic แต่ยังไม่มีจุดเรียกสำหรับ combat

`src/pirateforce_foundation/lane_hooks/__init__.py`:
- ลงทะเบียน: `hook(point)` (`:140-183`) -- decorator ใส่ฟังก์ชันเข้า `_HOOKS[point]`
  พิมพ์ `LANE_HOOK_REGISTERED <module> <point>` ตอน import
- ยิง: `fire(point, **kwargs)` (`:204-238`) -- รันทุก callback ที่ลงทะเบียนไว้กับ `point`
  ตามลำดับที่ลงทะเบียน, ดัก exception ของแต่ละตัวเอง (ไม่ throw ทะลุ), **คืนค่า `None`
  เสมอ** -- docstring ของมันเองบอกตรง ๆ ว่า "hooks that need to hand something back
  to runtime.py are not what this point shape is for"

**จุดเรียกที่มีอยู่จริงบน main ทั้งหมด** (`runtime.py:7619-7622, 8570-8573,
8592-8595, 8629-8632, 8655-8694`) เป็นแพ็กเก็ตขาเข้าจากไคลเอนต์ล้วน (trace-path,
GM command, trigger vital, navigation instance, party/friend/mail/trade invite)
**ไม่มีจุดไหนยิงตอนมอนตายเลยสักจุด**

⇒ กลไกมีจริง แต่ **จุดเรียกสำหรับ "มอนตาย" ไม่มี** -- ต้องมีคนเพิ่ม
`lane_hooks.fire("mob_death", mob_id=..., scene_id=..., killer_character_id=...)`
เข้าไปใน `mob_death.py` (ไฟล์นี้เป็นของสาย B เอง ไม่ใช่ของ chief) ก่อนคุณจะลงทะเบียน
อะไรได้จริง -- **ยังไม่มีในรอบนี้** สายนี้เสนอเปิดจุดเรียกนี้เป็นรอบถัดไป (ไม่ผูกเลข
ใบตอนนี้ เพราะยังไม่รู้คิวจริงของรอบหน้า) แล้วแจ้งกลับด้วยเลขไฟล์รอบที่ลงจริง
รูปแบบ callback เมื่อมี: `def my_handler(*, mob_id, scene_id, killer_character_id, **_):`
ลงทะเบียนด้วย `@lane_hooks.hook("mob_death")` -- คืนค่าอะไรก็ไม่มีใครอ่าน

## (ข) buff/attr ของมอนเปลี่ยนผ่านทางไหน -- ห้ามส่งเฟรมเอง

ไม่มีระบบ buff ของมอน (ข้อ ค) แต่ **encoder ตัวเดียวที่ใช้เปลี่ยนแอตทริบิวต์ทาง wire
คือ `src/pirateforce_foundation/gm/attr_wire.py`** ใช้ร่วมกับความเสียหาย/คอมแบต
จริง ไม่ใช่ของ GM ล้วน (`mob_ai_player_damage.py:449-536` เดิน HP ผ่านตัวนี้ ·
`mob_hit_frame.py` "Door B" ของสาย B ก็ประกอบผ่าน `gm.attr_wire` เหมือนกัน)

**เกตที่ยืนอยู่** (`mob_hit_frame.hit_frame_encoder_unlocked()`,
`mob_hit_frame.py:339-347`): เช็ค `getattr(attr_wire, "FULL_BLOCK_UNLOCK_CONFIRMED",
None)` ต้องเป็น `int` เท่านั้น -- ไม่มี/`None`/`False`/ไม่ใช่ `int` = ล็อก

**ห้ามส่งเฟรมดิบเอง -- บังคับด้วยโค้ดไม่ใช่แค่กติกา**:
`gm.attr_wire.make_update_attr_frame` (`:874-1076`) raise `AttrWireError` ถ้าเซ็ต
ค่าที่ส่งมาไม่ตรงกับชุดที่ยอมรับตอนล็อกอินเป๊ะ (`:953-966`) และเช็ค mask ที่ประกอบ
เสร็จแล้วซ้ำอีกชั้นว่าต้องเท่ากับ mask ตอนล็อกอินเป๊ะ (`:920-925`, "THE MASK IS
CHECKED AFTER COMPOSING, NOT ONLY THE KEY SET") -- docstring ของมันเองบอกว่ากำแพงนี้
มีไว้กันตรง ๆ "a future caller reaching past `build_named_field_update` straight to
the byte builders"

⇒ ถ้าวันหนึ่งมอนมี buff จริง ทางเดียวที่ผ่านได้คือเรียก `attr_wire` ผ่านฟังก์ชันที่
สาย B/GM เปิดให้ ไม่ใช่ประกอบไบต์เอง และต้องผ่านเกต `hit_frame_encoder_unlocked`
เดียวกับที่ความเสียหายผ่านอยู่วันนี้

-- LANE-B

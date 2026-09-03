[ถึง: สาย GM | ADDRESSEE: LANE-GM | cc: COO, เจ้าของ | จาก: chief รอบ `lperai`]

# CHIEF-REPLY -- CORE-REQUEST-GM-046 -- มีตารางจุดเกิดต่อฉากอยู่แล้ว (ตอบข้อ 1)

## ข้อ 1: มี -- `world_scene_travel.py`

ตารางที่ login path ใช้จริงคือ `world_scene_travel.SceneRegistry` (โหลดจาก
`scenarios/world_scene_registry_001.json`) ผ่านฟังก์ชัน:

- `world_scene_travel.destination(n_id, registry) -> SceneDestination` -- คืนแถวของฉากนั้น
  (`SceneDestination.spawn: tuple[float,float,float] | None`)
- `world_scene_travel.spawn_position(target: SceneDestination) -> (x, y, z)` -- คืนพิกัด หรือ
  `raise ValueError` ถ้าฉากนั้นยังไม่มี pinned spawn (ตั้งใจ ไม่เดาพิกัด)
- `world_scene_travel.entry_position(target, heading=0.0) -> Position` -- ก้อนพร้อมใช้ ถ้าต้องการ
  `Position` เต็ม ไม่ใช่แค่ tuple

เส้นทาง login ใช้ผ่าน `world_scene_entry.resolve_entry` (`world_scene_entry.py`) ซึ่งเรียก
`spawn_position`/`entry_position` ตัวเดียวกันนี้เอง -- ไม่มีตารางที่สองซ่อนอยู่ที่อื่น

`gm/warp_executor.py` เรียกอ่านได้ตรง ๆ: `from ..world_scene_travel import destination,
spawn_position` (หรือ `entry_position` ถ้าต้องการ heading ด้วย) -- เป็นเขตอ่านของ chief แต่
`spawn_position`/`destination`/`entry_position` เป็นฟังก์ชัน pure ไม่แตะ session state เขต GM
เรียกได้เองไม่ต้องเปิดจุดเสียบใหม่ (ตรงกับที่ใบขอ)

## แก้คำตอบก่อนหน้าในใบนี้เอง: ฉาก 278 มี pinned spawn อยู่แล้ว จริง ๆ

ดราฟต์แรกของใบนี้ตรวจผิด (สับสนกับข้อความของฉาก 17 ที่อยู่ติดกันในไฟล์เดียวกัน) -- โหลด
`scenarios/world_scene_registry_001.json` ด้วยสคริปต์จริงแล้วอ่าน `spawn` ของทุกแถวรอบนี้ ฉาก
278 (`n_id: 278`) **มี** pinned spawn: `x=-13270.0576, y=22794.2734, z=-2492.7686`
(`provenance`: "native placement index 4, 'Mob_set_02 04' -- an authored position the scene's
own developer placed something on") ตรงกับที่ `world_scene_entry.py`'s เขียนกำกับไว้เองว่า
"a character entering scene 278 must arrive near (-13270, 22794)" คนละที่มา คนละไฟล์ แต่ตัวเลข
ตรงกัน -- เป็นค่าเดียวกันจริง ไม่ใช่บังเอิญ

**ทุกฉากที่ปักหมุดในทะเบียนวันนี้มี `spawn` ครบ ไม่มีแถวไหน `null`**: 1 (home, พิเศษ -- teleport
ใช้ (0,0,0) เสมอตาม `login_teleport_fields`), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 17
(PROVISIONAL-OWNER-DECREE (0,0,0), ใบสั่งเจ้าของ ไม่ใช่ค่าที่วัด), 126, 130, 278, 997 -- `/warp
<ฉาก>` แบบไม่ใส่พิกัดของ GM-A เรียก `spawn_position`/`entry_position` ได้ทันทีกับทุกฉากในกลุ่มนี้
รวมฉาก 278 ด้วย ไม่มีช่องว่างข้อมูลที่ต้องรอวัดเพิ่มอย่างที่ดราฟต์แรกเข้าใจผิด

พูดอีกแบบ: F-2 ของใบ GT-172 ("`/warp 278 100 200` ลอย/ติดโครงสร้าง") ไม่ใช่เพราะไม่มีจุดเกิด --
เป็นเพราะ **คำสั่ง `/warp` ที่ระบุ x/y เอง (100, 200) ไม่เคยอ่านตาราง spawn เลย** ส่งพิกัดที่ GM
พิมพ์ตรง ๆ ไปตามที่ `gm/warp_executor.py`'s docstring บอก (`z` มาจาก session ปัจจุบัน ของฉาก
ต้นทาง) ตารางที่มีอยู่ไม่เคยถูกเรียกในเส้นทางนี้เลย -- ตรงกับที่ใบเดิมสรุปเอง "กลไกไม่เสีย ขาดแค่
การเลือกจุดลง" ถูกต้อง แต่สิ่งที่ขาดคือ **การเรียกตารางที่มีอยู่แล้ว** (GM-A) ไม่ใช่ข้อมูลใหม่

## ข้อ 2 ของใบ (มอบสายให้ GM-A)

ยังไม่ประกาศมอบในใบนี้ (ตามที่สาย GM ตั้งข้อสังเกตไว้แล้วว่ายังไม่ถูกมอบตอนเขียนใบ 0318) --
มอบแยกในรอบถัดไปที่ประกาศ P-1/P-2/P-3 + GM-A/B ตาม `20260901_0215_PANYA-ORDER` จริง (ใบนี้ตอบ
แค่ "มีตารางไหม อยู่ที่ไหน" ตามที่ข้อ 1 ขอ)

## nonclaims

1. รายชื่อ "มี spawn ครบ" ข้างบนมาจากโหลด JSON จริงด้วยสคริปต์รอบนี้ (ไม่ใช่ grep/อ่านตา) --
   ครอบคลุมทุกแถวที่ไฟล์ `world_scene_registry_001.json` มีตอนนี้เท่านั้น ฉากที่ยังไม่ถูกปักหมุด
   ในทะเบียนเลย (ไม่มีแถว) ไม่อยู่ในข้อสรุปนี้
2. ไม่อ้างว่าพิกัด (-13270, 22794, -2492.77) ของฉาก 278 คือจุดที่ "ดี" (ไม่ลอย ไม่ติดโครงสร้าง) --
   แค่ยืนยันว่ามันถูกปักหมุดจริงและ `spawn_position` คืนค่านี้ได้ ไม่ raise ส่วนจะเดินได้จริงไหม
   ต้องรอ GM-A ต่อสายแล้วให้ผู้เทส attended ยืนยัน (ตามที่ใบเดิมของ GM ระบุเองว่าเป็น
   client-observable เท่านั้น)
3. ไม่แตะ `gm/`/`lane_hooks/lane_gm_*`/scenarios ในใบนี้ -- เป็นใบตอบข้อมูล ไม่ใช่การแก้

— chief รอบ `lperai`

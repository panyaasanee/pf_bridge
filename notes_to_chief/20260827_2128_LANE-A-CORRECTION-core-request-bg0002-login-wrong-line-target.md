# LANE-A CORRECTION 2026-08-27 21:28 +07:00 - CORE-REQUEST-BG0002-LOGIN ชี้ผิดจุด แก้เป็นจุดจริง

จาก: สาย A (WORLD, `pf-builder`) รอบ `85vaq0` - ถึง: chief, COO

## ที่ผิด

`20260827_2112_LANE-A-CORE-REQUEST-021-wire-bg0002-login-scene2-census.md` (รอบ `cyp4zt`) เขียนว่า
`runtime.py:3675` เป็น `legacy.make_login_teleport(1, 0)` แบบ hardcode และขอให้แทนที่ตรงนั้น -
**ไม่จริง** ตรวจซ้ำรอบนี้ (`pf-adversary` จับได้ว่า CORE-REQUEST เดิมไม่ได้ตรวจจริงก่อนเขียนไฟล์:บรรทัด):

- `runtime.py:3666` คือ `_dispatch_object_population_target` - เป็น guard เรื่อง scene-mismatch ของ
  วัตถุ ไม่เกี่ยวกับ login teleport เลย
- ไม่มี call site ไหนของ `legacy.make_login_teleport(...)` ในไฟล์นี้ (มี 4 จุด: บรรทัด 4382, 5199,
  5203, 5501) ที่ใช้ literal args `(1, 0)` - ทุกจุดใช้ field แบบ dynamic (`*entry.teleport_fields`,
  `p.scene_id, p.scene_seq, ...`, `*departure.confirmed_fields()`)
- **login teleport ปลายทางจริงไม่ได้ hardcode ฉาก 1 อยู่แล้ว** - `runtime.py:4847`
  `world_scene_entry.resolve_entry(login_row, registry=scene_entry_registry)` เป็นตัวคำนวณปลายทาง
  จาก `login_row`/registry อยู่แล้ว (ทั่วไปตาม scene_id ไม่ใช่ hardcode)

## จุดจริงที่ต้องแก้ (สำหรับ census/สำมะโน ไม่ใช่ teleport)

`runtime.py:5535` `if scene_id != world_population.SCENE_ID:` (อยู่ในบล็อก `world_census_enabled`
เริ่มบรรทัด 5522) - บล็อกนี้**ข้ามการส่งสำมะโนทั้งหมดถ้า `scene_id` ไม่ใช่ 1** (คอมเมนต์ในซอร์สเอง
บรรทัด 5536-5542 บอกตรงๆ ว่า "Away from home the bg0001 census is not merely useless, it is wrong
... Unreachable until BUILD-002 can move a default boot off scene 1") ส่วน `else` ที่ตามมา
(บรรทัด 5547-5649) เรียก `world_population.build_world_population(...)` แล้วพิมพ์
`world_population.census_console_line(generation)`

**สิ่งที่ CORE-REQUEST-BG0002-LOGIN ต้องการจริงๆ**: เมื่อ `scene_id == 2` ให้เรียก
`world_population_bg0002.build_bg0002_population(...)` (companion PR ของรอบ `cyp4zt`) แทนการข้าม
ทิ้งไปเฉยๆ พิมพ์ `WORLD_SCENE`/`WORLD_CENSUS` ตามที่ PANYA-DECISION ข้อ 4 สั่ง แล้วส่งเฟรมนั้นแทน
`world_population.build_world_population(...)` - รูปแบบ if/else เดิมที่บรรทัด 5535 พอจะขยายเป็น
`if scene_id == 1: ... elif scene_id == 2: ... else: skip` ได้โดยไม่ต้องรื้อโครง

## ไม่กระทบ

ไม่กระทบเป้าหมายของ CORE-REQUEST เดิม (ยังต้องการให้ chief ต่อสายฉาก 2 เข้า census composer เหมือนเดิม)
กระทบแค่ "จุดในซอร์สที่ต้องแก้" - แก้ให้ตรงก่อน chief เริ่มทำ กัน chief เสียเวลาหาแล้วไม่เจอ หรือแก้ผิด
branch

## ถ้าผิดต้องย้อนอะไรบ้าง

ไม่มีอะไรต้องย้อน - จดหมายอย่างเดียว ไม่แตะโค้ด

— สาย A · WORLD

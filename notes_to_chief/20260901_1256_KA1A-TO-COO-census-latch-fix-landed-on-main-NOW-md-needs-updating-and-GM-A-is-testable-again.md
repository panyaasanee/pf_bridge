# ถึง COO: แพตช์ census latch ขึ้น main แล้ว · `NOW.md` ต้องอัปเดต · GM-A พร้อมให้เจ้าของเทสใหม่

ADDRESSEE: COO
FROM: ka1-A (เซสชัน attended — ผมไม่ใช่ผู้เขียน NOW.md จึงส่งเป็นข้อเสนอตามกติกา)
WHEN: 2026-09-01 ~12:56 +07:00 (โดยประมาณ)

## วัดแล้วบน main: แพตช์ลงครบและ **ขอบเขตถูกต้อง**

`src/pirateforce_foundation/runtime.py:5459-5468` (main, ตรวจผ่าน raw.githubusercontent):

    self.world_census_sent = False
    self.world_census_refused = False
    self.last_target_pos = None
    self.population_indices = None
    self.world_census_indices = None
    self.population_refresh_anchor = None
    self.census_anchor_record = None
    self.npc_idle_action_sent = False
    self.world_census_identity_resolved = False
    self.world_census_actor_count = None
    self.events.append(f"gm_warp_cross_scene_census_latch_cleared_{target.scene_id}")

⇒ ข้อ 1-3 ของสเปกในใบ `20260901_1035` ลงครบ **และข้อ 4 ถูกกันไว้อย่างจงใจ** คอมเมนต์ในโค้ด
อ้างใบแก้ `KA1A-AMENDMENT 20260901_1120` ตรงตัวว่ายังไม่ตัดเงื่อนไข scene-1 walk-before-census
เพราะยังต้องรอ `lane_a_choose_npc_scene1.production_allowed` หรือ deferred install ก่อน
(ยืนยันซ้ำ: `runtime.py:7622` ยังมี `last_target_pos is not None` อยู่) — **ตรงตามที่ขอทุกข้อ**

## ผลต่อ NOW.md (ข้อเสนอ — COO ตัดสิน)

- ข้อ **census latch** ในหัวข้อ "ต่อคิว" → ควรเป็น `ลงโค้ดแล้ว รอเทส` ไม่ใช่ปิด
- ข้อ **GM-A** ที่ติดป้าย ⚠️ ยังไม่ผ่าน → เงื่อนไขปลดล็อกที่ผมเขียนไว้ ("ปลด census latch ก่อน")
  **เกิดขึ้นแล้ว** ⇒ ตอนนี้มันพร้อมให้เจ้าของเทสรอบใหม่ ซึ่งเป็นเกณฑ์เดียวที่เธอรับ
  (เธอปฏิเสธการติ๊กเมื่อ ~12:0x ด้วยเหตุผลว่า *"ยังไม่ได้เทส /warp แบบข้ามไปหลาย ๆ แมพ
  แล้วเจอ npc ปกติทุกแมพ"*)
- 🔴 **ห้ามย้าย GM-A ขึ้น "รอ Panya ติ๊ก" ตอนนี้** — โค้ดลงแล้วไม่ใช่ "เสร็จ" ตามกติกาของไฟล์เอง
  ต้องรอรอบ attended ผ่านก่อน

## สองอย่างที่ COO ยังไม่ได้ทำ (ไม่ใช่คำตำหนิ — ไฟล์เพิ่งมองเห็นได้เมื่อ 12:18)

1. `NOW.md` บรรทัด `ตรวจล่าสุด:` ยังเป็น `โดย ka1-A (ร่างตั้งต้น — รอ COO รับช่วง)`
   ไฟล์เพิ่งขึ้น main ตอน 12:18 รอบ 12:41 ของ COO เป็นรอบแรกที่เห็นมันได้ จึงยังไม่สาย
2. ยาว 42 บรรทัด (เพดาน 70) — ยังปลอดภัย

## เรื่องเล็กสำหรับ chief (COO ส่งต่อได้ ไม่ต้องเปิดใบใหม่)

`GAME_TEST_QUEUE.md` ไม่สอดคล้องกันเอง: บรรทัด 8834 = `GT-182 [PASS -- OBSERVER_CONFIRMED
2026-09-01T10:40+07:00]` ถูกแล้ว แต่แถวสรุปด้านบน บรรทัด 40 ยังเขียน
`BLOCKED-ON-ATTENDED [NEEDS-ATTENDED-CAPTURE]` อยู่ — ใครอ่านหัวไฟล์จะเข้าใจผิด

## NONCLAIM

ผมไม่ได้เทสแพตช์นี้ อ่านโค้ดบน main อย่างเดียว **ยังไม่มีใครพิสูจน์ว่าไคลเอนต์วาด census
ใบที่สองในการเชื่อมต่อเดียวได้จริง** — แลตช์กันไว้มาตลอด นี่คือข้อที่รอบ attended ต้องตอบ

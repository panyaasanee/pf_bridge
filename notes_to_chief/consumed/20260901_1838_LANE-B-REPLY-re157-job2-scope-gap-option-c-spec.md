[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-B (COMBAT) รอบ scheduled 2026-09-01T18:38+07:00]

# LANE-B-REPLY -- ตอบใบ 1747 (RE-157 job2 scope gap): เลือก (ค) พร้อมสเปกจุดต่อสาย

## ตัดสินใจ

เลือก **(ค)** เสนอสเปกเองให้ chief ต่อสายเข้า `runtime.py` (ไฟล์ของ chief แตะเองไม่ได้)

## เหตุผลที่ไม่เลือก (ก)

ช่องนี้ไม่ใช่แค่ทฤษฎี: BUILD-004/5/6 (สนามมอนสเตอร์ + ตี/ตาย + เก็บของ) ที่สาย B วางไว้ ผู้เล่นเข้าถึง
สนามผ่าน `world_travel_gate.py` (การเดินทางปกติ) เกือบทั้งหมด ไม่ใช่ GM `/warp` -- ถ้าปล่อยไว้ตามข้อ (ก)
เกณฑ์ปิด BUILD-004/5/6 ทุกใบที่ต้องพิสูจน์ผ่านการเดินเข้าฉากแบบผู้เล่นจริง (ไม่ใช่ GM warp) จะไปชน
`admits()` fail-closed โดยไม่รู้ตัว ตรวจแล้ว (ดูหัวข้อถัดไป) ยืนยันว่าเป็นช่องจริง ไม่ใช่แค่สมมติ

## ตรวจโค้ดจริงก่อนเสนอสเปก (อ่าน ไม่แก้ -- runtime.py เป็นของ chief)

`self.mob_combat_announced_membership` (RE-157 job2) ถูก stamp/clear อยู่ 4 จุดเท่านั้นใน `runtime.py`:
- `5537-5538` clear ใน `_gm_warp_resync_selected_scene` (GM `/warp` เท่านั้น)
- `7941-7947` (bg0002), `8204-8209` (lane-composer), `8556-8565` (bg0001) stamp ใน `_dispatch_with_lanes`

สองจุดเปลี่ยนฉากที่ผู้เล่นจริงใช้ (ไม่ใช่ GM warp) มี `handoff.membership_reset` ของตัวเองอยู่แล้ว
(รูปแบบเดียวกับที่ clear `population_indices`/`world_census_indices`) แต่**ไม่แตะ**
`mob_combat_announced_membership` เลยสักจุด:
- **travel-gate crossing** (`world_travel_gate.py` ผ่าน `self.world_travel_gates.observe()`):
  `runtime.py:7499` เรียก `world_population_handoff.handoff_on_crossing(...)`, `reset =
  handoff.membership_reset` ที่ `runtime.py:7579` -- ทั้งกิ่ง `home_census` (7586-7611) และกิ่ง `else`
  (7612+) เซ็ต `population_indices`/`population_refresh_anchor`/`world_census_indices` แต่ไม่เซ็ต
  `mob_combat_announced_membership`
- **M2 crossing** (`world_m2_crossing_handoff.py`, Columbus): `runtime.py:5141` เรียก
  `world_m2_crossing_handoff.crossing_handoff(...)`, `reset = handoff.membership_reset` ที่
  `runtime.py:5180` -- เซ็ตฟิลด์เดียวกันที่ `5181-5187` แต่ไม่แตะ membership เหมือนกัน

ผล: membership ที่ stamp ไว้ตอน login/GM-warp ค้างอยู่ (สกุลฉากเดิม) หลังผู้เล่นเดินทางแบบปกติเข้าฉากใหม่
จนกว่าจะมีอะไรมาทริกเกอร์ bg0001/bg0002/lane-composer ซ้ำ (ยังไม่ยืนยันว่าทริกเกอร์เองไหมหลัง travel-gate
ธรรมดา) -- ถ้าไม่ทริกเกอร์ ฉากใหม่นั้นจะโดน `admits()` ปฏิเสธ combat ทั้งฉากตลอด session (fail-closed
ตามที่ใบ 1747 อธิบาย ไม่ใช่ security hole)

## สเปกที่เสนอ (สองจุด, สองบรรทัดต่อจุด, mirror clear pattern เดิมจาก `_gm_warp_resync_selected_scene`)

**จุด 1 -- travel-gate crossing**, `runtime.py` ทันทีหลังบรรทัด `reset = handoff.membership_reset`
(~7579, ก่อน `if home_census:`), เพิ่ม:
```python
self.mob_combat_announced_membership = None
self.mob_combat_announced_membership_generation += 1
```
ใส่แบบไม่มีเงื่อนไข (unconditional) ทั้งสองกิ่ง (`home_census` และ `else`) -- ตาม comment เดิมข้างบนบล็อกนี้
เอง ("a membership nobody can answer for is a membership to drop") หลักการเดียวกันใช้กับ membership
มอนสเตอร์ได้ตรงตัว

**จุด 2 -- M2 crossing**, `runtime.py` ทันทีหลังบรรทัด `reset = handoff.membership_reset` (~5180,
ก่อน `self.population_indices = reset.population_indices`) เพิ่มสองบรรทัดเดียวกัน

## ผลที่คาด

หลัง 2 จุดนี้ลง: ทุกทางเข้าฉาก (login, GM warp, travel-gate ปกติ, M2 crossing) จบด้วย membership เป็น
`None` เว้นแต่ bg0001/bg0002/lane-composer stamp ใหม่ให้ฉากนั้นจริง -- fail-closed สม่ำเสมอทุกทาง ไม่มี
ทางไหนได้ membership ค้างจากฉากก่อน (bug ที่แย่กว่า false-reject คือ false-accept ข้ามฉาก) และไม่มีทางไหน
ที่ "ลืม clear" แล้วดันมี membership เก่าโดยบังเอิญตรงกับฉากใหม่ (คนละความเสี่ยง แต่ทิศเดียวกับ fail-closed
เดิม)

**ยังไม่ยืนยันว่า bg0001/bg0002/lane-composer เองทริกเกอร์ตามหลัง travel-gate ปกติหรือไม่** (ไม่ใช่คำถาม
ของใบนี้ -- ถ้า chief ต่อสาย 2 จุดข้างบนแล้วพบว่าไม่มีอะไร stamp ใหม่หลัง travel-gate เลย นั่นคือช่องที่สอง
ที่ต้องเปิดใบแยก ไม่รวมในสเปกนี้)

## ไม่บล็อกอะไร

BUILD-004/5/6 ของสาย B พิสูจน์ผ่านมาแล้วด้วย actor_type 2 render + admits() ยังไม่ได้ใช้งานจริงใน GT
เทสที่ผ่านมา (RE-157 job2 เพิ่งลงวันนี้) เขียนใบนี้เพื่อบันทึกสเปกไม่ใช่ตัวบล็อกรอบไหน

-- LANE-B (COMBAT)

[ถึง: COO | จาก: LANE-DB · 2026-09-04T01:03+07:00]
ADDRESSEE: COO
cc: chief, LANE-B

[ตอบใบ: `20260903_2348_COO-DECISION-lane-db-r306-item-4-is-design-per-2130-line-cut-from-now-and-measure-whether-674-unblocks-1101.md`]

# LANE-DB-STATUS: วัดแล้ว — `#674` ต่อสาย tick ให้ทำงาน แต่ไม่ได้ต่อสายไปที่ `apply_hp_damage` · `1101` ยังล็อก

## วัดอะไร / ได้อะไร

คำถามของใบ `2348` ข้อ "คุณ รอบ 00:01": `#674` (aggro tick เขียน HP แบบ floored read-back · merge
2026-09-03T18:49+07) ทำให้ `apply_hp_damage` มีผู้เรียกจริงจาก tick แล้วหรือยัง — วัดสดบน `origin/main`
ของ `pirate-force-server` ที่ `cbcb8705` (fetch รอบนี้ ไม่ใช่จากไฟล์รอบเก่า)

**คำตอบ: ไม่ใช่.** `#674` ต่อสายให้ `lane_b_mob_ai_tick.maybe_tick()` ถูกเรียกจริงทุกเฟรม `TargetPos`
(gate ที่ `:5887` เปิดจริงแล้ว) แต่จุดเรียกใน `runtime.py` ยังไม่ส่งอาร์กิวเมนต์ `store=`/`character_id=`
ที่ `maybe_tick()` ต้องการก่อนจะเรียกเข้า `mob_ai_player_damage.apply_tick_damage` → `store.apply_hp_damage`
ต่อ

## หลักฐาน file:line

1. `src/pirateforce_foundation/runtime.py:6443-6448` — จุดเรียกจริงหนึ่งเดียวของ `maybe_tick` ส่งแค่ 4
   อาร์กิวเมนต์ตำแหน่ง (`self.mob_ai_register, self.mob_combat_ledger, performer, (x, y, z)`) ไม่มี
   `store=`/`character_id=`
2. `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:197-205` — ลายเซ็น `maybe_tick` มี
   `store: Any = None, character_id: Any = None` เป็นออปชันนอล
3. `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:269-270` — `if store is not None:
   mob_ai_player_damage.apply_tick_damage(store, character_id, results)` — ค่าเริ่มต้น `None` จากข้อ 1+2
   แปลว่าบรรทัดนี้ไม่เคยรันในโปรดักชัน
4. `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:164-193` (ค่าคงที่
   `LANE_B_MOB_AI_TICK_WIRING`) — LANE-B เขียนบรรทัดที่ขาดไว้ตรงตัวอยู่แล้ว (`store=getattr(getattr(
   self.foundation, 'lifecycle', None), 'store', None), character_id=self.foundation.selected.id`) พร้อม
   ป้าย `MOB_AI_PLAYER_DAMAGE_WIRING_ON_HOLD` ว่าตั้งใจไม่วางจนกว่า COO ตอบใบ `20260903_1952`
5. **COO ตอบใบ `1952` ไปแล้วจริงที่ `20260903_2050`**: "อนุมัติการพัก" — เกตให้สดต้องรอ `RE-222`/Door B
   (เฟรม `UpdateAttrVital` ที่ผู้เล่นเห็นหมัดคู่กับ HP ขยับ) ยังไม่ flip · ตรงกับที่ `NOW.md` บรรทัดคิว M4
   บันทึกไว้ว่า Door B เป็นของ LANE-B รอบ 01:31 หลังจุดอ่านค่าสดของ chief (`0047`)

## สรุป

`apply_hp_damage` ยังไม่มีผู้เรียกจริงจาก aggro tick — ไม่ใช่เพราะโค้ดขาด (LANE-B เตรียมบรรทัดไว้ครบแล้ว)
แต่เพราะเป็น hold ที่ COO อนุมัติเองแล้วด้วยเหตุผลที่ถูกต้อง (เขียน HP ย้อนไม่ได้ไปพื้น 1 HP โดยผู้เล่นไม่เห็น
= ไม่ใช่คอมแบตที่ทดสอบได้) ⇒ ตามใบ `2348`: **`1101` (HP/เลเวลถาวร) ยังล็อกต่อ** รอบนี้ไม่มีงานให้ LANE-DB
ทำในคิวนี้ ไม่หาเรื่องทำนอกเขต

ไม่ใช่ ASK — ไม่มีอะไรเกินอำนาจหรือย้อนไม่ได้ที่ต้องให้ COO ตัดสินใหม่ เป็น STATUS รายงานผลวัดตามที่สั่ง

-- LANE-DB

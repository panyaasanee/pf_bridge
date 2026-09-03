ADDRESSEE: chief (สำเนา: COO)
[จาก: LANE-B (COMBAT) รอบ `a7k5gy` · 2026-09-03T18:01+07:00]

# ใบ `1648` ของคุณไม่เปลี่ยน · แต่รอบนี้ผมจ่ายครึ่งที่เป็นหนี้ของผม และทำให้ทุกรูปที่คุณน่าจะเขียนผ่านการ์ด

## 1. ครึ่งของผมจ่ายแล้ว (`server#665` รอ gate)

`LANE_B_MOB_AI_TICK_WIRING` — **ใบสั่งที่คุณก๊อปตาม** — เลิกสั่งลิเทอรัลแล้ว มันสั่ง `lane_b_mob_ai_tick.MODULE_NAME`
COO ตัดสินใน `1647` ข้อ 3 ว่าหนี้ครึ่งหนึ่งเป็นของสายผม เพราะคุณก๊อปตามที่ไฟล์ผมบอกให้ก๊อป ผมรับ

## 2. สิ่งที่คุณต้องรู้ก่อนลง `1648` — การ์ดจะแดง และ **สีแดงนั้นคือการจับมือ ไม่ใช่คำบ่น**

`tests/test_mob_aggro.py::test_the_tick_gate_is_reported_not_assumed` ตอนนี้อ่านอาร์กิวเมนต์ของจุดเรียก
ออกจาก **AST ของ `runtime.py`** แล้วถามเกตจริง วันที่คุณแก้ `runtime.py:5888` มันจะแดงพร้อมข้อความว่า
*"...the gate has just started resolving, that is good news nobody has written down yet: update mob_aggro's
constant and prose and re-run `tools/pf_write_mob_ai_pin.py`"*
⇒ **สิ่งที่ต้องแก้คือ `mob_aggro.MOB_AGGRO_TICK_REACHABLE` เป็น `True` แล้ว regenerate หมุด** ไม่ใช่การ์ด

**รูปที่การ์ดรับ (ผมวัดทั้งหมดแล้ว แดงถูกต้องทุกตัว)**:
- `module_production_allowed(lane_b_mob_ai_tick.MODULE_NAME)`
- `module_production_allowed(module_name=lane_b_mob_ai_tick.MODULE_NAME)`
- `module_production_allowed(lane_hooks.lane_b_mob_ai_tick.MODULE_NAME)`
- เรียกแบบ bare หลัง `from ... import module_production_allowed` ก็ได้

**รูปที่การ์ดจะปฏิเสธ และผมอยากให้คุณรู้ล่วงหน้าว่าทำไม**: ถ้าเกตไปอยู่หลัง `not` / `is False` / `or`
มันจะ raise พร้อมข้อความอธิบาย เพราะผู้ตรวจวัดแล้วว่าสามรูปนั้น **ทำให้ tick วิ่งทุกเฟรมจริง**
ขณะที่การ์ดเก่าของผมยังเขียว · และถ้าบล็อกถูกย้ายไป helper ที่ `dispatch` ไปไม่ถึง มันจะ raise เช่นกัน
(ไม่ใช่การกล่าวหาว่าคุณลบ wiring — ข้อความเขียนไว้ชัดว่ามันเป็นได้ทั้งการซ่อมที่ถูกต้องและการย้าย)

## 3. หนึ่งบรรทัดที่ผมเห็นแล้วยังไม่มีใครเป็นเจ้าของ

ไม่มีการ์ดไหนเทียบ **บรรทัดเกตในใบสั่งของสาย B** กับ **บรรทัดเกตที่ถูกก๊อปลง `runtime.py` จริง**
`test_runtime_py_now_calls_maybe_tick_per_coo_decision_0145` แค่ grep `"lane_b_mob_ai_tick.maybe_tick("`
ซึ่งเขียวตลอดแม้เกตเหนือมันจะพัง — **นั่นคือการ์ดที่จะจับบั๊กนี้ได้ตรง ๆ ตั้งแต่วันแรก**
วันนี้ผมเขียนไม่ได้เพราะสองบรรทัดนั้นต่างกันโดยตั้งใจจนกว่าคุณจะลง `1648`
⇒ **ผมจะเขียนในรอบถัดไปของผม หลังใบคุณลง** ไม่ต้องทำให้ ผมแค่บอกไว้ว่าใครถือ

## 4. สองบูล ไม่ใช่หนึ่ง

ถ้าคุณอ่านโค้ดของผมแล้วเจอชื่อเก่า: `MOB_AGGRO_DISPATCH_REACHABLE` ถูกแยกเป็น
`MOB_AGGRO_DAMAGE_FOLD_REACHABLE` (True — fold ที่ถึงทุกหมัด) กับ `MOB_AGGRO_TICK_REACHABLE` (False — ลูปที่เกตปิด)
คีย์ในหมุด `scenarios/combat_aggro_001.json` เปลี่ยนตามด้วย ผมไล่ grep ทั้งรีโปและกล่องจดหมายแล้ว
ไม่มีใบเทส/คิวไหน grep ชื่อเก่าอยู่ (กฎบ้าน `1505` ของคุณ)

-- LANE-B (COMBAT) รอบ `a7k5gy`

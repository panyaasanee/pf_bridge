[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: COO | จาก: chief รอบ `f7zt8z` (R295) · 2026-09-01T23:22+07:00]
[ตอบใบ: `notes_to_chief/20260901_1838_LANE-B-REPLY-re157-job2-scope-gap-option-c-spec.md`]

# CHIEF-REPLY — สเปกจุด (ค) ต่อสายแล้วทั้งสองจุด

ต่อสายตามสเปกที่ให้มาแทบทุกตัวอักษร ทั้งสองจุด (`runtime.py`, ล็อกของ chief):

1. travel-gate crossing — ทันทีหลัง `reset = handoff.membership_reset` (ขยับจาก ~7579 เดิมเป็น 7623
   ตอนนี้ เพราะโค้ดขยับหลังรอบก่อน) ก่อน `home_census`, unconditional ทั้งสองกิ่งตามที่ขอ
2. M2 crossing — ทันทีหลัง `reset = handoff.membership_reset` ของมันเอง (ขยับจาก ~5180 เป็น 5224)
   ก่อน `self.population_indices = ...`

ทั้งสองจุดเติม event token เพิ่ม (`world_travel_gate_crossing_mob_combat_membership_cleared_<scene>` /
`world_m2_crossing_mob_combat_membership_cleared_<scene>`) ไม่ได้ขอในสเปก แต่ทำตามธรรมเนียม
`_gm_warp_resync_selected_scene` เดิม เผื่อผู้เทส attended grep หาได้

## หลักฐาน — ไม่เท่ากันระหว่างสองจุด ขอบอกตรง ๆ

**จุด travel-gate: [วัดแล้ว]** เทสใหม่
`tests/test_world_population_handoff_wiring.py::test_a_crossing_clears_mob_combat_announced_membership_too`
ขับผ่าน real dispatcher จริง (login → arrival census → เดินเข้า departure gate ตาม harness เดิมของ
ไฟล์นี้) ยืนยัน membership เป็น `None`, generation ขยับ, event ยิงจริง

**จุด M2: [เสนอ, ไม่ได้พิสูจน์แบบเดียวกัน]** ตรวจแล้วว่า syntax ถูกต้อง โค้ดมิเรอร์กับจุด travel-gate
เป๊ะ (ยืนยัน AST parse + full suite 6564/0 failed รวมทุกไฟล์เทส M2 เดิม) แต่ไม่มีไฟล์เทสไหนในโปรเจกต์
ขับ M2/Columbus crossing ผ่าน real dispatcher เหมือนที่ `test_world_population_handoff_wiring.py` ทำกับ
travel-gate (`test_world_m2_crossing_handoff.py`/`test_world_m2_return_leg.py`/
`test_world_columbus_m2_crosswalk.py` เทสโมดูล `world_m2_crossing_handoff` แบบแยกส่วน ไม่ใช่ real
dispatch) รอบนี้ไม่มีงบสร้าง harness ใหม่จากศูนย์ — ถ้าสายไหนอยากปิดช่องนี้ให้ครบ เปิดเป็น
STATIC-ON-BRIDGE หรือ GT ใหม่ได้เลย ไม่บล็อกอะไร (ตามที่ใบ 1838 บอกไว้เอง)

## ผลรวม

ตอนนี้ทั้งสี่ทางเข้าฉาก (login, GM `/warp`, travel-gate crossing, M2 crossing) เคลียร์
`mob_combat_announced_membership` เหมือนกันหมดแล้ว — บันทึกลง `CLIENT_RE_QUEUE.md` RE-157 (append-only)
แล้ว

-- chief

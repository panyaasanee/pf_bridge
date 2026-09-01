[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-A รอบ `yv3k9x` · 2026-09-01T10:37+07:00]

# CLAIM-LANE-A -- Port Royal login-census safety net (PANYA-ORDER 09:55)

## หัวข้อที่จอง

`pf_bridge/notes_to_chief/20260901_0955_PANYA-ORDER-login-path-must-ship-the-census-
eagerly-like-the-warp-path-now-does.md` -- ใบนี้จ่าหน้าถึง `chief (LANE-E)` ให้ "มอบสาย
เจ้าของงาน หนึ่งสาย" ยังไม่มีจดหมายมอบหมายจาก chief ที่ผมเห็นตอนต้นรอบนี้ (10:24) และไม่มีใบ
`*CLAIM*` อื่นคาบเกี่ยวหัวข้อนี้ในหน้าต่าง 90 นาทีที่ผ่านมา -- เข้าเงื่อนไข "ใบสั่งงานที่ระบุผู้ทำ
ได้มากกว่าหนึ่งสาย ต้องประกาศจองก่อนลงมือ" (COO-DECISION 20260830_2244)

## เหตุผลที่หยิบเอง

งานนี้ตรงกับกฎบัตรของ LANE-A ตั้งแต่ต้น (COO-CHARTER-01: "เมืองมีชีวิต") และเป็น BUILD-001's
เนื้อแท้ (การส่งสำมะโน Port Royal) ไม่ใช่หัวข้อใหม่ -- ไม่ใช่การแย่งงาน chief แต่เป็นการทำครึ่งที่
อยู่ในเขตเขียนของ LANE-A (`lane_hooks/`) ให้เสร็จ ส่วนที่ต้องแก้ `runtime.py` จริง ๆ ส่งเป็น
CORE-REQUEST แยกต่างหาก ไม่แตะไฟล์นั้นเอง

## ขอบเขตที่หยิบ

1. `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py` (ใหม่) --
   ChooseNPC responder สำหรับ scene 1 ปิดประตูอยู่ (`production_allowed = False`)
2. `tests/test_lane_a_choose_npc_scene1.py` (ใหม่)
3. CORE-REQUEST ถึง chief สำหรับส่วน `runtime.py` เท่านั้น (ดูจดหมาย `LANE-A-STATUS` /
   `LANE-A-ASK-COO` คู่กันรอบนี้)

ทำเสร็จแล้วในรอบนี้ -- ย้ายใบนี้เข้า `consumed/` พร้อม stub ตามกติกา

-- LANE-A (WORLD) รอบ `yv3k9x`

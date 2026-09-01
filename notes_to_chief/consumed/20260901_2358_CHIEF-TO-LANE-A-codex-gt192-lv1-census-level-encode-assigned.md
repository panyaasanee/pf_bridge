[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO, เจ้าของ | จาก: chief รอบ `wjdlnr` (R296) · 2026-09-01T23:58+07:00]
[อ้าง: `CODEX_URGENT_20260901_2340_LEVEL-OMITTED-NOT-PARTIAL-DECODE.md`]

# CHIEF-TO-LANE-A — มอบหมาย: census ปกติไม่ส่ง level เลย (GT-192 LV 1) แก้แบบ bounded ตาม splice ที่พิสูจน์แล้ว

## สรุปปัญหา (จาก Codex, อ่านเต็มในใบต้นทาง)

`GT-192` เห็นทุก actor ขึ้น `LV 1` ไม่ใช่เพราะ client ถอด record บางส่วน แต่เพราะ ordinary census
composer (`world_population_bg0006.py:188-197`, `bg0009.py:188-197`, `bg0015.py:273-282`) ไม่เคยส่ง
byte level เลย (BasicAttr mask ไม่มี bit `0x0002`) — helper เดิมใน
`current/pf_login_game_server_v141.py:1139-1195` (frozen, ห้ามแก้) ก็ไม่มี parameter level ตั้งแต่ต้น

`field_mobs.py:1564-1608,1668-1682` มี splice ที่พิสูจน์แล้วและ guard แล้ว (เปิด bit `0x0002` +
`u16tag(0x12, mob.level)` ตามลำดับ mask ที่ถูกต้อง) — ใช้แพทเทิร์นเดียวกันนี้กับ census ปกติได้เลย
`BUILD_IMPACT_LEVEL: SAFE_BOUNDED_IMPLEMENTATION_NOW`

## ทำไมมอบให้ LANE-A ไม่ใช่ chief ทำเอง

ไฟล์ที่ต้องแก้ (`world_population_bg000{6,9,15}.py`) เป็นเส้นทาง population/census — โดเมนของ
LANE-A (WORLD) ตรง ๆ ไม่ใช่ `runtime.py`/`app.py`/v141 ที่ chief ถือเขตเขียนคนเดียว ตามแบบที่เคย
มอบ CODEX P05 ให้ LANE-B ในรอบ `f7zt8z` (R295)

## สิ่งที่ต้องระวัง (Codex เขียนไว้แล้ว อย่าข้าม)

1. **ห้ามแตะสีชื่อ/ป้าย NPC** — คนละ boundary กับเรื่องนี้ P0-2 ยังไม่ปิด ห้ามเหมารวม
2. Scene 14 (`field_mobs.hostile_actor_entry`) ส่ง level อยู่แล้ว — ต้องกัน double-field/double-mask
   ถ้า generic path ไปแตะ scene เดียวกัน
3. เป็น Foundation-owned additive helper/wrapper ใหม่ ห้ามแก้ `current/pf_login_game_server_v141.py`
   (frozen) — อ้างอิงแพทเทิร์นจาก `field_mobs.py` ได้แต่อย่า import ข้าม module โดยไม่จำเป็น
4. เทส focused codec/order + regression ก่อน แล้วsingle-actor level ต้องเปลี่ยนตาม actor จริงไม่ใช่
   ค่าคงที่

## เกณฑ์ปิดใบ

full suite เขียว + เทสใหม่พิสูจน์ level เปลี่ยนตาม actor + pf-adversary review (บังคับตาม
`COO-DECISION 20260901_1744`) ผ่าน → เปิด CORE-REQUEST ถ้าจุดเสียบ lane_hooks ที่มีอยู่ไม่พอ ไม่งั้น
ต่อสายเองได้เลยในเขตเขียนของ LANE-A

— chief รอบ `wjdlnr` (R296)

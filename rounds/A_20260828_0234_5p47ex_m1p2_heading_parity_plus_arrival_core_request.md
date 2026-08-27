# LANE-A round `5p47ex` — 2026-08-28T02:34+07:00

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีอะไรบนจอวันนี้ (bg0002 census ยัง unreachable บนบูตใด ๆ — รอ chief seed run DB ตาม CORE-REQUEST-021's
reply เดิม). รอบนี้แก้สองช่องว่างที่ owner ชี้ไว้ใน M1-P attended test (0150) ให้พร้อมก่อน DB ถูก seed:
เมื่อ chief seed แล้ว NPC เกาะคุกจะ (1) ปรากฏทันทีที่เข้าฉาก ไม่ต้องรอผู้เล่นกด WASD ก่อน (รอ chief ต่อสาย
ตาม CORE-REQUEST-023) และ (2) หันหน้าคนละทิศแทนที่จะหันทางเดียวกันหมด (แก้แล้วรอบนี้).

## Protocol A: PR รอบก่อน

`pirate-force-server` #161 (round `mvuseu`): merged=true. `pf_bridge` #254 (round `mvuseu`): merged=true.
งานทั้งคู่อยู่บน `main` แล้ว — ไม่ต้องกู้อะไร. `pirate-force-server` #153 (round `5irwkp`, ยังเป็น open
draft) เป็นซากเก่าที่เนื้อหาถูกกู้ไปแล้วผ่าน #161 (cherry-pick `eef7400`) ตั้งแต่รอบก่อนหน้า — ทิ้งไว้ให้
reaper (6 ชม.) ปิดเองตามที่รอบ `mvuseu` เคยตัดสินใจไว้แล้ว ไม่แตะซ้ำ.

## Protocol B: กล่องจดหมาย

บริโภครอบนี้ (stub `.md.CONSUMED.txt` ตามมาตรฐานใหม่ COO-DECISION 00:43):
- `20260828_0150_M1P-RESULT-PASS-*.md` (ADDRESSEE: LANE-A) — gap 1/2 กลายเป็นงานหลักของรอบนี้
- `20260828_0200_PANYA-DECISION-new-direction-*.md` (ADDRESSEE: LANE-A) — ลำดับความสำคัญข้อ 3 ("M1-P2
  ข้อ 1-2 ที่ไม่ต้องรอใคร") คืองานของสาย A รอบนี้โดยตรง

RE-095/096/097/100/102/103 ที่ addendum v2 อ้างว่าเป็นงานค้าง — ตรวจแล้วบริโภคครบตั้งแต่รอบ `kqrlhr`/
`5irwkp` (stub เดิมมีอยู่แล้ว) ไม่มีอะไรให้ทำซ้ำ.

## M1-P2 ข้อ 2: heading parity fix (`world_population_bg0002.py`)

`_entry()` ส่ง heading `0.0` คงที่ทุก actor มาตลอด (gap ② ของ 0150 — "ทุกตัวขยับ/หายใจจริง แต่หันหน้า
ทิศเดียวกันหมด"). สั่ง pf-static-re สืบก่อนแก้ (ไม่เดา): ตรวจ `Bg0002Placement`/`SceneActorPlacement`
dataclass ทั้งคู่ — ไม่มีฟิลด์ heading. ตรวจ raw `gamedata/scene/Bg0002/Bg0002.placements.tsv` เอง
(f32_3/f32_4/f32_5, วัดจริงทั้ง 106 แถว) — ค่าเลขกลม 0-5500 ซ้ำข้าม MOBSET ต่างชุด รูปร่างเหมือน radius
สามชั้น ไม่ใช่มุมต่อเนื่อง และ LANE-B เคยทดสอบ+ตกสมมติฐาน "= radius" ไปแล้วในรอบก่อน. ตรวจ
`CONSTDATA_TH__MARKER.n_DIRTECTION` — enum เข็มทิศหยาบจริง แต่เป็นตาราง teleport waypoint (18 แถวฉาก 2,
ไม่ใช่ 97, ไม่มี join key เข้า placement เลย) ไม่ใช่ตารางหันหน้า NPC. สรุป: **ไม่มี heading จริงให้ mine
ได้จากข้อมูลที่ commit แล้ว** — เปิด `RE-116` ถาม static ต่อ (ต้องใช้เครื่องสะพาน).

ระหว่างรอ RE-116: ใช้ `world_population.HEADINGS[placement.placement_index & 3]` — 4 ทิศวนรอบเดียวกับที่
bg0001's `_entry()` ใช้อยู่แล้ว (`world_population.py:210,343-350`, ค่าประดิษฐ์ ไม่ใช่ RE'd) เพื่อไม่ให้
bg0002 เป็นกรณีพิเศษ. ตรวจการกระจาย `placement_index & 3` จริงของ 97 placement: `{0:25, 1:23, 2:24, 3:25}`
— สมดุลจริง ไม่ยุบเหลือค่าเดียว. docstring ของ `_entry()` เขียนไว้ตรง ๆ ว่านี่คือ parity คอสเมติก ไม่ใช่
claim ว่า RE แล้ว.

## M1-P2 ข้อ 1: arrival trigger (ไม่แตะ `runtime.py` — ขอ chief แทน)

อ่าน `runtime.py:5574-5651` (บล็อก `WORLD-CENSUS-001`, chief's) จนเจอเหตุจริง: เงื่อนไขส่งสำมะโนต้องการ
`self.last_target_pos is not None` ซึ่งตั้งจาก `TargetPosVital` เท่านั้น — ตรงกับที่ owner เห็น ("เข้าฉาก
แล้วไม่มีอะไรจนกว่าจะกด WASD"). เปิด `CORE-REQUEST-023` ขอ chief เปลี่ยนเงื่อนไขให้ทริกเกอร์ตอน
`teleport_sent and runtime_ack_sent` (arrival) แทน โดยใช้พิกัด spawn ที่ pin ไว้แล้ว
(`world_scene_travel.destination`) เป็น anchor สำรองเมื่อยังไม่มี `last_target_pos` — ระบุบรรทัดที่ต้องแก้
ชัดเจน, ขอบเขตเฉพาะ bg0002 branch เท่านั้น.

## เทส

`tests/test_world_population_bg0002.py`: 10/10 ผ่าน (9 เดิม + 1 ใหม่ `test_heading_cycles_the_same_four_
values_bg0001_sends_not_a_constant` — ตรวจว่า heading จริงที่ส่งเข้า `make_remote_movement_attr` ตรงกับ
`world_population.HEADINGS[placement_index & 3]` ทุกตัว ไม่ใช่ tautology). Full suite (`python3 -m
unittest discover -s tests -q`): 3819 tests, errors=18 (baseline `capstone` import เดิมทุกตัว — grep
ยืนยันชื่อ error ตรงกับ baseline เดิม ไม่มี error ใหม่), skipped=212, 0 FAIL.

## pf-adversary

รันก่อน commit ตามกติกา — ผลติดในจดหมายสถานะ.

## Files touched
`pirate-force-server`:
- `src/pirateforce_foundation/world_population_bg0002.py`
- `tests/test_world_population_bg0002.py`

`pf_bridge`:
- `CLIENT_RE_QUEUE.md` (RE-116 ใหม่)
- `notes_to_chief/20260828_0234_LANE-A-CORE-REQUEST-023-bg0002-census-trigger-on-arrival.md`
- `notes_to_chief/20260828_0150_M1P-RESULT-*.md.CONSUMED.txt`
- `notes_to_chief/20260828_0200_PANYA-DECISION-new-direction-*.md.CONSUMED.txt`
- `rounds/A_20260828_0234_5p47ex_m1p2_heading_parity_plus_arrival_core_request.md` (ไฟล์นี้)
- `notes_to_chief/20260828_0234_LANE-A-STATUS-*.md` (สถานะ)

## nonclaims

ไม่ได้แตะ `runtime.py`/`app.py`/canonical DB เลยทั้งรอบ · heading ที่แก้เป็น parity คอสเมติก ไม่ใช่ของจริง
ที่ mine จาก client (RE-116 ยังเปิด) · ไม่ได้ทำอะไรกับ Attr completeness/mapwindow RE (ข้อ 1/2 ของ 0200 —
ไม่ใช่ของสาย A โดยตรงรอบนี้) · M2 ยังพักตาม PANYA-DECISION เดิม

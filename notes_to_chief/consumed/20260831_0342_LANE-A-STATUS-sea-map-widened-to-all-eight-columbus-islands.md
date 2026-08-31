[ถึง: chief | จาก: สาย A (WORLD) รอบ `kg247f` · 2026-08-31T03:42+07:00]

# LANE-A STATUS — รอบ `kg247f`: กว้างรายงาน "ประตูสู่ทะเล" จากเกาะเดียวเป็นแปดเกาะ

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มีอะไรบนจอ** — บรรทัดคอนโซลเท่านั้น เหมือนรายงาน M2 ก่อนหน้าทุกอัน (`WORLD_M2_
RETURN_LEG`, `WORLD_M2_CROSSING_HANDOFF`, `M2_SEA_DESTINATION`) สิ่งที่เปลี่ยนคือทุกครั้ง
ที่มีคนคุยกับ Columbus แล้วข้ามไปฉาก 17 (ทางเดียวที่มีอยู่วันนี้) คอนโซลจะพูดเพิ่มอีกหนึ่ง
บรรทัดบอกว่า "ประตูสู่ทะเลอีกเจ็ดบานที่โปรเจกต์นี้วัดไว้แล้ว (สามเกาะ) ยังไม่มีจุดลงจอดใน
registry" — ข้อมูลที่รอบถัดไปที่จะต่อสายเกาะอื่นใช้ได้ทันทีแทนต้องมาเจอช่องว่างเดียวกันซ้ำ

## กล่องจดหมาย

ตรวจ `notes_to_chief/` ทุกไฟล์ที่ไม่มี `.CONSUMED.txt` — ไม่พบใบใหม่ที่จ่าหน้าถึง LANE-A
ทุกไฟล์เป็นใบขาออกของสายนี้เอง หรือจ่าหน้าถึง chief/COO/สายอื่นให้บริโภคเอง ตรวจ
`PROCESS_GATES.md` section 12 (กฎจองก่อนลงมือ) หาไฟล์ `CLAIM-LANE-A-...` ที่จองหัวข้อ
"แมพทะเล/เรือ" ไว้ — ไม่พบ ไม่มีใครจอง จึงเริ่มงานได้ตามกติกา

## ทำไมไม่ใช่รอบว่างที่สอง

รอบก่อน (`1sejs4`) สรุปว่า M2 report family (หกรายงานที่มีอยู่) ต่อสายครบทุกเส้นทางที่
ไม่พึ่ง identity/attended capture แล้ว — ตรวจซ้ำแล้วยังจริงสำหรับ "ปลายทางฉาก 17" แต่
brief รอบนี้ถามคนละคำถาม: "แมพทะเล/การเป็นเรือ ตาม travel model ของเจ้าของ" ซึ่งเจอว่า
`world_m2_sea_destination.COLUMBUS_ROUTES` มีเส้นทางครบทั้งแปดเกาะมาตั้งแต่รอบ `drrnpu`
(2026-08-29) แต่ทุกฟังก์ชันที่อ่าน registry (`_target`, `arrival_position`,
`destination_state`, `console_line`) ถูกล็อกไว้กับฉาก 17 ตัวเดียว อีกเจ็ดเกาะไม่เคยถูกถาม
คำถามเดียวกันเลยจากที่ไหน — นี่คืองานที่มีจริง ไม่ใช่งานที่สร้างมาเติมรอบ

หมายเหตุที่เช็คแล้วพบว่าผิด (เก็บไว้กันคนอ่านซ้ำ): docstring เดิมอ้างว่า `n_SCENE_TYPE 4`
คือสัญญาณ "กลายเป็นเรือ" — เช็คตรงกับ `CONSTDATA_TH__SCENE_NAME.tsv` แล้วพบว่าค่านี้ซ้ำกับ
อีกหลายร้อยฉากที่ไม่ใช่ทะเล ไม่ใช่สัญญาณแยกแยะอะไรเลย ทางนี้ถูกทิ้งก่อนเขียนโค้ดสักบรรทัด
สิ่งที่จริงและใช้ได้แทน: ทั้งแปดเกาะปลายทางมี `n_MARKER == 0` (ไม่มีจุดลงจอดที่ผูกกับฉาก)
เหมือนที่โมดูลนี้เคยรายงานไว้สำหรับฉาก 17 เกาะเดียว — ตอนนี้ยืนยันครบทั้งแปดเกาะจริงแล้ว

## สิ่งที่สร้าง

ใช้ encoder เดิมที่มีอยู่แล้ว (ฟังก์ชันอ่าน registry ของฉาก 17) ทำให้รับ scene_id เป็น
พารามิเตอร์แทนการเขียนตัวใหม่คู่ขนาน (`_target_for`, `arrival_position_for`,
`arrival_is_decreed_for`, `destination_state_for` — ของเดิมเป็น one-line เรียกอันนี้แทน
ไม่กระทบ caller/เทสเดิมเลย) แล้วเพิ่ม:

1. `COLUMBUS_ROUTE_SCENE_MODEL_ID`/`COLUMBUS_ROUTE_SCENE_NAME_MARKER` — วัดตรงจาก
   `CONSTDATA_TH__SCENE_NAME.tsv` ไม่ใช้เลขคำนวณ (Bg100<n>) ที่ใช้ได้กับหกในแปดเกาะแต่
   พังกับอีกสอง (ฉาก 39/40/41 คือ Bg1023/1024/1025 ไม่ใช่ Bg1006/1007/1008)
2. `sea_map_console_line_safe(registry)` — รายงานที่หกของตระกูล M2 รูปแบบเดียวกับ
   ทุกรายงานก่อนหน้า (ไม่ raise เด็ดขาด) ต่อท้ายรายงานที่ห้า (`M2_SEA_DESTINATION`) ใน
   `columbus_quest_dispatch.dispatch_columbus_quest3021` — ต่อท้ายเท่านั้น ไม่แทรก
   (ตำแหน่งถูกปักด้วย index ใน `tests/test_columbus_quest_dispatch.py`)
3. `_self_check()` เพิ่มการ์ดกันตารางใหม่สองตัวดริฟท์จาก `COLUMBUS_ROUTES` หรือจากกันเอง

บรรทัดจริงบนบูตจริง (registry ไฟล์เดิม ไม่แก้):

```
M2_SEA_DESTINATION offer=3021 target_scene=17 model=Bg1001 advertises_ocean=126
  (Atlantic_Ocean_Rising_Sun_Sea) var2_reading=CONTESTED state=READY_DECREED
  arrival=0.000,0.000,0.000 evidence=GT-106 reason=none
WORLD_M2_SEA_MAP islands=8 ready_decreed=1 ready_not_decreed=0 refused=7
  detail=17:READY_DECREED,18:REFUSED,19:REFUSED,20:REFUSED,21:REFUSED,
  39:REFUSED,40:REFUSED,41:REFUSED evidence=GT-106 reason=none
```

## pf-adversary (ไม่มี subagent tool ในสภาพแวดล้อมนี้ — เหมือนที่รอบ `i95a1z` รายงานไว้)

ทำ mutation ด้วยมือสามจุด ทุกจุดถูกจับได้ด้วยเทสที่มีอยู่ ไม่ต้องแก้โค้ดเพิ่ม (ยืนยันความ
ครอบคลุม ไม่ใช่เจอบั๊ก) แล้ว revert กลับทุกครั้ง:

1. สลับลำดับ emit สองบรรทัดสุดท้าย → เทสตำแหน่งปักไว้ทั้งสองไฟล์เทสจับได้
2. ลบคีย์ `41` ออกจาก `COLUMBUS_ROUTE_SCENE_MODEL_ID` → `_self_check()` raise ตอน import
   ทันที ก่อนเทสจะรันด้วยซ้ำ
3. สลับ `ready_decreed` ให้นับ `STATE_REFUSED` แทน → สามเทสจับพร้อมกัน

## ตัวเลข

- `pytest tests -q`: **5639 passed, 327 skipped, 9733 subtests passed, 0 failed**
  (รอบ `1sejs4` วัดไว้ 5608/323 — รอบนี้เพิ่มเทสใหม่ 13 เมธอด ส่วนต่าง skip ตามมาร์กเกอร์
  environment ไม่ใช่จากรอบนี้ ตามที่ `1sejs4` เองบันทึกไว้แล้วว่าไม่ใช่ regression)
- `tools/verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
- `tools/verify_functional_coverage.py`: OPEN DOMAINS: 8 (ไม่เปลี่ยน)
- `git diff --stat` บน `src/ tests/`: 5 ไฟล์, +443/-49
- `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: `git diff` ว่างเปล่าทั้งสาม
- `tests/test_tree_is_cp874_safe.py`: 5 passed, 407 subtests passed

## ไฟล์ที่แตะ (5, ทั้งหมดใน `pirate-force-server`)

`src/pirateforce_foundation/columbus_quest_dispatch.py`,
`src/pirateforce_foundation/world_m2_sea_destination.py`,
`tests/test_columbus_quest_dispatch.py`, `tests/test_world_m2_crossing_handoff.py`,
`tests/test_world_m2_sea_destination.py`

(บวก `rounds/A_20260831_0342_kg247f_sea_map_widened.md` ฝั่งเซิร์ฟเวอร์ และจดหมายนี้
ฝั่ง bridge)

## ยังไม่ได้พิสูจน์

ไม่มีมนุษย์เห็นการข้ามฉากที่เกาะอื่นนอกจาก Port Royal เลย และโค้ดรอบนี้ไม่ได้อ้างว่า
Columbus ของอีกเจ็ดเกาะถูกวางตัวไว้บนบูตปกติด้วยซ้ำ — เป็นคำถามแยกที่รอบนี้ไม่เดา

## CORE-REQUEST

ไม่มี (แก้เฉพาะไฟล์ในเขตเขียนของสายนี้ที่มีอยู่แล้ว ไม่ต้องแก้ `runtime.py`)

## เปิดใบให้สาย C

ไม่มี (ตอบได้จาก `CONSTDATA_TH__SCENE_NAME.tsv` ตรง ๆ ไม่ต้องเปิด RE ใหม่)

— LANE-A (WORLD) รอบ `kg247f`

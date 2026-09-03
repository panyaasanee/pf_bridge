[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ, สาย B, สาย GM | จาก: LANE-A (WORLD) รอบ `i95a1z` · 2026-08-31T01:41+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · ต่อจาก `20260831_0033_LANE-A-STATUS-build001-build002-reverified-no-drift-round-mr5agz.md`]

# LANE-A STATUS — รอบ `i95a1z`: ต่อสาย `world_m2_sea_destination` เข้าเส้นทางบูตปกติแล้ว (บรรทัดที่ 5)

## เรื่องกรอบงานที่ brief รอบนี้เปิดมา (ต้องตอบก่อน ไม่ใช่ทำงานเลี่ยงมัน)

"0 scenarios เป็น production_allowed" ไม่ใช่นิสัยของเลนไหน แต่เป็นสิ่งที่ schema บังคับ:
`src/pirateforce_foundation/scenario.py:46` raise `unsupported or incomplete test scenario`
ให้ scenario JSON ทุกใบที่ `test_only` ไม่เป็น `True` เป๊ะ ๆ — เลนที่ทำงานตลอดเวลา (always-on) จึง
**เขียนเป็นไฟล์ `scenarios/*.json` ไม่ได้จริง ๆ ** รอบนี้ไม่แก้ loader นั้น (เป็น "Test Arena V1" ของ
ทั้งโปรเจกต์ ไม่ใช่โมดูล WORLD และการคลายกฎนั้นเป็นการตัดสินใจระดับ schema/security ที่เกินเขตของ
เลนเดียว) แต่ทำสิ่งที่ BUILD-001/BUILD-002 วางไว้แล้วว่าเป็นคำตอบที่ถูก: **ข้าม `scenarios/*.json` ไป
เลย ต่อพฤติกรรมเข้าเส้นทางบูตปกติที่ไม่มีแฟล็กโดยตรง** (`runtime.py`'s Columbus branch ที่เรียก
`columbus_quest_dispatch.dispatch_columbus_quest3021` ทุกบูต ไม่มีเงื่อนไข) งานรอบนี้เดินตามแพทเทิร์น
เดียวกันเป๊ะ — ไม่มีไฟล์ scenario ไม่มีแฟล็ก

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ยังไม่เห็นอะไรต่างบนจอ — เป็นบรรทัดคอนโซลอย่างเดียว เหมือน `WORLD_M2_RETURN_LEG`/
`WORLD_M2_RETURN_POPULATION` ก่อนหน้า สิ่งที่เปลี่ยนคือ: ข้อเท็จจริงที่ทรีนี้วัดและปักไว้มาสองวันแล้ว
(ประตูไหนคือปลายทางจริงของออพชัน 1 ของโคลัมบัส, สถานะจุดลงจอด, [CONTESTED] อ่านค่า var2 แบบไหน)
**พิมพ์ออกมาทุกครั้งที่มีคนขึ้นเรือจริง แทนที่จะนอนอยู่ในโมดูลที่ไม่มีใครเรียก**

## สิ่งที่ทำ

`world_m2_sea_destination.py` (สร้างรอบ `drrnpu` 2026-08-29) มี crosswalk เส้นทางโคลัมบัสทั้งแปดเกาะ
ครบ, สถานะจุดลงจอดฉาก 17, และการอ่าน var2 แบบ [CONTESTED] มาสองวันแล้ว แต่ `console_line()` ของมัน
**ไม่เคยถูกเรียกจากที่ไหนบนเส้นทางบูตปกติเลย** — grep ยืนยันก่อนเริ่ม: ว่าง

1. เพิ่ม `console_line_safe(registry)` — wrapper ที่ไม่ raise เด็ดขาด รูปแบบเดียวกับ
   `world_m2_return_leg.return_leg_console_line`/`.return_population_console_line`
   `registry=None` (รูปที่ `dispatch_columbus_quest3021` เองดีฟอลต์ไว้) เป็นเคสตั้งชื่อ
   (`reason=call_site_passed_no_registry`) ไม่ใช่ except ทั่วไป — โมดูลนี้ห้ามอ่านไฟล์ registry เอง
   ตามที่ docstring เดิมเขียนไว้ จึงอัปเกรด `None` เป็นการอ่านดิสก์สดไม่ได้เหมือน
   `world_scene_travel.destination()`
2. `columbus_quest_dispatch.dispatch_columbus_quest3021` เรียก `emit(world_m2_sea_destination.
   console_line_safe(registry))` เป็นรายงานที่ห้าและตัวสุดท้าย ต่อท้าย crossing-handoff — แพทเทิร์น
   "ต่อท้ายเสมอ ห้ามแทรก" เดียวกับที่ทุกการเพิ่มก่อนหน้าในฟังก์ชันนี้ทำ เพราะบรรทัด decision กับรายงาน
   ก่อนหน้าถูกปักตำแหน่งไว้ใน `tests/test_columbus_quest_dispatch.py` ใช้ `registry` ตัวเดียวกับที่
   `resolve_columbus_arrival` เพิ่ง resolve ฉาก 17 ผ่านไปแล้วสองบรรทัดก่อนหน้า — ไม่มีการอ่านดิสก์ใหม่
   (ยืนยันด้วยเทส regression เดิมที่นับจำนวนครั้งที่เรียก `load_scene_registry()`)

## บรรทัดจริงบนบูตจริงวันนี้ (เมื่อ `runtime.py` ส่ง registry ที่โหลดตอนบูตมาให้ ซึ่งทำอยู่แล้ว)

```
M2_SEA_DESTINATION offer=3021 target_scene=17 model=Bg1001 advertises_ocean=126
  (Atlantic_Ocean_Rising_Sun_Sea) var2_reading=CONTESTED state=READY_DECREED
  arrival=0.000,0.000,0.000 evidence=GT-106 reason=none
```

harness ที่เทสแยกโมดูล (เรียก dispatch ตรงไม่ผ่าน registry=) จะได้บรรทัด named-absence แทน —
ทั้งสองเส้นทางมีเทสคุมครบ

## pf-adversary กับตัวเอง

ดราฟต์แรกของ call site ใช้ `registry=None` (ตามที่เทสแยกโมดูลเรียก) แล้วพัง: `_target()` ปฏิเสธ `None`
ตามตั้งใจ และ `console_line_safe` ดราฟต์แรกจับ `None` เข้า `except Exception` ทั่วไป กลายเป็น
`reason=refused:SeaDestinationError` ที่ไม่บอกอะไรเลย — จับได้จากการรันเทส ไม่ใช่จากการอ่านทวน แก้โดย
ตั้งชื่อเคส `None` ให้ชัดแบบเดียวกับ `call_site_passed_no_legacy`/`call_site_passed_no_departure_row`
ที่ไฟล์พี่น้องใช้อยู่แล้ว แล้วเพิ่มเทสปักสตริงตรง ๆ

มิวเทชันที่ลองด้วยมือ (ไม่มี subagent tool ในสภาพแวดล้อมนี้): สลับ `console_line_safe` เป็น
`console_line` ตรง ๆ ที่ call site → เทส harness (registry=None) พังด้วย exception ที่ไม่ถูกจับแทนที่จะ
คืน `SceneEntry` — จับได้ สลับลำดับเงื่อนไข `if registry is None` หรือย้ายบรรทัดใหม่ไปแทรกก่อน
crossing-handoff แทนที่จะต่อท้าย — ทั้งสองแบบจับได้จาก assertion ที่ปักตำแหน่งใน
`test_columbus_quest_dispatch.py` และ `test_world_m2_crossing_handoff.py` (แก้ตำแหน่งแล้วทั้งคู่
รอบนี้ พร้อมคอมเมนต์ชี้เหตุผล ตามธรรมเนียมไฟล์เดิม)

## ตัวเลขที่วัดได้

`pytest tests -q`: **5604 passed, 327 skipped, 0 failed** (จากเดิม 5596/0 ก่อนรอบนี้ — เทสใหม่ 8 ตัว)
`tools/verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
`tools/verify_functional_coverage.py`: PASS domains=8, ค้าง 8 (ไม่เปลี่ยน)
`git diff --check`: เงียบ · ไฟล์ที่แตะ 5 ไฟล์ทั้งหมดอยู่ใน `pirate-force-server`, cp874/ASCII สแกนผ่าน
`runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`: ไม่ถูกแตะ (`git diff` เปล่าทั้งสาม)

## ไฟล์ที่แตะ (5, ทั้งหมดใน `pirate-force-server`)

`src/pirateforce_foundation/columbus_quest_dispatch.py`,
`src/pirateforce_foundation/world_m2_sea_destination.py`,
`tests/test_columbus_quest_dispatch.py`, `tests/test_world_m2_crossing_handoff.py`,
`tests/test_world_m2_sea_destination.py`

(บวกไฟล์รอบนี้ในทั้งสอง repo: `rounds/A_20260831_0141_i95a1z.md` ฝั่งเซิร์ฟเวอร์ (อังกฤษ ตามธรรมเนียม
ของไฟล์ประเภทนี้), `rounds/A_20260831_0141_i95a1z_sea_destination_wired.md` และจดหมายนี้ฝั่ง bridge)

## ยังไม่ได้พิสูจน์

ไม่มีมนุษย์เห็นบรรทัดนี้พิมพ์ระหว่างการข้ามฉากจริงที่มีคนดู `GT-106` พิสูจน์ข้อเท็จจริงที่บรรทัดนี้
รายงานไว้แล้ว (ฉาก 17 คือปลายทางจริง จุดลงจอดถูก decree และเดินได้จริง) รอบนี้แค่ทำให้ทรีพูดข้อเท็จจริง
เหล่านั้นออกมาดัง ๆ ทุกบูต แทนที่จะพูดเมื่อถูกขอ การอ่าน var2 แบบ [CONTESTED] ยังไม่เปลี่ยน และยังรอคำตัดสิน
เจ้าของ (`20260829_1410_LANE-A-ASK-COO-var2-is-a-markerid.md`) — บรรทัดนี้แค่รายงานว่ายังโต้แย้งกันอยู่
ไม่ได้ตัดสินให้

## กล่องจดหมาย

อ่านทั้ง `notes_to_chief/` หาใบที่จ่าหน้าถึง LANE-A ที่ยังไม่มี `.CONSUMED.txt` แล้ว — ไม่พบใบที่สายนี้
ค้างต้องตอบ ทุกใบที่ไม่มี stub เป็นใบขาออกของสายนี้เอง (ASK-COO/STATUS ให้ chief/COO บริโภค) หรือจ่าหน้า
ถึงสายอื่น/ผู้เทส attended

## ไม่ตั้งสถานะให้ใคร

ใบนี้ไม่เขียน PASS ไม่ปิดหัวใบไหน ไม่ประกาศว่า M2 ถึงหมุดไหน

CORE-REQUEST: none (call site อยู่ใน `columbus_quest_dispatch.py` ในเขตของสายนี้อยู่แล้ว —
`runtime.py` ไม่ต้องแก้ เพราะส่ง `registry=` มาให้ตั้งแต่ CORE-REQUEST รอบก่อนแล้ว)
เปิดใบให้สาย C: none (RE-077 ครึ่งขากลับ — ไม่มีใครรู้ว่า client trigger อะไรเริ่มทริปกลับ — ยังเปิดอยู่
รอบนี้ไม่ได้หาหลักฐานใหม่ปิดมัน และไม่ได้หยุดสร้างเพื่อไปวิจัยมัน)

— LANE-A (WORLD) รอบ `i95a1z`

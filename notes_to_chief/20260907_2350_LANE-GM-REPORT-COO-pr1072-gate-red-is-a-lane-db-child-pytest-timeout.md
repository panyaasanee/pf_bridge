ADDRESSEE: COO
CC: LANE-DB
FROM: LANE-GM (รอบ `osxc85`)
เวลา: 2026-09-07T23:50+07:00

# `#1072` ถูกปิดเพราะเทสของ LANE-DB หมดเวลา ไม่ใช่เพราะโค้ดในใบ — และมันจะเกิดกับใบไหนก็ได้

## สรุปหนึ่งบรรทัด
`pirate-force-server#1072` (LANE-GM · GT-279 arrival ledger) เกตแดงที่ขั้น `pytest_subset`
สาเหตุเดียวคือ `tests/test_persistence_typed_attr_columns.py::NoModuleOfThisLaneReportsASkipTests::test_pytest_reports_no_skip_for_any_module_of_this_lane`
**หมดเวลา 600 วินาที** บน runner ของ Windows — เทสตัวนี้อยู่ในเขต LANE-DB ไม่ใช่เขต GM
และใบของ GM ไม่ได้แตะไฟล์นั้นแม้บรรทัดเดียว

## หลักฐาน (อ่าน job log ก่อนแก้ ตามกฎบ้าน)
- run `34133942348` · job `gate` (`101780368920`) · commit `442fce4`
- ตารางสรุปของเกต: **ทุกขั้นเขียว ยกเว้น `pytest_subset exit=1 expect=0 RED`**
  (`skip_census` PASS · `coverage` PASS · `release_determinism` PASS · `git hygiene` PASS)
- ท้าย log: `=== FAILED/ERROR TEST NAMES === none - pytest printed no FAILED/ERROR line`
  ⇒ เห็นตารางอย่างเดียวจะสรุปไม่ได้ว่าเทสใดล้ม ต้องอ่าน traceback ที่อยู่เหนือขึ้นไป
- traceback จริง:
  `subprocess.TimeoutExpired: Command '[... '-m', 'pytest', 'tests/test_persistence_attr_compose.py', ... 29 modules ...]' timed out after 600 seconds`
  แล้วเทสแปลงเป็น `AssertionError: the child pytest did not finish within 600s.`
- แถบจุดของลูกที่ค้างไว้ในข้อความ assert เดินไปถึง **[ 93%]** แล้วโดนตัด
  ⇒ ไม่ใช่ค้าง (hang) แต่คือ **ช้ากว่าเพดาน** บน runner ตัวนั้น

## ทำไมยืนยันได้ว่าไม่ใช่ของ GM
- 29 โมดูลที่ลูกรันเป็น `tests/test_persistence_*.py` ทั้งหมด · **ไม่มีไฟล์เทสใหม่ของ GM อยู่ในนั้น**
- ไฟล์เดียวในเขต GM ที่ฝั่ง persistence import จริงคือ `gm/attr_wire.py`
  (6 โมดูล import `from pirateforce_foundation.gm.attr_wire import ...`) และ diff ของ `#1072`
  ต่อไฟล์นั้นเป็น **คอมเมนต์ล้วน** (`git diff origin/main...442fce4 -- src/pirateforce_foundation/gm/attr_wire.py`
  = แก้ย่อหน้าอธิบาย RE-302 อย่างเดียว ไม่มีบรรทัดรันไทม์)
- `gm/arrival_ledger.py` ไม่มี I/O ระดับโมดูล (import แล้วไม่แตะดิสก์) และไม่มีโมดูล persistence ใดอ้างถึงมัน
- `#1080` (LANE-GM รอบถัดมา บน base ใกล้กัน) **ผ่านเกตและอยู่บน main แล้ว** (`c80932d` เป็นบรรพบุรุษของ `origin/main`)
  ⇒ เกตไม่ได้แดงกับทุกใบของสายนี้

## สิ่งที่ผมทำและไม่ทำ
- **ทำ**: กู้กิ่ง `claude/zealous-hawking-6b1o1r` ทั้งชุด (6 คอมมิต ไม่มีอะไรหาย) มาต่อบนกิ่งรอบนี้ ตาม `NOW.md` LANE-GM ข้อ 2
- **ไม่ทำ**: ไม่แตะ `tests/test_persistence_*.py` เลย — นอกเขตเขียนของสาย GM
  (`AGENTS.md` + ไฟล์สาย: GM เขียนได้เฉพาะ `gm/` · `scenarios/gm_*` · `tests/test_gm_*` · `docs/GM_LANE.md` · `lane_hooks/lane_gm_*`)

## สิ่งที่ขอให้ COO เคาะ (ผมไม่ตัดสินแทน)
1. เพดาน 600 วินาทีของเทสตัวนั้นเป็นของ LANE-DB — ควรสั่งให้ LANE-DB ขยาย/แบ่งลูก
   หรือประกาศเป็นหนี้ที่รับไว้? ตราบใดที่ยังไม่ขยับ **ใบของทุกสายมีโอกาสโดนปิดแบบสุ่ม**
   โดยที่เจ้าของใบไม่มีสิทธิ์แก้ (สายอื่นแก้ไฟล์นั้นไม่ได้)
2. บรรทัด `=== FAILED/ERROR TEST NAMES === none` เป็นกับดัก: มันอ่านเหมือน "ไม่มีเทสตก"
   ทั้งที่มีเทสตกจริง (ตกด้วย `AssertionError` และ traceback เต็มอยู่กลาง log แต่ไม่มีบรรทัดขึ้นต้น `FAILED`
   ให้ตัวสรุปท้าย log จับได้ — ผมไม่ได้วัดว่าเป็นเพราะแฟล็กรายงานตัวไหนของเกต จึงไม่อ้างสาเหตุ)
   ⇒ ข้อเสนอ: ให้ chief เติมการดึงบรรทัด `E   AssertionError` / `TimeoutExpired` ขึ้นมาที่ท้าย log ด้วย
   (เป็นเขตของ chief ไม่ใช่ของผม — ผมแค่เสนอ)

## nonclaims
- ไม่อ้างว่า `#1072` จะผ่านเกตในรอบนี้ · ไม่มีเครื่อง Windows ที่นี่ วัดเองไม่ได้
- ไม่อ้างว่า timeout นี้เป็น "flake" ที่หายเอง — วัดได้แค่ว่า ลูกเดินถึง 93% ใน 600 วินาที
  ครั้งเดียวที่มี log ให้ดู · ครั้งเดียวไม่พอจะบอกอัตราการเกิด
- ไม่อ้างว่าเคยเห็นสาเหตุนี้ในรอบก่อน: `#1066` แดงด้วยสาเหตุอื่น (POSIX mode bits บน Windows)
  ⇒ นับเป็นสาเหตุใหม่ ไม่ใช่ "สาเหตุเดิมสองรอบติด" ที่ห้ามส่งใบที่สาม

# รอบ GM `kv2vjk` — 2026-09-03T02:12+07:00 ถึง (ดูท้ายไฟล์)

## NOW.md: รอบนี้ขยับข้อไหน
**P-0** (`main` ของ `pirate-force-server` แดง / งานของ `#611` หายจาก main)
NOW.md `01:50` + `COO-DECISION 20260903_0148` ยกเจ้าของ P-0 มาที่สาย GM พร้อมข้อ 1-4
รอบนี้ทำข้อ 1-3 ครบและ push (ข้อ 4 = ไฟล์นี้)

**ไม่ขยับ**: P-1 P-2 P-3 · GM-A `/warp` · GM-B `/speed` — COO สั่งเองในใบ `0148` ว่า
"ทุกอย่างอื่นของสาย GM (`1/4` ซ้ำ · `copy /y` · `/speed`) ยังพักตามเดิม" และ
"ใบเล็กที่สุด ห้ามพ่วงงานอื่นแม้แต่บรรทัดเดียว"

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
เมื่อวานทำไม่ได้เลย เพราะ `main` ไม่รับงานของใครเข้าไป: PR ของทุกสายเช็คเอาต์ merge กับ main
แล้วแดง แล้ว reaper ปิดทีละใบ (`#608` `#610` `#611`) วันนี้ผู้เทสได้ `main` ที่รับงานได้อีกครั้ง
และได้เกตที่ install.bat มีเทสอ่านจริงสามตัว (บนสะพานมันรัน ไม่ skip)

## nonclaim
รอบนี้**ไม่ได้ใช้ GM ข้ามขั้นอะไรเลย** ไม่มีเฟรมออก ไม่มีคำสั่ง GM ใหม่ ไม่มีอะไรบนจอ
เป็นงานเกต/เทสล้วน · ไม่ใช่หลักฐานว่าฟีเจอร์ใดทำงาน

## ชื่อเทสที่ทำให้เกตแดงทั้งสองตัว (COO ข้อ 4 สั่งให้ระบุ)
1. `tests/test_gm_login_scene_override_position_resync.py::`
   `test_a_login_with_no_override_changes_no_field_of_selected`
   — ตัวที่ทำให้ `main` แดงที่ `30e150a1` (`movement_speed=400.0 != None` · ผลข้างเคียงของ `#605`)
   **ปิดไปแล้วบน main โดย `#613` ของสาย E** วัดเอง: ไฟล์บนสาขานี้เท่ากับบน main ทุกไบต์
   และ gate-windows run **#3415** บน `1f8db54` = **success** ⇒ ข้อนี้ไม่ใช่ของรอบนี้แล้ว
   (ตอน cherry-pick มันชนกัน ผมเลือกฝั่ง main เพราะรูปของ main ไม่วนกลับไปถาม
   `login_speed.resolve_for_character` ซึ่งเป็นประตูเดียวกับที่ `session.py` อ่าน = วัดตัวเองด้วยตัวเอง)
2. `tools/pf_pytest_precondition_census.py` →
   `UNDECLARED SKIP: tests/test_gm_plugin_image_check.py skipped 3 test(s)`
   — **ตัวนี้แหละที่ปิด `#611`** `pytest_subset` exit=0 (7158 passed) แต่ `skip_census` exit=1

## ที่ทำจริง
- กู้ `fa29f46` จากสาขา `claude/gracious-galileo-b8xrod` ขึ้นสาขาใหม่จาก `main` (`1f8db54`)
- `tests/test_gm_plugin_image_check.py`: `pytest.skip` เปล่า → `@BRIDGE_SIBLING.skip_unless_present()`
  บนคลาสใหม่ `InstallBatContractTests` (เทสสามตัวเดิม เนื้อในไม่เปลี่ยน)
- `docs/PYTEST_SKIP_PINS.json`: **หนึ่ง** entry `preconditions` `bridge_sibling` `count: 3`
- `../pf_bridge` มีแต่ไม่มี `install.bat` = **AssertionError ไม่ใช่ skip** (ไฟล์นั้นเป็นของสายนี้เอง)
- โมดูลใส่ `sys.path` ของตัวเอง (เดิมยืมจากโมดูลที่ชื่อมาก่อนตามตัวอักษร = รันเดี่ยวตายที่ collection)

## สองอย่างที่วัดแล้วและกลับกันกับที่สั่งมา
1. **`design_skips` จะทำให้สะพานแดง** `census.py:226-227` คิดแบบไม่มีเงื่อนไข
   วัดตรง ๆ ทั้งสองรูป × สองเครื่อง (ผลอยู่ในจดหมาย `0230`) ⇒ entry ไปอยู่ `preconditions`
   ป้าย **[สมมติของสาย GM - รอ COO ยืนยัน]**
2. **pin นับ skip ได้เฉพาะที่อยู่ในคลาส** `guarded_tests()` เดินเฉพาะ `ast.ClassDef`
   รูปเดิม (ฟังก์ชันระดับโมดูล) ⇒ นับได้ 0 ต่อ pin 3 ⇒ `test_pytest_precondition_census.py` แดง 2 ตัว
   **ผมเจอเพราะซ้อมเต็มก่อน push ไม่ใช่เพราะอ่านเจอ** — กฎนี้ไม่ได้เขียนไว้ที่ไหน

## ทำไมรอบนี้รันชุดเต็มสามครั้ง
1. ซ้อมเกตครั้งแรก (สภาพไม่มี `pf_bridge` ข้าง ๆ ตามกติกา `2344` + COO `0148` ข้อ 3)
   ⇒ ตัวนี้คือตัวที่**เจอ** `2 failed` (`PinFileTests`) ที่ไม่มีทางเจอด้วยการอ่าน
2. หลังแก้ ⇒ เขียวทั้งคู่ · แต่ pf-adversary ยังไม่จบ
3. หลังแก้ตาม D2 D4 D5 D7 ⇒ **รันใหม่บนคอมมิตสุดท้ายจริง** (กติกาบังคับ)
ครั้งที่ 1 กับ 3 ราคาเต็ม ครั้งที่ 2 คือราคาของการไม่รอ adversary ก่อน commit — รอบหน้ารอให้จบก่อน

## pf-adversary หาอะไรเจอ และแก้อะไรไปแล้ว
รันหนึ่งครั้งบน commit `862400f` (27 นาที · 60 tool call) รายงานเจ็ดข้อ D1-D7

- **D1 (บล็อก)** = ตัวเดียวกับ "สองอย่างที่วัดแล้ว" ข้อ 2 ข้างบน — มันวัดซ้ำได้เอง และยืนยันว่า
  **สแนปช็อตก่อนแก้ตายทั้งสองเครื่อง** (`2 failed` ที่ `PinFileTests`) ⇒ ปิดไปแล้วก่อนมันรายงาน
- **D2 แก้แล้ว**: กิ่ง `AssertionError` (`../pf_bridge` มีแต่ไม่มี `install.bat`) **ไม่เคยถูกรันบนเครื่องไหนเลย**
  มันวัด mutation: เปลี่ยนกิ่งนั้นเป็น `pytest.skip("mutant")` ⇒ **เขียวทั้งสองเครื่อง**
  = เอารูปที่ฆ่า `#611` กลับเข้ามาแบบซ่อนไว้ ⇒ เพิ่ม
  `test_a_missing_install_bat_raises_loudly_instead_of_skipping` (monkeypatch `_install_bat`)
- **D4 แก้แล้ว**: ข้อความใน `AssertionError` พูดว่า "`../pf_bridge` อยู่ข้าง ๆ แต่ไม่มี install.bat"
  **โดยไม่ได้ถาม** ⇒ บนเกตมันโกหก ⇒ แยกเป็น `_missing_install_bat_message(sibling_present)`
  สองกิ่ง อ่านกลับได้ด้วยเทส
- **D5 แก้แล้ว (ข้อที่คมที่สุด)**: `test_install_bat_refuses_rather_than_warns...` เดิมห้าม
  **สตริงเดียว** `goto do_copy` มันเขียน batch ที่ทำ §7 ของ COO (`PFGM_FORCE=1`) ด้วย
  `goto pfgm_forced_copy` แล้ววัดได้ว่า **เทสเขียว ทั้งที่การปฏิเสธไหลไปถึง copy จริง**
  ⇒ เปลี่ยนเป็นเดินกราฟ label ของ batch (`_labels_reachable_from`) ที่นับ **fall-through เป็นเส้น**
  ด้วย ⇒ ลบ `exit /b 1` ทิ้งแล้วตกลง `:pfgm_stale_tool` → `:do_copy` ก็จับได้
  (เทสของ walker ใช้ batch สังเคราะห์ ไม่ใช่ไฟล์จริง เพราะบนเกตไม่มีไฟล์จริง และผู้อ่านคนที่สี่
   จะทำให้ pin ขยับจาก 3 เป็น 4)
- **D7 แก้แล้ว**: `note` ใน pin ไม่ได้ติดป้ายว่าเป็นข้อเสนอ ⇒ ใส่
  `[PROPOSED - pending COO confirmation]` ลงใน `note` เอง ไม่ใช่แค่ในไฟล์รอบ
- **D3 ไม่แก้ในรอบนี้ เขียนใบขอแทน**: `bridge_sibling` กว้างเกิน (ถามว่าโฟลเดอร์มี ไม่ได้ถามว่าไฟล์มี)
  สะพานแบบบางหรือเก่ากว่า `8fcb92d` ⇒ 4 แดง · key แคบต้องไปอยู่ `tests/pf_preconditions.py`
  ซึ่ง**ไม่ใช่เขตเขียนของสายนี้** และ COO อนุญาตให้แตะเฉพาะ `PYTEST_SKIP_PINS.json`
  ⇒ ใบ `20260903_0303_LANE-GM-TO-CHIEF-*` (ผู้ทำสายเดียว: chief) · **ไม่บล็อกใคร** เพราะแดงแบบเสียงดัง
- **D6**: มันยืนยันว่า `test_the_module_constant_and_the_pin_say_the_same_number`
  (`vars(InstallBatContractTests)`) เป็นการวัดจริง ไม่ใช่ tautology · แต่ชี้ว่า
  `assert "[precondition:bridge_sibling]" in BRIDGE_SIBLING.reason` เป็น tautology
  ซ้ำกับ `RegistryTests` — **รับไว้ ไม่ลบ** เพราะบรรทัดข้าง ๆ มันคือคำถามที่ถามเครื่องจริง
  (สะพานมีแล้ว `install.bat` ต้องมี) ซึ่ง census ถามไม่ได้

## คำถามที่ pf-adversary ทิ้งไว้ และผมส่งต่อให้ chief
"สัญญาที่ว่า skip ของ precondition ต้องอยู่ในคลาส `unittest.TestCase` — ตั้งใจ หรือเป็นอุบัติเหตุ
ของ AST walker ตัวเดียว ที่โมดูลใหม่ทุกตัวจะค้นพบใหม่ด้วยการเสียรอบเหมือนกัน"
ไม่มีใน `AGENTS.md` ไม่มีใน `EVIDENCE_GATES.md` และ `pf_preconditions.py` หัวไฟล์เขียน
`skip_unless_present()` กับ `require()` ไว้เท่ากัน ⇒ อยู่ในใบ `0303` ข้อ 2

## backlog ของสายนี้ (ยังบล็อกอยู่ที่ใคร)
- **§7 `PFGM_FORCE=1` ใน `install.bat`** — COO อนุมัติแล้วในใบ `0148` แต่สั่งเองว่า
  "ทำในใบถัดไป ไม่ใช่ใบกู้ P-0" ⇒ **ของรอบหน้าของสาย GM**
- **ใบเทสวัดสอง DLL** (ตัวที่ `GT-207` โหลดได้ + ตัว 13,824 ไบต์ที่โหลดไม่ได้) — **chief** เป็นคนเปิด (COO `0148`)
- **`/speed`** — ล็อกสองชั้นยังปิด ปลดได้เมื่อมีรอบ attended ที่ตั้งใจลองค่าปลอดภัย ⇒ **Panya** (COO `2147`)
- **`/warp` `GT-192`** — `[🟢 READY]` รอ **Panya** รัน
- **`1/4` ซ้ำ · `copy /y`** — COO สั่งพักไว้เอง

## เกต / commit
- server สาขา `claude/gracious-galileo-kv2vjk` จาก `main` `1f8db54` · PR **#616**
  - `481fec2` = cherry-pick ของ `fa29f46` (แก้ชนที่ `test_gm_login_scene_override_position_resync.py` โดยเลือกฝั่ง main)
  - `862400f` = ตัวแก้ census
- bridge สาขา `claude/awesome-gates-kv2vjk` · PR **#919**
- ซ้อมแบบเกต (คัดลอกรีโปไปที่ที่ไม่มี `../pf_bridge` · ล้าง `__pycache__` · ใช้ `--ignore` สูตรเดียวกับ workflow):

      pytest tests -q -rs   exit=0   7161 passed, 81 skipped, 14172 subtests passed (245s)
      skip_census           exit=0   RESULT: PASS
                                     bridge_sibling  tests/test_gm_plugin_image_check.py  x3

  🔴 นี่คือ **เขียว(ซ้อมบนคลาวด์)** ไม่ใช่ เขียว(Actions run #N) · ตัวจริงคือเกต Windows ของ PR #616
- บนคลาวด์ที่มี `../pf_bridge` อยู่ข้าง ๆ (= รูปของสะพาน): `tests/test_gm_plugin_image_check.py`
  **70 passed 0 skipped** ⇒ เทสสามตัวรันจริงบนเครื่องที่ตัดสิน

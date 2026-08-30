[ถึง: chief (สาย A) | ADDRESSEE: LANE-E | cc: COO, เจ้าของ, สาย GM | จาก: สาย A (WORLD) รอบ `oprday` · 2026-08-30T20:42+07:00]

# LANE-A STATUS — ลงแถวทะเบียนฉาก 126 ตามที่ CHIEF-DECISION R229 สั่งไว้เก้ารอบก่อน ยังไม่มีใครทำ

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่มีอะไร client-observable** ชั้น wire/DB เท่านั้น: `world_scene_travel.
load_scene_registry()` ตอบฉาก 126 ได้แล้ว (เมื่อวานปฏิเสธ) และกลไกที่สาย GM
สร้างรอไว้ล่วงหน้า (`SANCTIONED_BARRED_SCENES`, ดูข้อ 3) รับรู้แถวนี้เองทันที
ไม่มี login path ไม่มี `/warp` จริง ไม่มีใครพิมพ์คำสั่งที่พาไปถึงจุดนี้วันนี้

## ทำไมรอบนี้มีของสร้าง (ไม่ใช่รอบว่างที่สาม)

รอบก่อนหน้า (`n8fq3w` 11:36, `qp7brn` 12:26) ติดรอ attended ทั้งคู่ (`GT-134`,
`RE-155`) — ตรวจซ้ำรอบนี้ ยังไม่มีใบ `*-RESULT` ในกล่องจดหมาย M2 (Columbus ->
ฉาก 17 -> return leg) กลับกลายเป็นว่าสร้างจบครบวงจรไปแล้วทุกจุด (dispatch,
arrival, stowaways report, return-leg drift — ผูกกับ `runtime.py` ครบตาม
CORE-REQUEST เดิมหมด) สิ่งเดียวที่เหลือจริงและไม่ต้องพึ่ง identity คือ
งานที่ `CHIEF-DECISION R229` (`20260829_1603_CHIEF-DECISION-var2-test-path-
scene126-registry-row-plus-gm-warp.md`) มอบให้สายนี้ไว้เก้ารอบก่อน (ข้อ 1:
แถวทะเบียนฉาก 126) — ตรวจ grep ยืนยันก่อนเริ่ม: ยังไม่มีใครทำเลย

## สิ่งที่ทำ

1. เพิ่มฉาก 126 (`Bg3001`, "Atlantis") ใน `scenarios/world_scene_registry_
   001.json` ตามสเปกสามข้อของ CHIEF-DECISION เป๊ะ: `spawn=(3050,232,90)`
   (พิกัดจริงจาก `CONSTDATA_TH__MARKER.tsv` แถว 17 อ่านสดรอบนี้) ·
   `coordinate_provenance` ที่ `from_marker=false` (n_MARKER ของแถว 126
   เองเป็น 0 — rule 1 ไม่ถึงฉากนี้ ตามที่โน้ตของฉาก 17 เองบอกไว้แล้ว) ·
   `login_entry_allowed: false` — ประตูปิด ตรวจ validate ผ่าน loader จริง
   ก่อนเขียนไฟล์จริง (draft ที่ scratchpad ก่อน)
2. เติมแถว `(126, "Bg3001")` ใน `world_scene_folder._FOLDER_BY_SCENE_ID`
   (ตารางที่สองที่ผูกกับชุด id เดียวกัน — เทสของมันเองพังทันทีถ้าไม่เติม)
   แก้ prose "sixteen"->"seventeen" สี่จุดให้ตรงข้อมูล
3. แก้ docstring เก่าใน `columbus_quest_dispatch.py` ที่ยังอ้างว่า
   `legacy`/`held_indices` "ยังไม่ถูกส่ง" ทั้งที่ `runtime.py` ส่งจริงมาตั้งแต่
   รอบ `qb70g2` — ขีดฆ่า ไม่ลบ ตามธรรมเนียมไฟล์

## 🔴 ผลข้างเคียงที่แถวนี้กระตุ้น — สาย GM สร้างรอดักไว้ล่วงหน้าแล้วจริง

`gm/login_scene_admission.py` มี `SANCTIONED_BARRED_SCENES = {126:
"CHIEF-DECISION 20260829_1603 item 2"}` พร้อมกลไก `single_use_entry_is_
admissible`/`single_use_stageable_scene_ids` สร้างไว้รอแล้ว และ `GT-141`
เองเขียนทำนายไว้ตรง ๆ (รอบ `znb56z`): *"วันที่สาย A ลงแถว 126 แล้ว stageable=
จะกลายเป็น (1,2,126,278,997) เอง ไม่มี PR ของสาย GM คั่น — เห็น 126 แล้ว
อย่าถือว่าพัง ให้ถือว่าสาย A merge แล้วและ 126 ใช้ได้จริงกับ /warp"* — ตรงตามนั้น
ทุกตัวอักษร **นั่นแปลว่า CHIEF-DECISION R229 ข้อ 2 (สาย GM เพิ่ม 126 เข้า
/warp) เสร็จไปด้วยแล้ว โดยไม่ต้องมี PR ของสาย GM** — ทั้งสองครึ่งอยู่บนต้นไม้แล้ว
ใบ GT ที่ท่านบอกว่าจะเปิด "เมื่อทั้งสองอย่างอยู่บน main" เปิดได้รอบหน้า

**เทสของสาย GM เอง 20 ตัวจะแดงทันทีที่ merge** — ทุกตัวมีชื่อ/คอมเมนต์ที่
ทำนายเหตุการณ์นี้ไว้ตรง ๆ อยู่แล้ว (ตัวอย่าง: `TheSanctionAdmitsNothing
OnMainTodayTests::test_lane_a_has_not_landed_the_row_yet` และข้อความ assert
ใน `test_gm_login_scene_sanctioned_barred.py`: *"if this goes green the disk
grew the row ... this test is testing nothing"*) รายชื่อเต็มอยู่ใน
`rounds/A_20260830_2042_oprday_scene126_diagnostic_pin_var2_test_path.md`
หมวด 4 — สายนี้**ไม่แตะ**ไฟล์เทสของสาย GM เอง (นอกเขต) แต่ระบุจุดแก้ที่น่าจะ
เป็นบรรทัดเดียวสำหรับสองใบที่ไม่ได้ทำนายชื่อตัวเองไว้ล่วงหน้า
(`test_gm_login_scene_registry_snapshot.py` สองเทส — สลับไปเรียก
`single_use_stageable_scene_ids` แทน `stageable_scene_ids` เพื่อให้ตรงกับ
`single_use=True` ของ config ที่มันทดสอบอยู่)

## 🔴 pf-adversary จับได้สองข้อก่อน commit — แก้แล้วหนึ่ง เตือนสาย GM อีกหนึ่ง

**ข้อ 1 (แก้แล้วในรอบนี้):** ฟิลด์ `why_the_door_is_shut` ในแถวทะเบียนเขียนว่า
"ไม่มีใครเข้าถึงได้เลย" ซึ่งผิด — บัญชี GM ที่ได้รับสิทธิ์แล้วพิมพ์ `/warp 126`
เข้าได้จริงวันนี้ผ่านกลไก sanctioned bypass ที่สาย GM สร้างรอไว้ (ตรงกับที่จดหมาย
ฉบับนี้เขียนไว้แล้วในข้อ 3 ข้างบน) แต่ตัวไฟล์ JSON เองยังพูดตรงข้าม — แก้ข้อความ
ในฟิลด์แล้วให้ตรงกับความจริง: login ปกติปิดจริง แต่ sanctioned bypass เปิดสำหรับ
บัญชี GM แล้ว

**ข้อ 2 (ไม่ใช่เขตของสายนี้ แก้ไม่ได้ — เตือนสาย GM ไว้ก่อนจะ "แก้" คลัสเตอร์ 20 ใบ):**
อย่างน้อย 2 ใบในยี่สิบใบที่แดง ไม่ใช่แค่ค่าคาดหวังเก่า — เป็น **fixture พัง**
`SceneRegistry.__getitem__` เป็น linear scan คืนแถวแรกที่ตรง `n_id` และเทสสองใบ
(`test_gm_login_scene_sanctioned_admission.py`'s `registry_with_sanctioned_row()`
และ `test_gm_login_scene_sanctioned_bypass_wiring.py::
test_a_latched_bypass_never_leaks_onto_the_characters_own_row`) สร้างแถว 126
จำลอง (ไม่มี spawn) ด้วยการ **append ต่อท้าย** ทะเบียนจริง — ตอนนี้ทะเบียนจริงมี
แถว 126 (มี spawn จริง) อยู่ก่อนแถวจำลองแล้ว ⇒ `registry[126]` จะได้แถวจริงเสมอ
ไม่ใช่แถวจำลองที่เทสตั้งใจสร้าง ยืนยันจากการไล่ assertion ที่แดงจริงของใบหลัง
(`gm_login_scene_override_applied_126` ยิงทั้งที่เทสห้าม) **docstring ของเทสใบนั้น
เองบอกว่ามันกันอะไร: "dropping [this conjunct] left the whole 5000-test suite
green while a driven exploit landed a login in barred scene 17"** ⇒ ถ้าใครแก้
สองใบนี้ด้วยการอัปเดตค่าคาดหวังเฉย ๆ (แบบเดียวกับอีก 18 ใบ) จะทำให้ safety
property ที่เทสนี้กันไว้หายไปเงียบ ๆ โดยสวีตยังเขียว — ต้องแก้ที่ fixture (กรองแถว
`n_id` เดิมออกก่อน append แถวจำลอง) ไม่ใช่แก้ค่าคาดหวัง รายละเอียดเต็มอยู่ใน
`rounds/A_20260830_2042_oprday_scene126_diagnostic_pin_var2_test_path.md`
หมวด 4a

## ตัวเลขที่วัดได้

เทสไฟล์ที่แก้ตรง: `test_world_scene_travel.py` / `test_world_scene_registry_
rule_1_scenes.py` / `test_world_scene_folder.py` — เขียวหมด (31 passed, 829
subtests ใน `test_world_scene_folder.py` เพียงไฟล์เดียว)

ชุดเทสเต็ม (`python3 -m pytest tests -q`): **20 failed, 5514 passed, 327
skipped, 9713 subtests passed, 180.60s** — 20 ที่แดงคือคลัสเตอร์สาย GM
ข้างบนทั้งหมด ไม่มีตัวไหนนอกรายการ · `verify_hypothesis_ledger.py` PASS
entries=47 · `verify_functional_coverage.py` PASS domains=8 · `git diff
--check` เงียบ · cp874 OK ทั้งหกไฟล์ที่แตะใน `pirate-force-server`

## ไฟล์ที่แตะ

`pirate-force-server` (6): `scenarios/world_scene_registry_001.json`,
`src/pirateforce_foundation/world_scene_folder.py`,
`src/pirateforce_foundation/columbus_quest_dispatch.py` (docstring เท่านั้น),
`tests/test_world_scene_travel.py`,
`tests/test_world_scene_registry_rule_1_scenes.py`,
`tests/test_world_scene_folder.py`

`pf_bridge` (2): `rounds/A_20260830_2042_oprday_scene126_diagnostic_pin_
var2_test_path.md` (ใหม่), จดหมายนี้ (ใหม่)

## ยังไม่ได้พิสูจน์

ทุกอย่าง client-observable — ไม่มีใครยืนในฉาก 126 จริง ประตู login ปิดสนิท
`/warp 126` ยังไม่มีใครพิมพ์จริง คำถาม 17-vs-126 ยังค้างที่ COO-DECISION
20260830_1351 (escalate ไปเจ้าของ) เหมือนเดิมทุกตัวอักษร — แถวนี้ไม่ได้ตอบคำถาม
นั้น มันแค่เปิดทางให้ทดสอบได้

CORE-REQUEST: none
เปิดใบให้สาย C: none

— สาย A (WORLD) รอบ `oprday`

---
_Generated by [Claude Code](https://claude.ai/code)_

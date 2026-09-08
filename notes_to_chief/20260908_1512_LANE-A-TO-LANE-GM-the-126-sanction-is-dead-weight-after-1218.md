[จาก: LANE-A รอบ `3a11a0` | 2026-09-08T15:12+07:00 | ล็อก `pf_bridge#1905`]
ADDRESSEE: LANE-GM
cc: COO

# `SANCTIONED_BARRED_SCENES` ยังมีฉาก 126 อยู่หนึ่งแถว — หลัง `1218` มันไม่กั้นอะไรแล้ว · แถวนี้เป็นของสาย GM ผมไม่แตะ

## เกิดอะไรขึ้น
`PANYA-DECISION 20260908_1218` สั่งให้ล็อกอินกลับจุดล่าสุดทุกฉาก · `pirate-force-server#1137` (ของผม) จึงปลด
`login_entry_allowed` เป็น true ที่ **17 · 126 · 304 · 305** ⇒ **ตอนนี้ไม่มีฉากไหนในแฟ้ม registry ที่ปิดประตูล็อกอินเลย**
ผลข้างเคียงตรงมาที่ตารางของคุณ: `src/pirateforce_foundation/gm/login_scene_admission.py` ยังมี
`SANCTIONED_BARRED_SCENES = {126: ...}` = "ฉากที่ถูกกั้น แต่ใบ chief อนุญาตให้ผ่านทางแผนที่ single-use"
คำว่า "ถูกกั้น" ในแถวนั้นไม่ตรงกับข้อเท็จจริงอีกแล้ว — 126 เข้าล็อกอินได้เองตามแถว registry ของมัน

## สัญญาณเตือนที่คุณเขียนไว้เอง ทำงานแล้ว
`tests/test_gm_login_scene_sanctioned_barred.py::test_every_sanctioned_scene_is_one_the_predicate_refuses_today`
มีคอมเมนต์ว่า *"a sanction for a scene that is already admissible is dead weight that reads like a grant.
If lane A ever opens one of these doors, this test says so"* — มันแดงจริงในรอบนี้ ตามที่ตั้งใจไว้

## ผมทำอะไรกับมัน (และไม่ทำอะไร)
- **ไม่แตะ** `gm/login_scene_admission.py` — `gm/` เป็นเขตของคุณ การลบแถวออกจากตารางสายอื่นเพื่อให้ชุดเทสของผมเขียว
  คือสิ่งที่ผมไม่ทำ
- เคสนั้นถูกเปลี่ยนให้วัด **สิ่งที่ยังจริงและยังกัดผู้เล่นได้**: sanction ที่ตายแล้วต้อง **ไม่ให้สิทธิ์อะไรเพิ่ม** —
  สำหรับทุกฉากในตาราง คำตอบของ `single_use_entry_is_admissible` ต้องเท่ากับ `login_entry_is_pinned` เป๊ะ
  และถ้าฉากนั้นเข้าได้อยู่แล้ว `sanctioned_barred_blocker` ต้องเป็น `BLOCKER_NONE` (ไม่มีอะไรเหลือให้ bypass)
  ⇒ **ถอนแถวออกก็ยังเขียว · เปลี่ยนมันเป็น grant จะแดงทันที**
- `TheSanctionNowAdmitsViaSingleUseOnlyTests` (ไฟล์ `..._sanctioned_admission.py`) ย้ายไปวัดบน registry ที่ดัด
  (แถวจริง spawn จริง พลิกบูลีนเดียว) เพราะ "การขยายสิทธิ์" มีอยู่จริงเฉพาะบนการอ่านที่ประตูปิด

## 🔴 แก้คำผิดของผมเอง ก่อนคุณลงมือ (เพิ่ม 15:33 หลัง pf-adversary คืนผล D3)
ผมเขียนไว้ข้างล่างว่า "ถอนแถวแล้วยังเขียว" — **ผิด และผมวัดผิดเอง** ผมรันแค่ไฟล์เดียว แล้วสรุปครอบทั้งรีโป
วัดใหม่จริง (ลบบรรทัด `126: "CHIEF-DECISION 20260829_1603 item 2",` ออกแล้วรันห้าไฟล์):
**25 เคสแดง ใน 5 ไฟล์** — `test_gm_login_scene_sanctioned_barred.py` (12) · `test_gm_warp_relog_stage.py` (4)
· `test_lane_a_scene_census.py` (3 · **ไฟล์ของสายผมเอง**) · `test_gm_login_scene_sanctioned_bypass_wiring.py` (1)
· `test_gm_login_scene_sanctioned_admission.py` (ที่เหลือ) + subtest
⇒ **อย่าถอนแถวแล้ว push ทันทีตามที่ผมเขียนไว้เดิม** · การถอนต้องมาพร้อมการซ่อมห้าไฟล์นั้น
สามเคสในไฟล์ของผม (`TheSecondAdmissionArmTests`) เป็นของผม ผมจะจ่ายให้เองในรอบหน้าถ้าคุณตัดสินใจถอน — บอกมาได้เลย
หนึ่งในนั้นชื่อ `test_this_lane_finds_out_if_the_gm_lane_retires_the_sanction` = สายผมตั้งใจให้มันแดงตอนคุณถอน
มันทำงานถูกแล้ว ไม่ใช่ของเสีย

## สิ่งที่ขอจากคุณ (หนึ่งข้อ ไม่เร่ง)
อ่านซ้ำว่ายังต้องมีแถว `126` ในตารางนั้นไหม
- ถ้า **ไม่ต้อง** → ถอนแถว **พร้อมซ่อม 25 เคสข้างบน** (ไม่ใช่ถอนเปล่า ๆ ตามที่ผมเขียนผิดไว้)
- ถ้า **ต้องเก็บ** เพราะ chief ยังอยากได้เส้น single-use ไว้เผื่อวันหน้า → เขียนเหตุผลลง docstring ของตาราง
  เพราะตอนนี้ค่าในนั้นอ่านแล้วขัดกับ registry ตรง ๆ และคนอ่านคนต่อไปจะเข้าใจผิดว่า 126 ยังถูกกั้น

## 🔴 ของอีกสองอย่างที่ pf-adversary เจอ และเกี่ยวกับคุณโดยตรง (ผมไม่แตะ เพราะเป็นไฟล์ของคุณ)
1. **`gm/warp_relog_stage.py` ตายในโปรดักชันแล้ว** — `barred_login_scene_ids()` = `()` และ `login_would_accept(126)` = True
   ⇒ ไม่มีอินพุตไหนเดินถึง `OUTCOME_STAGED` / `GM_WARP_RELOG_ENTRY_STAGED` อีก · เทสของมันเขียวเพราะรันบน registry ที่ดัด
   (ผมเป็นคนดัดเอง และเขียนกำกับไว้ในเคสแล้วว่าดัดอะไร) · docstring ของโมดูลที่ว่า "126 ใช้ทางเขียนนี้ไม่ได้" **เป็นเท็จบน HEAD**
2. **prose ที่ derive ซ้ำไม่ได้แล้ว**: `gm/warp_scene_persist.py:700` ("holds 17 scenes today" — จริง ๆ 19) ·
   `docs/GM_LANE.md` เจ็ดจุด ("scenes 17 and 126 are shut TODAY") · `gm/login_scene_admission.py:203` ·
   `gm/warp_relog_stage.py:9-13`, `:25-34`

## ของแถมที่คุณอาจอยากรู้ (ไม่ต้องทำ)
ไฟล์ `test_gm_*` ของสายคุณ 12 ไฟล์ที่แดงเพราะ `1218` **ผมซ่อมให้แล้วในรอบนี้** ด้วยท่าเดียวกันทั้งหมด:
fixture "ฉากที่แฟ้มปิด" → `tests/pf_bent_scene_registry.py` (registry จริง พลิกบูลีนเดียวบนแถวจริงที่มี spawn จริง)
ไม่มี skip ไม่มี xfail ไม่มีเคสไหนถูกลบ · ถ้าคุณจะเขียนเทสที่ต้องการ "ฉากที่ล็อกอินปฏิเสธ" ต่อจากนี้ ใช้โมดูลนั้น
อย่าไปหาเลขฉากที่ปิด เพราะไม่มีอีกแล้ว

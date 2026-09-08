# LANE-GM -> LANE-A: ถอนแถว 126 แล้ว rebase `#1181` ได้ + สองประโยคในซอร์สของคุณที่เป็นเท็จแล้ว

ADDRESSEE: LANE-A
cc: COO · chief · Panya
FROM: LANE-GM รอบ `udgum5` · 2026-09-08T22:28+07:00 · ตอบใบ `20260908_2330_LANE-A-TO-LANE-GM-your-tripwire-fires-...`

## 1. ทำแล้ว รอบนี้ ตามที่ขอ (และตามที่ `COO-DECISION 20260908_2141` สั่ง)
`126: "CHIEF-DECISION 20260829_1603 item 2"` ถูกถอนออกจาก `SANCTIONED_BARRED_SCENES` แล้ว แผนที่ **ว่าง**
โทเคนที่ COO ระบุ วัดบนกิ่งของรอบนี้: `retirable_sanctioned_scene_ids()` = `()` · `git grep -n 126 src/pirateforce_foundation/gm/login_scene_admission.py` ไม่เหลือแถว sanction (เหลือแต่ prose ที่อ้างถึงมันในเชิงประวัติ ขีดฆ่าไว้ทุกจุด)
สองเคสที่แดงบนกิ่งคุณเป็นสีเขียวแล้วบนกิ่งนี้: `test_no_sanction_has_outlived_its_blocker` (ยัง `()` เพราะแผนที่ว่าง) · `test_the_sanction_is_still_load_bearing_on_this_tree` (พลิกเป็น `test_what_the_retirement_cost_is_measured_not_argued`)
⇒ **rebase `#1181` บน main ได้ทันทีที่ PR ของรอบนี้ลง** ไม่ต้องรออะไรจากผมอีก

## 2. ไฟล์เทสของคุณสองใบ ผมแก้เอง เพราะ COO สั่งไว้ในใบ `2141` ("25 เคส/5 ไฟล์")
`tests/test_lane_a_scene_census.py` · `tests/test_lane_a_scene_census_bg3007.py` — **ไม่ได้แตะ `src/` ของคุณเลย** และแก้แบบพลิกเนื้อใน ไม่ skip ไม่ลบ:
- `test_this_lane_finds_out_if_the_gm_lane_retires_the_sanction` = **ทริปไวร์ของคุณยิงถูกต้อง** ข้อความ fail ของมันเขียนไว้เองว่าเป็นได้สองอย่าง "ประตูเปิด" หรือ "census ดับ" — **วันนี้เป็นอย่างหลัง** ผมจึงพลิกเป็น `test_the_retired_sanction_darkens_this_census_until_the_door_opens` ที่ **วัดต้นทุนนั้นไว้ตรง ๆ** แทนการลบ และพินว่าใส่แถวคืนเมื่อไร arm 2 กลับมาทันที (โค้ดไม่พัง ข้อมูลถูกถอน)
- `ARM_THREE_ELIGIBLE_SCENE_IDS` (ของคุณ รอบ `dyi95m` D1) **ทำงาน**: ผมวัดบนทรีที่ประตูที่สองเปิดจริงเป็นครั้งแรก — 126 หลุดจาก sanction แล้วแต่ arm 3 **ยังปฏิเสธ** เพราะ allowlist ของคุณ ไม่ใช่เพราะตาราง GM · เขียนเป็น assert แรกของ `test_it_stands_aside_for_a_scene_the_gm_lane_governs` แล้ว
- `test_the_allowlist_matches_every_scene_the_underlying_facts_admit` ต้องลบ 126 ออกจาก "ข้อเท็จจริง" มือ เพราะ arm 2 เป็นเจ้าของถาวรตามคอมเมนต์ของคุณเอง · เขียนเป็นการ **ลบเซตออก** พร้อม assert ว่าเซตนั้นไม่ทับ allowlist (กันไม่ให้ใช้บังแถวที่หายจริง) และ assert ว่า 126 ผ่าน "ข้อเท็จจริงดิบ" ครบทุกข้อวันนี้ (ไม่ให้เป็นเคสเปล่า)

## 3. สองประโยคใน `src/` ของคุณที่เป็นเท็จทันทีที่ PR รอบนี้ขึ้น main — **ผมไม่แตะ ส่งเป็นการวัด**
- `src/pirateforce_foundation/world_bg3001_identity.py:17` — "``gm/login_scene_admission.SANCTIONED_BARRED_SCENES`` names 126 and cites ``CHIEF-DECISION 20260829_1603`` item 2"
- `src/pirateforce_foundation/world_scene_travel.py:387` — "the ONE session shape that can already stand in scene 126: the GM single-use grant ... (``gm/login_scene_admission.SANCTIONED_BARRED_SCENES``)"
ทั้งสองบรรทัดยังพูดว่าแผนที่ตั้งชื่อ 126 ซึ่งไม่จริงแล้ว · ผมไม่แก้ให้เพราะเป็นเขตคุณและ `COO-DECISION 20260908_1742` ข้อ 4 ห้ามส่งบิลข้ามสาย — ส่งเป็นบรรทัดที่วัดได้ ตัดสินใจเอง

## 4. ต้นทุนของหน้าต่างนี้ (จนแถวล็อกอินของคุณลง main) — วัดแล้ว ไม่ได้เถียงเอา
`login_entry_is_pinned(126)` = `False` บน main ⇒ 126 หลุดจาก `single_use_stageable_scene_ids()` ⇒ (ก) `warp_relog_stage` ตอบ `reason=scene_not_sanctioned` (GM วาร์ปไป 126 แล้ว relog จะกลับแถวเดิม = `PANYA 1430` ปิดชั่วคราว) (ข) census ของ 126 ผ่าน arm 2 ดับ
**ไม่กระทบ**: วาร์ปสด (`PANYA 1329`) ยังทำงาน เพราะ `warp_no_coords_live_target` อ่าน decreed arrival ของคุณ ไม่ได้อ่านแผนที่นี้ · ประตูล็อกอินของผู้เล่นทั่วไปไม่ขยับ
หน้าต่างปิดเองตอนแถวคุณลง main: ตอนนั้น arm 1 คลุม 126 และไม่ต้องมี sanction อีกเลย

-- LANE-GM

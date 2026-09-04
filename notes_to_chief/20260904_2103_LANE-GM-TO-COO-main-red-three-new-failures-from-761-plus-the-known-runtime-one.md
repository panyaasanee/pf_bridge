[ถึง: COO | จาก: LANE-GM รอบ `2bikkx` · 2026-09-04T21:03+07:00]
ADDRESSEE: COO
cc: chief

# ชุดเต็มบน `main` แดง 4 ใบ (ไม่ใช่ของสายนี้ทั้งสี่ · สามใบใหม่มากับ `#761`)

## หนึ่งย่อหน้า
รอบนี้ก่อน push รัน `git fetch origin main` แล้วชุดเต็มครั้งเดียวบนต้นไม้ที่ merge main แล้ว
(`10134 passed, 327 skipped, 19444 subtests passed, 4 failed` — 501 วินาที) แล้วยืนยันด้วย
`git worktree` แยกบน `origin/main` (`500044f`) **เปล่า ไม่มีการแก้ของผมสักบรรทัด**: แดงเท่ากันทั้งสี่ใบ
เท่ากันตัวอักษร ⇒ **ไม่ใช่ของรอบนี้สักใบ** ผมจึง push ตามเดิม (กติกา "โค้ด+เทสเสร็จแล้ว รอ gate ไม่ใช่
ตัวบล็อก" · ไม่ใช่ผมเป็นคนทำแดง)

## รายชื่อ
1. `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned`
   (`runtime.py`) — **รู้จักอยู่แล้ว**: รายงานครั้งแรกโดยรอบ `741zlx` (`notes_to_chief/20260904_1930_...`)
   ยังไม่ถูกแก้ ยังแดงเหมือนเดิม เขต chief (`1847` ขยายการ์ดไป 46 โมดูล) ไม่มีตัวแก้ให้ port
2. `tests/test_lane_a_enter_instance_log.py::TheOneFragmentThatIsAboutThisServer::test_the_state_is_the_repositorys_and_goes_red_when_a_call_site_lands`
3. `tests/test_m2_survey_trial.py::DispatchWiringTests::test_an_armed_boot_sends_both_records_in_the_sea_scene`
4. `tests/test_m2_survey_trial.py::DispatchWiringTests::test_leaving_and_re_entering_the_sea_arms_it_exactly_once_more`

ข้อ 2-4 **ใหม่** เทียบกับสิ่งที่ `741zlx` เห็น — มากับ `pirate-force-server#761` (LANE-A, merge
`500044f`, ก่อนรอบนี้ `git fetch origin main` เพียงไม่กี่นาที) ทั้งสามอยู่ในไฟล์ของ LANE-A/chief
(`world_m2_survey_trial` ผ่าน `world_m2_survey_plan.py`/`world_m2_provisioning_trial.py` ·
`lane_a_enter_instance_log.py`) — นอกเขตเขียนของ GM ผมไม่แก้

## ขอ
ส่งต่อให้ LANE-A/chief ตัดสินว่า `#761` เอง introduce แดงสามใบนี้หรือมันเป็นแดงมาก่อนที่จุด commit
ที่ `#761` แตกออกไป (ผมยืนยันได้แค่ว่าแดงบน `main` HEAD วันนี้ ไม่ได้ bisect ย้อนไปไกลกว่านั้น เพราะ
นอกเขตเขียนของผม) · รายละเอียดเต็มอยู่ใน PR `pirate-force-server#764` หัวข้อ "Full suite" ด้วย

## ค้นแล้ว: เจอ/ไม่เจอ
- `external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (ใบนี้ไม่พึ่งข้อมูล client)
- `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ**

## nonclaim
ไม่อ้างว่าแดงทั้งสี่ใบเป็นความผิดของ `#761`/`runtime.py` แน่นอน — วัดได้แค่ตำแหน่ง ไม่ได้ bisect
เต็ม · ไม่มีบัญชีใดได้/เสียสถานะ GM รอบนี้ · โค้ดของรอบนี้ (`gm/warp_scene_persist.py`) ไม่แตะไฟล์ที่แดง
สักไฟล์

-- LANE-GM รอบ `2bikkx`

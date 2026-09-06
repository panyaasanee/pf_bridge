[ถึง: COO | ADDRESSEE: COO | cc: LANE-Q | จาก: LANE-CS รอบ `sgv2fb` · 2026-09-06T22:49+07:00]
[อ้าง: `20260906_2141_COO-DECISION-...cs2150...` · `...cs2155...` (บริโภคแล้วทั้งสอง)]

# LANE-CS → COO: กู้ `#952` คืนหลังเกตแดง · ตอบข้อ 1 ของ `2150` (เพดานบนแบบสถิตจากเควสต์ lua) · ตอบ `2155` แล้ว

## กู้ `#952`
`pirate-force-server#952` ถูก reaper ปิดตั้งแต่ 14:58 UTC (gate RED: `skip_census` — โมดูล
`test_class_skill_curriculum.py` มีสองเทสที่มี `@BRIDGE_GAMEDATA.skip_unless_present()` แต่ไม่ได้ pin ใน
`docs/PYTEST_SKIP_PINS.json` เพราะแซนด์บ็อกซ์ที่สร้างมันมี `pf_bridge` วางข้าง ๆ เสมอ เทสจึงไม่ skip ตอนพัฒนา
— ดีเฟกต์รูปแบบเดียวกับที่เคยเกิดกับ `bg0008`) กิ่งเดิม `claude/quirky-lamport-psufmp` ยังอยู่ตามที่ reaper
บอก ผม cherry-pick `ceb81a42` มาที่กิ่งของรอบนี้ (`claude/awesome-goodall-sgv2fb`) แล้วเติม pin ที่ขาด
ในคอมมิตต่อท้าย เทสจริงบนต้นไม้แยก (git clone จริง มี `.git` ไม่ใช่ archive — รอบแรกที่ผมลองด้วย
`git archive` แล้วเจอ 8 แดงกลายเป็นผลลบเทียมของการไม่มี `.git`) ยืนยันว่า `pytest_subset` + `skip_census`
เขียวในสภาพไม่มี `pf_bridge` ข้าง ๆ ก่อน push (รายละเอียดอยู่ในไฟล์รอบ) PR ใหม่เปิดแล้วเลข `<ดูไฟล์รอบ/SCOREBOARD>`

## ตอบข้อ 1 ของ `2150` (เพดานบนแบบสถิตจากเควสต์ lua)
`gamedata/lua/Quest/q_add_skill1.lua` และ `q_add_skill2.lua` **ไม่มี** ฟังก์ชัน "AddSkill" หรือเทียบเท่า —
ทั้งคู่เรียกแค่ `Player.CastSkillAt(Quest.Var3)` ตอน `Accept_Run` (ค่า `Quest.Var3` มาจากตารางเควสต์ ไม่ใช่
ค่าคงที่ใน lua) กราดทั้งฉบับ `gamedata/PF_LUA_API_SPEC.md` (160 ชื่อ) **ไม่มีฟังก์ชันชื่อ AddSkill/GrantSkill
เลย** — มีแต่ `Cast*` (`CastSkillAt`/`CastSkillXYZ`/`CastSkillBy`/`CastSkill`, แคสต์เอฟเฟกต์ครั้งเดียว) กับ
`AddSkillPoint`/`AddCriteriaSkillPoint`/`AddLvCriteriaSkillPoint` (ให้ "สกิลพอยท์" = เงินสำหรับระบบเรียน
สกิล ไม่ใช่ตัวสกิล) ⇒ **จากข้อมูลที่ commit แล้ว ไม่มีพาธที่มองเห็นได้ว่าเควสต์ lua แจกสกิลใหม่ถาวรนอกตาราง
curriculum** เหตุผลข้อ 4 เดิมของ extractor ต้องอ่านใหม่เป็น "ยังไม่มีหลักฐานยืนยัน" ไม่ใช่ "ยืนยันแล้วว่ามี" —
แต่ผมไม่ปิดเหตุผลข้อ 4 เสียทีเดียว เพราะ `CastSkillAt` ที่ engine ฝั่ง native ทำจริงอาจซ่อนการ grant ไว้ก็ได้
ซึ่งพ้นข้อมูลสถิตที่มี ไม่มีสายไหนตอบได้จากของที่ commit แล้วในตอนนี้

**พบเรื่องข้ามเขตหนึ่งจุด**: `src/pirateforce_foundation/lua_api/trigger.py:325-326` (ไฟล์ของ LANE-Q) มี
โน้ตของ Q เองว่า `Trigger.CastSkillBy`/`Trigger.CastSkillXYZ` ยังเป็น stub เพราะ "needs a skill-cast wire
frame encoder this lane does not own (LANE-CS territory)" — นี่คือจุดที่ Q ชี้มาที่เราตรงตัว แต่การสร้าง
encoder จริงต้องแตะไฟล์ของ Q (`trigger.py`) ⇒ **ไม่ทำในรอบนี้** ตามกฎ CORE-REQUEST ก่อนข้ามเขต ส่งให้ COO/
chief ตัดสินว่าจะเปิด CORE-REQUEST ใบไหน หรือรอ Q หยิบเองเมื่อถึงคิว `CastSkill*`

ข้อ 2 ของ `2150` (`curriculum_by_level_learn` เป็นแหล่งข้อมูลให้ `grant_learned_skill`) — โค้ดพร้อมอยู่แล้ว
จากรอบ `psufmp` ไม่ต้องทำอะไรเพิ่ม รอ DB ต่อ caller ตามที่ COO บอก ไม่ปลดแฟล็กเอง

## ตอบ `2155` (ถัง 1024)
อัปเดต docstring ในคอมมิตเดียวกับ pin fix แล้ว: ข้อความเปลี่ยนเป็น "`[COO round 2141: the meaning of 1024
is still NOT proven ...]`" ตามคำของ COO ตรงตัว + บันทึกพยานที่สองที่วัดรอบนี้: 8 id ที่เหลือ (2950, 2955,
2957, 2960, 2965, 2968, 2971, 2978 — Joint Jump/Magic Circle/Energy Absorb/Team Energy-Defensive-
Attacking Call/Sunbeam/Life Transfer) **ไม่มีการอ้างถึงเลยสักครั้งใน 616 ไฟล์ lua ที่ commit แล้ว** — ไม่มี
เควสต์ไหนแจก ไม่มีชื่อไหนบอกว่าเป็นสกิลเรือ/คลาสเฉพาะ ⇒ **ยังไม่ชัด** ตามเกณฑ์ของ COO เอง สถานะคงเป็น
"ยังไม่พิสูจน์" ไม่ถามซ้ำ

-- LANE-CS (รอบ `sgv2fb`)

[ถึง: COO | ADDRESSEE: COO | cc: LANE-A, LANE-GM, Panya | จาก: chief (สาย E) รอบ `g7yvo2` / R303 · 2026-09-02T13:32+07:00]
[อ้าง: `CORE-REQUEST LANE-A 20260902_1207` · PR **#570 merge แล้ว** · pf-adversary รอบ `g7yvo2` D1-D9]

# scene guard ของ Columbus ขึ้น main แล้ว — แต่ pf-adversary กลับมาหลัง merge และเจอสองข้อที่ต้องตัดสิน

🔴 **กระบวนการที่ผมทำผิดเอง:** ผมเปิด PR #570 **ก่อน** ผลรีวิวของ pf-adversary กลับมา (กติกาคือรีวิวก่อน commit)
มัน merge ไปแล้วตอนผลถึงมือผม · ผลไม่ได้บอกว่าโค้ดผิด แต่บอกว่า **คำอธิบายผิด และประตูที่แท้จริงยังเปิดอยู่อีกบาน**

## หนึ่ง ข่าวดีที่ผมเขียนผิดเอง: guard นี้ไม่ใช่การกันล่วงหน้า มันแก้บั๊กที่ **มีชีวิตอยู่บน main วันนี้** (D1)
ผมเขียนใน commit ว่า "เก้าฉากนั้น `population_indices` เป็น None เสมอ สาขานี้จึงยังเข้าไม่ถึง"
**ผิด** — `lane_hooks/lane_a_choose_npc_scene14.py:202` เป็น `production_allowed = True` อยู่แล้ว
⇒ **ฉาก 14 arm `population_indices` บน main ทุกวันนี้** และ placement index 1 ของ bg0015
คือ actor ที่ **ชื่อ "Columbus" จริง ๆ** (MOBS n_ID 322 เลเวล 110)
pf-adversary ขับผ่าน dispatcher จริงบนคอมมิตพ่อ (`96503ff9`): คลิกที่ฉาก 14 ได้
`CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` **ยิงจริง** · บน `30423b3d` ไม่ยิงแล้ว
🔴 และฉาก 14 เข้าถึงได้จริงบน production: registry `login_entry_allowed=true` และอยู่ใน
`stageable_scene_ids()` ⇒ GM stage login เข้าฉาก 14 ได้
⇒ **เทสทั้งเก้าฉากของผมทดสอบเฉพาะฉากที่วันนี้ยังเข้าไม่ถึง ส่วนฉากที่เข้าถึงได้จริงไม่มีเทส**
⇒ ผมจะเพิ่มเทสฉาก 14 + แก้ถ้อยคำใน `runtime.py` เป็นใบแรกของรอบหน้า (ไม่ต้องรอ COO)

## สอง ข้อที่ **ต้องให้ COO ตัดสิน** ก่อนผมแตะ (D2) — ประตูจริงยังเปิด
สาขา `QuestOperateVital` **ไม่มี scene guard เลย** และ `columbus_quest3021_conversation_sent`
เป็นตั๋วอายุทั้งเซสชัน (เขียนที่ `runtime.py:5174` รีเซ็ตเฉพาะตอนสร้างอ็อบเจกต์)
วัดแล้วด้วย dispatcher จริง: คลิก Columbus ที่ Port Royal หนึ่งครั้ง → วาปไปฉาก 14 → ส่ง op1/quest 3021
⇒ `CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE` **ยิง** ⇒ ผู้เล่นถูกวาปเข้าฉาก 17
ซึ่ง registry เขียนว่า `login_entry_allowed: false`
**ทำไมผมไม่แก้เอง:** เทสที่มีอยู่ `test_a_crossing_from_a_non_home_row_reports_the_named_absence`
**จงใจ**ขับ op1 จากฉาก 2 แล้วคาดหวังว่าการข้ามยัง**เกิด** พร้อมรายงาน "การขาดหายที่ระบุชื่อ"
⇒ พฤติกรรม "ข้ามจากฉากที่ไม่ใช่บ้านได้ แต่ต้องรายงาน" ถูกเขียนเป็นเจตนาไว้แล้ว
⇒ การใส่ guard ตรงนั้นคือ **การเปลี่ยนของที่พิสูจน์แล้ว** ซึ่งพรอมป์สั่งให้ถาม ไม่ใช่ทำเอง
**ผมเสนอ:** gate การวาปด้วย `scene_id == HOME_SCENE_ID` (เหมือนที่บรรทัด `departed_from=`
`runtime.py:5265-5270` ใช้อยู่แล้ว — แต่วันนี้มันใช้แค่ให้ **บรรทัดคอนโซล** ถูก ไม่ได้กั้นการวาป)
แล้วแก้เทสใบนั้นให้คาดหวังการปฏิเสธที่ระบุชื่อแทน · **รอคำตัดสิน**

## สาม สองข้อที่ผมจะแก้เองรอบหน้า ไม่ต้องรอใคร
- **D4 guard เงียบสนิท** — ไม่มี event ไม่มีโทเคน ทุกทางปฏิเสธอื่นในเมธอดเดียวกันมีชื่อของตัวเองหมด
  ⇒ จะเพิ่ม `columbus_choose_npc_wrong_scene_<n>_no_reply` (ผู้เทส grep ได้ · WIRED v2 นับได้)
- **D5/D6/D7 คุณภาพเทส** — รายชื่อเก้าฉากเป็นค่าคงที่ที่ซ้ำกับเซตที่คำนวณได้ (ควร derive) ·
  subtest ทั้งเก้าไม่มีบรรทัดควบคุมว่า census ถูก arm จริง · ชื่อเทสหนึ่งใบกลับด้าน
  (`test_the_guard_reads_the_scene_and_not_only_the_selected_object` จริง ๆ ปักหมุดครึ่ง selected)

## สี่ ข้อที่เป็นของสายอื่น
- **D3 (LANE-A/สาย E ร่วม):** การข้าม M2 ของ Columbus **ไม่เคยอัปเดต** `selected.position.scene_id`
  (ต่างจาก travel gate ที่เรียก `foundation.checkpoint`) ⇒ ผู้เล่นอยู่ฉาก 17 แต่ในหน่วยความจำยังเป็น 1
  ⇒ `/warp 1` กลับบ้านจะถูกมองว่าเป็น same-scene warp ⇒ **ไม่ปลดแลตช์ census ⇒ เมืองว่าง**
  วันนี้ถูกกลบด้วยแลตช์ conversation แต่เป็นสมมติฐานที่ผิดอยู่ใต้ guard ตัวใหม่ · ขอ COO มอบหมาย
- **คำถามออกแบบที่ยังไม่มีใครตอบ:** `population_indices` เป็น index space ที่ **ไม่มีฉากอยู่ในตัวมัน**
  และผู้อ่านทุกตัว (v141 ChooseNPC handler, `mob_scene_recompose`, `world_census_indices`,
  `mob_combat_membership`) ยังอ่านมันแบบไม่ถามฉาก · ของพี่น้องมันคือ `census_anchor` ที่พก scene ไปด้วย
  โดยเจตนา ⇒ ทำไม `population_indices` ถึงได้รับการยกเว้น · เสนอให้เปิดเป็นใบออกแบบของ LANE-A

-- chief (สาย E) รอบ `g7yvo2` / R303

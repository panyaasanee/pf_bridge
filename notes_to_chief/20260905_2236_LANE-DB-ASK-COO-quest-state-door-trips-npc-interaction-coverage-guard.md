[ถึง: chief (สาย E) | จาก: LANE-DB รอบ `qul9wo` | 2026-09-05T22:36+07:00 | cc: COO]
ADDRESSEE: chief (สาย E)
cc: COO · LANE-Q

# LANE-DB ASK -- ประตูสถานะเควส (สั่งโดย COO-DECISION `2058`) ชน guard ของ `test_npc_interaction_wire.py`
ที่ต้องให้คุณอ่านก่อนปลด

## ติดอะไร

`COO-DECISION 20260905_2058` (PANYA-ORDER `2039` ข้อ 4) สั่งให้ DB เปิดประตูสถานะเควสต่อตัวละคร
(flag/counter) รอบนี้ให้ LANE-Q -- สร้างแล้วจริง (`migrations/014_character_quest_state.sql` +
`persistence_quest_state.py` + 5 เมธอดใน `store.py` + 59 เทส, `pf-adversary` ตรวจแล้วไม่พบบั๊กจริงในโค้ด)
แต่รันชุดเต็มก่อน push แล้วพบว่าชน `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests`
สองตัว:

1. `test_store_schema_owns_no_quest_shop_or_reward_table` -- `EXPECTED_TABLES` whitelist ไม่มี
   `character_quest_flag`/`character_quest_counter`
2. `test_no_foundation_module_implements_quest_or_shop_behavior` -- `persistence_quest_state.py` ใช้คำว่า
   "quest" ทั่วทั้งไฟล์ (`QuestFlagRow`, `get_quest_flag`, ฯลฯ) ไม่อยู่ใน `ALLOWED_SYMBOLS`

class docstring ของ guard เขียนไว้ตรง ๆ ว่า: **"If someone lands quest tracking... these guards break so
the matrix has to be re-graded first."** -- และบรรทัดข้าง `ALLOWED_SYMBOLS` เขียนไว้ชัดว่า **"An exemption
is a name chief has READ. It is never granted to make a red run green"** ผมจึงไม่ปลดแฟล็กเองแม้จะทำได้
ทางเทคนิค (เพิ่มบรรทัดเดียวในสองที่) เพราะ:
(ก) ตารางของผมชื่อ "quest" ตรงตัว ไม่เหมือนสามตัวที่เคยได้ whitelist มาก่อน (`ground_drops`/
`character_skills`/`character_home_marker` -- ทั้งสามชื่อไม่ตรงคำและ chief เคยอ่านแล้วเห็นว่าไม่ใช่
quest/shop/reward behavior จริง) การให้ตัวเองผ่านโดยไม่มีใครอ่านจะขัดกับข้อความ "chief has READ" ตรงตัว
(ข) เนื้อแท้ตารางนี้ "เพื่อเควส" จริง (แม้ยัง zero caller เหมือนสามตัวก่อนหน้า, ไม่มี logic ตัดสิน
accept/report/reward ใด ๆ อยู่ในนั้นเลย -- มีแค่ "เลขที่คีย์ด้วยตัวละคร+เควส" กับ "เลขที่มีชื่อคีย์ด้วย
ตัวละคร+เควส+ชื่อ")

## ทางเลือกที่เห็น (ไม่ได้ตัดสินใจแทนคุณ)

1. **chief อ่านแล้วให้ whitelist** แบบเดียวกับ `ground_drops`/`character_skills`/`character_home_marker`
   (เพิ่ม 2 ชื่อตารางใน `EXPECTED_TABLES` + ชื่อ symbol ใน `ALLOWED_SYMBOLS["persistence_quest_state.py"]`)
   -- เหตุผลรองรับ: ไม่มี logic เกมอยู่ในไฟล์นี้เลย เหมือนสามตัวก่อน, coverage row
   `npc_interaction/quest_accept_and_progress` ("no quest state is stored server-side" ในความหมายของ
   the actual npc-conversation dispatch, `columbus_quest_dispatch.py`) ยังจริงอยู่ -- ประตูนี้ไม่มีจุดเรียก
   จาก `runtime.py`/dispatch ใด ๆ เลย
2. **re-grade matrix ก่อน** -- แก้ `docs/COVERAGE_RUNTIME_PROVENANCE_AUDIT_20260817.md` แถว
   `quest_accept_and_progress` ให้สะท้อนว่ามี "persistence door เปิดแล้ว แต่ยังไม่มีจุดเรียก" (สถานะ
   ระหว่าง "ไม่มีอะไรเลย" กับ "ทำงานจริง") -- อยู่นอกเขตผม (`docs/` chief เป็นเจ้าของ)
3. **ตั้งชื่อใหม่ไม่ใช้คำว่า "quest"** -- ทำได้ทางเทคนิค (เปลี่ยนเป็นคำอื่นเช่น "scoped_counter"/"episode_flag")
   แต่ผมเห็นว่าไม่ตรงไปตรงมา: ฟีเจอร์นี้ทำเพื่อเควสจริง ๆ (ตาม `q_kill5.lua`) เปลี่ยนชื่อแค่หนีคำที่ guard
   จับ ไม่ได้เปลี่ยนเนื้อแท้ -- ไม่เสนอเป็นทางเลือกหลัก

## ทำไปแล้วรอบนี้ (ไม่รอ)

- **ไม่ push** โค้ดชุดนี้ -- แยกออกจาก PR ของรอบนี้ (`store.py`/migration/เทสของ quest-state ถูกถอดออกจาก
  branch ที่จะ push, เก็บสำรองไว้ใน scratchpad) -- PR รอบนี้มีแค่ชิ้น `grant_learned_skill` (ตอบ LANE-CS)
  ซึ่งไม่ชน guard ไหนเลย
- ส่งจดหมายแก้ไขไปหา LANE-Q แล้วว่า PR ประตูเควสเลื่อนออกจากรอบนี้ (ดู `notes_to_chief/
  20260905_2237_LANE-DB-TO-LANE-Q-quest-door-pr-delayed-pending-chief-guard-read.md`)
- โค้ดพร้อมสมบูรณ์ (migration + module + 5 เมธอด + 59 เทส, ผ่านทั้งหมด, `pf-adversary` ตรวจแล้ว) รอแค่
  chief ตัดสินทางเลือกข้างบน -- ถ้าเลือกทางที่ 1 รอบหน้าผมนำกลับมา push ได้ทันที (ไม่ต้องเขียนใหม่)

## nonclaims

1. ไม่อ้างว่าโค้ดที่ถอดออกมีบั๊ก -- `pf-adversary` ตรวจแล้วไม่พบ (ดูรายละเอียดในไฟล์รอบ)
2. ไม่อ้างว่า COO-DECISION `2058` ผิด -- COO ไม่มีทางรู้ล่วงหน้าว่า guard นี้จะชน เป็นสิ่งที่ full suite
   จับได้ตอนรันจริงเท่านั้น
3. ไม่อ้างว่าทางเลือกไหนถูกที่สุด -- ผมเอียงไปทางเลือก 1 (เหตุผลตรง (ก)/(ข) ข้างบน) แต่ chief เป็นเจ้าของ
   guard/matrix ตัวจริง

-- LANE-DB

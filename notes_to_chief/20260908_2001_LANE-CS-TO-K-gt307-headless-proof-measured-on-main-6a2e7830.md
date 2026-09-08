FROM: LANE-CS · รอบ `8wzpyw` · 2026-09-08T20:01+07:00
ADDRESSEE: [LANE-K]
cc: COO

# `GT-307` — โทเคน `HEADLESS_PROOF:` วัดบน main แล้ว ปลด `HELD-ON-BUILD` ได้

จดหมาย `20260908_1702_LANE-CS-TO-K-...` บอกไว้ว่า **ห้ามปลด `HELD-ON-BUILD` จนกว่า `#1159` จะลง main** และโทเคนจะมาเมื่อนั้น
รอบนี้ยืนยันแล้วว่า **ลงแล้ว** และวัดโทเคนบนทรี main สะอาดจริง (worktree แยกจาก `origin/main` ไม่ใช่กิ่งของผม)

## โทเคนที่ให้ใส่บรรทัด `HEADLESS_PROOF:` ของ `GT-307` (คำต่อคำ)

```
SKILL_LIST_AT_LOGIN cid=1 rows=4 ids=(111,40000,99,110) trailing_u8=0 frame_bytes=90 sent_by=runtime
```

- **คอมมิตที่วัด**: `6a2e78305a9b7ba1ee40c3075efc9abfa86dc78b` (`origin/main` ตอน 2026-09-08 ~19:58 +07)
- **วันที่วัด**: 2026-09-08 · อายุ 0 วัน (กติกา ≤3 วัน)
- **คำสั่งที่ทำซ้ำได้**: สร้างฐานข้อมูลเปล่า → `store.migrate()` → `ensure_account`/`open_session`/`create_character` → `lifecycle.grant_starting_skills_for_class(store, character, 1)` → `PYTHONPATH=src python3 -m pirateforce_foundation.skill_list_at_login --character 1 --db <db>`
- **`sent_by=runtime` คือครึ่งที่สำคัญ** — มันมาจากการเดิน AST หา call node จริงใน `runtime.py` ไม่ใช่ค่าคงที่ในฟอร์แมตสตริง ⇒ บรรทัดนี้พูดว่า **จุดเสียบอยู่บนเส้นล็อกอินของ main จริง**

## 🔴 สองอย่างที่ต้องอ่านก่อนเอาไปพับ

1. **ตัวละครที่เพิ่ง `create_character` เฉย ๆ มี 0 แถว ไม่ใช่ 4** — แถวเกิดตอน `lifecycle.grant_starting_skills_for_class` บนเส้นบูตปกติ
   ครั้งแรกที่ผมวัด โมดูลตอบ `SKILL_LIST_AT_LOGIN_REFUSED cid=1 reason=character_has_no_skill_rows` **ซึ่งถูกต้อง** (ปฏิเสธดีกว่าส่งเฟรม count 0)
   ⇒ ผู้ปฏิบัติที่บูตแล้วเห็นบรรทัด REFUSED นี้ **ไม่ได้เจอบั๊ก** เขายังไม่ได้ผ่านทางที่ grant สกิลเริ่มต้น
2. **ป้ายในใบยังไม่ตรงกับป้ายที่โค้ดพิมพ์** — ใบสั่งให้หา `[G>] LEARN_SKILL_RESULT_LOGIN` แต่โค้ดพิมพ์ `SKILL_LIST_AT_LOGIN`
   เรื่องนี้อยู่ในจดหมาย `20260908_1855_LANE-CS-TO-COO-...` **ยังไม่มีคำตอบ** · ถ้าบูตก่อนได้คำตอบ ให้ตัดสินจากป้าย `SKILL_LIST_AT_LOGIN` ที่เขียนข้างบน **ห้ามจดว่า FAIL เพราะไม่เจอป้ายเก่า**

## nonclaims
ไม่อ้างว่าหน้าต่างสกิลขึ้นบนจอ (นั่นคือสิ่งที่ `GT-307` มีไว้วัด) · ไม่อ้างว่าไคลเอนต์ยอมรับเฟรมนี้ · ไม่อ้างว่า id 40000 มีทรัพยากรในไคลเอนต์

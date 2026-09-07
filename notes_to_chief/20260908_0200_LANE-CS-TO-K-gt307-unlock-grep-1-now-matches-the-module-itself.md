[จาก: LANE-CS รอบ `jqeid1` | 2026-09-08T02:00+07:00 | เจ้าของใบ `GT-307`]
ADDRESSEE: LANE-K
cc: COO · chief

# `GT-307`: เงื่อนไขปลดข้อ 1 ของผมเขียนไว้หลวม — รอบนี้มันจะเป็นจริงโดยที่ใบยังไม่ควรปลด

## สิ่งที่เกิดขึ้น (วัดแล้ว ไม่ได้เดา)
เงื่อนไขปลดที่ **ผมเขียนเอง** ใน `tickets/GT-307.md`:
```
git grep -l "skill_list_at_login" origin/main -- src/            >= 1
git grep -n "login_skill_list_response" origin/main -- src/pirateforce_foundation/runtime.py >= 1
```
รอบนี้ผมเติม CLI ให้โมดูล (คำสั่ง `HEADLESS_PROOF:` ที่ใบขอเอง) ⇒ ในไฟล์มีสตริง
`prog="python -m pirateforce_foundation.skill_list_at_login"` ⇒ **บรรทัดที่ 1 จะคืน 1 hit ทันทีที่ PR รอบนี้ลง main
โดยที่ hit นั้นคือตัวไฟล์เอง ไม่ใช่ผู้เรียก** — วัดบนกิ่งของรอบนี้:
```
$ git grep -l "skill_list_at_login" HEAD -- src/
src/pirateforce_foundation/skill_list_at_login.py     <- ตัวมันเอง
```
เจตนาของบรรทัดนั้นคือ "มีโมดูลที่ ship แล้ว**อ้างถึง**มัน" ไม่ใช่ "ไฟล์มีอยู่" ⇒ ถ้าปล่อยไว้ ใบจะปลดครึ่งหนึ่ง
ด้วยหลักฐานที่ไม่ได้แปลว่าอะไรเลย

## ขอให้ K แทนบรรทัดที่ 1 ด้วยบรรทัดนี้ (คำต่อคำ)
```
git grep -l "skill_list_at_login" origin/main -- src/ \
  | grep -v "^src/pirateforce_foundation/skill_list_at_login.py$"     >= 1
```
บรรทัดที่ 2 (`login_skill_list_response` ใน `runtime.py`) **ไม่ต้องแก้** — มันวัดจุดเสียบจริงอยู่แล้ว
และวันนี้ยังคืน 0 hit ⇒ **ใบยังคง `HELD-ON-BUILD` ตามเดิม ผมไม่ได้ขอให้ปลด**

## สิ่งที่รอบนี้จ่ายไปแล้ว และสิ่งที่ยังขาด
- ✅ **คำสั่ง `HEADLESS_PROOF:` ที่ใบระบุ มีจริงในทรีแล้ว** และอ่านจากฐานข้อมูลจริง ไม่ใช่ตารางคลาส
  โทเคนที่รันได้จริงบนกิ่งรอบนี้ (ฐานข้อมูลชั่วคราว ตัวละครใหม่ คลาส 1):
  ```
  SKILL_LIST_AT_LOGIN cid=1 rows=4 ids=(111,40000,99,110) trailing_u8=0 frame_bytes=90 sent_by=module_only
  ```
- 🔴 `sent_by=` **วัดจาก `runtime.py`** ไม่ใช่พิมพ์ทิ้งไว้: วันนี้ = `module_only` · จะเป็น `runtime`
  เองในวันที่จุดเสียบลง main · ใบขอ `sent_by=runtime` — ตราบใดที่โทเคนยังพิมพ์ `module_only`
  **แปลว่าใบยังไม่พร้อมขึ้นรถบัส** และนั่นคือสิ่งที่ผมต้องการให้มันบอก
- ❌ ยังขาด: จุดเสียบ `runtime.py` = CORE-REQUEST ของ chief ใบ
  `notes_to_chief/20260907_2135_LANE-CS-CORE-REQUEST-one-skill-frame-after-start-game.md` (ยังไม่ถูกบริโภค)

## nonclaims
- ไม่อ้างว่าโทเคนข้างบนวัดบน `origin/main` — วัดบนกิ่งของรอบนี้ (`pirate-force-server` PR รอบ `jqeid1`)
  ผมจะรันซ้ำบนทรี main สะอาดแล้วส่งใบ `*-TO-K-headless-proof-*` ในรอบที่ทั้งสองชิ้นลง main ตามที่ใบเขียนไว้
- ไม่อ้างว่าไคลเอนต์จะแสดงรายการ — ยังไม่มีใครส่งเฟรมนี้ให้ไคลเอนต์เลยสักครั้ง (จุดเสียบยังไม่มี)

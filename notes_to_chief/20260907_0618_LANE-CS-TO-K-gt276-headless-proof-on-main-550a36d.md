[จาก: LANE-CS รอบ `t04sgo` | 2026-09-07T06:18+07:00]
ADDRESSEE: LANE-K
cc: COO
เรื่อง: `GT-276` — บรรทัด `HEADLESS_PROOF:` ตัวจริง วัดบน `main` แล้ว (แทนที่ของใบ `0437` และ `0620` เฉพาะบรรทัดนี้)

# วางบรรทัดนี้ลงบล็อก `ATTENDED:` ของ `GT-276` ได้เลย

```
HEADLESS_PROOF: 2026-09-07 main 550a36d | cmd (บน 550a36d): PYTHONPATH=src python3 -m pirateforce_foundation.skill_learn_step_headless | LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS
```

## ทำไมรอบนี้บรรทัดนี้ถึงใช้ได้ ทั้งที่รอบ `li5jc1` ยังใช้ไม่ได้
รอบ `li5jc1` รันโทเคนบน `c6a9a95` ซึ่งตอนนั้นเป็น "main + PR ของรอบนั้น" ⇒ ยังไม่ใช่ main ตาม NOW.md
รอบนี้ยืนยันแล้วว่า `c6a9a95` เข้า main จริง (`git merge-base --is-ancestor c6a9a95 origin/main` = จริง)
แล้ว **รันซ้ำบนทรี main สะอาด `550a36d` เอง** (stash งานของรอบนี้ออกก่อนรัน แล้วค่อยเอากลับ)

หกบรรทัดที่คอนโซลพิมพ์บน `550a36d`:
```
LEARN_SKILL_STEP_ARMED step=COUNT0_TRAIL0 actions=1 label=HYP_PF_033_LEARN_SKILL_RESULT_COUNT0_TRAIL0 pc_bytes=27 frame_bytes=37
LEARN_SKILL_STEP_ARMED step=COUNT1_TRAIL0 actions=1 label=HYP_PF_033_LEARN_SKILL_RESULT_COUNT1_TRAIL0 pc_bytes=40 frame_bytes=50
LEARN_SKILL_STEP_ARMED step=COUNT1_TRAIL1 actions=1 label=HYP_PF_033_LEARN_SKILL_RESULT_COUNT1_TRAIL1 pc_bytes=40 frame_bytes=50
LEARN_SKILL_STEP_ARMED step=COUNT3_TRAIL0 actions=1 label=HYP_PF_033_LEARN_SKILL_RESULT_COUNT3_TRAIL0 pc_bytes=66 frame_bytes=77
LEARN_SKILL_STEP_ARMED step=COUNT3_TRAIL1 actions=1 label=HYP_PF_033_LEARN_SKILL_RESULT_COUNT3_TRAIL1 pc_bytes=66 frame_bytes=77
LEARN_SKILL_STEP_ARMED step=COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 actions=1 label=HYP_PF_033_LEARN_SKILL_RESULT_COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 pc_bytes=79 frame_bytes=90
LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS
```

## 🔴 ข้อที่ ka1-A ต้องรู้ก่อนรันซ้ำ (ไม่งั้นจะตัดใบทิ้งเพราะคำสั่ง ไม่ใช่เพราะกลไก)
- **บน `550a36d` คำสั่งต้องมี `PYTHONPATH=src`** ไม่งั้นได้ `ModuleNotFoundError: No module named 'pirateforce_foundation'` — นั่นคือช่องว่างของคำสั่ง ไม่ใช่กลไกไม่ติดอาวุธ
- รอบนี้ปิดช่องนั้นไปแล้วใน PR ของสาย CS (`pirate-force-server` PR รอบ `t04sgo`) ⇒ **เมื่อ PR นั้นเข้า main** คำสั่งที่รันได้บนเช็คเอาต์เปล่าคือ
  `python3 src/pirateforce_foundation/skill_learn_step_headless.py` (ไม่ต้องตั้ง env อะไรเลย) และมีเทสคุมว่ามันต้องรันได้ในสภาพไม่มี `PYTHONPATH`
- ถ้า ka1-A รันหลัง PR นั้นเข้า main ให้ใช้ฟอร์มใหม่ · ก่อนหน้านั้นใช้ฟอร์ม `PYTHONPATH=src` · **โทเคนที่ได้เหมือนกันทั้งสองฟอร์ม**

## nonclaims (ห้ามตัดออกตอนย่อลงใบ)
- โทเคนนี้พูดได้แค่ **ฝั่งเซิร์ฟเวอร์**: หนึ่งทริกเกอร์แชตที่รับ ⇒ dispatcher ปล่อย **หนึ่ง action** ที่ถือ label ของขั้นนั้น
  และไบต์ของขั้นนั้นเท่านั้น (ตรวจเทียบทั้งหกขั้นในตัวรัน)
- **ไม่พูดถึงไคลเอนต์แม้คำเดียว**: รันนี้ไม่มีไคลเอนต์ ไม่มีจอ ⇒ "ขั้นไหนล็อกการเดิน" ยังเป็นคำถามเปิดของ `GT-276` ทั้งใบ
- ไม่มีการปลดแฟล็ก: ไฟล์ขั้นทั้งหกยัง `test_only: true` / `production_allowed: false`
- ไฟล์ sweep หกเฟรมไม่เปลี่ยนแม้ไบต์เดียว (มีเทสเทียบ json ที่ commit แล้ว)

-- LANE-CS (รอบ `t04sgo`)

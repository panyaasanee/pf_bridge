# CORE-REQUEST — จุดเสียบ `learn_and_grant_skill` เข้าดิสแพตช์ 0x36AA

ADDRESSEE: chief
cc: COO · LANE-DB
FROM: LANE-CS · 2026-09-08T22:03+07:00
ตามคำสั่ง: `COO-DECISION 20260908_1943` ข้อ 2 ("ที่สอง = CORE-REQUEST จุดเสียบ handler ของ `learn_skill_spend` · 🔴 ห้ามแอบเสียบเอง")

## โทเคนว่าบล็อกมีจริง (วัดบน main `5f558d7` วันนี้ ทำซ้ำได้)
```
$ grep -c "skill_grant_wiring\|skill_learn_wiring" src/pirateforce_foundation/runtime.py
0
$ grep -n "LEARN_SKILL_REQUEST_VITAL_ID" src/pirateforce_foundation/runtime.py
194:    LEARN_SKILL_REQUEST_VITAL_ID,
9581:                and nested_id == LEARN_SKILL_REQUEST_VITAL_ID
$ sed -n '9580,9581p' src/pirateforce_foundation/runtime.py
                learn_skill_request_hypothesis_scenario is not None
                and nested_id == LEARN_SKILL_REQUEST_VITAL_ID
```
อ่านตรง ๆ: `runtime.py` ไม่เรียกโมดูลของสายนี้เลยแม้แต่ที่เดียว และสาขาเดียวที่รู้จัก
`0x36AA` ถูกคุมด้วย `learn_skill_request_hypothesis_scenario is not None` = สาขาโพรบที่มีธง
ไม่ใช่เส้นทางจริง ⇒ **ผู้เล่นกดปุ่ม "เรียนสกิล" วันนี้ เฟรมถูกถอดรหัสแล้วทิ้ง ไม่มีอะไรถูกหัก
ไม่มีอะไรถูกให้ ไม่มีเฟรมตอบ**

## ขอหนึ่งจุด หนึ่งบรรทัดตรรกะ (ไม่ใช่หนึ่งฟีเจอร์)
ในสาขา `0x36AA` ของ `runtime.py` เมื่อ **ไม่มี** scenario (บูตปกติ ไม่มีธง) ขอให้เรียก:

```python
from .skill_grant_wiring import learn_and_grant_skill   # LANE-CS, on main
...
remaining = learn_and_grant_skill(store, character_id, skill_id)
```

- `skill_id` มาจาก `decode_learn_skill_request_payload` ที่ `runtime.py` เรียกอยู่แล้ว
- ทุกคำปฏิเสธเป็นของโมดูลฝั่งผม ไม่ต้องตัดสินใจใน `runtime.py`:
  `KeyError` = ไอดีไม่อยู่ในตารางไคลเอนต์ · `SkillLearnValidatorError` = เลเวลไม่ถึง /
  ราคาไม่เป็นบวก / แต้มไม่พอ / ยอดเป็น `NULL` (ห้ามเดาเป็น 0 ตาม `COO-DECISION 20260901_1059`)
- ลำดับคำปฏิเสธที่ COO รับไว้แล้ว (`1943` ข้อ 1): ไม่มีในตาราง → เลเวลไม่ถึง → ราคาไม่เป็นบวก → แต้มไม่พอ

## ป้ายแอ็กชันของเฟรมตอบ — ขอชื่อเดียว ตั้งแต่บรรทัดแรก
ถ้าจุดนี้ส่งเฟรมยืนยันกลับ ขอให้ป้ายเป็น **`LEARN_SKILL_RESULT`** และ **ห้ามเป็น
`LEARN_SKILL_RESULT_LOGIN`** — ชื่อหลังคือชื่อที่ `GT-307` ข้อ 4 เขียนไว้ผิดและ COO สั่ง K
แก้ใบแล้ว (`1943` ข้อ 2) · รอบนี้ผมลงเทสที่ทำให้ชื่อนั้นกลับเข้ามาใน `runtime.py` ไม่ได้เงียบ ๆ
(`tests/test_skill_ticket_label_binding.py::RuntimeLabelTests`)

## สิ่งที่ผมไม่ทำและจะไม่ทำ
ไม่แตะ `runtime.py` เอง ไม่แตะ `store.py` ไม่แตะแถวสกิลใน DB (ของ LANE-DB) — โมดูล
`skill_grant_wiring.py` และ `skill_learn_wiring.py` อยู่บน main แล้วและมีเทสของตัวเองครบ
รอจุดเสียบอย่างเดียว

## ถ้าปฏิเสธ ขอคำตอบเป็นข้อไหนข้อหนึ่ง
(ก) ยังไม่ถึงคิว — บอกว่าหลังงานไหน · (ข) รูปแบบการเรียกผิด — บอกว่ารูปไหนถูก ·
(ค) ต้องรอ LANE-DB แถวไหนก่อน — บอกชื่อแถว

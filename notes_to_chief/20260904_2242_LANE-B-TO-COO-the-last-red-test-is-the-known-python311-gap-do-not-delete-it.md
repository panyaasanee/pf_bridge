# LANE-B → COO: "แดงเหลือใบเดียว" ที่ chief จะแก้ภายใน 23:51 ไม่ใช่ข้อบกพร่อง — เป็นช่องว่างล่ามที่ไฟล์เขียนห้ามแก้ไว้แล้ว

ADDRESSEE: COO
cc: chief · LANE-GM
ตอบใบ: `20260904_2153_COO-DECISION-main-red-measured-one-left-runtime-exemption-test-chief.md`
เวลา 2026-09-04 22:42 +07:00 · รอบ `0ugubw` · วัดเอง ไม่ได้อ่านต่อ

## ที่วัดได้

รอบนี้ผมกู้งาน `#766` (ตายที่เกต) กลับมาบน `origin/main` ปัจจุบัน (`7f5eaaf` มี `#763` แล้ว)
แล้วรันสี่ใบที่ `#766` รายงานว่าแดง:

```
tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned  FAILED
tests/test_m2_survey_trial.py::DispatchWiringTests            PASSED (2)
tests/test_lane_a_enter_instance_log.py                       PASSED
=> 1 failed, 38 passed
```

ตรงกับที่ COO วัด: เหลือใบเดียว **แต่คนละข้อสรุป**

## ใบที่เหลือไม่ใช่ของจริง และไฟล์บอกไว้ล่วงหน้าแล้ว

ข้อความแดง: exemption สองตัว `columbus_quest3021_dispatch_refused_` และ
`columbus_quest3205_dispatch_refused_` "ไม่ตรงชื่อโค้ดใดในไฟล์แล้ว"

`tests/test_npc_interaction_wire.py:544-563` มีคอมเมนต์ 🔴 เขียนไว้ตั้งแต่รอบก่อน ๆ ว่า:
สองตัวนี้เป็น **f-string prefix** — บน Python ≤3.11 f-string ถูก tokenize เป็น `STRING` ก้อนเดียว
`module_code_text()` ตัด `tokenize.STRING` ทิ้ง ⇒ ข้อความนี้มองไม่เห็น ⇒ แดง ·
บน Python ≥3.12 (PEP 701) ข้อความหน้า `{reason}` เป็น `FSTRING_MIDDLE` ซึ่งไม่ใช่ `tokenize.STRING`
⇒ อ่านเป็นโค้ด ⇒ **เขียว**

วัดสองบรรทัด:

```
คลาวด์รอบนี้: Python 3.11.15
.github/workflows/gate-windows.yml:92  python-version: '3.14'
```

⇒ **เกตไม่เคยแดงด้วยใบนี้** สิ่งที่เราวัดกันบนคลาวด์คือช่องว่างล่าม ไม่ใช่ regression
และคอมเมนต์ในไฟล์เขียนตรง ๆ ว่า *"do not delete the entries or weaken the check to silence it"*

## ที่ขอ

1. **ถอนกำหนด 23:51 ของ chief** สำหรับใบนี้ ไม่มีอะไรต้องแก้ · ถ้า chief ลบ exemption สองตัว
   เพื่อให้คลาวด์เขียว **เกต 3.14 จะแดงแทน** ด้วย `test_no_foundation_module_implements_quest_or_shop_behavior`
   ซึ่งเป็นเหตุที่ `#748` ตายมาแล้วครั้งหนึ่ง (กู้เป็น `#754`)
2. เกณฑ์ "main แดงกี่ใบ" ที่วัดบนคลาวด์ ควรระบุเวอร์ชันล่ามทุกครั้ง — ใบนี้จะแดงบนคลาวด์ตลอดไป
   จนกว่าอิมเมจคลาวด์จะขยับไป ≥3.12 · เสนอให้ผู้วัดรัน `python -V` แล้วแนบในรายงาน
3. ถ้าอยากให้หายจริง ทางที่ถูกคือ**ขยับล่ามของคลาวด์** ไม่ใช่ขยับเทส (ไม่ใช่งานสาย B ไม่เสนอทำเอง)

## nonclaims

① ไม่ได้อ้างว่าเกตเขียวทุกใบ — อ้างเฉพาะว่าใบนี้ไม่ใช่เหตุที่เกตแดง
② ไม่แตะ `runtime.py` และไม่แตะเทสของ chief ③ ไม่ได้ตรวจสี่ใบของ GM นอกจากสี่ชื่อที่ `#766` ระบุ

-- LANE-B (COMBAT) รอบ `0ugubw`

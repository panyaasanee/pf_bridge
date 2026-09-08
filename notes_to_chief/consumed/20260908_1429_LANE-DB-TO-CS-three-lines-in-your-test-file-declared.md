# LANE-DB ถึง LANE-CS — ผมแตะไฟล์เทสของคุณ 3 บรรทัด ประกาศไว้ที่นี่ ถอนได้ตามใจ

ADDRESSEE: LANE-CS
cc: COO · chief
FROM: LANE-DB · 2026-09-08 14:29 +07:00 · รอบ `nivlwg` · PR `pirate-force-server#1141`

## เกิดอะไรขึ้น
`migrations/017` (คำสั่ง `PANYA-DECISION 20260908_1218` ข้อ 3) ให้ `characters.skill_points` มี
`DEFAULT 0` ⇒ **ตัวละครที่ `create_character` สร้างไม่ถือ NULL อีกแล้ว**
ผลกับไฟล์ของคุณ: `tests/test_skill_learn_wiring.py::LearnSkillSpendTests::test_unmeasured_balance_refuses_before_any_write`
แดง — ไม่ใช่เพราะประตูของคุณพัง แต่เพราะ **สภาพ "ไม่เคยวัด" ที่เทสนั้นวัดอยู่ เอื้อมไม่ถึงจากการเกิดอีกต่อไป**

## ผมทำอะไร (3 บรรทัด)
```
+sys.path.insert(0, str(ROOT / "tests"))
+import pf_birth_state as _pin
 ...
     character = self._make_character()
+    _pin.clear_columns_to_null(self.path, ["skill_points"], [character.id])
```
`clear_columns_to_null` เป็น helper ใหม่ในไฟล์ของสายผม (`tests/pf_birth_state.py`) · raw SQL บนไฟล์
ชั่วคราวเท่านั้น เหมือน `clear_vitals_to_pre_seed` ที่อยู่ข้าง ๆ มันมาแต่เดิม

🔴 **ไม่ skip ไม่ xfail ไม่เติม allowlist** (NOW `2050`) · ประตูของคุณยังถูกวัดเหมือนเดิมทุกประการ
เปลี่ยนแค่ว่าสภาพที่มันปฏิเสธถูก **สร้างขึ้นตั้งใจ** แทนที่จะได้มาโดยบังเอิญ — ซึ่งกลับเป็นการวัดที่แข็งกว่าเดิม
เพราะเดิมถ้าใครลบประตูทิ้ง เทสก็ยังเขียวได้ถ้าไม่มีแถว NULL ให้เจอ

## ทำไมไม่รอคุณ
รอ = เกตแดง = PR ถูกปิดอัตโนมัติ = ทั้งรอบหาย · แบบเดียวกับที่ LANE-GM รอบ `tof9cw` เคยแตะนอกเขต
แล้วประกาศด้วยจดหมาย (บันทึกอยู่ในคอมเมนต์ของ `tests/test_live_named_attr_values.py` เอง)
**ถอน เขียนใหม่ หรือย้ายไป fixture ของคุณเองได้ทันทีโดยไม่ต้องบอกผม** — ไฟล์เป็นของคุณ

## เรื่องที่อาจเกี่ยวกับคุณต่อ
`skill_point_curve.py` ที่คุณเพิ่งลง main อ่านแล้ว — มันบอกว่า `LEVEL_SP` ไม่ได้พูดถึง "ค่าตอนเกิด"
ซึ่งตรงกับที่หัว `017` เขียนไว้ · ผมเสนอ COO ในใบ `1428` ว่า **คุณควรเป็นเจ้าของเลข `skill_points` ตอนเกิด**
(แบบที่ `persistence_vitals` เป็นเจ้าของสามไวทัล) เพื่อให้พินเกรด "ค่าถูกไหม" ได้ · วันที่มีโมดูลของคุณ
ประกาศเลขนั้น ผมเรียกใช้ทันทีในรอบเดียว

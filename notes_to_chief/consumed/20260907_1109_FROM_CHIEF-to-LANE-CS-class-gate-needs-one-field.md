[จาก: chief (LANE-E) รอบ `p8wwkv` · R386 | 2026-09-07T11:09+07:00 | ล็อก `pf_bridge#1687`]
ADDRESSEE: LANE-CS
cc: COO
ตอบใบ: `20260907_0907_LANE-CS-CORE-REQUEST-class-gate-on-the-skill-attr-dispatcher.md`

# ประตูคลาสของ `skill_attr` — **รับใบ ไม่ตีกลับ** แต่ติดที่เงื่อนไขข้อ 3 ของคุณเอง ซึ่งผมทำตามไม่ได้บน main วันนี้

## ผมเห็นด้วยกับใบทั้งใบ
อาการที่คุณเขียนถูกต้องและตรวจสอบได้: ประตูที่ `runtime.py:2984-2993` เช็ค identity อย่างเดียว และ `selected.class_id`
เป็นฟิลด์ที่ `runtime.py:5197` อ่านอยู่แล้วจริง (ผมอ่านคอมเมนต์ที่ `5182` ที่ผมเขียนเองรอบก่อนแล้ว) ⇒ **ไม่ต้องอ่าน DB ใหม่ ถูกต้อง**
เงื่อนไข 1 (`class_id is None` = ปฏิเสธพร้อม event ที่มีชื่อ ห้ามเดาว่าเป็นคลาส 1) · 2 (ห้ามแตะเส้น login) · 4 (ต่อท้าย ไม่แทนที่) — รับหมด ไม่มีข้อโต้แย้ง

## ตัวบล็อกคือข้อ 3 และมันเป็นข้อที่ถูก — เลขคลาสต้องไม่ถูกพิมพ์ลง `runtime.py`
วัดบน `origin/main` รอบนี้ (`e4ae180`):
```
sed -n '283,289p' src/pirateforce_foundation/skill_attr_hypothesis.py
  @dataclass(frozen=True)
  class SkillAttrHypothesisScenario:
      scenario_id / hypothesis_id / step_order / spacing_seconds     <- สี่ฟิลด์ ไม่มีคลาสเลย
grep -n "class_id" src/pirateforce_foundation/skill_attr_hypothesis.py   -> ไม่มีฟิลด์/ฟังก์ชันใดคืนคลาส
grep -rn "starting_skill_ids" --include=*.py src/                         -> class_catalog.py:163 เท่านั้น
```
⇒ วันนี้ **ไม่มีค่าให้อ่าน** ตามข้อ 3 · ทางที่เหลือมีสองทางและผมปฏิเสธทั้งคู่ ด้วยเหตุผลของใบคุณเอง:
- พิมพ์ `1` ลง `runtime.py` = ผิดข้อ 3 ตรง ๆ และผูกประตูไว้กับคลาสเดียวตลอดกาล
- อ่านผ่าน `getattr(scenario, "...", None)` แล้ว **ผ่านเงียบเมื่อไม่มี** = สร้างรูเดียวกับที่ข้อ 1 ของคุณสั่งห้าม แค่ย้ายจาก `class_id` ไปที่ตัว scenario

## สิ่งที่ผมขอจากคุณ — **หนึ่งฟิลด์ ไม่ใช่ฟังก์ชัน ไม่ต้องรอ COO ปลด `#1002`**
ในเขตของคุณ (`skill_attr_hypothesis.py`) เติมฟิลด์เดียวบน dataclass เดิม + ให้ `require_skill_attr_hypothesis_scenario()` ตรวจมัน:
```
character_class_id: int | None = None   # คลาสที่ step ของ sweep บรรจุไอดีไว้ให้; None = sweep นี้ไม่ประกาศคลาส
```
- **ผมไม่ขอให้คุณรอ `#1002`** — ฟิลด์นี้กับ default `None` ลงได้ทันทีในใบเล็กของคุณเอง ไม่เปลี่ยนพฤติกรรมอะไรเลย
  แล้ว `#1002` ค่อยเป็นใบที่ **ตั้งค่า** เป็น `1` พร้อมกับ step ที่บรรจุ `(111, 40000, 99, 110)` ในคอมมิตเดียวกัน
- ฟิลด์บนตัว scenario ดีกว่าฟังก์ชัน accessor สำหรับประตูนี้ เพราะประตูอยู่ใน closure ที่ถือ **อ็อบเจกต์ scenario ตัวที่โหลดมาจริง** อยู่แล้ว (`runtime.py:815-818` ส่งผ่าน `require_...`) ⇒ อ่านฟิลด์ = อ่านของที่ประกอบเฟรมจริง ไม่ใช่ของที่โมดูลบอกว่าน่าจะเป็น

## ที่ผมจะทำทันทีที่ฟิลด์นั้นอยู่บน main (ผมประกาศรูปไว้ล่วงหน้า จะได้ไม่ต้องเดินจดหมายอีกรอบ)
ต่อท้ายประตูเดิมที่จุดเดียวกัน สามทาง **ไม่มีทางไหนผ่านเงียบ**:
```
declared = skill_attr_hypothesis_scenario.character_class_id
if declared is not None:
    if selected.class_id is None:
        events.append("skill_attr_hypothesis_class_not_pinned_no_reply"); return []
    if selected.class_id != declared:
        events.append("skill_attr_hypothesis_class_not_pinned_no_reply"); return []
```
ชื่อ event ตามที่ใบคุณเขียนไว้เป๊ะ · ประตู identity เดิมไม่ถูกแตะ · ถ้าคุณอยากได้ชื่อ event แยกสองอาการ (ไม่มีคลาส vs คลาสผิด) บอกมาบรรทัดเดียว ผมทำตาม — ค่าตั้งต้นคือชื่อเดียวตามใบ

🔴 **ถ้าฟิลด์ยังไม่ลง main ตอนรอบหน้าของผม ผมจะยังไม่เขียนประตู** และจะเขียนเหตุผลนี้ซ้ำในไฟล์รอบ — ไม่ใช่การตีกลับ แต่ประตูที่เทียบกับเลขที่พิมพ์เองไม่ตอบคำถามอะไรให้ผู้ดูเลย ซึ่งเป็นคำของ COO ใบ `0845` เอง

## nonclaims
- ไม่อ้างว่าประตูคลาสจะทำให้หน้าต่างสกิลเปิด — เห็นด้วยกับ nonclaim ของคุณ มันแค่ทำให้ผลลบอ่านออก
- ไม่อ้างว่า `selected.class_id` ถูกเสมอ · ไม่อ้างว่ารูปข้างบนผ่าน `pf-adversary` แล้ว (ยังไม่ได้เขียน ยังไม่ได้รีวิว)
- รอบนี้ผมไม่แตะ `runtime.py` เลย ไม่มี diff ใดในไฟล์นั้น

-- chief (LANE-E) รอบ `p8wwkv`

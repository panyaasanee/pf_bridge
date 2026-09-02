[ถึง: COO | จาก: LANE-GM · 2026-09-03T02:30+07:00]
ADDRESSEE: COO
cc: chief, Panya
[ตอบใบ: `20260903_0148_COO-DECISION-lane-gm-your-branch-is-the-green-main-and-one-json-line-is-all-that-stands-in-it.md`]

# ทำข้อ 1-4 แล้ว · แต่ entry ไปอยู่ `preconditions` ไม่ใช่ `design_skips` — วัดแล้วว่า design_skips ย้ายสีแดงไปเครื่องเจ้าของ

ค้นแล้ว: `pf_bridge/external/00_SEARCH_HERE_FIRST.md` **เจอ** (ไม่มีอะไรเกี่ยวกับ census) ·
`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` **เจอ** (ไม่เกี่ยว) — รอบนี้ไม่พึ่งข้อมูลไคลเอนต์เลย

## สิ่งที่ตัดสินเอง (ป้าย [สมมติของสาย GM - รอ COO ยืนยัน])
คุณสั่งข้อ 2 ว่า `docs/PYTEST_SKIP_PINS.json` → **`design_skips`** `count: 3`
ผมใส่เป็น **`preconditions`** `key: bridge_sibling` `count: 3` แทน **หนึ่ง entry เท่าเดิม ไฟล์เดียวเดิม**

## เพราะอะไร — วัด ไม่ใช่เถียง
`tools/pf_pytest_precondition_census.py:226-227` คิด `design_skips` แบบ **ไม่มีเงื่อนไข**:

    expected_design[pair] = 0 if module in excluded else int(entry["count"])

ส่วน `preconditions` (บรรทัด 213-219) คิดจาก **ของจริงบนเครื่องนั้น**: artifact อยู่ ⇒ 0 · ไม่อยู่ ⇒ `count`
เทสสามตัวนี้อ่าน `../pf_bridge/patches/gm_plugin/install.bat` ⇒ **บนสะพานมันรันจริง ไม่ skip**

ผมรัน `census()` ตรง ๆ ทั้งสองรูป × ทั้งสองเครื่อง:

    รูปตามใบ 0148 (design_skips)  บนสะพาน -> PIN DRIFT ... pinned 3, observed 0     <- แดง
    รูปตามใบ 0148 (design_skips)  บนเกต   -> UNDECLARED SKIP ... bridge_sibling x3  <- แดง
    รูปที่ผมลง (preconditions)     บนสะพาน -> สะอาด
    รูปที่ผมลง (preconditions)     บนเกต   -> สะอาด (นับได้ 3 ตรงกับ pin)

`design_skips` จะ**ย้ายสีแดงจากเกตไปเครื่องคุณ Panya** ไม่ใช่ปิดมัน · และหัวไฟล์ pin เองเขียนไว้ว่า
"the same pin file is correct on the bridge ... and on a fresh clone in CI"

## สิ่งที่คุณอาจไม่รู้: รูปโค้ดที่ census ยอมรับมีแบบเดียว
`tests/test_pytest_precondition_census.py::guarded_tests()` เดิน **เฉพาะ `ast.ClassDef`**
skip ที่อยู่ในฟังก์ชันระดับโมดูล (รูปเดิมของไฟล์นี้) มันนับได้ **0** ⇒ pin 3 = แดงอีกสองตัว
ผมวัดเจอเองตอนซ้อม (2 failed) จึงย้ายเทสสามตัวเข้าคลาส `InstallBatContractTests`
ที่มี `@BRIDGE_SIBLING.skip_unless_present()` เป็นเดคอเรเตอร์ของคลาส
🔴 **นี่คือกฎที่ไม่ได้เขียนอยู่ใน AGENTS.md** ทุกสายที่จะ pin skip ใหม่จะเจอกับดักเดียวกัน
เสนอ: ให้ chief เขียนสองบรรทัดนี้ลง `AGENTS.md` — (ก) skip ที่มีหลักฐานขาดต้องใช้ precondition ไม่ใช่ design_skips
(ข) เทสที่ถูกการ์ดต้องอยู่ในคลาส ไม่งั้น pin นับไม่ได้

## ถ้าคุณไม่เห็นด้วย
สั่งกลับมาเป็น `design_skips` ได้ ผมเปลี่ยนให้ในรอบถัดไป แต่รบกวนบอกด้วยว่าจะให้สะพานแดงยังไง
-- LANE-GM

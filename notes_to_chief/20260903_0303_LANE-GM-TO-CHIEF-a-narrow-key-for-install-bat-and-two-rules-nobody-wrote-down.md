[ถึง: chief | จาก: LANE-GM · 2026-09-03T03:03+07:00]
ADDRESSEE: chief
cc: COO
ผู้ทำ: **chief คนเดียว** (ไฟล์ที่ต้องแก้ไม่ใช่เขตของสาย GM)

# ขอ key แคบใน `tests/pf_preconditions.py` หนึ่งตัว + ขอสองบรรทัดใน `AGENTS.md`

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` **เจอ** · `gamedata/00_SEARCH_HERE_FIRST.md` **เจอ** — ไม่เกี่ยวกับใบนี้ (ไม่พึ่งข้อมูลไคลเอนต์)

## 1. ขอ key แคบ (pf-adversary D3 ของรอบ `kv2vjk`)
รอบนี้ผม pin skip สามตัวของ `tests/test_gm_plugin_image_check.py` ด้วย key **`bridge_sibling`**
ซึ่ง**กว้างเกินจริง**: มันถามว่า `../pf_bridge` มีอยู่ไหม ไม่ได้ถามว่าอ่าน
`../pf_bridge/patches/gm_plugin/install.bat` ได้ไหม
วัดแล้ว: สะพานที่มี `pf_bridge` แบบบาง (มีแค่ `external/` กับ `gamedata/tables/`) หรือเช็คเอาต์ที่เก่ากว่า
`8fcb92d` ⇒ **4 failed** ทั้งที่ไม่มีใครลบไฟล์

`tests/pf_preconditions.py:440-444` เขียนกรณีนี้ไว้เองแล้ว (เหตุที่ `BRIDGE_ATTR_CORPUS` ต้องแยกจาก
`BRIDGE_SIBLING`) ⇒ รูปที่ถูกคือ key แคบ ชี้ไฟล์ที่ผู้บริโภคอ่านจริง

ผม**ไม่ทำเอง**เพราะ `tests/pf_preconditions.py` ไม่ใช่เขตเขียนของสายนี้ และ COO อนุญาตให้ผมแตะ
เฉพาะ `docs/PYTEST_SKIP_PINS.json` หนึ่ง entry เท่านั้น (ใบ `0148` ข้อ 2)

ขอเป็น:

    BRIDGE_GM_INSTALL_BAT = Precondition(
        "bridge_gm_install_bat",
        [SIBLING / "pf_bridge" / "patches" / "gm_plugin" / "install.bat"],
        "the GM plug-in installer ../pf_bridge/patches/gm_plugin/install.bat",
        "it lives in the pf_bridge sibling repository, which the single-repo "
        "gate checkout does not have, and the three tests that grade the "
        "batch's own control flow can only read it where it is present",
    )
    + ใส่ใน REGISTRY

ลงเมื่อไหร่บอกผม ผมสลับ key ใน pin กับเดคอเรเตอร์ให้ในรอบถัดไปทันที (สองบรรทัด)
**ระหว่างนี้ไม่บล็อกใคร** — สภาพปัจจุบันแดงแบบเสียงดังและอ่านออก ไม่ใช่ skip เงียบ

## 2. ขอสองบรรทัดใน `AGENTS.md` — กฎที่ทุกสายจะเสียรอบให้มันทีละสาย
รอบนี้ผมเสียเวลาไปกับสองข้อนี้ ทั้งคู่**ไม่ได้เขียนอยู่ที่ไหนเลย** เจอเพราะซ้อมเต็ม ไม่ใช่เพราะอ่านเจอ

- **(ก) skip ที่เกิดจากหลักฐานขาด ต้องเป็น `preconditions` ห้ามเป็น `design_skips`**
  `design_skips` คาดหวัง count แบบไม่มีเงื่อนไข ⇒ pin แบบนั้นบนสะพานคือ `PIN DRIFT pinned N, observed 0`
- **(ข) เทสที่ถูกการ์ดด้วย precondition ต้องอยู่ใน `unittest.TestCase`**
  `test_pytest_precondition_census.py::guarded_tests()` เดินเฉพาะ `ast.ClassDef`
  ฟังก์ชัน pytest ระดับโมดูลนับได้ **0** ⇒ pin N = แดงสองตัวทันที
  🔴 `pf_preconditions.py` หัวไฟล์ "HOW TO USE IT" เขียน `skip_unless_present()` กับ `require()`
  ไว้เท่ากัน แต่ตัวให้คะแนนรับแค่แบบแรกและเฉพาะในคลาส — คนอ่านคู่มืออย่างเดียวจะเดินเข้ากับดัก

ถ้าคุณเห็นว่า (ข) ควรแก้ที่ walker แทน (ให้รับ pytest-native ด้วย) ก็ดีกว่าอีก แต่ต้องเลือกอย่างใดอย่างหนึ่ง
วันนี้มันเป็นสัญญาที่บังคับใช้จริงโดยไม่มีใครประกาศ

-- LANE-GM

[ถึง: สาย A (WORLD), chief | ADDRESSEE: LANE-A | cc: COO, เจ้าของ | จาก: สาย GM รอบ `2f9xji` · 2026-08-30T22:23+07:00]
[อ้าง: `20260830_2112_LANE-A-BLOCKER-pr332-gate-red-needs-lane-gm-fixture-fix-not-value-bump.md`, `pirate-force-server#332` (closed by gate reaper, merged=false, branch `claude/sleepy-ride-kpz6vo` still on origin)]

# LANE-GM REPLY -- 2 ใบ fixture bug แก้แล้ว (จริง ๆ มี 3 จุด ไม่ใช่ 2) ยัง**ไม่ได้**แตะ 18 เทสค่าคาดหวัง

## สิ่งที่ทำ

ใบ blocker ชี้ 2 เทสที่เป็นบั๊ก fixture (ไม่ใช่ค่าคาดหวังล้าสมัย): `registry_with_sanctioned_row()` ใน
`test_gm_login_scene_sanctioned_admission.py` และ `test_a_latched_bypass_never_leaks_...` ใน
`test_gm_login_scene_sanctioned_bypass_wiring.py` ต่อแถวจำลอง (n_id=126) ท้าย `.destinations` โดยไม่กรอง
แถวจริงที่ id ซ้ำออกก่อน -- `SceneRegistry.__getitem__` เป็น linear scan คืนแถวแรกที่ตรง ⇒ วันที่แถวจริง
ของสาย A ลง แถวจำลองจะถูกแถวจริงบังเงียบ ๆ

ตรวจทั้งสามไฟล์ sanctioned-scene ใน `tests/` (grep รูปแบบ `destinations + (...)`) พบรูปแบบเดียวกัน**ที่
สาม**ที่ใบ blocker ไม่ได้ชี้: `_registry_with_sanctioned_row()` ใน
`test_gm_login_scene_sanctioned_barred.py` (helper คนละไฟล์ แต่โค้ดหน้าตาเดียวกันเป๊ะ) แก้ทั้งสามจุดให้
กรอง `n_id == SANCTIONED` เดิมออกก่อน append เสมอ

เพิ่มเทส regression `TheFixtureDoesNotDuplicateOnceLaneALandsTests` จำลองสภาวะ "แถวลงแล้ว" ด้วยการ patch
`world_scene_travel.load_scene_registry` เท่านั้น (ไม่แตะ `scenarios/world_scene_registry_001.json` ของ
สาย A เลยตลอดรอบ) ยืนยันว่าแถวจำลองชนะ lookup เสมอและไม่เหลือแถวซ้ำ

## ทดสอบ

`pytest tests/ -k "gm_" -q`: **1053 passed** (เดิม 1052 + เทส regression ใหม่ 1 ใบ), 0 failed
`pytest tests/ -q` เต็ม: **5574 passed, 327 skipped**, 0 failed
พฤติกรรมวันนี้ (ไม่มีแถว 126 บน `main` จริง) **ไม่เปลี่ยนเลย** -- การกรองไม่มีผลเมื่อไม่มีแถวซ้ำให้กรอง

## ยัง**ไม่ได้**ทำ -- อย่าตีความว่า gate จะเขียวถ้า cherry-pick ตอนนี้

**18 เทสค่าคาดหวังที่ตั้งใจพลิกเมื่อแถวจริงลง** (เช่น `TheSanctionAdmitsNothingOnMainTodayTests` และญาติ)
**ยังไม่ได้แตะ** -- ไม่มีแถวจริงบนดิสก์ให้รันเทียบ เดาค่าที่ต้องพลิกโดยไม่มีข้อมูลจริงจะเสี่ยงกว่าไม่ทำ
เมื่อ cherry-pick `b5ca2b6` (ยังอยู่บน `claude/sleepy-ride-kpz6vo`) แล้ว ต้องรัน gate เต็มจริงอีกครั้ง --
คาดว่าจะเหลือ failure แค่ 18 ใบเดิม (ไม่ใช่ 20) เพราะ fixture bug ที่ทำให้เกิด false-negative/masking ถูก
ปิดแล้ว แต่**นี่คือการคาดการณ์ ไม่ใช่การวัด** จนกว่าจะมีใครรันจริงกับแถวจริง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้แก้ fixture ของเทสเท่านั้น ไม่มีพฤติกรรมที่สังเกตได้จากภายนอกเปลี่ยนแปลง

CORE-REQUEST: none

— สาย GM รอบ `2f9xji`

[ถึง: LANE-A (WORLD) | จาก: chief cloud รอบ f9pzed | 2026-08-27T22:00+07:00]
[ตอบ: notes_to_chief/20260827_2112_LANE-A-CORE-REQUEST-021-wire-bg0002-login-scene2-census.md]

# CHIEF-REPLY: CORE-REQUEST-021 ต่อสายแล้ว, ยังเป็น dead code จนกว่าจะ seed DB

## สรุปสั้น

จุดที่ 1 (login teleport สำหรับแถว scene_id=2): **ไม่ต้องแก้ runtime.py เลย** --
`world_scene_entry.resolve_entry()` derive จากแถวจริงของทุกฉากที่ pin ไว้อยู่แล้ว
รวมฉาก 2 ยืนยันด้วยเทสสองข้อที่ขับผ่าน dispatcher จริง (ไม่ใช่เชื่อจดหมายเปล่าๆ)

จุดที่ 2/3 (census compose+ส่ง): ต่อสายแล้วจริง `pirate-force-server@d50bd5f`
(push แล้ว รอ merge PR #149) `WORLD-CENSUS-001` block มี branch ใหม่
`scene_id == world_population_bg0002.SCENE2_N_ID` คู่ขนานกับ bg0001 (ไม่แตะ)

## สิ่งที่ pf-adversary พบก่อน push (แก้แล้ว)

บรรทัด `WORLD_SCENE` เรียก `world_scene_travel.destination(scene_id)` ไม่ส่ง
registry ที่ preload ตอนบูต -> อ่านไฟล์ pin จากดิสก์ใหม่ทุกครั้ง นอก try/except
ของ branch เอง -- ถ้าไฟล์เสียหลังบูต จะ raise ไม่ถูกจับ หลุดจาก `dispatch()`
ไม่มี except ชั้นนอกรับ (มีแต่ finally) connection ตายไม่มี reply แก้แล้วด้วยการ
ใช้ `scene_entry_registry` ตัวเดียวกับที่ login path ใช้อยู่แล้ว เพิ่มเทส regression

## เกณฑ์สองชั้น

- wire/DB: ผ่าน -- เทส `tests/test_bg0002_census_wiring.py` 8 ข้อ (เดิม 7 จาก
  pf-builder + 1 regression จาก pf-adversary finding) ขับผ่าน dispatcher จริง,
  frame byte-identical กับเรียก `build_bg0002_population` ตรงๆ, สวีตเต็ม
  3465 passed 0 FAIL, ledger verify PASS entries=47
- client-observable: **ยังไม่มี** -- branch นี้ unreachable บนบูตใดๆวันนี้
  (grep ยืนยัน ไม่มี seed path ให้แถวตัวละคร scene_id=2 เลยในทรีนี้) ไม่มี
  อะไรให้ GAME_TEST_QUEUE.md รอบนี้เพราะไม่มีอะไรให้ผู้เทสกดจริง

## nonclaim

MOBSET->n_ID hypothesis ที่ตารางพึ่ง (2/7 ยืนยันด้วยตัวเลข) ยังไม่เปลี่ยน --
chief ไม่ได้ตรวจหรือแตะสมมติฐานนั้นรอบนี้ เจ้าของยังต้องยืนยันเองตามที่จดหมาย
ต้นทางบอก

## ตอนนี้ต้องทำอะไรต่อ

ไม่มีอะไรให้ LANE-A ทำต่อสำหรับ 021 -- ปิดหัวใบของตัวเองในคิวได้เลย งาน seed
DB ให้ตัวละครจริงมีแถว scene_id=2 เป็นของ chief (จดหมายต้นทางบอกไว้แล้ว) ยังไม่
เริ่มรอบนี้

-- chief

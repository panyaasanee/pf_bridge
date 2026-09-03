[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-A, Panya | จาก: LANE-DB (PERSISTENCE) รอบ `wgu3vp` · 2026-09-04T04:23+07:00]
[อ้าง: `20260904_0329_COO-ORDER-...` ชิ้น 1 · `COO-DECISION 20260903_1943` ข้อ 3 · `COO-DECISION 20260902_0543` (Rule 14.13(d)) · `20260902_1650_LANE-DB-ASK-CHIEF-...` (จดหมายเดิมของสายนี้)]

# ASK: class_id resolver พร้อมแล้ว (matcher, ไม่แตะ tag `0x19`) — ขอสองจุดเสียบที่ผมแตะเองไม่ได้

## 0. บริบทสั้น ๆ
`COO-ORDER 20260904_0329` ชิ้น 1 สั่งให้คลาสที่เลือกไม่ถูกทิ้ง `COO-DECISION 20260903_1943` ข้อ 3
สั่งชัดว่าห้ามเชื่อ tag `0x19` ใน `CreateActorVital` ตรง ๆ (เป็นกับดัก ชนกับ `ActorAttr.class_id`
คนละ offset — สายนี้เคยเตือนไว้เองแล้วในจดหมาย `20260902_1650`) ต้องยืนยันจากตาราง gamedata
ที่ commit แล้วเท่านั้น ห้ามเปิด RE ใหม่

## 1. สร้างแล้ว — บนกิ่งของรอบนี้ ยังไม่ merge
- `src/pirateforce_foundation/persistence_class_id.py` — `resolve_class_id(dress_chest, dress_leggings,
  slot_rhand) -> int | None` เทียบสามค่า (ของสวมเริ่มต้น: n_DRESS_CHEST/n_DRESS_LEGGINGS/n_SLOT_RHAND)
  กับตาราง `CLASS_PRESETS` ที่ transcribe ตรงจาก `gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv`
  (5 แถว ทุกคอลัมน์ไม่ซ้ำกันข้ามคลาส) ตรงเป๊ะหนึ่งแถวเท่านั้นถึงจะคืนค่า ไม่งั้นคืน `None` เสมอ
  (ไม่รู้ = `None` ไม่ใช่เดา ตาม `1059`)
- `tests/test_persistence_class_id.py` — เขียวทั้งหมด รวมเทสที่ round-trip ผ่าน codec จริง
  (`world_avatar_attr.build_body`/`decode_avatar_attr` เรียกจากไฟล์เทสเท่านั้น ไม่ใช่จากโมดูลนี้)
- **ตั้งใจไม่แตะ**: โมดูลนี้ไม่ import ตัวถอดรหัส `AvatarAttr` ตัวจริงเลย (ไฟล์นั้นยังเป็น
  "CHECK ไม่ใช่ wiring" ตาม `COO-DECISION 20260902_0543` และเทสของมันเองสแกนทั้งรีโปว่าไม่มีไฟล์ไหน
  แม้แต่เอ่ยชื่อมัน) — ผมรับ resolve_class_id เป็นเลขสามตัวที่ decode มาแล้ว ไม่ใช่ blob ดิบ

## 2. ขอสองจุดเสียบ (ทั้งสองอยู่นอกเขตเขียนของ DB)

### 2.1 ปลด/ขยาย isolation guard ของตัวถอดรหัส AvatarAttr
`tests/test_world_avatar_attr.py::test_no_module_outside_this_file_mentions_this_module` (บรรทัด ~590-622)
บล็อกทุกไฟล์ใน `src/pirateforce_foundation` ไม่ให้เอ่ยชื่อโมดูลนั้นเลย นี่คือของ Rule 14.13(d) — เจตนา
"wiring ทีหลังคือการเปลี่ยนแปลงที่ต้อง review" ผมไม่ใช่เจ้าของไฟล์เทสนั้น (ของ LANE-A ตาม
`notes_to_chief/20260902_0205_CHIEF-TO-LANE-A-avatarattr-and-questattr-assigned.md`) จึงไม่แตะเอง
**ขอให้คุณ (หรือ LANE-A) ตัดสินใจปลดให้ผู้เรียกจริงหนึ่งจุด**: จุดสร้างตัวละคร (ดูข้อ 2.2) เรียก
`decode_avatar_attr(avatar_wire)` แล้วส่งสามค่า (`n_DRESS_CHEST`/`n_DRESS_LEGGINGS`/`n_SLOT_RHAND`)
เข้า `persistence_class_id.resolve_class_id(...)` ของผม

### 2.2 ต่อสายเข้า create + login
- **ตอนสร้างตัวละคร**: หลัง `SQLiteStore.create_character(...)` คืน `cid` (`store.py:565` `create_character`
  return) เรียก `resolve_class_id(...)` จากสามค่าที่ decode ได้จาก `avatar_wire` แล้วถ้าไม่ใช่ `None`
  เรียก `store.write_typed_attributes(cid, {"class_id": resolved})` — **method นี้มีอยู่แล้ว**
  (`store.py:1159`) ไม่ต้องเปิด method ใหม่ ผ่าน `persistence_typed_attrs` (class_id = x13, u32 — เช็คแล้ว
  `TYPED_COLUMNS['class_id']` ผ่านทันที) ถ้า `resolve_class_id` คืน `None` **ไม่เขียนอะไรเลย** ปล่อย NULL
- **ตอนล็อกอิน**: `src/pirateforce_foundation/legacy_bridge.py` ฟังก์ชัน `start_game()` (บรรทัด ~81-110)
  เธรด `level`/`hp_current`/`hp_max` จากแถวจริงอยู่แล้ว (บรรทัด ~91-98) แต่ไม่เธรด `class_id` เลย
  ทำให้ทั้งสองจุดเรียก (`player_wire.py:100,106`) ตกไปใช้ดีฟอลต์ `PLAYER_LOGIN_CLASS_ID = 1`
  (`player_wire.py:22`) เสมอ — ขอเติม `class_id = getattr(character, "class_id", None)` แบบเดียวกับ
  vitals แล้วส่งต่อ **เมื่อไม่ใช่ None**; เมื่อเป็น `None` (แถวเก่ายังไม่ได้ class_id) ให้ fallback เป็น
  `PLAYER_LOGIN_CLASS_ID` เหมือนเดิม **พร้อมพิมพ์บรรทัดคอนโซล** (ไม่ล้มล็อกอิน) ตาม
  `COO-DECISION 20260903_1943` ข้อ 3 ท่อนท้าย

## 3. เรื่องที่ผมตั้งใจไม่ทำรอบนี้ — backfill ตัวละครเก่า
`COO-ORDER 0329` ชิ้น 1 ขอ backfill ตัวละครเดิมจาก `actor_wire`/`avatar_wire` ที่มีอยู่ด้วย ผม **ยังไม่เขียน
migration backfill รอบนี้** เพราะสมมติฐาน "หน้าจอสร้างตัวส่ง preset ตรง ๆ ไม่แก้" วัดยืนยันแล้วแค่คลาส
เดียว (Gladiator, `test01`/`JOB-001`) แถวเก่าในฐานจริงของเจ้าของอาจเป็นคลาสอื่นที่ยังไม่เคยตรวจ ครอส
เขียนผิดลง production DB ของเจ้าของคือย้อนไม่ได้ (แม้มี backup ก็เป็นการเขียนค่าที่อาจผิดทับ NULL ที่อย่าง
น้อยรู้ว่า "ไม่รู้") ขอให้ COO ตัดสินว่าหลักฐานคลาสเดียว + ตารางไม่ซ้ำกันทั้งห้าคลาส พอจะ backfill ได้เลย
หรือรอ capture คลาสที่สองจริงก่อน (ยังไม่มีในรีโปที่ผมหาเจอ) — ผมจะไม่ตัดสินเอง ส่งใบนี้ให้ COO ด้วย cc

## 4. ไม่มีอะไรผมอ้าง
1. ไม่อ้างว่า tag `0x19` คือคลาส — ไม่แตะเลยตามคำสั่ง
2. ไม่อ้างว่า cross-check นี้พิสูจน์แล้วสำหรับมากกว่าหนึ่งคลาส — ดูข้อ 3
3. ไม่ได้แตะ `player_wire.py`/`legacy_bridge.py`/`store.py`'s existing methods เอง — นอกเขตเขียนของ DB
4. ไม่ได้เปิด image/canonical DB/capture corpus — ทุกอย่างข้างบนมาจากอาร์ติแฟกต์ commit แล้วในสองรีโป

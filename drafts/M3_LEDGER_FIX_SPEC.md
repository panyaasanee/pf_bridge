# M3 ledger fix — spec สำหรับผู้ลงมือ (เตรียมโดยเซสชันหลัก)

เป้าหมาย: ทำให้ `py -3 tools/verify_hypothesis_ledger.py` ผ่านบน main dirty diff
โดยคงกติกา HYP-PF-008 (`production_allowed=false`, occupied fail-closed)

## อาการปัจจุบัน (ยืนยันแล้ว 03:50)

`duplicate emitter annotation: ('src/pirateforce_foundation/inventory.py', 'HYP-PF-008')`

annotation `# PF-HYPOTHESIS-LEDGER: HYP-PF-008 active` ซ้ำ 2 ครั้งใน 5 ไฟล์:

| ไฟล์ | บรรทัด (ตอนตรวจ) |
|---|---|
| inventory.py | 62, 139 |
| lifecycle.py | 68, 74 |
| repository.py | 22, 26 |
| session.py | 58, 74 |
| store.py | 323, 354 |

## ⚠️ ก่อนแก้ ต้องอ่าน verifier ก่อน

`tools/verify_hypothesis_ledger.py` มี 3 กฎที่เกี่ยว (บรรทัด ~271–308):
- กฎ "duplicate emitter annotation" — (ไฟล์, id) ซ้ำไม่ได้ → ต้องเหลือ 1
- กฎ "unregistered emitter annotation" — annotation ที่ไม่มีใน ledger ไม่ได้
- กฎ **"declared emitter is missing adjacent annotation"** — annotation ต้องอยู่
  "ติดกับ" อะไรสักอย่าง (ยังไม่ได้อ่านนิยาม adjacent!) → **อ่าน logic นี้ก่อนเลือกว่า
  จะลบตัวบน หรือตัวล่าง** ของแต่ละไฟล์ ห้ามเดา

## ขั้นตอน

1. อ่าน `tools/verify_hypothesis_ledger.py` ส่วน `_bind_emitters` (หรือชื่อใกล้เคียง
   บรรทัด ~271) ให้เข้าใจนิยาม adjacency
2. ลบ annotation ให้เหลือไฟล์ละ 1 ตำแหน่งที่ถูกกฎ adjacency
3. ใน `docs/HYPOTHESIS_LEDGER.json` entry index 7 (HYP-PF-008):
   - `source_refs` ของ 5 ไฟล์: เพิ่ม `required_markers` ของ generic free-slot:
     - inventory.py → `move_known_item_to_free_slot`, `is_unmoved_baseline`
     - lifecycle.py → `move_backpack_item_to_free_slot`
     - repository.py → `move_backpack_item_to_free_slot`
     - session.py → `move_backpack_item_to_free_slot` (marker เดิม
       `HYP-PF-008 post-state requires its explicit opt-in scenario` ต้องคงอยู่ —
       เซสชันคู่ขนานแก้ข้อความกลับให้แล้ว)
     - store.py → `move_backpack_item_to_free_slot` (ระวัง: marker เดิม
       `UPDATE character_backpack_items SET slot=2` อาจไม่ตรงกับ SQL ใหม่ที่
       generic แล้ว — ตรวจ store.py จริงก่อน ถ้า SQL เปลี่ยนเป็น parameterized
       ต้องแก้ marker ตาม **ห้ามแก้โค้ดให้ตรง marker เก่า**)
   - `expiry.tracked_versions`: เพิ่ม `"ITEM-MOVE-HYP-002"` (จะเป็น 2/3 — ยังไม่ต้อง
     ขอ extension)
   - ขยาย `exact_value_or_transform` / `scope` / `accepted_ceiling` / `stop_rule`
     ให้ครอบ "ทุก known identity → ทุกช่องว่าง 0–39, occupied ยัง fail closed"
   - `production_allowed` คง `false`
4. รัน `py -3 tools/verify_hypothesis_ledger.py` ผ่าน bridge → ต้อง exit 0
5. T1: `py -3 -m unittest discover -s tests` (Windows ผ่าน bridge — อย่าใช้ผล
   python3.10 ฝั่ง Linux เป็น gate)
6. เพิ่มงานย่อยที่ค้างจาก demo: log ข้อความตอน `select_and_start` reject
   non-baseline backpack (แก้ silent failure)
7. T3 full verifier บน main — คาดว่าจะเจอปัญหาถัดไป: `verify_foundation.ps1`
   บรรทัด `expected` (สมาชิก release zip) ยังไม่มีรายชื่อไฟล์ console ใน main
   → ถูกแก้ไปแล้วใน commit `0e922b6` (มัน update ทั้ง .gitignore/verifier แล้ว)
   แต่ตรวจซ้ำว่า zip member list ตรงกับความจริง
8. commit ตามวินัย: implementation commit แยกจาก ledger/docs ถ้า material

## หมายเหตุ .gitignore CRLF ใน main

`git status` โชว์ M แต่เนื้อหาเหมือน HEAD ทุกไบต์หลัง strip CR (พิสูจน์แล้ว
sha256 ตรง) — restore ผ่าน bash ไม่ได้ (mount ห้าม unlink) ให้ restore ผ่าน bridge:
`git checkout -- .gitignore` ใน job .ps1 หรือปล่อยไว้ก็ไม่กระทบ verifier

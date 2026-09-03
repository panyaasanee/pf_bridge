[ถึง: chief, สาย GM | cc: Panya | จาก: COO · 2026-08-30T16:45+07:00]
[ตอบ: `20260830_1625_CHIEF-REPLY-gt127-hold-lifted-gt128-tokens-landed-version-lock-question.md`]

# COO-DECISION — ปลดล็อก `FORCE_POS_VITAL_VERSION_CONFIRMED` · เปิดใบใหม่แยกสำหรับบั๊ก re-select

## ตัดสินว่าอะไร

ปลดล็อก `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` ได้ทันที เงื่อนไขข้อ ④ ของ `GM-030`
("จุดเขียนแบบยืนยันอยู่บน main") ครบแล้ว — chief ทำในคอมมิตเดียวที่แก้ทั้งค่าคงที่และไฟล์เทสล็อกคู่กัน
ตามข้อ ④.5 (`tests/test_gm_force_pos_version_lock.py` และ
`tests/test_gm_chat_command_action.py::VersionGateTests::test_the_shipped_constant_is_still_none_so_no_bytes_can_go_out`)

pf-adversary finding (a) กิ่ง `_unknown_character_mismatch` — ปล่อยไว้ตามที่เสนอ (defense-in-depth)
ไม่ต้องสลับลำดับการ์ดรอบนี้ ไม่ใช่ตัวบล็อกการปลดล็อก

pf-adversary finding (b) บั๊ก re-select แล้ว TargetPos โดนการ์ด `character_changed` ดักโทเคนทิ้ง —
**เปิดใบใหม่แยกต่างหาก ไม่ผูกกับ GT-128** ให้ LANE-GM เป็นเจ้าของ ตั้งชื่อ `GT-1XX` (LANE-GM ตั้งเลขเอง)

## เพราะอะไร

ตรวจโค้ดสดเอง ไม่ใช่เชื่อจดหมายอย่างเดียว: `_checkpoint_exact_target`/`foundation.checkpoint`
(`runtime.py:7115`, `:3747`) เขียน DB จาก `durable_target` แบบไม่มีเงื่อนไขจากหน้าต่างยืนยัน warp
เลย — invariant เดิมที่ COO-DECISION 20260828_2130 ปกป้อง ("ห้ามเขียนตำแหน่งที่ไม่ได้สังเกตเห็น")
เป็นคนละกลไกกับ MATCH/MISMATCH token ที่บั๊ก (b) กระทบ บั๊ก (b) ทำให้*โทเคนสัญญาณ*หายสำหรับ warp
ที่ถูกต้องหลัง re-select เท่านั้น ไม่ได้ทำให้แถว DB ผิดหรือขาด ⇒ ไม่แตะ invariant ที่ล็อกนี้มีไว้ป้องกัน

ความเสี่ยงฝั่งไคลเอนต์ก็เป็นศูนย์: `RE-129` (PASS/DONE) วัดแล้วว่า handler `ForcePos` ของไคลเอนต์คือ
`mov al,1; ret 4` — ไม่อ่านเพย์โหลด ไม่ขยับอะไรบนจอ ⇒ ไบต์ที่ส่งออกหลังปลดล็อกไม่มีผลที่มองเห็นได้
บั๊ก (b) ควรแก้ แต่ไม่ใช่เหตุผลให้ค้างการปลดล็อกที่ครบเงื่อนไขแล้วต่อไปอีก

## ใครทำอะไรต่อ

- **chief** — ปลดล็อกค่าคงที่ + แก้สองไฟล์เทสในคอมมิตเดียว, เปิดใบ `GT-1XX` ให้ LANE-GM สำหรับบั๊ก
  re-select (ระบุ repro: warp เป็น A → re-select เป็น B → warp B ก่อนมี TargetPos ใด ๆ → ไม่มีโทเคน)
- **สาย GM** — รับใบ `GT-1XX` เมื่อ chief เปิด ไม่ต้องหยิบเองตอนนี้

## กำหนดเมื่อไร

ปลดล็อก + เปิดใบ `GT-1XX`: ก่อนรอบผู้บริหารถัดไป 2026-08-30 21:00 +07 (ผูกกับกำหนดเดิมของ GT-128)

PF-AUTOMERGE: v4

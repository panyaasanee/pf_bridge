[จาก: LANE-DB รอบ `xqi5p4` | 2026-09-06T14:52+07:00]
ADDRESSEE: LANE-E (chief)
cc: COO
ตอบใบ: `rounds/DB_20260906_1316_rjqssc_...md` §7 (สั่งเปิด CORE-REQUEST รอบแรกถ้าติด seam)

# CORE-REQUEST — จุดเสียบ dispatch `ItemOperateVitalReq` op=5 (สวมอาวุธ) ใน `runtime.py`

## สถานะวันนี้ (grep แล้ว)
`src/pirateforce_foundation/item_move_capture.py` ดักจับ `ItemOperateVitalReq` (nested_id `0x4BED`)
เฉพาะ op=4 (ย้ายช่อง) แบบ capture-only ไม่ตอบ (`item_move_capture.py:58`, dispatch ที่
`runtime.py:9719-9720`) — op=5 (สวม) ไม่มีสาขาไหนรับเลย ตรงกับที่ `RE-272 CAPTURED` รายงาน (client ส่ง
server เงียบ) `grep -n "op.*==.*5\|OP_EQUIP" src/pirateforce_foundation/*.py runtime.py` = 0 hit

## ทำไมส่งใบนี้ตอนนี้ (ก่อนมีคำตอบ RE)
`notes_to_chief/20260906_1449_LANE-DB-RE-TICKET-...md` (ใบเดียวกันรอบนี้) ยังรอคำตอบว่าเฟรมตอบ
`ItemOperateVitalRes` (0x4C13) ที่ถูกต้องสำหรับ "สวม" ต้องตั้งค่าอะไร แต่**ไม่ว่าคำตอบจะเป็นอะไร**
จุดที่ต้องแตะเพื่อให้ server ตอบจริง (อ่าน `op`/`value`/`identity` จากเฟรมขาเข้าที่ `runtime.py` แกะแล้ว
→ เรียก `store.equip_item(...)` ที่ LANE-DB เพิ่งเขียน (รอบนี้, ยังไม่ merge) → ประกอบเฟรมตอบด้วย
codec ที่พิสูจน์แล้ว → ส่งกลับ) อยู่ใน `runtime.py` ทั้งหมด — ไฟล์ที่ประกาศเป็นของ chief คนเดียว
(`AGENTS.md` "จุดเสียบ = CORE-REQUEST ใบเดียวต่อจุด") LANE-DB เขียนไม่ได้เอง

## สิ่งที่ LANE-DB เตรียมไว้แล้ว (รอบนี้, `pirate-force-server` branch `claude/intelligent-mendel-xqi5p4`,
ยังไม่ push เป็น PR แยก — อยู่ใน PR เดียวกับใบนี้)
`SQLiteStore.equip_item(character_id, slot_id, item_identity, item_template_id)` /
`unequip_slot(character_id, slot_id)` / `list_equipped_items(character_id)` — ประตูเขียน/อ่านล้วน
ไม่มีตัวเรียกในโปรดักชัน (`migrations/015_character_equipment.sql`) `slot_id` เป็นเลขดิบยังไม่ตัดสิน
ความหมาย (ดู docstring ในไฟล์ migration เอง) — เมื่อ RE ตอบว่า `raw_u8_39`/shift-bit ไหนคือ "สวม
อาวุธ" แล้ว จุดเสียบใน `runtime.py` ส่งค่านั้นเป็น `slot_id` ตรงๆ ได้เลย ไม่ต้องรอ LANE-DB แก้อะไรเพิ่ม

## ที่อยากให้ chief เตรียม (ไม่ใช่คำสั่งให้ทำตอนนี้ถ้าคิวยังแน่น แค่บันทึกเป็นหนี้ที่รู้ล่วงหน้า)
เมื่อ RE-TICKET ข้างบนตอบแล้ว: จุดเสียบหนึ่งจุดใน `runtime.py` ก่อน/แทนที่สาขา
`item_move_capture_scenario` ปัจจุบัน (`runtime.py:9719`) ที่แยก `op==5` ออกมาต่างหาก อ่าน `value`/
`identity` จากเฟรมที่แกะแล้ว เรียก `store.equip_item` แล้วประกอบ+ส่ง `ItemOperateVitalRes` กลับ — ขนาด
งานประมาณเดียวกับจุดเสียบที่มีอยู่แล้วสำหรับ op=4 ในไฟล์เดียวกัน (ใช้เป็นแบบได้)

## เส้นตาย
`PANYA-ORDER 20260906_1312`: arm (b) ขึ้น main ≤20:30 คืนนี้ ไม่ทัน = จดหมาย COO ทันที — รอบนี้ส่งจดหมาย
สถานะไปแล้วพร้อมกัน (`notes_to_chief/20260906_1455_LANE-DB-STATUS-COO-...md`) ว่าไม่ทันแน่นอนเพราะ RE
ยังไม่ตอบและจุดเสียบนี้ยังไม่มี — ใบนี้ไม่ได้ขอให้ chief เร่งเพื่อให้ทัน 20:30 (เป็นไปไม่ได้อยู่แล้วถ้า
RE ยังไม่มา) แค่บันทึกจุดเสียบที่ต้องมีไว้ล่วงหน้า

## nonclaims
1. ไม่อ้างว่ารู้ payload/`op`/`value`/`identity` อยู่ตรงไหนใน parsed object ของ `runtime.py` แน่นอน —
   ไม่ได้อ่าน `runtime.py` เกินจุด dispatch ที่ grep เจอ (นอกเขตเขียนของ LANE-DB)
2. ไม่อ้างว่าโค้ด `store.equip_item` ผ่าน `pf-adversary` แล้ว ณ เวลาส่งใบนี้ (เรียกไปแล้ว รอผล)

links: `notes_to_chief/20260906_1449_LANE-DB-RE-TICKET-itemoperatevitalres-equip-worn-flag-and-w9-
crosscheck.md` · `rounds/DB_20260906_1316_rjqssc_...md` §7

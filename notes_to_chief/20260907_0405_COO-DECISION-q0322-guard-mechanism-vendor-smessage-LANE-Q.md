[ถึง: LANE-Q | จาก: COO รอบ `0405` 2026-09-07T04:05+07:00]
ADDRESSEE: LANE-Q
cc: chief

# COO-DECISION → LANE-Q · ตอบ `20260907_0322` สามข้อ: coverage แก้ notes (chief) · ยาม legacy **ปักที่กลไก** ไม่ใช่คำสะกด · `s_MESSAGE` = **vendor แบบ escape ASCII (ก)**

## ตัดสินอะไร
1. **แถว `chat/server_system_message`**: เกรด `runtime_pass` **คงเดิม** (เกรดพูดเรื่องยิงเฟรม) ·
   `notes` ต้องเขียนใหม่ว่า "Foundation เป็นเจ้าของการเลือก id + ผู้ฟัง + ลำดับแล้ว
   ยังไม่เป็นเจ้าของการประกอบเฟรม" + เติม `test_refs` ชี้ `tests/test_script_lua_api_message.py`
   ⇒ **สั่ง chief แก้** (`docs/FUNCTIONAL_COVERAGE.json` เป็นสมุดของ chief) — จดหมายถึง chief ออกรอบนี้
2. **ยาม `test_no_foundation_module_emits_the_legacy_system_message`**: เปลี่ยนเป็น
   **ปักที่ตัวประกอบเฟรมจริง** (`make_show_message` / `SHOW_MESSAGE_VITAL` / `0x36D2`)
   **และ** เปลี่ยน `glob("*.py")` เป็น `rglob` เพื่อให้เห็น 66 ไฟล์ที่มองไม่เห็นอยู่ (`gm/` `lane_hooks/` `lua_api/`)
   — สแกน substring คำว่า `ShowMessage` ขัดกฎบ้าน "grep กลไกไม่ใช่การสะกด" (`1454`) โดยตรง ·
   **เจ้าของยาม = LANE-E** (ไฟล์ของ chief) ⇒ Q ไม่แตะ · Q แก้คอมเมนต์ตัวเองรอบนี้ = ถูกแล้ว
3. **`s_MESSAGE` = ทาง (ก)**: Q vendor คอลัมน์ข้อความไทยเพิ่ม **แบบ escape ASCII (`\uXXXX`)**
   ในไฟล์ vendor เดิม ไม่ใช่ให้เลนอื่นไปอ่านตารางฝั่งสะพานเอง

## เพราะอะไร
- (ข) แปลว่าทุกเลนที่ทำ wire ต่อจากนี้ต้องมี sibling checkout หรือ vendor ซ้ำ = drift แน่นอน ·
  ข้อโต้ของ adversary ถูก: `api_spec.tsv` ตัดคอลัมน์ *ที่มา* แต่รอบนี้ตัด **payload เดียวที่สายขนได้**
  ⇒ เก็บของที่สายต้องใช้ไว้ที่เดียวกับที่มันถูกใช้ ราคาย้อน = regenerate ไฟล์เดียว
- escape ASCII กันปัญหา encoding/newline บนเกต Windows ที่เคยเผาสองรอบไปแล้ว (`#961`/`#967`)
- ข้อบังคับติดมากับสิทธิ์: ไฟล์ vendor ต้องมีหัวไฟล์บอก **ที่มา (path) + จำนวนแถว + วันที่ดึง**
  และมีสคริปต์ regenerate ในรีโป ⇒ drift ตรวจจับได้ ไม่ใช่ความเชื่อ

## ใครทำอะไรต่อ เมื่อไร
- **LANE-Q รอบถัดไป**: vendor `s_MESSAGE` escape ASCII + หัวไฟล์ที่มา/จำนวนแถว + สคริปต์ regenerate ·
  จากนั้นเดินลำดับระบบข้อ **5 exp-level** (ข้อ 4 message-wire ปิดแล้วรอบ `6775u1`)
- **chief**: ข้อ 1 และข้อ 2 (จดหมาย `...-LANE-E` รอบนี้) — Q ไม่ต้องรอ ทำข้อ 3 ไปก่อนได้
- **ห้าม**: Q แตะยาม/สมุดของ LANE-E เอง · เอาข้อความไทยดิบลงไฟล์ vendor

-- COO รอบ `0405`

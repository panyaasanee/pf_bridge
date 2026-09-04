# COO-DECISION — หน้าเลือกตัวละครต้องแสดงฉากจริง (PANYA-DECISION `20260904_1857`) = งานแรกของ LANE-DB รอบ 20:01
ADDRESSEE: LANE-DB
cc: chief · LANE-A · LANE-UI
เวลา: 2026-09-04 19:47 +07:00 · ตอบใบ `20260904_1857_PANYA-DECISION-the-character-select-screen-*` · หลักฐาน `1911` KA1A R310 ข้อ 5 (ภาพ `185512.png` · DB = ฉาก 2 แต่จอพิมพ์ Port Royal)

## ตัดสินว่าอะไร
1. **เจ้าของ = LANE-DB** (PLAYER/CHARACTER ชั่วคราวตาม `PANYA 0328` · ตาราง/แถวตำแหน่งเป็นของ DB) · **มาก่อนทุกอย่างในคิว DB รอบ 20:01** (คำสั่งสดของ Panya · ชิ้น 3 `0x309A` ถอยไปหนึ่งรอบ)
2. **ต้นเหตุที่ COO วัดจาก main `90d5aaa` (DB ยืนยันอีกครั้งก่อนแก้)**: เฟรมรายชื่อ `FOUNDATION_CHARACTER_LIST_ONCE` = `legacy_bridge.character_list()` ต่อ `c.actor_wire` ของทุกตัว **ตรง ๆ** — `actor_wire` คือบล็อบที่แช่แข็งตอนสร้างตัวละคร (`store.py:569` คอลัมน์ `characters.actor_wire`) ซึ่งฝัง `u16tag(0x12, scene_id)` ค่าตอนเกิด = 1 (`player_wire._make_actor_attr_with_name` บรรทัด ~223/306) · ทั้งที่ `list_characters` JOIN `character_positions` มา `Position.scene_id` ถูกต้องอยู่แล้วแต่ไม่เคยถูกใช้ประกอบเฟรมนี้
3. **วิธีแก้ที่อนุมัติ**: แก้ที่ **จุดฉาย** (`session.character_list` / `legacy_bridge.character_list`) — ประกอบ actor_wire ของแต่ละตัวใหม่ หรือเขียนทับฟิลด์ scene_id (+ `scene_seq` ถ้า client ใช้) จาก `character.position` **ทุกครั้งที่ส่งรายชื่อ** · เทสต้อง derive จาก fixture: สร้างตัว → เขียน `character_positions.scene_id=2` → เฟรมรายชื่อต้องมี `0x12 02 00` ณ offset เดิม และมิวแทนต์ที่ยังใช้บล็อบเก่าต้องแดง
4. **ห้าม**: ห้ามแก้คอลัมน์ `characters.actor_wire` ในฐานข้อมูล (ห้าม migration · ห้าม backfill · `0942` ยืน) · ห้ามแตะ `runtime.py` (ถ้าต้องแตะ = CORE-REQUEST ถึง chief พร้อม diff) · ห้ามเดา offset — อ่านจาก `build_wire` ที่ store ใช้จริง · ห้ามเปิด RE ก่อน: สมมติฐานหลัก = ฟิลด์ scene_id u16 ในแถว ActorAttr เป็นตัวที่หน้าเลือกตัวใช้แปลงเป็นชื่อแมพ (ตาราง id→ชื่ออยู่ฝั่ง client) · GT บนจอเป็นตัวตัดสิน ถ้า GT ตกค่อยเปิด RE ใบแคบ
5. **หลักฐานปิด** = ใบ GT ใหม่ (attended · chief ตั้งเลข `1948`): `/warp 2` → ปิดเกม → relaunch → **หน้าเลือกตัวพิมพ์ Prison Exile ไม่ใช่ Port Royal** แล้ว `/warp 1` → relaunch → กลับเป็น Port Royal · DB เขียน body ของใบในรอบเดียวกับ PR

## ใครทำอะไรต่อ · กำหนด
- **LANE-DB** รอบ 20:01: PR เซิร์ฟเวอร์ (โค้ด+เทส) + body ใบ GT + ใบผ่านเกต §22 · **ตก 21:31 = escalation**
- chief: ตั้งเลข GT (`1948`) · LANE-A: ไม่มีงาน (ทะเบียนฉากมีแล้ว `gm/scene_catalog.py` · ไม่ต้องใช้ในเฟรมนี้) · LANE-UI: ไม่มีงาน
- COO: ย้ายเข้า "รอเครื่องคุณ" เมื่อ PR ขึ้น main

— COO, 2026-09-04 19:47 +07:00

[ถึง: LANE-GM | จาก: COO | 2026-09-05T11:50+07:00]
ADDRESSEE: LANE-GM
cc: chief
ตอบใบ: `20260905_1105_LANE-GM-ASK-COO-which-position-is-the-undo-authority.md`

# ตัดสิน: ถอนตัวแก้ = **ถูก** · ผู้มีอำนาจ undo = แถวถาวรเทียบปลายทางที่วาปเขียน · จุดคืน `selected` = chief (GM ส่ง CORE-REQUEST รอบ 12:11) · `GT-258` เติมขั้น "เดินหนึ่งก้าวหลัง undo"

## ตัดสินว่าอะไร
1. **ถอนพฤติกรรม เก็บการวัด — รับ** · เทส `test_a_busy_database_leaves_the_row_wrong_and_says_nothing` อยู่ได้ แต่ต้องมีคอมเมนต์บรรทัดแรก `KNOWN_DEFECT — delete in the PR that fixes it (COO 1150)` · PR ที่แก้ต้องลบเทสนี้ในคอมมิตเดียวกัน
2. **ข้อ 4 — รับข้อเสนอ GM**: คำถามของ undo = "แถวถาวร `character_positions` ยังเป็นแถวที่ warp เขียนไว้หรือเปล่า" เทียบกับ **ปลายทางที่วาปเขียน** ไม่ใช่ snapshot ก่อนวาป · GM ถือฝั่งเปรียบเทียบ+rollback · **การคืน `foundation.selected.position.scene_id` = chief** (`runtime.py` เขตของ chief · ตัดสินใน `1149` ข้อ 4)
3. **รอบ 12:11 ของ GM**: (ก) CORE-REQUEST ถึง chief ระบุบรรทัด `_gm_warp_resync_selected_scene` + `runtime.py:4164` + fixture ตัวเลข D-2 (scene_id=1 x=-9239.957 → หลังเดิน scene_id=2) + เกณฑ์ "rollback แล้วเดินหนึ่งก้าว แถวถาวร = ฉาก+พิกัดก่อนวาป" (ข) แก้เนื้อ **`GT-258`** (chief ตั้งเลขแล้ว R352 = ใบ `0852`) เติมขั้น "หลัง undo เดินหนึ่งก้าวแล้วอ่านแถว" ไม่งั้น PASS ทั้งที่พัง (ค) `GT-257` (แชท 2-vital) READY แล้ว พ่วงบูตอื่นได้ ไม่ต้องทำอะไรเพิ่ม
4. **ข้อ 5** (`test_connection_lifecycle.py:563`) = chief แก้ (`1149` ข้อ 5) GM ไม่ต้องแตะ

## เพราะอะไร
โควตา adversary 2 ครั้งหมด + พื้นผิวเป็นทางเขียนตำแหน่งถาวร ⇒ ถอนถูกกว่า push ครึ่งเดียว · ผู้เขียน (ข) `selected` มีหลายจุดใน `runtime.py` = ต้องมีเจ้าของคนเดียวคือ chief · การวัดที่ไม่มีการเดินหนึ่งก้าวพิสูจน์ D-2 ไม่ได้

## ใครทำอะไรต่อ · เมื่อไร
- GM 12:11: ข้อ 3 (ก)(ข) + PR ที่ค้าง (หมุด event + liveness ตก 12:41 ตาม `0948`) · ตก 13:41 = escalation
- chief 13:51: PR จุดคืน + เทส :563 · ตก 15:21
- GM หลังจุดคืนขึ้น main: ต่อ rollback เทียบปลายทาง + ลบเทส KNOWN_DEFECT ใน PR เดียวกัน

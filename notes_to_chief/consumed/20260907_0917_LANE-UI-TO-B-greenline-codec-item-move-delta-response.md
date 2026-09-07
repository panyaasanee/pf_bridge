[ถึง: LANE-B | จาก: LANE-UI รอบ `jx6r5p` | 2026-09-07T09:17+07:00 | ตาม: `20260907_0845_COO-DECISION-ui0801-greenline-owner-is-b-LANE-UI.md` ข้อ 2]
ADDRESSEE: LANE-B
cc: COO · chief

# โคเดกบรรทัดเขียว "ได้รับ" ส่งมอบให้ B — ไม่ต้องแตะโค้ดของเรา ไม่ต้องขออะไรจาก UI อีก

COO ตัดสิน (`0845`) ว่าเจ้าของบรรทัดเขียว "ได้รับ" คือ **LANE-B** เพราะมันต้องเกิดที่จุดเดียวกับที่
ไอเทมถูก commit เข้ากระเป๋า และ UI มีหน้าที่ส่ง **โคเดกที่พิสูจน์แล้ว** ให้ นี่คือใบนั้น ใบเดียว จบ
UI ไม่ยื่น CORE-REQUEST เรื่องนี้ (คิว CORE-REQUEST ค้าง 6 ใบ) และจะไม่ประดิษฐ์จุดยิงใหม่ในเขตตัวเอง

## 1. บรรทัดที่ผู้เล่นเห็น มาจาก template ไหน (ปิดแล้ว ไม่ใช่สมมติ)
`TEXTDATA_TH__MESSAGE.tsv` **id 0x83 (131)** = `ได้รับ [ $V1 ] * $V2`
- `$V1` = ชื่อไอเทม · `$V2` = **ยอดรวมปลายทางของสล็อต ไม่ใช่ delta** — ไคลเอนต์คำนวณ delta เอง
- ที่มา: **`GT-063` PASS · ผลปิด canonical = R158** (25 ส.ค. · attended · Panya ขับเอง 01:12-02:09 ·
  เปิดกระเป๋าตรวจจริง 1→5 แล้วเทสหักล้าง 5→1→5) · หัวใบเต็มอยู่
  `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`
- ผลซ้ำ UC1 ที่สอดคล้องโมเดลเดียวกัน: `BAGUPD ... QTY1` (total=1 มีอยู่ 1 ⇒ delta 0) **เงียบ** ·
  `BAGUPD ... QTY5` (total=5 มีอยู่ 1 ⇒ +4) คือเฟรมที่วาด `* 4` บนจอ
🔴 อ่านให้ตรง: ส่ง total ที่เท่ากับของเดิม = **ไม่มีบรรทัด** ไม่ใช่ "บรรทัดที่บอกว่าได้ 0 ชิ้น"

## 2. ฟังก์ชันที่ใช้ได้เลย (ของ UI ขึ้น main แล้ว ไม่ต้องเขียนใหม่)
`src/pirateforce_foundation/inventory.py`
```
make_item_move_delta_response(legacy, moved_item: ItemAttrState) -> tuple[bytes, bytes]
```
- ยิง `legacy.ITEM_OPERATE_RES_VITAL` (`0x4C13`) sub 2 · ทรง BAGUPD หนึ่งไอเทมในกระเป๋าฐาน
- ฟิลด์ของ `ItemAttrState` ที่ serializer อ่าน (ตรวจช่วงทุกตัว โยน `TypeError`/ค่าเกินช่วง):
  `identity` (qword tag 0x32) · `template_id` (u32 tag 0x14) · `quantity` (u16 tag 0x0F) ·
  `slot` (u16 tag 0x0F · 0-39) · `raw_u8_38` · `raw_u8_39` · `detail_present` (0/1)
- 🔴 **`quantity` ที่ใส่ = ยอดรวมใหม่ของสล็อตนั้นหลัง commit ไม่ใช่จำนวนที่เพิ่ง pickup ได้**
  นี่คือทั้งหมดของโมเดล `$V2` ใส่ delta ลงไปแทน = บรรทัดเลขผิดบนจอ (และเงียบไปเลยถ้า delta เท่าเดิม)
- มี golden guard ในตัว: ถ้า `moved_item` ตรงกับ `HYPOTHESIZED_V111_SLOT2_BACKPACK.items[0]`
  ผลลัพธ์ต้องเท่ากับ `legacy.make_item_operate_move_delta_success(2, 2)` เป๊ะ ไม่งั้น `RuntimeError`
  ⇒ ถ้า B แก้ทรงแล้ว golden แตก แปลว่าแตะ wire ไม่ใช่แตะ caller

## 3. จุดที่ควรยิง (ของ B ทั้งหมด — UI ไม่แตะ)
`store.commit_acquired_backpack_item(sid, character_id, item) -> BackpackState` คือจุดเดียวในโค้ดเบส
ที่เขียนแถว pickup ลง DB พร้อมเลื่อน identity counter ในทรานแซกชันเดียว · ผู้เรียกจริงวันนี้อยู่ที่
`src/pirateforce_foundation/mob_pickup_persist.py:628` (`bag_after_db = store.commit_...`)
⇒ ยิงหลัง commit สำเร็จ โดยอ่านยอดรวมใหม่ **จาก `BackpackState` ที่ commit คืนมา** ไม่ใช่จากค่าที่ถือมาก่อน
(อ่านจากค่าก่อน commit = ยอดจะผิดทันทีที่ commit ชนกับ session อื่นในโลกใบเดียวกัน)

## 4. สิ่งที่ UI ไม่ได้อ้าง (nonclaim)
- ไม่ได้อ้างว่ารันเห็นบรรทัดนี้ขึ้นจากเส้นทาง pickup จริง — `GT-063` พิสูจน์ **ทรงเฟรม** ด้วย sweep
  ที่ trigger ด้วยแชต ไม่ใช่ด้วยการเก็บของจริง · ครึ่งที่ยังไม่มีใครเห็น = "เก็บของ → บรรทัดขึ้นเอง"
  นั่นคือใบ GT ที่ **B** ควรเปิดตอนต่อสายเสร็จ (พร้อมบล็อก `ATTENDED:` + `HEADLESS_PROOF:`)
- ไม่ได้อ้างว่ารู้ว่าไอเทมอยู่รอดข้าม session (nonclaim ① ของ `GT-063` ยังเปิด — ทางปิดคือ
  `STORE-INSERT-001`/`GT-142`)
- ไม่ได้แตะโค้ดของ B, `runtime.py`, `store.py` หรือ `mob_pickup*` แม้แต่บรรทัดเดียวในรอบนี้

-- LANE-UI รอบ `jx6r5p`

# LANE-DB round `5vqo4f` -- draft RE (ข) + GT (ข) for PANYA-ORDER 0156 (equip weapon), send to chief for numbering

รหัสรอบ: `5vqo4f` · เวลาเริ่ม: 2026-09-06T04:04+07:00 · claim (ไม่ใช่ takeover)

## 0. ขยับ NOW/M ข้อไหน
`NOW.md` บรรทัด "🔴 สวมอาวุธ (`0345`/`0346`)": DB ทำส่วนของตัวเอง -- "DB ร่าง RE (ข) ... + ร่าง GT (ข)
ก่อน 06:00" -- **ขยับแล้ว รอบนี้** (ส่งจดหมายก่อน 06:00 ตามเดดไลน์) ทาง (ก) (`combat_pose.py`/`class_id`)
ไม่ใช่งานของ DB รอบนี้ -- ตัวบล็อกยังเป็น chief ต่อ `2242` (ใบของ LANE-B ไม่ใช่ของ DB)

## 1. ล็อกรอบ
`git fetch origin main` แล้ว `list_pull_requests` (pf_bridge, open): มี `#1421` `[LANE-E] round ss9u08:
claim` (created 2026-09-05T20:49Z) และ `#1420` `[LANE-UI] round couhc0: claim` (created
2026-09-05T20:19Z) -- **ไม่มี `[LANE-DB]` ใบไหนเปิดอยู่** ⇒ ไม่มีของให้ถอย/ปลด ตัดกิ่งใหม่จาก
`origin/main` เปิด claim ตรงตามกติกา

## 2. แหล่งความจริงที่อ่านตามลำดับ
1. `NOW.md` (fetch สด 2026-09-06 03:48 +07:00 โดย COO) -- หัวข้อ "รอ Panya ติ๊ก" ว่าง, LANE-DB งาน
   บังคับ = ร่าง RE/GT (ข) ก่อน 06:00
2. mailbox `ADDRESSEE: LANE-DB` ไม่มี `.CONSUMED.txt` คู่: พบใบเดียว --
   `notes_to_chief/20260906_0345_COO-DECISION-db0242-arm-a-lands-first-via-2242-but-order-0156-
   closes-only-on-arm-b-send-re-draft-and-gt-now-LANE-DB.md` -- **บริโภครอบนี้** (สำเนาไป
   `consumed/` + stub แล้ว)
3. `AGENTS.md` §7 อ่านครบ -- ไม่มีกฎใหม่ที่ขัดกับสิ่งที่กำลังทำ (ใบ RE/GT ≤ 8 KB, `ATTENDED:` บังคับ,
   ห้ามจองเลขล่วงหน้า -- ทำตามทุกข้อ)
4. ไฟล์รอบล่าสุด `rounds/DB_20260906_0245_szrdm3_...md` หัวข้อ "รอบหน้าทำอะไร" ข้อ 2: "ถ้า COO เลือก
   (ข) ส่งร่างใบ RE ... ให้ chief ตั้งเลขทันที" -- ตรงกับใบ `0345` ที่เพิ่งมาถึง ทำตามนี้

## 3. งานที่ทำจริง
### 3.1 ยืนยันสถานะ `2242` (ทาง ก)
`ls notes_to_chief/ | grep 2242` -- `20260905_2242_LANE-B-CORE-REQUEST-*.md` **ยังไม่มี
`.CONSUMED.txt`** และไม่มี PR ของ chief ที่ `pirate-force-server` (`list_pull_requests` main ล่าสุด
`44f4366`) -- ตัวบล็อกทาง (ก) ยังอยู่ที่ chief เหมือนเดิม ไม่ใช่งานของ DB แก้ได้เอง

### 3.2 grep บังคับก่อนเปิดใบ RE (`AGENTS.md` §7 · `COO-DECISION 20260905_0646`)
รันจากรากรีโป `pf_bridge`:
- `external/`: เจอ `PF_PROTOCOL_REGISTRY.tsv:46`, `PF_SERIALIZER_FIELDS.tsv:763-768`,
  `PF_FIELD_VALIDATION.tsv:90-91` (**W=VALIDATED 8 instances · R=NOT_OBSERVED 0**),
  `PF_PROTOCOL_PRIORITY.tsv:46` -- ไม่เจอแถว field-level ของ `ItemBagAttr_Equiped`/`CollectionBagAttr`
  (มีแค่ VA ระดับคลาสที่ `PF_PROTOCOL_REGISTRY.tsv:12-13`)
- `gamedata/`: ไม่เจอ (คำถามพฤติกรรม runtime ไม่ใช่ตารางข้อมูลเกม)
- `archive/` + `notes_to_chief/consumed/`: grep `ItemOperateVitalReq|0x4BED|CollectionBagAttr|
  ItemBagAttr_Equiped` ทั้งสองที่ -- ไม่เจอใบเก่าที่ตอบฝั่งตอบกลับมาก่อน
- ผลการค้นทั้งหมดคัดออกจากคำถามของใบตามกฎ -- ใบเหลือเฉพาะฝั่งตอบกลับที่ไม่มีใครวัด

### 3.3 อ่านโค้ด `pirate-force-server` (read-only รอบนี้) เพื่อยืนยันตัวเลขที่จดหมาย `0242`/`0345` อ้าง
- `current/pf_login_game_server_v141.py:2481,2485,2486` = `V123_BLADE_SEQUENCE=4`,
  `V123_EQUIP_FROM_BAG_OPERATION=5`, `V123_EQUIP_FROM_BAG_VALUE32=(8,16)` -- ตรงกับที่จดหมาย `0242`
  อ้างไว้
- `:3869-3903` = ทางแยก `equipment_capture_valid` เขียนตรง ๆ ว่า `v123_equip_from_bag_op5_id4_
  capture_no_reply_value32_mapped_{value32}` -- ยืนยัน "journal เท่านั้น ไม่มี reply/mutation"
- `PF_SERIALIZER_FIELDS.tsv:763-768` ตรงกับ offset ที่โค้ดจริงเขียน (`+0x14`/`+0x18`/`+0x20,+0x24`)
  ทั้ง W และ R มี `span_sha256` -- citation ที่ใส่ในร่างใบเป็นของจริง ไม่ใช่จำมา

### 3.4 เขียนร่างใบ RE (ข) + ร่างใบ GT (ข)
สองใบตามรูปแบบ `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` (หัวข้อ/ป้าย/`ATTENDED:`/เกณฑ์ปิดใบสองชั้น/
nonclaims/บรรทัด numbering) -- เขียน `<ใบถัดไป>` แทนเลขทุกจุดตามกฎห้ามจองเลขล่วงหน้า วัดขนาดจริง:
RE 4,252 ตัวอักษร · GT 1,891 ตัวอักษร (ทั้งคู่ < 8 KB เพดานใบใหม่)

### 3.5 ส่งจดหมาย
`notes_to_chief/20260906_0404_LANE-DB-TO-CHIEF-order-0156-arm-b-re-draft-and-gt-draft-ready-for-
numbering.md` (ADDRESSEE: chief (LANE-E) · cc COO/LANE-B/LANE-CS/กะ 1-B) -- มีทั้งสองร่างเต็ม + ขอให้
chief วางลงคิวจริงพร้อมกันในรอบเดียวก่อน 06:00

### 3.6 บริโภคจดหมายที่ถึง DB
`20260906_0345_COO-DECISION-*-LANE-DB.md` -> สำเนาไป `notes_to_chief/consumed/` + วาง
`<ชื่อเดิม>.CONSUMED.txt` ข้าง ๆ ต้นฉบับ (ไม่ลบ ไม่ย้ายต้นฉบับ)

### 3.7 pf-adversary
ไม่เรียก -- ไม่มี diff โค้ด (`pirate-force-server` อ่านอย่างเดียว ไม่มี commit) รอบนี้มีแต่จดหมาย/ไฟล์
รอบใน `pf_bridge`

## 4. ชุดเทสของรอบ
ไม่มี -- ไม่ได้แก้โค้ด `pirate-force-server` เลยรอบนี้ (อ่าน `current/pf_login_game_server_v141.py`
เพื่อยืนยัน citation เท่านั้น ไม่มี branch ใหม่ที่ repo นั้น)

## 5. หลักฐาน -- สองชั้นแยกกัน
### 5.1 client-observable
ศูนย์ -- รอบนี้เป็นการร่างใบขอ attended capture ยังไม่มีใครกดสวมอาวุธจริง
### 5.2 wire/DB
ศูนย์ทางโค้ด แต่ citation ทุกจุดในร่างใบ RE ตรวจกับซอร์สจริงแล้ว (§3.3): `v141.py:2481-2486,3869-3903`
+ `PF_SERIALIZER_FIELDS.tsv:763-768` + `PF_FIELD_VALIDATION.tsv:90-91`

## 6. nonclaims
1. ไม่อ้างว่า chief จะรับ `2242`/วางใบทันเวลาแน่ -- แค่ส่งของที่ `0345` ขอให้ครบก่อนเส้นตาย
2. ไม่อ้างว่าได้ capture อะไรมาแล้ว -- ทั้งสองใบยังเป็นร่าง รอเครื่อง Panya
3. ไม่อ้างว่ามาสก์ `8`/`16` ตรงกับ `n_SLOT_RHAND`/`n_SLOT_LHAND` ของ `CHARCREATE_CLASS` -- คนละ
   namespace ยังไม่มีใครเทียบ (nonclaim เดียวกับที่ใส่ในร่างใบ RE)
4. ไม่ได้แตะไฟล์ใดในเขตของสายอื่น -- diff รอบนี้อยู่ใน `pf_bridge/notes_to_chief/` และ
   `pf_bridge/rounds/` เท่านั้น ไม่มีอะไรใน `pirate-force-server`

## 7. รอบหน้าทำอะไร
1. เช็คว่า chief วางใบ RE/GT ลงคิวจริงแล้วหรือยัง (`grep` เลขจริงใน `CLIENT_RE_QUEUE.md`/
   `GAME_TEST_QUEUE.md`) -- ถ้าวางแล้วให้บริโภคใบยืนยันของ chief (ถ้ามี) แล้วปิดหัวข้อนี้ในไฟล์รอบ
2. เช็คว่า `2242` ถูก chief รับเข้า main หรือยัง (`grep .CONSUMED.txt` คู่ใบ `2242` + `list_pull_
   requests` ที่ `pirate-force-server`)
3. เช็คว่าเครื่อง Panya จับผล `ATTENDED:` ของสองใบนี้มาหรือยัง -- ถ้ามาแล้วและระบุว่ามีเฟรมตอบกลับจริง
   DB เขียน migration ใหม่ (เลขไฟล์ใหม่) รับผลนั้นเป็นงานแรก
4. ถ้าไม่มีคำตอบ/ไม่มีความคืบหน้าใน 6 ชม. (เกินครึ่งเดดไลน์ 14:00) ⇒ ทวง COO ตาม §7 ของ
   `COMMON_LANE_ROUND.md`

## งานสำรอง (ทำเมื่องานหลักติด)
1. เฝ้าคำตอบ chief/COO เรื่องนี้เป็นอันดับหนึ่ง (เดดไลน์ 14:00)
2. คิวเดิม: ชิ้น 2/3/4 ของ PLAYER/CHARACTER รอผล RE runner, ประตูเควสรอ chief whitelist

SCOREBOARD: NONE | ผู้เล่นไม่เห็นอะไรใหม่รอบนี้ -- รอบนี้เป็นงานกระดาษ (ร่างใบ RE + GT ตามคำสั่ง
`0345`) ให้ chief ตั้งเลขและวางคิวก่อนเครื่อง Panya จับผลจริง ไม่มีโค้ดใหม่จาก DB เพราะฝั่งตอบกลับของ
เฟรมสวมอาวุธยังไม่มีใครวัด (ห้ามเดาไบต์) | `notes_to_chief/20260906_0404_LANE-DB-TO-CHIEF-order-0156-
arm-b-re-draft-and-gt-draft-ready-for-numbering.md`, citation ตรวจสดกับ `pirate-force-server`
`current/pf_login_game_server_v141.py:2481-2486,3869-3903` รอบนี้

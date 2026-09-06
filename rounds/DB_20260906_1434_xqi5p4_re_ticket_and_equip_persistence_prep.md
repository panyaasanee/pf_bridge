# LANE-DB round `xqi5p4` -- arm (b) equip weapon: RE-TICKET (narrowed) + CORE-REQUEST + equip-state persistence prep

รหัสรอบ: `xqi5p4` · เวลาเริ่ม: 2026-09-06T14:34+07:00 · claim (ไม่ใช่ takeover)

## 0. ขยับ NOW/M ข้อไหน

ไม่ขยับ M2/M3/M4 โดยตรง แต่ตอบ `PANYA-ORDER 20260906_1312` ("แขน (ข) สวมอาวุธ เป็นงานแรกของรอบถัดไป
ของ LANE-DB") ด้วยการพิสูจน์ว่าเฟรมตอบยังประกอบไม่ได้จริง (ไม่ใช่เพราะ DB ทำช้า) แล้วเปิด RE-TICKET
ที่แคบลงมากจากที่ดูเหมือนตอนแรก + CORE-REQUEST จุดเสียบ `runtime.py` + เตรียมประตู DB ให้พร้อมทันทีที่
RE ตอบ ตามลำดับที่ `rounds/DB_20260906_1316_rjqssc_...md` §7 วางไว้ (RE ticket ก่อน ถ้าไม่พอสร้าง
encoder ⇒ เปิดใบ · ถ้าติด `runtime.py` seam ⇒ CORE-REQUEST รอบแรก)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว (ไม่แตะ world/scene state ทั้งรอบ)

## 1. ล็อกรอบ

`git fetch origin main` ทั้งสองรีโปสด (`pf_bridge` @ `269978c`, `pirate-force-server` @ `0b027b7`) ·
`search_pull_requests` (pf_bridge, open, title `[LANE-DB] round`): ว่างเปล่าก่อนเปิดใบตัวเอง (ใบล่าสุด
ของสาย `#1485` ปิดไปแล้ว) ⇒ ไม่มีล็อกค้าง ไม่ต้อง takeover · ใช้กิ่งที่ระบบสุ่มให้ทั้งสองรีโปตรง
(`pf_bridge`: `claude/kind-lovelace-xqi5p4`, `pirate-force-server`: `claude/intelligent-mendel-xqi5p4`) ·
commit `rounds/DB_20260906_1434_xqi5p4_claim.md` push เปิด `pf_bridge#1499 [LANE-DB] round xqi5p4:
claim` (ไม่มี marker ตอนเปิด) · list ซ้ำทันที: มีใบเดียวคือของตัวเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. แหล่งความจริงที่อ่านตามลำดับ

1. `NOW.md` (fetch สด `14:32`) — บรรทัดแรกสุด: "LANE-DB แขน (ข): RE-272 CAPTURED ... DB งานแรกรอบถัดไป
   = ตอบ op 5 + แถว DB + ส่งสถานะกลับ · เฟรมขาออกไม่รู้ ⇒ ใบ RE ต้นรอบ · ขึ้น main ≤20:30"
2. mailbox `ADDRESSEE: (LANE-)?DB` ไม่มี `.CONSUMED.txt` คู่: พบ 3 ใบ — `0749` (รับทราบ #896 เป็นงาน
   สำรอง, ตรวจแล้วว่า pf-adversary บน #896 รันไปแล้วจริงในรอบ `dtrykm` ⇒ consume ตอนนี้ ไม่มีงานใหม่จาก
   ใบนี้), `1312` (คำสั่งที่รอบนี้กำลังทำ ⇒ consume พร้อมอ้างผลรอบนี้), `1319` (จดหมายของตัวเองรอบก่อน
   ส่งออก ไม่ใช่ของเข้า ไม่ต้อง consume)
3. `AGENTS.md` §7: grep วันที่ `2026-09-06` — เจอกฎเดียว (บรรทัด `manual` ใน `SCOREBOARD_FACTS.tsv`) ไม่
   เกี่ยวกับรอบนี้
4. ไฟล์รอบล่าสุดของสายตัวเอง `rounds/DB_20260906_1316_rjqssc_...md` §7 — งานที่ส่งต่อ (อ่านสรุปด้านบน)
5. ไม่มีจดหมาย broadcast ใหม่ที่ยังไม่ consume เกี่ยวข้องกับ DB (อ่าน `FROM_CHIEF_R370` แล้ว — กฎ reaper
   ใหม่ ไม่กระทบรอบนี้เพราะไม่มี PR ค้างจากรอบก่อน)

## 3. งานที่ทำจริง

### 3.1 พยายามประกอบ encoder ของ `ItemOperateVitalRes` (0x4C13) สำหรับ "สวม" ก่อนเขียนโค้ดเดา

สั่ง `pf-static-re` agent อ่าน `external/PF_SERIALIZER_FIELDS.tsv:769-794` (26 แถว, ฟังก์ชัน
`0x005EDA20-0x005EDC31`) สด — **ยืนยัน: ยังไม่พอสร้าง encoder** (13 W-order field มีแค่ 5 ที่ tag/size/
source ครบ, อีก 8 เป็น `UNKNOWN`, W9 เรียก `0x0046F4D0` ที่ยังไม่ reclassify เป็น non-wire สำหรับ
ฟังก์ชันนี้โดยเฉพาะแม้จะมี precedent กับ 4 ข้อความอื่น) สถานะโครงการเองยืนยันซ้ำใน
`PF_V5_P1_OPEN.tsv:77`/`PF_PROTOCOL_PRIORITY.tsv:47` (`OPEN`, capture layer `NOT_OBSERVED`)

ระหว่างอ่านโค้ด server หาบริบทเพิ่ม พบ `tests/test_equip_state_static.py` (commit อยู่แล้วในรีโป
server, gate ด้วย `GAME_INSTALL_TREE.skip_unless_present()`) ที่ตอบคำถามแคบกว่าและตรงกว่า: (1) W9
(`0x0046F4D0`) คือ plain-itembag factory จริง**สำหรับฟังก์ชันนี้โดยเฉพาะ** (บรรทัด 316-337, pinned
sha256) — ตอบ RE ask #1 ของ static-re agent ไปแล้วในทางเทคนิค เพียงแต่ยังไม่ผูกกลับเข้า
`PF_A2_POOL_46F4D0_DELTA.tsv`/ปลด `OPEN` status (2) ช่องอุปกรณ์บนจอไม่ได้อ่านจากคอนเทนเนอร์แยก แต่
คำนวณ bitmask จาก `ItemAttr`'s `+0x39` byte (=`ItemAttrState.raw_u8_39` ใน `inventory.py`) เป็น
shift-count (บรรทัด 267-313) ⇒ **คำถามที่เหลือจริงแคบลงเหลือข้อเดียว: ค่า `raw_u8_39` เท่าไรคือ "สวม
อาวุธ"** ไม่ใช่ "5 call site ไม่รู้ความหมาย" อย่างที่ดูตอนแรก — เขียน RE-TICKET ใหม่ที่แคบกว่าเดิมมาก
(`notes_to_chief/20260906_1449_LANE-DB-RE-TICKET-...md`, ส่งถึง LANE-K ให้ตั้งเลขตามกฎ 6 ก.ย.)

### 3.2 CORE-REQUEST จุดเสียบ `runtime.py`

grep ยืนยัน: op=5 ไม่มีสาขา dispatch เลย (`item_move_capture.py`/`runtime.py:9719-9720` ดักแค่ op=4) —
เปิด `notes_to_chief/20260906_1452_LANE-DB-CORE-REQUEST-item-operate-vital-op5-dispatch-seam.md` ถึง
chief ตามที่ `1312`/COMMON สั่ง (ติด seam ⇒ CORE-REQUEST รอบแรก) พร้อมชี้ว่าประตู DB (§3.3) พร้อมรับ
ค่าจาก RE ทันทีที่มา ไม่ต้องรอ LANE-DB แก้เพิ่ม

### 3.3 เตรียมประตู DB (สิ่งเดียวที่เขียนได้จริงในเขตตัวเองโดยไม่เดาไบต์)

`migrations/015_character_equipment.sql` (ตาราง `character_equipment`, `slot_id` เป็นเลขดิบไม่ผูก
ความหมาย — เหตุผลเต็มในไฟล์เอง) · `SQLiteStore.equip_item`/`unequip_slot`/`list_equipped_items` (สาม
เมธอดใหม่ ไม่แตะเมธอดเดิม, สไตล์เดียวกับ `grant_learned_skill`/`spend_skill_points`) ·
`tests/test_store_character_equipment.py` (14 เทสใหม่)

`pf-adversary` เรียกต้นงาน (ตามกฎ) — คืนผล 2 จุดจริงก่อน push ทั้งคู่แก้แล้ว:
1. `character_id` เกินช่วง SQLite int64 รั่ว `OverflowError` แทน `KeyError` ทั้งสามเมธอดใหม่ (บั๊กคลาส
   เดียวกับที่เคยพบใน `get_skill_points`/`spend_skill_points`) — แก้ด้วย `_fits_sqlite_integer
   (character_id)` guard ก่อน `db.execute` ทุกเมธอด + เพิ่มเทสคุมไว้
2. ตาราง `character_equipment` ใหม่ทำให้ `tests/test_npc_interaction_wire.py::
   QuestAndShopStateGuardTests::test_store_schema_owns_no_quest_shop_or_reward_table` (allowlist ของ
   ทุกตารางที่ store เป็นเจ้าของ) แดง — แก้ด้วยการเติม `character_equipment` เข้า `EXPECTED_TABLES`
   แบบ one-line whitelist เดียวกับที่ `ground_drops`/`character_skills`/`character_home_marker` เคยทำ

## 4. ชุดเทสของรอบ

`tests/test_store_character_equipment.py` เดี่ยว: 14 passed · ร่วมกับ `test_npc_interaction_wire.py`
+ `test_persistence_boot_006_to_008.py`: 82 passed, 34 subtests passed · `git merge origin/main`:
already up to date (ไม่มี conflict) · `python3 tools_bridge/pf_gate_preflight.py --repo .`: **PASS**
(cp874, no new skips, mainmerge PASS, census PASS, ทั้งสองกิ่งถูกต้อง, bridgesize เดิมไม่ใช่ของรอบนี้)
ชุดเต็ม (`pytest tests/ -q`) เริ่มรันแล้วตอนเขียนบรรทัดนี้ ยังไม่จบ — ตัวเลขจะเติมในจดหมายติดตามถ้าจบ
หลังปลดล็อกรอบนี้ (ไฟล์รอบของตัวเองรอบนี้แก้ไม่ได้แล้วหลังปลด ตาม COMMON กฎ "ปลดล็อกแล้ว = รอบจบ")

BYTECODE_PURGED: `PYTHONDONTWRITEBYTECODE=1 python3 -B` ทุกคำสั่งรอบนี้

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
ศูนย์ -- arm (b) ยังไม่ถึงมือผู้เล่น (บล็อกด้วย RE + `runtime.py` seam ทั้งคู่ ตามที่รายงาน COO)

### 5.2 wire/DB
`pirate-force-server` PR (branch `claude/intelligent-mendel-xqi5p4`) -- ประตู DB ล้วน ไม่มีตัวเรียกใน
โปรดักชัน เทส 14 ตัวใหม่ผ่าน

## 6. nonclaims

1. ไม่อ้างว่า arm (b) เสร็จหรือใกล้เสร็จ -- บล็อกจริงด้วย RE (คำถามเดียวที่เหลือ, ดู §3.1) + CORE-REQUEST
2. ไม่อ้างว่า `test_equip_state_static.py` รันจริงในรอบนี้ -- gate ด้วยไบนารีที่ cloud clone ไม่มี อ่าน
   แค่เนื้อไฟล์/assertion ที่ commit ไว้แล้ว
3. ไม่อ้างว่า value=8/identity=4 ที่ client ส่งมาคือ `n_EQUIPTYPE` -- สังเกตค่าตรงกันหนึ่งแถวใน
   `creation_gear_by_class.tsv` เท่านั้น เขียนไว้เป็น observation ไม่ใช่ข้อสรุปในใบ RE
4. ไม่อ้างว่า `character_equipment` มีตัวเรียกจริงในโปรดักชัน -- ประตูเปล่ารอ RE+CORE-REQUEST
5. ไม่อ้างว่าเส้นตาย 20:30 มีทางทันได้ -- รายงาน COO ตรงๆ ว่าไม่ทันแน่ (`notes_to_chief/
   20260906_1455_LANE-DB-STATUS-COO-...md`)

## 7. รอบหน้าทำอะไร

1. เช็คจดหมายตอบ RE-TICKET (`1449`)/CORE-REQUEST (`1452`) ก่อนงานอื่นทุกชนิด (ตามกฎ "ใครเปิดใบ คนนั้น
   บริโภคผล")
2. ถ้า RE ตอบและ chief เปิดจุดเสียบแล้ว: เขียน encoder จริง (ค่า `raw_u8_39` ตามคำตอบ) + wire
   `store.equip_item` เข้าจุดเสียบนั้น (ถ้าจุดเสียบยังอยู่นอกเขต DB ให้ chief เป็นคนต่อสาย DB แค่ให้
   เมธอด)
3. ถ้ายังไม่ตอบ: ตรวจว่า chief ทำจุดเสียบไว้รอหรือยัง แล้วไปงานสำรอง (mailbox ~70 ใบที่ค้างตรวจแบบ
   ถูกวิธี ตามที่ `rjqssc` เริ่มไว้ หรือ `#920` ผ่านเกตหรือยัง)

## งานสำรอง (ทำเมื่องานหลักติด)

1. ตรวจ mailbox ~70 ใบ `ADDRESSEE: DB` แบบถูกวิธี (เช็คคู่ `.md`/`.md.CONSUMED.txt`)
2. `pirate-force-server#920` (skill_points/unspent_points audit) ผ่านเกตหรือยัง

SCOREBOARD: STUCK | ยังตอบ "สวมอาวุธ" บนจอไม่ได้คืนนี้ -- พิสูจน์แล้วว่าเฟรมตอบยังเดาไม่ได้จริง (ไม่ใช่
DB ทำช้า) เปิด RE-TICKET แคบ + CORE-REQUEST จุดเสียบ + เตรียมประตู DB รอพร้อมแล้ว | `notes_to_chief/
20260906_1449_...md` · `notes_to_chief/20260906_1452_...md` · `notes_to_chief/20260906_1455_...md` ·
`pirate-force-server` PR (branch `claude/intelligent-mendel-xqi5p4`)

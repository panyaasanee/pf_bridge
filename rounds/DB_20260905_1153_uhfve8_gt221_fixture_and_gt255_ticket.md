# DB round (`uhfve8`) -- 2026-09-05T11:35+07:00 -> 2026-09-05T12:16+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- อ่าน `NOW.md` ล่าสุดก่อนอื่น (ตรวจล่าสุด 10:45 โดย COO) งานรอบนี้คือการเติมงานสำรอง 2 ข้อ
ตาม `COO-DECISION 20260905_1044` ข้อ 4 (backlog เหลือต่ำกว่าเพดาน 3 ข้อ) -- ผลคือ PR เซิร์ฟเวอร์ +
จดหมาย ไม่ใช่บรรทัดของ NOW.md เอง (ไม่มีบรรทัด M ไหนที่ผมมีเขตเขียนขยับได้ตรง ๆ รอบนี้)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

## 1. ล็อกรอบ

- ต้นรอบ list PR หัวข้อ `[LANE-DB]` open ทั้งสองรีโป (ก่อนแตะโค้ด/จดหมายใด ๆ): **ว่างเปล่าทั้งคู่**
  (ตรวจผ่าน `search_pull_requests`/`list_pull_requests` ทั้ง `pirate-force-server` และ `pf_bridge`)
  ไม่มีใบค้าง ไม่ต้อง takeover
- ตัดกิ่งจาก `origin/main` สดของทั้งสองรีโป -- พบว่ากิ่งเซสชันเดิมทั้งสอง (`claude/admiring-johnson-uhfve8`
  ของ `pf_bridge` และ `claude/brave-goodall-uhfve8` ของ `pirate-force-server`) โดน reaper ลบไปแล้ว
  (PR ก่อนหน้า merge ครบ history) -- restart ทั้งสองกิ่งจาก `origin/main` สดตามกติกา "PR merged แล้ว
  = เริ่มงานใหม่จาก main" (0 commit ที่ยังไม่ merge บนทั้งสองกิ่งก่อน restart -- ตรวจด้วย
  `git log origin/main..<branch>` = ว่างเปล่าทั้งคู่ ก่อนตัดสินใจ restart)
- commit `rounds/DB_20260905_1135_uhfve8_claim.md` (สามบรรทัด: round/started/claim) push แล้วเปิด
  `pf_bridge#1303 [LANE-DB] round uhfve8: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1303` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep` แบบไม่ยึดตำแหน่งหา `ADDRESSEE: LANE-DB` บนไฟล์ที่ยังไม่มี `.CONSUMED.txt` คู่ ใน `notes_to_chief/`:
เจอ**หนึ่งใบ** -- `20260905_1044_COO-DECISION-0745-item2-dropped-until-door-b-flips-item3-closed-
refill-two-backup-items-LANE-DB.md` (ตอบใบ `20260905_1004` ของรอบก่อน `9fkcll`) -- consumed รอบนี้

อ่านสามใบก่อตั้งสาย (`20260901_1059`/`1100`/`1101`/`1112`) ครบตามกติกา "รอบแรกของเซสชัน" (เซสชันนี้
ไม่มีความจำข้ามรอบ -- เจอในอาร์ไคฟ์ `archive/notes_to_chief_2026-09/`)

อ่านไฟล์รอบล่าสุด `DB_20260905_1004_9fkcll_conflict_between_0745_and_2050_hold.md` -- ทำต่อจากที่รอบนั้น
ถามค้างไว้ (RE-222/Door B flip หรือยัง) ซึ่งใบ `1044` ตอบแล้ว: **ยังไม่ flip** -- ข้อ 2 ของ `0745`
ตัดออกจาก backlog ถาวรตามที่ COO สั่ง

เพิ่มเติมนอกกล่องจดหมายที่ตรงชื่อ (ไม่ผ่าน grep `ADDRESSEE: LANE-DB` เพราะจ่าหน้า "ทุกสาย"):
`FROM_CHIEF_R352_TO_ALL_20260905_1145.md` มอบใบ `RE-259`/`RE-260` ให้ LANE-DB ตรง ๆ ในตาราง (บรรทัด
41-42) -- อ่านและตรวจสอบเป็นส่วนหนึ่งของรอบนี้ (ข้อ 3.3 ข้างล่าง) ไม่ใช่กล่องจดหมายที่ต้อง .CONSUMED.txt
(ไม่ใช่ `ADDRESSEE: LANE-DB`) แต่เป็นงานที่มอบให้ตรง ๆ จึงทำ

## 3. ทำอะไร

### 3.1 สำรวจ backlog ของตัวเอง (2 ข้อใหม่ที่ต้องเติม)

ใช้ agent สำรวจ (general-purpose) ให้ตรวจ `rounds/DB_*.md` ล่าสุด 24 ชม. + `persistence_*.py` +
`GAME_TEST_QUEUE.md` หา candidate ที่ (ก) เริ่มได้ทันที (ข) ออกเป็น diff+เทส หรือใบ GT/RE ที่รันได้
ผลที่ verify ได้จริง (อ่านไฟล์ปัจจุบันเอง ไม่เชื่อจดหมายเก่า):

1. **`GT-221`** (`GAME_TEST_QUEUE.md:12372`) BLOCKED เพราะขาด fixture เดียว: สคริปต์รับ path DB
   ภายนอกแล้วเขียนสามแถว (`level`/`hp_max`, `hp_current=0`) ผ่าน `store.write_typed_attributes` บน
   run copy -- ตรวจสดว่ายังไม่มีจริง (`grep` หา `write_typed_attributes` คู่กับ CLI arg ใน `tests/` =
   0 hit ของสคริปต์แบบนี้) ⇒ ตรงเกณฑ์ (ก)(ข) ชัดเจน = **งานหลักของรอบนี้**
2. **`GT-255`** (`GAME_TEST_QUEUE.md:14448`) PENDING -- เนื้อใบยังไม่เขียน เจ้าของ/ผู้เขียนเนื้อ = LANE-DB
   เอง เนื้อครบอยู่แล้วในจดหมายของผมเอง (`20260904_1309`/`20260904_1434`) ขาดแค่คัดลงเทมเพลต -- ตรง
   เกณฑ์ (ข) ("ใบ GT/RE ที่รันได้") แต่ไม่ใช่ audit เพราะเป็นงานผลิตจริง (ต้องอ่าน `GT-242` เพื่อหา
   ช่องประหยัดบูตด้วย ไม่ใช่แค่คัดลอก)

ข้อ 3 (audit slot, `<=1/3`): **`RE-259`/`RE-260`** ที่ chief มอบตรงในตาราง R352 -- ตรวจซ้ำเองบนสะพาน
ก่อนส่งต่อ RE runner กันเผารอบเครื่อง Panya (ผลคือยืนยันสถานะเดิม ไม่มีอะไรใหม่ -- ดู 3.3)

### 3.2 `GT-221` -- โค้ด+เทสจริง

ไฟล์ใหม่ทั้งคู่ (เขตเขียนของสาย ไม่แตะ `store.py`/migration ใด ๆ):
- `src/pirateforce_foundation/persistence_gt221_fixture.py` -- `seed_rows`/`list_roster` + CLI
  (`python -m pirateforce_foundation.persistence_gt221_fixture`) เรียกเฉพาะ method เดิมของ
  `SQLiteStore` ที่มีอยู่แล้ว (`write_typed_attributes`/`ensure_account`/`list_characters`/
  `read_typed_attributes`/`migrate`) -- **ไม่สร้างตัวละครใหม่** (สังเคราะห์ `actor_wire` ที่ไคลเอนต์จริง
  render ได้ไม่มีทางพิสูจน์แล้วบนคลาวด์ -- `lifecycle.CharacterLifecycle.create` ต้องการไบต์จริงจาก
  ไคลเอนต์เท่านั้น) -- เขียนแค่บน "แถวที่มีอยู่แล้ว" ในสำเนา (สร้างครั้งเดียวผ่านหน้าไคลเอนต์ตามที่
  `GT-215` ทำอยู่แล้ว)
- `tests/test_persistence_gt221_fixture.py` -- 20 เคส (หลัง adversary แก้ 3 ข้อ) พิสูจน์ guard
  ชื่อ canonical, สามแถวลงตรง, ประตู validate เดิมยังใช้, id ไม่มีจริง = ล้มแบบมีชื่อ, `--list` ไม่เขียน,
  `--gt221` ปฏิเสธเลขผิด/id ซ้ำ

**pf-adversary ครั้งที่ 1** (สั่งพร้อมเริ่มงาน 3.2 ตามกติกาใหม่ `COO 0903_2345`/`1428`): พบ 3 ข้อจริง
ทั้งหมด แก้ครบก่อน push (ไม่ใช้ `ADVERSARY_PENDING` เพราะผลคืนก่อน push จริง):
1. **HIGH**: `_refuse_canonical_name` เช็คชื่อดิบ ไม่ resolve -- symlink/hardlink (`mklink`/`robocopy`
   แบบรักษา link จริงบน Windows) เลี่ยงได้แล้วเขียนทับ canonical จริง (สาธิตแล้วในสำเนาทดลองแยก) ⇒
   แก้เป็น resolve path ก่อนเทียบชื่อ (จุดเดียวกับที่ `store.py:312` ทำอยู่แล้ว) + เทสใหม่ (symlink)
2. **HIGH**: CLI ป้อนทั้งลิสต์เข้า `seed_rows` ครั้งเดียวแล้วพิมพ์หลังลูปจบ -- แถวที่ล้มกลางทาง (แถวที่ 3)
   ทำให้ไม่มีบรรทัด `SEEDED` ออกมาเลยแม้แถว 1-2 เขียนจริงแล้ว (สาธิตแล้ว) ⇒ แก้เป็นป้อนทีละแถว พิมพ์
   ทันทีที่สำเร็จ + เทสใหม่ (จับ stdout/stderr จริง)
3. **MEDIUM**: `--gt221` เช็คแค่ multiset ของ (level,hp_max) ไม่เช็ค id ซ้ำ -- id ซ้ำ+ขาดหนึ่งตัวผ่านเช็ค
   ได้เงียบ ๆ ทิ้งตัวละครหนึ่งตัวไว้ที่ค่าคงตัวเกิดใหม่พอดี (สาธิตแล้ว) ⇒ เพิ่มเช็ค id ซ้ำ + เทสใหม่

แก้ครบ รันเทสไฟล์ตัวเองซ้ำ (20 เคสผ่าน) ไม่เรียก adversary ครั้งที่ 2 (เพดาน 2/รอบยังไม่ชน แต่ตัวแก้
เล็กและตรงจุดที่ adversary ชี้ตรง ๆ ไม่ใช่การเดา)

### 3.3 `RE-259`/`RE-260` -- ตรวจซ้ำ ไม่มีอะไรใหม่

ใช้ `pf-static-re` ยืนยันซ้ำสิ่งที่หัวใบเขียนไว้เอง: `grep -rn "CNetNPC|CMyActor" external/ gamedata/` =
0 hit ทั้งคู่ (`RE-259`) · `PF_A2_ATTR_FIELD_DELTA.tsv:8-11` ยังเขียน
`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr` ตรงตัว (`RE-260`) -- ทั้งสองใบยังต้อง RE runner
บนเครื่อง Panya จริง ไม่มีทางลัดจากสะพาน ⇒ เขียนจดหมายยืนยันสถานะ ไม่แก้หัวใบเอง (ไม่ใช่เขตเขียน)

### 3.4 `GT-255` -- เนื้อใบเต็ม

ใช้ `pf-queue-author` ร่างเนื้อใบเต็มจากสองจดหมายเดิมของผมเอง (`20260904_1309`/`20260904_1434`) พบเพิ่ม
ว่า `GT-242` เอง (`GAME_TEST_QUEUE.md:13337`) มีบันทึกเฟรมขาเข้า `CheckSecondPwdVital 0x4B98` ครั้งหนึ่ง
อยู่แล้วจากรอบ attended จริง (`20260904_1430_KA1A-R309-RESULTS-*` finding 1) แต่ไม่เคยถูกดึงเป็น exhibit
แยก ⇒ ออกแบบให้ "Event B" (เปิดกระเป๋า) ยืมจังหวะของ `GT-242` เอง ไม่ต้องกดอะไรเพิ่ม เหลือ "Event A"
(ตั้งรหัสผ่านรอง) เป็นการกระทำใหม่จริงหนึ่งบล็อกสั้น ๆ แทรกหลังขั้น 7 ก่อนขั้น 8 ของ `GT-242` -- ไม่เพิ่ม
บูตใหม่ตามที่หัวใบสั่งไว้เดิม

### 3.5 จดหมายที่ส่ง (สามใบ รอบเดียว)

1. `20260905_1153_LANE-DB-GT255-full-ticket-body-ready-to-paste.md` (ADDRESSEE: chief, cc COO)
2. `20260905_1153_LANE-DB-RE259-RE260-status-still-needs-re-runner.md` (ADDRESSEE: chief, cc COO)
3. stub `.CONSUMED.txt` ของใบ `1044`

## 4. ชุดเทสของรอบ

ระหว่างทำ: `pytest tests/test_persistence_gt221_fixture.py -q` หลายครั้งระหว่างแก้ (20 เคสสุดท้าย)
ไม่รันชุดเต็มระหว่างทาง

ชุดเต็ม **สองครั้งในรอบนี้ (เกินหนึ่งครั้ง -- เหตุผลตามกติกา)**: ครั้งแรกบน commit ก่อนแก้ seam-scan
(`10847 passed, 1 failed, 323 skipped` -- `test_the_module_has_at_most_one_seam_and_it_is_the_login_one`
แดงเพราะ docstring ของโมดูลใหม่อ้างชื่อ `persistence_login_vitals` เป็นข้อความเฉย ๆ แต่เทสสแกน `src/`
หาสตริงนั้นตรง ๆ = false positive ของงานผมเอง ไม่ใช่ regression ของโมดูลอื่น) แก้โดยเขียนใหม่ไม่ให้มี
สตริงนั้น (อธิบายด้วยเลขบรรทัดในไฟล์ ticket แทน) ครั้งที่สองบน commit สุดท้ายหลังแก้: **10848 passed,
323 skipped, 20145 subtests passed, 0 failed** (528.15s) -- ครั้งที่สองคือครั้งจริงที่ push ตาม `git
fetch origin main` ก่อนรันทั้งสองครั้ง (`f98b7b18` เหมือนกันทั้งสองครั้ง ไม่มี drift)

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ศูนย์** -- รอบนี้เป็นเครื่องมือฝั่งเซิร์ฟเวอร์ (fixture script) + เนื้อใบเทส ไม่มีอะไรถึงจอผู้เล่นเอง
`GT-221`/`GT-255` เองเป็นใบ attended ที่ยังไม่รัน (`GT-221` READY เมื่อ `#819` merge · `GT-255` READY
เมื่อ chief วางเนื้อใบ)

### 5.2 wire-DB
`pirate-force-server#819` (`claude/brave-goodall-uhfve8`) -- **เปิดแล้ว 12:1x+07 พร้อม
`PF-AUTOMERGE: v4` รอเกต Windows** (สถานะ ณ ตอนเขียนไฟล์นี้ ยังไม่เห็นผล `merged: true`) หนึ่งคอมมิต
(หลัง amend แก้ seam-scan) ผ่านชุดเต็มตาม §4 ทั้งสองครั้ง · `pf_bridge#1303` claim -- เติม marker
ทันทีหลังไฟล์นี้ + จดหมาย + stub ขึ้นกิ่งเดียวกัน (ข้อ 7)

## 6. nonclaims

1. **ไม่อ้างว่า `pirate-force-server#819` ขึ้น main แล้ว** -- เปิดรอเกต ตามกฎ §22 (`1158`) ต้องอ่านผล
   job `gate` ของรอบ `pull_request` เอง แต่รอบนี้จบก่อนเกตรันเสร็จ (เขียนตามจริง ไม่รอ)
2. **ไม่อ้างว่า `GT-221` PASS แล้ว** -- แก้แค่ตัวบล็อกโค้ด (fixture) เท่านั้น การบูต attended จริงยังไม่
   เกิด นี่คืองานของ chief/Panya ต่อจากนี้
3. **ไม่อ้างว่า `GT-255` READY แล้ว** -- ส่งเนื้อใบเป็นจดหมาย ยังรอ chief วางลง `GAME_TEST_QUEUE.md` จริง
4. **ไม่อ้างว่า `RE-259`/`RE-260` มีความคืบหน้าใหม่** -- ยืนยันสถานะเดิมซ้ำเท่านั้น ป้องกัน RE runner
   เสียเวลาซ้ำ ไม่ใช่การปิดใบ
5. **ไม่แตะ `store.py`, `runtime.py`, migration ใด ๆ, `app.py`, `GAME_TEST_QUEUE.md`,
   `CLIENT_RE_QUEUE.md`, `current/pf_login_game_server_v141.py`** -- ไฟล์ใหม่สองไฟล์เท่านั้นฝั่ง
   `pirate-force-server`
6. **ไม่อ้างว่า `1101` (M4 หลัก) ปลดล็อกแล้ว** -- ยังล็อกที่ `runtime.py:6443`/Door B ของ LANE-B ตามที่
   COO ตัดสินในใบ `1044` ไม่มีสัญญาณใหม่รอบนี้

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจผลเกตของ `pirate-force-server#819` ก่อนอื่น -- ถ้าแดง แก้ในรอบนั้นทันที
3. ตรวจว่า chief วางเนื้อใบ `GT-255` ตามจดหมายหรือยัง (ไม่บล็อกใคร ไม่ต้องทวง)
4. ถ้า COO/chief เห็นว่าควรเรียก adversary ครั้งที่ 2 บนตัวแก้ 3.2 ให้ทำเป็นงานแรก
5. backlog `0745` ครบสามข้อจริงแล้ว (ข้อ 1 ปิด · ข้อ 2 ตัดถาวร · ข้อ 3 ปิดถาวร) รอบหน้าที่ไม่มีใบใหม่
   ถึง LANE-DB กลับไปหาใบ chief/COO ที่ cc ถึง LANE-DB ย้อน 12 ชม. ก่อนประกาศ "ไม่มีงาน"
6. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ

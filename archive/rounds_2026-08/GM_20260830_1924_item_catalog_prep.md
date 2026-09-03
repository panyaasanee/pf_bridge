# รอบ LANE-GM `opr2xd` — 2026-08-30T19:24+07:00

## สรุปหนึ่งบรรทัด

สร้าง `gm/item_catalog.py` (GM-042 prep) — id/ชื่อ/max stack ของไอเทมทั้ง 3,485 แถวจาก misc/consumable/quest
เทสผ่านครบ, ไม่ต่อสายรันไทม์ พบข้อเท็จจริงสำคัญ: item id ชนกันข้ามตาราง (ไม่ใช่ namespace เดียว) และยังไม่พบ
inventory-grant call site สำเร็จรูปในเอนจิน — ส่งจดหมายสถานะ ยังไม่เปิด CORE-REQUEST

## ล็อกรอบ

- ตรวจสอบมาก่อนแล้ว (โดยผู้สั่งงาน): HEAD ทั้งสอง repo ตรงกับ `origin/main`, ไม่มี PR `[LANE-GM]` เปิดค้าง
  ทั้งสอง repo (`search_pull_requests` 0 hit) — เริ่มรอบใหม่ได้ทันที
- ยึดล็อก: commit เปล่า "round claim: opr2xd" push สำเร็จทั้งคู่ เปิด draft PR
  `pf_bridge#519` และ `pirate-force-server#327` พร้อม `PF-AUTOMERGE: v4`

## กล่องจดหมาย

- `20260830_1655_PANYA-ORDER-open-RE-162-in-session-scene-change-with-a-named-consumer-chain.md` —
  คำสั่งจาก Panya เปิดใบ RE-162 (in-session scene change wire) **รับทราบแล้ว กำลังรอ** ตรวจแล้ว
  `grep RE-162 CLIENT_RE_QUEUE.md` มีแค่บรรทัดจองชื่อ ยังไม่มีผลจาก RE runner ⇒ ยังไม่มีอะไรให้ LANE-GM
  ทำตอนนี้ ไม่ได้วาง `.CONSUMED.txt` (ยังไม่ได้บริโภคจริง เพราะยังไม่มีผลให้ใช้)
- เช็ค `notes_to_chief/2026083*LANE-GM*.md`/`*-for-lane-gm*.md` ที่ยังไม่มี `.CONSUMED.txt`: เจอ 5 ไฟล์
  แต่ทั้งหมดเป็นจดหมาย **จาก** สาย GM เอง (สถานะ/CORE-REQUEST ที่ส่งออกไปในรอบก่อนๆ) ไม่มีใบไหน
  `ADDRESSEE: LANE-GM` ⇒ ไม่มีอะไรใหม่ต้องบริโภค ตรงกับที่ผู้สั่งงานตรวจไว้แล้ว
- `CORE-REQUEST-GM-041` (npc toggle call site) ยังไม่มี `CHIEF-REPLY` — รอต่อไป ไม่ส่งซ้ำ ไม่ escalate

## งานที่ทำ

สร้าง `src/pirateforce_foundation/gm/item_catalog.py` ตามรูปแบบ `npc_switch_catalog.py`/`scene_catalog.py`:

- ดึง `n_ID`/`n_QUATITY_STACK` จาก `CONSTDATA_TH__ITEM_{MISC,CONSUMABLES,QUEST}.tsv` (1,646/1,260/579 แถว)
  และชื่อแสดงผลจาก `TEXTDATA_TH__ITEM_{MISC,CONSUMABLES,QUEST}_TIP.tsv` ที่ตรงกัน (ทุก id ใน CONST
  หาชื่อใน TIP เจอครบ 100%) copy เป็น `gm/data/gm_item_{misc,consumable,quest}.tsv` (3 ไฟล์ย่อย)
- pin sha256 ทั้งไฟล์ต้นทาง pf_bridge (6 ไฟล์ บันทึกใน docstring) และไฟล์ที่ extract แล้ว (บังคับเช็ค
  ตอน import — ถ้าตารางแก้ในอนาคต เทสต้องแดง)
- ฟังก์ชัน: `is_known_item(item_id, category=None)`, `item_name(item_id, category=None)`,
  `item_category(item_id)` (คืน tuple ของทุก category ที่ตรง), `item_max_stack(item_id, category)`
- **ข้อค้นพบ**: `n_ID` ไม่ใช่ namespace เดียวข้ามตาราง — id 1 = "Adventure Key" (misc) แต่ = "Sky Lantern"
  (quest); วัดชนกัน misc∩consumable 230 ไอดี, misc∩quest 213, consumable∩quest 239 ⇒ `item_name()` โยน
  `ValueError` ถ้าเรียกกับ id ที่ชนโดยไม่ระบุ `category=` แทนที่จะเดาเงียบๆ

ไม่ต่อสายเข้า `gm/commands.py`/`chat_command_action.py`/`runtime.py` ตามขอบเขตรอบนี้ — catalog เป็นของ
เตรียมไว้ล่วงหน้าเหมือน `npc_switch_catalog.py` ก่อนมี CORE-REQUEST-GM-041

## ค้นแล้ว (ก่อนสร้างสิ่งที่พึ่งข้อมูล client) — เจอ

`gamedata/00_SEARCH_HERE_FIRST.md` บรรทัด 70-82 (รายชื่อตาราง item), แล้วอ่านตารางจริงทั้ง 6 ไฟล์ที่ใช้
(3 CONST + 3 TIP) ยืนยัน sha256 และ join id ตรงครบก่อนเขียน extraction — วัดสด ไม่ใช่เดา

## จดหมาย GM-042

ส่ง `notes_to_chief/20260830_1924_LANE-GM-STATUS-gm042-item-catalog-ready-no-grant-call-site-yet.md`
รายงาน catalog พร้อมแล้ว + ข้อค้นพบ id ชนกัน + ผล grep หา inventory-grant call site นอกเขต `gm/`:
พบทางเดียวที่เขียนไอเทมลง backpack จริงคือ `store.py:408 commit_acquired_backpack_item` ซึ่งผูกกับ flow
"เก็บของจากพื้น" เท่านั้น (identity ต้องมาจาก `mob_pickup.next_item_identity`, item ต้อง compose จาก
`mob_pickup.py` ก่อน) ไม่มีฟังก์ชัน "แจกตรงเข้ากระเป๋า" แบบไม่ผ่านการหยิบของบนพื้น — **ยังไม่เปิด
CORE-REQUEST** เพราะยังไม่รู้ว่า chief อยากให้เดินทาง (ก) simulate pickup หรือ (ข) เปิด write path ใหม่
(ข้อ (ข) จะชนกฎบ้าน "ห้าม factory ใหม่โดยไม่ถาม" เหมือนกรณี spawn)

## ทดสอบ

`pytest tests/test_gm_*.py -q` บน `pirate-force-server`: **1033 passed, 453 subtests passed**, 0 failed —
ไม่มีการถดถอย (ขึ้นจาก 1023/439 ที่รอบก่อนวัด: +10 เทสของรอบนี้เอง (`test_gm_item_catalog.py`), subtests
เพิ่มจาก subTest ในไฟล์เดียวกัน)

## self-review (adversarial)

- ไม่มี Agent tool ชนิด `pf-adversary` ให้เรียกตรงในเซสชันนี้ (ค้นด้วย ToolSearch ไม่พบ — สถานการณ์เดียวกับ
  ที่รอบ `noixtz` บันทึกไว้) ⇒ ทำ self-critique เข้มงวดแทน ไม่ได้เรียก subagent จริง
- พบและแก้เอง 1 จุดก่อน commit: `is_known_item`/`item_name`/`item_max_stack` เมื่อรับ `category=` ที่เป็น
  string ผิด (เช่น `"weapon"`) เดิมโยน `KeyError` เปล่าๆ จาก dict lookup ตรง ไม่มีข้อความอธิบาย — เพิ่ม
  `_validate_category()` ให้โยน `ValueError` ชัดเจนแทน พร้อมเทสยืนยัน 3 ฟังก์ชัน
  (`test_unknown_category_string_raises_clean_value_error_not_bare_keyerror`)
- ตรวจว่าเทสไม่ hardcode ชื่อไอเทมเดา: ทุกค่าคาดหวังอ่านจากไฟล์ TSV จริงที่ test-time (`_read_raw()`) ไม่มี
  string ชื่อไอเทม hardcode ไว้ในเทสเพื่อเทียบ (มีแค่ใน docstring ของโมดูล ซึ่งเป็นเอกสารประกอบ ไม่ใช่
  assertion)
- ตรวจว่า sha256 ที่ pin ทั้ง 6 ค่าของไฟล์ต้นทาง pf_bridge คำนวณจากไฟล์บนดิสก์จริงตอนรอบนี้ (ไม่ได้เดา/
  ก็อปจากที่อื่น) และ sha256 ของไฟล์ extract แล้ว 3 ค่าที่โมดูลบังคับเช็คตอน import ก็ผ่านจริงในเทส
  (`test_data_file_sha256_matches_pin`)
- ตรวจว่า claim "id ชนกัน" ไม่ใช่ artifact ของโค้ดที่เขียนเอง: วัดจาก set intersection บนตารางต้นทางตรงๆ
  ก่อนเขียนโมดูล (ไม่ใช่หลังเขียนแล้วมโนย้อนหลัง) ตัวเลข 230/213/239 มาจาก python ที่รันตรงบน pf_bridge
  ไม่ได้ผ่าน item_catalog.py เลย

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี — catalog เตรียมของ ยังไม่ต่อสาย `item <id> <n>` ยัง parse+log อย่างเดียวเหมือนเดิมทุกประการ
ไม่มีการเปลี่ยนพฤติกรรมโค้ดที่ผู้เล่น/ผู้เทสสังเกตเห็นได้ในเกมจากรอบนี้

## nonclaim

โมดูล gamedata-only ล้วน pin sha256 ทุกไฟล์ ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริงรอบนี้ ไม่มีการ
ต่อสายรันไทม์ (`commands.py`/`chat_command_action.py`/`runtime.py` ไม่แตะ) ข้อค้นพบเรื่อง
inventory-grant call site มาจาก grep/read ซอร์สที่ commit แล้วบน `origin/main` เท่านั้น ไม่ได้ยืนยันด้วยการ
รันจริง วัดจาก `pytest tests/test_gm_*.py` (1033 passed, 453 subtests) และ GitHub API เท่านั้น

— สาย GM รอบ `opr2xd`

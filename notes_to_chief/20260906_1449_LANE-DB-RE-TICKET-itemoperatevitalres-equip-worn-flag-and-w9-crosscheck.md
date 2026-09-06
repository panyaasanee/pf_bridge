ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย

ADDRESSEE: LANE-K (ตั้งเลข) · CC: COO

# RE-TICKET — ItemOperateVitalRes (0x4C13) สำหรับ "สวมอาวุธ" (op=5): field `ItemAttr@+0x39` worn-flag ความหมายคืออะไร + cross-check ว่า W9 คือ plain itembag codec จริงหรือไม่สำหรับฟังก์ชันนี้โดยเฉพาะ

จากสาย: LANE-DB · รอบ `xqi5p4` · ต่อจาก `rounds/DB_20260906_1316_rjqssc_...md` §7 (สั่งเปิดใบนี้เป็นงานแรกถ้ารอบหน้าอ่าน 26 แถวแล้วยังไม่พอสร้าง encoder)

## ค้นใน `pf_bridge\external\` แล้ว: เจอ <อะไร> / ไม่เจอ
เจอ `external/PF_SERIALIZER_FIELDS.tsv:769-794` (26 แถว ItemOperateVitalRes) และ `external/PF_PROTOCOL_REGISTRY.tsv:47` (vtable/handler/serializer VA) — **ไม่มี layout ที่ครบพอสร้าง encoder** (ดู §1)

## ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ
ไม่เกี่ยว — นี่คือคำถามระดับ wire/static-image ไม่ใช่ตารางข้อมูลเกม

## บริบท (ทำไมใบนี้เปิด)
`ItemOperateVitalReq` (0x4BED) op=5 (สวม), value=8, identity=0x4 ("Blade") ยืนยันซ้ำ 3 ครั้งจริง
(`notes_to_chief/20260906_1255_KA1A-R321-RESULTS-*.md` §2 ภาคผนวก A) แต่ server ไม่ตอบ (RE-272
CAPTURED). `PANYA-ORDER 20260906_1312` สั่งให้ LANE-DB ตอบ op=5 ด้วย `ItemOperateVitalRes` (0x4C13,
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:125`, คู่กับ 0x4BED ที่ `:123`) รอบนี้ (`xqi5p4`) พยายาม
ประกอบ encoder แล้วพบว่ายังไม่พอ — รายละเอียดสองชั้นด้านล่าง

## §1 ชั้น static-image (pf-static-re agent รอบนี้, ไม่ใช้ client binary): NOT PROVABLE จาก TSV อย่างเดียว
`external/PF_SERIALIZER_FIELDS.tsv:769-794` (26 แถว, ฟังก์ชัน `0x005EDA20-0x005EDC31`): จาก 13 W-order
field มีแค่ 5 ที่มี tag/size/source ครบ (W1 tag `0x08` size 1 จาก `+0x30` · W2 tag `0x0B` size 1 จาก
`STACK+0x19` · W4 tag `0x08` size 1 จาก `STACK+0x1A` · W6 tag `0x32` size 8 จาก `DEREF(...)+0x24...+0x10`
PHI-branched · W8 tag `0x08` size 1 จาก `DEREF(...)+0x24...+0x18` PHI-branched) — อีก 8 แถวเป็น
`UNKNOWN`: W3/W12 `indirect_call_not_proven_serializer_slot` (`:772,:789`) · W5/W7
`invalid_parameter_import_call_wire_effect_unproved` (`:775,:778`, CRT `_invalid_parameter_noinfo`) ·
W9 `direct_call_not_proven_serializer` เรียก `0x0046F4D0` (`:783`) · W10/W11 atomic
increment/decrement ที่ vtable+0x04/+0x0C (`:785,:787`) · W13 `direct_call_not_proven_serializer` เรียก
`0x005ED2F0` (`:794`, ไม่มี closure ในทั้ง `pf_bridge` ที่อธิบายที่อยู่นี้เลย)

สถานะโครงการเองยืนยันซ้ำ: `notes_to_chief/reference_codex_attr/PF_V5_P1_OPEN.tsv:77` และ
`PF_PROTOCOL_PRIORITY.tsv:47` ระบุ `ItemOperateVitalRes` เป็น `OPEN` ทั้ง base/effective
serializer/structural status, blocker `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED`,
`applied_overlay_chain=BASE_ONLY` (ยังไม่ได้ apply overlay ที่ reclassify การเรียก `0x0046F4D0` เป็น
non-wire แบบที่ `PF_A2_POOL_46F4D0_DELTA.tsv` ทำให้ 4 ข้อความอื่นแล้ว — grep `"ItemOperateVital"` ใน
ไฟล์ delta นั้น = 0 hit) · `PF_FIELD_VALIDATION.tsv:92` ระบุ capture layer `NOT_OBSERVED` — ไม่เคยมี
frame 0x4C13 จริงถูกจับจากฝั่ง server เลย (ตรงกับที่ server ไม่เคยตอบ op=5)

## §2 หลักฐานที่แรงกว่า: `tests/test_equip_state_static.py` (commit แล้วในรีโป server, gate ด้วย
`GAME_INSTALL_TREE.skip_unless_present()` — ต้องเครื่อง Panya ถึงจะรัน แต่ assertion ถูก pin sha256
ไว้แล้วในไฟล์นี้เอง ไม่ใช่ของใหม่ที่ใบนี้ขอ) ให้ข้อเท็จจริงที่แคบกว่าและตรงประเด็นกว่าทั้ง §1:

1. `test_item_operate_result_optional_bag_is_plain_not_collection` (บรรทัด 316-337): พิสูจน์แล้วว่า
   ฟังก์ชัน `item_operate_result_codec` (=`0x005EDA20`, ตัวเดียวกับ ItemOperateVitalRes) เรียก
   `0x46F4D0` (`plain_itembag_factory`) จริง สร้างกล่อง 0x68-byte ("plain ItemBag") ไม่ใช่ 0x90-byte
   `CollectionBagAttr` — **นี่คือคำตอบของ RE ask #1 ใน §1 สำหรับฟังก์ชันนี้โดยเฉพาะ (ไม่ใช่ analogy
   ข้ามข้อความแบบที่ `PF_V5_P1_OPEN.tsv` เตือน)** แต่ยังไม่ได้ผูกกลับเข้า `PF_A2_POOL_46F4D0_DELTA.tsv`
   หรือปลด `OPEN` status ใน `PF_V5_P1_OPEN.tsv:77`/`PF_PROTOCOL_PRIORITY.tsv:47`
2. `test_character_equipment_ui_requests_collection_bag_not_equipped_bag` (บรรทัด 267-313): ช่อง
   อุปกรณ์บนจอ (equipment UI) **ไม่ได้อ่านจาก `ItemBagAttr_Equiped`** แต่คำนวณจาก `CollectionBagAttr`
   ที่ map ทุก `ItemAttr` ใน backpack ที่ byte `+0x39` (ตรงกับ `ItemAttrState.raw_u8_39` ใน
   `inventory.py`) ผ่าน `mov dl, byte ptr [ecx+0x39]` แล้ว `shl edx, cl` (บรรทัด `0x5833AF`/`0x5833FE`)
   — คือใช้ค่า `+0x39` เป็น**shift count**สร้าง bitmask ของช่องที่สวมอยู่ ไม่ใช่คอนเทนเนอร์แยก
3. `notes_to_chief/reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:478` ยืนยัน `+0x39` ค่า sentinel
   คือ `0xFF` (ตรงกับ `ItemAttrState.raw_u8_39` default ใน `inventory.py:27`) แต่ "gameplay identity
   is not uniquely bound to Data or an exact UI slot" — **ความหมายของค่าที่ไม่ใช่ 0xFF (ตัวเลขอะไรคือ
   'สวมอาวุธ'/'สวมโล่'/ฯลฯ) ยังไม่มีใครพิสูจน์**

## §3 สรุป: คำถามที่เหลือแคบกว่าที่ §1 ทำให้ดูเหมือน (ไม่ใช่ "5 call site ไม่รู้ความหมาย" อีกต่อไป)
เพราะ §2 ข้อ 1-2 ตอบคำถาม "โครงสร้างเฟรมเป็นยังไง" ไปแล้ว (คือ codec เดียวกับที่ `inventory.py`/
`item_operate_res_hypothesis.py` พิสูจน์แล้วสำหรับ pickup — ItemAttr ก้อนเดียวในกล่อง plain itembag)
คำถามที่เหลือจริง ๆ มีข้อเดียวที่ block arm (b): **ต้องตั้งค่า `raw_u8_39` (หรือฟิลด์ไหน) เป็นเลขอะไร
ในเฟรมตอบ เพื่อให้ client คำนวณ bitmask แล้วโชว์ "Blade" เป็นอาวุธที่สวมอยู่ในช่องอุปกรณ์บนจอ**

## สิ่งที่ขอให้ RE runner ตอบ (เรียงตามลำดับความสำคัญ)
1. **[หลัก]** ในเครื่อง Panya: หา call site หรือ const-data ที่เขียนค่า `+0x39` ที่ไม่ใช่ `0xFF` ให้
   `ItemAttr` จริง (grep VA รอบ ๆ `0x5833AF`/`0x5833FE`/`0x46B466` — จุดที่ตั้งค่า sentinel `0xFF` เอง
   อาจอยู่ใกล้จุดที่ตั้งค่าอื่นด้วย) แล้วตอบ: ค่า N ที่ไม่ใช่ 0xFF หมายถึง "สวมอยู่ที่ shift-bit N" ใช่
   หรือไม่ และมีตารางแม็ป N → equip-type (weapon/shield/head/...) ที่ไหนไหม (เทียบกับ
   `n_EQUIPTYPE`/`n_SLOT_RHAND` ใน `src/pirateforce_foundation/data/creation_gear_by_class.tsv` — ค่า
   value=8 ที่ client ส่งมาใน `ItemOperateVitalReq` op=5 บังเอิญตรงกับ `n_EQUIPTYPE=8` ของ
   `n_CLASS_ID=16` แถวเดียวในตารางนั้น — **สังเกตการณ์เฉยๆ ไม่ใช่ข้อสรุป** อาจเป็นเรื่องบังเอิญ)
2. **[รอง, เพื่อปิด status ให้ตรงของจริง ไม่ใช่เพื่อ arm (b)]** ยืนยัน/ปฏิเสธว่า W3/W5/W7/W10/W11/W12/W13
   ใน `PF_SERIALIZER_FIELDS.tsv:769-794` ล้วนเป็น non-wire lifecycle/refcount/CRT-param-check
   artifact (ตามรูปแบบที่ `PF_A2_POOL_46F4D0_DELTA.tsv`/`PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv`
   ทำกับ 4 ข้อความอื่นแล้ว) **เฉพาะสำหรับฟังก์ชันนี้** ไม่ใช่โดย analogy แล้วเติมแถว
   `ItemOperateVitalRes` เข้าไฟล์ delta ทั้งสอง ถ้าจริง — จะปลด `OPEN` status ใน `PF_V5_P1_OPEN.tsv:77`
3. resolve `0x005ED2F0` (W13, `:794`) — ไม่มี closure ไหนในทั้ง `pf_bridge` อธิบายที่อยู่นี้เลย

## เกณฑ์ที่ทำให้ตอบได้ (ไม่ต้องเปิดเกม ไม่ต้องแคปเจอร์สด — static ล้วนถ้าเครื่อง Panya มี binary)
ตอบข้อ 1 อย่างเดียวก็พอให้ LANE-DB เขียน encoder ได้ (มีโครงสร้างเฟรมพร้อมจาก §2 แล้ว เหลือแค่ค่า
`raw_u8_39` ที่ถูกต้อง) — ข้อ 2/3 เป็นการปิดบัญชี status ให้ตรงความจริง ไม่ block arm (b)

## nonclaims
1. ไม่อ้างว่า value=8/identity=4 ที่ client ส่งมาคือ n_EQUIPTYPE จริง — สังเกตค่าตรงกันหนึ่งแถวเท่านั้น
2. ไม่อ้างว่า `test_equip_state_static.py` เคยรันจริงในรอบนี้ (gate ด้วย binary ที่ cloud clone ไม่มี) —
   อ่านเนื้อไฟล์/assertion ที่ commit ไว้เท่านั้น
3. ไม่อ้างว่าโครงสร้างเฟรม (tag/size ตาม §2) พิสูจน์แล้วสำหรับ "สวม" โดยเฉพาะ — พิสูจน์แล้วสำหรับ
   "pickup" (`item_operate_res_hypothesis.py`/RE-059) เท่านั้น ยังไม่มี capture ของเฟรมตอบ "สวม" จริง
   (`PF_FIELD_VALIDATION.tsv:92`: `NOT_OBSERVED`) — สมมติว่าโครงสร้างเดียวกันใช้ได้กับ "สวม" ด้วย เป็น
   ข้อสันนิษฐานที่สมเหตุสมผล (โค้ดฝั่ง client ใช้ handler เดียวกันสำหรับทุกกรณีของ 0x4C13) ไม่ใช่ข้อพิสูจน์

links: `notes_to_chief/20260906_1316_...rjqssc...md` §7 · `notes_to_chief/20260906_1255_KA1A-R321-
RESULTS-*.md` §2 · `notes_to_chief/reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:478` ·
`notes_to_chief/reference_codex_attr/PF_V5_P1_OPEN.tsv:77` · `notes_to_chief/reference_codex_attr/
PF_A2_POOL_46F4D0_DELTA.tsv` · `pirate-force-server tests/test_equip_state_static.py:267-337` ·
`pirate-force-server src/pirateforce_foundation/inventory.py:21-28`

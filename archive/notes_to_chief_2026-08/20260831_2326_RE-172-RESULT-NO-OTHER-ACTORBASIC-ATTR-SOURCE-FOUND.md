[ถึง: chief, COO, เจ้าของ | จาก: สาย GM รอบ `thhkup` · 2026-08-31T23:26+07:00]
[ตอบใบ: `CLIENT_RE_QUEUE.md:3277` RE-172 · เปิดโดยสาย GM เอง บริโภคผลเอง ตามสัญญาผู้บริโภคของใบนั้น]
[กระตุ้นโดย: `20260831_2305_KA1A-TO-LANE-GM-*` + `20260831_2315_KA1A-SELFCORRECTION-*` — กะ1-A ชี้ถูกว่าใบนี้เป็นของสาย GM เอง ตอบได้แบบ static ไม่ต้องรอสาย RE]

# RE-172 RESULT — ทั้งสองคำถามตอบลบ (bounded-negative), ปิดใบชั้น wire/DB

## Q1 — message ID อื่นนอก 0x309A/CreateActorDataEx ที่รับ/ส่ง ActorAttr/BasicAttr แบบเต็ม: **ไม่พบ**

วิธีค้น: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีชื่อ "Attr" แค่สองแถว —
`Express_ClientGetExpressItemAttrsVital` (item attrs คนละคลาส) กับ `UpdateAttrVital` (0x309A, รู้แล้ว)
ขยายค้นทั้ง 520 ชื่อ message ใน `external/PF_SERIALIZER_FIELDS.tsv`: ไม่มีแถวใดอ้าง codec entry
point ของ `ActorAttr` (`0x00466230`) หรือ `BasicAttr` (`0x004656F0`) เป็น call target เลย
(`grep -c` = 0 ทั้งคู่) — รวมถึง `UpdateAttrVital` เอง เพราะ dispatch เข้าคลาสเหล่านี้เป็น virtual
call ผ่าน vtable+0x34 (`UpdateAttrVital.Entry` เป็น polymorphic, เลือก concrete class จาก type-key)
ซึ่งเครื่องมือ census ระดับ message ไม่ resolve จุดเรียกแบบนี้

ตรวจ candidate ที่ชื่อดูเกี่ยวข้องที่สุดอีกตัว — `CWebGMVital_GSGC` (0x2DEF, ดูชื่อเหมือนเครื่องมือ GM
บนเว็บ): field shape จริง (`external/PF_SERIALIZER_FIELDS.tsv` แถว 6463-6483) คือ u16 หนึ่งฟิลด์ +
nested block (u16+u64) + u32 ปิดท้าย — 4 ฟิลด์ ไม่ใช่ ~55 ฟิลด์แบบ `attr_wire.py::FIELDS` และไม่มี
tag/offset ตรงกับ `ActorAttr`/`BasicAttr` เลยสักฟิลด์ — ตัดออก

ค้นลึกสุดเท่าที่มีในเครื่องนี้ — `notes_to_chief/reference_codex_attr/PF_ATTR_CLASS_CENSUS.tsv`
(Codex checkpoint, IMAGE sha256 `9627211412...8623`) มีแถว `ActorAttr`/`BasicAttr` จริง (ทั้งคู่
`PROVEN_EXACT` RTTI, parent chain `PcRefObject>Attribute>DBAttribute>BasicAttr[>ActorAttr]`) แต่
คอลัมน์ `slot34_role` ของทั้งสองแถวระบุตรง ๆ ว่า `NO_REGISTERED_VTABLE_BOUNDARY_THROUGH_OWN_PLUS_0x34`
— แม้ census ที่ลึกที่สุดที่มีก็ยังพิสูจน์ไม่ได้ว่า container ไหนเรียกเข้าคลาสนี้จริง **รวมถึง
`UpdateAttrVital` เองก็ไม่ถูกพิสูจน์จากหลักฐานชุดนี้ว่าเป็นผู้ถือ entry ชนิดนี้จริง** (สอดคล้องกับ
`PF_ATTR_CONTAINER_SEMANTICS.tsv` แถว `UpdateAttrVital.Entry`:
`OUTER_CODEC_ONLY_NO_UNIQUE_CHILD_RTTI_BINDING`, "type-key to concrete Attr class/vtable map is not
proved")

**สรุป Q1**: ไม่มี message ID อื่นที่พบ และแม้แต่ตัวที่รู้อยู่แล้ว (`UpdateAttrVital`) ก็ไม่มีหลักฐาน
static ที่ commit อยู่ในเครื่องนี้ผูกมันเข้ากับ `ActorAttr`/`BasicAttr` โดยเฉพาะ — เป็น "ไม่พบ" ไม่ใช่
"พิสูจน์ว่าไม่มี"

## Q2 — column/table DB นอก `characters.actor_wire` ที่ persist ฟิลด์เหล่านี้: **ไม่พบ**

อ่าน `pirate-force-server/src/pirateforce_foundation/model.py` เต็มไฟล์ (21 บรรทัด): `Character`
มีแค่ `id, account_id, selector, name, actor_wire, avatar_wire, identity_lo, identity_hi, position`
— ไม่มี level/hp/mp/stat ใด ๆ

อ่าน `migrations/001_initial.sql` ถึง `005_character_backpack_identity_counter.sql` ทั้ง 5 ไฟล์เต็ม:
ตาราง `characters` (actor_wire/avatar_wire BLOB + identity/name เท่านั้น), `character_positions`
(x/y/z/heading), `character_backpacks`/`character_backpack_items` (item/slot/quantity) — ไม่มีคอลัมน์
ชื่อหรือรูปร่างตรงกับ `attr_wire.py::FIELDS` ('level'/'hp_current'/'str'/'con'/'dex'/'int_'/'per'/
'class_id'/'skill_points'/'experience'/'cash' ฯลฯ) แม้แต่คอลัมน์เดียว

## ปิดใบ

ทั้งสองคำถามตอบลบ ตรง pass criteria ของใบเอง ("ผลลบก็เป็นคำตอบ") — ปิด `RE-172` ชั้น wire/DB เป็น
**DONE / BOUNDED-NEGATIVE** อัปเดต `CLIENT_RE_QUEUE.md:3277` แล้วในรอบนี้

## ผลต่อ

`COO-DECISION 20260831_1843` ข้อ "กำหนดเมื่อไร" สั่งไว้ล่วงหน้า: RE-172 ตอบลบ ⇒ ส่งตรงไปเจ้าของ
(cc COO) เป็นคำถามนโยบายทาง 1 vs 2 ไม่ใช่ COO เคาะแทน — เปิดใบแยกรอบนี้:
`20260831_2327_LANE-GM-TO-OWNER-attr-wire-path1-vs-path2-after-re172-negative.md`

## nonclaims

1. ไม่อ้างว่าพิสูจน์แล้วว่า **ไม่มี** แหล่งอื่นอยู่จริง — พิสูจน์ได้แค่ว่า "ไม่พบในหลักฐาน static ที่
   commit อยู่ในเครื่องนี้" (520 ชื่อ message + census ลึกสุดที่มี) ถ้ามี capture จริงหรือ disassembly
   เพิ่มเติมนอกเครื่องนี้อาจพบสิ่งที่ไม่เห็นตอนนี้
2. ไม่อ้างว่า `UpdateAttrVital` **ไม่ใช่** ผู้ถือ `ActorAttr`/`BasicAttr` — แค่ไม่มีหลักฐาน static ผูกมัน
   ทั้งสองทาง (ทั้งยืนยันและปฏิเสธ)
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`gm_accounts.json`/
   `scenarios/world_*.json`/`scenarios/combat_*.json`
4. ไม่ให้สถานะ GM กับบัญชีใดที่ไม่อยู่ใน `gm_accounts.json`
5. `attr_wire.py`/`build_named_field_update` ยังคง fail-closed เหมือนเดิมทุกไบต์ ไม่มีการแก้โค้ดจาก
   ผลใบนี้ในรอบนี้

— สาย GM รอบ `thhkup`

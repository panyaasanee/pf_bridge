ADDRESSEE: chief · cc: COO, เจ้าของ
ประเภท: CORE-REQUEST-GM-044 — คำถาม static ที่ routing ผ่าน chief ไปสาย RE (ไม่ใช่ runtime.py wiring
request — ตรวจแล้วว่าไม่มีจุดเสียบใหม่ให้ขอ ดูเหตุผลข้อ 3 ด้านล่าง)

# สามบรรทัด

`COO-DECISION 2026-08-31T16:50+07:00` สั่งให้สาย GM ออกแบบกลไก "เก็บบล็อกดิบต่อ connection" ก่อนขอ
version-confirmation unlock ของ `gm/attr_wire.py` — ค้นแล้วพบว่าเซิร์ฟเวอร์ไม่มีแหล่งข้อมูลนี้เก็บไว้ที่ไหน
เลยวันนี้ ยกเว้นความเป็นไปได้หนึ่งจุดที่ยังไม่ได้ตรวจสอบ: `characters.actor_wire` BLOB คำถามนี้ถามแค่จุด
เดียว: sub-structure ข้างในมันตรงกับ layout ที่ `gm/attr_wire.py::FIELDS` ใช้หรือไม่

# ค้นแล้ว: เจอ/ไม่เจอ

ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` ก่อน —
**ไม่เจอ** อะไรเกี่ยวกับ `CreateActorDataEx`/`ActorAttr` sub-structure layout ในสองไฟล์นี้ (นี่เป็นคำถาม
เรื่อง client wire format ไม่ใช่ gamedata — คาดว่าไม่เจอในนี้อยู่แล้ว ค้นตามกฎแต่ผลลบ)

ค้น `pirate-force-server` เต็มต้นไม้หา `CreateActorDataEx`/`decode_create_actor_data_ex`: เจอ
`legacy.decode_create_actor_data_ex` (เรียกใน `runtime.py`'s foundation-create path) และ
`gm/actor_wire.py` (Known-safe edits to the otherwise opaque wire — เอกสารตัวเองบอกว่า "the rest of the
AvatarAttr remains opaque and byte-preserved", ไม่มีการ decode ฟิลด์อื่นนอกจาก identity/selector/name)
ไม่พบไฟล์ใดถอดรหัส sub-structure เต็มรูปแบบของ `CreateActorDataEx` เทียบกับ `FIELDS`

# คำถาม (static, ตอบได้จากภาพไบนารีหรือ capture ที่มีอยู่ ไม่ต้องมี attended session)

`CreateActorDataEx` (ที่ `legacy.decode_create_actor_data_ex`/`gm/actor_wire.py` จัดการอยู่) มี
sub-structure ฝังอยู่ข้างในที่เป็น ActorAttr/BasicAttr DBAttribute collection แบบเดียวกับที่
`UpdateAttrVital` (0x309A) ใช้หรือไม่ — ถ้าใช่ tag/offset ของแต่ละฟิลด์ตรงกับตาราง 55 แถวใน
`gm/attr_wire.py::FIELDS` (ที่มาจาก `reference_adhoc_probe/adhoc_attr_probe.py`) หรือไม่

**ถ้าตรง**: `characters.actor_wire` (เก็บอยู่แล้วทุกตัวละคร, byte-preserved) เป็นแหล่ง raw-block ที่ใช้ได้
ทันทีสำหรับ `RawBlockCache.capture_initial()` — ไม่ต้องแก้ `runtime.py`/เปิด `lane_hooks` จุดใหม่เลย สาย
GM อ่าน BLOB นี้ (ผ่าน `session.foundation.selected.actor_wire` ถ้าเข้าถึงได้จากจุดที่ `gm/` เรียกอยู่
แล้ว, หรือ chief ชี้ทางที่ถูกให้) ถอดเองในเขต `gm/` ได้เลย

**ถ้าไม่ตรง**: ไม่มีแหล่งข้อมูลนี้อยู่จริงวันนี้ — สาย GM จะเขียนใบ ASK-COO แยกถามว่าจะเลือกนโยบายไหน (ยอม
รับความเสี่ยงเคลียร์ฟิลด์ไม่รู้จักครั้งแรก vs จำกัดขอบเขตให้ตลอดไปเฉพาะฟิลด์ที่มีชื่อ) แทนที่จะรอ RE ตอบ
เรื่อง layout ต่อไปเรื่อย ๆ

# ทำไมใบนี้ไม่ใช่คำขอเปิดจุดเสียบ runtime.py

ตรวจแล้ว (รายละเอียดในรอบนี้, `pf_bridge/rounds/GM_20260831_1736_rawblk_*.md`): `runtime.py` ไม่เคย
ประกอบ ActorAttr/BasicAttr DBAttribute block รูปแบบ 0x309A ตอน login เลย (`model.Character` ไม่มีฟิลด์
level/hp/stat ให้ประกอบด้วยซ้ำ) — จุดเสียบ `lane_hooks` ใหม่ที่ดักตอน login จะเป็นการดักข้อมูลที่ไม่มีอยู่
จริง ไม่ใช่ปัญหาที่ "ไม่มีจุดเสียบพอ" (ADDENDUM G's exception) แต่เป็นปัญหาที่ "ไม่มีข้อมูลให้ดักตั้งแต่ต้น"
— คนละเหตุผลกัน จึงไม่ขอจุดเสียบใหม่รอบนี้ ขอแค่คำตอบ static ข้างบนก่อน

# ระบุ (ตามฟอร์แมต CORE-REQUEST)

- โมดูล: `gm/attr_wire.py` (มีอยู่แล้วรอบนี้ — composer+cache พร้อม รอแค่แหล่งข้อมูล)
- ฟังก์ชันที่ต้องเรียก: ไม่มี (นี่คือคำถาม ไม่ใช่คำขอ wiring)
- ตรงไหนของ runtime: ไม่มีจุดที่ต้องแก้ — คำถามอยู่ที่ `legacy.decode_create_actor_data_ex`/client image
  ฝั่ง static เท่านั้น
- เทสที่พิสูจน์: `tests/test_gm_attr_wire.py` (46 ใบ, มีอยู่แล้ว, ครอบ composer/cache — จะเพิ่มเทส decode
  `actor_wire` BLOB เมื่อมีคำตอบ)

PF-AUTOMERGE: v4

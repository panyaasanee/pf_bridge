[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, สาย RE (Codex), เจ้าของ | จาก: LANE-GM รอบ `h6rsgl` · 2026-09-01T09:21+07:00]
[อ้างอิง: 20260901_0302_FROM_CHIEF_R278_priority-reorg-panya-order-P1-P2-P3-plus-new-builds.md (หัวข้อ P-2),
20260901_0215_PANYA-ORDER-drop-milestones-all-hands-on-three-things-plus-new-gm-and-ui-work.md]

# LANE-GM-STATUS — P-2 (สีชื่อมอน): ยังไม่มี fontstyle ของ "ตาย=เทา" ที่พิสูจน์แล้ว, เสนอใบ RE แคบ

## ค้นแล้ว: เจอบางส่วน

ตามคำสั่งเจ้าของข้อ 5 ("การหาข้อเท็จจริงแบบ static/headless ทำต่อได้เลย" แม้ `GT-146`/ใบตีมอนปิดคิว
ชั่วคราว) รอบนี้ค้นข้อมูล static/headless ที่ commit แล้วทั้งหมดที่เกี่ยวกับสีชื่อ NPC (ไม่เปิด client
image/capture — ไม่มีในสภาพแวดล้อมนี้) ผลสรุป:

**ยังไม่มีแถวใน `PF_ATTR_NAME_COLOR_SELECTOR.tsv` ที่เป็น `PROVEN_EXACT` + `selector_lane=typed_CNetNPC`
สำหรับเงื่อนไข "ตาย"** — มีแค่ 2 fontstyle ที่ยืนยันแล้วในเลนที่ typed จริง (61=สู้/ธรรมดา, 62=ธรรมดา
ไม่สู้) ไม่มีแถวที่สาม

พบตัวเลือกที่ใกล้เคียงที่สุด: `fontstyle_id=63` ที่แถว 9/11/12 ของตารางเดียวกัน แต่ทั้งสามแถวมาจากเลน
`untyped_dynamic_controller` (`owner_class_unproved`) ไม่ใช่ `typed_CNetNPC` แถว 9 อ้าง predicate ที่
`0x0043BD70..0x0043BD9D` ซึ่ง **พิสูจน์แยกต่างหากแล้วจริง** (ทั้งใน `PF_ATTR_ROLE_DISCRIMINATOR.tsv`
row `ACTOR_DEATH_SHARED` และ `PF_COMBAT_LIFECYCLE.tsv` row `CL-IMG-018`) ว่าเป็น shared death predicate
ของ 4 ตระกูล actor รวม `CNetNPC` — แต่ nonclaim ของแถว 9 เองเขียนตรง ๆ ว่า **"FontStyleID 63 is not
equivalent to dead"** เพราะยังไม่พิสูจน์ว่า predicate นี้ถูกเรียกผ่าน vtable ของ `CNetNPC` จริง (อาจเป็น
เลนทั่วไป/`CNetActor`) `RE-109` (ปิดแล้ว, bounded-negative) มี `BUILD_IMPACT: NONE` ชัดเจนอยู่แล้ว — ห้าม
เดาสีจาก id ใด ๆ ในตารางนี้จนกว่าจะพิสูจน์ทางเรียกจริง ตรงตามที่ RE-109 ห้ามไว้ สายนี้จึงไม่เขียนโค้ดสี
รอบนี้ (จะเป็นการเดา ขัดกับ `RE-109`)

`RE-155` (เปิดอยู่, `[NEEDS-ATTENDED-CAPTURE]`) เป็นทางปิดเดียวที่มีอยู่ในบันทึกเดิม แต่**ไม่ใช่เรื่อง
ตาย=เทา** (เป็นเรื่อง NPC เขียว->เหลือง กับ Training Iron Man แดง) — ไม่ช่วยปิดช่องว่างนี้โดยตรง

## 🔴 ปัญหาโครงสร้างที่พบ (ไม่ใช่ของสายนี้ตัดสิน — แจ้งให้ chief/COO เห็น)

ทางปิดที่มีอยู่ของ P-2 (attended capture ตาม `RE-155`) ชนกับคำสั่งเจ้าของเองที่ห้าม "ใบตีมอนทั้งหมด"
เข้าคิว attended จนกว่า P-1/P-2 จะเสร็จ — ถ้า "สังเกตสีชื่อ NPC เฉย ๆ ไม่ตีจริง" **ไม่**นับเป็น "ใบตีมอน"
ตามเจตนาของเจ้าของ นี่คือทางเดียวที่เหลือจริง แต่สายนี้ไม่มีสิทธิ์ตีความคำสั่งเจ้าของเอง (ไม่ใช่เขตของ
สาย) — ส่งต่อให้ chief/COO ตัดสินว่า `RE-155`-style capture (ยืนดูป้ายชื่อ ไม่โจมตี) เข้าข่ายข้อยกเว้น
หรือไม่ [สมมติของสาย GM - รอ COO ยืนยัน: ตอนนี้ถือว่ายังห้าม จนกว่าจะมีคำตอบ]

## ข้อมูลเก่าที่ควรรู้ (data hygiene, แจ้งเฉย ๆ ไม่ใช่ block)

`PF_ATTR_ROLE_DISCRIMINATOR.tsv` และ `PF_COMBAT_LIFECYCLE.tsv` (สองตารางที่ใช้ยืนยัน predicate
`0x0043BD70` ข้างต้น) **ไม่ปรากฏใน `artifacts{}` ของ `PF_ATTR_GENERATION_MANIFEST.json`** และ
`reference_codex_attr/README_WHAT_THIS_IS.md` มีป้าย STALE ค้างอยู่เจาะจงชื่อ
`PF_ATTR_ROLE_DISCRIMINATOR.tsv` V2 ว่ายังไม่ยืนยันกับ generation ปัจจุบัน — `image_sha256` ที่ฝังในแถว
ตรงกับ image ที่ pin ไว้ก็จริง แต่ไม่ได้ผ่าน checksum process แบบเดียวกับตารางหลัก ไม่ใช่เหตุด่วน แจ้งให้
สาย RE/chief ทราบเผื่อกระทบงานอื่นที่อ้างอิงสองตารางนี้

## ขอ (เสนอใบ RE แคบให้ chief มอบสาย RE — ไม่ใช่ CORE-REQUEST เข้า runtime.py)

`[PROPOSED]` หัวข้อ: พิสูจน์ว่า predicate ตาย `0x0043BD70..0x0043BD9D` ถูกเรียกผ่าน vtable ของ
`CNetNPC` (`0x00F2CD48`) จริงหรือเลนทั่วไป — ใช้วิธี typed-downcast เดียวกับที่ปิดแถว 13-15 สำเร็จแล้ว
(`CNetNPC_cast=0x00469700..0x0046972E`) ถ้าพิสูจน์ได้ ให้ยืนยัน RGB จริงของ `fontstyle_id=63` ผ่าน
`UILabel_FontStyleID_parser_setter` (`0x00AA488F`) เทียบกับ 61/62 ที่ถอดแล้วเป็น control — ใบนี้ไม่เปิด
ซ้ำ RE-067/109/155 ใช้ pin เดิมทั้งหมด เป็นก้าวถัดเดียวที่ตารางเองระบุไว้แล้ว (`required_next_evidence`)

## nonclaim

1. ไม่อ้างว่า fontstyle 63 คือสีเทาของมอนตาย — ตารางเองปฏิเสธการอ้างนี้ตรง ๆ
2. ไม่เขียนโค้ดสีใด ๆ รอบนี้ — จะเป็นการเดาขัด `RE-109` `BUILD_IMPACT: NONE`
3. ไม่ตัดสินเองว่า attended capture แบบสังเกตอย่างเดียวเข้าข่ายข้อยกเว้นคำสั่งเจ้าของหรือไม่ — ส่งต่อ COO
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`
5. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone

— สาย GM รอบ `h6rsgl`

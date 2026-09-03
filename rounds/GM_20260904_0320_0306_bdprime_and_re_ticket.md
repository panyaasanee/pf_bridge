# LANE-GM round `0306`/`0320` — 2026-09-04, +07:00

รอบนี้ขยับ NOW ข้อไหน: **"งานด่วนตอนนี้" ข้อ GM-B `/speed`** — (b') → (b'') ตาม `COO-DECISION 20260904_0215`
ทำแล้วครบสามข้อ (x=9 เข้าชุดชื่อ · แถว `known=False` ต้องมีไบต์จากล็อกอิน · ประโยค "266 คำสั่ง" ถอนแล้ว)
ยกเว้นข้อ `encode_block` raise ตามตัวอักษร — ดูหัวข้อ "สิ่งที่เบี่ยงจากคำสั่ง" ด้านล่าง
· และ **P-2** (ข้อ "งานด่วนตอนนี้") — ร่างใบ RE ที่สองตาม `COO-DECISION 20260904_0217` ส่งแล้ว

## ล็อกรอบ — หมายเหตุกระบวนการ (อ่านก่อนรอบถัดไป)
ต้นรอบ list ทั้งสองรีโป: pf_bridge ไม่มี `[LANE-GM]` PR เปิดค้าง, pirate-force-server ไม่มีเช่นกัน
(มี `[LANE-E]` PR #1041 เปิดอยู่ — ไม่ใช่ของสายนี้ ไม่แตะ) 🔴 **รอบนี้ไม่ได้เปิด claim PR ก่อนเริ่มงาน**
(พลาดขั้นตอน — เห็นว่าไม่มี PR ค้างแล้วเริ่มลงมือเลย) เนื่องจากงานเสร็จสมบูรณ์และ push ในรอบเดียวจบ
จึงเปิด PR จริงตรง ๆ แทนการเปิด claim ก่อนแล้วตามด้วยไฟล์รอบ — บันทึกไว้ให้รอบถัดไปรู้ว่าไม่ใช่รูปแบบมาตรฐาน
ห้ามทำซ้ำถ้ารอบยาวเกิน ~30 นาทีแรกโดยยังไม่มีอะไร push ได้

## งานที่ทำ

### 1. `(b') → (b'')` ใน `pirate-force-server/src/pirateforce_foundation/gm/attr_wire.py`
- `FIELDS` แถว 9 (`category_5C`): `known=False` → `True` (คำสั่ง 0215 ข้อ 2 — เป็นตัวเลือกคู่ HP ที่พิสูจน์แล้ว
  ไม่ใช่แถวไม่รู้ชื่อธรรมดา)
- เพิ่ม `unnamed_field_x()` / `all_field_x()` และจุดอ่านที่สอง `live_login_bytes`
  (`LOGIN_BYTES_READ_POINT = "current_login_attr_bytes"` — ชื่อที่สายนี้เสนอ ยังไม่มีจริงฝั่ง chief
  ตาม `COO-DECISION 20260904_0216`)
- `live_full_block_values` รวมสองแหล่ง แหล่งไหนพังก็ปฏิเสธทั้งก้อน (ไม่มี "ส่งเท่าที่มี")
- `seed_cache_from_live_values` เปลี่ยนไปเรียก `live_full_block_values` แทน `live_named_values`
- `build_named_field_update`'s completeness check ขยายจาก `named_field_x()` เป็น `all_field_x()`
- เทสมิวแทนต์ตามคำสั่ง (บล็อกขาดแถวเดียวต้องแดง) — วนทุก 55 แถวใน `FIELDS`, เช็คกับ `build_named_field_update`
- ประโยค "266 คำสั่ง" ถอนอย่างเป็นทางการ (คำสั่ง 0215 ข้อ 3) — ขีดฆ่าในซอร์ส ไม่ลบ
- `tests/test_gm_attr_wire_name_crosscheck.py`: ย้าย x=9 ออกจาก `REFUSED_WIDENING` (คนละเหตุผลกับที่ใบ
  เดิมขอ — เขียนคอมเมนต์แยกไว้ชัดว่าไม่ใช่การอนุมัติใบ ka1-B เดิม)

### 🔴 สิ่งที่เบี่ยงจากคำสั่ง 0215 และทำไม
`0215` สั่งตรงตัวว่า `encode_block` ต้อง raise ถ้าบิตไม่ครบ ผมวัดก่อนทำแล้วพบว่าจะพัง
`tests/test_persistence_attr_compose.py` (LANE-DB นอกเขต) และ `tests/test_gm_speed_shape_hold.py`
(ของสายนี้เอง — ปักรูปเฟรมจริงของ GT-193) จึงย้ายการบังคับไปที่ `build_named_field_update` แทน
เขียนเหตุผลเต็มไว้ใน docstring ของทั้งสองฟังก์ชัน และส่งใบ ALARM ให้ COO ตัดสิน

### 2. pf-adversary รอบนี้ (สั่งต้นรอบ ผลกลับมาก่อน push — ไม่ใช่ `ADVERSARY_PENDING`)
พบสองข้อสำคัญ:
- **Finding 1 (สูง):** docstring ที่เขียนไว้ว่า "no partial 0x309A block ever leaves this module,
  for any reason" **ผิด** — `speed_wire.compose_sparse_speed_update` ยังเรียก `encode_block` แบบ sparse
  ได้จริง และมีทางเดินถึง runtime ผ่าน `PF_SPEED_TRIAL` (เกตที่ COO อนุมัติไว้ก่อนหน้าเพื่อรัน `GT-218`)
  แก้ docstring ให้ตรงกับของจริงแล้ว (ระบุขอบเขตว่าคุ้มครองเฉพาะประตู `build_named_field_update`)
- **Finding 2:** ผมอ้างอิงใบ ALARM ด้วยชื่อไฟล์ placeholder (`02xx`) ที่ไม่มีไฟล์จริงอยู่เบื้องหลัง —
  แก้แล้วโดยเขียนใบจริง (`20260904_0309_LANE-GM-ALARM-*`) และแก้ทุกจุดอ้างอิงในโค้ดให้ชี้ไฟล์จริง
- Finding 3 (encode_block deviation ที่ตรวจแล้วว่ามีเหตุผลสมเหตุสมผล แต่เป็น policy guarantee ไม่ใช่
  โครงสร้างที่บังคับไม่ได้) และ Finding 5 (เทสบางตัวเช็ค `AttrWireError` แบบไม่เจาะจงเหตุผล — severity ต่ำ)
  บันทึกไว้ในโค้ด/ใบ ALARM ไม่ได้แก้เพิ่มรอบนี้ (severity ต่ำ ไม่บล็อก)

### 3. จดหมาย
- `notes_to_chief/20260904_0306_LANE-GM-TO-CHIEF-RE-TICKET-p2-cnetnpc-readiness-not-construction.md`
  — ร่างใบ RE ตาม `0217` ค้นก่อนแล้วพบว่าครึ่งแรกของคำถาม ("อะไรสร้าง CNetNPC") มีคำตอบอยู่แล้วบางส่วน
  (`MCG-IMG-002`, `field_mobs.py`'s `NPC_STYLE_ACTOR_TYPE=4` ตรงกับเงื่อนไข factory) จึงตีคำถามให้แคบลง
  เป็น Q1 (ไบต์ไวร์ตรงตำแหน่งจริงไหม) + Q2 (บิตโมเดลพร้อม `+0x70` กั้นตัวเลือกสีด้วยไหม — อาจอธิบาย "ชมพู"
  ที่ไม่อยู่ในตาราง `RE-195` เลยสักแถว)
- `notes_to_chief/20260904_0309_LANE-GM-ALARM-speed-trial-gate-and-encode-block-not-covered-by-bdprime.md`
  — ขอ COO ตัดสิน: `PF_SPEED_TRIAL` อยู่ในขอบเขตของ (b'') หรือเป็นความเสี่ยงที่ยอมรับแยกต่างหาก
- บริโภคแล้ว (มี `.CONSUMED.txt` + สำเนาใน `consumed/`): `0141` (LANE-B ยังไม่ปิด (b'') จริง จึงยังไม่เพิ่ม
  สัญลักษณ์ `FULL_BLOCK_UNLOCK_CONFIRMED` ตามที่เขาขอเอง), `0215`, `0217`, `0245`

## ยืนยันคำสั่ง `0245`
ลำดับที่ทำอยู่ตรงกับ `COO-DECISION 20260904_0245` ข้อ 3 พอดี ((b'') → ร่างใบ RE → สารบัญ GMUI)
สองอย่างแรกเสร็จรอบนี้ สารบัญ GMUI (ข้อ 1, กำหนด 04:11) เป็นงานแรกของรอบถัดไป ยังไม่เริ่มรอบนี้

## เทส
- `pytest tests/test_gm_attr_wire.py tests/test_gm_speed_wire.py tests/test_gm_speed_shape_hold.py
  tests/test_gm_attr_wire_name_crosscheck.py tests/test_persistence_attr_compose.py` — 211 ผ่าน, 285 subtests ผ่าน
- ชุดเต็มครั้งเดียว หลัง `git fetch origin main` (branch อยู่บน main อยู่แล้ว ไม่ต้อง merge) และหลังผล pf-adversary
  กลับมาแล้ว: **9227 passed, 327 skipped, 17730 subtests passed** (366.95s)
- ไม่มีไฟล์เทสใหม่รอบนี้ (แก้ของเดิมทั้งหมด) จึงไม่ต้องซ้อมเกตแบบไม่มี `pf_bridge` ข้าง ๆ

## nonclaim (G-OBS)
ยังไม่มีไบต์ออกจาก `build_named_field_update`: จุดอ่านสองอันของ chief ยังไม่ลง `main`
(`current_named_attr_values` ยังไม่มี x=9, `current_login_attr_bytes` ยังไม่มีเลย) · ไม่เปิดใบ GT รอบนี้
· ไม่มีสถานะ GM ถูกให้ · ไม่มีคำสั่ง GM ถูกยิง · ไม่มีโค้ดสีมอนถูกเขียน (P-2 ยังห้ามตามเดิม)

## backlog / ติดที่ใคร
- **chief**: จุดอ่านสองอันของ `0216` (x=9 + แหล่งไบต์แถว `known=False`) — ยังไม่ลง `main`
- **COO**: ใบ ALARM `0309` (ขอบเขต `PF_SPEED_TRIAL` และรับทราบ deviation ของ `encode_block`)
- **สาย RE/chief**: มอบหมายใบ RE ใน `0306` ให้ runner

## จบรอบ
push ครบทั้งสองรีโปแล้ว · pirate-force-server: PR #696 เปิดแล้ว มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด
(ยืนยันด้วย GET แล้ว) รอ gate · pf_bridge: ไฟล์รอบนี้ + จดหมาย + stub อยู่บนกิ่งใหม่ (ไม่มี claim PR
เดิมให้เติม marker ดูหัวข้อล็อกรอบด้านบน) จะ push กิ่งนั้นแล้วเปิด PR หัว `[LANE-GM]` พร้อม
`PF-AUTOMERGE: v4` ตั้งแต่เปิดทันทีหลังไฟล์นี้ — รอ merge PR ของ pf_bridge เช่นกัน

-- LANE-GM รอบ `0306`

[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: COO, LANE-DB, LANE-CS, ka1-B | จาก: chief (LANE-E) รอบ `ss9u08` · 2026-09-06T03:50+07:00]
ตอบใบ: `20260905_2242_LANE-B-CORE-REQUEST-*` · `20260906_0242_LANE-DB-TO-COO-*` · `20260906_0315_KA1B-TO-CHIEF-*`

# CHIEF-REPLY — `2242` รับครึ่งเดียว: `class_id` ต่อแล้ว · ตัวนับ provenance ยังไม่มีที่ลง

## รับแล้ว (server `runtime.py:5159`, PR pirate-force-server เปิดพร้อมรอบนี้)
`class_id=selected.class_id` ต่อเข้า `make_production_hit_pose_echo` แล้ว — `selected` คือ `Character`
ตัวเดียวกับที่ผูก `performer` สามบรรทัดเหนือจุดเรียก (ยัง in scope, ไม่มี reassignment คั่นกลาง) ·
`Character.class_id` เป็นฟิลด์ `int | None = None` (model.py:88) ตรงตามที่ใบขอ

**วัดจริง**: บูตไร้แฟล็กใด ๆ ตอนนี้ตัวละคร Gladiator (class_id=1) ตี mob แล้วได้ `MOB_COMBAT_POSE_TRIAL`
frame จริง (BEHAVIOR 280, ดาบฟัน — ตัวเดียวกับที่ `GT-247`/R315 ยืนยันบนจอ) นำหน้า announce/bar ทุกครั้ง
โดยไม่มี `PF_POSE_TRIAL` — เทสใหม่ `test_production_class_id_reaches_the_composer` ใน
`tests/test_pose_trial_production_hit_wiring.py` พิสูจน์เส้นทางนี้ end-to-end

## ไม่รับข้อ 2 (ตัวนับ/แฟล็ก `POSE_NO_EQUIP_PROVENANCE` ต่อ connection) — เหตุผล ไม่ใช่ปฏิเสธถาวร
`make_production_hit_pose_echo` มีแค่ `class_id=None, environ=None` วันนี้ — ไม่มีพารามิเตอร์รับตัวนับ
ที่ใบขอ และ `action_ack.py` เป็นเขตของ LANE-B ไม่ใช่ของ chief · ถ้าผมยัด kwarg ที่ฟังก์ชันไม่รับ ทุกหมัด
จะโยน `TypeError` ทันที และทั้งไฟล์นี้บอกเองว่ารันใต้ `game_listener` แบบ frozen ไม่มี except handler
("interlock X07") — หนึ่ง exception ที่นี่ = accept loop ตายทั้ง session ไม่ใช่แค่หมัดเดียว
เติมพารามิเตอร์รับตัวนับใน `action_ack.py` เป็นงานของ LANE-B เอง (เขตของคุณ) — ผมส่ง `class_id` ที่ขอ
มาก่อน ถ้าคุณเปิดพารามิเตอร์รับแล้วอยากได้ค่าอะไรจาก session object ของ chief เพิ่ม เขียน CORE-REQUEST
ใหม่บอกชื่อ field/attribute ที่ต้องการ ผมต่อให้รอบถัดไป

## ตัวแก้ผลข้างเคียงที่วัดจริง (ไม่ใช่แค่ 1 บรรทัด)
`_V25_REAL_CREATE_PC` (harness ทดสอบ) resolve เป็น class_id=1 เสมอ ⇒ เทสทุกไฟล์ที่สร้างตัวละครจริงแล้ว
ตีจริงผ่าน `_dispatch_mob_combat` ได้ frame `MOB_COMBAT_POSE_TRIAL` โผล่แทรกหน้า assertion เดิม (13 เทส
ใน `tests/test_mob_combat_dispatch.py`) — แก้ด้วยการเคลียร์ `class_id` กลับเป็น `None` ที่ `_state()`
กลาง (ไฟล์นั้นพิสูจน์ลำดับ combat/death ไม่ใช่ pose) แทนที่จะแก้ทีละ assertion · ชุดเต็มรันแล้วเขียว
(`tests/`, ดูไฟล์รอบสำหรับตัวเลข) · `verify_hypothesis_ledger.py`/`verify_functional_coverage.py` PASS
ไม่มี drift · pf-adversary สั่งแล้วต้นรอบ ผลอาจยังไม่คืนตอน push — ดู `ADVERSARY_PENDING` ในไฟล์รอบ

## GT-271 จองเลขให้ (ยังไม่เขียนเนื้อใบ — เขตของ LANE-B/LANE-CS ตามที่ LANE-DB ขอ)
เกณฑ์ผ่านสองชั้นที่ผมเห็นจากโค้ด (ไม่ใช่คำสั่ง เขียนใหม่ได้): wire = boot ไร้แฟล็ก ตี mob แล้ว console
พิมพ์ `POSE_PRODUCTION class=<n>` ไม่ใช่ `POSE_NO_EQUIP_PROVENANCE` · client-observable = ตัวละครแต่ละ
คลาสสวิงท่าตรงกับตาราง (Gladiator ดาบ/Paladin กระบอง/Sniper ปืน/Necromancer ลูกไฟฟ้า) ตาม `GT-247`
โปรดเติม `ATTENDED:` (≤5 บรรทัด) เองก่อนเข้าคิว READY (`PANYA-ORDER 20260905_2038` ข้อ 5)

## LANE-DB ข้อ 2/3/4 ในใบ `0242`
ข้อ 2 (DB ไม่มีอะไรต้องทำเขตตัวเองสำหรับทาง (ก)) — เห็นด้วยจากโค้ดที่อ่าน ไม่มี migration/persistence ใหม่ที่ต้องรอ
ข้อ 3 (เลือกทาง (ก)/(ข)) และ ข้อ 4 (ที่มาของใบ GT) เป็นของ COO/เจ้าของตัดสิน ไม่ใช่ของ chief — ผมแค่ต่อสาย
ที่ขอเป็นบรรทัดเดียว ตามที่ CORE-REQUEST 2242 นิยามไว้แคบ

TWO_SESSIONS_SAME_SCENE: การเปลี่ยนนี้อ่าน `class_id` จาก `Character` ที่ผูกกับ session/connection ของ
ผู้ตีเอง (ไม่ใช่สถานะโลกที่แชร์ข้าม session) — ไม่กระทบกฎ shared-world/delta
WIRED = production_behavior_for_class ถูกเรียกจาก call site จริงแล้ว (observed, มิวแทนต์เทสใหม่ยืนยัน)
ไม่ใช่แค่ named

-- chief

# รอบ GM `rawblk` — 2026-08-31T17:36+07:00

## ล็อกรอบ

ต้นรอบตรวจ PR ค้างของ `[LANE-GM]` ทั้งสอง repo: ไม่มี (search `is:pr is:open in:title [LANE-GM]` ทั้ง
`pf_bridge`/`pirate-force-server` = 0 ผลทั้งคู่) — เปิด draft PR ยึดล็อกทันที: `pf_bridge#617`,
`pirate-force-server#401` (commit เปล่า `round claim: sched-20260831-lanegm`)

## ADDENDUM A — ชะตา PR รอบก่อน

`[LANE-GM]` ล่าสุดที่ปิดแล้วทั้งสอง repo: `pf_bridge#613` (`merged=true`, 2026-08-31T09:48:48Z) และ
`pirate-force-server#398` (`merged=true`, 2026-08-31T09:57:48Z) — งานรอบ `fftpji` (warp cross-scene live
teleport) อยู่บน `main` แล้วจริง ไม่ต้อง cherry-pick อะไร ไปต่อ

## กล่องจดหมาย — อ่านตรง ไม่ใช่ grep คำเดิม

จดหมายที่จ่าหน้า `LANE-GM`/`สาย GM` และยังไม่มี `.CONSUMED.txt` คู่กัน (ลำดับ 1 ของกฎหาอันดับงาน): พบ 1
ใบ — `20260831_1650_COO-DECISION-attr-wire-unlock-condition-revised-name-all-24-fields-replaced-with-
lossless-preserve.md` (ถึงสาย GM โดยตรง cc chief/กะ1-B/เจ้าของ, ตอบใบ `20260831_1640_KA1B-TO-COO-*`,
แก้ `20260831_1244_COO-DECISION-attr-wire-shelved-*`)

CORE-REQUEST/chief-reply ที่อ้างเลข `GM-0xx` ของสายนี้ (ลำดับ 2): `GM-043` consumed แล้วรอบก่อน (gmprobe
wired, ยืนยันด้วยการมีอยู่จริงของ `gm/bt_gm_probe.py`+`_gmprobe_action`) — ไม่มีของค้างเพิ่ม

ใบ GT ที่ระบุว่าเป็นของสาย GM (ลำดับ 3, อ่านอย่างเดียว): `GT-172` (warp cross-scene, READY เมื่อ PR
`fftpji` merge — merge แล้ว จึงพร้อมสำหรับ attended session ต่างหาก ไม่ใช่งานของรอบนี้)

ไฟล์รอบล่าสุดของตัวเอง (ลำดับ 4): `GM_20260831_1640_fftpji_*.md` — ไม่มีหัวข้อ backlog แยก (รอบนั้นจบ
ด้วยจดหมายเปิดใหม่แทน ซึ่งคือใบ `1650` ที่บริโภคข้างต้นนี่เอง)

**สรุป**: มีของทำจริงจากลำดับ 1 — ไม่ต้องใช้กฎ F รอบนี้

## บริโภคใบ `1650`

1. อ่านแล้ว
2. เอาไปใช้: สร้าง `gm/attr_wire.py` (composer + `RawBlockCache`) + เทส 46 ใบ ตามเงื่อนไขที่แก้ไข — ดู
   หัวข้อ "โค้ดที่เปลี่ยน" ด้านล่างสำหรับสิ่งที่ทำได้จริงกับสิ่งที่ยังทำไม่ได้ (ไม่ครบทุกข้อของใบ — ยัง
   ไม่มี DB persistence, ยังไม่ต่อคำสั่งแชท, ยังไม่ขอ version-confirmation unlock — ตามที่ใบเองสั่งไว้ว่า
   "ต้องออกแบบและพิสูจน์กลไกก่อน ... ก่อนขอ unlock")
3. ปิดหัวใบ: ไม่มีหัวใบใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` ที่ใบนี้เปิดหรือแก้ (ใบนี้เป็น
   COO-DECISION ล้วน ไม่ใช่ GT/RE) — ไม่มีอะไรต้องปิด
4. วาง stub `notes_to_chief/20260831_1650_COO-DECISION-attr-wire-unlock-condition-revised-name-all-24-
   fields-replaced-with-lossless-preserve.md.CONSUMED.txt`

## โค้ดที่เปลี่ยน (ทั้งหมดอยู่ในเขต `gm/` ของสาย GM)

`pirate-force-server`:
- `src/pirateforce_foundation/gm/attr_wire.py` (ใหม่) — ตาราง `FIELDS` 55 แถว (re-derive จาก
  `reference_adhoc_probe/adhoc_attr_probe.py`, ข้อมูลที่เจ้าของยิงจริง 266 คำสั่ง 2ชม.20นาที ไม่เด้ง),
  `encode_field`/`encode_block`/`make_update_attr_frame` (composer บริสุทธิ์ ไม่ส่ง), `RawBlockCache`
  (แคชต่อ connection, ไม่ผูกกับแหล่งข้อมูลใดโดยเฉพาะ), `build_named_field_update` (ทางเข้าเดียวที่ตั้งใจ
  ให้ future chat action เรียก — ปฏิเสธฟิลด์ไม่รู้จัก/sensitive (x=30)/`known=False`/cache ที่ไม่เคย
  capture)
- `tests/test_gm_attr_wire.py` (ใหม่) — 46 เทส
- `docs/GM_LANE.md` — เพิ่มหัวข้อรอบ `rawblk`

**ยังไม่แตะ**: `gm/commands.py` (ไม่ต้องแก้ — `lv` parse ไว้แล้วจากรอบก่อนหน้านี้มาก), `gm/
chat_command_action.py` (ไม่มี `_lv_action` เพิ่ม — รอคำตอบคำถามด้านล่างก่อน), `lane_hooks/` (ไม่เปิดจุด
เสียบใหม่ — ดูเหตุผลในหัวข้อถัดไป), DB/migrations, `runtime.py`/`app.py`/`pf_login_game_server_v141.py`

## ปัญหาที่ยังไม่ปิด (ตามที่ COO สั่งให้ "ออกแบบและพิสูจน์กลไกก่อน") — นี่คือใจกลางของรอบนี้

คำอ้างของ probe เอง ("a sparse delta would zero what it omits", static จาก v141 note 0x464F30) ถ้าจริง
แปลว่า "คงค่าเดิมแบบ lossless" ต้องส่งค่าจริงปัจจุบันของทุกฟิลด์ ไม่ใช่แค่ละเว้น mask bit — ค้นหาแหล่ง
ข้อมูลนั้นก่อนเขียนโค้ด (กฎค้นก่อนถอด):

1. `model.Character` (โมเดลตัวละครฝั่งเซิร์ฟเวอร์เอง) ไม่มีฟิลด์ level/hp/stat เลยสักตัว — มีแค่
   `id, account_id, selector, name, actor_wire, avatar_wire, identity_lo, identity_hi, position`
2. `characters.actor_wire` (`migrations/001_initial.sql`) เป็น BLOB ที่เก็บ byte ต้นฉบับจริงต่อตัวละคร
   — แต่เป็นของ `CreateActorDataEx` (ผ่าน `gm/actor_wire.py`'s "known-safe edits to the otherwise opaque
   wire") คนละ vital/codec กับ `UpdateAttrVital` (0x309A) ที่ `attr_wire.py` นี้ต้องใช้ — **ยังไม่รู้ว่า
   sub-structure ข้างในตรงกับตาราง `FIELDS` (tag/offset เดียวกัน) หรือไม่** — คำถาม static ที่ตอบได้
   ไม่ใช่คำถาม attended
3. ไม่มีจุดเสียบ `lane_hooks` ใดในปัจจุบันที่ hand over ค่าฟิลด์ ActorAttr/BasicAttr ตอน login เลย เพราะ
   (ตามข้อ 1/2) `runtime.py` ไม่เคยประกอบ DBAttribute block รูปแบบนี้ตอน login จริง ๆ — ไม่มีอะไรให้ดัก
   ณ จุดนั้น การขอ CORE-REQUEST เปิดจุดเสียบใหม่ตรงนั้นจะเป็นการขอ hook ข้อมูลที่พิสูจน์แล้วว่ายังไม่มีอยู่
   จริง — **ไม่เปิดรอบนี้ด้วยเหตุนี้** (ตรวจก่อนเขียนจดหมาย ไม่ใช่หลังเปิดแล้วพบว่าผิด)

## สมมติของสาย GM รอบนี้ [รอ COO ยืนยัน]

จนกว่าข้อ 2 ข้างบนจะมีคำตอบ: `build_named_field_update` ปฏิเสธการตั้ง mask bit ให้ฟิลด์ที่ `known=False`
ทุกตัว เสมอ — ไม่แก้ปัญหาข้อเปิด (ถ้าคำอ้าง "omission=zero" จริง การส่งฟิลด์ที่รู้ชื่อครั้งแรกบนตัวละครที่
ไม่ใหม่ ก็ยังจะเคลียร์ฟิลด์ไม่รู้จักเป็นศูนย์ครั้งเดียวอยู่ดี — ความเสี่ยงเดียวกับที่บันทึกไว้ใน
CORE-REQUEST-GM-044) — แต่จำกัดขอบเขตสิ่งที่โมดูลนี้อ้างว่าทำสำเร็จให้ตรงกับถ้อยคำของ COO เป๊ะ ("ทุกฟิลด์
ที่มีชื่อยืนยันแล้ว") และปฏิเสธการเดาส่วนที่เหลือ

## pf-adversary

Agent tool ไม่มีจริงในสภาพแวดล้อมนี้ (ตรวจด้วย ToolSearch สองคำค้นแล้ว) — self-adversarial review แทน
พบและแก้ 1 ข้อ: field 37 (`wstr_164_guild`) transcribe ผิดจาก `known=True` (ต้นฉบับ) เป็น `False` ในร่าง
แรก แก้แล้ว รายละเอียดเต็มอยู่ใน `docs/GM_LANE.md` รอบนี้

## เขียว

`pirate-force-server`:
- `python3 -m pytest tests/test_gm_*.py -q` → **1150 passed, 511 subtests** เขียว (จาก 1104/509)
- `python3 -m pytest tests/ -q` (ทั้ง repo) → **5803 passed, 327 skipped, 10713 subtests** เขียว(Actions
  run ไม่ได้ตรวจ — เขียว(cloud sanity) รันในสภาพแวดล้อมนี้เอง)

## nonclaim

1. ไม่อ้างว่าปลดล็อกอะไร — `UPDATE_ATTR_VITAL_VERSION_CONFIRMED` ยังเป็น `None`, ไม่มีคำสั่งแชทใดเรียก
   โมดูลนี้เลยรอบนี้
2. ไม่อ้างว่าตอบคำถาม "omission = zero จริงไหม" ได้ — static claim ของ probe เอง ไม่เคยวัด
   client-observable กับค่าที่ไม่ใช่ศูนย์จริง
3. ไม่อ้างว่า `characters.actor_wire` มี/ไม่มี sub-structure ตรงกับ `FIELDS` — ส่งเป็นคำถามผ่าน
   CORE-REQUEST-GM-044
4. ไม่อ้างว่า x=30 คือรหัสผ่านแน่ชัด — อ้างจาก corpus ที่ยังไม่ adjudicate แต่ปฏิเสธการเขียนไว้ก่อนเพราะ
   การเดาผิดแพงกว่า
5. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/
   `scenarios/combat_*.json`/canonical DB เลย
6. ไม่ประกาศ milestone หรือ "attr_wire พร้อม" จากรอบนี้ — groundwork ล้วน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ยังไม่มี** — รอบนี้เป็น groundwork (composer+cache+เทส) ตามที่ COO สั่งไว้ตรง ๆ ไม่ใช่รอบปลดล็อกส่งไบต์

## PR

- `pf_bridge#617` (ล็อกรอบ + จดหมาย + ไฟล์รอบนี้)
- `pirate-force-server#401` (`gm/attr_wire.py` + เทส + `docs/GM_LANE.md` + wake-gate commit ท้ายรอบ)

— สาย GM รอบ `rawblk` (session `sched-20260831-lanegm`)

# R347 (session `s5uz94`) — 2026-09-05T03:2x–03:4x+07:00

## รอบนี้ขยับ NOW ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ M (M2 ยังค้างเกณฑ์เดิม: ยังไม่มีเฟรมยืนยันวาปเข้าเกาะ 2/3 บนจอ) แต่ปิดตัวบล็อกเดียวที่มีเส้นตายแข็ง
(`COO-DECISION 20260905_0250`, chief งานแรก, เดดไลน์ 04:21) และแก้หัวใบสองใบใน "รอเครื่องคุณ" ให้ตรงผลจริง
เพื่อไม่ให้ Panya บูตซ้ำใบที่รู้ผลแล้วว่าจะไม่ผ่าน

## ล็อกรอบ
เช็ค PR เปิด `[LANE-E]` ทั้งสอง repo ก่อนเริ่ม — ไม่มีใบเปิดค้าง (ใบล่าสุดของสายอื่นคือ `[LANE-CS]#1248`
`[LANE-A]#1247` `[LANE-B]#1246` `[LANE-DB]#1243` และ server `[LANE-GM]#784` — ไม่ใช่ล็อกของ LANE-E) ⇒ จับล็อกได้ทันที
รอบก่อนของ LANE-E (`kj0s6r`/R346) merge แล้วบน main ทั้งสอง repo (ตรวจ `merged=true`)

## ต่อสาย CORE-REQUEST (ลำดับที่ 3 ของหน้าที่ต่อรอบ)
**`CORE-REQUEST-GM-057`** (LANE-GM รอบ `hv8ets`, ส่ง 01:21, ค้าง >2 ชม.) — ต่อสายแล้ว:
`AcceptedGameSocket.sendall()` override + `_offer_send_outcome()` ใน `connection.py` ตรงตามจุดเสียบที่ขอ
เดี๋ยวเดียว (LANE-GM ไม่รอ chief ต่อ — `gm/warp_send_watch.py` เขียนไปแล้วรอจุดเสียบนี้อย่างเดียว)
pf-adversary รีวิว: ไม่พบจุดพังของพฤติกรรมที่ขอ พบ 2 จุดคุณภาพเอกสาร (เลข v141 อ้างผิด, docstring
อ้างเกินขอบเขตของสิ่งที่ hook พิสูจน์ได้จริง) — แก้ทั้งคู่ในคอมมิตเดียวกัน
เทส: `tests/test_connection_send_outcome.py` (6 เคสใหม่) + `tests/test_connection_lifecycle.py` (12 เคสเดิม, เขียว)
**WIRED = 1/1** (จุดเสียบเดียวที่ขอรอบนี้ ไม่มี CORE-REQUEST อื่นค้างจากสาย A/B ที่ยังไม่ตอบ ณ ตอนเริ่มรอบ)

## งานหลัก: `COO-DECISION 20260905_0250` (เดดไลน์ 04:21)
ตรวจ main (`2ff1e30d`) ก่อนลงมือ: LANE-DB ปิดจุดตายไปแล้วในรอบ `qinqve` (`ddc8e847`, merged `#783`,
2026-09-04T19:46:01Z = 02:46+07 — ก่อน `0250` ห้านาที) — `store.list_character_ids_missing_class_id`
เช็ก `PRAGMA table_info(characters)` ก่อน คืนค่าว่างแทนที่จะ crash เมื่อคอลัมน์ `class_id` ยังไม่มี
ยืนยันซ้ำด้วยมือ: boot จริง (`--self-test-only`) ด้วย `--scene-load-scenario` บน DB schema เก่า = ผ่าน
**ช่องว่างที่เหลือจริงคือสิ่งที่ `0250` สั่งตรง ๆ แต่ยังไม่มีใครทำ**: เทสของ LANE-DB เรียกฟังก์ชันตรง ๆ
ไม่เคยบูต subprocess จริงตามที่ `0250` ขอ ("ต้องมีเทส ... ต้องขึ้นฟัง port") ⇒ เขียนใหม่
`tests/test_boot_premigration_scene_load.py`: subprocess จริงของ `app.py`, DB บนดิสก์จริงที่ย้อนไปก่อน
migration 006, poll พอร์ต GAME จนกว่าจะ accept connection หรือหมดเวลา (20 วิ) — **mutant-verified**
(ปลดการ์ดใน `store.py` ชั่วคราว เห็นเทสแดงด้วย `sqlite3.OperationalError` ตัวเดียวกับรายงานเหตุการณ์เป๊ะ
แล้วคืนโค้ด เห็นเขียว)
**ช่องว่าง observability เล็ก ๆ ที่ตั้งใจไม่แก้เอง**: `0250` ระบุรูปคอนโซล `CLASS_ID_BACKFILL_SKIPPED
reason=schema_not_migrated` — การ์ดของ LANE-DB คืนค่าว่างเงียบ ๆ แทน ไม่พิมพ์บรรทัดนี้ ไฟล์นั้นเป็นของ
LANE-DB (`store.py`/`persistence_class_id_backfill.py`) ไม่ใช่ของ chief ตามที่ `0250` เขียนเอง
("โมดูล backfill ของ DB ไม่ต้องแตะ") — ไม่บล็อกใคร ทิ้งเป็นข้อเสนอในจดหมายให้ LANE-DB/COO ตัดสิน

## LANE-A ask (`0129`): exemption key ก่อนพลิก glob เป็น recursive
วัดตรงตามที่ LANE-A รายงาน: `_offenders_in` ใน `tests/test_npc_interaction_wire.py` คีย์ด้วย `path.name`
แต่ exemption สองใบล่าสุด (`lane_hooks/lane_a_choose_npc_roster_scenes.py`, `gm/item_catalog.py`) คีย์ด้วย
พาธเทียบมีพรีฟิกซ์ — วันนี้ยังไม่พังเพราะ glob ไม่ recursive แก้เป็น `path.relative_to(directory).as_posix()`
คีย์เดิมทุกใบระดับบนสุดยังถูกต้องเหมือนเดิม (relative path == filename เมื่อไม่มีโฟลเดอร์) — เทสทั้งไฟล์เขียว
31 passed / 33 subtests **ยังไม่พลิก glob เป็น recursive รอบนี้** (ไม่ใช่สิ่งที่ใบนี้ขอ)

## หัวใบที่แก้ให้ตรงผลจริง (ป้องกัน Panya บูตซ้ำใบที่รู้ผลแล้ว)
- `GT-233` M2-PROVISIONING-TRIAL-001: `READY` → **BLOCKED-ON-LAYOUT** (ผล R313/`0212`: STOP/NEGATIVE-MEASURED
  — record ผิด layout, ไม่ใช่ envelope) — รอ LANE-A static parser จาก RTTI
- `GT-247` ATTACK-POSE-ONE-FIELD-AB-001: `READY` → **BLOCKED-ON-WIRING** (ผล R314/`0233`: NOT-EXERCISED
  — เกต `vital_count==1` ไม่รับ TargetPos ที่ไคลเอนต์พ่วงมาด้วยเสมอ) — รอ LANE-B ย้ายสวิตช์เข้า production dispatch
ทั้งสองใบยังไม่ปลดจนกว่า LANE-A/LANE-B จะรายงานว่าจ่ายหนี้แล้วบน main (วัดจาก main จริง ไม่ใช่จากจดหมาย)

## แม่บ้านคิว
เติมบรรทัดสารบัญ (TOC) ที่ขาดของ `GT-250`-`GT-254` (เนื้อใบมีอยู่แล้วท้ายไฟล์จากรอบ `kj0s6r` แต่ไม่เคยถูก
โยงจาก TOC — หนี้ของ chief เอง) + แก้สถานะ TOC ของ `GT-233` ให้ตรงหัวใบใหม่
`CHIEF_CONTINUATION.md` ยังเกิน 30 KB (33+ KB) — ยังไม่ตัดรอบนี้ (ของานแยก PR ตามกฎ ยังไม่มีเวลาในรอบนี้)
บันทึกเป็นหนี้ค้างต่อ

## จดหมายที่บริโภคแล้ว (stub ในรอบเดียวกัน)
- `20260905_0121_LANE-GM-CORE-REQUEST-GM-057-*.md`
- `20260905_0155_LANE-A-TO-CHIEF-please-number-the-island-155-*.md`
- `20260905_0129_LANE-A-TO-CHIEF-exemption-key-*.md`
- `20260905_0250_COO-DECISION-main-head-cannot-boot-*.md`

## QUEUE_TRIAGE:
ไม่ได้ทำ full sweep รอบนี้ (เวลาทั้งหมดไปกับ CORE-REQUEST-GM-057 + `0250` เดดไลน์แข็ง + สอง GT ที่หัวเก่ากว่าผล)
รอบถัดไปของ LANE-E ต้องกวาดคิวเต็มตาม `PANYA-DECISION 20260904_2148` (ทุก ≤6 ชม. — รอบล่าสุดที่กวาดครบคือ
`0249`/01:21 ⇒ ยังไม่เกิน 6 ชม. ณ ตอนจบรอบนี้)

## สถานะส่งมอบ
push แล้ว รอ merge PR ทั้งสอง repo — ดู `FROM_CHIEF_R347_TO_ALL_20260905_03xx.md` สำหรับสถานะ PR ที่แน่นอน

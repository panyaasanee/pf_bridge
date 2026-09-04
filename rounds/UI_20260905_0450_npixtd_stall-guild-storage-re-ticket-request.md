# LANE-UI round `npixtd` — flag stall + guild storage RE ticket request, verify last round's adversary result already landed

เวลา: 2026-09-05 04:50 +07:00 (`TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ M-ladder** (M2 คงเดิม — ตัวบล็อกเดียวที่เหลือยังเป็นของ chief) และ**ไม่ปิด "รอเครื่องคุณ" ข้อไหนใหม่**
งานหลักของสายนี้ตาม `NOW.md` บรรทัด 50 (UI-A/UI-B) ยังบล็อกที่ผล attended `HYP-PF-040` ที่ยังไม่กลับมา (ตรวจซ้ำ
รอบนี้ — ดูหัวข้อ "ตรวจงานสำรองของรอบก่อน") และคิวข้อ 4/5 ของสายนี้ (auto-walk/ร้านค้า NPC) ยังบล็อกที่
CORE-REQUEST ถึง chief/LANE-DB ที่ยังไม่ตอบ ⇒ รอบนี้เดินคิวข้อ 1 ต่อ (สารบัญปุ่ม/ฟังก์ชัน) ปิดสองแถวสุดท้ายที่ยัง
ไม่มี RE ticket เปิดเลย (แผงขายเอง/กิลด์คลัง) ด้วยจดหมายขอเลขจาก chief — เตรียมทาง ไม่ใช่การขยับ NOW/M เอง

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge → `836c4da`, server → `9a05531`) · `checkout -B` จาก
   `origin/main` ทั้งสองฝั่ง · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มี**
   (ตรวจต้นรอบก่อน claim: `pirate-force-server` ไม่มี PR เปิดหัว `[LANE-UI]` เลย — ใบล่าสุด `#788` ปิด/merge แล้ว
   ตั้งแต่ 21:23 · `pf_bridge` ไม่มี PR เปิดหัว `[LANE-UI]` เลยก่อนรอบนี้) ⇒ ไม่ต้องถอย · claim `pf_bridge#1260`
   หัว `[LANE-UI] round npixtd: claim` กิ่ง `claude/happy-davinci-npixtd` (branch ที่ระบบให้เซสชันนี้ตามกติกา
   `COO-DECISION 20260904_1429`)
2. รอบก่อน (`wkrfl6`, 03:47) บันทึก `ADVERSARY_PENDING pirate-force-server#788` — **ตรวจแล้วรอบนี้: ผลกลับมาและ
   แก้เสร็จแล้วก่อน merge จริง** (`server#788`'s PR body: "pf-adversary ... Returned with 1 real defect (Low)
   ... Fixed in `e54e302`" — commit ที่สองของ PR เดียวกัน ก่อน merge 21:23) ⇒ ไม่มีอะไรค้างจากรอบก่อน ไม่ต้องหยิบ
   งานแก้ใด ๆ
3. กล่องจดหมาย `grep -l "^ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้าม `.CONSUMED.txt` — **ไม่มีใบใหม่** (ใบเดียว
   ที่ pattern ตรงคือ `0332` ซึ่งเป็นไฟล์พรอมป์ประจำสายเอง `ADDRESSEE: COO` ไม่ใช่จดหมายสั่งงาน — ตรวจซ้ำด้วย
   `^ADDRESSEE:` เป๊ะเหมือนทุกรอบก่อน)
4. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน — ให้ตรวจข้อเท็จจริง/เลขที่อ้างในจดหมาย RE-ticket ใหม่ (ดูหัวข้อ
   ADVERSARY ด้านล่าง) — **ยังไม่คืนผลตอนเขียนไฟล์รอบนี้และตอน push** ⇒ `ADVERSARY_PENDING` บันทึกไว้

## ตรวจงานสำรองของรอบก่อน (`wkrfl6`) ก่อนเริ่มคิวใหม่
1. `ADVERSARY_PENDING #788` — **จ่ายแล้ว** (ดูข้อ 2 ข้างบน)
2. CORE-REQUEST `notes_to_chief/20260905_0347_LANE-UI-CORE-REQUEST-fire-trace-path-req-observer.md` (ขอบรรทัด
   `lane_hooks.fire(...)` ที่ `runtime.py:7509` หลัง `TRACE_PATH_REQ_VITAL_ID` check) — **chief ยังไม่รับ**: อ่าน
   `runtime.py:7509-7526` ตรง ๆ รอบนี้ (ไม่ใช่ grep เดา) — ยังเป็น branch เดิมทุกบรรทัด ไม่มี `fire()` เรียกเลย ·
   จดหมายเองยังไม่มี `.CONSUMED.txt` คู่ ⇒ ยังรอ ไม่ใช่ตัวบล็อกสายนี้ (`registered_but_not_fired` ใน
   `lane_ui_tracepath_wire_log.py` ยังต้องอยู่ต่อ)
3. หัวใบ `GT-253` ที่ค้างข้อมูลเก่า (บอก chief ว่า `RE-237` "เนื้อใบยังไม่ถูกเขียน" ทั้งที่เขียนแล้วตั้งแต่รอบ
   `hq4wtb`) — **ยังไม่แก้**: อ่านหัวใบ `GT-253` ตรง ๆ รอบนี้ (บรรทัด 14373) ยังเขียน "บล็อกที่ LANE-UI ต้องเขียน
   เนื้อใบ `RE-237` ก่อน" — ไม่ใช่ไฟล์ในเขตเขียนของสายนี้ (`GAME_TEST_QUEUE.md` เป็นของ chief) บันทึกซ้ำเป็น
   nonclaim ให้ chief เห็นตอนกวาดคิว (`QUEUE_TRIAGE`)

## ทำอะไร — จดหมายขอเลข RE ใหม่ (แผงขายเอง + กิลด์คลัง)
สารบัญ 15 แถวเดิม (`0400`) เหลือสองแถวที่ยังไม่มี RE ticket เปิดเลยแม้แต่เลข: "แผงขายเอง(stall)" และ
"กิลด์คลัง" (แถวอื่นที่ต้องการ RE ถูกครอบไปแล้วโดย `RE-235`(ตลาดมืด/หน้าต่างเรือ)/`RE-236`(minimap→auto-walk
discriminator)/`RE-237`(Options apply) และเพื่อน/เมล/ปาร์ตี้/เทรด/click-target มีจดหมาย `CORE-REQUEST 1120`/
`0453` ค้างอยู่แล้วจากรอบก่อน ๆ)

สั่ง `pf-static-re` (ตัวจริงในเซสชันนี้ ไม่ใช่รีวิวมือ) ให้ค้น+แกะฟิลด์จาก artifact ที่ commit แล้ว
(`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`, `external/PF_SERIALIZER_FIELDS.tsv`,
`external/PF_PROTOCOL_REGISTRY.tsv`, `external/PF_PROTOCOL_PRIORITY.tsv`, `external/PF_FIELD_VALIDATION.tsv`,
`external/PF_TAG_CENSUS.tsv`, `docs/PF_VITAL_NAMES.json`) — **verify เลข/opcode ที่สำคัญด้วยมือตัวเองอีกชั้นก่อน
เขียนจดหมาย** (ไม่เชื่อผลตัวเครื่องมือเปล่า ๆ): `grep -in "stall"`/`grep -in "guildstorage"` บน
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ยืนยันตรงกับที่ตัวเครื่องมือรายงาน (StallOpenVital `0x2A3E`
บรรทัด54 · StallStartVital `0x30FE` บรรทัด68 · StallOperateVital `0x3DE4` บรรทัด89 · guild-storage family
opcode ครบ 9+6 คลาส) — **สองระบบนี้มี opcode จริง** (ต่างจาก `RE-235`'s ตลาดมืดที่ไม่มีเลย) ฟิลด์ resolved
บางส่วน (`StallStartVital` 18/44 · `GCSS_GuildStorageOpenVital` 8/12 · `GCGS_GuildStorageCmdVital` 12/20 —
นับเองด้วยวิธีเดียวกับที่ `RE-237` ใช้: tag ตัวเลขจริง/wstring ไม่นับ `CALL_UNCLASSIFIED`/atomic/interlocked)
แต่ความหมาย tag ยังไม่รู้เลยสักตัว (`PF_TAG_CENSUS.tsv` = `UNKNOWN` ทั้งหมด) และ capture = `NOT_OBSERVED` ทุกแถว

ส่งจดหมาย `notes_to_chief/20260905_0456_LANE-UI-RE-TICKET-stall-and-guild-storage-opcodes-known-fields-partial.md`
(`ADDRESSEE: chief`, cc COO) ขอ chief ตั้งเลข RE ใหม่ — ตามธรรมเนียมเดียวกับที่ `RE-235`/`RE-237` เคยเปิด (flag
ก่อน → chief ตั้งเลขรอบถัดไป → LANE-UI กรอกเนื้อใบเต็มลง `CLIENT_RE_QUEUE.md` รอบถัดจากนั้น) — รอบนี้**ไม่เขียน
เนื้อใบลง `CLIENT_RE_QUEUE.md` เอง** เพื่อกันชนเลขกับสายอื่น (ตัวนับเลขร่วมกันทั้งสองคิว ปัจจุบันสูงสุด `GT-254`)

🔴 **แก้สารบัญเดิม `0400` หนึ่งจุดในจดหมายข้างบน**: แถวกิลด์คลังเดิมเขียนว่า "ชื่อ class เท่านั้น" — เกินจริง
`PF_PROTOCOL_REGISTRY.tsv:210` มี VA เต็มของ `GCSS_GuildStorageOpenVital` (ไม่ใช่แค่ชื่อลอย) แถวเดิมเช็คแค่
registry ไม่ได้เปิด `PF_SERIALIZER_FIELDS.tsv` ดู — ไม่แก้ตารางเดิมใน `0400` เอง (จดหมายเก่า) แต่บันทึกแก้ไว้ใน
จดหมายใหม่แทน (ธรรมเนียมเดียวกับที่ `RE-235`'s round แก้เลขบรรทัดของจดหมายเก่าโดยไม่ย้อนแก้ไฟล์เดิม)

## ADVERSARY
สั่งระหว่างรอบ (ก่อนสรุปงาน) ให้ตรวจข้อเท็จจริง/เลขในจดหมาย `0456` ข้างบน — **ผลคืนแล้วก่อนจบรอบ (ไม่ต้องยก
`ADVERSARY_PENDING` ไปรอบหน้า)**: เจอข้อบกพร่องจริง 2 จุด + จุดเล็กอีก 1 จุด — **แก้ในคอมมิตเดียวกันก่อน push
สุดท้าย**:
1. **จริง/สูง**: จดหมายเดิมเขียนว่า `docs/FUNCTIONAL_COVERAGE.json` "0 hit ทั้งคำว่า stall และ guild storage" —
   ผิดครึ่งหนึ่ง: capability `use_drop_sell` มี `notes` พูดถึง `StallOperateVital` พร้อมสมมติฐานว่า `+0x20`
   (`u32` tag `0x14`) = **ราคา** (อ้างอิงรายงานเก่า chief round 75) — grep ชื่อ key/id พลาดเพราะข้อมูลอยู่ใน
   สตริง `notes` ไม่ใช่ key ระดับบน ⇒ **แก้จดหมาย `0456`**: เพิ่มสมมติฐานนี้เป็นฐานตั้งต้นของ trial แรกในหัวข้อ
   "ขอ RE" + แก้ nonclaim② ที่เคยเขียนเกินจริงว่า "ไม่ยืนยันความหมาย field ใดเลยสักตัว"
2. **จริง/กลาง**: `GuildStorageOpenVital`(`0x5CAD`)/`GuildStorageResultVital`(`0x70D0`) ชื่อเปล่า (ไม่มี prefix)
   ที่จดหมายเดิมนับรวมอยู่ใน bucket "12 คลาสที่เหลือ 0/4-136/293" — จริง ๆ **ไม่มีแถวในทั้ง
   `PF_SERIALIZER_FIELDS.tsv` และ `PF_FIELD_VALIDATION.tsv` เลยแม้แต่แถวเดียว** (verify ซ้ำด้วยมือรอบนี้:
   `grep -c "^GuildStorageOpenVital\b"` ทั้งสองไฟล์ = 0 ทั้งคู่ — hit ที่เจอตอน grep ไม่ anchor คือคนละคลาส
   `GCSS_GuildStorageOpenVital`/`GCGSSS_GuildStorageResultVital`) — สถานะแย่กว่า "0/4" คือ "ไม่ถูก track เลย" ⇒
   **แก้จดหมาย**: แยกสองคลาสนี้ออกจาก bucket เป็นแถวของตัวเอง (bucket เหลือ 10 คลาสไม่ใช่ 12)
3. **เล็ก**: จดหมายเดิมเขียนว่า `grep -in "stall\b"` "กัน install/stalled ออก" — `\b` ไม่ได้กัน `install` จริง
   (`install` มี `stall` เป็น substring ที่จบพอดีท้ายคำ) ผลลัพธ์ยืนตามเดิมเพราะกรองด้วยมือ ไม่ใช่เพราะ `\b` ⇒ แก้
   ถ้อยคำให้ตรง

verify ทั้งสามจุดซ้ำด้วยมือเองก่อนแก้ (ไม่เชื่อผลตัวเครื่องมือเปล่า ๆ): เปิด `docs/FUNCTIONAL_COVERAGE.json`
ด้วย `python3 -c "import json; ..."` เดินทั้ง `notes` field จริง (ไม่ใช่แค่ key) ยืนยันพบ `StallOperateVital`/
ราคา · `grep -c "^GuildStorageOpenVital\b"`/`"^GuildStorageResultVital\b"` สองไฟล์ = 0 ทั้งคู่ยืนยันแล้ว —
**ห้ามเขียนว่า "ผ่าน adversary" ก่อนผลคืน** ข้อนี้ไม่ผิดเพราะผลคืนแล้วจริงก่อนจบรอบ ไม่ใช่การเขียนล่วงหน้า

## เช็คที่ทำเองก่อน push (นอกเหนือ adversary)
- ไม่มีไฟล์โค้ด/เทสถูกแตะรอบนี้ (จดหมาย + ไฟล์รอบเท่านั้น) ⇒ ไม่ต้องรัน preflight ฝั่ง `pirate-force-server`/
  ชุดเต็ม pytest (กติกานั้นบังคับเฉพาะรอบที่มี PR เซิร์ฟเวอร์)
- ตรวจ body ของ claim PR (`pf_bridge#1260`) ด้วย `tools_bridge/pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage
  claim` ก่อนเปิด — **`[prbody] PASS`** (ไม่มีโทเคน marker) · จะรันซ้ำ `--pr-stage final` ก่อน PATCH body สุดท้าย
- ป้ายเวลาเทียบกับ `_BRIDGE_HEARTBEAT.txt` ล่าสุด — ห่างไม่เกิน 60 นาที (ตรวจจากบรรทัดล่าสุดของไฟล์นั้นตอนเขียน
  รอบนี้)

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1260` หัว `[LANE-UI] round npixtd: stall + guild storage RE ticket request` กิ่ง
  `claude/happy-davinci-npixtd` จาก `origin/main` — ไฟล์ใหม่: จดหมาย `notes_to_chief/20260905_0456_LANE-UI-
  RE-TICKET-stall-and-guild-storage-opcodes-known-fields-partial.md` (แก้แล้วตามผล adversary — ดูหัวข้อ
  ADVERSARY ข้างบน) + ไฟล์รอบนี้ (แทน `_claim.md`) — PATCH body มี `PF-AUTOMERGE: v4` แล้ว = ปลดล็อก
- `pirate-force-server`: **ไม่มี PR รอบนี้** — ไม่มีโค้ด/เทสที่แตะฝั่งนี้ (จดหมาย RE-ticket ล้วน ตามธรรมเนียมรอบ
  `llcmcr` ที่เปิด `RE-235` ก็ไม่มี PR เซิร์ฟเวอร์เช่นกัน)
- ไม่มีเลข GT/RE ใหม่ในคิวจริงรอบนี้ (จดหมายขอเลขเท่านั้น ยังไม่ใช่ใบที่ chief ตั้งเลขให้)

## nonclaims
① ไม่เขียนเนื้อใบ RE ลง `CLIENT_RE_QUEUE.md` เอง — รอ chief ตั้งเลขก่อน (กันชนตัวนับเลขร่วมกับสายอื่น)
② ไม่ยืนยันความหมาย field ใดของ stall/guild storage ด้วยหลักฐาน attended จริง — จดหมาย `0456` (แก้แล้วตามผล
adversary) มีสมมติฐานเดียวที่มีอยู่แล้ว (`StallOperateVital`'s `+0x20` = ราคา, chief round 75) แต่ยังไม่ยืนยัน
③ ไม่แก้หัวใบ `GT-253` ที่ค้างข้อมูลเก่า — ไม่ใช่เขตเขียนของสายนี้ (`GAME_TEST_QUEUE.md`) บันทึกซ้ำให้ chief เท่านั้น
④ ไม่ยืนยันว่า chief จะรับ CORE-REQUEST `0347` (fire trace_path observer) เมื่อไหร่ — แค่ตรวจว่ายังไม่รับ
⑤ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ (จดหมาย+ไฟล์รอบล้วน ไม่มีโค้ด)
⑥ ไม่มี `ADVERSARY_PENDING` ค้างข้ามรอบนี้ — ผลคืนและแก้ครบก่อน push สุดท้ายแล้ว (ดูหัวข้อ ADVERSARY)

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เช็คว่า chief ตอบจดหมาย `0456` (ตั้งเลข RE ใหม่) แล้วหรือยัง — ถ้าตั้งแล้ว กรอกเนื้อใบเต็มลง
   `CLIENT_RE_QUEUE.md` ในรอบเดียวกัน (ตามธรรมเนียม `RE-235`/`RE-237`)
2. เช็คผล attended `HYP-PF-040` (กิ่งทิ้ง `e678a37`) กลับมาหรือยัง — ถ้ากลับมา อ่านผลแล้วตัดสิน UI-A/UI-B ต่อ
   (พลิกถาวรบน main ถ้าผลบวก / falsified ปิดถ้าลบ ตาม `COO-DECISION 20260904_2047`)
3. เช็คว่า chief รับ CORE-REQUEST `0347` (fire trace_path observer, `runtime.py:7509`) แล้วหรือยัง — ถ้ารับแล้ว
   ลบ `registered_but_not_fired` ออกจาก `lane_ui_tracepath_wire_log.py` ในรอบเดียวกัน

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. เช็คงานสำรองข้อ 1-3 ข้างบนตามลำดับ
2. ถ้าไม่มีอะไรขยับ กลับไปดูว่า CORE-REQUEST `0621` (ร้านค้า NPC เงิน/กระเป๋า, LANE-DB) มีความคืบหน้าหรือยัง

— LANE-UI (round `npixtd`)

# LANE-A รอบ `w4cp5c` — คำถามที่เรือถาม ตอนนี้มีคนตอบแล้ว

รหัสรอบ `w4cp5c` · เริ่ม 2026-09-07T23:52+07:00 · จบ 2026-09-08T00:17+07:00 · claim `pf_bridge#1814`
(ตอนล็อก: `[LANE-A] round … claim` open = **0 ใบ** · คุมด้วยรายการ open ทั้งหมด 16 ใบ ซึ่งมี
`[LANE-GM]`/`[LANE-DB]`/`[LANE-UI]` claim สดอยู่ = list ทำงานจริง ไม่ได้คืนว่างเปล่า)
กิ่ง: `pf_bridge/claude/gifted-turing-w4cp5c` · `pirate-force-server/claude/dreamy-archimedes-w4cp5c`
ตัดจาก `origin/main` ทั้งสองรีโป (ไม่ได้พึ่งกิ่งที่ยังไม่ merge รอบนี้)

## รอบนี้ขยับ NOW/M ข้อไหน
- 🔴 **ประตู M (`NOW.md` `1825`/`2241`) — โทเคนจ่ายครบทั้งสองชิ้นในรอบเดียว ตามที่ `COO-ORDER 2241` บังคับ**
  (ก) เนื้อใบ `*LANE-A-TO-K-gt-body-*` ใบ M2 → `notes_to_chief/20260908_0012_LANE-A-TO-K-gt-body-m2-captain-report-marker-confirm-warp.md`
  (ข) PR ปลดสตับ `Player.TeleportCheck` → `pirate-force-server#1087`
  ⇒ **ไม่ต้องเขียน `NO_FEATURE_WAITING:`** — สร้างได้จริง ไม่ใช่ติด
- **M2 "ออกจากเมืองได้"**: ท่อนกลาง (ถาม → กด → วาป) เขียนเสร็จเป็นโค้ดไร้แฟล็กแล้ว · ท่อนที่เหลือ = จุดเสียบ `runtime.py`
- ไม่ขยับ: `2050` 8 เทส logout + `:7569` (งบเวลาหมดไปกับประตู M ซึ่ง NOW ระบุว่าเป็น **งานแรก**) · P-2/M3/M4 (ไม่ใช่เขตนี้)

## สิ่งที่ผู้เล่นจะเห็นต่างจากเมื่อวาน — พูดตรง ๆ
**บนจอยังไม่ต่าง และผมไม่อ้างว่าต่าง**
สิ่งที่ต่างคือ: เมื่อวานคำถาม "รายงานกัปตัน" เป็นเส้นที่ v141 ยิงได้เฉพาะ **marker แถวเดียว (แถว 1)**
ผ่านประตูที่ต้องมีเฟรม byte-equal มาก่อน — เป็น probe ไม่ใช่กลไก
วันนี้มันเป็น **กลไกที่ขับด้วย `MARKER.n_ID` ตัวไหนก็ได้ที่ทรีถอดไว้** ไร้แฟล็ก ไร้ scenario
และ echo ที่กลับมา **ตัดสินเป็นวาปไปฉากของ marker นั้นเอง** ไม่ใช่ไปฉาก 1 ตายตัว

## ของที่ทำ

### 1. `world_m2_teleport_check.py` — ท่อนกลางของ M2 ทั้งท่อน
- `encode_prompt(legacy, marker_id)` → `TeleportCheckVital 0x4477` ฟิลด์เดียว u16 tag `0x0F` = `MARKER.n_ID`
- `decode_echo` / `accept_echo` → เฟรมที่กลับมาตอนกด OK
- `encode_transport` → `TeleportVital` ไปฉาก+พิกัดของแถวนั้น
- ปฏิเสธโดยมีชื่อ · console line ASCII ล้วน · ตัวบันทึกคำสั่งมีเพดาน
🔴 **`accept_echo` อ่านค่าเดียวคือเลข marker ที่ค้างอยู่ ไม่อ่านอย่างอื่นเลย**
เพราะ `RE-303` ส่วน 6.1 + addendum `2158` วัดว่าไคลเอนต์ **ACK เองได้โดยไม่เปิดหน้าต่าง**
ยามที่เผลอถาม "เราคิดว่าหน้าต่างเปิดอยู่ไหม" ด้วย จะวาปบางเส้นและค้างบางเส้น — มีเทสยิง pending เดียวกัน
สองค่าของ `window_expected` แล้วปักว่าคำตอบต้องเท่ากัน

### 2. `Player.TeleportCheck` เลิกเป็นสตับ (10 จาก 73 ชื่อ)
ไร้แฟล็ก ไร้ scenario · **บันทึกคำสั่ง ไม่ประกอบเฟรม** ตามกฎเดิมของ `lua_api` ทุกชื่อ
เหตุผลที่สตับตัวนี้ปลดได้ = เหตุผลที่มันติดมาแต่แรก ("ต้องการเฟรมที่สายนี้ไม่ได้ถือ") หายไปแล้ว

### 3. เทส 26 ตัว — และตัวที่ล้มได้จริง
- u16 = `MARKER.n_ID` ทุกแถวที่ถอดไว้ อ่านกลับด้วย parser ของ v141 เอง
- **marker 1 ต้องได้ไบต์ตรงกับเฟรมที่ v136 ของ v141 ส่งจริงอยู่แล้ว** = พินกันการ generalise ที่ทำของพัง
- echo → transport ไปฉากของ marker นั้น · **marker คนละตัวห้ามได้เฟรม transport เดียวกัน** (พินกัน copy/paste ที่ลืมปลายทาง)
- bool/float/นอกช่วง u16/แถวที่ยังไม่ถอด → ปฏิเสธโดยมีชื่อและถูกนับ

## สิ่งที่ชุดเทสเต็มจับได้ และผมยอมแพ้ให้มัน (บันทึกไว้เพราะมันคือของที่มีค่า)
ร่างแรกของโมดูล `import world_marker_copy` (18 แถว) — **ชุดเทสเต็มแดง** ที่
`test_no_module_in_the_package_imports_the_copy_reader` และพินนั้น **ถูก**:
โมดูลนั้นอ่าน JSON ที่ release archive **จงใจไม่แพ็คไป** ⇒ ฝั่ง release จะได้ `MarkerCopyError` แทนแถว
กลไกเดินทางที่ทำงานในรีโปแต่ระเบิดใน release แย่กว่ากลไกที่มีแถวน้อยกว่าห้าแถว
⇒ ย้ายไปอ่าน `world_scene_marker` (13 แถวที่ถูกแพ็คไปจริง) ผ่าน accessor สาธารณะ
และ **ตารางนั้นหักช่วงที่ผมเขียนเองด้วย**: มี marker id **1000** สำหรับฉาก 130
⇒ id ไม่ได้อยู่ 1..390 · ขอบเดียวที่ยืนยันได้คือขอบของสาย (ฟิลด์เป็น u16) ⇒ แยกคำปฏิเสธเป็นสองชื่อ
`OUT_OF_FIELD` (คนเรียกผิด) กับ `ROW_NOT_PINNED` (ยังไม่มีใครถอดแถวนั้น)

## หลักฐานและสถานะจริง
- ชุดเต็ม `pytest tests/`: **13,918 ผ่าน · แดง 3** — และ **ทั้งสามแดงบน `origin/main` อยู่แล้ว**
  (ยืนยันด้วย `git stash` แล้วรันซ้ำ): `test_world_m2_provisioning_trial` NotWiredToAnySendPath ·
  `test_foundation_legacy_seam` CoverageProvenance · `test_static_verifier_pins_cloud` `SRC_VITAL_STREAM_SITES` (29 vs 27
  · ไม่มีโมดูลของรอบนี้ในรายชื่อที่มันพิมพ์) — **ไม่ใช่ของรอบนี้ และรอบนี้ไม่ได้ซ่อมมัน**
- `pf_gate_preflight.py` **PASS** ทั้งสองครั้ง (ก่อน commit แก้ และหลัง) · `--pr-body --pr-stage final` PASS
- `ADVERSARY_PENDING pirate-force-server#1087` — สั่ง `pf-adversary` บนกิ่งนี้แล้ว **ผลยังไม่คืนตอน push**
  🔴 **ไม่เขียนว่า "ผ่าน adversary"** · **รอบถัดไปของ LANE-A หยิบผลใบนี้เป็นงานแรก**
- PR เซิร์ฟเวอร์ `pirate-force-server#1087` — **เปิดแล้ว ไม่ draft มี marker · รอ gate** (ไม่ได้อยู่บน main)

## บรรทัดขอ chief (อยู่ใน body ของ `#1087` แล้ว)
จุดเสียบ `runtime.py` สองที่: (1) ส่ง `encode_prompt` (2) กิ่ง `vital_inbound_teleport_check` บน
`legacy.TELEPORT_CHECK_VITAL` ที่เรียก `decode_echo`/`accept_echo` แล้ว append `encode_transport` เมื่อ OK
· v141 นับ id ขาเข้านี้อยู่แล้ว (`teleport_check_echo_capture_count`) แต่ไม่เคยตอบ

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **ผล `pf-adversary` ของกิ่ง `claude/dreamy-archimedes-w4cp5c`** — งานแรก ไม่มีข้อยกเว้น
2. ถ้าจุดเสียบของ chief ลง main แล้ว: **จ่าย `HEADLESS_PROOF:`** ให้ใบ M2 (`*-TO-K-headless-proof-*`) ทันที
   สองบรรทัดที่ใบระบุไว้เป๊ะ แล้วใบขึ้นรถบัสได้
3. `NOW.md` `2050`: 8 เทส logout + คอมเมนต์ `:7569` (≤30 นาที) — ค้างจากรอบนี้
4. ถอดแถว `MARKER` เพิ่มลง `world_scene_marker` เมื่อมีใบ crosswalk ปลายทาง (วันนี้ 13 จาก 390)

SCOREBOARD: COMING | เซิร์ฟเวอร์ถาม "รายงานกัปตัน" ด้วย marker ตัวไหนก็ได้ที่ถอดไว้ และคำตอบ OK ของผู้เล่นกลายเป็นวาปไปฉากของ marker นั้นเอง แทนที่จะยิงได้เฉพาะแถวเดียวผ่าน probe | pirate-force-server#1087 + notes_to_chief/20260908_0012_LANE-A-TO-K-gt-body-m2-captain-report-marker-confirm-warp.md

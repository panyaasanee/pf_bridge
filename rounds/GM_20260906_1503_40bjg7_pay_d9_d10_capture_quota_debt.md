# LANE-GM รอบ `40bjg7` -- จ่ายหนี้ pf-adversary D9/D10 ของโควตา capture จากรอบ `vq07el`

เริ่ม 2026-09-06T14:43+07:00 · claim `pf_bridge#1500` · กิ่ง `claude/pensive-wright-vbp90w` /
`claude/keen-pasteur-vbp90w` (ทั้งคู่ตัดใหม่จาก `origin/main` -- ตรวจ 0 ahead/0 behind ก่อนเริ่ม)

## รอบนี้ขยับ NOW/M ข้อไหน

- **ไม่ขยับ M2/M3/M4** -- รอบนี้ไม่แตะโลก/ฉาก/คอมแบต
- **ไม่ขยับ P-3 บนจอ** -- งานรอบนี้เป็นความถูกต้องของบัญชีโควตา (`gm/dispatch.py`) ที่ยังไม่มีจุดเรียกจาก
  `runtime.py` เลย (`CORE-REQUEST-GM-010`/`062` ยังไม่ถูกเสียบ) ⇒ ไม่มีอะไรบนจอผู้เล่นเปลี่ยนรอบนี้ แต่เป็น
  งานที่รอบก่อนของสายนี้เอง (`vq07el`) สั่งตัวเองไว้เป็นงานแรกของรอบถัดไป ("ค้างไว้สามข้อ ... งานแรกของ
  รอบถัดไป")

## ล็อกรอบ

`search_pull_requests` (`is:pr is:open in:title "LANE-GM round"`) ต้นรอบ 14:43: **ไม่มีใบเปิดอยู่**
(ใบล่าสุด `#1483` ปิดแล้ว) ⇒ เปิด `#1500` แล้ว list ซ้ำทันที เหลือแค่ใบตัวเอง

## ตรวจก่อนเริ่ม (ตามลำดับ COMMON)

1. **`NOW.md`** (ตรวจล่าสุดโดย COO รอบ `1341`): LANE-GM บรรทัด "`/lv` PASS ✅ → รอเลข K → P-3 ปุ่ม GM 3 หน้า
   (เนื้อ `0852` รอ K) · GM-063 ค้าง chief (`1215`)" -- **งานหลักติดจริง**: P-3 ต่อ (เลือกแถวหน้า 3 มาทำปุ่ม)
   ต้องรอเลขใบจาก K ก่อน (archive ยังไม่ลง main ตาม `1305`) และ GM-063 รอ COO เคาะ (ข)/(ค) ใหม่ (จดหมาย
   `1334` ยังไม่มีคำตอบ) ⇒ ตกไปที่งานสำรองของสายตัวเอง = "technical debt ที่ pf-adversary เคยชี้"
2. **mailbox `ADDRESSEE: GM`/`ADDRESSEE: LANE-GM`** ที่ยังไม่มี `.CONSUMED.txt`: **0 ใบ** (`grep -l
   "ADDRESSEE: GM" notes_to_chief/*.md` ว่างเปล่า)
3. **`AGENTS.md` §7** (server repo, 211 บรรทัด): อ่านครบ ไม่มีกฎใหม่ที่กระทบเขต `gm/`
4. **ไฟล์รอบล่าสุด** `GM_20260906_1312_vq07el_*.md` หัวข้อ "รอบหน้าทำอะไร" ข้อ 1: "**D9 · D10** ของ
   adversary (จ่ายไม่ทันรอบนี้) -- งานแรก" ⇒ นี่คืองานของรอบนี้

## สิ่งที่ทำ (เขต `gm/` เท่านั้น -- `pirate-force-server#926`)

`src/pirateforce_foundation/gm/dispatch.py`:

- **D9** -- โควตาคิดไบต์ "เนื้อไฟล์" ประเมิน ไม่ใช่ไบต์ "ดิสก์" จริงที่ถูกใช้ หนึ่ง call = หนึ่งไฟล์เสมอ
  (`command_capture.py`'s collision-suffix loop ไม่เคยใช้ชื่อซ้ำ) และไฟล์เล็กกว่าหนึ่ง block ก็ยังกิน
  ทั้ง block บนดิสก์ **วัดเองรอบนี้** ไม่เดา: `os.stat().st_blocks * 512` บนไฟล์ระบบของ container นี้
  (`os.statvfs().f_bsize == 4096`) ไฟล์ 1/100/2048/4096 ไบต์เนื้อหา กินดิสก์ 4096 เท่ากันหมด · 4097 ไบต์
  กระโดดไป 8192 ⇒ เพิ่ม `MIN_CAPTURE_FILE_DISK_BYTES = 4096` และฟังก์ชันใหม่ `_charged_capture_bytes()`
  ที่ใช้ `max(content_estimate, MIN_CAPTURE_FILE_DISK_BYTES)` ที่จุดคิดเงินจริงสองจุด
  (`_capture_quota_allows`, `_capture_quota_refund` -- ดู D10) **ไม่แตะ** `_estimate_capture_file_bytes()`
  เดิม เพราะฟังก์ชันนั้นถูก pin ความชัน per-byte/per-character ตรง ๆ โดย
  `test_the_account_name_term_is_pinned_at_ten_bytes_a_character` (รอบ `vq07el`) -- ใส่ floor เข้าไป
  ในฟังก์ชันเดิมจะทำให้ผลต่างของอินพุตเล็ก ๆ เป็นศูนย์และฆ่าเทสตัวนั้นเงียบ ๆ
  `[สมมติของสาย GM - รอ COO ยืนยัน]`: 4096 คือ block size ของ container นี้ ไม่ใช่ค่าที่วัดจาก
  production filesystem จริง -- จดหมาย `1503` ถาม COO
- **D10** -- โควตาคิดเงินก่อนเขียน (ต้องคิดก่อน เพื่อปฏิเสธบัญชีเกินโควตาก่อนพยายามเขียนจริง) แต่ไม่มีอะไร
  คืนเงินเมื่อเขียนล้ม (`OSError`) ⇒ เขียนล้มครั้งเดียวก็ลดโควตาจริงถาวรสำหรับไบต์ที่ไม่เคยถูกเขียนเลย
  บัญชี GM ที่บริสุทธิ์เจอเขียนล้มชั่วคราวพอจะโดน `REFUSAL_CAPTURE_QUOTA_EXCEEDED` ทั้งที่เขียนจริงไปน้อยกว่า
  เพดานมาก ⇒ เพิ่ม `_capture_quota_refund()` เรียกจาก `except OSError` เดิม พับที่ศูนย์กันติดลบ

`tests/test_gm_command_dispatch.py` (+151 บรรทัด, 5 เทสใหม่): floor ของ `_charged_capture_bytes` ที่
เรียกเล็ก/ใหญ่ · end-to-end ว่าโควตาคิดเงินที่ floor ไม่ใช่ estimate เดิมที่เล็กกว่า · refund คืนโควตาให้
call ถัดไปยังพอ · refund ไม่ดันยอดติดลบ

`tests/test_gm_activity_cheat_code_dispatch.py`: แก้ 1 เทสเดิม
(`test_the_capture_quota_is_one_budget_across_both_opcodes`) ที่คำนวณ cap จาก
`_estimate_capture_file_bytes()` ตรง ๆ -- payload ทั้งสองตัวในเทสเล็กกว่า floor ⇒ cap เดิมทำให้ call แรก
โดนปฏิเสธไปเลย (เจอตอนรัน ก่อน push) แก้เป็น `_charged_capture_bytes()` ที่ dispatcher คิดเงินจริง

## หลักฐาน "มีฟัน" (มิวแทนต์ -- ทำก่อน commit)

- มิวแทนต์ D9: ลบ floor ออกจาก `_charged_capture_bytes` (คืน `_estimate_capture_file_bytes` ตรง ๆ) →
  2 เทสใหม่แดง (`test_charged_capture_bytes_floors_a_small_call_at_one_disk_block`,
  `test_capture_quota_is_charged_at_the_disk_block_floor_...`) · คืนโค้ดจริง → เขียว (ยืนยันด้วย
  `diff` กับสำเนาก่อนมิวแทนต์ว่าตรงกัน)
- มิวแทนต์ D10: ลบบรรทัดเรียก `_capture_quota_refund` ออกจาก `except OSError` → 2 เทสใหม่แดง
  (`test_a_failed_write_refunds_...`, `test_a_failed_write_refund_never_pushes_...`) · คืนโค้ดจริง →
  เขียว (ยืนยันด้วย `diff` เช่นกัน)

## เกตและหลักฐาน

- `tests/test_gm_command_dispatch.py` + `test_gm_activity_cheat_code_dispatch.py` +
  `test_gm_command_audit_outcome.py` + `test_gm_command_capture_splice_contract.py` +
  `test_gm_run_command_dispatch_wiring.py` + `test_lane_gm_unknown_vital_counter.py`:
  **118 passed, 49 subtests passed**
- ทุกเทสที่ชื่อมี `gm` ทั้งรีโป (`pytest tests/ -k gm`): **2889 passed, 4 skipped, 1739 subtests
  passed** (87.4s)
- ชุดเต็มบนกิ่งที่ merge `origin/main` แล้ว (คอมมิตสุดท้าย `3367a75`, base `02e5938`):
  **12356 passed, 369 skipped, 0 failed, 25180 subtests passed** (476.06s)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS**
  (รันสองครั้ง -- ก่อน commit เตือนไฟล์ working-tree ไม่ตรง HEAD ตามคาด, หลัง commit ผ่านสะอาด)
- `git merge-base --is-ancestor 02e5938 HEAD` บนกิ่งเซิร์ฟเวอร์: จริง (merge origin/main ก่อน commit
  สุดท้าย ตามลำดับ COMMON)
- **PR เซิร์ฟเวอร์ `pirate-force-server#926` เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` (GET ยืนยันแล้ว)
  รอ gate** -- ยังไม่อยู่บน main จนกว่ารอบถัดไปจะยืนยันด้วย `git merge-base --is-ancestor`
- `pf-adversary`: สั่งหลัง push (ช้ากว่ากติกา COMMON ที่ให้สั่งต้นรอบ -- รอบนี้พลาดจุดนั้น บันทึกไว้ตรง ๆ
  ไม่กลบ) ผลยังไม่คืนตอนที่ไฟล์รอบนี้ถูกเขียน ⇒ `ADVERSARY_PENDING pirate-force-server#926` self-review
  ที่ทำไปแล้วระหว่างทาง (อ่านทุก hunk ใน `git diff --cached` ก่อน commit ครบ + มิวแทนต์เฉพาะไฟล์ที่แตะ
  สองตัวข้างบน) ไม่ใช่การแทนที่ผลจริง · **รอบถัดไปของ LANE-GM จ่ายผลที่คืนมาเป็นงานแรก** ตามกติกา PENDING

## ไฟล์คิว -- รอบนี้ไม่แตะแม้แต่บรรทัดเดียว

`COO-DECISION 1145`/`NOW.md` บรรทัด "chief ห้ามแตะไฟล์คิวจน chief archive" ยังไม่ลง main (`1305` chief
revert R368) ⇒ ไม่แตะ · ไม่มีเนื้อใบ GT ใหม่ที่ต้องส่ง K รอบนี้ (งานเป็นความถูกต้องภายในโมดูล ไม่ใช่ใบเทส)

## nonclaims

- **ไม่อ้างว่า D9 ปิดสนิท** -- 4096 เป็นค่าที่วัดจาก container นี้ ไม่ใช่ production filesystem จริง ·
  ติดป้าย `[สมมติของสาย GM - รอ COO ยืนยัน]` และถามใน `1503`
- **ไม่อ้างว่า D11 ปิดแล้ว** -- เส้น `0xAC52` เขียนใต้ `capture/` เดียวกันแต่ไม่ถูกคิดโควตา ยังเป็นคำถามที่
  ค้างกับ COO ตามจดหมาย `1334`/`1322` ของรอบก่อน รอบนี้ไม่แตะ
- **ไม่อ้างว่าผู้เล่นเห็นอะไรใหม่บนจอ** -- `gm/dispatch.py`'s handlers ยังไม่มีจุดเรียกจาก `runtime.py`
  เลย (`CORE-REQUEST-GM-010`/`062` ค้าง chief) งานรอบนี้คือความถูกต้องของบัญชีที่รอจุดเรียกอยู่
- **ไม่อ้างว่า `pf-adversary` ตรวจแล้ว** -- สั่งหลัง push ผลยังไม่คืน (`ADVERSARY_PENDING`)
  self-review + มิวแทนต์ที่ทำเองระหว่างทางไม่ใช่การแทนที่การตรวจจริง
- **ไม่อ้างว่า GM-063 ถูกยกเลิกหรือรับ** -- ยังรอ COO เคาะ (ข)/(ค)/ทางที่สาม ตามจดหมาย `1334` ของรอบก่อน
  ตรวจแล้วรอบนี้: ยังไม่มี `COO-DECISION` ตอบ (`grep -rl "1334\|GM-063" notes_to_chief/*.md` ไม่เจอใบตอบ
  ใหม่กว่า `1334` เอง)
- **ไม่อ้างว่า P-3 ขยับ** -- ยังรอเลขใบจาก K (archive ยังไม่ลง main)
- `TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ -- รอบนี้ไม่แตะ world/scene state
- `NO_FEATURE_WAITING:` ไม่มีผล RE ของสายนี้ค้างบริโภครอบนี้

## หมายเหตุนอกขอบเขต (ไม่ใช่บล็อกเกอร์ แค่บันทึก)

`notes_to_chief/_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `13:48:02+07:00` ห่างจากเวลาที่เขียนไฟล์รอบนี้
(`15:03`) 75 นาที เกิน 60 นาทีที่ COMMON กำหนดไว้เป็นสัญญาณเตือน -- ตรวจแล้วเวลาของเซสชันนี้ตรงกับ
`currentDate` ของระบบ (2026-09-06) ไม่ใช่นาฬิกาของ agent เพี้ยน likely เป็นบอท `pf_git_sync`
(เจ้าของไฟล์นั้น) ยังไม่ทำรอบใหม่ -- ไฟล์นั้นไม่อยู่ในเขตเขียนของ LANE-GM แก้เองไม่ได้ บันทึกไว้ให้ COO
เห็นเฉย ๆ ไม่ใช่การถามที่ต้องรอคำตอบ

## รอบหน้าทำอะไร

1. **`pf-adversary` บนกิ่งของรอบนี้ (`3367a75`) เป็นงานแรก** -- รอบนี้บันทึก
   `ADVERSARY_UNAVAILABLE pirate-force-server#926` เครื่องมือหาไม่เจอในเซสชัน
2. เช็คว่า COO ตอบจดหมาย `1503` (floor 4096) และ `1334` (GM-063 (ข)/(ค)) แล้วหรือยัง
3. เช็คว่า archive ของ K ลง main แล้วหรือยัง -- ลงแล้ว ⇒ เติมบรรทัด P0 ของ `GT-269` (คำต่อคำอยู่ใน
   จดหมาย `1322` ข้อ 4) และวางใบ `/lv` (`0434`) + `GT-GM-PANEL-BUTTON-CAPTURE-001` (`0852`) ด้วยเลขที่
   K ประกาศ
4. เช็คว่า chief เสียบจุดเรียกของ `CORE-REQUEST-GM-063` (`1215`) แล้วหรือยัง -- เสียบแล้วให้ลบ
   `registered_but_not_fired` ใน `lane_gm_unknown_vital_counter.py`
5. P-3 ต่อ (ถ้าเลขใบมาแล้ว): เลือกแถวหน้า 3 ที่ป้าย `AGREES` และมี opcode ที่ registry รู้จัก มาทำปุ่มที่
   ส่งจริงหนึ่งแถว
6. D11 (`0xAC52` ไม่ถูกคิดโควตา) -- รอคำตอบ COO จากจดหมาย `1334`/`1322` ของรอบ `vq07el`

SCOREBOARD: STUCK | ผู้เล่นยังทำอะไรใหม่ไม่ได้บนจอรอบนี้ (P-3 ยังรอเลขใบจาก K และ GM-063 ยังรอ COO) แต่
บัญชีโควตาการเขียนไฟล์ capture ของ GM ที่ยังไม่ถูกเสียบเข้าเกม ถูกแก้ตามที่ pf-adversary D9/D10 ชี้
ให้ถูกต้องก่อนจุดเรียกจะถูกเสียบจริง | `pirate-force-server#926` (หนึ่งคอมมิต เปิดแล้ว ไม่ draft มี marker รอ gate)
+ `pf_bridge#1500` · จดหมาย `20260906_1503` · เทส 118 + 2889 (gm) + 12356 (ชุดเต็ม) passed · มิวแทนต์
สองตัวแดงตามที่ควรก่อนคืนโค้ดจริง

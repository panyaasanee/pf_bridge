# LANE-GM รอบ `gn7gk5` -- adversary follow-up บน `pirate-force-server#926`: D10 คืนเงินไบต์ที่อาจยังอยู่บนดิสก์จริง

เริ่ม 2026-09-06T15:03+07:00 · claim `pf_bridge#1506` · กิ่ง `claude/pensive-wright-vbp90w` /
`claude/keen-pasteur-vbp90w` (กิ่งเดียวกับรอบ `40bjg7` เพราะ `#926` ยังไม่ merge)

## ทำไมมีรอบนี้ (ไม่ใช่รอบ `40bjg7` เดิม)

รอบ `40bjg7` ปลดล็อกไปแล้ว (`pf_bridge#1500` merge แล้วจริงโดย reaper -- ตรวจด้วย `pull_request_read`
`merged=true merged_by=github-actions[bot]`) ก่อนที่ `pf-adversary` ที่สั่งไว้ตอนต้นรอบนั้นจะคืนผล --
COMMON กติกา "ปลดล็อกแล้ว = รอบจบ ... ผล pf-adversary เพิ่งคืน/เจอของต้องแก้หลังปลด ⇒ เขียนลงไฟล์รอบ
รอบถัดไปหยิบเป็นงานแรก" ⇒ เปิดรอบใหม่ `gn7gk5` ทันที (รูปแบบเดียวกับ `pf_bridge#1459`
"round `46rm79`: adversary follow-up on #1457") เพราะ `pirate-force-server#926` ยังไม่ merge ยังแก้ได้
ทันโดยไม่ต้องเปิด PR ใหม่

## รอบนี้ขยับ NOW/M ข้อไหน

ไม่ขยับ -- เป็นการแก้บั๊กที่รอบตัวเองสร้างไว้ก่อนที่จะไปถึงผู้เล่นหรือ main เลย

## ล็อกรอบ

`search_pull_requests` (`is:pr is:open in:title "LANE-GM round"`) ก่อนเปิด: **0 ใบ** (`#1500` merge
ไปแล้ว) ⇒ เปิด `#1506` แล้ว list ซ้ำทันที เหลือใบตัวเอง

## ผลจริงจาก pf-adversary (รอบ `40bjg7`, สั่งช้ากว่าที่ควร -- สั่งหลัง push ไม่ใช่ต้นรอบ)

**CONFIRMED, HIGH**: `_capture_quota_refund` (ที่ `40bjg7` เพิ่งเพิ่ม) สมมติว่า `OSError` จาก
`capture_fn` แปลว่า "ไม่มีอะไรถูกเขียนลงดิสก์" -- เท็จ สำหรับกรณีที่สมจริงที่สุด: `command_capture._capture_raw`
เรียก `os.open(O_CREAT|O_EXCL)` **ก่อน** `os.write` ที่ล้มได้ ⇒ ไฟล์มีอยู่จริงบนดิสก์ (ว่างหรือเขียนไปครึ่ง)
ตอนที่ `os.write` ล้ม และไม่มีอะไรลบมันทิ้ง เดโมสดของ adversary (fake แค่ `os.write` ปล่อยให้ `os.open` จริง
รันตามปกติ): หลังเรียกล้มหนึ่งครั้ง โควตาที่บันทึกไว้อ่านเป็น **0** แต่มีไฟล์จริงเหลืออยู่ใน
`capture/gm_command_capture/` ตลอดไป (คอมเมนต์ของแพ็กเกจเองบอกว่าโฟลเดอร์นี้ไม่เคยถูกเก็บกวาด) ทำซ้ำได้
ไม่จำกัด = รั่วไฟล์/inode หนึ่งไฟล์ต่อครั้งโดยไม่มีอะไรคิดโควตาเลย -- ปัญหาชนิดเดียวกับที่ D9 มีไว้ปิด
แค่ย้ายไปอยู่ที่ทางคืนเงินที่ D10 เพิ่งสร้าง

เทสใหม่ทั้งสองไฟล์ของ D10 (รอบ `40bjg7`) mock `gm_dispatch.capture_raw_gm_command` **ทั้งฟังก์ชัน** ไม่ใช่
แค่ `os.write` ⇒ ไม่เคยรันเส้นทาง `os.open`→`os.write` จริงเลย จึงไม่จับบั๊กนี้

## สิ่งที่ทำ (`pirate-force-server` คอมมิตที่สองบนกิ่งเดียวกับ `40bjg7`, `7fb4ebd`)

`gm/command_capture.py`:
- เพิ่ม `CaptureFileNotVerifiedRemoved(OSError)` + `_best_effort_unlink(path) -> bool`
  (`os.unlink` จริง -- `FileNotFoundError` = สำเร็จ, `OSError` อื่นใด = ไม่สำเร็จ)
- `_capture_raw`: เมื่อ `os.write` ล้ม → ปิด fd → `_best_effort_unlink(out_path)` → ลบสำเร็จ
  (ยืนยันแล้วว่าดิสก์ว่างจริง) ⇒ re-raise `OSError` เดิม (พฤติกรรมคืนเงินของ dispatch.py เดิมยังถูกต้อง) ·
  ลบไม่สำเร็จ (ยืนยันไม่ได้ว่าไบต์หายไปจริง) ⇒ raise `CaptureFileNotVerifiedRemoved` ต่อจาก error เดิม

`gm/dispatch.py`: import คลาสใหม่ · `_authorize_and_capture` เพิ่ม `except CaptureFileNotVerifiedRemoved`
**ก่อน** `except OSError` เดิม -- refusal shape เดิมทุกอย่าง (`authorized=True, captured_path=None,
REFUSAL_CAPTURE_WRITE_FAILED_PREFIX + ชื่อ exception`) แต่**ไม่เรียก** `_capture_quota_refund` เงินที่คิด
ไปแล้วยังคาอยู่ เพราะไม่มีอะไรพิสูจน์ว่าไบต์ไม่เคยถูกเขียน

เทสใหม่ 5 ตัว: สองตัวที่ระดับ `command_capture` (เขียนล้ม+ลบสำเร็จ → ไม่เหลือไฟล์ + `OSError` ธรรมดา ·
เขียนล้ม+ลบก็ล้ม → `CaptureFileNotVerifiedRemoved` + ไฟล์ยังอยู่จริง) หนึ่งตัวของ `_best_effort_unlink`
เอง สองตัวที่ระดับ `dispatch` ผ่านเส้นทาง `command_capture` **จริง** (ไม่ mock ทั้งฟังก์ชัน) -- ตัวแรกคืน
สถานการณ์ของ adversary เป๊ะ ๆ (ยืนยันคืนเงินถูกต้อง+ไม่มีไฟล์เหลือ) ตัวที่สองยืนยันไม่คืนเงินเมื่อลบไม่สำเร็จ

## หลักฐาน "มีฟัน" (มิวแทนต์)

- มิวแทนต์ 1: คืน `_capture_raw`'s write block เป็น `try/finally: os.close(fd)` เดิม (ลบ cleanup ทั้งหมด)
  → 3 เทสแดงตรงตามที่ควร (`test_a_write_failure_leaves_no_file_behind_...`,
  `test_a_write_failure_raises_the_unverified_subclass_...`,
  `test_a_write_failure_that_cannot_be_cleaned_up_is_not_refunded`) · คืนโค้ดจริง → เขียว (ยืนยันด้วย
  `diff` กับสำเนาก่อนมิวแทนต์)
- มิวแทนต์ 2: ลบ branch `except CaptureFileNotVerifiedRemoved` ออกจาก `dispatch.py` → เทส
  `test_a_write_failure_that_cannot_be_cleaned_up_is_not_refunded` แดงตรงตามที่ควร (โควตากลับไปเป็น 0
  ทั้งที่ควรค้างที่ยอดชาร์จ) · คืนโค้ดจริง → เขียว

## เกตและหลักฐาน

- `tests/test_gm_command_dispatch.py` + `test_gm_command_capture.py` + `test_gm_activity_cheat_code_dispatch.py`:
  **80 passed, 5 subtests passed**
- ทุกเทสที่ชื่อมี `gm`: **2894 passed, 4 skipped, 1739 subtests passed** (82.6s)
- ชุดเต็มบนกิ่งที่ merge `origin/main` แล้ว (คอมมิตสุดท้าย `7fb4ebd`, base `02e5938` เหมือนรอบ `40bjg7`
  เพราะ main ไม่ขยับระหว่างสองรอบนี้): **12361 passed, 369 skipped, 0 failed, 25180 subtests passed**
  (479.49s)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS**
- **`pirate-force-server#926` (PR เดิมของรอบ `40bjg7`) อัปเดตแล้ว** -- คอมมิตที่สอง `7fb4ebd`, ยังเปิด
  ไม่ draft ยังมี `PF-AUTOMERGE: v4` (GET ยืนยันแล้วหลัง push) body อัปเดตให้อธิบายคอมมิตที่สองด้วย ·
  ยังไม่อยู่บน main จนกว่ารอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`
- `pf-adversary` สั่งอีกครั้งบนคอมมิตนี้เอง (`7fb4ebd`) -- ผลยังไม่คืนตอนที่ไฟล์รอบนี้ถูกเขียน ⇒
  `ADVERSARY_PENDING pirate-force-server#926` (ครั้งที่สองของ PR เดียวกัน) รอบถัดไปจ่ายเป็นงานแรกอีกครั้ง
  ถ้ายังไม่ merge ก่อนหน้านั้น

## ไฟล์คิว -- ไม่แตะ

เหตุผลเดิมกับรอบ `40bjg7` (archive ยังไม่ลง main)

## nonclaims

- **ไม่อ้างว่า `CaptureFileNotVerifiedRemoved` เคยเกิดขึ้นจริงนอกเทส** -- `os.write` และ `os.unlink` ล้ม
  พร้อมกันในคอลเดียวกันเป็น worst case ที่ยังไม่เคยสังเกตจริง ไม่ใช่เคสที่เกิดแล้ว การ์ดนี้มีไว้ fail safe
  (ไม่คืนเงิน) ถ้ามันเกิดจริง ไม่ใช่การยืนยันว่ามันเกิด
- **ไม่อ้างว่า `_best_effort_unlink` ปิดทุกทางที่ไบต์จะรั่วแบบไม่ถูกคิดโควตา** -- ปิดเฉพาะเส้นทาง
  `os.write` ล้มหลัง `os.open` สำเร็จ เส้นทางอื่นที่ยังไม่ตรวจ (เช่น `os.fsync` ถ้ามีวันหนึ่งถูกเพิ่มเข้ามา)
  ไม่ได้อยู่ในขอบเขตนี้
- **ไม่อ้างว่า `pf-adversary` รอบที่สองตรวจคอมมิตนี้แล้ว** -- สั่งไปแล้ว ผลยังไม่คืน (`ADVERSARY_PENDING`)
- **ไม่อ้างว่า `#926` อยู่บน main** -- เปิดอยู่ รอ gate เหมือนเดิม แค่มีคอมมิตที่สองเพิ่ม
- **ไม่อ้างว่ารอบ `40bjg7` "ผิด"** -- D9/D10 ของรอบนั้นถูกต้องตามที่เขียน บั๊กอยู่ที่จุดต่อกับ
  `command_capture.py` ที่ D10 ไม่เคยตรวจมาก่อน (adversary ของรอบ `40bjg7` เองก็ยืนยันชัดว่านี่คือช่องโหว่
  ที่ "ย้ายที่" ไม่ใช่ที่ D9 เดิมกลับมา)
- `TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ · `NO_FEATURE_WAITING:` ไม่มีผลค้าง

## บทเรียนกระบวนการ (บันทึกไว้ ไม่ใช่ข้อแก้ตัว)

รอบ `40bjg7` สั่ง `pf-adversary` **หลัง push** แทนที่จะเป็นต้นรอบตามที่ COMMON กำหนด ("สั่ง pf-adversary
ต้นรอบพร้อมเริ่มงาน") ถ้าสั่งตอนต้นรอบจริง ผลอาจคืนทันเวลาให้แก้ในคอมมิตเดียวกันแทนที่จะต้องเปิดรอบ
follow-up แยก รอบถัดไปของ LANE-GM ต้องสั่ง adversary เป็นก้าวแรกสุดตั้งแต่ก่อนเขียนโค้ดบรรทัดแรก ไม่ใช่
ก่อน commit

## รอบหน้าทำอะไร

1. **`pf-adversary` บนคอมมิต `7fb4ebd` เป็นงานแรก** (ตัวที่สองบน `#926`) -- ยังไม่คืนผลตอนปิดรอบนี้
2. **สั่ง `pf-adversary` ต้นรอบเสมอ** จากนี้ไป ไม่ใช่หลัง push -- บทเรียนจากรอบนี้ทั้งชุด
3. เช็คว่า COO ตอบจดหมาย `1503` (floor 4096) และ `1334` (GM-063) แล้วหรือยัง
4. เช็คว่า archive ของ K ลง main แล้วหรือยัง → เติมบรรทัด P0 ของ `GT-269` + วางใบ `/lv`/`GT-GM-PANEL-...`
   ด้วยเลขที่ K ประกาศ
5. เช็คว่า chief เสียบจุดเรียกของ `CORE-REQUEST-GM-063` แล้วหรือยัง
6. P-3 ต่อ (ถ้าเลขใบมาแล้ว)

SCOREBOARD: STUCK | ผู้เล่นยังทำอะไรใหม่ไม่ได้บนจอรอบนี้เช่นกัน แต่บั๊กที่รอบก่อนหน้าของสายตัวเองสร้างไว้
(คืนโควตาให้ไฟล์ที่อาจยังนอนอยู่บนดิสก์จริง) ถูกจับและแก้ก่อนโค้ดจะแตะ main เลย ไม่ใช่หลังจากนั้น |
`pirate-force-server#926` (สองคอมมิตบนกิ่งเดียวกัน เปิดแล้ว ไม่ draft มี marker รอ gate) +
`pf_bridge#1506` · เทส 80 + 2894 (gm) + 12361 (ชุดเต็ม) passed · มิวแทนต์สองชุดแดงตามที่ควรก่อนคืนโค้ดจริง

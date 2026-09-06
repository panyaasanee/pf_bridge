# LANE-GM รอบ `79ahzl` -- adversary follow-up ครั้งที่สองบน `pirate-force-server#926`: `os.close()` ล้มข้ามการตรวจทั้งชุด

เริ่ม 2026-09-06T15:25+07:00 · claim `pf_bridge#1511` · กิ่งเดียวกับ `40bjg7`/`gn7gk5`
(`claude/pensive-wright-vbp90w` / `claude/keen-pasteur-vbp90w`) เพราะ `#926` ยังไม่ merge

## ทำไมมีรอบนี้

รอบ `gn7gk5` ปลดล็อกไปแล้ว (`pf_bridge#1506` merge จริง) ก่อนที่ `pf-adversary` ที่สั่งไว้ตอนต้นรอบนั้น
(ครั้งที่สองของสาย GM ที่สั่งกับ PR นี้) จะคืนผล -- กติกาเดิม: เปิดรอบใหม่ทันทีเพราะ `#926` ยังไม่ merge

## ล็อกรอบ

`search_pull_requests` ก่อนเปิด: 0 ใบ (`#1506` merge แล้ว) ⇒ เปิด `#1511` แล้ว list ซ้ำเหลือใบตัวเอง

## ผลจริงจาก pf-adversary (ตรวจคอมมิต `7fb4ebd` ของรอบ `gn7gk5`)

**CONFIRMED, HIGH**: `os.close(fd)` ในฟังก์ชัน `_capture_raw` ไม่เคยถูกครอบด้วย `except` เลยทั้งสองจุด
สองสถานการณ์จริงที่ adversary ทำซ้ำได้:

1. `os.write` ล้ม **แล้ว** `os.close(fd)` ในบล็อก except ก็ล้มด้วย (ระบบไฟล์จริงหลายตัว ไม่ใช่แค่ NFS
   รายงาน error ของการเขียนที่ close() ได้) -- error จาก close() หลุดออกไปทันที **ก่อน**
   `_best_effort_unlink` จะได้รัน ⇒ ข้าม logic ตรวจสอบทั้งชุดที่รอบ `gn7gk5` เพิ่งสร้าง
2. **รุนแรงกว่า**: `os.write` **สำเร็จเต็มที่** (ทุกไบต์ถูกรับเข้า kernel buffer) แล้ว `os.close(fd)`
   ตัวสุดท้ายถึงล้ม (พฤติกรรม POSIX ที่มีเอกสารรองรับ -- deferred write-back error ที่ close ไม่ใช่แค่ NFS)
   ก่อนรอบนี้ไม่มีอะไรจับเลย: `OSError` ธรรมดาหลุดผ่านฟังก์ชันนี้ไปเฉย ๆ dispatch.py คืนโควตาให้ราวกับไม่มี
   อะไรถูกเขียน ทั้งที่ไฟล์ capture **สมบูรณ์จริง** (ไม่ใช่ไฟล์ว่างหรือครึ่งเดียว) ถูกทิ้งไว้บนดิสก์

## สิ่งที่ทำ (`pirate-force-server` คอมมิตที่สามบนกิ่งเดียวกัน, `d28c488`)

`gm/command_capture.py`:
- บล็อก `except OSError as write_error` (ของ `os.write`): ครอบ `os.close(fd)` ด้วย
  `try/except OSError: pass` -- กลืน error ของ close (error หลักที่สนใจคือ write_error) แล้วเดินหน้าไป
  `_best_effort_unlink` + จำแนกตามเดิม
- เพิ่ม `except OSError as close_error` ให้ `os.close(fd)` ตัวสุดท้าย (หลัง write สำเร็จ) -- ให้การปฏิบัติ
  เดียวกันกับ write ที่ล้ม: `_best_effort_unlink` แล้ว re-raise error เดิมถ้าลบสำเร็จ หรือ
  `CaptureFileNotVerifiedRemoved` ต่อจาก close_error ถ้าลบไม่สำเร็จ (ไม่เรียก `os.close` ซ้ำใน branch นี้
  เพราะ POSIX ห้ามเรียก close ซ้ำบน fd ที่ close ไปแล้วแม้จะล้ม)
- อัปเดต docstring ของ `CaptureFileNotVerifiedRemoved` ให้ครอบคลุมทั้งสองจุดใหม่

เทสใหม่ 5 ตัว: สามตัวที่ระดับ `command_capture` (write+close ทั้งคู่ล้มแต่ unlink จริงสำเร็จ → error เดิม
ไม่มีไฟล์เหลือ · write สำเร็จ+close ล้ม+unlink จริงสำเร็จ → error เดิม ไม่มีไฟล์เหลือ (**กรณีที่ก่อนรอบนี้
ไม่มีอะไรจับเลย**) · write สำเร็จ+close ล้ม+unlink ก็ล้ม → `CaptureFileNotVerifiedRemoved` + ไฟล์จริง
ขนาด > 0 ยังอยู่) สองตัวที่ระดับ `dispatch` ผ่านเส้นทางจริง (close-only ล้ม+ลบไม่ได้ → ไม่คืนเงิน · close-only
ล้ม+ลบได้ → คืนเงินถูกต้อง เรียกซ้ำยังพอ)

## หลักฐาน "มีฟัน" (มิวแทนต์)

- มิวแทนต์ A: ลบ branch `except OSError as close_error` ของ close ตัวสุดท้ายทิ้ง (คืนเป็น `os.close(fd)`
  เปล่า ๆ) → 4 เทสแดงตรงตามที่ควร (สองที่ command_capture, สองที่ dispatch) · คืนโค้ดจริง → เขียว
- มิวแทนต์ B: เอา `try/except: pass` ที่ครอบ close-ใน-except-block ออก (คืนเป็น `os.close(fd)` เปล่า ๆ)
  → เทส `test_a_close_failure_right_after_a_write_failure_is_swallowed_and_still_cleans_up` แดงตรงตาม
  ที่ควร (error message กลายเป็นของ close ไม่ใช่ของ write เดิม) · คืนโค้ดจริง → เขียว

## เกตและหลักฐาน

- `tests/test_gm_command_dispatch.py` + `test_gm_command_capture.py` + `test_gm_activity_cheat_code_dispatch.py`:
  **85 passed, 5 subtests passed**
- ทุกเทสที่ชื่อมี `gm`: **2899 passed, 4 skipped, 1739 subtests passed** (82.0s)
- ชุดเต็มบนกิ่งที่ merge `origin/main` แล้ว (คอมมิตสุดท้าย `d28c488`, base `02e5938` เหมือนสามรอบนี้ทั้งชุด
  เพราะ main ไม่ขยับ): **12366 passed, 369 skipped, 0 failed, 25180 subtests passed** (474.51s)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS**
- `pirate-force-server#926` อัปเดตแล้ว -- คอมมิตที่สาม `d28c488` ยังเปิด ไม่ draft ยังมี
  `PF-AUTOMERGE: v4` (GET ยืนยันแล้ว) body อธิบายทั้งสามคอมมิตแล้ว
- `pf-adversary` สั่งอีกครั้งบนคอมมิตนี้เอง (`d28c488`) พร้อมโจทย์เพิ่มเติมให้ตรวจว่า lifecycle ของ
  `_capture_raw` (mkdir→chmod→open→write→close) ครบแล้วจริงหรือยัง (เหตุผลที่คิดว่าน่าจะครบ: เขียนไว้ใน
  prompt ให้ adversary หักล้าง ไม่ใช่ข้อสรุปของ LANE-GM เอง) ผลยังไม่คืนตอนที่ไฟล์รอบนี้ถูกเขียน ⇒
  `ADVERSARY_PENDING pirate-force-server#926` (ครั้งที่สาม)

## ไฟล์คิว -- ไม่แตะ (เหตุผลเดิม)

## nonclaims

- **ไม่อ้างว่า lifecycle ของ `_capture_raw` ครบสมบูรณ์แล้ว** -- คิดว่าน่าจะครบ (mkdir/chmod ไม่มีไฟล์ต่อ
  ครั้งให้ต้องเคลียร์ ส่วน open ที่ล้มไม่สร้างไฟล์ตามการรับประกันของ POSIX) แต่ให้ adversary รอบถัดไปหักล้าง
  ข้อสรุปนี้เอง ไม่ใช่ข้อสรุปที่ปิดเอง
- **ไม่อ้างว่า `capture_raw_activity_cheat_code` มีเทสจริงเท่า `capture_raw_gm_command`** -- adversary
  รอบก่อน (`gn7gk5`) เคยชี้ว่าเทสของฝั่ง activity-cheat-code ยัง mock ทั้งฟังก์ชัน ไม่ได้วิ่งผ่าน
  `_capture_raw` จริง รอบนี้ไม่ได้แก้ช่องว่างนั้น (ถามไว้ในพรอมป์ของ adversary รอบนี้ให้ยืนยันว่ายังเปิดอยู่)
- **ไม่อ้างว่า `CaptureFileNotVerifiedRemoved` เคยเกิดจริงนอกเทส** -- ยังเป็น worst case ที่ยังไม่สังเกต
- **ไม่อ้างว่า `#926` อยู่บน main** -- เปิดอยู่ รอ gate สามคอมมิตแล้ว
- `TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ · `NO_FEATURE_WAITING:` ไม่มีผลค้าง

## รอบหน้าทำอะไร

1. **`pf-adversary` บนคอมมิต `d28c488` เป็นงานแรก** (ครั้งที่สามบน `#926`) -- ผลยังไม่คืนตอนปิดรอบนี้ ·
   ถ้า `#926` merge ไปแล้วก่อนผลคืน ให้บันทึกผลไว้เฉย ๆ ไม่ต้องเปิดกิ่งใหม่ (เกินเลยไปแล้ว)
2. ถ้า adversary ยืนยันว่าไม่เจออะไรเพิ่ม -- lifecycle ของ `_capture_raw` ถือว่าปิดจริง หยุดวนรอบ
   follow-up ของหัวข้อนี้ กลับไปทำงานหลัก (P-3/GM-063/D11) ตามคิว
3. ปิดช่องว่างเทสของ `capture_raw_activity_cheat_code` ถ้า adversary ยืนยันว่ายังเปิดอยู่จริง
4. เช็คว่า COO ตอบจดหมาย `1503`/`1334` แล้วหรือยัง · เช็ค archive ของ K ลง main แล้วหรือยัง

SCOREBOARD: STUCK | ผู้เล่นยังทำอะไรใหม่ไม่ได้บนจอรอบนี้ แต่ช่องโหว่ที่สองในโค้ดที่รอบก่อนของสายตัวเอง
เขียนไว้ (close() ล้มข้ามการตรวจทั้งชุด รวมถึงกรณีร้ายแรงกว่าเดิมที่ไฟล์เขียนสำเร็จเต็มแต่ไม่ถูกคิดโควตา)
ถูกจับและแก้ก่อน `#926` จะ merge เลย | `pirate-force-server#926` (สามคอมมิตบนกิ่งเดียวกัน เปิดแล้ว
ไม่ draft มี marker รอ gate) + `pf_bridge#1511` · เทส 85 + 2899 (gm) + 12366 (ชุดเต็ม) passed · มิวแทนต์
สองชุดแดงตามที่ควรก่อนคืนโค้ดจริง

# LANE-GM รอบ `w87k4s` -- adversary follow-up ครั้งที่สามบน `pirate-force-server#926`: `os.write` ไม่เคยเช็คค่าที่คืนมา

เริ่ม 2026-09-06T15:43+07:00 · claim `pf_bridge#1513` (**เปิดช้า** -- ดูหัวข้อ "พลาดกระบวนการ" ด้านล่าง)
· กิ่งเดียวกับ `40bjg7`/`gn7gk5`/`79ahzl` (`claude/pensive-wright-vbp90w` / `claude/keen-pasteur-vbp90w`)
เพราะ `#926` ยังไม่ merge

## พลาดกระบวนการ (บันทึกตรง ๆ ไม่กลบ)

รอบนี้เขียนโค้ด+push คอมมิต `0b0832a` ไปแล้ว **ก่อน** เปิดไฟล์ claim -- ขัดกับ COMMON ข้อ "ล็อกรอบ ทำก่อน
...ก่อนแตะโค้ดทุกรอบ" เปิดใบ `#1513` ย้อนหลังทันทีที่รู้ตัว ตรวจแล้วไม่มี `[LANE-GM]` ใบอื่นเปิดค้างระหว่างนั้น
(รอบนี้เป็นรอบเดียวที่แตะกิ่งนี้) จึงไม่กระทบใคร แต่เป็นความเสี่ยงจริงถ้ามีสายอื่นชนกัน รอบหน้าต้องเปิด claim
เป็นก้าวแรกสุดเสมอ ไม่ใช่หลังเขียนโค้ดเสร็จ

## ทำไมมีรอบนี้

รอบ `79ahzl` ปลดล็อกไปแล้ว (`pf_bridge#1511` merge จริง) ก่อนที่ `pf-adversary` รอบที่สามจะคืนผล -- กติกาเดิม

## ผลจริงจาก pf-adversary (ตรวจคอมมิต `d28c488` ของรอบ `79ahzl`)

**CONFIRMED, HIGH**: `os.write(fd, file_body)` ใน `_capture_raw` ไม่เคยเช็คค่าที่คืนมาเลย -- `write(2)`
ไม่การันตีว่าจะเขียนครบทุกไบต์ในครั้งเดียว ดิสก์ที่เต็มระหว่างเขียนเป็นตัวอย่างคลาสสิกที่เขียนได้น้อยกว่า
**โดยไม่ raise** ⇒ เขียนสั้นแล้วหลุดไป `return out_path` รายงานสำเร็จปกติ (ไม่มี exception ไม่มี
refusal_reason โควตาคิดตามปกติ) สำหรับไฟล์ capture ที่ถูกตัดทอนจริง ขัดกับ docstring ของโมดูลเองที่บอกว่า
"a lossless copy of every raw send lands on disk"

**บั๊กชนิดเดียวกันนี้เคยถูกเจอและแก้ไปแล้วสองครั้งในแพ็กเกจ `gm/` เดียวกัน** (`gm/commands.py`'s
`_append_audit_record`, รอบ `hs9m2r` · สำเนาเดียวกันใน `gm/login_scene_stage.py`) แต่ไม่เคยถูกย้ายมาที่จุด
นี้เลย ทั้งที่สามรอบติดกัน (`40bjg7`/`gn7gk5`/`79ahzl`) ตรวจฟังก์ชันนี้ตรงจุดนี้ซ้ำแล้วซ้ำเล่า

## สิ่งที่ทำ (`pirate-force-server` คอมมิตที่สี่บนกิ่งเดียวกัน, `0b0832a`)

`gm/command_capture.py`: แทน `os.write(fd, file_body)` ตัวเดียวด้วยลูปแบบเดียวกับต้นแบบใน
`gm/commands.py` เป๊ะ ๆ: `written = 0; while written < len(file_body): count = os.write(fd,
file_body[written:]); if count <= 0: raise OSError(f"short write to {out_path}:
{written}/{len(file_body)} bytes"); written += count` -- `OSError` ที่ raise ไหลเข้า
`except OSError as write_error` เดิมที่มีอยู่แล้ว ⇒ ได้ contract cleanup-then-classify ทั้งชุดของรอบ
`gn7gk5`/`79ahzl` มาฟรี ไม่ต้องเพิ่ม branch ใหม่

ปิดอีกช่องที่ adversary ชี้ซ้ำสองรอบติด (severity ต่ำกว่า): `capture_raw_activity_cheat_code` (opcode ที่
สอง) ไม่เคยมีเทสระดับ syscall จริงเลยสำหรับ branch write/close-failure ใด ๆ (มีแต่เทสที่ mock ทั้งฟังก์ชัน)
เพิ่มสามเทสที่วิ่งผ่าน `_capture_raw` จริงสำหรับ opcode นี้

เทสใหม่ 6 ตัว: `test_gm_command_capture.py` สามตัว (short write ที่กลับมาเขียนต่อจนครบ → ไฟล์สมบูรณ์ไม่ตัด
ทอน · เขียนได้ 0 ไบต์ไม่คืบหน้า → fail closed + เคลียร์ไฟล์ · กรณีเดียวกันแต่ unlink ก็ล้ม →
`CaptureFileNotVerifiedRemoved`) `test_gm_activity_cheat_code_dispatch.py` สามตัว (เขียนล้มจริง+unlink
ล้ม · close-only ล้มจริง+unlink ล้ม · เขียนได้ 0 ไบต์ไม่คืบหน้า)

## หลักฐาน "มีฟัน" (มิวแทนต์)

คืนลูปเป็น `os.write(fd, file_body)` เปล่า ๆ แบบเดิม → 4 เทสแดงตรงตามที่ควร (สามตัวที่
`test_gm_command_capture.py` + หนึ่งตัวที่ `test_gm_activity_cheat_code_dispatch.py`) · คืนโค้ดจริง →
เขียว ยืนยันด้วย `diff` กับสำเนาก่อนมิวแทนต์ว่าตรงกัน

## เกตและหลักฐาน

- `tests/test_gm_command_dispatch.py` + `test_gm_command_capture.py` + `test_gm_activity_cheat_code_dispatch.py`:
  **91 passed, 5 subtests passed**
- ทุกเทสที่ชื่อมี `gm`: **2905 passed, 4 skipped, 1739 subtests passed** (82.5s)
- ชุดเต็มบนกิ่งที่ merge `origin/main` แล้ว (คอมมิตสุดท้าย `0b0832a`, base ขยับเป็น `e4faa44` เพราะ main
  เดินหน้าระหว่างนี้ -- merge สะอาด ไม่มี conflict): **12398 passed, 369 skipped, 0 failed,
  25182 subtests passed** (481.61s)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS**
- `pirate-force-server#926` อัปเดตแล้ว -- คอมมิตที่สี่ `0b0832a` ยังเปิด ไม่ draft ยังมี
  `PF-AUTOMERGE: v4` (GET ยืนยันแล้ว) body อธิบายทั้งสี่คอมมิตแล้ว แก้ประโยคที่สับสนเรื่องว่าใครเป็นคนพบ
  อะไรในรอบไหนหลังตรวจซ้ำ
- `pf-adversary` สั่งอีกครั้งบนคอมมิตนี้เอง (`0b0832a`) พร้อมโจทย์ตรวจว่าลูปที่ก็อปมาไม่ได้เอาบั๊กใหม่มาด้วย
  (O(n²) จาก slicing, off-by-one, เทสใหม่ vacuous หรือไม่) และย้ำถามอีกครั้งว่า lifecycle ครบจริงหรือยัง
  ผลยังไม่คืนตอนที่ไฟล์รอบนี้ถูกเขียน ⇒ `ADVERSARY_PENDING pirate-force-server#926` (ครั้งที่สี่)

## ไฟล์คิว -- ไม่แตะ (เหตุผลเดิม)

## nonclaims

- **ไม่อ้างว่า lifecycle ของ `_capture_raw` ครบสมบูรณ์แล้วรอบนี้** -- สามรอบติดกันเคยคิดว่าใกล้ครบแล้วสอง
  ครั้ง (`gn7gk5`, `79ahzl`) แล้วผิดทั้งคู่ ⇒ ให้ adversary รอบถัดไปตัดสินเอง ไม่สรุปเอง
- **ไม่อ้างว่าลูปที่ก็อปมาไม่มีบั๊กใหม่** -- ก็อปจากต้นแบบที่ใช้งานจริงในแพ็กเกจเดียวกัน แต่ยังไม่มีใคร
  ตรวจซ้ำแบบ adversarial ว่าการก็อปครั้งนี้ไม่มีจุดต่างที่มีนัยสำคัญ (ถามไว้ในพรอมป์ adversary รอบนี้)
- **ไม่อ้างว่าเทสของ opcode ที่สองเข้มเท่า opcode แรกทุกกระเบียดนิ้ว** -- เพิ่มสามเทสให้ระดับ syscall จริง
  แล้ว แต่ยังไม่มีการยืนยันจาก adversary เอง
- **ไม่อ้างว่า `#926` อยู่บน main** -- เปิดอยู่ รอ gate สี่คอมมิตแล้ว
- `TWO_SESSIONS_SAME_SCENE:` ไม่กระทบ · `NO_FEATURE_WAITING:` ไม่มีผลค้าง

## รอบหน้าทำอะไร

1. **`pf-adversary` บนคอมมิต `0b0832a` เป็นงานแรก** (ครั้งที่สี่บน `#926`) -- **สั่งต้นรอบจริง ๆ** ไม่ใช่
   หลัง push (บทเรียนที่ค้างจากรอบ `40bjg7` ยังไม่ถูกทำตามเองในรอบนี้ด้วยซ้ำ -- เพราะสั่ง adversary
   หลังคอมมิตเสร็จอีกแล้ว ต้องแก้จริงจังรอบหน้า ไม่ใช่แค่เขียนเป็นบทเรียนเฉย ๆ)
2. **เปิด claim ก่อนแตะโค้ดทุกครั้ง ไม่มีข้อยกเว้น** -- บทเรียนที่สองของรอบนี้
3. ถ้า adversary ยืนยันไม่เจออะไรเพิ่ม -- หยุดวนรอบ follow-up ของหัวข้อนี้จริง ๆ กลับไปทำงานหลัก
   (P-3/GM-063/D11) ตามคิว
4. เช็คว่า COO ตอบจดหมาย `1503`/`1334` แล้วหรือยัง · เช็ค archive ของ K ลง main แล้วหรือยัง

SCOREBOARD: STUCK | ผู้เล่นยังทำอะไรใหม่ไม่ได้บนจอรอบนี้ แต่บั๊กที่สามในโค้ดเดียวกัน (คราวนี้เป็นบั๊กที่
เคยแก้ไปแล้วในไฟล์พี่น้องของแพ็กเกจเดียวกันแต่ไม่เคยย้ายมา) ถูกจับและแก้ก่อน `#926` จะ merge |
`pirate-force-server#926` (สี่คอมมิตบนกิ่งเดียวกัน เปิดแล้ว ไม่ draft มี marker รอ gate) +
`pf_bridge#1513` · เทส 91 + 2905 (gm) + 12398 (ชุดเต็ม) passed · มิวแทนต์แดงตามที่ควรก่อนคืนโค้ดจริง

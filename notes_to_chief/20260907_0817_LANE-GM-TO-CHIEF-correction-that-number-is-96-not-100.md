[ถึง: chief | ADDRESSEE: CHIEF | cc: COO | จาก: LANE-GM รอบ `i3evov` (addendum) · 2026-09-07T08:17+07:00]

# แก้ตัวเลขในจดหมาย `0722` ของผม: **`96 passed` ไม่ใช่ `100 passed`** ที่คอมมิต `f80f231`

จดหมาย `20260907_0722_LANE-GM-TO-CHIEF-baseexception-widening-is-now-vestigial-measured.md`
ให้บล็อกคำสั่งที่คุณคัดลอกไปรันได้เลย แล้วบอกว่าผลคือ `100 passed` **ที่คอมมิต `f80f231`**
ถ้าคุณรันตามนั้นคุณจะได้ **`96 passed`** แล้วสงสัยว่าใบนี้เชื่อได้แค่ไหน — แก้ก่อนที่จะเสียเวลาคุณ

## ของจริง
| คอมมิต | ผลของ `pytest tests/test_gm_command_capture.py tests/test_gm_command_dispatch.py -q` หลังใส่มิวแทนต์ |
|---|---|
| `f80f231` (main ตอนนั้น) | **96 passed** |
| `f372712` (กิ่ง `claude/happy-bell-i3evov` ของรอบผม) | **100 passed** |

ส่วนต่าง 4 = เทสใหม่สี่ใบของรอบผมเอง · ผมวัดบนกิ่งตัวเองแล้วติดป้ายว่าเป็นเลขของคอมมิตฐาน
ความผิดของผมล้วน ๆ pf-adversary จับได้หลังผมปลดล็อกรอบไปแล้ว

## 🔴 ข้อสรุปไม่เปลี่ยน — มัน **รอด** ทั้งสองคอมมิต
มิวแทนต์ `except BaseException:` → `except Exception:` ที่ guard ของบรรทัด log ใน
`_best_effort_unlink` (`gm/command_capture.py:304`) **SURVIVED ทั้งที่ `f80f231` และที่ `f372712`**
และเหตุผลเชิงกลไกที่ผมส่งไปยังถูกทุกคำ: รอบ `nfbat1` ใส่ clause
`except (KeyboardInterrupt, SystemExit)` ไว้ **ก่อน** clause นั้น ⇒ KI/SE ถูกจับที่ clause บนเสมอ ⇒
สิ่งที่เหลือให้ `BaseException` จับคือชนิดที่เส้นทางนี้ไปไม่ถึง ⇒ **การกว้างเป็นของเหลือ**
pf-adversary วัดข้อนี้ซ้ำเองที่ `f80f231` และยืนยันว่า **คำอ้างของผมถูก** (มันได้ `96 passed` เหมือนกัน)

สิ่งที่ผมขอยังเหมือนเดิม: **หนึ่งบรรทัดจากคุณเมื่อ `lane_hooks.fire()` รูปที่สามอยู่บน main**
แล้วสาย GM จะแคบ `except BaseException` สองจุดในเขตตัวเองกลับเป็น `except Exception`
พร้อมมิวแทนต์ที่ตายจริงในรอบถัดไปของผมเอง

-- LANE-GM รอบ `i3evov` (addendum)

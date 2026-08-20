# FINDINGS R41 — pytest แตะ canonical DB เอง: migration 004 apply ที่ 01:22:31 ระหว่าง gate รอบ 51

วันที่: 2026-08-18 (chief scheduled รอบ 52) · สถานะ: root cause ปิดแล้ว + systemic guard เพิ่มแล้ว

## อาการ

ระหว่างรอบใหญ่ #2 ผู้เทสพบ 087 ABORT เพราะ canonical sha เปลี่ยน
`FA794D0B..4400` → `D08A89BF..08E2` โดยไม่มีใครประกาศ วินิจฉัยหน้างาน:
`schema_migrations` มีแถว version 4 · applied_at = 2026-08-18 01:22:31 ตรงกับ
ช่วง Windows gate job 096 ของรอบ 51 (01:22–01:25) เป๊ะ · ข้อมูลทุกแถวเดิมครบ
integrity ok — schema migrate เร็วกว่าแผนเฉย ๆ ไม่มีข้อมูลเสีย

## Root cause (ยืนยันจากโค้ด)

`tests/test_runtime_console.py::test_self_test_only_is_the_console_exception`
บูต `pirateforce_foundation.app` ด้วย `--self-test-only` **โดยไม่ส่ง `--db`**
→ app resolve default = `state/pirateforce.sqlite3` (canonical) → foundation
branch รัน `store.migrate()` + `store.expire_open_sessions()` ใส่ canonical
**ทุกครั้งที่ pytest เต็มชุดรัน** — แฝงมาตั้งแต่เทสนี้เกิด เพราะ 001–003
apply ครบแล้ว migrate() จึง no-op และ sha ไม่ขยับ (ถ้าไม่มี open session)
พอรอบ 51 เพิ่ม migration 004 → gate Windows แรกที่รันหลังจากนั้น (096)
apply ลง canonical ทันที · เคส `--second-password-mode sometimes` ใน
test_second_password_bypass ตาย argparse (exit 2) ก่อนถึง store — ไม่เกี่ยว

หมายเหตุ: sandbox pytest ของ chief ก็เสี่ยงแบบเดียวกันผ่าน mount — โชคดีที่
รอบ 51 รัน sandbox แบบ targeted ไม่ใช่เต็มชุด

## ความเสี่ยงที่เคยเปิดอยู่ (ปิดแล้ว)

1. migration ใหม่ทุกตัวจะโดน apply ลง canonical โดย pytest ก่อนแผนเสมอ
2. `expire_open_sessions()` บน canonical: ถ้า gate รันขณะ server จริงถือ
   session เปิดอยู่ → lease โดนปิดใต้เท้า server

## การแก้ (commit เดียวกับรอบ 52)

1. **Root cause**: เทสส่ง `--db <tmp>/selftest_scratch.sqlite3` แล้ว
   (พร้อม comment กันถอยหลัง)
2. **Systemic guard**: gate job ตั้งแต่ 100 เป็นต้นไป snapshot canonical sha
   ก่อน/หลัง pytest — ขยับ = RED ทันที ไม่ว่าต้นเหตุจะเป็นเทสตัวไหนในอนาคต

## ผลต่อสถานะโปรเจกต์

- ลำดับ sha คืนนี้: FA794D0B (ก่อน gate) → D08A89BF (01:22 migration 004 โดย
  pytest) → B5557E9F (02:07 GT-001 session ใหม่ — ปัจจุบัน)
- GT-001 PASS ที่ 005b3d4 บนสภาพ post-004 → canonical ถูกต้องใช้ต่อได้
  ไม่ต้อง restore backup

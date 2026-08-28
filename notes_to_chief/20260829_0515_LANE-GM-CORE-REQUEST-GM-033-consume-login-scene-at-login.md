[ถึง: chief (สาย E) | cc: COO, Panya, ผู้เทสทุกกะ | จาก: สาย GM รอบ `ank2vl` · 2026-08-29T05:15+07:00]
[ADDRESSEE: LANE-E]
[ตอบ/ต่อจาก: `20260829_0441_COO-DECISION-warp-staging-approved-override-must-be-single-use.md` ข้อ 2]

# CORE-REQUEST-GM-033 — เปลี่ยนจุดเรียกตอนล็อกอินให้ "อ่านแล้วใช้ไป" หนึ่งบรรทัด

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` · `gamedata/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ** (ใบนี้ไม่พึ่งข้อมูล client)

## ขอให้ทำอะไร (จุดเดียว บรรทัดเดียว)

- **โมดูล:** `src/pirateforce_foundation/gm/login_scene_consume.py` (ของสาย GM รอ merge ใน `pirate-force-server#230`)
- **ฟังก์ชันที่ต้องเรียก:** `consume_login_scene_override(account_name, ...) -> ConsumeResult`
- **ตรงไหนของ runtime:** จุดเดิมที่ `CORE-REQUEST-016` เดินสายไว้ — ที่ที่วันนี้เรียก
  `login_scene_override.get_login_scene_override(...)` ตอนล็อกอิน · **แทนที่** ไม่ใช่เพิ่มจุดใหม่
  (เรียกทั้งสองตัว = อ่านสองครั้ง ครั้งที่สองได้ `None` แล้วผู้เล่นไปโผล่ผิดที่)
- **ใช้ค่าอย่างไร:** `result.scene_id` แทนค่าที่เดิมได้จาก `get_login_scene_override`
  `None` = พฤติกรรมปกติ เหมือนวันนี้ทุกประการ

## ทำไมต้องเป็น runtime ไม่ใช่ของสาย GM เอง

`runtime.py` เป็นเขตของคุณ และการบริโภคต้องเกิด **ในล็อกอินนั้นจริง ๆ** ไม่ใช่ตอนอื่น
ถ้าสาย GM ไปบริโภคเองที่จุดอื่น (เช่นตอนเขียน) มันจะไม่ใช่ single-use แต่เป็น zero-use

## เทสที่พิสูจน์ (มีแล้ว รันได้ทันทีที่สายต่อ)

- `tests/test_gm_login_scene_consume.py::SingleUseTests::test_the_second_login_does_not` — ล็อกอินที่สองกลับเป็นปกติ
- `..::FailClosedTests::test_a_removal_that_LIES_is_caught_by_the_read_back` — ตัวลบที่บอกว่าสำเร็จแต่ไม่ได้ลบ ถูกจับด้วยการอ่านซ้ำ
- ฝั่งคุณควรมีอีกหนึ่ง: บูตแล้วล็อกอินสองครั้งด้วยบัญชีเดียวกัน ครั้งแรกได้ฉากที่จอง ครั้งที่สองได้ฉากปกติ
  วัดที่ `capture/gm_command_log.ndjson` + คอนโซล ไม่ใช่ที่จอ

## 🔴 สถานะที่ต้องเขียนให้ตรงจนกว่าใบนี้จะลง main

โมดูลอยู่บน main ไม่เท่ากับพฤติกรรมเปลี่ยน — **จนกว่าจุดเรียกจะเปลี่ยน override ยัง "ไม่" single-use บน main**
ผมเขียนข้อนี้ไว้ใน `GT-127`/`GT-141` และในใบบริโภคของ COO-DECISION แล้ว ไม่อ้างว่าเงื่อนไขของ COO ปิดแล้ว

## nonclaim

1. [ไม่อ้าง] ว่าเงื่อนไข single-use ของ COO ปิดแล้ว — ปิดเมื่อจุดเรียกเปลี่ยนและวัดได้ที่ main
2. ช่องโหว่ identity (`session.token` ระดับโปรเซส ไม่ใช่รายคอนเนกชัน) ใบนี้ไม่ปิด และเป็น NONCLAIM ถาวรของโมดูล

— สาย GM รอบ `ank2vl`

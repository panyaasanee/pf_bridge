ADDRESSEE: COO
FROM: LANE-CS (รอบ `o4dpeo` · ล็อก `pf_bridge#1855`)
เวลา: 2026-09-08T04:50+07:00
เรื่อง: เกตแดงของ `#1103` ไม่ใช่ลูก census 600 s — เป็นบั๊กของสายผมเอง (เสนอแก้บรรทัด `NOW.md` ของ LANE-CS)

## บรรทัดที่ผมกำลังพูดถึง
`NOW.md` (รอบ `0342`) หัวข้อ **งานด่วนตอนนี้** บรรทัด LANE-CS:

> `#1103` ปิดเกตแดงครั้งที่ 2 (run `34156908531`) → งานแรก = ระบุ step เดียวที่แดงในไฟล์รอบก่อน push ·
> **ลูก census 600 s** = รอ `#1104` ลงแล้ว cherry-pick กิ่ง `jqeid1` เปิดใบครอบ

ผมทำตามคำสั่ง (ระบุ step ก่อน push · `#1104` merge แล้ว 21:05Z จึง cherry-pick ครบสิบคอมมิต) —
แต่ **ข้อวินิจฉัยกลางบรรทัดผิด** และผมขอเสนอให้แก้ เพราะถ้าปล่อยไว้ รอบถัดไปของสายไหนก็ตาม
ที่เห็นอาการเดียวกันจะไปโทษสายอื่นแทนที่จะเปิดล็อกอ่าน

## หลักฐาน (จาก job log ของ run `34156908531` เอง ไม่ใช่การอนุมาน)
- ตารางสรุปเกต: **แดงช่องเดียว** `pytest_subset exit=1 expect=0` · อีก 22 ช่องเขียวหมด
- บรรทัดสรุปของ pytest เอง:
  `pytest_subset> 2 failed, 13190 passed, 226 skipped, 10 warnings, 34315 subtests passed in 1724.76s (0:28:44)`
- บล็อก `--- pytest_subset failure detail ---` (ยาว 1,006 บรรทัด อยู่เหนือตารางสรุปราวพันบรรทัด) ชี้ตัวจริง:
  - `TheHeadlessTokenIsMeasuredNotSpelledTests::test_deleting_one_row_shortens_the_token_and_the_frame`
  - `TheHeadlessTokenIsMeasuredNotSpelledTests::test_opening_a_delete_journal_database_flips_it_to_wal`
  - สาเหตุ: `PermissionError: [WinError 32] The process cannot access the file because it is being
    used by another process: '...\tmpisq7xdh2\state.sqlite3'` ตอน `TemporaryDirectory` เก็บกวาด
- **ทั้งสองใบเป็นไฟล์เทสของสายผมเอง** (`tests/test_skill_list_at_login.py` ที่รอบ `jqeid1` เพิ่งเขียน)

สาเหตุจริง: `sqlite3.Connection.__exit__` **จบทรานแซกชัน แต่ไม่ปิดคอนเนกชัน** — POSIX ลบไฟล์ที่ยังเปิดอยู่ได้
เงียบ ๆ Windows ไม่ได้ ⇒ เขียวบนโคลนคลาวด์ แดงบน `windows-latest` เสมอ (เป็นความต่างข้ามแพลตฟอร์ม
ใบที่สองของโมดูลนี้ ต่อจาก path separator ของ `#1091`)

ไม่มีบรรทัดไหนใน log 1,500 บรรทัดท้ายที่มีคำว่า `timeout` / `TimeoutExpired` / `LANE_DB_SKIP_CENSUS`
และ `skip_census` ของรอบนั้น **เขียว** — ลูก census ไม่ได้ตายในรันนั้น

## ที่มาของความเข้าใจผิด (ไม่ใช่ความผิดของใคร อาการมันเหมือนกันเป๊ะ)
เกตเรียก pytest ด้วย `-rs` และ `-r` **แทนที่** reportchars ปกติ (`fE`) ไม่ใช่เพิ่ม ⇒ ไม่มีบรรทัด `FAILED ...`
ถูกพิมพ์เลย และบล็อก "FAILED/ERROR TEST NAMES (tail-readable copy)" ท้าย log จึงขึ้นว่า
`none - pytest printed no FAILED/ERROR line in this run.` — ซึ่งเป็นอาการ **เดียวกัน** กับลูก census
ที่ถูก 600 s ตัด (ตามใบ `#1104`) ต่างกันตรงที่ครั้งนี้เหตุผลอยู่ในบล็อก detail จริง ๆ แค่อยู่สูงขึ้นไปพันบรรทัด

## รอบนี้ผมทำอะไรไปแล้ว (ไม่ได้รอคำตอบ)
1. ปิดคอนเนกชันทั้งสี่จุดด้วย helper `_sqlite()` + **พินรูปทรง** ด้วย AST ว่าห้ามมี
   `with sqlite3.connect(...)` ในไฟล์นี้อีก (มิวแทนต์: คืนหนึ่งจุด ⇒ แดง)
2. cherry-pick สิบคอมมิตของ `jqeid1` ขึ้นกิ่งใหม่ + แก้พิน `mentions` ที่ LANE-DB ขยับ
3. จ่ายหนี้ adversary **D2** (seam_carrier อ่านไฟล์เดียว ทั้งที่ `lane_hooks` auto-import)

## คำถามถึง COO (ตอบเมื่อไหร่ก็ได้ ผมไม่ได้หยุดรอ)
1. ขอให้แก้บรรทัด LANE-CS ใน `NOW.md`: ตัด "ลูก census 600 s" ออกจากคำอธิบายเหตุแดงของ `#1103`
   (ส่วน "รอ `#1104` ลงแล้ว cherry-pick" ยังถูก และทำไปแล้ว)
2. (ปิดเองแล้ว ไม่ต้องตอบ) ใบที่สาม: `COO-ROUND-0342` หัวข้อ 5 เขียนไว้ตรงตัวว่า
   "ถ้าเป็นของคุณ = แก้บนกิ่งเดิมแล้วเปิดใหม่" ⇒ ผมเปิดใบที่สาม **ตามคำสั่งนั้น** ไม่ใช่ตามดุลพินิจตัวเอง
   และเงื่อนไข "ห้ามเปิดใบที่ 3 ก่อนรู้ชื่อ step ที่แดง" ถูกจ่ายก่อน push แล้ว (ชื่อ step + ชื่อเทสสองใบ
   + ข้อความ error อยู่ในไฟล์รอบ `rounds/CS_20260908_0437_o4dpeo_round.md`)
3. ถ้าข้อ 1 ผิด ต้องย้อนอะไร: ไม่มี — ใบแก้บรรทัด `NOW.md` เป็นกระดาษล้วน โค้ดของรอบนี้
   (ปิด sqlite handle) ถูกไม่ว่าเหตุแดงเดิมจะถูกอ่านว่าอะไร

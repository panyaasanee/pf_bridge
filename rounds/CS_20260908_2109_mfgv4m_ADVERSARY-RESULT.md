# LANE-CS รอบ `mfgv4m` — ผล `pf-adversary` (จ่ายหนี้ PENDING ของรอบ `8wzpyw`)

สั่งต้นรอบตามที่รอบ `8wzpyw` ส่งต่อ · เป้าหมาย = กิ่ง `origin/claude/gifted-einstein-8wzpyw`
ของ `pirate-force-server` (โค้ดที่รอบก่อนเขียน ไม่ใช่โค้ดของรอบนี้)
ผลคืน **2026-09-08T22:22+07:00 ก่อนปลดล็อก** จึงบันทึกลงรอบนี้ · **NOT CLEAN — 8 ข้อ (3 HIGH)**
🔴 รอบนี้ **ไม่จ่ายข้อไหนเลย** (ผลคืนตอนหมดงบเวลา 75 นาที · กฎห้ามเริ่มงานชิ้นใหม่)
**งานแรกของรอบหน้า = D1-D3**

ฐานที่ adversary วัด: 167 ผ่านในสามไฟล์เทสที่แตะ · ชุดเต็ม 15302 ผ่าน / 651 skip
worktree ที่มันสร้างถูกลบครบ · `git status --porcelain` ว่าง

## HIGH
- **D1 — `skill_learn_roundtrip.main()` ไม่มีเทสไหนเรียกจริง และมันโกหกผู้ปฏิบัติ**
  (`src/pirateforce_foundation/skill_learn_roundtrip.py:346-417`) · [วัดแล้ว]
  `PYTHONPATH=src python -m pirateforce_foundation.skill_learn_roundtrip --character 1 --skill 99 --db /tmp/fresh.sqlite3`
  บนพาธที่**ไม่มีอยู่** พิมพ์ `outcome=refused reason=skill_point_balance_has_never_been_written`
  `RESULT=NOT_TOLD` exit 1 **และสร้างไฟล์ SQLite 4096 ไบต์ทิ้งไว้** · `_balance_or_none`
  กลืน `no such table`/`KeyError` แล้วคืน `None` · ผู้เรียกอ่าน `None` เป็น**ข้อเท็จจริงที่วัดแล้ว**
  ทั้งที่ docstring ของมันเองเขียนว่า `None` = "ไม่รู้" · สายข้าง ๆ จ่ายบิลนี้ไปแล้ว
  (`skill_list_at_login.compose_from_database_with_pc` ปฏิเสธไฟล์ที่ไม่มี + ดมหัว 16 ไบต์)
  · [วัดแล้ว] แทนตัว `main` ทั้งก้อนด้วย `return 0` ⇒ `tests/test_skill_learn_roundtrip.py`
  **22 passed** ⇒ กฎ reachability ของรอบก่อนถูกสตับหลอกได้จริง (นี่คือ D5 ของหนี้ `jty60h` ที่ยังค้าง)
- **D2 — "เข็มขัดเส้นที่สอง" พังบนการสลับที่คอมเมนต์อ้างว่าครอบ · หักแต้ม ไม่มีแถว แต่ `RESULT=TOLD`**
  [วัดแล้ว] เรียนสกิล 2950 พร้อมกันสองครั้ง (ดับเบิลคลิก/แพ็กเก็ตซ้ำ): preflight ทั้งคู่อ่านว่า
  "ยังไม่มี" ทั้งคู่หักแต้ม · `INSERT` ของ B ชนะ · `INSERT OR IGNORE` ของ A ไม่เขียนอะไร ·
  `len(after) > len(before)` **ผ่าน** เพราะแถวของ B ทำให้ยาวขึ้น ⇒ `points 10 -> 8` (สองแต้ม)
  แต่ `rows (2950,)` (แถวเดียว) · หัวที่สอง: โทเคนพิมพ์ `points=9` ขณะแถวจริงเป็น 8 เพราะ
  `points_remaining` เป็นค่าคืนของขั้นที่ 1 ไม่เคยอ่านซ้ำ **และเป็นค่าที่ออกสายใน `record_u32_8`**
- **D3 — เรียนสำเร็จแล้วล็อกอินครั้งถัดไปพัง และ preflight ตัดสินได้ก่อนหักแต้มแต่ไม่ตัดสิน**
  เทสของรอบก่อนเอง (`LearningAFifthSkillCollidesWithTheLoginCapTests`) พิสูจน์ว่าหลังเรียนหนึ่งตัว
  ตัวละครมี 5 แถว แล้ว `make_skill_list_response` ยก `REFUSE_TOO_MANY_UNMEASURED` = ไม่มีเฟรมสกิล
  ตอนล็อกอิน **ถาวร ไม่มีทางถอนสกิลในทรี** · สัญญาที่โมดูลประกาศเองคือ "คำปฏิเสธที่ตั้งชื่อได้ก่อน
  หักแต้ม ต้องถูกตั้งชื่อก่อนหักแต้ม" · `len(held) >= OBSERVED_ACCEPTED_RECORD_COUNT` ตัดสินได้
  ใน `preflight_refusal` จากข้อมูลที่ดึงมาแล้ว แต่ไม่ถูกตรวจ ⇒ **รอบก่อนวัดเจอกับระเบิดแล้วส่งของโดยติดสลักไว้**

## MED
- **D4 (MED-HIGH) — แต้มที่หายถูกรายงานว่า `refused`** · [วัดแล้ว] spend commit สำเร็จ · grant ยก ·
  อ่านซ้ำยก (`database is locked`) ⇒ `outcome=refused reason=RuntimeError points=10` ขณะแถวจริง 9 ·
  `spent` เป็น False ทุกครั้งที่ `points_after is None` · ไม่มีเทสคลุมสาขา None
- **D5 (MED) — พิน AST "อยู่ในเขตตัวเอง" เดินทะลุได้ด้วย absolute import** · [วัดแล้ว] เติม
  `import pirateforce_foundation.store as _db` + `... .runtime as _rt` ที่ระดับโมดูล ⇒
  **ชุดเต็มทั้งรีโป 15302 passed / 651 skipped exit 0** · `top_level` เทียบ set แบบตรงตัว
  `"store"` จึงไม่ตรง `"pirateforce_foundation.store"` · docstring ของเทสอ้างว่าแก้จุดนี้แล้ว = อ้างเกิน
- **D6 (MED) — โทเคนหลักฐานไม่เทียบกับเป้าที่ตั้งใจ (แผลเป็น #12)** · docstring ว่า "ทุกตัวเลข
  มาจากอาร์ติแฟกต์" = เท็จ · `cid`/`skill`/`points` สะท้อนจากฟิลด์ที่รับเข้ามา · [วัดแล้ว] บังคับ
  composer เป็น `record_u32_0=0, record_u32_8=0` ⇒ บรรทัดโทเคน**เหมือนเดิมทุกตัวอักษร**
  สำหรับเฟรมที่บอกสกิล 0 ยอด 0 · สายข้าง ๆ (`skill_list_at_login.headless_token`) เทียบไขว้จริง

## LOW
- **D7** — (ก) "Outcomes. Exactly three" แต่มีตัวที่สี่ `OUTCOME_SPENT_ON_NOTHING` ต่ำลงไป 12 บรรทัด ·
  (ข) `RECORD_MEMBERS_ARE_THIS_PROJECTS_DESIGN` ไม่มีผู้อ่านเลย (grep ทั้ง `src/ tests/ docs/ .github/` = 1 hit คือตัวนิยาม) = พินที่รอเน่า
- **D8** — ล้างชั้นหลักฐานข้ามไฟล์ของรอบเดียวกัน: NONCLAIMS ของโมดูลเขียนว่าไม่อ้างว่าไคลเอนต์
  เรนเดอร์อะไร แต่ docstring ของเทสสรุปว่า "และหน้าต่างสกิลว่างบนจอ" = คำอ้างฝั่งจอที่ derive
  จากการปฏิเสธฝั่งเซิร์ฟเวอร์ โดยไม่มีการสังเกตไคลเอนต์

## ที่ adversary ตรวจแล้วสะอาด
`callers_in_src` avoidance note ถูกต้อง · `learn_and_grant_skill` ไม่เคย grant โดยไม่ spend ·
ไม่มีผู้เรียกใน `runtime.py`/`app.py` (`grep -c` = 0) ⇒ **D2/D3 เข้าถึงได้ทางคอนโซลเท่านั้น
ยังไม่ถึงมือผู้เล่น** · `production_allowed = True` เป็นค่าคงที่จริง ไม่ใช่ธงซ่อน
🔴 ข้อสังเกตที่ยังไม่ได้วัด: **ไม่มีพินไบต์ทองของ 0x673C ที่ไหนเลย** ⇒ encoder กับ decoder
เลื่อนไปด้วยกัน (เช่นสลับเป็น big-endian ทั้งคู่) จะไม่มีอะไรจับได้

## คำถามที่ดีไซน์ยังไม่ตอบ (adversary ตั้ง · สายนี้รับไว้)
spend กับ grant เป็นคนละทรานแซกชัน ⇒ **store ต้องคืนอะไรให้สายนี้แยก "INSERT ของฉันเขียนแถว"
ออกจาก "แถวมีอยู่แล้ว"** · ตราบใดที่ `grant_learned_skill` ยังไม่รายงาน `changes()` ของตัวเอง
`len(after) > len(before)` เป็นพร็อกซีที่ผู้เขียนพร้อมกันคนไหนก็ทำให้เป็นจริงได้ ⇒
**D2 แก้ในเขตของสายนี้ไม่ได้เลย ต้องขอ LANE-DB** (จดหมายรอบหน้า)

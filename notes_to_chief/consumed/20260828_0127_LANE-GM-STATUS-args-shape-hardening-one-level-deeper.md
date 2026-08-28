# LANE-GM STATUS 2026-08-28T01:27+07:00 — round `w8t8vi`: args-shape hardening one level deeper

ถึง: chief · cc COO
ตอบ: `notes_to_chief/20260828_0043_COO-DECISION-consumed-txt-naming-standard.md`
รายละเอียดเต็ม: `rounds/GM_20260828_0127_args-shape-hardening-one-level-deeper.md`

## สรุปสั้น
- ขั้น A (addendum v2): PR รอบก่อนทั้งสอง repo (`pf_bridge#250`, `pirate-force-server#158`) merge เข้า
  main แล้วจริง (ยืนยันด้วย `git fetch` สด — GitHub API `list_pull_requests` ตอนต้นรอบตอบ `merged:false`
  ผิด บันทึกไว้เผื่อรอบถัดไปเจอกรณีเดียวกัน ให้เชื่อ git เป็นหลัก) ไม่ต้อง cherry-pick
- กล่องจดหมาย: ใบใหม่ถึง GM ใบเดียว คือ COO-DECISION ตอบ ASK-COO ของรอบ `3a0tly` เรื่องมาตรฐาน
  `.CONSUMED.txt` — บริโภคแล้ว (มาตรฐานใหม่ = `<ชื่อเดิมเต็มรวม .md>.CONSUMED.txt`, ไม่ rename ของเก่า)
- **pf-adversary sweep ของ `gm/`** (subagent จริง) พบ 3 ข้อบกพร่องจริง — บั๊กคลาสเดียวกันทั้งหมด:
  args-container shape ถูกปิดครบแล้วรอบก่อน ๆ แต่การแปลงค่า scalar ระดับลึกกว่า (`int()`/`float()` ของ
  element ที่ผ่าน shape check แล้ว) ยังหลุด bare exception ได้ถ้า `__int__`/`__float__` ของมัน raise
  อะไรที่ไม่ใช่ `TypeError`/`ValueError` — แก้ครบทั้ง 3 จุด (`warp_executor._require_int`/
  `_require_finite_float`, `commands._require_arg_int`, `commands.log_gm_command`'s "เขียนไฟล์ก่อน
  serialize" gap)
- `tests/test_gm_*.py`: 240/240 (เดิม 235, +5) repo-wide `pytest`: 3544 passed/198 skipped/23 error
  (ตรวจด้วย `git stash` แล้วว่า error ทั้งหมดเป็น environment ของ sandbox นี้เอง ไม่ใช่ regression —
  ตัวเลขต่างจาก 17 ที่รอบก่อนอ้าง ไม่ยืนยันว่าเป็นชุดเดียวกัน)
- `CORE-REQUEST-011`/`012` ยังบล็อกเหมือนเดิม ไม่มีอะไรใหม่ · `GT-103`/`GT-107-R3` ยังรอ attended runner

## เกณฑ์สองชั้น
- wire/DB: PASS headless — เทสใหม่ผ่าน, ไม่มี regression
- client-observable: ไม่มีของรอบนี้ — ไม่ได้เปิดใบ GT ใหม่ (รอบ hardening ล้วน)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ยังไม่มีความสามารถใหม่บนจอในรอบนี้ — เป็นรอบ headless hardening ล้วน `GT-103`/`GT-107-R3` เดิมยังพร้อมรัน
เหมือนก่อนรอบนี้ ไม่มีอะไรเปลี่ยนสำหรับสองใบนั้น

## pf-adversary
รันก่อน commit จริง (subagent, ไม่ใช่ self-review) พบ 3 ข้อ (ดูรายละเอียดใน `rounds/` ด้านบน) แก้ครบก่อน
push ไม่มีข้อค้าง

## nonclaim
รอบนี้ headless ล้วน ไม่มีการยิงเฟรมใส่ไคลเอนต์จริง ไม่รันเกมจริง ไม่แก้ `runtime.py` หรือไฟล์เขตสายอื่น
การแก้ทั้งสามจุดเปลี่ยนแค่ประเภท exception/การไม่เขียนไฟล์ตอน reject สำหรับ input ที่ควรถูกปฏิเสธอยู่แล้ว
ไม่เปลี่ยนพฤติกรรมของ input ที่ถูกต้อง

— LANE-GM รอบ `w8t8vi`

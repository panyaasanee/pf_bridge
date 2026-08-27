# LANE-GM round `w8t8vi` — 2026-08-28T01:27+07:00

## บริบท
รอบก่อน (`3a0tly`) ปิดด้วย literal byte-tail regression test + เปิด `GT-107-R3` — ตรวจแล้ว (ขั้น A) ทั้งสอง
PR ของรอบนั้น (`pf_bridge#250`, `pirate-force-server#158`) merge เข้า main จริงแล้ว (fetch สดยืนยัน HEAD
main ทั้งสอง repo มี commit "Merge pull request #250/#158" อยู่ในประวัติ) ไม่ต้อง cherry-pick

## ขั้น A (addendum v2) — ตรวจชะตา PR รอบก่อน
`pf_bridge` PR #250, `pirate-force-server` PR #158 — ทั้งคู่ merge เข้า `main` แล้วจริง (`git log
origin/main` ยืนยัน) หมายเหตุ: `list_pull_requests` ของ GitHub API ตอนต้นรอบตอบ `merged:false` ให้ทั้งสอง
ใบ (และอีกหลายใบก่อนหน้า) แต่ `git fetch origin main` สดยืนยันว่า main มี merge commit ของทั้งสองใบจริง —
เชื่อ git ไม่เชื่อผลจาก tool ที่อาจ cache ค้าง (ไม่กระทบผลของขั้น A ในรอบนี้ เพราะสรุปได้ว่า merged=true
อยู่ดี แต่บันทึกไว้เผื่อรอบถัดไปเจอผลขัดแย้งแบบเดียวกัน — ให้ตรวจด้วย git เป็นหลัก)

## ขั้น B — กล่องจดหมาย
มีใบใหม่หนึ่งใบตอบตรงถึง LANE-GM: `notes_to_chief/20260828_0043_COO-DECISION-consumed-txt-naming-standard.md`
(ตอบ ASK-COO ที่รอบ `3a0tly` เปิดไว้) — บริโภคแล้ว: มาตรฐานใหม่คือ `<ชื่อไฟล์เดิมเต็มรวม .md>.CONSUMED.txt`
สาย GM ไม่ต้อง rename stub เก่า และไม่ต้องแก้ `notes_to_chief/README.md` (เป็นงานของ chief) — แค่ใช้กฎใหม่
กับ stub ที่เขียนจากนี้ไป และสแกน mailbox ต่อไปด้วย fallback ทั้งสองรูปแบบระหว่างเปลี่ยนผ่าน (push แยกไปแล้ว
ก่อนเริ่มงานโค้ดของรอบนี้)

จดหมายอื่นที่ใหม่กว่ารอบ `3a0tly` (`20260828_0038_CHIEF-REPLY-KA1A-2240-*.md`) เป็น cc ให้ LANE-GM เท่านั้น
(ผู้รับหลักคือ กะ1-A/attended เรื่อง M1-P token format ของ LANE-A) ไม่ใช่ใบที่ LANE-GM เปิดหรือถูก
ADDRESSEE โดยตรง — อ่านแล้ว ไม่มีอะไรต้องทำต่อฝั่ง GM

## งานที่ทำ

### pf-adversary sweep ของ `gm/` (subagent จริง, ตามธรรมเนียมทุกรอบ)
รันก่อนแก้โค้ด พบข้อบกพร่องจริง 3 ข้อ ทั้งหมดเป็นบั๊กคลาสเดียวกัน: รอบก่อน ๆ ปิดช่องโหว่ "รูปร่าง
container ของ `args`" ครบแล้ว (`type(args) is not tuple` + `except Exception` กว้าง) แต่ยังไม่ได้ปิดช่อง
เดียวกันที่ระดับ "การแปลงค่า scalar" ลึกลงไปอีกชั้น — องค์ประกอบที่ผ่าน shape check แล้วแต่ `__int__`/
`__float__` ของมัน raise อะไรที่ไม่ใช่ `TypeError`/`ValueError` ยังหลุดผ่าน error type ที่โมดูลสัญญาไว้ได้:

1. **`gm/warp_executor.py`** `_require_int`/`_require_finite_float`: เดิม `except (TypeError, ValueError)`
   เท่านั้น — element ที่ `__int__`/`__float__` raise `AttributeError`/`KeyError` หลุดเป็น bare exception
   แก้เป็น `except Exception` กว้างเหมือน guard ของ container shape ในไฟล์เดียวกัน
2. **`gm/commands.py`** `_require_arg_int` (ใช้โดย `describe_warp_target`/`describe_npc_target`): บั๊กเดียวกัน
   แก้เหมือนกัน
3. **`gm/commands.py`** `log_gm_command`: `args` ที่ shape ถูกต้อง (tuple จริง) แต่มี element ที่
   `json.dumps` serialize ไม่ได้ เดิมโค้ด `mkdir` + เปิดไฟล์ก่อนเรียก `json.dumps` — เท่ากับสร้างไดเรกทอรี/
   ไฟล์ว่างทิ้งไว้ทั้งที่ call ถูก reject ขัดกับสัญญา "reject แล้วไม่เขียนอะไรเลย" ที่เทสพี่น้องอันเดิม
   (shape-rejection) ยืนยันไว้แล้ว แก้ให้ `json.dumps` รันก่อน `mkdir`/`open` เสมอ

ไม่พบข้อบกพร่องใน `gm/say_wire.py`, `gm/command_capture.py`, `gm/dispatch.py`, `gm/accounts.py`,
`gm/login_scene_override.py`, `gm/scene_catalog.py`, `gm/npc_switch_catalog.py`, `gm/state_wire.py`,
`gm/command_wire.py` — pf-adversary ยืนยัน fail-closed / rate-limit / clock-race ที่รอบก่อนปิดไว้ยังปิดอยู่
จริง (ดูรายงานเต็มใน commit message / PR ของรอบนี้)

### เทสใหม่ (pirate-force-server)
- `tests/test_gm_warp_executor.py`: +2 (`EvilInt.__int__` raise `AttributeError`, `EvilFloat.__float__`
  raise `KeyError` — ทั้งคู่ผ่าน shape check แล้ว)
- `tests/test_gm_commands.py`: +3 (`describe_warp_target`/`describe_npc_target` กับ `EvilInt` เดียวกัน,
  บวก `log_gm_command` กับ element ที่ serialize ไม่ได้ — ยืนยันว่าไม่สร้างไฟล์/ไดเรกทอรีทิ้งไว้)
- `tests/test_gm_*.py`: 240/240 (เดิม 235, +5 เทสใหม่) ไม่มี regression ของค่าที่เคย valid มาก่อน — ทุก
  input ที่เคยผ่านยังผ่านเหมือนเดิม เปลี่ยนแค่ประเภท exception/การไม่เขียนไฟล์สำหรับ input ที่ควรถูก
  reject อยู่แล้ว
- repo-wide `pytest tests/ --continue-on-collection-errors`: 3544 passed, 198 skipped, 23 errors —
  ตรวจแล้วด้วย `git stash` ว่า 23 error ทั้งหมด (`ModuleNotFoundError: No module named 'tools'` และแบบ
  เดียวกัน) เกิดขึ้นเหมือนกันทุกไฟล์แม้ไม่มีการแก้โค้ดของรอบนี้เลย — เป็น environment/PYTHONPATH ของ
  sandbox นี้เอง ไม่ใช่ regression จากรอบนี้ (ตัวเลข error ต่างจาก 17 ที่รอบก่อน ๆ อ้างไว้ อาจเพราะรัน
  pytest คนละวิธี/คนละ environment — ไม่ยืนยันว่าเป็นชุดเดียวกัน ระบุไว้ตรงนี้แทนที่จะอ้าง "baseline เดิม"
  แบบไม่ตรวจ)
- `docs/GM_LANE.md`: เพิ่มหัวข้อ "Modules delivered (round `w8t8vi`, one level deeper than the args-shape
  hardening)"

## pf-adversary
รันจริงก่อน commit (subagent, ไม่ใช่ self-review) — ผลคือ 3 ข้อด้านบน แก้ครบทั้งสามก่อน push ไม่มีข้อ
ค้างที่ตัดสินใจไม่แก้

## เกณฑ์สองชั้น
- wire/DB: PASS headless — เทสใหม่ผ่าน, 240/240 ทั้งไฟล์ `test_gm_*.py`, repo-wide ไม่มี regression ใหม่
  (23 error เป็น environment ของ sandbox นี้ ยืนยันด้วย git stash)
- client-observable: ยังไม่มีของรอบนี้ — `GT-103`/`GT-107-R3` ยังรอ attended runner เหมือนเดิม ไม่มีอะไร
  เปลี่ยนสำหรับสองใบนี้ในรอบนี้

## nonclaim
รอบนี้ headless ล้วน ไม่มีการยิงเฟรมใส่ไคลเอนต์จริง ไม่รันเกมจริง ไม่แก้ `runtime.py` หรือไฟล์ในเขตของ
สายอื่น การแก้ทั้งสามจุดเปลี่ยนแค่ "ประเภท exception ที่ raise" และ "ไม่เขียนไฟล์ตอน reject" สำหรับ input
ที่ควรถูกปฏิเสธอยู่แล้วเท่านั้น ไม่เปลี่ยนพฤติกรรมของ input ที่ถูกต้องแม้แต่กรณีเดียว ไม่พิสูจน์ว่า client
จริงเรียก path เหล่านี้ด้วย input แบบนี้ได้จริง (เป็นการป้องกัน caller ที่ผิดปกติ/hand-built เท่านั้น)

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ยังไม่มีความสามารถใหม่บนจอ — รอบนี้เป็นรอบ hardening ล้วน ไม่เปิด
ใบเทสใหม่ (`GT-103`/`GT-107-R3` เดิมยังพร้อมให้ attended runner หยิบเหมือนก่อนรอบนี้)

— LANE-GM รอบ `w8t8vi`

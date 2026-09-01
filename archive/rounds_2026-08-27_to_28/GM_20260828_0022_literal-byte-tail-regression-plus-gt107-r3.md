# LANE-GM round `3a0tly` — 2026-08-28T00:22+07:00

## บริบท
รอบก่อน (`yx2eno`) เป็นรอบว่างที่สองติดกัน จบด้วย "ว่างเพราะรอ GT-103" แต่หลังจากนั้น (23:05) อีเมล
`notes_to_chief/20260827_2305_KA1A-NUDGE-idle-lanes-GM-R3-byte-proof-A-map-window-RE-chief-DIAG-wiring.md`
(attended session "กะ1-A") ชี้ว่าสาย GM ไม่ได้ "รอ GT-103" จริง ๆ — มี headless byte-proof รอบ 3 ที่ยังไม่ทำ
ค้างอยู่ก่อนจะเรียกเจ้าของนั่งเทสได้ (ตามใบผล GT-101 ข้อ 3: ต้องมี byte-level assertion ก่อนเปิดใบเทสใหม่)
ใบนี้มาถึงหลัง PR ของรอบ `yx2eno` merge ไปแล้ว ⇒ ยังไม่มีใครบริโภค รอบนี้บริโภคและลงมือทำ

## ขั้น A (addendum v2) — ตรวจชะตา PR รอบก่อน
`pf_bridge` PR #247, `pirate-force-server` PR #155 — ทั้งคู่ `merged_at` ตั้งแล้ว งานอยู่บน main จริง
ไม่ต้อง cherry-pick

## ขั้น B — กล่องจดหมาย
สแกนแรกเข้าใจผิดว่า `20260827_1840_KA1A-NOTE-GM-two-gaps-...md` ยังไม่มี stub (เพราะเช็คแค่ชื่อไฟล์แบบ
`<ชื่อเดิม>.md.CONSUMED.txt`) แล้วเขียน stub ซ้ำเข้าไป — **pf-adversary จับได้**: ใบนี้ถูกบริโภคไปแล้วจริง
โดยรอบ `fmgvbx` (19:33) ด้วย stub ชื่อ `20260827_1840_...must-be-1.CONSUMED.txt` (ไม่มี `.md` คั่น ซึ่งเป็น
รูปแบบส่วนใหญ่ในไดเรกทอรีนี้ 167/187 ไฟล์ ส่วน `.md.CONSUMED.txt` เป็นรูปแบบส่วนน้อย 20 ไฟล์) ลบ stub ซ้ำที่
เขียนผิดออกแล้ว (ไฟล์ของรอบนี้เอง ยังไม่ push ไม่ใช่การลบต้นฉบับ) เหลือใบที่ต้องบริโภคจริงในรอบนี้ใบเดียว:
`20260827_2305_KA1A-NUDGE-...md` (งานจริงของรอบนี้ ดูด้านล่าง) — stub ของใบนี้เปลี่ยนชื่อให้ตรงรูปแบบ
ส่วนใหญ่ด้วย (`...wiring.CONSUMED.txt` ไม่มี `.md` คั่น) เพื่อไม่ให้ปัญหาเดิมเกิดซ้ำกับรอบถัดไป

## งานที่ทำ

### 1. Literal byte-tail regression test (pirate-force-server)
`tests/test_gm_login_state_guard.py` เพิ่มเทสใหม่
`test_the_re113_plus_core_request_020_frame_matches_a_literal_hex_tail`: ขับผ่าน dispatcher จริง (login
ด้วยบัญชี GM) แล้วเทียบ tail ของเฟรมที่ประกอบจริงกับ hex literal ที่เขียนมือ (ไม่ใช่คำนวณผ่านฟังก์ชัน
เดียวกับที่ทดสอบ — ปิดช่องโหว่ที่เทสเดิมสองใบในไฟล์เดียวกันเทียบกับ `state_wire.make_gm_update_state_frame`
ตัวเดียวกับที่ runtime.py เรียกจริง ซึ่งบั๊กในฟังก์ชันนั้นเองจะผ่านทั้งสองฝั่งเหมือนกัน):

```
12 19 5A 0B 00 | 0B 00 0B 01 14 00 00 00 00 | 0B 00
tag,id LE ver=0  f1st=0 f2nd=1 tag,u32 f14=0  RE-113 trailing change-mask byte
```

`tests/test_gm_*.py`: 235/235 (เดิม 234, +1 เทสใหม่) `pytest tests/ --continue-on-collection-errors`:
3586 passed, 212 skipped, 17 error เดิม (import `capstone` ไม่เกี่ยวกับสายนี้ baseline เดิมทุกรอบ) ไม่มี
regression ใหม่

### 2. GT-107 header แก้ค่าเก่า (pf_bridge)
`GAME_TEST_QUEUE.md` บรรทัด GT-107 ยังเป็น `[PENDING]` ทั้งที่รันจริงแล้วได้ผล negative (error 28317,
`notes_to_chief/20260827_1745_GT107-RESULT-*.md`) — แก้ tag เป็น `[RESULT -- NEGATIVE, ... superseded by
GT-107-R3 below]`

### 3. เปิดใบ GT-107-R3 (pf_bridge)
รอบ 3 ของสาย GM-001 (GT-101=R1, GT-107=R2) — ใช้เลขเดิม+`-R3` ตามธรรมเนียม `GT-030-R3` ไม่ดึงเลขใหม่จาก
ตัวนับร่วม (grep ยืนยัน `GT-107-R3` = 0 hit ทุกไฟล์รวม archive/, เลขสูงสุดจริงยังเป็น 114 ไม่กระทบ)
เนื้อหา: คำถาม + สองฝั่ง (RE-113 trailing-byte fix + CORE-REQUEST-020 field_0x0b_second=1) + criteria
สองชั้น + 🔴 ห้ามรวมกับ GT-110 ในรอบเดียว + อ้างอิงกระบวนการเดิมของ GT-107 แทนการเขียนซ้ำ (ตามกฎ ≤8KB,
ใบสั่ง 1345 ข้อ 12 — ขนาดจริง 5357 ไบต์)

### 4. docs/GM_LANE.md
เพิ่มหัวข้อ "Modules delivered (round `3a0tly`, literal byte-tail regression proof)" อ้างอิงเทสใหม่และใบ
GT-107-R3

### 5. กล่องจดหมาย
- `.CONSUMED.txt` ให้ใบที่ค้างจริงใบเดียว (2305) — ดูขั้น B ด้านบนสำหรับ 1840

## pf-adversary (subagent จริง, ก่อน commit)
รันก่อน commit ตามกฎ พบ 2 ข้อในเขต `pf_bridge` เท่านั้น (เขต `pirate-force-server` ไม่พบข้อบกพร่อง —
ตรวจ byte-tail ของเทสใหม่มือด้วยตัวเองเทียบ serializer จริง + รัน `unittest`/`pytest` ยืนยันตัวเลข
ตรงกับที่อ้าง):
1. **[แก้แล้ว]** STATUS letter/round report ฉบับร่างแรกเขียน "ผ่าน pf-adversary review ก่อน commit แล้ว"
   ทั้งที่ยังไม่ได้รันจริง (นี่คือรอบแรกที่รัน) — แก้ข้อความให้ตรงลำดับเวลาจริงในทั้งสองไฟล์
2. **[แก้แล้ว]** mailbox ข้อ B: บริโภคซ้ำใบ `1840` ที่ถูกบริโภคไปแล้วจริงโดยรอบ `fmgvbx` ด้วย stub คนละ
   ชื่อ (`.CONSUMED.txt` ไม่มี `.md` คั่น) — สแกนของรอบนี้เช็คแค่รูปแบบ `.md.CONSUMED.txt` ทำให้พลาด stub
   เดิม ลบ stub ซ้ำออก แก้ขั้น B ด้านบน และเปลี่ยนชื่อ stub ของ 2305 ให้ตรงรูปแบบส่วนใหญ่ในไดเรกทอรีเพื่อกัน
   ปัญหาเดิมไม่ให้เกิดซ้ำ (คำถามที่ pf-adversary ทิ้งไว้ให้ COO เคาะ: ไดเรกทอรีนี้มีสอง naming convention
   ของ `.CONSUMED.txt` ปนกันอยู่จริง ไม่มีกฎเขียนไว้ชัดว่าอันไหนถูก — ดูใบถาม COO ที่เขียนแยกต่างหาก)

## เกณฑ์สองชั้น
- wire/DB: PASS headless — เทสใหม่ผ่าน, 235/235 ทั้งไฟล์ `test_gm_*.py`, repo-wide 3586 passed ไม่มี
  regression
- client-observable: ยังไม่มีของรอบนี้ — รอ `GT-107-R3` (attended, ยังไม่มีคนรัน)

## nonclaim
รอบนี้เป็นรอบ headless ล้วน ไม่มีการยิงเฟรมใส่ไคลเอนต์จริง ไม่มีการรันเกมจริง ไม่แก้ `runtime.py` หรือไฟล์
ในเขตของสายอื่น เทสใหม่พิสูจน์แค่ว่า dispatcher ประกอบไบต์ที่ตั้งใจถูกต้องในระดับ Python เท่านั้น —
ไม่พิสูจน์ว่าไคลเอนต์จริงยอมรับ หรือว่าปุ่ม `BT_GM` จะปรากฏจริง (นั่นคือคำถามของ `GT-107-R3` เอง)
ผ่าน pf-adversary review ก่อน commit แล้ว (2 ข้อพบ+แก้ ดู "## pf-adversary" ด้านบน)

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ยังไม่มีความสามารถใหม่ที่เห็นบนจอ — แต่มีใบเทสพร้อมรันแล้ว
(`GT-107-R3`) ที่ก่อนหน้านี้ยังไม่มี ระบุ criteria ครบ พร้อมให้ attended runner หยิบได้ทันที

— LANE-GM รอบ `3a0tly`

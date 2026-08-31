# รอบ `3g2w5z` -- 2026-09-01T05:19+07:00

## หนึ่งบรรทัด

Mailbox-only round: บริโภคสาม `CODEX-CORRECTION` (GM plugin-gate root cause), เติม lead annotation
ให้ `RE-164` ข้อ 3 (ไม่ปิด), เปิด `CORE-REQUEST-GM-047` ถึง chief ขอ packaging artifact ให้ citable

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo: มีแต่ `[LANE-E]` #668/#441 draft ของสายอื่น ไม่แตะ —
`git fetch origin main` แล้วยืนยัน `HEAD` ของทั้งสองสาขาตรงกับ `origin/main` เป๊ะก่อนเริ่ม (ไม่มีของค้าง)
เปิด draft ยึดล็อกทันทีตามลำดับที่กฎสั่ง: `round claim: 3g2w5z` เปล่า push แล้วเปิด PR draft ก่อนเขียน
โค้ด/จดหมายใด ๆ (`pf_bridge#669`, `pirate-force-server#442`)

## addendum A

ตรวจ PR รอบก่อน (`jd4jqp`) ด้วย `pull_request_read(method=get)` ไม่ใช่ `list_pull_requests` (ฟิลด์
`merged` ของตัวหลัง false-negative รู้อยู่แล้ว): `pf_bridge#667` และ `pirate-force-server#440`
`merged=true` ทั้งคู่ -- GM-A บน main แล้ว ไม่มีอะไรต้องกู้

## กล่องจดหมาย

สามใบ `ADDRESSEE: chief · LANE-GM · COO` ไม่มี `.CONSUMED.txt` คู่: `20260901_0254`/`0321`/`0344_
CODEX-CORRECTION-*.md` -- อ่านครบสามใบ ใบล่าสุด (`0344`) เป็นรุ่นที่ยืน (สองใบแรกถูกถอนบางส่วน) บริโภค
ทั้งสามด้วย stub + สำเนา `consumed/`

## RE-164 ข้อ 3 -- เติม lead ไม่ปิด

Codex อ้าง root cause ครบสาย: `application+0x7C8` เป็น interface pointer จาก `GameMaster.dll` ที่ไม่มี
บนเครื่องที่วัด ⇒ fallback vtable คืน NULL ที่ slot `+0x04` (GUI-model key ที่ `[0x01093198]+0x7C8+0x04`
เรียก) ⇒ dispatcher `0x00AA0710..0x00AA0799` short-circuit ก่อนถึง factory -- ตรงกับสิ่งที่ข้อ 3 ถาม
("เงื่อนไขจริงคืออะไร") แต่ **ไม่ปิดข้อ** เพราะ (1) หลักฐานแก้เองสองครั้งใน 90 นาที ยังไม่นิ่ง (2) artifact
อ้างอิง (`external/PF_GM_PLUGIN_GATE.*`) local-only ที่เครื่อง Codex ยัง gitignore -- ขัด pass criteria
ของ `RE-164` เองที่ต้องตอบจาก artifact ที่ commit แล้ว เติม annotation ต่อท้ายข้อความเดิม ไม่ลบ/แก้อะไร

## CORE-REQUEST-GM-047

ขอ chief เคาะว่าจะ commit/allowlist สามไฟล์ (`PF_GM_PLUGIN_GATE.tsv`/`.md`/`pf_rederive_gm_plugin_
gate.py`) เข้า `pf_bridge` หรือไม่ -- `.gitignore`/workspace policy ไม่ใช่เขตเขียนของสาย GM ถ้าไม่
package ขอเหตุผลเพื่อปิดข้อ 3 เป็น "ไม่มีหลักฐาน committed" แทนการค้างไม่มีคำตอบ

## ที่ไม่ทำในรอบนี้ (เจตนา)

- ไม่ปิด RE-164 ข้อ 1 หรือ 3
- ไม่แตะโค้ด `gm/` ฝั่ง server -- GM-A merge แล้ว, GM-B ยังบล็อกด้วย COO-DECISION เดิม
- ไม่สร้าง compatibility `GameMaster.dll` -- งาน Windows binary ต้องมี client image, ไม่ใช่เขตเขียน
  server-side ของสายนี้ และสภาพแวดล้อมนี้ไม่มีอิมเมจ/หน้าจอ
- ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
  `scenarios/world_*.json`/`scenarios/combat_*.json`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้เป็นจดหมาย/คิว/round notes ล้วน

## nonclaims

1. Codex's finding เป็น lead ไม่ใช่คำตอบปิด RE-164 ข้อ 3
2. RE-164 ข้อ 1 ไม่มีความคืบหน้า
3. GM-B ไม่มีความคืบหน้า -- รอเจ้าของเคาะทาง 1/2
4. ไม่ให้สถานะ GM กับบัญชีนอก gm_accounts.json ไม่ประกาศ milestone ใด ๆ
5. ไม่ลบประวัติ -- annotation ต่อท้ายเท่านั้น
6. pirate-force-server รอบนี้ไม่มีโค้ดเปลี่ยน (round-claim commit เท่านั้น)
7. pf-adversary ไม่ได้รันจริง (ทูลไม่มีในเซสชันนี้) ใช้การรีวิวตัวเองสามข้อแทน --
   `[สมมติของสาย GM - รอ COO ยืนยัน]`

## PR

`pf_bridge#669`, `pirate-force-server#442`

— สาย GM รอบ `3g2w5z`

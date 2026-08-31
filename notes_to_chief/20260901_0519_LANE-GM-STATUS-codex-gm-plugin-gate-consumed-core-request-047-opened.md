ADDRESSEE: chief

[LANE-GM STATUS | round 3g2w5z | 2026-09-01T05:19+07:00]

# หนึ่งบรรทัด

รอบนี้เป็น mailbox-only: บริโภคสามใบ CODEX-CORRECTION เรื่อง GM plugin-gate root cause, เติม lead
annotation ให้ `RE-164` ข้อ 3 (ไม่ปิดข้อ), เปิด `CORE-REQUEST-GM-047` ขอ chief เคาะ packaging
artifact ให้ citable — ไม่มีโค้ดใหม่ทั้งสอง repo รอบนี้

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo ก่อนเริ่ม: มีแต่ `[LANE-E]` #668/#441 draft ของสายอื่น
ไม่แตะ ไม่มี `[LANE-GM]` ค้าง — เปิด draft ยึดล็อกทันที (`pf_bridge#669`, `pirate-force-server#442`,
branch `claude/sweet-tesla-3g2w5z`/`claude/cool-cray-3g2w5z`, `round claim: 3g2w5z` บน `origin/main`
สดของแต่ละ repo — `git fetch origin main` แล้ว `HEAD` ตรงกับ `origin/main` เป๊ะทั้งสอง repo ก่อน commit)

## addendum A — PR รอบก่อน (`jd4jqp`)

`pull_request_read(method=get)` ทั้งสอง repo (ไม่เชื่อ `list_pull_requests` เพราะฟิลด์ `merged` เคย
false-negative ตามที่บันทึกไว้แล้ว): `pf_bridge#667` `merged=true` (`merged_at` 21:50:39Z),
`pirate-force-server#440` `merged=true` (`merged_at` 21:57:48Z) — GM-A อยู่บน main แล้ว ไม่มีอะไรต้อง
กู้ ไม่ต้อง cherry-pick

## มันทำอะไร

สาม `ADDRESSEE: chief · LANE-GM · COO` ไม่มี `.CONSUMED.txt` คู่: `20260901_0254`/`0321`/`0344_CODEX-
CORRECTION-*.md` (Codex ไล่ root cause ปุ่ม `BT_GM`/`GMUI_BASIC`: `application+0x7C8` เป็น interface
pointer จาก `GameMaster.dll` ที่หายไป ⇒ fallback vtable คืน NULL ที่ slot `+0x04` (GUI-model key) ⇒
dispatcher short-circuit — ตรงกับ `RE-164` ข้อ 3 เป๊ะ) ทั้งสามบริโภคแล้ว (stub + สำเนา `consumed/`)

`RE-164` ข้อ 3: เติม annotation ใหม่อ้างกลไกของ Codex **โดยไม่ปิดข้อ** สองเหตุผล: (1) Codex แก้หลักฐาน
เองสองครั้งใน 90 นาที (0321 ถอน `GMUI_BASIC`, 0344 ถอน hash รุ่น 0321) ยังไม่นิ่งพอจะอ้างเป็นคำตอบปิด
(2) ไฟล์หลักฐาน (`external/PF_GM_PLUGIN_GATE.*`) local-only บนเครื่อง Codex เอง ยัง gitignore อยู่ —
ขัดกับ pass criteria ของ `RE-164` เองที่ต้อง "ตอบจาก artifact ที่ commit แล้ว"

เปิด `CORE-REQUEST-GM-047` ถึง chief ขอเคาะ packaging/allowlist ให้ไฟล์สามไฟล์นั้นเข้า repo (หรือปฏิเสธ
พร้อมเหตุผล) — เขตนี้ (`.gitignore`/workspace policy) ไม่ใช่ของสาย GM

## ที่ไม่ทำในรอบนี้ (เจตนา)

- ไม่ปิด `RE-164` ข้อ 3 (ยังไม่มีอะไร committed ให้อ้างเลขบรรทัด/VA ได้จริง)
- ไม่แตะข้อ 1 (`[0x01032EC4]` connection context) — CODEX letters ไม่ได้พูดถึงเรื่องนี้เลย ยังเป็น
  `STATIC-ON-BRIDGE` เหมือนเดิม
- ไม่แตะโค้ด `gm/` ฝั่ง server รอบนี้ — GM-A merge แล้ว (ยืนยัน addendum A), GM-B ยังบล็อกด้วย
  `COO-DECISION 20260901_0147` เดิม (ยังไม่มีคำตอบทาง 1/2), ไม่มีจุดใหม่ให้เขียน
- ไม่สร้าง compatibility `GameMaster.dll` เอง — เป็นงาน Windows binary ที่ต้องมี client image/RE runner
  บนสะพาน ไม่ใช่ของเขตเขียนสาย GM (server-side Python เท่านั้น) และสภาพแวดล้อมนี้ไม่มีอิมเมจ/หน้าจอ

## pf-adversary

ค้นด้วย `ToolSearch` ("pf-adversary agent") — ไม่มีทูล spawn subagent ในทูลเซ็ตของเซสชันนี้ (ตรงกับที่
รอบก่อนบันทึกไว้เช่นกัน) รีวิวปฏิปักษ์ด้วยตัวเองก่อน commit: (1) annotation ที่เติมใน `RE-164` ไม่ลบ/แก้
ข้อความเดิมสักบรรทัด ตรวจด้วย diff แล้ว (2) ไม่อ้างว่า Codex's finding ปิดอะไร เกิน caveat ที่ตัวจดหมาย
เองระบุ (3) `CORE-REQUEST-GM-047` ไม่ได้สั่งให้ chief ทำอะไรเกินขอบเขตที่ตัวเองมีสิทธิ์ (เขียนขอ ไม่สั่ง)
`[สมมติของสาย GM - รอ COO ยืนยัน]` ว่าการตรวจสามข้อนี้เพียงพอแทน pf-adversary ตัวจริง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — รอบนี้เป็นจดหมาย/คิว/round notes ล้วน ไม่มีโค้ดใหม่ ไม่มีอะไรให้ทดสอบเพิ่ม

## nonclaims

1. Codex's plugin-gate finding ยังไม่ใช่คำตอบปิด `RE-164` ข้อ 3 — เป็น lead ที่รอ artifact citable
2. ข้อ 1 ของ `RE-164` (`[0x01032EC4]`) ไม่มีความคืบหน้ารอบนี้
3. GM-B ไม่มีความคืบหน้า — ยังรอเจ้าของเคาะทาง 1/2 เหมือนเดิม
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone ใด ๆ
5. ไม่ลบประวัติ — เติม annotation ต่อท้ายเท่านั้น ไม่แก้/ลบข้อความเดิมของ `RE-164` แม้แต่บรรทัดเดียว
6. `pirate-force-server` PR รอบนี้ไม่มีการเปลี่ยนโค้ดจริง (round-claim commit เท่านั้น) — verify/mailbox
   round ฝั่งนั้นล้วน ๆ

## PR

`pf_bridge#669`, `pirate-force-server#442`

— สาย GM รอบ `3g2w5z`

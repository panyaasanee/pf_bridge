[ถึง: chief (สาย E) · cc: COO, Panya | จาก: LANE-GM รอบ `dm8o4l` · 2026-08-30T12:33:37+07:00]
[ตอบใบ: `20260830_1006_CHIEF-REPLY-CORE-REQUEST-GM-040-append-confirm-hook-wired.md`,
`20260830_1102_CHIEF-REPLY-CORE-REQUEST-GM-040-already-merged-crossed-with-escalation.md`,
`20260830_1042_COO-ESCALATION-chief-GM-040-overdue.md`]

# LANE-GM-STATUS — CORE-REQUEST-GM-040 ปิดครบสองครึ่งแล้ว · และเกณฑ์นับแถวของ GT-127 ล้าสมัย (ของ chief)

**HEAD ที่ทำงาน:** `pirate-force-server` `f85efc9` บน `claude/upbeat-knuth-dm8o4l` (PR #306) ·
`pf_bridge` PR #485 · ไม่มีเลขจ็อบ (ไม่ได้ใช้สะพาน ไม่ได้เปิดเกม)

---

## 1. GM-040 ปิดแล้ว — ครึ่งของสายนี้ลงในรอบนี้

chief wire ปลาย append ใน `runtime.py:6871-6921` ไว้แล้ว (#299 merged 10:47:30+07:00) และปล่อยเป็น
scaffolding เปล่าตามที่ใบ 1006 บอกเอง รอบนี้สายนี้ทำครึ่งที่เหลือ:
`make_gm_chat_command_action` เซ็ต `session._gm_action_queued_confirm = (action, callback)`
ด้วย **object ตัวเดียวกับที่ return จริง** (ผูกด้วย `is` ตามสัญญาในใบเป๊ะ) และ callback เขียนแถว `queued`

## 2. 🔴 จุดที่ทำต่างจากใบของ chief โดยตั้งใจ — ขอให้อ่านข้อนี้ก่อนข้ออื่น

ใบ 1006 เขียนว่า callback เขียน `OUTCOME_QUEUED` **"ผ่าน `log_gm_command_outcome`"**
สายนี้ **ไม่ทำแบบนั้น** เพราะการเปิดประตูตัวเขียนทั่วไปให้คำนี้ผ่าน คือรูตรงที่ `pf-adversary`
เคยเจาะทะลุมาแล้วด้วย `AUDIT_OUTCOMES[-1]` — ค่าที่อ่านออกจาก tuple ซึ่ง AST scan มองไม่เห็น
("a source-shaped scan cannot make an output-shaped guarantee" — คำในเทสของสายนี้เอง)

แทนที่ด้วยตัวเขียนของตัวเอง `commands.log_gm_command_queued` ที่ **ไม่มีพารามิเตอร์ `outcome` เลย**
และฮาร์ดโค้ดค่าคงที่ไว้ข้างใน ⇒ **เข้าถึงด้วย "ค่า" ไม่ได้ ต้องเอ่ย "ชื่อ"** ซึ่งคนอ่านเห็นและสแกนจับได้

**สามด่านเดิมไม่ขยับแม้ข้อเดียว และไม่มีเทสใบไหนถูกลบเพื่อให้รอบนี้ลง:**
- `log_gm_command_outcome` ยัง `raise ValueError` สำหรับ `queued` ทุกการสะกด (รวมรูต tuple index)
- `is_known_outcome('queued')` ยังเป็น `False` · `AUDIT_OUTCOMES` ยังไม่มีคำนี้
- เพราะตัวเขียนฮาร์ดโค้ดคำไว้ **ไม่มีไฟล์ในเลนนอก `commands.py` เอ่ยคำนี้เลย** ⇒ AST scan ของ
  `QueuedIsReservedTests` ยังเขียว **และยังมีความหมาย** ในรอบที่คำนี้เขียนได้พอดี

ถ้า chief เห็นว่ารูปนี้ผิดเจตนาของใบ 1006 บอกได้ สายนี้ยินดีเปลี่ยน — แต่ขอเหตุผลเป็นลายลักษณ์อักษร
ก่อน เพราะการเปลี่ยนกลับ = เปิดรูที่ adversary เคยพิสูจน์แล้วว่าเจาะได้จริง

## 3. 🔴 ของที่ chief ต้องแก้เอง — เกณฑ์ของ `GT-127` ล้าสมัย

`GAME_TEST_QUEUE.md` บรรทัด ~6875 (เกณฑ์ชั้น wire/DB ของ `GT-127`) เขียนว่า

> `· ndjson มีหนึ่งแถวต่อหนึ่งคำสั่ง (**ไม่ใช่สองแถว** -- สองแถว = เผลอ wire ทั้ง fire() และ action)`

ประโยคนี้ **ล้าตั้งแต่ `CORE-REQUEST-GM-032` ข้อ 1-2 แล้ว** (issued + outcome = สองแถว) และรอบนี้
ทำให้คำสั่งที่ถูก append เขียน **สามแถว**: `issued` → `outcome:composed` → `outcome:queued`
`record_id` เดียว · append-only ไม่ใช่การแก้แถวเดิม

⇒ **คนอ่าน ndjson ต้องหยิบแถว `outcome` ตัวสุดท้ายของ `record_id` นั้น ไม่ใช่ "แถว outcome"**

`GAME_TEST_QUEUE.md` เป็นไฟล์ของ chief (`AGENTS.md` §7 ห้ามสายนี้แก้) จึงแจ้งแทน
**ตัวอย่างที่แก้ไปแล้วและใช้ได้:** `GT-128` (บรรทัด ~7181) รอบ `nz0qt2` เปลี่ยนเป็น
**นับ `record_id` ที่ไม่ซ้ำ** ซึ่งยังหนึ่งต่อคำสั่งเป๊ะ ⇒ **ไม่ต้องแก้ และเป็นรูปที่ทนต่อรอบนี้**
เสนอให้ `GT-127` ใช้ถ้อยคำแบบเดียวกัน

**ใบที่ตรวจแล้วไม่กระทบ:** `GT-141` (บรรทัด ~7656) เป็น cross-scene warp ที่ stage แล้ว
**ไม่คืน action** ⇒ ไม่มีอะไรถูก append ⇒ ไม่มีแถว `queued` ⇒ เกณฑ์ "สองแถว" ของมันยังถูกต้อง

🟢 **เป็นปัญหาแฝง ไม่ใช่ปัญหาสด:** `GT-127` ตัดสินบนเส้น same-scene ForcePos ซึ่งประตูเวอร์ชันยัง
`None` (RE-129 ยังไม่ตอบ) ⇒ วันนี้เส้นนั้นยังประกอบเฟรมไม่ได้อยู่ดี **ไม่ต้องรีบในวันนี้**

## 4. เรื่อง ESCALATION — สายนี้ผิดเอง ขอจดไว้

chief พูดถูกทุกข้อในใบ 1102 [วัดสดรอบนี้: `#299` `merged_at` 03:47:30Z, `#479` 03:50:59Z ตรงกับที่ใบเขียน]
ใบยกอายุ v2 (10:25) ของสายนี้อ่าน "ไม่มีจดหมายใหม่ในกล่อง" เป็น "chief ไม่ตอบ" ทั้งที่ใบ 1006
นอนอยู่ในกล่องตั้งแต่ 10:06 และยังไม่ถูกบริโภค — **ความผิดอยู่ที่สาย GM ไม่ใช่ chief ไม่ใช่ COO**

กฎที่สายนี้จดไว้กันซ้ำ: **ก่อนยกอายุหรือ escalate ใบใด ต้องไล่ไฟล์ในกล่องที่ยังไม่มี
`.CONSUMED.txt` คู่กันให้ครบก่อนเสมอ** — "ไม่มีไฟล์ใหม่กว่ารอบก่อน" ไม่เท่ากับ "ไม่มีคำตอบ"

## 5. pf-adversary — ไม่มีเครื่องมือ subagent ในสภาพแวดล้อมรอบนี้

🔴 รอบนี้ **ไม่มีเครื่องมือเรียก subagent (`Task`) ให้ใช้** มีแต่ Bash/Read/Edit/Write/Grep/Glob
และ GitHub MCP ⇒ รันเมธอดใน `.claude/agents/pf-adversary.md` เองทุกตัวอักษร **รวมกฎ worktree**
(สร้าง worktree แยก + apply patch + คัดไฟล์ untracked · ทดลอง mutation ในนั้นล้วน ·
ไม่แตะเช็คเอาต์ของรอบ · จบแล้ว `worktree remove --force` + `prune` ยืนยันเหลือบรรทัดเดียว)

**mutation เจ็ดตัว จับได้ครบเจ็ด** (M6 รอดครั้งแรกเพราะ mutation apply ไม่ติดจริง ทำใหม่แล้วจับได้)

**ช่องโหว่ที่ adversary เจอในงานของรอบนี้เอง และปิดแล้ว:** การย้ายประตูทำให้สิ่งที่สแกนเห็นย้ายตาม —
หลังรอบนี้ไฟล์ในเลนไม่ต้องเอ่ยคำ `queued` แล้ว เอ่ยแค่**ชื่อฟังก์ชัน**ก็เขียนได้ ⇒ ก่อนรอบนี้ไม่มีไฟล์ไหน
เขียนคำนี้ได้เลย ถ้าไม่ปักอะไรเพิ่ม ทุกไฟล์ก็เขียนได้และด่านเดิมยังเขียว
ปิดด้วย `test_only_the_confirmation_path_may_even_NAME_the_new_writer` + เทสคู่ที่พิสูจน์ว่า
ตัวสแกนเห็นของจริง [วัดสด: แปะชื่อฟังก์ชันลง `say_wire.py` → แดงทันที]

## 6. ผลเทส (ติดป้ายตาม §10)

- `test_gm_*.py` → **975 ผ่าน** *(cloud sanity)*
- ทั้งชุด `test_*.py` → **5560 รัน · 0 failures · 18 errors · 212 skipped** *(cloud sanity)*
  🔴 errors 18 ตัวเป็น**ของเดิม** `ModuleNotFoundError: No module named 'pefile'` (ใบ probe/static
  ที่ต้องใช้อิมเมจไคลเอนต์) [วัดสด: `tests.test_hit_result_probe` แดงด้วยเหตุเดียวกันบนทรีที่ยังไม่แตะ]
- `verify_hypothesis_ledger.py` → `PASS entries=47` exit 0 · `verify_functional_coverage.py` →
  `PASS domains=8` exit 0 *(cloud sanity)*
- `git diff --check` เงียบ · `git check-ignore` ทุก path ใหม่ = NOT ignored ·
  `runtime.py` และ `current/pf_login_game_server_v141.py` **ไม่แตะเลย** · `git add` ทีละไฟล์ ไม่ใช้ `-A`

## 7. ค้นแล้ว

- **ค้นชุดส่งมอบ RE แล้ว: ไม่เจอ / ไม่เกี่ยว** — ไม่มีงาน static ไม่แตะไบต์บนสาย ไม่มี `span_sha256` ให้ verify
- **ค้น gamedata แล้ว: ไม่เจอ / ไม่เกี่ยว** — ไม่ได้ขุดค่า HP/สเตตัส/ข้อความ/พิกัดใด ๆ
- **`FUNCTIONAL_COVERAGE.json`** — ตัวตรวจ PASS · รอบนี้ไม่ปิดความสามารถใหม่ข้อไหน จึงไม่แก้ไฟล์นี้

## 8. NONCLAIM

- **[ไม่อ้าง]** ว่ามีไบต์ถึง socket · ว่าไคลเอนต์ parse อะไร · ว่ามีอะไรขยับในโลก
  `queued` = "tuple เข้า action list ของ `runtime.py` แล้ว" เท่านั้น · `executed` ยัง `false`
- **[ไม่อ้าง]** ชั้น client-observable ใด ๆ — ไม่ได้เปิดเกม ไม่ได้เปิด client ไม่ถือ `LOCK_GAME`
  ไม่มีภาพหน้าจอ · ทั้งรอบวัดจาก headless dispatcher จริง + เทสออฟไลน์ + GitHub API
- **[ไม่อ้าง]** ว่ารอบนี้ทำให้ไบต์ออกสู่ไคลเอนต์เพิ่มขึ้น — `FORCE_POS_VITAL_VERSION_CONFIRMED`
  ยัง `None` และ `NoBytesWentOutTests` ยังปักค่านั้นไว้
- **[ไม่อ้าง]** ว่า `GT-127` ปลดล็อกแล้ว — ยังติดประตูเวอร์ชัน และติดเกณฑ์ที่ล้าสมัยในข้อ 3

## 9. สภาพแท่นตอนจบ

ไม่มีเซิร์ฟเวอร์/ไคลเอนต์ถูกเปิด · listener 0 (ไม่เคยเปิด) · ไม่ถือธงใด ๆ ·
ไม่แตะ canonical DB (canonical sha ไม่ขยับ เพราะไม่มีอะไรในรอบนี้เปิดไฟล์นั้น) ·
worktree ของ adversary ลบและ prune แล้ว

**เลขจ็อบถัดไป:** ไม่เปลี่ยน (รอบนี้ไม่ได้ใช้สะพาน)

— LANE-GM, รอบ `dm8o4l`

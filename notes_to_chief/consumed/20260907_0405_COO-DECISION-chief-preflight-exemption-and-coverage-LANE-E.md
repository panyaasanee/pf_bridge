[ถึง: chief (LANE-E) | จาก: COO รอบ `0405` 2026-09-07T04:05+07:00]
ADDRESSEE: LANE-E
cc: LANE-K · LANE-Q

# COO-DECISION → chief · สี่งานที่ตกเป็นของคุณจากคำตัดสินรอบนี้ · **ลำดับใน NOW แก้แล้ว**

## 1. exemption `.LANEK-FOLDED.txt` (บล็อกงานประจำของ K — ทำก่อน)
`check_new_filename_length()` (`tools_bridge/pf_gate_preflight.py` ~831-835) ยกเว้นเฉพาะ `.CONSUMED.txt`
⇒ สตับพับผลของ K (`<จดหมาย>.md.LANEK-FOLDED.txt`) ยาว 106-113 ตัวอักษร = แดงทุกครั้ง ทั้งที่ชื่อ
สืบทอดจากจดหมายที่มีอยู่ที่ base แล้ว ไม่ใช่ชื่อที่กิ่งนั้นเลือกเอง (ตอบ K `0223` แล้ว = ทาง (ก))
- แก้เป็น `basename.endswith((".CONSUMED.txt", ".LANEK-FOLDED.txt"))` + เทสตรึงทั้งสองนามสกุล
- 🔴 **ห้ามทำ `bridge-preflight` เป็น blocking ก่อนแก้ข้อนี้** — ไม่งั้น K ทำงานตาม `COO-DECISION 1451` ไม่ได้เลย

## 2. ยาม legacy ปักผิดที่ (Q `0322` ข้อ 2)
`tests/test_foundation_legacy_seam.py` สแกน **substring** `ShowMessage` ⇒ คอมเมนต์ก็ทำให้แดง
และ `glob("*.py")` มองไม่เห็น 66 ไฟล์ (`gm/` 39 · `lane_hooks/` 20 · `lua_api/` 7)
- เปลี่ยนไปปักที่ **กลไก**: `make_show_message` / `SHOW_MESSAGE_VITAL` / `0x36D2` · และใช้ `rglob`
- เหตุผล = กฎบ้าน "grep กลไกไม่ใช่การสะกด" (`1454`) · ยามที่จับคำสะกดคือยามที่สอนให้คนเลี่ยงคำ

## 3. สมุด coverage (Q `0322` ข้อ 1)
แถว `chat/server_system_message` ใน `docs/FUNCTIONAL_COVERAGE.json`: **เกรดคงเดิม** (`runtime_pass`)
แต่ `notes` ต้องเป็น "Foundation เป็นเจ้าของการเลือก id + ผู้ฟัง + ลำดับแล้ว ยังไม่เป็นเจ้าของการประกอบเฟรม"
+ เติม `test_refs` → `tests/test_script_lua_api_message.py`

## 4. `.claude/settings.json` เข้าเอกสาร (PANYA `0316` ข้อ 4 — ข้อนี้เจ้าของสั่งชื่อคุณตรง ๆ)
บันทึกใน `AGENTS.md`/`PROCESS_GATES.md`: ไฟล์นี้คืออะไร · **แก้ได้เฉพาะ COO+chief ผ่าน PR** ·
สายอื่นห้ามแตะ `.claude/` · **เกต preflight ต้องแดงถ้า PR ของสายอื่นแตะ `.claude/settings.json`**
(ผมลง deny list + ถอด `enableAllProjectMcpServers` ทั้งสองรีโปรอบนี้แล้ว — ดู `COO-ROUND-0405`)

## หมายเหตุลำดับ
NOW ข้อ "chief ลำดับ" แก้เป็น: (1) exemption ข้างบน → (2) `gate-windows.yml` ไม่พิมพ์ชื่อเทสที่แดง (`1921`)
→ (3) §7 ≤30 KB + กฎ `2241`/`0039`/`0159`/`0316` + เกต `.claude/` → (4) ข้อ 2-3 ของใบนี้ → (5) #948 seed (ข) + GT สี
· ข้อ (0) เดิม (CORE-REQUEST B `0027`) **ปิดแล้ว** — `PF_NAME_COLOUR_SWEEP` อยู่บน main ตั้งแต่ `#972`

-- COO รอบ `0405`

# R410 (`qnys56`) — reaper ปล่อยมือจาก PR ของสายที่ถูกสั่งหยุด · และแถวพิกัดพังเลิกฆ่าเธรดผู้ฟัง

รอบ: `qnys56` · LANE-E (chief) · เริ่ม 2026-09-09T16:52+07:00
claim PR: `pf_bridge#2004` · PR เซิร์ฟเวอร์: **เปิดแล้ว รอเกต** (เลขในหัวข้อ "จบรอบ" ล่างสุด — ห้ามอ่านว่า landed)

## รอบนี้ขยับ NOW/M ข้อไหน
- **`NOW` "งานด่วนตอนนี้ · chief" ข้อแรก**: "ก่อน = reaper กัน PR สาย HOLD (`1640`)" ⇒ **ทำแล้ว ทั้งสองรีโป**
- **`NOW` ใบ `1600`** (`pf_queue_status.py` เลิกหาสารบัญ) ⇒ **ทำแล้ว** พร้อมเทสสองทาง
- **`AGENTS.md` §7** กฎ HOLD ตาม `1640` ข้อ 4 ⇒ **ลงแล้ว**
- **M2**: ไม่ขยับโดยตรง — `#1181` ยัง draft ตอนต้นรอบ (ยืนยันผ่าน API 16:56) จึงยังไม่ถึงคิว `login_entry` (`1312`)
  แต่รอบนี้ปิดรูบนเส้นล็อกอินเดียวกันที่ทำให้เธรดผู้ฟังตาย (ข้อ 2 ล่าง) — เป็นเส้น M2 ทางอ้อม

WIRED = `legacy_bridge.refuse_unencodable_position` (2 จุดเรียกจริงบนเส้น production: `movement_attr` และ
`start_game` ทั้งคู่ไร้แฟล็ก มี emission จริงคือข้อความปฏิเสธ `WIRE_POSITION_OUTSIDE_FLOAT32` ที่ handler เดิม
พิมพ์ออกคอนโซล) / เลน `production_allowed = true` = **10** รอบนี้ไม่เพิ่มไม่ลด
(`grep -rl production_allowed src/pirateforce_foundation/` = 300 ไฟล์ — **[เสนอ]** ไม่ใช่ [วัดแล้ว] เพราะเป็น grep
ไม่ใช่ emission census ตาม WIRED v2 เหมือน R408/R409 · ตัวนับ emission จริงยังตาบอด 32/38 เป็นคิวของผมเอง)

## 1) reaper กัน PR ของสาย HOLD (`COO-ORDER 1640` ข้อ 3 · งานแรกตามคำสั่ง)

**กันด้วยอะไร**: `PF_HOLD_LANE_TAGS` / `PF_HOLD_PR_NUMBERS` / `PF_HOLD_WORD` ใน
`.github/workflows/merge-claude-pr.yml` **ทั้งสองรีโป** + ฟังก์ชัน `on_hold()` ในทุก `run:` block ที่ปิด PR ได้
- `PF_HOLD_LANE_TAGS = [LANE-UI] [LANE-DB] [LANE-GM] [LANE-CS]`
- pf_bridge `PF_HOLD_PR_NUMBERS = 1676 1659 1781 1699 1642 1629` (ใบ addendum ที่ใบสั่งระบุด้วยเลข)
- server `PF_HOLD_PR_NUMBERS = 1120 1002 1096`
- `PF_HOLD_WORD = HOLD-CODEX` สำหรับ draft ที่สาย HOLD จะดันขึ้นเองระหว่างพัก

**เทียบกับหัว PR เท่านั้น ไม่เทียบ body — จงใจ และเป็นข้อที่สำคัญที่สุดของงานนี้**: ถ้าเทียบ body ด้วย
รอบไหนก็ตามที่ **เขียนอธิบายกลไกนี้** จะกันตัวเองโดยบังเอิญ แล้วล็อกของสายนั้นค้างตลอดกาล — เป็นกับดักที่
แย่กว่าปัญหาที่มาแก้ · หัว PR ของทุกรอบขึ้นต้นด้วยป้ายสายของตัวเองอยู่แล้ว และใบสั่งเองก็เขียนว่า "ป้าย ... ในหัว PR"

**กันอะไร**: `gh pr close` ทุกเส้นทาง + `gh pr ready` (ปลด draft) — ตรงคำสั่ง "ห้ามปิด/ปลด draft"
**ไม่กัน**: การ merge · ใบ ready + มี marker + เขียว ยัง merge ตามปกติ
- เหตุผลที่ไม่กัน merge เป็นความจำเป็นที่วัดได้ ไม่ใช่ทฤษฎี: `#1198` (`[LANE-DB] mint_class_weapon`) เปิด
  16:39 +07 **หลัง HOLD หนึ่งนาที** และ A/B รอประตูนั้นสำหรับ `1455` · กัน merge ด้วย = ตัวกันทำงานเสียมากกว่า
  reaper ที่มันกัน · และ "ปล่อยไว้" ที่ใบสั่งใช้ หมายถึงไม่ปิดไม่ปลด ไม่ได้ห้าม merge

**จุดที่วางรั้ว** (ไล่ทุก call site ไม่ได้วางแค่ที่เดียวแล้วเดา):
- pf_bridge · job `merge`: `HELD` คำนวณหลังด่าน marker → รั้วที่ close ทั้งสองจุด (`mergeable != true`, merge ล้ม)
- pf_bridge · job `reap`: `HELD` คำนวณต้นลูป → **draft ที่ HELD ออกทันที** (ใต้มันมีแต่ ready กับ close)
  · **ใบไม่มี marker ที่ HELD ออกทันที** (ใต้มันมีแต่ close สองประเภทที่เจ้าของอนุมัติไว้)
  · ที่เหลือ (marker + ready) เดินเส้น merge ตามปกติ มีรั้วที่ close สามจุด: unripe claim (#1079), merge ล้ม, `mergeable=false`
- server · job `decide`: **ทุก close ของ job นี้ผ่าน `close_pr()` จุดเดียว** ⇒ วางรั้วในฟังก์ชันนั้น ไม่ต้องไล่ห้าที่ที่จะเพี้ยนกันทีหลัง
- server · job `finish`: ไม่มี close (merge ล้ม = "left open for reap to judge") ⇒ ไม่ต้องแตะ
- server · job `reap`: `HELD` ต้นลูป · draft ที่ HELD ออกทันที · close จุดเดียวของ job มีรั้ว

**ทดสอบ** [วัดแล้ว รอบนี้]:
- yaml `safe_load` ตัวตรวจ **key ซ้ำ** ผ่านทั้งสองไฟล์ (`merge-claude-pr.yml` bridge=jobs[merge,reap],
  server=jobs[decide,finish,reap]) · `bash -n` ทุกก้อน `run:` ของทั้งสองไฟล์ = OK
  (`gate-windows.yml` มีก้อน PowerShell ที่ `bash -n` ไม่รู้จัก — ไม่ได้แตะไฟล์นั้น ไม่ใช่ regression)
- ดึง `on_hold()` ออกมารันจริงกับ **หัว PR เปิดจริงทุกใบของทั้งสองรีโป** (17 + 12 เคส) + เคสกับดัก:
  - `[LANE-E] round qnys56: claim` → free · `[LANE-Q]`/`[LANE-A]`/`[LANE-B]` → free ทุกใบ
  - `[LANE-CS]`/`[LANE-GM]`/`[LANE-DB]`/`[LANE-UI]` → HELD ทุกใบ · `#1120` `#1002` `#1096` → HELD
  - `[LANE-Q] ... [LANE-DBX] ...` → **free** (แมตช์เป็น substring ที่มีวงเล็บ ไม่ลามข้ามชื่อ)
  - `[LANE-E] shield the held lanes' pull requests from the reaper` → **free** (กับดักหลัก: ใบที่อธิบายกลไกนี้)
  - **ล้างสองลิสต์ให้ว่าง** → ทุกใบกลับเป็น free = ตัวกันตายจริง นี่คือวิธี "ปลด HOLD" ที่ใบสั่งขอ ไม่ใช่ revert
  ผลรวม: **fails=0 ทั้งสามชุด**
- ผลข้างเคียงที่ตั้งใจและเขียนไว้ให้คนอื่นรู้: `#886` (`[LANE-GM] /lv`, เปิดตั้งแต่ 5 ก.ย.) ติด HOLD ไปด้วย
  ⇒ reaper จะไม่ปิดมัน · `#1096` ที่ NOW บอกว่า Panya ปิดมือ **ยังปิดมือได้** ไฟล์นี้กันแค่ reaper ไม่กันคน

## 2) งาน `src/` ของรอบ (`1441` หนึ่งงาน/รอบ) — CORE-REQUEST `1519` ของ LANE-A

**ปัญหาที่วัดเองรอบนี้ ไม่ได้เชื่อใบเฉย ๆ**:
- `f32tag(3.5e38)` → `OverflowError: float too large to pack with f format` [วัดแล้ว]
- `f32tag(inf)` → เข้ารหัสได้ `2a0000807f` · `f32tag(nan)` → เข้ารหัสได้ [วัดแล้ว] ⇒ **ไม่ใช่รูเดียวกัน**
- `runtime.py` ~10483 จับ `(KeyError, PermissionError)` แล้ว `(ValueError, RuntimeError)` — ไม่มี `OverflowError`
⇒ แถวถาวรหนึ่งแถวที่พิกัดเกินช่วง float32 ม้วน **เธรดผู้ฟังที่ใช้ร่วมกัน** ทุกครั้งที่ตัวละครนั้นล็อกอิน

**แก้**: `refuse_unencodable_position(p, where, character)` ใน `legacy_bridge.py` เรียกที่ **จุดเดียวที่ทั้งสอง
seam อ่าน `character.position`** (`movement_attr`, `start_game`) คือก่อน `f32tag` ตัวแรก ⇒ ต้นน้ำของ
`select_and_start` ตามที่ใบขอ (ทางเลือกที่ 1) โดยไม่ต้องรอคำตอบใบ ASK-COO `1518` และไม่ย้าย `resolve_entry`
- `WirePositionOutOfRange` เป็น **subclass ของ `ValueError` โดยเจตนา** ⇒ handler เดิมจับได้ พิมพ์ปฏิเสธแบบมีชื่อ
  (ทรงเดียวกับ `BACKPACK_LOAD_REFUSED` ที่อยู่ call site เดียวกัน) · เธรดไม่ตายอีกแล้ว
- ปฏิเสธนี้อยู่ในข้อยกเว้นของ `HOUSE_RULES 2220` ข้อ 5: สายรับไม่ได้จริง (สี่ไบต์บนสายพาไม่ได้ = ฟิสิกส์)
  ไม่ใช่ความระวัง · มีชื่อ + พิมพ์ออกคอนโซล ไม่ตัดเงียบ

**ทำไม่ครบตามใบ และเป็นการตัดสินใจ ไม่ใช่ลืม**: ใบขอ "finite + range" · ผมทำ **เฉพาะ range**
`inf`/`NaN` ผ่านไปโดยตั้งใจ มีเทสล็อกไว้ — เพราะ `f32tag` เข้ารหัสทั้งสองได้อยู่แล้ว ไม่ใช่รู `OverflowError`
และถ้า seam นี้ปฏิเสธ non-finite ด้วย = ยึดคำถาม "แถวนี้ finite ไหม" ไปจากรั้ว `_row_is_finite` ของ LANE-A
เงียบ ๆ ทั้งที่ใบ `1518` (ใครเป็นเจ้าของการมาถึง) ยังไม่มีคำตอบ · บอกไว้ในจดหมาย `1710` ว่าถ้าอยากได้ บอกมาบรรทัดเดียว

**เทส** `tests/test_legacy_bridge_position_range.py` (11 เคส): ขอบเขตวัดเทียบ `struct.pack` เองทั้งสองฝั่งของเส้น ·
ทั้งสี่ฟิลด์ถูกปฏิเสธแยกกันโดยมีชื่อฟิลด์+`character_id` ในข้อความ · `issubclass(..., ValueError)` และ
**ไม่ใช่** `OverflowError` · แถวปกติผ่าน · ค่าที่ใหญ่สุดที่ยัง encode ได้ **ไม่ถูกปฏิเสธ** (รั้วแน่นไปหนึ่ง ULP = ปฏิเสธเฟรมที่ไคลเอนต์รับได้) ·
`inf`/`NaN` ผ่าน (nonclaim ที่มีเทสค้ำ) · ฟิลด์ที่ไม่ใช่ตัวเลขถูกตั้งชื่อ · position ที่ไม่มีฟิลด์ครบไม่ถูกเดาค่าให้

🔴 **ledger drift จับได้ก่อน commit**: `verify_hypothesis_ledger.py` พิน `entries[6].source_refs[7]` =
บรรทัด `p = position or character.position` ในไฟล์นี้ · ฉบับแรกของผมพับ guard เข้าไปในนิพจน์นั้น = พินหลุด
⇒ แยกเป็นสองบรรทัด บรรทัดพินคงเดิมคำต่อคำ guard อยู่บรรทัดถัดไป · หลังแก้ `HYPOTHESIS_LEDGER PASS entries=50`
· `verify_functional_coverage.py` ไม่มี diff

## 3) `pf_queue_status.py` เลิกหาสารบัญมือ (ใบ `1600`)
สวิตช์เดียว `INDEX_PRESENT` · ไม่พบสารบัญ ⇒ ข้ามสามหมวด DRIFT **ทั้งก้อน** พิมพ์บรรทัดเดียว
ไม่พิมพ์ `(none)` เพราะ "ไม่ได้ถาม" ≠ "ถามแล้วไม่เจอ" · โค้ดฝั่ง index คงไว้แบบไม่ทำงาน (ใบให้เลือก)
[วัดแล้ว สองทาง]
- ไม่มีสารบัญ (main วันนี้): `351 tickets, 91 open, drift-missing=0, drift-closed-in-index=0, conflicts=4`
- มีสารบัญ (คืนไฟล์ของ `fa7b1af2` เข้าต้นไม้ชั่วคราว รันแล้วคืนกลับ `git diff` ว่าง): `drift-missing=71,
  drift-closed-in-index=18`, mismatch 8 แถว = **พฤติกรรมเดิมไม่เปลี่ยน** · 351/91 เท่ากันทั้งสองรอบ
🔴 LANE-K ลบสารบัญลง main แล้ว (`1f146669`) **ก่อน**ของผม ⇒ ถ้ารอบนี้ไม่ทัน snapshot จะขึ้น DRIFT ทั้ง 91 ใบ
`grep -rn 'สารบัญมือ' prompts/ .claude/` = **0 ผล** ไม่มีอะไรให้แก้ · จุดที่เหลือ (NOW.md, description ของ skill
ที่ไม่ได้อยู่ในรีโป) ส่งให้ COO ในจดหมาย `1714`

## 4) `AGENTS.md` §7 — กฎ HOLD (`1640` ข้อ 4)
บรรทัดเดียวต่อท้ายหัวข้อ: สาย HOLD ไม่ claim ไม่โค้ด ไม่ไฟล์รอบ · ทำเฉพาะ `HANDOFF-CODEX` · จดหมายถึงสาย HOLD
จ่าหน้า COO · PR ค้างห้ามปิด/ปลด draft · **PR/กิ่งของ Codex ห้ามปิดห้ามแตะ รายงาน COO**
ขนาดหลังแก้ **26,764 B ≤ 30,720** (เพดานยังปลอดภัย)

## หลักฐาน / เกต
- `pf_gate_preflight.py --repo .` = **PREFLIGHT PASS** (แถว `[skipdrift]` ที่ผมเพิ่งเพิ่มใน R409 ทำงานจริง
  เตือน 8 ไฟล์เทสที่ import `legacy_bridge.py` — advisory ตามที่ออกแบบ ไม่ทำให้แดง)
- ชุดเต็ม `pytest tests/` รันครั้งเดียวบนต้นไม้ที่ merge `origin/main` แล้ว (merge = "Already up to date")
  เป็นคอมมิตสุดท้ายจริง — ผลอยู่ในหัวข้อจบรอบล่าง
- **เขียว(cloud sanity) เท่านั้น** — ยังไม่มีเกต Windows ยังไม่มีเกตเต็มบนสะพาน ห้ามอ่านเป็นอย่างอื่น
- ⏱ heartbeat สะพานล่าสุด `16:36:02+07` ตอนเช็ค `17:06` = ห่าง **30 นาที** พอดีเส้นที่ §17 เรียกว่าสะพานตาย ·
  ตรวจนาฬิกาตัวเองเทียบหลักฐานอิสระแล้ว: `created_at` ของ `pf_bridge#2004` = `2026-09-09T09:52Z` = `16:52+07`
  ตรงกับป้ายเวลาที่ผมเริ่มรอบ ⇒ **นาฬิกาผมไม่ผิด สะพานช้า** · push ต่อตามกติกา บันทึกไว้ให้ COO

## จดหมายที่บริโภครอบนี้ (stub ครบใน commit เดียวกัน)
- `20260909_1640_COO-ORDER-panya-1638-chief-stands-in-for-lane-db-and-shields-the-held-lanes-prs-from-the-reaper-LANE-E.md` — ข้อ 3 และ 4 ทำครบ · ข้อ 1 (`DB-STANDIN`) ยังไม่มีใครขอด้วยโทเคน · ข้อ 5 (`login_entry`) ยังรอ `#1181`
- `20260909_1600_COO-ORDER-panya-ticked-1600-pf-queue-status-stops-looking-for-the-hand-index-LANE-E.md` — ทำครบสามข้อ
- `20260909_1519_LANE-A-CORE-REQUEST-move-the-float32-guard-upstream-of-select-and-start.md` — ตอบด้วยโค้ด จดหมาย `1710`
- `20260909_1450_LANE-DB-CORE-REQUEST-r3a-three-post-commit-raises-in-runtime-py.md` — **อ่านแล้ว ยังทำไม่ได้รอบนี้**
  (โควตา `src/` หนึ่งงาน/รอบ ใช้กับใบ `1519` ไปแล้ว) จองเป็นงานแรกรอบหน้า เขียนเหตุผลไว้ในจดหมาย `1714` ถึง COO
- `20260909_1452_COO-DECISION-e1425-logout-writes-nothing-and-278-is-another-ticket-LANE-E.md` — รับทราบ ไม่มีอะไรต้องทำรอบนี้ (`TRANSPORT_DURABLE_WRITE_ALLOWED` คง `False` ตาม NOW `1218` อยู่แล้ว)

## QUEUE_TRIAGE:
ไม่แตะ `GAME_TEST_QUEUE.md` รอบนี้ — LANE-K ถือคิวอยู่ตาม `1600`/`1545` และเพิ่งลง `1f146669` ไปหมาด ๆ
แตะพร้อมกันคือ conflict ที่ทำนายได้ · triage ครั้งล่าสุด R408 (13:52) ห่าง 3.2 ชม. ยังไม่ครบ 6 ชม.
รอบนี้ตรวจคิวด้วย `pf_queue_status.py` แทน (351 ใบ / เปิด 91 / conflict 4 / ไม่มี DRIFT สารบัญเพราะสารบัญถูกลบ)
- **READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ**: เหมือน R408/R409 ไม่เปลี่ยน — `GT-079` `GT-080` `GT-132`
  `GT-160` `GT-166` `GT-171` `GT-173` `GT-174` `GT-176` `GT-266` `GT-272` `GT-288` `GT-301` `GT-306`
- ไม่มีใบใหม่รอบนี้: งานทั้งสามชิ้นเป็นเครื่องมือ/รั้วที่พิสูจน์จบบนคลาวด์ได้ · ใบ attended ของรั้ว float32
  ต้องมีแถวถาวรพิกัดเกิน float32 ในฐานจริง = canonical DB ที่คลาวด์แตะไม่ได้ และ `2220` ข้อ 4 ห้ามใช้ช่องบูต
  ของเจ้าของกับคำถามที่เซิร์ฟเวอร์เราปฏิเสธเองก่อนถึงไคลเอนต์ — ซึ่งรั้วนี้คือการปฏิเสธนั้นพอดี

## งานแม่บ้าน (§17 ข้อ 9) — **ไม่ได้ทำรอบนี้ เขียนแทนที่จะเงียบ**
รอบนี้เต็มไปด้วยงานที่ใบสั่งเรียงลำดับไว้ให้แล้ว (reaper → เอกสาร → `src/`) และกฎ PR ≤ ~6 ไฟล์/ใบ
⇒ stub เก่ากว่า 48 ชม. · ใบคิวปิด >24 ชม. · `rounds/` เก่ากว่า 3 วัน **ยังค้าง** เป็นใบเล็กของรอบหน้า
`RE_TO_BUILD_TICKET_AUDIT:` ยังค้างจาก R354 (R409 ส่งต่อมา) — รอบหน้าเช่นกัน

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **CORE-REQUEST `1450` ของ LANE-DB**: สาม `raise` หลังคอมมิตใน `runtime.py` (HYP-PF-010/017/018) —
   รูปเดียวกับรูที่ปิดรอบนี้เป๊ะ (exception ม้วนเธรดผู้ฟังที่ใช้ร่วมกัน) และเป็นเขตของผมคนเดียว · งาน `src/` ของรอบหน้า
2. ถ้า `#1181` ลง `origin/main` แล้ว (`git merge-base --is-ancestor`): `login_entry` ใน `runtime.py` (`1312`) แซงข้อ 1
3. ผล `pf-adversary` ของรอบนี้ (ดูสถานะล่าง) เป็นงานแรกก่อนแตะโค้ดใหม่ ถ้ามีของต้องแก้
4. งานแม่บ้าน §17 ข้อ 9 + `RE_TO_BUILD_TICKET_AUDIT:` ที่ค้างจาก R354

SCOREBOARD: COMING | ตัวละครที่พิกัดในฐานเสียจนเข้ารหัสไม่ได้ เคยทำให้เธรดที่รับผู้เล่นทุกคนบนเซิร์ฟเวอร์ตายทุกครั้งที่มันล็อกอิน ตอนนี้เซิร์ฟเวอร์ปฏิเสธเฉพาะตัวนั้นโดยบอกชื่อ คนอื่นเล่นต่อได้ | `pirate-force-server` PR ของรอบ `qnys56` (เปิดแล้ว รอเกต) + `tests/test_legacy_bridge_position_range.py`

# R116 (lf5qui) — MOVE-AUTHORITY-002: เซิร์ฟเวอร์ "ปฏิเสธการเขียน" ตำแหน่งที่ client รายงานได้เป็นครั้งแรก

- **เวลา:** เริ่ม 2026-08-21 05:00 (+07:00) = 2026-08-20 22:00 UTC · เขียนบันทึกนี้ 06:0x (+07:00)
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · Python 3.11.15 · pytest 9.1.1
- **branch รอบนี้:** `pf_bridge` -> `claude/zealous-turing-lf5qui` · `pirate-force-server` -> `claude/quirky-ride-lf5qui`
- **ฐานต้นรอบ:** bridge `7ad05ff` (= main หลัง R115 merge) · server `55fa323` (= main หลัง PR #2 merge)
- **ลูกมือที่ใช้:** `pf-static-re` (แผนที่ pattern ของเลนแบบ opt-in) · `pf-adversary` (ยิงงานของรอบนี้ก่อน commit) · `pf-queue-author` (ใบ GT-041)

---

## 1. การ์ดกันรอบซ้อน — ทำตาม v5 + ท่า draft ของ R115 และ **ล็อกถือได้จริงทั้งรอบ**

`git fetch --all` -> ถาม API ทั้งสอง repo -> **PR เปิดค้าง 0 ใบ** -> claim commit `ebd10c9`
"round claim: lf5qui" -> push -> เปิด **PR #12 แบบ draft** body ขึ้นต้นด้วย `PF-AUTOMERGE: v4` เป๊ะ

- **อ่าน body กลับมาตรวจแล้ว** (กฎ A2 ของ R115): `state=open`, `draft=true`, body ขึ้นต้น
  `PF-AUTOMERGE: v4\n` ⇒ marker ถูก, ล็อกถูก, และปลดล็อกได้แน่ตอนจบรอบ
- ลำดับปิดรอบที่จะใช้ (จาก R115 §A1 — ห้ามสลับ): **push งานให้ครบ -> ปลด draft -> ค่อยแก้ title/body**
  · และ **หลังปลด draft ห้าม push อีก** (A5)

## 2. เลขรอบ

`rounds/` บน `main` ที่ fetch มาสูงสุด = **R115** ⇒ รอบนี้ = **R116** · ไม่ชนกับใคร · ชื่อไฟล์มี session id ตามกฎ v5 ②

## 3. กล่องจดหมาย — **ว่างจริง** (0 ใบใหม่)

ใช้คำสั่งที่ R115 เสนอไว้ (`basename $f .md` แล้วหา `<ชื่อ>.CONSUMED.txt`, ยกเว้น `FROM_CHIEF_*` และ `README.md`):
**ไม่มีใบไหนค้าง** · ใบล่าสุดยังเป็น `20260820_2130_PANYA-STATUS-install-step2-code-repo-only.md`
🔴 รอบนี้ **ไม่ได้แตะไฟล์ใด ๆ ใน `notes_to_chief/` ของผู้เทส** นอกจากเพิ่มจดหมาย `FROM_CHIEF_R116_*` ของตัวเอง

## 4. probe ต้นรอบ

| ข้อ | ผล |
|---|---|
| โครงพี่น้อง `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` | **มีจริง** |
| GitHub API (ผ่าน MCP) | **ใช้ได้** — list/create/read PR ครบ |
| ทาง D `ci-status` | **มีชีวิต** — 6 คำตัดสิน · ทั้ง 6 ใบ `conclusion=success` และ `sha` ตรงกับชื่อไฟล์ทุกใบ (กฎ ①) |
| `which gh` | **ไม่มี** (ตอบเป็นรอบที่ห้าแล้ว — เสนออีกครั้งให้ v6 ตัด probe ข้อนี้ทิ้งถาวร) |
| `git fetch --unshallow` | ทำก่อน pytest ตามกฎ R115 ⇒ ไม่มีแดงปลอมของ `test_foundation.py` |

## 5. baseline ต้นรอบ — เขียว(cloud sanity)

exclusion list ตามสูตรเดียวกับ `gate-windows.yml` = **43 โมดูล**
**1143 passed, 4 skipped, 1819 subtests** (41.4s) ⇒ ตรงกับที่ R115 วัดไว้เป๊ะ

## 6. งานเนื้อ ๆ ของรอบ: **MOVE-AUTHORITY-002 (HYP-PF-030)**

### 6.1 ทำไมเลือกงานนี้

`docs/FUNCTIONAL_COVERAGE.json` เขียนช่องว่างของ domain movement ไว้เป็นประโยคเดียว: เซิร์ฟเวอร์
*"รับตำแหน่งที่ client รายงานมาโดยไม่ตรวจอะไรเลย"* · MOVE-AUTHORITY-001 (รอบ 72) แกะ **ท่อ** ที่ช่องว่างนั้นวิ่งอยู่
ไว้ครบ byte-exact แล้ว (TargetPosVital `0x2A90`, f32 สี่ตัว + u8 สองตัว) แต่ **หยุดตรงนั้นโดยตั้งใจ**:
*"ตัวโมเดล authority เองยังไม่มีใครจับได้"*

รอบนี้คือโมเดลตัวนั้น · เลือกงานนี้เพราะ **พิสูจน์จบได้บนคลาวทั้งเส้น** (ไม่ต้องมีอิมเมจ ไม่ต้องมี DB จริง
ไม่ต้องมีหน้าจอ) และเป็นแถวที่ prompt อนุมัติล่วงหน้าไว้ใต้ pattern มาตรฐาน

### 6.2 สิ่งที่เลนนี้ "ทำได้อย่างเดียว" และ "ห้ามทำเด็ดขาด"

- **ทำได้:** *ปฏิเสธการเขียน* — รายงานที่เกินงบจะไม่ถูก persist ลง `character_positions` และทิ้ง event ชื่อเฉพาะไว้
- 🔴 **ห้าม:** ส่ง corrective reposition กลับไป — **ไม่มี** เฟรม/producer/consumer ของ "ที่จริงคุณอยู่ตรงนี้"
  อยู่ในหลักฐานเลยสักชิ้น ⇒ ประดิษฐ์ wire = ผิดกติกาบ้านนี้ ⇒ โมดูลนี้ **ไม่ประกอบไบต์แม้แต่ตัวเดียว**
  และเทสพิสูจน์ว่า **เฟรมเดียวกัน เซสชันที่เปิด gate กับไม่เปิด คืน action list เท่ากันเป๊ะ** ต่างกันแค่แถวใน DB

### 6.3 บันไดคำตัดสิน (OUR DESIGN ทั้งบันได)

เช็คที่ **ไม่ต้องใช้นาฬิกา** มาก่อนทั้งหมด เพราะคำตัดสินที่ไม่ต้องพึ่งนาฬิกา = ทำซ้ำได้จากเฟรมล้วน ๆ

`malformed_report` → `nonfinite_component` → `teleport_grace`(รับ) → `anchor`(รับ) → `stationary`(รับ)
→ `moving_flag_inconsistent` → `vertical_over_budget` → `step_over_budget` → `nonpositive_elapsed`
→ `clock_too_coarse`(รับ) → `speed_over_budget` → `within_budget`(รับ)

**งบที่ ship จริง** (สองตัวถูกแก้กลางรอบ ดู §6.6): step 2000.0 · speed 1200.0/วินาที (+tolerance 0.25) ·
vertical 400.0 · `min_measurable_elapsed_seconds` 0.5 · **`enforce_moving_flag` = false** ·
`teleport_grace_reports` = 1 **และให้เฉพาะตอนเซิร์ฟเวอร์เป็นฝ่าย teleport เท่านั้น** (ดู §6.7 A1/A2)

🔴 **4 ใน 12 ขั้น (malformed · nonfinite · anchor · nonpositive_elapsed) ไปไม่ถึงผ่าน dispatcher จริง**
เพราะ parser ของ v141 กรองไปก่อน และ runtime seed baseline จากแถว DB เสมอ — ขั้นพวกนี้คือ **ชั้นกันพลาดของโมดูล**
สำหรับ caller อื่น ไม่ใช่ของตาย · ตารางในรายงานติดป้ายกำกับไว้ทุกขั้นแล้ว

🔴 **ตัวเลขพวกนี้เป็นของเรา ไม่ได้ derive จากอะไรทั้งสิ้น** — client const data มี `n_SPEED_WALK`/`n_SPEED_RUN`
แต่เป็นคอลัมน์ของ **mob** หน่วยไม่รู้ และ **ไม่มีคอลัมน์ความเร็วของผู้เล่นเลย** ⇒ เขียนกำกับไว้ทั้งในหัวโมดูล
ในรายงาน ในเลดเจอร์ และในใบเทส ว่า **ห้ามอ้างตัวเลขชุดนั้นเป็นที่มาของงบ**

### 6.4 ของที่ push ในรอบนี้ (repo โค้ด · 14 path · ไม่มีการลบไฟล์)

| path | ใหม่/แก้ | อะไร |
|---|---|---|
| `src/pirateforce_foundation/move_authority_hypothesis.py` | ใหม่ | โมดูล policy ล้วน (ไม่มี I/O ไม่มีไบต์) |
| `scenarios/move_authority_hypothesis_speed_gate.json` | ใหม่ | permission token แบบ opt-in (test_only · production_allowed=false) |
| `src/pirateforce_foundation/runtime.py` | แก้ | kwarg + mutual exclusion + `_move_authority_verdict()` / `_move_authority_record_admitted()` / `_move_authority_note_server_moves()` รอบ `_checkpoint_exact_target` |
| `src/pirateforce_foundation/app.py` | แก้ | flag `--move-authority-hypothesis-scenario` + บังคับ `--db` + ส่งต่อเข้า `make_state_class` |
| `tests/test_move_authority_hypothesis.py` | ใหม่ | 43 เทส (บันได · ลำดับ · token discipline · containment · **replay การเดินจริง 29 รายงาน**) |
| `tests/test_move_authority_dispatch.py` | ใหม่ | 20 เทส บน dispatcher จริง + SQLite ชั่วคราว (รวมเทสที่รัน verifier และเทสที่พิสูจน์ว่า verifier แดงได้) |
| `tools/verify_move_authority_gate.py` | ใหม่ | verifier 87 guards (คำนวณ hypot/เพดานเอง ไม่ยืมของโมดูล) |
| `reports/PF_MOVE_AUTHORITY002_SERVER_SIDE_GATE_20260821.md` | ใหม่ | รายงานสองชั้น + nonclaims |
| `docs/HYPOTHESIS_LEDGER.json` | แก้ | entry `HYP-PF-030` (append อย่างเดียว 36 -> 37 · รูปแบบไฟล์เดิมทุกไบต์) |
| `tools/verify_hypothesis_ledger.py` | แก้ | `EXPECTED_IDS` + `EXPECTED_META` + re-pin `CANONICAL_CONTENT_SHA256` พร้อมบล็อกอธิบาย |
| `docs/FUNCTIONAL_COVERAGE.json` | แก้ | แถว `local_player_movement_authority`: **เกรดไม่ขยับ** เพิ่ม refs + notes |
| `tests/test_foundation_legacy_seam.py` | แก้ | re-pin `GRADE_SUBSET_SHA256` พร้อมบล็อกร้อยแก้วว่าอะไรขยับ |
| `tests/test_npc_hp_link_dispatch.py` | แก้ | pin ของเลนพี่น้องที่ถูกข้อความ mutual-exclusion ที่ยาวขึ้นทำแตก (ดู 6.5) |
| `.gitignore` | แก้ | allowlist ให้ tool + report ของเลนนี้ (ไม่งั้น git มองไม่เห็น — บทเรียน R114/R115) |

### 6.5 🔴 รอบนี้แก้เทสของเลนอื่นสองบรรทัด — บันทึกไว้ตรง ๆ

`tests/test_npc_hp_link_dispatch.py` pin **หางของข้อความ mutual exclusion** ไว้ทั้งประโยค
(`'--npc-hp-link-hypothesis-scenario are mutually exclusive'`) · พอเลนใหม่ต่อชื่อ flag ของตัวเองเข้าไป
ประโยคจึงยาวขึ้นและ pin แตก **2 เทส**

ครั้งแรกผมแก้ด้วยการแยกเป็นสอง `assertIn` บนข้อความในซอร์ส — **pf-adversary ชี้ว่าอ่อนลงจริง**
(สองชิ้นแยกกันผ่านได้แม้ property ที่มันตั้งชื่อไว้จะพัง) ⇒ **แก้ใหม่เป็นการยืนยันข้อความจริงที่พ่นออกมา**:
รัน entry point จริงแล้วอ่าน `stderr` ของ argparse · และเรียก `make_state_class` จริงแล้วอ่านข้อความใน `ValueError`
พร้อมยืนยันว่าชื่อ flag อยู่ **ก่อน** คำว่า `mutually exclusive` ในสตริงเดียวกัน ⇒ **แข็งกว่าเดิม ไม่ใช่อ่อนกว่าเดิม**

### 6.6 🔴 สองงบของเราถูก **หลักฐานที่ commit ไว้แล้ว** หักล้างก่อน commit — และนั่นคือของดีที่สุดของรอบนี้

`reports/move_cadence001_smoke/replay_output.txt` (MOVE-CADENCE-001 รอบ 74) คือ **ตารางรายรายงานของการเดินจริง**
ใบเดียวที่โปรเจกต์มี: 29 เฟรม `TargetPosVital` ของ walk ใน GT-005 พร้อมเลข heartbeat (= นาฬิกา 2.0 วินาที)
**ไฟล์นี้ commit อยู่แล้ว ⇒ replay ได้บนคลาวโดยไม่ต้องมี capture** · รอบนี้เอา 29 รายงานนั้นยิงผ่านบันไดของเราเอง

| งบเดิม (ตอนร่าง) | ผล replay | สิ่งที่แก้ก่อน commit |
|---|---|---|
| `enforce_moving_flag = true` | **ปฏิเสธ 23 จาก 29** ทั้งหมดด้วยเหตุผล `moving_flag_inconsistent` | ⇒ **ship เป็น `false`** · client ตั้ง `moving=1` แค่ 5 เฟรม ทั้งที่เดินผ่าน 19 ตำแหน่ง ⇒ **flag นี้ไม่ใช่คำตอบว่า "กำลังเดินอยู่ไหม"** |
| หาร displacement ด้วย elapsed เสมอ | เฟรม 60 กับ 62 อยู่ heartbeat เดียวกัน ⇒ elapsed = 0 ⇒ **ปฏิเสธการเดินปกติ** | ⇒ เพิ่ม `min_measurable_elapsed_seconds = 0.5` · ต่ำกว่านั้น = **รับโดยไม่วัดความเร็ว** (`clock_too_coarse`) เพราะการหารด้วยความละเอียดของนาฬิกาคือการ *ผลิตความเร็วปลอม* |

**หลัง ship งบใหม่: replay ปฏิเสธ 0 จาก 29** (anchor 1 · within_budget 17 · clock_too_coarse 1 · stationary 10)
· step ใหญ่สุด **538.4** (งบ 2000) · เร็วสุด **269.2/วินาที** (เพดาน 1500) · dz สูงสุด **8.0** (งบ 400)
· และ replay นี้ **กลายเป็นเทสถาวร** (`tests/test_move_authority_hypothesis.py`) ไม่ใช่การคำนวณครั้งเดียวทิ้ง

### 6.7 pf-adversary ยิงงานรอบนี้ก่อน commit — **จับได้ 4 บั๊กจริง + 5 ข้อคำอ้างเกิน แก้ทั้งหมดแล้ว**

สั่งให้ **หักล้าง** ไม่ให้อนุมัติ · มันรันเทสจริง ขุด v141 จริง และหักล้างของที่ผมเขียนได้สี่จุด:

| # | ข้อ | สิ่งที่แก้ |
|---|---|---|
| A1 | **grace ตอนต้น connection = ช่องโหว่เขียนอิสระ 2 ครั้งต่อการต่อเชื่อม และ re-arm ได้ด้วยการ reconnect** (มันรันจริงจนได้แถว `x=999999`) | ล้าง grace ตอนสร้าง state ทิ้ง · **seed baseline จากแถว DB จริง** ⇒ รายงานแรกถูกวัดเหมือนทุกใบ · grace เหลือ **1 ใบ และให้เฉพาะตอนเซิร์ฟเวอร์เป็นฝ่าย teleport** |
| A2 | **teleport ของเซิร์ฟเวอร์เอง (V137 marker ห่าง 2340 แนวราบ / 448 แนวดิ่ง) ทำให้แถว DB ค้างถาวรทั้งเซสชัน** | wrap `dispatch` แล้วดู label ของ action ที่ส่งออก — เจอคำว่า `TELEPORT` ⇒ **เปิด grace ใหม่** (เซิร์ฟเวอร์รู้ว่ามันย้ายผู้เล่นเอง) |
| A3 | **บันทึก event/ตัวนับ/baseline ถูก commit ก่อนการเขียนจริง** ⇒ ถ้า `save_position` โยน `PermissionError` (lease หมดอายุ) log จะบอกว่า "เขียนแล้ว" ทั้งที่ไม่มีแถวไหนขยับ | ย้ายการบันทึกไปหลัง `checkpoint()` ผ่าน · เปลี่ยนชื่อ event เป็น `_admitted` (คำตัดสิน) ไม่ใช่ `_checkpointed` (การกระทำ) · มีเทสที่ปิด session แล้วยืนยันว่าไม่มีอะไรถูกบันทึก |
| A4 | **verifier 78 guards ไม่มีใครรันเลย** (ไม่อยู่ในเทส ไม่อยู่ใน gate) ⇒ "PASS" ที่แดงไม่ได้ | เพิ่ม `MoveAuthorityToolTests` รัน verifier จริงผ่าน subprocess **และรันสำเนาที่จงใจทำให้พังเพื่อพิสูจน์ว่ามันแดงได้** |

**ข้อคำอ้างเกินที่มันจับได้ (แก้ในรายงาน/เลดเจอร์แล้วทุกข้อ):**
- "action list เท่ากัน" จริงเฉพาะ **เฟรมที่อยู่ในมือ** — แต่ **การไม่เขียนเปลี่ยนไบต์ตำแหน่งใน StartGame ของการล็อกอินครั้งถัดไป**
  (projector ประกอบจากแถว DB) ⇒ **ตอนนี้พิสูจน์เป็นเทสแล้ว** ไม่ใช่ยกไปให้ชั้น attended
- เทียบงบ step กับระยะ "ทั้ง walk" ของ GT-005 (1060 หน่วย) = เทียบคนละหน่วย ⇒ แทนที่ด้วยตัวเลข **รายรายงาน** จาก §6.6
- 4 ใน 12 ขั้นของบันได **ไปไม่ถึงผ่าน dispatcher** (parser กรองก่อน) ⇒ ตารางในรายงานติดป้ายกำกับทุกขั้นแล้ว
- pin ของเลนพี่น้องที่ผมแก้ (§6.5) มันชี้ว่า **อ่อนลงจริง** (สอง assertIn แยกกันผ่านได้ทั้งที่ property พัง)
  ⇒ เปลี่ยนเป็น **ยืนยันข้อความจริงที่ argparse/ValueError พ่นออกมา** ไม่ใช่ข้อความในซอร์ส
- ความเร็ว **แนวดิ่งไม่ถูกจำกัดเลย** ⇒ เขียนเป็น nonclaim + เทสตรึงพฤติกรรมไว้

**ช่องโหว่ที่ยัง *เหลืออยู่* และเขียนไว้ตรง ๆ (ไม่ปิดในรอบนี้):**
① รายงาน **หนึ่งใบ** หลังเซิร์ฟเวอร์ teleport ไม่ถูกวัด (ปิดได้ต้องรู้ปลายทางของ teleport ซึ่ง v141 ไม่ประกาศ)
② ยิงถี่กว่าพื้นนาฬิกา = จำกัดด้วย step ต่อใบเท่านั้น ③ ความเร็วแนวดิ่ง ④ `lifecycle.exit` เป็นผู้เขียนแถวคนที่สอง
(ตายอยู่ตอนนี้ · มีเทสตรึงไว้) ⑤ event list โตไม่จำกัด (วัดแล้ว ~1 รายงานต่อ 2-6 วินาทีตอนเดิน ⇒ ไม่ใช่ flood)

🔴 **สิ่งที่ mendokusai แต่ต้องพูด: ถ้าไม่มีลูกมือรอบนี้ ของที่ commit ไปจะมีช่องโหว่ A1 และบั๊ก A2/A3 ติดไปด้วย**

## 6.7 🔴🔴 เจอของที่กระทบ "ท่าอ่าน ci-status" ของทั้งโปรเจกต์ — merge commit **ไม่มีวันมีคำตัดสิน**

รอบนี้ตรวจ pointer ของ GT-039 ("บูต `origin/main` HEAD ล่าสุดที่ ci-status = `success`") แล้วพบว่า
**ตอนนี้ทำตามตัวอักษรไม่ได้แล้ว**:

```
origin/main            = 55fa323  (Merge pull request #2 ...)   <- ci/55fa323.json ไม่มี
origin/main^1          = cc46a03  success (run 32406182274)
origin/main^2          = 24d5b94  success   <- head ของ PR ที่ถูก gate จริง
```

**กลไก (ยืนยันจาก Actions API แล้ว ไม่ใช่การเดา):** run ของ `gate-windows` บน branch `main` มีทั้งหมด 8 ครั้ง
ทุกครั้ง `event=push` และ `triggering_actor=panyaasanee` — **ไม่มี run ไหนเลยที่ head_sha = `55fa323`**
เพราะ commit merge ถูก push โดย `GITHUB_TOKEN` ของ workflow `merge-claude-pr` และ **push ด้วย GITHUB_TOKEN
ไม่ trigger workflow** ⇒ merge commit ไม่ถูก gate และไม่มีใครเขียน `ci/<sha>.json` ให้มันตลอดกาล

**ผลที่ตามมา (สำคัญกว่าตัวเคส):** ทุกใบในคิวที่เขียนว่า *"บูต main HEAD ที่ ci-status success"* จะ **อ่านไม่เจอไฟล์**
หลังจากนี้ทุกครั้งที่ automerge ทำงาน · และตาม **กฎ ③ ของทาง D** "ไม่มีไฟล์ = ไม่รู้ผล = ห้ามแปลว่าน่าจะเขียว"
⇒ ถ้าไม่แก้ถ้อยคำ ผู้เทสจะติดค้างทั้งที่ของเขียวอยู่จริง

✅ **ถ้อยคำที่ถูก (ใช้ในใบ GT-041 ของรอบนี้แล้ว และเสนอให้ใช้กับใบอื่นต่อไป):**
> บูตที่ **commit ที่ใหม่ที่สุดในสาย ancestor ของ `origin/main` ที่มี `ci/<sha>.json` และ `conclusion=success`
> และ `sha` ในไฟล์ตรงกับชื่อไฟล์** — ปกติคือ `origin/main^2` (head ของ PR ที่เพิ่ง merge)
> ท่าหา: `git fetch origin ci-status main` แล้วไล่ `git rev-list origin/main` เทียบกับ
> `git ls-tree --name-only origin/ci-status ci/`

🔴 **รอบนี้ไม่แก้ใบเก่าในคิว** (GT-039 ฯลฯ) เพราะกฎห้ามแตะรายการที่ยังไม่ได้เทส — เขียนเสนอไว้ในจดหมายแทน
และ **ห้ามตีความว่านี่แปลว่าโค้ดบน main ไม่ถูกเทส**: parent ทั้งสองของ merge commit เขียวทั้งคู่

⚠️ **ค่าใช้จ่ายที่ต้องจดไว้ตามบทเรียน R115:** เรียก `actions_list` ครั้งเดียวเพื่อยืนยันข้อนี้กินไปหลายพัน token
เพราะ API คืน `head_commit.message` เต็มก้อนของทุก run (บาง commit message ยาวเป็นย่อหน้า) —
**รอบหลังใส่ `per_page` เล็ก ๆ เสมอ (2-3) และอย่าเรียกถ้าไม่จำเป็น** เครื่องมือนี้ไม่มีพารามิเตอร์เลือกฟิลด์

## 7. ผลรัน (ทุกอย่างเป็น **เขียว(cloud sanity)** เท่านั้น — ไม่ใช่ gate เต็ม ไม่ใช่ Actions)

| อะไร | ผล |
|---|---|
| pytest subset (43 โมดูลถูก exclude ตามสูตร gate) | **1206 passed · 4 skipped · 1879 subtests** (39.9s) — ต้นรอบคือ 1143 ⇒ เลนนี้เพิ่ม **63 เทส** |
| `tools/verify_move_authority_gate.py` | **87 guards · PASS** (และมีเทสรันสำเนาที่พังเพื่อพิสูจน์ว่ามันแดงได้) |
| `tools/verify_hypothesis_ledger.py` | **PASS entries=37** |
| `tools/verify_functional_coverage.py` | **PASS domains=8** (ยัง INCOMPLETE ครบทั้ง 8) |
| `tools/pf_pytest_precondition_census.py` | **PASS** — skip ทั้ง 4 ถูกประกาศและ pin ครบ ไม่มี drift |
| seam test | **PASS** หลัง re-pin |

🔴 **สิ่งที่ที่นี่ตรวจไม่ได้และไม่ได้ตรวจ:** กับดัก cp874 บนคอนโซล Windows (ไฟล์ใหม่ทั้งหมดเป็น ASCII ล้วน
ตรวจด้วย `encode('ascii')` + `encode('cp874')` ในเทสเอง แต่ **ไม่ได้รันบน console จริง**) · gate เต็ม 8 check
ที่ต้องใช้อิมเมจ/DB · และ **พฤติกรรมของ client จริง**

## 8. คิวเทสเกม (ข้อบังคับ v5 ⑤)

**เพิ่มหนึ่งใบ: `GT-041 MOVE-AUTHORITY-002`** (เขียนโดย `pf-queue-author` แล้วผมปรับตัวเลขให้ตรงกับที่ ship จริง)
- คำถามหลักคือ **false refusal ก่อน** (เดินธรรมดาแล้วโดนปฏิเสธไหม) แล้วค่อยถามว่าผู้เล่นเห็นอะไร
- **pass criteria สองชั้นแยกเด็ดขาด** · ⏳ ติดป้าย **"รอ merge ก่อน"** พร้อมท่ายืนยันสามข้อ
- 🔴 ลูกมือจับได้ว่าคำสั่งของผมผิดหนึ่งข้อ: **event ของเลนนี้ไม่ถูกพิมพ์ที่ไหนเลย** (อยู่ใน `state.events` ในหน่วยความจำ)
  ⇒ ใบเทสถูกเขียนใหม่ให้ยืนบน **raw GAME log + แถว DB** แทน และบอกผู้เทสตรง ๆ ว่าคอนโซลจะเงียบ = ถูกแล้ว
- **ไม่มีรายการไหนถูกลบหรือย้าย** — GT-001/026/030/031/032/033/034/035/036/038/039/040 อยู่ครบเหมือนเดิม

## 8b. ของที่ push รอบนี้

| repo | branch | commit | PR |
|---|---|---|---|
| `pf_bridge` | `claude/zealous-turing-lf5qui` | `ebd10c9` claim (empty) + commit เอกสารรอบนี้ | **PR #12 (draft = ตัวล็อก)** — ปลด draft ตอนจบรอบ |
| `pirate-force-server` | `claude/quirky-ride-lf5qui` | `cdc52f1` (14 path · ไม่มีการลบ) | **PR #3 (non-draft ตามกฎ A4)** — รอ gate Actions ตัดสิน |

**ไม่ได้ทำโดยตั้งใจ:** ไม่ merge เอง · ไม่ปิด PR ของใคร · ไม่ push `main` · ไม่แตะ v141 · ไม่ขยับเกรด coverage
· ไม่แตะ `notes_to_chief/` ของผู้เทส · ไม่ลบ/ย้ายรายการคิวใด ๆ · ไม่แตะ `cloud_round_lock.json` (หลุมศพ)

## 9. 🔴 ที่ต้องให้ Panya เคาะ / รู้ (เขียนไว้แล้วเดินต่อ ไม่นั่งรอ)

1. **งบตัวเลขของ MOVE-AUTHORITY-002 เป็นของเรา และยังไม่เคยวัดกับการเดินจริงสักครั้ง** — ใบ GT-041
   ถูกออกแบบให้ตอบข้อนี้ก่อนข้ออื่น (ถ้าเดินปกติแล้วโดนปฏิเสธ = งบผิด ไม่ใช่กลไกผิด)
2. **ยังไม่ตัดสินใจว่าจะทำ corrective reposition ไหม** — ต้องมีหลักฐานใหม่ก่อน (หรือยอมรับว่ามันคือการประดิษฐ์ wire)
   รอบนี้จึงไม่แตะ และเขียน stop rule ห้ามไว้ในเลดเจอร์
3. ข้อค้างเดิมจาก R115 ยังค้างเหมือนเดิม: รับท่า draft เป็น v6 ①, เรื่องไฟล์ชื่อ R114 สองใบ, และ cadence

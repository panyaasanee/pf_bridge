R378
start 2026-09-06T22:52+07:00
claim (no takeover)

# chief round `tdc8si` — เกต ≤100 เริ่ม "รันจริง" บน pf_bridge (ครึ่งแรกของเงื่อนไข (2) ของ COO)

## รอบนี้ขยับ NOW/M ข้อไหน

ขยับ **ลำดับ chief ข้อ (1)** ใน `NOW.md` (`2141`) = เงื่อนไขของ
`COO-DECISION 20260906_2141` ใบ `e2015` ข้อ 1 — **ครึ่งแรก** ("workflow เรียก
`pf_gate_preflight.py` จริง") ไม่ขยับบันได M2/M3/M4 โดยตรง (M2 ยังรอเฟรม
ผู้สมัครจาก UI/A ตาม NOW · `#948` เพิ่งได้คำเคาะ (ข) รอบนี้ ยังไม่ลงมือ — เหตุผล
ในข้อ 3)

## 1) สิ่งที่วัดได้ก่อนแตะอะไร

- `grep -rn pf_gate_preflight /home/user/pf_bridge/.github /home/user/pirate-force-server/.github` = **0 hit** (ตรงกับที่ COO เขียนในใบ)
- และเหตุผลที่มันเป็น 0 ไม่ใช่แค่ "ยังไม่มีใครเขียน workflow": `main()` ของ
  `tools_bridge/pf_gate_preflight.py` **`return 2` ทันที**เมื่อไม่มี clone ของ
  `pirate-force-server` อยู่ข้าง ๆ (บรรทัด `if not (repo / ".git").exists()`)
  โดยที่เช็คฝั่งสะพานทั้งสี่ตัว (file-size ceilings · queue growth cap · ชื่อไฟล์
  ≤100 ของ pf_bridge · manual scoreboard rows) **ไม่เคยรันเลย** — และงานใน CI
  ของ pf_bridge มี repo เดียวเสมอ · `exit 2` ไม่ใช่ RED ⇒ workflow ที่ต่อกับโค้ด
  เดิมจะพิมพ์ FATAL แล้ว**เขียว**
- เงื่อนไข (1) ของ COO (ข้อยกเว้นเทียบ **basename เป๊ะ** ไม่ใช่ prefix) **มีอยู่แล้ว
  บน main**: `check_new_filename_length` ใช้ `if basename in old_basenames`
  (เซ็ตของ basename ที่ base) และเส้น `.CONSUMED.txt` ตรวจว่าไฟล์ต้นทาง
  **มีจริงที่ base** ด้วย `_git_blob_size` — ไม่ใช่การเทียบ prefix ⇒ ข้อ (1)
  ไม่ต้องแก้อะไรเพิ่มรอบนี้ (ตรวจแล้ว ไม่ได้เชื่อไฟล์รอบเก่า)

## 2) สิ่งที่ลงรอบนี้ (2 ไฟล์)

**ก. `tools_bridge/pf_gate_preflight.py`: โหมด `--bridge-only` (+ `--bridge-root`)**
รันเช็คฝั่งสะพานสี่ตัวโดยไม่ต้องมี clone ของเซิร์ฟเวอร์ · พิมพ์ออกมาตรง ๆ ว่า
เช็คฝั่งเซิร์ฟเวอร์ **ไม่ได้รัน** (ไม่ยืมความเขียวข้ามฝั่ง) · ใช้กติกาเดิมของไฟล์:
`False` = RED, `None` = INCONCLUSIVE **ไม่ใช่ผ่าน** (ทั้งคู่ exit 1)

**ข. `.github/workflows/bridge-preflight.yml` (ใหม่ ใน pf_bridge)**
`on: pull_request` · `permissions: contents: read` · `fetch-depth: 0` ·
เทียบกับ **base SHA ของ PR** ไม่ใช่ชื่อกิ่ง `main` (main ขยับระหว่างงานรัน ⇒
ไฟล์ที่รอบอื่น merge เข้ามาจะถูกนับเป็นของกิ่งนี้ — วัดเจอตอนทดสอบ ดูข้อ 4)

## 3) เงื่อนไข (2) ยัง **ไม่ครบ** — พูดตรง ๆ ว่าครึ่งเดียว และทำไม

COO เขียนว่า "เกตที่ไม่บังคับไม่นับว่าตั้งแล้ว" ถูกแล้ว และรอบนี้**ยังไม่บังคับ**:
`.github/workflows/merge-claude-pr.yml` ของ pf_bridge merge PR ที่มีโทเคน
ทันทีที่ mergeable และ **ไม่เคยอ่าน check run ใด ๆ เลย** (ส่วนหัวไฟล์เขียนไว้เอง
ว่า "THIS MERGE IS UNGUARDED, AND THAT IS A DELIBERATE CHOICE WITH A CONDITION")
⇒ tick แดงของ workflow ใหม่ไม่หยุด merge

ทำไมไม่ทำครึ่งหลังในรอบเดียวกันทั้งที่ COO ขอ "PR เดียวกัน" — สองเหตุผลที่วัดได้
ไม่ใช่ความขี้เกียจ:
1. **ทางที่ตรงที่สุดคือทางที่ผิด**: ให้ merge job รอ check run ชื่อ
   `bridge-preflight` = ผูกกับกลไกที่ (ก) PR ที่**เปิดค้างอยู่แล้ว**วันนี้
   (`#1493` `#1571` `#1577`) ไม่มี check run ของ workflow ที่เพิ่งลง main และ
   จะไม่มีจนกว่าจะ push ใหม่ ⇒ ล็อกของสายนั้นไม่ปลด **ตลอดไป** (ค่าเสียหาย =
   ทั้งสายหยุด ซึ่งเป็นสิ่งที่เจ้าของเกลียดที่สุด) และ (ข) `on: pull_request`
   รัน workflow **ฉบับที่อยู่ใน PR** ⇒ สายที่แก้ไฟล์ workflow ในใบเดียวกันแจก
   tick เขียวให้ตัวเองได้ · เขียนข้อจำกัดทั้งสองไว้ในหัวไฟล์ workflow แล้ว
2. **รูปที่ถูกต้องแพงกว่า 1 รอบ**: คำตัดสินต้องมาจากโค้ดฝั่ง base เท่านั้น —
   merge job (`pull_request_target` ซึ่งรันสำเนาบน base และ**ไม่เคย checkout
   หัว PR** = invariant ที่ header ของไฟล์นั้นพึ่งอยู่) ดึงหัว PR มาเป็น
   **ข้อมูล** (`git fetch refs/pull/N/head` แล้ว diff ชื่อไฟล์) แล้วรัน
   preflight ฉบับ base ⇒ ต้องมีโหมดเทียบ **สอง ref** (วันนี้เช็คเทียบ working
   tree HEAD กับ base) + เทสของมัน + แก้ไฟล์ 72 KB ที่ถ้าพลาดคือทุกสาย merge
   ไม่ได้ · งบ 75 นาทีของรอบนี้ไม่พอทำให้ปลอดภัยจริง ⇒ **งานแรกของรอบถัดไป**

## 4) หลักฐาน (รันจริง ไม่ใช่เดา)

- `--bridge-only` บนกิ่งนี้: `BRIDGE PREFLIGHT PASS` (4 เช็ค + consumed-stub warning) exit 0
- **เทสลบ**: clone แยก (`mktemp -d`) → เพิ่มไฟล์ basename 120 ตัวอักษร → commit → รัน `--bridge-only` ⇒ `[filenamelen] RED ... 120 chars: notes_to_chief/20260906_2300_LANE-E-THIS-IS-A-DELIBERATELY-VERY-LONG-...md` + `BRIDGE PREFLIGHT RED` exit 1 (ไฟล์ทดสอบอยู่ใน clone ชั่วคราวเท่านั้น ไม่ได้ commit ลงกิ่งนี้)
- เทสลบเดียวกันยังวัดได้อีกอย่างหนึ่ง: ถ้า `--base` ชี้ commit ที่ไม่ใช่ base จริง ⇒ RED 1044 ใบ (ชื่อเก่าทั้งนั้น) = false red · นี่คือเหตุผลที่ workflow ใช้ `github.event.pull_request.base.sha` ไม่ใช่ `origin/main`
- `--self-test`: `SELF-TEST PASS: 68 cases, 68 compared` (ไม่ถอยหลัง)
- โหมดเดิม (มี clone เซิร์ฟเวอร์) ยังเหมือนเดิมทุกแถว: `PREFLIGHT PASS` (cp874 · skips · mainmerge · census · branch ×2 · bridgesize · queuegrowth · filenamelen ×2 · scoreboard-manual)
- แตะ `.github/workflows/*.yml` ⇒ ตัวตรวจ key ซ้ำ (yaml SafeLoader ที่ raise เมื่อ key ซ้ำ) **ผ่าน** · `bash -n` ทุกก้อน `run:` (2 ก้อน) rc=0
- 🔴 หลัง push ต้องดู `actions/runs?head_sha=<sha>`: job=0 + conclusion=failure = GitHub ปฏิเสธไฟล์ (CHIEF §7) — **รอบถัดไปต้องยืนยันว่า `bridge-preflight` มี run จริง** ไม่มี = ไฟล์ตาย รายงาน ATTENDED-URGENT
- `ADVERSARY_PENDING pf_bridge#1578 (claude/eloquent-fermat-tdc8si)` — สั่ง `pf-adversary` ต้นรอบให้หักล้างแผนนี้ (blast radius ของ reaper · ชุดเช็คใน bridge-only · None ถูกนับเป็นเขียวไหม · base ชี้ผิด · วัดกิ่ง PR ที่เปิดอยู่) ผลยังไม่คืนตอน push ⇒ รอบถัดไปอ่านผลเป็นงานแรกคู่กับข้อ 3

## 5) จดหมายที่บริโภครอบนี้

- `20260906_2141_COO-DECISION-e2015-*-LANE-E` (เกตชื่อไฟล์ + §7) ⇒ งานข้อ 2/3 ของไฟล์นี้
- `20260906_2141_COO-DECISION-e2115-*-LANE-E` (`#948` death seed = **(ข)**) ⇒ ยังไม่ลงมือ เป็นงานรอบถัดไป (ดู "รอบหน้าทำอะไร" ข้อ 2) — คำเคาะเพิ่งมาถึงรอบนี้
- `20260906_2141_COO-ROUND-2141-*-LANE-E` (รอบผู้บริหาร) ⇒ อ่านครบ ไม่มีคำสั่งใหม่นอกจากที่อยู่ใน NOW แล้ว
- `SYNC_STUCK_20260906_18{16,34,36,42,44,52,54,56}.md` ×8 ⇒ สะพานค้าง **cherry-pick ที่ยังไม่จบ** บนเครื่อง Panya (`CHERRY_PICK_HEAD exists`, behind 4 ahead 0) ไม่ใช่สะพานตายและคลาวด์แก้ให้ไม่ได้ · heartbeat ล่าสุด 19:00 = เครื่องปิดตามที่ NOW บอก ไม่ใช่ตัวสะพานพัง ⇒ แจ้งในจดหมาย FROM_CHIEF

## 6) คิวเทสเกม

รอบนี้ **ไม่แตะไฟล์คิว** ตามคำสั่งใน `NOW.md` (`1259`: เลขใบ/เนื้อใบ/พับผล/archive
= LANE-K · `2141`: chief "ไม่แตะไฟล์คิว/`prompts/`") · และรอบนี้ไม่มีอะไรให้เทส
attended จริง ๆ: ผลผลิตคือเกต CI ของ repo สะพาน ผู้เล่นและผู้เทสหน้าจอไม่เห็น
อะไรเปลี่ยน ตัดสินได้จาก log ของ Actions อย่างเดียว

QUEUE_TRIAGE: ไม่ทำรอบนี้ (เจ้าของไฟล์คิว = LANE-K ตาม `1259` · chief คัดกรอง
เนื้อใบต่อไปในรอบที่แตะคิวได้) — ใบที่รอเครื่องเจ้าของยังเป็นชุดเดิมใน `NOW.md`
"รอเครื่องคุณ" (`RE-280` → `GT-281` → `GT-276` → `GT-279`) ไม่มีใบใหม่จากรอบนี้
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่ตรวจรอบนี้ (ต้องเปิด
`QUEUE_STATUS_SNAPSHOT.md` ที่ generate สด = แตะคิว) — ส่งต่อให้ LANE-K

WIRED = 19 lane_hooks บน production path / 102 ไฟล์ `production_allowed = True`
(นับด้วย `grep -rl "production_allowed\s*=\s*True" src/` บน `origin/main` ของ
เซิร์ฟเวอร์ · COO นับได้ 103 เมื่อ 21:41 — ต่าง 1 ใบ ไม่ไล่หารอบนี้ บันทึกไว้)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว — รอบนี้ไม่มีโค้ดที่รันในเซิร์ฟเวอร์เกม
(เครื่องมือ CI ของ repo สะพานล้วน ๆ ไม่มี state ต่อฉากหรือต่อ session)

## รอบหน้าทำอะไร (เรียงแล้ว)

1. **ครึ่งหลังของเงื่อนไข (2)**: ทำให้ merge job ของ `pf_bridge` ปฏิเสธ merge เมื่อ preflight ฉบับ **base** แดง — โหมดเทียบสอง ref (`--base <sha> --head <sha>`) + เทส + แก้ `merge-claude-pr.yml` แบบระวังล็อกของทุกสาย (ห้ามให้ PR ที่เปิดค้างอยู่แล้วค้างตลอดไป) · อ่านผล `pf-adversary` ของรอบนี้ก่อนเขียนโค้ด
2. **`#948` death seed (ข)** ตาม `COO-DECISION 2141` e2115: ย้าย seed ไป census ขาเข้า + ขอบเปลี่ยนฉาก **ถอดออกจากเส้น ActionVital** · ก่อนแตะโค้ดให้ `git apply rounds/E_20260906_2123_awnjat_death_seed_f7_f8_fix.patch` (F7/F8 ของ R377 ที่ยัง push เข้ากิ่งนั้นไม่ได้) · adversary วัด 2 เคสตามใบ · ผ่านทั้งคู่ = ใส่โทเคน automerge ได้เลยไม่ต้องถามอีก
3. **ตาราง 18 เทสใน 6 ไฟล์** ของ `tests/conftest.py` (แดงเพราะลำดับ vs แดงเพราะสัญญาเดิมถูกละเมิด) — รายชื่อดิบอยู่ที่ `rounds/E_20260906_2123_awnjat_f5_no_conftest_failures.txt` · ไม่เสร็จในรอบถัดไป = ถอน conftest ออกจาก `#948` แล้วแก้เทสตรง ๆ (คำสั่ง COO)
4. reaper + concurrency เท็จ + D2 ของ B (`1712`) · ปิด `#886`/`#894`/`pf_bridge#1493`
5. `AGENTS.md` §7 ยุบ ≤30 KB (COO อนุมัติให้เป็นรอบหลัง reaper)

SCOREBOARD: NONE | รอบนี้ผู้เล่นไม่เห็นอะไรใหม่ — เป็นงานเครื่องมือล้วน ๆ: กฎ "ชื่อไฟล์ใหม่ ≤100 ตัวอักษร" ที่เคยหยุดสะพานทั้งเครื่องเมื่อ 18:xx เริ่มถูกตรวจอัตโนมัติทุก PR ของ pf_bridge แทนที่จะพึ่งให้แต่ละสายจำมารันเอง (ยังเป็นตัวเตือน ยังไม่บล็อก merge) | pf_bridge#1578 (`.github/workflows/bridge-preflight.yml` + `--bridge-only`)

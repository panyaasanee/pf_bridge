# PIRATE FORCE — Chief Architect continuation file

> ✅ **คำตัดสิน Panya 2026-08-20 ~18:30 (รอบนี้เท่านั้น):**
> **ท่า push = 🆕 A′ ไม่ใช่ A** — A ตั้งอยู่บนสมมติฐานว่า Panya กด Merge เอง · รายชั่วโมง = **กดวันละ 24 ครั้ง**
> ซึ่งเธอปฏิเสธไปแล้ว ⇒ **A′: รอบ N push ขึ้น `claude/rNNN-*` · รอบ N+1 อ่านผล Actions แล้ว fast-forward `main` เอง**
> เขียว→ff+ลบ branch แล้วค่อยทำงานใหม่ · แดง→**ทั้งรอบใช้แก้ ห้ามเปิดงานใหม่** · ยังรัน→ไม่ merge รอบนี้
> 🔴 **ff เท่านั้น ห้าม force ห้าม merge commit** · **branch ค้าง ≥2 อัน = หยุดเปิดงานใหม่ ไล่เคลียร์ก่อน**
> `pf_bridge` ยัง commit ลง `main` ตรงเหมือนเดิม (เอกสารล้วน ผู้เทสต้องได้ใบสั่งทันที)
> ⚠️ cadence = รายชั่วโมง **แต่ต้องเช็คเพดานรันต่อวันก่อน** · 🔴 **ห้ามฝังตัวเลข cadence ลงในตัวบท prompt**
> 🔴 **งานสำคัญที่สุดรอบนี้: ยืนยันว่าอ่านผล Actions จากในเซสชัน Routine ได้จริงยังไง**
>   **ถ้าอ่านไม่ได้ A′ พังทั้งทาง — ต้องบอกทันที ห้ามเขียน prompt ที่สั่งให้ทำสิ่งที่ทำไม่ได้**
> รายละเอียด: `notes_to_chief\20260820_1830_PANYA-DECISION-cloud-prompt-A-prime.md`
> *(แบนเนอร์ใช้ครั้งเดียว — รอบถัดไปลบทิ้งได้)*


## 🟩 รอบ 107 (2026-08-20 ~17:00–18:0x · scheduled) — **ทำครบทั้งสามข้อของใบสั่ง 1710 · ไม่ push · ไม่แตะ routine**

**คำตัดสินเดียวที่ต้องจำจากรอบนี้:** 🔴 **ระบบธง LOCK ไม่ต้องข้ามเครื่อง และไม่ควรข้าม**
ธงคุ้มครอง *ทรัพยากรของเครื่องหนึ่งเครื่อง* (พอร์ต · process · หน้าต่างเกม · canonical DB · git index)
ซึ่ง **cloud chief เอื้อมไม่ถึงสักอย่างเดียว** ⇒ **chief บน cloud ไม่ถือธงเลยตลอดกาล**
สิ่งที่มาแทนคือ **"เขตเขียนไม่ทับกัน"** + ให้ **git เองเป็นตัวล็อก** (non-fast-forward rejection = mutual exclusion
ตัวจริงตัวเดียวในระบบนี้ · **ห้ามทำลายด้วย `--force`**) · เหตุผลเต็ม 3 ทางเลือกอยู่ใน `DESIGN_R107_WINDOWS_SYNC.md` ข้อ 3

**ส่งมอบ 5 ไฟล์ (เอกสารล้วน ไม่แตะ `src/` ไม่แตะ `tools/` ไม่บูตอะไร):**

| ไฟล์ | คืออะไร |
|---|---|
| `agent_kit\chief_task_prompt_CLOUD_v2_20260820.md` | **ตัวบท prompt เต็ม พร้อมวางลงช่อง Routine** (ข้อ 1 ของใบสั่ง) |
| `agent_kit\DIFF_CLOUD_PROMPT_v1_to_v2_20260820.md` | diff เทียบ **ข้อต่อข้อ** กับร่างเดิม — 5 ข้ออ้างที่ผิด · 6 ที่ถูก · 9 ท่อนที่ไม่เคยมี · 4 ที่ตัดทิ้งโดยตั้งใจ |
| `DESIGN_R107_WINDOWS_SYNC.md` | **ตัว sync ฝั่ง Windows** (ข้อ 2 · เช็คลิสต์ข้อ 10) — Task Scheduler 5 นาที · 8 ด่านต่อรอบ · allowlist · 9 ข้อห้าม · เกณฑ์รับงาน 6 ข้อ |
| `PROPOSAL_R107_PLANTED_RED.md` | **ปลูกแดงจงใจ** (ข้อ 3) — 5 ตัวเลือกพร้อม patch/error ที่คาด/เวลา/ความเสี่ยง + ขั้นตอนก๊อปวาง |
| `FACTPACK_R107_SYNC_MECHANICS.md` | ตัวเลขวัดจริงที่ดีไซน์ยืนอยู่บน (ลูกมือ) |
+ ภาคผนวก 9 ใน `FINDINGS_R106_R12_MEASURED_ON_A_SECOND_MACHINE.md` (**run #4 GREEN** · R12 ปิด)
+ หัว SUPERSEDED บน `chief_task_prompt_CLOUD_DRAFT.md` (เนื้อเดิมไม่ถูกแก้แม้แต่ตัวเดียว)

**commit ของรอบนี้ (จ็อบ 171 บนสะพาน · ไม่ push):** `pf_bridge` HEAD `2accb96` → **`3b99475`**
34 path · tracked 228 → **257** · **worktree สะอาด** · commit ที่สองของ repo นี้
🔴 **`pirate-force-server` ไม่ถูกแตะเลยทั้งรอบ** — ยังสะอาดที่ `9045978`
(จ็อบ 170 ตายที่ parser: **trailing comma ใน array ของ PowerShell** — บทเรียนเล็ก ๆ ที่ควรจำ
`@( 'a', 'b', )` ใช้ไม่ได้ ต่างจาก Python · จ็อบ 171 คือตัวเดียวกันที่แก้แล้ว)

### 🔴 สามอย่างที่ Panya ต้องเคาะ (chief จะไม่เดาแทน)
1. **branch ของ repo โค้ด: ทาง A หรือ B** — A = `pf_bridge` commit ลง `main` ตรง ๆ (เอกสารล้วน ผู้เทสต้องได้ใบสั่งเร็ว)
   แต่ `pirate-force-server` ไปทาง `claude/rNNN-*` + PR **เพื่อให้ Actions ยิงก่อนแตะ `main`** ⭐ chief แนะนำ A
   · B = main ตรงทั้งคู่ (ง่ายกว่า แต่โค้ดเข้า `main` ก่อนผ่าน gate ⇒ ผู้เทส pull ของแดงไปเทสได้)
2. **cadence ของ routine** — chief เสนอ **ทุก 3 ชม. (8 รอบ/วัน)** เพราะรอบจริงยาว 1.5–2.5 ชม.
   **ต้องดูเพดานรันต่อวันจริงที่หน้า routines ก่อนตั้ง**
3. **`evidence_screens/**` ควรขึ้น GitHub ไหม** — ถ้าไม่เอา ตัด allowlist เหลือ `notes_to_chief/**` ได้ทันที ดีไซน์ไม่เปลี่ยน

### 🔴🔴 และหนึ่งอย่างที่ต้อง **ทำ** ไม่ใช่แค่เคาะ — บล็อกเกอร์ตัวจริงของการสับสวิตช์
**`pf_bridge` repo มี commit เดียว: `2accb96` (2026-08-20 13:56)** · tracked 228 ไฟล์
งานรอบ **104/105/106 และจดหมายทั้งวัน ยังไม่เคย commit** (modified 4 · untracked 19 · จดหมาย 13 ไฟล์ 75,508 B)
⇒ **cloud chief ที่ clone ตอนนี้จะทำงานบนโลกของเมื่อวาน** — ต้อง commit+push `pf_bridge` ก่อน
(`pirate-force-server` ตรงข้าม: 173 commit · HEAD `9045978` · **worktree สะอาด** ⇒ พร้อมแล้ว)

### สิ่งที่รอบนี้ค้นพบระหว่างทาง (ของแถมที่ต้องไม่หาย)
- 🐛 **`LOCK_GIT.txt` มี UTF-8 BOM (`EF BB BF`)** จาก `Out-File -Encoding utf8` บน PS 5.1
  ⇒ การ์ด `$firstLine -cmatch '^HELD:'` ใน `done\169_*.ps1:83` **ไม่แมตช์ตอนธงถูกถือจริง** = ทับธงเงียบ ๆ ได้
  **`LOCK_GAME.txt` ไม่มี BOM** · ทุกเครื่องมือที่อ่านธงต้องตัด BOM ก่อนเทียบ
- 🐛 **`README_GATE_CI.md` ผิดสองจุด**: recipe เขียน `git checkout master` (repo มีแต่ `main`) ·
  recipe 2 ทำนาย "แดงสองช่อง" ทั้งที่ Actions หยุด job ที่ step แรกที่ล้ม และ workflow **ไม่มี `if: always()`** ⇒ เห็นช่องเดียวเสมอ
- ⚠️ **cp874 ถูกจับชั้นเดียวบน CI ไม่ใช่สองชั้น** — `Cp874ConsoleGateTests` (สแกนทั้ง `tools/`) ยังติดตัวกรอง
  `GameClient|capture_v141` จึงถูก `--ignore` ⇒ บนบริดจ์สองชั้น บน runner ชั้นเดียว
- ⚠️ **เลข "22 check" ยังไม่ยืนยัน** — ตาราง `GATE SUMMARY` ที่ pin=0 นับได้ **23 แถว** · เทียบกับ log run #4 ก่อนอ้างซ้ำ
- ⚠️ **`.CONSUMED.txt` แทนการลบ** — รอบนี้รันจากแซนด์บ็อกซ์ Linux ซึ่ง **ลบไฟล์บน mount ไม่ได้**
  (`Operation not permitted`) ⇒ จดหมายที่บริโภคแล้วถูก **คัดลอก** เข้า `consumed\` + วางไฟล์ marker ไว้แทน

### งานรอบถัดไป (เรียงแล้ว)
1. **ถ้า Panya เคาะดีไซน์ sync → เขียน `pf_git_sync.ps1` จริง** + ชุดเทสเชิงลบ 5 ข้อในเกณฑ์รับงาน
2. **แก้ skill `pf-attended-test` ให้อ่าน `NEW_ORDERS.txt` เป็นขั้นแรกของเซสชัน** (งานพ่วงของดีไซน์ ยังไม่ทำ)
3. `FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md` — เอา **9 โมดูล false-positive** ออกจาก ignore list
   ได้เทสคืน **398 ตัว** บน runner โดยไม่ต้องแก้เทสสักบรรทัด แล้วเดินคลื่น 1-4 ต่อ
4. sibling-layout rule + เทสที่ล้มถ้าหา `../pf_bridge/VITAL_REGISTRY_*.tsv` ไม่เจอ (เงื่อนไข ③ ของ chief verdict)
5. `DRAFT_gitignore_REPO2` second pair of eyes · R102 static (BEHAVIOR row + fight-vital delivery) · GT-037 LOOT-ROLL-001
6. housekeeping: `GAME_TEST_QUEUE` 86.9KB เกินเพดาน — **แต่เกินเพราะคิวที่ยังไม่ได้เทส ⇒ ปล่อยให้เกินตามกฎ 09:4x**

---


> ## 🆕🆕 รอบ 106 (2026-08-20 15:5x → 16:4x · scheduled) — **⭐⭐ ORDER 1545 executed ครบ: แดงตัวสุดท้ายของ Actions run #3 ปิดแล้ว "ที่ตัวเทส" ไม่ใช่ที่ CI · เกิด `tests/pf_preconditions.py` + skip census ที่พินได้ทั้งสองเครื่องด้วยไฟล์ใบเดียว · commit `9045978` · ⭐ ของแถมที่มีค่าที่สุด: 9 ใน 42 โมดูลที่ CI ซ่อนอยู่เป็น false positive — คืนเทสได้ 398 ตัวฟรี (วัดแล้ว รอลงรอบหน้า)**
>
> **HEAD `7f893b8` → `9045978`** · commit **12 paths** (4 new + 8 modified) · **จ็อบ 168 แดง → จ็อบ 169 เขียวรวด** (ถือ `LOCK_GIT` 16:18→16:23 และ 16:24→16:29 · จ็อบเขียน HELD/RELEASED เอง) · **ไม่แตะ `LOCK_GAME` เลย** (RELEASED อยู่แล้วตั้งแต่ 15:10)
>
> ### ⭐ สิ่งที่ลง — สองครึ่ง
> - **ครึ่งแรก: เทสประกาศเงื่อนไขนำเข้าของตัวเอง** · `tests/pf_preconditions.py` = ทะเบียนกลาง **7 คีย์** (`canonical_db` `client_image` `capture_v141` `backups_tree` `login_req_capture` `bridge_sibling` `game_install_tree`) · ทุก reason ขึ้นต้นด้วย token `[precondition:<key>]` (จงใจวางไว้ **หน้าสุด** เพราะ pytest ตัดท้ายบรรทัดตามความกว้าง console) · แก้ครบทั้ง 4 ตัวที่ run #3 แดง
> - 🔴 **ไม่มีจุดไหนอ่อนลงเลยบนเครื่องที่มีของครบ — และเพิ่มเทสที่รัน "ทุกเครื่อง" 3 ตัว** เพื่อไม่ให้ skip พาของที่ยังตรวจได้หายไปด้วย: ① `..._refuses_a_missing_database_in_pure_ascii` (ชี้ tool ไปที่ DB ที่ไม่มีจริง → บังคับ exit 2 + ข้อความ + ASCII ล้วน ⇒ **สัญญา cp874 กับสัญญา exit code รอดบน fresh clone**) ② `..._v94_provenance_paths_are_declared_machine_local` ③ `..._login_capture_guard_states_which_machine_it_is_on` (บังคับ `reproduced` ที่ไหนมี capture · บังคับสตริง `skipped (untracked capture absent)` **เป๊ะ** ที่ไหนไม่มี)
> - **ครึ่งหลัง: `tools/pf_pytest_precondition_census.py` + `docs/PYTEST_SKIP_PINS.json`** — อ่าน transcript `-rs` จริง · พิมพ์ skip **ทุกตัวพร้อมชื่อและเหตุผล** · เกรดกับ pin ที่ **คำนวณสด ไม่ใช่ท่องจำ**: `module ถูก exclude → 0` · `artifact มีอยู่ → 0` · นอกนั้น = ค่า pin ⇒ **ไฟล์ pin ใบเดียวถูกต้องทั้งบริดจ์ (1 skip) และ runner (4 skip) โดยไม่มีเลขที่พิมพ์มือเพื่อเครื่องใดเครื่องหนึ่ง** · **แดงทั้งขาขึ้นและขาลง** · แดงกับ skip ที่ไม่ประกาศตัว
> - **ใบเสร็จว่ามัน "เคยแดง" จริง:** `tests/test_pytest_precondition_census.py` **33 เทส** ส่วนใหญ่เป็นการปฏิเสธ (skip เกินมา · skip หายไป · skip บนเครื่องที่มี artifact · skip ไม่ประกาศ · คีย์นอกทะเบียน · pin ที่ยอมความ prefix ทางเดียวเท่านั้น) + จ็อบ 169 **ปลูกแดงสดบนเครื่อง Panya** (transcript ปลอม → census exit 1)
> - workflow: `pytest_subset` ใส่ `-rs` + tee ลงไฟล์ → step ใหม่ **`skip_census`** (พิมพ์เต็มลง log และ `GITHUB_STEP_SUMMARY` ก่อนเกรด) · runbook เพิ่ม postmortem run #3 + หัวข้อ census + **recipe 6** (วิธีทำให้มันแดงทั้งสองทิศ)
>
> ### 📐 ตัวเลขที่วัดได้ (ทั้งสองเครื่อง — นี่คือของที่ R12 ขาดมาตลอด)
> | | บริดจ์ (job 169) | fresh clone ในแซนด์บ็อกซ์ ที่ `9045978` |
> |---|---|---|
> | สวีต | **1897 passed · 1 skipped · 3599 subtests (243 วิ)** | **947 passed · 4 skipped · 1517 subtests** (+1 failed ที่เป็นของ Python 3.10 ล้วน — `__notes__` เป็นของ 3.11+ · runner เป็น 3.14) |
> | census | **PASS** — 7 artifact ครบ · design skip 1 · precondition skip 0 | **PASS** — artifact ขาดครบ 7 · precondition skip 4 ตรง pin เป๊ะ |
> ⭐ **เครื่องมือใหม่ที่ควรใช้ทุกครั้งจากนี้ไป: `git clone` รีโปลง `/tmp` แล้วรันสวีตด้วย exclusion list เดียวกัน = เห็นสิ่งที่ runner เห็น ภายใน ~50 วินาที โดยไม่ต้อง push** (ต้อง **clone** ไม่ใช่ `git archive` — หลายเทส `skipTest("not a git work tree")` จะหลอกตัวเอง · ต้องรันใน `/tmp` **ห้ามรันบน mount** ไม่งั้นแตะ canonical DB ตามบทเรียน R41 · หักผลต่าง 3.10 vs 3.14 ออกทุกครั้ง)
> · `FINDINGS_R106_R12_MEASURED_ON_A_SECOND_MACHINE.md` (ตามที่ ORDER สั่งให้บันทึกเป็น FINDINGS ใหม่)
>
> ### ⭐⭐ ของแถมที่มีค่าที่สุด — และเหตุผลที่ **จงใจยังไม่ลงรอบนี้**
> `FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md` (ลูกมือวัดทีละโมดูลครบ 42 ตัว):
> - **9 ตัวเป็น false positive ของ heuristic `GameClient|capture_v141`** — **7 ตัวโดนจับเพราะ docstring เขียนว่า "no GameClient"** (โดนลงโทษเพราะประกาศว่าไม่ต้องใช้!) · ทั้ง 9 ผ่าน **100%** บน clone ที่ไม่มี artifact เลย ⇒ **เอาออกจาก ignore ได้ฟรี คืนเทสให้ runner 398 ตัว โดยไม่แก้เทสสักบรรทัด**
> - ไม่มีโมดูลไหนพังตอน collection (890 node, 0 error) ⇒ **ไม่ต้องใช้ module-level skip กับตัวไหนเลย**
> - 8 โมดูลที่ "ป้องกันตัวเองอยู่แล้ว" **ไม่ฟรี** — reason ไม่มี token และ **4 ใน 8 ฝัง path เต็มของเครื่องไว้ในข้อความ** (pin ข้ามเครื่องไม่ได้แน่นอน) · 3 โมดูลใช้ `allow_module_level=True` ซ่อน `def test_` ไว้ **56 ตัว** จาก collector แล้วรายงานแค่ `1 skipped`
> - 🔴 **เหตุผลที่ไม่ลงรอบนี้ (บันทึกไว้ให้ตรวจสอบได้):** ฝั่ง "artifact ขาด" ของ 42 โมดูลนี้ **วัดได้เฉพาะบน Linux + Python 3.10** ในแซนด์บ็อกซ์ · การส่งของขยาย 398 เทสที่ยังไม่เคยเห็นบน Windows/3.14 ไปพร้อมกับ fix ที่ *ต้อง* ลงคืนนี้ **คือความผิดพลาดแบบ "เขียวบนเครื่องเดียว" ตัวเดียวกับที่ milestone นี้ทั้งอันมีไว้แก้** ⇒ **งานลำดับหนึ่งของรอบหน้า wave 0** (ในแฟกต์แพ็กมี 5 wave เรียงจากเสี่ยงน้อยไปมาก · ยอดรวมทุก wave cross-check ตรงกัน 398+88+82+0+43 = 611)
>
> ### 🐛 ข้อบกพร่องเล็กที่ **รู้แล้วและจงใจไม่แก้รอบนี้** (อย่าให้ใครมาเจอเองแล้วตกใจ)
> - **exclusion list ของ workflow ตอนนี้กลายเป็น 43 ไม่ใช่ 42** เพราะ heuristic ใช้ `tests\*.py` แล้วไปจับ **`tests/pf_preconditions.py`** ซึ่งเป็นไฟล์ทะเบียน ไม่ใช่โมดูลเทส · **ไม่มีผลต่อการทำงาน** (`--ignore` ไฟล์ที่ไม่ถูก collect = no-op · พิสูจน์แล้วบน fresh clone ผลเท่ากันเป๊ะ) แต่ทำให้บรรทัดที่พิมพ์ว่า "each reads the client image or the capture corpus" **ไม่จริงสำหรับหนึ่งบรรทัด** — แก้ = เปลี่ยนเป็น `tests\test_*.py` · **รอบหน้า wave 0 รื้อ heuristic นี้ทิ้งทั้งอันอยู่แล้ว ทำพร้อมกัน**
> - จ็อบ **168 แดงเพราะเลขคณิตของตัวเอง ไม่ใช่เพราะ tree**: การ์ด ASCII อ่าน blob ที่ HEAD ผ่าน PowerShell (`git show | Out-String` → `UTF8.GetBytes`) ได้ 12207 ทั้งที่ไฟล์บนดิสก์มี 4270 · **การ์ดทำถูกที่ไม่ยอม commit** · จ็อบ 169 ย้ายการเทียบทั้งก้อนเข้า Python อ่าน `git cat-file blob` เป็นไบต์ดิบ → 4270 = 4270 · **บทเรียนที่ควรเข้า template gate: สองตัวเลขที่ไม่ได้มาด้วยวิธีเดียวกัน ไม่ใช่การเปรียบเทียบ**
>
> ### 📬 กล่องจดหมาย + คิว
> - บริโภค **2 ใบ** → `consumed/` + stub: **`1545_ORDER-pytest-subset...`** (executed เต็ม) และ **`1520_GT027-RERUN-FINAL-video`**
> - จาก 1520: **บันทึกผล "HP ของเป้าหมายไม่ขยับ" ลง GT-028 พร้อมป้ายว่าเป็นคำบอกเล่า ไม่ใช่ใบเสร็จ** (`63+379+63 = 505` แต่หลอด NPC ยัง `100` · **ตอกย้ำ DAMAGE-MODEL-001: `CHitResult` ไม่แตะ HP ของใครเลย**) 🔴 **รอบใหญ่ #10 ไม่มีหลักฐานชั้น wire เลย** (ไม่มี teardown · ไม่มีไฟล์ capture ลงวันที่ 20 ส.ค.) ⇒ อ้างได้เฉพาะชั้น client-observable
> - **PLAYBOOK ข้อ 11 ใหม่: ห้ามยืดระยะเฟรมของ scenario เพื่อให้ผู้เทสถ่ายทัน — ถ่ายวิดีโอแทน** (ข้อเสนอ "profile 15–20 วิ" ของ chief เอง = **ถอนแล้ว**) · **ข้อ 12 ใหม่: ลูกศรเหลืองสองอัน = เครื่องหมายเป้าหมายที่เลือก ไม่ใช่เอฟเฟกต์ hit**
> - งานแม่บ้านทำแล้ว: **R100/R101/R102 → `archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R100_R101_R102.md`** (ไฟล์นี้ 101KB → ~63KB) · GAME_TEST_QUEUE ~87KB **ยังเกินเพดาน — รอบหน้าทำ**
>
> ### 📌 คำถามค้าง / งานรอบถัดไป (เรียงตามที่แนะนำ)
> ① **wave 0 ของแฟกต์แพ็ก: ถอด 9 false positive ออกจาก ignore** (+ แก้ heuristic เป็น `test_*.py` ในการแก้เดียวกัน) ② เฝ้า Actions run #4 หลัง Panya push — **"run #4 เขียว" ยังเป็นคำทำนาย ไม่ใช่ผลวัด** ③ **deliberate red → เขียวกลับ ยังค้าง** (recipe 1 หรือ recipe 6 ใหม่) ④ wave 1–4 ของแฟกต์แพ็ก ⑤ กฎ sibling สองรีโป + เทสที่ล้มจริง ⑥ rebase `chief_task_prompt_CLOUD_DRAFT.md` ⑦ ตรวจ `DRAFT_gitignore_REPO2` ตาสอง ⑧ static ค้าง R102: BEHAVIOR row + fight-vital delivery ⑨ GT-037 LOOT-ROLL-001 ⑩ แม่บ้าน QUEUE
> - 🔴 **รอ Panya เคาะ:** GT-034 เดิน/teleport/ตัวอื่น (ระยะ 11,914 หน่วย) · **การ์ดสามใบจากจดหมาย 1520**: ① จ็อบบูตเขียนจ็อบ teardown ลง `staged\` ทันที ② heartbeat หมดอายุแล้วมีคนเตือน (**ข้อนี้บังคับใช้แล้วตั้งแต่รอบ 105**) ③ ขยายอายุ template teardown จาก 180 นาที หรือทำโหมด `-Salvage`
> - จบก้อน 2 multiplayer (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3 · persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · milestone สำรอง not_started: `pvp_engagement` · `mob_aggro_and_server_ai`
> - เลขจ็อบ: chief ใช้ **168 + 169** ⇒ ถัดไป **170** · ผู้เทส 9xx/0xxx · จดหมายแจ้งผล: `FROM_CHIEF_R106_TO_ATTENDED_20260820_1640.md`
>
> ### nonclaims ของรอบ 106
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่แตะ `LOCK_GAME` · ไม่ flip coverage (OPEN 8 เท่าเดิม) · ไม่เพิ่ม ledger (35 เท่าเดิม) · ไม่แตะ census ทั้งสามตัว · ไม่แตะ v141 · ไม่แตะ remote/push**
> · **"Actions run #4 จะเขียว" = คำทำนาย** — ที่วัดจริงคือ clone จริงของ `9045978` ในแซนด์บ็อกซ์ + exclusion list เดียวกัน + Python 3.10 บน Linux · ตัวเลข 398/180/70/890 ของแฟกต์แพ็กวัดบน Linux+3.10 ⇒ เป็นแผนที่ ไม่ใช่ใบเสร็จ · ผล GT-028 "HP เป้าไม่ขยับ" = **คำบอกเล่า + ภาพ ไม่ใช่ใบเสร็จที่ re-derive ได้ และไม่มีชั้น wire รองรับเลย** · census ยังมองไม่เห็นสิ่งที่ `--ignore` ไม่เคยเก็บมา collect (นั่นคือ wave 0)

> ## 🆕🆕 รอบ 105 (2026-08-20 14:5x → 15:1x · scheduled) — **⭐ ORDER 1440 (A) executed ครบ: หมุดค้างยุค 2 ตัว (ไม่ใช่ตัวเดียว) → 0 · audit ตัวเลข hardcode ทั้ง yml จบ · commit เขียวรวด `7f893b8` · (B) จดบทเรียนแท่นสกปรก + เตรียม receipt ให้ Panya · จบรอบตามคำสั่ง**
>
> **HEAD `6bd1b95` → `7f893b8` (job 167 — จ็อบเดียว allGreen · ถือ LOCK_GIT 14:59→15:03 จ็อบเขียน HELD/RELEASED เอง)** · commit **2 paths**: `gate-windows.yml` (+30/-8) · `README_GATE_CI.md` (+67/-12)
> - **หมุด 1 (ตามสั่ง):** cadence cp874 `= 6` → `= 0` — คงแถวไว้เป็นบันทึก + คอมเมนต์อ้าง `2992998` (รอบ 93 คือคนแก้ · yml เขียน 19 ส.ค. ก่อน fix แล้วถูก gitignore ซ่อนจนรอบ 103 ⇒ หมุดไม่เคยเห็น fix)
> - ⭐ **หมุด 2 (audit เจอเอง): `COVERAGE_EVIDENCE_DEBT_PIN: '33'` → `'0'`** — วัดที่ `47c7211` เหมือนกัน · **จ่ายโดย commit เดียวกัน `2992998`** ("files added, references kept") · re-derive = 0 **ทุก commit** ตั้งแต่นั้นถึง HEAD (ไล่ทีละ commit) · **run #3 จะแดงตัวนี้ต่อถ้าไม่แก้** · ⚠️ **ผลพวงโดยดีไซน์: `verify_functional_coverage.py` ตอนนี้ BLOCKING บน Actions** (pin=0 → Step จริง) — ยืนยัน exit 0 ที่ HEAD ทั้ง sandbox และ Windows ก่อน flip · หมุดอื่นตรวจครบ: `3.14`/`3.14.*` คู่ self-consistent · `exit 23` internal · expect-codes อยู่กับ step — **ไม่เหลือตัวเลขที่ re-derive ไม่ได้**
> - **การ์ดใหม่ในจ็อบ 167 (ควรเข้า template gate+commit รอบหน้า):** step `REDERIVE` — นับหมุดทั้งสองสดบนเครื่อง gate ก่อน commit (computed not quoted) · แดง = abort ก่อนแตะ index
> - **prose ค้างยุคแก้ครบ (ติดป้าย ไม่ลบของเดิม):** README_GATE_CI (Run #2 postmortem + RESOLVED บนย่อหน้า "latent landmine" — มันระเบิดแล้วและถูกแก้ก่อนระเบิด + recipe 4 → `1 (pinned at 0)` + measured-facts supersede) · READINESS_CHECKLIST ข้อ 2/6 · PANYA_REPORT cloud-readiness
> - **gate เขียวครบ:** rederive ✓ seam 22p+217sub ✓ covTest 34p ✓ coverage exit 0 (OPEN 8) ✓ ledger 35 ✓ censuses ✓ full pytest ✓ canonical `6BFCEDD5..8FC7` ไม่ขยับ ✓ v141 ✓ diff --check ✓ acceptance: committed blob มีหมุด 0 ทั้งคู่ + non-ascii 0 ✓ worktree สะอาด
> - 🔴 **ข้อ 5 เช็คลิสต์ยังค้าง — run #2 ก็ไม่นับ** (แดงจริง repository-caused แต่ไม่ได้*ปลูก*) · ลำดับเดิม: push → run #3 เขียว (ครั้งแรกของ tripwire เขียว + `Declare` + `THE GATE` บน runner — เฝ้า pytest duration กับ step coverage ที่เพิ่ง blocking) → ปลูกแดง recipe 1 → เขียวกลับ
> - **(B) แท่นสกปรก — รายงาน ไม่แตะ:** `0947` ของ Panya ล้ม **exit 12 โดยดีไซน์** (stamp 189.4 นาที > 180 — template ปฏิเสธรอบถูกทิ้ง) · `0948` (TOOL_stop_stale_server) Panya รัน 14:51: **`BEFORE listeners = 0` — พอร์ตว่างไปเองแล้ว** ⇒ เหลือความเสี่ยงเดียว: canonical guard ไม่ถูกตรวจตั้งแต่จ็อบ 943 (11:27) → **เตรียม `staged\0949_gt027_stalepad_canonical_guard.ps1`** (read-only receipt) ให้ Panya หย่อนเอง · `LOCK_GAME` ยัง HELD ค้าง (heartbeat 11:35) = **ธงถูกทิ้ง ไม่ใช่มีคนทำงาน** — chief ไม่เขียนธง รอเซสชันหลัก/Panya ปิด · **คำตัดสิน run copy (ค้างจากรอบ 8–10): ทิ้งได้ทั้งหมด แต่ยังไม่ลบ** (อยู่ใต้ร่ม LOCK_GAME — รอธงคืนแล้วค่อยวางจ็อบลบ) · บทเรียนเข้า PLAYBOOK แล้ว (QUEUE ข้อ 10: เลิกเล่น ≠ ไม่ต้อง teardown · แท่นทิ้ง >180 นาทีใช้ TOOL ไม่ใช่ template · **การ์ดใหม่: chief เห็น LOCK_GAME heartbeat เก่า >30 นาที → รายงานในจดหมายทุกรอบ**)
> - 📬 บริโภค 1 ใบ: `1440_ORDER-cp874-pin-stale-and-platform-dirty` (ใบเดียวที่ค้าง) → consumed/ + stub · จดหมายแจ้งผล: `FROM_CHIEF_R105_TO_ATTENDED_20260820_1510.md`
> - **งานรอบถัดไป — สืบทอดจาก R103/R104 ไม่เปลี่ยน (ห้ามหล่น):** ① หลัง push: เฝ้า run #3 (แยก "แดง runner" vs "แดงรีโป" ก่อนแก้) ② deliberate red → เขียวกลับ ③ กฎ sibling สองรีโป + เทสล้มจริง ④ rebase `chief_task_prompt_CLOUD_DRAFT.md` ⑤ ตรวจ `DRAFT_gitignore_REPO2` ตาสอง ⑥ static ค้าง R102: BEHAVIOR row + fight-vital delivery ⑦ GT-037 LOOT-ROLL-001 ⑧ **งานแม่บ้าน: QUEUE ~81KB เกินเพดาน 60KB แล้ว + CONTINUATION ~97KB ใกล้เพดาน — รอบหน้าควรทำก่อนงานอื่นถ้าไม่มี ORDER** · GT-034 ยัง ⏸ รอ Panya เคาะระยะ/teleport
> - เลขจ็อบ: chief ใช้ **167** ⇒ ถัดไป **168** · ผู้เทส 9xx/0xxx · nonclaims: ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่แตะ LOCK_GAME/คิว(นอกจาก PLAYBOOK ข้อ 10)/ledger/coverage/census/v141 · "run #3 เขียว" เป็นคำทำนาย ไม่ใช่ผลวัด

> ## 🆕🆕 รอบ 104 (2026-08-20 14:1x → 14:2x · scheduled) — **⭐ ORDER 1410 executed ครบ: false red ของ Actions run #1 ถูกแก้ที่ต้นตอ (SELF-CHECK exit-code) + audit ทั้งไฟล์ยืนยันไม่มีจุดอื่น · commit เขียวรวด · จบรอบทันทีตามคำสั่ง 12:30 ไม่หยิบงานอื่น**
>
> **HEAD `2de7d11` → `6bd1b95` (job 166 — จ็อบเดียว allGreen · ถือ LOCK_GIT 14:18→14:24 จ็อบเขียน HELD/RELEASED เอง)** · commit **2 paths, +49 บรรทัด**: `gate-windows.yml` (+12) · `README_GATE_CI.md` (+37)
> - **root cause (อ่านจากโค้ด ตรงตามที่ order วิเคราะห์):** คำสั่ง native สุดท้ายของ step `SELF-CHECK` คือ `py -3 -c "print('\U0001F534')"` ที่**ตั้งใจ exit 1 เพื่อพิสูจน์ tripwire** · wrapper ของ `shell: pwsh` จบ step ด้วย `$LASTEXITCODE` และ `Write-Host` ไม่รีเซ็ต ⇒ step แดงทั้งที่ log ตัวเองบอกผ่านหมด — **false red ที่ท่อสร้างเอง ภาพสะท้อนของ false green รอบ 142** · แก้ด้วย `exit 0` ปิดท้าย step (หลัง assertion ทั้งสองข้อ ตัว throw ยังยิงได้ปกติถ้า self-check ล้มจริง)
> - **audit ทั้งไฟล์ตามคำสั่ง "อย่าแก้จุดเดียว" — ไม่มี step อื่นมีบั๊กนี้:** `cp874 static tripwire` จบด้วย `py -3 $f` + throw-guard (success path ทิ้ง 0) ✓ · `THE GATE` จบด้วย `exit 0/1` ชัดเจน (runbook จดกฎนี้ไว้เองอยู่แล้ว — step SELF-CHECK คือตัวที่ไม่ทำตามกฎของตัวเอง) ✓ · shim/declare steps จบด้วย cmdlet ไม่ตั้ง native code ✓ · ไม่มี step ใดจบด้วย `| Out-Null` ✓
> - **runbook อัปเดต 3 จุด:** postmortem "Run #1" (false red + สิ่งที่ run #1 **พิสูจน์ได้จริง**: checkout/setup-python/`py -3` shim/pip/**`chcp 874` + cp874 strict ใช้ได้บน windows-latest** — คำเดา runner อังกฤษไม่รับ cp874 = ผิด) · ป้าย RESOLVED บน blocker `.gitignore` (ปิดโดยรอบ 103 — เนื้อเดิมคงไว้ตาม norm) · supersede note ใต้ "NOT proven" (setup steps วัดแล้วบน runner จริง · **steps หลัง SELF-CHECK ยังไม่เคยรันบน runner** — push รอบหน้าคือครั้งแรกของ tripwire/THE GATE บน GitHub)
> - **gate เขียวครบ:** seam 22 ✓ covTest 34 ✓ coverage OPEN 8 ✓ ledger 35 ✓ censuses (152/191/PASS) ✓ **full suite 1860 passed 1 skipped 3569 subtests (373 วิ)** ✓ canonical `6BFCEDD5..8FC7` ไม่ขยับ ✓ v141 ✓ diff --check ✓ + acceptance ใหม่: **blob ที่ commit แล้ว** มี `exit 0` ปิด SELF-CHECK block จริง + blob non-ascii = 0 ✓ · worktree สะอาดหลัง commit
> - 🔴 **ข้อ 5 เช็คลิสต์ (deliberate red) ยังค้างตามเดิม — run #1 ไม่นับ** (ต้องแดงเพราะ defect จริงในรีโป) · ลำดับที่ Panya เคาะ: **push → เขียวผ่าน SELF-CHECK → จงใจแดง (recipe 1 ใน runbook) → เขียวกลับ** · chief ไม่แตะ remote/push ตลอดกาล
> - 📬 บริโภค 1 ใบ: `1410_ORDER-fix-actions-selfcheck-exitcode` (ใบเดียวในกล่อง) · ไม่แตะคิว/ledger/coverage/LOCK_GAME เลยตามคำสั่ง (LOCK_GAME ยัง HELD โดยรอบใหญ่ #10 — heartbeat 11:35 แต่มีสัญญาณชีพผ่านกล่องจดหมาย 14:07 ⇒ ไม่เข้าเกณฑ์ takeover และ chief ไม่มีธุระกับเกม)
> - **งานรอบถัดไป — ไม่เปลี่ยนจาก R103 (ห้ามหล่น):** ① หลัง Panya push: เฝ้าผล Actions (steps หลัง SELF-CHECK รันครั้งแรก — ถ้าแดงต้องแยก "แดงเพราะ runner" vs "แดงเพราะรีโป" ก่อนแก้) ② deliberate red → เขียวกลับ ③ กฎ sibling สองรีโป (doc + เทสที่ล้มจริง) ④ rebase `agent_kit\chief_task_prompt_CLOUD_DRAFT.md` (never-drop-untested-queue + 0-prefix) ⑤ ตรวจ `DRAFT_gitignore_REPO2_20260820.txt` ตาที่สอง ⑥ static ค้าง R102: populated BEHAVIOR row `B_CONSTDATA` + fight-vital delivery ⑦ GT-037 LOOT-ROLL-001 (dev headless) ⑧ งานแม่บ้าน CHIEF_CONTINUATION ~92KB · GT-034 ยัง ⏸ รอ Panya เคาะระยะ/teleport
> - เลขจ็อบ: chief ใช้ **166** ⇒ ถัดไป **167** · ผู้เทส 9xx/0xxx · จดหมายแจ้งผล: `FROM_CHIEF_R104_TO_ATTENDED_20260820_1430.md`
> - nonclaims: ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่แตะ LOCK_GAME/คิว/ledger/coverage/census/v141 · "workflow เขียวบน GitHub" ยังเป็นคำทำนาย ไม่ใช่ผลวัด จนกว่า Panya จะ push

> ## 🆕🆕 รอบ 103 (2026-08-20 13:3x → 13:4x · manual-fire โดย Panya) — **⭐ URGENT ORDER executed ครบถ้วน: allowlist `.github/` + track CI workflow — commit เขียวรวด · จบรอบทันทีตามคำสั่ง ไม่หยิบงานอื่น**
>
> **HEAD `eab98e6` → `2de7d11` (job 165 — จ็อบเดียว allGreen · ถือ LOCK_GIT 13:34→13:41 จ็อบเขียน HELD/RELEASED เอง)** · commit **3 paths**: `.gitignore` (+8 บรรทัดต่อท้าย: คอมเมนต์เล่าเหตุ + `!/.github/` + `!/.github/**`) · `.github/workflows/gate-windows.yml` (489 บรรทัด) · `.github/workflows/README_GATE_CI.md` (411 บรรทัด)
> - **เงื่อนไขจบของ Panya ผ่านครบสามข้อ:** ① `git ls-files .github` = **2 บรรทัด** (ก่อนแก้ = ว่าง · จ็อบพิสูจน์สดก่อนแก้: check-ignore ชี้ `.gitignore:1:/*` จริง) ② gate เขียวปกติ — seam ✓ covTest ✓ coverage (OPEN 8 ไม่ขยับ) ✓ ledger 35 ✓ censuses 3 ตัว ✓ full suite ✓ canonical `6BFCEDD5..8FC7` ไม่ขยับ ✓ v141 ✓ diff --check ✓ ③ **fresh clone มี workflow+runbook จริง** coverage=0 ledger=0 (บทเรียนรอบ 87: อยู่บนดิสก์ ≠ อยู่ในรีโป)
> - 📬 บริโภค 2 ใบ: **`1215_PANYA-GOLIVE`** (คำตัดสิน: `VITAL_REGISTRY...tsv` **ขึ้น** · `evidence_screens/` **ขึ้น** · `report_images/` **กันออก—ยังไม่ตัดสิน** · `verify_foundation.ps1` 79-vs-105 **พัก ไม่ใช่ตัวบล็อก** · ลำดับสับสวิตช์: **push → Actions แดงจริงหนึ่งครั้งแล้วเขียวกลับ → ค่อยสับ chief ขึ้น cloud**) + **`1230_URGENT-ORDER-github-only`**
> - 🔴 **chief ไม่แตะ remote/push ตลอดกาลจนกว่า Panya เปลี่ยนกฎ — credential เป็นของท่าน · ท่าน push เอง** · origin โผล่ใน `git remote -v` กลางรอบ = Panya ไม่ใช่ข้อผิดพลาด · `.git\STALE_index.lock_20260820_1210_delete_me` = ซากที่ผู้เทสเปลี่ยนชื่อกันไว้ Panya ลบเอง **ห้ามยุ่ง**
> - **งานรอบถัดไป (จาก GOLIVE letter + ค้างจากรอบ 102 — ห้ามหล่น):** ① กฎ sibling สองรีโป (clone เป็นพี่น้องกัน ชื่อ `Pirate Force ServerProject` + `pf_bridge` เป๊ะ — `tools\pf_vital_name_thunk_static.py:127` พึ่ง `ROOT.parent / "pf_bridge"`) เป็นเอกสาร + **เทสที่ล้มจริงถ้าโครงไม่ตรง** ② ทำ Actions **แดงจริงหนึ่งครั้งแล้วเขียวกลับ** (เช่นใส่อักขระนอก cp874 ชั่วคราว) — *เขียวที่ไม่เคยแดง ไม่ใช่ gate* — ทำได้ต่อเมื่อ Panya push แล้ว ③ rebase `agent_kit\chief_task_prompt_CLOUD_DRAFT.md` (ตกรุ่น 19 ส.ค. 17:40 — เพิ่มกฎ never-drop-untested-queue + กฎเลขจ็อบ 0-prefix) แล้วให้ Panya เห็น diff ④ ตรวจซ้ำ `DRAFT_gitignore_REPO2_20260820.txt` ด้วยตาที่สองก่อน Panya `git init` (ผู้เทสขอเอง) ⑤ static ลำดับหนึ่งค้างจากรอบ 102: populated BEHAVIOR row ใน `B_CONSTDATA` + fight-vital delivery ⑥ GT-037 LOOT-ROLL-001 (dev headless ของ chief) ⑦ งานแม่บ้าน CHIEF_CONTINUATION ~86KB (เลื่อนมาจากรอบนี้ตามคำสั่ง) · GT-034 HOSTILE-NATIVE-001 ยัง ⏸ รอ Panya เคาะเรื่องระยะ/teleport
> - เลขจ็อบ: chief ใช้ 165 ⇒ ถัดไป **166** · ผู้เทส 9xx/0xxx (0-prefix แซงคิวได้) · จดหมายแจ้งผล: `FROM_CHIEF_R103_TO_ATTENDED_20260820_1345.md` · คิว/ledger/coverage ไม่แตะเลยรอบนี้ตามคำสั่ง

> 📦 **[archive]** รอบ **100 / 101 / 102** ย้ายไป `archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R100_R101_R102.md` แล้ว (งานแม่บ้านรอบ 106 — ห้ามลบ)
> สาระสั้น: **R102** ปิด GT-027/028/029 + static ปิด dying-countdown ((ข) UI นับเอง) และ TargetVital + ORDER retarget hostile (roster 13 ตัว · GT-034 รอ Panya เคาะระยะ) · **R101** HYP-PF-028 logout-return-select (GT-033 variant B พร้อมรัน) · **R100** เปิดแถว monster_spawn_and_loot + แกะ ctor ของ attack task

> ## 🆕🆕 รอบ 99 (2026-08-20 08:2x → 09:2x) — **⭐ Door A ของ mob-aggro ลงจริง: HYP-PF-027 NPC-HOSTILE-001 — NPC ตัวแรกของ Port Royal "ขึ้นศัตรู" ด้วยการจับคู่ faction (ผู้เล่น 1 + NPC 6) · headless-proven ครบ · commit เดียวเขียวรวด**
>
> **HEAD `7a1137c` → `87f0769` (job 161 — จ็อบเดียว allGreen ตั้งแต่รอบแรก)** · commit **16 paths** (9 modified + 7 new) · full suite **1847 passed 1 skipped 3561 subtests** (167 วิ บน Windows) · fresh clone reproduce ครบ (coverage=0 ledger=0 nhVerify=0 nhReplay=0) · ledger APPEND entry **34** (HYP-PF-027 · canonical sha re-pin `9841B53D..` → `E2253C31..`) · canonical DB sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 09:19→09:22 (จ็อบเขียน HELD เอง ปล่อยเอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่างตั้งแต่ต้นรอบ (ทุกใบ consumed แล้ว)
>
> ### ⭐ สิ่งที่ลง: เลน HYP-PF-027 (Door A — pre-approved gameplay มาตรฐาน + ดราฟต์ mob-aggro รอบ 98)
> ดราฟต์รอบ 98 แยกการสู้เป็นสามประตู hostility/attack/hit-lands · Door A (hostility) คือประตูเดียวที่พิสูจน์บนสายแล้ว (SCENE-005) และเป็น checkpoint แรกที่ honest · เลนนี้ทำ Door A นั้นบนของที่พิสูจน์แล้วสองชิ้นเท่านั้น:
> - **SCENE-005 semantics:** faction = BasicAttr bit `0x0400` @ `+0x68` (u32 tag 0x14) · relation lookup `0x4A1D50` เทียบ **สองactor** · คู่ (ผู้เล่น 1, NPC 6) = แดง (runtime pass) · **arena-v2 พิสูจน์ว่า NPC 6 เดี่ยว vs ผู้เล่น 0 (ค่าคอนสตรัคเตอร์) = เป็นกลาง** (นับ 1,023 ครั้ง) ⇒ **ต้องส่งสองข้าง ไม่งั้น re-run negative**
> - **HYP-PF-023 transport:** ท่อ actor-entry (`0x6E9D` v4 · derived mask 0x02 · actor_type 4 · NPC `0x2001`) พก BasicAttr อยู่แล้ว (GT-022/025 PASS)
> **sweep 1 เฟรม (`HOSTILE_SPAWN`) + entry recompose:**
> - **ครึ่ง sweep:** เฟรม SPAWN ของ HYP-PF-023 เป๊ะ + splice 5 ไบต์ (bit 0x0400 = faction 6 · mask 0x030C → 0x070C) · **guard แข็งสุด = cross-lane byte equality** เทียบ PC กับ composer ของ HYP-PF-023 เอง (module + profile object ของพ่อ) → เลนนี้ drift จากพ่อได้ก็ต่อเมื่อ verifier สองตัวแดงพร้อมกัน · ค่าคงที่ copy + drift test ไม่ import
> - **ครึ่ง entry:** runtime recompose StartGame ผ่าน `player_wire.make_actor_attr_with_basic_faction` (frozen · รับแค่ faction 1 · scene_seq 0 · scene 1/2) **เฉพาะ identity `0x10010001`** · identity อื่น/serializer refuse/length drift → fallback production bytes + named event → dispatch ปฏิเสธ `..._player_faction_not_applied_no_reply` (ผู้เทสเห็นคู่ครบหรือไม่เห็นเลย)
> - **nonclaim บังคับ:** faction 1/6 เป็นของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล · ไม่มี name bit บน spawn (ดูเส้นขอบ+แผง Tab ไม่ใช่ป้ายชื่อ) · ไม่มี aggro/attack (Door B ยังปิด) · ไม่มี persistence
>
> ### ใบเสร็จ (headless-proven ทั้งหมด — client ยังไม่เคยเห็นแม้แต่ไบต์เดียว)
> `tools/verify_npc_hostile_encoder.py` **63 guards** (diff byte-for-byte กับ SPAWN composer ของพ่อ + ขับ refusal ทุกตัว) · `tools/pf_npc_hostile_headless_replay.py` **52 guards** ผ่าน dispatcher จริงบนสำเนา DB — walker อิสระ**อ่าน faction กลับจากไบต์ที่ dispatch จริง** + ยืนยัน StartGame พก faction-1 attr (production ไม่พก) · เทส **44 + 24 subtests** (`test_npc_hostile_hypothesis` + `test_npc_hostile_dispatch`)
> census re-pin: `pf_runtimeres_actor_entry_static.py` actor-entry sites **6→7** + modules **5→6** (โมดูลใหม่ named) · **timer census ทั้งสาม (SET/FORBID/mention 0x0080) ไม่ขยับเลย** — โมดูลใหม่ไม่เคยเอ่ย 0x0080 เลย (forbid ทุกบิตนอก 0x070C ด้วย mask equality) ⇒ **นั่นคือ guard ที่พิสูจน์ว่า builder ที่ 7 ไม่ใช่ตัวฆ่าตัวที่ 3** · report NOTE + COUNTS + test pins ครบ · `.gitignore` allowlist +3 (2 tools + report) · **coverage ไม่แตะเลย** (precedent damage lane: เลน gameplay อยู่ใน ledger อย่างเดียว ไม่มีแถว matrix ของตัวเอง ⇒ seam digest ไม่ re-pin · แถว `mob_aggro_and_server_ai` ยัง not_started จนกว่า client เห็น)
>
> ### คิว attended พร้อมรอบใหญ่ #9 (เพิ่มของใหม่)
> - 🆕 **GT-032 NPC-HOSTILE-001 = PENDING** ที่ `87f0769` — boot `--npc-hostile-hypothesis-scenario` · 1 เฟรม · **คำถามหลัก: NPC `0x2001` ขึ้นแดง (เส้นขอบ/แผง Tab) เหมือน SCENE-005 ไหม** · ⛔ ผลลบมีค่า: ถ้าไม่แดง = faction บิตตอน spawn บนท่อ actor-entry ไปไม่ถึง relation read (redirect Door A) · ตารางถ่าย+เกณฑ์สองชั้นครบในคิว · จบด้วย End task
> - GT-030/031/027/028/029/026 + GT-001 re-arm ยัง PENDING เหมือนเดิม · **GT-001 ควร re-arm ที่ `87f0769`** (commit นี้แตะ src/ runtime.py + app.py — ทุกจุดหลังธง opt-in ความเสี่ยงต่ำ)
> - เลขจ็อบ: chief ใช้ **161** ⇒ **chief ถัดไป 162** · ผู้เทส **933**
>
> ### 🧾 ธุรการ + งานแม่บ้าน
> - 🧹 **GAME_TEST_QUEUE.md = 65KB** (เกิน ~60KB) — **แต่ overage เป็นของ load-bearing:** 7 GT ที่ยัง PENDING + PLAYBOOK/บทเรียนเครื่องมือที่ **skill `pf-attended-test` อ่านจากไฟล์นี้โดยตรง** (SKILL.md บรรทัด 37/53 ชี้มาที่นี่) ⇒ archive ไม่ได้จนกว่า GT พวกนั้นปิด · รอบนี้ trim pointer รอบ-52 ที่ซ้ำซ้อนแล้ว · **การลดจริงเกิดตอนรอบใหญ่ #9 รันแล้ว GT ปิดเป็น stub**
> - CHIEF_CONTINUATION.md = 66KB (ยังไม่ถึง 100KB)
> - static-RE questions เปิดค้าง 4 ข้อ (จากดราฟต์รอบ 98 · ไม่เปลี่ยน): ① walk `CActorTask_UseBehavior`/`PlayActionEvent` ctors (Door B) ② field ที่ `CAIStateCombatProxy` อ่าน ③ parse `Data/B_CONSTDATA_TH.pc_` หา behavior row ④ singletons `[0x10339B0]`/`[localplayer+0x420]`
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 97/98)
> - **Door B (HYP-PF-028 attack probe) = ทำได้หลัง GT-032 ยืนยัน Door A บวก** · pre-approved ใต้ pattern มาตรฐาน · ผลลบ (lookup คืน null เหมือนเดิม) น่าจะเป็นผลที่มีค่าที่สุด
> - **จบก้อน 2 (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3** · HYP-PF-025 เหลือ 1 slot · HYP-PF-026/027 เหลือ 2 slots ต่ออัน
> - persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · `verify_foundation.ps1` re-pin/ปลดระวาง · `.gitignore !/.github/` · `git remote` ยังไม่มี = คำถามค้างเดิม
> - **milestone สำรอง not_started ที่เหลือ:** `monster_spawn_and_loot` · `pvp_engagement` — รอบหน้าถ้าไม่มีจดหมาย/ผลเทส แนะนำเดิน Door B (HYP-PF-028) หรือ design draft ของ monster_spawn
>
> ### nonclaims ของรอบ 99
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage row ใด ๆ · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่แตะ HYP-PF-022/023/024/025/026 หรือไบต์ของมัน (พิสูจน์ด้วย equality)**
> · **ไม่มี runtime observation ใหม่เลย** — NPC hostile presentation ยังไม่เคยถูกส่งให้ client (นั่นคือ GT-032) · ไม่ claim ว่าคู่ (1,6) ทำงานบน NPC ที่ project ผ่าน actor-entry เหมือน scene-load · ไม่ claim ว่า NPC โจมตีได้ (Door B ปิด) · faction 1/6 = การนับ/ประกอบของเราเอง ไม่ใช่ข้ออ้างเรื่องเซิร์ฟเวอร์ต้นฉบับ · full suite รันบน Windows เท่านั้น


> ## 🆕🆕 รอบ 98 (2026-08-20 07:4x → 08:2x) — **⭐ ปิดช่องว่าง "static RE เส้น server AI ยังไม่มีเลย": design draft MOB-AGGRO / server-AI ลง worktree · commit docs-only เขียวรวด**
>
> **HEAD `af10536` → `7a1137c` (job 160 — จ็อบเดียว allGreen ตั้งแต่รอบแรก)** · commit **2 paths เท่านั้น** (draft + `.gitignore` allowlist) · full suite **1803 passed 1 skipped** (162 วิ) · fresh clone reproduce ครบ (draftPresent=yes coverage=0 ledger=0) · **ไม่แตะ ledger/coverage/census เลย** (entries=33 · OPEN DOMAINS 8 · runtimeres 152 · hp 191 นิ่งหมด) · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 08:15→08:18 (จ็อบเขียน HELD เอง ปล่อยเอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่าง (ทุกใบ consumed แล้ว · R97 ยืนยัน)
>
> ### ⭐ สิ่งที่ลง: `drafts/MOB_AGGRO_SERVER_AI_STATIC_AND_DESIGN_R98_20260820.md` (252 บรรทัด · ASCII ล้วน)
> รอบนี้เลือก **milestone สำรอง pre-approved** `mob_aggro_and_server_ai` (แถว not_started) ตามที่บล็อกรอบ 96/97 แนะนำเอง — spawn ลูกมือ static RE ขนาน 3 ตัว (in-repo fact pack + binary token sweep + combat-state entry dig) แล้วเขียนเป็น design draft ไม่ใช่ lane เพราะ **ความจริงคือถนนส่วนใหญ่ยังไม่ถูกสร้าง**
> **ของใหม่ที่ไม่เคยมีรายงานไหนแกะ:**
> - client มี **local mob-AI FSM เต็ม** ใน RTTI (`CAIStateRamble{_Idle,_Walk}` → `CAIStateCombat`+`CAIStateCombatProxy` → `CAIState_Dead` · `CAIControler/Condition/Behavior` · `PatrolPath` · `MobLuaProxy_Client`) — **แต่ไม่มี live xref นอก registrar และไม่เคยยิงให้ CNetNPC ที่ server project เลย** ⇒ เป็นระบบ client-side/offline ไม่ใช่ตัวขับจากสาย
> - **attack animation vocabulary ~625 คลิป** (`_f_attack_*`/`_c_attack_*` ใน `Data/GC/A/`) เลือกด้วย **BEHAVIOR row** (`.beh` schema: `s_ANIMATION`/`s_HIT_KEYFRAME`/`n_RANGE`/`n_DAMAGE_AREA`) ไม่ใช่ task literal (ต่างจาก `_F_DIE_000`)
> - **task-id space:** id = KIND (`0x80000002/4/5/6`) ไม่ unique ต่อคลาส · family มี `UseBehavior`/`PlayActionEvent`/`Knockdown`/`Stun`/`Dodge`/… **ไม่มี `CActorTask_Attack`**
>
> ### ⭐ ข้อสรุปดีไซน์ (สามประตูของการสู้ เรียงตามความพิสูจน์แล้ว)
> - **Door A HOSTILITY = พิสูจน์แล้วบนสาย:** faction = BasicAttr bit `0x0400` @ `+0x68` · SCENE-005 runtime pass ทำชื่อแดงได้ · ท่อ actor-entry (HYP-PF-023) พก BasicAttr อยู่แล้ว ⇒ **ทำ NPC 0x2001 ให้ขึ้นศัตรูได้เลยด้วยสองกลไกที่พิสูจน์แล้ว**
> - **Door C HIT LANDS = ของเราแล้ว:** damage (GT-024 ถ่ายภาพ) + death (GT-019 หน้าต่างตาย) + HYP-PF-026 เชื่อมแล้ว
> - **Door B ATTACK = ยังไม่พิสูจน์:** ทริกเกอร์เดียวในไบนารีคือ behavior-id vital (`CHitResult+0x22` / `CKnockdownVital+0x20`) → BEHAVIOR lookup `0x702A10` · **แต่ทุก lookup ที่เคยเห็นคืน null · inbound ActionVital พิสูจน์แล้วว่า inert (SCENE-008) · ไม่มี capture ต้นฉบับ · ไม่มี encoder** ⇒ นี่คือ blocker
>
> ### เสนอ checkpoint ถัดไป (ยังไม่ได้ทำ — เป็นข้อเสนอในดราฟต์)
> - **HYP-PF-027 "NPC HOSTILE PRESENTATION"** = ประตูถูก+พิสูจน์แล้ว: scenario opt-in project 0x2001 + BasicAttr `0x0400` อย่างเดียว · headless-provable วันนี้ + attended GT ถาม "NPC ขึ้นแดงเหมือนผู้เล่นไหม" · **ต้อง ledger entry ใหม่ + re-pin runtimeres census** (บทเรียนรอบ 96 — โมดูล src/ ที่ build actor entry ขยับ census)
> - **HYP-PF-028 "attack probe"** (ทำหลัง A เท่านั้น) = ประตูแพง+ไม่แน่: `CKnockdownVital` behavior key ชี้ `7101.beh` (`_F_ATTACK_018`) · **ผลลบ (null เหมือนเดิม) น่าจะเป็นผลที่มีค่าที่สุด**
>
> ### 🧾 ธุรการ
> - เลขจ็อบ: chief ใช้ **160** ⇒ **chief ถัดไป 161** · ผู้เทส **933**
> - **ไม่เพิ่ม attended test รอบนี้** (ดราฟต์เป็นดีไซน์ ยังไม่ใช่เฟรมที่เทสได้) ⇒ **GAME_TEST_QUEUE ไม่เปลี่ยน** · คิวรอบใหญ่ #9 (GT-030/031/027/028/029/026 + GT-001 re-arm) ยังค้างเหมือนเดิม
> - 🧹 **GAME_TEST_QUEUE.md ~59.9KB ชนเพดาน ~60KB แล้ว** — รอบหน้าควรทำแม่บ้าน (ย้ายรอบเก่าที่ปิดแล้วไป archive ทิ้ง pointer) ก่อนเติมของใหม่
> - static-RE questions เปิดค้าง 4 ข้อ (เรียงตามคุณค่า): ① walk `CActorTask_UseBehavior`/`PlayActionEvent` ctors (อีกครึ่งของ Door B) ② field ที่ `CAIStateCombatProxy` อ่าน ③ parse `Data/B_CONSTDATA_TH.pc_` หา behavior row จริง ④ singletons `[0x10339B0]`/`[localplayer+0x420]` (หนี้ค้างตั้งแต่รอบ 90)
>
> ### nonclaims ของรอบ 98
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage · ไม่เพิ่ม ledger · ไม่แตะ census · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่มี runtime observation ใหม่**
> · draft = **ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · ไม่ claim ว่า NPC โจมตีได้วันนี้ (Door B ยังปิด) · Door A พิสูจน์แค่บน "ผู้เล่น" — project ลง NPC คือคำถามที่ HYP-PF-027 จะตอบ · coverage row `mob_aggro_and_server_ai` **ยัง not_started** (ไม่มี client เห็นอะไร)

> ## 🆕🆕 รอบ 97 (2026-08-20 05:5x → 07:4x) — **⭐ ชิ้นกลางของวง "ตี → เลือด → ตาย" ลงจริง: HYP-PF-026 DAMAGE-HP-LINK-001 — damage ของเราลด HP ที่ server ถือเอง แล้วบอก client ทั้งสองครึ่ง · headless-proven ครบ · commit เดียวเขียวรวด**
>
> **HEAD `8dfd303` → `af10536` (job 159 — จ็อบเดียว เขียวหมดตั้งแต่รอบแรก)** · commit เดียว 14 paths · full suite **1803 passed 1 skipped** (167 วิ) · fresh clone reproduce ครบ (ledger=0 coverage=0 hplEnc=0 hplReplay=0) · ledger APPEND entry **33** (index เก่านิ่งหมด) · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 07:28→07:32 (จ็อบปล่อยเอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่าง (ทุกใบ consumed ตั้งแต่รอบก่อน)
>
> ### ⭐ สิ่งที่ลง: เลนเชื่อม (นโยบาย #11 ของ Panya — damage model "ทาง 1" อนุมัติเต็ม + pre-approval gameplay มาตรฐาน)
> ปัญหาที่เลนนี้ตอบ: GT-024 เห็นเลขลอยแต่ **HP ไม่ลด (ยืนยันสองปาก)** · GT-019 เห็น hp 0 + timer เปิดหน้าต่างตาย · สองอย่างนี้ไม่เคยแตะกัน — และรอบ 83 พิสูจน์ว่า client **ไม่ลบเลขเอง** ⇒ server ต้องพูดทั้งสองครึ่งเอง
> **sweep 8 เฟรม opt-in เดียว (`--damage-hp-link-hypothesis-scenario`) · 15 วิ/เฟรม · one-shot:**
> `HP_BASELINE`(100/100) → `HIT_WEAK`(-63) → `HP_AFTER_WEAK`(**37 = 100−63 คำนวณจริง ไม่ได้ pin มือ**) → `MISS`(0) → `HP_AFTER_MISS`(37 ซ้ำ — control ไบต์เหมือนเป๊ะ) → `HIT_STRONG`(-379) → `HP_ZERO_DYING`(**clamp 37−379 → floor 0** + timer 20.0 เฟรมเดียว = ท่า GT-019) → `DYING_ELAPSED`(timer 0.0 = ท่า GT-023)
> - **balance ladder `(100,100,37,37,37,37,0,0)` re-walk ด้วยเลขคณิตจริงทุกครั้งที่ compose** — ไม่ตรง = refuse (`hp_arithmetic_not_reproducible`)
> - ⭐ **guard แข็งสุดของเลน: cross-lane byte equality** — เฟรม hit ทุกใบ compose ผ่าน composer ของเลน HYP-PF-024 เอง (unlock ของมันเอง) แล้วเทียบ `==` ไบต์ · เฟรม hp เทียบกับ composer ของ HYP-PF-022 เอง ⇒ เลนนี้ drift จากพ่อแม่ได้ก็ต่อเมื่อ verifier สองตัวแดงพร้อมกัน · ค่าคงที่ทั้งหมด **copy + drift test ไม่ import** (containment census ห้ามชื่อโมดูลข้ามกัน)
> - 🆕 **แคบกว่าทุกเลนเพื่อน: identity-pinned dispatch** — ยิงได้เฉพาะ selected = `0x10010001` (canonical smoke) ไม่งั้น `..._identity_not_pinned_no_reply` ⇒ ผู้เทสเห็นไบต์ตรง pin เป๊ะหรือไม่เห็นเลย
> - nonclaim ติดทุกที่: **สูตรและการเชื่อมเป็นของเรา — ต้นฉบับกู้ไม่ได้ตลอดกาล · ไม่มีคอลัมน์ HP ใน DB และไม่ได้เพิ่ม** (balance ตายพร้อม sweep) · ไม่มี path คืนชีพ (คำต้องห้ามสามคำไม่ปรากฏใน src)
>
> ### ใบเสร็จ (headless-proven ทั้งหมด — client ยังไม่เคยเห็นแม้แต่ไบต์เดียว)
> `tools/verify_damage_hp_link_encoder.py` **270 guards** (ไม่มีโหมด --binary — เลนนี้ไม่ pin อะไรใหม่จากอิมเมจ ใช้ cross-lane equality แทน) · `tools/pf_damage_hp_link_headless_replay.py` **198 guards** ผ่าน dispatcher จริงบนสำเนา DB — walker อิสระ**อ่าน ladder กลับจากไบต์ที่ dispatch จริง** (hp ที่อ่านได้ต้องเท่ากับเลขคณิตบนไบต์ ไม่ใช่บนโมดูล) · เทส **141 + 44** · **48 named refusals** · pc sizes 106/84/106/84/106/84/111/111
> census re-pin 2 ตัวพร้อมเหตุผลข้างตัวเลข (ธรรมเนียมรอบ 90/96): `src_vital_stream_call_sites` 14→15 · `src_modules_mentioning_basicattr_bit_0x0080` 4→5 (+NOTE ต่อท้าย report — SET/FORBID census ไม่ขยับ เลนนี้ไม่ build actor entry) · `.gitignore` allowlist +3 (จับได้โดยเทส EVIDENCE-VISIBLE ใน sandbox ก่อน commit — ระบบทำงาน) · **coverage ไม่แตะเลย** (precedent HYP-PF-024: เลน damage อยู่ใน ledger อย่างเดียว ไม่มีแถว matrix ของตัวเอง ⇒ seam digest ไม่ re-pin)
>
> ### คิว attended พร้อมรอบใหญ่ #9 (อัปเดตแล้ว)
> - 🆕 **GT-031 DAMAGE-HP-LINK = PENDING** — boot `--damage-hp-link-hypothesis-scenario` · 8 เฟรม/105 วิ · ตารางถ่ายทีละเฟรม+เกณฑ์สองชั้นครบในคิว · **คำถามหลัก: หลอดลดเหลือ 37 ที่เฟรม +30 ไหม** · ⛔ ตื่นเต้นพิเศษ: หลอดลดตอนเฟรมเลข = หักล้างรอบ 83 (ผลลบมีค่าที่สุด) · จบเทสต้อง End task (ห้ามกดปุ่มหน้าต่างตาย)
> - **GT-001 re-arm ที่ `af10536`** (ครอบ commit รอบ 96+97 — ทุกจุดหลังธง opt-in) · GT-030/027/028/029/026 ยัง PENDING เหมือนเดิม · GT-028 ได้ทางเลือกใหม่: ภาพ `63`/`MISS` เก็บจาก GT-031 ได้เลยถ้า GT-027 ลบ
> - เลขจ็อบ: chief ใช้ 159 ⇒ **chief ถัดไป 160** · ผู้เทส **933**
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 96)
> - **จบก้อน 2 (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3** · HYP-PF-025 เหลือ 1 version slot · HYP-PF-026 เหลือ 2 slots
> - persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · `verify_foundation.ps1` re-pin/ปลดระวาง · `.gitignore !/.github/` · `git remote` ยังไม่มี = คำถามค้างเดิม
> - **แถว not_started ที่เหลือเป็น milestone สำรอง:** `mob_aggro_and_server_ai` (ชิ้นถัดไปธรรมชาติของ combat — NPC โต้กลับ) · `monster_spawn_and_loot` — รอบหน้าถ้าไม่มีจดหมาย/ผลเทสให้ประมวล แนะนำเริ่ม design draft ของ mob_aggro (static RE เส้น server AI ยังไม่มีเลย)
>
> ### nonclaims ของรอบ 97
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage row ใด ๆ · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่แตะ HYP-PF-022/023/024/025 (ไบต์เดิมทุกเลน — พิสูจน์ด้วย equality)**
> · **ไม่มี runtime observation ใหม่เลย** — วงเต็มยังไม่เคยถูกส่งให้ client เห็น (นั่นคือ GT-031) · ไม่ claim ว่าหลอดจะลดจริงบนจอ · ไม่ claim ว่า GT-019/023 behaviours compose กันได้ในหนึ่ง sweep (นั่นคือคำถามของเทส)

## รอบ 93 + 95 + 96 — ⤴ ย้ายไป archive แล้ว (รอบ 102)

> ฉบับเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R93_R95_R96.md`
> ใจความที่ยังต้องรู้: R93 ปิดหนี้ gate-reproducible + แก้ GT-024 ด้วยไบต์ (FINDINGS_R93 = ท่อแสดงผล CHitResult) ·
> R95 ปิดงบ HYP-PF-024 (3/3) ด้วย profile npc_sweep + IMG-QUERY-001 · R96 เปิด multiplayer ก้อน 2 (HYP-PF-025) ·
> บทเรียน census SET-vs-mention (จ็อบ 156 REFUSED = guard ทำงานถูก) อยู่ในฉบับเต็ม

## รอบ 92 (+ residue ก่อนรอบ 93) — ⤴ ย้ายไป archive แล้ว (รอบ 96)
> เนื้อหาเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R92.md` (ไม่ได้ลบ ไม่ได้แก้)
---

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** รอบเก่า ☕ 26→M13 + คำขอจาก Panya (ตอบครบแล้ว) → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน A

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง

### 0.1 ใครทำอะไร (ผู้ใช้สั่ง 04:40 แก้ 04:45)

- **`pirate-force-chief-continue`** (คุณ, ตื่นนาทีที่ 0,10,20,…):
  งานโค้ด / เอกสาร / ledger / verifier / commit
  🚫 **ห้ามเทสในเกม** — ถึงจุดที่ต้องเทส ให้เขียนรายการ PENDING ลง
  `pf_bridge\GAME_TEST_QUEUE.md` แล้วจบรอบ
- **ผู้เทสในเกม = เซสชันหลัก** (Claude ตัวที่คุยกับผู้ใช้ ถือสิทธิ์ computer use อยู่แล้ว)
  task `pirate-force-game-tester` ถูกปิดชั่วคราวคืนนี้
- **กลไกปลุก:** chief-continue จบรอบ → notification ปลุกเซสชันหลักอัตโนมัติ
  → ผู้เทสอ่านคิว ถ้ามี PENDING ก็เทสแล้วกรอกผลกลับ
  **แค่จบรอบให้เรียบร้อย = ปลุกผู้เทสแล้ว ไม่ต้องทำอะไรเพิ่ม**
- ทั้งคู่ใช้ `LOCK.txt` เดียวกัน

### 0.2 เช็คตามลำดับ

1. **`pf_bridge\LOCK.txt`**
   - ขึ้นต้น `RELEASED` = ว่าง ทำงานได้เลย
   - ขึ้นต้น `HELD` และ timestamp อายุ **< 20 นาที** = มีคนทำอยู่ → **หยุดทันที**
     ห้ามเขียน `inbox\` ห้ามแตะ repo
   - `HELD` แต่ timestamp **นิ่ง** เกิน 20 นาที = หมดอายุ เขียนทับเป็นของตัวเองได้
   - timestamp **ขยับ** = เจ้าของยังมีชีวิต ห้ามแย่ง
2. **`pf_bridge\inbox\`** — ถ้ามี `.ps1` ค้าง แปลว่างานก่อนหน้ายังรันไม่จบ → หยุด
3. **`pf_bridge\outbox\`** — อ่านไฟล์ล่าสุด ถ้ามีผลที่ยังไม่วิเคราะห์ ให้อ่านก่อน
4. **`pf_bridge\GAME_TEST_QUEUE.md`** — ถ้ามีรายการที่ผู้เทสกรอก `result` กลับมาแล้ว
   ให้เอามาประมวล/commit ต่อ

---

> 📦 **[ย้ายไป archive 2026-08-18 (chief รอบ 53)]** §1–§35 (ข้อจำกัดเครื่อง §1 · PF BRIDGE §2 ·
> Workspace §3 · Playbook full-loop §7 — สำเนาสดใช้งานอยู่ใน GAME_TEST_QUEUE.md แล้ว ·
> โครงสร้างทีม §16 — ฉบับ authoritative อยู่ใน prompt ของ scheduled task · บันทึกรอบ 41–45 §31–§35)
> → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R53.md`
>
> ⚡ digest ข้อจำกัดที่ยังบังคับ (จาก §1–§3 — รายละเอียดในไฟล์ archive):
> bash=Linux sandbox เท่านั้น งาน Windows ผ่าน PF BRIDGE `.ps1` ASCII → inbox (log UTF-8, quote ทุก path มี space) ·
> request_access ใน scheduled run โดนปฏิเสธเสมอ · เปิดเกมจาก bridge = บล็อก · worktree เดิม 3 path ห้าม clone/สร้างใหม่ ·
> git ใน sandbox: cd เข้า ServerProject + `--no-optional-locks` + หลัง commit `mv HEAD.lock HEAD.lock.stale` ·
> gate จริง = Windows `py -3` ผ่าน bridge · sqlite เปิดจาก sandbox = copy /tmp หรือ mode=ro เท่านั้น · sleep ≤100 วิ

> 📦 **[ย้ายไป archive 2026-08-18 06:1x (chief รอบ 60)]** §36–§44 (บันทึกรอบ 46–54 ปิดครบแล้ว:
> รอบ 46 ดีไซน์ persistence characters/accounts `d0401f0` PROPOSED · รอบ 47+50 probe ลูกมือ Windows
> Claude CLI ผ่าน read `094` + acceptEdits `095` · รอบ 48–49 idle สั้น · รอบ 51 HYP-PF-015 soft delete
> + slot reuse `005b3d4` gate 449/0 · รอบ 52 ประมวลรอบใหญ่ #2 + fix v2 delete ack + ปิดบั๊กระบบ 2 ตัว
> `0411987` + canonical guard · รอบ 53 CHAT-ECHO-002 + HYP-PF-016 headless GREEN TCP จริง →
> GT-012/013 staged + archive §1–§35 · รอบ 54 CHAT-ECHO-004 static 0xAC52 Q1=A `5789f13`)
> → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R60.md`
>
> ⚡ ยังมีผลบังคับ (รายละเอียดใน archive):
> - **ลูกมือ Windows Claude CLI พร้อมใช้** (probe 094 read + 095 acceptEdits ผ่าน — เดิม §37.2/§40.3):
>   full path `& "C:\Users\Panya\.local\bin\claude.exe" -p` · stdout → `.agent_stdout.txt` · กติกา scope/ห้าม
>   commit/ห้ามแตะ canonical อยู่ใน prompt ของ scheduled task แล้ว
> - **❓ คำถามค้าง Panya (รอบ 46, ไม่บล็อก):** ดีไซน์ persistence characters/accounts ยัง PROPOSED
>   รอเคาะ — รายละเอียด §36.2–36.3 ใน archive

## [ARCHIVED รอบ 68] §45–§50 (รอบ 55–60) + รอบ 61–63 → pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R67.md

> ย้ายโดย chief รอบ 68 (housekeeping, CONTINUATION ชนเพดาน 100KB) — สรุปหัวเรื่องที่ย้าย:
> §45–47 CHAT-ECHO-005..007 (Q2 render gate/vtable, static) · §46 e1741db/820d473/eb52975
> §48 MOVE-AUTHORITY-001 856f9e9 (client-authoritative movement, static) · §49 MOVE-CADENCE-001 ef9acd7 (headless B)
> §50 CHAT-ECHO-008 cec8c82 (map 10 คลาส Community_*Vital, Grade A static) + แม่บ้าน archive §36–§44
> รอบ 61 TELEPORT-CHECK-001 · รอบ 62 NAMEID-HASH-001 · รอบ 63 NAMEID-RESOLVE-001 (static, นำไปสู่กำแพง v141 ในรอบ 64)

## รอบ 64–67 — ⤴ ย้ายไป archive แล้ว (รอบ 75)

รอบ 64 (NAMES fold ชนกำแพง v141-immutable → revert · ซ่อม manifest 61–63 · commit `561cb02`) ·
รอบ 65 (occupied_destination_policy → HYP-PF-017 swap headless · commit `9126fb5`) ·
รอบ 66 (same_slot_noop blocked→runtime_pass · commit `e2fca8a`) ·
รอบ 67 (move_negative_paths isolation → MOVE-ISOLATION-001 · commit `2f82af9`)
→ เนื้อหาเต็มอยู่ที่ `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R72.md`

## รอบ 68–71 — ⤴ ย้ายไป archive แล้ว (รอบ 76)

> 📦 `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R76.md`
> - **รอบ 68** SPLIT-OPERATE-001 `950819c` — inventory/split_stack not_started→in_progress, ItemOperate opcode space
> - **รอบ 69** SPLIT-OPERATE-002 `08fb65b` — op6 = quantity-op family 4 call-site
> - **รอบ 70** SPLIT-OPERATE-003 `ab89a24` — verb 0x16 two-panel, static caption route ปิด (เหลือ live capture)
> - **รอบ 71** ITEM-MERGE-001 / HYP-PF-018 `8282a21` — generalized same-template merge, headless wire/DB proven
> ⚡ ที่ยังบังคับอยู่จากสี่รอบนี้: **ป้าย "numeric-input dialog resource 0x12" @0x5A34D7 ของ SPLIT-OPERATE-001/002 ถูกแก้แล้วในรอบ 75** (จริง ๆ คือ MSVC EH trylevel store) — โครงสร้างที่พิสูจน์ไม่กระทบ · GT-015 ต้องการ live capture เท่านั้น

## รอบ 72–75 — ⤴ ย้ายไป archive แล้ว (รอบ 77)

> `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R77.md` — เนื้อหาครบไม่ตัดทอน
> · รอบ 72 MOVE-AUTHORITY-001 `6577626` · รอบ 73→74 MOVE-PROJECT-001 `f0f1968`
> · รอบ 75 USE-DROP-SELL-001 + CHAT-CHANNEL-001 `b2e4669`

## รอบ 76–78 — ⤴ ย้ายไป archive แล้ว (รอบ 81)

> เนื้อหาเต็มของ **รอบ 76 (CHAT-CHANNEL-002/003), รอบ 77 (MULTIPLAYER-READINESS-AUDIT-001),
> รอบ 78 (STATS-PROG-002 + MP-AUDIT-FOLLOWUP-001)** อยู่ที่
> `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R78.md`
>
> สิ่งที่ยังต้องรู้จากสามรอบนี้โดยไม่ต้องเปิด archive:
> - **MP-AUDIT-FOLLOWUP-001 (รอบ 78) ตอบ G1 ของ audit ไปแล้วระดับ ①** — `actor_type` 2..6 =
>   CNetActor / CMyActor / CNetNPC / CAvatarNPC / Pet · **remote player = 2** · F8 ปิด · G2 แคบลง
>   ⇒ **Option 1 ส่วน (a) เสร็จตั้งแต่รอบ 78 ห้ามทำซ้ำ** (รอบ 81 เกือบสั่งลูกมือทำซ้ำ)
> - audit รอบ 77 = ต้นทางของคำถาม G1–G9 และของคำตัดสิน Option 1 ของ Panya
> - รอบ 79 ไม่มีบันทึก: ถือ LOCK 18:2x แล้วตายเงียบ 5h42m โดยไม่ spawn อะไรเลย

---

## รอบ 80–81 — ⤴ ย้ายไป archive แล้ว (รอบ 83)

`archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R80_R81.md`
· รอบ 80 = UI-REFRESH-001 + HP-DEATH-001 · รอบ 81 = สี่ lane ขนาน (NAMES/DELETE-REFRESH/HP-DEATH-002/MP-OPT1-B)
· **ทั้งสี่ lane ของรอบ 81 ถูกเทสจริงในรอบใหญ่ #4-#5 และ PASS หมด** — ผลอยู่ในรอบ 83


## รอบ 82–83 — ⤴ ย้ายไป archive แล้ว (รอบ 85)

> เนื้อหาเต็มของ **รอบ 82 (CORPUS-PIN-001), รอบ 83 (DAMAGE-MODEL-001)** อยู่ที่
> `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R82_R83.md`
>
> สิ่งที่ยังต้องรู้จากสองรอบนี้โดยไม่ต้องเปิด archive:
> - **`docs/PF_CAPTURE_CORPUS.json` = บ้านเดียวของชุดหลักฐาน** (รอบ 82) — เลิกถามไดเรกทอรีว่าไฟล์ไหนคือหลักฐาน
>   ตัวเลขที่เผยแพร่ = **44 จาก 67** (ไม่ใช่ 69 · 2 live tail ถูกกันออกโดยระบุชื่อ) · ถ้าตัวตรวจ corpus แดง
>   **ห้าม regenerate ตารางให้เขียว** ให้ไปหาจ็อบที่เขียนทับหลักฐาน
> - **รอบ 83 พิสูจน์ว่า client ไม่คำนวณ damage เอง** — ตัวเลขที่ลอยขึ้นคือ **i32 มีเครื่องหมาย** ที่ server
>   วางไว้ที่ hit entry `+0x08` ผ่าน abs() แล้วพิมพ์ ⇒ **ตัวเลขต้นฉบับกู้ไม่ได้ตลอดกาล** (ทาง 2 ปิดถาวร)
> - **wire = tagged stream** — ทุก field คือ tag byte 1 ตัวแล้วตามด้วย payload · client เทียบ tag แล้วยก
>   error flag ถ้าไม่ตรง ⇒ **server ต้องส่ง tag ให้ตรงเป๊ะ ไม่ใช่แค่ความกว้างถูก** · hit result = 5 field
>   แล้วตามด้วย array ของ entry ละ 32 ไบต์ (target id · i32 damage · position vec · reaction angle · u16 flag)
> - **`DURATION_DYING` = 20** (อ่านจากอิมเมจรอบ 83) — ปิดหนี้ค่า placeholder 60.0f ของรอบ 81
> - 🔴 **รอบ 85 หักล้างพาดหัวรอบ 83 หนึ่งประโยค** — ดูรอบ 85 หัวข้อ RUNTIMERES-ACTOR-ENTRY-001 และ
>   erratum ที่ต่อท้าย `reports/PF_HP_DEATH001_HP_DEATH_AND_RESPAWN_STATIC_20260819.md`

---

## รอบ 84–85 — ⤴ ย้ายไป archive แล้ว (รอบ 87)

อยู่ที่ `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R84_R85.md` (ไม่ได้ลบ ไม่ได้แก้)
· รอบ 84 = DYING-HOLD-001 + ATTENDED-EVIDENCE-001 + SCAN-DEBT-001 → commit `8360f57`
· รอบ 85 = NAMES-FOLD-002 + RUNTIMERES-ACTOR-ENTRY-001 + RESOLVE-SCOPE-001 → commit `32878e0`
· เรื่องเล่าฉบับเต็มของทั้งสองรอบอยู่ในข้อความ commit ของมันเองด้วย

## รอบ 86 + 87 — ⤴ ย้ายไป archive แล้ว (รอบ 92)
> เนื้อหาเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R86_R89.md`
> (RUNTIMERES-ENCODER-001 + NAMES-FOLD-003 + COMMENT-ERRATA-002 + LEDGER-VISIBILITY-001 + CP874-PORTABILITY-001)
> 🔑 **บทเรียนที่ยังใช้อยู่ อย่าลืม:** เครื่องมือห้ามพิมพ์อักขระนอก cp874 ออก console (อีโมจิทำ gate แดงเฉพาะบน Windows)
> · *"check ที่ไม่เคยเห็นมันแดง ไม่ใช่ check"*

## รอบ 89 — ⤴ ย้ายไป archive แล้ว (รอบ 92)
> เนื้อหาเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R86_R89.md`
> (บัญชีใหม่รอบแรก · DEATH-ESCALATE-001 + BRIDGE-LIVENESS-001 + งานแม่บ้านส่งกะ)

## รอบ 90 (ถูกตัดกลางคัน) + รอบ 91 — ⤴ ย้ายไป archive แล้ว (รอบ 95)

> ฉบับเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R90_R91.md`
> ใจความ: จ็อบ 145 แดงหนึ่ง guard จึงไม่ commit (fail closed ทำงาน) · รอบ 90 ถูกตัดกลางซ่อม ·
> รอบ 91 อ่านทรี รันเทสซ้ำจนเขียว แล้ว commit `d4ed4d4` (HYP-PF-024 ลงจริง 16 path) +
> เปิด RUNTIMERES-LATCHONLY-001 (`47c7211`) ตามที่ผู้เทสขอ · บทเรียนหลัก: **guard ที่แดงคือ guard ที่ทำงาน**
> และ **takeover แล้วให้อ่านทรีก่อน อย่าเขียนทับ**

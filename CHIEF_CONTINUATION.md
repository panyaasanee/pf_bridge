# PIRATE FORCE — Chief Architect continuation file

> 📌 **สถานะ 2026-08-20 ~21:30 (รอบนี้เท่านั้น) — เหลือ repo โค้ด repo เดียว:**
> ✅ **PR #1/#2 ปิดแล้ว** (Panya ตรวจเอง: เอกสารล้วน ไม่มี src/tools/tests/docs · branch เก็บไว้) ⇒ ล็อกปลดแล้ว
> ✅ **`pf_bridge` ติดตั้ง `merge-claude-pr` + allowlist `.github/` และ `rounds/` เรียบร้อย** (ยืนยัน ls-files = 1)
> 🔴 **งานรอบนี้: gate + commit ไฟล์เดียว** — `.github\workflows\merge-claude-pr.yml` ใน repo โค้ด
>   stage เฉพาะพาธนั้น · `.gitignore` ไม่ต้องแก้ · **Panya push เอง**
> ⚠️ **Panya ทำงานมาตั้งแต่เช้า ~21:30 แล้ว ⇒ รอบนี้ให้สั้นที่สุด** ห้ามเปิดงานใหม่ ห้ามเขียนเอกสารเพิ่ม เสร็จแล้วจบ
> 🔴 **ห้าม push · ห้ามแตะ routine · ห้ามแตะ PR**
> รายละเอียด: `notes_to_chief\20260820_2130_PANYA-STATUS-install-step2-code-repo-only.md`
> *(แบนเนอร์ใช้ครั้งเดียว — รอบถัดไปลบทิ้งได้)*


## 🔄 รอบ 110 (chief · 2026-08-20 ~20:36-21:1x) — **ตอบสี่ข้อของ Panya + สร้างตัว merge ที่ทำให้ล็อก PR ไม่มีวันค้าง**

**รับใบสั่ง:** `notes_to_chief/20260820_2035_PANYA-DECISION-A-double-prime-PR-lock.md` (กล่องเคลียร์แล้ว เหลือ 0 ใบ)
**ธง:** ไม่ถือใบไหนเลยทั้งรอบ — ไม่มี gate/commit job · ไม่แตะ server/เกม/DB · ไม่ push อะไรทั้งสิ้น
**📄 รายงานหลักอ่านที่:** `pf_bridge/PANYA_REPORT_20260820_answers_PR_lock.md` *(บล็อกนี้เป็นแค่สรุป)*

### สิ่งที่ตอบได้ กับสิ่งที่ตอบไม่ได้ — แยกให้ชัด
🔴 **แซนด์บ็อกซ์ของ chief ไม่มี GitHub credential** — วัดจริง: `git ls-remote origin` ตอบ
`fatal: could not read Username for 'https://github.com'` ⇒ **มองไม่เห็น PR #1/#2 · อ่าน repo settings ไม่ได้ · ยิง API ทดสอบไม่ได้**

| ข้อ | คำตอบ |
|---|---|
| ① PR แดง = ล็อกค้างถาวร | **แก้แล้วโดยไม่ต้องรู้ว่า sandbox ปิด PR ได้ไหม** (ตอบไม่ได้ และไม่ต้องตอบ) — **ให้ GitHub ปิดเอง** ทุกทางจบที่ PR ไม่เปิดค้าง: เขียว→merge · แดง→comment+ปิด+เก็บ branch · ชน→ปิด · ไม่มีผลเกิน 6 ชม.→job `reap` ปิด |
| ② auto-merge มีจริงไหม | **ตอบไม่ได้ (repo setting)** ⇒ **จงใจไม่ใช้มัน** ใช้ workflow เรียก `gh pr merge` แทน · ✅ `contents: write` **วัดแล้ว** (branch `ci-status` เกิดได้ด้วยกลไกเดียวกันนี้) · 🟡 `pull-requests: write` **ยังไม่วัด** → ถ้าถูกปฏิเสธจะเห็น **403** ใน log job `decide` |
| ③ CONTINUATION แทรกบรรทัด 3 | **การ์ด PR ครอบไม่หมด — พูดตรง ๆ** รั่วสองรู: check-then-act · **และสะพาน Windows ไม่อยู่ในล็อกเลย** (`pf_git_sync.ps1` push ทุก ~5 นาที) ⇒ แก้ที่ไฟล์ ไม่ใช่ที่ล็อก = **"หนึ่งรอบหนึ่งไฟล์"** `rounds/R<NNN>_*.md` + ดัชนีต่อท้าย |
| ④ PR #1/#2 | **เสนอ: ปิดทั้งคู่ เก็บ branch** (มองไม่เห็น ⇒ เป็นข้อเสนอมีเงื่อนไข) — เนื้อหาได้จากใบสั่ง 20:35 แล้ว · ถ้า merge จะฝัง A′+ล็อกไฟล์ที่ตายแล้วลง `main` · **เช็ค Files changed ก่อน: เห็นไฟล์ใต้ `src/` `tools/` `tests/` = หยุด อย่าปิด** |

### ของที่ทำเสร็จ (ทั้งหมด **ยังไม่ commit** — index ของ `pf_bridge` เป็นของ Panya, R109 เตือนไว้)
- 🆕 `Pirate Force ServerProject/.github/workflows/merge-claude-pr.yml` — 324 บรรทัด · job `decide` (workflow_run) + `reap` (cron)
- 🆕 `pf_bridge/drafts/WORKFLOW_bridge_merge-claude-pr.yml` — ฉบับ repo เอกสาร (`pull_request_target` ไม่ใช่ `pull_request` — กัน PR แก้กติกาที่ตัดสินตัวเอง)
- 🆕 `pf_bridge/drafts/INSTALL_merge_workflows_20260820.md` — วิธีติดตั้ง + `.gitignore` ของ `pf_bridge`
- 🆕 `pf_bridge/agent_kit/chief_task_prompt_CLOUD_v4_20260820.md` — **v4** (v3 = ประวัติ)
- ✏️ `pf_bridge/FINDINGS_R108_A_PRIME_HOW_TO_READ_ACTIONS.md` — CORRECTION + กำกับ 11 จุด **ไม่ลบของเดิม**
- ⚰️ `pf_bridge/cloud_round_lock.json` — เขียนเป็นหลุมศพ `state: "DEAD"` **เก็บไว้ ไม่ลบ**

### 🔴 ปมสำคัญที่รอบถัดไปต้องไม่ลืม
**opt-in ด้วย marker `PF-AUTOMERGE: v4` ใน PR body** — PR ที่ไม่มีบรรทัดนี้ workflow จะเมิน
⇒ ติดตั้ง workflow ตอนนี้ **merge PR #1/#2 ย้อนหลังไม่ได้** (จงใจ) แต่ **สองใบนั้นยังเป็นล็อกอยู่ถ้าไม่ปิด**

**ลำดับก่อนเปิด routine (ห้ามสลับ):** ① ตัดสิน PR #1/#2 → ② ติดตั้ง workflow ทั้งสอง repo + แก้ `.gitignore` ของ `pf_bridge`
→ ③ ยิง `workflow_dispatch` ดูว่ามี 403 ไหม → ④ เปิด routine ด้วย v4
⚠️ **เปิด routine ก่อนข้อ ② = ทุกรอบจบทันทีตลอดไป** — การ์ดทำงานถูก แต่ไม่มีใครปลดล็อก

### ✅ ของที่ปิดไปแล้วในเช็คลิสต์ "ก่อนสับสวิตช์" (อัปเดตใน v4)
sync **ติดตั้งแล้วและวิ่งอยู่จริง** (`sync.log` 20:42 · push `pf_bridge` ทุก ~5 นาที · repo โค้ด pull อย่างเดียว · หยุดเองเมื่อ `LOCK_GAME` ถือ)
· อ่านผล gate **ปิดสองชั้น** (API ได้ + ทาง D มีชีวิต) · `push main` **ปิดแล้ว: ทำไม่ได้**
🔴 เหลือข้อเดียวที่ยังบล็อก: **workflow `merge-claude-pr` ยังไม่อยู่บน `main` ของทั้งสอง repo**

### 🔎 ตรวจแบบปฏิปักษ์ แล้ว **เขียน workflow ใหม่ทั้งไฟล์** (ร่างแรกพัง 6 จุด)
สั่งลูกมือว่า *"หน้าที่คุณคือหาจุดที่มันพัง"* — เจอของจริง สองข้อแรกทำลายสิ่งที่ไฟล์นี้อ้างว่าแก้ได้พอดี:
1. 🔴 `reap` เจอ "เขียวแต่ PR ยังเปิด" แล้ว **แค่ warning** = **ล็อกถาวรที่อ้างว่ากำจัดแล้ว** ⇒ ให้ `reap` **merge เอง แล้วปิดถ้าไม่ได้**
2. 🔴 `gh pr merge` ล้ม (403/แข่งแพ้) ⇒ `set -e` ฆ่าสคริปต์ **โดย PR ยังเปิด** ⇒ จับ exit code แล้ว **ปิด PR พร้อมแปะ log**
3. 🔴 อ่าน `workflow_run.conclusion` (ผลรวมทั้ง workflow) ⇒ `publish-status` ล้มเองได้ ⇒ **gate เขียวแต่ปิด PR ทิ้งพร้อมบอกว่าแดง** ⇒ อ่าน conclusion ของ **job ชื่อ `gate`** แทน
4. ไม่มีเช็ค **fork** (ทั้งสองไฟล์) + ไม่มีเช็ค **base branch** (ไฟล์โค้ด) — `claude/*`+marker เป็นสิ่งที่คนเปิด PR เขียนเองได้ ⇒ repo เอกสารที่ไม่มี gate = ใครก็ merge เข้า main ได้
5. `gh api ... || true` ⇒ API ล่มดูเหมือน "ไม่มีอะไรต้องทำ" แล้วจบเขียว ⇒ ฟังก์ชัน `api()` แยก "ล้ม" ออกจาก "ว่าง"
6. ไม่มี `concurrency:` · `date` parse ไม่ได้ฆ่าทั้งลูป
⭐ **ทั้ง 6 ข้อเป็นรูปแบบเดียวกัน: "ทางออกที่รายงานแทนที่จะลงมือ"** — ในระบบที่ *ความเงียบ = ล็อกค้าง* นี่คือความล้มเหลวที่แพงที่สุด

### nonclaims รอบ 110
- **workflow ทั้งสองไฟล์ยังไม่เคยรันแม้แต่ครั้งเดียว** — ตรวจแค่ yaml parse + `bash -n` ทั้งสอง job + non-ASCII = 0 ไบต์ + ตรวจปฏิปักษ์หนึ่งรอบ
- **การตรวจไม่ใช่การรัน** — การอ่าน conclusion ของ job และทางค้นหา PR ทางที่สอง **ยังไม่เคยถูกยิงจริง**
- **`workflow_run.head_sha` ของ run ที่มาจาก event `pull_request` ยังไม่มีใครวัด** ⇒ ไฟล์จึงมีทางค้นหา PR สองทาง ไม่พึ่งข้อนี้ข้อเดียว
- **ไม่ได้อ่าน PR #1/#2 · ไม่ได้อ่าน repo settings · ไม่ได้ยิง GitHub API เลย** (ไม่มี credential)
- **ยังไม่ได้ย้ายไป `rounds/` จริง** — ต้องเติม `!/rounds/` `!/rounds/**` ใน `.gitignore` ของ `pf_bridge` ก่อน
  ไม่งั้นไฟล์จะอยู่บนดิสก์แต่ git มองไม่เห็น (กับดักเดิมของ `.github/` รอบ 87-103)
- ไม่แตะเกม/เซิร์ฟเวอร์/canonical DB/คิวเทส · **คิว GAME_TEST_QUEUE ไม่เปลี่ยนรอบนี้** (รอบนี้เป็นงาน infra ล้วน)


> 🗂 **แบนเนอร์ "ทาง D" (คำสั่ง Panya 2026-08-20 ~19:10) — บริโภคจบแล้ว ลบทิ้งตามที่มันบอกเอง (chief รอบ 111)**
> เนื้อหาเต็มของใบสั่ง: `notes_to_chief\20260820_1910_PANYA-APPROVED-path-D-ci-status.md` · สิ่งที่ทำ: บล็อกรอบ 109 ด้านล่าง

---

## 🟩 รอบ 109 (2026-08-20 ~19:12–19:5x · scheduled) — **ทาง D ลงไฟล์แล้ว · gate เขียว · commit เดียว · ไม่ push**

**ธง:** `LOCK_GIT` ถือเฉพาะช่วงจ็อบ 175 รันจริง (19:27 → ปล่อยเองท้ายจ็อบ) · **`LOCK_GAME` ไม่แตะเลย**
**ไม่ push · ไม่บูตเซิร์ฟ · ไม่เปิดเกม · ไม่เขียน DB · ไม่แตะ routine · ไม่แตะ scheduled task**

### สิ่งที่เปลี่ยนจริง
| ไฟล์ | คือ |
|---|---|
| `.github/workflows/gate-windows.yml` | **job ใหม่ `publish-status`** เขียนคำตัดสินหนึ่งใบต่อหนึ่ง commit ลง **orphan branch `ci-status`** ที่ `ci/<sha>.json` · `if: always()` ⇒ ประกาศทั้งเขียวและแดง · และ trigger เปลี่ยนจาก `branches: ['**']` → `branches-ignore: ['ci-status']` |
| `FINDINGS_R109_PATH_D_APPLIED_AND_REHEARSED.md` | **หกอย่างที่ของจริงต่างจากร่างรอบ 108** + หลักฐานการซ้อม + nonclaims |
| `agent_kit\chief_task_prompt_CLOUD_v3_20260820.md` | ท่อน "อ่านผล gate ยังไง" เขียนใหม่ทั้งท่อน + คำสั่งสแกน branch + **ตาราง fallback ของ `push main`** |

### 🔴 บทเรียนที่แพงที่สุดของรอบนี้ — **ร่างของรอบ 108 มีบั๊กจริงหนึ่งข้อ**
ร่างไม่มี `shell: bash` ทั้งที่ไฟล์ workflow ประกาศ `defaults: run: shell: pwsh`
⇒ ภายใต้ pwsh บรรทัด `set -euo pipefail` **ไม่ใช่ error ที่หยุดสคริปต์ แต่คือคำสั่งที่หาไม่เจอ ถูกข้ามไป**
⇒ สคริปต์เดินต่อหลังคำสั่งแรกที่ล้ม ⇒ **push ไม่ขึ้นแต่ step เขียว** ⇒ chief จะอ่าน "ไม่มีสถานะ" ตลอดกาลโดยไม่มีใครรู้ว่าทำไม
📌 **กฎที่ตกผลึก: ทุกครั้งที่เพิ่ม step ลง workflow ที่มี `defaults.run.shell` ให้ประกาศ shell ของ step นั้นเสมอ**

### สี่ข้อของ Panya — ตอบด้วยตัวแพตช์ ไม่ใช่ด้วยคำอธิบายข้างแพตช์
- **① ผูกกับ SHA** ⇒ `ci/<sha>.json` **และ ตัด `ci/latest.json` ทิ้งทั้งใบ** — ไฟล์ "ล่าสุด" คือทางเดียวที่ความผิดพลาดนั้นเกิดได้จริง
  (อ่านคำว่า `success` ของ commit อื่นแล้ว merge ของที่ยังไม่ผ่าน โดยไม่มีสัญญาณเตือน) · **จ็อบ 175 มี negative guard กันไม่ให้ใครใส่กลับ**
- **② ไม่ลูป** ⇒ `branches-ignore` ที่ trigger **และ** `if: always() && github.ref_name != 'ci-status'` ที่ job
  กฎ GITHUB_TOKEN ของ GitHub เป็น **ชั้นที่สาม ไม่ใช่ชั้นเดียว**
- **③ A′ ไม่นับ** ⇒ `ci-status` เป็น **orphan** (ซ้อมแล้ว: `rev-list --max-parents=0` = 1 root)
  และ prompt v3 สแกนด้วย `git for-each-ref refs/remotes/origin/claude/` ⇒ **มันโผล่ไม่ได้ตั้งแต่แรก ไม่ใช่ถูกกรองทีหลัง**
- **④ ไม่มีสถานะ = ไม่ merge** ⇒ เขียนเป็นหนึ่งใน **สี่กฎการอ่าน** ใน prompt v3 พร้อมข้อที่ยังไม่มีใครพูดถึง:
  **`skipped` และ `cancelled` ก็ไม่ใช่เขียว** (`needs.gate.result` มีสี่ค่า)

### หลักฐานการซ้อม (ก่อน commit ไม่ใช่หลังจากนั้น)
ดึงเนื้อ bash **ออกจาก YAML ด้วย `yaml.safe_load`** แล้วรันจริงกับ bare repo — **ไบต์ชุดเดียวกับที่ GitHub จะรัน**
สร้าง orphan รอบแรก ✅ · ต่อท้ายรอบหลัง ✅ · rerun commit เดิม ✅ (`--allow-empty`) ·
**race: ผู้แพ้ rebase แล้วชนะ โดยไม่มีคำตัดสินใบไหนหาย** ✅ · **ไฟล์ที่ไม่มี → exit 128** ✅ (= สัญญาณ ⏳)

### ✅ จ็อบ 175 — **allGreen=True · committed=1 · blobOk=0** · `9045978` → **`89ce13b`**
`pytest **1897 passed · 1 skipped** · 3599 subtests · 189s` (skip เดียวคือ design skip ที่ pin ไว้แล้ว)
· skip census **PASS — artifact ครบ 7/7 บนสะพาน** · seam 22p/217sub · covTest 34p · coverage exit 0 · ledger 35
· mpaudit 0 · census PASS · **canonical sha `6BFCEDD5..8FC7` ไม่ขยับ** · v141 สะอาด · diffcheck 0
· staged = 1 path เป๊ะ · **acceptance บน blob ที่ commit แล้ว: publishJob=1 shellBash=1 branchesIgnore=1 liveOldTrigger=0**

### 🔴🔴 ของแถมที่เจอระหว่างทาง — **บั๊กในโปรโตคอลธงที่ซ่อนมา 16 จ็อบ (160→175)**
จ็อบ gate/commit ทุกใบเขียนธงด้วย `Out-File -Encoding utf8` ซึ่งบน **Windows PowerShell 5.1 ใส่ BOM ให้**
แต่ด่านขอธงในจ็อบเดียวกันเช็ค `'^HELD:'` ซึ่ง **ไม่ match บรรทัดที่มี BOM**
⇒ **ด่านนี้รายงานว่า "ธงว่าง" ตรงเวลาที่ธงถูกถืออยู่พอดี** — พังกลับด้านสนิท และเงียบ
📌 รอบ 108 **เขียนคำเตือนนี้ไว้ในธงเองแล้ว** แต่จ็อบ 175 ยังสืบทอดบั๊กมาเพราะ copy จาก template จ็อบ 169
⇒ **บทเรียนจริงคือ: กฎที่อยู่แต่ในร้อยแก้ว จะถูกเรียนใหม่โดยคนอ่านคนถัดไปเสมอ**

**แก้แล้วสามชั้น:**
1. **ถอด BOM ออกจาก `LOCK_GIT.txt`** แล้ว (ตอนธงว่าง ไม่มีใครถือ) + เขียนกฎติดไว้ในไฟล์ธงเอง
2. `staged\TEMPLATE_lock_flag_helpers.ps1` — `Write-Flag` (ไม่มี BOM) · `Test-FlagHeld` (ทน BOM) · heartbeat
   **แก้สองที่ที่ไม่ขึ้นแก่กัน** เพราะคนเขียนธงกับคนเช็คธงถูกแก้คนละจ็อบคนละเวลา
3. **self-test 4 เคส และมีคนดูมันตัดสินจริง** — จ็อบ 176/177
   🔴 **จ็อบ 176 = FAIL และนั่นคือกำไร**: `"^$bom?HELD:"` ทำให้ PowerShell parse เป็น drive-qualified variable
   แล้วตายทั้งฟังก์ชัน · ต้องเป็น `"^${bom}?HELD:"` · **โค้ดนั้นถูกเรียกเฉพาะตอนมีคนถือธงอยู่**
   ⇒ ถ้าส่ง template ไปโดยไม่รัน **มันจะระเบิดในวันที่มันสำคัญที่สุดพอดี**
   **จ็อบ 177 = `JOB177_VERDICT=PASS` ครบ 4 เคส** รวม **T4 (ไฟล์ HELD ที่มี BOM — เคสที่ด่านเก่าตอบว่า "ว่าง")**
📌 **จ็อบ gate/commit ใบถัดไป (176+) ให้ dot-source template นี้ ห้าม copy ด่านธงจากจ็อบ 169 อีก**

### 🔴 สิ่งที่รอบนี้ *ไม่ได้* อ้าง
- **ทาง D ยังไม่พิสูจน์** — ตามเกณฑ์ที่ Panya วางเอง: *จนกว่าจะเห็น `ci-status` เกิดจริงบน GitHub ห้ามนับว่าใช้ได้*
  การซ้อมทั้งหมดอยู่บน filesystem ไม่ผ่าน proxy ไม่ผ่าน `x-access-token` ไม่ผ่าน permission model ของ Actions
- **ไม่ได้พิสูจน์ว่า `branches-ignore` กันลูปได้จริง** — รู้ได้ต่อเมื่อมี push ลง `ci-status` แล้วไม่มี run เกิด
- 🔴 **สะพานไม่มี pyyaml** ⇒ จ็อบ 175 ตรวจโครง YAML **ไม่ได้** และมันรายงาน `yamlParse=SKIP` ตรง ๆ ไม่แกล้งผ่าน
  **การ parse ที่ทำจริงเกิดใน sandbox** บนไบต์ชุดเดียวกัน (ไฟล์เดียวกันผ่าน mount) — คนละเครื่อง คนละความมั่นใจ
  ⇒ **ถ้าอยากได้ด่านนี้จริงบนสะพาน ต้องตัดสินก่อนว่าจะลง pyyaml ไหม (จ็อบ gate ไม่ใช่ที่ที่ควรลงแพ็กเกจเอง)**
- **repo `pf_bridge` ไม่ถูก commit โดยรอบนี้โดยตั้งใจ** — Panya มี backlog commit ของท่านเองค้างอยู่ที่นั่น
  สองมือเขียน index เดียวกันคือวิธีที่ dirty diff หายไป · เอกสารรอบ 109 อยู่บนดิสก์ครบ รอท่าน commit พร้อมกัน

### 🔴 ด่านตรวจท้ายรอบจับผมได้เอง 2 ข้อ — **บันทึกไว้เพราะมันคือเหตุผลที่ด่านนี้ต้องมี**
1. **ผม `mv` ต้นฉบับจดหมายเข้า `consumed\` ทั้งที่กฎรอบ 108 บอกว่าต้อง *สำเนา* และ "ต้นฉบับอยู่ที่เดิมเสมอ"**
   (เหตุผลของกฎ: **ตัว sync ปฏิเสธ commit ที่มีการลบทั้งก้อน** — เทส T6 พิสูจน์ไว้แล้ว
   ⇒ การย้ายไฟล์จะทำให้ **commit ทั้งใบถูกปฏิเสธ** ไม่ใช่แค่ไฟล์นั้นหาย)
   **แก้แล้ว: คืนต้นฉบับกลับที่เดิม 3 ใบ** (`..._1520_GT027-RERUN-FINAL`, `..._1545_ORDER-pytest-subset`,
   `..._1910_PANYA-APPROVED-path-D`) — สองใบแรกเป็นของค้างจากรอบก่อน ไม่ใช่ของรอบนี้
2. **`URGENT_20260819_1752_STOP-duplicate-chief-run.md` ไม่มี stub `.CONSUMED.txt` มาตั้งแต่ 19 ส.ค.**
   ⇒ กล่องจดหมาย "ยังไม่เคลียร์" ตามนิยามของมันเอง · เขียน stub แล้ว (เนื้อหาปิดไปนานแล้ว:
   ปัญหารอบซ้อนถูกแทนที่ด้วย `cloud_round_lock.json` ซึ่งเป็นล็อกที่ *ได้มาด้วยการ push* ไม่ใช่ด้วยการเขียนไฟล์)
📌 **สแกนหาไฟล์กำพร้าท้ายรอบทุกครั้ง** — `.md` ที่ไม่มี `.CONSUMED.txt` คู่ และไม่ใช่ `FROM_CHIEF_*`/`README.md`

## 🟩 รอบ 108 (2026-08-20 ~17:55–19:1x · scheduled) — **ท่อ sync มีตัวตนแล้ว และถูกพิสูจน์ว่า "ปฏิเสธเป็น" · prompt เป็น A′ แล้ว**

**ทำครบทั้งสองใบสั่งที่มาถึงระหว่างรอบ:** ใบ 18:00 (ดีไซน์ sync ผ่าน → ลงมือ) และใบ 18:30 (A′ + วิธีอ่านผล Actions)
**ธง:** ไม่ถือใบไหนเลยทั้งรอบ · **ไม่ commit ไม่ push ไม่บูตเซิร์ฟ ไม่เปิดเกม ไม่แตะ DB ไม่รัน gate/pytest**

### ของใหม่ที่จับต้องได้
| ไฟล์ | คือ |
|---|---|
| `pf_git_sync.ps1` | ตัว sync 8 ด่านตามดีไซน์ · โหมด `-SelfCheck` / `-DryRun` / `-NoServer` / ชี้ `-BridgeRepo` ไป fixture ได้ |
| `pf_git_sync_selftest.ps1` | เทส 14 ข้อบน bare repo ปลอมใน `%TEMP%` |
| `SETUP_GIT_SYNC.bat` + `setup_git_sync_admin.ps1` | ติดตั้ง `PF_Git_Sync` ครบในคลิกเดียว **`WakeToRun=False`** + trigger logon/unlock + ใบเสร็จ `VERDICT=` |
| `HOWTO_INSTALL_GIT_SYNC.md` | 3 ขั้นสำหรับ Panya + เกณฑ์ 6 ข้อว่าตอนนี้อยู่ตรงไหน |
| `FINDINGS_R108_SYNC_PROVEN_ON_FIXTURES.md` | ใบเสร็จ + nonclaims ของท่อ |
| `FINDINGS_R108_A_PRIME_HOW_TO_READ_ACTIONS.md` | คำตอบข้อ 2 ของใบสั่ง 18:30 + แพตช์ `ci-status` + probe |

### ✅ **`SELFTEST_PASSED=14 FAILED=0`** (จ็อบ 172 18:30 · จ็อบ 173 18:34 ยืนยันซ้ำสะอาด)
รวมข้อที่ Panya เน้น: **T8 non-fast-forward — ไม่ได้เชื่อ exit code แต่ grep หาข้อความจริงใน `sync.log`**
ว่ามีทั้ง `rejected as non-fast-forward` และ `pushed after one rebase` · และ **T7** พิสูจน์ว่าถ้ามีคนแก้ไฟล์ของ chief
ที่เครื่อง มันหยุดเสียงดัง **โดยข้อความที่แก้ไว้ไม่หายสักตัวอักษร**

### 🔴 บทเรียนสามข้อของรอบนี้ (จำไว้ให้ได้ อย่าให้ใครทำซ้ำ)
1. **การ์ดที่ตัดสินจากการ *อ่านข้อความ* ที่มนุษย์อ่านสวย มักตาบอดต่อกรณีกลับด้าน**
   การ์ดธงเวอร์ชันแรกอ่าน output ของ `check-ignore -v` แล้วเห็นชื่อไฟล์ ⇒ ตัดสินว่า "ignore อยู่"
   **แต่ `-v` พิมพ์บรรทัดออกมาแม้กฎที่ตัดสินจะเป็น negation (`!`) ซึ่งแปลว่าไม่ ignore**
   ⇒ แก้เป็นดู **exit code ของ `check-ignore -q` ทีละไฟล์** + เพิ่มเทส **T11b เป็น regression test ของการ์ดเอง**
2. **invariant ที่ "นับ" คือ invariant ที่โกหกได้** — จ็อบ 172 แดงเพราะนับ dirty path 3→4
   ทั้งที่ไฟล์ที่ 4 คือไฟล์ที่ **chief เองวางระหว่างจ็อบกำลังวัด** ⇒ จ็อบ 173 เทียบ **เซต** แล้วพิมพ์ว่าอะไรเข้าออก
3. **วินัย: chief ห้ามเขียนไฟล์ลงโฟลเดอร์ที่จ็อบกำลังวัดอยู่**

### 🧾 จ็อบ 174 (18:54) — **หลังแก้ `.gitignore` ต้องพิสูจน์การ์ดใหม่ ไม่ใช่ยืมหลักฐานเก่า**
การ์ด `[0]` ยังผ่าน · ธงสามใบยัง ignore ครบ · **`cloud_round_lock.json` ยืนยันว่า *ไม่* ถูก ignore** ⇒ `JOB174_VERDICT=PASS`

### 🆕 กติกาใหม่ที่มีผลกับทุกคนทันที — **ห้ามลบ/ย้ายไฟล์ใน `notes_to_chief\`**
ตัว sync **ปฏิเสธ commit ที่มีการลบทั้งก้อน** (T6 พิสูจน์แล้ว) ⇒ บริโภคจดหมายเสร็จ = **สำเนา**ไป `consumed\`
+ วาง stub `.CONSUMED.txt` · **ต้นฉบับอยู่ที่เดิมเสมอ** ⇒ "กล่องว่างหรือยัง" อ่านจาก **`.md` ใบไหนไม่มี `.CONSUMED.txt` คู่กัน**
(ไม่นับ `FROM_CHIEF_*` ซึ่งเป็นขาออก) · ✅ **backfill stub ให้จดหมายเก่าที่บริโภคไปแล้ว 18 ใบเรียบร้อย**
⇒ กฎนี้ให้คำตอบถูกย้อนหลังทั้งกล่อง ไม่ใช่แค่กับของใหม่ · **ตอนนี้กล่องเคลียร์หมดจริง (ตรวจด้วยสคริปต์ ไม่ใช่ด้วยสายตา)**

### 🔴 คำตอบข้อ 2 ของใบสั่ง 18:30 — **ต้องบอกทันทีตามที่ Panya สั่ง**
**อ่านผล Actions จาก Routine: ยืนยันไม่ได้ และหลักฐานเอนไปทาง "อ่านไม่ได้ด้วย gh/API"**
เอกสาร Anthropic: **sandbox ไม่มี credential เลย** git เดินได้เพราะ **proxy ฉีด token ให้ตอนวิ่งออก**
⇒ **ทางหลักที่เสนอ: ให้ workflow เขียนผลของตัวเองลง branch `ci-status` แล้ว chief อ่านด้วย git ล้วน**
(แพตช์เขียนแล้ว ชื่อ job ตรวจแล้ว = `gate` บรรทัด 62 · **ยังไม่ apply เพราะแตะ repo โค้ด**)
🔴 **ความเสี่ยงข้อสองที่ใบสั่งยังไม่ได้พูดถึง: A′ ต้อง `push main` จาก Routine ซึ่งไม่มีใครเคยลอง**
⇒ probe บรรทัดที่ 4 ตอบได้โดยไม่เปลี่ยนอะไรสักไบต์ (`git push origin origin/main:main`) · fallback = **A″ เปิด PR**

### 🔒 ใบสั่ง 18:45 — **การ์ดกันรอบซ้อน (ทำครบแล้วเช่นกัน)**
Panya เคาะ **cadence รายชั่วโมง แต่ต้องมีการ์ดก่อน** เพราะ Routine สร้างเซสชันอิสระทุก trigger
⇒ **chief สองตัวทำงานพร้อมกันได้จริง** และรอบจริงยาวกว่าระยะ trigger เป็นเรื่องปกติ
- **`agent_kit/chief_task_prompt_CLOUD_v3_20260820.md`** = ฉบับที่ต้องเอาไปวางจริง (v2 กลายเป็นประวัติ + SUPERSEDED header)
  หัวข้อใหม่: ล็อกที่ **ได้มาด้วยการ push สำเร็จเท่านั้น** · **push ถูกปฏิเสธ = แพ้ = จบรอบทันที ห้าม retry ห้าม force**
- **`cloud_round_lock.json`** (tracked จริง) + **`.gitignore` เติม `!/cloud_round_lock.json`**
  จงใจไม่ตั้งชื่อ `LOCK_*` และไม่ใช่ `.txt` — ไม่งั้นโดน deny-all กินเงียบ ๆ **ซึ่งคือความล้มเหลวแบบที่การ์ดมีไว้กัน**
  ค่าเริ่มต้นวางไว้เป็น `RELEASED` แล้ว ⇒ รอบแรกไม่ต้องตัดสินใจอะไรกับไฟล์ที่หายไป
- 💰 เหตุผลเรื่องเงินเขียนลง prompt ด้วย: **ชนเพดานรายสัปดาห์ = ทุกอย่างหยุดสนิท ไม่ใช่จ่ายเพิ่ม**
  ⇒ **ความถูกและความถูก(ราคา)ของรอบที่ข้าม เป็นเรื่องเป็นเรื่องตาย** · รอบแรกที่ข้ามจริงต้องรายงาน token เป็นตัวเลข
- ถือ `LOCK_GIT` ~10 นาทีเพื่อแก้ `.gitignore` บรรทัดเดียว แล้วปล่อย (ไม่ commit ไม่ push)

### 🔬 ของแถมที่วัดได้เองระหว่างทาง (เก็บไว้ในธง LOCK_GIT ด้วย)
**`git check-ignore -v` คืน exit 0 และพิมพ์บรรทัดออกมา สำหรับ path ที่ถูก negation เปิดกลับ**
(วัด 18:4x บน git 2.34.1: `-v` → 0 · แบบไม่มี `-v` และ `-q` → 1 สำหรับ path เดียวกัน)
⇒ **การ์ดที่อ่านข้อความของ `-v` ตาบอดในทิศทางที่สำคัญที่สุดพอดี** — ให้ดู exit code ของ `-q` ทีละไฟล์เสมอ

### ค้างอยู่ / รอ Panya
- 🔲 **ติดตั้งท่อ** — `SETUP_GIT_SYNC.bat` (Run as administrator) · จนกว่าจะกด ทุกอย่างข้างบนยังไม่มีผล
- 🔲 **push `pf_bridge` ขึ้น GitHub** — HEAD ที่เครื่อง = `9d346d8` (Panya commit เองอยู่) ยังไม่ยืนยันว่า push แล้ว
- 🔲 **แพตช์ `ci-status` ลง workflow** — ต้องผ่าน gate + Panya push
- 🔲 เพดานรันต่อวันของ routine — Panya คนเดียวที่เปิดหน้านั้นได้ (**ถ้าน้อยกว่า 24 ⇒ ลดเป็นทุก 2 ชม.**)
- 🔲 skill `pf-attended-test` ยังไม่ได้แก้ให้อ่าน `NEW_ORDERS.txt` (สำเนา skill: `agent_kit\skill_pf-attended-test*.md`)
- 🧹 **งานแม่บ้านรอบหน้า: `CHIEF_CONTINUATION.md` = ~99 KB ชนเพดาน ~100 KB แล้ว** ⇒ ย้ายรอบเก่าที่ปิดแล้ว
  ไป `archive/` ทิ้ง pointer (ห้ามลบ) · `GAME_TEST_QUEUE.md` ~89 KB ก็เกิน ~60 KB เช่นกัน
  🔴 แต่คิวมีกฎเหล็กทับอยู่: **ห้ามย้ายรายการที่ยังไม่ได้เทส** — ย้ายได้เฉพาะรอบที่ปิดแล้วกับ evidence เก่า

### nonclaims ของรอบ 108
**ไม่เคย push ขึ้น GitHub จริง** (เทสทั้งหมด push เข้า bare ปลอมใน `%TEMP%`) ⇒ **ไม่ทราบว่าเครื่องนี้มี credential ที่ push ได้ไหม** ·
**ไม่เคยติดตั้ง scheduled task** ⇒ ไม่ทราบว่า trigger unlock ติดจริงไหม · **ไม่เคยรัน `pf_git_sync.ps1` โหมดจริงบนรีโปจริง** ·
**ไม่ได้แตะ `pirate-force-server`** (สะอาดที่ `9045978` ตลอดรอบ) · **ไม่มีผลเทสในเกมใหม่ ไม่มีรายการคิวถูกเพิ่มหรือลบ**

---

## รอบ 107 — ⤴ ย้ายไป archive แล้ว (รอบ 109)

`pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R109_ROUND107.md`
— ดีไซน์ sync ฝั่ง Windows (ทำจริงแล้วรอบ 108) · repo ที่สอง · ข้อเท็จจริงของ Routine
· คำถาม A/B เรื่อง push (เคาะเป็น A′ รอบ 108) · วิธีอ่านผล Actions (เคาะเป็นทาง D รอบ 109)

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

- R112 2026-08-20 ~18:00 UTC v4 live ครั้งแรก: probe ผ่าน (MCP อ่าน API ได้ · gh ไม่มี · ทาง D มีชีวิต) · เขียว(cloud sanity) 948 pass ที่ server 2842fb9 · พบ clone เป็น shallow ต้อง --unshallow · PR ใบนี้ = ทดสอบ merge-claude-pr ฝั่ง bridge ครั้งแรก -> rounds/R112_v4_first_live_round_probe_and_pipeline.md
- R112(xt9cn1) 2026-08-20 ~18:0xZ **รอบ 112 ตัวที่สอง รันพร้อมกันกับตัวบน** (routine ยิงสองเซสชัน ทั้งคู่เห็นล็อกว่างพร้อมกัน) — ท่อ automerge **พิสูจน์ครบสองขาแล้ว**: PR #3 merge เอง ไม่มี 403 · PR #4 ชน merge แล้วถูก bot ปิด+เก็บ branch · เพิ่ม: `curl` ยิง GitHub API ได้จริง (หักล้าง R109/R110) -> rounds/R112_xt9cn1_automerge_proven_and_concurrent_round_evidence.md
  🔴 กฎ "หนึ่งรอบหนึ่งไฟล์" กันการชนนี้ไม่ได้ เพราะสองเซสชันเลือก**เลขรอบและชื่อไฟล์เดียวกันเป๊ะ** ⇒ เสนอ v5: ใส่ท้าย branch ที่สุ่มไม่ซ้ำลงในชื่อไฟล์ทุกใบ

- R113 2026-08-20 ~18:40 UTC LOOT-ROLL-001 (GT-037) build เสร็จ เขียว(cloud sanity) 992 pass · **แก้ข้อเท็จจริง: xt9cn1 ไม่ได้ถูกทิ้ง** — มันเปิด PR #5 ใหม่แล้ว merge สำเร็จ 18:09Z (ดูบรรทัดบน) · PR รอบนี้ = ทดสอบท่อ server ครั้งแรก -> rounds/R113_loot_roller_and_first_server_pipeline_test.md

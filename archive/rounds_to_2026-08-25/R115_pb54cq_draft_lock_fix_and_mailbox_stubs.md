# R115 (pb54cq) — ล็อกรอบที่ "ถือไว้ได้จริง" · รอบ 114 ที่หายไปถูกกู้กลับมา · Door 3 ปิดตายบนคลาว

- **เวลา:** เริ่ม 2026-08-21 04:01 (+07:00) = 2026-08-20 21:01 UTC
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · Python 3.11.15 · pytest 9.1.1
- **branch รอบนี้:** `pf_bridge` -> `claude/zealous-turing-pb54cq` · `pirate-force-server` -> `claude/quirky-ride-pb54cq`
- **ฐานต้นรอบ:** bridge `4eeeee0` (= main หลัง R114 merge) · server `cc46a03` (= main · ci-status `success`)
- **ลูกมือที่ใช้:** `pf-static-re` (สำรวจ Door 3) · `pf-adversary` (หักล้างดีไซน์ล็อก — **จับได้ 1 ข้อที่ทำให้ต้อง revert commit ของตัวเอง**) · `pf-queue-author` (เขียน GT-040)

---

## 1. การ์ดกันรอบซ้อน — ทำตาม v5 แล้วพบว่า v5 ข้อ ① **ไม่ได้ทำให้เกิดล็อกบน `pf_bridge`**

**ทำตามลำดับ v5 เป๊ะ:** `git fetch --all` -> ถาม API -> PR เปิดค้าง **0 ใบทั้งสอง repo**
-> claim commit `31d46e9` "round claim: pb54cq" -> push -> เปิด PR #11 body ขึ้นต้นด้วย `PF-AUTOMERGE: v4` เป๊ะ

### 🔴 ข้อบกพร่อง: `pf_bridge` merge PR **ทันทีที่เปิด** ⇒ ล็อกหลุดก่อนเริ่มงาน

`pf_bridge/.github/workflows/merge-claude-pr.yml:58-60` ยิงงานที่ `types: [opened, reopened, synchronize, edited]`
และ repo นี้ **ไม่มี gate** ⇒ PR ที่เปิดเพื่อ *จับล็อก* ถูก merge และ branch ถูกลบภายในไม่กี่วินาที

**หลักฐานที่ re-derive ได้จาก git ที่ HEAD (ไม่ใช่ความจำ · แก้ตัวเลขผิดของดราฟต์แรกแล้ว):**

| commit | ผู้ commit | เวลา (UTC) | คืออะไร |
|---|---|---|---|
| `da91743` | Claude | 19:00:37 | claim commit ของ lx6eer |
| `a67f935` | **github-actions[bot]** | 19:00:57 | **merge commit ของ PR #8** — ห่างกัน **20 วินาที** |
| `5f03dea` | Claude | 20:00:08 | claim commit ของ lij8pk (**ไม่ใช่ merge commit**) |
| `52908d6` | **github-actions[bot]** | 20:00:28 | **merge commit ของ PR #9** — ห่างกัน **20 วินาที** |

- ผู้ merge เป็น `github-actions[bot]` (= `GITHUB_TOKEN`) ไม่ใช่คนกดผ่านเว็บ (จะขึ้นเป็น `GitHub <noreply@…>`)
- `reap` ของ repo นี้ **ไม่มีคำสั่ง merge เลย** ⇒ ตัด reap ออกจากคำอธิบายได้
- ⇒ ทุกคำอธิบายที่ไม่ใช่ "merge job ทำงานตอน opened" ถูกหักล้างหมด

### 🔴🔴 ราคาที่จ่ายไปแล้วจริง: **รอบ 114 (lx6eer) หายไปทั้งรอบ**

นี่คือหลักฐานที่หนักกว่าตัวเลขวินาที และรอบนี้เพิ่งขุดเจอ:

1. lx6eer เปิด PR #8 เป็น claim -> workflow merge ทิ้งตอน 19:00:57 **แล้วลบ branch**
2. lx6eer ทำงานจนจบ push `e6f502b` ตอน 19:07:18 — **push นี้สร้าง branch ขึ้นมาใหม่ แต่ไม่มี PR ผูกอยู่แล้ว**
3. lx6eer แก้หัวข้อ PR #8 ตอน 19:07:48 ตามขั้นตอนปิดรอบ -> workflow ตื่นขึ้นมาเห็น `state=closed` -> `not open - nothing to do`
4. ⇒ `e6f502b` (บันทึกรอบ 108 บรรทัด + ดัชนีหนึ่งบรรทัด) **ไม่เคยเข้า `main`** · `git ls-tree origin/main rounds/ | grep lx6eer` = 0
5. ⇒ รอบถัดมา (lij8pk) เห็น `rounds/` สูงสุด = R113 จึงตั้งชื่อตัวเองว่า **R114 ซ้ำ**

**รอบนี้กู้กลับมาแล้ว:** `rounds/R114_lx6eer_lock_first_and_backlog_drain.md` (คัดจาก `e6f502b` ด้วย `git show`
ไม่แตะ branch ของเขา ไม่ rebase ไม่ force) · **เนื้อไม่แก้แม้แต่ตัวอักษรเดียว** · ใส่ดัชนีให้ใหม่ท้าย `CHIEF_CONTINUATION.md`
⇒ ตอนนี้ **มีไฟล์ชื่อ R114 สองใบ** (lij8pk และ lx6eer) ซึ่ง **ถูกต้องแล้ว** เพราะมีรอบ 114 เกิดขึ้นจริงสองรอบ

### ✅ สิ่งที่รอบนี้ทำแทน: **เปิด claim PR เป็น DRAFT** (เสนอเป็น v6 ข้อ ① — เฉพาะ `pf_bridge`)

`merge-claude-pr.yml:140` = `[ "$DRAFT" = "false" ] || { echo "draft - skipped"; exit 0; }`
⇒ draft PR **ไม่ถูก merge** แต่ **ยังเป็น "PR เปิดค้าง"** ในสายตาการ์ด ⇒ ถือล็อกได้ตลอดรอบจริง

**พิสูจน์แล้วรอบนี้ ด้วยล็อกของ Actions เอง ไม่ใช่แค่ "run เขียว":**

```
PR #11 claude/zealous-turing-pb54cq -> main state=open draft=true headrepo=panyaasanee/pf_bridge
draft - skipped
```
(run `32417278649` job `96581189078` · 2026-08-20T21:02:04Z)

- ยืนยันซ้ำหลัง push commit ที่สอง: PR #11 ยัง `state=open draft=true` ⇒ `synchronize` ก็ไม่ปลุกให้ merge
- 🔴 **marker ยังเป็น `PF-AUTOMERGE: v4` เป๊ะ ห้ามเปลี่ยนเป็น v5/v6** — มันคือ `PF_MARKER` ที่ workflow จับ

---

## 2. pf-adversary ยิงดีไซน์นี้ — และมันคือรอบที่คุ้มที่สุดของลูกมือจนถึงตอนนี้

สั่งให้ **หักล้าง** ไม่ใช่อนุมัติ · ผลคือ **หักล้างข้อกลางไม่ได้ แต่ยิงตกรายละเอียดจนต้องแก้แผน 4 จุด**

### 🔴 A1 (ร้ายแรงที่สุด) — ลำดับ "ปลด draft" ที่ดราฟต์แรกเขียนไว้ **ทำให้ PR ตายค้าง**
`ready_for_review` **ไม่อยู่ใน** `types:` ของ workflow ⇒ การปลด draft **ไม่ทำให้เกิด run ใด ๆ เลย**
ดราฟต์แรกเขียนลำดับว่า `push -> แก้หัวข้อ -> ปลด draft` ⇒ event สุดท้ายคือ `ready_for_review` ⇒ **ไม่มีอะไร merge ตลอดกาล**
และจะ **ไม่มี run ให้ดูใน Actions ด้วยซ้ำ** (ไม่ใช่ run แดง — คือไม่มี run) ⇒ 6 ชม.ต่อมา `reap` มาปิดทิ้ง **โดยไม่ merge**

✅ **ลำดับที่ถูก (ใช้จริงรอบนี้ และต้องเข้าไปอยู่ใน v6):**
```
push งานให้ครบก่อน  ->  ปลด draft (draft=false)  ->  ค่อยแก้ title/body
```
`edited` **อยู่ใน** `types:` และตอนนั้น job จะอ่าน state สดเห็น `draft=false` ⇒ merge
**ถ้าเลย deadline แล้วยังไม่ merge:** push empty commit เพื่อบังคับ `synchronize` (ห้ามปิด PR เอง ห้าม force)

### 🔴 A2 — ตอนเป็น draft **workflow ไม่เคยตรวจ marker เลย**
ลำดับเช็คคือ state -> **draft** -> head repo -> base -> branch prefix -> **marker**
⇒ ถ้าพิมพ์ marker ผิด จะไม่มีใครรู้จนกว่าจะปลด draft ตอนท้ายรอบ
และ PR ที่ marker ผิด **ทั้ง merge job และ reap มองไม่เห็น** (`:259-261` กรอง marker เหมือนกัน)
แต่ **การ์ดต้นรอบมองเห็น** (v5 §🔒🔒 เช็คแค่ `headRefName`) ⇒ **ล็อกที่ไม่มีใครปลดได้เลยตลอดกาล**
✅ รอบนี้จึงอ่าน body ของ PR #11 กลับมาตรวจ: ขึ้นต้นด้วย `PF-AUTOMERGE: v4\n` เป๊ะ **ผ่าน**
🔴 **v6 ต้องสั่งให้ตรวจ marker ย้อนกลับทุกครั้งหลังเปิด PR** ไม่ใช่เชื่อว่าที่ส่งไปคือที่ถูกบันทึก
(MCP ต่อท้าย footer `_Generated by Claude Code_` ให้เอง — ไม่กระทบ marker เพราะเช็คเป็น substring)

### 🔴 A3 — "ปลด draft ทำได้จริงไหม" คือสมมติฐานที่ทั้งดีไซน์ยืนอยู่ และดราฟต์แรกจะไปทดสอบมัน**ตอนท้ายรอบ**
REST `PATCH /pulls/{n}` **เปลี่ยน draft ไม่ได้** (ต้อง GraphQL `markPullRequestReadyForReview`) และที่นี่ **ไม่มี `gh`**
⇒ ถ้า MCP ทำไม่ได้ = PR ปลด draft ไม่ได้ + ปิดเองก็ไม่ได้ (prompt ห้าม) + เปิด PR ใบใหม่จาก branch เดิมก็ไม่ได้ = **งานหายทั้งรอบ**
✅ **รอบนี้ทดสอบทันทีตั้งแต่ต้นรอบแทน:** `update_pull_request draft=false` -> อ่านกลับ -> `draft=true` -> อ่านกลับ
**ทำได้ทั้งสองทิศ** และ**ไม่มี run ไหนถูกปลุก** (ยืนยันว่า `ready_for_review`/`converted_to_draft` ไม่อยู่ใน `types`)
⇒ ความสามารถนี้ **วัดแล้ว ไม่ใช่สมมติ** และวัดตอนที่ยังมีทางถอย

### 🔴 A4 — **ห้ามเอาท่า draft ไปใช้กับ repo โค้ด**
`pirate-force-server/.github/workflows/merge-claude-pr.yml` เป็นคนละไฟล์: trigger คือ
`workflow_run` (จบ `gate-windows`) + cron `:17` — **ไม่มี `pull_request_target` เลย**
⇒ **v5 ตามตัวอักษรให้ล็อกจริงอยู่แล้วบน repo โค้ด** (ไม่มีอะไรรันตอน `opened`)
⇒ ถ้าเอา draft ไปใช้ที่นั่น: gate จบ -> `decide` เห็น draft -> ข้าม -> ปลด draft ก็ไม่ปลุก gate ใหม่
-> ต้องรอ `reap` **~5 ชั่วโมง** โดยถือล็อกไว้ทั้งหมดนั้น ⇒ ฆ่ารอบถัดไปหลายรอบ
✅ **รอบนี้จึงเปิด PR #2 ของ repo โค้ดแบบ non-draft ตามปกติ** · **v6 ต้องเขียนให้ชัดว่า draft = bridge เท่านั้น**

### ข้ออื่นที่รับไว้เป็นความเสี่ยงที่รู้ตัว (ไม่แก้รอบนี้)
- **A5 branch delete ไม่มี guard:** `:195` `DELETE refs/heads/<branch>` ไม่มี expected-SHA ⇒ ถ้า push ซ้อนจังหวะหลัง merge งานนั้นหาย
  ⇒ **กฎปฏิบัติ: หลังปลด draft แล้ว ห้าม push อะไรอีกเด็ดขาด** (ท่า draft ย้ายหน้าต่างความเสี่ยงนี้มาอยู่ตอนท้ายรอบ)
- **A6 ท่า draft ยกเลิกคุณสมบัติ "ผู้เทสเห็นใบสั่งภายในไม่กี่วินาที"** ที่ v5 บรรทัด 303 โฆษณาไว้ — ของจะถึง `main` ตอนจบรอบเท่านั้น
  และคอมเมนต์ของ `reap` (`:270-275`) ที่เขียนว่า "PR ที่เปิดค้างเกิน 6 ชม. แปลว่า merge job ไม่เคยรัน" **จะกลายเป็นคำวินิจฉัยที่ผิด**
  ⇒ ถ้า Panya รับ v6 ข้อนี้ **ต้องแก้ข้อความใน workflow ด้วย** ไม่ใช่แก้แค่ prompt
- **A7** คอมเมนต์ใน workflow `:174` อ้างว่าสะพาน Windows commit `CHIEF_CONTINUATION.md` ทุกไม่กี่นาที — **ไม่จริง**
  `DESIGN_R107_WINDOWS_SYNC.md` และ `pf_git_sync.ps1` ระบุ allowlist = `notes_to_chief/**` + `evidence_screens/**` เท่านั้น
  ตัวชนจริงคือ **สองรอบคลาวที่ต่อท้ายไฟล์เดียวกัน**

---

## 3. 🔴 pf-adversary จับ commit ของรอบนี้เองได้ — และมัน**ถูก** ⇒ revert แล้ว

**สิ่งที่ทำผิด:** commit `7048d32` เขียน stub 29 ใบชื่อ `<ชื่อ>.md.CONSUMED.txt`
**ความจริง:** convention บนดิสก์และใน git คือ **ตัด `.md` ทิ้ง** -> `<ชื่อ>.CONSUMED.txt`
และ **จดหมายขาเข้าทั้ง 29 ใบมี stub ที่ถูกต้องอยู่บน `main` ครบอยู่แล้ว** (`git ls-tree -r origin/main notes_to_chief/` ยืนยัน)
⇒ กล่องจดหมาย **ว่างอยู่แล้วตั้งแต่ต้นรอบ** · ที่สแกนไม่เจอเพราะ **แพตเทิร์นที่ผมใช้ผิด** — ผิดแบบเดียวกับ
ดราฟต์แรกของ R114 (lij8pk) และเป็นเรื่องเดียวกับที่ R114 (lx6eer) เขียนไว้แล้วแต่บันทึกของเขาไม่เคยขึ้น `main`

**แก้แล้ว:** commit `d185439` ลบทั้ง 29 ใบ ⇒ **diff สุทธิของ branch นี้ต่อ `notes_to_chief/` = 0 ไฟล์**
ไม่มีอะไรของผู้เทสถูกแตะ ทุก path ที่ลบคือ path ที่ commit ก่อนหน้าในบรานช์เดียวกันสร้างขึ้นเอง

🔴 **นี่คือรอบที่สามติดกันที่พลาดเรื่องเดียวกัน ⇒ ต้นเหตุอยู่ที่ตัว prompt ไม่ใช่ที่คนอ่าน**
ตัว prompt เขียนนิยามกล่องว่างไว้ว่า *"มี `.md` ใบไหนที่ยังไม่มี `.CONSUMED.txt` คู่กัน"* ซึ่งอ่านตรงตัวได้เป็น
`X.md` + `.CONSUMED.txt` = `X.md.CONSUMED.txt`
✅ **ขอให้ v6 เขียนให้ไม่กำกวม พร้อมคำสั่งสำเร็จรูป:**
```
for f in notes_to_chief/*.md; do b=$(basename "$f" .md); \
  [ -e "notes_to_chief/$b.CONSUMED.txt" ] || echo "UNCONSUMED: $f"; done
```
(และยกเว้น `FROM_CHIEF_*` กับ `README.md` ซึ่งไม่ใช่จดหมายขาเข้า)

**สถานะจริงของกล่องต้นรอบ: จดหมายใหม่ 0 ใบ** — ใบล่าสุดคือ `20260820_2130_PANYA-STATUS-install-step2-code-repo-only.md`

---

## 4. probe ต้นรอบ

| ข้อ | ผล | หมายเหตุ |
|---|---|---|
| `which gh` | **ไม่มี** | ตอบซ้ำเป็นรอบที่สี่แล้ว — **เสนอ v6 ตัด probe ข้อนี้ทิ้งถาวรเหมือนที่ตัด push-main** |
| GitHub API (ผ่าน MCP) | **ใช้ได้** | list/create/update PR · `actions_list` · `get_job_logs` (อ่าน log ของ job ได้ = ปิดช่องโหว่ D4) |
| ทาง D `ci-status` | **มีชีวิต** | 5 คำตัดสิน · `cc46a03` -> `success` sha ตรง |
| sibling registry | **อยู่จริง** | `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` |

🔴 **ค่าใช้จ่ายที่ต้องระวัง:** เรียก `actions_list` โดยไม่ระบุ `fields` คืน commit message เต็มก้อนทุกใบ
รอบนี้กินไปหลายพัน token ในการเรียกครั้งเดียว — **รอบหลังระบุ `fields` เสมอ**

---

## 5. baseline — เขียว(cloud sanity)

สร้าง exclusion list ด้วยกฎเดียวกับ `gate-windows.yml` (โมดูลที่มี `GameClient`/`capture_v141` **ยกเว้น seam test**) = **43 โมดูล**

- ครั้งแรก: **1 failed**, 1142 passed, 4 skipped — ตัวแดงคือ `tests/test_foundation.py`
  (`git show 5c200e2:migrations/001_initial.sql` exit 128) = **clone เป็น shallow** ไม่ใช่บั๊กโค้ด
- หลัง `git fetch --unshallow`: **1143 passed, 4 skipped, 1819 subtests passed** (42.9s) ⇒ **เขียว(cloud sanity)**
- 🔴 **`git fetch --unshallow` ต้องทำก่อน pytest ทุกรอบ** ไม่งั้นเห็นแดงปลอมหนึ่งใบเสมอ

### 5b. ตรวจซ้ำงาน R114: pointer ของ GT-039 ใช้ได้จริง
```
origin/main                  = cc46a0371c737c2121a9bc86119b81c5b8e595c2
ci/<sha>.json  "sha"         = cc46a0371c737c2121a9bc86119b81c5b8e595c2   (ตรง = กฎ ①)
               "conclusion"  = success                                    (กฎ ②)
               run 32406182274 · 2026-08-20T19:02:16Z
```
⇒ tester re-derive SHA ได้จาก fresh clone จริง — งานของ R114 (lij8pk) ยืนได้

---

## 6. งานเนื้อ ๆ: **Door 3 ของลูปลูท — ปิดตายบนคลาว ทุกคำถามที่เหลือต้องใช้อิมเมจ**

`pf-static-re` สำรวจจาก artifact ที่ commit แล้วเท่านั้น (ไม่มีอิมเมจที่นี่) ได้ผลว่า **6 ประตู**
Door 1 (มอนสเตอร์เกิด/เป็นศัตรู/ตาย) และ Door 2 (ตัดสินใจว่าดรอปอะไร) **สร้างแล้ว** ·
Door 3/4 **ไม่มีเส้นทางเลย** · Door 5/6 มีบางส่วน

**สิ่งที่ตัดสินได้จากของที่ commit แล้ว:** ของในกอง (`loot_roll.roll_mob_loot`) · mob ไหนดรอปชุดไหน ·
ตำแหน่งวาง (`population.py`) · identity ที่ห้ามชนกัน · id ที่ derive จาก name-hash
**สิ่งที่ตัดสินไม่ได้เลยถ้าไม่มีอิมเมจ:** เฟรมไหนพา object ที่ไม่ใช่ actor · pass ลบ/อายุของ object ·
serializer ของ `PickupTerrainThing` · DropThing ถูกสร้างจริงไหม
⇒ **เขียนโมดูลตอนนี้ = ประดิษฐ์ wire format** ซึ่งบ้านนี้ห้าม ⇒ **ออกเป็นใบสั่ง STATIC-ON-BRIDGE แทน (GT-040)**

**ของแถมที่สำคัญกว่า: เจอคำอ้างเกินจริงในเอกสารที่ commit แล้ว ซึ่งเป็นตัวรับน้ำหนักของ Door 3**
`DropThingBoard` และ `DropThingGameObj` **ไม่ได้อยู่ในตาราง 521 คลาส** — ทั้งคู่ `literal_kind=none`,
`in_round86_census=False` (`FACTPACK_L2_CLASSCENSUS001_20260820.tsv:482,483`) และนิยามของ 521 คือ
"มี RTTI type descriptor **และ** runtime name literal" (`...md:34`) ⇒ ไม่มี literal = อยู่ในตารางนั้นไม่ได้
มีแต่ `DropThingModule_Client` (`:484`) และ `PickupTerrainThing` (`:1003`) ที่มี literal จริง
· ไฟล์ต้นทางเองยังขัดกันเอง (บูลเล็ตท้ายเขียนว่า "registration proven for PickupTerrainThing and the Stall family")

**แก้แล้วสองที่ ด้วยการเขียน ERRATUM ข้าง ๆ ของเดิม (ไม่ลบของเดิมสักตัวอักษร):**
- `pf_bridge/FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` -> ERRATUM E1 (คำอ้าง 521) + E2 (`runtime.py:164-174` เป็น pointer ที่ค้าง ของจริงอยู่ `:586-596`)
- `pirate-force-server/drafts/MONSTER_SPAWN_LOOT_STATIC_AND_DESIGN_R100_20260820.md` -> ERRATUM เดียวกัน (PR #2 ของ repo โค้ด)

⇒ **คำตัดสินของ Door 3 ไม่เปลี่ยนทิศ** — ยัง NEGATIVE เหมือนเดิม แต่ **หลักฐานที่หนุนอยู่น้อยกว่าที่เอกสารเคยอ้าง**

### ข้อที่ลูกมือรายงานมาแล้ว **ผมตรวจเองแล้วหักล้าง — ไม่แก้**
`pf-static-re` แจ้งว่ารายงาน LOOT-ROLL-001 เขียน "43 modules excluded" ผิด ควรเป็น 44
**ตรวจแล้ว: 43 ถูกต้อง** — pattern match ได้ 44 ไฟล์จริง แต่ `gate-windows.yml:392` ตัด
`tests/test_foundation_legacy_seam.py` ออกจาก exclusion list โดยเจตนา (มันต้องรัน) ⇒ 44 - 1 = **43**
· บทเรียน: **ลูกมือรายงานอะไรมา ต้องตรวจก่อนแก้เอกสารเสมอ** (รอบนี้ถ้าเชื่อทันที = แก้ของถูกให้ผิด — ซ้ำรอย R114)

---

## 7. คิวเทสเกม (ข้อบังคับ v5 ข้อ ⑤)

**เพิ่มหนึ่งใบ: `GT-040 DROPTHING-TRANSPORT-PROBE-001` (หมวด STATIC-ON-BRIDGE)** — เขียนโดย `pf-queue-author`
เป็นใบสั่งงาน static RE บนเครื่องสะพาน ไม่ต้องบูตเซิร์ฟเวอร์ ไม่แตะ canonical DB ไม่แตะ `LOCK_GAME`
· pass criteria สองชั้นตามกฎ และ **บอกตรง ๆ ว่าชั้น client-observable ว่างเปล่า** เพราะงานนี้ไม่ผลิตผลที่ตาเห็น
· **ผลลบคือผลเต็ม** ไม่ใช่ความล้มเหลว
· **ไม่มีรายการไหนถูกลบหรือย้าย** — GT-001/026/030/031/032/033/034/035/036/038/039 อยู่ครบเหมือนเดิม

**เพิ่มสามแถวใน `IMAGE_ACCESS_COST.tsv`** (Door 3 x2 · Door 4 x1) — ทั้งสามแถว workaround = `no`

---

## 8. ของที่ push รอบนี้

| repo | branch | commit | เนื้อ |
|---|---|---|---|
| `pf_bridge` | `claude/zealous-turing-pb54cq` | `31d46e9` | claim (empty) |
| | | `7048d32` | stub 29 ใบ (**ผิด convention**) |
| | | `d185439` | revert `7048d32` ⇒ สุทธิเป็น 0 |
| | | (ท้ายรอบ) | ERRATUM · GT-040 · IMAGE_ACCESS_COST · R114(lx6eer) ที่กู้มา · บันทึกรอบนี้ · ดัชนี · จดหมาย |
| `pirate-force-server` | `claude/quirky-ride-pb54cq` | `24d5b94` | ERRATUM ใน R100 loot design (1 path · **PR #2 non-draft**) |

**ไม่ได้ทำ (โดยตั้งใจ):** ไม่แตะ `src/` `tools/` `tests/` `scenarios/` `docs/` · ไม่เพิ่ม ledger entry ·
ไม่ขยับ coverage · ไม่บูตเซิร์ฟเวอร์ · ไม่แตะ DB · ไม่ merge เอง · ไม่ปิด PR ของใคร · ไม่แตะ branch ของ lx6eer

---

## 9. 🔴 ที่ต้องให้ Panya เคาะ (เขียนไว้แล้วเดินงานอื่นต่อ ไม่นั่งรอ)

1. **รับ v6 ข้อ ① (claim PR เป็น draft เฉพาะ `pf_bridge`) ไหม** — พร้อมลำดับปิดรอบที่ถูก
   (`push -> ปลด draft -> ค่อยแก้ title/body`) และคำสั่ง "ห้าม push อีกหลังปลด draft"
   ถ้ารับ **ต้องแก้ข้อความใน `merge-claude-pr.yml:270-275` ด้วย** ไม่งั้น reap จะเขียนคำวินิจฉัยผิดลง repo
2. **งานของรอบ 114 (lx6eer) ที่กู้มา** — เนื้อไม่ถูกแก้เลย แต่ **ยังมีรอบชื่อ R114 สองใบ** ปล่อยไว้แบบนี้โอเคไหม
3. **cadence:** คืนนี้มีสองรอบชนกันจริง (00:41/00:59 ตามที่ v5 บันทึก) และรอบ 19:0x หายไปหนึ่งรอบ
   — v5 ห้าม chief แก้เองด้วยการเพิ่มล็อกชั้นสอง ⇒ **ตัวเลข cadence เป็นของคุณคนเดียว**

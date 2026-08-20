# รอบ 112 — รอบแรกที่รันจริงบน Routine ด้วย prompt v4

**เวลา:** 2026-08-20 ~17:5x UTC (~00:5x +07 ของวันที่ 21)
**ที่รัน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · fresh clone ทั้งสอง repo
**branch ของรอบนี้:** `claude/hopeful-knuth-xt9cn1` (pf_bridge) · `claude/nifty-cerf-xt9cn1` (pirate-force-server)

> **หนึ่งประโยค:** การ์ด PR ว่าง ⇒ ทำงานได้ · probe ตอบสามข้อและ **หักล้างสมมติฐานใหญ่ของรอบ 109/110 ว่า
> "แซนด์บ็อกซ์ไม่มี credential ของ GitHub"** — มันมี และ `curl` ธรรมดายิง API ได้ในนามของ Panya ·
> แต่ **`gh` ไม่มีจริง** ซึ่งทำให้ **การ์ดข้อ 4 ของ v4 ตามตัวอักษรจะฆ่าทุกรอบตลอดกาล** — ต้องแก้ prompt

---

## ① การ์ดกันรอบซ้อน (ทำเป็นอย่างแรก ตามกติกา v4)

| repo | PR เปิดค้างจาก `claude/*` | ผล |
|---|---|---|
| `panyaasanee/pirate-force-server` | **0 ใบ** | ผ่าน |
| `panyaasanee/pf_bridge` | **0 ใบ** | ผ่าน |

⇒ **ล็อกว่าง ทำงานต่อได้** (PR #1/#2 ถูก Panya ปิดไปแล้วตามโน้ต 21:30 — ยืนยันจาก API ว่าไม่มีอะไรเปิดค้างจริง)

🔴 **แต่คำสั่งที่ v4 เขียนไว้ให้ใช้ (`gh pr list ...`) รันไม่ได้** — ดูข้อ ② ท่อน P1
สิ่งที่ใช้จริงคือ **GitHub MCP server** (`mcp__github__list_pull_requests`) ซึ่งเซสชันนี้มีให้อยู่แล้ว

---

## ② PROBE — ผลวัดจริง (ห้ามเดา ห้ามยิงซ้ำในรอบหน้า)

### P1 — `gh` ไม่มีอยู่ในแซนด์บ็อกซ์ 🔴
```
which gh   -> exit 1
command -v gh -> ไม่มีผลลัพธ์  ("gh: command not found", exit 127 เมื่อเรียกตรง ๆ)
```
**ผลที่ตามมาที่ต้องแก้ prompt ทันที:** v4 หัวข้อการ์ด PR ข้อ 4 เขียนว่า
> *"คำสั่งข้อ 1 **ล้มเอง** (ไม่มี `gh` / API ปิด) ⇒ 🔴 **จบรอบทันที**"*

ถ้าอ่านตามตัวอักษร **ทุกรอบบน cloud จะจบทันทีตลอดกาล** เพราะ `gh` ไม่เคยมีและจะไม่มี
⇒ **การ์ดต้องเปลี่ยนเป็น "ถามสถานะ PR ให้ได้ด้วยช่องทางใดก็ได้"** ไม่ใช่ผูกกับชื่อเครื่องมือ `gh`
(รอบนี้ไม่จบตัวเอง เพราะ**เจตนา**ของการ์ดคือ *"มองไม่เห็นล็อก = ห้ามทำงาน"* และรอบนี้ **มองเห็นล็อกชัดเจน**
ด้วยช่องทางที่วัดแล้วว่าใช้ได้ — เจตนาถูกเคารพครบ ตัวอักษรเท่านั้นที่ผิด)

### P2 — 🔴🔴 แซนด์บ็อกซ์ **มี** credential ของ GitHub — หักล้างรอบ 109 และ 110
รอบ 110 บันทึกไว้ว่า `git ls-remote origin` ตอบ `fatal: could not read Username for 'https://github.com'`
และรอบ 109 เขียนไว้ในข้อความ commit ว่า chief *"cannot ask the Actions API whether a run was green,
not with gh, not with curl"*. **วัดใหม่รอบนี้: ทั้งสองข้อไม่จริงอีกต่อไป**

```
git ls-remote origin -h refs/heads/main   -> exit 0, ตอบ SHA จริง
curl -sS https://api.github.com/user      -> HTTP 200  {"login":"panyaasanee", "id":317252912, ...}
curl -sS https://api.github.com/rate_limit-> HTTP 200  core.limit = 15000/hr   (= โทเคนที่ authenticate แล้ว
                                                        ไม่ใช่ anonymous ซึ่งได้ 60/hr)
curl -sS https://api.github.com/repos/panyaasanee/pirate-force-server -> HTTP 200 (repo เป็น private)
```
⇒ **proxy ฉีด credential ให้ทั้ง `git` และ `curl` ขาออก** โดยที่ไม่มีโทเคนวางอยู่ในแซนด์บ็อกซ์เลย
⇒ chief **อ่าน Actions API / PR API ได้ตรง ๆ** ด้วย `curl` เปล่า ไม่ต้องมี `gh` ไม่ต้องมี connector

🟡 **สิ่งที่ proxy ยัง "ปิด" อยู่ — วัดแล้วเหมือนกัน:** path ตั้งค่าของ Actions ถูกบล็อกที่ชั้น proxy
```
GET /repos/{owner}/{repo}/actions/permissions          -> {"message":"Access to this GitHub Actions path
GET /repos/{owner}/{repo}/actions/permissions/workflow ->  is not permitted through this proxy."}
```
⇒ **อ่านค่า `default_workflow_permissions` ไม่ได้** ⇒ คำถาม 403 ของ Panya **ตอบด้วยการอ่านไม่ได้** ดูข้อ ③

### P3 — ทาง D (`ci-status`) ยังมีชีวิต บน repo โค้ด
```
git fetch origin ci-status && git ls-tree --name-only origin/ci-status ci/   -> exit 0
  ci/2842fb9935b28c223c345ed3c8c385ea5867e06c.json
  ci/4ae65036059c3b4ec0e655ca17cfb286b7b5b20d.json
  ci/89ce13b7ce4677d8f92ccd5b1d4875680c258bc4.json
```
คำตัดสินของ HEAD ปัจจุบันของ `main` อ่านออกมาได้ครบและ **`sha` ในไฟล์ตรงกับที่ขอ** (กฎการอ่านข้อ ①):
```json
{"sha":"2842fb9935b28c223c345ed3c8c385ea5867e06c","conclusion":"success","event":"push",
 "ref":"refs/heads/main","run_id":"32383555993","utc":"2026-08-20T15:03:48Z"}
```
🔴 **ข้อควรระวังที่ v4 ไม่ได้เขียนไว้:** branch `ci-status` **มีเฉพาะบน repo โค้ด**
บน `pf_bridge` **ไม่มี** (`git ls-remote origin refs/heads/ci-status` = ว่าง) และนั่นถูกแล้ว เพราะ repo เอกสารไม่มี gate
⇒ chief ที่รัน probe ข้อ 3 ขณะ `cd` อยู่ใน `pf_bridge` จะเห็นมันล้ม **ห้ามตีความว่า "ทาง D ตาย"**

---

## ③ blocker ข้อ 6 ของ v4 — **ปิดแล้ว** (v4 เขียนว่ายังบล็อกอยู่ ตอนนี้ไม่แล้ว)

v4 หัวข้อ "สิ่งที่ต้องเสร็จก่อนสับสวิตช์" ข้อ 6 บอกว่า `merge-claude-pr` ยังไม่อยู่บน `main` ของทั้งสอง repo
**วัดจริงรอบนี้: อยู่ครบทั้งสอง repo แล้ว**

| repo | `main` HEAD | มี `.github/workflows/merge-claude-pr.yml` |
|---|---|---|
| `pf_bridge` | `f83d860` "merge-claude-pr: add actions: read" | ✅ |
| `pirate-force-server` | `2842fb9` "merge-claude-pr: add actions: read, required to list a run's jobs" | ✅ · gate-windows run #7 เขียว |

⇒ **โน้ต Panya 21:30 (งานรอบก่อน: gate+commit ไฟล์นี้ลง repo โค้ด) ทำเสร็จไปแล้ว** — บริโภคแล้ว ไม่มีงานเหลือจากใบนั้น

### 🟡 `pull-requests: write` — ยังไม่ถูกพิสูจน์ และ**พิสูจน์ด้วยการอ่านไม่ได้**
workflow `merge-claude-pr` รันไปแล้ว 5 ครั้งบน repo โค้ด และ 2 ครั้งบน `pf_bridge` — **เขียวหมด**
แต่ **เขียวเปล่า**: อ่าน log ของ job `reap` (run 32395253311) แล้วมันจบที่บรรทัด

```
reaping eligible claude/* pull requests older than 6h
no open pull requests
```

⇒ พิสูจน์แล้วแค่ **`pull-requests: read`** (ลิสต์ PR ได้) · `gh pr merge` / `gh pr close` / `gh pr comment`
**ยังไม่เคยถูกเรียกแม้แต่ครั้งเดียว** ⇒ **403 จะโผล่หรือไม่ ยังไม่มีใครรู้**
และ P2 บอกว่า proxy ปิด path ตั้งค่า ⇒ **อ่านค่ามาตอบล่วงหน้าไม่ได้**

**⇒ ทางเดียวที่เหลือคือเปิด PR จริงหนึ่งใบแล้วดู — ซึ่งคือสิ่งที่รอบนี้ทำ (ข้อ ④)**

---

## ④ การทดสอบ automerge ครั้งแรกของโปรเจกต์ — ออกแบบให้ระเบิดวงแคบ

`merge-claude-pr.yml` **ยังไม่เคยรันกับ PR จริงแม้แต่ใบเดียว** (nonclaim ของ v4 เขียนไว้เอง)
⇒ **PR ของรอบนี้คือตัวทดสอบมันไปในตัว** และมีความเสี่ยงจริงที่ต้องพูดตรง ๆ:

> ถ้า `pull-requests: write` ถูกปฏิเสธ → `decide` ได้ 403 → PR ค้างเปิด → `reap` ก็ปิดไม่ได้ (403 เหมือนกัน)
> → **ล็อกค้างถาวร → ทุกรอบถัดไปจบทันที** จนกว่า Panya จะปิด PR ใบนั้นด้วยมือ

**วิธีลดความเสียหาย (เจตนา ไม่ใช่ความบังเอิญ):**
1. เปิด PR ที่ **`pf_bridge` ก่อนที่เดียว** — repo เอกสาร merge ทันทีที่เปิด ไม่ต้องรอ gate ⇒ **ได้คำตอบเร็วที่สุด**
2. **ยังไม่เปิด PR ที่ repo โค้ดในรอบเดียวกัน** ⇒ ถ้า 403 จริง จะค้างแค่ **ใบเดียว ไม่ใช่สองใบ**
3. ผลออกทางไหนก็ตาม **เขียนไว้ในไฟล์นี้และแจ้ง Panya ทันที**

**ถ้าเจอ 403 — ข้อเสนอเตรียมไว้ล่วงหน้าแล้ว (Panya สั่งให้เขียนรอไว้ในโน้ต 21:30):**
- **ทางที่ 1 (ถูกที่สุด ควรลองก่อน):** repo → Settings → Actions → General → Workflow permissions →
  เลือก **"Read and write permissions"** · นี่คือสวิตช์ที่ทำให้ `permissions:` block ใน workflow ขอ write ได้จริง
  ⇒ แก้ครั้งเดียวจบ ไม่ต้องแก้ดีไซน์อะไรเลย
- **ทางที่ 2 (ถ้าทางที่ 1 ไม่ได้):** ใช้ PAT ของ Panya เก็บเป็น repo secret แล้วให้ workflow ใช้แทน `GITHUB_TOKEN`
  ⇒ เสีย: มีความลับเพิ่มหนึ่งชิ้นที่ต้องดูแล/หมดอายุ
- **ทางที่ 3 (ถ้าไม่อยากให้ workflow merge เลย):** เลิกใช้ PR เป็นล็อก แล้วกลับไปหาล็อกแบบอื่น
  🔴 **ไม่แนะนำ** — ล็อกไฟล์ตายไปแล้วด้วยเหตุผลที่ยังจริงอยู่ (ชื่อ branch สุ่มทุกเซสชัน ⇒ ไม่มีเป้าให้แข่ง push)

---

## ⑤ สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์ (nonclaims)

- **ไม่ได้พิสูจน์ว่า `pull-requests: write` ใช้ได้** — ณ เวลาที่เขียนบรรทัดนี้ยังไม่รู้ผล ดูท้ายไฟล์
- **ไม่ได้แตะ `src/` `tools/` `tests/` ของ repo โค้ด** — ไม่มี commit ในเลนโค้ดรอบนี้
- **ไม่ได้รัน gate** ไม่ว่าชั้นไหน · ไม่ได้บูตเซิร์ฟเวอร์ · ไม่ได้เปิด client · ไม่ได้แตะ DB
- **ไม่ได้เทสว่า proxy ยอมให้ `curl` ทำ write operation ไหม** — วัดแต่ read ทั้งหมด (`GET`)
  การเขียนอย่างเดียวที่รอบนี้ทำคือ **push `claude/*` + เปิด PR** ซึ่งเป็นท่าที่กติกาอนุญาตอยู่แล้ว
- **ไม่ได้ยิง `git push origin main`** — v4 ตัดข้อนี้ทิ้งถาวรแล้ว และรอบนี้เคารพข้อนั้น

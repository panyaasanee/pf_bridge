# FINDINGS R108 — **"cloud chief อ่านผล Actions ได้ยังไง"** และคำเตือนสองข้อที่ต้องอ่านก่อนเปิดใช้ A′

---

## ⛔ CORRECTION 2026-08-20 ~20:35 — **ข้อสรุปหลักของเอกสารนี้ผิด และถูกวัดจริงแล้วว่าผิด**

> เอกสารเดิม **ไม่ถูกลบและไม่ถูกแก้** ทั้งฉบับ อ่านต่อได้ตามปกติ แต่ต้องอ่านผ่านบล็อกนี้ก่อน

**ข้อความที่ผิด (คำหลัก):** *"chief ที่รันใน Claude Code Routine ไม่มี GitHub credential ในแซนด์บ็อกซ์
⇒ ถามผล Actions ผ่าน GitHub API ไม่ได้ ไม่ว่าจะด้วย `gh`, `curl` หรือ connector"*
ปรากฏเป็นแกนของ **ข้อ 0 (บรรทัด ~10-14)** · **ตาราง ข้อ 1 แถว B/C** · **ข้อ 2** · **คอมเมนต์ในแพตช์ ข้อ 3** · **ข้อ 6 NONCLAIMS**

**ผิดยังไง:** เอกสารเอา *กลไก* ที่อ่านจากเอกสาร Anthropic (proxy ฉีด credential ให้ git · sandbox ไม่เก็บ token ·
โดเมนไม่เปิดล่วงหน้า) มาอนุมานเป็น *ข้อเท็จจริงเชิงผล* ว่า "อ่าน API ไม่ได้" ทั้งที่ยังไม่มีใครยิงจริงสักครั้ง
กลไกอาจถูก แต่ **ข้อสรุปเรื่องความสามารถผิด** — ของจริงอ่าน API ได้

**หลักฐานที่หักล้าง (cloud round 110 และ 111 — สองรอบแรกที่รันบนคลาวด์จริง):**
- **รอบ 111 อ่าน GitHub API ได้จริง** — คำพูดที่ยกมาตรง ๆ คือ *"verified directly against the GitHub API"*
- **รอบ 110 เปิด PR #1 ได้ · รอบ 111 เปิด PR #2 ได้** ⇒ ไม่ใช่แค่ **อ่าน** เท่านั้น **เขียน** ผ่าน API ก็ทำได้อย่างน้อยหนึ่งอย่าง
- **วันเวลา / ผู้วัด:** Panya รายงานตรง ๆ **2026-08-20 ~20:35** หลังรัน cloud round 110 และ 111

**ข้อจำกัดจริงคือคนละเรื่องกับที่เอกสารนี้เดา — สองข้อนี้ต่างหากที่วัดแล้วว่าจริง:**
1. **push `main` ถูกปฏิเสธที่ชั้น sandbox** (นี่คือ "ความเสี่ยงข้อสอง" ในข้อ 4 — ข้อนั้นเดาถูก แต่คนละข้อกับข้อ 0)
2. **ชื่อ branch สุ่มใหม่ทุกเซสชัน** ⇒ ห้ามเขียนโค้ด/prompt ที่ hardcode ชื่อ branch ข้ามรอบ

### ทาง D (branch `ci-status`) **ยังเก็บไว้ ไม่เสียเปล่า** — แค่เปลี่ยนตำแหน่ง
- คุณค่าเดิมที่เอกสารนี้ให้ไว้: *"ช่องทางเดียวที่เป็นไปได้"* ⇒ **ข้อนี้ตกไป** เพราะ API ใช้ได้จริง
- คุณค่าใหม่: **ช่องทางสำรองที่ไม่พึ่ง API เลย** — ใช้ git ล้วน ยังคงมีประโยชน์ในวันที่ API/โดเมนถูกปิด
  หรือ credential ของ routine เปลี่ยน และไม่มี race แบบ "ถาม API ตอนที่ยังรันไม่จบ"
- **รอบ 111 พิสูจน์แล้วว่ามันทำงานจริง** — อ่าน `conclusion: success` ออกมาได้จาก branch `ci-status`
- ⇒ **ห้ามรื้อทาง D ทิ้ง** ให้คงไว้เป็นเส้นทางที่สอง และให้ API เป็นเส้นทางหลักเมื่อใช้ได้

### บทเรียน (สำคัญกว่าตัวข้อเท็จจริงที่ผิด)
รอบ 108 **เดา** ว่าอ่าน API ไม่ได้ แล้วเขียนคำเดานั้นออกมา **ด้วยน้ำเสียงของข้อเท็จจริง** — หัวข้อ 0 ขึ้นต้นว่า
"คำตอบตรง ๆ" ทั้งที่ไม่มีการยิงจริงแม้แต่คำสั่งเดียว (ข้อ 6 ยอมรับไว้เอง แต่ตัวบทข้างบนไม่ได้พูดด้วยน้ำเสียงนั้น)
ผลคือรอบถัดมาเกือบเสียเวลาไปสร้างทางอ้อมให้ปัญหาที่ไม่มีจริง และเกือบมองข้ามข้อจำกัดจริง (push `main`, branch สุ่ม)
**นี่คือความผิดพลาดของวิธีทำงาน ไม่ใช่แค่ข้อเท็จจริงผิดดวงเดียว** — กติกาต่อจากนี้: สิ่งที่ยังไม่ได้ยิงจริง
ต้องเขียนกำกับว่า **"ยังไม่ได้วัด"** เสมอ และห้ามให้ข้อความที่ยังไม่ได้วัดไปนั่งอยู่ในตำแหน่งของข้อสรุป

---

**ใบสั่ง:** `notes_to_chief\20260820_1830_PANYA-DECISION-cloud-prompt-A-prime.md` ข้อ 2
**คำสั่งของ Panya ตรง ๆ:** *"ถ้าอ่านไม่ได้ ทาง A′ พังทั้งทาง ⇒ ต้องบอกทันที อย่าเขียน prompt ที่สั่งให้ทำสิ่งที่ทำไม่ได้"*

---

## 0. คำตอบตรง ๆ ก่อน (แล้วค่อยดูเหตุผล)

🔴 **ผมยืนยันไม่ได้ว่าอ่านได้ และหลักฐานที่มีเอนไปทาง "อ่านไม่ได้ด้วยวิธีที่เรานึกถึงกันตอนแรก"**
เอกสารของ Anthropic เรื่อง Claude Code on the web ระบุว่า **ไม่มี credential อยู่ใน sandbox เลย** —
git ทำงานผ่าน **proxy ที่ฉีด token ให้ตอนวิ่งออก** และ *"ตรวจเนื้อหาของ git interaction ก่อน"*
⇒ ใน sandbox ไม่มี token ให้ `gh` หรือ `curl` ใช้ยิง `api.github.com` และ repo เป็น private
⇒ **การอ่าน Actions ด้วย API/gh จากใน sandbox ไม่ใช่สิ่งที่วางแผนพึ่งได้** จนกว่าจะมีใครยิงจริงแล้วเห็นว่าได้

> **[แก้ 2026-08-20: ข้อความข้างบนผิด — รอบ 111 อ่าน API ได้จริง ("verified directly against the GitHub API") และรอบ 110/111 เปิด PR ได้ ดู CORRECTION ด้านบน]**

⭐ **แต่ A′ ไม่พัง** — เพราะมีทางที่ **ใช้ช่องทางเดียวที่พิสูจน์แล้วว่าทำงาน คือ git เอง**
👉 **ให้ workflow เป็นคนประกาศผลของตัวเองลง git** (ข้อ 3 ข้างล่าง — ผมแนะนำอันนี้เป็นทางหลัก ไม่ใช่ทางสำรอง)

> **[แก้ 2026-08-20: "ช่องทางเดียวที่พิสูจน์แล้ว" ผิด — API ก็ใช้ได้ · ทาง D ยังเก็บไว้แต่เป็น **ช่องทางสำรองที่ไม่พึ่ง API** ไม่ใช่ทางเดียว ดู CORRECTION ด้านบน]**

🔴 **และมีความเสี่ยงข้อสองที่ใบสั่งยังไม่ได้พูดถึง ซึ่งอันตรายกว่าข้อแรก:**
**A′ สั่งให้ cloud chief `push main` เอง** แต่กติกา push ของ Routine ที่เราจดไว้เองบอกว่า
*branch ที่ขึ้นต้น `claude/` รับเสมอ · branch อื่นรับก็ต่อเมื่อไม่ถูก protect · ไม่มี PR ค้าง · ไม่มี commit ของคนอื่น*
⇒ **ยังไม่มีใครเคยยิง push ขึ้น `main` จาก Routine สักครั้ง** ถ้า proxy ปฏิเสธ **A′ พังที่ขาที่สอง ไม่ใช่ขาแรก**
(ข้อ 4 มีทางลงให้แล้ว)

---

## 1. ทางที่เป็นไปได้ทั้งหมด เรียงตามความน่าเชื่อถือ

| # | วิธี | ต้องมีอะไร | ประเมิน |
|---|---|---|---|
| **D** | **workflow เขียนผลของตัวเองลง branch `ci-status` แล้ว chief อ่านด้วย `git fetch`** | แก้ workflow 1 ก้อน | ⭐ **แนะนำ — ใช้ git ล้วน ไม่ต้องมี token ไม่ต้องเปิดโดเมนใหม่** |
| A | GitHub **connector/MCP** ที่ผูกกับ routine (ทำงานฝั่งเซิร์ฟเวอร์ ไม่ใช่ใน sandbox) | Panya เปิด connector ให้ routine | **เป็นไปได้จริง แต่ไม่มีใครยืนยัน** ⇒ ต้อง probe |
| B | `gh run list` ใน sandbox | `gh` ติดตั้ง + auth | **น่าจะไม่ได้** — ไม่มี token ใน environment · `gh auth login` เป็น interactive |
| C | `curl https://api.github.com/...` | token + โดเมนอยู่ใน allowlist | **น่าจะไม่ได้** — repo private ต้อง auth และ *"no domains are pre-allowed by default"* |

> **[แก้ 2026-08-20: คอลัมน์ "ประเมิน" ของแถว A/B/C ผิด — รอบ 111 เข้าถึง GitHub API ได้จริง (อ่าน) และรอบ 110/111 เปิด PR ได้ (เขียน) · แถว D ยังใช้ได้แต่สถานะเปลี่ยนจาก "ทางเดียว" เป็น "ทางสำรอง" ดู CORRECTION ด้านบน]**

> หมายเหตุที่ต้องพูดให้ชัด: ข้อ B/C ที่ผมเขียนว่า "น่าจะไม่ได้" มาจาก **การอ่านเอกสาร ไม่ใช่การยิงจริง**
> เอกสารบอกกลไก (proxy ฉีด credential ให้ git · sandbox ไม่มี credential · โดเมนไม่เปิดล่วงหน้า)
> การอนุมานจากกลไกไปสู่ "ทำไม่ได้" ยังเป็นการอนุมาน ⇒ **ข้อ 5 คือ probe ที่ตัดสินได้ใน 30 วินาที**

> **[แก้ 2026-08-20: ย่อหน้านี้เดาถูกว่า "เป็นการอนุมาน" แต่ผลของการอนุมานผิด — ยิงจริงแล้วในรอบ 110/111 อ่าน API ได้ ดู CORRECTION ด้านบน]**

---

## 2. ทำไม D ถึงเป็น "ทางหลัก" ไม่ใช่ "ทางสำรอง"

หลักดีไซน์ของโปรเจกต์นี้ที่ Panya วางเอง: **"เหมือนจริงใช้จริง ทำครั้งเดียวจบ" > "ง่ายวันนี้แต่รื้อทีหลัง"**

- **git คือช่องทางเดียวที่เรามีหลักฐานว่าทำงานจากทั้งสองฝั่ง** (Routine clone ได้จริง — probe 15:4x
  พิสูจน์ไฟล์ครบ 228/519 · และตัว sync ฝั่ง Windows รอบนี้พิสูจน์แล้วว่า push/pull/rebase เดินได้)
  ทุกทางอื่นเพิ่ม **ช่องทางที่สองที่พังได้เอง** เข้ามาในเส้นทางที่สำคัญที่สุดของระบบ
- ผลที่ workflow ประกาศเอง **เป็นความจริงจากปากผู้รู้** — runner เป็นคนรู้ว่าตัวเองเขียวหรือแดง
  ไม่ต้องมีใครไปถามใครแทน และไม่มี race แบบ "ถาม API เร็วไปตอนที่ยังรันไม่จบ"
- มันทำงาน **แม้ในวันที่ทุก HTTP นอก proxy ถูกปิด** ซึ่งเป็นทิศทางที่ sandbox กำลังเดินไป

> **[แก้ 2026-08-20: เหตุผล "git คือช่องทางเดียวที่มีหลักฐาน" ผิด — API ก็มีหลักฐานแล้วจากรอบ 111 · แต่ bullet ข้อสุดท้าย (ทำงานแม้ HTTP ถูกปิด) ยังจริง และเป็นเหตุผลที่ทำให้ **เก็บทาง D ไว้เป็นช่องทางสำรอง** ดู CORRECTION ด้านบน]**

### ราคาที่ต้องจ่าย (เขียนไว้ให้ครบ)
- ต้องแก้ `.github/workflows/gate-windows.yml` **ซึ่งแตะ repo โค้ด ⇒ ต้องผ่าน gate + Panya push**
- branch `ci-status` จะโตเรื่อย ๆ (ไฟล์ละไม่กี่ร้อยไบต์ต่อ run) — ปีละไม่กี่ MB ยอมรับได้ และ prune ได้ทีหลัง
- ถ้า job สุดท้ายไม่ได้รัน (เช่น runner ตายกลางคัน) **จะไม่มีไฟล์สถานะ** ⇒ chief ต้องอ่านว่า
  "ไม่มีไฟล์" = **ยังไม่รู้ผล** ไม่ใช่ "เขียว" — เขียนไว้ใน prompt แล้ว

---

## 3. แพตช์ที่พร้อมใช้ (ยังไม่ได้ apply — แตะ repo โค้ด ต้องรอ Panya)

> ⚠️ **อัปเดต 2026-08-20 ~19:2x (chief รอบ 109): Panya เคาะทาง D แล้ว และแพตช์ถูก apply ไปแล้ว
> — แต่ *ไม่ใช่ตามร่างข้างล่างนี้เป๊ะ ๆ* มันต่างกัน 6 อย่าง และข้อแรกคือบั๊กจริงในร่างนี้**
> (ร่างนี้ไม่มี `shell: bash` ทั้งที่ไฟล์ workflow ตั้ง `defaults: shell: pwsh` ⇒ `set -euo pipefail` จะถูกข้าม
> และ step จะเขียวทั้งที่ push ไม่ขึ้น) · **ร่างข้างล่างเก็บไว้เป็นประวัติ อย่าเอาไปใช้**
> **ของที่ลงไปจริงและหลักฐานการซ้อม:** `FINDINGS_R109_PATH_D_APPLIED_AND_REHEARSED.md`

ต่อท้าย `.github/workflows/gate-windows.yml` เป็น **job ใหม่ที่รันหลัง job เดิมเสมอ** (`if: always()`)

```yaml
  publish-status:
    # Why this exists: a chief running in a cloud Routine has no GitHub token -
    # git works only because a proxy injects credentials on the way out - so it
    # cannot ask the API whether this run was green.  The runner knows, so the
    # runner writes it down where the only proven channel can reach it: git.
    needs: [gate]            # ตรวจแล้ว: ไฟล์นี้มี job เดียว ชื่อ `gate` (บรรทัด 62)
    if: always()
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Publish the verdict to the ci-status branch
        env:
          CONCLUSION: ${{ needs.gate.result }}
          SHA: ${{ github.sha }}
          REF: ${{ github.ref }}
          RUN_ID: ${{ github.run_id }}
        run: |
          set -euo pipefail
          git init -q status_repo && cd status_repo
          git config user.name  "gate-windows"
          git config user.email "gate-windows@users.noreply.github.com"
          git remote add origin "https://x-access-token:${{ github.token }}@github.com/${{ github.repository }}.git"
          # ci-status is an orphan branch: it shares no history with main on purpose.
          if git fetch -q origin ci-status; then git checkout -q FETCH_HEAD -b ci-status
          else git checkout -q --orphan ci-status; fi
          mkdir -p ci
          printf '{"sha":"%s","ref":"%s","conclusion":"%s","run_id":"%s","utc":"%s"}\n' \
            "$SHA" "$REF" "$CONCLUSION" "$RUN_ID" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "ci/$SHA.json"
          cp "ci/$SHA.json" ci/latest.json
          git add ci
          git commit -q -m "ci: $CONCLUSION $SHA"
          # Another run may have pushed between our fetch and our push.  Rebase once
          # and try again; never force, exactly like the Windows sync.
          git push -q origin ci-status || { git pull -q --rebase origin ci-status && git push -q origin ci-status; }
```

> **[แก้ 2026-08-20: คอมเมนต์ `Why this exists` ในแพตช์ข้างบนผิด — ประโยค "a chief running in a cloud Routine has no GitHub token ... so it cannot ask the API" ถูกหักล้างแล้วโดยรอบ 111 · ตัวแพตช์เองยังถูกต้องและยังใช้อยู่ (รอบ 111 อ่าน `conclusion: success` จาก `ci-status` ได้จริง) เหตุผลของมันเปลี่ยนเป็น "ช่องทางสำรองที่ไม่พึ่ง API" ดู CORRECTION ด้านบน]**

**ฝั่ง cloud chief อ่านแบบนี้ (ไม่ต้องมี token ไม่ต้องมี gh):**
```bash
git fetch origin ci-status
SHA=$(git rev-parse origin/claude/r107-something)
git show "origin/ci-status:ci/$SHA.json"     # ไม่มีไฟล์ = ยังไม่รู้ผล ไม่ใช่เขียว
```

> **[หมายเหตุ 2026-08-20: สคริปต์อ่านข้างบนยังใช้ได้ แต่บรรทัด `origin/claude/r107-something` เป็นชื่อสมมติ — ของจริง **ชื่อ branch สุ่มใหม่ทุกเซสชัน** ห้าม hardcode ข้ามรอบ ให้หาชื่อ branch ของรอบนั้นตอน runtime]**

🔴 **ก่อน apply ต้องเช็ค 3 อย่าง:** ชื่อ job จริงใน `needs:` · `github.token` ต้องมีสิทธิ์ `contents: write`
(ตั้งไว้ที่ job แล้ว) · และ **push ด้วย `GITHUB_TOKEN` ไม่ทำให้ workflow ยิงตัวเองซ้ำ** (กติกาของ GitHub — กันลูป)

---

## 4. ความเสี่ยงข้อสอง — **A′ ต้อง push `main` และเรายังไม่เคยลอง**

A′ สั่งว่า *รอบ N+1 เห็นเขียว ⇒ fast-forward `main` แล้ว push*
แต่เอกสาร Routine บอกว่า branch ที่ไม่ใช่ `claude/*` ถูกรับ **แบบมีเงื่อนไข**

| ถ้า push `main` … | ทำอะไรต่อ |
|---|---|
| **สำเร็จ** | A′ เดินได้เต็มตัว ✅ **เขียนผลลง `CHIEF_CONTINUATION` ทันทีในรอบนั้น** เพื่อไม่ให้ใครต้องมาลองซ้ำ |
| **ถูกปฏิเสธ** | 🔴 **ห้าม force ห้ามหาทางอ้อม** ⇒ ตกลงมาที่ **A″: เปิด PR จาก branch นั้นแล้วเขียนในจดหมายว่า "รอ Panya กด Merge"** และ **เสนอให้ Panya ลด cadence** เพราะราคาของการกดจะได้ต่ำลง (ทุก 3 ชม. = 8 ครั้ง/วัน ไม่ใช่ 24) |

> **[อัปเดต 2026-08-20: ข้อนี้ **เดาถูก และวัดแล้ว** — รอบ 110/111 ยืนยันว่า **push `main` ถูกปฏิเสธที่ชั้น sandbox** ⇒ เดินทาง A″ จริง คือเปิด PR (PR #1 รอบ 110 · PR #2 รอบ 111) แล้วรอ Panya merge · ต่างจากข้อ 0 ที่เดาผิด]**

📌 **ทั้งสองความเสี่ยงมีลักษณะเดียวกัน: มันตัดสินได้ในรอบแรกด้วยการยิงจริง 30 วินาที ไม่ใช่ด้วยการเถียงกัน**

---

## 5. 🔬 PROBE รอบแรกของ cloud chief — **ทำเป็นอย่างแรกก่อนงานอื่นทั้งสิ้น แล้วเขียนผลลง `CHIEF_CONTINUATION`**

```bash
# 1. gh มีไหม และ auth ได้ไหม
which gh && gh --version && gh auth status ; echo "gh_exit=$?"
gh run list --limit 3 ; echo "ghrun_exit=$?"

# 2. API ตรง ๆ (คาดว่า 401 หรือโดนบล็อก - ทั้งสองอย่างคือคำตอบ)
curl -s -o /dev/null -w '%{http_code}\n' https://api.github.com/rate_limit

# 3. ช่องทาง D มีของหรือยัง
git fetch origin ci-status && git show origin/ci-status:ci/latest.json ; echo "d_exit=$?"

# 4. เสี่ยงที่สุดและสำคัญที่สุด: push main ได้ไหม (ยิงตอนที่ main ไม่ได้ขยับจริง)
git fetch origin main && git push origin origin/main:main ; echo "mainpush_exit=$?"
```
> **[อัปเดต 2026-08-20: probe นี้ถูกยิงจริงแล้วในรอบ 110/111 — ผล: ข้อ 2 (API) **ได้** ตรงข้ามกับที่ข้อ 0 คาดไว้ · ข้อ 3 (ทาง D) **ได้** อ่าน `conclusion: success` ออกมาจริง · ข้อ 4 (push `main`) **ถูกปฏิเสธ** ⇒ ไม่ต้องยิงซ้ำอีก ดู CORRECTION ด้านบน]**

**ข้อ 4 ปลอดภัยโดยตั้งใจ**: push `origin/main` ทับ `main` = no-op ที่ฝั่งเซิร์ฟเวอร์ (`Everything up-to-date`)
**แต่มันเดินผ่าน proxy เส้นเดียวกับ push จริงทุกประการ** ⇒ ตอบคำถามได้โดยไม่เปลี่ยนอะไรเลยแม้แต่ไบต์เดียว

🔴 **ผลของ probe นี้ต้องถูกเขียนลง `CHIEF_CONTINUATION.md` และ push ในรอบเดียวกัน**
ไม่งั้นรอบถัดไปที่ clone ใหม่จะไม่รู้ และจะมาลองซ้ำอีกตลอดไป

---

## 6. 🔴 NONCLAIMS

- **ทั้งเอกสารนี้ไม่มีการยิงจริงบน Routine แม้แต่คำสั่งเดียว** — chief รอบนี้รันบนสะพาน ไม่ได้อยู่บน cloud
- ข้อสรุปเรื่อง "ไม่มี credential ใน sandbox" มาจาก **เอกสารของ Anthropic** ไม่ใช่จากการวัด
- **แพตช์ workflow ในข้อ 3 ยังไม่เคยรัน** — ไม่ผ่าน gate ไม่ถูก commit ไม่ถูก push · syntax ยังไม่เคยถูก validate
  โดย GitHub · (ชื่อ job ใน `needs:` **ตรวจแล้ว** — ไฟล์มี job เดียวชื่อ `gate` ที่บรรทัด 62 · `on: push: branches:['**']`
  ⇒ branch `claude/*` ยิง workflow อยู่แล้ว · `permissions: contents: read` ระดับไฟล์ ⇒ job ใหม่ต้องประกาศ `contents: write` ของตัวเอง ซึ่งแพตช์ทำแล้ว)
- ไม่ทราบเพดานจำนวนรันต่อวันของ Routine เป็นตัวเลข (Panya เป็นคนเดียวที่เปิดหน้านั้นได้)

> **[แก้ 2026-08-20: bullet ข้อ 2 ("ไม่มี credential ใน sandbox" มาจากเอกสาร ไม่ใช่จากการวัด) — ตอนนี้วัดแล้วและ **ผลตรงข้าม**: รอบ 111 อ่าน GitHub API ได้จริง · bullet ข้อ 1 (ไม่เคยยิงจริงบน Routine) ยังจริงสำหรับ *รอบ 108* แต่ไม่จริงอีกต่อไปสำหรับโปรเจกต์ — รอบ 110/111 รันบนคลาวด์จริงแล้ว ดู CORRECTION ด้านบน]**

---

**Sources (เอกสารสาธารณะที่ใช้อ้างในข้อ 0/1):**
- [Making Claude Code more secure and autonomous with sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Claude Code on the web — Anthropic Help Center](https://support.claude.com/en/articles/12618689-claude-code-on-the-web)

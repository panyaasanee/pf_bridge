# FINDINGS R108 — **"cloud chief อ่านผล Actions ได้ยังไง"** และคำเตือนสองข้อที่ต้องอ่านก่อนเปิดใช้ A′

**ใบสั่ง:** `notes_to_chief\20260820_1830_PANYA-DECISION-cloud-prompt-A-prime.md` ข้อ 2
**คำสั่งของ Panya ตรง ๆ:** *"ถ้าอ่านไม่ได้ ทาง A′ พังทั้งทาง ⇒ ต้องบอกทันที อย่าเขียน prompt ที่สั่งให้ทำสิ่งที่ทำไม่ได้"*

---

## 0. คำตอบตรง ๆ ก่อน (แล้วค่อยดูเหตุผล)

🔴 **ผมยืนยันไม่ได้ว่าอ่านได้ และหลักฐานที่มีเอนไปทาง "อ่านไม่ได้ด้วยวิธีที่เรานึกถึงกันตอนแรก"**
เอกสารของ Anthropic เรื่อง Claude Code on the web ระบุว่า **ไม่มี credential อยู่ใน sandbox เลย** —
git ทำงานผ่าน **proxy ที่ฉีด token ให้ตอนวิ่งออก** และ *"ตรวจเนื้อหาของ git interaction ก่อน"*
⇒ ใน sandbox ไม่มี token ให้ `gh` หรือ `curl` ใช้ยิง `api.github.com` และ repo เป็น private
⇒ **การอ่าน Actions ด้วย API/gh จากใน sandbox ไม่ใช่สิ่งที่วางแผนพึ่งได้** จนกว่าจะมีใครยิงจริงแล้วเห็นว่าได้

⭐ **แต่ A′ ไม่พัง** — เพราะมีทางที่ **ใช้ช่องทางเดียวที่พิสูจน์แล้วว่าทำงาน คือ git เอง**
👉 **ให้ workflow เป็นคนประกาศผลของตัวเองลง git** (ข้อ 3 ข้างล่าง — ผมแนะนำอันนี้เป็นทางหลัก ไม่ใช่ทางสำรอง)

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

> หมายเหตุที่ต้องพูดให้ชัด: ข้อ B/C ที่ผมเขียนว่า "น่าจะไม่ได้" มาจาก **การอ่านเอกสาร ไม่ใช่การยิงจริง**
> เอกสารบอกกลไก (proxy ฉีด credential ให้ git · sandbox ไม่มี credential · โดเมนไม่เปิดล่วงหน้า)
> การอนุมานจากกลไกไปสู่ "ทำไม่ได้" ยังเป็นการอนุมาน ⇒ **ข้อ 5 คือ probe ที่ตัดสินได้ใน 30 วินาที**

---

## 2. ทำไม D ถึงเป็น "ทางหลัก" ไม่ใช่ "ทางสำรอง"

หลักดีไซน์ของโปรเจกต์นี้ที่ Panya วางเอง: **"เหมือนจริงใช้จริง ทำครั้งเดียวจบ" > "ง่ายวันนี้แต่รื้อทีหลัง"**

- **git คือช่องทางเดียวที่เรามีหลักฐานว่าทำงานจากทั้งสองฝั่ง** (Routine clone ได้จริง — probe 15:4x
  พิสูจน์ไฟล์ครบ 228/519 · และตัว sync ฝั่ง Windows รอบนี้พิสูจน์แล้วว่า push/pull/rebase เดินได้)
  ทุกทางอื่นเพิ่ม **ช่องทางที่สองที่พังได้เอง** เข้ามาในเส้นทางที่สำคัญที่สุดของระบบ
- ผลที่ workflow ประกาศเอง **เป็นความจริงจากปากผู้รู้** — runner เป็นคนรู้ว่าตัวเองเขียวหรือแดง
  ไม่ต้องมีใครไปถามใครแทน และไม่มี race แบบ "ถาม API เร็วไปตอนที่ยังรันไม่จบ"
- มันทำงาน **แม้ในวันที่ทุก HTTP นอก proxy ถูกปิด** ซึ่งเป็นทิศทางที่ sandbox กำลังเดินไป

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

**ฝั่ง cloud chief อ่านแบบนี้ (ไม่ต้องมี token ไม่ต้องมี gh):**
```bash
git fetch origin ci-status
SHA=$(git rev-parse origin/claude/r107-something)
git show "origin/ci-status:ci/$SHA.json"     # ไม่มีไฟล์ = ยังไม่รู้ผล ไม่ใช่เขียว
```

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

---

**Sources (เอกสารสาธารณะที่ใช้อ้างในข้อ 0/1):**
- [Making Claude Code more secure and autonomous with sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Claude Code on the web — Anthropic Help Center](https://support.claude.com/en/articles/12618689-claude-code-on-the-web)

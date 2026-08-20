# ติดตั้ง `merge-claude-pr` — สองไฟล์ สอง repo · **Panya เป็นคน push เท่านั้น**

*(chief รอบ 110 · 2026-08-20 ~21:00 · ตามใบสั่ง Panya 20:35 ข้อ 2)*

🔴 **ลำดับสำคัญกว่าตัวไฟล์:** อย่าเพิ่งเปิด routine จนกว่าทั้งสอง repo จะมี workflow นี้บน `main` แล้ว
เพราะ **ตั้งแต่ v4 เป็นต้นไป "PR ที่เปิดค้าง" คือล็อกของ cloud chief** — ถ้าไม่มีใคร merge PR
รอบแรกจะเปิด PR แล้วรอบที่สองจะเห็นล็อกและจบรอบทันที **และทุกรอบหลังจากนั้นก็จะจบทันทีตลอดไป**

---

## ก่อนอื่น — ตัดสิน PR #1 และ #2 ให้จบก่อน

ทั้งสองใบเปิดโดย cloud round 110/111 **ก่อน** ดีไซน์นี้ ⇒ ไม่มีบรรทัด `PF-AUTOMERGE: v4` ใน body
⇒ **workflow นี้จะเมินทั้งสองใบโดยตั้งใจ** ติดตั้งไปก่อนก็ไม่มีอะไร merge ย้อนหลัง (นี่คือเหตุผลที่มี marker)
แต่ **ถ้าปล่อยเปิดค้างไว้ มันจะเป็นล็อกที่ทำให้ทุกรอบจบทันที** ⇒ ต้องปิด
คำแนะนำเต็มอยู่ใน `pf_bridge\PANYA_REPORT_20260820_answers_PR_lock.md` หัวข้อ **④**

---

## repo 1 — `pirate-force-server` (โค้ด)

ไฟล์อยู่ที่เดิมพร้อม commit แล้ว **ยังไม่ได้ commit** ตามกติกา:

```
Pirate Force ServerProject\.github\workflows\merge-claude-pr.yml
```

- ✅ `.gitignore` **ไม่ต้องแก้** — `!/.github/` และ `!/.github/**` เปิดไว้แล้วตั้งแต่รอบ 103 (บรรทัด 489-490)
- ✅ ไฟล์นี้ **ไม่แตะ** `.manifest` / coverage / report ⇒ **ไม่ต้องรัน seam test**
- ✅ ตรวจแล้ว: yaml parse ผ่าน · `bash -n` ผ่านทั้งสอง job · **0 non-ASCII bytes** (462 บรรทัด)
- ✅ **ผ่านการตรวจแบบปฏิปักษ์หนึ่งรอบ แล้วเขียนใหม่** — ผู้ตรวจอิสระเจอ 6 ข้อจริง แก้ครบแล้ว
  (รายละเอียดใน `PANYA_REPORT_20260820_answers_PR_lock.md` หัวข้อ "ผลการตรวจแบบปฏิปักษ์")
- ⚠️ commit ตัวนี้แตะ `.github/` ⇒ ตามกฎเหล็กควรรัน gate ปกติหนึ่งรอบก่อน push

## repo 2 — `pf_bridge` (เอกสาร)

repo นี้ **ยังไม่มี `.github/` เลย** และ `.gitignore` บรรทัดแรกคือ `/*` (deny-all + allowlist)
⇒ ต้องทำ **สองอย่าง** ไม่ใช่อย่างเดียว มิฉะนั้นไฟล์จะอยู่บนดิสก์แต่ git มองไม่เห็น
(นี่คือกับดักเดิมเป๊ะ ๆ ที่ทำให้ gate workflow ใช้ไม่ได้ตั้งแต่รอบ 87 ถึงรอบ 103)

**① คัดลอกไฟล์:**
```
pf_bridge\drafts\WORKFLOW_bridge_merge-claude-pr.yml
   ->   pf_bridge\.github\workflows\merge-claude-pr.yml
```

**② เติมสองบรรทัดใน `pf_bridge\.gitignore`** — วางในบล็อก allowlist ของไดเรกทอรี
ต่อจาก `!/factpack_L1/make_factpack_l1.py` (บรรทัด 67) ได้เลย:

```gitignore
# ---- workflows: merge a cloud round's pull request (chief round 110) ----
# Line 1 of this file is `/*`, so git does not even descend into .github/
# unless the directory is opened by name BEFORE its contents.  Both lines are
# needed; the first one alone opens an empty door.
!/.github/
!/.github/**
```

**③ (แนะนำ ทำพร้อมกันเลย) เติมอีกสองบรรทัดสำหรับกฎ "หนึ่งรอบหนึ่งไฟล์"** — prompt v4 สั่งให้ cloud chief
เขียนบันทึกรอบลง `pf_bridge/rounds/R<NNN>_*.md` แทนการแทรก `CHIEF_CONTINUATION.md` ที่บรรทัด 3
**ถ้าไม่เติมสองบรรทัดนี้ ไฟล์รอบจะอยู่บนดิสก์แต่ git มองไม่เห็น** (กับดักเดิมเป๊ะ ๆ):
```gitignore
# ---- one file per round, so two pull requests never touch one line ----
!/rounds/
!/rounds/**
```

**ยืนยันว่าเห็นจริงก่อน commit — อย่าเชื่อว่าไฟล์อยู่ในดิสก์แล้วแปลว่าอยู่ใน repo:**
```
git -C "C:\Users\Panya\Desktop\Pirate Force\pf_bridge" ls-files .github
```
ต้องได้ **1 บรรทัด** · ได้ 0 บรรทัด = `.gitignore` ยังกินอยู่ **ห้าม commit ต่อ**

⚠️ **ตัว sync จะ commit + push ให้เองภายใน ~5 นาที** — `pf_git_sync.ps1` push repo นี้อัตโนมัติ
ถ้าไม่อยากให้ขึ้นก่อนพร้อม ให้ปิด sync ก่อนวางไฟล์

---

## ตรวจหลังติดตั้ง — สามอย่าง วัดได้ ไม่ใช่เดา

1. **Actions tab ของทั้งสอง repo ต้องมี workflow ชื่อ `merge-claude-pr` โผล่ในลิสต์** (ยังไม่ต้องรัน)
2. กด **Run workflow** (`workflow_dispatch`) หนึ่งครั้งต่อ repo — จะไปเข้า job `reap`
   ไม่มี PR ที่มี marker ⇒ ต้องจบ **เขียว** พร้อมข้อความ `no open pull requests` หรือข้าม PR ทุกใบ
   🔴 **ถ้าเห็น HTTP 403** = repo setting ไม่ยอมให้ `pull-requests: write` ⇒ **บอก chief ทันที ต้องออกแบบใหม่**
   (`contents: write` วัดแล้วว่าใช้ได้บน repo โค้ด — `ci-status` เกิดขึ้นได้เพราะกลไกเดียวกันนี้)
3. ค่อยเปิด routine ด้วย prompt **v4** (`agent_kit\chief_task_prompt_CLOUD_v4_20260820.md`)

## nonclaims
- **ทั้งสองไฟล์ยังไม่เคยรันจริง** — ที่ตรวจแล้วคือไวยากรณ์เท่านั้น (yaml parse + `bash -n` + ASCII)
- **`pull-requests: write` ยังไม่เคยวัดบน repo ใดในโปรเจกต์นี้**
- ไม่ได้ตรวจว่า GitHub auto-merge / branch protection ใช้ได้ไหมบนแผนของ Panya — **ดีไซน์นี้จงใจไม่พึ่งมัน**

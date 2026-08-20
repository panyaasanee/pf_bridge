# 🛑🛑 คำสั่ง Panya 2026-08-20 ~12:30 — **รอบนี้ทำเฉพาะงาน GitHub เท่านั้น หยุดงานอื่นทั้งหมด**

> **Panya กดรันรอบนี้ด้วยมือเอง (manual fire) และกำลังจะ `git push` เดี๋ยวนี้**
> คำพูดของท่าน: *"ให้มันทำเฉพาะงาน github ให้เรียบเสร็จ ยังไม่ต้องทำงานอื่นต่อ เพราะฉันจะ push แล้วเดี๋ยวนี้"*

---

## ✅ งานเดียวที่ต้องทำรอบนี้

**เติม allowlist ให้ `.github/` ใน `.gitignore` ของรีโปหลัก แล้ว commit**

เหตุผล (ตรวจสดเมื่อ 12:1x):
```
git check-ignore -v .github/workflows/gate-windows.yml
  -> .gitignore:1:/*        .github/workflows/gate-windows.yml
git ls-files .github
  -> (ว่างเปล่า)
```
⇒ ไฟล์ workflow **มีอยู่จริงบนดิสก์แต่ไม่ได้ถูก track** · ถ้าไม่แก้ **Actions จะไม่มีวันรันเลย** ต่อให้ push แล้ว

**สิ่งที่ต้องเติม** (จำกฎ deny-all: git ไม่เดินเข้าโฟลเดอร์ที่ถูก exclude แล้ว ⇒ ต้องเปิดตัวโฟลเดอร์ก่อน):
```
!/.github/
!/.github/**
```

**เงื่อนไขจบที่วัดได้:**
1. `git ls-files .github` ต้องคืน **อย่างน้อย 2 บรรทัด** (`gate-windows.yml` + `README_GATE_CI.md`)
2. gate เขียวตามปกติ (การแก้ `.gitignore` ต้องผ่าน seam test + ignoreGuard ตามกฎเดิม)
3. commit ลงจริง · เขียน `head:` ใหม่ในใบเสร็จ

---

## 🔴 ห้ามทำรอบนี้ (ทุกข้อ)
- ❌ static RE ใด ๆ · ❌ เปิดเลนใหม่ · ❌ เขียน design draft · ❌ spawn ลูกมือไปขุด
- ❌ แตะคิว `GAME_TEST_QUEUE.md` · ❌ เพิ่ม ledger entry · ❌ ขยับ coverage grade
- ❌ งานแม่บ้าน archive (CHIEF_CONTINUATION ใกล้ 100KB — **รอบนี้ปล่อยไว้ก่อน**)
- ❌ **`git remote add` / `git push` / แตะ config ของ remote เด็ดขาด** — credential เป็นของ Panya
  ท่าน push เอง · chief **ไม่มีสิทธิ์ push จนกว่าท่านจะสั่งเปลี่ยนกฎ**
- ❌ อย่าตกใจถ้าเห็น `git remote -v` มี origin โผล่มากลางรอบ — **นั่นคือ Panya ไม่ใช่ความผิดพลาด**

## ⏱️ ข้อบังคับเรื่องเวลา — Panya นั่งรออยู่หน้าจอ
- ทำเป็น **จ็อบเดียว สั้น ๆ** · ถือ `LOCK_GIT` ให้สั้นที่สุด **ปล่อยธงทันทีที่ commit จบ**
- ⚠️ ผู้เทสอาจกำลังรันรอบเทสสดอยู่ — จ็อบของผู้เทสรอบนี้ขึ้นต้นด้วย `0` และ **แซงคิวคุณได้**
  (กฎใหม่ 2026-08-20 ~11:0x · ดูจดหมาย `..._1105_PANYA-RULE-queue-priority-zero-prefix.md`)
- **ถ้าทำงาน GitHub เสร็จแล้ว ให้จบรอบทันที** เขียนกล่องจดหมาย + `next:` แล้วหยุด
  **ห้ามหยิบงานถัดไปมาทำต่อเพื่อ "ใช้เวลาให้คุ้ม"**

## 📋 งานที่รอ *รอบหน้า* (อ่านไว้เฉย ๆ รอบนี้ห้ามทำ)
อยู่ในจดหมาย `20260820_1215_PANYA-GOLIVE-decisions-and-repo2-gitignore.md` ครบแล้ว:
กฎ sibling + เทส · ทำ Actions แดงจริงหนึ่งครั้งแล้วเขียวกลับ · rebase `chief_task_prompt_CLOUD_DRAFT.md`
(ร่างเก่าลงวันที่ 19 ส.ค. 17:40 ขาดกฎแม่บ้าน never-drop-untested และกฎเลขจ็อบ `0`-prefix)

## 🧾 หมายเหตุ
- **คำตัดสินของ Panya วันนี้:** `VITAL_REGISTRY...tsv` = **ขึ้น** · `evidence_screens/` = **ขึ้น** ·
  `report_images/` = **ยังไม่ตัดสิน กันออกก่อน** · `verify_foundation.ps1` (79 vs 105) = **พักไว้ ไม่ใช่ตัวบล็อก**
- `.gitignore` ของรีโปที่สองสร้างและทดสอบแล้ว: `pf_bridge\DRAFT_gitignore_REPO2_20260820.txt`
  (224 ไฟล์เข้า / 1,086 กันออก · assertion 20/20 · `strings_*` และ `pe_*` ถูกกันสองชั้น) — **Panya จะ `git init` เอง**
- ⚠️ มีไฟล์ `.git\STALE_index.lock_20260820_1210_delete_me` อยู่ในรีโปหลัก — **เป็นซาก `index.lock` ที่ผมทิ้งไว้
  แล้วเปลี่ยนชื่อกันไว้ ไม่ใช่ lock ที่ใช้งานอยู่** git ทำงานได้ปกติ · Panya จะลบเอง · **chief ไม่ต้องยุ่ง**

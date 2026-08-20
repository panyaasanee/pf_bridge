# 📌 สถานะ 2026-08-20 ~21:30 — เหลือ repo โค้ด repo เดียว

## ทำไปแล้ว (ไม่ต้องทำซ้ำ)
- ✅ **PR #1 และ #2 ปิดแล้ว** — Panya ตรวจ Files changed เอง: **เอกสารล้วนทั้งสองใบ ไม่มี `src/` `tools/` `tests/` `docs/`**
  branch ไม่ถูกลบ ⇒ จดหมาย R110/R111 ยังตามหาได้ · ล็อกปลดแล้ว
- ✅ **`pf_bridge` ติดตั้งครบแล้ว** (ผู้ช่วยทำให้ ตามคู่มือ `drafts\INSTALL_merge_workflows_20260820.md` ข้อ ①②③)
  - `drafts\WORKFLOW_bridge_merge-claude-pr.yml` → `.github\workflows\merge-claude-pr.yml`
  - `.gitignore` เติม `!/.github/` + `!/.github/**` และ `!/rounds/` + `!/rounds/**`
  - **ยืนยันแล้ว** `git ls-files --others --exclude-standard .github` = **1 บรรทัด** (ไม่โดน deny-all กิน)
  - Panya push เอง

## 🔴 งานรอบนี้: เหลือ **repo โค้ดอย่างเดียว**
`Pirate Force ServerProject\.github\workflows\merge-claude-pr.yml` **เขียนไว้แล้ว ยังไม่ commit**
⇒ **รัน gate ปกติหนึ่งรอบ แล้ว commit** ตามกฎเหล็ก (แตะ `.github/`)
- `.gitignore` ไม่ต้องแก้ (`!/.github/` เปิดไว้ตั้งแต่รอบ 103)
- stage **เฉพาะพาธเดียวนี้** · Panya push เอง

## หลังจากนั้น Panya จะทำเอง (chief ไม่ต้องยุ่ง)
- ยิง `workflow_dispatch` ทีละ repo **หา HTTP 403** — `pull-requests: write` ยังไม่เคยวัดที่ไหนเลยในโปรเจกต์นี้
  🔴 **ถ้าเจอ 403 = ต้องออกแบบใหม่** เขียนรอไว้เลยว่าถ้าเจอจะเสนออะไร
- แล้วค่อยเปิด routine ด้วย **prompt v4**

## ⚠️ เตือนเรื่องเวลา
Panya ทำงานต่อเนื่องมาตั้งแต่เช้า (ตอนนี้ ~21:30) ⇒ **ถ้ารอบนี้ทำได้สั้น ให้สั้น**
ทำแค่ gate+commit ไฟล์เดียว **อย่าเปิดงานใหม่ อย่าเขียนเอกสารเพิ่ม** เสร็จแล้วจบรอบ

## ขอบเขต
🔴 **ห้าม push · ห้ามแตะ routine · ห้ามแตะ PR**

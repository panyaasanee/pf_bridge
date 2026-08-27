# 🔴 แก้คำของตัวเอง · 2026-08-24 19:30 (+07:00) — 4 ไฟล์เครื่องมือ **ไม่เคย** ติดด่านชื่อ

**ผู้เขียน:** ผู้ช่วย (cloud) · **แก้จดหมาย** `20260824_1915_SYNC-PATCH-name-guard-waiver-for-letters.md`
หัวข้อ "🟡 กับดักที่ยังเหลือ" · **สถานะแพตช์:** ยังคงไว้ (คุณ Panya เคาะแล้ว · ไม่มีผลเสีย) แต่**ไม่ได้แก้อะไรวันนี้**

## ผมเขียนอะไรผิด

ผมเขียนว่า 4 ไฟล์นี้ "ชื่อจะติดด่านเดียวกันถ้าถูกแก้ไข":

```
external/pf_validate_capture_fields.py
staged/1027_gt047_capture_validate_baseline.ps1
staged/gt047_patch_run_20260824_1438/pf_validate_capture_fields.py
staged/re059_extract_capture.py
```

**ผิดที่สมมติฐาน** — ทั้งสี่ไฟล์ **untracked** ยังไม่อยู่ใน git เลยสักไฟล์
จึง "ถูกแก้ไข" ในความหมายของ git ไม่ได้ตั้งแต่ต้น และ**ไม่มีวันเดินไปถึงด่านชื่อ**

## ตัวบล็อกจริงคืออะไร (คนละตัวกันสองตัว)

**① `external/pf_validate_capture_fields.py` — ถูก `.gitignore` บล็อก**
`.gitignore` บรรทัด 86-96 ทำ `external/` เป็น **allow-list 9 ไฟล์**:

```
!/external/
/external/*                      <- ignore ทุกอย่างใน external/
!/external/00_SEARCH_HERE_FIRST.md
!/external/PF_PROTOCOL_REGISTRY.tsv
... (รวม 9 บรรทัด)
```

`pf_validate_capture_fields.py` ไม่อยู่ใน 9 ชื่อนั้น ⇒ ถูก ignore · ด่านชื่อไม่เกี่ยวเลย

**② `staged/` สามไฟล์ — untracked และ sync สแกน `staged/` ด้วย `--untracked-files=no` (บรรทัด 334)**
`staged/` **ไม่ได้ถูก ignore** (`!/staged/` + `!/staged/**` บรรทัด 50-51) และมี 35 ไฟล์ tracked อยู่แล้ว
แต่สามไฟล์นี้ไม่เคยถูก `git add` ⇒ sync หยิบขึ้นมาไม่ได้ **โดยเจตนาของดีไซน์** ไม่ใช่บั๊ก

## วิธีตรวจ (ไม่ได้รัน git บน mount ตามกฎ)

อ่าน `.git/index` ตรง ๆ ด้วย python (read-only ไม่จับ lock ไม่แตะ index)
index v2 · 2,013 entries · เทียบชื่อทั้งสี่กับ set ของ path ที่ tracked

## แพตช์ที่เพิ่มไปเมื่อ 19:2x ยังคุ้มไหม

**คุ้ม แต่เป็นการ "อนุญาตล่วงหน้า" ไม่ใช่การแก้ของที่พังอยู่**

```
$NAME_GUARD_WAIVER = @('notes_to_chief/|.md',
                       'external/|.py', 'staged/|.py', 'staged/|.ps1')
```

วันไหนที่มีคน `git add` ไฟล์เหล่านี้เข้าไปจริง (งานมือของ Codex + LOCK_GIT)
การแก้ครั้งถัดไปจะไม่ถูกด่านชื่อกลืนเงียบ ๆ · รอบ 19:27:02 พิสูจน์แล้วว่าสคริปต์รันผ่าน
(`refusals=0` · `committed 1 path(s)` · `pushed`) ไม่มี syntax error จาก array หลายบรรทัด

## 🟡 คำถามที่แยกออกไป — รอคุณ Panya เคาะ (ไม่ด่วน)

อยากให้เครื่องมือ 4 ตัวนี้เข้า repo ไหม? ตามคำตัดสิน 2026-08-23 20:39 ของคุณ Panya
สคริปต์ที่ผลิต derived metadata **ไปยัง remote ได้** — แค่ยังไม่เคยมีใครพามันเข้าไป
ถ้าเอา ต้องทำสองอย่างคนละแบบ:

- `external/` → เพิ่ม `!/external/pf_validate_capture_fields.py` ใน `.gitignore` แล้วค่อย add
- `staged/` 3 ไฟล์ → `git add` ตรง ๆ ได้เลย (ไม่ถูก ignore)

ทั้งสองเป็นงานมือของ Codex ใต้ LOCK_GIT · ผู้ช่วยไม่รัน git เอง

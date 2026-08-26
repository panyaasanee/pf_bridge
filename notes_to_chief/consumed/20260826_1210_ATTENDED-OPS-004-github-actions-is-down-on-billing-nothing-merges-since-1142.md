[ถึง: **COO (รอบคลาวด์)** · chief / สาย E · สาย A · สาย B · Panya | จาก: **มือเขียนแทน Panya (เซสชัน attended [กะ1])** · 2026-08-26T12:10+07:00]

# `OPS-004` — **GitHub Actions ของบัญชี `panyaasanee` ถูกระงับเรื่องบิลลิ่ง ⇒ ไม่มี PR ใบไหน merge ได้ตั้งแต่ 11:42 · และ `PR #41` ถูก reaper ปิดไปแล้วตั้งแต่ 10:38**

## ① วัดจาก GitHub API (job 1182/1183/1184 บนสะพาน · GET อย่างเดียว)

ทุก job ที่สร้างหลัง **11:42 +07** ในทั้งสองรีโป (`ubuntu-latest` และ `windows-latest`) จบ `failure` ภายใน ~2 วินาที **โดยไม่มี step ใดเริ่ม** (`steps=0`, ไม่มี runner, log 404) และทุก job มี annotation เดียวกัน:

> `The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings`

- รีโปทั้งสอง **private** ⇒ กินโควตานาที Actions · gate บน `windows-latest` คิด 2 เท่า
- job สุดท้ายที่ยังได้ runner: `gate` ของ run 32931193256 (11:41:57Z สร้าง) — `publish-status` ของ run เดียวกันตายแล้ว
- **ไม่ใช่** ปัญหา workflow · **ไม่ใช่** ปัญหาการสลับบัญชี Claude (PR ของ [กะ1] ถูก author โดย `panyaasanee` เหมือนเดิม head repo เดียวกัน)

## ② ผลที่ตามมา — ระบบล็อกรอบพังทั้งก้อนแบบเงียบ

| ที่ค้าง | สถานะ |
|---|---|
| `pf_bridge #104` **[COO]** Mob AI ruling + OPS-003 closure · non-draft · marker ครบ · `mergeable=true` | merge job ไม่ได้ runner ⇒ **คำตัดสิน 11:44 ยังไม่ขึ้น `main`** |
| `pf_bridge #103` [LANE-E] draft claim · `#105` [LANE-B] draft claim · `claude/upbeat-turing-gye38n` [LANE-A] | เปิดค้าง |
| `server #54` [LANE-E] draft claim `870c967e` | gate ไม่รัน (push และ pull_request ตายทั้งคู่) |
| `reap` (:17 / :23) | **รันไม่ได้เช่นกัน** ⇒ PR ค้างไม่ถูกเก็บ ⇒ ทุกสายเห็น "PR เปิดค้าง" แล้วจบรอบทันทีทุกชั่วโมง **ตลอดไปจนกว่าบิลลิ่งจะแก้** |

🔴 **นี่คือโหมดตายที่ยังไม่มีใครมองเห็นจากคลาวด์** — เหมือน `OPS-002` (สะพานตาย) แต่คนละชั้น: สะพานสบายดี (sync commit 11:50) แต่ท่อ merge ตาย · COO ควรเพิ่ม "Actions ได้ runner ไหม" เป็นข้อตรวจในรอบผู้บริหาร (ดู `actions/runs?per_page=5` ถ้า `conclusion=failure` ติดกันและ job ไม่มี step = บิลลิ่ง ไม่ใช่โค้ด)

## ③ `PR #41` (M1) — ปิดแล้วจริง ก่อนบิลลิ่งจะตาย

- run `32927231864` (`merge-claude-pr` **schedule** 10:38:53 +07) job `reap`: *"a GREEN gate exists and this PR is still open - decide must have failed; finishing it here"* → `gh pr merge` ปฏิเสธ `not mergeable` → **REAPED -> closed; branch kept**
- ตรงกับที่ใบส่งมอบ ④ เตือนไว้ทุกตัวอักษร — ต่างแค่ตัวปลุกไม่ใช่ `workflow_dispatch` แต่เป็นรอบ schedule ของ reaper เอง
- กิ่ง `claude/youthful-fermat-prw6i5` ยังอยู่ที่ `817ca55` · ahead 3 · behind `main` 39 · `merge-tree` ชน **ไฟล์เดียว** `tests/test_foundation_legacy_seam.py` (พิน `GRADE_SUBSET_SHA256`) · `docs/FUNCTIONAL_COVERAGE.json` auto-merge ได้

## ④ คำสั่งเจ้าของ (การ์ดคำถาม ~12:05 +07)

1. **routine สาย A / B / COO ปล่อยรันต่อ** ระหว่างรอ (เจ้าของเลือกเอง — รอบจะจบเร็วเพราะติดล็อก)
2. **บิลลิ่ง GitHub เจ้าของไปแก้เอง** (เติมเงิน/เพิ่ม spending limit หรือเปลี่ยน public หรือรอรีเซ็ต) — มือเขียนแทนแตะไม่ได้
3. หลัง Actions กลับมา **มือเขียนแทนทำสองอย่างผ่านจ็อบบนสะพาน** (credential ของเจ้าของบนเครื่อง · ไม่มี force ไม่มี rebase):
   (ก) ปลุก `#104` ด้วย event `edited` (แก้หัวข้อเล็กน้อย) ให้ merge job ตื่น
   (ข) เตรียม `#41` ใหม่ตามขอบเขต `COO-ESCALATION 09:52` เป๊ะ: merge `origin/main` เข้ากิ่ง (worktree แยก) · แก้ชนเฉพาะ `test_foundation_legacy_seam.py` โดยเก็บ prose ทั้งสองฝั่งและ **คำนวณ digest ใหม่ด้วย `grade_digest()` ของเทสเอง ไม่พิมพ์ค่าเอง** · merge commit เท่านั้น · push เป็นกิ่งใหม่ `claude/youthful-fermat-prw6i5-m1-rebuild` · **เปิด PR เฉพาะเมื่อ Actions รันได้แล้ว** (เปิดตอนนี้ = reaper ปิดทิ้งอีกรอบเมื่อครบ 6 ชม. โดยไม่มี gate)
   ⇒ สาย A **ไม่ต้องทำ `#41` ซ้ำ** ถ้าเห็นกิ่ง `*-m1-rebuild` โผล่บน origin แล้ว

## nonclaims
- ไม่ได้เห็นหน้า Billing ของ GitHub โดยตรง — สรุปจาก annotation ที่ GitHub แนบมากับทุก job เท่านั้น
- ไม่รู้ว่าโควตาหมดหรือบัตรตัดไม่ผ่าน (annotation ใช้ข้อความเดียวกันทั้งสองกรณี) และไม่รู้วันรีเซ็ตรอบบิล
- `#41` ที่จะเตรียมใหม่ยังไม่ได้ผ่าน gate ใด ๆ — จะรู้ผลก็ต่อเมื่อ Actions กลับมาและ PR ใหม่ถูกเปิด

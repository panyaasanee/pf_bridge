# R112 — รอบแรกที่รันด้วย prompt v4 จริง: probe + commissioning ท่อ A″ (PR + automerge)

- **เวลา:** 2026-08-20 ~17:51–18:1x UTC (≈ 00:51–01:1x เวลาไทย 21 ส.ค.)
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · Python 3.11.15
- **branch รอบนี้:** `pf_bridge` → `claude/hopeful-knuth-fps3tp` · `pirate-force-server` → `claude/nifty-cerf-fps3tp` (ไม่ได้แตะ — ดูข้อ 5)

## 1. การ์ดกันรอบซ้อน (ทำก่อนทุกอย่าง) — ล็อกว่าง

ถาม GitHub API ผ่าน **GitHub MCP tools** (ไม่ใช่ `gh` — ดูข้อ 2):
- `pirate-force-server` open PRs = **0**
- `pf_bridge` open PRs = **0**
⇒ ไม่มี PR ค้างจาก `claude/*` ทั้งสอง repo — ทำงานได้

## 2. ผล PROBE v4 (ตัดข้อ push main ทิ้งแล้วตามคำสั่ง)

| ข้อ | ผล | หมายเหตุ |
|---|---|---|
| 1. `gh` CLI | ❌ **ไม่มี** (`which gh` exit 1) | v4 เขียนคำสั่งการ์ดเป็น `gh pr list` — **ใช้ตรงตามตัวอักษรไม่ได้** |
| 2. API อ่านได้ไหม | ✅ **ได้ ผ่าน GitHub MCP tools** (`list_pull_requests` ตอบจริงทั้งสอง repo) | ยืนยันสิ่งที่รอบ 111 วัด — แต่ช่องทางคือ MCP ไม่ใช่ `gh`/`curl` |
| 3. ทาง D (`ci-status`) | ✅ **มีชีวิต** — `git fetch origin ci-status` สำเร็จ · มีคำตัดสิน 3 ใบ | ทุกใบ `conclusion: "success"` (event: push บน main) |

คำตัดสินใน `ci-status` ณ ต้นรอบ (repo โค้ด):
- `89ce13b` (round 109) → success · run 32370578994 · 12:49Z
- `4ae6503` (install merge-claude-pr) → success · run 32381658674 · 14:44Z
- `2842fb9` (actions: read patch) → success · run 32383555993 · 15:03Z

🔴 **ข้อเสนอแก้ v4 → v5 (บรรทัดเดียว):** เปลี่ยนคำสั่งการ์ดจาก `gh pr list ...` เป็น
"ถามผ่าน GitHub MCP tool `list_pull_requests` (มีในทุกเซสชัน Routine) · `gh` ไม่มีในอิมเมจ"
— ความหมายของการ์ดไม่เปลี่ยน (มองไม่เห็นล็อก = ห้ามทำงาน ยังบังคับเหมือนเดิม)

## 3. สภาพ repo ณ ต้นรอบ — บล็อกข้อ 6 ปลดแล้ว

- **`merge-claude-pr.yml` อยู่บน `main` ของทั้งสอง repo แล้ว** (Panya push เอง ~22:00 เวลาไทย):
  bridge `8fe5545` · server `2842fb9` — เงื่อนไข "ก่อนสับสวิตช์" ข้อสุดท้ายปิดแล้ว
- กล่อง `notes_to_chief/` **เคลียร์แล้วตั้งแต่ก่อนรอบ** (ใบ 21:30 มี stub `.CONSUMED.txt` บน main แล้ว — รอบ attended เป็นคนบริโภค)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง — โครงพี่น้องปกติ
- branch `claude/*` ของ PR #1/#2 เดิมถูกลบจาก remote แล้ว แต่**เนื้อหาถูกรวมเข้า main แล้วทั้งหมด**
  (ทั้ง `f83d860` ฝั่ง bridge และ `2842fb9` ฝั่ง server เป็น ancestor ของ main ปัจจุบัน) — ไม่มีงานหาย

## 4. งานรอบนี้: commissioning ท่อ — เจตนาให้แคบ

เหตุผลที่รอบนี้ไม่เปิดงาน gameplay ใหม่ (เขียนตรง ๆ):
1. `merge-claude-pr.yml` **ไม่เคยรันจริงแม้แต่ครั้งเดียว** — nonclaim ของ v4 เอง บอกว่ารอบแรกที่มี PR คือรอบทดสอบมัน
   ⇒ PR ใบแรกควรเป็นใบเล็กที่อ่านผลง่าย ไม่ใช่งานโค้ดก้อนใหญ่ที่ไปพันกับท่อที่ยังไม่พิสูจน์
2. งบ token ของ Panya ใช้ไปครึ่งสัปดาห์แล้ว — รอบ commissioning ควรถูก
3. คำเตือนใน v4 เรื่อง `README.md:15` / `AGENTS.md:117` โฆษณา `verify_foundation.ps1` ผิด — **ตรวจแล้ว: ล้าสมัย**
   ทั้งสองไฟล์มีบล็อกแก้ครบแล้ว (README.md:26 · AGENTS.md:128 "is NOT the gate, and it cannot pass")
   ⇒ งานชิ้นนั้นไม่มีอยู่จริงแล้ว ไม่ต้องทำ

สิ่งที่ทำ:
- รัน **สวีต sanity บน Linux** กับ server clone ที่ `2842fb9` — ผลอยู่ข้อ 6
- เขียนไฟล์รอบนี้ (`rounds/R112_*.md`) ตามกฎ "หนึ่งรอบหนึ่งไฟล์" — **ไฟล์แรกใต้ `rounds/`**
- ต่อท้าย `CHIEF_CONTINUATION.md` หนึ่งบรรทัด (ดัชนี) — ไม่แตะบรรทัด 3 ไม่เขียนบล็อก
- เปิด PR ฝั่ง `pf_bridge` พร้อม `PF-AUTOMERGE: v4` — **นี่คือการยิงทดสอบ workflow ฝั่ง bridge ครั้งแรก**

## 5. สิ่งที่รอบนี้ *ไม่* ได้ทำ / ไม่ได้พิสูจน์ (nonclaims)

- **ไม่ได้แตะ `pirate-force-server` เลย** — ไม่มี commit ไม่มี PR ⇒ ท่อฝั่ง server
  (gate-windows → workflow_run → merge) **ยังไม่เคยถูกทดสอบ live** — รอบถัดไปที่มีงานโค้ดจริงคือรอบทดสอบมัน
- ไม่มีผลเทสในเกมใหม่ · `GAME_TEST_QUEUE.md` ไม่ขยับ (ไม่มีรายการเพิ่ม/ปิด/ย้าย)
- ผลสวีตข้อ 6 คือ **เขียว(cloud sanity) เท่านั้น** — ไม่ใช่ gate · กับดัก cp874 และพฤติกรรม 3.14 ไม่มีที่นี่
- การ์ด PR ใช้ MCP อ่าน — **ยังไม่เคยเห็นเคส "API ล้มแล้ว fallback ทาง D" เกิดจริง** (แค่พิสูจน์ว่าทาง D อ่านได้)
- แบนเนอร์ใช้ครั้งเดียว (21:30) หัว `CHIEF_CONTINUATION.md` **จงใจไม่ลบ** — กฎ v4 ให้แตะไฟล์นั้นแค่บรรทัดต่อท้าย
  การลบแบนเนอร์ = แก้กลางไฟล์ = เสี่ยงชนกับสะพาน ให้ Panya/สะพานลบเองได้ทุกเมื่อ

## 6. ผลสวีต sanity (Linux · Python 3.11.15 · pytest 9.1.1) — ที่ server `2842fb9`

รันสองแบบ — แบบแรกผิดวิธี แบบสองคือสูตรของ gate เอง:

1. **`pytest tests -q` เปล่า ๆ (ผิดวิธี — จดไว้กันคนทำซ้ำ):** `193 failed, 1565 passed, 29 skipped, 70 errors`
   — ก้อนแดงทั้งหมดคือ 43 โมดูลที่อ่าน client image / capture corpus ซึ่ง gate **exclude ด้วยสูตร
   `Select-String 'GameClient|capture_v141'`** (gate-windows.yml:390-398) — ที่นี่ต้อง exclude แบบเดียวกัน
2. **สูตร gate (exclude 43 โมดูล ด้วย `grep -lE 'GameClient|capture_v141'` ยกเว้น seam):**
   - รอบแรก: `1 failed, 947 passed, 4 skipped` — ตัวเดียวที่แดง: `test_upgrade_from_original_foundation_schema`
   - 🆕 **root cause = ข้อเท็จจริงสิ่งแวดล้อมใหม่ที่ v4 ยังไม่รู้: clone ของ Routine เป็น SHALLOW** (53 commits ·
     มี `.git/shallow`) ⇒ `git show 5c200e2:migrations/001_initial.sql` ตาย เพราะ commit เก่าไม่อยู่ในประวัติ
   - แก้ด้วย `git fetch --unshallow origin` (เน็ตถึง GitHub อยู่แล้ว) → เทสตัวนั้นผ่านทันที
   - gate ฝั่ง Actions รู้จักปัญหาคลาสนี้อยู่แล้ว (checkout ตั้ง depth เพราะ `git ls-tree 5cc0eda` — gate-windows.yml:79-83)
   - **รอบสอง (หลัง unshallow): `948 passed, 4 skipped (declared, precondition:*), 1517 subtests passed, 0 failed`**
     = **เขียว(cloud sanity)** ที่ server `2842fb9` — ไม่ใช่ gate · skip ทั้ง 4 ประกาศเหตุผลครบตามกลไกรอบ 106

🔴 **บทเรียนสำหรับรอบถัดไป (ควรเข้า v5):** ต้นรอบฝั่ง server ให้ `git fetch --unshallow origin` ก่อนรันสวีต
และรันสวีตด้วยสูตร exclude ของ gate เสมอ — เลขอ้างอิง ณ `2842fb9`: excluded 43 โมดูล · 948 pass · 4 skip

## 7. งานค้างที่มองเห็นจากรอบนี้ (ให้รอบถัดไปเลือกหยิบ)

- **ทดสอบท่อฝั่ง server ด้วยงานโค้ดจริงชิ้นเล็ก** — pre-approved backlog มีอยู่ (HYP-PF-025 ก้อน 2 ยัง active ·
  DAMAGE-MODEL ทาง 1 อนุมัติแล้ว) — รอบถัดไปเริ่มจากอ่าน `STATUS.md` + coverage matrix ก่อนเลือกชิ้น
- **งานแม่บ้าน:** `CHIEF_CONTINUATION.md` ~99KB ชนเพดาน ~100KB — ต้องย้ายรอบเก่าที่ปิดแล้วไป `archive/`
  🔴 แต่การย้าย = ลบบล็อกกลางไฟล์ = ชนกติกา "แตะแค่บรรทัดต่อท้าย" ของ v4 **และ** เสี่ยงชนสะพาน
  ⇒ เป็นคำถามถึง Panya: อนุญาตให้รอบ cloud รอบใดรอบหนึ่งทำ archive ครั้งเดียว (ประกาศ deletion ชัด) หรือให้ฝั่ง Windows ทำ
- **ข้อเสนอ v5 บรรทัดเดียว** (ข้อ 2 ข้างบน): การ์ด PR ให้เขียนเป็น MCP ไม่ใช่ `gh`

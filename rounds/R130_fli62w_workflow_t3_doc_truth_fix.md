# R130 (fli62w) — แก้เอกสารมีชีวิตที่ยังโฆษณา `verify_foundation.ps1` เป็น acceptance

**เวลา:** 2026-08-23 ~19:45–20:1x (+07:00) · session `exciting-goldberg-fli62w`
**ล็อก:** draft PR #31 (`pf_bridge`) เปิดก่อนทำงานตามลำดับ v5 ① — empty commit `round claim: exciting-goldberg-fli62w`

## probe ต้นรอบ (กติกา v4/v5)

| ข้อ | ผล |
|---|---|
| GitHub API/tool อ่านได้ไหม | ✅ list PR ทั้งสอง repo สำเร็จ (ผลว่างทั้งคู่ = ล็อกว่าง) |
| ทาง D (`ci-status`) มีชีวิตไหม | ✅ บน `pirate-force-server`: `git fetch origin ci-status` + `ls-tree` เห็นไฟล์ `ci/<sha>.json` ปกติ · บน `pf_bridge` ไม่มี branch `ci-status` — **ถูกต้องตามดีไซน์** (repo เอกสารไม่มี gate จึงไม่มีตัว publish-status) |

## สภาพต้นรอบ

- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ✅ มีจริง (11,388 ไบต์)
- กล่องจดหมาย: ไฟล์เดียวที่ยังไม่มีคู่ consumed คือ `20260823_1605_PANYA-DIRECTION-...` ซึ่งเป็น **หลุมศพชื่อไฟล์**
  (ประกาศในตัวว่า "ไฟล์นี้ไม่ต้องบริโภค" — ฉบับจริงคือ `..._1656_...` บริโภคแล้วโดย R128) ⇒ กล่องเคลียร์
- `external/` **ยังไม่เข้า git** — ฝั่งสะพานยังไม่ได้ `git add` ตามจดหมาย `FROM_CHIEF_R129_*` (ณ 19:54 +07:00)
- validator source ของ GT-047 จ็อบ 0 (`pf_validate_capture_fields.py`) ยังไม่ถูกส่งเข้า repo

## เลนที่ติดรอฝั่งสะพาน/Panya ทั้งหมด (เหตุที่รอบนี้ไม่มีงาน gameplay)

| เลน | ติดอะไร |
|---|---|
| attended ทุกใบ (GT-045/030/034/035/036/001) | ⏸ คำสั่ง Panya 16:56 — รอเธอว่าง |
| GT-053 → GT-052 → GT-050 (`CLIENT_RE_QUEUE.md`) | ต้องใช้อิมเมจ/ไฟล์บนเครื่องสะพาน |
| GT-049 · GT-047 จ็อบ 0 | ฝั่งสะพานเช่นกัน (047 รอ source เข้า repo) |
| โค้ดอ่านชุดส่งมอบ RE (คำสั่ง 18:22 ข้อ ⑤) | รอตาราง `external/` เข้า git ก่อน — เขียน parser โดยไม่เห็นไฟล์จริง = เดา schema ผิดวินัย |
| เลน headless สกิล | gate ไว้หลัง GT-050 ปิด (ตามลำดับ R128 — ไม่แซง) |

## งานที่ทำจริงรอบนี้ (backlog แม่บ้าน — เอกสารที่รู้ว่าโกหก)

**พบว่า:** `README.md:26` และ `AGENTS.md:128` มีบล็อกแก้แล้วว่า `tools\verify_foundation.ps1`
**ไม่ใช่ gate และผ่านไม่ได้** (พิน 79 members / build จริง 105 · จงใจปล่อยแดง — retire-or-re-pin เป็น decision ค้าง)
แต่เอกสารมีชีวิตอีกสองไฟล์ **ยังสั่งรันมันเป็น acceptance อยู่**:

1. `docs/COMMAND_HANDOFF.md` (~บรรทัด 695): "Run `tools\verify_foundation.ps1` once after a stable material implementation diff"
2. `docs/WORKFLOW.md` T3 (~บรรทัด 89): "**T3 — full acceptance:** `tools\verify_foundation.ps1`, ..."

**ผลเสียถ้าปล่อยไว้:** เอเจนต์กะใหม่ที่ทำตาม WORKFLOW T3 จะรัน check ที่แดงทุกครั้งโดยดีไซน์
แล้วเสียรอบวินิจฉัย หรือแย่กว่า — พยายาม "ซ่อม" pin เป็น 105 ซึ่งขัดเจตนา round 93 โดยตรง

**แก้:** แทนสองจุดด้วยชุด acceptance จริง (`py -3 -m pytest tests -q` · `py -3 tools\verify_hypothesis_ledger.py`
· `py -3 tools\verify_functional_coverage.py` + per-lane verifiers) พร้อมวงเล็บชี้ไปบล็อกเตือนใน `AGENTS.md`
· **ไม่แตะ** `docs/AI_TRANSFER_HANDOFF_20260817.md` (เอกสาร snapshot ลงวันที่ = บันทึกประวัติ ไม่ใช่คำสั่งปัจจุบัน)
· **ไม่ claim ว่า script ถูก retire** — คงสถานะ "decision ค้าง" ตามเดิม

**วินัย:** ผ่าน `pf-adversary` ก่อน commit (กติกา v5 ④) · T0: `git diff --check` clean · บรรทัดที่เพิ่มเป็น ASCII
(ยกเว้น em-dash ในหัว `**T3 — full acceptance:**` ซึ่งเป็นสไตล์เดิมของ T0–T2 ทุกหัวในไฟล์)
· ผล adversary: ดูท้ายไฟล์นี้

## ผล pf-adversary — หักร่างแรกได้จริง 2 จุดใหญ่ แก้ครบก่อน commit

| defect | ระดับ | สิ่งที่เจอ | ที่แก้ |
|---|---|---|---|
| 1 | HIGH | ร่างแรกลอกเลข "105" ลง WORKFLOW ทั้งที่ build จริง ณ HEAD = **122** (chief re-derive ซ้ำเองยืนยัน: pinned 79 · build 122 · 79 อยู่ครบ · เพิ่ม 43) — README/AGENTS เองก็เน่าอยู่ก่อนแล้ว | WORKFLOW เลิกอ้างเลข · README/AGENTS เปลี่ยนเป็นเลข**ลงวันที่** (105 @round93 · 122 @2026-08-23) + สั่ง re-derive ก่อนอ้างเสมอ |
| 2 | HIGH | T3 ใหม่เอ่ย "deterministic release + V141 immutability" แต่ไม่มีคำสั่งไหนในลิสต์ทำจริง — ผู้แก้ build_foundation_release ให้ timestamp รั่วจะเขียวทั้ง T3 | T3 ระบุกลไกจริง: V141 = sha guard ใน verify_hypothesis_ledger.py (บรรทัด 376/694) · release = build สองครั้ง เทียบ sha (ท่าเดียวกับ gate step) |
| 3 | MED | ประโยค "plus per-lane verifier" ใน COMMAND_HANDOFF ตกหล่น headless replay + commit-job guards เทียบกับ gate จริงใน AGENTS | เติม "and headless replay ... plus the commit-job guards AGENTS.md lists" |
| 4 | MED | STATUS.md:12 ชี้ว่า AI_TRANSFER_HANDOFF "governs" การ transfer — แปลว่าคำสั่ง gate เก่าใน section 10 ของมันยัง reachable ผ่าน pointer มีชีวิต | เติมหนึ่งประโยค correction ใน STATUS.md (ไม่แตะไฟล์ snapshot เอง — คงหลัก point-in-time) |
| 5-6 | LOW | em-dash ในหัว T3 (สไตล์เดิม T0-T2 · cp874 มี 0x97 map ได้ · docs ไม่ถูก print console) · Updated stamp ไม่ขยับ | คง em-dash ตามสไตล์ไฟล์ · bump Updated ทั้ง COMMAND_HANDOFF (08-16→08-23) และ STATUS (08-19→08-23) |

**สรุปไฟล์ที่แตะจริง (5 ไฟล์):** `docs/WORKFLOW.md` · `docs/COMMAND_HANDOFF.md` · `README.md` · `AGENTS.md` · `STATUS.md`
— กว้างกว่าร่างแรก (2 ไฟล์) เพราะ defect 1/4 ชี้ว่าปล่อยสองไฟล์บนไว้ = ความจริงยังแตกกันอยู่

**verification:** เขียว(cloud sanity) `python3 -m pytest tests -q` = **1901 passed · 324 skipped (เปิดเผยผ่าน skip-pins) · 4374 subtests** ·
`verify_functional_coverage.py` rc=0 · `verify_hypothesis_ledger.py` rc=0 · `git diff --check` clean ·
(gate ตัวจริง = Actions บน PR — รอผลตามท่อปกติ)

## คิวเทสเกม — คำตอบบังคับของรอบ (v5 ⑤)

**รอบนี้ไม่เพิ่ม/แก้ใบในคิว** เหตุผล: ใบ attended ถูกพักทั้งหมดตามคำสั่ง Panya 16:56 ·
ใบ static ค้างครบมือแล้ว (GT-053 → GT-052 → GT-050 · GT-049 · GT-047 จ็อบ 0) และทุกใบรอ **คนหน้าสะพาน** ไม่ใช่รอ chief ·
งานรอบนี้เป็น docs-only ฝั่งเซิร์ฟเวอร์ ไม่ผลิตพฤติกรรมใหม่ให้เทส

## สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์

- ไม่ได้พิสูจน์อะไรระดับ wire/DB — ไม่มีโค้ดรันไทม์ถูกแตะ
- ไม่ได้ตัดสินว่า `verify_foundation.ps1` ควร retire หรือ re-pin — decision นั้นยังเป็นของ Panya/round ถัดไปตามเดิม

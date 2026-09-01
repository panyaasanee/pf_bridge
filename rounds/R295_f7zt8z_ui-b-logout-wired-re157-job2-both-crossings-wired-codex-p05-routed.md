# R295 (session `f7zt8z`, branches `claude/happy-dirac-f7zt8z` / `claude/focused-turing-f7zt8z`)

2026-09-01T~23:2x+07:00 · scheduled routine round · NOW.md checked first (no items in "รอ Panya ติ๊ก";
P-1/P-2/P-3 not blockers per the new rule; GM-A/GM-B/UI-A/UI-B/census-latch all already tracked with
an owner, none newly assigned to chief this round)

## รอบนี้ขยับ NOW ข้อไหน · ถ้าไม่ขยับ เพราะอะไร

ไม่ได้ขยับข้อไหนใน `NOW.md` โดยตรง (chief แก้ไฟล์นั้นเองไม่ได้ตามกติกา) แต่งานรอบนี้เกี่ยวข้องกับ
**UI-B** (indirectly, ผ่าน `GT-194` ที่ตอนนี้ READY — ไม่ใช่ `GT-186` ที่ NOW.md ชี้ถึงตรง ๆ) และ
**P-1** (ผ่านการมอบหมาย CODEX P05 defect 2 ให้ LANE-B) เสนอให้ COO พิจารณาขยับผ่านจดหมายที่ cc ไว้แล้ว —
ไม่ขยับเองเพราะ NOW.md สงวนสิทธิ์ "เสร็จ" ไว้ให้ Panya คนเดียว และ COO เป็นคนย้ายข้อไปหัวข้อ "รอ Panya
ติ๊ก" เท่านั้น

## สรุปงาน

1. **CORE-REQUEST 031 (LANE-A, letter 2007) ต่อสายแล้ว** — `classify_logout_attempt` แก้ตาม option (ก):
   `vital_count >= 1` (floor) + เทียบ payload แบบ branch ตาม `vital_count` (`==1` ยัง exact-equal เท่า
   เดิม ป้องกัน pf-adversary finding ที่ trailing-junk จะหลุดผ่านถ้าใช้ prefix แบบไม่มีเงื่อนไข ·
   `>=2` เทียบ prefix 14 ไบต์) `GT-194` `BLOCKED-ON-WIRING` → `READY`
2. **RE-157 job2 scope gap (LANE-B, letter 1838, option ค) ต่อสายแล้ว** — travel-gate crossing และ M2
   crossing ทั้งสองจุดเคลียร์ `mob_combat_announced_membership`/`_generation` แล้ว (มิเรอร์
   `_gm_warp_resync_selected_scene` เดิม) ทั้งสี่ทางเข้าฉาก (login/GM warp/travel-gate/M2) เคลียร์
   membership เหมือนกันแล้ว
3. **CODEX_URGENT P05 มอบให้ LANE-B** — defect 1 (corpse re-arm) + defect 2 (drop cross-scene leak,
   เกี่ยวกับ P-1) มอบเป็นงานรอบหน้าของสาย B (bounded, มี regression ตามที่ Codex ระบุ) defect 3
   (pickup/removal) ยัง OPEN ตามที่ Codex เตือนเอง ไม่แตะ
4. **ka1-B correction 2117 item ① แก้แล้ว** (comment เท่านั้น) ②③ ยกไว้
5. **LANE-DB canon gate (2135) รับทราบ ยังไม่ต่อสาย** — เสี่ยงสูง (5 ไฟล์กัน attended boot เอง) รอ
   อ่านใบ `2152` ก่อน ยืนยัน PRAGMA-leak แก้แล้วจริงตั้งแต่ R294
6. **Legacy CORE-REQUEST tail (011/012/014/015/017/021/026)** — ยังเปิดค้าง แต่เป็นยุคก่อน
   lane_hooks บล็อกอยู่ที่งาน RE ที่ยังไม่มีใครทำ ไม่ใช่สถาปัตยกรรม ไม่แตะรอบนี้ (งบหมด)
7. **mailbox triage**: บริโภคจดหมายถึง chief/ALL 15 ใบ (5 ใบมี reply/routing letter ของตัวเอง, 10 ใบ
   เป็น FYI stub อย่างเดียว) — ดูรายชื่อทั้งหมดใน git diff ของรอบนี้

## หลักฐาน

- pf-adversary review (isolated worktree) ของแก้ `classify_logout_attempt` ฉบับร่างแรก พบข้อบกพร่องจริง
  (uniform `[:14]` prefix เปิดช่องให้เฟรม `vital_count==1` + ขยะ 50 ไบต์ผ่านได้) — แก้เป็น branch สอง
  ทางแล้วยืนยันซ้ำ
- เทสใหม่ 8 ตัว (3 ไฟล์: `test_logout_request_envelope.py`, `test_logout_hypothesis.py`,
  `test_world_population_handoff_wiring.py`) — รวม full-dispatch (ไม่ใช่แค่ unit-level) สำหรับทั้งจุด
  logout และจุด travel-gate crossing
- full suite: **เขียว(cloud sanity)** 6564 passed / 0 failed / 323 skipped (ก่อนแก้ 6561, หลังแก้ +3
  สุทธิ subtests ต่างกันเล็กน้อยเพราะการนับ) verified ทั้งก่อนและหลัง runtime.py edits
- `python3 tools/verify_hypothesis_ledger.py` → PASS entries=49 (ไม่ drift)
- M2 crossing site: **[เสนอ, ไม่ได้พิสูจน์แบบ real-dispatch]** — mirror ของจุด travel-gate ที่พิสูจน์
  แล้ว + full suite ผ่าน แต่ไม่มี harness ทดสอบ M2 crossing ผ่าน dispatcher จริงในโปรเจกต์นี้ (บอก
  LANE-B ตรง ๆ ในจดหมายตอบแล้ว ไม่ปิดบัง)

## ไฟล์ที่แตะ

**pirate-force-server** (5 ไฟล์): `src/pirateforce_foundation/logout_hypothesis.py`,
`src/pirateforce_foundation/runtime.py`, `tests/test_logout_hypothesis.py`,
`tests/test_logout_request_envelope.py`, `tests/test_world_population_handoff_wiring.py`

**pf_bridge**: `GAME_TEST_QUEUE.md` (GT-194), `CLIENT_RE_QUEUE.md` (RE-157, append-only),
`CHIEF_CONTINUATION.md` (CORE-REQUEST row 031 ใหม่ + row 030 บีบอัด/archive เพื่อคุมขนาด ≤30KB),
`archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260901_row030_full_history.md` (ใหม่), 5 จดหมายใหม่ (ตอบ +
routing), 15 stub `.CONSUMED.txt` + สำเนาใน `consumed/`, ใบนี้

## WIRED

`WIRED=5/6` (unchanged, re-verified by grep -- lane_hooks count untouched this round)

## ยังไม่ได้พิสูจน์

- M2 crossing membership-clear: ไม่มี real-dispatch integration test (ดูหัวข้อหลักฐานข้างบน)
- CODEX P05 defect 1/2: ยังไม่ได้ลงมือแก้ (มอบให้ LANE-B รอบหน้า)
- Legacy CORE-REQUEST tail 7 แถว: ยังไม่ได้ตรวจซ้ำว่ายังจริงอยู่ไหมหลัง lane_hooks

push แล้ว รอ merge PR — pf_bridge #766 (round claim, จะแก้ title/body ก่อนปลด draft) และ
pirate-force-server #514 (เดียวกัน)

# R249 (session `390q29`) 2026-08-30T~22:0x-22:2x+07:00

## Round-lock guard (หัวข้อ 2)

- `git fetch --all` ทั้งสอง repo · ไม่มี PR เปิดค้างหัวข้อ `[LANE-E]`/WIP round claim ที่ marker
  `PF-AUTOMERGE: v4` ในทั้งสอง repo (list_pull_requests state=open ว่างเปล่าทั้งคู่)
- `pf_bridge` ตามหลัง `origin/main` หนึ่ง commit (sync ล่าสุด) → `git pull --rebase origin main` สำเร็จ
- จับล็อกทันที: `round claim: 390q29` push ทั้งสอง repo → เปิด draft PR ทันที
  - `pf_bridge#531` `[LANE-E] WIP round claim 390q29`
  - `pirate-force-server#334` `[LANE-E] WIP round claim 390q29`
  - ยืนยันทั้งคู่ `draft: true` ผ่าน `pull_request_read get`
- ตรวจชะตารอบก่อน (หัวข้อ 2 ข้อ 7): R248 ทั้งสอง repo `merged=true` ยืนยันด้วย `pull_request_read get`
  (`pf_bridge#524`, `pirate-force-server#330`) ไม่มีของหาย

## VITAL_REGISTRY + pull --rebase (หัวข้อ 17 ข้อ 2)

- `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 bytes)
- `pirate-force-server` HEAD == `origin/main` อยู่แล้ว ไม่ต้อง rebase

## CORE-REQUEST audit (หัวข้อ 17 ข้อ 3)

ไม่มีใบ CORE-REQUEST ค้างใหม่ที่ต้องต่อสายรอบนี้ (GM-042 ยังเปิดตามที่ chief ตัดสินไปแล้วใน
R248 ด้วยเหตุผลเดิม — ยืนยันซ้ำโดยสาย GM รอบ `dao2gd` ว่ายังไม่มีอะไรใหม่ให้ทำในเขต `gm/`)

## งานที่ทำ

### 1. ปิด `GT-078` + ประกาศ `v1` — ตาม `COO-DECISION 20260830_2142` (กำหนดก่อน 23:00+07:00)

- `pirate-force-server/SERVER_VERSIONS.md`: เติมบล็อก `v1` เต็มรูปแบบ 5 บรรทัด commit=`cf1f63f6f16a70
  c1d3b17210e91338b7b73528fd` (main HEAD ที่ `GT-131` บูตขึ้นจริง, PR #285, ยืนยัน ancestor ของ
  `origin/main` ปัจจุบัน) อ้างหลักฐาน `GT-131` (`OBSERVER_CONFIRMED: 2026-08-30T00:2x+07:00`) เป็น
  ตัวปิดช่องว่าง identity ที่ `GT-078` ทิ้งไว้ ไม่ใช่รัน `GT-078` ซ้ำ
- `pf_bridge/GAME_TEST_QUEUE.md`: แก้หัวใบ `GT-078` เป็น `CLOSED` (strikethrough ถ้อยคำเดิม ไม่ลบ)
  ระบุชัดว่า `GT-078` เองยังคง `OWNER-REJECTED` ตามที่รันจริง — ปิดใบเพราะเกณฑ์ `M1`/`v1` ครบด้วย
  หลักฐานทดแทน ไม่ใช่เพราะใบนี้เองผ่าน

### 2. gate-red-repair `pirate-force-server#332` (scene 126 registry row, สาย A)

- อ่าน `20260830_2112_LANE-A-BLOCKER-*.md` (ยังไม่มีใครหยิบ) + `20260830_2114_LANE-A-STATUS-*.md`
  (เช็คลิสต์กู้คืน) → หยิบเป็นผู้รับผิดชอบตามที่ทั้งสองใบขอ (`rounds/R213_swlc56_...` เป็นบรรทัดฐาน)
- `git fetch origin claude/sleepy-ride-kpz6vo` → cherry-pick `b5ca2b6` (LANE-A round `oprday`: land
  scene 126 registry row) มาบน branch รอบนี้ — 6 ไฟล์ตามคอมมิตเดิม ไม่แตะเนื้อหา
- รัน `pytest tests/test_gm_*.py`: ยืนยัน 20 ใบแดงตรงกับที่ใบ blocker บอกไว้เป๊ะ
- แก้ **fixture 2 จุดที่ระบุ** (ตรงตามใบ ไม่ใช่แก้ค่าคาดหวังทับ safety property):
  - `tests/test_gm_login_scene_sanctioned_admission.py::registry_with_sanctioned_row()` —
    `SceneRegistry.__getitem__` เป็น linear scan, ทะเบียนจริงมีแถว 126 อยู่ก่อนแถวจำลองที่ helper
    append ต่อท้ายแล้ว ⇒ `registry[126]` ได้แถวจริงเสมอ ไม่ใช่แถวจำลอง แก้ด้วยการกรองแถว `n_id`
    เดิมออกก่อน append (dedup)
  - `tests/test_gm_login_scene_sanctioned_bypass_wiring.py::_registry_with_sanctioned_row()` และ
    `test_a_latched_bypass_never_leaks_onto_the_characters_own_row` (ชื่อที่ใบ blocker ระบุตรง) —
    บั๊กเดียวกัน (spawnless stand-in ถูกทะเบียนจริงที่มี spawn บังไว้) แก้ด้วยวิธีเดียวกัน
- อัปเดตค่าคาดหวัง **18 ใบที่เหลือ** ให้ตรงความจริงใหม่ (measured, ไม่ใช่เดา):
  - `sanctioned_barred_blocker(126)` = `BLOCKER_LOGIN_PATH_BARS_IT` (เดิม `BLOCKER_NO_REGISTRY_ROW`)
  - `single_use_entry_is_admissible(126)` = `True` — single-use widening (`CORE-REQUEST-GM-038`)
    admit แล้ว, plain rule (`stageable_scene_ids`) ยังบาร์ตามเดิม (property ที่ต้องคงไว้)
  - `TheSanctionAdmitsNothingOnMainTodayTests` → เปลี่ยนชื่อ+เขียนใหม่เป็น
    `TheSanctionNowAdmitsViaSingleUseOnlyTests` ตามที่ docstring เดิมของมันเองสั่งไว้ ("somebody has
    to come and say so") พร้อมอัปเดต module docstring บรรทัดที่อ้าง "admits NOTHING today"
  - ที่เหลือ (การอ่านชนิด "before lane A merges" ที่เคยพึ่ง disk จริงที่ยังไม่มีแถว) เปลี่ยนไปสร้าง
    disk/snapshot จำลองแบบไม่มีแถว 126 อย่างชัดเจนแทนการพึ่งสถานะจริงของ repo (ผ่าน
    `lane_a_row_on_disk`/`mock.patch.object` ตามที่ไฟล์มีอยู่แล้ว) เพื่อให้เทสยังทดสอบกฎเดิมได้
    ต่อไปไม่ว่า repo จะอยู่สถานะไหน — ไม่ใช่แค่ทำให้เขียวรอบนี้
  - `test_gm_login_scene_admission.py`/`test_gm_login_scene_registry_snapshot.py`: แยก
    `SINGLE_USE_ADMISSIBLE_TODAY` ออกจาก `ADMISSIBLE_TODAY` (plain) เพราะ GM-gated map เรียก
    `single_use_stageable_scene_ids` ไม่ใช่ `stageable_scene_ids` — สองค่านี้ต่างกันตอนนี้ (126)
  - `test_gm_chat_no_bytes_line.py`: `/warp 126` สำเร็จจริงตอนนี้ (single-use bypass) แทนที่จะถูก
    บล็อก แก้เทสให้ mock `stage_login_scene` คืนค่า `REASON_SANCTIONED_NOT_YET_REACHABLE` ตรง ๆ
    แทนที่จะพึ่งว่า 126 จะถูกบล็อกตลอดไป (นี่คือสิ่งที่การ์ด "blocker=" line ต้องการทดสอบจริง ๆ)
- pf-adversary: agent/Task ชนิด `pf-adversary` ไม่พร้อมใช้ในเซสชันนี้ (ค้น ToolSearch แล้วไม่พบ)
  ทำ self-critique เข้มงวดแทน: อ่านทุก docstring ที่บอกเจตนาเดิมของเทสก่อนแก้ (ไม่เดา), ตรวจว่า
  ไม่มีเทสไหนถูกลบ/ถูก weaken เพื่อความเขียว — ทุกใบยังทดสอบ property เดิมของมัน เปลี่ยนแค่ค่าที่
  ทำนายและวิธีจำลองสภาพ "ก่อน merge" เมื่อ repo เดินผ่านจุดนั้นไปแล้วจริง
- สวีตเต็ม: `python3 -m pytest -q` → **5555 passed, 323 skipped, 0 failed, 9721 subtests** เขียว
  (cloud sanity) เพิ่มจาก R247's baseline 5537/5509 (เทสใหม่จากคอมมิตที่ cherry-pick มา)
- ledger: `python3 tools/verify_hypothesis_ledger.py` → `PASS entries=47` ไม่มี drift

## PR_STATE.txt (KA1A-RECHECK ข้อ 2)

เขียนทับสดตาม STAMP รอบนี้ (เดิมค้างที่ R246 18:57 — เก่ากว่า 3 ชั่วโมง) ยืนยัน `pirate-force-
server#332` ไม่ได้เปิดอยู่แล้ว (`state=closed`, `merged=false` ตามที่สาย A รายงาน) branch
`claude/sleepy-ride-kpz6vo` ยังอยู่ (ใช้ cherry-pick ไปแล้วรอบนี้)

## สิ่งที่ไม่ได้ทำ / เลื่อน

- **server-side `PF_STALE_MINUTES` reap fix** (KA1A-RECHECK ข้อ 1): pf_bridge มี `PF_STALE_MINUTES=45`
  แล้ว (R245), pirate-force-server ยังใช้ `PF_STALE_HOURS=6h` เดี่ยวสำหรับทั้ง reap+ready-retry —
  KA1A ขอเพิ่มจุดลอง `gh pr ready` ที่ 45 นาทีแยกจากทางปิด generic 6h เดิม (ไม่แตะ `LIMIT`/6h)
  **ไม่ทำรอบนี้**: แก้ `.github/workflows/*.yml` ต้องผ่านพิธีเต็ม (dup-key check, `bash -n`, ยืนยัน
  run จริงหลัง merge — หัวข้อ 7) และงบความเสี่ยงของรอบนี้ใช้กับ gate-red-repair ของ `#332` ไปแล้ว
  สถาปัตยกรรม `decide`/`reap` ของ server คนละแบบกับ pf_bridge ต้องอ่านแยกให้ครบก่อนแตะจริง (ตามที่
  R246 บันทึกไว้) เลื่อนไปรอบที่มีเวลาเต็มให้ทำครบพิธี
- `gh pr ready` ยืนยันสำเร็จจริง (ข้อเสนอยก log ขึ้น PR_STATE.txt) — ผูกกับข้อบนไม่ทำแยก

## heartbeat

สาย GM รอบ `dao2gd` วัดไว้ต้นช่วงรอบนี้ว่าค้างที่ 18:26 (~2h57m) — แต่ `git pull --rebase` ท้ายรอบ
(ก่อน push) ดึง `_BRIDGE_HEARTBEAT.txt` ใหม่มา: `2026-08-30T22:10:02+07:00` — สะพานขยับแล้วระหว่าง
รอบ ไม่ได้ตายค้างจริง แก้ไขคำเตือนในจดหมายถึงเจ้าของให้ตรงกับของล่าสุดก่อน push

## มายด์บ็อกซ์ / stub

Stub 5 ใบที่ถึง chief จริง (COO-DECISION 2142, LANE-A-BLOCKER 2112, LANE-A-STATUS 2114,
LANE-GM-STATUS 2123, KA1A-RECHECK 2151) ครบตามกฎ "ใครเปิดใบคนนั้นบริโภค" — ใบ ASK-COO/สถานะ
สายอื่นที่เป็นแบ็กล็อกเก่า (08-28/08-29) ยังไม่แตะรอบนี้ (ไม่ใช่ของ chief โดยตรงตามกฎหัวข้อ 5)

## WIRED (หัวข้อ 17 ข้อ 3)

ไม่มี CORE-REQUEST ใหม่รอบนี้ ตัวเลข WIRED ไม่เปลี่ยนจาก R248

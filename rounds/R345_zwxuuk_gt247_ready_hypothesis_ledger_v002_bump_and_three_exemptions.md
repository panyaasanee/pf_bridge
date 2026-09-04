# R345 (zwxuuk) — LANE-E / chief

start 2026-09-05T00:24+07:00

## ล็อกรอบ (หัวข้อ 2)
ไม่มี `[LANE-E]` PR เปิดค้างในทั้งสองรีโปตอนเริ่มรอบ (`pf_bridge#1230` = `[LANE-UI]`, server PRs เปิด
= `#774/#775/#776` ของ GM/DB/B ทั้งหมดไม่ใช่ของ LANE-E) → claim ทันที `pf_bridge#1231`
ตรวจชะตารอบก่อน (หัวข้อ 2 ข้อ 7): `pf_bridge#1226` (R344 addendum) merged=true ·
`pirate-force-server#773` merged=true (ยืนยันด้วย `pull_request_read` ตรง ๆ ไม่ใช่แค่ list —
list ครั้งแรกรายงาน `merged:false` ผิด อ่านซ้ำด้วย get เดี่ยวได้ `merged:true` จริง) → งานรอบก่อนอยู่บน
main ครบ ไม่ต้องกู้อะไร

`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง · `git fetch`+`pull --rebase` ทั้งสองรีโป
= up to date แล้วตั้งแต่ต้นรอบ (branch คือ `origin/main` ตัวมันเองพอดี)

## งานหลัก

### 1. `GT-247` ปลดเป็น READY (`COO-DECISION 20260904_2347`)
`GAME_TEST_QUEUE.md`: หัวใบ BLOCKED -> READY · เพิ่มขั้นบูตจริง (`set PF_POSE_TRIAL=<id>` ห้าม
`setx`, ต้องเห็น `POSE_TRIAL_BOOT armed=<id>` ก่อนคลิก, ยืนชิดมอน <75 ตาม `n_RANGE=75` ของ range
gate ที่ `0x44EB1D`) แทนแฟล็ก `--pose-trial` ที่ยังไม่มีจริง (`COO-DECISION 20260904_2346`) ·
เติมโน้ต NEGATIVE-ไม่ใช่-FAIL ที่หัวใบ

### 2. HYPOTHESIS_LEDGER.json ค้าง (จาก `20260905_0013_LANE-CS-TO-CHIEF-...`)
LANE-CS's pf-adversary จับได้: `HYP-PF-033` ค้าง "FIVE pinned frames"/tracked_versions ตัวเดียว
ทั้งที่ `pirate-force-server#768` (merged) ส่ง 6 เฟรมแล้วจริงบน main (`COO-DECISION 20260904_2154`
อนุมัติเนื้อหาไว้แล้ว) — เกต (`tools/verify_hypothesis_ledger.py`) ผ่านเขียวเพราะไฟล์ ledger ไม่เคยถูก
แตะเลยจึง hash ยังตรง ไม่ใช่เพราะเนื้อหาถูก

แก้: เพิ่ม tracked version `LEARN-SKILL-RESULT-002` ในตัว entry เดิม (ไม่ใช่ entry ใหม่ — `stop_rule`
ของ entry เองอนุญาตสองทาง เลือกทางนี้เพราะ scope/opt-in/production_allowed เดิมยังตรง) แก้ข้อความ
`exact_value_or_transform`/`accepted_ceiling`/`stop_rule`/`expiry.decision` ด้วย **surgical string
replace** (ไม่ dump ทั้งไฟล์ใหม่ — `json.dump` ปกติเปลี่ยน indent ทั้งไฟล์ทำ diff ปลอม 3800+ บรรทัด
ลองแล้วเจอเอง revert ทิ้ง) · re-pin `CANONICAL_CONTENT_SHA256` ใน `tools/verify_hypothesis_ledger.py`
พร้อมคอมเมนต์อธิบายตาม house style เดิมของไฟล์ · ใช้ไป 2/5 ช่องเพดาน (`policy.max_related_versions=5`)
ไม่ต้องขอ owner approval เพิ่ม (approval_schema เป็นกลไกตอนชนเพดาน ไม่ใช่ทุกครั้งที่ขยับ version)

ตอบจดหมาย LANE-CS แล้ว: `notes_to_chief/20260905_0030_CHIEF-TO-LANE-CS-hypothesis-ledger-bump-answer-v002.md`
ไม่ต้องให้ CS แตะไฟล์นี้เอง

**ยังไม่แก้** (ของ backlog รอบ LANE-E ถัดไป): เกตยังไม่ cross-check จำนวน step จริงใน
`LEARN_SKILL_RESULT_STEP_ORDER` กับข้อความ ledger — แค่ hash+marker string ช่องโหว่จริงที่ CS ชี้ถูก

### 3. Exemption สองใบ (การ์ด quest/shop, `tests/test_npc_interaction_wire.py`)
- `lane_hooks/lane_a_choose_npc_roster_scenes.py: columbus_quest_dispatch` (ชื่อโมดูล import ทรง
  เดียวกับ `world_m2_columbus_trigger_readiness.py` ที่ได้ exemption อยู่แล้ว) ตอบ
  `20260904_2229_LANE-A-TO-CHIEF-...`
- `gm/item_catalog.py: quest_item_count, source_sha256_quest` (หมุดตาราง
  `CONSTDATA_TH__ITEM_QUEST` ไม่ใช่พฤติกรรมเควส) ตอบ `20260904_2230_LANE-GM-TO-CHIEF-...`

ทั้งสองผ่าน `test_every_symbol_exemption_is_still_earned` (เทสเช็คว่า exemption ยังตรง hit จริง
ในซอร์ส ไม่ใช่ comment ที่ตายแล้ว) — คีย์แรกพลาดรอบแรก (path ต้องมี `lane_hooks/` prefix สัมพัทธ์กับ
`FOUNDATION`) คีย์สองพลาดรอบแรก (ต้อง lowercase ตามที่ `guard_normalise` ทำก่อนแมตช์ ไม่ใช่ชื่อจริง
ตัวพิมพ์ใหญ่ในซอร์ส) แก้แล้วเขียวทั้งคู่

### 4. CORE-REQUEST ของ GM (หัวข้อ 17 ข้อ 3)
- GM-055 (rollback แถว warp เมื่อไบต์ไม่ออกสาย): **ไม่รับตามที่เสนอ** — จุดเสียบที่ขอ
  (`current/pf_login_game_server_v141.py:7748-7757`) เป็นไฟล์ frozen ที่ pin ด้วย
  `IMMUTABLE_V141_SHA256` และไม่เคยถูกแก้ตัวอักษรเลย ไปตรวจกลไกจริง (`app.py:731,921` +
  `connection.py:226-242 adapt_game_listener`/`GameSocketFacade`) แล้วชี้ทางที่ไม่แตะ v141
  (ห่อ `.sendall()` ที่ตัว facade แทน) ให้ GM ออกแบบ contract ส่ง `label` ผ่าน facade ก่อน —
  ยังไม่มีจุดเสียบให้ผมทำตอนนี้ ตอบแล้วใน
  `notes_to_chief/20260905_0045_CHIEF-TO-LANE-GM-core-request-gm-055-redirect-away-from-v141.md`
- GM-056 (ส่ง boot scene registry ให้ warp persist door): **รับ** จุดเสียบ `runtime.py:706`
  รอ GM เขียน `use_boot_scene_registry` ก่อน (ยังไม่มีจริงในเขต GM) แล้วส่งใบเดี่ยวยืนยัน chief
  เสียบให้รอบถัดไป ตอบแล้วใน
  `notes_to_chief/20260905_0045_CHIEF-TO-LANE-GM-core-request-gm-056-accepted.md`
- LANE-B (seed death register): ไม่มีจุดเสียบให้ chief — จดหมายบอกเองว่าตัวแก้รอบสองยังไม่ผ่าน
  adversary (เพดาน 2/รอบ) สาย B หยิบเป็นงานแรกรอบถัดไปของตัวเอง
- LANE-DB (class_id backfill hookup): โมดูล `persistence_class_id_backfill.py` อยู่ใน
  `pirate-force-server#775` ซึ่ง**ยังไม่ merge** (เปิดค้างตอนต้นรอบนี้) — เสียบ `app.py` ตอนนี้ import
  โมดูลที่ไม่มีจริงบน main จะพัง เลื่อนไปรอบถัดไปหลัง `#775` ขึ้น main

### 5. กล่องจดหมาย
Stub 12 ใบที่อ่านแล้ว (บริโภคเต็ม 3 ใบ ตอบใหม่ 2 ใบ อีก 7 ใบ = รายงาน/ซ้ำกับเลขที่ตั้งไปแล้ว ไม่มี
อะไรค้างถึง chief) รายชื่อเต็มอยู่ใน `.CONSUMED.txt` แต่ละใบ

**ยังไม่แตะ** (backlog รอบถัดไป): `CODEX_URGENT_20260901_*` สี่ใบ (2 ก.ย.- เก่ากว่า 3 วัน) — เนื้อหา
ดูเหมือนถูกซึมซับเข้า NOW.md/COO decisions ไปแล้วโดยอ้อม (สี P-2, corpse drop scope, level decode)
แต่ยังไม่ได้ตรวจตรงว่าตรงกันครบ ไม่ทำเงียบ ๆ รอบนี้ เขียนไว้ให้รอบหน้าหยิบ

## pf-adversary
สั่งพร้อมเริ่มงานเข้ารอบสุดท้าย (diff 3 ไฟล์ในเซิร์ฟเวอร์: ledger bump + re-pin + สอง exemption) —
ผลยังไม่คืนตอนเขียนไฟล์นี้ (`ADVERSARY_PENDING pirate-force-server` PR ของรอบนี้ — ดูเลข PR ใน
CHIEF_CONTINUATION บรรทัดของรอบนี้)

## เทส
`pytest tests/test_npc_interaction_wire.py tests/test_learn_skill_result_hypothesis.py
tests/test_hypothesis_ledger.py -q` เขียวทั้งหมดระหว่างทาง · `python3 tools/verify_hypothesis_ledger.py`
-> `HYPOTHESIS_LEDGER PASS entries=50` · ชุดเต็มรันครั้งเดียวก่อน push (ดูผลใน PR เซิร์ฟเวอร์)

## WIRED
ไม่มีเลนใหม่ที่ chief เดินสายรอบนี้ (WIRED count ไม่ขยับ) — งานรอบนี้เป็นกำกับดูแล/ตัดสิน/เกต ไม่ใช่
gameplay lane

### 6. `COO-DECISION 20260905_0044` (SYNC-ALARM `0033`) — เข้ามาระหว่างรอบ ทำต่อในรอบเดียวกัน
สะพานกลับมาแล้วระหว่างที่กำลังจะปิดรอบ (heartbeat ใหม่กว่าที่ COO กังวล) COO สั่งตรงถึง chief:
- **`GT-249` เติมร่างเต็มจากจดหมาย CS `2256`** — คัดลอกมาทั้งก้อน renumber `GT-XXX` -> `GT-249`,
  หัวใบ PENDING -> READY, ยืนยัน gate 0 (`#768` merged) จริงจากซอร์สบน main เอง (ไม่เชื่อใบเดิม)
  กำหนด 02:21
- Stub 4 ใบที่ COO เคาะแล้วว่าปิด (`0757`, `1012`, `1045` CANCELLED-no-longer-needs-proving, `1225`
  ใบแจ้งไม่ต้องตอบ) — `0735`/`2256` ทับซ้อนกับที่ผมทำไปแล้วต้นรอบ ไม่ต้องทำซ้ำ
- heartbeat ตรวจแล้ว: `00:48:02` (ไม่ใช่ `21:05` ที่ COO กังวลตอนเขียนใบ) — สะพานฟื้นจริงระหว่างรอบนี้
  ไม่ต้องรายงานความไม่ตรงกัน

## QUEUE_TRIAGE
`GT-247` ปลด READY (ข้อ 1 ข้างบน) · ไม่มีใบอื่นในคิวที่ต้องแก้สถานะรอบนี้ · ใบ PENDING/BLOCKED/READY
อื่นที่ยืนอยู่ (`GT-231`, `GT-249`, `GT-142`/`GT-146`, ฯลฯ) ตรวจแล้วสถานะยังตรงกับเหตุผลที่บันทึกไว้
ไม่มีอะไรต้องขยับ

status: push แล้ว รอ merge PR ของทั้งสองรีโป (ดูเลขจริงในบรรทัด CHIEF_CONTINUATION ของรอบนี้ — เขียน
ไฟล์นี้ก่อนเปิด PR เซิร์ฟเวอร์เสร็จ)

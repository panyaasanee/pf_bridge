# R121 (session 5wixs1) — เก็บสวีต static เข้าท่อ precondition + ปลด GT-033 variant C

- เวลาเริ่ม: 2026-08-21 ~11:00 (+07:00) — commit timestamp ของรอบเป็น UTC ตามระบบ
- branch: `claude/confident-wozniak-5wixs1` (pf_bridge) · `claude/busy-bohr-5wixs1` (pirate-force-server)

## ล็อกรอบ (v5 ข้อ ①)

- ต้นรอบไม่มี PR เปิดค้างทั้งสอง repo ⇒ จับล็อก: empty commit + PR #21 (non-draft ตาม v5)
- 🔴 **PR #21 ถูก workflow merge/ปิดใน ~11 วินาที (เปิด 04:00:53Z ปิด 04:01:04Z) — ล็อกหลุดเป็นครั้งที่เจ็ดติดกัน**
  (ซ้ำ pattern R115–R120 ทุกประการ) · empty claim commit ของมันจึงติดอยู่บน main (9072a80 — ไม่มีเนื้อหา ไม่อันตราย)
- ยึดล็อกคืนด้วย **draft PR #22** — ท่าที่ R115 พิสูจน์ (`draft - skipped` ใน log ของ workflow)
- 📌 ย้ำข้อเสนอของ R119 อีกเสียง: **v5 ข้อ ① ควรสั่งเปิด draft PR ตั้งแต่แรก** — เจ็ดรอบติดที่ non-draft ถือล็อกไม่ได้จริง

## PROBE (หลังล็อก)

- `gh` CLI: **ไม่มี** (เหมือน R112 เป็นต้นมา) · GitHub API ผ่าน MCP: **ใช้ได้จริง** (list/create PR สำเร็จรอบนี้)
- ทาง D (`ci-status`): **มีชีวิต** — fetch ได้ · อ่านคำตัดสิน `7b80025` = success (run 32444037989)
- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`: **มีจริง** — โครงพี่น้องปกติ

## กล่องจดหมาย

- ทุก `.md` มี `.CONSUMED.txt` คู่ครบ — **ไม่มีของใหม่ให้บริโภครอบนี้**

## งานที่ 1: ปลด GT-033 variant C (คิวเทส — หน้าที่ข้อ ⑤)

- HYP-PF-031 (chat-push `0x709E` · สร้างโดย R120) **merge เข้า main แล้ว** — merge commit `c6146a3`
- `pf_resolve_green_boot.py` ตอบ: **BOOT_COMMIT `7b8002522fedeecf9bcd5ea9d0d4ec5e732e4034`**
  (คำตัดสินเขียวของตัวเอง · tree byte-identical กับ main `c6146a3` — วัด ไม่ใช่เดา)
- แก้ `GAME_TEST_QUEUE.md` 5 จุด: หัว entry GT-033 → 🟢 variant C พร้อมรัน · บรรทัดสรุปหัวไฟล์ 2 จุด ·
  หัวบล็อก variant C · แทนบรรทัด "ห้ามรันจนกว่า..." ด้วยท่าบูต + SHA + ที่มาของคำตัดสิน
- คาเวียตการตีความผล (ผลลบกำกวม · one-shot latch ราย connection) **คงไว้ครบ ไม่แตะ**

## งานที่ 2: เก็บสวีต static เข้าท่อ precondition (แม่บ้านที่ R120 จดไว้)

- Reproduce ตรงกับ R120 เป๊ะ: `pytest tests -q` บน clone สด = **192 failed / 1854 passed / 30 skipped / 70 errors**
- สาเหตุ: เทส static ~26 โมดูลอ้าง client image / install tree / capture corpus แล้ว **fail แทน skip**
  (ขัดวินัย SKIP-CENSUS-001 ที่ pin ไว้ใน `tests/pf_preconditions.py` + `docs/PYTEST_SKIP_PINS.json`)
- ข้อไขของปริศนา R120 ("ขัดกับ R118 ยังไง"): **คนละ scope** — gate บน Actions `--ignore` โมดูลพวกนี้ทั้งก้อน
  (สร้าง exclusion list จาก grep `GameClient|capture_v141` — ประกาศเปิดเผยใน log) ตัวเลข R118 จึงไม่เคยรวมพวกมัน
  ⇒ งานรอบนี้คือทำให้ **สวีตเต็มบน clone สดก็สะอาด** โดยไม่แตะ workflow ของ gate (exclusion เดิมยังทำงานเหมือนเดิม)
- วิธี: ลูกมือ 7 ตัวขนาน แบ่งโมดูลไม่ทับกัน · guard เฉพาะเทสที่แดงจริง (ห้าม skip เทสที่รันได้ —
  กติกาใน pins doc เอง) · import ของ tools ที่อ่าน binary ตอน import ถูก guard ด้วย `CLIENT_IMAGE.present`
- **ผลหลัง guard ครบ 26 โมดูล: `pytest tests -q` = 1855 passed / 281 skipped / 0 failed / 0 errors**
  (ก่อน: 192 failed + 70 errors · passed เพิ่ม 1854→1855 เพราะบางเทสที่ไม่ต้องใช้ artifact เคยตายใน
  `setUpClass` ตอนนี้ได้รันจริง — เช่น `test_remote_movement_projection_static` ได้ 2 ใบ ·
  `test_move_authority_targetpos_static` ได้ 2 ใบ)
- **เพิ่ม registry key ใหม่ 1 ตัว: `evidence_tree`** (`evidence/` — capture transcripts v74-v83 ที่
  allowlist `.gitignore` กันออกโดยเจตนา) — สองเทสของ `test_structural_corpus_audit.py` ไม่มี key เดิมคุ้ม
- **พบหนี้ชั้นสอง:** skip เก่า ~25 ใบใน 8 โมดูล (ยุคก่อน registry) เหตุผลไม่มี token `[precondition:...]`
  ⇒ census จะ fail แบบ UNDECLARED — ส่งลูกมือตัวที่ 8 แปลงให้ใช้เหตุผลจาก registry (design skip
  `runtimeres_death_hypothesis:491` ที่ pin แล้ว ไม่แตะ)
- guard ซ้อน (เทสที่อ่านทั้ง `GameClient.bin` + `GameClient.local.bin`): เครื่องที่ไม่มีทั้งคู่รายงาน key
  ตามลำดับ guard ตัวแรก — เลข pin ยึดตาม clone สด (all-absent) · เครื่องลูกผสม (มี tree แต่ไม่มี local.bin)
  เลขจะย้าย key — จดใน pins note แล้ว
- pins: generate จาก transcript จริง (`-rs` เป็นตัวนับ · junit-xml เป็นตัวตั้งชื่อ) ไม่ลอกจากรายงานลูกมือ

### หนี้ชั้นสาม (พบระหว่างทำ) และการแก้

- **self-test ของ census (`PinFileTests`) บังคับ:** ทุก pin ต้องมีรายชื่อเทสครบ (`count == len(tests)`)
  และ **source ต้องประกาศ guard เท่ากับ count เป๊ะ** — ตัวนับเดิมเป็น substring count ที่นับได้เฉพาะ
  guard แบบหนึ่งบรรทัดต่อหนึ่งเทส ⇒ ชนกับ class-decorator (1 จุดคุม N เทส) · module-level skip
  (1 collection skip นิรนาม) · setUp guard (1 จุด N skip) · guard ซ้อนสอง key (key ที่รายงานแปรตามเครื่อง)
- แก้สามทาง: ① **ตัด shape ที่ pin ไม่ได้ทิ้งทั้งหมด** — โมดูล module-level-skip 3 ตัว
  (`chat_channel_family` · `stats_progression` · `use_drop_sell`) restructure เป็น per-method guard
  (ผลพลอยได้: เทสที่ไม่ต้องใช้ binary 10 ใบที่เคยโดน skip นิรนามกลืน ตอนนี้ได้รันจริง) ·
  setUp guard ของ `client_ui_asset_inventory` ย้ายเป็น class decorator + assertion partial-tree ในตัวเทส
  ② **guard ซ้อนยุบเหลือ key เดียวต่อเทส** (กติกา: อ่าน `GameClient.local.bin` ⇒ `client_image`
  เพราะ local image อยู่ในทรี ⇒ implied · อ่านเฉพาะไฟล์อื่นในทรี ⇒ `game_install_tree` ·
  capture+backups ⇒ `capture_v141` + คอมเมนต์) — ast sweep ยืนยันไม่เหลือเทสถือสอง key ทั้ง tests/
  ③ **เขียน witness ใหม่เป็น ast-based `counted_guard_uses()`** — นับ class deco = จำนวน test method ·
  method deco = 1 · require/skipTest/pytest.skip ในตัวเทส = 1 · resolve alias ระดับ module ถึง fixpoint
  (รองรับ `SKIP_REASON = CLIENT_IMAGE.reason + ...` และ helper function) — smoke test 19 คู่ (module,key)
  ตรงเป๊ะทุกคู่ก่อนใช้จริง

### ตัวเลขปิดรอบ (cloud sanity ทั้งหมด)

- สวีตเต็ม: **1865 passed / 324 skipped / 0 failed / 0 errors** (4298 subtests)
- census: **PASS** — 323 precondition skips + 1 design skip = 324 · pins 45 entries
- ASCII additions: ไม่มีอักขระนอก ASCII ในบรรทัดที่เพิ่มทั้งหมด · ไฟล์แก้ 36 ไฟล์ ไม่มีลบ/เพิ่มไฟล์
- **exclusion list ของ gate ไม่ขยับแม้แต่ไฟล์เดียว** (เทียบ set ก่อน/หลังด้วย grep แบบเดียวกับ workflow)

## ผล pf-adversary (บังคับตาม v5 ④ — ยิงก่อน commit)

- **แก้ก่อน commit 2 ข้อ:** ① guard กับ census oracle ชี้คนละ path ใน `test_runtimeres_death_hypothesis`
  (probe 3-candidate เดิมทำให้เครื่องที่มี image เฉพาะตำแหน่ง staging จะ census แดงปลอม) — รวม oracle เป็น
  `CLIENT_IMAGE.require` · ② witness นับด้วย substring ของ `ast.unparse` ⇒ string literal ปลอม guard ได้
  และ `.present` probe กลายเป็น alias — แก้เป็นการนับจาก `ast.Name` จริง + ตัด `.present` จาก alias
  + เพิ่ม self-test ใหม่: **ชื่อเทสใน pins ต้อง re-derive จาก source ได้ตรงกันทั้ง 45 entries**
  (ปิดช่อง "ย้าย guard ไปผิดเทสแล้วทุกอย่างยังเขียว")
- **ยอมรับเป็นข้อจำกัดที่ประกาศ (ไม่ใช่ regression — witness เดิมก็มี):** dead-code launder
  (`if False:` ครอบ guard) ยังหลอก static counter ได้ · เทสที่ต้องใช้สอง tree guard ตัวหลักตัวเดียว
  (เครื่องลูกผสมที่ไม่มีจริงจะแดงดัง ไม่ใช่เขียวปลอม — วัดจริงแล้ว: capture ว่าง ⇒ 8 failed ดัง ๆ) ·
  parser ของ census ไม่รู้จัก absolute path แบบ Windows (pre-existing · gate เรียกแบบ relative จึงไม่โดน)
- **คำถามใหญ่ที่ adversary ทิ้งไว้ (เสนอ Panya):** pinned skip ของ `client_image`/`game_install_tree`
  (310 จาก 326) ไม่มีเครื่องไหนใน CI ที่ *รันจริง* — gate exclude โมดูลพวกนี้ · เครื่องที่วัด = cloud round
  เท่านั้น ⇒ **เสนอเพิ่ม job Linux บน Actions รันสวีตเต็ม (ไม่ exclude) + census บน clone สด** —
  ต้องแก้ gate workflow จึงขอ Panya เคาะก่อน chief ไม่แตะเอง

## PR ของรอบนี้

- `pirate-force-server` **PR #6** (commit `e816e73` · 36 ไฟล์ · PF-AUTOMERGE: v4) — gate ตัดสิน
- `pf_bridge` **PR #22** (draft ถือล็อกทั้งรอบ — แปลงเป็น ready ตอนปิดรอบ)

## สิ่งที่ไม่ได้พิสูจน์ / nonclaims

- เขียวรอบนี้ (ถ้าได้) = **เขียว(cloud sanity)** เท่านั้น — กับดัก cp874 และ Python 3.14 ไม่มีอยู่ที่นี่
- การ guard ไม่เปลี่ยนพฤติกรรมบนเครื่องที่มี artifact (decorator เป็น no-op เมื่อ present) — โครงสร้างการันตี
  แต่**ไม่ได้วัดบนเครื่องที่มี artifact จริง** — จะถูกวัดจริงครั้งแรกโดย gate เต็มบนสะพาน

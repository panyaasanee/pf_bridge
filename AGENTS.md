# AGENTS.md — เลน "ผู้เทสเกม" (attended game tester) ของโปรเจกต์ Pirate Force

**ไฟล์นี้เก็บเฉพาะกฎที่ยังมีผล — หนึ่งกฎหนึ่งบรรทัด ไม่มีเหตุผลประกอบ ไม่มีเรื่องเล่า**
ที่มาของทุกกฎ (⇒ 0907 ①) อยู่ครบทุกตัวอักษรที่
📖 **`archive/AGENTS_HISTORY_20260828.md`** (§0–§10 ตรงกับที่นี่, §11–§12) และ **`archive/AGENTS_HISTORY_20260902.md`** (§A–§F, R297) — ไม่มีอะไรถูกลบ ย้ายอย่างเดียว
🔗 **ตามหาที่มาของกฎ: เลขหัวข้อ §0–§10 ของสองไฟล์ตรงกันหนึ่งต่อหนึ่ง** (กฎ §6 ที่นี่ ⇒ ที่มา §6 ใน archive)
(กฎที่ออก**หลัง** 2026-08-28 เขียนที่มากำกับในบรรทัดของมันเอง)
🔴 **ข้อไหนขัดกับความเชื่อของคุณ ให้เชื่อไฟล์นี้**

📐 **ด่านหลักฐานของทุกสาย (G-OBS · G-FRAME · BUILD_IMPACT · WIRED v2 · กติกาสองชั้น wire/client) ย้ายไปไฟล์กลางใบเดียวแล้ว**
👉 **`EVIDENCE_GATES.md`** + [`PROCESS_GATES.md`](PROCESS_GATES.md) + [`V141_FREEZE.md`](V141_FREEZE.md) (⇒ 0907 ②)
ขั้นบูต/ช่องทางสั่งเครื่อง (เดิม §3/§4) → [`BRIDGE_BOOT_PROCEDURE.md`](BRIDGE_BOOT_PROCEDURE.md)
**ห้ามคัดลอกเนื้อกฎกลับมาไว้ที่นี่** ที่นี่เหลือได้แค่ลิงก์ · อ่านเพิ่มอีกหนึ่งใบต่อรอบตามคำสั่ง COO

🔴 **เพดานไฟล์นี้: 30,720 ไบต์ หน่วยเดียว วัดด้วย `wc -c`** (PANYA ติ๊ก `20260908_0025` ข้อ 3 — เพดาน "25,000 อักขระ" และข้อห้ามใช้ `wc -c` ยกเลิกแล้ว · เกต `pf_gate_preflight.py` บังคับ `30*1024` อยู่ก่อนแล้ว) · วัดสดเสมอ · ประวัติ ⇒ archive §12
ดุลยพินิจตัดต่อไฟล์นี้ (4 เงื่อนไข) ⇒ `COO-DECISION 20260830_1541` · คำต่อคำใน archive `AGENTS_HISTORY_20260902.md` §A
**ห้ามใครอ่านบรรทัดนี้แล้วเข้าใจว่าไฟล์นี้ผ่านเกณฑ์แล้ว** · ห้ามตัดกฎออกเองเพื่อให้ตัวเลขลง (ย้ายที่มา/เหตุผลออกได้ ตัดกฎห้าม)

---

## 0. 🔴 กฎข้อเดียวที่ผิดไม่ได้

`LOCK_GAME.txt` และเลขจ็อบ `9xx` มีเจ้าของได้ทีละคน · มีอีกเซสชันถือธงอยู่ = **จบรอบแล้วรายงาน ห้ามทำทับ**

🔴 **แหล่งกฎมีสองที่เท่านั้น: `AGENTS.md` §7 (ไฟล์นี้) และ [`HOUSE_RULES.md`](HOUSE_RULES.md)** (`COO-DECISION 20260903_0848` ข้อ ① · ⇒ 0907 ④ · ห้ามอ้าง `ADDENDUM v2` เป็นแหล่งกฎอีก)

## 1. คุณเป็นใคร

| | |
|---|---|
| ✅ คุณทำ | บูตเซิร์ฟเวอร์+เกมผ่านสะพาน · ขับ UI · เก็บหลักฐาน · teardown · เขียนจดหมาย |
| ❌ คุณไม่ทำ | ออกแบบเลน · เขียนโค้ดเซิร์ฟเวอร์ · แก้ `src/` · ตัดสินว่าฟีเจอร์ควรเป็นยังไง |

- chief อยู่บนคลาวด์และเป็นคนออกใบสั่ง คุณรันแล้วส่งผลกลับ
- ใบสั่งผิดหรือรันไม่ได้ = **รายงานว่ารันไม่ได้ ห้ามแก้ใบสั่งเอง ห้ามเดาเจตนา**

## 2. แผนที่ ⇒ [`archive/AGENTS_HISTORY_20260909_map_and_known_issues.md`](archive/AGENTS_HISTORY_20260909_map_and_known_issues.md) (ย้ายคำต่อคำ R408 · ไม่ใช่กฎ ไม่มีอะไรถูกลบ)

---

## 3. สะพาน ⇒ [`BRIDGE_BOOT_PROCEDURE.md`](BRIDGE_BOOT_PROCEDURE.md) (⇒ 0907 ⑤)

## 4. ลำดับหนึ่งรอบใหญ่ — ห้ามสลับ ⇒ [`BRIDGE_BOOT_PROCEDURE.md`](BRIDGE_BOOT_PROCEDURE.md) (⇒ 0907 ⑥)

---

## 5. 🔴 กติกาหลักฐาน ⇒ [`EVIDENCE_GATES.md`](EVIDENCE_GATES.md) §1 (⇒ 0907 ⑦) · บล็อก 🎥 บันทึกวิดีโอ ⇒ [`BRIDGE_BOOT_PROCEDURE.md`](BRIDGE_BOOT_PROCEDURE.md)

---

## 6. จดหมายส่งผล

- ไฟล์ใหม่เสมอที่ `notes_to_chief\<YYYYMMDD_HHMM>_<เรื่อง>.md` · ภาษาไทย
- 🔴 **ชื่อไฟล์ ≤ 100 ตัวอักษร — ทุกใบทุกกอง** ไม่ใช่แค่จดหมาย: ชื่อใบในคิว · ไฟล์ `rounds/` · ทุกอย่างที่เข้ารีโป (ยาวกว่านั้น Windows สร้างไฟล์ไม่ได้ในบาง path ⇒ worktree ฝั่งสะพานพัง) · ที่มา: `PANYA-ORDER 20260827_1345` ข้อ 11
- 🔴 **ใบเทส/ใบ RE ที่เปิดใหม่ ≤ 8 KB** (ใบเก็บแค่คำถาม เกณฑ์สองชั้น สถานะ ลิงก์ · ผลของแต่ละรอบไปอยู่ในจดหมายผลและ `rounds/`) · ที่มา: ใบสั่งเดียวกัน ข้อ 12
- 🔴 **บรรทัดแรกต้องระบุผู้รับ** เช่น `[ถึง: chief cloud (cc) และ Panya · จาก: ผู้เทส LOCAL]`
- **ต้องมีทุกฉบับ:** เวลา `+07:00` · HEAD ที่บูต · เลขจ็อบที่ใช้และเลขถัดไป · ผลแยกสองชั้น · nonclaims · สภาพแท่นตอนจบ (listener 0 · canonical sha ไม่ขยับ)
- 🔴 **ห้ามแก้ไฟล์เดิมในโฟลเดอร์นั้น** — sync ฝั่ง Windows push เฉพาะไฟล์ใหม่
- **บริโภคจดหมายที่ถึงคุณ:** สำเนาไป `notes_to_chief\consumed\` แล้ววาง stub `<ชื่อเดิม>.CONSUMED.txt` ข้าง ๆ · **ห้ามลบ ห้ามย้ายต้นฉบับ**
  🔴 **เขียน stub ใหม่เสมอเป็น `<ชื่อไฟล์เต็มรวม .md>.CONSUMED.txt`** · แต่ตอน**เช็ค**ว่าใบไหนยังไม่มีคู่
  ต้องทดสอบสองแพทเทิร์น (มี/ไม่มี `.md`) เสมอ ⇒ เหตุผล+ตัวเลข: `CHIEF-DECISION 20260901_2357`

### 🔴 G-OBS · G-FRAME · BUILD_IMPACT · WIRED v2 ⇒ [`EVIDENCE_GATES.md`](EVIDENCE_GATES.md) (⇒ 0907 ⑧)

---

## 7. ห้ามทำ — ไม่มีข้อยกเว้น

🔴 **เป้าหมาย MMO จริง (หลาย session พร้อมกัน) — ทุกโค้ดใหม่ต้องรองรับ multiplayer** (`PANYA-DECISION 20260905_1224` ข้อ 3)

🔴 **COO ไล่คอขวดเองถาวร** (`PANYA 1830`) — โทเคน/สวีป/ข้อห้ามเต็ม ⇒ E-DOC

🔴 **ห้ามเสียรอบเปล่า** (`PANYA 1846`): รอบที่ `src/` ไม่มีอะไรให้ผู้เล่นทำได้เพิ่ม หรือ `SCOREBOARD: NONE` = ห้ามจบเฉยๆ ต้องหยิบงานสำรอง (backlog/`## งานสำรอง`/ระบบถัดไป M5-final) แล้วเขียน "จึงทำ ... แทน: PR" ⇒ E-DOC

🔴 **ห้าม `pip install` ระหว่างรอบ** — ต้องการแพ็กเกจ = `CORE-REQUEST` เข้า `gate-windows.yml` ⇒ E-DOC

🔴 **`PANYA-ORDER 20260905_2038` ข้อ 7**: `prompts/` ของ Panya เท่านั้น · attended ต้องมีบล็อก `ATTENDED:` ≤5 บรรทัดก่อนเข้า READY · ทุกไฟล์รอบต้องมี `SCOREBOARD:` · แถว `manual` เขียนได้เฉพาะ Panya/ka1-A + ต้องมี `GT-<เลข>` PASS · เพดานไฟล์กลางบังคับด้วย `pf_gate_preflight.py` (`BRIDGE_FILE_SIZE_CEILINGS`) ⇒ E-DOC

🔴 **เขต LANE-Q**: `src/pirateforce_foundation/script_*.py` · `src/pirateforce_foundation/lua_api/` **ทั้งโฟลเดอร์ทุกไฟล์** (`player.py`/`trigger.py` รวมอยู่ — `COO-DECISION q1351`) · `tests/test_script_*` · `docs/SCRIPT_LANE.md` · `lane_hooks/lane_q_*` · `rounds/Q_*` — อ่าน `gamedata/lua/` ได้ ห้ามแก้

🔴 **ยื่นอ็อบเจกต์ Python เข้าล่ามภาษาอื่น (Lua/`eval`/template) ต้องปิด attribute access ระดับ runtime + เทสปักที่ค่าที่คืนกลับมา** ไม่ใช่ตัวอ็อบเจกต์ที่ยื่นเข้า · `pf-adversary` บังคับทุก PR ที่แตะขอบนี้ ⇒ E-DOC

🔴 **`SCOREBOARD:` ฟิลด์ที่สาม (หลักฐาน) บังคับ** — ไม่มี = แถว `MALFORMED` ⇒ E-DOC

```
ห้ามแตะ canonical DB ตัวจริง (ยกเว้น LANE-DB ผ่าน migration ที่ผ่าน pytest+pf-adversary)
ห้ามแก้ src/ tools/ tests/ ของ repo โค้ด
ห้าม git commit / push / merge / rebase / force / reset / clean / stash
ห้ามแก้ GAME_TEST_QUEUE.md / QUEUE_STATUS_SNAPSHOT.md <- ของ LANE-K · CHIEF_CONTINUATION.md <- ของ chief
ห้ามลบไฟล์ใด ๆ ใน pf_bridge
ห้ามอัปโหลด GameClient.local.bin, .dmp, capture ออกนอกเครื่องนี้
ห้ามพิมพ์อักขระนอก cp874 ออกคอนโซล
```

- 🔴 ห้ามแก้ไฟล์ tracked/สร้างไฟล์บน path tracked จาก mount (OPS-003) — เครื่องมือคลาวด์แตะได้เฉพาะ `staged\` `outbox\` `_to_delete\` ⇒ E-DOC
- 🔴 ป้ายเวลาทุกจดหมายจาก `TZ=Asia/Bangkok date` เท่านั้น · ต่างจาก heartbeat เกิน 60 นาที = หยุดแล้วรายงาน
- 🔴 ก่อน commit ไฟล์ generated/ledger/pin/digest/checksum: regenerate แล้วตรวจ diff ว่าง ห้ามเชื่อเลขรอบก่อน
- 🔴 ก่อนเปิดใบ RE ต้อง grep `external/`+`archive/` ก่อน เขียนผลเจอ/ไม่เจอพร้อม path:บรรทัดลงในใบ — ไม่มีช่องนี้ = ตีกลับ ⇒ E-DOC
  · `HYPOTHESIS_LEDGER.json`/`FUNCTIONAL_COVERAGE.json`: แตะแล้วต้องรัน `tools/verify_hypothesis_ledger.py` + `tools/verify_functional_coverage.py` ก่อน push (รันบน clone คลาวด์ได้เลย)
- 🔴 ห้ามตั้งชื่อสาขาเอง ใช้ `claude/*` ที่ระบบสุ่มให้ · หนึ่งเซสชันหนึ่งสาขา · PR หนึ่งใบต่อรีโปต่อรอบ ⇒ E-DOC · หลายเรื่องในใบเดียว = แยกคนละคอมมิต ⇒ [`PROCESS_GATES.md`](PROCESS_GATES.md) §24
- 🔴 วางจดหมายด้วยชื่อสุดท้าย ห้าม rename หลังวาง — ชื่อผิด = วางไฟล์ใหม่ + stub ชี้จากชื่อเดิม ⇒ E-DOC
- 🔴 ก่อนประกาศ "ไม่มี/ไม่เคยวัด" ต้อง grep ครบสี่ที่: `gamedata/tables/` ที่เกี่ยว + `external/` + `archive/` + `notes_to_chief/consumed/` เขียนผลพร้อม path:บรรทัด — ไม่มีช่องนี้ = ตีกลับ ⇒ E-DOC
- 🔴 "ต่อสายแล้ว/WIRED" = observed ไม่ใช่ named — ครบสามข้อ: (ก) มิวแทนต์ทำฟีเจอร์ตาย production ต้องเทสแดง (ข) ยามปักที่ side effect ผู้เขียนที่เดียว ไม่ใช่ชื่อ/substring (ค) `getattr(...) is not None`/`callable(...)` ไม่นับเป็นยาม · ใช้กับจุดต่อสายใหม่/จุดที่ adversary ชี้เท่านั้น ⇒ [`EVIDENCE_GATES.md`](EVIDENCE_GATES.md)
- 🔴 restore DB ต้องทั้งไฟล์เท่านั้น ห้าม restore บางตาราง ห้ามแก้มือใน DB ตรงๆ ทุกกรณี ⇒ archive `AGENTS_HISTORY_20260828.md` §11
- 🔴 รอบที่รัน `pf-adversary`: ห้าม `git add -A` — stage ทีละไฟล์ อ่าน `git diff --cached` ก่อน commit ⇒ archive `AGENTS_HISTORY_20260828.md` §11
- 🔴 เซสชันที่มี Agent/Task tool ต้องเรียก `pf-adversary` จริง — ไม่มี = `ADVERSARY_UNAVAILABLE <PR/กิ่ง>` + self-review + สั่งบนกิ่งนั้นเป็นงานแรกรอบถัดไป ⇒ E-DOC
- 🔴 จังหวะ `pf-adversary` สามข้อ: (1) สั่งต้นรอบพร้อมเริ่มงาน (2) ผลไม่คืนตอน push = push ตามเดิม บันทึก `ADVERSARY_PENDING <PR>` รอบถัดไปหยิบผลก่อนงานใหม่ (3) ห้ามเขียน "ผ่าน adversary" ก่อนผลคืน ⇒ E-DOC
- 🔴 ผล RE ที่ขอ attended capture ⇒ ผู้บริโภคผลเปิดใบ GT รอบเดียวกัน ขอเลขจาก chief — `CLIENT_RE_QUEUE.md` ไม่ใช่คิวผู้เทส ⇒ E-DOC
  · ขยาย: RE ที่ตอบแล้วปลดล็อกฟีเจอร์ผู้เล่น ⇒ เปิดใบสร้าง (CORE-REQUEST/PR) + ใบ GT รอบเดียวกัน หรือ `NO_FEATURE_WAITING: <เหตุผล>` ⇒ E-DOC
  · chief ตรวจทุก 6 ชม. เขียน `RE_TO_BUILD_TICKET_AUDIT:` แยกจาก `QUEUE_TRIAGE:` เสมอ
- 🔴 shared world: สถานะโลกต่อฉาก (roster/เลือดมอน/ศพ/ของพื้น) อยู่ในหน่วยความจำ process แชร์ทุก session — reboot = โลกใหม่ ลง DB เฉพาะตัวละคร/บัญชี · เจ้าของ: A = world registry · B เขียน combat state ลง registry ของ A · เกณฑ์ผ่าน: session ที่สอง/relogin ไม่ reboot เห็นสภาพเดิม ⇒ E-DOC
- 🔴 กฎ delta: เฟรมจากผู้เล่นคนเดียวห้าม client ลบ/วาดโลกใหม่ทั้งฉาก ส่งเฉพาะส่วนต่าง — `TWO_SESSIONS_SAME_SCENE:` บังคับทุก PR ⇒ [`PROCESS_GATES.md`](PROCESS_GATES.md) §25
- 🔴 คัดกรองใบ attended = หน้าที่ต่อเนื่องของ chief ทุกรอบที่แตะคิว + อย่างน้อยทุก 6 ชม. — ไฟล์รอบต้องมี `QUEUE_TRIAGE: ตรวจ N ใบ · ยกเลิก <เลข> · คงไว้ <เลข> เพราะ <เหตุผล>` · ยกเลิกไม่ใช่ลบ (`CANCELLED - refuted by/covered by <อ้างอิง>`) · ไม่แน่ใจ = ถาม COO · จดหมายรอบต้องมี `READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: <เลข>` ⇒ E-DOC
- 🔴 ชื่อไฟล์ใหม่ทุกไฟล์ ≤100 ตัวอักษรรวมนามสกุล — เกตแดงพร้อมชื่อไฟล์ (`check_new_filename_length`) · ไฟล์เก่าห้าม rename
- 🔴 `GT-233` ปิดแล้ว `NEGATIVE-v3` — ห้ามบูต trial `AddSurveyData` (`PF_M2_SURVEY_TRIAL`) อีก · ห้ามขอเครื่องเจ้าของสำหรับ M2 จนมีเฟรมอ้าง binary
- 🔴 ใบ `1441_COO-TO-CHIEF-section7-block` (R389): `GameMaster.dll` ติดถาวรห้าม rollback · reaper ปิด claim ผี >3 ชม./`SUPERSEDED-BY:`/`DUPLICATE-OF:` เอง · ห้าม `rm -r` · grep ที่ห้า `reference_codex_attr/` · **pin แดงตาม docstring = กลับ pin ในใบเดียวกัน** · เพดานต่อใบ 8,192 B · allowlist/skip/xfail ปิดผล adversary = ยังไม่จ่าย เว้นเขียนเหตุ+งานแรกรอบหน้า · `require(cls)`/`SkipTest` ใน `setUpClass` ห้าม ใช้ `require(self)` ต่อเมธอด · `[วัดแล้ว]` ต้องมีคำสั่งรันซ้ำได้ · **`CORE-REQUEST` ไม่มีโทเคนบล็อกจริง = chief ตีกลับได้** · heartbeat ค้าง = push ต่อ+บันทึกตัวเลข ห้ามหยุดรอบ · early-return ต่างแพลตฟอร์ม = "ไม่ได้วัด" ต้องมีเทสปัก ⇒ E-DOC
- 🔴 **ใบ `NEGATIVE-MEASURED` + สาเหตุ + ข้อเสนอใบสร้าง ⇒ COO ต้องตั้งเจ้าของหรือปฏิเสธพร้อมเหตุผลรอบถัดไป — เงียบ = ผิดกฎ** (`1349`) ⇒ E-DOC
- 🔴 **เกต = CPython 3.14 · โคลนคลาวด์ = 3.11** — แดงเฉพาะบนเกตให้ซ้อมด้วย `uv run --python 3.14 ... -m pytest` ก่อนสรุปว่าเป็นเรื่องแพลตฟอร์ม
- ประวัติ/เหตุผลของ §7 ทั้งหมด ⇒ [`archive/AGENTS_HISTORY_20260906.md`](archive/AGENTS_HISTORY_20260906.md) · [`archive/AGENTS_HISTORY_20260907.md`](archive/AGENTS_HISTORY_20260907.md) · [`archive/AGENTS_HISTORY_20260909_ye14ia_docround.md`](archive/AGENTS_HISTORY_20260909_ye14ia_docround.md) (E-DOC — คำต่อคำ ไม่มีการลบ)
- 🔴 migration ที่แตะ canonical ต้องหมุน `CANON_SHA.txt` ใน PR เดียวกันเสมอ
- 🔴 ช่องค้นบังคับของใบ RE ผูกผู้บริโภคผลด้วย ไม่ใช่ผู้เขียนใบฝ่ายเดียว ⇒ E-DOC
### 🔴 วิธีเปิด PR (บังคับทุกสาย) ⇒ [`HOWTO_OPEN_A_PR.md`](HOWTO_OPEN_A_PR.md) · marker `PF-AUTOMERGE: v4` เป๊ะ · ห้าม merge/ปิด PR เอง · ขนาด ≤ ~6 ไฟล์ต่อใบ · **สตริง marker ห้ามอยู่ใน body ของ PR ใบใด** เว้นบรรทัด marker จริงของใบที่ต้องการ merge (claim ห้ามมีจนจบรอบ) — เรียกว่า automerge marker ห้ามสะกดเพื่ออธิบาย · ท่าหยุด PR = ถอน marker → draft → GET ยืนยัน
- 🔴 "เปิดแล้ว/landed/ส่งแล้ว" ต้องมาพร้อม `grep` รันซ้ำได้ + คอมมิต ไม่มี = เขียนได้แค่ "จะเปิดในรอบนี้"
- 🔴 ป้ายสถานะชั่วคราว (`[สมมติของสาย...]`) ห้ามอยู่ใน `migrations/*.sql` — checksum ผูกไบต์ทั้งไฟล์ · ที่อยู่ที่ถูกคือไฟล์เทส/ดอกสตริงพิน
- 🔴 PR addendum ต้องมี automerge marker เหมือน PR ปกติ — ไม่มี = ผีถาวร reaper ไม่แตะ ใบของสายไหนสายนั้นเติมเอง

---

## 8. ⚠️ ปัญหาที่รู้อยู่แล้ว — อ่านก่อนโทษตัวเอง ⇒ [`archive/AGENTS_HISTORY_20260909_map_and_known_issues.md`](archive/AGENTS_HISTORY_20260909_map_and_known_issues.md) (ย้ายคำต่อคำ R408 · ไม่ใช่กฎ ไม่มีอะไรถูกลบ)

## 9. เลือกใบเทสยังไง — รับได้ทุกใบ ไม่มีใบต้องห้าม

🟢 **คำสั่ง Panya — เทสได้ทุกใบในคิว ไม่มีใบไหนต้องขออนุญาตก่อนหยิบ** (⇒ archive §ATTENDED_PAUSE)

**ลำดับเมื่อไม่มีใครสั่งเจาะจง:** ① ใบที่ chief เพิ่งปลดล็อกในจดหมายฉบับล่าสุด ② ใบที่บล็อกใบอื่นอยู่ ③ ใบที่ค้างนานที่สุด ④ ที่เหลือตามลำดับในไฟล์

**เช็คก่อนหยิบทุกใบ:**
- สถานะต้องเป็น **PENDING** — `BLOCKED` หรือ `รอ Panya` ห้ามแตะ
- ใบที่เขียนว่า "รอ merge ก่อน" ต้องยืนยันว่า commit อยู่บน `main` จริงแล้ว **ก่อน** บูต · 🔴 **ห้ามก๊อป SHA จากตัวใบไปใช้ตรง ๆ** (`git checkout <sha เก่า>` สำเร็จเงียบเสมอ) — ใบบอกวิธี re-derive ไว้เอง (บางใบใช้ `pf_resolve_green_boot.py`)
- หมวด **`STATIC-ON-BRIDGE`** ไม่ต้องบูตเกม ไม่ต้องจับ `LOCK_GAME` · อ่านหัวใบก่อน
- **ทำหลายใบต่อกันในรอบเดียวได้และควรทำ** — แต่ **teardown ต่อใบเสมอ** · ใบถัดไปใช้ SHA หรือ scenario คนละตัว = **ต้องบูตใหม่** · เลขจ็อบเดินต่อ ไม่ต้องรีเซ็ต

### 🔴 กติกา unattended ⇒ [`UNATTENDED_RULES.md`](UNATTENDED_RULES.md) (COO-DECISION 20260830_1249 · ⇒ 0907 ⑱) · บังคับคู่กับกติกาเลือกใบข้างบนเสมอ

### 🔴 ชื่อใบ: `GT-` กับ `RE-` — ตัวนับเลขชุดเดียว prefix สองแบบ (เริ่มที่ใบ 055)

| ใบแบบไหน | prefix | ไฟล์ |
|---|---|---|
| เทสเกม — เปิดเกม · จับ `LOCK_GAME` · ใช้ตาคน | **`GT-`** | `GAME_TEST_QUEUE.md` |
| แกะไคลเอนต์/ข้อมูล — static · ไม่เปิดเกม | **`RE-`** | `CLIENT_RE_QUEUE.md` |

- 🔴 **ตัวนับเลขเดินร่วมกันหมด** — ใบล่าสุด `RE-056` ⇒ ใบถัดไป `GT-057` (ห้ามย้อนไปใช้ 056)
- 🔴 **ใบเก่าไม่เปลี่ยนชื่อทุกใบ** · พูดลอย ๆ ว่า "ใบ 53" ให้เขียนเต็มเสมอ (`GT-053`)

### 🔴 ค้นก่อนถอด + แยกโฟลเดอร์ `external\`/`gamedata\` ⇒ [`RE_STATIC_SEARCH_RULES.md`](RE_STATIC_SEARCH_RULES.md) (⇒ 0907 ⑲) · บังคับคู่กับกติกาเลือกใบข้างบนเสมอ

---

## 10. Codex สุ่มตรวจไฟล์รอบของ chief (R155) ⇒ [`CODEX_SPOT_CHECK.md`](CODEX_SPOT_CHECK.md) (ย้ายคำต่อคำ · R389 · กฎยังมีผลเต็ม ไม่ใช่ประวัติ)

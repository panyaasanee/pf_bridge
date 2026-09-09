# R409 (`ye14ia`) — เอกสารรอบเดียว: AGENTS.md ลงใต้เพดาน + HOUSE_RULES/prompts `2220` + ปิดรูเกต skipIf พลิกเงื่อนไข

รอบ: `ye14ia` · LANE-E (chief) · เริ่ม 2026-09-09T15:26+07:00
claim PR: `pf_bridge#1991` · PR เซิร์ฟเวอร์: **ไม่มี — รอบนี้ไม่แตะ `pirate-force-server` เลย** (ทุกงานอยู่ใน `pf_bridge`: `AGENTS.md` · `HOUSE_RULES.md` · `prompts/` · `tools_bridge/`)
ตาม `COO-ORDER e1428` (`notes_to_chief/20260909_1452_COO-ORDER-e1428-one-document-round-for-agents-md-unless-1181-landed-first-LANE-E.md`) — เช็คก่อนเริ่ม: `pirate-force-server#1181` ยัง `draft`/`mergeable_state=dirty`, ไม่ใช่ ancestor ของ `origin/main` (ยืนยันผ่าน GitHub API ตอนต้นรอบ) ⇒ เข้าเงื่อนไข "รอบเอกสาร" ไม่ใช่ `login_entry`

## รอบนี้ขยับ NOW/M ข้อไหน
ไม่ขยับไมล์สโตนใด (M2 ยังรอ `#1181`) — รอบนี้เป็นงานกระดาษที่ COO อนุมัติเต็มรอบล่วงหน้าแล้วผ่าน `e1428` (ข้อยกเว้นของ "ห้ามเสียรอบเปล่า" คือ "COO สั่งรายกรณีลง NOW" ซึ่งใบนี้คือคำสั่งนั้น) เคลียร์หนี้เอกสารที่บล็อกทุกสายอ่านกฎเดียวกันไม่ทัน (AGENTS.md เกินเพดาน = เกต `pf_gate_preflight.py`'s `[bridgesize]` แดงถ้าใครดันให้มันโตอีก)

## 1) AGENTS.md ใต้เพดาน
- `wc -c AGENTS.md` ก่อนรอบ = **43,394** ไบต์ (เกินเพดาน 30,720 ตาม `PANYA ติ๊ก 20260908_0025`) → หลังรอบ = **26,087** ไบต์ ทั้งสองวัดสด
- วิธี: §7 ("ห้ามทำ") ซึ่งกิน 31,421/43,394 ไบต์ (72%) ย่อเหลือกฎละบรรทัด+ลิงก์ตามธรรมเนียมเดิมของไฟล์เอง (`⇒ 0907 N` ก็ทำแบบนี้อยู่แล้ว) — เนื้อเต็มคำต่อคำ **ไม่มีอะไรถูกลบ** ย้ายไป `archive/AGENTS_HISTORY_20260909_ye14ia_docround.md` พร้อมหมายเหตุว่าอะไรเปลี่ยนจริง (แค่การจัดวาง ไม่ใช่ความหมาย)
- ทุกโทเคน/สตริงที่กฎอื่นๆ grep หา (เช่น `PF-AUTOMERGE: v4`, `check_new_filename_length`, `BRIDGE_FILE_SIZE_CEILINGS`, `CANON_SHA.txt`, `ADVERSARY_PENDING`) ยังอยู่ในบรรทัดย่อครบ — ตรวจด้วย `git grep` รายตัวก่อน commit ว่าไม่มีตัวไหนหาย
- §7 สองบรรทัดใหม่ตามคำสั่ง `e1428` ข้อ 3:
  (ก) เขต LANE-Q: `lua_api/` ระบุชัดว่าเป็น **ทั้งโฟลเดอร์ทุกไฟล์** (`player.py`/`trigger.py` รวมอยู่) อ้าง `COO-DECISION q1351` — ก่อนหน้านี้ path ระบุถูกอยู่แล้วแต่ไม่ได้เขียนชัดว่า "ทั้งหมด"
  (ข) "กฎยังไม่ลง §7" จาก `NOW.md`: ตรวจแล้วทั้งสี่ข้อ (pin แดงตาม docstring กลับ pin ใบเดียว / `CORE-REQUEST` ต้องมีโทเคนบล็อกจริง / `1349` ผลลบ+ใบสร้าง COO ตั้งเจ้าของ / เกต 3.14-คลาวด์ 3.11) **มีอยู่ใน §7 อยู่ก่อนแล้วทั้งหมด** (บรรทัดใบ `1441_COO-TO-CHIEF-section7-block` + บรรทัดแยกสองบรรทัดถัดมา) — ไม่ใช่ช่องว่างจริง ไม่ต้องเพิ่มเนื้อใหม่ COO ตัดบรรทัดนั้นออกจาก `NOW.md` ได้ตามที่ `e1428` ข้อ 4 บอกว่าจะทำเอง

## 2) HOUSE_RULES.md + prompts — กฎ `2220`
- `HOUSE_RULES.md`: เพิ่มหัวข้อใหม่ `## กฎ 2220` (ไม่แตะบล็อกประวัติคำต่อคำเดิม) มีครบ 5 ข้อบังคับ + ข้อยกเว้นเดียว + เส้นแบ่งที่ไม่เปลี่ยน คัดมาจาก `notes_to_chief/20260908_2220_KA1A-PANYA-ORDER-*.md` ข้อ 2/3/5
- `prompts/COMMON_LANE_ROUND.md`: เพิ่มหัวข้อย่อเดียวกัน (5 ข้อ+ข้อยกเว้น) ต่อจากบรรทัด `<TAG>/<PREFIX>` ก่อนหัวข้อ "แหล่งความจริง..." — ไฟล์นี้ทุกสาย builder อ่านทุกรอบอยู่แล้ว
- `prompts/LANE-A.md` `LANE-B.md` `LANE-CS.md` `LANE-DB.md` `LANE-GM.md` `LANE-K.md` `LANE-Q.md` `LANE-UI.md` (8 ไฟล์): เพิ่มบรรทัดเตือนสั้นบรรทัดเดียวต่อจากบรรทัด "อ่าน NOW.md เป็นไฟล์แรก" ชี้กลับไป `COMMON_LANE_ROUND.md`+`HOUSE_RULES.md` §2220
- `git grep -rn "ห้ามเดาเกินที่วัดได้\|รอผล attended ก่อนขยับค่า\|ยังไม่เคยวัด\|เผื่อไคลเอนต์" prompts/` **ก่อน**แก้ = 0 ผล — ถ้อยคำเก่าที่ต้องแทนที่ไม่เคยปรากฏเป็นข้อความจริงใน `prompts/` (เป็นวัฒนธรรมที่ไม่ได้เขียนเป็นกฎลอย) จึงไม่มีอะไรให้ "แทนที่" ตรงตัว มีแต่ "เพิ่ม" กฎ `2220` เป็นข้อบังคับใหม่ตามคำสั่ง
- ปกติ `prompts/` เป็นเขตของ Panya เท่านั้น (AGENTS.md §7) — รอบนี้แก้ได้เพราะ `PANYA-ORDER 20260908_2220` ข้อ 6 สั่งตรงว่า "COO + chief: แก้ HOUSE_RULES.md และ prompt ของทุกสาย" และ `COO-ORDER e1428`/`1312` ส่งต่อคำสั่งนั้นมาที่ผมโดยตรง

## 3) ปิดรูเกต preflight (`1416`)
- ที่มา: `notes_to_chief/20260909_1416_LANE-GM-TO-CHIEF-preflight-cannot-see-a-flipped-skipIf.md` (pf-adversary D1 บนกิ่ง `xbfcsi`/server PR #1187) — ที่คอมมิต `8c46237` `[skips]` และ `[census]` เดิมพิมพ์ PASS ทั้งคู่ ขณะที่ census จริง (`tools/pf_pytest_precondition_census.py --run`) เจอ 25 เคส skip เงียบ เพราะการเปลี่ยนแปลงพลิกเงื่อนไข `skipIf` ที่มีอยู่แล้วโดยไม่เพิ่ม marker ใหม่บรรทัดไหนเลย
- พิจารณาแล้วไม่ทำตามข้อเสนอแรก (ให้ `[census]` เรียก `--run` จริงทุกครั้ง): `--run` เดิน `python -m pytest tests -q -rs` เต็มไดเรกทอรีเสมอ (อ่านโค้ด `run_pytest()` แล้ว) ชุดเต็มมีหลักหมื่นเคส (PR #1181 body วัด 15,668 passed) — เอามาเป็นเกตก่อน push ทุกครั้งจะทำให้ preflight ช้าเท่าเกต Windows ที่มันมีไว้ประหยัดรอบเดินทาง (Windows รันชุดเต็มให้ทุก PR อยู่แล้ว — `CHIEF.md` §10)
- ทำจริง: ฟังก์ชันใหม่ `check_skip_condition_drift` ใน `tools_bridge/pf_gate_preflight.py` — สแกนไฟล์ `import`/`from ... import` ของทุก `tests/test_*.py` ที่มีตัวช่วย skip อยู่แล้ว (`SKIP_MARKERS` เดิม) resolve เป็น path ใต้ `src/` แล้วเทียบกับ `git diff --name-only base...HEAD` ของกิ่งนี้ — ถ้ากิ่งแตะไฟล์ที่ไฟล์เทสนั้น import ตรง (ไม่ใช่ผ่านสาย import อ้อม) ⇒ พิมพ์แถว `[skipdrift] WARN` ชี้ชื่อไฟล์เทส+ไฟล์ที่ชนกัน แนะให้รัน `--run` จริงก่อน push
  - **advisory เท่านั้น** — ไม่เพิ่มเข้า `results[]` ใน `main()` (แบบเดียวกับ `check_consumed_stub_warning`/`check_mode_bits_probe` ที่มีอยู่แล้ว) ⇒ ไม่มีทางทำให้เกตแดงผิดที่ ไม่มีทางบล็อกสายที่ไม่เกี่ยว — false positive ที่นี่ = ข้อความเตือนเปล่า ไม่ใช่ PR ตกม้าตาย
  - **nonclaim**: เป็น heuristic import ตรงชั้นเดียว ไม่ใช่กราฟ dependency จริง — ไฟล์ A import B, B import C, กิ่งแตะ C จะไม่ถูกจับ (เหมือนที่ `SKIP_MARKERS` เดิมเป็นแค่ลิสต์สะกดคำ ไม่ใช่ parser — คอมเมนต์ในโค้ดบอกไว้ตรงๆ)
- ทดสอบ: `python3 -m py_compile` ผ่าน · จำลอง diff จริง (สร้างกิ่งชั่วคราวแก้ `class_catalog.py` หนึ่งบรรทัด commit แล้วรัน) → ได้ `[skipdrift] WARN` ชี้ 3 ไฟล์เทสที่ import ไฟล์นั้นตรง ถูกต้อง แล้วลบกิ่งทดสอบทิ้ง · รันเต็ม `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` บน diff ว่าง (server อยู่ที่ `main`) → `[skipdrift] PASS - no diff vs origin/main to check` ไม่ crash
- **เกินเวลาที่ `e1428` ให้ไว้ (30 นาทีสำหรับข้อนี้)** เพราะเลือกเขียน+ทดสอบโค้ดจริงแทนการรัน `--run` เฉยๆ — ตัดสินใจว่าคุ้มเพราะ `--run` เต็มจะเป็นภาระถาวรทุกรอบทุกสาย ไม่ใช่ครั้งเดียว
- **ยังไม่ทำ / ส่งต่อรอบถัดไปของ chief**: `RE_TO_BUILD_TICKET_AUDIT:` ค้างมาตั้งแต่ R354 (เกิน 6 ชม. ตามกฎ §7 มาก) — รอบนี้ไม่มีเวลาไล่ใบ RE ที่ปิดในช่วงนั้นทั้งหมด เขียนไว้ตรงนี้แทนการเงียบ ตามกฎ "เงียบ = ผิดกฎ"

## โทเคนตรวจตาม `e1428`
- `wc -c AGENTS.md` = 26087 ≤ 30720 ✅
- `git grep -n "lua_api/" AGENTS.md` = มี (บรรทัดเขต LANE-Q) ✅
- preflight รายงาน skip ที่รันจริงเป็นบรรทัดในผลของเกต: แถว `[skipdrift]` ใหม่ ✅ (advisory ตามที่ตัดสินใจไว้ข้างบน ไม่ใช่ RED)

## จดหมายที่บริโภครอบนี้
- `20260909_1452_COO-ORDER-e1428-one-document-round-for-agents-md-unless-1181-landed-first-LANE-E.md` (ADDRESSEE: LANE-E) — ทำครบตามสั่ง เขียนผลไว้ข้างบน
- `20260909_1416_LANE-GM-TO-CHIEF-preflight-cannot-see-a-flipped-skipIf.md` (ADDRESSEE: chief) — ตอบด้วยโค้ดข้อ 3 ข้างบน

## QUEUE_TRIAGE:
ไม่แตะ `GAME_TEST_QUEUE.md` รอบนี้ (ตามคำขอของผมเองใน `1428`, LANE-K รับ archive งานนี้ไปแล้วผ่าน `1452_COO-ORDER-e1428-...-LANE-K`) · triage ล่าสุดคือ R408 (13:52+07:00) ห่างจากตอนนี้ (15:26+07:00) ~1.5 ชม. ยังไม่ครบ 6 ชม. ไม่ต้องทำซ้ำรอบนี้
- **READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ**: เหมือน R408 ไม่เปลี่ยน — `GT-079` `GT-080` `GT-132` `GT-160` `GT-166` `GT-171` `GT-173` `GT-174` `GT-176` `GT-266` `GT-272` `GT-288` `GT-301` `GT-306`

## รอบหน้าทำอะไร
1. ถ้า `#1181` ยัง draft ตอนรอบเริ่ม: `RE_TO_BUILD_TICKET_AUDIT:` ที่ค้างมาตั้งแต่ R354 เป็นงานแรก (เกินกำหนด 6 ชม. มากแล้ว)
2. ถ้า `#1181` ลง `origin/main` แล้ว (เช็คด้วย `git merge-base --is-ancestor <sha> origin/main`): `login_entry` ใน `runtime.py` ตามคิว `1312`/`e1428` ข้อ 2 — ไม่ใช่รอบเอกสารอีกต่อไป
3. เดินตาม §17 ของ `CHIEF.md` ต่อ (WIRED line, PROMOTION_BACKLOG, housekeeping)

SCOREBOARD: NONE | ผู้เล่นไม่ได้อะไรใหม่รอบนี้ — งานเอกสาร/เครื่องมือที่ COO อนุมัติเต็มรอบล่วงหน้า (e1428) ไม่ใช่ src/ | `pf_bridge#1991`

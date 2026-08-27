# R157 — เปิดเลน AGGRO-001 สไลซ์แรก (pure logic + headless proof · ไม่แตะ runtime)

- session id: `el0w3q`
- เวลา (+07:00): เริ่ม 2026-08-24 ~23:5x · จบ 2026-08-25 ~00:4x
- รอบก่อนจบเมื่อไหร่: อ่านจาก `CHIEF_CONTINUATION.md` (R156 = exciting-goldberg-oyhrtl)
- branch: bridge `claude/exciting-goldberg-el0w3q` · code `claude/amazing-goodall-el0w3q`

## การ์ดกันรอบซ้อน (ทำก่อนอย่างอื่น)
- `git fetch --all` ทั้งสอง repo ✅
- ถาม GitHub API (MCP tool ไม่ใช่ `gh`): PR เปิดค้าง head `claude/*` ทั้งสอง repo = **ว่างทั้งคู่** (`[]`, `[]`)
- จับล็อก: empty commit `round claim: el0w3q` → push branch bridge → เปิด **draft PR #58**
  (`WIP round claim el0w3q` · body มี `PF-AUTOMERGE: v4`) ตั้งแต่วินาทีแรก ✅

## PROBE ต้นรอบ
1. **GitHub API/tool อ่านได้** ✅ — `list_pull_requests` ทั้งสอง repo คืน `[]` ปกติ · เปิด draft PR ได้จริง ⇒ ใช้เป็นทางหลัก
2. **ทาง D (`ci-status`) มีชีวิต** ✅ — `git fetch origin ci-status` + `git ls-tree origin/ci-status ci/` คืนรายการไฟล์ `d_exit=0`
- ไม่ล้มทั้งคู่ ⇒ ทำงานต่อได้

## โครงพี่น้อง + กล่องจดหมาย
- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅
- กล่องจดหมาย: **ไม่มีใบใหม่** — ทุก `.md` มี `.CONSUMED.txt` คู่แล้ว (ใบล่าสุด 2241 ถูก R156 บริโภคไปแล้ว)

## เหตุผลการเลือกงาน (backlog ตามหน้าที่ ⑤)
- คิว static (`CLIENT_RE_QUEUE.md`) = 0 ใบเปิด · ใบ attended ทั้งหมดรอตา/เครื่อง Panya
  (GT-063/GT-060 พร้อมบูตแล้วแต่ต้องมีคนหน้าเกม · GT-045/GT-034 นัดตา 2026-08-26)
- คำถามค้าง compose count>0 (R156) ยังรอ Panya เคาะ — stop_rule ใน ledger ห้ามเปิดเอง
- ⇒ ตามกติกา "ติดรอคำตอบ → ดึง milestone สำรอง (แถว not_started = pre-approved)"
  เลือก `mob_aggro_and_server_ai` (coverage domains[3].capabilities[8] · not_started)
- เหตุที่เดินได้แล้วทั้งที่ ROADMAP เขียนว่า "queue behind damage": เงื่อนไขจริงคือ "ต้องมีตัวเลข damage"
  ซึ่งปลดแล้วด้วย DAMAGE-ENCODER-001 (สูตรของเราเอง · Panya อนุมัติทาง 1 · GT-024 พิสูจน์ตัวเลขเรนเดอร์บนจอจริง)
- ขอบเขตสไลซ์แรก **จงใจแคบ**: pure logic library + headless tests + ledger/matrix/verifier เท่านั้น
  **ไม่แตะ runtime.py · ไม่เพิ่ม scenario · ไม่แตะ LANE_SETS · ไม่มี wire frame ใหม่**
  การต่อเข้า boot/scenario = สถาปัตยกรรมใหญ่กว่า ⇒ เขียนเป็นคำถามถึง Panya ก่อน

## เนื้องาน — MOB-AGGRO-001 (repo code · 3 ไฟล์)
ยึดตามร่างดีไซน์ของบ้านเอง `drafts/MOB_AGGRO_SERVER_AI_STATIC_AND_DESIGN_R98_20260820.md` §5
("all aggro intelligence must live on our server ... a tick loop selects the highest-threat
player in range") — R98 ออกแบบไว้แล้วแต่ยังไม่เคยสร้าง · Door A (hostility) มีเลน HYP-PF-027 แล้ว
· Door B (attack) ยังปิดตาย (ศูนย์ capture ศูนย์ encoder) · Door C (damage/death) พิสูจน์แล้ว

1. **NEW `src/pirateforce_foundation/mob_aggro.py`** — pure logic ตามแบบ `loot_roll.py`:
   - threat table ต่อ mob (abs ของ damage i32 จาก DAMAGE-MODEL-001 · saturate ที่ i32 max)
   - proximity floor = 1 เมื่อผู้เล่นมีชีวิตเข้ารัศมี aggro (ไม่สะสม)
   - เลือกเป้า: threat สูงสุดชนะ เสมอกันเอา identity ต่ำสุด · ประเมินใหม่ทุก tick
   - attack cadence นับเป็น tick (ไม่อ่านนาฬิกา) · ยิงเฉพาะในระยะ attack_range
   - leash แตก ⇒ ล้าง threat ทั้งหมด + RETURN จน กลับเข้า home_radius · ตายแล้ว absorbing
   - deterministic ล้วน (ไม่มี random แม้แต่ injected) · frozen dataclasses · fail-closed
     named refusals 9 ชื่อ · ระยะทาง 3D เทียบกำลังสอง ขอบเขต inclusive
   - **จุดซื่อสัตย์สำคัญ:** intent โจมตีชื่อ `INTENT_ATTACK_UNDELIVERABLE` และ
     `ATTACK_INTENT_DELIVERABLE = False` — เซิร์ฟเวอร์ "ตัดสินใจ" ได้ แต่ Door B ยังไม่มีทางส่ง
   - ค่า balance ไม่มี default สักตัว (สเกลพิกัดโลกยัง [UNKNOWN] — ผู้เรียกต้องเลือกเอง)
   - `production_allowed=False` · ไม่มี scenario · ไม่มีใครใน src/ import · ไม่มี ledger entry
     (precedent LOOT-ROLL-001: เลน pure-logic ไม่มี wire claim ไม่มี entry)
2. **NEW `tests/test_mob_aggro.py`** — 47 เทส / 18 subtests: refusal ครบชื่อ · ขอบเขตรัศมี
   inclusive/exclusive · 3D · cadence ทุกจังหวะ (รวม approach เดินหน้า counter) · leash/return/
   re-acquire · death absorbing · scripted fight 4 tick พินเป็น golden ASCII · containment
   (import allowlist AST · ไม่มี side effect ตอน import · ASCII+cp874 · ไม่ถูก import)
3. **EDIT `docs/FUNCTIONAL_COVERAGE.json`** — แก้ *เฉพาะ* `notes` ของแถว
   `mob_aggro_and_server_ai` · **status คง `not_started` ตามกติกา R98 บรรทัด 8-9**
   ("แถวขยับเมื่อ client จริงถูกเฝ้าดูเท่านั้น") ⇒ notes ไม่อยู่ใน GRADE_SUBSET_SHA256
   ⇒ **ไม่ต้อง re-pin**

บั๊กที่เจอระหว่างทาง: mob_aggro docstring เอ่ยชื่อไฟล์ npc_hostile_hypothesis ทำเทสพิน
"exactly two foundation modules mention the lane" แดง ⇒ แก้เป็นอ้าง HYP-PF-027 โดยไม่เอ่ยชื่อไฟล์

## รอบ pf-adversary (บังคับ) — 11 findings แก้ครบก่อน commit ทุกข้อ
- **D1 (MED · coverage notes):** "no frame exists for any intent" เป็นเท็จ — เฟรม movement ที่ client
  เรนเดอร์มีจริง (npc_locomotion/teleport = runtime_pass) ⇒ แก้เป็น "no intent is wired to an emitter"
  และประกาศตรง ๆ ว่า delivery ของ approach/leash คือเรื่องรอ ruling ไม่ใช่ขาดหลักฐาน
- **D2 (MED · claim ลอย):** "STATIC-ON-BRIDGE" ไม่มีใบจริงรองรับ ⇒ **เปิด RE-065
  ACTORTASK-USEBEHAVIOR-CTOR-WALK-001** ใน `CLIENT_RE_QUEUE.md` จริง (pf-queue-author เขียน ·
  ยืนยันเลข: 064 ออกซ้ำ RE-064/GT-064 ⇒ ว่างถัดไป 065) แล้ว notes อ้างใบนี้แทน
- **D3 (MED · Door A ล้าสมัย):** GT-043 วัดแล้วว่า red outline โผล่หลัง Tab-select เท่านั้น ⇒ docstring
  เติม refinement นี้ ห้ามอ่านว่าเฟรม hostility ทาสีแดงเอง
- **D4 (MED · fail-closed เท็จ):** string/bool หลุดเป็น bare ValueError · hp ไม่ validate (NaN hp = ไม่ตาย)
  ⇒ เพิ่ม `value_not_numeric`/`hp_not_int` + refuse โดยชื่อทุกทาง
- **D5 (MED · silent coercion):** radius จาก string · alive จาก string · identity ซ้ำเงียบ ๆ ⇒ เพิ่ม
  `alive_not_bool`/`duplicate_player_identity` refuse ครบ
- **D6 (MED-LOW):** damage ระหว่าง RETURN ถูกทิ้งเงียบ ⇒ ทำเป็น no-op ประกาศ (invariant: RETURN/DEAD
  ถือ threat ว่างเสมอ) + chosen reading ใหม่
- **D7 (MED-LOW):** ค่าบวก (ความหมาย UNKNOWN ตาม damage model) เคยกลายเป็น threat เต็ม ⇒ เปลี่ยนเป็น
  เฉพาะค่าลบเท่านั้นที่เพิ่ม threat (nonnegative = declared no-op)
- **D8 (LOW):** `MobAiState` ไม่ validate (rehydrate จาก DB หลุด) ⇒ เพิ่ม `__post_init__` เต็ม
  (`phase_unknown`/`state_malformed`)
- **D9 (LOW):** quote R98 แล้ว diverge เงียบ ⇒ เพิ่มท่อน "3 DELIBERATE divergences" (ไม่มี faction ·
  selection ไม่มี range bound — leash คือขอบเขตไล่ · ไม่มี Attack state แยก)
- **D10 (LOW):** doc cadence off-by-one ⇒ แก้เป็น "attack PERIOD: at most one per N ticks"
- **D11 (LOW):** Door C เหมารวม HYP-PF-026 เป็น attended ⇒ แยกชั้น headless/attended ให้ตรง report
- เพิ่มท่อน "THE DRIVER CONTRACT THIS MODULE ASSUMES" ตอบคำถามปิดท้ายของ adversary
  (dedup บังคับแล้ว · nonnegative บังคับแล้ว · flicker-free กับ tick duration เป็นภาระ driver — จดไว้)

## พิสูจน์ (cloud sanity — ไม่ใช่ gate เต็ม)
- `pytest tests/test_mob_aggro.py` ⇒ **55 passed / 32 subtests** เขียว(cloud sanity)
- `verify_hypothesis_ledger` ⇒ PASS entries=45 (ไม่แตะ ledger) · `verify_functional_coverage` ⇒ PASS domains=8
- สวีตเต็มหลังแก้ทุกอย่าง: **2280 passed / 324 skipped / 4478 subtests** เขียว(cloud sanity)
- บั๊กระหว่างทาง: docstring เอ่ยชื่อไฟล์ npc_hostile ชนเทสพิน "exactly two modules mention the lane"
  ⇒ แก้เป็นอ้าง HYP-PF-027 · สวีตเต็มรอบแรกจึงมีแดง 1 (2271/324/4464) ก่อนปิดจบเขียวหมด

## commit / PR
- repo code: commit `6d5eb7b` (3 ไฟล์ตามประกาศ · staged 3/3 · ไม่มี deletion) → push
  `claude/amazing-goodall-el0w3q` → **PR #27** (มี `PF-AUTOMERGE: v4`) — รอ gate · workflow merge เอง
- repo bridge: ไฟล์รอบนี้ + `CLIENT_RE_QUEUE.md` (RE-065 + status line) + จดหมาย
  `FROM_CHIEF_R157_TO_ATTENDED_20260825_0040.md` + ดัชนีท้าย `CHIEF_CONTINUATION.md` → push แล้วปลด
  draft PR #58 → แก้หัวข้อ/บอดี้ (ลำดับ ①②③ ตาม v5)

## คิวเทสเกม (⑤)
- **GT ใหม่: ไม่มี** — สไลซ์นี้ pure logic ไม่มีพฤติกรรม client-observable ให้เทส (ไม่มีเฟรมออก wire)
- **RE ใหม่: RE-065** (static · NEEDS-BRIDGE-IMAGE) — ctor walk ของ Door B ตาม draft R98 §7 ข้อ 1
- ไม่ลบ/ย้ายรายการที่ยังไม่ได้เทส

## คำถามค้างถึง Panya (ต่อจาก R156)
1. (เดิม R156 — ยังรอ) compose count>0 ของ HYP-PF-037: เปิด NEW VERSION เลย หรือรอผลตา GT-063?
2. (ใหม่ R157) เลน mob-aggro: อนุญาตให้ **wire intent ที่ส่งได้จริง** (approach/leash-return → เฟรม
   movement ที่ client เรนเดอร์อยู่แล้ว) เป็นเลนโค้ดรอบถัดไปไหม? — ผมถือว่านี่เกิน pre-approved pattern
   (ต่อ decision loop เข้า runtime = สถาปัตยกรรม) จึงไม่เริ่มเอง · ถ้าเคาะ จะเปิด HYP ใหม่ตาม pattern เต็ม

## nonclaims (ยกไปหัวไฟล์โค้ดด้วย)
- สูตร/ค่าคงที่ aggro ทั้งหมดเป็น **ของเราเอง** — เซิร์ฟเวอร์ต้นฉบับกู้ไม่ได้ตลอดกาล ไม่มี claim ว่าตรงต้นฉบับ
- ไม่มี claim พฤติกรรม client-observable ใด ๆ ในสไลซ์นี้ (ยังไม่มีเฟรมออก wire)
- "เขียว" ในไฟล์นี้ = cloud sanity เท่านั้น เว้นแต่ระบุเลข Actions run

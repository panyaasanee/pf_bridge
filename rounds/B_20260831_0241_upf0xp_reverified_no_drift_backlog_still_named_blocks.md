# LANE-B (COMBAT) รอบ `upf0xp` -- 2026-08-31T02:41+07:00

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้ไม่แตะ `src/` ในทั้งสอง repo -- ตรวจสดว่างานที่สั่งไว้ล่วงหน้า (world-wipe fix
สำหรับ `bar_frames`/`death_frames`) ถูกทำไปแล้วจริงในรอบก่อนหน้า (ยังผ่านเทสไม่ regress) และ
backlog ที่เหลือของสาย B ทุกจุดยังบล็อกด้วยเหตุผลที่มีคนตัดสินไปแล้ว ไม่มีจุดที่โค้ดใหม่ในเขตของ
สายนี้จะปลดเองได้โดยไม่ละเมิดกฎที่ตัดสินไว้ -- บอกตรง ๆ แทนการแต่งงานขึ้นมาทำ

## ต้นรอบ -- ตรวจสถานะสด ไม่เชื่อจดหมายเก่า

- `git fetch` ทั้งสอง repo: `pf_bridge` และ `pirate-force-server` local branch ของรอบนี้
  (`claude/wizardly-gauss-upf0xp`, `claude/tender-goldberg-upf0xp`) ตรงกับ `origin/main` เป๊ะ
  ณ ต้นรอบ (ไม่มี commit ค้าง ไม่ต้อง cherry-pick อะไรจากรอบก่อน)
- ตรวจ PR ปิดล่าสุดของสาย B ทั้งสอง repo ผ่าน GitHub API ตรง ๆ (ไม่ใช่เชื่อ `rounds/`):
  `pf_bridge#551` และ `pirate-force-server#343` ทั้งคู่ `merged=true` จริง -- งานรอบก่อนอยู่บน
  `main` แล้ว ไม่มีอะไรต้อง cherry-pick
- ไม่มี PR เปิดค้างของ `[LANE-B]` ในทั้งสอง repo ก่อนรอบนี้ (ตรวจด้วย
  `GET /repos/.../pulls?state=all` แล้วกรอง title -- เห็นแต่ PR ปิด/merged แล้วทั้งหมด)

## หมายเหตุเครื่องมือ

ไม่มี `mcp__github__*` tool จริงในชุดเครื่องมือของสาย B รอบนี้ (แม้ระบบจะโหลดคำแนะนำของ MCP server
มาให้) -- ใช้ `curl` ยิง GitHub REST API ตรงด้วย `$GITHUB_TOKEN` ที่ proxy ฉีดให้แทนตลอดทั้งรอบ
(list PRs, สร้าง PR, จะ mark ready ด้วยวิธีเดียวกัน) เช่นเดียวกัน **ไม่มี Agent/Task tool ให้เรียก
subagent `pf-adversary` ตรงในเซสชันนี้** -- ตรวจสอบเองแทน (self-review) ตามที่รอบก่อน ๆ ของสาย
นี้เจอปัญหาเดียวกันมาแล้ว (ดู `rounds/B_20260831_0147_n4vwrq_*.md` ข้อ ⑤) -- orchestrator เป็น
ผู้เรียก pf-adversary จริงหลัง push ถ้ามี

## ① งานสงวนของรอบก่อน (world-wipe: `bar_frames`/`death_frames` ต้องประกอบสำมะโนแบบเดียวกับ `arrival`)
## -- ยืนยันซ้ำอีกครั้ง: ยังอยู่ ไม่มี regression

`lane_hooks/` ยังอยู่บน `main` ของ `pirate-force-server` (`lane_a_choose_npc_scene14.py`,
`lane_a_scene_census.py`, `lane_gm_chat_command.py`, `lane_gm_run_command.py`) แต่ยังไม่มี
`lane_b_*.py` ตัวไหนเลย -- สาย B ยังไม่มีจุดที่ต้องใช้ `hook()`/`census_composer()` ของตัวเอง
รอบนี้ (ไม่มี combat-specific `fire()` point ใน `runtime.py` เลย -- grep
`lane_hooks\.(fire|scene_census_composer|scene_choose_npc_responder)\(` เจอแค่จุดของสาย GM/A)

รันเทสจริงซ้ำ: `tests/test_world_wipe_headless_proof.py` -- **7 passed, 2 subtests passed**
(เหมือนรอบ `n4vwrq` เป๊ะ ไม่มี regression) -- งานสงวนนี้ปิดแล้วจริง ไม่ใช่ของค้าง

## ② กล่องจดหมาย -- grep `ADDRESSEE: LANE-B` ทุกไฟล์ใน `notes_to_chief/`

ไม่มีใบไหนที่จ่าหน้าถึงสาย B (หรือ cc สาย B ในทางที่ต้องบริโภค) ที่ยังไม่มี `.CONSUMED.txt` คู่กัน
ใบเดียวที่ไม่มี stub คือ `20260831_0147_LANE-B-STATUS-addendum-2355-consumed-*.md` ซึ่ง
`ADDRESSEE:` ของมันเองคือ "LANE-B (self-consumption of a multi-lane letter)" -- เป็นบันทึกผลลัพธ์
ขาออกของสาย B เอง (รอบ `n4vwrq` บริโภคใบ 2355 แล้วเขียนรายงานนี้) ไม่ใช่ใบเข้าใหม่ที่ต้อง consume
ซ้ำ -- ไม่สร้าง stub ให้จดหมายของตัวเอง

ตรวจใบใหม่กว่ารอบ `n4vwrq` ด้วย (ไม่มี commit แตะ `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` ตั้งแต่
`2026-08-31T01:47+07:00` -- `git log --since` ยืนยันว่างเปล่า) และไล่อ่านทุกไฟล์ `notes_to_chief/`
ที่ประทับเวลาหลังจากนั้น: `FROM_CHIEF_R253_TO_ATTENDED_20260831_0224.md` (broadcast ทั่วไป --
`GT-128` ปลดล็อกบางส่วนแต่ยังไม่พร้อมบูต, `CORE-REQUEST-GM-042` ยังค้าง -- ไม่มีจุดของสาย B),
`20260831_0152_PANYA-ORDER-*BT_GM*` (สาย GM ล้วน), `20260831_0124_KA1A-FINDING-*lane-GM*`
(สาย GM ล้วน), `20260830_2356_PANYA-DECISION-one-addressee-per-letter-*` (นโยบายทั่วไป cc สาย B
เท่านั้น ไม่ใช่ ADDRESSEE -- เนื้อหาตรงกับกติกาที่คำสั่งของรอบนี้ให้มาอยู่แล้ว: จ่าหน้าเดียว, จองก่อน
เริ่ม, อายุใบจอง 90 นาที -- ไม่มีอะไรใหม่ที่ต้องเปลี่ยนวิธีทำงานของสาย B) -- ไม่มีใบไหนต้องเปิด
`.CONSUMED.txt` ใหม่รอบนี้

## ③ ไล่ backlog ของสาย B ทั้งหมดซ้ำ -- ตรวจสดทีละจุด ไม่ก็อปจดหมายเดิม

```
BUILD-004 (M3 สนามมีมอนสเตอร์)
  _SCENE_TABLE_MODULES = {bg0001, bg0002} เท่านั้น (field_mobs.py:475-478) -- LIVE default-on
  จริงสำหรับสองฉากนี้ (ไม่มีแฟล็ก, ใช้แถวจริงจาก MOBS ผ่าน field_mob_tables*.py)
  scene 14 (Bg0015): COO-DECISION 2026-08-26T12:46+07:00 ยังไม่ถูกยกเลิก -- ห้าม import
  จนกว่าสาย A จะผ่าน travel gate ที่สอง -- ไม่ใช่ของสาย B แก้

BUILD-005 (M4 ตีได้ ตายได้)
  mob_death.kill()      : runtime.py:4503 (WIRED, default-on, ไม่มีแฟล็ก)
  mob_loot.roll_drops() : runtime.py:4767 (WIRED)
  mob_census_wire_count : runtime.py:4457, :4742 (WIRED) -- world-wipe fix ยืนยันซ้ำแล้วข้อ ①
  ⇒ ยังคง LIVE จริง ไม่มีอะไรต้องทำเพิ่ม

BUILD-006 (M5 เก็บของได้)
  grep -c mob_pickup_persist runtime.py = 0 (ยังไม่มีจุดเสียบที่สาม)
  บล็อกจริง: GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 ยังเป็น PENDING (attended, หัวคิว) --
  grep ซ้ำ GAME_TEST_QUEUE.md:8200 ยืนยันสถานะเดิม ไม่มี opcode มาให้ต่อสาย
  ไม่มี combat-specific lane_hooks point ที่มีอยู่แล้วให้ผูกล่วงหน้า (ตรวจข้อ ①) --
  เขียนโค้ด "เผื่อ" opcode ที่ยังไม่เห็นจริงจะเป็นการแต่งงาน ไม่ใช่การต่อสายของจริง

RE-157 job 1/2 wiring (trade/combat membership guard -> runtime.py call site)
  predicate สร้างครบสองไฟล์แล้ว (`trade_session_membership.py`, `mob_combat_membership.py`)
  การต่อสายเข้า runtime.py เป็นการตัดสินใจของ chief ที่เลื่อนไว้แล้วสองรอบ (R246, R247:
  "ต้องอ่านครบ 5 commit site ของ world_census_* ก่อนถึงจะปลอดภัย") -- ไม่ใช่ของสาย B บังคับต่อเอง

mob_aggro M6
  RE-150 ปิด BOUNDED-NEGATIVE แล้ว ไม่มี aggro placement นอกบล็อกที่เจ้าของปฏิเสธแล้วในคลังข้อมูล
  ปัจจุบัน -- ไม่มีอาการใหม่ให้เริ่ม

GT-132/GT-149 (coalesced drop labels / label life)
  BOOTED, ANSWERED-DIFFERENTLY แล้ว -- ตัวบล็อกจริงคือ label_life ซึ่ง COO-DECISION 20260830_1742
  ยืนกฎเดิม "สาย B ไม่ต้องทำอะไรเพิ่มเรื่องนี้" จนกว่าจะมีรอบ attended วัดส่งซ้ำครั้งเดียว
```

สวีตเทสหลักของโมดูลคอมแบต (`mob_combat.py`, `mob_death.py`, `mob_ai_control.py`,
`field_mobs.py`) ตรวจ docstring เทียบจุดเรียกจริงใน `runtime.py` แล้วอีกครั้ง -- ไม่มีจุดไหนดริฟท์

## ④ ทำไมไม่มีโค้ดใหม่รอบนี้

ทุกจุดใน backlog ของสาย B ยืนยันซ้ำแล้วว่าบล็อกด้วยเหตุผลที่มีชื่อและมีคนตัดสินไปแล้ว (attended
test ที่ยังไม่บูต, COO-DECISION ที่ยังไม่ถูกยกเลิก, chief's call ที่เลื่อนไว้ หรือ corpus ที่ไม่มี
สัญญาณใหม่ให้เริ่ม) -- ไม่มีจุดไหนที่เขียนโค้ดในเขตของสาย B แล้วปลดได้เองโดยไม่ละเมิดกฎที่ตัดสินไว้
แล้ว รอบนี้เป็นรอบที่สองติดกัน (ต่อจาก `n4vwrq`) ที่ผลการตรวจสดออกมาเหมือนเดิม -- บันทึกไว้ตรง ๆ
แทนการแต่งอาการใหม่ขึ้นมาเขียนโค้ดให้มีอะไรทำ

## ⑤ pf-adversary

ไม่มี Agent/Task tool ให้เรียก subagent `pf-adversary` ตรงในเซสชันของสาย B รอบนี้ (เหมือนรอบ
`n4vwrq` ที่บันทึกปัญหาเดียวกันไว้แล้ว) -- ทำ self-review แทน: รันสวีตเต็มสองครั้ง (ก่อนเขียนไฟล์นี้
และตอนสรุปตัวเลขด้านล่าง ไม่มีการแก้ `src/` คั่นกลางจึงตัวเลขต้องตรงกัน), grep ซ้ำทุกเลขบรรทัด/
เลขไฟล์ที่อ้างในข้อ ①-③ แทนการเชื่อจดหมายเดิม, และ **ไม่อ้างว่าได้รันเช็ค cp874 ของไฟล์นี้จริง**
(ไฟล์นี้ใช้เลขวงกลม ①②③④⑤ ซึ่งไม่ใช่ cp874 -- อยู่นอกขอบเขตเกตที่มีอยู่ ตาม hard limit ของรอบนี้เอง
ที่บอกว่า `pf_bridge`/`notes_to_chief`/`rounds` ไม่ใช่ scope ที่ต้อง cp874-safe แต่ก็จะไม่เขียนคำอ้าง
เท็จว่า "ตรวจแล้วผ่าน" ซ้ำความผิดพลาดที่รอบ `n4vwrq` ต้องแก้ทีหลัง)

## ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ (pirate-force-server): 1
  - rounds/B_20260831_0241_upf0xp_CLAIM.md (ใหม่, force-added เหมือนไฟล์ CLAIM ก่อนหน้าทุกไฟล์
    เพราะ .gitignore deny-all ที่ root ไม่มี allowlist entry ให้ rounds/)

ไฟล์ที่แตะ (pf_bridge): 2 (นับเฉพาะรอบนี้ ไม่รวมไฟล์นี้เอง)
  - notes_to_chief/20260831_0241_LANE-B-STATUS-reverified-no-drift-round-upf0xp.md (ใหม่)
  - rounds/B_20260831_0241_upf0xp_reverified_no_drift_backlog_still_named_blocks.md (ไฟล์นี้, ใหม่)

สวีตเต็ม (pirate-force-server, ก่อนรอบนี้ = หลังรอบนี้ เพราะไม่แก้ src/):
  5608 passed, 323 skipped, 9729 subtests passed, 0 failed (192.80s)
  (มากกว่าตัวเลข 5600/9729 ที่รอบ n4vwrq บันทึกไว้ 8 ใบ -- เพิ่มจาก PR ของสาย A/GM ที่ merge เข้า
  main ระหว่างสองรอบนี้ ไม่ใช่ของสาย B)
tests/test_world_wipe_headless_proof.py + tests/test_tree_is_cp874_safe.py (รันรวม): 12 passed,
  407 subtests passed (7+2 กับ 5+405 ตามลำดับ)
```

## ยังไม่ได้พิสูจน์

- ว่า backlog ที่ตรวจว่า "บล็อก" รอบนี้จะยังบล็อกอยู่รอบหน้า -- ขึ้นกับผล `GT-146` ที่ยังไม่บูต
  (attended) และ COO-DECISION ใหม่ถ้ามี ไม่ใช่สิ่งที่รอบนี้ยืนยันได้
- ว่าเนื้อหาไฟล์ที่ใบ `20260830_2355_PANYA-ADDENDUM-*` เคยอ้าง (`adhoc_actorattr_probe/`,
  `PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md`) ตรงกับที่คิดไว้จริงหรือไม่ -- ไฟล์เหล่านี้
  ไม่อยู่ใน git clone นี้ (ตรวจซ้ำแล้วในรอบ `n4vwrq`, ยังไม่มีอะไรเปลี่ยน)

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `upf0xp`

# LANE-B round oabhhe-adv — 2026-09-06T07:25+07:00 start (continuation of round oabhhe)

## รอบนี้ขยับ NOW/M ข้อไหน
ไม่ขยับ NOW/M ใหม่ — เป็นการปิดของค้างจากรอบ `oabhhe` เอง ตาม `prompts/COMMON_LANE_ROUND.md`:
"ผล pf-adversary เพิ่งคืน/เจอของต้องแก้หลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก" — รอบนี้คือ
รอบถัดไปนั้น (ยังเป็นเซสชัน/กิ่งเดียวกับ `oabhhe` เพราะระบบให้กิ่งเดียวต่อเซสชัน ไม่ใช่ยึดของสายอื่น)

## ทำอะไรไปแล้ว
1. **แก้คอมเมนต์เท็จใน `field_mobs.py`** (`pirate-force-server#895`, commit `dba65a7`, ยังไม่ merge ตอน
   push): คอมเมนต์เดิมของรอบ `oabhhe` เขียนว่า Nina "does not reach a player's screen at all" —
   pf-adversary รันโค้ดจริงพบว่า **เท็จ**: `LANE_WITHHELD_PLACEMENTS` กรองเฉพาะผู้บริโภคของสาย B เอง
   (`load_roster`/AI register/combat ledger/hostile census override) · census ฐานของสาย A
   (`world_population_bg0008.py`/`world_bg0008_identity.py`) ไม่อ่านดิกนี้เลย ⇒ Nina ยังถูกส่งชื่อจริง/n_id
   จริง/avatar จริงไปยังไคลเอนต์ทุกเครื่องที่เข้าฉากนี้ — สิ่งที่ withhold ปิดจริงคือ "ตายไม่ได้" ไม่ใช่
   "มองไม่เห็น" แก้คอมเมนต์แล้วให้ตรงกับที่วัดได้ · เทสที่แตะไฟล์ (104 ผ่าน) รันซ้ำผ่านหมด ไม่มีเทสใด pin
   ข้อความเดิม
   🔴 **ไม่ใช่ช่องโหว่ใหม่**: พฤติกรรมเดียวกันมีกับ Carlos มาก่อนแล้ว (census ฐานไม่อ่านดิกนี้เหมือนกัน)
   เพิ่งวัดเจอเพราะรอบนี้เป็นรอบแรกที่ adversary รันเส้นทาง census จริง
2. **อัปเดต PR body ของ `#895`** ให้ตรงกับคอมเมนต์ที่แก้แล้ว + ใส่บรรทัด `TWO_SESSIONS_SAME_SCENE:` ที่
   ตอนแรกไฟล์รอบ `oabhhe` ลืมใส่ (ดูข้อ 3)
3. **เขียนใบถาม COO** (`20260906_0725_LANE-B-ASK-COO-bg0008-nina-visible-not-invisible-adversary-finding.md`):
   ถามว่า "unkillable แต่มองเห็น" เป็นขอบเขตที่ COO ตั้งใจให้จริงหรือไม่ (เจตนาเดิมอาจเป็น "อย่าเอาเนื้อหา
   ที่ไม่รู้จักไปอยู่ตรงหน้าผู้เล่น" ไม่ใช่แค่ห้ามฆ่า) — [สมมติของสาย B - รอ COO ยืนยัน] เอนไปทางตัวเลือก
   (ค) รอใบ RE/content "924+529 คืออะไร" ตอบก่อนค่อยตัดสินทั้งสองแกนพร้อมกัน เพราะไม่บล็อกผู้เล่นวันนี้
   (P-2/GT ยังปิดอยู่ดี) แต่ไม่ใช่คนตัดสินเอง ส่งคำถามแล้วเดินต่อ ไม่รอ
4. **`TWO_SESSIONS_SAME_SCENE`** ของรอบ `oabhhe` (bg0008 registration) ที่หายไปจากไฟล์รอบเดิม บันทึกไว้ที่นี่
   แทน: **ถูก** — `HOSTILE_PLACEMENTS` เป็นข้อมูลระดับโมดูล (process-wide) เหมือนทุกฉากก่อนหน้า ไม่ใช่ต่อ
   session/connection · `DeathRegister` (ไม่แตะรอบนี้หรือรอบก่อน) คีย์ด้วย `(scene, actor_identity)` พร้อม
   compare-and-swap อยู่แล้ว ⇒ สองเซสชัน/รีล็อกอินในฉากเดียวกันเห็น roster และการตายชุดเดียวกัน
   pf-adversary ยืนยันด้วยการรันโค้ดจริง ไม่พบการละเมิดกฎ shared-world/delta ในโค้ดของรอบ `oabhhe` เอง —
   ช่องว่างที่แท้จริงคือ **เอกสาร** (ไฟล์รอบไม่มีบรรทัดนี้) ไม่ใช่ตัวโค้ด

5. 🔴 **`#895` โดน reaper ปิดจริงระหว่างรอบนี้ — gate RED ที่ `skip_census`**: commit `5ee6b850`
   (ก่อนแก้คอมเมนต์) แดงที่ Windows gate ด้วยเหตุคนละเรื่องกับที่ pf-adversary เจอ:
   `tests/test_field_mob_tables_bg0008.py` ใหม่มีเทสที่ skip บน precondition `bridge_gamedata`
   ในโคลนสดที่ไม่มี `pf_bridge` ข้าง ๆ (Windows gate) — รอบ `oabhhe` **ไม่ได้เติม pin ให้**
   `docs/PYTEST_SKIP_PINS.json` ทั้งที่ `AGENTS.md` §7 สั่งไว้ตรง ๆ อยู่แล้วว่า "เพิ่มไฟล์เทสใหม่ที่มี skip
   ⇒ ซ้อม skip_census ในสภาพไม่มี pf_bridge ข้างๆ" — sandbox ที่ build โมดูลนี้มี `pf_bridge` เป็น sibling
   เสมอ เทสนี้จึงไม่เคย skip ตอน build เลย ไม่มีใครเห็นช่องว่าง จนกระทั่ง gate จริงรันจากโคลนสด
   reaper ปิด `#895` อัตโนมัติตามกฎ (`.github/workflows/merge-claude-pr.yml`) — **กิ่งไม่หาย** คอมมิตยังอยู่
   บน `claude/gifted-clarke-oabhhe` ตามที่ reaper บอก
   **แก้แล้ว**: เพิ่ม entry `bridge_gamedata`/`tests/test_field_mob_tables_bg0008.py`/count 1 ใน
   `docs/PYTEST_SKIP_PINS.json` (commit `88fab41`) · **พิสูจน์ด้วย `git worktree add --detach` ไปที่
   `/tmp` (ไม่มี `pf_bridge` เป็น sibling จริง จำลองสภาพ gate ได้ตรง)**: ก่อนแก้ `pf_pytest_precondition_
   census.py` รายงาน `UNPINNED` ตรงกับที่ gate เจอเป๊ะ หลังแก้ `RESULT: PASS` · full suite รอบสองบน merged
   tree: **11935 passed, 365 skipped, 0 failed, 23426 subtests** (559s) · `pf_gate_preflight.py` PASS เต็ม
   ทุกข้อ · ลบ worktree ทิ้งเรียบร้อยแล้ว (`git worktree remove --force` + `prune`)
   **เปิดใบใหม่ `pirate-force-server#899`** แทน `#895` ที่ปิดไปแล้ว (กิ่งเดิม คอมมิตเดิม + คอมมิตแก้ pin)
   ไม่ draft มี `PF-AUTOMERGE: v4` ยืนยันแล้ว

## บทเรียน (ตัวเองทำผิดกฎที่มีอยู่แล้ว ไม่ใช่กฎใหม่)
รอบ `oabhhe` ควรซ้อม skip_census ในสภาพไม่มี `pf_bridge` ข้างๆ **ก่อน push ครั้งแรก** ตามที่ `AGENTS.md` §7
สั่งไว้อยู่แล้ว แต่ไม่ได้ทำ — เพิ่งมาซ้อมตอนรอบนี้หลังจาก gate จับได้เอง ผลคือเสียรอบ reaper ไปหนึ่งใบ (`#895`)
ไม่ใช่ช่องโหว่ของกฎ เป็นการไม่ทำตามกฎที่มีอยู่แล้วของรอบก่อน บันทึกไว้เตือนตัวเอง/สายอื่นที่เพิ่มไฟล์เทสใหม่

## ผลตรวจของ pf-adversary ที่ไม่ต้องแก้ (บันทึกไว้เฉย ๆ)
- คอมเมนต์เก่าใน `tests/test_mob_ai_control.py:234-235` ("Bg0015 is not in `_SCENE_TABLE_MODULES`") ยืนยัน
  ว่าเท็จจริง (Bg0015 อยู่ในดิกนั้นมาหลายรอบแล้ว) แต่ **ยืนยันว่ามีอยู่ก่อนรอบ `oabhhe`แล้ว** (เช็ค
  `git show origin/main:tests/test_mob_ai_control.py` ตรง) ไม่ใช่ของรอบนี้/รอบก่อนทำเสีย — ปล่อยให้รอบที่
  แตะไฟล์นั้นจริงเป็นคนแก้
- ข้อสงสัยเรื่อง `mob_scene_recompose.py` บรรทัด ~365-395 มีของเก่าค้าง scene-8 — pf-adversary เช็คแล้ว
  **ไม่จริง** ที่ HEAD (บรรทัดนั้นพูดถึงฉาก 14 ไม่ใช่ฉาก 8) ถอนข้อสงสัยนี้จากไฟล์รอบ `oabhhe`

## สิ่งที่ยังไม่ปิด
- ใบถาม `0725` รอ COO เคาะ (ทางเลือก ก/ข/ค) — ไม่บล็อกผู้เล่นวันนี้
- `pirate-force-server#899` ยังไม่ merge ตอนปิดรอบนี้ (ห้ามเขียนว่าอยู่บน main จนกว่ารอบถัดไปยืนยันด้วย
  `git merge-base --is-ancestor`) · gate ยังไม่รันจริงบน `#899` ตอนปิดรอบนี้ (แค่ preflight local เขียว)

## รอบหน้าทำอะไร
1. เช็ค gate ของ `#899` จริง (ไม่ใช่แค่ preflight local) ก่อนเชื่อว่าผ่าน — ถ้าแดงอีกด้วยเหตุอื่น อ่านล็อก
   ก่อนเดา (`mcp__github__get_job_logs`)
2. เช็คว่า COO ตอบใบ `0725` หรือยัง — ถ้าตอบ (ข) ต้องเพิ่มโค้ดให้ census ฐานของสาย A อ่าน
   `LANE_WITHHELD_PLACEMENTS`/`LANE_WITHHELD_REASON` ด้วย (งานข้ามสาย ต้องคุยกับ A ก่อนแตะ `world_*`)
3. เช็คว่า `#899` merge แล้วหรือยัง ด้วย `git merge-base --is-ancestor` ก่อนเขียนว่า "อยู่บน main"
4. งานหลักเดิม: ต่อจดหมาย `0659` (five-scene recon ค้าง bg0009/bg0010)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรวันนี้ (P-2/GT ยังปิดเหมือนเดิม) แต่โค้ดที่ทำให้มอน 6 ตัวใน
Silver Harbour ตายได้จริงถึง PR แล้วรอบสอง หลังแก้ทั้งคอมเมนต์เท็จ (pf-adversary) และ pin ที่หายไป
(Windows gate) ที่ทำให้ใบแรกโดนปิด | `pirate-force-server#899` commit `88fab41`

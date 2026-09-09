# LANE-Q รอบ `6gc0zk` -- `Player.AddItem` ออกจาก stub table จริง + จ่ายกล่องจดหมาย 1 ใบ

เริ่ม 2026-09-09T16:39+07:00 · claim `pf_bridge#2000`
นาฬิกา: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด 16:36:02 · เช็คตอน 16:48 ⇒ ห่าง ~12 นาที (< 60) -- ไม่ค้าง

`TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว -- ของที่รอบนี้แตะเป็นแถวกระเป๋าต่อตัวละคร (ผ่านประตูของ DB ที่มีอยู่แล้ว
`commit_acquired_backpack_item`) + เอกสาร/จดหมาย ล้วนไม่มี state ต่อฉาก ไม่มี world registry ไม่มี combat state

`ADVERSARY_UNAVAILABLE claude/hopeful-hopper-6gc0zk` -- ค้น ToolSearch สำหรับ Agent/Task subagent
`pf-adversary` แล้วไม่พบเครื่องมือนั้นในเซสชันนี้ตั้งแต่ต้นรอบ (คำค้น "Agent subagent pf-adversary" และ "Task
subagent_type launch agent" ทั้งคู่คืนเฉพาะ SendMessage/EnterWorktree/SearchPlugins/TaskStop/subscribe_pr_activity
ไม่มี pf-adversary) -- ทำ self-review เต็มแทน (อ่านทุก hunk ใน `git diff --cached` ก่อน commit แต่ละครั้ง ดูข้อ 3)
รอบหน้าของสายนี้สั่ง `pf-adversary` บนกิ่งนี้เป็นงานแรกตามกฎ (เหมือนกรณี PENDING)

## 0. ล็อกรอบ

list PR `pf_bridge` open ก่อนเปิด (16:36): ไม่มีใบหัว `[LANE-Q] round <id>: claim` ⇒ ว่าง เปิด `#2000`
เปิดแล้ว list ซ้ำทันที (16:39): เป็น `[LANE-Q]` ใบเดียวที่เป็น claim และใหม่สุด ⇒ ไม่มีใครแก่กว่าให้ยอม

## 1. รอบนี้ขยับ NOW/M ข้อไหน

- **บันได M**: ไม่ขยับ (M2 ยังเป็นของ LANE-A) -- งานรอบนี้เป็นคิวที่รอบก่อน (`7mdavp`) วางไว้เป็นงานแรกของรอบหน้า
  (ข้อ 3 ในไฟล์รอบนั้น: q1351/q2226) ไม่ใช่รายการ M โดยตรง
- **NOW บรรทัด Q**: `1452` ("`lua_api/` = Q · จ่าย/หักต้องเข้า ledger") -- รอบนี้ทำครึ่งแรก (จ่าย `Player.AddItem`
  จริง) ครึ่งหลัง (ต่อเข้า `RefusalLedger` โดยตรง) เขียนเป็นสมมติ + ใบถาม COO แทน (ข้อ 5)
- **จดหมายที่บริโภครอบนี้**: 1 ใบ (`20260909_1450_LANE-DB-TO-LANE-Q-item-minter...`) -- สแกนด้วย
  `grep -l "ADDRESSEE: LANE-Q\b" notes_to_chief/*.md` แล้วกรองใบไม่มี stub เจอใบเดียว (รอบก่อนเคลียร์ backlog
  13 ใบไปหมดแล้ว)

## 2. งานหลัก -- `Player.AddItem` (1430 จุดเรียก, มากที่สุดในบรรดา `Player.*` ที่ยัง stub) ออกจาก `STILL_STUBBED`

**เหตุ**: จดหมาย `20260909_1450` จาก DB ยืนยัน `store.mint_backpack_item(sid, character_id, item_id, quantity,
category)` ลงจริงบน `main` แล้ว (ตอบ `COO-DECISION 20260908_2055`) -- ประตูที่ `Player.AddItem` รออยู่มาถึงแล้ว
และ `COO-DECISION 20260909_1452`/`20260909_1312` ยืนยันเขตของ Q ครอบ `lua_api/` ทั้งหมดรวม `player.py`

**ทำ**:
- `lua_api/reward.py`: เพิ่มประตูที่ห้า `mint()` (คู่กับ `pay`/`grant`/`charge` เดิม) -- ไม่เคย raise เมื่อปฏิเสธ
  ไม่เคยมินต์แถวเอง refusal set ปิด (`MINT_REFUSALS`) หา category จาก `gm.item_catalog.item_category(item_id)`
  เอง (สคริปต์เรียก `Player.AddItem(item_id, quantity)` arity 2 จริงจากคอร์ปัส ไม่มีอาร์กิวเมนต์ category ให้)
  id ที่ชนกันข้ามตาราง (misc/consumable/quest มีเป็นร้อย ตามดอกสตริงของ `item_catalog` เอง) ⇒ ปฏิเสธชื่อ
  `ambiguous_item_category` ไม่เดา (ขีดจำกัดรูปแบบข้อมูลจริง ไม่ใช่เพดานที่ตั้งเอง -- เข้าข้อยกเว้นของ `2220`)
- `lua_api/player.py`: จุดเรียก `Player.AddItem` จริง เรียก `_reward.mint(...)` · ย้ายชื่อเข้า `REAL_METHODS`
  ออกจาก `STILL_STUBBED` · เพิ่มฟิลด์ `sid` ให้ `PlayerContext` (ค่าเริ่มต้น `""` ⇒ ปฏิเสธ `no_session`) เพราะ
  `mint_backpack_item` ต้องมี session id พิสูจน์ความเป็นเจ้าของตัวละคร ซึ่ง `character_id` เดี่ยว ๆ ไม่พอ
- **เทสสองทางที่ COO รับ (`20260909_1312`)**: store ที่ **มี** `mint_backpack_item` ⇒ จุดเรียกเรียกมันจริงด้วย
  อาร์กิวเมนต์ที่ตกลงกัน (spy พิสูจน์ ไม่ใช่แค่ mock ผ่าน) · store ที่ **ไม่มี** ⇒ ปฏิเสธโดยชื่อเป๊ะ
  `no-item-minter` และ**ไม่มินต์เอง** -- ปักที่ `lua_api.reward.mint` ตรง ๆ (`MintTests`) และซ้ำที่จุดเรียก
  `Player.AddItem` (`AddItemClosureTests`) + เทสทั่วรีโปที่ตายทันทีถ้าไฟล์ใน `lua_api/` เขียนสคีมากระเป๋าเอง
  (`NoSelfMintedBagSchemaTests`, grep `INSERT INTO character_backpack*`/`UPDATE character_backpack*`)

## 3. สิ่งที่วัดได้ระหว่างทาง -- คำกล่าวอ้างเก่าของไฟล์นี้เองผิด

`docs/SCRIPT_LANE.md`/`test_script_lua_quest_rewards.py`'s module docstring เคยเขียนไว้ (2 รอบก่อน) ว่า "พอ
`Player.AddItem` เป็นของจริง กลุ่มธุรกรรมจะเปิดเอง" -- **วัดแล้วรอบนี้: ผิด** กลไก group gate ที่มีอยู่แล้ว
(`COO-DECISION 20260908_0242`, D2 ของรอบ `ad7t6n`) รอสมาชิกฝั่ง give **ทุกตัว** ไม่ใช่แค่ `Player.AddItem`:
`Q_CLASS.Report_Run` มี 5 สมาชิก (`Player.AddItem` + `Player.AddPpClass` + `Quest.AddCriteriaCash/Exp/
SkillPoint`) -- 4 ตัวหลังยังเป็น stub ⇒ กลุ่มยังถูกปฏิเสธทั้งกลุ่มเหมือนเดิม (ไม่มีการเก็บ 15000 แล้วไม่ได้ของ) --
**นี่เป็นผลบวก**: ระบบที่สร้างไว้ตั้งแต่ก่อนหน้านี้ (สำหรับป้องกันบั๊กชนิดนี้โดยเฉพาะ) ทำงานถูกตามที่ออกแบบไว้
ปรับ 5 เทสที่เคยสมมติว่า `AddItem` เป็น stub ตัวเดียวของกลุ่ม (2 ใบใช้มันเป็นตัวอย่าง stub เฉย ๆ สลับเป็น
`Player.RemoveItem`/`Player.AddPpClass` แทน ยังเป็น stub จริง · 3 ใบปักชื่อ `blocked_on=` ตรงตัว ปรับเป็นชื่อที่
บล็อกจริงตอนนี้) -- ไม่มีใบไหนถูกทำให้อ่อนลง ปรับตามความจริงที่วัดใหม่ทั้งหมด

## 4. ใบที่บริโภครอบนี้

| ใบ | สถานะ |
|---|---|
| `20260909_1450_LANE-DB-TO-LANE-Q-item-minter...` | **ทำแล้วรอบนี้** -- ข้อ 2 (ปักชื่อ/ลายเซ็นตามที่ DB เสนอ ไม่เปลี่ยน ตามที่ดอกสตริงของ `store.py` บอกว่า Q เป็นคนปัก) |

stub + สำเนา `consumed/` วางแล้ว (คู่เดียว) -- ไม่ลบต้นฉบับ

## 5. สมมติที่เลือกไปแล้ว ไม่รอ

`[สมมติของสาย LANE-Q - รอ COO ยืนยัน]` ใบ `q1351` ข้อ 2 สั่งให้ `RefusalLedger`/`unreadable_reason` "เห็น" จุดจ่าย
`Player.AddItem` -- รอบนี้**ไม่ได้**ต่อ `reward.mint`'s refusal เข้า `quest_state_signal.RefusalLedger`'s
object model ตรง ๆ เพราะกลไกที่ป้องกันเจตนาเดียวกัน (จ่ายทั้งที่ส่งของไม่ได้) มีอยู่แล้วคนละชั้น (group gate ข้อ 3
ข้างบน) และ `RefusalLedger` เองติดตามแถวสถานะเควส (flag/counter) ไม่ใช่แถวกระเป๋า -- เขียนใบถาม COO
(`notes_to_chief/20260909_1650_LANE-Q-ASK-COO-q1351-ledger-vs-group-gate-covering-additem.md`)
พร้อมทางย้อนถ้า COO ต้องการให้ต่อจริง แล้วเดินหน้าต่อ

## 6. เขตที่จงใจไม่แตะ

`store.py`/`migrations/`/`runtime.py`/`app.py`/`v141`/registry ของ A/combat state ของ B · `Player.RemoveItem`/
`Quest.RewardItemSelect` (ยัง stub -- ไม่มีประตูหักของ DB ให้ `RemoveItem` และ `RewardItemSelect` ยังขาด
per-character reward-choice state) · D3/D5 (คำถามใหญ่ของ addendum `z113cx`) · D2/D1 ที่ค้างมาสองรอบ -- เวลารอบนี้
หมดไปกับฟีเจอร์เดียว (`Player.AddItem`) ที่มีผลกระทบกว้าง (ต้องแก้เทส 3 ไฟล์ที่สมมติผิด) ไม่ใช่ขี้เกียจ เขียนไว้ตรง ๆ

**พบแต่ไม่ได้แก้**: `pf_bridge#1951` ([LANE-Q] round 7cf5ak addendum) เปิดค้างไม่มี marker มาตั้งแต่ 8 ก.ย.
เนื้อหา (ledger unit เดิม) ถูกสร้างใหม่ทับไปแล้วโดยรอบ `z113cx`/`yd9u99`/`7mdavp` -- ไม่มีเวลารอบนี้ตรวจให้แน่ใจ
100% ว่า superseded สนิทก่อนเติม marker (การเติม marker ผิดใบทำให้ reaper ปิดของที่ยังไม่จบ) ทิ้งไว้ให้รอบหน้า

## 7. หลักฐาน

- เทสเฉพาะจุด (`PYTHONPATH=src pytest tests/test_script_lua_api_player.py tests/test_script_lua_api_reward.py
  tests/test_script_lua_quest_rewards.py tests/test_script_lua_quest_vars.py tests/test_script_lua_api_quest.py
  tests/test_script_lua_corpus.py`): 298 passed, 46 skipped (lupa ไม่มีในแซนด์บ็อกซ์นี้), 233 subtests passed
- เทสทั้งกลุ่ม `test_script_lua_*.py` (649 ไฟล์เทสในสคริปต์เลนทั้งหมด): 649 passed, 80 skipped, 8417 subtests
  passed
- **ชุดเต็ม (`PYTHONPATH=src pytest tests/`) บนกิ่งของรอบนี้ หลัง merge origin/main แล้ว**: **15781 passed, 446
  skipped, 0 failed, 43488 subtests passed** ใน 1109.00s (0:18:29) -- เขียว ยืนยันก่อน push จริง (แซนด์บ็อกซ์นี้
  ช้ากว่าที่รอบก่อนบันทึกไว้บนสะพาน ~720s มาก แต่ไม่มี fail สักตัว)
- `tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PASS** ทุกแถว (cp874/skips/mainmerge/
  census/branch/bridgesize/queuegrowth/filenamelen/scoreboard-manual/claudecfg/consumedstub/modebits) · มีแค่
  `[skipdrift] WARN` (advisory ไม่ใช่แดง) ชี้ 5 ไฟล์เทสที่ import โมดูลที่กิ่งนี้แก้ -- สั่ง
  `tools/pf_pytest_precondition_census.py --run` ตามคำแนะนำแล้วพบว่ามันรันชุดเต็มซ้ำอีกรอบ (~18 นาทีเท่ากัน) จึงหยุด
  เพราะซ้ำกับชุดเต็มข้างบนที่เขียวแล้วบนต้นไม้เดียวกัน ไม่ใช่การข้ามเพราะขี้เกียจ
- `git merge-base --is-ancestor 2e284962 origin/main` (pirate-force-server, ก่อน merge origin/main เข้ากิ่งนี้):
  true -- ยืนยันว่ากิ่งเริ่มจาก main ปัจจุบันจริง ไม่ใช่ฐานเก่า

## 8. สถานะที่ส่งมอบ

- `pirate-force-server` กิ่ง `claude/hopeful-hopper-6gc0zk` (`e159b75c` ฟีเจอร์ · `bc079b1e` เอกสาร · merge
  origin/main รวมอยู่แล้ว) -- **เปิด PR แล้ว: `pirate-force-server#1201`** ไม่ draft มี `PF-AUTOMERGE: v4`
  ยืนยันด้วย GET แล้ว (state=open, draft=false, body มี marker บรรทัดของมันเอง) -- **ห้ามอ้างว่า "เสร็จ/landed/อยู่
  บน main"** จนกว่ารอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`
- `pf_bridge#2000` = claim ของรอบนี้ -- ปลดล็อกหลังไฟล์นี้ + จดหมาย/stub ลงกิ่งแล้ว (ขั้นสุดท้ายของไฟล์นี้)

## รอบหน้าทำอะไร (เรียงแล้ว)

1. 🔴 **สั่ง `pf-adversary` บนกิ่ง `claude/hopeful-hopper-6gc0zk` เป็นงานแรก** ก่อน claim งานใหม่ (`ADVERSARY_UNAVAILABLE`
   รอบนี้ -- เครื่องมือไม่มีในเซสชัน ไม่ใช่ผลที่คืนมา)
2. **ตรวจ `pf_bridge#1951`** (LANE-Q round 7cf5ak addendum ค้างไม่มี marker) ว่า superseded สนิทจริงหรือไม่ ก่อน
   เติม marker หรือทิ้งไว้ต่อพร้อมเหตุผล
3. **q1351 ต่อจริงหรือไม่**: รอผล COO ต่อใบ `20260909_1650_...` -- ถ้า COO สั่งให้ต่อ `reward.mint` เข้า
   `RefusalLedger` จริง ทำเป็นงานแรก ๆ ถ้าไม่ตอบใน 1 ชม. ตามกฎเดิน (`เขียนคำถาม แล้วเดินต่อ`) ถือว่าสมมติยืน
4. **`Player.RemoveItem`/`Quest.RewardItemSelect`**: ยังรอประตูหักของ DB (`RemoveItem`) และ per-character
   reward-choice state (`RewardItemSelect`) -- เขียนจดหมายขอถ้ายังไม่มีคิวของ DB สำหรับสองอย่างนี้
5. **D3+D5** (คำถามใหญ่ของ addendum `z113cx`) -- ค้างมาสามรอบแล้ว (`yd9u99`/`7mdavp`/รอบนี้) อย่าให้ตกรอบที่สี่
6. **D2 ทางเต็ม**/**D1** (carry-over จาก `l8ayrt` ผ่านหลายรอบ)
7. หลังจากนี้: `Player.*` ตัวถัดไปตามจำนวนจุดเรียก (`AddAndEquip` 48, หรือกลุ่ม `_STAT_GRANT`/`_STAT_READ` ที่ยังไม่มี
   ประตู DB -- เช็คจดหมายจาก DB ก่อนเลือก)

SCOREBOARD: COMING | ผู้เล่นที่รับเควสที่ให้รางวัลไอเทมเดี่ยว ๆ (ไม่อยู่ในกลุ่มธุรกรรมที่ยังพร่องสมาชิกอื่น) จะได้ไอเทมจริงเข้ากระเป๋าเมื่อสคริปต์เรียก `Player.AddItem` แทนที่จะเป็น no-op เงียบ ๆ เหมือนเมื่อวาน (โค้ดถึงกิ่งแล้ว รอ PR เปิด/รอเกต) -- เควสรวมที่มีกลุ่มธุรกรรมหลายสมาชิก (เช่น q_class.lua) ยังไม่เปลี่ยนพฤติกรรมเพราะกลุ่มยังพร่องสมาชิกอื่นอยู่ (วัดและบันทึกไว้ตรง ๆ ในข้อ 3) | pirate-force-server claude/hopeful-hopper-6gc0zk (e159b75c ฟีเจอร์ + bc079b1e เอกสาร) + pf_bridge#2000

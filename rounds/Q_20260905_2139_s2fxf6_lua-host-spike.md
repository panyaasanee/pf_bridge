# LANE-Q round `s2fxf6` — 2026-09-05T21:35+07:00 ถึง 21:5x+07:00 (รอบแรกของสาย)

## ล็อกรอบ
- list PR `[LANE-Q]` ทั้งสองรีโปก่อนเริ่ม: **ไม่มีใบเปิดค้างเลย** — `pirate-force-server` open = `#850`(GM) `#846`(UI) `#794`(E) · `pf_bridge` open = `#1373`(B) `#1372`(A) `#1370`(UI) `#1336`(courier) ทั้งหมดเป็นของสายอื่น ไม่ใช่ล็อกของเรา
- mailbox `grep -l "ADDRESSEE: LANE-Q"`: **`20260905_2055_COO-DECISION-...-LANE-Q.md` หนึ่งใบ ไม่มี `.CONSUMED.txt` คู่** ⇒ บริโภครอบนี้ (stub วางแล้ว) · ใบ `2056`/`2057`/`2058` จ่าหน้าถึง A/B/DB ไม่ใช่ถึงเรา (สั่งให้เขาประกาศ interface ให้เรา) — อ่านแล้ว ยังไม่มี interface ตอบกลับมาบน main จึงยังไม่มีอะไรให้ต่อรอบนี้
- ตรวจตามคำสั่งใน `2055`: **ไม่มี `rounds/E_*` ที่เป็น Lua spike และไม่มี `docs/SCRIPT_LANE.md` ของ chief บน main** (`git ls-tree -r origin/main | grep -E "SCRIPT_LANE|script_|lua_api"` = 0 hit) ⇒ **spike เป็นของเรา** ตามกติกา "ใครถึงก่อนเป็นเจ้าของ" · แจ้ง chief หนึ่งบรรทัด: LANE-Q ทำ spike แล้ว chief เลิกทำได้
- claim PR `pf_bridge#1379` เปิดโดยไม่มีสตริง automerge marker ตั้งแต่เปิด (ผ่าน `pf_gate_preflight.py --pr-body ... --pr-stage claim` = PASS) → list ซ้ำ ไม่มีใบ `[LANE-Q]` อื่นเก่ากว่า → ไม่ต้อง yield

## รอบนี้ขยับ NOW/M ข้อไหน
**ขยับ**: บันไดไมล์สโตนบรรทัด "ทีม 8 สาย" ระบุ LANE-Q = `Lua host 616 สคริปต์ · 0/160 API · คิว: spike → Trigger.* 17 (ปลด M2) → Quest.* 25 → Player.* 73` — รอบนี้ปิด **ข้อ spike ทั้งข้อ** ตาม charter ข้อ 1 และตาม `COO-DECISION 2055` ข้อ 1
**ยังไม่ขยับ**: M2 เอง (ตัวบล็อกคือ `SAILING_RESULT` ของ LANE-A) — ชั้น `Trigger.*` 17 ตัวที่จะต่อจาก A คือคิวข้อ 2 ของเรา รอบหน้า

## ลำดับตาม §7
ไม่แตะ canonical DB · ไม่แตะ `GAME_TEST_QUEUE.md`/`CHIEF_CONTINUATION.md` · ไม่ลบไฟล์ใดใน `pf_bridge` · ไม่แตะ `v141` · ไม่แตะ `runtime.py`/`app.py`/`store.py` (ยังไม่มีจุดเสียบ — เป็น CORE-REQUEST รอบหลัง) · ไม่ตั้งชื่อสาขาเอง (`claude/kind-albattani-s2fxf6` · `claude/hopeful-hopper-s2fxf6` ที่ระบบให้) · ไม่ใช้ `rm` แฟล็ก `-r` สะกดใดเลยทั้งรอบ (worktree ใช้ `mktemp -d` ตาม `PROCESS_GATES.md` §26 · ไม่เก็บกวาด) · ทุกอย่างที่ลงรีโปเซิร์ฟเวอร์และ commit message เป็น ASCII ล้วน (ตรวจแล้ว `docs/SCRIPT_LANE.md` decode ascii ผ่าน) · stage ทีละไฟล์ ไม่มี `git add -A` ทั้งรอบ

## งานหลัก — Spike (charter ข้อ 1) เสร็จทั้งข้อ
สร้างในรีโปเซิร์ฟเวอร์ (กิ่ง `claude/hopeful-hopper-s2fxf6` · 4 คอมมิต `529c59b`, `1a11d13`, `bf476ad`, `d97bb06`):
1. **`src/pirateforce_foundation/script_host.py`** — Lua host แบบ sandbox: `ScriptHost` = หนึ่ง `lupa.LuaRuntime` ต่อหนึ่งสคริปต์ (เหตุผลในหัวไฟล์: 616 ไฟล์ใช้ชื่อ entry point ซ้ำกัน `ScriptStart`/`Accept_Check`/`Report_Run` — state เดียวร่วมกันแปลว่าไฟล์ท้าย ๆ ทับฟังก์ชันของไฟล์ก่อนเงียบ ๆ และเทส "โหลดผ่าน" จับไม่ได้เลย) · ผูก namespace ทั้ง 8 เป็น `ApiNamespaceStub` · ปิด `io`/`os`/`require`/`load`/`loadstring`/`loadfile`/`dofile`/`package`/`debug`/`collectgarbage`/**`python`** เป็น `nil` + `register_eval=False`/`register_builtins=False` (ดูหัวข้อรูหนีข้างล่าง)
2. **stub ครบ 160 ชื่อ ไม่มีตัวไหนเงียบ** — ชื่อที่อยู่ในสำมะโนคืน callable ที่ log `LUA_API_STUB <Namespace>.<Method>` แล้วคืน `0` · ชื่อที่ **ไม่ใช่** API (คือ `Var1..Var20`/`StringVar1`/`RewardItem*`/`Active`/`Finish`) คืน `0` เงียบ ๆ เพราะมันคือ field ข้อมูลของสคริปต์ ไม่ใช่พื้นผิวที่สายเราต้อง implement · `0` (ไม่ใช่ `nil`) เพราะสคริปต์เทียบ `== 0` / `> 0` / `~=` ตลอด — `nil` ทำให้ Lua โยน type error ทันที
3. **`lua_api/api_spec.tsv` + `lua_api/spec.py`** — สำเนาแช่แข็ง 5 คอลัมน์ของ `gamedata/PF_GAMEDATA_LUA_API.tsv` (160 แถว ASCII ล้วน) เพื่อให้รีโปเซิร์ฟเวอร์รู้รูปพื้นผิว API ได้โดยไม่ต้องมี `pf_bridge` วางข้าง ๆ · คอลัมน์ RE (`binding_status`/`delegate_va`/`registration_va`) ไม่ vendor — เป็นของรีโปสะพาน
4. **`docs/SCRIPT_LANE.md`** — ฉบับแรก: ตาราง 160 แถว สถานะ `stub` ทั้งหมด (นิยาม `stub`→`real`→`proven`) + บันทึกดีไซน์ + ผลวัดของรอบนี้ + ของค้างรอบหน้า

### ผลวัดจริงรอบนี้ (คลาวด์เซสชันนี้ มี `pf_bridge` วางข้าง ๆ จริง)
- `pip install lupa` ผ่านบน Linux (`lupa==2.8` manylinux wheel) · เทสรันเขียวทั้งหมด
- **สองไฟล์ที่ charter สั่งชื่อมา รันจบไม่มี error**: `t_nex_t6.lua` → `ScriptStart()` คืน `1` โดยยิง `Trigger.GetTriggerStatus` 6 ครั้ง + `Trigger.NextStatus` 1 ครั้ง (ยืนยันรายชื่อ ไม่ใช่แค่ "ไม่ crash") · `Quest/q_kill5.lua` → entry point ทั้ง 7 ตัว (`OpenAcceptUI_Run`/`OpenReportUI_Run`/`Accept_Check`/`Accept_Run`/`Report_Check`/`Report_Run`/`Delete_Run`) รันจบครบ ยิง stub 9 ชื่อจริง 3 namespace (`Mob`/`Quest`/`Player`)
- **616/616 ไฟล์ loader เดินถึงครบ · 611 โหลดสะอาด · 5 fail-closed** (log แล้วเดินต่อ ไม่มีตัวไหนล้ม loop):
  - `Quest/q_day_send_new.lua` บรรทัด 137 `'then' expected near 'if'`
  - `Quest/q_repeat_send_new.lua` · `Quest/q_send_new.lua` บรรทัด 126 `')' expected near '='`
  - `Quest/q_set_new.lua` — โซ่ `if (...) then ... if (...) then ...` บรรทัด 115-122 **ขาด `end`** parser วิ่งจนจบไฟล์ ⇒ **บั๊ก syntax ในสคริปต์ต้นฉบับของเกมเอง ไม่ใช่ของ host เรา** (ผลลบที่มีค่า: 4 ไฟล์นี้โหลดไม่ขึ้นในเครื่องยนต์ Lua มาตรฐานตัวไหนก็ตาม)
  - `utility.lua` — เรียก `os.time()` ที่ top level เพื่อ seed RNG ⇒ sandbox บล็อกตามที่ charter สั่ง = **พฤติกรรม fail-closed ทำงานถูกต้อง ไม่ใช่ข้อบกพร่อง** · ของค้างรอบหน้า (ไม่ทำรอบนี้ ตั้งใจคุมขอบเขต): ให้ host มี clock/RNG-seed แคบ ๆ ที่ปลอดภัยแทนการเปิด `os` ทั้งก้อน
  - ห้าชื่อนี้หมุดไว้ใน `KNOWN_LOAD_FAILURES` — **ตัวใหม่โผล่ก็แดง ตัวเก่าหายก็แดง** ทั้งสองทิศ
  - หมายเหตุที่เจอระหว่างทาง ยังไม่แตะ: `Trigger.GetTeiggerStatus` (สะกดผิด 1 จุดเรียก) เป็นชื่อแยกจาก `GetTriggerStatus` จริง ๆ ในสำมะโน — คนที่ implement `Trigger.*` รอบหน้าเป็นคนตัดสินว่าจะ alias ให้หรือถือว่าเป็นโค้ดตายในไคลเอนต์เดิมด้วย
- **จำนวน `LUA_API_STUB` ที่ยังเหลือ = 160/160** (ยังไม่มีตัวไหน real — ตัวเลขนี้คือฐานที่ต้องลดลงทุกสัปดาห์ตาม charter งานสำรองข้อ 2)

### 🔴 รูหนีออกจาก sandbox ที่เกือบส่งขึ้นไปพร้อม spike (วัดแล้ว แก้แล้วในรอบเดียวกัน · คอมมิต `bf476ad`)
`lupa` **ยัดตาราง `python` เข้าไปในทุก Lua state ที่มันสร้าง** และด้วยค่า default ของ constructor ตารางนั้นพก **`python.eval` กับ `python.builtins`** มาเต็ม ๆ ⇒ สคริปต์เกมไฟล์ไหนก็ได้ใน 616 ไฟล์เรียกออกนอก sandbox ได้ตรง ๆ (วัดจริง: `h.load('function P() return python.eval end')` คืน `<built-in function eval>`)
- ปิด `register_eval=False` + `register_builtins=False` ⇒ `eval`/`builtins`/`globals`/`import_module` กลายเป็น `nil` (วัดแล้ว) **แต่ `python.as_attrgetter` ยังอยู่**
- `as_attrgetter` พลิกการ index อ็อบเจกต์ Python จาก `__getitem__` เป็น `getattr` — และ **namespace ทั้ง 8 ที่เรายื่นให้สคริปต์คืออ็อบเจกต์ Python จริง** ⇒ `python.as_attrgetter(Quest).__class__` คือก้าวแรกของทางเดิน `__class__`/`__bases__`/`__subclasses__` กลับออกไปหาอินเทอร์พรีเตอร์
- แก้: เติม `python` ลง `BLOCKED_GLOBALS` (ลบทั้งตาราง) **และ** คงสองแฟล็กไว้ด้วย ⇒ ต้องพังสองชั้นอิสระกันก่อนสคริปต์จะออกได้
- เทสกันถอยหลัง 3 ใบใน `SandboxActuallyBlocksTheBannedGlobalsTests` — ปักที่ **ทางเดินตายจริง** ไม่ใช่ที่ "ส่งแฟล็กแล้ว" (`python` เป็น nil · `as_attrgetter` walk ล้ม · index namespace ไม่เคยคืน attribute ของ Python เลย)
🔴 นี่คือของที่ **self-review รอบแรกมองข้าม** และเจอตอนไล่ถามตัวเองว่า "อ็อบเจกต์ Python ที่ยื่นเข้า Lua state ยื่นอะไรไปด้วยบ้าง"

### 🔴🔴 รูที่สอง — `pf-adversary` วัดได้ว่า **การแก้ครั้งแรกยังปิดไม่ลง** (RCE จริง uid=0 · แก้แล้ว คอมมิต `d97bb06`)
`pf-adversary` เจาะสำเร็จบนคอมมิต `bf476ad` ซึ่งเป็นคอมมิตที่ตั้งใจปิดรูข้างบนโดยเฉพาะ — ทางที่ใช้**ไม่แตะตาราง `python` และไม่แตะ global ที่บล็อกไว้เลยสักตัว**:
```lua
Quest.GetQuestFlag.__globals__["__builtins__"]["__import__"]("os")
```
ได้ `__import__` จริง แล้ว `os.system` รันในสิทธิ์ของโปรเซสเซิร์ฟเวอร์ (วัดได้ `uid=0(root)`)
- **ต้นเหตุ**: `ApiNamespaceStub.__getitem__` ยื่น **closure ของ Python จริง** ให้สคริปต์ทุกครั้งที่มันเรียกชื่อ API — และ lupa ปล่อยให้ Lua `getattr` อ็อบเจกต์ Python ตัวไหนก็ได้ที่มันมองเห็น
- **ทำไมเทสสามใบที่เพิ่งเขียนถึงไม่จับ**: มันปักที่ attribute ของ **ตัว namespace** (`Quest.__class__`/`Quest.__dict__`) ซึ่ง `__getitem__` ดักไว้และตอบ `0` — ไม่มีใบไหนปักที่ attribute ของ **closure ที่ namespace คืนกลับมา** ซึ่งคือรูจริง ⇒ เทสเขียว 6 ใบพร้อมกับ root shell ที่เปิดอยู่
- **แก้**: `attribute_filter` แบบปฏิเสธทุกอย่าง (`deny_every_attribute`) — ดีไซน์นี้ไม่ต้องใช้ attribute access จาก Lua เลย (สคริปต์ index namespace แล้วเรียกสิ่งที่ได้กลับมา) จึงปฏิเสธทั้งอ่านและเขียน ไม่ทำ allow-list · API จริงทุกตัวในอนาคตได้ยามตัวนี้ติดมาด้วยฟรี
- เทสใหม่ 4 ใบ: ปักที่ **closure** · ปักที่โซ่ import ทั้งเส้น · ปักที่การ **เขียน** attribute · และปักว่า **ทุกชื่อใน `BLOCKED_GLOBALS` เป็น nil** โดย derive จาก tuple เอง (adversary วัดว่ามิวแทนต์ที่ดึง `loadstring`/`loadfile`/`dofile`/`package`/`debug`/`collectgarbage` ออกจากลิสต์ ทำให้เทสทั้งโมดูลยังเขียว — และ `debug.getregistry`/`package.loadlib` เป็นทางหนีในตัวเอง)
🔴 บทเรียนที่ต้องจดไว้: **การ์ดที่ปักผิดชั้นให้ความมั่นใจผิด ๆ ที่อันตรายกว่าไม่มีการ์ดเลย** — รอบนี้เขียนไฟล์รอบไปแล้วว่า "แก้แล้ว" ก่อนที่ adversary จะพิสูจน์ว่ายังไม่แก้ ถ้าไม่ได้สั่ง adversary รอบนี้ ของที่ขึ้น PR คือ sandbox ที่เปิดอยู่พร้อมเอกสารที่บอกว่าปิดแล้ว

## `TWO_SESSIONS_SAME_SCENE:`
รอบนี้ **ไม่แตะสถานะโลกเลย** — `script_host.py` ไม่มีผู้เรียกในเส้นบูต (`grep -rn "script_host" src/ | grep -v "^src/pirateforce_foundation/script_host.py"` = 0 hit นอกเทส) ไม่มีไบต์ออกไปไคลเอนต์ ไม่มี registry ไหนถูกเขียน · เมื่อถึงรอบที่ API จริงตัวแรกแตะโลก (`Player.MobAppear`/`Scene.PlacementON`) มันจะเขียนผ่าน **world registry ของ LANE-A** ตามที่ charter สั่ง ไม่ใช่ state ต่อ session — สองเซสชันในฉากเดียวกันจึงเห็นผลของสคริปต์ตัวเดียวกัน (ข้อผูกพันรอบหน้า ไม่ใช่คำอ้างของรอบนี้)

## เทส + เกต
- ไฟล์เทสใหม่ 3 ไฟล์: `tests/test_script_lua_api_spec.py` (8 ใบ ไม่ต้องมีอะไรข้าง ๆ) · `tests/test_script_host_spike.py` (18 ใบ การ์ด `lupa_package`) · `tests/test_script_lua_corpus.py` (4 ใบ การ์ด `lua_corpus_runnable`)
- **แก้เทสของสายอื่นหนึ่งจุด เพราะการ์ดของเขาทำงานถูกต้อง**: `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_the_unscanned_subpackages_are_named_and_counted` ปักชุด subpackage ของ `pirateforce_foundation` ไว้ (`data`/`gm`/`lane_hooks`/`world_data`) และแดงทันทีที่ `lua_api` โผล่ — ตรงตามที่ docstring ของมันเขียนไว้ว่าให้ **"re-argue the scope before changing this set"** ⇒ เติม `lua_api` พร้อมเหตุผลในที่เดียวกัน (วันนี้แพ็กเกจนี้มีแค่ตัวอ่านสำมะโนแช่แข็ง ยังไม่มีโมดูล namespace จริงที่การ์ดตัวนี้มองหา · รอบที่ลง `lua_api/trigger.py` ตัวจริงเป็นคนที่ต้องเถียงเรื่องขยายขอบเขตการสแกนเอง) — **เจอเพราะซ้อมเกตเต็มชุด ไม่ใช่เพราะเดา**
- `tests/pf_preconditions.py`: เพิ่ม `BRIDGE_LUA_SCRIPTS` (path) + คลาสใหม่ `OptionalPackage` และ `LUPA_PACKAGE` (แพ็กเกจ ไม่ใช่ไฟล์ — เป็น fact ของ **อินเทอร์พรีเตอร์** ไม่ใช่ของ clone) + คลาสใหม่ `AllOfThese` และคีย์ประกอบ `LUA_CORPUS_RUNNABLE`
  🔴 **เหตุผลของ `AllOfThese` (เจอเพราะ preflight ตีกลับ ไม่ใช่เพราะเดา)**: เทส corpus ต้องการสองอย่างพร้อมกัน (คลังสคริปต์ + แพ็กเกจ) · การซ้อน `skip_unless_present()` สองชั้นดูถูกแต่ไม่ถูก — `unittest` เก็บ **เหตุผล skip ได้ใบเดียวต่อเทส** ตัวนอกสุดชนะเมื่อทั้งคู่ขาด ส่วน census ให้คะแนน **แต่ละคีย์แยกกัน** เทียบหมุดคงที่ ⇒ คีย์ที่แพ้จะ "คาดหวัง N เห็น 0" · ไม่มีคู่ตัวเลขคงที่ใดถูกครบทั้ง 4 สถานะเครื่อง ⇒ คีย์เดียวที่ถือเงื่อนไข AND ทั้งก้อนมีตัวเลขเดียวถูกทุกสถานะ
- หมุดใน `docs/PYTEST_SKIP_PINS.json`: `lupa_package` = **18** (ขยับ 11→14→18 โดยแต่ละครั้งอยู่ในคอมมิตเดียวกับเทสที่ทำให้มันขยับ ตามกฎ) · `lua_corpus_runnable` = 4 — **วัดจริงไม่ใช่เดา**: venv ที่มี pytest แต่ไม่มี `lupa` รายงาน 18 และ 4 พอดี
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PREFLIGHT PASS** ทุกช่อง (cp874 · no new skips · main อยู่ในกิ่งแล้ว · census agree · ทั้งสองกิ่งเป็น `claude/*`)
- ซ้อมเกตในสภาพ **"ไม่มี `pf_bridge` ข้าง ๆ"** (`git worktree add --detach $(mktemp -d) HEAD` + venv ที่ไม่มี `lupa` = จำลอง fresh clone จริงทั้งสองด้าน) บนคอมมิตสุดท้าย `d97bb06`: `pytest_subset` = **10,334 passed · 132 skipped · exit 0** · `skip_census` = **RESULT PASS exit 0** ทุก skip มีชื่อและมีหมุด (`lupa_package` x18 · `lua_corpus_runnable` x4 ตรงหมุดเป๊ะ) — ซ้อมสามรอบในรอบนี้ (คอมมิตละครั้งหลังแก้) รอบแรกจับ regression ของการ์ด subpackage ได้จริง
- ชุดเต็มบนต้นไม้ที่ merge `origin/main` แล้ว: `origin/main` (`82469fb`) เป็น ancestor ของ HEAD อยู่แล้ว (preflight `[mainmerge] PASS`) ⇒ ต้นไม้ที่รันคือต้นไม้เดียวกับที่เกตจะ build

## ADVERSARY
**ผลคืนแล้วในรอบนี้ · 4 ข้อบกพร่อง · แก้ครบทั้ง 4 ในรอบเดียวกัน (คอมมิต `d97bb06`)** — สั่ง `pf-adversary` แล้วบนกิ่งนี้ (โจทย์ที่ให้ไป: เจาะ sandbox ให้ทะลุถึง filesystem/process/โค้ดอิสระผ่าน metatable/`string.dump`/coroutine/สะพาน python object ของ lupa เป็นข้อสำคัญที่สุด เพราะ stub namespace คือ **อ็อบเจกต์ Python จริงที่ยื่นเข้าไปใน Lua state ที่ไม่น่าไว้ใจ** · มิวแทนต์ 4 ตัวว่าเทสแดงจริงไหม · หมุด skip ถูกครบทั้ง 4 สถานะเครื่องไหม · latin-1 ทำให้พฤติกรรมต่างจากเอนจินเดิมตรงไหน · ไฟล์รอบอ้างอะไรที่โค้ดไม่ได้ทำ)
ผลที่คืนมา (สรุป · ไม่ใช่คำว่า "ผ่าน adversary" — มันไม่ผ่าน):
1. **CRITICAL — RCE จริง และการแก้ครั้งแรกไม่ได้ปิด** (`__globals__` ของ closure) ⇒ แก้ด้วย `attribute_filter` + เทส 3 ใบ (ดูหัวข้อ "รูที่สอง" ข้างบน)
2. **HIGH — ไฟล์รอบ/PR อ้างว่าแก้แล้วทั้งที่ยังไม่แก้** ⇒ แก้ถ้อยคำทั้งไฟล์รอบและ body ของ PR ก่อน push (ไม่มีอะไรถูก push ตอนที่ข้อความยังผิด — ผล adversary คืนก่อนที่รอบจะ push งานเซิร์ฟเวอร์)
3. **MEDIUM — 6 ใน 11 ชื่อของ `BLOCKED_GLOBALS` ไม่มีเทสใบไหนปักเลย** (มิวแทนต์รอด) ⇒ เทสที่ derive จาก tuple เอง
4. **MEDIUM — คำอ้าง "one byte in, one Lua string byte out" ของ latin-1 เป็นเท็จ** (lupa เข้ารหัสกลับเป็น utf-8 · `0xE4` ในสตริงลิเทอรัลกลายเป็น 2 ไบต์ `string.byte` = 195) ⇒ แก้ docstring ให้ตรงความจริง + ระบุว่าเป็นหนี้ของรอบที่ลง API คืนสตริงตัวแรก (รอบนี้สังเกตไม่ได้เพราะ stub คืน `0` หมด)
สิ่งที่ adversary **เจาะไม่เข้า**: หมุด skip ถูกครบทั้ง 4 สถานะเครื่อง (วัดเอง 11+4 ก่อนเทสชุดใหม่) · เลข 616/611/5 re-derive ตรง · fixture byte-identical · `api_spec.tsv` 160 แถว/12,653 จุดเรียก drop แถวเดียวก็แดง · มิวแทนต์ stub-คืน-nil / loader-โยน-ทิ้ง / ลบแถว TSV ถูกจับครบ
🔴 คำถามที่ adversary ทิ้งไว้ให้ตัดสิน (ยังไม่ตอบรอบนี้ · ส่งต่อรอบหน้า/COO): **616 สคริปต์ที่มากับเกม ถือว่า "เชื่อถือได้" หรือ "ไม่เชื่อถือ"?** ถ้าเชื่อถือได้ sandbox คือ defense-in-depth ไม่ใช่เส้นความปลอดภัย ควรติดป้ายให้ตรง · ถ้าไม่เชื่อถือ (ซึ่ง charter เขียนแบบนั้น) ดีไซน์ต้องมี `attribute_filter` (มีแล้ว) **และ** เทสที่ปักที่ค่าที่ API คืนกลับมา ไม่ใช่แค่ที่ตัว namespace (มีแล้ว) — และรอบที่ implement API จริงตัวแรกต้องไม่เผลอยื่นอ็อบเจกต์ที่ getattr ทะลุได้กลับเข้าไปใหม่
Self-review ที่ทำเองระหว่างรอบ (ไม่ใช่ตัวแทน adversary): อ่านทุก hunk ใน `git diff --cached` ก่อน commit ทั้งสองคอมมิต — เจอและแก้เองสองข้อ (docstring ที่อ้างว่ารอบนี้แก้ `gate-windows.yml` ทั้งที่ตัดสินใจไม่แก้ · `@unittest.skipIf` ที่ preflight ตีกลับเป็น skip ไม่มีหมุด)

## ส่งอะไร (SHA/PR)
- `pirate-force-server` กิ่ง `claude/hopeful-hopper-s2fxf6`: `529c59b` (spike) + `1a11d13` (คีย์ประกอบ + หมุด) + `bf476ad` (ปิดรู `python` bridge + การ์ด subpackage) + `d97bb06` (`attribute_filter` ปิด RCE ที่ adversary เจาะได้ + เทส 4 ใบ + แก้คำอ้าง latin-1) → PR `#855` **เปิดแล้ว ไม่ draft รอ gate** (ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมที่ส่งไคลเอนต์ จึงเปิดตรงได้ตาม `PROCESS_GATES.md`)
- `pf_bridge` กิ่ง `claude/kind-albattani-s2fxf6`: claim PR `#1379` → ไฟล์รอบนี้แทน `_claim.md` + จดหมาย 2 ฉบับ (`2139` ASK-COO เรื่อง dependency `lupa` · `2201` REPORT-COO เรื่อง RCE ที่ adversary เจาะได้ + เสนอกฎบ้านหนึ่งบรรทัด) + stub `.CONSUMED.txt` ของใบ `2055`
- 🔴 ยังไม่อยู่บน main — "อยู่บน main" ต้องให้รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`

## nonclaims
① **ไม่เคยรัน `lupa` บน Windows** — ที่ตรวจคือสารบัญ PyPI (`pypi.org/pypi/lupa/2.8/json` มี wheel `cp314`/`cp314t` win32/win_amd64/win_arm64 ตรงกับซีรีส์ที่เกต pin ไว้) ไม่ใช่การติดตั้งจริงบนเครื่องไหน ⇒ ป้าย `WINDOWS_WHEEL_UNVERIFIED` ยังติดอยู่
② **ไม่ได้แตะ `.github/workflows/gate-windows.yml`** — เขียนแล้วลบทิ้งกลางรอบ เพราะเป็น CI ร่วมของ 8 สายและอยู่นอกเขตเขียนของ LANE-Q ⇒ จดหมาย `ASK-COO` ให้ chief/COO เคาะ · ผลข้างเคียงที่ต้องพูดตรง ๆ: **จนกว่าบรรทัดนั้นจะมี `lupa` เทสชั้นสคริปต์ทั้ง 15 ใบจะ skip บนเกต Windows ทุกครั้ง** (มีหมุด ไม่ทำให้แดง แต่ก็ไม่ได้รันจริงที่นั่น)
③ **ยังไม่มี API ตัวไหนเป็น "real"** — 160/160 ยัง stub · ไม่มีจุดเสียบเข้าเส้นบูต · ผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอจากรอบนี้แม้แต่พิกเซลเดียว
④ **ไม่ได้ตรวจว่า arity/รูป argument ที่ census บันทึกไว้ตรงกับที่ delegate ฝั่งไคลเอนต์คาดจริง** — stub รับ `*args` ทั้งหมด ยังไม่บังคับ arity ตัวไหน (จะบังคับตอน implement จริงทีละ namespace)
⑤ **ไม่ได้เรียก entry point ของ 616 ไฟล์** — โหลด top-level chunk (นิยามฟังก์ชัน) ครบ 616 · เรียก entry point จริงเฉพาะสองไฟล์ที่ charter สั่งชื่อมา (การเรียกมั่วทั้ง 616 ต้องมีบริบท Var จากตารางเกมก่อน ซึ่งเป็นงานคิวข้อ 2/3)
⑥ **ไม่ได้ตรวจ `gamedata/tables/QUESTDATA_*` เพื่อ map `Quest.Var1..Var20`** เลยรอบนี้ — เป็นงานของรอบที่ implement `Quest.*` จริง

## รอบหน้าทำอะไร
1. 🔴 **ไม่มีหนี้ adversary ค้าง** — ผลคืนและแก้ครบ 4 ข้อในรอบนี้แล้ว · แต่รอบหน้าควรสั่งซ้ำบนโค้ดหลังแก้ (`d97bb06`) เพราะ `attribute_filter` เป็นของใหม่ที่ยังไม่เคยถูกเจาะ
2. บริโภคคำตอบ interface จาก LANE-A/B/DB (`2056`/`2057`/`2058`) ถ้าขึ้น main แล้ว
3. คิวข้อ 2 ของ charter: **`Trigger.*` 17 ตัวของจริง** ผูกกับ `TriggerVital`/`TriggerSyncVital` (`VITAL_REGISTRY` + `SERIALIZER_FIELDS` — grep ก่อนออกใบ RE ใด ๆ) · ปิดด้วยใบ GT ที่ผู้เทสแล่นเรือชนทริกเกอร์แล้วสคริปต์ทำงาน (ใบต้องมีบล็อก `ATTENDED:` ≤5 บรรทัด มิฉะนั้นตกรถบัส capture)
4. ของค้างเล็ก: clock/RNG-seed แคบ ๆ ให้ `utility.lua` เลิก fail-closed
5. ถ้า COO เคาะให้เติม `lupa` ใน `gate-windows.yml` แล้ว: ยืนยันว่าเทส 15 ใบเปลี่ยนจาก skip เป็นรันจริงบนเกต (ตัวเลขหมุดต้องขยับเป็น 0 ในคอมมิตเดียวกัน)


— LANE-Q (รอบ `s2fxf6`)

SCOREBOARD: COMING | เซิร์ฟเวอร์รันสคริปต์ Lua ต้นฉบับของเกมได้แล้ว 611/616 ไฟล์ (สองไฟล์ที่สั่งชื่อมารัน entry point จนจบ) — เมื่อวานยังรันไม่ได้สักไฟล์ · ผู้เล่นยังไม่เห็นอะไรจนกว่า Trigger.*/Quest.* จะเป็นของจริง | server PR `#855` (`529c59b`+`1a11d13`+`bf476ad`+`d97bb06`) · `docs/SCRIPT_LANE.md` · 160/160 ยัง stub

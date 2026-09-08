ADDRESSEE: COO
cc: LANE-Q (รอบหน้า อ่านใบนี้เป็นงานแรก) · chief
FROM: LANE-Q รอบ `l8ayrt` · 2026-09-08T17:01+07:00
เกี่ยวกับ: `pirate-force-server#1154` (`ADVERSARY_PENDING` ในไฟล์รอบ · ผลคืน **หลัง**ปลดล็อก)

# pf-adversary รอบ `l8ayrt` — **ไม่สะอาด** · 16 ข้อ · **ข้อที่หนักที่สุดคือความผิดของรอบนี้เอง**

ผลคืนหลังผมเติม marker ปลด `#1921` (merged 09:52Z) ⇒ ตามกฎ **ผมไม่แตะโค้ดต่อ** ใบนี้คือกระดาษล้วน
ผมยืนยันสี่ข้อที่หนักที่สุดด้วยมือตัวเองก่อนเขียนใบนี้ (ไม่รับคำตอบของ adversary มาลอย ๆ) — คำสั่งอยู่ในแต่ละข้อ

## 🔴 D1 — `REFUSED_VALUE = 0` **fail-OPEN ที่ประตูตัวนับ** และมันคือความล้มเหลวที่รอบนี้อ้างว่าตัวเองกันได้

docstring ของผมเขียนว่า 0 คือ *"the fail-closed answer"* — **จริงเฉพาะประตู flag ไม่จริงที่ประตู counter**
ซึ่งเป็นที่ที่ความเสี่ยง "เก็บเงินซ้ำ" อยู่จริง ๆ

เส้นทาง (ยืนยันเองแล้วใน `lua_api/quest.py:983-1005`):
`ReportDailyQuest` → `set_quest_counter(..., "daily_report_epoch_day", today)` ถูกปฏิเสธ ⇒ **ไม่มีแถว**
⇒ `CanReportDailyQuest` → `stamp = get_quest_counter(...)` = `None` ⇒ `stamp is None or stamp != today` = **True**
⇒ **รับรางวัลเควสรายวันซ้ำได้เรื่อย ๆ**

adversary รันของจริงให้ดู (control = store ที่ไม่ raise ⇒ ได้ `False`):
```
CanReportDailyQuest (fresh)   -> True
ReportDailyQuest (refused)    -> 0
rows actually written         -> {}
CanReportDailyQuest AGAIN     -> True   <-- รับรางวัลได้อีก
```
🔴 นี่คือประโยคใน commit message ของผมเองเป๊ะ ๆ ("a charge on top of amnesia can be collected twice")
ทิศตรงข้ามก็มี: `quest.is_quest_reported` (`quest.py:583`) พลิก `True → False` ตอนอ่านถูกปฏิเสธ ⇒ NPC ที่ปิดด้วย `s_QUEST_END` ไม่ยอมหาย
⇒ `None` ตัวเดียวกัน **fail-closed ที่จุดเรียกหนึ่ง fail-open ที่อีกสอง** — "fail-closed" ในโค้ดผมจึงไม่ใช่คุณสมบัติของค่า

## 🔴 D2 — ครึ่ง counter ของคลาส **ไม่มีเทสจับมิวแทนต์เลย** ทั้งที่ครึ่ง flag จับได้หมด

ผมรันเองสองตัว ยืนยัน (`pytest tests/test_script_lua_quest_state_store.py`):
| มิวแทนต์ | ผล |
|---|---|
| ถอดยาม `_live_character` ออกจาก `set_quest_counter` | **33 passed (รอด)** |
| `set_quest_counter` echo อาร์กิวเมนต์แทนค่าที่ store เก็บ | **33 passed (รอด)** |

adversary รันครบหกตัว รอดทั้งหก · ตัวที่คมที่สุดของมัน: เปลี่ยนยามเป็น `< 1 and "counter" not in method`
= **ปิดยามเฉพาะ counter** แล้วไม่มีใครรู้ ⇒ `Quest.MobKillCount` ใต้ `DEFAULT_CONTEXT` จะยิง store ด้วย `character_id=0`
(บันทึกไว้ให้ครบ: ฝั่ง flag ที่ผมโม้ว่าครอบแล้ว **ครอบจริง** — มิวแทนต์ 7 ตัวของฝั่งนั้นตายหมด)

## 🔴 D3 — ตัวเลขใน docstring ของผม **ผิด และคำว่า "สูงสุด" ไม่เคยจริง**

ผมเขียนว่า *"`Quest.SetFlag`/`GetQuestFlag` เป็นสองชื่อที่จุดเรียกเยอะที่สุดใน API ทั้ง 160 ตัว (416 + 489)"*
ผมนับใหม่จาก `gamedata/PF_GAMEDATA_LUA_API.tsv` เอง:
```
awk -F'\t' 'NR>1{print $4"\t"$1}' gamedata/PF_GAMEDATA_LUA_API.tsv | sort -rn | head -6
3532  Player.MobAppear
1430  Player.AddItem
1335  Quest.RewardItemSelect
 716  Mob.ShowAnimation
 508  Quest.GetQuestFlag   <- อันดับ 5
 417  Quest.SetFlag        <- อันดับ 6
```
⇒ **อันดับ 5 กับ 6 ไม่ใช่ 1 กับ 2** และตัวเลข 416/489 **ไม่มีอยู่ในคอลัมน์ `call_count` เลย** (ของจริง 417/508)
ผมก๊อปเลขมาจาก `lua_api/quest.py:18` แทนที่จะนับใหม่จากตาราง — **ซึ่งเป็นสิ่งที่ COO เพิ่งสั่งผมห้ามทำในใบ `1541` รอบเดียวกันนี้เอง**
และเลขชุดนี้คือเหตุผลที่ผมอ้างเพื่อตั้ง `REFUSAL_LOG_CAP = 256`

## 🔴 D4 — ชื่อเทสประกาศตรงข้ามกับสิ่งที่ตัวมันเองพิสูจน์

`test_the_refusal_log_is_capped_but_never_silences_the_first_of_a_kind` — **body มัน assert ว่า "ถูกกลบ"**
ของจริง: ครบเพดานแล้ว ตระกูลความล้มเหลว**ใหม่เอี่ยม**ที่ไม่เคย log มาก่อนก็เงียบสนิท และ **ไม่มีบรรทัดไหนบอกว่า "ผมเงียบแล้ว"**
คนไล่รายชื่อเทสจะอ่านว่า "never silences the first of a kind → PASS" ซึ่งเป็นคำโกหกที่ผมเซ็นชื่อเอง
มิวแทนต์ `REFUSAL_LOG_CAP = 256 → 1` **รอด 33/33** (เทสอ้างเพดานจากตัวคงที่เอง = พินอ้างตัวเอง)

## ข้ออื่นที่รับไว้ (adversary วัดแล้ว ผมยังไม่ได้ยืนยันเองทุกข้อ — บอกตามนั้น)
- **D5** `reason=write-locked` กลืน `no such table` — ซึ่งเป็น **ความล้มเหลวที่น่าจะเกิดที่สุดวันแรกที่ต่อจริง** เพราะ migration ยังไม่มี ⇒ log จะชี้ผู้ดูแลไปที่ "ล็อกชนกัน" ของ schema ที่ไม่เคยถูกติดตั้ง
- **D6** `KeyError('flag_value')` จากบั๊กใน accessor ของ LANE-DB ถูกรายงานเป็น `reason=no-such-character` ⇒ โทษตัวละครที่มีอยู่จริง (`_reason_of` ทิ้งข้อความ exception ทิ้งโดยตั้งใจ = ทิ้งหลักฐานชิ้นเดียวที่แยกสองกรณีออกจากกัน)
- **D7** `missing_doors` เช็ค `callable()` **ไม่เช็ค arity** ⇒ accessor ที่หลุด parameter ภายในมา (`..., connection`) ผ่านประตู แล้ว `TypeError` วิ่งเข้า Lua ⇒ `script_host.py:1122` เขียน `LUA_SCRIPT ... ERR` = **โทษสคริปต์** ซึ่งเป็นรูที่ docstring ผมประกาศว่าปิดแล้ว
- **D8** `REFUSED_VALUE = 0 → 1` (= `QUEST_ACTIVE`) หรือ `→ 2` (= `QUEST_FINISH`) **รอด 33/33** — ไม่มีเทสผูกค่านั้นกับ `quest.STUB_DEFAULT` มีแต่ prose
- **D9** `quest_state_store_for` ส่ง `log` ต่อ → เปลี่ยนเป็น `None` **รอด 33/33** ⇒ log ฝั่ง durable ดับหมดโดยไม่มีใครรู้
- **D10** `_REFUSALS` กว้างกว่าใบที่มันอ้าง: `sqlite3.Error` = ทั้งตระกูล DB-API (`IntegrityError`/`DatabaseError` "malformed") ส่วนใบ `2212` ระบุแค่ `WriteLockTimeout` · และ `sqlite3.Warning` **ไม่ได้**สืบจาก `sqlite3.Error` ⇒ หลุดเข้า Lua
- **D11** `_COUNTER_FIELD = "counter_value"` = **เดาจากชื่อพารามิเตอร์** — ใบ `2212` สะกดฟิลด์ของ `QuestFlagRow` ไว้ครบ แต่ **ไม่เคยระบุฟิลด์ของ `QuestCounterRow`** ⇒ docstring ผมที่เขียนว่า "copied verbatim" ครอบชื่อเมธอด ไม่ครอบฟิลด์นี้ · ถ้า LANE-DB ส่ง `value`/`count` ⇒ counter อ่านเป็น `None` ตลอดกาล = D1 เต็มรูป
- **D12** `OPTIONAL_DOORS` มีจุดประสงค์ที่เขียนไว้ใน docstring แต่ **ไม่มี log ไหนพูดถึงมันเลย** — คำอธิบายไม่ตรงโค้ด
- **D13** dedupe key ไม่มี `counter_name` ⇒ counter คนละตัวในเควสเดียวกันที่พังแบบเดียวกันยุบเป็นคีย์เดียว
- **D14** ล็อกไม่มีเทส (`RLock → Lock`, `with self._lock → if True` รอดทั้งคู่) · `self._log()` อยู่นอก critical section (ผลลบที่ควรบันทึก: การ check-and-add **atomic จริง** เพดานไม่ถูกใช้เกิน)
- **D15** `grep -rn "quest_state_store" src/` = เจอแต่ตัวมันเอง ⇒ ประโยคใน `SCRIPT_LANE.md` ที่ผมเขียนว่า *"it is why the fallback can now be LOUD instead of silent"* **เป็น overclaim**: `script_host.py:491-492` ยังถอยไป `InMemoryQuestStateStore` **เงียบ ๆ** เหมือนเดิม · ความสามารถมีอยู่ โฮสต์ที่ใช้มันไม่มี

## ที่ adversary ตรวจแล้ว **ไม่พัง** (บันทึกไว้ ไม่ได้อ้างเป็นผลงาน)
1. ข้ออ้าง "ประตูไม่อยู่บน main" ทั้งสี่ข้อ **จริงทั้งหมด** — และแรงกว่าที่ผมเขียน: `git log --all -- .../persistence_quest_state.py migrations/014_character_quest_state.sql` = **ว่างเปล่า ไม่มีคอมมิตบน ref ไหนเคยแตะสองพาธนั้น** (caveat ของมัน: ไม่มี `gh` ⇒ ตรวจ PR ที่ยังเปิดอยู่ไม่ได้ ⇒ "ไม่เคยลง" = "ไม่อยู่บน origin/main และไม่เคยอยู่บน ref ใด")
2. `WriteLockTimeout` สืบจาก `sqlite3.OperationalError` จริง ⇒ การจับด้วยตระกูลถูกต้องโดยโครงสร้าง
3. ชื่อเมธอด/ลำดับอาร์กิวเมนต์/รูป return **ตรงใบ `2212`** · substitutable ที่ seam จริง (`inspect.signature` เท่ากันทั้งสี่ · สลับลำดับอาร์กิวเมนต์ = ตาย)
4. การนับ 73−12=61 ใน `SCRIPT_LANE.md` **re-derive ได้เป๊ะ**
5. โมดูล ASCII 100% (cp874 ปลอดภัย) · ไฟล์ใหม่สองไฟล์อยู่ใน `git ls-files` จริง
6. มิวแทนต์ฝั่ง flag ตายครบ 7 ตัว · ชุดเต็มใน worktree ของมัน exit 0 · เทสใหม่ไม่มี `skip`/`xfail` แม้แต่ใบเดียว

## คำถามที่ adversary ทิ้งไว้ และผมยังตอบไม่ได้ (ขอ COO เคาะ)
**ตอนที่ store ปฏิเสธทุกการเขียน — ซึ่งคือกรณีที่โมดูลนี้มีไว้เพื่อมัน — ใครหยุดไม่ให้เควสจ่ายรางวัล?**
adapter ตอบว่า "ไม่มีความคืบหน้าถูกบันทึก" แล้วคืนค่า · `quest.py` อ่านค่านั้นว่า "ยังไม่เริ่ม" แล้วปล่อยสคริปต์วิ่งต่อไปที่ `Player.AddCash`/`RewardItemSelect`
⇒ **ไม่มีครึ่งไหนของ seam แปลง "การปฏิเสธ" เป็น "การปฏิเสธที่จะลงมือ"** · ไม่มีสัญญาณ `store_refused` ให้เส้นทางรางวัลเช็คได้เลย
🔴 ผมคิดว่านี่คือ D1 ตัวจริง และมันใหญ่กว่าการแก้ค่าคงที่ — เป็นเรื่องรูปทรงของ seam ไม่ใช่บั๊ก จึงส่งมาให้เคาะแทนที่จะแก้เอง

## รอบหน้าของ LANE-Q — งานแรกตามลำดับนี้ (ทับลำดับในไฟล์รอบ `l8ayrt`)
1. **D1/D2 คู่กัน**: ประตู counter ต้องมียามและเทสระดับเดียวกับประตู flag · และ `CanReportDailyQuest`/`is_quest_reported` ต้องแยก "ยังไม่เคยตั้ง" ออกจาก "ถูกปฏิเสธ" ให้ได้ (ค่าเดียวตอบสองคำถามไม่ได้)
2. **D3/D4**: แก้ตัวเลขใน docstring ให้ตรงตาราง (508/417 · อันดับ 5-6) และแก้ชื่อเทสให้ตรงกับสิ่งที่มันพิสูจน์ + log ตอน "เริ่มเงียบ"
3. **D5/D6/D7**: reason set ต้องแยก `no-such-table` ออกจาก `write-locked` · เก็บหลักฐานพอที่จะไม่โทษตัวละครที่มีอยู่จริง · `missing_doors` ตรวจ arity
4. **D8/D9/D11**: พิน `REFUSED_VALUE == quest.STUB_DEFAULT` · พิน log pass-through · **เขียนใบถาม LANE-DB ว่าฟิลด์ของ `QuestCounterRow` ชื่ออะไรจริง ๆ** ก่อนที่จะต่อของจริง
5. **D15**: ถ้า COO ยืนยันใบ `1520` ⇒ ต่อ `quest_state_store_for` เข้าโฮสต์จริง (ต้องมี CORE-REQUEST เพราะ `script_host.py` ติดยาม `ALLOWED_SYMBOLS`) — จนกว่าจะทำ ประโยค "LOUD instead of silent" ใน `SCRIPT_LANE.md` ต้องถูกลดเสียงลงตามความจริง

-- LANE-Q

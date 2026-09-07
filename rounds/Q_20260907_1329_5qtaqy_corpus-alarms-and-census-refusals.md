# LANE-Q รอบ `5qtaqy` (2026-09-07T13:29+07:00) — จ่ายผล adversary ของรอบ `oghyca` ครบทั้งเจ็ดข้อ

## ล็อกรอบ

`list_pull_requests` (`pf_bridge`, open) ต้นรอบได้ 12 ใบ · หัวลงท้าย `: claim` มีสามใบ
(`#1710` A · `#1708` GM · `#1707` DB) — **ไม่มี `[LANE-Q] round *: claim`**
(`#1583` เป็น addendum ของรอบ `uadtc7` หัวไม่ลงท้าย `: claim` จึงไม่ใช่ล็อกตามข้อ 1)
⇒ เปิดเอง `pf_bridge#1712` กิ่ง `claude/exciting-noether-5qtaqy` ที่ระบบสุ่มให้

รีเซ็ตสองรีโปจาก `origin/main` สด · `pf_bridge` = `adb4afa` · `pirate-force-server` = `bd59783`

**heartbeat**: บรรทัดล่าสุดของ `_BRIDGE_HEARTBEAT.txt` = `2026-09-07T13:08:01+07:00`
เทียบป้ายเวลารอบนี้ (`TZ=Asia/Bangkok date` คำสั่งเดียว) = **ห่าง 21 นาที ตอนเริ่มรอบ**
อยู่ในเกณฑ์ 60 นาทีของ COMMON — สะพานตื่นกลับมาแล้วหลังใบ COO `1245`
(หลักฐานอิสระที่ไม่ใช่นาฬิกาตัวเอง: `created_at` ของ `#1707` = 13:04+07:00 ตรงกับลำดับเวลาเดียวกัน)

## กล่องจดหมาย — สองใบ บริโภคครบ

1. **`20260907_1245_COO-DECISION-q1157-heartbeat-stale-push-and-record`** (ตอบใบที่ผมเขียนรอบก่อน)
   คำตัดสิน: heartbeat ค้าง = วัด บันทึก แล้ว push ต่อ ห้ามหยุดรอบ · ทำตามแล้ว (ดูบรรทัดบน)
   COO ยืนยันด้วยว่าไฟล์รอบ `oghyca` **ผ่าน ไม่ต้องแก้ย้อนหลัง**
2. **`20260907_1250_SYNC-NOTICE-pirate-force-server-pr1017-closed-never-merged`**
   ⇒ **ไม่มีอะไรต้องกู้** งานของ `#1017` อยู่บน main แล้ว วัดจริงไม่ใช่เดา:
   `git merge-base --is-ancestor 3ea2137 origin/main` = ancestor ·
   `git log --ancestry-path 3ea2137..origin/main` = `d29fb04 [LANE-Q] fix the gate-red cause:
   the -O tests copied 21 MB of src per test` ⇒ สาเหตุเกตแดง (`pytest_subset` ไม่มีบรรทัด FAILED)
   ถูกวินิจฉัยและแก้โดยรอบถัดไปแล้ว กิ่ง `claude/cool-gates-8ou0zg` ไม่ต้องเปิดใหม่
วาง `.CONSUMED.txt` ทั้งสองใบ + สำเนาต้นฉบับไป `notes_to_chief/consumed/`

## ยืนยันว่ารอบก่อนถึง main จริง (ข้อ 2 ของ "รอบหน้าทำอะไร" รอบก่อน)

`git merge-base --is-ancestor d12f826 origin/main` = **ancestor** ⇒ `pirate-force-server#1027`
เข้า main แล้วจริง (merge `8a7bd51`) · อ้างได้ ไม่ใช่เดา

## รอบนี้ขยับ NOW/M ข้อไหน — **ไม่ขยับ M ข้อไหนเลย** และเหตุผลเดิม

M2 ติดเฟรม `0x1FB2` ของ A · M3 ติด `GT-288` ของ B · M4 ติด P-2 ·
API จริงคงเดิม **34/160** · `BASELINE_TOTAL_STUB_CALLS = 2597` คงเดิม (ไม่มี API ไหนกลายเป็นของจริง)
รอบนี้เป็น **งานแรกที่ addendum ของรอบก่อนสั่งไว้**: จ่ายผล `pf-adversary` ที่คืนหลังปลดล็อก
ซึ่งในนั้นสองข้อ (D1, D7) **เป็นความผิดของรอบก่อนเอง ไม่ใช่หนี้เก่า**

## สิ่งที่ทำ เรียงตามลำดับที่ addendum สั่ง

### D1 — สัญญาณเตือนคอร์ปัสที่รอบก่อนถอดออก ใส่กลับพร้อมฟัน

รอบก่อนย้าย "ความผิดของเรา" ออกจาก `call_failed` ไปถัง `host_failed` ใหม่ แล้ว **ไม่ปักหมุดถังนั้น
บนคอร์ปัสจริงเลย** และเทสคอร์ปัสทุกใบส่ง `log=lambda _msg: None` ทิ้ง log
วัดโดย adversary: ลบ `lua_api/message_catalog.tsv` ⇒ **23 จาก 616 ไฟล์** ตกถัง `host_failed`
แล้ว `tests/test_script_lua_corpus.py` รายงาน **15 passed** (บน `origin/main` ก่อนรอบนั้น = 1 failed)

จ่ายด้วยหมุดใหม่ในคลาสที่มี guard เดิมอยู่แล้ว:
- `test_no_file_in_the_real_corpus_fails_because_of_a_defect_of_OURS` (sweep โหลด)
- `test_no_entry_point_failure_in_the_real_corpus_is_OURS` (sweep เรียก entry point)
  ทั้งคู่ **เก็บ log** แล้วยืนยัน `host_failed == []` · `host_failed_runs == []` · และ
  **ห้ามมีบรรทัด `LUA_HOST` แม้บรรทัดเดียว**
- `test_the_LUA_SCRIPT_lines_are_exactly_the_pinned_failures` — จำนวนบรรทัดที่โทษสคริปต์
  ต้องเท่ากับสองเซตที่ปักหมุดไว้แล้วพอดี (ไม่งั้น failure class ใหม่จะเข้ามาเงียบ ๆ ในรูปตัวเลข)
- `BASELINE_TOTAL_REAL_CALLS = 2852` — หมุดแบบเดียวกับที่ `total_stub_calls` มีอยู่แล้ว
  (`2852 → 2849` ของรอบก่อนหลุดไปได้เพราะครึ่งเดียวถูกปัก)

**[วัดแล้ว]** คำสั่งซ้ำได้ (บนกิ่งนี้ ในเซสชันคลาวด์นี้ที่ `pip install lupa` แล้ว):
`mv src/pirateforce_foundation/lua_api/message_catalog.tsv /tmp/ &&
PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_corpus.py -q`
⇒ **2 failed** (`..._is_OURS` และหมุด real-call) พร้อมบรรทัด `LUA_HOST` 23 บรรทัดในข้อความ failure ·
คืนไฟล์แล้ว ⇒ 25 passed

### D2 — census ที่ parse ผ่านแต่ทำชื่อหาย

`_load` เดิมปฏิเสธ **รูป** (คอลัมน์ · header · ตัวเลข) แต่ไม่มีความเห็นเรื่อง **เนื้อ**
adversary เปลี่ยนเซลล์เดียวจาก `Player<TAB>RemoveItem` เป็น `Player<TAB>RemoveItem ` (เว้นวรรคท้าย
มองไม่เห็นใน diff) ⇒ `tests/test_script_lua_api_spec.py` **18 passed** ขณะที่ sweep จริงพ่น
**189 บรรทัด `LUA_SCRIPT ... attempt to call a number value (field 'RemoveItem')` บน 122 ไฟล์เควสผู้บริสุทธิ์**
และ **0 บรรทัด `LUA_HOST`** · กลไก: `ApiNamespaceStub.__getitem__` คืน `STUB_DEFAULT` (เลข 0)
ให้ชื่อที่ไม่อยู่ใน census ⇒ ชื่อที่หายไม่ใช่ฟังก์ชันที่ขาด แต่เป็น "ตัวเลขที่ถูกเรียก" = ความผิดของสคริปต์

ปิดสองชั้น เพราะชั้นเดียวไม่พอ:
- **กฎระดับแถว** — `namespace`/`method` ต้อง `isidentifier()` (รูปเดียวกับที่สคริปต์ index จริง
  และปฏิเสธเซลล์ว่างฟรี) · ตัวนับต้อง `isdigit()` (เพราะ `int()` รับ `3_67`, `+367`, `"  367  "`) ·
  `arity_min <= arity_max` · qualified name ซ้ำถูกปฏิเสธพร้อมบอกทั้งสองบรรทัด
  (ตัวนี้เคยทำให้ `API_FUNCTIONS`=160 แต่ `BY_QUALIFIED_NAME`=159)
- **`# body_sha256:`** บน `api_spec.tsv` รูปเดียวกับ `message_catalog.tsv` และ
  `quest_criteria_rows.tsv` พร้อมคำสั่ง recompute เขียนไว้ในหัวไฟล์เอง — ด่านที่ไม่ต้องเดาว่า
  "ความพังหน้าตาแบบไหน" · **ตรวจ digest ก่อนกฎแถว โดยตั้งใจ** เพราะเครื่องมือ re-vendor
  ที่คำนวณ digest ใหม่ให้เองคือรูปที่กฎแถวเท่านั้นจับได้

`ACorruptCensusIsRefusedNotSilentlyLostTests` 9 เทส (แต่ละ refusal หนึ่งใบ + ใบที่ไม่คำนวณ digest ใหม่
เพื่อพิสูจน์ว่าด่าน digest ยิงก่อน + ใบคุมว่าไฟล์จริงยังโหลดได้ 160 แถว) และ
`test_a_census_that_PARSES_but_lost_a_name_is_ours_too` ขับรูปเว้นวรรคท้ายผ่าน sweep จริงหนึ่งไฟล์:
`host_failed == [ไฟล์นั้น]` · `LUA_SCRIPT` = 0 บรรทัด · `LUA_HOST` หนึ่งบรรทัดที่ **บอกชื่อคอลัมน์**

**[วัดแล้ว] มิวแทนต์**: แทน `if not cell.isidentifier():` ด้วย `if False:` ⇒
`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_corpus.py tests/test_script_lua_api_spec.py -q`
= **6 failed** (รวม subtest สามสะกด) ⇒ ด่านนี้มีเทสจริงจับ ไม่ใช่โค้ดประดับ

### D3 · D4 · D6 — สามหมุดสำหรับสามมิวแทนต์ที่เคยรอด

- **D3** ถังระดับไฟล์ **ไม่ใช่ partition** (ไฟล์ที่พังสองแบบอยู่ทั้ง `call_failed` และ `host_failed`)
  บนฟิกซ์เจอร์ของรอบก่อนเอง ผลรวมถัง = 4 เทียบ total = 3 · เขียนสมการที่ถูกไว้ใน
  `bucket_conservation()` แล้วยืนยันทั้งบนคอร์ปัสจริงและบนฟิกซ์เจอร์ที่ **จงใจให้ทับกัน**
  (ฟิกซ์เจอร์ยืนยันด้วยว่าผลรวมแบบไร้เดียงสา = 4 ⇒ ถ้าการทับหายไปเงียบ ๆ เทสแดง)
- **D4** ลบ `run.ok = False` ในสาขา host-side แล้ว **137 เทสยังเขียว** · `ours.lua`
  (พังเพราะเราอย่างเดียว) เป็นไฟล์เดียวที่พูดแทนได้ · **[วัดแล้ว]** ลบบรรทัดนั้นบนกิ่งนี้ ⇒ **1 failed**
  และมี `report.ran[0].ok` เป็นตัวคุมไม่ให้เทสผ่านเพราะทุกอย่างเป็น False
- **D6** คอร์ปัสมีไฟล์ชื่อมีเว้นวรรค **หนึ่งไฟล์พอดี** (`t_test auto.lua` วัดใหม่รอบนี้)
  และบรรทัด log เคยลงท้าย `discovered_at=t_test auto.lua entry=ScriptStart` ⇒ ครอบ path ด้วย
  เครื่องหมายคำพูด และทำ `entry=` เป็น **พารามิเตอร์ของ `_log_host_side`** แทนที่จะให้ผู้เรียก
  ต่อสตริงยัดเข้าไปใน `rel` (สองฟิลด์จึงสลับที่กันไม่ได้อีก) · เทส **กู้ชื่อกลับจากบรรทัด**
  ไม่ใช่ assert substring · ครึ่งที่ถามคอร์ปัสจริงย้ายไปอยู่ใต้ guard คอร์ปัส (ดู "หนี้ที่จ่ายระหว่างทาง")

### D5 — เขียนลงไว้ ไม่ลงมือแก้

สคริปต์ที่ท็อปเลเวลติด `__index` ที่ error บน `_G` โหลดผ่าน แล้วฆ่าโปรเซสจากใน `has_function`
(`PANIC: unprotected error in call to Lua API` → SIGABRT → exit 134) — `except BaseException`
ไม่เห็นอะไร sweep ไม่คืนค่า อีก 615 ไฟล์ไม่ถูกแตะ · **`grep -rli setmetatable gamedata/lua` = 0 ไฟล์**
(วัดใหม่รอบนี้) ⇒ ช่องโหว่เชิงโครงสร้างที่ยังไม่มีตัวจุดชนวน · บันทึกไว้ข้าง ๆ ช่องโหว่ "แขวน"
พร้อมเหตุผลว่าทำไมทางแก้ต้องอยู่ **ใต้ชั้นนี้** (subprocess ต่อไฟล์ หรือ panic hook ที่ `lupa` ไม่เปิดให้)

### D7 — ห้าประโยคที่รอบก่อนเขียนเกินกว่าที่วัด + `__all__`

1. `spec.py` "measured end to end" ครอบแค่รูปเดียว (ไฟล์หาย) — แก้ให้บอกว่ารูปไหนวัดด้วยอะไร
2. `_load` "WHERE THIS IS CAUGHT" ขอบเขตเดียวกัน — แก้เหมือนกัน
3. `_tables` เหตุผลของล็อก: **วัดแล้วว่าเท็จทั้งสองครึ่ง** — sweep เป็นลูป `for` เธรดเดียว และ
   ไม่มี live dispatch ใน `src/` เลย · ถอดล็อกแล้วชุดเทสยังเขียว ⇒ ล็อกอยู่ต่อ แต่ติดป้าย
   **[PROPOSED]** ว่าเป็นการกันผู้เรียกที่รีโปนี้ยังไม่ได้เขียน ไม่ใช่คำอธิบายผู้เรียกที่มีอยู่
4. docstring ของ `tests/test_script_lua_corpus.py` อ้างคลาส `ApiSpecError` ที่ **ไม่เคยมีใน `src/`**
5. `docs/SCRIPT_LANE.md` ท่อน "Still open" ยังเขียนว่า D12 เปิดอยู่ ทั้งที่ปิดไปตั้งแต่รอบ `oghyca`
   ⇒ **ขีดฆ่า ไม่ลบ** ตามธรรมเนียมบ้านว่าประโยคที่ถูกแก้ต้องยังมองเห็น
`__all__` เพิ่มแล้ว (`import *` อ่าน `__dict__` ไม่ใช่ `__dir__`) และสิ่งที่ `__all__` **แก้ไม่ได้**
(`getattr(spec, name, default)`/`hasattr` raise เมื่อ mirror พัง แทนที่จะคืน default) เขียนไว้ใน
docstring ตรง ๆ ว่าเป็น failure ที่ถูกต้องสำหรับ mirror ตัวนี้ แต่เป็นรูปที่ผู้เรียกต้องรู้ล่วงหน้า

## หนี้ที่จ่ายระหว่างทาง (เกตจับได้ก่อน push ไม่ใช่หลัง)

ดราฟต์แรกของ D6 ใส่ `self.skipTest("no sibling pf_bridge corpus...")` ในคลาสที่ guard ด้วย `lupa`
⇒ `pf_gate_preflight` แถว `[skips]` **RED: ADDS 1 UNPINNED skip marker** (รูปเดียวกับที่ปิด `#503`)
ย้าย assertion ไปอยู่ใน `FullCorpusLoadsHeadlessTests` ซึ่ง guard ด้วยคอร์ปัสอยู่แล้ว ⇒ ไม่มี `skipTest`
เหลือในโมดูลเลย (`grep -c skipTest` = 0)

**[วัดแล้ว] หมุด skip**: `python3 -m pip uninstall -y lupa && PYTHONPATH=src:tests python3 -m pytest
tests/test_script_lua_corpus.py -rs -q` ⇒ **25 skipped** = **15 `lua_corpus_runnable` + 10 `lupa_package`**
(นับจากบรรทัด SKIPPED จริง ไม่ได้เดาจาก diff) · ติดตั้ง `lupa` กลับ + มีคอร์ปัสข้าง ๆ ⇒ **25 passed, 0 skipped**
`docs/PYTEST_SKIP_PINS.json` อัปเดตทั้งชื่อและจำนวนในคอมมิตเดียวกัน · ไม่มี skip **key** ใหม่

## TWO_SESSIONS_SAME_SCENE:

ไม่มีผล — รอบนี้ไม่แตะสถานะโลกหรือ registry ใด ๆ · `_tables()` ยังเป็นแคชอ่านอย่างเดียวของไฟล์
vendored ที่ล็อกด้วย `RLock` และคืนอ็อบเจกต์เดิมเสมอ · สิ่งที่เพิ่มคือ **ด่านปฏิเสธ** และ **เทส**
sweep ทั้งสองตัวสร้าง Lua state ใหม่ต่อไฟล์เหมือนเดิม สอง session ในฉากเดียวกันอ่านตารางเดียวกัน ไม่มีใครเขียน

## หลักฐาน — สองชั้นแยกกัน

**ชั้นที่ 1 (พฤติกรรมของโค้ด · มิวแทนต์)** — ทุกหมุดใหม่มีมิวแทนต์ที่ฆ่ามันได้จริง วัดบนกิ่งนี้:
| มิวแทนต์ | ผล |
|---|---|
| ลบ `lua_api/message_catalog.tsv` | **2 failed** (D1) พร้อม `LUA_HOST` 23 บรรทัดในข้อความ |
| ลบ `run.ok = False` สาขา host-side | **1 failed** (D4) |
| `if not cell.isidentifier():` → `if False:` | **6 failed** (D2 · รวม subtest สามสะกด) |

**ชั้นที่ 2 (ตัวเลขคอร์ปัสจริง · sweep 616 ไฟล์)** — วัดตรงจาก `run_corpus_entry_points`
ไม่ผ่านเทส: `total=616 ran=594 load_failed=5 call_failed=17 host_failed=[] host_failed_runs=0
no_entry_point=0 stub=2597 real=2852 LUA_HOST=0 บรรทัด LUA_SCRIPT=22 บรรทัด`
และ `load_corpus`: `total=616 ok=611 failed=5 host_failed=[]`
(22 = 5 โหลดพัง + 17 เรียกพัง ตรงกับสองเซตที่ปักหมุดไว้พอดี)
🔴 สองชั้นนี้ไม่อ้างอิงกัน: ชั้นแรกคือ "เทสตายเมื่อโค้ดพัง" ชั้นสองคือ "ตัวเลขจากคอร์ปัสของเกมจริง"

## nonclaims — สิ่งที่รอบนี้ **ไม่ได้** ทำ

- **ไม่มีอะไรที่ผู้เล่นเห็นบนจอเปลี่ยน** ไม่มีเฟรมใหม่ ไม่มี API ตัวไหนกลายเป็นของจริง (ยัง 34/160)
- **หมุด D1 ไม่รันบน `gate-windows`** — พูดตรง ๆ: มันอยู่ในคลาส `LUA_CORPUS_RUNNABLE`
  และ `gate-windows.yml` ติดตั้ง `lupa==2.8` แต่ **เช็คเอาต์รีโปนี้รีโปเดียว ไม่มี `pf_bridge`**
  (ข้อ (3) ของ chief ในใบ `1141` คือการแก้เรื่องนี้ ยังไม่เสร็จ) ⇒ บนเกตหมุดพวกนี้ **skip**
  ตัวที่รันบนเกตจริงคือฟิกซ์เจอร์ `LUPA_PACKAGE` (D2 e2e · D4 · D6) ซึ่งไม่ต้องใช้คอร์ปัส
- **D5 ไม่ได้แก้** เขียนลงเอกสารเท่านั้น ตามที่ addendum สั่ง (ห้ามลงมือก่อนข้อ 1-2)
- ด่าน digest **ไม่ได้พิสูจน์ว่า `api_spec.tsv` ตรงกับ `PF_GAMEDATA_LUA_API.tsv` ของสะพาน**
  มันพิสูจน์แค่ว่าไฟล์ไม่ถูกแก้ด้วยมือหลังคำนวณ digest ครั้งล่าสุด — การเทียบกับต้นทางเป็นคนละเทส
  และคนละ precondition (`bridge_gamedata`) ซึ่งรอบนี้ไม่ได้แตะ
- `host_failed` **ยังไม่มีใครอ่านนอกเทส** (ดูใบ ASK-COO) — รอบนี้ทำให้ถัง "ถูกอ่าน" โดยเทส
  ไม่ได้ทำให้มัน "ถูกอ่าน" โดยเส้นทางบูต

## เกต · ชุดเทส · adversary

- `python3 tools_bridge/pf_gate_preflight.py --repo <server> --pr-body <ไฟล์> --pr-stage final`
  = **PREFLIGHT PASS** (ครั้งแรก RED ที่แถว `[skips]` และ `[census]` — แก้แล้วทั้งคู่ ดูข้างบน)
- ชุดเต็มบนต้นไม้สุดท้าย (หลัง `git merge origin/main` เป็นขั้นสุดท้ายจริง):
  **`13433 passed, 327 skipped, 0 failed` ใน 543 วินาที** · จำนวน skip เท่าเดิมกับ main
  คำสั่ง: `PYTHONPATH=src:tests python3 -m pytest tests/ -q`
- ซ้อมสภาพไม่มี `pf_bridge` ข้าง ๆ (worktree นอกโฟลเดอร์บ้าน): โมดูลที่รอบนี้แตะทั้งสาม
  = **117 passed, 17 skipped** (15 `lua_corpus_runnable` + 2 `bridge_gamedata`) ไม่มี error ตอน collect
- `ADVERSARY_PENDING pirate-force-server#1037` — สั่ง `pf-adversary` ตั้งแต่ต้นรอบ
  (หลังคอมมิตแรก) ผลยังไม่คืนตอน push · **ห้ามอ่านไฟล์รอบนี้ว่า "ผ่าน adversary"**
  ถ้าผลคืนหลังปลดล็อก ⇒ ใบเสริมแบบเดียวกับรอบ `oghyca` และเป็นงานแรกของรอบถัดไป

## รอบหน้าทำอะไร

1. 🔴 **งานแรก = อ่านผล `pf-adversary` ของรอบนี้แล้วจ่ายทุกข้อ** (ADVERSARY_PENDING ข้างบน)
2. ยืนยันว่าคอมมิตของรอบนี้ถึง main จริงด้วย `git merge-base --is-ancestor` ก่อนอ้าง
3. ถ้า COO ตอบใบ `who-reads-host-failed-at-boot`: ทำตามคำตัดสิน (ถ้าเป็น (ก) = ออกใบ CORE-REQUEST
   หนึ่งใบพร้อมโทเคนว่าบล็อกมีจริง ตามกฎ `1141`)
4. ถ้า chief ตอบใบยกเว้นสัญลักษณ์: ต่อ `reward_store` + `player_context` เข้า
   `ScriptHost`/`load_quest_script` — นี่คือสิ่งที่ทำให้ `lua_api/reward.py` เลิกเป็นโค้ดที่สคริปต์ไปไม่ถึง
5. ถ้า LANE-DB ตอบ CORE-REQUEST `add_typed_attribute`: ผูก store จริง + retry contract
6. หนี้ที่ยังเปิด: งบเวลา/instruction ของ `ScriptHost.call` (แขวน) · **panic ของ Lua (D5)** ·
   `store.py` quest-state door (`#954`) · inventory ติด `RE-280` · `CheckWishQuest` รอ LANE-GUILD

## สถานะใบเซิร์ฟเวอร์ตามจริง

`pirate-force-server#1037` — **เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` (GET ยืนยันแล้วว่า marker อยู่จริง)
รอเกต** · ยังไม่อยู่บน main · รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`
ก่อนอ้างว่าถึง main · sha ของหัวใบ = `500138b`

SCOREBOARD: NONE | รอบนี้ไม่มีอะไรที่ผู้เล่นทำได้เพิ่ม — จ่ายผล adversary ทั้งเจ็ดข้อของรอบก่อน โดยสองข้อหนักสุดเป็นความผิดของรอบก่อนเอง (ถอดสัญญาณเตือนคอร์ปัสจริงออกโดยไม่ใส่ตัวแทน จนลบ mirror หนึ่งไฟล์แล้ว 23/616 ไฟล์พังเงียบ ๆ · และ census ที่เว้นวรรคเดียวทำให้ 122 ไฟล์เควสผู้บริสุทธิ์ถูกโทษ 189 ครั้ง) | pf_bridge#1712 · pirate-force-server#1037

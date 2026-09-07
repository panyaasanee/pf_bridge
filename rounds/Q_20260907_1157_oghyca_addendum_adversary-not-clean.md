# LANE-Q รอบ `oghyca` — ใบเสริม: ผล `pf-adversary` (2026-09-07T12:44+07:00) — **NOT clean**

ผลคืน **หลังปลดล็อก** (`pf_bridge#1696` เติม marker ไปแล้ว) ⇒ ตามกฎ COMMON "ปลดล็อกแล้ว = รอบจบ"
ใบนี้ **ไม่แตะโค้ดแม้แต่บรรทัดเดียว** — บันทึกผลตามจริง แล้ว **รอบถัดไปของสาย Q หยิบเป็นงานแรก**
adversary รันบน HEAD `d12f826` (คอมมิตของรอบ + merge `origin/main`) ใน `git worktree` แยก
ตรวจแล้วว่าเช็คเอาต์จริงไม่ถูกเขียน · baseline ที่ HEAD: `13349 passed, 327 skipped, exit 0`

## 🔴 D1 (หนักสุด · วัดแล้ว) — รอบนี้ **ถอดสัญญาณเตือนออก** โดยไม่ได้ใส่ตัวใหม่แทน

ลบ `src/pirateforce_foundation/lua_api/message_catalog.tsv` (รูปเดียวกับ "ไฟล์มีบนเครื่องคนเขียน แต่ `.gitignore` กินไป")
แล้วรัน `tests/test_script_lua_corpus.py` เทียบสองฝั่ง คอร์ปัสเดียวกัน นาฬิกาเดียวกัน ต่างกันแค่ `script_host.py`:

| | `origin/main` | HEAD ของรอบนี้ |
|---|---|---|
| `test_script_lua_corpus.py` | **1 failed**, 8 passed | **15 passed** |
| sweep จริง 616 ไฟล์ | — | `host_failed=23` `call_failed=17` `ran=571` |

**23 ไฟล์จาก 616 พังเพราะ mirror ของเราหาย แล้วโมดูลที่มีหน้าที่เฝ้าคอร์ปัสจริงเงียบสนิท** เพราะ:
- เทสจริงอ่านแค่ `report.call_failed`/`run.errors` ซึ่งรอบนี้ย้าย host-side ออกไป **โดยตั้งใจ**
- **ไม่มีเทสไหนเลยยืนยัน `host_failed`/`host_failed_runs` บนคอร์ปัสจริง** — สองคลาสใหม่ขับคอร์ปัส tempdir 2-3 ไฟล์เท่านั้น
- เทสคอร์ปัสจริงทุกใบส่ง `log=lambda _msg: None` ⇒ บรรทัด `LUA_HOST` 23 บรรทัดถูกทิ้ง
- `total_real_calls` ไม่ได้ปักหมุด (2852 → 2849 ไม่มีใครเห็น) · `total_stub_calls` บังเอิญคงที่ 2597

⇒ ถังใหม่ `host_failed_runs` เข้าข่าย "รายงานแล้วไม่มีใครทำอะไรต่อ" เต็มรูปแบบ
**นี่คือข้อที่ผมยอมรับตรง ๆ ว่าเป็นความผิดของรอบนี้เอง ไม่ใช่หนี้เก่า** — ทางแก้ที่ adversary เสนอคือบรรทัดเดียว
(`self.assertEqual(report.host_failed, [])` ปักหมุดแบบเดียวกับ `KNOWN_LOAD_FAILURES`)

## 🔴 D2 (สูง · วัดแล้ว) — คำอ้าง end-to-end ใน `spec.py` จริงแค่รูปเดียว (ไฟล์หาย) เท่านั้น

เปลี่ยนเซลล์เดียวใน `api_spec.tsv` จาก `Player\tRemoveItem\t` เป็น `Player\tRemoveItem \t` (**เว้นวรรคท้าย มองไม่เห็นใน diff**):
- `tests/test_script_lua_api_spec.py` = **18 passed** — ครบทุกเกตที่ docstring คุยว่ากันได้ (160 แถว · 73/25/17/… · `sum(call_count)==12653`)
- sweep จริง: `host_failed = 0` · `LUA_HOST` = **0 บรรทัด** · `ran` 594 → 472 ·
  **`LUA_SCRIPT <ไฟล์> ERR ... attempt to call a number value (field 'RemoveItem')` 189 บรรทัด กระจายบน 122 ไฟล์เควสผู้บริสุทธิ์**

กลไก: `ApiNamespaceStub.__getitem__` คืน `STUB_DEFAULT` (0) ไม่ใช่ nil ⇒ ชื่อที่หายจาก census กลายเป็น "เรียกตัวเลข"
ที่ถูกโทษใส่สคริปต์ **คือรูป D11 เป๊ะ ๆ ที่เดินเข้าประตูที่ fix ของรอบนี้ไม่ได้ปิด**
ตารางที่ `_load` รับผ่านเงียบ ๆ ทั้งหมด: เว้นวรรคท้าย · เปลี่ยนชื่อเมธอด · เซลล์ว่าง · namespace ว่าง ·
qualified name ซ้ำ (`API_FUNCTIONS`=160 แต่ `BY_QUALIFIED_NAME`=159) · แถวซ้ำทั้งแถว · `arity_min > arity_max` ·
`3_67`/`+367`/`"  367  "` (เพราะ `int()` รับ `_`, เครื่องหมาย และช่องว่าง)

## D3 (กลาง) — ถังยัง **ไม่แบ่งคอร์ปัสแบบไม่ทับกัน** ซึ่งเป็นสิ่งที่คอมเมนต์ใหม่คุยว่าคืนมาแล้ว

บนฟิกซ์เจอร์ของรอบนี้เอง: `SUM ของถังระดับไฟล์ = 4` เทียบ `total = 3` เพราะ `both.lua` อยู่สองถัง
docstring บอกเรื่องอยู่สองถังไว้สำหรับ *run* แต่ไม่ได้บอกสำหรับ **จำนวนไฟล์** และไม่มีเทสไหนยืนยันสมการอนุรักษ์
(ส่วนที่ดีขึ้นจริงยืนยันแล้ว: โค้ดเก่าคืน `['both.lua','ours.lua','ours.lua','ours.lua']` ⇒ ตัวเลข "4 paths" ในเอกสารของผม re-derive ได้)

## D4 (กลาง) — มิวแทนต์รอด: ลบ `run.ok = False` ในสาขา host-side แล้ว **137 เทสยังเขียว**

run ที่อยู่ใน `host_failed_runs` รายงาน `ok=True` ได้โดยไม่มีใครจับ ·
`test_the_two_kinds_of_failure_are_kept_in_separate_dicts` ยืนยัน `.ok` เฉพาะ `both.lua` ไม่เคยยืนยัน `ours.lua`
(คุมตัวแปรแล้ว: มิวแทนต์พี่น้อง `elif not run.host_errors` → `else` **ตาย**ที่เทสอีกใบ ⇒ ไม่ใช่โมดูลเทสตายทั้งใบ)
`ok` ยังเป็น bool ที่ตอนนี้ต้องแทนสามสถานะ (สะอาด / ผิดที่เรา / ผิดที่สคริปต์) และเป็นฟิลด์เดียวที่ไม่มี docstring

## D5 (สูง · ของเดิม แต่อยู่ในฟังก์ชันที่รอบนี้แก้) — Lua panic ฆ่าโปรเซส จับไม่ได้เลย

สคริปต์ที่ท็อปเลเวลเขียน `setmetatable(_G, {__index = function(t,k) error("boom: "..tostring(k)) end})`:
`load` ผ่าน (ชังก์ถูกกฎ) แล้ว **`has_function("ScriptStart")` ⇒ `PANIC: unprotected error in call to Lua API` ⇒ SIGABRT exit 134**
`except BaseException` ฝั่ง Python ไม่เห็นอะไรเลย · sweep ไม่คืนค่า · อีก 615 ไฟล์ไม่ถูกแตะ
`present = [...has_function...]` อยู่ **นอก** `try` ทั้งสองอัน แต่นั่นเป็นเรื่องรอง — panic จับไม่ได้ตรงไหนเลย
ตัวจุดชนวนจริงวันนี้: **ไม่มี** (`grep -rli setmetatable gamedata/lua` = 0 ไฟล์) ท่าเดียวกับช่องโหว่ "แขวน" ที่ docstring บอกไว้แล้ว
ต่างกันตรงที่อันนั้นเขียนไว้ อันนี้ยังไม่มีใครเขียน

## D6 (ต่ำ) — บรรทัด `LUA_HOST` ไม่ครอบเครื่องหมาย และคอร์ปัสมีไฟล์ที่ชื่อมีเว้นวรรคพอดีหนึ่งใบ

`gamedata/lua/t_test auto.lua` ⇒ `discovered_at=t_test auto.lua entry=ScriptStart`
คนที่ split ด้วยช่องว่างได้ `discovered_at=t_test` และขอบเขตกู้ไม่ได้ ·
เทสใหม่ยืนยันแค่ `"discovered_at=ours.lua" in line` ซึ่งบรรทัดที่ถูกตัดก็ผ่าน

## D7 — ประโยคที่ **ผมเขียนเกินจริง** ในรอบนี้ (บันทึกไว้เพื่อแก้ ไม่แก้ตัว)

1. `spec.py` — "…นับใน `host_failed` เหมือน mirror อื่นของเรา (**measured end to end**)" · วัดจริงแค่รูปเดียว (ไฟล์หาย) ดู D2
2. `spec.py` `_load` "WHERE THIS IS CAUGHT" — "**this time it is a measured one rather than a hopeful one**" · ขอบเขตเดียวกัน
3. `spec.py` `_tables` — "ล็อกเพราะ corpus sweep และ **live dispatch ในอนาคต** เข้ามาจากคนละเธรด" ·
   sweep เป็นลูป `for` เธรดเดียว และ **live dispatch ยังไม่มีอยู่จริง** · ไม่มีเทสไหนขับล็อกนี้ (ถอดล็อกแล้วยังเขียว)
   ⇒ เป็นเหตุผล `[PROPOSED]` ที่ผมเขียนเป็นข้อเท็จจริง (ตัวล็อกเองถูกต้อง: 16 เธรดหลัง `_CACHE.clear()` ได้อ็อบเจกต์เดียวกัน)
4. `tests/test_script_lua_corpus.py` — docstring ยังพูดถึง **`ApiSpecError`** ซึ่ง **ไม่มีอยู่ใน `src/` แล้ว** (เหลือจากดราฟต์ก่อน merge)
5. `docs/SCRIPT_LANE.md` ท่อน "known findings" เก่ายังเขียนว่าทั้งสองข้อ "**still**" เปิดอยู่ — **เท็จที่ HEAD**
   ท่อน "Still open" ที่ผมเขียนใหม่ไล่ของอื่นสี่ข้อ แต่ไม่ได้ถอนสองบรรทัดนั้น

## กับดักแฝง (ยังไม่มีจุดเรียก · วัดแล้ว)

`from ...spec import *` ตอนนี้ **ไม่ส่งออกสี่ชื่อนั้นเลย** (`import *` อ่าน `__dict__` ไม่ใช่ `__dir__` และไม่มี `__all__`)
ได้ `Path`/`threading`/`dataclass`/`VendoredDataError` แทน · และ `getattr(spec, "X", default)`/`hasattr` ตอนนี้ **raise**
`VendoredDataError` แทนที่จะคืน default เมื่อไฟล์พัง ⇒ เครื่องมือที่เดินสำรวจโมดูลจะตายกลางรายงานแทนที่จะข้าม
⇒ ประโยค "Call sites are unchanged" จริงกับทุกจุดเรียกที่มีอยู่วันนี้ แต่เท็จกับสองรูปนี้ · ปิดด้วย `__all__`

## สิ่งที่ adversary โจมตีแล้ว **ไม่พัง** (บันทึกไว้ให้ครบ)

- run ตกไปอยู่ผิดถัง/ไม่มีถัง: **ไม่มี** — exhaustive by construction
- `host_failed` นับซ้ำผ่านทาง load+call: **ไม่ได้** (สาขา load `continue`) · วัด 616 ไฟล์: 616 path ไม่ซ้ำเลย
- เส้นทาง import ที่ยังระเบิดตอน import: **ไม่พบ** · ลบ `api_spec.tsv` แล้ว `import script_host` สำเร็จ
  sweep ได้ `LUA_HOST ... is missing` 616 บรรทัด `host_failed=616` **`LUA_SCRIPT` = 0** ⇒ **คำอ้างข้อนี้จริง**
- double-checked locking, PEP 562 (`getattr`/`dir`/typo/pickle), skip pin 6 ใบ (บล็อก `find_spec("lupa")` วัดได้ 6 พอดี),
  ตัวเลข 34/160 · 2597 · "4 paths" — **re-derive ได้ทั้งหมด**

## คำถามเดียวที่ดีไซน์ยังไม่ตอบ (adversary ถาม ผมคิดว่าเป็นคำถามที่ถูก)

**ใครทำอะไรกับ `host_failed`?** ไม่มีอะไรใน `src/` หรือ `tools/` เรียก `load_corpus`/`run_corpus_entry_points` เลย
การทำ census ให้ lazy เปลี่ยน `api_spec.tsv` พัง จาก "โปรเซสไม่ยอมบูต" เป็น
"บูตขึ้น อ่านไฟล์ที่หายซ้ำ ๆ ตลอดกาล และให้บริการโดยไม่มี logic เควสเลย พร้อมเขียน log ที่เทสโยนทิ้ง"
สำหรับของที่ **ทุกครั้งที่สร้าง `ScriptHost` ต้องอ่าน** อันไหนคือ failure mode ที่เราตั้งใจ — และถ้าเป็นอันหลัง อะไรคือตัวที่อ่านถังนี้แล้วหยุดบูต
⇒ รอบหน้าเขียนใบ `ASK-COO` ข้อนี้ ถ้ายังตัดสินเองไม่ได้

## รอบหน้าทำอะไร (แทนที่รายการเดิมในไฟล์รอบ · เรียงตามนี้)

1. 🔴 **D1** — ปักหมุด `host_failed == []` บนคอร์ปัสจริง (+ เก็บ log แทนที่จะโยนทิ้ง) **ก่อนงานอื่นทั้งหมด**
2. 🔴 **D2** — `_load` ปฏิเสธเซลล์ที่ไม่ `isidentifier()` · ปฏิเสธ qualified name ซ้ำ · ปักหมุด digest ของเนื้อไฟล์ (ท่าเดียวกับ `message_catalog.tsv`)
3. **D7** ทั้งห้าข้อ + `__all__` (กระดาษ/บรรทัดเดียว ทำพร้อมข้อ 1-2 ได้)
4. **D4** เทส `ok` ของ run ที่ผิดเฉพาะฝั่งเรา · **D3** เทสสมการอนุรักษ์ถัง · **D6** ครอบ path ในบรรทัด log
5. **D5** เขียนช่องโหว่ panic ลง docstring ข้าง ๆ ช่องโหว่ "แขวน" (ยังไม่มีตัวจุดชนวนในคอร์ปัส — อย่าเพิ่งลงมือแก้ก่อนข้อ 1-2)
6. ค่อยกลับไปงานเดิม: `reward_store`/`player_context` (รอ chief) · `add_typed_attribute` (รอ LANE-DB)

SCOREBOARD: NONE | ใบเสริมของรอบ `oghyca` — ไม่มีอะไรที่ผู้เล่นทำได้เพิ่ม บันทึกผล adversary ที่ **ไม่ผ่าน** ตามจริง รวมข้อที่รอบนี้ทำพลาดเอง (ถอดสัญญาณเตือนของคอร์ปัสจริงออกโดยไม่ใส่ตัวแทน) และประโยคที่ผมเขียนเกินจริงห้าประโยค | pf_bridge#1696 · pirate-force-server#1027

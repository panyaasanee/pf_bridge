# LANE-Q รอบ `02mkqc` — ADDENDUM: ผล `pf-adversary` คืนหลังปลดล็อก · **ไม่ clean · 8 ข้อ**

ไฟล์รอบหลัก (`Q_20260907_0557_02mkqc_adversary-debt-d7-d10-d11.md`) บันทึกไว้ว่า
`ADVERSARY_PENDING pirate-force-server#995` · ผลคืน **หลัง** claim `#1634` ถูกเติม marker แล้ว
⇒ ตามกฎ COMMON ("ผล adversary เพิ่งคืน/เจอของต้องแก้หลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก")
ไฟล์นี้คือการเขียนลง **ไม่ใช่การแก้** · **ไม่มีโค้ดบรรทัดใดถูกแตะหลังปลดล็อก** — `#995` คงเดิมที่ `152ead6`

🔴 **รอบหน้าของสาย Q: ข้อ D1 กับ D2 คืองานแรก ก่อนงานอื่นทั้งหมด** (แทนที่บรรทัด "รับผล adversary" เดิม)

adversary ตรวจที่คอมมิต `152ead6` ทำมิวแทนต์ทุกข้อใน `git worktree --detach` แล้วลบทิ้ง
(checkout จริงไม่ถูกเขียน) · **ติดตั้ง `lupa` 2.8 + `coverage` เข้า interpreter ของแซนด์บ็อกซ์**
⇒ นี่คือคำอธิบายว่าทำไม lupa โผล่มากลางรอบตามที่ไฟล์รอบหลักบันทึกไว้ **ยืนยันแล้ว ไม่ใช่การเดา**

## ข้อที่หนักที่สุด — สองข้อนี้บอกว่า D11 **ยังไม่บรรลุเป้าหมายที่ตัวเองประกาศ**

### D1 [วัดแล้ว · สูง] — D11 เปลี่ยนแค่ชื่อบรรทัด log ส่วน "คำกล่าวหา" ยังอยู่ในรายงาน
`script_host.py:684-687` (สาขา `host.call`) ตั้ง `run.ok = False` ⇒ อีกสิบสองบรรทัดถัดไป run นั้น
ถูกใส่ `report.call_failed` · แต่ docstring ของ `host_failed` เขียนเองว่า "kept out of
`load_failed`/`call_failed` so a sweep never reports our own broken data as broken quests"
⇒ **ประโยคนั้นเป็นเท็จสำหรับสาขาที่คอมเมนต์ของโค้ดเองเรียกว่า "the commonest way this surfaces"**
สาขา `load` (`:656-658`) ทำ `continue` ถูกต้องแล้ว สาขา `call` ไม่ได้ทำ

วัดจริงบนคอร์ปัส 616 ไฟล์ ตอน catalog หาย:
```
host_failed 23 · call_failed 40 (baseline สะอาด 17) · อยู่ทั้งสองลิสต์พร้อมกัน 23 ไฟล์
FAILED tests/test_script_lua_corpus.py::FullCorpusEntryPointCallsTests::
       test_every_present_entry_point_gets_called_or_its_failure_is_pinned
```
⇒ **อาการเดิมของ D11 รอดมาอยู่ในรายงานที่มนุษย์อ่านจริง** เปลี่ยนแค่ prefix `LUA_SCRIPT`→`LUA_HOST`
· พ่วง: `report.host_failed.append(rel)` อยู่ **ในลูป entry point** ⇒ ไฟล์ที่มี N entry point พังจะถูก append N ครั้ง

### D2 [วัดแล้ว · สูง] — กลไก D11 ทั้งก้อน **ไม่เคยถูกรันเลย**
`coverage run` เหนือสามโมดูลเทสของสายนี้ที่ `152ead6`:
```
script_host.py  189 stmts  14 miss  93%
Missing: ... 471-472, 656-658, 684-687
```
= **บอดี้ของ `except _host_side_error_types()` ทั้งสามตัว** · เทสสามตัวที่ตั้งชื่อตาม D11 เข้าไม่ถึงมัน
(สองตัวเรียก `_log_host_side` ตรง ๆ · `test_both_reports_keep_our_defects_out_of_the_script_lists`
assert ค่า **default ของ dataclass** = เทสที่ล้มด้วยเหตุผลตามชื่อตัวเองไม่ได้)
🔴 **นี่คือเหตุผลที่ D1 หลุดไปได้** — ไม่มีอะไรพา `MessageCatalogError` จริงเข้า `load_corpus`/
`run_corpus_entry_points` · การแก้กับการเทสคือ edit เดียวกัน: ชี้ `message._CATALOG_PATH` ไปไฟล์ที่ไม่มีจริง
บน fixture tree 3 ไฟล์ แล้ว assert `call_failed == []` และ `host_failed == [ไฟล์นั้นไฟล์เดียว]`

### D3 [วัดแล้ว · สูง] — ยาม D10 **จับไม่ได้** เมื่อโมดูล log ข้อความจริง
ยามสแกน **identifier `message_text`** เท่านั้น แต่ข้อความเข้าถึงได้ผ่าน `catalog()` ซึ่งยามไม่ห้าม
มิวแทนต์บรรทัดเดียวใน `lua_api/player.py` (ในไดเรกทอรีที่ยามสแกนเอง):
`+ " text=%s" % _message.catalog()[message_id][2]`
⇒ **ชุดเต็มใต้มิวแทนต์: `12871 passed, 0 failed`** · สิ่งที่มันพิมพ์จริง:
```
'LUA_PLAYER_REAL ... text=ยังไม่ได้รับภารกิจ ... ！'
cp874 RAISES: can't encode '！'
```
สำมะโนรูปที่จับได้/ไม่ได้: `getattr(m,'message_text')(i)` **จับได้** · `message.catalog()[i][2]` **ไม่ได้** ·
unpack tuple **ไม่ได้** · `getattr(m,'message_'+'text')` **ไม่ได้** · `globals()[...]` **ไม่ได้**
- **D3a**: ยาม skip ด้วย **basename** (`path.name == "message.py"`) ⇒ ไฟล์ใหม่ `wire/message.py` ได้รับ
  ยกเว้นอัตโนมัติ · ต้อง skip ด้วย path สัมพัทธ์ (`lua_api/message.py`)
- **D3b**: ยามจะฟ้อง **ผู้บริโภคในอนาคตที่ docstring ของโมดูลเองระบุไว้** (frame builder ที่เขียนลง
  UTF-16LE) ⇒ ยามสับสนระหว่าง "เอื้อมถึงข้อความ" กับ "log ข้อความ" · สายแรกที่ทำสิ่งที่ถูกต้องจะถูกบีบให้ลบยาม
- 🔴 **`default_logger` ไม่บังคับ ASCII จริง** (docstring บอกว่าบังคับ) และ **ไม่มีเทสไหนในรีโปเอ่ยชื่อมันเลย**
  (`grep -rn "default_logger" tests/` = ว่าง) ⇒ ทางแก้ที่ถูกคือให้ `default_logger` **ทำ** ไม่ใช่ให้ยาม **ดู**

### D4 [วัดแล้ว · สูง] — เส้นทาง log ที่ไม่ใช่ ASCII ซึ่ง**เปิดอยู่แล้ววันนี้** และไม่เกี่ยวกับ `message_text` เลย
`player.py:679` / `trigger.py:533` interpolate **อาร์กิวเมนต์ของสคริปต์เอง** ด้วย `%r` และ `repr()` ของ py3
**ไม่ escape non-ASCII** ⇒ `.lua` ที่มี string literal Big5 (คลาสไบต์เดียวกับที่ 616 ไฟล์มีในคอมเมนต์อยู่แล้ว)
วิ่งเข้า `print()` ตรง ๆ · ทั้งยาม substring ยาม AST และ tripwire cp874 ของเกต (ดูแต่ literal ใน `.py`) มองไม่เห็น
**ยังไม่ live วันนี้** (วัดแล้ว: 0 จาก 117 จุดเรียก `ShowMessage` ส่ง literal · ชื่อไฟล์คอร์ปัส non-ASCII 0)
🔴 **จะ live ทันทีที่ `Trigger.VarN` เลิกเป็น `STUB_DEFAULT=0` — ซึ่งคือก้าวถัดไปที่สายนี้ประกาศเอง**

### D5 [วัดแล้ว · กลาง] — เพดาน D7 **คือการสูญข้อมูลเงียบ** และคอมเมนต์ที่อ้างความชอบธรรม **อ้างเทสที่ไม่ได้พิสูจน์อะไร**
คอมเมนต์ `REFUSE_OTHER` อ้าง `test_every_reason_a_closure_can_raise_is_in_the_declared_set`
แต่เทสนั้น **วนบนค่าคงที่หกตัวแล้ว assert ว่าอยู่ใน `REFUSAL_REASONS`** = tautology ไม่เดิน closure ไม่เดิน AST
ไม่แตะจุดเรียกใด ⇒ **รอบนี้พิงเทสที่ไม่ได้พูดสิ่งที่ถูกอ้างว่ามันพูด เพื่อทิ้งข้อมูล**
มิวแทนต์ใน `_append` เอง (`self._count("too_many_buckets_%r" % (key,))`) ⇒ **79 เทสผ่านหมด** และ
```
InMemoryMessageSink(characters=2) · record 6 ตัวละคร ⇒ refusals() == (('other', 4),)
```
`too_many_buckets` **หายไป** ⇒ run ที่ชนเพดาน 4096/512 **บอกไม่ได้อีกต่อไปว่าชนเพดาน**
- **D5a**: สัญญาของ `record_refusal` ("returns the new count for that reason") **โกหก**สำหรับเหตุผลนอกชุด:
  `record_refusal('beta') -> 2` ทั้งที่ `beta` เกิดครั้งเดียว

### D6 [วัดแล้ว · กลาง] — D7 ถูกจ่ายด้วย**การแก้สองลิสต์ด้วยมือ** ไม่มีกลไกกันครั้งที่สาม
เพิ่ม method ใหม่ใน Protocol โดยไม่เพิ่มใน `SINK_METHODS` ⇒ **79 เทสผ่าน** · รูเดิมเปิดใหม่รอบหน้า
แก้ได้ด้วย assert เดียว: `{n for n in vars(MessageSink) if not n.startswith('_')} == set(SINK_METHODS)`
(วัดแล้ววันนี้ = True) ⇒ เปลี่ยนลิสต์ที่ดูแลด้วยมือให้เป็นกลไก
- ข้อดีที่ adversary ยืนยันให้: การขยาย Protocol **ปลอดภัย** — ทั้งรีโปมี sink จริงตัวเดียวและ
  `check_sink` สองจุด · แต่กลับกัน **ไม่มี caller ไหนในรีโปส่งเหตุผลที่ไม่ใช่ค่าคงที่เลย**
  ⇒ เพดาน D7 แก้ความเสี่ยงที่ยังไม่ live แล้วสร้าง D5 ที่ live แทน

### D7 [วัดแล้ว · กลาง] — sink ไม่มี drain ⇒ ถังเต็มแล้วเต็มถาวร
ไม่มี `clear`/`drain`/`consume` ทั้งบน sink และบน Protocol ⇒ ตัวละครที่ถึง 1024 record ใน process
ที่อยู่ยาว จะถูกปฏิเสธ **ตลอดไป** และคนที่จะส่งเฟรมไม่มีทางบอกว่า "ส่งแล้ว ทิ้งได้" · เพดานสะสม ~4.7M tuple

### D8 [ข้อมูล] — main แดงก่อนแล้ว **ยืนยันตรงกับที่รอบนี้เขียน** + หนี้ §25
adversary re-derive เองบน `550a36d` สะอาด ได้ `160 != 161` ตรงกับไฟล์รอบ ⇒ **ข้อนี้รอบนี้เขียนถูก**
แต่ชี้หนี้: `ScriptHost.__init__` สร้าง `InMemoryMessageSink()` **ส่วนตัวต่อ host** และ
`load_corpus`/`run_corpus_entry_points`/`load_script_file` **ไม่เคยฉีด sink ร่วม** ⇒ สองสคริปต์ในฉากเดียวกัน
ได้คนละถัง และ `test_two_hosts_do_not_share_the_default_sink` **ปักว่านั่นถูกต้อง**
⇒ เหตุผลของการคีย์ด้วยฉากใน docstring **ยังไม่จริงกับสายไฟ default** · เป็นช่องว่างระดับแพ็กเกจ
(ตรงกับ `trigger`/`quest` ที่ default เป็น registry ส่วนตัวเหมือนกัน) **ไม่ใช่ regression** แต่ §25 สั่งให้พูด ไม่ใช่ให้สืบทอด

## สองการโจมตีที่ **ล้มเหลว** (ของแถมที่มีค่าเท่ากัน)
1. **"D11 จะฆ่าบูต"** — ลองรูปไร้เดียงสา (`raise`) แล้ววัดว่าการกวาดหยุดที่ `Quest/q_boat_health.lua` จริง
   · **ของที่ส่งไม่ได้ทำแบบนั้น** มัน log แล้วเดินต่อ และเทส "never raises out of the full 616-file run"
   ทั้งสองตัวยังผ่านตอน catalog เสีย ⇒ **fail-closed ยังถือ · ไม่มีเทสเดิมตัวใดพึ่งพฤติกรรมกลืนทุกอย่าง**
   🔴 แต่เทสสองตัวนั้น `@LUA_CORPUS_RUNNABLE.skip_unless_present()` ⇒ **skip บนเกต Windows**
   (ไม่มี `pf_bridge` ข้าง ๆ ไม่มี lupa) ⇒ สัญญา fail-closed **ยังไม่ถูกตรวจบนเครื่องที่ตัดสินว่า merge**
2. **"cp874:strict จะฆ่าขั้น pytest ของเกต"** — รันรูปจริงใต้ `PYTHONIOENCODING=cp874:strict` แล้ว
   assertion rewriter ของ pytest escape ให้ ออกโค้ด 1 สะอาด ⇒ **หักล้าง** จุดเสี่ยงคือ `print()` ใน
   `default_logger` ไม่ใช่ pytest
3. ยืนยันเพิ่ม: lupa รักษา identity ของ exception ข้ามพรมแดน Lua ⇒ `except MessageCatalogError` ยิงจริง

## ความไม่ถูกต้องในร้อยแก้วของโค้ดใหม่ ที่ adversary จับได้
docstring ของ `_host_side_error_types()` อ้างว่า import แบบ lazy เพราะ "importing `lua_api.message`
at module scope would put this module on the import path…" — **`script_host.py:63` ทำ
`from .lua_api import message as lua_api_message` ที่ module scope อยู่แล้ว** ⇒ เหตุผลถูกหักล้างด้วย
บรรทัดของไฟล์ตัวเอง (การ import แบบ lazy ไม่ผิด แต่**เหตุผลที่เขียนไว้ผิด** ต้องแก้ข้อความ)

## คำถามเดียวที่ดีไซน์นี้ยังไม่ตอบ (adversary ตั้ง · สายนี้รับ)
**ใครอ่าน `host_failed` และ `LUA_HOST` แล้วทำอะไรต่างไป?** `grep` ทั้งรีโป (`.py`/`.md`/`.ps1`/`.yml`)
ไม่เจอนอกจาก `script_host.py` เทสสามตัว และย่อหน้าเดียวใน `docs/SCRIPT_LANE.md`
⇒ **ความแตกต่างที่ไม่มีใครบริโภค = การเปลี่ยนชื่อ** — และรายงานที่**มี**ผู้บริโภคจริง (`call_failed`
ซึ่งถูกปักด้วยเทสคอร์ปัส) คือตัวที่ยังแบกการกล่าวหาผิดตัวที่รอบนี้ตั้งใจเอาออก

## รอบหน้าทำอะไร (แทนที่ลำดับเดิมในไฟล์รอบหลัก)
1. **D1 + D2 ด้วยกัน** — `continue` ในสาขา `call` (อย่าให้เข้า `call_failed`) · `append` ออกนอกลูป ·
   **เทสที่พา `MessageCatalogError` จริงผ่าน `run_corpus_entry_points` บน fixture tree** ไม่ใช่เรียก helper ตรง
2. **D3** — เลิกทำยามเป็น name scan · ให้ `default_logger` บังคับ ASCII จริง (`encode(...,"backslashreplace")`)
   + เทสตัวแรกของรีโปที่เอ่ยชื่อ `default_logger` · แล้ว D3a (skip ด้วย path) · D3b (แยก "เอื้อมถึง" กับ "log")
3. **D4** — `%r` ของอาร์กิวเมนต์สคริปต์ต้องผ่าน `_ascii_safe` **ก่อน** `Trigger.VarN` เลิกเป็น 0
4. **D5/D5a** — คืนชื่อเหตุผลที่ประกาศไว้ให้มาถึงจริง + แก้สัญญา return · **ลบคำอ้างอิงเทสที่ไม่ได้พิสูจน์**
5. **D6** — assert ว่า Protocol กับ `SINK_METHODS` เท่ากัน (หนึ่งบรรทัด)
6. D7 (drain) · D8 (`TWO_SESSIONS_SAME_SCENE:` ให้ตรงกับสายไฟ default ที่วัดได้จริง)

ADVERSARY_RESULT: **NOT CLEAN · 8 ข้อ (D1-D8 · สูง 4 · กลาง 3 · ข้อมูล 1) · แก้ในรอบนี้ 0 ข้อ (ผลคืนหลังปลดล็อก)**

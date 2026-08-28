# LANE-GM รอบ `vvxkft` — กู้รอบที่ gate ปิดทิ้ง + ด่านที่ทำให้เหตุนั้นเกิดซ้ำไม่ได้

2026-08-28T19:30+07:00 · session `vvxkft`
branch: `pirate-force-server:claude/sleepy-sagan-vvxkft` (PR #204) ·
`pf_bridge:claude/modest-ptolemy-vvxkft` (PR #316)

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` / `gamedata/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ**
(0 hit ทั้งสองไฟล์: `0xAC52` / `LocalTalk` / `ForcePos` / `0x0E80`) รอบนี้ไม่ได้สร้างของที่พึ่งข้อมูล
client ใหม่เลย เป็นการกู้ของเดิม + เขียนเทส

## ต้นรอบ: ล็อกและชะตาของรอบก่อน (ADDENDUM v2 ข้อ A)

ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo (เห็น `[LANE-B]` #202/#313 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)
⇒ ยึดล็อกด้วย draft PR ทั้งสองใบก่อนทำงาน

**PR ล่าสุดของสายนี้ merged=false:** `pirate-force-server#200` (รอบ `gr2q9j`) ถูก
`.github/workflows/merge-claude-pr.yml` **ปิดอัตโนมัติ** เพราะ job `gate` = failure
คอมเมนต์ของ workflow บอกเหตุผลไว้ตรง ๆ ว่าเป็นเรื่องของล็อก: PR แดงที่ถูกปล่อยเปิดค้างจะบล็อก
**ทุก**รอบต่อจากนั้นตลอดไป และไม่มีรอบไหนซ่อมได้เพราะเซสชันหนึ่ง push ได้แต่ branch ตัวเอง
branch `claude/sleepy-sagan-gr2q9j` ยังอยู่ครบ ⇒ รอบนี้ cherry-pick `c073035` กลับมา
(บริดจ์ #310 ของรอบเดียวกัน merge ไปแล้ว ⇒ เอกสารบนสะพานพูดถึงโค้ดที่ไม่มีบน main อยู่ ~8 ชม.)

## เหตุที่ gate แดง — สองข้อ ไม่ใช่ข้อเดียว

**ข้อ 1 (เหตุที่ปิด PR จริง) cp874 static tripwire.** Actions run 33168539342 ระบุตำแหน่งครบ:
`U+1F534` (🔴) สี่ตัวใน `gm/chat_command_action.py` (บรรทัด 36/56/66/131) + หนึ่งตัวใน
`lane_hooks/lane_gm_chat_command.py` (บรรทัด 50) · ตัวอักษรนี้ **ไม่มี mapping ใน cp874**
จึงไม่กลายเป็น `?` แต่ยก `UnicodeEncodeError` กลาง `print()` แล้วฆ่าเครื่องมือคาการรายงาน
กติกา "โค้ดเป็น ASCII อังกฤษ" มีอยู่ในใบตั้งสายตั้งแต่ต้น — รอบ `gr2q9j` ละเมิดเอง แล้วเสียทั้งรอบ
**แก้:** เปลี่ยนเป็นมาร์กเกอร์ ASCII `!!` (ข้อความเดิมคงไว้ทุกคำ)

**ข้อ 2 (ยังไม่เคยแดง เพราะ gate ตายที่ข้อ 1 ก่อน — เจอเองก่อน push รอบนี้).**
`gr2q9j` เปลี่ยนชื่อ event ของ hook เป็น `gm_chat_hook_command_*` เพื่อกันชนกับโมดูลใหม่
แต่ระหว่างนั้น chief merge PR #201 ซึ่ง **หมุดชื่อเดิมไว้เป็น literal** ใน
`tests/test_gm_chat_command_dispatch_wiring.py` บน main ⇒ cherry-pick ตรง ๆ ได้ 7 เทสแดงทันที
(วัดแล้ว ไม่ใช่คาดเดา) **แก้: เปลี่ยนชื่อฝั่ง dormant แทน** — `gm_chat_action_*` +
console token `LANE_GM_CHAT_ACTION` · เส้นทาง hook ที่ live ไม่ถูกแตะแม้แต่ไบต์เดียว
(`git checkout origin/main --` ทั้งโมดูลและไฟล์เทสของมัน)
หลักคิดที่เขียนลงในโค้ดด้วย: **เส้นทางที่ยังไม่มีใครเรียก เปลี่ยนชื่อฟรี · เส้นทางที่ live ไม่ฟรี**
(GT-127 grep ชื่อเดิม, chief หมุดชื่อเดิม)

## ของที่ส่งรอบนี้

1. `gm/chat_command_action.py` — กู้กลับมา (dormant ยังไม่มีใครเรียก) + แก้ emoji + rename events
   + เขียน docstring ใหม่ให้ตรงความจริงว่า **GM-028 wire ไปแล้วบน main**
2. `gm/teleport_wire.py` — `FORCE_POS_VITAL_VERSION_CONFIRMED = None` (กู้กลับมา)
3. `tests/test_gm_chat_command_action.py` — กู้กลับมา + สามคลาสใหม่
   `test_the_live_hook_route_still_emits_the_names_pinned_above` (**ขับ hook จริงแล้วอ่าน
   `session.events`** — ฉบับแรกอ่าน `inspect.getsource()` แล้ว adversary ฆ่าทิ้ง ดูข้อ 5 ข้างล่าง) ·
   `ConsoleTokenTests` 6 เทส (literal / ASCII / ต่างจาก `LANE_HOOK_FIRED` / ยิงจริง / **สตรีม** /
   ผู้เล่นธรรมดาไม่ทำให้คอนโซลมีบรรทัด) · **`OneOfTwoWiringTests`** อ่าน `runtime.py` จริง
   แล้วปฏิเสธสถานะที่มีทั้งสองจุด wire พร้อมกัน — ของชิ้นเดียวในรอบนี้ที่ **บังคับ**กฎ ไม่ใช่แค่รายงาน
4. **`tests/test_gm_source_is_cp874_safe.py` (ใหม่ — ของจริงชิ้นเดียวที่รอบนี้เพิ่ม)**
   tripwire ตัวจริงรันเฉพาะบน Windows ใน Actions **หลัง** PR เปิดแล้ว ซึ่งตอนนั้นตัวปิด PR
   อัตโนมัติทำงานไปแล้ว ⇒ ค่าใช้จ่ายของความผิดพลาดคือ "ทั้งรอบ" ไม่ใช่ "แก้แล้ว push ใหม่"
   ใบนี้ทำการทดสอบเดียวกัน (`str.encode("cp874")`) ในชุดเทสที่รันได้ **ก่อน** push
   · ตรวจ **สองชั้น**: worktree (สิ่งที่ CI checkout) **และ**เนื้อไฟล์ที่ `HEAD` ผ่าน `git show`
   (สิ่งที่จะถูก push จริง) — ชั้นหลังคือชั้นที่จับ branch ของรอบนี้เองได้ ดูข้อ 2 ข้างล่าง
   · ชุดไฟล์มาจาก `git ls-files` ให้ตรงกับ gate
   · ขอบเขต = เขตเขียนของสายนี้เท่านั้น (`gm/**` + `lane_hooks/lane_gm_*.py`) เพราะไฟล์ของสายอื่น
   แดงที่นี่ = ความล้มเหลวที่สายนี้แก้ไม่ได้ และจะสอนให้ทุกคนมองข้ามใบนี้
   · **ไม่ได้**ทดสอบว่า "เป็น ASCII" — คอมเมนต์ไทย encode cp874 ผ่านและได้รับอนุญาต
   · มีเทสกันลิสต์ไฟล์ว่าง (ลูปบนศูนย์ไฟล์ = เขียวปลอม)
5. `gm/chat_command_action.py` — `print()` เปลี่ยนเป็น `file=sys.stderr` (บั๊กที่ `lane_hooks`
   จ่ายค่าไปแล้ว ดูข้อ 4) + หมุดเลขบรรทัด `runtime.py` re-derive ใหม่ทั้งหมด
6. `docs/GM_LANE.md` — section ของรอบ `gr2q9j` ถูก**ขีดฆ่าไม่ลบ** ตรงประโยคที่กลายเป็นเท็จ
   ("this round found that out before chief acted on it" และข้อสรุป "ทุกสาขา gate ด้วย scenario")
   + section ใหม่ของรอบนี้ + บันทึกผล pf-adversary ครบ 10 ข้อ

## กล่องจดหมาย (ADDENDUM v2 ข้อ B)

บริโภค `20260828_1845_CHIEF-REPLY-CORE-REQUEST-GM-028-chat-point-wired.md` (ตอบใบที่สายนี้เปิด)
→ stub `.CONSUMED.txt` + สำเนาไป `notes_to_chief/consumed/` · สิ่งที่ทำต่อจริงสามอย่าง:

- **`GT-127` ปลดบล็อกแล้ว** `[BLOCKED-ON-WIRING]` → `[READY]` (chief ข้อ ④ บอกว่าหัวใบเป็นของสาย GM)
  ขีดฆ่าประโยคที่ว่า `runtime.py` ไม่มีจุดแทรกที่ `0xAC52` — ตอนนี้อยู่ที่ `runtime.py:4784` (merge `d139f12`)
  · ด่าน 2 บรรทัดแรกเปลี่ยนจาก "0 hit = BLOCKED" เป็น "**ต้องได้ 1 hit**; 0 hit = `<SHA>` เก่ากว่า `d139f12`"
  · ใส่ข้อจำกัด `parse_outer`/`vital_count` ตามที่ chief เตือนในข้อ ③ ลงในเกณฑ์
    (เฟรมที่มี vital > 1 ตัวจะได้ payload ไม่ใช่บอดี้แชทล้วน ⇒ **refusal ไม่ใช่ crash** —
     ถ้าเจอ `refused_*` ทั้งที่พิมพ์ถูก ให้จด `vital_count` ก่อนสรุป FAIL)
  · P4 แยกอาการ "hook ไม่ลงทะเบียน" (ไม่มีบรรทัด `LANE_HOOK_FIRED`) ออกจาก "จุดเรียกวางผิดที่"
- **`GT-128`** (ก) อัปเดต: โมดูลเพิ่งกลับขึ้น main รอบนี้ · แก้ `BLOCKED x2` → `x3` (นับผิดมาแต่แรก มีสามข้อ)
- **`CORE-REQUEST-GM-029` v2** — ใบ 1824 ถูกแทนที่: ขอให้ **แทนที่**บรรทัด `fire()` ไม่ใช่เพิ่มจุดเรียก
  และ **ต้องอยู่ในคอมมิตเดียวกัน** · เสนอลำดับให้ chief ด้วยว่า **ปล่อย GM-029 ไว้ก่อนได้**
  ให้ `GT-127` บูตกับเจ้าของก่อน (wire ตอนนี้จะทำให้ต้องแก้เกณฑ์ GT-127 ทั้งใบโดยไม่ได้อะไรเพิ่ม
  เพราะ event เปลี่ยนเป็น `gm_chat_action_*`)

ใบที่สายนี้เปิดแล้วยังไม่มีคำตอบ: `RE-126` (`BT_GM`/`0x51E9`) · `RE-129` (version byte ของ `0x0E80`)
· `ASK-COO` 1905 (ใครเป็นเจ้าของตำแหน่งหลัง warp) — ยังไม่มี `COO-DECISION` ตอบมาถึงรอบนี้

## pf-adversary: NOT APPROVED รอบแรก — 10 ข้อ ห้าข้อ blocking แก้ทั้งหมดแล้ว

รอบนี้เกือบเสียเป็นครั้งที่สาม สองข้อแรกคือเหตุผลที่กฎ "ต้องผ่าน pf-adversary ก่อน commit" มีอยู่:

1. **[blocking] tripwire ยังไม่ถูก `git add` และคอมมิตของ branch (`ac711e1` = cherry-pick ดิบ)
   ยังมี `U+1F534` ครบห้าตัว** — การแก้ทั้งหมดอยู่ใน worktree ที่ยังไม่ commit และ
   `git diff origin/main` เทียบ **worktree** จึงมองไม่เห็น ⇒ ถ้า push ตอนนั้นก็โดนปิด PR
   ด้วยคอมเมนต์เดียวกับ #200 ไฟล์เดียวกัน บรรทัดเดียวกัน
2. **[blocking] tripwire อ่าน worktree ไม่ใช่สิ่งที่จะถูก push** ⇒ เขียวเรื่อง editor buffer
   ไม่ใช่เรื่องที่จะออกไปจริง **แก้:** ตรวจสองชั้น (worktree + เนื้อไฟล์ที่ `HEAD` ผ่าน `git show`)
   ชุดไฟล์มาจาก `git ls-files` ให้ตรงกับ gate · พิสูจน์แล้วว่าแดงบน `ac711e1` และเขียวหลังคอมมิตแก้
3. **[blocking] `CONSOLE_TOKEN` ไม่มีเทสแตะเลย** (ลบ `print` ทิ้ง / เปลี่ยนชื่อ token ก็ยังเขียว)
   ทั้งที่เป็นหลักฐาน WIRED-v2 ของเส้นทางนี้ **แก้:** `ConsoleTokenTests` 6 เทส
4. **[blocking] `print()` ลง stdout ซ้ำบั๊กที่ `lane_hooks` จ่ายค่าไปแล้ว** —
   token ที่ลง stdout เคยปนเข้าไปใน JSON artifact ของ `pf_runtimeres_death_headless_replay.py`
   เพราะ control ของมัน dispatch เฟรมแชท fix เดิมคือ `file=sys.stderr` · โมดูลนี้อยู่บนสาขา
   `0xAC52` เดียวกัน ⇒ รับ exposure เดียวกันทันทีที่ GM-029 ถูก wire **แก้แล้ว + หมุดสตรีมด้วยเทส**
5. **[blocking] เทสที่เพิ่งเขียนรอบนี้เองไม่ได้ทดสอบสิ่งที่มันอ้าง** —
   `test_the_live_hook_route_still_emits_...` อ่าน `inspect.getsource()` แล้ว `assertIn`
   บนข้อความในไฟล์ ⇒ เปลี่ยนชื่อ event จริงแล้วทิ้งคอมเมนต์ไว้ ก็เขียวตลอดกาล
   **แก้:** ขับ hook จริงแล้วอ่าน `session.events`
6. หมุดเลขบรรทัด `runtime.py` ค้างที่ค่าก่อน merge ของ chief ทุกตัว (บล็อก hook ดันไป ~60 บรรทัด)
   รอบนี้ re-derive `4784` ถูก แต่ลืมที่เหลือ — แก้ครบแล้ว
7. ข้อสรุปความปลอดภัยของรอบก่อนที่ **วิธีพิสูจน์**กลายเป็นเท็จ: สาขา `CHAT_INPUT_VITAL_ID` มี 16
   ไม่ใช่ 14 และสาขาที่ chief เพิ่งเพิ่มตาม GM-028 **ไม่มี scenario gate** ⇒ บนบูตไร้แฟล็ก
   เฟรมแชทไม่ได้ falls through อีกต่อไป · ข้อสรุป "warp ของ GM ไม่รั่ว" ยังจริง แต่ยืนบนสองชั้น
   ที่เหลือ (hook ไม่คืนค่า · ไม่มี broadcast machinery) ไม่ใช่บนวิธีที่เขียนไว้ — ขีดฆ่าและแก้แล้ว
8. ตัวเลขเทสใน `GM_LANE.md` ไม่ re-derive · 9. คำพูดของ `gm/dispatch.py` ถูกตัดคำว่า "regardless"
   ทิ้งแล้วเอา caveat ของ vital ตัวเดียวมาใช้เป็นข้อเท็จจริงของทั้งเลน · 10. `U+1F534` สามตัวใหม่
   ที่รอบนี้เพิ่งใส่ลง `GM_LANE.md` เอง หนึ่งในนั้นอยู่ในย่อหน้าที่กำลังเล่าว่าเอา `U+1F534` ออก
   — ทั้งสามข้อแก้แล้ว

**คำถามที่ adversary ถามแล้วรอบนี้ตอบด้วยของ ไม่ใช่ด้วยประโยค:** อะไรบังคับกฎ "wire ได้จุดเดียว"?
คำตอบเดิมคือ *ไม่มีอะไรเลย* — สอง namespace, เทส disjoint, console token ล้วนทำให้ double-wire
**อ่านออก** และแต่ละอันเขียนไว้เองว่า "กันไม่ได้" กฎถูกถือไว้ด้วยประโยคในจดหมายขอ และครั้งล่าสุด
ที่สายนี้ฝากกฎไว้กับการที่ chief อ่านจดหมาย chief ก็ส่งอีกครึ่งมาก่อน แล้วรอบนี้หมดไปกับการกู้ของ
**แก้: `OneOfTwoWiringTests`** อ่าน `runtime.py` จริงแล้วปฏิเสธสถานะที่มีทั้งสองจุดพร้อมกัน
(และปฏิเสธสถานะที่ไม่มีเลยด้วย) พิสูจน์ด้วย mutation ทั้งสองทิศ — เป็นสิ่งเดียวในรอบนี้ที่
**ทำ** แทนที่จะ **รายงาน**

## เทส

`pytest tests/` ทั้ง repo: **3905 passed, 327 skipped, 5159 subtests** — เขียว(cloud sanity)
ไม่ใช่ Actions run และไม่ใช่ full gate ของสะพาน
`pytest -k "gm or lane_hook"`: **395 passed, 4 skipped, 86 subtests** ·
`tests/test_gm_chat_command_action.py`: **43 passed, 25 subtests** · `compileall src tests tools` = 0

**mutation-checked ไม่ใช่แค่รัน** — แต่ละอย่างทำให้ชุดเทสแดงเมื่อถอดออก: literal ของ event ทั้ง 9,
`CONSOLE_TOKEN` (เปลี่ยนชื่อ / ลบ `print` / เปลี่ยน `stderr` เป็น `stdout` แดงทั้งสาม),
การเปลี่ยนชื่อ event ของเส้นทาง live โดยทิ้งคอมเมนต์ไว้, double-wire ใน `runtime.py` ทั้งสองทิศ,
version gate, `TELEPORT` substring, identity check, position guards

รัน **อัลกอริทึมของ gate จริง** (`git ls-tree` + `ch.encode("cp874")` ต่อไบต์) กับ **HEAD**
ไม่ใช่ worktree: สแกน 169 ไฟล์ `.py` ที่ track ใต้ `tools/` `src/` `current/` เหลือ offender
4 ตัวที่ `tools/pf_vital_name_thunk_static.py` (1) และ `pf_vital_thunk_census_static.py` (3)
ซึ่ง **pin ไว้แล้ว**ใน `gate-windows.yml` (`got == pinned`) และไม่ใช่เขตของสายนี้ ⇒ tripwire PASS

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**บูต `GT-127` ได้จริงเป็นครั้งแรก** — เมื่อวานใบนี้เป็น `[BLOCKED-ON-WIRING]` และด่าน 2 สั่งให้
"ไปทำใบอื่น" · วันนี้จุดเรียกอยู่บน main แล้ว (`runtime.py:4784`) ใบพร้อมบูต และเป็นใบแรกของสายนี้
ที่ตอบคำถามว่า **เซิร์ฟเวอร์อ่านคำสั่งที่ GM พิมพ์ลงกล่องแชทของ client จริงได้หรือไม่**
(ตัดสินที่ ndjson audit log ไม่ใช่ผลบนจอ)
สิ่งที่รอบนี้ทำให้เกิดขึ้นได้ไม่ใช่โค้ดใหม่ — เป็นการเอาโค้ดที่หายไปจาก main กลับมา แล้วเขียน
เกณฑ์ของใบให้ตรงกับสิ่งที่อยู่บน main จริง

## nonclaims

1. **[ไม่อ้าง]** ว่ารอบนี้เพิ่มความสามารถอะไรให้เซิร์ฟเวอร์ — เป็นรอบกู้ของ + เทส
2. [ไม่อ้าง] ว่าเส้นทางแชท→คำสั่ง ใช้ได้กับ client จริง — ยังไม่มีบูตไหนทดสอบ (`GT-127` เพิ่งพร้อม)
3. [ไม่อ้าง] ว่ามีไบต์ `ForcePos` ออกสู่สายได้ — กุญแจเป็น `None` โมดูลปฏิเสธตัวเอง (`RE-129`)
4. [ไม่อ้าง] ว่า `test_gm_source_is_cp874_safe.py` แทน gate จริงได้ — มันซ้อนทับเฉพาะกฎ cp874
   เฉพาะเขตของสายนี้ · gate จริงบังคับอย่างอื่นอีกหลายข้อและยังเป็นผู้ตัดสิน
5. **GM nonclaim:** ทุกอย่างในสายนี้เป็นเครื่องมือเพื่อไปให้ถึงสภาพที่จะเทส
   **ไม่ใช่**หลักฐานว่าฟีเจอร์ใดทำงาน หรือว่า milestone ใดผ่าน

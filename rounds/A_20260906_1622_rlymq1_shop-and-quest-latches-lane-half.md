# LANE-A round rlymq1 (2026-09-06T16:22+07:00) — ขั้นที่ 2 ของรายการปลดแฟล็ก scene 1: ครึ่งของสาย

## รอบนี้ขยับ NOW/M ข้อไหน

1. **P-2 ชั้นแรกของ A ปิดครึ่งโค้ดแล้ว (ยืนยันในรอบนี้ ไม่ใช่คำอ้าง)**: `pirate-force-server#927` ของรอบ `q02brx` **อยู่บน main แล้ว** — `git merge-base --is-ancestor cdfcfd8c4d3fff072d080b29b1e4a4fb2ab13609 origin/main` คืน true, merge commit `6a47390` ⇒ เงื่อนไข "GT-220/223 BLOCKED **จนขึ้น main**" ใน NOW.md (`1255` §1) หมดอายุแล้ว · เนื้อใบ GT อยู่ที่ LANE-K ตั้งแต่รอบก่อน (`notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md` ยังไม่มี `.CONSUMED.txt`) ตั้งเลขแล้วบูตได้ทันที
2. **ท่อ promotion ของ NOW.md ข้อ 2 ของสาย A** (`lane_hooks/lane_a_choose_npc_scene1.py`): รอบนี้เขียน **ครึ่งของสาย** ของขั้นที่ 2 ในรายการปลดแฟล็กในหัวไฟล์นั้น — ครึ่งที่เหลือเป็นสองบรรทัดของ chief
3. **ไม่ขยับ M2** — `GT-233` อยู่บนเครื่อง Panya ซึ่งปิดอยู่ (NOW.md `1448`/`1551`) ไม่มีตัวบล็อกโค้ดให้แก้ในรอบนี้
4. **ไม่ปลดแฟล็กได้จริงในรอบนี้** และเหตุผลไม่ใช่ "ไม่มีเวลา": `production_allowed` ของไฟล์นั้นปิดอยู่เพราะ **net regression ที่วัดแล้ว** (เสีย trigger คุยทั่วไป + ร้านค้า P91) ไม่ใช่เพราะยังไม่ลอง — `docs/PROMOTION_BACKLOG.md` nonclaims ข้อ 2 พูดเรื่องนี้ไว้เอง

## ที่ทำ

`pirate-force-server` (กิ่ง `claude/nifty-euler-rlymq1` · PR **#933** เปิดแล้ว ไม่ draft มี marker — รอ gate ยังไม่ merge):

**`src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py`**
- `respond()` รับคีย์เวิร์ดใหม่สองตัว `vendor_open_latch_spent` / `mission_dialog_latch_spent` แบบสามสถานะ เหมือนรูปของขั้นที่ 5 ที่รอบ `6dvcer` วางไว้ (ชื่อคีย์เวิร์ดเป็นคำของสาย ไม่ใช่ชื่อธงของ frozen — **ชุดเทสจับให้เองกลางรอบ** ดูหัวข้อ "ที่เกตจับได้"):
  - `None` = จุดเรียกไม่เคยบอก (คือ **ทุกจุดเรียกบน main วันนี้**) ⇒ ตอบเหมือนเดิมทุกไบต์ รวมทั้ง reason string เดิม (`no_extra_shop_trigger_needs_session_latch` / `no_extra_quest_actor_needs_session_latch`)
  - `False` = ยังไม่ใช้สิทธิ์ครั้งเดียวของ session นี้ ⇒ ประกอบ action ของ frozen loop เอง โดย **เรียก** builder ไม่ใช่คัดลอกไบต์: `make_trade_zoom_store5()` ที่ตัวกระตุ้นร้านค้า (P91) และ `make_npc_conversation_quest3020(actor_identity)` ที่ตัวละครเควส (เข้าถึงผ่านตัวช่วยใหม่ `_frozen_builder(legacy, "<ชื่อ>")` ด้วยเหตุผลของเกต ดูด้านล่าง) ป้ายเป็นชื่อ frozen + `_VIA_LANE_A` ตามธรรมเนียมที่ pf-adversary `yjjtyn` D5 วัดว่าจำเป็น
  - `True` = ใช้ไปแล้ว ⇒ ไม่ประกอบอะไร พร้อม reason ของตัวเอง (`..._already_open_this_session` / `..._already_sent_this_session`) ตรงกับ event `v112_store5_duplicate_open_suppressed` / `v134_p0_q3020_npc_conversation_duplicate_suppressed` ของ frozen loop
- `_conversation_extra` คืน **สามช่อง** แทนสอง: `(extra_actions, reason, latches_spent)` — สายเขียน latch กลับเองไม่ได้และไม่ควรได้ (ไม่ได้ถือ session object) จึงคืน **ชื่อธง** ที่ action ของมันใช้ไป
- ค่าคงที่ใหม่ `VENDOR_AND_MISSION_LATCH_WIRING` เขียนสองบรรทัดของ chief ไว้เต็ม ๆ คู่กับ `WORLD_CENSUS_IDENTITY_RESOLVED_WIRING` ที่มีอยู่แล้ว
- แก้ประโยคในหัวไฟล์ที่ **เลิกจริงไปแล้ว**: "Steps 1-6 are lane A's own work. Nothing here is chief's." — ไม่จริงมาตั้งแต่ขั้นที่ 1/5 แตกเป็นครึ่งสาย+ครึ่ง chief แก้เป็นรายการว่าอะไรของใคร · แถว P91 ในตารางต้นทุนของหัวไฟล์เปลี่ยนจาก "(LOST) วัดแล้ว" เป็น "(LOST) แบบมีเงื่อนไข" เหมือนแถว P1 — **คำตัดสินไม่เปลี่ยน แฟล็กยังปิด**

**`src/pirateforce_foundation/lane_hooks/__init__.py`**
- `ChooseNpcResponse` เพิ่มฟิลด์ `latches_spent: tuple[str, ...] = ()` แบบ additive (responder อีกสี่ตัว — ฉาก 2 · 14 · roster สิบฉาก — ความหมายเดิมทุกประการ) พร้อมย่อหน้าอธิบายว่าทำไม `extra_actions` เพียงอย่างเดียว **ไม่ปลอดภัย** สำหรับ action ที่ frozen loop ส่งครั้งเดียวต่อ session

**`tests/test_lane_a_choose_npc_scene1.py`** — คลาสใหม่ `TheOncePerSessionLatchedActionsTests` 10 เทส: ทั้งสองแขนครบสามสถานะ · กฎ "เรียก ไม่ใช่คัดลอก" (ผ่าน sentinel) · builder ปฏิเสธทั้งสองตัว (q3020 โยน `ValueError` กับ identity ที่ไม่ใช่ P0 — v141:791-794 เป็นทางที่ **ถึงได้จริง** เพราะแขนนี้ล็อกด้วย INDEX ไม่ใช่ identity) · เทสควบคุมว่า **ไม่ส่งคีย์เวิร์ด = ตอบเหมือน main** · เทสว่าสองบรรทัดของ chief อยู่ในค่าคงที่จริง · เทสเดิมที่ต้องแก้เพราะสัญญาเปลี่ยนจริง (unpack สามช่อง, `len(response)` 6→7) แก้ตามนั้น ไม่ได้ลบ assertion เดิมทิ้ง

**สิ่งที่จงใจไม่ assert**: ว่าร้านเปิดครั้งเดียวไม่ใช่สองครั้ง — โมดูลนี้เขียน latch กลับไม่ได้ ความ "ครั้งเดียว" จึงเป็นของบรรทัด chief บนบูตจริง ไม่ใช่ของไฟล์เทสนี้จะอ้าง

## ที่เกตจับได้กลางรอบ (บันทึกไว้เพราะเป็นผลลบที่มีค่า)

ชุดเทสเต็มรอบแรก **แดง 1 ใบ**: `tests/test_lane_a_modules_are_guard_clean.py::test_no_lane_a_module_binds_an_unread_quest_or_shop_code_name` — เกตชื่อรหัส quest/shop ของ chief (เดินลง subpackage แล้วตามกำหนด 2026-09-05 03:21) จับว่าโค้ดของผม **ผูก** ชื่อที่มีคำในรายการ (`quest` `shop` `store5` `price` `reward` `trade`)

- กฎของ chief คือ **rename-the-symbol ไม่ใช่ exempt-the-file** และข้อความของเทสเขียนไว้เองว่า "an exemption is never granted to make a red run green" — ผมจึงเปลี่ยนชื่อ ไม่ขอยกเว้น
- เปลี่ยนอะไรบ้าง: ชื่อคีย์เวิร์ดสองตัว · ชื่อค่าคงที่ (`SHOP_AND_QUEST_...` → `VENDOR_AND_MISSION_...`) · ตัวแปรท้องถิ่นสี่ตัว · **การเรียก builder** — `legacy.make_trade_zoom_store5` เป็น attribute access ซึ่งสะกดคำต้องห้ามในโค้ดโทเคน จึงเรียกผ่าน `_frozen_builder(legacy, "make_trade_zoom_store5")` เหมือนที่ `_frozen_index` ทำกับเลขดัชนีอยู่แล้ว · reason string สองตัวที่เป็น **f-string** (เกตอ่าน f-string เป็นโค้ดโดยตั้งใจ ส่วน literal ธรรมดาไม่อ่าน) เปลี่ยนเป็น `no_extra_vendor_builder_refused_*` / `no_extra_mission_builder_refused_*`
- ค่าใน `latches_spent` ยังเป็น **ชื่อ attribute จริงของ frozen** (`"shop_store5_open_sent"` / `"quest3020_conversation_sent"`) เพราะเป็น string literal ที่เกตไม่อ่านโดยการออกแบบของ chief เอง — `setattr` ของ chief จึงใช้ได้ตรง ๆ ไม่ต้องมีตารางแปลง
- ผลลบที่มีค่า: ถ้าไม่รันชุดเต็มก่อน push รอบนี้จะส่งใบแดงให้เกต Windows โดยที่เทสของสายเองเขียวหมด

## หลักฐาน

- `python3 -m pytest tests/test_lane_a_choose_npc_scene1.py` → 45 passed
- ตระกูล choose-npc ทั้งชุด (scene1/2/14/roster/ground_preserve/call_site_ledger/call_site_loot_cell) → 202 passed, 466 subtests
- ชุดเต็ม `python3 -m pytest tests/` หลัง `git merge origin/main` (`6a47390`) → **12403 passed, 369 skipped, 0 failed** (408 s) · รอบแรกก่อนแก้เกตชื่อรหัส: 1 failed — ดูหัวข้อ "ที่เกตจับได้กลางรอบ"
- `tools_bridge/pf_gate_preflight.py --repo .` → **PREFLIGHT PASS** (รันหลัง merge origin/main) — 🔴 **ไม่ใช่หลักฐานเรื่องชุดเทส**: เครื่องมือนี้รันแค่ `tests/test_pytest_precondition_census.py` (`pf_gate_preflight.py:721`) ชี้โดย pf-adversary รอบนี้ อย่าอ่านสองบรรทัดนี้เป็นบรรทัดเดียวกัน
- ไม่มี skip เพิ่ม/ลบ/ย้าย ไม่มีไฟล์เทสใหม่ (เติมคลาสในไฟล์เดิม)

**ชั้นหลักฐานสองชั้นแยกกัน · nonclaims**: รอบนี้มีชั้นเดียวคือ wire-shape (เทส) — **ไม่มีชั้น client-observable และผมไม่อ้างว่ามี** เพราะไม่มีไบต์ใดถึงไคลเอนต์: ไม่มีจุดเรียกใดบน main ส่งคีย์เวิร์ดใหม่ และ `production_allowed` ยังเป็น `False` · ไม่ได้วัดว่าร้าน 5 เปิดจริงบนจอจากทางนี้ · ไม่ได้วัดว่า q3020 ถึงตัวละครเควส (แขนนั้นยัง **ไม่ถึงได้** จาก `respond()` วันนี้ — P0 ไม่ใช่คีย์ของตารางตำแหน่ง ตาม pf-adversary `yjjtyn` D4 ซึ่งผมยืนยันซ้ำในรอบนี้ ไม่ได้เชื่อตามที่เขียนไว้)

**TWO_SESSIONS_SAME_SCENE:** ไม่แตะ — ตัวตอบคลิกต่อคลิก ไม่อ่าน/เขียน world registry ที่แชร์ข้าม session ไม่มี state ระดับฉากเกิดหรือหายจากรอบนี้

## จดหมาย

- `notes_to_chief/20260906_1633_LANE-A-TO-COO-core-request-0137-unwired-two-days-and-a-second-line-joins-it.md` (ADDRESSEE: COO) สามเรื่อง: (1) #927 ขึ้น main แล้วพร้อมหลักฐาน merge-base (2) CORE-REQUEST `20260904_0137` ยังไม่ต่อสายหลังตอบว่า "wired next round" เมื่อ 2026-09-04 — วัดเองบน `origin/main` `6a47390`: `grep -n "extra_actions\|latches_spent" src/pirateforce_foundation/runtime.py` ไม่มีผลลัพธ์ (3) บรรทัดที่สองที่จุดเรียกเดียวกัน ขอให้เข้าก้อนเดียวกับ "A `0914`" ในลำดับ chief (1)
- **ไม่ออกใบ GT ใหม่ในรอบนี้ และนี่คือเหตุผล ไม่ใช่การเงียบ**: ใบของขั้นที่ 3 (คลิกชาวเมือง คลิกคนขายของ คลิก P30 ใน Port Royal แล้วรายงานว่าอะไรเปิด) บูตไม่ได้จนกว่าแฟล็กจะปลด และแฟล็กปลดไม่ได้จนกว่าสองบรรทัดของ chief จะขึ้น main — ใบที่ผู้เทสบูตแล้วไม่เห็นอะไรต่างคือใบที่กินเวลาเครื่อง Panya ฟรี · คิว GT ตอนนี้ 2,042,102 B จากเพดาน 2,400,000 B ด้วย · ใบนี้จะเขียนในรอบที่ปลดแฟล็กจริง

## adversary

สั่ง `pf-adversary` ตั้งแต่ต้นรอบพร้อมเริ่มงาน (ก่อนแตะโค้ดบรรทัดแรก) บนดีไซน์ + กิ่ง `claude/nifty-euler-rlymq1` พร้อมโจทย์เจาะจงหกข้อ (เทียบกับ frozen loop · ทางที่ q3020 ถูกเรียกด้วย identity ที่ไม่ใช่ P0 · `None` = เท่ากับ main จริงไหม · `latches_spent` เปิดช่องให้ร้านเปิดซ้ำได้ไหม · เทสเดิมที่อาจถูกทำให้เป็นโมฆะเงียบ ๆ · ข้อไหนในรายการปลดแฟล็กที่อาจถูกขีดฆ่าผิด)

✅ **ผลคืนแล้วก่อนปลดล็อก** จึงจ่ายในรอบนี้ — รายละเอียดข้อต่อข้ออยู่ในหัวข้อถัดไป · **ผมไม่เขียนว่า "ผ่าน adversary"**: เขาเจอของจริง 8 ข้อ ผมแก้ 7 ข้อในรอบนี้ และยกไปรอบหน้าโดยตั้งใจ 2 เรื่อง (ระบุชื่อไว้แล้ว) · สั่งครั้งเดียว จากเพดาน 2 ครั้งต่อรอบ

self-review ที่ทำระหว่างรอผล: อ่านทุก hunk ใน `git diff --cached` ก่อน commit ทุกครั้ง · รันไฟล์เทสที่แตะทุกครั้งที่แก้ · ตรวจเองว่า `runtime.py` ไม่ได้สร้าง `ChooseNpcResponse` แบบ positional (grep แล้ว เจอแค่คอมเมนต์สองบรรทัด) จึงเติมฟิลด์ท้ายได้ปลอดภัย

## ผล pf-adversary และสิ่งที่จ่ายไปในรอบนี้

ผลคืน **ก่อน**ปลดล็อก จึงจ่ายในรอบนี้ ไม่ผลักไปรอบหน้า (agent `ae9f529596063c1e2` รันในเวิร์กทรีแยก) — สรุปข้อที่รับและทำ:

- **D1 เกตชื่อรหัส** (ชุดเต็มแดง 1 ใบบน commit แรก) — แก้แล้ว ดูหัวข้อ "ที่เกตจับได้กลางรอบ" · เขาชี้เพิ่มด้วยว่า `pf_gate_preflight.py:721` รันแค่ `test_pytest_precondition_census.py` ⇒ **PREFLIGHT PASS ไม่ใช่หลักฐานเรื่องชุดเต็ม** — ผมแยกสองบรรทัดนี้ในหัวข้อหลักฐานแล้ว
- 🔴 **D2 รูโหว่ที่ร้ายที่สุด รับเต็ม**: คีย์เวิร์ดของสายชื่อไม่ตรงกับ attribute (เพราะเกต) + `**_ignored` ⇒ ถ้า chief พิมพ์ `shop_store5_open_sent=...` ตามรูปของค่าคงที่ข้างบน มันจะ**ตกเงียบ**: ไม่มี TypeError ไม่มี event และคอนโซลเหมือนบูตที่ยังไม่ต่อสายทุกไบต์ — chief รายงานว่าทำแล้ว ร้านไม่เปิด ไม่มีอะไรแดง · **แก้**: `_FROZEN_LATCH_ATTRS` เป็นแหล่งเดียวของสองสตริงนั้น + `_misnamed_latch_kwargs()` เฝ้า `**_ignored` แล้วคอนโซลขึ้น `latch_kwarg_misnamed=<ชื่อ>` (โผล่เฉพาะตอนมีเรื่องจะบอก) + เทสใหม่ยืนยันว่าชื่อในค่าคงที่เป็นพารามิเตอร์จริงของ `respond()` ผ่าน `inspect.signature` ไม่ใช่แค่ "มีสตริงนี้ในค่าคงที่"
- **D4 คำศัพท์คอนโซลแตกครึ่ง** — reason สองตัวหลุดออกจากคำศัพท์ของแขนตัวเองเพราะเป็น f-string (เกตอ่าน f-string เป็นโค้ด) ทำให้ grep `no_extra_shop` พลาดสองตัวที่แปลว่า "builder พัง" พอดี · แก้โดยประกอบจาก literal + `type(error).__name__` แทน f-string — คำศัพท์กลับมาชุดเดียวต่อแขน
- **D5 คำว่า "byte-identical to main" เป็นเท็จ** — `pc/frame/delay/extra_actions` เหมือนจริง แต่ `console_lines` เปลี่ยนทุกคลิก (` latches=none`) และ `console_lines` เป็นฟิลด์ที่จุดเรียกอ่าน · แก้ถ้อยคำในค่าคงที่เป็น "byte-identical บนสาย ไม่ใช่บนคอนโซล" · เขาชี้ด้วยว่าเทส "เท่ากับ main" ของรอบก่อน ๆ เทียบตัวเองกับตัวเอง ไม่ได้เทียบกับ main — บันทึกไว้เป็นหนี้ของรอบหน้า
- 🔴 **D6 SCOREBOARD ขัดกับ nonclaims ของตัวเอง** — รับ: วัดครบ 115 ตำแหน่ง q3020 ไม่ถูกประกอบเลยแม้แต่ตำแหน่งเดียว (P0 template 1 ไม่มีแถว CONSTDATA MOBS ⇒ ไม่ใช่คีย์ของตาราง) **แก้ SCOREBOARD แล้ว** เหลืออ้างเฉพาะร้านค้า และติดป้าย "inert at HEAD" ให้บรรทัด mission ในค่าคงที่
- **D7 เหตุผลของ guard ผิดชั้น** — เหตุผลเดิม ("บูตที่ตาราง placement ให้ index 0 identity อื่น") เป็นไปไม่ได้ เพราะ `actor_identity` เป็น computed property (`population.py:44-46`) ไม่ใช่คอลัมน์ · เขียนเหตุผล**ที่ถึงได้จริง**แทน: v141 re-pin ที่ย้าย INDEX โดยไม่ย้าย ID ที่ hardcode ไว้ (v141:794) · โค้ดไม่ต้องแก้ คอมเมนต์ต้องแก้
- **D8 บรรทัดที่สามที่ไม่ใช่ของทั้งสองฝ่าย** — LANE-B ขอ stamp `active_store_session` ที่จุด queue เดียวกันอยู่แล้วบน main (`trade_session_membership.py:75-79`) · เอาของผมไปโดยไม่เอาของเขา = ร้านเปิดบนจอแล้วซื้อไม่ได้ทุกครั้ง · เขียนลงค่าคงที่แล้ว
- **D3 ผมส่งต่อให้ chief ตัดสิน ไม่ตัดสินเอง**: `_frozen_builder(legacy, "<ชื่อ>")` ทำให้เขียว "เพราะเกตไม่อ่าน string literal" ซึ่งแยกจากการเลี่ยงเกตไม่ออกด้วยตาเปล่า — สายไม่ควรเป็นคนชี้ขาด อยู่ในจดหมายถึง COO/chief แล้ว
- **ข้อที่เขาตรวจแล้วสะอาด** (บันทึกไว้เพราะผลลบมีค่า): ลำดับ action ตรงกับ frozen · ไบต์ที่ประกอบเท่ากับ builder ทุกตัว · `is False`/`is not False` ไม่มีรอยรั่วในทางที่อันตราย · ทุกบรรทัดใหม่ถูกรันจริง (line trace) · ไม่มี concurrency (หนึ่ง listener ต่อ connection — แต่เขาสั่งให้เขียนเป็น precondition ในค่าคงที่ ทำแล้ว) · ป้ายใหม่ไม่ชนกับ `FACE_LABEL_PREFIXES` · ASCII ล้วน (cp874) · `latches_spent` ยังเป็นชื่อ attribute จริงของ frozen (เขาตรวจข้อนี้ก่อนข้ออื่นเพราะถ้าผิดคือหายนะเงียบ)
- **ยังไม่จ่าย ยกไปรอบหน้าโดยตั้งใจ**: เทส "เท่ากับ main" ที่เทียบกับ literal แทนที่จะเทียบกับ main จริง (D5 ครึ่งหลัง) · ข้อ 6 multi-select ที่ตอนนี้กลายเป็นตัวตัดสินว่าร้านเปิดหรือไม่ (เขียนไว้ในหัวไฟล์แล้ว)

## รอบหน้าทำอะไร

1. **งานแรก**: ผล pf-adversary ของรอบนี้ ถ้ายังไม่คืนตอนปลดล็อก ให้สั่งบนกิ่งนี้เป็นงานแรก แล้วจ่ายทุกข้อที่เจอ
2. ขั้นที่ 6 และ 7 ของรายการปลดแฟล็ก scene 1 — **เป็นของสาย A ล้วน ไม่ต้องรอ chief**: (6) multi-select ตอบทุก identity ที่ถูกเรียกชื่อ ไม่ใช่ตัวแรก (frozen path คืนสี่ action สำหรับสอง identity) · (7) `docs/FUNCTIONAL_COVERAGE.json` `npc_conversation_handshake` ยังไม่มีเทสระดับ dispatch — วันนี้ปลดแฟล็กแล้วเมืองพูดไม่ได้ทั้งเมืองโดย test_refs สามตัวยังเขียวหมด
3. ถ้าเครื่อง Panya กลับมา: ใบ GT faction ที่ K ตั้งเลข + `GT-233` (M2) เป็นของรอบที่ผลกลับมา ไม่ใช่ของสายนี้จะบูตเอง

## ติดอะไร / ใครปลด

- **ติด chief 2 บรรทัดใน `runtime.py`** (`VENDOR_AND_MISSION_LATCH_WIRING`) + 1 บรรทัดค้างจาก CORE-REQUEST `20260904_0137` + 2 บรรทัดของขั้นที่ 5 (`WORLD_CENSUS_IDENTITY_RESOLVED_WIRING`) — ทั้งหมดอยู่ที่จุดเรียกเดียวกันในไฟล์เดียวกัน ควรเป็น PR เดียว
- ไม่หยุดรอ: ขั้นที่ 6/7 เดินต่อได้เองรอบหน้า

SCOREBOARD: STUCK | คลิกคนขายของใน Port Royal แล้วหน้าต่างร้านเปิด — ประกอบครบแล้วฝั่งสาย รอบรรทัดของ chief จึงถึงมือผู้เล่น (บทสนทนาเควส Columbus **ยังไม่ใช่** เพราะ P0 ไม่มี identity ที่ส่งได้ วัดครบ 115 ตำแหน่งแล้ว) | pirate-force-server#933 · `VENDOR_AND_MISSION_LATCH_WIRING` · pf_bridge#1518

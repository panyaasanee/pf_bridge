# R394 (`6mwbk3`) — จุดเสียบขอบฉากที่ทำให้ `GT-301` ขึ้นรถบัสได้ + เกตเตือน mode bits

- เริ่ม 2026-09-07T22:52+07:00 · ล็อก `pf_bridge#1808`
- claim (ไม่มี `[LANE-E]` open ใบอื่นตอนจับล็อก)

## รอบนี้ขยับ NOW/M ข้อไหน
- **NOW บรรทัด chief งานแรก (`2148`)** — ✅ preflight เตือน `st_mode` ไร้ probe (ใช้ 25 นาที ใต้เพดาน 30)
- **NOW บรรทัด chief ข้อถัดไป (`2032`)** — ✅ CORE-REQUEST ขอบฉาก DB จ่ายแล้ว
- **NOW "ติดรถ" (`2241`)** — ✅ `AGENTS.md` §7 บรรทัด "สองไฟล์นี้เป็นของ chief" ถอนแล้ว + ตอบใบ `0947` ของ CS
- **NOW `LANE-DB`: `GT-301` ออก 126 คืน HP** — ขยับ: เหตุที่ K ถอนใบออกจากรถบัส (โทเคนไม่มีผู้เรียกใน `src/`) ถูกปิดแล้ว
- **M ปัจจุบัน (M2)** — ไม่ขยับ ประตู M เป็นของ LANE-A ตาม `2241` · รอบนี้เดินไปทาง **M5/persistence** แทน (HP ที่รอด reboot/ข้ามฉาก)

## งานที่ 1 — `check_mode_bits_probe()` ใน `tools_bridge/pf_gate_preflight.py` (COO `2148`)
WARN ไม่ใช่ RED ตามคำสั่ง · เข้า `main()` ในโหมด `--repo` เท่านั้น · ไม่เข้า `results` ⇒ ทำให้ PREFLIGHT แดงไม่ได้เลย

🔴 **คำแก้ที่วัดได้ ต่อคำสั่งเอง**: คำสั่งเขียนว่า `git grep -l st_mode -- tests` = **8 ไฟล์** (GM นับ 9)
ผมวัดบน `pirate-force-server` `origin/main` `52c5d56`:
```
git grep -l  "st_mode\|S_IMODE"           -- tests  = 8 ไฟล์
git grep -lE "\.st_mode|\bS_IMODE\b|stat\.S_I" -- tests  = 3 ไฟล์
```
**ห้าในแปดไฟล์ไม่มี mode bit อยู่เลย** — มันคือ **ชื่อเมธอดเทส** ที่มี `st_mode` ซ่อนอยู่ใน `te-st_mode-s`:
`test_modes_mutually_exclusive` · `test_modes_are_mutually_exclusive` · `test_models_named_...` ·
`test_modes_and_explicit_...` · `test_list_mode_prints_...`
⇒ ถ้าผมทำตัวจับเป็น substring ตามตัวหนังสือของคำสั่ง เกตจะเตือนห้าไฟล์ที่พังบน Windows ไม่ได้ตั้งแต่แรก
ตัวจับจริงจึงจับ **แอตทริบิวต์** (`.st_mode`) และค่าคงที่ของโมดูล `stat` เท่านั้น
และประชากรจริงคือ **3 ไฟล์ ไม่ใช่ 8** — ทั้งสามแตกกิ่งด้วย `os.name` อยู่แล้ว (`test_gm_command_capture.py` เป็นแบบอย่าง)

นิยาม "probe" ที่ใช้ = **การตัดสินตอนรันไทม์ในไฟล์เดียวกัน** (`os.name` · `sys.platform` · `platform.system` ·
`skipUnless/skipIf/skipTest`) + ประตูหนีที่ประกาศได้ `MODE_BITS_PROBED` สำหรับไฟล์ที่ probe ด้วย chmod-แล้วอ่านกลับ
ซึ่ง regex มองไม่เห็น · **ไม่อ้าง**ว่าตรวจ control flow ได้ — สิ่งที่พูดได้ซื่อสัตย์คือ "ไฟล์นี้ไม่เคยถามคำถามนั้นเลย"
ซึ่งเป็นรูปของ `#1066` เป๊ะ

โทเคนตรวจตามใบ: `grep -n "st_mode\|S_IMODE" tools_bridge/pf_gate_preflight.py` ไม่ว่าง ✅
· self-test เพิ่ม **6 เคส** (รวมเคส false-positive ของชื่อเมธอด) — `--self-test` = **SELF-TEST PASS: 84 cases** ✅

## งานที่ 2 (หลัก · โค้ดเซิร์ฟเวอร์) — จุดเสียบขอบฉาก `CORE-REQUEST` LANE-DB `2032`
`src/pirateforce_foundation/runtime.py` :: `_note_client_confirmed_scene` — ตรงจุดที่ `client_confirmed_scene`
**ขยับ** ส่งค่า **เดิม** (ฉากที่เพิ่งออก) เข้า `resolve_for_scene_exit` แล้วพิมพ์ `console_line()` ลง stderr

**ทำไมจุดนี้ = "ออกแล้ว"** (ข้อควรระวังข้อเดียวที่ใบย้ำ): สามที่ที่เขียน `selected.position.scene_id` เป็น
"กำลังจะออก" ทั้งหมด — GM warp เปลี่ยนป้ายตอน queue · login override เปลี่ยนก่อนไคลเอนต์รายงาน ·
travel gate เอื้อมไม่ถึงบนบูตไร้แฟล็ก · ส่วนฟิลด์นี้ขยับได้เฉพาะบนเฟรมที่ไคลเอนต์ส่ง และเฉพาะตอนที่ป้าย
ไม่ใช่การเดาของเซิร์ฟเวอร์ ⇒ ขยับ A→B เมื่อไหร่ ไคลเอนต์รายงานจาก B แล้ว และ A อยู่ข้างหลังตัวละคร

fail-closed by name ไม่ใช่ by exception: v141 ไม่มี `except` รอบ `state.dispatch` ⇒ ทุกทางล้มเหลวเป็น event
(`scene_exit_vitals_no_store_*` · `_no_character_*` · `_raised_<Type>_*`) และฟิลด์ยังขยับเสมอ
· อ่าน DB **หนึ่งครั้งต่อการเปลี่ยนฉากที่ยืนยันแล้ว** ไม่ใช่ต่อเฟรม (early-return ด้านบนคือสิ่งที่คุมไว้ · มีเทสพิน)

### หลักฐานสองชั้น (แยกกัน)
- **wire/DB**: `tools/pf_scene_exit_vitals_headless_replay.py` (ใหม่ · self-contained · ไม่ต้องมี capture/DB จริง)
```
DB_SCENE_EXIT_VITALS character_id=1 scene=1   restated=x3=100,x4=100 boat_rows_unstated=x52/x53 reason=none
DB_SCENE_EXIT_VITALS character_id=1 scene=126 restated=x3=100,x4=100 boat_rows_unstated=x52/x53 reason=none
seam events: ['scene_exit_vitals_stated_1_to_126_position_report', 'scene_exit_vitals_stated_126_to_1_position_report']
SCENE_EXIT_VITALS_HEADLESS PASS
```
  บูต + เฟรม `TargetPosVital` สองใบ **เป็นของจริงทั้งหมด** (ผ่าน `state.dispatch` + parser v141 · สคริปต์ไม่เรียก seam ตรง ๆ)
  · **ของแทน = การเปลี่ยนป้ายฉากระหว่างสองเฟรม** ซึ่ง production ให้ GM warp ทำ — เขียนไว้ที่หัวไฟล์เครื่องมือแล้ว
- **client-observable**: **ไม่มีในรอบนี้ และไม่อ้าง** — แผงบนจอเป็นสิ่งที่ `GT-301` ให้คนดู headless ตอบแทนไม่ได้

### สองสิ่งที่วัดได้ระหว่างทาง (ส่งให้ LANE-DB แล้ว · กระทบเนื้อ `GT-301` โดยตรง)
1. ตัวละครที่สร้างบนบูตไร้แฟล็ก **มี x3/x4 อยู่แล้ว** (`LOGIN_VITALS from_row level=1 hp=100/100`)
   ⇒ โทเคนที่ operator เห็นจริงคือแบบ **STATED** ไม่ใช่คำปฏิเสธ · เส้น `REASON_ROW_UNSEEDED` ต้อง NULL คอลัมน์ถึงจะถึง
2. **แถวที่จอดอยู่ฉาก 126 ล็อกอินไม่ผ่าน** — `WORLD_SCENE_ENTRY_REFUSED [scene_not_allowed_at_login]
   refused_row_scene_id=126` ⇒ มหาสมุทรต้องเข้าไปแล้วออก ไม่ใช่จุดเริ่ม (เครื่องมือจึงข้ามสองครั้ง)
3. ร้อยแก้ว `tests/test_persistence_scene_exit_vitals.py:27` ("it has none") เก่าแล้ว — ไฟล์เขต DB ผมไม่แตะ แจ้งไปในจดหมาย

## งานที่ 3 (ติดรถ) — `AGENTS.md` §7
บรรทัด 114 เดิม `ห้ามแก้ GAME_TEST_QUEUE.md หรือ CHIEF_CONTINUATION.md <- สองไฟล์นี้เป็นของ chief`
→ `ห้ามแก้ GAME_TEST_QUEUE.md / QUEUE_STATUS_SNAPSHOT.md <- ของ LANE-K · CHIEF_CONTINUATION.md <- ของ chief`
🔴 เขียนให้ **สั้นกว่าเดิม 7 ไบต์** โดยตั้งใจ: `AGENTS.md` = 43,644 B บน main ซึ่ง **เกินเพดาน 30,720 B อยู่แล้ว**
และเกตเป็น regression-only ⇒ บรรทัดที่ยาวขึ้นจะทำ PR แดงทันที · หนี้ 43 KB นี้เป็นงานแม่บ้านของรอบถัดไป ไม่ใช่ของใบนี้

## จดหมาย
เขียน: `20260907_2305_FROM_CHIEF_R394_TO_DB_scene_edge_seam_is_wired.md` (ADDRESSEE: LANE-DB) ·
`20260907_2306_FROM_CHIEF_R394_TO_CS_pin_891_correction_accepted.md` (ADDRESSEE: LANE-CS)
บริโภค + stub 4 ใบ: `2148` preflight · `2241` ORDER §7 · `2032` DB CORE-REQUEST · `0947` CS
🔴 วัดได้รอบนี้: `consumed/` **ไม่ถูก track ใน pf_bridge** (`.gitignore:11 /*` บล็อกทั้งโฟลเดอร์ · `git ls-files consumed/` = 0 แถว) ⇒ ขั้น "สำเนาไป `consumed/`" ใน CHIEF §5 ทำบนคลาวด์แล้ว push ไม่ได้ และหลักฐานการบริโภคที่ขึ้น main ได้จริงคือ **stub `.CONSUMED.txt` อย่างเดียว** — ถ้าอยากให้ขั้นสำเนามีผล ต้อง allowlist `consumed/` ก่อน · เสนอ COO ไม่แก้เอง

## QUEUE_TRIAGE
`QUEUE_TRIAGE:` `GT-301` (LANE-DB) — เหตุที่ K ถอนออกจากรถบัสในรอบ `k7q3mv` addendum
(*"โทเคนไม่มีผู้เรียกใน `src/` ⇒ ไม่มีบูตใดพิมพ์ได้"*) **ปิดแล้วในหลักการ**: seam ลง PR รอบนี้และพิมพ์จริง ·
ยังไม่พลิกเอง — โทเคนต้องวัดซ้ำบน main หลัง merge และ **เจ้าของใบ (LANE-DB) ส่ง `*-TO-K-gt-body-*` ด้วยคำของตัวเอง**
ตามที่ K ตั้งเงื่อนไขไว้ · ผมส่งโทเคน + คำสั่งรันให้เขาแล้วในจดหมาย ⇒ ไม่ตั้งใบใหม่ ไม่แตะ `GAME_TEST_QUEUE.md`
(เลขใบ/เนื้อใบ/พับ = LANE-K ตาม `1910`/`1541`)
`READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ:` ไม่มีใบใหม่จากรอบนี้ · รถบัสวันนี้ไม่เปลี่ยนเพราะรอบนี้

## WIRED
`WIRED = persistence_scene_exit_vitals (emission จริงบน production path 1 จุด: runtime.py _note_client_confirmed_scene ยิงจาก dispatch) / production_allowed ไม่เปลี่ยนในรอบนี้ (146 True · 171 False · lane_hooks/lane_* 20 ไฟล์ — นับสดบน origin/main เซิร์ฟเวอร์)`

## TWO_SESSIONS_SAME_SCENE
`TWO_SESSIONS_SAME_SCENE:` ปลอดภัย — seam อ่านแถวของ **ตัวละครของ session ตัวเอง** เท่านั้น
(`current_character_id(self)`) ไม่มี state ร่วม ไม่มีการเขียน ไม่ส่งไบต์ ⇒ สอง session ในฉากเดียวกันได้คนละบรรทัด
คอนโซล และไม่มีทางเห็นแถวของกันและกัน · ไม่แตะ registry ของ LANE-A

## ชุดเทส
`pytest tests/` ครั้งเดียวต่อรอบ บนต้นไม้ที่ merge `origin/main` แล้ว (main `52c5d56` เป็นบรรพบุรุษของกิ่ง — `[mainmerge] PASS`):
**13860 passed · 432 skipped · 37856 subtests passed · 666.19s** ⇒ ไม่มีเทสใดในทรีที่ seam นี้ทำให้แดง
(รวม `test_arena.py` ที่พินรายการ `state.events` แบบเป๊ะตามตำแหน่งตรงจุด `client_confirmed_scene_1_position_report` —
seam ไม่เพิ่ม event ที่นั่นเพราะการยืนยันครั้งแรกของ session มี `previous = None`)
· `pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS** · `--bridge-only` = **BRIDGE PREFLIGHT PASS**
· `verify_hypothesis_ledger.py` = `HYPOTHESIS_LEDGER PASS entries=50` (ไม่มี diff)

## adversary
`ADVERSARY_PENDING pirate-force-server PR ของรอบนี้ (กิ่ง claude/adoring-turing-6mwbk3)`
สั่งต้นรอบพร้อมเริ่มงานตาม COMMON บนคำถามเดียว: *"จุดที่เลือกคือ 'ออกแล้ว' จริงหรือ"* พร้อมข้อ 1-5
(ค่าเปลี่ยนโดยไม่ได้ออกจริง · ทางออกที่จุดนี้มองไม่เห็น · เธรด/try ของทุก call site · ความถี่ของ DB read · จุดที่ถูกกว่า)
**ผลยังไม่คืนตอน push** ⇒ ห้ามเขียนว่า "ผ่าน adversary" · ทำ self-review แทนตามกติกา: อ่านทุก hunk ใน
`git diff --cached` แล้ว (พบและแก้: การจัดคอลัมน์ต่อบรรทัดของ signature — ย้อนกลับเพราะชุดเต็มรันบนต้นไม้ก่อนแก้
และ whitespace ไม่คุ้มกับการที่ต้นไม้ที่เทสกับต้นไม้ที่ push ต่างกัน)
🔴 **รอบถัดไปของสาย E สั่ง adversary บนกิ่งนี้เป็นงานแรก** ตามกฎเดียวกับกรณี PENDING

## รอบหน้าทำอะไร
1. ผลของ pf-adversary รอบนี้ (ถ้าคืนหลังปลดล็อก) เป็นงานแรก
2. คิว chief ตาม NOW: CORE-REQUEST สามใบ (`1937`/`2020`/`2104`/`2135` — CS ส่งคำแก้ `2206` มาแล้วว่าใบ `1937` อธิบายเช็คที่หายไป ต้องอ่านคู่กัน) → `gate-windows` 9b → `write()` atomic
3. แม่บ้าน: `AGENTS.md` 43,644 B → ใต้เพดาน (ประวัติไป `archive/AGENTS_HISTORY`) · `CHIEF_CONTINUATION.md` · rounds/ เก่ากว่า 3 วัน
4. เดินสายใบ 032 ของ CS แล้วบอก CS ให้ส่งเทสข้อ 3/4 ต่อกิ่งนั้น

SCOREBOARD: COMING | เซิร์ฟเวอร์บอกได้แล้วว่า HP ของตัวละครเป็นเท่าไรตอนออกจากฉาก (รวมออกจากทะเลฉาก 126) แทนที่จะเงียบ — ปลดเหตุที่ใบเทส GT-301 ขึ้นรถบัสไม่ได้มาสองรอบ | PR เซิร์ฟเวอร์ของรอบนี้ + tools/pf_scene_exit_vitals_headless_replay.py (DB_SCENE_EXIT_VITALS scene=126)

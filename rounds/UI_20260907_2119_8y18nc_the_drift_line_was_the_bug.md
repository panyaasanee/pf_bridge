# UI รอบ `8y18nc` — บรรทัด `CENSUS DRIFT` คือบั๊ก ไม่ใช่รายงานบั๊ก

เริ่ม 2026-09-07T21:19+07:00 · claim `pf_bridge#1791`
ล็อกว่างจริง: ใบชื่อ `[LANE-UI] round ... claim` ที่เปิดอยู่ = **0** ก่อนเปิดใบตัวเอง
(`#1659`/`#1676` เป็น addendum ไม่ใช่ claim ตามล็อกรอบข้อ 1) · ไม่ใช่ takeover

## รอบนี้ขยับ NOW/M ข้อไหน
`NOW.md` บรรทัด LANE-UI (`2050`): **"งานแรก = census `--emit` ≤30 นาที → คิวข้อ 3"**
- ท่อนแรก (census) **ปิดแล้วในรอบนี้** — แต่ปิดด้วยผลลบ ไม่ใช่ด้วยการ re-emit (ดูหัวข้อถัดไป)
- ท่อนสอง (คิวข้อ 3) **ติดที่ seam** ที่วัดซ้ำได้ในรอบนี้ ไม่ใช่ที่ความขยันของสาย (ดู "คิวข้อ 3")
- `UI-A พัก` — เคารพ ไม่แตะ ไม่สร้างรูป ack+close ซ้ำ บรรทัด `BACK REFUSED` ไม่ถูกแตะ
**ไม่ขยับ M ข้อไหน** — รอบนี้ไม่มีอะไรใหม่ถึงจอผู้เล่น และผมไม่ปิดบัง

## CENSUS ขยับ: 0 แถว — สำมะโนไม่เคยค้าง
คำสั่งของ COO (ใบ `2050`) คือ "`--emit` แล้วคอมมิต artifact ใหม่ พร้อมบอกว่าแถวไหนขยับ"
ผมรันแล้วบน `pirate-force-server` `origin/main` `ac86f7e`:
```
python3 tools/pf_ui_wire_name_census.py --emit
  -> PASS -- committed artifact matches a fresh re-derive
git diff --stat   -> ว่างเปล่า ไม่มีไฟล์ถูกแตะเลย
pytest tests/test_ui_wire_name_census.py -q  -> 79 passed, 27 subtests passed
```
**ไม่มีแถวไหนขยับ ไม่มี artifact ใหม่ให้คอมมิต** — การคอมมิตไฟล์ที่เหมือนเดิมทุกไบต์ไม่ใช่การแก้อะไร
ผมจึงไม่ทำ และรายงานเป็นผลลบพร้อมสาเหตุแทน

### สาเหตุจริงของบรรทัด `CENSUS DRIFT`
คำสั่งที่ทั้ง LANE-GM (ใบ `1929`) และ COO (ใบ `2050`) รัน:
```
python3 tools/pf_ui_wire_name_census.py --tsv reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv
```
`--tsv` คือ **ขาเข้า** ของเครื่องมือ (สารบัญ 327 แถวใน `pf_bridge`) · `--artifact` คือ **ขาออก**
คำสั่งนี้ป้อนไฟล์ผลลัพธ์เข้าไปในช่องของสารบัญ

มันผ่านได้เพราะ artifact ของเครื่องมือนี้หน้าตาเหมือนสารบัญมาก: บรรทัดแรกเป็นหัวตาราง
`id<TAB>name<TAB>family...` และทุกบรรทัดใต้นั้นก็มี id ฐานสิบหกในคอลัมน์ 1 กับชื่อ Vital ในคอลัมน์ 2
⇒ `load_names()` อ่าน artifact เป็นสารบัญได้สนิท คืน **328 แถว** (327 แถวจริง + คู่ `("id","name")` จากหัวตาราง)
⇒ `main()` เอาสำมะโนที่ derive จากของผิดไปเทียบกับ artifact ที่ commit ไว้ แล้วพิมพ์ `CENSUS DRIFT`

🔴 บรรทัดนั้น**พูดถึงขาเข้าที่ผิด ด้วยถ้อยคำของขาออกที่ค้าง** สองสายอ่านมันตรงตามที่มันเขียน
และมันเขียนผิด — **GM เสียหนึ่งรอบไปรายงาน COO เสียหนึ่งรอบไปตัดสิน** ความผิดอยู่ที่เครื่องมือของสายผม
GM ทำถูกทุกข้อ (ไม่ emit ทับของสายอื่น · สร้าง worktree ของ main เปล่ายืนยันซ้ำ · เขียน nonclaim ว่าไม่ได้ diff ตาราง)

### แก้แล้ว — โค้ด ไม่ใช่คำอธิบายในไฟล์รอบ
`tools/pf_ui_wire_name_census.py` `load_names()` ปฏิเสธไฟล์ที่แถวแรกเป็นคู่ `("id","name")`
(= หัวตารางของ artifact) ด้วย `CENSUS ERROR` ที่ **เอ่ยชื่อทั้งสองแฟล็ก** ว่าอันไหนรับอะไร
สารบัญจริงติดกับดักนี้ไม่ได้: สองบรรทัดหัวของมันเป็น `#` ที่ถูกข้าม และไม่มีแถวไหนเป็นคู่นั้นได้
เป็นการ **ปฏิเสธ** ไม่ใช่การข้ามหัวตารางเงียบ ๆ เพราะการอ่าน artifact เป็นสารบัญให้คำตอบที่
**หน้าตาเหมือนสำมะโนแต่ไม่ใช่สำมะโน**
```
ก่อนแก้: --tsv <artifact>  ->  CENSUS DRIFT ...           exit 1
หลังแก้: --tsv <artifact>  ->  CENSUS ERROR ... --tsv/--artifact   exit 2
ดีฟอลต์ (ไม่ใส่แฟล็ก)     ->  PASS -- committed artifact matches a fresh re-derive  exit 0
```
เทสสามใบ `tests/test_ui_wire_name_census.py` คลาส `ArtifactPassedAsCatalogIsRefused`:
(1) `CensusError` เอ่ยทั้ง `--tsv` และ `--artifact` (2) `main()` คืน 2 และ **ไม่มีคำว่า `CENSUS DRIFT`**
ในเอาต์พุต — สตริงที่สองสายลงมือตามมัน (3) สารบัญจริงยังโหลดผ่าน
`docs/PYTEST_SKIP_PINS.json` `ui_wire_census_inputs` 15 -> 16 (ใบ (3) เท่านั้นที่ guarded
เพราะอ่านสารบัญพี่น้อง · ใบ (1)/(2) สร้าง artifact ปลอมสองบรรทัดใน `TemporaryDirectory` เอง
จึงรันบน gate-windows ได้ = ตัวจับ regression อยู่ฝั่งที่เกตรันจริง)

**พิสูจน์ว่าเทสตายจริง ไม่ใช่แค่เขียว** (มิวแทนต์): เปลี่ยนการ์ดเป็น `if False:`
⇒ ใบ (1) และ (2) **FAILED** · คืนการ์ด ⇒ ผ่านทั้งสาม

## คิวข้อ 3 — ติดที่ seam และนี่คือการวัดของรอบนี้ ไม่ใช่การอ้างซ้ำจากรอบก่อน
ไฟล์สายนิยามคิวข้อ 3 (แก้โดยรอบ `719e10`) = ฟังก์ชันที่ **layout รู้แล้ว และมี call site อยู่แล้ว**
วัดบน `origin/main` `ac86f7e` รอบนี้:
- โมดูล `ui_*.py` ในเขตของสาย = **19 ไฟล์** · ที่ `runtime.py` อ้างถึงเลย = **5 ชื่อ**
  (`ui_friend_wire` `ui_mail_wire` `ui_party_wire` `ui_trade_wire` เป็นการ import **ค่า id เท่านั้น**
  ไม่ใช่การเรียกฟังก์ชัน · `ui_logout_exit_game` เป็นตัวเดียวที่ถูก **เรียก** จริง)
- แปด vital ของสายที่ dispatch แล้ว (`_FRIEND_MAIL_PARTY_TRADE_DISPATCH_IDS`, `runtime.py:8806`)
  จบที่ `lane_hooks.fire(...)` แล้ว `return []` — และ `fire()` มีลายเซ็น `-> None` โดยสัญญา
  (docstring: "Never returns a value; hooks that need to hand something back to runtime.py are
  not what this point shape is for") ⇒ **ไม่มีโมดูล `lane_hooks/lane_ui_*` ของผมตอบเฟรมได้เลย
  ต่อให้เขียนดีแค่ไหน** · `lane_hooks/` เป็นเขตเขียนของสาย แต่ **รูปของจุดต่อ**ไม่ใช่
- ทางเดียวที่ตอบได้บน main วันนี้คือรูปของ `ui_logout_exit_game`: call site ที่ `runtime.py:7606`
  เรียกโมดูลตรง ๆ และคืน `list(outcome.actions)` เมื่อ `handled` — `runtime.py` เป็นเขตของ chief
⇒ **บล็อกเกอร์เดียว = CORE-REQUEST `notes_to_chief/20260907_2020_LANE-UI-CORE-REQUEST-one-seam-that-lets-a-ui-module-answer-a-frame.md`** ยังเปิดอยู่
คิวของ chief ใน `NOW.md` (`2050`) มีสามงานก่อนหน้าใบนี้ ⇒ ผมไม่รอ และไม่ออกใบซ้ำ (ใบซ้ำ = เสียรอบ chief)

**"ว่างเพราะรอ chief ใบ `2020`" จึงทำ census (คำสั่ง COO `2050` ข้อ 3) แทน: `pirate-force-server` PR ของรอบนี้**

## หลักฐาน
- ชั้น wire/DB: `pytest tests/test_ui_wire_name_census.py` = **82 passed, 27 subtests** (79 เดิม + สามใบใหม่)
  · `pytest tests/test_pytest_precondition_census.py` = 69 passed, 1308 subtests
  · ชุดเต็ม `pytest tests/` รันบนต้นไม้ที่ `git merge origin/main` แล้ว (`Already up to date`, main `ac86f7e` เป็น ancestor)
  — ผล: **13788 passed, 411 skipped, 0 failed, 37700 subtests** (699 s)
  · `pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS** (census row RED ก่อนอัปเดตพิน → PASS หลัง)
  · ซ้อมไร้ `pf_bridge` ข้าง ๆ (`git worktree add --detach` ตามที่ใบพินเองสั่ง):
    `pytest tests/test_ui_wire_name_census.py` = **66 passed, 16 skipped, 0 failed**
    และ `test_pytest_precondition_census.py` เขียวในทรีเดียวกัน
- ชั้น client-observable: **ไม่มี และไม่อ้าง** — ไม่มีอะไรใหม่ถึงจอผู้เล่นในรอบนี้
- `git diff --stat origin/main..HEAD -- src/` = **ว่าง** ไม่มีโมดูลรันไทม์ถูกแตะ
- `TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว — ไม่มีโค้ดรันไทม์ถูกแก้ เครื่องมือออฟไลน์ล้วน
- `ADVERSARY_PENDING pirate-force-server#1078` — สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน ผลยังไม่คืนตอน push · **ผมไม่เขียนว่า "ผ่าน adversary"** · รอบถัดไปของสายนี้สั่ง adversary บนกิ่ง `claude/ecstatic-franklin-8y18nc` เป็นงานแรก

## nonclaims
- ไม่อ้างว่าการ์ดใหม่จับ "ไฟล์ผิด" ได้ทุกชนิด — จับได้เฉพาะไฟล์ที่ขึ้นต้นด้วยหัวตาราง `id/name` ของ artifact นี้
  ไฟล์ TSV อื่นที่บังเอิญมีสองคอลัมน์แรกเป็น id/ชื่อ ยังผ่านเข้าไปได้เหมือนเดิม
- ไม่อ้างว่าเกต Windows เคยแดงด้วยเหตุนี้ — วัดบนคลาวด์ Linux เท่านั้น
- ไม่อ้างว่า GM หรือ COO วัดผิด — ทั้งคู่รันคำสั่งเดียวกันแล้วได้บรรทัดเดียวกัน **บรรทัดนั้นเองที่ผิด**
- 🔴 **ผมยังอธิบายรายงานของ GM ไม่ได้ทั้งหมด และไม่แกล้งว่าอธิบายได้**: GM เขียนว่าใบที่แดงในชุดเต็มของเขาคือ
  `CommittedArtifactTests::test_committed_artifact_matches_a_fresh_rederive` · รอบนี้ใบนั้น**เขียวทั้งสองแบบ**
  บน `origin/main` `ac86f7e` — รันเดี่ยว (`2 passed`) และในชุดเต็ม (`13788 passed / 0 failed`)
  ⇒ สมมติฐาน "ปนเปื้อนข้ามเทส" ที่ผมตั้งไว้ตอนแรก **ไม่มีหลักฐานรองรับ** ผมถอนมันทิ้ง
  สิ่งที่ยืนยันได้มีสองอย่าง: (ก) คำสั่ง `--tsv <artifact>` ให้บรรทัด `CENSUS DRIFT` จริง ซึ่งเป็นบรรทัดที่
  ใบของ GM และใบของ COO ยกมาอ้างคำต่อคำ และ (ข) ใบเทสนั้นไม่แดงบน main ทั้งเดี่ยวและในชุดเต็ม
  ผมไม่รู้ว่าชุดเต็มของ GM แดงจากทรีคนละสถานะหรือจากอย่างอื่น และไม่มีสิทธิ์เดาแทนเขา
- ไม่อ้างว่าคิวข้อ 3 เดินต่อได้ — บล็อกเกอร์เป็นเขตเขียนของ chief ไม่ใช่ของสายผม
- ไม่อ้างว่า UI-B/`GT-205`/`GT-211` ขยับ — ไม่ได้แตะเลยรอบนี้

## จดหมายออก
- `notes_to_chief/20260907_2129_LANE-UI-TO-COO-the-census-was-never-stale.md` (ADDRESSEE: COO)
  — ผลลบเต็ม + สาเหตุ + สิ่งที่แก้ + ข้อค้างเรื่องชุดเต็มของ GM
- `.CONSUMED.txt` สามใบ (`1941` RE-294 · `2050` census · `2050` UI-A พัก) + สำเนาต้นฉบับลง `consumed/`

## รอบหน้าทำอะไร (งานแรกก่อนอื่น)
1. **หนี้เครื่องมือ ≤30 นาที (ทำเฉพาะถ้ามีใครรายงานซ้ำ ห้ามใช้รอบไปตรวจซ้ำเอง)**: ชุดเต็มรอบนี้เขียว
   ⇒ ไม่มีอะไรให้ไล่ · ถ้ามีรายงานแดงใบนั้นอีก ผู้ต้องสงสัยที่ระบุไว้แล้วคือ `_CENSUS_INPUT_CACHE`
   ที่มีคีย์เป็น `str(tsv_path)` อย่างเดียว ทั้งที่ผลขึ้นกับ `census.SRC_DIR` ด้วย และมีเทสในไฟล์เดียวกัน
   patch `SRC_DIR` เป็นทรีชั่วคราว ⇒ แก้คีย์ให้รวม `SRC_DIR` + เทสดักที่รันสองใบเรียงกันในโปรเซสเดียว
2. **คิวข้อ 3 ทันทีที่ chief ตอบ CORE-REQUEST `2020`**: `PartyInviteVital` `0x37B1` = คำตอบจริงตัวแรก
   (layout พิสูจน์แล้ว · decoder อยู่บน main แล้ว) แล้วปิดด้วยใบ GT บนจอ
3. **ใบ GT ปิด UI-B** (คิวข้อ 1) — hookup ลง main แล้ว เหลือครึ่ง client-observable
   ติดตรงที่ **ยังไม่มี `HEADLESS_PROOF:` token**: ไม่มี `print()` ไหนบนเส้น `ui_logout_exit_game`
   ที่พิสูจน์ว่ากลไก "ติดอาวุธ" ในบูตจริงได้จากบรรทัดเดียว ⇒ ต้องทำ token ก่อน แล้วค่อยส่งเนื้อใบไป K
   (`NOW.md 1910`: เลขใบ/เนื้อใบ = LANE-K · ส่งเป็น `*-TO-K-gt-body-*`)
4. `Stall*` 509-512 ปิดเองเมื่อ K พับ `RE-294` — **บล็อกเกอร์ที่เช็คแล้ว ห้ามใช้รอบไปตรวจซ้ำ**

SCOREBOARD: STUCK | ผู้เล่นไม่ได้อะไรเพิ่มรอบนี้ และคิวข้อ 3 ติดที่ seam ของ chief (ใบ `2020`) ไม่ใช่ที่สายผม | ว่างเพราะรอ chief ใบ CORE-REQUEST `20260907_2020` จึงทำงาน census ตามคำสั่ง COO `2050` แทน: `pirate-force-server#1078` (สำมะโนไม่เคยค้าง — บรรทัด `CENSUS DRIFT` ที่กิน GM หนึ่งรอบและ COO หนึ่งรอบ เป็นบั๊กของเครื่องมือสายผมเอง แก้แล้ว + เทสสามใบ + มิวแทนต์) · `pf_bridge#1791`

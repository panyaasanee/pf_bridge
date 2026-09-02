# รอบ `p7q74c` (LANE-GM) — 2026-09-03T03:40+07:00

ล็อกรอบ: `pf_bridge#924` (draft ตั้งแต่วินาทีแรก) · สาขา `claude/awesome-gates-p7q74c` (bridge) ·
`claude/gracious-galileo-p7q74c` (server)

## รอบนี้ขยับ NOW ข้อไหน

**P-3 — ปุ่ม GM กดแล้วต้องเปิดใช้งานได้จริง** ข้อที่ `NOW.md` เขียนว่า
🔴 *"COO `0148` แก้ `2342` ของตัวเอง: กฎ id 2 ยังบล็อก แต่ `install.bat` ต้องรับ `PFGM_FORCE=1`
แล้วก๊อปต่อพร้อมพิมพ์ verdict จริงตัวใหญ่"* — รอบนี้ทำข้อนั้นจนจบ

ข้ออื่นของ NOW ที่ไม่ได้ขยับ และเพราะอะไร:
- **P-1 ตัวเดินหลาย vital** — เจ้าของคือ **สาย E** (`COO 1845`) ไม่ใช่สายนี้ ห้ามแตะ
- **P-2 สีชื่อมอนสเตอร์** — `NOW.md` เขียนเองว่า *"ห้ามเปิด RE ใหม่จนมีผลจากเครื่องจริงและ P0-2 ขยับ"*
  ⇒ ติดที่ **เครื่องเจ้าของ** ไม่ใช่ที่โค้ด
- **GM-B `/speed`** — `COO 2147` สั่งห้ามปลดล็อกใดล็อกหนึ่งจนกว่ารอบ attended จะเกิด ⇒ ติดที่ **Panya**
- **GM-A `/warp`** — เหลือ `GT-192` ซึ่ง `[🟢 READY]` แล้ว ⇒ ติดที่ **Panya**

## ตรวจต้นรอบ (ตามลำดับที่พรอมป์สั่ง)

1. `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **มีจริง** (อยู่ที่ราก `pf_bridge`
   ไม่ใช่ `external/`)
2. PR ค้างที่ขึ้นต้น `[LANE-GM]` ทั้งสองรีโป — **ไม่มี** (bridge เปิดค้าง #923 `[LANE-DB]` · #922
   `[LANE-E]` · #920 `[LANE-A]` · server เปิดค้าง #617 `[LANE-A]` — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)
3. **ชะตา PR รอบก่อน (ADDENDUM ข้อ A)** — `pf_bridge#919` **merged=true** 19:56Z ·
   `pirate-force-server#616` **merged=true** 20:12Z (`main` ของเซิร์ฟเวอร์ = `24a422d` ซึ่งเป็น merge
   ของ `#616`) ⇒ ไม่มีอะไรต้องกู้
4. **กล่องจดหมาย** — ใบที่หัวใบเขียน `ADDRESSEE: LANE-GM` และยังไม่มี `.CONSUMED.txt` คู่กัน:
   **ค้นแล้ว: ไม่เจอ ศูนย์ใบ** (ใบ `0148` ถูกบริโภคไปแล้วในรอบ `kv2vjk`) · ใบที่สายนี้เปิดไว้และ
   **ยังไม่มีคำตอบ**: `20260903_0230_LANE-GM-ASK-COO-*` (pin ไป `preconditions` แทน `design_skips`)
   และ `20260903_0303_LANE-GM-TO-CHIEF-*` (ขอคีย์แคบ `BRIDGE_GM_INSTALL_BAT`) — ทั้งคู่ไม่บล็อกรอบนี้
5. **กฎค้นก่อนถอด** — `external/00_SEARCH_HERE_FIRST.md` + `gamedata/00_SEARCH_HERE_FIRST.md`
   **ค้นแล้ว: ไม่เจอ** ของที่เกี่ยวกับ `RT_MANIFEST` / `GameMaster.dll` ของไคลเอนต์ (คำว่า MANIFEST
   ที่เจอทั้งหมดคือ `PF_V*_MANIFEST.md` ของรีโปเอง คนละเรื่อง) ⇒ รอบนี้ไม่พึ่งข้อมูลไคลเอนต์เลย

## ทำอะไรลงไป

### 1. `pf_bridge/patches/gm_plugin/install.bat` — revision 4: `PFGM_FORCE=1`

ทางออกที่ **ทิ้งหลักฐาน** สำหรับกรณีเดียว: `plugin_image_check` ปฏิเสธไฟล์ที่กำลังจะติดตั้ง

- ตัวแปร **ไม่มีค่าปริยาย** ที่ไหนในทั้งสองรีโป และรับเฉพาะ `1` ตัวเดียว (`PFGM_FORCE=0`,
  `PFGM_FORCE=no` ไม่ force) · de-quote ก่อนเทียบ เพราะ `set PFGM_FORCE="1"` คือวิธีที่คนพิมพ์จริง
- **ไปไม่ถึง** ด่าน `[STOP] A GameMaster.dll ALREADY EXISTS` (ด่านนั้นคือด่านกันทำลายไฟล์ที่โปรเจกต์
  หามาไม่ได้ตั้งแต่ 27 ส.ค. — ไม่มีตัวแปรไหน force ได้) และไปไม่ถึงด่าน `.rsrc` `[FAIL]`
- พิมพ์ `[FORCED] verdict=<ค่าจริง> rules=<กฎที่ไม่ผ่าน>` **ตัวใหญ่** · เก็บรายงานเต็มไว้บนดิสก์ ·
  และ **พิมพ์ซ้ำใต้บรรทัด `[OK]`** เพราะ `[OK]` กับ SHA256 คือสิ่งที่คนถ่ายจอ ส่วนคำปฏิเสธเลื่อนหายไป
  ข้างบนแล้ว
- สองโทเคนนั้น **อ่านจากผลของตัวตรวจ** ไม่ได้พิมพ์ค่าซ้ำในไฟล์ batch

### 2. `pirate-force-server/src/pirateforce_foundation/gm/plugin_image_check.py` — `failed_rules`

`console_lines()` พิมพ์บรรทัดใหม่ใต้ verdict: `GM_PLUGIN_IMAGE <label> failed_rules=<รายการ>`
ไล่ **ทุกกฎที่ไฟล์ทำผิด** ตามลำดับ `CONSOLE_RULES` ไม่ใช่แค่กฎเดียวที่ verdict บังเอิญเป็น (ไฟล์เดียว
ผิดได้สองกฎ) · `none` เมื่อผ่าน · `none_evaluated` สำหรับ `missing` / `no_such_dir` / `unreadable`
ซึ่งยังไม่ได้อ่านไบต์ไหนเลย — การพิมพ์ชื่อกฎตรงนั้นคือการอ้างการทดสอบที่ไม่เคยเกิด

### 3. เทส (`tests/test_gm_plugin_image_check.py`)

- `test_install_bat_refuses_rather_than_warns_when_the_checker_answers_no` — **แคบลง ไม่ได้ถอด**:
  เดิมเกรด "ไม่มีเส้นทางไหนจาก `:pfgm_refuse` ถึง `:do_copy`" ตอนนี้เกรด "**ทุก** เส้นทางที่ถึงต้องมี
  `PFGM_FORCE` และ `=="1"` อยู่บนบรรทัดเดียวกัน และต้องมี **เส้นเดียว**" — `goto` เปล่า, `exit /b 1`
  ที่ถูกลบจนตกลงบล็อกถัดไป, เงื่อนไขตัวแปรอื่น, หรือทางออกที่สองล้วนทำให้แดง
- ใบใหม่ `test_install_bat_forces_only_the_checker_and_reads_the_real_tokens` — เกรดสามอย่าง:
  โทเคนที่ batch grep ต้องเป็นโทเคนที่โมดูลพิมพ์จริง (derive จาก `console_lines`) · `[STOP]` guard
  ต้องไม่มีคำว่า `PFGM_FORCE` อยู่ในบล็อกของมัน · fallback สำหรับตัวตรวจรุ่นเก่าต้องเป็นประโยค
  ไม่ใช่ค่าว่าง และ **ห้ามมี `<` `>`** เพราะ `echo %VAR%` ที่มี `<` คือ redirect — บรรทัดเดียวที่เรา
  ขอให้เจ้าของรายงานจะหายเข้าไฟล์
- `INSTALL_BAT_TESTS` 3 → 4 และ pin `bridge_sibling` ของโมดูลนี้ใน `docs/PYTEST_SKIP_PINS.json`
  count 3 → 4 + ชื่อเทสใบที่สี่ (**entry เดิม entry เดียว** ตามที่ `COO 0148` อนุญาต ไม่แตะ entry อื่น)

## หลักฐาน

### ตารางกลายพันธุ์ — เทสใหม่ฆ่าได้จริงกี่ตัว (5 ตัว 5 ตาย)

รันคุณสมบัติที่เทสเกรด ใส่ข้อความ batch ที่ถูกกลายพันธุ์ทีละแบบ:

| กลายพันธุ์ | ผล |
|---|---|
| ไฟล์จริงบนสาขานี้ | GREEN |
| `goto pfgm_forced` แบบไม่มีเงื่อนไข | RED — `unguarded escape` |
| เปลี่ยนยามเป็นตัวแปรอื่น (`if defined PFGM_PY`) | RED — `unguarded escape` |
| รับค่าอะไรก็ได้ที่ไม่ว่าง (`if defined PFGM_FORCE_FLAG`) | RED — `wrong guard` |
| ลบ `exit /b 1` ให้ตกลงบล็อกถัดไป | RED — `no exit` |
| เติมทางออกที่สอง (`if defined PFGM_PY goto do_copy`) | RED — `unguarded escape` |

### ตาราง `failed_rules` — วัดกับภาพ PE ที่ประกอบเอง

| ภาพ | verdict | `failed_rules` |
|---|---|---|
| ปกติ | `image_ok` | `none` |
| manifest ฝังที่ id 1 | `manifest_missing` | `manifest_id2` |
| ไม่มี manifest | `manifest_missing` | `manifest_id2` |
| ไม่ใช่ DLL + export ถูกตกแต่งชื่อ | `not_a_dll` | `pe32_dll,export_exact` (**สองกฎ**) |
| PE32+ | `wrong_machine` | `pe32_dll` |
| export เป็น forwarder | `export_forwarded` | `export_exact` |
| ไฟล์ตัดกลาง | `not_pe` | `pe32_dll` |
| โฟลเดอร์ไคลเอนต์ที่ไม่มี DLL | `missing` | `none_evaluated` |

### ซ้อมเกต (สภาพไม่มี `pf_bridge` ข้าง ๆ)

`git clone` สาขานี้ลงโฟลเดอร์ที่ **ไม่มี** `pf_bridge` เป็นพี่น้อง แล้วรันสองอย่างตามที่ `COO 0148`
ข้อ 3 กับ `COO 2344` สั่ง:
- `pytest tests/test_gm_plugin_image_check.py` → **70 passed, 4 skipped** (สี่ตัวคือ pin ที่เพิ่งขยับ)
- `python tools/pf_pytest_precondition_census.py --run` → **`every skip is declared, named and pinned`
  · RESULT: PASS**

### เทสระหว่างทาง

- `pytest tests/test_gm_plugin_image_check.py` → **74 passed** (เดิม 73)
- `pytest tests/test_gm_plugin_image_check.py tests/test_pytest_precondition_census.py
  tests/test_gm_source_is_cp874_safe.py` → **143 passed, 893 subtests passed**
- ซ้อมเกตในสภาพ **ไม่มี `pf_bridge` ข้าง ๆ**: ดูหัวข้อ "ซ้อมเกต" ด้านล่าง
- ชุดเต็ม `pytest tests/`: ดูหัวข้อ "ชุดเต็ม" ด้านล่าง (รันครั้งเดียว บน commit สุดท้าย)

## NONCLAIM

- **ไม่มีเฟรม GM ถูกส่งในรอบนี้ ไม่มีขั้นไหนถูกข้ามด้วย GM** งานรอบนี้เป็นสคริปต์ติดตั้งกับตัวตรวจไฟล์
- `install.bat` **ยังไม่เคยถูกรันเลยสักครั้ง** ไม่มีใครเคยตั้ง `PFGM_FORCE` และไม่มี DLL ตัวไหนถูก force
  ⇒ **P-3 ไม่ขยับไป "รอ Panya ติ๊ก"** สิ่งที่อ้างคือ "ทางออกมีจริง ถูกจำกัดขอบเขต และใช้เงียบ ๆ ไม่ได้"
  ไม่ใช่ "สคริปต์ผลิต DLL ที่โหลดได้เอง"
- กฎ id 2 **ยังไม่เคยอ่าน DLL จริงสักไฟล์** — นั่นคือเหตุผลที่ COO สั่งให้มีทางออกนี้ ไม่ใช่ผลของมัน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

เมื่อวาน ถ้า `install.bat` ปฏิเสธ DLL ที่ **เจ้าของเคยเห็นกับตาว่าโหลดได้** (build 1 ของ `GT-207`
หน้าต่าง GMUI เปิดจริงเวลา 18:54) รอบเทสจบตรงนั้น ไม่มีทางไปต่อและไม่มีอะไรให้รายงานนอกจาก
"มันไม่ยอม" · วันนี้พิมพ์ `set PFGM_FORCE=1` แล้วรันซ้ำ ได้ทั้งการติดตั้งและบรรทัดหลักฐานตัวใหญ่ที่บอก
ว่า verdict จริงคืออะไรและกฎข้อไหนไม่ผ่าน — ถ้าปุ่มเปิดได้หลัง force แปลว่ากฎของเราผิดกับไฟล์จริง
และเราติดหนี้เจ้าของหนึ่งการแก้ ถ้าไม่เปิด แปลว่ากฎเพิ่งกันรอบเทสไว้ได้หนึ่งรอบ ทั้งสองคำตอบคือหลักฐาน

## backlog ของสายนี้ ติดที่ใคร

- `GT-192` (`/warp` หลายแมพ) · `GT-183`/`/speed` attended · `GT-211` — **ติดที่ Panya** (ใบพร้อมหมดแล้ว)
- ใบวัดสอง DLL (ตัวที่ `GT-207` โหลดได้ กับตัว 13,824 ไบต์ที่โหลดไม่ได้) — **ติดที่ chief** (`COO 0148`
  สั่ง chief เปิดใบนี้ ไม่ใช่สายนี้)
- คีย์แคบ `BRIDGE_GM_INSTALL_BAT` ใน `tests/pf_preconditions.py` — **ติดที่ chief** (ใบ `0303`)
- pin ควรอยู่ `preconditions` หรือ `design_skips` — **ติดที่ COO** (ใบ `0230` ยังไม่มีคำตอบ)
- P-2 สีชื่อมอนสเตอร์ — **ติดที่เครื่องเจ้าของ** (`NOW.md` ห้ามเปิด RE ใหม่จนกว่าจะมีผลจากเครื่องจริง)

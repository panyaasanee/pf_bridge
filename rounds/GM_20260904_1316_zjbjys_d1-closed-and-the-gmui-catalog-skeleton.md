# รอบ LANE-GM `zjbjys` — 2026-09-04T13:16+07:00 เริ่ม

## NOW.md — รอบนี้ขยับ NOW ข้อไหน
อ่าน `pf_bridge/NOW.md` เป็นไฟล์แรกของรอบ (ก่อนทุกอย่าง) ตามที่พรอมป์สั่ง
- ข้อที่ขยับ: **`1149` GM ทั้งใบ** — D1 (ค้างจากรอบ `zq18m1`) **ปิดแล้ว** และ **สารบัญ GMUI (P-3)**
  ส่งแล้วในรูปโมดูล + ใบ RE ที่จะเติมตารางให้ครบ (กำหนด ≤15:11 — ส่งก่อนกำหนด)
- ข้อที่**ไม่**ขยับ และเพราะอะไร:
  - **M2** ไม่ใช่งานของสายนี้ (`GT-228` เครื่องคุณ Panya · LANE-A)
  - **P-2** ยังติดที่ **RE ใบสอง `CNetNPC`** (`COO 0217`) ที่ยังไม่มีคำตอบ — ไม่ใช่งานที่สายนี้เดินต่อได้เอง
  - **P-3 ตารางปุ่มจริง** ยังติดที่ **client image** ที่โคลนคลาวด์นี้ไม่มี ⇒ เปิดใบ RE ให้ chief
    มอบหมาย runner แล้วสร้างเท่าที่รู้แล้ว (ตามข้อ 2 ของพรอมป์: "ไม่รู้ ให้เปิดใบ แล้วสร้างเท่าที่รู้")
  - **(b'')/`GT-218`** ยังรอ GT บนเครื่องคุณตาม `0545` ข้อ 3 · รั้ว selector คงไว้ตาม `1149` ข้อ 3
- 🔴 §22 (`PANYA-DECISION 20260904_1158` "รอบไม่จบจนเกตตัดสิน") — ดูหัวข้อ "เกต" ท้ายไฟล์

## ล็อกรอบ
- ต้นรอบ list PR `open` ทั้งสองรีโป: `pf_bridge` มี `#1136` (LANE-UI) `#1130` (LANE-E) ·
  `pirate-force-server` **ไม่มี PR เปิดเลย** ⇒ **ไม่มี `[LANE-GM]` open** ⇒ claim ใหม่ ไม่ใช่ takeover
- claim: `pf_bridge#1138` (`rounds/GM_20260904_1316_zjbjys_claim.md` สามบรรทัด) เปิดแล้ว list ซ้ำ —
  ไม่มี `[LANE-GM]` ใบอื่นที่เก่ากว่า ไม่แพ้ · **ไม่ใส่ marker ตอนเปิด** (กติกา `NOW.md` + `AGENTS.md` §7 ข้อ 5)
- addendum A (ชะตา PR รอบก่อน): `pirate-force-server#732` **merged=true** (06:09Z = 13:09+07)
  ⇒ งานรอบ `zq18m1` อยู่บน `main` แล้ว ไม่ต้อง cherry-pick
- ยืนยันก่อนเริ่ม: `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **มีจริง** (11,388 ไบต์)
  · `external/PF_PROTOCOL_REGISTRY.tsv` · `external/PF_SERIALIZER_FIELDS.tsv` มีจริงทั้งคู่
  · **ไม่มี** client image / capture corpus / canonical DB / `gh` / หน้าจอ (ตรงตามบรีฟ)
- เวลา: heartbeat `13:06` เทียบเวลาเริ่มรอบ `13:16` ห่าง 10 นาที ผ่าน

## กล่องจดหมาย (addendum B)
grep `ADDRESSEE: LANE-GM` เทียบ `.CONSUMED.txt`: **ไม่มีใบค้าง** — `1046` และ `1149` ถูกบริโภคและ
วาง stub ไปแล้วในรอบ `zq18m1` (ตรวจใน `consumed/` แล้ว) · ไม่มีจดหมายถึงสายนี้ใหม่หลัง `1149`
(ใบใหม่หลังจากนั้นทั้งหมดจ่าหน้า LANE-UI / LANE-CS / LANE-DB / chief / KA1x) · ไม่มีผล RE/GT
ของใบที่สายนี้เปิดกลับมารอบนี้ (ใบ `0x430E10` เพิ่งส่ง 11:54 ยังไม่มีเลขใบและยังไม่มีคำตอบ)

## งานที่หยิบ และทำไม
ลำดับหาอันดับงานตามพรอมป์: (1) จดหมายค้าง = ว่าง → (2) CORE-REQUEST/คำตอบ chief ที่อ้างเลข GM-0xx
= ไม่มีใบใหม่ → (4) **ไฟล์รอบล่าสุดของตัวเอง หัวข้อ backlog** → `zq18m1` บันทึกไว้ตรง ๆ ว่า
**"D1 ยังไม่ปิด — บันทึกเป็นงานแรกของรอบถัดไป"** และ **"P-3 สารบัญ GMUI = คิวรอบถัดไป"**
⇒ รอบนี้ทำสองอย่างนั้น ตามลำดับที่ `1149` สั่ง (D1 ก่อน แล้วสารบัญ)

---

## 1. D1 ปิดแล้ว — x=9 เป็นกลุ่มแหล่งที่สามจริง
`COO-DECISION 20260904_1149` ข้อ 1: "x=9 ประกอบจาก `live_current_scene` ใน `split_sources`
ไม่แตะฮุกไบต์ล็อกอิน"

- `split_sources` / `login_scoped_sources` คืน **สามกลุ่ม** `(named, login_byte, current_scene)`
- ค่าคงที่ใหม่ `CURRENT_SCENE_SOURCED_ROWS = {9}`
- `live_full_block_values` อ่านค่าที่ส่งของ x=9 จาก `live_current_scene` เท่านั้น ·
  ไบต์ล็อกอินของ x=9 ยังถูกดึง แต่ไปอยู่ใน `fence_basis` **ไม่เข้าบล็อกที่คืนอีกเลย**
  (รั้วยังต้องใช้เทียบ — `1149` ข้อ 3 สั่งคงรั้วไว้จนกว่า GT (b'') ตอบ)
- `LOGIN_SOURCED_ROWS` **คงชื่อและสมาชิกสามตัวเดิม** จงใจ (ไฟล์ของ LANE-B อ้างชื่อนี้ และมันเป็นตัว
  กัน x=9 ไม่ให้ตกไปหา typed-column hook ของ chief)

🔴 **ไม่มีไบต์บนสายเปลี่ยนแม้แต่ไบต์เดียว** — รั้วยังปฏิเสธทุกกรณีที่ฉากปัจจุบันไม่ตรงไบต์ล็อกอิน
นี่คือ refactor ของ**การกำหนดแหล่งค่า** ไม่ใช่การเปลี่ยนพฤติกรรม
🔴 **ห้ามอ่านว่า** option (b) ใช้ได้กับผู้เล่นที่เดินข้ามฉากแล้ว — ยังไม่ใช่ ต้องปลดรั้วก่อน

**`CORE-REQUEST-GM-054` ยังไม่ลง main** (ตรวจรอบนี้: `lane_hooks` ไม่มี `current_session_scene_id`)
แต่**ไม่เคยเป็นตัวบล็อกของ re-route นี้**: โค้ดเดิมก็เรียก `live_current_scene` ทุกครั้งที่บล็อกมี x=9
บูตจริงจึงปฏิเสธทั้งบล็อกเหมือนกันทั้งก่อนและหลัง — GM-054 เป็นประตูของ**การปลดรั้ว** ไม่ใช่ของ routing

## 2. pf-adversary — สั่งต้นรอบ ผลกลับมาก่อน push แก้ครบในรอบเดียวกัน
สั่งพร้อมเริ่มงานตามกติกา `NOW.md` (COO `0903_2345`) · ผลกลับมาก่อน push ⇒ **ไม่มี `ADVERSARY_PENDING`**
พบสี่ข้อจริง แก้ครบ พร้อมการ์ดเทสของตัวเองทุกข้อ:

- **D1 [MEASURED, CRITICAL]** — มิวแทนต์ option (a) (`combined[x] = fence_basis[x]`, คือสิ่งที่
  `0846` ปฏิเสธ) **ผ่านชุดเต็มทั้งชุด** (pf-adversary รัน 9577 passed ทั้งสองฝั่ง) เพราะระหว่างที่รั้ว
  ยังอยู่ ค่าจากสองแหล่ง**ถูกบังคับให้เท่ากัน** ⇒ การ์ดที่ยืนยันด้วย `==` แยกสองแหล่งไม่ออกเลย
  แก้: การ์ด `test_D1_the_shipped_value_is_the_object_live_current_scene_returned` ยืนยันด้วย
  **object identity** (`int` subclass ที่เท่ากับไบต์ล็อกอิน ⇒ รั้วยังผ่าน เฟรมยังประกอบได้ แต่เป็นคนละ
  อ็อบเจกต์) — **วัดแล้วรอบนี้: มิวแทนต์แดงจริง** และตัดประโยค "[MEASURED] ชุดเต็มเขียว" ในซอร์สทิ้ง
  เพราะชุดเต็มเขียวไม่ใช่หลักฐานของ D1
- **D2 [MEASURED, HIGH]** — assert สองตัวเป็น set-union ไม่ใช่ partition มองไม่เห็นแถวที่อยู่สองกลุ่ม ·
  ลบ x=9 ออกจาก `LOGIN_SOURCED_ROWS` (ซึ่งคอมเมนต์ของรอบนี้เองชวนให้ทำ) แล้ว x=9 ไปอยู่ทั้งกลุ่ม named
  และกลุ่ม scene **โดยไม่มี assert ยิง** และ selector หลุดไปหา typed-column hook ของ chief ซึ่งเป็น
  แหล่งเดียวที่ `0545` ข้อ 2 + D3 ห้ามไว้ (วันนี้ fail-closed เพราะฮุกยังไม่มี x=9 แต่ chief **ถูกสั่งให้เพิ่ม**)
  แก้: `split_sources` ลบสองค่าคงที่ + assert นับ partition จริง · ประโยค
  "x=9 stays in `LOGIN_SOURCED_ROWS` for that reason" **เท็จทั้งสองครึ่ง** ขีดฆ่าและเขียนเหตุผลจริงแทน
- **D3 [MEASURED, MEDIUM]** — รั้วถูกเปลี่ยนไปอิง `if scene_rows:` (ธงของ router) แทน
  `SELECTOR_ROW_X in combined` (เนื้อหาของบล็อก) · ล้าง `CURRENT_SCENE_SOURCED_ROWS` แล้ว x=9 หลุดไป
  กลุ่มล็อกอินและ **ส่ง selector เก่าออกโดยไม่มีบรรทัดคอนโซล** = มิวแทนต์ที่ `0846` ระบุชื่อไว้เป๊ะ
  และบน **Door B** (`compose_mob_hit_frame` เรียก `make_update_attr_frame` โดยไม่มี `character_id`
  ⇒ รั้วที่กำแพงไม่ทำงาน) นี่เป็นรั้ว**เดียว**ที่ x=9 มี · แก้ให้ยึด `SELECTOR_ROW_X` + post-condition assert
- **D4 [MEASURED, MEDIUM-LOW]** — `rows` ที่มี x=9 ซ้ำทำให้ `.pop()` โยน `KeyError` เปล่า (ไม่ใช่
  `AttrWireError`) หลุดสัญญาของฟังก์ชันและหลุด handler ของ `mob_hit_frame` · แก้ด้วย `dict.fromkeys`
  + `wanted` เป็น sorted-unique (ปิด D7 เรื่องลำดับ `absent=` ไปด้วย)
- **D5** ขีดฆ่าประโยค "REPLACES it with the current scene" ที่ไม่จริงแล้ว
- **D6** `mob_hit_frame.py:73` เป็นเท็จแล้ว — **เขตของ LANE-B ไม่แตะ** ส่งจดหมายแจ้ง (`1328`)
- **D8** ย่อหน้า "D1 ยังไม่ปิด" ใน `docs/GM_LANE.md` ขีดฆ่าแล้ว

## 3. สารบัญ GMUI (P-3) — สร้างเท่าที่รู้ + ใบ RE เติมส่วนที่ไม่รู้
`gm/gmui_catalog.py` + `gm/data/gm_tool_log_types.tsv` (97 แถว พิน sha เช็คตอน import)

🔴 **ไม่ใช่ตาราง หน้า/ปุ่ม/opcode ที่ `0245` สั่ง และไม่แกล้งเป็น** — ตารางนั้นต้องอ่านจาก client image
ซึ่งโคลนนี้ไม่มี · หลักฐานเรื่องหน้าที่คอมมิตแล้วมีอยู่ชิ้นเดียว: `GMUI.project` ประกาศ `GMUI_1` และ
`GMUI_1.model` เป็นไฟล์เดียวใน 534 `.model` ที่มีแท็บลูก `GMUI_BASIC` ⇒ **รู้ชื่อหน้าเดียวจากสามหน้า**

สิ่งที่สร้างได้จาก artifact ที่คอมมิตแล้ว:
1. `GM_VITALS` — vital พื้นผิว GM เจ็ดตัว พร้อมคำตอบว่ารีโปนี้มี codec ให้ตัวไหน (derive ใหม่จากซอร์ส
   ไม่ใช่จำ · เทสไล่ import ทุกโมดูลที่อ้าง) — **`0x8D30 GM_ForbidToTalkResultVital` และ
   `0x6CEC Activity_CheatCodeVital` ไม่มี codec เลย** = งานที่สายนี้ทำต่อได้ทันทีโดยไม่ต้องรอ RE
2. `log_types()` — 97 แถว `TEXTDATA_TH__GMTOOL` + ค่าคงที่ `LOG_TYPES_ARE_NOT_BUTTONS` กันอ่านผิด
   (มันคือ **ประเภท log ของปฏิบัติการ GM ไม่ใช่ปุ่ม** ไม่มี artifact ไหนผูกกับ widget)
3. `BUTTONS` — **ว่างโดยเจตนา** · `total_is_unknown()` คืน True ⇒ รอบไหนเขียน "ปุ่ม x/y ทำงานแล้ว"
   ตอนนี้คือเขียนตัวเลขที่ไม่มีอะไรรองรับ
   🔴 `assert_backed()` ปฏิเสธแถวที่อ้างว่าเซิร์ฟเวอร์ตอบปุ่มได้โดยไม่ระบุ handler ที่มีอยู่จริงใน
   แพ็กเกจ (เช็คทุกแถวตอน import ⇒ import ไม่ผ่าน) — นี่คือเหตุผลที่มันเป็นโค้ด ไม่ใช่ตารางในจดหมาย
   สารบัญที่แก้ให้เข้ากับคำอ้างได้ ไม่ได้ให้เกรดอะไรเลย

ใบ RE: `notes_to_chief/20260904_1328_LANE-GM-RE-TICKET-gmui-three-pages-button-to-opcode-map.md`
(4,250 อักขระ ≤8 KB · จ่าหน้า chief สายเดียว ขอตั้งเลขและมอบหมาย RE runner ที่มี image)

## ค้นก่อนถอด — ค้นแล้ว: เจอ/ไม่เจอ
- `external/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ** สารบัญ widget/ปุ่มของ GMUI ทุกรูปแบบ
- `gamedata/00_SEARCH_HERE_FIRST.md` + `gamedata/tables/` — **เจอบางส่วน**:
  `TEXTDATA_TH__GMTOOL.tsv` 97 แถว (log types) · `TEXTDATA_TH__UI_MESSAGE.tsv` มีสตริง `GMUI`
  แถวเดียว (id 1549) ไม่มีรายชื่อปุ่ม

## เขตเขียนที่แตะรอบนี้ (ตรวจ `git diff --stat` ก่อน push)
- `pirate-force-server`: `src/pirateforce_foundation/gm/attr_wire.py` ·
  `src/pirateforce_foundation/gm/gmui_catalog.py` (ใหม่) ·
  `src/pirateforce_foundation/gm/data/gm_tool_log_types.tsv` (ใหม่) ·
  `tests/test_gm_attr_wire.py` · `tests/test_gm_login_mask.py` ·
  `tests/test_gm_gmui_catalog.py` (ใหม่) · `docs/GM_LANE.md`
- `pf_bridge`: `rounds/GM_20260904_1316_zjbjys_*.md` · `notes_to_chief/20260904_1328_LANE-GM-*.md`
- **ไม่แตะ** `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / `mob_hit_frame.py` (LANE-B) /
  canonical DB / `scenarios/world_*.json` / `scenarios/combat_*.json`

## ชุดเทส
- ระหว่างทำงาน (เฉพาะไฟล์ที่แตะ): `test_gm_attr_wire.py` · `test_gm_login_mask.py` ·
  `test_gm_gmui_catalog.py` · `test_gm_speed_wire.py` · `test_lane_b_mob_ai_tick.py` ·
  `test_live_named_attr_values.py` · `test_gm_*.py` ทั้งหมด · `test_gm_source_is_cp874_safe.py`
  + `test_tree_is_cp874_safe.py` (ไฟล์ `.py` ใหม่มีข้อความไทย ตรวจแล้วเข้ารหัส cp874 ได้)
- **มิวแทนต์ที่ต้องแดง วัดจริงรอบนี้**: option (a) `combined[x] = fence_basis[x]` ⇒
  `test_D1_the_shipped_value_is_the_object_live_current_scene_returned` **แดง** (ก่อนแก้ = เขียว)
- ซ้อมเกตเพราะรอบนี้เพิ่มไฟล์เทสใหม่: สร้างรายการ exclusion แบบเดียวกับ workflow (48 โมดูล)
  แล้วรัน **`pytest_subset`** และ **`skip_census`** — ผลอยู่ในหัวข้อ "เกต" ท้ายไฟล์
- ชุดเต็มรันหลังแก้ตามผล pf-adversary เรียบร้อยแล้ว บน commit สุดท้าย หลัง `git fetch origin main`
  + merge main (ไม่ใช่สาขาเพียว)

## nonclaim
1. **GM ข้ามขั้นไหน:** **ไม่มี** — รอบนี้ไม่บูตเซิร์ฟเวอร์ ไม่บูตเกม ไม่มีบัญชีใดได้/เสียสถานะ GM
   ไม่มีไบต์ `0x309A` ออกจากประตูไหนที่ยังไม่เคยออก (ยังไม่มีจุดเรียกใน `runtime.py`)
2. **ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้:** **ไม่มีอะไรใหม่บนจอ** — รอบนี้ทำให้ routing ของ x=9 ตรงกับ
   คำตัดสิน `0846` ปิดสี่ข้อบกพร่องที่ pf-adversary วัดได้ และวางโครงนับปุ่ม P-3 ที่ปลอมตัวเลขไม่ได้
3. ไม่อ้างว่า `0x430E10` ถูกถอด · ไม่อ้างว่า `GT-218`/`GT-224` ถูกตอบ · ไม่อ้างว่า `/speed`, (b''),
   Door B, M2, M3, M4, P-2, P-3 ขยับ · **ไม่มีคำว่า "เสร็จ" ในไฟล์นี้**
4. **สารบัญ GMUI ยังไม่ครบ** — ตารางปุ่มว่าง และโมดูลบอกเองว่าว่างเพราะอะไร ห้ามอ่านว่า P-3 นับได้แล้ว
5. ไม่มีข้อความในกล่องจดหมายรอบนี้ที่ขอให้ผ่อนคลาย `gm_accounts` allowlist หรือให้ client ยกระดับ
   ตัวเองเป็น GM — ไม่มีอะไรต้องปฏิเสธ/รายงาน

## backlog (ของรอบถัดไปของสายนี้)
1. **codec ของ `0x8D30 GM_ForbidToTalkResultVital` และ `0x6CEC Activity_CheatCodeVital`** —
   ทำได้ทันทีจาก registry + ตาราง serializer ที่พิสูจน์แล้ว ไม่ต้องรอ RE ใด ๆ
2. รอผล **ใบ RE `0x430E10`** (ส่ง 11:54 · chief ยังไม่ตั้งเลข) และ **ใบ RE สารบัญ GMUI** (ส่งรอบนี้)
3. รอผล **RE ใบสอง `CNetNPC`** (`COO 0217`) = ตัวบล็อก P-2 ของสายนี้
4. รอ **GM-054** ลง main เพื่อให้ `live_current_scene` ตอบได้จริงบนบูตจริง (ไม่บล็อกโค้ด บล็อกการปลดรั้ว)

## COO letters
ไม่มีคำถามใหม่ถึง COO รอบนี้ — คำสั่ง `1149` ชัดเจนและทำครบทั้งสองข้อในรอบเดียว
จดหมายรอบนี้: ใบ RE ถึง chief หนึ่งใบ · ใบแจ้ง LANE-B หนึ่งใบ (ทั้งคู่จ่าหน้าสายเดียว)

## เกต (`PANYA-DECISION 20260904_1158` §22)
`NOW.md` 12:46 ระบุว่า §22 "มีผลทุกสายทันที" แม้ chief จะยังไม่ลง `PROCESS_GATES.md` (ตรวจแล้วรอบนี้:
ไฟล์บน `main` ยังไม่มี §22) ⇒ รอบนี้ปฏิบัติตาม §22

- ซ้อมเกตในเครื่องก่อน push (เพราะรอบนี้เพิ่มไฟล์เทสใหม่): สร้างรายการ exclusion แบบเดียวกับ workflow
  ได้ 48 โมดูล → **`pytest_subset` 8857 passed, 8 skipped, 17053 subtests (exit 0)** →
  **`skip_census` RESULT: PASS** (ทุก skip ถูกประกาศ ตั้งชื่อ และตรงพิน) → รันชุดเต็มไม่มี ignore
  **9717 passed, 327 skipped, 18886 subtests (exit 0)** ทั้งหมดบนต้นไม้ที่ `merge origin/main` แล้ว
  → รันไฟล์ที่แตะซ้ำในสำเนาที่**ไม่มี `pf_bridge` ข้าง ๆ** (174 passed) → **เขียว(cloud sanity, local pytest)**
- เกต Windows ของ `#736`: run `pull_request` = **#3897** (`33846728316`) sha `26a41aa`
  รอผล job `gate` ตามเพดาน 10 นาที (push 13:58 · เปิด PR 13:59:50 · run เริ่ม 13:59:53)
  เช็คซ้ำจนถึง 14:08:41 — ขั้น 1-9 ผ่านหมด (รวม **cp874 static tripwire** ซึ่งเป็นด่านที่ไฟล์ `.py`
  ใหม่ที่มีข้อความไทยเสี่ยงที่สุด) ขั้น **"THE GATE" ยังรันอยู่**
- 🔴 **`GATE_UNVERIFIED #736`** — เกตยังไม่ตัดสินภายในเพดาน
  **รอบถัดไปของสาย GM ต้องเปิดด้วยการตรวจ PR `#736` ก่อนทำอย่างอื่น** แดง = แก้ทันที
  (ไม่ใช้ประโยค "waiting on gate — routine" ตามที่ §22 ห้าม)

## สถานะท้ายรอบ
- **push แล้ว รอ merge PR `pirate-force-server#736`** — เปิดแล้ว ไม่ draft · marker `PF-AUTOMERGE: v4`
  ยืนยันด้วย GET หลังเปิด · สถานะ: **เปิดแล้ว รอเกต** (`GATE_UNVERIFIED`)
- **push แล้ว รอ merge PR `pf_bridge#1138`** (claim PR) — เติม marker หลัง push ไฟล์รอบนี้ = ปลดล็อก
- 🔴 ห้ามอ่านว่า "เสร็จ" หรือ "อยู่บน main" จนกว่า workflow จะ merge จริง และรอบถัดไปเห็น `merged=true`

-- LANE-GM รอบ `zjbjys`

# LANE-A รอบ `ihjytc` — 2026-09-05 16:22-17:0x +07:00

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน**
เมื่อวาน พิมพ์ `/warp 126` แล้วจอไม่ขยับ ต้องล็อกเอาต์แล้วล็อกอินใหม่ถึงจะไปถึงทะเล
วันนี้ พิมพ์แล้วเมืองหายกลายเป็นทะเลตรงหน้าในวินาทีเดียว เหมือน `/warp 2` ทุกประการ

---

## รอบนี้ขยับ NOW ข้อไหน
ขยับ **`GM-A /warp <เลขแมพ>`** ในหัวข้อ "ต่อคิวทันทีหลังสองข้อบน" — ใบ `1346` (`LANE-A` รอบ 14:21 ตก 15:51) ที่ค้างมาหนึ่งรอบ
และขยับ **`P-1`/`M2`** ทางอ้อมผ่านการแก้หัวใบ `RE-227` + ร่างใบ `RE-265` (ใบ `1348` ข้อ 3/4)

**ที่ไม่ขยับและเพราะอะไร**
- ใบ `1348` **ข้อ 6 (ข้ามขอบทะเล 304/305)** — ไม่ลงในรอบนี้ **โดยตั้งใจ ไม่ใช่เพราะหมดเวลา**: ชุดแถว `MARKER` จริงของ 304/305
  คือ **7 กับ 11 แถว** ไม่ใช่ 3 กับ 3 ตามที่ใบเขียน · มีแถวพิกัดซ้ำกันสองแถว (`n_ID 70`/`347`) และแถวจุดกำเนิดเสื่อม `(0,0,100)` (`n_ID 348`)
  ⇒ กติกา "เลือกไม่ได้ = แถวแรก" กลายเป็นการเดา · เขียนคำถามแล้วเดินต่อ: จดหมาย `20260905_1639_LANE-A-ASK-COO-sea-edge-304-305-*.md`
  เลือก **(A) เกณฑ์ทิศเข้า** ไปก่อน (`304` → `n_ID 343` · `305` → `n_ID 345`) ติดป้าย `[สมมติของสาย A - รอ COO ยืนยัน]` · ยังไม่ commit ค่าลง registry
  อีกสองตัวบล็อกที่จริงกว่าเวลา: (1) แถว 304/305 ยังไม่เคยอยู่ใน registry เลย ต้องมี `table_row` ครบ 14 คอลัมน์ + `native_sha256`
  (2) แถว `MARKER` 20/21/41/... ไม่มีใน `world_marker_crosswalk.json` ที่คอมมิตไว้ ⇒ ต้อง regenerate สำเนา + `COPY_SHA256` ในคอมมิตเดียวกัน
  **= งานแรกของรอบถัดไปของสาย A**
- **world registry ของ "ของบนพื้นต่อฉาก"** (`1152` ข้อ 2/3 · chief `1446`) — ไม่ขยับรอบนี้ เพราะ `NOW.md` + ใบ `1346` เป็นคำสั่งเจ้าของและมาก่อน
  อยู่ในคิวถัดจากข้อ 6

---

## 1. งานหลัก — จุดมาถึงถาวรของฉาก 126 (ใบ `1346` · `PANYA-DECISION 1329`)

### ปัญหาที่วัดได้ก่อนแก้
`gm/warp_executor.warp_no_coords_live_target(126)` คืน `None` ⇒ `/warp 126` ไป stage แทนที่จะวาปสด
เกตอยู่ที่ `has_authored_entry` = `entry_marker != 0` และ `entry_marker` มาจาก `SCENE_NAME[126].n_MARKER` ซึ่ง **เป็น 0**
แต่ `CONSTDATA_TH__MARKER.tsv` แถว `n_ID 17` carries `n_SCENE 126` ที่ `(3050, 232, 90)` `n_DIRTECTION 6` — ไคลเอนต์มีจุดนั้นอยู่แล้ว
เพียงแต่คอลัมน์ `n_MARKER` ของฉาก 126 ไม่ได้ชี้กลับไปหามัน

### ทางที่เลือก — เพิ่ม "การปักโดยเจ้าของ" เป็นทางที่สอง ไม่ใช่ทำให้เกตเดิมอ่อนลง
คำสั่ง COO ข้อ 3 มีสองครึ่ง: ให้ 126 มี arrival ที่ `has_authored_entry` เป็นจริง **และ** ห้ามอ่อนตัวการตรวจ `n_MARKER` ของฉากอื่น

- `scenarios/world_scene_registry_001.json` แถว 126: บล็อกใหม่ `decreed_arrival = {marker_n_id: 17, heading: 6, authority, reverse_lookup}`
  · `evidence_tier` ย้าย `decreed_provisional` → **`decreed_permanent`** (tier ใหม่ · PANYA บอกว่าถาวร ⇒ ไม่มีวันหมดอายุอีก)
  · `from_marker` ยัง `false` · `marker_n_id` ยัง `null` · `n_MARKER` ยัง `0` — **rule 1 ยังไม่ถึงฉากนี้ ไม่มีอะไรในกฎเดิมถูกแก้**
- `world_scene_travel.py`: แยกข้อเท็จจริงออกจากเกต
  · `has_table_authored_entry` = `entry_marker != 0` — **ข้อเท็จจริงบริสุทธิ์จากตารางไคลเอนต์ ค่าเดิมทุกฉาก**
  · `has_decreed_arrival` = มีบล็อก decree ที่ผ่านการตรวจ
  · `has_authored_entry` = อย่างใดอย่างหนึ่ง ← **เกตที่ `warp_executor` อ่าน**
- `world_scene_marker.py`: `DECREED_ARRIVAL_ROWS = ((17, 126, 3050, 232, 90, 6),)` + `decreed_arrival_row(marker_n_id)`
  อ่าน **ทิศ MARKER → SCENE เท่านั้น** และคืน `n_SCENE` ของแถวมาให้ผู้เรียกตรวจย้อน
- **ไม่แตะไฟล์ `gm/` เลยแม้แต่บรรทัดเดียว** (ใบ `1346` ข้อ 5) — `git diff` ยืนยัน

### สี่ชั้นที่กันไม่ให้ decree กลายเป็น self-report
loader ปฏิเสธเมื่อ (1) ฉากนั้นมี `n_MARKER != 0` อยู่แล้ว (rule 1 ตอบได้ ห้ามมีประตูหลัง)
(2) marker id ที่อ้างไม่ได้ถูกปักไว้ใน `DECREED_ARRIVAL_ROWS` (3) แถวนั้น `n_SCENE` ไม่ได้ชี้กลับมาที่ฉากนี้
(4) `spawn` ไม่ได้ยืนบนพิกัดของ marker นั้นเป๊ะ · และ heading ต้องตรงกับ `n_DIRTECTION` ของแถว
บวกอีกสองทาง: tier `decreed_permanent` ที่ไม่มีบล็อก = ปฏิเสธ · บล็อกที่ไม่มี tier = ปฏิเสธ
**เจ็ดกรณีนี้มีเทสมิวเตทจริงทีละกรณีใน `tests/test_world_scene_decreed_arrival.py`** (แก้ JSON ในโฟลเดอร์ชั่วคราว ไม่แตะไฟล์ที่ shipped)

### 🔴 จุดที่เกือบพลาด และเทสของโปรเจกต์จับได้
ฉบับแรกผมให้ `world_scene_travel` **import `world_marker_copy`** เพื่อตรวจพิกัดกับสำเนา crosswalk โดยตรง
`tests/test_world_marker_copy.py::test_no_module_in_the_package_imports_the_copy_reader` แดงทันที และมันถูก:
**`world_marker_crosswalk.json` ไม่ได้ถูกใส่ใน release archive** ⇒ ถ้าปล่อยไป `load_scene_registry()` จะพังทุกบูตของบิลด์ที่ปล่อยจริง
ทางแก้ = ใช้รูปแบบเดียวกับ `_ROWS`: **ปักแถวไว้ในโมดูล และให้ "เทส" เป็นตัวสอบทานกับสำเนาที่คอมมิตไว้**
(`TheCoordinateIsCrossExamined` ใน `test_world_scene_decreed_arrival.py`) — พิกัดถูกถอดความครั้งเดียว ถูกสอบทานครั้งเดียว
บันทึกไว้ตรงนี้เพราะมันคือเหตุผลที่กติกา "ห้าม import สำเนา" มีอยู่ ไม่ใช่พิธีกรรม

### สองอย่างที่รักษาความหมายเดิมไว้ ไม่ให้ decree ไปเปลี่ยนคำที่คนอื่นเชื่อ
- `entry_report["needs_return_ticket"]` เปลี่ยนไปอ่าน `has_table_authored_entry`
  **ฉาก 126 ยังติดหนี้ตั๋วขากลับอยู่** — มีที่ให้ลงไม่ใช่มีทางกลับ (`n_SAVE = 0` และประตูล็อกอินยังปิด)
- `world_travel_gate` คีย์ `destination_has_authored_entry` เปลี่ยนไปอ่านตัวเดียวกัน (ชื่อคีย์บอกว่า "authored" ⇒ ต้องหมายถึงตารางไคลเอนต์)
  เพิ่มคีย์ใหม่ `destination_arrival_is_decreed` แทนที่จะยัดสองความหมายลงคีย์เดียว
- `entry_console_line` เติมท้าย ` decreed_arrival=17` **เฉพาะฉากที่มี decree** — เพราะ `GT-079` อ้างบรรทัดของฉาก 278 แบบตัวต่อตัว
  (เทส `test_world_scene_entry.py` จับได้ตอนฉบับแรกเติมแบบไม่มีเงื่อนไข)

### หลักฐานสองชั้นที่มีจริงในรอบนี้
- **wire/DB**: `warp_no_coords_live_target(126)` คืนเป้า `(3050, 232, 90)` · `17/278/997` ยังคืน `None`
  บรรทัดคอนโซล: `WORLD_SCENE scene_id=126 ... save=0 marker=0 return_ticket=REQUIRED decreed_arrival=17`
- **dispatch (วัดจริงในรอบนี้ ไม่ใช่การอนุมาน)**: ขับ `make_gm_chat_command_action` ด้วย fake session ของชุดเทส
  `/warp 126` → **`action=FRAME`** (เหมือน `/warp 2`) · `/warp 278` → `action=None` + `GM_CHAT_STAGED_NEXT_LOGIN`
  = ก่อนรอบนี้ `/warp 126` เดินเส้นเดียวกับ 278 วันนี้เดินเส้นเดียวกับ 2
- 🔴 **หลักฐานที่ดีที่สุดของรอบนี้ มาจากเทสที่แดง ไม่ใช่จากเทสที่ผมเขียนเอง**:
  `tests/test_gm_chat_frame_tail.py::R313CapturedFrameTests::test_the_captured_frame_reaches_the_route_and_is_executed`
  ขับ **ไบต์จริงที่ R313 จับได้** ของคำสั่ง `/warp 126` เข้าเส้นทาง dispatch แล้วปักว่าคอนโซลต้องมี `scene_id=126`
  หลังรอบนี้มันแดง เพราะบรรทัดนั้นคือบรรทัดของสาขา **staging** ซึ่งไม่ถูกพิมพ์อีกแล้ว — สาขาที่เดินตอนนี้คือ live (`scene=126`)
  ⇒ เฟรมจริงจากเครื่องของ Panya เปลี่ยนเส้นทางจริง ไม่ใช่แค่ฟังก์ชันตัวเดียวเปลี่ยนคำตอบ
  แก้เทสนั้นแล้ว: ปักที่ "คอนโซลต้องมีเลขฉาก 126" **และ** "ต้องไม่มี `GM_CHAT_STAGED_NEXT_LOGIN`" (ปักสาขาแบบบวก ไม่ใช่ปล่อยหลวม)
- **client-observable**: ยังไม่มี — เป็นของ `GT-266` (เนื้อใบส่งให้ chief แล้ว) และใบ `1347` ของ LANE-GM

### 🔴 สิ่งที่กว้างขึ้นจริง และบันทึกไว้แล้ว (ไม่ใช่แค่การเปลี่ยนเส้นทาง)
เส้นทาง live ของ `/warp` **ไม่ปรึกษาตารางสิทธิ์ของ staging เลย** · วัดบนกิ่งนี้:
`stageable_scene_ids()` = `(1..11, 14, 130, 278, 997)` — **ยังไม่มี 126** · `single_use_stageable_scene_ids()` มี 126 (ผ่าน `SANCTIONED_BARRED_SCENES`)
ก่อนรอบนี้ การที่ 126 ไม่อยู่ในตารางแรกคือสิ่งที่กัน GM ที่ไม่มีสิทธิ์ single-use ออกจาก 126
**หลังรอบนี้ GM ทุกบัญชีที่ผ่านเกต `/warp` วาปสดไป 126 ได้** — เป็นสิ่งที่ `PANYA-DECISION 1329` สั่งตรง ๆ
บันทึกไว้ใน `why_the_door_is_shut` ของแถว 126 เอง เพราะมันคือการเปลี่ยน **สิทธิ์การเข้าถึง** ไม่ใช่แค่เส้นทาง
ที่ **ไม่** กว้างขึ้น: `login_entry_allowed` ยัง `false` · ไม่มีผู้เล่นที่ไม่ใช่ GM มีเส้นทางใดไปถึง 126

### สิ่งที่รอบนี้ **ไม่** ทำ
- ไม่เปิดประตูล็อกอินของ 126 (`login_entry_allowed` ยัง `false` · `COO-DECISION 20260829_1444` ต้องมี attended var2 test ก่อน)
  ⇒ ล็อกอินใหม่ขณะแถวเป็น 126 คาดว่าจะถูกดีดกลับพร้อม `WORLD_SCENE_ENTRY_REFUSED` — เขียนเป็น non-claim ไว้ในใบ `GT-266` แล้ว
- ไม่ยุ่งกับคำถาม var2 ของ `QUESTDATA` แถว 3021 (ยังค้างที่ `COO-DECISION 20260830_1351`) — เจ้าของตัดสินว่า *จุดมาถึงอยู่ที่ไหน* ไม่ได้ตัดสินว่าแถว 3021 แปลว่าอะไร
- ไม่ส่ง heading ไปกับเฟรม (`n_DIRTECTION 6` บันทึกไว้เฉย ๆ) ตาม `1346` ข้อ 3 ที่ห้ามเดา

`TWO_SESSIONS_SAME_SCENE:` N/A — รอบนี้ไม่ได้สร้าง state ของโลกใด ๆ · registry เป็นข้อมูลอ่านอย่างเดียวที่ทุก session อ่านตัวเดียวกันอยู่แล้ว

---

## 2. กล่องจดหมาย — บริโภคครบสี่ใบ
| ใบ | ทำอะไร |
|---|---|
| `1346` COO (warp 126) | ครบ 5 ข้อ · stub เขียนแล้ว |
| `1348` COO (R318/GT-233) | ข้อ 3 (ร่าง `RE-265` + ตอบ (ค) เอง) · ข้อ 4 (แก้หัว `RE-227`) · **ข้อ 6 ยังไม่ลง** เหตุผลข้างบน |
| `1404` chief R354 | รับ `GT-264` · ส่งเนื้อใบ `GT-266`/`RE-265` กลับ · `GT-267` รอคำเคาะ |
| `1446` chief R354b | รับการถอนคำอ้าง `#827` · registry ของพื้นเข้าคิวสาย A |

**หัวใบที่แก้เอง**: `CLIENT_RE_QUEUE.md` `RE-227` → `primary hypothesis REFUTED-ON-SCREEN (R318) · covered by RE-265`
ขีดฆ่าข้อความเดิมทั้งก้อน ไม่ลบ (`GT-233` R318 เข้าใกล้เกาะ 37 หน่วยแล้วหน้ารายงานไม่เด้ง = ชั้น ① ถูกหักล้างบนจอ)

**ของแถมที่วัดได้**: `pf_bridge/gamedata/scene/Bg3001/Bg3001.placements.tsv` (sha256 `571c147f...` ตรงกับ `native_sha256` ของแถว 126)
มีแต่ placement ของ NPC/Mob_Set **ไม่มีตารางทริกเกอร์** · และ id ที่ R318 เห็น (2,3,7,35,48,57,69) เทียบกับ `template_ids` ทั้ง 38 แถว
**ตรงแค่ 2 กับ 7 · อีกห้าตัวไม่มีเลย** ⇒ trigger id ไม่ใช่ template id เป็นคนละ namespace (ยืนยันความกังวลของ `RE-234` ข้อ 3 ด้วยตัวเลข)

---

## 3. ไฟล์ที่แตะ
`src/pirateforce_foundation/world_scene_travel.py` · `world_scene_marker.py` · `world_marker_copy.py` · `world_travel_gate.py`
`scenarios/world_scene_registry_001.json` · `tests/test_world_scene_decreed_arrival.py` (ใหม่) · `tests/test_world_scene_travel.py` · `tests/test_world_scene_marker.py`
`tests/test_gm_chat_frame_tail.py` · `tests/test_gm_chat_no_bytes_line.py` · `src/pirateforce_foundation/gm/warp_chain_preflight.py`
`src/pirateforce_foundation/gm/warp_executor.py` (docstring + ข้อความปฏิเสธ) · `src/pirateforce_foundation/gm/chat_command_action.py` (คอมเมนต์) · `docs/GM_LANE.md`
🔴 ข้ามเขต **หลายจุดในไฟล์ `gm/`** — ทั้งหมดเกิดหลัง pf-adversary และทั้งหมดเป็นเพราะรอบนี้ทำให้ของเดิม**ผิดหรือแตก** ไม่ใช่การขยายงาน:
1. `tests/test_world_scene_marker.py` allowlist ของ public API ถูกขยายเพื่อรับ `decreed_arrival_row`
   — เทสตัวนั้นออกแบบมาให้ "การขยายเป็นการกระทำโดยเจตนา" เหตุผลสามข้อเขียนไว้ในคอมเมนต์ข้าง ๆ allowlist เอง
2. `tests/test_gm_chat_frame_tail.py` (LANE-GM) — assertion เดียว · รอบนี้ทำให้บรรทัด staging ที่มันปักหายไป
3. `tests/test_gm_chat_no_bytes_line.py` (LANE-GM) — เปลี่ยน "พาหนะ" จาก `/warp 126` เป็น `/warp 278`
   คอมเมนต์ในเทสตัวนั้น**เตือนเรื่องนี้ไว้เองอยู่แล้ว** ("แทนที่จะพึ่งว่า 126 จะไปไม่ถึงตลอดไป") · หัวข้อของเทสคือบรรทัด `blocker=` ไม่ใช่ฉาก 126
4. `gm/warp_chain_preflight.py` (LANE-GM) — **เป็นการแก้ D2 ไม่ใช่การขยายงาน**: ถ้าไม่แก้ โซ่ `GT-192` ของเจ้าของจะกลายเป็น 14 ฉากเงียบ ๆ
5. `gm/warp_executor.py` (docstring + ข้อความปฏิเสธที่ GM อ่าน) · `gm/chat_command_action.py` (คอมเมนต์) · `docs/GM_LANE.md`
   — ทั้งสามบอกกฎเก่าซึ่งรอบนี้ทำให้**เป็นเท็จ** · ขีดฆ่าไม่ลบ
ทุกจุด: cc LANE-GM ในจดหมาย `1655` และ `1708` · เจ้าของย้อนได้ทุกเมื่อ · ไม่แตะ `runtime.py`/`app.py` เลย

## 3b. 🔴 pf-adversary จับได้ 9 ข้อ — แก้ 8 บันทึก 1 (ทั้งหมดวัดจริง ไม่ใช่ข้อกังวล)
| # | สิ่งที่จับได้ | ทำอะไร |
|---|---|---|
| D1 | **เทสแตก 4 ตัว** (`test_gm_warp_chain_preflight.py` ×3 · `test_gm_chat_no_bytes_line.py` ×1) เกตวินโดวส์จะแดง | แก้ครบ |
| D2 | 🔴 **126 แอบเข้าไปในโซ่ `GT-192` ของเจ้าของ** — `reachable_scene_ids()` derive จากเกต ⇒ 13 ฉากกลายเป็น 14 · ผู้เทสจะถูกสั่งให้วาปเข้า Atlantis ซึ่งไม่มีตั๋วขากลับ | กันไว้: โซ่รับเฉพาะฉากที่ **ตารางไคลเอนต์** เปิด (`has_table_authored_entry`) · decree ไม่พาเข้าโซ่ · ปักเทสว่ายัง 13 |
| D3 | 🔴 **การเขียนแถวถาวรถูกปฏิเสธที่ 126** (`login_would_accept` → False เพราะ `login_entry_allowed=False`) ⇒ ขัด `PANYA 1430` · ก่อนรอบนี้ `/warp 126` + relog เคยพาไปถึงจริง | **ไม่แก้ ตัดสินใจแล้วและติดป้าย** — ดูข้างล่าง |
| D4 | `decreed_arrival_row(17)` คืนพิกัดของฉาก 126 · **17 เป็นเลขฉากจริงด้วย** และเป็นกับดักที่โมดูลนี้ยกเป็นตัวอย่างของตัวเอง | เปลี่ยน API เป็น `(scene, marker)` ทั้งคู่ · คืนพิกัดโดยไม่คืน `n_SCENE` · ปักเทสทุกสะกดของเลข 17 |
| D5 | ข้อความ `reverse_lookup` ในไฟล์ข้อมูล **โกหก** (บอกว่า loader ตรวจกับ `world_marker_copy` ซึ่งเป็นไปไม่ได้) | เขียนใหม่ให้ตรงกับสองฮอปจริง + ระบุชัดว่า **ไม่มีอะไรตรวจข้อความร้อยแก้วสองช่องนี้** |
| D6 | docstring/ข้อความปฏิเสธที่ GM จะอ่าน ยังบอกกฎเก่า 3 ที่ | แก้ `warp_executor.py` ×2 · `chat_command_action.py` ×1 · `GM_LANE.md` |
| D7 | อ้าง "GT-182 nonclaim 4" แบบอ่านจาก 4 ฉากเหลือ 3 โดยไม่มีใบแก้ | เขียนใหม่: nonclaim 4 ยังคุม 3 ฉาก · เจ้าของตัดสินฉากที่สี่แยกต่างหาก |
| D8 | `[PROPOSED]` `GM_WARP_POSITION_CONFIRMED` อาจยิงทั้งที่ persist ล้ม (`runtime.py:4224-4229` อ่าน parked target · park ทำก่อน persist) · **126 คืออินพุตแรกที่แยกสองอย่างนี้ได้** | `runtime.py` เป็นของ chief — ส่งเป็นข้อ 3 ของจดหมาย `1708` |
| D9 | ไฟล์เทสใหม่ยัง untracked | `git add` แล้ว |

**ผ่านการโจมตีโดยไม่ต้องแก้**: `GT-141` เขียวตลอด · ไม่มีโมดูล production import `world_marker_copy` · loader ต้านมิวเทชันจริง
(`spawn.z += 1e-7` → ปฏิเสธ · heading ผิด → ปฏิเสธ · tier/block ขาดข้างใดข้างหนึ่ง → ปฏิเสธ) · ท้าย `entry_console_line` ไม่ทำใครพัง

### D3 — ตัดสินใจแล้ว ติดป้ายแล้ว ไม่ใช่มองข้าม
`/warp 126` วาปสดได้ แต่ `character_positions` ไม่ถูกเขียน (`GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse`)
เพราะ `login_entry_allowed` ของ 126 ยัง `false` และเปิดเองไม่ได้ (`COO-DECISION 20260829_1444` ต้องมี attended var2 test)
**สิ่งที่แลกไปจริง**: ก่อนรอบนี้ `/warp 126` แล้ว relog หนึ่งครั้ง = อยู่ 126 จริง (single-use bypass) · ตอนนี้ถึงทันทีแต่ relog แล้วกลับบ้าน
เลือก **(A) ขึ้น main ตามนี้** `[สมมติของสาย A - รอ COO ยืนยัน]` เพราะ `PANYA 1329` ใหม่กว่าและเจาะจงคำสั่งนี้ฉากนี้ ·
ใบ `1347` ที่ COO ออกเองวางให้ LANE-GM วัด "วาปสด + persist" หลังรอบนี้อยู่แล้ว · ผลเสียมีขอบเขต (ฉาก GM-only · เด้งกลับบ้าน ไม่ล็อกออก)
**ทำให้ดังแทนที่จะเงียบ**: ปักเทส `TheDurableHalfIsRefusedAndSaysSo` ว่า **126 เป็นฉากเดียวในเกมที่เป็นแบบนี้** — วันที่ประตูเปิด เทสพลิกเอง
จดหมาย: `20260905_1708_LANE-A-ASK-COO-warp-126-live-but-not-persisted-*.md` · non-claim อยู่ในใบ `GT-266` แล้ว
**ย้อนทั้งก้อนได้ด้วยการลบบล็อก `decreed_arrival` ออกจากแถว 126 บล็อกเดียว ไม่ต้องแตะโค้ด**

## 4. ชุดเทส
`BYTECODE_PURGED:` ใช่ — ลบ `__pycache__` ทั้งต้นไม้ก่อนรัน และรันทั้งรอบด้วย `PYTHONDONTWRITEBYTECODE=1` (กติกา COO `1446`)
ระหว่างทางรันเฉพาะไฟล์ที่เกี่ยวข้อง · **ชุดเต็มรันบน commit สุดท้าย หลังแก้ตาม pf-adversary ครบแล้ว**

**ผล: `1 failed, 11056 passed, 327 skipped, 20358 subtests passed` (749.73s)**

ตัวที่แดงตัวเดียวคือ `tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_the_shipped_tables_when_it_can_run`
**ไม่ใช่ของรอบนี้**: `tools/pf_equip_attack_behavior_extract.py` **ไม่เคยถูก commit ลง main** ⇒ แดงบน clone ใหม่ทุกครั้ง
= ตัวเดียวกับที่ LANE-CS รายงาน (`1510_LANE-CS-TO-COO-pre-existing-red-test-on-main-*`) และ LANE-GM ยกซ้ำ (`1534`)
ตัวแก้ของ LANE-B อยู่ใน `pirate-force-server#832` ซึ่ง **ปิดโดยไม่ merge** (`1548_SYNC-NOTICE-*`)
diff ของรอบนี้ไม่แตะ `combat_pose` / `tools/` / `.gitignore` เลย · ยืนยันด้วย `git log origin/main -- tools/pf_equip_attack_behavior_extract.py` = ว่างเปล่า

รันชุดเต็มกี่ครั้ง: **ครั้งเดียวบน commit สุดท้าย** (มีการรันชุดเต็มรอบแรกโดย pf-adversary ในกิ่งชั่วคราวของมันเอง ซึ่งเป็นตัวที่จับ D1 ได้ — ไม่ใช่การรันของผม)

## 5. สถานะจบรอบ
**push แล้ว รอ merge PR `pirate-force-server#838`** — เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` อยู่ใน body ตั้งแต่เปิด (GET กลับมายืนยันแล้ว) · **รอ gate**
ฝั่ง `pf_bridge`: ไฟล์รอบ + จดหมาย 5 ใบ + stub 4 ใบ + แก้หัวใบ `RE-227` ลงกิ่ง claim แล้ว · claim PR `#1345` เติม marker = ปลดล็อก
🔴 ห้ามอ่านข้อนี้ว่า "เสร็จ" หรือ "อยู่บน main" — งานอยู่บน main ต่อเมื่อรอบถัดไปเห็น `merged=true`

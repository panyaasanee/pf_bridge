# LANE-GM รอบ `awgcfu` -- 2026-09-06T00:01+07:00

รหัสรอบ: `awgcfu` · server PR `pirate-force-server#864` (เปิดแล้ว ไม่ draft · marker ยืนยันด้วย GET ·
รอ gate) · pf_bridge PR (เลขเติมหลัง push -- ดูท้ายไฟล์นี้)

## ล็อกรอบ

🔴 **สารภาพการข้ามขั้น**: รอบนี้ไม่ได้เปิด claim PR เปล่าก่อนอ่านกล่องจดหมาย/แตะโค้ด (ต่างจากที่
`prompts/COMMON_LANE_ROUND.md` ข้อ 6 สั่ง) -- อ่าน `COMMON_LANE_ROUND.md`/`prompts/LANE-GM.md`/
`AGENTS.md` §7/ไฟล์รอบล่าสุดก่อน แล้วค่อยตัดกิ่งและลงมือเลย เพื่อลดความเสี่ยงเรื่องเวลา แก้ตัวด้วยการ
`list_pull_requests` ตรวจ `[LANE-GM]` ซ้ำ **สามครั้ง** ตลอดรอบ (ก่อนเริ่ม, หลัง fetch ครั้งที่สอง ตอน
`checkout -B`, และก่อนเปิด PR จริง) -- ไม่มีใบ `[LANE-GM]` เปิดอยู่ทุกครั้งที่ตรวจ ⇒ ไม่มีการชนกับรอบอื่น
จริง แต่กระบวนการเองผิดขั้น บันทึกไว้ตรงนี้ตามกฎ (เทียบ `LANE-GM-SELFCORRECTION` รอบก่อน ๆ)

ตรวจ (ครั้งที่ 3, ก่อนเขียนไฟล์นี้): `list_pull_requests` state=open ทั้งสองรีโป กรองหัวขึ้นต้น
`[LANE-GM]` = **ไม่มีเลย** (bridge เปิดอยู่: `#1386` CS · `#1377` UI yield · `#1336` courier ·
server: ไม่มี `[LANE-GM]` อื่นนอกจาก `#864` ที่รอบนี้เพิ่งเปิด)

`main` ขยับสามครั้งระหว่างรอบ (`pf_bridge`: `ed1eaf9` -> `53e1735` · `pirate-force-server`: `a7136e4` ->
`23e2a37` -> `387666e`) -- fetch ใหม่ทุกครั้งก่อนเขียนอะไรที่อ้างว่า "อยู่บน main" ตามกฎ

ยืนยัน `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ตรวจแล้วต้นรอบ)

## กล่องจดหมาย

`ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` เมื่อเริ่มรอบ = **4 ใบ** (grep ตรง ๆ เจอ 6 hit แต่ 2
ใบ ["0558", "0855"] เป็น false positive -- คำว่า `ADDRESSEE: LANE-GM` ปรากฏในเนื้อหาที่เป็นการรายงานผล
grep ของตัวเอง ไม่ใช่บรรทัด `ADDRESSEE:` จริง ของใบนั้น (`ADDRESSEE:` จริงของทั้งสองใบคือ `COO`) --
ตรวจแล้วก่อนนับ):

1. `1347` (`COO-DECISION warp-126`) -- ปิดตามที่ `2051` บอก: วัด
   `git merge-base --is-ancestor 1801c90 origin/main` = **true** (ยืนยันจริงรอบนี้) ⇒ consumed as
   superseded/closed
2. `2051` (`COO-DECISION gm1933`) -- รับทราบ · เช็คว่า PR ของ chief (ที่กลืน D3/D4/GM-060 เข้า
   `runtime.py`) ขึ้น main หรือยัง: **ยัง** (grep `git log --grep GM-060`, grep
   `_restore_selected_scene`/snapshot-restore ใน `runtime.py`, และเช็คว่า `docs/PROMOTION_BACKLOG.md`
   มีจริงหรือยัง -- ไม่มีทั้งสามอย่าง ณ commit `387666e`) ⇒ **ไม่ทำการหด `_restore_selected_scene`
   รอบนี้** ตามที่ใบสั่งไว้ชัดว่าให้ทำ "รอบแรกหลัง PR chief ขึ้น main" เท่านั้น -- consumed เป็น
   "รับทราบ, งานเลื่อนจริง (ไม่ใช่เงียบ)"
3. `2150` (`COO-DECISION` ปิด `1928`/`2110`, เตือน `rm -rf` ครั้งเดียว) -- รับทราบ ไม่มีคำสั่งใหม่ ·
   ไม่ใช้ `rm -r`/`rm -rf` ทุกการสะกดตลอดรอบ (ตรวจแล้ว: ไม่มีการเรียก `rm` เลยในรอบนี้ -- ไม่มีการมิวเทต
   ไฟล์ใดที่ต้องคืนด้วย `cp`/`Write`)
4. `2348` (`COO-DECISION` ตอบ `ASK-COO 2232`: สีเป็นคุณสมบัติของคู่ (คนดู, มอน), จุด compose = chief,
   faction-only ยังห้าม, งานแรกรอบถัดไป = ยื่น `CORE-REQUEST-GM-<nnn>`) -- **ทำจริงรอบนี้**: ยื่น
   `CORE-REQUEST-GM-061` (จดหมายแยก, ดูหัวข้อถัดไป)

ทั้ง 4 ใบ: คัดลอกต้นฉบับไป `notes_to_chief/consumed/` แล้ว · วาง `.CONSUMED.txt` ข้างต้นฉบับ (ไม่ลบ/ย้าย
ต้นฉบับ)

## รอบนี้ขยับ NOW ข้อไหน

- **ไม่มีข้อ NOW ขยับสถานะ DONE/COMING** -- รอบนี้เป็นการจ่ายหนี้ pf-adversary (D4/D8/D10/D11 จากรอบ
  `y1evqj`) บวกยื่น CORE-REQUEST หนึ่งใบ ไม่มีฟีเจอร์ใหม่ที่ผู้เล่นเห็นบนจอ
- P-2 (สีชื่อมอน): ยังคง STUCK เหมือนเดิม -- `CORE-REQUEST-GM-061` เป็นการขอจุดเสียบจาก chief ไม่ใช่
  โค้ดที่ใช้งานได้ · P-3 (ปุ่ม GM): ไม่แตะรอบนี้ (เวลาทั้งหมดไปที่หนี้ adversary + CORE-REQUEST)

## งานที่ 1 (หลัก) -- จ่ายหนี้ pf-adversary D4/D8/D10/D11 จากรอบ `y1evqj`

อ่านรายงานเดิมจากไฟล์รอบ `y1evqj` เอง (`rounds/GM_20260905_2211_y1evqj_p3_denominator_17_rows_and_re222_answer_surfaced.md`
หัวข้อ "pf-adversary" และ "รอบหน้าทำอะไร" ข้อ 1) เพราะไม่มี PR review comment แยก (`#856` merge แล้ว
ไม่มี comment thread ให้ดึงรายละเอียดเพิ่ม -- ตรวจแล้วด้วย `pull_request_read get_comments` = ว่าง)

- **D4**: `gm/name_color_gate.py` เขียนว่า "the two sites that emit the name style" ในบริบท `RE-263`
  (ถูกต้องสำหรับเลน local `CMyActor` เท่านั้น -- `RE-263` เดินแค่เลนนั้น) แต่ประโยคนี้ถูกอ่านเป็น
  "ตัว selector มีจุด emit สองจุด" ทั้งที่ `PF_ATTR_NAME_COLOR_SELECTOR.tsv` (อ่านทั้งไฟล์รอบนี้ -- 15
  บรรทัด = 1 header + **14 แถวข้อมูลจริง**: 2 `typed_CMyActor_local` · 9 `untyped_dynamic_controller` ·
  3 `typed_CNetNPC`, ยืนยันด้วย `cut -f2 ... | sort | uniq -c`) มี 14 แถว ไม่ใช่ 2 -- แก้ด้วยค่าคงที่ใหม่
  `PF_ATTR_NAME_COLOR_SELECTOR_TSV_ROW_COUNT = 14` และแก้ประโยคเดิมให้ระบุชัดว่า "the two **LOCAL**
  emit sites" ไม่ใช่ "the" emit points เฉย ๆ -- ไม่ได้เดา/เติมรายละเอียดที่ตารางไม่มี (คำอธิบาย 14 แถว
  ในคอมเมนต์ใหม่เป็นการสรุปคอลัมน์ `selector_lane`/`output_fontstyle_id` ของตารางจริง ไม่ใช่การตีความ
  เพิ่ม)
- **D8**: โมดูล/คอมเมนต์อ้างตารางเดียวกันด้วยชื่อไฟล์เปล่า (ไม่มี path) ซึ่งอ่านเป็นว่าอยู่ `external/`
  โดยเทียบเคียงกับตารางพี่น้องในแพ็กเกจเดียวกันที่อยู่ `external/` จริง (`PF_SERIALIZER_FIELDS.tsv`,
  `PF_PROTOCOL_REGISTRY.tsv`) -- ยืนยันตำแหน่งจริงด้วยการ `find`/`grep` ตรงในโคลน `pf_bridge`:
  `notes_to_chief/reference_codex_attr/PF_ATTR_NAME_COLOR_SELECTOR.tsv` (ไม่ใช่ `external/`) -- แก้ด้วย
  ค่าคงที่ `PF_ATTR_NAME_COLOR_SELECTOR_TSV_PATH` ที่ pin path เต็ม และแก้ทุกจุดที่อ้างชื่อไฟล์เปล่า
- **D10**: `tests/test_gm_p2_color_call_site_tripwire.py` สแกนหาโทเคนสี (`FontStyleID`, `name_color`,
  ...) เฉพาะใน `gm/` -- มองไม่เห็น `field_mobs.py` ซึ่งตาม `COO-DECISION 20260905_2348` เป็นไฟล์ที่จุด
  compose สีต่อ (คนดู, มอน) จริงน่าจะไปแตะ (ผ่าน `hostile_actor_entry`) -- เพิ่มการสแกน
  `field_mobs.py` **อ่านอย่างเดียว** (ค่าคงที่ `FIELD_MOBS_PATH` ใหม่ + เทส
  `test_field_mobs_is_scanned_for_p2_colour_tokens_read_only`) พร้อมเทสแยกยืนยันว่า call เดียวที่ทำกับ
  path นี้คือ `.exists()` (ตรวจด้วย AST parse ของฟังก์ชันเทสเอง ไม่ใช่การ grep string ที่ตัวเองชนตัวเอง
  -- ลองแบบ string-match ก่อนแล้วพบว่ามันจับสตริงในเทสตัวเองผิดพลาด แก้เป็น AST-based) -- **ไม่แก้
  `field_mobs.py` แม้แต่ไบต์เดียว** (นอกเขตเขียนของสายนี้) วันนี้ `field_mobs.py` สะอาด (ไม่มีโทเคนสีใน
  executable code -- คอมเมนต์ที่มีคำว่า FontStyleID เป็น docstring ซึ่งเทสเว้นให้อยู่แล้ว) เทสจึงเขียว
  โดยไม่มีการเปลี่ยนพฤติกรรมที่วัดได้
- **D11**: แก้ citation หลวมสองจุด: (1) `"Read the letter when a human needs a number"` ไม่ได้ชี้ว่าใบ
  ไหน ทั้งที่ `RE_191_RESULT_LETTER` ถูก pin ไว้ไกลออกไป ~200 บรรทัด แก้เป็นชี้ตรงไปที่ชื่อค่าคงที่
  (2) ประโยค `"...and in PF_ATTR_NAME_COLOR_SELECTOR.tsv"` (ไม่มี path, ซ้ำกับ D8) แก้ให้เต็มพร้อมชี้ไป
  ยังค่าคงที่ใหม่ทั้งสอง

**ไฟล์ที่แตะ** (4 ไฟล์ ทุกไฟล์อยู่ในเขตเขียนของสายนี้): `src/pirateforce_foundation/gm/name_color_gate.py`
· `tests/test_gm_name_color_gate.py` · `tests/test_gm_p2_color_call_site_tripwire.py` ·
`docs/GM_LANE.md` -- **ไม่แตะ** `field_mobs.py`/`runtime.py`/`app.py`/`v141`/DB/`scenarios/world_*`/
`scenarios/combat_*` (ตรวจด้วย `git diff --cached --name-only` ก่อน commit)

## งานที่ 2 -- `CORE-REQUEST-GM-061` ตาม `COO-DECISION 20260905_2348`

จดหมาย `notes_to_chief/20260906_0001_LANE-GM-CORE-REQUEST-GM-061-per-viewer-name-colour-splice-point.md`
(`ADDRESSEE: LANE-E`) -- ขอให้ chief เพิ่มจุดผูก identity ของคนดูเข้ากับการเรียก
`field_mobs.hostile_actor_entry` ต่อ session ใน `runtime.py` ตามฟิลด์ที่ COO ระบุ (`NPCAttr+0x98` tag
`0x32` 8 ไบต์ presence bit `0x08` ใน mask `+0xBC`) -- **ตรวจเองรอบนี้แค่สองข้อ** (ไม่มี client image
ตรวจ tag/mask เอง): (ก) `field_mobs.py:227`/`237` มี `BASIC_BIT_FACTION`/`BASIC_BIT_LEVEL` จริงตามที่
COO อ้างเป็นจุด splice ข้างเคียง (ข) `hostile_actor_entry` (`field_mobs.py:1932-1941`) วันนี้ไม่มี
พารามิเตอร์ "คนดู" จริง (อ่าน signature ตรง) -- ฟิลด์ไบต์ (`+0x98`/tag `0x32`/mask `+0xBC`) เป็นการ
ถอดความจาก `COO-DECISION 2348` เอง (ซึ่งอ้างอิงกับ `RE-222-RESULT` บรรทัด 119) ไม่ใช่สิ่งที่สายนี้ตรวจ
จาก client image เอง (ไม่มี image ในโคลนนี้) -- ป้าย `[PROPOSED]` ในจดหมายจนกว่าจะมีใบ GT ยืนยัน · ขอเลข
GT ในจดหมายเดียวกันตามกฎ NOW (RE ตอบแล้ว -> ใบสร้าง + ใบ GT รอบเดียวกัน)

## `pf-adversary`

**ADVERSARY_UNAVAILABLE claude/keen-pasteur-awgcfu** -- ค้นด้วย `ToolSearch` ("pf-adversary agent
subagent task") ก่อนสรุป: ไม่มี Agent/Task tool ในเซสชันนี้ที่จะสั่ง subagent จริงได้ (มีแค่ `SendMessage`/
`ListAgents` สำหรับ agent อื่นในบัญชีเดียวกัน ไม่ใช่ subagent แบบ Task) ⇒ ทำ self-review แทนตามกฎ:
- อ่านทุก hunk ใน `git diff --cached` ของทั้ง 4 ไฟล์ก่อน commit (ดูรายการไฟล์ข้างบน)
- มิวแทนต์เท่าที่ทำได้โดยไม่แตะไฟล์นอกเขต: (1) จำลอง token สีที่ไม่ consult gate ผ่าน
  `_token_hits`/`_consults_the_refusal` โดยตรง (ไม่ใช่แก้ `field_mobs.py` จริง) -- ยืนยันว่า logic ยังจับ
  ได้ (2) พลิกค่า `PF_ATTR_NAME_COLOR_SELECTOR_TSV_ROW_COUNT` เป็น `2` ชั่วคราวใน python REPL (ไม่ใช่
  ไฟล์จริง) -- ยืนยัน assertion แดง (3) รันเทสจริงสองไฟล์ที่แตะ -- 98 passed ก่อน merge origin/main
- ไม่มีการ mutate ไฟล์บนดิสก์เพื่อทดสอบ (จึงไม่มีการ `cp`/`Write` คืนไฟล์ -- ไม่มีอะไรต้องคืน)

## หลักฐาน

- `git diff --check` ว่าง (ทั้งสองรีโป)
- cp874: `tests/test_tree_is_cp874_safe.py` = 5 passed, 659 subtests (ทั้งต้นไม้ pirate-force-server)
- เทสสองไฟล์ที่แตะโดยตรง: `pytest tests/test_gm_name_color_gate.py tests/test_gm_p2_color_call_site_tripwire.py`
  = **98 passed** (ก่อน merge origin/main)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PASS** (cp874 + no
  new skips + mainmerge + census agrees + branch names ถูก + bridge file sizes ใต้เพดาน)
- `python3 tools_bridge/pf_gate_preflight.py --pr-body <server PR body> --pr-stage final` = **PASS**
  (marker หนึ่งบรรทัดพอดี)
- ชุดเต็ม (`pytest tests/`) รันครั้งเดียวหลัง `git merge origin/main` (`387666e`) บนต้นไม้ merge จริง
  (`1005e30`): **11,426 passed · 355 skipped · 21,121 subtests passed · แดง 0 · exit 0** (654.43s /
  10:54)
- `BYTECODE_PURGED: PYTHONDONTWRITEBYTECODE=1 + python3 -B ทุกคำสั่งของรอบ`
- ไม่ใช้ `rm -r`/`rm -rf` ทุกการสะกดตลอดรอบ (คำเตือนครั้งเดียวของ COO `2150`) -- ตรวจแล้ว: ไม่มีการเรียก
  คำสั่งลบไดเรกทอรีใด ๆ เลยในรอบนี้

## nonclaim (บังคับ)

- ไม่อ้างว่ารู้ว่า 14 แถวไหนคือแถวที่จะใช้จริงเมื่อ P-2 wiring เดินหน้า -- แค่แก้เลขที่โมดูลอ้างผิด
- ไม่อ้างว่า field mob สี ใช้งานได้บนจอผู้เล่นวันนี้ -- `CORE-REQUEST-GM-061` เป็นการขอจุดเสียบ ไม่ใช่
  โค้ดที่รัน
- ไม่อ้างว่าฟิลด์ไบต์ `NPCAttr+0x98`/tag `0x32`/mask `+0xBC` bit `0x08` เป็นสิ่งที่สายนี้ตรวจสอบเองจาก
  client image -- เป็นการถอดความจาก `COO-DECISION 20260905_2348` ทั้งหมด (ระบุชัดในจดหมาย
  `CORE-REQUEST-GM-061` เอง)
- ไม่อ้างว่า `_restore_selected_scene` ถูกหดแล้ว -- เช็คแล้วว่า PR ของ chief ยังไม่ขึ้น main จึงไม่แตะ
  ตามที่ `2051` สั่งไว้ชัด
- ไม่อ้างว่ามี PR/รอบไหน merge ไปแล้ว -- ทั้ง `#864` (server) และ PR ของ `pf_bridge` รอบนี้ **เปิดแล้ว
  รอ gate** เท่านั้น อยู่บน main ต่อเมื่อรอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`
- ไม่ได้ทำ P-3 (ปุ่ม GM) หรืองานสำรอง (ปลดแฟล็ก scenario -- `scenarios/gm_*.json` ยังคง 0 ไฟล์,
  `docs/PROMOTION_BACKLOG.md` ยังไม่มีอยู่) รอบนี้เต็มเวลาไปกับหนี้ adversary + CORE-REQUEST

TWO_SESSIONS_SAME_SCENE: รอบนี้ไม่แตะสถานะโลกต่อฉากเลย (แก้แค่คอมเมนต์/ค่าคงที่ pin ในโมดูล refusal
อ่านอย่างเดียว + เทสที่อ่าน `field_mobs.py` โดยไม่เขียน) -- ไม่เกี่ยวข้องกับกฎนี้โดยตรงรอบนี้

## จดหมายที่ออกรอบนี้

1. `20260906_0001_LANE-GM-CORE-REQUEST-GM-061-per-viewer-name-colour-splice-point.md` --
   `ADDRESSEE: LANE-E` (cc COO, LANE-A, LANE-B) ตามที่อธิบายข้างบน
2. สี่ `.CONSUMED.txt` stub (`1347`, `2051`, `2150`, `2348`) พร้อมสำเนาต้นฉบับใน `consumed/`

## รอบหน้าทำอะไร (เรียงแล้ว)

1. เช็คซ้ำว่า PR ของ chief ที่กลืน D3/D4/GM-060 เข้า `runtime.py` ขึ้น main หรือยัง (grep `GM-060`,
   `_restore_selected_scene`, `docs/PROMOTION_BACKLOG.md`) -- ถ้าขึ้นแล้ว: หด
   `gm/warp_send_watch.py::_restore_selected_scene` เหลือเรียก restore ของ chief ตามที่ `2051` สั่ง
   แล้ววาง stub ปิด `1933`/`GM-060`
2. รอคำตอบ chief ต่อ `CORE-REQUEST-GM-061` (และเลข GT ที่ขอไปในใบเดียวกัน) -- ถ้ามาแล้วและมีจุดเสียบจริง
   ให้เริ่มเขียนเทส/โค้ดฝั่ง GM ที่ประกอบ viewer identity (ถ้าจุดเสียบอยู่ในเขต GM) หรือรายงานผล GT ถ้า
   chief เดินโค้ดจริงแล้ว
3. ถ้าทั้งสองข้อบนติด: งานสำรอง P-3 ไล่ปุ่ม GM ทีละปุ่ม (ตาม NOW · `docs/PROMOTION_BACKLOG.md` ยังไม่มี
   scenario ของ GM ให้ปลดแฟล็ก)
4. ตรวจว่า PR ของรอบนี้ (`#864` และ pf_bridge PR นี้) merge หรือยังด้วย `git merge-base --is-ancestor`
   ก่อนเขียนว่า "อยู่บน main"

## SCOREBOARD: NONE | ไม่มีอะไรใหม่บนจอผู้เล่นวันนี้ -- รอบนี้แก้คำเท็จ/คำหลวมในโค้ดของสายตัวเอง (evidence-grade cleanup) และยื่นคำขอจุดเสียบสีชื่อมอนให้ chief ไม่ใช่ฟีเจอร์ที่ผู้เล่นสัมผัสได้ | pirate-force-server#864 (เปิดแล้ว รอ gate, sha 1005e30) + pf_bridge PR (เลขเติมหลัง push, sha ดูท้ายรอบ)

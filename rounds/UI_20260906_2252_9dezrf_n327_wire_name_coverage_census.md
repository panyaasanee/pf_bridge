# LANE-UI round `9dezrf` -- 2026-09-06T22:52+07:00

## ล็อกรอบ
list เปิด `[LANE-UI]` ใน `pf_bridge` ก่อนเริ่มรอบ: ว่าง -- ใบเปิดอื่นทั้งหมดเป็นคนละสาย
(`#1577` LANE-CS, `#1575` LANE-B, `#1571` LANE-DB, `#1493` LANE-B addendum) เปิด claim
`pf_bridge#1581` ทันที list ซ้ำ: ยังเป็นใบเดียว ไม่มีใครแข่ง

## แหล่งความจริงที่อ่านต้นรอบ
1. `NOW.md` (ตรวจล่าสุด COO รอบ `2141`, 21:41+07:00) -- บรรทัด LANE-UI: RE "รายงานกัปตัน" ส่ง A/K
   แล้ว (`2124`) -> wstring `0x48` PR (`1713`) -> งาน 2 `2032` แถบ n/327 (`2047`) · express/community
   ยังห้าม (`1649`)
2. กล่องจดหมาย `ADDRESSEE: UI`/`ADDRESSEE: LANE-UI` ไม่มี `.CONSUMED.txt`: **ว่าง** -- ไล่ทุกใบใน
   `notes_to_chief/*.md` เทียบ `.CONSUMED.txt` คู่ ไม่พบใบค้าง (ล่าสุดที่ consume แล้วคือ `2047` เอง
   ซึ่ง round `k9vrmz` อ่านและวางแผนไว้แล้ว) -- อ่าน `20260906_2032_KA1A-PANYA-DECISION-...` ต้นทาง
   ของ `2047` เพิ่มด้วย (cc: LANE-UI, ไม่ใช่ ADDRESSEE ตรง จึงไม่ต้องมี stub ของตัวเอง) ยืนยันขอบเขต
   ส่งมอบตรงกับที่ทำรอบนี้ทุกข้อ
3. `AGENTS.md` §7 -- อ่านครบ ไม่มีกฎใหม่กระทบงานรอบนี้โดยตรง นอกจากกฎเดิม: (ก) Agent tool จริง ต้อง
   สั่ง `pf-adversary` ทุกรอบที่แก้โค้ด (ข) ห้าม `git add -A` (ค) ชุดเต็มครั้งเดียวหลัง merge
   origin/main เป็น commit สุดท้าย (ง) marker ห้ามอยู่ใน claim PR จนจบรอบ (จ) PR ที่ไม่แตะบูต/ล็อกอิน/
   ตัวตน actor/เฟรมที่ส่งไคลเอนต์ เปิดตรงได้ไม่ต้อง draft -- งานรอบนี้ (census script + doc, อ่านโค้ด
   ที่คอมมิตแล้วเท่านั้น ไม่แตะ dispatch ใด ๆ) เข้าเงื่อนไข (จ)
   🔴 พบด้วย: `pf_bridge` commit `37fd418` (LANE-B, 22:00+07:00) รายงาน `pirate-force-server` main
   แดงจาก assertion ค้างของ LANE-A ใน `test_lane_a_choose_npc_scene1.py` (คู่ `0137`) -- อยู่ใน
   `KNOWN_RED_MAIN` แถวที่สองของ `NOW.md` แล้ว ไม่ใช่ของสายนี้ ไม่แก้ -- **ระหว่างรอบ LANE-A ปิดจริง
   ผ่าน `pirate-force-server#957` (merge เข้า main `be06164`) รอบนี้ `git merge origin/main` รับเข้า
   เป็นครั้งที่สอง แล้วยืนยันด้วยชุดเต็ม: 0 failed**
4. ไฟล์รอบล่าสุดของสาย: `rounds/UI_20260906_2124_k9vrmz_...md` -- "รอบหน้าทำอะไร" ข้อ 3 ชี้ไปที่ PR
   migrate wstring `0x48` (`1713`) ก่อน แล้วจึงงาน 2 ของ `2032` -- **ตรวจด้วย
   `git merge-base --is-ancestor` แล้วพบว่า migration `1713` อยู่บน main แล้วจริง**: `c54231f`
   (round `rqwwp8`) เป็น ancestor ของ `origin/main` -- งานที่เหลือของข้อ 3 คือ งาน 2 ของ `2032`
   เท่านั้น หยิบมาทำรอบนี้ตามลำดับที่ COO-DECISION `2047` วางไว้ (ข้อ 1: "ถ้ารอบ RE binary ติดตัน...
   ทำงานนี้แทนได้")

## งานที่ทำ
`docs/UI_WIRE_COVERAGE.md` -- หน้าสารานุกรม "n/327" (PANYA `2032` งาน 2 / COO-DECISION `2047`)
+ `tools/pf_ui_wire_name_census.py` -- สคริปต์ census รันซ้ำได้ อ่าน 327 แถวจาก
`pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` แบ่งสามชั้น:
  - `SOURCE` = ชื่อพบในบรรทัดที่ไม่ใช่คอมเมนต์ของ `.py` ใต้ `src/pirateforce_foundation/` (ทุกสาย
    ไม่ใช่แค่ UI) หลักฐาน = `path:line` ของจุดแรกที่เจอ
  - `NAME-ONLY` = ไม่เจอใน SOURCE แต่พบใน `docs/PF_VITAL_NAMES.json` หรือ
    `pf_bridge/external/PF_PROTOCOL_REGISTRY.tsv` หรือ `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv`
    หรือ `docs/UI_LANE.md`
  - `UNTOUCHED` = ไม่เจอที่ไหนเลยนอกจากแถวในสารบัญหลัก
  แยกธง `is_client_req` (ชื่อมี token "Req" แบบ PascalCase แยกคำ -- ครอบทั้ง `...VitalReq` และ
  `...ReqVital[_ภูมิภาค]`)
ผลปัจจุบัน (หลังแก้ที่ pf-adversary ชี้ -- ดูหัวข้อถัดไป): **160/327 SOURCE · 158 NAME-ONLY ·
9 UNTOUCHED** (คอมมิตเป็น `reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv` 327 แถว) เทสปักตัวเลขนี้ไว้
(`tests/test_ui_wire_name_census.py`) ให้แดงถ้ามีชื่อย้ายชั้นโดยไม่มีใครอัปเดตไฟล์คู่กัน
🔴 nonclaim: SOURCE **ไม่ใช่** คำว่า "WIRED" ตาม `AGENTS.md` §7 (ต้องมี mutation test + single-writer
guard + observed round trip) -- เป็นแค่การพบชื่อในซอร์สโค้ดแบบกลไก (grep-shaped) หน้าเอกสารเขียน
เตือนไว้ตรง ๆ พร้อม nonclaim อีกสี่ข้อ (รวมช่องโหว่ inline-comment ที่ยังไม่ปิดสนิท -- ดูหัวข้อถัดไป)

## `pf-adversary`
สั่งต้นรอบพร้อมเริ่มงาน (Agent tool มีจริงในเซสชันนี้) ผลคืนก่อนจบรอบ พบสามข้อจริง แก้ครบก่อน push:
1. **`is_client_req` เดิมเช็คแค่ `.endswith("Req")`** พลาดชื่อแบบ `...ReqVital[_ภูมิภาค]` เช่น
   `CTracePathReqVital` ที่ `trace_path.py` ของโปรเจกต์เองเขียนไว้ตรง ๆ ว่าเป็น inbound (client ส่ง) --
   แก้เป็น token-based (แยกคำ PascalCase เช็คว่ามีคำ "Req" เป๊ะ) ซึ่งแยก "Req" ออกจาก "Request" ได้ถูก
   (`Community_RequestBeFriendVital` ไม่ถูกติดธงผิด)
2. **SOURCE นับคอมเมนต์เป็นหลักฐานโค้ด** -- `VitalData` เป็น SOURCE เพราะคอมเมนต์ใน `app.py` ใช้ชื่อ
   นี้เป็นศัพท์ทั่วไปของ memory layout ไม่ใช่การอ้างเฟรมจริง ไม่มีที่อื่นอ้างเลย -- แก้โดยข้ามบรรทัดที่
   เป็นคอมเมนต์เต็มบรรทัด (`line.lstrip().startswith("#")`) ผลคือ `UpdateNPCAppearVital` ย้ายจาก
   SOURCE เป็น NAME-ONLY จริง (เคยนับผ่านคอมเมนต์รวมชื่อหลายตัวบรรทัดเดียวกับ `CreateActorVital`/
   `SelectActorVital` ซึ่งสองตัวหลังมีหลักฐานโค้ดจริงที่อื่น เลยยังเป็น SOURCE) -- ช่องโหว่ที่เหลือ
   (คอมเมนต์ท้ายบรรทัดโค้ด/docstring) เปิดเผยไว้เป็น nonclaim ข้อ 4 ใน `docs/UI_WIRE_COVERAGE.md`
   ไม่ได้ปิดสนิท (ต้อง parse AST ถึงจะปิดได้ เกินขอบเขตรอบนี้)
3. **ประสิทธิภาพ**: อัลกอริทึมเดิมสแกนทุกไฟล์ใหม่ต่อหนึ่งชื่อ (สูงสุด ~65,000 ครั้งอ่านไฟล์) --
   เขียนใหม่เป็นสแกนต้นไม้รอบเดียวเก็บทุกชื่อพร้อมกัน + แคชระดับโปรเซส เทสไฟล์เดียว: 226s -> 0.7s
ตัวเลขเปลี่ยนจาก 161/157/9 (ก่อนแก้ข้อ 2) เป็น 160/158/9 (หลังแก้) -- ปักในเทสและหน้าเอกสารแล้ว

## เทส
- `pytest tests/test_ui_wire_name_census.py -q` -- 10 passed (0.69s)
- ชุดเต็ม `pytest tests/` ครั้งแรก (ก่อน main รับ `#957`): `1 failed (KNOWN_RED_MAIN เดิม),
  12486 passed` -- ครั้งที่สอง หลัง `git merge origin/main` รับ `#957` (LANE-A ปิด KNOWN_RED_MAIN
  แถวนั้นแล้ว) เป็น commit สุดท้ายก่อน push: **`12489 passed, 373 skipped, 0 failed`**
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` -- PASS (รวม
  `--pr-body ... --pr-stage final` ยืนยัน marker เดียวในบอดี้ก่อนเปิด PR จริง)

## งานที่ทำ (pf_bridge)
- claim PR `pf_bridge#1581`
- PR โค้ด `pirate-force-server#961` (ไม่ draft ตั้งแต่เปิด มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด ยืนยัน
  ด้วย GET แล้ว) -- อัปเดตบอดี้อีกครั้งหลัง merge `#957` เพื่อรายงานชุดเต็มที่เขียวจริง

## nonclaims
1. ไม่อ้างว่า 160/327 คือ "WIRED" -- ดูหัวข้อ "งานที่ทำ" ด้านบน
2. ไม่แก้ assertion ค้างของ LANE-A เอง (`#957` เป็นของสาย A) -- แค่รับผลผ่าน `git merge origin/main`
   สองครั้งในรอบนี้
3. ไม่เปิดใบ RE ใหม่รอบนี้ -- งานนี้ไม่ต้องการ RE (อ่านโค้ด/registry ที่คอมมิตแล้วเท่านั้น ไม่มีที่ไหน
   ต้องอ่าน `GameClient.local.bin`)
4. ไม่อ้างว่าตัวเลข 160/327 นับ "ปุ่มที่ผู้เล่นกดได้" -- เป็นแค่การนับชื่อในซอร์ส ตารางฟังก์ชันของ
   `docs/UI_LANE.md` (layout known / needs RE / needs capture / done) ยังเป็นตัวชี้สถานะจริงของ
   UI lane เอง คนละมิติกับหน้านี้
5. ไม่อ้างว่าช่องโหว่ inline-comment ของ SOURCE ปิดสนิทแล้ว -- ปิดแค่คอมเมนต์เต็มบรรทัด เปิดเผยไว้ใน
   `docs/UI_WIRE_COVERAGE.md` nonclaim ข้อ 4 ตรง ๆ

## กล่องจดหมายที่อ่านเพิ่มระหว่างรอบ (consume แล้วทั้งคู่)
- `20260906_2217_LANE-K-NUMBERED-RE-286.md` -- แค่รับทราบเลข `RE-286` (TriggerResult ทิศทาง/caller
  chain) ยังไม่มีบรรทัดใน `CLIENT_RE_QUEUE.md` (K ติด tool write-ceiling) ต้องเปิด `tickets/RE-286.md`
  ตรง ๆ จนกว่า K จะเติมบรรทัดให้
- `20260906_2258_SYNC-NOTICE-pirate-force-server-pr945-closed-never-merged.md` -- PR เก่าของสายนี้
  (round `u3pzcz`, "guard test for express/community_social wiring before migration") ถูก reaper ปิด
  เพราะเกตแดง (ไม่เกี่ยวกับ main-red ของ LANE-A ที่ `#957` เพิ่งแก้ -- ปิดไปตั้งแต่ 20:41+07 ก่อนเหตุนั้น
  เกิด) กิ่ง `claude/inspiring-feynman-u3pzcz` ยังมี commit `5e59849` (ไฟล์เทสใหม่ไฟล์เดียว 340 บรรทัด
  ไม่มีโค้ด production) ที่ยังไม่ได้กู้ -- **ยังไม่กู้รอบนี้เพราะงบเวลาลงกับ `2032` งาน 2 ตามลำดับที่
  `2047` วางไว้** จุดประสงค์ของเทส (กันไม่ให้ต่อสาย express/community ก่อน migration ของมันเอง) ยังใช้
  ได้จริงเพราะสองโมดูลนั้นยังห้ามต่อสายตาม `1649`

## รอบหน้าทำอะไร
1. **กู้ `pirate-force-server#945`** จากกิ่ง `claude/inspiring-feynman-u3pzcz` (commit `5e59849`) --
   cherry-pick หรือเปิด PR ใหม่จากกิ่งเดิมตามคำแนะนำใน SYNC-NOTICE ตรวจให้ผ่านชุดเต็ม + preflight ก่อน
   ยืนยันว่ายังไม่มีใครแตะ `ui_express_wire.py`/`ui_community_social_wire.py` ระหว่างนี้ (ยังห้ามอยู่)
2. ถ้ายังไม่มีเฟรมผู้สมัครใหม่จาก RE `TriggerResult`/`RE-286` (ใบส่ง K รอบ `k9vrmz`) หรือ M2 -- กลับไป
   สาย RE binary ต่อตามลำดับ `1955`
3. ถ้า COO ต้องการต่อยอดหน้า n/327 (เช่น ผูกเข้า `SCOREBOARD_FACTS.tsv` เป็นแถวถาวรจริง ไม่ใช่แค่
   บรรทัด SCOREBOARD ของรอบนี้) -- รอคำสั่ง K/COO
4. งานสำรอง: คิวหลักข้อ 3 ของ `prompts/LANE-UI.md` (ฟังก์ชันถัดไปที่ layout รู้แล้วใน `docs/UI_LANE.md`)

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นปุ่มใหม่วันนี้ แต่โครงการมีตัวเลขวัดความคืบหน้าถาวรตัวแรก
("server รู้จักชื่อเฟรม 160 จาก 327 แบบมีโค้ดอ้างอิงจริง") ที่รันซ้ำได้ทุกรอบและไม่หลอกตัวเอง (ผ่าน
pf-adversary แก้บั๊กจริงสามข้อก่อนขึ้น main) | `pirate-force-server#961` (PF-AUTOMERGE ยืนยันแล้ว,
ชุดเต็ม 12489 passed 0 failed) + `pf_bridge#1581`

-- LANE-UI (round `9dezrf`)

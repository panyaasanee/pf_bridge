# LANE-GM รอบ `07kjfd` — 2026-09-03T19:16→19:5x+07:00

รหัสรอบ: `GM_20260903_1916_07kjfd`
เริ่ม: 2026-09-03T19:16+07:00 · claim: `pf_bridge#1008` (`[LANE-GM] round 07kjfd: claim`)

## รอบนี้ขยับ NOW ข้อไหน
**ขยับ**: หัวข้อ `GM-A /warp <เลขแมพ>` บรรทัดสุดท้าย —
`PANYA-DECISION 1800` (`/warp <n>` ไม่มีพิกัดในฉากเดิม ต้องวาปไป spawn ทันที ไม่ใช่ `STAGED_NEXT_LOGIN`)
ทำครบทั้งข้อในรอบนี้ ตามที่ `COO-DECISION 1845` สั่งว่าต้องขึ้นก่อนทุกอย่างในรอบ 19:11
**ขยับด้วย**: หัวข้อ `GM-B /speed` บรรทัดที่สาม — `/warp <n> <x> <y>` (มีพิกัด) ปิดแล้วจริงในโค้ด
ตาม `COO-DECISION 1744` ข้อ 3
**ยังไม่ขยับ**: `P-2` สีชื่อมอนสเตอร์ (รอเครื่องเจ้าของ) · `P-3` (รอเครื่องเจ้าของ)
· ใบ RE รูปเฟรม `UpdateAttrVital` — ส่งร่างให้ chief แล้ว รอ chief วางหัวใบ (สาย GM แก้คิวเองไม่ได้)

## ล็อกรอบ
- ต้นรอบ list PR สถานะ open ทั้งสองรีโป: `[LANE-GM]` = **ไม่มีเลย** (open ตอนนั้น:
  `pf_bridge#1006` LANE-DB · `#988` LANE-A · `server#671` LANE-B · `#670` LANE-E · `#669` LANE-A
  — สายอื่นทั้งหมด ไม่ใช่ล็อกของผม ไม่แตะ)
- ตัดกิ่งจาก `pf_bridge/main` commit ไฟล์ร่าง `_claim.md` push เปิด `#1008` **ไม่มี marker** ตามกติกาใหม่
- list ซ้ำหลังเปิด: ไม่มี `[LANE-GM]` ใบอื่นที่เก่ากว่า ⇒ ถือล็อกทั้งรอบ
- ไม่มี takeover · ไม่มี released-on-behalf

## ชะตา PR รอบก่อน (ADDENDUM ข้อ A)
- `pf_bridge#994` (รอบ `lx4yib`) **merged=true**
- `server#667` (รอบ `lx4yib`) **merged=false — งานหายจาก main** ใบแจ้ง `20260903_1900_SYNC-NOTICE-*`
  กิ่ง `claude/ecstatic-johnson-lx4yib` ยังอยู่ครบ 2,394 บรรทัด
  (`gm/lane_gate_name_audit.py` 1,007 · `tests/test_gm_lane_gate_name_audit.py` 1,214
  · `docs/GM_LANE.md` 156 · `lane_hooks/lane_gm_chat_command.py` 17)
- **อ่านล็อกเกตแล้ว หาเหตุเดียวเจอแล้ว** (run `33750126020` sha `a9030e86`):
  `pytest_subset exit=1` · แดงตัวเดียว =
  `tests/test_gm_lane_gate_name_audit.py::GateScopeTests::test_a_misspelled_prefix_is_inside_the_asserted_subset`
  ที่ `literal='Lane_GM_chat_command'` → ได้ finding
  `lane_module_declares_production_allowed_but_the_registry_refuses_it`
  แทน `FINDING_NAMES_NO_MODULE`
  ⇒ **สาเหตุ: ระบบไฟล์ Windows ไม่แยกตัวพิมพ์** `Lane_GM_chat_command` resolve เจอโมดูลจริงบน Windows
  แต่ไม่เจอบน Linux ⇒ เทสนี้เขียวบนคลาวด์และแดงบนเกตทุกครั้ง ไม่ใช่ flake
  แก้: `gate_findings_in_lane_gm_scope` ต้องเทียบชื่อโมดูลแบบ case-sensitive เอง ห้ามพึ่ง `Path.exists`/importlib
- **ยังไม่ cherry-pick ในรอบนี้ โดยตั้งใจ** — `NOW.md` + `COO 1845` สั่งให้คำสั่งเจ้าของ `1800` ขึ้นก่อน
  ทุกอย่าง และการเอา 2,394 บรรทัดที่ไม่เกี่ยวเข้ามาใน PR ใบเดียวกัน คือการเอา PR ของเจ้าของ
  ไปเสี่ยงกับเกตของงานเก่า ⇒ **งานแรกของรอบถัดไป** (ดู backlog)

## กล่องจดหมาย (ADDENDUM ข้อ B)
บริโภคครบ 4 ใบที่จ่าหน้า `LANE-GM` และยังไม่มี stub · วาง `.CONSUMED.txt` + สำเนาเข้า `consumed/` แล้ว:
`1744` (COO /speed+warp) · `1800` (PANYA warp) · `1845` (COO ลำดับ) · `1900` (SYNC-NOTICE #667)
ค้างไว้หนึ่ง: `20260902_1035_LANE-GM-TO-CHIEF-re191-*` เป็นใบ**ขาออก**ของสายเราเอง ไม่ใช่ผลที่ต้องบริโภค

## ทำอะไรบ้าง (เขต `gm/` ล้วน ไม่แตะ runtime.py/app.py/v141 · ไม่แตะเขตสาย A/B · ไม่แตะ canonical DB)

### งานที่ 1 — `PANYA-DECISION 1800`: `/warp <n>` ในฉากเดิม = วาปไป spawn ของฉากนั้น
`gm/chat_command_action.py::_warp_action` — สาขา no-coordinates ตัดเงื่อนไข
`target_scene_id != position.scene_id` ออก (ขีดฆ่าคอมเมนต์เดิมไว้ ไม่ลบ)
นอกนั้นไม่เปลี่ยนเลย: handler เดิม (`_warp_teleport_action_no_coords`) · composer เดิม
(`make_warp_teleport_frame_no_coords_with_target`) · label เดิม
(`LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL`) · เฟรม TeleportVital **73 ไบต์**
ไปที่ spawn ที่ `world_scene_travel` pin ไว้ของฉากนั้น
- **โทเคนคอนโซลใหม่** `GM_CHAT_SAME_SCENE_TELEPORT_SENT` — โทเคนแรกของโมดูลนี้ที่พิมพ์ให้คำสั่งที่ **ส่ง** จริง
  เหตุผลที่ต้องมี: label บอกว่า CROSS_SCENE และตอนนี้ label เดียวกันออกให้วาปที่ไม่ข้ามฉากด้วย
  ⇒ คอนโซลที่แยกสองอย่างนี้ไม่ออกจะทำให้คำสัญญาของ label กลายเป็นเท็จ
  ผูกกับคำตอบ `sent` ของ `_make_action` ไม่ใช่กับ verdict ⇒ เฟรมที่ audit ทำตกไป **ไม่** พิมพ์บรรทัดนี้
- `GM_CHAT_STAGED_NEXT_LOGIN` **ไม่ออกอีก** สำหรับรูปนี้ · เทสชื่อ
  `test_the_staged_token_is_not_printed_for_a_same_scene_marker_warp` ตั้งชื่อตามมิวแทนต์ที่มันฆ่า
- **ยังสเตจเหมือนเดิม**: ปลายทางไร้ marker (17/126/278/997 · `n_MARKER == 0` · GT-182 nonclaim 4)
  ฉากเดิมหรือข้ามฉากก็ตาม — ไม่แตะ `warp_no_coords_live_target` ⇒ คำตอบ GT-141 ของฉาก 278 เท่าเดิม
- เทสที่พิสูจน์: ประกอบทั้งสองรูป (ในฉาก 2 ยิงไป 2 · จากฉาก 5 ยิงไป 2) ผ่าน route จริง แล้วยืนยันว่า
  **ไบต์เท่ากันทุกไบต์** ⇒ คำว่า "เฟรมเดียวกับข้ามฉาก" วัดเอา ไม่ใช่เขียนในคอมเมนต์
  ตัวเลข x/y/z มาจาก `world_scene_travel` (fixture) ไม่ได้พิมพ์ลงเทส (COO `0846`)

### งานที่ 2 — `COO-DECISION 1744` ข้อ 3: `/warp <n> <x> <y>` (ForcePos) ปิด
แฟล็กใหม่ `warp_executor.WARP_SAME_SCENE_FORCE_POS_AUTHORIZED = False`
ปฏิเสธ **เหนือ** ตัวอ่านเวอร์ชันและ **เหนือ** `_park_warp_target` ⇒ ไม่มีเป้าค้างให้โทเคนยืนยันของ chief
เอาไปเทียบกับก้าวเดินจริง · เหตุการณ์ `..._warp_withheld_same_scene_force_pos_closed_r306`
· outcome `withheld_same_scene_force_pos_frame_shape`
· บรรทัดคอนโซล `GM_CHAT_NO_BYTES_SENT ... blocked_on='R306 closed the client with ErrorData=28317 ...'`
**ทำไมเป็นแฟล็กที่สาม ไม่ใช่พลิกสองตัวที่มีอยู่**
- `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` = **ไบต์** ที่ `RE-129` ตอบแล้วและ COO เปิดเป็น 0
  ไบต์ที่พิสูจน์แล้วไม่กลายเป็นไม่พิสูจน์เพราะเฟรมรอบมันฆ่าไคลเอนต์ · พลิกกลับ = ยัดเรื่องนี้ใต้ใบที่ปิดไปแล้ว
- `WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED` คุมครึ่ง TeleportVital ที่ R306 วัดว่า **ผ่านห้าครั้งในรอบเดียว**
  ⇒ ยัดรวมกัน = ปิดรูป `/warp` เดียวที่เจ้าของใช้ได้อยู่ตอนนี้
- เทสยืนยันว่าแฟล็กสองตัวนี้ **ค่าตรงข้ามกัน** ⇒ รอบไหนปิดทั้งคู่หรือเปิดทั้งคู่จะแดง ไม่ใช่เงียบ ๆ หายไป

### หนี้ที่ต้องบอกให้ชัด — เทสหกไฟล์ที่ยืมเส้นทาง ForcePos เป็นพาหนะ
หกไฟล์ใช้ `/warp 2 100 200` เป็น "คำสั่งที่ประกอบเฟรมได้" เฉย ๆ ไม่ได้สนใจนโยบาย
`open_the_version_gate`/`open_the_warp_gate` จึงเปิด **สองประตู** และ `close_the_*` **เปิดประตูนโยบาย
ค้างไว้ขณะปิดประตูเวอร์ชัน** — เพราะประตูนโยบายถูกอ่านก่อน เทสที่แยกประตูเวอร์ชันแล้วปล่อยประตู
นโยบายปิดไว้จะไปเช็คคำปฏิเสธผิดตัวและเขียวทั้งที่สาขาของตัวเองไม่เคยถูกเดิน
คำตอบของสภาพจริง (ไม่ patch อะไรเลย) อยู่ที่เดียว: `SameSceneForcePosClosedTests`

## หลักฐาน / เทส
- ระหว่างทาง: `pytest tests/ -k gm_` (ไฟล์ที่รอบนี้แตะ) — **1,957 passed, 1,127 subtests** เขียว(local)
- ชุดเต็ม `pytest tests/`: รันครั้งเดียวบน commit สุดท้าย หลังแก้ตาม pf-adversary — ผลอยู่ท้ายไฟล์นี้
- pf-adversary: รันก่อน commit (ผลและสิ่งที่แก้อยู่ท้ายไฟล์นี้)

## 🔴 nonclaim (G-OBS) — ใช้ GM ข้ามขั้นอะไรไปบ้าง
- การประกอบและส่งเฟรมนี้ = **หลักฐานว่าไบต์รูปถูกต้องออกจากเซิร์ฟเวอร์** เท่านั้น
  **ไม่ใช่** หลักฐานว่าไคลเอนต์ขยับ · ว่าจุด spawn เดินได้ · ว่าฉากเรนเดอร์ใหม่ · ว่าจอเจ้าของหายบั๊ก
- `RE-162` (ไม่มี census ตามหลัง TeleportVital กลางเซสชัน) รูปฉากเดิม **สืบทอดช่องว่างนี้มาเต็ม ๆ**
  และรอบนี้ไม่ปิดมัน · census ซ้ำเป็นของ LANE-A/LANE-B ตามคำสั่งเจ้าของเอง (`1800` ข้อ 3)
- คำสั่ง GM คือเครื่องมือไปถึงสภาพที่จะเทส **ไม่ประกาศไมล์สโตนใดจากผลที่ได้ด้วย GM**
- ต้องมีใบเทส attended (chief เปิดตาม `COO 1845` ข้อ 4) ก่อนใครจะพูดว่า `/warp <n>` ในฉากเดิม "ใช้ได้"

## backlog — อะไรบล็อกอยู่ที่ใคร
1. **งานแรกของรอบถัดไป: กู้ `server#667`** — cherry-pick กิ่ง `claude/ecstatic-johnson-lx4yib`
   แล้วแก้เหตุเดียวที่รู้แล้ว (case-insensitivity ของ Windows ในเทส `Lane_GM_chat_command`) ไม่ต้องทำใหม่
2. **ใบ RE รูปเฟรม `UpdateAttrVital 0x309A`** — ร่างส่ง chief แล้ว (`1933`)
   **บล็อกที่: chief** (วางหัวใบใน `CLIENT_RE_QUEUE.md` — สาย GM แก้คิวเองไม่ได้) แล้วต่อที่ **สาย RE**
   (ต้องดิสแอสเซมบลีอิมเมจ ทำบนคลาวด์ไม่ได้)
3. **ล็อก `/speed` ทุกตัว** — **บล็อกที่: สาย RE** ผ่านใบข้อ 2 · `2147` ยังยืน ห้ามใครปลด
4. **P-2 สีชื่อมอนสเตอร์ / P-3 ปุ่ม GM** — **บล็อกที่: เครื่องเจ้าของ** (COO `1046` บอกเองว่าไม่นับว่าสายไหนค้าง)
5. **ใบเทสจอของ same-scene warp** — **บล็อกที่: chief** เมื่อ PR ของรอบนี้ขึ้น main (`1845` ข้อ 4)

## จบรอบ

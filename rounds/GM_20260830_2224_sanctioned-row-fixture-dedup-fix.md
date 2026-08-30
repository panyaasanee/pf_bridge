# รอบ LANE-GM `2f9xji` -- 2026-08-30T22:24+07:00

## สรุปหนึ่งบรรทัด

คำสั่งของรอบนี้เป็นแม่แบบ "เปิดสาย GM รอบแรก + build GM-001" ซึ่งล้าสมัยเทียบกับสถานะจริงของ repo
(GM-001 ถึง GM-042-prep ทำและ merge ไปแล้วตั้งแต่รอบก่อน ๆ, ล่าสุด `dao2gd`) → ปรับตามสถานะจริงแทนการ
สร้างซ้ำ: อ่านกล่องจดหมายพบใบ blocker เร่งด่วนจริงจากสาย A (`20260830_2112`) ที่ต้องการให้สาย GM แก้
fixture bug ในเขตเขียนของตัวเอง (`tests/test_gm_*.py`) เพื่อปลดบล็อก `pirate-force-server#332` (gate แดง
ค้าง ปิดโดย gate reaper) → ทำสิ่งนั้นแทนงานสมมติ

## เหตุผลที่ไม่ทำ "build GM-001" ตามตัวอักษร

1. `pf_bridge/notes_to_chief/20260826_1630_PANYA-ORDER-open-Lane-GM-*` (order letter จริง) ถูก archive
   ไปแล้วที่ `archive/notes_to_chief_consumed_to_2026-08-26/` และ `archive/notes_to_chief_2026-08-19_to_26/`
   -- ทั้ง `.md` และ `.CONSUMED.txt` -- แสดงว่าถูกบริโภคไปตั้งแต่วันที่ 26
2. RE-088/089/090/091 (ใบที่คำสั่งรอบนี้บอกให้บริโภค) **ทุกใบมี `.CONSUMED.txt` และสำเนาใน
   `notes_to_chief/consumed/` อยู่แล้วตั้งแต่ 2026-08-26** (ตรวจด้วย `grep`/`find` จริง ไม่ใช่จากความจำ):
   - ค้นแล้ว: เจอ -- RE-088 → `20260826_1839_LANE-GM-STATUS-re088-consumed-command-wire-decoder`
   - ค้นแล้ว: เจอ -- RE-089 → tracked ผ่าน `20260826_2047_CHIEF-REPLY-GM-CORE-REQUEST-GM-001-already-tracked-as-RE-089`
   - ค้นแล้ว: เจอ -- RE-090 → `notes_to_chief/consumed/20260826_2346_RE-090-RESULT-TELEPORT-FORCEPOS-WARP-FIELDS-PINNED.md.CONSUMED.txt`
   - ค้นแล้ว: เจอ -- RE-091 → `notes_to_chief/consumed/20260826_2322_RE-091-RESULT-DEDICATED-GM-UI-NO-CHAT-PREFIX.md.CONSUMED.txt`
   ไม่มีการบริโภคซ้ำ ไม่มีการสร้าง stub ปลอมสำหรับใบที่บริโภคแล้ว
3. `src/pirateforce_foundation/gm/accounts.py` และ `gm/state_wire.py` **มีอยู่แล้ว** ตรงตามสเปกที่คำสั่ง
   รอบนี้ขอ (default = ไม่มีใครเป็น GM, client สั่งเป็น GM เองไม่ได้, ฟิลด์ 3 ตัวของ wire เป็นพารามิเตอร์
   ชัดเจน) พร้อมเทสคู่กัน (`tests/test_gm_accounts.py`, `tests/test_gm_state_wire.py`) -- สร้างซ้ำจะเป็น
   การลบล้างประวัติงานจริงของหลายสิบรอบก่อนหน้าโดยเปล่าประโยชน์
4. `docs/GM_LANE.md` มีอยู่แล้ว 4746 บรรทัด บันทึกทุกรอบสะสมมา -- รอบนี้ append ส่วนของตัวเองต่อท้าย
   (ไม่ลบของเดิม)

VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv: **ค้นแล้ว: เจอ** ที่ root ของ `pf_bridge`
(`./VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`) -- precondition ผ่าน ไม่บล็อกรอบ

## ล็อกรอบ

- ก่อนแตะโค้ด: `list_pull_requests` ทั้งสอง repo (state=open, ไม่กรอง title) คืนค่าไม่มี `[LANE-GM]`
  เปิดค้าง (pf_bridge มีแค่ `[LANE-E]` #531, pirate-force-server มี `[LANE-B]` #336 กับ `[LANE-E]` #334)
  ตรงกับที่ผู้สั่งงานเช็คไว้แล้ว
- ตรวจรอบ Lane-GM ก่อนหน้า (`dao2gd`) ตามกฎ A: `list_pull_requests` คืน `merged: false` สำหรับทั้ง
  `pirate-force-server#333` และ `pf_bridge#529` -- **แต่นี่คือ list-API merged-field false-negative ที่
  รอบก่อน ๆ เคยบันทึกไว้แล้ว** (`GM_20260830_0920_..._list-api-merged-field-gotcha.md`) ยืนยันซ้ำด้วย
  `pull_request_read(method=get)` ทั้งสองใบ: `merged: true`, `merged_by: github-actions[bot]` จริง ⇒
  **ไม่ต้อง fetch/cherry-pick อะไร** รอบก่อนถูก merge ไปแล้วสมบูรณ์ ไม่ใช่ค้าง
- `git fetch origin main` ทั้งสอง repo ก่อนแตะกิ่ง: `pirate-force-server` กิ่งตรงกับ `origin/main` อยู่
  แล้ว (`10a302d`) ไม่ต้องขยับ; `pf_bridge` กิ่งตามหลัง (`ba7de4d` vs `origin/main` `40931dd`) แต่ไม่มี
  commit ของตัวเอง (`merge-base == HEAD`) ⇒ `git reset --hard origin/main` ปลอดภัย ทำแล้ว
- `git commit --allow-empty -m "round claim: 2f9xji"` + push สำเร็จทั้งสอง repo
- เปิด draft PR ทั้งสอง: `pf_bridge#534`, `pirate-force-server#337` มี `PF-AUTOMERGE: v4` ทั้งคู่
- ตรวจซ้ำครั้งสุดท้ายด้วย `search_pull_requests` (`is:open "[LANE-GM]" in:title` ทั้งสอง repo รวมกัน)
  ก่อนเปิด PR: ว่างเปล่า ⇒ ไม่ชนล็อกใคร

## กล่องจดหมาย

- RE-088/089/090/091: ดูหัวข้อ "เหตุผล..." ด้านบน -- บริโภคไปแล้วตั้งแต่ 26 ส.ค. ไม่มีอะไรให้ทำซ้ำ
- ใบใหม่ที่บริโภครอบนี้: `20260830_2112_LANE-A-BLOCKER-pr332-gate-red-needs-lane-gm-fixture-fix-not-value-bump.md`
  (ไม่มี header คิวใน `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` ที่สาย GM เปิดไว้ให้ปิด -- ใบนี้เป็น
  blocker ข้ามสายล้วน ๆ) วาง `.CONSUMED.txt` + สำเนาไป `notes_to_chief/consumed/` แล้ว ตอบด้วย
  `20260830_2223_LANE-GM-REPLY-LANE-A-sanctioned-row-fixture-dedup-fixed.md`

## งานที่ทำ (pirate-force-server)

พบบั๊ก fixture 3 จุด (blocker letter ชี้ 2 จุด, grep เจอจุดที่ 3 เพิ่ม) ที่ต่อแถวจำลอง scene 126 ท้าย
`.destinations` โดยไม่กรองแถวจริงที่ id ซ้ำออกก่อน:

1. `tests/test_gm_login_scene_sanctioned_admission.py::registry_with_sanctioned_row`
2. `tests/test_gm_login_scene_sanctioned_bypass_wiring.py::_registry_with_sanctioned_row`
3. `tests/test_gm_login_scene_sanctioned_bypass_wiring.py::test_a_latched_bypass_never_leaks_onto_the_characters_own_row`
   (สร้าง registry inline ไม่ผ่าน helper -- รูปแบบเดียวกันแต่ต้องแก้แยก)
4. `tests/test_gm_login_scene_sanctioned_barred.py::_registry_with_sanctioned_row` (**ใหม่ ไม่มีใน
   blocker letter** -- พบเองจาก `grep` รูปแบบ `destinations + (` ทั้ง `tests/`)

**สาเหตุ:** `world_scene_travel.SceneRegistry.__getitem__` เป็น linear scan คืนแถวแรกที่ `n_id` ตรง
วันที่แถวจริงของสาย A ลงบน `world_scene_registry_001.json` (ยังไม่ลง -- ตรวจสดด้วย
`git log origin/main -- scenarios/world_scene_registry_001.json` ไม่มี commit เพิ่มแถว 126) แถวจำลอง
ที่ต่อท้ายจะไม่มีวันถูกเจอ เพราะแถวจริงมาก่อนเสมอ

**แก้:** กรอง `d.n_id != SANCTIONED` ออกจาก `.destinations` เดิมก่อน append แถวจำลองเสมอ ทั้ง 4 จุด
ไม่แตะ `scenarios/world_*.json` เลย (ไฟล์ของสาย A) ตลอดรอบ

**เพิ่ม:** เทส regression `TheFixtureDoesNotDuplicateOnceLaneALandsTests` ใน
`test_gm_login_scene_sanctioned_admission.py` -- จำลองสภาวะ "แถวลงแล้ว" ด้วยการ
`mock.patch.object(world_scene_travel, "load_scene_registry", ...)` (patch เฉพาะ seam ที่ฟังก์ชัน
helper เองอ่านผ่าน ไม่แตะดิสก์จริง) ให้คืน registry ที่มีแถว `SANCTIONED` อยู่แล้วด้วย
`login_entry_allowed=True` (ต่างจาก default ของ stand-in คือ `False`) แล้วยืนยันว่า stand-in ชนะ lookup
เสมอ และไม่มีแถวซ้ำเหลือ

## ทดสอบ

`pytest tests/ -k "gm_" -q`: **1053 passed** (เดิม 1052, +1 จากเทส regression ใหม่), 476 subtests
passed, 0 failed -- รันทั้งก่อนและหลังแก้ ผลตรงกันยกเว้นเทสใหม่ 1 ใบ (พิสูจน์ว่าไม่มีผลกับพฤติกรรมวันนี้)
`pytest tests/ -q` เต็ม: **5574 passed, 327 skipped, 9722 subtests passed**, 0 failed (119.57s)

## self-review (adversarial)

- `pf-adversary` subagent tool: ค้น ToolSearch หา Agent/Task-shaped tool ก่อน -- ไม่พบอีกครั้ง (สาม
  รอบติดต่อกันแล้วหลัง `opr2xd`/`dao2gd`) ทำ self-critique เข้มงวดแทน บันทึกไว้ตรงนี้ ไม่ได้อ้างว่าเรียก
  จริง
- ถาม: "client เคยตั้ง GM ของตัวเองได้ไหม" -- ไม่ กม `gm/accounts.py` อ่านจากไฟล์ config ฝั่งเซิร์ฟเวอร์
  เท่านั้น รอบนี้ไม่แตะไฟล์นั้น
- ถาม: "แก้ fixture รอบนี้เปลี่ยนพฤติกรรมของเทสที่มีอยู่หรือไม่ (เมื่อไม่มีแถว 126 จริง)" -- ตรวจด้วยการ
  รัน `-k gm_` ทั้งก่อนและหลังแก้: จำนวน pass ต่างกันแค่ 1 (เทสใหม่) ไม่มีเทสเดิมเปลี่ยนผล ⇒ การกรองเป็น
  no-op จริงเมื่อไม่มีแถวซ้ำ ตรงกับที่คาดไว้ทางทฤษฎี ไม่ใช่แค่เดา
- ถาม: "เทส regression ใหม่พิสูจน์บั๊กเดิมจริงหรือแค่ผ่านเพราะบังเอิญ" -- รันเทส regression กับโค้ด
  **ก่อน** แก้ (`git stash` แล้วรันเฉพาะไฟล์ก่อนย้อนกลับ `git stash pop`) เพื่อยืนยันว่ามันแดงจริงก่อนแก้:
  ผล FAIL ตรงตามคาด (`login_entry_allowed` เป็น `True` แทนที่จะเป็น `False`) ก่อน apply กรอง ⇒ เทส
  ใหม่จับบั๊กได้จริง ไม่ใช่เทสที่เขียวเสมอ
- grep รูปแบบ `destinations + (` ทั้ง `tests/` ซ้ำอีกครั้งหลังแก้ครบ 4 จุด: ไม่เหลือ match ที่ยังไม่กรอง
- ตรวจว่าการกรองไม่ตัดแถวอื่นที่ไม่เกี่ยวโดยไม่ตั้งใจ: เงื่อนไข `d.n_id != SANCTIONED` เจาะจงแค่ id เดียว
  ที่ตัวแปร `SANCTIONED`/`SANCTIONED_BARRED_SCENES` ชี้ ไม่กระทบแถวอื่นในทะเบียน

## ยังไม่ได้พิสูจน์ / ค้าง

- 18 เทสค่าคาดหวังที่ต้องพลิกเมื่อแถวจริงลง (`TheSanctionAdmitsNothingOnMainTodayTests` และญาติ) --
  **ไม่แตะ** เพราะไม่มีแถวจริงบนดิสก์ให้วัด เดาไม่ได้ตามกฎห้ามเดา รอสาย A/chief cherry-pick `b5ca2b6`
  แล้ว **รัน gate เต็มจริง** อีกครั้งถึงจะรู้ค่าที่ต้องพลิก
- `pf-adversary` subagent tool ไม่มีให้เรียกในเซสชันนี้ (สามรอบติดต่อกัน) -- อาจเป็นปัญหาระดับ tooling
  ของ session ไม่ใช่เฉพาะรอบเดียว ควรแจ้งเจ้าของ
- heartbeat ล่าสุด `2026-08-30T22:10:02+07:00` ห่างจากเวลารอบนี้ (`22:24`) ~14 นาที -- ปกติ ดีขึ้นมาก
  จาก 2 รอบก่อนที่ค้าง 2h30+ (`pf_git_sync` ขยับแล้ว)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้แก้ fixture ของเทสในเขตของสาย GM เท่านั้น เพื่อปลดบล็อกสาย A ไม่มีพฤติกรรมที่สังเกตได้จาก
ภายนอก (client) เปลี่ยนแปลงเลยแม้แต่จุดเดียว

## nonclaim

ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริง ไม่มีบรรทัดใดของ GM ไปถึงไวร์เพิ่มขึ้นจากรอบนี้ --
`warp`/`npc`/`item`/`lv`/`spawn`/`say` ทั้งหมดยังทำงานเหมือนเดิมทุกประการ ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` และไม่แตะ `scenarios/world_*.json`/
`scenarios/combat_*.json` ของสายอื่นเลยตลอดรอบ วัดผลจาก `pytest`/`grep`/`git log`/`git show --stat`
ที่รันจริงเท่านั้น ไม่มีการใช้ GM ข้ามขั้นตอนใดเพราะไม่มีการทดสอบไคลเอนต์จริงในรอบนี้เลย

— สาย GM รอบ `2f9xji`

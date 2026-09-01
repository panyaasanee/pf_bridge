# รอบ LANE-GM `2f9xji` -- 2026-08-30T22:24+07:00

## สรุปหนึ่งบรรทัด

คำสั่งของรอบนี้เป็นแม่แบบ "เปิดสาย GM รอบแรก + build GM-001" ซึ่งล้าสมัยเทียบกับสถานะจริงของ repo
(GM-001 ถึง GM-042-prep ทำและ merge ไปแล้วตั้งแต่รอบก่อน ๆ, ล่าสุด `dao2gd`) → ปรับตามสถานะจริงแทนการ
สร้างซ้ำ: อ่านกล่องจดหมายพบใบ blocker เร่งด่วนจริงจากสาย A (`20260830_2112`) ที่ต้องการให้สาย GM แก้
fixture bug ในเขตเขียนของตัวเอง (`tests/test_gm_*.py`) เพื่อปลดบล็อก `pirate-force-server#332` (gate แดง
ค้าง ปิดโดย gate reaper) → ทำสิ่งนั้นแทนงานสมมติ **แต่ที่ push ท้ายรอบพบว่า chief (รอบ `390q29`/R249)
ทำงานชิ้นเดียวกันเสร็จสมบูรณ์กว่าไปแล้วคู่ขนานกัน ดูหัวข้อ "ส่วนเพิ่มท้ายรอบ" ด้านล่าง**

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
- ใบใหม่ที่ตั้งใจบริโภครอบนี้: `20260830_2112_LANE-A-BLOCKER-pr332-gate-red-needs-lane-gm-fixture-fix-not-value-bump.md`
  -- **ระหว่างรอบ chief (390q29/R249) บริโภคใบเดียวกันนี้ไปพร้อมกันคู่ขนานและ merge เข้า main ก่อน**
  (ดูหัวข้อ "ส่วนเพิ่มท้ายรอบ") จึงไม่ทับ stub ของ chief -- stub ของ chief ยืนตามเดิมบน `main`

## งานที่ทำ (pirate-force-server) -- ที่ push ตอนแรก ก่อนพบการชนกัน

พบบั๊ก fixture 3 จุด (blocker letter ชี้ 2 จุด, grep เจอจุดที่ 3 เพิ่ม) ที่ต่อแถวจำลอง scene 126 ท้าย
`.destinations` โดยไม่กรองแถวจริงที่ id ซ้ำออกก่อน:

1. `tests/test_gm_login_scene_sanctioned_admission.py::registry_with_sanctioned_row`
2. `tests/test_gm_login_scene_sanctioned_bypass_wiring.py::_registry_with_sanctioned_row`
3. `tests/test_gm_login_scene_sanctioned_bypass_wiring.py::test_a_latched_bypass_never_leaks_onto_the_characters_own_row`
   (สร้าง registry inline ไม่ผ่าน helper -- รูปแบบเดียวกันแต่ต้องแก้แยก)
4. `tests/test_gm_login_scene_sanctioned_barred.py::_registry_with_sanctioned_row` (**ใหม่ ไม่มีใน
   blocker letter** -- พบเองจาก `grep` รูปแบบ `destinations + (` ทั้ง `tests/`)

**สาเหตุ:** `world_scene_travel.SceneRegistry.__getitem__` เป็น linear scan คืนแถวแรกที่ `n_id` ตรง
วันที่แถวจริงของสาย A ลงบน `world_scene_registry_001.json` (ตอนเริ่มรอบนี้ยังไม่ลง -- ตรวจสดด้วย
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

## ทดสอบ (ก่อนพบการชนกัน)

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
  **ก่อน** แก้ (แก้ชั่วคราวให้ filter เป็น no-op, รัน, ยืนยัน `AssertionError` แดงจริงตามคาด, คืนของเดิม)
  ก่อนคอมมิต ⇒ เทสใหม่จับบั๊กได้จริง ไม่ใช่เทสที่เขียวเสมอ
- grep รูปแบบ `destinations + (` ทั้ง `tests/` ซ้ำอีกครั้งหลังแก้ครบ 4 จุด: ไม่เหลือ match ที่ยังไม่กรอง
- ตรวจว่าการกรองไม่ตัดแถวอื่นที่ไม่เกี่ยวโดยไม่ตั้งใจ: เงื่อนไข `d.n_id != SANCTIONED` เจาะจงแค่ id เดียว
  ที่ตัวแปร `SANCTIONED`/`SANCTIONED_BARRED_SCENES` ชี้ ไม่กระทบแถวอื่นในทะเบียน

## ส่วนเพิ่มท้ายรอบ -- พบการชนกันกับ chief รอบ `390q29` (R249) ตอน push (2026-08-30T22:27+07:00)

หลัง push แรกและเปิด PR แล้ว, ตรวจ PR ทั้งสองกลับ (ตามขั้นตอนปิดรอบข้อ 3) พบว่า
`pf_bridge#534` **ถูกปิดโดย gate reaper ทันที** (`mergeable=false`) -- คอมเมนต์ของบอทอธิบายว่า
`main` ขยับใต้กิ่งของรอบนี้และไฟล์ `notes_to_chief/20260830_2112_...md.CONSUMED.txt` ถูกสร้างโดย
**ทั้งสองรอบพร้อมกัน** ด้วยเนื้อหาต่างกัน (path เดียวกัน content ต่างกัน = conflict จริง ไม่ใช่ false
alarm) `git fetch origin main` แล้วอ่าน `pf_bridge/rounds/R249_390q29_*.md` และ diff ของ
`pirate-force-server#334` (PR ของรอบ `390q29`, `[LANE-E]`, ยังเปิดอยู่ ไม่ merge) พบว่า:

- chief **หยิบใบ blocker เดียวกันนี้ไปทำคู่ขนานในช่วงเวลาเดียวกัน** ในฐานะ gate-red-repair (สิทธิ์
  chief ตามที่ใบ blocker เองอ้างถึง `rounds/R213_..._fullgate-red-repair-*.md` ว่า "สาย GM **หรือ
  chief**")
- งานของ chief **สมบูรณ์กว่างานของรอบนี้จริง**: cherry-pick `b5ca2b6` มาลงจริง (แถวทะเบียนฉาก 126
  ลงบน branch ของเขาแล้ว), แก้ fixture ครบทั้ง 4 จุดเดียวกันที่รอบนี้พบ (ยืนยันจาก `pull_request_read
  get_files` ของ `pirate-force-server#334`: ไฟล์ที่เปลี่ยนรวม `test_gm_login_scene_sanctioned_
  admission.py`, `..._bypass_wiring.py`, `..._barred.py` ครบ), **และอัปเดตค่าคาดหวัง 18 เทสที่เหลือ
  ให้ตรงกับแถวจริงที่ลงแล้ว** (`sanctioned_barred_blocker(126)` → `BLOCKER_LOGIN_PATH_BARS_IT`,
  `single_use_entry_is_admissible(126)` → `True`) ซึ่งเป็นสิ่งที่รอบนี้ **ทำไม่ได้** เพราะไม่มีแถวจริง
  บนดิสก์ให้วัด (ระบุไว้ชัดในรอบนี้แล้วว่าเป็นข้อจำกัด ไม่ใช่ทำไม่ครบ) -- สวีตเต็มของ chief:
  **5578 passed, 0 failed** (cloud sanity)
- `pirate-force-server#337` (PR ของรอบนี้) **ยังเปิดอยู่** (ไม่ปิดเอง ตามกฎ) แต่จะซ้ำซ้อนกับ
  `pirate-force-server#334` แน่นอนเมื่อ #334 merge -- คาดว่า gate reaper จะจัดการเองตามกลไกเดียวกับที่
  จัดการ `#534` (ไม่ใช่หน้าที่รอบนี้จะปิดเอง)

**การกู้คืนที่ทำ:** `git reset --hard origin/main` บนกิ่ง `claude/magical-cannon-2f9xji` (commit เดิม
ยังอยู่ใน reflog/remote ก่อนหน้า ไม่ได้หายจริง) เขียนไฟล์รอบนี้ใหม่ (round notes ฉบับนี้ + จดหมายตอบ
ฉบับแก้ `20260830_2230_LANE-GM-STATUS-collision-with-chief-r249.md`) **ไม่ทับ stub ของ chief ที่ merge
ไปแล้ว** (เนื้อหาต่างกันจริง ไม่ใช่แค่รูปแบบ -- ตามกฎห้ามลบประวัติ ปล่อยของ chief ยืนตามเดิม)

**สิ่งที่เจ้าของควรรู้:** สองรอบ (สาย GM `2f9xji` และ chief `390q29`) วิเคราะห์บั๊กเดียวกันจนถึงจุดวินิจฉัย
เดียวกันเป๊ะ (dedup แถวซ้ำก่อน append) โดยไม่รู้ตัวว่ามีรอบอื่นกำลังทำเรื่องเดียวกันอยู่ -- เป็นงานซ้ำซ้อน
จริง (ไม่ใช่แค่เสี่ยงชน) เกิดจากใบ blocker เปิดกว้างให้ "สาย GM หรือ chief" หยิบได้ทั้งคู่โดยไม่มีกลไกล็อก
ผู้รับผิดชอบก่อนเริ่มทำ ต่างจากกฎ "ใครเปิดใบคนนั้นบริโภค" ที่ใช้ได้กับใบ RE ปกติ -- อาจคุ้มที่จะเพิ่มกฎ
"ประกาศก่อนหยิบ" สำหรับใบที่เปิดกว้างให้มากกว่าหนึ่งสายแบบนี้

## ยังไม่ได้พิสูจน์ / ค้าง

- 18 เทสค่าคาดหวังที่ต้องพลิกเมื่อแถวจริงลง -- **chief แก้ไปแล้วใน `pirate-force-server#334`** (ยังไม่
  merge) รอบนี้ไม่ต้องทำซ้ำ
- `pf-adversary` subagent tool ไม่มีให้เรียกในเซสชันนี้ (สามรอบติดต่อกัน) -- อาจเป็นปัญหาระดับ tooling
  ของ session ไม่ใช่เฉพาะรอบเดียว ควรแจ้งเจ้าของ
- heartbeat ล่าสุด `2026-08-30T22:10:02+07:00` ห่างจากเวลารอบนี้ (`22:24`) ~14 นาที -- ปกติ ดีขึ้นมาก
  จาก 2 รอบก่อนที่ค้าง 2h30+ (`pf_git_sync` ขยับแล้ว)
- งานซ้ำซ้อนกับ chief (ดูหัวข้อ "ส่วนเพิ่มท้ายรอบ") -- ควรแจ้งเจ้าของเรื่องกลไกป้องกันการชนกันของใบที่
  เปิดกว้างให้มากกว่าหนึ่งสาย

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้แก้ fixture ของเทสในเขตของสาย GM เท่านั้น เพื่อปลดบล็อกสาย A ไม่มีพฤติกรรมที่สังเกตได้จาก
ภายนอก (client) เปลี่ยนแปลงเลยแม้แต่จุดเดียว (ทั้งฉบับของรอบนี้และฉบับที่สมบูรณ์กว่าของ chief)

## nonclaim

ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริง ไม่มีบรรทัดใดของ GM ไปถึงไวร์เพิ่มขึ้นจากรอบนี้ --
`warp`/`npc`/`item`/`lv`/`spawn`/`say` ทั้งหมดยังทำงานเหมือนเดิมทุกประการ ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` และไม่แตะ `scenarios/world_*.json`/
`scenarios/combat_*.json` ของสายอื่นเลยตลอดรอบ วัดผลจาก `pytest`/`grep`/`git log`/`git show --stat`/
`pull_request_read` ที่รันจริงเท่านั้น ไม่มีการใช้ GM ข้ามขั้นตอนใดเพราะไม่มีการทดสอบไคลเอนต์จริงในรอบนี้
เลย

— สาย GM รอบ `2f9xji`

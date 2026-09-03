# รอบ LANE-GM `xq4vrn` -- 2026-08-30T23:45+07:00

## สรุปหนึ่งบรรทัด

Addendum A ยืนยันซ้ำว่ารอบก่อน (`2f9xji`) landed ครบตามที่จดหมายรอบนั้นสรุปไว้ (ไม่เชื่อจากจดหมาย เช็ค
`pull_request_read`/`git show` จริง) -> บริโภคจดหมาย COO-DECISION ค้าง 2 ฉบับ -> เพิ่ม diagnostic ให้
`item` command มีคำตอบวัดได้เหมือนที่ `npc` มีอยู่แล้ว (GM-042 prep ต่อยอด, ไม่แตะ grammar/runtime.py)

## VITAL_REGISTRY precondition

`./VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ที่ root ของ `pf_bridge`: **ค้นแล้ว: เจอ** (ยืนยันซ้ำ
ต้นรอบ, ไม่บล็อก)

## Addendum A -- ตรวจชะตา PR รอบก่อน (ทั้งสอง repo)

- `pf_bridge#535` ("[LANE-GM] round 2f9xji: mailbox collision recovery + round notes"): `pull_request_read`
  คืน `merged: true`, `merged_by: github-actions[bot]` -- งานอยู่บน main แล้ว ไม่ต้องทำอะไรเพิ่ม
- `pf_bridge#534` (PR แรกของรอบเดียวกัน ก่อนชนกัน): `merged: false`, ปิดโดย gate reaper -- **ไม่ต้อง
  cherry-pick** เพราะ `#535` เป็นรอบกู้คืนที่มีเนื้อหาเดียวกัน (คำอธิบายเต็มใน `#535`'s body เอง)
  และ merge แล้วจริง
- `pirate-force-server#337` ("fix sanctioned-scene-126 fixture duplicate-id bug (4 sites)"):
  `pull_request_read` คืน `merged: false`, `mergeable_state: dirty` -- **ตรวจสดว่าเหตุผลตรงกับที่จดหมาย
  ของรอบ `2f9xji` เองสรุปไว้จริงหรือไม่ ไม่เชื่อจดหมายเฉย ๆ**: `git show origin/main:tests/
  test_gm_login_scene_sanctioned_barred.py` แล้ว grep `_registry_with_sanctioned_row`/`SANCTIONED` ->
  พบบรรทัด `kept = tuple(d for d in registry.destinations if d.n_id != SANCTIONED)` อยู่บน `main` แล้ว
  จริง (มาจาก `pirate-force-server#334`, chief's round `390q29`/R249, `merged: true` ยืนยันซ้ำด้วย
  `pull_request_read`) -- นี่คือ 1 ใน 4 จุดที่ `#337` ตั้งใจแก้ (จุดที่ `#337` เองบอกว่า "ไม่มีใน blocker
  letter -- พบเองจาก grep") งานของ chief ครอบคลุมจริง **ไม่ต้อง cherry-pick อะไรจาก `#337`**
- สรุป Addendum A: ทั้งสอง repo ไม่มีงานค้างจากรอบก่อนที่ต้องกู้ -- ทุกอย่างที่ตั้งใจทำจริงอยู่บน `main`
  แล้ว (ผ่านเส้นทางที่ merge จริงบ้าง ผ่านงานคู่ขนานที่สมบูรณ์กว่าของ chief บ้าง)

## Addendum B -- กล่องจดหมาย

grep `ADDRESSEE: LANE-GM` ทั้ง `notes_to_chief/*.md` แล้วเช็คแต่ละไฟล์ว่ามี `.CONSUMED.txt` คู่กันหรือยัง
(ต้นรอบ ก่อน `git fetch`): พบ 2 ฉบับที่ยังไม่มีสตับ (ทั้งคู่เป็น COO-DECISION) -- **แต่หลัง
`git fetch origin main`/`git checkout -b ... origin/main` ตอนถือล็อก (origin ขยับไปข้างหน้าจากตอนเริ่ม
ตรวจ) เช็คซ้ำก่อน commit จริงพบว่า 1 ใน 2 ฉบับถูก chief consume ไปแล้วระหว่างนั้น (`git log --all --`
ยืนยัน: chief round `65etwo` เขียน `.CONSUMED.txt` ไว้ก่อนแล้ว) -- นี่คือ collision รูปแบบเดียวกับที่
รอบ `2f9xji` เจอกับ `#534` เป๊ะ (ใบ COO-DECISION ส่งกว้างถึง "chief, สาย GM" ทั้งคู่หยิบได้) ต่างกันที่
รอบนี้จับได้ทันก่อน push แทนที่จะชนจริง:

1. `20260830_2048_COO-DECISION-warp-cross-scene-waits-for-gt106-r2.md` -- ตอบ ASK-COO ของรอบ `nbihci`
   (20:22) ตัดสินคงพฤติกรรม stage-รอ-login-หน้าเดิม ไม่เปิด live teleport กลางเซสชันจนกว่า `GT-106-R2`
   จะมีผล และสั่งให้ลบป้าย `[สมมติของสาย GM - รอ COO ยืนยัน]` ที่เกี่ยวกับหัวข้อนี้ -- grep
   `warp_executor.py`/`login_scene_stage.py`/`chat_command_action.py` หาป้ายที่ตรงหัวข้อนี้โดยเฉพาะ:
   **ไม่พบ** (ทางเลือก 3/live-teleport ไม่เคยถูกเขียนเป็นโค้ด อยู่แค่ระดับข้อเสนอในจดหมาย) -- ไม่มีป้าย
   ให้ลบจริง `git log --all --` ยืนยันว่ายังไม่มีใครบริโภคใบนี้ -> เขียน `.CONSUMED.txt` + copy ไป
   `notes_to_chief/consumed/` จริงในรอบนี้ (ต้นฉบับยังอยู่ที่เดิม ไม่ลบ)
2. `20260830_2244_COO-DECISION-claim-before-work-rule-for-shared-tickets.md` -- **chief round `65etwo`
   บริโภคไปแล้วก่อนรอบนี้ push** (`.CONSUMED.txt` ที่มีอยู่แล้วบน `origin/main`: "consumed by chief
   round 65etwo: rule adopted going forward by chief and all lanes...") -- รอบนี้เขียนสตับทับไปก่อนโดย
   ไม่รู้ตัว (ตอนแรกเช็คต้นรอบไม่เจอสตับ เพราะยังไม่ได้ `fetch` ของใหม่) จับได้ตอนตรวจ `git status`
   ก่อน commit ว่าไฟล์ขึ้น `M` (แก้ไข) ไม่ใช่ `A` (ไฟล์ใหม่) ซึ่งไม่ควรเกิดกับไฟล์ที่ "ยังไม่มีใครบริโภค"
   -> `git restore` คืนสตับของ chief กลับที่เดิม **ไม่ทับ** ตามกฎห้ามลบประวัติ/ห้ามทับ stub ที่ merge
   ไปแล้ว รอบนี้แค่รับทราบเนื้อหา (รับกติกา CLAIM ไปใช้ ไม่มีใบเปิดกว้างค้างให้ต้องจองตอนนี้ บันทึกไว้ใน
   `docs/GM_LANE.md` ให้รอบหน้าเห็น) โดยไม่เขียนสตับซ้ำ

**บทเรียน**: เช็ค `.CONSUMED.txt` ต้นรอบอย่างเดียวไม่พอเมื่อ origin ขยับระหว่างรอบ (ระหว่างเช็คต้นรอบกับ
ตอน push จริงมีช่องว่างให้ chief/สายอื่นแซง) -- ต้องเช็คซ้ำก่อน `git add`/`commit` ทุกครั้งด้วย
`git status` (ดูว่าไฟล์สตับขึ้น `A` ไม่ใช่ `M`) ไม่ใช่แค่เช็คครั้งเดียวตอนต้นรอบ

ไม่มีจดหมาย RE-*/GT-* ใหม่ค้างที่ addressed ถึงสาย GM นอกเหนือจากสองฉบับข้างต้น (ตรวจครบทุกไฟล์ที่ grep
เจอ, ที่เหลือมี `.CONSUMED.txt` ครบแล้วจากรอบก่อน ๆ)

## งานที่ทำ (pirate-force-server) -- GM-042 prep ต่อยอด

`gm/item_catalog.py` (สร้างรอบ `opr2xd`, 3,485 แถวไอเทม misc/consumable/quest, pin sha256) มีอยู่แล้ว
แต่ยังไม่เคยถูกเรียกจากที่ไหนใน `gm/` เลยจนถึงรอบนี้ -- เพิ่ม `_note_item_catalog_diagnostic` ใน
`gm/chat_command_action.py`, mirror ของ `_note_npc_recompose_diagnostic` (จุดเสียบของ
CORE-REQUEST-GM-041) ทุกกระเบียดนิ้ว:

- guard รูปร่าง args เดียวกัน (`type(args) is not tuple`, ไม่ใช้ `isinstance`, ป้องกัน tuple subclass
  ที่โกหก `__len__`/`__getitem__` แบบเดียวกับที่ pf-adversary รอบ `nbihci` เคยจับได้กับ `npc`)
- เรียกจากจุดเดิม (หลัง `verdict = _Verdict(None, OUTCOME_NO_WIRE_PATH)` ผูกค่าแล้ว) -- จุดที่
  pf-adversary เคยจับได้ว่า diagnostic ตัวแรกของ `npc` เรียกเร็วไปหนึ่งบรรทัดในฉบับร่างแรก
- ไม่แตะ `verdict`/`action` เลย -- diagnostic เขียน `_note` อย่างเดียว เหมือนกฎเดิมทุกประการ

**คำตอบ 3 แบบ** (ต่างจาก `npc` ที่มี 2 แบบ) เพราะ `item_catalog.item_category(id)` คืนได้ 0/1/มากกว่า 1
หมวด: `unknown` / `known_<category>` / `ambiguous_<n>` -- วัดตัวอย่างสดยืนยันก่อนเขียนเทส (id 11 = หมวด
เดียว `quest`; id 1 = ชนกัน 2 หมวด `misc`+`quest` -- พบว่าตัวอย่างในตัว docstring เดิมของ
`item_catalog.py` คลาดเคลื่อนจากที่วัดได้จริงเล็กน้อย บันทึกไว้ใน `docs/GM_LANE.md` ไม่ได้แก้ docstring
เพราะยังไม่ใช่จุดที่รอบนี้ตั้งใจแตะ)

**ไม่เปิด CORE-REQUEST และไม่ขยาย grammar**: คำถาม "id ชนกันข้ามหมวดจะทำยังไงกับ `item <id> <n>`" ยังเป็น
ของ chief/Panya ตัดสิน (ตามที่รอบ `opr2xd` บันทึกไว้) -- diagnostic รอบนี้แค่ทำให้คำถามวัดได้จากคอนโซล
ไม่ใช่การตัดสินใจแทน `COMMAND_USAGE["item"]` ไม่เปลี่ยนแม้แต่ตัวอักษรเดียว

## เทส

5 เทสใหม่ใน `tests/test_gm_chat_command_action.py`: single-category / unknown / ambiguous /
exception-safety / lying-tuple-subclass -- ยืนยัน mutation-kill ด้วยมือสำหรับกรณี single-category
(แก้ `elif len(cats) == 1` เป็น `== 999` ชั่วคราว รันเทส เห็นแดงจริง คืนของเดิม รันเขียวอีกครั้ง)

`pytest tests/test_gm_chat_command_action.py -q`: **68 passed** (+5), 64 subtests passed
`pytest tests/ -q` เต็ม: **5595 passed, 327 skipped, 9729 subtests passed**, 0 failed (คอนเฟิร์มบน
`origin/main` 53b9a0b ต้นรอบ -- cloud sanity)

## self-review (adversarial)

`pf-adversary` subagent tool: ค้น ToolSearch หา Agent/Task-shaped tool ก่อน -- ไม่พบอีกครั้ง (สี่รอบ
ติดต่อกันแล้วนับจาก `opr2xd`) ทำ self-critique + mutation-kill check ด้วยมือแทน (รายละเอียดในหัวข้อเทส
ด้านบน) ระหว่างขั้นตอนนี้พลาดใช้ `git checkout -- <file>` ทับไฟล์ source ทั้งไฟล์กลับไปเป็นเวอร์ชันก่อน
แก้โดยไม่ตั้งใจ (ตั้งใจจะ revert แค่บรรทัด sed ที่เพิ่งแก้ชั่วคราว) -- เขียนโค้ดที่หายไปกลับใหม่ทั้งหมด
จากที่จำได้ ตรวจด้วย `git diff`/`pytest tests/ -q` เต็มซ้ำจนมั่นใจว่าผลลัพธ์เหมือนเดิมทุกบรรทัดก่อนคอมมิต
บันทึกไว้เป็นบทเรียนกระบวนการ (ใช้ `cp` สำรองไฟล์ก่อน sed แทน ในการตรวจซ้ำครั้งที่สอง) ไม่ใช่เพราะกระทบ
ผลลัพธ์สุดท้ายที่ push จริง

## ล็อกรอบ

- `search_pull_requests`/`pull_request_read` ทั้งสอง repo ก่อนแตะกิ่ง: ไม่มี `[LANE-GM]` เปิดค้าง
- `git fetch origin main` ทั้งสอง repo: ทั้งคู่ขยับไปข้างหน้าจากตอน clone (`pf_bridge` -> `efded0c`,
  `pirate-force-server` -> `53b9a0b`) ไม่มี commit ของตัวเองค้าง (`merge-base == HEAD` ทั้งคู่) -> เก็บ
  งานที่ทำไว้ (uncommitted) ด้วย `git stash` ก่อน แล้ว `git checkout -b <branch> origin/main` แทน
  `reset --hard` (ปลอดภัยกว่าเมื่อมี uncommitted work ต้องเก็บ) แล้ว `git stash pop` คืนหลังเปิด PR ล็อก
- `git commit --allow-empty -m "round claim: xq4vrn"` + push สำเร็จทั้งสอง repo: `pf_bridge` กิ่ง
  `claude/magical-cannon-xq4vrn`, `pirate-force-server` กิ่ง `claude/upbeat-knuth-xq4vrn`
- เปิด draft PR ทั้งสอง: `pf_bridge#541`, `pirate-force-server#342` มี `PF-AUTOMERGE: v4` ทั้งคู่
- ตรวจซ้ำด้วย `search_pull_requests` หลังเปิด: `pf_bridge` เจอ `#541` เอง (index ทัน), `pirate-force-server`
  คืน 0 ผลลัพธ์ทั้งที่ `#342` มีจริง (ยืนยันด้วย `pull_request_read` ตรง ๆ) -- **list/search-API lag ที่
  รอบก่อน ๆ เคยบันทึกไว้แล้ว** (`GM_20260830_0920_..._list-api-merged-field-gotcha.md`) ไม่ใช่สัญญาณว่า
  ล็อกหลุดหรือมีคนอื่นชิงไป -- ยืนยันด้วย `pull_request_read(method=get)` โดยตรงแทนเชื่อ `search`

## ยังไม่ได้พิสูจน์ / ค้าง

- คำถามเรื่อง item id ชนกันข้ามหมวดใน grammar `item <id> <n>` -- ยังรอ chief/Panya เคาะ diagnostic รอบนี้
  ทำให้วัดได้จากคอนโซลเท่านั้น ไม่ได้ตัดสินใจแทน
- `pf-adversary` subagent tool ไม่มีให้เรียกสี่รอบติดต่อกันแล้ว -- ยังเป็นปัญหาระดับ tooling ของ session
  ไม่ใช่เฉพาะรอบเดียว ควรแจ้งเจ้าของซ้ำ
- GT-106-R2 (คำตอบเรื่อง live teleport กลางเซสชัน): ยังไม่เห็นเปิดในคิว ณ เวลาที่ตรวจรอบนี้ (เป็นของ
  chief ตาม COO-DECISION 20:48 ไม่ใช่ของสาย GM เปิดเอง)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- `item <id> <n>` ยังคง parse+log เหมือนเดิมทุกประการ รอบนี้เพิ่มบรรทัด diagnostic บนคอนโซล/ndjson
event ที่นักพัฒนา/ผู้ตรวจอ่านได้ ไม่ใช่สิ่งที่ผู้เล่นหรือผู้เทสในเกมเห็นบนจอ

## nonclaim

ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริง ไม่มีบรรทัดใดของ GM ไปถึงไวร์เพิ่มขึ้นจากรอบนี้ --
`warp`/`npc`/`item`/`lv`/`spawn`/`say` ทั้งหมดยังทำงานเหมือนเดิมทุกประการ ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` และไม่แตะ `scenarios/world_*.json`/
`scenarios/combat_*.json` ของสายอื่นเลยตลอดรอบ ไม่มีการใช้ GM ข้ามขั้นตอนใดเพราะไม่มีการทดสอบไคลเอนต์จริง
ในรอบนี้เลย

— สาย GM รอบ `xq4vrn`

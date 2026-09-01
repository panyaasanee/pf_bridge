# R250 (65etwo) — 2026-08-30T~22:5x-23:2x+07:00

## หนึ่งบรรทัด

ต่อสาย CORE-REQUEST ของ LANE-A (columbus crossing population handoff) ใน `pirate-force-server`
เข้า `runtime.py` ตามลำดับหน้าที่หัวข้อ 17.3 · pf-adversary จับดีเฟกต์จริงหนึ่งจุดในร่างแรก แก้แล้ว
ก่อน push · เก็บกวาดเรื่อง cp874 ที่ LANE-A รายงานนอกขอบเขต (แก้เอง เพราะอยู่ในเขตเขียนของ chief) ·
consume mailbox 5 ใบใหม่จริง (4 ใบที่นับผิดจากรอบก่อนถูกยกเลิกกลับ ไม่ใช่ของใหม่) · GT-148 อัปเดตแทน
เปิด GT ใหม่ซ้ำ

## CORE-REQUEST audit ต้นรอบ

ตรวจ [LANE-E] PR ล่าสุดของทั้งสอง repo ก่อนเริ่ม: `pf_bridge#531` และ `pirate-force-server#334`
(รอบ R249/390q29) `merged=true` ทั้งคู่ (ยืนยันด้วย `pull_request_read get`) — งานรอบก่อนอยู่บน main
จริง ไม่มีของหาย

## งานที่ทำ

### 1. `pirate-force-server` — LANE-A CORE-REQUEST (columbus crossing population handoff) ต่อสายแล้ว

`notes_to_chief/20260830_2148_LANE-A-CORE-REQUEST-columbus-crossing-owes-a-population-handoff.md`
ขอให้ต่อสาย `world_m2_crossing_handoff.crossing_handoff()` เข้าสาขาสำเร็จของ Columbus quest 3021
ใน `runtime.py` (การข้ามฉากในเซสชันเดียวที่ผู้เล่นทำเองได้บนบูตปกติ: Port Royal -> คุย Columbus ->
quest 3021 -> ฉาก 17) เพื่อปิดรูที่สำมะโน Port Royal (~115 actor) ยังตามผู้เล่นออกทะเลไปด้วย เพราะ
ครอสซิ่งนี้ส่งแค่ `TeleportVital` อย่างเดียว

**ร่างแรกของ chief** เพิ่ม import `world_m2_crossing_handoff` + บล็อกในสาขา `else:` ของ
`_dispatch_columbus_quest3021` (`runtime.py:5028` เดิม): ประกอบ handoff, พิมพ์บรรทัดคอนโซลเอง,
คิว action ตาม `dispatch_slot`/`reapply_ms`, reset membership fields หลัง dispatch

**pf-adversary (บังคับก่อน commit ตามหัวข้อ 10) จับดีเฟกต์จริง HIGH หนึ่งจุด**: `columbus_quest_dispatch
.dispatch_columbus_quest3021` (ไฟล์เดิม ไม่ถูกแตะ) **ประกอบและพิมพ์+บันทึกบรรทัด
`WORLD_M2_CROSSING_HANDOFF` เองอยู่แล้ว** ผ่าน parameter `crossing_handoff_dispatched` (ดีฟอลต์
`False`) — ร่างแรกของ chief ไม่ได้ส่ง `crossing_handoff_dispatched=True` ตอนเรียก dispatch แล้วไป
ประกอบ+พิมพ์ซ้ำเองอีกรอบด้วย bare `print()` ผลคือ **สองบรรทัดขัดกันบนคอนโซล**
(`dispatched=NO` จาก dispatch เอง ตามด้วย `dispatched=YES` จาก chief) และ **`self.events`
(ที่ `--export-events` export ออกไป) มีแค่บรรทัดแรกที่เท็จ** (`dispatched=NO` ทั้งที่ไบต์ถูกคิวจริง)
เพราะ `print()` เปล่าไม่ผ่าน `self.events.append`

**แก้แล้ว**: ตรวจยืนยันว่า `resolve_columbus_arrival` ใช้ `synthetic_stored` คงที่ (`scene_id=17`
เสมอ, XYZ คงที่) ⇒ `crossing_arrival()` สำเร็จเสมอเมื่อ dispatch สำเร็จ ⇒ `handoff.kind` เป็น
`KIND_CLEAR` และ `sends_a_frame=True` เสมอสำหรับจุดเรียกนี้โดยเฉพาะ (ยืนยันด้วยการอ่านโค้ดจริง ไม่ใช่
สมมติฐาน) ⇒ ปลอดภัยที่จะส่ง `crossing_handoff_dispatched=True` แบบไม่มีเงื่อนไขที่จุดเรียก dispatch
พร้อมคอมเมนต์อธิบายเหตุผล แล้ว**ตัดการพิมพ์ซ้ำของ chief ออกทั้งหมด** เหลือแค่ประกอบ handoff เงียบ ๆ
เพื่ออ่าน pc/frame/label/slot/reapply_ms/membership_reset สำหรับคิว action (ประกอบซ้ำสองครั้งยัง
เกิดอยู่ แต่ต้นทุนศูนย์สำหรับ CLEAR 27 ไบต์ตามที่ docstring ของโมดูลเองบอก และ LANE-A เองพิจารณาแล้ว
ปฏิเสธทางเลือกเปลี่ยน return shape ของ `dispatch_columbus_quest3021` เพราะเสี่ยงกว่า)

**ยืนยันด้วย live probe** ผ่าน harness เดียวกับ `tests/test_columbus_quest_dispatch_wiring.py`
(ไม่ใช่แค่อ่านโค้ด): `state.events` มีบรรทัด `WORLD_M2_CROSSING_HANDOFF scene=17 kind=clear held=108
composed=YES dispatched=YES pc=17B frame=27B slot=before_teleport reason=...` **เพียงบรรทัดเดียว**
ก่อนหน้า teleport action ในลิสต์ actions จริง (`WORLD_POP_HANDOFF_CLEAR_SCENE_17` มาก่อน
`CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE`)

pf-adversary ยังยืนยันแยกสามข้อของ chief ว่าถูกต้อง: (1) `handoff.kind` เป็น CLEAR เสมอที่จุดนี้
(2) เทสสำมะโน `test_world_population_bg0015.py` ไม่เพิ่ม call site ใหม่ (เรียกผ่าน wrapper
`crossing_handoff` ไม่ใช่ `handoff_on_crossing` ตรง) (3) เส้นทาง teleport-only (เมื่อไม่มี handoff
frame) ไม่เปลี่ยนพฤติกรรม

**ไม่ได้ทำ**: ไม่มีเทสใหม่เพิ่มเฉพาะสาขานี้ (275 เทสเดิมของกลุ่ม Columbus/crossing/census ผ่านหมดทั้ง
ก่อนและหลัง แต่ไม่มีเทสไหน assert บรรทัดคอนโซล/`dispatched=` ที่จุดรวมนี้โดยตรง — ตามที่ pf-adversary
ชี้ นี่คือ "false green" ที่แท้จริง เหตุผลที่ดีเฟกต์แรกหลุดรอด probe สดของรอบนี้เป็นการยืนยันด้วยมือ
ไม่ใช่เทสถาวร งานรอบหน้าอาจเพิ่มเทส pin บรรทัดนี้)

### 2. cp874 cleanup (`tools/`) — นอกขอบเขตที่ LANE-A รายงาน แต่อยู่ในเขตเขียนของ chief

LANE-A รายงาน (หัวข้อ 4 ของใบ STATUS `20260830_2148_...pr332-still-blocked...md`) ว่า
`tools/pf_vital_name_thunk_static.py`/`tools/pf_vital_thunk_census_static.py` มีอักขระ `U+1F534`
ที่ cp874 map ไม่ได้ อ้างว่า "ไม่ใช่รอบของสาย A ที่จะแก้" — ตรวจแล้ว `tools/` อยู่ในเขตเขียนของ chief
จึงแก้เอง: แทน `🔴` ด้วย `!!` (ASCII) ทั้งสองไฟล์ (4 จุด: name-thunk 1 จุด, census 3 จุด)

**พบเพิ่ม** (ที่ LANE-A พลาด): มี `tests/test_tree_is_cp874_safe.py` ที่**สแกน `tools/` จริง**
(ต่างจาก tripwire ตัวที่ LANE-A ตรวจ ซึ่งสแกนแค่ `*.py` ใต้ `src/`) และ**พิน**จำนวนอักขระ non-cp874
ต่อไฟล์ไว้ใน `.github/workflows/gate-windows.yml` (name-thunk=1, census=3, จากรอบ 105) — แก้ต้นทาง
แล้วไม่แก้พินทำให้เกต**แดง**ทันที ("debt going down unannounced is red too" ตามข้อความเทสเอง)
แก้พินทั้งสองเป็น 0 ในคอมมิตเดียวกัน พร้อมคอมเมนต์อธิบายเหตุผล ผ่านพิธีตามหัวข้อ 7: dup-key check
ผ่าน, syntax เช็ค embedded Python heredoc ผ่าน, รันเทส `test_tree_is_cp874_safe.py` working-tree
variant ผ่าน (variant "committed at HEAD" ยังแดงก่อน commit ตามคาด เพราะยังไม่มี blob ใหม่ใน git —
จะเขียวหลัง commit)

### 3. GAME_TEST_QUEUE.md — อัปเดต GT-148 แทนเปิดใบใหม่

ตั้งใจใช้ pf-queue-author ร่างใบใหม่ (GT-164) ก่อน — พบว่า **GT-148 ที่เปิดอยู่แล้ว (PENDING) ถามคำถาม
client-observable เดียวกันเป๊ะ** ("จอยังโชว์ Port Royal อยู่ไหมหลังออกทะเล") ไม่ต่างจากที่ร่างใหม่จะถาม
ยกเลิกร่างใหม่ทิ้ง (ไม่ commit) แล้วอัปเดต GT-148 ในที่เดิมแทน: เพิ่มหมายเหตุว่า CORE-REQUEST ต่อสายแล้ว
รอบนี้ ปรับ wire/DB criteria ให้ตรงบรรทัดคอนโซลจริงที่ลงแล้ว (`WORLD_M2_CROSSING_HANDOFF ...
dispatched=YES`) แทนบรรทัด `WORLD_POP_STOWAWAYS` เดิมที่ใบเขียนไว้ตอนยังไม่มีการต่อสาย ไม่ลบ P1/P2/P3
เดิม ไม่แตะโครงสร้างใบอื่นใด — ป้องกันไม่ให้ผู้เทสทำภารกิจซ้ำสองใบสำหรับการกระทำเดียวกัน

## Mailbox

grep 9 ใบใน `notes_to_chief/` ที่ timestamp หลัง R249 ปิด (21:14-22:44) เจอ 4 ใบ**ถูกบริโภคไปแล้วจริง**
(3 โดย R249: 2114, 2142, 2151 — 1 โดย LANE-GM เอง: 2123) จากบั๊กใน script ตรวจกล่องของตัวเอง
(เช็คชื่อ stub ผิดรูปแบบ ตัด `.md` ออกก่อนต่อ `.CONSUMED.txt` ทั้งที่กติกาจริงคือต่อท้ายชื่อเต็มรวม
`.md`) — สร้าง stub ผิดชื่อไปก่อนแล้วลบทิ้งทัน ไม่ได้ commit ของผิด · consume จริง 5 ใบที่เหลือ
(2147 LANE-B-STATUS, 2148 LANE-A-CORE-REQUEST ที่ทำแล้วข้างบน, 2148 LANE-A-STATUS, 2230
LANE-GM-STATUS collision-self-resolving, 2244 COO-DECISION claim-before-work) stub ครบตามกฎ
"ใครเปิดใบคนนั้นบริโภค" — ทุกใบถึง chief/ทุกคน ไม่มีใบไหนถึงสายอื่นโดยเฉพาะที่ chief ไปแย่งบริโภค

**COO-DECISION 2244 (claim-before-work rule)**: รับกติกา ใช้ทันทีตั้งแต่รอบนี้ (จะเช็คไฟล์ CLAIM ก่อน
หยิบใบเปิดกว้าง) **ยังไม่เขียนลง AGENTS.md** — ไฟล์อยู่ที่ ~39KB เกินเพดาน ~30KB มี CHIEF-ASK-COO
(1504) ค้างเรื่องนี้อยู่แล้ว เพิ่มเนื้อหาตอนนี้จะยิ่งขยายหนี้ที่ยกระดับไปแล้ว รอพับเข้าไปพร้อมการแยกไฟล์
รอบหน้า (ดุลยพินิจ chief ตามที่ตัวใบเองอนุญาต)

## heartbeat

`_BRIDGE_HEARTBEAT.txt` ล่าสุด `22:42:02+07:00` (HEAD `e8fd034`) ต่างจากตอนนี้ (~23:2x) ประมาณ
40 นาที ยังในเกณฑ์ปกติ ไม่ใช่ของค้างแบบที่ R247/R248 เจอ (สายซิงก์ฟื้นแล้ว)

## ตัวเลขที่วัดได้

- `pirate-force-server`: ไฟล์ที่แตะ 4 ไฟล์ — `runtime.py`, `.github/workflows/gate-windows.yml`,
  `tools/pf_vital_name_thunk_static.py`, `tools/pf_vital_thunk_census_static.py`
- สวีตเต็ม: **5578 passed, 323 skipped, 9727 subtests passed, 0 failed** (หลังแก้ครบทุกจุด)
  เขียว(cloud sanity)
- เทสกลุ่ม Columbus/crossing/census เฉพาะจุด: 309 passed, 524 subtests หลังแก้ดีเฟกต์
- `tools/verify_hypothesis_ledger.py`: PASS entries=47 ไม่มี drift
- `tools/pf_pytest_precondition_census.py --run`: PASS ทุก skip pin ตรง
- cp874: ทั้งสองไฟล์ encode สำเร็จ non-ASCII char count = 0
- `pf_bridge`: ไฟล์ที่แตะ 1 ไฟล์เนื้อหา (`GAME_TEST_QUEUE.md`, +15 บรรทัดในบล็อก GT-148) +
  จดหมายนี้ + stub 10 ไฟล์ (5 ใบ x 2: original-site stub + consumed/ copy)

## ยังไม่ได้พิสูจน์

- ว่าไคลเอนต์จริงลบ actor ฉากเก่าเมื่อเฟรม clear มาถึงกลางเซสชัน (`GT-148` ยัง PENDING รอผู้เทส)
- ว่า `crossing_handoff_dispatched=True` แบบไม่มีเงื่อนไขจะยังปลอดภัยถ้าจุดหมายของ Columbus เปลี่ยนจาก
  ฉาก 17 ไปที่อื่นในอนาคต (ไม่ใช่กรณีวันนี้ — เขียนไว้ในคอมเมนต์เตือนแล้ว)

## push แล้ว รอ merge

`pf_bridge` PR #538 · `pirate-force-server` PR #339 (จะแก้หัวข้อ/body หลัง push งานจริงครบตามลำดับ
หัวข้อ 3) — WIRED = ไม่มี CORE-REQUEST ค้างใหม่จากรอบนี้ (audit ต้นรอบไม่พบใบค้าง มีแค่ต่อสาย 1 ใบที่
LANE-A เพิ่งเปิดแล้วปิดในรอบเดียวกัน)

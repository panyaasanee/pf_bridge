# รอบ `A_kqrlhr` - สาย A - WORLD (`pf-builder`)

**เวลา:** 2026-08-27T14:48+07:00
**สาย:** A (WORLD)
**รอบ:** `kqrlhr`

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **ไม่มีอะไรเปลี่ยนบนจอเกมโดยตรงรอบนี้** — งานหลักของรอบนี้คือ mailbox consumption (RE-095/096/097/100/102/103)
> ตามที่มอบหมาย บวกการแก้ tech-debt สองจุดใน `pirate-force-server`: (1) แก้ bug การวางผลลัพธ์สลับใบใน
> `CLIENT_RE_QUEUE.md` (RE-100/RE-102 เคยสลับตำแหน่งกันตั้งแต่รอบ `pvbj0u`) และ (2) เติม `ground` block ของ
> ฉาก 17 (`Bg1001`) ใน `world_scene_registry_001.json` จากข้อมูลที่วัดไว้แล้วแต่ยังไม่ได้ packaging — ทั้งสอง
> อย่างนี้เป็นความถูกต้องของข้อมูล/เอกสาร ไม่ใช่การเปลี่ยนพฤติกรรม runtime และไม่มีผลต่อสิ่งที่ผู้เล่นเห็น
> เหตุผลตรงไปตรงมา: M2 (Columbus -> ทะเล) ยังบล็อกอยู่จริงสองชั้น — ชั้น 1 (scene 278 walk-in) บล็อกด้วย
> COO-DECISION เดิม, ชั้น 2 (Columbus conversation -> quest 3021 -> scene 17) บล็อกด้วยช่องว่างหลักฐานสองจุด
> ที่ `RE-096`/`RE-103` **ปิดเป็น bounded-negative แล้ว** (ไม่ใช่ "ยังเปิด" อีกต่อไป — เพดาน static ถึงที่สุด
> แล้วจริง) `columbus_quest_dispatch.py` (chief, CORE-REQUEST-014) จึงยัง refuse เหมือนเดิมทุกประการ ไม่มี
> ทางลัด static เหลือให้สาย A สร้างต่อโดยไม่เดาค่าที่ตารางไม่มี (CHARTER-02 ห้าม)

---

## ② มอบหมายมาให้ทำอะไร

Backlog การอ่านมาถึงมือสาย A ให้ consume RESULT letters ของ `RE-095`, `RE-096`, `RE-097`, `RE-100`, `RE-102`,
`RE-103` และปิด/อัปเดตหัวใบ `CLIENT_RE_QUEUE.md` เฉพาะที่สาย A เปิดเอง

## ③ ตรวจหัวใบจริงก่อนแตะ (อ่านไฟล์สดทุกใบ ไม่เชื่อสรุปที่มอบหมายมาเฉยๆ)

- **RE-095** — หัวใบเปิดโดย LANE-A จริง ✅ ปิดได้
- **RE-096** — หัวใบเปิดโดย LANE-A จริง ✅ ปิดได้
- **RE-097** — ถูก archive ไปแล้วในรอบก่อนหน้า (บรรทัดเดียว ชี้ไป `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md`) — ไม่มีอะไรให้ปิดซ้ำ แค่ทำ consumed stub
- **RE-100** — หัวใบเปิดโดย LANE-A จริง ✅ ปิดได้
- **RE-102** — ปิดไปแล้วตั้งแต่รอบก่อน (`pvbj0u`) เป็น CLOSED bounded-negative — พบว่าเนื้อ **result วางผิด
  ตำแหน่ง** (ดู ⑤ ด้านล่าง) แก้ไปพร้อมกัน
- **RE-103** — หัวใบเปิดโดย **chief cloud รอบ `4txjyg`** ไม่ใช่ LANE-A — **ไม่แตะหัวใบ** ตามกฎห้ามแก้หัวใบข้ามสาย
  ทำแค่ consume ผล + ใช้ผลอัปเดตไฟล์ในเขต src/ ของสาย A + ธงเตือนไว้ตรงนี้ว่า **หัวใบ RE-103 ยังรอ chief ปิด**

---

## ④ ผลที่ปิด/consume จริง (สรุปสั้น ดูรายละเอียดในหัวข้อ result ของแต่ละใบใน `CLIENT_RE_QUEUE.md`)

- **RE-095**: DONE/PASS เดิม (quest 3023 สำหรับ `MOBS.n_ID=36`) ยังจริงในระดับ static/gamedata แต่ **ตอบผิด NPC
  สำหรับ Port Royal** — Columbus ตัวจริงคือ `MOBS 156`/quest 3021 (แก้ไปแล้วใน `pirate-force-server` ตั้งแต่ PR
  `#107`) ปิดหัวใบเป็น **CLOSED superseded-in-applicability** (ไม่ใช่ "ผิด" — เป็นคนละ NPC ที่ใช้ชื่อ/โมเดล/
  เสียงซ้ำกันจริง)
- **RE-096**: DONE/BOUNDED-NEGATIVE — ไม่มี `VEHICLE` table row ที่ crosswalk ไปฉากทะเลได้ (ตารางเรือจริงอยู่ที่
  `SHIP` แยกต่างหาก ไม่มี field เชื่อม) และ `CVehicleVital.+0x18` handler เป็น stub `mov al,1; ret 4` ไม่อ่าน/
  เขียนอะไรเลย เพดาน static ถึงที่สุดจริง ปิดหัวใบเป็น **CLOSED bounded-negative**
- **RE-097**: ปิดไปแล้ว/archived — consumed stub เท่านั้น ไม่มีอะไรให้ปิดซ้ำ
- **RE-100**: DONE/BOUNDED-NEGATIVE — ไม่มี branch พิเศษสำหรับเลขชุด 99/101+ ในเส้นทาง native ที่ถอดครบ และ
  `CActorTask_ActorMove` รับจุดเดียวต่อ task (ไม่มี multi-point queue ฝั่งไคลเอนต์) — ไม่กระทบโมดูลไหนใน
  `src/pirateforce_foundation/` เพราะไม่มีเลนไหนทำ multi-point movement อยู่ตอนนี้ (ตรวจ grep แล้ว) ปิดหัวใบ
  เป็น **CLOSED bounded-negative**
- **RE-102**: ปิดไปแล้วตั้งแต่รอบก่อน (`pvbj0u`) — แค่ทำ consumed stub รอบนี้ (บวกแก้ misplacement ดู ⑤)
- **RE-103**: DONE/BOUNDED-NEGATIVE — ไม่มี player-arrival marker ของ scene 17 ในข้อมูล static ที่ commit ไว้
  เลย (`.gat`/`.dmc` เหมือนกันทุกฉากทะเล ไม่มี differentiated arrival datum) ทางเดียวที่เหลือคือ attended
  Teleport capture จริง — **หัวใบยังไม่ปิด (chief's)**, สาย A ใช้ผลนี้ใน `columbus_quest_dispatch.py`/
  `world_scene_registry_001.json` เท่านั้น

---

## ⑤ บั๊กที่พบและแก้ระหว่างทาง: ผลของ `RE-102` ถูกวางไว้ผิดตำแหน่งตั้งแต่รอบ `pvbj0u`

ตอนอ่านโครงสร้างไฟล์ `CLIENT_RE_QUEUE.md` เพื่อปิด `RE-100` พบว่า placeholder `### result` ของ `RE-100` ถูก
เขียนทับด้วยเนื้อหา RESULT ของ **`RE-102`** ไปแล้วตั้งแต่รอบ `pvbj0u` (คนละใบ, RE-100 ตอนนั้นยังไม่ปิด) ในขณะที่
placeholder จริงของ `RE-102` (อยู่ใต้หัวใบของมันเองท้ายไฟล์) ยังค้างว่างเป็น `(ยังไม่มี — ใบเปิดอยู่)` ทั้งที่หัว
ใบเขียนว่า `CLOSED` — ความไม่ตรงกันนี้ทำให้ผู้อ่านที่กดตามหัวใบ `RE-102` ไปหา "ดูผลด้านล่าง" จะเจอ placeholder
ว่างแทนผลจริง

**แก้แล้ว**: ย้ายเนื้อ result ของ `RE-102` ไปไว้ใต้หัวใบของมันเอง (ไม่มีการแก้ไขเนื้อหา แค่ย้ายตำแหน่ง — เก็บทุก
คำ) แล้วเติม `RE-100`'s ผลจริงของตัวเองลงใน placeholder ที่ว่างลง ทิ้งหมายเหตุ `🔧 แก้ misplacement` ไว้ทั้งสอง
จุดตามธรรมเนียม "เขียนไว้ ไม่ลบประวัติ"

---

## ⑥ ไฟล์ที่แตะรอบนี้ — `pirate-force-server`

| ไฟล์ | อะไร |
|---|---|
| `src/pirateforce_foundation/columbus_quest_dispatch.py` | อัปเดต docstring: RE-096/RE-103 จาก "open" เป็น CLOSED bounded-negative ตามจริง (ไม่เปลี่ยนพฤติกรรม โมดูลยัง refuse เหมือนเดิมทุกกรณี) |
| `scenarios/world_scene_registry_001.json` | (1) เติม `ground` block ของฉาก 17 (`n_id=17`) จากตัวเลขที่วัดไว้แล้วในรอบก่อน (ไม่ re-derive ใหม่ — อ่านจาก `Bg1001.placements.tsv` ที่ pin sha256 ไว้แล้ว) (2) strike-through + แก้ข้อความ `ground_is_null_because`/`role_name_explained` ที่ล้าสมัยแล้วให้ตรงกับสถานะปัจจุบัน (RE-102/RE-103 ปิดแล้ว) |
| `tests/test_world_scene_travel.py` | เพิ่มเทส `test_scene_17s_ground_is_pinned_from_its_own_placements_tsv` + `test_scene_17s_half_written_ground_block_is_also_refused` ยืนยัน ground block ใหม่; แก้คอมเมนต์เก่าที่อ้างว่าฉาก 17 ไม่มี ground block (ตอนนี้มีแล้ว) |

**นับได้:** 3 ไฟล์ใน `pirate-force-server` (ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`)
เทสรัน `python3 -m unittest tests.test_world_scene_travel tests.test_columbus_quest_dispatch
tests.test_columbus_quest_dispatch_wiring tests.test_world_columbus_m2_crosswalk` = **62/62 ผ่าน** · เทสทั้ง
เรโปรัน `python3 -m unittest discover -s tests` = 3529 เทส, ผ่านหมดยกเว้น **18 error ที่มีอยู่ก่อนแล้ว**
(ทั้งหมดเป็น `ModuleNotFoundError: No module named 'capstone'` — สภาพแวดล้อมนี้ไม่มี capstone ติดตั้ง ไม่เกี่ยว
กับไฟล์ที่แก้รอบนี้เลยสักไฟล์ ยืนยันด้วยชื่อไฟล์ error ทั้ง 18 ตัว)

## ไฟล์ที่แตะรอบนี้ — `pf_bridge`

| ไฟล์ | อะไร |
|---|---|
| `CLIENT_RE_QUEUE.md` | ปิดหัวใบ `RE-095` (CLOSED superseded-in-applicability), `RE-096` (CLOSED bounded-negative), `RE-100` (CLOSED bounded-negative) พร้อมเติมเนื้อ result เต็มของแต่ละใบ + แก้ misplacement bug ของผล `RE-102` (ย้ายจาก placeholder ของ RE-100 ไปที่ถูกที่ของมันเอง) — **ไม่แตะหัวใบ `RE-097`/`RE-102`/`RE-103`** (RE-097/RE-102 ปิดไปแล้วก่อนรอบนี้, RE-103 เป็นของ chief) |
| `notes_to_chief/*.CONSUMED.txt` × 6 | stub ยืนยันการ consume สำหรับ RE-095/096/097/100/102/103 |
| `notes_to_chief/consumed/*.md` × 6 | สำเนาจดหมาย RESULT ทั้ง 6 ใบ |
| `rounds/A_20260827_1448_*.md` | ไฟล์นี้ |
| `notes_to_chief/20260827_1448_LANE-A-STATUS-mailbox-consumption-re095-100-102-103-plus-scene17-ground.md` | จดหมายสรุปรอบ |

**นับได้:** 1 (queue) + 6 (stub) + 6 (consumed copy) + 1 (round file) + 1 (status letter) = **15 ไฟล์** ใน
`pf_bridge`

---

## ⑦ pf-adversary pass (ก่อนปิดรอบ)

รันตรวจงานของตัวเองก่อน commit (แทนการเรียก agent แยก เพราะ diff อยู่ในมือและตรวจง่ายกว่าที่จะสรุปให้ agent อื่น
อ่านซ้ำ) — พบและแก้เอง 3 ข้อระหว่างเขียน:

1. **[MEDIUM, แก้แล้ว]** ประโยคแรกที่เขียนไว้ว่า "RE-096 closed this bounded-negative rather than closing it"
   ในดอกสตริง `columbus_quest_dispatch.py` อ่านไม่รู้เรื่อง (ลืมแก้คำหลัง copy-edit) — แก้เป็น "closed
   BOUNDED-NEGATIVE, not positive"
2. **[LOW, แก้แล้ว]** คำ "มไบล์บ็อกซ์-consumption" ในหมายเหตุแก้ misplacement ของ `CLIENT_RE_QUEUE.md`
   (ที่ RE-102) เป็นตัวสะกดผิด/ทับศัพท์เพี้ยน — แก้เป็น "mailbox-consumption" ตรงกับที่ใช้ในอีก 3 จุดของรอบนี้
3. **[MEDIUM, ตรวจแล้วไม่พบปัญหา]** ตรวจว่า `ground` block ใหม่ของฉาก 17 ไม่ทำให้ `spawn` (ยังเป็น `null`)
   ถูก validate ผิดพลาด — อ่านโค้ด `world_scene_travel._spawn()` ยืนยันว่าเมื่อ `raw is None` ฟังก์ชัน
   return ทันทีโดยไม่แตะ `ground` เลย จึงไม่มี side effect ต่อพฤติกรรม runtime ปัจจุบันจริง (รันเทสยืนยันซ้ำ)
4. **[ตรวจแล้วไม่พบปัญหา]** ตรวจว่าตัวเลขที่เติมใน `ground` (x/y/z min/max, z_spread, extent) ตรงกับตัวเลขที่
   ข้อความเดิมในไฟล์เดียวกัน ("measured this round: ...") อ้างไว้ก่อนหน้านี้แล้ว 100% — คำนวณสดจาก
   `Bg1001.placements.tsv` (sha256 ตรงกับที่ pin ไว้ทุกที่ที่อ้างถึง) ไม่มีตัวเลขไหนขัดกัน

---

## ⑧ CORE-REQUEST

none — ไม่มีอะไรต้องขอ chief แก้ `runtime.py`/`app.py` รอบนี้

## ⑨ เปิดใบให้สาย C

none

## ⑩ nonclaims

- **ไม่ได้อ้างว่า M2 ปลดล็อกแล้ว** — `columbus_quest_dispatch.py` ยัง refuse ทุกครั้งเหมือนเดิม ทั้งสองช่องว่าง
  (vehicle-bind payload, scene-17 spawn) ยังต้องใช้ attended capture เท่านั้น การปิด RE-096/RE-103 เป็น
  bounded-negative คือ "เพดาน static ถึงที่สุดแล้ว" ไม่ใช่ "ปัญหาใกล้แก้"
- **ไม่ได้ปิดหัวใบ `RE-103`** — เป็นของ chief cloud (รอบ `4txjyg`) เท่านั้น ธงเตือนไว้ที่นี่ให้ chief ปิด
- **ไม่ได้ตัดสินใจแทนเจ้าของ/COO เรื่องอะไรใหม่** — ทุกอย่างในรอบนี้เป็นการ consume ผลที่ปิดแล้ว + แก้บั๊ก
  เอกสาร + เติมข้อมูลที่วัดไว้แล้วให้ครบ schema
- **ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ได้แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py`

— สาย A · WORLD

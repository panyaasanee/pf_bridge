# A_20260828_0931 (z851j4) -- RE-123 RESULT consumed (Mirage Reel = n_ID 230, hard guard),
formalized as 4 new enforced tests in pirate-force-server, M2/sea-travel escalated to
COO instead of started (owner's specific pause decision vs. general addendum conflict)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีอะไรเปลี่ยนบนจอวันนี้ -- ยังไม่เห็น NPC "Mirage reel" ที่หน้าเต็นท์ Mo Yuzi (RE-123 ปิด identity ได้แล้ว
ว่าเป็น `n_ID=230` แต่ `BUILD_IMPACT: hard guard` เพราะไม่มี XYZ/visibility policy จริงในคลัง static -- ใบ
สั่งห้ามเพิ่ม static row ตรง ๆ) สิ่งที่เปลี่ยนคือของที่ไม่เห็นบนจอ: มี unit test ใหม่ 4 ตัวป้องกันไม่ให้รอบถัดไป
เผลอเพิ่ม NPC ตัวนี้ด้วยพิกัดที่แต่งขึ้น (เช่น ยืมพิกัดของ Mo Yuzi) ก่อนจะมีหลักฐานจริง

## Protocol A / มือถือล็อก

`pirate-force-server` HEAD `98307ae` (merge #186 เข้า `main`), `pf_bridge` HEAD `7b325c7` (merge #289
เข้า `main`) -- ทั้งคู่สะอาดจาก clone สดรอบนี้ ไม่มี PR `[LANE-A]` ค้างเปิดในทั้งสอง repo (grep/list ก่อน
เริ่มงาน)

## Protocol B: กล่องจดหมาย -- พบ 1 ใบใหม่ที่ต้องบริโภค

grep ใบทั้งหมดที่ `ถึง:` ระบุ `LANE-A` ตรง ๆ ใน `notes_to_chief/` (ไม่รวม `consumed/`) เทียบกับรอบก่อนหน้า
(`of27sx`, จดหมายล่าสุดของสาย A เอง คือ `20260828_0833`): พบ
`20260828_0913_RE-123-RESULT-NID230-SERVER-OWNED-XYZ-UNPROVEN.md` (ถึง chief cloud · LANE-A (WORLD) · COO)
เป็นใบใหม่ที่ยังไม่มี `.CONSUMED.txt` -- นี่คือผลของ `RE-123` ที่สาย A เองเปิดไว้รอบก่อน

ใบอื่นที่ timestamp ใหม่กว่า (`0844`/`0845` COO-DECISION, `0846` LANE-B-STATUS, `0912` CHIEF-REPLY, `0920`
LANE-GM-ASK-COO, `0921` CHIEF-ASK-COO) อ่านหมดแล้ว -- ทุกใบระบุ "ทุกสาย"/"cc" แบบประกาศกว้าง ไม่มีบรรทัด
action ผูกสาย A โดยตรง และ `0912`/`0921` (CORE-REQUEST-027 ชื่อตัวละคร) เขียนไว้เองว่า "ไม่กระทบเขตเขียน
ใคร" -- ไม่ต้องมี `.CONSUMED.txt`

## บริโภค RE-123 RESULT

ผลใบ: identity = `MOBS/TIP n_ID=230` (named-field crosswalk quest 51/926 scene 2, T1) แต่ placement TSV
ทุกฉากไม่มี template 230 เลย (T2) และ client Lua/`Player.MobAppear` เป็น stub no-op (T3) ⇒ actor ต้องมา
จาก server-owned population แต่ไม่มี XYZ/policy ในคลัง ⇒ `BUILD_IMPACT: ไม่มี source patch -- hard guard`

ทำตามคำสั่งตรง ๆ: ไม่เพิ่ม static row 230, ไม่ยืมพิกัด Mo Yuzi (n_ID 39) แทนที่จะปล่อยเป็นแค่ finding
ในจดหมาย formalize เป็น enforced test (แนวเดียวกับที่สาย B ทำกับ `RE-122`): เพิ่มคลาส
`MirageReelRe123GuardTests` (4 tests) ใน `tests/test_scene2_prison_exile_tables.py`:
1. `230` ไม่อยู่ใน `KNOWN_PLACEMENTS`
2. `230` ไม่อยู่ใน `UNRESOLVED_PLACEMENTS` เลย (ไม่มีแถวเลย ไม่ใช่แค่ unresolved)
3. loader (`load_known_placements`'s n_id range `1..41` ที่มีอยู่แล้ว) จะ refuse ถ้ามีใครเผลอเพิ่ม 230 จริง
   -- ยืนยันด้วยเทสตรง ไม่ใช่แค่สมมติว่า guard เดิมครอบ
4. ไม่มีแถวไหนที่ n_id=230 ใช้พิกัดเดียวกับ Mo Yuzi

ไม่แตะ production code ของ `scene2_prison_exile_tables.py` เลย (สอดคล้องกับ `BUILD_IMPACT_NONE`)

## เทส (รอบนี้)

`python3 -m unittest tests.test_scene2_prison_exile_tables -v`: **21 passed** (เดิม 17 + ใหม่ 4), 0 failed

`python3 -m unittest discover -s tests -p "test_*.py"`: **3874 ran**, 0 failed, 208 skipped (ปักหมุดแล้ว
ทุกตัว), 18 errors -- ทั้งหมดเป็น `ModuleNotFoundError` ของ `capstone`/`pefile`/`pytest` (ไม่มีในแซนด์บ็อกซ์
นี้ ยืนยันด้วย grep traceback ตรงชื่อ 3 แพ็กเกจนี้เท่านั้น ไม่ใช่ FAIL, ไม่เกี่ยวกับการแก้รอบนี้)

## CLIENT_RE_QUEUE.md

ปิดหัวใบ `RE-123` เป็น `CLOSED MIXED-POSITIVE-BOUNDED` พร้อมสรุปผลและสิ่งที่สาย A ทำ (บล็อกใหม่ต่อท้ายหัว
ใบเดิม แนวเดียวกับ `RE-116`/`RE-119`) ไม่ลบ/ไม่ย้าย/ไม่แก้ถ้อยคำเดิมของใบ

## M2/sea-travel -- ไม่เริ่ม, เปิด ASK-COO แทน

addendum บอกให้สาย A ทำ M2 ระหว่างรอ RE เรื่อง Columbus แต่ `PANYA-DECISION 2026-08-27 20:10` สั่งพัก M2
ตรง ๆ เพื่อโฟกัส M1/identity-first คำสั่งเจาะจง+ใหม่กว่า+จากเจ้าของตรงกว่าชนะคำสั่งทั่วไป และนี่เข้าเงื่อนไข
escalation ของโปรเจกต์เอง ("ขัดกับคำสั่งที่เจ้าของเคาะเอง") -- ไม่ตัดสินเอง เขียนใบ
`notes_to_chief/20260828_0932_LANE-A-ASK-COO-m2-pause-vs-addendum-conflict.md` แทน เลือกคงคำสั่งพักไว้
เป็น default (ไม่มีอะไรต้องย้อนถ้าเลือกผิด เพราะไม่ได้เริ่มโค้ด M2 ใด ๆ รอบนี้)

## pf-adversary (manual pass -- ไล่ตรวจ claim ทุกอันในจดหมาย/ไฟล์รอบนี้)

- Stale pins: SHA/ตัวเลขทั้งหมดที่อ้างในจดหมายบริโภค RE-123 คัดลอกตรงจากใบ RESULT เอง (ไม่ได้เดา/จำผิด) --
  เช็คด้วย grep ตรงกับเนื้อใบ
- Unlabeled proposal vs measurement: "21 passed"/"3874 ran" มาจากการรันเทสจริงรอบนี้ ไม่ใช่คำยืนยันเฉย ๆ
- Guessed row: guard test #3 ไม่เดาว่า loader refuse -- รันจริงด้วย `assertRaises` เห็น
  `Scene2TableError` จริง
- Scope creep: ไม่แตะ production code ของโมดูล, ไม่แตะ M2, ไม่แตะ `runtime.py`/`app.py`
- cp874: ไฟล์ที่แตะทั้งหมด (โค้ด/เทสภาษาอังกฤษล้วน, จดหมายภาษาไทยมาตรฐาน) ไม่มีอักขระนอก cp874 ใหม่
- No defects found requiring a fix before push.

## Files touched

**pirate-force-server**: `tests/test_scene2_prison_exile_tables.py` (เพิ่มคลาส `MirageReelRe123GuardTests`,
4 tests ใหม่ -- ไม่แตะ production code) -- รวม 1 ไฟล์

**pf_bridge** (repo นี้): `CLIENT_RE_QUEUE.md` (ปิดหัวใบ `RE-123`),
`notes_to_chief/20260828_0913_RE-123-RESULT-NID230-SERVER-OWNED-XYZ-UNPROVEN.md.CONSUMED.txt` (stub ใหม่),
`notes_to_chief/consumed/20260828_0913_RE-123-RESULT-NID230-SERVER-OWNED-XYZ-UNPROVEN.md` (สำเนา),
`notes_to_chief/20260828_0931_LANE-A-STATUS-re123-result-consumed-guard-test-added-m2-conflict-escalated.md`
(ใบสถานะรอบนี้), `notes_to_chief/20260828_0932_LANE-A-ASK-COO-m2-pause-vs-addendum-conflict.md` (ใบขอ COO),
`rounds/A_20260828_0931_z851j4_*.md` (ไฟล์นี้เอง) -- รวม 6 ไฟล์ (ไม่นับสำเนาต้นฉบับที่ไม่ถูกแก้)

## ยังไม่ได้พิสูจน์

- ใบ ASK-COO เรื่อง M2 pause vs addendum ยังไม่มีคำตอบจาก COO/เจ้าของ -- รอบหน้าจะเดินตามคำตอบ
- RE-123's guard test ป้องกันได้แค่การเพิ่มแบบ manual ใน `KNOWN_PLACEMENTS`/`UNRESOLVED_PLACEMENTS` โดยตรง
  ไม่ได้ป้องกันเส้นทางอื่นที่ยังไม่มีในโค้ด (เช่นถ้าในอนาคตมี tool ที่ generate roster จากไฟล์อื่น)
- G-OBS: ไม่มีมนุษย์กดจอยืนยันรอบนี้ -- นี่คือรอบ verify+guard เท่านั้น

## CORE-REQUEST

None opened this round.

## เปิดใบให้สาย C

None opened this round (RE-123 ปิดแล้ว ไม่มีใบใหม่)

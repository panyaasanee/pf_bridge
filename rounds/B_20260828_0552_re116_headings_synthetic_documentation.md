# round `B_20260828_0552` (`db07x9`) - lane B - COMBAT -- consume RE-116, document HEADINGS as synthetic

**opened:** 2026-08-28 05:37 (+07:00) - **closed:** 2026-08-28 ~05:5x (+07:00)
**branches:** `claude/admiring-galileo-db07x9` (pirate-force-server) -
`claude/friendly-ride-db07x9` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่เห็นอะไรต่างบนจอ -- รอบนี้ไม่ใช่การเปลี่ยนพฤติกรรมที่ส่งจริง
(ทิศหันหน้าของมอนยังเป็นค่าวนสี่ทิศเดิมทุกอย่าง) เป็นการปิดคำถามว่า "ทิศหันหน้านี้มาจากข้อมูลจริงหรือ
เราคิดเอง" ด้วยหลักฐานสอง static evidence และเขียนคำตอบ (ไม่ใช่ค่าใหม่) ลงในโค้ดเอง เพื่อไม่ให้รอบถัดไป
อ้างผิดว่ามันคือของที่ recover มาจากไคลเอนต์

## 1 ล็อกต้นรอบ

รับข้อมูลจาก orchestrator แล้ว (ตรวจสดไปแล้วโดยผู้เรียก): ไม่มี PR `[LANE-B]` เปิดค้างทั้งสองรีโป
(มีแค่ `[LANE-GM] WIP round claim i76is0` ซึ่งไม่ใช่ล็อกของสายนี้) รอบ LANE-B ล่าสุด (`2pnu4l`,
pf_bridge#272 + pirate-force-server#174) merged=true จริงทั้งคู่ -- ไม่ต้องกู้คืนอะไร

## 2 บริโภคจดหมาย: RE-116 NPC-SPAWN-HEADING-SOURCE-001

`notes_to_chief/20260828_0516_RE-116-RESULT-MOVEMENTATTR-IS-SPAWN-HEADING-SOURCE.md`
(addressed ถึง LANE-A/LANE-B/COO ยังไม่มี `.CONSUMED.txt`)

**ผลของใบ (DONE / PASS static-only, ปิด T0-T4):**

- T1: recursive CFG ปักหมุด CNetNPC initial-apply อ่าน `MovementAttr+0x34` ตรงๆ ที่
  `0x0045D34F/0x0045D355` -- นี่คือ**แหล่งจริง**ที่ client ใช้ตอน spawn ไม่ใช่จุด wire-merge ที่เคยพิสูจน์
  แล้ว
- T4: reconcile `0x0043BB80` (arg-copier เปล่า, slot-semantic mismatch ใน `external/`) กับ
  `0x004671C0` (`MovementAttr::Serial` ตัวจริง) -- ไม่ใช่ class ชนกัน มี `MovementAttr` เดียว
- T2 (native `.npc` loader chain) และ T3 (`CONSTDATA_TH__MARKER.n_DIRTECTION` named-xref) เป็น
  **bounded negative ทั้งคู่**: ไม่พบ byte/field ใดใน raw placement record หรือ MARKER ที่ feed
  ค่า heading ต่อ-placement เข้า CNetNPC spawn path -- MARKER's consumer เดียวที่พบคือ teleport/
  scene-entry ของผู้เล่น ไม่ใช่ NPC placement

**การตัดสินใจ (ตามกฎข้อ ก/ข ของรอบนี้):** ใบนี้ **ไม่พอ**จะ wire ค่า heading ต่อ-placement ที่แท้จริงได้ --
ทาง**กลไก** wire ที่ `field_mobs.hostile_actor_entry` ใช้อยู่แล้ว (`legacy.make_remote_movement_attr`
mask `0x02`, object `+0x34`) **ถูกต้องตรงกับที่ RE-116 พิสูจน์แล้ว** ไม่ต้องแก้อะไรตรงนั้น แต่ไม่มีข้อมูล
ต่อ-placement จริงให้ใส่แทนค่าวนสี่ทิศ (`HEADINGS = (0, pi/2, pi, 3pi/2)`) ดังนั้น**ไม่เดา ไม่ประดิษฐ์ค่า
per-placement ใหม่** -- ทำสิ่งที่ BUILD_IMPACT ของใบขอไว้ตรงๆ แทน: เขียนลงโค้ดให้ชัดว่าค่าที่ส่งอยู่นี้เป็น
**synthetic cosmetic policy ของโปรเจกต์เอง** ไม่ใช่ข้อมูล recover จากไคลเอนต์/gamedata

## 3 ของที่สร้าง (pirate-force-server)

- `src/pirateforce_foundation/field_mobs.py`:
  - เพิ่มคอมเมนต์ยาวเหนือค่าคงที่ `HEADINGS` อธิบาย provenance เต็ม (กลไก wire ถูกต้อง, T2/T3 bounded
    negative, ค่าที่ใช้เป็นของเราเอง) อ้าง RE-116 ตรงตัว
  - เพิ่ม bullet ใหม่ใน `pin_document()`'s `nonclaims` list ระบุเรื่องเดียวกัน (ตอนนี้มี 8 bullets, เทส
    เดิมเช็คแค่ `>= 6` จึงไม่พัง)
- `scenarios/field_mobs_hostile_001.json`: regenerate สดจาก `field_mobs.pin_document(legacy)` จริง
  (ไม่พิมพ์ค่าเอง) diff เหลือแค่ nonclaims bullet ใหม่ตัวเดียว

ไม่แตะกลไก wire ใดๆ (`legacy.make_remote_movement_attr`/`FULL_MOVEMENT_MASK`/mask bit `0x02`) เพราะ
RE-116 ยืนยันว่าถูกอยู่แล้ว ไม่แตะ `world_population.py`/`world_population_bg0002.py` (มี round-robin
เดียวกันแต่เป็นเขตสาย A) ไม่แตะ `current/pf_login_game_server_v141.py`

## 4 เทส

`python3 -m unittest tests.test_field_mobs tests.test_mob_death tests.test_mob_combat -v`:
177 tests, ok

Full suite (`python3 -m unittest discover -s tests -p "test_*.py"`, ติดตั้ง `capstone`/`pefile`/
`pytest` ในแซนด์บ็อกซ์รอบนี้เพื่อไม่ให้มี collection error แบบที่รอบก่อนๆ เจอ): **4048 tests, 3721
passed, 327 skipped, 0 failed, 0 errors**

## 5 pf-adversary self-check (ทำเอง, ไม่มี agent แยกให้เรียกรอบนี้)

ตรวจ:
- ค่า `HEADINGS` เอง**ไม่ได้เปลี่ยน** (ยังเป็น `(0, pi/2, pi, 3pi/2)` เดิมทุกบิต) -- ยืนยันด้วย diff:
  บรรทัดเดียวที่เปลี่ยนคือคอมเมนต์เหนือมัน ไม่ใช่ตัวค่า เพื่อไม่ให้เป็นการ "แอบเปลี่ยนพฤติกรรม" ปนกับ
  "แค่เพิ่มเอกสาร"
- คอมเมนต์ใหม่ไม่ claim อะไรเกินกว่าที่ RE-116 พิสูจน์จริง (อ่านทวนกับใบต้นฉบับ T1-T4 คำต่อคำก่อนเขียน)
  ไม่บอกว่า "ทิศทางถูกต้องแล้ว" (มันไม่ถูก มันแค่คอสเมติก) ไม่บอกว่า "ไม่มีทางหาข้อมูลจริงได้อีกแล้ว"
  (แค่บอกว่าวันนี้ยังไม่มี)
- `pin_document()`'s nonclaims bullet ใหม่ตรวจว่าไม่ทำให้ JSON ไม่ ASCII (ข้อความเป็นอังกฤษล้วน, เทส
  `raw.decode("ascii")` ผ่าน) และไม่ทำ `test_the_committed_pin_is_what_the_code_produces` พัง (ตรวจ
  ผ่านจริงหลัง regenerate)
- ค้นซ้ำว่ามีที่อื่นใน `src/` claim ว่า HEADINGS เป็นข้อมูลจริงหรือไม่ (grep `HEADINGS|heading` ทั้ง
  `field_mobs.py`/`mob_death.py`) -- ไม่พบ claim ผิดที่อื่น `mob_death.py` อ้าง `field_mobs.HEADINGS`
  ตรงๆ โดยไม่มีคอมเมนต์ซ้ำ (พึ่งเอกสารจาก `field_mobs.py` แหล่งเดียว ไม่ต้อง duplicate)
- ตรวจว่า `world_population.py`/`world_population_bg0002.py` (เขตสาย A) มี round-robin แบบเดียวกัน
  แต่**ไม่แตะ** -- อยู่นอกเขตเขียนของสาย B ตามกติกา แจ้งใน handback แทน
- รัน full test suite ก่อน/หลัง diff เทียบ -- ไม่มีเทสใหม่พัง ไม่มีเทสเดิมถูกลบ/ปิดเพื่อให้ผ่าน

ไม่พบปัญหาที่ต้องแก้เพิ่ม

## 6 ของที่หาแล้วแต่ไม่ทำต่อ (กฎข้อ 2)

กวาดหา TODO/FIXME ใน `mob_*.py`/`field_mobs.py`: ไม่พบ กวาด `GAME_TEST_QUEUE.md` หา GT ticket lane-B
ที่ยัง OPEN/BLOCKED: `GT-036` บล็อกอยู่ที่คำตัดสินของ Panya (นโยบาย, ไม่ใช่โค้ด) `GT-109`/`GT-120`
รอ wiring/attended capture ที่ไม่ใช่ของสายนี้ล้วนๆ หรือรออยู่แล้วตามที่บันทึกไว้ ไม่มีของใหม่ที่ self-
decidable ในเขตเขียนของสาย B รอบนี้นอกจาก RE-116

## 7 mailbox

- stub ใหม่: `notes_to_chief/20260828_0516_RE-116-RESULT-....md.CONSUMED.txt` + สำเนาต้นฉบับใน
  `notes_to_chief/consumed/` (ต้นฉบับไม่ถูกลบ)
- `CLIENT_RE_QUEUE.md`: หัวใบ `RE-116` ปิด `CLOSED PASS/DONE` พร้อมสรุปผลและ `BUILD_IMPACT` ไว้ในใบ

## 8 write zone

`pirate-force-server`: `src/pirateforce_foundation/field_mobs.py`, `scenarios/field_mobs_hostile_001.json`.
`pf_bridge`: `notes_to_chief/` (stub + consumed copy), `rounds/`, `CLIENT_RE_QUEUE.md` (หัวใบ RE-116
เท่านั้น). ไม่แตะ `runtime.py`, `app.py`, `pf_login_game_server_v141.py`, `scenarios/world_*.json`,
`world_population*.py` เลยรอบนี้.

## CORE-REQUEST

none

## เปิดใบให้สาย C

none -- RE-116 ปิด bounded negative แล้ว ไม่มีเบาะแสใหม่ที่ควรเปิดใบต่อ

## 9 จบรอบ -- push แล้ว รอ merge

pf-adversary จริง (subagent แยก, orchestrator เป็นผู้เรียก) รันบน diff ที่ push แล้ว: **ไม่พบข้อบกพร่อง**
ตรวจครบ 5 จุด (ขอบเขต diff เทียบ merge-base จริง, JSON pin มาจาก `pin_document()` จริงไม่ใช่ hand-edit,
คอมเมนต์ตรงกับใบ RE-116 ต้นฉบับทีละจุดไม่ overclaim, mailbox mechanics ฝั่ง pf_bridge ถูกต้อง ต้นฉบับไม่ถูก
ลบ, ไม่แตะไฟล์นอกเขต) -- push แล้ว เอา draft ออกแล้ว รอ merge:

- `pf_bridge#276` (`claude/friendly-ride-db07x9` @ `4379ed0`)
- `pirate-force-server#178` (`claude/admiring-galileo-db07x9` @ `f9923da`)

ยังไม่ merge ณ เวลาปิดรอบนี้ -- รอบถัดไปต้องตรวจ `pull_request_read` method `get` ยืนยัน `merged=true`
จริงก่อนถือว่างานอยู่บน `main` (ตามข้อ A ของ ADDENDUM v2) ห้ามเชื่อไฟล์นี้เฉยๆ ว่า "เสร็จ"

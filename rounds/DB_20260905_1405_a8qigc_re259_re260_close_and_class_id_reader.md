# DB round (`a8qigc`) -- 2026-09-05T14:05+07:00 -> 2026-09-05T14:55+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- อ่าน `NOW.md` ล่าสุดก่อนอื่น (ตรวจล่าสุด 13:53 โดย COO). ไม่มีบรรทัดในหัวข้อ "งาน
ด่วนตอนนี้" ที่รอบนี้แตะได้ตรง ๆ (M4 หลักยังล็อกที่ `runtime.py:6443`/Door B ของ LANE-B เหมือนเดิม
-- CORE-REQUEST ของรอบก่อนยังไม่มีคำตอบ ไม่ใช่ของรอบนี้จะทวง) งานรอบนี้คือกล่องจดหมาย (RE-259/
RE-260 ที่รอบก่อนไม่ทันกรอกผล + LANE-B CORE-REQUEST ใหม่) ตามลำดับที่ไฟล์รอบก่อนทิ้งไว้ (ข้อ 0
ของ "รอบหน้าทำอะไร")

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยวข้อง -- รอบนี้ไม่แตะโลก/ฉากเลย (ตัวอ่านใหม่เป็น per-character
read ผ่าน `SQLiteStore`, ไม่มี world registry เข้ามาเกี่ยว)

## 1. ล็อกรอบ

- ⚠️ **process deviation, บันทึกตามจริง**: รอบนี้ตรวจ list `[LANE-DB]` open ครั้งแรก (ว่างเปล่าทั้ง
  สองรีโป) **ก่อน**เปิดกล่องจดหมาย/แตะโค้ด แต่เปิด claim **ช้ากว่าที่กติกาสั่ง** -- อ่านกล่องจดหมาย
  และเริ่มแก้ `store.py` ไปพักหนึ่งก่อนจึง commit/push ไฟล์ `_claim.md` (ไม่ใช่ก่อนแตะโค้ดจริง ๆ
  ตามที่ "ล็อกรอบ ... ทำก่อนอ่านกล่องจดหมายและก่อนแตะโค้ดทุกรอบ" สั่ง) list ซ้ำหลัง claim เปิดแล้ว
  ก็ยังว่างเปล่ายกเว้นใบของตัวเอง (`pf_bridge#1327`) ไม่มีการชนกับสายอื่นเกิดขึ้นจริง แต่ลำดับ
  ขั้นตอนไม่ตรงกติกา -- บันทึกไว้ตรง ๆ แทนการซ่อน ไม่ใช่การอ้างว่าไม่มีความเสี่ยง
- ตัดกิ่งจาก `origin/main` สดของทั้งสองรีโป -- กิ่งของเซสชันนี้เอง (`claude/brave-goodall-a8qigc`
  ของ `pirate-force-server`, `claude/admiring-johnson-a8qigc` ของ `pf_bridge`) อยู่ตรง
  `origin/main` พอดีตั้งแต่ต้น
- commit `rounds/DB_20260905_1405_a8qigc_claim.md` (สามบรรทัด) push แล้วเปิด
  `pf_bridge#1327 [LANE-DB] round a8qigc: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1327` ของผมเอง ⇒ ไม่แพ้
  ทำงานต่อ

## 2. กล่องจดหมาย

`grep` แบบไม่ยึดตำแหน่งหา `ADDRESSEE: LANE-DB` (และรูปแบบ sync-notice ที่จ่าหน้าในบรรทัดแรกของ
เนื้อหาแทน หัวไฟล์) บนไฟล์ที่ยังไม่มี `.CONSUMED.txt` คู่: เจอ**หนึ่งใบใหม่จริง**

1. `20260905_1353_LANE-B-CORE-REQUEST-store-read-for-a-characters-class-id.md` -- ขอตัวอ่าน
   `class_id` (consumed รอบนี้ -- ดูข้อ 3.2)

อ่านสามใบก่อตั้งสาย (`20260901_1059`/`1100`/`1101`/`1112`) ครบตามกติกา "รอบแรกของเซสชัน"
(เซสชันนี้ไม่มีความจำข้ามรอบ)

อ่านไฟล์รอบล่าสุด `DB_20260905_1333_j9wwc4_home_marker_and_gt221_recovery.md` -- ข้อ 0 ของ "รอบ
หน้าทำอะไร" ชี้ตรงไปที่สองใบผลลัพธ์ RE ที่รอบนั้นเจอตอนท้ายรอบ ไม่ทันกรอก:

2. `20260905_1323_RE-259-RESULT-UPDATEATTR-TARGETS-CMYACTOR-ONLY.md` -- ผลออกแล้ว รอ LANE-DB
   กรอก `### result:` (consumed รอบนี้ -- ดูข้อ 3.1)
3. `20260905_1327_RE-260-RESULT-CONCRETE-OWNER-BOUNDED-AT-GENERIC-ACTORATTR.md` -- เช่นเดียวกัน
   (consumed รอบนี้ -- ดูข้อ 3.1)

## 3. ทำอะไร

### 3.1 ปิดหัวใบ `RE-259`/`RE-260` (งานค้างจากรอบก่อน, ข้อ 0 ที่สั่งไว้)

ทั้งสองใบเป็น **bounded negative** ไม่ใช่ผลที่ปลดล็อกฟีเจอร์ผู้เล่น:

- `RE-259`: `UpdateAttrVital 0x309A` address เฉพาะ local `CMyActor` (player) ไม่ถึง `CNetNPC` เลย
  ⇒ **player-class only** ตัดกลุ่ม 1+2 (9 VA) ออกจากรายการค้างของ piece 3
  (`notes_to_chief/20260904_1748_LANE-DB-RE-TICKET-...`) ตาม redirect ของใบเอง -- **ไม่**แปลว่า
  ค่าเหล่านั้นถูกต้องสำหรับ `CMyActor` ตามที่ใบกำชับไว้ล่วงหน้า
- `RE-260`: concrete owner ของ `ActorAttr@0x99`/`@0x9A` พิสูจน์ไม่ได้จาก IMAGE นี้ ⇒ x=26/x=27
  **คงอยู่นอก** `RESEND_ADJUDICATED` ต่อไปตามเดิม (ตรวจแล้ว:
  `persistence_attr_compose.py:420` ยังว่างเปล่า ก่อนใบนี้ก็ไม่มีสองเลขนี้อยู่แล้ว ผลนี้ยืนยัน
  สถานะเดิม ไม่ได้เปลี่ยนอะไรในโค้ด)

ทั้งสองใบ: กรอก `### result:` ในไฟล์ผลลัพธ์เอง + เขียน `NO_FEATURE_WAITING: <เหตุผล>` ตามกติกา
(`PANYA-DECISION 20260905_1130`) เพราะไม่มีฟีเจอร์ผู้เล่นใหม่ให้เปิดใบสร้าง/GT `CLIENT_RE_QUEUE.md`
เป็นไฟล์ของ chief (นอกเขตเขียนของ DB) เลยส่ง CORE-REQUEST แยก
(`20260905_1425_LANE-DB-CORE-REQUEST-close-re259-re260-headers-in-client-re-queue.md`) ระบุ
ถ้อยคำหัวใบที่ขอให้ chief แก้ตรง ๆ แทน

### 3.2 ตัวอ่าน `class_id` -- `SQLiteStore.read_class_id_by_identity` (LANE-B CORE-REQUEST)

`store.py` (ข้าง ๆ `write_speed_by_identity`, method ใหม่เท่านั้น ไม่แตะของเดิม): อ่านอย่างเดียว
`identity_lo`/`identity_hi` → `class_id` หรือ `None` -- `None` ครอบคลุมทุกกรณีที่ไม่มีค่าซื่อสัตย์
(identity ไม่พบ/สอง active row/ผิดชนิด-ช่วง, soft-deleted, NULL จริง, schema ก่อน migration 006,
**และฐานข้อมูลที่แตะไม่ถึงเลย** -- ดูย่อหน้าถัดไป) ไม่มีการเดาเป็น 0 หรือคลาสไหน ไม่ยกระดับเป็น
resolver ใหม่ ตามข้อจำกัดที่จดหมายขอ

**`pf-adversary` (เรียกพร้อมเริ่มงาน 3.2 ตามกติกา `COO 0903_2345`/`1428`) รอบแรก**: พบข้อบกพร่อง
จริง -- ร่างแรกครอบเฉพาะ guard ของ identity part ด้วย `try/except` ปล่อยให้ `with self.connect()`
และการอ่านข้างในราวข้ามขอบเขตได้ (เช่น `sqlite3.DatabaseError` เมื่อไฟล์ฐานข้อมูลเสีย) ต่างจาก
`write_speed_by_identity` ที่ครอบทั้งฟังก์ชันไว้ในหนึ่ง `try` พิสูจน์จริงด้วยการเขียนไบต์ขยะทับไฟล์
ฐานข้อมูล: `write_speed_by_identity` คืน `None` (ถูก) แต่ตัวอ่านใหม่ raise ตรง ๆ (ผิด) **แก้แล้ว**:
ย้ายทั้งฟังก์ชันเข้า `try/except Exception: return None` เดียว ให้ทรงเดียวกับ
`write_speed_by_identity` เป๊ะ พร้อมเทสใหม่ `DatabaseCannotBeReachedTests` ที่ปักการแก้ไว้ (ยืนยัน
ทั้งสองประตูตอบ `None` เหมือนกันสำหรับไฟล์เดียวกันที่เสีย) และเทสรอบที่สอง
`test_a_class_id_written_through_the_real_writer_comes_back_unchanged` ที่ round-trip ผ่าน
`write_typed_attributes` จริง (ไม่ใช่แค่ raw SQL helper ที่ไฟล์นี้ใช้ seed แถวที่เหลือ) แก้ตาม
finding ที่สองของรอบแรก (docstring อ้างว่า round-trip ผ่าน production writer ทั้งที่ยังไม่มีเทส
ยืนยัน)

**`pf-adversary` รอบที่สอง (ตัวแก้)**: ยืนยันการแก้ถูกต้องและครบ (reproduce ซ้ำ, ตรวจว่าไม่มี
`KeyboardInterrupt`/`SystemExit` หลุดเข้า `except`, ตรวจว่า `connect()`'s `finally: db.close()` ยัง
ปิด connection แม้ raise กลางทาง = ไม่มี resource leak) รันเทสไฟล์ + `test_store_speed_by_identity.py`
เต็ม = เขียว ไม่พบข้อบกพร่องใหม่ ไม่ใช้ `ADVERSARY_PENDING`

### 3.3 ค้นพบข้างเคียง (ไม่แก้ นอกเขต): `test_combat_pose.py::SourcePinTests` แดงเมื่อมี `pf_bridge`
ข้าง ๆ

ชุดเต็มรอบแรก (หลัง merge `origin/main`) แดง 1 เคส -- ตรวจแล้วไม่ใช่ของรอบนี้: `git diff --stat
origin/main` ของกิ่งนี้แตะแค่ `store.py` + ไฟล์เทสใหม่ตัวเดียว, ต้นเหตุคือ
`tools/pf_equip_attack_behavior_extract.py` หายจาก `origin/main` ทั้งที่ `test_combat_pose.py`
(LANE-B, `#827`, merge ก่อนรอบนี้เริ่ม) เรียกมันเมื่อ `pf_bridge/gamedata` อยู่ข้าง ๆ จริง (เซสชันนี้
มี) `tools/` เป็นเขตเขียนของ chief ไม่ใช่ของ DB -- ส่งเป็น SYNC-NOTICE
(`20260905_1450_LANE-DB-SYNC-NOTICE-combat-pose-source-pin-test-fails-with-pf-bridge-alongside.md`)
ไม่แก้เอง ไม่บล็อกการ push ของรอบนี้

### 3.4 จดหมายที่ส่ง (รอบเดียว)

1. `20260905_1425_LANE-DB-CORE-REQUEST-close-re259-re260-headers-in-client-re-queue.md`
   (ADDRESSEE: chief, cc COO)
2. `20260905_1430_LANE-DB-REPLY-class-id-reader-built-read-class-id-by-identity.md`
   (ADDRESSEE: LANE-B, cc chief/COO)
3. `20260905_1450_LANE-DB-SYNC-NOTICE-combat-pose-source-pin-test-fails-with-pf-bridge-alongside.md`
   (ADDRESSEE: chief, cc COO/LANE-B)
4. `### result:` กรอกในไฟล์ `RE-259`/`RE-260` เอง (ไม่ใช่จดหมายแยก ตามที่ใบขอ) + stub
   `.CONSUMED.txt` สามใบ (`1353`, `1323`, `1327`)

## 4. ชุดเทสของรอบ

ระหว่างทำ: `pytest tests/test_store_read_class_id_by_identity.py tests/test_store_speed_by_identity.py -q`
หลายครั้งระหว่างแก้ (ไฟล์สุดท้าย 51 passed / 33 subtests passed) ไม่รันชุดเต็มระหว่างทาง

ชุดเต็ม **หนึ่งครั้งในรอบนี้** บนต้นไม้ที่ merge `origin/main` แล้ว (หลังผล adversary รอบสองกลับมา
ว่าไม่พบข้อบกพร่องใหม่), commit สุดท้ายจริงที่ push:
**1 failed, 10973 passed, 323 skipped, 20293 subtests passed (414.13s)** -- ตัวที่แดงคือ
`tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_the_shipped_tables_when_it_can_run`
ตรวจแล้วไม่ใช่ regression ของรอบนี้ (ดู §3.3) เป็นความล้มเหลวที่มีอยู่ก่อนแล้วบน `origin/main`
เอง ไม่ใช่ไฟล์ที่รอบนี้แตะ

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable

**ศูนย์** -- รอบนี้เป็นประตูอ่านฝั่งเซิร์ฟเวอร์ (store method ใหม่) ไม่มีจุดเรียกจริงในโปรดักชัน
จนกว่า LANE-B จะเสียบเข้า `combat_pose.py`/caller ของตัวเอง ไม่มีอะไรถึงจอผู้เล่นเองในรอบนี้ ผล
`RE-259`/`RE-260` เองก็เป็น static-image ล้วน ไม่มีจอเกี่ยวข้อง

### 5.2 wire-DB

`pirate-force-server#830` (`claude/brave-goodall-a8qigc`) -- **เปิดแล้ว 14:5x+07 พร้อม
`PF-AUTOMERGE: v4` รอเกต Windows** (สถานะ ณ ตอนเขียนไฟล์นี้ ยังไม่เห็นผล `merged: true`) หนึ่งคอมมิต
ผ่านชุดเต็มตาม §4 · `pf_bridge#1327` claim -- เติม marker ทันทีหลังไฟล์นี้ + จดหมาย + stub ขึ้น
กิ่งเดียวกัน (ข้อ 7)

## 6. nonclaims

1. **ไม่อ้างว่า `pirate-force-server#830` ขึ้น main แล้ว** -- เปิดรอเกต ตามกฎ §22 (`1158`) ต้องอ่าน
   ผล job `gate` ของรอบ `pull_request` เอง แต่รอบนี้จบก่อนเกตรันเสร็จ (เขียนตามจริง ไม่รอ)
2. **ไม่อ้างว่ามีจุดเรียก `read_class_id_by_identity` ในโปรดักชัน** -- ประตูพร้อมแล้ว แต่ LANE-B
   ยังไม่ได้เสียบ (จดหมายของ LANE-B เองบอกไว้ว่า "ไม่บล็อกอะไรของ DB")
3. **ไม่อ้างว่าผล `RE-259`/`RE-260` ปลดล็อกฟีเจอร์ผู้เล่นใหม่** -- ทั้งคู่เป็น bounded negative
   ตามที่ `NO_FEATURE_WAITING` ในหัวใบระบุตรง ๆ `compose_full_block` ยังบล็อกด้วยเหตุผลเดิมทั้งหมด
4. **ไม่อ้างว่า `CLIENT_RE_QUEUE.md` แก้แล้ว** -- ไฟล์นั้นเป็นของ chief ส่ง CORE-REQUEST ให้แก้
   หัวใบแทน ยังไม่เห็นผล ณ ตอนเขียนไฟล์นี้
5. **ไม่อ้างว่า `test_combat_pose.py::SourcePinTests` เป็นของรอบนี้แก้แล้ว** -- ส่งแจ้งเหตุอย่าง
   เดียว (§3.3) ไม่แตะไฟล์นั้นเลย นอกเขตเขียนของ DB
6. **ไม่อ้างว่า `1101` (M4 หลัก, HP/เลเวล) ปลดล็อกแล้ว** -- ยังล็อกที่ `runtime.py:6443`/Door B
   ของ LANE-B เหมือนเดิม CORE-REQUEST ของรอบก่อน (`home marker`, `1311`) ยังไม่มีคำตอบ ไม่ใช่
   เรื่องเดียวกับ class_id reader
7. **ไม่แตะ `store.py` ของเดิม (เฉพาะเพิ่ม method ใหม่), `runtime.py`, `columbus_quest_dispatch.py`,
   `app.py`, `tools/`, `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, `current/pf_login_game_server_v141.py`**
   -- ไฟล์ที่แก้จริงคือ `store.py` (เพิ่ม method) + เทสใหม่หนึ่งไฟล์ + จดหมาย/stub ฝั่ง `pf_bridge`
8. **ไม่ปิดบัง process deviation ของล็อกรอบ** -- บันทึกไว้ตรง ๆ ใน §1 (claim เปิดช้ากว่าที่กติกาสั่ง
   แม้ตรวจ list ก่อนแตะโค้ดจริง และไม่มีการชนกันเกิดขึ้น)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ **และทำตามลำดับ "ล็อกรอบก่อนอ่านกล่องจดหมาย/แตะโค้ด" ให้ตรง
   กติกาจริง ๆ** -- ไม่ใช่แค่ตรวจ list ก่อน แต่ commit+push+เปิด claim PR ก่อนอ่านจดหมายซี่ 2
   ของรอบนี้ทำผิดลำดับ (§1) แม้ผลจะไม่มีการชนกันจริง
2. ตรวจผลเกตของ `pirate-force-server#830` ก่อนอื่น -- ถ้าแดง แก้ในรอบนั้นทันที
3. ตรวจว่า chief รับ CORE-REQUEST ปิดหัวใบ `RE-259`/`RE-260` (`1425`) หรือยัง (ไม่บล็อกใคร)
4. ตรวจว่า chief/LANE-A รับ CORE-REQUEST home-marker hookup ของรอบ `j9wwc4` (`1311`) หรือยัง --
   ค้างมาสองรอบแล้ว ยังไม่เกิน deadline ปกติของสาย แต่ใกล้เวลาที่ควรทวงถ้ารอบหน้ายังไม่มีคำตอบ
5. ตรวจว่า LANE-B ตอบรับ `read_class_id_by_identity` (`1430`) หรือยัง (ไม่บล็อกใคร)
6. ไม่มีใบใหม่ถึง LANE-DB รอบหน้า: กลับไปหาใบ chief/COO ที่ cc ถึง LANE-DB ย้อน 12 ชม. ก่อนประกาศ
   "ไม่มีงาน" หรือหยิบคิว "COO-ORDER 0329" ชิ้น 3/4/5 ที่ยังไม่ปิด (piece 3 = `0x309A` full block,
   ยังบล็อกด้วยเหตุผลเดิมทุกข้อ; piece 4/5 -- ตรวจสถานะจริงจากจดหมายล่าสุดก่อนอ้างว่ายังเปิดอยู่)
7. มาร์กกล่องจดหมายด้วย unanchored grep เสมอทั้งสองแบบ (`ADDRESSEE:` หัวไฟล์ และจ่าหน้าในบรรทัด
   แรกของเนื้อหาแบบ sync-notice)

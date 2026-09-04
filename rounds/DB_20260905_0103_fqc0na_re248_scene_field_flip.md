# DB round (`fqc0na`) -- 2026-09-05T01:03+07:00 -> 2026-09-05T01:23+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับขั้น M** (M2 คงเดิม -- นี่คือหนี้ภายในสายของ "รอเครื่องคุณ" ข้อ 2 หน้าเลือกตัวแสดงฉากจริง, ไม่ใช่
milestone gate) แต่ปลดตัวบล็อกเดียวที่ค้างของ item นั้น: `SCENE_FIELD` ยังเป็น `None` เพราะรอผล RE ใบแคบ
ตอนนี้ RE-248 ตอบแล้ว (`FIELD_A` = scene) และ PR ขึ้นแล้ว (รอ gate) ⇒ เมื่อ merge, `GT-245` (`รอเครื่องคุณ`
ข้อ 2) พร้อมบูตได้ ไม่มีตัวบล็อกโค้ดเหลือ -- การปลดล็อกให้บูตจริงเป็นหน้าที่ chief คัดกรองคิว (`2159`)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159` ไม่ใช่ DB)

## 1. ล็อกรอบ

- 01:03+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชันทั้งสองรีโป (`claude/gifted-wright-fqc0na` server, `claude/admiring-ride-fqc0na` bridge)
  ที่ระบบตั้งชื่อให้ reset ตรงที่ `origin/main` ก่อนเริ่ม (server 0 ahead/behind, bridge เช่นกัน)
- commit `rounds/DB_20260905_0103_fqc0na_claim.md` push แล้วเปิด `pf_bridge#1234 [LANE-DB] round
  fqc0na: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1234` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -q "ADDRESSEE: LANE-DB"` (unanchored) บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี
`.CONSUMED.txt` คู่ -- ใบเดียวค้าง:

1. `notes_to_chief/20260905_0053_RE-248-RESULT-FIELD-A-IS-SCENE-FIELD-B-IS-LEVEL.md` (RE runner local,
   00:53) -- ตอบด้วย §3.1

สร้าง stub `.CONSUMED.txt` แล้ว

chief ยังไม่ตอบใบ `2357` (class_id backfill one-line hookup, ค้างจากรอบ `suh0aq`) -- ตรวจแล้วไม่มีใบ
`CHIEF-TO-LANE-DB` ใหม่กว่า `0938` และ `grep` บน `app.py` สดยังว่างเปล่า -- ไม่ใช่งานของรอบนี้ (รอ chief)

## 3. ทำอะไร

### 3.1 RE-248 -- flip `SCENE_FIELD` จาก `None` เป็น `FIELD_A`

ใบ `0053` (static IMAGE trace, หกชิ้นหลักฐานปักตำแหน่งจาก codec write-order ถึงชื่อ widget UI ที่ผูกจริง
`LABEL_SCENE` / `NUMLABEL_CHARLV`) ตอบคำถามที่สแคฟโฟลด์รอบ `w7w30l` เปิดค้างไว้: `FIELD_A` (`+0x20`) คือ
ฟิลด์ scene ที่หน้าเลือกตัวใช้พิมพ์ชื่อแมพ, `FIELD_B` (`+0x22`) คือเลเวลตัวละคร (คนละฟิลด์ โมดูลนี้ไม่แตะ)
`BUILD_IMPACT` ของใบอนุญาตแค่การเปลี่ยนแปลงเดียว: flip `SCENE_FIELD` เป็น `FIELD_A`

แก้ตาม:
- `src/pirateforce_foundation/persistence_scene_field_patch.py`: `SCENE_FIELD = FIELD_A` (เดิม `None`)
  แก้ docstring ของโมดูลจาก "RESOLVED... That flip is the fix" เป็น **"FLIPPED, NOT YET CLOSED"**
  (เหตุผลดูหัวข้อ pf-adversary ด้านล่าง)
- `src/pirateforce_foundation/legacy_bridge.py`: แก้ **เฉพาะคอมเมนต์** ใน `LegacyProjector.character_list`
  ให้ตรงสถานะใหม่ (บรรทัดโค้ดไม่เปลี่ยนแม้แต่ตัวเดียว -- มีบรรทัดนี้เป็นของสายนี้อยู่แล้วจากรอบ `w7w30l`
  ที่เสียบจุดเรียกจริง จึงมีสิทธิ์แก้คอมเมนต์บรรทัดนี้ต่อ)
- `tests/test_persistence_scene_field_patch.py`: แก้เทสที่ยึดค่า default เดิม (`None`, เฟรม byte-identical
  เสมอ) ให้ยึดค่าที่ส่งจริงตอนนี้ (`FIELD_A`) แทน -- เทสตัวละครที่ย้ายฉากตอนนี้ต้องพิสูจน์ว่าเฟรมที่ส่งจริง
  พิมพ์ฉากปัจจุบัน ไม่ใช่ฉากเกิด, โดย `FIELD_B`/ไบต์อื่นทุกตัวต้องไม่เปลี่ยน

**`pf-adversary` เรียกครั้งที่ 1 (ต้นรอบ)**: พบข้อเดียว (MEDIUM, ยืนยันจริง) -- docstring เดิมเขียน
"RESOLVED"/"That flip is the fix" ซึ่งเกินจริงเทียบกับที่ RE-248 พิสูจน์จริง (ใบเองก็เขียน nonclaims ข้อ 3
ว่าไม่อ้างว่า IMAGE trace คือ client-observable -- ตัวพิสูจน์จริงคือ `GT-245` ซึ่งยังไม่ได้บูต) -- แก้โดยเขียน
ใหม่เป็น "FLIPPED, NOT YET CLOSED" ระบุชัดว่า flip นี้ "authorized และ shipped" ไม่ใช่ "confirmed correct
on a real screen" จนกว่า `GT-245` จะบูต + แก้คอมเมนต์ใน `legacy_bridge.py` ให้สอดคล้องกัน
ข้ออื่นทั้งหมด (7 ข้อ) ยืนยันว่าไม่ใช่บั๊ก: mutation-test สองแบบ (stomp ฟิลด์คู่, สลับ `FIELD_A`/`FIELD_B`)
ยืนยันเทสจับได้จริงไม่ใช่ผ่านลอย ๆ, `FIELD_B` ไม่ถูกแตะในทุก code path จริง (grep ยืนยัน), การเขียนคอมเมนต์
ใน `legacy_bridge.py` ไม่แตะโค้ด, และ **สร้าง fixture สองตัวละครจริงทดลอง** (ชื่อยาวไม่เท่ากัน ย้ายคนละฉาก)
ยืนยันว่า offset คำนวณถูกต่อคนเพราะ `project_actor_wire_for_list` เรียกทีละตัวก่อน join เฟรม -- แต่ชี้ว่า
**ชุดเทสที่ส่งไม่มีเทสหลายตัวละครเลย** เป็นช่องว่างจริง (ไม่ใช่บั๊ก แต่ควรมีเทส) ⇒ เพิ่ม
`test_two_characters_with_different_name_lengths_patch_independently` ตามที่ชี้

**`pf-adversary` เรียกครั้งที่ 2 (ตรวจตัวแก้)**: เรียกแล้วแต่ **ผลยังไม่คืนตอน push** -- ตามกติกา
(`COO 2345`/`1428`): push ตามเดิม ไม่ถือล็อก บันทึก `ADVERSARY_PENDING pirate-force-server#778` รอบหน้าหยิบ
ผลเป็นงานแรกก่อน claim ห้ามเขียนว่า "ผ่าน adversary" (รอบนี้เขียนแค่ว่าถูกเรียกและกำลังรอ)

## 4. ชุดเทสของรอบ

- ระหว่างทำงาน: `tests/test_persistence_scene_field_patch.py` (19 passed หลังแก้ครบ, รวมเทสใหม่) +
  `tests/test_player_name.py` + `tests/test_foundation.py` + `tests/test_delete_refresh_hypothesis.py`
  (34 passed, 1 skipped, 6 subtests -- ทั้งสี่ไฟล์นี้เรียก `character_list()` โดยตรง) เขียวทุกครั้งที่รัน
- ชุดเต็ม (ครั้งเดียวของรอบ, บน commit สุดท้าย `66f9802`, `git fetch origin main` ยืนยัน `origin/main` =
  `f2a62bf` เหมือนตอนเริ่มรอบ ไม่ต้อง rebase ซ้ำ): **10347 passed, 327 skipped, 19570 subtests passed,
  0 failed** ใน 402.30s -- ไม่มีเทสแดงเก่าค้างจากรอบก่อน

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ยังศูนย์** -- โค้ดยังไม่ merge (PR รอ gate) และแม้ merge แล้ว การพิสูจน์บนจอจริงเป็นหน้าที่ `GT-245`
(attended, ยังไม่บูต) ไม่ใช่ของรอบนี้ ไม่มีอะไรเปลี่ยนบนจอผู้เล่นจากรอบนี้

### 5.2 wire-DB
`pirate-force-server#778` เปิดแล้ว (`claude/gifted-wright-fqc0na` @ `66f9802`) พร้อม `PF-AUTOMERGE: v4`
🔴 **GATE_UNVERIFIED `#778`** -- push แล้วสอง check run `gate` ยัง `in_progress` ที่ ~2 นาทีหลัง push
ยังไม่ตัดสิน (ตามกติกา `PANYA-DECISION 1158` §22 รอบถัดไปเปิดด้วยการตรวจ PR นี้ก่อนอย่างอื่น)

### 5.3 addendum (ยังอยู่ในรอบเดียวกัน) -- ผล `pf-adversary` ครั้งที่ 2 กลับมาแล้ว

หลัง push #778 ผล `pf-adversary` ครั้งที่ 2 (ตรวจตัวแก้จากครั้งที่ 1) กลับมาระหว่างที่ยังทำรอบต่อ (เขียนไฟล์
รอบนี้/มาร์กจดหมาย): **GO** -- ตรวจ wording ใหม่เทียบกับใบ `0053` จริง (nonclaims ข้อ 3, `BUILD_IMPACT`) และ
สถานะ `GT-245` บน `GAME_TEST_QUEUE.md` ตรงกับที่ docstring อ้าง, mutation-test เทสสองตัวละครใหม่ด้วยการทำให้
`project_actor_wire_for_list` แคช offset ตัวแรกแล้วใช้ซ้ำ (บั๊กชนิดที่เทสนี้อ้างว่าจับได้) -- เทสแดงจริง ไม่ใช่
ผ่านลอย ๆ ยืนยัน `_preset()` helper ตรงกับ `tests/test_foundation.py:51-57` ทุกจุด ไม่พบข้อบกพร่องใหม่
**`ADVERSARY_PENDING #778` ในหัวข้อ §6 ข้อ 3 ปิดแล้ว -- ไม่ต้องมีตัวแก้เพิ่ม ไม่มี commit ใหม่ในรอบนี้**

## 6. nonclaims

1. **ไม่อ้างว่า `SCENE_FIELD = FIELD_A` ขึ้น `main` แล้ว** -- อยู่ใน PR `#778` ที่ยังรอ gate
2. **ไม่อ้างว่าหน้าเลือกตัวละครพิมพ์ฉากถูกต้องจริงบนจอแล้ว** -- นี่คือสิ่งที่ `GT-245` (attended) ต้องพิสูจน์
   โค้ดรอบนี้เป็นแค่การ "authorize + ship" ตามที่ `BUILD_IMPACT` ของ RE-248 สั่ง ไม่ใช่การปิดคำถาม
3. ~~ไม่อ้างว่า `pf-adversary` ผ่านครั้งที่สอง~~ -- **แก้ไข**: ผลกลับมาแล้วระหว่างรอบเดียวกัน (GO, ดู §5.3)
   ไม่ต้องรอรอบหน้า
4. **ไม่แตะ `runtime.py`, `app.py`, `lifecycle.py`, `current/pf_login_game_server_v141.py`,
   `characters.actor_wire` ในฐานข้อมูล (ไม่มี migration/backfill)** -- ตามข้อห้ามเดิมของ `1947` ข้อ 4
5. **ไม่แก้บรรทัดโค้ดใน `legacy_bridge.py`** -- แก้เฉพาะคอมเมนต์ (ตรวจด้วย `git diff` ก่อน commit)
6. **ไม่อ้างว่า `GT-245` ปลดล็อกให้บูตแล้ว** -- การแก้หัวใบ (BLOCKED -> READY) เป็นของ chief คัดกรองคิว
   (`2159`) ไม่ใช่ของรอบนี้

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. **ตรวจ `pirate-force-server#778` ก่อนอย่างอื่น** (GATE_UNVERIFIED ข้างบน) -- ถ้าแดง แก้ในรอบนั้นทันที
   ถ้าเขียว/merge แล้ว ไม่ต้องทำอะไรเพิ่ม
3. **หยิบผล `pf-adversary` ครั้งที่ 2 เป็นงานแรกก่อน claim** (`ADVERSARY_PENDING #778`) -- ถ้าเจอข้อบกพร่อง
   แก้ใต้กิ่งเดิม (`claude/gifted-wright-fqc0na` ถ้ายังไม่ merge) หรือ PR ใหม่ (ถ้า merge แล้ว) ตามกติกา
4. ตรวจว่า chief ตอบใบ `2357` แล้วหรือยัง (class_id backfill hookup ค้างจากรอบ `suh0aq`)
5. ถ้ายังไม่มีอะไรใหม่ -- DB กลับไปคิว M4 ปกติ (NOW.md บรรทัด 49: `1101` ล็อกต่อรอ chief แก้ `store=` ที่
   `runtime.py:6443` -- งานสำรองรอบถัดไป: วัด `1101` เป็นรายงานหนึ่งหน้า ตามที่ `1450` ข้อ 6 ยังค้าง)
6. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ

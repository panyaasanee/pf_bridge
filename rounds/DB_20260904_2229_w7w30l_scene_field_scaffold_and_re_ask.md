# DB round (`w7w30l`) -- 2026-09-04T22:08+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- "รอเครื่องคุณ" ข้อ 2 (หน้าเลือกตัวแสดงฉากจริง) ยังรอ RE ใบแคบตอบก่อน โค้ดจริงยังไม่ส่ง
(ตามที่ `COO-DECISION 20260904_2152` สั่งให้ทำ -- สแกฟโฟลด์เท่านั้นรอบนี้ ไม่ใช่ตัวแก้) รอบนี้ปิด
ข้อ 2/3/4 ของใบ `2152` (ค้น capture + ร่างใบ RE + ส่ง PR scaffold) ตามกำหนด 23:31

## 1. ล็อกรอบ

- 22:08+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชันทั้งสองรีโป (`claude/admiring-ride-w7w30l` bridge, `claude/gifted-wright-w7w30l` server)
  ที่ระบบตั้งชื่อให้ชี้ตรงที่ `origin/main` 0 ahead/0 behind ก่อนเริ่ม
- commit `rounds/DB_20260904_2208_w7w30l_claim.md` push แล้วเปิด `pf_bridge#1213 [LANE-DB] round
  w7w30l: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1213` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -q "ADDRESSEE: LANE-DB"` (unanchored) บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี
`.CONSUMED.txt` คู่ -- ใบเดียวค้าง:

1. `notes_to_chief/20260904_2152_COO-DECISION-two-0x12-fields-external-captures-first-then-narrow-re-
   scaffold-now-LANE-DB.md` (COO 21:52) -- งานของทั้งรอบนี้ ตอบด้วย §3

สร้าง stub `.CONSUMED.txt` แล้ว

## 3. ทำอะไร

### 3.1 ข้อ 2 ของ `2152` -- ค้น capture ภายนอกก่อน (≤10 นาที ตามกำหนด)

ค้น `archive/stray_captures_20260819/` (3 ไฟล์ capture จริงที่มีอยู่ในรีโปนี้ทั้งหมด) พบไฟล์เดียวที่มี
`CreateActorVital`: `GAME_20260819_015205_409718_61636.txt` -- ตัวละคร `test01`, `CREATE_ACTOR_DECODE`
มี `field20=1 field22=1` (ตรงกับ `u16 tag 0x12` สองตัว) แต่นี่คือ capture ที่ localtest สร้างที่ Port
Royal เหมือนกันทุกประการกับ `get_preset_actor_wire()` -- **ไม่ไขว้ได้** (ไม่ต่างฉาก ไม่ต่างค่า) ค้น
`gamedata/00_SEARCH_HERE_FIRST.md`/ตาราง `CONSTDATA_TH__*` ด้วย: เป็นตารางค่าคงที่ของเกม ไม่ใช่
capture เฟรมจริง ไม่มีอะไรช่วยไขว้ได้เช่นกัน

🔴 **แก้ไขกลางรอบ (`pf-adversary` จับได้)**: รอบแรกที่ผมค้นแค่ capture จริง/ตารางค่าคงที่ ไม่ได้ grep
`external/PF_SERIALIZER_FIELDS.tsv` ตามกฎบังคับของ `external/00_SEARCH_HERE_FIRST.md` ("ก่อนเริ่มงาน
static ใด ๆ: grep หาชื่อ message ก่อนเสมอ แล้วเขียนว่าเจอ/ไม่เจอ") ก่อนร่างใบ RE ฉบับแรก แก้แล้ว: grep
`SelectActorVital`/`0x5DFF60` เจอสองแถว (`order 17`/`18`, `tag 0x12`, `+0x20`/`+0x22`, span
`[0x005DFF60,0x005E01C6)` sha `de9de2a0...e3f8a`) ตรงโครงสร้างเป๊ะกับที่โค้ดเดินเอง (u32 tag `0x19`
ที่ `order 16`/`+0x1C` ตามด้วย `0x12` สองตัวติดกัน) -- **ยืนยันโครงสร้างจากคนละเครื่องมือ แต่ไม่บอกชื่อ
ตัวแปร/ความหมาย** (ตารางนี้ประกาศเองว่าไม่ทำ) คำถามที่ RE ต้องตอบยังเปิดอยู่เต็มที่ แก้ไขแล้วในใบ
`2212` ก่อนส่ง (ดู §0.5 ของใบนั้น) -- ไม่มีใบไหนหลุดออกไปแบบไม่มีบรรทัด "ค้นแล้ว: เจอ/ไม่เจอ"

**ผล**: ค้นแล้ว: เจอ (แต่ไม่พอไขว้/ไม่พอตอบความหมาย) ⇒ ไปข้อ 3 ตามที่ใบ `2152` สั่ง

### 3.2 ข้อ 3 ของ `2152` -- ร่างใบขอเลข RE ใบแคบ

ส่ง `notes_to_chief/20260904_2212_LANE-DB-ASK-CHIEF-narrow-re-ticket-actor-wire-two-0x12-scene-
fields.md` (ADDRESSEE: chief) คำถามเดียวตามที่ COO ตัดสินคำต่อคำใน `2152` ข้อ 3 คำต่อคำ: serializer
`0x5DFF60` เขียน `u16 tag 0x12` สองตัวจากตัวแปรชื่ออะไร และหน้าเลือกตัวอ่านตัวไหนไปพิมพ์ชื่อฉาก
พร้อมบรรทัดค้นแล้วเจอ/ไม่เจอ (§0.5 ของใบ) ตามที่แก้ไขข้างบน

### 3.3 ข้อ 4 ของ `2152` -- PR scaffold (`pirate-force-server#767`)

- `src/pirateforce_foundation/persistence_scene_field_patch.py` (ใหม่): `locate_scene_field_candidates`
  เดินโครงสร้าง `actor_wire` ด้วย cursor เดียวกับที่ `extract_avatar_attr_wire_from_actor` เดิน
  (re-derive เอง ไม่ import `current/pf_login_game_server_v141.py`) หาออฟเซ็ตของฟิลด์ A และ B ทั้งสอง
  ไม่เดาว่าตัวไหนคือ scene_id · `patch_scene_field(actor_wire, field, scene_id)` แพตช์ทีละฟิลด์ตาม
  พารามิเตอร์ หรือคืนค่าเดิมเป๊ะเมื่อ `field=None` · ค่าคงตัวเดียว `SCENE_FIELD: str|None = None` (วันนี้
  = ไม่เขียนทับ) · `project_actor_wire_for_list(character)` = จุดเรียกจริง
- `legacy_bridge.LegacyProjector.character_list()` เรียก `project_actor_wire_for_list` แทน
  `c.actor_wire` ตรง ๆ (จุดฉายที่ `1947` ข้อ 3 อนุมัติไว้ให้แก้แล้ว)
- `tests/test_persistence_scene_field_patch.py` (19 เทส): หาออฟเซ็ตทั้งสองถูก, แพตช์ A/B แยกกันไม่
  กระทบอีกฟิลด์/ไบต์อื่น, error path (ฟิลด์ไม่รู้จัก, scene_id นอกช่วง u16, ไม่ใช่ int, ไบต์ขาด), และ
  เทสหลักที่ COO ขอ: `SCENE_FIELD=None` ⇒ `legacy_bridge.character_list()` ไบต์ออกเท่าเดิมทุกไบต์กับ
  สูตรเก่า (`c.actor_wire` ต่อตรง ๆ) ทั้งกรณีตัวละครยังอยู่ฉากเกิดและกรณีย้ายฉากไปแล้ว

**pf-adversary (เรียกก่อน commit ตามกติกา)** พบ 2 ข้อ แก้แล้วทั้งคู่ก่อน push:
1. `patch_scene_field`'s `scene_id` guard รับ `bool` เงียบ ๆ เป็น 0/1 (bool เป็น int subclass) และโยน
   `struct.error`/`TypeError` ผิดชนิดสำหรับ `float`/`str` แทนที่จะเป็น `TypeError` ที่เช็คได้แน่นอน --
   แก้ด้วย `isinstance(scene_id, bool) or not isinstance(scene_id, int): raise TypeError` เพิ่ม 2 เทส
   (จุดนี้ยังไม่ทำงานจริงตอนนี้เพราะ `field is None` short-circuit ก่อนถึงโค้ดนี้เสมอ แต่แก้ไว้ก่อนใครมา
   flip `SCENE_FIELD` ในอนาคต)
2. กระบวนการ (ไม่ใช่โค้ด) -- ดู §3.1 ข้างบน (พลาดกฎบังคับ grep `external/` ก่อนร่างใบ RE แก้แล้วในใบ)
pf-adversary ยืนยันด้วยว่า offset arithmetic ถูกต้อง (re-derive เองด้วย `Cursor` จริงจาก v141 ได้ค่า
เดียวกัน 38/41) และเทส byte-identical เรียกจุดเรียกจริงจริง ไม่ใช่ tautology (ตรวจ `session.py:100-102`
ยืนยันเส้นทางเรียกจริง)

## 4. ชุดเทสของรอบ

- ระหว่างทำงาน: `pytest tests/test_persistence_scene_field_patch.py` (ไฟล์ใหม่) +
  `tests/test_delete_refresh_hypothesis.py tests/test_foundation.py tests/test_player_name.py`
  (ไฟล์เดียวที่เรียก `.character_list(` จริงในรีโปนี้ -- `grep -l "\.character_list(" tests/*.py`)
  รันซ้ำหลังแก้ตาม pf-adversary แล้วด้วย -- เขียวทุกครั้ง
- ชุดเต็ม (ครั้งเดียวของรอบ, บน commit สุดท้าย `cfa20266` หลัง `git fetch origin main` ยืนยัน
  `origin/main` ยังเป็น `7f5eaaf0` เหมือนต้นรอบ ไม่ต้อง rebase): **10199 passed, 323 skipped, 1 failed**
  ตัวที่แดง = `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::
  test_every_symbol_exemption_is_still_earned` -- ตรวจแล้วด้วย `git stash`/รันเฉพาะเทสนี้บนต้นไม้ที่
  **ไม่มี** ดิฟฟ์ของผมเลย: แดงเหมือนกันเป๊ะ ⇒ **main แดงอยู่ก่อนแล้ว ไม่ใช่จากดิฟฟ์รอบนี้** ตรวจโค้ด/เทส
  ต่อพบว่าเป็นช่องว่างที่ประกาศไว้แล้วในตัวเทสเอง (`tests/test_npc_interaction_wire.py:547-562`):
  Python <=3.11 ทำให้ f-string ทัวไนซ์เป็น token เดียว ทำให้ guard เห็นไม่ตรง แต่ gate จริงพิน
  `python-version: '3.14'` ที่ผ่าน -- สิ่งแวดล้อมรันของเซสชันนี้คือ Python 3.11.15 (`python3 --version`)
  เจ้าของไฟล์ = LANE-E (commit `f2d3df2d`/`917c8a19` "LANE-E round ub8svt") ไม่ใช่เขตเขียนของผม
  (`runtime.py`, `tests/test_npc_interaction_wire.py`) -- ไม่แก้ ไม่ reopen อะไร ไม่ใช่ตัวบล็อกโค้ด M4
  ของผม แค่บันทึกไว้เพราะเจอระหว่างรันชุดเต็มตามกติกา

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ยังศูนย์โดยตั้งใจ** -- นี่คือสแกฟโฟลด์ (`SCENE_FIELD=None`) เทส `CharacterListWireIsUnchangedWhile
ScaffoldIsOffTests` พิสูจน์ว่าเฟรมรายชื่อตัวละครไบต์เท่าเดิมทุกไบต์กับก่อนรอบนี้ -- ไม่มีอะไรเปลี่ยนบนจอ
ผู้เล่นจนกว่า RE ตอบและมีคนแก้ `SCENE_FIELD` เป็น `FIELD_A`/`FIELD_B`

### 5.2 wire-DB
`pirate-force-server#767` เปิดแล้ว (`claude/gifted-wright-w7w30l` @ `cfa20266`) พร้อม
`PF-AUTOMERGE: v4` -- รอ gate

## 6. nonclaims

1. **ไม่อ้างว่ารู้แล้วว่าฟิลด์ไหนคือ scene_id** -- ยังเป็นคำถามเปิดที่ส่งให้ RE ตอบ (ใบ `2212`)
2. **ไม่อ้างว่า `external/PF_SERIALIZER_FIELDS.tsv` ปิดคำถามนี้ได้** -- ยืนยันแค่โครงสร้าง/ออฟเซ็ต
   ไม่มีความหมายของฟิลด์ (ดู §3.1, ใบ `2212` §0.5/nonclaim 4)
3. **ไม่อ้างว่าแก้ `1947` (หน้าเลือกตัวจริง) แล้ว** -- นี่คือสแกฟโฟลด์เท่านั้น `SCENE_FIELD` ยังเป็น `None`
4. **ไม่แตะ `characters.actor_wire` ในฐานข้อมูล** -- ไม่มี migration ไม่มี backfill (ห้ามตาม `1947`
   ข้อ 4 / `2152` ข้อ 5) · **ไม่แตะ `runtime.py`** · **ไม่แตะ `current/pf_login_game_server_v141.py`**
5. **ไม่อ้างว่า `tests/test_npc_interaction_wire.py` ที่แดงเป็นความผิดของดิฟฟ์นี้** -- ตรวจซ้ำด้วย
   `git stash` แล้ว แดงเหมือนกันบนต้นไม้ที่ไม่มีดิฟฟ์ของผมเลย และเป็นช่องว่างที่ไฟล์นั้นประกาศเองว่าเป็น
   Python-version-only ไม่ใช่ของ CI gate จริง (3.14)
6. **ไม่ reopen หรือแก้ไฟล์นอกเขตเขียนของ LANE-DB ใด ๆ** (`tests/test_npc_interaction_wire.py`,
   `runtime.py`, `current/`)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ + ตรวจว่า chief ตั้งเลข RE ใบแคบให้ใบ `2212` แล้วหรือยัง (ควรเกิดใน
   รอบ 22:21 ของ chief ตาม `2152` ข้อ 3) -- ถ้าตั้งแล้วรอผลจาก ka1-A/Codex (ไม่มีกำหนด เครื่อง Panya)
2. `pirate-force-server#767` -- ตรวจ gate เมื่อรอบถัดไปเริ่ม (ไม่รอในรอบนี้ตามกติกา §22 "งานถูกส่งมอบ
   ให้ reaper แล้วคือจบหน้าที่ของรอบ")
3. เมื่อ RE ตอบ: แก้ `SCENE_FIELD` ในไฟล์เดียวเป็น `FIELD_A`/`FIELD_B` ตามที่ RE ชี้ + เทสใหม่ที่ยืนยันว่า
   แพตช์จริง (เฟรมรายชื่อมี `0x12` ตามด้วย `scene_id` จริง ณ ออฟเซ็ตที่ยืนยันแล้ว) + มิวแทนต์บล็อบเก่า
   ต้องแดง (ตามที่ `1947` ข้อ 3 กำหนดไว้) -- PR ใต้รหัสรอบเดิมตามที่ `2152` ข้อ 4 สั่ง
4. ถ้ายังไม่มีผล RE และไม่มีจดหมายใหม่ -- DB กลับไปคิว M4 ปกติ (NOW.md บรรทัด 49: `1101` ล็อกต่อรอ
   chief แก้ `store=` ที่ `runtime.py:6443` -- งานสำรอง: ชิ้น 2 ส่วนที่ไม่รอ RE + backfill `class_id`)
5. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ

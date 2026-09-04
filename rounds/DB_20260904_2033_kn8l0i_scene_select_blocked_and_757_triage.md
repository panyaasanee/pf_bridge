# DB round (`kn8l0i`) -- 2026-09-04T20:33+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- งานแรกที่ NOW.md มอบให้ (`1947`: หน้าเลือกตัวพิมพ์ต้องแสดงฉากจริง) ยังไม่ปิด เจอเงื่อนไข
ที่ต้องรอ COO ตัดสินก่อนแก้โค้ดจริง (ดู §3.1) จึงไม่มีอะไรขึ้น main รอบนี้ที่ปลดเกณฑ์ไหน

## 1. ล็อกรอบ

- 20:33+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชันทั้งสองรีโป (`claude/admiring-johnson-kn8l0i` bridge, `claude/brave-goodall-kn8l0i` server)
  ที่ระบบตั้งชื่อให้ชี้ตรงที่ `origin/main` 0 ahead/0 behind ก่อนเริ่ม
- commit `rounds/DB_20260904_2033_kn8l0i_claim.md` push แล้วเปิด `pf_bridge#1198 [LANE-DB] round
  kn8l0i: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1198` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ

## 2. กล่องจดหมาย

`grep -q "ADDRESSEE: LANE-DB"` (unanchored ตามบทเรียนรอบก่อน) บน `origin/main` สดของ `pf_bridge`
ต้นรอบ หักใบที่มี `.CONSUMED.txt` คู่ -- สองใบค้าง:

1. `notes_to_chief/20260904_1947_COO-DECISION-select-screen-scene-name-from-character-positions-
   LANE-DB.md` (COO 19:47) -- งานแรกของรอบ ตอบด้วยงานหลัก §3
2. `notes_to_chief/20260904_2018_SYNC-NOTICE-pirate-force-server-pr757-closed-never-merged.md`
   (`pf_git_sync.ps1` [5d] 20:18) -- ตอบด้วย §4

สร้าง stub `.CONSUMED.txt` ทั้งสองใบแล้ว

## 3. ทำอะไร

### 3.1 งานแรก (`1947`) -- ติดที่การตรวจ ไม่ใช่ที่โค้ด

ต้นเหตุที่ COO ระบุ (`legacy_bridge.character_list` ต่อ `c.actor_wire` ตรง ๆ ไม่เคยใช้
`character_positions` ที่ `list_characters` JOIN มาแล้ว) **ตรวจซ้ำแล้วถูกต้อง** -- อ่าน
`session.py:100-102`, `legacy_bridge.py:25-29`, `store.py:627-630` ยืนยันตรงกับใบ

แต่ก่อนแก้ ตรวจตามกติกา "ห้ามเดา offset" ในใบเดียวกัน (ข้อ 4) ว่าฟิลด์ `u16 tag 0x12` ตัวไหนใน
`actor_wire` คือ scene_id จริง -- เดินโครงสร้างจริงของ `actor_wire` (ผ่าน cursor walk เดียวกับที่
`current/pf_login_game_server_v141.py`'s `extract_avatar_attr_wire_from_actor` ใช้อยู่แล้ว, อ่าน
อย่างเดียว ไม่แก้ไฟล์ v141) พบว่า:

- `characters.actor_wire` **ไม่ได้ประกอบผ่าน `player_wire.py`** เลย -- มันคือ `CreateActorDataEx` ที่
  ไคลเอนต์ส่งจริงตอนสร้างตัว (`lifecycle.py:138` `build()` → `actor_wire.bind_actor_and_avatar_identity`
  แก้แค่ identity/selector) การอ้างอิงบรรทัด `223`/`306` ของ `player_wire._make_actor_attr_with_name(
  _and_class)` ในใบ `1947` เป็นคนละ serializer คนละโครงสร้างกับ `actor_wire` จริง
- โครงสร้างจริง (จาก preset ที่เทสทั้งรีโปใช้ร่วมกัน): หลัง `u32 tag 0x19 = 1` (= สมมติฐาน class_id ที่
  `COO-DECISION 20260903_1943` สั่งห้ามใช้เป็นความจริง) มี **`u16 tag 0x12` สองตัวติดกัน ค่า = 1 ทั้งคู่**
  ก่อนถึง `astr`/`wstr` แล้วต่อด้วย embedded AvatarAttr
- ตัวอย่างเดียวที่มี (`get_preset_actor_wire()`) สร้างตัวละครที่ Port Royal (scene_id คาดว่า=1) เหมือน
  ทุกการสร้างจริง ⇒ **ไม่มีทางแยกจากตัวอย่างเดียวว่า field A หรือ field B คือ scene_id** ทั้งคู่อ่านได้ 1
  เท่ากัน เขียนทับผิดตัวจะไม่มีทางรู้จากเทสเลยเพราะค่าที่ผิดก็ยังคง "1" เหมือนเดิม
- นี่คือกับดักเดียวกับที่ `persistence_class_id.py` เคยเจอกับ tag `0x19` มาแล้ว (tag ชนกัน คนละฟิลด์
  คนละออฟเซ็ต, docstring ของไฟล์นั้นเตือนไว้ตรง ๆ)

**ตัดสินใจไม่เขียนโค้ดแก้จนกว่า COO จะชี้** -- ใบ `1947` ข้อ 4 ห้ามเดา offset ชัดเจน และเขียนทับผิดตัว
จะส่งบิตขยะเข้าฟิลด์ที่ไม่รู้ความหมายไปทุกเฟรมรายชื่อตัวละครของทุกคนอย่างเงียบ ๆ ไม่มี GT ไหนจับได้ถ้าเดาผิด
(ทางเลือกที่ไม่มีทางพิสูจน์ถูกด้วยหลักฐานที่มี = เขียนใบถึง COO ก่อนตัดสินเอง) ส่งใบ
`notes_to_chief/20260904_2058_LANE-DB-TO-COO-scene-select-fix-blocked-two-identical-u16-0x12-
fields.md` พร้อมสามทางเลือก (มี second capture ไหม / เปิด RE ใบแคบ / เขียนทับทั้งสองฟิลด์ -- ไม่แนะนำ)

โครงร่างโค้ดแก้ (`legacy_bridge.character_list` เดินสองรอบ: หา field boundary ด้วย cursor เดียวกับ
`bind_identity_and_selector`/`bind_common_attr_identity` ใช้อยู่แล้วใน `actor_wire.py`, patch เฉพาะ
2 ไบต์ของ field ที่ยืนยันแล้วด้วย `character.position.scene_id`) + เทส (fixture จาก
`legacy.get_preset_actor_wire()`, ตั้ง `character_positions.scene_id=2`, มิวแทนต์ที่ยังใช้บล็อบเก่า
ต้องแดง) **พร้อมเขียนทันทีที่ COO ชี้ตัวฟิลด์** -- ไม่ต้องคิดใหม่รอบหน้า

### 3.2 SYNC-NOTICE `pirate-force-server#757` ปิดเพราะเกตแดง -- ตรวจแล้ว ไม่ reopen รอบนี้

อ่าน gate log จริง (`actions/runs/33874297946`, job `gate` บน `windows-latest`): แดงจุดเดียวคือ
`pytest_subset exit=1` -- ทดสอบล้ม **1 ตัวเท่านั้น** จาก 9127 ผ่าน:
`tests/test_mob_ground_persistence.py::TheDurableDoorTests::
test_the_restore_half_stands_down_until_the_taken_marker_exists` -- `AssertionError: True is not false`
ที่บรรทัด 522 -- **ตรงกับที่รอบก่อน (`p6x3ee`) ทำนายไว้แล้วเป๊ะ** ในไฟล์รอบของมันเอง (§3.2 ข้อ 3): เทส
"ก่อน" ของ LANE-B เองที่โมดูล `mob_ground_persistence.py` (docstring ของมันเอง) บอกไว้ล่วงหน้าว่าจะพลิก
วันที่มาร์กเมท็อดคู่มีอยู่จริง -- ไม่ใช่ regression ของดิฟฟ์ `#757`

**ไม่ reopen PR รอบนี้**: เขตเขียนของสายนี้ไม่ครอบ `tests/test_mob_ground_persistence.py` (ไฟล์ทั้งใบ
เป็นของ LANE-B ตาม `COO-DECISION 20260901_1100`) -- แก้เองไม่ได้ และ `main` ยังไม่มีตัวแก้ของ LANE-B
(ตรวจแล้ว: `test_mob_ground_persistence.py:516-525` บน `origin/main` สดยังเป็นเทส "ก่อน" ตัวเดิม) เปิด
PR ซ้ำตอนนี้จะแดงเหมือนเดิมทันที เสียรอบเกตฟรี ๆ -- LANE-B ได้รับแจ้งแล้วจริงจากรอบก่อน (letter `1935`)
สร้าง stub CONSUMED ให้ SYNC-NOTICE นี้แล้ว โค้ด+เทสของ migration 012/สองเมท็อดยังอยู่ครบบน branch
`claude/gifted-wright-p6x3ee` (SYNC-NOTICE ยืนยันว่าไม่มีอะไรหาย) -- รอบไหนที่ LANE-B แก้/ลบเทสนั้นแล้ว
ค่อยหยิบกิ่งนั้นมาเปิด PR ใหม่

## 4. ชุดเทสของรอบ

**ไม่มีดิฟฟ์โค้ด** รอบนี้ (§3.1 บล็อกก่อนเขียน, §3.2 เป็นการอ่าน log อย่างเดียว) -- ไม่มีอะไรให้รันเทส
ไม่รันชุดเต็ม (ไม่มีอะไรเปลี่ยนให้วัด)

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
**ยังศูนย์** -- ไม่มีโค้ดขึ้น ไม่มีอะไรเปลี่ยนบนจอผู้เล่น

### 5.2 wire-DB
**ยังศูนย์** -- ไม่มีดิฟฟ์ ไม่มี PR เซิร์ฟเวอร์รอบนี้

## 6. nonclaims

1. **ไม่อ้างว่าแก้ `1947` แล้ว** -- บล็อกอยู่ที่การยืนยันฟิลด์ รอ COO ตอบใบ `2058`
2. **ไม่อ้างว่า `#757` กู้คืนแล้ว** -- เจตนาไม่ reopen เพราะแดงซ้ำแน่นอน (ไฟล์นอกเขตเขียนยังไม่แก้)
3. **ไม่แตะ `tests/test_mob_ground_persistence.py`, `legacy_bridge.py`, `session.py`, `actor_wire.py`,
   `player_wire.py`** รอบนี้ -- ยังไม่มีคำตอบจาก COO ที่ยืนยันฟิลด์ที่แก้ได้ปลอดภัย
4. **ไม่ได้อ้างว่า field A หรือ field B คือ scene_id** -- นี่คือคำถามเปิดที่ส่งให้ COO ตัดสิน ไม่ใช่ข้อสรุป
5. **ไม่ได้แก้/เดา field ไหนแบบเผื่อไว้ในโค้ด** -- ไม่มีโค้ดฉบับ draft/commented-out ทิ้งไว้ในกิ่งเลย

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ + ตรวจว่า COO ตอบใบ `2058` หรือยัง -- ถ้าตอบแล้ว เขียน
   `legacy_bridge.character_list` (หรือจุดที่ COO ชี้) ทันทีตามโครงที่วางไว้ §3.1 ไม่ต้องคิดใหม่
2. ถ้ายังไม่ตอบและเกิน 21:31 (ตามที่ใบ `1947` กำหนด) = escalation ตามกติกาเดิม (ไม่ใช่สายนี้ตัดสินเอง
   ว่าจะทำอะไรต่อ -- ใบ `2058` ส่งไปแล้วตรงเวลา ก่อน 21:31)
3. ตรวจว่า LANE-B แก้/ลบเทส `test_the_restore_half_stands_down_until_the_taken_marker_exists` แล้วหรือยัง
   -- ถ้าแก้แล้ว เปิด PR ใหม่จากกิ่ง `claude/gifted-wright-p6x3ee` (rebase ถ้าจำเป็น) ทันที ไม่ต้องเขียน
   migration 012 ใหม่
4. มาร์กกล่องจดหมายด้วย unanchored grep เสมอ
5. ถ้าไม่มีจดหมายใหม่และ COO ยังไม่ตอบ -- PLAYER/CHARACTER ยืนที่เดิม, DB กลับไปว่างได้ตามคิวปกติ
   (NOW.md บรรทัด 49)

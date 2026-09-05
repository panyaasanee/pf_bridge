# DB round (`6o6qnr`) -- 2026-09-05T21:04+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

อ่าน `NOW.md` สดล่าสุด (ตรวจล่าสุด 21:00 โดย COO, หลัง PANYA-ORDER `2038`/`2039` ตัด NOW จาก 68 KB
เหลือ 12 KB) ก่อนอื่นตามกติกา -- รอบนี้ขยับบันไดไมล์สโตน บรรทัด "PLAYER/CHARACTER = LANE-DB":
**"ตอนนี้: `select_character_honoring_home_marker` PR ตก 21:31 (`1946`)"** -- นี่คืองานของรอบนี้

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended ตาม `2159`)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- โค้ดรอบนี้ไม่แตะ world/scene state ที่แชร์ระหว่าง session เลย
(`character_home_marker`/`characters` เป็นข้อมูลต่อตัวละคร ไม่ใช่ต่อฉาก, ตรงกับ `1154` ที่ห้าม DB
รับงานโลก)

## 1. ล็อกรอบ

- `list_pull_requests`/`search_pull_requests` หัวข้อ `[LANE-DB]` สถานะ open ทั้งสองรีโป ก่อนแตะโค้ด:
  **ว่างเปล่าทั้งคู่** -- ไม่มีรอบทำงานค้าง ไม่ต้อง takeover
- เซสชันนี้ได้กิ่งที่ระบบมอบให้ตรงตัวอยู่แล้ว (`claude/kind-lovelace-6o6qnr` ที่ `pf_bridge`,
  `claude/intelligent-mendel-6o6qnr` ที่ `pirate-force-server` -- คนละกิ่งเดียวกันตลอดเซสชันนี้ ไม่ตัด
  กิ่งใหม่) `git fetch origin main` แล้ว fast-forward ทั้งสองกิ่งให้ตรง `origin/main` สดก่อนเริ่ม
  (`pf_bridge` -> `27e0a9a` ตอนเริ่มเขียนไฟล์รอบนี้, `pirate-force-server` -> `6e0e863`) -- ไม่มีอะไร
  หายเพราะกิ่งไม่มี commit ของตัวเองมาก่อนหน้านี้ (fast-forward ล้วน)

## 2. กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-DB"` บน `origin/main` สด: ใบใหม่ (ไม่มี `.CONSUMED.txt` คู่) มีหนึ่งใบ --
`20260905_1946_COO-DECISION-db1909-home-marker-reader-option-a-new-store-method-writelocktimeout-approved-as-operationalerror-subclass-LANE-DB.md`
(ตอบใบของ DB เอง `1909`, อ้าง `1606`/`0612`) -- อ่านทั้งสามใบ (`1946`/`1606`/`1909`) ก่อนแตะโค้ด

รีเฟรชกล่องจดหมายอีกครั้งกลางรอบ (หลัง NOW.md ปรับ 21:00): พบใบใหม่ที่สองจ่าหน้าถึง DB --
`20260905_2058_COO-DECISION-ka1a2039-item4-lane-q-needs-quest-state-columns-per-character-declare-store-doors-LANE-DB.md`
(LANE-Q ต้องการประตูสถานะเควสต่อตัวละคร) -- ใบนี้ระบุเองว่า **"ลำดับคุณไม่เปลี่ยน:
`select_character_honoring_home_marker` PR รอบ 20:01 ตก 21:31 (`1946`) มาก่อน · จดหมายถึง Q = งานที่
สอง ตก 23:01"** ⇒ รอบนี้ทำข้อ 1946 ให้เสร็จก่อน ใบ `2058` (จดหมายถึง Q + ประตูเควสจริง) เป็นงานของ
รอบถัดไป (ยังไม่ครบกำหนด, ดู §7)

## 3. ทำอะไร -- `COO-DECISION 1946` ทั้งสองข้อ

### 3.1 ข้อ 1: `store.select_character_honoring_home_marker(sid, selector)`

เมธอดใหม่ใน `store.py` (charter `COO-DECISION 20260901_1100`: เมธอดใหม่ทำได้ เมธอดเดิมห้ามแตะ) --
เรียก `select_character` เดิม (ไม่ถูกแก้แม้แต่บรรทัดเดียว) แล้วสลับเฉพาะ `position.scene_id` เป็น
`home_scene_id` เมื่อ `get_home_marker` เจอแถวที่ชื่อฉากต่างจากที่ยืนอยู่ -- `scene_seq`/`x`/`y`/`z`/
`heading` คงค่าจาก `character_positions` เดิมทุกประการ

**ทำไมไม่ resolve พิกัดสปอว์นเอง (ตามที่ใบ `1606` แขวนคำถามไว้ "+ ตำแหน่งเกิดของฉากนั้น")**: ตรวจ
`world_scene_entry.py` (module docstring) แล้วพบว่า `resolve_entry` -- ต่อสายอยู่ใน `runtime.py`'s
login path แล้วด้วยเหตุผลอื่น (ไม่เกี่ยวกับฟีเจอร์นี้) -- มีกฎข้อ 2 อยู่แล้ว: ตำแหน่ง XY ที่อยู่นอก
ขอบเขตพื้นของฉากปลายทางถูกแทนที่ด้วยสปอว์นที่ปักหมุดของฉากนั้นโดยอัตโนมัติ (พร้อมพิมพ์บรรทัดคอนโซล) --
ตรงกับสถานการณ์ของตัวละครที่ยืนอยู่ฉากอื่นแล้วถูกส่งกลับบ้านเป๊ะ ⇒ สลับแค่ `scene_id` พอ ไม่ต้อง
import ข้ามเขต (`world_scene_travel`/`gm.warp_executor` เป็นของ LANE-A) ไม่ต้องเดาพิกัด (ตรงกับ
`persistence_home_marker.HomeMarkerRow`'s docstring เองที่บอกไว้แล้วว่า "a spawn point inside that
scene is a later round's question, not a guess this door makes today")

ผลลัพธ์: ตัวละครไม่มี home marker หรือ home marker ชี้ฉากเดิม = คืนค่าเหมือน `select_character` ทุก
ไบต์ (ข้อบังคับจากใบ `1606` ข้อ 2: "นบต้องไม่เห็นอะไรเปลี่ยน") -- ตรวจด้วยเทสเปรียบเทียบตรง ๆ

### 3.2 ข้อ 2: `WriteLockTimeout` ครอบสามเมธอดเดิม

`write_typed_attributes` / `write_typed_attribute_if_unset` / `read_typed_attributes` เดิมปล่อย
`sqlite3.OperationalError("database is locked")` ดิบออกไปเมื่อชนล็อก -- ครอบด้วย `try/except` แบบ
เดียวกับที่ `spend_skill_points` ทำอยู่แล้ว (จับเฉพาะ `_LOCKED in str(error)` แล้ว raise
`WriteLockTimeout` แทน) -- `WriteLockTimeout` เป็น subclass ของ `sqlite3.OperationalError` อยู่แล้ว
ตั้งแต่นิยาม (`store.py:302` เดิม) จึงเข้าเงื่อนไขที่ `1946` ข้อ 2 วางไว้โดยไม่ต้องแก้คลาส -- ผู้เรียก
เดิมที่ `except sqlite3.OperationalError` ยังจับได้เหมือนเดิม ไม่มีใครพัง

`read_typed_attributes` ไม่มี `BEGIN IMMEDIATE` ของตัวเอง (อ่านล้วน) -- ครอบรอบ
`PRAGMA table_info`/`SELECT` แทน (statement แรกในบล็อก) ด้วยตรรกะเดียวกัน

## 4. ชุดเทสของรอบ

- `SelectCharacterHonoringHomeMarkerTests` (`tests/test_persistence_home_marker.py`): ไม่มี home
  marker = เหมือน `select_character` ทุกไบต์ · home marker ชี้ฉากเดิม = เหมือนกันอีก · home marker
  ชี้ฉากอื่น = สลับ `scene_id` เท่านั้น (x/y/z/heading/scene_seq/id/name/account_id/selector ตรงกัน
  หมด) · `select_character` เองยังคืนค่าดิบเหมือนเดิม (ไม่ถูกแก้) · selector ที่ไม่มีจริง = `KeyError`
  เหมือนกันทั้งสองเมธอด
- สองคลาสใหม่ใน `tests/test_persistence_typed_attr_columns.py`: proxy `sqlite3.connect` ที่ raise
  `database is locked` บน statement ที่ระบุ (ยกจากแบบเดียวกับ
  `test_store_skill_points.py::test_write_lock_timeout_replaces_a_raw_operational_error` แล้วสรุป
  เป็น helper ใช้ซ้ำ) พิสูจน์ทั้งสามเมธอด raise `WriteLockTimeout` ไม่ใช่ `OperationalError` ดิบ และ
  ไม่มีอะไรถูกเขียนเมื่อ `BEGIN IMMEDIATE` ถูกปฏิเสธ

`git merge origin/main` เข้ากิ่งเป็นขั้นสุดท้าย (`b7b53b9` -> `6e0e863`, fast-forward, ไม่มี
conflict) แล้วรันชุดเต็มครั้งเดียวบนต้นไม้นั้น: **11298 passed, 327 skipped, 20989 subtests passed,
0 failed (753.86s)** -- รันก่อนสร้าง commit สุดท้าย (`git status`/`git diff --cached` ตรวจแล้วว่า
สามไฟล์ที่แก้ตรงกับที่ commit จริง ไม่มีอะไรหลุด) `python3 tools_bridge/pf_gate_preflight.py --repo .`
เขียวทั้งสองครั้ง (ก่อนและหลัง merge) -- ไม่มี skip ใหม่ ไม่มี cp874 violation branch ตรงกับที่
มอบหมาย

BYTECODE_PURGED: `PYTHONDONTWRITEBYTECODE=1 python3 -B` ทุกคำสั่งรอบนี้ (ไม่มีการคืนค่ามิวแทนต์รอบนี้
เลย แต่ตั้งค่าไว้ทุกครั้งตามกติกาเริ่มต้นของ COMMON)

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
ศูนย์รอบนี้ -- เมธอดใหม่ยังไม่มีจุดเรียกจริง (`chief` ต้องสลับจุดเรียกใน `runtime.py`/`session.py`
อีกบรรทัดเดียวตามที่ `1946` ข้อ 1 มอบหมาย) ไม่มีอะไรเปลี่ยนบนจอผู้เล่นจนกว่านั้นจะเกิดขึ้น --
`GT-255` เนื้อใบพร้อมวางแล้ว (`1153`) แต่ยังเกรดไม่ได้จนกว่าจุดเสียบของ chief ขึ้น main

### 5.2 wire-DB
`pirate-force-server` PR (เปิดรอบนี้, ดู §6) -- diff เดียว: `src/pirateforce_foundation/store.py` +
สองไฟล์เทส -- ชุดเต็ม 0 failed ตามที่บันทึกใน §4

## 6. สถานะ PR

- `pirate-force-server#851` -- เปิดแล้ว ไม่ draft พร้อม `PF-AUTOMERGE: v4` ตั้งแต่เปิด (ยืนยันด้วย
  GET หลังเปิด: `state: open`, `draft: false`, marker อยู่ใน body จริง) จากกิ่ง
  `claude/intelligent-mendel-6o6qnr` (ไม่ใช่ PR ที่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมที่ส่งไคลเอนต์ --
  เมธอดใหม่ยังไม่มีผู้เรียก, สามเมธอดเดิมเปลี่ยนแค่ชนิด exception ตอนชนล็อก ไม่ใช่ boundary นั้น จึง
  ไม่ draft) -- commit `18f446a` -- `mergeable_state: unstable` ตอนเปิด (main ขยับไปอีกสอง PR
  ระหว่างรอชุดเต็มรัน, `merge-tree` ตรวจแล้วไม่มี conflict กับไฟล์ที่แก้) -- ยังไม่ตรวจ gate ตอนเขียน
  บรรทัดนี้ (ดู §7 ข้อ 1)
- `#798` (guard ฝั่งเขียน, `0612`): **merged** แล้วตั้งแต่ 2026-09-04 23:23 UTC (`0f2bd53` เป็น
  ancestor ของ `origin/main` ยืนยันด้วย `git merge-base --is-ancestor`) -- ไม่มีอะไรต้องรายงานเพิ่ม

## 7. รอบหน้าทำอะไร

1. ตรวจเกต PR ของรอบนี้ (`GATE_UNVERIFIED` จนกว่าจะตรวจ) เป็นงานแรก
2. ตอบใบ `2058` (LANE-Q ต้องการประตูสถานะเควสต่อตัวละคร): จดหมายจ่าหน้าถึง LANE-Q ระบุ (ก) ประตูที่มี
   จริงบน main วันนี้ (ข) ประตูใหม่ที่จะเปิด (`get/set quest state`, `player flag`) พร้อมชื่อ
   เมธอด/สัญญา/อ่านกลับหลังเขียน/`BEGIN IMMEDIATE` แบบ `spend_skill_points` (ค) รอบที่ PR จะออก --
   กำหนด 23:01 ตาม `2058`
3. หลังจดหมายถึง Q: เปิด PR ประตูเควสจริงตามที่ประกาศไว้ (ไม่รอ Q ขอ)
4. ตรวจว่า chief สลับจุดเรียกใน `runtime.py`/`session.py` มาเป็น
   `select_character_honoring_home_marker` แล้วหรือยัง (`1946` ข้อ 1 มอบหมายให้ chief) -- ถ้ายัง ไม่
   ใช่ของบล็อก DB แต่ถ้า `GT-255` ต้องเกรดต้องรอจุดนี้

## งานสำรอง (ทำเมื่องานหลักติด)

1. **ปลดแฟล็ก 1 ตัวในเขตตัวเอง** (`PANYA-ORDER 2039` ข้อ 3, งานสำรองข้อแรกของทุกสาย) -- ยังไม่มี
   `docs/PROMOTION_BACKLOG.md` จาก chief ให้เลือก (รอรอบ 23:51 ตาม `2059`) -- เมื่อมีแล้วเป็นข้อแรก
2. เพิ่ม method/เทสของ persistence ที่ `pf-adversary` เคยชี้เป็น debt (ยังไม่พบของใหม่รอบนี้)
3. ตอบใบ RE/STATIC เรื่อง schema/attr ที่ตอบได้จาก `reference_codex_attr` ที่ commit แล้ว

## nonclaims

1. **ไม่อ้างว่า `GT-255` เกรดได้แล้ว** -- ต้องรอ chief เสียบจุดเรียกก่อน (`1946` ข้อ 1)
2. **ไม่อ้างว่าผู้เล่นเห็นอะไรเปลี่ยนบนจอรอบนี้** -- เมธอดใหม่ยังไม่มีผู้เรียก
3. **ไม่อ้างว่าได้ resolve พิกัดสปอว์นของฉากบ้านจริง** -- ตั้งใจไม่ทำ (ดู §3.1) ปล่อยให้
   `world_scene_entry.resolve_entry` ที่ต่อสายอยู่แล้วจัดการ
4. **ไม่แตะไฟล์ใดในเขตของสายอื่น** -- ไม่มีการแก้ `runtime.py`/`app.py`/`session.py`/`lifecycle.py`
   รอบนี้
5. **ไม่อ้างว่าได้ตอบใบ `2058`** -- เป็นงานของรอบหน้า (กำหนด 23:01 ยังไม่ถึง)
6. **ไม่เรียก `pf-adversary`** -- ไม่มี tool ให้เรียกในเซสชันนี้เท่าที่ค้นเจอ แต่ทำ self-review เอง
   (อ่านทุก hunk ใน diff, ตรวจ docstring ทุกจุดตรงกับโค้ดจริง, ตรวจว่า `select_character` ไม่ถูกแก้
   ด้วย `git diff` โดยตรง) -- ไม่บันทึก `ADVERSARY_UNAVAILABLE` เพราะไม่ได้พยายามเรียกแล้วพบว่าหาย
   (ยังไม่มี `pf-adversary` agent ในรายชื่อ agent ของเซสชันนี้เลย)

SCOREBOARD: COMING | ตัวเลือก "กลับบ้านที่ Port Royal" จากเควส born-again จะย้ายฉากจริงตอน relog
ทันทีที่ chief เสียบจุดเรียกอีกบรรทัดเดียว (PR ของรอบนี้ยังไม่ merge) | pirate-force-server#851,
commit 18f446a, GT-255

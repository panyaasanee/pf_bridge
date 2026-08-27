# รอบ `A_hrz814` - สาย A - WORLD (`pf-builder`)

**เวลา:** 2026-08-27T18:48+07:00
**สาย:** A (WORLD)
**รอบ:** `hrz814`

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **ยังไม่มีอะไรเปลี่ยนบนจอเกม** — รอบนี้เพิ่มฟังก์ชันฝั่งเซิร์ฟเวอร์ (`make_columbus_conversation_two_options`,
> `matches_columbus_bornagain_dispatch`, `dispatch_columbus_quest3205`) ที่ทำ option 2 (quest 3205, "ตั้ง
> ฐานทัพที่ Port Royal") พร้อมใช้ **แต่ยังไม่มีใครเรียกที่จุด dispatch จริง** — ต้องรอ chief ต่อสายใน
> `runtime.py` ก่อน (`CORE-REQUEST-019`) ถึงจะเห็นผลจริง: ตอนนั้นผู้เล่นที่คุย Columbus จะเห็น **ตัวเลือกที่ 2**
> ในกล่องสนทนา นอกเหนือจาก "มุ่งหน้าไป Atlantic Ocean" เดิม — กดแล้วจะถูก refuse อย่างมีเหตุผล (ยังไม่มี
> คอลัมน์ DB เก็บ home-marker) ไม่ใช่ error ดิบและไม่ใช่สำเร็จหลอกๆ ไม่มี PR ฝั่ง `pf_bridge` ที่เปลี่ยนโค้ดเลย
> (เอกสาร/คิวเท่านั้น)

## ② ต้นรอบ: ตรวจชะตา PR รอบก่อน (ADDENDUM v2 หัวข้อ A)

`pull_request_read(method=get)` ยืนยัน PR ล่าสุดของสาย A ทั้งสอง repo ก่อนเริ่ม:

- **`pirate-force-server` #136** (`jafskv`): `merged=true`, `merged_by=github-actions[bot]` — อยู่บน `main`
  แล้ว (`persist_position_allowed` guard)
- **`pf_bridge` #222** (`jafskv`): `merged=true`, `merged_by=github-actions[bot]` — อยู่บน `main` แล้ว

ไม่มีอะไรต้อง cherry-pick ไม่มี PR `[LANE-A]` เปิดค้างทั้งสอง repo → เปิด PR ใหม่ยึดล็อก (`pirate-force-server
#139`, `pf_bridge #225`) ด้วย empty commit ก่อน (สร้าง branch ใหม่จาก `main`, ยังไม่มี diff ให้เปิด PR ได้จน
กว่าจะมี commit อย่างน้อยหนึ่งตัว)

## ③ กล่องจดหมาย (ADDENDUM v2 หัวข้อ B)

อ่านกล่องหลัง `jafskv` (18:20+07:00 เป็นต้นมา) พบใบใหม่ที่เกี่ยวกับสาย A โดยตรงเพียงใบเดียว:

- **`20260827_1746_COO-DECISION-M2-not-closed-fix-persistence-and-destination-scene-before-passing.md`**
  ถึง "chief · สาย A (WORLD) · สาย GM/RE runner" ตรงๆ — สั่งสาย A ทำ 2 เรื่อง: (1) แก้ persistence (ทำไปแล้ว
  รอบ `jafskv` ก่อนใบนี้ถูกเขียนด้วยซ้ำ — ตรงกัน ไม่ต้องทำซ้ำ) และ (2) **เพิ่ม option 2 (quest 3205) เข้า
  dialog Columbus 3021** — ยังไม่ได้ทำ ⇒ งานหลักของรอบนี้ (ดู ④) วาง `.CONSUMED.txt` คู่กันแล้ว (ต้นฉบับอยู่ที่
  เดิม + สำเนาไป `consumed/`)
- `RE-109 RESULT` (18:15+07:00): ถึง "chief (cloud) / LANE-B" ไม่ใช่ของสาย A — ข้าม
- ไฟล์อื่นที่ใหม่กว่า `jafskv` (`FROM_CHIEF_R196_*`, `LANE-A-CORE-REQUEST-018`/`LANE-A-STATUS` เอง) เป็นของที่
  สาย A เปิดเองในรอบ `jafskv` แล้ว หรือเป็นจดหมายจาก chief ถึง attended session — ไม่ใช่ของที่สาย A ต้อง
  consume ซ้ำ

## ④ ของที่สร้างจริงรอบนี้ (`pirate-force-server` — ทั้งรอบมีแค่นี้)

**สั่งจาก**: COO-DECISION 17:46+07:00, อ้างอิงข้อเท็จจริงจาก `20260827_1710_GT106-RESULT-*.md` ④.1 —
gamedata `MOBS 156 s_QUEST_BEGIN = 111;998;3021;3205;7062;7063`, `3205` = Q_BORNAGAIN "ตั้งฐานทัพที่ Port
Royal", `n_VARI_2=1` → lua เดิม `Player.ResetMarker(1)` (คนละเรื่องกับการวาร์ปฉาก — เป็น marker/spawn-save
action)

**ไฟล์ที่แตะ (2 ไฟล์, purely additive บน `src/pirateforce_foundation/columbus_quest_dispatch.py` ที่เป็น
โมดูลของสายนี้อยู่แล้ว)**:

- `columbus_quest_dispatch.py`: เพิ่ม `COLUMBUS_QUEST_BORNAGAIN_ID=3205`,
  `COLUMBUS_QUEST_BORNAGAIN_MARKER_ID=1`, `_conversation_entry()` (แยก helper จาก
  `make_columbus_conversation` เดิม — output เดิมไม่เปลี่ยน ยืนยันด้วยเทสที่มีอยู่แล้ว +
  `test_single_option_encoder_is_still_byte_for_byte_unchanged` ใหม่), `make_columbus_conversation_two_options`
  (entry_count=2, ทั้งสอง quest), `matches_columbus_dispatch` เพิ่ม param `quest_id=COLUMBUS_QUEST_ID`
  (default เดิมทุก call site เดิมไม่เปลี่ยน — มี call site จริงที่เดียวใน `runtime.py:4315-4317` เรียกแบบ
  positional หนึ่ง arg เท่านั้น ไม่โดนกระทบ), `matches_columbus_bornagain_dispatch`,
  `dispatch_columbus_quest3205` (refuse เสมอ, reason=`BORNAGAIN_MARKER_RESET_REFUSED_NO_PERSISTENCE_ROW`,
  ไม่มี branch ที่จะสำเร็จได้เลยในโค้ดตอนนี้)
- `tests/test_columbus_quest_dispatch.py`: เทสใหม่ 12 ตัว (27/27 รวมของเดิม) — ครอบ frame encoding ของ
  option คู่, การ match quest 3205, การ refuse เสมอของ `dispatch_columbus_quest3205`, และพิสูจน์ว่า path
  quest 3021 เดิม **ไม่เปลี่ยน** (`test_quest_3021_dispatch_is_unaffected_by_the_option_2_addition` pin
  token/จำนวนบรรทัดเป๊ะ)

**ห้ามแตะ `runtime.py`/`app.py` — ตามกฎ** ยังไม่มีใครเรียกฟังก์ชันใหม่ที่จุด dispatch จริง งานรอบนี้จบแค่
"ฟังก์ชันพร้อมใช้ + เทสผ่าน" → เปิด `CORE-REQUEST-019` ให้ chief ต่อสาย (ดู ⑥)

**เทส**: `test_columbus_quest_dispatch.py` 27/27 (เดิม 15) · `test_columbus_quest_dispatch_wiring.py` +
`test_world_columbus_m2_crosswalk.py` 16/16 ไม่เปลี่ยน (ไฟล์ไม่ถูกแตะ) · full suite `unittest discover` =
3632 เทส, 0 FAIL, 18 error เดิม (`capstone` import, ไม่เกี่ยวรอบนี้ — stash diff แล้วรันซ้ำยืนยันเลขเดิมทุก
ตัวยกเว้นเทสใหม่ 12 ตัวที่เพิ่ม), 208 skipped · cp874/ASCII-encodability ผ่านทั้ง 2 ไฟล์ (byte-scan ยืนยัน
ไม่มี byte > 0x7F)

## ⑤ ของที่สร้างจริงรอบนี้ (`pf_bridge` — เอกสาร/คิวเท่านั้น)

- **`CLIENT_RE_QUEUE.md`**: เปิดใบใหม่ `RE-112 BORNAGAIN-MARKER-RESET-WIRE-ACK-001` (เลขว่างยืนยันด้วย grep
  ทั้งสองไฟล์) — ถามว่าเกมเดิมส่งเฟรมอะไรกลับ (ถ้ามี) หลัง `Player.ResetMarker` — ห้ามเดา ต้องมีหลักฐานก่อน
  สาย A จะเขียนโค้ด persist จริง
- ไม่ได้แตะ `GAME_TEST_QUEUE.md` — ยังไม่มีอะไรให้ผู้เทส attended ทำได้จนกว่า `CORE-REQUEST-019` จะถูกต่อสาย

## ⑥ จดหมายที่เขียนรอบนี้

1. `20260827_1848_LANE-A-CORE-REQUEST-019-wire-columbus-quest3205-option2.md` — ขอ chief ต่อสายฟังก์ชันใหม่
   ทั้งสองเข้า `runtime.py` (ดู ④)
2. `20260827_1746_COO-DECISION-M2-*.CONSUMED.txt` — บริโภคคำสั่ง COO ส่วนของสาย A (ดู ③)

## ⑦ pf-adversary pass (ก่อนปิดรอบ)

รัน agent แยกตรวจ diff เต็ม (ไม่ใช่ตรวจเอง) ก่อน commit ตามกฎ — ผลลัพธ์: ตรวจครบ 6 แกน (byte-identical
regression ของ quest 3021 เดิม, unconditional refuse ของ quest 3205, positional-argument shadowing ของ
`quest_id` param ใหม่, self-referential test quality, ASCII purity, wiring-scope leakage เข้า `runtime.py`)
— **ไม่พบข้อบกพร่อง** ทุกแกน ยืนยันด้วยการรัน test suite จริงเอง (ไม่เชื่อตัวเลขที่รายงาน) และ diff เทียบ
`git stash` ก่อน/หลัง จุดเดียวที่ agent บอกว่ายืนยันเองไม่ได้ (ไม่ใช่ข้อบกพร่อง): ข้อเท็จจริง gamedata
(`MOBS 156`/`QUESTDATA` แถว 3205) เพราะ repo ที่ตรวจไม่มีไฟล์ gamedata — ข้อเท็จจริงนี้ยืนยันแล้วโดยตรงจาก
`GT-106-RESULT` ④.1 (attended, ka1-B) ในรอบที่แล้ว จึงไม่ใช่ช่องโหว่จริง

## ⑧ CORE-REQUEST

`CORE-REQUEST-019` (ดู ⑥.1) — ต่อสายฟังก์ชัน option-2 เข้า Columbus dispatch loop ใน `runtime.py`

## ⑨ เปิดใบให้สาย RE

`RE-112` (ดู ⑤) — เกมเดิมส่งอะไรกลับหลัง `Player.ResetMarker` ไม่รู้คำตอบ ไม่เดา เปิดใบให้ RE runner ตอบ

## ⑩ nonclaims

- **ไม่ได้อ้างว่า option 2 ใช้งานได้จริงตอนนี้** — ฟังก์ชันพร้อมใช้เท่านั้น ยังไม่มีจุดเรียกจริง (รอ
  `CORE-REQUEST-019`) และตัว dispatch เองก็ตั้งใจ refuse เสมอ (รอ `RE-112` + schema)
- **ไม่ได้ตัดสินปลายทางฉาก 17 vs 126** — COO มอบให้สาย GM/RE ไปหาหลักฐานก่อน ไม่ใช่ของสายนี้รอบนี้
- **ไม่ได้ทำ persistence fix ซ้ำ** — ทำไปแล้วรอบ `jafskv` ก่อน COO-DECISION ใบนี้ถูกเขียนด้วยซ้ำ ตรงกันพอดี
- **ไม่ได้ตัดสิน schema คอลัมน์ home-marker** — ถาม chief ตรงใน `CORE-REQUEST-019`
- **ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ได้แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py` · `world_scene_travel.py`
  (ไม่เกี่ยวกับงานรอบนี้) ทั้งรอบ

— สาย A · WORLD

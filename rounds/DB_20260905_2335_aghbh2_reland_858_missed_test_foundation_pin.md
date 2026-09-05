# DB round (`aghbh2`) -- 2026-09-05T23:35+07:00 -> 2026-09-05T23:49+07:00 (TZ=Asia/Bangkok)

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

อ่าน `NOW.md` สดล่าสุด (ตรวจล่าสุด 22:50 โดย COO) ก่อนอื่นตามกติกา -- รอบนี้ขยับบรรทัด "PLAYER/CHARACTER
= LANE-DB มาก่อนทุกอย่างในคิว DB" ทางอ้อมอีกครั้ง: `grant_learned_skill` + source `'learned'` (ตอบ
CORE-REQUEST `2119` ของ LANE-CS ที่ NOW.md เองอ้างถึงในบรรทัดนั้น) ที่ landed แล้วในรอบ `qul9wo` แต่ถูก
เกตปิดที่ Windows gate -- รอบนี้แก้สาเหตุจริงแล้วเปิด PR ใหม่ ยังไม่ merge (ดู §3/§7)

QUEUE_TRIAGE: ไม่ใช่หน้าที่ของสายนี้ (chief คัดกรองใบ attended)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- โค้ดรอบนี้ไม่แตะ world/scene state ที่แชร์ระหว่าง session
(`character_skills` เป็นข้อมูลต่อตัวละคร ไม่ใช่ต่อฉาก) เหมือนรอบ `qul9wo`

## 1. ล็อกรอบ

- `list_pull_requests` หัวข้อ `[LANE-DB]` สถานะ open ทั้งสองรีโปก่อนแตะโค้ด: **ว่างเปล่าทั้งคู่** -- ไม่มี
  รอบทำงานค้าง ไม่ต้อง takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`e0a54df`) -- กิ่งเซสชัน `claude/intelligent-mendel-aghbh2`
  · `pirate-force-server` เช่นเดียวกัน กิ่ง `claude/kind-lovelace-aghbh2` จาก `origin/main` (`d2b9ce8`
  ตอนเริ่ม)
- commit `rounds/DB_20260905_2335_aghbh2_claim.md` (สามบรรทัด) push แล้วเปิด `pf_bridge#1392
  [LANE-DB] round aghbh2: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1392` ของผมเอง ⇒ ไม่แพ้

## 2. กล่องจดหมาย

`grep -l "ADDRESSEE: (LANE-)?DB"` บน `origin/main` สด (ตรวจสองรอบ ครั้งแรกตอนเริ่ม ครั้งที่สองหลัง
`origin/main` ขยับระหว่างรัน full suite): ใบใหม่หนึ่งใบ
- `20260905_2332_SYNC-NOTICE-pirate-force-server-pr858-closed-never-merged.md` -- courier แจ้งว่า
  `pirate-force-server#858` (งานของรอบ `qul9wo` เอง) ถูกเกตปิด ไม่ merge -- **นี่คือใบที่ผมพบก่อนแล้วจาก
  การอ่าน PR `#858` ตรง ๆ (`pull_request_read`) ก่อนใบนี้จะถูกเขียนด้วยซ้ำ** เนื้อหาใบตรงกับสิ่งที่ผม
  วินิจฉัยและแก้ไปแล้วทั้งหมด -- บริโภคแล้ว (stub `.CONSUMED.txt` + สำเนาใน `consumed/`)

ไม่มีใบใหม่อื่นจ่าหน้าถึง DB (รีเฟรชกล่องจดหมายอีกครั้งก่อนปิดรอบ: ไม่มีใบใหม่เพิ่ม)

## 3. ทำอะไร -- วินิจฉัยและแก้ gate แดงที่ปิด `#858`

### 3.1 พบว่า `pirate-force-server#858` (รอบ `qul9wo` เอง) ถูกปิดโดย reaper

`pull_request_read get` บน `#858`: `state: closed`, `merged: false` -- อ่านคอมเมนต์ปิด
(`get_comments`): `Gate RED (job gate = failure)` run `33976719164` commit `2c227c6`

### 3.2 วินิจฉัยสาเหตุจริงจาก job log

`get_job_logs` (`failed_only`, `return_content`) บน run `33976719164`: `pytest_subset exit=1` --
`1 failed, 10407 passed`. ไล่หา traceback จริง (log ยาว 242KB ต้องค้นเป็นช่วง ๆ ผ่านสคริปต์ python
อ่านไฟล์ที่บันทึกไว้) พบตัวที่แดง: `tests/test_foundation.py:312`

```
AssertionError: Lists differ: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] != [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
```

รอบ `qul9wo` อัปเดตพินสามจุด (migration-count ใน `test_item_move_capture.py`, pending-versions list ใน
`test_persistence_speed_walk_seed_008.py`, CHECK-refusal probe ใน `test_persistence_character_skills_
011.py`) แต่พลาดจุดที่สี่ -- `tests/test_foundation.py:312` pin รายการเวอร์ชัน `schema_migrations` แบบ
เป๊ะจากการ replay migration ทั้งหมดกับ DB legacy ก่อน-006 ยังเขียน `[1..13]` -- ตัวเทสทำหน้าที่ของมัน
ถูกต้อง (จับ drift ที่แท้จริง) ไม่ใช่เทสพัง

`git grep` หา pin แบบเดียวกันอีกจุดในทั้งรีโป (`schema_migrations` ทุกไฟล์ที่อ้างถึง +
`10, 11, 12, 13\]` +ตรวจทุกไฟล์ที่แตะ `schema_migrations` ทีละไฟล์): **ไม่พบจุดที่ห้าที่พลาด** -- สี่จุด
คือครบ (สามจุดเดิม + จุดนี้)

### 3.3 re-land เนื้อหาเดิมทุกจุด + แก้จุดที่พลาด

ดึง diff จาก commit จริงของรอบก่อน (`bdf8c92` บนกิ่งเก่า `claude/cool-babbage-qul9wo` ที่ reaper เก็บไว้
ตามที่สัญญา -- "nothing is lost") มา apply บนกิ่งใหม่จาก `origin/main` สด:
`migrations/014_character_skills_learned_source.sql` (ไม่แก้อะไร) + `SQLiteStore.grant_learned_skill`
ใน `store.py` (แก้หนึ่งจุด: docstring อ้าง "migration 015" ผิดจากการ renumber รอบก่อน แก้เป็น "014") +
เทสใหม่ 19 ตัว (`test_persistence_character_skills_learned_014.py`) + สามไฟล์เทสเดิมที่ pin migration
facts (เหมือนรอบก่อนทุกจุด) **บวก** แก้ `tests/test_foundation.py:312` (list ต่อจาก `13` เป็น `14`
+ คอมเมนต์ชี้ไปที่ `014` แทน `013`)

ชิ้นเควสของรอบก่อน (piece 2 ของ `qul9wo`) **ไม่แตะรอบนี้** -- ยังรอคำตอบ chief/COO เรื่อง guard
`QuestAndShopStateGuardTests` ตามใบ `2236` เดิม (ยังไม่มีคำตอบ -- ตรวจแล้วรอบนี้ ดู §3.4)

### 3.4 ตรวจว่า chief/COO ตอบใบ `2236` (guard เควส) หรือยัง -- ยัง

Grep จดหมายทั้งหมดตั้งแต่ `2236`/`2237` ถึงตอนนี้ (`0035`): ไม่มีใบใหม่ตอบตรง ๆ (`2352`/`0035` เป็น
คำถามเรื่องเพดาน `AGENTS.md` และ scoreboard คนละเรื่อง) -- ไม่ยกระดับซ้ำรอบนี้ (ใบ `1909`-แบบเดียวกัน
ยกระดับไปแล้วครั้งหนึ่งในรอบ `qul9wo`) เก็บไว้เป็นงานแรกของรอบหน้า

### 3.5 `pf-adversary`

เรียกต้นรอบพร้อมเริ่มงาน (ก่อน push) บน diff เต็มของกิ่ง `claude/kind-lovelace-aghbh2`
(`d82adb1` เทียบ `origin/main`) -- ผลยังไม่คืนตอน push ⇒ `ADVERSARY_PENDING pirate-force-server#863`
ตามกติกา (ห้ามถือล็อกรอ)

## 4. ชุดเทสของรอบ

- ไฟล์ที่แตะ: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/test_persistence_character_skills_
  learned_014.py -q` → 19 passed · `tests/test_foundation.py tests/test_item_move_capture.py tests/
  test_persistence_character_skills_011.py tests/test_persistence_speed_walk_seed_008.py -q` → 80
  passed, 1 skipped, 14 subtests passed
- ก่อน push: `git merge origin/main` (ไม่มีอะไรใหม่ตอน merge) แล้วรันชุดเต็มครั้งเดียว: `pytest tests/ -q`
  → **11385 passed, 349 skipped, 0 failed, 21085 subtests passed (636.68s)**
- `python3 tools_bridge/pf_gate_preflight.py --repo .` → PASS (branch/cp874/skips/mainmerge/census/
  bridgesize ทุกข้อเขียว)

BYTECODE_PURGED: `PYTHONDONTWRITEBYTECODE=1 python3 -B` ทุกคำสั่งรอบนี้ + ลบ `__pycache__` ก่อน push

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
ศูนย์ -- `grant_learned_skill` ยังไม่มีจุดเรียกจริงจาก `runtime.py` เหมือนรอบก่อน (LANE-CS's Protocol
shim ยังไม่ wire) ผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอ

### 5.2 wire-DB
`pirate-force-server#863` -- diff 7 ไฟล์ (เหมือนรอบ `qul9wo` บวกไฟล์เดียวที่แก้เพิ่ม
`tests/test_foundation.py`) จากกิ่ง `claude/kind-lovelace-aghbh2` commit `d82adb1` -- เปิดแล้ว ไม่
draft พร้อม `PF-AUTOMERGE: v4` ตั้งแต่เปิด (ยืนยันด้วย GET: `state: open`, `draft: false`, marker อยู่
ใน body จริง) -- `mergeable_state: unstable` ตอนเขียนบรรทัดนี้ (ยังไม่ตรวจเกต Windows -- main ขยับอีก
ครั้งหลัง merge เข้ากิ่งแล้ว ไม่ได้ merge ซ้ำเพราะงบเวลารอบและ diff ไม่ทับกับ commit ใหม่ที่ main ได้)

## 6. nonclaims

1. **ไม่อ้างว่า `#863` merge แล้วหรือขึ้น `main` แล้ว** -- แค่เปิด+เขียว local เท่านั้น รอบถัดไปยืนยันด้วย
   `git merge-base --is-ancestor <sha> origin/main`
2. **ไม่อ้างว่า `grant_learned_skill` มีผู้เรียกจริง** -- zero production caller เหมือนรอบก่อน
3. **ไม่อ้างว่า `pf-adversary` ผ่านแล้ว** -- ผลยังไม่คืน บันทึกเป็น `ADVERSARY_PENDING` เท่านั้น (ห้ามเขียน
   "ผ่าน adversary" ก่อนผลคืนจริงตามกติกา)
4. **ไม่อ้างว่าใบ `2236` (guard เควส) มีคำตอบแล้ว** -- ตรวจแล้วรอบนี้ ยังไม่มี
5. **ไม่แตะไฟล์ใดในเขตของสายอื่น** -- diff ทั้งหมดอยู่ใน `migrations/`, `src/pirateforce_foundation/
   store.py`, `tests/` เขตเขียนของ DB ตามกฎบ้าน
6. **ไม่อ้างว่าพบจุดพลาดอื่นนอกจาก `test_foundation.py:312`** -- ค้นครบตาม §3.2 แล้วไม่พบจุดที่ห้า

## 7. รอบหน้าทำอะไร

1. ตรวจผล `pf-adversary` ของรอบนี้ (`ADVERSARY_PENDING pirate-force-server#863`) เป็นงานแรก -- เจอบั๊ก
   จริงที่ตอนนั้นอยู่บน `main` แล้ว = เปิดใบแก้ตัดจาก `main` ทันที ไม่รอคิว
2. ตรวจเกต `pirate-force-server#863` (Windows gate) -- ยืนยันด้วย `pull_request_read`/`merge-base
   --is-ancestor` ว่า merge จริงหรือถูกปิดอีกครั้งหรือไม่ก่อนอ้างสถานะใด ๆ
3. ตรวจคำตอบใบ `2236` (guard เควส) -- ถ้ามาแล้ว ทำตามทันทีเป็นงานหลัก (โค้ดจากชิ้นเควสที่ยังพร้อมอยู่ ต้อง
   เลื่อนเลข migration เป็นเลขว่างล่าสุด ณ ตอนนั้นเพราะ `014` ถูกจองไปแล้วรอบนี้)
4. ตรวจว่า LANE-CS เปิด CORE-REQUEST ใหม่/ปรับ arity ของ `learn_and_grant_skill` ให้ตรงกับ
   `grant_learned_skill` (ตามใบ `2228` ของรอบก่อน) หรือยัง

## งานสำรอง (ทำเมื่องานหลักติด)

1. **เฝ้าคำตอบใบ `2236`**: `notes_to_chief/` (อ่านอย่างเดียว) · หลักฐานผ่าน = พบใบตอบใหม่
2. **วัด `1101` ซ้ำ**: `grep -c "store=" src/pirateforce_foundation/runtime.py` บน `origin/main` สด
3. **ตรวจ CORE-REQUEST ใหม่จาก LANE-CS เรื่องปรับ arity `learn_and_grant_skill`**: `notes_to_chief/`

SCOREBOARD: COMING | ประตู "เรียนสกิลใหม่" (`grant_learned_skill` + `character_skills.source='learned'`)
ที่เคย landed แล้วครั้งหนึ่งแต่ถูกเกตปิดกลับมาเปิด PR ใหม่อีกครั้งพร้อมสาเหตุที่แท้จริงแก้แล้ว (พินเทสที่
พลาดจุดหนึ่ง) รอ merge จริง -- ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ (ยังไม่มีจุดเรียกจาก `runtime.py`) |
pirate-force-server#863, commit d82adb1, pf_bridge#1392

# DB round (`aghbh2b`) -- 2026-09-05T23:57+07:00 -> 2026-09-06T00:10+07:00 (TZ=Asia/Bangkok)

Continuation of round `aghbh2` (same session): that round closed and unlocked before `pf-adversary`
(called at its start) returned. Result arrived after unlock, per the protocol's own rule this round
picks it up as the first task, before claiming any new work.

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

ไม่ขยับ -- รอบนี้เป็นการแก้ finding ของ `pf-adversary` บน PR ที่เปิดค้างจากรอบก่อน (`#863`) ไม่ใช่งานใหม่
ใน NOW.md

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว (แก้คอมเมนต์เทสเดียว ไม่แตะ world/scene state)

## 1. ล็อกรอบ

- `list_pull_requests` หัวข้อ `[LANE-DB]` สถานะ open ทั้งสองรีโปก่อนแตะโค้ด: ว่างเปล่าทั้งคู่ (รอบ `aghbh2`
  ปิดและ merge ไปแล้วจริง -- ยืนยันด้วย `pull_request_read` ก่อนเริ่ม) ไม่ต้อง takeover
- กิ่ง `claude/intelligent-mendel-aghbh2` (pf_bridge) ถูกลบทิ้งโดย workflow ตอน merge รอบก่อน (ตามที่
  กติกาเอกสารไว้: "workflow ลบ ref ตอน merge") -- push ซ้ำขึ้นชื่อเดิม (ห้ามตั้งชื่อสาขาใหม่เอง ตาม
  `AGENTS.md §7`) สร้างกิ่งขึ้นใหม่จาก `origin/main` สด (`4b49353`)
- `pirate-force-server` ใช้กิ่งเดิมที่ยังเปิดอยู่ `claude/kind-lovelace-aghbh2` (PR `#863` ยังไม่ merge)
  ต่อยอด ไม่ต้องเปิดกิ่งใหม่
- commit `rounds/DB_20260905_2357_aghbh2b_claim.md` push แล้วเปิด `pf_bridge#1394 [LANE-DB] round
  aghbh2b: claim` (ไม่มี marker ตอนเปิด) list ซ้ำทันที: ใบเดียวของผมเอง ไม่แพ้

## 2. กล่องจดหมาย

ไม่มีใบใหม่จ่าหน้าถึง DB ระหว่างรอบนี้ (ตรวจก่อนเริ่มและก่อนปิด)

## 3. ทำอะไร -- แก้ finding ของ `pf-adversary`

ผล `pf-adversary` ที่เรียกต้นรอบ `aghbh2` (diff `d82adb1` เทียบ `origin/main`) คืนกลับมาหลังรอบนั้นปิดแล้ว
สรุปผล:

**ยืนยันแล้ว (high confidence) ว่าโค้ดถูกต้อง**: migration 014 (ตรวจ static เทียบ `004` + ทดสอบ live
corruption -- ตัด `INSERT` แถวออกแล้วรัน `migrate()` จริง ได้ `IntegrityError` DB ค้างที่ version 13 ไม่มี
ตาราง scratch ค้าง = rollback ทำงานจริง), `grant_learned_skill` concurrency/idempotency (20 thread
grant สกิลต่างกันพร้อมกัน -- ครบทั้ง 20 · 30 thread grant สกิลเดียวกันพร้อมกัน -- แถวเดียว ไม่มี error),
และคำอ้าง root-cause ของ `test_foundation.py` fix (reproduce ตรง ๆ ว่า `migrate()` บนต้นไม้ 14 ไฟล์ผลิต
`[1..14]` จริง)

**พบข้อบกพร่องจริงหนึ่งจุด (low severity)**: `tests/test_persistence_character_skills_011.py:199`
คอมเมนต์ที่เพิ่มใหม่ในรอบก่อนยังอ้าง `migrations/015_character_skills_learned_source.sql` -- ไฟล์จริงคือ
`014` ขัดกับที่ commit message ของรอบก่อนอ้างว่า "แก้จุด 015 แล้ว" (แก้จุดในไฟล์อื่นจริง แต่จุดนี้หลุด)
ไม่กระทบพฤติกรรมเทส (ยังทดสอบค่า `'trainer'` ที่ถูกปฏิเสธถูกต้อง) แต่ผิดถ้าใครอ่านย้อนหาว่าไฟล์ไหนขยาย
CHECK -- แก้แล้ว (commit `0c2f2c3`, เปลี่ยนคอมเมนต์บรรทัดเดียว ไม่แก้ logic)

**ตั้งข้อสังเกตล่วงหน้า (ไม่ใช่บั๊กของ diff นี้ เปิดเผยอยู่แล้วใน docstring ของ `store.py` เอง)**:
`skill_grant_wiring.py`'s `SkillGrantStore` Protocol เรียก `grant_learned_skill(character_id, skill_id,
granted_at)` สามอาร์กิวเมนต์ ขณะ concrete method รับสองอาร์กิวเมนต์ -- จะ `TypeError` วันที่มีคน wire
`runtime.py` เข้ากับ `SQLiteStore` จริงโดยไม่แก้ shim ก่อน บันทึกไว้ใน PR body ของ `#863` ให้ CS/chief เห็น
เมื่อถึงรอบ wiring จริง ไม่ใช่งานของ DB ที่จะแก้เอง (shim เป็นของ LANE-CS)

**คำถามเปิดที่ adversary ตั้งไว้ (ไม่ตัดสินใจแทนใคร)**: `migrate()` (ที่ทุกเทส/boot path จริงเรียก) ไม่ได้
สำรอง DB ก่อน มีแต่ `migrate_with_backup` ที่สำรอง -- migration 014 อ้างว่ากลไก backup "already covers"
มันแต่ไม่มีอะไรบังคับ caller จริงให้เรียก `migrate_with_backup` แทน `migrate()` เปล่า ๆ กับ DB ที่มีแถว
`character_skills` จริงอยู่แล้ว -- นี่คือช่องว่างเดิมของโค้ดเบส ไม่ใช่ของใหม่จาก migration นี้ (migration
009/013 เองก็อ้างกลไกเดียวกันมาก่อนแล้ว) ไม่ใช่ของที่ DB รอบนี้จะแก้ -- ถ้า chief ต้องการปิดช่องนี้จริง
ต้องเป็นจุดเสียบที่ chief เดินสาย `migrate_with_backup` เข้า boot path เอง (นอกเขตเขียนของ DB)

## 4. ชุดเทสของรอบ

`tests/test_persistence_character_skills_011.py tests/test_persistence_character_skills_learned_014.py
tests/test_foundation.py -q` → 56 passed, 1 skipped, 14 subtests passed -- ก่อน push: `git merge
origin/main` (ดึงงานของ LANE-B/LANE-UI ที่ landed ระหว่างรอ -- merge สะอาด ไม่มี conflict) แล้วรันชุดเต็ม
ครั้งเดียว: **11412 passed, 349 skipped, 0 failed, 21091 subtests passed (654.99s)**
`python3 tools_bridge/pf_gate_preflight.py --repo .` → PASS

BYTECODE_PURGED: `PYTHONDONTWRITEBYTECODE=1 python3 -B` ทุกคำสั่งรอบนี้ + ลบ `__pycache__` ก่อน push

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable
ศูนย์ -- คอมเมนต์เทสเดียวเท่านั้น ไม่มีพฤติกรรมเปลี่ยน

### 5.2 wire-DB
`pirate-force-server#863` -- อัปเดตด้วย commit ใหม่สองตัว (`ce80d56` = merge `origin/main` +
`0c2f2c3` = แก้คอมเมนต์) จาก `d82adb1` เดิม -- ยังเปิด ไม่ draft พร้อม `PF-AUTOMERGE: v4` (ยืนยันด้วย GET
ซ้ำ) -- อัปเดต body ของ PR ให้สะท้อนผล adversary + ตัวเลขชุดเต็มใหม่ -- `mergeable_state: unstable`
ตอนเขียนบรรทัดนี้ ยังไม่ตรวจเกต Windows

## 6. nonclaims

1. **ไม่อ้างว่า `#863` merge แล้ว** -- ยังเปิด รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`
2. **ไม่อ้างว่าปัญหา `skill_grant_wiring.py` arity mismatch เป็นบั๊กที่ DB ต้องแก้** -- เป็น shim ของ
   LANE-CS บันทึกไว้ให้เห็นเท่านั้น
3. **ไม่ตัดสินใจแทน chief เรื่อง `migrate()` vs `migrate_with_backup()`** -- เป็นคำถามเปิดที่ adversary
   ตั้ง ไม่ใช่ของใหม่จาก migration นี้ ไม่แตะ boot path (นอกเขตเขียนของ DB)
4. **ไม่แตะไฟล์ใดในเขตของสายอื่น** -- แก้บรรทัดเดียวในไฟล์เทสของ DB เอง

## 7. รอบหน้าทำอะไร

1. ยืนยันว่า `#863` merge จริงหรือถูกเกตปิดอีกครั้งหรือไม่ (`pull_request_read` + `merge-base
   --is-ancestor`) ก่อนอ้างสถานะใด ๆ
2. ตรวจคำตอบใบ `2236` (guard เควส) ตามเดิม
3. ถ้า `#863` merge แล้ว: พิจารณาว่าจะเปิดใบถึง chief เรื่อง `migrate()` vs `migrate_with_backup()`
   (จากคำถามเปิดของ adversary §3) หรือปล่อยเป็นหนี้เดิมของโค้ดเบสที่ chief ทราบอยู่แล้ว

## งานสำรอง

1. เฝ้าคำตอบใบ `2236`
2. ตรวจ CORE-REQUEST ใหม่จาก LANE-CS เรื่องปรับ arity `learn_and_grant_skill` ให้ตรงกับ
   `grant_learned_skill`

SCOREBOARD: NONE | ไม่มีอะไรใหม่ที่ผู้เล่นเห็นรอบนี้ -- แก้คอมเมนต์เทสเดียวตามผล pf-adversary บน PR ที่
เปิดค้างจากรอบก่อน (`#863` ยังไม่ merge ผู้เล่นยังไม่เห็นอะไรเปลี่ยนไม่ว่ารอบไหน) | pirate-force-server#863
commit ce80d56/0c2f2c3, pf_bridge#1394

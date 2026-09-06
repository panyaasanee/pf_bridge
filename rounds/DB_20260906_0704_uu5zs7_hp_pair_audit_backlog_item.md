# LANE-DB round `uu5zs7` -- read-only HP-pair audit (GM 0436 backlog item), main queue still blocked on Panya's capture

รหัสรอบ: `uu5zs7` · เวลาเริ่ม: 2026-09-06T07:04+07:00 · claim (ไม่ใช่ takeover)

## 0. ขยับ NOW/M ข้อไหน
`NOW.md` บรรทัด "🔴 สวมอาวุธ (`0345`/`0346`)": **ไม่ขยับ**. ทาง (ก) ยังคง `merged: true` บน
`pirate-force-server#883` เหมือนรอบก่อน (`9otpzx`) ยืนยันซ้ำผ่าน `pull_request_read get`. ทาง (ข)
`RE-272`/`GT-272` ยังไม่มีผลจับจริง (grep `RE-272.*RESULT`/`GT-272.*RESULT` ใน `CLIENT_RE_QUEUE.md`,
`GAME_TEST_QUEUE.md`, `notes_to_chief/*.md` = 0 hit ทั้งหมด) -- ยังรอเครื่อง Panya เหมือนเดิม เวลาเริ่ม
รอบนี้ (07:04) ยังไม่ถึงครึ่งเดดไลน์ 14:00 (จุดทวง COO ตามไฟล์รอบก่อนคือ ~09:00+) จึงยังไม่ทวง

รอบนี้จึงหยิบ **งานสำรองข้อ 2** ของไฟล์รอบก่อน (`9otpzx`) แทน: read-only audit ของ HP-pair rows
สามสภาพที่ตอบจดหมาย GM `0436` ไว้ -- ปิดคำสัญญาที่เขียนไว้ในจดหมาย
`20260906_0536_LANE-DB-REPLY-gm0436-...md`

## 1. ล็อกรอบ
`git fetch origin main` แล้ว `list_pull_requests` (pf_bridge, open): มี `[LANE-E] round d5igq0: claim`
เท่านั้น (ไม่ใช่ `[LANE-DB]`) -- ไม่มีล็อกค้างของสายตัวเอง ตัดกิ่งใหม่จาก `origin/main`
(`claude/epic-meitner-uu5zs7`, กิ่งที่ระบบให้เซสชันนี้) เปิด claim `pf_bridge#1443` list ซ้ำทันที:
มีใบเดียวคือของตัวเอง (บวก `#1440` ของ LANE-E) ⇒ ไม่แพ้ ทำงานต่อ

## 2. แหล่งความจริงที่อ่านตามลำดับ
1. `NOW.md` (fetch สด สองครั้ง -- ต้นรอบ 06:47 และท้ายรอบ 07:20 -- บรรทัด "ตรวจล่าสุด" ไม่ขยับระหว่างนั้น)
2. mailbox `ADDRESSEE: LANE-DB`/`ADDRESSEE: DB` ไม่มี `.CONSUMED.txt` คู่: **ว่างเปล่า** (เช็คคำต่อคำที่
   `notes_to_chief/` ไม่ใช่ `consumed/` -- ทุกใบถึงรอบก่อนมี stub ครบ, และไม่มีใบใหม่ตั้งแต่ `0536`
   ถึงตอนเช็คซ้ำ 07:20)
3. `AGENTS.md` §7: `git log` ยืนยันไม่มีคอมมิตใหม่กว่ารอบก่อนของตัวเอง -- ไม่มีกฎใหม่ที่ขัดกับรอบนี้
4. ไฟล์รอบล่าสุด `rounds/DB_20260906_0536_9otpzx_...md` หัวข้อ "รอบหน้าทำอะไร": ข้อ 1/2/3 ยังรอ
   Panya/chief (ไม่มีอะไรให้ทำ) ข้อ 5 (audit read-only) หยิบมาทำเป็นงานหลักรอบนี้เพราะข้อ 3/4 ยังไม่ถึง
5. ไม่มีจดหมาย broadcast ใหม่กว่า `FROM_CHIEF_R364` ที่ consume ไปแล้วรอบก่อน

## 3. งานที่ทำจริง

### 3.1 ยืนยันสถานะคิวหลักซ้ำ (ก่อนหยิบงานสำรอง)
- `pull_request_read get` บน `pirate-force-server#883`: `merged: true` เหมือนรอบก่อน (ไม่เปลี่ยน)
- `grep -in "RE-272.*RESULT\|GT-272.*RESULT"` ทั่ว `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/
  `notes_to_chief/*.md` = 0 hit -- ยังไม่มีผลจับจริง งานหลักยังติดที่เครื่อง Panya จริง ไม่ใช่ที่โค้ด
- `GT-255` full body (`GAME_TEST_QUEUE.md:10615-10706`): `grep -n "ATTENDED:"` = 0 hit ยังไม่ถูก chief
  วางบล็อกตามจดหมายที่ส่งไปรอบก่อน -- ไม่ใช่สิ่งที่ DB ทำต่อได้เอง (เขตเขียนของ chief)

### 3.2 read-only audit ของ HP-pair rows (`pirate-force-server#896`)
เพิ่ม `src/pirateforce_foundation/persistence_hp_pair_audit.py`: หนึ่ง aggregate `SELECT` นับแถวที่
เข้าเงื่อนไขสามสภาพที่ GM วัดได้จริง (`hp_max IS NULL` · `hp_current > hp_max` · `hp_max = 0`) แยก
live/any ต่อสภาพ (รูปแบบเดียวกับ `persistence_null_audit`) -- ยืนยันก่อนเขียนว่าทั้งสามสภาพเกิดได้จริง
บนสคีมานี้: `migrations/006` วาง `CHECK` อนุญาต `hp_max IS NULL`/`hp_max = 0` และไม่มีกฎข้ามคอลัมน์
ระหว่าง `hp_current`/`hp_max` เลย (`grep -n "hp_current\|hp_max" migrations/006_*.sql`)

เพิ่ม `SQLiteStore.hp_pair_audit()` -- ผ่าน `connect_read_only` เหมือน `typed_column_null_audit`
(เหตุผลเดียวกัน: ไม่ขยับไบต์ของไฟล์ที่ตั้งใจให้ hash ไม่เปลี่ยน) เขตเขียนของตัวเอง (`persistence_*.py`
+ เพิ่ม method ใหม่ใน `store.py` โดยไม่แก้ method เดิม) -- ไม่แตะ `runtime.py`/`app.py`/`gm/`

เทส `tests/test_persistence_hp_pair_audit.py` (17 ใบ): แต่ละสภาพ reachable จริงบนสคีมา · ประตูของ
login vitals resolver ปฏิเสธจริงทั้งสาม (grade ต่อ `persistence_vitals.resolve()` ตรง ไม่ใช่ prose) ·
ไม่มีคำสั่งเขียนในโมดูล (AST scan ตามแบบ `test_persistence_null_audit.py`) · แถว soft-delete นับแยก ·
ประตู store ถูกเปิดจริงและไม่ขยับไบต์ของไฟล์ (sha256/mtime/data_version ก่อน-หลัง) · ค่าที่นับไม่ได้
พิมพ์ `not-counted` ไม่ใช่ `0`

**กับดักที่เจอและแก้ระหว่างเขียน**: ดราฟต์แรกของ docstring โมดูลสะกดชื่อโมดูล login-vitals resolver
ตรง ๆ ในประโยคอธิบาย ทำให้ `tests/test_persistence_login_vitals.py::
TheModuleOwnsNoConstantsTests::test_the_module_has_at_most_one_seam_and_it_is_the_login_one` แดง
(การ์ดสแกน `src/` หาการสะกดชื่อโมดูลนั้นแบบตรง ๆ ทุกที่ ยกเว้น `session.py` จุดเดียว) -- แก้เป็นบรรยาย
ด้วยคำพูดแทนตามรูปแบบที่ `persistence_null_audit`/`persistence_login_vitals` เองใช้กับการอ้างถึงกัน
(measured, ไม่ใช่แค่คาดเดา: รันเทสไฟล์นั้นซ้ำหลังแก้ = เขียว)

### 3.3 ชุดเต็ม + preflight + PR
`git fetch origin main` -> fast-forward merge เข้ากิ่ง (ไม่มีคอมมิตชนกัน, ได้ `damage_by_skill.py` ของ
สายอื่นมาด้วย) -> `pytest tests/` ชุดเต็มครั้งเดียวบนต้นไม้ที่ merge แล้ว = **11910 passed, 365
skipped, 0 failed** (468s) -> `python3 tools_bridge/pf_gate_preflight.py --repo` จากโคลน `pf_bridge`
= PASS ทุกช่อง (cp874/skips/mainmerge/census/branch/bridgesize/scoreboard-manual)

PR ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมที่ส่งไคลเอนต์ (มีแต่ query อ่านอย่างเดียวกับ method ใหม่ใน
store) ⇒ เปิดตรงได้ ไม่ต้อง draft ตาม `HOWTO_OPEN_A_PR.md`

Body ของ PR final ตรวจผ่าน `pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage final` จากโคลน
`pf_bridge` ก่อนเปิด = `[prbody] PASS - exactly one marker line (line 16), nothing else mentions the
token` -- เปิด `pirate-force-server#896` แล้ว `pull_request_read get` กลับมายืนยัน body ที่ GitHub
เก็บจริงมี marker บรรทัดเดียวคำต่อคำ (ไม่ใช่แค่ไฟล์ที่ตรวจไปตอนแรก)

### 3.4 pf-adversary
ค้นด้วย ToolSearch/Agent listing: ไม่มี `pf-adversary` ในรายชื่อ agent ที่เซสชันนี้เรียกได้ ⇒ บันทึก
`ADVERSARY_UNAVAILABLE pirate-force-server#896` ตามกฎ · ทำ self-review แทน: อ่านทุก hunk ใน
`git diff --cached` ก่อน commit (3 ไฟล์ ไม่มีอะไรนอกเขตเขียนของตัวเอง) · รันมิวแทนต์เฉพาะไฟล์เทสที่แตะ
(`pytest tests/test_persistence_hp_pair_audit.py` -- เขียว 17/17, ดูข้อ 3.2 สำหรับกับดักที่จับได้จริง
ระหว่างทาง) · รอบหน้าของ LANE-DB สั่ง adversary บนกิ่งนี้เป็นงานแรกถ้ายังมีชีวิต (branch เก็บไว้แล้ว)

## 4. ชุดเทสของรอบ
`tests/test_persistence_hp_pair_audit.py` (17 ใบ ใหม่ทั้งไฟล์) + ชุดเต็ม `pytest tests/` = 11910
passed / 365 skipped / 0 failed (ดู 3.3)

## 5. หลักฐาน -- สองชั้นแยกกัน
### 5.1 client-observable
ศูนย์ -- นี่คือ reporting door อ่านอย่างเดียว ไม่มีอะไรถึงจอผู้เล่น ไม่มีการเปลี่ยน behavior ของ path
ที่ผู้เล่นแตะได้เลย (login เดิมยังทำงานเหมือนเดิมทุกประการ)

### 5.2 wire/DB
`pirate-force-server#896` (`html_url`, `mergeable_state: unstable` ตอนเปิด -- ปกติสำหรับ PR ที่ยังไม่
รัน gate, ไม่ใช่ conflict) · `pull_request_read get` ยืนยัน body มี `PF-AUTOMERGE: v4` บรรทัดเปลือย
บรรทัดเดียว · เทสทั้ง 17 ใบเขียว + ชุดเต็ม 11910 passed 0 failed · `pf_gate_preflight.py --repo` PASS
คำต่อคำ (ทุกช่องรวม `[mainmerge]`/`[census]`/`[bridgesize]`)

## 6. nonclaims
1. ไม่อ้างว่านับจำนวนแถวจริงบนฐานข้อมูลของเจ้าของแล้ว -- โมดูลนี้เขียนและเทสบนฐานข้อมูลชั่วคราวใน
   `TemporaryDirectory` เท่านั้น (แบบเดียวกับที่ `persistence_null_audit`'s header ระบุเรื่องตัวเอง)
2. ไม่อ้างว่าสามสภาพนี้คือสาเหตุเดียวที่ login gate ปฏิเสธแถวได้ -- `REASON_NOT_SEEDED`/
   `REASON_LEVEL_ZERO` ยังมีอยู่และตั้งใจไม่รวมมาตามที่ตอบ GM ไว้ (ดู 0. และตัวโมดูลเอง)
3. ไม่อ้างว่า `pf-adversary` ตรวจแล้ว -- ไม่มีให้เรียกในเซสชันนี้ (`ADVERSARY_UNAVAILABLE`) ทำ
   self-review แทนตามกฎ
4. ไม่อ้างว่า RE-272/GT-272 มีผลจับจริงแล้ว -- ยังรอเครื่อง Panya เหมือนรอบก่อนทุกประการ (ดู 3.1)
5. ไม่อ้างว่า `GT-255` READY เต็มรูปแบบ -- ยังรอ chief วางบล็อก `ATTENDED:` ตามจดหมายที่ส่งไปแล้ว
6. ไม่อ้างว่าใบนี้ปิดหนี้ hp-pair rows ทั้งหมด -- นี่คือ**การนับ**เท่านั้น ยังไม่มีการตัดสินว่าจะ backfill
   อย่างไร (หรือจะ backfill หรือไม่) และไม่มีสิทธิ์ตัดสินเองตาม `COO-DECISION 20260903_1047` ข้อ 2's
   สปิริตเดียวกัน (ห้าม backfill ก่อนเห็นตัวเลข -- ตัวเลขจริงบนฐานเจ้าของยังไม่มีใครรัน `hp_pair_audit()`)

## 7. รอบหน้าทำอะไร
1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. เช็คว่า `pirate-force-server#896` merge หรือยัง (`git merge-base --is-ancestor <sha> origin/main`
   ไม่ใช่ฟิลด์ `merged` ของ API) -- ถ้ายัง ดู gate/reaper ว่าติดอะไร
3. เช็คว่า chief วางบล็อก `ATTENDED:` ของ `GT-255` แล้วหรือยัง (`grep "^ATTENDED:"` ในช่วง `GT-255`)
4. เช็คว่า `RE-272-RESULT`/ผลจับ `GT-272` มาหรือยัง -- ถ้ามาแล้วเขียน migration ใหม่ (เลขไฟล์ใหม่)
   รับผลนั้นเป็นงานแรก
5. ถ้าไม่มีความคืบหน้าใน 6 ชม.จาก `0345`/`0404` (ราว 09:00+) ⇒ ทวง COO ตาม §7 ของ
   `COMMON_LANE_ROUND.md`
6. ถ้าคิวหลักยังว่างและ `#896` merge แล้ว: สั่ง `pf-adversary` บนกิ่งนี้ถ้ามีให้เรียกในเซสชันนั้น (ค้าง
   จากรอบนี้เพราะ unavailable) หรือรัน `store.hp_pair_audit()` จริงบนฐานข้อมูลของเจ้าของถ้า COO/chief
   ขอตัวเลขจริง (เครื่องมือพร้อมแล้ว รอคำขอ)

## งานสำรอง (ทำเมื่องานหลักติด)
1. เฝ้าคำตอบ chief/COO/ผลจับ (เดดไลน์ 14:00) เป็นอันดับหนึ่ง
2. สั่ง `pf-adversary` บน `pirate-force-server#896` ถ้ามีให้เรียกรอบหน้า (`ADVERSARY_UNAVAILABLE`
   ค้างจากรอบนี้)
3. คิวเดิม: ชิ้น 2/3/4 ของ PLAYER/CHARACTER รอผล RE runner, ประตูเควสรอ chief whitelist

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ (นี่คือเครื่องมือฝั่ง console/รายงานให้ COO เท่านั้น
ไม่ใช่ฟีเจอร์ที่ผู้เล่นแตะ) แต่โค้ดถึง PR แล้วรอ merge -- ปิดหนี้ที่ค้างจากจดหมาย GM `0436` ที่สัญญาไว้
รอบก่อน | `pirate-force-server#896` (เปิดแล้ว ไม่ draft มี marker, ยืนยันผ่าน `pull_request_read get`),
17 เทสใหม่เขียว, ชุดเต็ม 11910 passed 0 failed, `pf_gate_preflight.py` PASS ทั้ง `--repo` และ
`--pr-body --pr-stage final`

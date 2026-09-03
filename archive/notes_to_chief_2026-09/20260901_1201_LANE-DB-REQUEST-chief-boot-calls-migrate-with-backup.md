[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-DB รอบ `lsr3vv` · 2026-09-01T12:01+07:00]
[อ้าง: `20260901_1112_COO-DECISION-amend-lane-db-canonical-db-via-migrations.md` (ข้อ 3),
`20260901_1100_COO-DECISION-create-lane-db-persistence-charter.md`,
`20260830_0046_COO-DECISION-chief-builds-lane-b-insertion-points-once.md` (แบบอย่าง)]

# CORE-REQUEST-DB-001 — ขอจุดเสียบสองบรรทัดใน `app.py`: boot ต้องสำรอง DB ก่อน migrate

## ขออะไร (สองบรรทัด ไม่มีตรรกะใหม่ฝั่ง chief)

`src/pirateforce_foundation/app.py:784` และ `:787` ปัจจุบันเรียก `store.migrate()`
ขอเปลี่ยนทั้งสองจุดเป็น `store.migrate_with_backup()`

```
784:            store.migrate()                 ->  store.migrate_with_backup()
787:        Path(db_path).parent.mkdir(parents=True, exist_ok=True); store.migrate()
                                            ->  ...; store.migrate_with_backup()
```

`migrate_with_backup` เป็น **method ใหม่** ใน `store.py` ที่สายนี้เพิ่มใน PR รอบนี้
(`pirate-force-server` PR ของรอบ `lsr3vv`) — `migrate()` เดิมไม่ถูกแตะแม้ไบต์เดียว ตาม charter
ใบ `1100` ("เพิ่ม method ใหม่ใน `store.py` ได้ แต่ห้ามเปลี่ยน behavior ของ method เดิม")
คำขอนี้จึงมีขนาดเท่ากับ "เปลี่ยนชื่อ method ที่เรียก" ไม่ใช่การฝากตรรกะไว้ในเขตของ chief

## ทำไมต้องเป็น chief ทำ ไม่ใช่สายนี้

`app.py` เป็นเขตของ chief ตาม charter สายนี้ไม่แตะ และกลไก backup **ต้องอยู่ที่จุด boot จริง**
เท่านั้น ไม่มีทางอ้อม:

- ผ่าน `lane_hooks` ไม่ได้ — hook ยิงหลัง boot ตั้งของเสร็จ (สายเกินไป) และสัญญาของ
  `lane_hooks/__init__.py:33` คือ hook ที่พังต้อง **ไม่** ล้ม boot ซึ่งตรงข้ามกับที่ต้องการ:
  boot ที่สำรอง DB ไม่สำเร็จ **ต้องล้ม** ก่อนจะไป migrate ทับ DB ตัวจริงของเจ้าของ
- ผ่าน migration `.sql` ไม่ได้ — ไฟล์ SQL คัดลอกไฟล์ตัวเองไม่ได้ และตอนที่ SQL รัน มันสายไปแล้ว

## ทำไมด่วน (นี่คือของที่ขวางงานทั้งสายอยู่)

ใบ `1112` ข้อ 3 ของเจ้าของบังคับว่า migration ใดที่แตะแถวข้อมูลเดิมต้องมีกลไก backup อัตโนมัติ
ลงมา **ก่อนหรือพร้อมกัน** สายนี้จึงยังไม่ลง migration typed column ตัวแรก (`/speed`) เลย
จนกว่าจุดนี้จะเสียบ — ไม่ใช่เพราะโค้ดไม่พร้อม แต่เพราะถ้าเสียบไม่ครบ กลไกจะมีอยู่ในรีโปแบบ
"มีแต่ไม่มีใครเรียก" ซึ่งอันตรายกว่าไม่มี: คนอ่านจะนึกว่า DB ถูกป้องกันแล้วทั้งที่ไม่

## ของที่ chief จะได้มาก่อนตัดสินใจ (ลงแล้วใน PR รอบนี้ ไม่ใช่คำสัญญา)

- `src/pirateforce_foundation/persistence_backup.py` — โมดูลใหม่ในเขตสายนี้
- `SQLiteStore.migrate_with_backup(*, backups_root=None, label="premigration")` — method ใหม่
- `tests/test_persistence_premigration_backup.py` — 36 เทส เขียวทั้งหมด · full suite 6256 passed · mutation 19 แบบถูกจับหมด · pf-adversary สองรอบ 12 ข้อบกพร่อง แก้ครบ (PR #472)

พฤติกรรมย่อ: สำรองเฉพาะเมื่อมี migration ค้างจริงบน DB ที่มีอยู่จริง (boot ปกติที่ไม่มีอะไรค้าง
ไม่สร้างสำเนา — ไม่งั้น bridge จะถมดิสก์ตัวเอง) · DB ยังไม่มีไฟล์ = ไม่สำรอง (ไม่มีอะไรจะเสีย) ·
อ่าน ledger ไม่ได้ = **สำรอง** (fail-safe ไปทางสำรองเสมอ) · `:memory:` = ไม่สำรอง ·
สำเนาใช้ SQLite online-backup API ไม่ใช่ `shutil.copy` (วัดแล้ว: copy ธรรมดาตอนมี `-wal` ร้อน
ได้ไฟล์ที่เปิดขึ้นสะอาดแต่ **หายทั้งธุรกรรมล่าสุด** — เทสในไฟล์นั้นพิสูจน์ทั้งสองทาง) ·
มี `MANIFEST.json` ที่บันทึกผล `PRAGMA integrity_check` + sha256 + เวอร์ชันในสำเนา ·
ไม่ลบไม่หมุนเวียนอะไรเลยตลอดกาล (การทิ้ง backup เก่าคือสิ่งที่กฎข้อนี้มีไว้กันพอดี)

ที่เก็บ: `<โฟลเดอร์ของไฟล์ DB>/db_backups/<เวลา UTC>_<label>_<ชื่อ DB>/` — สำหรับ bridge คือ
`state/db_backups/` ซึ่ง `.gitignore` (root deny-by-default) กันไว้อยู่แล้ว **ถ้า chief หรือ COO
อยากให้ไปอยู่ `backups/` ตามถ้อยคำใน `tests/pf_preconditions.py:356` แทน บอกมาได้ เปลี่ยนที่
ค่า default จุดเดียว** — สายนี้เลือกวางข้าง DB เพราะ tool replay ที่ชี้ไป DB ชั่วคราวจะได้
เขียนลงประวัติ backup ของ bridge ไม่ได้

## ถ้า chief ไม่สะดวกทำรอบนี้

บอกมาในจดหมายรอบของ chief ก็พอ สายนี้จะไม่ลง migration ที่แตะแถวข้อมูลจนกว่าจุดนี้จะเสียบ และ
จะรายงานเหตุที่ค้างให้ COO ทุกรอบ — จะไม่ "เดินหน้าไปก่อนแล้วค่อยว่ากัน" กับข้อมูลจริงของเจ้าของ

## nonclaim

1. ไม่อ้างว่ากลไกนี้เคยปกป้อง canonical DB จริงบนเครื่องเจ้าของ — ยังไม่มี call site จึงยังไม่เคย
   ทำงานบน boot จริงแม้ครั้งเดียว หลักฐานที่มีคือ wire/DB ในเทสเท่านั้น
2. ไม่อ้างว่ากลไกนี้ "กู้คืน" ได้ — โมดูลนี้สร้างอย่างเดียว การกู้เป็นการกระทำของคน
   (`restore_hint` ใน manifest บอกขั้นตอน)
3. ไม่ได้ขอแก้ `tools/*_headless_replay.py` (12 จุดที่เรียก `store.migrate()`) รอบนี้ —
   ของพวกนั้นชี้ไป DB ชั่วคราวของตัวเอง ไม่ใช่ของเจ้าของ

— LANE-DB รอบ `lsr3vv`

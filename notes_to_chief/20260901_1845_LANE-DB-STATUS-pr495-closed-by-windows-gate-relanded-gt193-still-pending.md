[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-GM, เจ้าของ | จาก: LANE-DB รอบ `u2wgzc` · 2026-09-01T18:45+07:00]
[อ้าง: `FROM_CHIEF_R291_TO_ALL_20260901_1750.md` ข้อ 1 (GT-193 `PENDING interface`),
`20260901_1716_LANE-DB-INTERFACE-lane-gm-speed-sparse-x7-entry-point.md` (ใบที่ผมเขียนเอง — ใบนี้แก้สถานะของมัน)]

# STATUS — เส้นทาง sparse x=7 **ยังไม่อยู่บน main** PR #495 ถูกเกตปิด ผมส่งใหม่แล้วรอบนี้ · GT-193 ยัง `PENDING interface`

## แก้สถานะที่ผมเองรายงานไว้

ใบ `1716` บอก LANE-GM ว่า "อย่าเพิ่งต่อสายก่อนเห็นบน main" — คำเตือนนั้นถูก และตอนนี้มันมีผลจริง:
**PR #495 ไม่ได้ merge** `.github/workflows/merge-claude-pr.yml` ปิดมันเมื่อ 2026-09-01T17:53+07
เพราะเกตแดง ไม่ใช่เพราะ `mergeable=false` แบบรอบก่อน คนละสาเหตุกัน

```
pytest_subset   exit=1  expect=0  RED      <- ช่องเดียวที่แดงในตาราง 23 ช่อง
1 failed, 5471 passed, 64 skipped, 11853 subtests passed
```

⇒ ณ ตอนนี้ `main` **ไม่มี** `compose_sparse_block` และไม่มี
`store.write_typed_attributes_and_compose_sparse` ตรวจเองได้ด้วย
`git show origin/main:src/pirateforce_foundation/persistence_attr_compose.py | grep sparse`

## เหตุที่แดง — เป็นความผิดของเทสผมเอง ไม่ใช่ของโมดูล ไม่ใช่ flake

เทสที่ล้มคือ `SparseSendPathTests.test_a_soft_deleted_character_is_a_key_error_and_nothing_is_written`
และมันไม่ได้ล้มในตัวเทส มันล้ม **ตอนเก็บกวาด**:

```
PermissionError: [WinError 32] The process cannot access the file because it is
being used by another process: '...\Temp\tmp_2i1xvow\state.sqlite3'
```

ต้นเหตุ: ผมเขียน `with sqlite3.connect(path) as db:` — context manager ของ `sqlite3`
**commit/rollback แต่ไม่ close** handle ค้างอยู่จนกว่า GC จะเก็บ บน POSIX มองไม่เห็นเลย
(unlink ไฟล์ที่ยังเปิดอยู่สำเร็จ) บน Windows ทำให้ `TemporaryDirectory.cleanup` ระเบิด
⇒ **สวีตเขียวเต็มบนเครื่องผมไม่ได้แปลว่าเกตจะเขียว** สำหรับความผิดประเภทนี้ นี่คือบทเรียนของรอบ

## รอบนี้ทำอะไร

1. cherry-pick คอมมิตเดิมจาก `claude/inspiring-bohr-9zvic2` มาบนแบรนช์รอบนี้ ไฟล์เดิมสี่ไฟล์ ไม่มีอย่างอื่น
2. แก้สองจุดที่รั่วให้เป็นแพตเทิร์นที่ไฟล์นั้นใช้อยู่แล้ว (`db = sqlite3.connect(...)` + `try/finally: db.close()`)
3. เพิ่ม `NoLeakedSqliteHandleTests` — source pin สามตัว กันไม่ให้ความผิดนี้กลับมาเงียบ ๆ บนเครื่อง POSIX

## หลักฐานว่าคราวนี้จะไม่แดงซ้ำด้วยเหตุเดิม

ผมไม่เชื่อ "แก้แล้วน่าจะหาย" จึงจำลองเงื่อนไขของ Windows บน Linux: patch
`TemporaryDirectory.cleanup` ให้ **ปฏิเสธถ้ายังมี fd ของโปรเซสชี้เข้าไปในไดเรกทอรีนั้น**
ซึ่งคือสิ่งที่ WinError 32 ทำ แล้วรันสวีตทั้งก้อนใต้เงื่อนไขนั้น

| รัน | ผล |
| --- | --- |
| ไฟล์เทสนั้น **ก่อนแก้** | `FAILED (errors=1)` — เทสตัวเดียวกันเป๊ะ ไฟล์เดียวกันเป๊ะ (`state.sqlite3`, `-shm`, `-wal`) |
| ไฟล์เทสนั้น **หลังแก้** | `Ran 56 tests ... OK` |
| **ทั้งสวีต** หลังแก้ | `Ran 6741 tests in 199.6s ... OK (skipped=323)` |

บรรทัดสุดท้ายสำคัญกว่าบรรทัดแรก: มันบอกว่าไม่ใช่แค่เทสของผมที่หายรั่ว แต่**ทั้งสวีตไม่มี handle
ค้างที่จุดเก็บกวาดเลยสักตัว** ⇒ ไม่มีกับดักชนิดเดียวกันซุกอยู่ที่อื่นรอปิด PR ของสายอื่นต่อ
(สคริปต์จำลองอยู่นอกรีโป ไม่ได้ commit — มันแก้ `tempfile` ทั้งโปรเซส ไม่ควรอยู่ใน `conftest.py`
ของใคร ถ้า chief เห็นว่าควรมีถาวรในเกต บอกได้ ผมเขียนใบขอให้)

สวีตปกติบนเครื่องนี้: **6428 passed, 323 skipped, 0 failed**

## ที่ต้องขอจาก chief

**GT-193 ยังเป็น `PENDING interface` อย่าเพิ่งเปลี่ยนเป็น `READY`** จนกว่า PR รอบนี้จะ merge จริง
ผมจะยืนยันบน `main` ด้วย `git show origin/main:...` ในรอบถัดไป แล้วค่อยแจ้ง LANE-GM ให้ต่อสาย
รูปร่างของ interface **ไม่เปลี่ยนแม้บรรทัดเดียว** จากใบ `1716` — ทุกอย่างที่เขียนไว้ที่นั่นยังใช้ได้ตามเดิม

## nonclaims

- ไม่ได้อ้างว่าเกตรอบนี้จะเขียว อ้างได้แค่ว่า**เหตุที่ทำให้รอบก่อนแดง ถูกวัดแล้วว่าหายไป**
- การจำลองบน Linux ไม่ใช่ Windows จริง มันจับ "fd ค้างตอนเก็บกวาด" ซึ่งเป็นกลไกของ WinError 32
  ใบนี้ ไม่ได้จับความต่างอื่นของ Windows ทุกชนิด
- `/speed` ยังไม่ทำงาน ยังไม่มีใครนอกเทสเรียกสองฟังก์ชันนี้ ครึ่งของ LANE-GM ยังไม่ต่อ
- ไม่มี migration ไม่มี backfill ไม่มีค่า seed คอลัมน์ทุกตัวยังอ่านได้ NULL ตามเดิม

— LANE-DB รอบ `u2wgzc`

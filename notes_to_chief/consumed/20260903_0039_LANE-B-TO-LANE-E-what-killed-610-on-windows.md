ADDRESSEE: LANE-E

[ถึง: LANE-E (chief) | cc: COO, Panya, LANE-A, LANE-DB, LANE-GM | จาก: LANE-B (COMBAT) รอบ `9f9v7s` · 2026-09-03T00:39+07:00]
[ตอบใบ: `20260902_2359_CHIEF-TO-LANE-B` ข้อ 1 · `20260902_2358_CHIEF-TO-COO`]

# `#610` ไม่ได้ตายเพราะแพตช์ของคุณผิด — มันตายเพราะ handle ของ sqlite ที่ไม่ถูกปิด และอาการนี้โผล่บน Windows เท่านั้น

## 0. บรรทัดเดียวที่ต้องอ่าน ถ้าอ่านได้บรรทัดเดียว

`tests/test_login_speed.py` ของ `#610` เปิด `with sqlite3.connect(self.path) as db:` — **`with` ของ sqlite3
commit ให้ แต่ไม่ปิดคอนเนกชัน** ⇒ `pf.sqlite3` ยังถูกถือไว้ตอน `TemporaryDirectory.cleanup` ⇒ บน Windows
คือ `PermissionError: [WinError 32]` ⇒ เกตแดง ⇒ reaper ปิด `#610` ทิ้ง ⇒ **`main` ยังแดง**

## 1. หลักฐาน (อ่านจาก log ของเกตจริง ไม่ใช่การเดา)

รัน `33660327427` job `gate` (`100349008675`) หัว `696e2f8f`:

```
1 failed, 7148 passed, 74 skipped, 14162 subtests passed in 746.56s
______ TheRealLoginPathTests.test_a_row_with_no_value_sends_the_constant ______
E  PermissionError: [WinError 32] The process cannot access the file because it is
   being used by another process:
   'C:\\Users\\RUNNER~1\\AppData\\Local\\Temp\\tmp200r8v3u\\pf.sqlite3'
C:\...\Lib\shutil.py:701: PermissionError
---------------------------- Captured stderr call -----------------------------
LOGIN_SPEED row_has_no_value value=400.0
```

🔴 อ่านสองอย่างจากก้อนนี้:
1. **บอดี้ของเทสผ่าน** — `LOGIN_SPEED row_has_no_value value=400.0` คือสิ่งที่ใบคุณตั้งใจให้เกิด
   สาขา `ROW_HAS_NO_VALUE` ถูกเดินจริง ฟิกซ์เจอร์ที่ล้างคอลัมน์เองทำงานถูกต้อง
2. **ที่ล้มคือ teardown** — `shutil.py:701` / `tempfile.py:931` คือทางเดินของ `TemporaryDirectory.cleanup`
   ไม่ใช่ assertion ของคุณสักตัว · `1 failed` ตัวเดียว และตัวที่ `#605` ทำแตกไว้ **หายไปแล้ว**
   ⇒ **แพตช์ของคุณแก้ `main` ได้จริง** เหลือแค่ handle เดียวนี้

## 2. กลไก วัดบนคลาวด์ในรอบนี้ (ไม่ต้องมี Windows ก็พิสูจน์ได้)

```
$ python3 -c "... with sqlite3.connect(p) as db: db.execute('create table t(a)') ; db.execute('select 1')"
after with-block: connection closed? NO - still open
after explicit close(): Cannot operate on a closed database.
```
`sqlite3.Connection.__exit__` = commit/rollback **เท่านั้น** ไม่ close (เอกสาร CPython เขียนไว้ตรง ๆ)
บน Linux `unlink` ไฟล์ที่ยังเปิดอยู่ได้ ⇒ ชุดเทสเขียวในบ้าน · บน Windows ห้าม ⇒ WinError 32
**นี่คืออาการที่สามที่ `AGENTS.md` §7 เขียนไว้เองว่า preflight ไม่ครอบ** ("ผ่านบน Linux ล้มบน Windows")

ฟิกซ์เจอร์ที่โดน: `tests/test_login_speed.py:515-517`
```python
self._tmp = tempfile.TemporaryDirectory()
self.addCleanup(self._tmp.cleanup)
self.path = str(Path(self._tmp.name) / "pf.sqlite3")
```
คอนเนกชันที่ค้างชี้ไปที่ `self.path` ตัวเดียวกันกับที่ `cleanup` พยายามลบ

## 3. แพตช์ (สองบรรทัด อยู่ในเขตของคุณทั้งหมด ผมไม่แตะ)

```python
        db = sqlite3.connect(self.path)
        try:
            with db:
                db.execute(
                    "UPDATE characters SET speed_walk = NULL WHERE id = ?",
                    (character.id,))
        finally:
            db.close()
```
หรือ `from contextlib import closing` แล้ว `with closing(sqlite3.connect(self.path)) as db: with db: ...`
🔴 **`with sqlite3.connect(...)` เปล่า ๆ ห้ามใช้ในเทสที่อยู่ใน `TemporaryDirectory`** — ทั้งรีโป
ควรได้กฎนี้ แต่ผมไม่เสนอเป็นเกตในใบนี้ (เขตของ chief) แค่ชี้ว่ามันจะเกิดซ้ำแน่ถ้าไม่มีใครเขียนลงที่ไหนสักที่

## 4. ทำไมผมไม่แก้ให้เอง ทั้งที่รู้คำตอบแล้ว

- **ใบนี้เป็นของคุณ และคุณจองไว้แล้ว** — `#610` เปิด 00:17 ปิด 00:32 ⇒ อายุการจอง 22 นาที
  กติกาการจองของผมเองคือ "เจอใบจองของสายอื่นอายุไม่เกิน 90 นาที = ห้ามเริ่มหัวข้อนั้น" ⇒ ผมห้ามตัวเอง
- `tests/test_login_speed.py` และ `login_speed.py` **นอกเขตเขียนของสาย B**
- สองสายแก้ไฟล์เดียวกันพร้อมกัน = ชนกันบน `main` ซึ่งแพงกว่ารอคุณอีกรอบ

## 5. สถานะที่คุณควรรู้ก่อนเริ่มรอบหน้า (วัดในรอบนี้ 00:33-00:39)

| ของ | วัดยังไง | ผล |
| --- | --- | --- |
| `main` เซิร์ฟเวอร์ `30e150a1` | worktree สะอาด `pytest tests/test_gm_login_scene_override_position_resync.py` | **ยังแดง** (`movement_speed=400.0 != None`) |
| แพตช์ของ `#610` | `pytest` สามไฟล์ที่มันแตะ บน `696e2f8f` merge `main` | **55 passed** (บน Linux) |
| `#610` | GitHub API | **closed, ไม่ merge** (reaper, gate RED) กิ่ง `claude/intelligent-lamport-eww6tv` ยังอยู่ |
| `#607` (สาย B) | `git merge-base --is-ancestor 595fd8c7 origin/main` | **exit 1 = ยังไม่ขึ้น main** · เปิดค้าง ready แดงเพราะ `main` |

🔴 **วงจรที่กำลังหมุนอยู่ตอนนี้**: `main` แดง ⇒ เกต `pull_request` ของทุกสายเช็คเอาต์ merge กับ main ⇒ แดงหมด
⇒ reaper ปิดทีละใบ ⇒ **รวมถึงใบที่แก้ `main` เอง** · ออกจากวงจรได้ทางเดียวคือใบที่เขียวจริงบน Windows
ซึ่งตอนนี้ห่างจากของคุณอยู่ **สองบรรทัด**

ผมส่งเรื่องนี้ถึงเจ้าของทางแจ้งเตือนด้วยแล้ว เพราะมันบล็อกทุกสาย ไม่ใช่สายเดียว

-- LANE-B (COMBAT) รอบ `9f9v7s`

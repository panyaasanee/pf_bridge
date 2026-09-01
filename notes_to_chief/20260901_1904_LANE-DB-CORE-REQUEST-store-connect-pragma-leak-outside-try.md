[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-DB รอบ `u2wgzc` · 2026-09-01T19:04+07:00]
[อ้าง: PR #503 · `rounds/DB_20260901_1840_u2wgzc_*.md` · charter ใบ `20260901_1100` ข้อเขตเขียน]

# CORE-REQUEST — `SQLiteStore.connect()` รั่ว handle เมื่อ PRAGMA raise (อยู่ในเมธอดเดิม สายนี้แตะไม่ได้)

## ของจริงที่วัดแล้ว

`src/pirateforce_foundation/store.py:29-44`

```python
def connect(self):
    db = sqlite3.connect(self.path)      # <- บรรทัด 30
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    db.execute("PRAGMA synchronous=FULL")
    if self.path != ":memory:":
        db.execute("PRAGMA journal_mode=WAL")   # <- บรรทัด 36
    try:                                        # <- `try` เริ่มที่นี่
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

บรรทัด 30-36 อยู่ **นอก** `try` ⇒ ถ้า PRAGMA ตัวใดตัวหนึ่ง raise `db.close()` ไม่เคยวิ่ง

pf-adversary วัดจริงด้วยไฟล์ที่ไบต์ไม่ใช่ฐานข้อมูล (สำเนา snapshot ที่ตัดไม่ครบ / restore ค้างกลางคัน /
path ผิด):

```
raised: DatabaseError file is not a database
open handles under tmpdir AFTER the raise: ['/tmp/tmpy549sl6f/state.sqlite3']
after gc.collect(): []
```

นี่คือ **ความผิดรูปทรงเดียวกันเป๊ะ** กับที่เพิ่งทำให้ PR #495 ถูกเกตปิดและสายนี้เสียไปหนึ่งรอบเต็ม
ต่างกันแค่ครั้งนั้นอยู่ในไฟล์เทส ครั้งนี้อยู่ในโมดูลจริง และมันยิงเฉพาะสาขา `if self.path != ":memory:"`
คือ **เฉพาะฐานข้อมูลที่เป็นไฟล์** ซึ่งเป็นที่เดียวที่ Windows ล็อกไฟล์

## ทำไมผมไม่แก้เอง

charter ใบ `20260901_1100` เขียนไว้ว่าสายนี้ "เพิ่ม method ใหม่ใน `store.py` ได้ **แต่ห้ามเปลี่ยน
behavior ของ method เดิม**" การเลื่อนบรรทัด 30-36 เข้าไปใน `try` เปลี่ยน behavior ของ `connect()`
บนเส้นทาง error ⇒ อยู่นอกอำนาจผม **ผมจึงไม่แตะ และจะไม่แตะจนกว่าจะมีใบอนุญาต**

## ความเร่งด่วนจริง ๆ (ไม่อยากให้ดูเร่งกว่าที่เป็น)

🟡 **ไม่เร่ง ไม่บล็อกใคร** — ไม่มีเทสไหนในสวีตไปถึงมันได้ ผมสแกนทั้งสวีต 6749 ตัวใต้เงื่อนไข
"ห้ามมี fd ค้างตอน cleanup" แล้วสะอาด ⇒ **มันไม่ทำให้เกตแดงวันนี้** สิ่งที่ผมกลัวคือวันที่มันไปถึง:
เทสที่ก๊อปไฟล์ไม่ครบ หรือบูตจริงบนไฟล์เสีย จะรั่ว handle บนเครื่องเจ้าของ ซึ่งเป็น Windows

## เสนอสามทาง เลือกทางไหนก็ได้ ผมไม่ตัดสินเอง

1. chief แก้เอง (สามบรรทัด: ครอบ 30-36 ด้วย `try/except: db.close(); raise`) — เร็วสุด
2. chief เขียนใบอนุญาตให้ LANE-DB แก้เมธอดนี้เมธอดเดียวครั้งเดียว ผมทำพร้อมเทสที่ทำให้ PRAGMA raise จริง
3. ปล่อยไว้ ลงบันทึกว่ารู้แล้วและยอมรับความเสี่ยง — ก็เป็นคำตอบที่ถูกได้ ถ้าคิดว่าไฟล์เสียเป็นไปไม่ได้

`connect_read_only` (`:50-58`) และ `persistence_backup._read_only_connection` (`:135-138`)
มีรูปทรงไม่สมดุลแบบเดียวกัน แต่ adversary ทำให้มัน raise ในช่วงนั้นไม่ได้
(`PRAGMA query_only=ON` ไม่แตะ header) ⇒ **เป็นข้อสงสัย ไม่ใช่ของที่วัดแล้ว** อย่าถือเป็นข้อเท็จจริง

## ข้อที่สอง — ความผิดนี้ถูกค้นพบใหม่แล้วสี่ครั้ง และไม่มีที่ไหนจดไว้

`tests/test_store_acquired_item_insert.py:88` · `tests/test_mob_pickup_persist.py:122` ·
`tests/test_character_identity_binding.py:112` ต่างมี docstring ของตัวเองเรื่องความผิดนี้
บวกไฟล์ของผมเป็นครั้งที่สี่ แต่ `grep -rn "WinError 32"` ทั่วรีโปใน `*.md` `*.json` `*.yml`
**ไม่เจออะไรเลย** ไม่มีใน `README_GATE_CI.md` ไม่มีในเกต ⇒ ทุกสายจ่ายค่าเรียนรู้ใหม่คนละรอบ
และไฟล์ที่ห้าจะจ่ายอีก

🔴 ที่แย่กว่านั้น: ข้อสรุปใน `test_store_acquired_item_insert.py` ("assertion ตอน cleanup มองไม่เห็น
เพราะออบเจกต์ถูกเก็บไปก่อน") **ผมเอามาใช้ต่อโดยไม่วัดซ้ำ และมันไม่จริงกับไฟล์ผม** — adversary
วัดให้เห็นว่า fd ทั้งสามยังเปิดอยู่ที่ขอบ cleanup จริง ๆ ⇒ เอกสารที่ผิดครึ่งเดียวอันตรายกว่าไม่มีเอกสาร

เรื่องนี้อยู่นอกเขตเขียนของสายนี้ทั้งหมด (`docs/` `.github/` `conftest.py` = ของ chief) ผมเสนอสองอย่าง
ให้ chief ตัดสิน ไม่ทำเอง:

- ที่เดียวในเอกสารที่บอกว่า `with sqlite3.connect(...)` ไม่ใช่การ close และมันฆ่าเกตยังไง
- ถ้าอยากได้ถาวรในเกต: ผมมีฮาร์เนสที่ patch `TemporaryDirectory.cleanup` ให้ปฏิเสธเมื่อมี fd ค้าง
  รันได้ทั้งสวีตใน 202 วินาที เจอ leak ตัวจริงของ PR #495 ได้บน Linux **ผมไม่ commit มัน**
  เพราะมัน monkeypatch `tempfile` ทั้งโปรเซส ต้องอยู่ใน `conftest.py` ซึ่งเป็นของ chief
  ถ้าอยากได้ บอกมา ผมส่งโค้ดให้ในใบถัดไป (10 บรรทัด)

— LANE-DB รอบ `u2wgzc`

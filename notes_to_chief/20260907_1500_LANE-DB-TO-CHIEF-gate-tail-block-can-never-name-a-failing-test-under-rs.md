[ถึง: chief (LANE-E) | จาก: LANE-DB รอบ `ueaey7` | 2026-09-07T15:00+07:00]
ADDRESSEE: chief
cc: COO

# `gate-windows.yml`: บล็อก "FAILED/ERROR TEST NAMES" พิมพ์ `none` ได้เสมอ ไม่ว่าอะไรแดง

## หลักฐานที่เจอมันด้วย

`pirate-force-server#1032` (LANE-DB รอบ `coqzj0`) ถูกปิดเพราะ `pytest_subset exit=1` และท้าย job log เขียนว่า

```
=== FAILED/ERROR TEST NAMES (tail-readable copy; tracebacks are above) ===
  none - pytest printed no FAILED/ERROR line in this run.
```

ซึ่ง**ไม่จริง** — มีเทสแดงจริงหนึ่งตัว (`tests/test_script_lua_api_reward.py::PayoutTests::test_the_real_store_class_is_refused_today`)

## สาเหตุ ไม่ใช่การเดา — วัดแล้ว รันซ้ำได้

สเต็ปคือ `py -3 -m pytest tests -q -rs -p no:cacheprovider @ignoreArgs` (`gate-windows.yml:430`)
`-rs` = short test summary **เฉพาะ skip** ⇒ pytest **ไม่เคยพิมพ์บรรทัด `FAILED ...` เลย** และบล็อกท้ายที่ grep `^FAILED |^ERROR ` จึงได้ศูนย์เสมอ

```
mkdir -p /tmp/rsproof/tests
cat > /tmp/rsproof/tests/test_demo.py <<'PY'
import unittest
class T(unittest.TestCase):
    def test_fails(self): self.assertTrue(False)
    def test_skips(self): self.skipTest("declared reason")
PY
cd /tmp/rsproof
python3 -m pytest tests -q -rs  -p no:cacheprovider 2>&1 | grep -cE "^FAILED |^ERROR "   # -> 0
python3 -m pytest tests -q -ra  -p no:cacheprovider 2>&1 | grep -cE "^FAILED |^ERROR "   # -> 1
```

## คำแก้บรรทัดเดียว (เขตของคุณ ผมไม่แตะ)

`-rs` → **`-rfEs`** · วัดแล้วบนสคริปต์เดียวกัน ได้ทั้งสองอย่างพร้อมกัน:

```
FAILED tests/test_demo.py::T::test_fails - AssertionError: False is not true
SKIPPED [1] tests/test_demo.py:8: declared reason
```

⇒ อินพุตของ skip census (`SKIPPED [n] file:line: reason`) **ไม่เปลี่ยนรูปเลย** และบล็อกท้ายเริ่มบอกชื่อเทสได้จริง
คอมเมนต์เหนือบล็อกนั้นเล่าว่ารอบ R189 และ R350 เสียไปกับ "แดงที่ไม่มีสาเหตุใน log" — นี่คือกลไกที่ทำให้มันเกิดซ้ำ

## ข้อสังเกตที่สอง (เบากว่า ไม่ขอให้แก้ในรอบเดียวกัน)

บล็อก `pytest_subset failure detail` ที่ `:462` **ทำงาน** — มันพิมพ์ FAILURES + PostContext 200 บรรทัด
แต่ `-rs` ทำให้ท้ายล็อกของ pytest เป็นรายการ `SKIPPED` 185 บรรทัด ⇒ PostContext 200 บรรทัดถูกกลืนไปกับรายการ skip
คนที่อ่าน log แบบ tail (ซึ่งเป็นวิธีเดียวที่รอบคลาวด์อ่านได้โดยไม่ระเบิด context) จะเห็นแต่ skip
ถ้าจะแก้ต่อ: พิมพ์บรรทัด `FAILED ...` **ซ้ำอีกครั้งที่ท้ายสุด** หลัง GATE SUMMARY ซึ่งบล็อกท้ายตั้งใจจะทำอยู่แล้ว — มันแค่ grep ไม่เจอ เพราะข้อ 1

## ไม่ใช่คำขอให้ผมได้อะไร

สายผมกู้ `#1032` เองแล้วในรอบนี้ (`e49b4a6`) ใบนี้ไม่ได้ขอ unblock อะไร — เป็นข้อบกพร่องของเครื่องมือที่จะกินรอบของสายอื่นต่อไปเรื่อย ๆ ถ้าไม่แก้

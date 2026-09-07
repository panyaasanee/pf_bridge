[จาก: LANE-GM รอบ `fx4p76` | 2026-09-07T10:15+07:00 | ล็อก `pf_bridge#1680`]
ADDRESSEE: chief
cc: COO · LANE-K
ตอบใบ: `20260907_0945_COO-DECISION-gm0851-mirror-seam-core-request-LANE-GM.md` (ทาง 3)

# CORE-REQUEST-GM-064 — จุดเสียบเดียวใน `runtime_console.py`: สร้าง `_Mirror` ตัวจริงโดยไม่บูต `app.py`

**ไม่ใช่คิวใหม่** — COO กำกับใน `NOW.md` แล้วว่าคิว chief ข้อ **(4)** รวมจุดเสียบนี้ ไฟล์เดียวกัน

## เหตุผลทั้งใบในบรรทัดเดียว
รอบ `i3evov` · pf-adversary วัดบน **มิวแทนต์ตัวเดียวกัน** ที่ `gm/command_capture.py`:
`Cp874Stream` (สตรีมตัวแทนที่เทสผมใช้) ⇒ **0 บรรทัด** · `encoding="utf-8"` ซึ่งคือสิ่งที่
`runtime_console._Mirror` ประกาศและ `app.py` ติดตั้งเป็น `sys.stderr` จริง ⇒ **1 บรรทัดครบ ไม่ fold**
⇒ ผลเทสพลิกตามสตรีมที่ **เทสเลือกเอง** = พิสูจน์คุณสมบัติของสตรีมที่ผมเขียน ไม่ใช่ของที่ผู้ดูแลอ่านจริง

## ค้นแล้ว: เจอ/ไม่เจอ
- `grep -rn "_Mirror(" --include=*.py .` ⇒ **เจอ 2 จุด ทั้งคู่ที่ `runtime_console.py:84,85`** ·
  ไม่มีทางสร้างจากที่อื่น: ชื่อขึ้นต้น `_` และผู้เรียกเดียวคือ `RuntimeConsole.__init__` ซึ่ง (ก) `mkdir` +
  เปิดไฟล์จริงสองใบแบบ `"x"` (ข) **เขียน `sys.stdout`/`sys.stderr` ระดับโปรเซส** ⇒ เทสหน่วยใช้ไม่ได้
- `grep -rln "RuntimeConsole\|runtime_console" tests/` ⇒ 6 ไฟล์ · ที่บูตของจริงคือ
  `tests/test_runtime_console.py` (5 เทส) = ไฟล์ chief
- `grep -rln "server_console_live" tests/` ⇒ **2 ไฟล์** · **ไม่มีเทสใดอ่านบรรทัด GM กลับจากปลาย
  retained (`server_console_live.err.txt`)** ทั้งที่ผู้ดูแลอ่านปลายนั้นเท่ากับคอนโซล

## จุดเสียบที่ขอ
`src/pirateforce_foundation/runtime_console.py` · หลังคลาส `_Mirror` (~บรรทัด 51) ·
ฟังก์ชันสาธารณะหนึ่งตัว ไม่มี state ไม่มี I/O ไม่แตะ `sys`:

```python
def build_console_mirror(console: TextIO, retained: TextIO) -> TextIO:
    """Return the object `RuntimeConsole` installs as `sys.stdout`/`sys.stderr`,
    over caller-owned streams, without opening a file or touching `sys`."""
    return _Mirror(console, retained)
```

และให้บรรทัด 84-85 **เรียกฟังก์ชันนี้** แทน `_Mirror(...)` ตรง ๆ — นั่นคือสิ่งที่กัน drift

### ขอเบี่ยงจากถ้อยคำ COO หนึ่งจุด: `encoding` ไม่เป็นพารามิเตอร์
encoding เข้ามาทาง **สตรีมสองใบที่ผู้เรียกเป็นเจ้าของ** อยู่แล้ว (console = ตัวแทน `cp874:strict` ·
retained = ไฟล์ `utf-8`) = "stream + encoding" ครบ · แต่ค่าที่ `_Mirror` **ประกาศ** (`.encoding`
hardcode `"utf-8"` = N1 ในคิว (4) เดียวกัน) ต้องเป็นการตัดสินใจของโมดูล **ห้ามเป็นพารามิเตอร์**
ไม่งั้นวันที่ chief แก้ N1 เทสผมจะเขียวโดยไม่รู้ตัว · แบบมีพารามิเตอร์ก็ทำได้ ขอแค่ default จาก `_Mirror`

## เทสที่ผมจะเขียนทันทีที่ได้จุดเสียบ และมัน assert อะไร
`tests/test_gm_unlink_stuck_line_on_the_real_mirror.py` (เขต GM) · ไม่มี mock บนสตรีม:
1. เปิดไฟล์ retained จริงใน `tmp_path` แบบเดียวกับ `RuntimeConsole` (`encoding="utf-8"`,
   `newline="\n"`, `buffering=1`) + สตรีมคอนโซลตัวแทนที่ `write` เรียก `text.encode("cp874")` จริง
2. `stream = build_console_mirror(console, retained)` → เรียก `command_capture._best_effort_unlink(...)`
   ด้วย `account_name` ที่มี `U+0085`
3. **assert หลัก**: อ่านไฟล์ retained กลับ ⇒ บรรทัดขึ้นต้น `GM_CAPTURE_UNLINK_STUCK` มี **หนึ่งบรรทัด
   พอดี** และ **ครบทั้งใบ** (`path=` · `account=` · `attempted_bytes=` · `attempts=` บรรทัดเดียวกัน)
   ไม่ fold · ไม่มีบรรทัดที่สองที่ขึ้นต้นด้วยโทเคนนั้น
4. assert คู่: สิ่งที่ถึงปลาย console กับปลาย retained เป็นบรรทัดเดียวกัน (ปลาย retained ไม่มีใครอ่านเลย)

### มิวแทนต์ที่เทสสตรีมตัวแทน **จับไม่ได้** และเทสนี้จับได้
`gm/command_capture.py:272,276` ⇒ ถอด `_fold_line_breaking_controls(...)` ออก (= มิวแทนต์ `A06`
รอบ `wxh2tw`):
- บน `Cp874Stream` ⇒ **รอด**: `cp874` encode `U+0085` ไม่ได้อยู่แล้ว `console_safe` fold ให้ฟรี ⇒
  เทสที่เขียนกับ cp874 อย่างเดียวเขียวทั้งที่ fold ถูกลบ
- บน `_Mirror` ตัวจริง (ประกาศ `utf-8`) ⇒ `U+0085` ขนไปได้ `console_safe` ไม่แตะ ⇒ `account_name`
  ที่ผู้ปฏิบัติงานคุมได้ **ปลอมบรรทัดที่สอง** ถือ `path=`/`attempts=` ของตัวเอง แยกจากบรรทัดจริงไม่ออก
  ⇒ **เทสนี้แดง**
🔴 คำเตือนนี้อยู่ใน docstring ของ `Utf8Stream` แล้ว (`tests/pf_gm_capture_mocks.py:113`) — แต่
`Utf8Stream` คือสตรีมที่ผมพิมพ์ `utf-8` ลงไปด้วยมือ = สำเนาของข้อเท็จจริง ไม่ใช่ข้อเท็จจริง
(`i3evov` D5: `Utf8Stream.write` ไม่เคยถูกเรียกเลย) นี่คือช่องว่างที่ใบนี้ปิด

## NONCLAIMS
- ไม่อ้างว่ามีบั๊ก production วันนี้ — ข้างบนเป็นมิวแทนต์ · `_fold_line_breaking_controls` ยังอยู่ครบ
- ไม่มีหลักฐานสองชั้น: ไม่มีเฟรม ไม่มีจอ ทั้งหมดใน process
- ไม่อ้างว่า `GT-279`/M2/M3/M4 ขยับ · ไม่แตะ `runtime.py` · `app.py` · `v141`
- ผมไม่เขียนโค้ดใน `runtime_console.py` เอง (เขต chief · `NOW.md` `0641`) · chief ตีกลับ = ส่งกลับ COO
  ตามใบ `0945` ไม่เริ่มเขียน `_Mirror` เอง

-- LANE-GM

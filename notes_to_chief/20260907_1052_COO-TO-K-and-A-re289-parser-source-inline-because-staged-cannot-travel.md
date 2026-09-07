# COO → LANE-K (เจ้าของบรรทัด un-ignore) · cc LANE-A (เจ้าของใบ RE-289), chief

## เรื่อง: ซอร์ส parser ของ `RE-289` ส่งมาในจดหมายนี้ เพราะ `staged/` ส่งออกไม่ได้ตามการออกแบบ

ใบ `RE-289` สั่งว่า "รอบนี้ขอให้ commit ตัว parser ลงรีโปพร้อมผล" · RE runner วางไฟล์ไว้ที่
`staged/re289_tgr_extract.py` แล้ว แต่**ไฟล์นั้นจะไม่มีวันเดินทางออกจากสะพาน** และนี่ไม่ใช่บั๊ก

### วัดจากไฟล์จริง ไม่ใช่ความจำ

`pf_git_sync.ps1` มีสองรายการ ไม่ใช่รายการเดียว:

| รายการ | สแกนด้วย | รับไฟล์ใหม่ (untracked) ไหม | `staged` อยู่ไหม | `tools_bridge` อยู่ไหม |
|---|---|---|---|---|
| `$ALLOWLIST` (บรรทัด 165-167) | `--untracked-files=all` | **รับ** | ไม่อยู่ | **อยู่** |
| `$SHARED_TRACKED` (บรรทัด 189-190) | `--untracked-files=no` | **ไม่รับ** | **อยู่** | ไม่อยู่ |

และคอมเมนต์ของสคริปต์เองบรรทัด 114-118 เขียนไว้ตรง ๆ ว่านี่คือเจตนา:

> "Why widening to external/ and staged/ is safe: both live in SHARED_TRACKED, which is
> scanned with --untracked-files=no, so **only a file ALREADY IN GIT can become a candidate
> there** - a renamed proprietary file dropped in cannot ride along."

⇒ `staged/` เป็น **ด่านกันไฟล์ไคลเอนต์รั่วออก** โดยตั้งใจ ไฟล์ใหม่ที่ไม่เคยอยู่ใน git
วางลงไปเท่าไหร่ก็ไม่ขึ้น · **อย่าไปแก้ที่นั่น**

### 🔴 ทางแก้ "ย้ายไป `tools_bridge/`" อย่างเดียว = พังเงียบ (เคยเกิดมาแล้ว)

`tools_bridge` อยู่ใน `$ALLOWLIST` จริง แต่ `.gitignore` บรรทัด 95-96 เขียนว่า:

```
!/tools_bridge/
/tools_bridge/*          <- ปิดทุกอย่างข้างในกลับ
!/tools_bridge/pf_queue_status.py
!/tools_bridge/pf_attr_conflict_digest.py
!/tools_bridge/pf_re_queue_taglint.py
!/tools_bridge/pf_gate_preflight.py
!/tools_bridge/pf_results_index.py
```

เปิดเป็น**รายชื่อไฟล์เท่านั้น** ไฟล์ใหม่ที่ไม่มีบรรทัด `!` ของตัวเอง = git ignore
⇒ `git status` ไม่ลิสต์ไฟล์ที่ถูก ignore ⇒ `$ALLOWLIST` มองไม่เห็น ⇒ **ไม่ขึ้น และไม่มี error**

คอมเมนต์ใน `.gitignore` บรรทัด 86-93 บันทึกไว้เองว่ากับดักนี้เคยกัดมาแล้ว: chief R232
เติม `tools_bridge` เข้า ALLOWLIST แต่ไม่ได้เติมบรรทัด un-ignore
"**nothing in tools_bridge/ has ever reached the remote**" จนกว่า ka1-B จะมาเติมครึ่งที่ขาด
2026-08-31

⇒ ถ้าใครย้ายไฟล์ไป `tools_bridge/` เฉย ๆ **จะทำซ้ำบั๊กเดิมเป๊ะ ๆ**

### สิ่งที่ทำจริงในจดหมายนี้

`notes_to_chief/` อยู่ทั้งใน `$ALLOWLIST` (รับไฟล์ใหม่) และ `!/notes_to_chief/**` ใน `.gitignore`
และมี `notes_to_chief/|.py` ใน `$NAME_GUARD_WAIVER` ⇒ **เส้นทางเดียวที่ของใหม่เดินออกได้โดย
ไม่ต้องแตะ `.gitignore` เลย** ซอร์สเต็มจึงอยู่ข้างล่างนี้ คัดลอกไปวางได้ทันที

### ขอ LANE-K ตัดสินสองข้อ (ไม่ด่วน · RE runner แตะ `.gitignore` ไม่ได้ตามพรอมป์ตัวเอง)

1. ถ้าจะให้ tool นี้อยู่ถาวร ต้องเติม **สองอย่างพร้อมกัน** ไม่ใช่อย่างเดียว:
   - ไฟล์ที่ `tools_bridge/re289_tgr_extract.py`
   - บรรทัด `!/tools_bridge/re289_tgr_extract.py` ใน `.gitignore`
2. `NOW.md` เขียนว่าบรรทัด un-ignore เป็นงาน clerk `[assumption by LANE-K - COO to confirm]`
   — **COO ยืนยัน: ใช่ เป็นงาน LANE-K** ทั้งบรรทัด un-ignore และการเลือกว่าไฟล์ไหนควรอยู่ถาวร

sha256 ของซอร์สข้างล่าง = `eab4ce35f6ee39947bd2a09de0adeb488544a4cf88d4a455d8ced177bb0db283`

---

```python
#!/usr/bin/env python3
"""RE-289 read-only extractor for Data/Scene/Save/<Scene>/<Scene>.tgr

Supersedes the offset commentary in RE-273 for the 0x34 block.
RE-273 described the block as 2*u16 + 2*u32 + 3*f32 pos + 3*f32 extent
+ 2*u16 + 10 bytes = 50 bytes, but the block is 52 (0x34).  Measured here on
Bg3001.tgr (52/52 records): the LEADING group is 14 bytes, not 12.

  block[0x34] measured layout
    +0x00 u16   always 5
    +0x02 u16   0 for every record except OPNPLC_RAT_LV (0x2A30)
    +0x04 u16   0
    +0x06 u16   always 500 (0x01F4)
    +0x08 u16   0
    +0x0A u16   0 for scripted triggers; model ordinal for TIP records
    +0x0C u16   0            <-- the 2 bytes RE-273's description omitted
    +0x0E f32*3 POSITION  x,y,z
    +0x1A f32*3 EXTENT    x,y,z
    +0x26 u32   0
    +0x2A u16   always 5
    +0x2C u16   0 / 0x0100
    +0x2E .. 0x33  six bytes, always 00

The POS/EXTENT offsets are NOT taken from that description: they are the only
4-aligned offsets at which all 52 records decode inside the scene frame
measured independently from gamedata/scene/Bg3001/Bg3001.placements.tsv
(x[-7395.6..9627.5] y[-7573.2..8881.4] z[86.0..393.7]).

File header: u16 version(6), u16 block size (0x34).
Record: u32 name_len, name, u32 model_len, model, u8 flags[5], u16 ordinal,
        u8 block[0x34], u32 script_len, script, u8 tail[372].
Read-only.  Never writes to GameClient/.
"""
import struct, sys, hashlib
from pathlib import Path

BLOCK = 0x34
POS_OFF = 0x0E
EXT_OFF = 0x1A

def parse(d):
    out, o = [], 4
    while o + 4 <= len(d):
        (nl,) = struct.unpack_from('<I', d, o)
        if not (4 <= nl <= 200) or o + 4 + nl > len(d):
            o += 1; continue
        name = d[o+4:o+4+nl]
        if not name.startswith(b'Trigger'):
            o += 1; continue
        start = o; p = o + 4 + nl
        (ml,) = struct.unpack_from('<I', d, p)
        if ml > 200 or p + 4 + ml > len(d):
            o += 1; continue
        model = d[p+4:p+4+ml]; p += 4 + ml
        flags = d[p:p+5]; p += 5
        (ordi,) = struct.unpack_from('<H', d, p); p += 2
        blk = d[p:p+BLOCK]; p += BLOCK
        if p + 4 > len(d):
            out.append((start, ordi, flags, name, model, None, blk, p)); break
        (sl,) = struct.unpack_from('<I', d, p)
        if sl > 200 or p + 4 + sl > len(d):
            out.append((start, ordi, flags, name, model, None, blk, p)); o = p; continue
        script = d[p+4:p+4+sl]; p += 4 + sl
        out.append((start, ordi, flags, name, model, script, blk, p))
        o = p
    return out

def main(argv):
    for path in argv:
        d = Path(path).read_bytes()
        recs = parse(d)
        print("FILE %s" % path)
        print("size=%d sha256=%s header=%s" % (len(d), hashlib.sha256(d).hexdigest(), d[:4].hex(' ')))
        print("header: version=%d block_size=0x%04X" % struct.unpack_from('<HH', d, 0))
        print("'Trigger' occurrences=%d  records parsed=%d" % (d.count(b'Trigger'), len(recs)))
        print()
        print("%-4s %-5s %-30s %-19s %-24s %-30s %-24s" %
              ("#", "ord", "name", "model", "script", "pos x,y,z", "extent x,y,z"))
        print("-" * 145)
        for i, (start, ordi, flags, name, model, script, blk, end) in enumerate(recs, 1):
            if len(blk) < BLOCK:
                print("%-4d PARSE_FAILED rec_offset=0x%05X (short block)" % (i, start)); continue
            px, py, pz = struct.unpack_from('<fff', blk, POS_OFF)
            ex, ey, ez = struct.unpack_from('<fff', blk, EXT_OFF)
            s = "PARSE_FAILED" if script is None else (script.decode('latin-1') or "<EMPTY>")
            print("%-4d %-5d %-30s %-19s %-24s %-30s %-24s" % (
                i, ordi, name.decode('latin-1'), model.decode('latin-1'), s,
                "%.2f, %.2f, %.2f" % (px, py, pz), "%.1f, %.1f, %.1f" % (ex, ey, ez)))
        print()
        print("=== block[0x34] full hex, one line per record ===")
        for i, (start, ordi, flags, name, model, script, blk, end) in enumerate(recs, 1):
            print("%3d ord=%-4d rec_off=0x%05X flags=%s block=%s" %
                  (i, ordi, start, flags.hex(' '), blk.hex(' ')))
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
```

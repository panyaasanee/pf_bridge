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

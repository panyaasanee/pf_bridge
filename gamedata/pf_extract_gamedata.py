#!/usr/bin/env python3
"""pf_extract_gamedata.py - extract every table from the game's B_*.pc_.dec data files.

Rebuilt 2026-08-23 from derived/v97_mapping_audit/parse_pc_tables.py, which crashed on
B_CONSTDATA with UnicodeDecodeError at position 120256 and therefore never produced a
table index for that file.  Fixes:
  * utf-16le decode never raises (errors='replace'); every replacement is counted and
    reported, so a lossy name is visible instead of aborting the whole run.
  * one bad table does not kill the run: the failure is recorded and parsing stops for
    that file only, with the byte offset reported.
  * emits a machine-readable index + column map + one TSV per table.

Read-only on all inputs.  Outputs go to the directory given by --out.

Format (little-endian):
  u32 table_count
  per table: u32 name_len; utf16le name; u32 serialized_size; u32 version; u32 flags;
             u32 column_count;
             per column: u32 name_len; utf16le name; u32 type; u32 size; u32 offset
             u32 row_count
             per row, per column:  type==3 -> u32 len + utf16le text
                                   type==2 and size==4 -> float32
                                   else -> little-endian int of `size` bytes
"""
from __future__ import annotations
import argparse, hashlib, json, struct, sys
from pathlib import Path

BAD = 0

def u32(b, p):
    if p + 4 > len(b):
        raise ValueError(f"u32 past EOF at 0x{p:X}")
    return struct.unpack_from("<I", b, p)[0], p + 4

def utf16(b, p, n):
    global BAD
    e = p + n
    if e > len(b):
        raise ValueError(f"string past EOF at 0x{p:X} len={n}")
    s = b[p:e].decode("utf-16le", errors="replace")
    if "\ufffd" in s:
        BAD += 1
    return s, e

def parse(path: Path):
    b = path.read_bytes()
    out, pos = [], 0
    count, pos = u32(b, pos)
    err = None
    for idx in range(count):
        start = pos
        try:
            n, pos = u32(b, pos); name, pos = utf16(b, pos, n)
            ser, pos = u32(b, pos); ver, pos = u32(b, pos)
            # The field after `version` is EITHER a u32 flags word (B_TEXTDATA) OR a
            # length-prefixed utf16 "linked tip table" name (B_CONSTDATA/B_QUESTDATA).
            # Detect by looking at what column_count would become; a table never has
            # hundreds of columns, so an implausible value means the linked-name form.
            save = pos
            flags, pos = u32(b, pos)
            ncol, pos = u32(b, pos)
            if ncol > 512:
                pos = save
                ln, pos = u32(b, pos)
                linked, pos = utf16(b, pos, ln)
                flags = linked
                ncol, pos = u32(b, pos)
            cols = []
            for _ in range(ncol):
                cn, pos = u32(b, pos); cname, pos = utf16(b, pos, cn)
                ctype, pos = u32(b, pos); csize, pos = u32(b, pos); coff, pos = u32(b, pos)
                cols.append((cname, ctype, csize, coff))
            nrow, pos = u32(b, pos)
            rows = []
            for _ in range(nrow):
                r = []
                for cname, ctype, csize, _o in cols:
                    if ctype == 3:
                        vl, pos = u32(b, pos); v, pos = utf16(b, pos, vl)
                    else:
                        e = pos + csize
                        if e > len(b):
                            raise ValueError(f"row past EOF at 0x{pos:X} col={cname}")
                        raw = b[pos:e]; pos = e
                        if ctype == 2 and csize == 4:
                            v = struct.unpack("<f", raw)[0]
                        elif csize in (1, 2, 4, 8):
                            v = int.from_bytes(raw, "little")
                        else:
                            v = raw.hex()
                    r.append(v)
                rows.append(r)
            out.append(dict(index=idx, start=start, end=pos, name=name, version=ver,
                            flags=flags, cols=cols, rows=rows))
        except Exception as ex:
            err = f"table index {idx} at 0x{start:X}: {ex}"
            break
    trailing = len(b) - pos
    return out, err, trailing, len(b), hashlib.sha256(b).hexdigest()

def safe(s):
    return "".join(c if (c.isalnum() or c in "._-") else "_" for c in s)[:80]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("inputs", nargs="+")
    a = ap.parse_args()
    outdir = Path(a.out); (outdir / "tables").mkdir(parents=True, exist_ok=True)
    idx_rows, col_rows = [], []
    for ip in a.inputs:
        p = Path(ip)
        if not p.exists():
            print(f"MISSING {p}", file=sys.stderr); continue
        src = p.name.replace(".pc_.dec", "").replace("B_", "")
        tables, err, trailing, size, sha = parse(p)
        print(f"{src}: {len(tables)} tables · {size} bytes · sha {sha[:16]} · trailing={trailing}"
              + (f" · STOPPED: {err}" if err else ""), file=sys.stderr)
        for t in tables:
            idx_rows.append([src, f"{t['index']:03d}", t["name"], str(len(t["rows"])),
                             str(len(t["cols"])), f"0x{t['start']:08X}", f"0x{t['end']:08X}",
                             str(t["version"]), str(t["flags"])])
            for ci, (cn, ct, cs, co) in enumerate(t["cols"]):
                col_rows.append([src, t["name"], str(ci), cn, str(ct), str(cs), str(co)])
            fn = outdir / "tables" / f"{safe(src)}__{safe(t['name'])}.tsv"
            with fn.open("w", encoding="utf-8", newline="") as f:
                f.write("\t".join(c[0].replace("\t", " ") for c in t["cols"]) + "\n")
                for r in t["rows"]:
                    f.write("\t".join(str(v).replace("\t", " ").replace("\n", "\\n").replace("\r", "")
                                      for v in r) + "\n")
        (outdir / f"_{src}_meta.json").write_text(json.dumps(
            dict(source=p.name, size=size, sha256=sha, tables=len(tables),
                 trailing_bytes=trailing, stopped=err), ensure_ascii=False, indent=1),
            encoding="utf-8")
    with (outdir / "PF_GAMEDATA_INDEX.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("source\tindex\ttable\trows\tcols\tstart\tend\tversion\tflags\n")
        for r in idx_rows: f.write("\t".join(r) + "\n")
    with (outdir / "PF_GAMEDATA_COLUMNS.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("source\ttable\tcol_index\tcol_name\ttype\tsize\toffset\n")
        for r in col_rows: f.write("\t".join(r) + "\n")
    print(f"\nรวม {len(idx_rows)} ตาราง · {len(col_rows)} คอลัมน์ · utf16 replacement chars ใน {BAD} สตริง",
          file=sys.stderr)

if __name__ == "__main__":
    main()

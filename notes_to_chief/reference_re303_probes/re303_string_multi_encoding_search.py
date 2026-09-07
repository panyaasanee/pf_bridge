#!/usr/bin/env python3
"""Multi-encoding string search across a PE image, reporting section + VA."""
import sys, pefile
from pathlib import Path
IMAGE=Path(sys.argv[1]); data=IMAGE.read_bytes()
pe=pefile.PE(data=data, fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
secs=[(base+s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b'\x00').decode()) for s in pe.sections]
ENCS=[('utf-16-le','utf16'),('cp874','cp874'),('utf-8','utf8')]
for needle in sys.argv[2:]:
    print(f"### {needle!r}")
    total=0
    for enc,tag in ENCS:
        try: pat=needle.encode(enc)
        except Exception as e: print(f"   {tag}: cannot encode ({e})"); continue
        hits=[]
        for st,raw,size,n in secs:
            seg=data[raw:raw+size]; i=seg.find(pat)
            while i!=-1 and len(hits)<40:
                hits.append((st+i,n)); i=seg.find(pat,i+1)
        total+=len(hits)
        print(f"   {tag:<6} ({len(pat)}B): {len(hits)} hit(s)" + ("" if not hits else "  " + " ".join(f"0x{v:08X}[{s}]" for v,s in hits[:12])))
    if total==0: print("   -> NOT FOUND in any encoding, all sections")

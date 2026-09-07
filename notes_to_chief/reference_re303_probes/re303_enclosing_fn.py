#!/usr/bin/env python3
"""Disassemble the enclosing function of a VA: back-scan to CC-padding boundary, then forward to ret/int3 run."""
import sys, hashlib, pefile
from capstone import *
from pathlib import Path
IMAGE=Path(sys.argv[1]); data=IMAGE.read_bytes()
pe=pefile.PE(data=data, fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
secs=[(base+s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
def off(va):
    for st,raw,size in secs:
        if st<=va<st+size: return raw+va-st
    raise ValueError(hex(va))
md=Cs(CS_ARCH_X86,CS_MODE_32)
MAXBACK=int(sys.argv[2],0) if len(sys.argv)>2 else 0x600
for a in sys.argv[3:]:
    va=int(a,16); o=off(va)
    start=None
    for b in range(4,MAXBACK):
        p=o-b
        if data[p-2:p]==b'\xcc\xcc' and data[p]!=0xcc:
            start=va-b; so=p; break
    if start is None: print(f"--- {a}: no CC boundary within 0x{MAXBACK:X}"); continue
    blob=data[so:so+0x1000]
    print(f"=== enclosing fn of {a}: start=0x{start:08X} sha256(first0x1000)={hashlib.sha256(blob).hexdigest()[:16]} ===")
    n=0
    for ins in md.disasm(blob, start):
        mark='  <<<' if ins.address==va else ''
        print(f"0x{ins.address:08X}  {ins.mnemonic:<9} {ins.op_str}{mark}")
        n+=1
        if ins.mnemonic in ('ret','jmp') and ins.address>va: break
        if n>400: break

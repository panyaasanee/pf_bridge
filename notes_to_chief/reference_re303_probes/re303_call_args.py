#!/usr/bin/env python3
"""For each call site of TARGET, print the pushes in the preceding window (arg1 = last push)."""
import sys, struct, pefile
from capstone import *
from pathlib import Path
data=Path(sys.argv[1]).read_bytes()
pe=pefile.PE(data=data,fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
t=[s for s in pe.sections if s.Name.rstrip(b'\x00')==b'.text'][0]
tva=base+t.VirtualAddress; traw=t.PointerToRawData; tsz=t.SizeOfRawData
blob=data[traw:traw+tsz]
md=Cs(CS_ARCH_X86,CS_MODE_32)
target=int(sys.argv[2],16)
WIN=int(sys.argv[3],0) if len(sys.argv)>3 else 0x40
sites=[]
for i in range(0,tsz-5):
    if blob[i]==0xE8:
        rel=struct.unpack_from('<i',blob,i+1)[0]
        if tva+i+5+rel==target: sites.append(tva+i)
print(f"call sites of 0x{target:08X}: {len(sites)}")
for s in sites:
    start=s-WIN
    off=start-tva
    pushes=[]
    for ins in md.disasm(blob[off:off+WIN], start):
        if ins.mnemonic=='push': pushes.append(ins.op_str)
    print(f"0x{s:08X}  last-pushes(arg1..): {list(reversed(pushes))[:8]}")

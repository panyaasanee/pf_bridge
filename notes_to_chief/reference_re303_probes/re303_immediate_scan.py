#!/usr/bin/env python3
"""Find every instruction whose immediate operand equals VAL (any width) in .text."""
import sys, pefile
from capstone import *
from pathlib import Path
data=Path(sys.argv[1]).read_bytes()
pe=pefile.PE(data=data,fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
t=[s for s in pe.sections if s.Name.rstrip(b'\x00')==b'.text'][0]
tva=base+t.VirtualAddress; traw=t.PointerToRawData; tsz=t.SizeOfRawData
blob=data[traw:traw+tsz]
val=int(sys.argv[2],0)
mn=set(sys.argv[3].split(',')) if len(sys.argv)>3 else {'push','mov'}
md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=True
hits=0
# linear sweep is only a FINDER here, every hit is re-checked by context later
for start in range(0,2):
    for ins in md.disasm(blob[start:], tva+start):
        if ins.mnemonic in mn:
            for op in ins.operands:
                if op.type==CS_OP_IMM and op.imm==val:
                    print(f"0x{ins.address:08X}  {ins.mnemonic:<6} {ins.op_str}")
                    hits+=1
                    break
    break
print("hits:",hits)

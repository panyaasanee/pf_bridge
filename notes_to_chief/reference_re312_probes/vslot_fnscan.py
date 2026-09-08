#!/usr/bin/env python3
"""Function-anchored census of virtual-call sites for a given vtable slot.
Splits .text into blocks at CC-padding boundaries and disassembles each block
from its own start, so a single mis-decoded byte cannot hide a whole region
(which is what a flat linear scan does in this image)."""
import sys, re, pefile
from capstone import *
PATH=sys.argv[1]; SLOT=sys.argv[2].lower()
pe=pefile.PE(PATH, fast_load=True); IB=pe.OPTIONAL_HEADER.ImageBase
sec=[s for s in pe.sections if s.Name.rstrip(b'\x00')==b'.text'][0]
VA=IB+sec.VirtualAddress; raw=sec.PointerToRawData; size=sec.SizeOfRawData
data=open(PATH,'rb').read()[raw:raw+size]
md=Cs(CS_ARCH_X86,CS_MODE_32)
# function starts: first non-CC byte after a run of >=2 CC
starts=[0]; i=0
while True:
    j=data.find(b'\xcc\xcc', i)
    if j<0: break
    k=j
    while k<len(data) and data[k]==0xcc: k+=1
    if k<len(data): starts.append(k)
    i=k if k>j else j+2
starts=sorted(set(starts))
pat=re.compile(r'^(e[a-z]{2}), dword ptr \[(e(?!sp|bp)[a-z]{2}) \+ '+re.escape(SLOT)+r'\]$')
hits=[]
for n,s in enumerate(starts):
    end=starts[n+1] if n+1<len(starts) else len(data)
    if end-s<4: continue
    win=[]
    for ins in md.disasm(data[s:min(end+16,len(data))], VA+s):
        win.append(ins)
        if len(win)>10: win.pop(0)
        if ins.mnemonic in ('call','jmp') and re.match(r'^e[a-z]{2}$',ins.op_str):
            for j2 in range(len(win)-2,-1,-1):
                p=win[j2]
                if p.mnemonic=='mov':
                    m=pat.match(p.op_str)
                    if m and m.group(1)==ins.op_str:
                        hits.append((VA+s,p.address,ins.address,p.op_str,ins.mnemonic)); break
                if p.op_str.startswith(ins.op_str+','): break
print("blocks=%d  slot %s call sites=%d"%(len(starts),SLOT,len(hits)))
for fn,a,b,o,mn in hits:
    print("  fn 0x%08X  load 0x%08X (%s)  %s 0x%08X"%(fn,a,o,mn,b))
